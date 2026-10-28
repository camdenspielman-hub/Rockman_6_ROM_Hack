# Rockman 6 (J) RAM map, v0 (rm6-scout)

Status: **v0, complete for the requested fields** (second run of rm6-scout; the first was killed by a
container restart and its findings were recovered from its transcript). Tags: **[seen]** = verified in the emulator (how is noted),
**[code]** = from disassembly, **[guess]** = unverified. Helper constants for everything here live in
`tools/analysis/rm6/cheats.py`; the warp toolkit and savestates are in `cheats.md`.

ROM: `roms/rm6j.nes`, MMC3, 512 KB PRG, CHR-RAM. Linear disassemblies of every bank:
`build/research/rm6/rm6-scout/bXX.asm` (even banks at $8000, odd at $A000; `b38_8000.asm`,
`b39_8000.asm`, `b39_A000.asm`, `b3B_A000.asm` are the other mappings; fixed `b3E.asm`/`b3F.asm`).

## Stage IDs (`$51`)

| $51 | Stage | Stage-select cell (col,row) | Boss flag (byte,bit) | Beat plate |
|---|---|---|---|---|
| 0 | Blizzard Man | (0,0) | $0692 b0 | |
| 1 | Wind Man | (1,0) | $0693 b0 | |
| 2 | Plant Man | (0,1) | $0695 b0 | |
| 3 | Flame Man | (2,0) | $0694 b0 | |
| 4 | Yamato Man | (0,2) | $0693 b1 (b2 = plate route) | E |
| 5 | Tomahawk Man | (2,1) | $0692 b1 (b2) | B |
| 6 | Knight Man | (1,2) | $0695 b1 (b2) | A |
| 7 | Centaur Man | (2,2) | $0694 b1 (b2) | T |
| 8-11 | Mr. X Fortress 1-4 | centre, once all 8 are beaten | - | |
| 12-15 | Wily Fortress 1-4 | after Mr. X 4 | - | |

[seen] stage-select cursor -> `$51` diff (8 entries), all 16 stages warped by RAM and recognised by their
graphics, the all-clear password shows B/E/A/T on exactly Tomahawk/Yamato/Knight/Centaur.
[code] grid table $3F:$F232 (`00 01 03 FF / 02 FF 05 FF / 04 06 07 FF`; the centre gives 8 only when
`$05C8` = 0, i.e. all eight beaten); per-stage tables in bank $3E at $DF25 (level bank pair), $DF85
(base CHR set), $DF95 (palette), $DFA5 (music id); stage -> flag byte $3F:$F6B3, bit masks $F6BB/$F6C3,
plate-route boss screens $3F:$F518 = `FF FF FF FF 1D 1F 1A 17` (stages 4-7 have two boss rooms; beating
the boss in the second one sets bit 2 = the plate).

## Zero page

