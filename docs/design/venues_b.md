# Heritage Venues B: Blizzard, Flame, Centaur, Yamato (design-venues-b)

Status: **v1, complete for all four venues.** Owner: design-venues-b. Scratch: `build/design/design-venues-b/`.

This doc designs four of the eight Heritage Venues of Rockman 6 GP:

| Venue | Stage id | Homage | Vanilla set piece kept (with one twist) |
|---|---|---|---|
| **Blizzard Man: SUMMIT CLIMBER** | 0 | *Ice Climber* (1985) | the rocking icebreaker (now it shakes icicles loose) and slippery ice |
| **Flame Man: PRINCE OF PERSIA PALACE** | 3 | *Prince of Persia* (1989, FC 1992) | igniting oil (now a choice you make, and it stays made) |
| **Centaur Man: ATLANTIS RUINS** | 7 | *Atlantis no Nazo* (1986), *Kid Icarus* (1986) | the tide (now a tool: high tide lifts you, low tide opens a door) |
| **Yamato Man: EDO NINJA ROW** | 4 | *Ninja Jajamaru-kun* (1985), *Ganbare Goemon!* (1986), *DuckTales* (1989) | the dark mid-boss room, the E-plate Jet ledge, the charged-punch bypass; Knight's falling ceiling, re-homed |

It follows `docs/design/BRIEF.md` (binding), starts from `docs/PLAN.md` §3.2 and corrects it against the research
(`docs/research/rm6/`, `cx/`, `r4mi/`). Weapon specs, chips, dialogue, the scorecard and the engine belong to
`systems.md`, `meta.md`, `story.md` and `tech.md`: where this doc needs something from them, it is a **proposal**
and is listed in §5.3 (dependencies).

Every vanilla map was read from `docs/research/rm6/img/maps/` (`00_blizzard`, `03_flame`, `04_yamato`, `07_centaur`).
Vanilla screen numbers are written **v0E**; GP screen numbers are plain **0E**.

---

## 0. Rules shared by the four venues

### 0.1 Tags

Each item carries the BRIEF §8 marks: **[engine-ok]** (vanilla does it, data only), **[new-code]**, **[new-art]**,
**[new-music]**, a size **S/M/L** and a tier **Must/Should/Could**. A line like `[new-code M · Should]` means new code,
medium size, Should tier.

### 0.2 Ids, screens and budgets

- **Stage ids stay vanilla** (Blizzard 0, Flame 3, Yamato 4, Centaur 7). The ship's and the tide's collision offsets
  (`$3E:$DA1C-$DA6A`) are hard-wired to stage ids 0 and 7, so keeping the ids keeps both set pieces working before the
  stage-attribute table (BRIEF §7.2) lands. Yamato borrows Knight's ceiling (stage-6 only) and therefore **needs**
  that table (§4.5.1).
- **One 32-screen layout per venue** (8 rows x 256 blocks; screens `$00-$1F`). Convention: the main route counts up
  from 00; branches, secret arenas and the hidden room live in the high screens, entered by exits with explicit
  targets (vanilla practice, `levels.md` §9). Every venue below fits in 32 screens with 2-4 spare for HARD-only rooms.
  If `tech.md` adopts WRAM-resident sections (BRIEF §7.2), nothing here breaks; the spare screens just get bigger.
- **One new tileset slot per venue** (BRIEF §4). I ask for **a whole 8 KB tileset bank per venue** (its own 9-page
  set plus its *own* alternate set at `$9B-$9F`), because two of these venues swap layouts through the alternate set
  (Blizzard's ice cells, Yamato's kabuki stage) and a shared alternate set would couple them to bank-mates
  (`stages_a.md` lessons).
- **Lag**: about 10 live objects fill a frame (`engine.md` §8). The screen tables give each screen's peak count in
  brackets, the player included and shots excluded; the target is **8 or fewer**, so the player's shots still fit.
- **Checkpoints**: two mid-stage checkpoints plus the boss shutter (vanilla has one plus the shutter). CASUAL adds the
  ones marked *(CASUAL)*. A checkpoint is the `LDA #s / JMP $8416` routine; every checkpoint screen gets a palette
  program that sets everything it needs (`levels.md` §19: palettes are cumulative deltas).

### 0.3 The gate matrix

Each venue has one secret exit, one one-screen hidden room and one behaviour-gated chip (BRIEF §5.4). They use
**four different kinds of gate**, so the four venues don't feel alike, and **none of the four secret exits needs an
adaptor**. Only the plates (Jet, as in vanilla) and Yamato's lower bypass (Power, as in vanilla) are adaptor-gated.

| Venue | Secret exit (gate kind) | Hidden room (tell) | Behaviour-gated chip | Plate | Adaptor routes |
|---|---|---|---|---|---|
| Blizzard | **Catch the condor** in the summit bonus before the timer ends (timing) | A floor of one climb screen does not wrap: the seals walk off it and don't come back | **SNOW CHAINS**: never destroy a Toppy seal-bot | none | F.BLAST ice pockets (revisit) |
| Flame | **Don't fight your shadow**: walk into it without shooting (behaviour) | A sealed gate with a mousehole: wait, and the mouse steps on the plate | **FIREPROOF**: reach the boss with no oil ignited | none | Power-block 1-up (revisit) |
| Centaur | **ZONE 100**: a sunken door that opens only at low tide (observation + timing) | **ZONE 0**: in the black zone, one door glows only in the dark | **CENTURION**: free the three petrified Centurion-bots with a charged shot | **T** across the Pegasus gap (Jet) | Jet sky route |
| Yamato | **The sekisho back road**: carry 3 travel passes to the checkpoint gate (collection) | Pogo on the gold crest in the caltrop hall: a trapdoor opens (DuckTales) | **DARUMA**: win the daruma otoshi without touching its head | **E** on the castle roof (Jet) | charged-punch bypass + dark mid-boss room (Power) |

