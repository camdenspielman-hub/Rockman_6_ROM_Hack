"""engine_dis.py ROM BANK8000 BANKA000 ADDR N -- py65 disassembly with any two 8 KB banks mapped at $8000/$A000
and the last two banks fixed at $C000/$E000 (MMC3 PRG mode 0, as in Rockman CX: $3E/$3F). Use '-' to leave a slot
empty. Prints address, bytes and mnemonic. Example (CX dash code, player bank $3C at $8000):
    python3 -I tools/analysis/cx/engine_dis.py roms/cx_en.nes 3C 3D 8588 12
Import: from engine_dis import Dis; D = Dis('roms/cx_en.nes'); D.map(0x1C, 0x1D); D.p(0x8000, 20)
(docs/research/cx/engine.md, agent cx-engine)"""
import sys, os
_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.environ.get('R6_PYLIB', os.path.join(_REPO, '.pylib')))
from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler


class Dis:
    def __init__(s, rom='roms/cx_en.nes'):
        s.d = open(rom, 'rb').read()[16:]
        s.mpu = MPU(); s.m = s.mpu.memory
        nb = len(s.d) // 0x2000
        s.m[0xC000:0xE000] = list(s.d[(nb - 2) * 0x2000:(nb - 1) * 0x2000])
        s.m[0xE000:0x10000] = list(s.d[(nb - 1) * 0x2000:])
        s.da = Disassembler(s.mpu)

    def map(s, b8=None, bA=None):
        if b8 is not None: s.m[0x8000:0xA000] = list(s.d[b8 * 0x2000:(b8 + 1) * 0x2000])
        if bA is not None: s.m[0xA000:0xC000] = list(s.d[bA * 0x2000:(bA + 1) * 0x2000])

    def lines(s, pc, n):
        out = []
        for _ in range(n):
            l, t = s.da.instruction_at(pc)
            out.append(f'{pc:04X}  {" ".join(f"{s.m[pc + k]:02X}" for k in range(l)):9s} {t}'); pc += l
        return out

    def p(s, pc, n): print('\n'.join(s.lines(pc, n)))


if __name__ == '__main__':
    a = sys.argv
    D = Dis(a[1]); D.map(None if a[2] == '-' else int(a[2], 16), None if a[3] == '-' else int(a[3], 16))
    D.p(int(a[4], 16), int(a[5]))