| Addr | Meaning | Tag |
|---|---|---|
| $00-$0F | scratch / pointer temps (`$08/$09` = indirect JMP vector for AI calls); on the stage select `$04`/`$05` = cursor column/row | [code]; [seen] cursor |
| $10, $11, $15-$18 | far-call ($CB28) and bank-switch ($CB91) temps; `$11` = far-call id | [code] |
| $21-$3F | 4 cooperative threads (n = 0-3): `$21+n` state (0 off, 1 waiting, 2 running, 8 new, $80 suspended), `$25+n` wait frames, `$29+n` saved S / start lo, `$2D+n` start hi, `$34+n`/`$38+n` saved $8000/$A000 banks, `$3C+n` saved `$10`; `$33` = current thread. Stacks: tops $013F/$015F/$017F/$019F, scheduler at $01FF | [code] $C568-$C61B; [seen] pause sets `$22`/`$23` = $80 |
| $40 / $41 | joypad 1 / 2 held. A=$80 B=$40 SELECT=$20 START=$10 UP=$08 DOWN=$04 LEFT=$02 RIGHT=$01 | [code] $C711, [seen] |
| $42 / $43 | joypad 1 / 2 newly pressed this frame | [code] [seen] |
| $44 / $45 | previous held, inverted (edge detection) | [code] |
| $4A/$4B/$4C | MMC3 bank shadows ($8000 bank, $A000 bank, last $8000 command) | [code] PLAN.md |
| $4D-$50 | scroll work: `$4D/$4F` camera X + 4 (lo/hi), `$4E/$50` camera Y | [code] $DC78 |
| **$51** | **stage id** (table above) | [seen] |
| $52/$53 | per-stage values from $DF35/$DF45 | [code] |
| **$56 / $57** | **camera X pixel / camera screen** (`$57` = screen number along the level path) | [seen] scrolls with the player |
| $58 / $59 | camera Y pixel / Y screen. `$58` scrolls during a vertical transition. **(corrected by critic)** `$57` and `$046F` do change: they switch to the target screen on the *first* frame of a vertical transition, and `$0697` follows when the ~120-frame scroll ends | [seen] Flame ladder climb: `$58` $E4 -> 0 over 100 frames; [seen, critic `emuchecks2.py`] Blizzard 0C -> 0D and 05 -> 06 down exits: `$57`/`$046F` = new screen at frame 1, `$0697` at frame ~122; [code] $DC87 |
| $63, $67, $6E, $6F | per-stage level-data pointers / bank (`$6F` = level bank) | [code] $DC00 |
| $70-$7F | current screen's object-list pointers (`$74..$7F`, bank $3A tables) | [code] $3A:$8032 |
| $80 | per-screen flag index (bitfield at $0340) | [code] $DB98 |
| $8C | OAM write index | [code] |
| $8F | object loop index (current slot) | [code] $E438 |
| **$94** | **player state**: 0 stand, 1 tiptoe start, 2 walk, 3 ?, 4 ladder, 6/7 airborne | [seen] trace (0/1/2/7), [code] (4 = ladder) |
| $95 | player sub-timer | [code] |
| $96 | "damage taken this frame" latch | [code] $8F89 |
| $99 / $9A | player input direction / jump-request bits (derived from `$40`) | [code] $D434 |
| **$9B** | **adaptor form: 0 normal, 1 Jet Rockman, 2 Power Rockman** | [seen] menu select -> 1/2 |
| **$9C** | **Rush Jet hover fuel**, $13 full, counts down while hovering, refills on landing | [seen] jet trace |
| $9D, $9E, $A0, $A1 | player action latches (slide, charge, shoot). **(corrected by critic, from `engine.md` 2.1/3.2)**: `$9E` = charge counter (+1 per frame while B is held, +2 for Power Rockman; half charge at `$24`, full at `$06AB` = `$5A`); `$9D` = Rush Jet fuel sub-counter (one fuel unit per 4 frames of flight). `$A0`/`$A1` still unassigned | [code] $803B, $38:$8651, $38:$825D; [seen] |
| **$A2** | **invincibility timer**: $3C after a hit, counts down; while non-zero no damage; the player blinks on bit 1 | [seen] every enemy contact sets 60 and costs 2-3 HP; freeze=2 -> no damage, no blink; [code] $8EA2, $8F72 |
| $A5 | ? set FF on hit | [code] |
| $A7 | player animation id | [code] |
| $A8 | player left X clamp (camera-relative, $10 normally) | [code] $8F31 |
| **$A9** | **lives** (menu shows it as-is; 1-up caps at 9; a death with `$A9` = 0 is game over) | [seen] pit death 2->1; [code] $8E8A, $B435 |
| $AE | current palette set id | [code] |
| $B0-$BF | sound request queue ring (write index `$D9`, read `$DB`); `$DC` = "play this id now" | [code] PLAN.md, [seen] |
| $DF/$E0/$E1 | RNG | [seen] change every frame |
| $EB-$EE | per-object motion temps: `$EB/$ED` X speed lo/hi, `$EC/$EE` Y speed lo/hi | [code] $E4CF |
| $EF | copy of `$0642` (boss bar) | [code] |
| **$F0** | **main-loop exit code**: 0 running, 1 stage clear, 2 respawn at checkpoint, 3 game over | [seen] poking 1/2 |
| $F1, $F2 | NMI handshake / "frame done" | [code] $C57F |
| $F3 | frame counter | [seen] |
| $F4 | IRQ split on/off | [code] PLAN.md |
| $F7 / $F9 | scroll X / Y shadows (`$F7` = `$56`) | [seen] |
| $F8/$FC, $FD, $FB | PPUCTRL, PPUMASK, mirroring shadows | [code] PLAN.md |

## Object table ($03A0-$063A): 23 slots x 29 field arrays

