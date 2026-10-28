"""r4mi_dis.py: 4MI-aware 6502 disassembler (MMC5 build, 8 KB banks).

    python3 -I tools/analysis/r4mi/r4mi_dis.py <bank-hex> <start-hex> [count] [base-hex]

Knows 4MI's inline-argument helpers in the fixed bank, which break a plain linear disassembly:
  JSR $DF8C  far CALL : 3 inline bytes  hi, lo, bank   -> calls (hi:lo)+1 in that bank, returns after the bytes
  JSR $DF66  far JUMP : 3 inline bytes  (bank goes to $F6, i.e. target in $A000-$BFFF)
  JSR $DF5F  far JUMP : 3 inline bytes  (bank goes to $F5, target in $8000-$9FFF)
  JSR $C4B8  jump table: the words that follow are state handlers (printed, decoding stops)
The bank is mapped at <base> (default $8000; use a000 for banks that run at $A000). Fixed banks $7E/$7F at $C000/$E000.
Also importable: dis(bank, start, count, base) -> list of (pc, text).
"""
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', '..', '.pylib'))
from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler
ROM = os.path.join(_here, '..', '..', '..', 'roms', 'r4mi_mmc5.nes')

def _mpu(bank, base):
    rom = open(ROM, 'rb').read()[16:]
    m = MPU(); mem = m.memory
    mem[0xC000:0xE000] = list(rom[0x7E * 0x2000:0x7F * 0x2000]); mem[0xE000:0x10000] = list(rom[0x7F * 0x2000:0x80 * 0x2000])
    mem[base:base + 0x2000] = list(rom[bank * 0x2000:(bank + 1) * 0x2000])
    return m

def dis(bank, start, count=80, base=0x8000):
    m = _mpu(bank, base); mem = m.memory; d = Disassembler(m); pc = start; out = []
    for _ in range(count):
        if not (base <= pc < base + 0x2000) and pc < 0xC000: break
        l, t = d.instruction_at(pc)
        if mem[pc] == 0x20:
            tgt = mem[pc + 1] | mem[pc + 2] << 8
            if tgt in (0xDF8C, 0xDF66, 0xDF5F):
                hi, lo, bk = mem[pc + 3], mem[pc + 4], mem[pc + 5]
                kind = 'FARCALL' if tgt == 0xDF8C else 'FARJMP'
                out.append((pc, f'{kind} ${bk:02X}:{(hi << 8 | lo) + 1:04X}'))
                pc += 6
                if kind == 'FARJMP': out.append((pc, '---'));
                continue
            if tgt == 0xC4B8:
                out.append((pc, 'JSR $C4B8 (jump table)')); pc += 3; tab = []
                for k in range(64):
                    w = mem[pc + 2 * k] | mem[pc + 2 * k + 1] << 8
                    if not (0x8000 <= w < 0xC000): break
                    tab.append(f'{k:02X}:${w:04X}')
                out.append((pc, 'TABLE ' + ' '.join(tab))); break
        out.append((pc, t)); pc += l
        if t.startswith(('RTS', 'JMP', 'RTI')): out.append((pc, '---'))
    return out

if __name__ == '__main__':
    a = sys.argv
    bank = int(a[1], 16); start = int(a[2], 16); n = int(a[3]) if len(a) > 3 else 80
    base = int(a[4], 16) if len(a) > 4 else (0xA000 if start >= 0xA000 and start < 0xC000 else 0x8000)
    for pc, t in dis(bank, start, n, base): print(f'{pc:04X}  {t}')
