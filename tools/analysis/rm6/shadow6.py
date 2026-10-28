"""Rockman 6 (J) "shadow frame" tracer: re-runs one emulator frame on py65 to get a code/data log (CDL).

FCEUmm (stable-retro) only exposes RAM and savestates, not a per-instruction trace. This module takes the
savestate at a frame boundary (CPU registers, 2 KB RAM, MMC3 registers), and re-executes the next frame on
py65 with a minimal NES around it: MMC3 PRG banking + scanline IRQ counter, NMI at the start of vblank,
$4016 joypad, OAM-DMA cycle cost, stubbed PPU/APU. It records every executed opcode address and every ROM
data read, each with the 8 KB bank mapped at that moment, plus the cycles the main thread was busy.

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
    from emu import Emu
    import shadow6
    e = Emu('roms/rm6j.nes'); e.load('build/research/rm6/states/stage_blizzard.state')
    sh = shadow6.Shadow('roms/rm6j.nes')
    r = sh.frame(e.save(), buttons=['RIGHT'])   # trace the frame e.step(['RIGHT']) is about to run
    e.step(['RIGHT']); print(sh.ram_diff(e))     # fidelity: bytes of RAM that differ from the real frame
    sh.exec_   # set of (bank, addr) opcode fetches;  sh.data = set of (bank, addr) ROM data reads

Timing model (FCEU): a retro frame starts at scanline 240; NMI ~118 CPU cycles later; MMC3 clocks at
dot ~260 of the pre-render line and of lines 0-239 while rendering is on. Accuracy is "good enough for
coverage"; ram_diff() is the check (0-2 differing bytes is typical).
"""
import os, struct, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_LIB = os.path.join(_HERE, '..', '..', '..', '.pylib')
if _LIB not in sys.path: sys.path.insert(0, _LIB)
from py65.devices.mpu6502 import MPU

