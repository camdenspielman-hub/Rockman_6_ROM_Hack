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
# tech.md round 2: tiers = the round-2 tiers (RULINGS R1.1-R1.14). The Must rows sum to 102.5, the same as tight.py's
# tech block (was 98, then 102: +2.5 fight loader moved from meta (R1.7), +2 OAM-builder lag steps (R1.8), +1 $9B audit
# (R1.12), -1.5 F-SIZES to Should (R3.6); round 3: attach state split M3/M5 (R8.2), +0.5 ending engine pieces).
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
add(T, 'M3 attach state core + the condor (one state, R1.10; slice per R8.2)', 'M', 1)
add(T, 'M5 attach state users: T5 vines/pendulum, balloon (R8.2); claw, arrow ride on the core', 'M', 1)
add(T, 'M8 ending engine pieces: CAPCOM TIMES GP pages via the new engine, credits room table + CREDITS bit (round 3)', 'M', 0.5)
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
# fortress.md round 2 ("v1.0 scope"): tiers = the round-2 tiers (RULINGS R0.2-R0.4, R3.6, R3.7). The Must rows sum to
# 70, the same as tight.py's fortress block (was 69: +1 for the ending's credits mode, fortress §6.2). Shared engine
# pieces (F-PIECES, the fight loader, RL_FLOOR8, F-SIZES, F-ERA, HUD widgets) are counted under tech; HARD per-stage
# lists under systems' HARD line.
F = 'fortress'
add(F, 'Opening-lite v1.0: tunnel + scenes as POP sequences (<= 15 pages), 4 lanes/judges (DAMAGE/TIME/STYLE/SECRETS), high striker, beach balls, scoreboard, parade (1 float per screen) + high fives, sabotage, Grand Pi-kun ONE size, dressing room, CASUAL, tests', 'M', 8)
add(F, 'HALFTIME RIOT v1.0: layout, VENDING + CHEER + audition rule, blackout + fuse boxes + master breaker, Bass sighting + crumble, NPC Break Man beats (help/crowd, block, reveal + Rule 9 in place), Bass beta duel 1 (4 pre-drawn copies, NO DATA, overdrive, help capsule), locker room, CASUAL, tests', 'M', 10)
add(F, 'H1 v1.0: Wily 2 remix, SCORE + 24 score balls, M.BEAM case + 96-px gap, appearing blocks as BG cells, Elec beams, Fire pillars, Big Eye, Yellow Devil on F-PIECES, archive + storeroom, CASUAL, tests', 'M', 9)
add(F, 'H3 v1.0: Mr. X 3 remix, Rush Coil, statue, needle presses, Gemini laser hall, Kamegoro Maker (re-skinned vanilla dispenser), fist-ride practice beat, Gamma head + fists (SC5), Super dock + demo, workshop via M.BEAM stair, CASUAL, tests', 'M', 10)
add(F, 'H5 v1.0: Mr. X 4 remix, low gravity (+ bubble flag) incl. the gravity hall low-grav form, crystals, Super Arrow, MEGAMAN V letters, 1993 wing + Mr. X card, Dark Man (lying panel, WRONG NOTE), unmasking (two masks, cup, castle picture palette steps), CASUAL, tests', 'M', 9)
add(F, 'W2 v1.0: SUPER-palette moat, hub as bracket board, pair bouts through the fight loader (hub-run TAG chain, +10 HP), 8 SUPER copies (records, palettes, pinch 14), Championship Ring + ropes, Bass duel 2, losers room, CASUAL, tests', 'M', 8)
add(F, 'W3 v1.0: Wily 4 remix, Trophy Dispenser + GP Cup, WILY MACHINE 6.5 (vanilla art retinted, 8 bands, drag, mortar shadow), Capsule SUPER (decoys, glow-band blast), gift + CHAMPION BUSTER, phase checkpoints, escape (clock, mercy, crumbling ladders, palette downgrade, Wily at the door), trophy room, CASUAL, tests', 'M', 11)
add(F, 'Ending v1.0 (R4.1 order): pixelation, S40 catch, arrest, podium + vow, CAPCOM TIMES (no $94), vanilla staff roll + DWNB cards with the bosses\' credits mode, rating hookup, LIGHTS OUT cue sync, sixth wing, silent TO BE CONTINUED', 'M', 5)
add(F, 'Opening Should: Grand Pi-kun three sizes on F-SIZES', 'S', 1)
add(F, 'Riot Should: UMBRELLA MAN (parachute, no shield), roof gust (VA-GUST), partner join pages + banner, TAG locker door', 'S', 1)
add(F, 'H1 Should: Guts Man tipping lifts, tag pocket, box-art figure', 'S', 1.25)
add(F, 'H3 Should: Doc Robot MK-VI copying AIR MAN through the fight loader, magnet pull (VA-GUST), tag pocket', 'S', 3.25)
add(F, 'H5 Should: Wave Man geysers, TWO BREAK MEN with the partner, tag pocket', 'S', 1.25)
add(F, 'W3 Should: THE APPROACH phase (drive-toward-camera sizes; F-SIZES and RL_FLOOR16 are tech), Flip-Top Jr. escape cameo', 'S', 1.5)
add(F, 'H2 ROCKMAN 2 wing: force beams (map_set), password board, Heat blocks, Picopico-kun on F-PIECES, Mecha Dragon, AIR MAN room', 'S', 11)
add(F, 'H4 ROCKMAN 4 wing: flash-bulb photo puzzle, chapel bells, Balloon, Dust Man conveyors, Flip-Top Jr., Cossack Catcher', 'S', 11)
add(F, 'W1 Upgrade Lab (POCKET rooms, palette blocks, 16-bit section with locked ExGrafix rooms, Enker, METALL 16)', 'C', 14)
add(F, 'Escape eras (F-ERA in reverse) + castle picture ExGrafix bloom', 'C', 1)
add(F, 'H5 Could: gravity arrows (flip rooms + Dark Man arena flip)', 'C', 3)
add(F, 'E1 Block Man (single arena on map_set/T6)', 'C', 4)
add(F, 'E2 Paddle Man (single arena)', 'C', 4)
add(F, 'E3 Invader Man (single arena, CANNON on the vehicle state)', 'C', 4)
add(F, 'Victory lap (one lap, playable credits)', 'C', 6)
add(F, 'E4 Maze Man (top-down MAZE mode, 4 ghost AIs)', 'W', 9)
add(F, 'Gemini Rock input-mirror twin (R3.1 keeps the laser)', 'W', 2)

