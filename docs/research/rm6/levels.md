# Rockman 6 (J) level data format (rm6-levels)

Status: **v2, complete**: decoder, encoder, byte-exact round trip (bank level and JSON level, plus an edited
ROM played in the emulator), screen graph, full maps of all 16 stages from ROM data alone, and two emulator
validations (61 savestates; a graph-driven tour of 319 screen arrivals).
Tags: **[seen]** emulator, **[code]** disassembly / ROM data, **[guess]** unverified.

- Extractor: **`tools/analysis/rm6/levels.py`** (decode, encode, walk, render, export). Commands:
  `info [stage]`, `roundtrip`, `maps [stage...]`, `strips [stage...]`, `appendix`, `json <dir>`. Run from
  the repo root with `python3 -I`.
- Scratch: `build/research/rm6/rm6-levels/`: `validate.py` (savestate PPU comparison), `tour.py`
  (graph-driven emulator tour), `edit_test.py` (edited-ROM test), `anatomy.py`, logs `validate_final.txt`,
  `tour_<nn>.txt`, `tour_all.log`, JSON exports `json/`, raw 32-screen strips `strip_*.png`.
- Generated companion: **`docs/research/rm6/levels_stages.md`**: every stage screen by screen (map position,
  entry, script, exits, BG CHR sets, palette, objects, sprite CHR sets) and its object types (AI, CHR, HP).
- Maps: `docs/research/rm6/img/maps/<nn>_<stage>.png`, one per stage, rendered **from ROM data alone**.
- Builds on the decoders of rm6-stages-a (`rm6_stagemap.py`, `stages_a.md` section 0) and rm6-stages-b
  (`rm6_level.py`, `stages_b.md` section 1). New here: the byte-level spec for all 16 stages, the fixed-bank
  screen scripts (the boss-room script lives at `$3F:$F947`; `rm6_stagemap.py` / `rm6_level.py` read that
  address from bank $3A and got `FF FF FF`, which is where the "mode $FF = boss room" in `stages_a.md` /
  `stages_b.md` comes from: the real script is `F9 4A 00` = init `$F94A`, mode 0),
  init / per-frame routine effects, teleports, the encoder and the round trip, the unused data.

## 0. The pipeline in one picture

```
stage id $51 --$3E:$DF25..$DFB4--> layout bank/page, tileset bank/pages, BG CHR set, palette, music
layout (8 rows x 256 cols, 1 byte = 32x32 block id; col = screen*8 + x/32)
  -> block (4 metatile ids TL TR BL BR)            tileset bank, pages $67..$67+3 (interleaved by 4)
    -> metatile (4 CHR tile ids + attribute)       tileset bank, pages $63..$63+4 ; alt set $9B-$9F
       attribute: bits 0-1 BG palette, bits 4-7 collision type (remapped per stage group $3E:$DB03/$DB13)
CHR-RAM  <- base BG set $064E, + extra BG set $064F from exits/inits, + sprite sets per enemy type
palette  <- start id, then partial updates from exits / inits / per-frame routines (cumulative buffer $0360)
object list (bank $3A): screen, X, Y, type ; type $80 = screen script (Y = script id, bank $39)
screen script: [init] mode [per-frame] {exit: type, CHR set, palette, [target]}... 0
```

## 1. Per-stage table (fixed bank $3E, 9 tables x 16 bytes at $DF25-$DFB4, indexed by `$51`) [code]

Stage init `$3E:$DBDB` (A = stage id): `$51` = id, `$063D` = id & 7, far call `$3A` function 2 (object list
init, section 8), palette `$DF95,Y` via `$C9EF`, music `$DFA5,Y` -> `$DC`, player HP `$03E5` = $1B, then copies
the tables below to zero page; `$57` = checkpoint screen `$0684`; far call `$3A` function 6 (object window +
sprite CHR for that screen); `$DC6A` loads CHR sets `$064E` and `$064F` and paints 30 rows of the screen.

| Table | RAM | Meaning |
|---|---|---|
| $DF25 | `$6F` | layout bank (8 KB, mapped at $A000) |
| $DF35 / $DF45 | `$52` / `$53` | layout base lo / page (lo is always 0) |
| $DF55 | `$6E` | tileset bank (8 KB, mapped at $8000): metatiles and blocks |
| $DF65 | `$63` | first of 5 metatile pages (TL, TR, BL, BR tile, attribute) |
| $DF75 | `$67` | first of 4 block pages (always `$63` + 5) |
| $DF85 | `$064E` | base BG CHR set id (bank $37 table, section 6) |
| $DF95 | `$069E` | start palette id (section 7) |
| $DFA5 | `$DC` | music id (sound request, see section 11) |