LINE = 341 / 3.0
BTN_ORDER = ['A', 'B', 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT']

def chunks(state):
    out, i = {}, 16
    while i + 5 <= len(state):
        size = struct.unpack_from('<I', state, i + 1)[0]; j, end = i + 5, i + 5 + size
        while j + 8 <= end:
            name = state[j:j + 4].rstrip(b'\0').decode('latin1'); n = struct.unpack_from('<I', state, j + 4)[0]
            out[name] = state[j + 8:j + 8 + n]; j += 8 + n
        i = end
    return out

# instruction length by opcode (from py65's addressing-mode table)
_LEN = {'imp': 1, 'acc': 1, 'imm': 2, 'zpg': 2, 'zpx': 2, 'zpy': 2, 'inx': 2, 'iny': 2, 'rel': 2,
        'abs': 3, 'abx': 3, 'aby': 3, 'ind': 3}

class Mem:
    def __init__(self, sh): self.sh = sh
    def __getitem__(self, a):
        sh = self.sh
        if a < 0x2000: return sh.ram[a & 0x7FF]
        if a >= 0x8000:
            b = sh.map[(a >> 13) & 3]
            if not (sh.ilo <= a < sh.ihi): sh.data.add((b, a))
            return sh.rom[b * 0x2000 + (a & 0x1FFF)]
        if a < 0x4000:
            r = a & 7
            if r == 2:
                v = 0x80 if sh.cyc < 21 * LINE else 0x00
                return v
            return 0
        if a == 0x4016:
            v = (sh.pad >> sh.padbit) & 1 if sh.padbit < 8 else 1
            sh.padbit += 1; return v | 0x40
        if a < 0x4020: return 0
        if 0x6000 <= a < 0x8000: return sh.wram[a - 0x6000]
        return 0
    def __setitem__(self, a, v):
        sh = self.sh
        if a < 0x2000: sh.ram[a & 0x7FF] = v; return
        if a >= 0x8000: sh.mapper_write(a, v); return
        if a < 0x4000:
            r = a & 7
            if r == 1: sh.mask = v
            elif r == 7: sh.ppu_writes += 1
            return
        if a == 0x4014: sh.dma = True; return
        if a == 0x4016:
            if v & 1: sh.padbit = 0
            return
        if 0x6000 <= a < 0x8000: sh.wram[a - 0x6000] = v

class Shadow:
    def __init__(self, rom_path):
        raw = open(rom_path, 'rb').read(); self.rom = raw[16:]
        self.nbanks = len(self.rom) // 0x2000
        self.exec_ = set(); self.data = set(); self.ilo = self.ihi = 0
        self.wram = bytearray(0x2000)
        self.mpu = MPU(memory=Mem(self))
        self.lens = [_LEN.get(m[1], 1) for m in self.mpu.disassemble]
        self.stats = []
        self.prof = None      # set to collections.Counter() to accumulate CPU cycles per (bank, pc)

    # --- MMC3 ---------------------------------------------------------------
    def remap(self):
        last = self.nbanks - 1
        r6, r7 = self.regs[6] % self.nbanks, self.regs[7] % self.nbanks
        if self.cmd & 0x40: self.map = [last - 1, r7, r6, last]
        else: self.map = [r6, r7, last - 1, last]
    def mapper_write(self, a, v):
        z = a & 0xE001
        if z == 0x8000: self.cmd = v; self.remap()
        elif z == 0x8001: self.regs[self.cmd & 7] = v; self.remap()
        elif z == 0xC000: self.latch = v
        elif z == 0xC001: self.reload = True
        elif z == 0xE000: self.irq_en = False; self.irq_pending = False
        elif z == 0xE001: self.irq_en = True
    def clock(self):
        if self.counter == 0 or self.reload: self.counter = self.latch; self.reload = False
        else: self.counter -= 1
        if self.counter == 0 and self.irq_en: self.irq_pending = True

    # --- one frame ----------------------------------------------------------
    def load(self, state):
        c = chunks(state); g = lambda k, n=1: int.from_bytes(c[k][:n], 'little')
        m = self.mpu
        m.pc, m.a, m.x, m.y, m.sp, m.p = g('PC', 2), g('A'), g('X'), g('Y'), g('S'), g('P')
        self.ram = bytearray(c['RAM'])
        self.regs = list(c['REGS']); self.cmd = c['CMD'][0]
        self.latch = c['IRQL'][0]; self.counter = c['IRQC'][0]; self.irq_en = bool(c['IRQA'][0])
        self.reload = bool(c['IRQR'][0]) if 'IRQR' in c else False
        self.irq_pending = False
        self.mask = c['PPUR'][1]
        self.remap()

    def frame(self, state, buttons=None, idle=0xC581):
        """Trace the frame that starts at this savestate. Returns a stats dict."""
        self.load(state)
        m = self.mpu; mem = m.memory
        self.pad = 0
        for b in (buttons or []): self.pad |= 1 << BTN_ORDER.index(b.upper())
        self.padbit = 8; self.ppu_writes = 0; self.dma = False
        self.cyc = 0.0
        t_nmi = LINE + 4
        clocks = [21 * LINE + 87] + [(22 + k) * LINE + 87 for k in range(240)]
        ci = 0; nmi_done = False; end = 262 * LINE
        busy = 0.0; irqs = 0; idle_t = 0.0; nmi_entry = None
        start_cyc = m.processorCycles
        lens = self.lens; exe = self.exec_
        while self.cyc < end:
            # events
            if not nmi_done and self.cyc >= t_nmi:
                nmi_done = True
                if self.ram_ctrl_nmi(): m.nmi(); nmi_entry = self.cyc
            while ci < len(clocks) and self.cyc >= clocks[ci]:
                if self.mask & 0x18: self.clock()
                ci += 1
            if self.irq_pending and not (m.p & 0x04):
                self.irq_pending = False; m.irq(); irqs += 1
            pc = m.pc
            # fast-forward the main idle loop (LDA $F2 / BEQ) to the next event
            if pc == idle and self.ram[0xF2] == 0 and m.sp >= 0xF0:
                nxt = min([t for t in (t_nmi if not nmi_done else end,
                                       clocks[ci] if ci < len(clocks) else end, end)])
                if self.irq_pending and not (m.p & 0x04): nxt = self.cyc
                if nxt > self.cyc:
                    idle_t += nxt - self.cyc; self.cyc = nxt
                    exe.add((self.map[(pc >> 13) & 3], pc)); continue
            op = mem[pc] if pc < 0x8000 else self.rom[self.map[(pc >> 13) & 3] * 0x2000 + (pc & 0x1FFF)]
            if pc >= 0x8000: exe.add((self.map[(pc >> 13) & 3], pc))
            self.ilo, self.ihi = pc, pc + lens[op]
            c0 = m.processorCycles
            m.step()
            dc = m.processorCycles - c0
            if self.dma: dc += 513; self.dma = False
            self.cyc += dc
            if self.prof is not None: self.prof[(self.map[(pc >> 13) & 3] if pc >= 0x8000 else -1, pc)] += dc
        self.ilo = self.ihi = 0
        r = dict(irqs=irqs, idle=idle_t, ppu_writes=self.ppu_writes, busy=end - idle_t)
        self.stats.append(r); return r

    def ram_ctrl_nmi(self):
        # PPUCTRL shadow $FC bit 7 = NMI enable (the game writes $2000 from $FC/$F8); assume enabled
        return True

    def ram_diff(self, e, ignore=range(0x100, 0x200)):
        """bytes of RAM that differ between this shadow frame's end and the emulator (after e.step())."""
        real = e.ram()
        return [a for a in range(0x800) if a not in ignore and real[a] != self.ram[a]]

def bank_summary(exec_, data):
    """{bank: (n opcode addresses, n data bytes)}"""
    out = {}
    for b, a in exec_: out.setdefault(b, [0, 0])[0] += 1
    for b, a in data: out.setdefault(b, [0, 0])[1] += 1
    return out
