# Rockman 6 GP: the non-venue stages (fortress.md)

Owner: design-fortress. Status: **round 2**, revised against `RULINGS.md` (binding; it overrides `BRIEF.md`), the four
critic reports (`review_feasibility_design.md`, `review_consistency_scope.md`), `crossrefs.md`, and the round-2
revisions of `tech.md`, `systems.md`, `venues_a.md` and `venues_b.md`. Scratch: `build/revise/fortress/` (round 1's
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
| **H5 ROCKMAN 5** (§4.5, §4.6) | M7 | Mr. X 4 remix; Star Man's low gravity; the gravity rooms' low-gravity form; Crystal Man's crystals; the Super Arrow ride; the MEGAMAN V letters; the 1993 wing and Mr. X's card; **Dark Man MK-VI** with the lying boss panel and the WRONG NOTE exposure; **Mr. Y's unmasking** (two masks) | 9 |
| **W2 BRACKET OF DOOM** (§5.2) | M8 | Wily 3 remix in SUPER colour (palettes + bands + music, R1.3); the hub as a bracket board; **pair bouts through tech's fight loader and FIGHT_CTX** (R1.7) into each champion's own arena; 8 SUPER copies; the Championship Ring and **Bass β duel 2**; the losers' bracket room | 8 |
| **W3 WILY MACHINE 6.5** (§5.3, §5.4) | M8 | Wily 4 remix; the Trophy Dispenser and the GP Cup; **WILY MACHINE 6.5** on vanilla Wily Machine 6 art, retinted, over an **8-band floor** (R3.6); the Wily Capsule SUPER and Break Man's gift (SC11); **the escape** with crumbling ladders (R3.1), injury time and Wily caught at the door; Wily's trophy room | 11 |
| **The ending** (§6) | M8 | R4.1's scene order: the castle pixelates, Break Man catches Rock and Wily, the arrest, the podium and Bass's vow, the CAPCOM TIMES (no `$94`), **the vanilla staff-roll engine with GP text and the DWNB cards**, the rating and Break Man's debrief, LIGHTS OUT, the sixth wing, TO BE CONTINUED. The last sound is pulse 1 alone | 5 |
| | | **Total** | **70** |

Round 1's `tally.py` gave these stages 94 Must sessions and `tight.py` 69. The +1 against `tight.py` is the ending: the
v1.0 credits keep vanilla's show of each champion fighting in his own room, and the eight reworked boss AIs need a
credits mode with no Rockman and a test for it (§6.2; the fallback, card strips only, costs nothing more).

**Milestones** (RULINGS §6). The Opening-lite lands at **M5**, before text v1b (M6): its scenes run as **pop-up
sequences under a script lock** on text v1a, and story may move them into the 4 × 28 window at M6 (§1.1). The Riot
lands at M6 after text v1b. H1, H3 and H5 land at M7 after `bgboss.py` (R1.13), F-PIECES and the `$9B` audit. W2, W3 and
the ending land at M8, after the fight loader (M7) and with `RL_FLOOR8`.

**Every v1.0 item rests only on Must items** (R0.4, scope-3):

| v1.0 item | Rests on (all Must) |
|---|---|
| Opening-lite | tech: stage record and ids `$10+` (M5), TS_STADIUM slot (§5.3), `RL_FLOOR`, text v1a, the commentator bus; systems: scorecard rows, attack bytes `$11-$14`, GP_BOSSHIT row 8; meta: the first bracket hand-off, the debrief, SECRETS m0; story: S03, S04, S06, S08 within 15 pages; art: TS_STADIUM, the parade set (8 vanilla idle frames), Pi-kun at one size |
| HALFTIME RIOT | tech: text v1b, the palette-flash and lighting service (§8.5), `COLL_GROUP` (the crumbling `$1D` group), the NPC Break Man (family `$F7`), the boss panel extension; systems: SC6, LATCHSRC's FULL flag, the help capsule as a pickup; meta: RATEFLAGS b2 RIVAL and a new NO-CAPSULE bit; story: S17-S20 for the rejects; art: two rejects, Bass β composited from Rock's sheet with 4 pre-drawn shots, the NPC Break Man composite; music: G04 and the whistle jingle (both Must, R5.2) |
| H1, H3, H5 | tech: `bgboss.py`, F-PIECES on the map-edit service, `alt_flip`, the HUD widget module, the `$9B` audit before SUPER, the attach state (the arrow), the boss panel re-type; systems: M.BEAM (64 px, max 2), SC5, the Super Adaptor, FORMS.SUPER on the dock, the mid-boss and machine defaults; meta: EVENTS b4/b6, EVENTS2 b4, the Hall of Fame map, RATEFLAGS b1 (the card); story: S25-S33; art: the MUSEUM CHR third and the wing contents |
| W2 | tech: the fight loader, FIGHT_CTX, the return-to snapshot (M7.2), `RL_PALBAND`; meta: fight records `$00-$07` with a SUPER palette and a pinch byte; venues: each boss reads the per-fight pinch byte (both venue docs accept it); systems: SC6 pre-adapted from BASS_ADAPT |
| W3 and the escape | tech: `RL_FLOOR8` (M8), the HUD widget (the clock), the map-edit service (crumbling ladders), the lighting service; systems: SC11 CHAMPION BUSTER, Beat's rescue; story: S38-S40 |
| The ending | tech: the D9 mute mask (Must, R5.2), the vanilla newspaper and staff-roll engines through the language hook; meta: the rating and the debrief; story: S40-S48; music: G37 LAST MATCH (Must; art_audio adds it, consistency-13) |

**Not in v1.0.** Kept below in place as v1.1+ material, each marked:

| Tier | Items (R0.3 cut-line item) |
|---|---|
| **Should (v1.1+)** | **Item 2, the tag partner**: Break Man's join pages and banner (S20 pages 3-6), the TAG opening of the Riot's and W2's rooms, H5's TWO BREAK MEN, the H1/H3/H5 tag pockets, the `NO_TAG` masks. **Item 3**: HARD poke lists and boss branches for every stage (kept in tech §5.5's format, counted in systems' HARD line). **Second set pieces**: H1's Guts lifts, H3's magnet pull (with venues_a's VA-GUST, itself Should), H5's Wave Man geysers, the Riot's roof gust and UMBRELLA MAN, W3's drive-toward-camera approach (F-SIZES + the 16-band floor), Grand Pi-kun's three sizes, **Doc Robot MK-VI** (he copies AIR MAN through the fight loader, R3.6), Bass's COUNTER (SC10). **Item 5**: H2 and H4 |
| **Could** | Item 5: **W1 Upgrade Lab** with F-ERA, its locked ExGrafix rooms and the POCKET arrangements (R1.3); the escape's eras; the ExGrafix bloom of the castle picture. Item 6: **the Exhibitions E1-E3** as single arenas (R3.7). Item 8: **the victory lap**, one lap (R3.8). H5's gravity flips. The doped variants (with the PART/TURBO bundle) |
| **Won't (v1)** | E4 Maze (R0.3); Mr. X Returns (R0.3); Gemini Rock (R3.1 keeps the laser); the escape's Rush catch (S40 is the catch, R4.1); the door-holding and roof Break Man variants (R4.1); every "OBVIOUSLY Blues" line (R4.2); the Museum's plaque gallery (meta's Museum is Won't) |

Estimates for the rest (`tally.py`, area `fortress`): Should 30.5 (Pi-kun's sizes 1, Riot 1, H1 1.25, H3 3.25, H5 1.25,
W3 1.5, H2 11, H4 11), Could 36 (W1 14, the escape's eras and the bloom 1, gravity flips 3, E1-E3 4 each, the lap 6),
Won't 11 (E4 9, Gemini Rock 2).

**If the budget falls below 440** (R0.3), cut next, in this order: merge H5's unmasking into H3's ending (Mr. Y unmasks
in Gamma's cockpit; about −2 here and −1 text), make W2 a single-arena Bass final (no pair bouts; −3), and reduce the
Opening to 3 tutorial screens (lanes 01-03, then Pi-kun; −2).

**Text** (R4.5). These stages need about **230 Must strings** for story's v1.0 budget of about 350 for the whole game:
the Opening about 40, the Riot about 35, H1/H3/H5 about 75 (with S25-S33 and the plaques), W2/W3 about 35, the ending
about 45 plus the credits roll. That is over budget once the venues' about 170 are added; story trims (§9.4 lists the
candidates: the float lines become Should first, then the champions' W2 shouts and the H-wing exhibit lines).

---

## 0. Rules shared by these stages

### 0.1 Ids, layouts, tileset slots

**Ids are tech's** (R1.2, tech §4.2; feasibility-2, consistency-2, scope-12). Round 1 put H1-W3 in the vanilla fortress
ids 8-15; that is withdrawn. The legacy ids `$08-$0F` stay vanilla (the regression movies, the `???` fight, the 1993
data rows), and every new stage reads the stage-attribute record (tech §4.4) with `CLASS` = SPECIAL, FORTRESS or
EXHIBITION. The meta index (`meta.md` §1.8) is unchanged.

| Stage | Id | Class | Base layout (vanilla, copied and remixed) | Screens / 32 | Tileset slot (tech §5.3) | Vanilla art kept | Music (art_audio's ids, R5.2) |
|---|---|---|---|---|---|---|---|
| Opening-lite | `$10` | SPECIAL | new | 13 + room + lobby (Could) | **TS_STADIUM** (bank `$66` slot 0) | Mr. X 1's night skyline and moon (set `$9D`) behind the plaza | G00 GRAND PRIX MARCH (Must); boss `$0C` |
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
  tour goes H1 → H3 → H5.
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
  `H2-`, `H4-`, `W1-`, `E1-`… when they return).
- **Deaths**: 4 death lines per stage in v1.0 (R4.5), in story §6.4's tables; this doc lists 4 recommended drafts per
  v1.0 stage. In H1-W3, story's rule applies (consistency-25, its decision 26): **one P1 heckle per respawn replaces the
  death line**, from story §6.5's Mr. Y table (H wings) and Wily table (W stages); round 1's per-wing heckle drafts are
  offered as wing-tagged variants (Should).
- **The YES/NO heckle is the 1-bolt respawn insurance** (R4.3, systems §7): round 1's fake "MR. Y PERFORMANCE
  PARTNERS" commercial is withdrawn.
- **Break Man's disguise is respected** (R4.2, design-2). Nobody calls him Blues: only Rock says "Blues?" (twice, in
  story's S06 and S40), and Light says the name once, at the very end. Every round-1 "OBVIOUSLY Blues" line is deleted.
  His name is first spoken in-stage at the Riot's 0E reveal; in the Opening he is the masked entrant 10 (story's S06).
- **The Wily gag plays once per act, with varied wording** (R4.4, R3.9): once in the Opening, once at the trophy theft
  (S25), once at the unmasking (S33, "WE KNOW").
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
| **Platforms that carry Rock** | Riot floats, H5's Super Arrow, H3's practice fist and Gamma's fists | §1, §4.3, §4.5 | the vanilla lift contact (`$38:$8F96`, class 2/5/9); tech's attach state only where a pose changes (H4's claw, Should) |
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
refights. Round 1's "HALL OF FAME theme in 5 arrangements" is withdrawn for art's G08-G12.

---
