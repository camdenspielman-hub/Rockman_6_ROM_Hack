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

# ---------------- TECH FOUNDATIONS (tech.md round 2: "v1.0 scope" and §16) ----------------
# tech.md round 2: tiers = the round-2 tiers (RULINGS R1.1-R1.14). The Must rows sum to 102, the same as tight.py's
# tech block (was 98: +2.5 fight loader moved from meta (R1.7), +2 OAM-builder lag steps (R1.8), +1 $9B audit (R1.12),
# -1.5 F-SIZES to Should (R3.6)).
T = 'tech'
add(T, 'M0 MMC5 go/no-go spike on Mesen (+cart if any) BEFORE M1 (R1.1)', 'M', 1.5)
add(T, 'M0 scaffold/build/BPS/registry/allocator, bank + WORK ledgers, test runner, golden record', 'M', 4)
add(T, 'M0 reassemblable fixed banks + sound driver', 'M', 3)
add(T, 'M0 .lvl/MML round trips, censuses ($51/$063D/$9B, damage steps), stagetab', 'M', 4)
add(T, 'M1 MMC5 insertion, header, RESET, interrupt stubs, re-entrant CW, CALL7E, FAR (R1.4)', 'M', 2.5)
add(T, 'M1 bank helpers (vanilla A, R1.14), sound service/reader, NMI CHR bank, mirroring', 'M', 2)
add(T, 'M1 IRQ literal port of 27 chains + calibration', 'M', 3.5)
add(T, 'M1 shadow6 MMC5 + golden equivalence', 'M', 2.5)
add(T, 'M1 PRG-RAM pages/probe/save skeleton/mailbox, Mesen re-check, lag baseline', 'M', 2.5)
add(T, 'M2 stage record v0 (48 B), init hook, $CE44 on every id change (R1.7)', 'M', 1)
add(T, 'M2 WRAM layouts, tileset-slot loader, poke-list tiers, map-edit service (R1.10)', 'M', 3)
add(T, 'M2 families/sub-id dispatcher, object lists v2, slot plan (R1.11)', 'M', 3)
add(T, 'M2 CHR set table v2 + stage-local ids (R1.13)', 'M', 2)
add(T, 'M2 art pipeline chr.py/sprites.py/palettes.py/artcheck.py (R1.13)', 'M', 5)
add(T, 'M2 level pipeline build + checks + free-id table (scan before text, R1.14)', 'M', 3)
add(T, 'M2 generic raster list (24 bands, R1.9), presets, IRQ logic out of IRQ, compositor', 'M', 4)
add(T, 'M2 text v1a (ExRAM window, glyph cache, compiler + dictionary, pop-up coroutine, debrief/help; R1.4)', 'M', 3.5)
add(T, 'M2 sound: track table v2, bank bytes, reader, multiplier, play clock, mml compile, D9 mute mask (D1/D2/D6/D9/D11)', 'M', 4)
add(T, 'M2 DEV build: EXTRA CONFIG engine, warps, DEV combos (R1.14), ring buffer', 'M', 1.5)
add(T, 'M2 CHR stream: unrolled copier in ROM, WORK staging, queue (R1.6); lag steps 1, 5', 'M', 1.5)
add(T, 'M3 LATCHSRC, frozen tick + frozen handlers (R2.2), LFSR, death audit', 'M', 1.5)
add(T, 'M3 T6 variant blocks + X-BONK on the map-edit service', 'M', 2.5)
add(T, 'M3 GP player-state takeover + X-WRAP', 'M', 1)
add(T, 'M3 HUD widget module (X-METER/X-LABEL/F-CLOCK/counters as ONE module, R1.10)', 'M', 2)
add(T, 'M3 commentator event bus/queue/cooldown', 'M', 2.5)
add(T, 'M3 lag steps 3-4 (OAM builder; Must so the 9-slot cap is re-measured, R1.8)', 'M', 2)
add(T, 'M5 stage-attribute table: 45+11 readers, relocated tables, ids $10-$21, YOU GET row', 'M', 3)
add(T, 'M5 T3 switch->target', 'M', 2.5)
add(T, 'M5 T7 input mirror (pad history; Shadow Rock)', 'M', 2)
add(T, 'M5 T8 multi-part boss library (AYACO, Daruma kept by R3.2)', 'M', 2)
add(T, 'M5 attach state: T5 vines/pendulum, balloon, condor, claw, arrow (one state, R1.10)', 'M', 2)
add(T, 'M5 X-EXWP set-piece weapon (pogo)', 'M', 1.5)
add(T, 'M5 boss panel extension (fight-id records, 10th field, re-type)', 'M', 1.5)
add(T, 'M5 pattern-table split for menus', 'M', 1)
add(T, 'M6 text v1b (dialogue, world freeze, ROM restore, choices, NPC menus)', 'M', 2.5)
add(T, 'M6 T1-lite wave director (in the script slot) + RL_BANDS rides', 'M', 3)
add(T, 'M6 free-flight vehicle state (SKY ACE; lane flag for CANNON)', 'M', 1.5)
add(T, "M6 palette-flash/lighting service (Riot blackout, black zone, REDUCED fades; Knight RADIANT is Won't per R3.1)", 'M', 1.5)
add(T, 'M7 bgboss.py (poses, deltas, hit boxes, streams)', 'M', 2)
add(T, 'M7 fight loader + FIGHT_CTX + return-to snapshot (moved from meta, R1.7; W2, EXTRA CONFIG FIGHT, mailbox)', 'M', 2.5)
add(T, 'M7 F-PIECES on the map-edit service (BG body that comes apart)', 'M', 2.5)
add(T, 'M7 $9B tables relocated with a 4th (SUPER) row (R1.12)', 'M', 1)
add(T, 'M8 8-band floor (W3, R3.6)', 'M', 1.5)
add(T, 'section switch (slot B) + sections > 32 screens', 'S', 1.5)
add(T, 'F-SIZES (size frames streamed; R3.6)', 'S', 2)
add(T, '16-band MODE-7 floor (W3)', 'S', 3)
add(T, 'driver D3 (instrument table moved) + D10 (tempo override) + sndtest', 'S', 1.5)
add(T, 'X-FLOOR new floor types (ski, hot spring, nightingale)', 'C', 1.5)
add(T, 'X-UPEXIT exit type 7 (Ice Climber climb)', 'C', 1.5)
add(T, 'F-ERA (POCKET/NES/SUPER eras, flip-screen, letterbox, firmware flags)', 'C', 3)
add(T, 'ExGrafix in W1/METALL 16 locked rooms (mode-2 fill while blanked; R1.3)', 'C', 3)
add(T, 'OAM behind-BG priority override (W1 POCKET) + 256 B/frame top-blank band', 'C', 1)
add(T, 'fms2mml.py', 'C', 2)
add(T, 'MMC5 pulses 2nd driver instance (D5) + D7 charge + D8', 'C', 4)
add(T, 'F-GRID (deleted, R1.10: grids use the map-edit service)', 'W', 2.5)

