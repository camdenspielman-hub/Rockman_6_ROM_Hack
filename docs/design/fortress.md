# Rockman 6 GP: the non-venue stages (fortress.md)

Owner: design-fortress. Status: **v1, being written** (the container can restart, so this file is rewritten as it
grows; sections still marked TODO are not done). Scratch: `build/design/design-fortress/`.

Scope: every stage that is not one of the 8 Heritage Venues.

| § | Stage | Meta index (`meta.md` §1.8) | Tier (BRIEF §9) |
|---|---|---|---|
| 1 | **OPENING CEREMONY**: intro, tutorial, Grand Pi-kun | 0 | Must |
| 2 | **SEMIFINAL RIOT**: Bass β duel 1, Break Man's reveal | 9 | Must |
| 3 | **EXHIBITIONS** E1 Block Man, E2 Paddle Man, E3 Invader Man, E4 Maze Man | 10-13 | Should |
| 4 | **HALL OF FAME** H1-H5: the Rockman 1-5 wings, the MK-VI bosses, Mr. Y's unmasking | 14-18 | H1, H3, H5 Must; H2, H4 Should |
| 5 | **SUPER WILY CASTLE** W1 Upgrade Lab, W2 Bracket of Doom, W3 MODE-7 Machine and the escape | 19-21 | W2, W3 Must; W1 Should |
| 6 | The **championship ending** and the **playable victory lap** | (23) | Must; the lap Should |
| 7 | Mr. X Returns (appendix) | 22 | Could |

Binding inputs: `BRIEF.md` (overrides `PLAN.md`), `docs/research/{rm6,cx,r4mi}/SUMMARY.md` and their topic docs.
Weapon specs, chips and the combat tables are `systems.md`'s; the saves, the bracket, the debrief and the rating are
`meta.md`'s; dialogue is `story.md`'s (every quoted line here is a **draft** for it); ids, banks and the engine are
`tech.md`'s. Where this doc needs something from them it is a **proposal**, collected in §9.

Notation, as in the venue docs: vanilla screens are **vNN** (from `docs/research/rm6/img/maps/` and
`rm6/fortress.md`), GP screens are plain **NN**. Tags per BRIEF §8: **[engine-ok]**, **[new-code]**, **[new-art]**,
**[new-music]**; size **S/M/L**; tier **Must/Should/Could**. Frame counts are at 60 Hz. Boss HP is in bar units (28 =
a full bar; vanilla stores 27 and dies below 0).

---

## 0. Rules shared by these stages

### 0.1 Ids, base layouts and tileset slots (proposal for `tech.md`)

**The key idea: the Hall of Fame and the Castle are exactly eight stages, and vanilla has exactly eight fortress
slots.** H1-H5 and W1-W3 therefore keep the fortress ids 8-15. Every vanilla "is this a fortress" test (the five
`AND #$08` sites, the three `CPY #$08`, the `$EFE4` fortress damage table indexed by stage−8, the fortress game-over
rule) stays valid for them with no code change, and only the 6 truly new stages (Opening, Semifinal, E1-E4) need the
stage-attribute table's class field from day one (BRIEF §7.2). The layouts are new copies in new banks (the vanilla
data stays where it is, untouched, so Mr. X Returns can still load vanilla Mr. X 1).

| Stage | Proposed id | Base layout (vanilla, copied and remixed) | Screens used / 32 | Tileset slot (new) | Vanilla art kept | Music |
|---|---|---|---|---|---|---|
| Opening Ceremony | 16 | new | 13 (+1 hidden) | **TS_STADIUM** | Mr. X 1's night-city skyline and moon (set `$9D`, v00-v02); the intro pictures `$53-$5A` | new: GP FANFARE (cutscene), GP STADIUM (stage), `$10` boss intro kept |
| Semifinal Riot | 17 | new, on the Opening's blocks | 14 (+1) | TS_STADIUM, night/riot palettes | as above; Mr. X 1's skyline behind the roof arena | new: RIOT (a minor-key remix of GP STADIUM); new: BASS β |
| E1-E4 | 18-21 | new | 6-7 each | **TS_ARCADE** (shared; one CHR third per exhibition) | none (simple new tiles: the cheap-art rule of PLAN §3.3) | new: one 30-s loop per guest |
| H1 ROCKMAN | 8 | **Wily 2** (19 screens) | 17 (+1) | TS_H1 = copy of `$2A:$89` + MUSEUM third + MM1 third | Wily 2's pink machine blocks and circuit walls, its disappearing-block objects `$8F`, its F.BLAST twin plug | new: HALL OF FAME (shared theme, 5 arrangements) |
| H2 ROCKMAN 2 | 9 | **Wily 1** (24 screens) | 21 (+1) | TS_H2 = copy of `$2A:$80` + MUSEUM + MM2 | the castle exterior, the long fall, the updraft blowers `$36/$41`, the Power pocket, the dinosaur art set `$8B` (re-skinned) | HALL OF FAME (MM2 arrangement) |
| H3 ROCKMAN 3 | 10 | **Mr. X 3** (18 screens) | 18 (+1) | TS_H3 = copy of `$2F:$92` + MUSEUM + MM3 | the red gear machinery, the pistons, the warning light thread | HALL OF FAME (MM3) |
| H4 ROCKMAN 4 | 11 | **Mr. X 2** (18 screens) | 18 (+1) | TS_H4 = copy of `$2F:$89` (about 100 free tiles) + MUSEUM + snow | the machine panels, the falling bell row, the pod-column BG technique | HALL OF FAME (MM4) |
| H5 ROCKMAN 5 | 12 | **Mr. X 4** (25 screens) | 24 (+1) | TS_H5 = copy of `$2B:$80` (159 of 256 blocks used) + MUSEUM + MM5 | the grey stone castle, the crates and drones, the open pit branch | HALL OF FAME (MM5) |
| W1 Upgrade Lab | 13 | new | 20 (+1) | **TS_LAB** (from Wily 3's base set `$A2`, 91 free tiles) + ExGrafix data | Wily 2/3's machinery | new: UPGRADE LAB in three arrangements (pocket / 2A03 / 2A03 + MMC5) |
| W2 Bracket of Doom | 14 | **Wily 3** (17 screens) | 19 (+1) | TS_W2 = copy of `$2A:$92` + bracket board | the moat, the teleporter, **the hub and its rush tables** | `$0B` Wily theme kept; refights `$0C`; new BASS β (final) |
| W3 MODE-7 Machine | 15 | **Wily 4** (7 screens) + escape | 13 | TS_W3 = copy of `$2B:$89` + TS_LAB's blocks for the escape | the capsule arrival, the dispenser routine, the Wily Machine slot and floor split | `$0B`, `$18` Wily Machine kept; new: FINAL LAP (escape) |
| Victory lap | 23 | new, on TS_STADIUM | 8 (loops) | TS_STADIUM | the credit cards `$71-$80`, the roll `$81-$88` | new: VICTORY LAP |
| Mr. X Returns | 22 | **vanilla Mr. X 1, untouched** | 22 | vanilla `$2C:$92` | everything | `$09` |

Notes:

- The four empty or spare tileset pages (`$2B:$92`, `$2D:$92`, and the pages freed by moving the eight fortress
  layouts) are enough for TS_STADIUM, TS_ARCADE and TS_LAB; the H/W slots are **copies** of vanilla pages in new
  banks, so a remix never touches a vanilla table.
- **The MUSEUM CHR third** (about 96 tiles, swapped into `$0A00-$0FFF` by screen exits exactly as vanilla's `$91/$95/$98`
  sets are) is shared by all five wings: marble floor trim, velvet ropes and posts, plaque frames, glass display
  cases, the wing doors with year numbers, a donor wall. One art job, five uses. [new-art] M Must.
- Free tile ids were checked against `rm6/fortress.md` §1-§8: Mr. X 2 references 157 of 256 tiles, Wily 4 101-199,
  Wily 3 71-123, Wily 2 141-157, so H4, W2, W3 and H1 have room; Mr. X 3 (255) and Wily 1 (254) are full, so H3 and
  H2 drop vanilla blocks they no longer use (the Mr. X 3 tank, the Wily 1 jester head) to make room.

### 0.2 What a main route may require

Venues follow `systems.md` §2.4 (no form, alt, synergy or Break Man on a normal exit). The fortress gets one more
rule, because by then the player's kit is known:

- **A main route may require only tools the player is guaranteed to own at that point and that also work under the
  1993 rules** (`systems.md` §13.3 keeps M.BEAM and the Super Adaptor in 1993): the buster's full charge (the Opening
  teaches it), the **Magnet Beam from H1's display case on**, and nothing else. Every punch, form, alt, synergy, weapon
  and Break Man gate is on optional content.
- Every required tool is **handed over on the main path right before it is needed, with a sign** (CX lesson 6).
  There is exactly one such gate in the whole fortress: H1 07, the Magnet Beam gap, which is also the homage
  (Rockman 1 could not be finished without the Magnet Beam).
- Exhibitions lend their vehicles ("COMMITTEE LOANER JET", the `venues_a.md` §1.2 precedent), because they can be
  unlocked before the 4th win.

### 0.3 Structure, checkpoints, saves

- **Two mid-stage checkpoints plus the boss shutter** in every H/W stage (vanilla had one, and Wily 4 none). A
  checkpoint is the vanilla `LDA #s / JMP $8416` script routine [engine-ok]. Multi-phase finals get **phase
  checkpoints** (§5.3): a death in a later phase restarts in that phase on CASUAL and NORMAL.
- **Saves**: after every stage (`meta.md` autosave 4). Vanilla never saved fortress progress; GP does.
- **The fortress maps** (`meta.md` §3.4): the Hall of Fame floor plan and the Castle picture replace vanilla's Mr. X
  map and Wily Fortress picture (`$39:$ACD4-$ADFE` path animation kept), each with a 3-row menu: `NEXT WING` /
  `REPLAY` (any cleared H/W stage) / `BACK TO BRACKET`. [new-code] S, [new-art] M, Must.
- **RETIRE** is allowed everywhere except the Opening (`meta.md` §3.7).
- **Break Man** (once he has joined, §2.6) can be called everywhere except during a boss bar fill and in stages or
  screens flagged NO TAG: the Opening (he has not joined), the exhibitions' vehicle screens, the W1 GB section (he
  "isn't compatible"), the escape.

### 0.4 Secrets in non-venue stages

`meta.md` §1.6 lets the stage owner define SECRETS bits b0-b4 for non-venue stages, with the same weight rule. This
doc uses one layout everywhere, so the debrief and the scorecard can treat these stages like venues:

| Bit | Meaning | Weight (`systems.md` §6.2) | Reward |
|---|---|---|---|
| b0 | **the stage's showpiece secret** (a mastery or homage act) | 3 | 30 bolts (paid once) + a Museum entry |
| b1 | **hidden room**: exactly one screen, off any route, with a visible tell | 2 | a sponsor envelope (+30, `systems.md` §7), a 1-UP or a tank, a gag plaque |
| b2 | **behaviour-gated prize** | 2 | per stage (a friend, a fixed item, the Mr. X card; never a chip: the chip list stays at 21) |
| b3 | H5 only: **Mr. X's business card** (`meta.md` T14) | 1 | RATEFLAGS b1 |
| b4 | the envelope taken (as for venues) | - | - |

- Every predicate, its `require` byte and both hint tiers are listed per stage. Tier A is a riddle about the homage,
  tier B an instruction (`meta.md` §4.3). Nothing ships as WIP text.
- Fortress envelopes: 8 (Opening, Semifinal, H1-H5, W1). `systems.md` §7 allows them ("fortress.md may add some");
  that is +240 bolts over a full game, inside its completionist model's slack.
- Showpiece and prize bolts (30 per b0) are **venue-prize-style** money: paid once per save, tokens on replays
  (`systems.md` §6.7).

### 0.5 Voice: commentators and Mr. Y's heckles

- **Commentators** (Cossack C, Kalinka K): ≤ 2 lines, toggleable, never during a prompt (BRIEF §5.5). Each stage
  lists its event hooks and a 6-line death rotation; then the generic table.
- **Mr. Y heckles between lives** in H1-W3 (BRIEF §5.5, CX lesson 3, CX Light 6's round table). On each respawn a
  line from the stage's 6-line table, then a shared 12-line table. One line in the shared table is a **YES/NO** (the
  CX s12 homage, made harmless): *"Tired? Sign with MR. Y PERFORMANCE PARTNERS! YES / NO"*. YES plays a 3-s fake
  commercial ("MR. Y: FOR ALL YOUR WORLD-CONQUEST NEEDS") and Kalinka: *"Don't sign anything!"*. No mechanical effect;
  TURBO is only at the booth (`systems.md` §9.4). After the unmasking (§4.7) the heckler is "DR. WI- I MEAN MR. Y"
  until W3.
- Shared heckle drafts: *"My museum thanks you for the donation of one life."* / *"In 1987 you had infinite
  continues. I've fixed that."* / *"The judges are taking notes. I bribed them to."* / *"Did you know respawning is
  an 8-bit habit?"* / *"Again! Encore! My sponsors love this part."* / *"I have your death on tape. Sixteen-bit tape."*

### 0.6 Vanilla fortress tech, reused with one twist each (CX lesson 5)

| Vanilla tech (`rm6/fortress.md`) | Where it was | GP stage | The twist |
|---|---|---|---|
| BG boss in NT1, **vertical** scroll, floor strip from NT0 (chain 7) | Mr. X 2 pod column | Opening: **Grand Pi-kun** (§1.6) | The BG **inflates and deflates**: three pre-drawn sizes streamed into CHR-RAM (the CX giant-Light technique) |
| BG boss in NT1, horizontal scroll, floor strip (chain 7) | Wily 2 walker | H1: **Yellow Devil MK-VI** (§4.2) | The body **comes apart**: its 12 pieces are erased from NT1, fly across as sprites, and are painted back on the far side; pieces you knock down become floor blocks |
| BG boss in NT0, floating, multi-split (chain `$16`) | Mr. X 4 X Crusher | H2: **Mecha Dragon MK-VI** (§4.3) | The floor is **Heat Man's appearing blocks** (sprite platforms on a rhythm), and in pinch the dragon dives into the pit and comes up through a block |
| Static BG boss, one head hit box, body reflects | Wily 1 Mechazaurus | H3: **Gamma MK-VI** (§4.4) | Its **rocket fists** are sprite platforms that rise back to its head: you ride Gamma's own fist up and punch it in the face |
| BG boss in NT1 with vertical-scroll technique (chain 7) | Mr. X 2 | H4: **Cossack Catcher MK-VI** (§4.5) | The pod column becomes a **crane cabin on a rail** (X and Y scroll) with a sprite claw that **grabs Rock** (mash to escape) |
| Robot Master framework: intro `$93`, room controller `$94`, the typed boss panel `$3C:$81B1` | the 8 RMs | H5: **Dark Man MK-VI** (§4.6) | **The boss panel lies**: it types "BREAK MAN", then re-types "DARK MAN MK-VI" when the disguise falls |
| BG tank + sprite pilot, floor strip (chain `$1A`) | Mr. X 3 Metonger Z | W1: **METALL 16** (§5.1) | The BG body **upgrades between bars**: GB palette, NES palette, then ExGrafix colours and MMC5 audio |
| Data-driven rush: hub, alcoves, tables `$39:$8EC8/$8ED2/$8EDC`, rooms `$09+id`, palette `$9A+id`, ninth teleporter | Wily 3 | W2: **Bracket of Doom** (§5.2) | **Pair bouts**: an alcove starts a two-champion bout; the first one's life capsule is replaced by a "TAG!" warp into the partner's room |
| Wily Machine: BG in NT1, floor split with a scrolled strip (chain `$19`), three bars in one room | Wily 4 | W3: **MODE-7 Machine** (§5.3) | The floor strip becomes a **16-band perspective floor** (per-band X and Y scroll), and the machine drives toward the camera in three streamed sizes |
| Sprite capsule with palette-fade teleports | Wily 4 | W3: **Wily Capsule SUPER** (§5.3) | It teleports with **afterimage decoys**, and it is where **Break Man's gift** (4MI's Wily Buster pattern) happens |
| Mr. X reveal: pod, typed speech, flight path (`$39:$8DE9/$8E04`) | after Mr. X 4 | after H5: **Mr. Y's unmasking** (§4.7) | Two masks: Y comes off to show X, X comes off to show Wily |
| Credits: each RM plays its real AI in its own room, then its card | the ending | the **victory lap** (§6.3) | You run past them on a playable lap, and touching each plays its card plus your WINS / LOSSES (4MI) |

Kept vanilla quirks (BRIEF §6, rm6 lesson 8): Wily 2's twin F.BLAST plug (one blast opens both) in H1; the falling
bell row in H4; the Mr. X 1 skyline; the scripted capsule arrival of Wily 4 in W3; the CAPCOM TIMES jailbreak line;
`TO BE CONTINUED`.

### 0.7 Shared objects and engine pieces this doc adds

New objects use the generic "GP object" id + sub-id once `tech.md` fixes it (`venues_b.md` X-GPOBJ; only about 30
type ids are free). Labels are prefixed **F-**.

