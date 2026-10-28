# Rockman 6 (J): warp toolkit, passwords and savestates (rm6-scout)

Status: **draft v0, being extended**. Helper: `tools/analysis/rm6/cheats.py`. RAM map: `ram.md`.

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
from emu import Emu
import cheats as c6
e = Emu('roms/rm6j.nes'); e.load(c6.state('stage_blizzard'))
c6.give_all(e)                 # all weapons, both adaptors, Beat, Energy Balancer, 9 E-tanks, 9 lives
c6.warp(e, 'knight')           # RAM warp to a stage start (or any checkpoint), waits until playable
c6.godmode(e)                  # frozen HP, lives and invincibility timer
print(c6.info(e))
```

## Stage IDs

`$51`: 0 Blizzard, 1 Wind, 2 Plant, 3 Flame, 4 Yamato, 5 Tomahawk, 6 Knight, 7 Centaur, 8-11 Mr. X
Fortress 1-4, 12-15 Wily Fortress 1-4. [seen] all 16 stages load by RAM warp and show the right graphics.

## Warps

1. **RAM warp (works everywhere).** From any in-stage state: `$51` = stage, `$0684` = checkpoint screen,
   `$0685`/`$0686` = that checkpoint's CHR-set id / palette id, then `$F0` = 2. `$F0` is the main
   loop's exit code (bank $3E, $CD5D: `LDA $F0 / BEQ loop`; 1 = stage clear, 2 = respawn at the
   checkpoint, 3 = game over). Code 2 is the death-respawn path ($CD46), so the stage reloads at the
   checkpoint with no boss intro and no life lost. [seen] `c6.warp()`.
2. **Next fortress stage by "stage clear".** In a fortress stage, `$F0` = 1 makes the game run its
   normal transition to the next one (`INC $51`, the fortress map cutscene, READY). [seen] used to make
   the mrx2..wily4 states below.
3. **Passwords** (only the 8 bosses, the 4 Beat plates and the Energy Balancer; no fortress progress).
   [seen] 12 passwords made by `c6.pw_encode()` were typed into the real password screen and all
   decoded to the intended `$0692-$0696`.

| Password (cells) | Meaning |
|---|---|
| A4 C2 C6 E4 E5 | everything: 8 bosses, B-E-A-T, Energy Balancer (Mr. X open) |
| B5 C5 D1 E6 F1 | 8 bosses and Beat, no Energy Balancer |
| A1 B4 C3 C4 E6 | Blizzard Man beaten only |

## Savestates (`build/research/rm6/states/`)

| File | What | How made |
|---|---|---|
| `intro.state` | intro story scene, before the title | boot + START |
| `title.state` | title screen, GAME START cursor, title loop running | boot, skip intro |
| `stage_select.state` | new-game stage select (nothing beaten) | GAME START |
| `password.state` | empty password grid | PASS WORD |
| `stage_select_all.state` | stage select after the all-clear password (Mr. X portrait in the centre) | password screen |
| `stage_<name>.state` x8 | each Robot Master stage after READY, playable | stage select + START |
| `mrx1.state` | Mr. X Fortress 1 start (after the fortress map) | `stage_select_all` + START on the centre |
| `mrx2..mrx4`, `wily1..wily4.state` | each fortress stage start, playable | previous stage + `$F0 = 1` |
