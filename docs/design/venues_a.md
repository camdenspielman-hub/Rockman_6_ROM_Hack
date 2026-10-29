# Heritage Venues A: Wind, Knight, Tomahawk, Plant (design-venues-a)

Owner: design-venues-a. Covers four of the eight Heritage Venues:

| Venue | Champion | Vanilla stage | Homage |
|---|---|---|---|
| **SKY ACE 1943** | Wind Man | 1 (`$51` = 1), MECHANICAL TOWER | Capcom's *1942* (1984) and *1943: The Battle of Midway* (1987) |
| **DRAGON QUESTLIKE** | Knight Man | 6, CAPITAL OF SCIENCE | *Dragon Quest* (1986), with a nod to *Zelda II* |
| **GUN.SMOKE FRONTIER** | Tomahawk Man | 5, RESTRICTED AREA | Capcom's *Gun.Smoke* (1985 / FC 1988) and *Wild Gunman* (1984) |
| **JUNGLE PITFALL** | Plant Man | 2, FORGOTTEN AREA | *Pitfall!* (1982), *Pitfall II: Lost Caverns* (1984), *Super Pitfall* (1986) |

Binding inputs: `docs/design/BRIEF.md` (overrides `docs/PLAN.md`), `docs/research/{rm6,cx,r4mi}/SUMMARY.md` and the topic
docs. Vanilla screen numbers below are written **vNN** and come from `docs/research/rm6/img/maps/*.png` and
`docs/research/rm6/levels_stages.md`; GP screen numbers are plain **NN**. Draft text in quotes is a placeholder for
`story.md`, which owns all final dialogue (JP and EN).

Tags, per BRIEF §8: **[engine-ok]** vanilla as-is or data only; **[new-code]**; **[new-art]**; **[new-music]**; size
**S / M / L**; tier **Must / Should / Could**.

New measurement used here (scratch `build/design/design-venues-a/bossmove.py`, 1,440 frames per boss against a
moving, invincible player; logs `bossmove_*.json`, sheets `bossmove_*.png`):

| Boss | What the vanilla AI actually does against a moving player |
|---|---|
| Wind Man | Long fan phases (pull); W.STORM pinwheels `$9A` in pairs at f249, 546, 591, 1198, 1257, 1428; walks/hops across the room only twice in 24 s (f786-811 to x `$98`; f1017-1058 jump, peak y `$6B`) |
| Knight Man | Jumps every 100-350 f (airtime 60-75 f, peaks y `$3E`-`$61`); mace `$96` at f468, 705, 828, 1424 |
| Plant Man | Barrier (4 x `$B3` + `$B5`) raised at f86, 348, 699, 954, 1218 (period 260-350 f); leaps of about 130 f, peak y `$43`-`$48` |
| Tomahawk Man | Tomahawk `$B0` every 100-130 f (f95, 220, 351, 444, 738, 937, 1299, 1382); feather triple `$B1` at f521, 1070, 1183 |

---

## 0. Rules shared by the four venues

### 0.1 Ids and the screen budget

- The four venues keep their vanilla stage ids (1, 6, 5, 2). Their rows in the stage-attribute table (BRIEF §7.2)
  carry the new fields this doc needs: tileset slot, **secret-boss screen** (the generalised `$3F:$F518`), plate
  slot, secret-exit flag index, the debrief predicate list and the HARD poke list.
- A stage is still one strip of at most **32 screens** (`$00-$1F`, `levels.md` §3). Main routes stay in
  `$00-$17`; branches, hidden rooms and second boss rooms use `$18-$1F`, as vanilla does.
- Budget used: Wind 29 of 32, Knight 28, **Tomahawk 32**, **Plant 32**. Tomahawk and Plant have no slack (see Risks).
- No design here needs the new "enter a screen from below without a ladder" exit condition (BRIEF §4). Every upward
  exit is a ladder; every balloon or lift ride stays inside one screen.

### 0.2 How the secrets are built (uniform)

| Secret | Rule | Mechanism |
|---|---|---|
| **Secret exit** | An alternate route that ends in a **second boss room**. Killing the boss there sets the venue's secret-exit flag (new save bit, `meta.md`) and, in Knight and Tomahawk, the plate bit | Vanilla's own plate mechanism: exits with explicit targets into `$18-$1F` plus the boss-screen test `$3F:$F4EB`/`$F518`, moved into the stage-attribute table [engine-ok] S Must |
| **Hidden room** | Exactly one screen (4MI convention), off any route, with a visible tell | One extra exit with a target, or a door warp (T3) |
| **Behaviour-gated item** | A chip earned by *how* you play a set piece, never bought | A per-venue counter in work RAM, tested when the reward object spawns |
| **Plates** | Knight keeps **A**, Tomahawk keeps **B**, both in their vanilla boss rooms (`$1A`, `$1F`). Wind and Plant had none and get none | Unchanged plate logic [engine-ok] |

Secret exits feed the Exhibitions (BRIEF §3): **Wind + Knight unlock E1**, **Tomahawk + Plant unlock E2**.

