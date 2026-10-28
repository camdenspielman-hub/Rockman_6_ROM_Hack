# Rockman 6 (J) stages, part A: Blizzard Man, Flame Man, Knight Man, Centaur Man (rm6-stages-a)

Status: **draft v2** (rewritten as work progresses; sections marked TODO are still being filled).

Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text, **[guess]** unverified.
Scripts: `build/research/rm6/rm6-stages-a/` (`lvl.py` level decoder, `mapper.py` route walker and map
renderer, `objs.py` object lists, `tiles.py` tileset sheets, `dmg.py` boss damage harness, `strips.py`
enemy behaviour strips, `census.py`, `fxwatch.py`, `irqscan.py`, `items.py`). States: the scout's
`build/research/rm6/states/` (`stage_*`, `*_ck1`, `*_ck2`, `*_boss`).

## 0. How a Rockman 6 stage is stored (all stages) [code][seen]

Decoded from the stage init ($3E:$DBDC), the address maths ($3E:$D8AF/$D904), the row/column painters
($3E:$D1FF/$D322) and the collision lookup ($3E:$DA6C). The static renderer built from this reproduces the
live nametable exactly (verified at 12 states: start, mid-stage checkpoint and boss shutter of the four
stages; `lvl.py`, `v1.py`, `v2.py`).

Per-stage tables in the fixed bank $3E, indexed by stage id `$51`:

| Table | RAM | Meaning |
|---|---|---|
| $DF55 | `$6E` | 8 KB bank at $8000 with the metatile and block tables |
| $DF25 | `$6F` | 8 KB bank at $A000 with the layout |
| $DF35/$DF45 | `$52/$53` | layout base (lo byte, page) |
| $DF65 | `$63` | first page of the metatile tables (5 pages: TL tile, TR, BL, BR, attribute) |
| $DF75 | `$67` | first page of the block table (4 pages: 256 blocks x 4 metatiles) |
| $DF85 | `$064E` | base CHR set (BG) |
| $DF95 | `$069E` | palette id |
| $DFA5 | `$DC` | music id (sound-queue request) |

| Stage | $6E | $6F | layout | metatiles | blocks | CHR set (file offset) | palette | music |
|---|---|---|---|---|---|---|---|---|
| 0 Blizzard | $2E | $32 | $A000 | $8000 | $8500 | $82 (bank $12+$0000, 0x24010) | $15 | $01 |
| 3 Flame | $2F | $32 | $B800 | $8000 | $8500 | $86 (bank $13+$1000, 0x27010) | $1E | $03 |
| 6 Knight | $2D | $33 | $B000 | $8000 | $8500 | $9E (bank $15+$0000, 0x2A010) | $74 | $07 |
| 7 Centaur | $2D | $33 | $B800 | $8900 | $8E00 | $AA (bank $1A+$1000, 0x35010) | $A6 | $05 |

- **Layout**: 8 rows x 256 columns of **32x32 blocks**: byte at `(($53 + row) << 8) + col`, with
  `col = screen*8 + x/32`. A stage is at most **32 screens** of 8x8 blocks (7.5 rows show: 240 px). The
  screen number is linear along the path: the code adds the X screen and the Y screen ($D904), so vertical
  shafts are simply the next screens of the same array.
- **Block** (4 bytes): metatile ids TL, TR, BL, BR. **Metatile** (16x16): 4 tile ids from 4 pages plus an
  attribute byte: bits 0-1 = BG palette, bits 4-7 = collision type.
- One 8 KB metatile bank holds three stage sets at pages $80, $89, $92 (9 pages each) plus a shared
  **alternate set at $9B00-$9F00**: a metatile whose bit is set in the 32-byte bitfield `$0340` (indexed by
  metatile id) is drawn and collided from the alternate tables instead (this is how broken/melted blocks
  disappear).
- **Collision types** (attribute high nibble). Odd = solid (`AND #1` tests everywhere, [code] $38:$9CAD).
  [code][seen]: 0 air, 1 solid, 3 ladder top, 4 ladder, 5 solid (ice/snow in Blizzard), 8 water (Centaur;
  ignored by the floor probe at $38:$837C), **$B = breakable by Power Rockman's punch** (attack code $14,
  $38:$8D67 -> $8D9D), **$D = destroyed by Flame Blast** (the F.BLAST shot $84 tests for $0D at
  $38:$9CA9), $F = deadly (bottomless water/oil, spikes). Flame's oil uses 2/6/9: entering type 6 or 9
  plays sound $50 and spawns a splash ($38:$88CC); jumping off type 9 gives a weaker jump (start
  velocity $FB instead of $FA, $38:$80D7) [code]; 7 is a solid variant (Blizzard ship deck, Flame/Knight
  "DANGER" walls) [guess: special floor]. Stage groups remap types through $3E:$DB03/$DB13 (identity
  for all four stages here).
- **CHR sets** (bank $37, $8000 + id*4): tile count (0 = 256), PPU address/16, source offset/16, flags (b7 =
  PPU +$1000, b0 = source +$1000, b1-6 = 8 KB bank). `$CAA4` copies one set. Stage BG = base set `$064E`
  plus an optional extra set `$064F` loaded by screen exits (checkpoints snapshot both).
- **Palettes** (bank $37, pointers $9000/$9100 + id; bank $28 instead when `$06A0` = revisit): a start
  index, then colour bytes (b6 = write $0F first, b7 = last). They are **partial**: an exit's palette id
  only rewrites a few entries of the 32-byte buffer `$0360`, so palettes must be applied cumulatively
  along the route (`mapper.walk` does this; verified against live palettes at the checkpoints).
