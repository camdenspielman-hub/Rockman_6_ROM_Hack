# Rockman 6 (J) stages, part B: Plant Man, Tomahawk Man, Wind Man, Yamato Man (rm6-stages-b)

Status: **v1, in progress** (written early per the resilience rule; bosses, alternate-exit verification and
tilesets are being added). Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text,
**[guess]** unverified.

Tools written for this (all in `build/research/rm6/rm6-stages-b/`, run from the repo root):

| Script | What it does |
|---|---|
| `lv.py` | static level decoder: layout, 32x32 blocks, 16x16 tiles, CHR-set loader, palette loader, screen scripts, renderer, collision overlay |
| `geom.py` | builds the screen graph from the screen scripts (scroll modes + exits + shutters) and renders a whole stage map (`python3 -I geom.py map 1 2 4 5`) |
| `objdump.py` | dumps every stage's object list (bank $3A) to `objlists.json` |
| `census.py` | RAM-warps to every screen, lists the spawned objects (type, HP, AI pointer), contact sheet per stage |
| `strips.py`, `sheet.py` | isolates each object type's sprite (remove-and-diff) and records a 10-frame behaviour strip; builds the enemy sheets |
| `behav.py` | 300-frame motion trace per enemy type: X/Y range, direction flips, child objects it spawns |
| `bossprep.py` | boss shutter / intro / fight savestates for the four bosses and both plate rooms |

## 1. How a stage is stored (applies to all four)

All of this was checked by rendering screens statically and comparing them with the live PPU: CHR-RAM matched
byte for byte and palettes matched on every tested screen [seen] (`t1_cmp.png`, `t2.png` in the scratch dir).

- **Per-stage table** (fixed bank $3E, indexed by `$51`) [code] $3E:$DBDB-$DC1C:

| Stage | $51 | layout bank `$6F` (at $A000) + page `$53` | tileset bank `$6E` (at $8000), 16x16 base `$63`, 32x32 base `$67` | base CHR set `$064E` | start palette id | music id (`$DC`) |
|---|---|---|---|---|---|---|
| Wind | 1 | $32, $A800 | $2C, $80, $85 | $83 | $17 | $00 |
| Plant | 2 | $32, $B000 | $2E, $92, $97 | $90 | $32 | $04 |
| Yamato | 4 | $33, $A000 | $2E, $89, $8E | $97 | $57 | $02 |
| Tomahawk | 5 | $33, $A800 | $2C, $89, $8E | $94 | $50 | $06 |

- **Layout**: 2 KB per stage = 8 rows x 256 bytes. Byte (row r, column c) at `$53+r : c`, where c =
  screen*8 + x/32. Each byte is a 32x32 block id. So a stage is a **linear strip of up to 32 screens** ($00-$1F)
  of 8x7.5 blocks; vertical sections are not stored as a grid, they are just the next screen index, and the
  screen scripts say in which direction it is entered [code] $3E:$D904, $DA6C.
- **32x32 blocks**: tileset bank, `$67<<8 + id*4`, 4 bytes (TL, TR, BL, BR) of 16x16 tile ids.
- **16x16 tiles**: five 256-byte pages at `$63`: CHR tile TL, TR, BL, BR, then an attribute byte
  (bits 0-1 palette, bits 4-7 collision type) [code] $D288-$D2E5. Wind/Tomahawk share bank $2C and Blizzard/Yamato/
  Plant share bank $2E, but each stage has its own 16x16 and 32x32 tables (3 sets per bank: $80/$85, $89/$8E, $92/$97).
- **Alternate tiles**: pages $9B-$9F of the tileset bank are a second graphics+attribute set for every tile id,
  used when the tile id's bit is set in the 256-bit array `$0340-$035F` [code] $D2B2, $DAC6. This is how
  **Power-breakable blocks disappear** (each breakable 32x32 block is made of four unique tile ids whose
  alternate is empty) and how boss shutters open (the shutter scripts set bits through `$80` and $DB98).
