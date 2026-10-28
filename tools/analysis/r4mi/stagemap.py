"""4MI stage tools (r4mi-stages-a): section maps, collision, enemy tables, screen-graph explorer, boss damage.

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/r4mi')
    from emu import Emu; import cheats as C, stagemap as M
    e = Emu(C.ROM); e.load('build/research/r4mi/states/ring_cp0.state'); e.run(2)
    ims = M.render_section(e)            # list of PIL images, one per local screen of the loaded section
    print(M.ascii(e, [0, 1]))            # collision maps as text ('.' air '#' solid 'H' ladder '^' spikes ...)
    M.enemy_table(4)                     # {screen: [(x, y, type), ...]} from bank $20+stage ($B100/$B180/$B200/$B280)
    M.sections(4)                        # [[(global, local), ...], ...] from the $B500 screen->local table
    M.explore('build/research/r4mi/states/pharaoh_cp0.state', 'out/PX')   # BFS screen graph (godmode + teleports)
    M.select_weapon(e, 7); M.boss_damage(e, 7)   # weapon via controller-2 A; damage/i-frames vs slot 23

How 4MI stores a stage (found here; details in docs/research/r4mi/stages_a.md section 0):
  * bank $20+stage at $A000: $A000-$A3FF 16x16 block tiles (TL/TR/BL/BR planes), $A400 block attr (low 2 bits
    palette, high nibble collision), $B100 enemy screen / $B180 X / $B200 Y / $B280 type ($FF end), $B300 first enemy
    per screen, $B500 global screen -> local index in its section.
  * Sections (up to ~23 screens) are decompressed into WRAM on entry: $6000-$64FF blocks, $6500-$68FF 32x32
    metatiles (4 bytes TL TR BL BR), $6900+ screen layouts (64 bytes, 8x8 metatiles, row-major).
  * Object slots (24): $0330 X, $0348 X page, $0378 Y, $0450 HP (bit7 = shares the boss bar; 255/127 = no HP),
    $0528 flags (bit7 active), $0558 state, $05B8 invincibility timer (boss slot 23 -> $05CF).
  * Poking $A0 does not change the weapon's behaviour for every weapon; controller-2 A (pseudo-R) does.
Caveat: teleports can leave the camera on another page in scrolling rooms (player invisible / stuck). Prefer walking.
"""
import collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from PIL import Image
from emu import Emu, _chunks, nes_rgb
import cheats as C
ROM = C.ROM
CH = '.#H^L56789abcd=f'

def _bank(stage):
    d = open(ROM, 'rb').read()[16:]; return d[(0x20 + stage) * 0x2000:(0x21 + stage) * 0x2000]
def enemy_table(stage):
    b = _bank(stage); out = collections.OrderedDict(); i = 0
    while b[0x1100 + i] != 0xFF and i < 0x80:
        out.setdefault(b[0x1100 + i], []).append((b[0x1180 + i], b[0x1200 + i], b[0x1280 + i])); i += 1
    return out
def sections(stage):
    loc = list(_bank(stage)[0x1500:0x1530]); secs, cur = [], []
    for s, l in enumerate(loc):
        if cur and l == 0 and loc[s - 1] != 0: secs.append(cur); cur = []
        cur.append((s, l))
    return secs + [cur]
def local_index(e):
    s = e.peek(0x348); return _bank(e.peek(0x22))[0x1500 + s] if s < 0x30 else 0
def _nloc(e):
    s = e.peek(0x348)
    for sec in sections(e.peek(0x22)):
        if any(g == s for g, l in sec): return max(l for g, l in sec) + 1
    return 12
def collision(e):
    w = _chunks(e.save())['WRAM']; out = []
    for s in range(_nloc(e)):
        lay = w[0x900 + 64 * s:0x940 + 64 * s]; g = np.zeros((16, 16), np.uint8)
        for i, m in enumerate(lay):
            my, mx = divmod(i, 8)
            for k, (dy, dx) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
                g[my * 2 + dy, mx * 2 + dx] = w[0x400 + w[0x500 + 4 * m + k]] >> 4
        out.append(g)
    return out
