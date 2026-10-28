# Rockman CX cheat sheet, warps and savestates (cx-scout)

DRAFT (being extended; resumed after a container restart). Scope: the RAM map, save format, boot flow, stage-select
layout, the shared savestates, and the helper module `tools/analysis/cx/cheats.py` that other CX investigators use.

Tags: **[seen]** observed in the emulator, **[code]** from disassembly or data, **[text]** in-game text,
**[doc]** readme, **[guess]** speculation. ROM: `roms/cx_en.nes` unless noted (JP and EN share all RAM addresses).

## 0. Quick start

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu
import cheats as cx
e = Emu('roms/cx_en.nes')          # one Emu per process (stable-retro limit); reuse it with e.load()
e.load(cx.state('air_man'))        # any state from build/research/cx/states/
cx.godmode(e)                      # freeze HP, lives, i-frames
cx.give_all_weapons(e)             # all 8 boss weapons, full energy, 4 E-tanks
print(cx.info(e))                  # one-line RAM summary
cx.warp(e, 3)                      # fresh start of Fire Mario's stage, via a crafted save + stage select
```

## 1. RAM map (first pass, see later sections for verification notes)

| Address | Meaning | Evidence |
|---|---|---|
| `$06C0` | Player HP (start 24 = `$18`) | [seen] HUD bar, hit diff |
| `$06C1` | Boss HP | [seen] |
| `$0099` | Max HP (24, +4 per heart tank; 40 as Quick Man in the opening) | [seen][code] |
| `$009A` | Bosses defeated = weapons owned, bit n = stage n | [code] `$C23C` ORs `$C279,X` |
| `$009B` | bit 7 = playing Quick Man; bits 4-6 = Dr. Light fortress progress | [code] `$FB10`, `$9100` |
| `$004B` | Invincibility timer (`$6E` on hit; Ubercharge adds `$34` per use) | [seen] |
| `$002A` | Stage ID (on the stage select: the cursor) | [seen][code] |
| `$0440` / `$0460` / `$04A0` | Player screen (room) / X pixel / Y pixel | [seen] |
| `$00A9` | Equipped weapon id (0 buster, 1-8 boss weapons, 9-11 items, 12 = E-tank cursor in the menu) | [seen] |
| `$009C-$00A6` | Energy of weapon id 1..11 (`$9B + id`), full = `$28` | [seen] |
| `$00A4` / `$00A5` / `$00A6` | Item 1 Floor / Item 2 Subtank / Item 3 Ubercharge energy | [seen] |
| `$00A7` | E-tanks | [seen] menu |
| `$00A8` | Lives | [seen] menu |
| `$7FF8 + stage` | Heart tank taken in that stage (WRAM) | [code] `$3D:BD85` |
| `$7FF0` | Current save slot (0-2) | [code] |
| `$7420 + 3*field + slot` | Save records | [code] `$FCD0`, `$1F:8BD1` |

(TODO in this draft: checkpoint, item upgrade level, stage-select screen bytes, fortress map.)