```
id  stage     L6F P53 T6E P63 P67 CHR PAL MUS  coll.group ($DB03)
 0  Blizzard  32  A0  2E  80  85  82  15  01   0
 1  Wind      32  A8  2C  80  85  83  17  00   0
 2  Plant     32  B0  2E  92  97  90  32  04   1
 3  Flame     32  B8  2F  80  85  86  1E  03   0
 4  Yamato    33  A0  2E  89  8E  97  57  02   2
 5  Tomahawk  33  A8  2C  89  8E  94  50  06   0
 6  Knight    33  B0  2D  80  85  9E  74  07   2
 7  Centaur   33  B8  2D  89  8E  AA  A6  05   0
 8  Mr.X 1    26  A0  2C  92  97  9D  68  09   3
 9  Mr.X 2    26  A8  2F  89  8E  A4  88  09   3
10  Mr.X 3    26  B0  2F  92  97  B1  AB  09   3
11  Mr.X 4    26  B8  2B  80  85  C3  C8  09   3
12  Wily 1    27  A0  2A  80  85  89  7C  0B   0
13  Wily 2    27  A8  2A  89  8E  A2  89  0B   0
14  Wily 3    27  B0  2A  92  97  A2  96  0B   1
15  Wily 4    27  B8  2B  89  8E  BA  18  0B   0
```

## 2. Where the level data lives (bank map) [code]

| Bank(s) | File offset | Content |
|---|---|---|
| $26, $27, $32, $33 | 0x4C010, 0x4E010, 0x64010, 0x66010 | layouts, 4 stages x 2 KB per bank (pages $A0/$A8/$B0/$B8). The whole 32 KB is layout data |
| $2A-$2F | 0x54010-0x5FFFF | tilesets: 3 slots of 9 pages ($80, $89, $92: 5 metatile pages + 4 block pages) + one shared alternate metatile set ($9B-$9F) per bank. **Slots $2B:$92 and $2D:$92 are unused** (Capcom $FF/$00 fill, 2 x 2304 bytes) |
| $37 | 0x6E010 | CHR set table $8000-$83FF (256 x 4), palette pointers $9000/$9100, palette programs $9200-$988B+ |
| $28 | 0x50010 | the same palette pointer table layout, used instead of bank $37 when `$06A0` != 0 (stage revisited) |
| $3A | 0x74010 | object list pointers $80BF/$80CF, counts $80DF, lists $85D8-$95D3; object type tables $82C9/$83C9/$84C9 (AI lo/hi/bank), $85C9 (sprite bank by type >> 4); spawner code |
| $39 (+$3A at $A000) | 0x72010 | screen-script pointers $82EB/$836B (128 entries), script bodies $83EB-..., script init / per-frame routines, exit handler table $9A88/$9A8F |
| $3E (fixed) | 0x7C010 | stage table, stage init, painters $D1FF/$D322, address maths $D8AF/$D904, collision $DA6C, exit handlers $D540-$D6B3, screen transitions $D720-$D8AE |
| $3F (fixed) | 0x7E010 | boss-room script `S0A` at $F947 (init $F94A) |
| $10-$1F, $0A | 0x20010-0x4000F, 0x14010 | BG CHR source data (uncompressed 2bpp; every BG set of the CHR set table points here) |
| $00-$0A, $10 | 0x00010-0x1600F | sprite CHR source data |

## 3. Layout [code][seen]

- 2 KB per stage = 8 rows x 256 columns. Byte for block row `r` (0-7, 32 px each) and column `c` is at
  `layout_bank : ($53 + r) << 8 | ($52 + c)`. **Column = screen * 8 + x / 32**, so a stage is a strip of
  **32 screens of 8 x 8 blocks** (only 7.5 rows show: the bottom 16 px of row 7 are never on screen).
- The address maths (`$3E:$D904`) adds the X screen `$4F` and the Y screen `$50` before forming the column,
  so **vertical sections are not a second dimension**: going up or down just moves to another screen index.
  The 2-D map shape exists only in the screen scripts (section 9).
- No compression anywhere: layouts, blocks, metatiles and CHR are raw tables.
- Wily 4 uses 7 screens and Mr. X 2 / 3 use 18; unused screens are block 0, except a few exact copies of
  used screens (section 16).

## 4. Blocks, metatiles, the alternate set, attributes [code][seen]

- **Block** (32x32): 4 metatile ids TL, TR, BL, BR at `tile_bank : ($67 << 8) + id * 4 + q` (256 blocks fill
  the 4 pages).
- **Metatile** (16x16): CHR tile ids TL, TR, BL, BR at pages `$63`, `$63+1`, `$63+2`, `$63+3` (offset = id), and
  the **attribute byte** at page `$63+4`: bits 0-1 = BG palette, bits 2-3 unused (0 in every stage), bits 4-7 =
  collision type. The painter (`$3E:$D1FF` columns, `$D322` rows) builds the nametable and the attribute
  table from these bytes.
- **Alternate set** at pages `$9B-$9F` of the same tileset bank (shared by the 3 stages in the bank): a
  metatile id whose bit is set in the 256-bit field `$0340-$035F` (byte id >> 3, mask `$DFB5[id & 7]`) is drawn
  and collided from the alternate pages instead ([code] `$D2B2`, `$DAC6`). Breakable blocks and some shutters
  use it (rm6-stages-b saw the Power punch set bits $38-$3B on Yamato 02). The static maps draw the normal set.
- **Closed boss shutters** are not metatiles: the shutter code writes tiles $1E/$1F straight into the
  nametable over the 16-px column at the room's left edge, rows 12-19 [seen] (the only 16 nametable cells
  that differ from the static render in every boss-room state).