| Id | What | Used in | Tags |
|---|---|---|---|
| **F-PLAQUE** | A museum plaque: stand in front, press UP, the T2 text window types 2-4 lines (JP/EN). Touching it also stamps it in the Museum's plaque gallery (`meta.md` §9.5) | H1-H5, W2 hub, Opening | [new-code] S, Must (T2 is shared) |
| **F-CASE** | A glass display case that holds a pickup; breaks open on touch (a glass-shatter SFX), plays the weapon-get screen (chain `$17`) when it holds a weapon | H1 (M.BEAM), museum gags | [new-code] S, [new-art] S, Must |
| **F-PIECES** | The "BG body that comes apart" engine: an object owns a w×h grid of 16×16 BG pieces in NT0/NT1; it can erase a piece (4 tiles through the VRAM buffer), turn it into a flying sprite, and paint it back elsewhere. ≤ 3 pieces in flight | Yellow Devil, Picopico-kun, the Opening's scoreboard gag | [new-code] M, Must |
| **F-SIZES** | Streams one of 2-4 pre-drawn size frames of a BG boss into CHR-RAM over 2-4 frames (CX's giant Light) | Grand Pi-kun, METALL 16, MODE-7 Machine | [new-code] M, Must |
| **F-GRID** | A WRAM cell grid (up to 16×14) mapped to BG tiles and collision, with a paint queue (≤ 8 cells per frame) and row operations (clear, shift) | E1 well, E2 bricks, E3 formation and bunkers, E4 dots | [new-code] M, Should (with the exhibitions) |
| **F-CLOCK** | A countdown in seconds and tenths drawn with sprites above the life bar (4MI `$7689-$768B`), with a time-out handler | the escape, E-stage bonus timers | [new-code] S, Must |
| **F-ERA** | The W1/escape "era" switch: palette tier, ExGrafix on/off, audio tier, letterbox on/off, firmware flags (slide/charge/forms) | W1, W3 escape, ending | [new-code] M, Should |
| Text window, director, push zones, timed blocks, input mirror | as defined by `venues_a.md` (T2, T1-lite, VA-GUST, VA-TIMED) and `venues_b.md` (T6, T7, X-WRAP, X-LABEL, X-METER) | many | shared |

### 0.8 Lag

About 10 live objects fill a frame (`rm6/engine.md` §8). Every set piece below states its cap, counting 3 player
shots. BG bosses are cheap by construction (the body is nametable art; only hit boxes and projectiles are objects),
which is why every MK-VI uses one.

---

## 1. OPENING CEREMONY (meta 0, id 16)

**Pitch.** The Grand Prix opens at the GP Stadium. A short intro reuses vanilla's own pictures (with one letter
changed), then the stage is the opening ceremony: a warm-up course that teaches the moves and the judging, a parade of
the eight champions, and the mascot, Grand Pi-kun, sabotaged by Mr. Y's "upgrade". It is the CX opening lesson
applied to a tutorial: the stage teaches by being the event, not by stopping the game.

**What it teaches, in order:** walk and jump (01), slide (02), the charge shot (03, and the boss), ladders and the up
exit (04), the commentator window (00), the scoreboard rows (the four lane judges), hidden rooms and their tells (02),
behaviour-gated prizes (the parade), a boss bar and a weak point (Pi-kun). The player owns the buster only. No form,
no weapon, no Break Man, no RETIRE.

### 1.1 The intro (before READY) [engine-ok] + text, Must

Vanilla's intro bytecode (`$3D:$BD00`) and its raster chains 8/9/A/B are reused with new scripts. Total ≈ 55 s,
START skips after the first line.

| Step | Picture | Text (EN draft; JP in the text pass) |
|---|---|---|
| 1 | black | `IN THE YEAR 20XX AD...` (vanilla, kept) |
| 2 | vanilla's tournament pictures `$57-$5A` | *A year ago, the 1st World Robot Championship ended in disaster: its sponsor, "Mr. X", was Dr. Wily in a moustache.* |
| 3 | the GP stadium (new, 1 picture) | *This year the Committee tries again: the GRAND PRIX! Eight venues, each a tribute to a legend of the games.* |
| 4 | vanilla's four pictures `$53-$56` (2 robots each), unchanged | *The eight champions return, rebuilt by the fans who designed them.* |
| 5 | vanilla's Mr. X picture, **with the X repainted as a Y** (a handful of tiles; the rest is the 1993 art) | *And at the last minute, a ninth sponsor registered an entrant...* `MR. Y` |
| 6 | Light's lab (new, small) | Rock: *"...That's Dr. Wily."* Light: *"That's definitely Dr. Wily."* Rock: *"Let's go, Rush!"* (vanilla's `$4A` line, kept) |

The repainted Y is the running gag's first screenshot. [new-art] S (the Y, the stadium, the lab).

### 1.2 Tileset and art

| Item | Content | Tags |
|---|---|---|
| Slot **TS_STADIUM** | New 16×16 metatile and 32×32 block tables; also used by the Semifinal, the GP Rush lobby (`meta.md` §9.2.2) and the victory lap | [new-art] L, Must |
| Kept | Mr. X 1's night city: the blue skyline and the moon (set `$9D`, v00-v02) as the plaza backdrop | [engine-ok] |
| New BG | stadium gate and turnstiles, concourse, bleachers with crowd tiles (two frames, animated by CHR swap), the pitch, the running track, a scoreboard (a 6×3-block BG panel whose text is painted through the VRAM buffer), the press box window, floodlight towers, the players' tunnel | [new-art] L, Must |
| New sprites | Grand Pi-kun's valve and confetti, the high striker's puck and bell, lane judges with score cards (one 16×24 sprite, the card digits as tiles), training targets, beach balls, the 8 parade floats' champion hands (the champions themselves are their own boss sprites, reused) | [new-art] M, Must |

### 1.3 Screen by screen

CHR column: S = TS_STADIUM base, C = the city third (`$9D` skyline), P = Pi-kun's sizes (F-SIZES).

| GP | CHR | The player does | Enemies (cap) | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | S+C | READY. Walks right across the plaza under banners to GATE 1 | none | **First commentator pop-up**: K: *"Welcome to the GRAND PRIX! I'm Kalinka, and beside me in the booth is my papa—"* C: *"Dr. Cossack, head judge. Hello, Rock."* (A third line, once: *"You can turn us off in CONFIG. Please don't."*) | [new-art] S, Must |
| **01** | S | **LANE 1: JUMP** (steeplechase): three hurdles, then the **water jump** (a 48-px pool of floor type 8, shallow: falling in only slows you, `rm6` collision 8, gravity `$00.18`), then two 32-px gaps | 2 training targets (HP 1, harmless) | The DAMAGE judge holds up a card at the lane's end: 10 minus 3 per splash or fall | [engine-ok] + judge [new-code] S, Must |
| **02** | S | **LANE 2: SLIDE**: four limbo bars at 24 px, 1.5 s apart on a "LIMBO" timer | none | The TIME judge: 10 if the four bars are cleared before the timer. **Hidden-room tell**: after the last bar, a 16-px-high gap at the foot of the right wall, with a door sign `STAFF ONLY - PI-KUN` above it; slide into it (exit to 1C) | [engine-ok], Must |
| **03** | S | **LANE 3: CHARGE**: the **HIGH STRIKER** (`TEST YOUR BUSTER!`). Shoot the pad: a tap sends the puck 1/4 up, a half charge 1/2, a full charge rings the **bell** (DING, confetti). The bell opens the gate to 04 | none | The STYLE judge: 10 for a ring with the first full charge. **The only required tool in the stage**, with its own sign `HOLD B`. A full charge always opens the gate, so the lesson is the gate | [new-code] S, Must |
| **04** | S | **LANE 4: STANDS**: climbs the bleachers by four ladders; the **up exit** (vanilla type 2) into the upper stand | beach balls bouncing down the steps (3 at most, contact 1, a "boing") | The DAMAGE judge again: 10 minus 2 per ball hit. Crowd tiles cheer (CHR swap every 16 f) | [new-code] S (ball), Must |
| **05** | S | Upper stand: walks past the **press box** (Cossack and Kalinka in the window, sprites) and the **scoreboard** | none | **The entrant board** (BG text): `CHALLENGER: ROCKMAN (DR. LIGHT)` over `1 BLIZZARD ... 8 YAMATO / 9 BASS β (SPONSOR: MR. Y) / 10 ?????? (MASKED)`. Line 10 is Break Man's foreshadowing (BRIEF §2: the masked 10th entrant; §2.6). The four lane judges' cards are summed on the board as `WARM-UP 34/40` | [new-art] S, Must |
| **06** | S | Down the **players' tunnel**; **checkpoint 1** | none | Doubles as the GP Rush lobby (`meta.md` §9.2.2: one extra screen in this tileset). Eddie waves from a side door (no shop yet: *"Pit stop opens after the ceremony!"*) | [engine-ok], Must |
| **07** | S | Onto the track: the **parade** begins (§1.4) | none | Floats roll left at 0.75 px/f along the track; the champions wave | [new-code] M, Must |
| **08** | S | The parade's second half, across the **fountain moat** (a pit; the floats are the only bridge) | none | Floats are rideable platforms (vanilla lift `$A0` contact code, a 64×16 deck each); 2 floats on screen at most | [new-code] S, Must |
| **09** | S | The centre stage on the pitch: the Committee chairman's speech (3 short lines), Grand Pi-kun dancing; Mr. Y waves from his skybox above | none | **The sabotage** (cutscene-lite, 6 s, controls locked): Mr. Y presses a button (`UPGRADE!`); Pi-kun's eyes turn red; the scoreboard reads `PI-KUN 16-BIT EDITION`; the shutter to 0A slams | [new-code] S, Must |
| **0A** | S+P | **Boss: GRAND PI-KUN** (§1.6). A flat pitch with the track as its floor | | Shutter checkpoint (09) | Must |
| **1C** | S | **Hidden room: PI-KUN'S DRESSING ROOM** (§1.5) | | | Must |

Checkpoints: 06, and the boss shutter (09). The stage has 13 screens (00-0A, 1C, plus 0B for the post-boss walk-out
to the bracket, a one-screen exit with the first scorecard).

### 1.4 The parade (07-08) and the behaviour prize

- Eight floats, one per champion, in bracket order, each a 64×32 BG-coloured deck sprite with the champion's own
  sprite standing on it (their idle frame; their CHR set is queued per float, so at most 2 floats share a screen,
  `rm6` lesson 5). Each champion speaks one line when Rock passes (`story.md`; drafts: Blizzard *"Cold out here, eh?"*,
  Wind *"Nice weather for it!"*, Plant *"Mind the flowers!"*, Flame *"Feeling the heat?"*, Yamato *"A worthy rival
  stands before me."*, Tomahawk *"Howdy, partner."*, Knight *"Hail, challenger!"*, Centaur *"..."* (ABILITY UNKNOWN,
  the vanilla panel joke)).
- **Behaviour prize, CROWD FAVOURITE**: each champion holds out a hand for 90 f as his float passes (a raised-hand
  frame and a sparkle). Stand under it and jump: **HIGH FIVE!** (a clap SFX, the crowd roars). Eight high fives in
  one run → Kalinka: *"Eight for eight! The crowd loves him!"*, and the scoreboard flashes `CROWD FAVOURITE`.
  Reward: 30 bolts and, later, the eight champions cheer by name in the victory lap (§6.3). [new-code] S, Must.
- The floats over the moat (08) are the platforming: they move, so the high fives there are harder.

### 1.5 Secrets

| Bit | Secret | How | Tell | Tier A (riddle) | Tier B (instruction) |
|---|---|---|---|---|---|
| b0 | **PERFECT WARM-UP** | 40/40 on the four lane cards in one run | the cards are shown live and summed on the scoreboard at 05 | `FOUR JUDGES, FOUR CARDS. / A CHAMPION SHOWS THEM / ALL A TEN.` | `GET A 10 FROM EVERY LANE JUDGE: NO SPLASH, BEAT THE LIMBO TIMER, ONE CHARGE, NO BALLS.` |
| b1 | **PI-KUN'S DRESSING ROOM** (1C) | slide into the gap after lane 2 | the gap and the `STAFF ONLY - PI-KUN` sign | `EVERY MASCOT HAS A ROOM / WITH ITS NAME ON THE / DOOR. YOU HAVE TO DUCK.` | `SLIDE UNDER THE WALL AFTER THE LAST LIMBO BAR.` |
| b2 | **CROWD FAVOURITE** | eight high fives in the parade | raised hands, sparkles | `EIGHT CHAMPIONS, EIGHT / HANDS IN THE AIR. DON'T / LEAVE THEM HANGING.` | `JUMP UP UNDER EVERY CHAMPION'S RAISED HAND DURING THE PARADE.` |

**1C, the dressing room**: a mirror with bulbs, three spare Pi-kun heads on stands (one winks), a rack of costumes
with one **Mr. Y costume** on a hanger (Kalinka: *"Why is there a Mr. Y costume in here?"*), the first **sponsor
envelope** (+30) and a 1-UP. Exit: the door back to 02. This is the game's first hidden room, so it sets the pattern
every later one follows: one screen, a tell you can see from the route, a joke, an envelope.

### 1.6 Boss: GRAND PI-KUN, "16-BIT EDITION" (fight `$26`)

**What it is.** The GP mascot: a giant inflatable robot chick in a GP sash, 128 px tall when fully inflated. Mr. Y's
"upgrade chip" makes it rampage. It is the game's first boss, so it is a lesson: **the body is a balloon that bounces
your shots; only the valve takes damage, and only while it is open**. A pre-charged shot is the efficient answer,
which is exactly what lane 3 taught.

