# Heritage Venues A: SKY ACE, HERO'S QUEST, HIGH NOON FRONTIER, LOST JUNGLE (design-venues-a)

Owner: design-venues-a. Round 2: every director's ruling in [`RULINGS.md`](RULINGS.md) and every critic finding about
this doc is applied (see "Changes in round 2" at the end). Round 3: RULINGS §8 and the venues_a requests of
[`reconcile.md`](reconcile.md) are applied (see "Changes in round 3"). Covers four of the eight Heritage Venues:

| On-screen name (R3.3) | Champion | Stage id (R1.2) | Meta index | Vanilla stage | Homage (design notes only, never on screen) |
|---|---|---|---|---|---|
| **SKY ACE** | Wind Man | `$01` | 2 | MECHANICAL TOWER | Capcom's *1942* (1984) and *1943* (1987) |
| **HERO'S QUEST** | Knight Man | `$06` | 7 | CAPITAL OF SCIENCE | the first console RPG hit of 1986, with a nod to the side-scrolling RPG sequel of 1987 |
| **HIGH NOON FRONTIER** | Tomahawk Man | `$05` | 6 | RESTRICTED AREA | Capcom's *Gun.Smoke* (1985), and the light-gun quick-draw and alley-gallery games of 1984 |
| **LOST JUNGLE** | Plant Man | `$02` | 3 | FORGOTTEN AREA | the 1982 jungle-explorer game for the 2600 and its 1984 cavern sequel |

**Binding inputs, in order:** [`RULINGS.md`](RULINGS.md) (overrides everything), [`BRIEF.md`](BRIEF.md), then the
single sources of truth: `systems.md` (combat, economy, chips), `meta.md` (save bytes, bracket, events, debrief),
`tech.md` (ids, memory, raster, CHR), `story.md` (every word, the ending), `art_audio.md` (tile, byte and track
budgets). This doc owns the **staging** of its four venues. Vanilla screens are written **vNN** (from
`docs/research/rm6/img/maps/*.png` and `levels_stages.md`); GP screens are plain **NN**.

**Words.** Every quoted line here is an EN **draft** for `story.md`, which owns all final text in JP and EN (R4.1).
Lines already in story carry its id (`WND-`, `KNT-`, `TMH-`, `PLT-`, story §6.3). EN is ALL CAPS on screen (R1.4).

**Tags** (BRIEF §8): **[engine-ok]** vanilla as-is or data only; **[new-code]**; **[new-art]**; **[new-music]**;
size **S / M / L**. **Tiers** (R0.2-R0.4):

| Tier | Meaning in this doc |
|---|---|
| **Must** | ships in **v1.0 "Championship"**. A Must depends only on Musts (R0.4) |
| **Should** | v1.1+, re-added in the R0.3 cut-line order (HARD lists = item 3; each venue's second set piece and secret-arena twist = item 4; Exhibitions = item 6; the tag partner = item 2) |
| **Could** | later, if ever |
| **Won't (v1)** | ruled out for v1 |

**Measurement kept from round 1** (scratch `build/design/design-venues-a/bossmove.py`, 1,440 frames per boss against a
moving, invincible player; logs `bossmove_*.json`):

| Boss | What the vanilla AI does against a moving player |
|---|---|
| Wind Man | Long fan phases (pull); W.STORM pinwheels `$9A` in pairs at f249, 546, 591, 1198, 1257, 1428; walks/hops across the room only twice in 24 s (f786-811 to x `$98`; f1017-1058 jump, peak y `$6B`) |
| Knight Man | Jumps every 100-350 f (airtime 60-75 f, peaks y `$3E`-`$61`); mace `$96` at f468, 705, 828, 1424 |
| Plant Man | Barrier (4 × `$B3` + `$B5`) raised at f86, 348, 699, 954, 1218 (period 260-350 f); leaps of about 130 f, peak y `$43`-`$48` |
| Tomahawk Man | Tomahawk `$B0` every 100-130 f (f95, 220, 351, 444, 738, 937, 1299, 1382); feather triple `$B1` at f521, 1070, 1183 |

---

## v1.0 scope

### What ships in v1.0

Each venue ships its **core** (R0.2): the homage mechanic, the secret exit, the hidden room, the behaviour chip and the
boss rework. **The secret arenas reuse the boss room with a new palette.** Each venue's second set piece and
secret-arena twist wait for v1.1 (R0.3 item 4), and so do the HARD lists (item 3) and every tag-partner hook (item 2).

| Venue | v1.0 (Must) | v1.1+ (Should), kept in full below |
|---|---|---|
| **SKY ACE** | Catapult launch; **the 2-minute sortie** on the free-flight vehicle state (LOOP, 1943 drain, shoot-to-cycle POW, 4 red squadrons, a simple AYACO, the SHOOTING DOWN % tally); the lamp board and the ACES ONLY elevator (secret exit); the **LAND** skip after the first clear (R3.8); a shortened tower with one sortie callback (design-16); WEATHER BALLOON (hidden room); YASHICHI (chip); Wind Man's rework; the secret fight on the tower top at night | **Gust decks** (VA-GUST, windsocks, Kite Mets, engine fans: the second set piece); the destroyer; AYACO's 4 engines, tail gun and BG version; **WING WALKER on the flying bomber** (the arena twist) with the hangar art and bomb carts; the re-sortie catapult; SC4 W.STORM joke |
| **HERO'S QUEST** | Talk and search verbs (King, Sage); MAGIC KEYS that doors eat; two fixed **ENCOUNTER!** command windows; the Trap Hall **ceiling with HP** (Knight's single use of the spike ceiling); the Metal Metslime (KAISHIN); LIGHT'S TABLET (hidden room); the stairs behind the empty throne with the **key check and a ladder back** (R3.9); the Knightlord's offer; Knight Man's battle-log rework | **The Inn and Princess Roll** (the second set piece); the Knightlord's throne staging in 1A (the arena twist); SC4 KNIGHT.C clash. Could: EXP level-ups, TRUE FORM. Won't: the dark basement (R3.1) |
| **HIGH NOON FRONTIER** | The WANTED board and three bounties; the alley gallery (SHERIFF STAR); the **judged quick-draw** at 24 / 18 / 40 f (R3.5); the 4:50 train on 3 bands with Sidewinder; **the conductor reads the bounty count** (R3.8) and offers the EXPRESS skip after the first clear; the Sheriff's back way (secret exit); THE OUTHOUSE (hidden room); every R3.4 fix: HIGH NOON MESA, the rodeo showman, the flag judge, the cactus walkers, the RODEO RING as the secret arena (boss room at dusk) | The train's separate sky band with the sun and shimmer, and the tunnel bats; the rodeo-ring fence and stands (arena twist); TNT crates; the 12 re-board; the pause-screen poster page; SC4 SILVER.T catch. Could: vulture re-skin, W.STORM dust-devil reversal |
| **LOST JUNGLE** | Vines (attach state), croc heads, rolling logs, the breathing tar pit; four treasures and the log counter (AUTO RECOVER); the 3-for-9 underground; the cat, the Lost Caverns and the balloon (secret exit); the storm and TREETOP HUT (hidden room, R3.5-safe lightning); Plant Man's rework; the secret fight in the bamboo room at night | **CONGA's logs and the flower-swamp croc channels** (the second set piece); the Lost City ruins arena (arena twist); eels; the vine burn; the Ice Block croc. Could: rain, the 20:00 clock, C.FLASH tar |

### Sessions (the ledger, R0.1)

Code, data and tests per venue, in `tools/plan/tight.py`'s units (shared engine pieces are counted under tech; art,
music and text under art_audio and story):

| Venue | v1.0 breakdown | v1.0 | v1.1+ (Should / Could) |
|---|---|---|---|
| SKY ACE | layout and lists 2 · sortie data on the vehicle state (waves, POW, LOOP, drain, lamps, tally) 4 · simple AYACO 1.5 · catapult, lamp board, elevator, LAND 1 · hidden room, seagull, YASHICHI 1 · Wind Man and the 1D fight 2.5 · CASUAL list, data, route movies 2 | **14** | 8 / 0 |
| HERO'S QUEST | layout and lists 2 · King, Sage, search spots, keys and doors, stairs check 2 · ENCOUNTER! and its two enemies 2.5 · ceiling with HP 1 · Metal Metslime and KAISHIN 1 · hidden room 0.5 · Knight Man with the battle log and the Knightlord 3 · CASUAL, data, movies 2 | **14** | 4.5 / 1 |
| HIGH NOON FRONTIER | layout and lists, cactus re-skin 2 · board and bounty 1 0.5 · gallery 2 · judged VA-DRAW and Sam 1.5 · train, Sidewinder, conductor, EXPRESS 3 · Sheriff, STAR, outhouse 1 · Tomahawk Man and the RODEO RING 2 · CASUAL, data, movies 2 | **14** | 4.5 / 1 |
| LOST JUNGLE | layout rebuild and thirds 2 · vines, crocs, logs, tar 3 · treasures and the perfect gate 1 · underground, cat, balloon 2.5 · storm and hidden room 1 · CONGA checkpoint and slot rule 0.5 · Plant Man and the 1E fight 2.5 · CASUAL, data, movies 1.5 | **14** | 4 / 0 |
| **Total** | | **56** | **21 / 2** |

These match `tight.py` (14 per venue) and the venues_a rows of `tools/plan/tally.py`, which round 2 splits into
v1.0 and v1.1+ rows with unchanged totals. HARD lists for these venues are in tally's systems row "HARD content".

**Milestones (R6, R8.1).** LOST JUNGLE is built in **M5** (it needs the stage-attribute table, the map-edit service, T5
and the attach state's vine and balloon users; the attach state's core arrives earlier, at M3, with Blizzard's condor:
R8.2). HERO'S QUEST, HIGH NOON FRONTIER and SKY ACE are built in **M6**, after **text v1b** (dialogue, choices,
NPC menus: R1.4) and T1-lite, before the "Round One" checkpoint (v0.5). Per milestone, for RULINGS §6's cumulative
column (R8.1): **M5 14, M6 42**. The bosses' credits modes (§1.7.2, §2.8.2, §3.8.3, §4.7.2) are costed in fortress's
ending row, not here.

### What v1.0 depends on (all Must, R0.4)

