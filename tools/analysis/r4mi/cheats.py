"""Rockman 4 Minus Infinity (4MI v1.01, MMC5 build) cheat sheet, save editor and warps for tools/analysis/emu.py.

    import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/r4mi')
    from emu import Emu
    import cheats as C
    e = Emu(C.ROM)                     # power-on
    C.unlock_all(e)                    # inject an unlocked save (SPECIAL MODE, EN text) and boot to the title menu
    C.to_extra_config(e)               # title -> SPECIAL MODE -> EXTRA CONFIGURATION (built-in level select)
    C.enter_stage(e, C.STAGE['RING'], cp=0, loadout='new')    # poke the fields, ENTER STAGE, run to control
    C.godmode(e); C.give_all(e)        # freeze HP/lives/i-frames (+FAIL-SAFE items), own everything
    print(C.status(e))
    # or simply: e.load('build/research/r4mi/states/ring_cp0.state')   (see docs/research/r4mi/cheats.md)

Regenerate the whole savestate set:  python3 -I tools/analysis/r4mi/cheats.py [outdir]

Everything below was found by RAM diffing and by reading the game's code; details and evidence are in
docs/research/r4mi/cheats.md.
  * RAM: $22 stage (16 = stage select, 17 = game-over/DATA SAVED screen), $1F checkpoint, $A0 weapon slot,
    $A1 lives, $A2 E-tanks, $A9 boss-clear bits, $AA fortress bits, $B0 HP, $B1-$BD weapon energy
    (bit7 = owned, bits0-4 = 0..28; energy of the current weapon = $B0+$A0), $3C player i-frames,
    $0330/$0348 player X pixel/page, $0378 player Y, $FC/$F9 scroll X pixel/page, $7839 equipment bits.
  * Save: WRAM $7C00 game block (+ working copy $7E00), $7D00 system block (+ working copy $7F00). Payload
    $00-$EF, checksum $F0-$FA = sum16 lo, sum16 hi, xor, xor of even offsets, xor of odd offsets, the same five
    inverted, xor of the first five. Bad game block -> "SAVE DATA BROKEN" handler (special menu hangs black).
  * Unlocks: system byte $78 (= $7F for every SPECIAL MODE item), $7E (= $07 for the three achievements).
"""
import os, sys

ROM = 'roms/r4mi_mmc5.nes'

# stage IDs ($22) == EXTRA CONFIGURATION "STAGE" values == vanilla RM4 order
STAGE = {'BRIGHT': 0, 'TOAD': 1, 'DRILL': 2, 'PHARAOH': 3, 'RING': 4, 'DUST': 5, 'DIVE': 6, 'SKULL': 7,
         'COSSACK1': 8, 'COSSACK2': 9, 'COSSACK3': 10, 'COSSACK4': 11,
         'WILY1': 12, 'WILY2': 13, 'WILY3': 14, 'WILY4': 15}
STAGE_NAME = {v: k for k, v in STAGE.items()}

RAM = dict(
    stage=0x22, checkpoint=0x1F, weapon=0xA0, lives=0xA1, etanks=0xA2, clear=0xA9, fortress=0xAA,
    hp=0xB0, iframes=0x3C, px=0x0330, ppage=0x0348, pxsub=0x0318, py=0x0378, pysub=0x0360, pvy=0x03F0,
    scroll_x=0xFC, scroll_page=0xF9, ss_col=0x10, ss_row=0x11, joy_held=0x14, joy_new=0x16,
    equip=0x7839, prog=0x7890, flag=0x7898, sval=0x7820, tml=0x78D3, crfl=0x78CA, exwp=0x78CB,
    # CONFIGURATION (live copies; packed into system block $79-$7B on save)
    cfg_language=0x78B0, cfg_main=0x78CD, cfg_damage=0x78CE, cfg_critical=0x78C9, cfg_itemdrop=0x78C8,
    cfg_failsafe=0x78CF, cfg_egen=0x78CC, cfg_vital=0x78D0, cfg_rockman=0x78D1, cfg_etank=0x78D2,
)
# weapon slots: energy byte = $B0 + $A0. Order = EXTRA CONFIG "WPN" bits (WPN1 bit0..7 = $B0..$B7, WPN2 bit0..5 = $B8..$BD)
WEAPON = {'BUSTER/HP': 0xB0, 'RUSH SEARCH': 0xB1, 'WISH STAR': 0xB2, 'RUSH CANNON': 0xB3, 'TOAD': 0xB4,
          'WIRE': 0xB5, 'BALLOON': 0xB6, 'DIVE': 0xB7, 'RING': 0xB8, 'DRILL': 0xB9, 'DUST': 0xBA,
          'PHARAOH': 0xBB, 'BRIGHT': 0xBC, 'SKULL': 0xBD}