### Collision types (attribute high nibble) [code][seen]

The value is remapped by group: `type' = $DB13[group * 16 + type]`, group = `$DB03[stage]`. Odd = solid
(`AND #1`). Group 0 is the identity; the others:

| group (stages) | remapped types |
|---|---|
| 0 Blizzard, Wind, Flame, Tomahawk, Centaur, Wily 1/2/4 | none |
| 1 Plant, Wily 3 | 5 -> $11, $D -> $1F, $E -> $10 |
| 2 Yamato, Knight | 5 -> $13, 7 -> $15, 9 -> $17, $D -> $19 |
| 3 Mr. X 1-4 | 5 -> $1D, 9 -> $01, $D -> $1B |

Meanings (from rm6-stages-a/b and the code they cite): 0 air, 1 solid, 3 ladder top, 4 ladder, 8 water
(Centaur), $A updraft (Wind), $B breakable by the Power punch, $D destroyed by Flame Blast, $F deadly
(spikes / pits); 2/6/9 Flame's oil; 5/7 and the remapped values $1x are stage specials (ice, conveyors,
spike beds: the type is the index into the player's floor handler table). Collision types used per stage
are in the summary table (section 13).

## 5. How the game paints a screen [code]

`$D8AF` turns the paint cursor (`$4D` X, `$4E` Y) into a nametable address (`$5C/$5D`) and an attribute
address (`$5E/$5F` = `$23C0 | ...`); `$D904` forms the layout pointer `$54/$55` (see section 3); `$D1FF`
paints one 8-px-wide column (both banks mapped: `$6E` at $8000, `$6F` at $A000) into the `$0300` buffer that
the NMI uploads (`$60` = $68 request), `$D322` does the same for a row, `$DA6C` reads the collision of a point.
Stage init paints 30 rows (`$DC91`: `$07` = $1E loops of `$D1FF`). Horizontal scrolling paints a new column
every 8 px ($DCE2 right, $DD42 left); vertical transitions repaint row by row while `$58` scrolls.

## 6. CHR: what is uploaded where [code][seen]

- **CHR set table** `$37:$8000 + id * 4`: `count` (0 = 256 tiles), `ppu/16` (low byte), `src/16`,
  `flags` (bit 7 = PPU +$1000, bits 1-6 = 8 KB source bank, bit 0 = source +$1000). The source is read with
  `bank` at $8000 and `bank+1` at $A000, so a set may run into the next bank. Loader: `$C95C` (decode) +
  `$CAA4` (copy now if rendering is off, else queue into the 8-entry ring `$07F0`, written by the NMI).
  `levels.chr_set(id)` / `levels.chr_ram([ids])`.
- **BG** = pattern table $0000 (PPUCTRL $88 in stages [seen]). Every stage loads one 256-tile base set
  (`$064E`, ids $82-$C3 above) and then extra sets that overwrite parts of it: `$064F`, set by exits (the
  exit's CHR byte, when negative for type 5 exits) and by script inits. Checkpoints save `$064F`
  (`$0685`), so a respawn reloads base + one extra set.
- **Sprites** ($1000-$1FFF): every object type's AI routine is preceded by a **6-byte header** read by
  `$3E:$EBD5` (the `JSR $EBD5` most AIs start with): `AI-6` -> `$E526` (animation / sprite id [guess]), `AI-5` sprite
  palette id (`$C9EF`, 0 = none; programs start at index $18/$19, never in the BG half), **`AI-4` CHR set id**,
  `AI-3` -> `$059A` (hitbox [guess]), **`AI-2` HP** (`$03E5`; matches the live spawn HP for 91 of 99 types the
  census of rm6-stages-a saw, the 8 others are child objects that set their own), `AI-1` -> `$0583` (flags).
  When the camera enters a screen, `$3A` function 5
  (`$826F`) walks the object list for that screen and queues the CHR set of each type not in the
  "recently loaded" list `$07E8-$07EF` (8 entries). So the sprite CHR upload list of a screen is
  `{ai(type).chr for the objects on it}` (`levels.ai(t)`). Items have CHR 0 (resident tiles).
  Exits whose CHR byte is a sprite-area set (e.g. `$61` in the `right/61` exits before boss doors) preload
  sprite tiles the same way.
- **Animated BG tiles**: some stages rewrite 4-8 BG tiles at run time [seen: the only CHR mismatches in
  section 15]: Centaur's water ($DC-$DF, $E8-$EF), Mr. X 3 ($F0-$F3), Knight (per-frame `$39:$888A` loads CHR
  sets $9F, $A0, $A1 in turn every 4 frames), Yamato's plate route (init `$39:$87A6` starts thread 7,
  `$39:$87B0`, cycling sets $9A-$9C), Wily 3's water. The maps show the base tiles.

## 7. Palettes [code][seen]

