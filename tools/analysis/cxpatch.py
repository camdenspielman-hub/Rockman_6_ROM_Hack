# Rebuilds Rockman CX without the Windows patcher (verified byte-identical to the
# official JP output, MD5 a2542f53663706837f3a5c99bb071217).
# The patcher's preprocessing: keep RM2's first 224 KB, insert 256 KB of zeros,
# then append RM2's last 32 KB (16 KB banks 14-15, incl. the MMC1 fixed bank).
# usage: cxpatch.py "Rockman 2 (J).nes" "Rockman CX.ips" out.nes
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ips import apply_ips
rom = open(sys.argv[1], 'rb').read()
h, prg = rom[:16], rom[16:]
assert len(prg) == 0x40000, 'expected a 256 KB Rockman 2 (J) PRG'
base = h + prg[:-0x8000] + bytes(0x40000) + prg[-0x8000:]
out, recs = apply_ips(base, open(sys.argv[2], 'rb').read())
open(sys.argv[3], 'wb').write(out); print(len(out), 'bytes,', len(recs), 'IPS records')
