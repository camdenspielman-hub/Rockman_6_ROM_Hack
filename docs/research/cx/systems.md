# Rockman CX player systems in practice (cx-systems)

Status: IN PROGRESS (skeleton written early so an interruption loses little).

Scope: the fake Rockman's toolset as it plays: the 8 boss weapons and the weakness chart, Items 1-3 (Instant Floor,
Subtank, Ubercharge) and their Dr. Light "upgrades", the dash, playable Quick Man, heart tanks, quick weapon change,
the HP-from-weapon-energy rule, the save system and menus. Tags: **[seen]** observed in the emulator, **[code]**
disassembly or ROM data, **[text]** in-game text, **[doc]** readme, **[guess]** speculation. ROM `roms/cx_en.nes`.
RAM names follow `docs/research/cx/cheats.md`.

## 1. The eight boss weapons

How they were tested: `cx.give_all_weapons()`, then each weapon equipped with the real Select+Down quick swap,
fired in the quiet brick corridor of `fire_mario_cp2` (frame logs of energy and object slots 2-9), and then fired at
eight boss rooms with a chase-and-fire script (`build/research/cx/cx-systems/bosshit.py`). The code is in two places:
the **fire dispatcher** `$3E:DA56` (12-entry jump table `$DCC7/$DCD3`, indexed by `$A9`) and the **boss-hit
dispatcher** `$17:A5F4` (12-entry jump table `$A90B/$A917`), which reads one 14-entry damage table per weapon,
indexed by the boss number `$B3` [code]. The player's colour changes with the weapon, as in RM2.

![Weapons in use](img/systems_weapons.png)

*One row per weapon, 2× zoom, frame numbers from the B press: Cheat Saber (slash arc, then a thrust that shrinks
back to the hilt), Dead Ringer (white "death" flash, then the 8-way ring burst of a Rockman death while the player
vanishes), Ringo Shield (leaf shield, then the thrown apple splatting on the wall), Fire Ball (SMB fireballs bouncing
along the floor), Print Cutter (paper sheets thrown up that flutter down), Mega Buster (pellet on the press, then a
full charge shot), Rider Kick (jump, hold B and a direction: a flying kick), Power Bomb (the "P" bomb, then the
blast).*

