# Rockman 6 GP: the non-venue stages (fortress.md)

Owner: design-fortress. Status: **round 3**, revised against `RULINGS.md` (binding; it overrides `BRIEF.md`), the four
critic reports (`review_feasibility_design.md`, `review_consistency_scope.md`), `crossrefs.md`, and the round-2
revisions of `tech.md`, `systems.md`, `venues_a.md` and `venues_b.md`; round 3 applies `RULINGS.md` §8 (R8.1-R8.8) and
the fortress requests routed in `reconcile.md` (§"Changes in round 3"). Scratch: `build/revise/fortress/` (round 1's
text is kept there as `fortress_round1.md`).

Scope: every stage that is not one of the 8 Heritage Venues, and the staging of the ending.

| § | Stage | Engine id (R1.2) | Meta index | Tier |
|---|---|---|---|---|
| 1 | **OPENING CEREMONY** (Opening-lite): the players' tunnel, four warm-up lanes, the parade, Grand Pi-kun | `$10` | 0 | **Must** |
| 2 | **HALFTIME RIOT**: the rejects, Break Man's beats, Bass β duel 1 | `$11` | 9 | **Must** |
| 3 | **EXHIBITIONS** E1-E3 as single arenas; E4 | `$12-$15` | 10-13 | Could; E4 Won't (v1) |
| 4 | **HALL OF FAME** H1, H3, H5 (+ Mr. Y's unmasking); H2, H4 | `$16-$1A` | 14-18 | H1, H3, H5 **Must**; H2, H4 Should |
| 5 | **SUPER WILY CASTLE** W2, W3 and the escape; W1 | `$1B-$1D` | 19-21 | W2, W3 **Must**; W1 Could |
| 6 | The **ending** (staging), the v1.0 credits; the victory lap | — / `$1E` | — / 23 | ending **Must**; lap Could |
| 7 | Mr. X Returns | `$1F` | 22 | Won't (v1) |

**Who owns what** (RULINGS R1.10, R4.1, R5.2 and the critics' decisions; this doc follows the single sources of truth):

- `systems.md` owns combat, the economy and the chips. Every damage cell, special case (SC), price and bolt payout here
  is a citation of systems or a proposal to it.
- `meta.md` owns the save bytes, the bracket, the events, the debrief and the rating.
- `tech.md` owns ids, memory, the raster list, CHR, the tileset slots and every shared engine (map-edit service, HUD
  widgets, attach and vehicle states, poke lists, the fight loader).
- `story.md` owns **every word** and the ending's scene list (S01-S51). Every quoted line in this doc is a draft or an
  intent for story; plaques, hints, hooks and panels are story's to finalise.
- `art_audio.md` owns the tile, byte and track budgets; this doc says what each asset is and which technique draws it.
- **This doc owns staging**: layouts, set pieces, mechanics, boss patterns, secrets and their predicates, scene placement
  and order. What it needs from the others is collected as requests in §9.

**Notation.** Vanilla screens are **vNN** (`docs/research/rm6/img/maps/`, `rm6/fortress.md`); GP screens are plain **NN**.
Tags per BRIEF §8: **[engine-ok]** only for vanilla as-is or data only (R1.14, feasibility-19); anything built on one
of tech's new engines says so ("data on tech's map-edit service") or is **[new-code]**; **[new-art]**, **[new-music]**;
size **S/M/L**; tier **Must / Should (v1.1+) / Could / Won't (v1)** (R0.3). Frames are at 60 Hz. Boss HP is in bar
units (28 = a full bar). **[n]** in a table = the occupied object slots at the worst moment of that screen or pattern,
counted by R1.8's rule (§0.8); the cap is 9.

---

## v1.0 scope

**What ships in v1.0** (RULINGS R0.2): Opening-lite, HALFTIME RIOT, H1, H3, H5, W2, W3 with the escape, and the ending
with a vanilla-engine staff roll. **70 focused sessions** of stage code, data and tests (`tools/plan/tight.py`, area
`fortress`; `tally.py` lists the same rows as Must). Shared engine pieces are counted under tech (F-PIECES, the fight
loader, `RL_FLOOR8`, the HUD widgets, the lighting service, the NPC Break Man object), combat rules under systems (SC5,
SC6, SC11, M.BEAM, the Super Adaptor), and art, music and text in their own ledgers.

| Stage | Milestone | v1.0 content (the core) | Sessions |
|---|---|---|---|
| **Opening-lite** (§1) | M5 | NEW GAME → the players' tunnel; four warm-up lanes whose judges each announce one scorecard row (jump/DAMAGE, limbo/TIME, high striker/STYLE, stands/SECRETS); the scoreboard page; the parade of eight floats with one line each and the high fives; the sabotage; **Grand Pi-kun, one size** (R3.6); Pi-kun's dressing room. ≤ 15 scene pages (R4.4) | 8 |
| **HALFTIME RIOT** (§2) | M6 | The stadium at night overrun by the **rejects** (R4.3): VENDING MAN and CHEER MAN with the audition rule; the one lights-on-a-timer set piece (R3.1) with fuse boxes and the master breaker; the Bass sighting and crumbling floor; NPC Break Man's help (he holds the crowd), block and reveal, with S20's Rule 9 lines played in place at 0E (R4.2); **Bass β duel 1** copying his 4 pre-drawn weapons (R3.6), the β OVERDRIVE finish and the HP < 6 help capsule; the locker room (a full-charge door, R4.2) | 10 |
| **H1 ROCKMAN** (§4.1) | M7 | Wily 2 remix; the useless SCORE and its 24 score balls; the Magnet Beam case and the 96-px gap; timed appearing blocks; Elec Man's beams; Fire Man's pillars; Big Eye MK-VI; **Yellow Devil MK-VI** on F-PIECES; the archive branch and the box-art storeroom | 9 |
| **H3 ROCKMAN 3** (§4.3) | M7 | Mr. X 3 remix; the Rush Coil exhibit; the Break Man statue; Needle Man's presses; Gemini Man's laser hall (R3.1); **KAMEGORO MAKER MK-VI**, a re-skinned vanilla mid-boss (R3.6); the no-risk fist-ride practice beat (R2.11); **Gamma MK-VI, head and fists only**, POWER required in phase 2 with its tell (R2.11); the Super Adaptor dock and demo room; the Doc Robot workshop behind an M.BEAM stair (R3.1) | 10 |
| **H5 ROCKMAN 5** (§4.5, §4.6) | M7 | Mr. X 4 remix; Star Man's low gravity; the gravity rooms' low-gravity form; Crystal Man's crystals; the Super Arrow ride; the ROCKMAN5 letters (R8.5); the 1993 wing and Mr. X's card; **Dark Man MK-VI** with the lying boss panel and the WRONG NOTE exposure; **Mr. Y's unmasking** (two masks) | 9 |
| **W2 BRACKET OF DOOM** (§5.2) | M8 | Wily 3 remix in SUPER colour (palettes + parallax and palette bands; the 2A03 music keeps all its channels, R8.3); the hub as a bracket board; **pair bouts through tech's fight loader and FIGHT_CTX** (R1.7) into each champion's own arena; 8 SUPER copies; the Championship Ring and **Bass β duel 2**; the losers' bracket room | 8 |
| **W3 WILY MACHINE 6.5** (§5.3, §5.4) | M8 | Wily 4 remix; the Trophy Dispenser and the GP Cup; **WILY MACHINE 6.5** on vanilla Wily Machine 6 art, retinted, over an **8-band floor** (R3.6); the Wily Capsule SUPER and Break Man's gift (SC11); **the escape** with crumbling ladders (R3.1), injury time and Wily caught at the door; Wily's trophy room | 11 |
| **The ending** (§6) | M8 | R4.1's scene order: the castle pixelates, Break Man catches Rock and Wily, the arrest, the podium and Bass's vow, the CAPCOM TIMES (no `$94`), **the vanilla staff-roll engine with GP text and the DWNB cards**, the rating and Break Man's debrief, LIGHTS OUT, the sixth wing, TO BE CONTINUED. The last sound is pulse 1 alone | 5 |
| | | **Total** | **70** |

Round 1's `tally.py` gave these stages 94 Must sessions and `tight.py` 69. The +1 against `tight.py` is the ending: the
v1.0 credits keep vanilla's show of each champion fighting in his own room, and the eight reworked boss AIs need a
credits mode with no Rockman and a test for it (§6.2; the fallback, card strips only, costs nothing more).

**Milestones** (RULINGS §6). The Opening-lite lands at **M5**, before text v1b (M6): its scenes run as **pop-up
sequences under a script lock** on text v1a, and story may move them into the 4 × 28 window at M6 (§1.1). The Riot
lands at M6 after text v1b. H1, H3 and H5 land at M7 after `bgboss.py` (R1.13), F-PIECES and the `$9B` audit. W2, W3 and
the ending land at M8, after the fight loader (M7) and with `RL_FLOOR8`. Per milestone this doc's share is **M5 8, M6
10, M7 28, M8 24** (70 in all); R8.1 adds these figures into RULINGS §6's cumulative column (v0.5 ≈ 342, v1.0 ≈ 450).

**Every v1.0 item rests only on Must items** (R0.4, scope-3):

| v1.0 item | Rests on (all Must) |
|---|---|
| Opening-lite | tech: stage record and ids `$10+` (M5), TS_STADIUM slot (§5.3), `RL_FLOOR`, text v1a, the commentator bus; systems: scorecard rows, attack bytes `$11-$14`, GP_BOSSHIT row 8; meta: the first bracket hand-off, the debrief, SECRETS m0; story: S03, S04, S06, S08 within 15 pages; art: TS_STADIUM, the parade set (8 vanilla idle frames), Pi-kun at one size |
| HALFTIME RIOT | tech: text v1b, the palette-flash and lighting service (§8.5), `COLL_GROUP` (the crumbling `$1D` group), the NPC Break Man (family `$F7`), the boss panel extension; systems: SC6, LATCHSRC's FULL flag, the help capsule as a pickup; meta: RATEFLAGS b2 RIVAL and b4 SOLO RIOT (rating T1, R8.5); story: S17-S20 for the rejects; art: two rejects, Bass β composited from Rock's sheet with 4 pre-drawn shots, the NPC Break Man composite; music: G04 and the whistle jingle (both Must, R5.2) |
| H1, H3, H5 | tech: `bgboss.py`, F-PIECES on the map-edit service, `alt_flip`, the HUD widget module, the `$9B` audit before SUPER, the boss panel re-type (the arrow, the fists and the practice fist use the vanilla lift contact); systems: M.BEAM (64 px, max 2), SC5, the Super Adaptor, FORMS.SUPER on the dock, the mid-boss and machine defaults; meta: EVENTS b4/b6, EVENTS2 b4, the Hall of Fame map, RATEFLAGS b1 (the card); story: S25-S33; art: the MUSEUM CHR third and the wing contents |
| W2 | tech: the fight loader, FIGHT_CTX, the return-to snapshot (M7.2), `RL_PALBAND`; meta: fight records `$00-$07` with a SUPER palette and a pinch byte; venues: each boss reads the per-fight pinch byte (both venue docs accept it); systems: SC6 pre-adapted from BASS_ADAPT |
| W3 and the escape | tech: `RL_FLOOR8` (M8), the HUD widget (the clock), the map-edit service (crumbling ladders), the lighting service; systems: SC11 CHAMPION BUSTER, Beat's rescue; story: S38-S40 |
| The ending | tech: the D9 mute mask (Must, R5.2), the vanilla newspaper and staff-roll engines through the language hook; meta: the rating and the debrief; story: S40-S48; music: G37 LAST MATCH (Must; art_audio adds it, consistency-13) |

**Not in v1.0.** Kept below in place as v1.1+ material, each marked:

| Tier | Items (R0.3 cut-line item) |
|---|---|
| **Should (v1.1+)** | **Item 2, the tag partner**: Break Man's join pages and banner (S20 pages 3-6), the TAG opening of the Riot's and W2's rooms, H5's TWO BREAK MEN, the H1/H3/H5 tag pockets, the `NO_TAG` masks. **Item 3**: HARD poke lists and boss branches for every stage (kept in tech §5.5's format, counted in systems' HARD line). **Second set pieces**: H1's Guts lifts, H3's magnet pull (with venues_a's VA-GUST, itself Should), H5's Wave Man geysers, the Riot's roof gust and UMBRELLA MAN, W3's drive-toward-camera approach (F-SIZES + the 16-band floor), Grand Pi-kun's three sizes, **Doc Robot MK-VI** (he copies AIR MAN through the fight loader, R3.6), Bass's COUNTER (SC10). **Item 5**: H2 and H4 |
| **Could** | Item 5: **W1 Upgrade Lab** with F-ERA, its locked ExGrafix rooms and the POCKET arrangements (R1.3); the escape's eras; the ExGrafix bloom of the castle picture. Item 6: **the Exhibitions E1-E3** as single arenas (R3.7). Item 8: **the victory lap**, one lap (R3.8). H5's gravity flips. The doped variants (with the PART/TURBO bundle) |
| **Won't (v1)** | E4 Maze (R0.3); Mr. X Returns (R0.3); Gemini Rock (R3.1 keeps the laser); the escape's Rush catch (S40 is the catch, R4.1); the door-holding and roof Break Man variants (R4.1); every "OBVIOUSLY Blues" line (R4.2); the Museum's plaque gallery (meta's Museum is Won't) |

Estimates for the rest (`tally.py`, area `fortress`): Should 31.25 (Pi-kun's sizes 1, Riot 1, H1 1.25, H3 3.25, H5
1.25, W3 1.5, H2 11, H4 11), Could 36 (W1 14, the escape's eras and the bloom 1, gravity flips 3, E1-E3 4 each, the lap 6),
Won't 11 (E4 9, Gemini Rock 2).

**If the M4 re-estimate asks for cuts** (R8.1: the tight Must of about 450 sessions is accepted, and R0.3's "cut next"
list is not applied now), these come first, in this order: merge H5's unmasking into H3's ending (Mr. Y unmasks in
Gamma's cockpit; about −2 here and −1 text), make W2 a single-arena Bass final (no pair bouts; −3), and reduce the
Opening to 3 tutorial screens (lanes 01-03, then Pi-kun; −2).

**Text** (R4.5, R8.4). **story's string counts are the single source** (story §10.4: about **400 Must strings** for the
whole game, R8.4), and they include every line these stages use (S03-S08, S17-S20, S25-S48 and §6.4's OPN-, RIO-,
H1-, H3-, H5-, W2- and W3- tables). Round 2's own estimate here (about 230) is withdrawn. Story's §10.4 trim list is the
reserve, not a plan (R8.4).

---

## 0. Rules shared by these stages

### 0.1 Ids, layouts, tileset slots

**Ids are tech's** (R1.2, tech §4.2; feasibility-2, consistency-2, scope-12). Round 1 put H1-W3 in the vanilla fortress
ids 8-15; that is withdrawn. The legacy ids `$08-$0F` stay vanilla (the regression movies, the `???` fight, the 1993
data rows), and every new stage reads the stage-attribute record (tech §4.4) with `CLASS` = SPECIAL, FORTRESS or
EXHIBITION. The meta index (`meta.md` §1.8) is unchanged.

| Stage | Id | Class | Base layout (vanilla, copied and remixed) | Screens / 32 | Tileset slot (tech §5.3) | Vanilla art kept | Music (art_audio's ids, R5.2) |
|---|---|---|---|---|---|---|---|
| Opening-lite | `$10` | SPECIAL | new | 12 + room (+ the lobby screen, Could) | **TS_STADIUM** (bank `$66` slot 0) | Mr. X 1's night skyline and moon (set `$9D`) behind the plaza | G00 GRAND PRIX MARCH (Must); boss `$0C` |
| HALFTIME RIOT | `$11` | SPECIAL | new, on the Opening's blocks | 15 + room | TS_STADIUM, NIGHT / BLACKOUT / FIRE palettes | the same skyline behind the roof | G04 BETA's stage entry (Must); the duel G04; RIOT remix Should |
| H1 ROCKMAN | `$16` | FORTRESS | **Wily 2** (19 screens) | 19 + room | H1, copy of `$2A:$89` (bank `$66` slot 1) | pink machine blocks, circuit walls, the twin F.BLAST plug, the walker room | `$09` (G08 tribute Should) |
| H3 ROCKMAN 3 | `$18` | FORTRESS | **Mr. X 3** (18 screens) | 19 + room | H3, copy of `$2F:$92` (bank `$67` slot 0) | red gear machinery, pistons, the warning-light thread | `$09` (G10 Should) |
| H5 ROCKMAN 5 | `$1A` | FORTRESS | **Mr. X 4** (25 screens) | 25 + room | H5, copy of `$2B:$80` (bank `$67` slot 1) | grey stone castle, crates and drones, the open pit branch | `$09` (G12 Should) |
| W2 BRACKET OF DOOM | `$1C` | FORTRESS, HUB | **Wily 3** (17 screens) | 19 + room | W2, copy of `$2A:$92` (bank `$68` slot 0) | the moat, the teleporter, **the hub and its rush tables** | `$0B`; refights `$0C`; the final G04 |
| W3 WILY MACHINE 6.5 | `$1D` | FORTRESS | **Wily 4** (7 screens) + escape | 13 + room | W3, copy of `$2B:$89` (bank `$68` slot 1); the escape uses it too | the capsule arrival, the dispenser routine, the **Wily Machine 6 art `$BE`** and its floor split | `$0B`, `$18`; escape FINAL LAP Should (fallback `$18`) |
| H2 (Should) | `$17` | FORTRESS | Wily 1 (24) | 24 + room | bank `$69` slot 0 | the castle approach, the blowers, the Power pocket | `$09` (G09) |
| H4 (Should) | `$19` | FORTRESS | Mr. X 2 (18) | 18 + room | bank `$69` slot 1 | machine panels, the falling bell row, the pod column | `$09` (G11) |
| W1 (Could) | `$1B` | FORTRESS | new | 19 + room | TS_LAB (bank `$6A` slot 0) | Wily 2/3 machinery | UPGRADE LAB (G14, Could) |
| E1-E3 (Could) | `$12-$14` | EXHIBITION | new | 2-3 each | TS_ARCADE (bank `$6A` slot 1) | none | G18-G20 |
| Victory lap (Could) | `$1E` | SPECIAL | new, on TS_STADIUM | 8 | TS_STADIUM | the credit cards `$71-$80` | G17 |

- **Layouts** live in tech's layout banks (R1.5); vanilla's fortress layouts `$26/$27` stay untouched for the legacy
  ids. Round 1's claim that moving the fortress layouts frees tileset pages is withdrawn (feasibility-17: layouts are
  not tileset pages).
- **The MUSEUM CHR third** (about 96 tiles: marble trim, velvet ropes and posts, plaque frames, glass cases, the wing
  doors with years) is one **CHR set** in tech's set table v2 (§7.6), swapped into `$0A00-$0FFF` by a screen exit
  exactly as vanilla's `$91/$95/$98` sets are, and shared by every wing. [new-art] M, Must.
- Free tile ids per base (`rm6/fortress.md` §1-§8): Mr. X 2 references 157 of 256 tiles, Wily 4 101-199, Wily 3 71-123,
  Wily 2 141-157, so H1, W2 and W3 have room; Mr. X 3 (255) is full, so H3 drops the Metonger Z tank's blocks and tiles
  (Gamma takes that budget).

### 0.2 What a main route may require

`systems.md` §2.4 is the rule: **a normal exit never needs a form, an alt fire, a synergy, Break Man, or any Should or
Could item.** The fortress has exactly the two ruled exceptions (R2.11, design-3, consistency-12):

1. **The Magnet Beam, from H1 on.** It is handed over on H1's main path at 03, before the only gap that needs it (0B),
   which every route passes (CX lesson 6; Rockman 1 could not be finished without it).
2. **POWER, owned from the 2nd win, at Gamma MK-VI's phase 2 (SC5).** Its tell is the plaque at H3 10, and H3 adds a
   **no-risk fist-ride practice beat** on that screen (§4.3.4). The Super Adaptor is not lent. Under 1993 RULES (Could)
   SC5 stays on and Power is reached through the pause menu's vanilla transform (systems §4.6).

Beyond those: the buster's full charge (the Opening's high striker teaches it) and the slide. Every punch, form, alt,
synergy, weapon and Break Man gate is on optional content. The Exhibitions (Could) lend their vehicle as tech's
free-flight vehicle state, which is not a form (systems §2.4, consistency-36).

### 0.3 Structure, checkpoints, saves, maps

- **Two mid-stage checkpoints plus the boss shutter** in every H and W stage (vanilla had one, Wily 4 none): the
  vanilla `LDA #s / JMP $8416` script routine [engine-ok]. CASUAL adds one more per section (§0.10). Multi-phase finals
  get **phase checkpoints** (§5.3.2).
- **Saves** after every stage (`meta.md` autosave 4); GP saves fortress progress, vanilla never did.
- **The fortress maps** are `meta.md`'s screens (the Hall of Fame floor plan and the Castle picture replace vanilla's
  Mr. X map and Wily Fortress picture; vanilla's path animation `$39:$ACD4-$ADFE` kept), with `NEXT WING` / `REPLAY` /
  `BACK TO BRACKET`. This doc only places the doors: in v1.0 the H2 and H4 doors read `CLOSED FOR RENOVATION` and the
  tour goes H1 → H3 → H5; on the Castle map W1 is drawn closed too, and the route is W2 → W3 (meta's closed wings).
- **RETIRE** is allowed everywhere except the Opening (`meta.md` §3.7).
- **Break Man's call** exists only with the tag partner (Should). This doc fills `NO_TAG` (tech's 32-bit screen mask,
  R1.14) for v1.1: the whole Opening, W2's Championship Ring, the escape, every set-piece sheet, the Exhibitions' vehicle
  screens and W1's POCKET rooms. In v1.0 the masks are 0 and unread.

### 0.4 Secrets in non-venue stages

`meta.md` §1.6 lets the stage owner define SECRETS b0-b4 for non-venue stages. This doc uses one layout everywhere, so
the debrief and the scorecard treat these stages like venues:

| Bit | Meaning | Weight (systems §6.2) | Reward |
|---|---|---|---|
| b0 | **the stage's showpiece secret** (a mastery or homage act) | 3 | 30 prize bolts, paid once |
| b1 | **hidden room**: exactly one screen, off any route, with a visible tell | 2 | a sponsor envelope (30, systems §7), plus a 1-UP, a tank or a large energy, and a gag |
| b2 | **behaviour-gated prize** | 2 | a fixed item (a tank, a friend, the card), plus 30 prize bolts where the table says so. **Never a chip** (the v1.0 chips are systems' 14) |
| b3 | H5 only: **Mr. X's business card** (rating T14) | 1 | RATEFLAGS b1 |
| b4 | the envelope taken | - | - |

- **Prize bolts ≤ 60 per stage** (R2.7, consistency-19): at most 30 on b0 and 30 on b2, paid once per save when the bit
  is first set. They count in systems §7's prize row; meta needs **no PRIZES bits** for them because SECRETS b0/b2
  already record them (§9.3).
- **No secret exits here** (BRIEF §5.4): b0 takes the exit's weight (3) in SECRETS and in the debrief order.
- **At most one "collect N" secret per stage** (R3.1, design-5), counted by `meta.md`'s stage counter and shown by
  tech's HUD widget (R1.10, scope-16): Opening b2 (8 high fives), Riot b2 (the auditions), H1 b0 (24 balls), H5 b0 (8
  letters). Every other secret is a single act.
- **Hidden-room keys vary** (R3.1, design-5): a slide gap (Opening), F.BLAST on a charred crate (H1), an M.BEAM stair
  (H3), six knocks (H5), the Super fist's homing return (W3). The two TAG rooms (the Riot, W2) are **full-charge doors**
  in v1.0, as R4.2 rules; the partner opens them too when he ships.
- **Hints** (R4.5): tier B (an instruction) is Must and is written per secret below as a draft for story; tier A (the
  riddle) is Should and is kept in round 1's text (`build/revise/fortress/fortress_round1.md`) for story to restore.
  Nothing ships as WIP text.
- **Tokens** (systems §6.7): on replays a taken envelope or prize item spawns as a judge's pin.

### 0.5 Voice: commentators, heckles, Break Man

- **story.md owns every word** (R4.1). This doc gives each moment a **hook id**, its trigger, its R4.5 tier and a short
  intent. Hook ids: `OPN-nn`, `RIO-nn`, `H1-nn`, `H3-nn`, `H5-nn`, `W2-nn`, `W3-nn`, `END-nn` (H2/H4/W1/E1-E3 use
  `H2-`, `H4-`, `W1-`, `E1-`… when they return), plus story's **`WK-WM` and `WK-WC`**, W3's two first-weakness lines
  (§5.4.1).
- **Secret lines** (R8.6, story's budget call): each stage's **b0 line and every tell are Must**; the **b1 and b2 lines
  are Should**, and in v1.0 story's generic secret lines play for them (story §6.2, §6.4).
- **Deaths**: 4 death lines per stage in v1.0 (R4.5), in story §6.4's tables; this doc lists 4 recommended drafts per
  v1.0 stage. In H1-W3, story's rule applies (consistency-25, its decision 26): **one P1 heckle per respawn replaces the
  death line**, from story §6.5's Mr. Y table (H wings) and Wily table (W stages); round 1's per-wing heckle drafts are
  offered as wing-tagged variants (Should).
- **The YES/NO heckle is the 1-bolt respawn insurance** (R4.3, systems §7): round 1's fake "MR. Y PERFORMANCE
  PARTNERS" commercial is withdrawn.
- **Break Man's disguise is respected** (R4.2, R8.5, design-2). Nobody calls him Blues: only Rock says "Blues?" (twice:
  first at the Riot's 0E reveal, S20, then at S40), and Light says the name once, in S42. Every round-1 "OBVIOUSLY Blues"
  line is deleted. His name is first spoken in-stage at the Riot's 0E reveal, as his answer to Rock's "Blues?"; in the
  Opening he is the masked entrant 10 and **S06 speaks no name** (R8.5).
- **The Wily gag plays once per act, with varied wording** (R4.4, R3.9): once in the Opening, once at the trophy theft
  (S25), once at the unmasking (S33, "WE KNOW"). **The Mr. Y / Mr. Z alias gag is used once in the whole ending, at the
  arrest** (S41, R8.5).
- **Entrant numbering is story's** (R4.3, consistency-29): champions 1-8, Rockman 9, Break Man 10, Bass "entrant β".

### 0.6 Vanilla fortress tech, reused with one twist each (CX lesson 5)

| Vanilla tech (`rm6/fortress.md`) | Where it was | GP stage (tier) | The twist |
|---|---|---|---|
| BG boss in NT1 positioned by X and Y scroll above a floor split (chain 7 → tech's `RL_FLOOR`) | Mr. X 2 pod column | Opening: **Grand Pi-kun** (Must) | A balloon: the body bounces every shot; only the valve, open while it deflates, takes damage. **One size** (R3.6); the three sizes are Should (§1.6) |
| BG boss in NT1, horizontal scroll, floor strip (`RL_FLOOR`) | Wily 2 walker | H1: **Yellow Devil MK-VI** (Must) | The body **comes apart** through tech's F-PIECES on the map-edit service; pieces knocked down become floor blocks |
| Static BG boss in NT0 (no split), one hit box, the body reflects | Wily 1 Mechazaurus | H3: **Gamma MK-VI** (Must) | **Head and fists only** (R2.11); the rocket fists are sprite platforms that rise to the cockpit: you ride Gamma's own fist and punch it |
| The Robot Master framework: intro `$93`, controller `$94`, the typed panel `$3C:$81B1` | the 8 RMs | H5: **Dark Man MK-VI** (Must) | **The boss panel lies**, then re-types itself (tech §11.2's re-type) |
| Data-driven rush: hub, alcoves, `$39:$8EC8/$8ED2/$8EDC`, the ninth teleporter | Wily 3 | W2: **Bracket of Doom** (Must) | **Pair bouts** through tech's fight loader into each champion's own arena |
| Wily Machine: BG in NT1, a scrolled floor strip (chain `$19`), three bars in one room | Wily 4 | W3: **WILY MACHINE 6.5** (Must) | The floor strip becomes an **8-band perspective floor** (tech's `RL_FLOOR8`) that shears and drags Rock: "MODE 7!" |
| Sprite Capsule with palette-fade teleports | Wily 4 | W3: **Wily Capsule SUPER** (Must) | **Afterimage decoys**; and Break Man's gift (4MI's Wily Buster pattern) |
| The dome dispenser `$39:$861B`, reused by vanilla Wily 4 at 03 | Tomahawk, Wily 4 | W3: **the Trophy Dispenser** (Must); H3: **Kamegoro Maker** (Must) | W3: the stolen GP Cup is bolted on, and falls intact. H3: Rockman 3's turtle machine, whose bar also falls when its turtles die |
| The Mr. X reveal: pod, typed speech, flight path (`$39:$8DE9/$8E04`) | after Mr. X 4 | after H5: **Mr. Y's unmasking** (Must) | Two masks: Y comes off to show X, X comes off to show Wily |
| The credits: each RM fights in its own room, then its card strip | the ending | the v1.0 credits (Must) | The reworked champions fight in their GP rooms; the roll gains GP text and keeps the 1993 staff |
| BG tank + sprite pilot (chain `$1A`) | Mr. X 3 Metonger Z | W1: **METALL 16** (Could) | The BG body upgrades its era between bars |
| BG boss floating over a multi-split (chain `$16`) | Mr. X 4 X Crusher | H2: **Mecha Dragon MK-VI** (Should) | The floor is Heat Man's appearing blocks |
| BG in NT1 with vertical scroll (`RL_FLOOR`) | Mr. X 2 | H4: **Cossack Catcher MK-VI** (Should) | A crane cabin on a rail with a claw that grabs Rock (tech's attach state) |

Kept vanilla quirks (BRIEF §6, rm6 lesson 8): Wily 2's twin F.BLAST plug (one blast opens both) in H1; the falling
bell row in H4 (Should); the Mr. X 1 skyline; Wily 4's scripted capsule arrival; the Wily Machine's silver-tomahawk
weakness and the Capsule's C.FLASH resist; vanilla's newspaper `$95/$96`; `TO BE CONTINUED`.

### 0.7 Objects and engine pieces this doc uses

New objects are sub-ids of tech's families (tech §7.2): `$F4` enemies, `$F5` set pieces, `$F6` pickups, `$F7` NPCs and
events, `$F8` boss controllers, `$F9` boss parts, `$FA` enemy shots, `$FD` effects. **Every new object states its
freeze class** (`FRZ_KIND`, R2.2, tech §7.7): **STD** (an enemy written with the `DMGSTEP` macro: frozen by the Ice
Block, still takes hits), **BOSS** (the boss-side frozen state), **NOFREEZE** (BG bosses, big parts, hazards, platforms,
NPCs), **CUSTOM** (its own handler). In v1.0 the only freeze is the Ice Block (systems §3.4); Time Stop is Should.

| Piece | What | Used in | Owner, tier |
|---|---|---|---|
| **F-PLAQUE** (`$F7`) | A museum plaque: UP with B not held (R2.10) opens a full-screen page (9 × 28, text v1b) | H1, H3, H5, the W2 hub | this doc, [new-code] S, Must |
| **F-CASE** (`$F6`) | A glass case holding a pickup; touching it shatters the glass. The M.BEAM case plays the weapon-get screen (chain `$17`) | H1 03 | this doc, [new-code] S, Must; NOFREEZE |
| **F-PIECES** | The BG body that comes apart: a piece that flies off is a `map_set` to empty plus a sprite; a piece that lands is a `map_set` to a piece block | Yellow Devil (H1); Picopico-kun (H2, Should) | **tech §5.6**, Must (M7) |
| **Clock, counters, letter row** | Round 1's F-CLOCK, H1's SCORE and ball count, the Riot's audition count, H5's letters | §1, §2, §4.1, §4.5, §5.4 | **tech's HUD widget module** (§7.13), Must; this doc gives the widget records |
| **Timed blocks, beams, ladders** | Appearing blocks, crumbling ladders and other timed BG cells | H1 04, the escape 0A, H2 (Should) | **tech's map-edit service** (`alt_flip`, `map_set`), Must |
| **NPC Break Man** (`$F7`) | About 10 frames composited from Rock's sheet (visor, scarf, palette) | Opening S06 (masked), Riot, H5, W3, the ending | **tech §7.9** object, art's composite; Must (R4.2) |
| **Platforms that carry Rock** | the Opening's floats, H5's Super Arrow, H3's practice fist and Gamma's fists | §1, §4.3, §4.5 | the vanilla lift contact (`$38:$8F96`, class 2/5/9); tech's attach state only where a pose changes (H4's claw, Should) |
| ~~F-GRID~~ | round 1's cell grid | — | **deleted** (R1.10, scope-10); the Exhibitions use the map-edit service |
| F-SIZES | stream 2-4 pre-drawn sizes of a BG boss | Pi-kun's sizes, W3's approach (Should); METALL 16 (Could) | **tech**, Should (R3.6) |
| F-ERA | the POCKET / NES / SUPER eras | W1, the escape's eras | **tech**, Could (R1.3) |

### 0.8 Lag (R1.8)

**The rule** (tech §15.1, feasibility-4): count **every occupied slot**: the player, the screen script (slot `$16`),
directors, shots, utilities (M.BEAM beams), effect objects, the text runner (slot `$15`, only while a pop-up is up, and
it waits when the screen is at the cap). **The cap is 9** until M3 measures the OAM-builder gain. A screen at the cap
holds the player, the script, 3 shots and **4 more**. Round 1 counted "3 shots + enemies" and wrote caps of 8-10; every
cap below is recounted by this rule, and the tables show it as **[n]**. Boss rooms follow `venues_b.md`'s rule: the
boss (1) + boss-side objects ≤ 3. Directors and set-piece controllers fold into the screen script where they can. Two
recurring fixes:

- **One object, custom hit test**: a BG boss's body, valve, chin or cockpit is one controller with a position-tested hit
  box (as venues_a's Plant Man ring), not several reflecting part objects. Pi-kun, Gamma, Dark Man's barrier and
  WILY MACHINE 6.5 use it.
- **Projectile throttles**: a thrower waits while its previous shot is alive (the Riot's cans, Gamma's head cannon,
  the Capsule's rings).

Vanilla screens kept as they are (H5's crate halls, W2's moat) keep vanilla's object lists; tech's lag suite measures
them, and fails a stage whose lag rises by more than 2 points.

### 0.9 Flashes (R3.5)

Every large-area flash goes through tech's palette-flash service (§8.5): at most **3 per second** in the default mode,
and an 8-frame **fade** under REDUCED. The health notice at boot is `meta.md`'s. This doc's effects:

| Effect | Where | Default | REDUCED |
|---|---|---|---|
| Pi-kun's "16-BIT EDITION" palette | Opening 0A pinch | one palette change (no strobe) | fade |
| BLACKOUT: emergency lights dark 60 f / lit 30 f | Riot 04 | 0.7 changes per second; the dark phase is a palette blackout | 8-f fades |
| Floodlights 120 f on / 60 f off, with a 20-f **dim and buzz** tell (round 1's 20-f flicker is withdrawn) | Riot 08 | ≤ 1 change per second | fades |
| The BASS BLASTER breaking on the shield | Riot 0D | one white flash | fade to white and back |
| Help capsule, gift orb, weapon-get | Riot, W3, H1 | one flash each | fade |
| Yellow Devil and Gamma explosions, the Super dock | H1, H3 | sprite explosions, no screen flash | — |
| The machine's mortar blasts | W3 06 | sprite blast, no screen flash | — |
| **16-BIT BLAST**: a row brightens for 40 f, then the beam | W3 Capsule pinch | a steady **glow** in a raster band (round 1's 40-f row flash is withdrawn) | the same |
| TIME! at 0:00.0 | escape | one red flash, then death | red fade |
| The castle pixelating | ending | palette steps 8 f apart (no strobe) | the same |

### 0.10 CASUAL (R2.9)

Every stage fills in **systems §13.4's standard lever list**: reflex windows ×2, mash counts −40 % (hold-to-struggle
allowed), set-piece timers +50 %, +1 checkpoint per section, skill-gated secrets relaxed by one step. Each stage section
has a table in systems' format (Lever / Where / NORMAL / CASUAL / How); "none" is a valid row. Mechanisms are tech's
(§5.5): `TIERVAL`, `MASH n`, `IFCASUAL` and the dormant checkpoint object woken by a CASUAL poke. Round 1's one-off
CASUAL ideas (the POCKET slide, the H1 mid-gap ledge, the 6-press grab) are re-expressed as rows of these tables.

### 0.11 Raster bands (R1.9)

Tech's buffer holds 24 bands per frame; the pop-up window costs 2 (`RL_WINDOW`), the flush band 1 when no window is open.
Every scene below fits; the busiest are listed:

| Scene | Bands | Total with a window |
|---|---|---|
| Pi-kun (Opening 0A) | `RL_FLOOR` 1 | 3 |
| Riot blackout screens (04, 08) | lighting service: 1 PPUMASK band + the bottom `RL_PALBAND` when the fuse box is lit | 4 |
| Yellow Devil (H1 0F) | `RL_FLOOR` 1 | 3 |
| W2 moat and hub (SUPER colour) | `RL_PARALLAX` 2 + `RL_PALBAND` 1 | 5 |
| WILY MACHINE 6.5 (W3 06) | `RL_FLOOR8` 8 + the machine's NT1 split 1 | 11 (consistency-27 resolved) |
| Capsule's 16-BIT BLAST | `RL_PALBAND`-style glow band 1 + the beam band 1 | 4 |
| Should/Could: W3's 16-band approach | `RL_FLOOR16` 16 + split 1 | 19 |
| Could: E3's lobby cellophane | none: BG attribute palettes (feasibility-15c) | 2 |

### 0.12 Music cues (R5.2; art_audio owns the list)

Must: G00 (the Opening), G04 BETA (the Riot's stage and both duels), the 2-second whistle jingle (the NPC Break Man),
the ending's **lights-out arrangement** (2A03 stems; MMC5 stems Could; consistency-13 names it G37 LAST MATCH) and the
D9 mute mask. Everything else uses vanilla ids in v1.0: `$09` in the H wings (the tributes G08-G12 are Should,
consistency decision 24), `$0B` and `$18` in W2/W3, `$18` for the escape (FINAL LAP is Should), `$0C` for the
refights. **W2, W3 and the escape keep every 2A03 channel** (R8.3): the channel drop belongs to LIGHTS OUT alone.
Round 1's "HALL OF FAME theme in 5 arrangements" is withdrawn for art's G08-G12.

---

## 1. OPENING CEREMONY: Opening-lite (`$10`, meta 0) · Must · M5

**Pitch.** The Grand Prix opens at the GP Stadium. NEW GAME goes straight to the players' tunnel (R4.4); the stage is
the opening ceremony: a warm-up course whose lane judges teach the scorecard, a parade of the eight champions, and the
mascot, Grand Pi-kun, sabotaged by Mr. Y's "upgrade". It is the CX opening lesson applied to a tutorial: the stage
teaches by being the event.

**What it teaches, in order:** walk and jump (01), the slide (02), the charge shot (03 and the boss), ladders and the up
exit (04), the pop-up window (00), four scorecard rows (the lane judges) and the fifth (the scoreboard, 05), hidden rooms
and their tells (02, 04), a behaviour prize (the parade), a boss bar and a weak point (Pi-kun). The player owns the
buster only: no form, no weapon, no RETIRE, no Break Man call.

### 1.1 Text budget and staging (R4.4, design-4)

- **One intro.** Story's S02 is the attract crawl (Should with meta's crawl); round 1's 55-second in-game intro is
  withdrawn, and its X→Y repainted Mr. X picture moves to S02's panel 5.
- **At most 15 scene pages**, the rules folded into the lane judges, the roll call reduced to the float lines, the Wily
  gag played once:

| Beat | Screen | Story scene | Pages | Engine at M5 |
|---|---|---|---|---|
| READY in the tunnel | 00 | S03 | 2 | pop-up sequence under a script lock |
| Roll on the radio; Eddie's shut stall | 00 | S04 | 2 POPs | pop-up (Roll's face icon; no Roll sprite) |
| Each lane judge announces his row | 01-04 | OPN-02…05 | 4 POPs | pop-up |
| The scoreboard: the four cards, VARIETY, medals and bolts (S07 folded) | 05 | S07 | 1 | pop-up sequence under a lock |
| The float lines (one per champion) | 07-08 | S05 → float lines | 8 POPs | pop-up |
| Entrants 10 and β | 08 | S06 | 3 | pop-up sequence under a lock |
| The sabotage and the one Wily gag | 09 | S08 (first half) | 3 | pop-up sequence under a lock |
| Pi-kun's defeat and the bracket reveal | 0B | S08 (second half) | 2 | pop-up, then the bracket's window |

  Scene pages: 2 + 1 + 3 + 3 + 2 = **11** (the 14 POP lines are one line each). The Opening lands at M5, before text
  v1b, so every scene runs as a **pop-up sequence** (2 × 28 pages, auto-advancing, A to hurry) while the screen script
  holds Rock in his stand pose; when v1b lands (M6), story may move S03, S06 and S08 into the 4 × 28 window.
- **Break Man's charge tip** (story S08) plays **only after a first death to Pi-kun** (design-2): his whistle, then one
  POP. The high striker teaches the charge first.

### 1.2 Tileset and art

| Item | Content | Tags |
|---|---|---|
| Slot **TS_STADIUM** | bank `$66` slot 0 (tech §5.3); shared by the Riot, the lap (Could) and the GP Rush lobby screen (Could) | [new-art] L, Must |
| Kept | Mr. X 1's night city: the blue skyline and the moon (set `$9D`) behind the plaza | [engine-ok] |
| New BG | the tunnel, turnstiles, bleachers with two-frame crowd tiles (a CHR swap every 16 f), the pitch, the running track, the scoreboard (a 6×3-block panel; digits and words are metatiles written by `map_set`), the press box, floodlight towers, Eddie's stall, Pi-kun's body (one pose, about 60 tiles, in NT1) | [new-art] L, Must |
| New sprites | Pi-kun's valve, puffs, confetti and the pump hose; the high striker's puck and bell; the lane judge (16×24) with card digits; training targets; beach balls; the float deck (48×16); a white glove (the raised hand) | [new-art] M, Must |
| **SET-PARADE** | the eight champions' vanilla idle frames, about 12 tiles each, packed into one 96-tile enemy-area set: a composite of vanilla art (R5.1, counted R). Reused at the ending's podium, a pair at a time (§6.1, R8.6) | [new-art] S, Must |
| Other sprites | **Eddie** (peeking from his stall) is **new art**, a composite (R8.6: he is not in vanilla RM6; art_audio's cast); the NPC Break Man composite (tech §7.9, masked palette); Bass β (§2.1) for S06 | Eddie [new-art] S (art_audio's), Must |

### 1.3 Screen by screen

| GP | The player does | Enemies [n] | Set pieces | Tags |
|---|---|---|---|---|
| **00** | **THE PLAYERS' TUNNEL.** READY; S03. Roll on the radio (S04): Rush's adaptors come later. Eddie's stall has its shutter down: `PIT STOP OPENS AFTER THE CEREMONY` (the shop opens at 0 wins, after the Opening: systems §8, consistency decision 14). Walk right into the light | none [2] | | [engine-ok] + text, Must |
| **01** | **LANE 1: JUMP** (steeplechase): three hurdles, the **water jump** (a 48-px pool of floor type 8: falling in only slows you, gravity `$00.18`), two 32-px gaps. The **DAMAGE judge** at the lane's end: 10 minus 3 per splash or fall (OPN-02) | 2 training targets (HP 1, harmless; STD) [8] | the judge object (family `$F7`) | [new-code] S, Must |
| **02** | **LANE 2: SLIDE** (limbo): four 24-px bars under a LIMBO timer (a HUD DIGITS widget). The **TIME judge**: 10 if all four are cleared before the timer (OPN-03). **Hidden-room tell**: after the last bar, a 16-px gap at the foot of the right wall, under `STAFF ONLY - PI-KUN`: slide in (exit to 1C) | none [3] | | [engine-ok] + widget data, Must |
| **03** | **LANE 3: CHARGE**: the **HIGH STRIKER** (`TEST YOUR BUSTER!`, `HOLD B`). The pad reads the shot's attack byte: `$11` sends the puck a quarter up, `$12` half, **`$13` (the full charge) rings the bell** (DING, confetti), and the bell opens the gate to 04. The **STYLE judge**: 10 if the first full charge rings it (OPN-04). The only required tool in the stage; a full charge always opens the gate | none [1 + 1 + 3 + puck + judge + confetti = 8] | puck object (`$F5`, NOFREEZE) | [new-code] S, Must |
| **04** | **LANE 4: STANDS**: up the bleachers by four ladders; the up exit (vanilla type 2) into the upper stand. Beach balls bounce down the steps (contact 1, a "boing"). The **SECRETS judge** at the top: a **10 if the dressing room (1C) was found this run**, else a `?` card and OPN-05 ("the judges know every hidden room"). It teaches SECRETS live | ≤ 3 beach balls (NOFREEZE) [9] | crowd tiles cheer | [new-code] S, Must |
| **05** | **THE UPPER STAND**: the press box (Cossack and Kalinka in the window, BG) and the **scoreboard**: the four cards summed (`WARM-UP 34/40`), then one page for the fifth judge (VARIETY), the medals and the bolts. **The entrant board** (BG text, story's numbering, R4.3): `1 BLIZZARD … 8 YAMATO / 9 ROCKMAN (DR. LIGHT) / 10 ?????? (MASKED) / β BASS (SPONSOR: MR. Y)`. **Checkpoint 1** | none [2] | `map_set` writes the sums | [new-art] S, Must |
| **06** | Down the players' ramp onto the track: the parade is coming | none [2] | | Must |
| **07** | **THE PARADE** (§1.4): floats 1-4 roll toward Rock; each champion's line; the high fives. CASUAL checkpoint | float + sparkle [7] | | [new-code] M, Must |
| **08** | The parade's second half, over the **fountain moat** (a pit): floats 5-8 roll right and are the only bridge; ride one across. At the far bank the parade ends with **S06**: the last float carries **entrant 10**, the NPC Break Man composite in a dimmed masked palette, whistle first, **no name spoken** (R4.2); then entrant β's late entry: Bass β drops in, shakes the screen and dashes off | float + sparkle [7]; under S06's lock: 2 NPCs [4] | | Must |
| **09** | **CENTRE STAGE**: Grand Pi-kun dances on the pitch; Mr. Y waves from his skybox. **The sabotage** (S08's first half, ≈ 6 s, controls locked): Mr. Y presses `UPGRADE!`; Pi-kun's eyes turn red; the scoreboard reads `PI-KUN 16-BIT EDITION`; **the Opening's one Wily gag** (story's words, R4.4). The shutter to 0A. **Shutter checkpoint** | Pi-kun's valve sprite [3] | the chairman's speech is cut (R4.4) | [new-code] S, Must |
| **0A** | **Boss: GRAND PI-KUN** (§1.6). The pitch; the track is the floor strip | | | Must |
| **0B** | The walk-out: S08's defeat lines, the first scorecard (`meta.md` §4.0), then the bracket and S08's reveal | none | | Must |
| **1C** | **Hidden room: PI-KUN'S DRESSING ROOM** (§1.5) | none | | Must |
| **1D** | (Could) the GP Rush lobby screen, entered by warp (tech §4.2, `meta.md` §9.2.2) | | | Could |

Checkpoints: 05 and the shutter (09); CASUAL adds 07. Screens: 00-0B, 1C (13), plus 1D when GP Rush ships.

### 1.4 The parade and CROWD FAVOURITE

- **Eight floats** in story's numbering (1 Blizzard … 8 Yamato). Each is one object (family `$F5` sub FLOAT, NOFREEZE):
  a 48×16 deck (6 sprites wide) with the champion's idle frame from SET-PARADE standing on it. **One float on screen
  at a time**: the deck's rows then hold 6 sprites + Rock's 2, the NES limit of 8, and the screen needs only two sprite
  palettes (deck and champion). Round 1's "2 floats per screen, each with its own boss set" could not fit the 96-tile
  enemy area.
- **07**: floats 1-4 roll left at 1.25 px/f toward Rock (about 3.4 s across). **08**: floats 5-8 roll right at
  1.0 px/f over the moat; Rock rides one across.
- **Platforms**: the deck uses the vanilla lift contact (`$38:$8F96`).
- **Lines**: as Rock reaches each float, its champion speaks once (POP; story's float lines, R4.4).
- **CROWD FAVOURITE (b2)**: each champion holds a white glove up for 90 f as his float passes Rock (a sparkle). Jump into
  it: **HIGH FIVE!** (a clap; the crowd roars). The count is `meta.md`'s stage counter, shown by an ICONROW widget (8
  glove icons, 2 rows of 4). Eight in one run → the scoreboard types `CROWD FAVOURITE` (no flash, §0.9; OPN-08).
  Reward: 30 prize bolts; the lap's name-calling cameo waits for the lap (Could).

### 1.5 Secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **PERFECT WARM-UP** | 40/40 on the four lane cards in one run: no splash or fall in lane 1, the limbo timer beaten, the bell rung by the first full charge, and the dressing room found before lane 4 | the cards are shown live and summed at 05 | 30 | `GET A 10 FROM ALL FOUR LANE JUDGES. THE LAST ONE WANTS TO KNOW ABOUT THE ROOM BEHIND THE LIMBO.` |
| b1 | **PI-KUN'S DRESSING ROOM** (1C) | slide into the gap after lane 2 | the gap, the `STAFF ONLY - PI-KUN` sign, and the SECRETS judge's `?` card | envelope + 1-UP | `SLIDE UNDER THE WALL AFTER THE LAST LIMBO BAR.` |
| b2 | **CROWD FAVOURITE** | eight high fives in one run | raised gloves, sparkles, the glove row | 30 | `JUMP INTO EVERY CHAMPION'S RAISED GLOVE DURING THE PARADE.` |

**1C, the dressing room**: a mirror with bulbs, three spare Pi-kun heads on stands (one winks), a rack of costumes with a
**Mr. Y costume** on a hanger (OPN-07), **the first sponsor envelope** (+30) and a 1-UP. Exit: the door back to 02. It
sets the pattern every later hidden room follows: one screen, a tell visible from the route, a joke, an envelope.
(Systems' income model left the Opening-lite without an envelope; this one adds 30, §9.2.)

### 1.6 Boss: GRAND PI-KUN, "16-BIT EDITION" (fight `$26`, GP_BOSSHIT row 8) · one size

**What it is.** The GP mascot: an inflatable robot chick in a GP sash, **80 px tall, one size** (R3.6, scope-14). Mr.
Y's "upgrade chip" makes it rampage. It is the game's first boss, so it is a lesson: **the body is a balloon that
bounces your shots; only the valve takes damage, and only while it is open.** A pre-charged shot is the efficient
answer, which is what lane 3 taught.

**How it is built.** The Mr. X 2 pod technique: the body is BG in NT1, positioned by the frame's X and Y scroll above the
split, and the pitch below comes from NT0 (tech's `RL_FLOOR`, vanilla chain 7, handler `$3E:$C23A`). One pose needs no
`bgboss.py` streams: the body is authored as nametable art in the level pipeline, so the Opening does not wait for M7.
**One controller object** (family `$F8`, FRZ BOSS) owns the body and a position-tested hit box: a shot that touches the
body outside the open valve is reflected (class 3, `BOING`); a shot on the open valve latches. [new-code] M, [new-art] M,
Must.

**Stats.** HP **14** (systems row 8: buster 1/30, charge 3/30; on replays the mid-boss default column serves the other
sources). Contact 3; shockwave 2; confetti 1.

| Id | Pattern | Timeline (frames) | Slots |
|---|---|---|---|
| A | **BOUNCE** | 3 bounces toward Rock, 48 f each, peak 64 px (Y scroll). Each landing sends **one shockwave each way** along the floor (8 px tall, 2 px/f, contact 2). Shots bounce off | [8] |
| B | **PFFFT** | f0-20: a hiss and puffs from the valve (the tell); f20-170: it zooms around the room like a released balloon on a scripted Lissajous loop at 2 px/f, never lower than 40 px above the floor at Rock's x. **The valve is open and hittable from f20 to f170.** One full charge lands 3; taps land 1, 30 f apart | [6] |
| C | **REFILL** | it lands; Mr. Y's skybox lowers a pump hose (one object); the body sags and swells back (Y scroll, 16 px) over 40 f. Shooting the hose cancels the refill for 60 f, and the valve stays open: a reward for attention | [7] |
| D | **CONFETTI** (HP ≤ 9) | during B, the sash cannons fire 2 confetti bursts (slow arcs that drift down, contact 1) | [8] |
| | Cycle | A, B, C (≈ 400 f). The valve faces Rock's side during B | |
| Pinch | **16-BIT EDITION** (HP ≤ 5) | one palette change to a garish "SUPER" palette (the foreshadowing of Project SUPER; no strobe, §0.9); A becomes 4 bounces; B loops at 3 px/f for 110 f | |

**Defeat.** The valve pops off; Pi-kun flies around the stadium like a released balloon (a 3-s scripted flight) and
lands as a flat heap on the pitch. Mr. Y's skybox blinds slam shut. Then 0B.

**Teaching.** It never needs anything but the buster. A player who learned lane 3 kills it in 5 openings (a full charge
per opening); a tap-only player needs about 3 cycles more.

**Panel**: NAME `GRAND PI-KUN` (12 cells, story §5.1's limit); story §5.3 writes the record.

**Should (v1.1, R3.6): the three sizes.** Round 1's design (S 48, M 80, L 128 px streamed by F-SIZES; it inflates
during C and flies the PFFFT loop small), about 150 tiles; it returns with F-SIZES (tech, Should).

### 1.7 Hooks (story's words; R4.5 tiers)

| Id | Trigger | Tier | Intent |
|---|---|---|---|
| OPN-01 | READY at 00 | Must (S03) | Light: this year it is a real tournament |
| OPN-02…05 | each lane card | Must | the judge announces his row (DAMAGE, TIME, STYLE, SECRETS) and the score |
| OPN-06 | first splash | Should | the water jump is only knee-deep |
| OPN-07 | entering 1C | Should | why is there a Mr. Y costume in here? |
| OPN-08 | the eighth high five | Should (b2's line; story's generic line plays in v1.0, R8.6) | CROWD FAVOURITE |
| OPN-09 | first high five | Should | up top! |
| OPN-10 | reaching the entrant board | Should | entrant ten is... masked |
| OPN-11 | first valve hit | Must (the boss's first-weakness line) | hit the valve! |
| OPN-12 | 1C found | Should (b1's line; generic in v1.0, R8.6) | the judges saw that |
| OPN-13 | PERFECT WARM-UP | Must (b0's secret line) | four tens |

Deaths (4, story §6.4; drafts): *"It's only a warm-up!"* / *"He got bounced."* / *"Charge it, Rock. CHARGE it."* /
*"Pop goes the entrant."*

### 1.8 CASUAL levers (systems §13.4)

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | none | — | — | — |
| mash | none | — | — | — |
| timer | 02, the LIMBO timer | 6.0 s | 9.0 s | `TIERVAL` |
| checkpoint | 06-09 | 05, 09 | + 07 | dormant checkpoint, CASUAL poke |
| secret step | b2 CROWD FAVOURITE | 8 high fives | 7 | `IFCASUAL` in the predicate |

### 1.9 HARD (Should, v1.1; tech §5.5's format, counted in systems' HARD line)

| Section | Entry | Kind |
|---|---|---|
| 01 | the water jump becomes a pit (water → air blocks); one more 32-px gap | LAYOUT pokes |
| 04 | beach balls fall 1.5× faster | `TIERVAL` |
| Pi-kun | HP 20; pinch at HP 8; A = 4 bounces, shockwaves 3 px/f; B's open window 120 f | `IFHARD` branch + `TIERVAL` |

### 1.10 Homage moments (the screenshot list)

1. Ringing the high striker's bell with a full charge.
2. The entrant board: `10 ?????? (MASKED)` and `β BASS`.
3. High-fiving Knight Man on his float over the fountain moat.
4. Mr. Y's `UPGRADE!` button, and the scoreboard reading `PI-KUN 16-BIT EDITION`.
5. A balloon chick zipping around the stadium with its valve open.

---

## 2. HALFTIME RIOT (`$11`, meta 9) · Must · M6

**Pitch.** After the 4th win, Bass β riots the bracket (`meta.md` §3.5: the POSTPONED stamps). The **HALFTIME RIOT**
(R4.3, design-14: it falls at the bracket's halfway point) is that riot, played: the GP Stadium at night, in a blackout,
overrun by **the rejects**, the losing entries of the fan design contest that Mr. Y hired (R4.3: the crowd is the
rejects, because they are mechanics). You chase Bass through the concourse, the service tunnels, the stands and up the
scoreboard to the roof, where he fights you with copies of the champions' weapons. When he loses he refuses to, and
**Break Man** steps in front of his last shot; on the roof Rock asks "Blues?", he answers with his name, and the
Committee's Rule 9 lines play.

The player owns 4 weapons, Power (from the 2nd win) and Jet (from the 4th). The main route needs none of them.

### 2.1 Tileset and art

| Item | Content | Tags |
|---|---|---|
| Slot | **TS_STADIUM** with three palette programs: NIGHT (lit); BLACKOUT (dark blue, only emissive tiles bright), driven by tech's lighting service (§8.5); FIRE, a 3-step palette cycle on the fire tiles only (Flame's oil format, `$3B:$9143`; a small area, not a flash) | data, Must |
| New BG | service tunnels (pipes, cable trays, emergency lights), rubble, the scoreboard scaffold and the jumbotron (a 6×4-block panel whose face is written by `map_set`), the roof gantry, two fuse boxes and the master breaker, the emblem door | [new-art] M, Must |
| Kept | Mr. X 1's night city and moon (set `$9D`) behind the roof | [engine-ok] |
| New sprites | VENDING MAN and CHEER MAN (16×24, ≤ 8 frames each, recolours and composites of vanilla RM6 enemies, R5.1); the ACCEPTED stamp; the can; the BASS BLASTER (2 pre-drawn sizes) | [new-art] S, Must |
| Bass β | **composited from Rock's sheet** (fins, the β, crash-test markers, palette; R4.2, R5.1), with his **4 copied weapons pre-drawn in his own 96-tile set** (R3.6) | [new-art] M, Must |
| NPC Break Man | tech §7.9's family `$F7` composite (about 10 frames from Rock's sheet: visor, scarf, palette); also the Opening, H5, W3 and the ending | [new-art] S, Must |
| UMBRELLA MAN | (Should) | [new-art] S, Should |

### 2.2 The rejects

The vanilla bosses came from a fan design contest (the credit cards DWNB-41..48 name the winners). Mr. Y hired the
losers. Each wears a `REJECTED` tag, and each gimmick is a mechanic (CX lesson 2). Family `$F4`, FRZ STD (written with
`DMGSTEP`).

| Enemy | Tier | HP | Behaviour | Contact / shot | Why it was rejected (hook) | Tags |
|---|---|---|---|---|---|---|
| **VENDING MAN** | Must | 6 | Stands; lobs a can every 90 f (an arc, 2 px/f), **but never while a can, a capsule or a walk-off is already live on the screen** (the §0.8 throttle). His lit front glows in the dark (an emissive palette entry), so in a blackout he is the room's only light | 2 / can 2 | "excessive product placement" | [new-code] S |
| **CHEER MAN** | Must | 2 | Hops in place with pom-poms. **While he lives, every other reject on the screen moves and throws 1.5× faster** (`GO! FIGHT! WIN!` sparkles over them). Kill him first | 1 | "only helps other robots" | [new-code] S |
| **UMBRELLA MAN** | Should | 3 | Drops in from the stands under an umbrella that is **a parachute, not a shield** (R3.1: Knight alone owns the shield): a shot on the canopy pops it, he drops fast and lands stunned for 60 f. On foot he walks at 0.5 px/f | 2 | "the umbrella was the whole robot" | [new-code] S |

**The audition rule** (Must). A reject killed by a **full-power blow**, which is LATCHSRC's FULL flag (systems §4.7: the
full charge, PUNCH★, the Super fist from H3 on), does not explode: a gold `ACCEPTED!` stamp, a wave, and he walks off.
It counts as a kill for scoring. An accepted Vending Man leaves a small capsule where he stood and beams out instead of
walking, so the slot count does not rise. This is b2's mechanic (§2.5). [new-code] S.

### 2.3 Screen by screen

| GP | Palette | The player does | Rejects [n] | Set pieces | Tags |
|---|---|---|---|---|---|
| **00** | NIGHT | READY at the main gate; trash-can fires; the scoreboard types `HALFTIME: ROCKMAN VS ?????`. S17 (story rewrites it for the rejects, R4.3) | none [2] | | Must |
| **01** | FIRE | The concourse | Vending 1, Cheer 1 [8] | overturned food carts as cover | Must |
| **02** | FIRE | Concourse 2 | Vending 2 [8] | | Must |
| **03** | NIGHT | The ticket hall. **Bass sighting** (90 f, controls live): Bass dashes along the upper rail and blasts the floor (RIO-03); the floor crumbles under Rock (the crumbling collision `$1D`, chosen by the stage record's `COLL_GROUP`, tech §4.3) into 04. It is the down exit; it cannot be avoided and cannot hurt | Bass (NPC) [3] | | data on tech's record + [new-code] S (the script), Must |
| **04** | BLACKOUT | A service tunnel: the emergency lights are dark 60 f, lit 30 f (tech's lighting service; **the game's one lights-on-a-timer set piece**, R3.1). The pulse is the tell: walk on the lit beats. **Fuse box A**: any shot flips it, and this screen stays lit. C.FLASH lights the room for 240 f (systems' tap tweak) | Vending 1, whose front lights the room [7] | | [new-code] S, Must |
| **05** | NIGHT | Tunnel 2: a burst water main floods the floor (floor type 8, gravity `$00.18`): floatier jumps over two 48-px pits | Cheer 1, Vending 1 [8] | | [engine-ok], Must |
| **06** | NIGHT | **Break Man's help** (§2.6): rubble seals the tunnel and the rejects pour out of the stands behind. **Checkpoint 1**. The **emblem door** on the left wall (→ 1D) | 2 crowd rejects + the NPC under a lock [5] | | [new-code] S, Must |
| **07** | NIGHT | Ladders up into the stands | Cheer 1 on a ledge [6] | | Must |
| **08** | BLACKOUT | The stands: the floodlights are on 120 f, off 60 f, with a 20-f **dim and buzz** before they go (the tell; §0.9). **Fuse box B** lights this screen for good | Vending 2 [8] | | [new-code] S, Must |
| **09** | NIGHT | Upper stands: **the cheer rally**. The 1.5× buff makes this the stage's hardest screen; the Cheer stands highest | Cheer 1, Vending 2 [9] | | Must |
| **0A** | NIGHT | Up the scoreboard scaffold (ladders); the jumbotron shows Bass's face and types taunts (story). **The master breaker** (b0) on a ledge reached by a 40-px jump from a ladder top | none [2] | | Must |
| **0B** | NIGHT | The jumbotron top. **Checkpoint 2** | Vending 1 [7] | | Must |
| **0C** | NIGHT | The roof gantry: a 16-px catwalk over the stands. Shutter. *v1.1: a gust zone (VA-GUST, Should with `venues_a.md`)* | Cheer 1 [6] | | Must (the gust Should) |
| **0D** | NIGHT, or LIT after b0 | **Boss: BASS β** (§2.4). The roof: a flat floor and two 48-px gantry ledges at 64 px | | | Must |
| **0E** | | **The reveal and Rule 9** (§2.6), then the walk-out and the scorecard | | | Must |
| **1D** | | **Hidden room: THE LOCKER ROOM** (§2.5) | | | Must |

Placed rejects: **15** (Vending 10, Cheer 5), plus the two scripted crowd rejects at 06, which do not count. Checkpoints:
06, 0B and the shutter (0C); CASUAL adds 03 and 09. Screens: 00-0E and 1D (16).

### 2.4 Boss: BASS β, duel 1 (fight `$21`, GP_BOSSHIT row 9)

**Who he is.** Mr. Y's entrant β, "built from Rockman's own tournament data", so he fights with the data: **he copies the
champions' weapons**. Prototype look: Rock's frame in unpainted panels with yellow-black crash-test markers and the
`β` on his chest.

**How he is built.** A family `$F8` boss controller entered through vanilla's intro (`$93`, the panel by fight id, tech
§11.2). His copies are enemy shots (family `$FA`) drawn from **his own boss set**: only the **4 weapons pre-drawn** in
his 96-tile enemy-area set (R3.6, scope-13; this answers systems' open question 3): **B.ATTACK, F.BLAST, KNIGHT.C and
SILVER.T**, four distinct silhouettes and dodges (Y.SPEAR would read as a buster shot, PLANT.B as a shield, C.FLASH as a
screen flash). FRZ BOSS. [new-code] M, [new-art] M (a composite), Must.

**Stats.** HP 28. Contact 4. No weakness (a rival, not a puzzle): systems row 9 (buster 1/40, charge 3/40, weapons
2/24, PUNCH★ 3/30), **plus SC6's adaptive armour**: the 3rd consecutive damaging hit from one column makes that column
1/45 until another column hits; a hex shimmer with that weapon's icon shows it (RIO-07).

| Copy (enemy tap) | What Bass fires | Damage to Rock | Live objects |
|---|---|---|---|
| B.ATTACK | 3 flakes in a spread (round 1: 4) | 2 each | 3 |
| F.BLAST | a fireball that leaves a floor pillar for 60 f | 3 | 2 |
| KNIGHT.C | a mace thrown out and back | 3 | 1 |
| SILVER.T | an arcing tomahawk | 3 | 1 |

**Which copies.** In duel 1 he uses the weapons among his four that the player owns. **If the player owns none of the
four, COPY fizzles**: `NO DATA` pops over his head (RIO-08) and he fires a 3-way buster spread instead.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **SCOUT** | f0-24: dash toward Rock at 2.5 px/f (contact 4); f24-36: 3 buster shots aimed at Rock, 6 f apart (2 damage, 3 px/f); f36-66: recovery |
| B | **DOUBLE-JUMP VOLLEY** | f0: jump (vy −5.2); at the apex a second jump (vy −4.0); at the second apex a 3-way volley down and forward (45°, 67°, 90°); land; 20 f |
| C | **COPY** | f0-30: the **ANALYZING** pose (visor scan lines; the copied weapon's icon floats over his head: the tell), his palette turns that weapon's colours; f30 and f70: the copy; f70-90: recovery. Never the same copy twice in a row |
| D | **WALL KICK** (HP ≤ 18) | he dashes into a gantry ledge and kicks off it (CX Quick Man's wall kick, credited) into a dive at Rock's x (contact 4); 70 f |
| | Cycle | A, B, A, C, then D when unlocked (≈ 400 f) |

**Slots**: Bass + at most 3 live shots (SCOUT's 3, the volley's 3, the flakes' 3) = **[9]**. Every pattern waits while 3
of his shots are alive.

**Pinch (HP ≤ 9): "β LIMITER OFF".** His outline cycles yellow and black (his sprite only); the dash is 3.0 px/f; SCOUT
fires 5 shots with at most 3 alive; COPY picks **the weapon you have hit him with most this fight**, among his four
("learning"; otherwise at random); every recovery is 25 % shorter.

**COUNTER (Should, SC10).** When Bass fires a copy, the same weapon from Rock cancels it in mid-air, and Rock's next hit
with that weapon within 60 f is a `COUNTER!`: 3/16, outside SC6. It returns with systems' Should list.

**The finish: β OVERDRIVE** (scripted, ≈ 9 s, Must). At 0 HP Bass does not explode. He drops to one knee, rises, the
music cuts to a drone (D9 leaves only the triangle), he floats up and charges a giant **BASS BLASTER** (a sphere growing
over 120 f). Controls stay live, but there is nowhere to hide. At f100 **Break Man's whistle** plays (the Must jingle),
the NPC Break Man beams down in front of Rock and raises his shield; the blast breaks on it (one white flash; REDUCED: a
fade) and Bass is thrown to the roof's edge. Bass asks who he is supposed to be; Break Man answers only "Entrant number
ten." Bass's exit line (story S19), and he teleports. Rock takes no damage in the scene. [8]

**The 4MI touch** (Must). If Rock's HP falls below 6 during the pinch, Break Man's whistle sounds once off-screen and a
large life capsule drops from the top of the screen (once per fight; it waits while Bass has 3 shots alive). A purist who
never drops below 6 never sees it. **Winning without it is rating T1, SOLO RIOT** (R4.2's partner-free test, R8.5;
systems §9.5): Bass β's death sets meta's **RATEFLAGS b4 SOLO RIOT** when the capsule never dropped in that run (round
2's "NO-CAPSULE" bit is that bit). The capsule beat stays Must, since T1 reads it.

**Records.** `BASS_ADAPT` (the column used most) is saved for duel 2 (SC6). **RIVAL** (RATEFLAGS b2, rating T13): no
damage taken from the bar fill to the overdrive.

**Panel**: NAME `BASS β`, story §5.3's record (entrant β).

### 2.5 Secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **LIGHTS FOR THE MAIN EVENT** | Shoot the **master breaker** on 0A, on a ledge that is a 40-px jump from a ladder top, in the dark. The floodlights come back for the rest of the stage: the crowd tiles cheer, and the roof duel is fought under the lights (0D's LIT palette) | the big red lever with a lightning sticker, visible from the ladder; fuse boxes A and B taught the lever | 30 | `ON THE SCOREBOARD SCAFFOLD, JUMP FROM THE TOP OF A LADDER TO THE BIG RED BREAKER AND SHOOT IT.` |
| b1 | **THE LOCKER ROOM** (1D) | The emblem door at 06 opens to **a full charge** (v1.0, R4.2). With the partner (Should), his Break Shot opens it too | the door carries his scarf emblem, is shown during the help beat, and hums while Rock is charged near it | envelope + E-tank | `THE EMBLEM DOOR IN THE TUNNEL OPENS FOR A FULLY CHARGED SHOT.` |
| b2 | **TALENT SCOUT** | **9 of the 15 placed rejects ACCEPTED** in one run; the counter `AUDITIONS 1/9` appears with the first stamp (a DIGITS + LABEL widget on `meta.md`'s stage counter) | the first ACCEPTED stamp and its hook (RIO-04) | 30 | `KNOCK OUT 9 REJECTED ENTRANTS WITH A FULL CHARGE OR A FULL PUNCH. THEY WALK AWAY HAPPY.` |

Round 1's six-fuse-box FLOODLIGHTS was a second "collect N" in one stage; b0 is now a single act (R3.1), and the two fuse
boxes stay as per-screen conveniences.

**1D, the locker room**: eleven lockers with name plates in story's numbering: 1-8 the champions (Wind Man's is full of
leaves, Knight Man's has a can of polish), **9 ROCKMAN** (a spare helmet), **10 ??????** (a spare yellow scarf), and a
dented one marked **β** (`KEEP OUT`). The sponsor envelope (+30) and an E-tank.

**TALENT SCOUT's reward**: 30 prize bolts, and the accepted rejects sit on W2's losers' benches (§5.2.4).

### 2.6 Break Man: help, block, reveal and Rule 9 (NPC, Must; the partner Should)

| Beat | Where | What happens | Story |
|---|---|---|---|
| **The help** | 06 | Rubble seals the tunnel; the rejects pour out of the stands behind Rock. Whistle; the NPC Break Man drops in, fires one Break Shot (an effect object) and the rubble (a cracked `$B` block) breaks. He turns to the crowd, shield up, and stays as Rock goes on. The emblem door shows his scarf emblem | **S18**, merged here with round 1's help beat (Must at this spot) |
| **The block** | 0D | the β OVERDRIVE shield block (§2.4) | S19 |
| **The reveal and Rule 9** | 0E | Bass is gone; Break Man stands at the roof's edge. Kalinka asks who that is; **Rock's first "Blues?"** (S20, R8.5), and he answers **"Break Man."**: the first time the name is spoken (R4.2). Nobody else says Blues. Then **S20's Rule 9 pages 1-2 play in place** (R4.2): the Committee rules that a sponsor's interference invokes Rule 9, and the other four matches resume. He leaves over the roof's edge | S20 pages 1-2 (Must); pages 3-6 (he joins, the CALL row, the banner) are **Should** with the partner and play at this spot. They set FORMS.TAG and EVENTS b5 (`meta.md`) |

In v1.0 nothing sets FORMS.TAG; meta's EVENTS b3 (the stamps peel off) still plays on the next bracket visit. Round
1's *"That's OBVIOUSLY Blues"* and its `BREAK MAN JOINS!` banner are deleted (R4.2, design-2).

### 2.7 Hooks (story's words; R4.5 tiers)

| Id | Trigger | Tier | Intent |
|---|---|---|---|
| RIO-01 | the first reject | Must | these are rejected contest entries; who paid them? |
| RIO-02 | the first Cheer buff | Should | he is cheering for the wrong team |
| RIO-03 | the Bass sighting | Must | Bass is wrecking the ticket hall |
| RIO-04 | the first ACCEPTED | Must (secret tell) | a full-power audition; rules are rules |
| RIO-05 | a fuse box; the master breaker | Must (b0's line) | lights! |
| RIO-06 | Bass's first copy | Must (the duel's teaching line) | that is YOUR weapon; he copied it |
| RIO-07 | SC6 adapts | Must (systems) | he's adapting |
| RIO-08 | NO DATA | Should | he has no data on you |
| RIO-09 | β OVERDRIVE | Must (S19) | he is still going |

Deaths (4; drafts): *"Rejected!"* / *"The crowd didn't see that. The lights were off."* / *"Bass is copying his falls
now too."* / *"That's a halftime exit."*

### 2.8 CASUAL levers (systems §13.4)

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | none | — | — | — |
| mash | none | — | — | — |
| timer | 04 and 08, the lit phases | 30 f / 120 f | 45 f / 180 f | `TIERVAL` |
| checkpoint | 00-05 and 06-0B | 06, 0B | + 03, + 09 | dormant checkpoints |
| secret step | b2 TALENT SCOUT | 9 of 15 | 7 of 15 | `IFCASUAL` in the predicate |
| secret step | b0, the breaker's ledge | a 40-px jump | a 16-px step block under the ledge | CASUAL layout poke |

### 2.9 HARD (Should, v1.1)

| Section | Entry | Kind |
|---|---|---|
| 01-02, 08-09 | the Cheer buff 2× instead of 1.5× | `TIERVAL` |
| 04, 08 | the dark phase 90 f instead of 60 | `TIERVAL` |
| Bass β | pinch at HP 14; D from the start; the help capsule never drops | `IFHARD` branches |
| 0C (with the v1.1 gust) | gust 0.75 px/f | `TIERVAL` |

### 2.10 Homage moments

1. Bass β throwing **your** Knight Crusher back at you, his palette turned Knight-Man green.
2. Break Man's whistle, and his shield breaking the BASS BLASTER.
3. A Vending Man taking a full charge and walking off with an `ACCEPTED!` stamp, leaving a can of energy.
4. `NO DATA` over Bass's head.
5. The 1993 night skyline behind the roof duel, under the floodlights you switched back on.

---

## 3. EXHIBITIONS E1-E3 (`$12-$14`, meta 10-12) · Could (v1.1+); E4 (`$15`) · Won't (v1)

**What they are** (R3.7, scope-9). Optional bonus matches, each lit on the bracket by a pair of venue secret exits
(`meta.md` §3.1: **E1 Wind + Knight, E2 Tomahawk + Plant, E3 Blizzard + Flame, E4 Yamato + Centaur**). When they
return, each is **one lobby plus one "rule boss" arena**: the guest is an "arcade legend" robot with a parody name, and
**his rule is a real mechanic from his game** (CX lesson 2). Round 1's three lesson screens and high-score corridor per
guest are cut; the arena's first phase teaches the rule. They are built on **tech's map-edit service and T6** (the well,
the bricks, the bunkers are layout cells written by `map_set`), not on a separate grid engine (F-GRID is deleted, R1.10,
scope-10). **E4 Maze is Won't (v1)**: its top-down MAZE mode is a new player-control model (scope-17), and four ghost
palettes do not fit two enemy sprite palettes (feasibility-20).

### 3.0 Rules shared by the exhibitions

- **Layout**: 00 the lobby (the guest's cabinet, his intro card, the commentators), 01 the arena, 1E a backroom only
  where the guest's own game supplies the trick (R3.8, design-20: round 1's identical OUT OF ORDER cabinet in all four is
  withdrawn). Par 90 s (systems §6.3).
- **Tileset**: TS_ARCADE (bank `$6A` slot 1, tech §5.3): an arcade hall (cabinets, carpet, a change machine, neon) plus
  one CHR third per guest. Simple tiles on purpose.
- **The rule does the damage**: a guest takes **4 with 12 i-frames** from his rule event through systems' **RULE column**
  (consistency-18 and its decision 19: a RULE source in GP_BOSSHIT, 4/12 with the WEAK bit on the guest rows, booked as
  class 4 for VARIETY). Weapons chip 1/32. HP 28. The stage record's `OWNED` override sets what the rule allows (Could).
- **Vehicles**: E3 seats Rock in CANNON mode, tech's free-flight vehicle state with the **lane** flag; a lent vehicle is
  not a form (systems §2.4). NO_TAG.
- **Reward** (first clear): 100 bolts (systems §7) + an exclusive RACING COLOUR (systems §8, Could) + a trophy drawn on
  the bracket badge (the Museum is Won't). No chip.
- **Secrets**: b0 the game's mastery act; b1 the backroom through the game's own trick, or none; b2 a clean-play act.
- **Text** (R3.3): the commentators cannot say the trademarks (the running gag, e.g. *"FALLING-BLOCK-FOUR-LINE-
  CLEAR!"*); the plaques describe the games and never name them ("a falling-block puzzle born in Moscow, 1984"); no
  third-party character names (round 1's ghost-name death line is deleted). Rule and folklore facts go through story's
  Appendix A.

### 3.1 E1 BLOCK MAN: "FALLING BLOCKS" (fight `$18`)

**The rule.** Tetrominoes fall into a well. **Rock moves them with his buster**: a tap on a piece's side pushes it one
column, a full charge **rotates** it 90°, and jumping into it from below bonks it up one row (once per piece). Landed
pieces are solid floor; completed rows clear, and the rows above drop 16 px (Rock with them).

| Mechanic | Numbers |
|---|---|
| Well | 10 × 13 cells of 16×16 (x 48-207), layout cells written by `map_set`; camera locked |
| Falling piece | one object drawing its 4 cells; 1 row per 32 f in phase 1, 24 f in the fight, 16 f in the pinch; the NEXT panel is BG |
| Ghost piece | a dotted outline of BG cells where the piece will land: the crush tell |
| Lock, clear | lock 16 f after touching down; a full row glows 20 f (no flash) and clears over 3 frames inside the repaint queue's budget |
| Crush, top out | a piece locking onto Rock: 4 damage, Rock pushed up onto it; a cell in row 0: Rock takes 8 and the well empties (no instant death) |

**The arena.** Phase 1 (the lesson): Block Man sits on the well's rim while three plain pieces fall, one per verb
(PUSH, ROTATE, CLEAR banners). Then he plays. **Block Man** is four 16×16 blocks that rearrange into the seven
tetrominoes; he flies to the top and **drops as one of the falling pieces**, and Rock can push and rotate him like any
other. A cleared row containing one of his blocks deals 4 per row (the RULE cell).

| Id | Pattern | Timeline |
|---|---|---|
| A | **DROP** | f0-30: flies to the top, picks a shape (a 7-bag), shows his face in NEXT; falls 1 row per 24 f; locks for 60 f (solid); then pulls his blocks out (a Block-Man-shaped hole) and flies up |
| B | **NEXT PIECE** | a plain piece falls between his drops |
| C | **GARBAGE** (every 3rd drop) | a grey row with one gap rises from the bottom; the stack lifts 16 px |
| D | **HARD DROP** (HP ≤ 12) | his ghost appears at Rock's column for 20 f, then he slams down in 4 f (crush 4) |
| Pinch (HP ≤ 8) | **LEVEL UP** | 16 f per row; GARBAGE every 2nd drop |

FOUR LINES with him inside = 16. Slots: Block Man + 1 piece = [7]. A flat I piece is 8 sprites on a line: it flickers
beside Rock (priority to Rock). Defeat: his four blocks fall into the well, complete a row and clear in a final glow.

| Secret | How | Tier B hint (draft) |
|---|---|---|
| b0 **FOUR LINES** | clear 4 rows at once | `ROTATE THE LONG PIECE UPRIGHT AND DROP IT IN A FOUR-ROW GAP.` |
| b1 | none (no trick of the game's own fits a backroom) | — |
| b2 **CLEAN STACK** | beat Block Man with no crush and no top-out | `BEAT BLOCK MAN WITHOUT BEING CRUSHED OR TOPPING OUT. THE DOTTED OUTLINE SHOWS WHERE PIECES LAND.` |

### 3.2 E2 PADDLE MAN: "BRICK BREAKER" (fight `$19`)

**The rule.** A ball bounces around and breaks bricks. **Rock is the paddle**: a buster shot that hits the ball knocks it
upward, angled by where it hits (5 zones, ±60°/±40°/±20°), and the ball bounces off his helmet the same way. **The ball
never hurts Rock; it hurts the floor**: a ball reaching the floor cracks its brick, a second hit opens a hole. SMASH (a
full charge or PUNCH★): red, pierces 3 bricks for 120 f. Capsules from capsule bricks: W wide, S slow, M multi (2
balls), L laser, R repair. Bricks and floor bricks are layout cells.

**The arena.** Paddle Man sits at the top centre inside a **brick shell** (3 layers, 8 bricks wide) and slides his paddle
along the ceiling, returning the ball at Rock; a ball through a hole that reaches his core does 4 (RULE). Phase 1: the
shell is closed and the floor is solid while Rock learns to deflect.

| Id | Pattern | Timeline |
|---|---|---|
| A | **RALLY** | his paddle returns the ball toward Rock's x ±24 px |
| B | **SPIN SERVE** (every 3rd return) | a curving ball (vx changes by ±0.05 px/f²); a spin sparkle is the tell |
| C | **REBUILD** (every 600 f, one ball only) | a brick-layer drone (HP 2) re-lays 4 shell bricks; shoot it to stop it |
| D | **MULTIBALL** (HP ≤ 12) | the paddle splits the ball into 2 (round 1: 3, over the cap); the floor erodes faster |
| E | **PADDLE BEAM** (HP ≤ 12) | the paddle stops over Rock and glows 30 f, then fires a beam straight down (3 damage) |
| Pinch (HP ≤ 8) | | ball cap 4.0 px/f; REBUILD every 400 f |

Slots: Paddle Man + paddle + 2 balls = [9]; the drone and capsules appear only while one ball is live.

| Secret | How | Tier B hint (draft) |
|---|---|---|
| b0 **RALLY 30** | keep one ball up for 30 deflections in a row (a counter widget from 10) | `KEEP ONE BALL UP FOR 30 HITS IN A ROW. HEADERS COUNT.` |
| b1 **THE BACKROOM** (1E) | the arena's back wall is a giant stone head (a parody of a famous final face) with a bricked-up mouth of silver bricks: only the ball breaks them, and the mouth is a door: the genre's own secret warp | `BREAK THE STONE HEAD'S MOUTH WITH THE BALL. IT IS A DOOR.` |
| b2 **PERFECT FLOOR** | beat Paddle Man with no floor brick broken | `BEAT PADDLE MAN WITHOUT THE BALL EVER BREAKING A FLOOR BRICK.` |

1E: a cabinet with a rotary knob labelled `ANALOG. VERY ADVANCED.`; plaque `IN 1976 THE CONTROLLER WAS A KNOB. IN 1993 WE
HAD A D-PAD. PROGRESS.`; a 1-UP and a W-tank (Should).

### 3.3 E3 INVADER MAN: "INVASION 1978" (fight `$1A`)

**The rule.** A formation steps side to side and down; **the fewer are left, the faster it steps** (one step every N
frames, N = invaders alive: the original's famous accident). **Rock is the cannon**: CANNON mode on the vehicle state's
lane, 1.25 px/f, B fires straight up at 4 px/f, **one shot on screen** (the cabinet card: `ARCADE RULES: ONE SHOT`).
Bunkers (3 wear states per tile, `map_set`) erode from both sides. A UFO crosses the top every 25 s. An invader reaching
the lane: Rock takes 10 and the wave restarts.

- The formation is BG moved by the scroll above a split (the Mr. X 4 floating-BG technique, `RL_MULTI`); its hit map is a
  40-bit WRAM mask offset by the scroll. The bottom band (bunkers, lane) is unscrolled.
- The lobby cabinet's coloured cellophane (green band at the bottom, red at the top) is BG attribute palettes, not
  raster swaps (feasibility-15c).

**The arena.** Phase 1 is a 3×6 wave without bunkers; then **Invader Man**, a crab-shaped commander (32×24, BG, part of
the top row), leads a full formation. He can only be hit through **a clear column**, and he keeps closing it.

| Id | Pattern | Timeline |
|---|---|---|
| A | **MARCH** | the formation steps by the rule and drops bombs (≤ 2: a zigzag and an aimed one) |
| B | **REINFORCE** (every 15 s) | invaders beam into up to 6 empty cells, the column under him first (a 40-f twinkle per cell) |
| C | **MOTHERSHIP DIVE** (HP ≤ 12) | he detaches and dives at the lane in a zigzag (3 px/f, contact 3), then flies back |
| D | **DEATH RAY** (HP ≤ 12) | a 24-px beam straight down at Rock's x after a 30-f glow; it erases the bunker cells it crosses |
| Pinch (HP ≤ 8) | | minimum step 2 f; REINFORCE every 10 s |

Slots: the commander's hit box, 2 bombs, the shot, the UFO, 1 explosion, the director in the script = [8]. Defeat: the
formation freezes and drops one row per frame like a curtain.

| Secret | How | Tier B hint (draft) |
|---|---|---|
| b0 **BUNKER HOLD** | finish phase 1's wave with all bunkers at least half intact | `GOOD COVER IS WORTH MORE THAN GOOD AIM. DON'T SHOOT THROUGH YOUR OWN BUNKERS.` |
| b1 **THE 23RD SHOT** (1E) | hit the UFO with the 23rd shot of a wave (the cabinet card states the folklore: the 23rd shot, then every 15th, paid best); it drops a coin, and the coin opens the coin door beside the lobby cabinet | `COUNT YOUR SHOTS. HIT THE UFO WITH THE 23RD AND TAKE ITS COIN TO THE LOBBY.` |
| b2 **NO INVASION** | beat Invader Man without an invasion | `BEAT INVADER MAN BEFORE ANY INVADER REACHES THE BOTTOM.` |

1E: an upright cabinet tipped on its side, its screen reading `INSERT 100 YEN`; plaque `THEY SAY THIS GAME CAUSED A COIN
SHORTAGE. THE BUSTER IS FREE.` (R3.9: worded as folklore).

### 3.4 E4 MAZE MAN: "MAZE MUNCHER 1980" (fight `$1B`) · Won't (v1)

Kept for the record: Rock flies a top-down Jet on an 8-px lattice through a single-screen maze, eating dots; four
Met-ghosts each chase a different target (Rock's cell; 4 cells ahead; the cell 2 ahead mirrored through the first ghost;
Rock's cell when far, else home), alternating SCATTER and CHASE; power pellets make them edible; Maze Man waits in the
pen and becomes edible too; his defeat is the famous right-half kill screen. Round 1's full specification is in the
scratch copy. Why Won't: a third player-control model (scope-17), four ghost palettes (feasibility-20), and the most
trademark-exposed guest.

### 3.5 CASUAL and HARD (when they return)

| Guest | Lever | NORMAL | CASUAL | How |
|---|---|---|---|---|
| E1 | timer: fall speed | 24 f per row | 36 f | `TIERVAL` |
| E1 | secret step: CLEAN STACK | no crush | ≤ 1 crush | `IFCASUAL` |
| E2 | timer: capsule durations | 15 s | 22 s | `TIERVAL` |
| E2 | secret step: RALLY | 30 | 20 | `IFCASUAL` |
| E3 | reflex: DEATH RAY's glow | 30 f | 60 f | `TIERVAL` |
| E3 | secret step: BUNKER HOLD | half intact | a quarter | `IFCASUAL` |
| all | checkpoint | the arena's door | + one at phase 2 | dormant checkpoint |

HARD (Should with them): E1 16 f per row from the start; E2 serve 2.5 px/f and 1-hit floor bricks; E3 the formation one
row lower and bombs 1.5× faster.

---

## 4. HALL OF FAME (`$16-$1A`, meta 14-18) · H1, H3, H5 Must (M7); H2, H4 Should

### 4.0 The museum

**The story beat** (story S25, EVENTS b4). At the 8th win, START on the lit trophy plays the theft: during the trophy
ceremony a **UFO-catcher crane** (the Cossack Catcher's claw, a first look at H4) lowers from a saucer with a Y painted
over its W, grabs the **GP CUP** and carries it off to an island museum, the **HALL OF FAME**. The claw (3 frames) is
**Must art** for this scene (art_audio §5.3, R8.6); H4's Cossack Catcher (Should) reuses it. The trophy theft is the
second act of the Wily gag (R4.4).

**The floor plan** (`meta.md`'s fortress map, story S26): a rotunda and five wing doors marked 1987, 1988, 1990, 1991,
1992, plus a sixth door, `1993 - UNDER CONSTRUCTION`, greyed out (§4.5.3). The wings are played **in order** (a museum
tour; consistency decision 40 keeps it linear), which also fixes when M.BEAM and Super arrive. **In v1.0 the 1988 and
1991 doors read `CLOSED FOR RENOVATION`**, and the tour is H1 → H3 → H5. Nothing in H3 or H5 depends on H2 or H4.

**Every wing has** (v1.0):

| Element | Rule |
|---|---|
| Plaques | F-PLAQUE full-screen pages (text v1b), 3-5 per wing, reading optional (story S27: Must for H1/H3/H5). Factual and short; folklore is worded as folklore; facts go through story's Appendix A. **Plaques describe and never name third-party games** (R3.3), and **say BLUES** for Rockman 3-5's mysterious robot (R3.9, design-23) |
| Remixed hazards | 2-3 signature hazards of that game, built on the base layout's own tech where possible |
| A display case | one exhibit you take: M.BEAM in H1, the Super Adaptor in H3; H5's "case" is the 1993 wing |
| The MK-VI boss | a legacy boss on a vanilla BG-boss technique with one twist (§0.6) |
| A mid-boss | H1 Big Eye, H3 Kamegoro Maker; H5 spends that budget on the unmasking |
| Secrets | b0 showpiece, b1 hidden room (a storeroom with a gag exhibit and an envelope), b2 behaviour prize (§0.4) |
| Heckles | story §6.5's Mr. Y table, one P1 line per respawn (§0.5); wing-tagged variants Should |
| *Tag pocket* | *Should (with the partner): an emblem shutter to a small reward* |

**MK-VI damage rows** are systems §4.5's (machines: buster 1/32, PUNCH★ 4/24; robots: the champion scale), cell for
cell; §8 lists them.

### 4.1 H1 ROCKMAN (1987) (`$16`), base vanilla Wily 2 · Must

**Pitch.** The first game's wing: appearing blocks, Elec Man's beams, Fire Man's pillars, the useless score counter, the
Magnet Beam you could not finish the game without, and the Yellow Devil. (Guts Man's tipping lifts are Should, §4.1.4.)

**Tileset.** H1 (bank `$66` slot 1) = a copy of Wily 2's tables (`$2A:$89`; 141-157 of 256 tiles used). Kept: the pink
machine blocks, the green circuit walls, the twin F.BLAST plug, the walker room's NT1 layout. New: the MUSEUM third, an
MM1 third (Elec beam emitters, fire vents, score balls, the Yellow Devil's pieces and eye ≈ 60 tiles through
`bgboss.py`), Big Eye's sprite set. [new-art] M, Must.

**The score.** In H1 only, a `SCORE` sits under the life bar (Rockman 1's): a HUD **DIGITS** widget of 4 digits plus a
fixed `00` **LABEL**, 6 sprites on one line (the widget module's limit; Rockman 1 showed 7 digits). Enemies drop **score
balls** (Rockman 1's bonus pellets) as well as their usual drops. The score does nothing, as it did in 1987 (a plaque
says so), except for b0. The ball count is `meta.md`'s stage counter, shown as an icon and 2 digits on a second row.
Data on tech's widgets + [new-code] S (the drop), Must.

| GP | From | The player does | Enemies [n] | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance hall: marble, velvet ropes; the wing plaque (the first game: a blue robot, six bosses and a score that counted nothing). READY | none [2] | vanilla's Power-block E-tank pocket kept | [engine-ok], Must |
| **01-02** | v01-v02 | Right through the "1987 gallery" | walkers `$12`, capped walkers `$1E`, each dropping a score ball [≤ 9] | score balls in awkward spots (b0) | [engine-ok], Must |
| **03** | v03 | **The Magnet Beam case** (F-CASE): `MAGNET BEAM (1987). HANDLE WITH CARE.` Touch: the glass shatters, **YOU GET MAGNET BEAM** (the weapon-get screen, chain `$17`; systems §3.10; `meta.md` WEAPONS `$031` b0, autosaved on pickup). **Checkpoint 1**. A plaque: in 1987, players who missed this beam could not finish the game; the museum put it on the main path | none [2] | | [new-code] S, Must |
| **04** | v04 | Up through the **appearing-block hall**: vanilla's 11 block positions over the spike floor, retimed to a 1987 rhythm, are now **BG cells switched by tech's `alt_flip`** in 4 phase groups (4 metatile ids, ≤ 8 cells each; a "pyoo" per switch). Vanilla's 11 `$8F` objects would not fit the cap; the cells cost no slot. The vanilla F.BLAST plug at the upper right leads to the branch 10-12 (one blast opens both plugs: the vanilla quirk, kept) | none [2] | | data on tech's map-edit service, Must |
| **05-06** | v05-v06 | The rider gallery over vanilla's pits. *v1.1: Guts Man's tipping lifts* (§4.1.4) | riders `$C6` throwing balls, 1 per screen [7] | | [engine-ok], Must |
| **07** | v07 | **Elec Man's beams**: three horizontal beams across a 48-px ladder shaft, each 60 f on, 90 f off, offset; the emitters spark 20 f before firing (the tell); 3 damage per touch. **One controller object** (family `$F5`, NOFREEZE) draws all three (a beam is 6 sprites on its line + Rock's 2) and runs their hit test | 1 rider [8] | | [new-code] S, Must |
| **08-09** | v08-v09 | Right, then down at 09; the E-tank at 09 (vanilla). *Tag pocket (Should): an emblem shutter at 08 → a closet with a large weapon energy* | 1 rider [7] | | [engine-ok], Must |
| **0A** | v0A | **Checkpoint 2** (vanilla's). The branch rejoins here | none | | Must |
| **0B** | v0B | **The Magnet Beam gap**: a **96-px** gap over a pit, under an anti-Jet field (floor type E blocks thrust) and the sign `NO RUSH JET: AUTHENTIC 1987 EXPERIENCE`. **Build one beam (64 px, systems §3.10) from the edge, walk it, and jump the last 32 px** (consistency-17: round 1's "walk across" did not add up). The sign's second line (story's) says so | none [2 + 1 beam] | the fortress's first required tool (§0.2), handed over at 03 | data + M.BEAM, Must |
| **0C** | v0C | **Fire Man's pillars**: floor vents glow 20 f (the tell), then a 16×64 flame column rises (30 f), holds (40 f) and drops; **at most 2 columns alive** (objects, NOFREEZE) | 1 rider [8] | | [new-code] S, Must |
| **0D** | v0D | **Mid-boss: BIG EYE MK-VI** (§4.1.1), the room locked by shutters | | | Must |
| **0E** | v0E | Shutter corridor; a plaque: the Yellow Devil's pieces never fly higher than 64 px, and a Magnet Beam built at the top of a jump is a fine place to watch from: **the boss's beam-shelf tell**. Shutter checkpoint | | | Must |
| **0F** | v0F | **Boss: YELLOW DEVIL MK-VI** (§4.1.2) | | | Must |
| **10-12** | v10-v12 | **Branch: THE ARCHIVE** (through the F.BLAST plug): dark corridors of old display cases; rejoins 0A, skipping 05-09. The hidden-room tell on 11 (b1). No score balls here | skeleton robots `$65` ×2 per screen [7] | | [engine-ok], Must |
| **13** | new | **Hidden room: THE BOX ART STOREROOM** | | | Must |

Checkpoints: 03, 0A and the shutter (0E); CASUAL adds 07. The M.BEAM case (03) is before the branch point (04), so every
route takes the beam before the gap (0B), and a death after 03 keeps it.

#### 4.1.1 Mid-boss: BIG EYE MK-VI (fight `$13`, mid-boss default row)

Rockman 1's hopping cyclops: a 32×48 sprite (≤ 8 frames, composited first from vanilla parts, R5.1), HP 20, contact 4,
family `$F8`, FRZ BOSS.

| Id | Pattern | Timeline |
|---|---|---|
| A | **LOW HOP** | a 24-px hop toward Rock, 24 f |
| B | **HIGH HOP** | crouch 12 f (the eye squints: the tell), an 80-px hop toward Rock, 56 f |
| | Landing | every landing shakes the screen (a scroll jitter); a grounded Rock within 64 px is **stunned 16 f** (a jump avoids it) |
| | Cycle | A or B at random, 2:1, with a 20-f pause between hops |
| Pinch (HP ≤ 7) | **MK-VI** | after each high hop the eye fires one aimed shot (3 px/f, 3 damage) |

Slide under a high hop. Slots: Big Eye + 1 shot = [7].

#### 4.1.2 Boss: YELLOW DEVIL MK-VI (fight `$1C`, row 10)

**What it is.** Rockman 1's famous boss: a yellow blob that crosses the room **piece by piece**, re-forms on the other
side, and opens a single eye. Weak to a beam (C.FLASH stands in for the Thunder Beam).

**How it is built.** Vanilla Wily 2's walker room: the boss body is BG in NT1 (layout blocks), the floor strip comes from
NT0 below the split (tech's `RL_FLOOR`). **The twist**: the body is a 3×4 grid of 16×16 pieces (48×64 px), and **tech's
F-PIECES** (on the map-edit service, M7) turns a piece into a flying sprite (`map_set` to empty plus a sprite) and paints
it back on the far side (`map_set` to a piece block). **One controller** (family `$F8`, NOFREEZE: a BG boss) owns the
eye sprite and a position-tested hit box: the eye takes damage, the body dinks. [new-code] M (the patterns; F-PIECES is
tech's), [new-art] M, Must.

**Lanes.** A piece flies at the height of its row: **lane 1** (0-16 px above the floor: jump it), **lane 2** (16-32:
slide under it, or jump high), **lane 3** (32-48: stand still, it passes over), **lane 4** (48-64: stand still). Nothing
flies above 64 px, so **an M.BEAM built at the top of a jump (its top near 72 px) is a safe shelf** (the 0E plaque is
the tell; two beams at most, 240 f each).

| Id | Pattern | Timeline (frames) | Slots |
|---|---|---|---|
| A | **CROSSING** | a piece leaves every 16 f, from an order table (two 12-entry tables alternate, e.g. `1 2 1 3 4 1 2 2 3 1 4 2`); each flies at 4 px/f (≈ 40 f across); **at most 3 in flight**; it re-forms piece by piece on the far side: ≈ 232 f | [9] |
| B | **EYE** | the eye opens for **120 f, +30 per missing piece** (cap +120); aimed lasers (3 px/f, 3 damage) at f30, f70 and f110 if still open; no piece flies during B | [8] |
| C | **BODY SLAM** (HP ≤ 18) | after B, the whole body hops 24 px toward Rock (NT1 Y scroll), 40 f; the landing stuns a grounded Rock within 64 px for 16 f | [6] |
| | Cycle | A, B, (C): ≈ 400-500 f | |

**The twist that changes the fight: knock the pieces down.** A flying piece hit by a full-power blow (LATCHSRC's FULL
flag: the full charge, PUNCH★, the Super fist on replays) or any hit of 3+ **drops to the floor** and lies there as a
solid 16×16 block (a `map_set`, no slot; at most 3). The body re-forms **with holes**, and each hole keeps the eye open
30 f longer. At the next crossing the floor pieces fly back first. Aggressive play buys longer windows and footholds;
dodging is slower but safe.

**Pinch (HP ≤ 9): MK-VI.** Pieces leave **two at a time** in two lanes (the order table always leaves a safe lane), at 5
px/f, still at most 3 in flight; three lasers per eye phase.

**Damage** (systems row 10, eye only): C.FLASH **4/12 W**, Y.SPEAR 3/16 G, PLANT.B 1/32 R, buster 1/32, charge 3/32,
PUNCH★ 4/24. SC7, the "SELECT trick", is Could (systems).

**Defeat.** The twelve pieces scatter, three sprites at a time, bounce and explode 4 f apart.

**Teaching.** It is the M.BEAM's first exam (the shelf), and the full charge's (knocking pieces down).

**Panel**: NAME `YELLOW DEVIL` (12), a year in LOCATION (story §5.4).

#### 4.1.3 Secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **THE SCORE COUNTS** | collect all **24 score balls** in one run (12 placed and 12 dropped by placed enemies, all on the main route) | the ball counter | 30 | `COLLECT ALL 24 SCORE BALLS ON THE MAIN ROUTE OF THE 1987 WING. EVERY ENEMY THERE DROPS ONE.` |
| b1 | **THE BOX ART STOREROOM** (13) | on branch screen 11, one crate in a stack is charred: an F.BLAST tap breaks it (`$D`) and a ladder leads down | the charred crate | envelope + 1-UP | `IN THE ARCHIVE BRANCH, BURN THE CHARRED CRATE WITH F.BLAST.` |
| b2 | **NEVER WHOLE** | from the second crossing on, the Yellow Devil never re-forms complete | the holes, and the first knock-down's hook (H1-06) | E-tank + 30 | `KNOCK DOWN AT LEAST ONE FLYING PIECE EVERY CROSSING WITH A FULL CHARGE OR A FULL PUNCH.` |

**13, the storeroom**: a crate stencilled `ROCKMAN (1987): OVERSEAS PACKAGING. DO NOT DISPLAY.` and a plaque, `SOME
EXHIBITS ARE KEPT IN STORAGE FOR EVERYONE'S SAFETY.` The envelope and a 1-UP. *Should: a figure of the stocky "box-art
robot" in yellow and blue, holding a pistol, beside the crate (new art).*

**Hooks** (story's words): H1-01 the M.BEAM case (Must: it is a weapon-get line); H1-02 the first score ball (Should);
H1-03 the gap sign (Should); H1-04 the Yellow Devil's bar fill and defeat (S28, Must); H1-05 the first C.FLASH hit on the
eye (the first-weakness line, Must); H1-06 the first piece knocked down (Must: b2's tell); H1-07 b0's secret line
(Must); H1-08 and H1-09, the b1 and b2 lines (Should: story's generic lines play in v1.0, R8.6). **Respawns**: story
§6.5's Mr. Y heckles; wing-tagged drafts (Should): *"My Yellow Devil was the hardest boss of
1987. Ask anyone."* / *"Score: zero. How very 1987."*

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | none | — | — | — |
| mash | none | — | — | — |
| timer | 04, a block's solid time; 07, the beams' off phase | 90 f; 90 f | 135 f; 135 f | `TIERVAL` |
| checkpoint | 03-0A | 03, 0A | + 07 | dormant checkpoint |
| secret step | b2 NEVER WHOLE | every crossing from the 2nd | every crossing from the 3rd | `IFCASUAL` |

**HARD** (Should): blocks solid 70 f; Elec beams 80 on, 70 off; the gap 112 px; Big Eye HP 28 with its pinch from the
start; the Devil's pieces at 5 px/f from the start and its pinch at HP 14.

#### 4.1.4 Should (v1.1): Guts Man's lifts

On 05-06, **Guts Man's lifts** ride a rail over the pits: OBJ_GUTSLIFT = the vanilla lift contact (`$A0`) + a rail path
table + a tip state: on the dashed rail sections a lift tips for 30 f (Rock slides off if he stays), then rights itself.
[new-code] M. With the tag pocket and the box-art figure: 1.25 sessions.

**Homage moments**: the Magnet Beam in a glass case with a museum label; `NO RUSH JET: AUTHENTIC 1987 EXPERIENCE`;
standing on a knocked-down piece of the Yellow Devil to shoot its eye; the score counter going up for nothing.

### 4.2 H2 ROCKMAN 2 (1988) (`$17`), base vanilla Wily 1 · Should (v1.1+, R0.3 item 5)

**Pitch.** The castle approach, Quick Man's force beams down a shaft, Air Man's fans, Heat Man's appearing blocks,
Picopico-kun, the first E-tank and the Mecha Dragon. When it returns it slots between H1 and H3; nothing later needs it.

**Tileset.** Bank `$69` slot 0, a copy of Wily 1's (`$2A:$80`; 255 of 256 blocks, so the jester head's and some shaft
blocks are dropped). Kept: the purple mountains, chain fence and rubble ground, the red-brick shaft, the updraft blowers
`$36/$41`, the blue riveted section, the Power pocket. The dinosaur's 162-tile set `$8B` is redrawn as the Mecha Dragon
(one size). New: the MUSEUM third, force-beam emitters, the password board.

| GP | From | The player does | Notes |
|---|---|---|---|
| **00** | v00 | The castle approach diorama at night; the wing plaque (E-tanks, passwords, the most famous castle intro) | Metalls `$18` |
| **01** | v01 | **The first E-tank** in a case (a real E-tank, once per save); a plaque with a **1988 postcard** showing a 5×5 password grid (b2) | Fire-Telly drones |
| **02** | v02 | **The password board** (5×5 layout cells; each shot toggles one) by the castle door, then down the well | Metalls |
| **03** | v03 | Top of **QUICK MAN'S SHAFT**; a plaque: Flash Man's Time Stopper stopped the beams, and so does C.FLASH's alt (back in v1.1); a warning light was added | skeleton `$65` |
| **04-08** | v04-v08 | **The force-beam fall** (§4.2.1); Air Man fan robots (vanilla blowers re-skinned) give the fall its rests | bombers `$1B` |
| **09-0D** | v09-v0D | The rest of the fall; the vanilla **Power pocket** at 09 → 14-17 | cannon rider, stompers |
| **0E** | v0E | Checkpoint 1 | |
| **0F** | v0F | Blue riveted hall; *tag pocket* (partner) | samurai spearman |
| **10** | v10 | **Mid-boss: PICOPICO-KUN MK-VI** (§4.2.2), replacing vanilla's jester head | |
| **11** | v11 | **Heat Man's appearing blocks** over lava: BG cells by `alt_flip` in Heat Man's long sequence. Checkpoint 2. A plaque blesses the Rush Jet skip (the homage of 1988's Item-2) | |
| **12** | v12 | Shutter corridor; a huge eye slides past a window (one sprite) | |
| **13** | v13 | **Boss: MECHA DRAGON MK-VI** (§4.2.3) | |
| **14-17** | v14-v17 | The Power pocket (vanilla) | b1's tell at 16 |
| **18** | new | **Hidden room: AIR MAN CAN'T BE BEATEN** | |

#### 4.2.1 The force-beam fall (04-08)

Each beam is a row of layout cells **grown by `map_set`** at 8 px/f (one 16-px cell every 2 frames, inside the repaint
budget) once its emitter has glowed 30 f; the emitter starts when Rock's Y passes its trigger line. **A beam is deadly on
touch**, flagged SPIKE so SPIKE GUARD applies (systems accepts it). Two or three beams per screen; the safe line weaves.
C.FLASH's Time Stop (Should, back by then) freezes a growing beam where it is. The beams cost no slots.

#### 4.2.2 Mid-boss: PICOPICO-KUN MK-VI (fight `$14`)

On **F-PIECES**: the room's right wall is 10 BG blocks. In pairs, blocks detach (`map_set` to empty + a sprite), fly at
Rock's position (2.5 px/f, contact 3), land and become hopping robots (HP 2, STD; hop 24 px every 40 f). At most 2 pairs
alive [9]. The bar counts the blocks left (10 blocks = 28 units). Each detached block leaves a hole; when all ten are
gone, the hole is the exit. Pinch (≤ 4 left): pairs every 60 f.

#### 4.2.3 Boss: MECHA DRAGON MK-VI (fight `$1D`, row 18)

The **Mr. X 4 X Crusher technique**: the dragon is BG in NT0 moved by the scroll above a split, a second split repointing
the bottom band (the pit, a lava glow; tech's `RL_MULTI`). One controller with a position-tested hit box: the **head**
takes damage; the body and wings dink. **The twist: the floor is Heat Man's appearing blocks**: four positions (x 64,
112, 160, 208; 96-112 px above the pit) of sprite platforms (vanilla lift contact), **two solid at a time** (round 1's
three broke the cap); every 180 f one vanishes (it flickers 30 f first) and another appears. **The block Rock stands on
never vanishes.**

| Id | Pattern | Timeline |
|---|---|---|
| A | **HOVER** | bobs ±24 px over 120 f; drifts 32 px toward Rock and back |
| B | **FIREBALL** | every 90 f one fireball aimed at Rock (2.5 px/f, 3 damage); from HP ≤ 18 every 60 f |
| C | **LUNGE** | the jaw opens 20 f (the tell); the head lunges 48 px for 40 f (contact 6) |
| Pinch (HP ≤ 9) | **DIVE** | it sinks out of view (60 f; bubbles and a shadow under one block are the tell), bursts up under that block (gone for 300 f) and drops 3 fireballs one after another as it rises |

Slots: dragon + 2 blocks + 1 fireball = [9]. Damage (systems row 18): KNIGHT.C 4/12 W, SILVER.T 3/16 G, F.BLAST 1/32 R,
PUNCH★ 4/24. M.BEAM bridges a vanished block; the Wall Spear perch and Time Stop return with the alts.

#### 4.2.4 Secrets

| Bit | Secret | How | Tier B hint (draft) |
|---|---|---|---|
| b0 | **QUICK REFLEXES** | fall from 03 to 09 without dying and without Time Stop | `GET DOWN THE FORCE-BEAM SHAFT WITHOUT DYING AND WITHOUT STOPPING TIME.` |
| b1 | **AIR MAN CAN'T BE BEATEN** (18) | in the Power pocket's room 16, white air rings leak through a crack: **a W.STORM tap into the crack** blows it open (wind against wind; R3.1: not another full-strength blow) | `IN THE POWER POCKET, FIRE W.STORM INTO THE CRACK WHERE THE AIR RINGS COME OUT.` |
| b2 | **PASSWORD** | copy the postcard's dots onto the board by shooting them | `COPY THE DOTS FROM THE POSTCARD PLAQUE ONTO THE PASSWORD BOARD.` |

**18**: two Air Man fan robots blow a gale toward a spike wall (VA-GUST, Should with venues_a); walk against it to the
envelope. An empty glass case: `AIR MAN (INVISIBLE EDITION). ON LOAN FROM ROCKMAN CX, WHO MADE HIM INVISIBLE. WE CAN'T SEE
HIM EITHER.` A second plaque describes the 2000s fan song about the robot who could not be beaten. b2: a W-tank + 30.

**CASUAL**: the beams' glow 30 → 45 f; Heat blocks +50 %; Picopico pairs 120 → 180 f; + a checkpoint at 0A; QUICK
REFLEXES allows one death. **HARD**: glow 20 f; one more beam on 05 and 07; Heat blocks 25 % faster; pairs every 90 f;
the dragon dives from HP 14.

### 4.3 H3 ROCKMAN 3 (1990) (`$18`), base vanilla Mr. X 3 · Must

**Pitch.** The third game's wing: the slide, Rush, Break Man's debut and his whistle, Needle Man's presses, Gemini Man's
laser, Rockman 3's turtle machine, and Gamma, which you beat by **riding its own rocket fist up and punching it in the
face**. The Super Adaptor comes out of Gamma's head.

**Tileset.** H3 (bank `$67` slot 0) = a copy of Mr. X 3's (`$2F:$92`; 256 blocks, 255 tiles: the Metonger Z tank's blocks
and tiles are freed for Gamma). Kept: the red gear machinery, the pistons, the warning-light thread (`$0E/$0F`, a palette
cycle on small lamps), Fire-Telly drones (thinned from 23 to 6). New: the MUSEUM third, needle-press heads, crystal tiles
and the Gemini laser, the Break Man statue (BG), the practice fist and punching bag, **Gamma's head and fists** (≈ 100
tiles, R2.11), the turtle-machine re-skin. [new-art] M, Must.

| GP | From | The player does | Enemies [n] | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance; the wing plaque (the slide, Rush, and a mysterious robot with a whistle). The warning light pulses. Up | none [2] | vanilla Power-block 1-up kept | Must |
| **01** | v01 | **RUSH (1990)**: a Rush-shaped spring pad (vanilla spring `$57` code) under the sign `RUSH COIL: PLEASE DO NOT JUMP ON THE EXHIBIT.` The only way up is to jump on the exhibit | samurai spearman `$A2` + its spear [7] | the joke is the route | [engine-ok], Must |
| **02** | v02 | **BLUES (1990)**: a statue on a ledge (BG); its plaque says BLUES (R3.9). A music box plays his whistle as you pass (the Must jingle). E-tank (vanilla). *Should, with the partner: called here, he calls it a bad likeness* | none [2] | | [new-art] S, Must |
| **03-07** | v03-v07 | **NEEDLE MAN'S PRESSES** down the dark machine hall (§4.3.1); b0's hall | ≤ 3 presses + 1 drone or turret shot per screen [9] | | [new-code] S, Must |
| **08** | v08 | **Checkpoint 1** (vanilla's). **The workshop window** (b1's tell): high in the back wall, 112 px up, a lit window under a `STAFF ONLY` sign | none [2; + 2 beams] | | Must |
| **09-0B** | v09-v0B | Up through **GEMINI MAN'S LASER HALL** (§4.3.2) | 1 bomber `$1B` per screen [7] | the laser | [new-code] S, Must |
| **0C-0D** | v0C-v0D | The vanilla machine rooms. *v1.1 (Should): Magnet Man's pull, magnet walls drawing Rock toward spike walls (VA-GUST with magnet art, Should with venues_a)* | stompers `$2D` [vanilla] | | [engine-ok], Must (the pull Should) |
| **0E** | v0E | **Mid-boss: KAMEGORO MAKER MK-VI** (§4.3.3). *v1.1: Doc Robot MK-VI* | | | Must |
| **0F** | v0F | **Checkpoint 2**. *Tag pocket (Should): an emblem shutter → a whistle-shaped 1-UP* | | | Must |
| **10** | v10 | Shutter corridor and **the practice beat** (§4.3.4, R2.11): the Gamma plaque (the head respects only a fist: the SC5 tell), the **practice fist** and the **punching bag**. Shutter checkpoint | the fist + the bag [7] | | [new-code] S, Must |
| **11** | v11 | **Boss: GAMMA MK-VI** (§4.3.5) | | | Must |
| **12** | new | **The Super Adaptor room** (§4.3.6) | | | Must |
| **13** | new | **Hidden room: THE DOC ROBOT WORKSHOP** (§4.3.7) | | | Must |

Checkpoints: 08, 0F and the shutter (10); CASUAL adds 05 and 0C.

#### 4.3.1 Needle presses (03-07)

OBJ_NEEDLEPRESS (family `$F5`, NOFREEZE: a hazard): a 16×48 spiked piston on the ceiling. Rest 70 f, **shake 20 f (the
tell)**, slam down 48 px in 8 f, hold 20 f, rise 30 f. Contact is deadly (spikes; SPIKE GUARD applies). Presses come in
groups of 2-3 with offset timers, **at most 3 per screen** (2 sprites wide each, so three side by side and Rock make 8 on
a line). **Some presses stop 16 px above the floor**: their slammed position leaves a slide gap (Rockman 3's slide,
celebrated; the gap presses have a yellow stripe). The vanilla red pistons are their art base. [new-code] S.

#### 4.3.2 Gemini Man's laser hall (09-0B)

R3.1 (design-5) swaps round 1's Gemini Rock, the input-mirror twin, for its own fallback, the laser: Flame's Shadow
Rock is the game's one mirror twin. **Gemini Rock is Won't (v1).**

Crystal rooms where wall emitters fire **Gemini Man's laser**: a beam head travelling at 4 px/f that **reflects off walls
and floors at 45°**, trailing a 3-segment tail (one object draws head and tail; family `$FA`, NOFREEZE; 3 damage; it
expires after 4 bounces). Each emitter glows 30 f before it fires (the tell); mirror crystals on the walls mark the
bounce points to learn. **09**: one emitter and a climb. **0A**: two emitters taking turns (one beam alive at a time) and
crystal ledges. **0B**: a floor plate aims the next beam: stand on it and the beam's path breaks the crystal wall that
blocks the exit (`map_set`). A plaque (story): Gemini Man's laser bounced. Slots: the laser + 1 bomber = [7]. [new-code] S.

#### 4.3.3 Mid-boss: KAMEGORO MAKER MK-VI (fight `$15`, mid-boss default row) · v1.0

**What it is.** Rockman 3's turtle-dispensing machine (a Wily-stage boss of that game). R3.6 makes v1.0's H3 mid-boss **a
re-skinned vanilla mid-boss**; this is the **vanilla dome dispenser routine** (`$39:$861B`, which vanilla Wily 4 already
reuses at its screen 03 through `$39:$8FBC`'s parameters), with its own parameters and art: the dome becomes the turtle
machine's shell press (HP 20 by the mid-boss default), its walkers become **turtles** (a recolour of vanilla's hard-hat
walkers with a shell), its rocks become eggs. **The twist** (the 1990 rule, a visible special case): **every turtle
destroyed also costs the machine 2 HP**, so the turtles are the way to win, and the machine itself takes the mid-boss
default row. [engine-ok routine + data] + [new-code] S (the rule) + [new-art] S (a re-skin), Must. Its `FRZ_KIND` is
the one the build derives for the vanilla routine (tech §7.7); the turtles are vanilla walkers.

| Id | Pattern | Timeline |
|---|---|---|
| A | **TURTLE** | a turtle drops every 120 f and crawls toward Rock; at a wall it flips onto its back for 60 f, harmless |
| B | **EGG** | an egg lobbed every 180 f (an arc, 2 damage) |
| Pinch (HP ≤ 7) | | a turtle every 80 f |

Slots: the machine + at most 3 turtles or eggs = [9]. **Why this one**: the four vanilla mid-bosses all appear elsewhere
(the gorilla tank in Plant, the jester head in Centaur, the dark-room rider tank in Yamato, the dispenser in Tomahawk and
W3); the dispenser routine is the one vanilla itself already reuses with parameters, and Rockman 3 had a machine that
dispensed turtles, so the re-skin is a mechanic homage. The fact (the machine, and that its turtles were the target)
goes through story's Appendix A. Hook H3-03 (Should): the commentators notice this is not Doc Robot (his exhibit is being
refurbished), which sets up v1.1.

**v1.1 (Should): DOC ROBOT MK-VI** replaces it (R3.1, R3.6). He **copies a Rockman 2 boss**, as Rockman 3's Doc Robot
did: **AIR MAN** (round 1's "copy of your worst venue's champion" is withdrawn: it needed portable champion AI in H3's
room, scope-13). He is reached **only through tech's fight loader**: touching the shutter at 0E calls `fight_load` with
FIGHT_CTX return kind 5 ("the H3 room") into fight `$29` (meta's spare range), a small arena with Air Man's tornado rows
and fans, Doc Robot drawn in a grey X-ray palette with a Doc Robot skull overlay; the win returns to 0E. HP 20 on Air
Man's row (systems adds it with him: PLANT.B 4/12 W, the Leaf Shield homage). Panel: NAME `DOC ROBOT`, SPECIALTY `COPY
OF AIR MAN` (story §5.1's fields). H3's b2 may then become COPYCAT (finish him with PLANT.B). 2.5 sessions.

#### 4.3.4 The practice beat (10; R2.11, design-3)

The fortress's one required form (§0.2) gets a no-risk lesson. A **practice fist** rests on a pedestal; it rises from
floor level to 120 px (Gamma's cockpit height) over 60 f, hangs 60 f and sinks back, on a loop (a vanilla-lift platform,
family `$F5`, NOFREEZE). There is no pit, no enemy, nothing that can hurt. A **punching bag** hangs at the top with a
bell above it: only fists hurt the bag (any other shot dinks and pops `FISTS ONLY`), the same SC5 rule as the fight.
Riding the fist up and punching the bag is the whole lesson; a PUNCH★ from the top rings the bell (b2). The plaque is
the tell (story's words). Slots: the fist + the bag = [7].

#### 4.3.5 Boss: GAMMA MK-VI (fight `$1E`, rows 11/12)

**What it is.** Rockman 3's giant peacekeeping robot: two phases, the second only beaten by a body blow to the head.

**How it is built.** The **Wily 1 Mechazaurus technique**: static BG art in NT0 with no split. **Head and fists only**
(R2.11; about 100 tiles, round 1's 160-tile body is cut): Gamma's head and shoulders loom over the arena's right wall
(x 144-255), as if it stood behind it. **One controller** (family `$F8`, NOFREEZE) owns a position-tested hit box: in
phase 1 the **chin cannon** (64-80 px above the floor, in jump-shot reach) takes damage and the rest of the head dinks;
in phase 2 the **cockpit** (120 px up, out of jump reach). **The twist: its rocket fists** are two 24×24 sprite objects
(3 sprites wide each, so both fists and Rock fit 8 on a line) that fly out, slam down, **become platforms** (vanilla lift
contact) and fly back; in phase 2 they rise to the cockpit with Rock standing on them. [new-code] M, [new-art] M (through
`bgboss.py`), Must.

**Phase 1, the chin cannon** (bar 1, 28):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **ROCKET FIST** | every 150 f, alternating hands: the shoulder sparks 20 f (the tell); the fist flies at Rock's position at launch (4 px/f), slams into the floor or wall, **stays 60 f as a 24×16 platform**, then flies back to its socket on a curve (3 px/f). **The return path hits** (contact 4): the homing return the Super Adaptor will inherit |
| B | **CHIN CANNON** | every 200 f: 3 shots that bounce once on the floor (2 px/f, 3 damage), **one alive at a time** |
| C | **QUAKE** (HP ≤ 14) | a stomp shakes the screen 30 f; dust marks 2 spots, then 2 rocks fall there one after the other |

Slots: the controller + 2 fists + 1 shot or rock = [9]. Damage (systems row 11): W.STORM **4/12 W**, B.ATTACK 3/16 G,
C.FLASH 1/32 R, PUNCH★ 4/24, buster 1/32. (Round 1's Updraft route to the core waits for the alts, Should.)

**Phase 2, the cockpit** (bar 2, refilled to 28: the Wily Machine's multi-bar technique). The chin cannon blows off and
the face plate falls with a crash: **Mr. Y** is at the controls, mask on. **SC5: only fists hurt the cockpit** (systems
row 12: the tap punch 2/30, PUNCH★ 4/12, and on replays the Super fist 3/20; everything else dinks). The ways up:

- **Ride the fist** (the intended way, taught at 10): a fist slams, rests 40 f, then **rises straight up at 2 px/f to
  cockpit height (60 f) and hangs there 60 f** with Rock on it, within punch reach (21-81 px) of the cockpit, then flies
  back.
- **An M.BEAM stair**: two beams (systems' max) make a staircase (H1's tool, re-examined).
- **Jet up, then swap to Power** in mid-air (SELECT + Left/Right, systems §1) and punch on the way down: a skill route.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **FIST ELEVATOR** | every 200 f, alternating: slam, rest 40, rise 60, hang 60, return |
| B | **COCKPIT LASER** | every 240 f: Mr. Y charges a glow (30 f, the tell) and fires a horizontal laser at cockpit height, sweeping the hanging fist (jump off, or time the ride) |
| C | **STUMP SHOT** | every 250 f: one bouncing shot from the broken cannon |
| Pinch (HP ≤ 9) | **DOUBLE SLAM** | both fists slam together and both rise; one is a decoy that **rises 2× faster and returns early** (the tell: its speed) |

Slots: the controller + 2 fists + the laser or a shot = [9].

**The uppercut finale.** The killing blow is always a fist (SC5), so it always gets the flourish: Rock's punch frame
angles up, an `UPPERCUT!` pop (a nod to the spinning top Gamma once needed), and Gamma's head flies off the top of the
screen. Mr. Y ejects in his pod (story's S28 line) and is gone. Two seconds later the head crashes back and cracks open.

**Panel**: NAME `GAMMA MK-VI` (11). **1993 RULES** (Could): SC5 stays on, and Power is reached through the pause menu's
vanilla transform (systems §4.6).

#### 4.3.6 The Super Adaptor (12)

Inside Gamma's head is its power core: a capsule stencilled `RUSH SUPER ADAPTOR. PROTOTYPE. ON LOAN FROM THE FUTURE
(1995).` (Rockman 7's adaptor in a 1993 game: Project SUPER's stolen future tech, the museum's one exhibit that has not
happened yet). Rush runs in and docks: **FORMS.SUPER is set here, with no YOU GET card** (story's rule that adaptors are
never announced on YOU GET; systems §2.3; consistency-28). Roll explains it on the map (story S29, EVENTS2 b4). The screen
is a one-screen demo walk-out: a cracked block behind a pillar that the rocket fist breaks **on its homing return**, and
a ledge that needs the jet hop. Neither is required; the stage clears at the exit. It needs tech's `$9B` audit (M7)
before SUPER is form 3. [new-code] S, Must.

So the Super Adaptor comes out of Gamma at the end of H3, as systems and meta assume; H5 and the castle then build an
optional room around the homing fist (W3's trophy room, §5.4.1).

#### 4.3.7 Secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **SLIDE CLASS** | cross the needle-press hall (03-07) without taking damage | the yellow-striped gap presses, and the hook on the first slide gap | 30 | `GET THROUGH NEEDLE MAN'S PRESS HALL WITHOUT A SCRATCH. SLIDE UNDER THE YELLOW-STRIPED PRESSES.` |
| b1 | **THE DOC ROBOT WORKSHOP** (13) | at 08, build an **M.BEAM stair** (one beam at the top of a jump, a second from it) up to the lit window and walk in (R3.1: a new tool, not a full charge) | the lit window and its sign | envelope + large weapon energy | `AT THE FIRST CHECKPOINT, BUILD TWO MAGNET BEAMS AS A STAIR UP TO THE LIT WINDOW.` |
| b2 | **PRACTICE MAKES PERFECT** | ring the practice bag's bell at 10 with a PUNCH★ thrown from the top of the rising fist | the bell above the bag | E-tank + 30 | `ON THE PRACTICE FIST BEFORE GAMMA, RIDE TO THE TOP AND RING THE BELL WITH A FULLY CHARGED PUNCH.` |

**13, the workshop**: shelves of Doc Robot skulls labelled with Rockman 2's eight bosses (METAL, QUICK, AIR, CRASH,
FLASH, BUBBLE, WOOD, HEAT) and a ninth labelled `MK-VI: BACK SOON` (the v1.1 setup). The envelope and a large weapon
energy.

**Hooks** (story's words): H3-01 the Rush Coil sign (Should); H3-02 the statue (Should; a partner variant); H3-03 the
turtle factory (Should); H3-04 the first slide gap (Must: b0's tell); H3-05 the practice bag's first dink (Must: SC5's
tell); H3-06 Gamma's bar fill (S28, Must); H3-07 the first W.STORM hit on the chin (the first-weakness line, Must); H3-08
phase 2, Mr. Y at the controls (S28, Must); H3-09 the uppercut (Must); H3-10 b0's secret line (Must); H3-11 and
H3-12, the b1 and b2 lines (Should: generic lines in v1.0, R8.6). **Respawns**:
story §6.5; wing-tagged drafts (Should): *"My Gamma is twice as tall in person."* / *"Doc Robot is on a coffee break."*

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | none | — | — | — |
| mash | none | — | — | — |
| timer | the presses' rest; the fists' hang (practice and phase 2) | 70 f; 60 f | 105 f; 90 f | `TIERVAL` |
| checkpoint | 00-08, 09-0F | 08, 0F | + 05, + 0C | dormant checkpoints |
| secret step | b0 SLIDE CLASS | no damage | at most 1 hit | `IFCASUAL` |

**HARD** (Should): presses rest 50 f; no slide-gap presses on 06; turtles every 80 f from the start; Gamma's fists hang
40 f and the decoy fist from the start of phase 2.

**Homage moments**: jumping on the Rush Coil exhibit against the sign; sliding under a slammed needle press; a laser
bouncing through a crystal room; riding Gamma's fist up and punching Mr. Y; the Super Adaptor "on loan from 1995".

### 4.4 H4 ROCKMAN 4 (1991) (`$19`), base vanilla Mr. X 2 · Should (v1.1+, R0.3 item 5)

**Pitch.** The fourth game's wing is Dr. Cossack's citadel, and Kalinka is in the booth, so it is personal: the charge
shot and the Metalls that learned to hide, Bright Man's flash bulbs, the falling chapel bells, Cossack's Balloon, Dust
Man's conveyors, Toad Man's rain, and the Cossack Catcher. R3.1 swaps two round-1 set pieces (design-5): the dark rooms
become a **flash-bulb photo puzzle** (the Riot keeps the game's one lights-on-a-timer set piece), and the spiked
compactor ceiling becomes **Dust Man's conveyors**, with no ceiling chain.

**Tileset.** Bank `$69` slot 1, a copy of Mr. X 2's (`$2F:$89`; 157 of 256 tiles referenced, so about 100 free for snow,
onion domes, bells and the crane). Kept: the machine blocks, the falling bell row, the pod-column technique.

| GP | From | The player does | Notes |
|---|---|---|---|
| **00** | v00 | The citadel diorama: snow on the machine blocks, onion domes in the windows; the wing plaque (the charge shot, Eddie, a scientist who was framed). Kalinka recognises her home | |
| **01-02** | v01-v02 | Snow Metalls (vanilla `$18`, the full-punch rule) | Metalls, drill tanks `$6E` |
| **03-05** | v03-v05 | **BRIGHT MAN'S PHOTO BOOTH**: the rooms are lit, but part of the route is **invisible blocks**. Shooting a wall-mounted flash bulb takes a photo: the room fades to a negative for 30 f (a fade, never a strobe, §0.9), and the hidden blocks show in it, then stay as outlines for 4 s (`alt_flip` on their ids) before fading out; a bulb recharges in 2 s. Each room needs one more photo than the last | [new-code] S |
| **06** | v06 | **The chapel bells**: vanilla's falling bell row, kept, re-skinned as onion-dome bells; **each bell rings a note as it drops**, so a clean run plays a scale (b0) | [engine-ok] + SFX |
| **07** | v07 | **WIRE & BALLOON (1991)**: a case with both inventions. The Balloon is a rideable platform that floats at 0.5 px/f in the D-pad's direction (it sinks slowly when idle), pops after 8 s and respawns at its post. It carries Rock over a 160-px pit to 08, and up to a door high in the wall (b1) | [new-code] S |
| **08** | v08 | Checkpoint 1 | |
| **09-0D** | v09-v0D | **DUST MAN'S CONVEYORS**: conveyor floors carry Rock and junk blocks toward a crusher pit at each screen's end (a grounded push, VA-GUST, Should with venues_a); junk-block pockets (Power) hold items; **Flip-Top Jr.'s cage at 0B** rides a conveyor toward the crusher (b2) | skull drones `$66`, walkers `$67` |
| **0E-0F** | v0E-v0F | **Toad Man's rain**: rain sprites (≤ 4, cosmetic) and a wet floor with ice momentum (floor type 5); *tag pocket at 0F* | Metalls |
| **10** | v10 | Shutter corridor; checkpoint 2; a plaque (a claw machine with a scientist in it) | |
| **11** | v11 | **Boss: COSSACK CATCHER MK-VI** (§4.4.1) | |
| **12** | new | **Hidden room: KALINKA'S ROOM** | |

#### 4.4.1 Boss: COSSACK CATCHER MK-VI (fight `$1F`, row 19)

Dr. Cossack's claw machine from Rockman 4, piloted by a **Kalinka-shaped decoy robot** (Kalinka denies the likeness). The
**Mr. X 2 pod technique**: the cabin (a 64×48 glass dome) is BG in NT1 positioned by the scroll above the split
(`RL_FLOOR`); **the twist**: the cabin also **travels along a crane rail** (the X scroll), and a sprite claw (the trophy
theft's claw art, Must with S25, reused) drops from it and **grabs Rock** (tech's attach state, input rule
"struggle"). The arena is a prize pit with two prize capsules (a
large life and a `KALINKA PLUSH`) that respawn 300 f after being taken.

| Id | Pattern | Timeline |
|---|---|---|
| A | **RAIL** | the cabin slides toward Rock at 1.5 px/f for up to 120 f, at rail height (out of jump reach) |
| B | **CLAW DROP** | a ding-ding chime and the claw opens 20 f (the tell); the cabin lowers 48 px (now in jump-shot reach) and the claw drops at 4 px/f. If it touches Rock: GRAB. Otherwise it takes what is under it: a capsule is lifted and thrown at Rock (3 damage) |
| GRAB | | Rock is lifted at 1 px/f, controls locked except A/B: **10 presses within 90 f, or hold to struggle** (R2.9, design-13) wriggle free; otherwise `PRIZE GET!`: the cabin drops him in the prize chute (6 damage) |
| C | **ICICLE SHAKE** (HP ≤ 14) | the cabin rattles the rail; 2 icicles wobble 30 f, then fall one after the other |
| Pinch (HP ≤ 9) | **C.HOPPER** | the claw detaches and hops on its three fingers (8 HP, contact 4; destroying it is the style act PRIZE DENIED) while the cabin drops 1 bomb per pass |

Slots: cabin + claw + 2 capsules = [9]. Damage (systems row 19): Y.SPEAR 4/12 W, W.STORM 3/16 G, KNIGHT.C 1/32 R,
PUNCH★ 4/24. KNIGHT.C's Hold (an alt, back by then) catches a capsule before the claw does. Defeat: the coin slot spews
coins, the decoy pops up on a spring neck, and the cabin slides into the prize chute.

#### 4.4.2 Secrets and the friend

| Bit | Secret | How | Tier B hint (draft) |
|---|---|---|---|
| b0 | **BELL CHOIR** | cross 06's bells in one go, so all eight drop in order (a rising scale, then a chord) | `RUN ACROSS THE CHAPEL BELLS WITHOUT STOPPING OR TURNING BACK.` |
| b1 | **KALINKA'S ROOM** (12) | **steer Cossack's Balloon** up from 07 to the door high in the wall (R3.1: a set-piece tool, not a punch); the Balloon must rise for about 4 s | `RIDE THE BALLOON IN THE INVENTION ROOM UP TO THE HIGH DOOR. KEEP IT RISING.` |
| b2 | **FLIP-TOP JR.** | the cage riding the conveyor at 0B holds `EDDIE PROTOTYPE (1991)`; its lock faces the wall, so only the **Super fist's homing return** strikes it. You have until the conveyor reaches the crusher (about 10 s); then the cage drops into a floor safe until a replay | `THROW THE SUPER FIST PAST THE CAGE ON THE CONVEYOR. ON ITS WAY BACK IT HITS THE LOCK.` |

**12, Kalinka's room**: a bed, a radio, a stack of drawings (one of Rock), an empty bird cage with a sign `BEAT WAS HERE
(ROCKMAN 4 MINUS INFINITY)` and a plaque thanking 4MI for rescuing her properly; the envelope and a 1-UP. **Flip-Top
Jr.** (Eddie's little brother) is a friend mechanic (4MI lesson 4): freed, he appears in the W3 escape and throws Rock a
large life and a large weapon energy (§5.4, 09), and rides Eddie's cart in the lap (Could). b2: 30 bolts.

**CASUAL**: GRAB 6 presses or hold; the photo outlines 6 s; the Flip-Top window 15 s; + a checkpoint at 0B; BELL CHOIR
allows one stop. **HARD**: outlines 3 s; faster conveyors; GRAB 14; icicles from the start; C.HOPPER at HP 14.

**Homage moments**: a photo flash revealing the floor you are standing on; the chapel bells ringing a scale as they
fall; riding Cossack's Balloon past his own exhibit; the rocket fist curving back to spring a caged Eddie; the claw
carrying Rock to the prize chute.

### 4.5 H5 ROCKMAN 5 (1992) (`$1A`), base vanilla Mr. X 4 · Must

**Pitch.** The fifth game's wing is "Blues' castle" (it wasn't his): Star Man's low gravity, Gravity Man's hall, Crystal
Man's crystals, Beat's letters, the ridable Super Arrow, and **Dark Man MK-VI disguised as Break Man**, an impostor of a
robot the player has already met. At the end of the corridor is a sixth door: the 1993 wing, under construction.

**Tileset.** H5 (bank `$67` slot 1) = a copy of Mr. X 4's (`$2B:$80`; only 159 of 256 blocks used). Kept: the grey stone
castle with red lights, the X crates and drones, cage cylinders, ceiling spiders `$3C`, the open pit branch, the cowboy
gunners `$6C`. New: the MUSEUM third, a starfield, crystal emitters, letter plates, the Super Arrow launcher, the throne
room; room 19 loads vanilla's own Mr. X 1 set `$9D`. [new-art] M, Must.

| GP | From | The player does | Enemies [n] | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance; the wing plaque: Beat, the Super Arrow, and **Blues' castle** (it wasn't his) (R3.9) | spiked ceiling unit `$A1` (vanilla) | big WE (vanilla) | Must |
| **01-02** | v01-v02 | **STAR MAN'S SPACE**: a starfield room with **low gravity** (floor type 8's gravity `$00.18` with **the bubbles suppressed**: a stage flag, [new-code] S, feasibility-19); long floaty jumps between cannon ledges over spikes | wheel cannons `$C0/$C9` [vanilla] | | [new-code] S, Must |
| **03-07** | v03-v07 | **GRAVITY MAN'S HALL** (§4.5.1): v1.0 is its **low-gravity form**; letter plates (b0) | X crates `$CB`, cage cylinders `$33` | | [new-code] S, Must (the flips Could) |
| **08** | v08 | **CRYSTAL MAN'S CRYSTALS**: two ceiling emitters drop crystal orbs in turn (one orb alive at a time, one every 60 f); an orb shatters on the floor into **2** shards (2 damage) | eye cannon `$54` (its shot waits while an orb or shard is alive) [9: the orb or its 2 shards, the cannon, one shot] | | [new-code] S, Must |
| **09** | v09 | **Checkpoint 1** (vanilla's). The open branch 16-18 starts at the right | walkers `$12` | | Must |
| **0A-0E** | v0A-v0E | Up and right through the crate halls | ceiling spiders `$3C` | the 1-UP at 0E (vanilla); *tag pocket at 0C (Should)* | [engine-ok], Must |
| **0F-10** | v0F-v10 | Down; the E-tank at 10 (vanilla) | | | Must |
| **11** | v11 | **Checkpoint 2** | | | Must |
| **12-13** | v12-v13 | **THE SUPER ARROW (1992)**: a launcher fires a ridable arrow every 120 f across a 160-px pit (it flies level at 2 px/f, then dips); ride it over. The arrow is a moving platform on the vanilla lift contact (family `$F5`, NOFREEZE); at most 2 alive. A plaque: a weapon you could stand on, and still can | cage cylinders [8] | | [new-code] S, Must |
| **14** | v14 | Shutter corridor. On the left wall, **a sixth door**: `ROCKMAN 6 (1993): WING UNDER CONSTRUCTION. KNOCK.` (b1) | | | Must |
| **15** | v15 | **Boss: DARK MAN MK-VI** (§4.5.2), in a throne room with a Blues-style emblem; then **the unmasking** (§4.6) | | | Must |
| **16-18** | v16-v18 | **Branch**: vanilla's open, risky shortcut, kept: floating platforms over the pit, rejoining at 0F and skipping 0A-0E (and the 1-UP). Two letters (b0). *v1.1 (Should): the platforms ride Wave Man's water geysers that rise and fall 32 px on a 120-f cycle* | cowboy gunners `$6C` [vanilla] | | [engine-ok], Must (the geysers Should) |
| **19** | new | **Hidden room: THE 1993 WING** (§4.5.3) | | | Must |

Checkpoints: 09, 11 and the shutter (14); CASUAL adds 05 and 0D.

#### 4.5.1 Gravity Man's hall (03-07)

**v1.0 (Must)**: low-gravity rooms like 01-02, with spikes on the ceiling as well as the floor, laid out to be crossed
upright (round 1's flip layouts mirrored). **Could: GRAVITY ARROWS** (round 1's design): wall panels with an up or down
arrow flip gravity; Rock falls toward the ceiling, his sprite V-flipped and his floor test reading the tile above him.
The rules that keep it small: flip rooms have no ladders and only left/right exits; enemies are not flipped; spikes line
both floor and ceiling; a flip resets at the screen edge. [new-code] M, Could (3 sessions).

#### 4.5.2 Boss: DARK MAN MK-VI (fight `$20`, row 13)

**What it is.** In Rockman 5, "Blues" kidnapped Dr. Light, and it was Dark Man in disguise. MK-VI plays the same trick on a
player who has met the real Break Man.

**How it is built.** A family `$F8` boss controller behind vanilla's Robot Master intro (`$93`, the panel by fight id).
Phase 1 wears **the disguise**: a 40-tile enemy-area set made from the NPC Break Man composite (feasibility-14, art's
budget) with **the scarf the wrong colour, orange instead of yellow**: the one visual tell (consistency-8: this doc's
orange scarf; story and art follow). Phase 2 is Dark Man (≈ 64 tiles, ≤ 16 frames, composited first, R5.1). FRZ BOSS.
[new-code] M, [new-art] M, Must.

**The twist: the boss panel lies.** Vanilla's typed panel (`$3C:$81B1`, fields `$3C:$85EE-$8615`) types the disguise's
record, and tech's **re-type** entry (§11.2, M5) later types the truth over it. The strings follow story §5.1's fields
(NAME ≤ 12, SPECIALTY ≤ 19; glyphs `0-9 A-Z . - ? ! ' β` and space; consistency-22) in vanilla's no-space style for a
Robot Master's name (R8.5): NAME `BREAKMAN`, SPECIALTY `DEFINITELY BREAKMAN`, re-typed as NAME `DARKMAN`, SPECIALTY
`BAD DISGUISES`. There is no "?" on the card: the panel lies with a straight face (story §5.4 writes the records).

**HP 28, two phases on one bar.** Robot scale (systems row 13): F.BLAST **4/16 W**, PLANT.B 3/20 G, SILVER.T 1/45 R,
buster 1/60, PUNCH★ 3/30.

Phase 1, **DISGUISE** (28 → 14):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **WHISTLE** | stands and whistles Break Man's melody **with one wrong note** (the audio tell; a red note sprite pops on it for 20 f); 180 f the first time, 90 f afterwards; hittable |
| B | **BREAK SHOT** (a copy) | three small shots 12 f apart (2 damage), then a charged shot at f90 (4 damage, 3 px/f) |
| C | **SHIELD JUMP** | jumps toward Rock with a shield up (frontal shots reflect while he is airborne), lands, 30 f |
| | Cycle | A, B, C, B. Slots: Dark Man + ≤ 3 shots = [9] |

At HP 14: **THE MASK SLIPS** (90 f, invulnerable): the costume pops off and flies away, the orange scarf flutters down,
the panel re-types, the music changes.

**The WRONG NOTE exposure** (b2; Must; a visible special case beside systems' SC list, systems §4.6). Hit him with a
**full charge** (LATCHSRC's FULL flag) **while the red note is up**: the real whistle answers from off-screen, in tune
(the Must jingle), and the disguise falls at once: his HP drops to 14 if it is higher, and the panel re-types a **third
record**, `DARKMAN` / `BAD DISGUISES` with VENUE `EXPOSED BY A WHISTLE` (story §5.4; tech's re-type supports a third
record, R8.5). This is story S30's "walked" staging, used in v1.0 because the partner is Should. *With the
partner (Should): calling Break Man in phase 1 exposes him in person (TWO BREAK MEN, S30's partner variant), with the same
effect.*

Phase 2, **DARK MAN** (14 → 0):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **BARRIER** | 4 orbs orbit him for 120 f, drawn by **one ring object** (venues_a's Plant Man trick); they reflect shots (contact 3) |
| B | **SHOCKWAVE** | a 48-px jump and a slam: two floor shockwaves (8 px tall, 2 px/f, 3 damage) |
| C | **DARK BALL** | a 32-px ball aimed at Rock at 1.25 px/f; it splits into 2 when it hits a wall (round 1: 4) |
| | Cycle | A, B, C, B (≈ 380 f). Slots: Dark Man + the ring, 2 waves or 2 halves = [8] |
| Pinch (HP ≤ 7) | **HEAVY AIR** | every 300 f the arena's gravity drops to the hall's low gravity for 120 f (H5's own hazard turned on you; he wears magnetic boots and stays put). *Could: the arena flips, with the gravity arrows* |

**Defeat.** He explodes; his visor flies off, and inside it is a little stamp: `MADE BY MR. Y`. Then the unmasking (§4.6).

#### 4.5.3 Secrets, and Mr. X's card

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **ROCKMAN5** | collect the eight letter plates R-O-C-K-M-A-N-5 (Rockman 5's own letters in the Japanese release, which built Beat; the same plates in both languages, R8.5, story A-5.3): six on screens both routes share (03, 05, 08, 0F, 12, 14) and two on the branch (16-18); an ICONROW widget (2 rows of 4) under the life bar fills in | the letters glow; the first is on the main path at 03 | 30 | `FIND THE EIGHT LETTERS R-O-C-K-M-A-N-5 IN THE 1992 WING. THE SHORTCUT HAS TWO.` |
| b1 | **THE 1993 WING** (19) | at 14, knock on the under-construction door: any shot or punch is a knock, and a number (1-6) pops over the door; **six knocks within 6 s** open it (story's line) | the `KNOCK` sign; the first knock gets an answer | envelope | `KNOCK SIX TIMES, FAST, ON THE UNDER-CONSTRUCTION DOOR BEFORE DARK MAN.` |
| b2 | **WRONG NOTE** | expose the disguise with a full charge on the wrong note (§4.5.2) | the red note and the off-key whistle | 30 | `WHEN THE FAKE BREAK MAN WHISTLES, HIT HIM WITH A FULL CHARGE ON THE WRONG NOTE.` |
| b3 | **MR. X'S BUSINESS CARD** | on the floor of the 1993 wing | it is the only object on the diorama floor | RATEFLAGS b1 (rating T14) | none: T14's hint is Break Man's (`meta.md` §6.2) |

**19, the 1993 wing**: a diorama of **vanilla Mr. X Fortress 1, screen v00** (the night city and the moon, the 1993 art
untouched: vanilla's BG set `$9D` and palette `$68`, loaded at the room's entry), a mannequin of Mr. X (the vanilla
reveal sprite) behind a velvet rope, a plaque (story's; the game you are playing, "exhibit in progress"), the envelope,
and on the floor **Mr. X's business card** (story's text, consistency decision 10). Taking it sets RATEFLAGS b1. The room
is the museum's joke about the game you are playing. *Won't (v1): a back door to Mr. X Returns.*

**Hooks** (story's words): H5-01 Star Man's space (Should); H5-02 the first crystal (Should); H5-03 the Super Arrow
(Should); H5-04 the first knock's answer (Must: b1's tell); H5-05 the wrong note (Must: b2's tell, S30); H5-06 the mask
slips (Must, S30); H5-07 the real whistle answers (Must, S30); H5-08 the first F.BLAST hit (the first-weakness line,
Must); H5-09 b0's secret line (Must); H5-10 and H5-11, the b1 and b2 lines (Should: generic lines in v1.0, R8.6; the
b1 and b2 tells H5-04 and H5-05 stay Must). Round 1's "That's not Blues!" / "Obviously not Blues." are deleted (R4.2).
**Respawns**: story §6.5; wing-tagged drafts (Should): *"My Dark Man is a master of disguise."* / *"Blues' castle! It
was mine all along! Like everything!"*

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | b2, the red note | 20 f | 40 f | `TIERVAL` |
| mash | none | — | — | — |
| timer | b1, the knock window; the arrows' interval | 6 s; 120 f | 9 s; 120 f (the arrow is a ride, not a timer) | `TIERVAL` |
| checkpoint | 00-09, 0A-11 | 09, 11 | + 05, + 0D | dormant checkpoints |
| secret step | b0 ROCKMAN5 | 8 letters | the letters stay collected after a death | `IFCASUAL` |

**HARD** (Should): one more spike row in the low-gravity rooms; crystals every 45 f; arrows every 150 f; Dark Man's
phase 1 at full speed from the start; HEAVY AIR from HP 10.

**Homage moments**: a moon jump over spikes in Star Man's starfield; riding a Super Arrow across a pit; the boss panel
typing `DEFINITELY BREAKMAN`, then re-typing it; the real whistle answering the fake one; knocking six times on the 1993
door and finding the 1993 game inside, with Mr. X's business card on the floor.

### 4.6 Mr. Y's unmasking (after H5; `meta.md` EVENTS b6) · Must

Played in H5's throne room right after Dark Man. Story's S32 ("the cup on the pedestal") and S33 (the unmasking) are
staged **here** (consistency-6 and its decision 8: this doc places scenes, story owns the words; story's "central
gallery" is this throne room). It is built on **vanilla's Mr. X reveal**: the pod sprite, the typed speech at the top of
the screen in the `$6C/$6D` style, the flight path `$39:$8E04` and the object animations `$39:$8DE9` [engine-ok] + text,
Must. About 25 s; START skips it after the first viewing (R3.8).

1. **The GP Cup** sits on the throne's pedestal, cables running out of it into the walls (S32's beat).
2. **Mr. Y descends** in his pod (the vanilla Mr. X pod, recoloured, with a Y emblem).
3. He pulls off the Y mask. Underneath is **the Mr. X face** (the vanilla 1993 sprite): the wrong layer.
4. He pulls off the X mask: **Dr. Wily**.
5. Everyone answers at once, one window per face icon (Cossack, Kalinka, Rock; Light and Roll on the radio):
   **"WE KNOW."** The third and last act of the Wily gag (R4.4).
6. Project SUPER (story's speech, S33). The pod's claw takes the GP Cup, and he flies off along the vanilla path with it.
   The cup turns up again in W3's Trophy Dispenser (§5.3.1).
7. A black screen, typed like vanilla's `$6E` (story's pun on vanilla's こんどは しんけんしょうぶ だ!!).
8. **Vanilla's Wily Fortress picture** (the skull castle with lightning, unchanged 1993 art) appears first in **four
   shades of green**, then its palettes step up to NES colours and then to the SUPER palettes (8-f steps, no strobe): the
   castle "upgrades", and the title `SUPER WILY CASTLE` slides in (story's "it is starting from the bottom"). Palette data
   only, Must. *Could: ExGrafix per-tile colour blooming over the picture (R1.3: it has no scroll and no text, tech §3.3).*

After the unmasking, the W stages' heckler is Wily (story's Wily table, §0.5). If the M4 re-estimate asks for cuts
(R8.1; §v1.0 scope's list), this scene moves to H3's ending (Mr. Y unmasks in Gamma's cockpit).

---

## 5. SUPER WILY CASTLE (`$1B-$1D`, meta 19-21) · W2, W3 Must (M8); W1 Could

### 5.0 SUPER colour in v1.0 (R1.3, R8.3)

Project SUPER is Wily's "16-bit upgrade" (BRIEF §1), and the castle shows it. Round 1 drew it with ExGrafix (ExRAM mode
1) across W1-W3; that collided with tech's text window, which keeps ExRAM in mode 0 for the whole game (the blocker
feasibility-1 / consistency-1). The ruling:

- **No ExGrafix in W2, W3 or the escape**, and **no extra 4 KB CHR page** (with 8 KB CHR-RAM the page bits reach only
  the two pattern tables).
- **SUPER colour in v1.0 = richer per-screen palettes, parallax and palette bands** (tech's `RL_PARALLAX` and
  `RL_PALBAND`). **The 2A03 music keeps all its channels** in W2, W3 and the escape (R8.3).
- **The channel drop is LIGHTS OUT's** (S42, §6.1 scene 9): the D9 mute mask takes G37's 2A03 stems away one at a time
  until pulse 1 plays alone (Must, R8.3). **The MMC5 pulse voices are Could**: if they ship, the castle adds them and
  the escape drops only them (§5.4).
- **ExGrafix is Could, with W1**: only in W1's locked, text-free 16-bit rooms and the METALL 16 arena, filled in mode 2
  while the screen is blanked, with the announcer held (tech §3.3). The castle picture's ExGrafix bloom (§4.6) is Could
  too.
- Round 1's three eras (POCKET / NES / SUPER, F-ERA) belong to W1 (Could). The escape's v1.0 "downgrade" is palettes
  only (§5.4).

### 5.1 W1 UPGRADE LAB (`$1B`) · Could (v1.1+, R0.3 item 5)

**Pitch.** The castle's entrance lab scans Rock, declares him obsolete, and downgrades him to a pocket screen "for
compatibility". You fight back up: an upgrade gate to NES colour, then a second to 16-bit, where the castle is gorgeous
and Roll's smuggled patches make Rock shine. The boss is a giant Metall that upgrades itself between bars. When W1
returns it slots before W2; its door on the castle map is shut in v1.0.

**The eras** (F-ERA, tech, Could):

| | **POCKET** (the 1991 handheld era) | **NES** | **SUPER** |
|---|---|---|---|
| View | a 160×144 window in the middle of the TV; the border is **opaque BG of a non-zero colour** (feasibility-20) | full screen | full screen |
| Palette | four greens | normal | richer per-screen palettes; **ExGrafix only in the locked, text-free 16-bit rooms (0D-10, held announcer) and the METALL 16 arena** (R1.3) |
| Audio | the POCKET arrangement (2 pulses + noise) | the 2A03 arrangement | 2A03, plus the MMC5 voices if they ship |
| Rock's firmware | **FW 1.0**: no slide, no charge, no forms (the first handheld Rockman had neither a slide nor a charge); a `FW 1.0` LABEL widget | FW 6.0 | FW 6.0. `NOT COMPATIBLE` is **cosmetic**: round 1's half-damage rule is dropped (R3.9, design-19) |
| Camera | flip-screen rooms (vanilla's teleport `$39:$89F5` behind a 16-f fade); enemies emerge from the black border (tech's OAM behind-BG override, Could) | scrolling | scrolling, up to 3 parallax bands, foreground pillars (over colour-0 backgrounds only, feasibility-20) |

| GP | Era | The player does | Notes |
|---|---|---|---|
| **00** | NES | The **FORMAT CHECK** scanner gate downgrades Rock (a 30-f iris to the window, the palette greens, the music thins) | |
| **01-04** | POCKET | Four pocket rooms: a ledge climb; low-ceiling gaps jumped through without the slide; a drop; **the blind jump**, whose next ledge now **shows 8 px inside the window** (design-19) with an arrow sign | green Metalls and drones emerge from the border |
| **05** | POCKET | **Mid-boss: ENKER MK-VI** (fight `$16`): the handheld game's first "Mega Man Killer". His raised spear absorbs shots and releases 3 as one big shot (4 damage); shoot him while the spear is down (GUARD 60 f, CHARGE across the window, RELEASE). HP 20, mid-boss default | it teaches patience where you cannot charge |
| **06** | NES | **UPGRADE GATE 1**: the window opens to full screen, colour floods in, `FW 6.0`. Checkpoint 1 | |
| **07-0B** | NES | **The palette blocks**: RED and BLUE sets, each solid only in its colour's phase; the palette cycles every 120 f with a 30-f pulse as the tell (`alt_flip` on a timer: VA-TIMED on tech's service) | Metalls, bombers; *tag pocket at 0A* |
| **0C** | SUPER | **UPGRADE GATE 2**: Project SUPER activates; `WARNING: ROCKMAN NOT COMPATIBLE` (cosmetic). Checkpoint 2. Roll on the radio: look for the patches | |
| **0D-10** | SUPER | **The 16-bit section**: SUPER enemies in richer palettes; **Roll's SUPER PATCH capsules** (3; CX's Light capsule, credited): 20 s of **16-BIT MODE**, every buster shot a full charge (a METER widget); 0E parallax and foreground pillars; 0F translucent water (a PPUMASK emphasis band over floor type 8, 4MI's Cossack 3 water, credited) | |
| **11** | SUPER | The UPGRADE CHAMBER (shutter) and the broken **32-BIT (NOT READY)** gate (b1) | |
| **12** | all three | **Boss: METALL 16** | |
| **13** | — | **Hidden room: THE 32-BIT ROOM** | |

**METALL 16** (fight `$22`, systems row 20). Project SUPER's flagship prototype: a giant Metall built with the Mr. X 3
Metonger Z technique (BG in NT1 with its own floor copy, `RL_FLOOR`; the face under the brim is a sprite). **It upgrades
itself between bars** through F-SIZES (tech, Should): POCKET 64×48 in greens, letterboxed by two bands; NES 96×64; SUPER
128×80 in the locked arena's ExGrafix. Three bars of 14. **Helmet down: only full-power blows hurt** (vanilla's Metall
rule, `$3F:$EA99`, and GP's FULL flag). Patterns per bar: HIDE, PEEK (one bullet), HOP (its shadow is the tell); PEEK
3-WAY, MET CALL (≤ 2 small Metalls); SPIN (rolls across the floor), PEEK SPREAD, PARATROOPERS (≤ 2); the pinch DX HOP.
**The weakness is a flip**: W.STORM 4/12 W, and its SC9 reaction flips the helmet onto its back for 60 f, when
everything hurts; SILVER.T 3/16 G, F.BLAST 1/32 R. Slots: the Metall + ≤ 3 small Metalls or shots = [9]. Defeat: the
helmet cracks open and a normal-size Metall waves a white flag.

| Bit | Secret | How | Tier B hint (draft) |
|---|---|---|---|
| b0 | **BACKWARD COMPATIBLE** | the POCKET section (01-05, Enker included) with no damage | `GET THROUGH THE GREEN HANDHELD ROOMS, ENKER INCLUDED, WITHOUT TAKING A HIT.` |
| b1 | **THE 32-BIT ROOM** (13) | the broken 32-BIT gate at 11 opens only for a robot **still in 16-BIT MODE**: keep the last patch's 20 s alive from 10 to 11 (R3.1: not a full-charge key) | `ARRIVE AT THE BROKEN 32-BIT GATE WHILE A SUPER PATCH IS STILL ACTIVE.` |
| b2 | **8-BIT PRIDE** | the 16-bit section (0D-11) without touching a patch | `CROSS THE 16-BIT SECTION WITHOUT USING ANY OF ROLL'S UPGRADE CAPSULES.` |

13: everything drawn in flat diagonal "polygon" tiles; a plaque (story's): Rockman 8 (1996), on loan from a future that
is not ready (kept, consistency decision 40); the envelope and a 1-UP. b1 and b2 need two runs, by design.
**CASUAL**: the palette cycle 120 → 180 f; patches 20 → 30 s; checkpoints + 03 and + 0F; BACKWARD COMPATIBLE allows one
hit (round 1's "CASUAL keeps the slide in POCKET" is dropped: it is not one of R2.9's levers). 14 sessions.

### 5.2 W2 BRACKET OF DOOM (`$1C`), base vanilla Wily 3 · Must

**Pitch.** Vanilla Wily 3's boss rush (a hub, eight teleporters, a ninth after the eighth win), turned into a tournament
bracket: eight Project SUPER copies of the champions in four **pair bouts**, then **the final against Bass β** (story S36,
S37).

**Tileset.** W2 (bank `$68` slot 0) = a copy of Wily 3's (`$2A:$92`; base set `$A2` + `$A8` + `$A9`). Kept: the water
castle, the teleporter, the hub and its alcoves, the hub lights thread `$13`. New: **the bracket board** on the hub's back
wall (the champions' 16×16 face icons as BG tiles, R5.1; lines lit by palette entries; vanilla's pause-menu weapon icons
copied in for the finishers), SUPER palettes for the moat and hub, the Championship Ring. [new-art] M, Must.

| GP | From | The player does | Enemies | Set pieces | Tags |
|---|---|---|---|---|---|
| **00-05** | v00-v05 | **The moat**: vanilla's underwater castle (floor type 8 throughout) in **SUPER colour**: richer palettes and one bottom `RL_PALBAND` (§0.11) | piranhas `$C1`, clam capsules `$CA` (vanilla) | spike pits; items as vanilla | [engine-ok] + palette data, Must |
| **06-07** | v06-v07 | Up past wheel cannons to the teleporter pad (07: collision D → `$1F`, vanilla). Checkpoint 1 at 06 | `$C0/$C9` | | [engine-ok], Must |
| **08** | v08 | **The bracket hub** (§5.2.1). Checkpoint (vanilla's: the hub is checkpoint 08). A plaque (story) | none | the board | [new-code] M, Must |
| (arenas) | the venues' boss rooms | **Pair bouts** (§5.2.2) through the fight loader | | | Must |
| **11** | new | **The Championship Ring**: Bass β, duel 2 (§5.2.3) | | | Must |
| **12** | new | Walk-out; stage clear | | | Must |
| **13** | new | **Hidden room: THE LOSERS' BRACKET** (§5.2.4) | | | Must |

Vanilla's eight refight rooms (v09-v10) stay in the legacy layout of id `$0E` for the 1993 CUP (Could); W2 does not use
them.

#### 5.2.1 The hub as a bracket [new-code] M (feasibility-3, feasibility-19: round 1's "[engine-ok] data" is withdrawn)

- **Vanilla's machinery is kept**: the per-frame routine `$39:$8E3B` reads the touched alcove metatile and looks up
  `$8ED2` (boss), `$8EC8` (X) and `$8EDC` (alcove metatiles); each win closes that alcove through its `$0340` bit; after
  all eight, byte `$0C` opens the ninth teleporter at the top centre.
- **The tables are re-ordered so pairs sit side by side**, on the Exhibition pairs the player knows from the bracket: left
  top + left middle = **Wind + Knight**; left bottom + centre left = **Tomahawk + Plant**; right top + right middle =
  **Blizzard + Flame**; right bottom + centre right = **Yamato + Centaur**.
- **The back wall is the bracket board**: 8 face icons in 4 pairs, a line from each pair to a quarterfinal node, two
  semifinal nodes, and the FINAL over the ninth teleporter. Lines light (one palette entry each) as bouts are won; a small
  icon beside each face shows the weapon that finished that copy (b0). The board is written by `map_set` from save
  flags at the hub's init.
- **Tech's fight loader replaces vanilla's "redraw screen `$09` + id"** (R1.7): an alcove calls `fight_load(champion,
  ctx = hub)`; meta's fight record sends Rock into **the champion's own venue boss room** (Blizzard 16, Wind 13, Plant 17,
  Flame 16, Yamato 16, Tomahawk 17, Knight 17, Centaur 17). FIGHT_CTX makes the boss-death, clear and respawn paths
  return to the hub and skip YOU GET, the flags, the saves and the debrief; the return-to snapshot restores the hub's
  `$0340/$0650`, so the closed alcoves stay closed (tech §4.6). The hub reads `FIGHT_RESULT` and does its own
  bookkeeping: it sets the alcove's `$0340` bit and lights the line. Its state lives only in `$0340/$0650` and save
  flags (tech's HUB rule), never in `map_set` edits that would need to survive a fight.
- **Why the venues' own arenas**: the venue reworks (Wind's push, Centaur's tide, Tomahawk's HIGH NOON draw, Knight's
  battle log) live in their arenas, and both venue docs confirm that their arenas set up their own effects and undo their
  own map edits under the loader.

#### 5.2.2 Pair bouts

- Step on either alcove of a pair: **bout 1** loads that champion. When he falls, `FIGHT_RESULT = WIN` returns Rock to the
  hub **under the TAG! card** (a 90-f full-screen card that hides both warps), Rock's HP rises by 10 (a large life capsule
  shown on the card), and the hub at once loads **the partner** (bout 2) from the same alcove. No new loader feature is
  needed: the chain is the hub's own script. When the partner falls, Rock returns to the hub, both alcoves close and the
  pair's line lights.
- **SUPER copies** (the real champions watch from the stands, story S36): each copy runs that champion's v1.0 GP AI and
  systems' Table 1/2 row (own-weapon cells included); the arena in a **SUPER palette** (the fight record's palette byte);
  the panel name in story's style, `BLIZZARD.EXE` (consistency-22); and **pinch at HP 14 instead of 9**, from **the fight
  record's per-fight pinch byte**, which both venue docs' bosses read.
- A death in a bout returns Rock to the hub with that bout reset (both copies at full HP); finished pairs stay finished.
  HP carries from bout 1 to bout 2, so the card's +10 matters.
- Slots: each arena keeps its venue doc's boss-room cap (the boss + ≤ 3 boss-side objects).

#### 5.2.3 Boss: BASS β, duel 2: "THE FINAL" (fight `$23`, row 9)

**The arena: the Championship Ring.** A boxing-ring stage under spotlights in SUPER palettes, ropes on both sides. **The
ropes rebound**: touching one throws Rock (or Bass) back toward the centre at 3 px/f for 12 f (the vanilla knockback path
with 0 damage, a rope object; not a push zone). In v1.1 the ring is NO_TAG: a one-on-one final.

**What is new since the Riot.** SC6's armour **starts adapted** to the column used most in duel 1 (`BASS_ADAPT`), and
the hook says so (story S37). His COPY is now a **counter-copy**: the last weapon that hit him if it is one of his four
pre-drawn weapons, otherwise the one of the four you have used most (round 1's "all eight" is withdrawn: his set holds
four, R3.6).

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **SCOUT** | duel 1's, 5 shots with at most 3 alive |
| B | **DOUBLE-JUMP VOLLEY** | duel 1's |
| C | **COUNTER-COPY** | the ANALYZING pose (30 f, the icon tell) with the counter-copied weapon, fired twice |
| D | **ROPE RUN** | runs into a rope and rebounds across the ring at 4 px/f (contact 4), twice |
| E | **WALL KICK** | duel 1's D, off the ring posts |
| | Cycle | A, D, B, C, E (≈ 450 f) |
| Pinch (HP ≤ 9) | **SUPER β** | a 16-bit afterimage trail (3 ghost copies of his sprite on alternate frames, drawn by his own object); dash-cancels into the double jump and a downward volley; every recovery −25 % |

Slots: Bass + ≤ 3 shots = [9]. HP 28, systems row 9 + SC6 (+ COUNTER, Should). No help and no overdrive: the fair final.
At 0 HP he drops to one knee and teleports (story S37); his vow is saved for the podium (§6.1).

#### 5.2.4 Secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **PERFECT BRACKET** | the eight copies finished by **eight different scoring sources** (systems §6.4's columns: the buster, the charge, the punch, the 8 weapons…) | the finisher icons on the board | 30 | `FINISH EACH OF THE EIGHT COPIES WITH A DIFFERENT WEAPON. THE BOARD SHOWS WHICH YOU USED.` |
| b1 | **THE LOSERS' BRACKET** (13) | a ninth slot, `??`, on the board, over a sealed alcove with Break Man's emblem: in v1.0 it opens to **a full charge** (R4.2); with the partner (Should), he opens it too | the emblem and the `??` slot | envelope + E-tank | `THE SEALED ALCOVE UNDER THE ?? ON THE BRACKET BOARD OPENS FOR A FULLY CHARGED SHOT.` |
| b2 | **UNDEFEATED** | the four bouts and Bass with no death | a `W` streak counter on the board | E-tank + 30 | `CLEAR ALL FOUR BOUTS AND THE FINAL WITHOUT DYING.` |

**13, the losers' bracket**: a lounge with benches where the rejects you ACCEPTED in the Riot sit (all of them with
TALENT SCOUT; the reject sprites load with the room), a Vending Man who dispenses the E-tank once, a plaque (story's: the
losers' bracket gives everyone a second chance, except Mr. Y), and the envelope.

**Hooks** (story's words): W2-01 entering the hub (S36, Must); W2-02 each copy's bar fill: the real champion shouts from
the stands (S36; Should flavour, the first story trim); W2-03 the TAG! card (Must); W2-04 a finished pair (Should);
W2-05 Bass pre-adapted (S37, Must: SC6's tell); W2-06 Bass's defeat (S37, Must); W2-07 b0's secret line (Must); W2-08
and W2-09, the b1 and b2 lines (Should: generic lines in v1.0, R8.6).
**Respawns**: story §6.5's Wily table.

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | the Tomahawk copy's HIGH NOON draw | 24 f | 40 f | SC8's table (venues_a) |
| mash | none | — | — | — |
| timer | none | — | — | — |
| checkpoint | 00-07 (the moat) | 06 | + 03 | dormant checkpoint |
| secret step | b2 UNDEFEATED | no death | at most one death | `IFCASUAL` |

**HARD** (Should): the copies' HARD branches (the venue docs'); no +10 between a pair; Bass pre-adapted to your two
most-used columns.

**Homage moments**: the vanilla hub with a tournament bracket on its wall; `TAG!` and a champion leaping into his own
arena; Bass throwing your favourite weapon back at you; a rope rebound in the ring.

### 5.3 W3 WILY MACHINE 6.5 (`$1D`), base vanilla Wily 4 · Must

**Pitch.** The final round. **WILY MACHINE 6.5** (R3.6, design-24: vanilla's Wily Machine 6, retinted, "halfway to the
future") stands on a pseudo-3D floor that Wily claims rotates ("MODE 7!", story S38); then the Capsule, where Break Man's
gift can happen; then the escape.

**Tileset.** W3 (bank `$68` slot 1) = a copy of Wily 4's (`$2B:$89`; 177 blocks). Kept: the teal castle, the capsule
arrival, the dome-dispenser routine, and **the Wily Machine 6 art (`$BE`, the 202-tile slot at `$0360`), retinted**, with
a `6.5` decal (a few tiles). New: the checker floor texture (NT0 rows 24-29), the Capsule's SUPER badge, the trophy
re-skin, the escape's palettes. [new-art] M, Must.

| GP | From | The player does | Enemies | Tags |
|---|---|---|---|---|
| **00** | v00 | Arrival in the teleporter capsule (vanilla script 73 at `$8F95`: it waits for Rock's Y = `$77` and places him at X `$30`, Y `$53`). Wily's PA (story) | eye cannon `$54` | [engine-ok], Must |
| **01** | v01 | Down the hall (vanilla big WE). b1's tell: a **barred window** shows a trophy shelf behind the wall, under a skull-shaped keyhole that faces away | `$54` | Must |
| **02-03** | v02-v03 | **Mid-boss: THE TROPHY DISPENSER** (§5.3.1) | | Must |
| **04** | v04 | Red skull spearman `$70` and the E-tank (vanilla). **Checkpoint 1** (vanilla Wily 4 had none) | `$70` | Must |
| **05** | v05 | Shutter corridor; it loads the machine art into the `$BE` slot (vanilla init `$8FCF`). Wily's PA (story S38) | | Must |
| **06** | v06 | **Boss: WILY MACHINE 6.5**, then **the WILY CAPSULE SUPER** (§5.3.2-§5.3.3). Phase checkpoints | | Must |
| **07-0C** | new | **The escape** (§5.4) | | Must |
| **0D** | new | **Hidden room: WILY'S TROPHY ROOM** | | Must |

#### 5.3.1 Mid-boss: THE TROPHY DISPENSER (fight `$17`, mid-boss default row)

Vanilla Wily 4's screen 03 reuses Tomahawk's dome mid-boss routine (`$39:$8FBC` → `$861B`: a dispenser that drops
hard-hat walkers and rocks, HP 14). GP keeps the routine and re-skins it: **the stolen GP CUP** bolted onto the
dispenser, dropping mini-Metalls (at most 3 alive, [9]). The payoff: when it breaks, **the GP CUP falls intact** and Rock
picks it up (`THE GP CUP: RECOVERED`); he carries it to the podium (§6.1). [engine-ok routine] + [new-art] S, Must.

#### 5.3.2 Boss: WILY MACHINE 6.5 (fight `$24`, row 14)

**How it is built** (R3.6, scope-14). **Vanilla's Wily Machine 6 art (`$BE`), retinted**: BG in NT1, moved by the scroll
above the floor split. The vanilla floor strip (chain `$19`, scrolled through `$0678/$0679`) becomes **tech's
`RL_FLOOR8`**: the bottom 64 lines (176-239) in **8 bands of 8 lines**; band k (0 far, 7 near) gets the X scroll
`camX × s[k] + rot × k` and a Y scroll that picks a row of the checkerboard texture in NT0 rows 24-29, so the checks rush
past as the machine drives and **shear** when it "spins". `s[k]` runs from 0.25 (far) to 2.0 (near). Rock's collision
floor is a flat line at y 192; the bands are visual. **A GP controller** (family `$F8`, NOFREEZE: a BG boss) runs new
patterns on the vanilla art, with one position-tested hit box (the cockpit) in place of vanilla's several `$E9` boxes
(§0.8). Bands: 8 + the machine's split 1 + a window 2 = 11 (§0.11; consistency-27 resolved). [new-code] M (the patterns;
`RL_FLOOR8` is tech's), [new-art] S (the retint, the decal, the checker texture), Must.

**Panel** (story §5.4): NAME `WILY MACHINE`, its version field `6.5`, ENERGY `PROJECT SUPER` (consistency-6, R3.6).

Phase 1, **THE DRIVE** (bar 1, 28):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **CRUISE** | ≈ 240 f: the machine drives left and right (X scroll), the checker bands scrolling at their depths. Every 90 f it lobs a **mortar** at Rock's x: **the shell's shadow grows on the floor for 60 f** (the depth tell, kept without the size streams), then a 24-px blast (3 damage) |
| B | **HOP** | the Wily Machine's hop toward Rock (64 px, crush 6) and vanilla's ring shots (`$F0`, 3 per volley, at most 2 alive) |
| C | **CHARGE** | a horn blast (30 f), headlights on the floor where it will arrive (30 f), then a rush across the arena at 4 px/f (contact 6): jump its low front |
| | Cycle | A, B, C, B (≈ 600 f). Slots: the machine + ≤ 2 rings or a mortar = [8] |

Phase 2, **SPIN-OUT** (bar 2, refilled to 28; vanilla's face plate bursts and Wily is visible). It "rotates the floor":
the bands **shear** (each band's X offset grows with its depth), and the machine's AI **drags Rock sideways at 0.75 px/f
while he is grounded** (written by its own AI, as Wind Man's vanilla pull is, `$31:$8AFC`; not venues_a's VA-GUST, which
is Should). The checks start to shear 30 f before (the tell); the direction alternates.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **SPIN** | 180 f of rotation; one sweeping cockpit laser at standing height (a 30-f charge tell; jump it) |
| B | **SUPER HOP** | two hops toward Rock, each landing sending shockwaves both ways |
| C | **RING STORM** | 3 volleys of 3 rings, at most 2 alive |
| | Cycle | A, B, A, C. Slots [8] |
| Pinch (HP ≤ 9) | **DRIFT** | spins every 200 f and **reverses mid-spin** once; rings split in 2 |

**Damage** (systems row 14, the vanilla homage): SILVER.T **4/12 W**, KNIGHT.C 3/16 G, Y.SPEAR 1/32 R, PUNCH★ 4/24,
buster 1/32. **Phase checkpoints** [new-code] S, Must: on CASUAL and NORMAL a death in phase 2 restarts in phase 2, and a
death in the Capsule restarts at the Capsule; HARD restarts at phase 1.

**Should (v1.1, R3.6): THE APPROACH.** Round 1's drive-toward-camera phase returns as phase 1 with F-SIZES (S 64 / M 112
/ L 160 px wide, ≤ 150 tiles for L with the castle background blanked, feasibility-16) over `RL_FLOOR16` (19 bands with
the window): FAR CRUISE out of range (an `OUT OF RANGE` pop), CHARGE at the camera, REVERSE. 1.5 sessions here, plus
tech's F-SIZES and 16-band floor.

#### 5.3.3 Boss: THE WILY CAPSULE SUPER (fight `$25`, row 15), and Break Man's gift

The machine explodes (vanilla's sequence) and the Capsule rises (bar 3, 28). **How it is built**: vanilla's sprite
Capsule (`$F2`: palette-fade teleports, rings that split) [engine-ok] behind a GP controller (FRZ BOSS). **The twist:
afterimages**: from HP 14 each teleport leaves **2 decoys** in faded palettes (objects that die to one hit and never
fire); only the real Capsule's `SUPER` badge blinks (a small sprite: the tell).

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **FADE** | every 180 f: fade out 20, in 20, at one of 6 positions |
| B | **SPLIT RING** | a ring that splits into 2 after 40 f (3 damage); while decoys live, one ring that does not split |
| C | **AFTERIMAGE** (HP ≤ 14) | 2 decoys per teleport |
| D | **16-BIT BLAST** (HP ≤ 7) | a band of the screen **glows** over 40 f (a raster band; no flash, §0.9), then a screen-wide beam fires at that height: low (jump it) or high (stand or slide); 4 damage. The hit test is the controller's (Rock's y against the band) |

Slots: the Capsule + 2 decoys + 1 ring, or the Capsule + 2 ring halves = [9]. **Damage** (systems row 15): KNIGHT.C
**4/12 W**, SILVER.T 3/16 G, C.FLASH 1/32 R (vanilla's Capsule ignored C.FLASH: kept as a resist), PUNCH★ 4/24; CHAMP.B
**4/8 W** (SC11).

**BREAK MAN'S GIFT** (4MI's Proto Man and the Wily Buster, credited; `r4mi/wily.md` §4.5). [new-code] S, Must; the rule
is systems' SC11.

- **Trigger**: in the Capsule phase, Rock's HP < 6, and the gift not yet given in this W3 run; checked every 8 f.
- **Scene** (≈ 4 s): the screen darkens with yellow sparkles (a fade, not a flash); the whistle; the NPC Break Man beams
  in, says his line (story's), and throws an orb; one white flash (REDUCED: a fade). Nobody says Blues (R4.2).
- **Effect** (SC11): HP refilled, and Rock holds the **CHAMPION BUSTER** for the rest of the fight (HUD `WPN: CB`): 4/8
  on the Capsule, 3 shots on screen, and while it is held any hit of 2 or more on Rock becomes 1. A death after the gift
  keeps it on respawn (4MI's re-give).
- **The purist path**: never drop below 6 HP in the Capsule phase, and the gift never comes (b2, PURIST).
- *Could (with the doping bundle): if Break Man walked, Roll brings the orb (story's variant).*

**Defeat.** The Capsule cracks; **Wily falls out and kneels, begging** (vanilla's ending art, kept: story S39's dogeza).
The PA (4MI's self-destruct announcement, credited; story's words): Project SUPER will self-destruct. A red alarm (a
palette, not a flash); Wily scrambles into an emergency pod and drops through a floor hatch; the escape begins. The
dogeza has **no Mr. Y line**: the Mr. Y / Mr. Z alias gag is used once in the whole ending, at the arrest (§6.1, S41,
R8.5).

### 5.4 The escape: THE FINAL LAP (W3 07-0C) · Must

**The clock.** A HUD widget (DIGITS with tenths, round 1's F-CLOCK) shows `1:00.0` over the life bar; a referee's whistle
sounds, and it runs. At zero: `TIME!`, one red flash (REDUCED: a fade), and Rock dies. A death restarts at 07 with a
fresh clock, never at the machine.

**The mercy** (4MI's escape, credited). Attempts 1-3 get 60.0 s. **From the 4th attempt the clock reads 90.0 s, with a
small yellow `+30 INJURY TIME` beside it** (a LABEL widget). The game never explains it; at the podium the head judge
confesses (§6.1). 4MI's excuse was a lowered self-destruct output; GP's is the referee's stoppage time. [new-code] S,
Must.

**The collapse** (v1.0). As Project SUPER falls apart, the castle's palettes step down: 07-08 SUPER, 09-0A NES, 0B-0C
four greens. The 2A03 music keeps all its channels here (R8.3). If MMC5 audio ships (Could), only its two voices drop
out, at 09 and 0A (story S42: "already silenced when the castle fell"); the console's own channels are kept for the
ending's LIGHTS OUT, so its gag is not spent here. Round 1's
letterboxed POCKET screen and FW 1.0 (F-ERA in reverse) are Could, with W1.

| GP | Palettes | The player does | Hazards [n] |
|---|---|---|---|
| **07** | SUPER | Runs right through the collapsing hall | crumbling floors (the crumbling `$1D` collision through `COLL_GROUP`); explosions (orb clusters with a 20-f glow tell, 2 damage, at most 2) [7] |
| **08** | SUPER | Drops down a shaft | falling debris (shadows on the ledges are the tells; at most 2) [7]. Beat's pit rescue works here as everywhere (systems §10) |
| **09** | NES | Across a crumbling bridge | crumbling floors [5]. *Should, with H4: Flip-Top Jr., if freed, pops out of a vent and throws a large life and a large weapon energy* |
| **0A** | NES | **Up crumbling ladders** (R3.1, design-5: round 1's descending ceiling on Knight's chain is withdrawn): each rung crumbles 30 f after Rock leaves it (`map_set` through the repaint queue), so there is no going back down; debris falls past | debris ≤ 2 [7] |
| **0B** | greens | The last corridor: explosions ahead, the floor falling away behind (scripted crumbles) | explosions ≤ 2 [7] |
| **0C** | greens | **The exit hall**: Wily's emergency pod is jammed in the exit door, sputtering. Rock reaches it and pulls Wily out by the collar (controls lock; vanilla's "Rockman holds Wily by the collar" pose reused as a sprite pair), and **the floor gives way** under them both: white-out | [4] |

The white-out is the ending's first frame (§6.1), so there is no load seam. Round 1's **Rush catch** at 0B and **Break
Man holding the exit door** at 0C are deleted (R4.1: S40 is the catch, and the door variant is gone).

#### 5.4.1 W3 secrets

| Bit | Secret | How | Tell | Prize | Tier B hint (draft for story, Must) |
|---|---|---|---|---|---|
| b0 | **NO INJURY TIME** | escape within the first three attempts | the clock | 30 | `ESCAPE THE CASTLE IN YOUR FIRST THREE ATTEMPTS.` |
| b1 | **WILY'S TROPHY ROOM** (0D) | at 01, throw the **Super fist** past the skull keyhole behind the barred window: the fist flies through the bars and **hits the keyhole from behind on its homing return** (R3.1: a new tool, not a full charge) | the window and the keyhole that faces away | envelope + E-tank + 1-UP | `AT THE BARRED WINDOW NEAR THE START, THROW THE SUPER FIST PAST THE KEYHOLE. IT HITS ON THE WAY BACK.` |
| b2 | **PURIST** | beat the Capsule without Break Man's gift | the gift's trigger (HP < 6), which the gift scene states | 30 | `BEAT THE WILY CAPSULE WITHOUT FALLING BELOW 6 HP, SO BREAK MAN NEVER STEPS IN.` |

**0D, Wily's trophy room**: a cabinet of participation ribbons from every contest Wily ever lost (`1987: 2ND PLACE (OF
2)`, `1988: 2ND PLACE (OF 2)`, … `1993: DISQUALIFIED`), a plaque (story's: Dr. Wily's personal bests), the envelope, an
E-tank and a 1-UP.

**Hooks** (story's words): W3-01 the arrival (Should); W3-02 the first mortar shadow (Must: its tell); W3-03 the floor
shears (S38, Must: "MODE 7!" and Kalinka's "it's just scrolling in strips"); W3-04 the afterimages (Should); W3-05 the
gift (Must); W3-06 the clock starts (Must); W3-07 Wily jammed in the door (Must, the lead-in to S40); **WK-WM** the first
SILVER.T hit on WILY MACHINE 6.5 and **WK-WC** the first KNIGHT.C hit on the Capsule (story's ids, `EV_WEAK_FIRST`: the
two first-weakness lines, Must); W3-08 b0's secret line (Must); W3-09 and W3-10, the b1 and b2 lines (Should: generic
lines in v1.0, R8.6). Round 1's *"Is that... Blues?" / "OBVIOUSLY Blues."* at the gift is deleted (R4.2). **Respawns**: story
§6.5's Wily table; drafts (Should): *"You can't hit what you can't scale!"* / *"My capsule has afterimages. Does
yours?"*

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | the 16-BIT BLAST's glow; the mortar's shadow | 40 f; 60 f | 80 f; 90 f | `TIERVAL` |
| mash | none | — | — | — |
| timer | the escape clock (and its mercy) | 60 s (90 s) | 90 s (120 s) | `TIERVAL` |
| checkpoint | 00-05 | 04 | + 02 | dormant checkpoint |
| secret step | b0 NO INJURY TIME | the first 3 attempts | the first 4 | `IFCASUAL` |

**HARD** (Should): mortar shadows 45 f; CHARGE every 240 f; spins alternate every 150 f; afterimages from HP 20; the
blast's glow 30 f; the escape clock 50 s (90 s after three tries, unchanged).

**Homage moments**: a 1993 Wily Machine retinted to "6.5" over a rushing checkerboard; the floor shearing under Rock's
feet ("MODE 7!"); Break Man's gift in the dark, yellow sparkles and all; the castle draining from SUPER colour to four
greens as Rock runs; `+30 INJURY TIME`; dragging Wily out of his jammed pod by the collar.

---

## 6. The championship ending · Must (M8); the victory lap · Could

### 6.1 The scene order (R4.1, design-1)

**story.md owns the ending's words and scene list**; this is the staging, and it follows R4.1's order exactly. About 3
minutes plus the credits; START skips each scene after its first viewing (R3.8). [new-code] S, [new-art] S, Must.

| # | Scene (story) | Staging | Built from |
|---|---|---|---|
| 1 | **The escape** (§5.4) | it ends in the white-out at 0C, Rock holding Wily by the collar as the floor gives way | |
| 2 | **The castle pixelates** | outside, at the bay: the castle collapses into a skull-shaped cloud (4MI's, credited) that **pixelates**: a cloud in SUPER palettes, then chunky 8-bit blocks, then four greens, then one green pixel, then nothing | 3 small BG pictures + palette steps 8 f apart (no strobe, §0.9) |
| 3 | **Break Man catches Rock and Wily (S40)** | the whistle over the white; on the grass by the bay, the NPC Break Man sets Rock and Wily down. Rock's second and last *"Blues?"*; *"Break Man."*; he walks away as the whistle fades (story's words). In v1.0 the catch itself happens inside the white-out, and the scene uses the NPC's stand and walk frames; story's carry art is Should | NPC Break Man, Rock, vanilla Wily |
| 4 | **The arrest (S41)** | two Committee guards (recoloured vanilla robots) lead Wily away; **the ending's one and only use of the Mr. Y / Mr. Z alias gag** (R4.1, R8.5; story's words) | vanilla's Wily-behind-bars art kept |
| 5 | **The podium and Bass's vow** | the GP Stadium by day (TS_STADIUM): Rock on the top step holding the **GP CUP** he recovered in W3; **the champions applaud in pairs**, one pair at a time beside the podium, about 2 s each (SET-PARADE, two enemy palettes per pair, 0 new tiles; R8.6, art_audio's staging): Rock + a pair + Bass + the script + the text runner = **[6]**. *Should: all eight at once as a BG applause row (SET-PARADE converted to BG).* Bass β beams in at the pitch's edge for his vow (story's words; the "it won't be 8-bit" line may move here from S37), then leaves in a multicoloured beam (a palette cycle on his beam sprite, ≤ 3 changes per second). **If the escape mercy fired**, Cossack confesses the injury time (one POP; 4MI's "who lowered the output?" in tournament clothes). No Break Man on the roof | sprites over the stadium BG |
| 6 | **The CAPCOM TIMES (S44)** | vanilla's newspaper driver (`$3B:$A886`) and masthead; the headline art redrawn (story's `ROCKMAN WINS GP!!`); story's pages, with its fallback page **S44.4F** in place of a second alias gag (R8.5), then vanilla's `$95/$96` verbatim. **`$94` (the jailbreak line) is not reprinted** (R4.1): S02 quotes it | vanilla `$92-$96` slots; [new-art] S |
| 7 | **The credits** (§6.2) | the vanilla staff-roll engine with GP text and the DWNB cards | vanilla |
| 8 | **The rating (S46) and Break Man's debrief (S47)** | `meta.md` §6's screen, drawn over meta's judges' desk (R8.6; round 2's "stadium at dusk" is withdrawn) | meta |
| 9 | **LIGHTS OUT (S42)** | night, the empty stadium; Rock and Dr. Light in the stands (with Roll, Rush, and Beat if B-E-A-T is complete). The GP theme in **the lights-out arrangement** (art_audio's G37 LAST MATCH, Must). The six floodlight towers switch off one by one, and **each takes a music channel with it** through the D9 mute mask (tech §12.6; the game's one channel drop, R8.3): the MMC5 voices first if they ship and are on, then noise, triangle, pulse 2; **pulse 1 plays the melody alone**, and the last tower goes dark on its last note (consistency decision 25: story's cue table without its DPCM cue). Each switch-off is a palette step, not a flash | stadium BG at night + 4-5 sprites; [new-music] S (art_audio's) |
| 10 | **The sixth wing (S43)** | the Hall of Fame the next morning: H5's room 19, the 1993 wing now finished, the GP Cup under the WING 6 plaque (story's text). **Silent**: no music and no typing blips, so pulse 1 stays the last sound | H5's room 19 |
| 11 | **TO BE CONTINUED (S48)** | vanilla's `$88`, typed in silence; START → the title | vanilla |

- **The last sound the player hears is pulse 1 alone** (R4.1).
- Withdrawn from round 1 (R4.1, design-1): the order podium → newspaper → lights out → lap; Wily's pod crashing on the
  pitch; Break Man on the stadium roof; Break Man holding the escape door; the `$94` reprint.
- A cleared file can replay W3 and see the ending again (`meta.md` §6.1).

### 6.2 The v1.0 credits (R4.1 step 7, scope-22) [new-code] S, Must

Vanilla's own credits sequence (`rm6/fortress.md` §10), kept and fed GP data:

1. `STAFF`, then for each champion in vanilla's alphabetical order: **the champion fights in his own GP boss room**
   (vanilla's show: `$51` = his venue id and the room from a relocated 8-entry table: Blizzard 16, Centaur 17, Flame 16,
   Knight 17, Plant 17, Tomahawk 17, Wind 13, Yamato 16), for about 1,000 frames with no Rockman, then **his DWNB-41..48
   card strip, verbatim** (the boss walks in and the card types `DWNB-41 BLIZZARD-MAN / DESIGNER …`).
   This needs each reworked boss to run a **credits mode**: no player, so no quick-draw, no battle-log text, no grabs;
   it loops its patterns at an empty spot (a request to the venue docs and tech, §9). **Fallback**: a champion whose AI
   misbehaves skips his room segment and plays only his card strip. The M8 test runs all eight.
2. The scrolling staff roll on the starfield, through the language hook: the GP staff by role (story's), the original
   staff (vanilla's roll `$81-$86`, unchanged, under a `ROCKMAN 6 (1993)` header), special thanks (Rockman CX, Rockman 4
   Minus Infinity, and every fan who mailed Capcom a robot; story's words), and vanilla's `PRESENTED BY CAPCOM` (`$87`)
   last.
3. Then the rating (scene 8), not vanilla's TO BE CONTINUED, which moves to the very end (scene 11).

Music: vanilla's credits track. Story's ALL ENTRANTS roll (every enemy, "ELIMINATED") waits for the lap (Could).

### 6.3 The VICTORY LAP: the playable credits (`$1E`, meta 23) · Could (R0.3 item 8)

CX's playable staff roll (credited) as **one denser lap** of the stadium track (R3.8, design-20, scope-22): 8 screens of
TS_STADIUM with the credits written into the stadium (the scoreboard, banners, the infield grass, crowd card stunts) and
the champions along the track (SET-PARADE idle frames in front of a backdrop strip of each venue). Touch a champion for
his DWNB card, 4MI's `WINS n / LOSSES n` and a job title (story's). At the finish line, A runs another optional lap and
START finishes.

- Rock has 99 lives and 99 E-tanks and every weapon and form. With the partner (Should), Break Man runs beside him and
  **pause → CALL swaps who you control** (consistency-30 and R2.10: SELECT keeps its weapon meaning). A doped file's lap
  partner is Roll (consistency decision 40).
- Cameos: CROWD FAVOURITE's champions call Rock's name; TALENT SCOUT's accepted rejects sit in the front row under a `WE
  GOT IN!` banner; Flip-Top Jr. (H4) rides Eddie's cart; **Wily** rides a cage on a float pulled by Eddie (4MI's captive
  Wily), breaks out on the lap and is pinned by Rush and Beat; the finish is a **PHOTO FINISH** still, shown just
  before the rating (which draws over meta's judges' desk, R8.6).
- When it ships it replaces scene 7's staff roll (the cards play at the champions). Records: LAP TIME (Time Attack,
  Should). 6 sessions.

---

## 7. Mr. X Returns (`$1F`, meta 22) · Won't (v1)

R0.3 puts it in Won't (v1). Kept for a later release, in round 1's text (scratch copy): unlocked by `meta.md`'s U1.5
through a back door of H5's 1993 wing; **vanilla Mr. X Fortress 1, untouched** (legacy id `$08`'s layout and tileset,
music `$09`); a new fight, **MR. X (THE REAL ONE)** in his flying office chair (fight `$28`: SWIVEL, BUSINESS CARDS that
stick in the walls as platforms, HOVER CHARGE, the LAWSUIT pinch), furious that Wily borrowed his name twice.

---

## 8. Boss index, and the damage rows this doc uses

Every boss and mid-boss here, with its `meta.md` fight id, systems' GP_BOSSHIT row (systems §4.8) and its cells.
**systems §4.5 owns the numbers**; this table cites them cell for cell (W weak, G good, R resisted, "damage /
i-frames"). Unlisted columns take systems' defaults for the family (machines: buster 1/32, charge 3/32, punch 2/32,
PUNCH★ 4/24, weapons 2/24; robots: the champion scale; mid-bosses: the mid-boss default row).

| Fight | Boss | Stage | Tier | HP | Row | W | G | R | Special rules (visible code) | FRZ | Slots |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `$26` | Grand Pi-kun | Opening | Must | 14 | 8 | - | - | - | the valve only, while open; the body reflects; buster 1/30, charge 3/30 | BOSS | [8] |
| `$21` | Bass β, duel 1 | Riot | Must | 28 | 9 | - | - | - | SC6; copies his 4 pre-drawn weapons; NO DATA; the overdrive and the help capsule | BOSS | [9] |
| `$13` | Big Eye MK-VI | H1 | Must | 20 | 16 | - | - | - | | BOSS | [7] |
| `$1C` | Yellow Devil MK-VI | H1 | Must | 28 | 10 | C.FLASH 4/12 | Y.SPEAR 3/16 | PLANT.B 1/32 | the eye only; full blows knock pieces down; SC7 Could | NOFREEZE | [9] |
| `$15` | Kamegoro Maker MK-VI | H3 | Must | 20 | 16 | - | - | - | each turtle destroyed costs it 2 | derived | [9] |
| `$1E` | Gamma MK-VI, phase 1 | H3 | Must | 28 | 11 | W.STORM 4/12 | B.ATTACK 3/16 | C.FLASH 1/32 | the chin cannon only | NOFREEZE | [9] |
| `$1E` | Gamma MK-VI, phase 2 | H3 | Must | 28 | 12 | - | - | - | **SC5**: fists only (tap 2/30, PUNCH★ 4/12, the Super fist 3/20) | NOFREEZE | [9] |
| `$20` | Dark Man MK-VI | H5 | Must | 28 | 13 | F.BLAST 4/16 | PLANT.B 3/20 | SILVER.T 1/45 | WRONG NOTE: a full charge on the red note sets HP to min(HP, 14) | BOSS | [9] |
| `$00-$07` | the 8 SUPER copies | W2 | Must | 28 | 0-7 | Tables 1/2 | | | pinch at HP 14 (the per-fight byte) | BOSS | venue caps |
| `$23` | Bass β, duel 2 | W2 | Must | 28 | 9 | - | - | - | SC6 pre-adapted; counter-copy | BOSS | [9] |
| `$17` | Trophy Dispenser | W3 | Must | 14 | 16 | - | - | - | the vanilla routine | derived | [9] |
| `$24` | WILY MACHINE 6.5 | W3 | Must | 2 × 28 | 14 | SILVER.T 4/12 | KNIGHT.C 3/16 | Y.SPEAR 1/32 | the cockpit only; drags Rock in phase 2 | NOFREEZE | [8] |
| `$25` | Wily Capsule SUPER | W3 | Must | 28 | 15 | KNIGHT.C 4/12 | SILVER.T 3/16 | C.FLASH 1/32 | decoys die to one hit; CHAMP.B 4/8 (SC11) | BOSS | [9] |
| `$29` | Doc Robot MK-VI (AIR MAN copy) | H3 | Should | 20 | new (Air Man's) | PLANT.B 4/12 | | | through the fight loader (FIGHT_CTX kind 5) | BOSS | |
| `$14` | Picopico-kun MK-VI | H2 | Should | 10 blocks | 16 | - | - | - | the bar counts blocks | STD | [9] |
| `$1D` | Mecha Dragon MK-VI | H2 | Should | 28 | 18 | KNIGHT.C 4/12 | SILVER.T 3/16 | F.BLAST 1/32 | the head only | NOFREEZE | [9] |
| `$1F` | Cossack Catcher MK-VI | H4 | Should | 28 | 19 | Y.SPEAR 4/12 | W.STORM 3/16 | KNIGHT.C 1/32 | the dome only; C.HOPPER 8 HP | NOFREEZE | [9] |
| `$16` | Enker MK-VI | W1 | Could | 20 | 16 | - | - | - | the raised spear absorbs shots | BOSS | |
| `$22` | METALL 16 | W1 | Could | 3 × 14 | 20 | W.STORM 4/12 + FLIP | SILVER.T 3/16 | F.BLAST 1/32 | helmet down: full blows only | NOFREEZE | [9] |
| `$18-$1A` | the E1-E3 guests | Exhibitions | Could | 28 | 21 | RULE 4/12 | | | weapons 1/32 | BOSS | [7-9] |
| `$1B` | Maze Man | E4 | Won't | | | | | | | | |
| `$27` | `???` = the 1993 Wily final | TRUE GP | Could (with GP Rush) | 3 × 27 | vanilla `$EFE4` | | | | legacy id `$0F`, room 06, under RULESET 1993 (tech §4.2; consistency decision 40) | vanilla | vanilla |
| `$28` | Mr. X (the real one) | Mr. X Returns | Won't | | | | | | | | |

**Overrides of systems §4.5**: none of its cells. Additions, each a visible special case in the same list as systems'
SCs: Pi-kun's reflect outside the valve, Gamma's chin and cockpit boxes, Kamegoro Maker's turtle rule, Dark Man's WRONG
NOTE, the per-fight pinch byte of the SUPER copies, WILY MACHINE 6.5's drag. Systems tags the H2 and H4 rows "Could, with
H2/H4"; this doc and tech tier H2 and H4 Should (§9.2).

---

## 9. Cross-doc dependencies (requests to the owners)

### 9.1 `tech.md` (ids, memory, raster, CHR, the shared engines)

- **Accepted as binding**: the id map (§4.2), the tileset slots (§5.3: TS_STADIUM and H1 in bank `$66`, H3 and H5 in
  `$67`, W2 and W3 in `$68`, H2 and H4 in `$69`, TS_LAB and TS_ARCADE in `$6A`), ExRAM in mode 0 (§3.3), the 48-byte
  record, the 9-slot rule (§15.1: this doc's caps are re-cut, answering tech's question 5), the 24-band list.
- **Used, all Must**: `RL_FLOOR` (Pi-kun, the Yellow Devil, Gamma's room), `RL_FLOOR8` (W3), `RL_PALBAND` and
  `RL_PARALLAX` (W2, W3), the lighting service (the Riot's blackout), the map-edit service (timed blocks, the crumbling
  ladders, the scoreboard, the bracket board, F-PIECES), the HUD widgets (records below), the fight loader with FIGHT_CTX
  kind 1 (W2; the pair chain is the hub's own script, so no new loader feature), the boss-panel re-type (Dark Man), the
  NPC Break Man (family `$F7`), the attach state (none in v1.0; H4's claw later), the vehicle state (E3's CANNON, Could).
- **HUD widget records**: the Opening's LIMBO timer (DIGITS) and glove row (ICONROW 8, 2 × 4); the Riot's AUDITIONS
  (DIGITS + LABEL); H1's SCORE (DIGITS 4 + LABEL `00`) and ball count (icon + DIGITS 2); H5's letters (ICONROW 8, 2 × 4);
  the escape clock (DIGITS with tenths + LABEL `+30`).
- **Record fields per stage**: `CLASS` (SPECIAL for `$10/$11/$1E`, FORTRESS for `$16-$1D`, EXHIBITION for `$12-$15`);
  `FLAGS1` FORT for the H and W stages and **HUB for W2**; `COLL_GROUP` with the crumbling `$1D` for the Riot and W3 and
  group 0's F.BLAST plug for H1; `FORT_COL` rows 8-15 (systems §4.8); `PAR` (systems' placeholders); `HUD_ID`, `COMM_ID`,
  `CK_TABLE`, `FIGHT_ROW`; `NO_TAG` masks for v1.1 (§0.3); `ERA` and `OWNED` only with W1 and the Exhibitions.
- **New small requests**: (1) a stage flag that suppresses the water bubbles of floor type 8 (H5's low gravity; a spare
  `EFFECTS` or `VARIANT` column), [new-code] S; (2) the relocated 8-entry **credits room table** (`$51` + screen per
  champion, §6.2) and a **CREDITS bit** that the reworked boss AIs test for their no-player mode; (3) the 4-phase
  `alt_flip` groups for H1's appearing blocks (≤ 8 cells per id per screen, the build check).
- **FIGHT_CTX kind 5** ("the H3 room") is used only by Doc Robot MK-VI (Should).

### 9.2 `systems.md` (combat, economy, chips)

- **Accepted cell for cell**: the v1.0 rows of §4.5 (rows 8-17), SC5 with its practice beat and 1993 behaviour, SC6 with
  BASS_ADAPT, SC11 the CHAMPION BUSTER, M.BEAM's 64 px and max 2 (the H1 gap), FORMS.SUPER on the H3 dock with no YOU GET
  card, TAG rooms as full-charge doors, envelopes and ≤ 60 prizes per stage, the mid-boss and machine defaults, the FULL
  flag for the auditions, force beams flagged SPIKE (H2), the RULE column (the Exhibitions, Could).
- **Answers**: Bass β's four pre-drawn weapons are **B.ATTACK, F.BLAST, KNIGHT.C and SILVER.T** (its open question 3);
  in duel 1 he copies the owned ones and fizzles (`NO DATA`) when none are owned.
- **Requests**: list beside the SCs, as visible special cases: Kamegoro Maker's "a destroyed turtle costs it 2", Dark
  Man's WRONG NOTE (a full charge on the red note sets HP to min(HP, 14)), Pi-kun's reflect outside the valve, WILY
  MACHINE 6.5's grounded drag; the **Opening-lite keeps its hidden room and envelope** (+30 in §7's income model); the
  fortress prizes are 30 on b0 and 30 on b2 per stage, paid when the SECRETS bit is first set; **Air Man's row** (PLANT.B
  4/12 W) arrives with Doc Robot MK-VI (Should); tag H2 and H4 rows **Should** (systems says "Could, with H2/H4"; tech
  and this doc say Should).
- **The rating's partner-free test** (systems §9.5) is meta's T1 **SOLO RIOT**, RATEFLAGS b4: the Riot won without the
  help capsule (§2.4, R8.5).

### 9.3 `meta.md` (save bytes, bracket, events, debrief, rating)

- **SECRETS** for meta 0, 9, 14, 16, 18, 20, 21 (v1.0) and 10-12, 15, 17, 19 (later) as defined per stage here (b0
  showpiece 3, b1 room 2, b2 prize 2, b3 the Mr. X card 1, b4 the envelope). **No PRIZES bits** for these stages: the
  prize bolts key on SECRETS b0/b2 (consistency-19). Tier B hints are drafted here for story; tier A is Should.
- **RATEFLAGS**: b1 the card (H5 room 19; rating T14, Must), b2 RIVAL (the Riot's duel), and **b4 SOLO RIOT** (the
  Riot won without Break Man's help capsule: rating T1, R4.2, R8.5; round 2's "NO-CAPSULE" is this bit), set by Bass
  β's death when the capsule never dropped in that run. The capsule beat and the card stay Must.
- **Fight ids**: `$13` Big Eye, **`$15` Kamegoro Maker** (v1.0), `$17` the Trophy Dispenser; `$14` Picopico-kun
  (Should), `$16` Enker (Could), **`$29` Doc Robot MK-VI** (Should; round 1 had him at `$15`); `$18-$1A` the guests
  (Could), `$1B` Maze Man (Won't); `$1C` Yellow Devil, `$1D` Mecha Dragon (Should), `$1E` Gamma, `$1F` Cossack Catcher
  (Should), `$20` Dark Man, `$21`/`$23` Bass β, `$22` METALL 16 (Could), `$24` WILY MACHINE 6.5, `$25` the Capsule,
  `$26` Pi-kun, `$27` `???` (legacy `$0F`), `$28` Mr. X (Won't). The venues keep `$08-$12` (consistency-44).
- **W2's fight records** `$00-$07` need a SUPER palette and **a per-fight pinch byte** (the 10-byte record has no field
  for it: add one, or use flags b5-7).
- **Events**: EVENTS b4 the theft (S25); b6 the unmasking in H5's throne room; EVENTS2 b4 SUPER on the dock (S29 on the
  next map visit); b5 the join only with the partner (Should); b3 the Riot cleared.
- **Names**: meta index 9 and §3.5 become **HALFTIME RIOT** (R4.3). In v1.0 the Hall of Fame map shows H2 and H4 as
  closed wings (`CLOSED FOR RENOVATION`) and the 1993 door greyed out, and the Castle map shows W1 closed. The GP Rush
  lobby is the Opening's screen `$1D` (Could).

### 9.4 `story.md` (every word, the ending)

- **The Opening** (R4.4): S03, S04 (Roll by radio; Eddie's sign `PIT STOP OPENS AFTER THE CEREMONY`), S06, S08 within
  15 pages, as pop-up sequences at M5 (§1.1); S05 → the eight float lines; S07 folded into four judge lines and one
  scoreboard page; **S06 with no name spoken** (R4.2, R8.5), so its "BREAK MAN!" goes and Rock's first "Blues?" moves
  to the Riot's 0E (S20); S08's Break Man tip only after a death to Pi-kun; the Opening's one Wily gag.
- **The Riot**: S17 and S18 for the rejects (R4.3); S18 is merged into 06's help beat; S20 pages 1-2 play in place at 0E
  (Must), pages 3-6 with the partner (Should); Bass's "Who are YOU supposed to be?" / "Entrant number ten." at the block;
  at 0E **Rock's first "Blues?"** and the first in-stage "Break Man." (S20, R8.5).
- **The Hall**: S25 the theft; S27 plaques that describe and say BLUES (R3.3, R3.9); S28 per boss; S29 after the dock;
  **S30's tell is the scarf's colour (orange)**, not its side, and its walked variant is the v1.0 WRONG NOTE staging;
  S32 + S33 in H5's throne room with this doc's two masks; the Mr. X card's text (consistency decision 10).
- **The castle**: S36 with `BLIZZARD.EXE`-style copies; S37's pre-adapted line; S38 with WILY MACHINE 6.5 and the 8-band
  joke; S39's dogeza with **no Mr. Y line** (R8.5).
- **The ending** in R4.1's order (§6.1): S40 at the bay (Rock's second "Blues?"), S41 the arrest with the ending's one
  Mr. Y / Mr. Z alias gag (R8.5), the podium (the champions in pairs, R8.6) with Bass's vow and the injury-time
  confession, S44 without `$94` and with **S44.4F** (R8.5), the credits, S46-S47 over meta's judges' desk, **S42 with
  the MMC5 voices first (if they ship) and no DPCM cue** (Light says "Blues" once here), S43 and S48 silent.
- **New lines** (Must unless marked): the four lane judges, the scoreboard page, the SECRETS judge's `?` card, the
  master breaker, NO DATA (Should), the turtle factory (Should), the practice bag's FISTS ONLY, the WRONG NOTE's answering
  whistle, the TAG! card, the gap sign's second line, Wily jammed in the door.
- **Hook ids** OPN-, RIO-, H1-, H3-, H5-, W2-, W3- with triggers and tiers (each stage section), plus story's **WK-WM
  and WK-WC** (W3's first-weakness lines, §5.4.1); **b0 lines and every tell Must, b1/b2 lines Should** with story's
  generic lines in v1.0 (R8.6); 4 death drafts for the Opening and the Riot; respawn heckles from story's tables
  (wing-tagged drafts are Should).
- **Panels** within §5.1's fields (consistency-22), in vanilla's no-space style (R8.5): `GRAND PI-KUN`, `BASS β`,
  `YELLOW DEVIL`, `GAMMA MK-VI`, `BREAKMAN` / `DEFINITELY BREAKMAN` → `DARKMAN` / `BAD DISGUISES` → the third record
  with VENUE `EXPOSED BY A WHISTLE` (the WRONG NOTE), `WILY MACHINE` with version `6.5` and ENERGY `PROJECT SUPER`,
  `BLIZZARD.EXE` and kin, later `DOC ROBOT` / `COPY OF AIR MAN`.
- **H5's letter plates** spell `ROCKMAN5` in both languages (R8.5, story A-5.3).
- **Fact checks for Appendix A**: Rockman 3's turtle-dispensing machine and its "destroy the turtles" rule; Doc Robot's
  copies; Gemini Man's bouncing laser; the coin-shortage folklore; Rockman 8 (1996).
- **Text volume**: story's §10.4 counts are the single source (about 400 Must strings for the whole game, R8.4); this
  doc keeps no estimate of its own (round 2's ≈ 230 is withdrawn), and story's trim list is the reserve (§v1.0 scope).

### 9.5 `venues_a.md` / `venues_b.md` (staging, mechanics)

- W2 loads each venue boss room through the fight loader with a per-fight pinch byte; both docs accept it (their arenas
  set up their own effects and undo their own map edits).
- **New request**: a **credits mode** for each reworked boss (no player: no quick-draw, no battle log, no grabs; loop the
  patterns at an empty spot), read from tech's CREDITS bit, for the v1.0 credits (§6.2). Without it that champion's
  credits show is cards only.
- SET-PARADE (the Opening, the podium) uses each champion's vanilla idle frame (venues_b agrees); the lap's backdrop
  strips are Could.
- VA-GUST stays Should (venues_a): no Must use here (H3's magnet pull, the Riot's gust and H4's conveyors wait for it).
- The HALFTIME RIOT keeps the game's one lights-on-a-timer set piece (R3.1), as venues_a notes.

### 9.6 `art_audio.md` (the tile, byte and track budgets; R5.3's re-run)

- **Must art**: TS_STADIUM (L); SET-PARADE (8 idle frames, a composite, one 96-tile set); Pi-kun at one size (≈ 60 BG
  tiles) with the valve, puffs, confetti and hose; the judge, puck, bell, balls, deck and glove; VENDING MAN and CHEER
  MAN (≤ 8 frames each, composites); Bass β composited from Rock's sheet with 4 pre-drawn shots; the NPC Break Man
  composite (≈ 10 frames; the masked palette for S06); the MUSEUM third (M); the H1/H3/H5 contents; Big Eye (≤ 8 frames);
  the Yellow Devil (≈ 60 tiles); the Kamegoro Maker re-skin (S); Gamma's head and fists (≈ 100 tiles); Dark Man (≈ 64
  tiles, ≤ 16 frames) and his 40-tile disguise with the **orange scarf**; the letter plates; the W2 board (face icons and
  copied weapon icons) and the ring; the Wily Machine 6 retint, `6.5` decal and checker texture; the Capsule badge; the
  trophy-dispenser re-skin; the three pixelation pictures; the CAPCOM TIMES headline; the lights-out stadium. Also
  (R8.6): **Eddie as new art** (a composite, art's cast), **the trophy theft's claw** (S25; H4's Catcher reuses it), and
  the podium's champions **in pairs** from SET-PARADE (0 new tiles).
- **Should/Could art**: Pi-kun's three sizes; the podium's all-eight BG applause row (R8.6); H2 and H4 contents (the
  Mecha Dragon in the `$8B` budget, the Cossack Catcher, reusing the theft's claw); Doc Robot's overlay and Air Man's
  arena; Umbrella Man; the box-art figure; W1 (TS_LAB, METALL 16's eras,
  Enker); TS_ARCADE and three guests; the lap.
- **Music**: G00, G04 (stage entry and duels), the 2-second whistle jingle and **G37 LAST MATCH** (the lights-out
  arrangement, 2A03 stems) are Must (R5.2); G07-G13 and FINAL LAP (G15) and a RIOT remix are Should with vanilla
  fallbacks; G14 (POCKET, with W1: R8.3), G17, G18-G20 are Could. W2, W3 and the escape keep all 2A03 channels; the
  channel drop is LIGHTS OUT's (R8.3). **SFX**: knocks, the high striker's DING, the bell scale (H4), HIGH FIVE, the
  referee's whistle, the press shake, the claw's ding-ding (H4).
- One scarf tell (orange) for Dark Man's disguise (consistency-8).

---

## Lessons applied

| Source | Lesson | Where |
|---|---|---|
| CX 1 | One premise everywhere: a ceremony with lane judges, a riot of rejected entrants with auditions, a museum with plaques and a sixth wing for the game you are playing, a bracket of pair bouts, a match clock with injury time, a podium and a newspaper | all |
| CX 2 | A homage is a mechanic: a balloon that bounces shots, a high striker, a body that comes apart, appearing blocks, presses with slide gaps, a bouncing laser, a turtle machine, a fist you ride, a lying boss panel, a floor that shears | §1-§5 |
| CX 3 | The villain talks between lives (story's heckle table, a 1-bolt insurance YES/NO) | §0.5 |
| CX 4 | The partner as a second body, when the partner ships; until then he is a character who helps at fixed beats | §2.6, §5.3.3 |
| CX 5 | Reuse engine set pieces with one twist each (the §0.6 table) | §0.6 |
| CX 6 | Telegraph tools: the one required tool and the one required form each get a sign and a safe place to learn (H1 03, H3 10); every gate has a visible tell | §0.2, §4.1, §4.3.4 |
| CX (staff roll) | The credits are a show (v1.0: vanilla's rooms and cards) and later a level (the lap, Could) | §6.2, §6.3 |
| 4MI 1 | Weakness in the i-frames, flat damage: every row is systems' | §8 |
| 4MI 4 | Friends are mechanics: Break Man's help, block and gift; the help capsule; Beat's rescue; the accepted rejects on W2's benches; Flip-Top Jr. (Should) | §2, §4.4, §5 |
| 4MI 4 (escape) | Hidden mercy with an in-fiction excuse, revealed later: 60 → 90 s, confessed at the podium | §5.4, §6.1 |
| 4MI 5 | Behaviour-gated prizes and a hint per missed secret, never WIP text (tier B drafts for every secret) | all secrets tables |
| 4MI (Wily 4) | An unwinnable-feeling moment with a fair, concrete trigger and a purist path: the gift at HP < 6, PURIST | §5.3.3 |
| 4MI 7 | Make the theme mechanics: the "16-bit upgrade" is a floor that shears, a castle that drains of colour, a channel drop | §5, §6.1 |
| 4MI 9 | A boss rush on one fight table: W2 calls tech's fight loader | §5.2 |
| 4MI 11 | One generic raster list with a band budget per scene | §0.11 |
| RM6 1 | Use the attribute table rather than id arithmetic (tech's map) | §0.1 |
| RM6 7, 8 | Keep vanilla quirks: Wily 2's twin plug, the falling bells (H4), the Mr. X 1 skyline, Wily 4's capsule arrival, the newspaper's last pages, the Capsule's C.FLASH resist, TO BE CONTINUED | §0.6 |
| RM6 (credits) | The ending reuses the real boss rooms with the real AI as a credits show; GP keeps it | §6.2 |

## Risks

1. **Scope.** 70 Must sessions for 7 stages and the ending; many set pieces sit exactly at the 9-slot cap. *Mitigation*:
   the ledger re-estimate at M4 decides any cut (R8.1), with §v1.0 scope's fallback list ready; any later addition must
   give up a slot until M3 measures the OAM-builder gain.
2. **The credits mode.** Eight reworked boss AIs must run with no player for vanilla's credits show. *Mitigation*: the
   fallback plays only the card strips (§6.2).
3. **The Opening at M5 runs on text v1a.** Its scenes are pop-up sequences of 2 × 28 cells, which may feel clipped.
   *Mitigation*: ≤ 15 pages of short lines; story may move S03, S06 and S08 into the 4 × 28 window at M6.
4. **Sprite-per-line limits** in Gamma's fists beside Rock, Elec Man's beams (6 + 2), the floats (one per screen), Block
   Man's flat I piece (Could). *Mitigation*: sizes chosen for ≤ 8 per line; flicker priority to Rock and projectiles.
5. **Text volume.** These stages carry many Must lines (story §10.4 counts them; v1.0 has about 400 Must strings, R8.4).
   *Mitigation*: the b1/b2 secret lines are Should with generic lines in v1.0 (R8.6), and story's §10.4 trim list is the
   reserve.
6. **Three dispenser fights** (Tomahawk's bounty, H3's Kamegoro Maker, W3's Trophy Dispenser). *Mitigation*: different
   rules (turtles that drain the machine; a cup that falls intact), and Doc Robot replaces Kamegoro in v1.1.
7. **The 8-band floor's IRQ timing** on emulators and hardware. *Mitigation*: the floor is decoration (the collision is a
   flat line), so even 4 bands keep the fight and the joke.
8. **W2's loader round trips**: 8 arenas and two warps per pair under one card. *Mitigation*: tech's M7 gate (a hub →
   arena → hub round trip with the snapshot restored, for a win and a loss); the TAG! card hides both warps.
9. **No pixel artist** (R5.1): the NPC Break Man, Bass β, Gamma and Dark Man are composites and drafts. *Mitigation*:
   reuse first, frame caps, the art-acceptance gate per milestone.
10. **Facts in plaques and homages** (dates, the turtle machine, Doc Robot's copies, the coin shortage). *Mitigation*:
    folklore worded as folklore; story's Appendix A checks each one.
11. **Trademarks in the Exhibitions** (Could). *Mitigation*: parody names, descriptive plaques, guests designed as
    Rockman robots, the commentators' "can't say it" gag.

## Open questions

1. **meta**: the per-fight pinch byte's home in the fight record (routed as META-03).
2. **venues**: can every reworked champion run a no-player credits mode in M8, or does the v1.0 credits show only cards
   (routed as VENUES_A-03 and VENUES_B-04)?
3. **systems**: accept the Opening-lite's envelope (+30), and re-tag the H2/H4 rows Should (routed as SYSTEMS-07)?
4. **User** (RULINGS §7): a pixel artist would replace the composites (the NPC Break Man, Bass β, Gamma, Dark Man) first;
   the hardware target decides how hard the 8-band floor is pushed.

Round 2's questions closed in round 3: the channel drop (R8.3: W2, W3 and the escape keep all 2A03 channels; the drop
is LIGHTS OUT's), Rock's first "Blues?" (R8.5: the Riot's 0E, S20; S06 speaks no name), the dogeza's Mr. Y line (R8.5:
none; the alias gag is used once, at the arrest) and the NO-CAPSULE bit (R8.5: meta's RATEFLAGS b4 SOLO RIOT).

Round 1's open questions are closed: the ids (R1.2), the doped lap partner (Roll, Could), W1's eras without W1 (the
escape keeps palettes only; F-ERA is Could), the Super Adaptor's timing (after Gamma, no lending: consistency decision
16), the linear Hall (kept), the racing colours (Could), the `???` fight under a 1993 RULESET (Could, with GP Rush), Block
Man's name (kept, Could), Doc Robot's copy (AIR MAN, R3.1/R3.6), the 32-bit room (kept, Could).

## Changes in round 2

Finding ids refer to `review_feasibility_design.md` and `review_consistency_scope.md`; R-numbers to `RULINGS.md`.

| # | Change | Ruling / finding |
|---|---|---|
| 1 | Added **"v1.0 scope"**: 70 Must sessions (Opening-lite 8, Riot 10, H1 9, H3 10, H5 9, W2 8, W3 11, ending 5), milestones M5-M8, a dependency table where every v1.0 item rests only on Musts, the v1.1+ list and R0.3's fallback cuts. `tools/plan/tally.py` (fortress rows split into Must / Should / Could / Won't) and `tight.py` (fortress block, ending 4 → 5) updated | R0.1-R0.4; scope-1, scope-2, scope-3 |
| 2 | Re-tiered: Opening-lite, the Riot, H1, H3, H5, W2, W3 and the ending are Must; H2 and H4 Should; W1, E1-E3, the lap and H5's gravity flips Could; E4, Mr. X Returns and Gemini Rock Won't. Should and Could designs kept in place, marked | R0.2, R0.3, R3.7; scope-2, scope-9, scope-22 |
| 3 | Renumbered to tech's id map (Opening `$10`, Riot `$11`, E `$12-$15`, H `$16-$1A`, W `$1B-$1D`, lap `$1E`, Mr. X Returns `$1F`); legacy `$08-$0F` untouched; round 1's "keep ids 8-15" argument withdrawn | R1.2; feasibility-2, consistency-2, scope-12 |
| 4 | Tileset slots taken from tech §5.3; the MUSEUM third is a CHR set; "pages freed by moving layouts" withdrawn | R1.10; feasibility-17, consistency-9, scope-11 |
| 5 | **No ExGrafix in W2, W3 or the escape** and no extra CHR page; SUPER colour = palettes, bands and music; ExGrafix Could in W1's locked rooms (mode-2 fill, announcer held); the castle picture's bloom Could | R1.3; feasibility-1, consistency-1, scope-3 |
| 6 | W2 runs on tech's fight loader, FIGHT_CTX and the return-to snapshot; §5.2.1 retagged [new-code] M; the pair chain is the hub's script under the TAG! card; the hub's state lives in `$0340/$0650` | R1.7; feasibility-3, feasibility-19, scope-3 |
| 7 | **Every cap recounted with all occupied slots (cap 9)**, shown as [n]; fixes: the Riot's can throttle and 2 reject types, Bass's ≤ 3 shots and 3 flakes, one-controller BG bosses (Pi-kun, the Yellow Devil, Gamma, WILY MACHINE 6.5), the Devil's lasers only between crossings, Gamma's one shot at a time, Dark Man's ring object and 2-way split, the Capsule's decoys without split rings, H1's appearing blocks as BG cells, ≤ 3 presses, 2 crystal shards, the Mecha Dragon's 2 blocks, Paddle Man's 2 balls, one float per screen | R1.8; feasibility-4 |
| 8 | Raster band budget per scene (§0.11); W3 on `RL_FLOOR8` (11 bands with a window); E3's cellophane on attribute palettes | R1.9; feasibility-15, consistency-27 |
| 9 | One engine each: F-GRID deleted (the Exhibitions use `map_set` and T6); F-PIECES is tech's; F-CLOCK and every counter are HUD widgets on meta's stage counter; timed blocks and crumbling ladders use `alt_flip` / `map_set`; the claw uses the attach state; CANNON the vehicle state | R1.10; scope-10, scope-16, scope-17 |
| 10 | [engine-ok] tags that need code retagged (W2's hub, H5's bubble suppression, the Riot's gust moved to Should, the crumble as data on tech's record) | R1.14; feasibility-19 |
| 11 | A freeze class (`FRZ_KIND`) for every new object and boss | R2.2; feasibility-6 |
| 12 | Weapons are taps only in v1.0: Gamma's Updraft route, Time Stop on force beams, Wall Spear perches and the KNIGHT.C Hold catch are marked v1.1 | R2.4; scope-8 |
| 13 | No fortress chip; the rating's TEAM test is the Riot won without the help capsule (meta's new NO-CAPSULE bit); T3 left with the Exhibitions | R2.5, R2.7, R4.2; scope-3, scope-21 |
| 14 | Prizes ≤ 60 per stage (30 on b0, 30 on b2), paid on SECRETS b0/b2 with no PRIZES bits; one envelope per hidden room, the Opening's included | R2.7; consistency-19, consistency-10 |
| 15 | TAG rooms (the Riot's lockers, W2's losers' bracket) are full-charge doors in v1.0; H5's b2 has a no-partner form (WRONG NOTE), so doping (Could) removes no secret | R2.8, R4.2; design-8, consistency-38 |
| 16 | R2.9's CASUAL lever table filled in for every stage; round 1's one-off levers (the POCKET slide, the H1 ledge, the 6-press grab) re-expressed or dropped; HARD lists kept as Should in tech's format | R2.9; design-7, scope-19, consistency-15, consistency-16 |
| 17 | Plaques open on UP with B not held; the lap swaps through pause → CALL | R2.10; design-21, consistency-30 |
| 18 | **Gamma**: POWER required in phase 2 with the plaque as its tell and a no-risk **fist-ride practice beat** at H3 10; SC5's 1993 behaviour cited; **head and fists only** (≈ 100 tiles), phase 1's hit box the chin cannon | R2.11; design-3, consistency-12 |
| 19 | **Repetition swaps**: H4's compactor → Dust Man's conveyors; the escape's 0A → crumbling ladders; H4's dark rooms → a flash-bulb photo puzzle (the Riot keeps the one timed dark set piece); H3's Gemini Rock → the laser; Doc Robot → Should, copying AIR MAN; hidden-room keys by new tools (H3's M.BEAM stair, W3's Super fist return, H4's Balloon, H2's W.STORM, W1's 16-BIT MODE); one collect-N per stage (the Riot's six fuse boxes → one master breaker) | R3.1; design-5 |
| 20 | Names: HALFTIME RIOT; story's entrant numbering on the board and lockers; WILY MACHINE 6.5; plaques describe, never name third-party games, and say BLUES; panel strings inside story §5.1's fields; the third-party ghost-name death line deleted | R3.3, R3.9, R4.3; design-10, design-14, design-23, design-24, consistency-22, consistency-29 |
| 21 | Flash audit (§0.9): the floodlight flicker becomes a dim and buzz; the 16-BIT BLAST a glow band; Pi-kun's pinch one palette change; the towers' switch-offs palette steps; REDUCED fades through tech's service | R3.5; design-13 |
| 22 | Bosses at v1.0 size: Pi-kun one size (sizes Should); WILY MACHINE 6.5 on vanilla art and 8 bands (the approach, F-SIZES and 16 bands Should); Bass copies 4 pre-drawn weapons (B.ATTACK, F.BLAST, KNIGHT.C, SILVER.T) with NO DATA; Doc Robot Should; the H3 mid-boss is KAMEGORO MAKER, a re-skinned vanilla dispenser; METALL 16 Could | R3.6; scope-13, scope-14, feasibility-16 |
| 23 | The Exhibitions redesigned as one lobby + one rule-boss arena each, with their own hidden-room trick or none; RULE column; E4 Won't; the coin-shortage plaque worded as folklore | R3.7, R3.8, R3.9; scope-9, design-20, design-23, consistency-18 |
| 24 | Replays: scenes skippable after the first viewing; the lap is one lap with more optional | R3.8; design-15, design-16, design-20 |
| 25 | The H1 gap: 96 px = one 64-px beam plus a 32-px jump; HARD 112 px | consistency-17 |
| 26 | **Break Man**: the disguise is respected; every "OBVIOUSLY Blues" line deleted; S06 masked with no name; first named at the Riot's 0E with S20's pages 1-2 in place (3-6 Should); the help beat merged with S18; the NPC composite Must; Dark Man's disguise a 40-tile set with the orange scarf | R4.2, R1.12; design-2, consistency-7, consistency-8, scope-15, feasibility-14 |
| 27 | **The ending** in R4.1's order; the door-holding, roof and Rush-catch variants deleted; Wily caught at the exit door; no `$94`; the lights-out drop MMC5 first, no DPCM, pulse 1 last; S43 and S48 silent | R4.1; design-1, consistency-6, consistency-13 |
| 28 | **The Opening** within 15 scene pages: one intro (S02's crawl), NEW GAME to the tunnel, rules folded into four lane judges (DAMAGE, TIME, STYLE, SECRETS) and one scoreboard page, float lines only, one Wily gag, pop-up sequences on text v1a at M5, Break Man's tip only after a death, the pit stop after the ceremony | R4.4, R1.4; design-4, consistency-7 |
| 29 | The Riot's crowd is the rejects; the Mr. Y YES/NO is the 1-bolt insurance; heckles follow story's single P1 rule | R4.3; consistency-25 |
| 30 | Hooks are ids, triggers, tiers and intents; 4 death drafts per stage; tier B hints Must, tier A Should (kept in the scratch copy); ≈ 230 Must strings estimated | R4.5; scope-18 |
| 31 | Art: composites first (SET-PARADE, Bass β and Break Man from Rock's sheet), face icons on the W2 board, one size per BG boss, the R5.3 art list | R5.1, R5.3; consistency-8 |
| 32 | Music on art_audio's list: G00, G04, the whistle and G37 Must; the tributes G08-G12 Should (fallback `$09`); FINAL LAP Should (fallback `$18`); round 1's five-arrangement Hall theme withdrawn | R5.2; scope-23, consistency-13 |
| 33 | FORMS.SUPER set on the H3 dock with no YOU GET card | consistency-28 |
| 34 | Vehicles are not forms (E3's CANNON); the GP Rush lobby is the Opening's screen `$1D` | consistency-36, consistency-31 |
| 35 | Fight ids: `$15` is Kamegoro Maker; Doc Robot moves to `$29`; the venues keep `$08-$12` | R3.6; consistency-44 |
| 36 | The escape's downgrade is palettes only (F-ERA Could); the MMC5 voices drop in the escape if they ship; the console's channels are kept for LIGHTS OUT | R1.3, R4.1; scope-3 |
| 37 | W1: the half-damage rule dropped, the blind jump's ledge 8 px inside the window, opaque POCKET borders, ExGrafix only in locked rooms | R3.9, R1.3; design-19, feasibility-20 |
| 38 | VA-GUST is Should (venues_a), so no Must use: the magnet pull, the roof gust and the conveyors wait; WILY MACHINE 6.5's drag is its own AI; the ring ropes are knockback | R0.4 |
| 39 | Round 1's open questions closed (the doped lap partner, the linear Hall, Block Man, the 32-bit room, the `???` fight) | consistency decision 40 |
| 40 | Mr. X's card text and the doped headline are story's words | consistency decision 10 |

## Changes in round 3

Request ids refer to `reconcile.md`'s "fortress.md" table; R-numbers to `RULINGS.md` §8. No session figure changed: the
fortress Must stays 70 (M5 8, M6 10, M7 28, M8 24).

| Id | Outcome | Section | Note |
|---|---|---|---|
| FORTRESS-01 | applied | §0.5, §2 (pitch), §2.6, §9.4 | Rock's first "Blues?" is at the Riot's 0E reveal (S20), the second at S40; S06 speaks no name; Light says "Blues" once, in S42 (R8.5) |
| FORTRESS-02 | applied | §4.5.2, §9.4 | Panel names in vanilla's no-space style: `BREAKMAN` / `DEFINITELY BREAKMAN` → `DARKMAN` / `BAD DISGUISES`; the WRONG NOTE types a third record with VENUE `EXPOSED BY A WHISTLE` (R8.5) |
| FORTRESS-03 | applied | §0.5, §1.7, §4.1.3, §4.3.7, §4.5.3, §5.2.4, §5.4.1, §9.4 | b0 lines and every tell Must; the b1/b2 lines (OPN-08, OPN-12, H1-08/09, H3-11/12, H5-10/11, W2-08/09, W3-09/10) Should, with story's generic lines in v1.0 (R8.6) |
| FORTRESS-04 | applied | v1.0 scope, §4.5.3, §9.4 | H5's b0 is **ROCKMAN5**: plates R-O-C-K-M-A-N-5 in both languages; hint and CASUAL row renamed (R8.5) |
| FORTRESS-05 | applied | §0.5, §5.4.1, §9.4 | WK-WM (first SILVER.T hit on WILY MACHINE 6.5) and WK-WC (first KNIGHT.C hit on the Capsule) registered as W3's first-weakness hooks, Must |
| FORTRESS-06 | applied | v1.0 scope (dependencies), §0.3, §2.4, §9.2, §9.3 | NO-CAPSULE renamed **SOLO RIOT**, RATEFLAGS b4, rating T1 (R8.5); the capsule beat and Mr. X's card (T14) stay Must; the Castle map draws W1 closed beside H2/H4. Stage ids already match tech §4.2 and fight ids meta's table (checked) |
| FORTRESS-07 | already | §2.4, §9.2; §4.3.5, §8; §4.1 (0B) | Bass β's four pre-drawn weapons are B.ATTACK, F.BLAST, KNIGHT.C, SILVER.T; Gamma's phase-1 row (11) is the chin cannon's hit box (phase 2's row 12 the cockpit); H1's gap is 96 px = one 64-px beam + a 32-px jump, with at most two beams (HARD 112 px) |
| FORTRESS-08 | applied | §1.2, §6.1 (scene 5), §9.6 | The podium's champions applaud in pairs (SET-PARADE, 0 new tiles); the all-eight BG row is Should (R8.6) |
| FORTRESS-09 | applied | §1.2, §4.0, §4.4.1, §6.1 (scene 8), §6.3, §9.6 | Eddie is new art (a composite); the rating draws over meta's judges' desk (the lap's photo finish now precedes it); the theft's claw is Must art and H4's Catcher reuses it (R8.6) |
| FORTRESS-10 | applied | §6.1 (scene 5) | The one v1.0 scene over the cap, the podium (12 occupied slots), is re-cut to [6]; every other v1.0 screen and pattern was rechecked at ≤ 9; Paddle Man (§3.2, Could) was already [9]; this doc has no Reaplet alarm |
| FORTRESS-11 | applied | v1.0 scope, §0.5, §0.12, §5.0, §5.3.3, §5.4, §6.1, §9.4, Risks | R8.3: W2, W3 and the escape keep all 2A03 channels, the drop is LIGHTS OUT's, MMC5 voices Could; R8.5: the alias gag only at the arrest (S41), no Mr. Y line at the dogeza, the CAPCOM TIMES uses S44.4F; R8.4: story §10.4's counts cited, round 2's ≈ 230 withdrawn |
| R8.1 | applied | v1.0 scope, §4.6, Risks 1 | "If the budget falls below 440" becomes "if the M4 re-estimate asks for cuts" (the ≈ 450 Must is accepted); this doc's per-milestone share stated for RULINGS §6 |
| R8.3 | applied | §9.6 | G14 POCKET noted Could, with W1 |
| R8.6 | applied | Risks 5 | The text risk now leans on the b1/b2 lines being Should and story's trim list as the reserve |
| R8.3, R8.5 | applied | Open questions | Round 2's questions 1-3 and the NO-CAPSULE half of 4 closed; the rest point at their reconcile.md ids |
| — | applied | header | Status set to round 3 |