**How it is built.** The Mr. X 2 pod-column technique: Pi-kun is BG art in NT1, positioned by the frame's X and Y
scroll above the IRQ split, and the pitch below the split comes from NT0 row 24 (chain 7, handler `$3E:$C23A`)
[engine-ok]. The twist is size: three pre-drawn sizes (S 48 px, M 80 px, L 128 px) are streamed into CHR-RAM by
F-SIZES, 2-3 frames per change behind a puff of air sprites. The valve is a sprite plus the hit-box object, which
follows the scroll (as vanilla's `$D1/$D2` do). [new-code] M (F-SIZES), [new-art] M (three sizes ≈ 150 tiles), Must.

**Stats.** HP **14** (half a bar, `systems.md` §4.5). Contact 3; shockwave 2; confetti 1. Only the valve is a hit
box; the body returns every shot as a harmless bounce (`BOING`). The buster 1/30, the charge 3/30
(`systems.md` row); on replays the mid-boss default column applies.

| Id | Pattern | Timeline (frames) | Notes |
|---|---|---|---|
| A | **BOUNCE** (size L) | 3 bounces toward Rock, 48 f each, peak 64 px. Each landing sends **two shockwaves** along the floor (8 px tall, 2 px/f, contact 2) | Jump the shockwaves. Shots bounce off |
| B | **PFFFT** (deflate) | f0-20: a hiss and puff sprites from the valve (the tell); f20-50: shrinks L → M → S; f50-170: flies a scripted loop around the room at 2 px/f (a Lissajous path, never lower than 40 px above the floor at Rock's x); **the valve is open and hittable from f20 to f170** | The damage window: 150 f. One full charge lands 3; tap shots land 1 each with 30 f between |
| C | **REFILL** | f0-40: lands, and Mr. Y's skybox lowers a pump hose; S → M → L | The hose is a 1-tile-wide sprite: shooting it during C cancels the refill for 60 f (the valve stays open: a reward for attention) |
| D | **CONFETTI CANNON** (from HP ≤ 9) | the sash cannons fire 3 confetti bursts (slow arcs that drift down, contact 1) during A | |
| | Cycle | A, B, C (≈ 400 f). The valve faces Rock's side during B | |

**Pinch (HP ≤ 5): "16-BIT EDITION".** Its palette flashes to a garish "SUPER" palette (the foreshadowing of
Project SUPER), A becomes 4 bounces, B lasts 110 f at 3 px/f.

**Defeat.** The valve pops off; Pi-kun deflates completely and **flies around the stadium like a released balloon**
(a 3-s scripted sprite at full speed across the whole screen, the size frames cycling), then lands as a flat heap on
the pitch. Mr. Y's skybox blinds slam shut. The first **scorecard** follows (the judges' desk, `meta.md` §4.0), then
the bracket.

**Teaching.** It never needs anything but the buster. A player who learned lane 3 kills it in 5 openings (a full
charge per opening ≈ 3); a tap-only player in about 3 cycles more.

### 1.7 Commentator hooks

| Event | Hook (draft) |
|---|---|
| A lane card shown | the lane judge's card, then K: *"A perfect ten!"* / C: *"The judges are... thorough."* |
| First splash | C: *"The water jump is only knee-deep, Rock. On you."* |
| High striker DING | K: *"DING DING DING!"* |
| Entrant board | C: *"Entrant ten is... masked. How irregular."* |
| First high five | K: *"Up top!"* |
| The sabotage | C: *"Sixteen-bit edition? That's not in the programme!"* K: *"Papa, the mascot is attacking the chairman!"* |
| First valve hit | K: *"The valve! Hit the valve!"* |
| Defeat | C: *"The mascot has been... deflated. Let the Grand Prix begin!"* |
| Deaths (rotation) | *"Even the mascot got a point off him."* / *"It's only a warm-up!"* / *"He got bounced."* / *"Pop goes the entrant."* / *"Charge it, Rock. CHARGE it."* / *"The chairman is still talking, by the way."* |

### 1.8 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| 01 | The water jump becomes a real pit (block poke: water → air); one more 32-px gap | layout |
| 04 | 5 beach balls instead of 3, falling 1.5× faster | object + constant |
| Pi-kun | HP 20; pinch at HP 8; A = 4 bounces, shockwaves 3 px/f; B's open window 120 f | AI branch + constants |

### 1.9 Homage moments (the screenshot list)

1. Vanilla's own Mr. X picture with the X painted over as a Y.
2. Ringing the high striker's bell with a full charge.
3. The entrant board's line 10: `?????? (MASKED)`.
4. High-fiving Knight Man on his float.
5. Mr. Y's `UPGRADE!` button, and the scoreboard reading `PI-KUN 16-BIT EDITION`.
6. A 128-px balloon chick deflating and zipping around the stadium.

---

## 2. SEMIFINAL RIOT (meta 9, id 17)

**Pitch.** After the 4th win, Bass β riots the bracket (`meta.md` §3.5: the POSTPONED stamps). The Semifinal is that
riot, played: the GP Stadium at night, in a blackout, overrun by **rejected entrants** Mr. Y hired from the fan
contest's reject pile. You chase Bass through the concourse, the service tunnels, the stands and up the scoreboard to
the roof, where he fights you with **your own weapons**. When you beat him he refuses to lose, and **Break Man** steps
in front of his last shot. Break Man joins as the tag partner here (BRIEF §5.6: mid-game; `systems.md` §11 suggested
"after the Semifinal").

The player owns 4 weapons, Power (from the 2nd win) and Jet (from the 4th). The main route needs none of them.

### 2.1 Tileset and art

| Item | Content | Tags |
|---|---|---|
| Slot | **TS_STADIUM** (§1.2), with three new palette programs: NIGHT (lit), BLACKOUT (dark blue, only emissive tiles bright) and FIRE (orange flicker, a 3-step palette cycle thread like Flame's oil, `$3B:$9143` format) | [engine-ok] data, Must |
| New BG | service tunnels (pipes, cable trays, emergency lights), rubble, the scoreboard scaffold and the jumbotron (a 6×4-block panel; its "picture" is a portrait painted through the VRAM buffer), the roof gantry, floodlight fuse boxes | [new-art] M, Must |
| Kept | Mr. X 1's night city and moon (set `$9D`) as the roof arena's skyline | [engine-ok] |
| New sprites | 3 rejected entrants (16×24 each, 2-3 frames, a `REJECTED` name tag), Bass β (≈ 96 tiles: stand, run, dash, jump, shoot, copy pose, kneel, overdrive float), Break Man (the tag partner's set, `systems.md` §11), the BASS BLASTER sphere (3 sizes), the ACCEPTED stamp | [new-art] L, Must |

### 2.2 The rejected entrants (new enemies)

The vanilla game's bosses came from a fan design contest (the credit cards DWNB-41..48 name the winners). Mr. Y
hired the losers. Each wears a `REJECTED` tag, and each has a one-line gimmick, so the joke is a mechanic (CX lesson 2).

| Enemy | HP | Behaviour | Contact / shot | Why it was rejected (commentary) | Tags |
|---|---|---|---|---|---|
| **UMBRELLA MAN** | 3 | Walks 0.5 px/f; drops in from the stands with the umbrella open (falls 0.75 px/f). Shot from the front, he opens the umbrella for 60 f: a vanilla class-3 shield (`$38:$90A2`), shots reflect. Hit him from behind or while he walks | 2 | C: *"Rejected: the umbrella was the whole robot."* | [new-code] S, [new-art] S, Must |
| **VENDING MAN** | 6 | Stands; lobs a can every 90 f (an arc, 2 px/f). His lit front glows in the dark (an emissive palette entry), so in a blackout he is the room's only light source | 2 / can 2 | K: *"Rejected for 'excessive product placement'."* | [new-code] S, [new-art] S, Must |
| **CHEER MAN** | 2 | Hops in place with pom-poms. **While he lives, every other reject on screen moves and fires 1.5× faster** (`GO! FIGHT! WIN!` sparkles over them). Kill him first | 1 | C: *"Rejected: only helps other robots. Admirable, actually."* | [new-code] S, [new-art] S, Must |

**The audition rule.** A reject killed by a **full-power blow** (the full charge `$13`, PUNCH★ `$24`, BREAK★, Burning
Knuckle, Morning Star) does not explode: he gets a gold `ACCEPTED!` stamp, waves, and walks off screen. It counts as a
kill for scoring (class of the blow). A **Vending Man** accepted this way also dispenses a random small capsule. This
is the stage's behaviour prize (§2.5). [new-code] S, Must.

Lag cap: 3 rejects + 1 can + 3 shots + the fuse-box lever = 8.

### 2.3 Screen by screen

CHR: S = TS_STADIUM, N = night city (`$9D`). Palette program in brackets.

| GP | CHR | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | S+N | READY at the main gate (NIGHT). Trash-can fires; the scoreboard flickers `SEMI-FINAL: ROCKMAN vs ?????` | none | K: *"We're live from the stadium, where it's a riot. Literally."* | Must |
| **01** | S | Concourse (FIRE): runs right | 2 Umbrella, 1 Vending | Overturned food carts as cover | Must |
| **02** | S | Concourse 2 (FIRE) | 1 Cheer, 2 Umbrella | **Fuse box 1** at eye level (§2.5 b0) with C: *"Flip that switch, Rock!"* | Must |
| **03** | S | The ticket hall. **Bass sighting** (cutscene-lite, 90 f, controls live): Bass dashes along the upper rail and blasts the floor. *"Too slow, Rockman! See you on the roof!"* The floor crumbles under Rock (the Mr. X group's crumbling collision `$1D`, the falling-bell behaviour) into 04 | none | The crumble is the down exit; it cannot be avoided, and it cannot hurt (a soft landing in 04) | [engine-ok], Must |
| **04** | S | Service tunnel (BLACKOUT): emergency lights pulse dark 60 f / lit 30 f. C.FLASH, if owned, lights it for 240 f (`systems.md` §3.9) | 1 Vending (his front lights the room), 1 Umbrella | The pulse is the tell: walk on the lit beats | [new-code] S (pulse thread), Must |
| **05** | S | Tunnel 2: a burst water main floods the floor (floor type 8, gravity `$00.18`) | 1 Cheer, 1 Umbrella | Floatier jumps over two 48-px pits | [engine-ok], Must |
| **06** | S | **Break Man's help beat** (§2.6). Then **checkpoint 1** | none | The rubble wall; the **emblem door** on the left (hidden room 1D, tag-gated) | [new-code] S, Must |
| **07** | S | Ladders up into the stands (NIGHT) | 1 Umbrella floating down | | Must |
| **08** | S | The stands (BLACKOUT rhythm: floodlights 120 f on, 60 f off; tell: they buzz and flicker 20 f before going out) | 2 Umbrella, 1 Vending | **Fuse boxes 2 and 3**. A box flipped on keeps that screen lit for good | [new-code] S, Must |
| **09** | S | Upper stands | **Cheer rally**: 1 Cheer, 3 Umbrella | The 1.5× buff makes this the stage's hardest screen; the Cheer stands highest | Must |
| **0A** | S | Climbs the scoreboard scaffold (ladders); the **jumbotron** shows Bass's face and types taunts (`BASS β: NICE TRY, BLUE BOY`) | none | **Fuse box 4** on a ledge reached by a 40-px jump from a ladder top | Must |
| **0B** | S | Jumbotron top; **checkpoint 2** | 1 Vending | **Fuse box 5** | Must |
| **0C** | S+N | The roof gantry: a 16-px catwalk over the stands, wind gust zone (VA-GUST 0.5 px/f, windsock) | 2 Umbrella (they glide on the wind: 1.5 px/f) | **Fuse box 6**; shutter | [engine-ok] gust reuse, Must |
| **0D** | S+N | **Boss: BASS β** (§2.4) | | The roof: a flat floor and two 48-px gantry ledges at 64 px | Must |
| **0E** | S+N | The reveal (§2.6), then the walk-out with the scorecard | | | Must |
| **1D** | S | **Hidden room: THE LOCKER ROOM** (§2.5 b1) | | | Must |

Checkpoints: 06, 0B, the shutter (0C). 15 screens.

### 2.4 Boss: BASS β (fight `$21`), duel 1

**Who he is.** Mr. Y's entrant, "built from Rockman's own tournament data". So he fights with the data: **he copies
the champions' weapons that you own**. At the Semifinal that is exactly four (whichever four you won), so every
player's duel is different, and the rival literally mirrors you. Prototype look: unpainted armour panels with
yellow-black crash-test markers, the `β` on his chest.

**How he is built.** The Robot Master framework: the intro object `$93` spawns the room controller `$94` and becomes
the boss type through a GP extension of `$31:$9D43` [engine-ok + new type]. The copied shots are the **player's own
weapon projectile objects** with an enemy flag and enemy damage (their tiles are already in the player's sprite
CHR, so no CHR clash; `tech.md` confirms which are resident). [new-code] M, [new-art] L, Must.

**Stats.** HP 28. Contact 4. No weakness (a rival, not a puzzle): `systems.md` row, buster 1/40, charge 3/40,
weapons 2/24, PUNCH★ 3/30, **plus SC6 adaptive armour** (the 3rd consecutive damaging hit from one column makes that
column 1/45 until another column hits; a hex shimmer with that weapon's icon shows it, K: *"He's adapting!"*).

His copies (enemy versions of each weapon's tap):

| Copied weapon | What Bass fires | Damage to Rock |
|---|---|---|
| Y.SPEAR | one spear, straight, 3 px/f | 3 |
| W.STORM | one floor tornado, 2 px/f | 3 |
| B.ATTACK | 4 flakes in a spread | 2 each |
| F.BLAST | a fireball that leaves a floor pillar for 60 f | 3 |
| PLANT.B | a 4-leaf barrier for 120 f; it deletes up to 2 of Rock's shots | 3 contact |
| KNIGHT.C | a mace thrown out and back | 3 |
| SILVER.T | an arcing tomahawk | 3 |
| C.FLASH | a flash that makes Rock flinch for 20 f (no damage; REDUCED FLASHES: a darken) | 0 |

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **SCOUT** | f0-24: dash toward Rock at 2.5 px/f (contact 4); f24-36: 3 buster shots aimed at Rock, 6 f apart (2 dmg, 3 px/f); f36-66: recovery |
| B | **DOUBLE-JUMP VOLLEY** | f0: jump (vy −5.2); at the apex a second jump (vy −4.0); at the second apex a 3-way volley down-forward (45°, 67°, 90°); land; 20 f |
| C | **COPY** | f0-30: the **ANALYZING** pose (visor scan lines, the copied weapon's icon floats over his head: the tell), palette swaps to that weapon's colours; f30 and f70: fires the copy; f70-90: recovery. Picks among owned weapons, never the same twice in a row |
| D | **WALL KICK** (HP ≤ 18) | dashes into a gantry ledge, kicks off it (CX Quick Man's wall kick, credited) into a dive at Rock's x (contact 4); 70 f |
| | Cycle | A, B, A, C, then D if unlocked: ≈ 400 f |

**Pinch (HP ≤ 9): "β LIMITER OFF".** His outline flickers yellow-black. Dash 3.0 px/f; SCOUT fires 5 shots; COPY now
picks **the weapon you have hit him with most this fight** ("learning"); every recovery is 25 % shorter.

**COUNTER (Should).** When Bass fires a copy, the same weapon from Rock **cancels** it in mid-air (a clash spark), and
Rock's next hit with that weapon within 60 f is a `COUNTER!`: 3/16, outside SC6. It rewards reading the icon tell.
A visible special case in code (CX lesson 7). [new-code] S, Should.

**The finish: β OVERDRIVE (the help beat; scripted, ≈ 9 s).** At 0 HP Bass does not explode. He drops to one knee
(*"This... isn't... possible..."*), rises, the music cuts to a drone, he floats up and charges a giant **BASS
BLASTER** (a sphere growing over 120 f). Controls stay live but there is nowhere to hide. At f100 **Break Man's
whistle** plays (a new 2-s jingle on the Rockman 3 melody), Break Man beams down in front of Rock and raises his
shield; the blast breaks on it (white flash; REDUCED FLASHES: a darken), and Bass is thrown to the roof edge.
Bass: *"Tch. Who are YOU supposed to be?"* Break Man: *"Entrant number ten."* Bass: *"This isn't over, Rockman.
The real final is mine!"* He teleports. Rock takes no damage in the scene.

**The 4MI touch (light).** If Rock's HP falls below 6 during the pinch, Break Man's whistle sounds once from
off-screen and a large life capsule drops from the top of the screen (once per fight). A purist who never drops below
6 never sees it. This is the 4MI Proto Man pattern (concrete trigger, fair, skippable) at the scale of a semifinal.

**Records.** `BASS_ADAPT` (the column used most) is saved for duel 2 (`systems.md` SC6). **RIVAL** (`meta.md` T13):
no damage taken from the bar fill to the overdrive.

### 2.5 Secrets

| Bit | Secret | How | Tell | Require | Tier A | Tier B |
|---|---|---|---|---|---|---|
| b0 | **FLOODLIGHTS** | flip all 6 fuse-box levers (02, 08, 08, 0A, 0B, 0C) in one run. Any shot flips a lever; each lit screen stays lit. Six on: the crowd returns (crowd tiles animate), K: *"The lights are back! The show goes on!"* | red levers with a lightning sticker; the first one at eye level, with C's hint | - | `A STADIUM WITHOUT LIGHTS / IS JUST A BIG DARK BOWL. / SIX SWITCHES. FLIP 'EM.` | `THERE ARE SIX FUSE BOXES BETWEEN THE CONCOURSE AND THE ROOF. SHOOT EVERY LEVER.` |
| b1 | **THE LOCKER ROOM** (1D) | the emblem door at 06 opens only to Break Man (`systems.md` §11 tag gate) | the door shows his scarf emblem during the help beat itself, and K: *"That door has his emblem on it..."* | TAG (`meta.md` R4) | `ENTRANT TEN'S LOCKER / ONLY OPENS FOR ENTRANT / TEN. ASK HIM NICELY.` | `CALL BREAK MAN AT THE RUBBLE WALL. HIS EMBLEM DOOR LEADS TO THE LOCKERS.` |
| b2 | **TALENT SCOUT** | all 9 placed rejects ACCEPTED (killed by a full-power blow) | the first ACCEPTED stamp, and C: *"A full-power audition. Rules are rules."* | - | `EVERY REJECT DESERVES A / SECOND AUDITION. MAKE IT / A FULLY CHARGED ONE.` | `DEFEAT EVERY REJECTED ENTRANT WITH A FULL CHARGE (OR A FULL PUNCH) AND THEY WALK AWAY HAPPY.` |

**1D, the locker room**: eleven lockers with name plates. Rock's, marked `CHALLENGER` (a spare helmet), the eight champions' (gags: Wind
Man's is full of leaves, Knight Man's has a "polish" can), #9 Bass's (dented, `KEEP OUT`), and **#10 `??????`**: a
spare yellow scarf and a pair of sunglasses (a nod to the Proto Man fan image). The sponsor envelope (+30) and an
E-tank.

**TALENT SCOUT's reward**: 30 bolts; the accepted rejects reappear in W2's losers' room (§5.2) and cheer in the
victory lap (§6.3). A friend mechanic made of enemies.

### 2.6 Break Man's reveal and help beats

| Beat | Where | What happens | Mechanic |
|---|---|---|---|
| **The help** | 06 | Rubble seals the tunnel. Whistle; Break Man drops in, fires one Break Shot (the `systems.md` §3.11 move, `$E4`), the rubble (a cracked `$B` block) breaks. *"Hmph. Don't keep the crowd waiting."* He leaves by the emblem door, which shuts | Shows the Break Shot, the scarf emblem and the tag gate before the player can use any of them (CX lesson 6) |
| **The block** | 0D | the β OVERDRIVE shield block (§2.4) | Shows his shield |
| **The reveal** | 0E | K: *"Who IS that?!"* C: *"...That's Blues."* K: *"That's OBVIOUSLY Blues."* Break Man: *"Name's Break Man."* (the scarf flaps) *"If you need a second pair of hands, whistle."* Banner: `BREAK MAN JOINS! PAUSE, THEN SELECT: CALL` | Sets `FORMS.TAG` and EVENTS b5 (`meta.md` §3.6). His disguise is as obvious as Mr. Y's, and he insists just as hard: the running gag, mirrored on the good side |

### 2.7 Commentator hooks

| Event | Hook (draft) |
|---|---|
| First reject | C: *"Those are rejected contest entries! Who let them in?"* K: *"Who PAID them?"* |
| First Cheer buff | K: *"He's cheering for the wrong team!"* |
| Bass sighting | K: *"That's Bass! He's wrecking the ticket hall!"* |
| A fuse box flipped | K: *"Lights!"* (once per box: *"Two!"*, *"Three!"*...) |
| Bass copies a weapon (first time) | C: *"That's YOUR weapon, Rock! He copied it!"* |
| SC6 adapts | K: *"He's adapting!"* |
| A COUNTER | C: *"Fight fire with fire, I always say."* |
| β OVERDRIVE | K: *"Papa, he's still going!"* C: *"That's not in the rules either!"* |
| Deaths (rotation) | *"Rejected!"* / *"The crowd didn't see that. The lights were off."* / *"Bass is copying his falls now too."* / *"Postponed: Rockman."* / *"Mind the umbrella. No, the OTHER umbrella."* / *"That's a semifinal exit."* |

### 2.8 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| 01-02, 08-09 | Cheer buff 2× instead of 1.5×; one more Umbrella on 09 | constant + object |
| 04, 08 | BLACKOUT dark phase 90 f instead of 60 | constant |
| 0C | Gust 0.75 px/f | constant |
| Bass β | Pinch at HP 14; SCOUT fires 5 shots from the start; D unlocked from the start; the off-screen life capsule never drops | AI branch |

### 2.9 Homage moments

1. Bass β throwing **your** Knight Crusher back at you, his palette turned Knight-Man green.
2. Break Man's whistle, and his shield breaking the BASS BLASTER.
3. *"Entrant number ten."* / *"That's OBVIOUSLY Blues."*
4. An Umbrella Man gliding down from the stands with a `REJECTED` tag.
5. A Vending Man taking a full charge and walking off with an `ACCEPTED!` stamp, dropping a can of energy.
6. The 1993 night-city skyline and moon behind the roof duel.

---

## 3. EXHIBITIONS E1-E4 (meta 10-13, ids 18-21)

**What they are.** Four optional bonus stages, each lit on the bracket by a pair of venue secret exits (`meta.md`
§3.1: **E1 Wind + Knight, E2 Tomahawk + Plant, E3 Blizzard + Flame, E4 Yamato + Centaur**). Each guest is an
"arcade legend" robot with a parody name, and **each rule is a real mechanic from its game**, not a costume (CX
lesson 2): rows that clear, a ball you keep in the air, a formation that speeds up as it shrinks, ghosts that each
chase a different target. Each is short: a lobby, three lesson screens, a high-score corridor, an arena.

### 3.0 Rules shared by the four exhibitions

- **One tileset, TS_ARCADE**: an arcade hall (cabinets, carpet, a change machine, neon) as the base, plus one CHR
  third per exhibition for its rule art. Simple tiles on purpose (PLAN §3.3). [new-art] M (base) + S each, Should.
- **Layout**: 00 lobby (the guest's cabinet, the guest's intro card, the commentators), 01-03 the rule taught in
  three steps, 04 a high-score corridor (checkpoint), 05 the arena, 1E the backroom. Par 90 s (`systems.md` §6.3).
- **Engine**: F-GRID (§0.7) is the shared core: a WRAM cell grid painted into the nametable with collision (the
  well, the bricks, the formation and bunkers, the dots). [new-code] M, Should.
- **The rule does the damage.** A guest takes **4 with 12 i-frames** from its rule event (a line clear, a ball, a
  cannon hit on the commander, a chomp), and **1/32** from weapons (`systems.md` §4.5's E1-E4 column). HP 28.
- **Scoring**: VARIETY's par would punish a stage with one tool, so each exhibition sets its OWNED set in the
  stage-attribute table to what the rule allows, and **rule damage is booked as class 4 (HAZARD)**, so a guest killed
  by its own rule counts. (A proposal to `systems.md` §6.4.)
- **Vehicles are lent**: E3 and E4 put Rock on a `COMMITTEE LOANER` Rush Jet if Jet is not owned yet. NO TAG on
  vehicle screens.
- **Reward (first clear)**: 100 bolts (`systems.md` §7) + an **exclusive RACING COLOUR** (one per exhibition: a fifth
  to eighth palette beside the shop's four, `systems.md` §8; cosmetic, no balance cost) + the guest's trophy in the
  Museum + the guest unlocked in GP Rush (fights `$18-$1B`). **No chip**: PLAN's Line Clear, Multiball, Barrier and
  Power Pellet live on **inside the stages as rule power-ups**, which keeps `systems.md`'s 21 chips intact (its open
  question 9, answered).
- **Secrets (the same three in every exhibition)**: b0 = the game's famous mastery act (a TETRIS, a long rally, a
  perfect UFO shot, all four ghosts on one pellet); b1 = **the BACKROOM** behind the lobby's `OUT OF ORDER` cabinet
  (one rule for all four, so the tell is learned once: the cabinet wobbles when shot; three full charges, or one
  full punch, topple it; behind it a door to 1E); b2 = a clean-play act.
- **The BACKROOM** (1E, one per exhibition): a dusty storeroom with a prototype cabinet and a gag plaque (each listed
  below), a 1-UP and a W-tank. No envelope (the envelopes are the venues' and the fortress's).

### 3.1 E1 BLOCK MAN: "FALLING BLOCKS" (1984 homage) (fight `$18`)

**The rule.** Tetrominoes fall into a well. **Rock moves them with his buster**: a tap on a piece's side pushes it one
column away from the shot, a full charge **rotates** it 90°, and jumping into it from below bonks it up one row.
Landed pieces are solid floor. Completed rows clear (the rows above drop 16 px, and Rock with them).

| Mechanic | Numbers | Tags |
|---|---|---|
| Well | 10 columns × 13 rows of 16×16 cells (160×208 px), centred (x 48-207); grey walls; camera locked | F-GRID, Should |
| Falling piece | 4 cell sprites (16 hardware sprites). Falls 1 cell per 32 f (lesson screens), 24 f (arena), 16 f (pinch). The **NEXT** piece is drawn in a side panel (BG) | [new-code] M |
| Ghost piece | a dotted outline (BG tiles) shows where the piece will land. **The crush tell** | [new-code] S |
| Push / rotate / bonk | tap: ±1 column (blocked by walls or cells: a clunk SFX); full charge: rotate clockwise (with a 1-column wall kick if blocked); a head bonk: up 1 row, once per piece | [new-code] S |
| Lock | 16 f after touching down; the cells become collision 1 and tiles | F-GRID |
| Clear | a full row flashes 20 f, then clears; rows above shift down over 12 f (≤ 8 cells repainted per frame) | F-GRID |
| Crush | a piece locking onto Rock: 4 damage, and Rock is pushed up onto it | [new-code] S |
| Top out | a cell locks in row 0: `GAME OVER` flashes, Rock takes 8, the well empties (no instant death) | [new-code] S |

Screens:

| GP | The player does | The rule's step | Tags |
|---|---|---|---|
| **00** | The arcade lobby: the `FALLING BLOCKS` cabinet; Block Man's intro card. The `OUT OF ORDER` cabinet (b1) | intro | Should |
| **01** | **MOVE**: the exit is a door 3 rows up the right wall. Only O and I pieces fall. Push them right with taps to build a staircase | taps push | Should |
| **02** | **ROTATE**: a 64-px spike pit across the floor. An upright I falls; rotate it flat with a full charge so it bridges the pit | charge rotates | Should |
| **03** | **CLEAR**: a stack with a 1-wide gap in each of its 4 bottom rows; the exit door is buried under it. An I falls: rotate it upright and drop it into the gap: **4 rows clear at once** and the door is uncovered (the b0 TETRIS is possible on purpose right here) | lines clear | Should |
| **04** | The high-score corridor (`1ST BMN 999999 ... 5TH ROCK %SCORE%`); checkpoint; shutter | - | Should |
| **05** | **Arena: BLOCK MAN** | | Should |
| **1E** | BACKROOM: a `FALLING BLOCKS (PROTOTYPE)` cabinet whose screen shows only one piece shape, the long one, falling forever. Plaque: `THE LONG ONE NEVER COMES WHEN YOU NEED IT. WE PUT IT IN STORAGE.` | | Should |

**Boss: BLOCK MAN.** A robot built of four 16×16 blocks that **rearranges itself into the seven tetromino shapes**.
He plays as a piece: **he flies to the top of the well and drops as one of the falling pieces**, and Rock can push
and rotate him like any other. Whenever a cleared row contains one of his blocks, he takes 4 per row (`systems.md`'s
4/12 rule cell). So the fight is: build rows with gaps shaped like Block Man, then make him fall into them.

| Id | Pattern | Timeline |
|---|---|---|
| A | **DROP** | f0-30: flies to the top, picks a shape (I O T L J S Z, a 7-bag so every shape comes once per 7), shows his face on the NEXT panel; falls 1 row per 24 f (Rock can push, rotate, bonk him); locks for 60 f (solid: Rock can stand on him); then pulls his four blocks back out (leaving a Block-Man-shaped hole) and flies up |
| B | **NEXT PIECE** | a plain piece falls between his drops (1 per drop) |
| C | **GARBAGE** (every 3rd drop) | a grey garbage row rises from the bottom with one gap; the whole stack lifts 16 px (Rock with it) |
| D | **HARD DROP** (HP ≤ 12) | his ghost appears at Rock's column for 20 f (the tell), then he slams down in 4 f (crush 4) |
| Pinch (HP ≤ 8) | **LEVEL UP** | fall speed 16 f per row; GARBAGE every 2nd drop |

- **FOUR LINES**: a clear of 4 rows that contains him = 16 damage. Kalinka shouts *"TETR- ...FALLING-BLOCK-
  FOUR-LINE-CLEAR!"* (the commentators cannot say the trademark: a running gag in all four exhibitions).
- Weapons: chip 1/32 on him (shots also push him, so they are never wasted). C.FLASH's Time Stop freezes the falling
  pieces for its 90 f (pieces are normal objects), which is the strongest setup tool. M.BEAM shelves keep Rock above
  a crush. Ice Block (B.ATTACK UP+B) cannot freeze him (NOFREEZE).
- Lag: Block Man (4 sprites, 1 object) + 1 piece + 3 shots = 5 objects.
- Defeat: his four blocks fly apart and fall into the well as four cells, which complete a row and clear in a final
  flash.

| Secret | How | Tier A | Tier B |
|---|---|---|---|
| b0 **FOUR LINES** | clear 4 rows at once anywhere in E1 (03 is built for it) | `FOUR ROWS AT ONCE. THE / LONG PIECE WAS BORN FOR / THIS. STAND IT UP.` | `ROTATE THE LONG PIECE UPRIGHT AND DROP IT IN A FOUR-ROW GAP.` |
| b1 **BACKROOM** | topple the lobby's OUT OF ORDER cabinet | `OUT OF ORDER? KICK IT. / WELL. SHOOT IT. THREE / TIMES, WITH FEELING.` | `HIT THE BROKEN CABINET IN THE LOBBY WITH THREE FULL CHARGES.` |
| b2 **CLEAN STACK** | beat Block Man with no top-out and no crush | `NO ONE GETS CRUSHED IN A / CLEAN STACK. WATCH THE / DOTTED OUTLINE.` | `BEAT BLOCK MAN WITHOUT BEING CRUSHED OR TOPPING OUT. THE GHOST PIECE SHOWS WHERE THEY LAND.` |

Hooks: first rotation K *"He's playing it!"*; first clear C *"A line! Very tidy."*; Block Man in a cleared row
C *"He was IN the line!"*; top-out K *"Game over! ...Not really. Get up!"*. Deaths: *"Crushed by a T."* / *"He
needed an I piece."* / *"Rock has been cleared."* / *"Too much garbage."* / *"Watch the dotted line!"* / *"Next
piece: Rockman."*

HARD: arena fall speed 16 f from the start; garbage every 2nd drop; hard drop from HP 20; no ghost piece in 03.

Homage moments: rotating a falling piece with a charged shot; Block Man locking in place as a T, and a four-row clear
taking him with it; a cleared row dropping Rock 16 px; *"FALLING-BLOCK-FOUR-LINE-CLEAR!"*.

### 3.2 E2 PADDLE MAN: "BRICK BREAKER" (1976/1986 homage) (fight `$19`)

**The rule.** A ball bounces around the room and breaks bricks. **Rock is the paddle**: a buster shot that hits the
ball knocks it upward, angled by where it hits, and the ball bounces off his helmet. **The ball never hurts Rock; it
hurts the floor**: a ball that reaches the floor cracks the brick it lands on, and a second hit opens a hole (a pit).
Lose the ball and you lose your footing, not a life.

| Mechanic | Numbers | Tags |
|---|---|---|
| Ball | 8×8, 2.0 px/f at serve, +0.25 per 8 brick hits, cap 3.5; reflects off walls, bricks and the ceiling | [new-code] M, Should |
| Shot deflect | a shot touching the ball sets vy = −|v|, and vx from the hit offset (5 zones: ±60°, ±40°, ±20° off vertical, like the classic paddle's zones) | [new-code] S |
| Header | the ball landing on Rock's helmet: vy = −|v|, vx from Rock's x offset (same 5 zones); a `boink` | [new-code] S |
| SMASH | a full charge (or PUNCH★) on the ball: it turns red and pierces up to 3 bricks for 120 f, speed 4.0 | [new-code] S |
| Bricks | F-GRID cells, 16×8; 1 hit each (silver: 2 hits; gold: unbreakable) | F-GRID |
| Floor bricks | the arena and lesson floors are bricks: 1 ball hit = cracked, 2 = hole | F-GRID |
| Capsules | a brick with a capsule drops it (falls 1 px/f): **W** wide (head-bounce from anywhere above, 15 s), **S** slow (−40 %, 15 s), **M** multi (3 balls; cap 3), **L** laser (shots pierce bricks, 15 s), **R** repair (fills every floor hole) | [new-code] S, [new-art] S |

Screens:

| GP | The player does | Step | Tags |
|---|---|---|---|
| **00** | Lobby: the `BRICK BREAKER` cabinet; Paddle Man's intro; the OUT OF ORDER cabinet | intro | Should |
| **01** | **SERVE**: a closed room; a 2-thick brick wall blocks the exit. Deflect the ball into the wall until it breaks through | shots deflect | Should |
| **02** | **KEEP IT UP**: the floor is bricks over a pit; the exit is behind the ceiling bricks. Keep the ball up (shots and headers) while it breaks the ceiling | the floor erodes | Should |
| **03** | **CAPSULES**: a wall of capsule bricks; a giant stone head in the background (`D.U.H.`, a parody of the famous final face) with its mouth bricked up (b1 is not here; the mouth hides an R capsule) | capsules | Should |
| **04** | High-score corridor; checkpoint; shutter | - | Should |
| **05** | **Arena: PADDLE MAN** | | Should |
| **1E** | BACKROOM: a cabinet with a rotary knob (a paddle controller) labelled `ANALOG. VERY ADVANCED.` Plaque: `IN 1976 THE CONTROLLER WAS A KNOB. IN 1993 WE HAD A D-PAD. PROGRESS.` | | Should |

**Boss: PADDLE MAN.** He sits at the top centre inside a **brick shell** (3 layers, 8 bricks wide) and slides his own
paddle along the ceiling under it, returning the ball down at Rock. A ball through a hole in the shell that reaches
his core does 4. HP 28: seven core hits.

| Id | Pattern | Timeline |
|---|---|---|
| A | **RALLY** | his paddle returns the ball toward Rock's x ±24 px |
| B | **SPIN SERVE** (every 3rd return) | a curving ball: vx changes by ±0.05 px/f² (the banana shot); a spin sparkle is the tell |
| C | **REBUILD** (every 600 f) | a brick-layer drone (a small object, HP 2) re-lays 4 shell bricks at the most damaged spot; shoot it to stop it |
| D | **MULTIBALL** (HP ≤ 12) | his paddle splits the ball into 3 (cap 3); the floor erodes faster |
| E | **PADDLE BEAM** (HP ≤ 12) | the paddle stops over Rock, flashes 30 f (the tell), fires a beam straight down (3 damage): the only attack that hurts Rock directly besides contact |
| Pinch (HP ≤ 8) | ball cap speed 4.0; REBUILD every 400 f | |

- Weapons: shots break bricks too (so every weapon helps open the shell) and chip 1/32 on the core. KNIGHT.C breaks
  bricks on both legs; SILVER.T arcs over the paddle; the held mace (KNIGHT.C hold) hangs under the shell and keeps
  the ball bouncing in the hole. **The Power punch is a synergy here**: a punch on the ball is a SMASH without a
  charge. R capsules repair the floor; M.BEAM bridges a hole.
- Lag: Paddle Man + paddle + 3 balls + drone + capsule + 3 shots = 10 (the cap; MULTIBALL suspends capsule drops).
- Defeat: the last ball breaks his core; the shell collapses brick by brick in a rising chime (each brick a note).

| Secret | How | Tier A | Tier B |
|---|---|---|---|
| b0 **RALLY 30** | keep one ball in play for 30 deflections in a row (a rally counter appears at 10) | `THIRTY TOUCHES WITHOUT A / DROP. EVEN THE KNOB / CONTROLLER COULD DO IT.` | `KEEP ONE BALL UP FOR 30 HITS IN A ROW. HEADERS COUNT.` |
| b1 **BACKROOM** | the OUT OF ORDER cabinet | (as E1) | (as E1) |
| b2 **PERFECT FLOOR** | beat Paddle Man with no floor brick broken | `THE FLOOR IS LAVA. NO, / THE FLOOR IS BRICKS. SAME / THING: DON'T LET IT FALL.` | `BEAT PADDLE MAN WITHOUT THE BALL EVER BREAKING A FLOOR BRICK.` |

Hooks: first header K *"A header! Is that allowed?"* C *"It is now."*; first floor hole C *"Mind your footing, Rock!"*;
SMASH K *"SMASH!"*; core hit C *"Right through the shell!"*. Deaths: *"He fell through his own floor."* / *"The ball
was fine, by the way."* / *"Lost the ball, lost the footing."* / *"Bricked it."* / *"Should've taken the R."* /
*"Paddle Man: 1, Gravity: also 1."*

HARD: serve 2.5 px/f; floor bricks break in 1 hit; no R capsule in 03; REBUILD every 400 f from the start.

Homage moments: a header that sends the ball through the shell; the floor eroding into a pit under a missed rally; a
three-ball MULTIBALL with Rock juggling; the bricked-up stone head's mouth.

### 3.3 E3 INVADER MAN: "INVASION 1978" (fight `$1A`)

**The rule.** A formation steps side to side and down; **the fewer are left, the faster it steps** (the original's
famous accident: the hardware drew fewer invaders faster). **Rock is the cannon**: Rush Jet locked to the bottom lane,
moving left and right, firing **straight up, one shot on screen at a time**. Bunkers erode from both sides. A UFO
crosses the top. Invaders reaching the lane is an invasion.

| Mechanic | Numbers | Tags |
|---|---|---|
| CANNON mode | Rock on the (loaner) Jet at y `$C0`, 1.25 px/f left/right, B fires the buster straight up at 4 px/f, **one shot on screen**. OWNED = {BUSTER} (§3.0). The cabinet card says `ARCADE RULES: ONE SHOT` | [new-code] S, Should |
| Formation | 5 rows × 8 columns of 16×8 invaders, **drawn as BG in NT1** and moved by the scroll above a split (the Mr. X 4 floating-BG technique, chain `$16`); the bottom band (bunkers, lane) is NT0, unscrolled | [engine-ok] tech + F-GRID |
| Step rule | the formation moves 2 px per step; **one step every N frames, N = invaders alive** (40 alive: every 40 f; 1 alive: every frame). At a wall: down 8 px and reverse | [new-code] S |
| Hits | the shot tests the formation's 40-bit WRAM map offset by the scroll; a hit erases 2 tiles and spawns an explosion sprite | F-GRID |
| Bombs | at most 3 on screen: a zigzag, a straight one, and one aimed at Rock (the original's three shot types). 2 damage | [new-code] S |
| Bunkers | 4 bunkers of 3×2 tiles in the bottom band; each tile has 3 wear states (tile swaps), eroded by both sides | F-GRID |
| UFO | crosses the top every 25 s at 1 px/f. Hit: a bonus. **The shot-count rule**: the cabinet card explains that the 23rd shot, then every 15th, gives the max bonus (the 1978 trick, credited as folklore) | [new-code] S |
| Invasion | an invader reaches the lane: Rock takes 10 and the wave restarts (no instant death) | [new-code] S |

Screens:

| GP | The player does | Step | Tags |
|---|---|---|---|
| **00** | Lobby: the `INVASION 1978` cabinet, its screen tinted by the famous coloured cellophane strips (a green band at the bottom, red at the top: done here with two palette bands); Invader Man's intro; the OUT OF ORDER cabinet. Rock docks the Jet at a `LAUNCH` pad | intro | Should |
| **01** | **WAVE 1**: 3×6, no bunkers. Teaches one shot at a time and the speed-up | one shot | Should |
| **02** | **WAVE 2**: 4×8, bunkers | bunkers | Should |
| **03** | **WAVE 3**: 5×8, bunkers, the UFO | the UFO | Should |
| **04** | High-score corridor (Rock on foot again); checkpoint; shutter | - | Should |
| **05** | **Arena: INVADER MAN** | | Should |
| **1E** | BACKROOM: an upright cabinet tipped on its side, its monitor showing `INSERT 100 YEN`. Plaque: `IN 1978 THIS GAME CAUSED A COIN SHORTAGE. THE BUSTER IS FREE.` (a well-known anecdote, worded as folklore) | | Should |

**Boss: INVADER MAN.** A big crab-shaped commander (32×24, BG in NT1, part of the formation's top row) leading a full
formation. He can only be hit through a **clear column** (shots stop at invaders), so you must cut a lane through his
troops, and he keeps closing it.

| Id | Pattern | Timeline |
|---|---|---|
| A | **MARCH** | the formation steps by the step rule and drops bombs |
| B | **REINFORCE** (every 15 s) | he beams invaders into up to 6 empty cells, **the column under him first** (a 40-f twinkle on each cell is the tell) |
| C | **MOTHERSHIP DIVE** (HP ≤ 12) | he detaches and dives at the lane in a zigzag (3 px/f, contact 3; the Galaxian-style homage), then flies back to his slot |
| D | **DEATH RAY** (HP ≤ 12) | a 24-px-wide beam straight down at Rock's x after a 30-f flash; it erases the bunker tiles it crosses |
| Pinch (HP ≤ 8) | the formation's minimum step interval is 2 f (very fast); REINFORCE every 10 s | |

- A cannon hit on Invader Man = 4/12 (seven hits). Invaders: 1 hit each.
- Lag: the formation is BG (0 objects); commander hit box, 3 bombs, 1 shot, the UFO, 2 explosions = 8.
- Defeat: the whole formation freezes, and every invader drops one row per frame like a curtain falling, then the
  commander's sprite tips over.

| Secret | How | Tier A | Tier B |
|---|---|---|---|
| b0 **UFO ACE** | hit the UFO with the 23rd shot of a wave (the cabinet card states the rule) | `THE MYSTERY SHIP PAYS / BEST ON SHOT 23. ARCADE / REGULARS COUNTED. COUNT.` | `COUNT YOUR SHOTS IN A WAVE. HIT THE UFO WITH THE 23RD.` |
| b1 **BACKROOM** | the OUT OF ORDER cabinet (on foot, in the lobby, before docking) | (as E1) | (as E1) |
| b2 **BUNKER HOLD** | finish wave 3 (03) with all four bunkers at least half intact | `GOOD COVER IS WORTH MORE / THAN GOOD AIM. DON'T SHOOT / THROUGH YOUR OWN WALLS.` | `FINISH WAVE 3 WITHOUT LOSING HALF OF ANY BUNKER. SHOOT AROUND THEM.` |

Hooks: first speed-up C *"They're getting faster as they go!"*; UFO hit K *"Mystery ship!"*; REINFORCE C *"He's calling
reinforcements!"*; last invader of a wave K *"The last one's always the fastest!"*. Deaths: *"Invaded."* / *"One shot
at a time, Rock!"* / *"Behind the bunker! THE BUNKER!"* / *"Earth has fallen. Again."* / *"The coin shortage is
back."* / *"Game ov- no, he's fine."*

HARD: formation starts one row lower; bombs 1.5× faster; 3 bunkers instead of 4.

Homage moments: the last invader zipping across the screen at one step per frame; a lane cut through the formation
and closed again by REINFORCE; the green/red cellophane tint on the lobby cabinet; the formation falling like a
curtain.

### 3.4 E4 MAZE MAN: "MAZE MUNCHER 1980" (fight `$1B`)

**The rule.** A single-screen maze, seen from above. **Rock flies the (loaner) Jet through it on a grid**, eating
dots. Four **Met-ghosts** chase him, **each with a different target**, exactly the famous four personalities. Power
pellets turn them blue and edible. The side tunnels wrap around.

| Mechanic | Numbers | Tags |
|---|---|---|
| MAZE mode | Rock on the Jet, top-down sprite (a 16×16 "seen from above" Rush with Rock), moves on an 8-px lattice at 1.25 px/f along 16-px corridors; **pre-turn buffering** (a direction held before a junction is taken at it). No firing (the rule). OWNED = {} (rule damage only, §3.0) | [new-code] M, Should |
| Maze | 224×208 px, 28×26 cells, dots as single BG tiles erased on touch (1 VRAM tile per dot) | F-GRID |
| Tunnel | the side exits wrap (`venues_b.md` X-WRAP) | shared |
| Ghost targets | RED **CHASER**: Rock's cell. PINK **AMBUSHER**: 4 cells ahead of Rock. CYAN **FLANKER**: the cell 2 ahead of Rock, mirrored through the red ghost (double the vector). ORANGE **SHY**: Rock's cell while farther than 8 cells, else its home corner. At each junction a ghost takes the exit closest (straight line) to its target and never reverses | [new-code] S |
| Modes | SCATTER 7 s (each ghost to its corner) / CHASE 20 s, alternating; every switch reverses them (the tell) | [new-code] S |
| Power pellet | 4, in the corners; ghosts turn blue for 6 s (4 s in the arena), flee with random turns, blink white for the last 2 s; touching a blue ghost eats it (its eyes go home) | [new-code] S |
| Damage | touching a normal ghost: 4 damage + 60 i-frames (Rock has HP; no instant death) | |
| Fruit | appears under the pen at 70 and 170 dots: a large life, then a large weapon energy | |

Screens:

| GP | The player does | Step | Tags |
|---|---|---|---|
| **00** | Lobby: the `MAZE MUNCHER` cabinet; Maze Man's intro (a round orange robot whose visor opens like a mouth: a homage, not a copy); the OUT OF ORDER cabinet | intro | Should |
| **01** | **MAZE 1**: a half-screen maze, 2 ghosts (red, pink), no pellets; eat all the dots and the pen gate opens to the exit | targets | Should |
| **02** | **MAZE 2**: the full maze, 4 ghosts, 4 pellets | pellets | Should |
| **03** | **INTERMISSION** (6 s, not interactive): Maze Man runs left chased by a red Met-ghost; then runs back chasing a blue one, twice his size. The commentators narrate (C: *"A coffee break. The original had them too."*) | - | Should |
| **04** | High-score corridor; checkpoint; shutter | - | Should |
| **05** | **Arena: MAZE MAN** | | Should |
| **1E** | BACKROOM: a cocktail-table cabinet (the sit-down kind) with two chairs. Plaque: `THE TABLE VERSION. YOU COULD PUT YOUR DRINK ON THE GHOSTS.` | | Should |

**Boss: MAZE MAN.** He waits in the ghost pen as the ghosts' boss. When Rock eats a power pellet, **the pen opens**
and Maze Man becomes edible too: touching him while the pellet lasts is a `CHOMP` for 4 (4/12). Pellets respawn when
all the dots in their quadrant are eaten, so the fight is: clear a quadrant, take its pellet, chase him down. HP 28:
seven chomps.

| Id | Pattern | Timeline |
|---|---|---|
| A | **PEN** | while no pellet is active, he stays in the pen and the 4 ghosts chase |
| B | **HUNT** | from the 2nd chomp on, he leaves the pen while no pellet is active and hunts Rock himself as a 5th chaser, targeting Rock's cell at 1.0 px/f (slower than Rock), contact 4 |
| C | **RUN** | during a pellet he flees to the pellet farthest from Rock |
| D | **PELLET RACE** (HP ≤ 12) | when Rock heads for a pellet (within 6 cells), Maze Man races for it too. **If he eats it first, the roles reverse**: Rock turns blue for 4 s and Maze Man and the ghosts hunt him (contact 6) |
| Pinch (HP ≤ 8) | ghosts +10 % speed; blue time 3 s | |

- Lag: Rock + 4 ghosts + Maze Man + fruit = 7.
- Defeat (**the kill screen**): the maze's right half turns into scrambled tiles (the famous level-256 split, a few
  dozen garbage tiles painted over 10 frames), Maze Man stops, and pops into the same garbage. [new-art] S.

| Secret | How | Tier A | Tier B |
|---|---|---|---|
| b0 **FOUR-GHOST COMBO** | eat all four ghosts on one power pellet (02 or the arena) | `ONE PELLET, FOUR GHOSTS. / THE PROS WAIT FOR THEM TO / BUNCH UP. THEN: DINNER.` | `LURE THE GHOSTS CLOSE TO A PELLET, EAT IT, AND CATCH ALL FOUR BEFORE THEY TURN BACK.` |
| b1 **BACKROOM** | the OUT OF ORDER cabinet | (as E1) | (as E1) |
| b2 **UNTOUCHED** | clear every dot of 02 without a ghost touching Rock | `EVERY GHOST HAS A HABIT. / LEARN ALL FOUR AND THEY / CAN'T LAY A FINGER ON YOU.` | `EAT ALL THE DOTS IN THE BIG MAZE WITHOUT BEING TOUCHED. THE ORANGE ONE GETS SHY UP CLOSE.` |

Hooks: first blue ghost K *"They're blue! Get them!"*; ghost eaten C *"Delicious, I'm told."*; pellet race lost
K *"He ate it first! RUN, Rock!"*; kill screen C *"The machine can't count that high!"*. Deaths: *"Caught by the pink
one. It's always the pink one."* / *"He went into the tunnel. They were waiting."* / *"Wakka wak- no. No trademarks."*
/ *"Blinky says hi. I mean the red one."* / *"Out of dots, out of luck."* / *"Ghosted."*

HARD: ghosts +10 % speed; blue time 4 s in 02 and 2 s in the arena; no fruit.

Homage moments: the pink ghost cutting Rock off at a junction he had not reached yet; four ghosts eaten in one
pellet; the intermission's giant blue chase; Maze Man dissolving into the right-half garbage of the kill screen.

---

## 4. HALL OF FAME H1-H5 (meta 14-18, ids 8-12)

### 4.0 The museum

**The story beat.** At the 8th win, START on the lit trophy plays the theft (`meta.md` EVENTS b4): during the trophy
ceremony a **UFO-catcher crane** (a first look at H4's boss) lowers out of the sky, grabs the GP CUP and carries it
off to an island museum, the **HALL OF FAME**: *"The greatest robots in history! Every one of them... er... that I
personally lost to! Rebuilt, MK-VI!"* (Mr. Y). It is a museum of Rockman 1-5, and each wing is one game.

**The floor plan** (the fortress map, §0.3): a rotunda and five wing doors marked 1987, 1988, 1990, 1991, 1992, plus a
sixth door, `1993 - UNDER CONSTRUCTION`, greyed out (§4.6). The wings are played **in order** (a museum tour; it also
fixes when M.BEAM and Super arrive). If a Should wing (H2, H4) is cut, its door reads `CLOSED FOR RENOVATION` and the
tour skips it; nothing later depends on H2 or H4 except H4's optional friend (§4.5).

**Every wing has:**

| Element | Rule |
|---|---|
| The entrance plaque | F-PLAQUE: the year and what the game introduced (2-4 lines). 4-5 plaques per wing in all; reading is optional; each stamps the Museum gallery (`meta.md` §9.5) |
| Three remixed hazards | the signature hazards of that game, built on the base layout's own tech where possible |
| A display case | one exhibit you can take (M.BEAM in H1, the first E-tank in H2, ...) |
| The MK-VI boss | a legacy boss re-skinned onto a vanilla BG-boss technique, with one twist (§0.6) |
| A mid-boss | H1 Big Eye, H2 Picopico-kun, H3 Doc Robot (H4 and H5 spend that budget on set pieces) |
| One tag pocket | a shutter with Break Man's emblem leading to a small reward (`systems.md` §11: always optional) |
| Secrets | b0 showpiece, b1 hidden room (a "storeroom" with a gag exhibit and an envelope), b2 behaviour prize (§0.4) |
| Mr. Y's heckles | §0.5, with 2 wing-specific lines each |

**Plaque text** is factual and short; every date below is a release year. Where a claim is folklore rather than a
documented fact, the plaque words it as folklore.

**MK-VI damage rows** follow `systems.md` §4.5 (machines: buster 1/32, PUNCH★ 4/24; robots: the champion scale), with
the overrides listed in §8.

### 4.1 H1 ROCKMAN (1987), id 8: base vanilla Wily 2

**Pitch.** The first game's wing: appearing blocks, Guts Man's tipping lifts, Elec Man's beams, Fire Man's pillars,
the useless score counter, the Magnet Beam you could not finish the game without, and the Yellow Devil.

**Tileset.** TS_H1 = a copy of Wily 2's tables (`$2A:$89`; 141-157 of 256 tiles used, so room for the MM1 third).
Kept: the pink machine blocks, green circuit walls, the disappearing-block objects `$8F`, the twin F.BLAST plug, the
walker room's NT1 layout. New: the MUSEUM third, an MM1 third (Guts lift and rail, Elec beam emitters, fire vents,
score balls, the Yellow Devil's pieces and eye ≈ 60 tiles, Big Eye). [new-art] M, Must.

**The score.** In H1 only, a 7-digit `SCORE` sits under the life bar (Rockman 1's), and enemies drop **score balls**
(Rockman 1's bonus pellets) instead of items. The score does nothing, as it did in 1987 (plaque: `THE SCORE (1987):
IT NEVER DID ANYTHING. THE JUDGES DISAGREE.`), except for b0. [new-code] S, Must.

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance hall: marble, velvet ropes; plaque `ROCKMAN (1987): THE FIRST. A BLUE ROBOT, SIX BOSSES AND A SCORE THAT COUNTED NOTHING.` READY | none | Vanilla's Power-block E-tank pocket (charged punch) kept | [engine-ok], Must |
| **01-02** | v01-v02 | Right through the "1987 gallery" | totem walkers `$12`, capped walkers `$1E` (each drops a score ball) | Score balls placed in awkward spots (b0) | [engine-ok], Must |
| **03** | v03 | **The Magnet Beam case** (F-CASE): `MAGNET BEAM (1987). HANDLE WITH CARE.` Touch: the case shatters, **YOU GET MAGNET BEAM** (weapon-get, chain `$17`; `systems.md` §3.10 sets WEAPONS b8). **Checkpoint 1** | none | Plaque: `IN 1987, PLAYERS WHO MISSED THIS BEAM COULD NOT FINISH THE GAME. WE PUT IT ON THE MAIN PATH. YOU'RE WELCOME.` | [new-code] S, Must |
| **04** | v04 | Up through the **appearing-block hall**: vanilla's 11 `$8F` blocks over the spike floor, retimed to a 1987 rhythm (each block: appear, 90 f, vanish; a "pyoo" SFX) | none | The vanilla **F.BLAST plug** at the upper right leads to the branch 10-12 (and one blast opens both plugs: the vanilla quirk, kept) | [engine-ok], Must |
| **05-06** | v05-v06 | **Guts Man's lifts** over a pit: lifts ride a rail; on the dashed rail sections the lift **tips** for 30 f (Rock slides off if he stays on), then rights itself | vanilla riders `$C6` throwing balls (1 per screen) | OBJ_GUTSLIFT: vanilla lift contact (`$A0`) + a rail path table + a tip state | [new-code] M, Must |
| **07** | v07 | **Elec Man's beams**: three horizontal beams across a ladder shaft, each 60 f on / 90 f off, offset; the emitters spark 20 f before firing | 1 rider | 3 damage per beam touch | [new-code] S, Must |
| **08-09** | v08-v09 | Right, then down at 09 | 1 rider; the E-tank at 09 (vanilla) | **Tag pocket**: an emblem shutter at 08 → a closet with 6 score balls and a large weapon energy | [engine-ok], Should |
| **0A** | v0A | **Checkpoint 2** (vanilla's). The branch rejoins here | none | | Must |
| **0B** | v0B | **The Magnet Beam gap**: a 96-px gap over a pit, with an anti-Jet field over it (floor type E blocks thrust, `systems.md` §2.1) and a sign `NO RUSH JET: AUTHENTIC 1987 EXPERIENCE`. Build a beam, walk across | none | **The fortress's only required tool** (§0.2), handed over 6 screens earlier on the same route, and on both routes | [engine-ok] + M.BEAM, Must |
| **0C** | v0C | **Fire Man's pillars**: floor vents glow 20 f, then a 16×64 flame column rises (30 f), holds (40 f), drops | 1 rider | | [new-code] S, Must |
| **0D** | v0D | **Mid-boss: BIG EYE MK-VI** (room locked by shutters) | | | Must |
| **0E** | v0E | Shutter corridor; plaque `THE YELLOW DEVIL'S PIECES NEVER FLY HIGHER THAN 64 PIXELS. A MAGNET BEAM AT 72 IS A FINE PLACE TO WATCH FROM.` | | The tell for the boss's beam shelf | Must |
| **0F** | v0F | **Boss: YELLOW DEVIL MK-VI** (§4.1.2) | | | Must |
| **10-12** | v10-v12 | **Branch: THE ARCHIVE** (via the F.BLAST plug): dark corridors of old display cases, skeleton robots `$65`; rejoins 0A, skipping 05-09 | `$65` ×2 per screen | Hidden-room tell on 11 (b1) | [engine-ok], Must |
| **13** | new | **Hidden room: THE BOX ART STOREROOM** | | | Must |

Checkpoints: 03, 0A, the shutter (0E). The M.BEAM case (03) is before the branch point (04), so **every route takes
the beam before the gap (0B)**. A death after 03 keeps the beam (WEAPONS b8 is set on pickup and autosaved).

#### 4.1.1 Mid-boss: BIG EYE MK-VI (fight `$08`)

Rockman 1's hopping cyclops. A 32×48 sprite (new art), HP 20 (`systems.md` mid-boss default row), contact 4.

| Id | Pattern | Timeline |
|---|---|---|
| A | **LOW HOP** | a 24-px hop toward Rock, 24 f |
| B | **HIGH HOP** | crouch 12 f (the tell: the eye squints), an 80-px hop toward Rock, 56 f |
| | Landing | every landing shakes the screen; a grounded Rock within 64 px is **stunned 16 f** (a jump avoids it) |
| | Cycle | A or B at random, 2:1, with a 20-f pause between hops |
| Pinch (HP ≤ 7) | **MK-VI** | after each high hop, the eye fires one aimed shot (3 px/f, 3 damage) |

Slide under a high hop. Lag: 1 object + 1 shot.

#### 4.1.2 Boss: YELLOW DEVIL MK-VI (fight `$1C`)

**What it is.** Rockman 1's famous boss: a yellow blob that crosses the room **piece by piece**, re-forms on the
other side, and opens a single eye. Weak to a beam (C.FLASH stands in for the Thunder Beam).

**How it is built** [new-code] M (F-PIECES), [new-art] M (≈ 60 tiles), Must. Vanilla Wily 2's walker room: the
boss body is BG in NT1, the floor strip comes from NT0 below the split (chain 7, handler `$3E:$C23A`) [engine-ok].
**The twist**: the body is a 3×4 grid of 16×16 pieces (48×64 px). F-PIECES erases a piece from NT1 (4 tiles), launches
it as a 16×16 sprite, and paints it back into NT1 on the far side when it arrives. The eye is a sprite plus the only
hit box; the body dinks.

**Lanes.** A piece flies at the height of its row: **lane 1** (0-16 px above the floor: jump it), **lane 2** (16-32:
slide under it, or jump high), **lane 3** (32-48: stand still, it passes over), **lane 4** (48-64: stand still). A
readable rhythm game, and nothing ever flies above 64 px, so an M.BEAM built at 72 px or higher is a **safe shelf**
(the plaque at 0E is the tell).

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **CROSSING** | a piece leaves every 16 f, from an order table (two 12-entry tables alternate, e.g. `1 2 1 3 4 1 2 2 3 1 4 2`); each flies at 4 px/f (≈ 40 f across); at most 3 in flight; re-forms piece by piece on the far side: ≈ 232 f |
| B | **EYE** | the eye opens for **120 f, +30 per missing piece** (cap +120); aimed lasers (3 px/f, 3 damage) at f30, f70, and f110 if still open |
| C | **BODY SLAM** (HP ≤ 18) | after B, the whole body hops 24 px toward Rock (NT1 Y scroll), 40 f; the landing stuns a grounded Rock within 64 px for 16 f |
| | Cycle | A, B, (C): ≈ 400-500 f |

**The twist that changes the fight: knock the pieces down.** A flying piece hit by a full-power blow (a full charge,
PUNCH★, the Super fist, BREAK★, or any hit of 3+) **drops to the floor** and lies there as a solid 16×16 block (a
platform, max 3). The body re-forms **with holes** where those pieces should be, and each hole keeps the eye open 30 f
longer ("he's not all there", K). At the next crossing the floor pieces fly back first. So aggressive play buys
longer windows and footholds; passive play (dodging) is slower but safe.

**Pinch (HP ≤ 9): MK-VI.** Pieces leave **two at a time** in two lanes (the order table guarantees one safe lane
between them), at 5 px/f; three lasers per eye phase.

**Damage** (`systems.md` row, eye only): C.FLASH **4/12 W**, Y.SPEAR 3/16 G, PLANT.B 1/32 R, buster 1/32, charge
3/32, PUNCH★ 4/24. SC7, the "SELECT trick" (Could), stays as `systems.md` defines it; the H1 plaque at 00 carries its
hint (`SOME TRICKS ARE A SELECT FEW.`).

**Defeat.** The twelve pieces scatter as sprites, bounce to the floor and explode one after another, 4 f apart.

**Teaching.** It is the M.BEAM's first exam (the shelf), and the full charge's (knocking pieces down).

#### 4.1.3 Secrets

| Bit | Secret | How | Tell | Tier A | Tier B |
|---|---|---|---|---|---|
| b0 | **THE SCORE COUNTS** | collect all 24 score balls in H1 (12 placed, 12 dropped by placed enemies, always) in one run; a counter `BALLS 17/24` sits under the SCORE | the counter | `IN 1987 THE SCORE MEANT / NOTHING. THE JUDGES WILL / PAY FOR EVERY LAST BALL.` | `COLLECT ALL 24 SCORE BALLS IN THE 1987 WING. EVERY ENEMY THERE DROPS ONE.` |
| b1 | **THE BOX ART STOREROOM** (13) | on branch screen 11, one crate in a stack is charred; F.BLAST breaks it (`$D`) and a ladder leads down | the charred crate | `SOME 1987 PACKAGING IS / STILL IN STORAGE. FOLLOW / THE SMELL OF SMOKE.` | `IN THE ARCHIVE BRANCH, BURN THE CHARRED CRATE WITH F.BLAST.` |
| b2 | **NEVER WHOLE** | from the second crossing on, the Yellow Devil never re-forms complete (knock at least one piece down every crossing) | the holes are visible, and K comments the first time | `A DEVIL WITH A HOLE IN / IT CAN'T CLOSE ITS EYE. / KEEP HIM INCOMPLETE.` | `KNOCK DOWN AT LEAST ONE FLYING PIECE EVERY CROSSING (FULL CHARGE OR FULL PUNCH).` |

Rewards: b0 30 bolts; b1 the envelope, a 1-UP, and the gag exhibit (a crate stencilled `ROCKMAN (1987): OVERSEAS
PACKAGING. DO NOT DISPLAY.` beside a new-art figure of a stocky "box-art robot" in yellow-and-blue holding a pistol,
and the plaque `SOME EXHIBITS ARE KEPT IN STORAGE FOR EVERYONE'S SAFETY.`); b2 an E-tank + 30 bolts.

Hooks: Magnet Beam case K *"A magnet beam! What does it do?"* C *"It's a beam. It's... not especially magnetic."*;
first score ball K *"Points! What are points for?"* C *"Nothing at all. Isn't it wonderful?"*; the gap sign
C *"Authentic. Painfully authentic."*; Yellow Devil appears C *"The Yellow Devil! I had nightmares about it in 1987."*
K *"Papa, you were a grown man in 1987."*. Heckles: *"My Yellow Devil was the hardest boss of 1987. Ask anyone."* /
*"Score: zero. How very 1987."*. Deaths: *"The lift tipped. They always tip."* / *"Should have built a beam."* / *"In
1987 we'd be restarting the whole castle."* / *"Jump the low ones, Rock!"* / *"The devil's in the pieces."* / *"Game
over? There's a score for that."*

HARD: appearing blocks 70 f instead of 90; lifts tip for 45 f; Elec beams 80 on / 70 off; the gap 112 px (two
beams); Big Eye HP 28 and the pinch from the start; the Devil's pieces at 5 px/f from the start and pinch at HP 14.

Homage moments: the Magnet Beam in a glass case with a museum label; `NO RUSH JET: AUTHENTIC 1987 EXPERIENCE`; a Guts
lift tipping Rock into a pit; standing on a knocked-down piece of the Yellow Devil to shoot its eye; the score counter
going up for nothing; the box-art robot in storage.

### 4.2 H2 ROCKMAN 2 (1988), id 9: base vanilla Wily 1

**Pitch.** The second game's wing: the famous castle approach, Quick Man's force beams down a shaft (and the Flash
Stopper that stops them), Air Man's fans, Heat Man's appearing blocks, Picopico-kun, the first E-tank, and the Mecha
Dragon.

**Tileset.** TS_H2 = a copy of Wily 1's (`$2A:$80`; 255 of 256 blocks, so the jester head's and some shaft-variety
blocks are dropped to make room). Kept: the purple mountains, chain fence and rubble ground (00-02), the red-brick
shaft, the updraft blowers `$36/$41`, the blue riveted section, the Power pocket. **The dinosaur's 162-tile set `$8B`
is redrawn as the Mecha Dragon** in the same budget. New: MUSEUM third; force-beam emitters and beams; the password
board; the castle silhouette for the backdrop. [new-art] M, Must (H2 itself is Should).

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | The castle approach diorama at night (vanilla mountains; a skull-castle silhouette added on the horizon). Plaque `ROCKMAN 2 (1988): E-TANKS, PASSWORDS, AND THE MOST FAMOUS CASTLE INTRO IN HISTORY.` | Metalls `$18` | | Must |
| **01** | v01 | The **first E-tank** in a case: `THE FIRST E-TANK (1988). PLEASE TAKE ONE.` (a real E-tank, once per save). A plaque with a **1988 postcard** showing a 5×5 password grid (b2's pattern) | Fire-Telly drones `$2C` (Telly debuted in Rockman 2) | Vanilla Power-block 1-up kept | [new-code] S, Must |
| **02** | v02 | The **password board** (b2) by the castle door, then down the castle well | Metalls | F-GRID 5×5 | [new-code] S, Should |
| **03** | v03 | Top of **QUICK MAN'S SHAFT**: plaque `QUICK MAN'S FORCE BEAMS (1988). FLASH MAN'S TIME STOPPER STOPPED THEM. SO DOES C.FLASH (UP+B). WE ALSO ADDED A WARNING LIGHT. YOU'RE WELCOME.` | skeleton `$65` | | Must |
| **04-08** | v04-v08 | **The force-beam fall** (§4.2.1): 5 screens of falling past beams that fire as you pass their trigger lines | bombers `$1B`, 1 shield-car (07) | **Air Man's fans**: vanilla's updraft blowers at v05/v06 re-skinned as Air Man fan robots (collision A columns, behaviour kept) give the fall its pauses | [new-code] M, Must |
| **09-0D** | v09-v0D | The rest of the fall (no beams) | cannon rider `$20` (0B), stompers `$2D` | The vanilla **Power pocket** at 09 → 14-17 (E-tank, 8 small HP, 3 big WE) kept; Air fans at 0A | [engine-ok], Must |
| **0E** | v0E | **Checkpoint 1** (vanilla's) | none | | Must |
| **0F** | v0F | Blue riveted hall | samurai spearman `$A2` + its 4 items (vanilla) | **Tag pocket**: an emblem shutter → 2 large life energies | [engine-ok], Should |
| **10** | v10 | **Mid-boss: PICOPICO-KUN MK-VI** (§4.2.2), replacing vanilla's jester head `$10` | | | Must |
| **11** | v11 | **Heat Man's appearing blocks** over a lava floor (collision F): vanilla Wily 2's `$8F` block objects, 8 of them, in Heat Man's long, cruel sequence. **Checkpoint 2** at the screen's start. Plaque `IN 1988 YOU SKIPPED THIS WITH ITEM-2. TODAY YOU HAVE RUSH JET. WE ARE NOT ANGRY.` (Jet is allowed: the skip is the homage) | none | | [engine-ok] reuse, Must |
| **12** | v12 | Shutter corridor (loads the dragon art, like vanilla's `$8B` load). A window in the back wall: **a huge eye slides past it** (one sprite) | none | Plaque `THE MECHA DRAGON (1988). IT CHASED YOU ACROSS THE SKY. IT HAS NOT CALMED DOWN.` | Must |
| **13** | v13 | **Boss: MECHA DRAGON MK-VI** (§4.2.3) | | | Must |
| **14-17** | v14-v17 | The Power pocket (vanilla, optional) | | b1's tell at 16 | [engine-ok] |
| **18** | new | **Hidden room: AIR MAN CAN'T BE BEATEN** | | | Must |

#### 4.2.1 The force-beam fall (04-08)

OBJ_FORCEBEAM [new-code] M, Must: an emitter on the left or right wall at a given height, with a trigger line above
it. When Rock's Y passes the trigger, the emitter **glows for 30 f** (the warning light Rockman 2 never had), then a
beam grows across the shaft at 8 px/f to the far wall and stays until the screen is left. **A beam is deadly on
touch** (Rockman 2's rule; it counts as spikes, so SPIKE GUARD applies, a proposal to `systems.md`). Two or three
beams per screen; the safe line weaves, so Rock must steer while falling (vanilla air control: walk speed).

**C.FLASH's Time Stop** freezes every growing beam where it is (a frozen half-beam is safe to fall past), the direct
Rockman 2 homage, and **the fans** are rests where Rock can hover and read the next screen. Lag: ≤ 3 beams + 2
enemies.

#### 4.2.2 Mid-boss: PICOPICO-KUN MK-VI (fight `$09`)

Rockman 2's wall blocks that come alive. Built on **F-PIECES** (the Yellow Devil's engine, reused at no extra code):
the room's right wall is 10 BG blocks (16×16). In pairs, blocks **detach from the wall** (erased from the BG), fly at
Rock's position at launch (2.5 px/f, contact 3), land, and become little hopping robots (HP 2 each; hop 24 px every
40 f). At most 2 pairs alive. The boss bar counts the blocks left (10 blocks = 28 units).

The twist: **each detached block leaves a hole in the wall**. When all ten are gone, the wall is open, and that hole
is the exit. Pinch (≤ 4 blocks left): pairs launch every 60 f instead of 120 f. Damage: the mid-boss default row per
block-robot. Lag: 4 robots + 3 shots.

#### 4.2.3 Boss: MECHA DRAGON MK-VI (fight `$1D`)

**What it is.** Rockman 2's dragon: it flies on the left of a bottomless arena and breathes fire while you stand on
floating blocks.

**How it is built.** The **Mr. X 4 X Crusher technique**: the dragon is BG art in NT0, moved by the frame's scroll
above an IRQ split, and a second IRQ 11 lines later repoints the PPU for the bottom band (chain `$16`, handler
`$3E:$C475`) [engine-ok]. The bottom band is the pit (dark, a lava glow). Its art replaces set `$8B` (162 tiles)
[new-art] M. Hit box: the **head** (an object that follows the scroll); the body and wings reflect (vanilla
Mechazaurus parts, class `$86`). **The twist: the floor is Heat Man's appearing blocks.** Four block positions
(x 64, 112, 160, 208; 96-112 px above the pit) are sprite platforms (vanilla lift contact); **three are solid at a
time**; every 180 f one vanishes and the empty one appears (it flickers 30 f first: the tell). **The block Rock is
standing on never vanishes.** [new-code] S, Must.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **HOVER** | bobs ±24 px over 120 f (Y scroll); drifts 32 px toward Rock and back (X scroll) |
| B | **FIREBALL** | every 90 f, one fireball aimed at Rock (2.5 px/f, 3 damage); from HP ≤ 18, three in a fan (−15°, 0°, +15°) |
| C | **LUNGE** | the jaw opens 20 f (the tell), the head lunges 48 px forward for 40 f (contact 6), then back |
| | Cycle | A runs throughout; B on its timer; C every 3rd B |
| Pinch (HP ≤ 9) | **DIVE** | the dragon sinks out of view (60 f; lava bubbles and a shadow under one block are the tell), bursts up under that block (the block shatters, gone for 300 f) and **rains six fireballs** straight down at random x (2 px/f) as it rises |

**Damage** (`systems.md` row): KNIGHT.C **4/12 W** (the returning-blade homage, [guess] on the Rockman 2 fact, as
`systems.md` notes), SILVER.T 3/16 G, F.BLAST 1/32 R (a fire dragon), PUNCH★ 4/24.

**Weapons as tools.** M.BEAM bridges a vanished block (plaque in 12: `ITEM-1 (1988) MADE PLATFORMS. SO DOES THE
MAGNET BEAM (1987). USE THE ONE YOU HAVE.`); Y.SPEAR's Wall Spear into the arena's right wall gives a perch; C.FLASH's
Time Stop freezes fireballs and pauses the block rhythm (the blocks are objects), and holds the dragon at most 45 f
(`systems.md` §3.9).

**Defeat.** The dragon falls into the pit with a long roar (a red palette flash); steam rises for 2 s.

#### 4.2.4 Secrets

| Bit | Secret | How | Tell | Tier A | Tier B |
|---|---|---|---|---|---|
| b0 | **QUICK REFLEXES** | fall from 03 to 09 without dying and without Time Stop | the plaque at 03 names the easy way, which makes the hard way a choice | `IN 1988 THE BRAVE FELL / PAST QUICK MAN'S BEAMS / WITHOUT STOPPING TIME.` | `GET DOWN THE FORCE-BEAM SHAFT WITHOUT DYING AND WITHOUT C.FLASH'S TIME STOP.` |
| b1 | **AIR MAN CAN'T BE BEATEN** (18) | in the Power pocket's room 16, behind the second Power wall, one wall section leaks white air rings (the vanilla blower puffs) through a crack: a charged punch breaks it | the leaking air rings | `SOMETHING IN THE POCKET / IS BLOWING AIR THROUGH / THE WALL. PUNCH THE WIND.` | `IN THE POWER-PUNCH POCKET, BREAK THE WALL THE AIR RINGS COME THROUGH.` |
| b2 | **PASSWORD** | at 02, shoot the 5×5 board's dots (each shot toggles a dot) to match the 1988 postcard on 01's plaque | the postcard and the board side by side, 1 screen apart | `A 1988 POSTCARD STILL / REMEMBERS ITS PASSWORD. / THE BOARD IS LISTENING.` | `COPY THE DOTS FROM THE POSTCARD PLAQUE ONTO THE PASSWORD BOARD BY SHOOTING THEM.` |

**18, the room**: two Air Man fan robots blow a gale (VA-GUST 1.0 px/f) across the room toward a spike wall; walk
against it to the envelope. On a pedestal, an empty glass case: `AIR MAN (INVISIBLE EDITION). ON LOAN FROM ROCKMAN
CX, WHO MADE HIM INVISIBLE. WE CAN'T SEE HIM EITHER.` (PLAN's CX thanks.) A second plaque: `AIR MAN COULD NOT BE
BEATEN (FOLK SONG, 2000s).` b2's reward: a W-tank + 30 bolts.

Hooks: first force beam K *"LASER!"* C *"They had no warning lights in 1988. Character-building."*; Time Stop on a
beam C *"Flash Man would be proud."*; Picopico wall opens K *"The wall was the boss!"*; dragon C *"I remember that
dragon. Everyone remembers that dragon."*. Heckles: *"Item-2 is not coming back."* / *"My dragon has a sense of
occasion."*. Deaths: *"Quick Man's beams: still undefeated."* / *"Heat Man's blocks claim another."* / *"He fell for
it. Literally."* / *"The dragon thanks you for dinner."* / *"Mind the gap. The VANISHING gap."* / *"Should've used the
password."*

HARD: beams glow 20 f instead of 30; one more beam per screen on 05 and 07; Heat blocks 25 % faster; Picopico pairs
every 90 f; the dragon dives from HP 14 and blocks vanish every 150 f.

Homage moments: falling past a force beam frozen in mid-growth by Time Stop; Heat Man's blocks over lava with a sign
blessing the Rush Jet skip; a wall of blocks coming alive and leaving the exit behind; the Mecha Dragon bursting up
through a block; an empty case for the invisible Air Man.

### 4.3 H3 ROCKMAN 3 (1990), id 10: base vanilla Mr. X 3

**Pitch.** The third game's wing: the slide, Rush, Break Man's debut and his whistle, Needle Man's presses, Gemini
Man's mirror twin, Magnet Man's pull, Doc Robot, and Gamma, which you beat by **riding its own rocket fist up and
punching it in the face**. The Super Adaptor comes out of Gamma's head.

**Tileset.** TS_H3 = a copy of Mr. X 3's (`$2F:$92`; 256 blocks, 255 tiles: the Metonger Z tank's blocks and tiles
are freed for Gamma). Kept: the red gear machinery, pistons, the pulsing warning-light thread (`$0E/$0F`), Fire-Telly
drones (thinned from 23 to 6). New: MUSEUM third; needle-press heads, crystal (Gemini) tiles, magnet blocks, the
Break Man statue, Gamma (≈ 160 tiles, the Mechazaurus budget). [new-art] L, Must.

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance; plaque `ROCKMAN 3 (1990): THE SLIDE, RUSH, AND A MYSTERIOUS ROBOT WITH A WHISTLE.` The pulsing warning light (vanilla). Up | none | Vanilla Power-block 1-up kept | Must |
| **01** | v01 | **RUSH (1990)**: a Rush-shaped spring pad (vanilla spring `$57` code) with the sign `RUSH COIL: PLEASE DO NOT JUMP ON THE EXHIBIT.` The only way up is to jump on the exhibit | samurai spearman `$A2` (vanilla guard) | The joke is the route | [engine-ok], Must |
| **02** | v02 | **BREAK MAN (1990)**: a statue on a ledge; plaque `A MYSTERIOUS ROBOT CALLED BREAK MAN. EVERYONE KNEW.` A music box plays his whistle when you pass. If Break Man is called here: *"...Bad likeness."* E-tank (vanilla) | none | | [new-art] S, Must |
| **03-07** | v03-v07 | **NEEDLE MAN'S PRESSES** down the dark machine hall (§4.3.1) | 6 Fire-Telly drones, dome turrets `$2B` | b1's stuck press at 05 | [new-code] S, Must |
| **08** | v08 | **Checkpoint 1** (vanilla's) | | | Must |
| **09-0B** | v09-v0B | Up through **GEMINI MAN'S MIRROR HALL** (§4.3.2) | bombers `$1B` | Gemini Rock | [new-code] M (T7 reuse), Should; fallback below |
| **0C-0D** | v0C-v0D | **MAGNET MAN'S PULL**: magnet walls pull Rock 0.75 px/f toward spike walls while he is in their field (VA-GUST with magnet art; the field glows) | stompers `$2D` | | [engine-ok] reuse, Must |
| **0E** | v0E | **Mid-boss: DOC ROBOT MK-VI** (§4.3.3) | | | Must |
| **0F** | v0F | **Checkpoint 2**. **Tag pocket**: emblem shutter → a whistle-shaped 1-UP | | | Should |
| **10** | v10 | Shutter corridor; plaque `GAMMA (1990): A PEACEKEEPING ROBOT. IT KEPT VERY LITTLE PEACE. ITS LAST WEAKNESS WAS A SPINNING TOP. WE HAVE NO TOPS. THE HEAD RESPECTS ONLY A FIST.` | | The SC5 tell | Must |
| **11** | v11 | **Boss: GAMMA MK-VI** (§4.3.4) | | | Must |
| **12** | new | The Super Adaptor room (§4.3.5) | | | Must |
| **13** | new | **Hidden room: THE DOC ROBOT WORKSHOP** | | | Must |

#### 4.3.1 Needle presses (03-07)

OBJ_NEEDLEPRESS [new-code] S, Must: a 16×48 spiked piston on the ceiling. Rest 70 f, **shake 20 f (the tell)**, slam
down 48 px in 8 f, hold 20 f, rise 30 f. Contact is **deadly** (spikes). Presses come in groups of 2-3 with offset
timers. **Some presses stop 16 px above the floor**: their slammed position leaves a slide gap (Rockman 3's slide,
celebrated; the gap presses have a yellow stripe). The vanilla red pistons are their art base.

#### 4.3.2 Gemini Man's mirror hall (09-0B)

**Gemini Rock**: a crystal-palette copy of Rock that mirrors his left/right inputs (the input mirror T7 that
`venues_b.md` builds for Flame's Shadow Rock, reused) [new-code] M, Should.

- 09: a crystal wall splits the room. Two floor plates, one on each side; the hatch above opens only while **both**
  are pressed: Rock on his, Gemini Rock on the mirrored one. The mirrored side has one obstacle the real side does not
  (a pit), so the player must route the copy around it by thinking in mirror.
- 0A: enemies attack the copy too; if it dies it reforms after 120 f.
- 0B: both must reach the top ledges at the same moment for the exit shutter.
- Plaque: `GEMINI MAN (1990): THERE WERE TWO OF HIM. NOW THERE ARE TWO OF YOU.`
- **Fallback** if T7 slips: Gemini Man's bouncing laser (a beam that reflects off walls at 45°) through a crystal
  room, Must.

#### 4.3.3 Mid-boss: DOC ROBOT MK-VI (fight `$0A`)

Rockman 3's Doc Robot copied Rockman 2's bosses. **Doc Robot MK-VI copies one of your champions: the one whose venue
you scored worst in** (from STAGEREC best scores; ties go to the most recent). It runs that champion's own GP AI with
**that champion's sprite in a grey X-ray palette** and a Doc Robot skull overlay (one 16×16 sprite following the head)
[new-code] S, [new-art] S, Must. The boss panel types `DOC ROBOT MK-VI / COPY OF: %CHAMPION% / (YOUR WORST MATCH)`.
HP 20; that champion's damage row (Tables 1/2); its pinch at HP 7.

It is a rematch with your weakest venue, in the museum, before Gamma.

#### 4.3.4 Boss: GAMMA MK-VI (fight `$1E`)

**What it is.** Rockman 3's giant peacekeeping robot: two phases, the second only beaten by a body blow to the head.

**How it is built.** The **Wily 1 Mechazaurus technique**: Gamma is static BG art in NT0 (no split, `$F4` = 0),
standing on the right half (x 144-255, 160 px tall); only hit-box objects take damage, and the body parts reflect
(class `$86`) [engine-ok]. Art ≈ 160 tiles in the freed tank budget [new-art] L. **The twist: its rocket fists** are
two 24×24 sprite objects (3 sprites per line each, to stay inside the 8-per-line limit with Rock) that fly out, slam
down, **become platforms**, and fly back. In phase 2 they rise to its head with Rock standing on them.

**Phase 1, the chest core** (bar 1, 28 HP; the hit box at 64-80 px above the floor, reachable with a jump shot):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **ROCKET FIST** | every 150 f, alternating hands: the shoulder sparks 20 f (the tell); the fist flies at Rock's position at launch (4 px/f), slams into the floor or wall, **stays 60 f as a 24×16 platform**, then flies back to its socket on a curve (3 px/f). **The return path hits** (contact 4): the homing return the Super Adaptor will inherit |
| B | **CHEST CANNON** | every 200 f: 3 shots that bounce once on the floor (2 px/f, 3 damage) |
| C | **QUAKE** (HP ≤ 14) | a stomp shakes the screen 30 f; dust marks 4 spots, then 4 rocks fall there |

Damage, phase 1: W.STORM **4/12 W** (and its Updraft alt lifts Rock to core height: the ranged answer), B.ATTACK
3/16 G, C.FLASH 1/32 R, PUNCH★ 4/24, buster 1/32 (`systems.md` row).

**Phase 2, the cockpit** (bar 2, refilled to 28: the Wily Machine's multi-bar technique). The face plate falls off
with a crash: **Mr. Y** is at the controls, mask on. **SC5: only fists hurt the cockpit** (tap punch 2/30, PUNCH★ and
Time Fist 4/12, Morning Star 3/20, the Super fist 3/20 on replays; everything else dinks). The cockpit is 120 px above
the floor, out of jump reach. The ways up:

- **Ride the fist** (the intended way): a fist slams, rests 40 f, then **rises straight up at 2 px/f to cockpit
  height (60 f), hangs there 60 f** with Rock on it, within punch reach (21-81 px) of the cockpit, then flies back.
- **M.BEAM stairs**: three beams make a staircase (H1's tool, re-examined).
- **Jet up, then swap to Power** in mid-air with SELECT+Left/Right (`systems.md` §1: the quick swap), and punch on the
  way down. A skill route.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **FIST ELEVATOR** | every 200 f, alternating: slam, rest 40, rise 60, hang 60, return |
| B | **COCKPIT LASER** | every 240 f: Mr. Y charges a glow (30 f, the tell) and fires a horizontal laser at cockpit height, sweeping the hanging fist (jump off, or time the ride) |
| C | **CHEST CANNON** | every 250 f, as phase 1 |
| Pinch (HP ≤ 9) | **DOUBLE SLAM** | both fists slam together and both rise; one is a decoy that **rises 2× faster and returns early** (the tell: its speed) |

**The uppercut finale.** The killing blow is always a fist (SC5), so it always gets the flourish: Rock's punch frame
angles upward, an `UPPERCUT!` pop (a nod to the spinning top Gamma once needed), and Gamma's head flies off the top of
the screen. Mr. Y ejects in his pod (*"My MUSEUM!"*) and is gone. Two seconds later the head crashes back down and
cracks open.

#### 4.3.5 The Super Adaptor (12)

Inside Gamma's head is its power core: a capsule stencilled `RUSH SUPER ADAPTOR. PROTOTYPE. ON LOAN FROM THE FUTURE
(1995).` (Rockman 7's adaptor, in a 1993 game: Project SUPER's stolen future tech, and the museum's one exhibit that
"has not happened yet"). Rush runs in and docks: **YOU GET / RUSH SUPER / ADAPTOR** (the weapon-get screen, chain
`$17`; FORMS.SUPER, `systems.md` §2.3; `meta.md` EVENTS2 b4). Screen 12 is a one-screen demo walk-out: a cracked block
behind a pillar that the rocket fist breaks **on its homing return** (it flies past the pillar and curves back), and a
ledge that needs the jet hop. Neither is required; the stage clears at the exit. [new-code] S, Must.

So the Super Adaptor is found **inside Gamma**, at the end of H3, as `systems.md` and `meta.md` assume; H4, H5 and the
Castle then build optional rooms around the homing fist.

#### 4.3.6 Secrets

| Bit | Secret | How | Tell | Tier A | Tier B |
|---|---|---|---|---|---|
| b0 | **GEMINI SYNC** | 09-0B without Gemini Rock ever being destroyed | the copy's reform is visible and costs time | `TWINS LOOK AFTER EACH / OTHER. DON'T LET YOUR / REFLECTION GET HURT.` | `GET THROUGH THE MIRROR HALL WITHOUT YOUR CRYSTAL COPY EVER BEING DESTROYED.` |
| b1 | **THE DOC ROBOT WORKSHOP** (13) | at 05, one press is stuck (it shakes forever and never slams); a full charge or a full punch knocks it down through the floor, opening a ladder | the endlessly shaking press | `ONE PRESS IN THE HALL IS / STUCK. GIVE IT THE PUSH / IT'S BEEN WAITING FOR.` | `HIT THE STUCK NEEDLE PRESS (THE ONE THAT ONLY SHAKES) WITH A FULL CHARGE OR A FULL PUNCH.` |
| b2 | **COPYCAT** | finish Doc Robot MK-VI with the copied champion's own weapon | the boss panel names the copy; SC4's 0-damage joke reaction on the first own-weapon hit is the second tell | `A COPY OF A COPY. FIGHT / IT WITH ITS OWN WEAPON. / IT HATES THAT.` | `FINISH DOC ROBOT WITH THE WEAPON OF THE CHAMPION IT IS COPYING.` |

**13, the workshop**: shelves of Doc Robot skulls labelled with Rockman 2's eight bosses (METAL, QUICK, AIR, CRASH,
FLASH, BUBBLE, WOOD, HEAT: the eight Doc Robot copied) and a ninth labelled `MK-VI: ??? (SEE YOUR SCORECARD)`. The
envelope, and a large weapon energy. b2's reward: an E-tank + 30 bolts.

Hooks: Rush Coil sign K *"We have to jump on the exhibit?"* C *"Authentically."*; Break Man statue (if partnered)
K *"Is that... you?"* Break Man *"No."*; first slide gap C *"The slide! 1990's greatest invention."*; Doc Robot
K *"It's copying your worst match!"* C *"How rude. How educational."*; phase 2 K *"Mr. Y is driving it!"*; the uppercut
C *"UPPERCUT!"*. Heckles: *"My Gamma is twice as tall in person."* / *"Doc Robot has seen your scorecards."*. Deaths:
*"Pressed."* / *"Slide, Rock! The yellow ones!"* / *"His reflection was fine, at least."* / *"Pulled into it."* /
*"Ride the fist! RIDE IT!"* / *"Gamma: still keeping the peace."*

HARD: presses rest 50 f; no slide-gap presses on 06; magnet pull 1.0 px/f; Doc Robot HP 28 and the champion's HARD
branch; Gamma's fists hang 40 f and the decoy fist from the start of phase 2.

Homage moments: jumping on the Rush Coil exhibit against the sign; sliding under a slammed needle press; steering a
mirror twin across a pit you cannot see from your side; Doc Robot in your worst opponent's X-ray; riding Gamma's fist
up and punching Mr. Y; the Super Adaptor "on loan from 1995".

### 4.4 H4 ROCKMAN 4 (1991), id 11: base vanilla Mr. X 2

**Pitch.** The fourth game's wing is Dr. Cossack's citadel, and Kalinka is in the commentary booth, so it is
personal: the charge shot and the Metalls that learned to hide, Bright Man's dark rooms, the citadel's falling chapel
bells, Cossack's Balloon, Dust Man's compactor (with a caged friend), Toad Man's rain, and the Cossack Catcher.

**Tileset.** TS_H4 = a copy of Mr. X 2's (`$2F:$89`; only 157 of 256 tiles referenced, so ≈ 100 free for snow, onion
domes, bells, the crane). Kept: the pink and blue machine blocks, the falling bell row, the pod-column BG technique.
New: MUSEUM third, snow cover, the Balloon, compactor plates, Flip-Top Jr.'s cage, the claw machine cabin and claw.
[new-art] M, Should (H4 is Should).

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | The citadel diorama: snow on the machine blocks, onion domes in the windows. Plaque `ROCKMAN 4 (1991): THE CHARGE SHOT, EDDIE, AND A SCIENTIST WHO WAS FRAMED.` K: *"Papa! It's your castle!"* C: *"...Please don't look at the fourth floor."* | none | | Must |
| **01-02** | v01-v02 | `1991: ROCKMAN LEARNED TO CHARGE. METALLS LEARNED TO HIDE.` Snow Metalls (vanilla `$18`, the punch-only rule, `systems.md` §4.7) | Metalls, drill tanks `$6E` (Drill Man's year) | b1's tell on 02 | [engine-ok], Must |
| **03-05** | v03-v05 | **Bright Man's dark rooms**: the lights go out 3 s in every 6 (the Semifinal's BLACKOUT thread); **flash bulbs** on the walls (shoot one: the room is lit for 10 s); C.FLASH lights it 240 f | Metalls | | [engine-ok] reuse, Must |
| **06** | v06 | **The chapel bells**: vanilla's falling bell row, kept, re-skinned as onion-dome chapel bells. **Each bell rings a note as it drops**, so a clean run plays a scale (b0) | none | | [engine-ok] + SFX, Must |
| **07** | v07 | **WIRE & BALLOON (1991)**: a case with both inventions (plaque `DR. COSSACK'S INVENTIONS. THE WIRE IS ON LOAN. THE BALLOON IS RIGHT THERE.`). The Balloon: a rideable platform that rises 0.5 px/f when stood on and drifts with LEFT/RIGHT; it pops after 8 s and respawns at its post. It carries Rock up a tall gap to 08 | none | A set-piece platform, not a weapon | [new-code] S, Must |
| **08** | v08 | **Checkpoint 1** (vanilla's) | | | Must |
| **09-0D** | v09-v0D | **DUST MAN'S COMPACTOR**: a spiked ceiling descends at 0.25 px/f while you run right (Knight's chain `$11` logic, run here through the stage-attribute table, as `venues_b.md` does for Yamato); junk-block pockets (Power) hold items; **Flip-Top Jr.'s cage at 0B** (b2) | skull drones `$66`, skull walkers `$67` | The ceiling resets at 0E | [new-code] S (attribute hook), Must |
| **0E-0F** | v0E-v0F | **TOAD MAN'S RAIN**: rain sprites (6 at most, cosmetic), and the floor is wet: ice momentum (floor type 5) | Metalls | **Tag pocket** at 0F: an emblem shutter → a large life and a large weapon energy | [engine-ok], Must |
| **10** | v10 | Shutter corridor; **checkpoint 2**. Plaque `COSSACK CATCHER (1991): A CLAW MACHINE WITH A SCIENTIST IN IT.` K: *"That machine took me a lot of places."* | | | Must |
| **11** | v11 | **Boss: COSSACK CATCHER MK-VI** (§4.4.1) | | | Must |
| **12** | new | **Hidden room: KALINKA'S ROOM** | | | Must |

#### 4.4.1 Boss: COSSACK CATCHER MK-VI (fight `$1F`)

**What it is.** Dr. Cossack's claw machine (a "UFO catcher" in Japanese) from Rockman 4. MK-VI is piloted by a
**Kalinka-shaped decoy robot**. K: *"That's not me! I don't look like that! ...Do I?"*

**How it is built.** The **Mr. X 2 pod-column technique**: the cabin (a 64×48 glass dome with the pilot) is BG in NT1
positioned by the scroll above the split, and the floor strip comes from NT0 (chain 7) [engine-ok]. Vanilla moved its
pods vertically only; **the twist**: the cabin also **travels sideways along a crane rail** (the frame's X scroll),
and a **sprite claw** on a sprite chain drops from it and **grabs Rock**. [new-code] M, [new-art] M, Should.

**The arena**: the "prize pit": a flat floor with **three prize capsules** (sprites: a large life, a large weapon
energy, and a `KALINKA PLUSH`, which does nothing; K: *"Papa, why is there a doll of me?"*) that respawn 300 f after
being taken.

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **RAIL** | the cabin slides toward Rock's x at 1.5 px/f, up to 120 f, at rail height (dome 88-136 px above the floor: out of jump reach) |
| B | **CLAW DROP** | stops over Rock; a ding-ding chime and the claw opens 20 f (the tell); **the cabin lowers 48 px** (the vertical scroll: now the dome is in jump-shot reach) and the claw drops on its chain at 4 px/f. If it touches Rock: **GRAB**. Otherwise it closes on what is under it: a prize capsule is lifted and **thrown at Rock** (an arc, 3 damage); nothing is a miss. Then the claw and cabin rise (2 px/f) |
| GRAB | | Rock is lifted at 1 px/f, controls locked except A/B: **10 presses within 90 f** (CASUAL 6) wriggle free. Otherwise `PRIZE GET!` (a jingle): the cabin carries Rock to the prize chute in the left corner and drops him: 6 damage |
| C | **ICICLE SHAKE** (HP ≤ 14) | the cabin rattles the rail; 4 icicles wobble 30 f (the tell) and fall (3 damage) |
| | Cycle | A, B, A, B, C: ≈ 520 f |
| Pinch (HP ≤ 9) | **C.HOPPER** (4MI's roster name, credited) | the claw detaches and hops around the floor on its three fingers like a crab (its own 8 HP, contact 4; destroying it is the style act `PRIZE DENIED`), while the cabin keeps A and drops 2 bombs per pass |

**Hit box**: the dome (the decoy pilot). The claw dinks except as C.HOPPER.

**Damage** (`systems.md` row): Y.SPEAR **4/12 W**, W.STORM 3/16 G, KNIGHT.C 1/32 R, PUNCH★ 4/24.

**Weapons as tools.** KNIGHT.C's Hold catches a prize capsule before the claw does (denying the throw and keeping the
item: the held mace "catches pickups", `systems.md` §3.7); Y.SPEAR's Wall Spear in the side walls gives perches at
dome height while the cabin is up; the slide gets under a falling claw.

**Defeat.** The coin slot spews a fountain of coins (a sprite gag), the decoy pilot pops up on a spring neck, and the
cabin slides off its rail into the prize chute.

#### 4.4.2 Secrets and the friend

| Bit | Secret | How | Tell | Require | Tier A | Tier B |
|---|---|---|---|---|---|---|
| b0 | **BELL CHOIR** | cross 06's bell row in one go, so all eight bells drop in order (a rising scale, then a chord) | the first bell's note; a plaque with a stave of eight notes | - | `EIGHT BELLS, ONE TUNE. / STOP HALFWAY AND THE / CHOIR LOSES ITS PLACE.` | `RUN ACROSS THE CHAPEL BELLS WITHOUT STOPPING OR TURNING BACK.` |
| b1 | **KALINKA'S ROOM** (12) | at 02, a cracked Cossack crest (the "C" emblem) in the ceiling corner is a Power block: a charged punch opens it, and a ladder goes up | the crack in the crest | - | `THE FAMILY CREST IS / CRACKED. A FATHER WOULD / FIX IT. PUNCH IT OPEN.` | `BREAK THE CRACKED COSSACK CREST NEAR THE START WITH A CHARGED POWER PUNCH.` |
| b2 | **FLIP-TOP JR.** | at 0B, a cage on the back wall holds `EDDIE PROTOTYPE (1991)`. Its lock faces the wall: only the **Super Adaptor's rocket fist on its homing return** can strike it (it flies past the cage and curves back). The compactor gives you about 10 s | the lock glints toward the wall; a plaque `THE KEY IS ALWAYS BEHIND YOU.` | SUPER (`meta.md` require 3) | `HE'S LOCKED FROM THE / BACK. YOUR NEW FIST KNOWS / HOW TO COME BACK AROUND.` | `THROW THE SUPER FIST PAST THE CAGE IN THE COMPACTOR. ON ITS WAY BACK IT HITS THE LOCK.` |

**12, Kalinka's room**: a bed, a radio, a stack of drawings (one of Rock), and an empty bird cage with a sign `BEAT
WAS HERE (ROCKMAN 4 MINUS INFINITY)`; a plaque thanking 4MI (PLAN): `THANK YOU, ROCKMAN 4 MINUS INFINITY, FOR
RESCUING HER PROPERLY.` The envelope and a 1-UP. K: *"This is my room! Papa, did you sell my room to a museum?"*

**Flip-Top Jr.** (Eddie debuted in Rockman 4; GP's Eddie runs the shop): freed, he hops out, salutes, and beams away
(*"Eddie's little brother!"*, K). He is a **friend mechanic** (4MI lesson 4): **he appears in the W3 escape** and
throws Rock a large life and a large weapon energy (§5.4), and he rides Eddie's cart in the victory lap (§6.3). 30
bolts.

Hooks: snow Metall C *"They hide under the snow now. Adorable. Lethal."*; first bell K *"Listen! It's singing!"*;
Balloon C *"My balloon! I was wondering where it went."*; grab K *"It's got him! Mash, Rock, MASH!"*; C.HOPPER
C *"The claw has a mind of its own. I never fixed that."*. Heckles: *"Cossack built it. I improved it. You're
welcome."* / *"The claw always wins. Ask the plush."*. Deaths: *"Prize get."* / *"Crushed in the compactor. Very
tidy."* / *"Slipped in the rain."* / *"The lights were off. So was Rock."* / *"The balloon popped. Balloons do."* /
*"Kalinka would've wriggled out faster."*

HARD: lights out 4 s in 6; the compactor at 0.35 px/f; GRAB needs 14 presses; icicles from the start; C.HOPPER at HP
14.

Homage moments: the chapel bells ringing a scale as they fall; riding Cossack's Balloon past his own exhibit; a
rocket fist curving back to spring a caged Eddie; the claw grabbing Rock and carrying him to the prize chute; a
Kalinka-shaped pilot, and Kalinka denying it.

### 4.5 H5 ROCKMAN 5 (1992), id 12: base vanilla Mr. X 4

**Pitch.** The fifth game's wing is "Proto Man's castle" (it wasn't his): Star Man's low gravity, Gravity Man's flips,
Crystal Man's falling crystals, Wave Man's geysers on the shortcut, Beat's letters, the ridable Super Arrow, and **Dark
Man MK-VI disguised as Break Man**, who is now your tag partner, so you can call the real one on him. At the end of the
corridor is a sixth door: the 1993 wing, under construction.

**Tileset.** TS_H5 = a copy of Mr. X 4's (`$2B:$80`; only 159 of 256 blocks used, plenty of room). Kept: the grey
stone castle with red lights, the X crates and drones, cage cylinders, ceiling spiders `$3C`, the open pit branch, the
cowboy gunners `$6C`. New: MUSEUM third, starfield, gravity arrows, crystal emitters, geysers, letter plates, the
Super Arrow launcher, the throne room. [new-art] M, Must.

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Entrance; plaque `ROCKMAN 5 (1992): BEAT, THE SUPER ARROW, AND PROTO MAN'S CASTLE. (IT WASN'T HIS.)` | spiked ceiling unit `$A1` (vanilla) | big WE (vanilla) | Must |
| **01-02** | v01-v02 | **STAR MAN'S SPACE**: a starfield room with **low gravity** (the vanilla water floor type 8: gravity `$00.18`, no bubbles, a space palette) | wheel cannons `$C0/$C9` | Long floaty jumps between cannon ledges over spikes | [engine-ok], Must |
| **03-07** | v03-v07 | **GRAVITY MAN'S FLIPS** (§4.5.1) | X crates `$CB` (drones), cage cylinders `$33` | Letter plates (b0) | [new-code] M, Should; fallback Must |
| **08** | v08 | **CRYSTAL MAN'S CRYSTALS**: ceiling emitters drop crystal orbs (1 every 60 f per emitter, 2 emitters), which shatter on the floor into 4 shards (2 damage) | eye cannon `$54` | | [new-code] S, Must |
| **09** | v09 | **Checkpoint 1** (vanilla's). The open branch 16-18 starts at the right | totem walkers `$12` | | Must |
| **0A-0E** | v0A-v0E | Up and right through the crate halls | ceiling spiders `$3C` | the 1-UP at 0E (vanilla); **tag pocket** at 0C (emblem shutter → an E-tank) | [engine-ok], Must |
| **0F-10** | v0F-v10 | Down; the E-tank at 10 (vanilla) | | | Must |
| **11** | v11 | **Checkpoint 2** | | | Must |
| **12-13** | v12-v13 | **THE SUPER ARROW (1992)**: a launcher fires a ridable arrow every 120 f across a 160-px pit (it flies 2 px/f level, then dips); ride it over | cage cylinders | Plaque `THE SUPER ARROW (1992): A WEAPON YOU COULD STAND ON. WE CHECKED: YOU STILL CAN.` | [new-code] S, Must |
| **14** | v14 | Shutter corridor. On the left wall, **a sixth door**: `ROCKMAN 6 (1993): WING UNDER CONSTRUCTION. KNOCK.` (b1) | | | Must |
| **15** | v15 | **Boss: DARK MAN MK-VI** (§4.5.2), in a throne room with a Proto-Man-style emblem | | | Must |
| **16-18** | v16-v18 | **Branch: WAVE MAN'S GEYSERS** (vanilla's open, risky shortcut, kept): the floating platforms now ride water geysers that rise and fall 32 px on a 120-f cycle; cowboy gunners on them; rejoins at 0F, skipping 0A-0E (and the 1-UP) | `$6C` | | [new-code] S, Must |
| **19** | new | **Hidden room: THE 1993 WING** (§4.5.3) | | | Must |

#### 4.5.1 Gravity flips (03-07)

**GRAVITY ARROWS** [new-code] M, Should: wall panels with an up or down arrow; touching one flips gravity. Rock falls
toward the ceiling, his sprite V-flipped, his floor test reads the tile above him, jumps go down. Rules that keep it
small: flip rooms have **no ladders and only left/right exits**; enemies are not flipped; spikes line both floor and
ceiling; a flip resets to normal at the screen edge. Plaque `GRAVITY MAN (1992): DOWN IS A MATTER OF OPINION.`

**Fallback (Must)**: if the flip code is late, 03-07 become low-gravity rooms (type 8, as 01-02) with ceiling spikes
and the same layouts mirrored to work upright.

#### 4.5.2 Boss: DARK MAN MK-VI (fight `$20`)

**What it is.** In Rockman 5, "Proto Man" kidnapped Dr. Light, and it was Dark Man in disguise. MK-VI is the same
trick, played on a player who now has the real Break Man.

**How it is built.** The **Robot Master framework** (intro `$93`, room controller `$94`, a boss type in the extended
`$31:$9D43` table) [engine-ok]. Phase 1 uses **the tag partner's own Break Man sprite set** with a subtly wrong
palette (an orange scarf instead of yellow: the visual tell), so the disguise costs no art; phase 2 is a new Dark Man
sprite (≈ 64 tiles) [new-art] M. **The twist: the boss panel lies.** Vanilla's typed boss-intro panel
(`$3C:$81B1`, its field layout in `$3C:$85EE-$8615`) types:

```
BREAK MAN
HEIGHT 179   WEIGHT 81
SPECIALTY: DEFINITELY BREAK MAN
```

and when the disguise falls it is **re-typed** over itself:

```
DARK MAN MK-VI
SPECIALTY: DISGUISES (BAD)
```

[new-code] S (re-type call), Must.

**HP 28, two phases on one bar.** Robot scale (`systems.md` row): F.BLAST **4/16 W**, PLANT.B 3/20 G, SILVER.T 1/45 R,
buster 1/60, PUNCH★ 3/30.

Phase 1, **DISGUISE** (28 → 14):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **WHISTLE** | stands and whistles Break Man's melody **with one wrong note** (the audio tell); 180 f the first time, 90 f afterwards; hittable |
| B | **BREAK SHOT** (a copy) | three small shots 12 f apart (2 damage), then a charged shot at f90 (4 damage, 3 px/f) |
| C | **SHIELD JUMP** | jumps toward Rock with a shield up (frontal shots reflect while he is airborne), lands, 30 f |
| | Cycle | A, B, C, B |

At HP 14: **THE MASK SLIPS** (90 f, he is invulnerable): the costume pops off and flies away, a scarf flutters down,
the panel re-types, the music changes.

**Special case (visible code): two Break Men.** If the real Break Man (the tag partner) hits him during phase 1, the
disguise ends at once: his HP drops to 14 if it is higher, and the panel re-types with an extra line, `(EXPOSED BY THE
REAL ONE)`. Break Man: *"Nice scarf. Wrong colour."* This is b2.

Phase 2, **DARK MAN** (14 → 0):

| Id | Pattern | Timeline (frames) |
|---|---|---|
| A | **BARRIER** | 4 orbs orbit him for 120 f; they reflect shots (contact 3) |
| B | **SHOCKWAVE** | a jump (48 px) and a slam: two floor shockwaves (8 px tall, 2 px/f, 3 damage) |
| C | **DARK BALL** | a 32-px ball aimed at Rock at 1.25 px/f; it splits into 4 on hitting a wall |
| | Cycle | A, B, C, B (≈ 380 f) |
| Pinch (HP ≤ 7) | **GRAVITY FLIP** | every 300 f the arena flips for 120 f (H5's own hazard turned on you; he wears magnetic boots and stays put). Fallback: low gravity for 120 f |

**Defeat.** He explodes; his visor flies off, and on its inside is a little stamp: `MADE BY MR. Y`. Then the
unmasking (§4.6).

#### 4.5.3 Secrets, and Mr. X's card

| Bit | Secret | How | Tell | Require | Tier A | Tier B |
|---|---|---|---|---|---|---|
| b0 | **MEGAMAN V** | collect the eight letter plates M-E-G-A-M-A-N-V hidden in H5 (Rockman 5's own letters, which built Beat); a letter row under the life bar fills in | the letters glow; the first one is on the main path at 03 | - | `IN 1992, EIGHT LETTERS / BUILT A BIRD. THE WING / STILL HAS ALL EIGHT.` | `FIND THE EIGHT LETTERS M-E-G-A-M-A-N-V IN THE 1992 WING. THE SHORTCUT HAS TWO.` |
| b1 | **THE 1993 WING** (19) | at 14, knock on the `UNDER CONSTRUCTION` door: any shot or punch is a knock, and a number (1-6) pops over the door. Six knocks within 6 s: *"Oh, the SIXTH one. Come in."* | the `KNOCK` sign; the first knock answers `WHO'S THERE?` | - | `THE SIXTH WING OPENS / FOR THE SIXTH KNOCK. / MIND YOUR MANNERS.` | `KNOCK SIX TIMES, FAST, ON THE UNDER-CONSTRUCTION DOOR BEFORE DARK MAN.` |
| b2 | **TWO BREAK MEN** | hit the disguised Dark Man with the real Break Man | the wrong-note whistle and the wrong-colour scarf | TAG | `TWO WHISTLES, ONE SONG. / ONE OF THEM IS OFF-KEY. / BRING THE REAL ONE.` | `CALL BREAK MAN DURING THE DISGUISE PHASE AND LET HIM HIT THE FAKE.` |
| b3 | **MR. X'S BUSINESS CARD** | on the floor of the 1993 wing | it is the only object on the diorama floor | - | (the rating's T14 hint is Break Man's, `meta.md` §6.2) | |

**19, the 1993 wing**: a diorama of **vanilla Mr. X Fortress 1, screen v00** (the night city and the moon, the 1993
art, untouched), a mannequin of Mr. X (the vanilla reveal sprite) behind a velvet rope, a plaque `ROCKMAN 6 (1993):
"MR. X", THE SHADOW RULER. EXHIBIT IN PROGRESS.`, the envelope, and on the floor **Mr. X's business card**: `MR. X.
SPONSOR, 1ST WORLD ROBOT CHAMPIONSHIP. (NO RELATION.)` Taking it sets RATEFLAGS b1 (`meta.md` T14). After the
post-game unlock U1.5, a door at the back of this diorama is the entrance to Mr. X Returns (§7). The room is the
museum's joke about the game you are playing.

Rewards: b0 30 bolts and a golden Beat whistle in the Museum; b2 30 bolts.

Hooks: Star Man's space K *"Moon jumps!"*; first flip C *"Down is now up. Please adjust."*; crystal K *"Shiny!
...OW."*; Super Arrow C *"Never stand on a weapon, Rock. Except that one."*; the knock K *"Is someone in there?"*;
Dark Man's whistle K *"Was that note wrong?"* C *"Very wrong."*; the mask slips K *"That's not Blues!"* C *"Obviously
not Blues."*. Heckles: *"My Dark Man is a master of disguise."* / *"Proto Man's castle! It was mine all along! Like
everything!"*. Deaths: *"Fell up."* / *"The arrow kept going. He didn't."* / *"Crystal clear."* / *"That geyser was on
a schedule."* / *"Fooled by a scarf."* / *"Gravity: 1, Rock: 0."*

HARD: low gravity rooms with one more spike row; flip rooms with a third flip panel; crystals every 45 f; Super Arrows
every 150 f; Dark Man's phase 1 at full patterns from the start and the gravity pinch at HP 10.

Homage moments: a moon jump over spikes in Star Man's starfield; walking on the ceiling past an X crate; riding a
Super Arrow across a pit; the boss panel typing `DEFINITELY BREAK MAN`, then re-typing it; the real Break Man
exposing the fake; knocking six times on the 1993 door and finding the 1993 game inside, with Mr. X's business card.

### 4.6 Mr. Y's unmasking (after H5; `meta.md` EVENTS b6)

Played in H5's throne room right after Dark Man, built on **vanilla's Mr. X reveal** (the pod sprite, the typed speech
at the top of the screen in the `$6C/$6D` style, the flight path `$39:$8E04` and the object animations `$39:$8DE9`)
[engine-ok] + text, Must. ≈ 25 s.

1. Mr. Y descends in his pod (the vanilla Mr. X pod, recoloured, a Y emblem). *"Impressive! You've toured my entire
   museum! But you will NEVER guess who I really am!"*
2. He pulls off the Y mask. Underneath is **the Mr. X face** (the vanilla 1993 sprite). *"...Wait. Wrong layer."*
3. He pulls off the X mask. **Dr. Wily.** *"It is I, the genius DR. WI—"*
4. Three windows open at once: Cossack, Kalinka, Rock: **"WE KNOW."** Then a fourth, Dr. Light on the radio: *"We all
   knew, Albert."*
5. Wily: *"...You could have SAID something!"* Then: *"No matter! Behold PROJECT SUPER! The age of 8-bit is OVER!"*
   He flies off along the vanilla path.
6. Black screen, typed like vanilla's `$6E`: `THIS TIME, IT'S A SUPER FIGHT!!` (JP: a pun on vanilla's
   こんどは しんけんしょうぶ だ!!).
7. **Vanilla's Wily Fortress picture** (the skull castle with lightning, unchanged 1993 art), then **it upgrades**:
   ExGrafix per-tile palettes bloom over it (§5.1's technique), the MMC5 pulses join the jingle, and the title `SUPER
   WILY CASTLE` slides in. [new-code] S, [new-art] S, Should (the upgrade); the picture itself Must.

After the unmasking, the heckler in W1-W3 is labelled `DR. WI- I MEAN MR. Y` (§0.5).

(TODO: §5 Castle, §6 ending, §7-§10 are being written.)
