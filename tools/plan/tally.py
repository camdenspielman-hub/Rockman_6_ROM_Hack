#!/usr/bin/env python3
"""critic-scope scratch: production inventory and session estimate for the R6GP design round 1.

Sessions = focused AI-assisted sessions (one well-scoped task each), CODE + DATA + TEST only.
Art, music and text are estimated separately at the bottom from art_audio.md / story.md ledgers.
Tier = the tier the design docs give today (M/S/C). 'P' column = proposed v1.0 tier (critic-scope).
"""
from collections import defaultdict

# (area, item, docs-tier, sessions, proposed-tier)
I = []
def add(area, item, tier, s, prop=None):
    I.append((area, item, tier, s, prop or tier))

# ---------------- TECH FOUNDATIONS (tech.md §16 + hidden items) ----------------
T = 'tech'
add(T, 'M0 scaffold/build/BPS/registry/allocator/test runner/golden record', 'M', 4)
add(T, 'M0.4 reassemblable fixed banks + sound driver', 'M', 3)
add(T, 'M0.5-0.8 .lvl/MML round trips, censuses, stagetab', 'M', 4)
add(T, 'MMC5 go/no-go spike on Mesen (+cart if any) BEFORE M1', 'M', 1.5)
add(T, 'M1.1-1.3 MMC5 insertion, helpers, mirroring, IRQ literal port+calibration', 'M', 8)
add(T, 'M1.4 shadow6 MMC5 + golden equivalence', 'M', 2.5)
add(T, 'M1.5-1.7 PRG-RAM pages/probe/save skeleton/mailbox, lag baseline', 'M', 2.5)
add(T, 'M2.1 stage-attribute table, 45+11 readers, static scan', 'M', 4)
add(T, 'M2.2 WRAM layouts, poke lists, map_set/log', 'M', 3)
add(T, 'M2.3 families/sub-id dispatcher, object lists v2, CHR-conflict hook', 'M', 3)
add(T, 'M2.4 generic raster list, presets, IRQ logic out of IRQ', 'M', 4)
add(T, 'M2.5 text engine v1 (ExRAM window, canvas, VWF, JP, borrow/restore, choices, compiler)', 'M', 7)
add(T, 'M2.6 sound: track table v2, bank bytes, multiplier, mml compile', 'M', 3)
add(T, 'M2.7 level pipeline build + checks + canvas table', 'M', 3)
add(T, 'M2.8 DEV build: EXTRA CONFIG engine, warps, ring buffer', 'M', 1.5)
add(T, 'M2.9-2.10 CHR stream queue, lag steps, latch source, frozen tick, LFSR, death audit', 'M', 3)
add(T, 'HIDDEN: CHR set table v2 + stage-local ids (art_audio §2.1; not scheduled in tech §16)', 'M', 2)
add(T, 'HIDDEN: art pipeline chr.py/sprites.py/sprslice/palettes.py (not in tech §16)', 'M', 3)
add(T, 'HIDDEN: artcheck.py (overlap, palettes, free-id map, flicker, streams, census)', 'M', 2.5)
add(T, 'HIDDEN: bgboss.py (poses, deltas, hit boxes, streams)', 'M', 2.5)
add(T, 'M3.3 T3 switch->target', 'M', 2.5)
add(T, 'M3.4 T6 variant blocks + X-BONK', 'M', 2.5)
add(T, 'M3.5 T1-lite wave director + RL_BANDS rides', 'M', 3)
add(T, 'M3.6 player ext: GP player states, X-WRAP, exit type 7, pad history', 'M', 2.5)
add(T, 'M3.8 lag steps 3-4 (OAM builder)', 'S', 2, 'S')
add(T, 'T5 pendulum (vines)', 'M', 2)
add(T, 'T7 input mirror (Shadow Rock, Gemini Rock, Shadow Flame Man)', 'M', 2)
add(T, 'T8 multi-part boss library', 'S', 2)
add(T, 'X-METER/X-LABEL/F-CLOCK/score/counters (HUD widgets) as ONE module', 'M', 2)
add(T, 'X-EXWP set-piece weapon', 'M', 1.5)
add(T, 'X-FLOOR new floor types (ski, hot spring, nightingale)', 'S', 1.5, 'C')
add(T, 'X-UPEXIT exit type 7 (Ice Climber climb)', 'S', 1.5, 'C')
add(T, 'section switch (slot $89) + sections > 32 screens', 'S', 1.5)
add(T, 'pattern-table split for menus', 'S', 1)
add(T, 'F-PIECES (BG body that comes apart)', 'M', 2.5)
add(T, 'F-SIZES (size frames streamed)', 'M', 2)
add(T, 'F-GRID (WRAM cell grid for exhibitions)', 'S', 2.5, 'C')
add(T, 'F-ERA (POCKET/NES/SUPER eras, flip-screen, letterbox, firmware flags)', 'S', 3, 'C')
add(T, 'ExGrafix spike + per-column ExRAM streaming', 'C', 3, 'C')
add(T, '16-band MODE-7 floor (W3)', 'M', 3, 'S')
add(T, 'commentator event bus/queue/cooldown (story §6.1)', 'M', 2.5)
add(T, 'boss panel extension (fight-id records, 10th field, re-type)', 'M', 1.5)
add(T, 'driver D3/D9/D10/D11 + sndtest', 'M', 2.5)
add(T, 'fms2mml.py', 'S', 2, 'C')
add(T, 'MMC5 pulses 2nd driver instance (D5) + D7 charge', 'C', 4, 'C')
add(T, 'lighting/darkness service (Knight RADIANT, blackout, black zone, Bright rooms)', 'M', 1.5)

