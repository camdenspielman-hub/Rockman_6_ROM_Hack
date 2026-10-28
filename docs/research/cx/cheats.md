# Rockman CX cheat sheet, warps and savestates (cx-scout)

Scope: everything another CX investigator needs to get anywhere in *Rockman CX* v1.1 quickly: the RAM map, the save
format and checksum, the boot flow, the stage-select layout, the checkpoint system, the Dr. Light fortress route,
50 savestates, and the helper module `tools/analysis/cx/cheats.py`. Surprises found on the way are in §9.

Tags: **[seen]** observed in the emulator, **[code]** read from disassembly or data, **[text]** in-game text,
**[doc]** readme, **[guess]** speculation. ROM: `roms/cx_en.nes` (the JP build shares every RAM address and routine
listed here; only text and fonts differ).

---

## 0. Quick start

```python
import sys; sys.path.insert(0, 'tools/analysis'); sys.path.insert(0, 'tools/analysis/cx')
from emu import Emu
import cheats as cx

e = Emu('roms/cx_en.nes')               # one Emu per process (stable-retro limit); reuse it with e.load()
e.load(cx.state('fire_mario_cp2'))      # any state in build/research/cx/states/ (list in §1)
cx.godmode(e)                           # freeze HP, lives and the i-frame timer
cx.give_all_weapons(e)                  # all 8 boss weapons + full energy + 4 E-tanks
print(cx.info(e))                       # 'stage 03(fire_mario) room 14 x 80 y 94 hp 24/24 lives 8 ...'

# or build a start from power-on (title.state):
cx.warp(e, 3)                           # fresh start of stage 3 via a crafted save + the stage select
cx.warp_cp(e, 10, 2)                    # Dr. Light stage 3 ($0A), checkpoint 2
cx.warp(e, 9)                           # Dr. Light stage 2 ($09): walks the fortress map up the ladder
cx.new_game(e)                          # title -> NEW GAME -> DATA 1 -> opening stage
```

Gotchas: after `e.load()`, run one frame before `e.shot()` (the frame buffer is not in the state). States carry no
frozen cheats; apply `godmode()` yourself. `godmode` does not stop pit deaths (you respawn at the checkpoint).

---

## 1. Savestates (`build/research/cx/states/`)

All made from crafted saves (max HP 24, 8 lives, 0 E-tanks, Ubercharge 0, no hearts). Robot-master stages have no
bosses beaten; fortress stages have all 8 beaten and the right fortress progress. Every state below was loaded and
checked with `cx.playable()` (LEFT/RIGHT moves the player) [seen]; screenshots in §8.

| State | What it is |
|---|---|
| `title.state` | Title screen, NEW GAME / LOAD GAME, frame 3000 after power-on |
| `opening_start` | Opening stage (`$0F`) at the foot of Wily's tower, right after NEW GAME → DATA 1, room `$17` |
| `opening_cp1` | Opening stage checkpoint 1 (room `$1D`): you are now **Quick Man** (40 HP), after the Guts Man scene (§9) |
| `stage_select` | Stage select from a fresh save (cursor on Cheat Man, nothing beaten) |
| `stage_select_allbosses` | Stage select with all 8 beaten: portraits blank, Dr. Light in the centre box |
| `cheat_man`, `air_man`, `whispy_woods`, `fire_mario`, `yoshino_man`, `mega_man`, `kamen_rider`, `bomberman` | Robot-master stage starts (after READY) |
| `<boss>_cp1` … `_cp4` | Each robot-master stage's checkpoints (Cheat Man 1-3, Air Man 1-4, the others 1-2). The last one is the restart point nearest the boss |
| `light1` … `light6` | Dr. Light fortress stages 1-6 = stage IDs `$08`-`$0D`, at the start |
| `light1_cp1`, `light3_cp1/2`, `light4_cp1/2`, `light5_cp1/2`, `light6_cp1/2` | Fortress checkpoints. `light1_cp1` is Light 1's boss room (scroll locked) |
| `ending`, `ending_cp1`, `ending_cp2` | Stage `$0E`, the final stage (the big shadow robot is on screen at once) |

