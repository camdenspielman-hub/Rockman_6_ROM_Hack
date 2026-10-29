# Rockman 6 GP: technical architecture v2 (design-tech)

This doc replaces `docs/PLAN.md` §5-7 (and rewrites milestones M0-M3 of PLAN §8). Every claim here comes from the research in
`docs/research/` or was measured for this doc; where the two disagree with PLAN, the research wins and the BRIEF wins on
decisions (BRIEF §7). Tags: **[engine-ok]** vanilla does it with data only, **[new-code]**, **[new-art]**, **[new-music]**;
sizes **S / M / L**; tiers **Must / Should / Could**. Evidence tags as in the research: **[code]**, **[seen]**, **[guess]**.

Addresses are `bank:CPU` in **vanilla numbering** unless marked *new*. After the MMC5 move, vanilla fixed banks `$3E/$3F`
become `$7E/$7F` (§1.2); a vanilla address `$3E:$C8C1` is then `$7E:$C8C1`, same CPU address.

Scratch and probes for this doc: `build/design/design-tech/` (`probe/` = MMC5 hardware probes run on the bundled FCEUmm
core, `sprtiles.py` = sprite-tile census, `irq_dis.txt` = the 27 IRQ handlers, `sites51.txt` = the 45 stage-id readers in
context).

Contents:
0. Decisions at a glance -
1. Cartridge and the MMC5 migration -
2. PRG-RAM -
3. Memory map (CPU RAM, ExRAM, PRG-RAM pages) -
4. Stage ids to 32 and the stage-attribute table -
5. WRAM-resident layouts (the 4MI model): decision -
6. Level pipeline -
7. Object / AI framework -
8. The generic raster list -
9. Autoscroll (T1) -
10. Per-position destructible tiles (T6) -
11. Text and dialogue engine (T2) -
12. Sound -
13. Saves -
14. Dev tooling and tests -
15. Lag plan -
16. Milestones M0-M3, rewritten -
Lessons applied - Risks - Open questions - Cross-doc dependencies.

---

## 0. Decisions at a glance

| # | Decision | Why (evidence) | Tag |
|---|---|---|---|
| D1 | **MMC5, 1 MB PRG by insertion**: vanilla banks `$00-$3D` stay in place, new banks `$3E-$7D`, vanilla fixed `$3E/$3F` move to `$7E/$7F` | BRIEF §7.1; CX and 4MI both expanded by insertion; every `LDY #bank / JSR $CBC0` with bank < `$3E` stays valid (`rm6/engine.md` §9) | [new-code] M Must |
| D2 | **PRG mode 3** (four 8 KB windows) with `$C000` = `$7E` and `$E000` = `$7F`, exactly MMC3 mode 0's shape | the helpers `$CB91/$CBC0/$CBDA/$CBE9` keep their contract | [new-code] S Must |
| D3 | **Bank id convention**: a bank byte `$00-$7F` is a ROM bank, `$80-$87` is PRG-RAM page 0-7. The ported helpers do `EOR #$80 / STA $5114` (ROM `n` → `$80|n`; RAM `$80+p` → `p`) | lets every vanilla table that holds a bank number (`$6E`, `$6F`, `$0441`, the stage table) point at RAM with no code change; MMC5 RAM in `$8000-$DFFF` works [seen: `probe/`] | [new-code] S Must |
| D4 | **The "C-window"**: GP service code runs in the `$C000` window (switched by a `$7F` stub), so a hook never disturbs the `$8000/$A000` banks of the vanilla code that called it. NMI and IRQ vectors move to `$7F` stubs that force `$7E` back into `$C000` | MMC5 can switch `$C000` (MMC3 could not); vanilla code banks `$38`, `$3E` have 0 bytes of fill and `$39`/`$3B` have under 100 (§1.9) | [new-code] M Must |
| D5 | **32 KB battery PRG-RAM** (EWROM shape), 4 pages: 0 SAVE, 1 WORK (always at `$6000`), 2 LAYOUT, 3 TILES | §2 | [new-code] S Must |
| D6 | **8 KB CHR-RAM, no CHR banking beyond 8 KB, no ExGrafix in scrolling stages** | the bundled FCEUmm wraps MMC5 CHR-RAM at 8 KB whatever the header says [seen: `probe/chr_*.nes`]; ExRAM extended attributes are shared by both nametables, which breaks a scrolling stage | constraint |
| D7 | **ExRAM in mode 0** = a spare nametable for text windows and panels, switched in mid-frame with `$5105` | works on FCEUmm: ExRAM shown from exactly the IRQ line [seen: `probe/exnt2.nes`]; §3.3, §11 | [new-code] S Must |
| D8 | **Stage ids 0-31** with a 32-byte **stage-attribute record** per id, copied to WORK RAM at stage init; all 45 `$51` readers rewritten (§4) | BRIEF §7.2 | [new-code] M Must |
| D9 | **WRAM-resident layouts, adopted in the "RAM image" form**: the stage's layout and tileset are copied raw into RAM pages laid out exactly like the ROM banks; vanilla painters and collision read them unchanged through D3 (§5) | gives map edits, T6, HARD poke lists and up to 4 sections × 32 screens per stage for one copy at stage start | [new-code] M Must (sections Should) |
| D10 | **IRQ: literal port first, raster list second.** M1 ports the 27 chains one-for-one (relative latch → absolute line). M2 replaces them with a **generic double-buffered raster list** and moves the 4 logic-in-IRQ handlers out of the interrupt | BRIEF §7.1, 4MI lesson 11; a literal port is the only change that golden movies can prove | [new-code] M + M Must |
| D11 | **Text: a new canvas-based window engine** (1bpp fonts rendered into borrowed CHR tiles, VWF for EN, kana + a small kanji set for JP) for dialogue and pop-ups; the vanilla PPU-script engine stays for full-screen text with a language hook | vanilla has no control codes (`rm6/text.md` §4.2); the sprite table is 96 % used in play [seen: `sprtiles.py`] | [new-code] L Must |
| D12 | **Sound: vanilla driver kept**, plus a per-track bank table, a new-song pipeline (MML → the decoded `$00-$18` command set, proven by a byte-exact round trip of all 36 vanilla songs), hardware multiply, and an optional second driver instance on the MMC5 pulses | `rm6/engine.md` §5, 4MI §9 | [new-code] M Must; MMC5 pulses Could |
| D13 | **Dev tooling from day one**: a hook registry with original-byte checks, BPS output, EXTRA CONFIG in DEV builds, the vanilla warp, a test mailbox, golden movies traced with shadow6 (ported to MMC5) | BRIEF §7.3, CX lesson 9, 4MI lesson 10 | [new-code] M Must |
| D14 | **Assembler: Ophis 2.3** from `.pylib` | it assembled this doc's MMC5 probe ROMs [seen] | tool |

---

## 1. Cartridge and the MMC5 migration

### 1.1 NES 2.0 header [new-code] S · Must

Vanilla: `4E 45 53 1A 20 00 40 08 00 00 00 07 00 00 00 01` (mapper 4, 512 KB, no battery, CHR-RAM 8 KB) [code].

| Byte | Value | Meaning |
|---|---|---|
| 0-3 | `4E 45 53 1A` | "NES" EOF |
| 4 | `$40` | PRG-ROM 64 × 16 KB = **1 MB** |
| 5 | `$00` | no CHR-ROM |
| 6 | `$52` | mapper low nibble **5**; bit 1 **battery**; mirroring bit ignored by MMC5 |
| 7 | `$08` | NES 2.0 identifier; mapper high nibble 0 |
| 8 | `$00` | mapper bits 8-11, submapper 0 |
| 9 | `$00` | ROM size MSBs |
| 10 | `$90` | **PRG-NVRAM 64 << 9 = 32 KB**; volatile PRG-RAM 0 |
| 11 | `$07` | **CHR-RAM 64 << 7 = 8 KB**; no CHR-NVRAM |
| 12 | `$00` | NTSC (RP2C02), as vanilla |
| 13 | `$00` | |
| 14 | `$00` | no misc ROMs |
| 15 | `$01` | standard controllers, as vanilla |

4MI's header declared PRG-RAM size 0 (`r4mi/engine.md` §1.1, lesson 12); GP declares the real size. **The test emulator
cannot catch a header mistake**: the bundled FCEUmm gave 8 distinct PRG-RAM pages (64 KB) for every byte-10 value tried
(`$90`, `$A0`, `$70`, `$09`, `$00`) [seen: `probe/probe_*.nes`]. Mesen sizes PRG-RAM from the NES 2.0 header (to be confirmed in M1.6), so the header is
checked on Mesen at every user gate (§14.6), and the boot code probes the RAM size itself (§2.3).

### 1.2 The insertion layout [new-code] M · Must

| File offset | Banks (new) | Contents |
|---|---|---|
| `0x000000-0x00000F` | | header (§1.1) |
| `0x000010-0x07C00F` | `$00-$3D` | vanilla banks, **in place**, patched only through the hook registry (§14.2) |
| `0x07C010-0x0FC00F` | `$3E-$7D` | **512 KB new space** |
| `0x0FC010-0x0FE00F` | `$7E` | vanilla `$3E` (CPU `$C000`), patched |
| `0x0FE010-0x10000F` | `$7F` | vanilla `$3F` (CPU `$E000`), patched; reset vector here (MMC5 powers on with `$5117` = last bank [seen: the probe ROMs booted from bank `$7F`]) |

The vanilla free banks `$0B-$0F` (40 KB, never executed or read in 139,200 traced frames, `rm6/engine.md` §6) are a second
pool. Bank roles in the new space (proposal; the allocator in §14.2 places data, these are the code homes):

| New banks | Role | Window |
|---|---|---|
| `$3E-$3F` | GP core services: stage loader, RAM image builder, save/load, FAR and C-window targets, poke lists | C-window (`$C000`) |
| `$40-$41` | systems.md: scorecard, chips, shop, form swap, weapon alts | C-window / `$8000` |
| `$42-$43` | meta.md: title, file select, bracket, results, config, post-game menus | `$8000/$A000` |
| `$44-$45` | text engine, glyph blitter, window manager | C-window |
| `$46-$49` | text data: JP, EN, ENGRISH strings and fonts | `$A000` (read by `$44-$45`) |
| `$4A-$51` | new object AIs (4 pairs), assembled for `$8000/$A000` like vanilla AIs | `$8000/$A000` |
| `$52-$59` | new sprite bank pairs (metasprite tables, vanilla format, §7.5) | `$8000/$A000` |
| `$5A-$63` | new CHR source data (80 KB = 5,120 tiles) | read by the CHR loader |
| `$64-$6B` | tileset slots (2 per bank, each with its own alternate set, §5.2) | copied to RAM |
| `$6C-$6F` | layouts (4 × 2 KB sections per bank), object lists, screen scripts, poke lists | copied to RAM |
| `$70-$77` | music and SFX (per-track bank byte, §12) | `$A000` (driver reader) |
| `$78-$7B` | big-boss BG art packs, portraits | read by the CHR loader |
| `$7C` | DEV: EXTRA CONFIG, test hooks (present in every build, entered only in DEV builds) | C-window |
| `$7D` | reserve | |
| `$0B-$0F` | overflow pool (music or CHR), filled last | |

### 1.3 RESET and MMC5 init [new-code] S · Must

Vanilla RESET (`$3F:$FF70-$FFDC`): SEI/CLD, PPU off, APU off, two vblank waits, `TXS`, **`STA $E000` at `$FF96`** (MMC3
IRQ off), clears CHR via `$2006/$2007`, clears `$0000-$07FF`, `$FB` = 1, **`STA $A000` at `$FFC9`**, writes CHR R5-R0 from
`$FF50` (`$FFCC-$FFD8`), `JMP $C51E` [code].

GP RESET (in `$7F`):

1. Keep `$FF70-$FF94`. `$FF96 STA $E000` becomes `STA $5204` (A comes from `LDA $2002` with bit 7 clear, so this disables
   the MMC5 IRQ).
2. Replace `$FFC9-$FFD9` with `JSR mmc5_init` + `JMP $C51E`. **`$C51E` lives in the `$C000` window, so `$5116` must be
   written before that jump.**
3. `mmc5_init` (in `$7F` free space, ~80 bytes):