def ascii(e, locals_=None):
    gs = collision(e); sel = locals_ if locals_ is not None else range(len(gs)); lines = []
    for s in sel:
        lines.append('#%d' % s); lines += [''.join(CH[v] for v in gs[s][y]) for y in range(15)]
    return '\n'.join(lines)
def render_section(e):
    ch = _chunks(e.save()); w, chr_, pal, ctrl = ch['WRAM'], ch['CHRR'], ch['PRAM'], ch['PPUR'][0]
    base = 256 if ctrl & 0x10 else 0
    t = np.frombuffer(chr_, np.uint8)[base * 16:(base + 256) * 16].reshape(256, 16)
    tiles = np.unpackbits(t[:, :8], axis=1).reshape(256, 8, 8) | (np.unpackbits(t[:, 8:], axis=1).reshape(256, 8, 8) << 1)
    rgb = np.array([nes_rgb(i) for i in range(64)], np.uint8)
    pals = [np.array([pal[0]] + [pal[p * 4 + k] for k in (1, 2, 3)], np.uint8) for p in range(4)]
    blocks = np.zeros((256, 16, 16, 3), np.uint8)
    for b in range(256):
        p = pals[w[0x400 + b] & 3]
        for k, (dy, dx) in enumerate(((0, 0), (0, 8), (8, 0), (8, 8))):
            blocks[b, dy:dy + 8, dx:dx + 8] = rgb[p[tiles[w[0x100 * k + b]]] & 0x3F]
    out = []
    for s in range(_nloc(e)):
        img = np.zeros((256, 256, 3), np.uint8)
        for i, m in enumerate(w[0x900 + 64 * s:0x940 + 64 * s]):
            my, mx = divmod(i, 8)
            for k, (dy, dx) in enumerate(((0, 0), (0, 16), (16, 0), (16, 16))):
                img[my * 32 + dy:my * 32 + dy + 16, mx * 32 + dx:mx * 32 + dx + 16] = blocks[w[0x500 + 4 * m + k]]
        out.append(Image.fromarray(img[:240]))
    return out
def objs(e):
    return [(i, e.peek(0x558 + i), e.peek(0x330 + i) + 256 * e.peek(0x348 + i), e.peek(0x378 + i), e.peek(0x450 + i))
            for i in range(24) if e.peek(0x528 + i) & 0x80]
def select_weapon(e, w, maxn=16):
    for k in range(maxn):
        if e.peek(0xA0) == w: return True
        e.step(['A'], player=1); e.step(['A'], player=1); e.step([], player=1); e.run(12)
    return e.peek(0xA0) == w
def boss_damage(e, w, slot=23, frames=900, dx=48, fire_every=6):
    """Chase the boss (teleport beside it at its height), fire weapon w; returns [(frame, damage, iframes_set)]."""
    C.godmode(e)
    for a in range(0xB1, 0xBE): e.freeze(a, 0x9C)
    e.poke(0x78F6, 1); e.poke(0x78C9, 1)
    for f in range(600):
        e.step([])
        if e.peek(0xBF) & 0x1F >= 28 and f > 60: break
    select_weapon(e, w); last = e.peek(0x450 + slot); out = []
    for f in range(frames):
        bx, by, px = e.peek(0x330 + slot), e.peek(0x378 + slot), e.peek(0x330)
        side = -1 if px < bx else 1
        if 16 < bx + side * dx < 240: e.poke(0x330, bx + side * dx)
        e.poke(0x378, min(max(by, 40), 200)); e.poke(0x3F0, 0)
        e.step(([('LEFT' if side > 0 else 'RIGHT')] if f % 30 == 0 else []) + (['B'] if f % fire_every == 0 else []))
        hp = e.peek(0x450 + slot)
        if hp != last: out.append((f, last - hp, e.peek(0x5B8 + slot))); last = hp
        if hp == 0 or hp > 200: break
    return out