`light2.state` is stage `$09`, entered from the fortress map by climbing the ladder to Quick Man (§5).

---

## 2. Boot flow [seen]

1. **Attract intro** (about 2,400 frames): story text typed under a night city skyline beside a grey tower, e.g.
   *"…desire of Dr. Wily. His robots are world-famous."*, *"While Dr. Wily thinks he can win if he creates many
   robots of only one kind."*, *"Thus, a new fake Mega Man has been sent out to the world…"* [text]. Then the
   camera climbs the tower, as in RM2's intro.
2. **Title** (`title.state`): "MEGA MAN CX" logo, NEW GAME / LOAD GAME, "2017 VER 1.1 HIMAJIN JICHIKU".
3. **NEW GAME** → slot list DATA 1 / DATA 2 / DATA 3, with the fake Rockman standing on the tower roof. A new game
   overwrites the chosen slot. **LOAD GAME** → same slot list, then straight to the stage select.
4. Choosing a slot on NEW GAME scrolls down the tower to a red-sky city: READY, and the **opening stage** (stage ID
   `$0F`, starting room `$17`) begins. You are the grey fake Rockman with 24 HP and 8 lives.
5. The opening stage plays out a story (Guts Man captures you, Quick Man takes over, §9) and ends in a Guts Man fight.
   Afterwards the game goes to the stage select.

`cx.new_game(e, slot)` reproduces steps 2-4 (title + START, 1,200 frames, START, 1,400 frames, wait for control).
`cx.to_stage_select(e, slot, **save)` writes a valid save record into WRAM on the title screen and LOAD GAMEs it.

---

## 3. Stage select [seen][code]

The layout is not RM2's 3×3 grid. Top row: five panels; middle: one large empty frame; bottom row: four panels.

```
 [WHISPY WOODS] [FIRE MARIO] [Dr.L logo] [KAMEN RIDER] [BOMBER MAN]
                     [       big centre frame        ]
 [CHEAT MAN]     [YOSHINO MAN]      [MEGA MAN]          [AIR MAN]
```

While this screen runs, `$2A` is the **cursor**, not the stage. Cursor values (`cx.SEL`):

| `$2A` | Panel | Stage ID |
|---|---|---|
| 0 | Dr. L logo (top centre): enters the Dr. Light fortress once all 8 are beaten | `$08`+ |
| 1 | Whispy Woods | 2 |
| 2 | Fire Mario | 3 |
| 3 | Kamen Rider | 6 |
| 4 | Bomberman | 7 |
| 5 | Air Man | 1 |
| 6 | Mega Man | 5 |
| 7 | Yoshino Man | 4 |
| 8 | Cheat Man | 0 |

LEFT/RIGHT/UP/DOWN move the cursor (seen: LEFT from 0 → 2 → 1, DOWN from 3 → 6, etc.). Poking `$2A` and pressing
START enters any stage. Bytes that change on this screen: `$2A` (cursor), `$EA` (frame counter), `$E2/$E3`,
`$F0/$F1`, `$FA` (sprite/PPU pointers). A beaten boss's portrait is blanked (`$1A:8027` loops over `$9A` bits).
With `$9A = $FF` the centre frame shows Dr. Light raising a hand, and START on the logo goes to the fortress.

Stage IDs (`cx.STAGES`): `0` Cheat Man, `1` Air Man, `2` Whispy Woods, `3` Fire Mario, `4` Yoshino Man, `5` Mega Man,
`6` Kamen Rider, `7` Bomberman, `8`-`$0D` Dr. Light 1-6, `$0E` final stage, `$0F` opening stage.

---

## 4. RAM map

### CPU RAM

