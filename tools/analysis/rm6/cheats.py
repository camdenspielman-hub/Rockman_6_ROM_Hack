"""Rockman 6 (J) cheat + warp + password + autoplay helpers.  Docs: docs/research/rm6/cheats.md, ram.md.

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
    from emu import Emu
    import cheats as c6
    e = Emu('roms/rm6j.nes'); e.load(c6.state('stage_select'))
    c6.give_all(e)                # every weapon, adaptor, Beat plate, the Energy Balancer, E-tanks, lives
    c6.warp(e, 'tomahawk')        # stage start (or c6.warp(e, 5, ckpt=1) for its mid-stage checkpoint)
    c6.godmode(e)                 # frozen HP / lives / invincibility timer
    best, arch = c6.explore(e, budget=200000)   # Go-Explore autoplayer, returns the best savestate

Only one Emu per process (stable-retro limit): reuse it with e.load().
After e.load(), run one frame before e.shot() (the frame buffer is not in the state).
"""
import os, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STATES = os.path.join(REPO, 'build', 'research', 'rm6', 'states')

# ---- RAM map (see docs/research/rm6/ram.md for how each one was verified) ----------------------
PAD, PAD_NEW = 0x40, 0x42      # joypad 1 held / newly pressed (A=80 B=40 SELECT=20 START=10 U=08 D=04 L=02 R=01)
STAGE = 0x51                   # stage id 0-15 (STAGES below)
CAM_X, CAM_SCR = 0x56, 0x57    # camera X pixel / camera screen (= current screen number in the level)
FORM = 0x9B                    # 0 normal, 1 Jet Rockman, 2 Power Rockman
JET_FUEL = 0x9C                # Rush Jet hover fuel ($13 full, counts down while hovering)
PSTATE = 0x94                  # player state: 0 stand, 1 tiptoe, 2 walk, 4 ladder, 7 airborne, ...
IFRAMES = 0xA2                 # invincibility timer ($3C on hit, counts down; non-zero = no damage)
LIVES = 0xA9                   # lives (shown as-is in the menu, 0-9; 1-up caps at 9)
GAMEFLOW = 0xF0                # main-loop exit code: 1 stage clear, 2 respawn at checkpoint, 3 game over
FRAME = 0xF3                   # frame counter
# object table: 23 slots ($17), slot 0 = player, field n of slot k at base_n + k
NSLOTS = 0x17
O_TYPE, O_FLAGS, O_DIR, O_HP = 0x03A0, 0x03B7, 0x03CE, 0x03E5
O_AIHI, O_AILO, O_AIBANK, O_ANIBANK = 0x0413, 0x042A, 0x0441, 0x0458
O_XSCR, O_X, O_XSUB = 0x046F, 0x0486, 0x049D
O_YSCR, O_Y, O_YSUB = 0x04B4, 0x04CB, 0x04E2
O_VYLO, O_VYHI = 0x05B1, 0x05C8   # for the player; other objects use $05B1-$0624 as AI variables
HP = O_HP                      # player HP, full = $1B (27); negative = dead
X, Y, XSCR = O_X, O_Y, O_XSCR
DIR = O_DIR                    # player facing: 1 right, 2 left
BOSSHP = O_HP + 8              # $03ED: the HUD boss bar reads slot 8's HP (bar shown while $0642 != 0)
BOSSBAR = 0x0642
ENERGY = 0x0688                # $0688+slot: weapon energy, $80 = not owned, else 0..$1B (slot 0 = buster)
FLAGS = 0x0692                 # $0692-$0695: password/progress bytes, 3 bits each (see BOSS_BIT)
BALANCER = 0x0696              # Energy Balancer owned (non-zero)
WEAPON = 0x0699                # current weapon slot 0-9 (menu cursor)
ETANKS = 0x06A1                # E-tanks (0-9)
CKPT_SCR, CKPT_CHR, CKPT_PAL = 0x0684, 0x0685, 0x0686   # respawn screen + its CHR set / palette ids
PW_GRID = 0x0300               # password grid, 36 cells A1..F6 (row-major), non-zero = orb

