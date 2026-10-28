"""(cx-systems) systems_bosshit.py <boss-state> <weapons comma> [frames] [flags9B]: equip each weapon with the Select+Down quick swap, chase and fire at the boss, and log every boss-HP drop (godmode, energy refilled each frame).  Run from the repo root.  Needs build/research/cx/cx-systems/su.py."""
import sys; sys.path.insert(0,'build/research/cx/cx-systems')
from su import *
from collections import Counter
st = sys.argv[1]; ws = [int(x) for x in sys.argv[2].split(',')]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 900
fl = int(sys.argv[4], 16) if len(sys.argv) > 4 else None
e = Emu('roms/cx_en.nes'); g = e.peek
for w in ws:
    e.load(cx.state(st)); e.run(1); cx.godmode(e); cx.give_all_weapons(e)
    if fl is not None: e.poke(0x9B, fl)
    ok = equip(e, w)
    hp = g(0x6c1); hits = []; died = None; php = g(0x6C0)
    for t in range(N):
        px, bx = g(0x460), g(0x461)
        face = 'RIGHT' if bx > px else 'LEFT'
        far = abs(bx - px) > 48
        ph = (t // 40) % 3
        b = []
        if ph == 0: b = [face] if far else []
        elif ph == 1: b = (['A'] if t % 40 < 16 else []) + ([face] if far or w == 7 else [])
        if w == 6: b += ['B'] if (t % 100) < 92 else []
        elif w == 7: b += ['B'] if ph == 1 and 8 <= t % 40 < 30 else []
        elif w == 2: b += ['B'] if t % 200 in (0, 1) else []
        elif t % 10 < 3: b.append('B')
        e.step(b)
        h = g(0x6c1)
        if h < hp: hits.append((t, hp - h))
        hp = h
        if g(0x6C0) == 0 and died is None: died = t
        if h == 0: break
        if w: e.poke(0x9B + w, 0x28)
    c = Counter(d for _, d in hits)
    print('%-18s w%-2d %-13s equip=%s flags=%02X hits %s total %d in %d frames, boss hp %d%s; first hits %s' % (
        st, w, cx.WEAPONS[w], ok, g(0x9B), dict(c), sum(d for _, d in hits), t + 1, g(0x6c1),
        (' PLAYER HP 0 at t%d' % died) if died is not None else '', hits[:12]))
