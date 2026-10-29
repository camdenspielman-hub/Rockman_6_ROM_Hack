# Heritage Venues B: Blizzard, Flame, Centaur, Yamato (design-venues-b)

Status: **v3 (design round 3), revised against [`RULINGS.md`](RULINGS.md) §8 and [`reconcile.md`](reconcile.md).**
Owner: design-venues-b. Scratch:
`build/revise/venues_b/` (round 1: `build/design/design-venues-b/`).

This doc designs four of the eight Heritage Venues of Rockman 6 GP:

| Venue (on-screen name, R3.3) | Stage id (R1.2) | Homage (design notes only; never on screen) | Vanilla set piece kept, with one twist |
|---|---|---|---|
| **Blizzard Man: SUMMIT CLIMBER** | `$00` | *Ice Climber* (1985) | the rocking icebreaker (now it shakes icicles loose) and slippery ice |
| **Flame Man: PERSIAN PALACE** | `$03` | *Prince of Persia* (1989, FC 1992) | igniting oil (now a choice you make, and it stays made) |
| **Centaur Man: ATLANTIS RUINS** | `$07` | *Atlantis no Nazo* (1986), *Kid Icarus* (1986) | the tide (now the venue's spine: a lift, a lock and a flooding shaft) |
| **Yamato Man: EDO NINJA ROW** | `$04` | *Ninja Jajamaru-kun* (1985), *DuckTales* (1989, Capcom) | the E-plate Jet ledge (now the plate waits on the castle roof); the charged-punch bypass and its dark mid-boss room, kept as they are. v1.1 re-homes Knight's falling ceiling under a nightingale floor |

**What binds this doc.** [`RULINGS.md`](RULINGS.md) first, then [`BRIEF.md`](BRIEF.md). The single sources of truth
are: `systems.md` for combat, the economy and chips; `meta.md` for save bytes, the bracket, events and the debrief;
`tech.md` for ids, memory, raster and CHR; `story.md` for **every word** and the ending; `art_audio.md` for the tile,
byte and track budgets. **This doc owns the staging of its four venues:** screens, set pieces, secret gates, objects
and their placements, boss patterns and reactions, and the CASUAL and HARD levers. Where it quotes a number another doc
owns, that doc wins; where it needs something from another doc, it says so in §5.3.

Every vanilla map was read from `docs/research/rm6/img/maps/` (`00_blizzard`, `03_flame`, `04_yamato`, `07_centaur`).
Vanilla screen numbers are written **v0E**; GP screen numbers are plain **0E**.

---

## v1.0 scope

v1.0 is the **tight Must** (R0.2). Each venue ships its **core**: the homage mechanic, the secret exit, the hidden
room, the behaviour chip and the boss rework. Each venue's **second set piece and its secret-arena twist are Should**
(v1.1+, cut-line item 4 of R0.3). **A Must depends only on Musts** (R0.4), so every Should below names what v1.0 ships
in its place. Blizzard is the **v0.1 vertical slice** (R0.2, RULINGS §6 M4) and is specified first and completely (§1.0).

### What ships in v1.0 (Must), per venue

| Venue | Core (Must, v1.0) | Second set piece and arena twist (Should, v1.1+) | Could | Won't (v1) |
|---|---|---|---|---|
| **Blizzard** (M4, v0.1) | Harbour and the rocking ship with falling icicles; the Ice Climber climb (head-bonk breaks ice cells, seals refill them, screens wrap, ladder stubs up); the 40-s bonus summit with vegetables and the **condor** (secret exit); the no-wrap floor to the Vegetable Cellar (hidden room); **SNOW CHAINS**; the boss rework (SLALOM, FLAKES with the ice block, SNOWBALL, AVALANCHE, MELT); secret arena = the boss room re-paletted; the **Ice Block** alt as the alt-dispatch prototype (R2.4); the bonus skip on replays (R3.8) | the ski run (v1.0: plain downhill steps); the CLOUD SUMMIT arena twist; the SNOWMAN own-weapon reaction (SC4); the bonus jingle | Shirokuma; jump-up exits (X-UPEXIT; v1.0 and v1.1: ladder stubs) | - |
| **Flame** (M5) | The oil field and the ignition lesson; the PoP dungeon (plates, portcullises, the timed gate you slide under, loose tiles, spike traps, palace guards with the **spacing parry**); the oil gallery's chandeliers; the mirror merge with **Shadow Rock** (secret exit); the **mouse** room (hidden room, R2.5); **FIREPROOF**; the fire vault's hourglass gate and loose bridge; the boss rework (the spacing DUEL, PILLARS, LEAP, THE PALACE BURNS, BLOWOUT); secret arena re-paletted | the chomper hall (v1.0: a spike hall); the skeleton (v1.0: a guard); the throne-room Shadow Flame Man; the vizier (Wily in costume); ABSORB (SC4) | Roll's cameo; the palace music | - |
| **Centaur** (M5) | ZONE cards; honest, lying and fake doors; the black zone and **ZONE 0** (hidden room); the tide with its dwell, used as a lift (0D) and a lock (**ZONE 100**, secret exit); the **tidal shaft** that floods as you climb (R3.1, replacing the wrap tower); the **Centurion statues** and **CENTURION**; the Pegasus gap and plate T; the boss rework (tide-picked moves, TIME FLASH, the ABILITY UNKNOWN slot reel, STUMBLE); secret arena re-paletted | the Kid Icarus cast (Grim Reap-bot, Nasubi Mage, hot spring); the Centurions' help in the boss fight; the SUNKEN THRONE twist; ZONE 100's currents; SAY CHEESE (SC4) | the eggplant curse; the underwater music | - |
| **Yamato** (M5), **trimmed** (R3.2) | The rooftop **bonk-stun** (kept); spinning scrolls; the **Daruma** (two-part) and **DARUMA**; the **spear pogo** over caltrops (homage mechanic) and the crest trapdoor to the vault (hidden room); **the draft** in the hall of scrolls (secret exit, R3.1: "the scroll gate alone"); vanilla's charged-punch bypass and dark room; plate E; the boss rework (RUSH, VAULT, WALL SPEARS, HELMET OFF, SNAP); secret arena re-paletted | the nightingale floor with Knight's ceiling (v1.0: a plain gold hall); the kabuki revolving stage; the bells; the ashigaru helpers in the boss fight; PARRY (SC4) | kuroko stagehands | the **sekisho**, its three passes and the runner ninja (R3.2, designer's choice); the **kite run** (R3.2); the **hanabi** lights-on-a-timer (R3.1) |

All four behaviour chips, all four hidden rooms (Flame's mouse room included) and all four secret exits are Must (R2.5,
scope-3). The per-venue HARD poke lists and boss AI branches are Should (R2.9, cut-line item 3); v1.0 HARD is the
global ×1.5 damage, drops LESS, no refill (`systems.md`). Every venue fills in the CASUAL standard lever list (R2.9;
§1.12, §2.10, §3.12, §4.11). Weapon alts and synergies are Should (R2.4) except **B.ATTACK's Ice Block**, which ships
in the Blizzard slice.

### Session estimates (venue code, data and tests; shared engine work is counted under tech and systems)

| Venue | Must (v1.0) | Should (v1.1+) | Could | Won't | Note |
|---|---|---|---|---|---|
| Blizzard | **13.5** | 3.25 | 0.75 | - | +1.5 on round 1's tight figure: SNOW CHAINS is Must (R2.5), the bonus skip (R3.8) and the Ice Block venue tests (R2.4) |
| Flame | **13** | 4 | - | - | +1: the mouse room and FIREPROOF are Must; the chompers drop to Should |
| Centaur | **13.5** | 5 | 1 | - | +1.5: CENTURION is Must; the tidal shaft replaces the wrap tower at about the same cost |
| Yamato | **13** | 4.75 | - | 2 | +1: the Daruma and DARUMA are Must; the sekisho, passes and runner leave |
| Tag-partner shortcuts (4 venues) | - | 1 | - | - | Should (cut-line item 2, with the tag partner: R0.3, R4.2) |
| **Total** | **53** | **18** | **1.75** | **2** | `tools/plan/tally.py` and `tight.py` carry these figures |

The four Must figures are 5 sessions above round 1's tight estimate (48), all from rulings that promoted content to
Must. Each Should figure includes about one session of v1.1 tests and golden-movie re-records. The per-venue HARD lists
are not here: they sit in systems' single HARD-content line of the ledger. All figures are re-estimated from actual
counts after the slice (R0.1): the Blizzard number becomes the calibration for the other three.

**Per milestone** (RULINGS §6's cumulative column adds these up, R8.1): **M4 13.5** (Blizzard, the slice) and **M5
39.5** (Flame, Centaur and Yamato); the Should and Could rows are v1.1+. The four champions' credits mode (§1.10, §2.8,
§3.10, §4.8) is counted in fortress's ending (M8), not here.

### Release rungs

- **v0.1 "Blizzard slice" (M4):** §1, complete: new game → bracket → SUMMIT CLIMBER (exit, room, chip, Ice Block,
  boss) → judges → save, reload, replay. It needs none of the M5 stage-attribute work (stage id `$00` keeps the ship's
  hard-wire, and its GP code reads the 48-byte stage record v0 from M2.1, with no stop-gaps: R8.2), no T3, no text v1b,
  no forms and no other venue (§1.0).
- **v0.5 "Round One" (M5-M6):** Flame, Centaur and Yamato after the stage-attribute table (M5): the tide's dwell is an
  `EFX_PARAM`, and T3, T7 and T8 arrive with them.
- **v1.0 "Championship":** unchanged venues, refought in W2 through the fight loader (§5.3).
- **v1.1+:** the Should rows above, in R0.3's order: alts and synergies (item 1), then the tag partner's shortcuts
  (item 2), HARD lists (item 3), then each venue's second set piece and arena twist (item 4).

---

## 0. Rules shared by the four venues

### 0.1 Tags and tiers

- Each item carries the BRIEF §8 marks: **[engine-ok]** (vanilla does it with data only; anything that needs code is
  **[new-code]**, R1.14), **[new-art]**, **[new-music]**, a size **S/M/L** and a tier. `[new-code M · Should]` means
  new code, medium size, Should tier.
- **Must** = ships in v1.0. **Should** = v1.1+, re-added in R0.3's cut-line order. **Could** = later, if ever.
  **Won't (v1)** = cut by a ruling; the idea is recorded so it can come back in a later version.
- **A Must depends only on Musts** (R0.4). Every Should item names its v1.0 stand-in ("v1.0:").

### 0.2 Ids, screens and budgets

- **Stage ids** (R1.2, tech §4.2): venues are `$00-$07`; these four keep vanilla's: Blizzard `$00`, Flame `$03`,
  Yamato `$04`, Centaur `$07`. The ship's and the tide's collision offsets (`$3E:$DA1C-$DA6A`) are hard-wired to ids 0
  and 7, so both set pieces work before vanilla's `$51` readers are rewritten for the stage-attribute record (M5). That
  is why Blizzard can be the slice: its GP code reads only the 48-byte record v0, which exists from M2.1 (`SECRET_SCR`,
  `PAR`, GP_BOSSHIT's row; no stage-`$00` stop-gaps: R8.2, tech §4.1). The tide's GP dwell is `EFX_PARAM` in the
  attribute record (tech §4.4), so Centaur waits for M5. Yamato's re-homed ceiling (Should) also needs the table.
- **Layouts:** one 32-screen layout per venue (8 rows × 256 blocks, screens `$00-$1F`). The main route counts up from
  00; branches, the secret route and arena, and the hidden room live in the high screens, entered by exits with
  explicit targets (vanilla practice, `levels.md` §9). The new layouts may overwrite vanilla layout banks `$32/$33`
  once vanilla ids 0-7 have their regression movies (R1.5).
- **Tilesets:** tech owns one slot table (R1.10): the RAM-image model, 2 slots per bank, an **independent alternate set
  per slot**. Round 1's request for a whole 8 KB bank per venue is withdrawn (consistency-9). What these venues need
  from the slot is listed per venue: T6 variant blocks (Blizzard's ice cells, Flame's loose tiles, Yamato's crest),
  distinct oil metatile ids (Flame's gallery), and, in v1.1, the kabuki set swap.
- **Lag (R1.8): every occupied slot counts, cap 9.** On a venue screen: the player (1) + the screen script in slot 22
  (1, always counted) + the player's shots (3, the buster's maximum) leave **at most 4 stage objects**. A stage object
  is anything in an enemy slot: enemies, their bullets, set-piece sprites, NPCs, pickups that are objects, and
  transient effects (T6 debris, explosions). The screen tables give each screen's peak in brackets: **[4]** means 4
  stage objects, 9 slots in all.
  - Where Rock cannot fire (the pogo hall, Yamato 12-13), the cap allows 7 stage objects; the tables say so.
  - **Boss rooms:** the boss (1) + **boss-side objects ≤ 3** (projectiles, helpers, props) = 9. Two requests to
    systems keep it there: the WEAK! pop spawns only while fewer than 3 boss-side objects are out (otherwise it is
    skipped; the stagger and the crunch still play: systems makes the pop optional under load), and the CENTURION
    chip's helper (a player-side utility in slots 4-7) is one more occupied slot, so while it hovers each boss here
    throws one projectile fewer per move.
  - A player utility in slots 4-7 (the Ice Block, R1.11) or B.ATTACK's fourth flake can lift a 4-object screen to 10
    for its lifetime. The slice measures exactly this (§1.0, test G7) on Blizzard 0A, 0D, 10 and the boss; if a
    screen lags past the 9-slot band, its object count drops to 3 (in the boss room, FLAKES throws one flake fewer
    while the Ice Block is out: R8.6, §1.10).
  - The design trick that keeps these numbers: **BG until it moves.** Hanging icicles, loose tiles, zone doors and
    plaques, the crest and Yamato Man's wall spears are BG cells or map edits; only the moment they move costs a slot.
- **Checkpoints:** two mid-stage checkpoints plus the boss shutter (vanilla has one plus the shutter). A checkpoint is
  the `LDA #s / JMP $8416` routine; every checkpoint screen gets a palette program that sets everything it needs
  (`levels.md` §19: palettes are cumulative deltas). CASUAL adds one per section through its poke list (§0.7).
- **Pop-ups** sit at the top by default (tech `EFFECTS` b6 clear; consistency-26). None of these venues needs the
  bottom position: the ship's and the tide's bands are below the window band.

### 0.3 The gate matrix

Each venue has one secret exit, one one-screen hidden room and one behaviour-gated chip (BRIEF §5.4), **all Must**.
They use different kinds of gate so the four venues don't feel alike, and **nothing here needs an adaptor, an alt, a
synergy, a form or Break Man** (`systems.md` §2.4). Only the plates (Jet, as in vanilla) and Yamato's bypass (Power, as
in vanilla) are adaptor-gated, and neither is on the main route.

| Venue | Secret exit (kind) | Hidden room (tell) | Behaviour chip | Plate | Adaptor extras |
|---|---|---|---|---|---|
| Blizzard | **Catch the condor** in the 40-s bonus round (timing) | One climb floor doesn't wrap: a seal walks off it and doesn't come back | **SNOW CHAINS**: never destroy a seal | none | a Power-block crate on the ship (07) |
| Flame | **Don't fight your shadow**: hold fire until the mirror glows, then walk into it (behaviour) | A shut gate with a mousehole: stand still, and the mouse presses the plate (patience) | **FIREPROOF**: reach the shutter with no oil ignited | none | a Power-block 1-up (02) |
| Centaur | **ZONE 100**: a sunken door that opens only at the lowest tide (timing) | **ZONE 0**: in the black zone, one door glows only in the dark (light) | **CENTURION**: free the three stone soldiers with full charges | **T** across the Pegasus gap (Jet) | the Jet sky route |
| Yamato | **The draft**: in a hall of five still scrolls, a lantern flame leans toward the one that turns (observation) | Pogo on the gold crest in the caltrop hall: a trapdoor opens (tool) | **DARUMA**: win the daruma otoshi without touching its head | **E** on the castle roof (Jet) | the charged-punch bypass (Power) |

- **Collect-N secrets** (R3.1): at most one per stage. CENTURION's three statues are the only one in these venues, and
  it uses meta's stage-counter predicate (R1.10).
- **Route choices.** In Centaur and Yamato the plate route and the secret exit branch off at different points, so one
  visit takes one or the other; a replay takes the other (replays for the other exit are allowed: meta removes
  vanilla's beam-out, consistency decision 38). Flame's secret route skips the fire vault, mouse room included;
  Blizzard's skips only the descent.
- **Exhibitions.** meta pairs E3 = Blizzard + Flame and E4 = Centaur + Yamato. The Exhibitions are Could (v1.1) and E4's
  Maze is Won't (v1) (R3.7), so in v1.0 these secret exits pay SECRETS (weight 3) and the rating's route test only.

### 0.4 Shared mechanics: tech's single engines (R1.10)

Round 1's working labels (X-…) map onto tech's single engines. The engines are tech's; the uses are this doc's.

| Engine (owner, tier) | Round-1 label | Uses here (tier of the use) |
|---|---|---|
| **Map-edit service**: `map_set` + a per-id alternate flip, one repaint queue (tech §5.6, Must) | T6, part of X-BONK | ice cells, loose tiles, the crest trapdoor (via T6); hanging icicles; the summit gate and the replay skip door (Blizzard, no T3 needed in the slice); Flame's timed arena oil; Yamato Man's wall spears (all Must); the kabuki set swap (Should) |
| **T6 variant blocks** (tech §10, Must) | T6 bitmap | Blizzard's ice cells and their refill; Flame's loose tiles; Yamato's crest. The bitmap is tech's fallback only |
| **Ceiling-probe callback** (tech §7.9, Must) | X-BONK | Blizzard: break the cell above (`t6_break`). Yamato: stun the enemy standing on the bonked floor cell |
| **X-WRAP** (tech §7.9, Must) | X-WRAP | Blizzard's climb only (Centaur's wrap tower is gone, R3.1) |
| **Exit type 7** (tech §7.9, Could) | X-UPEXIT | Blizzard's climb (Could). v1.0: a 2-rung ladder stub at each climb screen's top |
| **Attach state** (R1.10, tech §7.9, Must) | condor carry | Blizzard's condor (Must), its first user: the core is built at M3 with the condor (R8.2, tech §7.9); Plant's vines and balloon follow at M5 |
| **GP player states** (tech §7.9, Must) + the **set-piece player sheet** (R2.3) | X-EXWP | Yamato's pogo (Must): the sheet streams at the rack, a locked moment |
| **HUD widget module** (R1.10, Must) | X-METER, X-LABEL | the bonus meter (Blizzard), ZONE cards (Centaur) (both Must) |
| **Families and sub-ids** (tech §7.2, Must) | X-GPOBJ | every new object kind here (about 37 after the cuts, §5.1) |
| **T3 switch → target** (tech §7.10, Must) | T3 | Flame's plates, gates and timed gates; Centaur's door warps; Yamato's scroll spins (all Must, M5) |
| **T7 input mirror + pad history** (tech §7.9, Must, M5) | T7 | Shadow Rock (Must: Flame's secret exit, R0.4); Shadow Flame Man (Should) |
| **T8 multi-part boss** (tech §7.11, Must, M5) | T8 | the Daruma (Must: DARUMA is Must, R0.4), two parts |
| **New collision groups via `GRP_ROW`** (tech §4.5, Could) | X-FLOOR | ski snow, the hot spring, the nightingale boards (all Should: re-adding any of them pulls X-FLOOR in with it) |
| **`EFFECTS` / `EFX_PARAM`** (tech §4.4, Must) | stage-attribute table | `SHIP` (Blizzard; hard-wired by id 0 until M5), `TIDE` + dwell (Centaur, Must), `CEILING` (Yamato, Should) |
| **Raster presets** (tech §8, Must) | chains 1, `$14`, `$11` | `RL_SHIP`, `RL_TIDE` (Must); `RL_CEILING` (Should) |
| **Hook registry** (tech, Must) | ignition hook | FIREPROOF's clean bit on `$3E:$DDFC`; the ship thread's turn event (icicles) |
| **Fight loader + FIGHT_CTX** (R1.7, Must) | - | W2 refights all four champions in their own arenas (§5.3) |
| **Credits room table + `GP_MODE` b0 `CREDITS`** (tech §4.6, Must, M8) | - | the v1.0 credits show each champion in his own boss room with no Rockman: each AI's credits mode tests `IFCREDITS` (§1.10, §2.8, §3.10, §4.8; fortress §6.2) |
| **Commentator bus** (tech/story, Must) | - | every hook in this doc |

### 0.5 Weapons: superseded by systems.md

Round 1's weapon proposals (§0.5) and every "proposed row" of boss damage are **superseded by `systems.md` §3 (weapons)
and §4 (Tables 1-2, SC1-SC14)** (consistency-33). Weakness i-frames are 16 f, not 8. This doc keeps three things:

1. **Boss previews.** Each boss performs its weapon's alt or synergy as a boss move before the player owns it. That
   is AI, not player code, so it stays in v1.0 although the player's alts are Should (R2.4).
2. **Reactions.** Each champion's WEAK reaction (SC9, Must) and own-weapon reaction (SC4, Should: systems tiers the
   hook Should) are defined in the boss sections.
3. **Venue jobs** for the weapons:

| Weapon | v1.0 jobs (Must: the taps, and the Ice Block) | v1.1 jobs (alts and synergies, Should) |
|---|---|---|
| **B.ATTACK** | the vanilla thematic one-shots on fire robots (Flame's Tellies and jugglers). **The Ice Block, the slice's prototype (R2.4):** encases seals and birds (Blizzard: platforms), stops Blizzard Man's snowball, freezes burning oil into a 300-f floor (Flame 13), encases ninjas into steps (Yamato) | Snow Bomb (Jet) |
| **F.BLAST** | melts `$D` ice (Blizzard 0C and 18 pockets); burns shoji (Yamato 08); ignites oil through `$3E:$DDFC` (systems OQ1) | Flare melts the ice cell above you (a faster climb); Burning Knuckle |
| **C.FLASH** | lights a dark room for 240 f (Centaur's black zone, Yamato's dark room) | Time Stop freezes the hourglass gate, the chompers and the tide; Time Fist |
| **Y.SPEAR** | the single spear (vanilla; it passes class-3 shields, SC1) | the pierce (Should tap polish, systems §3.2); Wall Spear reaches high ledges on Blizzard 07, Flame 0D and Centaur 0D; the Pogo synergy crosses Yamato's caltrop hall without the rack |
| **KNIGHT.C, SILVER.T** | their arcs hit diving birds (Blizzard) and a patrolling Reap-bot from behind (Should) | - |

**Featured enemies** (`systems.md` §4.7): the PART drop is cut (R2.5), but the one-shot stays as an in-stage tell for
the champion's weakness: Blizzard's snow robot `$4D` to F.BLAST (vanilla), Flame's Fire Telly `$2C` to W.STORM,
Centaur's seahorse `$C4` to KNIGHT.C, Yamato's samurai `$A2` to SILVER.T.

**Frozen objects** (R2.2): every object table below has a **Freeze** column. **H** = a frozen handler (the enemy's
damage step is `$E9D7`/`$EA20`/`$EA6E`, so it keeps taking damage while frozen); **NF** = NOFREEZE (it ignores Time
Stop and the Ice Block but still takes hits); **boss** = a boss-side frozen state. The column becomes each kind's
`FRZ_KIND` (systems). Vanilla types follow tech's audit of their damage step.

### 0.6 Fiction, names and words

- **On-screen names** (R3.3): SUMMIT CLIMBER, PERSIAN PALACE, ATLANTIS RUINS, EDO NINJA ROW (meta's ≤ 20-character
  list). Homage games are named only in this doc's design notes, never on screen; plaques describe, they don't name
  (R3.3). The parody labels (TOPPY, NITPICKY, Jaja-nin, Nasubi Mage, Grim Reap-bot) are design labels; in-game text
  says "seals", "birds" and "ninjas". Capcom's own names (DuckTales, the Sakugarne) may be nodded to.
- **Words:** `story.md` owns every word (R4.1). This doc gives each hook a stable id and a trigger; the text lives in
  story §6.3, and the debrief hints in meta §4.4. Text tiers follow R4.5: the first-weakness line, the hooks that are
  the tell of a Must secret, the secret and plate lines, the tier B hints and **4 death lines per venue** are Must;
  flavour hooks are Should. **String counts** (R8.4): story §10.4's by-area table is the single source; this doc keeps
  no estimate of its own. These four venues' Must text is **50 strings and 0 labels** (Blizzard 13, Flame 11, Centaur
  14, Yamato 12).
- **Signs** (the summit sign, the Atlantis tablet, notice boards) are BG art with a symbol; their words appear in the
  2 × 28 pop-up (ALL CAPS, R1.4) when Rock presses UP at them.
- **The Mr. Y gag in every venue** (story §1.2 rule 4), always as cheap BG art (≤ 12 tiles, Must): the icebreaker's
  *MR. Y MARU* banner; Flame's sponsor tapestry with a familiar moustache on it (the vizier, Wily in an obviously fake
  costume, is Should: R3.4); the Atlantean mural of a bald man with a moustache, "THE Y-MAN SHALL COME"; the Edo
  WANTED poster, "MR. Y - 1,000,000 RYO". The Wily line is varied at every step (R3.9).
- **The match card** is meta's (vanilla's typed boss-intro panel); the commentators read its stats: SOLAR ENERGY,
  ABILITY UNKNOWN, MOBILE 31.
- The champions are good-natured rivals (BRIEF §2): they trash-talk, they don't hate you.

### 0.7 CASUAL and HARD

- **CASUAL** (R2.9): a `CFG_CASUAL` bit and CASUAL poke lists in tech's poke-list format (§5.5). Every venue section
  ends with the **standard lever list**: reflex windows ×2; mash counts −40 % (hold-to-struggle allowed); set-piece
  timers +50 %; +1 checkpoint per section; skill-gated secrets relaxed by one step. All of it is Must (data).
- **HARD** in v1.0 is the global ×1.5 damage, drops LESS, no refill (`systems.md`). The per-venue HARD poke lists and
  boss AI branches in this doc are **Should** (v1.1, cut-line item 3), written for tech's format.

### 0.8 Flashes and input

- **Flashes** (R3.5): in the default mode no effect flashes a large area more than 3 times per second, and REDUCED
  turns every flash into a fade.

  | Venue | Flash-like effects | Rule check |
  |---|---|---|
  | Blizzard | none; the AVALANCHE yodel is a 2-px shake (the SHAKE option) | pass |
  | Flame | the merge (one flash per merge); the pinch's red tint (held 40 f, not a flash); the vanilla oil palette cycle | the cycle's rate is measured at M5 and slowed if it changes a large area more than 3 times a second |
  | Centaur | TIME FLASH (one 4-f flash per move, at least 4 s apart, pinch included); C.FLASH's tap (systems) | pass |
  | Yamato | none (the hanabi are cut, R3.1) | pass |

- **Input** (R2.10): every UP interaction here (zone doors, the ZONE 100 door, scrolls, signs, the tablet) goes through
  systems' `IFINTERACT`: an UP press with B not held, and not within 10 f of an alt. In-stage, SELECT means only the quick swap and the
  last-weapon toggle.

### 0.9 Prizes and envelopes (R2.7)

- **Each hidden room holds one sponsor envelope** (30 bolts, once per save; `systems.md` §7). The round-1 bolt bags and
  the 100-bolt chest are gone (consistency-10).
- **Venue prize bolts:** at most 60 per venue, once per save, shown as tokens on replays (`systems.md` §7, §6.7). Only
  Blizzard has them: four bonus vegetables worth 60 in all. That is **4 prize bits** for Blizzard and none for the other
  three, so the venue prizes fit a 4-byte PRIZES field (meta owns the bytes; consistency-11).
- Each hidden room also holds one tank or 1-up and one large energy, never both a tank and a 1-up (safety nets don't
  stack, R2.6).
- **Secret weights** (exit 3, room 2, item 2, plate 1) and the **debrief order** are `systems.md` §6.2's and meta
  §4.3's. Each venue gives one **VENUE ACT** style act (systems §6.5) and a placeholder **par** (systems §6.3; measured
  from the golden movies).