# equipment bits in $7839 (the 3 starting items ENERGY CHARGER / BALANCER / EXCHANGER are not bits)
EQUIP = {'ENERGY SPLITTER': 0x01, 'SKULL AMULET': 0x02, 'SUPER STAR': 0x04, 'METALL HELMET': 0x08,
         'SHOCK GUARD': 0x10, 'TRAMPOLINE': 0x20, 'BEAT': 0x40, '?DAGGER': 0x80}
# EXTRA CONFIG "EXWP" values: the super-special weapon that replaces the buster
EXWP = {0: 'none', 1: 'QUINT', 2: 'ENKER', 3: 'R.ARMOR', 4: 'R.COPTER', 5: 'R.CANNON', 6: 'R.PWC',
        7: 'R.S.SHIP', 8: 'PUNK (SCREW CRUSHER)', 9: 'BALLADE (BALLADE CRACKER)', 10: 'EARTH (SPARK CHASER)',
        11: 'W.BUSTER (WILY BUSTER)'}
# EXTRA CONFIGURATION field -> RAM (pointer table at bank $4C:$93A1 (lo) / $93BF (hi), 15 rows x 2 columns)
FIELD = {'STAGE': 0x22, 'CP': 0x1F, 'CLEAR': 0xA9, 'CLEAR2': 0xAA, 'WPN1': 0x04A0, 'WPN2': 0x04A1,
         'LIVES': 0xA1, 'TANK': 0xA2, 'EQUIP': 0x7839, 'TML': 0x78D3, 'CRFL': 0x78CA, 'EXWP': 0x78CB,
         'PROG': 0x7890, 'FLAG': 0x7898, **{'SVAL%d' % i: 0x7820 + i for i in range(16)}}

# ----------------------------------------------------------------------------- save blocks
def cks(blk):
    """4MI save checksum over blk[0:0xF0] -> the 11 bytes stored at blk[0xF0:0xFB] (bank $40:$AAFD/$AC42)."""
    s = sum(blk[0:0xF0]); x = ev = od = 0
    for i in range(0xF0):
        x ^= blk[i]
        if i & 1: od ^= blk[i]
        else: ev ^= blk[i]
    c = [s & 0xFF, (s >> 8) & 0xFF, x, ev, od]
    return c + [v ^ 0xFF for v in c] + [c[0] ^ c[1] ^ c[2] ^ c[3] ^ c[4]]

def fix_block(e, base):
    blk = list(e.ram(base, 0x100))
    for i, v in enumerate(cks(blk)): e.poke(base + 0xF0 + i, v)

def _bases(which): return (0x7C00, 0x7E00) if which == 'game' else (0x7D00, 0x7F00)

def write_block(e, which, data):
    """which = 'game' ($7C00 + $7E00) or 'sys' ($7D00 + $7F00); data = up to 256 bytes (checksum recomputed)."""
    data = list(data) + [0] * (256 - len(data)); data[0xF0:0xFB] = cks(data)
    for base in _bases(which):
        for i, v in enumerate(data): e.poke(base + i, v)

def set_save_byte(e, which, off, v):
    for base in _bases(which):
        e.poke(base + off, v); fix_block(e, base)

def sys_block(english=True, unlock=0x7F, achievements=0x07):
    b = [0] * 256
    b[0x78] = unlock          # $01/$02 game cleared, $04 MECHANICAL, $08 LIMITED, $10 MY + "True", $20 AUDIO, $40 EXTRA
    b[0x79] = 0x01 if english else 0x00   # MAIN<<7 | E.GEN<<6 | DAMAGE<<4 | CRITICAL<<3 | ITEM DROP<<1 | LANGUAGE
    b[0x7A] = 0x1C            # FAIL-SAFE<<5 | VITAL (28)
    b[0x7B] = 0x40            # ROCKMAN (lives, 4)<<4 | ETANK (0)
    b[0x7E] = achievements    # bit0 SUPER HERO, bit1 HARD ROCK, bit2 PROOF OF OMEGA
    b[0x7F] = 0x01            # "system block initialised" marker (bank $40:$AB5D)
    return b

def new_game_block():
    b = [0] * 256; b[0x2F] = 0x02   # what NEW GAME writes on NORMAL (bit1: not eligible for HARD ROCK)
    return b