# ---------------- SYSTEMS (systems.md) ----------------
Y = 'systems'
add(Y, 'SELECT modifier + last-weapon toggle', 'M', 1.5)
add(Y, 'controller-2 pseudo L/R', 'S', 0.5)
add(Y, 'quick form swap + 2 KB CHR stream + debut cutscene', 'M', 2.5)
add(Y, 'forms fire weapon TAPS (dispatch, may-shoot table)', 'M', 2)
add(Y, 'adaptors by win count', 'M', 1)
add(Y, 'Power parry', 'S', 2, 'C')
add(Y, 'Super Adaptor (fist with homing return + jet hop)', 'M', 4)
add(Y, '8 weapon ALTS (Wall Spear, Updraft, Ice Block, Flare, Petal Shot, Hold, Feather Fan, Time Stop)', 'M', 10, 'S')
add(Y, '8 form SYNERGIES (Pogo, Tailwind, Snow Bomb, Burning Knuckle, Petal Storm, Morning Star, Dive Throw, Time Fist)', 'M', 9, 'S')
add(Y, 'tap tweaks (pierce, PLANT.B 2 hits, C.FLASH lights rooms, half-charge 2)', 'M', 1.5)
add(Y, 'MAGNET BEAM', 'M', 2.5)
add(Y, 'GP_BOSSHIT tables + generator + i-frame classes', 'M', 2.5)
add(Y, 'frozen tick + type->damage-routine table (256) + tests', 'M', 2.5)
add(Y, 'normal-enemy rules, lingering re-hit timer, punch-only list', 'M', 1)
add(Y, 'WEAK! pop + stagger + SFX + flash', 'M', 1.5)
add(Y, 'special cases SC1-SC9', 'M', 5)
add(Y, 'shot re-class + LASTHIT/LATCHSRC + death convergence hooks', 'M', 2.5)
add(Y, 'scorecard counters + formulas + pars + tokens', 'M', 3)
add(Y, 'bolts/economy/shop stock & prices', 'M', 2)
add(Y, 'chip framework (bits, slots, help pages)', 'M', 2)
add(Y, 'chip effects: 7 shop + Balancer', 'M', 3)
add(Y, 'chip effects: 8 venue behaviour prizes', 'M', 3)
add(Y, 'PARTs + featured enemies + garage + 4 garage chips', 'S', 3, 'C')
add(Y, 'Mr. Y booth + Y-TURBO + asterisks + Break Man walks', 'S', 1.5, 'C')
add(Y, 'plates->slots, Beat pit rescue', 'M', 2)
add(Y, 'Break Man tag partner (body, call/swap, moveset, gates)', 'S', 5)
add(Y, 'pickup routing, drops, refill, W-tank, E-tank x2, overflow', 'M', 2)
add(Y, 'difficulty presets + overrides + RULESET reads', 'M', 2)
add(Y, 'HARD framework (poke lists applied, IFHARD)', 'M', 1.5)
add(Y, 'HARD content: per-stage poke lists + AI branches (22 stages)', 'M', 8, 'S')
add(Y, '1993 rules preset (generated rows, vanilla forms, shop off)', 'S', 3, 'C')
add(Y, 'criticals + KAISHIN fallback', 'C', 1, 'C')