# ---------------- PRODUCTION OVERHEAD ----------------
# The Must rows sum to 16, the same as tight.py's overhead block and PLAN §4.1 (R8.1's code 377.5 includes it;
# round 1's 19 was the untrimmed figure).
O = 'overhead'
add(O, 'user gates (Mesen runs, feedback rounds) at the gates and milestone reviews', 'M', 8)
add(O, 'balance pass (pars, prices, tables, presets)', 'M', 4)
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
# art_audio.md round 2 ("v1.0 scope", §11, §13; R5.1 no-artist baseline, R5.3 re-run). Source of every number:
# build/revise/art_audio/budget_r2.py (art) and music_r2.py (music + SFX). Rows: (BG tiles, sprite tiles, frames, sessions).
# Methods: reuse/recolour R, composite X (both "R" in R5.1's sense), programmatic C, Claude draft D (final; no artist).
# Session model: D 80 BG tiles or 12 frames, X 18 frames (or 150 tiles), R 300 tiles + 24 frames, C 200 tiles per session,
# +5 % for the fixes the art-acceptance gates ask for. The 240 1-bpp text glyphs (Must) are inside the Must row's sessions.
art = {'Must': (2567, 1968, 354, 51.6), 'Should': (1684, 518, 114, 29.7), 'Could': (828, 384, 64, 14.5),
       "Won't": (20, 279, 63, 4.6)}
for k, (bg, spr, fr, ses) in art.items():
    print(f"art {k:6}: {bg} BG + {spr} spr tiles, {fr} frames -> ~{ses:.1f} Claude sessions")
art_msc = sum(v[3] for k, v in art.items() if k != "Won't")
print(f"art M+S+C : ~{art_msc:.1f} sessions (no human hours: R5.1's baseline has no pixel artist; a human pass is optional polish)")
# music (R5.2: art_audio owns the one track list): tracks, bytes, new SFX, sessions (full 1.5, loop 1, jingle 0.5, 12 SFX/session)
music = {'Must': (7, 3740, 21, 9.0), 'Should': (18, 13180, 35, 26.4), 'Could': (15, 10550, 7, 19.1), "Won't": (2, 1500, 0, 3.0)}
for k, (n, b, sfx, ses) in music.items():
    print(f"music {k:6}: {n} tracks, {b} B, {sfx} new SFX -> ~{ses:.1f} sessions")
print("music Must = G00-G04, G27 WHISTLE (2 s), G37 LAST MATCH (2A03 stems) + 21 new SFX in the $36 tail (392 of 449 B)")
# text: story.md §10.4 (round 3, counted by build/revise/story/fit.py): translated strings (EN+JP) Must 397
# (R4.5's kinds 333 + Must mechanics' text 64), Should 362, Could 90, Won't 5; plus 28 Must labels and 18 panel records.
print("text: Must 397 strings EN+JP at ~40/session + M2 setup + M9 review fixes = ~12 sessions (tight.py); "
      "Should 362 (short pop-ups, drafted) = ~7; Could 90 = ~3; Won't ~0.5 (+ external native-JP review, gates release)")
