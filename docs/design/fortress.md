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
| **05** | S | Upper stand: walks past the **press box** (Cossack and Kalinka in the window, sprites) and the **scoreboard** | none | **The entrant board** (BG text): `1 BLIZZARD ... 8 YAMATO / 9 ROCKMAN / 10 BASS β (SPONSOR: MR. Y) / 11 ?????? (MASKED)`. The 11th line is Break Man's foreshadowing (§2.6). The four lane judges' cards are summed on the board as `WARM-UP 34/40` | [new-art] S, Must |
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
3. The entrant board's line 11: `?????? (MASKED)`.
4. High-fiving Knight Man on his float.
5. Mr. Y's `UPGRADE!` button, and the scoreboard reading `PI-KUN 16-BIT EDITION`.
6. A 128-px balloon chick deflating and zipping around the stadium.

(TODO: §2 onward are being written.)