- Pointer table `$9000 + id` (lo) / `$9100 + id` (hi) in bank $37 (bank $28 if `$06A0` != 0: the revisit
  palettes; 2014 of 4096 bytes differ). Program: start index into the 32-byte buffer `$0360`, then colour
  bytes: bit 6 = write `$0F` first, bit 7 = last byte. Loader `$3E:$C9EF`; `$39:$8110/$8114` = load + fade in.
- They are **partial updates**: a screen's palette is the start palette plus every update on the way there,
  in route order (`levels.walk` carries the 32-byte buffer along each edge).
- Palette changes come from: exits (the exit's palette byte: types 1/3 apply a negative id before the
  scroll and every id after it; types 2/4/6 apply it before; type 5 applies a positive id before and a
  negative one after), script inits,
  per-frame routines (often only "when the camera is on screen n" or "when the camera stops"), spawned
  bosses (fortress boss AIs load the room palette with `$8110`), and **effect threads** started by
  `LDX #n / JSR $C5C7` (many are palette cyclers: Flame's oil, Tomahawk's sunset, Mr. X 3). The maps show
  the first frame of a cycle.

## 8. Object lists (enemy / item / script placement) [code][seen]

- Pointer `$3A:$80BF[s]` (lo) / `$80CF[s]` (hi), count `n = $80DF[s]`. At the pointer: **4 parallel arrays
  of n bytes, each preceded by a sentinel byte**: `[S] screen[n] [S] X[n] [S] Y[n] [S] type[n]`
  (4 + 4n bytes; the sentinel is $FF, except the very first byte of stage 0's list, $24, which no code
  reads; after stage 15: $FF fill). The arrays are sorted by (screen, X).
- Init (`$3A:$8032`, function 2): zero-page pointers `$74` screen, `$78` X, `$7C` Y, `$7E` type and
  `$76`/`$7A` (= the screen and X arrays offset by -1, for the backward scan); window indices `$0649`/`$064A`.
- Spawner (`$3A:$8120`, function 0, every frame): moving right, every entry with `(screen, X) <=
  camera + $FE` is spawned and `$0649` advances; moving left, entries at `camera + 8` or later scroll back in
  ($064A). An entry is skipped if its bit in the **kill bitfield `$0650+`** (by list index) is set, so
  defeated objects and taken items do not respawn until the field is cleared. The spawned object gets
  X screen = list screen, X = list X, Y = list Y, `$03FC` = list index, AI from the type tables, and HP
  from the AI header. Type `$80` always goes to **slot 22** (`$16`): one active screen script at a time.
  The kill field is 32 bytes (`$0650-$066F`, cleared with the alternate-tile field `$0340` by `$3E:$CE44`;
  bits set by `$3F:$ED30`), so a list may hold up to 256 objects.
- After a transition that leaves `$70` = 2 (left exits, and the "back" exits 3/4), function 6 starts the
  window at the first object of screen + 1: the arrival screen's own objects (and its script) spawn only once
  the camera moves [code `$3A:$8250`][seen: Yamato 1A -> 13 keeps palette $5E until the camera scrolls].
- Item types [seen] (rm6-stages-a/b): $37 1-up, $38/$39 small/large life energy, $49/$4A small/large weapon
  energy, $1D E-tank, $8A Energy Balancer. The maps label them `1UP e E w W ET BAL`; other types are shown as
  their hex id (look them up in `stages_a.md`, `stages_b.md`, `fortress.md`).

## 9. Screen scripts (scroll and transition rules) [code][seen]