# ---------------- META (meta.md) ----------------
X = 'meta'
add(X, 'save module A/B ping-pong, trailer, migration, BROKEN paths, autosaves', 'M', 3.5)
add(X, 'title + menu + license + hidden PASS WORD', 'M', 2)
add(X, 'attract crawl (6 panels on vanilla bytecode)', 'S', 1.5, 'C')
add(X, 'file select cards + NEW/ERASE guards + difficulty pick', 'M', 2.5)
add(X, 'bracket screen: node table, states, centre, semifinal trigger, event queue', 'M', 4)
add(X, 'bracket Exhibition layer + badges', 'S', 1.5, 'C')
add(X, 'Riot intro animation', 'S', 1, 'C')
add(X, 'results screen (judges desk, slide-in rows, stamp, prize)', 'M', 2.5)
add(X, 'debrief engine + predicate tables (22 stages)', 'M', 2.5)
add(X, 'pit stop UI (shop, chips grid, config page)', 'M', 2.5)
add(X, 'pit stop garage + booth rows', 'S', 1, 'C')
add(X, 'game over / RETIRE / unplug', 'M', 1.5)
add(X, 'medals + HoF points + unlock bits', 'M', 1)
add(X, 'championship rating + Break Man debrief', 'M', 2.5)
add(X, 'fortress maps (HoF, Castle) + BACK TO BRACKET', 'M', 2)
add(X, 'GP Rush fight loader (needed by W2 even without GP Rush)', 'S', 2.5, 'M')
add(X, 'GP Rush runner, lobby, courses, MY GP', 'S', 5, 'C')
add(X, 'Time Attack (+ splits, DEV times, presets per stage)', 'S', 3)
add(X, 'KNOCKOUT', 'C', 3, 'W')
add(X, 'Exhibition Rules + TURBO rule', 'C', 3.5, 'W')
add(X, 'RECORDS pages 1-3', 'M', 1.5)
add(X, 'RECORDS 4-7 + achievements', 'S', 2.5, 'C')
add(X, 'Museum + VAULT + plaque gallery', 'C', 3.5, 'W')
add(X, 'EXTRA CONFIG UI + mailbox + scratch file', 'M', 3)
add(X, 'CONFIG global + per file', 'M', 1.5)
add(X, 'ENGRISH override table', 'C', 1, 'C')
add(X, 'Bass Mode (player sheet code + meta + level answers)', 'C', 10, 'W')
add(X, 'Mr. X Returns (+ chair boss)', 'C', 4, 'W')