# ---------------- SYSTEMS (systems.md) ----------------
Y = 'systems'
# systems.md round 2 (docs/design/systems.md "v1.0 scope"): tiers = the round-2 tiers (RULINGS R2.1-R2.11).
# The Must rows sum to 49.5, the same as tight.py's systems block.
add(Y, 'SELECT modifier + last-weapon toggle + input rules (GP_INTERACT, alt lock, mash/reflex/timer helpers)', 'M', 2)
add(Y, 'quick form swap: 2 KB stream, per-form $71-$7F slot-set map, set-piece sheet hook, debut cutscene', 'M', 3)
add(Y, 'forms fire weapon TAPS (dispatch table with alt/synergy columns, $0699 reset removed)', 'M', 2)
add(Y, 'adaptors by win count + FORMS.SUPER on the H3 dock', 'M', 1)
add(Y, 'B.ATTACK Ice Block alt (slice prototype: alt dispatch, encase, shell, platform contact)', 'M', 1.5)
add(Y, 'frozen tick: FRZKIND table, 3 frozen handlers, boss stall', 'M', 2.5)
add(Y, 'GP_BOSSHIT tables (v1.0 boss list) + generator + i-frame classes', 'M', 2.5)
add(Y, 'normal-enemy rules, re-hit timer, featured-enemy tell tables (no PART drop)', 'M', 1)
add(Y, 'WEAK! pop + stagger + SFX + flash-safety changes (C.FLASH, machine pulse, FLASH_GATE)', 'M', 2)
add(Y, 'LATCHSRC/SHOTCOL attribution + death convergence hooks (no punch re-class)', 'M', 2.5)
add(Y, 'scorecard counters + formulas + pars + skips + tokens', 'M', 3)
add(Y, 'bolts/economy/shop stock & prices, envelopes, prize caps', 'M', 2)
add(Y, 'chip framework (3-byte bits, slots, second-wind family)', 'M', 2)
add(Y, 'chip effects: 5 shop + Balancer', 'M', 2)
add(Y, 'chip effects: 8 venue behaviour prizes', 'M', 3)
add(Y, 'pickup routing, drops presets, respawn refill, game over', 'M', 2)
add(Y, 'presets + DIFF bits + CASUAL tier/lever helpers + INPUT LAG', 'M', 3)
add(Y, 'tap tweaks: B.ATTACK/PLANT.B costs, C.FLASH dark rooms', 'M', 0.5)
add(Y, 'plates->slots, Beat pit rescue (once per screen)', 'M', 2)
add(Y, 'HARD framework (IFHARD, layout tier)', 'M', 1.5)
add(Y, 'special cases SC1, SC5, SC6, SC8, SC9, SC11', 'M', 3.5)
add(Y, 'MAGNET BEAM build (max 2)', 'M', 2)
add(Y, 'Super Adaptor (fist with homing return + jet hop)', 'M', 3)
add(Y, 'controller-2 pseudo L/R', 'S', 0.5)
add(Y, '7 weapon ALTS (Time Stop + SC2, Wall Spear, Updraft, Hold, Flare, Feather Fan, Petal Shot)', 'S', 8.5)
add(Y, '8 form SYNERGIES (Pogo, Tailwind, Snow Bomb, Burning Knuckle, Petal Storm, Morning Star, Dive Throw, Time Fist)', 'S', 9)
add(Y, 'tap polish (Y.SPEAR pierce, PLANT.B 2 contacts) + M.BEAM magnet', 'S', 1.5)
add(Y, 'special cases SC4 (own-weapon hook), SC10 (COUNTER)', 'S', 1.5)
add(Y, 'W-tank, E-tank x2, overflow bolts, low-fuel pip', 'S', 1.5)
add(Y, 'Break Man tag partner (slot-0 variant, call row, moveset, gates)', 'S', 5)
add(Y, 'HARD content: per-stage poke lists + AI branches', 'S', 8)
add(Y, 'Power parry', 'C', 2)
add(Y, 'PARTs + garage + Mr. Y booth + Y-TURBO (one bundle, ships with the partner)', 'C', 4.5)
add(Y, '1993 RULES preset (1993 column, vanilla forms, shop off)', 'C', 3)
add(Y, 'small Coulds: ice grip, weakness star, RACING COLOURS, SC3, SC7, RULE column + OWNED override', 'C', 2.5)
add(Y, 'criticals (KAISHIN keeps the deterministic EXCELLENT MOVE)', 'W', 1)
add(Y, 'cut chips AFTERIMAGE, GLIDER, JET TUNER', 'W', 0.5)