### 0.10 What changed from PLAN §3.2 (round 1, still true)

| Venue | Kept from PLAN | Changed, and why |
|---|---|---|
| Blizzard | the vertical ascent; seal-bots pushing ice into holes; the condor secret exit; the skiing boss who makes snowballs | ice ceilings break to a **head-bonk** (Ice Climber's verb, no adaptor); the downhill autoscroll became a forced-slide floor and is now Should; the rocking ship, which PLAN dropped, is back (BRIEF §6) |
| Flame | plates and timed gates; loose floors; igniting oil; the mirror room's Shadow Rock; "don't fight your shadow" | the merge rule is "hold fire until the mirror glows, then touch it", not "walk in unequipped"; the oil gets a **player choice** (chandeliers); the duel is about **spacing**, not a shield (R3.1) |
| Centaur | numbered zones linked by doors, warps and fake doors; the tide; the galloping boss; C.FLASH's time stop | the secret exit is **ZONE 100 at low tide**; walls that crack under a Power punch are dropped; the tide gets a dwell and becomes the venue's spine, flooding shaft included (R3.1) |
| Yamato | rooftop ninjas; sliding-door secret passages; the Daruma Otoshi mini-boss; the helmet that flies off at half HP; the DuckTales pogo | the scrolls became a mechanic with a tell, and the secret exit is now a scroll (R3.1, R3.2); the pogo is an **in-stage set piece**; Knight's falling ceiling is Should |
| All | homage set pieces | PLAN reused each vanilla tileset; every venue now gets its own slot in tech's table, vanilla CHR kept and extended |

---

## 1. Blizzard Man: SUMMIT CLIMBER (stage `$00`): the v0.1 slice

### 1.0 The slice build sheet (M4)

Blizzard is the vertical slice (R0.2; RULINGS §6 M4; scope-4). This section is the **complete v1.0 spec**: every Must
item below can be built on the output of M0-M3 plus this venue's own data and code. The slice needs **no M5
stage-attribute work** (id `$00` keeps the ship's hard-wire, and its GP code reads the 48-byte stage record v0 from M2.1
with **no stage-`$00` stop-gaps**: R8.2), **no T3**, **no text v1b** (pop-ups and the debrief window are text v1a),
**no forms** (a new file owns the buster only; Power comes with the 2nd win, so the form swap, forms firing taps and
adaptors by win count wait for M5: R8.2) and **no other venue**. The path the slice proves: new game → bracket →
SUMMIT CLIMBER (exit, room, chip, Ice Block, boss) → judges → save, reload, replay.

**What the slice needs from other docs**, in milestone order (RULINGS §6):

| Need | Owner | Milestone |
|---|---|---|
| Vanilla stage id `$00`, chain 1 (the ship) through the raster list's `RL_SHIP` preset | tech | M2 |
| Level pipeline and canvas table; Blizzard's slot in the RAM-image tileset table; CHR set table v2; `chr.py`, `sprites.py`, `palettes.py`, `artcheck.py` | tech, art_audio | M2 |
| Families and sub-ids for the 7 Must Blizzard kinds (§1.9), with their `FRZ_KIND` (frozen or NOFREEZE) | tech | M2 |
| `map_set` and the repaint queue: the summit gate, the replay skip door, hanging icicles | tech | M2 |
| Stage record v0 (48 bytes, `SA_CUR`, the init hook): the slice's GP code reads `SECRET_SCR`, `PAR` and GP_BOSSHIT's row from it, as every later stage does (R8.2, tech §4.1) | tech | M2 (M2.1) |
| Text v1a (pop-up, debrief window), the commentator bus | tech, story | M2-M3 |
| Save, file-select-lite, bracket-lite, results, debrief (BL0-BL2), REMATCH, EXTRA CONFIG and the test mailbox | meta | M2 |
| T6 variant blocks with `t6_break` and `t6_refill`; the ceiling-probe callback (X-BONK) | tech | M3 |
| X-WRAP with a per-row opt-out | tech | M3 |
| The HUD widget module (the bonus meter) | tech | M3 |
| GP_BOSSHIT, WEAK! and SC9 (MELT), the frozen tick and frozen handlers | systems, tech | M3 |
| Scorecard, bolts, venue prizes and tokens, the sponsor envelope; the chip framework | systems | M3 |
| B.ATTACK's tap in Normal form and the **Ice Block** alt: alt dispatch's prototype (R2.4), in the dispatch table with Normal form's tap column (R8.2) | systems | M3 |
| The **attach state**'s core, with the condor as its first user, and a demo movie of the carry (R8.2; tech §7.9, M3.7) | tech | M3 |
| SNOW CHAINS's effect (`systems.md` §9.2) | systems | M4 |
| Blizzard's row of the stage record, from its `.lvl` header: `SECRET_SCR` (the secret-exit flag on a kill in 1A, tested by the post-kill hook at `$3F:$F9A0`), `PAR` and `FORT_COL` (GP_BOSSHIT's row). No stage-`$00` stop-gaps (R8.2; tech §4.1, §16.7) | tech | M4 |

**Build order inside M4** (each step leaves a playable build):

1. Layout 00-16 with checkpoints, palettes, the ship and its icicles.
2. The climb (09-0E): T6 cells, seals and their refills, birds, clouds, wrap, ladder stubs; the no-wrap floor and the
   Vegetable Cellar (1E).
3. The bonus summit (0F-11): the meter, vegetables, the condor and its passes, the summit gate, the replay skip door.
4. The secret route (17-19) with the condor carry, and the secret arena 1A.
5. The boss rework (16), its WEAK reaction and its pinch.
6. SNOW CHAINS: the seal ledger and the foreman.
7. Hooks, debrief predicates and hints, par, VENUE ACT.
8. The tests below, then the lag report and the ledger re-estimate (R0.1). The boss's flicker check with the Ice Block
   out decides FLAKES' Ice Block rule (§1.10, R8.6).

**Acceptance tests** (golden movies on NORMAL + EN; one smoke movie per other setting; RULINGS §6 testing policy):

| Test | Route | Must show |
|---|---|---|
| G1 | normal route 00 → 16, boss kill | results, bolts paid, autosave, the bracket marks the win |
| G2 | secret route: condor → 17 → 1A kill | secret-exit flag and SECRETS weight 3; the weapon is awarded (a secret-arena win is a full clear) |
| G3 | the no-wrap floor on 0D → 1E → back to 0D | room predicate set; the envelope pays 30 once; prize bits untouched |
| G4 | SNOW CHAINS: no seal destroyed (shoves allowed) | the foreman hands over the chip; a second movie destroys one seal: the sad foreman, no chip |
| G5 | REMATCH with B.ATTACK owned | the Ice Block encases a seal (FROZEN STEP) and a bird, stops the boss's snowball; vegetables appear as tokens; the skip door on 0F opens; pay = improvement only |
| G6 | save on the bracket, power cycle, reload | resume on the bracket; a second save mid-venue (death autosave) resumes on the bracket too |
| G7 | lag report on 04-07, 0A, 0D, 10, 11, 17 and the boss, with the Ice Block out | every screen within the 9-slot cap of §0.2, or the screen drops to 3 stage objects; the boss passes the flicker simulator, or FLAKES throws one flake fewer while the Ice Block is out (§1.10, R8.6) |

### 1.1 The pitch

*Frozen Island's mountain course.* You sail to the mountain on the vanilla icebreaker, then climb it the Ice Climber
way: floor by floor, **breaking the ice above your head with your helmet**, while seal-bots patch the holes you made
and birds dive at you. At the summit a 40-second **bonus round** pays out prize vegetables, and a **condor** flies
over: grab its feet and it carries you to the secret exit. Miss it and you take the back of the mountain down to
Blizzard Man's lodge.

| Ice Climber (design notes) | Here | Mark |
|---|---|---|
| Hammer the ice above, jump through the hole | **Head-bonk** breaks the ice cell above (ceiling probe + T6); two bonks make a hole wide enough | `[new-code M · Must]` |
| Topi pushes ice into holes | **The seal-bot** (TOPPY) pushes an ice cube into your hole 300 f after you make it | `[new-code S · Must]` `[new-art S]` |
| The screen wraps left and right | **X-WRAP** on every climb screen | `[new-code S · Must]` |
| Floors scroll up as you climb | jump-up exits (exit type 7). **v1.0:** a 2-rung ladder stub at the top of each climb screen | `[new-code M · Could]`; stubs `[engine-ok · Must]` |
| Nitpicker birds, icicles, drifting clouds | **Bird-bots** (NITPICKY), icicles, cloud platforms | `[new-code S · Must]` |
| The bonus stage: vegetables, a 40-s timer, the condor | **BONUS SUMMIT**: vegetables are prize bolts, the HUD meter is the timer, the condor is the secret exit | `[new-code S · Must]` |
| The polar bear in sunglasses who stomps when you dawdle | **Shirokuma**: a BG cameo (asleep) | `[new-art S · Could]` |

### 1.2 Map shape

```
00-03 harbour ──> 04-07 ICEBREAKER (rocking) ──> 08 shelf [CP1]
                                                   │ up
        1E hidden room <──(no-wrap floor)── 0D     │
                                            0E ◄── 09-0D CLIMB (5 floors per screen, wrap, ladder stubs) [CP2 at 0B]
                                            │ up
                                            0F summit approach ──(replays only: skip door)──┐
                                            │ up                                            │
                                            10-11 BONUS SUMMIT ──(condor)──> 17 flight ─> 18 cloud isle ─> 19 shutter ─> 1A SECRET ARENA
                                            │ meter ends: the wall opens                    │
                                            12-14 DESCENT (v1.1: SKI RUN) <─────────────────┘
                                            ─> 15 lodge [shutter CP] ─> 16 BOSS
```

Screens used: main 00-16 (23), secret route 17-1A (4), hidden room 1E (1) = **28 of 32**. Spare: 1B-1D, 1F.

### 1.3 Screen by screen

Brackets give the peak **stage objects** (§0.2: ≤ 4, so player + script + 3 shots + objects ≤ 9). CHR and palettes are
named by vanilla id where kept. Hook ids are story §6.3's (§1.13 gives their tiers).

