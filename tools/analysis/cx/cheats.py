"""Rockman CX / Mega Man CX cheats, warps, checkpoint warps and autoplayers (docs: docs/research/cx/cheats.md).

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
    from emu import Emu
    import cheats as cx
    e = Emu('roms/cx_en.nes')
    e.load(cx.state('fire_mario_boss'))   # 62 ready states in build/research/cx/states/ (see the doc, section 1)
    cx.godmode(e)                         # freeze HP / lives / i-frames (pits still kill)
    cx.give_all_weapons(e)                # $9A = $FF, all energies full, 4 E-tanks
    print(cx.info(e))
    cx.warp(e, 3)                         # fresh stage start from a crafted save (0-15; 9 via the fortress map)
    cx.warp_cp(e, 10, 2)                  # checkpoint warp: die with the room byte held at the checkpoint room
    cx.autorun(e, 4000, until=cx.boss_active)   # dumb autoplayer;  cx.explore(...) = Go-Explore autoplayer
    cx.finish_boss(e)                     # boss to 1 HP, shoot until it dies (poking 0 does not kill)

Only one Emu per process (stable-retro limit): reuse it with e.load().
After e.load(), run one frame before e.shot() (the frame buffer is not in the state).
All warps start from build/research/cx/states/title.state.
"""
import os, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STATES = os.path.join(REPO, 'build', 'research', 'cx', 'states')

# ---- RAM map (verified addresses are documented in docs/research/cx/cheats.md) -------------
HP = 0x06C0        # player HP, 0..max (start 24 = $18, max 40 = $28 with 4 heart tanks)
BOSSHP = 0x06C1    # boss HP (vanilla RM2 slot; full = $1C)
MAXHP = 0x0099     # max HP; reloaded from the save slot ($7420+slot) at every stage start
BOSSES = 0x009A    # bosses defeated = weapons owned, bit n = stage n
FLAGS = 0x009B     # bit7 = playing Quick Man, bits 4-6 = Dr. Light fortress stages cleared (0-6)
IFRAMES = 0x004B   # invincibility timer (set to $6E on hit, +$34 per Ubercharge use, counts down)
STAGE = 0x002A     # stage id (also the stage-select cursor while on that screen, see SEL)
ROOM = 0x0440      # player X screen (room counter along the level path; also counts vertical screens)
X = 0x0460         # player X pixel within the screen
Y = 0x04A0         # player Y pixel
WEAPON = 0x00A9    # current weapon / item id (0 buster, 1-8 boss weapons, 9-B items, C = E-tank cursor)
ENERGY = 0x009B    # energy of weapon id n (1..11) is at $9B+n ($9C..$A6), max $28
FLOOR, SUBTANK, UBER = 0x00A4, 0x00A5, 0x00A6   # item energies; UBER starts at 0 and is saved
ETANKS = 0x00A7
LIVES = 0x00A8
HEARTS = 0x7FF8    # WRAM, $7FF8+stage = 1 when that stage's heart tank is taken (tanks in stages 0,3,5,7)
SLOT = 0x7FF0      # WRAM, current save slot (0-2)

STAGES = {0: 'cheat_man', 1: 'air_man', 2: 'whispy_woods', 3: 'fire_mario', 4: 'yoshino_man',
          5: 'mega_man', 6: 'kamen_rider', 7: 'bomberman',
          8: 'light1', 9: 'light2', 10: 'light3', 11: 'light4', 12: 'light5', 13: 'light6', 14: 'ending',
          15: 'opening'}
WEAPONS = {0: 'P (buster)', 1: 'CHEAT SABER', 2: 'DEAD RINGER', 3: 'RINGO SHIELD', 4: 'FIRE BALL',
           5: 'PRINT CUTTER', 6: 'MEGA BUSTER', 7: 'RIDER KICK', 8: 'POWER BOMB',
           9: '1.FLOOR', 10: '2.SUBTANK', 11: '3.UBERCHARGE'}