**Route choices.** In Centaur and Yamato the plate route and the secret exit branch off at different points, so one
visit takes one or the other (Yamato's Jet route skips the keep, and with it the third pass); a replay takes the other
(§8, question 3). Flame's secret route skips the fire vault, mouse room included; Blizzard's skips only the ski run.

Exhibition pairs (PLAN §3.3): **E3 = Blizzard + Flame**, **E4 = Centaur + Yamato**. Both can open before the first
adaptor, which spreads the Exhibitions across the game instead of piling them at the end.

### 0.4 Shared mechanics these venues depend on

Built once, owned by `tech.md`. My working labels (prefix **X-** so they don't collide with PLAN's T1-T8):

| Label | What | Used by | Mark |
|---|---|---|---|
| T3 | Generic switch → target pair (plates, gates, doors, warps, timed gates, the sekisho) | Flame, Centaur, Yamato | `[new-code M · Must]` (shared) |
| T6 | Per-position destructible tiles: a WRAM bit per 16x16 cell, checked by the painters (`$3E:$D1FF`/`$D322`) and the collision read (`$3E:$DA6C`); a "refill" call clears the bit and repaints | Blizzard climb + secret arena | `[new-code M · Must]` |
| T7 | Input mirror: an object that replays the player's pad with LEFT/RIGHT swapped | Flame (Shadow Rock, Shadow Flame Man) | `[new-code M · Should]` |
| T8 | Multi-segment boss framework | Yamato (Daruma) | `[new-code M · Should]` (shared) |
| **X-BONK** | A callback when the player's head hits a ceiling, by collision type. Blizzard: break the ice cell (T6). Yamato: stun every enemy standing on that floor tile | Blizzard, Yamato | `[new-code S · Must]` |
| **X-WRAP** | Horizontal wrap in a locked one-screen room: player X < `$08` → `$F0` and back; enemies flagged "wrap" do the same; per-row opt-out so one floor can lead somewhere else | Blizzard climb, Centaur tower | `[new-code S · Must]` |
| **X-UPEXIT** | Jump-up exit: rising, Y < `$0B`, the cells above open → transition up with a small upward boost. BRIEF §4 lists it as a Could "designed only if a venue needs it"; **Ice Climber needs it** | Blizzard climb, Centaur tower | `[new-code M · Should]`, fallback: a 2-rung ladder stub at each screen top `[engine-ok · Must]` |
| **X-METER** | A stage meter drawn in the boss-bar slot (4MI's TEMP gauge trick, `stages_b.md` lessons) | Blizzard bonus timer | `[new-code S · Must]` |
| **X-LABEL** | A 4-8 letter room label drawn with sprites under the life bar (4MI Pharaoh's curse words) | Centaur ZONE cards, Yamato PASS n/3 | `[new-code S · Should]` |
| **X-EXWP** | A set-piece weapon that replaces the buster for a stretch and is dropped at a stand (4MI EXWP: Quint's pogo) | Yamato pogo | `[new-code M · Must]` |
| **X-FLOOR** | New floor types through the group remap (`$3E:$DB03/$DB13`): *ski snow* (forced slide), *hot spring* (slow heal), *nightingale* (chirps) | Blizzard, Centaur, Yamato | `[new-code S each · Should]` |
| **X-GPOBJ** | One generic "GP object" type with a sub-id and a per-sub-id code bank (4MI's `$5E` pattern). Only 30-32 type ids are free in the whole ROM; these four venues alone add about 45 object kinds | all four | `[new-code M · Must]` |
| Stage-attribute table | BRIEF §7.2; lets the ship (chain 1), tide (chain `$14`) and spike ceiling (chain `$11`) run in any stage | Yamato ceiling; tide in Centaur's boss rooms | `[new-code M · Must]` (tech.md) |
| Commentator pop-up | T2 text window, 1-2 lines, toggleable (BRIEF §5.5) | all hooks in this doc | owned by meta/tech |

### 0.5 Weapon proposals for systems.md

The four bosses here award B.ATTACK, F.BLAST, C.FLASH and Y.SPEAR. BRIEF §5.1 gives each weapon a tap, an alternate
(UP+B or hold) and one form synergy. Each boss fight below **shows the player its weapon's alternate and synergy
before they own it** (a boss move that *is* the alternate). These are proposals; `systems.md` decides.

| Weapon | Tap | Alternate (UP+B) | Form synergy | Cross-venue jobs proposed here |
|---|---|---|---|---|
| **B.ATTACK** | 4 flakes in a spread (vanilla) | an **ice block** (32x16, solid, slippery top, 240 f) | **Jet**: flakes drop straight down as bombs | freezes burning oil into a 300-f ice floor (Flame revisit) |
| **F.BLAST** | fireball that leaves a short pillar | an **upward fire column** | **Power: Burning Knuckle** (flaming lunge punch) | melts `$D` ice (vanilla), **ignites oil** (Flame revisit), burns paper shoji (`$D`) in Yamato |
| **C.FLASH** | screen flash (vanilla, 4 to every class 1/3/F object) | **time stop** 2 s (Flash Man nod) | **Power**: x3 punch damage during a time stop | lights dark rooms for 4 s (Yamato's dark room, Centaur's black zone) |
| **Y.SPEAR** | 3-spear volley | a spear that **sticks in walls** as a one-way platform (240 f) | **Power: the DuckTales pogo** (hold DOWN in the air: bounce on enemies and spikes) | wall spears reach Centaur's high zone ledges and a ledge on Blizzard's ship |

Proposed boss rows (damage / boss i-frames) follow the BRIEF §5.1 shape (weakness 4 dmg and very short i-frames,
most weapons 2 and mid i-frames, buster 1 and ≈ 60 f). Each boss section lists its row and its **self-weapon
reaction** (4MI's Toad/Bright lesson: a boss hit by its own weapon does something special; here it is a joke
instead of damage, once per fight, worth a STYLE point if `meta.md` agrees).

### 0.6 Fiction shared by the four venues

- Every venue opens with a **match card**: `MATCH: ROCKMAN vs BLIZZARD MAN / VENUE: SUMMIT CLIMBER`. The vanilla
  boss-intro panel stays (its stats are English in both languages), and the commentators read from it: Blizzard Man
  runs on SOLAR ENERGY, Centaur Man's specialty is ABILITY UNKNOWN, Yamato Man has MOBILE 31.
- **The Mr. Y gag in every venue** (BRIEF §1), always as cheap BG art or one sprite:
  the icebreaker is the *MR. Y MARU*; a vizier with a familiar moustache watches from the palace balcony; an Atlantean
  mural of a bald man with a moustache labelled "THE Y-MAN SHALL COME"; an Edo **WANTED** poster: `MR. Y - 1,000,000 RYO`.
- The champions are good-natured rivals (BRIEF §2): they trash-talk, they don't hate you.

---

## 1. Blizzard Man: SUMMIT CLIMBER (stage 0)

### 1.1 The pitch

*Frozen Island's mountain course.* You sail to the mountain on the vanilla icebreaker, then climb it the Ice Climber
way: floor by floor, **breaking the ice above your head with your helmet**, while seal-bots patch the holes you made
and birds dive at you. At the summit a 40-second **bonus round** pays out prize vegetables (bolts), and a **condor**
flies over: grab its feet and it carries you to the secret exit. Miss it and you ski down the back of the mountain to
Blizzard Man's lodge.

Homage as mechanics (CX lesson 2):

| Ice Climber | Here | Mark |
|---|---|---|
| Hammer the ice above, jump through the hole | **Head-bonk** breaks the ice cell above (X-BONK + T6); two bonks make a hole wide enough | `[new-code M · Must]` |
| Topi (the Famicom seal) pushes ice into holes | **TOPPY** seal-bot pushes an ice cube into your hole after 300 f | `[new-code S · Must]` `[new-art S]` |
| The screen wraps left/right | **X-WRAP** on every climb screen | `[new-code S · Must]` |
| Floors scroll up as you climb | **X-UPEXIT** (fallback: ladder stubs) | `[new-code M · Should]` |
| Nitpicker birds, icicles, drifting clouds | **NITPICKY** bird-bot, icicles, cloud platforms | `[new-code S · Must]` |
| Bonus stage: vegetables, a 40-s timer, the condor | **BONUS SUMMIT**: vegetables = bolts, X-METER timer, the condor = the secret exit | `[new-code S · Must]` |
| The polar bear in sunglasses who stomps when you dawdle | **SHIROKUMA** cameo (NORMAL) / enforcer (HARD) | `[new-art S · Could]` |

### 1.2 Map shape

```
00-03 harbour ──> 04-07 ICEBREAKER (rocking) ──> 08 shelf [CP1]
                                                   │ up
        1E hidden room <──(no-wrap floor)── 0D     │
                                            0E ◄── 09-0D CLIMB (5 floors per screen, wrap) [CP2 at 0B]
                                            │ up
                                            0F summit approach
                                            │ up
                                            10-11 BONUS SUMMIT ──(condor)──> 17 flight ─> 18 cloud isle ─> 19 shutter ─> 1A SECRET ARENA
                                            │ timer ends: gate opens
                                            12-14 SKI RUN (back side) ─> 15 lodge [shutter CP] ─> 16 BOSS
```

Screens used: main 00-16 (23), secret route 17-1A (4), hidden room 1E (1) = **28 of 32**. Spare: 1B-1D, 1F.

### 1.3 Screen by screen

Peak objects in brackets. CHR and palette are named by vanilla id where kept.

| Scr | What the player does | Enemies and objects | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Start at base camp. Match card. Walk right over snow ledges; a short **slippery ice strip** (type 5) leads to a 1-up on its far end, so the slide is felt with nothing at stake | 1 snow robot `$4D` (F.BLAST one-shot on revisit) [4] | vanilla ice momentum (24-36 px slide) | vanilla v00 art (girders, mountain skyline), CHR `$82`, palette `$15`. Commentator BLZ-01 |
| **01** | The pier: ice floor over freezing water. A hole in the pier (32 px). **Toppy's first appearance is friendly**: it pushes an ice cube into the hole and you walk over it | Toppy x1, red drone `$24` x2 [5] | water below the pier = pit (type F). Teaches that Toppy *fills* holes | the friendly first meeting sets up the climb, where it is the opposite |
| **02** | Count-bomb hop over open water (vanilla v03 idea) | count bombs `$19` x4, drone `$24` x1 [6] | the "3" pods explode once passed | |
| **03** | The gangway. A banner: **MR. Y MARU** (the icebreaker's name; Mr. Y gag). Exit right boards the ship | wall pod `$21` x1 [3] | | exit loads the ship set `$85`, palette `$1A`, and starts effect thread 3 (vanilla script 05) |
| **04** | **THE ICEBREAKER**, bow. The deck rocks (vanilla chain 1, 51 px travel). **Twist: the rocking shakes icicles loose.** At each top turn of the rock (the vanilla thump, sound `$41`), the icicles over the bow shake for 30 f, then drop | cannon rider `$20`+`$1F` x1, icicles x3 [7] | rocking deck; icicles (2 dmg, shootable while hanging) | vanilla v0E-v0F art. Commentator BLZ-03 |
| **05** | Superstructure: climb the pink deckhouse (platforms) | rider x1, icicles x2 [6] | icicles drop at **both** turns here | Power-block crate holding a 1-up (revisit) `[engine-ok]` |
| **06** | Ice floes: the bow breaks a floe field; two **floe platforms** (sprite, class 2) bob with the hull. Jump floe to floe to the stern deck | rider x1, floes x2, icicles x2 [7] | falling between floes = sea pit | the floes reuse the cloud-platform object with ice art |
| **07** | Stern. E-tank on the aft deck (vanilla v12 had one). Disembark right onto the ice shelf | rider x1 [4] | | exit right: CHR `$82`+new set, palette `$1C`; ship thread off (vanilla screen-13 script) |
| **08** | **CHECKPOINT 1** at the foot of the mountain. A wooden sign: `↑ SUMMIT 2,000 M / USE YOUR HEAD` | none [1] | | Checkpoint 1 (08). The climb starts with an up exit at the top right |
| **09** | **Climb 1** (5 floors, 48 px apart: Rockman's jump rises 52 px, measured, so 4 px of clearance). Floor 1 already has a hole; floor 2 has a single breakable cell: **bonk it** (Cossack: "Use your head! Literally."). Floors 3-5 mix breakable blue cells and unbreakable brown rock | Toppy x1 [4] | first wrap: floor 4's only gap is across the screen edge | X-BONK, T6, X-WRAP, X-UPEXIT. Commentator BLZ-05 |
| **0A** | **Climb 2**: two Toppies patch holes 300 f after you make them, so you have to commit to a column | Toppy x2, Nitpicky x1 [6] | Nitpicky dives (tell: hover 20 f + screech) | first Toppy you **shoot** triggers BLZ-07 (the SNOW CHAINS tell) |
| **0B** | **Climb 3**: a wide gap on floor 3 crossed on **two drifting clouds**. *(CHECKPOINT 2 on arrival at the camp ledge on floor 1)* | clouds x2, Nitpicky x1, Toppy x1 [7] | falling from floor 1 is a pit; higher floors fall onto lower floors (safe) | Checkpoint 2 (0B) |
| **0C** | **Climb 4**: slippery-ice floors (type 5): bonking while sliding carries you past the hole. Icicles hang under floor 5 | Toppy x1, icicles x3 [6] | slippery floors + bonk = the venue's skill test | |
| **0D** | **Climb 5**: the **no-wrap floor** (floor 3, see §1.5.2) | Toppy x2 (one walks floor 3), Nitpicky x1 [6] | | the hidden room's tell |
| **0E** | **Climb 6**: icicle chimney. A cave on floor 2 shows **SHIROKUMA**, a polar-bear robot in sunglasses, asleep (cameo; on HARD he is awake, §1.10) | icicles x4, Nitpicky x1 [6] | | Commentator BLZ-08 ("Is that a polar bear in sunglasses?") |
| **0F** | Summit approach: one flat floor, a red flag, a sign `BONUS ↑`. Up exit | none [1] | | `[new-music S · Should]`: the bonus jingle (an original tune in the spirit of a bonus round) starts on the transition |
| **10** | **BONUS SUMMIT 1**: the **X-METER timer starts at 40 s**. Vertical bonus climb (no enemies, no damage): drifting clouds and ledges with **prize vegetables** (eggplant 5, carrot 10, cabbage 15, corn 20 bolts; values for `meta.md`) | clouds x3, vegetables x4 [8] | no pits: falling just costs time | the timer uses the boss-bar slot |
| **11** | **BONUS SUMMIT 2**: the peak. The **condor** crosses the top of the screen right to left, then left to right, at 1.5 px/f, its feet about 40 px above the peak ledge. **Jump and touch its feet** to grab it → screen 17 (secret exit). When the timer ends, the condor leaves, a gate in the peak's right wall opens, and the normal route continues right to 12 (the back of the mountain) | condor, vegetables x3 [5] | | §1.5.1 |
| **12** | **SKI RUN 1**, down the back of the mountain: **ski snow** (X-FLOOR) forces 2.5 px/f to the right; you can jump and shoot but not stop. Moguls, a crevasse (pit) | snow robot `$4D` x1, count bombs x2 [5] | forced slide | `[new-code S · Should]`; the camera follows, no autoscroll needed. If cut: plain downhill steps |
| **13** | **SKI RUN 2**: two crevasses and a snowball rolling in from behind (it is faster than you: jump it) | rolling snowball x1, drone x1 [4] | | Commentator BLZ-09 |
| **14** | **SKI RUN 3**: the run ends at the lodge fence; normal snow from here | Nitpicky x1 [3] | | |
| **15** | Blizzard Man's **ski lodge**: shutter corridor. **Boss checkpoint** | none | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room**: the lodge's sun deck (§1.8) | Blizzard Man | | vanilla boss-room art (snowy mountain backdrop) kept |
| **17** | **Condor flight** (secret route): Rockman hangs from the condor, which flies right at 2 px/f and the camera follows. Nitpickies attack; you can shoot. Press A to let go early (onto clouds below) | condor, Nitpicky x3, clouds x2 [7] | letting go over a gap = pit | the carry is a player state locked to the condor's X/Y |
| **18** | **Cloud isle**: the condor drops you on a cloud bank above the summit. Short platforming over drifting clouds to a snow hut | clouds x3, Toppy x1 [5] | pits | |
| **19** | Secret shutter corridor (checkpoint) | | | shutter checkpoint (`$0684` = 19); plate-style table entry: secret flag on the kill in 1A |
| **1A** | **SECRET ARENA: CLOUD SUMMIT** (§1.9) | Blizzard Man, Toppy x2 | breakable ice floor | killing him here sets the Blizzard secret-exit flag |
| **1E** | **Hidden room: the Vegetable Cellar** (§1.5.2) | | | |

### 1.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 08 | camera on 08 | `$82` + new climb set / `$1C`-based program |
| CP2 | 0B | camera on 0B | same |
| *(CASUAL)* | 05 | camera on 05 (mid-ship: restarts the ship thread) | `$82`+`$85` / `$1A` |
| *(CASUAL)* | 12 | camera on 12 | |
| Shutter | 15 (main), 19 (secret) | shutter entry (vanilla `$3F:$FA20`) | |

T6's cell flags behave like vanilla breakables: they **survive deaths** and reset at stage start, so a hole you made
before dying is still there (and so is any hole a Toppy patched).

### 1.5 Secrets

#### 1.5.1 Secret exit: catch the condor `[new-code S · Must]` `[new-art M]`

- **Gate:** reach screen 11 with time left on the 40-s bonus timer and touch the condor's feet from below. The condor
  makes two passes (about 12 s in all), so a player who reaches the peak with at least 12 s left gets two tries.
- **Tell:** the condor is the tell: it is big, slow and flies low enough that a well-timed jump from the peak ledge
  reaches its feet; the bonus sign on 0F; Kalinka (BLZ-10): "The condor! Jump for its feet!" (only the first time the condor appears, so replays stay
  quiet).
- **Fail state:** none. When the timer ends the gate to 12 opens and the stage goes on (Ice Climber's bonus is the same).
- **Effect:** grab → 17 → 18 → 19 → secret arena 1A. Beating Blizzard Man in 1A clears the venue **and** sets its
  secret-exit flag (new save bit; vanilla has no flag for stages 0-3).

#### 1.5.2 Hidden room: the Vegetable Cellar (1E) `[engine-ok + X-WRAP opt-out · Must]`

- **Gate:** on screen 0D, **floor 3 does not wrap**. Walk off its left edge and a left exit (type 6, explicit target
  `$1F`, so it lands on 1E) takes you into a one-screen ice cave.
- **Tell:** the Toppy that patrols floor 3 walks off the left edge and **does not come back** on the right (every other
  Toppy in the climb visibly wraps). The left wall of floor 3 has a darker, cracked doorframe in the ice.
- **Contents:** a frozen **giant eggplant** statue (Ice Climber's bonus vegetable), an E-tank, two large weapon
  energies and a 50-bolt bag.
- **Return:** walk right off 1E (type 5, target `$0C`, so it lands on 0D) back to floor 3.

#### 1.5.3 Behaviour-gated chip: SNOW CHAINS `[new-code S · Should]`

- **Gate:** **never destroy a Toppy** anywhere in the venue (there are 9). A buster shot only shoves a Toppy 16 px and
  stuns it for 60 f; **any hit of 3 or more damage destroys it** (charged shot, F.BLAST, KNIGHT.C...). Shoving is
  allowed; destroying voids the chip for this visit.
- **Why it is a trade-off** (4MI lesson 3): Toppies patch the holes you need, so sparing them costs time (the
  scorecard's TIME) and patience. The tidy solution, the charged shot, is exactly what voids the chip.
- **Tell:** BLZ-07 on the first Toppy you shoot ("Don't hurt the seals! They're union workers!"). A spared Toppy
  bows as you pass it on a higher floor. The debrief hint (§1.12).
- **Award:** the **Toppy foreman** waits in the shutter corridor (15 on the main route, 19 on the secret route) and
  hands over the chip if no Toppy was destroyed (a sad-seal sprite otherwise). The chip goes to `meta.md`'s list.
- **Proposed effect:** SNOW CHAINS: no ice slide (momentum off on types 5/`$15`), and falling icicles bounce off your
  helmet (no damage).

### 1.6 Tileset slot

- **Kept vanilla CHR:** `$82` (ice blocks, snow ledges, girder scaffolds, mountain skyline, ladders), `$85` (the whole
  ship set: hull, deckhouse, portholes, sea), `$84` (cave tiles, for the ice cellar 1E). Palettes `$15`, `$1A`, `$1C`
  as starting points.
- **New BG tiles** (about 70) `[new-art M · Must]`: Ice Climber floors (breakable ice cell: intact, cracked, gone;
  unbreakable rock floor; grassy ledge ends), cloud tiles, the summit peak and flag, the ski-run fence and moguls,
  the lodge (logs, window, sun deck), the MR. Y MARU banner, the giant eggplant statue, the sign boards.
- **New sprites** (about 110 tiles): Toppy (walk x2, push, stun, bow, sad), ice cube, Nitpicky (fly x2, dive), condor
  (32x24, 2 frames), 4 vegetables, Shirokuma (32x32, 3 frames), icicle (hang, shake, fall), floe/cloud platform,
  Blizzard Man's skis-off and slush-puddle frames, the snowman, the Toppy foreman.
- **Collision:** group 0 (identity) plus the new *ski snow* type (X-FLOOR) and the T6 ice cell (a metatile whose
  per-position bit swaps it to air).

### 1.7 Enemies and objects

| Object | Kind | HP (buster hits) | Behaviour | Mark |
|---|---|---|---|---|
| Snow robot `$4D` | vanilla | 5 | lobs snowballs; F.BLAST one-shot (vanilla table `$EB56`) | `[engine-ok]` |
| Count bomb `$19`/`$21` | vanilla | - | floating platform that explodes once passed | `[engine-ok]` |
| Drone `$24`, cannon riders `$20`/`$1F` | vanilla | 3 / 6 | as vanilla | `[engine-ok]` |
| **TOPPY** (seal-bot) | new | shove only; dies to a hit of 3+ | walks its floor at 0.75 px/f, wraps; 300 f after a hole opens on its floor it fetches an ice cube and pushes it in (refills the T6 cell). Contact 2 | `[new-code S · Must]` |
| **NITPICKY** (bird-bot) | new | 1 | sine flight across the screen; hovers 20 f above Rockman (screech), then dives at 3 px/f. Contact 3 | `[new-code S · Must]` |
| **Icicle** | new | 1 (while hanging) | shakes 30 f, falls 4 px/f, shatters. 2 dmg. On the ship it is triggered by the rock turns | `[new-code S · Must]` |
| **Cloud / floe platform** | new (shared with Centaur) | - | solid sprite platform 48x8, drifts 0.5-1 px/f, wraps on wrap screens, bobs with the ship on 06 | `[new-code S · Must]` |
| **Condor** | new | - | two passes over screen 11; grab = carry state; 17: flies right at 2 px/f | `[new-code S · Must]` |
| **Vegetables** | new | - | bolt pickups | `[new-code S · Must]` |
| **Rolling snowball** | new | 3 | rolls downhill at 3 px/f on the ski run | `[new-code S · Should]` |
| **Shirokuma** | new | - | cameo; HARD enforcer (§1.10) | `[new-code S · Could]` |

### 1.8 Boss: Blizzard Man, "the lodge sun deck" (16)

**Arena:** one screen; a slippery snow floor (type 5) with two short ice shelves at the sides (32 px up). Mountain
backdrop (vanilla).

**Intro (90 f):** he skis in from the right over a mogul, stops in a spray, and holds up a tiny **solar panel** to the
sky. A cloud covers the sun. He sighs. (The vanilla data panel says SOLAR ENERGY; this is the joke.)

**Pattern loop (HP 28 to 10):** SLALOM → FLAKES → SLALOM → SNOWBALL, about 600 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **SLALOM** | crouch, poles planted, 20 f | skis across at 3 px/f (16 px tall), turns at the wall (16 f), skis back | 20 + 75 + 16 + 75 | jump over; contact 4 |
| **FLAKES** (vanilla B.ATTACK) | arms up, 24 f | throws 4 flakes in a spread (they fall at 1 / 1.5 / 2 / 2.5 px/f); the **second flake to land becomes an ice block** (32x16, solid, slippery top, 240 f): **the B.ATTACK alternate, shown** | 24 + 60 + 30 recovery | stand on the block; flakes 2 dmg |
| **SNOWBALL** (vanilla) | hunches "Hup!", 12 f | rolls as a 24-px snowball at 2.5 px/f, bounces off each wall once, **grows 4 px per crossing** (24 → 32). **An ice block stops it**: the ball shatters the block and bounces back | 12 + ~200 + 20 uncurl | jump it, or hide behind an ice block |

**Pinch (HP ≤ 9): AVALANCHE.** On entering pinch and then every second loop: he plants his poles and **yodels**
(60 f, 2-px screen shake: the tell), then three 16-px snowballs drop from the top at x = 40, 128 and 216 and roll
toward the nearer wall at 2 px/f. SLALOM speeds up to 4 px/f, and SNOWBALL splits into two small balls on its second
bounce.

**Proposed row** (damage / i-frames, `systems.md`): F.BLAST **4 / 8** (weakness); KNIGHT.C, Y.SPEAR, SILVER.T,
PLANT.B, W.STORM 2 / 30 (W.STORM also shoves him 16 px); C.FLASH 1 / 40; buster 1 / 60; charged buster 3 / 60; punch
2 / 40, charged punch 3 / 40.

**Weakness reaction, MELT:** F.BLAST turns him into a **slush puddle** for 40 f (no contact damage, WEAK! pop,
commentator BLZ-12), and for the rest of the current move he skis at 2 px/f.

**Self-weapon reaction, SNOWMAN:** the first B.ATTACK hit does 0: he catches the flakes ("Thank you!") and builds a
**snowman** (16x32, 3 hits) in 30 f. The snowman blocks your shots; if his SNOWBALL rolls through it, the ball jumps to
full size. Once per fight; after that B.ATTACK does 1.

**Forms:** a charged Power punch on the rolling SNOWBALL cracks it: he tumbles out stunned for 30 f (free hits). Jet
hovers over the avalanche (one snowball still reaches hover height: 32 px).

**How it teaches B.ATTACK:** FLAKES is the tap; the ice block it leaves is the alternate, and it *works* (it stops the
snowball), so the player has already used the alternate's idea before owning it.

### 1.9 Secret arena: CLOUD SUMMIT (1A) `[new-code S · Must]`

The same fight on the mountain's true peak, above the clouds, with one twist: **the floor is breakable ice cells**
(T6). His SNOWBALL breaks the cells it rolls over on its second crossing (32-px holes) and his FLAKES break the cell
each one lands on. A hole is a pit. **Two Toppies** patrol the floor and refill holes every 240 f; **if no Toppy was
destroyed this visit, four come** ("the seal union stands with you"). The condor circles every 600 f and drops
a vegetable that heals 4 HP. The arena is the payoff for the whole venue: bonk-breaking, Toppy refills and the condor
in one room.

### 1.10 HARD pokes

Per-section poke lists plus AI branches (BRIEF §5.7, the 4MI model):

| Section | Poke | Kind |
|---|---|---|
| Ship 04-07 | icicles drop at **every** turn (NORMAL: top turns only, except 05) | object param |
| Ship 06 | one floe removed (two jumps become one long jump) | object list |
| Climb 09-0E | Toppy refill delay 300 → 150 f; one more Toppy on 0A and 0C | object param + list |
| Climb 0B | the lower cloud removed; floor 3's gap crossed on one cloud | object list |
| Climb 0E | **Shirokuma is awake**: if you stand on one floor for 10 s anywhere in 09-0E, he jumps in and stomps: every open hole on the screen refills and all icicles fall | AI branch |
| Bonus 10-11 | timer 40 → 30 s; the condor makes one pass | param |
| Ski 13 | one more crevasse | layout poke (3 blocks) |
| Boss | pinch at HP ≤ 14; avalanche 3 → 5 balls; SNOWBALL grows 8 px per crossing | AI branch |

### 1.11 Commentator hooks

Drafts for `story.md` (K = Kalinka, C = Cossack; ≤ 2 lines each). Ids are stable so `story.md` can rewrite the text.

| Id | Trigger | Draft |
|---|---|---|
| BLZ-01 | match card ends | K: "Frozen Island! Blizzard Man runs on SOLAR ENERGY." C: "...On a glacier?" |
| BLZ-02 | first slide on ice (00) | C: "Ice is slippery, Rockman. Science!" |
| BLZ-03 | first icicle drops on the ship | K: "The ship is shaking the icicles loose!" |
| BLZ-04 | MR. Y MARU banner on screen | K: "Sponsored by Mr. Y." C: "It's Wily." K: "It's definitely Wily." |
| BLZ-05 | first bonk breaks a cell | C: "Use your head! Literally!" |
| BLZ-06 | first Toppy refill | K: "Hey! It filled the hole back in!" |
| BLZ-07 | first Toppy destroyed | K: "Don't hurt the seals! They're union workers!" |
| BLZ-08 | Shirokuma on screen | C: "Is that... a polar bear in sunglasses?" K: "He looks cool." |
| BLZ-09 | ski run starts | K: "He's skiing! Does he even have skis?" |
| BLZ-10 | condor first appears | K: "The condor! Jump for its feet!" |
| BLZ-11 | condor grabbed | C: "Next stop: the clouds! Hold on, lad!" |
| BLZ-12 | first F.BLAST hit on Blizzard Man | K: "He's melting!" C: "That's what you get for skiing on solar power." |
| BLZ-13 | snowman built | C: "He built a snowman. Mid-match. The judges love it." |
| BLZ-14 | pinch (yodel) | K: "Is he... yodelling?" C: "AVALANCHE!" |

**Death lines** (rotate, BRIEF §5.5):

1. K: "Brr! Rockman's taking a cold nap." C: "Up, lad! It's only minus forty!"
2. C: "In my country we call this weather 'spring'."
3. K: "The seals are clapping. I think that's bad."
4. C: "The mountain always wins the first round."
5. K: "Note to self: helmets are for bonking, not landing."

### 1.12 Judges' debrief hints

First missed secret, in this order (BRIEF §5.4: real hints, never WIP text):

1. Secret exit: "The summit condor only carries climbers who reach it with time on the clock. Jump for its feet."
2. Hidden room: "On the mountain, one floor doesn't wrap around. Watch where the seals walk."
3. SNOW CHAINS: "The seals are only doing their job. A climber who never breaks one earns a set of chains."

### 1.13 How crazy it gets (screenshot moments)

1. Blizzard Man holds up a solar panel in a snowstorm, and a cloud covers the sun.
2. The MR. Y MARU icebreaker rocks so hard the icicles fall off the ceiling.
3. Rockman breaks the ice with his **head**, floor after floor, while a seal patiently fills the holes back in.
4. A polar bear in sunglasses naps in a cave on the way up.
5. A 40-second **bonus round** in a Rockman game, paying out vegetables.
6. Rockman hangs from a condor's feet over a sea of clouds.
7. Blizzard Man builds a snowman in the middle of a boss fight.
8. The secret arena's floor breaks under you, and the seals you spared rush in to patch it.

### 1.14 Revisits and VARIETY

- F.BLAST melts the `$D` ice walls on 0C and 18 (two pockets: a large energy and a 1-up), as vanilla's E-tank at v09.
- Y.SPEAR wall spears reach the high ledge on 05 (bolts).
- KNIGHT.C and SILVER.T clear Nitpickies from below (their arcs reach diving birds).
- B.ATTACK's Jet bombs break ice cells from above, so a revisit can open holes ahead of time: a faster climb for Time
  Attack.
- **Tag partner** (Could): Break Man's shield blocks the icicle rain on the ship if you jump through it; the optional
  shortcut is a stern-deck ledge only his double knockback reaches.

---

## 2. Flame Man: PRINCE OF PERSIA PALACE (stage 3)

### 2.1 The pitch

*The Palace of the Oil Sultanate*, built (unwisely) on Flame Man's oil field. You cross the vanilla oil field at
dusk, drop into the palace dungeon and play it like the 1989 game: pressure plates and portcullises, loose floor tiles,
spikes that spring up, chompers in the doorways, guards who block with their swords, a skeleton that puts itself back
together. In the gallery **you can drop a chandelier into an oil pool to burn the guards standing in it**, but vanilla
oil burns forever (per metatile id, through deaths), so that pool is gone for the rest of your visit. In the mirror
room **your shadow steps out of the glass**: fight it and the stage goes on; **don't**, walk into it, and you merge
and the mirror opens the secret route. Then down into the burning fire vault (vanilla's red cave) and a sword duel
with Flame Man.

| Prince of Persia | Here | Mark |
|---|---|---|
| Raise/drop plates and portcullises; the gate that closes as you roll under it | **T3 plates + gates**, a timed gate you slide under | `[new-code M · Must]` (T3) |
| Loose floor tiles that shake, fall, crush guards and land on plates | **Loose tile** object | `[new-code S · Must]` |
| Spikes that spring up; stepping carefully | **Spike traps**; the slide is the careful step | `[new-code S · Must]` |
| Chompers (slicers) | **Chomper** doors | `[new-code S · Must]` |
| Sword guards who parry | **Palace guard-bots** on the vanilla class-3 shield rule (frontal shots reflect) | `[engine-ok]` rule + `[new-code S · Must]` AI |
| The skeleton that reassembles | **Skeleton-bot** | `[new-code S · Should]` |
| The mirror and the shadow; merging by sheathing the sword | **Shadow Rock** (T7 input mirror): peace = merge = secret exit | `[new-code M · Must]` |
| The princess's mouse presses the plate | **Mouse-bot** = the hidden room | `[new-code S · Should]` |
| The vizier | **The vizier on the balcony is Mr. Y** | `[new-art S · Should]` |

### 2.2 Map shape

```
00-03 oil field (vanilla) ─> 04 drop ─> 05-08 DUNGEON (plates, loose floors, spikes, guard, timed gate)
   ─> 09 [CP1] ─> 0A chompers ─> 0B OIL GALLERY ─> 0C balcony ─> 0D skeleton ─> 0E MIRROR ROOM
                                                                                │ fight the shadow: wall stays
                                                                                │ merge: mirror opens ─> 17 mirror passage ─> 18 rooftops ─> 19 shutter ─> 1A THRONE ROOM (secret)
                                                                               0F down
   10 FIRE VAULT [CP2] ─> 11 hourglass gate ─> 12 mouse alcove ──(mouse)──> 1C hidden room
                                              └─> 13 loose bridge ─> 14 antechamber ─> 15 shutter ─> 16 BOSS
```

Screens used: main 00-16 (23), secret 17-1A (4), hidden room 1C (1) = **28 of 32**. Spare: 1B, 1D-1F.

### 2.3 Screen by screen

| Scr | What the player does | Enemies and objects | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Match card. The oil field at dusk: purple dunes, arches, pipes, **oil pools** (types 6/9: 0.5 px/f walk, lower jump). Walk to the palace on the horizon | Metall `$18` x2 [4] | oil slows you | vanilla v00 art, CHR `$86`, palette `$1E`, oil cycle (thread 4). FLM-01 |
| **01** | **The ignition lesson.** A Fire Telly hovers **120 f** over a small isolated oil pool before it drops. Shoot it and nothing happens; let it drop and the pool ignites, permanently | Fire Telly `$2C` x2 [4] | burning oil = deadly (type F) | Kalinka: "Shoot it before it drops!" (FLM-02). This is FIREPROOF's tell |
| **02** | Pipeline. A wheel cannon; the vanilla **1-up inside a Power block** (v02) | wheel cannon `$C0` x1 [3] | | `[engine-ok]` revisit pocket |
| **03** | **The palace gate.** A portcullis and a raise plate in front of it: step on the plate and the gate rises (60 f) and stays up 300 f. Teaches plates | DANGER drums (scenery) [2] | | T3. Exit right loads the palace CHR set (new) and the dungeon palette. FLM-03 |
| **04** | Inside the gate the floor ends: **drop into the dungeon** (PoP starts in the dungeon). Torches | none [1] | | down exit; torch palette cycle (a bank-`$3B` cycler, data only) |
| **05** | **Loose-floor puzzle.** The right gate is shut. Its plate is on the lower floor, under a loose tile of the upper floor. Walk over the loose tile: it shakes 20 f, falls, **lands on the plate**, and the gate stays open (the tile's weight holds it). A Metall below gets crushed if it is under the tile | Metall x1, loose tiles x3 [5] | loose tiles | the classic PoP move, taught with no damage at stake. FLM-04 |
| **06** | **Spike corridor.** Three spike traps rise 12 f after you come within 24 px and stay up 60 f. **Slide** past (2.5 px/f clears a trap in 13 f): the slide is PoP's careful step | spike traps x3 [4] | spikes = 6 dmg | Jet hovers over; Power waits for the retract. FLM-05 |
| **07** | **First guard duel.** A palace guard-bot: frontal shots reflect (vanilla class-3 shield), he advances and slashes. Shoot him during the 16-f wind-up of his slash, jump behind him, or use a charged punch (always hits class 3) | guard x1 [3] | | FLM-06 |
| **08** | **The timed gate.** A raise plate on the left opens the right gate for 240 f; it lowers during the last 60 f. While its bottom is still 16 px above the floor you can **slide under it** (PoP's roll) | spike trap x1 [3] | gate closes (blocks; no damage) | T3 timed. The plate can be pressed again |
| **09** | **CHECKPOINT 1.** A palace hall: carpets, columns, a window onto the oil field | none [1] | | Checkpoint 1 (09) |
| **0A** | **Chomper hall.** Three chompers in doorways, each closed for 8 f every 90 f, offset by 30 f. Tell: a glint and a "shing" 12 f before they close | chompers x3, Fire Telly x1 [5] | chomper 8 dmg | C.FLASH's time stop freezes them (revisit) |
| **0B** | **THE OIL GALLERY** (the oil twist, §2.5.3). Three oil pools on the floor, each with a guard standing in it and a **chandelier** on a chain above it. Shoot a chain: the chandelier falls, **that pool ignites** (its own metatile id), and its guard burns. The pool is now deadly for the rest of the visit, so you take the **upper balcony** over it instead (harder jumps, a Fire Telly). Or don't, and fight the guards in slow oil | guards x3, chandeliers x3, Fire Telly x1 [8] | the choice per pool; the Telly can ignite a pool itself | each pool uses a **distinct oil metatile id** so they ignite separately (vanilla's per-id rule). FLM-07 |
| **0C** | **The balcony.** A window with the **vizier**: turban, Wily's moustache, waving. Fire Tellies over a last oil channel | Fire Telly x2 [4] | | FLM-08 (the Mr. Y gag) |
| **0D** | **The skeleton.** A skeleton-bot: at 0 HP it collapses into bones for 120 f, then rises with full HP. It is destroyed for good if it falls into the pit in the middle of the room (a **charged shot knocks it back 16 px**), if a loose tile falls on its bones, or if it stands in burning oil. Or just run past while it is bones | skeleton x1, loose tile x1 [4] | pit | |
| **0E** | **THE MIRROR ROOM** (§2.5.1). A tall mirror on the right wall. When you reach the middle of the room, **Shadow Rock** steps out of the glass | Shadow Rock [3] | | FLM-09. T7 |
| **0F** | Down a shaft into the fire vault | Fire Telly x1 [2] | | down exit loads CHR `$87` (vanilla red rock and flames), palette `$1F` |
| **10** | **CHECKPOINT 2. The fire vault** (vanilla v0E-v15 art): channels of oil that are **already burning** (placed as the burning variant), small orange platforms | juggler `$2A` x2, mine `$73` x1 [5] | burning channels | Checkpoint 2 (10). Pre-lit oil does not count against FIREPROOF |
| **11** | **The hourglass gate.** A plate on the left starts a long gate closing over 600 f; a mural hourglass drains (palette cycle). Cross the platforms over burning oil before it shuts. If it shuts, walk back and press the plate again | mine `$73` x2, juggler x1 [5] | | T3 timed. No fail state |
| **12** | **The mouse alcove.** The main route runs over the top platforms. Below, a short dead end: a shut gate, a **mousehole** beside it, and a plate on the far side of the gate (§2.5.2) | juggler x1 [3] | | the hidden room's entrance |
| **13** | **Loose bridge.** A bridge of loose tiles across a burning channel: each tile falls 20 f after you step on it. Jugglers throw flames from the far side | jugglers x2, loose tiles (cells; at most 2 falling at once) [5] | | loose tiles are T6 cells until they fall |
| **14** | The antechamber: two guards in front of the throne-room doors | guards x2 [3] | | |
| **15** | Shutter corridor. **Boss checkpoint.** The **palace fire marshal** stands here (FIREPROOF, §2.5.3) | fire marshal [2] | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room** (§2.8) | Flame Man | | vanilla boss-room art (red pistons, oil-pipe floor) kept, plus two oil strips |
| **17** | **The mirror passage** (secret route): a dark corridor behind the glass, in an inverted purple palette. Mirror panels on the walls show your reflection walking the other way (harmless) | guards x2 (shadow palette) [4] | | palette swap only `[engine-ok]` |
| **18** | **The rooftops at night**: domes, minarets, a crescent moon. Loose roof tiles, a guard, Fire Tellies against the moon | guard x1, Fire Telly x2, loose tiles x3 [7] | pits between domes | new art |
| **19** | Secret shutter corridor (checkpoint) | | | secret flag on the kill in 1A |
| **1A** | **SECRET ARENA: THE THRONE ROOM** (§2.9) | Flame Man + his shadow | | |
| **1C** | **Hidden room: the princess's chamber** (§2.5.2) | | | |

### 2.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 09 | camera on 09 | `$86` + palace set / palace palette |
| CP2 | 10 | camera on 10 | `$86`+`$87` / `$1F` |
| *(CASUAL)* | 0D | camera on 0D | palace |
| Shutter | 15 (main), 19 (secret) | shutter entry | |

Ignited pools, opened gates (held by tiles) and fallen loose tiles all **survive deaths** (they are `$0340` /
per-position flags, like vanilla breakables), so a death never undoes a puzzle you solved, and never un-burns a pool.

### 2.5 Secrets

#### 2.5.1 Secret exit: don't fight your shadow `[new-code M · Must]`

- **Shadow Rock** is a dark-palette Rockman (the player's own sprite, a new palette: no new tiles) that **replays your
  pad with LEFT and RIGHT swapped** (T7). It starts at the mirror facing you, so when you walk toward it, it walks
  toward you. When you fire, it fires. HP 12; contact 4.
- **Fight it:** it fights back with your own moves, mirrored. Beat it and it shatters; the mirror becomes an ordinary
  wall and the stage goes on (0F).
- **Don't:** if you **have not fired since it appeared, for at least 5 s**, and you touch it, you **merge**: a white
  flash, your HP refills (as in PoP), and the mirror cracks open on the passage to 17.
- **Why it is fair:** because the shadow copies you, a player who holds fire is never attacked by it. The rule teaches
  itself to anyone who stops shooting, and PoP players will try it on sight.
- **Tell:** Kalinka (FLM-09): "There's another Rockman!" Cossack: "He copies everything you do. *Everything.*" The
  debrief hint (§2.12).
- **Effect:** merge → 17 → 18 → 19 → the throne room 1A. Beating Flame Man there clears the venue and sets the secret
  flag.

#### 2.5.2 Hidden room: the mouse (1C) `[new-code S · Should]`

- **Gate:** stand in the alcove of screen 12 and **don't touch the pad for 10 s**. A mouse-bot scurries out of the
  mousehole, runs under the gate and sits on the plate on the far side: the gate opens to 1C.
- **Tell:** the mousehole is drawn beside the gate; while you stand in the alcove a squeak plays every 3 s; Kalinka
  (FLM-12) reacts when the mouse appears. The gate itself, shut in front of a dead end with a plate behind it, says
  "something has to get in there".
- **Contents:** the princess's chamber: a big potion (large life energy), an E-tank, two large weapon energies and a
  50-bolt bag. *Could:* **Roll** asleep on the divan, on her pit-crew break: "Oh! You found my nap spot." (BRIEF §2
  optional cameo).
- **Return:** the gate stays open; walk out.

#### 2.5.3 Behaviour-gated chip: FIREPROOF `[new-code S · Should]`

- **Gate:** reach a boss shutter (15, or 19 on the secret route) with **no oil ignited this visit**. Every ignition goes through `$3E:$DDFC`,
  so one hook there clears a "clean" bit; the pre-lit channels of the fire vault are placed burning and never call it.
- **Why it is a trade-off:** the gallery's chandeliers (0B) are the easy way past three guards, and the Fire Tellies of
  01, 0B and 0C will light the oil themselves unless you shoot them before they drop. The chip asks for the hard
  way all the way through.
- **Tell:** screen 01 is the lesson (a Telly hangs 120 f over a pool while Kalinka says "Shoot it before it drops!");
  the first ignition gets Cossack's "...and it stays lit"; the fire marshal stands in plain view at 15 and
  **tsk-tsks** if you failed. The debrief hint.
- **Award:** the fire marshal hands over the chip in the shutter corridor (he stands in 15 and in 19).
- **Proposed effect:** FIREPROOF: burning floors and fire hazards do 4 damage with knockback instead of killing; fire
  projectiles do half.

### 2.6 Tileset slot

- **Kept vanilla CHR:** `$86` (oil field: pipes, girders, DANGER drums, wavy oil, dunes, arches, purple brick walls,
  spikes, ladders) and `$87` (red rock and flame tufts for the fire vault). The oil palette cycle (thread 4,
  `$22-$24`) and the ignite alternates (flame tiles `$E6-$E9`) are kept as they are.
- **New BG tiles** (about 90) `[new-art M · Must]`: dungeon stone and torches, palace columns, arches and PoP-style
  windows, carpets, pressure plates (raised and pressed, via the alternate set), the loose tile's empty socket, chomper
  slots, the mirror (32x48), the hourglass mural, the mousehole, the throne room, rooftop domes, minarets and moon,
  the balcony window.
- **New sprites** (about 100 tiles): guard-bot (stand, advance, slash, block), skeleton-bot (walk, collapse, bones),
  portcullis (16x48), loose tile, chomper blades (2 frames), chandelier (16x24), spike trap (3 frames), mouse-bot,
  the fire marshal, the vizier (cameo), Flame Man's **flaming scimitar**. Shadow Rock reuses the player's tiles with
  a dark palette.

### 2.7 Enemies and objects

| Object | Kind | HP (buster hits) | Behaviour | Mark |
|---|---|---|---|---|
| Metall `$18`, Fire Telly `$2C` (+ drop `$30`), wheel cannon `$C0`/`$C9`, juggler `$2A`, mine `$73` | vanilla | as vanilla | vanilla; the Telly's drop and the juggler's flame ignite oil (vanilla) | `[engine-ok]` |
| **Palace guard-bot** | new | 6 | class-3 shield (frontal shots reflect); advances 0.75 px/f; SLASH: raise 16 f (open to shots), swing 8 f (4 dmg), recover 20 f; in oil it moves at half speed | `[new-code S · Must]` |
| **Skeleton-bot** | new | 4, then bones 120 f, then full HP | slow walk, slash; destroyed for good by a pit, a loose tile or burning oil; a charged shot knocks it back 16 px | `[new-code S · Should]` |
| **Raise plate / gate / timed gate** | new (T3) | - | plate (metatile, alternate set when pressed) + gate (16x48 sprite, solid, rises/lowers 1 px/f) | `[new-code M · Must]` |
| **Loose tile** | new | - | a floor cell (T6 bit) until stood on: it shakes 20 f, then the cell clears and a falling-tile object spawns (so only falling tiles cost an object slot); breaks on landing; 4 dmg to what it lands on; weighs down plates | `[new-code S · Must]` |
| **Spike trap** | new | - | rises 12 f after the player comes within 24 px, up 60 f, down 12 f; 6 dmg | `[new-code S · Must]` |
| **Chomper** | new | - | 8 f closed every 90 f, offset param; tell 12 f; 8 dmg | `[new-code S · Must]` |
| **Chandelier** | new | 1 (the chain) | falls, ignites the pool below (calls the vanilla ignite on that pool's id), 6 dmg if it lands on you | `[new-code S · Must]` |
| **Shadow Rock** | new (T7) | 12 | §2.5.1 | `[new-code M · Must]` |
| **Mouse-bot**, **fire marshal**, **vizier** | new | - | scripted | `[new-code S · Should]` |

### 2.8 Boss: Flame Man, "the palace duel" (16)

**Arena:** the vanilla boss room (red pistons) with **two oil strips** in the floor: the left third and the right
third. The middle third is stone. Arena oil uses a **timed** ignite (burns 90-180 f, then goes out), not the venue's
permanent one, so the fight stays fair.

**Intro (90 f):** Flame Man draws a **flaming scimitar** from his sash, bows, and takes a PoP fencing stance:
"En garde!"

**Pattern loop (HP 28 to 10):** DUEL → PILLARS → LEAP → PILLARS, about 540 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **DUEL** | the stance itself | advances 0.75 px/f with his guard up (**class-3 shield**: frontal shots reflect); after 60 f, THRUST: blade glint 12 f, lunges 24 px in 8 f (4 dmg), recovers 24 f **guard down**. Twice, then a 32-px backstep (20 f) | 60 + (12+8+24) x2 + 20 | shoot during the recovery, jump behind him, or charged punch (always hits class 3) |
| **PILLARS** (vanilla) | kneels, 16 f | two floor flames, 20 f apart, travel at 3 px/f and rise into 16x48 pillars where you stood (45 f). **A pillar on oil ignites that strip for 90 f** | 16 + 40 + 45 | move off the oil; this is F.BLAST's tap, shown |
| **LEAP** (vanilla) | crouch 10 f | jumps high (peak y `$30`) and lands within 24 px of you (50 f airtime); landing in oil splashes two droplets | 10 + 50 + 16 | run under him |

**Pinch (HP ≤ 9): THE PALACE BURNS.** He drives the scimitar into the floor (40 f, the room tints red: the tell). Both
oil strips ignite **from the walls inward**, 8 px every 4 f, and burn for 180 f; the stone middle stays safe. While
the strips burn he fights in the middle (DUEL only), and once per burn a **fire column rises from the floor and sweeps
across the room** at 2 px/f (16x40: jumpable): the F.BLAST alternate, shown. The strips relight every 300 f.

**Proposed row:** W.STORM **4 / 8** (weakness); KNIGHT.C, SILVER.T, Y.SPEAR, B.ATTACK, PLANT.B 2 / 30 (B.ATTACK
also puts out a burning strip for 120 f); C.FLASH 1 / 40; buster 1 / 60 (reflected while his guard is up); charged
buster 3 / 60; punch 2 / 40; charged punch 3 / 40 + DISARM.

**Weakness reaction, BLOWOUT:** W.STORM blows out the flame on his head. He pats his head and fumbles to relight it
for 40 f: no guard, no attacks, WEAK! pop, FLM-14.

**Self-weapon reaction, ABSORB:** the first F.BLAST hit heals him 1 and his flame grows: for 300 f PILLARS fires three
flames instead of two. FLM-15: "You *fed* him?"

**Forms:** a charged Power punch hits through his guard and **disarms** him: the scimitar spins into the ceiling and
sticks there for one loop (no DUEL until he pulls it down). His flaming lunge is the **Burning Knuckle** synergy,
shown before the player owns it.

### 2.9 Secret arena: THE THRONE ROOM (1A) `[new-code M · Should]`

The palace's real throne room, with the hourglass mural behind the throne. The twist: **now Flame Man has a shadow.**
A dark Shadow Flame Man (Flame Man's sprite, dark palette) stands mirrored across the room's centre line and copies
every move, mirrored, so DUEL thrusts and PILLARS come from both sides. The shadow cannot be hurt and deals half
damage. **Each weakness hit (W.STORM) makes it flicker; the third one blows it out for good.** The player who merged
with their own shadow to get here now has to beat a man who didn't. (If T7 slips, the fallback is the main fight on
an all-oil floor: slow walk, low jump. `[engine-ok]`)

### 2.10 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| Ignition lesson 01 | the Telly hovers 60 f instead of 120 f | AI param |
| Dungeon 06 | spikes rise 6 f after you come in range (a slide started early still clears them) | param |
| Dungeon 08 | timed gate 240 → 180 f | param |
| All | loose tiles shake 10 f instead of 20 f | param |
| Chompers 0A | cycle 90 → 70 f, closed 8 → 12 f | param |
| Gallery 0B | one more Fire Telly; guards slash every 40 f | object list + param |
| Skeleton 0D | rises after 60 f | param |
| Mirror 0E | the merge needs 8 s without firing; contact damage 6 | param |
| Fire vault 11 | hourglass gate 600 → 420 f | param |
| Boss | pinch at HP ≤ 14; DUEL thrusts three times; the strips relight every 200 f | AI branch |

### 2.11 Commentator hooks

| Id | Trigger | Draft |
|---|---|---|
| FLM-01 | match card ends | K: "The Palace of the Oil Sultanate!" C: "Built on an oil field. What could go wrong?" |
| FLM-02 | Telly over the pool (01) / the pool ignites | K: "Shoot it before it drops!" / C: "The oil's lit. And it stays lit. Remember that." |
| FLM-03 | first plate pressed | K: "A pressure plate! Just like the old computer games!" |
| FLM-04 | first loose tile falls | C: "That's the 'loose' in 'loose floor'." |
| FLM-05 | first spike trap | K: "Slide! Tiptoe! Do something!" |
| FLM-06 | first shot reflected by a guard | C: "His guard's up. Hit him while he swings." |
| FLM-07 | a chandelier ignites a pool | K: "You set the gallery on fire!" C: "Effective. Expensive." |
| FLM-08 | the vizier on screen | K: "Who's on the balcony?" C: "A vizier with Wily's moustache." K: "It's Mr. Y." C: "It's *Wily*." |
| FLM-09 | Shadow Rock appears | K: "There's another Rockman!" C: "He copies everything you do. *Everything.*" |
| FLM-10 | merge | K: "They... merged?" C: "Sometimes the best fight is no fight at all." |
| FLM-11 | Shadow Rock destroyed | C: "You beat yourself. Philosophically troubling." |
| FLM-12 | the mouse appears | K: "A mouse! It's pressing the plate! Good mouse!" |
| FLM-13 | FIREPROOF awarded / refused | C: "The fire marshal approves. A rare event in this palace." / K: "He's tutting at you." |
| FLM-14 | first W.STORM hit | K: "His flame went out!" C: "He's looking for a match." |
| FLM-15 | F.BLAST on Flame Man | C: "You *fed* him?" |
| FLM-16 | pinch | K: "The whole floor's on fire!" |

**Death lines:** 1. K: "Sliced!" C: "The palace has a strict no-running policy." 2. C: "Oil and fire. Who could
have predicted this?" 3. K: "The floor fell!" C: "Read the brochure, lad: *loose* floors." 4. C: "The hourglass
doesn't stop for retries." 5. K: "The vizier is laughing." C: "Wily always laughs."

### 2.12 Judges' debrief hints

1. Secret exit: "Your shadow only fights if you fight. Hold your fire and walk into it."
2. Hidden room: "Something small lives behind a gate in the fire vault. Stand still and listen."
3. FIREPROOF: "The palace fire marshal rewards entrants who leave the oil unlit. Shoot the fire-droppers first."

### 2.13 How crazy it gets

1. Rockman slides under a closing portcullis like a 1989 prince.
2. A chandelier crashes into an oil pool and the guards standing in it go up in flames, and the pool burns for the rest
   of the match.
3. A vizier with Wily's moustache waves from the balcony.
4. Rockman meets his own shadow, and the winning move is a hug.
5. A mouse opens the secret room.
6. A skeleton guard falls apart and puts itself back together.
7. Flame Man draws a flaming scimitar and fights a fencing duel.
8. In the throne room, Flame Man has a shadow of his own.

### 2.14 Revisits and VARIETY

- **F.BLAST ignites oil** on purpose: burn the gallery's guards from the floor without the chandeliers.
- **B.ATTACK freezes burning oil** into a 300-f ice floor: a shortcut across 13's channel to a bolt ledge.
- **C.FLASH's time stop freezes chompers** (0A) and the hourglass gate (11).
- **W.STORM** blows the Fire Tellies' drops sideways off the oil (they land on stone).
- **Y.SPEAR** wall spears up the mirror room's high ledge (a large weapon energy).
- **Tag partner** (Could): Break Man's shield catches the guards' slashes from the front; the optional shortcut is a
  guard on a ledge over 18's pit that only his double knockback can push off.

---

## 3. Centaur Man: ATLANTIS RUINS (stage 7)

### 3.1 The pitch

*The Ancient City* (vanilla's location), sunk under the sea. **Every room is a ZONE with a number**, shown under the
life bar the way 4MI shows Pharaoh's curses. Doors carry zone numbers on their plaques, and most tell the truth: but
in Atlantis **cracked doors lie** (a "ZONE 99" that drops you back to ZONE 8), **painted doors are fake**, and in the
**black zone** the only thing you can see is what glows, including a door to ZONE 0 that only shines in the dark.
Then the **tide** (vanilla's raster set piece) rises and falls through the halls, and here it is a tool: at high tide
you swim-jump up to ledges you can't reach on foot, and at the lowest tide a barnacled door marked **ZONE 100** opens:
the secret exit. The way out is a **Kid Icarus** climb up a wrap-around tower (a Grim Reap-bot with a siren, a wizard
who turns you into an eggplant, a hot spring that turns you back), then the vanilla 112-px **Pegasus gap**: fall in
for the main route, or fly over it with the Jet to the sky temple and Beat's **T plate**.

| Homage | Here | Mark |
|---|---|---|
| *Atlantis*: numbered zones | **X-LABEL** ZONE card per room | `[new-code S · Should]` |
| *Atlantis*: doors that warp, doors that send you back, doors that aren't | **Zone doors** (T3 warp): honest, lying (cracked lintel), fake (painted) | `[new-code M · Must]` |
| *Atlantis*: dark "black" zones | **The black zone** (palette black; doors' plaques glow) | `[engine-ok]` palette + `[new-code S]` |
| *Atlantis*: warping deep into the game | **ZONE 100**, the tide door (secret exit) | `[new-code S · Must]` |
| *Kid Icarus*: the Underworld climb that wraps left/right | **The tower** (X-WRAP, X-UPEXIT or ladder stubs) | `[new-code S · Must]` |
| *Kid Icarus*: the Reaper who panics and calls Reapettes | **Grim Reap-bot** with a siren and Reaplets | `[new-code S · Should]` |
| *Kid Icarus*: the Eggplant Wizard; the hospital | **Nasubi Mage**; a **hot spring** cures it (and slowly heals) | `[new-code M · Could]` (the curse), `[new-code S · Should]` (the spring) |
| *Kid Icarus*: Centurions who help at the boss | **Centurion-bots**, freed from stone (the behaviour chip) | `[new-code S · Should]` |
| *Kid Icarus*: Pegasus, the sky temple | the Jet over the **Pegasus gap**; the **sky temple** holds the T plate | `[engine-ok]` geometry |

### 3.2 Map shape

```
00-03 ZONES 1-4 sky ruins (vanilla) ─> 04 down ─> 05 ZONE 6 sea corridor ─> 06 ZONE 7 [CP1] tablet
   ─door─> 07-0B ZONE MAZE (ZONES 8-12, locked rooms, doors; 0A = BLACK ZONE ──"0" door──> 1D hidden room)
   ─door─> 0C ZONE 13 [CP2] TIDE ─> 0D ZONE 14 ─> 0E ZONE 15 ──(lowest tide: "100" door)──> 1A ZONE 100 ─> 1B shutter ─> 1C SUNKEN THRONE (secret)
   ─> 0F ZONE 16 waterfall ─up─> 10-13 TOWER (ZONES 17-20, wrap) ─> 14 ZONE 21 PEGASUS GAP
          fall: 15 lower hall ─> 16 shutter ─> 17 BOSS (tide arena)
          Jet:  18 sky bridge ─> 19 SKY TEMPLE (T plate) ─drop─> 15
```

Screens used: main 00-17 (24), T route 18-19 (2), secret 1A-1C (3), hidden room 1D (1) = **30 of 32**. Spare: 1E, 1F.

### 3.3 The door rules (taught on screen 06)

A stone tablet at checkpoint 1 reads: `IN ATLANTIS AN HONEST DOOR SHOWS WHERE IT GOES. A CRACKED DOOR LIES. A PAINTED
DOOR IS A PAINTING.` That is the whole rule set, and the tell for every door in the maze:

- **Honest door**: the plaque's number is the zone it leads to.
- **Lying door** (cracked lintel): shows a big number and **sends you back** to an earlier zone (ZONE 8's lies to
  ZONE 7, ZONE 12's to ZONE 8; on HARD both send you to ZONE 1). It never kills; it costs time (Atlantis's
  notorious warps back, made fair by the crack).
- **Fake door** (painted, flat shading): pressing UP bonks Rockman's head (sound, 8-f stun, no damage on NORMAL).
- Doors are entered with UP (16-f fade, then a teleport through the vanilla `$39:$89F5` path). Maze rooms are locked
  single screens (mode 0), so they don't have to be neighbours in the layout.

### 3.4 Screen by screen

| Scr | ZONE | What the player does | Enemies and objects | Hazards and set pieces | Notes |
|---|---|---|---|---|---|
| **00** | 1 | Match card. Sky ruins: purple fluted columns, gold capitals, clouds. **Centurion statue #1** on a pedestal by the path: cracked stone, eyes that blink | Centurion statue [3] | | vanilla v00 art, CHR `$AA`, palette `$A6`. CEN-01, CEN-02 |
| **01** | 2 | **Drifting cloud platforms** over a sky gap | clouds x3, pelican spawner `$A9` + `$AB` x2 [7] | sky gap = pit | cloud object shared with Blizzard |
| **02** | 3 | More clouds; pelicans bomb from above | clouds x2, `$AB` x2 [6] | | |
| **03** | 4 | **The Y-MAN mural** (a bald Atlantean with a moustache: `THE Y-MAN SHALL COME`). One door, plaque `5`: the door lesson | door x1 [2] | | CEN-03 |
| **04** | 5 | Down into the drowned city: water begins (type 8, floaty gravity) | piranha `$C1` x2 [3] | | down exit (vanilla v04 → v05 shape) |
| **05** | 6 | Underwater corridor (vanilla v06-v08 art). **Centurion #2** sits in an alcove above the corridor (a swim-jump) | piranhas x3, wall cannon `$C9` x2 [6] | | palette `$A7` |
| **06** | 7 | **CHECKPOINT 1.** The stone tablet (§3.3). A door `8` | door [2] | | Checkpoint 1 (06). CEN-04 |
| **07** | 8 | **MAZE 1.** Three doors: `9` (honest), `12` (**cracked**: lies, back to 06), and a painted door. A piranha pond between them | piranhas x2, doors x3 [6] | | CEN-05, CEN-06 |
| **08** | 9 | **MAZE 2.** Doors `10` (honest) and `11` (honest: **skips ZONE 10**, and with it Centurion #3) | wall cannon x1, doors x2 [4] | | the first real choice |
| **09** | 10 | **MAZE 3.** **Nasubi Mage** floats over the room throwing eggplants. **Centurion #3** on a ledge. A **hot spring** pool in the corner. Door `11` | Nasubi Mage, statue, door [4] | eggplant curse (Could) | CEN-09, CEN-10 |
| **0A** | 11 | **MAZE 4: THE BLACK ZONE.** The BG palette goes black; only sprites, the doors' glowing plaques and a few glowing wall glyphs show the room. Door `12` (honest). **The `0` door** glows on a high ledge reached from a floating stone (§3.6.2) | piranhas x2, floating stone x1, doors x2 [6] | jumps in the dark | CEN-07. C.FLASH lights it on revisit |
| **0B** | 12 | **MAZE 5.** Doors `13` (honest) and `99` (**cracked**: lies, back to 07) | seahorse `$C4` x1, doors x2 [4] | | |
| **0C** | 13 | **CHECKPOINT 2.** **The tide starts** (vanilla chain `$14`, about 60 px of travel). GP adds a **60-f dwell** at both extremes, so "high tide" and "low tide" are states you can read and wait for | seahorse x1 [3] | | Checkpoint 2 (0C); the vanilla tide init (script 5B) moved here, plus the dwell parameter (`tech.md`) |
| **0D** | 14 | **The tide as a lift.** A ledge with a large energy and the way on sits 80 px up: **only a swim-jump at high tide** reaches it. At low tide you walk under the overhang | seahorses x2 [4] | | CEN-12 |
| **0E** | 15 | **THE SUNKEN DOOR.** On the floor of the room, a barnacled door with the plaque `100` and a painted tide line across it. It opens **only while the tide is at its lowest** (the 60-f dwell plus the slow approach: about 90 f in each 6-s cycle of 244 f of travel plus two dwells). Otherwise UP does nothing and bubbles stream from its frame (§3.6.1) | seahorse x1, piranhas x2 [5] | | the secret exit. CEN-13 |
| **0F** | 16 | Waterfall room (vanilla v0E-v0F): climb out of the water past dome turrets and a red spearman | dome turret `$2B` x2, spearman `$70` x1 [5] | | up exit; palette `$CA` |
| **10** | 17 | **Tower base** (Kid Icarus Underworld bricks): a hot spring, a second Nasubi Mage | Nasubi Mage, waterfall enemy `$A5` x1 [4] | | |
| **11** | 18 | **TOWER 1** (X-WRAP): a **Grim Reap-bot** patrols the middle floor. Sneak behind him or kill him before he turns (§3.7) | Reap-bot [3 → 7 on alarm] | | CEN-11 |
| **12** | 19 | **TOWER 2**: a floor whose only gap is across the wrap; floating stones | Reap-bot, `$AB` x1 [4 → 8] | | |
| **13** | 20 | **TOWER 3**: the top. The vanilla **jester head** `$10` guards it, its crest now drawn as snakes | jester head `$10` [3] | | CEN-14. Palette swap of `$10` only |
| **14** | 21 | **THE PEGASUS GAP** (vanilla v15: 112 px wide, the far floor 32 px lower). **Fall in** for the main route; **fly across with the Jet** to the T route (18) | pelicans x2 [4] | | vanilla geometry kept exactly (the Jet's measured crossing: hold A 100+ f) |
| **15** | ? | The lower hall (the fall lands here; vanilla v18 shape). The ZONE card shows `??` | spearman `$70` x1 [3] | | down exit target, back exit up* to 14 as vanilla |
| **16** | | Shutter corridor. **Boss checkpoint** | | | shutter checkpoint (`$0684` = 16) |
| **17** | | **Boss room: the Temple of Tides** (§3.8) | Centaur Man | the tide | |
| **18** | | **SKY BRIDGE** (T route): Kid Icarus sky: clouds, three small landing islands to rest on while the Jet's fuel regrows (+1 per 2 f), pelicans | clouds x3, `$AB` x2 [7] | pits | CEN-15 |
| **19** | | **THE SKY TEMPLE**: Beat's **T plate** on the altar (§3.6.4). A hole in the floor drops you back to 15 | T plate [2] | | CEN-16 |
| **1A** | 100 | **ZONE 100** (secret route): the Atlantean core, fully underwater, coral and gold. Currents from vents | piranhas x3, seahorse x1 [5] | currents | palette from the vanilla **revisit** set (bank `$28`: gold turns orange-brown), free |
| **1B** | | Secret shutter corridor (checkpoint) | | | |
| **1C** | | **SECRET ARENA: THE SUNKEN THRONE** (§3.9) | Centaur Man | | |
| **1D** | 0 | **Hidden room: ZONE 0** (§3.6.2) | | | |

### 3.5 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 06 | camera on 06 | `$AA` / `$A7` program |
| CP2 | 0C | camera on 0C (tide init) | `$AA` / tide palette |
| *(CASUAL)* | 0A | camera on 0A (the black zone) | black-zone palette |
| *(CASUAL)* | 11 | camera on 11 | tower palette |
| Shutter | 16 (main), 1B (secret) | shutter entry | |

### 3.6 Secrets

#### 3.6.1 Secret exit: ZONE 100 `[new-code S · Must]`

- **Gate:** in ZONE 15 (0E), press UP at the barnacled `100` door **while the tide is at its lowest**. The door object
  reads the tide variable (`$069C`, vanilla) and is open only in the bottom 16 px of the tide's travel plus the GP
  dwell (about 90 f in each cycle).
- **Tell:** the door is in plain sight on the room's floor; a tide line is painted across its frame at exactly the
  open level; while it is shut, bubbles stream from it and UP plays a "locked" thunk. Kalinka (CEN-13) when it first
  opens: "ZONE 100? That's the whole game!" Atlantis players know the legend of warping deep.
- **Effect:** 1A → 1B → the Sunken Throne 1C; the kill sets the secret flag.

#### 3.6.2 Hidden room: ZONE 0 (1D) `[new-code S · Must]`

- **Gate:** in the black zone (0A), a door whose plaque reads `0` **glows only while the room is dark**. It sits on a
  ledge reached from a floating stone. Enter it with UP.
- **Tell:** it glows (in a room where glowing is how you find things: the honest door `12` glows the same way).
  Cossack (CEN-07): "Look for what shines." On a revisit, C.FLASH lights the room and the `0` door disappears for
  4 s: "it only shines in the dark" is literal.
- **Contents:** the treasure room of Atlantis: an E-tank, a 1-up, two large weapon energies, a 50-bolt bag, and a
  wall inscription: `ZONE 0: THE ZONE BEFORE THE FIRST. YOU WERE NOT SUPPOSED TO FIND THIS.`
- **Return:** a door `11` leads back to the black zone.

#### 3.6.3 Behaviour-gated chip: CENTURION `[new-code S · Should]`

- **Gate:** free all three **Centurion statues** (00, 05, 09) with a **fully charged buster shot** (`$13`) in normal
  form. Other shots "tink" off the stone. Freed, each one says `THANK YOU!` in a pop-up and flies off.
- **Why it is behaviour, not geometry:** #2 needs a swim-jump detour, and #3 is in ZONE 10, which door `11` of ZONE 9
  lets you skip. A player in a hurry misses them.
- **Tell:** the statues blink; the first shot that tinks off one gets K: "That statue... blinked?"; CEN-08 on the
  first one freed. The debrief hint.
- **Award and payoff:** in Centaur Man's fight, each freed Centurion hovers at the screen edge and intercepts one
  pellet or arrow aimed at you (Kid Icarus: Centurions help at the boss). With all three freed, the judges award the
  chip after the fight.
- **Proposed effect:** CENTURION: at the start of each boss fight, one Centurion-bot hovers beside you and blocks the
  first three projectiles that would hit you.

#### 3.6.4 Plate T: the sky temple `[engine-ok geometry + new-code S · Must]`

- **Gate:** the vanilla Pegasus gap (14), crossed with the **Jet** (Jet arrives after the 4th win; BRIEF §4). The
  gap's numbers are kept exactly, so the vanilla measurements still hold: normal jumps fall in, the Jet hovers across.
- **Change from vanilla:** the plate is a **pickup on the sky temple's altar** (19), using the Energy Balancer's
  pattern (an object guarded by its progress bit, `stages_b.md` lessons) instead of a second boss room, and the route
  **rejoins the main route** by dropping into 15. The vanilla YOU GET line `C.FLRSH AND BEAT T-PARTS` (script `$6B`)
  still plays at the boss kill if the plate was taken this visit, typo and all (BRIEF §6 keeps C.FLRSH).
- **Tell:** from the gap's near edge you can see the temple's gold roof on the far side, and the plate glints on it.

### 3.7 Enemies and objects

| Object | Kind | HP (buster hits) | Behaviour | Mark |
|---|---|---|---|---|
| Pelicans `$A9`/`$AB`, piranha `$C1`, wall cannon `$C9`, seahorse `$C4`, dome turret `$2B`, spearman `$70`, waterfall enemy `$A5`, jester head `$10` | vanilla | as vanilla | as vanilla | `[engine-ok]` |
| **Zone door** (honest / lying / fake) | new (T3) | - | §3.3; the plaque digits are sprites (shared with the ZONE card digits) | `[new-code M · Must]` |
| **Cloud platform** | new (shared) | - | as Blizzard | `[new-code S · Must]` |
| **Centurion statue** | new | immune except to `$13`; then freed | §3.6.3 | `[new-code S · Should]` |
| **Nasubi Mage** | new | 4 | floats in a figure-8, every 150 f throws an eggplant in an arc (tell: raises his staff 20 f). The eggplant does 2 dmg; *Could:* it **curses** you instead: 6 s as Eggplant-Rock (walk and jump only, no shots, no menu); water or the hot spring cures it early | `[new-code S · Should]`; curse `[new-code M · Could]` `[new-art S]` |
| **Hot spring** | new floor (X-FLOOR) | - | water with steam; standing in it heals 1 HP every 30 f and cures the curse | `[new-code S · Should]` |
| **Grim Reap-bot** | new | 8 | patrols at 0.5 px/f; every 120 f stops and looks around (20 f, the tell) and turns; sees 64 px ahead (±24 px vertically). **On sight:** a siren, he flashes red and 4 **Reaplets** (1 hit each, home at 0.75 px/f, contact 2) dive in from the top. Contact 4 | `[new-code S · Should]` |
| **ZONE 100 door** | new | - | §3.6.1 | `[new-code S · Must]` |
| **T plate** | new (progress-bit pickup) | - | §3.6.4 | `[new-code S · Must]` |

### 3.8 Boss: Centaur Man, "the Temple of Tides" (17)

**Arena:** a temple hall with the **tide** running (vanilla chain `$14` in a stage-7 room, so the collision offset
works as it is) plus the GP dwell. At low tide the floor is dry; at high tide the water covers the lower 60 px and
everyone swims (floaty jumps for Rockman; Centaur Man gallops at reduced speed).

**Intro (90 f):** he gallops in, rears, and a placard pops over his head: `SPECIALTY: ???`. (The vanilla data panel
says ABILITY UNKNOWN; the pinch pays this off.)

**Pattern loop (HP 28 to 10):** he picks by the tide: GALLOP at low tide, TIME FLASH at high tide, BLINK & BURST in
between. About 480 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **GALLOP** | rears, neighs, 20 f | charges across at 4 px/f (2.5 in water), turns at the wall (12 f), charges back | 20 + ~64 + 12 + ~64 | jump him; easy at high tide, so he saves it for low tide |
| **BLINK & BURST** (vanilla) | fades out, 16 f | reappears 48 px from you, on your facing side, and fires a shot (2 px/f) that bursts after 40 f into 6 pellets | 16 + 16 + 40 + 20 | move away from the burst point; the C.FLASH tap's "hits everything", shown |
| **TIME FLASH** | raises his arms; three clock ticks, 30 f | screen flash (4 f), then **time stops for 60 f**: you and the projectiles freeze, greyed. He trots to the far side and sets **3 arrows** in the air aimed at where you stand. Time resumes: the arrows fly at 3 px/f | 30 + 4 + 60 + 40 | the arrows start at least 64 px away: jump or swim out of the line. **The C.FLASH alternate (time stop), shown** |

**Pinch (HP ≤ 9): ABILITY UNKNOWN.** A three-icon **slot reel** appears over his head (WAVE / FLASH / GALLOP),
spins 40 f, stops, and the icon stays up for 30 f (the tell). Then:

- **WAVE**: the tide jumps to its maximum for 180 f and a current pushes you toward the far wall at 0.5 px/f while he
  fires BLINK & BURST twice.
- **FLASH**: two TIME FLASHes back to back (two sets of three arrows).
- **GALLOP**: three charges at 5 px/f.

Between spins he does BLINK & BURST. Commentator CEN-19: "So *that's* his ability!" "It's... gambling?"

**Proposed row:** KNIGHT.C **4 / 8** (weakness); Y.SPEAR, W.STORM, B.ATTACK, F.BLAST, SILVER.T, PLANT.B 2 / 30; buster
1 / 60; charged buster 3 / 60; punch 2 / 40; charged punch 3 / 40. During his own time stop nothing can hit him.

**Weakness reaction, STUMBLE:** a KNIGHT.C hit buckles his front legs: he kneels for 40 f (WEAK! pop, CEN-17).

**Self-weapon reaction, SAY CHEESE:** the first C.FLASH does 0: he strikes a heroic pose for 60 f as if for a
camera flash (CEN-18). Free hits for 60 f, once per fight.

**Centurions:** each one freed this visit hovers at the edge and intercepts one pellet or arrow (§3.6.3).

**Forms:** Jet hovers above the tide's surface (GALLOP can't reach it; arrows can). Power: a charged punch to his
flank during a GALLOP turn knocks him over for 30 f.

### 3.9 Secret arena: THE SUNKEN THRONE (1C) `[new-code S · Should]`

The throne room of Atlantis, entirely underwater (no tide: water everywhere, floaty jumps all fight). Centaur Man
fights as a **sea-centaur** (the vanilla sprite with a sea-green palette and a fish-tail overlay sprite). GALLOP becomes
a **looping swim charge** (a diagonal figure-8 across the room at 3 px/f). Two vents in the floor alternate every 240 f,
pushing you sideways at 0.5 px/f (tell: bubbles 30 f before). His pinch reel gains a fourth icon, **WHIRLPOOL** (a
current that circles the room for 180 f).

### 3.10 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| Maze 07, 0B | lying doors send you to **ZONE 1** (00), as Atlantis would; the checkpoint is still 06 | object param |
| Maze | fake doors bite: 2 dmg | object param |
| Tide 0C-0E | dwell 60 → 30 f; the tide moves 1 px per frame instead of every other frame | param |
| ZONE 100 | the open window shrinks with the dwell | (follows) |
| Tower 11-12 | Reap-bot sight 64 → 96 px; 6 Reaplets | param |
| Tower 12 | one floating stone removed | object list |
| Nasubi Mage | eggplant curse 6 → 10 s | param |
| T route 18 | one landing island removed (fuel discipline) | object list |
| Boss | pinch at HP ≤ 14; time stop 60 → 90 f; burst 6 → 8 pellets | AI branch |

### 3.11 Commentator hooks

| Id | Trigger | Draft |
|---|---|---|
| CEN-01 | match card ends | K: "Centaur Man! Specialty: ABILITY UNKNOWN." C: "Even the judges don't know." |
| CEN-02 | first ZONE card | K: "ZONE 1? How many zones are there?" C: "In Atlantis? At least a hundred." |
| CEN-03 | first door | C: "Doors in Atlantis go where they like, Rockman." |
| CEN-04 | the tablet (06) | K: "'A cracked door lies.' Helpful!" |
| CEN-05 | a lying door used | K: "Back to ZONE 7?! That's so mean!" |
| CEN-06 | a fake door bonked | K: "It's a *painting*!" |
| CEN-07 | the black zone | K: "I can't see a thing!" C: "Then look for what shines." |
| CEN-08 | a Centurion freed | K: "The statue said thank you!" |
| CEN-09 | eggplant curse (Could) / first eggplant | K: "He's... an eggplant." C: "A very determined eggplant." |
| CEN-10 | first hot spring | C: "A hot spring! Even robots need a soak." |
| CEN-11 | Reap-bot alarm | K: "He saw you! RUN!" |
| CEN-12 | first high tide | C: "High tide! You'll jump like a fish." |
| CEN-13 | ZONE 100 opens | K: "ZONE 100? That's the whole game!" |
| CEN-14 | the snake-crested jester head | K: "Is that Medusa?" C: "A jester with snakes. Budget cuts." |
| CEN-15 | Jet over the gap | C: "Wings! Well, a dog. Close enough." |
| CEN-16 | T plate taken | K: "Beat's T-parts!" |
| CEN-17 | first KNIGHT.C hit | K: "His legs buckled!" |
| CEN-18 | C.FLASH on Centaur Man | C: "He's posing for the photo! Say cheese!" |
| CEN-19 | pinch reel | K: "So *that's* his ability!" C: "It's... gambling?" |
| CEN-20 | YOU GET C.FLRSH | K: "C... F-L-R-S-H?" C: "The engraver was paid by the letter." |

**Death lines:** 1. K: "Wrong door!" C: "In Atlantis, every door is the wrong door." 2. C: "Centaur Man runs on a DRY
battery. Rockman, evidently, does not." 3. K: "The tide waits for no robot." 4. C: "Only ninety-nine zones to go."
5. K: "A vegetable has fallen." (after an eggplant death)

### 3.12 Judges' debrief hints

1. Secret exit: "Atlantis keeps its deepest door underwater. In ZONE 15, wait for the lowest tide."
2. Hidden room: "In the black zone, one door only shines with the lights off. Climb to it."
3. CENTURION: "Three soldiers in the ruins are not statues. A charged shot wakes them."
4. Plate T: "Beat's T-plate rests in a temple beyond the Pegasus gap. You'll need wings, or a Jet."

### 3.13 How crazy it gets

1. Every room has a ZONE number, and a door in ZONE 12 sends you back to ZONE 8.
2. A door labelled 99 that lies, and a door labelled 0 that only exists in the dark.
3. The tide is an elevator: wait for high tide and swim up to the ledge.
4. Rockman turned into an eggplant, soaking in a hot spring to turn back.
5. A Grim Reap-bot with a siren.
6. Centaur Man's ABILITY UNKNOWN turns out to be a slot machine over his head.
7. Centaur Man freezes time and lines up three arrows while you stand there greyed out.
8. He poses for C.FLASH like a camera flash.
9. Three stone soldiers you freed fly in to block his arrows.

### 3.14 Revisits and VARIETY

- **C.FLASH** lights the black zone for 4 s (and hides the `0` door: it only shines in the dark); its **time stop
  freezes the tide**, so you can stop it at low water and walk into ZONE 100 at leisure.
- **B.ATTACK**'s ice block **floats**: placed in water, it bobs at the surface and rides the tide up and down, a lift
  to 0D's ledge at any tide.
- **Y.SPEAR** wall spears reach 0D's ledge and the tower's high stones.
- **KNIGHT.C** and **SILVER.T** arc over the Reap-bot's back without turning him.
- **Tag partner** (Could): Break Man's shield blocks the Reaplets while jumping; the optional shortcut is a cracked
  pillar in 0F that only his double knockback topples into a bridge.

---

## 4. Yamato Man: EDO NINJA ROW (stage 4)

### 4.1 The pitch

*The Impregnable Fortress* (vanilla's location), with an Edo town at its feet. You start under Mt. Fuji (vanilla's
one-screen vista), cross the town's rooftops **bonking ninjas from below** through the floorboards (Jajamaru), and
break into a **ninja mansion**: singing nightingale floors that bring the spiked ceiling down (slide, and they stay
quiet), hanging scrolls that **spin you through the wall**, a ninja who **steals a travel pass** and runs. Inside the
keep a giant **daruma otoshi** waits to be knocked apart block by block (never touch the head), and the caltrop hall
is crossed on a **spear pogo** (DuckTales). At the **sekisho** checkpoint gate, a traveller carrying **three passes**
(Goemon) may take the back road to the secret kabuki theatre; everyone else goes on to Yamato Man. Vanilla's two
side routes stay: the **charged-punch bypass** to the dark room of GAMARN & GAMADAYU (now lit by fireworks), and the
**Jet ledge** to Beat's **E plate**, now on the castle roof.

| Homage | Here | Mark |
|---|---|---|
| *Jajamaru*: knock enemies from below through the floor | **Bonk-stun** (X-BONK: hit the ceiling under an enemy, it is stunned 90 f) | `[new-code S · Must]` |
| *Goemon*: three travel passes to get through the sekisho | **PASS 0/3** (X-LABEL), the **sekisho** gate (T3) | `[new-code S · Must]` |
| *Goemon* / ninja houses: hidden passages | **Hanging scrolls** that spin (donden-gaeshi), tell = the scroll flutters in a draft | `[new-code S · Must]` |
| Castle lore: the nightingale floor (*uguisubari*), the hanging-ceiling trap | **Nightingale floor** + **Knight's spike ceiling**, re-homed (chain `$11`) | `[new-code M · Should]` |
| Daruma otoshi (the toy) | **The Daruma** mini-boss (T8) | `[new-code M · Should]` |
| *DuckTales*: the pogo cane; treasure found by pogoing a spot | **Spear pogo** (X-EXWP) over caltrops; **pogo the crest** = the hidden room | `[new-code M · Must]` |
| Edo fireworks ("Tamaya!") | **Hanabi** light the dark room | `[new-code S · Should]` |
| Kabuki: the revolving stage, the trapdoor, the shouted names | **The kabuki stage** secret arena | `[new-code S · Should]` |

### 4.2 Map shape

```
00 Fuji street ─> 01 rooftops ─> 02 JUNCTION ──(charged punch)──> 0C kura ─> 0D down ─> 0E DARK ROOM (Gamarn & Gamadayu) ─> 0F E-tank ─up─> 09
                                  │ up
                                  03 floors ─> 04 runner ninja (PASS 1) ─> 05 NIGHTINGALE FLOOR ─> 06 SCROLLS (PASS 2) ─> 07 down ─> 08 shoji
   09 [CP1] ─> 0A courtyard ─> 0B JUNCTION ──(Jet: high ladder)──> 18 sunset roofs ─> 19 KITE RUN ─> 1A castle roof (E plate) ─drop─> 15
                                  │ down
   10 armory ─> 11 DARUMA (PASS 3) [CP2] ─> 12-13 CALTROP HALL (pogo; crest ─trapdoor─> 1E hidden room) ─> 14 SEKISHO
          ├─ main gate ─> 15 shutter ─> 16 BOSS
          └─ back road (3 passes) ─> 1B backstage ─> 1C hanamichi shutter ─> 1D KABUKI STAGE (secret)
```

Screens used: main 00-16 (23, including the bypass 0C-0F), E route 18-1A (3), secret 1B-1D (3), hidden room 1E (1)
= **30 of 32**. Spare: 17, 1F. Vanilla used 30 (`stages_b.md` §2).

### 4.3 Screen by screen

| Scr | What the player does | Enemies and objects | Hazards and set pieces | Notes |
|---|---|---|---|---|
| **00** | Match card. **Mt. Fuji** over the castle-town skyline; an Edo street of shopfronts. A notice board: the **WANTED** poster (`MR. Y - 1,000,000 RYO`) and a sign: `SEKISHO AHEAD. THE BACK ROAD IS OPEN TO TRAVELLERS WITH 3 PASSES` | lantern robot `$C2` x1 [3] | | vanilla v00 vista (CHR `$97`; its Fuji third is only valid here, `stages_b.md` §6). YAM-01, YAM-02 |
| **01** | Rooftop run. **Jaja-nin** ninjas stand on the thin roof floors above you: jump into the floor tile under one and it is **stunned 90 f** (Jajamaru); stunned ninjas take double damage | Jaja-nin x2, lantern `$C2` x1 [5] | | X-BONK. YAM-03 |
| **02** | **JUNCTION** (vanilla): ladder up to 03 (main), or a **Power block** in the right wall (charged punch) → the bypass 0C | Jaja-nin x1 [3] | | vanilla breakable ids `$38-$3B` kept. Tell: the venue's standard cracked Power-block art |
| **03** | Up through the mansion's floors: three thin wooden floors with gaps, ninjas on each; bonk your way up | Jaja-nin x3 [5] | | up exit (ladder at top), CHR `$98` (vanilla interior) |
| **04** | **The runner ninja**: a ninja holding a paper (**PASS #1**) runs right at 1.5 px/f, hopping gaps; he leaves the screen after about 6 s. Shoot him (3 hits) or bonk-stun him and he drops the pass. The PASS counter appears | runner, samurai `$A2` x1 [4] | | YAM-04, YAM-05. A missed runner is back on the next visit |
| **05** | **THE NIGHTINGALE FLOOR.** Gold floorboards **chirp** when you walk or land on them (not when you slide); each chirp lowers the **spiked ceiling** 8 px (Knight's chain `$11` handler, §4.5.1); quiet, it rises 1 px every 4 f. The ceiling starts 112 px up: walk the whole floor and it is down to about 32 px, too low to jump the samurai's spears at the far end. **Slide and it never moves** | samurai `$A2` x1 [3] | ceiling spikes (deadly) | YAM-06, YAM-07. Jet hovering is silent too; Power walks and pays for it |
| **06** | **THE SCROLL ROOM.** Three hanging scrolls. Two **flutter** (a draft behind them): UP in front of one and the wall **spins** (donden-gaeshi, 24 f) and puts you on its other side. Scroll A hides a closet with **PASS #2**; scroll B is a shortcut down to 08. The still scroll: K: "It's just a scroll." | hopping shuriken robot `$69` x2 [4] | | YAM-08, YAM-09 |
| **07** | Down through a shoji shaft: shuriken robots, a bubble cluster | `$69` x2, `$25` x1 [4] | | down exit |
| **08** | **Paper walls**: shoji panels (collision `$D` → `$19` in group 2) hide two pockets that **F.BLAST burns open** on a revisit (a 1-up, bolts) | samurai `$A2` x1 [3] | | `[engine-ok]` |
| **09** | **CHECKPOINT 1** (vanilla set it on v09 for v0A). The bypass rejoins here from 0F | | | Checkpoint 1 (09) |
| **0A** | The castle courtyard: lanterns, and a **kite ninja** (rides a kite across the sky, drops bombs) | kite ninja x1, lantern `$C2` x1 [4] | | introduces kites |
| **0B** | **JUNCTION** (vanilla): ladder **down** to 10 (main), or the **high ladder** in the top right, above a ledge 64 px over the floor: **Jet only** → 18 (E route). A kite with an "E" painted on it flies above the ledge | kite (scenery) [2] | | vanilla gate geometry kept exactly (so vanilla's measured result holds: only the Jet reaches it). Tell: the E kite |
| **0C** | *Bypass.* The storehouse (kura): rice bales, a samurai | samurai `$A2` x1 [2] | | CHR `$99` (vanilla dark bypass) |
| **0D** | *Bypass.* Down into the cellar | | | sprite set `$61` for the mid-boss (vanilla) |
| **0E** | *Bypass.* **THE DARK ROOM: GAMARN & GAMADAYU** (vanilla mid-boss: the frog mech and its ninja rider, 14 + 15 HP). **Twist: hanabi.** The room is dark (vanilla palette `$B9`); every 180 f Gamadayu lights a firework (fuse hiss 30 f, a spark climbs), it bursts at the top and **the room lights up for 24 f**, showing the floor and its two pits | Gamarn, Gamadayu, low shot `$D8` [5] | 2 pits in the dark | YAM-15 ("Tamaya!"). The reduced-flash option shortens the light to 8 f and dims it. C.FLASH lights the room for 4 s on a revisit |
| **0F** | *Bypass.* The E-tank pocket behind a second Power block (vanilla ids `$3C-$3F`); up exit to 09 | | | vanilla |
| **10** | Down into the keep's armory: eye cannons, spring flowers | eye cannon `$54` x2, spring `$5F` x1 [5] | | vanilla v10-v11 enemies |
| **11** | **THE DARUMA** (§4.5.3, mini-boss, locks the screen). **CHECKPOINT 2** after it. **PASS #3** lies under it and drops when it is beaten | Daruma (6 parts) [7] | | T8. YAM-10-12 |
| **12** | **THE CALTROP HALL**: a floor of caltrops (spikes, `$F`). A **pogo spear** stands in a rack at the entrance: touch it and it replaces the buster (X-EXWP). Hold DOWN in the air: pogo; bounce on caltrops and on enemies (3 dmg). One floor cell bears a **gold crest** (§4.6.2) | propeller lanterns `$24`/`$26` x2, Jaja-nin x1 [5] | caltrops (deadly without the pogo) | YAM-13 |
| **13** | Caltrop hall 2: pogo across ashigaru heads and up three bell towers (ringing a bell with the pogo bounces you 72 px). A rack at the end takes the pogo back | ashigaru x2, bells x3 [6] | | the pogo can't leave 12-13 |
| **14** | **THE SEKISHO.** A barrier gate and a guard-bot. The main gate opens for everyone (→ 15). With **3 passes**, the guard bows and opens the side gate: **the back road** (→ 1B) | sekisho guard [2] | | T3 + counter. YAM-14 |
| **15** | Shutter corridor. **Boss checkpoint.** The E route drops in here | | | shutter checkpoint (`$0684` = 15) |
| **16** | **Boss room** (§4.8) | Yamato Man | | |
| **18** | *E route.* Edo rooftops at sunset: vanilla's pink sunset windows (v1A-v1D art and its animated CHR sets `$9A-$9C`) | Jaja-nin x2, beetle `$75` x1 [5] | | |
| **19** | *E route.* **THE KITE RUN**: ride kites (moving platforms that bob on a sine) over the town; kite ninjas drop bombs; land on roofs to let the Jet's fuel regrow | kites x3, kite ninja x2 [7] | pits | |
| **1A** | *E route.* The castle roof: a golden **shachihoko** (the carp ornament) holds **Beat's E plate** (§4.6.4). A hatch drops you into 15 | E plate [2] | | YAM-20 |
| **1B** | *Secret.* **Backstage** at the kabuki theatre: prop flats as platforms, kuroko stagehands moving scenery (harmless; they carry platforms) | kuroko x2, ashigaru x2 [5] | | |
| **1C** | *Secret.* The **hanamichi** (the runway through the audience): shutter corridor, checkpoint | | | |
| **1D** | **SECRET ARENA: THE KABUKI STAGE** (§4.9) | Yamato Man | | |
| **1E** | **Hidden room: the treasure vault** (§4.6.2) | | | |

### 4.4 Checkpoints

| # | Screen | Set by | CHR / palette |
|---|---|---|---|
| CP1 | 09 | camera on 09 (vanilla script `$2F`, moved one screen) | `$97`+`$98` / `$5B` |
| CP2 | 11 | the Daruma's death | keep palette |
| *(CASUAL)* | 05 | camera on 05 (before the nightingale floor) | `$98` |
| *(CASUAL)* | 0E | camera on 0E (the dark room) | `$99` / `$B9` |
| Shutter | 15 (main and E route), 1C (secret) | shutter entry | |

Passes, like items, are cleared from the object list once taken (the vanilla kill bitfield `$0650`), so a death keeps
them; leaving the venue resets them (the sekisho wants three in one visit, as Goemon's checkpoints do).

### 4.5 The three set pieces that carry the venue

#### 4.5.1 The nightingale floor (05) `[new-code M · Should]`

- **Floor:** a new X-FLOOR type in Yamato's collision group (group 2), the gold boards. Every 24 px walked, and every
  landing, plays a chirp and posts a "chirp" event. A slide (2.5 px/f) never chirps; nor does the Jet in flight.
- **Ceiling:** Knight's descending spike ceiling (IRQ chain `$11`, handler `$3E:$C337`, logic inside the IRQ; the
  collision offset through `$069C`, `$3E:$DA40`). Vanilla lowers it steadily; here **each chirp lowers it 8 px** (over
  8 f) and silence raises it 1 px every 4 f. It needs the stage-6 checks generalised (the stage-attribute table).
- **The lesson:** slide = quiet. Normal Rockman can cross it untouched; Power Rockman can't slide and must hurry;
  Jet Rockman hovers. The fallback if the chain can't be re-homed: the ceiling is a row of sprite spike blocks that
  drop on chirps `[new-code S]`.

#### 4.5.2 The pogo (12-13) `[new-code M · Must]`

- An **X-EXWP**: touching the rack's pogo spear replaces the buster until the rack at 13's end (4MI's Quint pogo,
  `r4mi/stages_a.md` §3). B does nothing while you carry it (no shots: you must bounce your way through).
- **Hold DOWN in the air** to pogo: landing on caltrops, enemies or bells **bounces** you (51 px; hold A for 72 px).
  Landing on an enemy does 3 damage. Without DOWN held, caltrops are deadly as usual.
- After beating Yamato Man, **Y.SPEAR's Power synergy is the same pogo**, everywhere (proposal, §0.5): the venue
  teaches it before you own it.

#### 4.5.3 The Daruma (11) `[new-code M · Should]` (T8)

- **Body:** a stack standing on the floor: **five coloured blocks** (32x16 each) and the **head** on top (32x32, a
  daruma face with one eye painted). The head wobbles side to side and every 120 f spits a **fortune slip** that flutters down (tell: its
  cheeks puff 20 f): `大凶` / `VERY BAD LUCK`, 3 dmg.
- **Daruma otoshi:** a hit on a block's side **knocks that block out**: it slides across the floor at 3 px/f, bounces
  off the wall once and vanishes (3 dmg on contact: jump it). The stack drops 16 px.
- **The head:** a hit on the head makes it **angry** (red): it hops off the stack and bounces around the room for
  180 f (contact 4), then hops back on.
- **The rule that makes it a game:** Rockman's buster shot spawns 1 px above his centre Y, about 12 px above his feet
  (measured, `build/design/design-venues-b/measure.py`), which is inside the *bottom* block (0-16 px). **Shoot from
  the floor** and you always hit the lowest block; the stack comes down to meet your shots. **Jump-shoot** and you hit
  higher, and eventually the head. The fortune slips are what tempt you to jump.
- **End:** when the last block is out, the head lands on the floor and the fight is won; PASS #3 slides out from
  under it.
- **DARUMA chip** (§4.6.3): won without ever hitting the head.

### 4.6 Secrets

#### 4.6.1 Secret exit: the sekisho back road `[new-code S · Must]`

- **Gate:** reach the sekisho (14) carrying **three passes**: #1 from the runner ninja (04), #2 behind the fluttering
  scroll A (06), #3 under the Daruma (11). All three are on adaptor-free paths.
- **Tell:** the sign on 00 says so in plain words; the **PASS n/3** label (X-LABEL) appears as soon as a pass is on
  screen and stays up; the runner visibly carries his pass; Kalinka calls out each pass (YAM-05); the sekisho guard
  points at the side gate and shakes his head if you have fewer than three.
- **Effect:** the back road → 1B backstage → 1C hanamichi → the kabuki stage 1D. Beating Yamato Man there clears the
  venue and sets the secret flag.

#### 4.6.2 Hidden room: the treasure vault (1E) `[new-code S · Must]`

- **Gate:** in the caltrop hall (12), **pogo-land on the gold crest** (a single floor cell among the caltrops). The
  cell is a trapdoor (T6 bit): it opens and you drop into 1E (DuckTales: treasure found by pogoing the right spot).
- **Tell:** the crest glints every 2 s, the only shiny cell in a floor of caltrops, right where the pogo makes you
  look down. The debrief hint names it outright.
- **Contents:** a vault of gold koban: an E-tank, a 1-up, a 100-bolt chest, and a sign: `THIS GOLD IS A LOAN FROM
  THE TOURNAMENT. MR. Y.` (it isn't).
- **Return:** a ladder up into 12, with the pogo still in hand.

#### 4.6.3 Behaviour-gated chip: DARUMA `[new-code S · Should]`

- **Gate:** win the daruma otoshi (11) **without ever hitting the head**.
- **Tell:** Kalinka says the rule as the fight starts (YAM-10: "Knock out the blocks and never hit the head!"); the
  head has only one eye painted; YAM-11 when you hit it.
- **Award:** the head lands on the floor and **paints its second eye** (a daruma's wish fulfilled; a brush stroke and a
  chime), then the chip appears beside PASS #3.
- **Proposed effect:** DARUMA (*nana korobi ya oki*, "fall seven times, stand up eight"): once per stage, a hit that
  would kill you at 2 HP or more leaves you at 1 HP (4MI's SKULL AMULET idea, earned the Edo way).

#### 4.6.4 Plate E: the castle roof `[engine-ok geometry + new-code S · Must]`

- **Gate:** vanilla's: the high ladder on 0B, above a ledge 64 px over the floor, needs the **Jet** (the Go-Explore
  test never reached it in normal form, `stages_b.md` §6).
- **Change from vanilla:** the plate is a **pickup** on the shachihoko (1A), not a kill in a second boss room, and the
  route **rejoins** at 15. The vanilla YOU GET line `Y.SPEAR AND BEAT E-PARTS` (`$68`) plays at the boss kill if the
  plate was taken this visit.
- **Tell:** the kite with the painted "E" over 0B's ledge; from 0A the shachihoko gleams on the castle roof in the
  backdrop.

### 4.7 Enemies and objects

| Object | Kind | HP (buster hits) | Behaviour | Mark |
|---|---|---|---|---|
| Lantern robot `$C2`, samurai `$A2`/`$A3`, shuriken robot `$69`/`$6B`, bubbles `$25`, eye cannon `$54`, springs `$5F`, propeller lanterns `$24`/`$26`, beetle `$75`, GAMARN & GAMADAYU `$D0-$D8` | vanilla | as vanilla | as vanilla | `[engine-ok]` |
| **Jaja-nin** (ninja-bot) | new | 2 | hops between floors, throws a shuriken every 90 f (tell: crouch 12 f); bonk-stun 90 f, stunned = double damage | `[new-code S · Must]` |
| **Runner ninja** | new | 3 | carries PASS #1, runs and hops at 1.5 px/f, leaves after ~6 s | `[new-code S · Must]` |
| **Hanging scroll** | new (T3) | - | flutters (2-frame BG animation) if it hides a passage; UP: 24-f spin, teleport through the wall | `[new-code S · Must]` |
| **Daruma** | new (T8) | blocks 1 hit each; head immune | §4.5.3 | `[new-code M · Should]` |
| **Pogo rack / pogo** | new (X-EXWP) | - | §4.5.2; needs pogo frames for the player sprite | `[new-code M · Must]` `[new-art S]` |
| **Ashigaru** | new | 2 | march at 1 px/f with a short spear poke; also the boss's helpers | `[new-code S · Must]` |
| **Bell** | new | - | pogo target: bounces 72 px | `[new-code S · Should]` |
| **Kite / kite ninja** | new | kite - / ninja 2 | kites: platforms on a sine (cloud code, kite art); the ninja drops a bomb every 120 f; SILVER.T cuts the string | `[new-code S · Should]` |
| **Pass**, **sekisho + guard** | new (T3) | - | §4.6.1 | `[new-code S · Must]` |
| **Hanabi** | new | - | Gamadayu's firework: lights the room 24 f | `[new-code S · Should]` |
| **Kuroko** | new | - | stagehands; harmless; carry platforms (1B) and props (1D) | `[new-code S · Could]` |

### 4.8 Boss: Yamato Man, "the impregnable" (16)

**Arena:** a castle hall: tatami floor, two short ledges at the sides (48 px up), wooden walls (Y.SPEAR's alternate
sticks in wood).

**Intro (90 f):** he bows in full armour; the panel's `MOBILE 31` blinks. Kalinka: "He isn't going anywhere."

**Pattern loop (HP 28 to 15):** RUSH → VAULT → RUSH → WALL SPEARS, about 560 f per loop.

| Move | Tell | Action | Frames | Counter |
|---|---|---|---|---|
| **SPEAR RUSH** (vanilla) | stamps a foot, "Ei!", 16 f | runs across the room (x `$21-$DE`) at 3 px/f, spear lowered (tip 16 px ahead, 4 dmg), stops at the wall 16 f | 16 + 64 + 16 | jump over; a charged punch **clashes** with the spear: both knocked back 16 px, he is stunned 20 f |
| **VAULT & RAIN** (vanilla) | plants the spear, 12 f | **pole-vaults** to y `$38` and at the top throws a **3-way spread** of spearheads down (vanilla `$B4`, 2.5 px/f); lands, 24 f | 12 + 40 + 24 | stand between the heads; this is the Y.SPEAR tap, and the vault is the **pogo**, both shown |
| **WALL SPEARS** | draws two spears, 16 f | throws them into the left and right walls (heights 48 and 80 px; they stay 240 f as **one-way platforms**), then GROUND THRUST: spear raised overhead 20 f, slams: two shockwaves (16 px tall, 3 px/f) run along the floor both ways | 16 + 20 + 20 + 60 | **stand on his spears** (the Y.SPEAR alternate, shown), or jump the waves |

**Ashigaru:** at HP 18 and HP 9 he whistles (20 f) and two ashigaru-bots march in from the shutter side (2 hits each).

**Pinch (HP ≤ 14, half his bar): HELMET OFF.** His kabuto pops off and **bounces around the room** for 180 f (16x16,
2 px/f, off the walls, 3 dmg), showing a topknot. From now on RUSH runs at 4 px/f, VAULT throws 5 heads, and his panel
stat flips: `MOBILE 99` (YAM-18).

**Proposed row:** SILVER.T **4 / 8** (weakness); KNIGHT.C, W.STORM, B.ATTACK, F.BLAST, PLANT.B, C.FLASH 2 / 30;
buster 1 / 60; charged buster 3 / 60; punch 2 / 40; charged punch 3 / 40 + CLASH.

**Weakness reaction, SNAP:** a SILVER.T hit chops his spear shaft in two: he stares at the stub for 40 f (no attacks,
WEAK! pop, YAM-16), then pulls a new spear from his back.

**Self-weapon reaction, PARRY:** the first Y.SPEAR does 0: he catches your spear and throws it back at you (2 dmg if it
hits). YAM-17: "A samurai never drops his spear. He throws yours back."

### 4.9 Secret arena: THE KABUKI STAGE (1D) `[new-code S · Should]`

A kabuki theatre with the striped curtain (black, persimmon, green) and the audience below. Yamato Man **rises
through the trapdoor** (*seri*) and strikes a *mie* pose to the clack of wooden clappers; the audience shouts
`YAMATO-YA!` (a pop-up). The twist is the **revolving stage** (*mawari-butai*): every 600 f, the clappers sound
(30-f tell), the curtain sweeps across (a 30-f palette wipe) and **the set changes** by toggling the alternate
metatile set (the `$0340` bits of the set's metatile ids: free, it is vanilla's breakable mechanism):

- **Set A, the castle hall:** flat, two ledges (the main arena's shape).
- **Set B, the moat bridge:** two side platforms and the open trapdoor in the middle (48 px, a pit).

Kuroko stagehands wheel props across during each change (harmless; if you shoot one, the audience boos). In pinch he
pauses for a second *mie*, and the audience goes wild. Everything else is the main fight.

### 4.10 Tileset slot

- **Kept vanilla CHR:** `$97` (the Fuji vista for screen 00, red riveted castle walls, green panels, pipes, shoji,
  purple pillars), `$98` (interiors), `$99` (the dark bypass), the sunset windows of the plate route with their
  animated sets `$9A-$9C`, sprite set `$61` (GAMARN & GAMADAYU). Palettes `$57-$5E`, `$B9`.
- **New BG tiles** (about 100) `[new-art M · Must]`: Edo shopfronts with noren curtains, kawara roof tiles, the notice
  board and WANTED poster, tatami, three hanging-scroll designs, the gold nightingale boards, the caltrop floor and gold
  crest, the sekisho gate, the kabuki curtain, the audience and the set flats, the treasure vault, the shachihoko.
- **New sprites** (about 120 tiles): Jaja-nin (hop, throw, stunned), the runner and his pass, kite and kite ninja,
  scroll spin frames, the Daruma (five coloured blocks, head with one and two eyes, angry head, fortune slip), the pogo
  rack, **the player's pogo frames** (2), ashigaru, bells, the sekisho guard, kuroko, hanabi spark and burst, Yamato
  Man's flying kabuto and topknot frames.
- **Collision:** group 2 as vanilla (`$D` → `$19` for the shoji, `$B` Power blocks), plus the nightingale type and the
  trapdoor cell (T6).

### 4.11 HARD pokes

| Section | Poke | Kind |
|---|---|---|
| Rooftops 01, 03 | Jaja-nin throw every 60 f; stun 90 → 60 f | param |
| Runner 04 | he escapes after ~4 s | param |
| Nightingale 05 | 12 px per chirp; the ceiling rises 1 px every 8 f | param |
| Scrolls 06 | a third fluttering scroll is a decoy that spins you back to the room's entrance | object list |
| Dark room 0E | hanabi every 240 f; light 16 f | AI param |
| Daruma 11 | six blocks; fortune slips every 80 f | AI param |
| Caltrop hall 12-13 | one more caltrop row in 13; bells bounce 60 px | layout poke + param |
| Kite run 19 | kites move 1.5x faster | param |
| Boss | pinch at HP ≤ 18; three ashigaru per whistle; pinch RUSH 5 px/f | AI branch |

### 4.12 Commentator hooks

| Id | Trigger | Draft |
|---|---|---|
| YAM-01 | match card ends | K: "Yamato Man! DEFENCE 185!" C: "And MOBILE 31. He isn't going anywhere." |
| YAM-02 | WANTED poster on screen | K: "'Mr. Y. Wanted. A million ryo.'" C: "Cheap. Wily's worth at least two." |
| YAM-03 | first bonk-stun | C: "Knock them from below! Ninja manners." |
| YAM-04 | the runner appears | K: "That ninja stole a travel pass!" |
| YAM-05 | a pass taken | K: "PASS 1 of 3! The sekisho wants three." (2 of 3 / 3 of 3: "The back road's open!") |
| YAM-06 | first chirp | K: "Shh! The floor sings when you walk!" C: "Slide, lad. Quietly." |
| YAM-07 | the ceiling drops 32 px | C: "Edo architecture: beautiful and lethal." |
| YAM-08 | first scroll spin | K: "The wall turned around!" |
| YAM-09 | UP at a still scroll | K: "It's just a scroll." |
| YAM-10 | Daruma fight starts | K: "Daruma otoshi! Knock out the blocks, and never hit the head!" |
| YAM-11 | the head is hit | C: "You hit the head. The daruma is NOT amused." |
| YAM-12 | perfect Daruma | K: "It painted its other eye! Wish granted!" |
| YAM-13 | pogo taken | K: "A pogo stick... with a spear on it?" C: "In my day we called that a Sakugarne." |
| YAM-14 | sekisho, 3 passes | C: "Three passes. The back road is yours." |
| YAM-15 | dark room / first hanabi | K: "Who turned off the lights?!" / K: "Tamaya~!" |
| YAM-16 | first SILVER.T hit | K: "He chopped the spear in half!" |
| YAM-17 | Y.SPEAR on Yamato Man | C: "A samurai never drops his spear. He throws yours back." |
| YAM-18 | pinch | K: "His helmet flew off!" C: "His MOBILE just went from 31 to 99!" |
| YAM-19 | kabuki entrance / mie | (audience) `YAMATO-YA!` |
| YAM-20 | E plate taken | K: "Beat's E-parts! On a golden fish!" |

**Death lines:** 1. K: "Shuriken! Duck!" C: "He did not duck." 2. C: "The floors sang at your funeral, Rockman."
3. K: "The ceiling came down!" C: "Beautiful *and* lethal." 4. C: "Defence 185, Mobile 31, and still faster than
you." 5. K: "Fall down seven times, stand up eight!"

### 4.13 Judges' debrief hints

1. Secret exit: "The sekisho opens its back road for travellers with three passes. One runs, one hides behind a
   scroll, one sits under a daruma."
2. Hidden room: "Edo's gold is under the floor. Bounce your pogo on the crest in the caltrop hall."
3. DARUMA: "Daruma otoshi: knock out every block, never touch the head, and the daruma will paint its other eye."
4. Plate E: "Beat's E-plate shines on the castle roof. The ladder over the courtyard ledge needs a Jet."

### 4.14 How crazy it gets

1. Rockman knocks ninjas silly from below, through the floorboards.
2. A ninja steals a travel pass and runs off with it.
3. The floor chirps, the spiked ceiling comes down, and the answer is to slide.
4. Walls that spin you round behind a hanging scroll.
5. A giant daruma otoshi you win by never touching the head, and it paints its own eye.
6. Rockman on a spear pogo, bouncing over caltrops and ringing bells.
7. Fireworks light up a dark room with a frog mech in it. "Tamaya!"
8. Yamato Man's helmet flies off and his MOBILE stat jumps to 99.
9. A kabuki stage revolves mid-fight while the audience shouts his name.
10. Mr. Y's WANTED poster: a million ryo.

### 4.15 Revisits and VARIETY

- **F.BLAST** burns the shoji pockets on 08 (`$D`, vanilla type).
- **C.FLASH** lights the dark room for 4 s; its time stop freezes the runner ninja.
- **SILVER.T** cuts kite strings (the kite ninjas fall) and is the weakness.
- **Y.SPEAR's pogo synergy** (Power) crosses the caltrop hall without the rack, and also opens the crest.
- **W.STORM** blows the Daruma's fortune slips away.
- **Tag partner** (Could): Break Man's shield blocks the shuriken rain on 07 while he jumps; the optional shortcut is
  a samurai on 0A's wall that only his double knockback dislodges, opening a ledge with bolts.

---

## 5. Across the four venues

### 5.1 Budgets

| | Blizzard | Flame | Centaur | Yamato | Total |
|---|---|---|---|---|---|
| Screens used / 32 | 28 | 28 | 30 | 30 | |
| Main route (incl. boss) | 00-16 | 00-16 | 00-17 | 00-16 (with bypass 0C-0F) | |
| Secret route + arena | 17-1A | 17-1A | 1A-1C | 1B-1D | |
| Hidden room | 1E | 1C | 1D | 1E | |
| Plate route | - | - | 18-19 (T, Jet) | 18-1A (E, Jet) | |
| New object kinds (as X-GPOBJ sub-ids) | ~10 | ~12 | ~10 | ~14 | **~46** |
| New BG tiles | ~70 | ~90 | ~80 | ~100 | ~340 |
| New sprite tiles | ~110 | ~100 | ~90 | ~120 | ~420 |
| Vanilla raster set piece | ship (chain 1) | none (palette cycle) | tide (chain `$14`) | spike ceiling (chain `$11`, re-homed) | |
| Peak objects on a screen (player in, shots out) | 8 (screen 10) | 8 (screen 0B) | 8 on alarm (screen 12) | 7 (screens 11, 19) | target ≤ 8 |

All four stay at or under 8 at their peak, which leaves room for the player's shots under vanilla's ~10. Flame 0B
(three guards and three chandeliers) and Centaur 11-12 (Reaplet alarms) are the screens to profile first.

### 5.2 Tiers at a glance

| Tier | Blizzard | Flame | Centaur | Yamato |
|---|---|---|---|---|
| **Must** | route; bonk + T6 + Toppy + wrap; ship icicles; condor secret exit; hidden room; boss rework; cloud summit arena | route; T3 plates/gates; loose tiles; spikes; chompers; guards; chandeliers; Shadow Rock merge; boss rework | route; zone doors; tide dwell + ZONE 100; ZONE 0; T plate pickup; tower wrap; boss rework | route; bonk-stun; passes + sekisho; scrolls; pogo EXWP; crest room; E plate pickup; boss rework |
| **Should** | X-UPEXIT (else ladder stubs); ski run; SNOW CHAINS; bonus jingle | skeleton; mouse room; FIREPROOF; throne-room shadow; vizier | ZONE labels; Reap-bot; Nasubi Mage; hot spring; CENTURION; sunken throne | nightingale floor + ceiling; Daruma; DARUMA chip; hanabi; kabuki stage; kites |
| **Could** | Shirokuma; tag shortcut | Roll cameo; palace music variant; tag shortcut | eggplant curse; underwater music; tag shortcut | kuroko; tag shortcut |

If a Should slips, each venue still has its homage as a mechanic (CX lesson 2): Ice Climber's bonk-and-patch, Prince
of Persia's plates and shadow, Atlantis's doors and Kid Icarus's wrap tower, and Jajamaru's bonk, Goemon's passes and
DuckTales' pogo.

### 5.3 Dependencies on other docs

| Doc | What this doc needs or proposes |
|---|---|
| `systems.md` | The weapon proposals of §0.5 (B.ATTACK ice block + Jet bombs; F.BLAST upward column + Burning Knuckle, oil ignition; C.FLASH time stop + lights dark rooms; Y.SPEAR wall spears + the Power pogo). The four boss rows (damage / i-frames). The **self-weapon reactions** as visible special cases (CX lesson 7). The "charged shot frees Centurions" and "charged shot knocks back skeletons" rules. Whether the vanilla weakness cycle stays (my rows assume it does) |
| `meta.md` | Four behaviour-gated chips and their effects: **SNOW CHAINS**, **FIREPROOF**, **CENTURION**, **DARUMA**. Four secret-exit save flags. **Plates as pickups** (E, T) instead of second boss rooms. Bolt values for vegetables and treasure bags. The debrief predicate order (§1.12, 2.12, 3.12, 4.13). STYLE credit for self-weapon reactions and the perfect Daruma. Venue replays (the SMW model: a cleared venue can be replayed for its other exit). Par times (proposal: Blizzard 330 s including the 40-s bonus, Flame 300 s, Centaur 300 s, Yamato 330 s) |
| `story.md` | ~70 commentator lines (ids BLZ-, FLM-, CEN-, YAM-), 20 death lines, 13 debrief hints, the boss intros' gags, all in JP (kana) and EN. The Mr. Y gag per venue. Roll's optional cameo line |
| `tech.md` | T3, T6, T7, T8; X-BONK, X-WRAP, X-UPEXIT, X-METER, X-LABEL, X-EXWP, X-FLOOR, X-GPOBJ (§0.4); the stage-attribute table (ship, tide and ceiling in any stage); **one 8 KB tileset bank per venue**; the tide dwell (the tide's logic runs inside IRQ handler `$C3D8`); an ignition hook on `$3E:$DDFC` (FIREPROOF); the ship thread's turn event (icicles); a palette-only "black zone"; the reduced-flash option honoured by hanabi, C.FLASH and the merge flash |

### 5.4 Music and sound

- **Kept:** each venue keeps its vanilla stage theme (`$01` Blizzard, `$03` Flame, `$05` Centaur, `$02` Yamato) and the
  boss theme.
- **New** (original compositions only, no quotations):
  - Blizzard: the 40-s **bonus jingle** `[new-music S · Should]`.
  - Yamato: the **kabuki arena** theme (clapper hits on the noise channel, a shamisen-like pulse) `[new-music M · Should]`.
  - Centaur: an **underwater variant** for ZONE 100 and the Sunken Throne `[new-music M · Could]`.
  - Flame: a darker **palace variant** for 04-0E `[new-music M · Could]`.
- **SFX** `[new-music S · Must]`: bonk, ice-cell break, Toppy push, condor cry, chomper "shing", gate rumble, plate
  click, mouse squeak, door fade, door bonk, siren, slot reel, chirp, scroll spin, pogo "boing", wooden clappers,
  hanabi fuse and burst, daruma chime.

### 5.5 Scorecard notes (proposals for `meta.md`)

- **VARIETY** (25): each venue has at least five weapons with a job (§1.14, 2.14, 3.14, 4.15), so variety is earned by
  using the tools the venue asks for, not by grinding.
- **SECRETS** (20): secret exit, hidden room and (Centaur, Yamato) the plate. The behaviour chips are their own reward.
- **STYLE** (15): weakness kill, no E-tank, and one "crowd-pleaser" moment per venue: the self-weapon reaction, or the
  perfect Daruma in Yamato.

---

## 6. Lessons applied

**Rockman CX** (`cx/SUMMARY.md` §6):

- **1. One premise everywhere:** every venue is a match with a card, judges, commentators, prize money (vegetables,
  treasure bags) and a Mr. Y gag.
- **2. Homage as a mechanic:** Ice Climber's bonk and the seal that patches holes; PoP's plates, loose floors and the
  shadow you must not fight; Atlantis's lying doors and deep warps; Kid Icarus's wrap tower, Reaper and eggplant;
  Jajamaru's floor bonk, Goemon's passes, DuckTales' pogo. The bosses' jokes are mechanics too (the snowman, the
  scimitar duel, the slot machine, the flying helmet).
- **3. Voice on failure:** a rotating death table per venue plus event hooks.
- **5. Reuse set pieces with one twist each:** the ship shakes icicles loose; the oil becomes a permanent choice; the
  tide becomes a lift and a lock; Knight's ceiling listens to the floor; the dark room gets fireworks; vanilla's
  breakable mechanism (`$0340`) becomes the kabuki stage's scene change.
- **6. Telegraph required tools:** every gate in §0.3 has a named tell, signs say the rules (the Atlantis tablet, the
  sekisho sign, the summit sign), and the mouse, the Centurions and the crest all announce themselves.
- **7. Special cases in visible code:** the self-weapon reactions are explicit branches, not table values.

**Rockman 4 Minus Infinity** (`r4mi/SUMMARY.md` §6 and the stage docs):

- **1. Weakness in the i-frames:** every boss row is damage / i-frames, weakness 4 / 8.
- **3. A moral trade-off:** SNOW CHAINS (the seals cost you time) and FIREPROOF (the chandeliers are the easy way).
- **4. Friends as mechanics:** the Centurions block arrows; Toppies refill the secret arena's floor if you spared them;
  Beat's plates are rewards for the Jet.
- **5. Behaviour-gated secrets with a hint after the fact:** four chips, 13 debrief hints, all written.
- **7. Theme into mechanics:** a fire marshal, a nightingale floor, a revolving stage, a tide you read like a clock,
  a summit bonus round.
- **8. Map edits by bosses:** Blizzard's snowball breaks the secret arena's floor; the kabuki stage swaps sets.
- **Pharaoh's curse words** → the ZONE labels; **Quint's pogo** (EXWP) → the spear pogo; **Toad's hidden-room link**
  → the one-screen detours that return you; **Dust's TEMP gauge** → the bonus timer and the PASS counter in the
  boss-bar slot; **Toad/Bright reacting to their own weapons** → the self-weapon reactions; **HARD as small data
  pokes** → §1.10, 2.10, 3.10, 4.11.

**Vanilla Rockman 6** (`rm6/SUMMARY.md` §7):

- **2. A tileset slot per venue,** vanilla CHR kept and extended; set pieces as sprites where possible (floes, gates,
  chandeliers, kites).
- **5. New enemies through free type ids** → X-GPOBJ, because ~46 new kinds don't fit the 30 free ids.
- **6. Breakables are per metatile id:** used deliberately (one oil id per gallery pool; the kabuki set swap) and
  replaced by per-position flags (T6) where Ice Climber needs single cells.
- **7. Adaptors by win count:** no secret exit needs an adaptor; the plates keep vanilla's Jet geometry exactly; the
  bypass keeps vanilla's charged-punch blocks.
- **8. Quirks kept on purpose:** igniting oil, slippery ice, the Jet-only gaps, C.FLRSH (now a commentator joke), the
  vanilla boss-panel stats.

---

## 7. Risks

1. **Object ids.** About 46 new object kinds in these four venues alone against 30-32 free type ids for the whole
   game. Without X-GPOBJ (a generic type plus sub-id and a code bank per sub-id, 4MI's `$5E`) the venues cannot ship.
   This is the first thing to build.
2. **T6 in hot code.** Per-position tiles add a lookup to the painters and to the collision read, and collision is
   already about 20% of the frame (`engine.md` §8). Mitigation: a per-screen "has T6 cells" flag so ordinary screens
   skip the lookup.
3. **IRQ-resident logic.** The tide (handler `$C3D8`) and the spike ceiling (`$C337`) run game logic inside the IRQ.
   The tide dwell (Centaur) and the chirp-driven ceiling (Yamato) change that logic. Do them after the MMC5 port's
   generic raster list moves the logic into an effect thread (BRIEF §7.1); fallbacks are given in §3.4 and §4.5.1.
4. **X-UPEXIT is a Could in the BRIEF.** Without it, Blizzard's climb and Centaur's tower use ladder stubs at each screen
   top: playable, but less Ice Climber. I argue it up to Should here.
5. **Lag** on Flame 0B (the gallery) and Centaur 11-12 (Reaplet alarms): both are capped in the tables, but must be
   profiled with shadow6.
6. **Screen budgets** are 28-30 of 32. Yamato and Centaur have two spare screens each, so a HARD-only room or a design
   change there has to replace something.
7. **Fairness of the behaviour gates.** FIREPROOF can be lost on screen 01 by a first-time player; that is intended
   (a replay goal), but the lesson there must be generous (120-f hover). SNOW CHAINS punishes the charged shot, the
   natural tool, so its tell (BLZ-07) must fire on the first destroyed Toppy every visit.
8. **Tedium in the climb.** Toppy refills can make the climb slow. CASUAL raises the refill delay to 600 f, and the
   climb has a checkpoint halfway (0B).
9. **Flashes.** Hanabi, C.FLASH, the merge flash and the black zone's glow must honour the "reduced flashes" option
   (BRIEF §5.7).
10. **Player art.** The pogo frames (Yamato) and the eggplant (Centaur, Could) are new player graphics; the form-swap
    CHR streaming (BRIEF §5.2) must leave room for them.
11. **Homage and trademarks.** All names are parodies (TOPPY, NITPICKY, Nasubi Mage, Grim Reap-bot, Jaja-nin) and no
    logos are used. "Sakugarne" is Capcom's own. The fortune slip's `大凶` is drawn as art (vanilla has no kanji font).
12. **Text volume.** About 70 hooks plus 20 death lines for four venues. If the pop-up window is busy,
    `story.md`/`meta.md` should rank them (first-time-only hooks first; death lines always).

---

## 8. Open questions

1. Does `systems.md` keep the vanilla weakness cycle (Flame > Blizzard > ... > Centaur > Wind > Flame)? The boss rows
   here assume it.
2. Plates: are they pickups (this doc) or still boss-kill rewards in a second boss room (vanilla `$3F:$F518`)? Pickups
   save two screens per venue and let the plate routes rejoin the main route.
3. Can a cleared venue be replayed for its other exit (the SMW model)? Vanilla beams you out of a beaten boss's room.
4. Does a secret-arena win also award the weapon? (Assumed yes: it is a full clear.)
5. Should the four behaviour chips be unique to their venues, or can `meta.md` overlap them with shop chips (DARUMA
   vs a shop "last stand")?
6. The tag partner joins mid-game: may venues place tag-only shortcuts (all marked Could here), and is Break Man
   callable in boss rooms?
7. CASUAL details: is the Toppy refill delay, the Daruma head's anger, or the merge's 5-s wait a CASUAL lever, or is
   CASUAL only damage and checkpoints?
8. Is X-UPEXIT accepted as a Should (Ice Climber needs it), or do the climbs ship with ladder stubs?

---

*Written by design-venues-b. Measurements: `build/design/design-venues-b/measure.py`, `measure2.py` (shot height, jump
rise 52 px, slide hitbox id). Map crops used for the outlines: `build/design/design-venues-b/*_0.png`, `*_1.png`.*
