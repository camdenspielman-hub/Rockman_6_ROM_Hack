# Rockman 6 (J) level data format (rm6-levels)

Status: **v0 skeleton** (written early per the resilience rule; filled in as each part is verified).
Tags: **[seen]** emulator, **[code]** disassembly / ROM data, **[guess]** unverified.
Extractor: `tools/analysis/rm6/levels.py`. Scratch: `build/research/rm6/rm6-levels/`.
Builds on the decoders of rm6-stages-a (`rm6_stagemap.py`, `stages_a.md` section 0) and rm6-stages-b
(`rm6_level.py`, `stages_b.md` section 1); this doc is the byte-level reference for all 16 stages.

## 1. Per-stage table (fixed bank $3E, 9 tables x 16 bytes at $DF25-$DFB4, indexed by `$51`) [code]

Stage init `$3E:$DBDB` (A = stage id): `$51` = id, `$063D` = id & 7, far call `$3A` function 2 (object list
init), palette `$DF95,Y` via `$C9EF`, music `$DFA5,Y` -> `$DC`, HP `$03E5` = $1B, then copies the tables below.

| Table | RAM | Meaning |
|---|---|---|
| $DF25 | `$6F` | layout bank (8 KB, at $A000) |
| $DF35 / $DF45 | `$52` / `$53` | layout base lo / page (always lo = 0) |
| $DF55 | `$6E` | tileset bank (8 KB, at $8000): 16x16 metatiles and 32x32 blocks |
| $DF65 | `$63` | first of 5 metatile pages (TL, TR, BL, BR tile, attribute) |
| $DF75 | `$67` | first of 4 block pages (256 blocks x 4 metatile ids, interleaved by 4) |
| $DF85 | `$064E` | base BG CHR set id (bank $37 table) |
| $DF95 | `$069E` | start palette id |
| $DFA5 | `$DC` | music id |

```
id  stage     L6F P53 T6E P63 P67 CHR PAL MUS
 0  Blizzard  32  A0  2E  80  85  82  15  01
 1  Wind      32  A8  2C  80  85  83  17  00
 2  Plant     32  B0  2E  92  97  90  32  04
 3  Flame     32  B8  2F  80  85  86  1E  03
 4  Yamato    33  A0  2E  89  8E  97  57  02
 5  Tomahawk  33  A8  2C  89  8E  94  50  06
 6  Knight    33  B0  2D  80  85  9E  74  07
 7  Centaur   33  B8  2D  89  8E  AA  A6  05
 8  Mr.X 1    26  A0  2C  92  97  9D  68  09
 9  Mr.X 2    26  A8  2F  89  8E  A4  88  09
10  Mr.X 3    26  B0  2F  92  97  B1  AB  09
11  Mr.X 4    26  B8  2B  80  85  C3  C8  09
12  Wily 1    27  A0  2A  80  85  89  7C  0B
13  Wily 2    27  A8  2A  89  8E  A2  89  0B
14  Wily 3    27  B0  2A  92  97  A2  96  0B
15  Wily 4    27  B8  2B  89  8E  BA  18  0B
```

(sections below are being filled in)