# stage-select cursor value ($2A while on the select screen) -> stage id; 0 = centre (Dr. Light fortress)
SEL = {1: 2, 2: 3, 3: 6, 4: 7, 5: 1, 6: 5, 7: 4, 8: 0}
SEL_OF = {v: k for k, v in SEL.items()}


def state(name):
    """Path of a shared savestate in build/research/cx/states/."""
    p = name if name.endswith('.state') else name + '.state'
    return p if os.path.isabs(p) else os.path.join(STATES, p)


def ram(e):
    m = e.d.memory.blocks
    return m[0] + m[1024]


def info(e):
    """One-line summary of the interesting RAM."""
    g = e.peek
    return ('stage %02X(%s) room %02X x %02X y %02X hp %d/%d lives %d etanks %d wpn %d bosses %02X flags %02X '
            'uber %d iframes %d' % (g(STAGE), STAGES.get(g(STAGE), '?'), g(ROOM), g(X), g(Y), g(HP), g(MAXHP),
                                    g(LIVES), g(ETANKS), g(WEAPON), g(BOSSES), g(FLAGS), g(UBER), g(IFRAMES)))


def godmode(e, hp=True, lives=True, iframes=True):
    """Freeze HP at max, lives at 9 and the i-frame timer (player passes through enemies, no knockback).
    Pits still kill you (you respawn at the checkpoint).  The player sprite blinks while i-frames run."""
    if hp: e.freeze(HP, max(e.peek(MAXHP), 0x18))
    if lives: e.freeze(LIVES, 9)
    if iframes: e.freeze(IFRAMES, 0x40)


def nogod(e):
    e.unfreeze()


def refill(e):
    """Full HP and all 11 weapon/item energies (one-shot poke)."""
    e.poke(HP, max(e.peek(MAXHP), 0x18))
    for n in range(1, 12): e.poke(ENERGY + n, 0x28)


def give_all_weapons(e, etanks=4):
    """All 8 boss weapons (sets the bosses-defeated bits, which is what the menu checks), full energy,
    a full Ubercharge and some E-tanks.  Note: on the stage-select screen this also blanks every portrait."""
    e.poke(BOSSES, 0xFF); refill(e); e.poke(ETANKS, etanks)


# ---- save slots (WRAM, battery backed) ----------------------------------------------------------
# slot s field f lives at $7420 + 3*f + s.  Checksum = 8-bit ADC chain (CLC first) in this order:
SAVE = 0x7420
SAVE_FIELDS = ['maxhp', 'bosses', 'flags', 'uber', 'etanks', 'lives', 'sum', 'heart0', 'heart3', 'heart5',
               'heart7', 'v98', 'r44', 'r47']          # sources: $99 $9A $9B $A6 $A7 $A8 - $7FF8 $7FFB $7FFD $7FFF $98
_SUM_ORDER = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13]


def _checksum(vals):
    a, c = 0, 0
    for i in _SUM_ORDER:
        t = a + vals[i] + c; a, c = t & 0xFF, t >> 8
    return a


def read_save(e, slot=0):
    v = [e.peek(SAVE + 3 * i + slot) for i in range(len(SAVE_FIELDS))]
    d = dict(zip(SAVE_FIELDS, v)); d['valid'] = _checksum(v) == v[6]; return d


def write_save(e, slot=0, maxhp=0x18, bosses=0, flags=0, uber=0, etanks=0, lives=8, hearts=(0, 0, 0, 0), v98=0):
    """Write a valid save record (hearts = taken flags for stages 0,3,5,7)."""
    v = [maxhp, bosses, flags, uber, etanks, lives, 0] + [1 if h else 0 for h in hearts] + [v98, 0, 0]
    v[6] = _checksum(v)
    for i, x in enumerate(v): e.poke(SAVE + 3 * i + slot, x)


# ---- warps --------------------------------------------------------------------------------------
def _xpos(e): return e.peek(ROOM) << 8 | e.peek(X)