| Id | Weapon (from) | Colour | What it does [seen] | Energy (of 40) [seen][code] | On screen |
|---|---|---|---|---|---|
| 1 | **Cheat Saber** (Cheat Man, who is drawn as Mega Man X) | X's blue and purple | A melee **Z-Saber**: a crescent slash in front of you, then a straight blade that shrinks back to the hilt over about 28 frames (`$04E0 = $1C`). It works on the ground and in the air | **7 per slash** (1 unit about every 4 frames while the blade is out) | 1 |
| 2 | **Dead Ringer** (Air Man; the *TF2* Spy's watch) | blue | **Fakes your death.** B plays the full Rockman death: a white flash and the 8-way ring burst, while the player turns invisible (drawn 1 frame in 16, a shimmer). B again, or an empty bar, uncloaks after a 46-frame fade (`$AC = $EE`). The rings are real projectiles (flag bit 0 set on slots 3-14 at `$DBC2`): each burst can hit a boss once for buster damage [seen: Whispy took 1 at 24, 48 and 80 px]. While cloaked (`$AC` bit 7), the shared "turn to face the player" routine `$3F:EFC5` leaves enemies facing the way they were, and the aiming routine `$3F:F18B` uses a random number instead of your position [code]. **It is not invulnerability**: four bosses hit a cloaked player as often as an uncloaked one [seen] | **1 per 16 frames while cloaked**: a full bar is about 12 s of cloak (40 → 0 in about 720 frames) [seen][code `$1E:812D`] | 1 cloak |
| 3 | **Ringo Shield** (Whispy Woods; *ringo* = apple) | green | B raises a Leaf-Shield-style ball of leaves around you that **follows you** when you walk or jump. B again **throws an apple** straight ahead; it splits in two on the wall and splats on the floor. Bonus [code `$A6C9`]: each time the raised shield touches a boss, 16 frames are added to your invincibility timer `$4B` | **3 per shield** (the throw is free) | 1 |
| 4 | **Fire Ball** (Fire Mario) | Mario red | SMB's fireball: it bounces along the floor and pops on walls. On a boss it **sticks and burns**: the boss's table value becomes the fireball's burn timer (`$04E0`), the ball is moved onto the boss and does 1 damage per tick, about every 4 frames [code `$A6ED`, seen] | **1 per 2 shots** (`$DAF9`) | 2 |
| 5 | **Print Cutter** (Yoshino Man) | white/grey | A paper sheet thrown forward and upward that flutters down. It bounces back off walls | **1 per 3 shots** (`$DB2E`) | 3 |
| 6 | **Mega Buster** (Mega Man / Rock) | **Rock's blue**: you look like the real Mega Man | A Rockman 4 charge shot. Tapping fires pellets. Holding B: under 22 frames = pellet, 22-63 frames = half charge, 64+ frames = full charge [seen: measured hold lengths]. The charge level multiplies the damage ×1 / ×2 / ×3 [code `$A67C`] | pellet 0, half 1, full 3 (table `$1E:8278`) | 3 |
| 7 | **Rider Kick** (Kamen Rider) | green | **A flying kick, not a shot.** In the air, hold B with LEFT or RIGHT: the player strikes the kick pose and flies forward at 3 px/frame on the jump arc, then keeps sliding on landing. Without a direction, or on the ground, the kick object appears for only 2-4 frames. Not usable in player states `$09`, `$0A`+ or `$0C` [code `$DB4B`]. On a boss hit the game **freezes for about 8 frames** (the player hangs in place) and plays a DMC "thud" sample [code `$A776`, seen] | **1 per 2 kicks** | 1 |
| 8 | **Power Bomb** (Bomberman) | red-orange | A black bomb marked "P" rolls a short way, sits for about 80 frames, then explodes in a plus of fireballs | **3 per bomb** | 1 |

Special interactions [code][seen]:

- **The Cheat Saber kills every robot master in one hit except Cheat Man, and hitting Cheat Man with it kills
  you.** Its boss-hit handler (`$17:A668`) does: boss number 0 → `STY $06C0` with Y = 0, i.e. *your* HP becomes 0,
  then `JMP $A870` clears your i-frames and spawns the death explosion; boss numbers 1-7 → boss HP set to 0;
  fortress bosses (8-13) → normal table damage (14, 40, 8, 8, 37, 0). Seen: two frames after a point-blank slash,
  the player's HP went 24 → 0, the death rings played, a life was lost, and Cheat Man still had 40 HP.
  ![Cheat Saber on Cheat Man](img/systems_saber_kills_you.png)
  *Point-blank Cheat Saber on Cheat Man (frames 0-78, every 3rd): the slash connects, the label reads hp0 from
  frame 3, and the player explodes.*
- **Quick Man does double damage** with his buster (Quick Boomerang), the Ringo Shield and the Mega Buster: the
  shared damage path `$A635` doubles the value (`ASL`) when `$9B` bit 7 is set [code].
- The Fire Ball's entry in the boss-hit jump table points one byte past the start of its handler (`$A6ED` instead of
  `$A6EC`), so it skips the `LDA $0421 / AND #$08` check that makes other weapons bounce off a boss that is
  currently armoured [code; whether this is a bug or a deliberate "fire ignores armour" is unknown].
- A table value of 0 means the shot is **deflected** (it turns into object `$2F` and plays the ricochet sound `$2D`),
  except for the buster table, which has no zero entries [code].
- Items 9 and 10 (Instant Floor, Subtank) have no boss-hit handler (`$FFFF`); the Ubercharge (11) uses the buster
  table, because with the upgraded Über, B fires the normal buster (section 3).

## 2. Weakness chart

Damage per hit on 40-HP bosses, read from the ROM tables at `$17:A92B-$A99A` (Cheat Saber at `$A923` for the
fortress bosses) [code]. "–" = 0, the shot is deflected. Boss numbers `$B3` [seen in each boss state]: 0 Cheat Man,
1 Air Man, 2 Whispy Woods, 3 Fire Mario, 4 Yoshino Man, 5 Mega Man, 6 Kamen Rider, 7 Bomberman; 9 is the Quick Man
fight (the `air_man_midboss` state, which `stages_1.md` shows is a Light 2 room), 10 Light 3's Guts Tank, 13 the
Light 6 boss once it activates. Numbers 8, 11 and 12 are the other fortress bosses (not checked one by one; the
Light 5 teleporter-pad fight runs with `$B3 = 6`, so it may be a refight). Fire Ball values are burn timers in
frames, not damage (1 damage per tick).