Slot k, field f lives at `base_f + k` (k = 0..$16). Slot 0 = the player; 1-3 = player shots (allocator
$E514 searches 3..0); 8-$15 = enemies, items, bosses (allocator $E59F searches $15..8); 4-7 and $16 =
special objects (Rush, weapons, screen effects). The object loop ($E438) walks all slots from $16 down,
maps `$0441,X` with $CBC0 and resumes each object's code at `$0413/$042A` (cooperative: an AI calls
$E46C to yield a frame, which stores its return address back here).

| Base | Field | Tag |
|---|---|---|
| $03A0 | object type id (0 = empty slot); spawn sets it from the level list ($3A:$81F0) | [code] [seen] |
| $03B7 | flags: b0 hidden (blink / death), b1 no-update, b5-7 OAM attribute (b6 = horizontal flip: $40 = facing right) | [seen] player $40/$00 with facing |
| $03CE | facing / direction: 1 right, 2 left | [seen] |
| $03E5 | **HP**; player full = $1B (27), negative = dead (`BMI` tests); boss HP = slot 8 (`$03ED`); $7F = invulnerable object | [seen] HUD bar follows poke; buster hits take enemy HP 4->3->2 (type $4D) and 2->1->0 (type $24), destroyed = negative; boss fight fills $03ED 0 -> $1B |
| $03FC | spawn index (which level-list entry made it, $FF = none), used to avoid respawn | [code] $E594 |
| $0413 / $042A | AI code pointer hi / lo (resume address) | [seen] player stand $8055, tiptoe $808A, walk $80AF, air $810B; **dying: pit $8F13 (60 frames), HP $8E7F (240 frames)**, then `$F0`=2; respawn beam $3B:$8DE2 |
| $0441 | AI code bank (pair mapped with $CBC0); player = $38 | [seen] |
| $0458 | sprite / animation bank | [code] $E21E |
| $046F / $0486 / $049D | **X screen / X pixel / X sub-pixel** | [seen] walking: +$01.4C per frame |
| $04B4 / $04CB / $04E2 | **Y screen / Y pixel / Y sub-pixel** | [seen] jumping |
| $04F9 / $0510 / $0555 | animation: frame count, frame index (x2), frame timer | [code] $E225 |
| $0527 / $053E | animation script pointer hi / lo | [code] |
| $056C | contact / hit result flags ($20, $30, $40 written on collisions). **(corrected by critic, from `engine.md` 2.1)**: the **hit latch**: a player shot touching this object copies its attack byte here, and the victim's damage routine reads and clears it | [code] $8F6C, $38:$8FDF |
| $0583 / $059A | ~~hitbox half-width / half-height~~ **(corrected by critic, from `engine.md` 1.3)**: `$0583` = **attack byte** (high nibble = collision class, low nibble = contact damage / shot power), `$059A` = **hit box id** (size table used by `$3F:$F72A`); both come from the 6-byte AI header (AI-1, AI-3) | [code] $3F:$EBD5 |
| $05B1 / $05C8 | player: **Y velocity lo / hi** (signed, + = down; gravity +$00.40 per frame). **(corrected by critic)** the jump stores `$FA.CC` (`$FB.CC` from oil type 9); the first airborne frame reads `$FB.0C` after one gravity step, the second `$FB.4C` (the value this table used to give) | [seen] trace; [code] $38:$80D7-$80EC |
| $05B1-$0624 | ($05B1, $05C8, $05DF, $05F6, $060D, $0624) six general AI variables for other objects | [code] |

Player X speed is not stored: it is looked up each frame from $38:$801B/$8022 into `$EB/$ED` (walk =
$01.4C px/frame) [seen] [code].

## Inventory, progress and stage state ($0640-$06AF)