The type-$80 object's Y byte is a script id (0-$7F). Pointer `$39:$82EB[id]` (lo) / `$836B[id]` (hi); the
pointer can be in the fixed banks (script $0A, the Robot Master boss room, is at `$3F:$F947`; fortress boss
rooms have scripts of their own, e.g. Mr. X 2 $6F, Wily 1 $67, whose inits spawn the boss into slot 8).
Interpreter `$39:$824D` (it runs as the object's thread):

```
if b0 & $80:  init_hi init_lo mode   ; JSR init (runs once). If init never returns (JMP $E45A), nothing follows
else:         mode
pf_hi pf_lo                         ; per-frame routine, pf_hi = 0: none
{ type chr pal [$80|target] }...    ; exits, checked every frame before pf; type 1-6
0 (or any byte >= $80)              ; end of the list
```

- **mode** -> `$71`. Bit 0 = the camera may scroll right across this screen's right edge (into screen+1),
  bit 1 = it may scroll left across the left edge (into screen-1); 0 = locked ([code] `$DCFC`: with bit 0
  clear a scroll that crosses into the next screen by less than 16 px snaps back; `$DD5A` the same leftwards).
  When the script object despawns (it scrolled off), `$71` becomes 3, so screens without a script of their
  own scroll freely. The usual pattern is mode 1 at X=$40 on the first screen of a horizontal run, mode 2 at
  X=$C0 on the last one, mode 0 on shaft screens.
- **exits** (handlers `$39:$9A88/$9A8F` -> `$3E`):

| type | handler | fires when | camera goes to |
|---|---|---|---|
| 1 down | `$D587` | player Y >= $E3 | target + 1, scrolled in from below (`$D7B3`) |
| 2 up | `$D612` | ladder state `$94` = 4 and Y < $0B | target + 1, from above (`$D82D`) |
| 3 down | `$D540` | Y >= $E3 | target - 1, from below (`$D7F0`) |
| 4 up | `$D5D1` | ladder and Y < $0B | target - 1, from above (`$D872`) |
| 5 right | `$D653` | player X >= $F0 | target + 1, 256-px scroll right (`$D720`) |
| 6 left | `$D6B3` | player X < $11 | target - 1, scroll left (`$D75F`) |

  `target` defaults to the current camera screen `$57`; an explicit target (byte with bit 7) is how branches
  jump to the alternate-route screens $18-$1F and back. Every exit kills the objects (`$D6F5`), resets the
  IRQ split (`$F4` = 0), loads the CHR set (`$73` -> `$064F` + `$CAAA`) and the palette (`$72`), stores the
  palette id in `$0687`, and re-initialises the object window for the new screen (`$D716` -> `$3A`
  function 6, which also queues its sprite CHR).
- **Common per-frame routines**: `LDA #s / JMP $8416` = set the checkpoint to screen s when the camera is
  on it (`$841A` unconditional); `$8480` / `$848E` = boss shutter 1 / 2 (opens, walks the player through,
  scrolls to screen + 1); script `$0A` (init `$3F:$F94A`) = Robot Master boss room (boss intro, victory jingle
  $13, then the weapon get or the stage clear).
- **Init routines** do anything: load CHR / palettes, start an IRQ split or an effect thread, spawn a
  mid-boss and wait (Plant `$8551` spawns the gorilla tank, type $50, into slot 8 and loops until `$03A8` = 0;
  `JMP $827C` then resumes the interpreter = "returns"), or replace the exit list with their own logic
  (Flame screen 0C's init loads palette $1F, runs its own down exit with CHR $87, and only if the script
  scrolls away instead loads palette $1E). An exit never ends the old script cleanly: `$D6F5` clears slots
  1-21 and the new screen's script overwrites slot 22, so code after an init's exit loop runs only when the
  script object scrolls off.
- **Teleports**: `$39:$89F5` (`STA $57 / STA $046F / JMP $D716`) jumps straight to a screen: Wily 3 screen 07
  -> 08 (the capsule hub); the hub's per-frame routine `$39:$8E3B` sends teleporter k to boss id `$8ED2[k]`
  = 4 0 2 3 6 7 1 5, screen `9 + id` (09 Blizzard, 0A Wind, 0B Plant, 0C Flame, 0D Yamato, 0E Tomahawk,
  0F Knight, 10 Centaur: the refight rooms), palette `$9A + id`; the ninth capsule ends the stage (`$F0` = 1).
  Wily 4 screen 03 reuses Tomahawk's dome mid-boss routine (`$39:$8FBC` sets its parameters and jumps to
  `$861B`).

## 10. The screen graph used for the maps (`levels.walk`) [code]

BFS from screen 0 with the start CHR set and palette. A screen's script gives its mode, exits and init /
per-frame effects (`screen_effects`, a small static tracer over the init and per-frame code: palette, CHR,
mode, exit-handler calls, checkpoint, teleports, spawned bosses). Edges: scroll right (mode bit 0) to
screen+1 at x+1, scroll left (bit 1) to screen-1 at x-1, exits (direction and target as in section 9),
shutters to screen+1 at x+1, teleports (own component). **Forward edges are taken before back edges** (exit
types 3/4/6 without a target, scroll left), so each screen is placed where the player first reaches it;
a screen that would land on an occupied cell starts a new component (only Wily 3 needs this: the 8
teleport rooms). Every screen that holds an object is reached in all 16 stages (Tomahawk: all 32).
Effects an init applies after its own exit loop are carried only along scroll edges (section 9). Effect
threads that are bank-$3B palette cyclers (`levels.thread_palettes(n)`: `LDY #i / BNE $911C`, data
`$3B:$9143+i` = delay, palette ids, 0 = loop, $FF = end) contribute their first palette. The result is a
consistent 2-D picture: of the 586 edges between placed screens, all agree with the placement except 6
back exits of the **shared shaft scripts** $02 (down + up\*) and $07 (down\* + up), reused on screens that
are entered sideways (Wind 0E, Tomahawk 0D, Knight 07, Centaur 09 / 0E, Wily 1 14): the script offers the
exit but the room has no ladder or pit there [guess from the maps], so the walker never needed a component
for a real overlap.

## 11. Music ids [code]

`$DFA5`: 00 Wind, 01 Blizzard, 02 Yamato, 03 Flame, 04 Plant, 05 Centaur, 06 Tomahawk, 07 Knight, 09 every
Mr. X stage, 0B every Wily stage. Boss rooms request $0C (fortress boss, $FA0F; $18 in Wily 4), $13 after a
Robot Master dies (`$F982`). Wily 3's refight rooms play $0C (`$39:$8EE7`).

## 12. Maps (from ROM data alone)

All in `docs/research/rm6/img/maps/` (each < 1 MB, full resolution: 256 x 240 px per screen). Labels: screen
number and how it was entered, `Sxx` = screen script id at its X position, object types as hex, items as
`1UP e E w W ET BAL`. Each screen uses the CHR sets and palette `walk()` computed for it (section 10), so
dark rooms, CHR swaps (Flame's oil field, Wind's tower interiors) and per-room palettes are reproduced.

