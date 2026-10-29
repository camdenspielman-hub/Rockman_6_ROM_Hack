# Rockman 6 GP: director's rulings (design round 1 → round 2)

These rulings resolve the four reviews of the first design round:

- [`review_feasibility_design.md`](review_feasibility_design.md): feasibility and design-quality critics.
- [`review_consistency_scope.md`](review_consistency_scope.md): consistency and scope critics.

They are **binding** on every doc in `docs/design/` and override [`BRIEF.md`](BRIEF.md) where they differ. Finding ids
(e.g. `feasibility-3`, `design-5`, `scope-4`, `consistency-11`) refer to those files.

**Default rule.** Any finding or "decision needed" not ruled on below is resolved as its critic recommended. Where two
critics disagree, the rulings below decide; where they are silent, **the more conservative option wins** (less scope,
fewer engines, vanilla behaviour kept).

---

## 0. The honest scale, and what v1.0 is

**R0.1 — The ledger is the scope authority.**

- As written, the design is about 830 focused sessions, about 550 of them Must (scope-1).
- The session ledger (`tools/plan/tally.py`, `tools/plan/tight.py`, seeded by critic-scope) decides scope from now on.
- It is re-estimated from actual counts after the vertical slice (M4) and at every ⛳ gate.

**R0.2 — v1.0 = the TIGHT MUST, about 440 sessions** (scope-2):

- **Engine:** all tech foundations.
- **Systems:** core systems with **weapon taps only**.
- **Meta:** the meta core.
- **Stages:**
  - 8 venues, each kept to its core: homage mechanic, secret exit, hidden room, behaviour chip, boss rework;
  - Opening-lite, HALFTIME RIOT, H1, H3, H5, W2, W3;
  - the ending, with a vanilla-engine staff roll.
- **Release ladder:**

| Release | Contents | ≈ sessions (cumulative) |
|---|---|---|
| **v0.1 "Blizzard slice"** | new game → bracket → Blizzard venue end to end → judges → save/reload/replay | ~115 |
| **v0.5 "Round One"** | Opening-lite, 8 venues, Halftime Riot; the scope checkpoint | ~285 |
| **v1.0 "Championship"** | + H1/H3/H5, W2, W3, ending | ~440 |
| v1.1+ | the Should list, in the cut-line order below, re-added from the top | — |

**R0.3 — The cut line, in priority order.** These items are out of v1.0, and come back in this order (scope-2):

1. Weapon alts and form synergies (§3).
2. The Break Man *tag partner* (the NPC stays Must; §4).
3. HARD per-stage poke lists and boss AI branches.
4. Each venue's second set piece and secret-arena twist.
5. H2, H4, W1 (and with W1: ExGrafix, F-ERA, POCKET).
6. The Exhibitions, redesigned as single arenas when they return. E4 Maze is Won't (v1).
7. Time Attack.
8. The victory-lap credits (one lap when built).
9. The PARTs + garage + Mr. Y booth + TURBO bundle.
10. The 1993 RULES preset.
11. GP Rush runner, courses, MY GP.
12. Achievements, ENGRISH, the attract crawl.

**Won't (v1):** KNOCKOUT, Exhibition Rules, Museum/VAULT, Bass Mode, Mr. X Returns, criticals.

If the budget tightens below 440, cut next: merge H5's unmasking into H3; make W2 a single-arena Bass final; reduce
the Opening to 3 tutorial screens.

**R0.4 — A Must item may depend only on Must items** (scope-3). Every doc re-tags against this rule.

**R0.5 — Context for the user.** CX took about 5 years and 4MI about 8. v1.0 at about 440 sessions is a long project
even with AI help. The release ladder makes every rung a playable, shareable build.

---

## 1. Platform and engine

**R1.1 — MMC5 go/no-go spike first** (scope-5, scope-11 decision).