| Addr | Meaning | Tag |
|---|---|---|
| $063D | stage id AND 7 | [code] $DBE1 |
| $0642 | boss bar mode: 0 none, $FF intro (bar filling), 1 fight | [seen] boss room |
| $0649 / $064A | level object list window: first / last entry in range. Advances along the level path, also through vertical sections (the best progress measure for an autoplayer) | [seen] 10 -> 13 on Flame's climb; [code] $3A:$8140 |
| $064E / $064F | current base CHR set / extra CHR set | [code] $DC19, $D552 |
| $0672 | IRQ scanline latch | [code] PLAN.md |
| $067D-$067F | demo (attract-mode) input playback | [code] $C739 |
| $0680 | last screen whose objects were spawned | [code] $3A:$822F |
| $0682 | ? cleared on stage start | [code] |
| **$0684** | **checkpoint screen** (respawn screen; 0 = stage start) | [seen] warps |
| **$0685 / $0686** | **checkpoint CHR set / palette** (copied to `$064F` / `$069E` on respawn) | [seen] [code] $8416 |
| **$0688-$0691** | **weapon energy, slot 0-9** = R.BUSTER, Y.SPEAR, W.STORM, B.ATTACK, F.BLAST, PLANT.B, KNIGHT.C, SILVER.T, C.FLASH, BEAT. `$80` = not owned, else 0..$1B | [seen] menu order and bars; [code] $3B:$BA3F gives energy from the flags |
| **$0692-$0695** | **progress bytes** (the password payload), 3 bits each, see the stage table | [seen] Blizzard kill sets `$0692` = 1; passwords |
| **$0696** | **Energy Balancer** owned | [seen] password variant sets it; menu icon |
| $0697 | target screen of the current screen transition (`$57` and `$046F` are set from it when it ends) | [seen] 5 -> 6 on a vertical transition; [code] $D564, $39:$82A8 |
| **$0699** | **current weapon** (0-9, menu cursor); HUD weapon bar reads `$0688+$0699` | [seen] menu; [code] $CF77 |
| $069E | current palette id | [code] |
| $06A0 | "boss already beaten" (stage revisit) -> palettes come from bank $28 instead of $37 | [code] $CDF4, $C9F7 |
| **$06A1** | **E-tanks** (menu shows the value) | [seen] poke -> menu |
| $06A2-$06A4 | per-stage temps cleared on stage start | [code] $CE32 |
| $06AB | $5A on stage start (timer) | [code] |

Adaptors are not stored separately: **Rush Jet = `$0695` bit 0 (Plant Man beaten), Rush Power =
`$0694` bit 0 (Flame Man beaten)**. [seen] poking only one of them makes only JET or only POW appear on
the pause menu's top row. Each time the menu opens it rebuilds `$0625` (Jet) / `$0626` (Power): $FF =
not owned, 0 = owned [code] $38:$931D. **Beat** = all four progress bytes have bit 2: [seen] bit 2 in
each byte lights the B, E, A, T boxes; `$0691` = $1B makes BEAT selectable; at stage start $3B:$BA63
gives `$0691` = $1B only when all four plates are in [code]. **Energy Balancer** = `$0696` [seen] menu
icon. E-tanks `$06A1` and lives `$A9` are displayed as-is ([seen] 7 -> "07", 5 -> "05").

Pause menu state [seen]: while it is open the scheduler threads 1 and 2 are suspended (`$22` = `$23` =
$80, 0 in play), `$FB` (mirroring) = 0, `$0688` (buster) is refreshed to $1B, `$0699` = highlighted
weapon, `$06A3` = menu section; the menu runs in $38:$92B4-$95FF (`LDA $42 / BEQ` loop at $9397).

Stage rules found on the way [seen]:
- **No Robot Master rematch.** If a stage's boss is already marked beaten when Rockman walks into its
  boss room, he beams out at once and the post-stage password screen follows (no fight, no weapon).
  Clearing the flag before reaching the room brings the boss back (Flame Man: bar $FF, then HP $1B).
- **The boss shutter is a checkpoint.** Entering the boss room sets `$0684` = boss screen - 1 with the
  current CHR/palette (Flame: `$0684` 0E -> 16) [code] $3F:$FA20, so a death in the fight restarts in
  the corridor.
- `$06A0` = "stage already cleared" is latched at stage start ($3E:$CDF4) and only selects the
  revisit palette bank ($28 instead of $37).

## Stage flow

The game loop ($3E:$CD3B-$CDBA) starts a stage three ways: `$CD3B` new stage with its intro (fortress
map, boss intro), `$CD43` new stage without the intro (`$CE52` resets checkpoint and boss state),
`$CD46` respawn at the checkpoint (`$CDBD` loads stage `$51` at screen `$0684` with CHR `$0685` and
palette `$0686`). The stage then runs until `$F0` != 0 ($CD5D): 1 = cleared (Robot Master stage:
weapon get + stage select; fortress: `INC $51` and the next stage), 2 = respawn, 3 = game over
(password screen with STAGE SELECT / CONTINUE, `$A9` reset to 2). [seen] all four outcomes by poking
`$F0`; see `cheats.md`.

