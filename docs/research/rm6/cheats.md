# Rockman 6 (J): warp toolkit, passwords, autoplay and savestates (rm6-scout)

Helper: `tools/analysis/rm6/cheats.py`. RAM map and how each address was verified: `ram.md`.
Tags as in the field guide: [seen] emulator, [code] disassembly, [text] in-game text, [guess].

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/rm6')
from emu import Emu
import cheats as c6
e = Emu('roms/rm6j.nes'); e.load(c6.state('stage_blizzard'))
c6.give_all(e)                 # 8 bosses + B-E-A-T + both adaptors + Energy Balancer, 9 E-tanks, 9 lives
c6.warp(e, 'knight', ckpt=2)   # RAM warp to Knight Man's boss shutter; returns frames until playable
c6.godmode(e, fuel=True)       # frozen HP, lives, invincibility timer and Rush Jet fuel
e.poke(c6.FORM, 1)             # Jet Rockman (0 normal, 1 Jet, 2 Power)
print(c6.info(e))              # stage, screen, x/y, hp, lives, E-tanks, weapon, form, flags, checkpoint ...
best, ok, ck = c6.explore_to(e, until='boss')   # Go-Explore autoplayer up to the boss bar
e.load(c6.state('knight_boss'))                 # or start from a ready boss-intro state
```

One Emu per process (stable-retro limit), so reuse it with `e.load()`. After `e.load()`, run one
frame before `e.shot()`.

## Stage IDs (`$51`)

| Id | Stage | Id | Stage |
|---|---|---|---|
| 0 | Blizzard Man | 8 | Mr. X Fortress 1 |
| 1 | Wind Man | 9 | Mr. X Fortress 2 |
| 2 | Plant Man | 10 | Mr. X Fortress 3 |
| 3 | Flame Man | 11 | Mr. X Fortress 4 |
| 4 | Yamato Man | 12 | Wily Fortress 1 |
| 5 | Tomahawk Man | 13 | Wily Fortress 2 |
| 6 | Knight Man | 14 | Wily Fortress 3 |
| 7 | Centaur Man | 15 | Wily Fortress 4 (capsule) |

`c6.STAGES` / `c6.STAGE_ID` map ids and short names (`'blizzard'` .. `'wily4'`); every helper accepts
either. [seen] all 16 load and are recognisable (`img/scout_states.png`). Stage-select layout and
the boss-flag bits are in `ram.md`.

## Cheats

| Call | What it does | Verified |
|---|---|---|
| `godmode(e, fuel=False)` | freezes HP `$03E5` = $1B, lives `$A9` = 9, invincibility `$A2` = 2 (no damage, no knockback, no blink); `fuel=True` also freezes Rush Jet fuel `$9C` = $13 | [seen] enemy contact does nothing; **pits and spikes still kill** (respawn at the checkpoint) |
| `give_all(e)` | progress bytes `$0692-$0695` = 7 (all bosses + plates), Energy Balancer `$0696` = 1, energies `$0688-$0691` = $1B, E-tanks `$06A1` = 9, lives 9 | [seen] pause menu: 10 weapons, NOR/JET/POW, Energy Balancer, BEAT |
| `set_progress(e, beaten, plates, balancer)` | progress bytes only (weapons follow at the next stage start) | [seen] |
| `give_weapons(e)`, `refill(e)` | energies only / HP + owned weapons to full | [code] |
| `e.poke(c6.FORM, n)` | form 0/1/2 mid-stage without the menu | [seen] Jet flies, Power punches; the form's sprite CHR is loaded by the menu, so a raw poke can show a mixed sprite |
| `info(e)` | one-line RAM summary | |

**Pitfall: no Robot Master rematch.** If the current stage's boss is marked beaten when Rockman walks
into its boss room, he beams out at once (stage over, post-stage password screen; no fight)
[seen] `img/scout_no_rematch.png`. For boss work use `set_progress(e, beaten=[the other seven])`;
`explore_to()` does this for you.

## Warps

1. **RAM warp: `warp(e, stage, ckpt=0)`.** From any in-stage state (otherwise `stage_blizzard` is
   loaded first) it writes `$51` = stage, `$0684` = checkpoint screen, `$0685`/`$0686` = that
   checkpoint's CHR set / palette, then `$F0` = 2. `$F0` is the main loop's exit code ($3E:$CD5D: 1 =
   stage clear, 2 = respawn at checkpoint, 3 = game over), and code 2 is the death-respawn path
   ($CD46): the stage reloads at the checkpoint with no boss intro and no life lost, and is playable
   130-140 frames later. Inventory and progress are kept. `ckpt` indexes `CHECKPOINTS[stage]`
   (0 = start, 1 = mid-stage, 2 = boss shutter), or pass `screen=`, `chr_=`, `pal=` directly.
   [seen] every entry below; each warped checkpoint renders identically to the moment the game set it
   naturally (`img/scout_ckpt_warp.png`).
2. **Next fortress stage: `clear_stage(e)`** (`$F0` = 1). In a fortress stage the game runs its own
   transition (`INC $51`, fortress map cutscene, READY), about 960 frames. In a Robot Master stage it
   returns to the stage select. [seen] made `mrx2.state` .. `wily4.state` (`img/scout_fortress_starts.png`,
   the Mr. X map path in `img/scout_mrx_map.png`).
3. **Passwords** encode only the 8 bosses, the 4 Beat plates and the Energy Balancer, never fortress
   progress. `pw_encode(flags, balancer)` / `pw_decode(cells)` implement $3F:$F3D0. The key cells
   E5/E6/F5/F6 pick one of four tables (two without, two with the Energy Balancer), then each of the
   four progress bytes is one more orb, so every valid password is exactly 5 orbs.
   `progress_flags(beaten, plates)` builds the bytes. [seen] 14 passwords typed into the real
   screen: all decoded to the intended `$0692-$0696` (`img/scout_passwords.png`); 4 or 6 orbs give
   "PASS WORD ERROR" [text].

| Password | Meaning |
|---|---|
| A4 C2 C6 E4 E5 | everything: 8 bosses, B-E-A-T, Energy Balancer (opens Mr. X) |
| A6 C4 E2 E4 F6 | the same, from the other table |
| B5 C5 D1 E6 F1 | 8 bosses and B-E-A-T, no Energy Balancer |
| A1 B4 C3 C4 E6 | Blizzard Man only |
| A1 B1 B4 C4 E6 | nothing beaten (valid) |

## Checkpoints (`c6.CHECKPOINTS`, screen / CHR set / palette)

How the values were found: the Go-Explore autoplayer played each stage until the game itself
rewrote `$0684-$0686` (mid-stage checkpoint, then the boss shutter). Three were not reached and are
marked **rule**. The checkpoint is a snapshot of the current CHR set `$064F` and palette `$069E`,
and those change only on screen exits that carry non-zero values in the screen scripts (bank $39,
pointer table $82EB/$836B). Following the exits up to the checkpoint screen reproduces all the
natural values (Blizzard 85/1A from screen $0C's exit; Wind 8D + inherited 17; Flame inherited 87
+ 1F). The rule values were warp-checked by eye (`img/scout_ckpt_rule.png`).

| Stage | [1] mid-stage | [2] boss shutter | Boss room |
|---|---|---|---|
| Blizzard | 0D / 85 / 1A | 17 / 84 / 1C | 18 |
| Wind | 08 / 8D / 17 | 14 / 8E / 3D | 15 |
| Plant | 09 / 92 / 32 | not reached | 17 [code] |
| Flame | 0E / 87 / 1F | 16 / 87 / 1F | 17 |
| Yamato | 0A / 98 / 5B (rule) | not reached | 17, plate room 1D [code] |
| Tomahawk | 0A / 95 / 95 | not reached | 17, plate room 1F [code] |
| Knight | 0B / 00 / 78 | 16 / 00 / 7B | 17 |
| Centaur | 0A / 00 / A7 | 19 / 00 / A9 | 1A |
| Mr. X 1 | 0E / B9 / 6C | not reached | |
| Mr. X 2 | 08 / 00 / 00 | 10 / B8 / 00 | 11 |
| Mr. X 3 | 08 / 00 / 00 | 10 / B4 / D0 | 11 |
| Mr. X 4 | 09 / C4 / 00 (rule) | not reached | |
| Wily 1 | 0E / 00 / 81 | 12 / 8B / 81 | 13 |
| Wily 2 | 0A / 00 / 00 (rule) | not reached | |
| Wily 3 | 08 / A9 / 00 | (the boss starts with no new checkpoint) | 0E |
| Wily 4 | (capsule stage, no checkpoint) | | |

Entering a boss room sets `$0684` = boss screen - 1 ($3F:$FA20), so a death in the fight restarts in
the shutter corridor [seen]. Boss rooms use screen script $0A and the corridor script $0B ($4E for
Tomahawk); the plate-route rooms are listed at $3F:$F518 [code].

## Autoplay: `explore()` / `explore_to()`

`explore()` is a Go-Explore autoplayer, same design as `tools/analysis/cx/cheats.py`: an archive of
cells (stage, object-list window `$0649`, player screen `$046F`, X/32, Y/32, camera Y/64, camera Y
screen) -> savestate. It restores a cell, biased to the best score, and plays random held-button
macros (walk, jump, ladders, mashed B). `explore_to(e, until='ckpt'|'boss'|'any', damage=False)`
wraps it with the setup that worked: everything given except the current stage's own boss, Jet form
with frozen fuel, godmode. It returns `(state, reached, checkpoint)`.

What made it work on RM6:

- **Score by the object-list window `$0649` only.** Vertical sections scroll the camera freely
  (`$58`) without touching `$57`/`$046F`, and many paths turn back left after a ladder. Scoring by
  screen or X stalled every stage at a ladder top. `$0649` advances along the path in both cases.
- **Death test by the player's AI pointer** (`dying(r)`): pit death parks it at $38:$8F13 for 60
  frames, HP death at $38:$8E7F for 240 frames. Y >= $F0 is not a death test, because dropping into
  the next screen of a shaft passes there too.
- **Jet Rockman with frozen fuel** hovers over most gaps and enemies.
- **Mid-bosses** (Plant's dark-room gorilla, Tomahawk's rock dispenser, `img/scout_explore_midbosses.png`)
  need `damage=True`: score = `$0649`*16 + (63 - enemy HP)/4, with enemy HP/4 in the cell key.

Results (`build/research/rm6/rm6-scout/run2/ex*/`, `boss/`): mid-stage checkpoint reached in 13 of
16 stages, typically 25-130 s of CPU (75-400k frames); boss reached in 10. It got stuck at Yamato
screen 9 (a closed room whose exits are a ladder and a pillar the punch does not break), Mr. X 4
screen 3 (cannon platforms over spikes) and Wily 2 screen 4. Those are good targets for a
hand-written route if someone needs them.

## Savestates (`build/research/rm6/states/`)

All of them load and are verified by `run2/verify_states.py`; contact sheets
`img/scout_states.png` and `img/scout_checkpoints.png`. Inventory = whatever the game had at that
point (new-game inventory for Robot Master stages; the all-clear password's for the fortress).

| File | What | How made |
|---|---|---|
| `intro.state` | intro story scene, Mr. X on screen: "へいわの ための / だい1かい せかいロボット せんしゅけん。/ しかし・・・" [text] ("For peace, the 1st World Robot Tournament. But...") | boot + START |
| `title.state` | title screen, GAME START cursor, title loop running | boot, skip intro |
| `password.state` | empty password grid | PASS WORD |
| `stage_select.state` | new-game stage select (nothing beaten) | GAME START |
| `stage_select_all.state` | stage select after the all-clear password (Mr. X portrait in the centre, B/E/A/T on the plate stages) | password screen |
| `stage_<name>.state` x8 | each Robot Master stage after READY, playable | stage select + START |
| `mrx1.state` | Mr. X Fortress 1 start (after the fortress map) | `stage_select_all` + START on the centre |
| `mrx2..mrx4`, `wily1..wily4.state` | each fortress stage start, playable | previous stage + `$F0` = 1 |
| `<name>_ck1.state` x15 | the mid-stage checkpoint of every stage except Wily 4, playable | RAM warp from that stage's start state |
| `<name>_ck2.state` x8 | boss shutter corridor (blizzard, wind, flame, knight, centaur, mrx2, mrx3, wily1) | RAM warp |
| `<name>_boss.state` x8 | boss intro (bar filling) for the same eight | `_ck2` + hold RIGHT until `$0642` != 0 |

## Images

- `img/scout_states.png`: every start state (menus, 8 Robot Master stages, 8 fortress stages).
- `img/scout_checkpoints.png`: every checkpoint, shutter and boss-intro state.
- `img/scout_ckpt_warp.png`: natural checkpoint moment (left) vs. RAM warp to it (right), ten stages.
- `img/scout_ckpt_rule.png`: rule-derived checkpoints (Yamato, Mr. X 4 with and without its CHR set, Wily 2) and Mr. X 1.
- `img/scout_passwords.png`: 12 generated passwords accepted by the real screen.
- `img/scout_password_edge.png`: the empty and Blizzard-only passwords accepted; 4 or 6 orbs give PASS WORD ERROR.
- `img/scout_fortress_starts.png`: all-clear stage select and the eight fortress starts.
- `img/scout_mrx_map.png`: the Mr. X fortress map path cutscene before stage 1.
- `img/scout_gameover.png`: game over: GAME OVER over the password, then STAGE SELECT / CONTINUE.
- `img/scout_no_rematch.png`: walking into a beaten boss's room beams Rockman out.
- `img/scout_explore_midbosses.png`: where the plain autoplayer stalled (Plant's gorilla, Tomahawk's dispenser, Yamato's climb).
- `img/scout_pause_flags.png`: pause menu with single progress flags poked (see `ram.md`).
- `img/scout_soundplayer_forced.png`: the dead bank-$28 sound player forced to run (the only SELECT handler).

## Lessons for Rockman 6 GP

- **Keep the `$F0` exit-code loop.** Respawn-at-checkpoint (`$F0` = 2) is a clean, general warp.
  A GP debug menu (bound to SELECT, which vanilla never uses) can offer "stage / checkpoint / items"
  with three pokes and `$F0` = 2, the same mechanism this toolkit uses.
- **Checkpoints are just (screen, CHR set, palette)** and the screen scripts in bank $39 own them
  (`LDA #scr / JMP $8416`, or `LDA $57 / JMP $8416` for "here"). Adding or moving GP checkpoints is
  data work in those scripts, as long as the CHR/palette snapshot rule is respected.
- **Passwords are full.** Five orbs carry exactly 12 bits + 1; GP's extra progress needs a new scheme
  or save RAM.
- **Testing GP stages**: with `explore_to()` and `damage=True`, most vanilla stages reach their
  checkpoint in a few minutes of CPU. The same harness on GP builds is a cheap "is it beatable /
  softlock-free" smoke test. Stalls point at sections needing a specific skill (Power punch walls,
  precise platforming).
- **Beware hidden rules when editing bosses**: the no-rematch beam-out, the shutter checkpoint and
  the two-boss-room plate stages (`$F518` screens) are all keyed on stage id and screen number, so
  moving a boss room means updating `$3F:$F518` and the flag logic at `$3F:$F4EB`.
