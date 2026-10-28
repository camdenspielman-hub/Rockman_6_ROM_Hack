# Rockman 6 (J) engine tables (rm6-engine)

Status: **draft v1, in progress** (object system and damage done; weapons, IRQ, sound, coverage, password, lag
follow). Tags as in the field guide: **[seen]** emulator, **[code]** disassembly / ROM data, **[guess]**.
Addresses are `bank:addr` with the bank mapped where the game maps it (AI banks are mapped at `$8000` with
`$CBC0`, so an odd bank such as `$29` or `$31` appears at `$8000-$9FFF` there). Fixed banks: `$3E` = `$C000`,
`$3F` = `$E000`. RAM names follow `ram.md`.

Scripts: `build/research/rm6/rm6-engine/` (`r6.py` = ROM + py65 disassembler with explicit bank pairs,
`objtypes.py` = the 256-type table dump `objtypes.txt/json`, `dmgmap.py` = which damage routine each type calls).

---

## 1. Object system

### 1.1 Object table and the AI loop [code]

23 slots x 29 arrays at `$03A0-$063A` (see `ram.md`). Slot 0 = Rockman, 1-3 = buster/weapon shots
(allocator `$3F:$E514` searches 3..0), 4 = Beat / Rush, 5-7 special, 8-$15 = enemies, items and bosses
(allocator `$3F:$E59F` searches $15..8, `$E5AF` = allocate + init), $16 = the screen script (type `$80`).

- Object loop `$3F:$E438`: X = $16 down to 0; empty slots (`$03A0` = 0) are skipped; for a live slot it maps the
  AI bank pair `$0441,X` / `+1` with `$CBC0` and does `JMP ($0413/$042A)` (via `$E486`).
- AIs are **coroutines**: `JSR $E46C` = yield (stores the return address back into `$0413/$042A`, restores the
  stack from `$90`, next slot); `JMP $E45A` = delete self (type 0, `$03FC` = `$FF`, HP `$FF`); `$E47B` = end
  this slot's turn without changing the resume address.
