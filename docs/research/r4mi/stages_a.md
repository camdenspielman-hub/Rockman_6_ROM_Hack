# 4MI stages A: Ring Man, Pharaoh Man, Drill Man, Dive Man (r4mi-stages-a)

Status: IN PROGRESS (this file is rewritten as the investigation proceeds).

Scope: Rockman 4 Minus Infinity v1.01 (`roms/r4mi_mmc5.nes`), the stages of Ring Man (`$22` = 4), Pharaoh Man (3),
Drill Man (2) and Dive Man (6): route, gimmicks, enemies, mid-bosses, hidden rooms, pickups, HARD differences, the
boss fights (patterns and weapon damage) and the jokes. Played with godmode (frozen HP and i-frames plus the FAIL-SAFE
items, `cheats.godmode()`), so the "intended challenge" notes are my reading of what a normal player faces.

Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text, **[doc]** readme, **[guess]**.

## 0. Method and tools

### How 4MI stores a stage (needed to draw the maps) [code + seen]

- The stage bank is still `$20 + stage` at `$A000` (MMC5 `$5115`), as in vanilla RM4. Its first `$500` bytes are the
  16×16 block table (four 256-byte tile planes TL/TR/BL/BR at `$A000-$A3FF`, block attributes at `$A400`: low 2 bits
  palette, high nibble collision type).
- **New in 4MI: the stage is split into sections of up to 12 screens, each with its own 32×32 metatile set, screen
  layouts and CHR.** When you enter a section the game decompresses it into battery WRAM: blocks `$6000-$64FF`
  (copied raw from the bank), metatiles `$6500-$68FF` (4 bytes each), screen layouts `$6900-$6BFF` (64 bytes per
  screen, 8×8 metatiles, row-major). The table at bank `$B500` maps each global screen number (`$0348`/`$F9`) to its
  local index in the section, so the reset points in that table are the section boundaries.
- The enemy table keeps the vanilla RM4 format: `$B100` screen, `$B180` X, `$B200` Y, `$B280` type, `$FF`-terminated,
  and `$B300` = index of the first enemy of each screen.
- Collision types seen (block attribute high nibble): 0 air, 1 solid, 2 ladder, 3 spikes, 4 ladder top, 5 boss
  shutter, 14 and 15 stage-specific (in Ring: the colour-cycling laser bars).

Tools (scratch, `build/research/r4mi/r4mi-stages-a/`): `secmap.py` renders every screen of the loaded section from
WRAM with the live CHR and palette, `ascii.py` prints collision maps as text, `enemies.py` dumps the enemy table,
`drive.py` is a scripted player with teleports.

## 1. Ring Man stage (`$22` = 4)

(in progress)

## 2. Pharaoh Man stage (`$22` = 3)

(pending)

## 3. Drill Man stage (`$22` = 2)

(pending)

## 4. Dive Man stage (`$22` = 6)

(pending)

## Lessons for Rockman 6 GP

(pending)