- **Collision** (raw nibble, remapped per stage by the 16-byte table at $3E:$DB13 selected by $DB03:
  Plant 5->$11, 13->$1F, 14->$10; Yamato/Tomahawk 5->$13, 7->$15, 9->$17, 13->$19; Wind unchanged). Odd values are
  solid (`AND #1` in the player code, $38:$8312). Seen in overlays [seen]+[code]:
  0 air, 1 solid, 3 ladder top (solid from above), 4 ladder, **$B = Power-breakable block** (also tested as $1B,
  $38:$8D67), **$A = Wind's updraft column**, $C = Wind's fan base, $F = spikes; 5/6/7/9/$D are stage-specific
  (see each stage).
- **CHR sets** (bank $37 table at $8000, 4 bytes: tile count (0 = 256), PPU dest/16, source tile index + bank)
  [code] $3E:$C95C. Each stage loads one 4 KB BG set into $0000-$0FFF at start, and screen exits / script inits
  overwrite parts of it mid-stage (table per stage below). Sprites live at $1000-$1FFF.
- **Palettes** (bank $37, or bank $28 when the stage was already cleared, `$06A0`) [code] $3E:$C9EF: pointer
  table $9000/$9100; data = start index into the `$0360` buffer, then colour bytes (bit 6 = insert a $0F first,
  bit 7 = last). They are partial updates, so a screen's palette is the start palette plus every update on the
  way.
- **Object list** (bank $3A pointer table $80BF/$80CF, four parallel arrays: screen, X, Y, type). Type `$80` =
  a **screen script** whose Y byte is the script id. Items: `$37` 1-up, `$38` small energy, `$39` large energy,
  `$49` small weapon energy, `$4A` large weapon energy, `$1D` E-tank [seen] sprites.
- **Screen scripts** (bank $39, pointer table $82EB/$836B) [code] $39:$824D: `[init hi lo] mode [per-frame hi lo]
  {exit type, CHR set, palette, [target|$80]} 0`. `mode` bit 0 = may scroll right into the next screen, bit 1 =
  may scroll left ($3E:$DCFC, $DD5A); 0 = locked screen. Exit types (handlers $39:$9A88): 1 down (to target+1),
  2 up (target+1, needs the ladder state `$94`=4 and Y < $0B), 3 down (target-1), 4 up (target-1), 5 right
  (X >= $F0, target+1), 6 left (X < $11, target-1). Target defaults to the current screen; an explicit target
  is how **branches** jump to the high screen numbers ($18-$1F) where the alternate routes live. Per-frame
  routine $8480/$848E = boss shutter 1/2; script $0A = boss room. An init routine can do anything (load CHR,
  palette, start an IRQ split, run a mid-boss and wait for it).

## 2. Plant Man (stage 2)

![Plant Man map](img/stages_b_map_plant.png)

`img/stages_b_map_plant.png`: the whole stage rendered from ROM data at 1/2 scale, screen numbers in yellow,
enemies (red) and items (green) from the object list, labelled with their type id.

### Route [code] screen graph + [seen] census

