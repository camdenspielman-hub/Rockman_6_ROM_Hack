# 4MI stages B: Toad Man, Dust Man, Skull Man, Bright Man (r4mi-stages-b)

Status: IN PROGRESS (rewritten as the investigation proceeds; Toad Man is the most complete section).

Scope: Rockman 4 Minus Infinity v1.01 (`roms/r4mi_mmc5.nes`), the stages of Toad Man (`$22` = 1), Dust Man (5),
Skull Man (7) and Bright Man (0): route, gimmicks, enemies, mid-bosses, hidden rooms, pickups, HARD differences, the
boss fights (patterns and weapon damage) and the jokes. Played with godmode (`cheats.godmode()`: frozen HP, lives and
i-frames, plus the SHOCK GUARD / TRAMPOLINE / BEAT safety items), so the "intended challenge" notes are my reading of
what a normal player faces.

Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text, **[doc]** readme, **[guess]**.

## 0. Method and new tools

### 0.1 How a 4MI stage is wired (new findings, useful for every stage) [code + seen]

- **Screens and sections.** `$B500-$B53F` of the stage bank (`$20 + stage`) is now a 64-entry table "global screen
  number → local layout index". A local index of 0 starts a new *section*. On entering a section the game unpacks
  its block set, metatiles and *all* its screen layouts into battery WRAM (`$6000` blocks, `$6400` block attributes,
  `$6500` metatiles, `$6900 + 64·local` layouts), so a section can be much longer than 12 screens (Toad's first section
  has 22, Dust's has 32). A copy of the 64-entry map sits at WRAM `$7100`. r4mi-stages-a found the WRAM part.
- **Vanilla's room table is gone; exits are an explicit link list.** The fixed-bank screen-transition code is still
  vanilla, but at `$7E:CD24` it far-jumps (`JSR $DF5F` + `80 6D 71`) into **bank `$71` @ `$806E`**, which looks the
  current screen up in a per-stage **link table** (pointers at `$71:$849E` lo / `$84AE` hi, indexed by `$22`).
  Entries are 8 bytes: `type, screen, exit, room, target screen, b5, section-to-load (b6, $FF = none), b7`. `exit` is
  `4` = leaving through the bottom, `8` = through the top (chosen by Rockman's Y: `$0378 ≥ $80` → bottom), `1` = right
  edge, `2` = left edge. Types 2-4 run the scrolling handler at `$81A6`. So **every vertical exit and every
  non-default horizontal exit in the game is one row in this table**, and that is how 4MI builds loops, warps and
  hidden rooms: a screen's exit can lead to *any* screen, including an earlier one. The dumper is
  `tools/analysis/r4mi/r4mi_links.py` (all 16 stages).
- Collision types in these stages (block attribute high nibble): 0 air, 1 solid, 2 ladder, 3 spikes, 4 ladder top,
  5 boss shutter, 6 water, 8 / 10 / 14 slope pieces (Rockman's RM3-style slopes), 12 water-edge / waterfall
  (passable), 14 / 15 also stage-specific breakable blocks (Toad's frog-egg pillars).
- Enemy placement keeps vanilla's format (`$B100` screen, `$B180` x, `$B200` y, `$B280` type) but almost every
  4MI enemy is placed as type `$08`/`$09` and runs object AI **`$5E`, a generic "4MI enemy" whose real kind is a
  sub-type in `$0468`** [code: the ●TOAD effect table at `$41:$A2E8` branches on AI `$5E` and indexes a second table
  by `$0468`]. Other placed types are items and markers (`$88`/`$89`/`$8A` at x≈8 look like section/music markers
  [guess]).

### 0.2 Scripts (scratch dir `build/research/r4mi/r4mi-stages-b/`)

| Script | What it does |
|---|---|
| `ghost.py`, `route.py` | "Ghost" explorer: BFS through the collision grid of the current screen and its neighbours, move Rockman along the path by poking X/Y/page (waiting for the camera), and let the engine do the transitions; climbs ladders for top exits, falls through bottoms, walks into shutters, kills bosses that block (`kill.py`), and as a last resort no-clips. `route.py` saves a state and a BG render at every screen (`scr/<stage>_NN.state`, `bg/`) and a route log |
| `stitch.py` | Assembles a stage map from the per-screen BG renders and the route log |
| `census.py` | Enemy census: per screen, the object AI ids / sprite ids / HP seen in 4 s, plus one screenshot each |
| `bossdmg.py` + `wsel.py` | Boss damage table. Weapons are selected the way the game does it (controller-2 A cycles weapons: poking `$A0` alone does **not** change the projectile, because the weapon's graphics and palette are loaded by the weapon-change routine) |
| `vlinks.py` | Link-table dumper (copied to `tools/analysis/r4mi/r4mi_links.py`) |

Gotcha for anyone driving controller 2 with `emu.py`: `step(buttons, player=1)` only sets player 2's mask, and it
*stays* set until you send `[]` for player 2 again. My first weapon-cycling attempt held P2-A forever and cycled once.

---

## 1. Toad Man stage (`$22` = 1): a flooded castle, a rain-soaked aqueduct, and a boss you can turn into a frog

48 screens in three sections: `0-21` (flooded stone-and-copper castle), `22-28` (outdoors in the rain), `29-47`
(aqueduct over waterfalls, indoor approach, boss). Checkpoints: screen 18 and screen 46 [seen]. Vanilla Toad Man is a
rainy sewer; 4MI keeps the rain only for the outdoor half and floods the whole first half.

![Toad Man stage map](img/stages_b_toad_map.png)
*Toad Man's stage stitched from the per-screen BG renders along the ghost route (screen numbers in yellow). The hidden
room (28) is drawn to the right of 27.*

### 1.1 Route, screen by screen [seen unless tagged]

| Screens | What happens |
|---|---|
| 0 | Start at the top of a sealed shaft. Drop through the slot in the floor (down-link 0 → 1). |
| 1-6 | **Flooded** tunnels: the castle interior is under water (slow falls, high jumps), walls trimmed with a dotted water edge, green pipes, copper columns with faces, and **slopes** (orange wedges; Rockman slides along them). **Water currents** push a standing Rockman sideways (in screen 5 he drifted ~12 px in 30 frames with no input). Small orange bird-fish robots swarm; green **frog statues on pillars** spit tadpoles (screens 3, 5, 6). |
| 6 → 7 | Drop down a shaft into the first mid-boss room. |
| 7 | **Mid-boss GAMARN AND GAMADAYU** (fight `$14`): a giant green frog mech with a hooded ninja rider (the frog is a big sprite on a pedestal; the rider is a separate object, slot 22). It fires white bars/lances and lobs bubble bombs; the room floor has spikes on the left. When it dies the rider flies off, and **the camera auto-scrolls right by itself** to screen 9 (screen 8 is an empty BG-drawn arena). |
| 9 → 10 → 11 | Two more drops (down-links). |
| 11-15 | A long flooded hall with ladders at the top and **giant orange pyramid slopes** on the floor, frog statues on pillars, tadpoles. The ladders at the top of screen 13 lead **up to the hidden room** (§1.3). |
| 15 → 16 → 17 | Slope descents (down-links), a big diagonal staircase room (17). |
| 18-20 | Checkpoint 1 (18). **Frog-egg pillars**: columns of round eggs (block types 14/15) block the corridor. Every egg is a separate breakable block; buster shots crack the bottom one into a bubble object, and you shoot your way through, egg by egg. A spiral "fiddlehead" egg (a tadpole curled up [guess]) sits on top of some columns. Screen 19 has a spike floor between the pillars. A boss shutter closes screen 20. |
| 21 | **Mid-boss PAKKUN SHADOW** (fight `$22`): **Shadow Man (MM3) riding a green frog**. The frog hops around the room, Shadow Man throws spreads of 4-point shuriken, and a smoke cloud "poof" marks his landings; small tadpoles crawl in. 28 HP, buster does 1 per hit with ~2 s i-frames. |
| 22-27 | **Outdoors in the rain** (diagonal blue rain BG): stilted platforms over a bottomless pit, small waterfalls, white gull-like birds, parachuting red bombs, and a big red domed walker (screen 26, AI `$46` with HP 254, i.e. not meant to be killed [guess]). Screen 27 has no floor: you **fall down into the aqueduct** (down-link 27 → 29, loading section `$1B`). |
| 29-39 | **The aqueduct**: a long walkway on arches over a row of waterfalls, still in the rain. Rockman rides on a small red **wheeled cart** for most of it [seen: red wheels under him in every frame]. Enemies: red crab robots, small fliers, a striped barrier pole, spike strips (screen 38), and pillars that rise out of the walkway. |
| 40-46 | Indoor copper halls again: red bird/crab robots (AI `$8E`, `$B0`). Checkpoint 2 is screen 46, in front of the boss door. |
| 47 | **Toad Man** (§1.4), in a green tiled room with a strip of water at the bottom. |

### 1.2 Enemies (census) [seen]

![Toad census](img/stages_b_toad_census.png)
*One screenshot per screen, 1.5 s after arriving, labelled with the object AI ids present (`5e` = generic 4MI enemy).*

### 1.3 Hidden room: screen 28 [code + seen]

The link table has `screen 13, exit up → screen 28` and `screen 28, exit down → screen 13 (reload section $0A)`. So
the ladder at the top of the flooded hall (screen 13, column 3) climbs into **a single screen that is not on the main
path**: a dark shaft with a ladder and two ledges holding an **E-tank, a 1UP and a large energy capsule**. Its floor
is open, and falling out of it drops you back into screen 13, so the trip costs nothing but time. It is drawn at the
end of section 2 (`22-28`), which is why it also appears to the right of screen 27 in the section render; from 27 it
is reachable only by staying high above the pit, which the floorless screen 27 makes impossible without help [seen:
every fall from 27 lands in 29].

![Toad hidden room](img/stages_b_toad_hidden.png)
*Screen 13's top ladder → screen 28 (E-tank top left, 1UP and big energy on the right ledge) → falling back into 13.*

### 1.4 Toad Man [seen + code]

**Behaviour.** Toad Man **does nothing until you shoot**: with Rockman only jumping (no B) he stood still for 1,600
frames. Once you fire (even shots that miss), he switches to vanilla-like play: high hops across the room toward
Rockman, the Rain Flush dance (arms up, white drops fall), and white splash bursts where he lands [seen]. The
readme's "very strong if you fight him with the buster" is about the i-frames: the buster does 1 damage and he is
then invulnerable for ~130 frames, so a buster-only fight takes 28 hits over about a minute [measured].

**●TOAD turns Toad Man into a real toad** [seen + code]. One hit of his own weapon does 28 damage and he becomes a
small hopping frog (AI changes; bank `$1D` @ `$BD1C` is the frog's AI). The ●TOAD weapon code (bank `$41` @ `$A11F`)
classifies every object through a table at `$41:$A2FC` (by AI id; AI `$5E` sub-types in a second table at `$A3FC`):
`$FF` = "Toad Man" (only AI `$8D`), which runs `$7898 |= $10` (**FLAG bit TOADMAN**) and `SEC / ROR $78A0` (marks the
fight result as a **draw**); `1` = turn the enemy into something else; `2` = damage; other values = damage of that
size. The frog keeps the boss bar at 28, hops harmlessly and never ends the fight on its own (12,000 frames). **Any
touch or hit kills it** (bank `$1D` @ `$BD2D`: player contact `JSR $F95D` or weapon contact `JSR $E9D1`), which
clears the TOADMAN bit again (`AND #$EF`), sets `$78A1 |= 2`, and ends the fight normally (weapon get, "YOU GOT
●TOAD"). Toad Man's own fight init (`$1D:$B80D`) also writes `$78A0 = 1` and clears the bit, so the flag cannot be
carried from an earlier attempt into a new fight (it does survive a death: it is in the autosave).

The ending code (bank `$0D` @ `$B10F`) prints the extra **"AND n DRAW"** line on Toad Man's result card only if the
TOADMAN bit is set at the end, and the RESULT code (bank `$4D` @ `$867E`) awards the BONUS "XXXXman" point from the
same bit. Together with Proto Man's hint "TOAD MAN WANT TO BECOME REAL TOAD" [text], the bonus is about transforming
him. How the bit is meant to survive the fight is still open (see open questions): every way of ending the fight
that I tried (all 15 weapons, touching, waiting, leaving) either killed the frog (bit cleared) or never ended.

**Weapon damage against Toad Man** (criticals off, measured from slot 23's HP; "i-frames" = shortest gap between
two damaging hits, which is the invincibility the hint file tells you to watch) [seen]:

| Weapon | Damage per hit | i-frames (frames) | Notes |
|---|---|---|---|
| Rock Buster | 1 | 127 | 28 hits needed |
| ●TOAD | 28 (transforms) | - | one hit |
| Drill Torpedo | 2 | 20 | |
| (others) | (pending) | | |

![Toad Man becomes a toad](img/stages_b_toad_toadtoad.png)
*●TOAD on Toad Man: one hit, he turns into a frog that hops around the room; touching it kills it and the fight ends
with "YOU GOT ●TOAD".*

---

## 2. Dust Man stage (`$22` = 5): an incinerator with a temperature gauge

(in progress) Findings so far [seen]:

- A **TEMP gauge** sits under the life bar for the whole stage, and the furnace rooms (screens 10-13) flash red and
  magenta.
- One long section (32 local screens); screens 16-22 reuse only two layouts (`16 16 16 17 16 17 16`), a repeating
  crusher corridor under ceiling pistons, with a **conveyor floor** of compacted garbage (pressing LEFT on it still
  carries Rockman right).
- **Screen 14 has a detonator.** A plunger box sits on the upper ledge next to a hopping red dome robot. Shooting the
  box blows a hole in the floor at the lower left (layout bytes `$6CA9/$6CAA` change [seen]), and the link table's
  `14 down → 15` drops you through it into checkpoint 1's garbage room. Without the detonator the room has no exit.

## 3. Skull Man stage (`$22` = 7)

(in progress) Link table: screen 0's floor leads down to a side branch `4-5` below the start; the main path goes right
`0-3`, then up `3 → 6 → 7`. Screens `29-35` are not linked from the main path (`28 → 37` skips them) [code].

## 4. Bright Man stage (`$22` = 0)

(in progress) Link table: screen 19's right edge leads to **screen 32** (and 32's left edge back to 19), a one-screen
side room at the end of section 2 holding items: the hidden room [code]. The stage has a bottom status bar ("WPN P").

## Lessons for Rockman 6 GP

(pending)