| Register | Value | Meaning |
|---|---|---|
| `$5100` | `$03` | PRG mode 3: four 8 KB windows |
| `$5101` | `$00` | CHR mode 0 (one 8 KB page), as 4MI. Not the 1 KB mode: with 8×8 sprites MMC5 uses whichever register set (`$5120-$5127` or `$5128-$512B`) was written last for *all* fetches, so a stray B-set write would remap the sprite half. (1 KB banking inside the 8 KB works on FCEUmm [seen: `probe/chr_*.nes`], but nothing needs it) |
| `$5102` / `$5103` | `$02` / `$01` | PRG-RAM writes enabled (stays enabled: MMC5's gate is global, §2.2) |
| `$5104` | `$00` | ExRAM as an extra nametable (D7). It is written to only during rendering (§3.3) |
| `$5105` | `$50` | horizontal mirroring (vanilla `$FB` = 1 at boot; MMC3 `$A000` = 1 is horizontal) |
| `$5106` / `$5107` | `$00` / `$00` | fill tile / attribute (fill mode only used by the window border, §11.3) |
| `$5113` | `$01` | **WORK page at `$6000`** (§2.2) |
| `$5114` / `$5115` | `$80|$3C` / `$80|$3D` | any valid ROM pair (MMC5 does not define them at power-on, so they are set before the first vanilla code runs); shadows `$4A`/`$4B` = `$3C`/`$3D` |
| `$5116` | `$FE` | `$7E` at `$C000` |
| `$5117` | `$FF` | `$7F` at `$E000` (power-on value; written anyway) |
| `$5120-$512B` | `$00` | in 8 KB mode only `$5127` and `$512B` matter: page 0 = the identity (vanilla's `$FF50` = `00 02 04 05 06 07` is MMC3's identity). Nothing writes them again |
| `$5130` | `$00` | |
| `$5200` | `$00` | vertical split off |
| `$5204` | `$00` | IRQ off |
| `$5015` | `$00` | MMC5 pulses off until the sound config turns them on (§12.5) |

4. Then `ram_probe` (§2.3), clear WORK page 1 (not the SAVE page), copy WRAM-resident code (§15.3), read the test mailbox
   (§14.5), `JMP $C51E`.

**Gotcha found for this doc** [code]: vanilla's main init `$3E:$C51E` checks that `$FFE0-$FFEF` are all `$FF` and that
`$FFF8 = $08`; otherwise it turns the screen off and loops forever at `$C53B`. Bank `$7F` must keep those 17 bytes, and the
free-space allocator must never place anything at `$7F:$FFE0-$FFEF`.

### 1.4 Bank switching [new-code] S · Must

MMC5 has one register per window, so MMC3's select register and its shadow `$4C` become dead; `$4A` (bank at `$8000`) and
`$4B` (bank at `$A000`) stay, because the scheduler (`$3E:$C604/$C609`), the sound service and the far calls read them [code,
coverage]. **No call site changes**: the helpers are rewritten in place.

| Helper | Vanilla (MMC3) | MMC5 replacement (same entry, same register contract) |
|---|---|---|
| `$CBAF` (tail of `$CB91`: `$17` → `$8000`) | `LDA #6 / STA $4C / STA $8000 / LDA $17 / STA $4A / STA $8001 / LDX $18 / RTS` | `LDA $17 / STA $4A / EOR #$80 / STA $5114 / LDX $18 / RTS` |
| `$CBC0` (Y → `$8000`, Y+1 → `$A000`) | 11 instructions, leaves Y = bank+1, A = 7 | `STY $4A / TYA / EOR #$80 / STA $5114 / INY / STY $4B / TYA / EOR #$80 / STA $5115 / RTS` (Y = bank+1 kept) |
| `$CBDA` (A → `$A000`, A preserved) | `PHA / STA $4B / LDA #7 / STA $4C / STA $8000 / PLA / STA $8001 / RTS` | `STA $4B / EOR #$80 / STA $5115 / EOR #$80 / RTS` |
| `$CBE9` (restore both from the stacked shadows) | writes `$8000/$8001` twice (`$CBF2-$CC09`) | same stack logic, `EOR #$80 / STA $5114` and `.../ STA $5115` |
| `$C8C1` sound service | maps `$34`/`$35` (`$C8C3-$C8D2`), restores from `$4A/$4B` and `$4C` (`$C8ED-$C901`) | `LDA #$B4 / STA $5114 / LDA #$B5 / STA $5115` ... restore from `$4A/$4B` with `EOR #$80`; the `$4C` restore is dropped |
| `$C7AD-$C7B4` NMI CHR-copy source | `LDA #6 / STA $8000 / LDA $8A / STA $8001` (no shadow) | `LDA $8A / ORA #$80 / STA $5114` (no shadow: the main thread is idle on these frames, and the sound service restores `$8000` afterwards, as in vanilla) |
| `$34:$804C-$8062` sound reader | maps `$36` at `$A000` for one byte, then `$35` | `LDA #$B6 / STA $5115` ... `LDA #$B5 / STA $5115`; then extended for the bank table (§12.2) |

Savings: `$CBC0` goes from ~36 to ~26 cycles; the stack-juggling `$CB91/$CBE9` stay (their cost is the stack work). The MMC3
hazard of an NMI landing between `STA $8000` and `STA $8001` disappears.

### 1.5 Mirroring [new-code] S · Must

Four real `$A000` writes [code, critic]: NMI `$3E:$C021` (`LDA $FB / STA $A000` at `$C01F`), pause menu `$38:$9295` and
`$38:$95BA`, RESET `$3F:$FFC9`.

- `$FB` stays the game's mirroring variable (0 vertical, 1 horizontal, MMC3 meaning). The NMI site becomes `JSR nmi_mirror`
  (3 bytes over the 5-byte `LDA/STA`, 2 NOPs): `LDY $FB / LDA mirtab,Y / STA $5105`, `mirtab = $44, $50`.
- The two menu sites become `JSR set_mirror` with A = 0/1.
- The NMI rewrites `$5105` every frame, which is what lets a window band switch it mid-frame (§11.3) without cleanup.

### 1.6 Fixed-bank numbers used as data [new-code] S · Must

`LDA #$3E / JSR $CB91` at `$3F:$E204` (OAM builder) and `$3F:$E430` (object loop) map "bank `$3E`" into `$8000` as a
placeholder [code, critic]. After the move, `$3E` is new space; the operand becomes `$7E` (2 bytes). No other immediate
`$3E/$3F` reaches a helper and no bank table holds them (`rm6/engine.md` §9).

### 1.7 IRQ: the literal port of all 27 chains [new-code] M · Must

**Mechanism** (vanilla, `rm6/engine.md` §4, re-read for this doc): the NMI copies `$0677` → `$0676` (handler index), writes
the latch `$0672` to `$C000` and `$C001`, then `STA $E000,Y` with Y = `$F4` (0 off, 1 on). This happens in **two NMI paths**:
the normal path `$C066-$C077` and the lag-frame path `$C0C4-$C0D5`. The IRQ entry `$C14C` acknowledges with
`STA $E000 / STA $E001` (`$C151/$C154`), calls `JMP ($C116 + 2*$0676)` through `$C104`, then `INC $0676` and RTI (`$C162`).
A handler that writes `$C000` sets the next relative latch; one that writes `$E000` ends the chain; `DEC $0676` repeats a
handler.

**Conversion rule.** MMC3 fires the next IRQ `latch + 1` scanlines after the previous one; MMC5 fires at an absolute line
`$5203`. A new hot byte `IRQ_LINE` (§3.1) tracks the current absolute line.

| Vanilla write | Replacement (3 bytes, same size) |
|---|---|
| NMI `LDA $0672 / STA $C000 / STA $C001` + `LDY $F4 / STA $E000,Y` (both paths) | `JSR nmi_irq_arm`: `IRQ_LINE = $0672 + K`; `$5203 = IRQ_LINE`; `$5204 = $80` if `$F4` else `$00` |
| handler `STA $C000` (A = L) | `JSR irq_next`: `SEC / ADC IRQ_LINE / STA IRQ_LINE / STA $5203 / RTS` (next = current + L + 1). **Moved to the end of each handler**, after its PPU writes, so the extra cycles never shift a split |
| handler `STA $E000` | `JSR irq_off`: `PHA / LDA #0 / STA $5204 / PLA / RTS` |
| entry `STA $E000 / STA $E001` (`$C151/$C154`) | `LDA $5204` (reading acknowledges) + 3 NOPs (A was pushed at `$C14C`) |

The fixed banks are rebuilt from the reassemblable source of M0.4, so the handlers are edited in that source (sizes may
change; the registry records each edit for review) rather than byte-patched in place.

`K` is a calibration constant (expected 0 or 1; 4MI's MMC5 build feeds the same variable to `$5203` that its MMC3 build
feeds to `$C000`, `r4mi/engine.md` §2.1). MMC3 asserts its IRQ near dot 260 of the line before the split and MMC5 near the
start of its target line, so each handler's `$C163` delay count (X) is re-tuned once, by comparing the vanilla and ported
frame of every split state pixel for pixel (§14.4). MMC5 counts lines only while rendering is on: no vanilla handler turns
rendering fully off, so this is safe for the literal port (see §8.4 for the raster list's rule).

**The 27 handlers** (`$3E:$C116` table; addresses re-read from the disassembly, `irq_dis.txt`):

| # | Addr | Effect (PPU writes) | Next | Conversion notes | Used by |
|---|---|---|---|---|---|
| 0 | `$C167` | `$2006 = $0671:00`, BG table `$1000`, sprites off | off `$C188` | delete (dead SOUND PLAYER only) | bank `$28` |
| 1 | `$C18C` | delay X=4; `$2006 = $28E0`; `$0674 = $8D - $0673` | L = `$0673` (`$C194`) | | Blizzard ship (`$3E:$D4BF`, start `$2F`) |
| 2 | `$C1AB` | 20 NOPs; `$2006 = $20E0`; scroll `$F7`; **sound** | L = `$0674` (`$C1AE`) | keep the NOP pad; retune | chain 1 |
| 3 | `$C1DB` | delay X=3; `$2006 = $2300`; scroll `$F7` | off `$C1F7` | | chain 1 |
| 4 | `$C1FB` | X scroll = -`$F7`; PPUCTRL NT flip; **sound** | L = `$68` (`$C1FD`) | | adaptor menu slide `$38:$966D` (`$42`) |
| 5 | `$C218` | scroll `$F7`; PPUCTRL `$FC` | off `$C225` | | chain 4 |
| 6 | `$C229` | scroll `$0675`; **sound** | L = `$AE` (`$C22B`) | delete (no starter) | none |
| 7 | `$C23A` | delay X=3; `$2006 = $2300`, scroll 0 (**fixed floor strip**) | off `$C254` | | `$39:$855D`, `$39:$941F`, `$39:$97DF` (start `$C1`): Plant 0E, Mr. X 2/3, Wily 2 |
| 8 | `$C258` | 9 NOPs; copies `$0624→$0678`, `$05CA→$05C9`, `$05E1→$05E0` | L = `$05B4` (`$C264`) | | opening story `$3E:$D135` (`$01`) |
| 9 | `$C27A` | **every 2nd line**: `$2006 = $05C9:$05E0`, scroll 0; `DEC $0678`; `DEC $0676` (repeat) | L = 1 (`$C285`); off at `$C2A1` when `$0678` = 0 | per-line; the repeat stays | opening story |
| A | `$C2A8` | PPUCTRL NT1, scroll `$05E0` | L = `$30` (`$C2AA`) | | opening story `$3E:$D10F` (`$82`) |
| B | `$C2BE` | PPUCTRL NT0, scroll `$05F7` | L = 1 (`$C2C0`), off (`$C2D3`) | writes both: the latch is dead | chain A |
| C | `$C2D7` | X scroll = camera / 2 (`$06A8:$06A7` >> 1): **parallax** | L = `$30` (`$C2D9`) | | Tomahawk 00-02 `$39:$86C4` (`$2E`) |
| D | `$C2F0` | X scroll = camera; **sound** | off `$C2F9` | | chains C, E (#`$10` = D) |
| E | `$C2FF` | scroll 0; `$0678` = 20; `$0679` = (`$F3` & 4) >> 2 | L = 1 (`$C301`) | | Tomahawk sunset `$39:$85E1` (`$1F`) |
| F | `$C31B` | X scroll `$0679` (0/1 alternating): **heat shimmer**, repeats 20 times | L = 2 (`$C31D`) | per-line | chain E |
| 10 | `$C2F0` | = D | | | chain E |
| **11** | `$C337` | `$2006 = $2800`; **logic**: moves the spike ceiling `$069C` by `$05C7/$05DE`, plays `$55/$56/$57`, special case `$57` = 6, sets **next frame's** `$0672 = $B0 - $069C` | L = `$069C + 8` (`$C33D`) | **logic in IRQ** (§1.8) | Knight 03-06 `$39:$884E` (`$B0`) |
| 12, 13 | `$C3B8` | delay X=3; `$2006 = $22E0`; scroll `$F7` | off `$C3D4` | | chains 11, 16 |
| **14** | `$C3D8` | `$2006 = $2800`; **logic** every 2nd frame (`$F3` odd): tide `$069C += $05DE` bouncing in `$03-$40`, `$0672 = $70 - $069C`, **every type-`$72` object's Y (`$04CB,X`) = `$0672 - 6`**, `$03BD` bit 7 | L = `$069C + 8` (`$C3DE`) | **logic in IRQ** | Centaur 0A-0B `$39:$8A7A` (`$6D`) |
| 15 | `$C453` | delay X=3; `$2006 = $21E0`; scroll `$F7`; **sound** | off `$C46F` | | chain 14 |
| 16 | `$C475` | delay X=2; `$2006 = $2000`; `$0676 = $12` (jumps to 13) | L = `$0B` (`$C477`) | | Mr. X 4 machine room, Mr. X reveal `$39:$98FC` (`$AE`) |
| 17 | `$C48F` | X scroll `$0678`; **sound** | L = `$6E` (`$C491`) | | weapon get `$3B:$9D60` (`$40`) |
| 18 | `$C4A3` | scroll 0 | off `$C4AE` | | chain 17 |
| **19** | `$C4B2` | delay X=3; `$2006 = $2300`; scroll `$0678`; **logic** every 2nd frame: `$0678 += $0679` (floor drift); if `$05B1` = 0, `$069B = -$0679` | off `$C4EE` | **logic in IRQ** | Wily Machine `$39:$9B20` (`$C1`) |
| **1A** | `$C4F2` | delay X=3; `$2006 = $2300`; scroll `$0678`; **logic**: while slot 8 lives (`$03A8`) and every 4th frame, jumps into 19's drift code (`$C4D4`) | off `$C51A` | **logic in IRQ** (a fourth one; the summaries list three) | Mr. X 3 tank `$39:$9651` (`$C1`) |

Register-write sites to convert: **15 latch writes** (`$C194 $C1AE $C1FD $C22B $C264 $C285 $C2AA $C2C0 $C2D9 $C301 $C31D
$C33D $C3DE $C477 $C491`), **12 disable writes** (`$C188 $C1F7 $C225 $C254 $C2A1 $C2D3 $C2F9 $C3D4 $C46F $C4AE $C4EE
$C51A`), the entry pair `$C151/$C154`, the two NMI arm paths and RESET `$FF96`. (`$C51A` is the last write of handler 1A,
not an init; the critic's list called it "init".) Index `$1B` would read `$8A48` past the table: the port adds a bounds check.

**Sound inside the IRQ.** Vanilla moves the sound update into the chain (`JSR $C8C1` via `$C1D7`, handlers 2, 4, 6, D/10,
15, 17) whenever the split is on and `$0672 < $70`, so the long sound update cannot delay an early split (`$C0A9-$C0B4`)
[code]. The literal port keeps this rule unchanged.

### 1.8 The logic-in-IRQ handlers [new-code] S · Must (M1 literal), S · Must (M2 move)

Four handlers change game state inside the interrupt: **11** (Knight's ceiling: position, velocity, three sounds, next
frame's latch), **14** (Centaur's tide: water line, latch, and the Y of every type-`$72` object), **19** (Wily Machine
floor drift and `$069B`), **1A** (Mr. X 3 tank: borrows 19's drift).

- **M1 (literal):** they are ported in place. Their logic does not touch mapper registers, so only the latch/disable writes
  change. Golden movies must match vanilla byte for byte here.
- **M2 (raster list):** the logic moves to `irq_logic_tick`, called from the NMI **after** the PPU work, on every frame on
  which the chain would have run (rendering on, `$F4` ≠ 0, chain id 11/14/19/1A), including lag frames (the lag-path arm
  `$C0C4` re-arms the chain in vanilla too). The cadence is unchanged: once per displayed frame, with the same `$F3`
  parity tests. What changes is the moment inside the frame: the tide no longer rewrites object Y while the main thread may
  be iterating objects, which removes a vanilla race. These two stages get "behaviour-equivalent" tests (positions within 1
  frame) instead of exact RAM equality (§14.4).
- venues_a asks for the Knight ceiling with HP and a retract flag; venues_b asks for a **dwell** at the tide's extremes
  (60 f). Both are trivial once the logic is out of the interrupt: `irq_logic_tick` reads per-stage parameters from the
  stage-attribute record (§4.4: `EFFECTS`, `EFX_PARAM`) instead of the stage-6 / stage-7 hard-wires.

### 1.9 The C-window, FAR calls and hooks [new-code] M · Must

**Why.** Every vanilla code bank is full: fill runs ≥ 32 B total 0 B in `$3E` and `$38`, 96 B in `$39` (`$BFA0`), 90 B in
`$3B`, 48 B in `$30`, 60 B in `$31`, 239 B in `$29` (`$BF11`) [measured for this doc]. The fixed bank has `$3F:$FAC0-$FF1F`
(1,120 B, `rm6/engine.md` §6) and, after M2, the ~950 B of the retired IRQ handlers (`$3E:$C163-$C51D`). Hooks therefore
detour through tiny stubs into GP banks.

**The C-window.** MMC5 lets `$C000` switch. A hook stub in `$7F` maps a GP service bank at `$C000`, calls it, and maps `$7E`
back. The vanilla caller's `$8000/$A000` banks (its own code and the object tables it is working on) stay mapped, so GP
code can read them directly.

```
CW:     ; JSR CW / .byte n        (4 bytes at the call site; n = hook index)
        save A,X,Y,P in hot RAM (§3.1); read n from the return address (+1 it)
        CWIN_CUR = CW_BANK[n] ; STA $5116            ; shadow first, register second
        JSR (CW_LO/HI[n])       ; carry and A,X,Y returned from the target
        CWIN_CUR = $FE ; STA $5116
        RTS                     ; ~55 cycles overhead
```

Rules:

1. **C-window code never yields** (`$E46C`) and never calls `$7E` routines directly: it uses `CALL7E addr` (a `$7F` stub
   that maps `$7E`, calls, and maps the GP bank back). Routines in `$7F` (`$E46C`, `$E5AF`, `$E526`, `$E9D7`, …) are
   callable directly.
2. **Vectors move to `$7F`.** NMI `$FFFA` → `nmi_stub` (`PHA / LDA #$FE / STA $5116 / PLA / JMP $C000`); the NMI's single
   exit (`$C0BA-$C0BF`, the only RTI at `$C0BF` [code, coverage]) becomes `JMP nmi_exit` (restore A/X/Y, then
   `LDA CWIN_CUR / STA $5116` before the final `PLA / RTI`). The IRQ vector gets the same stub (its RTI is `$C162`; after
   M2 the raster walker lives in `$7F`).
3. **Object AIs never run in the C-window.** New AIs live in `$8000/$A000` banks like vanilla AIs (the object loop maps
   `$0441,X` and resumes at `$0413/$042A`).
4. Hot per-frame hooks (the frozen tick in the object loop, the T6 test) are inline patches in `$7F`, not `CW` calls.

**FAR** (for GP code calling GP code in another bank pair): `JSR FAR / .byte bank / .word target` maps the pair at
`$8000/$A000`, pushes the old shadows, and restores them on return, the `$CB91` pattern. The vanilla far call `$CB28`
(4 slots `$3C/$3A/$38/$36`, all used) is left alone.

---

## 2. PRG-RAM

### 2.1 Size: 32 KB, battery [new-code] S · Must

| Option | For | Against | Verdict |
|---|---|---|---|
| 8 KB battery (EKROM) | most supported | save + work + layouts do not fit; no page isolation for the save | no |
| 8 KB battery + 8 KB volatile (ETROM) | save isolated | MMC5 selects the second chip with bank bit 2; emulator support for mixed sizes is uneven; still no room for D9 | no |
| **32 KB battery (EWROM shape)** | 4 pages: SAVE / WORK / LAYOUT / TILES; one chip; a common MMC5 configuration | the `.sav` file is 32 KB; the work pages are battery-backed (harmless: they are rebuilt at boot and stage start) | **yes** |
| 64 KB | room for 4 more pages | MMC5's two-chip split again; nothing in the design needs it | no |
| 8 KB battery + 24 KB volatile (NES 2.0 allows declaring both) | only the save is battery-backed | no MMC5 board has that shape, and which page number reaches the battery chip is not defined across emulators, so the save could land in volatile RAM | no |

### 2.2 Pages and the write gate

| Page | Role | Normally mapped at | Contents |
|---|---|---|---|
| 0 | **SAVE** | nowhere; `$A000` only inside the save module (§13) | meta.md's persistent blocks (SYS-A/B, FILE1-3 A/B, test mailbox) |
| 1 | **WORK** | **`$6000`, always** (`$5113 = 1`) | hot GP state, LIVE FILE / LIVE SYS images, object-list copy, raster list, text buffers, CHR stream queue (§3.4) |
| 2 | **LAYOUT** | `$A000` whenever the painter or collision maps `$6F` (bank id `$82`) | up to 4 layout sections of 2 KB (§5) |
| 3 | **TILES** | `$8000` whenever they map `$6E` (bank id `$83`) | the stage's metatile and block pages, a second slot, the alternate set (§5) |

MMC5's write gate (`$5102/$5103`) covers all PRG-RAM at once, so it must stay open while WORK is in use. **The save page is
protected by isolation instead**: no code maps page 0 except the save module, so a runaway write lands in WORK (rebuilt) or
in the current layout (rebuilt at the next stage start), never in the saves. The A/B copies and checksums (meta.md §1.3) are
the second line.

### 2.3 RAM probe at boot [new-code] S · Must

`ram_probe` writes a signature to `$6000` of pages 3, 2, 1, 0 (in that order, saving page 0's byte first), then reads them
back in reverse. If any page aliases another (fewer than 32 KB present), the game shows a one-screen message
**"THIS EMULATOR GAVE ROCKMAN 6 GP LESS THAN 32 KB OF PRG-RAM. CHECK THE NES 2.0 HEADER."** and stops, instead of corrupting
saves. FCEUmm always passes (it allocates 64 KB); the test exists for strict emulators and flash carts.

---

## 3. Memory map

### 3.1 CPU RAM (`$0000-$07FF`)

Vanilla is full: no free zero page (the 7 never-written zero-page bytes are live; poking them broke the Wily Capsule's death,
`rm6/ram.md`), stack headroom `$01A0-$01E4` is a safety margin, not storage. Free and confirmed over 232,722 traced frames:
`$06AF-$06FF` (81 B), `$07FA-$07FF` (6 B), `$0698`, `$064C` [seen, scout + critic]. **Rule (rm6 lesson 3): only bytes read
in interrupts or every frame by hot vanilla-side hooks live here; everything else lives in WORK.**

| Address | Name | Owner | Use |
|---|---|---|---|
| `$06AF` | `CWIN_CUR` | tech | bank currently in the `$C000` window (`$FE` = `$7E`) |
| `$06B0-$06B3` | `CW_A/X/Y/P` | tech | C-window dispatcher save area |
| `$06B4` | `IRQ_LINE` | tech | current absolute IRQ line (§1.7) |
| `$06B5` | `RL_CUR` | tech | raster-list cursor (0-15 buffer A, 16-31 buffer B) |
| `$06B6` | `RL_BASE` | tech | live buffer base (0 / 16) |
| `$06B7` | `RL_FLAGS` | tech | b7 staging dirty; b6 sound-in-IRQ; b0-3 chain id for `irq_logic_tick` |
| `$06B8` | `SECTION` | tech | current layout section 0-3 (§5.4) |
| `$06B9` | `CK_SECTION` | tech | checkpoint section (beside `$0684-$0686`) |
| `$06BA` | `GP_HOT` | tech | b0 window open, b1 world frozen, b2 autoscroll on, b3 T6 repaint pending, b4 DEV, b5 text owns NMI CHR slot, b6 new-stage entry (set by `$CD3B`/`$CD43`, read by the stage-init hook, §4.5) |
| `$06BB-$06BC` | `LFSR` | tech | 16-bit Galois LFSR (§7.8) |
| `$06BD-$06C8` | `SYS_HOT` | systems.md | 12 bytes for its ~10 hot values (SELECT hold, SEL_USED, SWAPMASK, LASTW, swap cooldown, CHR stream position, Time Stop, stagger, multi-kill) |
| `$06C9-$06D0` | `SND_BANK[8]` | tech | per-stream data bank for the sound reader (§12.2) |
| `$06D1-$06D8` | `TXT_HOT` | tech | text engine: state, delay counter, blip id, cursor, canvas slot, flags |
| `$06D9-$06DC` | `ASCROLL` | tech | autoscroll speed (8.8), sub-pixel, flags (§9) |
| `$06DD-$06FF` | reserve | any doc | 35 B, handed out through the hook registry |
| `$07FA-$07FF` | `NMI_EXT` | tech | NMI extension: window palette restore request, CHR-stream head/tail, VRAM-queue flags (next to the vanilla queue `$07F0-$07F9`) |
| `$0698` | `DEV_FLAGS` | tech | b0 EXTRA CONFIG used this boot, b1 godmode, b2 no-clip |
| `$064C` | reserve | | |

### 3.2 Zero page

No new zero page. GP routines borrow vanilla scratch `$00-$0F` inside a routine (vanilla's convention) and never across a
yield. Pointers that must survive an interrupt use absolute WORK addresses.

### 3.3 ExRAM (`$5C00-$5FFF`, 1 KB)

Mode 0 for the whole game (D7): ExRAM is a nametable that `$5105` can place in any of the four slots. CPU writes count only
**while the PPU is rendering** (in modes 0/1 MMC5 stores `$00` otherwise), and the CPU cannot read it back, so:

- `$5C00-$5FBF` hold the window and panel tile map (30 rows × 32), `$5FC0-$5FFF` its attribute table;
- the text engine keeps a WORK-RAM mirror and a small write queue (≤ 32 bytes per frame); the queue is flushed by a
  raster-list band routine at line 8 (`OPS` b6), i.e. **inside an IRQ, so always during rendering**. The `$5204` bit 6
  "in frame" flag is **not** used: FCEUmm does not implement it (a probe that polled it never left its loop) [seen];
- nothing else is stored in ExRAM.

Probes for this doc [seen, `probe/exnt2.nes`, `exnt2.png`]: ExRAM writes timed after the NMI (past vblank) landed; with
`$5203 = 120` and an IRQ that writes `$5105 = $AA`, scanlines 0-119 showed the CIRAM nametable and **scanlines 120+ showed
ExRAM**, on exactly line 120. A control build without the IRQ showed CIRAM only. ExRAM in mode 2 also behaves as RAM. Mesen
is checked in M1.6.

### 3.4 WORK page (page 1 at `$6000-$7FFF`)

| Range | Size | Use | Owner |
|---|---|---|---|
| `$6000-$61FF` | 512 B | **per-slot extension arrays**, 32-byte stride, slots 0-22: `$6000` GP_SUBID, `$6020` GP_ARG, `$6040` GP_OFLAGS, `$6060` LASTHIT, `$6080` LATCHSRC, `$60A0` REHIT, `$60C0` FREEZE, `$60E0-$61FF` 9 more AI variables (GPV0-GPV8) | tech / systems |
| `$6200-$621F` | 32 B | `SA_CUR`: the current stage-attribute record (§4.4) | tech |
| `$6220-$624F` | 48 B | stage loader state: `GRP_ROW` (16, the collision remap row), the `VARIANT` row (16), `RAM_ID` (id whose images are resident), `LIST_N` / `LIST_PTR` (the 3 bytes `$3A:$8032` now reads), section residency bits | tech |
| `$6250-$62FF` | 176 B | stage run block: systems' run block (~24 B), scorecard counters, announcer queue (16 entries × 2), T6 state | systems / meta |
| `$6300-$63FF` | 256 B | raster list, 2 × 16 bands (§8.1) | tech |
| `$6400-$69FF` | 1.5 KB | **object-list copy** (6 arrays × 255 + sentinels, §7.3) | tech |
| `$6A00-$6DFF` | 1 KB | text: glyph canvas buffer (48 tiles × 16 B), ExRAM mirror of the window rows, line buffer, choice state | tech |
| `$6E00-$6EFF` | 256 B | CHR stream queue (form swap, canvas, T6 debris) + WRAM-resident unrolled VRAM copier (§15.3) | tech |
| `$6F00-$6FFF` | 256 B | MMC5 audio: the second driver instance's channel state (§12.5) | tech |
| `$7000-$71FF` | 512 B | map-edit log (T6 refills, boss edits), poke-list scratch | tech |
| `$7200-$73FF` | 512 B | DEV ring buffer (last 64 events), test probes | tech |
| `$7400-$75FF` | 512 B | **LIVE FILE** (meta.md §1.2; same CPU address meta gives, but in page 1, §13) | meta |
| `$7600-$79FF` | 1 KB | **LIVE SYS** (meta.md §1.2) | meta |
| `$7A00-$7FFF` | 1.5 KB | free: handed out through the registry (venue objects' persistent state, Break Man, Bass Mode) | any |

---

## 4. Stage ids to 32 and the stage-attribute table

### 4.1 Why the id space breaks today

`$51` is read by **45 executed instructions** (`build/research/rm6/rm6-critic/stage_id_sites.txt`, each disassembled in
context for this doc in `sites51.txt`). A stage id ≥ 16 has bit 3 clear, so every "is this a fortress?" test treats it as a
Robot Master stage; the stage table `$3E:$DF25` (9 × 16), the object-list tables `$3A:$80BF/$80CF/$80DF` and the collision
groups `$3E:$DB03` are 16 entries packed against code; several tables are 8 entries (`rm6/engine.md` §9).

### 4.2 The id map (proposal; meta.md's meta index alongside)

| Engine id | Stage | Class | Meta index | Data |
|---|---|---|---|---|
| `$00-$07` | the 8 venues, **vanilla ids kept** (Blizzard 0, Wind 1, Plant 2, Flame 3, Yamato 4, Tomahawk 5, Knight 6, Centaur 7) | VENUE | 1-8 | new tileset slot each, new layouts |
| `$08-$0F` | **legacy** Mr. X 1-4, Wily 1-4, unchanged | LEGACY | none | vanilla data; serve meta.md's fight table (legacy arenas), Mr. X Returns' base map, and the vanilla regression movies |
| `$10` | Opening Ceremony | SPECIAL | 0 | |
| `$11` | Semifinal Riot | SPECIAL | 9 | |
| `$12-$15` | Exhibitions E1-E4 | EXHIBITION | 10-13 | |
| `$16-$1A` | Hall of Fame H1-H5 | FORTRESS | 14-18 | |
| `$1B-$1D` | Super Wily Castle W1-W3 | FORTRESS | 19-21 | |
| `$1E` | victory-lap credits | SPECIAL | 23 | |
| `$1F` | Mr. X Returns (Could) | FORTRESS | 22 | points at id `$08`'s layout and tileset (meta.md: "its layout stays in ROM") |
| `$20` | DEV sandbox (DEV builds only; the table has 33 rows there) | DEV | none | a copy of any stage, for tests |

All 32 ids are taken. If `fortress.md` needs more, the legacy block `$09-$0F` is the flex: the fight table needs a legacy
arena only for bosses it actually lists. Nothing in the new code assumes ids < 32 except table sizes; the field widths allow
64.

### 4.3 The 45 `$51` readers and their replacements [new-code] M · Must (part of D8)

`SA.x` = a field of the current stage-attribute record (`SA_CUR`, §4.4). "Retired" = the routine is replaced as a whole by
a GP screen owned by meta.md / fortress.md and no longer runs.

**A. Fortress tests on bit 3 (7 sites)**

| Site | Vanilla | Decides | GP |
|---|---|---|---|
| `$38:$916B` | `AND #$08 / BEQ` | player's end-of-stage path (fortress → `JMP $9208`) | `LDA SA.FLAGS1 / AND #FORT` |
| `$3C:$805F` | `AND #$08 / BNE` | game-over menu: fortress = CONTINUE only (script `$1A`) | `SA.FLAGS1.FORT` (meta's game-over menu reads it) |
| `$3F:$F0FB` | `AND #$08 / BEQ` | stage clear: fortress → `$F197` | `SA.FLAGS1.FORT` |
| `$3F:$F197` | `BIT $FF5C` (mask `$08` from `$FF58`) + `AND #$04` | which fortress map (`$F6D3` Mr. X / `$F6D8` Wily) | `SA.MAP` |
| `$3F:$F9A0` | `AND #$08 / BNE` | after the boss dies: weapon get (RM) or not | `SA.FLAGS1.YOUGET` |
| `$3B:$BB74` | `ORA #$08 / STA $51` | entering the fortress map | retired (fortress map) |
| `$3E:$CD95` | `INC $51 / BIT $FF5C / BNE` | next fortress stage, or the ending | `SA.NEXT` (`$FF` = return to the map; `$FE` = ending) |

**B. `CPY #$08` (3 sites)**

| Site | Decides | GP |
|---|---|---|
| `$3F:$EF6B` | boss damage: Robot Master rule (< 8) or fortress table column `$EFE4[class*8 + stage-8]` | `SA.FLAGS1.FORT` + `SA.FORT_COL` (systems.md replaces the tables themselves) |
| `$3F:$F4EB` | boss and plate flags only for stages < 8 (`$F6B3/$F6BB/$F6C3`, plate screen `$F518`) | `SA.FLAGIDX` (a bit index into the LIVE FILE) + `SA.PLATE_SCR` |
| `$3F:$F96A` | fortress boss room waits `$3C` frames | `SA.FLAGS1.FORT` |

**C. `CMP #n` stage specials (15 sites).** Nine are enemies picking a palette or a quirk by stage; the build turns each
into a column of a **variant row** (`SA.VARIANT` selects a row; rows 0-15 reproduce vanilla exactly, new rows are data).

| Site | Nearest AI / routine | Vanilla rule | GP |
|---|---|---|---|
| `$29:$942A` | type `$C0` (`$29:$941D`) | Flame (3) → palette `$92`; Mr. X 4 (`$0B`) → `$2E` | variant col 0 |
| `$30:$8341` | type `$14` (`$30:$8312`) | Tomahawk (5) → palette `$12` + `DEC $0624,X`; else `$BB` | variant col 1 |
| `$30:$8415` | type `$4F` (`$30:$8412`) | not Tomahawk → palette buffer `$037F = $24` | variant col 2 |
| `$30:$8C76` | type `$24` (`$30:$8C73`) | not Plant → palette `$36` | variant col 3 |
| `$30:$8DD2` | type `$29` (`$30:$8DCF`) | Wind → none; Knight → `$7E`; else `$E1` | variant col 4 |
| `$30:$953E` | type `$2D` (`$30:$953B`) | Knight → palette `$EB` | variant col 5 |
| `$30:$98D7` | type `$34` (`$30:$98D1`) | Wily 1 (`$0C`) → facing `$0C` + `JSR $E5E3` | variant col 6 |
| `$30:$9D36` | type `$54` (`$30:$9D33`) | not Plant → palette `$7D` | variant col 7 |
| `$3B:$870D` | type `$12` (`$3B:$870A`) | Blizzard (0) or Wily 2 (`$0D`) → palette `$D3` | variant col 8 |
| `$3B:$957D`, `$3B:$9588` | type `$7F` (`$3B:$9539`) | Wily 4 (`$0F`): keep `$069D` | variant col 9 |
| `$3E:$CDBD` | respawn | Centaur (7): clear `$0358` (alternate-set bits of metatiles `$C0-$C7`) | variant col 10 (a `$0340` index to clear, `$FF` none) |
| `$3E:$CDE5` | respawn | Wily 3 (`$0E`): clear the boss bar `$0642`/`$EF` | variant col 11 |
| `$3B:$BA3F` | stage start | ids ≥ 9 skip the weapon refill from progress flags | `SA.FLAGS1.KEEPWE` (systems.md's refill rules) |
| `$3F:$FA13` | boss shutter | Wily 4 → boss music `$18` | `SA.BOSS_MUSIC` |

**D. Tables and calls indexed by `$51` (20 sites)**

| Site | Reads | GP |
|---|---|---|
| `$39:$8480` / `$39:$848E` | shutter 1 / 2 parameter `$9A96,Y` / `$9AA6,Y` (16 each) | `SA.SHUT1` / `SA.SHUT2` |
| `$3B:$BDB8` | YOU GET weapon slot `$F704,Y` → `$0699` | `SA.YOUGET` → weapon slot table (systems.md: weapons by venue) |
| `$3B:$BDF0` | YOU GET text id `$60 + $51 + $06A5` | `SA.YOUGET` → text id table |
| `$3B:$BE7F` | YOU GET demo input `$BEAA,X` (a fake pad for the weapon demo) | index by `$063D` (8 entries suffice) |
| `$3B:$BD20` | saves `$51`, loads stage 5's data for the YOU GET room, restores | kept [engine-ok] |
| `$3C:$80D6`, `$8147`, `$8178`, `$8185` | boss intro: CHR `$F210`, anim `$F200`, palette `$F218`, anim `$F208` (8 entries each) | `Y = SA.INTRO`; the four tables relocated to N entries |
| `$3C:$81B1` | data-panel record `$8606/$860E` | `Y = SA.INTRO`; table relocated |
| `$3E:$CDF2` | `JSR $F533`: stage already cleared → revisit palettes (`$06A0`) | LIVE FILE `STAGE_CLEAR[SA.META]` and `SA.FLAGS1.REVISIT` |
| `$3F:$F94F` | `JSR $F527`: boss already beaten → beam out (no rematch) | `SA.FLAGS1.REMATCH` (meta.md and systems.md remove the beam-out) |
| `$3E:$CE07` | `JSR $DBDB` with A = `$51` (stage init on respawn) | the stage-init hook (§4.5) |
| `$3E:$DA1C` | `LDA $51 / BNE`: Blizzard's ship-deck collision offset | `SA.EFFECTS.SHIP` |
| `$3E:$DAEE` | collision group `$DB03,Y`, then `$DB13[group*16+type]` | `LDY $11 / LDA GRP_ROW,Y`: the stage's 16-byte remap row is copied into WORK at init (§4.5); 16 groups available |
| `$3B:$BB82`, `$BBC2`, `$BBD6`, `$BBE4` | fortress-map dot positions (`$BC5D`, `$BC86`) | retired (fortress map) |

**E. The 11 readers of `$063D`** (`stage & 7`, executed): `$31:$98B7/$98C1/$9930` (intro tables), `$31:$98F6` (`$9B82`),
`$31:$993D` (boss type `$9D43`), `$31:$99D9` (table `$9A35`, next to the weakness table `$9A45`), `$31:$9A1A` (Centaur's death), `$39:$8E8C/$8E9A/$8F42`
(Wily 3 refight room, palette, alcove), `$3F:$FA66` (boss sprite CHR `$FA5B`). They keep working if `$063D` holds the
**Robot Master slot** 0-7: init writes `SA.RM_SLOT` there instead of `stage & 7`, and the Wily-3-style rush overwrites it
per fight, as vanilla does.

### 4.4 The stage-attribute record (32 bytes) [new-code] M · Must

Stored as 32 tables of 32 (33 in DEV) entries in core bank `$3E` (new), the 4MI lesson of "a bank byte beside every
pointer" applied. At stage init the record is copied to `SA_CUR` (`$6200`), so patched readers use absolute addressing and
never map a bank.

| Off | Field | Meaning (vanilla source) |
|---|---|---|
| `$00` | `CLASS` | 0 VENUE, 1 FORTRESS, 2 EXHIBITION, 3 SPECIAL, 4 LEGACY, 5 DEV |
| `$01` | `FLAGS1` | b0 FORT (fortress rules), b1 YOUGET, b2 REMATCH, b3 KEEPWE, b4 NO_TAG (Break Man call off, systems.md), b5 REVISIT (bank-`$28` palettes when cleared), b6 TA_OK (Time Attack eligible), b7 NO_SAVE (credits, sandbox) |
| `$02` | `RM_SLOT` | → `$063D` |
| `$03` | `META` | meta.md's row, `$FF` none |
| `$04` | `NEXT` | next id on clear, `$FF` map, `$FE` ending |
| `$05` | `MAP` | which map/bracket screen follows (meta.md / fortress.md enumerate) |
| `$06` | `MUSIC` | `$DFA5` |
| `$07` | `BOSS_MUSIC` | `$0C`; `$18` for the Wily Machine (`$FA13`) |
| `$08` | `PALETTE` | start palette `$DF95` |
| `$09` | `CHR_BASE` | base BG CHR set `$DF85` |
| `$0A` | `COLL_GROUP` | remap row 0-15 (`$DB03`) |
| `$0B` | `LIST_ID` | object list of section 0 (into the list table, §7.3) |
| `$0C-$0D` | `LAYOUT_SRC` | ROM bank and page of section 0's layout (`$DF25`, `$DF45`) |
| `$0E-$0F` | `TILE_SRC` | ROM bank and slot page of the tileset (`$DF55`, `$DF65`) |
| `$10-$11` | `ALT_SRC` | ROM bank and page of the alternate set (vanilla: `TILE_SRC` bank, `$9B`) |
| `$12` | `SECT` | index into the section table (sections 1-3: layout source, tileset slot A/B, list id, HARD list), `$FF` none |
| `$13` | `EFFECTS` | b0 SHIP, b1 TIDE, b2 CEILING, b3 WM_FLOOR, b4 AUTOSCROLL allowed, b5 T6 cells present, b6 pop-ups at the bottom (default top), b7 no pop-ups |
| `$14` | `EFX_PARAM` | effect parameter (tide dwell, ceiling special screen; vanilla's `$57 = 6` test in handler 11) |
| `$15` | `FORT_COL` | fortress table column / systems.md's boss row |
| `$16` | `INTRO` | boss-intro record, `$FF` none |
| `$17` | `YOUGET` | YOU GET record (weapon slot, text id) |
| `$18-$19` | `SHUT1/2` | `$9A96/$9AA6` |
| `$1A` | `PLATE_SCR` | `$F518` (`$FF` none) |
| `$1B` | `FLAGIDX` | LIVE FILE bit set on the boss kill (replaces `$F6B3/$F6BB/$F6C3`) |
| `$1C` | `HARD_LIST` | poke list of section 0 (§5.5) |
| `$1D` | `SCORE_ID` | systems.md's scoring boss / meta.md's secret list |
| `$1E` | `PAR` | par time in 4-s units (systems.md §6.3) |
| `$1F` | `VARIANT` | variant row (§4.3 C) |

Rows for ids 0-15 are generated from the vanilla tables by `tools/build/stagetab.py`, and a test asserts that every vanilla
id's record reproduces the vanilla values (the M2 regression gate for this change).

### 4.5 Stage init and the relocated tables [new-code] M · Must

The hook sits at the entry of `$3E:$DBDB` (A = stage id), called from `$CD3B`/`$CD43` (new stage) and `$CE07` (respawn).
The two new-stage entries also set `GP_HOT`'s "new stage" bit, so the hook knows which case it is.

1. `$51` = id; copy the record to `SA_CUR`; `$063D = SA.RM_SLOT`; copy the 16-byte collision row to `GRP_ROW`; load
   `VARIANT` row into WORK.
2. **New stage, or an image that is not resident** (`RAM_ID` ≠ id): build the RAM images (§5.2), apply the poke lists,
   copy the object list to WORK (§7.3), clear the T6 log, set `RAM_ID`. The second condition matters: the YOU GET room
   calls `$DBDB` with A = 5 to borrow Tomahawk's data (`$3B:$BD20`), and meta.md's fight table enters arenas through the
   respawn warp (`$F0 = 2`), so neither goes through the new-stage entries. A plain respawn keeps the image (and its edits).
3. Set the zero-page level pointers exactly as `$DBFB-$DC17` did, but from RAM ids: `$6E = $83`, `$6F = $82`, `$52 = 0`,
   `$53 = $A0 + 8*SECTION`, `$63 = $80` (or `$89` for slot B), `$67 = $63 + 5`; `$064E = SA.CHR_BASE`; palette
   (`$C9EF` via `CALL7E`), music to `$DC`, HP `$1B`.
4. Return into vanilla at `$DC1F` (thread setup, PPU off, variable clears, checkpoint screen `$0684`, paint).

Relocated tables (all in core bank `$3E`, read only by GP code or by patched operands): the stage table `$DF25-$DFB4`
(replaced by the record); object lists `$3A:$80BF/$80CF/$80DF` (replaced by the list table with bank bytes, §7.3);
`$DB03/$DB13` (16 groups); `$F518`, `$F6B3/$F6BB/$F6C3`, `$F704`; intro `$F200/$F208/$F210/$F218` and panel
`$3C:$8606/$860E` (N records); shutters `$39:$9A96/$9AA6`. Freed vanilla bytes are returned to the allocator only after
the M2 gate passes.

---

## 5. WRAM-resident layouts (the 4MI model): decision

### 5.1 What 4MI does

At each section start 4MI copies the stage bank's block tables into WRAM and unpacks an LZ section of metatiles and screen
layouts into `$6500-$70FF`, then applies a NORMAL/HARD poke list; bosses and a terrain task edit the map live; an 8-byte
link table per stage wires loops and hidden rooms (`r4mi/engine.md` §6, §10).

### 5.2 The GP variant: a RAM image of the ROM bank

RM6's level data is raw and fixed-size (`rm6/levels.md` §3-4), and its readers find it through bank bytes in zero page
(`$6E` tileset at `$8000`, `$6F` layout at `$A000`) and page bytes (`$53`, `$63`, `$67`, the alternate set at `$9B-$9F`).
With D3, GP copies the data **into RAM pages laid out exactly like the ROM banks** and points those bytes at RAM:

| RAM page (id) | Mapped by | Layout of the page (CPU address when mapped) |
|---|---|---|
| 2 LAYOUT (`$82`) | `$6F` at `$A000` | section 0 at `$A000-$A7FF`, 1 at `$A800`, 2 at `$B000`, 3 at `$B800`: the same four page groups as a vanilla layout bank, so `$53` keeps its vanilla meaning |
| 3 TILES (`$83`) | `$6E` at `$8000` | slot A metatiles `$8000-$84FF` + blocks `$8500-$88FF` (`$63 = $80`); slot B `$8900-$91FF` (`$63 = $89`); T6 tables `$9200-$9AFF`; alternate set `$9B00-$9FFF` |

- No compression and no format change: `levels.py`'s round trip stays the authority for the bytes.
- **No vanilla reader changes**: the painters `$D1FF/$D322`, the address maths `$D904`, the collision read `$DA6C` (which
  maps `$6E` with `$CB91` and `$6F` with `$CBDA`, then reads `($54),Y` and `($68),Y` [code]) all run on RAM.
- Each venue's tileset can now have **its own alternate set** (venues_b's request) without wasting a whole 8 KB ROM bank:
  the loader copies slot pages and the alternate set from two independent sources, so two venues share one ROM bank.
- Cost: about 5.5 KB copied at a new stage start (2 KB layout section 0, 2.25 KB tileset slot, 1.25 KB alternate set;
  sections 1-3 and slot B on demand) with an unrolled copy, ≈ 50,000 cycles ≈ 1.7 frames, while the screen is already off
  for the 30-row paint.

### 5.3 Pros and cons

| | WRAM-resident (adopted) | ROM-resident (vanilla) |
|---|---|---|
| Map edits (bosses that dig, T6 cells, switches that open walls, VA-TIMED floors) | write a byte, repaint | impossible without alternate-set tricks per metatile id |
| HARD / CASUAL variants | a poke list per section (4MI) | a second layout copy |
| Sections > 32 screens | 4 sections in one page; switch = change `$53` | possible too, by switching `$6F`/`$53` |
| Per-venue alternate set | free | needs a full ROM bank per venue |
| Hidden rooms and links | exits with explicit targets (already data in RM6) | same |
| Load cost | ~1.7 frames at stage start | none |
| Persistence | layout survives deaths unless the stage asks to reset (vanilla's breakables do the same: `$0340` survives deaths) | n/a |
| Risk | a stray write corrupts the current stage only; 16 KB of RAM | none |
| Emulator dependence | needs 32 KB PRG-RAM and RAM in `$8000-$BFFF` (both confirmed on FCEUmm [seen]; Mesen expected, checked in M1.6) | none |

### 5.4 Recommendation

**Adopt it (Must)**, in the RAM-image form above, because T6 (BRIEF §4, venues_b Blizzard), map-editing set pieces, HARD
poke lists (BRIEF §5.7) and venue alternate sets all need it, and it costs no reader changes. **Sections: Should**: the
format reserves 4 × 32 screens per stage; the venues fit in 32 screens today (venues_a: Tomahawk and Plant use 32/32;
venues_b: 2-4 spare each). **LZ compression: Won't (v1)**: 1 MB leaves room for raw layouts (22 stages × ~1.3 sections × 2
KB ≈ 60 KB).

Section mechanics (Should): an exit target byte `$A0-$FF` (bit 7 = explicit target, as vanilla, plus bits 5-6 = section) means
"section `(t >> 5) & 3`, screen `t & $1F`". Inside a script, any byte ≥ `$80` after an exit's palette byte is read as its
target and exit types are 1-6, so these bytes cannot be mistaken for a list terminator. The exit handler hook (`$D6F5` path, `rm6/levels.md` §9) copies the section's layout if it is not
resident, sets `SECTION`, `$53` and the section's object list (§7.3), then runs the vanilla transition. Checkpoints store `CK_SECTION` beside `$0684-$0686`. Note that vanilla targets already use bit 7 with screens
`$00-$1F` (bits 5-6 clear), so every vanilla exit keeps its meaning.

### 5.5 Poke lists [new-code] S · Must

Applied right after a section is copied. Format, per list:

```
header: difficulty mask (b0 CASUAL, b1 NORMAL, b2 HARD, b3 1993), then entries:
        page_id (02 LAYOUT, 03 TILES, 01 WORK), offset_hi, offset_lo, value
        ... terminated by page_id $FF; several lists may follow, ended by mask $00
```

A list applies when `mask & current_preset_bit` ≠ 0, so one list can serve CASUAL and NORMAL. Per section the stage record
(`HARD_LIST`, and the section table) points at a chain of lists. Object placements are patched the same way (page 1 offsets
into the object-list copy). AI branches for HARD read the file's DIFF bytes (meta.md `$009-$00D`); tech provides the macro
`IFHARD` = `BIT DIFF_A / BVC` (b5 HARD on).

### 5.6 Map-edit API [new-code] S · Must

`map_set(section, screen, row, col, block)` writes a layout byte and queues a repaint of the 32-px column pair if it is on
screen (the vanilla repaint pattern of the oil ignition `$3E:$DE03-$DE5C`: set the paint cursor, `$D8AF`, `$D904`, `$D1FF`,
yield, next 8-px column). Every edit is appended to the map-edit log (`$7000`) with the old byte, so `map_undo_all()` can
restore a boss room after a death and EXTRA CONFIG can show what changed.

---

## 6. Level pipeline

### 6.1 What exists [done by research]

`tools/analysis/rm6/levels.py`: decode, encode, **byte-exact round trip** of all 16 stages at bank level and JSON level,
`build_rom()` with object-list repacking (proven in game: a new platform and a new 1-up on Blizzard 00), the screen graph
`walk()`, the full-map renderer, `decode_script()`, `trace()` (`rm6/levels.md`). M0 moves it to `tools/build/levels/` and
adds what follows.

### 6.2 Authoring format (`assets/levels/<stage>/<section>.lvl`) [new-code] M · Must

Plain text, diffable, writable by Claude and by hand. Blocks are **2 hex digits** (up to 256 block ids, BRIEF §4).

```
stage    WIND                     # id $01
section  0
tileset  wind_a                   # assets/tilesets/wind_a/ (blocks.txt, metatiles.txt, chr sets)
chr      base=83 extra=8C
palette  17
music    00

map                               # 2-D placement: screen ids by position; . = empty
  00 01 02 03 .. ..
  .. .. .. 04 .. ..
  .. .. .. 05 06 07
  18 .. .. .. .. ..               # hidden room, reached only by a link

screen 03                         # 8 rows x 8 blocks; row 7 shows only its top 16 px
  1A 1A 1A 1A 1A 1A 1B 00
  00 00 00 00 00 00 2C 00
  00 00 00 00 00 00 2C 00
  00 00 41 41 00 00 2C 00
  00 00 00 00 00 00 2C 00
  00 00 00 00 00 00 2C 00
  30 31 30 31 30 31 30 31
  32 33 32 33 32 33 32 33
  obj  40 A0 $4D                  # x y type (vanilla snow robot)
  obj  C0 70 F4:SKYMINE arg=2     # GP family $F4, sub-id by name, 1-byte argument
  checkpoint                      # LDA #$03 / JMP $8416
  script init=VA_GUST(1) pf=-

link 06.up -> 18                  # explicit-target exit (hidden room)
link 07.right -> S1:00            # section 1, screen 00 (Should)
hard 05 row=6 col=2 = 2C          # poke list entries (HARD); also casual / 1993
```

The `map` grid makes **scroll modes and ordinary exits generated, not hand-written**: horizontal neighbours give mode bits 0/1
(the vanilla convention: mode 1 at the start of a run, mode 2 at its end, free scrolling between), vertical neighbours give
down/up exits (types 1/2 or 3/4 with explicit targets) and use the shared shaft scripts `$02/$07` where they fit
(`rm6/levels.md` §9-10, lesson "the 2-D shape is code"). `link` lines add explicit targets (branches, hidden rooms, plate
rooms in `$18-$1F`). `script` lines attach init/per-frame routines by name from the hook registry.

### 6.3 Build and checks [new-code] M · Must

`tools/build/levels/build.py`: `.lvl` → the `levels.py` JSON schema → `encode_stage()` → regions handed to the allocator
(layout section in a layout bank, tileset slot, object list, scripts, poke lists) → the stage-attribute record fields.
Checks that fail the build:

1. every block id exists in the tileset; every metatile has a collision nibble;
2. no spawn point or checkpoint inside a solid cell (the first edit test killed Rockman inside a new platform,
   `rm6/levels.md` §14);
3. every screen in `map` is reachable by `walk()`; every `link` target exists; no exit scrolls into an empty screen;
4. **every checkpoint screen's palette is self-contained** (palettes are cumulative deltas; lesson: "test respawns");
5. sprite CHR conflicts per screen (§7.6);
6. live-object count per screen ≤ 8 plus shots (the lag budget, §15);
7. block/tile budget report per tileset (blocks used / 256, BG tile ids used / 256).

Outputs: the ROM regions, `build/maps/<stage>.png` (the existing renderer), and a per-screen table for the text engine's
canvas (§11.4).

**Round trip as a regression:** `levels decompile` writes `.lvl` for all 16 vanilla stages, and `build` must reproduce the
vanilla bytes exactly (the existing JSON round trip extended to the text format).

### 6.4 The 32-screen limit and how sections extend it

A layout is 8 rows × 256 columns, and the column index `screen*8 + x/32` is one byte (`$D904`), so **32 screens per layout
is a hard limit** of the vanilla readers (`rm6/levels.md` §3). Sections (§5.4) extend a stage to 4 × 32 = 128 screens without
touching the readers. Vertical sections stay "more screen indices" as in vanilla.

### 6.5 Link tables

RM6 already stores connectivity as data: screen-script exits with an explicit target (`$80|screen`) jump anywhere in the
strip, and that is how the vanilla plate routes reach `$18-$1F`. GP keeps that and adds only the section bits (§5.4), the
teleport routine `$39:$89F5` for scripted warps (as Wily 3's hub does), and the build-time link check. A one-screen hidden
room (BRIEF §5.4) is one `link` line plus one screen. **[engine-ok]** for single-section stages.

### 6.6 Screen scripts

Vanilla has 128 script ids (`$39:$82EB/$836B`), 968 bytes of bodies, and the interpreter runs with banks `$39/$3A`
mapped. GP relocates the pointer table to 256 entries in `$3A`'s free space (`$3A:$95D4-$9FFF`, 2,604 B of fill after the
vanilla object lists; GP's new lists go to GP banks instead, §7.3), patches the two `LDA $82EB,Y / LDA $836B,Y` operands, and
puts new script bodies there too (one script ≈ 6-12 bytes, so ~2 KB holds ~200 scripts). GP init and per-frame routines
that return at once point at `$7F` trampolines (`CW` targets), since the interpreter calls them with `$39/$3A` mapped.
Routines that wait with yields (Plant's `$39:$8551` pattern: spawn a mid-boss, loop until slot 8 is empty, then
`JMP $827C` back into the interpreter) run as object code instead: they switch slot 22's own bank pair (`$0441`) to a GP AI
bank, and map `$39` back before `JMP $827C`.

---

## 7. Object / AI framework

### 7.1 What exists [done by research]

23 slots × 29 arrays at `$03A0`; type tables `$3A:$82C9/$83C9/$84C9/$85C9`; init `$3A:$81F0`; the 6-byte AI header read by
`$EBD5` (anim, palette, CHR set, hit box, HP, attack); coroutines (`JSR $E46C` yield, `JMP $E45A` delete, `$E47B` end turn);
allocators `$E514` (shots), `$E59F`/`$E5AF` (enemies); the metasprite format (118/118 verified); the damage routines
(`rm6/engine.md` §1-2).

### 7.2 Free type ids and GP families [new-code] M · Must

Types with AI pointer `$0000` (clean): `$42 $7B-$7E $BA-$BF $CE $D7 $DB-$DF $F4-$FF` = **30**. `$CF` and `$D2` point at
filler and are listed free in `rm6/engine.md`, but `$D2` is also named as a Mr. X 4 part there: both stay reserved until
checked. Venues alone ask for ~90 new object kinds (venues_a ~45, venues_b ~46), so **one type id per kind cannot work**.
GP uses **families**: a type id plus a sub-id, the 4MI `$5E` pattern.

| Type | Family | Examples |
|---|---|---|
| `$F4` | GP enemy | venue enemies (Metslime, scorpions, Toppy seals) |
| `$F5` | director / set piece | wave director (T1-lite), raster-band object, T3 switch and target, gust zone, search spot |
| `$F6` | pickup | bolts, chips, sponsor envelopes, plates as pickups, PARTs |
| `$F7` | event trigger | commentator hooks, NPC talk, dialogue starters, debrief predicates |
| `$F8` | boss controller | GP bosses and reworked champions' controllers |
| `$F9` | boss part | hit boxes and segments (T8) |
| `$FA` | enemy projectile | |
| `$FB` | player-side GP shot | weapon alternates and synergies (systems.md) |
| `$FC` | Break Man | the tag partner body |
| `$FD` | effect | swap flash, debris, WEAK! pop |
| `$FE` | DEV probe | test objects |
| `$FF` | reserve | |
| `$42 $7B-$7E $BA-$BF $CE $D7 $DB-$DF` | single-purpose ids | handed out only when vanilla code tests a type id directly (as the tide moves type `$72`) |

**Per-sub-id table** (per family, in core bank `$3E`, ≤ 256 entries): AI entry (lo, hi), AI bank pair, sprite bank pair, a
GP flag byte (frozen-immune, wrap, NOPARRY, NOFREEZE…). The 6-byte header still sits in front of the AI entry and is read by
`$EBD5` as usual.

**Dispatch costs nothing at run time**: the family's own entry in `$3A:$82C9/$83C9/$84C9` points at a small resolver, but
the init hook (`$3A:$81F0`, far fn 1, Y = type, X = slot) writes the sub-id's real AI address, bank (`$0441`) and sprite
bank (`$0458`) into the slot directly, so the object loop never sees the resolver. `$0458` is per slot already (the OAM
builder reads it per object, `rm6/engine.md` §1.5), so families are not bound to `$85C9`'s 16-type rows.

Spawning: level placements carry the sub-id (§7.3); child objects use `gp_spawn(family, sub, arg)` = `$E59F` (allocate),
write `GP_SUBID,X` / `GP_ARG,X`, then init. Plain `LDY #type / JSR $E5AF` keeps working for vanilla types.

### 7.3 Object lists in WORK [new-code] S · Must

Vanilla lists are 4 parallel arrays with sentinels (`screen, X, Y, type`), sorted by (screen, X), read through zero-page
pointers `$74/$78/$7C/$7E` set by `$3A:$8032` from `$80BF/$80CF/$80DF` [code]. GP:

- **ROM format v2** adds two arrays, `sub` and `arg` (6 × n + 6 bytes); vanilla lists stay in v1 where they are.
- At stage or section load, the list is copied to WORK `$6400` (v1 lists get zero `sub`/`arg`), and `$3A:$8032` is patched
  to load the count and pointers from 3 fixed WORK bytes (`LDA $80DF,Y` → `LDA LIST_N` etc., same length), so the spawner
  `$3A:$8120` and the kill bitfield `$0650` work unchanged.
- The spawn site in `$3A:$8120` copies `sub[i]`/`arg[i]` into `GP_SUBID,X`/`GP_ARG,X` before init (one detour).
- **List table**: up to 64 lists, each (bank, address, count, format); the stage record and the section table hold list ids.
  The 256-object ceiling per list (kill field `$0650-$066F`) stays.
- Poke lists can patch the copy (§5.5): HARD extra enemies cost no second list.

### 7.4 The AI header and the coroutine rules

- New AIs keep the 6-byte header (anim, sprite palette, sprite CHR set, hit box, HP, attack) and start with `JSR $EBD5`.
- Hit-box ids index the size table used by `$F72A`; new sizes are appended to that table (relocated if full; M2 task).
- **Yield** with `JSR $E46C` (the resume address is stored in `$0413/$042A`, so an AI can yield from any depth of its own
  code but never from a subroutine in another bank); **die** with `JMP $E45A`; **end turn** with `JMP $E47B`.
- AIs run in `$8000/$A000` banks (`$0441` = the even bank of the pair), never in the C-window (§1.9).
- Ophis macros (`src/gp/ai.oph`): `YIELD`, `WAIT n`, `DIE`, `ANIM id`, `MOVE`, `SPAWN fam,sub,arg`, `IFHARD`, `TELL id`
  (queue a commentator line), `ONHIT` (read and clear the latch `$056C` through the damage routines systems.md picks).

### 7.5 Metasprite pipeline [new-code] M · Must; [new-art] per enemy

Input: a PNG sheet per object (4 colours) + `sprite.json` (frames as lists of 8×8 cells with flips and offsets, animations as
`[frame, duration]` lists). `tools/build/sprites.py`:

1. slices and de-duplicates tiles (flip-aware), emits a sprite CHR set (the CHR-set table format `$37:$8000`: count, PPU
   address/16, source/16, bank+flags) in a CHR bank;
2. emits frames `[n-1][layout id]` + n × `[tile, attr]`, layouts n × `[dy, dx]` (shared across frames), animations (half
   flag + `[frame, duration]` pairs) into a GP sprite bank pair, at the vanilla offsets (`$8000/$8200` (+`$8100/$8300`)
   frames, `$8400/$8500` layouts, `$8600/$8700` animations; ≤ 256 per table, `rm6/engine.md` §1.5);
3. renders a preview through the same decoder `spritefmt.py` used to verify 118/118 vanilla sprites, and diffs it against
   the PNG.

Vanilla sprite banks have 1.2 / 2.3 / 4.3 KB of fill (`$20/$22/$24`); GP objects go in the new pairs `$52-$59`.

### 7.6 Sprite CHR set conflicts [new-code] S · Must

When the camera enters a screen, `$3A:$826F` queues the CHR set (AI-4) of each object type on that screen unless it is in
the 8-entry recently-loaded list `$07E8-$07EF`; the NMI drains the 8-entry ring `$07F0` (`rm6/levels.md` §6). Two sets that
overlap in `$1000-$1FFF` cannot share a screen. For families, the hook makes `$826F` read the set from the sub-id's header.

The build check: for every screen, the union of sets queued on it **and on the screens the camera can reach without a
transition** (sets persist), as PPU tile ranges; any overlap between sets used together is an error, with the offending
objects named. It also reports the per-screen free sprite tiles. For scale: across 73 vanilla in-stage scenes only 11 sprite
tile ids were never shown (`$3B-$3D $4D $4F $7D-$80 $8A-$8B`) [seen: `sprtiles.py`], so the sprite table is effectively full
and new enemies must replace, not add.

### 7.7 Collision, damage and the frozen tick

- Damage tables and their special cases belong to systems.md; tech provides the hook points it lists (§15.1 there) in the
  registry, and the **latch source**: the shot-vs-enemy routine `$38:$8FDF` writes `LATCHSRC,X` (WORK `$6080`) with the
  shot's weapon slot when it copies the attack byte into `$056C`, so kill attribution (VARIETY, PACIFIST) is exact.
- **Frozen tick** (systems.md's FREEZE): an inline `$7F` patch in the object loop `$3F:$E438`, before the bank map: if
  `FREEZE,X` ≠ 0, decrement it and skip the AI call; the OAM builder draws the object anyway (it is a separate pass). Cost
  ≈ 8 cycles per live slot.
- **Death-hook audit** (systems.md asks): a static scan for stores of the death types `$17`/`$25` into `$03A0,X` and for
  calls of `$ED42`, cross-checked with shadow6 coverage of every boss kill in the golden suite, lists every custom death path
  (M2 task).

### 7.8 RNG

Vanilla's RNG `$DF-$E1` is advanced every NMI (`$C88D`) [code], so it depends on lag. GP's **LFSR** (16-bit Galois, taps
`$B400`, in `LFSR`) advances only when called, is seeded at stage start from a per-stage constant (Time Attack fairness:
venues_a's quick-draw delay) and in normal play is mixed with the frame counter at the first input of the stage.

### 7.9 Player extensions [new-code] S each · Must unless marked

Rockman is slot 0's coroutine (AI `$38:$802D`; resume points stand `$8055`, tiptoe `$808A`, walk `$80AF`, air `$810B`, pit
death `$8F13`, HP death `$8E7F`, `rm6/ram.md`). So:

- **GP player states** need no dispatch hook: GP code takes slot 0 over by writing `$0441` (its bank pair) and
  `$0413/$042A` (its routine), sets `$94` to a GP value (`$10+`), and hands back by writing the vanilla air or stand resume
  address. Used by T5 (hang on a vine or pendulum, venues_a), X-EXWP (Yamato's pogo, venues_b), and systems.md's set pieces.
- **Exit type 7** (X-UPEXIT, Should): the exit handler table is 7 entries, `$39:$9A88` (lo) / `$9A8F` (hi), type 0 unused,
  handlers `$D587 $D612 $D540 $D5D1 $D653 $D6B3`, read at `$A290/$A295` (bank `$3A` mapped at `$A000`) [code]; the shutter
  tables follow at `$9A96`, so the table is relocated to `$3A`'s free space with room for types 7-9 and the two operands are
  patched. Type 7 fires when the player is rising, `Y < $0B`, and the cells above are open; it reuses the type-2 scroll-in
  (`$D82D`) with a small upward boost.
- **X-WRAP** (venues_b): a post-move hook on slot 0 (and on objects whose `GP_OFLAGS` has WRAP): in a locked room, X < `$08`
  becomes `$F0` and back, unless the row is flagged as an exit.
- **Pad history** (T7, Should): a 64-frame ring of `$40` in WORK, written by a 4-byte hook at the end of the joypad read
  `$3E:$C711`; the mirror object replays it with LEFT/RIGHT swapped.
- **Ceiling probe callback** (X-BONK for T6): a hook where the player's upward collision stops the jump, passing the cell's
  collision type and position.

### 7.10 T3: switch → target [new-code] M · Must

Family `$F5`, two kinds of sub-id joined by a **channel** (the placement's `arg`, 0-15). WORK holds `CHAN[16]` (state bytes)
in the run block; channels that must persist across deaths are flagged in the stage data and saved in the map-edit log.

| Switch kinds | Target kinds |
|---|---|
| shot (any class, or one weapon class), touch, plate (standing on it, the vanilla class-2/5/9 platform contact `$38:$8F96`), key (consumes a per-stage key counter in the run block: venues_a's question 6), timer, all-of-N (counts channel hits) | door (UP to enter → exit with an explicit target), gate (a solid object, class 2/5/9, that slides away), wall (`map_set` + repaint, §5.6), warp (`$39:$89F5`), lift (rides through a down exit), spawner, palette/music change (CX's object `$40` idea) |

A target reacts on the frame its channel changes; every link is checked by the level build (§6.3).

### 7.11 T8: multi-part bosses [new-code] M · Should

The vanilla pattern (the gorilla tank `$50-$53`, the Wily Machine's `$E9` boxes, `rm6/engine.md` §1.4) as a library: the
controller (family `$F8`) sits in slot 8 and owns the boss bar (`$0642`); parts (family `$F9`) are glued each frame at
`controller + offset` (per-part offset tables), use class 0 hit boxes (shots pass through and latch, `$38:$9021`), and
forward their latch to the controller with a per-part multiplier, so systems.md's damage and i-frame tables still decide.
`part_spawn(offset, sub)`, `parts_glue()`, `parts_kill()`. Used by venues_a's AYACO bomber and venues_b's Daruma.

---

## 8. The generic raster list [new-code] M · Must

### 8.1 Format

Double-buffered, 16 bands per buffer, struct-of-arrays in WORK (`$6300-$63FF`); buffer A = index 0-15, buffer B = 16-31.
Game code builds the **staging** buffer at any time; the NMI swaps buffers (no copying) when `RL_FLAGS` b7 is set, the
4MI commit rule (`r4mi/engine.md` §4.2) without 4MI's copy loop.

| Array | Field | Meaning |
|---|---|---|
| `$6300,X` | `LINE` | absolute scanline 1-239 at which this band starts; `$FF` ends the list |
| `$6320,X` | `OPS` | b0 write PPUADDR (`$2006` hi/lo), b1 write scroll (with b0: the 4-write `$2006/$2005/$2005/$2006` split that sets X, Y and nametable), b2 PPUCTRL, b3 PPUMASK, b4 `$5105` (nametable mapping: window bands), b5 call the sound update after this band, b6 call a band routine (`ARG` = routine index), b7 palette swap (rendering off, 4 BG colours, rendering on: **only allowed in the last band**, §8.4) |
| `$6340,X` / `$6360,X` | `HI` / `LO` | PPUADDR, or the two precomputed `$2006` bytes of a scroll split |
| `$6380,X` | `SX` | fine/coarse X |
| `$63A0,X` | `SY` | Y for scroll splits |
| `$63C0,X` | `CTRL` | PPUCTRL value |
| `$63E0,X` | `MASK` | PPUMASK value (4MI's water tint and sprite-free bars, CX's effect 8) |
| (shared) | `ARG`, `MAP5105`, palette set | 3 small arrays in `$7A00+` or folded into `HI/LO` by op; fixed in M2 |

### 8.2 The walker

In `$7F` (fast, no C-window switch). NMI: if the staging flag is set, flip `RL_BASE`; `RL_CUR = RL_BASE`; `$5203 =
LINE[RL_CUR]`; `$5204 = $80` (or 0 for an empty list). IRQ: `LDA $5204` (ack), load band `RL_CUR`, do its ops in the order
CTRL → `$5105` → PPUADDR/scroll → MASK (the order 4MI and CX use), increment the cursor, arm the next `LINE` or disable,
run the band's sound/routine flags, RTI. ~70-90 cycles per band; a per-line effect (shimmer, wobble) is a run of bands or a
band routine that re-arms itself (`OPS` b6), like vanilla handlers 9 and F.

### 8.3 Presets that replace the 27 chains (M2)

| Preset | Bands | Replaces | Used by |
|---|---|---|---|
| `RL_FLOOR(line, addr, scroll)` | 1 | 7, 1A, 19 (with drift in `irq_logic_tick`) | Plant 0E, Mr. X 2/3, Wily 2, Wily Machine; BG bosses (H wings) |
| `RL_SHIP(...)` | 3 | 1-2-3 | Blizzard ship (venues_b keeps it) |
| `RL_PARALLAX(line, divisor)` | 2 | C-D | Tomahawk, venues_a T4 |
| `RL_SHIMMER(line, n)` | 1 + n | E-F-10 | Tomahawk sunset |
| `RL_CEILING(h)` / `RL_TIDE(h)` | 2 | 11-12 / 14-15 (logic in `irq_logic_tick`, §1.8) | Knight, Centaur; Yamato (venues_b) |
| `RL_MULTI(...)` | 2 | 16-13 | Mr. X 4 machine, reveal |
| `RL_WEAPONGET` | 2 | 17-18 | YOU GET |
| `RL_MENUSLIDE` | 2 | 4-5 | adaptor change (systems.md's quick path skips it) |
| `RL_STORY` | n | 8-9, A-B | opening (replaced by the GP attract, meta.md §2.1) |
| `RL_WINDOW(top, rows, pal)` | 1-2 | new | text windows and pop-ups (§11) |
| `RL_BANDS(list)` | ≤ 6 | new | venues_a T4: "≥ 4 bands + the window band"; T1-lite |

A **band compositor** merges the stage's preset, the window band and any director-object bands by line, drops the lowest
priority band if more than 16 are asked for, and writes the staging buffer once per frame. CX's trick of an invisible
object whose position gives a band's line and height (`cx/engine.md` §8) is family `$F5` sub `BAND`.

### 8.4 Rules

1. **Rendering-off writes end the list.** MMC5 counts scanlines only while the PPU renders; a palette swap (rendering off)
   resets its counter, so no IRQ can follow in that frame. Palette-swap bands are therefore last (the bottom dialogue
   window); a top pop-up uses one of the stage's own BG palettes.
2. **Sound in the IRQ**: vanilla's rule is kept generically: if the first band's line is below `$70`, the NMI skips the
   sound update and the first band with `OPS` b5 (or band 0) runs it.
3. Lag frames re-arm the same list (vanilla's lag path `$C0C4` does the same for chains).
4. Line budget: a band's writes must land in h-blank; the walker is calibrated once against vanilla splits (§14.4).

---

## 9. Autoscroll (T1)

### 9.1 T1-lite: fixed-camera rides [new-code] M · Must

Accepting venues_a's proposal (its §0.4 and open question 1): **the camera is locked** (screen-script mode 0, vanilla),
**raster bands scroll by time** (and by camera for parallax) through `RL_BANDS`, and a **wave director** (`$F5` sub
`WAVES`) spawns enemies from a list `[frame, family, sub, x, y, path, arg]`, counted from the screen lock so every run is
identical (golden movies, Time Attack). Nothing solid moves, so collision, spawning and exits stay vanilla. The ride ends at
the list's `END` entry, which unlocks the screen (mode 1).

- In a locked room the director may switch `$FB` to vertical mirroring (two nametables side by side) so band art loops
  every 512 px instead of 256; the exit restores it.
- Cap: 6 director-spawned objects alive (the lag budget, §15).
- Used by: Wind's sortie (01) and wing arena (1D), Tomahawk's train (10-11) (venues_a). venues_b's ski run needs none (a
  forced-slide floor type, X-FLOOR).

### 9.2 T1-full: forced horizontal scroll [new-code] M · Could

Only if a venue needs terrain that moves. Design:

- `ASCROLL` (speed 8.8, flags) is set by a script init; the camera-follow step in the horizontal scroll routines
  (`$3E:$DCE2` right / `$DD42` left, `rm6/levels.md` §5) uses `camera += speed` instead of following the player; the
  column painter runs unchanged as the camera crosses 8-px boundaries.
- The player is pushed by the existing left clamp `$A8` (camera-relative, `$10`, `$38:$8F31`) and stopped by a new right
  clamp (`camera + $F0`). **Crush**: pushed by the clamp while a wall blocks him on the left → the pit-death path
  (`$38:$8F13`).
- Every screen in the run is mode 3 (free); the last screen's script clears `ASCROLL`.
- Vertical autoscroll: **Won't (v1)**; vanilla scrolls vertically only during scripted transitions.

---

## 10. Per-position destructible tiles (T6) [new-code] M · Must

Vanilla breakables are **one bit per metatile id** in `$0340` (all blocks sharing the id open together; only the full punch
`$14` or F.BLAST), so they cannot break one cell of an ice floor (`rm6/SUMMARY.md` §1.6, lesson 6).

**Design: rewrite the RAM layout with authored variant blocks.**

1. **Mark**: metatile attribute **bit 2** = DESTRUCT (bits 2-3 are 0 in every metatile of every vanilla stage [code]).
   Collision ignores the bit.
2. **Author**: the tileset tool expands every block that contains DESTRUCT metatiles into its **variants** (each subset
   of those quadrants replaced by the tileset's RUBBLE metatile, usually air): 2^k − 1 extra block ids for k breakable
   quadrants, plus a **transition table** `(block, quadrant) → block` in the TILES page (`$9200-$9AFF`). A floor block
   with 2 breakable cells costs 3 ids; the build reports the total against the 256-block budget.
3. **Break**: a trigger calls `t6_break(x, y)`: venues_b's head-bonk X-BONK (a callback on the player's ceiling probe),
   a weapon class hit, or the punch. It finds the layout byte and quadrant, looks up the transition, writes the new block
   id into the LAYOUT page, logs the old byte (map-edit log, §5.6), spawns debris (family `$FD`), and queues the repaint.
   **Collision changes on the next probe**, because `$DA6C` reads the RAM layout.
4. **Repaint**: the oil-ignition pattern (`$3E:$DE03-$DE5C`): two 8-px columns through `$D8AF/$D904/$D1FF`, one per
   frame. At most one break starts per frame; more are queued.
5. **Refill** (venues_b's Ice Climber floors): `t6_refill()` writes the logged byte back and repaints.
6. **Persistence**: broken cells survive deaths and reset at the next stage start (vanilla breakables' rule); a stage flag
   can refill on respawn instead.

**Alternative kept as fallback**: a 1-bit-per-16×16-cell bitmap (1 KB per section), checked for bit-2 metatiles inside
`$DA6C` and both painters, as 4MI's `$7E:$D5A7` does for its type-`$E` cells. It costs no block ids but patches the three
hottest level routines (collision alone is 7 % of the frame, `rm6/engine.md` §8); use it only if a venue runs out of block
ids.

---

## 11. Text and dialogue engine (T2) [new-code] L · Must

### 11.1 Three layers

| Layer | When | Engine |
|---|---|---|
| Full-screen text | attract, story cards, ending, CAPCOM TIMES, staff roll | **vanilla PPU scripts** (`$3C:$8631`, 168 scripts, typewriter via `$069F/$06AC/$06A6`), with a language hook |
| **Dialogue window** | story beats, NPCs, shop, debrief, choices; the world is frozen | new: bottom window, 3 lines, portrait, choices |
| **Pop-up** | commentators (BRIEF §5.5), live, ≤ 2 lines, toggleable | new: top band (or bottom per screen), no freeze |

### 11.2 Full-screen text and the language hook [new-code] S · Must

One hook in the interpreter at `$3C:$8636` (where it reads the pointer from `$8787/$882F`, `rm6/text.md` §8) picks the
pointer table by `LANG`. EN scripts live in a GP text bank, so the interpreter (~370 bytes) is copied into that bank pair and
reached through `FAR`; the far-call slot table `$CB5F` (4 slots, all used) is not touched. EN text uses the vanilla capitals
(A-Z, 0-9, `. ? ! ' : ,` are in every main-font scene, `rm6/text.md` §7) or a language-specific font set loaded instead of
`$81/$D2` when mixed case is wanted. Line breaks are command addresses, so EN layouts are re-flowed by the encoder
(`rm6_ppuscript.py` already encodes `row, col, "text"`).

### 11.3 Window display

- **Nametable**: the window's tiles live in **ExRAM** (D7). The window band sets `$5105 = $AA` (all four nametable slots →
  ExRAM) and points `$2006` at the window rows; the NMI writes the stage's mapping back every frame (§1.5). No vanilla
  nametable byte is touched, so the playfield never needs repainting.
- **Palette**: the bottom dialogue window swaps BG palette 3 in its band (rendering off for 1-2 lines at the border, the
  CX effect-10 trick, `cx/engine.md` §3.2); the NMI restores it from the `$0360` buffer while a window is open. The top
  pop-up cannot swap (§8.4) and uses the stage BG palette the build picks for contrast (§11.4).
- **Sprites**: the dialogue band turns sprites off (PPUMASK); a pop-up band keeps them on so the life bars stay visible.

### 11.4 Glyph canvas and where its CHR comes from

Measured constraints: the BG table is nearly full on most stages (Plant has 0 free ids over all its CHR configs; 12 of 16
vanilla stages have ≤ 11 free, `rm6/SUMMARY.md` §2), and **the sprite table shows 245 of 256 ids in play** (73 scenes,
`sprtiles.py`). CHR-RAM is 8 KB and cannot be banked further on the test emulator (D6). So the engine draws text into
**borrowed BG tile ids**:

- The level build computes, per screen, the BG tile ids that neither that screen nor its scroll neighbours reference
  (the method of venues_a's `swapcap.py`), and stores per screen up to two runs of 16 canvas ids, their CHR source
  (bank, offset) for restoring, and the best BG palette for text.
- **Pop-up**: 2 lines × 16 tiles (32 ids) from the free runs; with one run it becomes a 1-line ticker; with none, the
  line waits in the announcer queue (max age 8 s) until a screen with room, a death/respawn, or a boss intro.
- **Dialogue**: the world is frozen (scheduler threads 1-2 suspended, as the pause menu does, `rm6/ram.md`), so it may also
  borrow ids in use: it reads their 16 bytes back through `$2007` into WORK during vblank while the box opens (8 tiles per
  frame), and writes them back while it closes. Budget: 3 lines × 26 columns of glyphs need ≤ 64 canvas ids with tile reuse
  per line (a VWF line packs ~1.4 characters per tile) + 16 for a 32×32 portrait.
- **Rendering**: 1bpp fonts in PRG, 8 px tall. **EN uses a VWF** (a width table; each glyph row shifted into the 16-byte
  tile buffer with `LSR/ROR`, CX `$26:$8490`), with a highlight colour from bitplane 1 (CX). **JP** is 8 px fixed-width,
  kana with dakuten composed into one glyph (vanilla spends a cell on each mark), plus a small **kanji** set (Should): with a
  canvas, a kanji costs 8 PRG bytes and no CHR, so the build only reports which kanji the script uses. ENGRISH uses EN
  glyphs.
- Each finished tile goes through the CHR stream queue (16 B, §15.3); typewriter speed and per-speaker blip use the
  vanilla variables' pattern (`$06AC`, `$06A6`).

### 11.5 Script format

Source: `assets/text/{ja,en,engrish}.yaml` (ENGRISH holds only overrides; missing ids fall back to EN, meta.md's request).
Encoded by `tools/build/text.py` into per-language banks with a 16-bit string id table. Control codes (CX's opcode set,
`cx/text.md` §1.1, adapted):

| Code | Meaning |
|---|---|
| `END`, `NL`, `CLEAR`, `CLOSE` | flow |
| `WAIT` | wait for A/START (START skips the rest of a window, venues_a risk 11) |
| `PAUSE n`, `SPEED n` | timing |
| `SPEAKER id` | name line + blip + portrait default |
| `PORTRAIT id` | 32×32 portrait (dialogue only) |
| `HL` / `HL_OFF` | highlight colour |
| `NUM var` | print a decimal (CX's spike counter) |
| `CHOICE n, ids…` | 2-4 options; result in A and carry; `SKIPIF n` branches on it (CX `0C`) |
| `CALL bank:addr` | run a routine (CX `09`): give an item, start a fight, set a flag |
| `IFFLAG f, skip` | branch on a LIVE FILE flag |

Text calls from code: `TELL id` (pop-up, queued, honours the ANNOUNCER config) and `TALK id` (dialogue, blocking). The
debrief and commentator tables (meta.md, story.md) are lists of string ids.

---

## 12. Sound

### 12.1 What exists [done by research]

Requests through `$DC` into the ring `$B0-$BF`, serviced at `$3E:$C8C1` (`$8003` play, `$8000` update); 102-entry big-endian
table `$34:$8A40` (36 music, 65 SFX, commands `$F0-$F7`); data in a 24 KB sound space (`$34`, `$35`, and `$36` through the
reader `$34:$803A`); the channel command set `$00-$18` decoded (`rm6/engine.md` §5.3); `songdec.py` decodes any track. Free:
449 B at the end of `$36`; ids `$1A` (empty stub) and SFX `$3D/$3E/$4D/$51` (never requested) can be recycled.

### 12.2 Driver extension [new-code] M · Must

1. **Track table v2**: ids `$00-$EF` (240; `$F0-$F7` stay commands), a relocated 240-entry pointer table and a **bank byte
   per track** (4MI's `$1E:$8E51` pattern, CX's `$18:$97B7`): bank `$00` = vanilla sound space, any other = the song's own
   bank. Ids < `$66` keep their vanilla entries.
2. **Reader**: the `$803A` reader's address test gains a fourth range: pointers `$E000-$FFFF` mean "the stream's own bank",
   mapped at `$A000` for the read (`LDA SND_BANK,x / ORA #$80 / STA $5115`) and `$35` mapped back, exactly how `$36` is
   handled today. Per-stream bank bytes live in hot RAM (`SND_BANK`, 8 entries). Which call sites read stream data, and with
   which stream index in X, is mapped in M0 with shadow6's data-read log (only 3 literal `JSR $803A` exist, at `$34:$8126`
   (header byte), `$8192`, `$81A2` (channel pointers); the channel interpreter `$83CC` reads through another path).
3. **Hardware multiply**: the 8×8 loop `$34:$8006`, the hottest loop of the driver, becomes `$5205/$5206` (4MI did the same,
   20 cycles instead of ~150-200). **The multiplier belongs to the sound driver**: game code never touches `$5205/$5206`,
   because the sound update can run inside the IRQ (§8.4) and interrupt any main-thread code.
4. **Play-time clock** in the `$C8C1` wrapper (it runs once per frame, lag frames included; 4MI ticks it in the driver),
   counted outside the LIVE images (meta.md §1.2).

### 12.3 New-song pipeline [new-code] M · Must; [new-music] per song

`tools/build/mml.py` compiles an MML dialect 1:1 onto the decoded command set:

| MML | Command | Notes |
|---|---|---|
| `c d e f g a b r`, `+ -`, length `1 2 4 8 16 32 64` | note byte: length index 7..1 (192, 96, 48, 24, 12, 6, 3 ticks), pitch 1-31 above the octave base (0 = rest) | the compiler emits octave changes when a pitch leaves the 31-semitone window |
| `.` | `02` dot | |
| `{ }` | `00` triplet toggle (lengths 2, 4, 8 … 128) | |
| `&` | `01` tie | |
| `^` | `03` octave+ toggle | |
| `F n` | `04` flags | |
| `t n` | `05` tempo (16-bit tick increment per frame) | |
| `q n` | `06` gate | |
| `v n` | `07` volume | |
| `@ n` | `08` instrument (8-byte entries at the table `$34:$8A41` points to; GP appends a relocated table) | |
| `o n` | `09` octave | |
| `K n` / `k n` | `0A` global transpose / `0B` transpose | |
| `D n` / `s n` | `0C` detune / `0D` slide | |
| `[ … \| … ]n` | `0E-11` loop 1-4 / `12-15` break 1-4 | 4 nesting levels |
| `L` | `16` jump (loop point) | |
| `!` | `17` end | |
| `w n` | `18` duty | |

Sound effects keep vanilla's format (priority byte + register stream, player `$34:$8251`) and are written as YAML register
frames. **Round trip test**: `mml.py decompile` turns all 36 vanilla music ids into MML and `compile` must give the same
bytes; it gates the compiler (M0). New stages reuse vanilla tracks until their songs exist (PLAN §6.5, kept).

### 12.4 Budget

Vanilla's 36 songs fit in about 21 KB. GP plans ≤ 1 new track per venue at Should (venues_a §10 q9), fortress and W
tracks, stingers and ~30 SFX: 16 banks (128 KB) are reserved (`$70-$77` + the `$0B-$0F` pool).

### 12.5 MMC5 pulses [new-code] M · Could

A **second driver instance** for the two MMC5 pulses: the M0 disassembly of `$34:$8000-$8A3F` (2.6 KB) becomes Ophis source
with symbolic RAM and register bases, assembled twice: once in place (4 channels, `$4000`, vanilla RAM `$0700-$07EF`) and once
in a GP bank (2 channels, `$5000-$5007`, state in WORK `$6F00`). A `COMPANION[id]` table names the 2-channel stream that
starts with a track when CONFIG "MMC5 AUDIO" is on; both instances tick in the same update call with identical tempo
commands, so they cannot drift. `$5015` is set only when the config is on (BRIEF §5.7: MMC5 audio on/off; music must stand on
the 5 core channels). Should, if time allows: 4MI's charge-shot loop on MMC5 pulse 1 so the charge never steals a music
channel (`r4mi/engine.md` §9.2).

---

## 13. Saves (implementation; the format is meta.md's) [new-code] S · Must

- **Where**: page 0 (SAVE), meta.md's map at page offsets `$0000-$1A1F` (SYS-A/B, FILE1-3 A/B, test mailbox `$1A00`).
  **Changed from meta.md's table**: the LIVE FILE and LIVE SYS images sit in **page 1 (WORK)** at the same CPU addresses meta
  gives (`$7400-$75FF`, `$7600-$79FF`), because WORK is the page mapped at `$6000` during play; page 0 offsets
  `$1400-$19FF` become reserve.
- **How**: `save_commit(block)` runs in the C-window (core bank `$3E`): it maps page 0 at `$A000` (`$5115 = $00`, shadow
  `$4B = $80`), so an NMI's sound service restores the same page through the shadow; copies the LIVE image into the older
  copy, writes the checksum and commit marker last (meta.md §1.3), and maps `$A000` back. ~10,000 cycles for a file block:
  done at meta.md's commit points (stage clear, bracket, settings), never mid-action.
- **Load**: verify both copies, take the newest valid one, fall back gracefully (meta.md §1.1: never the 4MI black-screen
  loop).
- **RESET**: maps page 0 at `$A000` briefly to read the test mailbox (§14.5), and clears WORK; it never clears page 0.
- **Passwords**: vanilla's codec `$3F:$F3D0` stays callable for meta.md's hidden PASS WORD gag.

---

## 14. Dev tooling and tests

### 14.1 Build [new-code] M · Must

`tools/build/build.py --config {release,dev}`: verify the base ROM (MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`) → expand to 1 MB
(§1.2) → assemble `src/` with Ophis → apply hooks from the registry → place segments with the allocator → write levels,
text, sound, sprites, CHR → header → `build/r6gp.nes` + `build/r6gp.bps` + `build/r6gp.map` (symbols) + a per-bank usage
report.

### 14.2 Hook registry and allocator [new-code] S · Must

`src/hooks.yaml`, one entry per patched vanilla address:

```yaml
- id: H_STAGEINIT
  site: 3E:DBDB          # vanilla numbering
  orig: "48 A8 85 51 29 07 8D 3D 06"   # must match the base ROM
  kind: cw               # cw | jsr | inline | operand | data
  target: stage_init     # symbol
  owner: tech.md §4.5
  tests: [vanilla_all_stages, sa_rows]
```

The build fails if `orig` does not match, if two hooks overlap, if a patch starts inside an instruction (checked against the
disassembly and shadow6 coverage), or if a free-space segment overflows. The coverage report lists hooks the test suite never
executed. Allocator seeds: banks `$0B-$0F`; `$3F:$FAC0-$FF1F` minus `$FFE0-$FFEF` (§1.3); `$3A:$95D4-$9FFF`; text-bank holes
`$3C:$9D16-$9FE1`, `$3D:$BA8D-$BCFF`, `$3D:$BF42-$BFFF`; `$36:$BE3F-$BFFF`; tileset slots `$2B:$9200`, `$2D:$9200`; sprite-bank
fill; after M2, `$3E:$C163-$C51D` (retired IRQ handlers); and the new banks.

### 14.3 BPS [new-code] S · Must

`tools/build/bps.py`: SourceRead / TargetRead / SourceCopy / TargetCopy with source, target and patch CRC32. The release is
the BPS against the vanilla ROM; no Capcom bytes ship (BRIEF §7.4). Tested by applying with the tool itself and with Rom
Patcher JS / Floating IPS at M10.

### 14.4 Golden movies and shadow6 [new-code] M · Must

- **Movies** are `frame:buttons` text plus checkpoints (RAM asserts, frame hashes, screenshots), run headless on FCEUmm
  (`tools/analysis/emu.py`).
- **M1 gate, vanilla equivalence**: the same input on vanilla and on the GP build in port-only configuration must give
  identical CPU RAM every frame, except the new hot bytes (`$06AF-$06FF`, `$07FA-$07FF`, `$0698`) which are masked, and
  identical frames. Suites: boot → title → each of the 16 stages for 600 frames; every IRQ state of `rm6/engine.md` §4.2
  (Blizzard ship, Plant 0E, Tomahawk 00 and 0A, Knight 03, Centaur 0A, Mr. X 2/3/4, Wily 2, Wily 4, YOU GET, the adaptor
  slide, the opening); a death, a game over, a boss kill.
- **Split calibration**: for each split state, the first differing scanline between vanilla and port frames is reported;
  `K` and the per-handler delays are tuned until it is none, on FCEUmm and once on Mesen (user gate).
- **shadow6 for MMC5**: `tools/analysis/rm6/shadow6.py` re-executes frames with MMC3 banking and the MMC3 IRQ counter;
  M1 adds PRG mode 3, RAM pages in every window, `$5203/$5204`, the multiplier, and ExRAM. Then the same tool gives coverage
  (hooks executed), the cycle profile per build (§15), and the "RAM matches the emulator" fidelity check it already has.

### 14.5 Test mailbox and warps [new-code] S · Must

- **Warp** (vanilla, `rm6/cheats.md`): write `$51`, `$0684-$0686`, set `$F0 = 2`. GP adds `CK_SECTION`. In DEV builds
  SELECT + START held 1 s = "kill and respawn here" (4MI lesson 10's one-byte respawn).
- **Mailbox** (meta.md §9.6, page 0 offset `$1A00`, 32 B): RESET reads a command (`BOOT_TO stage, section, checkpoint,
  preset, flags…`), clears it, and builds that state without menus. Tests write the mailbox into the `.sav` before boot,
  replacing savestates (vanilla states cannot load into the MMC5 build).

### 14.6 EXTRA CONFIG and the DEV build [new-code] M · Must

meta.md designs the screen (WHERE / STAGE / CP / SCREEN / ENTER STAGE, a RAM editor in the 4MI pattern: a table of RAM
pointers and help strings). Tech: code in bank `$7C`; entered only when the build has `DEV = 1` (a byte in the header-adjacent
version block) or after meta.md's unlock; any use sets `DEV_FLAGS` and meta.md's FILEFLAGS.EDITED; the DEV ring buffer at
`$7200` logs hooks, warps and saves. User gates (⛳) always include a Mesen run, to catch header and timing issues FCEUmm
forgives (§1.1, D6).

### 14.7 CI-like runs [new-code] S · Must

`tools/build/check.py`:

| Suite | Contents | When | Time |
|---|---|---|---|
| static | hook registry, allocator, header, `$FFE0-$FFEF` guard, stage-attribute vanilla rows, level checks (§6.3), sprite CHR conflicts | every build | seconds |
| unit | `levels` round trip (bank + text format), MML round trip, PPU-script selftest (168/168), text encoder, BPS round trip | every build | < 1 min |
| smoke | boot, title, file select, 3 venues × 600 frames, one save/load | every commit | ~2 min |
| full | all of §14.4 + every venue route movie that exists + lag report | milestone gates | ~15 min |

Every session ends green, committed, with `docs/STATUS.md` updated (PLAN §10 kept).

---

## 15. Lag plan

### 15.1 Baseline [done by research]

~21,000 of 29,780 CPU cycles per frame are busy in play; a lag frame needs ~29,000. OAM builder 23 % (4,800), sound driver
18 % (3,700-3,900, the multiply loop hottest), bank switching 12-13 % (2,700), terrain collision 7 %, object loop 7 %,
hit-box overlap 5-8 %, object scan 4 %, player 4 %, NMI + PPU 7 %; each extra live object costs ~1,760 cycles, so ~10 live
objects fill a frame; enemy AI itself is under 1 %. Music keeps tempo during lag (`rm6/engine.md` §8).

### 15.2 Savings, in order of cost

| Step | Where | Expected | Tier |
|---|---|---|---|
| 1 | hardware multiply in the sound driver (§12.2) | −1,000 to −1,500 cycles [guess, 4MI's factor] | Must (M2) |
| 2 | MMC5 helpers (§1.4) | −10 cycles per `$CBC0`, more per `$CB91` path | Must (M1) |
| 3 | drop the placeholder `LDA #$7E / JSR $CB91` pair at `$E204`/`$E430` if shadow6 confirms nothing reads the window (critic: nothing does) | one `$CB91` round trip per object per pass [guess: ~1,000 cycles at 10 objects] | Should (M3) |
| 4 | OAM builder: unflipped fast path, early off-screen cull, unrolled pair writes | −20-25 % of 4,800 | Should (M3) |
| 5 | unrolled VRAM copy in WORK (4MI `$7B70`: 8-9 instead of 15-16 cycles per byte) | vblank headroom for streams | Must (M2) |

Target: **+3 live objects at vanilla lag**; until measured, designers keep the vanilla budget (~10 live objects, 8 + shots,
BRIEF §6). Each step is measured with the shadow6 profiler on the same input; the full suite fails a stage whose lag frames
rise by more than 2 points.

### 15.3 VBlank budget (systems.md asks)

NTSC vblank ≈ 2,273 CPU cycles. The NMI spends ~550 on OAM DMA and setup, and runs **one** of: the VRAM buffer + column paint
chain (`$C69E/$C6D7/$C7DE`), or the CHR-set copy `$C79C`, which vanilla runs only when nothing else is pending and which moves
16/32/48/64 bytes per frame (`$C7D6` = `40 10 20 30`) at ~16 cycles per byte [code, read for this doc]. A column paint costs
~600-700 cycles.

**GP's CHR stream** (form swaps, canvas glyphs, T6 debris, CHR thirds swapped by exits) uses an unrolled copier in WORK and is
allowed on every frame:

| Frame has | Stream budget |
|---|---|
| no column paint, no VRAM buffer | **128 B** |
| a column paint | **64 B** |
| a full VRAM buffer (menus, text) | 32 B |

So systems.md's form swap (≤ 1 KB) takes 8-16 frames (its 12-frame target holds when the camera is still). A larger budget
needs a blanked top band (rendering enabled late), which is a Could.

### 15.4 Joypad 2 (systems.md asks)

Vanilla reads **both** pads every frame (`$3E:$C711`, X = 1 then 0, `AND #$03` so Famicom expansion pads count) into
`$41/$43`, but **no executed instruction reads `$41` or `$43`** outside that loop in the 139,200-frame coverage set [code +
coverage, checked for this doc]. Controller 2 is free for systems.md's pseudo L/R.

---

## 16. Milestones M0-M3, rewritten

Each milestone ends with a playable build, the test suites green, and `docs/STATUS.md` updated. **S** < 1 session, **M** 1-2,
**L** 3+. ⛳ = the user plays the build (always in Mesen as well as FCEUmm). M4 onward keep PLAN §8's order with the BRIEF §9
tiers; their engine prerequisites are all in M2-M3 below.

### 16.1 What the research already finished (PLAN's M0, done)

| PLAN M0 task | Status | Where |
|---|---|---|
| M0.3 RAM map v0 | **done** (+ critic corrections, free RAM proven over 232,722 frames) | `rm6/ram.md` |
| M0.4 disassembler, free-space confirmation | **mostly done**: py65 tools, linear disassemblies of every bank, shadow6 coverage of 139,200 frames, free ROM confirmed by execution; *missing*: reassemblable source | `rm6/engine.md` §6, `tools/analysis/rm6/shadow6.py` |
| M0.5 stage tables | **done** | `rm6/levels.md` §1 |
| M0.6 level extractor, renderer, round trip | **done** (byte-exact, JSON, edited ROM played, 16 full maps) | `tools/analysis/rm6/levels.py`, `img/maps/` |
| M0.7 object / AI / damage tables | **done** (type tables, AI header, damage routines, weakness tables) | `rm6/engine.md` §1-2 |
| M0.8 sound driver | **done** for decoding (table, command set, `songdec.py`); *missing*: the compiler | `rm6/engine.md` §5 |
| M0.9 text | **done** (168 scripts, interpreter, 11 tables, EN proof of concept) | `rm6/text.md` |
| (new) metasprite format | **done** (118/118) | `rm6/engine.md` §1.5 |
| (new) IRQ chain map, MMC5 port list, 45 stage-id readers | **done**, re-read here | §1.7, §4.3 |
| (new) warps, godmode, password codec, 87 savestates | **done** | `rm6/cheats.md`, `build/research/rm6/states/` |
| (new) MMC5 hardware probes (RAM pages, RAM in `$8000-$DFFF`, CHR-RAM size, multiplier, ExRAM mode 2, ExRAM as a nametable from a mid-frame `$5105` write, no in-frame flag) | **done** for FCEUmm | `build/design/design-tech/probe/` |

### 16.2 M0 — Workbench (what remains)

1. **M0.1 (S)** Repo scaffold (`src/`, `assets/`, `tools/build/`, `tests/`); `build.py` no-op path (vanilla in → vanilla out,
   MD5 check) and `bps.py` with a round-trip test.
2. **M0.2 (S)** Hook registry and allocator skeleton (§14.2), seeded with the verified free ranges; static checks, including
   the `$FFE0-$FFEF` guard.
3. **M0.3 (S)** `tests/run.py` on `emu.py`: movies = inputs **plus scripted RAM pokes** (so a warp at frame N runs identically
   on vanilla and on later MMC5 builds, which cannot load vanilla savestates); record the vanilla golden suite (§14.4).
4. **M0.4 (M)** Reassemblable Ophis source of the fixed banks `$3E/$3F` (16 KB) and the sound driver `$34:$8000-$8A3F`,
   byte-identical when assembled; code/data split from shadow6 coverage. Needed by the IRQ port, the raster walker and the
   second driver instance.
5. **M0.5 (S)** `.lvl` text format: decompile and rebuild all 16 stages byte-identically (§6.2).
6. **M0.6 (S)** `mml.py` decompile/compile round trip of the 36 vanilla songs (§12.3).
7. **M0.7 (S)** shadow6 censuses: every instruction that reads sound stream data (for §12.2), and a static scan of all code
   banks for `$51`/`$063D` reads to catch readers the tour did not execute; decode the player's floor-handler table (the
   type → handler dispatch near `$38:$875A`) for X-FLOOR.
8. **M0.8 (S)** `stagetab.py`: stage-attribute rows 0-15 and variant rows from the vanilla tables, with a test that they
   reproduce every vanilla value.

**Exit**: vanilla round-trips through `build.py`; unit suite green (levels, MML, PPU scripts 168/168, BPS); vanilla golden
suite recorded.

### 16.3 M1 — Big Cartridge (MMC5)

1. **M1.1 (M)** 1 MB insertion (§1.2), header (§1.1), RESET and `mmc5_init` (§1.3), vectors to `$7F` stubs, the C-window
   dispatcher, `CALL7E` and `FAR` (§1.9).
2. **M1.2 (M)** Bank helpers, sound service, NMI CHR-copy bank, sound reader (§1.4); `$E204/$E430` operands (§1.6);
   mirroring (§1.5).
3. **M1.3 (M)** IRQ literal port: the two NMI arm paths, the entry, the 15 latch and 12 disable writes, `$FF96` (§1.7);
   calibrate `K` and the per-handler delays against vanilla frames.
4. **M1.4 (M)** shadow6 MMC5 support (§14.4); golden equivalence green (RAM + frames); coverage shows every ported site
   executed.
5. **M1.5 (S)** PRG-RAM: pages, `ram_probe`, WORK clear, page 0 never cleared; save module skeleton (A/B commit, checksum,
   load fallback) on a test block; test mailbox read at RESET.
6. **M1.6 (S)** Spike ROMs (like this doc's probes, which already pass on FCEUmm): ExRAM mode 0 as a window nametable with
   mid-frame `$5105`; MMC5 IRQ line timing vs MMC3; a bottom band with a palette swap; RAM pages in `$8000/$A000`; all on
   Mesen, plus the IRQ timing and palette band on FCEUmm.
7. **M1.7 (S)** Lag baseline of the port equals vanilla's within 2 % (shadow6 profile).

**Exit**: golden equivalence green; ⛳ the user spot-checks in Mesen (header sizes, saves, every split). **Contingency**: if
ExRAM-as-nametable fails on Mesen, the window falls back to a nametable row reserved per screen by the level build (costs
layout rows in window screens); if MMC5 itself fails on the user's target, BRIEF §7.1 has to be revisited (risk 1).

### 16.4 M2 — Engine foundations

1. **M2.1 (M)** Stage-attribute table and 32 ids (§4): the 45 `$51` readers, the 11 `$063D` readers, relocated tables, the
   stage-init hook. Gate: every vanilla id still plays its golden movie identically.
2. **M2.2 (M)** WRAM-resident layouts (§5): RAM images, poke lists, map-edit API and log. Gate: vanilla stages from RAM are
   identical in the golden suite.
3. **M2.3 (M)** Object lists in WORK, list format v2, families `$F4-$FF`, init and spawn hooks, `gp_spawn`, the sprite-CHR
   hook (§7.2-7.3, §7.6); one test object per family.
4. **M2.4 (M)** Raster list and presets; all chains migrated; logic out of the IRQ (§8, §1.8); the old handler space freed.
   Gate: golden equivalence except Knight/Centaur, which pass behaviour-equivalence.
5. **M2.5 (L)** Text engine v1 (§11): window band on ExRAM, canvas and VWF, JP font, dialogue with freeze and
   borrow/restore, pop-ups with the per-screen canvas table, choices, the PPU-script language hook, `text.py`. Samples in JP
   and EN.
6. **M2.6 (M)** Sound (§12.2-12.3): track table v2, bank bytes, reader range, hardware multiply, play-time clock, `mml.py`
   compile; the first new song plays in a vanilla stage.
7. **M2.7 (M)** Level pipeline (§6): `.lvl` build in `build.py`, all checks of §6.3, the canvas table, maps; one test
   section authored in text and played.
8. **M2.8 (S)** DEV build: EXTRA CONFIG (meta.md's UI), warps, respawn-here, the DEV ring buffer (§14.5-14.6).
9. **M2.9 (S)** Lag steps 1 and 5; the CHR stream with the budgets of §15.3 (systems.md's form swap is its first user).
10. **M2.10 (S)** For systems.md: death-hook audit, latch source, frozen tick, LFSR (§7.7-7.8).

**Exit**: vanilla content runs on the new engine (attribute table, RAM layouts, raster list) and passes the suite; a
dialogue and a pop-up play inside a vanilla stage in JP and EN; a new song plays. ⛳

### 16.5 M3 — Systems and shared mechanics (engine side)

1. **M3.1 (M)** Saves, file select and config plumbing on meta.md's format (§13); difficulty bytes read by `IFHARD` and the
   poke lists.
2. **M3.2 (M)** systems.md's hook set (its §15.1): SELECT quick swap with the form CHR stream, weapon alt/synergy dispatch,
   damage and i-frame tables, adaptor by win count (`$38:$931D`, `$3B:$BA3F`), WEAK! pop, commentator events.
3. **M3.3 (M)** T3 switch → target (family `$F5`): doors, keys, gates, lifts through exits, timed toggles (VA-TIMED).
4. **M3.4 (M)** T6 (§10) with X-BONK; a test climb with break and refill.
5. **M3.5 (M)** T1-lite (§9.1): wave director and band rides; a test sortie.
6. **M3.6 (S)** Player extensions (§7.9): GP player states (T5 grab, X-EXWP), X-WRAP, exit type 7 (X-UPEXIT, Should), pad
   history (T7, Should).
7. **M3.7 (S)** Scorecard counters and results hooks (meta.md, systems.md); the announcer queue feeding pop-ups.
8. **M3.8 (S)** Lag steps 3-4; measure how many objects were gained and publish the new budget.

**Exit**: the full loop (score, bolts, chips, saves, commentators) runs on vanilla stages; T1-lite, T3 and T6 demo rooms pass
their movies. ⛳ Then M4 (vertical slice) can start on real venue data.

---

## Lessons applied

- **CX 8** (engine): a bank byte beside every pointer table (tracks, lists, sections, families); raster effects behind one
  stub with their parameters in dedicated RAM (§8); interrupt-safe banking through shadows (§1.4, §1.9); old entry points
  kept by rewriting the helpers in place (§1.4). **CX 9**: test harness from day one (mailbox, warps, dialogue injection
  through `TALK id`, damage sweeps via EXTRA CONFIG). CX's text lessons: an opcode set with `CALL` and `SKIPIF`, scripts
  started from object data, a VWF for English with a highlight plane, text kept out of code banks (§11).
- **4MI 8**: level data in RAM, connectivity as data, HARD as poke lists (§5). **4MI 11**: a generic double-buffered raster
  list (§8). **4MI 12**: an accurate target and a correct NES 2.0 PRG-RAM size, plus a boot probe (§1.1, §2.3). **4MI 13**:
  resolve placements statically (§6.3, §7.6). 4MI engine lessons: PPUMASK as an effects register (§8.1), spare attribute
  bits instead of new formats (T6's bit 2), shared hardware guarded in NMI (the multiplier belongs to the sound driver),
  an unrolled VBlank copy (§15).
- **RM6 1**: ids past 15 only after the 45 readers are rewritten, and the packed tables relocated (§4). **RM6 2**: the block
  table as the art budget (T6 variants are reported in block ids; venue tilesets get their own alternate set). **RM6 3**:
  the 89 free bytes for hot hooks only (§3.1). **RM6 4**: the corrected porting checklist, completed here (§1.4-1.7).
  **RM6 5**: new enemies as families with the 6-byte header and a CHR-conflict check (§7). **RM6 6**: per-position
  destruction (§10). **RM6 7**: adaptor acquisition hooks listed (§16.5). **RM6 8**: quirks kept (oil ignition's repaint
  reused, the `$FFE0` check respected, C.FLRSH and TO BE CONTINUED untouched by the text hook).

## Risks

1. **Hardware and flash-cart support** for MMC5 + 8 KB CHR-RAM + 32 KB PRG-RAM is unverified; 4MI's MMC5 build is the
   existence proof only for emulators. Mitigation: the boot probe's clear message; Mesen at every gate; ask the user which
   cart matters (open question 5).
2. **FCEUmm forgives too much**: it always gives 64 KB of PRG-RAM and wraps CHR-RAM at 8 KB [seen], and its MMC5 timing
   may differ from Mesen's. Bugs that only Mesen shows reach the user late. Mitigation: Mesen in every ⛳, and a headless
   Mesen in CI if one can be installed (open question 4).
3. **IRQ calibration** may not hit h-blank identically on both emulators; bands may shimmer by a line. Mitigation: per-band
   timing tests on both; prefer PPUMASK/PPUCTRL bands (less sensitive than `$2006`) where a design allows.
4. **ExRAM writes count only while rendering**, and FCEUmm lacks the in-frame flag. Mitigation: all ExRAM writes go through
   a queue flushed inside a line-8 IRQ band (§3.3); the window cannot change on rendering-off screens, so full-screen text
   stays on the PPU-script engine.
5. **Canvas CHR**: dense screens have no free BG ids (Plant), so pop-ups wait; a bug in the dialogue's borrow/restore would
   corrupt visible tiles. Mitigation: every dialogue screen gets a movie with a frame hash after the window closes.
6. **Moving the logic out of IRQs** changes Knight's and Centaur's timing by part of a frame: exact golden equality is lost
   there (behaviour tests instead).
7. **WRAM layouts**: a stray write corrupts the current stage. Mitigation: DEV builds compare the LAYOUT page with the ROM
   image plus the map-edit log at every screen exit.
8. **T6 block-id cost** on full tilesets; fallback: the bitmap variant (§10).
9. **Unexecuted `$51` readers** may exist outside the 139,200-frame tour; M0.7's static scan closes the gap.
10. **Sound driver reassembly** for the second instance is delicate; that is why MMC5 audio stays Could.
11. **Text engine size (L)**: Knight's venue depends on it (venues_a risk 5). It starts in M2, before any venue.
12. **Cartridge space**: 4MI filled 1 MB to 97 %; GP plans ~45 % of the new space for code and data and reports usage per
    bank on every build.
13. **Vanilla savestates cannot load into MMC5 builds**: all tests must boot and warp (mailbox, scripted pokes); recording
    them is an M0 task, not an afterthought.

## Open questions

1. **fortress.md**: does it need engine ids beyond `$16-$1D` and `$1F` (separate arenas for the Bass duels, multi-stage
   wings)? Which legacy ids `$09-$0F` may be reclaimed?
2. **meta.md**: accept the LIVE FILE / LIVE SYS images in page 1 at meta's CPU addresses (§13)?
3. **Pop-up position**: top band by default (keeps floors and pits visible) or bottom (venues_a/b assumed the bottom)? A
   per-stage flag exists either way.
4. Can a headless Mesen run in this environment for CI, or is Mesen a user-gate tool only?
5. Which hardware target matters (Everdrive N8 Pro, PowerPak, none)? It decides how far to trust MMC5 CHR-RAM and 32 KB
   PRG-RAM.
6. **art_audio.md**: tiles per form for the quick swap; portrait count (16 canvas tiles each, dialogue only).
7. Does any venue need T1-full (terrain moving with a forced camera)? Today none does.
8. **story.md**: kanji in JP dialogue (cheap with the canvas: about 1.6 KB of PRG for 200 glyphs), or kana only as vanilla?
9. Do any stages need more than 32 screens (H wings, W stages)? That decides whether sections move from Should to Must.
10. Should the legacy ids 8-15 keep vanilla fortress rules (CONTINUE-only game over, no weapon get) when the fight table
    loads them?

## Cross-doc dependencies

| Doc | Must agree with |
|---|---|
| `meta.md` | PRG-RAM page 0 map unchanged, LIVE images moved to page 1 at the same CPU addresses (§13); mailbox at page offset `$1A00`; EXTRA CONFIG UI on tech's warp, DEV flag and ring buffer (§14.5-14.6); `SA.META` = its meta index (§4.2); its fight table points at engine ids (legacy `$08-$0F`, §4.2); ENGRISH as an override table (§11.5); difficulty bytes read by `IFHARD` and poke lists (§5.5) |
| `systems.md` | its hot bytes at `$06BD-$06C8`, per-slot arrays at `$6000+` (§3.1, §3.4); hook sites in the registry; VBlank stream budget 128 / 64 / 32 B (§15.3); controller 2 is free (§15.4); frozen tick, latch source, LFSR, death-hook audit (§7.7-7.8); the multiplier is not for game code (§12.2); stage fields `FORT_COL`, `SCORE_ID`, `PAR`, `NO_TAG`, `KEEPWE` (§4.4) |
| `venues_a.md` | T1-lite accepted (§9.1); T4 through `RL_BANDS` with ≤ 6 bands plus the window band (§8.3); T2 (§11); T3, T5 and VA-* objects built on families `$F4/$F5` and GP player states (§7); the Knight ceiling out of the IRQ with parameters (§1.8); two tileset slots per ROM bank, each with its own alternate set (§5.2) |
| `venues_b.md` | T6 is a layout rewrite with variant blocks, not a bitmap (§10; the bitmap is the fallback); X-BONK is a ceiling-probe callback; X-GPOBJ = families (§7.2); the ship, tide and ceiling become `EFFECTS` bits with `EFX_PARAM` (tide dwell) (§4.4); X-UPEXIT = exit type 7 (§7.9); X-FLOOR = new collision groups via `GRP_ROW` once M0.7 decodes the floor handlers; the ignition hook on `$3E:$DDFC` goes in the registry |
| `fortress.md` | ids `$16-$1D`, `$1F` (§4.2); BG bosses on `RL_FLOOR` (§8.3); legacy ids for refights; sections for wings over 32 screens (§5.4) |
| `story.md` | the text control codes and limits: pop-up 2 lines × 16 tiles (~22 EN characters with the VWF, 16 JP), dialogue 3 lines × 26 columns with a 32×32 portrait (§11); speaker ids with blips; kana (+ kanji if adopted) |
| `art_audio.md` | 8 KB CHR-RAM and no banking (D6); sprite PNG + JSON input (§7.5); 1bpp 8-px fonts; portraits 32×32; the MML dialect (§12.3); 16 music banks; MMC5 companion streams (§12.5) |