STAGES = {0: 'blizzard', 1: 'wind', 2: 'plant', 3: 'flame', 4: 'yamato', 5: 'tomahawk', 6: 'knight',
          7: 'centaur', 8: 'mrx1', 9: 'mrx2', 10: 'mrx3', 11: 'mrx4', 12: 'wily1', 13: 'wily2',
          14: 'wily3', 15: 'wily4'}
STAGE_ID = {v: k for k, v in STAGES.items()}
WEAPONS = ['R.BUSTER', 'Y.SPEAR', 'W.STORM', 'B.ATTACK', 'F.BLAST', 'PLANT.B', 'KNIGHT.C', 'SILVER.T',
           'C.FLASH', 'BEAT']
# stage -> (flags byte index, bit) set when its boss is beaten; stages 4-7 have a second boss room
# (the Beat-plate route) that sets bit 2 instead (bit 2 implies bit 1).  Tables $3F:$F6B3/$F6BB/$F6C3.
BOSS_BIT = {0: (0, 1), 1: (1, 1), 2: (3, 1), 3: (2, 1), 4: (1, 2), 5: (0, 2), 6: (3, 2), 7: (2, 2)}
PLATE = {5: 'B', 4: 'E', 6: 'A', 7: 'T'}      # Beat plate letter per stage (stage-select portrait)
ALT_BOSS_SCREEN = {4: 0x1D, 5: 0x1F, 6: 0x1A, 7: 0x17}   # boss room screen of the plate route ($3F:$F518)
# stage-select cursor ($04 col, $05 row) per stage
SEL_POS = {0: (0, 0), 1: (1, 0), 3: (2, 0), 2: (0, 1), 5: (2, 1), 4: (0, 2), 6: (1, 2), 7: (2, 2)}

# checkpoints: stage -> list of (screen, chr id, palette id): [0] stage start, [1] mid-stage checkpoint,
# [2] boss shutter (entering the boss room sets $0684 = boss screen - 1).  Values written by the game
# itself when the autoplayer got there, except the ones marked 'rule' (derived from the screen-script
# exits, see cheats.md) - all were checked by warping there.
CHECKPOINTS = {
    0: [(0, 0, 0), (0x0D, 0x85, 0x1A), (0x17, 0x84, 0x1C)],   # Blizzard
    1: [(0, 0, 0), (0x08, 0x8D, 0x17), (0x14, 0x8E, 0x3D)],   # Wind
    2: [(0, 0, 0), (0x09, 0x92, 0x32)],                       # Plant
    3: [(0, 0, 0), (0x0E, 0x87, 0x1F), (0x16, 0x87, 0x1F)],   # Flame
    4: [(0, 0, 0), (0x0A, 0x98, 0x5B)],                       # Yamato (rule)
    5: [(0, 0, 0), (0x0A, 0x95, 0x95)],                       # Tomahawk
    6: [(0, 0, 0), (0x0B, 0x00, 0x78), (0x16, 0x00, 0x7B)],   # Knight
    7: [(0, 0, 0), (0x0A, 0x00, 0xA7), (0x19, 0x00, 0xA9)],   # Centaur
    8: [(0, 0, 0), (0x0E, 0xB9, 0x6C)],                       # Mr. X 1
    9: [(0, 0, 0), (0x08, 0x00, 0x00), (0x10, 0xB8, 0x00)],   # Mr. X 2
    10: [(0, 0, 0), (0x08, 0x00, 0x00), (0x10, 0xB4, 0xD0)],  # Mr. X 3
    11: [(0, 0, 0), (0x09, 0xC4, 0x00)],                      # Mr. X 4 (rule)
    12: [(0, 0, 0), (0x0E, 0x00, 0x81), (0x12, 0x8B, 0x81)],  # Wily 1
    13: [(0, 0, 0), (0x0A, 0x00, 0x00)],                      # Wily 2 (rule)
    14: [(0, 0, 0), (0x08, 0xA9, 0x00)],                      # Wily 3
    15: [(0, 0, 0)],                                          # Wily 4 (capsule stage)
}