| Address | Meaning | Evidence |
|---|---|---|
| `$06C0` | Player HP (24 = `$18` at the start; 40 as Quick Man) | [seen] HUD bar and hit diff |
| `$06C1` | Boss HP (object slot 1). Guts Man starts at 40 | [seen] |
| `$0099` | Max HP. Reloaded from the save slot at every stage start; +4 per heart tank | [code] `$1F:8C07` |
| `$009A` | Bosses beaten = weapons owned. Bit n = stage n = weapon id n+1 | [seen] menu per bit, [code] `$C23C` |
| `$009B` | bit 7: playing Quick Man. bits 4-6: fortress progress (Light stages cleared). bits 0-3: see §6 | [code] `$FB10`, `$1F:9100` |
| `$004B` | Invincibility timer: `$6E` after a hit, counts down 1/frame; each Ubercharge use adds `$34` | [seen] |
| `$002A` | Stage ID (on the stage select: the cursor, §3) | [seen][code] |
| `$0440` | Player room (screen index along the stage, also for vertical screens) | [seen] |
| `$0460` / `$04A0` | Player X / Y pixel | [seen] |
| `$0038` | Level segment (which part of the stage's screen list is loaded) | [code] `$C503` |
| `$00B0` | Checkpoint index, recomputed at death (§5). Reused as scratch on other screens | [code] `$C1AF`, `$C4D7` |
| `$0014` / `$0015` | Scroll limits (first / last room of the current section) | [code] `$C50B` |
| `$00A9` | Equipped weapon: 0 buster, 1-8 boss weapons, 9-11 items; 12 = E-tank cursor in the menu | [seen] |
| `$009C`-`$00A6` | Energy of weapon id 1-11 (address = `$9B` + id). Full = `$28` | [seen] |
| `$00A4` / `$00A5` / `$00A6` | Item 1 Floor / Item 2 Subtank / Item 3 Ubercharge energy | [seen] |
| `$00A7` | E-tanks | [seen] menu |
| `$00A8` | Lives | [seen] menu |
| `$0098` | Saved byte; incremented up to `$C8` under a condition in `$1F:9110` [guess: a counter] | [code] |

Weapon ids and names [seen, pause menu]: 0 MEGAMAN (buster), 1 CHEAT SABER, 2 DEAD RINGER, 3 RINGO SHIELD,
4 FIRE BALL, 5 PRINT CUTTER, 6 MEGA BUSTER, 7 RIDER KICK, 8 POWER BOMB, 9 1.FLOOR, 10 2.SUBTANK,
11 3.ÜBERCHARGE. The menu shows the left column 0-5 and the right column 6-11; E-tanks and lives below.
Select + UP/DOWN cycles `$A9` through owned weapons and the three items (`$3B:B770`) [code].

### WRAM (battery)

| Address | Meaning |
|---|---|
| `$7FF0` | Current save slot (0-2) [code] |
| `$7FF8 + stage` | 1 = this stage's heart tank is taken. Saved fields exist for stages 0, 3, 5 and 7 [code] |
| `$7420 + 3·field + slot` | Save records (below) |

### Save record

Slot `s`, field `f` lives at `$7420 + 3f + s`. Fields: 0 max HP (`$99`), 1 bosses (`$9A`), 2 flags (`$9B`), 3 Ubercharge
(`$A6`), 4 E-tanks (`$A7`), 5 lives (`$A8`), 6 checksum, 7-10 heart flags (`$7FF8`, `$7FFB`, `$7FFD`, `$7FFF`), 11 `$98`,
12-13 unused (included in the sum). Checksum = 8-bit ADC chain (CLC once, carry propagates) over fields
0-5 and 7-13 [code `$FCD0` save, `$1F:8BD1` load]. A bad checksum wipes the slot to a new game (8 lives, 24 HP).
`cx.write_save()` / `cx.read_save()` implement it. Saving happens after every boss and every Light stage, and when a
heart tank is taken.

---

## 5. Checkpoints and stage banks [code][seen]

- Each 16 KB stage bank (`stage & 7` → 8 KB banks `2·(stage&7)` and `+1` at `$8000`/`$A000`) holds **one robot-master
  stage and one fortress/opening stage**, sharing a 6-entry restart table: `$BB06` rooms, `$BB30` segment (`$38`),
  `$BB37`/`$BB3D` scroll limits. Vanilla RM2 uses the same scheme for its Wily stages (banks 0-5), but its banks 6-7
  have only 3 entries; CX filled all eight banks.
- **On death** (`$C190`): `$B0` = (number of table entries ≤ current room) − 1. Stage 5 skips the −1 because Mega Man's
  stage runs **right to left** (start room `$0E`, checkpoints `$08`, `$01`).
- **Restart** (`$C4CD`): reads entry `$B0` of each table, sets the room, segment and scroll limits, and redraws.
- Room tiles depend on the stage ID: the rooms that belong to the bank's partner stage render with the wrong tiles
  if you force them under the other stage ID.
- Rooms per stage (`cx.CP_ROOMS`):

| Stage | Restart rooms | Shares bank with |
|---|---|---|
| 0 Cheat Man | `00 08 16 18` | 8 Light 1: `19 21` |
| 1 Air Man | `00 0A 14 17 20` | 9 Light 2: `2B` |
| 2 Whispy Woods | `00 0D 16` | `$0A` Light 3: `18 21 28` |
| 3 Fire Mario | `00 0C 14` | `$0B` Light 4: `17 21 2A` |
| 4 Yoshino Man | `00 07 16` | `$0C` Light 5: `18 1D 29` |
| 5 Mega Man | `0E 08 01` (reverse) | `$0D` Light 6: `15 16 20` |
| 6 Kamen Rider | `00 0A 13` | `$0E` final: `18 1A 28` |
| 7 Bomberman | `00 08 11` | `$0F` opening: `17 1D` |

**Checkpoint warp** (`cx.warp_cp(e, stage, cp)`): warp to the stage start, drop the player below the screen
(`$04A0 = $F0`), and hold `$0440` at the target room until the life counter drops. The restart code then picks that
checkpoint. The life is refunded. Poking `$B0` directly does nothing, because death recomputes it.

### Dr. Light fortress route [seen]

After Light 1 the game shows a **walkable fortress map**: Dr. Light's house at night with the route drawn on it, and
below it a small scene with the fake Rockman on the floor, a ladder to a ledge with **Quick Man**, and **Guts Man** on
the floor. Climb the ladder and walk into Quick Man → stage `$09` (Light 2, a gear-and-chain tower). Walk along
the floor into Guts Man → stage `$0A` (Light 3), skipping `$09`. At other progress values the map plays automatically.
The stage-clear code (`$C253`) sets progress = stage − 7 and then increments `$2A`, so the Guts Man route never
visits `$09` [code]. `cx.fortress_route(e, quick_man=True)` walks either route.

---

## 6. Item upgrades and other progress bits [code]

- At the weapon-get screen (`$1B:BC93`) the game counts the bits of `$9A`. After the **1st, 3rd and 5th** boss it
  plays an extra event (scene ids `$0E`, `$0C`, `$0D`, palette set from `$E2AB`) and ORs a bit into `$9B`:
  1st boss → `$04`, 3rd → `$01`, 5th → `$02` (table `$9669+X`). These are the "Dr. Light upgrades your items"
  steps from the readme [doc], so the item upgrade level lives in `$9B` bits 0-2 [guess, see TODO].
- The same routine refills Ubercharge to `$28` while the event runs and restores it afterwards.
- **Ubercharge charges when you get hurt**: `$A6` goes up by 1 per hit taken [seen: Guts Man fight log and
  checkpoint warps]. It starts at 0 on a new game and is saved.

(TODO: confirm the item behaviour per upgrade level.)