| Screens | Layout | Notes |
|---|---|---|
| 00-03 | horizontal, jungle floor (canopy, pale tree trunks, yellow bamboo pipe floor) | `$61` hovering propeller pods in the canopy, `$60` grass-hopper bugs on the floor, `$5B` falling debris; screen 03 has a **Power-breakable block** (tiles $28-$2B) and a 1-up `$37` + large energy `$39` |
| 03-05 | vertical climb up (ladders), red curtain-wood interior | `$59` the big blue armoured robot (11 HP) on 04 |
| 05-06 | horizontal at the top | `$24`/`$26` propeller lanterns, `$54` walking eye cannons |
| 06-07 | down a shaft; exit loads CHR $91 + palette $33 (**dark**) | |
| 08 | **Gorilla tank mid-boss room #1** (locked screen). Script $1C init: starts an IRQ split ($0672 = $C1, `$F4` = 1), spawns the mid-boss, waits until slot $0A is empty, then restores palette $32 (lights on) and the next exit | checkpoint: script $1C's per-frame routine `LDA #$09 / JMP $8416` = checkpoint at screen 09 (`$0684-$0686` = 09/92/32 [seen]) |
| 09-0D | horizontal, back to the jungle (exit loads CHR $92 = the jungle tiles again) | spikes, `$57` springy objects, items `$38`/`$49`/`$4A` |
| 0D-0E | exit to the right loads CHR $91 + palette $34: **gorilla mid-boss room #2** (same script $1C, same checkpoint routine) | |
| 0F-14 | horizontal jungle; script $1F at 10 loads palette $32 + CHR $BB, script $1E at 11 loads palette $35 + CHR $93 (magenta flowers, purple trunks) | stalk-and-flower platforms over a pit floor, `$5F` spring flowers, `$58` hovering eye drones, `$5A` hornets, `$62` (not seen at warp time) |
| 15-16 | boss shutters | |
| 17 | Plant Man | |

There is no alternate exit in Plant Man's stage (no branch targets in its scripts) [code].

### Enemies (object list + census) [seen]

![Plant enemies](img/stages_b_enemies_plant.png)

`img/stages_b_enemies_plant.png`: every object type spawned in the stage, isolated from a live frame (type id,
HP byte, first screen, AI bank:address). Kill rule: an object dies when its HP goes negative, so HP byte n
takes n+1 buster shots.

| Type | HP | Look / behaviour | Screens |
|---|---|---|---|
| $61 | 1 | propeller pod hiding in the canopy, swoops along the screen | 01, 0A, 0C |
| $60 | 0 | grasshopper bug, hops toward the player | 02-03, 0A-0D |
| $5B | 0 | small falling leaf/debris | 00, 03, 09, 0C |
| $59 | 11 | big blue horned armoured robot, jumps (78 px) and fires `$5D` | 04 |
| $24 / $26 | 2 / 3 | propeller lantern (body + rotor), floats down, drops `$55` balls | 05-06 |
| $54 / $55 | 2 / 2 | walking eye cannon / its blue ball shot | 05-06, 0F-15 |
| $50-$53 | 24 / 0 / 23 / 0 | **gorilla tank** mid-boss (gorilla body, tank treads, arm, head parts), throws rocks `$14` | 08, 0E (trigger `$56`) |
| $57 | 0 | yellow spring / bounce pad | 09, 0F |
| $5F | 0 | spring flower on stalk tops | 10-15 |
| $58 | 2 | hovering blue eye drone | 11-13 |
| $5A | 0 | yellow hornet | 13+ |
| $62, $70 | ? | not spawned by a warp (trigger-type objects) | 10-15, 07 |

## 3. Tomahawk Man (stage 5)

![Tomahawk map](img/stages_b_map_tomahawk.png)

`img/stages_b_map_tomahawk.png`: the whole stage at 1/2 scale with object labels. The upper-left island (18-1B)
and the lower-right rooms (1C-1F) are the branches.

### Route [code] + [seen]

