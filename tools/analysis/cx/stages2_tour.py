"""(cx-stages-2) Go-Explore autoplayer that keeps each cell's input history, so the best route can be replayed
and recorded (see stages2_replay.py). Options: NOOH=1 env var disables the one-hit-kill cheat (needed when lifts or
other useful objects have HP). Outputs go to build/research/cx/cx-stages-2/.
Go-Explore with input history + one-hit-kill cheat + intra-room progress score.
python3 -I tools/analysis/cx/stages2_tour.py <start-state> <target-room-hex|boss> <budget> <tag> [rev|flat:<hi-room>|up] [seed]
Writes <tag>.path (json [act, n]), <tag>_end.state, and <tag>_r<room>.state at the first arrival in every room."""
import sys, json, random, time, os
sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu
import cheats as cx, stagemap as sm
D = 'build/research/cx/cx-stages-2/'
ACTS = cx.ACTS

def onehit(e):
    for s in range(16, 32):
        if e.peek(0x420 + s) & 0x80 and e.peek(0x6c0 + s) > 1: e.poke(0x6c0 + s, 1)

def make_score(stage, rev):
    rom = sm.load_rom(); d = {}
    for (a, z, f) in sm.segments(rom, stage):
        for r in range(a, z + 1):
            d[r] = 'x' if r != z else ('u' if f & 0x80 else 'd' if f & 0x60 else 'x')
    def sc(r):
        rm = r[0x440]
        if rev:
            return (0x40 - rm) + (255 - r[0x460]) / 512.0
        m = d.get(rm, 'x')
        p = r[0x460] if m == 'x' else (r[0x4a0] if m == 'd' else 255 - r[0x4a0])
        return rm + p / 512.0
    return sc

def step(e, b, oh):
    e.step(b)
    if oh and not os.environ.get('NOOH'): onehit(e)

def run_explore(e, budget, score, done, seed=0, log=print, xs=4, ys=5, oh=not os.environ.get('NOOH'), tag='x'):
    rnd = random.Random(seed)
    cx.godmode(e); e.step(None)
    key = lambda r: (r[0x2a], r[0x440], r[0x460] >> xs, r[0x4a0] >> ys)
    r = cx.ram(e); c0 = key(r)
    arch = {c0: [e.save(), 0, 0, score(r), None]}
    total, it, best, t0 = 0, 0, score(r), time.time(); rooms = {r[0x440]}
    while total < budget:
        it += 1
        keys = list(arch); top = max(arch[k][3] for k in keys)
        w = [(6.0 ** (arch[k][3] - top)) / (1 + arch[k][2]) ** 0.5 for k in keys]
        k = rnd.choices(keys, w)[0]; a = arch[k]; a[2] += 1
        e.load(a[0]); fr = a[1]; hist = a[4]; nact = rnd.randint(2, 6); spent = 0; i = 0; c = k
        while i < nact or (c == k and spent < 1500):
            i += 1
            act = rnd.choice(ACTS); n = rnd.randint(3, 32)
            mash = any(b.endswith('*') for b in act)
            for j in range(n):
                step(e, cx._press(act, j) if mash else act, oh)
            fr += n; total += n; spent += n; hist = (hist, ACTS.index(act), n)
            r = cx.ram(e); c = key(r)
            if c not in arch or arch[c][1] > fr:
                v = score(r)
                if v > best + 0.25 or int(v) > int(best):
                    log('it %d frames %d score %.2f cell %s (%.0fs)' % (it, total, v, c, time.time() - t0))
                best = max(best, v)
                arch[c] = [e.save(), fr, 0, v, hist]
                if r[0x440] not in rooms:
                    rooms.add(r[0x440]); e.save(D + '%s_r%02X.state' % (tag, r[0x440]))
            if done(r):
                log('done it %d frames %d cell %s' % (it, total, c)); return hist, arch
    kb = max(arch, key=lambda k: (arch[k][3], -arch[k][1]))
    return arch[kb][4], arch

def flatten(h):
    out = []
    while h is not None:
        h, a, n = h; out.append((a, n))
    return out[::-1]

if __name__ == '__main__':
    start, tgt, budget, tag = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else ''
    rev = mode == 'rev'
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    e = Emu('roms/cx_en.nes'); e.load(cx.state(start) if '/' not in start else start); e.run(1)
    st0 = e.peek(0x2a)
    score = make_score(st0, rev)
    if mode.startswith('flat'):          # flat:<hi-room>: novelty search, score only for rooms below <hi-room>
        hi = int(mode.split(':')[1], 16); score = lambda r: max(0, hi - r[0x440])
    if mode.startswith('up'):            # up: score = room + (255-y)/512 everywhere (vertical climbs)
        score = lambda r: r[0x440] + (255 - r[0x4a0]) / 512.0
    if tgt == 'boss':
        done = lambda r: r[0x2a] == st0 and 0 < r[0x6c1] <= 0x40 and r[0x421] & 0x80
    else:
        T = int(tgt, 16); dn = rev or mode.startswith('flat'); done = lambda r: (r[0x440] <= T) if dn else (r[0x440] >= T)
    h, arch = run_explore(e, budget, score, done, seed=seed, log=lambda s: print(s, flush=True), tag=tag)
    path = flatten(h)
    json.dump(path, open(D + tag + '.path', 'w'))
    e.save(D + tag + '_end.state')
    print('END', len(arch), 'cells', sum(n for _, n in path), 'frames', cx.info(e), flush=True)
