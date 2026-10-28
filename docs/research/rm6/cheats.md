# Rockman 6 (J): warp toolkit, passwords, autoplay and savestates (rm6-scout)

Status: **v0.9** (checkpoint table still being completed). Helper: `tools/analysis/rm6/cheats.py`.
RAM map and how each address was verified: `ram.md`. Tags as in the field guide.

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
from emu import Emu
import cheats as c6
e = Emu('roms/rm6j.nes'); e.load(c6.state('stage_blizzard'))
c6.give_all(e)                 # 8 bosses + B-E-A-T + both adaptors + Energy Balancer, 9 E-tanks, 9 lives
c6.warp(e, 'knight', ckpt=1)   # RAM warp to Knight Man's mid-stage checkpoint, waits until playable
c6.godmode(e, fuel=True)       # frozen HP, lives, invincibility timer (and Rush Jet fuel)
e.poke(c6.FORM, 1)             # Jet Rockman (adaptor form 0/1/2)
best, arch = c6.explore(e, budget=200000)   # Go-Explore autoplayer
print(c6.info(e))
```

One Emu per process (stable-retro). After `e.load()`, run one frame before `e.shot()`.

## Stage IDs (`$51`)

0 Blizzard, 1 Wind, 2 Plant, 3 Flame, 4 Yamato, 5 Tomahawk, 6 Knight, 7 Centaur, 8-11 Mr. X Fortress
1-4, 12-15 Wily Fortress 1-4. `c6.STAGES` / `c6.STAGE_ID` map ids and names. [seen] all 16 load and
look right (`img/scout_states.png`).

## Cheats

| Call | What it does | Verified |
|---|---|---|
| `godmode(e)` | freezes HP `$03E5` = $1B, lives `$A9` = 9, invincibility `$A2` = 2 (no damage, no knockback, no blink); `fuel=True` also freezes Rush Jet fuel `$9C` | [seen] enemy contact does nothing; pits still kill (respawn at the checkpoint) |
| `give_all(e)` | progress bytes `$0692-$0695` = 7 (all bosses + plates), `$0696` = 1, energies `$0688-$0691` = $1B, `$06A1` = 9, `$A9` = 9 | [seen] pause menu: 10 weapons, NOR/JET/POW, Energy Balancer, BEAT |
| `set_progress(e, beaten, plates, balancer)` | writes just the progress bytes | [seen] |
| `refill(e)` | HP and every owned weapon to full | [code] |
| `e.poke(c6.FORM, n)` | 0 normal, 1 Jet, 2 Power, works mid-stage without the menu | [seen] Jet flies; the sprite CHR is loaded by the menu, so a raw poke can show a mixed sprite |

**Pitfall: no Robot Master rematch.** If the current stage's boss is marked beaten when Rockman
enters its boss room, he beams out at once (stage over, post-stage password screen). So for boss
work use `set_progress(e, beaten=[all but this stage])` [seen].

## Warps

1. **RAM warp, `warp(e, stage, ckpt=0)`** (works from any in-stage state; otherwise it loads
   `stage_blizzard` first). It writes `$51` = stage, `$0684` = checkpoint screen, `$0685` / `$0686` =
   that checkpoint's CHR set / palette, then `$F0` = 2, the main loop's "respawn at checkpoint" code
   ($3E:$CD5D exits the loop when `$F0` != 0: 1 = stage clear, 2 = respawn, 3 = game over). The game
   reloads the stage exactly as after a death (no boss intro, no life lost) and is playable 130-140
   frames later. Inventory and progress are kept. [seen] every stage and checkpoint below; each
   warped checkpoint renders identically to the moment the game set it naturally
   (`img/scout_ckpt_warp.png`).
2. **Next fortress stage: `clear_stage(e)`** (`$F0` = 1). In a fortress stage the game runs its own
   transition (`INC $51`, the fortress map cutscene, READY). In a Robot Master stage it returns to the
   stage select. [seen] used to make `mrx2.state` .. `wily4.state`.
3. **Passwords** encode only the 8 bosses, the 4 Beat plates and the Energy Balancer (never fortress
   progress). `pw_encode(flags, balancer)` / `pw_decode(cells)` implement the decoder at $3F:$F3D0:
   the key cells E5/E6/F5/F6 choose one of four tables (two without, two with the Energy Balancer) and
   each progress byte is one more orb, so every password is exactly 5 orbs. [seen] 12 generated
   passwords typed into the real screen all gave the intended `$0692-$0696`.

| Password | Meaning |
|---|---|
| A4 C2 C6 E4 E5 | everything: 8 bosses, B-E-A-T, Energy Balancer (opens Mr. X) |
| A6 C4 E2 E4 F6 | same, other table |
| B5 C5 D1 E6 F1 | 8 bosses and B-E-A-T, no Energy Balancer |
| A1 B4 C3 C4 E6 | Blizzard Man only |
| A1 B1 B4 C4 E6 | nothing (a valid "empty" password) |

## Checkpoints (`c6.CHECKPOINTS`)

Each value was written by the game itself (`$0684/$0685/$0686`) when the Go-Explore autoplayer
reached the checkpoint, or on entering the boss room. Index 0 = stage start. The boss-room entry is
also a checkpoint: `$0684` = boss screen - 1 ($3F:$FA20).

| Stage | Mid-stage checkpoint (screen / CHR / palette) | Boss shutter checkpoint |
|---|---|---|
| Blizzard | 0D / 85 / 1A | pending |
| Wind | 08 / 8D / 17 | pending |
| Plant | 09 / 92 / 32 | pending |
| Flame | 0E / 87 / 1F | 16 / 87 / 1F |
| Yamato | pending (screen 0A per its screen script) | pending |
| Tomahawk | 0A / 95 / 95 | pending |
| Knight | 0B / 00 / 78 | pending |
| Centaur | 0A / 00 / A7 | pending |
| Mr. X 1 | pending (screen 0E by probe) | |
| Mr. X 2 | 08 / 00 / 00 | 10 / B8 / 00 |
| Mr. X 3 | 08 / 00 / 00 | 10 / B4 / D0 |
| Mr. X 4 | pending | |
| Wily 1 | 0E / 00 / 81 | 12 / 8B / 81 |
| Wily 2 | pending | |
| Wily 3 | 08 / A9 / 00 | (boss reached without a new checkpoint) |
| Wily 4 | (capsule stage, 7 screens) | |

## Autoplay: `explore()`

A Go-Explore autoplayer, same design as the CX one: an archive of cells (stage, object-list window
`$0649`, player screen `$046F`, X/32, Y/32, camera Y/64, camera Y screen) -> savestate; it restores
cells biased to the best score and plays random held-button macros (walk, jump, ladders, mashed B).
What made it work on RM6:

- **Score by the object-list window `$0649`, not by screen or X.** Vertical sections scroll the
  camera smoothly (`$58`) and leave `$57`/`$046F` unchanged, and many paths turn back left after a
  ladder, so an X term starves the right cells. `$0649` advances along the path in both cases.
- **Death test by the player's AI pointer** (`dying(r)`): pit death parks it at $38:$8F13 for 60
  frames, HP death at $38:$8E7F for 240. Y >= $F0 is not a death test: dropping into the next screen
  of a shaft passes there too.
- **Jet Rockman with frozen fuel** flies over most obstacles: `e.poke(FORM, 1)` + `godmode(e, fuel=True)`.
- **Mid-bosses** (Plant's dark-room gorilla, Tomahawk's rock dispenser) need a damage term:
  `score = $0649*16 + (63 - enemy HP)/4`, plus enemy HP/4 in the cell key.

Typical cost: a checkpoint in 25-130 s of CPU (75-400k frames).

## Savestates (`build/research/rm6/states/`)

| File | What | How made |
|---|---|---|
| `intro.state` | intro story scene, before the title | boot + START |
| `title.state` | title screen, GAME START cursor, title loop running | boot, skip intro |
| `stage_select.state` | new-game stage select (nothing beaten) | GAME START |
| `password.state` | empty password grid | PASS WORD |
| `stage_select_all.state` | stage select after the all-clear password (Mr. X in the centre) | password screen |
| `stage_<name>.state` x8 | each Robot Master stage after READY, playable, new-game inventory | stage select + START |
| `mrx1.state` | Mr. X Fortress 1 start (after the fortress map) | `stage_select_all` + START on the centre |
| `mrx2..mrx4`, `wily1..wily4.state` | each fortress stage start, playable | previous stage + `$F0 = 1` |