| Screens | Layout | Notes |
|---|---|---|
| 00-02 | horizontal desert (red mesas, cacti, signposts, blue metal pillars) | `$6C` cowboy gunner robots (5 HP) on crates fire `$6D` bullets; screens 01 and 02 hold three **Power-breakable blocks**; an E-tank `$1D` on 02 |
| 02-04 | down a shaft | `$12` red totem walker on 04 |
| 05 | `$4F` dome dispenser on a pole (14 HP) that drops `$14` rocks / `$15` hard-hat walkers (spawner `$79`) | |
| 06-08 | horizontal cave, then up | `$6E` drill tank (4 HP), `$18` hard-hats |
| 09-0A | up (dark-blue mesh shaft) | `$70` red skull bot |
| 0A-0C | horizontal **sunset** strip (pink sky, setting sun, red rock spires) | `$67` skull walkers; checkpoint 0A/95/95 [seen]; at 0A an **up** exit (ladder at the top left) leads to the **sky branch 18-1B** |
| 0D-12 | down, right, the same dispenser `$4F` again on 10, `$13` red flying claws, `$12` totems | |
| 13 | **four-way junction**: down to 12, up to 14 (main), **right to 1D** (plate route), **left to 1C**; a Power-breakable block (tiles $28-$2B) on the left side | |
| 14-16 | up, horizontal, shutters | |
| 17 | Tomahawk Man | |
| 18-1B | sky branch: platforms `$A0` over a spike floor with bubbles `$08` rising; 1B has an E-tank, large weapon energy and large energy; its down exit drops back into 0D | |
| 1C | side room left of 13 (`$8A` object, not spawned by a warp) | |
| 1D-1F | plate route: shutters, then the second Tomahawk Man room; beating him here sets bit 2 = **B plate** | |

### Enemies [seen]

![Tomahawk enemies](img/stages_b_enemies_tomahawk.png)

`img/stages_b_enemies_tomahawk.png`: isolated sprites of every object type in the stage.

| Type | HP | Look / behaviour | Screens |
|---|---|---|---|
| $6C / $6D | 5 / 0 | green cowboy gunner on a crate, stationary, fires bullets left (every ~50 frames) | 01-03 |
| $12 | 3 | red/pink totem walker, paces back and forth | 04, 11-12 |
| $4F (+$79, $15, $14) | 14 | dome dispenser hanging on a pipe; drops hard-hat walkers `$15` and rocks `$14` | 05, 10 |
| $6E | 4 | drill tank, drives at the player | 07 |
| $18 | 0 | hard-hat (dome) turret, shoots `$14` | 08 |
| $70 | 3 | red skull bot, stationary | 09 |
| $67 | 1 | skull walker, hops (37 px) | 0B-0C, 14-15 |
| $59 | 11 | the same big blue horned robot as Plant/Wind | 0F |
| $13 | 3 | red flying claw, drops `$14` | 11-12 |
| $64/$66 (+$A4) | 0 | propeller drones over the sunset, drop `$A4` | 15 |
| $A0 | 0 | small yellow lift platform in the sky branch, bobs up/down | 18-1B |
| $08 | 0 | rising white bubble (sky branch hazard) | 18-1D |

## 4. Wind Man (stage 1)

![Wind map](img/stages_b_map_wind.png)

`img/stages_b_map_wind.png`: the whole stage at 1/2 scale with object labels.

### Route [code] + [seen]

| Screens | Layout | Notes |
|---|---|---|
| 00 | sky, girders on golden pillars | |
| 01-05 | **climb up a green tower shaft** (4 screens of ladders), exit to 02 loads CHR $8C | `$27` white panda robots on drums (5 HP) throw balls `$28`; `$29` crawling blue tank; screen 03 has a **Power-breakable block** |
| 05-07 | horizontal at the top (sky): **updraft columns** (collision $A above fans $C) carry the player up; ceiling spikes on 07 | `$1B` green propeller bombers drop `$1C` red balls; `$36` hovering spinning tops; `$2D` spiked stompers on girders |
| 07-0A | exit right loads CHR $8D (checkpoint 08/8D/17 [seen]); open sky with `$34` flying shield-cars | |
| 0A-0D | climb, then right | `$75` beetle walker, 1-up |
| 0E-12 | second tower: down through it; CHR $83, then $8E + palette $87 (dark tower base with stars) | `$59` big blue robot on 0E |
| 12-14 | up, shutters | |
| 15 | Wind Man | |

There is no alternate exit in Wind Man's stage [code].

### Enemies [seen]

![Wind enemies](img/stages_b_enemies_wind.png)