- Off-screen test `$E489` (carry set = off screen: Y screen != 0, Y >= $F8, or not on the camera's screen).
- Motion `$E4CF` / `$E4D5`: add `$EB/$ED` (X speed lo/hi) and `$EC/$EE` (Y speed) to the slot's position.
- Animation start `$E526` (Y = animation id, from the sprite bank `$0458,X` tables `$8600/$8700`), `$E561`
  restarts only if different.

### 1.2 Type tables (`$3A:$82C9`) [code]

Indexed by type id t (0-$FF), all in bank `$3A`:

| Table | Meaning |
|---|---|
| `$82C9+t` | AI entry address, low byte |
| `$83C9+t` | AI entry address, high byte |
| `$84C9+t` | AI bank (the `$8000` bank of the pair; `$0441`) |
| `$85C9+(t>>4)` | sprite / animation bank for the 16 types of a row (`$0458`): $20 for 0-$4F, $22 for $50-$8F and $A0-$AF/$C0-$DF, $24 for $90-$BF, $E0-$FF |

Init `$3A:$81F0` (far-call `$41` = bank `$3A` function 1, Y = type, X = slot) copies these and clears
`$0583/$056C/$04B4` and four AI variables. **Free type ids** (AI pointer `$0000` / filler): `$7B`, `$7C`,
`$BA-$BF`, `$CE`, `$D2`, `$D7`, `$DB-$DF`, `$F5-$FF` (and `$00`, `$42`, `$7D`, `$F4`, `$7E` point at
junk). That is **about 30 unused ids** for GP's new enemies.

Type families by AI bank [code] (`objtypes.txt`):

| Bank (at $8000) | Types | What |
|---|---|---|
| `$38` (+`$39`) | `$04-$0F`, `$81-$89`, `$8D`, `$8E`, `$DA`, `$E4` | Rockman (`$04` = AI `$802D`), buster shots, the ten weapons and their child objects |
| `$30` (+`$31`) | `$10-$4F` mostly | normal enemies, Flame/Knight/Blizzard groups, power blocks |
| `$29` (+`$2A`) | `$3D-$3F`, `$59-$78`, `$A0-$AD`, `$C0-$CD` | normal enemies (Wind/Plant/Tomahawk/Yamato/fortress) |
| `$31` (+`$32`) | `$90-$B5`, `$8A`, `$8F`, `$B8`, `$B9` | **Robot Masters and their projectiles**, boss-room controller `$93`/`$94` |
| `$3B` (+`$3C`) | items (`$1D`, `$37-$39`, `$49`, `$4A`, `$7F`), respawn beam `$03`, `$50-$57` gorilla tank, Mr. X 1 riders `$B6/$B7`, misc | |
| `$39` (+`$3A`) | `$80` screen script interpreter (`$824D`), `$D0-$F3` fortress bosses (Mr. X 3/4, Wily 2/4 machines, capsule) | |

### 1.3 The AI header (6 bytes before the entry point) [code]

Almost every AI starts with `JSR $EBD5`, which reads the 6 bytes in front of its own entry address:

| Byte | Goes to | Meaning |
|---|---|---|
| AI-6 | `$E526` | first animation id |
| AI-5 | `$C9EF` | sprite palette program (0 = none) |
| AI-4 | (read by `$3A:$826F`) | **sprite CHR set** queued when the camera enters the screen |
| AI-3 | `$059A` | **hit box id** (size table used by `$F72A`) |
| AI-2 | `$03E5` | **HP** (dies when it goes negative, so HP n takes n+1 damage; `$7F`/`$FF` = never hurt in practice) |
| AI-1 | `$0583` | **attack byte**: high nibble = class, low nibble = contact damage / shot power |

The header is the whole "enemy stats" table: there is no separate HP or damage table. Types without
`JSR $EBD5` (`-` in `objtypes.txt`) set these fields in code.

### 1.4 Spawning [code]

- Level objects: `$3A:$8120` (function 0, every frame) walks the stage's object list (`levels.md` section 8)
  and spawns into `$15..8` with `$03FC` = list index; the kill bitfield `$0650+` (set by `$3F:$ED25`) stops
  respawns of killed enemies and taken items.
- Child objects: `LDY #type / JSR $E5AF` (allocate in `$15..8` + init) or `JSR $E514` (shots, 3..0), or an
  explicit slot `LDX #slot / LDY #type / JSR $CB28 .byte $41` (bosses go to slot 8: `$3F:$FA74` spawns the
  Robot Master controller `$93`).
- Robot Master rooms: script `$0A` (`$3F:$F94A`) -> `$FA07` (music `$0C`, shutter checkpoint) -> `$FA63`:
  loads the boss sprite CHR set `$FA5B[stage & 7]` = `36 3F 45 43 3E 44 39 46`, waits 60 frames, spawns type
  `$93` into slot 8. `$93` (`$31:$98AA`) spawns the room controller `$94` into slot 9, plays the intro pose
  (`$F200` animation, `$F218` palette by stage), fills the bar (`$EF2D`) and replaces itself with the boss type
  from **`$31:$9D43[stage & 7]`**.

**Boss AI entry points** [code][seen] (all HP `$1B`; header byte = attack byte, low nibble = contact damage):

| Boss | Type | AI | Attack byte | Boss | Type (slot 8) | AI | Parts |
|---|---|---|---|---|---|---|---|
| Blizzard Man | `$90` | `$31:$8006` | `$F5` | Mr. X 1 riders | `$B7` (bar) | `$3B:$81D1` | riders `$B6` `$3B:$8006`, shells `$B8`, bombs `$B9` |
| Wind Man | `$99` | `$31:$8A9C` | `$F5` | Mr. X 2 pods | `$EB` | `$39:$978D` | rocks `$EC` |
| Plant Man | `$B2` | `$31:$95D0` | `$F5` | Mr. X 3 tank | `$E8` | `$39:$95EB` | `$E9` boxes |
| Flame Man | `$9C` | `$31:$9050` | `$F4` | Mr. X 4 machine | `$D3` | `$39:$98DF` | `$D1`, `$D2` boxes |
| Yamato Man | `$98` | `$31:$870E` | `$F4` | Wily 1 dinosaur | `$E0` | `$39:$92B6` | `$E1` head/body boxes |
| Tomahawk Man | `$9F` | `$31:$938C` | `$F4` | Wily 2 walker | `$E5` | `$39:$942F` | `$E6` |
| Knight Man | `$95` | `$31:$8324` | **`$34`** (class 3 = shield) | Wily Machine 1 / 2 | `$EF` / `$F1` | `$39:$9AFE` / `$9CD6` | six / three `$E9` boxes |
| Centaur Man | `$9B` | `$31:$8D76` | `$F0` | Wily Capsule | `$F2` | `$39:$9CE7` | shots `$F3` |

Robot Masters share the per-frame routine `$31:$997D` (blink, damage, death); fortress bosses share
`$3F:$EF2D` (bar fill, music `$F1`) and `$3F:$EF64` (damage). Knight Man's class-3 attack byte is why shots
from the front bounce off his shield (section 2.2). **Power-punch rebound**: in Wily 1 (`$39:$93B0`) and in one
more fight (`$39:$8229`) an enemy projectile hit by the full punch (`$14`) is replaced by a player-side object
`$E4` / `$DA` (attack `$1A`) flying back; Wily 1's head box `$E1` (`$39:$9288`) reacts to `$1A` only and turns
it into 1 damage on the controller.

---

## 2. Collision and damage

### 2.1 The attack byte (`$0583`) and the hit latch (`$056C`) [code]

Every object's `$0583` = `CCCC DDDD`: class C (0-F) and power D. When a player shot touches an enemy, the
shot's `$0583` is copied into the **enemy's** `$056C` (hit latch). The enemy's own AI then calls one of the
damage routines below, which reads `$056C`, subtracts HP and clears it. So the damage a weapon does is decided
by **the victim's damage routine**, with the shot's byte as input.

Classes of the player's shots [code] (shot type = `$80 + $0699` for weapons, `$38:$856A` handler table):

| Class | Shot byte | Weapon | Shot object(s) | Energy per use |
|---|---|---|---|---|
| 1 | `$11` | R.BUSTER (`$09`), half charge `$0A` | `$38:$8C9D` | - |
| 1 | `$13` | full charge (`$0B`) | | - |
| 1 | `$12` / `$13` / `$14` | Power Rockman punch: tap `$0C`, half `$0E`, **full `$0F` = `$14`** | | - |
| 1 | `$11` | Jet Rockman buster (`$09` always: Jet cannot charge, `$38:$854A` row 1) | | - |
| 5 | `$52` | Y.SPEAR (`$81`) | `$38:$9AC1` | 1 |
| 6 | `$62` | W.STORM (`$82`) | `$38:$9B22` | 1 |
| 7 | `$72` | B.ATTACK (`$83` spawns 4 x `$8E`) | `$38:$9B8D` | 3 |
| 8 | `$84` | F.BLAST (`$84`) | `$38:$9C28` | 1 |
| 9 | `$94` | PLANT.B (`$85` spawns 4 x `$8D`) | `$38:$9D08` | 4 |
| A | `$A3` | KNIGHT.C (`$86`) | `$38:$9DB1` | 1 |
| B | `$B3` | SILVER.T (`$87`) | `$38:$9E26` | 1 |
| C | `$C4` | C.FLASH (`$88`): writes `$C4` straight into `$056C` of **every** object of class 1, 3 or F | `$38:$9E52` | 4 |
| D | `$DF` | BEAT (`$89`/`$0D`, slot 4) | `$38:$9EB8` | HP of the victim + 1 |

Energy: `$38:$9E8E` adds A (signed) to `$0688+$0699`; a weapon whose energy is negative kills its shot at
once. [Charge thresholds] `$9E` counts up while B is held: >= `$24` = half charge, >= `$06AB` (= `$5A`) = full
(`$38:$8651`); table `$38:$854A` = shot type by form x level (`09 0A 0B / 09 09 09 / 0C 0E 0F`).

### 2.2 Shot meets enemy: what happens to the shot [code]

`$38:$8FDF` (called by every shot each frame) tests the shot against slots $15..8 (`$3F:$ECC8`, box sizes
from `$059A`) and dispatches on the **enemy's** class through `$38:$8FBF/$8FCF`:

| Enemy class | Handler | Effect on the shot |
|---|---|---|
| 0 | `$9021` | passes through, enemy latches the hit (multi-part bosses' hit boxes) |
| 1, 9, A, B, E, F | `$9067` | normal hit: latch; the shot vanishes **unless its power kills the enemy** (it then flies on). PLANT.B (`$94`) vanishes with all four leaves (`$9034`); BEAT (`$DF`) see below |
| 2, 6, 8 | `$90D6` | **reflected** ("dink", sound `$27`): the shot loses its attack byte and bounces back up-left/right |
| 3 | `$90A2` | **shielded**: reflected if it comes from the side the enemy faces; the charged punch (`$14`) always hits; type `$A2` special-cased |
| 4 | `$9028` | enemy bullets: shots pass; **PLANT.B deletes the bullet** (and the barrier) |
| 5, 7, D | `$9027` | no interaction |
| C | (`$9119`, unused) | no enemy has class C |

Player contact (`$38:$8EA0`, skipped while `$A2` != 0) dispatches on the enemy class through `$38:$8F46`:
0 and A harmless, 2/5/9 = **solid platform** (`$8F96`, stand on it), 7 = touch flag only (`$8F6C`: items,
Rush), 8 = hurt **and** solid, every other class hurts for the low nibble (`$8F72`, sets `$A2`).

### 2.3 Damage routines (the victim side) [code]

| Routine | Users (`dmgmap.txt`) | Rule |
|---|---|---|
| `$3F:$E9D7` | ~35 normal enemies (most of bank `$29`/`$30`) | **damage = low nibble of the shot byte**; death -> becomes type `$17` (explosion + item drop) |
| `$3F:$EA20` | 5 types (`$10`, `$59`, `$A2`, `$C5`, `$CA`) | same, death -> type `$25` |
| `$3F:$EA6E` | 62 types | immune: clears the latch (armour, projectiles, invulnerable phases) |
| `$3F:$EA99` | `$15`, `$18` (Metall), `$24`, `$A3` | **only the full-charge Power punch (`$14`) hurts** (via `$E9D7`) |
| `$3F:$EA80` | `$2E`, `$2F` | immune, stays while off-screen check |
| `$3F:$EAB7` (A = table) | `$1E`, `$2A`, `$2C`, `$2D`, `$4D`, `$75` | per-class table `$EB46` / `$EB56` / `$EB66`; class 1 = low nibble; `$80` = instant kill |
| `$31:$997D` | the 8 Robot Masters | per-boss table `$31:$9A45 + 16 * (stage & 7)` (2.4) |
| `$3F:$EF64` | fortress bosses (slot 8) | per-class x fortress-stage table `$3F:$EFE4` (2.5) |

Damage to normal enemies by weapon (the `$E9D7` rule) [code]: buster 1, half charge 1, full charge 3,
Y.SPEAR 2, W.STORM 2, B.ATTACK 2 (per flake), F.BLAST 4, PLANT.B 4, KNIGHT.C 3, SILVER.T 3, C.FLASH 4 (to every
class 1/3/F object on screen), punch 2 / 3 / 4, BEAT = kills any class-1 enemy outright and costs `HP + 1`
BEAT energy (`$38:$9088` -> `$9E8E`).

Enemy tables (`$EAB7`), index = shot class:

| Table | Used by | 5 SPEAR | 6 STORM | 7 B.ATK | 8 F.BLAST | 9 PLANT | A KNIGHT | B SILVER | C FLASH | D BEAT |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 `$EB46` | `$2D`, `$75` (Knight's blue hall) | 0 | 0 | **kill** | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 `$EB56` | `$1E`, `$4D` (Blizzard walkers, snow robot) | 2 | 2 | 1 | **kill** | 3 | 3 | 4 | 4 | 3 |
| 2 `$EB66` | `$2A`, `$2C` (Flame juggler, Fire Telly) | 2 | 2 | **kill** | 1 | 3 | 3 | 3 | 4 | 3 |

(Buster/punch, class 1, use the low nibble in tables 1 and 2; table 0 ignores the buster.)

### 2.4 Robot Master weakness table `$31:$9A45` [code][seen]

`$31:$997D` is the Robot Masters' per-frame damage + blink routine. Rules: no damage while the boss blinks
(`$0640` = `$3C` frames after a hit), while its own class is A or 6, or for latch `$30`. Class 1 (buster) =
low nibble; **latch `$14` (full punch) = 2** and only when `$063E` != 0 (`$9AD6`); every other class looks up
`$9A45 + 16*(stage&7) + class`:

| Boss (`$063D`) | 5 Y.SPEAR | 6 W.STORM | 7 B.ATTACK | 8 F.BLAST | 9 PLANT.B | A KNIGHT.C | B SILVER.T | C C.FLASH |
|---|---|---|---|---|---|---|---|---|
| 0 Blizzard | 1 | 1 | 1 | **4** | 0 | 1 | 1 | 0 |
| 1 Wind | 1 | 1 | 1 | 1 | 0 | 1 | 1 | **4** |
| 2 Plant | 1 | 1 | **4** | 2 | 0 | 1 | 1 | 0 |
| 3 Flame | 1 | **4** | 1 | 1 | 0 | 1 | 1 | 0 |
| 4 Yamato | 1 | 1 | 1 | 1 | 0 | 1 | **4** | 0 |
| 5 Tomahawk | 1 | 1 | 1 | 1 | **4** | 1 | 1 | 0 |
| 6 Knight | **4** | 1 | 1 | 1 | 0 | 1 | 1 | 0 |
| 7 Centaur | 1 | 1 | 1 | 1 | 0 | **4** | 1 | 0 |

Classes 0-4 and D-F are `$FF` (never reached: BEAT never latches on a class-F boss, so "BEAT 1" in the
measured tables is the buster shot that BEAT mode also fires, `$38:$85D0`). Every value matches the measured
tables in `stages_a.md` / `stages_b.md` [seen], including Plant Man's F.BLAST 2. Death: `$ED42` (explosion,
sound `$26`); Centaur also runs `$8F74`.

### 2.5 Fortress boss table `$3F:$EFE4` [code][seen]

`$3F:$EF64` (slot 8 only): stage >= 8 and class != 1 -> `damage = $EFE4[class*8 + (stage-8)] & $0F`; 32
frames of flashing (`$05DF`, palette `$BB`) after a hit; death restores palette `$0624,X`.

| Class | Mr. X 1 | Mr. X 2 | Mr. X 3 | Mr. X 4 | Wily 1 | Wily 2 | Wily 3 | Wily 4 |
|---|---|---|---|---|---|---|---|---|
| 5 Y.SPEAR | 0 | 2 | 1 | 1 | *4* | 2 | 0 | 1 |
| 6 W.STORM | 0 | 1 | 1 | 1 | 1 | **4** | 0 | 1 |
| 7 B.ATTACK | 0 | 1 | **3** | 1 | 1 | 1 | 0 | 1 |
| 8 F.BLAST | 0 | 1 | 1 | **4** | 1 | 1 | 0 | 1 |
| 9 PLANT.B | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| A KNIGHT.C | 0 | 2 | 1 | 1 | 1 | 1 | 0 | 2 |
| B SILVER.T | 0 | **3** | 1 | 1 | 1 | 1 | 0 | **4** |
| C, D | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Matches `fortress.md` section 11 for Mr. X 2-4, Wily 2 and the Wily Machine / Capsule (Wily 4). Mr. X 1's
riders (`$3B:$8006`) use the plain `$E9D7` rule (hence their 2/2/2/4/4/3/3 row), Wily 3 uses the Robot Master
tables. **Wily 1's column says Y.SPEAR 4, but play gives 0** (`fortress.md`): the table is live (poking a
Y.SPEAR latch `$52` into slot 8 takes 4 HP [seen]), yet shots never reach the controller's own box; even shots
glued onto its position latch onto the `$E1` boxes in slots `$0A`/`$0C` instead [seen]. So Wily 1's intended
weakness is unreachable in vanilla. Class 1 (buster, punch) = low nibble, which is
why the full Power punch does **4** to every fortress boss but only 2 to Robot Masters.

---

### 2.6 Measured check: every weapon against a normal enemy [seen]

`wtest.py` pokes a type-`$10` enemy (HP 15, class 1, `$EA20` rule) into slot 9 in front of Rockman in
Blizzard Man's stage (all weapons, godmode), pins it there, fires, and logs every HP drop and the energy used:

| Weapon | Damage per hit | Energy per use (of 28) |
|---|---|---|
| R.BUSTER / Jet buster | 1 | 0 |
| full charge (B held 100 f) | 3 (a half charge gives 1) | 0 |
| Y.SPEAR | 2 | 1 |
| W.STORM | 2 | 1 |
| B.ATTACK | 2 per flake | 3 |
| F.BLAST | 4 | 1 |
| PLANT.B (enemy 12 px away) | 4, and the barrier vanishes | 4 |
| KNIGHT.C | 3 | 1 |
| SILVER.T | 3 | 1 |
| C.FLASH | 4 (screen-wide) | 4 |
| BEAT | 15 (= kills); costs the victim's HP + 1, so the 2nd kill emptied a full bar (energy `$FF`) | see left |
| Power punch tap / full charge | 2 / 4 | 0 |

Every value is what section 2.3 predicts from the code.

---

## 3. Weapons and adaptors

### 3.1 Firing [code]

The player AI (bank `$38`, entry `$38:$802D`, type `$04`) calls `$38:$856A` when B is pressed: a jump table
`$38:$8556/$8560` by `$0699`:

| `$0699` | Weapon | Fire routine | Rule |
|---|---|---|---|
| 0 | R.BUSTER | `$862C` | charge logic below; shot type from `$854A[form*4 + level]` into a free slot 3..0 (`$E514`) |
| 1, 2, 4 | Y.SPEAR, W.STORM, F.BLAST | `$8582` | type `$80+w`, one at a time (slot 3) |
| 3, 5, 8 | B.ATTACK, PLANT.B, C.FLASH | `$85D9` | only if slots 1-4 are all empty; spawns `$80+w` into slot 1 |
| 6 | KNIGHT.C | `$857E` | slots 2-3 (two on screen) |
| 7 | SILVER.T | `$857A` | slots 2-3 |
| 9 | BEAT | `$85AE` | spawns Beat (`$0D`) into slot 4 if not out and energy >= 0, **and always fires a buster shot** |

`$8605`: may the player shoot in this state? (`$E130[form*8 + $94]`, negative = no). `$8615`: shot inherits
the facing, shoot-pose timers `$97` = $10, `$98` = $18.

Weapon behaviour code (all bank `$38`, header via `$EBD5`, energy via `$9E8E` on the first frame):

| Weapon | Object | Code | Notes |
|---|---|---|---|
| Y.SPEAR | `$81` | `$9AC1` | |
| W.STORM | `$82` | `$9B22` | |
| B.ATTACK | `$83` -> 4 x `$8E` | `$9B8D` / `$9C07` | four flakes, `$063B` = spread index |
| F.BLAST | `$84` | `$9C28` | |
| PLANT.B | `$85` -> 4 x `$8D` | `$9D08` / `$9D58` | leaves orbit Rockman; one hit removes all four (`$9034`) |
| KNIGHT.C | `$86` | `$9DB1` | |
| SILVER.T | `$87` | `$9E26` | |
| C.FLASH | `$88` | `$9E52` | no projectile: latches `$C4` into every class-1/3/F object, flashes, 16-frame wait |
| BEAT | `$89` / `$0D` | `$9EB8` | homes on the nearest class-1 object (`$9F71`), uses `$8FDF` like a shot |

### 3.2 Charge and adaptor physics [seen][code]

`phys.py` (Blizzard start, godmode; values per frame):

| | Normal | Jet Rockman (`$9B` = 1) | Power Rockman (`$9B` = 2) |
|---|---|---|---|
| walk | 1.297 px (`$01.4C`) | same | same |
| jump | vy0 = -4.95 px (`$FB.0C`), gravity 0.25 px/f², peak 51 px, 42 f airtime | same start, then **flight** while A is held | same as normal |
| slide (DOWN+A) | 2.5 px/f (40 px in 16 f) | none | none |
| charge `$9E` | +1 per frame; half at `$24`, full at `$5A` (= `$06AB`, 90 f) | **no charge** (always `$09`) | **+2 per frame** (full in 45 f); punch shots `$0C/$0E/$0F` |
| B weapon energy | weapons cost energy | buster only | punch only |

- **Rush Jet fuel** `$9C` [seen][code]: `$13` (19) when full. Holding A while not rising (`$05C8` >= 0) and
  `$9C` >= 0 enters flight (`$38:$8180`); `$38:$825D` takes 1 unit every 4 frames (`$9D` sub-counter), so a full
  tank flies 76 frames; at -1 flight stops (sound `$3F`) and Rockman falls. The HUD routine `$3E:$CF90` refills
  it by **1 every 2 frames whenever Rockman is not flying**, even in mid-air, so it is a stamina bar, not
  ammunition. In flight he rises (166 -> 43 px in ~50 f) and then holds height; X speed from `$38:$800F/$8012`.
- **Adaptors never use weapon energy** [seen]: all ten `$0688-$0691` stayed $1B through the Jet and Power runs.
  The Jet fuel bar is drawn in the weapon bar position when `$9B` = 1 (`$3E:$CF90`).
- **Power punch reach** [seen] (`punch.py`): the fist object appears 6 frames after B at +21 px, flies out
  at 4 px/frame to +81 px (15 frames), holds there ~10 frames and is gone 32 frames after the press; it hit a
  pinned enemy at every distance from 16 to 80 px.
- **Power punch** vs bosses: class 1, so `$12` = 2 and the full charge `$14` = 4 by the low-nibble rule; Robot
  Masters special-case `$14` to a fixed 2 and only while their AI sets `$063E` (`$31:$9AD6`); shield enemies
  (class 3) and the "punch-only" routine `$EA99` (Metall `$18`, `$15`, `$24`, `$A3`) accept only `$14`.
- Adaptor ownership is derived from boss flags (Jet = Plant Man, Power = Flame Man; `ram.md`); the menu builds
  `$0625/$0626` from them (`$38:$931D`).

---

## 4. IRQ (raster split) effects [code][seen]

### 4.1 Mechanism

- Per frame the NMI (`$3E:$C066-$C077`) copies `$0677` -> `$0676` (current handler index), writes the latch
  `$0672` to `$C000` and `$C001` (reload), and `STA $E000,Y` with Y = `$F4`, so `$F4` = 0 disables and 1 enables
  the MMC3 IRQ (`$E000`/`$E001`).
- IRQ entry `$3E:$C14C`: acknowledge (`$E000`, `$E001`), `JSR $C104` = `JMP (table $C116 + 2*$0676)`, then
  `INC $0676`. So a **chain** is a run of consecutive handlers: each one may set the next latch (`$C000`) and
  return; the next IRQ runs handler+1; the last one writes `$E000`. A handler that `DEC $0676`s repeats itself
  (per-line effects). `$C163` = delay loop (X x 5 cycles) to hide the write in h-blank.
- If the IRQ is on and the latch is below `$70`, the sound update moves from the NMI into the handlers that
  `JMP $C1D7` (`JSR $C8C1`).
- Who turns it on: screen-script inits (`$39`), a few fixed-bank routines, and every screen exit resets it
  (`$F4` = 0 in `$D6F5` path, `levels.md` section 9).

### 4.2 The 27 handlers (`$3E:$C116`, index = `$0676`)

| # | Addr | What it does | Chain start set by (latch) | Used in [seen = `$0677` observed in the tour] |
|---|---|---|---|---|
| 0 | `$C167` | `$2006` = `$0671`:00, BG pattern table `$1000`, sprites off, IRQ off | bank `$28` only (`$BE`) | the dead SOUND PLAYER only |
| 1 | `$C18C` | split at `$0673`: `$2006` = `$28E0`; next latch `$8D - $0673` | `$3E:$D4BF` (`$2F`) | Blizzard ship deck bobbing (`stages_a.md`) |
| 2 | `$C1AB` | `$2006` = `$20E0`, X scroll, sound | (chain 1) | |
| 3 | `$C1DB` | `$2006` = `$2300` (NT0 row 24), IRQ off | (chain 1) | |
| 4 | `$C1FB` | latch `$68`, X scroll = -`$F7`, other nametable, sound | `$38:$966D` (`$42`) | [guess] pause / weapon screen |
| 5 | `$C218` | restore scroll and PPUCTRL, IRQ off | (chain 4) | |
| 6 | `$C229` | latch `$AE`, X scroll `$0675`, sound | **nobody** | dead handler (5 turns the IRQ off) |
| 7 | `$C23A` | `$2006` = `$2300`, scroll 0, IRQ off: **fixed floor strip from NT0 row 24** | `$39:$855D`, `$39:$941F` (`$C1`) | Plant gorilla rooms [seen], Mr. X 2 pods, Wily 2 walker |
| 8 | `$C258` | latch `$05B4`, prepares 9 | `$3E:$D135` (`$01`) | opening story [seen: boot] |
| 9 | `$C27A` | **every line**: `$2006` = `$05C9:$05E0`, scroll 0, repeats `$0678` lines | (chain 8) | opening story |
| A | `$C2A8` | latch `$30`, nametable 1, scroll `$05E0` | `$3E:$D10F` (`$82`) | opening story [seen: boot] |
| B | `$C2BE` | nametable 0, scroll `$05F7`, IRQ off | (chain A) | |
| C | `$C2D7` | latch `$30`, X scroll = camera / 2: **parallax** | `$39:$86C4` (`$2E`) | Tomahawk desert 00-02 [seen] |
| D | `$C2F0` | X scroll = camera, IRQ off, sound | (chain C) | |
| E | `$C2FF` | scroll 0, 20 lines of wobble from `$F3` | `$39:$85E1` (`$1F`) | Tomahawk sunset 0A-0C [seen] |
| F | `$C31B` | **every 2nd line** X scroll 0/1 alternating (heat shimmer), 20 times | (chain E) | |
| 10 | `$C2F0` | = D | (chain E) | |
| 11 | `$C337` | **Knight's spike ceiling**: moves the ceiling (`$069C`, sounds `$55/$56/$57`) inside the IRQ, next latch `$B0 - $069C` | `$39:$884E` (`$B0`) | Knight 03-06 [seen, latch $71-$78] |
| 12, 13 | `$C3B8` | `$2006` = `$22E0` (row 23), IRQ off | (chains 11, 16) | |
| 14 | `$C3D8` | **Centaur's tide**: moves `$069C` and every type-`$72` object to the water line, inside the IRQ | `$39:$8A7A` (`$6D`) | Centaur 0A-0B [seen, latch $30-$37] |
| 15 | `$C453` | `$2006` = `$21E0` (row 15), IRQ off, sound | (chain 14) | |
| 16 | `$C475` | latch `$0B`, `$2006` = `$2000`, jumps the chain to `$12` | `$39:$98FC` (`$AE`) | Mr. X 4 machine (multi-split) |
| 17 | `$C48F` | latch `$6E`, X scroll `$0678`, sound | `$3B:$9D60` (`$40`) | **weapon-get screen** [seen in all 5 boss kills, latch $40] |
| 18 | `$C4A3` | scroll 0, IRQ off | (chain 17) | |
| 19 | `$C4B2` | Wily Machine floor: `$2006` = `$23xx`, scroll `$0678` (+`$0679` drift) | `$39:$9B20` (`$C1`) | Wily 4 |
| 1A | `$C4F2` | Mr. X 3 tank floor strip | `$39:$9651` (`$C1`) | Mr. X 3 |

Stages without any split [seen, other agents' per-screen scans]: Wind, Flame, Yamato, Mr. X 1, Wily 1, Wily 3; the
fortress stages use splits only in their boss rooms (`fortress.md`). Every stage effect is a special case keyed to
a screen script, and three of them (Knight, Centaur, Wily Machine floor) run game logic inside the IRQ handler.

---

## 6. Code coverage [seen]

### 6.1 Method

1. **End-of-frame PC sampling** (`e.cpu()` after every frame, as asked). This turned out to be a poor coverage
   tool: a retro frame ends just before the NMI, so in **96%** of frames the PC is in the scheduler's idle loop
   `$3E:$C581/$C583` (`LDA $F2 / BEQ`). The other 4% are lag or loading frames (OAM builder `$3F:$E2xx`, CHR
   copy `$3E:$CAFE`). It answers "where does the game overrun the frame", not "what code runs".
2. **Shadow re-execution of every frame** (new tool `tools/analysis/rm6/shadow6.py`): from each frame's
   savestate (CPU registers, 2 KB RAM, MMC3 registers) py65 re-runs the frame with MMC3 PRG banking, the scanline
   IRQ counter, NMI at vblank, the joypad, OAM-DMA timing and stubbed PPU/APU, and logs every opcode fetch and
   every ROM data read with the 8 KB bank mapped at that moment. **Fidelity check: after each shadow frame, RAM is
   compared with the real emulator's RAM; it matched byte for byte** (0 differing bytes in the 60-frame test and
   in spot checks), so the trace is the real execution. Cost ~11 ms per frame, so every frame of the tour was
   traced, not a sample.

The tour (`tour.py`, resumable, `cov/<scene>.pkl`): power-on boot through the intro and title (3,000 f), title
idle/attract (2,400), title -> stage select -> boss intro -> stage (1,500), password entry, the all-clear stage
select -> Mr. X map -> Mr. X 1, every Robot Master stage from its start, mid checkpoint and boss shutter with an
autoplayer (godmode, buster + every owned weapon cycled, all three forms), every Robot Master and fortress boss
killed (victory, weapon get, YOU GET, password, stage select, fortress maps), all 16 stages, the eight Wily 3
refights and the capsule hub, the pause menu (weapons, Jet, Power, E-tank), a death and respawn, a game over and
continue, the Mr. X reveal, the Wily Machine phase 2 and capsule kills, and the whole ending and staff roll.

(results below)

---

## 8. Lag [seen]

(results below)

---

## 5. Sound driver [code][seen]

### 5.1 Calling it

- **Request**: game code stores an id in `$DC` (`LDA #id / STA $DC`, about 200 sites); the scheduler (`$3E:$C61B`,
  at every yield) moves it into the ring `$B0-$BF` with `$C8B2` (write index `$D9`) and sets `$DC` = `$FF`.
- **Service**: `$3E:$C8C1` maps banks `$34` (`$8000`) and `$35` (`$A000`), sends every queued id to
  `$8003` (read index `$DB`), calls `$8000` once (the per-frame update), then restores `$4A/$4B/$4C`. It runs in
  the NMI (`$C0B4`) unless an IRQ split is active with a latch below `$70`; then the IRQ handler calls it
  (`$C1D7`, used by chains 2, 4, 6, `$D`/`$10`, `$15`, `$17`) so the sound update does not delay the split.
- Driver entry points (bank `$34`): `$8000` = `JMP $806C` (update), `$8003` = `JMP $80FE` (play id in A).
  Work RAM: zero page `$C0-$D8`, `$0700-$07EF` (four music channels x 4 + SFX state).

### 5.2 The track table

| Address | Content |
|---|---|
| `$34:$8A40` | **track count = `$66` (102)**; ids >= 102 and < `$F0` wrap modulo 102 (`$810D`) |
| `$34:$8A41/$8A42` | instrument table pointer, big-endian = `$8B0F`, 8 bytes per instrument (`INST n`: `$866E`) |
| `$34:$8A43` | **102 big-endian pointers** (hi, lo) |

The pointers live in a 24 KB "sound address space": `$8000-$9FFF` = bank `$34`, `$A000-$BFFF` = bank `$35`,
`$C000-$DFFF` = **bank `$36`**, which the byte reader `$803A` maps into `$A000` for the one read and then maps
`$35` back. So the music data spans three banks.

- First byte 0 = **music**: then 4 big-endian channel pointers in the order pulse 1, pulse 2, triangle,
  noise (channel X = 3..0, APU register `(3-X)*4`, `$80D8`). No DPCM. The channel data starts right after the
  9-byte header.
- First byte != 0 = **sound effect**: bits 0-6 = priority (a new SFX plays only if its priority >= the
  current one, `$8133`), bit 7 = channel flag; one register stream follows (player `$8251`).
- **Ids `$00-$22` and `$39` are music (36), `$23-$65` are SFX (65).** Ids `$F0-$F7` are commands (`$81AD`):
  `$F0` stop everything, `$F1` stop SFX, `$F2` stop music, `$F3` pause music, `$F4` resume, `$F5`/`$F6` fade
  (speed in Y) [guess for the fade direction], `$F7` = set `$D8`; `$FF` = no request.

Which id plays where (`sndcensus.py`: every id queued during the coverage tour, section 6) [seen][code]:

| Id | Where | Id | Where |
|---|---|---|---|
| 00 | Wind Man stage (`$DFA5`) | 0F | stage select |
| 01 | Blizzard Man | 10 | boss intro (silhouette on white, before every stage) |
| 02 | Yamato Man | 11 | Mr. X fortress map |
| 03 | Flame Man (`$DFA5`) | 12 | Wily fortress map |
| 04 | Plant Man (`$DFA5`) | 13 | boss defeated (`$F982`) |
| 05 | Centaur Man | 16 | weapon get (YOU GET room) |
| 06 | Tomahawk Man (`$DFA5`) | 15 | after the weapon get, before the stage select [guess: password jingle] |
| 07 | Knight Man (`$DFA5`) | 17 | Wily defeated, start of the ending |
| 08 | ending "STAFF" roll | 18 | Wily Machine (Wily 4 boss, `$FA19`) |
| 09 | Mr. X Fortress stages | 0E | CAPCOM PRESENTS; 0D "IN THE YEAR 20XX AD..." opening; 19 title |
| 0A | final credits (starfield) | 1B-22 | ending: one track per Robot Master scene (`$3B:$8D10` = `1B 21 1F 1D 22 20 1E 1C`) |
| 0B | Wily Fortress stages | 0C | fortress boss (`$FA0F`) |
| 14 | not heard in the tour [guess: game over] | 1A | **never requested**: an empty 4-channel stub (15 bytes) |

![music ids](img/engine_music_ids.png)
*90 frames after each music id was first queued in the tour (label = id, scene).*

SFX never requested by a literal `LDA #id / STA $DC` and not heard in the tour: `$3D`, `$3E`, `$4D`, `$51`
(candidates for unused effects; some ids are requested via `LDY #id / STY $DC`, e.g. `$40/$41` at
`$3E:$D522`).

### 5.3 Music command format (decoded from the channel interpreter `$34:$83CC`) [code]

A byte `>= $20` is a **note**: bits 7-5 = length index 1-7 -> 3, 6, 12, 24, 48, 96, 192 ticks (`$8923`; triplet
mode uses `$891C` = 2, 4, 8, ..., 128; dotted = x1.5), bits 4-0 = pitch (0 = rest, else semitone above the
current octave base). A byte `< $20` is a command (jump table `$84A6`); commands `$04` and up read one parameter
byte first (`$8496`):

| Cmd | Name | Params | Effect |
|---|---|---|---|
| 00 | triplet | - | toggle flag `$20` of `$0730,X` |
| 01 | tie | - | toggle `$40` (legato into the next note) |
| 02 | dot | - | next note x1.5 (flag `$10`, cleared after use) |
| 03 | octave+ | - | toggle `$08` |
| 04 | flags | 1 | `$0730 = $0730 & $97 | p` |
| 05 | tempo | 2 (hi, lo) | `$C9/$CA` (16-bit tick increment per frame) |
| 06 | gate | 1 | note-on fraction `$073C` (x note length / 256 -> `$0740`) |
| 07 | volume | 1 | `$070C` low bits |
| 08 | instrument | 1 | envelope/instrument p (table `$8B0F + 8p`) |
| 09 | octave | 1 | low 3 bits of `$0730` |
| 0A | global transpose | 1 | `$CB` |
| 0B | transpose | 1 | `$0734,X` |
| 0C | detune | 1 | `$0714,X` |
| 0D | slide | 1 | `$0718,X` (portamento speed) |
| 0E-11 | loop 1-4 | count, hi, lo | repeat: jump back count times |
| 12-15 | break 1-4 | count, hi, lo | jump out on the last pass of loop n |
| 16 | jump | hi, lo | (the end of every looping channel) |
| 17 | end | (1 ignored) | channel off |
| 18 | duty | 1 | pulse duty bits 6-7 |

Example (`songdec.py 01`), **Blizzard Man**, header `$9167` (bank `$34`): channels at `$9170` / `$9281` /
`$9394` / `$945E`, sizes 272 / 274 / 201 / 137 bytes, each ending in `JUMP`. Pulse 1 begins:
`TEMPO $0216  VOL $0B  INST $0F  FLAGS $08  GATE $E1  DUTY $C0  OCT 1  FLAGS $08  n08/24 rest/48 n11/24 rest/48
TIE n15/12 INST $13 DOT TIE n15/24 INST $0F rest/24 SLIDE $64 TIE n18/24 ...  BREAK1 x8 -> $91BB ... LOOP1 x1 ->
$917F`. The noise channel is drums as pitches (`n05`, `n10`, `n15`) with `TRIPLET` fills.

### 5.4 Free sound space [code]

Banks `$34` and `$35` have no fill at all; bank `$36` ends with **449 bytes** of fill (sound address `$DE3F-$DFFF`,
file `0x6DE4F-0x6E00F`). The driver code itself is `$34:$8000-$8A3F` (2.6 KB). Music for GP must go elsewhere:
the reader `$803A` already switches a third bank in for addresses >= `$C000`, so pointing that window at a
free bank (`$0B-$0F`) is a 2-byte change (`$8051` `LDA #$36`) that adds 8 KB; more needs a bank number per track.

---

## 7. Password system [code][seen] (codec by rm6-scout, `cheats.py pw_encode/pw_decode`)

- Grid RAM `$0300-$0323` (36 cells, A1 = `$0300`, row-major), cursor `$05B1`/`$05C8`.
- Decoder `$3F:$F3D0`: the key cells E5 (`$1C`), E6 (`$1D`), F5 (`$22`), F6 (`$23`) form a 4-bit index into
  `$F573` (16 bytes; exactly one key cell must be lit, else `$FF` = error) -> variant 0-3; `$F583[v]` = offset
  into the two 144-byte tables `$F593` (cell -> progress byte 0-3, `$FF` = not a data cell) and `$F623` (cell ->
  3-bit value); `$F587[v]` = Energy Balancer bit -> `$0696`. Each of the 4 bytes must be hit exactly once.
- Capacity: 4 variants x 4 bytes x 8 cells: **every one of the 8 x 8 x 8 x 8 x 2 = 8192 states is encodable, each
  in 2 ways** (two variants per Energy-Balancer value; the display `$3F:$F477` picks one by `$F3` bit 1, so the
  same save can show two passwords). Always exactly 5 orbs.
- Not saved: lives, E-tanks, weapon energy, fortress progress, Rush/Beat (derived from the boss bits).
- All clear with Energy Balancer: `A4 C2 C6 E4 E5` or `A6 C4 E2 E4 F6` [code, codec].

(sections 4, 6 and 8 follow)

## Lessons for Rockman 6 GP (so far)

- Enemy stats live in the 6-byte AI header, damage rules in the victim's routine. A GP rebalance edits
  three small tables (`$31:$9A45`, `$3F:$EFE4`, `$3F:$EB46-$EB75`) plus the shot bytes in the weapon AI headers.
- About 30 type ids are free (`$7B/$7C`, `$BA-$BF`, `$CE`, `$D2`, `$D7`, `$DB-$DF`, `$F5-$FF`).
- C.FLASH is coded to hurt only classes 1/3/F, and every Robot Master/fortress table gives it 0 except Wind
  Man: a GP C.FLASH needs both the class filter (`$38:$9E61`) and the tables changed.