## Password RAM

- `$0300-$0323`: the 6x6 grid, cell = row*6 + col (A1 = $0300 ... F6 = $0323); non-zero = orb
  (the entry screen writes $90 + a counter). [seen] pressing A writes $95, $94, $93 ...; poking $90 works.
- Cursor: `$05B1` = column (0-5), `$05C8` = row [code] $F3AF / $F3BB.
- Decoder $3F:$F3D0 writes `$0692-$0696`; `$0696` = the Energy Balancer bit of the key variant [seen].
- Display after game over: $3F:$F477 picks one of two variants with `$F3` bit 1, so the same progress
  can show two different passwords [code].
- An invalid grid (not exactly one key cell and one orb per byte) shows **"PASS WORD ERROR"** [text]
  and leaves `$0692-$0695` = $FF [seen] (`img/scout_password_edge.png`). The empty password (nothing
  beaten) A1 B1 B4 C4 E6 is valid [seen].

## Free RAM

Method [seen]: a 118,526-frame scripted run (power-on boot, intro, title idle, password entry with a
bad and the all-clear password, stage select browsing, Mr. X Fortress 1, all eight stages from a new
game without cheats including deaths and a game over, all 16 stages with every weapon/adaptor and
menu use, E-tank use, the game-over CONTINUE / STAGE SELECT choices, a Blizzard Man kill with the
weapon get) logged every byte every frame. 413 bytes never changed after boot; most of those are
in use (written with the same value, or rare paths). Candidates were then filled with a canary ($5A)
after every state load and re-poked whenever the game changed them, and a behaviour trace (stage,
camera screen, player X/Y, HP, `$F0`, every 16 frames = 7,407 samples) was compared with the clean
run. Static references come from the linear disassemblies (`run2/ramrefs.py`).

| Range | Bytes | Result |
|---|---|---|
| **$06AF-$06FF** | 81 | never written, canary survives, trace identical, no code references (the few operand hits are inside music/graphics data) |
| **$07FA-$07FF** | 6 | same (just above the PPU-update queue `$07F0-$07F9`) |
| **$0698**, **$064C** | 1 + 1 | same, no references at all |
| $01A0-$01E4 | 69 | never written: headroom of the main stack (deepest use seen $01E5). Free in practice; a deeper call chain would reach it. **(critic)** also never written in the late-game run below; but a stack overflow lands here first (see the zero-page note), so treat it as a safety margin, not storage |
| $0100-$010D, $0160-$0167, $0180-$0184 | 27 | never written: bottoms of the scheduler threads' stacks ($C5C3: tops $013F/$015F/$017F/$019F). Same caveat |

No free zero page: the seven zero-page bytes that were never written in the run ($2D, $3B, $AF,
$DD, $DE, $EA, $F5) all have code references (thread table, rare paths). Everything inside the
object table, the palette buffers ($0360-$039F), the per-screen flags ($0340-$035F) and the sound
work area ($0700-$07EF) counts as used even where a byte never changed.

**Late-game confirmation (added by critic)** [seen] (`build/research/rm6/rm6-critic/freeram_late.py`,
results in `freeram_late.txt`): the paths this run did not cover were played for 114,196 frames with two
canaries ($5A, then $A5) in every candidate above: the Mr. X reveal into Wily 1, the Wily 3 hub and two
refights killed, the rush exit into Wily 4, the Wily Machine phase 1 and 2 and the Wily Capsule killed, the
whole ending (24,000 frames), boot after the START reset, a fortress game over with CONTINUE, and 8,000 frames
of the title attract demo. **No candidate was written** (`$01A0-$01E4`, `$064C`, `$0698`, `$06AF-$06FF`,
`$07FA-$07FF`), and the seven zero-page bytes, only observed, never changed either. Caution: a first attempt
that also poked the canary into those zero-page bytes made the Wily Capsule's death overflow the stack (a
repeating 8-byte frame with P = $B4, i.e. a BRK storm, written down through $01A0). They are live state
(thread table and rare paths), so never borrow them.

## SELECT button

