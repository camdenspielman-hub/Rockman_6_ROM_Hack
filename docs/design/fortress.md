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
| **SET-PARADE** | the eight champions' vanilla idle frames, about 12 tiles each, packed into one 96-tile enemy-area set: a composite of vanilla art (R5.1, counted R). Reused at the ending's podium (§6.1) | [new-art] S, Must |
| Vanilla sprites | Eddie (peeking from his stall); the NPC Break Man composite (tech §7.9, masked palette); Bass β (§2.1) for S06 | — |

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
  glove icons, 2 rows of 4). Eight in one run → the scoreboard flashes nothing: it *types* `CROWD FAVOURITE` (OPN-08).
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
| OPN-08 | the eighth high five | Must (secret line) | CROWD FAVOURITE |
| OPN-09 | first high five | Should | up top! |
| OPN-10 | reaching the entrant board | Should | entrant ten is... masked |
| OPN-11 | first valve hit | Must (the boss's first-weakness line) | hit the valve! |
| OPN-12 | 1C found | Must (secret line) | the judges saw that |
| OPN-13 | PERFECT WARM-UP | Must (secret line) | four tens |

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
**Break Man** steps in front of his last shot; on the roof he names himself, and the Committee's Rule 9 lines play.

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
never drops below 6 never sees it. **Winning without it is the rating's TEAM test** that replaces T1 in v1.0 (R4.2,
systems §9.5): meta records it as a new RATEFLAGS bit, NO-CAPSULE.

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
| **The reveal and Rule 9** | 0E | Bass is gone; Break Man stands at the roof's edge. Kalinka asks who that is; he names himself, **"Break Man."**: the first time the name is spoken (R4.2), and nobody says Blues. Then **S20's Rule 9 pages 1-2 play in place** (R4.2): the Committee rules that a sponsor's interference invokes Rule 9, and the other four matches resume. He leaves over the roof's edge | S20 pages 1-2 (Must); pages 3-6 (he joins, the CALL row, the banner) are **Should** with the partner and play at this spot. They set FORMS.TAG and EVENTS b5 (`meta.md`) |

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
over its W, grabs the **GP CUP** and carries it off to an island museum, the **HALL OF FAME**. The trophy theft is the
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
eye (the first-weakness line, Must); H1-06 the first piece knocked down (Must: b2's tell); H1-07…09 the secret lines
(Must). **Respawns**: story §6.5's Mr. Y heckles; wing-tagged drafts (Should): *"My Yellow Devil was the hardest boss of
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
phase 2, Mr. Y at the controls (S28, Must); H3-09 the uppercut (Must); H3-10…12 the secret lines (Must). **Respawns**:
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
(`RL_FLOOR`); **the twist**: the cabin also **travels along a crane rail** (the X scroll), and a sprite claw drops from it
and **grabs Rock** (tech's attach state, input rule "struggle"). The arena is a prize pit with two prize capsules (a
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
| **08** | v08 | **CRYSTAL MAN'S CRYSTALS**: two ceiling emitters drop crystal orbs in turn (one orb alive at a time, one every 60 f); an orb shatters on the floor into **2** shards (2 damage) | eye cannon `$54` [9] | | [new-code] S, Must |
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
(NAME ≤ 12, SPECIALTY ≤ 19; glyphs `0-9 A-Z . - ? ! ' β` and space; consistency-22): NAME `BREAK MAN`, SPECIALTY
`DEFINITELY BREAKMAN`, re-typed as NAME `DARK MAN`, SPECIALTY `BAD DISGUISES`. There is no "?" on the card: the panel
lies with a straight face (story writes the record).

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
(the Must jingle), and the disguise falls at once: his HP drops to 14 if it is higher, and the panel re-types with one
extra line (story's words). This is story S30's "walked" staging, used in v1.0 because the partner is Should. *With the
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
| b0 | **MEGAMAN V** | collect the eight letter plates M-E-G-A-M-A-N-V (Rockman 5's own letters, which built Beat): six on screens both routes share (03, 05, 08, 0F, 12, 14) and two on the branch (16-18); an ICONROW widget (2 rows of 4) under the life bar fills in | the letters glow; the first is on the main path at 03 | 30 | `FIND THE EIGHT LETTERS M-E-G-A-M-A-N-V IN THE 1992 WING. THE SHORTCUT HAS TWO.` |
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
Must); H5-09…11 the secret lines (Must). Round 1's "That's not Blues!" / "Obviously not Blues." are deleted (R4.2).
**Respawns**: story §6.5; wing-tagged drafts (Should): *"My Dark Man is a master of disguise."* / *"Blues' castle! It
was mine all along! Like everything!"*

**CASUAL levers**:

| Lever | Where | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | b2, the red note | 20 f | 40 f | `TIERVAL` |
| mash | none | — | — | — |
| timer | b1, the knock window; the arrows' interval | 6 s; 120 f | 9 s; 120 f (the arrow is a ride, not a timer) | `TIERVAL` |
| checkpoint | 00-09, 0A-11 | 09, 11 | + 05, + 0D | dormant checkpoints |
| secret step | b0 MEGAMAN V | 8 letters | the letters stay collected after a death | `IFCASUAL` |

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

After the unmasking, the W stages' heckler is Wily (story's Wily table, §0.5). If the budget falls below 440 (R0.3), this
scene moves to H3's ending (Mr. Y unmasks in Gamma's cockpit).

---