Debrief (4MI's predicate table, BRIEF §5.4): each venue lists its predicates in order; the first one missed prints
its hint. Hints are written below in full (EN draft); none are placeholders.

### 0.3 Adaptor and partner rules

Power arrives after the 2nd win, Jet after the 4th (BRIEF §4). **No normal exit needs an adaptor.** Gates in these
venues:

| Venue | Needs Power | Needs Jet | Needs nothing special |
|---|---|---|---|
| Wind | item pocket 04 (vanilla v03 block) | none (the sortie lends a Jet) | secret exit, hidden room, behaviour item |
| Knight | 1-up pocket 01 (vanilla); **or** the two basement walls (keys also open them) | none | secret exit (search), hidden room, behaviour item |
| Tomahawk | Energy Balancer 1C (vanilla, kept) | sky bypass 18-1A (vanilla quirk, kept) | secret exit (bounties), hidden room, behaviour item |
| Plant | underground wall 19 → 1A (a shortcut; Break Man's charge shot also breaks it) | none | secret exit (the cat), hidden room, behaviour item |

Every venue can be the player's first. Break Man (tag partner, BRIEF §5.6) gets one optional interaction per venue
(§1.9, §2.9, §3.9, §4.9); none is ever required.

### 0.4 Tech these venues use

PLAN's ids T1-T8 are kept; tech specific to this doc is prefixed **VA-**. Owners: `tech.md` builds the engine
pieces; this doc owns the data and the per-venue objects.

| Id | What | Used in | Tags |
|---|---|---|---|
| **T1-lite** "fixed-camera ride" | The camera is locked on one or two screens; raster bands scroll by time (plus camera, for parallax); a **wave director** object spawns enemies from a data list (frame, kind, x, y, path id). No true autoscroll: nothing solid moves, so collision and spawns stay vanilla. Band art loops every 512 px, so no column streaming is needed except where noted | Wind sortie 01 and wing arena 1D, Tomahawk train 10-11 | [new-code] M Must |
| **T2** text window + choice | Bottom window, typewriter, YES/NO and 2-4 item menus (the BRIEF §7.5 text engine) | all four; Knight heavily | [new-code] L Must (shared) |
| **T3** switch → target | Doors (enter with UP), keys, chests, gates, lamp boards, lifts that ride through a down exit | Knight, Tomahawk, Wind | [new-code] M Must (shared) |
| **T4** raster band list | Up to 4 bands per frame, each with its own X scroll (and Y for one band); built on the generic double-buffered raster list (BRIEF §7.1). Reuses vanilla chain C (parallax), E/F (sunset shimmer) and 7 (fixed floor) as band presets | Wind, Tomahawk; Plant keeps chain 7 | [new-code] M Must |
| **T5** pendulum | Scripted swing angle θ(t) = A·sin(2πt/T); grab when airborne and touching the bottom 16 px; release with A keeps the tip velocity | Plant vines, Plant Man | [new-code] M Must |
| **T8** multi-part boss | Several hit boxes, one controller (the gorilla tank pattern) | Wind's AYACO bomber | [new-code] M Should |
| **VA-GUST** push zone | Horizontal force on the player, lifted from Wind Man's own pull code (AI `$31:$8AFC`), with a direction and a schedule | Wind decks, Wind Man | [new-code] S Must |
| **VA-TIMED** timed hazards | (a) rideable-when-closed platform (vanilla lift `$A0` code plus a state); (b) **toggling floor**: flip the alternate-metatile bits in `$0340` on a timer and repaint the 2x4 metatile area. Vanilla only ever sets those bits | Plant croc heads, tar pits, Plant Man | [new-code] S Must |
| **VA-SEARCH** search verb | DOWN held 24 f while standing still on a floor (not on a ladder top) probes a "search spot" object under Rockman | Knight | [new-code] S Must |
| **VA-DRAW** quick-draw | READY / DRAW! prompt, RNG delay, reaction window, FOUL detection, reaction-time readout | Tomahawk saloon and boss | [new-code] S Must |
| **VA-ENCOUNTER** | Screen lock with vanilla shutters, music swap, T2 command menu, a wave, a victory chest | Knight | [new-code] M Must |

New objects take the generic id + sub-id pattern (4MI's `$5E`, CX's `$40`/`$41` directors) once `tech.md` fixes it;
vanilla has only about 30 free type ids (`rm6/SUMMARY.md` §3). This doc names objects `OBJ_*`.

### 0.5 Lag and sprite budget

About 10 live objects fill a frame (`engine.md` §8). Every set piece below states its cap, counting up to 3 player
shots. The worst vanilla offenders in these four stages (Plant 09-0D at 21 % lag, Knight 0B-0C at 14 %) are thinned
on purpose.

### 0.6 Commentators

Cossack (C) and Kalinka (K) pop up in the bottom window (BRIEF §5.5): ≤ 2 lines, toggleable, never during a
reaction-time prompt. Each venue lists its **event hooks** and a **rotating death table** (6 lines, played in
order, then the generic table). All lines are drafts for `story.md`.

### 0.7 Tileset slots

Each venue gets its own new tileset slot (BRIEF §4): a fresh copy of the vanilla 16x16 metatile and 32x32 block
tables in a new bank (`tech.md` assigns it), so new blocks never collide with a bank-mate. **Tile ids stay the
binding limit** (256 BG tiles live at once). New art therefore enters as extra **CHR sets swapped into one third of
the BG table by screen exits** (`$0A00-$0FFF` or `$0000-$01FF`, exactly as vanilla's `$91`/`$95`/`$98` sets do), and
large set pieces are sprites or one-off BG bosses. Each section lists which CHR state each screen uses.

---

## 1. Wind Man: SKY ACE 1943

**Pitch.** Wind Man's floating Mechanical Tower hovers over a mock sea battle. You are catapulted off the Committee
carrier on Rush Jet, fly a two-minute 1943-rules sortie, land on the tower's flight deck and climb it through
changing winds. 1942/1943 are played through their **rules**: energy that drains in flight, POWs you shoot to change,
the limited loop, red squadrons, the giant bomber, and the "SHOOTING DOWN %" tally at the landing.

Vanilla facts used: layout `$32:$A800`; tileset `$2C:$80` (blocks 232/256, BG tile ids 248 used / 8 free); base
CHR `$83`, extras `$8C` (tower), `$8D` (open sky), `$8E` (dark base); palette `$17`; music `$00`; checkpoints v08
and shutter v14; boss `$99`, AI `$31:$8AFC`; weakness C.FLASH (4); W.STORM landed once in 7 s of glued shots
(`stages_b.md` §5). No raster split anywhere in vanilla Wind.

### 1.1 Tileset slot and art

| Item | Content | Tags |
|---|---|---|
| Slot **TS_WIND** | Copy of `$2C:$80` tables; 24 free block ids plus reclaimed ones | [engine-ok] S Must |
| Kept (vanilla CHR) | `$83` sky, clouds, coral girders, gold pillars, green tower shaft, fans and updraft tiles; `$8C`, `$8D`, `$8E` (dark base) | [engine-ok] |
| **W-CARRIER** (new third, `$0A00-$0FFF`, ~96 tiles) | Grey steel deck, deck stripes, catapult track, arresting wires, lamp board, elevator rim, the tower's girder landing strip | [new-art] M Must |
| **W-SEA** (new third, ~64 tiles) | Sea band (512-px loop), distant islands, the destroyer silhouette for the sea band | [new-art] S Must |
| **W-HANGAR** (new third, ~96 tiles) | Hangar interior, parked fighters as BG, bomb racks, the wing's top surface for 1C-1D | [new-art] M Should |
| AYACO bomber | Must: sprite build (48x24, 4 engine parts). Should: BG art in the sky band (~110 tiles, loaded only during its phase) | [new-art] M Must / L Should |
| Sprites | Propeller Met fighter (green and red), gold leader, Kite Met, deck crew Met, seagull, POW / 3-WAY / AUTO / YASHICHI icons, LOOP icons "R", lamp icons, windsock, loop pose of Rockman on Rush (4 frames) | [new-art] M Must |

### 1.2 Screen-by-screen

CHR state column: B = base `$83`, C = W-CARRIER, S = W-SEA, T = `$8C` tower, O = `$8D` open sky, D = `$8E` dark base,
H = W-HANGAR.

| GP | From | CHR | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|---|
| **00** | new (replaces v00) | B+C | Walks right across the Committee carrier's deck to the catapult and stands on it (launch after 40 f, or press UP) | Deck crew Met waving flags (harmless) | **Catapult launch**: 60-f cut, Rush and Rockman shot off the bow. If Jet is not owned yet: a "RENTAL" bib on Rush and the card "COMMITTEE LOANER JET" | [new-code][new-art] S Must |
| **01** | new | B+S | **The sortie** (§1.3), 2 min, camera locked | waves (§1.3) | POW cycling, LOOP, energy drain, red squadrons, destroyer, AYACO | T1-lite, T4 [new-code] L Must |
| **02** | new | B+C | Lands automatically (1942 landing glide, 90 f); tally "SHOOTING DOWN 87%"; **checkpoint 1**. Walk right (main) or ride the **elevator** down (secret) | none | **Lamp board**: 4 lamps, one per red squadron destroyed. At 4/4 the elevator unlocks. **Re-sortie catapult** at the left end relaunches into 01 without dying | T3 [new-code] S Must; re-sortie Should |
| **03-05** | v01-v04 (4 → 3) | B+T | Climbs the green tower shaft by ladders | `$27`/`$28` panda drums (2 per screen max), `$29` crawler | Item pocket on 04 behind the vanilla v03 breakable (tiles `$0C-$0F`), big energy, charged Power punch | [engine-ok] S Must |
| **06** | v05 | B+T | Top of the tower; first windsock | `$2D` stompers, `$1B` bomber | **First gust** (§1.4), shown once with a commentator line; updrafts `$A` over fans `$C` (vanilla) | VA-GUST S Must |
| **07** | v06 | B+T | Gust deck with two updraft columns | `$36` tops, `$1B` | Gust L/R alternating | Must |
| **08** | v07 | B+T | Gust deck under the **ceiling spikes** (vanilla v07 spikes): a strong gust while you ride an updraft pushes you sideways under them | `$2D`, `$36` | Gust timing is the puzzle | Must |
| **09** | v08 | B+O | Open sky with floating girders | `$34` shield-cars, **Kite Mets** | Kite Mets ride the gust and drop straight down when it stops | [new-code][new-art] S Should |
| **0A** | v09 | B+O | Open sky; **hidden-room tell**: a seagull stands on one cloud | `$34` | The only solid cloud (§1.6) and a rope ladder's last 16 px at the top of the screen | [engine-ok] S Must |
| **0B** | v0A | B+O | Gust deck, then the ladder up (vanilla v0A up exit) | `$36`, `$34` | Gust on the ladder's approach | Must |
| **0C** | v0B+v0C (2 → 1) | B+O | Ladder climb; 1-UP on a side ledge (vanilla v0B) | `$75` beetle | | [engine-ok] S Must |
| **0D** | v0D | B+O | Right along the top | `$27` | | [engine-ok] Must |
| **0E-10** | v0E-v10 | B+D | Down the second tower into the dark engine base | `$59` big robot (v0E), `$29` | | [engine-ok] Must |
| **11-12** | v11-v12 | B+D | Rubble floor under ceiling spikes, then up | `$36`, `$27` | **Engine fans**: constant push zones (left, 0.5 px/f) under the vanilla ceiling spikes, so every jump drifts | VA-GUST S Must |
| **13-14** | v13-v14 | B+D | Shutters; **checkpoint 2** at 13 | | | [engine-ok] Must |
| **15** | v15 | B | **Wind Man** (§1.7): the purple tower top; a windsock on the left wall | | Should: the cloud band behind the arena scrolls (T4) to sell the speed | Must; band Should |
| **18** | new | B+H | Secret: rides the elevator platform down from 02 | none | Lift object rides through 02's down exit (target `$17` → 18) | T3 S Must |
| **19-1A** | new | B+H | Hangar bays: walk between parked fighters | deck crew Mets with wrenches, rolling bomb carts (2 max) | Bomb carts roll along the floor like logs; F.BLAST detonates them | [new-code][new-art] M Should |
| **1B** | new | B+H | Ladder up through the wing hatch | | | Must |
| **1C** | new | B+H | Shutter corridor **on the wing** of the airborne AYACO; **checkpoint 2b** | | Clouds rush past (T1-lite band) | Should (fallback: hangar corridor) |
| **1D** | new | B+H | **Secret boss room: WING WALKER** (§1.7.4). Kill sets the Wind secret-exit flag | | Open wing edges; gusts | Must room; Should arena |
| **1E** | new | B | **Hidden room** "WEATHER BALLOON" | | | Must |
| 16, 17, 1F | - | | unused (3 spare) | | | |

Checkpoints: 02 (after the sortie), 13 (shutter), 1C (secret shutter). A death in the sortie restarts at 00, which is
one screen and a launch (about 4 s).

### 1.3 The sortie (screen 01)

**SKY ACE mode** [new-code] M Must: Rockman rides Rush Jet freely in 8 directions at 1.5 px/f, no gravity, no
stamina use (the fuel bar is hidden). Screen clamp x 16-232, y 24-200. B fires the Jet buster (or the equipped
weapon, if `systems.md` allows forms to fire weapons). **A = LOOP** (1942): a 48-frame loop-the-loop of radius 20 px
with full invincibility; 3 loops per sortie, shown as three "R" icons under the life bar; +1 per POW taken as POW
(max 3).

**1943 energy rule.** Life drains by 1 HP every 600 f in flight (CASUAL: off; HARD: every 360 f). Contact with a
plane costs 3, a bullet 2. That is about 12 HP over the whole sortie, and the four POWs give back up to 24.

**Bands (T4).** Sky band y 0-151 (clouds, loops every 512 px, 1 px/f); sea band y 152-239 (W-SEA, 2 px/f). Cloud
sprites at 3 px/f are optional foreground.

**Wave list** (t in seconds from launch; the director spawns from data, so HARD and CASUAL are just other lists):

| t | Wave | Count | Path | Notes |
|---|---|---|---|---|
| 0-1 | Launch | | | "TAKE OFF!" |
| 3 | Fighters | 5 | line from the right, sine path | Propeller Mets (HP 1, contact 3) |
| 8 | Fighters | 5 | V from the upper right | |
| 14 | Fighters | 3 | **from behind** (left edge), overtake and turn | 1943's surprise from the rear |
| 20 | **Red squadron 1** | 5 | 1942 loop path across the middle | All 5 down → POW, lamp 1 |
| 28 | Bombers | 2 | vanilla `$1B` green bombers, re-pathed, dropping red balls | |
| 35 | Shield-cars | 4 | vanilla `$34` in a column | |
| 42 | **Destroyer** | 1 | BG ship in the sea band, 64 px, scrolls through in 12 s | 2 flak turrets (hit-box objects, HP 3) fire upward bursts every 70 f |
| 50 | **Red squadron 2** | 5 | from behind | POW, lamp 2 |
| 58 | Tops | 3 | vanilla `$36`, homing slowly | |
| 65 | **Red squadron 3** | 5 | pincer, 3 from the top and 2 from the bottom | POW, lamp 3 |
| 78-113 | **AYACO** | 1 | enters from the right, cruises in the right half, bobs ±8 px | §1.3.2. Leaves after 35 s if alive |
| 115 | **Red squadron 4** | 5 | wide V with a **gold leader** | POW, lamp 4 |
| 120 | Landing | | the flight deck slides in from the right | → screen 02 |

Lag cap: 5 planes + 2 enemy bullets + 3 shots = 10 at the worst instant of a red squadron (the POW only appears
once the last plane is down); the director delays a wave by up to 30 f while 8 or more objects are live.

#### 1.3.1 The POW (1943)

The last plane of a red squadron drops a POW that drifts left at 0.5 px/f and leaves the screen after about 6 s.
**Shooting it cycles it** and knocks it 8 px up (it can be juggled):

| Shown | Taken | Effect |
|---|---|---|
| **POW** | +6 HP, +1 LOOP | |
| **3-WAY** | 15 s | buster fires 3 shots at -20°, 0°, +20° |
| **AUTO** | 15 s | hold B: one shot per 6 f, 4 on screen |
| (back to POW) | | |
| **YASHICHI** | 8 hits on the same POW within 240 f turn it into Capcom's spinning pinwheel | full HP, 3 LOOPs, and on the first take ever the **YASHICHI chip** (§1.6) |

#### 1.3.2 AYACO, the big bomber (1942's boss, parody name)

| Part | HP (proposal; `systems.md` owns damage) | Behaviour |
|---|---|---|
| Engines x4 | 6 each | Smoke when below half. F.BLAST is the best tool (one of VARIETY's "best somewhere" spots) |
| Tail gun | 4 | 3-shot burst at Rockman every 90 f |
| Bomb bay | - | Opens every 240 f, drops 1 bomb Met that falls and bursts in 4 pellets |

All four engines destroyed: AYACO tilts and falls out of the sky band (band Y scroll +1 px/f, smoke sprites), +STYLE
(`systems.md`). Lag cap: 4 engines + gun (controller merged into the gun) + 1 bomb + 1 bullet + 3 shots = 10.

#### 1.3.3 The tally

On 02: "SHOOTING DOWN 87%" (planes destroyed / planes spawned; AYACO counts as one plane), typed in the 1942 style,
then the lamp board lights one lamp per completed red squadron. 100 % plays a fanfare and a commentator line; the
percentage is a Record (`meta.md`).

### 1.4 Gusts (06-0B, 11-12)

`OBJ_GUSTCTL`, one per screen, with a windsock sprite at the top of the screen (VA-GUST).

| Phase | Frames | What you see and hear |
|---|---|---|
| CALM | 120 | windsock limp |
| WARN | 30 | windsock stiffens toward the coming direction; whoosh SFX; leaf/debris sprites start to blow |
| GUST | 150 | push 0.75 px/f on the ground, 1.0 in the air (Jet included) |

The direction list is per screen data (06: L, R; 07: R, R, L; 08: L only, toward the spikes; 0B: R, L). W.STORM
tornados ride a gust; Kite Mets ride it and fall when it stops. Engine fans (11-12) are a GUST phase that never ends,
0.5 px/f, no windsock (the fan art is the tell).

### 1.5 Secret exit: the ace's elevator

- **Requirement**: destroy all five planes of each of the **four red squadrons** in one sortie. No adaptor.
- **Tells**: the 4 lamps are drawn on the lamp board next to the elevator and as icons in the sortie HUD; a lamp
  pings and lights mid-sortie the moment a squadron is wiped; the elevator's sign reads "ACES ONLY"; the re-sortie
  catapult sits on the same screen so a player can retry without dying.
- **Route**: 02 elevator ↓ 18 → 19-1A hangar → 1B ladder ↑ → 1C wing → **1D WING WALKER**. The kill sets the flag.
- **Debrief hint**: "FOUR RED SQUADRONS, FOUR LAMPS. THE ELEVATOR ONLY TAKES ACES."

### 1.6 Hidden room and behaviour item

**Hidden room 1E "WEATHER BALLOON"** [engine-ok] S Must.
- Entry: on 0A, one cloud is solid (one metatile with collision 1 and cloud art: CX's "clouds are not floors",
  inverted). A seagull stands on it and squawks every 4 s. A rope ladder's bottom 16 px hangs above it; climbing
  takes the up exit (target `$1D` → 1E).
- Content: the balloon's gondola: an E-tank, two large weapon energies, a 1-UP (`systems.md` sets the drops).
- Exit: ladder down back to 0A.
- Hint: "A SEAGULL WAS STANDING ON A CLOUD. CLOUDS AREN'T FLOORS... ARE THEY?"

**Behaviour item: the YASHICHI chip** [new-code] S Must.
- Earned by juggling one POW through 8 hits (§1.3.1). The first time the pinwheel is taken, the chip is granted.
- Proposed effect (`systems.md` decides): once per stage, a hit that would kill you at 2+ HP leaves 1 HP (the 4MI
  Skull Amulet idea, in Capcom's oldest secret item).
- Tells: the POW visibly changes on the first hit; Kalinka comments on the first change ("It changes when you shoot
  it!"); the pinwheel is a famous Capcom secret.
- Hint: "SHOOT THE POW. THEN KEEP SHOOTING IT."

Predicate order for the debrief: hidden room → YASHICHI → secret exit.

### 1.7 Boss: Wind Man, "MASTER OF WIND"

Arena: v15 (purple tower top, gold pillar floor), windsock on the left wall. HP and damage per `systems.md`
(vanilla HP 27). The vanilla AI already owns the hardest parts (the fan pull, the pinwheels, the cross-room hop);
the rework adds a **blow** phase and the 1943 pinch.

#### 1.7.1 Patterns (frames at 60 Hz)

| Id | Name | Timeline | Notes |
|---|---|---|---|
| A | **HEADWIND** | 0: fans turn on, **push Rockman away** 0.75 px/f (1.0 in the air) for 180 f. f30 and f90: a W.STORM tornado rolls along the floor at 2 px/f toward Rockman (contact 3). Each tornado stops at the far wall and becomes an **updraft column** for 60 f | Jumping into the column lifts you to y `$40`: the same updraft W.STORM's alternate fire gives you (teaching) |
| B | **CROSSWIND HOP** | 10-f crouch, jump to the other third of the room, peak y `$6B`, 50 f | vanilla move |
| C | **SUCTION** | **Pull** toward him 0.75 px/f for 150 f (vanilla). f40 and f100: two pinwheels `$9A` launched up, falling at Rockman's x. Touching his fan blades: 4 | vanilla move, timed |
| | Cycle | A, B, C, B (430 f) | Windsock always shows the current direction |

#### 1.7.2 Pinch (HP ≤ 9): SKY ACE

- **D: 1943 LOOP** (72 f) opens every cycle: a vertical loop of radius 40 px, then a dive at Rockman's last x
  (contact 4). Shots ping off him during the loop.
- **E: RED SQUADRON** (at most once per 1,200 f): 5 Propeller Mets cross the top in a V at 2 px/f. All 5 down →
  a POW that cycles exactly as in the sortie (3-WAY lasts 10 s here). The boss uses the venue's own mechanic.
- In A and C the wind flips every 90 f (the windsock flips first: 12 f of warning).

#### 1.7.3 Weapons in this fight

| Weapon | Effect | Tags |
|---|---|---|
| **C.FLASH (weakness)** | **STALL**: his fans stop for 120 f (no push, no tornados, no pinwheels); if airborne he drops; smoke puffs sputter from his propellers; the windsock goes limp. With C.FLASH's time-stop alternate (if `systems.md` keeps PLAN's Up+B), the stall lasts 180 f. Short i-frames per BRIEF §5.1 | [new-code] S Must |
| **W.STORM** | Special case in code (CX lesson 7): **absorbed**. No damage; his suction gets +50 % for 60 f. This turns vanilla's "W.STORM landed only once" quirk into a rule. K: "He LIKES that!" | [new-code] S Must |
| Charged Power punch | Knocks him out of B or D (lands him) | [new-code] S Should |
| Jet form | Headwind halves Jet speed; a tailwind doubles it: a preview of W.STORM's Jet synergy "Tailwind" (PLAN) | Should |

Defeat (Should): his propellers spin down and he spirals to the floor like a paper plane.

#### 1.7.4 Secret room 1D: WING WALKER

Same AI, fought on top of AYACO's wing as it flies: cloud band rushing past at 3 px/f (T1-lite), wing edges open (a
fall is a pit death), 16-px lips at both ends so a grounded Rockman cannot be pushed off by the fans alone, only
while jumping. Pinch at 12 HP instead of 9. Must: the room and the fight; Should: the moving-sky arena (fallback:
the hangar with the night revisit palette).

### 1.8 HARD pokes (per section; 4MI model)

| Section | Poke | Kind |
|---|---|---|
| Sortie | Drain every 360 f; red squadrons fly at 2.5 px/f and each plane fires once (still 5, for the lag cap); destroyer turrets HP 5; AYACO engines HP 8 and a second tail gun; 2 LOOPs at start | wave list + constants |
| Sortie | POW drifts at 0.75 px/f (shorter juggling window); YASHICHI still needs 8 hits | constant |
| 06-0B | GUST 1.0 / 1.25 px/f; WARN 30 → 20 f; two updraft columns on 07 removed (blocks `$A` → air) | constants + layout poke |
| 08 | One more spike row under the ceiling (layout poke) | layout |
| 11-12 | Engine fans 0.75 px/f | constant |
| Wind Man | Pinch at HP 13; A's push 1.0 px/f; RED SQUADRON every 900 f; tornados 2.5 px/f | AI branch |

### 1.9 Commentator hooks and partner

| Event | Hook (draft) |
|---|---|
| Launch | C: "Rock is cleared for takeoff!" |
| First POW shot | K: "It changes when you shoot it!" |
| A red squadron wiped | K: "Red squadron down!" (lamp pings) |
| AYACO appears | C: "That's not a plane. That's a bigger plane." |
| AYACO shot down | K: "AYACO is going down!" |
| Tally 100 % | C: "One hundred percent! In my day we called that an ace." |
| First gust | K: "Watch the windsock, Rock!" |
| Elevator unlocks | C: "The elevator's moving. Where is he going?" |
| W.STORM on Wind Man | K: "He LIKES that!" |
| First C.FLASH hit | C: "His engines stalled! No wind, no Wind Man!" |
| Deaths (rotation) | "Mayday, mayday!" / "He forgot the loop button." / "Gone with the wind." / "The windsock tried to warn him." / "That cloud was NOT a floor." / "Even 1942 gave you three loops!" |

**Break Man**: the call is greyed out during the sortie ("NO PASSENGERS"); on the decks the gusts push him at half
strength (his scarf flaps). No tag-only shortcut. Should.

### 1.10 Homage moments (the screenshot list)

1. The catapult launch off the Committee carrier, Rush in a RENTAL bib.
2. Juggling a POW through 3-WAY and AUTO until it spins into a Yashichi.
3. The LOOP button: Rush loop-the-loops through a bullet curtain, three times per sortie.
4. AYACO, the four-engined bomber, falling out of the sky in smoke.
5. "SHOOTING DOWN 87%" on the deck, and four lamps that decide the secret exit.
6. A seagull standing on the one cloud that is a floor.
7. Wind Man flying a 1943 evasive loop, then calling his own red squadron.
8. C.FLASH stalls his fans and he sputters to the floor.
9. The secret fight on the wing of the airborne bomber.

### 1.11 Weapons as tools in this venue (VARIETY)

B.ATTACK's spread vs formations; C.FLASH wipes a whole formation and stalls Wind Man; F.BLAST on AYACO's engines and
the hangar bomb carts; Y.SPEAR through `$34` shield-cars; SILVER.T's arc vs Kite Mets above you; W.STORM's
updraft reaches the hidden ladder without the seagull's cloud; charged Power punch opens the 04 pocket.

---
## 2. Knight Man: DRAGON QUESTLIKE

**Pitch.** Knight Man's castle is run as a Dragon Quest theme park, "TANTE-GP CASTLE". A King gives you the quest,
signs and sages talk, chests hold MAGIC KEYS that locked doors eat, corridors throw **ENCOUNTER!** command windows
at you, the vanilla spike ceiling becomes a monster with HP, a Metal Metslime runs away with the critical-hit chip,
and the hidden stairs are where Dragon Quest put them: behind the empty throne. Knight Man narrates his own attacks
in a battle log, which makes every move telegraphed.

Vanilla facts used: layout `$33:$B000`; tileset `$2D:$80` (blocks 255/256, metatiles 155, BG tile ids 250 / 6
free); one BG set `$9E` for the whole stage plus torch animation `$9F-$A1` on v08-09 (`$39:$888A`); palettes
`$74`/`$78`/`$82`/`$CD`/`$7B` and distinct **revisit palettes** in bank `$28`; music `$07`; collision group 2.
Spike ceiling v03-06: script `$3F`, init `$39:$8833`, IRQ chain `$11` (handler `$C337`, **logic inside the IRQ**),
latch `$B0`, collision offset for stage 6 at `$3E:$DA40`. Checkpoints v0B and v16 (plate route v19). Plate **A** in
room v1A through the Power pillar in v15 (charged punch) and two more Power walls in v18. Boss `$95`, mace `$96`,
shield = attack class 3 (front shots reflect; only the full punch always hits); weakness Y.SPEAR (4).

### 2.1 Tileset slot and art

| Item | Content | Tags |
|---|---|---|
| Slot **TS_KNIGHT** | Copy of `$2D:$80` tables (Knight shares bank `$2D` with Centaur in vanilla; the new slot ends that coupling) | [engine-ok] S Must |
| Kept | `$9E` green stone castle, battlements, purple and red halls, arched windows, chains, spiked ceilings, banners, blue machine hall, gates, ladders; torches `$9F-$A1`; the sunset sky of v00; the revisit palettes | [engine-ok] |
| **K-DQ** (new third, ~48 tiles, swapped in on 01, 0A-0D, 15) | Two thrones (32x32), stone tablet, inn bed, cracked floor and trapdoor, the hidden-stairs metatiles (the alternate set of the v15 pillar) | [new-art] S Must |
| Window frame | The DQ-style white frame on black comes from the T2 text engine's font set (shared with `story.md`) | [new-art] S Must (shared) |
| Basement | No new tiles: v18-1A keep `$9E` under a black palette with sconce sprites | [engine-ok] |
| Sprites | King, Sage, Innkeeper, Princess Roll (Roll in a gown), chest (closed/open), Killer Chest, Metslime, Metal Metslime, ceiling winch, sconce flame, MAGIC KEY icon, Roll's Love heart | [new-art] M Must (Princess, Innkeeper: Should) |

### 2.2 Screen-by-screen

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Starts on the tower top under the sunset. The **Sage** at the gate (UP to talk): "TO READ A SIGN, PRESS ↑. TO SEARCH, STAND STILL AND PRESS ↓." Drops down | none | Teaches both verbs | T2, VA-SEARCH S Must |
| **01** | v01 | **The King's hall.** The King: "O DESCENDANT OF LIGHT! THE KNIGHTLORD AWAITS. TAKE THIS KEY." The tutorial chest sits on the floor in the path (unmissable): MAGIC KEY 1. Searching behind the King's throne: "THOU FINDEST NOTHING. THIS IS NOT THAT THRONE." (false lead) | `$29` armadillo | 1-UP behind the vanilla Power block (charged punch) | T3 [new-code] S Must |
| **02** | v02 | Down the shaft; a **locked door** at the bottom eats key 1, then right | `$3D` pod (1, not 3) | "THOU HAST NO KEY." if somehow keyless (the chest is unmissable) | T3 S Must |
| **03-06** | v03-v06 | **The Trap Hall** (§2.4): fight the ceiling or run under it | `$6E` lance knights (3) | Spike ceiling with 4 winches; palette cycle `$75-$77` kept | [new-code] S Must |
| **07** | v07 | Up | `$65` skeleton robot | | [engine-ok] Must |
| **08-09** | v08-v09 | **Tower of torches** (torch CHR animation kept) | `$67` swooper | The green ring blocks (collision `$D`) stay F.BLAST pockets: one holds a large weapon energy, the other 30 bolts in a pouch | [engine-ok] S Must |
| **0A** | v0A | Tower top; **Princess Roll** at a window (§2.6) | none | "BUT THOU MUST!" | T2 S Should |
| **0B** | v0B | **Checkpoint 1** = the **INN** (§2.6) | none | Innkeeper YES/NO | T2 S Should (the checkpoint itself Must) |
| **0C** | v0C | **ENCOUNTER 1** at x `$40` (§2.3) | 3 Metslimes, 1 Killer Chest | Victory chest: MAGIC KEY 2 | VA-ENCOUNTER M Must |
| **0D** | v0D | Walks on, then up (vanilla up exit). **Hidden-room tell**: a floor glint at x `$A0` (§2.7) | none (items: 2 small energies, vanilla) | Search → trapdoor → down exit (target `$1D` → 1E) | VA-SEARCH S Must |
| **0E-0F** | v0E-v0F | Climb | `$70` red spearman as the ROYAL GUARD | | [engine-ok] Must |
| **10** | v10 | The vanilla high E-tank now sits in a **chest** on the same ledge (y `$17`) | `$C6` riders ("Drakee riders", 2) | | [engine-ok] S Must |
| **11** | v11 | Down | `$3C` (vanilla) | | [engine-ok] Must |
| **12** | v12 | **"A METAL METSLIME APPEARS!"** (§2.7) | Metal Metslime | It flees after 240 f | [new-code] S Must |
| **13-14** | v13-v14 | **ENCOUNTER 2** at 13 x `$60` in the blue machine hall: "KNIGHT GUARDS DRAW NEAR!" | 2 `$6E` lance knights, `$3A` mines (2) | Victory chest: MAGIC KEY 3 | VA-ENCOUNTER Must |
| **15** | v15 | **The empty throne** stands on the arch platform. Behind it is the dip with the vanilla Power pillar. **Search** there (or charged-punch the pillar, the vanilla way) → hidden stairs ↓ 18. Main route: right to the shutter | `$2D` (2) | §2.5 | VA-SEARCH S Must |
| **16** | v16 | Shutter corridor, **checkpoint 2** | | | [engine-ok] Must |
| **17** | v17 | **Knight Man** (§2.8) | | Battle log in the window | Must |
| **18** | v18 | **Charlock basement**: dark (§2.5); two **locked doors** where vanilla had two Power walls (a key **or** a charged punch opens each); the vanilla spike pit | `$2D`, `$3A` | Sconces; RADIANT | T3 S Must |
| **19** | v19 | Shutter corridor, **checkpoint 2b** | | | [engine-ok] Must |
| **1A** | v1A | **Secret boss room: THE KNIGHTLORD** (§2.8.4). Kill: KNIGHT.C + BEAT A-PARTS + secret-exit flag | | The offer | Must |
| **1E** | new | **Hidden room** "LIGHT'S TABLET" | | | Must |
| 1B-1D, 1F | - | unused (4 spare) | | | |

Checkpoints: 0B (inn), 16 (shutter), 19 (secret shutter).

Key economy (DQ1 keys are consumable): 3 keys (01, 0C, 13) for 3 doors (02, and the two in 18). **Running from an
encounter forfeits its chest**, so a player who runs needs the charged Power punch for one of the basement doors.
Keys are not kept after the stage. The key count shows next to the life bar while in this venue.

Lag: the vanilla 14 % stretch (v0B-0C, `$2E` with `$3D`/`$3E` pairs) loses its pods; the encounter caps at 4 enemies
+ 3 shots + the chest = 8.

### 2.3 ENCOUNTER! (VA-ENCOUNTER)

Fixed triggers, never random (Time Attack needs determinism; the joke is that the window *says* it is random).

| Step | Frames | What happens |
|---|---|---|
| Trigger | 0 | Rockman crosses the trigger x. The music cuts |
| Transition | 16 | The DQ window grows from the centre (reduced flashes: a fade instead of a flash); vanilla shutters close both screen edges |
| Window | - | "A METSLIME DRAWS NEAR! / COMMAND?" ▶FIGHT RUN SPELL ITEM; BATTLE theme starts |
| FIGHT | - | Window closes; the wave spawns |
| RUN | - | 1st try: "BUT THOU WERT BLOCKED!" and the enemies get a free hop. The menu comes back after 60 f. 2nd try: "ROCK RAN AWAY." Shutters open, enemies vanish, **no chest, no EXP**, and kills do not count for VARIETY |
| SPELL / ITEM | - | Open the vanilla pause menu on the weapon row / the E-tank row, then FIGHT |
| Victory | - | "THOU HAST DONE WELL. ROCK GAINED 12 EXP." A chest drops (MAGIC KEY); shutters open; the stage music resumes |

Enemies:

| Object | HP | Behaviour |
|---|---|---|
| `OBJ_METSLIME` | 1 | A Metall's helmet on a slime's teardrop body; hops toward Rockman (period 48 f, 24-px hops), contact 2. Hides under the helmet like a Metall when shot from the front at range (shots ping off) | [new-art][new-code] S Must |
| `OBJ_KILLERCHEST` | 6 | Looks like the victory chest. Opens when Rockman is within 40 px; bites (contact 4) and hops twice, then shuts (invulnerable while shut). The real chest is a different colour once you know | [new-art][new-code] S Must |

EXP and levels (Could): EXP from encounters, the ceiling and the Metal Metslime; at 30 and 100 EXP a level-up
fanfare: "ROCK'S LEVEL WENT UP! (ROBOT MASTERS DO NOT LEVEL UP.)" No stat changes.

### 2.4 The Trap Hall: the ceiling draws near

Vanilla: the spiked platforms on chains descend over v03-06 while the IRQ latch climbs (`$7D` → `$A3` in 220 f) and
`$069C` drives both the split and the collision offset.

GP twist (one twist on one vanilla set piece, CX lesson 5): **the ceiling is a monster with HP.**

- On entering 03: a non-blocking window "THE CEILING DRAWS NEAR!" (90 f; play continues).
- `OBJ_WINCH` x4 (two in 04, two in 05) hang under the ceiling platforms; each object reads `$069C` every frame and
  rides with the platform (no IRQ change needed for the motion). HP 3 each.
- All four destroyed: "THE CEILING IS DEFEATED! ROCK GAINED 8 EXP." A flag makes the ceiling **retract** (`$069C`
  back toward 0 at 1 px per 2 f) and stay up for the rest of the stage, including after deaths.
- Not destroyed: vanilla behaviour, unchanged.
- Engine note: the ceiling's motion logic runs inside IRQ handler `$11`. The retract needs one flag test where
  `$069C` is stepped. If `tech.md` moves this logic out of the IRQ while porting to the raster list (recommended:
  a per-frame controller object writes `$069C`, the raster list only places the split), the test lives there.
  [new-code] S Must.

### 2.5 Secret exit: the hidden stairs behind the empty throne

Dragon Quest's most famous secret: in the Dragonlord's castle the throne is empty, and searching the floor behind it
reveals the stairs down to the real Dragonlord.

- **Requirement**: stand in the dip **behind the empty throne** on 15 and search (DOWN, 24 f). No adaptor.
  - The search sets the same `$0340` bits as breaking the vanilla pillar, so the pillar's alternate metatiles are
    drawn as **stairs** going down (new alternate art, K-DQ).
  - The vanilla way still works: a fully charged Power punch opens it too (K: "That is NOT how you find secret
    stairs!"). This keeps the vanilla secret (BRIEF §6, keep quirks) and adds the homage.
- **Tells**: the King's throne at 01 is occupied, this one is empty; the Sage at 00 taught the search verb; the King's own throne at 01 is the deliberate false lead ("THIS IS NOT THAT THRONE"); Roll's Love
  pulses on 15 (Should).
- **Route**: 15 ↓ 18 (dark basement, two locked doors) → 19 → **1A KNIGHTLORD**.
- **The dark basement** [engine-ok + new-code S]: 18-19 start with the BG palette black (the vanilla dark-room
  precedent: Yamato v0E, Plant's gorilla rooms). **RADIANT**: every shot fired lights the BG for 30 f, then it fades
  back over 16 f. Two sconces (`OBJ_SCONCE`, HP 1): shoot both and the room stays lit. F.BLAST lights both at once.
- **Debrief hint**: "THE KNIGHTLORD'S THRONE IS EMPTY. WHY? SEARCH WHERE NO ONE SITS."

### 2.6 NPCs: King, Sage, Inn, Princess

| NPC | Where | Lines (draft) and effect | Tags |
|---|---|---|---|
| King | 01 | Quest giver; gives key 1 (chest). Joins the death table: "DEATH SHOULD NOT HAVE TAKEN THEE, ROCK. I WILL GIVE THEE ANOTHER CHANCE." | T2 S Must |
| Sage | 00 | Teaches ↑ read and ↓ search; second line after a death: "THE THRONE OF A LORD WHO NEVER SITS HIDES SOMETHING." | T2 S Must |
| Innkeeper | 0B (checkpoint) | "WELCOME TO THE INN. ONE NIGHT IS 20 BOLTS. ▶YES NO". YES: fade to black, a 2-s inn jingle, full HP and weapon energy, "GOOD MORNING. THOU SEEMST TO HAVE SLEPT WELL." The checkpoint sign reads "THY DEEDS HAVE BEEN RECORDED." | T2 S Should; jingle [new-music] S Could |
| **Princess Roll** | 0A | Roll (pit crew, BRIEF §2 cameo) in the venue's princess costume. "DOST THOU LOVE ME, ROCK? ▶YES NO". **NO → "BUT THOU MUST!"** and the question again, forever (after 10 NOs: "...FINE. THE COSTUME IS HOT, ROCK."). YES: she gives **ROLL'S LOVE**: for this venue, a heart beside the life bar pulses within one screen of a secret (0D's glint, 12's Metslime, 15's throne). A tell-helper, not a secret | T2 S Should |

### 2.7 Hidden room and behaviour item

**Hidden room 1E "LIGHT'S TABLET"** [engine-ok + VA-SEARCH] S Must.
- Entry: on 0D a floor tile glints for 8 f every 4 s (the only glint in the venue). Search on it: a trapdoor opens
  (alternate metatiles), drop through the down exit (target `$1D` → 1E).
- Content, after Erdrick's tablet in DQ1: a stone tablet: "I, THOMAS LIGHT, HAVE LEFT THIS FOR MY DESCENDANT. TELL
  NO ONE. ESPECIALLY NOT WILY." An E-tank and a 1-UP.
- Exit: ladder up to 0D.
- Hint: "SOMETHING GLITTERED ON THE FLOOR OF THE HALL. THOU DIDST NOT SEARCH."

**Behaviour item: the KAISHIN chip** (DQ's critical hit, *kaishin no ichigeki*) [new-code][new-art] S Must.
- `OBJ_METALMETSLIME` on 12: "A METAL METSLIME APPEARS!". HP 8; **every hit does exactly 1** whatever the weapon
  (visible special case); 2-f i-frames; hops erratically at 2 px/f; flees through the right edge at f240 ("THE
  METAL METSLIME ESCAPED!"). It returns on the next visit to 12 (after a death, or a replay).
- Killed: "AN EXCELLENT MOVE! ROCK GAINED 1000 EXP." and the chip drops. Proposed effect: PLAN's Critical Chip
  (1/16 chance of double damage with a chime). `systems.md` owns the numbers.
- Best tools: many small hits, not big ones (B.ATTACK's four flakes, an AUTO-style rapid buster if `systems.md` has
  one, KNIGHT.C's return pass hitting twice).
- Tells: its own announcement and its escape line; Roll's Love pulses here.
- Hint: "METAL ONES FLEE FAST. HIT THEM OFTEN, NOT HARD."

Predicate order: hidden room → KAISHIN → secret exit (with plate A).

### 2.8 Boss: Knight Man, "MASTER OF MACE BALL"

Arena: v17 (red hall, blue banners). Vanilla HP 27. Rhythm kept from vanilla (jumps of 60-75 f, mace about every
240 f) but every move is **announced in a one-line battle log** (the T2 window; its position is Open question 8) a
fixed lead time before it starts. The commentators stay quiet during the log; they speak only at the weakness hit and the kill.

Intro: "KNIGHT MAN DRAWS NEAR! / COMMAND?" ▶FIGHT RUN. RUN: "BUT THOU WERT BLOCKED!" (always, he is a boss) and
Knight Man gets the first action.

#### 2.8.1 Patterns

| Id | Log line | Lead | Action | Vulnerable? |
|---|---|---|---|---|
| A | "KNIGHT MAN ATTACKS!" | 30 f | Mace `$96` sweeps along the floor across the room (60 f out, 40 f back); jump it | **Yes**: shield down for the whole 130 f |
| B | "KNIGHT MAN IS GUARDING." | 20 f | Walks at Rockman 1 px/f for 90 f, shield up (front shots reflect, vanilla class 3), then a **shield bash** lunge of 32 px in 12 f (contact 4) | From behind only |
| C | (none: it is a physical move) | 10-f crouch | High jump onto Rockman's x, peak y `$3F`, 72 f airtime (vanilla). Landing **quake**: a grounded Rockman is stunned 16 f | In the air |
| D | "KNIGHT MAN CASTS BLAZE!" | 40 f cast pose, shield lowered | 3 fireballs: along the floor, +15°, +30°, 2 px/f, contact 3 | **Yes** during the cast |
| | Cycle | | B, A, C, B, D, C (about 650 f) | |

#### 2.8.2 Pinch (HP ≤ 9): "KNIGHT MAN IS ENRAGED!"

| Id | Log line | Action |
|---|---|---|
| E | "KNIGHT MAN SWINGS THE MORNING STAR!" | The mace orbits him (radius 28 px, 1 turn per 40 f) for 120 f while he walks at Rockman, then he flings it as a returning flail. This is KNIGHT.C's orbit alternate and its tap, shown before you own them |
| F | "KNIGHT MAN CASTS HEALMORE!" | Once per fight (HARD: twice). 45-f cast, shield down. **Any hit during the cast** → "THE SPELL FIZZLED!". Otherwise +6 HP |
| | Cycle | E, C, A, F (once), D, B |

#### 2.8.3 Weapons in this fight (special cases in visible code)

| Weapon | Effect | Tags |
|---|---|---|
| **Y.SPEAR (weakness)** | **Pierces the shield**, even from the front during B. The DQ critical chime and "AN EXCELLENT MOVE!", a 24-f stagger with the shield knocked aside. Short i-frames | [new-code] S Must |
| Fully charged Power punch | The first one that hits the shield from the front: "THE SHIELD BROKE!". The shield is gone for the rest of the fight (no more reflect); his palette loses the shield colour | [new-code] S Must |
| KNIGHT.C | Mace meets mace: a CLANG spark, both bounce, no damage | [new-code] S Should |
| C.FLASH | "A SPELL THAT HITS ALL ENEMIES": ordinary damage, but it interrupts HEALMORE from anywhere | Should |

#### 2.8.4 Secret room 1A: THE KNIGHTLORD

- He sits on the real throne. Window: "IF THOU WILT JOIN ME, I WILL GIVE THEE HALF THE BRACKET. ▶YES NO".
  - **YES** (CX lesson: a Yes that hurts): the screen tints red. "THEN HALF THE BRACKET IS THINE..." then "THY
    TOURNAMENT IS OVER. TAKE NOW A LONG, LONG REST." A DISQUALIFIED card, **one life lost**, respawn at 19.
    C: "Did he just take the deal?!" K: "Dad, he pressed YES." [new-code] S Must.
  - **NO**: "THEN THOU ART A FOOL!" The fight starts with BLAZE.
- Same AI; pinch at HP 12.
- **TRUE FORM** (Could): at 0 HP, "KNIGHT MAN REVEALS HIS TRUE FORM!" He refills 12 HP in a red palette with a taller
  plume, and BLAZE comes every cycle. The kill line: "THOU HAST BROUGHT PEACE TO THE BRACKET. AGAIN."
- Kill: "YOU GET KNIGHT.C AND BEAT A-PARTS" (vanilla script `$6A`) plus the secret-exit flag.

### 2.9 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| Encounters | RUN never succeeds; 4 Metslimes and 2 Killer Chests in encounter 1; encounter 2 adds a third lance knight | data |
| Trap Hall | Winch HP 3 → 5; latch step ×1.5 | constants |
| 08-09 | One F.BLAST pocket becomes a spike pocket (bait) | layout |
| 12 | Metal Metslime flees at f150 | constant |
| 18 | RADIANT lasts 15 f; one sconce is placed behind the spike pit | constant + object list |
| Knight Man | Log lead times 30/20/40 → 18/12/28 f; HEALMORE twice; the broken shield regrows after 600 f | AI branch |

### 2.10 Commentator hooks and partner

| Event | Hook (draft) |
|---|---|
| First encounter | K: "A random encounter! In a ROCKMAN game?" C: "It is not random. I checked." |
| RUN blocked | C: "You cannot run from a tournament, Rock." |
| Ceiling defeated | K: "He beat the ceiling. Can you DO that?" |
| Metal Metslime escapes | C: "They always get away. Always." |
| Search finds the stairs | K: "Stairs! Behind the throne! Just like the old days!" |
| Charged punch opens them instead | K: "That is NOT how you find secret stairs!" |
| Shield broke | C: "Shield down! Now we have a fight!" |
| First Y.SPEAR hit | K: "Right through the shield!" |
| The offer: YES | as in §2.8.4 |
| Deaths (rotation) | King: "DEATH SHOULD NOT HAVE TAKEN THEE..." / "Rock was defeated. The judges are not pleased." / "He should have stayed at the inn." / "The ceiling won that round." / "Thou art... out of HP." / "That chest had teeth!" |

**Break Man**: with him called, RUN always works ("BREAK MAN RAN AWAY. NOBODY WAS SURPRISED."). Princess Roll asks
him instead: "DOST THOU LOVE ME?" "...No." "BUT THOU MUST!" (he whistles and leaves the screen). Should.

### 2.11 Homage moments

1. The stage starts with a King: "O DESCENDANT OF LIGHT!"
2. "A METSLIME DRAWS NEAR! COMMAND?" in a Rockman game, and "BUT THOU WERT BLOCKED!"
3. The spike ceiling has HP, and dies.
4. "BUT THOU MUST!" until you say yes.
5. A Metal Metslime that takes exactly 1 damage from everything, then runs.
6. Stairs behind the empty throne.
7. The Knightlord's offer: say YES and the game puts you to sleep.
8. A boss that announces every attack in a battle log, and a HEALMORE you can interrupt.
9. Light's tablet in the hidden room: "ESPECIALLY NOT WILY."

### 2.12 Weapons as tools in this venue

Y.SPEAR pierces Knight Man's shield; F.BLAST opens the `$D` torch pockets and lights the whole basement; B.ATTACK's
flakes kill the Metal Metslime; C.FLASH is the "group spell" in encounters and stops HEALMORE; KNIGHT.C's return
pass double-hits; SILVER.T arcs over the lance knights' shields in the Trap Hall; W.STORM lifts Metslimes off the
floor (they flip and are stunned 60 f); charged Power punch: 01's 1-UP, the throne pillar, the basement doors.

---
## 3. Tomahawk Man: GUN.SMOKE FRONTIER

**Pitch.** A frontier town in Tomahawk Man's desert, run as a Capcom western. Three WANTED posters at the trailhead
name three bounties (Gun.Smoke's posters); a main-street shooting gallery mixes outlaws with townsfolk you must not
hit; the saloon hosts Wild Gunman quick-draws with a reaction timer; the 4:50 train crosses the desert at sunset
with tunnels and a mounted outlaw alongside; claim all three bounties and the Sheriff lets you take "the back way"
to Tomahawk Man's hideout. The boss fight opens, and later punctuates itself, with a draw at high noon.

Vanilla facts used: layout `$33:$A800`, **all 32 screens used**; tileset `$2C:$89` (221 blocks, 212 metatiles, BG
tile ids 255 / 1 free); base CHR `$94` (desert), `$96` (cave), `$95` (sunset), `$D7` (boss corridor); palettes
`$50` / `$51` / `$95`; music `$06`. **Desert parallax**: script `$29`, init `$39:$86C0` (`$0672` = `$2E`, `$0677` =
`$0C`, chain C at line 46, X = camera/2). **Sunset shimmer**: script `$21`, init `$39:$85D8` (latch `$1F`, chain E
then F every 2nd line, 20 times), which also writes checkpoint v0A. Dome dispenser `$4F` (HP 14) on v05 and v10.
**Secrets kept**: plate **B** in room v1F via the right-hand ladder of v12 (no adaptor; `$F518[5]` = `$1F`);
**Energy Balancer** (`$8A`, `$0696`) in v1C via the charged-punch block at v13's left; **sky bypass** v18-1B via
Rush Jet from v0A's hanging ladder (column 4, rows `$00-$1F`; E-tank, big WE, big HP; drops into v0D). Boss `$9F`, AI
`$31:$93EA`, tomahawk `$B0`, feathers `$B1`; weakness PLANT.B (4).

### 3.1 Tileset slot and art

| Item | Content | Tags |
|---|---|---|
| Slot **TS_TOMAHAWK** | Copy of `$2C:$89` tables (35 free block ids before reclaiming) | [engine-ok] S Must |
| Kept | `$94` desert, mesas (the parallax strip), cacti, signposts, blue metal pillars, orange pipes, mesh; `$96` cave; `$95` sunset sky and sun disc; `$D7` boss corridor | [engine-ok] |
| **T-TOWN** (new third, ~96 tiles) | False-front buildings, windows and doors for the gallery, boardwalk, water tower, outhouse, WANTED board with three posters, store signs | [new-art] M Must |
| **T-SALOON** (new third, ~96) | Bar, bottles, mirror, piano, swinging doors, a skylight (for the sky-bypass drop) | [new-art] M Must |
| **T-TRAIN** (new third, ~80) | Car roofs and couplings, station platform, rails and ties for the near band (512-px loop), wheels (CHR animation, 4 frames, the torch technique) | [new-art] M Must |
| **T-BOOTHILL** (new third, ~48) | High-noon mesa top with grave markers for the boss room | [new-art] S Should (fallback: vanilla v17 mesh room) |
| Sprites | Tumbleweed, outlaw, pianist, lady with parasol, Eddie behind a store window, Six-Shot Sam, Sheriff, conductor, Sidewinder on a robot horse (32x32, 4-frame gallop), tunnel mouth (32x48), dust devil, bounty stamp, "DRAW!" / "FOUL!" text sprites | [new-art] M Must |

### 3.2 Screen-by-screen

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | **The WANTED board** (UP reads each poster; §3.3). Then right | none | Desert parallax (chain C, vanilla) | T2 S Must |
| **01-02** | v01-v02 | Desert trail | `$6C` gunners on crates (vanilla), tumbleweeds (1 at a time; shot: a small bolt) | Vanilla breakables kept as Power pockets (01: two blocks on tile ids `$1C-$1F`; 02: the E-tank inside a block) | [engine-ok] S Must |
| **03-04** | v03-v04 | Down into the canyon mine (cave CHR `$96`) | `$6C`, `$12` walker (re-skinned as a cactus walker: Could) | | [engine-ok] Must |
| **05** | v05 | **Bounty 1: DOMINGO DOME**, the vanilla dome dispenser (`$4F`, HP 14) wanted for claim-jumping. Locked screen (vanilla) | `$15` walkers, `$14` rocks (vanilla spawns) | The kill stamps "BOUNTY CLAIMED" over the poster icon | [engine-ok] + S Must |
| **06-08** | v06-v08 | The mine, then up | `$6E` drill tanks, `$18` turrets | F.BLAST blows TNT crates open (one holds a W-tank: per `systems.md`) | [engine-ok] S Should |
| **09** | v09 | Dark mesh shaft up into town | `$70` | | [engine-ok] Must |
| **0A** | v0A | **Sunset main street**; **checkpoint 1** (vanilla). The hanging ladder (sky bypass, Jet) is kept exactly | none | Sunset shimmer (chains E/F, vanilla) | [engine-ok] Must |
| **0B-0C** | v0B-v0C | **The gallery** (§3.4): walk the street while windows and doors pop. The **outhouse** stands at 0C's right end (hidden room, §3.7) | outlaws; civilians | Sign: "PLEASE DO NOT SHOOT THE PIANIST. HE IS DOING HIS BEST." | [new-code][new-art] M Must |
| **0D** | v0D | **The saloon**: **Bounty 2: SIX-SHOT SAM**, best of three quick-draws (§3.5). The sky bypass drops in here through the skylight (vanilla's 1B → 0D exit, kept) | Sam | Piano stops when you land from the roof | VA-DRAW S Must |
| **0E-0F** | v0E-v0F | Down to the **station**; the conductor: "ALL ABOARD!" at the platform's end | `$29` (v0E), `$59` (v0F) | | [engine-ok] Must |
| **10-11** | new (replaces v10-v11) | **The 4:50 train** (§3.6): walk the roofs of four cars while the desert rushes by; **Bounty 3: SIDEWINDER** | `$6C` robbers (2 max), Sidewinder | Tunnels; T1-lite + T4 (three bands) | [new-code][new-art] L Must |
| **12** | v12 | **Junction station**, **checkpoint 2**. Middle ladder (main) up to 13. The right-hand ladder (vanilla's plate route) is barred by the **Sheriff's gate** (§3.7) | `$12` (1) | Sheriff hands out the SHERIFF STAR | T3 S Must |
| **13** | v13 | Vanilla junction, unchanged: left ladder up (main); left end of the corridor: the charged-punch block over the spike pit → **1C Energy Balancer**; top-right pocket (only from 12's right ladder) → right edge → **1D** | | | [engine-ok] Must |
| **14-15** | v14-v15 | Mesa climb at sunset | `$64`/`$66` drones re-skinned as **vultures** dropping `$A4` (Could), `$67` skull walkers | | [engine-ok] Must |
| **16** | v16 | Shutter corridor (script `$4E`), **checkpoint 3** | | | [engine-ok] Must |
| **17** | v17 | **Tomahawk Man, HIGH NOON** (§3.8) | | T-BOOTHILL arena | Must; art Should |
| **18-1A** | v18-v1B (4 → 3) | **The sky bypass** ("VULTURE PASS"), vanilla: Jet up 0A's hanging ladder; lifts `$A0` over spikes, rising bubbles `$08`; the E-tank, big WE and big HP in 1A; 1A drops down into 0D (through the skylight) | | Skips the gallery (and its civilians) | [engine-ok] Must |
| **1B** | new | **Hidden room "THE OUTHOUSE"** (§3.7) | | | T3 S Must |
| **1C** | v1C | **Energy Balancer** room, vanilla, kept (`$8A` object; the item becomes the Energy Balancer chip per `systems.md`) | | | [engine-ok] Must |
| **1D-1E** | v1D-v1E | **The back way**: corridor and shutters (vanilla), **checkpoint 3b** | | | [engine-ok] Must |
| **1F** | v1F | **Secret boss room: THE HIDEOUT** (§3.8.4). Kill: SILVER.T + BEAT B-PARTS + secret-exit flag | | | Must |

The main route keeps vanilla's 24 screens (00-17). The second dome dispenser (v10) and the v11 claw screen give way
to the train. Checkpoints: 0A (town), 12 (after the train), 16 (shutter), 1E (secret shutter). Vanilla sets
checkpoints from any screen script (`LDA #s / JMP $8416`), so the third one is data [engine-ok].

### 3.3 Bounties (Gun.Smoke's posters)

| # | Poster (draft) | Where | Claimed by | Pays (proposal, `systems.md` owns) |
|---|---|---|---|---|
| 1 | "WANTED: DOMINGO DOME. CLAIM-JUMPING. 300 BOLTS" | 05, the mine | killing the dispenser | 300 |
| 2 | "WANTED: SIX-SHOT SAM. CARD SHARP. 500 BOLTS" | 0D, the saloon | winning the best of three | 500 |
| 3 | "WANTED: SIDEWINDER. TRAIN ROBBERY. 800 BOLTS" | 10-11, the 4:50 | knocking him off the train before the third tunnel | 800 |

Poster icons with a CLAIMED stamp sit in the pause screen while in this venue. Bounties persist through deaths
within the stage. A missed Sam or Sidewinder can be retried after a death before checkpoint 2 (both respawn at
checkpoint 1, 0A) or on a replay; once checkpoint 2 (12) is reached, only a replay brings the train back. "Prize money" is
BRIEF §1's theme made literal.

### 3.4 The gallery (Wild Gunman's saloon game, Hogan's Alley rules)

`OBJ_POPUP` in 8 window/door spots over 0B-0C; a data list per screen gives (spot, kind, delay), started by camera
position; at most 3 open at once; about 14 pops per walk-through.

| Kind | HP | Behaviour |
|---|---|---|
| Outlaw | 1 | Appears, shows a "!" for 24 f, fires one bullet at Rockman (2 px/f, contact 2), ducks after 60 f |
| Pianist | 1 | Holds sheet music. Never shoots |
| Lady | 1 | Parasol. Never shoots |
| **Eddie** | 1 | Behind "EDDIE'S GENERAL STORE". Never shoots. Hitting him: "HEY! I'M ON YOUR TEAM!" |

Hitting any civilian: a "HEY!" pop, the **civilian counter** goes up, and that civilian ducks for good. The counter
drives the behaviour item (§3.7). Players who take the sky bypass skip the gallery entirely; the counter stays 0 and
the Sheriff treats them as clean (the bypass is the "ride around town" option).

### 3.5 The quick-draw (VA-DRAW)

Used by Sam (0D) and by Tomahawk Man (17). All movement is locked except B.

| Step | Frames | Detail |
|---|---|---|
| Walk-up | ~60 | The screen locks; Rockman auto-walks to his mark (x `$40`), Sam stands at x `$C0` |
| READY | random 45-150 (HARD 30-180) | From the vanilla RNG (`$C88D`). "READY..." in the window; commentators are muted |
| **DRAW!** | window **W**: NORMAL 20, CASUAL 40, HARD 12 | Big "DRAW!" sprite, a bell SFX (audio tell for accessibility), Sam's hat glints |
| Win | | Any fire within W hits him: he falls; the readout shows your time in seconds to two places, "0.23" (Wild Gunman's timer). Best time is a Record (`meta.md`) |
| FOUL | | Firing during READY: "FOUL!" and Sam shoots (4) |
| Late | | No fire within W: Sam shoots (4) |
| Match | | Best of three. Win 2: bounty 2. Lose 2: "COME BACK WHEN YOU'RE FASTER." The doors unlock, no bounty. Coming back (after a death or a replay) allows a rematch |

Any weapon counts as a draw; C.FLASH during READY is a FOUL like any other shot.

### 3.6 The 4:50 train (T1-lite + T4)

- **Board** at 0F's platform end → 10. The camera may scroll 10 ↔ 11 as Rockman walks the four cars (static BG);
  the world moves instead:

| Band | y | Content | X scroll |
|---|---|---|---|
| Sky | 0-79 | sunset sky and sun disc (`$95`), shimmer kept (chain E/F) | 0 |
| Mesas | 80-127 | the vanilla mesa strip | camera/2 + 0.5 px/f (chain C, plus a time term) |
| Train | 128-191 | car roofs and couplings, static | camera |
| Near ground | 192-239 | rails, ties, telegraph poles (T-TRAIN loop) | camera + 3 px/f |

- **Timeline**: tunnels at t = 15, 30 and 45 s; arrival at 55 s ("JUNCTION! ALL OFF!") → screen 12.
- **Tunnel**: 90 f before, a whistle SFX and a "TUNNEL!" sign passing in the near band. Then `OBJ_TUNNEL` (a
  32x48 sprite wall at roof height) sweeps right to left at 4 px/f. Safe: **slide** (normal form) or stand in a
  **coupling gap** between cars, 24 px lower (any form: Power and Jet cannot slide). Hit: 4 damage and a knockback
  toward the rear. Inside: 90 f with every band's palette black; only sprites show (two bats).
- **Robbers**: vanilla `$6C` gunners re-pathed to climb up from the couplings every 8 s and shoot along the roof;
  at most 2.
- **SIDEWINDER** (bounty 3), `OBJ_SIDEWINDER`, HP 10: rides along the ridge in the mesa band (above roof level,
  so B.ATTACK, SILVER.T arcs and jumping shots reach him) firing 2-shot bursts every 90 f; after each tunnel he
  jumps onto the caboose roof for a 150-f showdown, then back to the ridge. Still alive at the third tunnel: he
  escapes into it ("SIDEWINDER GOT AWAY!"), no bounty.
- **Lag cap**: 2 robbers + Sidewinder + 2 bullets + tunnel + 3 shots = 9.

### 3.7 Secret exit, hidden room, behaviour item

**Secret exit: the back way** [T3] S Must.
- **Requirement**: all three bounties claimed. No adaptor.
- **The gate**: the Sheriff (a Metall with a star) stands at 12's right-hand ladder behind a barrier. UP to talk:
  "BOUNTIES: 2 OF 3. THE BACK WAY IS FOR DEPUTIES." With 3 of 3: "WELL I'LL BE. YOU'VE EARNED THE BACK WAY, DEPUTY."
  The barrier lifts. The route behind it is vanilla's plate route, geometry unchanged: right ladder → 13's
  top-right pocket → 1D → 1E → **1F THE HIDEOUT**.
- **Tells**: the posters at 00 (and their icons in pause); the Sheriff's line names the count; the barrier is
  visible from the middle ladder.
- **Debrief hint**: "THE SHERIFF ONLY OPENS THE BACK WAY FOR A DEPUTY WITH THREE BOUNTIES."
- This **re-homes the vanilla B-plate gate on purpose**: vanilla's gate was just "pick the other ladder"; GP keeps
  the rooms and the plate, and gives the choice a reason.

**Hidden room 1B "THE OUTHOUSE"** [T3] S Must.
- Entry: the outhouse at 0C's right end rattles and shows "OCCUPIED". Shoot its door 3 times (Gun.Smoke reveals
  its secrets to gunfire): the sign flips to "VACANT" and the door swings open; UP to enter (door warp → 1B).
- Inside it is far bigger than outside: "THE GOLD MINE VAULT", a 1-UP, two bolt sacks, a W-tank (`systems.md`).
  The door back returns to 0C.
- Hint: "SOMETHING IN TOWN WAS RATTLING. IN GUN.SMOKE YOU SHOOT WHAT LOOKS ODD."

**Behaviour item: the SHERIFF STAR chip** S Must.
- Earned by reaching the Sheriff (12) with the civilian counter at 0. He pins it on you: "NOT ONE TOWNSFOLK HURT.
  WEAR THIS, DEPUTY."
- Proposed effect (`systems.md`): bounty and boss payouts +25 % (a found version of PLAN's Judge's Favor).
- Tells: the pianist sign at the gallery's start; the "HEY!" pop on every civilian hit.
- Hint: "THE SHERIFF SAW YOU SHOOT AT TOWNSFOLK. READ THE SIGN BY THE PIANO."
- Moral flavour (BRIEF §5.3 asks for one moral trade-off recipe somewhere; `systems.md` owns it): Eddie in the
  store window is the obvious candidate, for example "shooting Eddie drops a big bolt sack but closes the shop's
  discount tier". Proposed only.

Predicate order: hidden room → SHERIFF STAR → secret exit (with plate B). The Energy Balancer is a chip found, not
a predicate.

### 3.8 Boss: Tomahawk Man, "MASTER OF TOMAHAWK"

Arena: v17 or T-BOOTHILL (Should), noon palette `$50`. Vanilla HP 27. Vanilla rhythm kept: a tomahawk every 100-130
f, a feather triple about every 550 f, leaps between.

#### 3.8.1 HIGH NOON (the opening)

Both stand twelve paces apart (Rockman x `$30`, Tomahawk Man x `$D0`). VA-DRAW with the stage's window W:
- win: a **free hit** (3, per `systems.md`) and he staggers 40 f; "YOU WIN THE DRAW. 0.19";
- FOUL or late: he throws first: a fast tomahawk at 3 px/f (contact 4).

#### 3.8.2 Patterns

| Id | Name | Timeline |
|---|---|---|
| A | **TOMAHAWK ARC** (vanilla `$B0`) | Every 110 f, one tomahawk, alternating a high arc (peak y `$40`) and a low arc; a leap toward Rockman between throws (vanilla range x `$38-$BE`) |
| B | **FEATHER FAN** (vanilla `$B1`, GP spread) | 24-f headdress shake, then 3 feathers in Gun.Smoke's three firing directions: along the floor at 2.5 px/f, 45° up-forward, and straight up then falling at Rockman's x |
| C | **DUST DEVIL** (new) | 30-f spin with sand puffs, then a dust devil (16x32) rolls along the floor at 1.5 px/f, bounces off the far wall once, fades at 300 f. A tomahawk that touches it is flung up and rains down at Rockman's x |
| | Cycle | A, A, B, A, C (about 650 f) |

#### 3.8.3 Pinch (HP ≤ 9): SHOWDOWN

- Every 300 f he holsters and stands still for 20 f, then "DRAW!" (VA-DRAW, same W). Win: he staggers 60 f and
  takes the hit. Lose: he throws two fast tomahawks.
- A **returning** tomahawk joins pattern A (the SILVER.T alternate, shown before you own it).
- A leap with a diagonal-down throw from the apex (PLAN's SILVER.T Jet synergy, previewed).

#### 3.8.4 Weapons in this fight

| Weapon | Effect | Tags |
|---|---|---|
| **PLANT.B (weakness)** | **HAY FEVER**: the petals' pollen makes him sneeze ("ACHOO!", 24-f stagger) and he **drops his tomahawk**, which lands 48 px away; he must walk over and pick it up (no throws for up to 120 f) while sneezing. K: "Bless you!" Short i-frames | [new-code][new-art] S Must |
| SILVER.T | Special case in code: **he catches it** (no damage) and throws it straight back as a fast tomahawk | [new-code] S Must |
| W.STORM | Feeds his dust devil: it doubles in size for 120 f | Could |
| Charged Power punch | Knocks his tomahawk out of the air (it clatters to the floor) | Should |

#### 3.8.5 Secret room 1F: THE HIDEOUT

Same AI, pinch at HP 12. On the hideout wall: "WANTED: ROCKMAN. 10,000 BOLTS. SPONSOR: MR. Y." Tomahawk Man, at the
intro: "That poster? Mr. Y put it up. I'm not collecting." (draft). Kill: SILVER.T + BEAT B-PARTS (vanilla script
`$69`) + secret-exit flag.

### 3.9 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| 01-04 | Two more `$6C` gunners (object list) | data |
| 05 | Dispenser drops 3 walkers per wave | AI constant |
| Gallery | Outlaw "!" 24 → 16 f; up to 4 open at once | data |
| Quick-draw | W 20 → 12 f; READY 30-180 f | constants |
| Train | 4 tunnels, warning 90 → 60 f; Sidewinder HP 14; 3 robbers | data |
| Tomahawk Man | Dust devil 2.25 px/f; two dust devils in pinch; SHOWDOWN every 240 f | AI branch |

### 3.10 Commentator hooks and partner

| Event | Hook (draft) |
|---|---|
| Reading the posters | C: "Three bounties. Kalinka, my reading glasses." |
| First civilian hit | K: "Not the PIANIST!" |
| Quick-draw win | K: "Zero point one nine seconds!" (reads the timer) |
| FOUL | C: "He jumped the gun!" |
| Tunnel hit | C: "Mind your head, Rock!" |
| Sidewinder escapes | K: "He got away!" |
| Sheriff opens the gate | C: "Deputy Rock! I always knew." |
| Balancer room found | C: "The old pipe room! Still here after all these years." |
| Sky bypass taken | K: "He's taking the high road!" |
| First PLANT.B hit | K: "Bless you!" |
| Deaths (rotation) | "Too slow on the draw." / "The 4:50 doesn't stop for anyone." / "That was a bad trade, partner." / "The pianist is fine, by the way." / "Boot Hill has room for one more." / "Always check the outhouse first." |

**Break Man**: he can't duel: his whistle intro plays during READY and counts as a FOUL (C: "Not the whistle!").
His shield blocks the gallery outlaws' bullets. No tag-only shortcut. Should.

### 3.11 Homage moments

1. The WANTED board: three bounties, Gun.Smoke style.
2. "PLEASE DO NOT SHOOT THE PIANIST. HE IS DOING HIS BEST." (the saloon sign Oscar Wilde reported from Leadville)
3. "DRAW!" and Wild Gunman's timer: "0.23".
4. The train at sunset: shimmer sky, half-speed mesas, rushing rails, and a tunnel you slide under.
5. Sidewinder galloping along the ridge, leaping onto the caboose for a showdown.
6. The stranger who drops through the saloon skylight from the sky bypass; the piano stops.
7. "WANTED: ROCKMAN. SPONSOR: MR. Y."
8. High noon: the boss fight starts with a draw.
9. Tomahawk Man sneezes and drops his tomahawk.

### 3.12 Weapons as tools in this venue

PLANT.B makes Tomahawk Man sneeze; SILVER.T's arc clears windows above you, and Tomahawk Man catches it; B.ATTACK's
spread and SILVER.T reach Sidewinder on the ridge; Y.SPEAR pierces outlaws behind crates; F.BLAST opens the mine's
TNT crates; C.FLASH stuns every open window at once (and is a FOUL in a duel); KNIGHT.C knocks tumbleweeds back into
outlaws; Power: the Balancer block and the desert pockets; Jet: the sky bypass.

### 3.13 Content note

Vanilla Tomahawk Man draws on Native American imagery. GP's western is a homage to Capcom's and Nintendo's western
games, not to stereotypes: Tomahawk Man is the dignified champion (and the Sheriff's friend), outlaws are cowboy
robots, and no joke targets his headdress or culture (his weakness gag is a sneeze). Re-skinning vanilla's pink
"totem" walkers `$12` as cactus walkers is suggested (Could).

---
## 4. Plant Man: JUNGLE PITFALL

**Pitch.** Plant Man's "Forgotten Area" becomes the jungle of the 2600's most famous explorer. Vines swing over tar
pits, crocodile heads open and close, logs roll, the tar pit breathes, four treasures wait, and a ladder hole leads
to the underground where one screen covers three above. Follow a robot cat through a floor that isn't there and you
reach the Lost Caverns, a balloon ride and Plant Man's Lost City. The gorilla tank stays, now throwing logs.

Vanilla facts used: layout `$32:$B000`; tileset `$2E:$92` (blocks 255/256, metatiles 197, **BG tile ids 256 / 0
free**); base CHR `$90` (256 tiles: canopy, trunks, grass, rock, bamboo floors, the red curtain-wood building),
`$91` dark gorilla rooms / `$92` canopy restore (`$0A00-$0FFF`), `$BB`/`$93` flowers (`$0000-$01FF`); palettes
`$32`, `$33`/`$34` dark, `$35` flowers; music `$04`; collision group 1 (5 → `$11`, D → `$1F`, E → `$10`). Gorilla
tank `$50-$53` (24 + 23 HP), spawner `$56`, script `$1C` (init `$39:$8551`: IRQ chain 7 at line `$C1`, `$069C` =
`$FE`), in v08 and v0E, **both rewriting checkpoint 09**. Breakable pockets on v03 (1-UP + big energy) and v0D (two
big WE). **Lag**: 21 % from the checkpoint (v09-0D) and 10 % at v01 (`engine.md` §8). No alternate exit. Boss `$B2`,
AI `$31:$95EF`; weakness B.ATTACK (4), F.BLAST 2, PLANT.B 0; a Plant Man hit costs 4.

### 4.1 Tileset slot, art and the zero-free-tiles rule

| Item | Content | Tags |
|---|---|---|
| Slot **TS_PLANT** | Copy of `$2E:$92`. Its 255 block ids are full, but the GP layout drops the second gorilla room and half of the lodge, so ids are reclaimed by rebuilding the block table from the GP layout (`levels.py` can list the ids a layout uses) | [engine-ok] S Must |
| Kept | `$90` canopy, trunks, grass, rock, bamboo floors, curtain-wood lodge and crates; `$91`/`$92` dark-room swap; `$BB`/`$93` flower swamp; palettes `$32-$35` | [engine-ok] |
| **P-PITFALL** (new third, ~64 tiles) | Vine knots on the canopy, tar pit surface (with alternate "closed" tiles), croc-pond water, ladder-hole rim, Pitfall's layered trunks, the parrot ledge and the hidden rope ladder | [new-art] M Must |
| **P-UNDER** (new third, ~96) | Underground brick tunnel, brick wall (breakable look), ladders, scorpion nests | [new-art] M Must |
| **P-CAVERN** (new third, ~96) | Cave walls, the underground river, waterfall, the Lost City gate and garden | [new-art] M Must |
| **P-RAIN** (8 tiles x 4 frames) | Rain in the canopy gaps on 0B-0E, animated by CHR swaps (the torch technique) | [new-art] S Could |
| Sprites | Vine segments (11 angle frames x 5 segments, one object), croc head (32x16, 3 frames), log (2 frames), tar bubbles, 4 treasures, scorpion, robot cat, balloon, bat, eel, parrot, Plant Man's bloom form and vine | [new-art] M Must |

**The rule this venue follows**: with 0 free tile ids, **nothing is ever added to the base set**. Every new tile
arrives in a third that replaces art the screen does not show, through the screen exit's CHR byte, exactly as
`$91` replaces the canopy in the dark rooms:

| Screens | BG CHR state | Replaced |
|---|---|---|
| 00-02, 09-0E | `$90` + P-PITFALL | the curtain-wood/crate tiles (only 03-07 need them; the 02 → 03 exit reloads them) |
| 03-07 | `$90` (vanilla) | |
| 08 | `$90` + `$91` | canopy (vanilla) |
| 0F-14 | `$90` + `$92` + `$BB`/`$93` | vanilla |
| 18-1A | `$90` + P-UNDER | canopy (no sky underground) |
| 1B-1E | `$90` + P-CAVERN | canopy and crates |
| 1F | `$90` + P-PITFALL | crates |

The exact tile ranges of the crate and curtain art inside `$90` must be measured before P-PITFALL is drawn
(`text.md` §7's `chrfree3.py` method); see Risks.

### 4.2 Screen-by-screen

| GP | From | The player does | Enemies | Hazards and set pieces | Tags |
|---|---|---|---|---|---|
| **00** | v00 | Starts under the canopy. A sign: "JUNGLE PITFALL. TIME 20:00" (§4.10). The **first rolling log** comes from the right: jump it | `$60` grasshopper (1) | Log spawner | [new-code] S Must |
| **01** | v01 | **The first vine** over a tar pit: jump into it, ride, press A at the far end of the swing | `$61` pod (1, not 2) | Tar pit (collision `$F`, P-PITFALL art; tar bubbles are sprites) | T5 M Must |
| **02** | v02 | **Croc pond**: three heads in the water; stand on closed heads. **Treasure 1: SILVER BAR** on the far bank | log | Croc heads (VA-TIMED) | [new-code] S Must |
| **03** | v03 | The **explorer's lodge** (the vanilla red building). Vanilla pocket kept: 1-UP + big energy behind the breakable (charged Power punch) | `$60` (1) | | [engine-ok] Must |
| **04-05** | v04-v05 | Lodge climb (ladders) | `$59` big robot (v04), `$24`/`$26` lanterns (2) | | [engine-ok] Must |
| **06** | v06 | Across the lodge top, then down | `$54` eye cannon | | [engine-ok] Must |
| **07** | v07 | Down the shaft (loads `$91`: the dark) | `$70` | | [engine-ok] Must |
| **08** | v08 | **CONGA**, the gorilla tank, in the dark, **throwing logs** (§4.6). Lights on when it dies (vanilla). Floor split kept (chain 7) | gorilla parts | **Checkpoint 1** = 09, set when CONGA dies | [new-code] S Must |
| **09** | v09 | Back in the jungle. **The breathing tar pit**: a 64-px floor section opens and closes. **Treasure 2: MONEY BAG** on a ledge above the pit, reached from the vanilla spring `$57` | `$60` (1) | VA-TIMED floor toggle | [new-code] S Must |
| **0A** | v0A | **The ladder hole** (Pitfall's underground entrance) ↓ 18. **Treasure 3: GOLD BAR** on a canopy ledge, reached by a vine. Main route: right | `$61` (1), log | Vine; ladder hole (down exit, target `$17` → 18) | T5 Must |
| **0B** | v0B | **Vine chain**: two vines in a row over the vanilla spike beds. **The storm starts**: lightning (§4.8). Hidden-room tell: the parrot ledge at the top right | parrot (harmless) | Lightning reveals the rope ladder; up exit (target `$1E` → 1F) | T5 Must |
| **0C** | v0C | **Croc river**: five heads with staggered phases, a rolling wave to time | `$61` (1) | VA-TIMED | Must |
| **0D** | v0D | Storm; vanilla pocket kept: two big WE behind the breakable | `$60` (2, not 4) | | [engine-ok] Must |
| **0E** | v0E (was gorilla 2) | **The big swing**: one long vine (length 88 px) over a croc pond with two logs rolling on the far bank | 2 logs | No gorilla, no split: the lag fix | T5 Must |
| **0F** | v0F | The storm ends; spring `$57`, eye cannon. **Underground exit 1** (from 19) arrives by ladder here | `$54` | | [engine-ok] Must |
| **10-14** | v10-v14 | **The flower swamp** (vanilla `$BB`/`$93`, palette `$35`): pillars with spring flowers over the swamp; croc heads in two swamp channels (11, 13). **Underground exit 2** (from 1A) arrives by ladder in 13 | `$58` eye drones, `$5A` hornets, `$5F` spring flowers, `$54` (vanilla; max 5 live) | | [engine-ok] + S Must |
| **15-16** | v15-v16 | Shutters; **checkpoint 2** at 16 | | | [engine-ok] Must |
| **17** | v17 | **Plant Man** (§4.7) in the green bamboo room, now with two ceiling hooks and an opening floor | | | Must |
| **18** | new | **Underground, west** (under 0A-0C): from the ladder hole; brick tunnel | 2 scorpions | | [new-art] Must |
| **19** | new | **Underground hub** (under 0D-0F): the **robot cat** (§4.5); **Treasure 4: DIAMOND RING** in a nook behind a scorpion (§4.4); a **brick wall** at the right end (charged Power punch, or Break Man's charge shot) → 1A; a ladder up → 0F (up exit, target `$10` → 0F) | 2 scorpions | False floor (cat) | [engine-ok] + S Must |
| **1A** | new | **Underground, east** (under 10-12): ladder up → 13 (target `$14` → 13) | 1 scorpion | The full 3-for-9 shortcut | Must |
| **1B** | new | **The Lost Caverns**: fall in through the cat's false floor; a shaft of ledges | 3 bats | | [new-art] Must |
| **1C** | new | **The underground river**: the **balloon** rises from the bank to the top ledge (§4.5) | eels, bats | River is a pit | [new-code] S Must |
| **1D** | new | The Lost City gate: shutters, **checkpoint 2b** | | | Must |
| **1E** | new | **Secret boss room: THE LOST CITY** (§4.7.5). Kill: PLANT.B + secret-exit flag | | | Must |
| **1F** | new | **Hidden room "TREETOP HUT"** (§4.8) | | | Must |

All 32 screens are used. The main route keeps vanilla's 24. Checkpoints: 09 (after CONGA), 16 (shutter), 1D (secret
shutter).

Lag targets: at most 8 live objects on any Plant screen. Vanilla's worst stretch (v09-0D) loses half its
grasshoppers and all its falling debris `$5B`; the second gorilla room is gone.

### 4.3 Jungle mechanics (numbers)

| Object | Behaviour | Numbers | Tags |
|---|---|---|---|
| `OBJ_VINE` (T5) | Swings constantly (Pitfall vines never stop). Grab: airborne, upper body touching the bottom 16 px. Hang pose = the ladder-climb sprite. **A** releases with the tip's velocity (capped at 3 px/f horizontal) plus a normal jump. **DOWN** drops. **B** fires toward the swing's direction. Power form can grab; Jet does not (it flies) | Pivot at the canopy (y `$20-$30`), length 64-88 px, period 128 f, amplitude ±50°. One object, 5 sprite segments; 11 angle frames | [new-code][new-art] M Must |
| `OBJ_CROC` (VA-TIMED a) | Head in the water. CLOSED = a rideable platform (vanilla lift `$A0` code) | CLOSED 120 f → BLINK 20 f (red eyes: the tell) → OPEN 90 f (jaws hurt 4, not rideable) → CLOSE 10 f. Phase offsets per head from data (0C: 0/48/96/144/192 f) | [new-code][new-art] S Must |
| `OBJ_LOG` + `OBJ_LOGGEN` | Rolls along the floor, drops off ledges. Contact 2 + 16-px knockback (Pitfall's logs never kill outright). Buster shots thunk off. **F.BLAST burns it** (a per-class thematic one-shot, vanilla style); a charged Power punch sends it rolling back | 1.25 px/f; one log per 200 f per generator; at most 2 live | [new-code][new-art] S Must |
| `OBJ_TARPIT` (VA-TIMED b) | A 64-px floor section toggles between solid floor and tar by flipping its 4 unique metatile ids in `$0340` and repainting | SOLID 150 f → BUBBLE 30 f (tar bubbles rise: the tell) → TAR 120 f (collision `$F`) → SOLID | [new-code] S Must |
| `OBJ_SCORPION` | Walks the tunnel floor; raises its tail for 30 f (tell) when Rockman is within 24 px, then strikes (3) | HP 2, 0.5 px/f | [new-art][new-code] S Must |
| `OBJ_BALLOON` | Grab from below or the side: Rockman hangs and rises 0.5 px/f; LEFT/RIGHT drift 0.5 px/f; A lets go. A bat touching the balloon pops it and drops him onto the bank ledge below (never into the river, except on HARD) | rise to y `$30`, then step right onto the top ledge | [new-code][new-art] S Must |
| `OBJ_EEL` | Leaps out of the river in an arc (2) | every 120 f | [new-art] S Should |
| `OBJ_BAT` | Swoops when Rockman passes below | HP 1 | [new-art] S Must |

Weapons on these objects (VARIETY): **B.ATTACK freezes a croc head CLOSED for 300 f**; C.FLASH stuns every croc and
scorpion on screen for 120 f; F.BLAST burns logs and Plant Man's vine; W.STORM gives the balloon +1 px/f for 60 f;
PLANT.B's barrier blocks eel leaps; Jet hovers over tar pits (late-game players may skip vines: allowed).

### 4.4 Behaviour item: the PITFALL PERFECT (AUTO RECOVER chip)

*Pitfall!*'s perfect score needs every treasure and no lost points; logs only ever cost points.

- **Treasures**: SILVER BAR (02), MONEY BAG (09), GOLD BAR (0A), DIAMOND RING (19, underground). Each pops
  "TREASURE n/4" and pays bolts (`systems.md`).
- **The log counter**: every log hit in the stage (including CONGA's logs) is counted and shown next to the
  treasure pop ("TREASURE 3/4 · LOGS 0").
- **The ring**: if the log counter is 0 when Rockman reaches the nook in 19, it is the **DIAMOND RING**; otherwise
  it is a "RHINESTONE RING" worth 10 bolts. With 4/4 and a real diamond, the ring also grants the chip.
- Chip: PLAN's **AUTO RECOVER** ("found in the Plant underground", kept), effect per `systems.md`.
- All four treasures are reachable without an adaptor in one run (three before the ladder hole, one in 19).
- Tells: the counter shown on every treasure; the rhinestone itself; C: "Harry never let a log touch him."
- Hint: "FOUR TREASURES, ZERO LOGS. THE DIAMOND IS SHY."

### 4.5 Secret exit: follow the cat to the Lost Caverns

*Pitfall II*'s Quickclaw is the cat Harry must find. Here a small green robot cat (K: "Is that... Tango? From the
Game Boy?") lives in the underground hub.

- **Requirement**: in 19, walk toward the cat. It meows, runs 48 px to a dead-end nook and **drops through the
  floor**: one floor metatile there has floor art and collision 0 (CX's "clouds are not floors", as a floor)
  [engine-ok]. Follow it: fall into 1B. No adaptor.
- If you do not follow within 300 f, the cat climbs back out and sits by the nook again (it repeats).
- **Route**: 19 → false floor ↓ 1B (bats, ledges) ↓ 1C (river; ride the balloon up past the bats) → 1D gate
  (shutters, checkpoint 2b) → **1E THE LOST CITY**. The kill sets the flag.
- **Tells**: the cat is the only friendly animal underground; it meows when you enter 19; the nook is a dead end
  with nothing in it, which is suspicious on its own.
- **Debrief hint**: "THE CAT KNEW A WAY DOWN. NEXT TIME, FOLLOW IT."

### 4.6 Mid-boss: CONGA, the gorilla tank

Vanilla object set kept (`$50-$53`, 24 + 23 HP, spawner `$56`, script `$1C`, chain 7 floor split, dark → lights
on). One change: it throws **rolling logs** instead of rocks `$14` (the logs bounce off the far wall once and roll
back: a Donkey Kong barrel nod). At most 2 logs. Lag: 4 parts + 2 logs + 3 shots = 9.

Checkpoint fix: vanilla's script re-writes checkpoint 09 in both gorilla rooms; GP has one gorilla room, and its
routine sets checkpoint 09 only when CONGA dies (one byte, `stages_b.md` §8). [engine-ok] S Must.

### 4.7 Boss: Plant Man, "FLOWER FANCIER"

Arena: v17 (green bamboo room) plus two ceiling hooks (x `$50` and `$B0`, y `$20`; BG) and a 64-px centre floor
section that can turn to tar (`OBJ_TARPIT`). Vanilla HP 27. Vanilla rhythm kept: the barrier about every 260-350 f,
leaps of about 130 f.

#### 4.7.1 Patterns

| Id | Name | Timeline |
|---|---|---|
| A | **PETAL GUARD + LEAP** (vanilla) | Raise the barrier (4 petals + centre, radius 20 px) in 40 f; leap toward Rockman (peak y `$44`, about 120 f); 20 f after landing, throw the 4 petals outward in an X at 2 px/f; 30-f recovery |
| B | **VINE SWING** (new) | 20 f: throws a vine to the nearer ceiling hook; one swing pass across the room (64 f, contact 4) with a jungle yell; lets go at the far apex and lands. **The vine stays for 150 f** and Rockman can grab it (T5 rules): the stage's mechanic, used against him |
| C | **SPROUT** (new) | 24-f stomp (the floor shakes: the tell); the centre floor turns to **tar** for 150 f; three sprout platforms (32 px wide) rise at x `$28`, `$80` (straight out of the tar: the way across) and `$D0`, to 32, 56 and 40 px, and last 180 f; at +40 f he lobs 2 seeds at the sprout tops |
| | Cycle | A, B, A, C (about 700 f) |

#### 4.7.2 Pinch (HP ≤ 9): BLOOM

- 30-f bloom animation (invincible): his head petals open into a large flower (new sprite frames).
- The barrier orbits wider (radius 32) and 1.5x faster: PLANT.B's Jet synergy "Petal Storm" (PLAN), previewed.
- 3 pollen spores drift toward Rockman at 0.5 px/f for 300 f (contact 2, shootable).
- VINE SWING makes two passes.

#### 4.7.3 Weapons in this fight

| Weapon | Effect | Tags |
|---|---|---|
| **B.ATTACK (weakness)** | **FROSTBITE**: his petals freeze white, drop and shatter; he cannot raise the barrier for 300 f and shivers for 30 f. K: "He's wilting!" Short i-frames | [new-code][new-art] S Must |
| PLANT.B | Special case in code: barrier meets barrier, **both pop** in a burst of petals (no damage). Replaces vanilla's silent 0 | [new-code] S Must |
| F.BLAST (2, vanilla) | During B it **burns his vine**: he drops mid-swing and lies stunned 40 f | [new-code] S Should |
| C.FLASH | Freezes the tar back to floor for its duration | Could |

What the fight teaches: PLANT.B's tap (his barrier), its Up+B petal launch (his throw), its Jet synergy (the bloom
orbit) and the venue's own vine.

#### 4.7.4 Defeat

Vanilla award, re-pointed by win count (BRIEF §4): "YOU GET PLANT.B" (the vanilla script `$62` says "AND RUSH JET
ADAPTOR"; that line is only shown when this is the 4th win, per `systems.md`).

#### 4.7.5 Secret room 1E: THE LOST CITY

Same AI, pinch at HP 12, in a night palette (the revisit-palette precedent) among the Lost City's ruins, with one
giant orchid behind him. Must: the room and the fight. Should: the night arena art.

### 4.8 Hidden room and the storm

**The storm** [engine-ok] S Must: from 0B to 0E an effect thread (vanilla palette cyclers, `$3B:$9143` data) plays
lightning: every 6-10 s the BG palette jumps to a bright set for 4 f, off 2 f, on 3 f. With **reduced flashes** on,
it is one soft 20-f brighten instead. Thunder SFX on every strike. Rain tiles are Could (P-RAIN).

**Hidden room 1F "TREETOP HUT"** S Must.
- Entry: on 0B a rope ladder hangs from a ledge at the top right, drawn in the canopy's darkest palette so it is
  invisible **except during lightning**, when that palette entry is lit. A parrot on the ledge squawks every 4 s.
  Reach the ledge by releasing the second vine at the far end of its swing; climb the ladder (up exit, target `$1E`
  → 1F).
- Content: a 1-UP, an E-tank, and a "game cartridge" prop worth bolts (`systems.md`).
- Exit: ladder down to 0B.
- Hint: "WHEN THE LIGHTNING STRUCK, A LADDER APPEARED IN THE TREES."

Predicate order: hidden room → PITFALL PERFECT → secret exit.

### 4.9 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| Crocs | CLOSED 120 → 90 f, OPEN 90 → 110 f | constants |
| Vines | Period 128 → 104 f | constant |
| Tar pit | SOLID 150 → 110 f | constant |
| Logs | 1.25 → 1.75 px/f; CONGA throws 3 | constants + AI branch |
| 10-14 | Two spring flowers `$5F` replaced by croc heads | object list |
| 1C | A popped balloon drops into the river; 4 bats | AI branch + data |
| Plant Man | Sprouts last 120 f; pinch at HP 13; seeds aimed at Rockman | AI branch |

### 4.10 Commentator hooks and partner

| Event | Hook (draft) |
|---|---|
| Stage start | K: "Twenty minutes on the clock!" C: "...It does nothing. That was the old rules." |
| First vine | C: "Hold on tight, Rock!" |
| Croc death (a pair) | C: "See you later, alligator!" K: "In a while, crocodile." |
| First log hit | K: "TIMBER!" |
| Treasure | K: "Treasure! That's two of four!" |
| Rhinestone | C: "That's paste, Rock. Harry never let a log touch him." |
| First lightning | K: "Eek!" |
| The cat | K: "Is that... Tango? From the Game Boy?" |
| Brick wall broken | C: "Nine screens in three! The underground is faster!" |
| First B.ATTACK hit | K: "He's wilting!" |
| Bloom | C: "Full bloom! Careful, Rock!" |
| Deaths (rotation) | "See you later, alligator!" / "Stuck in the tar!" / "He let go too early." / "The jungle always wins the first round." / "Watch the eyes on those crocs!" / "That wasn't a floor, Rock." |

The 20:00 sign (Could): a clock in the corner counts down from 20:00 like the 2600 game's; at 0:00 nothing happens
but the commentator line.

**Break Man**: his charge shot breaks the underground brick wall (19 → 1A), an optional tag shortcut that gives the
3-for-9 underground to players without Power yet. Should.

### 4.11 Homage moments

1. Screens 00-02: a rolling log, a vine over a tar pit, crocodile heads: the 2600 jungle in Rockman's engine.
2. Crocodile heads you stand on, with "See you later, alligator!" / "In a while, crocodile."
3. The tar pit that breathes.
4. The underground where three screens cover nine.
5. Following a robot cat through a floor that isn't there.
6. A balloon ride up an underground river while bats try to pop it.
7. Lightning reveals a rope ladder in the trees.
8. The gorilla tank throwing logs that bounce back like barrels.
9. Plant Man swinging across his arena on a vine, then blooming.
10. "That's paste, Rock": the rhinestone ring for anyone a log touched.

---
## 5. The four venues side by side

| | SKY ACE 1943 | DRAGON QUESTLIKE | GUN.SMOKE FRONTIER | JUNGLE PITFALL |
|---|---|---|---|---|
| Homage made a mechanic | 1943 rules: draining energy, shoot-to-cycle POW, 3 loops, red squadrons, SHOOTING DOWN % | Command windows, keys that doors eat, search, inn, Metal Metslime, battle log | Bounty posters, Hogan's Alley gallery, quick-draw with a timer, train with tunnels | Vines, croc heads, logs, breathing tar pit, 3:1 underground, treasures, balloon |
| Vanilla set piece + one twist | Wind Man's pull → gust zones; Tomahawk's parallax chain → sortie bands | Spike ceiling (IRQ `$11`) → **a monster with HP**; Power pillar → stairs behind the throne | Dome dispenser → bounty 1; parallax + shimmer chains → the train's bands; plate ladder → Sheriff's back way | Gorilla tank → **throws logs**; dark-room swap → underground thirds |
| Vanilla secrets | Pocket on 04 kept | **A plate** kept (1A); 1-UP pocket kept | **B plate** (1F), **Energy Balancer** (1C), **Jet sky bypass** (18-1A) kept | Pockets on 03 and 0D kept |
| Secret exit | 4 red squadrons → elevator → hangar → WING WALKER (1D) | Search behind the empty throne → dark basement → KNIGHTLORD (1A) | 3 bounties → Sheriff → back way → HIDEOUT (1F) | Follow the cat → Lost Caverns → balloon → LOST CITY (1E) |
| Hidden room | 1E WEATHER BALLOON (seagull on a solid cloud) | 1E LIGHT'S TABLET (glint, search) | 1B THE OUTHOUSE (shoot the rattling door) | 1F TREETOP HUT (lightning shows the ladder) |
| Behaviour item | YASHICHI (juggle a POW 8 times) | KAISHIN (kill the Metal Metslime) | SHERIFF STAR (hurt no townsfolk) | AUTO RECOVER (4 treasures, 0 logs) |
| Boss weakness reaction | C.FLASH: engines STALL | Y.SPEAR: pierces the shield, "AN EXCELLENT MOVE!" | PLANT.B: sneezes, drops his tomahawk | B.ATTACK: FROSTBITE, petals shatter |
| Own-weapon special case | W.STORM absorbed (he likes it) | KNIGHT.C clashes | SILVER.T caught and thrown back | PLANT.B: both barriers pop |
| Pinch | SKY ACE: loop dive, calls a red squadron | ENRAGED: Morning Star, HEALMORE | SHOWDOWN: mid-fight draws | BLOOM: wide orbit, pollen |
| Screens used | 29 / 32 | 28 / 32 | 32 / 32 | 32 / 32 |
| Exhibition | E1 (with Knight) | E1 (with Wind) | E2 (with Plant) | E2 (with Tomahawk) |

## 6. Build list by tier

Sizes are per item; "shared" items are built once by `tech.md` and counted there.

| Venue | Must | Should | Could |
|---|---|---|---|
| **Wind** | TS_WIND (S); W-CARRIER (M), W-SEA (S), sprites (M); catapult (S); **SKY ACE mode** (M) + wave director data (M) + POW cycle (S) + LOOP (S) + drain (S) + tally (S); AYACO as a sprite build (M); lamp board + elevator (S); gusts (S); hidden room (S); YASHICHI (S); Wind Man rework (M); room 1D fight (S) | Re-sortie catapult (S); W-HANGAR + bomb carts (M); WING WALKER moving arena (M); Kite Mets (S); AYACO as BG art (L); arena cloud band (S); sortie theme [new-music] (M); Break Man hooks (S) | Paper-plane defeat (S) |
| **Knight** | TS_KNIGHT (S); K-DQ (S); sprites (M); VA-SEARCH (S); VA-ENCOUNTER (M) + Metslime (S) + Killer Chest (S); keys, doors, chests (T3 data, S); ceiling with HP (S); dark basement + RADIANT (S); Metal Metslime + KAISHIN (S); Knight Man rework with battle log (M); Knightlord offer (S) | Princess Roll + Roll's Love (S); Inn (S); KNIGHT.C clash, C.FLASH interrupt (S); battle theme [new-music] (M); Break Man hooks (S) | EXP and level-ups (S); TRUE FORM (S); inn jingle and level-up fanfare [new-music] (S) |
| **Tomahawk** | TS_TOMAHAWK (S); T-TOWN, T-SALOON, T-TRAIN (M each); sprites (M); WANTED board (S); gallery (M); VA-DRAW (S); train ride (L); Sidewinder (S); Sheriff gate (S); outhouse room (S); SHERIFF STAR (S); Tomahawk Man rework (M); hideout gag (S); DRAW bell SFX (S) | T-BOOTHILL (S); TNT crates (S); punch knocks tomahawks down (S); duel stinger and train theme [new-music] (M); Break Man hooks (S) | Vulture and cactus re-skins (S); W.STORM dust devil (S); honky-tonk piano arrangement [new-music] (S) |
| **Plant** | TS_PLANT (S); P-PITFALL, P-UNDER, P-CAVERN (M each); sprites (M); vines T5 (M); croc heads (S); logs (S); tar pit (S); scorpions, bats (S); balloon (S); treasures + log counter (S); cat + false floor (S); CONGA's logs + checkpoint fix (S); lightning (S); hidden room (S); Plant Man rework (M) | Eels (S); vine burn (S); Lost City night arena (S); Break Man wall shortcut (S) | Rain (S); 20:00 clock (S); C.FLASH freezes tar (S); "Lost Caverns" theme [new-music] (S) |

Each venue is **L** overall. If the schedule needs a cut, cut in this order: Could items; the Should moving arenas
(WING WALKER, Lost City night); AYACO's BG version; the Inn and Princess; never the core homage mechanic of a venue,
its secret exit, hidden room or behaviour item.

## 7. Dependencies on other docs

| Doc | What this design needs from it |
|---|---|
| `systems.md` | Damage and i-frame rows for the 4 bosses (weakness short i-frames; the special cases listed in §1.7.3, §2.8.3, §3.8.4, §4.7.3); weapon behaviours this doc previews: W.STORM tap tornado and Up+B updraft, C.FLASH Up+B time-stop, KNIGHT.C returning flail and orbit, SILVER.T arc, boomerang and Jet dive throw, PLANT.B barrier, petal launch and Jet "Petal Storm"; whether forms fire weapons in the sortie; the **rental Jet** (forced form without owning Jet); chips YASHICHI, KAISHIN (Critical), SHERIFF STAR (Judge's Favor variant), AUTO RECOVER, Energy Balancer; SECRETS and STYLE rows (100 % tally, draws won, Pitfall perfect); bolt payouts (bounties, treasures, Inn price); the moral trade-off recipe (Eddie in the gallery is offered); the YOU GET text by win count |
| `story.md` | Every line here (EN drafts) in JP and EN: King, Sage, Innkeeper, Princess Roll, the Knightlord, Sam, the Sheriff, the conductor, posters, battle-log lines, commentator hooks and death tables, debrief hints; Roll's cameo as the princess; Tango's cameo; the "WANTED: ROCKMAN" gag |
| `meta.md` | Four secret-exit flags (Wind, Knight, Tomahawk, Plant) in save RAM; E1 = Wind + Knight, E2 = Tomahawk + Plant; Records: best quick-draw time, best SHOOTING DOWN %; debrief predicate order per venue (§1.6, §2.7, §3.7, §4.8) |
| `tech.md` | T1-lite fixed-camera rides and the wave director; T4 raster bands (≥ 4 bands + the window band) on the generic list, with chains C, E/F and 7 as presets; T2 text window with YES/NO and 4-item menus; T3 doors, keys, gates, lifts through exits; T5 pendulum; VA-GUST, VA-TIMED, VA-SEARCH, VA-DRAW, VA-ENCOUNTER; the generic object id + sub-id dispatcher (about 45 new object kinds here alone); four tileset slots and their banks; the stage-attribute fields of §0.1 (secret-boss screen, plate slot, flag index, HARD list); the Knight ceiling's `$069C` logic moved out of IRQ `$11` or given a retract flag |
| `venues_b.md` | Shared tech with the other four venues (T1 for Blizzard's ski, T3 for Flame's plates and Centaur's doors, the falling ceiling for Yamato); avoid a second train, a second shmup or a second quick-draw; the E1-E4 pairing |
| Exhibitions (E1, E2) | Unlock conditions from these four secret exits |

## 8. Lessons applied

- **CX 1, one premise everywhere**: bounties are prize money, the sortie is judged in percent, Knight's King records
  your deeds, every death gets a commentator line.
- **CX 2, a homage is a mechanic**: 1943's rules, DQ's command windows and hidden stairs, Wild Gunman's timer,
  Pitfall's 3:1 underground and treasure rules, each the core of its venue, not a re-skin.
- **CX 3, voice on failure**: per-venue death rotations, the DQ King's death line, the Knightlord's YES.
- **CX 4, the partner as a second body**: one optional Break Man interaction per venue, with one tag-only shortcut
  (Plant's wall).
- **CX 5, reuse set pieces with one twist each**: the spike ceiling gets HP; the gorilla throws logs; Wind Man's pull
  becomes the gusts; the dome dispenser becomes bounty 1; Tomahawk's parallax and shimmer chains carry the train;
  vanilla's plate routes become the secret routes.
- **CX 6, telegraph tools**: lamp boards, windsocks, the battle log, the croc's red eyes, tar bubbles, the "TUNNEL!"
  sign and whistle, the DRAW bell, the Sheriff's count.
- **CX 7, special cases in visible code**: W.STORM absorbed, SILVER.T caught, PLANT.B barrier pop, Y.SPEAR pierce, the
  Metal Metslime's 1 damage.
- **CX 9 / 4MI 10, testability**: fixed encounter triggers and data-driven waves keep every set piece deterministic
  for golden-movie tests.
- **4MI 1, the weakness in the i-frames**: every weakness reaction is a stagger window, not just damage.
- **4MI 5, behaviour gates with after-the-fact hints**: four behaviour items and twelve real debrief hints.
- **4MI 6, old weapons, new jobs**: C.FLASH stalls engines and stuns crocs, B.ATTACK freezes croc heads, F.BLAST
  burns logs and vines and lights the basement.
- **4MI 7, the theme as mechanics**; **4MI 8, HARD as poke lists** (one table per venue); **4MI 11, the raster
  list**; 4MI's Cossack 1 fixed-screen shoot-'em-up is the precedent for T1-lite.
- **RM6 1-8**: vanilla ids kept; one tileset slot per venue with art entering by CHR thirds (RM6 lesson 2, Plant's 0
  free tiles); the ~10-object budget stated per set piece; breakables per metatile id reused for the stairs and
  the tar pits (unique ids per pit); adaptors by win count with no adaptor on a normal exit; vanilla quirks kept on
  purpose (the Jet sky bypass, the Balancer room, the A and B plate rooms, the revisit palettes).

## 9. Risks

1. **Screen budget.** Tomahawk and Plant use 32 of 32 screens. Any new idea there costs an existing screen. Fallbacks:
   Plant merges 1B and 1C into one cavern screen; Tomahawk shortens the sky bypass to 2 screens.
2. **Plant's tiles.** P-PITFALL assumes the lodge's curtain/crate tiles in `$90` form a replaceable block. If they are
   interleaved with jungle tiles, 00-02 lose the Pitfall art: the tar pit falls back to black tiles plus bubble
   sprites and the croc water to sprites. Measure before drawing.
3. **Raster bands.** The sortie and the train need 3-4 bands plus the commentator window band on the same frame.
   This needs the generic raster list (BRIEF §7.1) and MMC5's scanline IRQ. Fallback: 2 bands (sky fixed, ground
   moving).
4. **Lag and flicker.** Formations of 5 at one height put 10 sprites on a scanline. Wave paths keep at most 4 planes
   within any 16-px row; red squadrons fly staggered.
5. **Knight depends on T2.** Encounters, the battle log, NPCs and the offer are all text. If the text engine slips,
   Knight loses most of its homage. Fallback: 4MI-style sprite words (as Pharaoh's curses) for the log and a
   two-choice sprite prompt.
6. **IRQ logic.** Knight's ceiling runs inside IRQ `$11`. Changing it inside an interrupt is fragile; moving the
   logic to a per-frame object is safer and should happen during the port anyway.
7. **Reaction-time content.** The quick-draw is a reflex test. CASUAL doubles the window to 40 f; the bell gives an
   audio cue; losing never blocks progress (only the bounty). Time Attack needs the RNG delay to be fair: draw it
   from the frame counter at the screen lock, so it is replayable.
8. **The sortie's forced Jet** contradicts "Jet after the 4th win" unless the rental is framed and scoped (only in
   01 and 1D). Needs `systems.md` and `story.md` sign-off.
9. **Trademarks.** The venue titles carry other publishers' marks (Dragon Quest, Pitfall, Gun.Smoke, 1943).
   On-screen, prefer descriptive forms and parody names (Metslime, AYACO, Six-Shot Sam, Tante-GP); never logos;
   dialogue paraphrases rather than quotes. `meta.md` should rule on the final on-screen titles.
10. **Cultural sensitivity** in the Tomahawk venue (§3.13).
11. **Text fatigue in Knight.** START skips any window; Time Attack auto-skips NPC text; the battle log stays (it is
    the boss's tell) but is one line and never blocks input.
12. **Skill-gated secrets.** Wind's 4 full squadrons and Tomahawk's Sidewinder are skill gates. CASUAL: a squadron
    counts at 4 of 5 planes; Sidewinder has HP 7.
13. **Object id pressure.** About 45 new object kinds in these four venues alone, against about 30 free vanilla type
    ids. The generic id + sub-id dispatcher is a hard prerequisite.
14. **Bass Mode (Could)**: the sky bypass ladder (128 px up), the Power walls and the sortie all need Bass answers
    (double jump + dash, Bass Buster breaking `$B` blocks per PLAN, and Treble as Bass's "rental").

## 10. Open questions

1. Does `tech.md` accept T1-lite (fixed camera, scrolling bands) for the sortie and the train, so that true autoscroll
   is only needed where terrain must move (Blizzard's ski, if anywhere)?
2. Is the rental Jet acceptable, or should the sortie be on a Committee glider that is not Rush at all?
3. Does `systems.md` keep the vanilla weakness chain (Wind ← C.FLASH, Knight ← Y.SPEAR, Tomahawk ← PLANT.B, Plant ←
   B.ATTACK)? All four reactions here assume it.
4. Chip effects and slot costs for YASHICHI, KAISHIN, SHERIFF STAR and AUTO RECOVER; is SHERIFF STAR a found Judge's
   Favor or a separate chip?
5. SECRETS row split: hidden room 5 + secret exit 10 + behaviour item 5 is proposed for every venue (the plate rides
   on the secret exit in Knight and Tomahawk). Does `systems.md` agree?
6. Do keys (Knight) need a general counter in T3, or a venue-local byte?
7. Will `story.md` let Roll play the princess and Tango cameo as the cat?
8. Where does Knight Man's battle log go: the bottom window (shared with the commentators, who stay muted) or a top
   line that must dodge the life bars?
9. Music budget: this doc asks for at most one new track per venue at Should (sortie, DQ battle, train or duel,
   Lost Caverns). Is that within the sound plan?
10. If `tech.md` enables MMC5 extended attributes or CHR banking that frees BG tile ids, Plant's art plan can drop
    its third-swapping; until then, this doc assumes 256 live BG tiles.
11. Does collision group 1 (Plant) remap `$F`? The tar pits and croc water assume it stays deadly.
12. Should the secret boss rooms' distinct arenas (WING WALKER, LOST CITY at night, T-BOOTHILL) be promoted to Must so
    that secret exits feel like different matches?