| Scr | What the player does | Stage objects [peak] | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Base camp. Match card. Walk right over snow ledges; a short **slippery ice strip** (type 5) leads to a 1-up on its far end, so the slide is felt with nothing at stake | snow robot `$4D` (+ its snowball), 1-up [3] | vanilla ice momentum (24-36 px slide) | vanilla v00 art (girders, skyline), CHR `$82`, palette `$15`. BLZ-01, BLZ-02 |
| **01** | The pier: an ice floor over freezing water with a 32-px hole. **The first seal is friendly**: it pushes an ice cube into the hole and you walk over it | seal (the cube is drawn in its push frames), propeller drone `$24`+`$26` (body and rotor) + its ball [4] | water under the pier = pit | teaches that seals *fill* holes, before the climb makes that a problem |
| **02** | Count-bomb hop over open water (vanilla v03's idea) | count bombs `$19` ×3 [3] | the "3" pods explode once passed | count bombs never share a screen with seals (art_audio §4.1: same tile range) |
| **03** | The gangway. The **MR. Y MARU** banner (BG; the Mr. Y gag). Exit right boards the ship | wall pod `$21` (the sideways count bomb) [1] | | the exit loads the ship set `$85`, palette `$1A`, and starts effect thread 3 (vanilla script 05). BLZ-04 |
| **04** | **THE ICEBREAKER**, bow. The deck rocks (vanilla chain 1, 51 px). **Twist: the rocking shakes icicles loose.** Hanging icicles are BG cells. At each top turn of the rock (the vanilla thump, sound `$41`), up to two of them shake for 30 f (a tile swap), then drop: the cell is cleared by `map_set` and a falling icicle spawns | falling icicles ≤ 2 [2] | rocking deck; icicles (2 dmg) | needs the ship thread's turn event (a registry hook). Vanilla v0E-v0F art. BLZ-03 |
| **05** | Superstructure: climb the pink deckhouse (platforms) | cannon rider `$20`+`$1F` (2) + its shot, falling icicle ≤ 1 [4] | icicles drop at **both** turns here | |
| **06** | Ice floes: the bow breaks a floe field; two **floe platforms** (sprites) bob with the hull. Jump floe to floe to the stern | floes ×2, falling icicle ≤ 1 [3] | falling between floes = sea pit | the floes are the cloud-platform object with ice art |
| **07** | Stern. An E-tank on the aft deck (vanilla v12 had one); a Power-block crate holding a 1-up (revisit) | E-tank, 1-up [2] | | exit right: CHR `$82` + the climb third, palette `$1C`; ship thread off (vanilla screen-13 script) |
| **08** | **CHECKPOINT 1** at the foot of the mountain. A wooden sign: an up arrow and a helmet (UP reads it) | none [0] | | the climb starts at the ladder stub, top right |
| **09** | **Climb 1** (5 floors, 48 px apart: Rockman's jump rises 52 px, measured, so 4 px of clearance). Floor 1 already has a hole; floor 2 has a single breakable cell: **bonk it**. Floors 3-5 mix breakable blue ice and unbreakable brown rock. The top floor's ladder stub leads up | seal ×1, debris [2] | first wrap: floor 4's only gap is across the screen edge | ceiling probe, T6, X-WRAP. BLZ-05 |
| **0A** | **Climb 2**: two seals patch holes 300 f after you make them, so you have to commit to a column | seals ×2, bird ×1, debris [4] | the bird dives (tell: hover 20 f + screech) | the first seal you **hit** triggers BLZ-07 (the SNOW CHAINS tell), before any can be destroyed |
| **0B** | **Climb 3**: a wide gap on floor 3 is crossed on two drifting clouds. **CHECKPOINT 2** on arrival at the camp ledge of floor 1 | clouds ×2, seal ×1, debris [4] | falling from floor 1 is a pit; higher floors fall onto lower floors (safe) | |
| **0C** | **Climb 4**: slippery floors (type 5): bonking while sliding carries you past the hole. A row of icicles hangs under floor 5 (BG). An F.BLAST `$D` ice pocket holds a large weapon energy | seal ×1, falling icicle ≤ 1, debris, the pocket's energy [4] | slippery floors + bonk = the venue's skill test | |
| **0D** | **Climb 5**: the **no-wrap floor** (floor 3, §1.6.2) | seals ×2 (one walks floor 3), bird ×1, debris [4] | | the hidden room's tell |
| **0E** | **Climb 6**: the icicle chimney. A cave on floor 2 (Could: a polar bear in sunglasses asleep in it, BG art) | falling icicles ≤ 2, bird ×1, debris [4] | | BLZ-08 (Could) |
| **0F** | Summit approach: one flat floor, a red flag, a sign with an up arrow; the ladder up. **The replay skip door** (R3.8): once the venue is cleared, the lodge door in the right wall is open (a `map_set` at screen init) and drops you to 12 | none [0] | | taking the door skips the bonus: no condor, so no secret exit that run, and no vegetables (they are tokens on replays anyway) |
| **10** | **BONUS SUMMIT 1**: the **meter starts at 40 s** (the HUD widget in the boss-bar slot). A vertical bonus climb with no enemies and no damage: drifting clouds and ledges with **prize vegetables** (eggplant 10, carrot 10) | clouds ×2, vegetables ×2 [4] | no pits: falling only costs time | the bonus jingle G25 is Should; v1.0 keeps the stage theme `$01` |
| **11** | **BONUS SUMMIT 2**: the peak, with a cabbage (15) on a side ledge and the **corn (25)** on the high ledge right under the condor's first pass: grab the corn or the condor first? The **condor** starts its passes when you arrive: it crosses the top of the screen at 1.5 px/f, feet about 40 px above the peak ledge, and circles back off-screen, one pass every 6 s until the meter ends. **Jump and touch its feet** to grab it → 17. When the meter ends, the condor leaves and the peak's right wall opens (`map_set`) onto 12 | condor, vegetables ×2 [3] | | §1.6.1 |
| **12** | **The descent** (v1.0): the back of the mountain as plain downhill snow steps (vanilla `$82` tiles), moguls and a crevasse. *v1.1 (Should): SKI RUN 1, ski snow forces 2.5 px/f to the right* | snow robot ×1 (+ snowball), count bomb ×1 [3] | crevasse = pit | |
| **13** | Descent 2: two crevasses. *v1.1: SKI RUN 2, with a snowball rolling in from behind (faster than you: jump it)* | propeller drone (body, rotor) + its ball [3] (v1.1: the rolling snowball replaces the ball's slot [3]) | | BLZ-09 (Should) |
| **14** | Descent 3: the lodge fence | bird ×1 [1] | | |
| **15** | Blizzard Man's **ski lodge**: shutter corridor. **Boss checkpoint.** The **seal foreman** waits here (SNOW CHAINS) | foreman, chip capsule [2] | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room**: the lodge's sun deck (§1.10) | Blizzard Man [boss + ≤ 3] | | vanilla boss-room art (snowy mountain backdrop) kept |
| **17** | **Condor flight** (secret route): Rock hangs from the condor's feet (the attach state), which flies right at 2 px/f while the camera follows. Birds attack; the buster still fires. A lets go (onto the cloud below) | condor, birds ×2, cloud ×1 [4] | letting go over a gap = pit | BLZ-11 |
| **18** | **Cloud isle**: the condor drops you on a cloud bank above the summit; short platforming over drifting clouds to a snow hut. An F.BLAST `$D` ice pocket in the hut holds a 1-up | clouds ×2, seal ×1, the pocket's 1-up [4] | pits | |
| **19** | Secret shutter corridor (checkpoint); the seal foreman again | foreman, chip capsule [2] | | shutter checkpoint (`$0684` = 19) |
| **1A** | **SECRET ARENA** (§1.11) | Blizzard Man | | a kill here sets the secret-exit flag |
| **1E** | **Hidden room: the Vegetable Cellar** (§1.6.2) | envelope, E-tank, large weapon energy [3] | | |

### 1.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 08 | camera on 08 | `$82` + the climb third / a `$1C`-based program |
| CP2 | 0B | camera on 0B | same |
| *(CASUAL)* | 05 | camera on 05 (mid-ship: restarts the ship thread) | `$82` + `$85` / `$1A` |
| *(CASUAL)* | 0D | camera on 0D (the upper climb) | as CP2 |
| *(CASUAL)* | 12 | camera on 12 (the descent) | `$82` / the summit program |
| Shutter | 15 (main), 19 (secret) | shutter entry (vanilla `$3F:$FA20`) | |

T6 cells behave like vanilla breakables (tech §10): they **survive deaths** and reset at the next stage start, so a
hole you made before dying is still there, and so is any hole a seal patched.

### 1.5 The climb's rules

- **Floors:** 5 per screen, 48 px apart; breakable cells are T6 DESTRUCT quadrants of the ice-floor blocks (each such
  block costs its variants in block ids; the build reports the total against Blizzard's 256, art_audio §4).
- **Bonk:** when Rock's head stops against a breakable cell while rising, the ceiling-probe callback calls `t6_break`
  on it (debris, repaint, collision on the next probe). Two adjacent cells make a 32-px hole Rock fits through; whether
  a single 16-px cell is enough is tuned at M4 against his hit box.
- **Refill:** a seal walking a floor with an open hole fetches a cube 300 f after the hole opened and pushes it in
  (`t6_refill`). A seal never refills a cell Rock is standing under (no crush deaths).
- **Wrap:** in each locked climb screen, X < `$08` becomes `$F0` and back, for Rock, seals, birds and clouds; one
  floor of 0D opts out (§1.6.2).
- **Up:** v1.0 climbs leave each screen by a 2-rung ladder stub at the top floor (vanilla can't enter a screen from
  below without a ladder). Could: exit type 7 lets a jump through the top floor's hole carry Rock up.

### 1.6 Secrets

#### 1.6.1 Secret exit: catch the condor `[new-code S · Must]` `[new-art M]`

- **Gate:** reach 11 with time left on the 40-s meter and touch the condor's feet from below. Each pass is a 6-s loop,
  so a player who reaches the peak with 12 s left gets two tries.
- **Tell:** the condor itself (big, slow, low enough that a well-timed jump from the peak ledge reaches its feet); the
  sign on 0F; BLZ-10 the first time it appears in a save (Must: the tell).
- **Fail state:** none. When the meter ends the wall to 12 opens and the stage goes on (Ice Climber's bonus does the
  same).
- **The carry** (consistency-43, art_audio §2.4): the attach state locks Rock to the condor's feet; the weapon switches
  to the buster on the grab and only the buster fires; Rock uses **vanilla's ladder-climb and ladder-shoot poses**, so
  the carry costs no player tiles and no set-piece sheet; A lets go.
- **Effect:** grab → 17 → 18 → 19 → the secret arena 1A. Beating Blizzard Man in 1A clears the venue **and** sets its
  secret-exit flag (SECRETS bit 0, meta). The weapon is awarded as on the main route.
- **VENUE ACT** (systems §6.5): **CONDOR, FIRST PASS**: the grab happens on the condor's first pass.

#### 1.6.2 Hidden room: the Vegetable Cellar (1E) `[new-code S · Must]`

- **Gate:** on 0D, **floor 3 does not wrap**. Walk off its left edge and X-WRAP's per-row opt-out runs a left exit
  instead (type 6 with the explicit target `$1F`, which lands on 1E): a one-screen ice cave.
- **Tell:** the seal that patrols floor 3 walks off the left edge and **does not come back** on the right (every other
  seal in the climb visibly wraps). Floor 3's left wall has a darker, cracked doorframe in the ice.
- **Contents:** a frozen **giant eggplant** statue (BG; Ice Climber's bonus vegetable), the **sponsor envelope** (30
  bolts), an E-tank and a large weapon energy.
- **Return:** walk right off 1E (type 5, target `$0C`, so it lands on 0D) back onto floor 3.

#### 1.6.3 Behaviour-gated chip: SNOW CHAINS `[new-code S · Must]`

- **Gate:** **never destroy a seal** anywhere in the venue (9 in all, 8 on the main route). A buster tap or a half
  charge only shoves a seal 16 px and stuns it for 60 f; **a hit of 3 or more destroys it** (the full charge, PUNCH★,
  F.BLAST, KNIGHT.C, SILVER.T). The Ice Block (1 damage + freeze) never destroys one. Shoving is allowed; destroying one
  voids the chip for this visit.
- **Why it is a trade-off** (4MI lesson 3): seals patch the holes you need, so sparing them costs time (the scorecard's
  TIME) and patience. The tidy solution, the full charge, is exactly what voids the chip.
- **Tell:** BLZ-07 on the first seal you hit, even with a harmless shove (Must: the tell), every visit. A spared seal
  bows as you pass it on a higher floor. The debrief hint (§1.14).
- **Award:** the **seal foreman** waits in the shutter corridor (15 on the main route, 19 on the secret route) and
  hands over the chip capsule if no seal was destroyed; otherwise he shows a sad-seal pose (BLZ-15, Should).
- **Effect:** `systems.md` §9.2, SNOW CHAINS (ice floors grip like normal floor; falling icicles bounce off the helmet).

### 1.7 The Ice Block here: the alt prototype (R2.4)

`systems.md` §3.4 owns B.ATTACK and its Ice Block (UP+B, cost 2, a 32×16 block that encases a normal enemy for 150 f or
lands as a slippery block for 240 f). The slice ships it as the **prototype of alt dispatch and of the frozen tick**,
exercised on a REMATCH of this venue after the first win. Blizzard's own objects give it one test case per rule:

| Target | Result | What it proves |
|---|---|---|
| a seal | encased for 150 f: a solid ice platform (class 9) that **doesn't refill** while frozen; it takes 1, so it is never destroyed (SNOW CHAINS-safe) | the frozen handler on a GP family enemy; the FROZEN STEP style act |
| a bird (now 2 HP, so the block's 1 doesn't kill it) | encased in mid-air for 150 f: a floating step | the class swap in the air |
| the snow robot `$4D` | encased (its damage step is vanilla `$E9D7`) | a frozen handler on a vanilla type |
| a falling icicle | NOFREEZE: it takes 1 and shatters | the NOFREEZE path |
| condor, clouds, floes | NOFREEZE and invulnerable: no effect | |
| the floor | a slippery block for 240 f: a step up to the next climb floor without bonking, and a wall a seal can't push past | the block object in a utility slot (4-7, R1.11) |
| Blizzard Man | a block in the SNOWBALL's path stops the ball: it bounces back and the block shatters. A block lobbed straight at him does 1 and doesn't freeze him | the boss-side rule |

The boss shows the idea first (§1.10, FLAKES leaves an ice block that stops his own snowball), so the player has
already seen the alternate work before owning it. Alt input follows R2.10 (UP+B never also opens a door or reads a
sign).

### 1.8 Tileset and art (art_audio §4.1 owns the counts)

- **Kept vanilla CHR:** `$82` (ice blocks, snow ledges, girder scaffolds, skyline, ladders), `$85` (the ship: hull,
  deckhouse, portholes, sea), `$84` (cave tiles for 1E). Palettes `$15`, `$1A`, `$1C` as starting points.
- **New BG** `[new-art M · Must]`: the climb third (ice cells intact and gone, as T6 variants; rock floors; grassy
  ledge ends; clouds; ladder stubs; hanging and shaking icicle cells; sign boards) and the summit third (peak and flag;
  lodge logs, window and sun deck; the MR. Y MARU banner; the giant eggplant statue). Should: ski fence and moguls.
  Could: the sleeping polar bear.
- **New sprites** `[new-art M · Must]`, from vanilla recolours and composites first (R5.1; art_audio picks the bases):
  seal (walk ×2, push with cube, stun, bow, sad: 6 frames), falling icicle, bird (fly ×2, dive), condor (32×24,
  2 frames), 4 vegetables, cloud/floe platform, the seal foreman (2). Blizzard Man's pinch set: skis-off and the slush
  puddle (MELT). Should: the rolling snowball, the snowman.
- **Changes for art_audio's re-run** (R5.3): hanging icicles move from SET-BZ1 to BG cells (only the falling frame stays
  a sprite); the condor carry reuses vanilla's ladder poses (drop art §7.1's 2 condor-carry tiles); the snowman and the
  rolling snowball become Should; Shirokuma becomes a BG cameo (Could).
- **Collision:** group 0 (identity) plus the T6 ice cell. Should: the ski-snow type (`GRP_ROW`).

### 1.9 Enemies and objects

| Object | Kind | HP (buster taps) | Behaviour | Freeze | Mark |
|---|---|---|---|---|---|
| Snow robot `$4D` | vanilla | 5 | lobs snowballs; F.BLAST one-shot (vanilla `$EB56`; the featured-enemy tell) | H | `[engine-ok]` |
| Count bomb `$19`/`$21` | vanilla | - | floating platform that explodes once passed | NF | `[engine-ok]` |
| Propeller drone `$24` + rotor `$26` (2 slots; drops `$55` balls), cannon rider `$20` + deck cannon `$1F` (2 slots; fires `$14`) | vanilla | 2 + 3 / 5 | as vanilla | per tech's audit | `[engine-ok]` |
| **Seal-bot** (TOPPY) | new | taps and half charges shove; a hit of 3+ destroys | walks its floor at 0.75 px/f and wraps; refills holes (§1.5); contact 2 | H | `[new-code S · Must]` |
| **Bird-bot** (NITPICKY) | new | 2 | sine flight across the screen; hovers 20 f above Rockman (screech), then dives at 3 px/f; contact 3 | H | `[new-code S · Must]` |
| **Icicle** | new | 1 (falling) | BG while hanging; shakes 30 f (tile swap), then a falling object at 4 px/f; 2 dmg; shatters on landing. On the ship the rock turns trigger it | NF | `[new-code S · Must]` |
| **Cloud / floe platform** | new (shared with Centaur) | - | solid sprite platform 48×8, drifts 0.5-1 px/f, wraps on wrap screens, bobs with the ship on 06 | NF | `[new-code S · Must]` |
| **Condor** | new | - | passes over 11 every 6 s while the meter runs; the attach-state carry; flies right at 2 px/f on 17 | NF | `[new-code S · Must]` |
| **Vegetables** | new | - | prize pickups, once per save (4 prize bits); tokens on replays | - | `[new-code S · Must]` |
| **Seal foreman** | new | - | NPC: hands over SNOW CHAINS, or the sad pose | NF | `[new-code S · Must]` |
| **Rolling snowball** | new | 3 | rolls downhill at 3 px/f on the ski run | H | `[new-code S · Should]` |
| **Shirokuma** | new | - | BG cameo, asleep; on HARD (v1.1) an enforcer | - | `[new-art S · Could]` |

### 1.10 Boss: Blizzard Man, "the lodge sun deck" (16)

**Arena:** one screen; a slippery snow floor (type 5) with two short ice shelves at the sides (32 px up). Mountain
backdrop (vanilla). Boss-side objects ≤ 3 at any time (§0.2: the WEAK! pop only takes a free slot).

**Intro (90 f):** he skis in from the right over a mogul, stops in a spray, and holds up a tiny **solar panel** to the
sky. A cloud covers the sun. He sighs. (The vanilla data panel says SOLAR ENERGY; this is the joke.)

**Pattern loop (HP 28 to 10):** SLALOM → FLAKES → SLALOM → SNOWBALL, about 600 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **SLALOM** | crouch, poles planted, 20 f | skis across at 3 px/f (16 px tall), turns at the wall (16 f), skis back | 20 + 75 + 16 + 75 | jump over; contact 4 |
| **FLAKES** (vanilla move) | arms up, 24 f | throws **3** flakes in a spread (they fall at 1 / 1.75 / 2.5 px/f); **the second to land becomes an ice block** (32×16, solid, slippery top, 240 f): **the Ice Block, shown**. At most one block; while it stands, FLAKES throws 2. If the M4 flicker simulator fails the 3-flake case with the player's **Ice Block** out (refights), FLAKES also throws 2 while an Ice Block exists (R8.6) | 24 + 60 + 30 recovery | stand on the block; flakes 2 dmg |
| **SNOWBALL** (vanilla move) | hunches "Hup!", 12 f | rolls as a 24-px snowball (the boss object itself) at 2.5 px/f, bounces off each wall once, **grows 4 px per crossing** (24 → 32). **An ice block stops it**: the ball shatters the block and bounces back. The player's Ice Block does the same on refights | 12 + ~200 + 20 uncurl | jump it, or hide behind an ice block |

**Pinch (HP ≤ 9): AVALANCHE.** On entering pinch and then every second loop he plants his poles and **yodels** (60 f
with a 2-px screen shake: the tell; the SHAKE option applies). The yodel shatters any ice block. Then 16-px snowballs
drop from the top: two at x = 40 and 216, and one at x = 128 24 f later, each rolling toward the nearer wall at
2 px/f (at most 2 alive at once). SLALOM speeds up to 4 px/f, and SNOWBALL splits into two small balls on its second
bounce.

**Damage and i-frames:** `systems.md` Tables 1-2 (Blizzard's column: F.BLAST 4 W with 16 f; KNIGHT.C 3 G; W.STORM 1 R;
B.ATTACK his own).

**WEAK reaction, MELT** (SC9, Must): F.BLAST turns him into a **slush puddle** for 40 f (no contact damage, WEAK! pop,
BLZ-12), and for the rest of the current move he skis at 2 px/f.

**Own-weapon reaction, SNOWMAN** (SC4, Should): the first B.ATTACK hit does 0: he catches the flakes ("Thank you!")
and builds a **snowman** (16×32, 3 hits) in 30 f. The snowman blocks your shots; if his SNOWBALL rolls through it, the
ball jumps to full size. Once per fight; while the snowman stands, FLAKES throws 2. In v1.0 the first B.ATTACK hit is a
plain own-weapon cell.

**Forms** (refights): a charged Power punch on the rolling SNOWBALL cracks it: he tumbles out stunned for 30 f (free
hits). Jet hovers over the avalanche (one snowball still reaches hover height: 32 px). These reactions arrive with the
forms at M5 (R8.2); the slice's fight has none.

**How it teaches B.ATTACK:** FLAKES is the tap; the ice block it leaves is the alternate, and it *works* (it stops the
snowball), so the player has used the alternate's idea before owning it.

**Fight loader** (W2): the arena needs no effect init; the pinch threshold comes from the per-fight byte. **Flicker:**
vanilla's Blizzard fight already shows 9 sprites on a line in 56 % of frames (art_audio §1.6); the 3-flake FLAKES and
the staggered avalanche keep GP's additions off the snowball's lines, and artcheck verifies it. At M4 the simulator
also runs FLAKES with the player's Ice Block out (art_audio §3.5); if that case fails, the one-flake-fewer rule in the
FLAKES row is switched on (R8.6).

**Credits mode** (the v1.0 credits, fortress §6.2; `IFCREDITS`, tech §4.6): with no Rockman he loops SLALOM → FLAKES →
SLALOM → SNOWBALL in room 16, and any move that would read Rock's position aims at a fixed mark instead (the floor at
x = 128). FLAKES still leaves its ice block, so the show includes the block stopping his own snowball. Nothing hits him,
so there is no pinch and no reaction; the commentator bus is already silent. Fallback: his card strip only.

### 1.11 Secret arena (1A)

- **v1.0 (Must):** the sun-deck arena again (same layout), above the clouds at sunset (a new palette program). Same
  fight, same pinch. The kill sets the secret-exit flag.
- **v1.1 (Should): CLOUD SUMMIT** `[new-code S · Should]`. The mountain's true peak, with one twist: **the floor is
  breakable ice cells** (T6). His SNOWBALL breaks the cells it rolls over on its second crossing (32-px holes) and his
  FLAKES break the cell each one lands on. A hole is a pit. **Two seals** patrol the floor and refill holes every 240 f;
  **if no seal was destroyed this visit, they refill twice as fast** ("the seal union stands with you"). The condor
  circles every 600 f and drops a vegetable that heals 4 HP. Boss-side objects: snowball or flakes, 2 seals, the
  condor: the condor waits off-screen while FLAKES is out.

### 1.12 CASUAL levers (Must) and HARD pokes (Should)

**CASUAL** (R2.9; `systems.md` §13.4's lever table, applied through tech's poke lists and the CASUAL layout tier):

| Lever | Where (screen, object) | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | the bird's dive tell (0A-0E, 14, 17) | 20 f | 40 f | `REFLEX` |
| reflex | the icicles' shake (04-06, 0C, 0E) | 30 f | 60 f | `REFLEX` |
| reflex | Blizzard Man's FLAKES tell; his yodel (16, 1A) | 24 f; 60 f | 48 f; 120 f | `REFLEX` |
| mash | none | - | - | - |
| timer | the bonus meter (10-11) | 40 s | 60 s | `TIERVAL` |
| timer | the seals' refill delay (09-0E) | 300 f | 450 f | `TIERVAL` |
| checkpoint | ship, upper climb, descent | CP1 08, CP2 0B | + 05, 0D, 12 | dormant checkpoint objects woken by a CASUAL poke |
| secret step | the condor (11) | its feet's hit box as drawn | +8 px | `IFCASUAL` |
| secret step | SNOW CHAINS (every seal) | a 3+ hit destroys a seal | the first 3+ hit only stuns it; the second destroys it | `IFCASUAL` in the seal's damage step |

**HARD** (Should, v1.1; R2.9):

| Section | Poke | Kind |
|---|---|---|
| Ship 04-07 | icicles drop at **every** turn (NORMAL: top turns only, except 05) | object param |
| Ship 06 | one floe removed (two jumps become one long jump) | object list |
| Climb 09-0E | seal refill delay 300 → 150 f; one more seal on 0B (with the cloud count cut to 1) | object param + list |
| Bonus 10-11 | meter 40 → 30 s; the condor makes one pass | param |
| Descent 13 | one more crevasse | layout poke (3 blocks) |
| Boss | pinch at HP ≤ 14; SNOWBALL grows 8 px per crossing; the avalanche's third ball drops 12 f after the first two | AI branch |
| Climb (Could) | Shirokuma is awake: stand on one floor for 10 s anywhere in 09-0E and he stomps in: every open hole on the screen refills and all icicles fall | AI branch |

### 1.13 Commentator hooks (ids; the words are story §6.3's)

| Id | Trigger | Tier (R4.5) |
|---|---|---|
| BLZ-01 | match card ends | Should |
| BLZ-02 | first slide on ice (00) | Should |
| BLZ-03 | first icicle drops on the ship | Should |
| BLZ-04 | the MR. Y MARU banner on screen | Should; reworded so the Wily line is not "It's definitely Wily" again (R3.9, design-23) |
| BLZ-05 | first bonk breaks a cell | Should |
| BLZ-06 | first seal refill | Should |
| BLZ-07 | first seal hit (shoved or destroyed), every visit | **Must** (the SNOW CHAINS tell) |
| BLZ-08 | the polar bear on screen | Could |
| BLZ-09 | the descent starts (the ski run in v1.1) | Should |
| BLZ-10 | the condor first appears, once per save | **Must** (the exit tell) |
| BLZ-11 | the condor grabbed | Should |
| BLZ-12 | first F.BLAST hit on Blizzard Man (`EV_WEAK_FIRST`) | **Must** |
| BLZ-13 | the snowman built | Should (with SC4) |
| BLZ-14 | pinch (the yodel) | Should |
| BLZ-15 | first seal destroyed; the foreman's sad pose | Should |

**Death lines** (Must: 4 per venue, R4.5): story's lines 1, 2, 3 and 5 are recommended. Line 4 ("The mountain always
wins the first round") repeats Plant's line 4 almost word for word; line 6 names the Ice Climbers' characters and breaks
R3.3, so it goes.

### 1.14 Judges' debrief hints (tier B; meta §4.4 holds them, story owns the words)

In meta's weight order (exit, room, item). Unchanged from round 1; set in capitals at build time:

1. BL0, exit: "The summit condor only carries climbers who reach it with time on the clock. Jump for its feet."
2. BL1, room: "On the mountain, one floor doesn't wrap around. Watch where the seals walk."
3. BL2, SNOW CHAINS: "The seals are only doing their job. A climber who never breaks one earns a set of chains."

### 1.15 How crazy it gets (screenshot moments)

1. Blizzard Man holds up a solar panel in a snowstorm, and a cloud covers the sun.
2. The MR. Y MARU icebreaker rocks so hard the icicles fall off the rigging.
3. Rockman breaks the ice with his **head**, floor after floor, while a seal patiently fills the holes back in.
4. A 40-second **bonus round** in a Rockman game, paying out vegetables.
5. Rockman hangs from a condor's feet over a sea of clouds.
6. Rockman freezes a seal in an ice block and stands on it (the Ice Block, on a replay).
7. *(v1.1)* Blizzard Man builds a snowman in the middle of a boss fight.
8. *(v1.1)* The secret arena's floor breaks under you, and the seals you spared rush in to patch it.
9. *(Could)* A polar bear in sunglasses naps in a cave on the way up.

### 1.16 Revisits, VARIETY and records

- **Taps (v1.0):** F.BLAST melts the `$D` ice walls on 0C and 18 (two pockets: a large weapon energy and a 1-up), as
  vanilla's E-tank at v09 did. KNIGHT.C and SILVER.T arcs reach diving birds from below.
- **Ice Block (v1.0, from the slice):** encased seals and birds become steps (§1.7); a block on a climb floor is a step
  to the next floor without bonking.
- **Alts (v1.1, Should):** Y.SPEAR's Wall Spear reaches a high ledge over the stern (07: a large weapon energy, not
  bolts, so the prize cap stays at 60: consistency-10; round 1 put it on 05, which is full); F.BLAST's Flare melts the cell above you, a faster climb for Time Attack.
- **Tag partner (Should, cut-line item 2, with the tag partner):** Break Man's shield blocks the icicle rain on the
  ship if he jumps through it; the optional shortcut is a stern-deck ledge only his double knockback reaches.
- **Par** (placeholder, systems §6.3): 330 s, the 40-s bonus included; measured from G1 at M4. A run that takes the
  replay skip door has the bonus's 2,400 f (40 s) added to its `T` when it takes the door, so the par stays 330 s and
  the skip neither buys nor costs TIME (systems §6.3).