def state(name):
    """Path of a shared savestate in build/research/rm6/states/."""
    p = name if name.endswith('.state') else name + '.state'
    return p if os.path.isabs(p) else os.path.join(STATES, p)


def ram(e):
    m = e.d.memory.blocks
    return m[0] + m[1024]


def sid(stage):
    return STAGE_ID[stage] if isinstance(stage, str) else stage


def info(e):
    """One-line summary of the interesting RAM."""
    g = e.peek
    return ('stage %02X(%s) scr %02X x %02X:%02X y %02X hp %d lives %d etanks %d wpn %d form %d flags %s '
            'eb %d ckpt %02X/%02X/%02X state %02X boss %d/%d' % (
                g(STAGE), STAGES.get(g(STAGE), '?'), g(CAM_SCR), g(XSCR), g(X), g(Y), g(HP), g(LIVES),
                g(ETANKS), g(WEAPON), g(FORM), ''.join('%d' % g(FLAGS + i) for i in range(4)), g(BALANCER),
                g(CKPT_SCR), g(CKPT_CHR), g(CKPT_PAL), g(PSTATE), g(BOSSBAR), g(BOSSHP)))


# ---- cheats -------------------------------------------------------------------------------------
def godmode(e, hp=True, lives=True, iframes=True, fuel=False):
    """Freeze HP at full, lives at 9 and the invincibility timer at 2 (no damage, no knockback, no
    visible blinking).  fuel=True also freezes the Rush Jet fuel.  Pits and spikes still kill."""
    if hp: e.freeze(HP, 0x1B)
    if lives: e.freeze(LIVES, 9)
    if iframes: e.freeze(IFRAMES, 2)
    if fuel: e.freeze(JET_FUEL, 0x13)


def nogod(e):
    e.unfreeze()


def refill(e):
    """Full HP and full energy for every weapon already owned."""
    e.poke(HP, 0x1B)
    for s in range(10):
        if not e.peek(ENERGY + s) & 0x80: e.poke(ENERGY + s, 0x1B)


def set_progress(e, beaten=range(8), plates=(4, 5, 6, 7), balancer=True):
    """Write the progress bytes $0692-$0695 (bosses beaten, Beat plates) and the Energy Balancer flag.
    Weapons follow from these bytes when a stage starts; call give_weapons() to set them right away."""
    f = [0, 0, 0, 0]
    for s in beaten:
        i, b = BOSS_BIT[s]; f[i] |= b
    for s in plates:
        i, _ = BOSS_BIT[s]; f[i] |= 6
    for i in range(4): e.poke(FLAGS + i, f[i])
    e.poke(BALANCER, 1 if balancer else 0)


def give_weapons(e, slots=range(10)):
    for s in slots: e.poke(ENERGY + s, 0x1B)


def give_all(e, etanks=9, lives=9):
    """All 8 bosses beaten, all 4 Beat plates (Beat), both Rush adaptors, the Energy Balancer, full
    energy for every weapon, E-tanks and lives.  On the stage select this also marks every portrait."""
    set_progress(e)
    give_weapons(e)
    e.poke(ETANKS, etanks); e.poke(LIVES, lives); e.poke(HP, 0x1B)


# ---- passwords ----------------------------------------------------------------------------------
# Decoder $3F:$F3D0, display $3F:$F477.  The four key cells E5 E6 F5 F6 select one of four tables
# (two for "no Energy Balancer", two for "with"); every one of the 4 progress bytes is then one orb in
# the grid (36 cells, A1..F6).  A password is always exactly 5 orbs.
def _rom():
    return open(os.path.join(REPO, 'roms', 'rm6j.nes'), 'rb').read()[16:]


def _t(rom, a, n):
    o = 0x3F * 0x2000 + a - 0xE000; return list(rom[o:o + n])