| Weapon | Cheat Man | Air Man | Whispy | Fire Mario | Yoshino | Mega Man | Kamen Rider | Bomberman | #8 | #9 Quick Man | #10 Guts Tank | #11 | #12 | #13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Buster, Dead Ringer rings | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 |
| Cheat Saber | **you die** | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 14 | 40 | 8 | 8 | 37 | – |
| Ringo Shield | 2 | **7** | – | 2 | – | 3 | 1 | – | 1 | 2 | – | 2 | 5 | – |
| Fire Ball (burn frames) | – | – | **29** | 12 | 14 | 4 | – | 7 | – | 7 | – | 4 | 10 | 10 |
| Print Cutter | 2 | 2 | – | 1 | – | 2 | 3 | 2 | 1 | 2 | – | **3** | 2 | 1 |
| Mega Buster (×1/×2/×3) | **3** | 1 | – | 1 | 1 | 1 | – | 1 | – | 1 | 1 | 2 | 1 | – |
| Rider Kick | – | – | 2 | 3 | 3 | **4** | **4** | – | – | 3 | 1 | 1 | 4 | 2 |
| Power Bomb | 1 | 4 | 2 | **4** | **4** | **4** | 2 | **6** | 2 | 2 | **4** | 2 | 3 | 2 |

Checked in the emulator [seen] (chase-and-fire script, 900-1,200 frames per weapon, plus the four bosses in
`stages_2.md`): every measured hit matched the table, on Cheat Man (buster 2, Ringo 2, Print Cutter 2, Power Bomb
1), Air Man (Print Cutter 2, a full Mega Buster charge 3 = 1×3, Power Bomb 4), Whispy (buster 1, Saber 40, Rider
Kick 2, Power Bomb 2; the Fire Ball **burned him to death** in 1,016 frames, 40 ticks of 1), Fire Mario (buster 1,
Saber 40, Ringo 2, Print Cutter 1, charged Mega Buster 3, Rider Kick 3, Power Bomb 4, Fire Ball ticks of 1),
Quick Man #9 (buster 1, Saber 40, Ringo 2, Fire Ball 1-ticks, Print Cutter 2, Rider Kick 3, Power Bomb 2) and the
Guts Tank #10 (buster 1, Saber 8 ×5, Mega Buster 1, Rider Kick 1, Power Bomb 4). The "Rider Kick 4?" on Bomberman
in `stages_2.md` was his own bombs: his Rider Kick entry is 0.

The intended order, reading the best non-Saber weapon for each boss:

- **Whispy Woods ← Fire Ball** (fire burns the tree: 29-frame burns, the best ratio in the game).
- **Air Man ← Ringo Shield** (7 per hit). RM2's Air Man is weak to the Leaf Shield, and the Ringo Shield is a leaf
  shield, so the hack keeps vanilla's most famous weakness.
- **Cheat Man ← Mega Buster** (3 per pellet, 9 per full charge): Mega Man X is beaten by the original Mega Man's gun.
- **Fire Mario, Yoshino Man, Mega Man ← Power Bomb** (4); **Mega Man and Kamen Rider ← Rider Kick** (4).
- **Bomberman ← his own Power Bomb** (6) and **Kamen Rider ← his own Rider Kick** (4): two guests are weakest to
  their own signature move.
- Fortress: the Guts Tank takes 4 from the Power Bomb (and only 8 from the Saber); #12 takes 37 from the Saber.

## 3. Items 1-3 and the upgrades

(to be filled)

## 4. Dash

(to be filled)

## 5. Quick Man

(to be filled)

## 6. Heart tanks

(to be filled)

## 7. Quick weapon change, HP from weapon energy, saves, menus

(to be filled)

## Lessons for Rockman 6 GP

(to be filled)