# ---------------- META (meta.md) ----------------
X = 'meta'
# meta.md round 2 (docs/design/meta.md "v1.0 scope" and §13): tiers = the round-2 tiers (RULINGS R0.2-R0.4).
# The Must rows sum to 31, the same as tight.py's meta block. The fight loader (2.5) moved to tech (R1.7).
add(X, 'save module A/B ping-pong, trailer, migration, BROKEN paths, autosaves, IN_MATCH/unplug, save fuzz tests', 'M', 3.5)
add(X, 'title + boot: license line, health notice (R3.5), menu', 'M', 1.5)
add(X, 'file select cards + NEW/START/ERASE guards + difficulty pick (CASUAL/NORMAL/HARD)', 'M', 2.5)
add(X, 'bracket: node table, states, centre, rematch hook $3F:$F951, HALFTIME RIOT trigger, event queue', 'M', 4)
add(X, 'results screen (judges desk, slide-in rows, stamp, prize, secret icons)', 'M', 2.5)
add(X, 'debrief engine + predicate tables (tier B) + stage counters (collect-N, R1.10)', 'M', 2)
add(X, 'medals + HoF points + unlock bits', 'M', 1)
add(X, 'RULESET choke point + generated bits.inc (DIFF A: CASUAL b4, GUARDS b5, HARD b6, 1993 b7)', 'M', 0.5)
add(X, 'CONFIG global + per file (INPUT LAG, CASUAL, FLASHES REDUCED, A/B SWAP)', 'M', 1.5)
add(X, 'EXTRA CONFIG UI + scratch file + mailbox (settings overrides) + FIGHT n', 'M', 3)
add(X, 'pit stop UI (shop, 14-chip grid + B help, file CONFIG, SAVE & QUIT)', 'M', 2.5)
add(X, 'game over / RETIRE / unplug count', 'M', 1.5)
add(X, 'RECORDS pages 1-3 + venue mini-records', 'M', 1.5)
add(X, 'fight table v1.0 records + run order + loader interface (loader code is tech)', 'M', 0.5)
add(X, 'fortress maps (HoF, Castle) + REPLAY + BACK TO BRACKET', 'M', 1.5)
add(X, 'championship rating re-derived (100 reachable in v1.0, R2.7) + Break Man debrief', 'M', 1.5)
add(X, 'Time Attack (+ splits, DEV times, presets per stage, return kind 6, HUD TIMER, RECORDS page 4)', 'S', 3)
add(X, 'file COPY', 'S', 0.5)
add(X, "sponsor's-chair gag + Eddie SAVING icon + tier A escalation data", 'S', 0.5)
add(X, 'attract crawl (story S02 panels)', 'C', 1.5)
add(X, 'hidden PASS WORD gag', 'C', 0.5)
add(X, 'bracket Exhibition layer + badges', 'C', 1.5)
add(X, 'Riot intro animation', 'C', 1)
add(X, 'bundle hooks: garage + booth rows, DOPED, BREAK MAN WALKS, asterisks, T1/T6/T7 bundle rows', 'C', 1.5)
add(X, '1993 RULES meta hooks (NEW GAME choice, R1993_CLEAN, 93 badge, 1993 ROW)', 'C', 0.5)
add(X, 'GP Rush runner, lobby (Opening screen $1D), courses, MY GP', 'C', 5)
add(X, "RECORDS 5-6 + achievements (page 4 is Time Attack's)", 'C', 2.5)
add(X, 'ENGRISH override table', 'C', 1)
add(X, 'KNOCKOUT', 'W', 3)
add(X, 'Exhibition Rules + TURBO rule', 'W', 3.5)
add(X, 'Museum + VAULT + plaque gallery', 'W', 3.5)
add(X, 'Bass Mode (player sheet code + meta + level answers)', 'W', 10)
add(X, 'Mr. X Returns (+ chair boss)', 'W', 4)

