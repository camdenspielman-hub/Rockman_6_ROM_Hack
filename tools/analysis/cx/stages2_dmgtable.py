"""(cx-stages-2) python3 -I dmgtable.py <boss-state> [frames]: per weapon 0-11, damage per hit on the boss ($06C1) under a chase-and-fire policy."""
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu
import cheats as cx
from collections import Counter
st = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 900
e = Emu('roms/cx_en.nes'); g = e.peek
for w in range(0, 12):
    e.load(cx.state(st)); e.run(1); cx.godmode(e); cx.give_all_weapons(e)
    for k in range(16):
        if g(0xA9) == w: break
        e.run(2, ['SELECT', 'DOWN']); e.run(12)
    if g(0xA9) != w: print('w', w, 'could not equip'); continue
    hp = g(0x6c1); hits = Counter(); t0 = None
    for t in range(N):
        px, bx = g(0x460), g(0x461)
        face = 'RIGHT' if bx > px else 'LEFT'
        far = abs(bx - px) > 48
        ph = (t // 40) % 3
        b = []
        if ph == 0: b = [face] if far else []
        elif ph == 1: b = (['A'] if t % 40 < 16 else []) + ([face] if far else [])
        else: b = []
        if t % 10 < 3: b.append('B')
        if w == 7 and ph == 1 and t % 40 in range(8, 11): b.append('B')
        e.step(b)
        h = g(0x6c1)
        if h < hp:
            hits[hp - h] += 1
            if t0 is None: t0 = t
        hp = h
        if h == 0: break
    for n in range(1, 12): e.poke(0x9b + n, 0x28)
    print('w %2d %-14s dmg/hit %s  total %d in %d frames, boss hp left %d' % (w, cx.WEAPONS.get(w, '?'), dict(hits), sum(k * v for k, v in hits.items()), t + 1, g(0x6c1)))