# ----------------------------------------------------------------------------- navigation
def at_title_menu(e):
    """the title-menu task is running (banks $39/$33 at $8000/$A000, task 0 parked with SP=$D1)"""
    return e.peek(0xF5) == 0x39 and e.peek(0xF6) == 0x33 and e.peek(0x82) == 0xD1

def to_title(e, maxf=3000):
    """Skip the intro with START until the title menu runs; then settle 60 frames."""
    for f in range(0, maxf, 10):
        if at_title_menu(e):
            e.run(60); return True
        e.run(7)
        if (f // 10) % 4 == 0: e.run(3, 'START')
        else: e.run(3)
    return False

def unlock_all(e, english=True):
    """Call right after Emu(ROM) (power-on). Injects an unlocked system save + a fresh NEW-GAME game save and boots
    to the title menu (NEW GAME / CONTINUE / SPECIAL MODE, cursor on CONTINUE). Returns True on success."""
    write_block(e, 'sys', sys_block(english))
    write_block(e, 'game', new_game_block())
    e.run(1)
    return to_title(e)

def new_game(e):
    """title menu -> NEW GAME (START+A wipes the game save) -> stage select"""
    e.tap('UP', 4); e.run(20); e.tap(['START', 'A'], 4); e.run(240)

def to_special_menu(e):
    """title menu (cursor on CONTINUE) -> SPECIAL MODE menu"""
    e.tap('DOWN', 4); e.run(20); e.tap('START', 4); e.run(200)

def to_extra_config(e):
    """title menu -> SPECIAL MODE -> EXTRA CONFIGURATION (7th item; cursor lands on EXIT)"""
    to_special_menu(e)
    for _ in range(6): e.tap('DOWN', 4); e.run(12)
    e.tap('START', 4); e.run(200)

def wait_control(e, maxf=2000, minf=240):
    """Run until the stage has started and the player stands still after teleporting in (Y unchanged for 20
    frames, HP > 0, stage < 16). Returns the frame count, or None (e.g. the Wily 3 space cutscene)."""
    last, same = -1, 0
    for f in range(maxf):
        e.step()
        y = e.peek(0x378)
        same = same + 1 if y == last else 0; last = y
        if f >= minf and same >= 20 and e.peek(0x22) < 16 and e.peek(0xB0) & 0x1F:
            return f
    return None

LOADOUTS = {
    # name: (CLEAR $A9, CLEAR2 $AA, WPN1, WPN2, LIVES, TANK, EQUIP, TML, C.RFL)
    'new':      (0x00, 0x00, 0x03, 0x00, 9, 0, 0x00, 0, 0),   # buster + Rush Search, like a fresh file
    'fortress': (0xFF, 0x00, 0xFF, 0x3F, 9, 4, 0x00, 0, 0),   # 8 bosses beaten, all weapons/Rush/Wire/Balloon
    'full':     (0xFF, 0x00, 0xFF, 0x3F, 9, 9, 0xFF, 1, 1),   # + every equipment bit, TML + C.RFL cheats on
}

def _apply(e, loadout, extra):
    clr, fort, w1, w2, lives, tanks, equip, tml, crfl = LOADOUTS[loadout]
    vals = {0xA9: clr, 0xAA: fort, 0x04A0: w1, 0x04A1: w2, 0xA1: lives, 0xA2: tanks, 0x7839: equip,
            0x78D3: tml, 0x78CA: crfl}
    vals.update(extra)
    for a, v in vals.items(): e.poke(a, v)

def enter_stage(e, stage, cp=0, loadout='new', fortress=None, exwp=0, wait=True, **fields):
    """From the EXTRA CONFIGURATION screen (cursor on EXIT): poke the fields and pick ENTER STAGE.
    The fields are live RAM (FIELD), so no bit-editing in the UI is needed. CLEAR2 defaults to "every earlier
    fortress stage cleared". Extra fields by name, e.g. PROG=0x10, FLAG=0x02. Returns frames to control."""
    if fortress is None: fortress = ((1 << (stage - 8)) - 1) if 8 <= stage < 16 else LOADOUTS[loadout][1]
    extra = {0x22: stage, 0x1F: cp, 0xAA: fortress, 0x78CB: exwp}
    extra.update({FIELD[k]: v for k, v in fields.items()})
    _apply(e, loadout, extra)
    e.tap('UP', 4); e.run(12); e.tap('UP', 4); e.run(12)   # EXIT -> BOSS SELECT -> ENTER STAGE
    e.tap('START', 4)
    return wait_control(e) if wait else None

def boss_select(e, loadout='fortress', **fields):
    """From EXTRA CONFIGURATION: apply a loadout and pick BOSS SELECT (stage-select screen, counters kept)."""
    _apply(e, loadout, {FIELD[k]: v for k, v in fields.items()})
    e.tap('UP', 4); e.run(12); e.tap('START', 4); e.run(240)

# ----------------------------------------------------------------------------- in-game cheats
def godmode(e, hp=28, lives=9, failsafe=True):
    """Freeze HP, lives and the player i-frame timer $3C (enemies cannot hurt you). HP alone does not stop pits
    and spikes, so by default also give SHOCK GUARD (spikes) + TRAMPOLINE (pits) + BEAT (pit rescue)."""
    e.freeze(0xB0, 0x80 | hp); e.freeze(0xA1, lives); e.freeze(0x3C, 2)
    if failsafe: e.poke(0x7839, e.peek(0x7839) | 0x70)

def give_all(e, etanks=9, equip=0xFF):
    """Own and fill every weapon/Rush slot ($B1-$BD = $9C), all equipment bits, E-tanks."""
    for a in range(0xB0, 0xBE): e.poke(a, 0x9C)
    e.poke(0x7839, equip); e.poke(0xA2, etanks)

def warp(e, stage, cp=0, maxf=600):
    """In-stage warp without menus: set $22/$1F, then drop the player into a pit (Y=$F0 every frame) so the respawn
    loads that stage and checkpoint with the current loadout. TRAMPOLINE/BEAT ($60) and a frozen lives/HP value
    are suspended during the fall and restored after. Returns frames to control (None on failure)."""
    saved = {a: e._frozen.pop(a) for a in (0xA1, 0xB0, 0x378) if a in e._frozen}
    eq = e.peek(0x7839); e.poke(0x7839, eq & ~0x60)
    if e.peek(0xA1) < 2: e.poke(0xA1, 2)
    e.poke(0x22, stage); e.poke(0x1F, cp)
    lives = e.peek(0xA1); died = False
    for _ in range(maxf):
        e.poke(0x378, 0xF0); e.step()
        if e.peek(0xA1) != lives: died = True; break
    f = wait_control(e) if died else None
    e.poke(0x7839, e.peek(0x7839) | (eq & 0x60)); e._frozen.update(saved)
    return f

def infinite_energy(e):
    for a in range(0xB1, 0xBE): e.freeze(a, 0x9C)

def set_weapon(e, name):
    """select a weapon directly (it must be owned); takes effect like the menu would, sprite palette may lag."""
    e.poke(0xA0, WEAPON[name] - 0xB0)

def status(e):
    p = e.peek
    return dict(stage=STAGE_NAME.get(p(0x22), p(0x22)), cp=p(0x1F), hp=p(0xB0) & 0x1F, lives=p(0xA1),
                etanks=p(0xA2), weapon=p(0xA0), clear='%02x' % p(0xA9), fort='%02x' % p(0xAA),
                x=p(0x348) * 256 + p(0x330), y=p(0x378), iframes=p(0x3C), equip='%02x' % p(0x7839))

# ----------------------------------------------------------------------------- regenerate the state set
def make_states(outdir='build/research/r4mi/states'):
    """Power-on -> unlocked title -> menus -> every stage x checkpoint 0-2. ~1 minute."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from emu import Emu
    os.makedirs(outdir, exist_ok=True); P = lambda n: os.path.join(outdir, n + '.state')
    e = Emu(ROM)
    assert unlock_all(e), 'title menu not reached'
    e.save(P('title'))
    new_game(e); e.save(P('stage_select_new'))
    e.load(P('title')); e.run(1); to_special_menu(e); e.save(P('special_menu'))
    e.load(P('title')); e.run(1); to_extra_config(e); e.save(P('extra_config'))
    boss_select(e, 'fortress'); e.save(P('stage_select_all'))
    out = {}
    for st in range(16):
        for cp in range(3):
            e.load(P('extra_config')); e.run(2)
            f = enter_stage(e, st, cp, 'new' if st < 8 else 'fortress')
            name = '%s_cp%d' % (STAGE_NAME[st].lower(), cp)
            e.save(P(name)); out[name] = dict(status(e), frames_to_control=f)
    return out

if __name__ == '__main__':
    for k, v in make_states(*sys.argv[1:]).items(): print(k, v)