`img/stages_b_enemies_wind.png`: isolated sprites of every object type in the stage.

| Type | HP | Look / behaviour | Screens |
|---|---|---|---|
| $27 / $28 | 5 / 3 | white panda robot on a red drum, throws a ball | 01, 03, 0C-0D, 10, 12 |
| $29 | 2 | blue crawler tank, patrols 40 px | 02, 0F |
| $1B / $1C | 2 / 0 | green propeller bomber, bobs (±24 px), drops red balls | 04, 06 |
| $36 | 2 | hovering spinning top / propeller mine | 04-07, 0A, 11-12 |
| $2D | 0 | spiked stomper sliding on girders | 05-07 |
| $34 | 2 | flying shield-car | 08-0A |
| $75 | 2 | beetle walker | 0B |
| $59 | 11 | big blue horned robot | 0E |

## 5. Yamato Man (stage 4)

![Yamato map](img/stages_b_map_yamato.png)

`img/stages_b_map_yamato.png`: the whole stage at 1/2 scale with object labels. The top-right strip (18-1D) is
the plate route.

### Route [code] + [seen]

| Screens | Layout | Notes |
|---|---|---|
| 00-02 | Mt. Fuji backdrop over a Japanese-castle cityscape, then red metal castle walls on green | `$C2` lantern robots (3 HP) |
| 02 | junction: **up** (ladder) to 03 (main) or **right** to 0C, behind a **Power-breakable block** (tiles $38-$3B) | |
| 03-08 | up, horizontal through rooms with shoji screens, then down | `$A2` samurai spear robot (11 HP) throwing spears `$A3`; `$69` hopping shuriken robots |
| 09 | exit right (to 0A) or down to 0F | checkpoint routine at 09 sets 0A |
| 0A-0B | horizontal | |
| 0B | junction: **up** to 18 (plate route) or **down** to 10 (main) | |
| 0C-0F | lower branch from 02: 0E is a **dark mid-boss room** (script $37 init) with the `$D0`-`$D8` mid-boss; 0F has an E-tank and a breakable block, its up exit returns to 09 | |
| 10-14 | main route: down, right, up, up (`$54` eye cannons, `$5F`/`$5E` springs, `$24`/`$26` lanterns, `$13` claws) | |
| 15-17 | shutters, Yamato Man (room 17) | |
| 18-1D | plate route: up from 0B, `$75` beetle, `$A2` samurai, `$A7` spring-necked robots; shutters 1B/1C; second Yamato Man room 1D = **E plate** | |

### Enemies [seen]

![Yamato enemies](img/stages_b_enemies_yamato.png)

`img/stages_b_enemies_yamato.png`: isolated sprites of every object type in the stage.

| Type | HP | Look / behaviour | Screens |
|---|---|---|---|
| $C2 (+$C3, $17) | 3 | hooded lantern robot, throws fire | 01-02, 0B |
| $A2 / $A3 | 11 / 15 | samurai robot with a spear / its thrown spear | 03, 0C, 15, 19 |
| $69 / $6B | 1 / 0 | small hopping robot / its shuriken | 04-06 |
| $25 | 0 | white bubble cluster | 05 |
| $D0 $D1 $D2 $D8 | 14, 127, 0, 15 | dark-room mid-boss (green dragon-like tank with a rider; $D1 is an invulnerable part, $D8 its shot) | 0E |
| $54 / $55, $5F | 2 / 2, 0 | eye cannon + ball, spring flower | 10-11 |
| $24 / $26 | 2 / 3 | propeller lantern | 12 |
| $13 / $14 | 3 / 0 | red flying claw, drops rocks | 13-14 |
| $75 | 2 | beetle walker | 18 |
| $A7 | 2 | spring-necked robot, bounces 48 px | 1A-1B |

## (sections still to come: bosses with damage tables, verified alternate exits, tilesets/CHR renders, IRQ
effects, lessons)
