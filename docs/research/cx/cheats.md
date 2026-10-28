# Rockman CX cheat sheet, warps and savestates (cx-scout)

Scope: everything another CX investigator needs to get anywhere in *Rockman CX* v1.1 quickly: the RAM map, the save
format and checksum, the boot flow, the stage-select layout, the checkpoint system, the Dr. Light fortress route,
63 savestates, and the helper module `tools/analysis/cx/cheats.py`. Surprises found on the way are in §9.

Tags: **[seen]** observed in the emulator, **[code]** read from disassembly or data, **[text]** in-game text,
**[doc]** readme, **[guess]** speculation. ROM: `roms/cx_en.nes`. Every routine and table cited here is byte-identical
in `roms/cx_jp.nes` (checked: death/restart, save/load, checkpoint tables, item and upgrade code); the two builds
differ in 23,771 bytes, mostly the text banks `$26-$29`, `$13`, `$1B`, `$1E` [measured].

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

63 states, made from crafted saves (max HP 24, 8 lives, 0 E-tanks, Ubercharge 0, no hearts). Robot-master stages
have no bosses beaten; fortress stages have all 8 beaten and the right fortress progress. All 60 gameplay states pass
`cx.playable()` (LEFT/RIGHT moves the player) and the 3 menu states (`title`, `stage_select*`) were checked by
screenshot [seen]; see §8.