# ---------------- VENUES (venue-specific code/data/tuning; shared tech counted above) ----------------
V = 'venues'
add(V, 'Wind: layout, SKY ACE mode + waves + POW/LOOP/drain/tally, AYACO sprite build, gusts, lamp/elevator, boss, wing room, room, YASHICHI, tests', 'M', 18)
add(V, 'Wind Should: re-sortie, hangar carts, Kite Mets, moving wing arena, AYACO BG', 'S', 4)
add(V, 'Knight: layout, ENCOUNTER, slimes/chest, keys/doors, ceiling HP, RADIANT, Metslime, NPCs, battle-log boss, Knightlord, tests', 'M', 17)
add(V, 'Knight Should: Inn, Princess Roll, clash/interrupt', 'S', 2.5)
add(V, 'Tomahawk: layout, posters, gallery, quick-draw, Sam, train ride (4 bands, tunnels), Sidewinder, Sheriff, outhouse, boss + high noon, tests', 'M', 18)
add(V, 'Tomahawk Should: Boot Hill, TNT crates, tomahawk knock-down', 'S', 1.5)
add(V, 'Plant: layout, vines, crocs, logs, tar pit, underground, cat/false floor, balloon, treasures, CONGA logs, lightning, boss, Lost City, tests', 'M', 18)
add(V, 'Blizzard: layout, ship icicles, climb (T6 bonk, Toppy refill, wrap), clouds, condor carry, bonus summit, boss, Cloud Summit, tests', 'M', 16)
add(V, 'Blizzard Should: ski run, SNOW CHAINS', 'S', 2)
add(V, 'Flame: layout, plates/gates, loose tiles, spikes, chompers, guards, chandeliers/oil, Shadow Rock merge, boss duel, tests', 'M', 16)
add(V, 'Flame Should: skeleton, mouse room, FIREPROOF, throne-room shadow', 'S', 4)
add(V, 'Centaur: layout, zone doors (honest/lying/fake), black zone, tide dwell + ZONE 100, tower wrap, plate T, boss, tests', 'M', 15)
add(V, 'Centaur Should: ZONE labels, Reap-bot, Nasubi Mage, hot spring, CENTURION, Sunken Throne', 'S', 6)
add(V, 'Yamato: layout, Jaja-nin bonk, passes/sekisho, scrolls, pogo EXWP, crest trapdoor, plate E, boss helmet-off, tests', 'M', 15)
add(V, 'Yamato Should: nightingale ceiling, Daruma (T8), DARUMA chip, kites, hanabi, Kabuki stage', 'S', 9)

# ---------------- NON-VENUE STAGES (fortress.md) ----------------
F = 'fortress'
add(F, 'Opening: layout, lanes/judges, high striker, parade + high fives, sabotage, Pi-kun (3 sizes), intro, room, tests', 'M', 12)
add(F, 'Semifinal: layout, 3 rejects + audition, blackout/fuses, Break Man beats, Bass beta duel 1 (copies), locker room, tests', 'M', 14)
add(F, 'E1 Block Man (falling-block engine + boss)', 'S', 9, 'C')
add(F, 'E2 Paddle Man (ball engine + boss)', 'S', 8, 'C')
add(F, 'E3 Invader Man (BG formation engine + boss)', 'S', 8, 'C')
add(F, 'E4 Maze Man (top-down maze mode + 4 ghost AIs + boss)', 'S', 9, 'W')
add(F, 'H1: layout, score balls, M.BEAM case, Guts lifts, Elec beams, Fire pillars, Big Eye, Yellow Devil (F-PIECES), tests', 'M', 11)
add(F, 'H2: force beams, password board, Heat blocks, Picopico, Mecha Dragon, tests', 'S', 11, 'C')
add(F, 'H3: presses, mirror hall fallback, magnet pull, Doc Robot (portable champion AI), Gamma 2 phases, Super room, tests', 'M', 13)
add(F, 'H3 Should: Gemini Rock (T7 reuse)', 'S', 2)
add(F, 'H4: dark rooms, bells, Balloon, compactor, Flip-Top, Cossack Catcher, tests', 'S', 11, 'C')
add(F, 'H5: low-grav, crystals, Super Arrow, geysers, letters, Dark Man (lying panel), 1993 wing, unmasking, tests', 'M', 12)
add(F, 'H5 Should: gravity flips', 'S', 3, 'C')
add(F, 'W1 Upgrade Lab (POCKET rooms, palette blocks, SUPER section, Enker, METALL 16)', 'S', 14, 'C')
add(F, 'W2: hub as bracket, pair bouts via loader, 8 SUPER copies portable, Championship Ring, Bass duel 2, tests', 'M', 10)
add(F, 'W3: Trophy Dispenser, MODE-7 machine (F-SIZES), Capsule SUPER, gift + CHAMPION BUSTER, escape, tests', 'M', 16)
add(F, 'Ending (9 scenes, lights-out per channel, CAPCOM TIMES)', 'M', 6)
add(F, 'Victory lap playable credits', 'S', 8, 'C')