- A 1-2 session spike on **Mesen** runs **before** M1.1, as a formal gate. It tests: the NES 2.0 header, 32 KB PRG-RAM pages, ExRAM as a nametable via mid-frame `$5105`, IRQ line timing, and form-sheet streaming at 256 B/frame.
- **Open question for the user:** the hardware target. Is an EverDrive N8 Pro or another cart available?
- If the spike fails, the contingency is BRIEF's MMC3 fallback with the tight Must re-cut.

**R1.2 — Stage ids: tech §4.2's map is binding** (feasibility-2, consistency-2, scope-12):

| Ids | Use |
|---|---|
| `$00-$07` | venues |
| `$08-$0F` | legacy Mr. X 1-4 / Wily 1-4, unchanged: regression, the 1993 data rows, the `???` fight |
| `$10` | Opening |
| `$11` | Halftime Riot |
| `$12-$15` | E1-E4 |
| `$16-$1A` | H1-H5 |
| `$1B-$1D` | W1-W3 |
| `$1E` | lap |
| `$1F` | Mr. X Returns (Won't v1) |
| `$20` | DEV |

fortress, meta and story renumber. The attribute table (M2.1) is needed before the Opening and Riot, not before the
Blizzard slice.

**R1.3 — ExRAM stays in mode 0 (text-window nametable) for the whole game** (blocker: feasibility-1, consistency-1).

- ExGrafix only in locked rooms with no text: the W1 16-bit section and the METALL 16 arena, filled in mode 2 while blanked, with commentary suppressed. That is Could, with W1.
- **There is no extra 4 KB CHR page.**
- The "SUPER colour" of W2/W3/escape in v1.0 = richer per-screen palettes + parallax/palette bands + **the MMC5 audio and the music channel drop** (D9 mute mask is Must).

**R1.4 — Text model** (feasibility-11, consistency-3):

- **Rendering:** a fixed-cell **glyph cache**; **EN ALL CAPS**; JP kana. The VWF is dropped.
- **Pop-up:** 2 × 28 cells, ≤ 24 glyph ids.
- **Dialogue, debrief and help pages:** 4 × 28.
- **Borrowed BG tiles are restored from ROM** (the build knows every screen's CHR state). There is no read-back buffer.
- **TALK, CHOICE and every frame-waiting UI run as yielding coroutines** (through `$E46C`), never inside the C-window (feasibility-10). CW pushes and pulls the previous `$5116` and registers; the NMI and IRQ stubs preserve the interrupted `$C000` bank; CW calls are forbidden from interrupt code.
- **Text v1a** (pop-up and debrief window) comes before the slice; **v1b** (dialogue, choices, NPC menus) comes before Knight.
- **Dictionary compression is Must.**

**R1.5 — Bank ledger owned by tech, printed on every build** (feasibility-13):

- Music 5 banks; text up to 10 banks (compressed); layouts 8 banks; tilesets per art's measured need.
- **The new venue layouts may overwrite vanilla layout banks `$32/$33`**, which are GP data, not Capcom art. Vanilla stages 0-7 are regression-tested from the base ROM before they are replaced.
- ExGrafix data, if it ships, is per metatile and per tileset, not per screen.

**R1.6 — WORK RAM** (feasibility-12): the unrolled VRAM copier lives in ROM (only a 128-256 B staging buffer in WORK). The map-edit log is 256 B. tech publishes a WORK ledger with an owner per range. PRG-RAM stays 32 KB.

**R1.7 — Stage changes and the fight loader** (feasibility-3, scope-6/12):

- `$3E:$CE44` (clear `$0340`/`$0650`) runs whenever the new stage id differs.
- A 64-byte "return-to" snapshot covers hubs and lobbies.
- A **FIGHT_CTX** byte makes the boss-death, clear and respawn paths return to the hub or lobby and skip YOU GET, flags and saves.
- **The fight loader is Must**, owned by tech. W2 uses it; EXTRA CONFIG's FIGHT command and the test mailbox use it.

**R1.8 — Lag budget** (feasibility-4): count **every occupied slot** (player, screen script, directors, shots, effects). The cap is **9** until M3 measures the OAM-builder gain. Directors fold into the slot-22 screen script where possible. tech §6.3 and artcheck enforce it.

**R1.9 — Raster list:** 24 bands per buffer; RL_SHIMMER = 2 entries; the sound update goes on a band followed by ≥ 36 band-free lines (feasibility-15).

**R1.10 — One of each engine, owned by tech** (scope-10, 16, 17, 25; consistency-9):

| Engine | Ruling |
|---|---|
| Map edits | **One map-edit service**: `map_set` plus a per-id alternate flip, one repaint queue with a per-frame budget. T6 = **variant blocks** (the bitmap is dropped). VA-TIMED and F-PIECES are built on it. F-GRID is deleted |
| HUD | **One HUD widget module** (digits, label, meter, icon row; data-driven). Every "collect N" secret uses meta's stage-counter predicate |
| Player states | **One attach state** (vine, balloon, condor, claw, arrow) and **one free-flight vehicle state** with a lane flag (SKY ACE; CANNON if the Exhibitions return) |
| Poke lists | **One poke-list format** (tech §5.5). Fix the IFHARD macro bug (consistency-15) |
| Tilesets | **One tileset-slot table** (tech's RAM-image model, 2 slots per bank, independent alternate sets). TS_STADIUM serves the Opening, Riot and lap; art_audio's table is regenerated from tech's |

**R1.11 — Player-side object slots** (feasibility-9): shots in 1-3; one GP utility each in 4-7; Beat's rescue reuses 4. Caps per weapon fit the plan (e.g. M.BEAM max 2). Utilities that damage call `$38:$8FDF`.

**R1.12 — Engine audits before new player variants** (feasibility-14):

- The `$9B` readers get the same static and coverage audit as the `$51` readers, before SUPER becomes form 3.
- **Break Man is a slot-0 character variant**: a character byte, his own physics constants, stashed HP, and his sheet streamed at beam-in. Family `$FC` is dropped.

**R1.13 — Missing prerequisites are scheduled** (scope-6):

- **CHR set table v2** (8-bit source bank, stage-local ids) before any new art.
- The minimal art pipeline: `chr.py`, `sprites.py`, `palettes.py`, `artcheck.py`.
- `bgboss.py` before the H wings.
- T5/T7/T8 and the attach and vehicle states, in the first tranche that needs them.

**R1.14 — Small engine rulings:**

- Helpers return vanilla A values (feasibility-22).
- The `$36` sound tail is reserved for SFX.
- DPCM, if any, lives in `$7F`.
- Each DEV combo has one meaning.
- IRQ handler 0 is kept as a preset (feasibility-21).
- The stage-attribute record widens to 48 bytes; NO_TAG becomes a 32-bit screen mask (feasibility-18).
- Every [engine-ok] tag that needs code is retagged [new-code] (feasibility-19).
- The free-id canvas scan runs before text M2.5 (scope-24).

---

## 2. Combat, systems and economy

**R2.1 — Punch scoring.** Vanilla attack bytes stay (`$11-$14`). Scoring categories come from **LATCHSRC**. There is no punch re-class, so no AI latch sites are patched (feasibility-5).

**R2.2 — Frozen objects keep taking damage** (feasibility-6).

- A per-(type, or family + sub-id) *frozen handler* applies to enemies whose damage step is `$E9D7`/`$EA20`/`$EA6E`.
- Everything else is **NOFREEZE**: it ignores freezes but still takes hits.
- Bosses get a boss-side frozen state, not a skipped AI.

**R2.3 — Form swap.**

- **16-20 frames** behind the flash. The M1 spike tests 256 B/frame on still frames. Keep 8 KB CHR-RAM. The vanilla docking cutscene plays once per form per save (feasibility-7, consistency-5).
- Each form gets a per-form `$71-$7F` map. Set pieces that change Rock's body use a **dedicated set-piece player sheet** streamed at a locked moment, never the 15-tile weapon slot (feasibility-8). artcheck rejects any weapon-slot set over 15 tiles.

**R2.4 — Weapons in v1.0** (scope-8; design-6).

- **Must:** every form fires every weapon's **tap**; the dispatch table has alt and synergy columns.
- **Should (v1.1):** the 8 alts and 8 synergies, added one weapon at a time.
- **B.ATTACK's Ice Block ships in the Blizzard slice** as the prototype for alt dispatch and the frozen tick.
- Bosses may preview their weapon's alt as a boss move (that is AI, not player code).
- **The parry is Could. Criticals are Won't**: KAISHIN is the deterministic EXCELLENT MOVE (+2 on every 12th boss hit).

**R2.5 — Chips in v1.0: 14** (design-6, scope-21):

- the **8 venue behaviour chips** (all Must, including venues_b's four: scope-3);
- the **Energy Balancer**;
- **5 shop chips**: SHOCK ABSORBER, SPIKE GUARD, CHARGE KIT, EXCHANGER, ENERGY SAVER.

Cut: AFTERIMAGE, GLIDER, JET TUNER. **PARTs, the garage, the Mr. Y booth and Y-TURBO** are one **Could bundle** that ships together with the tag partner. Featured-enemy one-shots stay as in-stage tells, with no PART drop. meta's FILE block moves to the final chip bits and adds prize bits (consistency-11).

**R2.6 — Safety nets don't stack** (design-9):

- A Break Man retreat uses up his call for the rest of the stage.
- Beat's rescue works once per screen.
- YASHICHI and DARUMA are one mutually exclusive "second wind" family.
- Tune at M4 by measuring deaths per stage with a full loadout against an empty one.

**R2.7 — Economy fixes:**

- venues_b's bolt bags become **sponsor envelopes**, one per hidden room, within systems' income model (consistency-10).
- Prize bolts stay capped at 60 per venue.
- The rating is **re-derived so 100 is reachable with v1.0 content**. T1 (partner) and T7 (TURBO trap) exist only when the bundle ships; T3 (Exhibitions) is removed in v1.0 (scope-3, decision 8).

**R2.8 — Doping** (when the bundle ships; design-8): the cost is the partner, the asterisk, T1 and the headline. TAG-gated secrets use their full-charge-door fallbacks. Mr. Y's second confirmation says **"BREAK MAN WILL WALK."**

**R2.9 — Difficulty** (design-7, scope-19/20):

- **CASUAL** gets a `CFG_CASUAL` bit and CASUAL poke lists in tech's format. **Every stage fills in one standard lever list:**
  - reflex windows ×2;
  - mash counts −40% (hold-to-struggle allowed);
  - set-piece timers +50%;
  - +1 checkpoint per section;
  - skill-gated secrets relaxed by one step.
- **HARD in v1.0** = ×1.5 damage, drops LESS, no refill; the framework hooks stay. Per-stage HARD poke lists and boss branches are Should.
- **1993 RULES** is Could. When built, its rules change but its content does not; it defines a 1993 column for every new fight, and complete plates give the Beat rescue.

**R2.10 — Input** (design-21):

- Interaction happens on an UP press with B not held, and is suppressed for 10 frames after an alt.
- In-stage, SELECT means **only** the quick swap and last-weapon toggle.
- Break Man's call is a **pause-menu row confirmed with A**. Help pages open with B on the CHIPS page.

**R2.11 — Gamma** (design-3, consistency-12): **POWER (owned from the 2nd win) may be required in the fortress, with a tell.** H3 adds a no-risk fist-ride practice beat before the fight. SC5's 1993 behaviour is stated. In v1.0, Gamma is **head and fists only** (about 100 tiles).

---

## 3. Content

**R3.1 — Repetition cuts: adopt all of design-5's swaps.**

| Where | Change |
|---|---|
| H4 compactor | Dust Man conveyors, no ceiling chain |
| Escape 0A | crumbling ladders |
| Dark rooms | one "lights on a timer" set piece only (the Riot's); H4's Bright rooms become a flash-bulb photo puzzle |
| Centaur 10-13 | a **tidal shaft** that floods as you climb (the tide is the venue's spine) |
| H3 Gemini | its laser fallback |
| Doc Robot MK-VI | Should; when built, he copies a Rockman 2 boss (R3.6) |
| Flame Man's DUEL | a spacing duel: he parries shots fired within 48 px, with a blade-glint tell. Knight alone owns the shield |
| Yamato's sekisho | one pass plus a ryo bribe, or the scroll gate alone |
| Non-venue hidden-room keys | use the new tools (M.BEAM stair, Super fist return); Time Stop keys wait for the alts |
| "Collect N" secrets | **at most one per stage** |

**R3.2 — Yamato is trimmed** (design-25): cut the kite run, and the bonk-stun *or* the sekisho (designer's choice). The pogo, the Daruma and the nightingale floor carry the venue.

**R3.3 — Names and trademarks** (design-10, decision 6):

- **On-screen venue names:**
  - Knight: **HERO'S QUEST**
  - Plant: **LOST JUNGLE**
  - Flame: **PERSIAN PALACE**
  - Wind: **SKY ACE**
  - Tomahawk: **HIGH NOON FRONTIER**
  - Blizzard: **SUMMIT CLIMBER**
  - Centaur: **ATLANTIS RUINS**
  - Yamato: **EDO NINJA ROW**
- **No third-party trademarks or character names on screen.** Capcom's own (1943, Gun.Smoke, DuckTales) may be nodded to in plaques and design notes.
- **Plaques describe; they don't name third-party games** ("a falling-block puzzle born in Moscow, 1984"). That keeps the commentators' "can't say the trademark" gag coherent.
- Remove Blinky, Popo/Nana, Pit and Harry from jokes.

**R3.4 — Cultural fixes, Must** (design-11, design-12).

- **Tomahawk:**
  - The arena is **HIGH NOON MESA**, with no graves.
  - The secret arena is the **Sheriff's office / rodeo ring**.
  - The Boot Hill line is dropped.
  - The draw is staged as a **judged tournament event** (flag judge, scoreboard).
  - Tomahawk Man is a **rodeo showman who is strict about duel etiquette**, not stoic.
  - The cactus re-skin of `$12` is Must; "totem" is dropped as a featured enemy.
- **Flame:**
  - No "Oil Sultanate".
  - Screen 18 is domes and a full moon: **no minarets, no crescent**.
  - The vizier exists only as an obvious Wily-in-costume gag.
  - The jokes aim at Prince of Persia's mechanics.

**R3.5 — Accessibility** (design-13):

- **Flashes:** in the default mode, no effect flashes a large area more than 3 times per second. REDUCED turns every flash into a fade. Add a health notice at boot.
- **Quick-draw windows:** NORMAL 24 f, HARD 18 f, CASUAL 40 f, plus an **INPUT LAG** offset in CONFIG.

**R3.6 — Bosses in v1.0** (scope-13/14):

- **Grand Pi-kun:** one size (the Mr. X 2 pod technique).
- **The W3 machine:** vanilla Wily Machine 6 art (`$BE`), retinted, with the **8-band** programmatic floor carrying the Mode-7 joke. Its panel reads **WILY MACHINE 6.5**. F-SIZES, the 16-band floor and the drive-toward-camera sizes are Should.
- **Bass β:** copies only the weapons whose tiles are pre-drawn into his own boss set (4).
- **Doc Robot MK-VI:** Should. If built, he **copies a Rockman 2 boss** and is reached through the fight loader, never by running champion AI in H3's room. v1.0's H3 mid-boss slot is a re-skinned vanilla mid-boss.
- **The W1 boss is METALL 16** (Could, with W1).

**R3.7 — Exhibitions** (scope-9): Could (v1.1). When they return, each is one lobby plus a "rule boss" arena, built on `map_set` and T6. E4 Maze is Won't (v1).

**R3.8 — Replays** (design-15/16/20):

- After the first clear, offer skips for fixed-length set pieces. Wind's **LAND** option forfeits that run's sortie secrets and score rows.
- The Tomahawk conductor reads the bounty count before boarding.
- When the victory lap is built, it is one lap with more optional.
- Each Exhibition gets its own hidden-room trick, or none.

**R3.9 — Small design rulings** (design-17/19/22/23):

- Contact with Shadow Rock is harmless while you haven't fired, and the mirror glows when a merge is possible.
- W1's half-damage rule is dropped.
- Knight's stairs check the key count, with a ladder back to 15.
- "THEY SAY THIS GAME CAUSED A COIN SHORTAGE".
- Plaques use **BLUES**.
- The Wily line is varied at every step of the ladder.

---

## 4. Characters and story

**R4.1 — story.md owns every word and the ending** (design-1, consistency-6). The ending order is:

1. escape;
2. the castle pixelates;
3. **Break Man catches Rock and Wily** (S40);
4. the arrest, with **one** use of the Mr. Y / Mr. Z gag;
5. the podium and Bass's vow;
6. the CAPCOM TIMES (no `$94` reprint);
7. credits: v1.0 uses the vanilla staff-roll engine with GP text and the DWNB cards;
8. rating and Break Man's debrief;
9. **LIGHTS OUT** (S42);
10. the sixth-wing plaque (S43);
11. TO BE CONTINUED.

The last sound is pulse 1 alone. The door-holding and roof variants are deleted from fortress. fortress's staging must match story's scene list.

**R4.2 — Break Man** (design-2, consistency-7, scope-15):

- **The disguise is respected.** Only Rock says "Blues?" (twice), and Light says the name once, at the very end. Delete every "OBVIOUSLY Blues" line.
- **Introduction:** the masked Opening roll call (S06), no name spoken.
- **Joins at HALFTIME RIOT 0E**, with S20's Rule 9 lines played in place.
- **NPC Break Man is Must:** a composite of about 10 frames built from Rock's sheet (visor, scarf, palette), for cutscenes, the Riot, H5 and W3.
- **The playable partner is Should.** Without him: the TAG rooms become full-charge doors, and rating T1 is replaced (e.g. "Riot won without the HP<6 capsule").

**R4.3 — Renames and identities:**

- **SEMIFINAL RIOT → HALFTIME RIOT** (design-14).
- Entrant numbering follows story: Rockman 9, Bass "entrant β".
- The Riot crowd is the fortress's **rejects** (they are mechanics). Story S17/S18 is rewritten to match.
- The Mr. Y YES/NO heckle is the **1-bolt respawn insurance** gag.

**R4.4 — The Opening is capped at about 15 SCN pages** (design-4):

- One intro: story S02 is the attract crawl, and NEW GAME goes straight to the tunnel.
- The rules are folded into the lane judges.
- The roll call is the float lines only.
- The Wily gag plays once per act, with varied wording.

**R4.5 — Text volume in v1.0: about 350 Must strings** (scope-18):

- death tables (4 per stage);
- first-weakness lines;
- secret and plate lines;
- Must scenes;
- **tier B hints only**;
- help pages for the 14 chips.

Tier A riddles, flavour hooks and heckle variants are Should. **The native-JP review is a dated external dependency that gates release** (user question).

---

## 5. Art and audio

**R5.1 — Baseline: no pixel artist** (scope-7). Reuse, composites and programmatic art come first, and **Claude's drafts are final**; a human pass is optional polish.

- Every new enemy starts as a recolour or composite of vanilla RM6 sprites, counted honestly as R.
- **One size per BG boss.**
- **16×16 face icons + name labels** instead of portraits and match-card portraits in v1.0. Portraits are Should.
- **Break Man and Bass β are composited from Rock's sheet.**
- Frame caps: 8 per enemy, 16 per boss.
- **An art-acceptance gate** with screenshots for the user at every milestone.
- Must art target: about 3,900 tiles and 350 frames, about 50 sessions.
- **User question:** will a pixel artist be recruited later?

**R5.2 — Music** (scope-23, consistency-13): art_audio owns one track list.

- **Must:**
  - G00-G04;
  - the **ending lights-out arrangement** (2A03 stems; MMC5 stems Could);
  - a 2-second whistle jingle;
  - the D9 mute mask.
- **Should, with vanilla fallbacks** (`$0B`, `$18`): RIOT, FINAL LAP, the POCKET arrangements.

**R5.3 — art_audio re-runs every budget after these rulings** (consistency-8): Pi-kun's single size, METALL 16 (Could), the mid-bosses, the rejects, the cut Exhibitions, and face icons.

---

## 6. Milestones (replaces PLAN §8 and tech §16's ordering; scope-4)

Cumulative ≈ sessions in brackets. ⛳ = the user plays it.

| M | Contents | ≈ |
|---|---|---|
| **M0** | Workbench: build, BPS, hook registry, allocator, test runner, golden recording, ledger. **MMC5 go/no-go spike on Mesen** | [12] |
| **M1** | Literal MMC5 port with golden equivalence; PRG-RAM, save skeleton, mailbox | [25] |
| **M2** | Slice engine: families and sub-ids; WRAM layouts and `map_set`; CHR set table v2 and minimal art tools; level pipeline with canvas table; raster list; **text v1a**; track table and MML; save, file-select-lite, bracket-lite, results, debrief, EXTRA CONFIG | [70] |
| **M3** | Slice systems: SELECT and form swap; taps in all forms; adaptors by win count; GP_BOSSHIT, WEAK!, frozen tick; scorecard and bolts; shop (3 chips); T6, X-BONK, X-WRAP; HUD widgets; commentator bus | [95] |
| **M4** ⛳⛳ | **BLIZZARD end to end** (v0.1): new game, bracket, venue (exit, room, chip, Ice Block, boss), judges, save, reload, replay. **Re-estimate the ledger** | [~115] |
| **M5** | Stage-attribute table; Opening-lite; Flame, Plant, Centaur, Yamato | [~205] |
| **M6** ⛳ | Text v1b; T1-lite; Knight, Tomahawk, Wind; HALFTIME RIOT. **"Round One" checkpoint (v0.5)** | [~285] |
| **M7** | BG-boss tooling, the fight loader; H1, H3, H5 | [~340] |
| **M8** ⛳ | W2, W3, ending | [~380] |
| **M9** | Native-JP review, balance, emulator and hardware matrix, BPS release (v1.0) | [~440] |

**Testing policy** (scope-26):

- Golden movies run on NORMAL + EN only.
- One smoke movie per other setting per milestone.
- Movies are re-recorded only at gates.
- Test overhead is about 10% of code sessions, in the ledger.

---

## 7. Questions only the user can answer (they don't block round 2)

1. **Hardware target.** Will GP run on real hardware? Which cart (EverDrive N8 Pro, other)? This decides how strict the MMC5 spike is.
2. **Art.** Will a pixel artist join (now, later or never)? The plan assumes never.
3. **Japanese.** Is a native-speaker reviewer available for the JP text, and when?
4. **Title.** ROCKMAN 6 GP (default), *Shijō Saidai no Kaizō!!*, or ENCORE?
5. **Budget pace.** Roughly how many sessions per week? The ledger turns that into dates.