- **Mini-record** (Could, meta's `VENUE_REC`): the meter's time left at the condor grab.

---

## 2. Flame Man: PERSIAN PALACE (stage `$03`)

### 2.1 The pitch

A palace built, unwisely, on Flame Man's oil field. You cross the vanilla oil field at dusk, drop into the palace
dungeon and play it like the 1989 game: pressure plates and portcullises, loose floor tiles, spikes that spring up,
and guards who parry anything you shoot at them point-blank. In the gallery **you can drop a chandelier into an oil
pool to burn the guard standing in it**, but vanilla oil burns forever (per metatile id, through deaths), so that pool
is gone for the rest of your visit. In the mirror room **your shadow steps out of the glass**: fight it and the stage
goes on; **don't**, wait for the mirror to glow, walk into your shadow, and you merge and the mirror opens the secret
route. Then down into the burning fire vault (vanilla's red cave), past a mousehole, to a spacing duel with Flame Man.

**Cultural fixes (R3.4, Must; design-12).** No "Oil Sultanate" anywhere: the joke is the oil field, not a culture.
The rooftops (18) are domes under a **full moon**: no minarets, no crescent. The vizier exists only as an obvious
Wily-in-costume gag (Should). The venue's jokes aim at *Prince of Persia*'s mechanics: loose floors, the shadow, the
mouse, the 60-minute clock.

| Prince of Persia (design notes) | Here | Mark |
|---|---|---|
| Raise and drop plates, portcullises; the gate that closes as you roll under it | **T3 plates and gates**, a timed gate you slide under | `[new-code M · Must]` (T3) |
| Loose floor tiles that shake, fall, crush guards and land on plates | the **loose tile** (a T6 cell until it falls) | `[new-code S · Must]` |
| Spikes that spring up as you pass | **spike traps**: bait them, then cross while they re-arm | `[new-code S · Must]` |
| Guards who block your sword when you stand too close | **palace guard-bots parry point-blank shots** (the 48-px spacing rule Flame Man also uses; R3.1: Knight alone owns the shield) | `[new-code S · Must]` |
| The mirror and the shadow; merging by sheathing the sword | **Shadow Rock** (T7): peace = merge = secret exit | `[new-code M · Must]` |
| The princess's mouse presses the plate | **the mouse-bot** opens the hidden room | `[new-code S · Must]` (R2.5, scope-3) |
| The 60-minute clock | **the hourglass gate** in the fire vault | data on T3 · Must |
| Chompers (slicers) | **chomper doors** | `[new-code S · Should]` (v1.0: a spike hall) |
| The skeleton that reassembles | **skeleton-bot** | `[new-code S · Should]` (v1.0: a guard) |
| The vizier | **Wily in an obviously fake vizier costume** on the balcony | `[new-art S · Should]` (v1.0: a sponsor tapestry) |

### 2.2 Map shape

```
00-03 oil field (vanilla) ─> 04 drop ─> 05-08 DUNGEON (plates, loose floors, spikes, guard, timed gate)
   ─> 09 [CP1] ─> 0A spike hall (v1.1: chompers) ─> 0B OIL GALLERY ─> 0C balcony ─> 0D ledge guard (v1.1: skeleton) ─> 0E MIRROR ROOM
                                                                                │ fight the shadow: the mirror stays a wall
                                                                                │ merge: the mirror opens ─> 17 mirror passage ─> 18 rooftops ─> 19 shutter ─> 1A SECRET ARENA
                                                                               0F down
   10 FIRE VAULT [CP2] ─> 11 hourglass gate ─> 12 mouse alcove ──(the mouse)──> 1C hidden room
                                              └─> 13 loose bridge ─> 14 antechamber ─> 15 shutter ─> 16 BOSS
```

Screens used: main 00-16 (23), secret 17-1A (4), hidden room 1C (1) = **28 of 32**. Spare: 1B, 1D-1F.

### 2.3 Screen by screen

Brackets: peak stage objects (≤ 4, §0.2). The dungeon has no Metalls and no Tellies in trap rooms (art_audio §4.4:
their tiles clash with the guards' and the traps').

| Scr | What the player does | Stage objects [peak] | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Match card. The oil field at dusk: purple dunes, arches, pipes, **oil pools** (types 6/9: 0.5 px/f walk, lower jump). Walk to the palace on the horizon | Metall `$18` ×1 (+ bullets ≤ 2) [3] | oil slows you | vanilla v00 art, CHR `$86`, palette `$1E`, the oil cycle (thread 4). FLM-01 |
| **01** | **The ignition lesson.** A Fire Telly hovers **120 f** over a small isolated oil pool before it drops. Shoot it and nothing happens; let it drop and the pool ignites, permanently | Fire Telly `$2C` ×2 + drops ≤ 2 [4] | burning oil = deadly (type F) | FLM-02 (Must: FIREPROOF's tell) |
| **02** | Pipeline. A wheel cannon; the vanilla **1-up inside a Power block** (v02) | wheel cannon `$C0` (+ shots ≤ 2), 1-up (revisit) [4] | | `[engine-ok]` revisit pocket |
| **03** | **The palace gate.** A portcullis with a raise plate in front of it: step on the plate and the gate rises (60 f) and stays up for 300 f. Teaches plates | gate [1] | | T3. The exit right loads the palace thirds and the dungeon palette. FLM-03 |
| **04** | Inside the gate the floor ends: **drop into the dungeon** (PoP starts in the dungeon). Torches | none [0] | | down exit; the torch palette cycle (a bank-`$3B` cycler, data) |
| **05** | **Loose-floor puzzle.** The right gate is shut; its plate is on the lower floor, under a loose tile of the upper floor. Walk over the tile: it shakes 20 f, falls, **lands on the plate**, and the gate stays open (the tile's weight holds it). A guard below is crushed if he is under it | guard ×1, falling tile ≤ 1, gate [3] | loose tiles | the classic PoP move, with no damage at stake. FLM-04 |
| **06** | **Spike corridor.** Three spike traps spring 12 f after you come within 24 px, stay up 60 f, then stay down 40 f while they re-arm. **Bait one, step back, and cross while it re-arms** (walking clears a trap in about 25 f, a slide in 13 f) | spike traps ×3 [3] | spikes = 6 dmg | Jet hovers over them. FLM-05 |
| **07** | **First guard.** A palace guard-bot advances with his blade up. **Any shot that reaches him less than 48 px from Rock is parried** (a clang and a glint; no damage); from farther away, shots hit. He lunges (blade glint 12 f, then 24 px in 8 f, 4 dmg) and recovers for 20 f, open to everything. PUNCH★ is never parried | guard ×1 [1] | | the spacing rule Flame Man uses (§2.8). FLM-06 |
| **08** | **The timed gate.** A raise plate on the left opens the right gate for 240 f; it lowers during the last 60 f. While its bottom is still above the slide's height (tuned to the slide hit box, `$059A` id 3) you can **slide under it** (PoP's roll) | spike trap ×1, gate [2] | the gate closes (blocks; no damage) | T3 timed. The plate can be pressed again |
| **09** | **CHECKPOINT 1.** A palace hall: carpets, columns, a window onto the oil field | none [0] | | |
| **0A** | **v1.0: the spike hall**: three spike traps in doorways at offset timings. *v1.1 (Should): THE CHOMPER HALL, three chompers, each closed 8 f every 90 f, offset by 30 f; tell: a glint and a "shing" 12 f before they close; 8 dmg* | spike traps ×3 [3] (v1.1: chompers ×3 [3]) | | v1.1: Time Stop freezes the chompers |
| **0B** | **THE OIL GALLERY** (the oil twist; where FIREPROOF is usually lost, §2.5.3). Two oil pools on the floor, each with a guard standing in it and a **chandelier** on a chain above it. Shoot a chain (one hit): the chandelier falls, **that pool ignites** (its own oil metatile id), and its guard burns (a HAZARD kill, `systems.md` §6.4). The pool is now deadly for the rest of the visit, so you take the **upper balcony** over it instead (harder jumps). Or don't, and fight the guards in slow oil | guards ×2, chandeliers ×2 [4] (a falling chandelier is the same object, and a burned guard's explosion takes his own slot, vanilla type `$17`: 9 slots at most) | the choice, per pool | each pool uses a **distinct oil metatile id** so they ignite separately (vanilla's per-id rule; block-id cost reported by the build). FLM-07 |
| **0C** | **The balcony.** The Mr. Y gag: v1.0, a sponsor tapestry with a familiar moustache on it; v1.1, a window with **the vizier**: Wily in an obviously fake costume-shop hat and a stick-on beard over his own moustache, waving a sponsor's clipboard. Fire Tellies over a last oil channel | Fire Telly ×2 + drops ≤ 2 [4] | | FLM-08 (Should) |
| **0D** | **v1.0:** a guard on a ledge over a pit, and a loose tile in front of him. *v1.1 (Should): the skeleton-bot: at 0 HP it collapses into bones for 120 f, then rises with full HP; it is destroyed for good if it falls into the pit (a full charge, systems' FULL flag, knocks it back 16 px), if a loose tile falls on its bones, or if it stands in burning oil* | guard ×1, falling tile ≤ 1 [2] | pit | |
| **0E** | **THE MIRROR ROOM** (§2.5.1). A tall mirror on the right wall. When you reach the middle of the room, **Shadow Rock** steps out of the glass | Shadow Rock + its mirrored shots ≤ 3 [4] | | FLM-09 (Must: the merge tell). T7 |
| **0F** | Down a shaft into the fire vault | Fire Telly ×1 + drop [2] | | the down exit loads CHR `$87` (vanilla red rock and flames), palette `$1F` |
| **10** | **CHECKPOINT 2. The fire vault** (vanilla v0E-v15 art): channels of oil that are **already burning** (placed as the burning variant), small orange platforms | juggler `$2A` (+ its flame `$2F` and ring `$48`), mine `$73` ×1 [4] | burning channels | pre-lit oil does not count against FIREPROOF |
| **11** | **The hourglass gate.** A plate on the left starts a long gate closing over 600 f; a mural hourglass drains (a palette cycle). Cross the platforms over burning oil before it shuts. If it shuts, walk back and press the plate again | mines ×2, gate [3] | | T3 timed. No fail state |
| **12** | **The mouse alcove.** The main route runs over the top platforms. Below, a short dead end: a shut gate, a **mousehole** beside it, and a plate on the far side of the gate (§2.5.2) | mine `$73` ×1, the mouse (when it is out), gate [3] | | the hidden room's entrance |
| **13** | **Loose bridge.** A bridge of loose tiles across a burning channel: a tile you step on shakes 20 f and falls, but the next one starts shaking only when the last has landed, so a runner crosses ahead of the collapse and a dawdler falls. A juggler throws flames from the far bank | juggler (+ flame, ring), falling tile ≤ 1 [4] | | loose tiles are T6 cells until they fall |
| **14** | The antechamber: two guards in front of the throne-room doors | guards ×2 [2] | | |
| **15** | Shutter corridor. **Boss checkpoint.** The **palace fire marshal** stands here (FIREPROOF, §2.5.3) | fire marshal, chip capsule [2] | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room** (§2.8) | Flame Man [boss + ≤ 3] | | vanilla boss-room art (red pistons, oil-pipe floor) kept, plus two oil strips |
| **17** | **The mirror passage** (secret route): a dark corridor behind the glass, in an inverted purple palette. Mirror panels on the walls show your reflection walking the other way (harmless, BG) | guards ×2 (shadow palette) [2] | | palette swap |
| **18** | **The rooftops at night**: domes under a full moon (R3.4). Loose roof tiles, a guard, a Fire Telly against the moon | guard ×1, Fire Telly (+ drop), falling tile ≤ 1 [4] | pits between domes | new BG art |
| **19** | Secret shutter corridor (checkpoint); the fire marshal again | fire marshal, chip capsule [2] | | |
| **1A** | **SECRET ARENA** (§2.9) | Flame Man | | the kill sets the secret flag |
| **1C** | **Hidden room: the princess's chamber** (§2.5.2) | envelope, large life energy, 1-up [3] | | |

### 2.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 09 | camera on 09 | `$86` + the palace third / palace palette |
| CP2 | 10 | camera on 10 | `$86` + `$87` / `$1F` |
| *(CASUAL)* | 07 | camera on 07 (the dungeon) | palace |
| *(CASUAL)* | 0D | camera on 0D (the palace, before the mirror) | palace |
| *(CASUAL)* | 12 | camera on 12 (the vault) | `$87` / `$1F` |
| Shutter | 15 (main), 19 (secret) | shutter entry | |

Ignited pools, opened gates (held by tiles) and fallen loose tiles all **survive deaths** (`$0340` and T6 state, like
vanilla breakables), so a death never undoes a puzzle you solved, and never un-burns a pool.

### 2.5 Secrets

#### 2.5.1 Secret exit: don't fight your shadow `[new-code M · Must]`

- **Shadow Rock** is a dark-palette Rockman (the player's own frames in a new palette: no new tiles) that **replays your
  pad with LEFT and RIGHT swapped** (T7). It starts at the mirror facing you, so when you walk toward it, it walks
  toward you. When you fire, it fires. HP 12.
- **Contact is harmless until you fire** (R3.9, design-17): a player who never shoots can bump into it freely.
- **The merge window:** after **5 s without firing** (counted from its appearance, and again from your last shot), **the
  mirror glows** and the shadow lowers its arm (R3.9). While the mirror glows, touching the shadow **merges** you: one
  white flash (a fade under REDUCED), your HP refills (as in PoP), and the mirror cracks open on the passage to 17.
  Firing ends the glow and restarts the 5 s.
- **After your first shot** its contact does 4, except while the mirror glows.
- **Fight it** and it fights back with your own moves, mirrored. Destroy it and it shatters; the mirror becomes an
  ordinary wall and the stage goes on (0F).
- **Why it is fair:** the shadow copies you, so a player who holds fire is never attacked, and the glow says "now".
  The rule teaches itself to anyone who stops shooting, and PoP players will try it on sight.
- **Tell:** FLM-09 when it appears; the glow; the debrief hint (§2.12).
- **Effect:** merge → 17 → 18 → 19 → the secret arena 1A. Beating Flame Man there clears the venue and sets the secret
  flag.
- **Fight id:** a mid-boss fight id from meta's `$08-$12` range (consistency-44 proposes `$0E`).

#### 2.5.2 Hidden room: the mouse (1C) `[new-code S · Must]`

- **Gate:** stand in the alcove of 12 and **don't touch the pad for 10 s**. A mouse-bot scurries out of the mousehole,
  runs under the gate and sits on the plate on the far side: the gate opens onto 1C.
- **Tell:** the mousehole is drawn beside the gate; while you stand in the alcove a squeak plays every 3 s (the squeak
  is Should in art_audio §12.6; this doc asks for it as a Must SFX of about 20 B because it is the tell of a Must
  secret, with a vanilla high blip as the fallback); FLM-12 when the mouse appears (Should). The gate itself, shut in
  front of a dead end with a plate behind it, says "something has to get in there".
- **Contents:** the princess's chamber: a big potion (large life energy), the **sponsor envelope** and a 1-up.
  *Could:* **Roll** asleep on the divan on her pit-crew break (BRIEF §2's optional cameo; story writes her line).
- **Return:** the gate stays open; walk out.

#### 2.5.3 Behaviour-gated chip: FIREPROOF `[new-code S · Must]`

- **Gate:** reach a boss shutter (15, or 19 on the secret route) with **no oil ignited this visit**. Every ignition goes
  through `$3E:$DDFC`, so one registry hook there clears a "clean" bit; the pre-lit channels of the fire vault are
  placed burning and never call it. Freezing a burning pool with the Ice Block later does not restore the bit.
- **Why it is a trade-off:** the gallery's chandeliers (0B) are the easy way past two guards, and the Fire Tellies of
  01 and 0C (and 18) light the oil themselves unless you shoot them before they drop. The chip asks for the hard way all
  the way through.
- **Tell:** screen 01 is the lesson (a Telly hangs 120 f over a pool; FLM-02, Must); the first ignition gets FLM-02's
  second half; the fire marshal stands in plain view at 15 and **tsk-tsks** if you failed (FLM-13, Should). The
  debrief hint.
- **Award:** the fire marshal hands over the chip capsule in the shutter corridor (he stands in 15 and in 19).
- **Effect:** `systems.md` §9.2, FIREPROOF (burning floors deal 4 with knockback instead of killing; fire projectiles
  do half).

### 2.6 Tileset and art (art_audio §4.4 owns the counts)

- **Kept vanilla CHR:** `$86` (the oil field: pipes, girders, DANGER drums, wavy oil, dunes, arches, purple brick,
  spikes, ladders) and `$87` (red rock and flame tufts for the fire vault). The oil palette cycle (thread 4,
  `$22-$24`) and the ignite alternates (flame tiles `$E6-$E9`) are kept as they are.
- **New BG** `[new-art M · Must]`: the dungeon third (stone and torches, columns, arches and PoP-style windows, carpets,
  pressure plates raised and pressed, the loose tile's socket) and the palace third (the mirror 32×48 with its glow
  palette, the hourglass mural, the mousehole, the sponsor tapestry, the throne-room backdrop for 1A, rooftop domes and
  a full moon, the balcony window). **Removed by R3.4:** minarets and the crescent moon. Should: chomper slots.
- **New sprites** `[new-art M · Must]`, vanilla recolours and composites first (R5.1): guard-bot (stand, advance,
  blade-up glint, lunge, recover: 5 frames), portcullis (16×48), loose tile, spike trap (3 frames), chandelier (16×24),
  mouse-bot (2), the fire marshal. Shadow Rock reuses the player's frames in a dark palette. Flame Man's pinch set: the
  **flaming sword** and the head flame guttering (BLOWOUT). Should: skeleton-bot (walk ×2, collapse, bones), chomper
  blades, the vizier.
- **Changes for art_audio's re-run** (R5.3): the mouse and the fire marshal are Must (art had SET-FL3 Must already);
  the gallery needs 2 chandeliers, not 3 (art §4.4's SET-FL1/FL3 overlap note shrinks); the guard's "block" frame
  becomes the blade-up parry glint; minarets and the crescent leave the palace third.

### 2.7 Enemies and objects

| Object | Kind | HP (buster taps) | Behaviour | Freeze | Mark |
|---|---|---|---|---|---|
| Metall `$18`, Fire Telly `$2C` (+ drop `$30`), wheel cannon `$C0`/`$C9`, juggler `$2A`, mine `$73` | vanilla | as vanilla | vanilla; the Telly's drop and the juggler's flame ignite oil (vanilla). The Telly dies to W.STORM (the featured-enemy tell) | per tech's audit | `[engine-ok]` |
| **Palace guard-bot** | new | 6 | advances 0.75 px/f with the blade up; **parries any shot that reaches him less than 48 px from Rock** (clang, glint, no damage; PUNCH★ always lands); LUNGE: glint 12 f, 24 px in 8 f (4 dmg), recover 20 f (no parry); in oil he moves at half speed | H | `[new-code S · Must]` |
| **Raise plate / gate / timed gate** | new (T3) | - | plate (a metatile; the pressed look comes from the slot's alternate set) + gate (16×48 sprite, solid, rises and lowers 1 px/f) | NF | `[new-code M · Must]` |
| **Loose tile** | new | - | a floor cell (T6) until stood on: it shakes 20 f, then the cell clears and a falling-tile object spawns (so only falling tiles cost a slot); breaks on landing; 4 dmg to what it lands on; weighs down plates | NF | `[new-code S · Must]` |
| **Spike trap** | new | - | springs 12 f after the player comes within 24 px, up 60 f, then down and disarmed 40 f; 6 dmg | NF | `[new-code S · Must]` |
| **Chandelier** | new | 1 (the chain) | falls, ignites the pool below (calls the vanilla ignite on that pool's id), 6 dmg if it lands on you; a guard it burns is a HAZARD kill | NF | `[new-code S · Must]` |
| **Shadow Rock** | new (T7) | 12 | §2.5.1 | NF (a frozen mirror would desync from the pad history) | `[new-code M · Must]` |
| **Mouse-bot**, **fire marshal** | new | - | scripted NPCs | NF | `[new-code S · Must]` |
| **Chomper** | new | - | 8 f closed every 90 f, offset param; tell 12 f; 8 dmg | NF | `[new-code S · Should]` |
| **Skeleton-bot** | new | 4, then bones 120 f, then full HP | slow walk, slash; destroyed for good by a pit, a loose tile or burning oil; a full charge (the FULL flag) knocks it back 16 px | H | `[new-code S · Should]` |
| **The vizier** | new | - | a waving figure in the balcony window | - | `[new-art S · Should]` |

### 2.8 Boss: Flame Man, "the palace duel" (16)

**Arena:** the vanilla boss room (red pistons) with **two oil strips** in the floor, the left third and the right
third; the middle third is stone. Arena oil uses a **timed** ignite (the map-edit service's per-id flip with a timer:
burns 90-180 f, then goes out) `[new-code S]`, not the venue's permanent one, so the fight stays fair.

**Intro (90 f):** Flame Man draws a **flaming sword** from his sash, bows, and takes a fencing stance: the duel of the
1989 game.

**Pattern loop (HP 28 to 10):** DUEL → PILLARS → LEAP → PILLARS, about 540 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **DUEL** (spacing, R3.1) | the stance itself; a **blade glint** whenever Rock is within 48 px | advances 0.75 px/f, blade raised. **Any shot that reaches him less than 48 px from Rock is parried** (clang, no damage); shots from 48 px or farther hit. After 60 f, THRUST: glint 12 f, lunge 24 px in 8 f (4 dmg), recover 24 f (nothing is parried). Twice, then a 32-px backstep (20 f) | 60 + (12+8+24) ×2 + 20 | **keep your distance and shoot**; back off from the glint; punish the recovery; PUNCH★ is never parried (DISARM) |
| **PILLARS** (vanilla move) | kneels, 16 f | two floor flames, 20 f apart, travel at 3 px/f and rise into 16×48 pillars where you stood (45 f). **A pillar on oil ignites that strip for 90 f** | 16 + 40 + 45 | move off the oil; this is F.BLAST's tap, shown |
| **LEAP** (vanilla move) | crouch 10 f | jumps high (peak y `$30`) and lands within 24 px of you (50 f airtime); landing in oil splashes two droplets | 10 + 50 + 16 | run under him |

Boss-side objects: 2 flames or 2 droplets (3 flames under ABSORB, v1.1); the WEAK! pop takes a free slot only (§0.2).

**Pinch (HP ≤ 9): THE PALACE BURNS.** He drives the sword into the floor (40 f; the room tints red and holds it: a
tint, not a flash). Both oil strips ignite **from the walls inward**, 8 px every 4 f, and burn for 180 f; the stone
middle stays safe. While the strips burn he fights in the middle (DUEL only), and once per burn a **fire column rises
from the floor and sweeps across the room** at 2 px/f (16×40: jumpable): F.BLAST's alt (Flare), shown. The strips
relight every 300 f.

**Damage and i-frames:** `systems.md` Tables 1-2 (Flame's column: W.STORM 4 W with 16 f; B.ATTACK 3 G, and B.ATTACK
also puts out a burning strip for 120 f; SILVER.T 1 R; F.BLAST his own).

**WEAK reaction, BLOWOUT** (SC9, Must): W.STORM blows out the flame on his head. He pats his head and fumbles to relight
it for 40 f: no parry, no attacks, WEAK! pop, FLM-14.

**Own-weapon reaction, ABSORB** (SC4, Should; a named SC4 exception, consistency-33): the first F.BLAST hit **heals him
1** instead of doing 0, and his flame grows: for 300 f PILLARS fires three flames instead of two. FLM-15.

**Forms** (refights): PUNCH★ hits through the parry and **disarms** him: the sword spins into the ceiling and sticks
there for one loop (no DUEL until he pulls it down). His flaming lunge previews **Burning Knuckle**, the F.BLAST
synergy.

**VENUE ACT** (systems §6.5): **CLEAN DUEL**: beat Flame Man with none of your shots parried.

**Fight loader** (W2): the strips are arena data and their timer lives in the arena's script, so the fight runs the
same when loaded alone; the pinch threshold comes from the per-fight byte.

**Credits mode** (fortress §6.2; `IFCREDITS`, tech §4.6): with no one to duel, DUEL becomes a kata: he advances to the
room's centre mark, shows the blade glint and THRUSTs at the air twice, then backsteps. PILLARS and LEAP aim at a fixed
mark on the right oil strip, so the show includes a strip burning out on its own timer. No parry, no pinch, no reaction.
Fallback: his card strip only.

### 2.9 Secret arena (1A)

- **v1.0 (Must):** the boss arena again, under a night palette, with the hourglass mural behind the throne (BG). Same
  fight; the kill sets the secret flag.
- **v1.1 (Should): THE THRONE ROOM's twist** `[new-code M · Should]`: **now Flame Man has a shadow.** A Shadow Flame Man
  (Flame Man's frames, dark palette) stands mirrored across the room's centre line and copies his **movement**, mirrored
  (T7 on the boss's own inputs), so DUEL thrusts come from both sides; the projectiles still come from Flame Man alone
  (lag). The shadow cannot be hurt and its contact deals half damage. **Each W.STORM hit makes it flicker; the third
  one blows it out for good.** The player who merged with their own shadow to get here now has to beat a man who
  didn't. (Fallback if T7 slips: the main fight on an all-oil floor: slow walk, low jump.)

### 2.10 CASUAL levers (Must) and HARD pokes (Should)

**CASUAL** (R2.9; `systems.md` §13.4's lever table):

| Lever | Where (screen, object) | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | every Fire Telly's hover before it drops (01, 0C, 0F, 18) | 120 f | 240 f | `REFLEX` |
| reflex | the spike traps' spring delay (06, 08, 0A) | 12 f | 24 f | `REFLEX` |
| reflex | the loose tiles' shake (05, 0D, 13, 18) | 20 f | 40 f | `REFLEX` |
| reflex | the lunge glint of the guards and of Flame Man (07, 0B, 14, 16-18, 1A) | 12 f | 24 f | `REFLEX` |
| mash | none | - | - | - |
| timer | the plate gates' hold (03, 05) | 300 f | 450 f | `TIERVAL` |
| timer | the timed gate (08) | 240 f | 360 f | `TIERVAL` |
| timer | the hourglass gate (11) | 600 f | 900 f | `TIERVAL` |
| checkpoint | dungeon, palace, vault | CP1 09, CP2 10 | + 07, 0D, 12 | dormant checkpoint objects woken by a CASUAL poke |
| secret step | the mirror's glow (0E) | 5 s without firing | 3 s | `IFCASUAL` |
| secret step | the mouse (12) | 10 s standing still | 6 s | `IFCASUAL` |
| secret step | FIREPROOF (every oil pool) | any ignition voids it | the first ignition by a Fire Telly's drop is forgiven; a chandelier shot still voids it (the chandelier's own ignite call marks its source) | `IFCASUAL` in the ignition hook on `$3E:$DDFC` |

**HARD** (Should, v1.1):

| Section | Poke | Kind |
|---|---|---|
| Ignition lesson 01 | the Telly hovers 60 f instead of 120 f | AI param |
| Dungeon 06 | spikes re-arm after 25 f instead of 40 f (a slide still clears them) | param |
| Dungeon 08 | timed gate 240 → 180 f | param |
| All | loose tiles shake 10 f instead of 20 f; guards parry within 64 px | param |
| Gallery 0B | guards lunge every 40 f | param |
| Mirror 0E | the mirror glows after 8 s; contact damage 6 | param |
| Fire vault 11 | hourglass gate 600 → 420 f | param |
| Boss | pinch at HP ≤ 14; DUEL thrusts three times; the strips relight every 200 f | AI branch |
| (v1.1 content) | chompers: cycle 90 → 70 f, closed 8 → 12 f; skeleton rises after 60 f | param |

### 2.11 Commentator hooks (ids; the words are story §6.3's)

| Id | Trigger | Tier (R4.5) |
|---|---|---|
| FLM-01 | match card ends (story already dropped "Oil Sultanate") | Should |
| FLM-02 | a Telly over the pool (01) / the first pool ignites | **Must** (FIREPROOF's tell) |
| FLM-03 | first plate pressed | Should |
| FLM-04 | first loose tile falls | Should |
| FLM-05 | first spike trap | Should |
| FLM-06 | **first shot parried** (trigger changed: story rewrites the line for the spacing rule) | Should |
| FLM-07 | a chandelier ignites a pool | Should |
| FLM-08 | the Mr. Y gag on screen (the tapestry; the vizier in v1.1) | Should |
| FLM-09 | Shadow Rock appears | **Must** (the merge tell) |
| FLM-10 | merge | Should |
| FLM-11 | Shadow Rock destroyed | Should |
| FLM-12 | the mouse appears | Should |
| FLM-13 | FIREPROOF awarded / refused | Should (story §6.2's "behaviour item" line covers the award) |
| FLM-14 | first W.STORM hit (`EV_WEAK_FIRST`) | **Must** |
| FLM-15 | F.BLAST on Flame Man (ABSORB) | Should (with SC4) |
| FLM-16 | pinch | Should |

**Death lines** (Must: 4): story's lines 1, 2, 3 and 6 are recommended (6 is the 60-minute joke, aimed at PoP's
mechanics as R3.4 asks). Line 5 needs the vizier (Should); line 4 (the hourglass) is a good alternate.

### 2.12 Judges' debrief hints (tier B; meta §4.4, story's words)

1. FL0, exit: "Your shadow only fights if you fight. Hold your fire until the mirror glows, then walk into it."
   (Reworded for the glow, R3.9.)
2. FL1, room: "Something small lives behind a gate in the fire vault. Stand still and listen."
3. FL2, FIREPROOF: "The palace fire marshal rewards entrants who leave the oil unlit. Shoot the fire-droppers first."

### 2.13 How crazy it gets

1. Rockman slides under a closing portcullis like a 1989 prince.
2. A chandelier crashes into an oil pool and the guard standing in it goes up in flames, and the pool burns for the
   rest of the match.
3. Rockman meets his own shadow, and the winning move is a hug.
4. A mouse opens the secret room.
5. Flame Man draws a flaming sword, bows, and parries every shot you fire from too close.
6. *(v1.1)* A skeleton guard falls apart and puts itself back together.
7. *(v1.1)* The vizier on the balcony is Wily in a costume-shop hat.
8. *(v1.1)* In the throne room, Flame Man has a shadow of his own.

### 2.14 Revisits and VARIETY

- **Taps (v1.0):** F.BLAST **ignites oil** on purpose: burn the gallery's guards from the floor without the
  chandeliers (and lose FIREPROOF). B.ATTACK's flakes snuff the Tellies and jugglers (vanilla's thematic table).
- **Ice Block (v1.0, from the slice):** freezes burning oil into a 300-f ice floor: a safe crossing of 13's burning
  channel under the loose bridge.
- **Alts (v1.1, Should):** Time Stop freezes the hourglass gate (11) and the chompers (0A); Y.SPEAR's Wall Spear climbs
  to 0D's high ledge (a large weapon energy; the mirror room keeps its slots for the shadow).
- **Tag partner (Should, cut-line item 2, with the tag partner):** Break Man's shield catches the guards' lunges from
  the front; the optional shortcut is a guard on a ledge over 18's pit that only his double knockback can push off.
- **Par** (placeholder): 300 s.

---

## 3. Centaur Man: ATLANTIS RUINS (stage `$07`)

### 3.1 The pitch

*The Ancient City* (vanilla's location), sunk under the sea. **Every room is a ZONE with a number**, shown under the
life bar the way 4MI shows Pharaoh's curses. Doors carry zone numbers on their plaques, and most tell the truth, but in
Atlantis **cracked doors lie** (a "ZONE 99" that drops you back to ZONE 8), **painted doors are fake**, and in the
**black zone** the only things you can see are the things that glow, including a door to ZONE 0 that only shines in
the dark. Then the **tide** (vanilla's raster set piece) rises and falls through the halls, and here it is **the
venue's spine** (R3.1): at high tide you swim-jump to ledges you can't reach on foot; at the lowest tide a barnacled
door marked **ZONE 100** opens (the secret exit); and the way out is a **drowned tower that floods as you climb**:
wait for the water, swim up, don't fall at low tide. At the top, the vanilla 112-px **Pegasus gap**: fall in for the
main route, or fly over it with the Jet to the sky temple and Beat's **T plate**.

| Homage (design notes) | Here | Mark |
|---|---|---|
| *Atlantis*: numbered zones | a **ZONE card** per room (a HUD widget label) | `[new-code S · Must]` (data on the widget) |
| *Atlantis*: doors that warp, doors that send you back, doors that aren't | **zone doors**: honest, lying (cracked lintel), fake (painted) | `[new-code M · Must]` |
| *Atlantis*: dark "black" zones | **the black zone** (BG palette black; plaques glow) | palette data + `[new-code S · Must]` |
| *Atlantis*: warping deep into the game | **ZONE 100**, the tide door (secret exit) | `[new-code S · Must]` |
| *Kid Icarus*: the Underworld climb | **the tidal shaft** (R3.1: replaces the wrap tower, which repeated Blizzard's climb) | `[new-code S · Must]` |
| *Kid Icarus*: Centurions who help at the boss | **Centurion statues**, freed with a full charge (CENTURION) | `[new-code S · Must]`; their help in the boss fight is Should |
| *Kid Icarus*: Pegasus, the sky temple | the Jet over the **Pegasus gap**; the **sky temple** holds the T plate | vanilla geometry + `[new-code S · Must]` |
| *Kid Icarus*: the Reaper who panics and calls Reapettes | **Grim Reap-bot** with a siren and Reaplets | `[new-code S · Should]` |
| *Kid Icarus*: the Eggplant Wizard; the hospital | **Nasubi Mage** (Should), the eggplant curse (Could), a **hot spring** that heals and cures (Should) | as marked |

### 3.2 Map shape

```
00-03 ZONES 1-4 sky ruins (vanilla) ─> 04 down ─> 05 ZONE 6 sea corridor ─> 06 ZONE 7 [CP1] tablet
   ─door─> 07-0B ZONE MAZE (ZONES 8-12; 0A = BLACK ZONE ──"0" door──> 1D hidden room)
   ─door─> 0C ZONE 13 [CP2] TIDE ─> 0D ZONE 14 ─> 0E ZONE 15 ──(lowest tide: "100" door)──> 1A ZONE 100 ─> 1B shutter ─> 1C SECRET ARENA
   ─> 0F ZONE 16 waterfall ─up─> 10-12 TIDAL SHAFT (ZONES 17-19) ─up─> 13 ZONE 20 tower top ─> 14 ZONE 21 PEGASUS GAP
          fall: 15 lower hall ─> 16 shutter ─> 17 BOSS (tide arena)
          Jet:  18 sky bridge ─> 19 SKY TEMPLE (T plate) ─drop─> 15
```

Screens used: main 00-17 (24), T route 18-19 (2), secret 1A-1C (3), hidden room 1D (1) = **30 of 32**. Spare: 1E, 1F.

### 3.3 The door rules (taught on screen 06)

A stone tablet at checkpoint 1 states the whole rule set (UP reads it; story writes the words; the round-1 draft was
"In Atlantis an honest door shows where it goes. A cracked door lies. A painted door is a painting."). It is the tell
for every door in the maze:

- **Honest door**: the plaque's number is the zone it leads to.
- **Lying door** (cracked lintel): shows a big number and **sends you back** to an earlier zone (ZONE 8's `12` to ZONE
  7; ZONE 12's `99` to ZONE 8). It never kills; it costs time (Atlantis's notorious warps back, made fair by the crack).
- **Fake door** (painted, flat shading): pressing UP bonks Rockman's head (a sound and an 8-f stun, no damage on
  NORMAL).
- **How doors are built (lag, §0.2):** a door is **BG**: its frame and its plaque numerals are tiles of the zone third.
  Each maze screen's script holds a small door table (cell, kind, target), and on an UP press at a door (R2.10) it runs
  a 16-f fade and T3's door/warp target through the vanilla `$39:$89F5` path. No door costs an object slot. Maze rooms
  are locked single screens, so they don't have to be neighbours in the layout.

### 3.4 Screen by screen

Brackets: peak stage objects (≤ 4, §0.2). The ZONE card is a HUD widget, not an object.

| Scr | ZONE | What the player does | Stage objects [peak] | Hazards and set pieces | Notes |
|---|---|---|---|---|---|
| **00** | 1 | Match card. Sky ruins: purple fluted columns, gold capitals, clouds. **Centurion statue #1** on a pedestal by the path: cracked stone, eyes that blink | statue [1] | | vanilla v00 art, CHR `$AA`, palette `$A6`. CEN-01, CEN-02 |
| **01** | 2 | A **drifting cloud platform** over a sky gap, with a pelican overhead | cloud ×1, pelican spawner `$A9` + pelican `$AB` ×1 + its dropped fish [4] | sky gap = pit | the cloud object is Blizzard's |
| **02** | 3 | Two drifting clouds over a wider gap | clouds ×2 [2] | | |
| **03** | 4 | **The Y-MAN mural** (BG: a bald Atlantean with a moustache, "THE Y-MAN SHALL COME"). One door, plaque `5`: the door lesson | none [0] | | CEN-03 |
| **04** | 5 | Down into the drowned city: water begins (type 8, floaty gravity) | piranha `$C1` ×2 + bubbles `$08` ≤ 2 [4] | | down exit (vanilla v04 → v05 shape) |
| **05** | 6 | Underwater corridor (vanilla v06-v08 art). **Centurion #2** sits in an alcove above the corridor (a swim-jump) | piranha ×1 (+ bubble), statue [3] | | palette `$A7` |
| **06** | 7 | **CHECKPOINT 1.** The stone tablet (§3.3). A door `8` | none [0] | | CEN-04 |
| **07** | 8 | **MAZE 1.** Three doors: `9` (honest), `12` (**cracked**: lies, back to 06), and a painted door. A piranha pond between them | piranhas ×2 (+ bubbles ≤ 2) [4] | | CEN-05, CEN-06 |
| **08** | 9 | **MAZE 2.** Doors `10` (honest) and `11` (honest, but it **skips ZONE 10**, and with it Centurion #3) | wall cannon (+ shot) [2] | | the first real choice |
| **09** | 10 | **MAZE 3.** **Centurion #3** on a ledge. A seahorse in a pool. Door `11`. *v1.1 (Should): the Nasubi Mage floats over the room throwing eggplants, and a hot spring steams in the corner* | statue, seahorse `$C4` (+ its shots `$14`/`$CC` ≤ 2) [4] (v1.1: the Mage + eggplant replace the seahorse [3]) | | CEN-09, CEN-10 (Should) |
| **0A** | 11 | **MAZE 4: THE BLACK ZONE.** The BG palette goes black; only sprites, the doors' glowing plaques and a few glowing wall glyphs show the room. Door `12` (honest). **The `0` door** glows on a high ledge reached from a floating stone (§3.7.2) | piranha ×1 (+ bubble), floating stone [3] | jumps in the dark | CEN-07 (Must: ZONE 0's tell). C.FLASH lights the room for 240 f (systems) |
| **0B** | 12 | **MAZE 5.** Doors `13` (honest) and `99` (**cracked**: lies, back to 07) | seahorse (+ shots ≤ 2) [3] | | |
| **0C** | 13 | **CHECKPOINT 2.** **The tide starts** (vanilla chain `$14`, about 60 px of travel). GP adds a **60-f dwell** at both extremes, so "high tide" and "low tide" are states you can read and wait for | seahorse (+ shots ≤ 2) [3] | | the vanilla tide init (script 5B) moves here, with the dwell in `EFX_PARAM` (tech §4.4) |
| **0D** | 14 | **The tide as a lift.** A ledge with a large energy and the way on sits 80 px up: **only a swim-jump at high tide** reaches it (estimate from the vanilla constants: about 90 px in water against 52 on land; verify in the emulator at M5). At low tide you walk under the overhang | seahorse ×1 (+ shots ≤ 2), the ledge's large energy [4] | | CEN-12 |
| **0E** | 15 | **THE SUNKEN DOOR.** On the floor of the room, a barnacled door with the plaque `100` and a painted tide line across it. It opens **only while the tide is at its lowest** (§3.7.1). Otherwise UP does nothing and bubbles stream from its frame | seahorse (+ shots ≤ 2) [3] | | the secret exit. CEN-13 |
| **0F** | 16 | Waterfall room (vanilla v0E-v0F): climb out of the water past a dome turret and a red spearman, up into the drowned tower | dome turret `$2B` (+ its shot `$2E`), spearman `$70` [3] | | up exit; palette `$CA`. No cloud or plaque sprites here (the turret's tiles clash with them, art_audio §4.8) |
| **10** | 17 | **TIDAL SHAFT 1** (§3.5): a locked tide room; three ledges zig-zag up, 80 px apart; the ladder up hangs from the top one | piranha ×1 (+ bubble), tide float [3] | falling = back to the ledge or room below | CEN-22 (Should) |
| **11** | 18 | **TIDAL SHAFT 2**: the mean water line is 16 px higher | piranha ×1 (+ bubble), tide floats ×2 [4] (v1.1: the Grim Reap-bot on the dry top ledge replaces the piranha and one float; on alarm, 2 Reaplets [4]) | | |
| **12** | 19 | **TIDAL SHAFT 3**: higher again; the top ladder leads to the tower top | piranha ×1 (+ bubble), tide floats ×2 [4] | | |
| **13** | 20 | **The tower top**: the vanilla **jester head** `$10` guards it, its crest now drawn as snakes | jester head (+ its shots ≤ 2) [3] | | CEN-14. A palette swap of `$10` only |
| **14** | 21 | **THE PEGASUS GAP** (vanilla v15: 112 px wide, the far floor 32 px lower). **Fall in** for the main route; **fly across with the Jet** to the T route (18) | spawner + pelican ×1 + its fish [3] | | vanilla geometry kept exactly (the Jet's measured crossing: hold A 100+ f) |
| **15** | ?? | The lower hall (the fall lands here; vanilla v18 shape). The ZONE card shows `??` | spearman ×1 [1] | | the down exit's target; the back exit up to 14 as vanilla |
| **16** | | Shutter corridor. **Boss checkpoint** | none | | shutter checkpoint (`$0684` = 16) |
| **17** | | **Boss room: the Temple of Tides** (§3.10) | Centaur Man [boss + ≤ 3] | the tide | |
| **18** | | **SKY BRIDGE** (T route, Jet): Kid Icarus sky, clouds, three small landing islands to rest on while the Jet's fuel regrows (+1 per 2 f), pelicans | cloud ×1, spawner + pelican ×1 + its fish [4] | pits | CEN-15 |
| **19** | | **THE SKY TEMPLE**: Beat's **T plate** on the altar (§3.7.4). A hole in the floor drops you back to 15 | T plate [1] | | story §6.2's plate line |
| **1A** | 100 | **ZONE 100** (secret route): the Atlantean core, fully underwater, coral and gold. *v1.1 (Should): currents from vents push you 0.5 px/f* | piranha ×1 (+ bubble), seahorse (+ shot) [4] | | palette from the vanilla **revisit** set (bank `$28`: gold turns orange-brown), free |
| **1B** | | Secret shutter corridor (checkpoint) | none | | |
| **1C** | | **SECRET ARENA** (§3.11) | Centaur Man | | |
| **1D** | 0 | **Hidden room: ZONE 0** (§3.7.2) | envelope, 1-up, large weapon energy [3] | | |

### 3.5 The tidal shaft (10-12) `[new-code S · Must]` (R3.1, design-5)

The wrap tower of round 1 repeated Blizzard's climb (X-WRAP twice). The tide replaces it, so the venue's own vanilla
set piece carries its ending as well as its secret.

- **Rooms:** three locked one-screen tide rooms stacked vertically and joined by ladders (vanilla shafts are
  consecutive screens with up/down exits). Each room runs the 0C tide init from its own screen script with a **per-room
  base level** (one byte, `TIDE_BASE`: each room's screen script writes it, and `EFX_PARAM` keeps the stage's dwell;
  tech §1.8): **the mean water line rises 16 px per room**, so the tower floods as you climb and the higher rooms stay
  wet longer.
- **The climb:** three ledges zig-zag up each room, 80 px apart. A jump from a ledge reaches the next one **only when
  the water covers the lower ledge** (a high-tide swim-jump: 0D's lesson, now a climb). At low tide the jump falls
  short. A miss drops you onto a lower ledge, or out of the bottom of the room into the room below: lost time, not a
  life.
- **Tide floats:** a floating stone rides the water line (vanilla's tide handler already moves every type-`$72` object
  to the line; the float is either that type or a GP family object that copies `$0672`, tech's call). Stand on it as
  the tide rises and it lifts you, the purest form of "the tide is a lift". If a float costs more than S, the shaft
  ships with swim-jump ledges only.
- **Danger:** a piranha patrols each room's always-wet bottom band. v1.1 (Should): the Grim Reap-bot patrols 11's dry
  top ledge and his alarm calls 2 Reaplets; that room drops its piranha and one float, for the lag cap.
- **Tells:** 0D teaches the lift; each ledge carries a **painted tide line** at the height the water must reach (the
  same mark as the ZONE 100 door), so the rule is readable in every room.
- **Fallback** if chain `$14` misbehaves across vertical exits (tech's check at the start of M5, tech §16.8): the three
  rooms join by honest zone doors (`18`, `19`) instead of ladders, which the maze already proves.

### 3.6 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 06 | camera on 06 | `$AA` / `$A7` program |
| CP2 | 0C | camera on 0C (tide init) | `$AA` / tide palette |
| *(CASUAL)* | 03 | camera on 03 (the sky ruins) | `$AA` / `$A6` |
| *(CASUAL)* | 0A | camera on 0A (the black zone) | black-zone palette |
| *(CASUAL)* | 11 | camera on 11 (the shaft) | tower palette |
| Shutter | 16 (main), 1B (secret) | shutter entry | |

### 3.7 Secrets

#### 3.7.1 Secret exit: ZONE 100 `[new-code S · Must]`

- **Gate:** in ZONE 15 (0E), press UP at the barnacled `100` door **while the tide is at its lowest**. The screen script
  reads the tide variable (`$069C`, vanilla): the door is open only in the bottom 16 px of the tide's travel plus the GP
  dwell (about 90 f in each cycle).
- **Tell:** the door is in plain sight on the room's floor; a tide line is painted across its frame at exactly the open
  level; while it is shut, bubbles stream from it and UP plays a "locked" thunk. CEN-13 the first time it opens.
  Atlantis players know the legend of warping deep.
- **Fallback** (if the dwell can't be added while the tide's logic still runs in the IRQ): the door opens in the bottom
  24 px of the tide's travel instead, about 96 f in each 244-f cycle.
- **Effect:** 1A → 1B → the secret arena 1C; the kill sets the secret flag.

#### 3.7.2 Hidden room: ZONE 0 (1D) `[new-code S · Must]`

- **Gate:** in the black zone (0A), a door whose plaque reads `0` **glows only while the room is dark**. It sits on a
  ledge reached from a floating stone. Enter it with UP.
- **Tell:** it glows, in a room where glowing is how you find things (the honest door `12` glows the same way). CEN-07
  ("look for what shines"). On a revisit, C.FLASH lights the room and the `0` door disappears for 240 f: its tiles use
  a palette that matches the wall when the room is lit, so "it only shines in the dark" is literal.
- **Contents:** the treasure room of Atlantis: the **sponsor envelope**, a 1-up, a large weapon energy, and a wall
  inscription (story's words; round-1 draft: "ZONE 0: THE ZONE BEFORE THE FIRST. YOU WERE NOT SUPPOSED TO FIND THIS.").
- **Return:** a door `11` leads back to the black zone.

#### 3.7.3 Behaviour-gated chip: CENTURION `[new-code S · Must]`

- **Gate:** free all three **Centurion statues** (00, 05, 09) in one visit with a **full charge** (systems' FULL flag,
  `systems.md` §6.4) in Normal form. Other shots "tink" off the stone. A freed statue stretches, salutes and flies off.
- **Why it is behaviour, not geometry:** #2 needs a swim-jump detour, and #3 is in ZONE 10, which door `11` of ZONE 9
  lets you skip. A player in a hurry misses them.
- **The count:** meta's stage-counter predicate (R1.10); this is the venue's only collect-N secret (R3.1).
- **Tell:** the statues blink; the first shot that tinks off one plays CEN-21 (Must: the tell); CEN-08 when one is freed
  (Should). The debrief hint.
- **Award:** the third statue freed leaves the **chip capsule** on its pedestal.
- **Payoff in the boss fight** (Should): each statue freed this visit lends one charge to a Centurion-bot that hovers at
  the screen's edge and intercepts one pellet or arrow aimed at you (Kid Icarus: Centurions help at the boss). It is the
  same single object as the chip's effect, so it costs one boss-side slot.
- **Effect:** `systems.md` §9.2, CENTURION (when a boss bar fills, a Centurion-bot hovers beside Rock and absorbs the
  first 3 projectiles that would hit him).

#### 3.7.4 Plate T: the sky temple `[engine-ok geometry + new-code S · Must]`

- **Gate:** the vanilla Pegasus gap (14), crossed with the **Jet** (after the 4th win). The gap's numbers are kept
  exactly, so the vanilla measurements still hold: normal jumps fall in, the Jet hovers across.
- **Change from vanilla:** the plate is a **pickup on the sky temple's altar** (19), guarded by its progress bit (the
  Energy Balancer's pattern, `stages_b.md` lessons), instead of a kill in a second boss room, and the route **rejoins
  the main route** by dropping into 15. The vanilla YOU GET line `C.FLRSH AND BEAT T-PARTS` (script `$6B`) still plays
  at the boss kill if the plate was taken this visit, typo and all (BRIEF §6 keeps C.FLRSH).
- **Tell:** from the gap's near edge you can see the temple's gold roof on the far side, and the plate glints on it.

### 3.8 Tileset and art (art_audio §4.8 owns the counts)

- **Kept vanilla CHR:** `$AA` (ruins, water, waterfalls, orange castle) and the water animation (`$DC-$DF`, `$E8-$EF`).
- **New BG** `[new-art M · Must]`: the zone third (doors honest, lying and fake; plaque numerals 0-9 as BG tiles; the
  tablet; the Y-MAN mural; painted tide lines; the tidal shaft's ledges and ladder; the sky temple and its altar).
  Should: the hot spring with steam; the sunken throne.
- **New sprites** `[new-art M · Must]`, vanilla recolours and composites first (R5.1): the cloud platform (Blizzard's),
  the tide float, the Centurion statue and the freed Centurion (2), the T plate. Centaur Man's pinch set: the
  tide-call pose, STUMBLE, the three slot-reel icons. Should: Nasubi Mage (float ×2, cast) and the eggplant; Grim
  Reap-bot (patrol ×2, look, alarm) and Reaplets (2). Could: Eggplant-Rock.
- **Changes for art_audio's re-run** (R5.3): the plaque digits are BG tiles now (not SET-CT1 sprites); the ZONE card's
  digits come with the HUD widget module; the Centurion statue and freed Centurion leave SET-CT2 (Should) for a Must
  set, the Nasubi Mage stays Should; the tower's wrap screens become the shaft's tide rooms (fewer new tiles: they reuse
  `$AA` water).
- **Collision:** vanilla group for stage 7, the tide's collision offset (hard-wired to id 7). Should: the hot-spring
  type (`GRP_ROW`).

### 3.9 Enemies and objects

| Object | Kind | HP (buster taps) | Behaviour | Freeze | Mark |
|---|---|---|---|---|---|
| Pelican spawner `$A9` and pelican `$AB` (drops `$AC`/`$AD` fish), piranha `$C1` (bubbles `$08`), wall cannon `$C9`, seahorse `$C4` (fires `$14` and `$CC`), dome turret `$2B` (fires `$2E`), spearman `$70`, jester head `$10` | vanilla | as vanilla | as vanilla; every projectile and bubble is a stage object in the counts above. The seahorse dies to KNIGHT.C (the featured-enemy tell) | per tech's audit | `[engine-ok]` |
| **Zone door** (honest / lying / fake), **ZONE 100 door** | new (BG + script table) | - | §3.3, §3.7.1 | - | `[new-code M · Must]` |
| **Cloud platform** | new (shared) | - | as Blizzard | NF | `[new-code S · Must]` |
| **Tide float** | new | - | rides the water line | NF | `[new-code S · Must]` |
| **Centurion statue** | new | immune except to a full charge (the FULL flag); then freed | §3.7.3 | NF | `[new-code S · Must]` |
| **T plate** | new (progress-bit pickup) | - | §3.7.4 | - | `[new-code S · Must]` |
| **Nasubi Mage** | new | 4 | floats in a figure-8; every 150 f throws an eggplant in an arc (tell: raises his staff 20 f); the eggplant does 2. *Could:* it **curses** you instead: 6 s as Eggplant-Rock (walk and jump only, no shots, no menu); water or the hot spring cures it early | H | `[new-code S · Should]`; curse `[new-code M · Could]` |
| **Hot spring** | new floor | - | water with steam; standing in it heals 1 HP every 30 f and cures the curse | - | `[new-code S · Should]` |
| **Grim Reap-bot** | new | 8 | patrols at 0.5 px/f; every 120 f stops and looks around (20 f, the tell) and turns; sees 64 px ahead (±24 px vertically). **On sight:** a siren, he flashes red, and 2 **Reaplets** (1 hit each, home at 0.75 px/f, contact 2) dive in from the top. Contact 4 | H | `[new-code S · Should]` |

### 3.10 Boss: Centaur Man, "the Temple of Tides" (17)

**Arena:** a temple hall with the **tide** running (chain `$14` in a stage-7 room, so the collision offset works as it
is) plus the GP dwell. At low tide the floor is dry; at high tide the water covers the lower 60 px and everyone swims
(floaty jumps for Rockman; Centaur Man gallops at reduced speed). Boss-side objects ≤ 3.

**Intro (90 f):** he gallops in, rears, and a placard pops over his head reading his specialty as a question mark (the
vanilla data panel says ABILITY UNKNOWN; the pinch pays it off).

**Pattern loop (HP 28 to 10):** he picks by the tide: GALLOP at low tide, TIME FLASH at high tide, BLINK & BURST in
between. About 480 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **GALLOP** | rears, neighs, 20 f | charges across at 4 px/f (2.5 in water), turns at the wall (12 f), charges back | 20 + ~64 + 12 + ~64 | jump him; easy at high tide, so he saves it for low tide |
| **BLINK & BURST** (vanilla move) | fades out, 16 f | reappears 48 px from you, on your facing side, and fires a shot (2 px/f) that bursts after 40 f into **3 pellets** in a fan (round 1 had 6: R1.8) | 16 + 16 + 40 + 20 | move away from the burst point; C.FLASH's tap ("hits everything"), shown |
| **TIME FLASH** | raises his arms; three clock ticks, 30 f | one screen flash (4 f; a fade under REDUCED), then **time stops for 60 f**: you and the projectiles freeze, greyed. He trots to the far side and sets **3 arrows** in the air aimed at where you stand. Time resumes: the arrows fly at 3 px/f | 30 + 4 + 60 + 40 | the arrows start at least 64 px away: jump or swim out of the line. **C.FLASH's alt (Time Stop), shown** |

**Pinch (HP ≤ 9): ABILITY UNKNOWN.** A three-icon **slot reel** appears over his head (WAVE / FLASH / GALLOP), spins
40 f, stops, and the icon stays up for 30 f (the tell). Then:

- **WAVE**: the tide jumps to its maximum for 180 f and a current pushes you toward the far wall at 0.5 px/f while he
  fires BLINK & BURST twice (the second after the first's pellets are gone).
- **FLASH**: two TIME FLASHes, the second after the first set of arrows has left the screen (flashes at least 4 s
  apart, R3.5).
- **GALLOP**: three charges at 5 px/f.

Between spins he does BLINK & BURST. CEN-19.

**Damage and i-frames:** `systems.md` Tables 1-2 (Centaur's column: KNIGHT.C 4 W with 16 f; SILVER.T 3 G; Y.SPEAR 1 R;
C.FLASH his own). SC2 (Should, systems): he gallops through Time Stop.

**WEAK reaction, STUMBLE** (SC9, Must): a KNIGHT.C hit buckles his front legs: he kneels for 40 f (WEAK! pop, CEN-17).

**Own-weapon reaction, SAY CHEESE** (SC4, Should): the first C.FLASH does 0: he strikes a heroic pose for 60 f, as if
for a camera flash (CEN-18). Free hits for 60 f, once per fight.

**Centurions** (Should): each one freed this visit intercepts one pellet or arrow (§3.7.3).

**Forms** (refights): Jet hovers above the tide's surface (GALLOP can't reach it; arrows can). Power: a charged punch to
his flank during a GALLOP turn knocks him over for 30 f.

**VENUE ACT** (systems §6.5): **NO WRONG DOOR**: clear the maze without using a lying or a fake door.

**Fight loader** (W2): the arena's screen script starts the tide itself (`EFFECTS` TIDE with its dwell), and the stage id
is still 7, so the collision offset holds; the pinch threshold comes from the per-fight byte.

**Credits mode** (fortress §6.2; `IFCREDITS`, tech §4.6): room 17's screen script starts the tide as in a fight (stage
id 7), and he still picks his moves by the tide. BLINK & BURST reappears 48 px from a fixed mark, and TIME FLASH has no
one to freeze: its one 4-f flash plays (a fade under REDUCED, at least 4 s apart) and the 3 arrows fly at the mark. No
slot reel (no pinch), no reaction. Fallback: his card strip only.

### 3.11 Secret arena (1C)

- **v1.0 (Must):** the Temple of Tides again, in the vanilla revisit palette (bank `$28`), tide running. Same fight; the
  kill sets the secret flag.
- **v1.1 (Should): THE SUNKEN THRONE** `[new-code S · Should]`. The throne room of Atlantis, entirely underwater (no
  tide: water everywhere, floaty jumps all fight). Centaur Man fights as a **sea-centaur** (the vanilla sprite in a
  sea-green palette with a fish-tail overlay, one boss-side object). GALLOP becomes a **looping swim charge** (a
  diagonal figure-8 across the room at 3 px/f). Two vents in the floor alternate every 240 f, pushing you sideways at
  0.5 px/f (tell: bubbles 30 f before). His pinch reel gains a fourth icon, **WHIRLPOOL** (a current that circles the
  room for 180 f). New music G30 UNDERWATER is Could.

### 3.12 CASUAL levers (Must) and HARD pokes (Should)

**CASUAL** (R2.9; `systems.md` §13.4's lever table):

| Lever | Where (screen, object) | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | Centaur Man's TIME FLASH ticks; his BLINK fade (17, 1C) | 30 f; 16 f | 60 f; 32 f | `REFLEX` |
| mash | none | - | - | - |
| timer | the tide's dwell (0C-0E, 10-12, 17, 1C) | 60 f | 90 f | `TIERVAL` on `EFX_PARAM` |
| checkpoint | sky ruins, maze, shaft | CP1 06, CP2 0C | + 03, 0A, 11 | dormant checkpoint objects woken by a CASUAL poke |
| secret step | the ZONE 100 door (0E) | open in the bottom 16 px of the travel | the bottom 24 px | `IFCASUAL` in the door's script |
| secret step | CENTURION (00, 05, 09) | a full charge frees a statue | a half charge does too | `IFCASUAL` in the statue |

**HARD** (Should, v1.1):

| Section | Poke | Kind |
|---|---|---|
| Maze 07, 0B | lying doors send you to **ZONE 1** (00), as Atlantis would; the checkpoint is still 06 | door table |
| Maze | fake doors bite: 2 dmg | door table |
| Tide 0C-0E, shaft | dwell 60 → 30 f; the tide moves 1 px per frame instead of every other frame | param |
| ZONE 100 | the open window shrinks with the dwell | (follows) |
| Shaft 10-12 | one tide float removed from each room | object list |
| T route 18 | one landing island removed (fuel discipline) | layout poke |
| Boss | pinch at HP ≤ 14; time stop 60 → 90 f; pellets 2 → 2.5 px/f | AI branch |
| (v1.1 content) | Reap-bot sight 64 → 96 px; eggplant curse 6 → 10 s | param |

### 3.13 Commentator hooks (ids; the words are story §6.3's)

| Id | Trigger | Tier (R4.5) |
|---|---|---|
| CEN-01 | match card ends | Should |
| CEN-02 | first ZONE card | Should |
| CEN-03 | first door | Should |
| CEN-04 | the tablet (06) | Should (the tablet's own text is the Must tell) |
| CEN-05 | a lying door used | Should |
| CEN-06 | a fake door bonked | Should |
| CEN-07 | the black zone | **Must** (ZONE 0's tell) |
| CEN-08 | a Centurion freed | Should |
| CEN-09 | first eggplant (or the curse, Could) | Should |
| CEN-10 | first hot spring | Should |
| CEN-11 | Reap-bot alarm | Should |
| CEN-12 | first high tide | Should |
| CEN-13 | ZONE 100 opens | Should |
| CEN-14 | the snake-crested jester head | Should |
| CEN-15 | Jet over the gap | Should |
| CEN-16 | T plate taken | retired: story §6.2's plate lines cover it |
| CEN-17 | first KNIGHT.C hit (`EV_WEAK_FIRST`) | **Must** |
| CEN-18 | C.FLASH on Centaur Man (SAY CHEESE) | Should (with SC4) |
| CEN-19 | pinch reel | Should |
| CEN-20 | YOU GET C.FLRSH | Should |
| **CEN-21** (new) | first shot that tinks off a statue ("That statue... blinked?") | **Must** (CENTURION's tell) |
| **CEN-22** (new) | first time the shaft's water lifts Rock onto a ledge | Should |

**Death lines** (Must: 4): story's lines 1-4 are recommended. Line 5 needs the eggplant curse (Could); line 6 names Kid
Icarus's hero and breaks R3.3, so it goes.

### 3.14 Judges' debrief hints (tier B drafts: meta §4.4 asked this doc for them; story owns the words)

In meta's weight order (exit, room, item, plate). Set in capitals at build time; each fits 4 × 28:

1. CE0, exit: "THE ZONE 100 DOOR IN ZONE 15 ONLY OPENS AT THE LOWEST TIDE. WAIT FOR THE WATER TO DROP."
2. CE1, room: "IN THE BLACK ZONE ONE DOOR ONLY SHINES IN THE DARK. DON'T LIGHT THE ROOM. CLIMB TO IT."
3. CE2, CENTURION: "THREE STONE SOLDIERS IN THE RUINS ARE NOT STATUES. A FULL CHARGE WAKES THEM UP."
4. CE3, plate T (JET): "BEAT'S T-PLATE RESTS IN A TEMPLE PAST THE PEGASUS GAP. YOU NEED WINGS, OR A JET."

### 3.15 How crazy it gets

1. Every room has a ZONE number, and a door in ZONE 12 sends you back to ZONE 8.
2. A door labelled 99 that lies, and a door labelled 0 that only exists in the dark.
3. The tide is an elevator: wait for high tide and swim up to the ledge.
4. A drowned tower floods under you as you climb it.
5. Centaur Man's ABILITY UNKNOWN turns out to be a slot machine over his head.
6. Centaur Man freezes time and lines up three arrows while you stand there greyed out.
7. *(v1.1)* He poses for C.FLASH like a camera flash.
8. *(v1.1)* Three stone soldiers you freed fly in to block his arrows.
9. *(v1.1)* A Grim Reap-bot with a siren. *(Could)* Rockman turned into an eggplant, soaking in a hot spring.

### 3.16 Revisits and VARIETY

- **Taps (v1.0):** C.FLASH lights the black zone for 240 f (and hides the `0` door: it only shines in the dark).
  KNIGHT.C and SILVER.T arc over the shaft's ledges.
- **Ice Block (v1.0):** a block placed on a shaft ledge is a step at low tide.
- **Alts (v1.1, Should):** Time Stop **freezes the tide** (stop it at low water and walk into ZONE 100 at leisure);
  Y.SPEAR's Wall Spear reaches 0D's ledge and the shaft's ledges at any tide. Proposal for systems: an Ice Block placed
  in water **floats** and rides the tide (a lift at any tide).
- **Tag partner (Should, cut-line item 2, with the tag partner):** Break Man's shield blocks the Reaplets while
  jumping; the optional shortcut is a cracked pillar in 0F that only his double knockback topples into a bridge.
- **Par** (placeholder): 300 s.

---

## 4. Yamato Man: EDO NINJA ROW (stage `$04`)

### 4.1 The pitch

*The Impregnable Fortress* (vanilla's location), with an Edo town at its feet. You start under Mt. Fuji (vanilla's
one-screen vista), cross the town's rooftops **bonking ninjas from below** through the floorboards, and break into a
ninja mansion whose hanging scrolls **spin you through the walls**. Inside the keep a giant **daruma otoshi** waits to
be knocked apart block by block (never touch the head), and the caltrop hall is crossed on a **spear pogo**. In the
last hall before Yamato Man, five scrolls hang perfectly still, but a paper lantern's flame leans toward one of them:
**follow the draft** and the wall spins you backstage at a kabuki theatre, the secret route. Vanilla's two side routes
stay: the **charged-punch bypass** to GAMARN & GAMADAYU's dark room, and the **Jet ledge** to Beat's **E plate**, now on
the castle roof.

**The trim (R3.2, design-25).** Round 1 stacked three homages and four cultural set pieces into 30 screens. Cut: the
**kite run** (19 becomes plain sunset roofs) and, by this doc's choice between the two that R3.2 offered, the **sekisho**
with its three travel passes, the runner ninja and the PASS counter. The bonk-stun stays: it rides the ceiling probe
Blizzard already needs, so it costs a few lines, and it is the town's whole identity. The sekisho was the costlier
piece: it repeated Tomahawk's "a guard counts 3 items" gate (design-5 f), and it was the venue's collect-N secret. The
secret exit becomes the scroll gate alone (R3.1). The **hanabi** that lit the dark room on a timer are cut too (R3.1:
only the Riot keeps lights on a timer). **The pogo, the Daruma and (from v1.1) the nightingale floor carry the venue.**

| Homage (design notes) | Here | Mark |
|---|---|---|
| *Jajamaru*: knock enemies out from below, through the floor | **bonk-stun**: the ceiling probe stuns the enemy standing on the bonked cell for 90 f | `[new-code S · Must]` |
| Ninja houses: hidden passages | **hanging scrolls** that spin (donden-gaeshi), tell = they flutter in a draft; the **draft** gate | `[new-code S · Must]` |
| Daruma otoshi (the toy) | **the Daruma** mini-boss (T8, two parts) | `[new-code M · Must]` (DARUMA is Must, R2.5) |
| *DuckTales* (Capcom): the pogo cane; treasure found by pogoing a spot | the **spear pogo** set piece over caltrops; **pogo the crest** = the hidden room | `[new-code M · Must]` |
| Castle lore: the nightingale floor (*uguisubari*), the hanging-ceiling trap | **nightingale floor** + Knight's spike ceiling, re-homed (chain `$11`) | `[new-code M · Should]` (v1.0: a plain gold hall) |
| Kabuki: the revolving stage, the trapdoor, the shouted names | **the kabuki stage** secret-arena twist | `[new-code S · Should]` |
| *Goemon*: three travel passes for the sekisho | cut (R3.2) | Won't (v1) |
| Kites over the town | cut (R3.2) | Won't (v1) |
| Edo fireworks ("Tamaya!") lighting the dark room | cut (R3.1: one lights-on-a-timer set piece in the game, the Riot's) | Won't (v1) |

### 4.2 Map shape

```
00 Fuji street ─> 01 rooftops ─> 02 JUNCTION ──(charged punch)──> 0C kura ─> 0D down ─> 0E DARK ROOM (Gamarn & Gamadayu) ─> 0F E-tank ─up─> 09
                                  │ up
                                  03 floors ─> 04 rafters ─> 05 GOLD HALL (v1.1: NIGHTINGALE FLOOR) ─> 06 SCROLLS ─> 07 down ─> 08 shoji
   09 [CP1] ─> 0A courtyard ─> 0B JUNCTION ──(Jet: high ladder)──> 18 sunset roofs ─> 19 sunset roofs ─> 1A castle roof (E plate) ─drop─> 15
                                  │ down
   10 armory ─> 11 DARUMA [CP2] ─> 12-13 CALTROP HALL (pogo; crest ─trapdoor─> 1E hidden room) ─> 14 HALL OF SCROLLS
          ├─ main door ─> 15 shutter ─> 16 BOSS
          └─ the draft (a scroll) ─> 1B backstage ─> 1C hanamichi shutter ─> 1D SECRET ARENA
```

Screens used: main 00-16 (23, including the bypass 0C-0F), E route 18-1A (3), secret 1B-1D (3), hidden room 1E (1) =
**30 of 32**. Spare: 17, 1F. Vanilla used 30 (`stages_b.md` §2).

### 4.3 Screen by screen

Brackets: peak stage objects (≤ 4, §0.2; in the pogo hall, where Rock fires nothing, ≤ 7). The samurai `$A2` takes all
96 enemy tiles, so samurai screens get nothing new beside it (art_audio §4.5).

| Scr | What the player does | Stage objects [peak] | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Match card. **Mt. Fuji** over the castle-town skyline; an Edo street of shopfronts. A notice board holds the **WANTED** poster (`MR. Y - 1,000,000 RYO`: the Mr. Y gag, BG) | lantern robot `$C2` (+ fireballs `$C3` ≤ 2) [3] | | vanilla v00 vista (CHR `$97`; its Fuji third is only valid here, `stages_b.md` §6). YAM-01, YAM-02 |
| **01** | Rooftop run. **Jaja-nin** ninjas stand on the thin roof floors above you: jump into the floor tile under one and it is **stunned 90 f** (Jajamaru); stunned ninjas take double damage | Jaja-nin ×2 + shuriken ≤ 2 [4] | | the ceiling-probe callback. YAM-03 |
| **02** | **JUNCTION** (vanilla): ladder up to 03 (main), or a **Power block** in the right wall (charged punch) → the bypass 0C | Jaja-nin ×1 + shuriken [2] | | vanilla breakable ids `$38-$3B` kept; the venue's cracked Power-block art is the tell |
| **03** | Up through the mansion's floors: thin wooden floors with gaps, ninjas on each; bonk your way up | Jaja-nin ×2 + shuriken ≤ 2 [4] | | up exit (ladder at the top), CHR `$98` (vanilla interior) |
| **04** | **The rafters**: ninjas drop from the rafters to the floor and hop back; the bonk lesson, harder | Jaja-nin ×2 + shuriken ≤ 2 [4] | | |
| **05** | **v1.0: the gold hall**: a long hall of gold floorboards with a samurai at the far end. *v1.1 (Should): THE NIGHTINGALE FLOOR (§4.5.1)* | samurai `$A2` (+ spear) [2] | v1.1: ceiling spikes (deadly) | v1.1: YAM-06, YAM-07 |
| **06** | **THE SCROLL ROOM.** Three hanging scrolls. Two **flutter** (a draft behind them): UP in front of one and the wall **spins** (donden-gaeshi, 24 f) and puts you on its other side. Scroll A hides a closet with a large weapon energy; scroll B is a shortcut down to 08. The still scroll is just a scroll (YAM-09) | shuriken robot `$69` ×1 (+ shuriken), the closet's energy [3] | | YAM-08. The lesson the secret exit pays off |
| **07** | Down through a shoji shaft: a shuriken robot, a bubble cluster | `$69` ×1 + shuriken, bubbles `$25` ×1 [3] | | down exit |
| **08** | **Paper walls**: shoji panels (collision `$D` → `$19` in group 2) hide two pockets that **F.BLAST burns open** on a revisit (a 1-up, a large weapon energy) | samurai (+ spear) [2] | | `[engine-ok]` |
| **09** | **CHECKPOINT 1** (vanilla set it on v09 for v0A). The bypass rejoins here from 0F | none [0] | | |
| **0A** | The castle courtyard: stone lanterns and a lantern robot on the wall | lantern robot (+ fireballs ≤ 2) [3] | | |
| **0B** | **JUNCTION** (vanilla): ladder **down** to 10 (main), or the **high ladder** in the top right, above a ledge 64 px over the floor: **Jet only** → 18 (E route). A banner painted with an "E" flutters above the ledge (BG) | none [0] | | vanilla gate geometry kept exactly (only the Jet reaches it). The banner replaces round 1's E kite |
| **0C** | *Bypass.* The storehouse (kura): rice bales, a samurai | samurai (+ spear) [2] | | CHR `$99` (vanilla dark bypass) |
| **0D** | *Bypass.* Down into the cellar | none [0] | | sprite set `$61` for the mid-boss (vanilla) |
| **0E** | *Bypass.* **THE DARK ROOM: GAMARN & GAMADAYU**, vanilla's mid-boss (the frog mech and its ninja rider, 14 + 15 HP) in vanilla's dark palette `$B9`, kept as it is: no timed lights (R3.1) | Gamarn, Gamadayu, low shots `$D8` ≤ 2 [4] | 2 pits in the dark | YAM-15's first half (Should). C.FLASH's tap lights the room for 240 f (systems) |
| **0F** | *Bypass.* The E-tank pocket behind a second Power block (vanilla ids `$3C-$3F`); up exit to 09 | E-tank [1] | | vanilla |
| **10** | Down into the keep's armory: an eye cannon, spring flowers | eye cannon `$54` (+ shot), spring `$5F` ×1 [3] | | vanilla v10-v11 enemies |
| **11** | **THE DARUMA** (§4.5.3; the mini-boss locks the screen). **CHECKPOINT 2** after it | Daruma head + stack, a knocked-out block, a fortune slip [4] | | T8. YAM-10 (Must: DARUMA's rule), YAM-11, YAM-12 |
| **12** | **THE CALTROP HALL**: a floor of caltrops (spikes, `$F`). A **pogo spear** stands in a rack at the entrance: touch it and it replaces the buster (§4.5.2). Hold DOWN in the air: pogo; bounce on caltrops and on enemies (3 dmg). One floor cell bears a **gold crest** (§4.6.2) | propeller lantern `$24` + rotor `$26` (+ its ball), Jaja-nin ×1 (+ shuriken) [5] (Rock fires nothing here: cap 7) | caltrops (deadly without the pogo) | YAM-13 |
| **13** | Caltrop hall 2: pogo across ashigaru heads. A rack at the end takes the pogo back. *v1.1 (Should): three bell towers; ringing a bell with the pogo bounces you 72 px* | ashigaru ×3 [3] (v1.1: + bells ×3 [6]) | | the pogo can't leave 12-13 |
| **14** | **THE HALL OF SCROLLS** (§4.6.1): five scrolls hang perfectly still along the back wall; a paper lantern (andon) stands on the floor, its flame leaning toward one of them. The main door → 15 | lantern flame, ashigaru ×1 [2] | | the secret exit. YAM-21 (Should) |
| **15** | Shutter corridor. **Boss checkpoint.** The E route drops in here | none [0] | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room** (§4.8) | Yamato Man [boss + ≤ 3] | | |
| **18** | *E route.* Edo rooftops at sunset: vanilla's pink sunset windows (v1A-v1D art and its animated CHR sets `$9A-$9C`) | Jaja-nin ×1 (+ shuriken), beetle `$75` (+ the walker it spawns) [4] | | |
| **19** | *E route.* More sunset roofs (the kite run is cut, R3.2): rooftop islands to land on while the Jet's fuel regrows | Jaja-nin ×1 (+ shuriken), beetle (+ its walker) [4] | pits | |
| **1A** | *E route.* The castle roof: a golden **shachihoko** (the carp ornament) holds **Beat's E plate** (§4.6.4). A hatch drops you into 15 | E plate [1] | | story §6.2's plate line |
| **1B** | *Secret.* **Backstage** at the kabuki theatre: prop flats as platforms. *Could: kuroko stagehands carry the platforms* | ashigaru ×2 [2] | | |
| **1C** | *Secret.* The **hanamichi** (the runway through the audience): shutter corridor, checkpoint | none [0] | | |
| **1D** | **SECRET ARENA** (§4.9) | Yamato Man | | |
| **1E** | **Hidden room: the treasure vault** (§4.6.2) | envelope, E-tank [2] | | |

### 4.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 09 | camera on 09 (vanilla script `$2F`, moved one screen) | `$97` + `$98` / `$5B` |
| CP2 | 11 | the Daruma's defeat | keep palette |
| *(CASUAL)* | 04 | camera on 04 (the mansion) | `$98` |
| *(CASUAL)* | 0E | camera on 0E (the bypass's dark room) | `$99` / `$B9` |
| *(CASUAL)* | 12 | camera on 12 (at the pogo rack, so a respawn always has the pogo in reach) | keep palette |
| Shutter | 15 (main and E route), 1C (secret) | shutter entry | |

### 4.5 The set pieces

#### 4.5.1 The nightingale floor (05) `[new-code M · Should]` (v1.1; the venue's second set piece)

- **Floor:** a new floor type in Yamato's collision group (group 2, through `GRP_ROW`), the gold boards. Every 24 px
  walked, and every landing, plays a chirp and posts a "chirp" event. A slide (2.5 px/f) never chirps; nor does the Jet
  in flight.
- **Ceiling:** Knight's descending spike ceiling (IRQ chain `$11`, handler `$3E:$C337`; the collision offset through
  `$069C`, `$3E:$DA40`), re-homed through the stage-attribute table's `CEILING` effect and `RL_CEILING`. Vanilla lowers
  it steadily; here **each chirp lowers it 8 px** (over 8 f), and after 60 f without a chirp it rises 1 px every 4 f
  (walking chirps every ~18 f, so a walker never gets that respite). The ceiling starts 112 px up: walk the whole floor
  and it is down to about 32 px, too low to jump the samurai's spears at the far end. **Slide and it never moves.**
- **The lesson:** slide = quiet. Normal Rockman crosses it untouched; Power Rockman can't slide and must hurry; Jet
  Rockman hovers. Fallback if the chain can't be re-homed: a row of sprite spike blocks that drop on chirps.
- **v1.0** ships 05 as the plain gold hall of §4.3; nothing else depends on it.

#### 4.5.2 The pogo (12-13) `[new-code M · Must]` (the homage mechanic)

- A set-piece weapon on tech's GP player states: touching the rack's pogo spear replaces the buster until the rack at
  13's end (4MI's Quint pogo, `r4mi/stages_a.md` §3). B does nothing while you carry it (no shots: you bounce your way
  through), which is why the hall's lag cap is 7.
- **The body** (R2.3, feasibility-8): the pogo poses live in a **dedicated set-piece player sheet** (`gp_player_sheet`) streamed while the
  rack's 24-f "take" animation plays (a locked moment: Rock stands still), and streamed back at the return rack. They are
  never in the 15-tile weapon slot.
- **Hold DOWN in the air** to pogo: landing on caltrops or on enemies **bounces** you with `systems.md` §3.2's Pogo
  numbers (vy `$FB.00`, or `$FA.CC` with A held). Landing on an enemy does 3 damage. Without DOWN held, caltrops are
  deadly as usual.
- **Shared code:** the v1.1 Y.SPEAR Power synergy (Should) is this same pogo, everywhere: the venue teaches it before
  the player owns it.

#### 4.5.3 The Daruma (11) `[new-code M · Must]` (T8; DARUMA's set piece)

- **Body:** a stack of **five coloured blocks** (32×16 each) under the **head** (32×32, a daruma face with one eye
  painted). Two T8 parts, for the lag cap: **the head is the controller** (it owns the boss bar), and **the stack is one
  part** drawn as one metasprite with one tall hit box. When the stack's latch fires, it reads the Y of the shot that hit
  it and picks the block whose band holds that Y.
- **The head** wobbles side to side and every 120 f spits a **fortune slip** that flutters down (tell: its cheeks puff
  for 20 f): "VERY BAD LUCK" (`大凶` drawn as art), 3 dmg.
- **Daruma otoshi:** a hit on a block's side **knocks that block out**: it slides across the floor at 3 px/f, bounces
  off the wall once and vanishes (3 dmg on contact: jump it), and the stack drops 16 px. At most one block slides at a
  time; a block hit while another slides just dinks.
- **Hitting the head** makes it **angry** (red): it hops off the stack and bounces around the room for 180 f (contact
  4), then hops back on.
- **The rule that makes it a game:** Rockman's buster shot spawns 1 px above his centre Y, about 12 px above his feet
  (measured, `build/design/design-venues-b/measure.py`), which is inside the *bottom* block (0-16 px). **Shoot from the
  floor** and you always hit the lowest block; the stack comes down to meet your shots. **Jump-shoot** and you hit
  higher, and eventually the head. The fortune slips are what tempt you to jump.
- **End:** when the last block is out, the head lands on the floor and the fight is won (CP2).
- **Lag:** head + stack + one sliding block + one slip = 4 stage objects.
- **Fight id:** a mid-boss fight id from meta (consistency-44 proposes `$10`; GAMARN & GAMADAYU `$0F`).

### 4.6 Secrets

#### 4.6.1 Secret exit: the draft (14) `[new-code S · Must]` (R3.1 "the scroll gate alone", R3.2)

- **Gate:** in the hall of scrolls (14), five scrolls hang perfectly still. A paper lantern on the floor burns with its
  flame **leaning toward one of them** (a 2-frame flicker sprite, tilted). UP at that scroll (R2.10) spins the wall as
  on 06 and puts you backstage (1B). UP at any other scroll: nothing (YAM-09, Should).
- **Tell:** 06 taught that a scroll with a draft behind it turns. Here the draft is too faint to stir the paper, but the
  flame shows it. No other lantern in the venue leans. The debrief hint names the lantern.
- **Fair by design:** a player who presses UP at all five scrolls finds it too. That is intended: checking the walls is
  the ninja-house game, and five tries cost seconds.
- **Effect:** 1B → 1C → the secret arena 1D. Beating Yamato Man there clears the venue and sets the secret flag.

#### 4.6.2 Hidden room: the treasure vault (1E) `[new-code S · Must]`

- **Gate:** in the caltrop hall (12), **pogo-land on the gold crest** (a single floor cell among the caltrops). The cell
  is a T6 trapdoor: it opens and you drop into 1E (DuckTales: treasure found by pogoing the right spot).
- **Tell:** the crest glints every 2 s, the only shiny cell in a floor of caltrops, right where the pogo makes you look
  down. The debrief hint names it outright.
- **Contents:** a vault of gold koban (BG), the **sponsor envelope** and an E-tank, and a sign with Mr. Y's "the gold is
  a loan from the tournament" joke (story's words). Round 1's 100-bolt chest is gone (R2.7).
- **Return:** a ladder up into 12, with the pogo still in hand.

#### 4.6.3 Behaviour-gated chip: DARUMA `[new-code S · Must]`

- **Gate:** win the daruma otoshi (11) **without ever hitting the head**.
- **Tell:** YAM-10 says the rule as the fight starts (Must: the tell); the head has only one eye painted; YAM-11 when you
  hit it (Should).
- **Award:** the head lands on the floor and **paints its second eye** (a daruma's wish fulfilled; a brush stroke and a
  chime, with a vanilla SFX as the fallback), then the chip capsule appears beside it.
- **Effect:** `systems.md` §9.2, DARUMA (once per life, a hit that would kill at HP ≥ 2 leaves 1 HP; 2 slots). It is
  one "second wind" family with YASHICHI: the two can't be equipped together (R2.6).

#### 4.6.4 Plate E: the castle roof `[engine-ok geometry + new-code S · Must]`

- **Gate:** vanilla's: the high ladder on 0B, above a ledge 64 px over the floor, needs the **Jet** (the Go-Explore test
  never reached it in Normal form, `stages_b.md` §6).
- **Change from vanilla:** the plate is a **pickup** on the shachihoko (1A), not a kill in a second boss room, and the
  route **rejoins** at 15. The vanilla YOU GET line `Y.SPEAR AND BEAT E-PARTS` (`$68`) plays at the boss kill if the
  plate was taken this visit.
- **Tell:** the banner painted with an "E" over 0B's ledge; from 0A the shachihoko gleams on the castle roof in the
  backdrop.

### 4.7 Tileset and art (art_audio §4.5 owns the counts)

- **Kept vanilla CHR:** `$97` (the Fuji vista for screen 00, red riveted castle walls, green panels, pipes, shoji,
  purple pillars), `$98` (interiors), `$99` (the dark bypass), the plate route's sunset windows with their animated sets
  `$9A-$9C`, sprite set `$61` (GAMARN & GAMADAYU). Palettes `$57-$5E`, `$B9`.
- **New BG** `[new-art M · Must]`: the Edo third (shopfronts with noren curtains, kawara roof tiles, the notice board
  and WANTED poster, tatami, three hanging-scroll designs with a 2-frame flutter, the "E" banner) and the castle third
  (the caltrop floor and gold crest, the treasure vault, the shachihoko, the theatre curtain and stage for 1D). Should:
  the gold nightingale boards; the audience and the set flats of the revolving stage.
- **New sprites** `[new-art M · Must]`, vanilla recolours and composites first (R5.1): Jaja-nin (hop, throw, stunned)
  and the shuriken; ashigaru (3); the paper-lantern flame (2); the Daruma (stack frames, head with one eye and two eyes,
  angry head, fortune slip) and the pogo rack. **The player's pogo frames (2) go in the set-piece player sheet** (R2.3),
  not in the Y.SPEAR weapon set. Yamato Man's pinch set: the flying kabuto and the topknot frames. Should: bells (2).
  Could: kuroko (2).
- **Changes for art_audio's re-run** (R5.3): **removed** (Won't, R3.2/R3.1): the runner ninja and his pass, the sekisho
  gate and guard, the kite and the kite ninja, the hanabi spark and burst. **Promoted to Must:** the Daruma and the pogo
  rack (art had SET-YM3 as Should); the pogo poses move from the weapon slot to the set-piece sheet. **Added:** the
  lantern flame and the "E" banner.
- **Collision:** group 2 as vanilla (`$D` → `$19` for the shoji, `$B` Power blocks), plus the T6 crest cell. Should: the
  nightingale type.

### 4.8 Boss: Yamato Man, "the impregnable" (16)

**Arena:** a castle hall: a tatami floor, two short ledges at the sides (48 px up), wooden walls. Boss-side objects ≤ 3.

**Intro (90 f):** he bows in full armour; the panel's `MOBILE 31` blinks.

**Pattern loop (HP 28 to 15):** RUSH → VAULT → RUSH → WALL SPEARS, about 560 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **SPEAR RUSH** (vanilla move) | stamps a foot, "Ei!", 16 f | runs across the room (x `$21-$DE`) at 3 px/f, spear lowered (tip 16 px ahead, 4 dmg), stops at the wall for 16 f | 16 + 64 + 16 | jump over; PUNCH★ **clashes** with the spear: both knocked back 16 px, he is stunned 20 f |
| **VAULT & RAIN** (vanilla move) | plants the spear, 12 f | **pole-vaults** to y `$38` and at the top throws a **3-way spread** of spearheads down (vanilla `$B4`, 2.5 px/f); lands, 24 f | 12 + 40 + 24 | stand between the heads; this is the Y.SPEAR tap, and the vault is the **pogo**, both shown |
| **WALL SPEARS** | draws two spears, 16 f | throws them into the left and right walls (heights 48 and 80 px). Each one that sticks becomes **a solid spear-shaft cell in the wall for 240 f** (a map edit: no slot once stuck). Then GROUND THRUST: spear raised overhead 20 f, slam: two shockwaves (16 px tall, 3 px/f) run along the floor both ways | 16 + 20 + 20 + 60 | **stand on his spears** (the Wall Spear alt, shown), or jump the waves |

**Pinch (HP ≤ 14, half his bar): HELMET OFF.** His kabuto pops off and **bounces around the room** for 180 f (16×16,
2 px/f, off the walls, 3 dmg), showing a topknot. From now on RUSH runs at 4 px/f and VAULT throws its 3 heads at
3 px/f; while the kabuto bounces, VAULT throws 2 (lag). The commentators read his new stat off the card: `MOBILE 99`
(YAM-18).

**Ashigaru** (Should): at HP 18 and HP 9 he whistles (20 f) and two ashigaru-bots march in from the shutter side (2 hits
each); while they are up he only RUSHes (lag).

**Damage and i-frames:** `systems.md` Tables 1-2 (Yamato's column: SILVER.T 4 W with 16 f; PLANT.B 3 G; KNIGHT.C 1 R;
Y.SPEAR his own). He may still throw volleys himself (systems §15.3).

**WEAK reaction, SNAP** (SC9, Must): a SILVER.T hit chops his spear shaft in two: he stares at the stub for 40 f (no
attacks, WEAK! pop, YAM-16), then pulls a new spear from his back.

**Own-weapon reaction, PARRY** (SC4, Should): the first Y.SPEAR does 0: he catches your spear and throws it back at you
(2 dmg if it hits). YAM-17.

**VENUE ACT** (systems §6.5): **SPEAR DANCER**: cross the caltrop hall from rack to rack without a single normal landing.

**Fight loader** (W2): the wall spears are logged map edits that the arena's script undoes, so the arena resets when
loaded alone; the pinch threshold comes from the per-fight byte.

**Credits mode** (fortress §6.2; `IFCREDITS`, tech §4.6): RUSH, VAULT & RAIN and WALL SPEARS loop as written, aimed at a
fixed mark (the floor at x = 128); the wall spears stick and are undone on their 240-f timer as in a fight. No helmet
(no pinch), no reaction. Fallback: his card strip only.

### 4.9 Secret arena (1D)

- **v1.0 (Must):** the castle-hall fight on a theatre set: the striped curtain (black, persimmon, green) as the backdrop
  and the hall's layout. Same fight; the kill sets the secret flag.
- **v1.1 (Should): THE KABUKI STAGE** `[new-code S · Should]`. Yamato Man **rises through the trapdoor** (*seri*) and
  strikes a *mie* pose to the clack of wooden clappers; the audience shouts `YAMATO-YA!` (a pop-up, YAM-19). The twist
  is the **revolving stage** (*mawari-butai*): every 600 f the clappers sound (a 30-f tell), the curtain sweeps across
  (a 30-f palette wipe) and **the set changes** through the map-edit service's per-id alternate flip:
  - **Set A, the castle hall:** flat, two ledges (the main arena's shape).
  - **Set B, the moat bridge:** two side platforms and the open trapdoor in the middle (48 px, a pit).

  In pinch he pauses for a second *mie*, and the audience goes wild. Everything else is the main fight. *Could:*
  kuroko stagehands wheel props across during each change (harmless; shoot one and the audience boos). Music: G26
  KABUKI (Should).

### 4.10 Enemies and objects

| Object | Kind | HP (buster taps) | Behaviour | Freeze | Mark |
|---|---|---|---|---|---|
| Lantern robot `$C2` (throws `$C3` fireballs), samurai `$A2` and its thrown spear `$A3`, shuriken robot `$69` and its shuriken `$6B`, bubbles `$25`, eye cannon `$54` and its ball `$55`, springs `$5F`, propeller lantern `$24` + rotor `$26`, beetle `$75` (spawns `$2D`), GAMARN & GAMADAYU `$D0-$D8` | vanilla | as vanilla | as vanilla; every projectile and spawn is a stage object in the counts above. The samurai dies to SILVER.T (the featured-enemy tell) | per tech's audit | `[engine-ok]` |
| **Jaja-nin** (ninja-bot) | new | 2 | hops between floors, throws a shuriken every 90 f (tell: a 12-f crouch); bonk-stun 90 f; stunned = double damage | H | `[new-code S · Must]` |
| **Hanging scroll** | new (T3 warp target) | - | flutters (a 2-frame BG animation) if it hides a passage; UP: a 24-f spin, then a teleport through the wall | - | `[new-code S · Must]` |
| **Paper lantern** | new | - | its flame leans toward the turning scroll on 14 | NF | `[new-code S · Must]` |
| **Daruma** | new (T8: head + stack) | blocks 1 hit each; head immune | §4.5.3 | boss | `[new-code M · Must]` |
| **Pogo rack / pogo** | new (GP player state) | - | §4.5.2; the set-piece player sheet | - | `[new-code M · Must]` `[new-art S]` |
| **Crest trapdoor** | new (T6 cell) | - | opens on a pogo landing | - | `[new-code S · Must]` |
| **Ashigaru** | new | 2 | marches at 1 px/f with a short spear poke | H | `[new-code S · Must]` (as the boss's helpers: Should) |
| **Bell** | new | - | a pogo target: bounces 72 px | NF | `[new-code S · Should]` |
| **Kuroko** | new | - | stagehands; harmless; carry platforms (1B) and props (1D) | NF | `[new-code S · Could]` |
| *Runner ninja, travel pass, sekisho gate and guard, kite, kite ninja, hanabi* | - | - | cut | - | Won't (v1) |

### 4.11 CASUAL levers (Must) and HARD pokes (Should)

**CASUAL** (R2.9; `systems.md` §13.4's lever table):

| Lever | Where (screen, object) | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | the Jaja-nin's throw crouch (01-04, 12, 18, 19) | 12 f | 24 f | `REFLEX` |
| reflex | the Daruma's cheek-puff (11) | 20 f | 40 f | `REFLEX` |
| reflex | Yamato Man's RUSH stamp (16, 1D) | 16 f | 32 f | `REFLEX` |
| mash | none | - | - | - |
| timer | the bonk-stun (01-04, 12, 18, 19) | 90 f | 135 f | `TIERVAL` |
| checkpoint | mansion, bypass, keep | CP1 09, CP2 11 | + 04, 0E, 12 (at the rack) | dormant checkpoint objects woken by a CASUAL poke |
| secret step | the crest (12) | 1 cell | 2 cells | a CASUAL layout poke |
| secret step | DARUMA (11) | no head hit | one head hit forgiven | `IFCASUAL` |
| secret step | the draft (14) | the turning scroll hangs still | it stirs (one flutter frame every 60 f) | a CASUAL object poke |

**HARD** (Should, v1.1):

| Section | Poke | Kind |
|---|---|---|
| Rooftops 01, 03, 04 | Jaja-nin throw every 60 f; stun 90 → 60 f | param |
| Scrolls 06 | a third fluttering scroll is a decoy that spins you back to the room's entrance | object list |
| Hall of scrolls 14 | the lantern flame flickers both ways before it settles | param |
| Daruma 11 | six blocks; fortune slips every 80 f | AI param |
| Caltrop hall 12-13 | one more caltrop row in 13 | layout poke |
| Boss | pinch at HP ≤ 18; pinch RUSH 5 px/f | AI branch |
| (v1.1 content) | nightingale: 12 px per chirp, the ceiling rises 1 px every 8 f; three ashigaru per whistle; bells bounce 60 px | param |

### 4.12 Commentator hooks (ids; the words are story §6.3's)

| Id | Trigger | Tier (R4.5) |
|---|---|---|
| YAM-01 | match card ends | Should |
| YAM-02 | the WANTED poster on screen | Should |
| YAM-03 | first bonk-stun | Should |
| YAM-04, YAM-05, YAM-14 | the runner, the passes, the sekisho | **retired** (Won't: the sekisho is cut) |
| YAM-06, YAM-07 | first chirp; the ceiling drops 32 px | Should (with the nightingale floor, v1.1) |
| YAM-08 | first scroll spin | Should |
| YAM-09 | UP at a still scroll | Should |
| YAM-10 | the Daruma fight starts | **Must** (DARUMA's tell: the rule) |
| YAM-11 | the head is hit | Should |
| YAM-12 | a perfect Daruma | Should |
| YAM-13 | pogo taken | Should |
| YAM-15 | the dark room: its first half ("Who turned off the lights?!") stays; the firework half is retired | Should |
| YAM-16 | first SILVER.T hit (`EV_WEAK_FIRST`) | **Must** |
| YAM-17 | Y.SPEAR on Yamato Man (PARRY) | Should (with SC4) |
| YAM-18 | pinch | Should |
| YAM-19 | the kabuki entrance / the *mie* | Should (with the kabuki stage) |
| YAM-20 | E plate taken | retired: story §6.2's plate lines cover it |
| **YAM-21** (new) | first time Rock enters 14 (the lantern flame leans: "Is there a draft in here?") | Should |

**Death lines** (Must: 4): story's lines 1, 4, 5 and 6 are recommended; lines 2 and 3 need the nightingale floor and
come back with it in v1.1.

### 4.13 Judges' debrief hints (tier B drafts: meta §4.4 asked this doc for them; story owns the words)

In meta's weight order (exit, room, item, plate). Set in capitals; each fits 4 × 28. YA0's tier A is story's new
riddle YA0.A (Should; story §7.1, meta §4.4); the sekisho riddle is retired.

1. YA0, exit: "IN THE LAST HALL OF SCROLLS, WATCH THE LANTERN. ITS FLAME POINTS AT THE SCROLL THAT TURNS."
2. YA1, room: "EDO'S GOLD IS UNDER THE FLOOR. POGO ON THE CREST IN THE CALTROP HALL."
3. YA2, DARUMA: "KNOCK OUT EVERY BLOCK, NEVER TOUCH THE HEAD, AND THE DARUMA PAINTS ITS OTHER EYE."
4. YA3, plate E (JET): "BEAT'S E-PLATE SHINES ON THE CASTLE ROOF. THE LADDER OVER THE COURTYARD LEDGE NEEDS A JET."

### 4.14 How crazy it gets

1. Rockman knocks ninjas silly from below, through the floorboards.
2. Walls that spin you round behind a hanging scroll.
3. A giant daruma otoshi you win by never touching the head, and it paints its own eye.
4. Rockman on a spear pogo, bouncing over caltrops and off the heads of the guards.
5. A lantern flame quietly points the way to the secret exit.
6. Yamato Man's helmet flies off and his MOBILE stat jumps to 99.
7. Mr. Y's WANTED poster: a million ryo.
8. *(v1.1)* The floor chirps, the spiked ceiling comes down, and the answer is to slide.
9. *(v1.1)* A kabuki stage revolves mid-fight while the audience shouts his name.

### 4.15 Revisits and VARIETY

- **Taps (v1.0):** F.BLAST burns the shoji pockets on 08 (`$D`, vanilla type). C.FLASH lights the dark room for 240 f.
  SILVER.T is Yamato Man's weakness and the samurai's one-shot.
- **Ice Block (v1.0):** encased Jaja-nin are steps up the mansion floors without bonking.
- **Alts (v1.1, Should):** Y.SPEAR's **Pogo** synergy (Power) crosses the caltrop hall without the rack and also opens
  the crest; Time Stop freezes the Jaja-nin mid-hop.
- **Tag partner (Should, cut-line item 2, with the tag partner):** Break Man's shield blocks the shuriken rain on 07
  while he jumps; the optional shortcut is a stack of rice bales in the kura (0C) that only his double knockback
  topples into a step up to a large weapon energy.
- **Par** (placeholder): 300 s (round 1 proposed 330 s; the trim removes about 30 s).

---

## 5. Across the four venues

### 5.1 Budgets

| | Blizzard | Flame | Centaur | Yamato | Total |
|---|---|---|---|---|---|
| Screens used / 32 | 28 | 28 | 30 | 30 | |
| Main route (incl. boss) | 00-16 | 00-16 | 00-17 | 00-16 (with the bypass 0C-0F) | |
| Secret route + arena | 17-1A | 17-1A | 1A-1C | 1B-1D | |
| Hidden room | 1E | 1C | 1D | 1E | |
| Plate route | - | - | 18-19 (T, Jet) | 18-1A (E, Jet) | |
| New object kinds, Must (family sub-ids) | 7 | 8 | 3 (+ the shared cloud) | 8 (the shuriken included) | **26** |
| New object kinds, Should / Could | 1 / 1 | 3 / 0 | 4 / 0 | 1 / 1 | **9 / 2** |
| Venue prize bits | 4 | 0 | 0 | 0 | 4 |
| Peak stage objects (§0.2) | 4 | 4 | 4 | 4 (5 of 7 in the pogo hall, where Rock can't fire) | cap 9 slots |
| Vanilla raster set piece | ship (chain 1) | none (palette cycle) | tide (chain `$14`) | none in v1.0 (the spike ceiling is Should) | |
| Art (tiles, frames) | art_audio §4.1 | §4.4 | §4.8 | §4.5 | art_audio §4.9 re-runs (R5.3) with §1.8, §2.6, §3.8, §4.7's change lists |

Round 1 needed about 46 object kinds and peaked at 8 objects "plus shots" (12 real slots). After the rulings the four
venues need 26 Must kinds, and no screen asks for more than 9 occupied slots. The screens to profile first, in the
slice and at M5: Blizzard 0A, 0D, 10 and the boss (with the Ice Block out), Flame 0B and 0E, Centaur 0D and 1A, Yamato
11 and 12.

### 5.2 The Must-only check (R0.4)

Every Must item and the Must engines it rests on. Nothing on this list needs a Should or a Could.

| Must item | Rests on (all Must) |
|---|---|
| Blizzard climb, refills, wrap | T6 variant blocks, the ceiling-probe callback, X-WRAP (tech, M3); ladder stubs (data) |
| The condor exit, the bonus summit | the attach state's core (M3, R8.2), the HUD widget meter, `map_set` (the gate) |
| The Vegetable Cellar | X-WRAP's per-row opt-out |
| SNOW CHAINS | the chip framework and its §9.2 effect (systems, Must by R2.5) |
| The Ice Block prototype | systems' Ice Block (Must by R2.4), the frozen tick and frozen handlers (R2.2) |
| Flame's dungeon, timed gates, hourglass gate | T3, T6 |
| Shadow Rock's merge | **T7** (Must by R0.4; tech's revision agrees) |
| The mouse room | T3's gate; the mouse NPC; its squeak (requested Must, with a vanilla SFX fallback, so it never waits on a Should) |
| FIREPROOF | the ignition hook on `$3E:$DDFC` (registry) |
| Flame's arena oil | the map-edit service's per-id flip with a timer |
| Centaur's doors, ZONE cards | T3's door/warp target, per-screen door tables in the screen scripts, the HUD widget label |
| The tide's dwell, ZONE 100, the tidal shaft | `EFFECTS` / `EFX_PARAM` (M5), `RL_TIDE`, a per-room tide base |
| CENTURION | meta's stage-counter predicate, systems' FULL flag |
| The pogo, the crest | GP player states, the set-piece player sheet (R2.3), T6 |
| The Daruma, DARUMA | **T8** (Must by R0.4; tech's revision agrees) |
| The draft (Yamato's exit) | T3's warp target |
| Plates E and T | systems' plates as pickups |
| The four boss reworks | GP_BOSSHIT, WEAK!, SC9 (systems, Must); own-weapon reactions are SC4 (Should) and nothing Must waits on them |
| W2's refights of these champions | the fight loader and FIGHT_CTX (R1.7) |
| The four champions' credits mode (v1.0 credits) | the credits room table and `GP_MODE` b0 `CREDITS` (tech §4.6); fallback: card strips only (fortress §6.2) |

### 5.3 Dependencies on other docs (requests)

| Doc | What this doc needs, or asks it to change |
|---|---|
| `systems.md` | (1) The Ice Block ships in the slice (R2.4), built at M3 with the dispatch table and Normal form's taps (R8.2): its code moves out of the Should alt line. (2) The four venue chips of §9.2 are **Must** (R2.5): systems' revision already tiers SNOW CHAINS v0.1 and the other three v0.5. (3) ABSORB's heal of 1 as a named SC4 exception (consistency-33). (4) VENUE ACTs: CONDOR, FIRST PASS; CLEAN DUEL; NO WRONG DOOR; SPEAR DANCER. (5) Placeholder pars: Blizzard 330 s, Flame 300 s, Centaur 300 s, Yamato 300 s (was 330). (6) The bird-bot has 2 HP, so the Ice Block encases it instead of killing it. (7) The Freeze columns of §1.9, §2.7, §3.9 and §4.10 for the NOFREEZE list. (8) Two boss-room lag rules (§0.2): the WEAK! pop spawns only while fewer than 3 boss-side objects are out, and the CENTURION chip's helper (a player-side utility) costs each boss here one projectile per move while it hovers. (10) Prizes: Blizzard's 4 vegetables are 10/10/15/25 = 60; the Y.SPEAR ledge (v1.1) holds an energy, not bolts. (11) Section moves for its cross-references: SNOW CHAINS is now §1.6.3, FIREPROOF §2.5.3, CENTURION §3.7.3, DARUMA §4.6.3. (9) Proposal (v1.1): an Ice Block in water floats and rides the tide |
| `meta.md` | (1) On-screen name **PERSIAN PALACE** (done in round 3: META-02). (2) Tier B hints for Centaur (§3.14) and Yamato (§4.13); FL0's tier B reworded for the glow (§2.12); YA0's tier A for the draft (done in round 3: meta §4.4 cites these tier B drafts, and YA0's tier A is story's new riddle YA0.A, §7.1; the sekisho riddle is retired). (3) PRIZES: 4 bits for Blizzard's vegetables, none for the other three. (4) Mid-boss fight ids for Shadow Rock, GAMARN & GAMADAYU and the Daruma (consistency-44 proposes `$0E`, `$0F`, `$10`). (5) The replay skip door on Blizzard 0F reads the venue's cleared bit. (6) Mini-record (Could): Blizzard's meter time at the condor grab. (7) Tier B hints now sit in §1.14, §2.12, §3.14 and §4.13 |
| `story.md` | (1) Words for every hook id; new ids **CEN-21** (Must), **CEN-22**, **YAM-21**; retired ids YAM-04, YAM-05, YAM-14, YAM-20, CEN-16 and YAM-15's firework half. (2) FLM-06's trigger is now "first parried shot", and its line should teach spacing. (3) BLZ-04 needs a varied Wily line (R3.9). (4) Death lines: drop BLZ 6 (the Ice Climbers' names) and CEN 6 (Kid Icarus's hero) (R3.3); the recommended four per venue are in §1.13, §2.11, §3.13 and §4.12. (5) Signs and inscriptions: the summit sign, the Atlantis tablet, ZONE 0's inscription, the vault's loan sign, the fortune slip. (6) The NPC row for Yamato: the sekisho guard's line is retired. (7) The Flame Mr. Y gag is a sponsor tapestry in v1.0 and Wily in costume in v1.1 (R3.4) |
| `tech.md` | (1) **T7 and T8 are Must** (R0.4; its revision agrees). (2) **The attach state's core at M3**, with the condor as its first user; the vines and the balloon follow at M5 (R8.2; routed as TECH-06). (3) The ship thread's turn event as a registry hook (icicles). (4) A per-room tide base for the tidal shaft, and a check of chain `$14` across vertical exits at the start of M5 (fallback: door-joined rooms) (decided in round 3: each room's screen script writes `TIDE_BASE`, `EFX_PARAM` keeps the dwell; tech §1.8, §16.8). (5) Per-screen door tables read by the screen scripts (Centaur's BG doors). (6) **No stage-`$00` stop-gaps** (R8.2): the slice's GP code reads stage record v0 from M2.1 (`SECRET_SCR`, `PAR`, GP_BOSSHIT's row), and Blizzard's row comes from its `.lvl` header at M4 (routed as TECH-07). (7) The map-edit uses of §0.4. (8) The set-piece player sheet streamed during the pogo rack's 24-f take animation. (9) The Daruma's stack part reads the hitting shot's Y on its latch. (10) The lag report of test G7. (11) The credits room table and the `CREDITS` bit that the four champions' credits mode tests (§1.10, §2.8, §3.10, §4.8; tech §4.6 has them). (12) §15.1's list of set pieces "written at 10-13" can drop Flame 0B: it is 9 occupied slots (§2.3) |
| `art_audio.md` | (1) The change lists of §1.8, §2.6, §3.8 and §4.7 for the R5.3 re-run (cuts, promotions, moves). (2) The mouse squeak as a Must SFX of about 20 B, or a named vanilla fallback. (3) Unchanged cue tiers: G25 BONUS SUMMIT and G26 KABUKI Should, G30 UNDERWATER and G31 PALACE Could. (4) The Blizzard fight's flicker check: art_audio §3.5 runs FLAKES with an Ice Block out; if it fails, FLAKES throws one flake fewer while the Ice Block exists (R8.6, applied at M4, §1.10) |
| `fortress.md` | W2's pair bouts load these four arenas through the fight loader. Each arena initialises its own effects (Centaur's tide) and undoes its own map edits (Yamato's wall spears, Flame's timed oil), and each boss reads its pinch threshold from the per-fight byte. The champions' idle frames are their vanilla stand frames; backdrop strips for the victory lap are Could. **The v1.0 credits** (fortress §6.2): each of the four champions runs a credits mode with no Rockman in his own boss room (Blizzard 16, Flame 16, Centaur 17, Yamato 16), given in §1.10, §2.8, §3.10 and §4.8; its cost is in fortress's ending figure (M8); fallback: that champion's card strip only |

### 5.4 Music and sound

- **Kept:** each venue keeps its vanilla stage theme (`$01` Blizzard, `$03` Flame, `$05` Centaur, `$02` Yamato) and the
  boss theme.
- **New** (art_audio §12.4 owns the list; original compositions only, no quotations):
  - Blizzard: **G25 BONUS SUMMIT**, the 40-s bonus-round tune `[new-music S · Should]`; v1.0 keeps `$01`.
  - Yamato: **G26 KABUKI**, the kabuki arena theme `[new-music M · Should]`, with the kabuki stage.
  - Centaur: **G30 UNDERWATER**, for ZONE 100 and the Sunken Throne `[new-music M · Could]`.
  - Flame: **G31 PALACE**, a darker palace variant for 04-0E `[new-music M · Could]`.
- **SFX** (art_audio §12.6): the Must ones these venues use are the bonk, the ice-cell break, the gate rumble, the plate
  click, the door unlock and the pogo boing. **Requested as Must:** the mouse squeak (the tell of a Must secret). Should,
  each with a vanilla fallback in v1.0: the seal's push, the condor's cry, the door fade, the siren, the slot reel, the
  scroll spin, the daruma chime, the chomper "shing", the chirp, the wooden clappers. **Cut:** the hanabi fuse and burst.

### 5.5 Scorecard notes (systems owns the formulas)

- **VARIETY** (25): each venue gives at least three weapon taps a job in v1.0 (§1.16, §2.14, §3.16, §4.15), the Ice
  Block one more, and the v1.1 alts more again. Variety is earned by using the tools the venue asks for.
- **SECRETS** (20): the secret exit (3), the hidden room (2), the behaviour chip (2) and, in Centaur and Yamato, the
  plate (1).
- **STYLE** (15): each venue's VENUE ACT (CONDOR, FIRST PASS; CLEAN DUEL; NO WRONG DOOR; SPEAR DANCER), the FROZEN STEP
  act on encased seals and ninjas, and, in v1.1, OWN MOVE through each champion's SC4 reaction.

---

## 6. Lessons applied

**Rockman CX** (`cx/SUMMARY.md` §6):

- **1. One premise everywhere:** every venue is a match with a card, judges, commentators, prize money (vegetables,
  sponsor envelopes) and a Mr. Y gag.
- **2. Homage as a mechanic:** Ice Climber's bonk and the seal that patches holes; PoP's plates, loose floors, the
  spacing duel and the shadow you must not fight; Atlantis's lying doors and deep warps; Jajamaru's floor bonk and
  DuckTales' pogo. The bosses' jokes are mechanics too (the ice block that stops the snowball, the parry at close range,
  the slot machine, the flying helmet).
- **3. Voice on failure:** four death lines per venue plus the Must tells.
- **5. Reuse set pieces with one twist each:** the ship shakes icicles loose; the oil becomes a permanent choice; the
  tide becomes a lift, a lock and a flooding shaft; vanilla's dark room stays dark. One twist each, and no twist repeats
  another venue's (R3.1).
- **6. Telegraph required tools:** every gate in §0.3 has a named tell; signs state the rules (the Atlantis tablet, the
  summit sign); the mouse squeaks, the statues blink, the crest glints, the mirror glows, the lantern flame leans.
- **7. Special cases in visible code:** the WEAK and own-weapon reactions are explicit branches (SC9, SC4).

**Rockman 4 Minus Infinity** (`r4mi/SUMMARY.md` §6 and the stage docs):

- **1. Weakness in the i-frames:** every boss uses systems' damage / i-frame tables.
- **3. A moral trade-off:** SNOW CHAINS (the seals cost you time) and FIREPROOF (the chandeliers are the easy way).
- **4. Friends as mechanics:** the seals refill holes; the Centurions block arrows (v1.1); Beat's plates reward the Jet.
- **5. Behaviour-gated secrets with a hint after the fact:** four chips and tier B hints for every secret.
- **6. Old tools, new jobs:** the full charge frees the Centurions and destroys seals (the trade-off); the slide is the
  way under the closing gate (and, in v1.1, across the nightingale floor); the vanilla Fire Telly is the ignition lesson.
- **7. Theme into mechanics:** a fire marshal, a tide you read like a clock, a summit bonus round, a lantern that shows
  the draft.
- **8. Map edits by bosses:** Yamato Man's spears stick in the walls; in v1.1 Blizzard's snowball breaks the arena floor
  and the kabuki stage swaps sets.
- Pharaoh's curse words → the ZONE cards; Quint's pogo (EXWP) → the spear pogo; Toad's hidden-room link → the
  one-screen detours that return you; Dust's TEMP gauge → the bonus meter in the boss-bar slot; Toad and Bright
  reacting to their own weapons → the own-weapon reactions; HARD as small data pokes → the HARD tables (v1.1).

**Vanilla Rockman 6** (`rm6/SUMMARY.md` §7):

- **2. A tileset slot per venue,** vanilla CHR kept and extended; set pieces as sprites only while they move.
- **5. New enemies through free type ids** → families and sub-ids (26 Must kinds here).
- **6. Breakables are per metatile id:** used deliberately (one oil id per gallery pool) and replaced by T6 where Ice
  Climber needs single cells.
- **7. Adaptors by win count:** no secret needs an adaptor; the plates keep vanilla's Jet geometry exactly; the bypass
  keeps vanilla's charged-punch blocks.
- **8. Quirks kept on purpose:** igniting oil, slippery ice, the Jet-only gaps, C.FLRSH (a commentator joke), the
  vanilla boss-panel stats, the dark mid-boss room.

**Round 2** (the rulings): **BG until it moves** (the lag cap is met by drawing hazards and doors as BG and spending a
slot only on motion); **a slice that is a whole venue** (Blizzard proves every loop before the other seven are built);
**a Must stands on Musts** (§5.2).

---

## 7. Risks

1. **Object kinds.** 26 Must kinds here (37 with Should and Could) against 30-32 free type ids for the whole game: the
   families and sub-ids (tech §7.2, M2) are the first thing to build.
2. **T6 block ids.** Blizzard already uses 255 of 256 blocks and Flame needs one oil id per gallery pool; T6 variants
   cost 2^k − 1 ids per breakable block. Mitigation: reclaim the cut vanilla screens' blocks (art_audio §4), keep the
   breakable quadrants to 2 per block; fallback: tech's bitmap variant (tech §10).
3. **IRQ-resident logic.** Vanilla's tide (handler `$C3D8`) runs game logic inside the IRQ. The raster list (M2) moves
   that logic out to a per-frame tick before Centaur is built (M5), so the dwell and the per-room base are written
   against the moved code. If that move slips, the fallbacks are ZONE 100's 24-px window without a dwell, and the shaft
   rooms joined by doors.
4. **The tidal shaft** is a new use of chain `$14` (vertical exits, a per-room base). It is checked at the start of M5;
   the door-joined fallback costs nothing new.
5. **Lag and flicker.** Every screen is planned at ≤ 9 occupied slots, but a utility (the Ice Block) or B.ATTACK's
   fourth flake can push a full screen to 10. The slice measures it (G7) before the other venues are built. Vanilla's
   Blizzard fight already flickers (9 sprites on a line in 56 % of frames); if the Ice Block case fails the flicker
   simulator, FLAKES throws one flake fewer while it is out (R8.6, §1.10).
6. **Screen budgets** are 28-30 of 32; Centaur and Yamato have two spare screens each.
7. **Fairness of the behaviour gates.** FIREPROOF can be lost on screen 01 by a first-time player: intended (a replay
   goal), with a generous lesson (a 120-f hover; 240 f on CASUAL, which also forgives one Telly ignition, §2.10). SNOW
   CHAINS punishes the full charge, the natural tool, so BLZ-07 fires on the first *hit*, every visit. The mouse's 10-s
   wait is unusual in a Rockman game; the squeak and the debrief hint carry it.
8. **Tedium.** Seal refills can slow the climb (450 f on CASUAL; a mid-climb checkpoint, plus one more on CASUAL). The
   40-s bonus is skippable on replays (R3.8).
9. **The Yamato trim** leaves a simple secret exit (five scrolls, one lantern). If playtests find it too easy, HARD's
   flickering flame or a sixth scroll tightens it without a new mechanism.
10. **Player art.** The pogo poses stream into the set-piece player sheet during the rack's 24-f animation: a 2 KB sheet
    takes 8 frames at 256 B/frame and 16 at 128 B/frame, so it fits either way. The condor needs no new player art.
11. **Homage and trademarks.** No parody label reaches the screen; plaques describe; DuckTales and the Sakugarne are
    Capcom's; the fortune slip's `大凶` is art (the text engine is kana-only).
12. **Estimates.** The four venues are 5 sessions above round 1's tight figure, all from rulings that promoted content to
    Must. The slice re-estimates them (R0.1), and every ⛳ gate re-estimates them again (R8.1).

---

## 8. Open questions

**Resolved since round 1** (consistency decision 38 and the rulings):

- The vanilla weakness cycle is kept (systems Table 1).
- Plates are pickups.
- A cleared venue can be replayed for its other exit (meta removes vanilla's beam-out).
- A secret-arena win awards the weapon (a full clear).
- The behaviour chips are unique to their venues (systems §9.2).
- Tag-only shortcuts are Should, shipped with the tag partner (cut-line item 2; Could until round 3); Break Man is
  callable in boss rooms after the bar fills, except where NO TAG.
- CASUAL uses the standard lever list through `CFG_CASUAL` (R2.9).
- Jump-up exits are Could (tech; the more conservative of the critics' Should and Could); the climbs ship with ladder
  stubs.
- **No stage-`$00` stop-gaps** (R8.2): the slice's GP code reads the stage record v0 from M2.1 (the secret screen, the
  boss row, the par); only vanilla's `$51` readers wait for M5.
- The attach state's core is built at M3 with the condor as its first user (R8.2).
- The four champions can run a no-player credits mode for the v1.0 credits (fortress §6.2's question): §1.10, §2.8,
  §3.10, §4.8.
- The per-room tide base: each room's screen script writes `TIDE_BASE`, and `EFX_PARAM` keeps the stage's dwell; the
  tide check across a vertical exit runs at the start of M5 (tech §1.8, §16.8; §3.5).
- The tier A riddle for Yamato's draft is story's YA0.A (Should; story §7.1, meta §4.4).

**Still open:**

1. Should an Ice Block float in water (v1.1)? (systems)
2. The mouse squeak: a Must SFX, or a vanilla fallback? (art_audio)

---

## Changes in round 2

Each change cites the ruling (R…) and the finding ids it resolves.

**Scope and tiers**

- Added the **v1.0 scope** section with per-venue Must / Should / Could / Won't and session estimates (53 Must; `tools/plan/tally.py`
  and `tight.py` updated). Every item re-tiered to the tight Must: each venue's core is Must; the second set piece and
  the secret-arena twist are Should; v1.0 secret arenas are the boss room re-paletted (R0.2, R0.3; scope-1, scope-2).
- **A Must depends only on Musts** (R0.4; scope-3): all four behaviour chips and Flame's mouse room are Must (R2.5); the
  Daruma becomes Must because DARUMA is; T7 and T8 are flagged Must for tech; §5.2 lists every Must's foundations.
- **Blizzard is the v0.1 slice** (R0.2, RULINGS §6 M4; scope-4): §1.0 gives its needs by milestone, its build order and
  its acceptance tests; it needs no attribute table, no T3, no text v1b and no forms.
- **B.ATTACK's Ice Block is the alt prototype** (R2.4; scope-8): §1.7 defines its test cases in Blizzard. All other alts
  and synergies are Should; each boss still previews its weapon's alt as AI.
- HARD poke lists and boss branches are Should; every venue fills in the CASUAL standard lever list (R2.9; design-7,
  scope-19, consistency-16).
- Exhibitions are Could and E4 is Won't (R3.7; scope-9): §0.3's pairing note.
- The tag-partner shortcuts stay Could, with the partner bundle (R2.5, R4.2; scope-15). *(Round 3: Should, with the
  tag partner, cut-line item 2; see "Changes in round 3".)*

**Engines, ids and memory**

- Stage ids `$00`, `$03`, `$04`, `$07` from tech's map (R1.2; feasibility-2, consistency-2, scope-12). New layouts may
  overwrite `$32/$33` after the vanilla regression (R1.5).
- Round-1 labels mapped onto tech's single engines: the map-edit service, T6 variant blocks (the bitmap is the
  fallback), the ceiling-probe callback, the HUD widget module, the attach state, families, `EFFECTS` / `EFX_PARAM`, the
  poke-list format (R1.10; scope-10, scope-16, scope-17, scope-25, consistency-33). The whole-bank tileset request is
  withdrawn for tech's slot table (R1.10; consistency-9, scope-11).
- **Lag recount with every occupied slot, cap 9** (R1.8; feasibility-4): every screen re-capped at ≤ 4 stage objects
  (§0.2). To get there: hanging icicles, loose tiles, zone doors, plaques and Yamato Man's wall spears are BG until they
  move; FLAKES throws 3 flakes; BLINK & BURST bursts into 3 pellets; the pinch VAULT throws 3 heads; the avalanche is
  staggered; the Daruma is two T8 parts; Flame's gallery has two pools; the loose bridge drops one tile at a time.
  Vanilla enemies are now counted with their projectiles and spawns (the propeller drone is a body and a rotor; the
  lantern robot, the seahorse and the dome turret fire; pelicans drop fish; piranhas blow bubbles), and enemy counts were
  trimmed on Blizzard 01, 02, 04, 06, 0B, 0C, 17; Flame 00, 0B, 12, 13, 18; Centaur 01, 02, 05, 0A, 0E, 10, 12, 14, 18,
  1A; Yamato 0A, 18. The slice measures the Ice Block case (G7).
- Frozen objects: every object table has a Freeze column (H / NF / boss) (R2.2; feasibility-6).
- Player-side slots: the Ice Block is a utility in 4-7 (R1.11; feasibility-9).
- The pogo poses go in a set-piece player sheet streamed at the rack, never the weapon slot (R2.3; feasibility-8); the
  condor carry reuses vanilla's ladder poses and allows the buster only (consistency-43).
- `[engine-ok]` kept only for data-only items (R1.14; feasibility-19).
- Pop-ups default to the top (consistency-26).
- Jump-up exits (X-UPEXIT) and the new floor types (X-FLOOR) follow tech's Could, the more conservative of the
  critics' tiers (RULINGS default rule; consistency decision 38 had Should); T7 and T8 are Must with tech. The attach
  state is asked for at M4, the slice being its first user (R1.13).

**Systems and economy**

- Round 1's weapon proposals and every "proposed row" are superseded by systems §3-§4; weakness i-frames are 16 f;
  only the boss previews and the reactions stay; ABSORB's heal is asked for as a named SC4 exception; DARUMA's effect and
  the pogo's numbers are systems' (consistency-33).
- Own-weapon reactions are Should (systems tiers SC4 Should); WEAK reactions are SC9, Must.
- **Bolt bags and the chest became sponsor envelopes**, one per hidden room; Blizzard's vegetables are re-priced to 60
  in all (4 prize bits); hidden rooms hold one tank or 1-up, not both (R2.7, R2.6; consistency-10, consistency-11,
  design-9).
- Featured enemies stay as in-stage tells with no PART drop (R2.5; scope-21, design-6).
- VENUE ACTs and placeholder pars added (systems §6.3, §6.5 requests).

**Content**

- **Centaur: the tidal shaft** (10-12) replaces the wrap tower (R3.1; design-5 c). X-WRAP is now Blizzard's alone.
- **Flame: the spacing duel** (R3.1; design-5 h): Flame Man and the palace guards parry shots that reach them less than
  48 px from Rock, with a blade-glint tell; no class-3 shields (Knight owns the shield). New VENUE ACT: CLEAN DUEL.
- **Yamato trimmed** (R3.2; design-25): the kite run and the sekisho (with its passes, runner and PASS counter) are
  Won't (v1); the bonk-stun stays; the secret exit is the scroll gate alone, a lantern flame showing the draft (R3.1;
  design-5 f); the nightingale floor is the Should second set piece. This also retires consistency-32 (PASS #3 under a
  Should Daruma).
- **Hanabi cut** (R3.1; design-5 b): Yamato's dark room stays vanilla-dark.
- At most one collect-N secret per venue: CENTURION, on meta's counter predicate (R3.1, R1.10; design-5 i, scope-16).
- **Names and trademarks** (R3.3; design-10, consistency-42): PERSIAN PALACE on screen; homage names only in design
  notes; parody labels never on screen; story asked to drop the Ice Climbers' and Kid Icarus's names from death lines.
- **Flame cultural fixes, Must** (R3.4; design-12): no "Oil Sultanate"; domes and a full moon on 18; the vizier only as
  Wily in a fake costume (Should), a sponsor tapestry in v1.0; jokes aimed at PoP's mechanics.
- **Flashes** audited, REDUCED fades (R3.5; design-13): §0.8.
- **Replays:** the bonus summit's skip door on 0F after the first clear (R3.8; design-16).
- **Shadow Rock** is harmless until you fire, and the mirror glows when a merge is possible (R3.9; design-17). BLZ-04's
  Wily line is to be varied (R3.9; design-23).
- UP interactions follow R2.10 (design-21). Signs and the Atlantis tablet show their words in the 2 × 28 ALL-CAPS
  pop-up (R1.4); the ship's and the tide's bands sit below the top pop-up band (R1.9, consistency-26).
- R3.6 changes nothing here: all four champions are sprite bosses at one size, within R5.1's 16-frame cap.

**Words, art and sound**

- story owns every word (R4.1; consistency-6): hook tables are ids, triggers and tiers; new ids CEN-21, CEN-22, YAM-21;
  retired YAM-04, YAM-05, YAM-14, YAM-20, CEN-16 and YAM-15's firework half.
- Text tiers (R4.5; scope-18): Must = first-weakness lines, the tells of Must secrets, 4 death lines (recommended per
  venue), tier B hints; flavour hooks Should. Tier B drafts written for Centaur and Yamato (meta §4.4's request,
  crossrefs).
- Art from recolours and composites first, with frame caps, and a change list per venue for art_audio's re-run (R5.1,
  R5.3; scope-7, consistency-8).
- Music cues keep art_audio's tiers; the hanabi SFX are cut; the mouse squeak is requested as Must (R5.2; scope-23).
- §8's round-1 questions are answered (consistency decision 38).

*Written by design-venues-b. Measurements: `build/design/design-venues-b/measure.py`, `measure2.py` (shot height, jump
rise 52 px, slide hitbox id). Map crops: `build/design/design-venues-b/*_0.png`, `*_1.png`. Round-2 scratch:
`build/revise/venues_b/`.*

---

## Changes in round 3

Requests routed to this doc in [`reconcile.md`](reconcile.md), and the [`RULINGS.md`](RULINGS.md) §8 rulings that touch
it. No Must figure changes: the four venues stay at 53 Must (M4 13.5, M5 39.5). The verify pass moves the tag-partner
shortcuts' 1 session from Could to Should (Should 18, Could 1.75).

| Id | Outcome | Section | Note |
|---|---|---|---|
| VENUES_B-01 | applied | §1.6.3, §2.5.3, §3.7.3, §4.5.3, §4.6.3; §1.12, §2.10, §3.12, §4.11; §7 risk 7 | Every chip's gate rests on Must set pieces (the seals and the foreman; the oil, the Tellies, the chandeliers and the marshal; the statues; the Daruma), and every venue fills in systems §13.4's lever table. One gap fixed: FIREPROOF had no CASUAL secret step; CASUAL now forgives the first ignition by a Telly's drop (a chandelier shot still voids it) |
| VENUES_B-02 | already | §0.2, §2.3 (0B), §5.1 | Since round 2 every screen peaks at ≤ 4 stage objects (9 slots; the pogo hall 5 of 7, where Rock can't fire) and every boss room at boss + ≤ 3. 0B's count is now spelled out (a falling chandelier is the same object; a burned guard's explosion takes his own slot); tech is asked to drop 0B from §15.1's "10-13" list |
| VENUES_B-03 | applied | §1.10 (FLAKES, flicker), §0.2, §1.0 (build step 8, G7), §5.3 art_audio (4), §7 risk 5 | At M4, if the flicker simulator fails FLAKES with the player's Ice Block out, FLAKES throws 2 flakes while an Ice Block exists (R8.6) |
| VENUES_B-04 | applied | §1.10, §2.8, §3.10, §4.8; §0.4, §5.2, §5.3 fortress, §8 | A credits-mode paragraph per champion (`IFCREDITS`: aimed moves use a fixed mark, no pinch, no reaction; fallback: the card strip only). The cost sits in fortress's ending figure (M8), not here |
| VENUES_B-05 | applied | v1.0 scope (rungs), §0.2, §0.4, §1.0, §1.10 (forms), §5.2, §5.3 systems and tech, §8 | R8.2: the attach state's core at M3 with the condor; the Ice Block row moves from M4 to M3 with the dispatch table; the stop-gap rows become stage record v0 (M2.1) plus Blizzard's row from its `.lvl` header at M4, tested by the post-kill hook at `$3F:$F9A0` (tech §4.1; was `$F4EB`); no forms in the slice, and Blizzard Man's form reactions arrive at M5. R8.6: the nightingale floor was already Should (§4.1, §4.5.1) |
| R8.1 | applied | v1.0 scope (session estimates), §7 risk 12 | This doc's per-milestone figures stated for §6's cumulative column (M4 13.5, M5 39.5, unchanged); every ⛳ gate re-estimates them |
| R8.3, R8.4, R8.5, R8.7 | already | - | Checked: no MMC5 audio, channel drop or POCKET cue; no string-count estimate of its own (story's counts rule); no verbatim quote from another game; no panel string, alias gag, "Blues" line, quick-draw or INPUT LAG figure in this doc |
| verify 1 | applied | §4.13, §5.3 meta (1)-(2), §8 | The stale requests are closed: meta prints PERSIAN PALACE (META-02), and YA0's tier A is story's new riddle YA0.A (Should; story §7.1, meta §4.4); the sekisho riddle is retired. §8's riddle question moves to the resolved list |
| verify 2 | applied | v1.0 scope (session table, rungs), §1.16, §2.14, §3.16, §4.15, §8, round 2's scope list | The tag-partner shortcuts are Should with the tag partner (cut-line item 2, R0.3, R4.2), like venues_a's and fortress's partner hooks, not Could with the PARTs bundle (item 9): Should 17 → 18, Could 2.75 → 1.75. `tools/plan/tally.py`'s row "venues_b tag-partner shortcuts" is to move from 'C' to 'S' to match |
| verify 3, 5 | applied | §1.16 (Par) | Blizzard's skip door adds the bonus's 2,400 f (40 s) to the run's `T` when it is taken, so the par stays 330 s and the skip neither buys nor costs TIME (systems §6.3, SYSTEMS-03); round 2's "taken off its par" is gone |
| verify 4 | applied | §0.5, §3.7.3, §4.8 | Y.SPEAR's v1.0 job is vanilla's single spear (it passes class-3 shields, SC1); the pierce is Should tap polish (systems §3.2). References fixed: SC1-SC14; featured enemies are systems §4.7; the FULL flag is systems §6.4; Yamato Man's volleys are systems §15.3 |
| verify 6 | applied | §3.5, §5.3 tech (4), §8 | The per-room tide base is decided: each room's screen script writes `TIDE_BASE`, `EFX_PARAM` keeps the stage's dwell (tech §1.8), and the vertical-exit check runs at the start of M5 (tech §16.8). §8's question 1 moves to the resolved list |
| verify 7 | applied | §0.6 (Words) | R8.4: cites story §10.4's by-area Must counts: venues_b 50 strings, 0 labels (Blizzard 13, Flame 11, Centaur 14, Yamato 12) |