- `00_blizzard.png` Blizzard Man; `01_wind.png` Wind Man; `02_plant.png` Plant Man; `03_flame.png` Flame Man
- `04_yamato.png` Yamato Man (with the E-plate route 18-1D and the lower bypass 0C-0F)
- `05_tomahawk.png` Tomahawk Man (all 32 screens: B-plate room, Energy Balancer room, sky bypass)
- `06_knight.png` Knight Man; `07_centaur.png` Centaur Man
- `08_mrx1.png` - `11_mrx4.png` Mr. X Fortress 1-4; `12_wily1.png` - `15_wily4.png` Wily Fortress 1-4
  (Wily 3: main route, capsule hub and the 8 refight rooms as separate panels)

Other images:

- `img/levels_anatomy.png`: Yamato Man screen 02 as stored: the static render, the 64 layout bytes (32x32
  block ids), the 256 metatile ids those blocks expand to, and the collision nibbles (B = breakable by the
  Power punch: the entrance of the lower bypass).
- `img/levels_edit_test.png`: the editor round trip in the game: left the original ROM, right a ROM rebuilt
  from edited JSON (a 3-block platform and a new 1-up object added to Blizzard Man screen 00).

## 13. Stage summary [code]

Counted over the screens the walker reaches plus every screen with objects.

| id | stage | screens used / 32 | blocks used / 256 | metatiles used / 256 | objects (types) | scripts | collision types | BG CHR sets | palette ids |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Blizzard Man | 25 | 255 | 245 | 57 (15) | 14 | 0 1 3 4 5 6 7 B D F | 82 84 85 | 15 1A 1C |
| 1 | Wind Man | 22 | 232 | 194 | 50 (13) | 19 | 0 1 3 4 A B C F | 83 8C 8D 8E | 17 3D 87 |
| 2 | Plant Man | 24 | 255 | 197 | 77 (17) | 16 | 0 1 3 4 5 6 7 B F | 90 91 92 93 BB | 32 33 35 |
| 3 | Flame Man | 24 | 254 | 178 | 52 (13) | 10 | 0 1 2 3 4 6 7 9 B F | 86 87 | 1F 22 |
| 4 | Yamato Man | 30 | 255 | 221 | 40 (16) | 28 | 0 1 3 4 9 B D F | 97 98 99 | 57 58 59 5A 5B 5C 5D 5E B9 |
| 5 | Tomahawk Man | 32 | 221 | 212 | 44 (18) | 27 | 0 1 3 4 B F | 94 95 96 | 50 51 53 95 |
| 6 | Knight Man | 27 | 255 | 155 | 32 (14) | 22 | 0 1 3 4 5 7 B D F | 9E | 74 75 78 7B 82 CD |
| 7 | Centaur Man | 27 | 250 | 176 | 48 (11) | 20 | 0 1 3 4 8 F | AA | A6 A7 A8 A9 AA CA |
| 8 | Mr. X Fortress 1 | 22 | 249 | 198 | 48 (14) | 17 | 0 1 3 4 6 7 B D F | 9D B9 D7 | 68 6C 6F DF |
| 9 | Mr. X Fortress 2 | 18 | 234 | 170 | 30 (7) | 12 | 0 1 5 6 7 F | A4 B3 B8 | 88 B9 BF |
| 10 | Mr. X Fortress 3 | 18 | 256 | 169 | 72 (10) | 13 | 0 1 3 4 B F | B1 | AC BC D0 |
| 11 | Mr. X Fortress 4 | 25 | 159 | 165 | 62 (15) | 15 | 0 1 3 4 9 B F | C3 C4 D2 | C8 C9 D0 |
| 12 | Wily Fortress 1 | 24 | 255 | 223 | 50 (17) | 23 | 0 1 3 4 6 7 A B C E F | 89 8B | 7C 7F 80 81 B9 |
| 13 | Wily Fortress 2 | 19 | 232 | 120 | 41 (8) | 12 | 0 1 3 4 5 B D F | A2 A3 B2 | 79 89 B8 B9 |
| 14 | Wily Fortress 3 | 17 | 251 | 151 | 31 (9) | 13 | 0 1 3 4 6 7 8 D E F | A2 A8 A9 | 96 97 9A-A1 |
| 15 | Wily Fortress 4 | 7 | 177 | 130 | 5 (5) | 7 | 0 1 6 7 | BA BC BD BE | 18 3E CC D0 |

(BG CHR sets: only ids >= $80; the sprite-area sets that some exits preload, $55-$72, are omitted.
Collision types before the group remap.) **The 32x32 block table is full or nearly full in 11 of 16
stages**; metatiles have more room (120-245 used).

## 14. Round trip (re-encoding reproduces the ROM) [code][seen]

`python3 -I tools/analysis/rm6/levels.py roundtrip` (exit code 0 = all identical) does two things:

1. **Bank level**: decode every structure, re-encode it from the decoded form (layouts from 32 x 8 x 8 block
   grids, metatile attributes rebuilt from `pal | coll << 4`, object lists from tuples + sentinels, scripts
   from (init, mode, per-frame, exits, terminator), palettes from (start, values)), write it into a copy of
   the ROM and compare. Covered and identical: the stage table, the 4 layout banks ($26/$27/$32/$33, 32 KB,
   every byte), the 6 tileset banks ($2A-$2F, 48 KB, every byte; the two unused slots are copied raw),
   the object-list pointer/count tables and all 16 lists ($3A:$85D8-$95D3), the 128 screen scripts
   (968 bytes), the 256 palette programs in bank $37 and in bank $28, and the CHR set table. **The rebuilt ROM
   is byte-identical (MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`).**
2. **JSON level**: `export(s)` writes each stage to `build/research/rm6/rm6-levels/json/<nn>_<stage>.json`
   (header, 32 screens, 256 blocks, 256 + 256 metatiles, objects, sentinels, every script the stage uses,
   the walk graph); the file is read back and `encode_stage()` rebuilds every region (19-36 regions, about
   6 KB per stage): **identical for all 16 stages**.
3. **Edited ROM in the game** (`build/research/rm6/rm6-levels/edit_test.py`): `build_rom()` of the 16
   unedited JSONs gives the original MD5; after adding a platform (3 layout bytes) and a 1-up (one more
   object, so every later list moves and the pointer table is rewritten) to Blizzard Man screen 00, the
   rebuilt ROM boots, the live nametable matches the edited static render 960/960 and the new 1-up spawns
   in slot 19 at (D0, 70) [seen] (`img/levels_edit_test.png`). The first attempt put the platform where
   Rockman beams in, and he exploded inside it [seen]: the collision came along with the graphics.

## 15. Validation against the running game [seen]

- **Savestates** (`validate.py`, 61 states, 51 in a stage, run 400 frames, compared with the static render of
  the camera screen and with `walk()`'s CHR / palette for it): nametable 960/960 in every state whose camera
  is at fine X 0, except boss rooms (944: the closed shutter, section 4) and text overlays; BG CHR exact over
  the tiles the screen uses except 4 animated tiles (Centaur waterfall, Mr. X 3); BG palette exact except
  colour-cycle entries (Flame 9-11, Mr. X 3 entry 5, Tomahawk 15) and the Wily 3 hub. Fortress boss rooms
  match only because `walk()` traces the boss spawned by the room's init and applies the palette its AI
  loads with `$39:$8110` (Mr. X 2 $BF, Mr. X 3 $BC, Wily 1 $7F).
- **Graph-driven tour** (`tour.py`): for every screen of every stage, load the state of the screen it is
  reached from, trigger the same edge (move the player with noclip-style hovering that avoids solid tiles
  using the decoded collision, place him on the exit edge, set the ladder state for up exits, walk into
  shutters), wait for the camera, settle, compare. The scout's `*_ck1` / `*_ck2` states seed the screens
  behind mid-boss rooms whose exit waits for a fight. **319 screen arrivals compared over the 16 stages,
  each reached by the predicted edge in the predicted direction**; CHR and palette exact in **264**; 36
  differ only in colour-cycle entries and 14 only in up to 8 animated CHR tiles; the 9 real mismatches are
  listed in section 17. 7 edges could not be driven: exits held by a fight (Plant 0E, Yamato 0E, Tomahawk
  05 and 10, Wily 4 03), Yamato 13 -> 14 (the arrival-window effect of section 8 when the tour comes from
  1A without moving the camera) and Centaur 15 -> 18 (the tour died in the pit). Not toured either: the
  Wily 3 teleporters (hub routine) and the screens behind the blocked edges (Plant 0F-17, Tomahawk 06-09
  and 11-1F, Wily 4 04-06).

## 16. Unused and duplicate data [code]

- **Tileset slots `$2B:$9200-$9AFF` and `$2D:$9200-$9AFF` are empty** (fill), 2 x 2304 bytes: room for two
  more complete stage tilesets without new banks.
- **Object-list space**: `$3A:$95D4-$9FFF` (2604 bytes) is fill, so the lists can grow by ~650 objects.
- **Layout screens**: every stage has its 32-screen strip; unused screens are block 0 except Mr. X 2 $12 (a
  4-block stub of the wall in $11), Wily 3 $15/$16/$18-$1B (exact copies, 64/64 blocks, of $07, $08, $09,
  $0A, $0C, $0B) and Wily 4 $10 (a copy of $01). The Wily 3 copies sit where a Robot Master stage keeps its
  alternate route; they look like an earlier arrangement of the capsule hub and refight rooms [guess].
  Raw strips: `build/research/rm6/rm6-levels/strip_<nn>_<stage>.png` (`levels.py strips`).
- Attribute bits 2-3 are 0 in every metatile of every stage (free for a hack's own flags).
- The first sentinel of the object lists (stage 0) is $24 instead of $FF; nothing reads it.

## 17. Remaining unknowns (precise)

- **Palettes set by object code from tables**: Plant's gorilla-tank rooms 08 / 0E (live sub-palettes 0 and 2
  = `10 27 17`, `30 20 10`; the tank AI `$3B:$9685` calls `$C9EF` twice with a computed id [guess: from a
  table]), Mr. X 4
  room 15 (the boss is drawn with BG tiles: its CHR, 121 tiles, and sub-palette 3 come from the boss code),
  Centaur 0D (per-frame `$39:$8A05` runs a palette sequence when the camera stops). The maps show these rooms
  with the stage palette / CHR.
- **Colour cycles and animated tiles** are shown at their first frame. Cyclers not in the bank-$3B format
  (Flame's oil rotation, Mr. X 1 entry 9, Mr. X 3 entry 5) are shown with the base palette.
- **Wily 3 hub arrival** (screen 08): the teleport routine `$39:$9AC4` reloads the palette from `$AE`, so its
  sub-palettes 0 and 2 differ from the map.
- **Collision types 5/6/7/9/$C/$E** and the remapped values $10-$1F are named only where rm6-stages-a/b saw
  them (ice, oil, spike beds, Wind's fans); the floor-handler table indexed by them was not decoded.
- The meaning of AI header byte `AI-3` (`$059A`, probably the hitbox size) and `AI-1` (`$0583`).
- Breakable blocks and shutters drawn through the alternate set (`$0340`) are shown intact; the closed
  boss door is drawn by direct nametable writes, not shown.

## 18. Using the extractor

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
import levels as L, json
js = [L.export(s) for s in range(16)]                    # plain dicts (json-safe)
js[0]['screens']['00'][4][5] = js[0]['screens']['00'][6][0]   # edit a layout byte
js[0]['objects'].append(dict(screen=0, x=0xD0, y=0x70, type=0x37))   # add a 1-up
L.build_rom(js, 'build/my_test.nes')                      # repacks object lists, rewrites pointers
L.render_map(0, 'blizzard.png')                           # stitched map
L.walk(0)[0x0D]                                           # Node: position, CHR sets, palette, entry edge
L.decode_script(0x0C), L.trace(0x849B)                    # a script and what its init routine does
```

`build_rom` sorts each object list by (screen, X) (the spawner needs it) and asserts that the lists still
fit in bank $3A; screens, blocks, metatiles and scripts are written in place (a script that grows must be
moved and its pointer updated by hand: `levels.SCR_LO/SCR_HI`).

## 19. Lessons for Rockman 6 GP

- **The level format is friendly**: no compression, fixed-size tables, one byte per 32x32 block, pointers in
  small per-stage tables. An editor pipeline (JSON <-> ROM) already round-trips byte for byte
  (`levels.build_rom`), so stages can be authored as data and rebuilt on every build.
- **Budgets per stage**: 32 screens of 8 x 7.5 blocks, 256 blocks, 256 metatiles, 256 objects. The block
  table is the tight one (full in 11 of 16 stages): new art or large new areas need a fresh tileset slot.
  Two empty slots exist ($2B:$92, $2D:$92), the free banks $0B-$0F can hold more tileset or layout banks
  (the stage table bytes are plain bank numbers), and Wily 4 uses only 7 of its 32 screens.
- **The 2-D shape is code, not data**: vertical sections are just more screens in the strip, and every
  turn is a screen-script exit. Keep a strict convention (mode 1 at the start of a run, mode 2 at the end,
  shared shaft scripts $02/$07) and generate scripts from a map, or new rooms will scroll into garbage.
- **One script per screen** (slot 22) and one extra BG CHR set (`$064F`) per checkpoint: a room that needs
  two CHR swaps or two scripts has to chain them in an init routine. Exits kill the old script mid-loop, so
  "on leave" code only runs on scroll-away.
- **Palettes are cumulative deltas along the route**, and a checkpoint stores only one palette id
  (`$0686` = `$069E`, and one extra CHR set `$0685` = `$064F`; [code] `$3F:$FA20` for the boss shutter): every
  checkpoint screen needs a palette program that sets everything it relies on, or a respawn will look
  different from the first visit. Test respawns, not only first visits.
- **Collision lives in the metatile attribute** (high nibble, remapped per stage group): new metatiles carry
  their collision with them (the first edit test killed Rockman inside a new platform), and a hack can add
  stage-specific floor types through the group table `$3E:$DB03/$DB13` without touching the layout.
- **Sprite CHR is automatic**: placing an enemy on a screen queues its CHR set from the AI header when the
  camera enters the screen, skipping the 8 sets in the "recently loaded" list `$07E8`. The NMI drains the
  8-entry ring `$07F0` and `$CAA4` waits a frame when it is full, so many new enemy types on one screen cost
  frames, and two types whose CHR sets overlap in $1000-$1FFF cannot share a screen. Budget enemy variety
  per screen pair and give new enemies CHR sets that do not collide.
- **Mid-boss rooms block exits in code** (`$03A8` = 0 waits): any new gate or arena can reuse the same
  pattern (spawn into slot 8, loop until the slot is empty, `JMP $827C`).
- **Free room for new data**: 2604 bytes after the object lists, 2 x 2304 bytes of tileset slots, attribute
  bits 2-3 unused in every metatile, and the many unused screens per layout.