| State | What it is |
|---|---|
| `title.state` | Title screen, NEW GAME / LOAD GAME, frame 3000 after power-on |
| `opening_start` | Opening stage (`$0F`) at the foot of Wily's tower, right after NEW GAME → DATA 1, room `$17` |
| `opening_cp1` | Opening stage checkpoint 1 (room `$1D`): you are now **Quick Man** (40 HP), after the Guts Man scene (§9) |
| `opening_boss` | Opening stage room `$26`: Quick Man vs. Guts Man, both at 40 HP |
| `stage_select` | Stage select from a fresh save (cursor `$2A = 0` = the Dr. L logo, nothing beaten; `info()` prints this as "cheat_man") |
| `stage_select_allbosses` | Stage select with all 8 beaten: portraits blank, Dr. Light in the centre box |
| `cheat_man`, `air_man`, `whispy_woods`, `fire_mario`, `yoshino_man`, `mega_man`, `kamen_rider`, `bomberman` | Robot-master stage starts (after READY) |
| `<boss>_cp1` … `_cp4` | Each robot-master stage's checkpoints (Cheat Man 1-3, Air Man 1-4, the others 1-2). The last one is the restart point nearest the boss |
| `light1` … `light6` | Dr. Light fortress stages 1-6 = stage IDs `$08`-`$0D`, at the start |
| `light1_cp1`, `light3_cp1/2`, `light4_cp1/2`, `light5_cp1/2`, `light6_cp1/2` | Fortress checkpoints. `light1_cp1` (room `$21`) is an empty sky room where the beam-in hangs unless you drop in from y=`$80`; no boss appeared under 4,000 frames of autorun |
| `ending`, `ending_cp1`, `ending_cp2` | Stage `$0E`, the final stage (the big shadow robot is on screen at once) |
| `<boss>_boss` (all 8 except Air Man) | In the boss room, boss bar full (40 HP = `$28`), player in control. Found with `autorun` / `explore` / `finish_boss` from the last checkpoint. Rooms: Cheat Man `$17`, Whispy `$17`, Fire Mario `$15`, Yoshino `$17`, Mega Man `$00`, Kamen Rider `$16` (not scroll-locked), Bomberman `$12` |
| `light3_boss`, `light5_boss`, `light6_boss` | Fortress boss rooms, boss at 40 HP: Light 3 = a giant Guts Man riding a tank (RM2's Guts Tank reskinned, room `$2B`); Light 5 = a small robot on teleporter pads (room `$24`, not scroll-locked); Light 6 = the "DR.LIGHT TELEPORT SYSTEM" hall (room `$20`, the boss is not visible at once) |
| `air_man_midboss` | Air Man's stage, room `$16`: a **Quick Man** mid-boss (40 HP). Air Man himself is further on |
| `air_man_deep` | Air Man's stage, room `$26`: the furthest point the explorer reached, inside a wind-arrow and fan maze. Air Man's boss room is still unfound |

`light2.state` is stage `$09`, entered from the fortress map by climbing the ladder to Quick Man (§5).
`python3 -I tools/analysis/cx/verify_states.py` re-checks every state and redraws `img/cheats_states.png` (§8).

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
5. The opening stage plays out a story (Guts Man captures you, Quick Man takes over, §9). As Quick Man you fight
   **Guts Man** (room `$26`, 40 HP), then break the cage holding the fake Rockman (room `$29`; the cage uses the boss
   HP bar). Quick Man: *"I'll scout ahead and collect as much information [in Dr.] Light's lab as I can."* …
   *"Now there're 8 Robot Masters including Mega Man."* … *"See you later."* [text]. Then the stage select, with
   you back as the fake Rockman (`$9B` bit 7 cleared).

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
| `$0099` | Max HP. Re-read from the save slot on LOAD GAME and at every respawn (poking the save's max HP to 28 and dying gave `$99 = 28`); +4 per heart tank | [code] `$1F:8C07`, [seen] |
| `$009A` | Bosses beaten = weapons owned. Bit n = stage n = weapon id n+1 | [seen] menu per bit, [code] `$C23C` |
| `$009B` | bit 7: playing Quick Man. bits 4-6: fortress progress (Light stages cleared). bits 0-3: see §6 | [code] `$FB10`, `$1F:9100` |
| `$004B` | Invincibility timer: `$6E` after a hit, counts down 1/frame; each Ubercharge use adds `$3C` (seen as +52 per 8-frame press cycle) | [seen][code `$DC76`] |
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
| `$0098` | Saved byte (field 11). `$1F:9110` increments it up to `$C8` when `$97 = $C0`, bit 7 of `$9B` is clear and one of `$32-$34` is 3. Meaning unknown [guess: a statistics counter] | [code] |

Weapon ids and names [seen, pause menu]: 0 MEGAMAN (buster), 1 CHEAT SABER, 2 DEAD RINGER, 3 RINGO SHIELD,
4 FIRE BALL, 5 PRINT CUTTER, 6 MEGA BUSTER, 7 RIDER KICK, 8 POWER BOMB, 9 1.FLOOR, 10 2.SUBTANK,
11 3.ÜBERCHARGE. The menu shows the left column 0-5 and the right column 6-11; E-tanks and lives below.
Select + UP/DOWN cycles `$A9` through owned weapons and the three items (`$3B:B770`) [code].

### WRAM (battery)

| Address | Meaning |
|---|---|
| `$7FF0` | Current save slot (0-2) [code] |
| `$7FF8 + stage` | 1 = this stage's heart tank is taken. Saved fields exist for stages 0, 3, 5 and 7 (Cheat Man, Fire Mario, Mega Man, Bomberman), so those are the four heart-tank stages [code] |
| `$7420 + 3·field + slot` | Save records (below) |

### Save record

Slot `s`, field `f` lives at `$7420 + 3f + s`. Fields: 0 max HP (`$99`), 1 bosses (`$9A`), 2 flags (`$9B`), 3 Ubercharge
(`$A6`), 4 E-tanks (`$A7`), 5 lives (`$A8`), 6 checksum, 7-10 heart flags (`$7FF8`, `$7FFB`, `$7FFD`, `$7FFF`), 11 `$98`,
12-13 unused (included in the sum). Checksum = 8-bit ADC chain (CLC once, carry propagates) over fields
0-5 and 7-13 [code `$FCD0` save, `$1F:8BD1` load]. A bad checksum wipes the slot to a new game (8 lives, 24 HP).
`cx.write_save()` / `cx.read_save()` implement it. Saving happens after every boss and every Light stage, and when a
heart tank is taken.

**Heart tank** [code]: item object 6 (handler table at `$3C:93A5`, lo bytes, hi bytes `+$C0`) → `$3D:BD85`. If
`$7FF8+stage` is 0 and the player touches it, it writes `$99 + 4` straight into the save slot's max-HP field, sets
`$7FF8+stage = 1` and saves the rest (`$FCD8`). `$99` itself is not changed, so the +4 appears at the next respawn or
stage start. The tank locations themselves were not searched for here.

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

## 6. Item upgrades ("improved or worsened" by Dr. Light) [code][seen]

After a boss's weapon-get screen ("You got: Power Bomb", over a full-screen Rockman artwork recoloured in the
weapon's colours), routine `$1B:BC86` counts the bits of `$9A`. The loop (`LDA $9A / LSR / BEQ / BCC / INC`)
exits before counting the last bit it shifts out, so the count is **popcount − 1**. For counts 1, 3 and 5, that is
after the **2nd, 4th and 6th** robot master, it plays a second "You got:" screen for an item and ORs a bit into
`$9B` (table `$1A:9669 + (X−4)`, scene ids `$0E/$0C/$0D` → pseudo-stage `$0A/$08/$09` for the text and palette):

| Boss # | Screen [text] | `$9B` bit | What changes [seen in the emulator] |
|---|---|---|---|
| 2nd | "You got: Übercharge" (grey Rockman) | `$04` | Base: B adds `$3C` (1 s) to the i-frame timer `$4B` for 1 unit, capped by overflow at about 4 s (`$DC69`). Upgraded: with a **full bar** (`$A6 = $28`), B deploys a full Über: object 8 holds `$4B` at 60 while the bar drains about 1 unit per 15 frames (about 10 s of invincibility), like TF2's Medic |
| 4th | "You got: Instant Floor" (red Rockman) | `$01` | Base: the platform holds you for about 220 frames (3.7 s): a 187-frame phase, then a 36-frame blink. Upgraded (`$E18D`): the first phase is skipped and the platform holds you for only about 35 frames. This is the "worsened" case |
| 6th | "You got: Sub Tank" (teal Rockman) | `$02` | Base: hold B with the Subtank equipped to move 1 unit every 7 frames from the tank into the target; UP/DOWN while holding picks the target (`$AC`: 0 = HP, n = weapon n). Upgraded (`$1F:AB3A`): one press dumps the whole tank at 1 unit per 2 frames, and it keeps draining after the target is full |

- The routine also refills Ubercharge to `$28` while the event runs and restores the old value afterwards
  (`$BC93-$BC99`, `$BCC2`).
- **Ubercharge charges when you get hurt**: `$A6` rises by 1 per hit taken [seen: Guts Man fight log, checkpoint
  warps]. It starts at 0 on a new game and is saved (save field 3).
- Reproduce: `python3 -I build/research/cx/cx-scout2/upgtext.py` kills Bomberman with `$9A` = `$01`/`$07`/`$1F` and
  screenshots the three upgrade screens (image in §8).

---

## 7. Helper module `tools/analysis/cx/cheats.py`

| Function | What it does |
|---|---|
| `state(name)` | Path of `build/research/cx/states/<name>.state` |
| `info(e)` | One-line RAM summary (stage, room, x, y, HP/max, lives, E-tanks, weapon, `$9A`, `$9B`, Ubercharge, i-frames) |
| `godmode(e)` / `nogod(e)` | Freeze HP at max, lives at 9, i-frames at `$40` (you pass through enemies). Pits still kill |
| `refill(e)`, `give_all_weapons(e, etanks=4)` | Full HP + all 11 energies; `$9A = $FF` (all weapons) + E-tanks |
| `write_save(e, slot, maxhp, bosses, flags, uber, etanks, lives, hearts, v98)`, `read_save(e, slot)` | Valid battery save record with checksum (§4) |
| `to_stage_select(e, slot, **save)` | From `title.state`: write the save, LOAD GAME it, wait for the stage select |
| `warp(e, stage, **save)` | Fresh start of any stage 0-15 (crafted save → stage select → START, or NEW GAME for `$0F`, or the fortress-map ladder for `$09`). Returns frames until playable |
| `warp_cp(e, stage, cp)` | Same, then restart at checkpoint `cp` of `CP_ROOMS[stage]` via `kill(e, room)` |
| `kill(e, room=None)` | Drop the player below the screen; optionally hold the room byte so the restart picks that checkpoint; refunds the life |
| `new_game(e, slot)`, `fortress_route(e, quick_man)` | Boot to the opening stage; walk the fortress map to stage `$09` or `$0A` |
| `playable(e)`, `wait_playable(e)` | Does LEFT/RIGHT move the player?; run until it does (after READY, cutscenes) |
| `boss_active(e)`, `finish_boss(e)` | Scroll-locked room with boss HP in `$06C1`; set the boss to 1 HP and shoot it until it dies |
| `autorun(e, frames, direction, until)` | Dumb autoplayer: hold a direction, mash B, jump when stuck, try UP and back-off. Reached Fire Mario, Yoshino Man and Bomberman from their last checkpoint in about 330 frames |
| `explore(e, budget, done, score, cell, checkpoint)` | Go-Explore autoplayer (archive of cells `(stage, room, x>>4, y>>5)` → savestate; restore frontier cells and play random held-button macros, mashing for wall kicks). From the last checkpoint it found the Whispy Woods, Cheat Man and Mega Man boss rooms and Kamen Rider's arena in 1-60 s, and Air Man's Quick Man mid-boss; it did not solve Air Man's wind maze in 4 minutes. `boss_score` biases it toward damaging the boss |
| `CP_ROOMS`, `cp_table(rom, stage)`, `STAGES`, `WEAPONS`, `SEL` | Data tables (§3, §5) |

Recipes:

```python
cx.warp_cp(e, 3, 2); cx.autorun(e, 4000, until=cx.boss_active)   # walk into Fire Mario's boss room (~330 frames)
e.load(cx.state('bomberman_boss')); e.poke(cx.BOSSES, 0x01); cx.finish_boss(e)
e.run(2500)                          # 2nd boss beaten -> "You got: Power Bomb", then "You got: Übercharge"
cx.warp(e, 0, flags=0x80)            # start Cheat Man's stage with Quick Man physics (the sprite stays Rockman's)
cx.warp(e, 1, maxhp=40, etanks=9, uber=40, hearts=(1, 1, 1, 1))  # a late-game save
```

Background runs: `build/research/cx/cx-scout2/deepboss.py <state> <budget> [seed]` (explore until a boss bar
appears), `make_cps.py` (rebuild every checkpoint state), `saveboss.py` (autorun to a boss, wait for the bar, save).

---

## 8. Images

- `img/cheats_states.png`: every shared savestate, one frame after loading (all gameplay states verified playable).
- `img/cheats_stage_select.png`: the stage select at 2×: five panels on top (Dr. L logo in the middle), a big
  empty centre frame, four panels below.
- `img/cheats_fortress_route.png`: the fortress map after Light 1. Left column: walking toward the ladder; middle:
  climbing to Quick Man; right: the resulting stage `$09` (gears, chains, spikes).
- `img/cheats_shared_bank_whispy.png`: Whispy Woods' bank restarted at all six table entries. Entries 3-5 are
  Light 3's rooms drawn with Whispy's tiles, which shows the shared-bank layout of §5.
- `img/cheats_item_upgrades.png`: the three upgrade screens after the 2nd, 4th and 6th boss ("You got:
  Übercharge", "Instant Floor", "Sub Tank"), after the normal "You got: Power Bomb" screen.
- `img/cheats_weapon_bits.png`: the pause menu with one `$9A` bit set at a time (bit n → weapon n+1).
- `img/cheats_opening_story.png`: the opening stage's Guts Man scene: "Hey, Guts Man, what are you doing?",
  rocks, "You're far too unaware, gray man. I'm a member of Dr. Light Numbers.", "Now you're captured.",
  Guts Man carries the fake Rockman off, and **Quick Man** beams in as the new player character.

---

## 9. Surprises ("how crazy it gets")

- **You change characters mid-stage in the opening** [seen]. The fake Rockman meets Guts Man, who calls him
  "gray man", announces he is one of the "Dr. Light Numbers", throws rocks, and carries him off. Quick Man beams
  in and you finish the opening stage as Quick Man with 40 HP: a Guts Man fight, then you free your own captured
  body from a cage, and Quick Man leaves to "scout ahead" in Dr. Light's lab. (CX's history file mentions the beta2
  bug where dying in the opening stage turned you into Quick Man on respawn; the flag is `$9B` bit 7, cleared on
  death everywhere except stage `$09` [code `$1F:9100`].) Poking bit 7 in any stage gives Quick Man's physics (62 px
  of walking per 30 frames vs. 40, no dash) but keeps the Rockman sprite, since the tiles load at stage start [seen].
- **The fortress has a branching route chosen by walking** [seen]. After Light 1, the map screen is a tiny playable
  scene: climb to Quick Man for the optional stage `$09`, or walk to Guts Man and skip straight to `$0A`.
- **Mega Man's stage runs backwards** [code][seen]: you start at room `$0E` and go left to room `$00`; the death
  code has a special case for stage 5 so its checkpoints work in reverse. The boss room has a blue diamond backdrop
  that big dark-blue block shapes keep redrawing over, with Rock (the real Mega Man) as the boss [seen].
- **Every bank is shared by two stages**, including the opening stage (with Bomberman) and the final stage (with
  Kamen Rider) [code]. CX filled the two banks vanilla RM2 left with only three checkpoint entries.
- **Cheat Man's arena is a cheat-code dump**: a red wall tiled with hex strings like `00EA 24A1 C93D 8548`. During
  the fight the player is suddenly moved across the room (X `$18` → `$E8` within 20 frames, no input toward it), so
  Cheat Man apparently cheats with your position [seen]. His checkpoint 3 restores room `$18` with scroll limits
  `$19-$20`, so you respawn in a black room of glitchy-looking tiles [seen][code].
- **Fire Mario's boss room is World 1-4's bridge**: grey castle bricks, lava, the bridge and the axe, with Fire Mario
  where Bowser would stand [seen].
- **Air Man's stage has a Quick Man mid-boss** (room `$16`, 40 HP), and its later rooms are a maze of wind arrows
  [seen].
- **Kamen Rider's arena is not scroll-locked**: the fight happens in a normal scrolling room [seen].
- **Bosses have 40 HP** (`$28`), not RM2's 28 [seen].
- **Ubercharge charges when you get hurt** (+1 per hit), and the 2nd-boss upgrade turns a full bar into a TF2-style
  deployed Über (about 10 s of invincibility) [seen].
- **Dr. Light's "upgrades" can make items worse**: after the 4th boss the Instant Floor lasts about 0.6 s instead of
  3.7 s, and after the 6th the Subtank dumps its whole contents in one go [seen]. The bit-count loop also makes the
  upgrades arrive one boss later than its 1/3/5 constants suggest [code].
- **The weapon-get screen** is a full-screen Rockman artwork that fades in grey and is recoloured to the new weapon,
  with a Dr. L emblem bar and "You got: …" typed beside it [seen].
- **The game hands you every item upgrade before the final stage**: the warp's save had `$9B = $60`, but stage `$0E`
  runs with `$9B = $67`, all three upgrade bits set [seen].

---

## 10. Lessons for Rockman 6 GP

- **Design**
  - A character swap inside the very first stage (CX's Guts Man kidnapping) teaches the second moveset without a
    menu. RM6 GP could do the same with its own alternate character.
  - A walkable map that doubles as a route choice is cheap (one small scene, a ladder, two NPC triggers) and makes the
    fortress feel non-linear.
  - Upgrades that may *worsen* an item are funny once, but they should be telegraphed: here the screen only says
    "You got:", so the player discovers it by dying.
- **Technical**
  - CX keeps RM2's checkpoint tables and restart routine and just fills all eight banks, two stages per bank. If RM6 GP
    adds stages, extending existing tables is safer than adding a new mechanism.
  - The checkpoint is recomputed from the room at death. That makes "warp to checkpoint N" a two-line cheat
    (die with the room held), which is worth keeping for our own test tooling.
  - A popcount loop that exits on `BEQ` before counting the last bit is an easy off-by-one. Test progression events
    in the emulator with crafted save bits, as done here.
  - For our hack's test harness: crafted saves with a correct checksum, plus automatic `<stage>_cp<N>` and
    `<stage>_boss` states, turn every stage into a 1-second load. Build that early.
