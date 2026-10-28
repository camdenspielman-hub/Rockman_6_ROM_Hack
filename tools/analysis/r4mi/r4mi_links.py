"""r4mi_links.py (r4mi-stages-b): dump 4MI screen-link tables. Usage: python3 -I tools/analysis/r4mi/r4mi_links.py [stage ...]
Dump 4MI vertical-link tables (bank $71: pointers $849E/$84AE by stage). 8-byte entries:
[type, screen, dir (4 = leaving downward, 8 = leaving upward), b3, b4, b5, b6, b7], terminated by bit7 in type."""
import sys
d = open('roms/r4mi_mmc5.nes', 'rb').read()[16:]
b = d[0x71 * 0x2000:0x72 * 0x2000]
def rd(a): return b[a - 0x8000]
names = 'BRIGHT TOAD DRILL PHARAOH RING DUST DIVE SKULL C1 C2 C3 C4 W1 W2 W3 W4'.split()
for st in [int(x) for x in sys.argv[1:]] or range(16):
    p = rd(0x849E + st) | rd(0x84AE + st) << 8
    print(f'{names[st]} ({st}) table ${p:04x}')
    if not (0x8000 <= p < 0xA000): print('  (outside bank)'); continue
    i = 0
    while rd(p + i) < 0x80 and i < 8 * 40:
        e = [rd(p + i + k) for k in range(8)]
        print('   type %d  screen %2d  %s  -> %s' % (e[0], e[1], {4: 'down', 8: 'up'}.get(e[2], e[2]), ' '.join('%02x' % x for x in e[3:])))
        i += 8