def kill_all(e, maxf=1500):
    hit, lastf = 0, 0
    for f in range(maxf):
        tg = [(i, x, y, hp) for i, t, x, y, hp in objs(e) if i and hp not in (255, 127) and 0 < (hp & 0x7F) < 60]
        if not tg:
            if f > (120 if hit else 400) and f - lastf > 120: break
            e.step([]); continue
        hit, lastf = 1, f; i, x, y, hp = tg[0]; e.poke(0x450 + i, (hp & 0x80) | 1)
        sx = x - e.peek(0xF9) * 256 - e.peek(0xFC); px = sx - 40 if sx > 60 else sx + 40
        e.poke(0x330, max(16, min(240, px + e.peek(0xFC))) & 0xFF); e.poke(0x378, max(30, min(200, y)))
        e.step((['RIGHT'] if px < sx else ['LEFT']) + (['B'] if f % 6 == 0 else []))
    e.run(60)
def _tele_exit(e, d, k, btn, maxf=200):
    s0 = e.peek(0x348)
    if d == 'U': e.poke(0x330, k * 16 + 8); e.poke(0x378, 24)
    elif d == 'D': e.poke(0x330, k * 16 + 8); e.poke(0x378, 210)
    else: e.poke(0x330, 236 if d == 'R' else 20); e.poke(0x378, k * 16 + 8)
    for i in range(maxf):
        if d in 'RL' and i < 30: e.poke(0x378, k * 16 + 8); e.poke(0x3F0, 0)
        e.step(btn)
        if d == 'U' and i % 10 == 0 and e.peek(0x30) not in (3, 4): e.poke(0x378, 24)
        if e.peek(0x348) != s0: return e.peek(0x348)
def _walk_exit(e, btn, maxf=500):
    s0 = e.peek(0x348); last = None; stuck = jt = 0
    for i in range(maxf):
        x = e.peek(0x330); stuck = stuck + 1 if x == last else 0; last = x; b = list(btn)
        if jt > 0: b.append('A'); jt -= 1
        elif stuck > 5: jt = 22
        if stuck > 60: e.poke(0x378, max(20, e.peek(0x378) - 48)); stuck = 0
        e.step(b)
        if e.peek(0x348) != s0: return e.peek(0x348)
def explore(start, outprefix=None, maxn=60, killall=True, log=print):
    """BFS over screens: from each reached screen try ladder tops, open bottoms, open edge rows (both D-pad
    directions, for reversed controls) and plain walking. Returns [(src, how, dst)]; saves <outprefix>_g<NN>.state."""
    e = Emu(ROM); e.load(start); C.godmode(e); e.run(30)
    q = collections.deque([e.peek(0x348)]); states = {e.peek(0x348): e.save()}; edges = []
    while q and len(states) < maxn:
        s = q.popleft(); e.load(states[s]); C.godmode(e); e.run(2)
        if killall: kill_all(e)
        base = e.save(); g = collision(e)[local_index(e)]
        cand = [('U', c, ['UP']) for c in range(16) if g[0][c] in (2, 4)] + \
               [('D', c, []) for c in range(16) if g[14][c] != 1 and g[13][c] != 1] + \
               [(d, r, [b]) for d, col in (('R', 15), ('L', 0)) for r in range(1, 14)
                if g[r][col] != 1 and g[r - 1][col] != 1 for b in ('RIGHT', 'LEFT')]
        found = {}
        for d, k, btn in cand + [('w' + b[0], 0, [b]) for b in ('RIGHT', 'LEFT')]:
            e.load(base); C.godmode(e)
            dst = _walk_exit(e, btn) if d[0] == 'w' else _tele_exit(e, d, k, btn)
            if dst is not None and dst != s:
                found.setdefault((d, dst), []).append(k)
                if dst not in states:
                    e.run(40); states[dst] = e.save(); q.append(dst)
                    if outprefix: e.save(f'{outprefix}_g{dst:02d}.state')
        log(f'{s:2d}: ' + ', '.join(f'{d}{ks}->{dst}' for (d, dst), ks in sorted(found.items())))
        edges += [(s, d, dst) for (d, dst) in found]
    return edges