| Owner | Piece | Used by |
|---|---|---|
| tech | Stage-attribute record (48 bytes, R1.14): `SECRET_SCR`, `PAR`, `EFFECTS` (CEILING), the 32-bit `NO_TAG` mask | all |
| tech | **One map-edit service** (`map_set` + per-id alternate flip, one repaint queue, R1.10) | stairs, trapdoor, doors, tar pits, outhouse, gallery windows, lamp board, windsock, sprouts, brick wall |
| tech | Families `$F4` (enemies) / `$F5` (directors, T3 switches and targets) and the object lists v2 | every new object |
| tech | **One HUD widget module** (R1.10) | key count, LOOP and lamp icons, bounty icons, log counter, draw readout |
| tech | **One attach state** (vine, balloon) with T5 (its core at M3 with Blizzard's condor; T5, the vine and the balloon at M5: R8.2); **one free-flight vehicle state** (SKY ACE, lane flag off) | Plant; Wind |
| tech | T1-lite (camera lock, time-scrolled bands, the wave director folded into the screen script), T3, T8 | Wind sortie and AYACO; Tomahawk train; doors, keys, lifts |
| tech | Raster list (24 bands, `RL_PARALLAX`, `RL_SHIMMER` = 2 entries, `RL_BANDS`; R1.9) | sortie, train, Tomahawk desert and sunset |
| tech | Text **v1a** (pop-up, 2 × 28) everywhere; **v1b** (dialogue 4 × 28, CHOICE, NPC menus) | Knight, Tomahawk |
| tech | The Knight ceiling's logic moved out of IRQ `$11` with a retract parameter (`EFFECTS` b2, `EFX_PARAM`) | Knight Trap Hall |
| tech | One poke-list format (tech §5.5) with the `CFG_CASUAL` layout tier (R2.9) | every CASUAL list |
| tech | The credits' room table and `GP_MODE` b0 `CREDITS`, tested by `IFCREDITS` (tech §4.6, M8) | each boss's credits mode (§1.7.2, §2.8.2, §3.8.3, §4.7.2) |
| systems | SC1 (with **Y.SPEAR in the pass-through list**), SC8 (the draw's free hit), SC9 (weak reactions); chips 13-16 and the Energy Balancer; the frozen handler and NOFREEZE (R2.2); the INPUT LAG setting (0-6 f: R3.5, R8.7) | the bosses, the chips |
| meta | SECRETS bits by meta index, the PRIZES field, `VENUE_REC`, the debrief (tier B hints), `STAGE_CLEAR` (LAND and EXPRESS appear after the first clear) | all |
| story | Every word; 4 death lines per venue in v1.0 (R4.5) | all |
| art_audio | The sets and thirds of §1.1/§2.1/§3.1/§4.1 below; vanilla music fallbacks | all |

No v1.0 item here needs a Should item. Every place that *could* touch one says what v1.0 does instead.

---

## 0. Rules shared by the four venues

### 0.1 Ids, screens and layouts

- The four venues keep their vanilla stage ids (`$01`, `$06`, `$05`, `$02`; tech §4.2, binding by R1.2). Their meta
  indexes are id + 1 (meta §1.8).
- Each venue's row in the 48-byte stage-attribute record (R1.14) carries what this doc needs: the tileset slot, the
  **secret-boss screen `SECRET_SCR`** (consistency-21: the renamed `PLATE_SCR`; a boss kill there sets SECRETS b0 and
  drops plate A or B), `PAR`, `EFFECTS` (Knight: b2 CEILING) and the 32-bit `NO_TAG` screen mask (used only when the
  partner ships). The record and its readers are tech's [new-code] (M2.1); this doc supplies data only.
- A stage is one strip of at most **32 screens** (`$00-$1F`). Main routes sit low; branches, secret rooms and the
  hidden room use `$18-$1F`, as vanilla does. Use: SKY ACE **27** of 32 (the tower is shortened, design-16), HERO'S
  QUEST 28, HIGH NOON FRONTIER **32**, LOST JUNGLE **32** (Risks 1).
- The new layouts are built in the GP level format and may overwrite vanilla layout banks `$32`/`$33` once vanilla
  stages 1, 2, 5 and 6 are regression-tested from the base ROM (R1.5).
- No design here needs the "enter a screen from below without a ladder" exit (BRIEF §4). Every upward exit is a ladder;
  every balloon or lift ride stays inside one screen.

### 0.2 How the secrets are built (uniform)

| Secret | Rule | Mechanism | Tags · tier |
|---|---|---|---|
| **Secret exit** | An alternate route ending in a **second boss room** (`SECRET_SCR`). The kill there sets the venue's SECRETS b0 (meta) and, in Knight and Tomahawk, drops the plate | Vanilla's own plate mechanism (exits with explicit targets into `$18-$1F`, the boss-screen test `$3F:$F4EB`/`$F518`), generalised into the attribute record by tech | [new-code] (tech, M2.1) + data S · Must |
| **Secret arena** | v1.0: **the venue's boss room with a new palette**, same AI, pinch at HP 12. v1.1: each venue's distinct arena (the twist) | layout copy + palette | data S · Must; arena twist Should |
| **Hidden room** | Exactly one screen, off every route, with a visible tell; holds the venue's **sponsor envelope** (30 bolts, systems §7) | an extra exit with a target, or a T3 door warp | S · Must |
| **Behaviour chip** | Earned by *how* you play a set piece, never bought (systems §9.2 rows 13-16 fix the effects) | a per-venue run counter in WORK, tested when the reward spawns. "Collect N" counts use meta's stage-counter predicate (R1.10); at most one collect-N secret per venue (R3.1) | S · Must |
| **Plates** | Knight keeps **A**, Tomahawk keeps **B**, in their vanilla second boss rooms (`1A`, `1F`). Wind and Plant have none | a pickup object (systems §10) dropped by the kill, so it is always collected with the exit; meta counts it with the exit | [new-code] S · Must |

**Debrief** (meta §4): the order is meta's weight rule (exit 3, room 2, item 2, plate 1): exit → room → item. The
predicate ids are meta's: `WI0-2`, `KN0-2`, `TO0-2`, `PL0-2`. Each venue's **tier B hints** below are real text (EN
draft, story finalises); tier A riddles are Should (R4.5).

**Exhibitions** are Could (v1.1, R3.7). When they return, these exits keep their pairing: **SKY ACE + HERO'S QUEST
light E1, HIGH NOON FRONTIER + LOST JUNGLE light E2** (meta's pinwheel). In v1.0 the exits score SECRETS and the
rating only.

### 0.3 Adaptors, vehicles and the partner

Power arrives after the 2nd win, Jet after the 4th (systems §2.3). **No normal exit needs a form, an alt fire, a
synergy or Break Man** (systems §2.4).

| Venue | Needs Power (optional content) | Needs Jet (optional) | Needs nothing special |
|---|---|---|---|
| SKY ACE | item pocket on 04 (vanilla v03 block) | none: the sortie **lends a vehicle** (below) | secret exit, hidden room, chip |
| HERO'S QUEST | 1-UP pocket on 01 (vanilla); either basement door **if** short of keys (the stairs warn, and a ladder leads back, §2.5) | none | secret exit, hidden room, chip |
| HIGH NOON FRONTIER | the Energy Balancer block on 13 (vanilla) | the sky bypass 18-1A (vanilla quirk, kept) | secret exit, hidden room, chip |
| LOST JUNGLE | the brick wall 19 → 1A (a shortcut) | none | secret exit, hidden room, chip |

**The lent vehicle** (consistency-36). SKY ACE's sortie runs on tech's **free-flight vehicle state** (R1.10), not on
the Jet form. It is NO TAG, it works under the 1993 rules if those ever ship, and it books no form-based VARIETY. If
the Jet is not owned yet, Rush wears a **RENTAL** bib (story approved it). Every venue can therefore be the first.

**Break Man** (the playable partner) is **Should** (R4.2, R0.3 item 2). Each venue keeps one optional partner hook,
listed in its text-and-partner section as v1.1 material; none is ever required, and v1.0 has no TAG gate in these
venues. Break Man's call is a pause-menu row confirmed with A (R2.10).

**Input** (R2.10): talking, reading and doors use an **UP press with B not held**, suppressed for 10 f after an alt.
In-stage SELECT means only the quick swap and the last-weapon toggle. The search verb is DOWN held 24 f (VA-SEARCH,
§0.4; taught on Knight 00).

### 0.4 Engine pieces these venues use (one owner each)

tech builds every engine piece (R1.10); this doc owns the data and the venue objects (`OBJ_*`, families `$F4`/`$F5`).
Ids T1-T8 are PLAN's; `VA-` pieces are this doc's, built **on** tech's shared services.

| Id | What | Built on | Used in | Tags · tier |
|---|---|---|---|---|
| **T1-lite** | Camera locked on one or two screens; raster bands scroll by time (plus camera for parallax); a **wave director folded into the slot-22 screen script** spawns from a data list (frame, kind, x, y, path) | tech §9.1, `RL_BANDS` | Wind sortie 01; Tomahawk train 10-11 | [new-code] M · Must (tech) |
| **Vehicle state** | Free flight in 8 directions, no gravity, lane flag off | tech §7.9 (R1.10) | Wind sortie 01 | [new-code] M · Must (tech) |
| **Attach state** + **T5** | Hang from a moving object (offset, input rules, release on A); T5 gives the vine its pendulum | tech §7.9 (R1.10) | Plant vines, balloon, Plant Man's vine | [new-code] M · Must (tech; the core at M3 with Blizzard's condor, T5 and these users at M5: R8.2) |
| **T2** | Text window, typewriter, CHOICE (YES/NO, 2-4 rows) | text v1a (pop-up) / v1b (dialogue, menus) | all; Knight heavily | [new-code] L · Must (tech) |
| **T3** | Switch → target: doors (UP), keys (a per-stage key counter in the run block, tech §7), chests, gates, lifts through a down exit, shot-count switches, warps | tech `$F5` channels | Knight, Tomahawk, Wind | [new-code] M · Must (tech) |
| **T4** | Raster bands per screen (≤ 4 here + the window band) | tech §8, `RL_BANDS` (24 bands per buffer, R1.9) | Wind 01, Tomahawk 00-02, 0A-0C, 10-11 | [new-code] M · Must (tech) |
| **T8** | Multi-part boss (one controller, part objects) | tech §7 library | AYACO | [new-code] M · Must (tech) |
| **Map edits** | `map_set` (per cell) and the per-id alternate flip, one repaint queue (R1.10) | tech §5.6 | stairs, trapdoor, doors, tar pits, outhouse, gallery windows, lamp board, windsock, sprouts, brick wall | [new-code] · Must (tech) |
| **HUD widgets** | digits, label, meter, icon row, data-driven (R1.10) | tech | every counter here | [new-code] M · Must (tech) |
| **VA-TIMED** | (a) rideable-when-closed hazard object (vanilla lift `$A0` code plus a state); (b) **toggling floor**: the per-id alternate flip on a timer | map-edit service | Plant croc heads (a), tar pits (b), Plant Man's centre (b) | [new-code] S · Must |
| **VA-SEARCH** | DOWN held 24 f while standing still on a floor (not on a ladder top) probes a search-spot object (`$F5`) under Rockman | T3 | Knight | [new-code] S · Must |
| **VA-DRAW** | Judged quick-draw: READY / flag / DRAW!, RNG delay, window per difficulty, FOUL, readout | HUD widget, LFSR | Tomahawk saloon and boss | [new-code] S · Must |
| **VA-ENCOUNTER** | Screen lock with vanilla shutters, music swap, T2 command menu, a wave, a victory chest | T2 v1b, T3 | Knight | [new-code] M · Must |
| **VA-GUST** | A horizontal push zone lifted from Wind Man's pull code (AI `$31:$8AFC`), with a direction schedule | Wind Man's AI | Wind decks | [new-code] S · **Should** (the boss's own push is AI, Must) |

### 0.5 Lag budget (R1.8)

**Count every occupied slot**: the player (slot 0), the screen script (slot 22, which also runs every director here),
player shots (slots 1-3), GP utilities (4-7), enemies, enemy bullets, pickups and effects. **Cap: 9** until M3
measures the OAM-builder gain; tech §6.3 and artcheck enforce it. The worst case is always 1 player + 1 script + 3
shots = **5 fixed slots, leaving 4 for the enemy side**. Every set piece below states its count. Rules used throughout:

- Directors, band control, gallery and croc timers live in the slot-22 script, never in their own slots.
- Closed windows, tar, lamps, windsocks, sprouts, flags and signs are **BG** through the map-edit service, not objects.
- An explosion stays in its dying enemy's slot; directors count it as live.
- A director that would exceed the cap **delays** the spawn (never drops it), so waves stay deterministic for golden
  movies.
- **The text runner and player utilities are occupied slots too** (tech §7.12, §15.1): an open pop-up or window (the
  text runner, slot `$15`) and a utility in slots 4-7 (the Ice Block, R1.11). Every director and boss AI here counts
  them before a spawn or a shot and waits while one more would make 10 (the sortie, the gallery, the train, Knight
  Man's fireballs). A pickup's pop-up opens as the pickup leaves, so the count holds (the treasures, the ring). On a screen with no
  director, a utility or a commentator pop-up can lift a full screen to 10 for its lifetime; the slice measures exactly
  that on Blizzard (venues_b §0.2, test G7) before these venues are built, and a screen that lags past the band drops to
  3 stage objects.
- The only vanilla screens kept as-is that could reach 10 are fixed by one AI rule each (CONGA, §4.6).

### 0.6 Text, pop-ups and commentators

- **Pop-ups** (text v1a): 2 × 28 cells, ≤ 24 glyph ids, ALL CAPS EN, kana JP (R1.4). **Default position: the top**
  (consistency-26, tech `EFFECTS` b6). The screen scripts of **Wind 01** and **Tomahawk 10-11** switch the window to
  the bottom on entry, because their top bands are raster set pieces; tech provides that per-screen switch.
- **Dialogue and menus** (text v1b): 4 × 28 (Knight's NPCs, the Knightlord, Tomahawk's Sheriff and conductor).
- **Commentators** (story §6.1's bus): v1.0 plays, per venue, **4 death lines** (story picks them from its 6), the
  **first-weakness line** and the **secret lines** (R4.5). The flavour hooks are Should. Never during a reaction-time
  prompt (READY, a tunnel warning, a battle-log line).

### 0.7 Tileset slots and CHR

- tech owns **one tileset-slot table** (R1.10): its RAM-image model, 2 slots per bank, an independent alternate set
  per slot. This doc lists content only.
- **No extra CHR page exists** (R1.3). Tile ids are the binding limit (256 BG tiles live at once). New BG art enters as
  CHR thirds swapped by screen exits (`$0A00-$0FFF` or `$0000-$01FF`), as vanilla's `$91`/`$95`/`$98` sets do;
  measured capacity is from round 1's `swapcap.py` and `planttiles.py`.
- New sprites start as **recolours or composites of vanilla RM6 sprites** (R5.1): 8 frames per enemy, 16 per boss.
  Claude's drafts are final; a human pass is optional polish.
- **Body changes** (R2.3): the sortie's flight and loop poses are a **dedicated set-piece player sheet** streamed
  during the catapult launch (a locked moment), never the 15-tile weapon slot. Vines and the balloon use vanilla's
  ladder poses, so they need no sheet; **only the buster fires while hanging** (consistency-43), and the equipped
  weapon returns on release.
- art_audio owns every count (R5.3). The v1.0 deltas this revision asks for are listed in §1.1, §2.1, §3.1 and §4.1.

### 0.8 Scoring and economy data (what systems §6-§9 asks of each venue)

| Venue | Featured enemy (an in-stage tell: it dies outright to the champion's weakness; **no PART**, R2.5) | VENUE ACT (STYLE, 1) | TIME par (tune) | Venue prizes (≤ 60, once per save) and their PRIZES indexes |
|---|---|---|---|---|
| SKY ACE | `$34` shield-cars (09-0B): C.FLASH ignores the shield and drops them, the same flash that stalls Wind Man | **ACE**: SHOOTING DOWN 100 % | 4:30 (includes the fixed 2:00 sortie) | none |
| HERO'S QUEST | `$6E` lance knights (Trap Hall, encounter 2): Y.SPEAR outreaches their lances and drops them, the tell for the boss | **SPELLBREAKER**: interrupt HEALMORE | 4:30 | 20: #0 the torch-pocket pouch (08-09) |
| HIGH NOON FRONTIER | `$6C` cowboy gunners (desert, train robbers): PLANT.B's pollen makes them sneeze off their crates, the tell for HAY FEVER | **QUICKEST GUN**: win the HIGH NOON draw | 5:00 (includes the fixed 0:55 train) | 60: #0-#2 bounties 15 / 20 / 25 |
| LOST JUNGLE | `OBJ_SCORPION` (underground): B.ATTACK drops the cold-blooded scorpion outright | **VINE KILL**: kill an enemy while hanging on a vine | 4:00 | 60: #0-#3 treasures 10 / 15 / 15 / 20 (a rhinestone pays 0) |

meta places the PRIZES bits (consistency-11); the indexes above are this doc's. Each hidden room holds the venue's
envelope (SECRETS b4). Replays show collected prizes as tokens (systems §6.7).

### 0.9 CASUAL and HARD

- **CASUAL** (R2.9, Must): a `CFG_CASUAL` bit (meta owns it) selects the CASUAL layout tier of tech's poke lists.
  **Every venue fills in the one standard lever list** (§1.8, §2.9, §3.9, §4.9), in systems §13.4's form with each
  row's mechanism (its How column): reflex windows ×2; mash counts −40 %
  (hold-to-struggle allowed); set-piece timers +50 %; +1 checkpoint per section; skill-gated secrets relaxed by one
  step. None of these four venues has a mash.
- **HARD in v1.0** is systems' preset: ×1.5 damage, drops LESS, no refill, the framework hooks kept. The only
  per-difficulty constant v1.0 reads here is the quick-draw window (R3.5, §3.5). **The per-venue HARD poke lists and
  boss branches are Should** (R0.3 item 3); they stay in this doc, in tech §5.5's format (R1.10, fixing the IFHARD bit
  bug of consistency-15).

### 0.10 Accessibility (R3.5)

- **Flashes**: in the default mode, no effect here flashes a large area more than **3 times per second**; REDUCED turns
  every flash into a fade. Large-area effects in these venues: the encounter transition (§2.3), the tunnels (§3.6),
  the storm (§4.8). Each states its numbers.
- **Reflex windows**: the quick-draw is NORMAL 24 f, HARD 18 f, CASUAL 40 f (R3.5, R8.6), plus the CONFIG **INPUT LAG**
  offset (0-6 f, R8.7; §3.5). Every reflex tell has a sound as well as a picture.

### 0.11 Freeze classes (R2.2)

Frozen objects keep taking damage. In v1.0 the freezes are the WEAK stagger and B.ATTACK's **Ice Block** (the one
alt that ships, with the Blizzard slice, R2.4). Each new object here declares its class:

| Class | Objects |
|---|---|
| Frozen handler (damage step `$E9D7`-style) | propeller Met fighters, Metslime, Killer Chest (open only), scorpion, bat, gallery outlaw, robber, cactus walker |
| **NOFREEZE** (ignores freezes, still takes hits) | AYACO and its parts, the Metal Metslime ("metal doesn't freeze"), winches, croc heads, logs, Six-Shot Sam, Sidewinder, the tunnel wall, gallery civilians, the cat, seagull, parrot, balloon |
| Boss-side frozen state | Wind Man, Knight Man, Tomahawk Man, Plant Man, and CONGA (vanilla parts) |

---

## 1. Wind Man: SKY ACE

**Pitch.** Wind Man's floating Mechanical Tower hovers over a mock sea battle. You are catapulted off the Committee
carrier, fly a two-minute sortie played by **1943's rules** (energy that drains in flight, POWs you shoot to change,
three loops, red squadrons, a giant bomber, and the "SHOOTING DOWN %" tally at the landing), land on the tower's flight
deck and climb the tower to Wind Man, who flies a 1943 evasive loop and calls his own red squadron.

Vanilla facts used: layout `$32:$A800`; tileset `$2C:$80` (blocks 232/256, BG tile ids 248 used / 8 free); base CHR
`$83`, extras `$8C` (tower), `$8D` (open sky), `$8E` (dark base); palette `$17`; music `$00`; checkpoints v08 and
shutter v14; boss `$99`, AI `$31:$8AFC`; weakness C.FLASH (4); W.STORM landed once in 7 s of glued shots
(`stages_b.md` §5). No raster split anywhere in vanilla Wind.

### 1.1 Tileset slot and art (art_audio §4.2 owns the counts; v1.0 deltas marked)

| Item | Content | Tags · tier |
|---|---|---|
| Slot **TS_WIND** | Copy of `$2C:$80` tables; 24 free block ids plus reclaimed ones (tech's slot table) | [engine-ok] S · Must |
| Kept (vanilla CHR) | `$83` sky, clouds, coral girders, gold pillars, tower shaft, fans and updraft tiles; `$8C`, `$8D`, `$8E` | [engine-ok] |
| **W-CARRIER** third (~96 at `$54-$B3`; v00's screens leave `$54-$E9` free) | Steel deck, stripes, catapult track, arresting wires, lamp board (lamps lit by `map_set`), elevator rim, "ACES ONLY" sign, **the LAND hatch and its sign** | [new-art] M · Must |
| **W-SEA** band (~48 at `$76-$B5`, programmatic) | Sea (512-px loop), distant islands | [new-art] S · Must. The destroyer silhouette (+16): Should |
| **Windsock** (BG, ~8 ids, 3 states: limp, left, right) | The boss room's wind tell on 13 and 1D, repainted by `map_set`; also the decks' tell once the gusts ship | [new-art] S · Must (boss rooms) |
| **SET-WS1** `A0+32` | Propeller Met fighter (bank L / level / bank R; green and red by palette), gold leader, bullets; a composite of the vanilla Metall and the `$1B` bomber's propeller (R5.1) | [new-art] M · Must |
| **SET-WS2** `C0+16` | POW / 3-WAY / AUTO / YASHICHI icons, LOOP "R", lamp icon | [new-art] S · Must |
| **SET-WS3** `D0+32` | v1.0 AYACO: a 48×24 body with two engine pairs (2 frames each) and a bomb | [new-art] M · Must. Four separate engines and the tail gun (+16): Should |
| **Seagull** (2 frames, SET-WS4 `A0+16`) | The hidden-room tell on 0A | [new-art] S · **Must** (art_audio had it Should; the Must hidden room needs its tell) |
| **Set-piece player sheet** (R2.3) | Rock in flight on the loaner (built from the Jet form sheet), 4 loop frames, the RENTAL-bib variant. Streamed during the catapult's 60-f cut, a locked moment; never the weapon slot | [new-art] S · Must (~24 new tiles) |
| Champion pinch set | SKY ACE goggles and scarf (12), the pinch-E red plane in one pose (4), a POW (4) | [new-art] S · Must (24 tiles; art_audio had 16) |
| Kite Met (SET-WS4), deck crew Met and bomb cart (SET-WS5) | | [new-art] S · Should |
| **W-HANGAR** third (~96), AYACO as BG art (~110) | Hangar bays, parked fighters, the bomber's wing top; AYACO drawn in the sky band | [new-art] M / L · Should |

The sortie (01) carries SET-WS1 + WS2 + WS3, so **no vanilla Wind enemy appears on 01** (art_audio §4.2) and
explosions use the common row.

### 1.2 Screen-by-screen

CHR column: B = base `$83`, C = W-CARRIER, S = W-SEA, T = `$8C` tower, O = `$8D` open sky, D = `$8E` dark base.
The tower is **shortened by two screens** (design-16): v0F+v10 and v11+v12 are merged.

| GP | From | CHR | The player does | Enemies | Set pieces | Tags · tier |
|---|---|---|---|---|---|---|
| **00** | new (replaces v00) | B+C | Walks right across the carrier deck to the catapult and stands on it (launch after 40 f, or UP). After the first clear, a deck hatch at the left end shows **LAND** (§1.3.5) | none | **Catapult launch**: a 60-f cut, Rush and Rockman shot off the bow; the set-piece sheet streams under it. Without the Jet owned: the RENTAL bib and the card "COMMITTEE LOANER JET" | [new-code][new-art] S · Must |
| **01** | new | B+S | **The sortie** (§1.3), 2:00, camera locked | waves | LOOP, POW, drain, red squadrons, AYACO | T1-lite, T4, vehicle state · Must |
| **02** | new | B+C | Lands automatically (a 90-f landing glide); the tally; **checkpoint 1**. Walk right (main) or ride the elevator down (secret) | none | **Lamp board**: 4 BG lamps, one per red squadron destroyed; at 4/4 the elevator unlocks | T3 [new-code] S · Must. Re-sortie catapult: Should |
| **03-05** | v01-v04 (4 → 3) | B+T | Climbs the tower shaft by ladders | `$27`/`$28` panda drums (2 per screen max), `$29` crawler | Item pocket on 04 behind the vanilla v03 breakable (tiles `$0C-$0F`): big energy, charged Power punch | [engine-ok] S · Must |
| **06** | v05 | B+T | Top of the tower | `$2D` stompers, `$1B` bomber | vanilla updrafts `$A` over fans `$C` | [engine-ok] · Must (the first gust: Should) |
| **07** | v06 | B+T | Deck with two updraft columns. **The sortie callback** (§1.4): two propeller Met fighters strafe the deck; the red one drops a POW that rides the updraft | 2 fighters, `$36` top (1) | vanilla updrafts | [new-code] S · Must |
| **08** | v07 | B+T | Updraft deck under the vanilla ceiling spikes | `$2D`, `$36` | vanilla | [engine-ok] · Must (the gust-timing puzzle: Should) |
| **09** | v08 | B+O | Open sky with floating girders | `$34` shield-cars (featured enemy) | | [engine-ok] · Must (Kite Mets: Should) |
| **0A** | v09 | B+O | Open sky; **hidden-room tell**: a seagull stands on one cloud | `$34` | The one solid cloud and a rope ladder's last 16 px at the top of the screen (§1.6) | [engine-ok] layout + seagull [new-code][new-art] S · Must |
| **0B** | v0A | B+O | Deck, then the ladder up (vanilla up exit) | `$36`, `$34` | | [engine-ok] · Must |
| **0C** | v0B+v0C (2 → 1) | B+O | Ladder climb; 1-UP on a side ledge (vanilla v0B) | `$75` beetle | | [engine-ok] S · Must |
| **0D** | v0D | B+O | Right along the top | `$27` | | [engine-ok] · Must |
| **0E** | v0E | B+D | Down the second tower | `$59` big robot | | [engine-ok] · Must |
| **0F** | v0F+v10 (2 → 1) | B+D | Down into the dark engine base | `$29` | | data S · Must |
| **10** | v11+v12 (2 → 1) | B+D | Rubble floor under the ceiling spikes, then up | `$36`, `$27` | vanilla fans (constant engine-fan push zones: Should) | data S · Must |
| **11-12** | v13-v14 | B+D | Shutters; **checkpoint 2** at 11 | | | [engine-ok] · Must |
| **13** | v15 | B | **Wind Man** (§1.7): the purple tower top; the windsock on the left wall | | Should: the cloud band behind the arena scrolls (T4) | Must |
| **18** | new | B+D | Secret: rides the elevator platform down from 02 | none | the lift rides through 02's down exit | T3 S · Must |
| **19-1A** | new | B+D | Service bays under the deck, in the vanilla dark-base art | `$29` crawlers, `$2D` (2 per screen max) | | data S · Must. Should: W-HANGAR bays, parked fighters, bomb carts (F.BLAST detonates them) |
| **1B** | new | B+D | Ladder up through a hatch | | | Must |
| **1C** | new | B+D | Shutter corridor; **checkpoint 2b** | | | Must. Should: the corridor on AYACO's wing, clouds rushing past |
| **1D** | new (copy of 13) | B | **Secret boss room: WING WALKER** (§1.7.4); v1.0 on the tower top at night. The kill sets SECRETS b0 | | | Must; the flying-wing arena Should |
| **1E** | new | B | **Hidden room "WEATHER BALLOON"** (§1.6) | | | Must |
| 14-17, 1F | - | | unused (5 spare) | | | |

Checkpoints: 02 (after the sortie), 11 (shutter), 1C (secret shutter). A death in the sortie restarts at 00, one screen
and a launch (about 4 s), and clears that sortie's lamps.

### 1.3 The sortie (screen 01)

#### 1.3.1 The vehicle and the rules

**SKY ACE** runs on tech's free-flight vehicle state (R1.10, lane flag off) [new-code] M · Must (tech; this doc's part
is data and the POW/LOOP rules, S):

- Rockman rides the loaner in 8 directions at 1.5 px/f, no gravity, no fuel use (the fuel bar is hidden). Screen clamp
  x 16-232, y 24-200.
- **B fires the vehicle's buster only** (a vehicle, not a form: consistency-36; and the weapon slot holds only the
  buster's shot tiles, R2.3). Shots use slots 1-3 (R1.11).
- **A = LOOP** (1942): a 48-f loop-the-loop of radius 20 px with full invincibility. 3 loops per sortie, shown as
  three "R" icons by the HUD widget under the life bar; +1 per POW taken as POW (max 3).
- **The 1943 energy rule.** Life drains 1 HP every 600 f in flight. A plane costs 3 on contact, a bullet 2. That is
  about 12 HP over the whole sortie; the four POWs give back up to 24.
- **Bands (T4, R1.9).** Sky band y 0-151 (clouds, a 512-px loop, 1 px/f; set at NMI); sea band from line 152 (W-SEA,
  2 px/f): one IRQ band. The pop-up window moves to the **bottom** on this screen (§0.6) and replaces the sea below its
  top line while open. Band budget: sky, sea, window, ExRAM flush = 4 entries of 24; the sound update rides the sea
  band (line 152), with 48 band-free lines before the bottom window's band (R1.9 asks for 36).
- **Lag (R1.8)**: player 1 + script with the director 1 + shots 3 = 5; **the enemy side holds at most 4** (planes,
  enemy bullets, the POW, AYACO's parts, a bomb). The director delays a spawn for as long as 4 enemy-side slots are
  taken (a lingering POW and an open pop-up each take one, §0.5) and never drops it.
  Flicker: ≤ 3 fighters in any 8-px band (art_audio §3.4); chains keep that.

#### 1.3.2 The wave list (v1.0)

t in seconds from launch. The director spawns from data, so CASUAL (and later HARD) are just other lists.

| t | Wave | Count | Path | Live at most |
|---|---|---|---|---|
| 0-1 | Launch | | "TAKE OFF!" | |
| 3 | Fighters (green) | 4 | chain from the right on a sine path, 30 f apart | 3 |
| 10 | Fighters | 3 | a V from the upper right, together | 3 |
| 16 | Fighters | 3 | **from behind** (left edge), one at a time, 40 f apart, overtake and turn: 1943's surprise from the rear | 2 |
| 22 | **RED SQUADRON 1** | 5 | chain on the 1942 loop path, 40 f apart | 3; all 5 down → POW, lamp 1 |
| 32 | Dive fighters | 4 | in pairs from the top; each fires one bullet | 2 + 2 bullets |
| 42 | **RED SQUADRON 2** | 5 | chain from behind | 3; POW, lamp 2 |
| 52 | Fighters | 6 | two chains of 3, top and bottom, staggered | 3 |
| 62 | **RED SQUADRON 3** | 5 | pincer: the chain enters from the top, then from the bottom | 3; POW, lamp 3 |
| 75-110 | **AYACO** | 1 | enters from the right, cruises in the right half, bobs ±8 px; leaves at 110 s if alive | body + 2 engine pairs + 1 bomb = 4 |
| 112 | **RED SQUADRON 4** | 5 | a wide chain led by a **gold leader**, who fires once | 3 + 1 bullet; POW, lamp 4 |
| 120 | Landing | | the flight deck slides in from the right | → 02 |

A lamp pings and lights in the HUD (icon row) the moment a squadron is wiped. Should: the destroyer (a 64-px BG ship in
the sea band with 2 flak turrets, HP 3, bursts every 70 f) at t = 42 with red squadron 2 moved to t = 48; it needs 2
enemy-side slots, so that wave thins to a chain of 2 while it passes.

#### 1.3.3 The POW (1943)

The last plane of a red squadron drops a POW that drifts left at 0.5 px/f and leaves after about 6 s. **Shooting it
cycles it** and knocks it 8 px up (it can be juggled). It is one enemy-side object.

| Shown | Taken | Effect |
|---|---|---|
| **POW** | +6 HP, +1 LOOP | |
| **3-WAY** | 15 s | one volley of 3 shots at −20°, 0°, +20° (all three shot slots) |
| **AUTO** | 15 s | hold B: one shot per 6 f, 3 on screen (R1.11) |
| (back to POW) | | |
| **YASHICHI** | 8 hits on the same POW within 240 f turn it into Capcom's spinning pinwheel | full HP, 3 LOOPs, and the first take ever grants the **YASHICHI chip** (§1.6) |

#### 1.3.4 AYACO, the big bomber (1942's boss, parody name)

v1.0 is the simple build (T8: one controller and two part objects) [new-code][new-art] M · Must:

| Part | HP (proposal; systems' mid-boss default column owns it) | Behaviour |
|---|---|---|
| Body (the controller) | invulnerable | Cruises in the right half. The bomb bay opens every 240 f and drops one bomb Met (contact 3) that bursts at the bottom of the screen |
| Engine pair, left / right | 10 each | Smoke below half |

Both pairs destroyed: AYACO tilts and falls out of the sky (+1 to the planes destroyed; the WND-05 line is Should). Lag: body + 2 pairs +
1 bomb = 4 enemy-side slots, so no fighters fly during AYACO, and the bomb bay stays shut while red squadron 3's POW
lingers (§0.5). Mid-boss fight id `$08` (meta, consistency-44) with the
arena "01, director at the AYACO wave" serves GP Rush when it ships (Could).

**Should (v1.1):** four engines of HP 6, a tail gun (3-shot burst every 90 f), and AYACO drawn as BG art in the sky
band (one controller object with BG hit boxes, which also frees its part slots).

#### 1.3.5 The tally and the LAND skip

- **Tally** on 02: the pop-up shows "SHOOTING DOWN 87%" (planes destroyed / planes spawned; AYACO counts as one plane),
  then the lamp board lights one BG lamp per completed red squadron (`map_set`). 100 % plays a vanilla fanfare SFX in
  v1.0 (the ACE stinger is G28, Should) and earns the **ACE** act. The best percentage is Wind's `VENUE_REC` (meta).
- **LAND** (R3.8, design-16) [new-code] S · Must. Once the venue is cleared (`STAGE_CLEAR`, meta 2), 00's screen script
  flips a deck hatch open at the left end, with a LAND sign. UP at the hatch (a T3 door) plays a 60-f "COMMITTEE
  SHUTTLE" cut and drops Rockman on 02. The run is marked **LANDED**:
  - the lamps stay dark and the elevator stays shut: no secret exit this run;
  - no YASHICHI and no ACE act this run (the POWs and the tally never happen);
  - systems adds the sortie's fixed **7,200 f** to the run's `T`, so the skip never buys TIME;
  - the tally reads "LANDED".

### 1.4 The tower (v1.0) and the gust decks (Should)

**v1.0.** The tower (03-12) is the vanilla tower, shortened by two screens, with vanilla's updrafts and fans and one
**callback to the sortie** (design-16) [new-code] S · Must: on 07, two propeller Met fighters dive across the deck
(the sortie's object on a deck path, SET-WS1 at `A0`, clear of 07's vanilla sets). The red one drops a POW that drifts
**up the updraft column** at 0.5 px/f. On foot a POW is +6 HP; shooting it makes it hop, but it does not cycle (the
3-WAY and AUTO buster rules exist only on the vehicle). Lag on 07: 1 + 1 + 3 + 2 fighters + 1 top = 8; the POW takes
the red fighter's slot.

**Should (v1.1): the gust decks**, the venue's second set piece. `OBJ_GUSTCTL` (VA-GUST) on 06-0B and the engine fans
on 10:

| Phase | Frames | What you see and hear |
|---|---|---|
| CALM | 120 | windsock limp |
| WARN | 30 | the windsock stiffens toward the coming direction; a whoosh SFX; leaf and debris sprites blow |
| GUST | 150 | push 0.75 px/f on the ground, 1.0 in the air (Jet included) |

The direction list is per-screen data (06: L, R; 07: R, R, L; 08: L only, toward the spikes; 0B: R, L). W.STORM
tornados ride a gust. **Kite Mets** (09) ride the gust and drop straight down when it stops. The engine fans on 10 are
a GUST phase that never ends, 0.5 px/f, with no windsock (the fan art is the tell). The windsock is BG (as in the boss
room), and the controller lives in the screen script, so a gust deck costs no slot.

### 1.5 Secret exit: the ace's elevator

- **Requirement**: destroy all five planes of each of the **four red squadrons** in one sortie. No adaptor.
- **Tells**: the 4 lamps on the lamp board beside the elevator and as HUD icons in the sortie; a lamp pings and lights
  the moment a squadron is wiped; the elevator's sign reads "ACES ONLY".
- **Route**: 02 elevator ↓ 18 → 19-1A service bays → 1B ladder ↑ → 1C (checkpoint 2b) → **1D WING WALKER**. The kill
  sets SECRETS b0 (meta 2).
- **Debrief hint (WI0, tier B)**: "FOUR RED SQUADRONS, FOUR LAMPS. THE ELEVATOR ONLY TAKES ACES."
- Should: the **re-sortie catapult** at 02's left end relaunches into 01 without dying, so a player can retry the
  squadrons at once.

### 1.6 Hidden room and behaviour chip

**Hidden room 1E "WEATHER BALLOON"** [engine-ok] layout + seagull [new-code][new-art] S · Must.
- Entry: on 0A, one cloud is solid (one metatile with collision 1 and cloud art: CX's "clouds are not floors",
  inverted). A seagull (an `$F4` object, harmless) stands on it and squawks every 4 s. A rope ladder's bottom 16 px
  hangs above it; climbing it takes the up exit with an explicit target → 1E.
- Content: the balloon's gondola: the **sponsor envelope**, an E-tank, two large weapon energies (systems sets drops).
- Exit: the ladder down to 0A.
- **Hint (WI1, tier B)**: "A SEAGULL WAS STANDING ON A CLOUD. CLOUDS AREN'T FLOORS... ARE THEY?"
- Should: W.STORM's Updraft alt (R2.4) reaches the ladder without the cloud.

**Behaviour chip: YASHICHI** [new-code] S · Must.
- Earned by juggling one POW through 8 hits within 240 f (§1.3.3). The first take ever grants the chip; on replays the
  capsule is a token (systems §6.7).
- Effect (systems §9.2 #13): once per stage, the first time HP falls to 4 or less, the pinwheel spins and refills HP.
  **YASHICHI and DARUMA are one "second wind" family and cannot be equipped together** (R2.6).
- Tells: the POW visibly changes on the first hit; the pinwheel is a famous Capcom secret; WND-02 (Should) adds
  Kalinka's "It changes when you shoot it!".
- **Hint (WI2, tier B)**: "SHOOT THE POW. THEN KEEP SHOOTING IT."

### 1.7 Boss: Wind Man, "MASTER OF WIND"

Arena: 13 (v15, the purple tower top, gold pillar floor), with the BG windsock on the left wall. HP and damage per
systems (vanilla HP 27). The vanilla AI already owns the hard parts (the fan pull, the pinwheels, the cross-room hop);
the rework adds a **push** phase (the vanilla pull with its sign flipped: AI, not VA-GUST) and the 1943 pinch.
[new-code] M · Must.

#### 1.7.1 Patterns (frames at 60 Hz)

| Id | Name | Timeline | Notes |
|---|---|---|---|
| A | **HEADWIND** | 0: the fans **push Rockman away** at 0.75 px/f (1.0 in the air) for 180 f. f30 and f90: a W.STORM tornado rolls along the floor at 2 px/f toward Rockman (contact 3); each stops at the far wall and becomes an **updraft column** for 60 f | Jumping into the column lifts you to y `$40`: a preview of W.STORM's Updraft alt (a boss move, R2.4) |
| B | **CROSSWIND HOP** | 10-f crouch, a jump to the other third of the room, peak y `$6B`, 50 f | vanilla move |
| C | **SUCTION** | **Pull** toward him at 0.75 px/f for 150 f (vanilla). f40 and f100: two pinwheels `$9A` go up and fall at Rockman's x. His fan blades: 4 on contact | vanilla move, timed |
| | Cycle | A, B, C, B (430 f) | The windsock always shows the current direction, 12 f ahead |

#### 1.7.2 Pinch (HP ≤ 9): SKY ACE

- **D: 1943 LOOP** (72 f), once per cycle: a vertical loop of radius 40 px, then a dive at Rockman's last x (contact
  4). Shots ping off him during the loop.
- **E: RED SQUADRON** (at most once per 1,200 f): Wind Man hovers and calls **3** red propeller Mets, a chain across
  the top at 2 px/f. All 3 down → a POW (+6 HP; it hops when shot but does not cycle on foot). The boss uses the
  venue's own mechanic.
- In A and C the wind flips every 90 f (the windsock flips 12 f first).

Lag: A = player + script + boss + 2 tornados + 3 shots = 8; C = 8 (2 pinwheels); **E = 9** (3 planes; the POW takes
the last plane's slot). The pinch set (24 tiles, §1.1) streams during D's first loop, which is invincible.

**Credits mode** (fortress §6.2; tech's `IFCREDITS`, §4.6) [new-code] S · Must, costed in fortress's ending row: the
v1.0 credits show Wind Man fighting in 13 with no Rockman. The A, B, C, B cycle loops at full HP (no pinch), aimed at an
empty spot (x `$40` on the floor) instead of Rockman; the push and the pull still turn the windsock and roll the
tornados, with nothing to move. Fallback (fortress's): his card strip only.

#### 1.7.3 Weapons in this fight

| Weapon | Effect | Tags · tier |
|---|---|---|
| **C.FLASH (weakness, 4 / 16 f)** | **STALL**: his fans stop for 120 f (no push, no tornados, no pinwheels); if airborne he drops; smoke puffs sputter from his propellers; the windsock goes limp. It replaces the generic weak freeze (SC9); damage keeps working (R2.2) | [new-code] S · Must |
| W.STORM (own) | SC4: the **first** W.STORM hit is **absorbed**: no damage, his suction +50 % for 60 f (vanilla's "landed only once" quirk, on purpose; WND-09 "He LIKES that!"). Later hits are the own cell (1 / 60 f) | [new-code] S · Should (the SC4 hook is Should) |
| C.FLASH's Time Stop alt | the STALL lasts 180 f | Should (with the alts, R2.4) |
| Charged Power punch (PUNCH★) | knocks him out of B or D (he lands) | [new-code] S · Should |
| Jet form | a headwind halves Jet speed, a tailwind doubles it: a preview of W.STORM's Tailwind synergy | Should |
| Y.SPEAR (G, 3 / 20) | jams a fan: the push stops for 30 f | Could |

Defeat (Could): his propellers spin down and he spirals to the floor like a paper plane.

#### 1.7.4 Secret room 1D: WING WALKER

- **v1.0**: 13's layout with a **night palette** (the tower top under the stars), same AI, pinch at HP 12. Kill: the
  YOU GET card per story S11, and SECRETS b0.
- **Should (the arena twist)**: the fight on top of AYACO's wing in flight: the cloud band rushing past at 3 px/f
  (T1-lite), open wing edges (a fall is a pit death), 16-px lips at both ends so a grounded Rockman cannot be pushed
  off by the fans alone, only while jumping. It brings the W-HANGAR art for 19-1C.

### 1.8 CASUAL levers (R2.9, Must)

| Lever | SKY ACE (NORMAL → CASUAL) | How (systems §13.4) |
|---|---|---|
| Reflex windows ×2 | the windsock's warning 12 → 24 f | `REFLEX` (`TIERVAL` + INPUT_LAG) |
| Mash counts −40 % | none in this venue | none |
| Set-piece timers +50 % | the 1943 drain every 600 → 900 f; a POW stays 6 → 9 s (drift 0.33 px/f); the YASHICHI juggle window 240 → 360 f (a timer, not a reaction window) | `TIERVAL` |
| +1 checkpoint per section | sortie: a restart point at t = 60 s (after red squadron 2; the lamps earned are kept; the director resumes at that list index); tower: 0A; secret route: 1A | the sortie: a CASUAL poke on the director's restart index; 0A, 1A: tech's dormant checkpoint objects, woken by a CASUAL poke |
| Skill-gated secrets −1 step | a red squadron counts at 4 of 5 planes (the secret exit); the YASHICHI needs 6 hits (the chip) | `IFCASUAL` in the two predicates |

### 1.9 HARD pokes (Should, R0.3 item 3; tech §5.5 format)

| Section | Poke | Kind |
|---|---|---|
| Sortie | drain every 360 f; red squadrons fly at 2.5 px/f and each plane fires once (the chain still keeps ≤ 3 planes + 1 bullet); AYACO engine pairs HP 14; 2 LOOPs at start | wave list + constants |
| Sortie | the POW drifts at 0.75 px/f (a shorter juggle); the YASHICHI still needs 8 hits | constant |
| 08 | one more spike row under the ceiling | layout |
| Gust decks (when they ship) | GUST 1.0 / 1.25 px/f; WARN 30 → 20 f; 07's two updraft columns removed (blocks `$A` → air) | constants + layout |
| Wind Man | pinch at HP 13; A's push 1.0 px/f; RED SQUADRON every 900 f; tornados 2.5 px/f | AI branch |

### 1.10 Text, commentators and the partner

- **v1.0 text** (R4.5; story §10.4 counts **10 Must strings** and 2 labels, the single source: R8.4): "TAKE OFF!",
  "COMMITTEE LOANER JET", the tally, "LANDED", WND-08 (the elevator unlocks: a
  secret line), WND-10 (first C.FLASH: the first-weakness line), 4 death lines (story picks from "Mayday, mayday!",
  "He forgot the loop button.", "Gone with the wind.", "The windsock tried to warn him.", "That cloud was NOT a
  floor.", "Even 1942 gave you three loops!"), and the hints WI0-WI2. The "ACES ONLY" and LAND signs are BG art.
- **Should**: the flavour hooks WND-01-07, 09, 11 (launch, first POW, squadron down, AYACO, 100 %, first gust, the
  pinch loop).
- **Break Man (Should, with the partner)**: 01 is in the venue's `NO_TAG` mask; the call row is greyed during the
  sortie ("NO PASSENGERS"); on the gust decks the gusts push him at half strength (his scarf flaps). No tag shortcut.

### 1.11 Homage moments (the screenshot list)

1. The catapult launch off the Committee carrier, Rush in a RENTAL bib.
2. Juggling a POW through 3-WAY and AUTO until it spins into a Yashichi.
3. The LOOP button: Rush loops through a bullet chain, three times per sortie.
4. AYACO falling out of the sky in smoke.
5. "SHOOTING DOWN 87%" on the deck, and four lamps that decide the secret exit.
6. A seagull standing on the one cloud that is a floor.
7. Wind Man flying a 1943 evasive loop, then calling his own red squadron.
8. C.FLASH stalls his fans and he sputters to the floor.
9. v1.1: the secret fight on the wing of the airborne bomber.

### 1.12 Weapons as tools in this venue (VARIETY)

On foot only (the sortie fires the buster): C.FLASH drops the `$34` shield-cars and stalls Wind Man; Y.SPEAR's pierce
goes through a shield-car's shield; SILVER.T's arc reaches the `$27` drums above you; the charged Power punch opens the
04 pocket. Should: F.BLAST on the hangar bomb carts; W.STORM's Updraft to the hidden ladder.

---

## 2. Knight Man: HERO'S QUEST

**Pitch.** Knight Man's castle is run as a hero's-quest theme park, "TANTE-GP CASTLE". A King gives you the quest, a
Sage teaches the verbs, chests hold MAGIC KEYS that locked doors eat, corridors throw **ENCOUNTER!** command windows at
you, the vanilla spike ceiling becomes a monster with HP, a Metal Metslime runs away with the critical-hit chip, and
the hidden stairs are where the genre put them: behind the empty throne. Knight Man narrates his own attacks in a
battle log, so every move is telegraphed. **Built after text v1b** (R1.4): the whole venue is verbs and windows.

Vanilla facts used: layout `$33:$B000`; tileset `$2D:$80` (blocks 255/256, metatiles 155, BG tile ids 250 / 6 free);
one BG set `$9E` for the whole stage plus the torch animation `$9F-$A1` on v08-09 (`$39:$888A`); palettes
`$74`/`$78`/`$82`/`$CD`/`$7B` and distinct **revisit palettes** in bank `$28`; music `$07`; collision group 2. Spike
ceiling v03-06: script `$3F`, init `$39:$8833`, IRQ chain `$11` (handler `$C337`, **logic inside the IRQ**), latch `$B0`,
collision offset for stage 6 at `$3E:$DA40`. Checkpoints v0B and v16 (plate route v19). Plate **A** in room v1A, through
the Power pillar in v15 (charged punch) and two more Power walls in v18. Boss `$95`, mace `$96`, shield = attack class
3 (front shots reflect; only the full punch always hits); weakness Y.SPEAR (4).

### 2.1 Tileset slot and art (art_audio §4.7 owns the counts; v1.0 deltas marked)

| Item | Content | Tags · tier |
|---|---|---|
| Slot **TS_KNIGHT** | Copy of `$2D:$80` tables (Knight shares bank `$2D` with Centaur in vanilla; the new slot ends that coupling) | [engine-ok] S · Must |
| Kept | `$9E` castle, battlements, halls, arched windows, chains, spiked ceilings, banners, machine hall, gates, ladders; torches `$9F-$A1`; v00's sunset sky; the revisit palettes | [engine-ok] |
| **K-DQ** third (~40 at ids `$B5-$DC`, swapped in on 01, 0D and 15, which leave `$B5-$FF` free; the machine hall 12-14 needs `$97-$DF`, so the 12 exit restores them) | Two thrones (32×32), stone tablet, trapdoor (the alternate of 0D's floor), hidden-stairs metatiles (the alternate of the v15 pillar) | [new-art] S · Must. The inn bed (+8, swapped on 0A-0B): Should |
| Window frame | the text engine's own frame tiles (art_audio §9.6) | [new-art] S · Must (shared) |
| **SET-KN1** `C0+48` | King (2), Sage (2), chest closed/open (2), MAGIC KEY icon; composites of vanilla NPC frames, crown and palette new (R5.1) | [new-art] M · Must (~32 tiles). Princess Roll in a gown, the Innkeeper, Roll's Love heart: Should |
| **SET-KN2** `C0+48` | Metslime (a vanilla Metall helmet on a teardrop body, bounce 3), Metal Metslime (a grey palette + a 2-tile shine), Killer Chest (3), ceiling winch (2) | [new-art] M · Must. The sconce flame: Won't (R3.1, §2.5) |
| Champion pinch set | ENRAGED (red eyes, mace raised), the "shield knocked aside" weak reaction | [new-art] S · Must (12 tiles) |

### 2.2 Screen-by-screen

| GP | From | The player does | Enemies | Set pieces | Tags · tier |
|---|---|---|---|---|---|
| **00** | v00 | Starts on the tower top under the sunset. The **Sage** at the gate (UP to talk): "PRESS UP TO TALK. TO SEARCH, STAND STILL AND HOLD DOWN." Drops down | none | Teaches both verbs | T2 v1b, VA-SEARCH S · Must |
| **01** | v01 | **The King's hall.** The King: "O DESCENDANT OF LIGHT! THE KNIGHTLORD AWAITS. TAKE THIS KEY." The tutorial chest sits on the floor in the path (unmissable): MAGIC KEY 1. Searching behind the King's throne: "THOU FINDEST NOTHING. THIS IS NOT THAT THRONE." (the false lead) | `$29` armadillo | 1-UP behind the vanilla Power block (charged punch) | T3 [new-code] S · Must |
| **02** | v02 | Down the shaft; a **locked door** at the bottom eats key 1, then right | `$3D` pod (1, not 3) | "THOU HAST NO KEY." if somehow keyless | T3 S · Must |
| **03-06** | v03-v06 | **The Trap Hall** (§2.4): fight the ceiling or run under it | `$6E` lance knights (1 per screen, 3 in all) | Spike ceiling with 4 winches; palette cycle `$75-$77` kept | [new-code] S · Must |
| **07** | v07 | Up | `$65` skeleton robot | | [engine-ok] · Must |
| **08-09** | v08-v09 | **Tower of torches** (torch CHR animation kept) | `$67` swooper | The green ring blocks (collision `$D`) stay F.BLAST pockets: one holds a large weapon energy, the other the **20-bolt pouch** (prize #0) | [engine-ok] S · Must |
| **0A** | v0A | Tower top | none | v1.0: plain. Should: **Princess Roll** at a window (§2.6) | Must / Should |
| **0B** | v0B | **Checkpoint 1** | none | Should: the **INN** (§2.6) and the sign "THY DEEDS ARE RECORDED." (KNT.S25) | [engine-ok] · Must; Inn Should |
| **0C** | v0C | **ENCOUNTER 1** at x `$40` (§2.3) | 3 Metslimes, 1 Killer Chest | Victory chest: MAGIC KEY 2 | VA-ENCOUNTER M · Must |
| **0D** | v0D | Walks on, then up (vanilla up exit). **Hidden-room tell**: a floor glint at x `$A0` (§2.7) | none (2 small energies, vanilla) | Search → trapdoor → down exit to 1E | VA-SEARCH S · Must |
| **0E-0F** | v0E-v0F | Climb | `$70` red spearman as the ROYAL GUARD | | [engine-ok] · Must |
| **10** | v10 | The vanilla high E-tank now sits in a **chest** on the same ledge (y `$17`) | `$C6` riders (2) | | [engine-ok] S · Must |
| **11** | v11 | Down | `$3C` (vanilla) | | [engine-ok] · Must |
| **12** | v12 | **"A METAL METSLIME APPEARS!"** (§2.7) | Metal Metslime | It flees after 240 f | [new-code] S · Must |
| **13-14** | v13-v14 | **ENCOUNTER 2** at 13 x `$60` in the blue machine hall: "KNIGHT GUARDS DRAW NEAR!" | 3 `$6E` lance knights | Victory chest: MAGIC KEY 3. The vanilla `$3A` mines leave this screen (their `D0` tiles meet SET-KN1/2: art_audio §4.7) | VA-ENCOUNTER · Must |
| **15** | v15 | **The empty throne** on the arch platform; behind it, the dip with the vanilla Power pillar. **Search** there (or charged-punch the pillar, the vanilla way) → hidden stairs ↓ 18, with the key check (§2.5). Main route: right to the shutter | `$2D` (2) | §2.5 | VA-SEARCH S · Must |
| **16** | v16 | Shutter corridor, **checkpoint 2** | | | [engine-ok] · Must |
| **17** | v17 | **Knight Man** (§2.8) | | The battle log in the pop-up window | Must |
| **18** | v18 | **The Knightlord's basement** (lit, §2.5): a **ladder up to 15** at its entry (R3.9); two **locked doors** where vanilla had two Power walls (a key **or** a charged punch opens each); the vanilla spike pit | `$2D`, `$3A` | | T3 S · Must |
| **19** | v19 | Shutter corridor, **checkpoint 2b** | | | [engine-ok] · Must |
| **1A** | v1A | **Secret boss room: THE KNIGHTLORD** (§2.8.4), v1.0 in Knight's vanilla revisit palette. Kill: KNIGHT.C + the plate A pickup + SECRETS b0 | | The offer | Must; the throne staging Should |
| **1E** | new | **Hidden room "LIGHT'S TABLET"** (§2.7) | | | Must |
| 1B-1D, 1F | - | unused (4 spare) | | | |

Checkpoints: 0B, 16 (shutter), 19 (secret shutter).

**Key economy** (the genre's keys are consumable): 3 keys (01, 0C, 13) for 3 doors (02, and the two in 18). **Running
from an encounter forfeits its chest**, so a player who ran needs the charged Power punch for one basement door, and
the stairs say so (§2.5). Keys are T3's per-stage key counter in the run block (tech §7: round 1's open question 4)
and are not kept after the stage. The HUD widget shows a key icon and the count beside the life bar while in this venue.

**Lag (R1.8)**: encounter 1 = player + script (the encounter controller) + 3 shots + 4 enemies = **9**; the victory
chest spawns only after the wave. Encounter 2 = 8. The Trap Hall, per screen = 1 + 1 (the ceiling controller is in the
script) + 3 + 2 winches + 1 knight = 8. The boss = **9** at BLAZE (§2.8.1). The vanilla 14 % stretch (v0B-0C, `$2E`
with `$3D`/`$3E` pairs) loses its pods.

### 2.3 ENCOUNTER! (VA-ENCOUNTER) [new-code] M · Must

Fixed triggers, never random (golden movies and Time Attack need determinism; the joke is that the window *says* it
is random).

| Step | Frames | What happens |
|---|---|---|
| Trigger | 0 | Rockman crosses the trigger x. The music cuts |
| Transition | 16 | The command window **wipes open from the centre** (a wipe, never a flash: R3.5, so default and REDUCED match); vanilla shutters close both screen edges |
| Window (v1b) | - | "A METSLIME DRAWS NEAR! / COMMAND?" ▶FIGHT RUN SPELL ITEM. The music swaps to vanilla's boss theme in v1.0 (art_audio picks the id); G23 ENCOUNTER is Should |
| FIGHT | - | The window closes; the wave spawns |
| RUN | - | 1st try: "BUT THE WAY WAS BARRED!" (KNT.S11) and the enemies get a free hop; the menu returns after 60 f. 2nd try: "ROCK RAN AWAY." The shutters open, the enemies vanish, **no chest**, and nothing counts for VARIETY |
| SPELL / ITEM | - | Opens the vanilla pause menu on the weapon row / the E-tank row, then FIGHT |
| Victory | - | "THOU HAST DONE WELL. ROCK GAINED 12 EXP." A chest drops (MAGIC KEY); the shutters open; the stage music resumes |

An encounter won or run from stays done for the run.

| Object | HP | Behaviour | Tags · tier |
|---|---|---|---|
| `OBJ_METSLIME` (`$F4`) | 1 | Hops toward Rockman (period 48 f, 24-px hops), contact 2. Hides under the helmet like a Metall when shot from the front at range (shots ping off) | [new-art][new-code] S · Must |
| `OBJ_KILLERCHEST` (`$F4`) | 6 | Looks like the victory chest (a different shade once you know). Opens when Rockman is within 40 px; bites 12 f later (contact 4) and hops twice, then shuts (invulnerable while shut) | [new-art][new-code] S · Must |

EXP and levels (Could): EXP from encounters, the ceiling and the Metal Metslime; at 30 and 100 EXP a level-up
fanfare: "ROCK'S LEVEL WENT UP! (ROBOT MASTERS DO NOT LEVEL UP.)" No stat changes.

### 2.4 The Trap Hall: the ceiling draws near

**This is HERO'S QUEST's single use of the spike ceiling** (R3.1 moved the H4 and escape copies to other set pieces).

Vanilla: the spiked platforms on chains descend over v03-06 while the IRQ latch climbs (`$7D` → `$A3` in 220 f) and
`$069C` drives both the split and the collision offset.

GP twist (one twist on one vanilla set piece, CX lesson 5): **the ceiling is a monster with HP** [new-code] S · Must.

- On entering 03, a non-blocking pop-up: "THE CEILING DRAWS NEAR!" Play continues.
- `OBJ_WINCH` ×4 (two in 04, two in 05) hang under the ceiling platforms; each reads `$069C` every frame and rides
  with the platform. HP 3 each. NOFREEZE.
- All four destroyed: "THE CEILING IS DEFEATED! ROCK GAINED 8 EXP." A flag makes the ceiling **retract** (`$069C`
  back toward 0 at 1 px per 2 f) and stay up for the rest of the stage, including after deaths.
- Not destroyed: vanilla behaviour, unchanged.
- Engine: tech moves the ceiling's motion out of IRQ `$11` into a per-frame controller in the slot-22 script (M2.4;
  `EFFECTS` b2 CEILING, `EFX_PARAM`); the raster list only places the split. The retract is one flag that controller
  tests.

### 2.5 Secret exit: the hidden stairs behind the empty throne

The genre's most famous secret: in the final castle the throne is empty, and searching the floor behind it reveals the
stairs down to the real lord.

- **Requirement**: stand in the dip **behind the empty throne** on 15 and search (DOWN, 24 f). No adaptor.
  - The search flips the pillar's metatile id to its alternate (the map-edit service's per-id flip, R1.10), drawn as
    **stairs** going down (K-DQ).
  - The vanilla way still works: a fully charged Power punch opens it too (KNT-06: "That is NOT how you find secret
    stairs!"). This keeps the vanilla secret (BRIEF §6) and adds the homage.
- **The stairs check** (R3.9, design-22) [new-code] S · Must. Stepping onto the top stair reads the key counter. With
  2 keys, or Power owned, nothing is said. Otherwise a pop-up: "THOU HAST BUT 1 KEY. TWO DOORS LIE BELOW." (or "THOU
  HAST NO KEY."). It never blocks: **18 has a ladder up to 15 at its entry**, so a player short of keys climbs back
  and finishes by the main route, or returns on a replay with Power or with both encounter keys.
- **Tells**: the King's throne at 01 is occupied, this one is empty; the Sage taught the search at 00, and after a
  death he adds: "THE THRONE OF A LORD WHO NEVER SITS HIDES SOMETHING."; the King's own throne is the deliberate false
  lead. Should: Roll's Love pulses on 15.
- **Route**: 15 ↓ 18 (two locked doors; the ladder back) → 19 → **1A KNIGHTLORD**.
- **The basement is lit in v1.0.** Round 1's dark basement (RADIANT: each shot lights the room for 30 f; sconces to
  shoot) is **Won't**: R3.1 keeps the game's one "lights on a timer" set piece in the HALFTIME RIOT.
- **Debrief hint (KN0, tier B)**: "THE KNIGHTLORD'S THRONE IS EMPTY. WHY? SEARCH WHERE NO ONE SITS."
- Should (with the partner): Break Man's Break Shot opens the basement doors too (design-22).

### 2.6 NPCs: King and Sage (Must), Inn and Princess (Should: the second set piece)

| NPC | Where | Lines (draft) and effect | Tags · tier |
|---|---|---|---|
| King | 01 | Quest giver; key 1 comes from his tutorial chest. His line heads the death table (story's KNT.D1, the genre's scolding in new words, R8.4: "O ROCK! TO FALL SO SOON! ARISE, AND TRY AGAIN!") | T2 S · Must |
| Sage | 00 | Teaches UP to talk and DOWN to search; his after-death line is the stairs tell (§2.5) | T2 S · Must |
| Innkeeper | 0B | "WELCOME TO THE INN. ONE NIGHT IS 20 BOLTS. ▶YES NO". YES: a fade to black (R3.5), a 2-s inn jingle (Could; a vanilla SFX until then), full HP and weapon energy, "GOOD MORNING. THOU SEEMST TO HAVE SLEPT WELL." A bolt sink that systems confirms (it is not income) | T2 S · Should |
| **Princess Roll** | 0A | Roll (pit crew, BRIEF §2 cameo; story approved) in the venue's princess costume. "DOST THOU LOVE ME, ROCK? ▶YES NO". **NO → "NAY! THOU SHALT SAY YES!"** (KNT.S23: the famous loop in new words, R8.4) and the question again, forever (after 10 NOs: "...FINE. THE COSTUME IS HOT, ROCK."). YES: **ROLL'S LOVE**: a heart beside the life bar pulses within one screen of a secret (0D's glint, 12's Metslime, 15's throne). A tell-helper, not a secret | T2 S · Should |

### 2.7 Hidden room and behaviour chip

**Hidden room 1E "LIGHT'S TABLET"** [VA-SEARCH] S · Must.
- Entry: on 0D a floor tile glints for 8 f every 4 s; the search-spot object draws the glint itself, and it is the
  venue's only glint. Search on it: a trapdoor opens (the per-id flip), and Rockman drops through the down exit to 1E.
- Content, after the 1986 hero's hidden tablet: a stone tablet: "I, THOMAS LIGHT, HAVE LEFT THIS FOR MY DESCENDANT.
  TELL NO ONE. ESPECIALLY NOT WILY." The sponsor envelope, an E-tank and a 1-UP.
- Exit: the ladder up to 0D.
- **Hint (KN1, tier B)**: "SOMETHING GLITTERED ON THE FLOOR OF THE HALL. THOU DIDST NOT SEARCH."

**Behaviour chip: KAISHIN** (*kaishin no ichigeki*, the genre's critical hit) [new-code][new-art] S · Must.
- `OBJ_METALMETSLIME` on 12: "A METAL METSLIME APPEARS!" HP 8. **Every hit does exactly 1** whatever the weapon (a
  visible special case for systems' mid-boss rules); 2-f i-frames; hops erratically at 2 px/f; flees through the right
  edge at f240 ("THE METAL METSLIME ESCAPED!"). NOFREEZE. It returns on the next visit to 12 (after a death, or on a
  replay). Mid-boss fight id `$09` (meta), arena 12, for GP Rush when it ships.
- Killed: "A SPLENDID STRIKE! ROCK GAINED 1000 EXP." (KNT.S16) and the chip capsule drops (a token on replays).
- Effect (systems §9.2 #14, R2.4): criticals are Won't, so KAISHIN is always the deterministic **EXCELLENT MOVE**: +2
  on every 12th damaging boss hit, with the chime. "A SPLENDID STRIKE!" (story's paraphrase of the genre's
  critical-hit line, R8.4) is used only for KAISHIN.
- Best tools: many small hits (B.ATTACK's flakes, KNIGHT.C's return pass hitting twice, a fast buster).
- Tells: its own announcement and its escape line. Should: Roll's Love pulses here.
- **Hint (KN2, tier B)**: "METAL ONES FLEE FAST. HIT THEM OFTEN, NOT HARD."

Debrief order (meta): secret exit with plate A (KN0) → hidden room (KN1) → KAISHIN (KN2).

### 2.8 Boss: Knight Man, "MASTER OF MACE BALL"

Arena: 17 (v17, red hall, blue banners). Vanilla HP 27. Story's chivalric ham who narrates his own attacks. The rhythm
is vanilla's (jumps of 60-75 f, the mace about every 240 f), but every move is **announced in a one-line battle log**
a fixed lead time before it starts [new-code] M · Must.

- **The log uses the pop-up window** (top by default; consistency-26 resolves round 1's open question 6). The log has
  priority: the commentators are muted while it runs, and the first-weakness line (KNT-08) and the kill line wait in
  story's queue for the next 60 f without a log line.
- Intro (v1b): "KNIGHT MAN DRAWS NEAR! / COMMAND?" ▶FIGHT RUN. RUN: "BUT THE WAY WAS BARRED!" (always: he is a boss)
  and Knight Man acts first.
- The log's words are story's KNT.L01-L10. BLAZE and HEALMORE below are design labels only: on screen they are "a fire
  spell" and "a healing spell" (R3.3, R8.4).

#### 2.8.1 Patterns

| Id | Log line | Lead | Action | Vulnerable? |
|---|---|---|---|---|
| A | "KNIGHT MAN ATTACKS!" | 30 f | Mace `$96` sweeps along the floor across the room (60 f out, 40 f back); jump it | **Yes**: shield down for the whole 130 f |
| B | "KNIGHT MAN IS GUARDING." | 20 f | Walks at Rockman at 1 px/f for 90 f, shield up (front shots reflect, vanilla class 3), then a **shield bash** lunge of 32 px in 12 f (contact 4) | From behind only |
| C | (none: a physical move) | 10-f crouch | High jump onto Rockman's x, peak y `$3F`, 72 f airtime (vanilla). Landing **quake**: a grounded Rockman is stunned 16 f | In the air |
| D | "KNIGHT MAN CASTS A FIRE SPELL!" | 40 f cast pose, shield lowered | 3 fireballs: along the floor, +15°, +30°, at 2 px/f, contact 3. The mace stays in his hand | **Yes** during the cast |
| | Cycle | | B, A, C, B, D, C (about 650 f) | |

Lag: D = player + script + boss + 3 fireballs + 3 shots = **9**; A and the pinch's E add one mace object = 7. D's log
line closes as the cast ends, before the first fireball, so the text runner never makes 10 (§0.5).

#### 2.8.2 Pinch (HP ≤ 9): "KNIGHT MAN IS ENRAGED!"

| Id | Log line | Action |
|---|---|---|
| E | "KNIGHT MAN SWINGS THE MORNING STAR!" | The mace grows and orbits him (radius 28 px, 1 turn per 40 f) for 120 f while he walks at Rockman, then he flings it out; it **hangs at its farthest point** for 30 f and returns. Boss-move previews of KNIGHT.C's Morning Star synergy and its Hold alt (R2.4) |
| F | "KNIGHT MAN CASTS A HEALING SPELL!" | Once per fight. A 45-f cast, shield down. **Any hit during the cast** → "THE SPELL FIZZLED!" (the SPELLBREAKER act). Otherwise +6 HP |
| | Cycle | E, C, A, F (once), D, B |

The pinch opens with a 30-f invincible ENRAGED pose (the log line above), and the 12-tile pinch set streams under it.

**Credits mode** (fortress §6.2; tech's `IFCREDITS`, §4.6) [new-code] S · Must, costed in fortress's ending row: in 17
with no Rockman there is no intro window and no battle-log line (the lead times stay, silent); the B, A, C, B, D, C
cycle loops at full HP, aimed at an empty spot (x `$40`) instead of Rockman, and the landing quake stuns nobody.
Fallback (fortress's): his card strip only.

#### 2.8.3 Weapons in this fight (special cases in visible code)

| Weapon | Effect | Tags · tier |
|---|---|---|
| **Y.SPEAR (weakness, 4 / 16 f)** | **Pierces the shield**, even from the front during B: systems adds Y.SPEAR to SC1's pass-through list (consistency-35); it pierces, it does not break. The log: "THE SPEAR PIERCED THE SHIELD!", a 24-f stagger with the shield knocked aside; it replaces the generic freeze (SC9) | [new-code] S · Must |
| **PUNCH★** (Power, full charge) | The first one that hits the shield from the front: "THE SHIELD BROKE!". This venue makes it **permanent for the fight** (SC1 lets the venue decide; systems' default is 180 f): no more reflect, and his palette loses the shield colour. Morning Star and BREAK★ do the same when they ship (Should) | [new-code] S · Must |
| C.FLASH (G, 3 / 20) | Latched around the shield, as vanilla does with class-3 shields. The flash hits from anywhere, so it interrupts HEALMORE from across the room | [engine-ok] · Must |
| KNIGHT.C (own) | SC4, the first hit of the fight: mace meets mace, a CLANG spark, both bounce, no damage (KNT-10). Later hits: the own cell (1 / 60 f) | [new-code] S · Should |

#### 2.8.4 Secret room 1A: THE KNIGHTLORD

- **v1.0**: 1A (vanilla's own second boss room) in Knight's vanilla **revisit palette** (bank `$28`). The window (v1b):
  "STAND AT MY SIDE, AND HALF THE BRACKET SHALL BE THINE. ▶YES NO" (KNT.K01: the genre's famous offer in new words,
  R8.4).
  - **YES** (CX lesson: a Yes that hurts): the screen tints red (a palette fade, not a flash). "SO BE IT. THY HALF IS
    WAITING FOR THEE..." then "THY TOURNAMENT ENDS HERE. SLEEP NOW, AND SLEEP LONG." (KNT.K02-K03). A DISQUALIFIED
    card, **one life lost**, respawn at 19. KNT-09: C "Did he just take the deal?!" K "Papa, he pressed YES."
    [new-code] S · Must.
  - **NO**: "REFUSED? THEN FOLLY IS THINE, AND SO IS THIS FIGHT!" (KNT.K04). The fight starts with BLAZE.
- Same AI; pinch at HP 12. Kill: the YOU GET card per story S11 (KNIGHT.C), the **plate A** pickup, SECRETS b0.
- **Should (the arena twist)**: he sits on the real throne (K-DQ's second throne swapped into 1A) and rises from it.
- **Could**: TRUE FORM. At 0 HP, "KNIGHT MAN REVEALS HIS TRUE FORM!" He refills 12 HP in a red palette with a taller
  plume, and BLAZE comes every cycle. The kill line: "THOU HAST BROUGHT PEACE TO THE BRACKET. AGAIN."

### 2.9 CASUAL levers (R2.9, Must)

| Lever | HERO'S QUEST (NORMAL → CASUAL) | How (systems §13.4) |
|---|---|---|
| Reflex windows ×2 | battle-log leads 30 / 20 / 40 → 60 / 40 / 80 f; HEALMORE's interruptible cast 45 → 90 f; the Killer Chest bites 12 → 24 f after opening | `REFLEX` (`TIERVAL` + INPUT_LAG) |
| Mash counts −40 % | none in this venue | none |
| Set-piece timers +50 % | the Trap Hall's descent 220 → 330 f (latch step ×0.67); the Metal Metslime flees at f240 → f360 | `TIERVAL` |
| +1 checkpoint per section | after the Trap Hall: 07; the upper castle: 10; the secret route: 18 (at the ladder) | tech's dormant checkpoint objects, woken by a CASUAL poke |
| Skill-gated secrets −1 step | the Metal Metslime has HP 8 → 6 (the chip) | a CASUAL poke on its HP |

### 2.10 HARD pokes (Should, R0.3 item 3; tech §5.5 format)

| Section | Poke | Kind |
|---|---|---|
| Encounters | RUN never succeeds; encounter 1 adds a second wave of 2 Metslimes after the first (the cap holds); encounter 2 adds a second wave of 2 lance knights | data |
| Trap Hall | winch HP 3 → 5; latch step ×1.5 | constants |
| 08-09 | one F.BLAST pocket becomes a spike pocket (bait) | layout |
| 12 | the Metal Metslime flees at f150 | constant |
| Knight Man | log leads 30 / 20 / 40 → 18 / 12 / 28 f; HEALMORE twice; the broken shield regrows after 600 f | AI branch |

### 2.11 Text, commentators and the partner

- **v1.0 text** (R4.5; story §10.4 counts **44 Must strings**, the most of any venue, all on text v1b; the single
  source: R8.4): the Sage (2), the King (1 + his
  death line), chest and door lines, the false throne, the ceiling (2), the encounter windows (6), the Metal Metslime
  (3), the stairs check (2), Light's tablet, the battle log (about 10), the Knightlord (4), KNT-05 and KNT-06 (the
  stairs: secret lines), KNT-08 (first weakness), KNT-09 (the offer), 4 death lines (story picks from its 6), and the
  hints KN0-KN2.
- **Should**: KNT-01-04, 07, 10; the Inn, Princess Roll and the checkpoint sign. Could: the EXP lines.
- **Break Man (Should, with the partner)**: with him called, RUN always works ("BREAK MAN RAN AWAY. NOBODY WAS
  SURPRISED."). Princess Roll asks him instead: "DOST THOU LOVE ME?" "...No." "NAY! THOU SHALT SAY YES!" (he whistles and
  leaves the screen). His Break Shot opens the basement doors.

### 2.12 Homage moments

1. The stage starts with a King: "O DESCENDANT OF LIGHT!"
2. "A METSLIME DRAWS NEAR! COMMAND?" in a Rockman game, and "BUT THE WAY WAS BARRED!"
3. The spike ceiling has HP, and dies.
4. A Metal Metslime that takes exactly 1 damage from everything, then runs.
5. Stairs behind the empty throne.
6. The Knightlord's offer: say YES and the game puts you to sleep.
7. A boss that announces every attack in a battle log, and a HEALMORE you can interrupt.
8. Light's tablet in the hidden room: "ESPECIALLY NOT WILY."
9. v1.1: "NAY! THOU SHALT SAY YES!" until you say yes.

### 2.13 Weapons as tools in this venue

Y.SPEAR pierces Knight Man's shield and drops the lance knights; F.BLAST opens the `$D` torch pockets; B.ATTACK's
flakes and KNIGHT.C's double-hit return kill the Metal Metslime; C.FLASH is the "group spell" in encounters (it hits
every slime at once) and stops HEALMORE from anywhere; SILVER.T arcs over the lance knights' shields in the Trap Hall;
the charged Power punch opens 01's 1-UP, the throne pillar and the basement doors. Should: W.STORM lifts Metslimes off
the floor (they flip and are stunned 60 f).

---

## 3. Tomahawk Man: HIGH NOON FRONTIER

**Pitch.** A frontier town in Tomahawk Man's desert, run as a Capcom western **and a tournament event**. Three WANTED
posters at the trailhead name three bounties; an alley gallery mixes outlaws with townsfolk you must not hit; the
saloon hosts a judged quick-draw with a reaction timer; the 4:50 train crosses the desert with tunnels and a mounted
outlaw alongside; claim all three bounties and the Sheriff lets you take "the back way". Tomahawk Man is the
frontier's **rodeo showman, strict about duel etiquette** (R3.4): the fight opens, and later punctuates itself, with a
judged draw at HIGH NOON on the mesa.

Vanilla facts used: layout `$33:$A800`, **all 32 screens used**; tileset `$2C:$89` (221 blocks, 212 metatiles, BG tile
ids 255 / 1 free); base CHR `$94` (desert), `$96` (cave), `$95` (sunset), `$D7` (boss corridor); palettes `$50` / `$51`
/ `$95`; music `$06`. **Desert parallax**: script `$29`, init `$39:$86C0` (`$0672` = `$2E`, `$0677` = `$0C`, chain C at
line 46, X = camera/2), now the preset `RL_PARALLAX`. **Sunset shimmer**: script `$21`, init `$39:$85D8` (latch `$1F`,
chain E then F every 2nd line, 20 times), which also writes checkpoint v0A; now `RL_SHIMMER`, a self-re-arming routine
of **2 entries** (R1.9). Dome dispenser `$4F` (HP 14) on v05 and v10. **Secrets kept**: plate **B** in room v1F via
the right-hand ladder of v12 (no adaptor; `$F518[5]` = `$1F`); the **Energy Balancer** (`$8A`, `$0696`) in v1C via the
charged-punch block at v13's left; the **sky bypass** v18-1B via Rush Jet from v0A's hanging ladder (column 4, rows
`$00-$1F`; E-tank, big WE, big HP; drops into v0D). Boss `$9F`, AI `$31:$93EA`, tomahawk `$B0`, feathers `$B1`;
weakness PLANT.B (4).

### 3.1 Tileset slot and art (art_audio §4.6 owns the counts; v1.0 deltas marked)

| Item | Content | Tags · tier |
|---|---|---|
| Slot **TS_TOMAHAWK** | Copy of `$2C:$89` tables (35 free block ids before reclaiming) | [engine-ok] S · Must |
| Kept | `$94` desert, mesas (the parallax strip), cacti, signposts, blue metal pillars, orange pipes, mesh; `$96` cave; `$95` sunset sky and sun disc; `$D7` boss corridor | [engine-ok] |
| **T-TOWN** third (≤ 64 at ids `$BD-$FF`, free on the sunset screens v0A-0C) | False fronts, gallery windows and doors (each opened and closed by `map_set`), boardwalk, water tower, the outhouse (door and OCCUPIED / VACANT sign by the per-id flip), the WANTED board with three posters, store signs, the pianist's sign board | [new-art] M · Must |
| **T-SALOON** third (96 at `$A0-$FF`, free on v0D) | Bar, bottles, mirror, piano, swinging doors, the skylight (for the sky-bypass drop) | [new-art] M · Must |
| **T-TRAIN** set (~80; the train screens replace v10-v11, so their ids are chosen fresh) | Car roofs and couplings, station platform, rails and ties (a 512-px near loop), wheels (a 4-frame CHR animation, the torch technique), the "TUNNEL!" sign tiles | [new-art] M · Must |
| **T-MESA** third (~40 at `$BE-$FF`, free on v17; **replaces round 1's T-BOOTHILL**) | The **HIGH NOON MESA**: a flat mesa top at noon and distant buttes, **no graves** (R3.4); the flag judge's stand and flag (two states by `map_set`) | [new-art] S · **Must** (the R3.4 fix) |
| T-RODEO (~48) | The rodeo ring's fence and stands for 1F, with the WANTED: ROCKMAN poster | [new-art] S · Should (the arena twist) |
| **SET-TM1** `A0+64` | Outlaw (pop up, aim, shoot, hit), townsfolk (lady with parasol, pianist, Eddie at a window), tumbleweed | [new-art] M · Must |
| **SET-TM2** `E0+32` | "DRAW!" / "FOUL!" / "HEY!" words, bounty stamp, hat glint, bullet hole | [new-art] S · Must |
| **SET-TM3** `A0+64` | Six-Shot Sam (stand, draw, shoot, fall), the Sheriff, the conductor, the **flag judge** (a vanilla Metall composite with a flag; a sprite in the saloon) | [new-art] M · Must |
| **SET-TM4** `A0+64` | Sidewinder on his robot horse (32×32, a 4-frame gallop + shoot), the tunnel wall (32×48), a robber (a local copy of `$6C`) | [new-art] M · Must |
| **Cactus walker** (the `$12` re-skin, `A0-BF`) | The vanilla walker recoloured green with new spine tiles; "totem" leaves the venue (R3.4) | [new-art] S · **Must** (round 1: Could) |
| Champion pinch set | SHOWDOWN (the hat brim down, the etiquette bow), the draw | [new-art] S · Must (16) |
| Vulture re-skin of the `$64`/`$66` drones | | [new-art] S · Could |

The cowboy gunners `$6C` (`A0-CF`) conflict with SET-TM1/3/4: they stay in the desert and the mine (01-09), and on the
train only as SET-TM4's local copy (art_audio §4.6).

### 3.2 Screen-by-screen

| GP | From | The player does | Enemies | Set pieces | Tags · tier |
|---|---|---|---|---|---|
| **00** | v00 | **The WANTED board** (UP reads each poster; §3.3). Then right | none | Desert parallax (`RL_PARALLAX`, vanilla chain C) | T2 S · Must |
| **01-02** | v01-v02 | Desert trail | `$6C` gunners on crates (vanilla, the featured enemy), tumbleweeds (1 at a time; shot: a small bolt) | Vanilla breakables kept as Power pockets (01: two blocks on tile ids `$1C-$1F`; 02: the E-tank inside a block) | [engine-ok] S · Must |
| **03-04** | v03-v04 | Down into the canyon mine (cave CHR `$96`) | `$6C`, **cactus walkers** (the `$12` re-skin, R3.4) | | [engine-ok] + art · Must |
| **05** | v05 | **Bounty 1: DOMINGO DOME**, the vanilla dome dispenser (`$4F`, HP 14), wanted for claim-jumping. Locked screen (vanilla) | `$15` walkers, `$14` rocks (vanilla spawns; the dispenser waits while 3 are live) | The kill stamps CLAIMED over the poster icon (HUD widget) | [engine-ok] + S · Must |
| **06-08** | v06-v08 | The mine, then up | `$6E` drill tanks, `$18` turrets | v1.0: vanilla. Should: F.BLAST blows TNT crates open (one holds a W-tank) | [engine-ok] · Must |
| **09** | v09 | Dark mesh shaft up into town | `$70` | | [engine-ok] · Must |
| **0A** | v0A | **Sunset main street**; **checkpoint 1** (vanilla). The hanging ladder (the sky bypass, Jet) is kept exactly | none | Sunset shimmer (`RL_SHIMMER`, 2 entries) | [engine-ok] · Must |
| **0B-0C** | v0B-v0C | **The gallery** (§3.4): walk the street while windows and doors pop. **The outhouse** stands at 0C's right end (hidden room, §3.7) | outlaws; civilians | The pianist's sign board; its words pop up as the gallery starts | [new-code][new-art] M · Must |
| **0D** | v0D | **The saloon**: **Bounty 2: SIX-SHOT SAM**, best of three judged quick-draws (§3.5). The sky bypass drops in here through the skylight (vanilla's 1B → 0D exit, kept) | Sam, the flag judge | Could: the honky-tonk piano stops when you land from the roof | VA-DRAW S · Must |
| **0E-0F** | v0E-v0F | Down to the **station**; at the platform's end **the conductor reads the bounty count**, then "ALL ABOARD!" (§3.6) | `$29` (v0E), `$59` (v0F) | after the first clear, the EXPRESS choice | T2 v1b S · Must |
| **10-11** | new (replaces v10-v11) | **The 4:50 train** (§3.6): walk the roofs of four cars while the desert rushes by; **Bounty 3: SIDEWINDER** | a robber (1), Sidewinder | Tunnels; T1-lite + T4 (3 bands) | [new-code][new-art] L · Must |
| **12** | v12 | **Junction station**, **checkpoint 2**. The middle ladder (main) leads up to 13. The right-hand ladder (vanilla's plate route) is barred by the **Sheriff's gate** (§3.7) | a cactus walker (1) | The Sheriff hands out the SHERIFF STAR | T3 S · Must |
| **13** | v13 | Vanilla junction, unchanged: the left ladder up (main); at the corridor's left end the charged-punch block over the spike pit → **1C Energy Balancer**; the top-right pocket (only from 12's right ladder) → the right edge → **1D** | | | [engine-ok] · Must |
| **14-15** | v14-v15 | Mesa climb at sunset | `$64`/`$66` drones (vulture re-skin: Could), `$67` skull walkers | | [engine-ok] · Must |
| **16** | v16 | Shutter corridor (script `$4E`), **checkpoint 3** | | | [engine-ok] · Must |
| **17** | v17 | **Tomahawk Man, HIGH NOON** (§3.8) on the HIGH NOON MESA | | The flag judge's stand | [new-art] · Must |
| **18-1A** | v18-v1B (4 → 3) | **The sky bypass** ("VULTURE PASS"), vanilla: Jet up 0A's hanging ladder; lifts `$A0` over spikes, rising bubbles `$08`; the E-tank, big WE and big HP in 1A; 1A drops into 0D through the skylight | | Skips the gallery (and its civilians) | data S · Must |
| **1B** | new | **Hidden room "THE OUTHOUSE"** (§3.7) | | | T3 S · Must |
| **1C** | v1C | **Energy Balancer** room, vanilla (`$8A`; the item is the Energy Balancer chip, systems §9.2 #1) | | | [engine-ok] · Must |
| **1D-1E** | v1D-v1E | **The back way**: corridor and shutters (vanilla), **checkpoint 3b** | | | [engine-ok] · Must |
| **1F** | v1F | **Secret boss room: THE RODEO RING** (§3.8.5); v1.0 is the HIGH NOON MESA at dusk. Kill: SILVER.T + the plate B pickup + SECRETS b0 | | | Must; the ring's fence and stands Should |

The main route keeps vanilla's 24 screens (00-17). The second dome dispenser (v10) and the v11 claw screen give way to
the train. Checkpoints: 0A (town), 12 (after the train), 16 (shutter), 1E (secret shutter). Vanilla sets checkpoints
from screen scripts (`LDA #s / JMP $8416`), so the new one is a tiny new screen script ([new-code] S; feasibility-19).

### 3.3 Bounties (the Capcom western's posters)

| # | Poster (draft) | Where | Claimed by | Pays (prize index) |
|---|---|---|---|---|
| 1 | "WANTED: DOMINGO DOME. CLAIM-JUMPING. 15 BOLTS" | 05, the mine | killing the dispenser | 15 (#0) |
| 2 | "WANTED: SIX-SHOT SAM. CARD SHARP. 20 BOLTS" | 0D, the saloon | winning the best of three | 20 (#1) |
| 3 | "WANTED: SIDEWINDER. TRAIN ROBBERY. 25 BOLTS" | 10-11, the 4:50 | knocking him off the train before the third tunnel | 25 (#2) |

- The HUD widget shows three poster icons, stamped when claimed, for 120 f at stage start, at each claim, and while
  the conductor or the Sheriff speaks. Should: a pause-screen poster page.
- Bounties persist through deaths within the run. A missed Sam or Sidewinder can be retried after a death before
  checkpoint 2 (both respawn from checkpoint 1, 0A) or on a replay. Once checkpoint 2 (12) is reached, only a replay
  brings the train back, **and the conductor says so before you board** (R3.8, design-15). Should: the 12 platform
  re-boards the 4:50 once (design-15's option).
- "Prize money" is BRIEF §1's theme made literal. The bolts are paid once per save (systems §7).

### 3.4 The gallery (the alley-gallery rules) [new-code][new-art] M · Must

The **gallery director** runs in the slot-22 script. Eight window and door spots over 0B-0C are BG; a spot opens with
`map_set`, and a figure object spawns in it. A data list per screen gives (spot, kind, delay), started by camera
position; about 12 pops per walk-through.

| Kind | HP | Behaviour |
|---|---|---|
| Outlaw | 1 | Appears, shows a "!" for 24 f, fires one bullet at Rockman (2 px/f, contact 2), ducks after 60 f |
| Pianist | 1 | Holds sheet music. Never shoots |
| Lady | 1 | Parasol. Never shoots |
| **Eddie** | 1 | Behind "EDDIE'S GENERAL STORE". Never shoots. Hitting him: "HEY! I'M ON YOUR TEAM!" |

- Hitting any civilian: a "HEY!" word sprite, the **civilian counter** goes up, and that civilian ducks for good. The
  counter drives the SHERIFF STAR (§3.7). C.FLASH hits every open figure, civilians included (the judges' joke).
- Players who take the sky bypass skip the gallery; their counter stays 0 and the Sheriff treats them as clean (the
  bypass is the "ride around town" option).
- **Lag**: at most **3 figures** open on 0B and **2** on 0C (the outhouse's shot switch takes the third slot), and
  **1 outlaw bullet** live (an outlaw holds fire while one is live): 1 + 1 + 3 + 3 + 1 = **9** on both screens. While
  the pianist's sign is up (a pop-up) or a player utility is out, the director keeps one figure fewer open for each
  (§0.5).
- Round 1's proposed Eddie moral trade-off is **deleted** (consistency-34; story §2.8; systems' doping is the trade-off).

### 3.5 The judged quick-draw (VA-DRAW) [new-code] S · Must

Used by Sam (0D) and by Tomahawk Man (17, 1F). Staged as **a judged tournament event** (R3.4): a flag judge and a
scoreboard. All movement is locked except B.

| Step | Frames | Detail |
|---|---|---|
| Walk-up | ~60 | The screen locks; Rockman auto-walks to his mark (x `$40`), the opponent stands at x `$C0`; **the flag judge** takes his place between them (a sprite in the saloon; the BG stand on the mesa) |
| READY | random 45-150 | From tech's LFSR mixed with the frame counter at the screen lock, so a replayed input movie draws the same delay. "READY..." in the window; the commentators are muted |
| **DRAW!** | window **W** | The judge's flag drops, a big "DRAW!" sprite, a bell, and the opponent's hat glints: three tells in two senses. v1.0's bell is a vanilla SFX (art_audio picks it); the duel stinger G28 is Should |
| Win | | Any fire within W hits; the opponent falls; the **scoreboard** (HUD widget digits) shows the reaction time to two places, "0.23". The best time is Tomahawk's `VENUE_REC` (meta) |
| FOUL | | Firing during READY: the judge raises a red flag, "FOUL!", and the opponent fires (4) |
| Late | | No fire within W: the opponent fires (4) |
| Match (Sam) | | Best of three. Win 2: bounty 2. Lose 2: "COME BACK WHEN YOU'RE FASTER." The doors unlock, no bounty. A rematch after a death or on a replay |

**The window W (R3.5)**: NORMAL **24 f**, HARD **18 f**, CASUAL **40 f** (R8.6), plus CONFIG's **INPUT LAG** offset
(0-6 f, R8.7; default 0; systems and meta own the setting) added to W. VA-DRAW reads the difficulty bits itself, so these three
constants ship in v1.0. Any weapon counts as a draw; C.FLASH during READY is a FOUL like any other shot.

Lag (saloon): player + script + Sam + judge + Sam's bullet + 3 shots = 8, plus the READY window's text runner = 9
(§0.5). Mid-boss fight id `$0B` (meta), arena 0D.

### 3.6 The 4:50 train (T1-lite + T4)

- **Boarding** (R3.8, design-15) [T2 v1b] S · Must. At 0F's platform end the conductor reads the count before anyone
  boards: "BOUNTIES: 2 OF 3. SIDEWINDER RIDES THE 4:50." With 3 of 3: "ALL THREE? THEN ENJOY THE RIDE, DEPUTY." Then
  "ALL ABOARD!" → 10.
- **EXPRESS** (R3.8) [new-code] S · Must. After the first clear (`STAGE_CLEAR`, meta 6), the conductor's window adds a
  choice: ▶ALL ABOARD / EXPRESS. EXPRESS plays a 60-f whistle cut and drops Rockman at 12. That run has no Sidewinder,
  so no bounty 3 and no back way, and systems adds the train's fixed **3,300 f** to `T` so the skip never buys TIME.
- The camera may scroll 10 ↔ 11 as Rockman walks the four cars (static BG); the world moves instead.

**v1.0 bands** (`tight.py`'s "train 3 bands"; R1.9):

| Band | y | Content | X scroll |
|---|---|---|---|
| Sky and mesas | 0-127 (set at NMI) | a flat sunset sky (`$95` palette) and the vanilla mesa strip | camera/2 + 0.5 px/f |
| Train | 128-191 (IRQ) | car roofs and couplings, static | camera |
| Near ground | 192-239 (IRQ) | rails, ties, telegraph poles (T-TRAIN loop) | camera + 3 px/f |

The pop-up window moves to the bottom here (§0.6) and covers the near band below its top line while open. Budget: 3
bands + the window + the ExRAM flush = 5 of 24 entries. The sound update rides the train band (line 128), with 64
band-free lines after it. **Should**: a separate sky band with the sun disc and the vanilla sunset shimmer
(`RL_SHIMMER`, 2 entries); the sound update then moves below the shimmer, to keep R1.9's 36 free lines.

- **Timeline**: tunnels at t = 15, 30 and 45 s; arrival at 55 s ("JUNCTION! ALL OFF!") → 12.
- **Tunnel**: 90 f before, a whistle SFX and a "TUNNEL!" sign written into the near band by `map_set` (no slot). Then
  `OBJ_TUNNEL` (a 32×48 sprite wall at roof height, NOFREEZE) sweeps right to left at 4 px/f. Safe: **slide** (normal
  form) or stand in a **coupling gap** between cars, 24 px lower (any form: Power and Jet cannot slide). Hit: 4 damage
  and a knockback toward the rear. Inside: 90 f with every band dark. **R3.5**: the dark fades in and out over 16 f,
  one cycle per 15 s; REDUCED is the same. Should: two bats inside each tunnel.
- **Robbers**: vanilla `$6C` gunners (SET-TM4's copy) climb up from the couplings every 8 s and shoot along the roof;
  **one at a time**, and none in the 120 f around a tunnel.
- **SIDEWINDER** (bounty 3), `OBJ_SIDEWINDER`, HP 10, NOFREEZE: rides along the ridge above roof level (so B.ATTACK,
  SILVER.T arcs and jumping shots reach him), firing 2-shot bursts every 90 f; after each tunnel he jumps onto the
  caboose roof for a 150-f showdown, then back to the ridge. Still alive at the third tunnel: he escapes into it
  ("SIDEWINDER GOT AWAY!"), no bounty. Mid-boss fight id `$0C` (meta), arena 10-11.
- **Lag (R1.8)**: player + script (director and bands) + 3 shots = 5; the enemy side holds Sidewinder + (one robber
  **or** the tunnel wall) + at most **2 enemy bullets** (a shooter waits while 2 are live) = 4 → **9**. An open pop-up
  ("SIDEWINDER GOT AWAY!", "JUNCTION! ALL OFF!") or a player utility (the Ice Block) takes a bullet's place, and the
  shooters wait for it (§0.5).

### 3.7 Secret exit, hidden room, behaviour chip

**Secret exit: the back way** [T3] S · Must.
- **Requirement**: all three bounties claimed in the run. No adaptor.
- **The gate**: the Sheriff (a polite Metall with a star) stands at 12's right-hand ladder behind a barrier. UP to
  talk: "BOUNTIES: 2 OF 3. THE BACK WAY IS FOR DEPUTIES." With 3 of 3: "WELL I'LL BE. YOU'VE EARNED THE BACK WAY,
  DEPUTY." The barrier lifts (TMH-07). The route behind it is vanilla's plate route, geometry unchanged: the right
  ladder → 13's top-right pocket → 1D → 1E → **1F THE RODEO RING**.
- **Tells**: the posters at 00 and their HUD icons; the conductor's count before the train; the Sheriff's count; the
  barrier is visible from the middle ladder.
- **Debrief hint (TO0, tier B)**: "THE SHERIFF ONLY OPENS THE BACK WAY FOR A DEPUTY WITH THREE BOUNTIES."
- This **re-homes the vanilla B-plate gate on purpose**: vanilla's gate was just "pick the other ladder"; GP keeps the
  rooms and the plate, and gives the choice a reason. It is the game's only "a guard checks N items" gate (R3.1 trims
  Yamato's sekisho).

**Hidden room 1B "THE OUTHOUSE"** [T3] S · Must.
- Entry: the outhouse at 0C's right end rattles (its door flips between two frames every 30 f) under an "OCCUPIED"
  sign. Shoot its door 3 times (a T3 shot-count switch; out west you shoot what looks odd): the sign flips to "VACANT"
  and the door swings open (the per-id flip); UP to enter (a door warp → 1B).
- Inside it is far bigger than outside: "THE GOLD MINE VAULT": the **sponsor envelope**, a 1-UP and a W-tank (systems
  §12). The door back returns to 0C.
- **Hint (TO1, tier B)**: "SOMETHING IN TOWN WAS RATTLING. OUT WEST, YOU SHOOT WHAT LOOKS ODD."

**Behaviour chip: SHERIFF STAR** S · Must.
- Earned by reaching the Sheriff (12) with the civilian counter at 0. He pins it on you: "NOT ONE TOWNSFOLK HURT.
  WEAR THIS, DEPUTY."
- Effect (systems §9.2 #15): +20 % on every scorecard payout and on venue prize bolts.
- Tells: the pianist's sign as the gallery starts; the "HEY!" on every civilian hit.
- **Hint (TO2, tier B)**: "THE SHERIFF SAW YOU SHOOT AT TOWNSFOLK. READ THE SIGN BY THE PIANO."

Debrief order (meta): secret exit with plate B (TO0) → hidden room (TO1) → SHERIFF STAR (TO2). The Energy Balancer is
a chip found, not a predicate.

### 3.8 Boss: Tomahawk Man, "MASTER OF TOMAHAWK"

Arena: 17, the **HIGH NOON MESA** (T-MESA), noon palette `$50`. Vanilla HP 27. **Character (R3.4)**: the frontier's
rodeo showman and a stickler for duel etiquette. He tips his hat to the flag judge, waits for the flag every time, and
bows to the crowd after a draw he wins; story writes his words. The vanilla rhythm is kept: a tomahawk every 100-130 f,
a feather triple about every 550 f, leaps between. [new-code] M · Must.

#### 3.8.1 HIGH NOON (the opening)

Both stand twelve paces apart (Rockman x `$30`, Tomahawk Man x `$D0`), the flag judge on his stand between them.
VA-DRAW with the stage's window W:
- win: a **free hit** of 3 with 30 i-frames, booked as BUSTER for VARIETY (SC8); he staggers 40 f and tips his hat;
  the scoreboard shows the time; the **QUICKEST GUN** act;
- FOUL or late: he throws first: a fast tomahawk at 3 px/f (contact 4).

#### 3.8.2 Patterns

| Id | Name | Timeline |
|---|---|---|
| A | **TOMAHAWK ARC** (vanilla `$B0`) | Every 110 f, one tomahawk, alternating a high arc (peak y `$40`) and a low arc; a leap toward Rockman between throws (vanilla range x `$38-$BE`) |
| B | **FEATHER FAN** (vanilla `$B1`, GP spread) | A 24-f shake of the hat, then 3 feathers: along the floor at 2.5 px/f, 45° up-forward, and straight up then falling at Rockman's x. A boss-move preview of SILVER.T's Feather Fan alt (R2.4). B starts only when no tomahawk is in flight and no dust devil lives |
| C | **DUST DEVIL** (new) | A 30-f spin with sand puffs, then a dust devil (16×32) rolls along the floor at 1.5 px/f, bounces off the far wall once, and fades at 200 f. A tomahawk that touches it is flung up and rains down at Rockman's x |
| | Cycle | A, A, B, A, C (about 650 f) |

#### 3.8.3 Pinch (HP ≤ 9): SHOWDOWN

- Every 300 f he holsters, tips his hat to the judge and stands still for 20 f; then the flag (VA-DRAW, same W). Win:
  he staggers 60 f and takes the hit. Lose: he throws two fast tomahawks.
- A leap with a diagonal-down throw from the apex: a preview of SILVER.T's Dive Throw synergy.

Lag: B = player + script + boss + 3 feathers + 3 shots = **9**; C = 8; a lost SHOWDOWN = 8. The pinch opens
with a 20-f invincible hat-tip, and the 16-tile pinch set streams under it (2 frames at 128 B/frame).

**Credits mode** (fortress §6.2; tech's `IFCREDITS`, §4.6) [new-code] S · Must, costed in fortress's ending row: in 17
with no Rockman there is no HIGH NOON draw and no SHOWDOWN (VA-DRAW never starts while `CREDITS` is set; the flag judge
stays on his stand); the A, A, B, A, C cycle loops at full HP, aimed at an empty spot (x `$30`, Rockman's mark) instead
of Rockman. Fallback (fortress's): his card strip only.

#### 3.8.4 Weapons in this fight

| Weapon | Effect | Tags · tier |
|---|---|---|
| **PLANT.B (weakness, 4 / 16 f)** | **HAY FEVER**: the petals' pollen makes him sneeze ("ACHOO!", a 24-f stagger) and he **drops his tomahawk**, which lands 48 px away; he must walk over and pick it up (no throws for up to 120 f) while sneezing. TMH-10: "Bless you!" SC9 | [new-code][new-art] S · Must |
| SILVER.T (own) | SC4, the first hit of the fight: **he catches it** (no damage) and throws it straight back as a fast tomahawk (TMH-12). Later hits: the own cell (1 / 60 f) | [new-code] S · Should |
| Charged Power punch | knocks his tomahawk out of the air (it clatters to the floor) | Should |
| W.STORM (G, 3 / 20: "a dust devil on a cowboy") | if his dust devil is out, the tornado turns it around and rolls it back into him | Could |

#### 3.8.5 Secret room 1F: THE RODEO RING (R3.4)

- **v1.0**: 17's layout **at dusk** (a new palette), staged as the rodeo ring with the flag judge on his stand.
  Tomahawk Man's intro pop-up carries the WANTED gag: "THAT POSTER WITH YOUR FACE? MR. Y PUT IT UP. I'M NOT
  COLLECTING. I'M HERE FOR A FAIR SHOW." (draft; story owns it).
- Same AI; pinch at HP 12. Kill: the YOU GET card per story S11 (SILVER.T), the **plate B** pickup, SECRETS b0.
- **Should (the arena twist)**: T-RODEO: the ring's fence and stands, and on the fence the poster "WANTED: ROCKMAN.
  999 BOLTS (THE COUNTER'S LIMIT). SPONSOR: MR. Y."
- Round 1's "THE HIDEOUT" (the boss as an outlaw under a WANTED poster) is gone (design-11).

### 3.9 CASUAL levers (R2.9, Must)

| Lever | HIGH NOON FRONTIER (NORMAL → CASUAL) | How (systems §13.4) |
|---|---|---|
| Reflex windows ×2 | the quick-draw W 24 → 40 f (R3.5, confirmed by R8.6: 40, not 48); the outlaw's "!" 24 → 48 f; the tunnel warning 90 → 180 f | the quick-draw table (SC8, + INPUT_LAG); the others `REFLEX` (`TIERVAL` + INPUT_LAG) |
| Mash counts −40 % | none in this venue | none |
| Set-piece timers +50 % | Sidewinder's caboose showdown 150 → 225 f; the dome dispenser's waves come 1.5× further apart | `TIERVAL` |
| +1 checkpoint per section | town: 0D (after the gallery); train: a restart at t = 30 s (after the second tunnel; bounties kept); mesa: 15 | the train: a CASUAL poke on the director's restart index; 0D, 15: tech's dormant checkpoint objects, woken by a CASUAL poke |
| Skill-gated secrets −1 step | Sidewinder HP 10 → 7 (the secret exit's third bounty); the SHERIFF STAR allows 1 civilian hit (the chip) | a CASUAL poke on Sidewinder's HP; `IFCASUAL` in the STAR's predicate |

### 3.10 HARD pokes (Should, R0.3 item 3; tech §5.5 format)

| Section | Poke | Kind |
|---|---|---|
| 01-04 | two more `$6C` gunners (they replace the tumbleweeds, so the cap holds) | data |
| 05 | the dispenser drops 3 walkers per wave (it still waits at 3 live) | AI constant |
| Gallery | the outlaw's "!" 24 → 16 f; 3 figures open on 0C too, with the outhouse at the far end | data |
| Quick-draw | READY 30-180 f (the window itself is VA-DRAW's HARD 18 f, already in v1.0) | constant |
| Train | 4 tunnels, warning 90 → 60 f; Sidewinder HP 14 (still one robber, for the cap) | data |
| Tomahawk Man | the dust devil at 2.25 px/f; SHOWDOWN every 240 f | AI branch |

### 3.11 Text, commentators and the partner

- **v1.0 text** (R4.5; story §10.4 counts **25 Must strings** and 1 label, the single source: R8.4): the three posters, the pianist's sign, Eddie's "HEY!" line, Sam's loss
  line, the conductor (the count in two forms, ALL ABOARD, the EXPRESS choice), "JUNCTION! ALL OFF!", "SIDEWINDER GOT
  AWAY!", the Sheriff (3) and the STAR line, the rodeo-ring line, TMH-07 (the gate: a secret line), TMH-10 (first
  PLANT.B: the first-weakness line), 4 death lines, the hints TO0-TO2.
- **Death lines**: story's "Boot Hill has room for one more." is **dropped** (R3.4). story picks v1.0's 4 from the
  other five ("Too slow on the draw.", "The 4:50 doesn't stop for anyone.", "That was a bad trade, partner.", "The
  pianist is fine, by the way.", "Always check the outhouse first.") and writes a new sixth.
- **Should**: TMH-01-06, 08, 09, 12 (posters, first civilian, draw time, FOUL, tunnel hit, Sidewinder escapes, the
  Balancer room, the sky bypass, the catch).
- **Break Man (Should, with the partner)**: he can't duel: his whistle intro plays during READY and counts as a FOUL
  (TMH-11: "Not the whistle!"). His shield blocks the gallery outlaws' bullets. No tag shortcut.

### 3.12 Homage moments

1. The WANTED board: three bounties, posters in the Capcom western's style.
2. "PLEASE DO NOT SHOOT THE PIANIST. HE IS DOING HIS BEST." (the saloon sign Oscar Wilde reported from Leadville)
3. The flag drops, "DRAW!", and the scoreboard reads "0.23".
4. The 4:50: half-speed mesas, rushing rails, and a tunnel you slide under.
5. Sidewinder galloping along the ridge, leaping onto the caboose for a showdown.
6. The stranger who drops through the saloon skylight from the sky bypass.
7. HIGH NOON on the mesa: a judged draw opens the boss fight, and the showman tips his hat.
8. Tomahawk Man sneezes and drops his tomahawk.
9. v1.1: "WANTED: ROCKMAN. SPONSOR: MR. Y." on the rodeo-ring fence.

### 3.13 Weapons as tools in this venue

PLANT.B makes Tomahawk Man sneeze and the gunners sneeze off their crates; SILVER.T's arc clears windows above you;
B.ATTACK's spread and SILVER.T reach Sidewinder on the ridge; Y.SPEAR pierces outlaws behind crates; C.FLASH hits every
open window at once (civilians too) and is a FOUL in a duel; Power: the Balancer block and the desert pockets; Jet: the
sky bypass. Should: F.BLAST opens the mine's TNT crates. Could: KNIGHT.C knocks tumbleweeds back into outlaws.

### 3.14 Content note (R3.4, design-11: every fix is Must)

GP's western is a homage to Capcom's own western and to the light-gun era's quick-draw games, staged as a tournament
event, not a frontier-conflict story. Rules for every line and asset in this venue:

- Tomahawk Man is the frontier's **rodeo showman and a duel stickler**: a champion and the Sheriff's friend. Never the
  outlaw, never the stoic-noble type, never a stereotype.
- Outlaws are cowboy robots; bounties are prize money.
- **No graves, no Boot Hill, no totems.** His arena is the HIGH NOON MESA; his secret arena is the RODEO RING.
- **The draw is a judged event** with a flag judge and a scoreboard: a contest between entrants, not a cowboy hero
  beating him.
- No joke targets his headdress or any culture; his weakness gag is a sneeze.
- The pink "totem" walkers `$12` are re-skinned as **cactus walkers** (Must). No featured enemy or PART is named for a
  totem; if PARTs ever ship (Could), systems renames the FEATHER PART (design-11 suggests SPUR).

---

## 4. Plant Man: LOST JUNGLE

**Pitch.** Plant Man's "Forgotten Area" becomes the jungle of the 2600's most famous explorer. Vines swing over tar
pits, crocodile heads open and close, logs roll, the tar pit breathes, four treasures wait, and a ladder hole leads to
the underground, where one screen covers three above. Follow a robot cat through a floor that isn't there and you reach
the Lost Caverns, a balloon ride, and Plant Man's secret arena. The gorilla tank stays (in v1.1 it throws logs).

Vanilla facts used: layout `$32:$B000`; tileset `$2E:$92` (blocks 255/256, metatiles 197, **BG tile ids 256 / 0
free**); base CHR `$90` (256 tiles: canopy, trunks, grass, rock, bamboo floors, the red curtain-wood building), `$91`
dark gorilla rooms / `$92` canopy restore (`$0A00-$0FFF`), `$BB`/`$93` flowers (`$0000-$01FF`); palettes `$32`,
`$33`/`$34` dark, `$35` flowers; music `$04`; collision group 1 (5 → `$11`, D → `$1F`, E → `$10`; `$F` stays deadly,
consistency decision 39). Gorilla tank `$50-$53` (24 + 23 HP), spawner `$56`, script `$1C` (init `$39:$8551`: IRQ chain
7 at line `$C1`, `$069C` = `$FE`), in v08 and v0E, **both rewriting checkpoint 09**. Breakable pockets on v03 (1-UP +
big energy) and v0D (two big WE). **Lag**: 21 % from the checkpoint (v09-0D) and 10 % at v01 (`engine.md` §8). No
alternate exit. Boss `$B2`, AI `$31:$95EF`; weakness B.ATTACK (4), F.BLAST 2, PLANT.B 0; a Plant Man hit costs 4.

### 4.1 Tileset slot, art and the zero-free-tiles rule (art_audio §4.3 owns the counts; v1.0 deltas marked)

| Item | Content | Tags · tier |
|---|---|---|
| Slot **TS_PLANT** | Copy of `$2E:$92`. Its 255 block ids are full, but the GP layout drops the second gorilla room and half of the lodge, so ids are reclaimed by rebuilding the block table from the GP layout (`levels.py` lists the ids a layout uses) | [engine-ok] S · Must |
| Kept | `$90` canopy, trunks, grass, rock, bamboo floors, curtain-wood lodge and crates; `$91`/`$92` dark-room swap; `$BB`/`$93` flower swamp; palettes `$32-$35` | [engine-ok] |
| **P-PITFALL** third (`$0A00-$0FFF`, 96 tiles, replacing the canopy; an internal asset id, never on screen) | A **2600-style canopy** in about 40 tiles (programmatic; a chunkier leaf band than vanilla's 96-tile foliage, which the homage justifies) plus about 56 tiles of set pieces: vine knots, the tar surface (2 boiling frames, the torch technique, and the "closed" alternate tiles), croc-pond water, the ladder-hole rim, layered trunks, the parrot ledge and the hidden rope ladder | [new-art] M · Must |
| **P-UNDER** third (~96) | Underground brick tunnel, cracked brick wall, ladders, scorpion nests | [new-art] M · Must |
| **P-CAVERN** third (~96) | Cave walls, the underground river, a waterfall, the cavern gate | [new-art] M · Must. The Lost City's ruins and giant orchid (for 1E): Should |
| P-RAIN (8 tiles × 4 frames) | Rain in the canopy gaps on 0B-0E (the torch technique) | [new-art] S · Could |
| **SET-PL1** `A0+48` | Vine (11 angle tiles; one object of 5 segments), croc head 32×16 (closed, opening, open), log (2). Tar bubbles are **BG animation**, not sprites (lag) | [new-art] M · Must |
| **SET-PL2** `D0+32` | 4 treasures, parrot (2) | [new-art] S · Must |
| **SET-PL3** `A0+48` | Scorpion (3), robot cat (3), bat (2), balloon (2) | [new-art] M · Must. The eel (2): Should |
| Vine and balloon poses | **v1.0 uses vanilla's ladder-climb and ladder-shoot poses** (R2.3: no body change, no weapon-slot poses); art_audio's 12-tile "buster + vine" weapon-slot set is dropped | 0 · Must. Dedicated swing poses in a set-piece sheet streamed on the 00 → 01 transition: Should |
| Champion pinch set | The bloom form (the 30-f invincible bloom covers the stream), vine lash | [new-art] S · Must (24) |
| CONGA's logs | a 4-tile log copy inside CONGA's set (its 80 tiles leave `A0-AF`) | Should (with CONGA's logs) |

**The rule this venue follows**: with 0 free tile ids, **nothing is ever added to the base set**. Every new tile
arrives in a third that replaces art the screen does not show, through the screen exit's CHR byte, exactly as `$91`
replaces the canopy in the dark rooms:

| Screens | BG CHR state | Replaced |
|---|---|---|
| 00-02, 09-0E | `$90` + P-PITFALL | the canopy third (00's init script loads it at stage start; the 02 → 03 exit restores vanilla's canopy with `$92`; the 08 → 09 exit loads P-PITFALL instead of `$92`) |
| 03-07 | `$90` + `$92` (vanilla) | |
| 08 | `$90` + `$91` | canopy (vanilla) |
| 0F-14 | `$90` + `$92` + `$BB`/`$93` | vanilla |
| 18-1A | `$90` + P-UNDER | canopy (no sky underground) |
| 1B-1D | `$90` + P-CAVERN | canopy |
| 1E | `$90` + `$92` (a copy of 17's state) | (v1.1: P-CAVERN with the ruins) |
| 1F | `$90` + P-PITFALL | canopy |

Why the canopy and not the lodge: measured with `planttiles.py`, the vanilla jungle screens use 201 (00-02) and 235
(09-0D) of the 256 ids, and only two ids (`$56-$57`) are used by the lodge alone: the yellow plank and crate tiles are
shared with the jungle floors. The only third that can go is the 96-tile foliage at `$A0-$FF`, which vanilla already
swaps out in the dark rooms (`$91`). Pop-ups on these dense screens wait for free glyph ids (tech's canvas table).

### 4.2 Screen-by-screen

| GP | From | The player does | Enemies | Set pieces | Tags · tier |
|---|---|---|---|---|---|
| **00** | v00 | Starts under the canopy. The **first rolling log** comes from the right: jump it | `$60` grasshopper (1) | Log generator (in the screen script) | [new-code] S · Must |
| **01** | v01 | **The first vine** over a tar pit: jump into it, ride, press A at the far end of the swing | `$61` pod (1, not 2) | Tar pit (collision `$F`; its surface boils by CHR animation) | T5 + attach state · Must |
| **02** | v02 | **Croc pond**: three heads in the water; stand on closed heads. **Treasure 1: SILVER BAR** on the far bank | none | Croc heads (VA-TIMED a); no log on this screen (the cap) | [new-code] S · Must |
| **03** | v03 | The **explorer's lodge** (the vanilla red building). The vanilla pocket is kept: 1-UP + big energy behind the breakable (charged Power punch) | `$60` (1) | | [engine-ok] · Must |
| **04-05** | v04-v05 | Lodge climb (ladders) | `$59` big robot (v04), `$24`/`$26` lanterns (2) | | [engine-ok] · Must |
| **06** | v06 | Across the lodge top, then down | `$54` eye cannon | | [engine-ok] · Must |
| **07** | v07 | Down the shaft (loads `$91`: the dark) | `$70` | | [engine-ok] · Must |
| **08** | v08 | **CONGA**, the gorilla tank, in the dark (§4.6): vanilla rocks in v1.0, with the slot rule. Lights on when it dies (vanilla). Floor split kept (the chain-7 preset) | gorilla parts | **Checkpoint 1** = 09, set when CONGA dies | [new-code] S · Must; its logs Should |
| **09** | v09 | Back in the jungle. **The breathing tar pit**: a 64-px floor section opens and closes. **Treasure 2: MONEY BAG** on a ledge above the pit, reached from the vanilla spring `$57` | `$60` (1) | VA-TIMED (b), run by the script | [new-code] S · Must |
| **0A** | v0A | **The ladder hole** (the underground entrance) ↓ 18. **Treasure 3: GOLD BAR** on a canopy ledge, reached by a vine. Main route: right | `$61` (1), a log | Vine; the ladder hole (a down exit with a target → 18) | T5 · Must |
| **0B** | v0B | **Vine chain**: two vines in a row over the vanilla spike beds. **The storm starts** (§4.8). Hidden-room tell: the parrot ledge at the top right | parrot (harmless) | Lightning shows the rope ladder; an up exit → 1F | T5 · Must |
| **0C** | v0C | **Croc river**: three heads with staggered phases (0 / 64 / 128 f), a rolling wave to time | `$61` (1) | VA-TIMED (a) | [new-code] · Must |
| **0D** | v0D | Storm; the vanilla pocket is kept: two big WE behind the breakable | `$60` (2, not 4) | | [engine-ok] · Must |
| **0E** | v0E (was gorilla 2) | **The big swing**: one long vine (88 px) over a croc pond (2 heads), one log rolling on the far bank | 1 log | No gorilla, no split: the lag fix | T5 · Must |
| **0F** | v0F | The storm ends; spring `$57`, eye cannon. **Underground exit 1** (from 19) arrives by ladder here | `$54` | | [engine-ok] · Must |
| **10-14** | v10-v14 | **The flower swamp** (vanilla `$BB`/`$93`, palette `$35`): pillars with spring flowers over the swamp. **Underground exit 2** (from 1A) arrives by ladder in 13 | `$58` eye drones, `$5A` hornets, `$5F` spring flowers, `$54` (vanilla; **at most 4 live**) | Should: croc heads in two swamp channels (11, 13) | [engine-ok] · Must |
| **15-16** | v15-v16 | Shutters; **checkpoint 2** at 16 | | | [engine-ok] · Must |
| **17** | v17 | **Plant Man** (§4.7) in the green bamboo room, now with two ceiling hooks and an opening floor | | | Must |
| **18** | new | **Underground, west** (under 0A-0C): from the ladder hole; brick tunnel | 2 scorpions | | [new-art] · Must |
| **19** | new | **Underground hub** (under 0D-0F): the **robot cat** (§4.5); **Treasure 4: DIAMOND RING** in a nook behind a scorpion (§4.4); a **cracked brick wall** at the right end (charged Power punch) → 1A; a ladder up → 0F | 2 scorpions | The cat's false floor | [engine-ok] layout + S · Must |
| **1A** | new | **Underground, east** (under 10-12): a ladder up → 13 | 1 scorpion | The full 3-for-9 shortcut | · Must |
| **1B** | new | **The Lost Caverns**: fall in through the cat's false floor; a shaft of ledges | 3 bats | | [new-art] · Must |
| **1C** | new | **The underground river**: the **balloon** rises from the bank to the top ledge (§4.5) | 2 bats | The river is a pit. Should: eels | [new-code] S · Must |
| **1D** | new | The cavern gate: shutters, **checkpoint 2b** | | | · Must |
| **1E** | new | **Secret boss room: THE LOST CITY** (§4.7.5); v1.0 is a copy of 17 at night. Kill: PLANT.B + SECRETS b0 | | | Must; the ruins arena Should |
| **1F** | new | **Hidden room "TREETOP HUT"** (§4.8) | | | · Must |

All 32 screens are used; the main route keeps vanilla's 24. Checkpoints: 09 (after CONGA), 16 (shutter), 1D (secret
shutter).

**Lag (R1.8)**, every screen at ≤ 9: 02 = player + script + 3 shots + 3 heads + the treasure = 9; 0A = vine + pod +
log + treasure + 5 = 9; 0B = 2 vines + parrot + 5 = 8; 0C = 3 heads + pod + 5 = 9; 0E = vine + 2 heads + log + 5 = 9;
the swamp = 4 + 5 = 9; 19 = cat + 2 scorpions + the ring + 5 = 9; 1B = 8; 1C = balloon + 2 bats + 5 = 8; CONGA and
the boss: §4.6, §4.7. Vanilla's worst stretch (v09-0D) loses half its grasshoppers and all its falling debris `$5B`;
the second gorilla room is gone; round 1's 5-head croc river becomes 3.

### 4.3 Jungle mechanics (numbers)

| Object | Behaviour | Numbers | Tags · tier |
|---|---|---|---|
| `OBJ_VINE` (T5 on the attach state) | Swings constantly (the 1982 vines never stop). Grab: airborne, upper body touching the bottom 16 px. Hang pose = the ladder-climb sprite. **A** releases with the tip's velocity (capped at 3 px/f horizontal) plus a normal jump. **DOWN** drops. **Only the buster fires** while hanging (consistency-43), from the ladder-shoot pose toward the swing's direction; the equipped weapon returns on release. Power form can grab; Jet does not (it flies) | Pivot at the canopy (y `$20-$30`), length 64-88 px, period 128 f, amplitude ±50°. One object, 5 sprite segments, 11 angle frames | [new-code][new-art] M · Must |
| `OBJ_CROC` (VA-TIMED a, NOFREEZE) | A head in the water. CLOSED = a rideable platform (vanilla lift `$A0` code) | CLOSED 120 f → BLINK 20 f (red eyes: the tell) → OPEN 90 f (the jaws hurt 4, not rideable) → CLOSE 10 f. Phase offsets per head from data | [new-code][new-art] S · Must |
| `OBJ_LOG` (NOFREEZE) | Rolls along the floor, drops off ledges. Contact 2 + 16-px knockback (the 1982 logs never kill outright). Buster shots thunk off. **F.BLAST burns it** (a per-class thematic one-shot, vanilla style). The generator is a screen-script timer | 1.25 px/f; one log per 200 f per generator; **at most 1 live** | [new-code][new-art] S · Must |
| Tar pits (VA-TIMED b) | Static pits are collision `$F` with the boiling surface. The **breathing pit** (09) toggles its 4 unique metatile ids with the per-id flip, run by the screen script (no object) | SOLID 150 f → BUBBLE 30 f (the boil speeds up and a gurgle plays: the tell) → TAR 120 f (collision `$F`) → SOLID | [new-code] S · Must |
| `OBJ_SCORPION` (featured enemy) | Walks the tunnel floor; raises its tail for 30 f (the tell) when Rockman is within 24 px, then strikes (3). B.ATTACK drops it outright | HP 2, 0.5 px/f | [new-art][new-code] S · Must |
| `OBJ_BALLOON` (attach state) | Grab from below or the side: Rockman hangs (the ladder pose, buster only) and rises 0.5 px/f; LEFT/RIGHT drift 0.5 px/f; A lets go. A bat touching the balloon pops it and drops him onto the bank ledge below (never into the river) | Rises to y `$30`, then a step right onto the top ledge | [new-code][new-art] S · Must |
| `OBJ_BAT` | Swoops when Rockman passes below | HP 1 | [new-art] S · Must |
| `OBJ_EEL` | Leaps out of the river in an arc (2) | every 120 f | [new-art] S · Should |

Should: a charged Power punch sends a log rolling back; B.ATTACK's Ice Block encases an open croc head and holds it
shut for the block's life (it needs a croc frozen handler); W.STORM's tornado gives the balloon +1 px/f for 60 f.

### 4.4 Behaviour chip: the EXPLORER'S PERFECT (AUTO RECOVER) [new-code] S · Must

The 1982 explorer's perfect score needs every treasure and no lost points; logs only ever cost points.

- **Treasures**: SILVER BAR (02), MONEY BAG (09), GOLD BAR (0A), DIAMOND RING (19). Each pops "TREASURE n/4 · LOGS m"
  and pays its prize bolts (#0-#3). The count is meta's stage-counter predicate (R1.10): the venue's one collect-N
  secret (R3.1).
- **The log counter**: every rolling-log hit in the run is counted (CONGA's logs too, once they ship). A hit shows
  "LOGS m" for 60 f (HUD widget).
- **The ring**: if the log counter is 0 when Rockman reaches the nook in 19, it is the **DIAMOND RING**; otherwise it
  is a "RHINESTONE RING" worth nothing. With 4/4 and the real diamond, the ring also grants the chip.
- Chip: PLAN's **AUTO RECOVER** ("found in the Plant underground", kept). Effect (systems §9.2 #16): after 60 f with no
  input, +1 HP every 30 f up to max; off while a boss bar is shown.
- All four treasures can be had without an adaptor in one run (three before the ladder hole, one in 19).
- Tells: the counter on every treasure pop; the rhinestone itself. Should: PLT-06, reworded without the explorer's
  name (R3.3): "That's paste, Rockman. A real explorer never lets a log touch him."
- **Hint (PL2, tier B)**: "FOUR TREASURES, ZERO LOGS. THE DIAMOND IS SHY."

### 4.5 Secret exit: follow the cat to the Lost Caverns

The 1984 sequel's explorer had to find his cat. Here a small green robot cat (Capcom's own Tango; story approved the
cameo) lives in the underground hub.

- **Requirement**: in 19, walk toward the cat (`$F4`, harmless, NOFREEZE). It meows, runs 48 px to a dead-end nook and
  **drops through the floor**: one floor metatile there has floor art and collision 0 (CX's "clouds are not floors", as
  a floor) [engine-ok] layout. Follow it: fall into 1B. No adaptor.
- If you do not follow within 300 f, the cat climbs back out and sits by the nook again (it repeats).
- **Route**: 19 → false floor ↓ 1B (bats, ledges) ↓ 1C (the river; ride the balloon up past the bats) → 1D gate
  (checkpoint 2b) → **1E THE LOST CITY**. The kill sets SECRETS b0 (meta 3).
- **Tells**: the cat is the only friendly animal underground; it meows when you enter 19 (PLT-08, a secret line: "Is
  that... Tango?"; round 1's "From the Game Boy?" names a third-party trademark and leaves the line, R3.3); the nook is
  a dead end with nothing in it, which is suspicious on its own.
- **Debrief hint (PL0, tier B)**: "THE CAT KNEW A WAY DOWN. NEXT TIME, FOLLOW IT."

### 4.6 Mid-boss: CONGA, the gorilla tank

- **v1.0**: the vanilla object set (`$50-$53`, 24 + 23 HP, spawner `$56`, script `$1C`, the chain-7 floor-split preset,
  dark → lights on) with its vanilla rocks `$14`. **One AI rule keeps the cap** (R1.8): it throws only while the player
  has 2 or fewer shots and utilities live (§0.5), and only 1 rock flies at a time: 4 parts + 1 rock + player + script + 2 shots = 9.
- **Checkpoint fix**: vanilla's script rewrites checkpoint 09 in both gorilla rooms. GP has one gorilla room, and its
  routine sets checkpoint 09 only when CONGA dies: a hook on one script byte (`stages_b.md` §8). [new-code] S · Must
  (feasibility-19: round 1 tagged it engine-ok).
- **Should (the second set piece, with the swamp crocs)**: CONGA throws **rolling logs** instead of rocks; they bounce
  off the far wall once and roll back (a nod to the 1981 barrel game), at most 1 live, and they count on the log
  counter. Mid-boss fight id `$0D` (meta), arena 08, for GP Rush when it ships.

### 4.7 Boss: Plant Man, "FLOWER FANCIER"

Arena: 17 (v17, the green bamboo room) plus two ceiling hooks (x `$50` and `$B0`, y `$20`; BG) and a 64-px centre floor
section that can turn to tar (VA-TIMED b). Vanilla HP 27. Story's gentle gardener-explorer who apologises to the
flowers. The vanilla rhythm is kept: the guard about every 260-350 f, leaps of about 130 f. [new-code] M · Must.

**The guard is rebuilt for the slot cap.** Vanilla's barrier is 5 objects (`$B3` ×4 + `$B5`). GP draws it as **one
ring object** (4 petals around a centre, one custom draw, one hit test per petal). The X-throw is **2 objects**, each
drawing two mirrored petals that fly apart along one diagonal.

#### 4.7.1 Patterns

| Id | Name | Timeline |
|---|---|---|
| A | **PETAL GUARD + LEAP** | Raise the ring (radius 20 px) in 40 f; leap toward Rockman (peak y `$44`, about 120 f); 20 f after landing, throw the 4 petals outward in an X at 2 px/f; 30-f recovery. A boss-move preview of PLANT.B's Petal Shot alt (R2.4) |
| B | **VINE SWING** (new) | 20 f: he throws a vine to the nearer ceiling hook; one swing pass across the room (64 f, contact 4) with a jungle yell; he lets go at the far apex and lands. **The vine stays for 150 f** and Rockman can grab it (T5, attach state): the stage's mechanic, used against him |
| C | **SPROUT** (new) | A 24-f stomp (the floor shakes: the tell); the centre floor turns to **tar** for 150 f; three sprout platforms (32 px wide) rise at x `$28`, `$80` (straight out of the tar: the way across) and `$D0`, to 32, 56 and 40 px, and last 180 f. **The sprouts are BG blocks written by `map_set`**, two steps each, so they cost no slot. At +40 f he lobs 2 seeds at the sprout tops |
| | Cycle | A, B, A, C (about 700 f) |

#### 4.7.2 Pinch (HP ≤ 9): BLOOM

- A 30-f bloom animation (invincible; the pinch set streams under it): his head petals open into a large flower.
- The ring orbits wider (radius 32) and 1.5× faster: a preview of PLANT.B's Petal Storm synergy.
- **2** pollen spores drift toward Rockman at 0.5 px/f for 300 f (contact 2, shootable).
- VINE SWING makes two passes.

Lag: A = player + script + boss + the ring (1) or the throw (2) + 3 shots = 8; B = 7; C = boss + 2 seeds = 8; BLOOM =
boss + ring + 2 spores + 3 shots + 2 = **9**.

**Credits mode** (fortress §6.2; tech's `IFCREDITS`, §4.6) [new-code] S · Must, costed in fortress's ending row: in 17
with no Rockman the A, B, A, C cycle loops at full HP, aimed at an empty spot (x `$40`) instead of Rockman; B's vine
hangs its 150 f with no one to grab it; C's tar and sprouts run through `map_set` as in the fight, and the room's script
restores the floor when the segment ends (the same undo W2's fight loader needs, §7). Fallback (fortress's): his card
strip only.

#### 4.7.3 Weapons in this fight

| Weapon | Effect | Tags · tier |
|---|---|---|
| **B.ATTACK (weakness, 4 / 16 f)** | **FROSTBITE**: his petals freeze white, drop and shatter; he cannot raise the guard for 300 f and shivers for 30 f. PLT-10: "He's wilting!" SC9 | [new-code][new-art] S · Must |
| PLANT.B (own) | SC4, the first hit of the fight: guard meets guard, **both pop** in a burst of petals (no damage; it replaces vanilla's silent 0; PLT-12). Later hits: the own cell (1 / 60 f) | [new-code] S · Should |
| F.BLAST (G, 3 / 20) | During B it **burns his vine**: he drops mid-swing and lies stunned 40 f | [new-code] S · Should |
| C.FLASH (R) | freezes the tar back to floor for its duration; systems' SC3 "photosynthesis" (+2 HP on the first flash) also applies | Could |

What the fight teaches: PLANT.B's tap (his guard), its Petal Shot (his throw), its Jet synergy (the bloom orbit) and
the venue's own vine.

#### 4.7.4 Defeat

The YOU GET card per story S11: "YOU GET PLANT.B". Round 1's 4th-win "AND RUSH JET ADAPTOR" line is **deleted**:
adaptors are never announced on YOU GET (consistency-34, story S11); Roll hands the Jet over on the bracket (meta
EVENTS b1).

#### 4.7.5 Secret room 1E: THE LOST CITY

- **v1.0**: a copy of 17 (the hooks and the tar centre) in a **night palette**; same AI, pinch at HP 12. The kill sets
  SECRETS b0.
- **Should (the arena twist)**: the Lost City's ruins with one giant orchid behind him (P-CAVERN art).

### 4.8 The storm and the hidden room

**The storm** [new-code] S · Must (feasibility-19: round 1 tagged it engine-ok). From 0B to 0E the screen script plays
lightning on vanilla's palette-cycler data (`$3B:$9143`): a strike every 6-10 s, never closer than 2 s apart. Each
strike makes the BG palette **jump bright for 6 f, then fade back over 16 f**: one flash per strike, well under R3.5's
3 per second. Thunder SFX on every strike. **REDUCED**: a soft 20-f brighten and fade, with no jump. Rain tiles are
Could (P-RAIN).

**Hidden room 1F "TREETOP HUT"** S · Must.
- Entry: on 0B a rope ladder hangs from a ledge at the top right, drawn in the canopy's darkest palette entry, so it
  shows **only while lightning lights that entry** (the 6-f peak plus the fade). A parrot on the ledge squawks every
  4 s: the tell that works without seeing a flash. Reach the ledge by releasing the second vine at the far end of its
  swing; climb the ladder (an up exit with a target → 1F).
- Content: the **sponsor envelope**, a 1-UP and an E-tank; a blank, unlabelled 2600-style cartridge on the shelf as a
  prop.
- Exit: the ladder down to 0B.
- **Hint (PL1, tier B)**: "WHEN THE LIGHTNING STRUCK, A LADDER APPEARED IN THE TREES."

Debrief order (meta): secret exit (PL0) → hidden room (PL1) → EXPLORER'S PERFECT (PL2).

### 4.9 CASUAL levers (R2.9, Must)

| Lever | LOST JUNGLE (NORMAL → CASUAL) | How (systems §13.4) |
|---|---|---|
| Reflex windows ×2 | the croc's red-eye BLINK 20 → 40 f; the scorpion's tail tell 30 → 60 f; the tar's BUBBLE 30 → 60 f; the hidden ladder's fade 16 → 32 f | `REFLEX` (`TIERVAL` + INPUT_LAG) |
| Mash counts −40 % | none in this venue | none |
| Set-piece timers +50 % | croc CLOSED 120 → 180 f; tar SOLID 150 → 225 f; the vine period 128 → 192 f; the cat waits 300 → 450 f; Plant Man's sprouts last 180 → 270 f | `TIERVAL` |
| +1 checkpoint per section | the jungle: 03 (the lodge); after CONGA: 0C; the swamp: 12; the underground and caverns: 1C (the riverbank) | tech's dormant checkpoint objects, woken by a CASUAL poke |
| Skill-gated secrets −1 step | the EXPLORER'S PERFECT allows 0 → 1 log hit (the chip; the ring stays the diamond) | `IFCASUAL` in the ring's test |

### 4.10 HARD pokes (Should, R0.3 item 3; tech §5.5 format)

| Section | Poke | Kind |
|---|---|---|
| Crocs | CLOSED 120 → 90 f, OPEN 90 → 110 f | constants |
| Vines | period 128 → 104 f | constant |
| Tar pit | SOLID 150 → 110 f | constant |
| Logs | 1.25 → 1.75 px/f; CONGA's throws 1.5× faster | constants + AI branch |
| 10-14 | when the swamp crocs ship: two spring flowers `$5F` become croc heads (still ≤ 4 live) | object list |
| 1C | a popped balloon drops into the river; 3 bats | AI branch + data |
| Plant Man | sprouts last 120 f; pinch at HP 13; seeds aimed at Rockman | AI branch |

### 4.11 Text, commentators and the partner

- **v1.0 text** (R4.5; story §10.4 counts **11 Must strings** and 1 label, the single source: R8.4): the treasure pop (one template), the rhinestone pop, PLT-08 (the cat: a
  secret line, reworded), PLT-10 (first B.ATTACK: the first-weakness line), 4 death lines (story picks from "See you
  later, alligator!", "Stuck in the tar!", "He let go too early.", "The jungle always wins the first round.", "Watch
  the eyes on those crocs!", "That wasn't a floor, Rockman."), and the hints PL0-PL2.
- **Should**: PLT-02-07, 09, 11, 12 (first vine, croc pair, first log, treasure, rhinestone, first lightning, the brick
  wall, bloom, the barrier clash). **Could**: PLT-01 "Twenty minutes on the clock!" with the 20:00 clock, which counts
  down from 20:00 like the 2600 game's and does nothing at 0:00 but the joke.
- **Break Man (Should, with the partner)**: his Break Shot breaks the cracked brick wall (19 → 1A), which gives the
  3-for-9 underground to players without Power yet. The wall carries **no scarf emblem**: it is an ordinary cracked
  block that the full punch also opens, and the emblem is only for Break-Man-only gates (systems §11).

### 4.12 Homage moments

1. Screens 00-02: a rolling log, a vine over a tar pit, crocodile heads: the 2600 jungle in Rockman's engine.
2. Crocodile heads you stand on.
3. The tar pit that breathes.
4. The underground where three screens cover nine.
5. Following a robot cat through a floor that isn't there.
6. A balloon ride up an underground river while bats try to pop it.
7. Lightning shows a rope ladder in the trees.
8. Plant Man swinging across his arena on a vine, then blooming.
9. "That's paste, Rockman": the rhinestone ring for anyone a log touched.
10. v1.1: the gorilla tank throwing logs that bounce back like barrels.

### 4.13 Weapons as tools in this venue (VARIETY)

B.ATTACK drops the scorpions (the featured tell) and gives Plant Man FROSTBITE; F.BLAST burns logs; C.FLASH hits every
scorpion and bat on screen; SILVER.T's arc reaches bats above you; the charged Power punch opens the 03 and 0D pockets
and the brick wall; the Jet hovers over tar pits (late-game players may skip vines: allowed). Should: F.BLAST burns
Plant Man's vine; the Ice Block holds a croc head shut; W.STORM lifts the balloon; PLANT.B's barrier blocks eel leaps.

---

## 5. The four venues side by side

| | SKY ACE | HERO'S QUEST | HIGH NOON FRONTIER | LOST JUNGLE |
|---|---|---|---|---|
| Homage made a mechanic | 1943's rules: draining energy, shoot-to-cycle POW, 3 loops, red squadrons, SHOOTING DOWN % | Command windows, keys that doors eat, search, Metal Metslime, battle log | Bounty posters, the alley gallery, the judged quick-draw with a timer, a train with tunnels | Vines, croc heads, logs, a breathing tar pit, the 3:1 underground, treasures, a balloon |
| Vanilla set piece + one twist | Wind Man's pull → his HEADWIND push (v1.1: the gust decks) | The spike ceiling (IRQ `$11`) → **a monster with HP**; the Power pillar → stairs behind the throne | The dome dispenser → bounty 1; the parallax chain → the train's bands; the plate ladder → the Sheriff's back way | The dark-room swap → the underground thirds (v1.1: the gorilla tank throws logs) |
| Vanilla secrets kept | The pocket on 04 | **Plate A** (1A); the 1-UP pocket | **Plate B** (1F), **Energy Balancer** (1C), **Jet sky bypass** (18-1A) | Pockets on 03 and 0D |
| Secret exit | 4 red squadrons → elevator → service bays → WING WALKER (1D) | Search behind the empty throne → the key check → basement → KNIGHTLORD (1A) | 3 bounties (the conductor counts) → Sheriff → back way → RODEO RING (1F) | Follow the cat → Lost Caverns → balloon → LOST CITY (1E) |
| Secret arena, v1.0 / v1.1 | tower top at night / on the flying bomber's wing | revisit palette / the real throne | the mesa at dusk / the rodeo ring's fence and stands | bamboo room at night / the Lost City ruins |
| Hidden room | 1E WEATHER BALLOON (a seagull on a solid cloud) | 1E LIGHT'S TABLET (glint, search) | 1B THE OUTHOUSE (shoot the rattling door) | 1F TREETOP HUT (lightning shows the ladder) |
| Behaviour chip | YASHICHI (juggle a POW 8 times) | KAISHIN (kill the Metal Metslime) | SHERIFF STAR (hurt no townsfolk) | AUTO RECOVER (4 treasures, 0 logs) |
| Weakness reaction | C.FLASH: engines STALL | Y.SPEAR: pierces the shield | PLANT.B: sneezes, drops his tomahawk | B.ATTACK: FROSTBITE, petals shatter |
| Own-weapon joke (SC4, v1.1) | W.STORM absorbed (he likes it) | KNIGHT.C clashes | SILVER.T caught and thrown back | both guards pop |
| Pinch | SKY ACE: loop dive, calls 3 red planes | ENRAGED: Morning Star, HEALMORE | SHOWDOWN: judged mid-fight draws | BLOOM: wide orbit, pollen |
| Replay skip (R3.8) | LAND | none needed | EXPRESS | none needed |
| Screens used | 27 / 32 | 28 / 32 | 32 / 32 | 32 / 32 |
| Exhibition pair (v1.1) | E1 (with Knight) | E1 (with Wind) | E2 (with Plant) | E2 (with Tomahawk) |

## 6. Build list by tier

Sizes are per item; shared engine items are built once by tech and counted there.

| Venue | Must (v1.0) | Should (v1.1+) | Could | Won't (v1) |
|---|---|---|---|---|
| **SKY ACE** | TS_WIND (S); W-CARRIER (M), W-SEA (S), windsock BG (S), SET-WS1-3 (M), seagull (S), set-piece player sheet (S), pinch set (S); catapult (S); sortie data on the vehicle state: wave list (M), POW cycle (S), LOOP (S), drain (S), lamps and tally (S); simple AYACO (M); lamp board + elevator (S); LAND (S); tower callback (S); hidden room (S); YASHICHI (S); Wind Man rework (M); 1D night fight (S); CASUAL list (S) | Gust decks: VA-GUST, windsocks, Kite Mets, engine fans (M); destroyer (S); AYACO's 4 engines, tail gun and BG art (L); WING WALKER on the wing + W-HANGAR + bomb carts (M); re-sortie catapult (S); arena cloud band (S); SC4 W.STORM (S); punch knock-down (S); Jet-form wind (S); Time Stop STALL (S); G22 SORTIE [new-music] (M); POW / LOOP / ACE stingers (S); Break Man hooks (S); HARD list (S); flavour hooks | Paper-plane defeat (S); Y.SPEAR fan jam (S) | |
| **HERO'S QUEST** | TS_KNIGHT (S); K-DQ (S), SET-KN1 (M), SET-KN2 (M), pinch set (S); VA-SEARCH and search spots (S); King and Sage (S); keys, doors, chests (T3 data, S); stairs check + ladder (S); VA-ENCOUNTER (M) + Metslime (S) + Killer Chest (S); ceiling with HP (S); Metal Metslime + KAISHIN (S); hidden room (S); Knight Man rework with the battle log (M); Knightlord offer (S); CASUAL list (S) | Inn (S); Princess Roll + Roll's Love (S); 1A throne staging (S); SC4 KNIGHT.C clash (S); W.STORM flips Metslimes (S); G23 ENCOUNTER [new-music] (M); Break Man hooks (S); HARD list (S); flavour hooks | EXP and level-ups (S); TRUE FORM (S); inn jingle and level-up fanfare [new-music] (S) | The dark basement, RADIANT and the sconces (R3.1) |
| **HIGH NOON FRONTIER** | TS_TOMAHAWK (S); T-TOWN, T-SALOON, T-TRAIN (M each); **T-MESA** (S); SET-TM1-4 (M); **cactus walker** (S); pinch set (S); WANTED board + bounty HUD (S); gallery (M); judged VA-DRAW (S); Sam (S); the train on 3 bands (L); Sidewinder (S); conductor count + EXPRESS (S); Sheriff gate (S); outhouse room (S); SHERIFF STAR (S); Tomahawk Man rework + HIGH NOON (M); RODEO RING fight (S); third checkpoint script (S); CASUAL list (S) | Train sky band + shimmer (S); tunnel bats (S); T-RODEO arena + poster (S); TNT crates (S); 12 re-board (S); pause poster page (S); punch knock-down (S); SC4 SILVER.T catch (S); G24 4:50 TRAIN [new-music] (M); duel stinger [new-music] (S); Break Man hooks (S); HARD list (S); flavour hooks | Vulture re-skin (S); W.STORM dust devil (S); honky-tonk piano G32 [new-music] (S); the piano stops on a skylight drop (S) | Graves, Boot Hill, totems, THE HIDEOUT (R3.4); the Eddie moral trade-off (consistency-34) |
| **LOST JUNGLE** | TS_PLANT rebuild (S); P-PITFALL, P-UNDER, P-CAVERN (M each); SET-PL1-3 (M); pinch set (S); vines on T5 + the attach state (M); croc heads (S); logs (S); tar pits (S); scorpions, bats (S); balloon (S); treasures + log counter (S); cat + false floor (S); CONGA slot rule + checkpoint fix (S); storm (S); hidden room (S); Plant Man rework with the ring guard (M); 1E night fight (S); CASUAL list (S) | CONGA's logs (S); swamp croc channels (S); eels (S); Lost City ruins arena (S); vine burn (S); Ice Block croc (S); W.STORM balloon (S); swing poses (S); SC4 PLANT.B clash (S); Break Man wall (S); HARD list (S); flavour hooks | Rain (S); the 20:00 clock (S); C.FLASH freezes tar (S); G29 LOST CAVERNS [new-music] (S) | |

**Below-v1.0 fallbacks** (only if the ledger forces cuts past R0.3's "if the budget tightens" list): SKY ACE: AYACO
becomes a gold-leader squadron (no T8). HERO'S QUEST: the vanilla ceiling without HP; sprite-word battle log (Risk 5).
HIGH NOON FRONTIER: the train on 2 bands. LOST JUNGLE: 1B and 1C merged into one cavern screen. **Never cut** a
venue's homage mechanic, secret exit, hidden room, behaviour chip or boss rework (R0.2).

## 7. Dependencies on other docs (single sources of truth)

| Doc (what it owns) | What this doc takes from it, and asks of it |
|---|---|
| `systems.md` (combat, economy, chips) | Takes: the vanilla weakness cycle; weakness 4 / 16 f; SC1, SC8, SC9; the SC4 hook (Should); chips #1 and #13-16 and their effects; YASHICHI ⟂ DARUMA (R2.6); prize bolts ≤ 60 per venue and one envelope per hidden room; plates as pickups; SECRETS weights; the mid-boss default column; the 14-chip v1.0 set (R2.5). **Asks**: (1) Y.SPEAR in SC1's pass-through list, piercing without breaking (consistency-35); (2) the vehicle-state clause in §2.4: a stage-lent vehicle is not a form, is NO TAG, works under 1993, books no form VARIETY (consistency-36); (3) the Metal Metslime's "every hit does 1" as a named mid-boss special case; (4) LANDED adds 7,200 f and EXPRESS 3,300 f to `T`; (5) INPUT LAG (0-6 f) added to VA-DRAW's window (R3.5); (6) the VENUE ACTs and pars of §0.8; (7) the freeze classes of §0.11; (8) if PARTs ever ship, rename the FEATHER PART (design-11); (9) v1.1: the Inn's 20-bolt price as a sink |
| `meta.md` (save bytes, bracket, events, debrief) | SECRETS b0-b4 for meta 2, 3, 6, 7; the PRIZES indexes of §0.8 (Knight 1, Tomahawk 3, Plant 4 bits); `VENUE_REC`: Wind's best SHOOTING DOWN % and Tomahawk's best draw in frames (Must), Knight's fastest Metal Metslime kill (proposed, Should); `STAGE_CLEAR`, read by LAND and EXPRESS; the `CFG_CASUAL` bit; the tier B hints verbatim (WI1, TO1 and PL2 wording here is final for round 2; TO1 no longer names a game); mid-boss fight ids `$08` AYACO, `$09` METAL METSLIME, `$0A` DOMINGO DOME, `$0B` SIX-SHOT SAM, `$0C` SIDEWINDER, `$0D` CONGA with arenas 01, 12, 05, 0D, 10-11, 08 (consistency-44; used when GP Rush ships); the E1/E2 pairing (v1.1); the R3.3 venue names on the debrief and panels. When tier A riddles return (Should), PL0's riddle loses the explorer's name (R3.3) |
| `tech.md` (ids, memory, raster, CHR) | Stage ids `$01`/`$06`/`$05`/`$02`; the 48-byte record (`SECRET_SCR`, `PAR`, `EFFECTS`, the `NO_TAG` mask); the map-edit service; families `$F4`/`$F5`; HUD widgets; the attach and vehicle states; T1-lite with the director in the slot-22 script; T3 with the per-stage key counter; T8; the raster list (24 bands, `RL_PARALLAX`, `RL_SHIMMER` = 2 entries, `RL_BANDS`; budgets: Wind 01 = 4 entries, the train = 5); text v1a/v1b; **a per-screen pop-up position switch the screen script can set** (Wind 01, Tomahawk 10-11); the Knight ceiling out of IRQ `$11` with a retract flag; the lag cap of 9 in artcheck; the poke-list format with the CASUAL tier; four slots in the tileset table (TS_WIND, TS_KNIGHT, TS_TOMAHAWK, TS_PLANT); streaming the set-piece player sheet during the catapult; the LFSR for VA-DRAW; permission to overwrite layout banks `$32`/`$33` after regression (R1.5); the credits' `CREDITS` bit and `IFCREDITS` (§4.6) for the four bosses' credits mode |
| `story.md` (every word, the ending) | Every line here is a draft. Changes for story: Tomahawk's death line "Boot Hill has room for one more." is dropped and a new sixth is needed (R3.4); PLT-06 and PLT-08 lose "Harry" and "Game Boy" (R3.3); TO1 no longer names a game; Tomahawk Man's §2.10 voice becomes the rodeo showman strict about duel etiquette (R3.4); "A SPLENDID STRIKE!" (KNT.S16) is reserved for KAISHIN, and Y.SPEAR's log line is "THE SPEAR PIERCED THE SHIELD!"; new lines: LAND / "LANDED", the conductor's count and EXPRESS, the stairs check, the Sage's after-death line, the RODEO RING line. HERO'S QUEST's 1986-RPG lines are story's paraphrases, never quotes (R8.4: KNT.D1, S11, S16, S23, S25, K01-K04, and "a fire spell" / "a healing spell" in the log), and this doc's drafts follow them. v1.0 Must text for these venues is **story §10.4's count**, the single source (R8.4): **90 strings and 4 labels** (Wind 10 + 2, Knight 44, Tomahawk 25 + 1, Plant 11 + 1), 4 death lines each (R4.5) |
| `art_audio.md` (tile, byte and track budgets) | The v1.0 deltas of §1.1, §2.1, §3.1, §4.1: Wind's seagull becomes Must, the windsock moves to BG, the loop poses move to the set-piece player sheet (feasibility-8), the pinch set grows to 24, W-SEA drops the destroyer, SET-WS5 becomes Should; Knight's inn bed, Princess, Innkeeper and heart become Should, the sconce flame Won't; Tomahawk's T-BOOTHILL becomes **T-MESA** (no graves, Must), T-RODEO Should, the cactus walker Must, the flag judge joins SET-TM3, "HEY!" joins SET-TM2; Plant's 12-tile vine weapon-slot set is dropped, its tar bubbles become BG animation, the eel Should. **Music**: no new track for these venues in v1.0 (G22, G23, G24 and the G28 stingers are Should, G29 and G32 Could); the encounter swaps to a vanilla boss theme; the DRAW bell and the ACE fanfare are vanilla SFX |
| `venues_b.md` | The same rules: secret arenas = boss room + new palette in v1.0; one CASUAL lever list; the lag cap of 9 counted the same way. No second train, shoot-'em-up or quick-draw. Yamato's sekisho is trimmed (R3.1), so the Sheriff is the game's only "guard checks N items" gate; Yamato's nightingale floor (Should, R8.6) reuses the ceiling engine with its own trigger. The E1-E4 pairing |
| `fortress.md` | The HALFTIME RIOT keeps the game's one lights-on-a-timer set piece, which is why Knight's basement is lit (R3.1). W2's pair bouts load these champions through the fight loader with FIGHT_CTX (R1.7): the four boss rooms (Wind 13, Knight 17, Tomahawk 17, Plant 17) run there with a per-fight pinch byte; the HIGH NOON draw runs in W2 too. The v1.0 credits (fortress §6.2) show each champion in the same room with no Rockman: each boss here has a **credits mode** (§1.7.2, §2.8.2, §3.8.3, §4.7.2) on tech's `IFCREDITS`, costed in fortress's ending row, with fortress's card-strip fallback |

## 8. Lessons applied

- **CX 1, one premise everywhere**: bounties are prize money, the sortie is judged in percent, the quick-draw has a flag
  judge and a scoreboard, Knight's King records your deeds, every death gets a commentator line.
- **CX 2, a homage is a mechanic**: 1943's rules, the RPG's command windows and hidden stairs, the light-gun timer, the
  2600 jungle's 3:1 underground and treasure rules, each the core of its venue and all of them in v1.0.
- **CX 3, voice on failure**: per-venue death rotations, the King's death line, the Knightlord's YES.
- **CX 4, the partner as a second body**: one optional Break Man hook per venue, all v1.1 with the partner.
- **CX 5, reuse set pieces with one twist each**: the spike ceiling gets HP (its one use in this venue); Wind Man's pull
  becomes his push; the dome dispenser becomes bounty 1; Tomahawk's parallax carries the train; vanilla's plate routes
  become the secret routes.
- **CX 6, telegraph tools**: lamp boards, windsocks, the battle log, the croc's red eyes, the boiling tar, the "TUNNEL!"
  sign and whistle, the flag and bell, the Sheriff's and the conductor's counts, the stairs' key check.
- **CX 7, special cases in visible code**: Y.SPEAR's pierce, the permanent shield break, the Metal Metslime's 1 damage,
  each weak reaction (SC9); the own-weapon jokes when SC4 ships.
- **CX 9 / 4MI 10, testability**: fixed encounter triggers, data-driven waves that delay rather than drop, and a draw
  delay seeded at the screen lock keep every set piece deterministic for golden movies.
- **4MI 1, the weakness in the i-frames**: every weakness reaction is a stagger window, not just damage.
- **4MI 5, behaviour gates with after-the-fact hints**: four behaviour chips and twelve real tier B hints.
- **4MI 6, old weapons, new jobs**: C.FLASH stalls engines and hits every gallery window; F.BLAST burns logs; PLANT.B
  makes outlaws sneeze; Y.SPEAR pierces shields.
- **4MI 7, the theme as mechanics**; **4MI lesson "accessibility = difficulty"**: one CASUAL lever list per venue and
  reflex windows with an input-lag offset; **4MI 8, HARD as poke lists** (kept for v1.1); **4MI 11, the raster list**;
  4MI's Cossack 1 fixed-screen shoot-'em-up is the precedent for T1-lite.
- **RM6 1-8**: vanilla ids kept; one tileset slot per venue with art entering by CHR thirds (Plant's 0 free tiles);
  every set piece counted against the 9-slot cap; per-id alternate flips for the stairs and the tar pits; adaptors by
  win count with no adaptor on a normal exit; vanilla quirks kept on purpose (the Jet sky bypass, the Balancer room,
  the A and B plate rooms, the revisit palettes).

## 9. Risks

1. **Screen budget.** Tomahawk and Plant use 32 of 32 screens. Any new idea there costs an existing screen. Fallbacks:
   Plant merges 1B and 1C into one cavern screen; Tomahawk shortens the sky bypass to 2 screens.
2. **Plant's tiles.** Measured: no part of `$90` but the canopy third can be replaced on the jungle screens (§4.1).
   P-PITFALL must redraw the canopy in about 40 tiles and still read as a jungle. Fallback: keep vanilla's canopy
   (`$92`) and build the tar surface and croc water from black tiles plus sprites.
3. **Raster bands.** The sortie needs 4 band entries and the train 5, of 24 (R1.9); both depend on the generic raster
   list and MMC5's scanline IRQ, which the M0 spike tests (R1.1). Fallback: 2 bands (sky fixed, ground moving).
4. **Lag at the cap.** Many set pieces sit at exactly 9 occupied slots. Any later addition must take a slot away
   (artcheck rejects 10). An open pop-up and a player utility count too (§0.5): the directors and boss AIs wait for
   them, and the slice's G7 test measures a utility on a full screen before these venues are built. If M3's
   OAM-builder measurement raises the cap, the v1.1 extras (bats, a second robber, the destroyer) come back first.
5. **Knight depends on text v1b.** Encounters, the King and Sage, the offer and the stairs check are all dialogue and
   menus. Fallback: 4MI-style sprite words (as Pharaoh's curses) for the log and a two-choice sprite prompt.
6. **IRQ logic.** Knight's ceiling runs inside IRQ `$11` in vanilla; tech moves it to a per-frame controller in M2.4,
   and Knight loses exact golden equality there (a behaviour-equivalence test instead).
7. **Reaction-time content.** The quick-draw is a reflex test: 24 / 18 / 40 f plus INPUT LAG, a sound cue, and losing
   only costs the bounty. The delay is seeded at the screen lock, so Time Attack (v1.1) stays fair.
8. **Text volume.** story §10.4 counts 90 Must strings in these four venues (R8.4's single source), about a quarter of
   R8.4's ~400; HERO'S QUEST alone is 44. story's reserve trim list (not a plan) starts with Knight's battle log, and
   the windows stay one or two lines.
9. **Trademarks.** On-screen names follow R3.3, and the design notes describe the homages. **Quoted lines from other
   games are paraphrased, never verbatim, in both languages** (R8.4): the King's death line, the RUN refusal, the
   critical hit, the Princess's loop and the Knightlord's offer use story's new words (KNT.D1, S11, S16, S23, K01-K04),
   and the log's spells are "a fire spell" and "a healing spell".
10. **Cultural sensitivity** in HIGH NOON FRONTIER: §3.14's rules are Must. A reader outside the team should review the
    venue's lines and art at the art-acceptance gate (R5.1) alongside the native-JP review.
11. **Text fatigue in Knight.** START skips any window; replays auto-skip NPC text; the battle log stays (it is the
    boss's tell) but is one line and never blocks input.
12. **Skill-gated secrets.** Wind's 4 full squadrons, Tomahawk's Sidewinder and Plant's zero logs; CASUAL relaxes each
    by one step.
13. **Object ids.** About 40 new kinds in these four venues in v1.0 (about 48 with v1.1), against about 30 free vanilla
    type ids. tech's families `$F4`/`$F5` are a hard prerequisite.
14. **Art without an artist** (R5.1). The King, Sage, Sam, the Sheriff, Sidewinder and AYACO start as composites and
    may look rough; the art-acceptance gate (a local HTML page plus PNGs, R8.8) shows them to the user at M5 and M6.
15. **The skips and TIME.** LAND and EXPRESS only stay fair if systems adds the skipped set piece's length to `T`.
16. **Bass Mode** is Won't (v1), so the sky-bypass ladder, the Power walls and the sortie need no Bass answers now.

## 10. Open questions

Round 1's eleven questions are answered (consistency decisions 17, 18, 28 and 39): T1-lite is accepted; the lent
vehicle is a vehicle state, not a form; Y.SPEAR pierces without breaking; keys use T3's per-stage counter; Roll as the
princess and Tango as the cat are approved; the battle log uses the pop-up window; the music fits one cue per venue
(all Should); Plant's canopy redraw stays; group 1 keeps `$F` deadly; and the distinct secret arenas are Should, with
the boss room plus a new palette in v1.0. New ones:

1. **tech**: a per-screen pop-up position switch set by the screen script, or `EFFECTS` b6 extended to a screen mask?
2. **systems**: confirm the `T` additions for LAND (7,200 f) and EXPRESS (3,300 f), and the Metal Metslime special
   case.
3. **meta**: does Knight want a `VENUE_REC` (fastest Metal Metslime kill) and Plant one at all?
4. **story**: the new sixth Tomahawk death line, the PLT-06 and PLT-08 rewordings, and Tomahawk Man's new voice.
5. **art_audio**: can Wind's pinch set grow to 24 tiles (it adds the red plane and the POW), and can the windsock and
   the flag judge's stand live in BG in their boss rooms?
6. *(Answered in round 3: R8.6 fixes the CASUAL quick-draw at 40 f; R2.9's ×2 applies to every other reflex window.)*

Questions 1-5 are routed to their owners in [`reconcile.md`](reconcile.md): TECH-05, SYSTEMS-03 and SYSTEMS-04,
META-01, STORY-02, ART_AUDIO-03.

---

## Changes in round 2

| # | Change | Ruling / finding |
|---|---|---|
| 1 | Re-tiered to v1.0 Must / Should (v1.1+) / Could / Won't; added "v1.0 scope" with 14 sessions per venue (56, matching `tight.py`); split the venues_a rows of `tally.py` into v1.0 and v1.1+ with unchanged totals | R0.1-R0.4; scope-1, scope-2, scope-3 |
| 2 | On-screen names SKY ACE, HERO'S QUEST, HIGH NOON FRONTIER, LOST JUNGLE; homage sources described, not named, in design notes; "Harry", "Game Boy" and "Gun.Smoke" removed from on-screen lines; "Drakee" and "Charlock" labels dropped | R3.3; design-10; consistency-42 |
| 3 | Stage ids `$01`/`$06`/`$05`/`$02` with meta indexes; `SECRET_SCR` (renamed `PLATE_SCR`); the 48-byte record and the `NO_TAG` screen mask | R1.2, R1.14; consistency-21; feasibility-18 |
| 4 | Each venue's second set piece and secret-arena twist moved to Should, kept in full: Wind's gust decks and WING WALKER on the wing; Knight's Inn and Princess and the 1A throne; Tomahawk's train sky band, shimmer and bats and the rodeo fence; Plant's CONGA logs and swamp crocs and the Lost City ruins. Secret arenas in v1.0 = the boss room with a new palette | R0.2, R0.3 item 4; scope-2; consistency decision 39 |
| 5 | HARD poke lists and boss branches moved to Should (kept, tech §5.5 format); the quick-draw's HARD window stays in VA-DRAW | R0.3 item 3, R2.9, R1.10; scope-19, scope-25; consistency-15 |
| 6 | One CASUAL lever list filled in per venue (§1.8, §2.9, §3.9, §4.9) on the `CFG_CASUAL` tier | R2.9; design-7; consistency-16 |
| 7 | Every set-piece cap recounted with all occupied slots, cap 9: the sortie's enemy side ≤ 4 (red squadrons as chains of ≤ 3, a simple AYACO, no vanilla enemies on 01); encounters 9; Knight Man 9; the gallery ≤ 3 figures + 1 bullet; the train ≤ 4 enemy-side with 1 robber; Tomahawk Man's B gated; Plant's croc river 3 heads, ≤ 1 log, the ring guard, sprouts by `map_set`, 2 spores; CONGA's shot rule; the swamp ≤ 4 | R1.8; feasibility-4 |
| 8 | Wind: the LAND skip after the first clear (forfeits the run's sortie secrets, ACE and TIME gain); the tower shortened by two screens with a sortie callback on 07; the boss now on 13 | R3.8; design-16 |
| 9 | Wind: the sortie runs on tech's free-flight vehicle state, buster only; its flight and loop poses are a set-piece player sheet streamed at the catapult | R1.10, R2.3; feasibility-8; consistency-36; scope-17 |
| 10 | Windsocks, lamps, gallery windows, flags and sprouts are BG through the map-edit service; VA-TIMED, the stairs, trapdoor and outhouse use the per-id flip | R1.10; scope-10 |
| 11 | Knight: the stairs check the key count, and 18 has a ladder back to 15 | R3.9; design-22 |
| 12 | Knight: the dark basement, RADIANT and the sconces are Won't; the basement is lit | R3.1; design-5 (b) |
| 13 | Knight: the ceiling with HP is the venue's single use of the spike ceiling; its logic leaves IRQ `$11` | R3.1; design-5 (a); tech |
| 14 | Pop-ups default to the top; Wind 01 and Tomahawk 10-11 switch to the bottom; Knight's battle log uses the pop-up window with the commentators queued | consistency-26 |
| 15 | Y.SPEAR pierces the shield without breaking it; "AN EXCELLENT MOVE!" reserved for KAISHIN; KAISHIN is always the deterministic EXCELLENT MOVE | consistency-35; R2.4; design-6 |
| 16 | Tomahawk: HIGH NOON MESA (T-MESA, no graves) and the RODEO RING are Must; the Boot Hill line dropped; the draw is a judged event (flag judge, scoreboard); Tomahawk Man is a rodeo showman strict about etiquette; cactus walkers Must, no totem; THE HIDEOUT removed; the content note rewritten | R3.4; design-11 |
| 17 | Quick-draw windows 24 / 18 / 40 f plus INPUT LAG; the draw's three tells | R3.5; design-13 |
| 18 | The conductor reads the bounty count before boarding; the EXPRESS skip after the first clear; the 12 re-board kept as Should | R3.8; design-15, design-16 |
| 19 | Flash rules: the storm is one flash per strike (REDUCED: a fade); the tunnels fade; the encounter wipes; the Knightlord's red tint fades | R3.5; design-13 |
| 20 | The Eddie moral trade-off and Plant's "AND RUSH JET ADAPTOR" YOU GET line deleted | consistency-34 |
| 21 | Vines and the balloon on tech's attach state with vanilla ladder poses; only the buster fires while hanging | R1.10, R2.3; consistency-43; scope-17 |
| 22 | All counters on the HUD widget module; the treasures, squadrons and bounties use meta's stage-counter predicate; one collect-N secret per venue | R1.10, R3.1; scope-16; design-5 (i) |
| 23 | Featured enemies are in-stage tells with no PART; the four venue chips and the Energy Balancer are Must; YASHICHI and DARUMA are one exclusive family | R2.5, R2.6; design-6, design-9; scope-21 |
| 24 | Prize indexes for meta's PRIZES field; envelopes in every hidden room | R2.7; consistency-10, consistency-11 |
| 25 | Exhibitions are Could; the E1/E2 pairing is kept for v1.1 | R3.7; scope-9 |
| 26 | Every Break Man hook is Should; his call is a pause-menu row; Plant's brick wall loses the scarf emblem | R4.2, R2.10; scope-15 |
| 27 | Interaction on UP with B not held, suppressed 10 f after an alt; SELECT in-stage only swaps and toggles | R2.10; design-21 |
| 28 | Freeze classes listed for every new object | R2.2; feasibility-6 |
| 29 | Retagged [engine-ok] items that need code: the secret-boss test, the storm, CONGA's checkpoint hook, the new checkpoint script, the seagull | R1.14; feasibility-19 |
| 30 | Knight and Tomahawk wait for text v1b; v1.0 text counted per venue; tier A riddles and flavour hooks Should; 4 death lines per venue | R1.4, R4.5; scope-4, scope-18 |
| 31 | No new music for these venues in v1.0; vanilla fallbacks; the DRAW bell and the ACE fanfare are vanilla SFX | R5.2; scope-23; consistency-13 |
| 32 | Art starts from reuse and composites; per-venue v1.0 deltas for art_audio | R5.1, R5.3; scope-7; consistency-8 |
| 33 | Band budgets per scene; `RL_SHIMMER` = 2 entries; the sound update's 36-line rule; the train on 3 bands | R1.9; feasibility-15; scope-5 |
| 34 | Mid-boss fight ids and arenas listed for meta | consistency-44 |
| 35 | The new layouts may overwrite vanilla layout banks `$32`/`$33` after regression | R1.5; feasibility-13 |
| 36 | Milestones: LOST JUNGLE in M5; HERO'S QUEST, HIGH NOON FRONTIER and SKY ACE in M6 | R6; scope-4 |
| 37 | No ExGrafix and no extra CHR page in these venues | R1.3; feasibility-1; consistency-1 |
| 38 | Round 1's open questions answered and replaced by six new ones | consistency decisions 17, 18, 28, 39 |

---

## Changes in round 3

Against [`RULINGS.md`](RULINGS.md) §8 (R8.1-R8.8) and the venues_a table of [`reconcile.md`](reconcile.md).

| Id | Outcome | Section | Note |
|---|---|---|---|
| VENUES_A-01 | applied | §1.5-§1.6, §2.7, §3.7, §4.4; §0.9, §1.8, §2.9, §3.9, §4.9 | Every chip gate is a Must set piece (POW juggle in the sortie, the Metal Metslime on 12, the gallery, the four treasures and the rolling logs). The four CASUAL tables now carry systems §13.4's How column (`REFLEX`, `TIERVAL`, dormant checkpoints, `IFCASUAL` or a CASUAL poke); the YASHICHI juggle window is a timer (240 → 360 f), not a reflex window, so the chip gate keeps one relaxation step (8 → 6 hits) |
| VENUES_A-02 | applied | §0.5, §1.3.1, §1.3.4, §3.4, §3.5, §3.6, §2.8.1, §4.6 | The sortie, AYACO and the train were already at 5 + 4 = 9. Gaps fixed: the text runner and player utilities count (tech §7.12, §15.1), and every director and boss AI waits for them; the sortie's "up to 30 f" delay (which could reach 10) is now "delay, never drop"; AYACO's bomb bay waits for a lingering POW; Knight Man's D log closes before the fireballs; CONGA counts utilities; a screen with no director is measured by the slice's G7 |
| VENUES_A-03 | applied | §1.7.2, §2.8.2, §3.8.3, §4.7.2; §7; v1.0 scope | A credits-mode note per boss on tech's `IFCREDITS`: no player, patterns looped at an empty spot, no draw, no battle log; Plant's room restores its floor; fortress's card-strip fallback. Costed in fortress's ending row (tight.py), so no session change here |
| VENUES_A-04 | applied | §2.2, §2.3, §2.6, §2.7, §2.8, §2.8.1, §2.8.4, §2.11, §2.12; §1.10, §3.11, §4.11, §7, Risks 8-9; §3.5, §3.9, §0.10, §10 | The 1986-RPG lines follow story's paraphrases (KNT.D1, S11, S16, S23, S25, K01-K04; "a fire spell" / "a healing spell" on screen, BLAZE and HEALMORE as design labels). String counts cite story §10.4 (90 + 4 labels) instead of this doc's ~86. The CASUAL quick-draw was already 40 f; now cited to R8.6, and open question 6 is closed |
| R8.1 | applied | v1.0 scope (Milestones) | Per-milestone figures stated for §6's column: M5 14, M6 42; no stale ledger or cumulative figures were in this doc |
| R8.2 | applied | v1.0 scope, "What v1.0 depends on", §0.4 | The attach state's core arrives at M3 with Blizzard's condor; T5, the vine and the balloon at M5 |
| R8.6 | applied | §7 (venues_b row) | Yamato's nightingale floor is Should |
| R8.7 | applied | "What v1.0 depends on", §0.10, §3.5 | INPUT LAG range 0-6 f cited to R8.7 |
| R8.8 | applied | Risk 14 | The art-acceptance gate is a local HTML page plus PNGs |
