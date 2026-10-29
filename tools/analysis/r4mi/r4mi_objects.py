"""r4mi_objects.py: resolve 4MI script placements to $5E sub-ids and AI banks (critic, from bank $6C code).

    python3 -I tools/analysis/r4mi/r4mi_objects.py [stage] [--sub XX,...]

How 4MI places its own objects [code, bank $6C:$B522 + $BBC2]:
  * Placement types $08/$09/$0A/$0B (stage bank enemy table $B100-$B2FF) all spawn object $5E; the placement's HP
    byte ($38:$83BF) tells the resolver which kind: $08 -> HP $08, $09 -> $18, $0A -> $FF, $0B -> $FE.
  * $08: sub-id = $6C:$B5C2 + 48*stage + screen   (one $08 object type per screen; the Y value is that object's parameter)
    $09: sub-id = $6C:$B8C2 + 48*stage + screen
    $0A: sub-id = $6C:$B5A0[param], real Y = $6C:$B5A9[param]
    $0B: sub-id = $6C:$B5B2[stage]
  * sub-id -> AI: entry lo $6C:$BBDC, hi $6C:$BCCA, bank $6C:$BDB8 (238 entries); the AI runs with that bank at $A000.
Placement types $31/$32 are vanilla RM4's item-giving Eddie (object $42), $33 is a 254-HP spring robot (object $46).
"""
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
ROM = os.path.join(_here, '..', '..', '..', 'roms', 'r4mi_mmc5.nes')
r = open(ROM, 'rb').read()[16:]
def rd(b, a, n, base=0xA000): o = b * 0x2000 + a - base; return r[o:o + n]
LO, HI, BK = rd(0x6C, 0xBBDC, 0xEE), rd(0x6C, 0xBCCA, 0xEE), rd(0x6C, 0xBDB8, 0xEE)
def ai(sub): return (BK[sub], HI[sub] << 8 | LO[sub]) if sub < 0xEE else (None, None)
def enemy_table(stage):
    b = r[(0x20 + stage) * 0x2000:(0x21 + stage) * 0x2000]; out = []; i = 0
    while b[0x1100 + i] != 0xFF and i < 0x80:
        out.append((b[0x1100 + i], b[0x1180 + i], b[0x1200 + i], b[0x1280 + i])); i += 1
    return out
def resolve(stage, screen, ptype, param):
    if ptype == 0x08: return rd(0x6C, 0xB5C2 + 48 * stage + screen, 1)[0]
    if ptype == 0x09: return rd(0x6C, 0xB8C2 + 48 * stage + screen, 1)[0]
    if ptype == 0x0A: return rd(0x6C, 0xB5A0 + param, 1)[0] if param < 9 else None
    if ptype == 0x0B: return rd(0x6C, 0xB5B2 + stage, 1)[0]
    return None
def script_objects(stage):
    for scr, x, y, t in enemy_table(stage):
        if t in (0x08, 0x09, 0x0A, 0x0B):
            s = resolve(stage, scr, t, y); yield scr, x, y, t, s, ai(s) if s is not None else (None, None)
if __name__ == '__main__':
    args = sys.argv[1:]; want = None
    if '--sub' in args:
        i = args.index('--sub'); want = {int(v, 16) for v in args[i + 1].split(',')}; args = args[:i] + args[i + 2:]
    stages = [int(args[0])] if args else range(16)
    for st in stages:
        for scr, x, y, t, s, (b, e) in script_objects(st):
            if want is None or s in want:
                print('stage %2d screen %2d x %3d param %3d type %02x -> sub %s  AI %s' % (st, scr, x, y, t, '%02x' % s if s is not None else '--', '%02x:%04x' % (b, e) if b is not None else '-'))