Vanilla never uses SELECT in normal play. [code] A scan of all 512 KB for every read of `$40-$45`
followed by a mask with bit 5, and for `BIT/AND/LDA $FF5A` (the bit-mask table at $3F:$FF58 is
`80 40 20 10 08 04 02 01`), finds exactly one SELECT test: $28:$813C `LDA $42 / AND #$20 / BEQ / JMP
$FF70` (SELECT = soft reset) inside the hidden **SOUND PLAYER** debug screen (SEQ / COL / TBL / TMR, ASCII
font; documented by rm6-text). No code maps bank $28 as code (the only `LDA #$28 / JSR $CB91` is the
revisit-palette loader at $C9FC), so it is unreachable. [seen] Holding/tapping SELECT for 240 frames in
eight states (title, stage select, stage, boss fight, after the boss, all items, pause, password) leaves
RAM identical except: pause menu = the generic "any key but B" cursor blip (sound $32, $38:$9397), and
the password screen's cursor blink. **SELECT is free for Rockman 6 GP.**

## Images

- `img/scout_pause_flags.png`: pause menu with single flags poked: none, `$0695`=1 (JET), `$0694`=1
  (POW), `$0696`=1 (Energy Balancer icon), E-tanks 7 / lives 5, `$0691`=$1B (BEAT listed), bit 2 in all
  four bytes (B-E-A-T lit).
- `img/scout_no_rematch.png`: walking into a beaten boss's room: Rockman beams out, the password
  screen follows.
- `img/scout_password_edge.png`: the empty password and Blizzard-only password accepted; 4 and 6 orbs
  give PASS WORD ERROR.
- `img/scout_gameover.png`: death with `$A9` = 0: GAME OVER over the password, then STAGE SELECT /
  CONTINUE.
- `img/scout_soundplayer_forced.png`: the bank-$28 sound player forced to run from an object slot
  (draws its "O E" strip over the stage; rm6-text has the full screen).

## Lessons for Rockman 6 GP

- **Free RAM is scarce but real**: `$06AF-$06FF` (81 bytes) plus `$07FA-$07FF`, `$0698`, `$064C` are
  never written and not read. That is the place for new GP state (new weapons' energy, extra
  progress bits, a SELECT-menu cursor, the "spun" counters of a new mechanic). If more is needed,
  the main-stack headroom `$01A0-$01E4` is untouched in practice, but anything new that recurses or
  nests interrupts eats into it. There is no free zero page; borrow scratch `$00-$0F` inside a routine.
- **SELECT is unused**, so GP can give it a job (quick weapon cycle, adaptor toggle, a GP-specific
  menu) without breaking any vanilla behaviour. The only handler is in the dead sound player.
- **Progress is four 3-bit bytes**, and the password format has no spare capacity (key cell +
  exactly one orb per byte). New progress (extra stages, items) cannot ride in vanilla passwords;
  GP needs either a new password scheme or save RAM. Vanilla has none: TGROM, header without the
  battery bit, no `$A001` (PRG-RAM enable) write in the fixed banks and no real `$6000-$7FFF` access
  [code]; GP would have to declare and enable it.
- **Adaptors and Beat are derived from boss flags**, not stored. To award Rush Jet/Power or Beat
  differently in GP, patch $38:$931D (menu) and $3B:$BA3F (stage start), not a separate inventory.
- **No rematches**: a beaten boss's room ends the stage. A GP refight/boss-rush feature needs that
  check changed, not just a new room.
- **The object table is 23 slots x 29 arrays with cooperative AI threads** (resume pointer + bank per
  slot). New enemies slot in by adding type entries to the $3A tables ($82C9/$83C9/$84C9/$85C9) with
  code in a free bank; each AI yields with `JSR $E46C`.
- ~~**Vertical sections do not change `$57`**~~ **(corrected by critic)**: `$57` *does* hold the
  current screen index after every transition, vertical ones included (`levels.md` section 3: vertical
  sections are simply more screen indices). It switches on the first frame of the transition, while
  `$0697` switches when the scroll ends. The vanilla checkpoint routine (`CMP $57`, `$39:$8416`) relies on
  it. GP code that keys on "the current screen" can use `$57`; use `$0697` if it must wait for the end of
  the scroll. Within one screen, ladders move only the player (`$04CB`), not `$57`.
