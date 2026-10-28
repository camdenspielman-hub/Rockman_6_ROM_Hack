# Rockman 6 (J) RAM map, v0 (rm6-scout)

Status: **draft, being verified**. Recovered from the first rm6-scout run (killed by a container restart) and
extended in the second run. Tags: **[seen]** = verified in the emulator (how is noted), **[code]** = from
disassembly, **[guess]** = unverified.

ROM: `roms/rm6j.nes`, MMC3, 512 KB PRG, CHR-RAM. Disassemblies of every bank are in
`build/research/rm6/rm6-scout/bXX.asm` (switchable banks at $8000 for even, $A000 for odd banks;
`b38_8000.asm`, `b39_8000.asm`, `b39_A000.asm`, `b3B_A000.asm` are the other mappings).

## Stage IDs ($51)

| $51 | Stage | Stage-select cell (col,row) |
|---|---|---|
| 0 | Blizzard Man | (0,0) top-left |
| 1 | Wind Man | (1,0) top-middle |
| 2 | Plant Man | (0,1) middle-left |
| 3 | Flame Man | (2,0) top-right |
| 4 | Yamato Man | (0,2) bottom-left |
| 5 | Tomahawk Man | (2,1) middle-right |
| 6 | Knight Man | (1,2) bottom-middle |
| 7 | Centaur Man | (2,2) bottom-right |
| 8-11 | Mr. X Fortress stages 1-4 | centre, once all 8 are beaten |
| 12-15 | Wily Fortress stages 1-4 | (entered after Mr. X 4) |

[seen] set on the stage select screen and confirmed by the stage graphics (contact sheet of all 16 warps);
[code] stage-select grid table at $3F:$F232 (`00 01 03 FF / 02 FF 05 FF / 04 06 07 FF`, FF = not a stage,
the centre gives 8 when `$05C8` = 0, i.e. all eight bosses beaten). Per-stage tables in bank $3E at
$DF25 (bank pair of the level data), $DF95 (music), $DFA5 (`$DC` sound id).