def playable(e, n=8):
    """True if RIGHT/LEFT input moves the player (compared with no input).  Restores the state."""
    s = e.save()
    e.run(n); x0 = _xpos(e); e.load(s)
    e.run(n, ['RIGHT']); x1 = _xpos(e); e.load(s)
    e.run(n, ['LEFT']); x2 = _xpos(e); e.load(s)
    return abs(x1 - x0) >= 3 or abs(x2 - x0) >= 3


def wait_playable(e, limit=6000, step=20, press_a=False):
    """Run until the player can move (after READY / cutscenes).  press_a taps A every other check
    (advances dialogue faster, but A may also skip text).  Returns frames waited or None."""
    for t in range(0, limit, step):
        e.run(step, ['A'] if press_a and (t // step) % 2 else None)
        if playable(e): return t + step
    return None


def to_stage_select(e, slot=0, **save):
    """From the title screen state: write a save record into `slot`, LOAD GAME it, wait for stage select.
    save kwargs go to write_save (maxhp, bosses, flags, uber, etanks, lives, hearts, v98)."""
    e.load(state('title'))
    write_save(e, slot, **save)
    e.run(2); e.tap('DOWN'); e.run(20); e.tap('START'); e.run(40)
    for _ in range(slot): e.tap('DOWN'); e.run(12)
    e.tap('START'); e.run(320)
    return e


def new_game(e, slot=0, wait=True):
    """Title -> NEW GAME -> DATA <slot+1> -> intro -> opening stage (stage $0F).  Returns frames waited."""
    e.load(state('title')); e.run(2)
    e.tap('START'); e.run(1200)
    for _ in range(slot): e.tap('DOWN'); e.run(12)
    e.tap('START'); e.run(1400)
    return wait_playable(e, step=5) if wait else None


def fortress_route(e, quick_man=True):
    """On the Dr. Light fortress map shown after Light stage 1 (progress 1), walk the fake Rockman:
    quick_man=True climbs the ladder and walks into Quick Man -> stage $09 (Light 2);
    False walks along the floor into Guts Man -> stage $0A (Light 3, skipping $09)."""
    if quick_man:
        for _ in range(400):
            if e.peek(X) >= 0x78: break
            e.step(['RIGHT'])
        e.run(120, ['UP']); e.run(60, ['UP', 'RIGHT'])
    e.run(600, ['RIGHT'])


def warp(e, stage, slot=0, wait=True, **save):
    """Start a stage fresh from the stage select, via a crafted save.
    stage 0-7 = robot masters, 8-13 = Dr. Light fortress 1-6 (sets bosses=$FF and the fortress progress),
    14 = final stage ($0E), 15 = opening stage (NEW GAME).  Stage 9 is reached through the fortress map
    (progress 1, ladder -> Quick Man).  Returns frames waited until playable (None if it never got control)."""
    if stage == 15:
        return new_game(e, slot, wait)
    if stage >= 8:
        save.setdefault('bosses', 0xFF)
        save['flags'] = (save.get('flags', 0) & 0x8F) | ((stage - 8) << 4)
        sel = 0
    else:
        sel = SEL_OF[stage]
    to_stage_select(e, slot, **save)
    e.poke(STAGE, sel); e.run(10); e.tap('START')
    if stage == 9:
        wait_playable(e)              # the map walker becomes controllable
        fortress_route(e, quick_man=True)
    return wait_playable(e) if wait else None


# Restart rooms per stage, in the order you reach them (cp 0 = stage start).  Each 16 KB stage bank holds
# one robot-master stage plus one fortress/opening stage, and both share the bank's 6-entry restart
# table at $BB06 (rooms) / $BB30 (segment $38) / $BB37 / $BB3D (scroll limits $14/$15) [code $C4CD].
# On death $C190 sets checkpoint index $B0 = (number of entries <= current room) - 1; stage 5 skips the -1
# because Mega Man's stage runs right-to-left (start room $0E, then $08, then $01).
CP_ROOMS = {0: [0x00, 0x08, 0x16, 0x18], 1: [0x00, 0x0A, 0x14, 0x17, 0x20], 2: [0x00, 0x0D, 0x16],
            3: [0x00, 0x0C, 0x14], 4: [0x00, 0x07, 0x16], 5: [0x0E, 0x08, 0x01], 6: [0x00, 0x0A, 0x13],
            7: [0x00, 0x08, 0x11], 8: [0x19, 0x21], 9: [0x2B], 10: [0x18, 0x21, 0x28], 11: [0x17, 0x21, 0x2A],
            12: [0x18, 0x1D, 0x29], 13: [0x15, 0x16, 0x20], 14: [0x18, 0x1A, 0x28], 15: [0x17, 0x1D]}


def cp_table(rom_bytes, stage):
    """The raw 6-entry restart-room table of a stage's bank (rom_bytes = ROM without the iNES header)."""
    o = (2 * (stage & 7) + 1) * 0x2000 + 0x1B06
    return list(rom_bytes[o:o + 6])


def kill(e, room=None, limit=400):
    """Kill the player now (drop him below the screen).  If room is given, the room byte is held there
    until the death registers, which picks the checkpoint the game restarts from.  Refunds the life."""
    lives = e.peek(LIVES)
    e.poke(Y, 0xF0)
    if room is not None: e.freeze(ROOM, room)
    for _ in range(limit):
        e.step(None)
        if e.peek(LIVES) != lives: break
    if room is not None: e.unfreeze(ROOM)
    e.poke(LIVES, lives)


def warp_cp(e, stage, cp, wait=True, **save):
    """Start `stage` at checkpoint `cp` (index into CP_ROOMS[stage]): warp to the stage start, then die
    with the room byte held at the checkpoint room so the restart code picks it."""
    t = warp(e, stage, **save)
    if cp == 0: return t
    rooms = CP_ROOMS[stage]
    if stage == 5:
        tab = [0x01, 0x08, 0x0E]           # B0 index k needs (entries <= room) == k
        k = 2 - cp; room = tab[k] - 1
    else:
        room = rooms[cp]
    kill(e, room)
    if not wait: return None
    t = wait_playable(e, limit=600)
    if t is None:                          # beam-in hung (scroll-locked boss rooms): drop in from y=$80
        e.poke(Y, 0x80); t = wait_playable(e, limit=600)
    return t


# ---- autoplay ----------------------------------------------------------------------------------
# Held-button macros.  'A*' / 'B*' = mash (pressed 3 frames, released 3): needed for wall kicks and rapid fire.

def boss_active(e):
    """True when a scroll-locked room with a filled boss bar is running (boss HP in $06C1, $14 == $15)."""
    return e.peek(0x14) == e.peek(0x15) and 0 < e.peek(BOSSHP) <= 0x40


def finish_boss(e, limit=4000):
    """Set the boss/mid-boss in object slot 1 to 1 HP and fire the buster at it (walking back and forth,
    jumping) until it dies.  Poking $06C1 = 0 does NOT kill: death is checked when a shot hits.
    Returns frames used, or None.  Leaves godmode on."""
    godmode(e)
    e.poke(BOSSHP, 1); st = e.peek(STAGE)
    for i in range(limit):
        if e.peek(BOSSHP) == 0 or e.peek(STAGE) != st: return i
        e.step((['RIGHT'] if (i // 40) % 2 else ['LEFT']) + (['B'] if i % 6 < 3 else []) +
               (['A'] if (i // 20) % 3 == 0 else []))
    return None


def autorun(e, frames=3000, direction='RIGHT', shoot=True, until=None, god=True):
    """Dumb autoplayer: hold `direction`, mash B, jump (full height) when X stops changing, try UP (ladders)
    and the other direction when stuck for long.  until(e) -> True stops early.  Returns frames used.
    Gets through many CX rooms with godmode; use explore() for mazes and vertical shafts."""
    if god: godmode(e)
    back = 'LEFT' if direction == 'RIGHT' else 'RIGHT'
    last, stuck, jump = None, 0, 0
    for t in range(frames):
        x = _xpos(e)
        stuck = stuck + 1 if x == last else 0
        last = x
        b = [direction]
        if jump > 0:
            b.append('A'); jump -= 1
        elif stuck > 6:
            jump = 22
        if stuck > 120: b = ['UP']
        if stuck > 200: b = [back, 'A'] if (t // 30) % 2 else [direction, 'A']
        if stuck > 320: stuck = 0
        if shoot and t % 8 < 4: b.append('B')
        e.step(b)
        if until and until(e): return t + 1
    return frames

ACTS = [['RIGHT'], ['RIGHT', 'A'], ['LEFT'], ['LEFT', 'A'], ['UP'], ['DOWN'], ['A'], [],
        ['RIGHT', 'DOWN', 'A'], ['LEFT', 'DOWN', 'A'], ['UP', 'RIGHT'], ['UP', 'LEFT'],
        ['RIGHT', 'B'], ['LEFT', 'B'], ['B'], ['RIGHT', 'A*'], ['LEFT', 'A*'], ['RIGHT', 'B*'], ['LEFT', 'B*']]


def _press(act, j):
    """Buttons for frame j of a held macro (expands the mash markers)."""
    out = []
    for b in act:
        if b.endswith('*'):
            if (j // 3) % 2 == 0: out.append(b[:-1])
        else:
            out.append(b)
    return out


def _cell(r, xshift=4, yshift=5):
    return (r[STAGE], r[ROOM], r[X] >> xshift, r[Y] >> yshift)


def explore(e, budget=300000, seed=0, acts=ACTS, done=None, keep=None, log=print, xshift=4, yshift=5,
            frontier=4.0, god=True, cell=None, checkpoint=None, idle_max=1500, score=None):
    """Go-Explore autoplayer.  Archive of cells (stage, room, x>>xshift, y>>yshift[, extra]) -> savestate;
    repeatedly restore a cell (biased to the furthest room reached) and play random held-button macros.
    - done(e, r) -> True stops the search (e.g. stage changed, boss dead).  r = 2 KB RAM bytes.
    - keep(r) -> False ends the rollout without archiving (e.g. while dying).
    - cell(r) -> extra hashable added to the cell key (e.g. boss HP bucket).
    - A rollout that ends in its start cell keeps going (up to idle_max frames), so cutscenes and
      dialogue boxes, which freeze the player, get played through.
    - checkpoint: path; the furthest state is written there whenever a new best score is reached.
    - score(r) -> number used for the frontier bias (default: the room number).  For boss fights use
      boss_score (room, then damage dealt).
    Returns (best_state_bytes, archive)."""
    rnd = random.Random(seed)
    if god: godmode(e)
    e.step(None)
    key = (lambda r: _cell(r, xshift, yshift) + ((cell(r),) if cell else ()))
    sc = score or (lambda r: r[ROOM])
    r = ram(e); c0 = key(r)
    arch = {c0: [e.save(), 0, 0, sc(r)]}        # cell -> [state, frames, visits, score]
    total, it, best, t0 = 0, 0, sc(r), time.time()
    while total < budget:
        it += 1
        keys = list(arch); top = max(arch[k][3] for k in keys)
        w = [(frontier ** (arch[k][3] - top)) / (1 + arch[k][2]) ** 0.5 for k in keys]
        k = rnd.choices(keys, w)[0]; a = arch[k]; a[2] += 1
        e.load(a[0]); fr = a[1]; nact = rnd.randint(2, 6); spent = 0; i = 0
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
    """Frontier score for boss fights: room first, then damage dealt to the boss ($06C1)."""
    return r[ROOM] * 64 + (0x1C - min(r[BOSSHP], 0x1C))