_PW = None


def _pw():
    global _PW
    if _PW is None:
        r = _rom()
        _PW = dict(KEYIDX=_t(r, 0xF573, 16), OFF=_t(r, 0xF583, 4), EBV=_t(r, 0xF587, 4),
                   T1=_t(r, 0xF593, 0x90), T2=_t(r, 0xF623, 0x90))
    return _PW


KEYCELL = {0: 0x1D, 1: 0x1C, 2: 0x22, 3: 0x23}     # table variant -> its key cell (E6 E5 F5 F6)


def cellname(i): return 'ABCDEF'[i // 6] + str(i % 6 + 1)


def cellindex(n): return 'ABCDEF'.index(n[0].upper()) * 6 + int(n[1]) - 1


def pw_encode(flags, balancer=False, variant=None):
    """flags = 4 progress bytes (0-7 each, as in $0692-$0695) -> sorted list of 5 cell names."""
    P = _pw(); v = variant if variant is not None else (1 if balancer else 0)
    assert P['EBV'][v] == (1 if balancer else 0), 'variant/balancer mismatch'
    cells = [KEYCELL[v]]
    for x in range(4):
        want = flags[x] & ~2 if flags[x] & 4 else flags[x]     # bit 2 implies bit 1; tables hold 0,1,4,5,..
        for y in range(36):
            if P['T1'][P['OFF'][v] + y] == x and P['T2'][P['OFF'][v] + y] in (flags[x], want):
                cells.append(y); break
        else:
            raise ValueError('no cell for byte %d value %d' % (x, flags[x]))
    return [cellname(c) for c in sorted(cells)]


def pw_decode(cells):
    """list of cell names (or indices) -> (flags[4], balancer) or None if invalid."""
    P = _pw(); s = {cellindex(c) if isinstance(c, str) else c for c in cells}
    k = (0x1C in s) << 3 | (0x1D in s) << 2 | (0x22 in s) << 1 | (0x23 in s)
    v = P['KEYIDX'][k]
    if v >= 0x80: return None
    f = [None] * 4
    for y in sorted(s, reverse=True):
        x = P['T1'][P['OFF'][v] + y]
        if x >= 0x80: continue
        if f[x] is not None: return None
        f[x] = P['T2'][P['OFF'][v] + y]
    if None in f: return None
    return [b | ((b & 4) >> 1) for b in f], P['EBV'][v]


def progress_flags(beaten=(), plates=()):
    f = [0, 0, 0, 0]
    for s in beaten:
        i, b = BOSS_BIT[s]; f[i] |= b
    for s in plates:
        i, _ = BOSS_BIT[s]; f[i] |= 6
    return f


# ---- warps --------------------------------------------------------------------------------------
def _xpos(e): return e.peek(XSCR) << 8 | e.peek(X)


def playable(e, n=8):
    """True if RIGHT/LEFT input moves the player (compared with no input).  Restores the state."""
    s = e.save()
    e.run(n); x0 = _xpos(e); e.load(s)
    e.run(n, ['RIGHT']); x1 = _xpos(e); e.load(s)
    e.run(n, ['LEFT']); x2 = _xpos(e); e.load(s)
    return abs(x1 - x0) >= 3 or abs(x2 - x0) >= 3


def wait_playable(e, limit=3000, step=10):
    for t in range(0, limit, step):
        e.run(step)
        if playable(e): return t + step
    return None


def in_stage(e):
    """The stage main loop is running: object slot 0 is the player (type 4, AI bank $38; Wily 4 starts
    with type 3) rather than a menu cursor (title $2C, stage select $01, password $50)."""
    return e.peek(O_TYPE) in (3, 4) and e.peek(STAGE) < 16 and e.peek(GAMEFLOW) == 0


def warp(e, stage, ckpt=0, base='stage_blizzard', wait=True, screen=None, chr_=None, pal=None):
    """Teleport by RAM: from any in-stage state (else `base` is loaded first), set the stage id and the
    checkpoint, then raise the respawn code ($F0 = 2).  The game reloads the stage at that checkpoint,
    exactly as after a death (no boss-intro screen, no life lost).  ckpt indexes CHECKPOINTS[stage];
    or pass screen/chr_/pal directly.  Returns frames until playable."""
    st = sid(stage)
    if not in_stage(e): e.load(state(base)); e.run(2)
    scr, c, p = CHECKPOINTS[st][ckpt] if screen is None else (screen, chr_ or 0, pal or 0)
    e.poke(STAGE, st); e.poke(CKPT_SCR, scr); e.poke(CKPT_CHR, c); e.poke(CKPT_PAL, p)
    e.poke(GAMEFLOW, 2)
    return wait_playable(e) if wait else None


def clear_stage(e, wait=True):
    """Raise 'stage clear' ($F0 = 1).  For fortress stages (8-14) the game moves on to the next one
    with its normal transition; for Robot Master stages it returns to the stage select (no weapon given
    unless the flags were set)."""
    e.poke(GAMEFLOW, 1)
    return wait_playable(e, limit=6000) if wait else None


# ---- autoplay -----------------------------------------------------------------------------------
ACTS = [['RIGHT'], ['RIGHT', 'A'], ['LEFT'], ['LEFT', 'A'], ['UP'], ['DOWN'], ['A'], [],
        ['UP', 'RIGHT'], ['UP', 'LEFT'], ['DOWN', 'RIGHT'], ['DOWN', 'LEFT'],
        ['RIGHT', 'B*'], ['LEFT', 'B*'], ['B*'], ['RIGHT', 'A', 'B*'], ['LEFT', 'A', 'B*']]


def _press(act, j):
    out = []
    for b in act:
        if b.endswith('*'):
            if (j // 3) % 2 == 0: out.append(b[:-1])
        else:
            out.append(b)
    return out


OBJWIN = 0x0649   # first entry of the level object list in range; advances along the level path, also
                  # through vertical sections where $57/$046F stay put (free vertical scrolling, camera Y $58)
CAM_Y, CAM_YSCR = 0x58, 0x50


def _cell(r, xshift=5, yshift=5):
    return (r[STAGE], r[OBJWIN], r[XSCR], r[X] >> xshift, r[Y] >> yshift, r[CAM_Y] >> 6, r[CAM_YSCR])


def progress(r):
    """Default explore score: the object-list window ($0649).  X is deliberately left out: many paths
    turn back left after a ladder, and an X term starves those cells (novelty does the rest)."""
    return r[OBJWIN]


DEATH_AI = {(0x8F, 0x13): 'pit', (0x8E, 0x7F): 'hp'}   # player AI pointer ($0413/$042A, bank $38) while dying


def dying(r):
    """'pit' / 'hp' while the player's death sequence runs (60 / 240 frames, then $F0 = 2), else None."""
    return DEATH_AI.get((r[O_AIHI], r[O_AILO]))


def safe(r):
    """Default explore keep(): drop rollouts that die or leave the stage loop.  (Y >= $F0 is not a death
    test: falling into the next screen of a vertical shaft also passes there.)"""
    return r[GAMEFLOW] == 0 and dying(r) is None


def explore(e, budget=200000, seed=0, acts=ACTS, done=None, keep=None, log=print, xshift=5, yshift=5,
            frontier=4.0, god=True, cell=None, checkpoint=None, idle_max=600, score=progress):
    """Go-Explore autoplayer (same design as tools/analysis/cx/cheats.py).  Archive of cells
    (stage, player screen, x>>xshift, y>>yshift[, extra]) -> savestate; repeatedly restore a cell, biased
    to the best score (default progress(): screen, then x) and play random held-button macros.  done(e, r) -> True stops; keep(r) -> False drops the rollout; cell(r) adds an
    extra key.  Returns (best_state_bytes, archive)."""
    rnd = random.Random(seed)
    if god: godmode(e)
    e.step(None)
    key = (lambda r: _cell(r, xshift, yshift) + ((cell(r),) if cell else ()))
    sc = score or progress
    keep = keep or safe
    r = ram(e); c0 = key(r)
    arch = {c0: [e.save(), 0, 0, sc(r)]}
    total, it, best, t0 = 0, 0, sc(r), time.time()
    c = c0
    while total < budget:
        it += 1
        keys = list(arch); top = max(arch[k][3] for k in keys)
        w = [(frontier ** (arch[k][3] - top)) / (1 + arch[k][2]) ** 0.5 for k in keys]
        k = rnd.choices(keys, w)[0]; a = arch[k]; a[2] += 1
        e.load(a[0]); fr = a[1]; nact = rnd.randint(2, 6); spent = 0; i = 0; c = k
        while i < nact or (c == k and spent < idle_max):
            i += 1
            act = rnd.choice(acts); n = rnd.randint(3, 32)
            mash = any(b.endswith('*') for b in act)
            for j in range(n):
                e.step(_press(act, j) if mash else act)
            fr += n; total += n; spent += n
            r = ram(e); c = key(r)
            if keep and not keep(r): break
            if c not in arch or arch[c][1] > fr:
                v = sc(r)
                if v > best:
                    best = v
                    if log: log('explore: it %d frames %d score %s cell %s (%.0fs)' % (it, total, v, c, time.time() - t0))
                    if checkpoint: open(checkpoint, 'wb').write(e.save())
                arch[c] = [e.save(), fr, 0, v]
            if done and done(e, r):
                if log: log('explore: done at it %d frames %d cell %s' % (it, total, c))
                return e.save(), arch
    kb = max(arch, key=lambda k: (arch[k][3], -arch[k][1]))
    return arch[kb][0], arch


def boss_score(r):
    """Frontier score for boss fights: screen first, then damage dealt to the boss ($03ED)."""
    return progress(r) * 32 + ((0x1B - min(r[BOSSHP], 0x1B)) if r[BOSSBAR] else 0)


def enemy_hp(r):
    """Total HP (capped at 63) of the live, damageable objects in the enemy slots 8-$15."""
    return min(63, sum(r[O_HP + k] for k in range(8, 0x16) if r[O_TYPE + k] and 0 < r[O_HP + k] < 0x7F))


def explore_to(e, until='ckpt', budget=300000, jet=True, damage=False, seed=0, log=None, **kw):
    """Run the autoplayer from the current in-stage state until the game writes a new checkpoint
    (until='ckpt'), the boss bar appears (until='boss'), or either ('any').  Sets everything up the way
    that worked: all items except the current stage's own boss (a beaten boss's room beams Rockman
    out), Jet form with frozen fuel, godmode.  damage=True adds the enemy-HP term (mid-bosses).
    Returns (state_bytes, reached, (ckpt screen, chr, pal))."""
    st = e.peek(STAGE)
    give_all(e)
    if st < 8:
        set_progress(e, beaten=[s for s in range(8) if s != st], plates=[s for s in (4, 5, 6, 7) if s != st])
    if jet: e.poke(FORM, 1)
    godmode(e, fuel=jet)
    ck0 = (e.peek(CKPT_SCR), e.peek(CKPT_CHR), e.peek(CKPT_PAL))
    def ck(r): return (r[CKPT_SCR], r[CKPT_CHR], r[CKPT_PAL])
    def done(e_, r):
        hit_ck, hit_boss = ck(r) != ck0, r[BOSSBAR] != 0
        return {'ckpt': hit_ck, 'boss': hit_boss, 'any': hit_ck or hit_boss}[until]
    if damage:
        kw.setdefault('score', lambda r: r[OBJWIN] * 16 + (63 - enemy_hp(r)) // 4)
        kw.setdefault('cell', lambda r: enemy_hp(r) // 4)
    best, arch = explore(e, budget=budget, done=done, seed=seed, log=log, god=False, **kw)
    e.load(best); e.step(None)
    r = ram(e)
    return best, done(e, r), ck(r)