# ---------------- PRODUCTION OVERHEAD ----------------
O = 'overhead'
add(O, 'user gates (Mesen runs, feedback rounds) ~1 per milestone x 10', 'M', 10)
add(O, 'balance pass (pars, prices, tables, presets)', 'M', 5)
add(O, 'emulator matrix + hardware + release packaging + readme', 'M', 4)

def tot(pred):
    return sum(s for a, i, t, s, p in I if pred(a, t, p))

areas = ['tech', 'systems', 'meta', 'venues', 'fortress', 'overhead']
print('CODE/DATA/TEST sessions by area and DOCS tier')
print(f"{'area':10} {'Must':>6} {'Should':>7} {'Could':>6} {'all':>6}")
for a in areas:
    m = tot(lambda A, t, p: A == a and t == 'M'); s = tot(lambda A, t, p: A == a and t == 'S')
    c = tot(lambda A, t, p: A == a and t == 'C')
    print(f"{a:10} {m:6.1f} {s:7.1f} {c:6.1f} {m+s+c:6.1f}")
M = tot(lambda A, t, p: t == 'M'); S = tot(lambda A, t, p: t == 'S'); C = tot(lambda A, t, p: t == 'C')
print(f"{'TOTAL':10} {M:6.1f} {S:7.1f} {C:6.1f} {M+S+C:6.1f}")
print()
print('PROPOSED v1.0 tiers (critic-scope)')
for a in areas:
    m = tot(lambda A, t, p: A == a and p == 'M'); s = tot(lambda A, t, p: A == a and p == 'S')
    c = tot(lambda A, t, p: A == a and p == 'C'); w = tot(lambda A, t, p: A == a and p == 'W')
    print(f"{a:10} M {m:6.1f} S {s:6.1f} C {c:6.1f} W {w:6.1f}")
pm = tot(lambda A, t, p: p == 'M'); ps = tot(lambda A, t, p: p == 'S'); pc = tot(lambda A, t, p: p == 'C'); pw = tot(lambda A, t, p: p == 'W')
print(f"TOTAL      M {pm:6.1f} S {ps:6.1f} C {pc:6.1f} W {pw:6.1f}")

# ---------------- ART / MUSIC / TEXT (from the ledgers) ----------------
print()
# art_audio.md §13.1 / §11.2
art = {'Must': (3228, 1623, 421), 'Should': (1208, 465, 107), 'Could': (72, 197, 45)}
# Claude-only throughput assumptions (draft quality): BG 80 tiles/session drafted, 200/session programmatic,
# sprites 12 animated frames/session (tiles included). Programmatic share of BG ~11% (510/4508).
def art_sessions(bg, spr, fr):
    prog = bg * 510 / 4508
    return (bg - prog) / 80 + prog / 200 + fr / 12
for k, (bg, spr, fr) in art.items():
    print(f"art {k:6}: {bg} BG + {spr} spr tiles, {fr} frames -> ~{art_sessions(bg, spr, fr):.0f} Claude sessions")
print(f"art all   : ~{sum(art_sessions(*v) for v in art.values()):.0f} sessions; human model in art_audio: 660 h Must / 890 h all")
# music: 37 compositions (+2 MMC5 layers) + ~4 missing (RIOT, FINAL LAP, POCKET arr., lights-out stems)
mus_full, mus_jingle = 30, 11
print(f"music: ~{mus_full} full tracks x1.5 + ~{mus_jingle} jingles x0.5 + SFX 70 (~4) = ~{mus_full*1.5+mus_jingle*0.5+4:.0f} sessions; Must 5 tracks + 20 SFX ~ 9")
# text: story.md §10.4 ~1,100 strings x 2 languages; Must ~600
print("text: ~1,100 strings EN+JP at ~90 strings/session (write+fit+compile checks) = ~24 sessions; Must ~600 = ~13 (+ external native JP review)")