# ---------------- VENUES (venue-specific code/data/tuning; shared tech counted above) ----------------
V = 'venues'
# venues_a round 2 (docs/design/venues_a.md "v1.0 scope"): each venue's v1.0 core = 14 (matches tight.py);
# the second set piece, the secret-arena twist and the SC4 jokes move to Should. Per-venue totals are unchanged.
add(V, 'Wind v1.0: layout (tower -2 screens), sortie data on the vehicle state (waves, POW/LOOP/drain/lamps/tally), simple AYACO, catapult/lamp board/elevator/LAND, room + seagull, YASHICHI, boss + 1D night fight, CASUAL, tests', 'M', 14)
add(V, 'Wind Should: gust decks (VA-GUST, Kite Mets, engine fans), destroyer, AYACO full + BG, WING WALKER on the wing + hangar art/carts, re-sortie, SC4 W.STORM', 'S', 8)
add(V, 'Knight v1.0: layout, King/Sage, search spots, keys/doors/chests, stairs key check + ladder, ENCOUNTER + slimes/chest, ceiling HP, Metal Metslime/KAISHIN, room, battle-log boss, Knightlord, CASUAL, tests (RADIANT cut by R3.1)', 'M', 14)
add(V, 'Knight Should: Inn, Princess Roll + Roll\'s Love, 1A throne staging, SC4 clash, W.STORM flip', 'S', 4.5)
add(V, 'Knight Could: EXP and level-ups, TRUE FORM', 'C', 1)
add(V, 'Tomahawk v1.0: layout, cactus re-skin, posters, gallery, judged quick-draw + Sam, train (3 bands, tunnels), Sidewinder, conductor count + EXPRESS, Sheriff, outhouse, STAR, boss + HIGH NOON MESA + RODEO RING, CASUAL, tests', 'M', 14)
add(V, 'Tomahawk Should: train sky band/shimmer + tunnel bats, rodeo-ring art, TNT crates, 12 re-board, poster page, tomahawk knock-down, SC4 catch', 'S', 4.5)
add(V, 'Tomahawk Could: vulture re-skin, W.STORM dust devil', 'C', 1)
add(V, 'Plant v1.0: layout rebuild, vines (attach state), crocs, logs, tar pits, treasures/log counter, underground, cat/false floor, balloon, storm + room, CONGA slot rule + checkpoint, boss (ring guard) + 1E night fight, CASUAL, tests', 'M', 14)
add(V, 'Plant Should: CONGA logs, swamp crocs, eels, Lost City ruins arena, vine burn, Ice Block croc, W.STORM balloon, SC4 clash', 'S', 4)
# venues_b round 2 (docs/design/venues_b.md "v1.0 scope"): core Must per venue; chips + Flame's mouse room are Must
# (R2.5, R0.4); second set pieces, arena twists and SC4 jokes are Should; HARD lists stay in systems' HARD line.
add(V, 'Blizzard v1.0 (M4 slice): layout, ship icicles, climb (T6 bonk, seal refill, wrap, ladder stubs), clouds, bonus summit + condor carry, cellar, SNOW CHAINS + foreman, boss + 1A re-palette, replay skip, Ice Block venue tests, CASUAL, tests', 'M', 13.5)
add(V, 'Blizzard Should: ski run, CLOUD SUMMIT twist, SC4 SNOWMAN, v1.1 tests', 'S', 3.25)
add(V, 'Blizzard Could: Shirokuma, jump-up exits (venue side; X-UPEXIT is Could in tech)', 'C', 0.75)
add(V, 'Flame v1.0: layout, plates/gates/timed gates, loose tiles, spike traps, guards (spacing parry), gallery chandeliers/oil, Shadow Rock merge + glow, mouse room, FIREPROOF + marshal, hourglass + loose bridge, spacing-duel boss + 1A re-palette, CASUAL, tests', 'M', 13)
add(V, 'Flame Should: chompers, skeleton, throne-room Shadow Flame Man, SC4 ABSORB, vizier, v1.1 tests', 'S', 4)
add(V, 'Centaur v1.0: layout, ZONE cards, zone doors (BG + tables), black zone + ZONE 0, tide dwell + 0D lift + ZONE 100, tidal shaft (R3.1), Centurion statues + CENTURION, Pegasus gap + plate T, boss + 1C re-palette, CASUAL, tests', 'M', 13.5)
add(V, 'Centaur Should: Reap-bot, Nasubi Mage, hot spring, Centurion boss help, Sunken Throne, ZONE 100 currents, SC4 SAY CHEESE, v1.1 tests', 'S', 5)
add(V, 'Centaur Could: eggplant curse', 'C', 1)
add(V, 'Yamato v1.0 (trimmed, R3.2): layout, Jaja-nin bonk-stun, scrolls + the draft exit, Daruma (T8, 2 parts) + DARUMA, pogo set piece + crest vault, plate E, vanilla bypass, boss + 1D re-palette, CASUAL, tests', 'M', 13)
add(V, 'Yamato Should: nightingale floor + re-homed ceiling, kabuki revolving stage, bells, boss ashigaru, SC4 PARRY, v1.1 tests', 'S', 4.75)
add(V, "Yamato Won't (R3.2, R3.1): sekisho + passes + runner, kite run, hanabi", 'W', 2)
add(V, 'venues_b tag-partner shortcuts (4 venues; ship with the partner bundle)', 'C', 1)

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