- **Object list** (bank $3A, pointers $80BF/$80CF, count $80DF): four parallel arrays screen, X, Y, type
  (sorted by screen/X; spawned when the camera reaches them, `$0649/$064A` window). Type $80 =
  **screen script** whose Y byte is the script index (bank $39, pointer tables $82EB/$836B). Other types
  map to AI code by $3A:$82C9 (lo) / $83C9 (hi) / $84C9 (bank pair) and a sprite bank $85C9[type>>4].
  Each screen's sprite CHR sets are queued by $3A:$826F when the screen comes into range.
- **Screen scripts** ([code] $39:$824D): [init routine (if b0 bit 7)], mode, per-frame routine, exits.
  Mode bit 0 = the camera may scroll right past this screen, bit 1 = left. Exit = direction (1 down, 2 up,
  5 right, 6 left = forward; 3 down*, 4 up* = back), CHR set, palette id, optional target (b7). Forward exits
  go to `target + 1` (default: this screen + 1), back exits to `target - 1`. Routine $8416 (`CMP $57`)
  = "set the checkpoint when the camera is on screen A"; $8480/$848E = boss shutter (next screen to the
  right); mode $FF = boss room. Init routines can start a **stage effect thread** with `LDX #n / JSR $C5C7`
  (table $3E:$C632/$C64D/$C668/$C683; thread 2 is the effect thread).
- **Items** (all stages; [seen] by spawning each type next to Rockman with low HP/energy, `items.py`):
  $37 1-up, $38 small life energy (+2), $39 large life energy (+10), $1D E-tank, $49 small weapon energy
  (+2), $4A large weapon energy (+10). Items have HP $7F (untouchable).
- **Enemy HP**: an object dies when its HP goes negative, so stored HP n = n+1 buster hits (HP 0 = one hit).

## Boss damage (all four bosses, measured) [seen]

Method (`dmg.py`): from each `<name>_boss` state, with the other seven bosses marked beaten, wait until the
bar is full, then every frame pin Rockman 44 px from the boss at the boss's height, select the weapon by
poking `$0699` (and the form `$9B`), fire every 14 frames (charge: hold 100 frames) and log every drop of
the boss HP `$03ED`. Three hits per weapon. Boss HP = 27 ($1B) for all four.

| Weapon | Blizzard Man | Flame Man | Knight Man | Centaur Man |
|---|---|---|---|---|
| R.BUSTER | 1 | 1 | 1 | 1 |
| charged buster | 3 | 3 | 3 | 3 |
| Y.SPEAR | 1 | 1 | **4** | 1 |
| W.STORM | 1 | **4** | 1 | 1 |
| B.ATTACK | 1 | 1 | 1 | 1 |
| F.BLAST | **4** | 1 | 1 | 1 |
| PLANT.B | 0 | 0 | 0 | 0 |
| KNIGHT.C | 1 | 1 | 1 | **4** |
| SILVER.T | 1 | 1 | 1 | 1 |
| C.FLASH | 0 | 0 | 0 | 0 |
| BEAT | 1 | 1 | 1 | 1 |
| Jet Rockman buster | 1 | 1 | 1 | 1 |
| Power punch (tap or charged) | 2 | 2 | 2 | 2 |

- Zeros were double-checked by eye: Centaur Flash flashes the screen and does nothing; the Plant Barrier
  forms and vanishes on contact (`pbtest.py`). As a control, the same harness gives Wind Man 4 from
  C.FLASH.
- The charged punch reaches full charge (`$9E` counts to $5A) but still does 2 [seen]; the buster charge
  is `$9E` too (counts +1/frame).
- So the weakness chain for this half is **Flame Blast -> Blizzard, Wind Storm -> Flame, Yamato Spear ->
  Knight, Knight Crusher -> Centaur**; every other weapon does 1 (Plant Barrier and Centaur Flash 0).

## 1. Blizzard Man (stage 0, FROZEN ISLAND)

Route ([code] walker + [seen] tour; map `img/stagesa_blizzard_map.png`): 25 screens.

| Screens | Section |
|---|---|
| 00-05 | Outdoors: green steel scaffolds with red girders in front of blue snow mountains, snowy rock ledges. 03 is a **pit crossed on floating Count Bomb platforms** ($19, the "3" pods) under propeller drones |
| 05 -> 06 -> 07 | Drop down an ice-block shaft (script 01/02/03) |
| 07-0B | Ice cave: frozen blocks on green brick, ladders; **E-tank in screen 09 sealed in Flame-Blast ice** (type $D blocks at $10-$3F,$40-$5F) |
| 0B -> 0C -> 0D | Second shaft down; the jester-head turret ($10) guards 0C; **checkpoint 0D** (CHR set $85, palette $1A) |
| 0D -> 0E (flip right) -> 13 | The **icebreaker ship**: pink/orange deck over icy sea, cannon riders ($1F/$20); the deck **bobs up and down** (IRQ split, below) |
| 13 -> 14 -> 15 | Climb up a shaft (CHR set $84 restores the cave tiles, palette $1C) |
| 15 -> 16 -> 17 -> 18 | Count-bomb corridor, boss shutter (17 = checkpoint 2), boss room 18 |

TODO: per-screen table, enemies, items, gimmicks, tileset, boss patterns.

## 2. Flame Man (stage 3, OIL FIELD)

TODO

## 3. Knight Man (stage 6, CAPITAL OF SCIENCE)

TODO. Plate A: route 15 -> 18 -> 19 -> boss room 1A ($3F:$F518), through Power-punch blocks (type $B) in
screens 15 and 18.

## 4. Centaur Man (stage 7, ANCIENT CITY)

TODO. Plate T: boss room **17** (the shutter route 15 -> 16 -> 17); falling into the shaft at screen 15
leads to 18 -> 19 -> boss room 1A without the plate.

## Lessons for Rockman 6 GP

TODO
