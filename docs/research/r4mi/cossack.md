# 4MI Cossack Citadel stages 1-4 (r4mi-cossack)

Status: IN PROGRESS (this file is rewritten as the investigation proceeds).

Scope: Rockman 4 Minus Infinity v1.01 (`roms/r4mi_mmc5.nes`), Cossack stages 1-4 (`$22` = 8, 9, 10, 11): route
screen by screen, gimmicks, enemies, mid-bosses, story events (Rush's arrival, the forced Balloon/Wire segments),
raster effects (pseudo-parallax, water), hidden rooms, pickups, HARD differences, the bosses (patterns, vanilla
comparison, weapon damage) and the jokes. Played with godmode (`cheats.godmode()`), so the "intended challenge" notes
are a reading of the design.

Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text, **[doc]** readme, **[guess]**.

## 0. Method

(pending)

## 1. Cossack 1 (`$22` = 8)

**In one line:** a night run from a train platform through a Russian city skyline (onion domes), down a shaft into
vanilla RM4's snowfield, where you pick up the BALLOON and jump off a cliff into a **fixed-screen "blizzard sky"
shoot-'em-up** that lasts about 3.5 minutes: squadrons of fighters, flying whales, **Shadow Man popping your balloon**,
**Rush arriving as Rush Jet** to catch you, and a giant sky serpent. Then you fly Rush Jet past the citadel wall into
the boss: **Mothraya, fought in mid-air on Rush Jet**. The readme's "forced Balloon segment until Rush arrives" is this
arena [doc + seen].

![Cossack 1 route](img/cossack_c1_route.png)
*Cossack 1, one frame per screen in route order (screens 0-19 on foot, then the screen-20 sky arena, 23 = boss).*

### 1.1 Route, screen by screen [seen]

Two sections: screens 0-24 (the whole stage as played) and 25-47 (the "city at dusk", see 1.4). `$0348` = screen.

| Screen | What happens |
|---|---|
| 0-1 | Start beside a parked passenger train (the castle intro ends with Rockman riding a Wire line in; cp0 has PROG = 8, "after the entrance scene" [doc]). Bumpy orange track bed; a Metall riding a small cart on screen 1. |
| 2 | Into a blue-glass building; drop through the floor gap on the right (cols 11-13). |
| 3-4 | Brick hall with stair blocks. The exit is a 2-tile-high tunnel *under* the stair block (rows 10-11) with Metalls in it; jumping up the stairs is a dead end. Orange flying-fish robots swoop. |
| 5 | A window onto the city, a desk-like turret. |
| 6-7 | Outside: night city with onion-dome silhouettes. Blue robots stand on pedestals and toss bouncing striped balls; small pits. |
| 8 | Brick tower with a ladder up (the only way on). |
| 9 | Pillar tops over pits. |
| 10-11 | Spiky-haired blue robots that run and shoot, dome cannons that lob white balls, pits. |
| 12-13 | Drop down a two-screen shaft. |
| 14 | **The vanilla RM4 Cossack 1 snowfield** (black pine silhouettes, snow on orange earth). A big blue robot (object `$1F`) with **254 HP** hops, turns into a jet/drill form and fires ring shots; it shoves you back to screen 13 on contact. The buster does 1 per hit (it took ~1150 frames of continuous fire to kill it), so this is hint.txt's "mooks that are too hard: better not to fight them" (`硬すぎる雑魚がいる`): jump it [doc + seen]. |
| 15 | Snow steps; small blue helicopter drones that fire three-way spreads; another walker. |
| 16 | **A green "B" capsule = the BALLOON** (picking it up sets `$B6 = $9C`, owned and full, with a ~290-frame freeze, player state 9) [seen]. It is there even if you already own the Balloon (from Dive Man's stage). Picking it up silently **re-numbers the screen from 16 to 19**: screens 16 and 19 are drawn identically, so the jump is invisible [seen]. |
| 19 | **Checkpoint 1.** A cliff edge over a bottomless drop; a hovering red box with a "→" sign (object `$74`, 24 HP) waits at the edge. Falling = death (pit), so you must make a Balloon (select it, jump, press B: a small pink balloon appears under your feet and you steer it with the D-pad) [seen]. |
| 20 | **The blizzard sky arena** (1.2). The camera is locked at x = 5120 for the whole event. |
| 21 | Rush Jet flies past a white citadel wall carrying Dr. Cossack's "Dr C" emblem. |
| 22 | **Checkpoint 2.** A black night sky with dashed "speed lines" (the flight continues), a few ring and spinner drones. |
| 23 | Boss room: Mothraya (1.3). |

**Screens 17-18 are never visited on this route** [seen]: rendered with the right tiles, 17 is solid earth and 18 is a
small brick room under the snow with a ladder up and an exit at the bottom right. The 16 → 19 renumbering skips them,
and walking left from 19 stops at a wall. Whether some other condition opens them was not found.

**HARD** (`$78CD = 1`, entered from EXTRA CONFIG): the section layouts and the objects at cp0, cp1 and cp2 are
byte-identical to NORMAL [seen], so any HARD change here is in enemy or boss behaviour (not checked).

### 1.2 The blizzard sky (screen 20): a shoot-'em-up on a balloon [seen]

![Cossack 1 sky arena](img/cossack_c1_sky.png)
*The screen-20 event in order (frame counts from leaving the cliff on a Balloon), then the citadel wall, the night dash and Mothraya.*

The screen never scrolls: the "flight" is sold by a background that thickens from a sparse dotted night sky into a
dense blizzard pattern (the staff roll's subtitle for this stage, per text.md, is *-BLIZZARD SKY-*). A spawner object
(`$7A`) feeds waves in, and S.VAL `$782E/$782F` step as they pass (`192,160` → `54,161` → `180` → `50,162` → `78`).
The order, with a hovering player shooting forward:

1. ~0-25 s: red jet squadrons in V and line formations (objects `$78`/`$79`, `$7B` leaders + `$7C` wingmen),
   red-white birds, white seagulls in flocks, green capsule pods and **homing pods** (object `$69`) that stick to you.
2. ~25-60 s: green caterpillar chains that snake across the screen.
3. ~63 s: a white flash and **two green flying whales** (airships with fins and a hatch, the same idea as Dive Man's
   whale battleship). They open their mouths and spit small fighters.
4. ~77 s: **Shadow Man** (spiky head, forehead star, red scarf) appears, throws shuriken and **pops the balloon**.
   Rockman falls, and **Rush flies in as Rush Jet and catches him**. Shadow Man then fights you as a mini-boss
   (object `$4C`, HP `$9C` = shares the boss bar `$BF`): in my run eight buster hits drove him off (bar 28 → 0 by 4s).
   This is where the RUSH friend joins in story terms; the FLAG byte `$7898` did not change during the event, so the
   RUSH and SHADOWMAN Hero-Score bits are earned elsewhere (bank `$56`'s `ORA #$08` sits in what looks like the
   Rush-call routine) [seen + code, guess on the meaning].
5. ~83-130 s: more squadrons and pods, now on Rush Jet (normal blue Rockman palette; Rush Jet moves freely in 8
   directions).
6. ~130-195 s: a **giant segmented sky serpent** (blue and white beads) that coils around the screen. When it is gone,
   the camera is released and Rush Jet flies on into screen 21.

Rush Jet is the only time Rush gives you mobility in 4MI (hint.txt: "unlike the original, Rush does not support
movement in this hack"), and it is a story event, not a weapon [doc + seen]. While Rush is the jet, selecting WISH STAR
or RUSH CANNON does nothing [seen: zero hits on the boss]. The readme's no-kill notes call this part "very hard in the
air; with luck you can push the homing mooks off the screen" (limited.txt `空中が至難の技`) [doc].

**Tooling gotcha:** with godmode's frozen i-frame timer the homing pods (`$69`) sit on Rockman forever and the wave
controller waits for them, so the arena stalls. Push them off-screen (`zap69()` in `build/research/r4mi/r4mi-cossack/sky.py`).

### 1.3 Boss: Mothraya on Rush Jet (fight `$08`, screen 23) [seen]

You fight in open night sky, standing on Rush Jet, so the fight is 2D dodging instead of vanilla's floor fight.

- **Parts:** body = slot 21 (object `$0E`, HP `$9C`: the bar), head = slot 22 (`$07`, 14 HP), and a separate
  **abdomen pod** = slot 23 (`$16`, 28 HP of its own). Shooting the pod does not touch the bar; when the pod's 28 HP
  are gone it turns into object `$19`/`$1D` and then cycles (slot 23 HP alternating 0/127, a respawning dart launcher).
- **Movement and attacks:** it loops around the whole screen, fires bursts of white pellets from its shoulders, and
  launches red darts (object `$1D`) that fly at you. Its eye lenses switch between cyan and red.
- **Phases:** at bar 20 and again at bar 10 it flashes white and becomes untouchable for a while (frames 136-270 and
  334-991 in a Drill run), then resumes; at 0 the screen turns white with the moth as a black silhouette before it
  explodes.

Damage to the body (slot 21), crits off, measured with `build/research/r4mi/r4mi-cossack/bdmg.py` (steering Rush
Jet beside it and firing):

| Weapon | Damage per hit | Boss i-frames after a hit | Hits to kill (28) |
|---|---|---|---|
| Rock Buster | 1 (one 3, a stray crit) | **49** | 24+ |
| Toad / Wire / Dive / Ring / Bright | 1 | 19 | 28 |
| **Drill** | **2** | **13** | 14 |
| Dust | 2 | **59** | 14 |
| Skull (Hell Wheel) | 1 | 49 | (only 3 hits land: it needs a floor) |
| Pharaoh | 0 | - | (never hit the body) |
| Wish Star, Rush Cannon | - | - | unusable while Rush is the jet |

So **Drill** is the weakness (double damage *and* the shortest invincibility), and Dust hits hard but leaves the
longest window. Versus the abdomen pod (slot 23, 28 HP) the numbers are the hack's fixed "normal enemy" values:
Drill 4, Dust 3, Toad/Ring/Bright/Pharaoh 2, Buster/Dive/Wire/Skull 1, with only 2-8 frames of invincibility.

**Vs vanilla** [guess: from memory of vanilla RM4, not re-played]: vanilla Mothraya is fought standing on a floor and
is weak to the Drill Bomb; the new things are the Rush Jet arena, the separate pod target, and the two invulnerable
phase breaks.

### 1.4 The "city at dusk" section (screens 25-31): arena-only fights

Section 2 of the stage (screens 25-47) is a pink-and-purple sunset skyline with a Kremlin-like silhouette and a
green girder floor. It holds the MY ARENA mid-boss fights `$10`-`$13` (scout, cheats.md §5b): a white runner robot plus
green hoppers (`$10`), a big frog robot blowing bubbles with tadpoles (`$11`), a round pink pod with birds (`$12`) and a
two-bar fight on screen 31 (`$13`). **The normal route never goes there** (0 → 23 → clear), so these look like content
made for the arenas [seen; purpose = guess].

![City at dusk fights](img/cossack_c1_city.png)
*MY ARENA fights `$10`-`$13`, loaded in Cossack 1's second section (2 s apart).*

### 1.5 Jokes and references

- Shadow Man **pops the balloon you were forced to use**, and Rush, who "does not support movement in this hack",
  turns up as Rush Jet anyway, as a plot rescue.
- Flying whales over a blizzard: the sky version of Dive Man's whale battleship.
- The real vanilla Cossack 1 (snowfield, pines) survives as screens 14-16, sandwiched between the new city and the
  sky.
- Credits [doc]: "Cossack 1's enemy graphics provided by B&K"; "Cossack 1's trap" is credited as similar to *Mega Man
  Forever* (Wing) and *Odyssey* (Duplex).

## 2. Cossack 2 (`$22` = 9)

(pending)

## 3. Cossack 3 (`$22` = 10)

(pending)

## 4. Cossack 4 (`$22` = 11)

(pending)

## Lessons for Rockman 6 GP

(pending)
