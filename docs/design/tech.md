# Rockman 6 GP: technical architecture (design-tech, round 3)

This doc replaces `docs/PLAN.md` §5-7. Its milestone section (§16) follows [`RULINGS.md`](RULINGS.md) §6, which replaces
PLAN §8 and round 1's tech §16 ordering. **[`RULINGS.md`](RULINGS.md) is binding and overrides everything here**, then
[`BRIEF.md`](BRIEF.md); the research in `docs/research/` wins on facts.

**Tiers** follow RULINGS §0: **Must** = v1.0 (the tight Must, about 450 sessions in all docs, R8.1), **Should** = v1.1+ (re-added
in the cut-line order of R0.3), **Could**, **Won't (v1)**. A Must depends only on Musts (R0.4). Tags: **[engine-ok]**
vanilla does it with data only, **[new-code]**, **[new-art]**, **[new-music]**; sizes **S / M / L**; evidence **[code]**,
**[seen]**, **[guess]**. Session counts come from the ledger (`tools/plan/tight.py`, `tools/plan/tally.py`).

**What this doc owns** (the single sources of truth, RULINGS and consistency critic): stage ids (§4.2), all memory (CPU
RAM, ExRAM, PRG-RAM pages, the WORK ledger, §3), the raster list (§8), CHR/ExRAM limits (§3.3, §7.6, §15.3), the bank
ledger (§1.2), the tileset-slot table (§5.3), the unified engines (map edits, HUD widgets, player states, poke lists;
§5, §7), the object-slot plan (§7.12) and the fight loader (§4.6). It **cites** the other owners: `systems.md` for
combat, economy and chip numbers; `meta.md` for save bytes, the bracket, events, the debrief and RULESET;
`venues_a.md`, `venues_b.md` and `fortress.md` for staging and mechanics; `story.md` for every word and the ending;
`art_audio.md` for tile, byte and track budgets.

Addresses are `bank:CPU` in **vanilla numbering** unless marked *new*. After the MMC5 move, vanilla fixed banks `$3E/$3F`
become `$7E/$7F` (§1.2); a vanilla address `$3E:$C8C1` is then `$7E:$C8C1`, same CPU address.

Scratch and probes: `build/design/design-tech/` (round 1: `probe/` = MMC5 probes on the bundled FCEUmm core,
`sprtiles.py`, `irq_dis.txt`, `sites51.txt`) and `build/revise/tech/` (round 2: `form9b.py` = the `$9B` census of R1.12,
`dmgstep.py` = the damage-step census behind R2.2, `slots47.py` = vanilla users of object slots 4-7 for R1.11).

Contents:
v1.0 scope -
0. Decisions at a glance -
1. Cartridge, the MMC5 migration and the bank ledger -
2. PRG-RAM -
3. Memory map (CPU RAM, ExRAM, the WORK ledger) -
4. Stage ids, the stage-attribute record, stage changes and the fight loader -
5. WRAM-resident layouts, the tileset-slot table, poke lists and the map-edit service -
6. Level and art pipelines -
7. Object / AI framework (families, slot plan, frozen handlers, player states, HUD widgets) -
8. The generic raster list -
9. Autoscroll (T1) -
10. Per-position destructible tiles (T6) -
11. Text engine -
12. Sound -
13. Saves -
14. Dev tooling and tests -
15. Lag plan -
16. Milestones M0-M9 -
Lessons applied - Risks - Open questions - Cross-doc dependencies - Changes in round 2 - Changes in round 3.

---

## v1.0 scope

v1.0 is RULINGS R0.2's tight Must (about 450 sessions in all docs, R8.1). Tech's share is **102.5 sessions**
(`tools/plan/tight.py`, area `tech`, holds 102). Round 1's ledger had 98; the round-2 changes are: +2.5 the fight
loader, moved here from `meta.md` (R1.7); +2 the OAM-builder lag steps, now Must because the slot cap is re-measured at
M3 (R1.8); +1 the `$9B` audit and the 4th form row (R1.12); −1.5 F-SIZES, now Should (R3.6). Round 3 adds +0.5 for the
ending's engine pieces (row 44) and moves 1 session of the attach state from M5 to M3 (rows 31a/31b, R8.2). Everything
below is **Must** and depends only on Must items (R0.4).

| # | Item (section) | Milestone | Sessions |
|---|---|---|---|
| 1 | MMC5 go/no-go spike on Mesen, plus the user's cart if one exists (§1.10) | M0 | 1.5 |
| 2 | Workbench: scaffold, `build.py`, BPS, hook registry, allocator, bank and WORK ledgers printed per build, test runner, vanilla golden suite (§14) | M0 | 4 |
| 3 | Reassemblable Ophis source of `$3E/$3F` and the sound driver (§14.2) | M0 | 3 |
| 4 | Round trips and censuses: `.lvl`, MML, `$51`/`$063D`/`$9B` static scans, sound-stream readers, floor handlers, `stagetab.py` (§4, §6, §12) | M0 | 4 |
| 5 | MMC5 insertion, header, RESET, interrupt stubs, re-entrant C-window, `CALL7E`, `FAR` (§1.2-1.3, §1.9) | M1 | 2.5 |
| 6 | Bank helpers returning vanilla A, sound service and reader, NMI CHR bank, `$E204/$E430`, mirroring (§1.4-1.6) | M1 | 2 |
| 7 | IRQ literal port of the 27 chains, calibrated (§1.7) | M1 | 3.5 |
| 8 | shadow6 for MMC5, golden equivalence (§14.4) | M1 | 2.5 |
| 9 | PRG-RAM pages, `ram_probe`, save skeleton, mailbox read, Mesen re-check, lag baseline (§2, §13, §14.5) | M1 | 2.5 |
| 10 | Stage record v0: the 48-byte table, `SA_CUR`, the init hook, `$CE44` on every id change; readers untouched (§4.4-4.5) | M2 | 1 |
| 11 | WRAM-resident layouts, poke lists (CASUAL/NORMAL/HARD/1993 tiers), the map-edit service (§5) | M2 | 3 |
| 12 | Families and sub-ids, object lists v2 in WORK, spawn hooks, the slot plan (§7.2-7.3, §7.12) | M2 | 3 |
| 13 | CHR set table v2 and stage-local ids (§7.6) | M2 | 2 |
| 14 | Minimal art pipeline: `chr.py`, `sprites.py`, `palettes.py`, `artcheck.py` (§6.7) | M2 | 5 |
| 15 | Level pipeline, build checks, the free-id scan for the glyph strip (§6) | M2 | 3 |
| 16 | Raster list (24 bands), presets, IRQ logic out of the interrupt, band compositor (§8, §1.8) | M2 | 4 |
| 17 | Text v1a: ExRAM window, glyph cache, compiler with dictionary compression, pop-up coroutine, debrief and help windows, language hook (§11) | M2 | 3.5 |
| 18 | Sound: track table v2, bank bytes, reader range, hardware multiply, play clock, `mml.py`, the D9 channel mute mask (§12) | M2 | 4 |
| 19 | DEV build: EXTRA CONFIG engine, warps, DEV combos, ring buffer (§14.6) | M2 | 1.5 |
| 20 | CHR stream: unrolled copier in ROM, WORK staging buffer, queue; lag steps 1 and 5 (§15.3) | M2 | 1.5 |
| 21 | LATCHSRC, the frozen tick and frozen handlers, LFSR, death-hook audit (§7.7-7.8) | M3 | 1.5 |
| 22 | T6 variant blocks and X-BONK on the map-edit service (§10) | M3 | 2.5 |
| 23 | GP player-state takeover and X-WRAP (§7.9) | M3 | 1 |
| 24 | HUD widget module (§7.13) | M3 | 2 |
| 25 | Commentator event bus (§11.7) | M3 | 2.5 |
| 26 | Lag steps 3-4 (OAM builder) and the re-measured slot cap (§15.2) | M3 | 2 |
| 31a | The attach state's core (one record: parent slot, offsets, input, release and weapon rules), with Blizzard's condor as its first user (§7.9; R8.2) | M3 | 1 |
| 27 | Stage-attribute table proper: the 45 `$51` and 11 `$063D` readers, relocated tables, ids `$10-$21` (§4.3) | M5 | 3 |
| 28 | T3 switch → target (§7.10) | M5 | 2.5 |
| 29 | T7 input mirror (pad history) (§7.9) | M5 | 2 |
| 30 | T8 multi-part bosses (§7.11) | M5 | 2 |
| 31b | The attach state's M5 users on the M3 core: the vines and T5's pendulum, Plant's balloon (§7.9; R8.2). The claw and the arrow ride are data on the core at M7/M8 | M5 | 1 |
| 32 | X-EXWP set-piece weapon (Yamato's pogo) (§7.9) | M5 | 1.5 |
| 33 | Boss-panel extension (fight-id records, 10th field, re-type) (§11.2) | M5 | 1.5 |
| 34 | Pattern-table split for menus (§8.3) | M5 | 1 |
| 35 | Text v1b: dialogue with world freeze, ROM restore of borrowed tiles, choices, NPC menus (§11) | M6 | 2.5 |
| 36 | T1-lite: wave director and band rides (§9.1) | M6 | 3 |
| 37 | The free-flight vehicle state (SKY ACE) (§7.9) | M6 | 1.5 |
| 38 | Palette-flash and lighting service (Riot blackout, REDUCED fades, R3.5) (§8.5) | M6 | 1.5 |
| 39 | `bgboss.py` (§6.7) | M7 | 2 |
| 40 | The fight loader, FIGHT_CTX, the return-to snapshot (§4.6) | M7 | 2.5 |
| 41 | F-PIECES on the map-edit service (H1's Yellow Devil) (§5.6) | M7 | 2.5 |
| 42 | `$9B` tables relocated with a 4th (SUPER) row (§7.9) | M7 | 1 |
| 43 | The 8-band floor (W3) (§8.3) | M8 | 1.5 |
| 44 | The ending's engine pieces: the CAPCOM TIMES' GP pages through the new engine (§11.2) and the credits' room table and `CREDITS` bit (§4.6) | M8 | 0.5 |
| | **Tech Must total** | M0-M8 | **102.5** |

Per milestone: M0 12.5, M1 13, M2 31.5, M3 12.5, M4 0 (support only), M5 14.5, M6 8.5, M7 8, M8 2. Release work in M9
(BPS release, emulator and hardware matrix) is in the ledger's `overhead` area, not here.

**Not in v1.0** (designs kept below as v1.1+ material, each marked in place):

| Tier | Items |
|---|---|
| **Should (v1.1+)** | layout sections over 32 screens and the slot-B section switch (§5.4); F-SIZES (§8.3); the 16-band floor (§8.3); the Break Man slot-0 character variant (§7.9, ships with the tag partner); 32×32 portraits (§11.4); per-stage HARD poke lists (content; the format is Must, §5.5) |
| **Could** | ExGrafix in W1's locked 16-bit rooms and the METALL 16 arena (§3.3); F-ERA; X-UPEXIT (exit type 7); X-FLOOR; the MMC5 pulse driver (§12.5); `fms2mml.py`; the OAM behind-BG priority override (W1 POCKET); a top-blank band for 256 B/frame streams (§15.3) |
| **Won't (v1)** | T1-full forced scroll (§9.2); the T6 bitmap (§10); F-GRID; LZ-compressed layouts; vertical autoscroll; kanji; DPCM (if ever, in `$7F`); 32 KB CHR-RAM; the VWF |

---

## 0. Decisions at a glance

| # | Decision | Why (evidence, ruling) | Tag · tier |
|---|---|---|---|
| D1 | **MMC5, 1 MB PRG by insertion**: vanilla banks `$00-$3D` stay in place, new banks `$3E-$7D`, vanilla fixed `$3E/$3F` move to `$7E/$7F`. A **go/no-go spike on Mesen runs before M1** (§1.10) | BRIEF §7.1; CX and 4MI both expanded by insertion; every `LDY #bank / JSR $CBC0` with bank < `$3E` stays valid (`rm6/engine.md` §9); R1.1 | [new-code] M · Must |
| D2 | **PRG mode 3** (four 8 KB windows), `$C000` = `$7E`, `$E000` = `$7F`, exactly MMC3 mode 0's shape | the helpers `$CB91/$CBC0/$CBDA/$CBE9` keep their contract, **including the A value they return** (R1.14) | [new-code] S · Must |
| D3 | **Bank id convention**: a bank byte `$00-$7F` is a ROM bank, `$80-$83` is PRG-RAM page 0-3. The ported helpers do `EOR #$80 / STA $5114` | every vanilla table that holds a bank number (`$6E`, `$6F`, `$0441`, the stage table) can point at RAM with no code change [seen: `probe/`]; consistency-41 (4 pages, not 8) | [new-code] S · Must |
| D4 | **The C-window**: GP service code runs in the `$C000` window, entered through a `$7F` stub that **pushes the previous `$5116` and the registers** (re-entrant). The NMI and IRQ stubs **save and restore the interrupted `$C000` bank**. C-window code never yields and is **never called from interrupt code** | MMC5 can switch `$C000`; vanilla code banks `$38`, `$3E` have 0 bytes of fill; feasibility-10, R1.4 | [new-code] M · Must |
| D5 | **32 KB battery PRG-RAM** (EWROM shape), 4 pages: 0 SAVE, 1 WORK (always at `$6000`), 2 LAYOUT, 3 TILES. It stays 32 KB | §2; R1.6 | [new-code] S · Must |
| D6 | **8 KB CHR-RAM, no CHR banking beyond 8 KB, no extra 4 KB CHR page** | FCEUmm wraps MMC5 CHR-RAM at 8 KB [seen: `probe/chr_*.nes`]; the page bits reach only the two pattern tables (feasibility-1 probe); R1.3 | constraint |
| D7 | **ExRAM in mode 0 for the whole game**: a spare nametable for text windows, switched in mid-frame with `$5105`. ExGrafix (mode 1) exists only as a Could, in text-free locked rooms (W1's 16-bit section, the METALL 16 arena), filled in mode 2 while blanked | works on FCEUmm from exactly the IRQ line [seen: `probe/exnt2.nes`]; R1.3 (blocker feasibility-1 / consistency-1) | [new-code] S · Must (ExGrafix Could) |
| D8 | **Stage ids 0-31** by the binding map of §4.2, with a **48-byte stage-attribute record** per id. The record and its init hook come first (M2, read by GP code only, the slice's included: no stage-`$00` stop-gaps); the 45 `$51` readers are rewritten at M5, before the first id ≥ `$10` | BRIEF §7.2; R1.2 (feasibility-2, consistency-2, scope-12); R1.14 (48 bytes); R8.2 | [new-code] M · Must |
| D9 | **WRAM-resident layouts in the "RAM image" form**: layout and tileset copied raw into RAM pages laid out like ROM banks; vanilla painters and collision read them unchanged through D3 (§5) | gives map edits, T6, CASUAL/HARD poke lists, per-slot alternate sets | [new-code] M · Must (sections Should) |
| D10 | **IRQ: literal port first, raster list second.** M1 ports the 27 chains one for one. M2 replaces them with a **double-buffered raster list of 24 bands per buffer** and moves the 4 logic-in-IRQ handlers into the NMI (in `$7E`, never through the C-window) | BRIEF §7.1, 4MI lesson 11; R1.9 | [new-code] M + M · Must |
| D11 | **Text: a fixed-cell glyph cache** in an ExRAM window. EN in ALL CAPS, JP kana, no VWF, no kanji. Pop-up 2 × 28 cells with ≤ 24 glyph ids; dialogue, debrief and help pages 4 × 28. Borrowed BG tiles are restored from ROM. TALK, CHOICE and every frame-waiting UI are yielding coroutines. Dictionary compression is Must. Split into v1a (before the slice) and v1b (before Knight) | R1.4 (feasibility-10/11, consistency-3); the BG table is full on most stages (`rm6/SUMMARY.md` §2) | [new-code] L · Must |
| D12 | **Sound: vanilla driver kept**, plus a per-track bank table, an MML pipeline proven by a byte-exact round trip, hardware multiply and the **D9 channel mute mask**. A second driver instance on the MMC5 pulses is Could | `rm6/engine.md` §5, 4MI §9; R1.3, R5.2 | [new-code] M · Must; MMC5 pulses Could |
| D13 | **Dev tooling from day one**: hook registry, BPS, EXTRA CONFIG, warps, test mailbox, the fight loader as a test entry, golden movies on shadow6 | BRIEF §7.3, CX lesson 9, 4MI lesson 10 | [new-code] M · Must |
| D14 | **Assembler: Ophis 2.3** from `.pylib` | it assembled the MMC5 probe ROMs [seen] | tool |
| D15 | **A bank ledger owned by tech** (§1.2), printed on every build: 128 banks = 1 MB, every bank with a role and an owner. Music 5 banks, text 9, layouts 8 (2 of them vanilla `$32/$33`, overwritten by the venue layouts), tilesets 13 | R1.5 (feasibility-13) | [new-code] S · Must |
| D16 | **A WORK ledger** (§3.4): every byte of page 1 has an owner. The unrolled copier lives in ROM; only a 256 B staging buffer lives in WORK; the map-edit log is 256 B | R1.6 (feasibility-12) | [new-code] S · Must |
| D17 | **Stage changes**: `$CE44` clears `$0340`/`$0650` whenever the stage id changes; a 64-byte return-to snapshot serves hubs and lobbies; a **FIGHT_CTX** byte reroutes boss death, clear and respawn. **The fight loader is Must and tech's** (§4.6) | R1.7 (feasibility-3, scope-6/12; measured stale bits) | [new-code] M · Must |
| D18 | **Lag rule**: count every occupied object slot (player, screen script, directors, shots, effects, the text runner); **cap 9** until M3 re-measures after the OAM-builder work (§15) | R1.8 (feasibility-4) | rule · Must |
| D19 | **One engine of each, owned by tech**: one map-edit service, one HUD widget module, one attach state, one free-flight vehicle state, one poke-list format, one tileset-slot table | R1.10 (scope-10, 16, 17, 25; consistency-9) | [new-code] · Must |
| D20 | **Object-slot plan**: shots in 1-3, one GP utility each in 4-7 (Beat's rescue reuses 4), enemies `8-$14`, the text runner in `$15`, the screen script in `$16` (§7.12) | R1.11 (feasibility-9); vanilla users of 4-7 measured (`slots47.py`) | [new-code] S · Must |
| D21 | **Frozen objects keep taking damage** through per-(type, or family + sub-id) frozen handlers; everything else is NOFREEZE; bosses get a boss-side frozen state (§7.7) | R2.2 (feasibility-6); `dmgstep.py` census | [new-code] S · Must |
| D22 | **Break Man is a slot-0 character variant**, not an object family; family `$FC` is dropped. The NPC Break Man (Must) is an ordinary NPC object. **The `$9B` readers are audited** before SUPER becomes form 3 (§7.9) | R1.12 (feasibility-14); `form9b.py` census | [new-code] · NPC and audit Must, variant Should |

---

## 1. Cartridge, the MMC5 migration and the bank ledger

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
(`$90`, `$A0`, `$70`, `$09`, `$00`) [seen: `probe/probe_*.nes`]. Mesen sizes PRG-RAM from the NES 2.0 header (the
go/no-go spike confirms it before M1, §1.10), so the header is checked on Mesen at every user gate (§14.6), and the boot
code probes the RAM size itself (§2.3).

### 1.2 The insertion layout and the bank ledger [new-code] M · Must

| File offset | Banks (new) | Contents |
|---|---|---|
| `0x000000-0x00000F` | | header (§1.1) |
| `0x000010-0x07C00F` | `$00-$3D` | vanilla banks, **in place**, patched only through the hook registry (§14.2) |
| `0x07C010-0x0FC00F` | `$3E-$7D` | **512 KB new space** |
| `0x0FC010-0x0FE00F` | `$7E` | vanilla `$3E` (CPU `$C000`), patched |
| `0x0FE010-0x10000F` | `$7F` | vanilla `$3F` (CPU `$E000`), patched; reset vector here (MMC5 powers on with `$5117` = last bank [seen: the probe ROMs booted from bank `$7F`]) |

**The bank ledger** (R1.5, feasibility-13). Tech owns it. `build.py` prints it on every build with the bytes used per
bank, and the allocator refuses a segment whose bank role does not match. The whole cartridge, 128 banks:

| Banks | Count | KB | Contents | Owner |
|---|---|---|---|---|
| `$00-$0A` | 11 | 88 | vanilla, kept in place | — |
| `$0B-$0F` | 5 | 40 | vanilla free banks (never executed or read in 139,200 traced frames, `rm6/engine.md` §6) → **text banks T5-T9** | tech (format), `story.md` (data) |
| `$10-$31` | 34 | 272 | vanilla, kept in place: legacy fortress layouts `$26/$27` (ids `$08-$0F`), tileset banks `$2A-$2F`, AI and sprite banks | — |
| `$32-$33` | 2 | 16 | vanilla venue layouts (stages 0-3 in `$32`, 4-7 in `$33`, one 2 KB page each [code: `$DF25`, `$DF45`]) → **GP venue layouts, each venue at its vanilla bank and page** | tech (format), venue docs (data) |
| `$34-$3D` | 10 | 80 | vanilla, kept: sound `$34-$36` (the 449-B tail of `$36` holds **SFX only**, R1.14), code `$38-$3D` | — |
| `$3E-$7D` | 64 | 512 | **new space**, next table | tech |
| `$7E-$7F` | 2 | 16 | vanilla fixed banks `$3E/$3F`, patched | tech |
| **Total** | **128** | **1,024** | | |

The new space, by role. "v1.0" is the estimated fill of the v1.0 build; "full" is the whole design with every Should and
Could:

| Banks | # | Role | Mapped | v1.0 | Full | Content owner |
|---|---|---|---|---|---|---|
| `$3E-$3F` | 2 | GP core services: stage loader, RAM images, poke lists, map-edit service, fight loader, save module, frozen handlers, HUD widgets, CW/FAR targets | C-window | ≈ 10 KB | ≈ 14 KB | tech |
| `$40-$41` | 2 | `systems.md` code: SELECT and form swap, weapon dispatch, GP_BOSSHIT, scorecard, chips, shop | C-window or `$8000` | ≈ 10 KB | ≈ 15 KB | systems |
| `$42-$43` | 2 | `meta.md` code: title, file select, bracket, results, debrief, pit stop, CONFIG, EXTRA CONFIG UI (thread code) | `$8000/$A000` | ≈ 11 KB | ≈ 16 KB | meta |
| `$44-$45` | 2 | text services: page decoder, dictionary, glyph renderer, strip allocator, commentator bus | C-window | ≈ 5 KB | ≈ 6 KB | tech |
| `$46` | 1 | NMI bank: the unrolled CHR/VRAM copier (1.5 KB, §15.3), raster preset tables | `$8000` during the NMI | ≈ 3 KB | ≈ 4 KB | tech |
| `$47` | 1 | DEV: EXTRA CONFIG engine, test hooks (present in every build, entered only as §14.6 says) | C-window | ≈ 4 KB | ≈ 6 KB | tech |
| `$48-$4D` | 6 | new object AIs, 3 pairs (`$48/$49`, `$4A/$4B`, `$4C/$4D`), incl. the text runner and the NPC Break Man | `$8000/$A000` | ≈ 30 KB (≈ 100 kinds) | ≈ 46 KB (≈ 155 kinds) | stage and systems docs (code), tech (homes) |
| `$4E-$53` | 6 | sprite bank pairs (frames, layouts, animations; vanilla format, §6.7) | `$8000/$A000` | 2 pairs | 2 pairs (532 frames, ≤ 512 per pair); the 3rd pair spare | art_audio |
| `$54-$61` | 14 | CHR source: new tiles, BG-boss art, face icons | read by the CHR loader | ≈ 9 banks (70.9 KB, 4,535 tiles; R8.7) | ≈ 15.5 banks (124.2 KB): 14 here plus the vanilla gap reserve | art_audio |
| `$62-$6E` | 13 | tileset slots: 2 slots + 2 alternate sets + T6 tables per bank (§5.3) | copied to RAM | 7 banks (14 slots) | 13 banks (26 slots) | tech (placement), art_audio (content) |
| `$6F-$74` | 6 | layouts of the non-venue stages (2 KB sections), the YOU GET room copy, object lists, screen-script overflow, poke lists, stage-local CHR set tables | copied to RAM | ≈ 3 banks | 6 banks | tech (format), stage docs (data) |
| `$75-$79` | 5 | music and SFX: track table v2, instruments, new songs, companion streams (Could) | `$A000` | 1 bank | `$75-$78` (≈ 29.6 KB, `art_audio.md` §12.8); `$79` spare | art_audio |
| `$7A-$7D` | 4 | text banks T1-T4: strings, dictionary, the 1-bpp glyph set | `$A000` | 4 banks (≈ 30 KB) | 9 banks with `$0B-$0F` (72 KB) | story (data), tech (format) |
| | **64** | | | **≈ 42 banks** | **64** | |

Reading the ledger:

- **Music 5, text 9, layouts 8** (`$6F-$74` plus the recycled `$32/$33`), **tilesets 13** (2 slots per bank for the 26
  slots of §5.3), CHR 14. That is R1.5's rebalance.
- **CHR, after art's re-measure** (`art_audio.md` §13.1; R8.7): v1.0 needs **about 9 of the 14 CHR banks** and **2
  sprite pairs**. The full design needs ≈ 15.5 banks; its overflow (≈ 780 tiles) goes into the **vanilla gap reserve**
  (`art_audio.md` §1.3: 1,126 blank tiles outside Capcom's sets, so filling them overwrites no art, BRIEF §7.4), a
  full-design allocator seed for CHR only, never used by v1.0. So **no CHR bank can leave this row**.
- **v1.0 uses about 42 of the 64 new banks.** The full design fills all 64 plus `$0B-$0F` except two spares: music's
  `$79` (the full design uses ≈ 3.6 of the 5 music banks) and the third sprite pair. Nothing else is left for growth, as
  4MI's 97 % fill warns. A v1.1+ item that needs a bank must displace another; the ledger is re-totalled at every ⛳
  gate (R0.1). **A tenth text bank**, if story's compressed size needs it, **comes from music's spare `$79`, not from
  CHR** (R8.7).
- **Vanilla gaps are allocator seeds for small data**, not roles: `$3F:$FAC0-$FF1F` minus `$FFE0-$FFEF` (§1.3),
  `$3A:$95D4-$9FFF` (screen scripts, §6.6), the empty tileset pages `$2B:$9200` and `$2D:$9200` (2,304 B each; no stage
  uses them now that the lap and lobby live on TS_STADIUM), the text-bank holes `$3C:$9D16-$9FE1`, `$3D:$BA8D-$BCFF`,
  `$3D:$BF42-$BFFF`, the sprite-bank fill (1.2 / 2.3 / 4.3 KB in `$20/$22/$24`) and, after M2, the retired IRQ handlers
  `$3E:$C163-$C51D` (≈ 950 B, minus `irq_logic_tick`, §1.8). The `$36` tail is reserved for SFX and is **not** a seed.
- **ExGrafix data** (Could, §3.3) is per metatile and per tileset (≈ 1 KB for TS_LAB), stored in the CHR banks; never
  per screen.

**Overwriting `$32/$33`** (R1.5). The venue layouts are GP data, not Capcom art, so each GP venue layout replaces its
vanilla page in place, and the stage table's layout bank and page for ids 0-7 never change. Two consequences:

1. Each vanilla stage 0-7 is regression-tested from the base ROM's layout (the golden suite of §14.4) **until** its venue
   layout lands; from then on its vanilla movie retires and the venue's route movie replaces it.
2. **The YOU GET room borrows stage 5's data** (`$3B:$BD20`: `LDA #$05 / JSR $DBDB`, then paints its room [code]). When
   Tomahawk's layout replaces `$33:$A800`, the room would change. So the operand at `$3B:$BD24` becomes `#$21`, a pseudo
   row of the stage table (§4.2) whose layout source is a verbatim copy of vanilla Tomahawk's section in a GP layout
   bank (2 KB, emitted by the BPS as a SourceCopy, so no Capcom bytes ship) and whose tileset is vanilla `$2C:$89`,
   untouched. [new-code] S · Must, with the attribute table (M5).

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
| `$5104` | `$00` | ExRAM as an extra nametable (D7), **for the whole game** (R1.3). It is written to only during rendering (§3.3). Only the Could ExGrafix rooms ever change it |
| `$5105` | `$50` | horizontal mirroring (vanilla `$FB` = 1 at boot; MMC3 `$A000` = 1 is horizontal) |
| `$5106` / `$5107` | `$00` / `$00` | fill tile / attribute (fill mode is not used) |
| `$5113` | `$01` | **WORK page at `$6000`** (§2.2) |
| `$5114` / `$5115` | `$80|$3C` / `$80|$3D` | any valid ROM pair (MMC5 does not define them at power-on, so they are set before the first vanilla code runs); shadows `$4A`/`$4B` = `$3C`/`$3D` |
| `$5116` | `$FE` | `$7E` at `$C000` |
| `$5117` | `$FF` | `$7F` at `$E000` (power-on value; written anyway) |
| `$5120-$512B` | `$00` | in 8 KB mode only `$5127` and `$512B` matter: page 0 = the identity (vanilla's `$FF50` = `00 02 04 05 06 07` is MMC3's identity). Nothing writes them again |
| `$5130` | `$00` | |
| `$5200` | `$00` | vertical split off |
| `$5204` | `$00` | IRQ off |
| `$5015` | `$00` | MMC5 pulses off until the sound config turns them on (§12.5) |

4. Then `ram_probe` (§2.3), clear WORK page 1 (not the SAVE page), read the test mailbox (§14.5), `JMP $C51E`. Nothing is
   copied into WORK: the unrolled copier lives in ROM (§15.3, R1.6).

**Gotcha found for this doc** [code]: vanilla's main init `$3E:$C51E` checks that `$FFE0-$FFEF` are all `$FF` and that
`$FFF8 = $08`; otherwise it turns the screen off and loops forever at `$C53B`. Bank `$7F` must keep those 17 bytes, and the
free-space allocator must never place anything at `$7F:$FFE0-$FFEF`.

### 1.4 Bank switching [new-code] S · Must

MMC5 has one register per window, so MMC3's select register and its shadow `$4C` become dead; `$4A` (bank at `$8000`) and
`$4B` (bank at `$A000`) stay, because the scheduler (`$3E:$C604/$C609`), the sound service and the far calls read them [code,
coverage]. **No call site changes**: the helpers are rewritten in place, and **each returns exactly the registers vanilla
returns** (R1.14, feasibility-22), re-read from the ROM for this revision:

| Helper | Vanilla (MMC3) and what it returns [code] | MMC5 replacement (same entry, same returned A/X/Y) |
|---|---|---|
| `$CBAF` (tail of `$CB91`: `$17` → `$8000`) | `LDA #6 / STA $4C / STA $8000 / LDA $17 / STA $4A / STA $8001 / LDX $18 / RTS`: **A = bank**, X = `$18` | `LDA $17 / STA $4A / EOR #$80 / STA $5114 / LDA $17 / LDX $18 / RTS` |
| `$CBC0` (Y → `$8000`, Y+1 → `$A000`) | 11 instructions: **A = 7**, Y = bank+1 | `STY $4A / TYA / EOR #$80 / STA $5114 / INY / STY $4B / TYA / EOR #$80 / STA $5115 / LDA #$07 / RTS` |
| `$CBDA` (A → `$A000`) | `PHA / STA $4B / LDA #7 / STA $4C / STA $8000 / PLA / STA $8001 / RTS`: **A preserved** | `STA $4B / EOR #$80 / STA $5115 / EOR #$80 / RTS` |
| `$CBE9` (restore both from the stacked shadows) | writes `$8000/$8001` twice (`$CBF2-$CC09`), then `$CC0C-$CC1F`: **A = `$17`, X = `$18`** | same stack logic: `LDA $0103,X / STA $4A / EOR #$80 / STA $5114 / LDA $0104,X / STA $4B / EOR #$80 / STA $5115`, then the vanilla tail `$CC0C-$CC1F` unchanged |
| `$C8C1` sound service | maps `$34`/`$35` (`$C8C3-$C8D2`), restores from `$4A/$4B` and `$4C` (`$C8ED-$C901`) | `LDA #$B4 / STA $5114 / LDA #$B5 / STA $5115` ... restore from `$4A/$4B` with `EOR #$80`; the `$4C` restore is dropped |
| `$C7AD-$C7B4` NMI CHR-copy source | `LDA #6 / STA $8000 / LDA $8A / STA $8001` (no shadow) | `LDA $8A / ORA #$80 / STA $5114` (no shadow: the main thread is idle on these frames, and the sound service restores `$8000` afterwards, as in vanilla) |
| `$34:$804C-$8062` sound reader | maps `$36` at `$A000` for one byte, then `$35` | `LDA #$B6 / STA $5115` ... `LDA #$B5 / STA $5115`; then extended for the bank table (§12.2) |

`$CBC0` goes from ~36 to ~28 cycles; the stack-juggling `$CB91/$CBE9` stay (their cost is the stack work). The MMC3
hazard of an NMI landing between `STA $8000` and `STA $8001` disappears. M1's coverage run (§14.4) also lists every
reader of `$4C`; the port expects none outside the helpers and the sound service.

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

The fixed banks are rebuilt from the reassemblable source of M0 (§14.2), so the handlers are edited in that source (sizes may
change; the registry records each edit for review) rather than byte-patched in place.

`K` is a calibration constant (expected 0 or 1; 4MI's MMC5 build feeds the same variable to `$5203` that its MMC3 build
feeds to `$C000`, `r4mi/engine.md` §2.1). MMC3 asserts its IRQ near dot 260 of the line before the split and MMC5 near the
start of its target line, so each handler's `$C163` delay count (X) is re-tuned once, by comparing the vanilla and ported
frame of every split state pixel for pixel (§14.4). MMC5 counts lines only while rendering is on: no vanilla handler turns
rendering fully off, so this is safe for the literal port (see §8.4 for the raster list's rule).

**The 27 handlers** (`$3E:$C116` table; addresses re-read from the disassembly, `irq_dis.txt`):

| # | Addr | Effect (PPU writes) | Next | Conversion notes | Used by |
|---|---|---|---|---|---|
| 0 | `$C167` | `$2006 = $0671:00`, BG table `$1000`, sprites off | off `$C188` | **kept**: becomes the preset `RL_SOUNDPLAYER` in M2 (R1.14), for a VAULT if one ever ships | bank `$28` (debug sound player) |
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
- **Where it lives:** `irq_logic_tick` is interrupt code, so it may not use the C-window (R1.4). It lives in `$7E`, in the
  space the retired handlers free (`$3E:$C163-$C51D`, ≈ 950 B; the four routines need ≈ 300 B), and is called directly.
- **Parameters:** `irq_logic_tick` reads per-stage parameters from the stage-attribute record (§4.4: `EFFECTS`,
  `EFX_PARAM`) instead of the stage-6 / stage-7 hard-wires. That gives `venues_a.md` the Knight ceiling with HP and a
  retract flag and `venues_b.md` the tide dwell at its extremes (60 f), and lets Yamato's nightingale floor (R3.2) reuse
  the ceiling. **No other stage reuses the ceiling** (R3.1: the H4 compactor and escape 0A were swapped out).

### 1.9 The C-window, FAR calls and hooks [new-code] M · Must

**Why.** Every vanilla code bank is full: fill runs ≥ 32 B total 0 B in `$3E` and `$38`, 96 B in `$39` (`$BFA0`), 90 B in
`$3B`, 48 B in `$30`, 60 B in `$31`, 239 B in `$29` (`$BF11`) [measured in round 1]. The fixed bank has
`$3F:$FAC0-$FF1F` (1,120 B, `rm6/engine.md` §6) and, after M2, the retired IRQ handlers. Hooks therefore detour through
tiny stubs into GP banks.

**The C-window.** MMC5 lets `$C000` switch. A hook stub in `$7F` maps a GP service bank at `$C000`, calls it, and maps the
**previous** bank back. The vanilla caller's `$8000/$A000` banks (its own code and the object tables it is working on)
stay mapped, so GP code can read them directly.

**CW is re-entrant** (R1.4, feasibility-10). Round 1's CW kept one save area and always returned to `$7E`; a CW target that
called CW came back into the wrong bank, and an interrupt that used CW clobbered the main thread's registers. Now:

```
; call site:  JSR CW / .byte n                 (4 bytes; n = hook index into CW_BANK / CW_LO / CW_HI)
CW:     PHP / PHA / TXA / PHA / TYA / PHA      ; the caller's P, A, X, Y on the stack
        LDA CWIN_CUR / PHA                     ; the window the caller had: CW nests
        ; read n: borrow $00/$01 on the stack, (ret+1),Y, give them back; bump the return address past n
        LDA CW_LO,n / STA CW_VEC / LDA CW_HI,n / STA CW_VEC+1
        LDA CW_BANK,n / STA CWIN_CUR / STA $5116       ; shadow first, register second
        reload the caller's A, X, Y from the stack; JSR (CW_VEC)
        ; the target returns A, X, Y and C
        PHP / STA CW_A / STX CW_X
        prevbank from the stack → STA CWIN_CUR / STA $5116
        drop the 5 saved bytes; LDA CW_A / LDX CW_X; PLP; RTS   ; ≈ 110 cycles in all
```

Rules:

1. **C-window code never yields** (`$E46C`, the scheduler waits `$C5F6`/`$C62B`) and never waits for a frame. Anything
   that waits (TALK, CHOICE, menus, fades) is a coroutine in a `$8000/$A000` bank (§11.6). C-window code calls `$7E`
   routines through `CALL7E addr` (a `$7F` stub that maps `$7E`, calls, and maps the caller's window back). Routines in
   `$7F` (`$E46C`, `$E5AF`, `$E526`, `$E9D7`, …) are callable directly.
2. **Interrupts save and restore the window they interrupt.** NMI `$FFFA` → `nmi_stub`: `PHA / LDA CWIN_CUR / PHA /
   LDA #$FE / STA CWIN_CUR / STA $5116`, reload A, `JMP $C000`. The NMI's single exit (`$C0BA-$C0BF`, the only RTI at
   `$C0BF` [code, coverage]) becomes `JMP nmi_exit`: vanilla's register pulls, then `PLA → CWIN_CUR → $5116`, drop the
   stub's A, RTI. The IRQ vector gets the same stub pair (its RTI is `$C162`; after M2 the raster walker lives in `$7F`).
   So an NMI that lands inside an M1 IRQ handler running from `$7E` restores `$7E`, not the main thread's window (the third
   hole of feasibility-10). Both stubs keep their own A in a hot byte (`NMI_A`, `IRQ_A`), because an NMI can interrupt the
   IRQ stub.
3. **No CW from interrupt code** (R1.4). Band routines, the ExRAM flush and `irq_logic_tick` live in `$7E/$7F`.
4. **Object AIs never run in the C-window.** New AIs live in `$8000/$A000` banks like vanilla AIs (the object loop maps
   `$0441,X` and resumes at `$0413/$042A`).
5. Hot per-frame hooks (the frozen tick in the object loop, the T6 test, the LATCHSRC write) are inline patches in `$7F`,
   not `CW` calls.

**FAR** (for GP code calling GP code in another bank pair): `JSR FAR / .byte bank / .word target` maps the pair at
`$8000/$A000`, pushes the old shadows, and restores them on return, the `$CB91` pattern. The vanilla far call `$CB28`
(4 slots `$3C/$3A/$38/$36`, all used) is left alone.

### 1.10 The MMC5 go/no-go spike [new-code] S · Must (before M1.1)

R1.1 (scope-5, scope-11): a 1-2 session spike on **Mesen** (and on the user's cart if one exists; RULINGS §7 question 1)
runs **before** M1.1, as a formal gate. It is a set of probe ROMs like round 1's (`build/design/design-tech/probe/`),
which already pass on FCEUmm:

| # | Test | Pass |
|---|---|---|
| 1 | NES 2.0 header (§1.1) | Mesen reports 32 KB PRG-NVRAM and 8 KB CHR-RAM; the `.sav` is 32 KB |
| 2 | 32 KB PRG-RAM in 4 pages | `ram_probe` (§2.3) sees 4 distinct pages; pages 2/3 read and write at `$8000/$A000` and page 1 at `$C000`; page 0 survives a power cycle |
| 3 | ExRAM as a nametable via a mid-frame `$5105` write from an IRQ at line N | ExRAM shows from exactly line N; CPU writes made while rendering land; writes made in vblank are dropped (mode 0 rule) |
| 4 | IRQ line timing | the `$5203` IRQ fires at line N; split jitter ≤ 1 line over 600 frames; the offset gives `K` for §1.7 |
| 5 | Form-sheet streaming (R2.3) | 2,048 B streamed at 192 B/frame, and at 256 B/frame with an 8-line top blank band, on still frames with OAM DMA, with no corrupted tile and no lag frame |
| 6 | A bottom band with a palette swap (rendering off for 2 lines) | the swap lands on the line and the IRQ count is not disturbed for the next frame |

The probes run headless if a Mesen can run in this environment (open question 2); otherwise the user runs the six ROMs
and reports a screenshot of each, which is the same evidence.

**Outcomes.** All pass: M1 starts. Test 5 at 256 B fails alone: streams stay at 192 B/frame (the 16-20-frame form swap
still holds, §15.3). Test 3 fails: text windows fall back to a nametable row reserved per screen by the level build
(text v1a re-planned, about +2 sessions). Tests 1, 2 or 4 fail on the user's target: **the MMC3 fallback** of R1.1:
1 MB on mapper 4 (4MI's MMC3 build is exactly that: `4E 45 53 1A 40 00 43 08 ...`, emulator-only beyond 512 KB), 8 KB
PRG-RAM, no C-window, no ExRAM window, ROM-resident layouts with map edits only through the alternate set, and the tight
Must re-cut through the ledger before M1 starts.

---

## 2. PRG-RAM

### 2.1 Size: 32 KB, battery [new-code] S · Must

PRG-RAM stays 32 KB (R1.6); the WORK ledger (§3.4) absorbs round 1's overflow without a fifth page.

| Option | For | Against | Verdict |
|---|---|---|---|
| 8 KB battery (EKROM) | most supported | save + work + layouts do not fit; no page isolation for the save | no |
| 8 KB battery + 8 KB volatile (ETROM) | save isolated | MMC5 selects the second chip with bank bit 2; emulator support for mixed sizes is uneven; still no room for the RAM images (§5) | no |
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
in interrupts or every frame by hot vanilla-side hooks live here; everything else lives in WORK (§3.4).**

| Address | Name | Owner | Use |
|---|---|---|---|
| `$06AF` | `CWIN_CUR` | tech | bank currently in the `$C000` window (`$FE` = `$7E`); pushed and pulled by CW and by the interrupt stubs (§1.9) |
| `$06B0-$06B1` | `CW_VEC` | tech | CW's target vector (consumed before the target runs, so nesting is safe) |
| `$06B2-$06B3` | `CW_A`, `CW_X` | tech | CW epilogue scratch |
| `$06B4` | `IRQ_LINE` | tech | current absolute IRQ line (§1.7) |
| `$06B5` | `RL_CUR` | tech | raster-list cursor (0-23 buffer A, 24-47 buffer B) |
| `$06B6` | `RL_BASE` | tech | live buffer base (0 / 24) |
| `$06B7` | `RL_FLAGS` | tech | b7 staging dirty; b6 sound-in-IRQ; b0-3 chain id for `irq_logic_tick` |
| `$06B8` | `SECTION` | tech | current layout section 0-3 (§5.4; always 0 in v1.0) |
| `$06B9` | `CK_SECTION` | tech | checkpoint section (beside `$0684-$0686`) |
| `$06BA` | `GP_HOT` | tech | b0 window open, b1 world frozen (dialogue), b2 T1-lite ride active, b3 repaint pending, b4 DEV, b5 text owns the CHR stream, b6 new-stage entry (set by `$CD3B`/`$CD43`, read by the stage-init hook, §4.5), b7 FIGHT_CTX active (hot copy for the respawn path, §4.6) |
| `$06BB-$06BC` | `LFSR` | tech | 16-bit Galois LFSR (§7.8) |
| `$06BD-$06C8` | `SYS_HOT` | systems.md | 12 bytes for its hot values (SELECT hold, SEL_USED, SWAPMASK, LASTW, swap cooldown, CHR stream position, Time Stop, stagger, multi-kill, the 10-frame interact lock of R2.10) |
| `$06C9-$06D0` | `SND_BANK[8]` | tech | per-stream data bank for the sound reader (§12.2) |
| `$06D1-$06D8` | `TXT_HOT` | tech | text runner state, typewriter delay, blip id, ExRAM queue head and tail, strip count, flags |
| `$06D9` | `CW_P` | tech | CW epilogue scratch |
| `$06DA-$06DB` | `NMI_A`, `IRQ_A` | tech | the interrupt stubs' own A (§1.9) |
| `$06DC` | `MUTE` | tech | the D9 channel mute mask, read by the sound driver inside interrupts (§12.6) |
| `$06DD-$06FF` | reserve | any doc | 35 B, handed out through the hook registry |
| `$07FA-$07FF` | `NMI_EXT` | tech | NMI extension: stream length and PPU address for this frame, window palette restore request, VRAM-queue and repaint flags (next to the vanilla queue `$07F0-$07F9`) |
| `$0698` | `DEV_FLAGS` | tech | b0 EXTRA CONFIG used this boot, b1 godmode, b2 no-clip, b3 frame step |
| `$064C` | reserve | | |

Round 1's `ASCROLL` (`$06D9-$06DC`) is gone with T1-full (Won't, §9.2); round 1's `CW_A/X/Y/P` save area became the CW
stack frame.

### 3.2 Zero page

No new zero page. GP routines borrow vanilla scratch `$00-$0F` inside a routine (vanilla's convention) and never across a
yield; CW borrows `$00/$01` on the stack and gives them back before its target runs. Pointers that must survive an
interrupt use absolute WORK addresses.

### 3.3 ExRAM (`$5C00-$5FFF`, 1 KB): mode 0 for the whole game (R1.3)

ExRAM is a nametable that `$5105` can place in any of the four slots, **for the whole game** (D7; the blocker
feasibility-1 / consistency-1 is resolved this way). CPU writes count only **while the PPU is rendering** (in modes 0/1
MMC5 stores `$00` otherwise), and the CPU cannot read it back. So:

| Range | Rows | Use |
|---|---|---|
| `$5C00-$5C7F` | 0-3 | the pop-up window: border, 2 text rows, border (§11.3) |
| `$5C80-$5D3F` | 4-9 | the dialogue, debrief and help window: border, 4 text rows, border |
| `$5D40-$5FBF` | 10-29 | free; full-screen text pages (plaques, crawl, scene cards) use rows 0-29 as a whole screen |
| `$5FC0-$5FFF` | | attribute table: the windows' palettes |

- No WORK mirror is kept: the decoder writes cells through the **ExRAM write queue** (64 B ring in WORK, §3.4), flushed
  ≤ 32 B per frame by a band routine in `$7F` that runs **inside an IRQ, so always during rendering**: the window's own
  top band when one is open, otherwise a 1-line band at line 8, armed only when the queue is not empty. The `$5204`
  bit 6 "in frame" flag is **not** used: FCEUmm does not implement it (a probe that polled it never left its loop) [seen].
- Nothing else is stored in ExRAM.
- **There is no extra 4 KB CHR page** (R1.3): with 8 KB CHR-RAM the ExGrafix page bits reach only `$0000` or the sprite
  table (feasibility-1 probe `exgfx.nes`).
- **ExGrafix (mode 1) is Could, with W1** (R1.3): only in locked rooms with no text, namely W1's 16-bit section and the
  METALL 16 arena. Entering such a room: rendering off, `$5104 = $02`, fill the 960 attribute bytes from the tileset's
  per-metatile extended-attribute table (≈ 1 KB per tileset, §1.2), `$5104 = $01`, rendering on, and the announcer queue
  is held (no pop-ups, no heckles) until the room is left. Leaving: rendering off, `$5104 = $00`; the window rows are
  rewritten at the next open. No scrolling screen ever uses mode 1.
- **The "SUPER colour" of W2, W3 and the escape in v1.0** (R1.3) needs nothing from ExRAM: richer per-screen palettes,
  parallax and palette bands from the raster list (§8), and the music channel drop (the D9 mute mask, §12.6, Must); the
  MMC5 pulses join it if they ship (Could, §12.5).

Probes [seen, round 1, `probe/exnt2.nes`]: ExRAM writes timed after the NMI (past vblank) landed; with `$5203 = 120` and
an IRQ that writes `$5105 = $AA`, scanlines 0-119 showed the CIRAM nametable and **scanlines 120+ showed ExRAM**, on
exactly line 120. A control build without the IRQ showed CIRAM only. Mesen is checked by the go/no-go spike (§1.10).

### 3.4 The WORK ledger (page 1 at `$6000-$7FFF`) (R1.6)

Every byte of page 1 has an owner. The ledger lives in `src/work.yaml`; GP code addresses WORK only through the symbols it
defines, and the static suite (§14.7) fails on any overlap or on an access outside a declared range.

| Range | Size | Name | Contents | Owner |
|---|---|---|---|---|
| `$6000-$61FF` | 512 | per-slot arrays | 32-byte stride, slots 0-22: `$6000` GP_SUBID, `$6020` GP_ARG, `$6040` GP_OFLAGS, `$6060` LASTHIT, `$6080` LATCHSRC, `$60A0` REHIT, `$60C0` FREEZE, `$60E0-$61FF` 9 AI variables (GPV0-GPV8) | tech (format); systems (meaning of LASTHIT, LATCHSRC, REHIT, FREEZE) |
| `$6200-$622F` | 48 | `SA_CUR` | the current 48-byte stage-attribute record (§4.4) | tech |
| `$6230-$625F` | 48 | loader | `GRP_ROW` (16), the `VARIANT` row (16), `RAM_ID`, `LIST_N`, `LIST_PTR` (2), section residency, `LAYOUT_TIER` (§5.5), T6 table base (2), spare | tech |
| `$6260-$626F` | 16 | fight | `FIGHT_CTX`, `FIGHT_ID`, `FIGHT_RESULT`, the return-to record (`RET_ID`, `RET_SCREEN/CHR/PAL` = copies of `$0684-$0686`, `RET_SECTION`, `RET_FLAGS`), spare (§4.6) | tech; meta and fortress read `FIGHT_RESULT` |
| `$6270-$627F` | 16 | `RULESET` | meta's ruleset choke point (`meta.md` §9) | meta |
| `$6280-$62BF` | 64 | `RET_SNAP` | the return-to snapshot: `$0340-$035F` and `$0650-$066F` of the hub or lobby (§4.6) | tech |
| `$62C0-$62FF` | 64 | HUD | 8 widget records × 8 B (§7.13) | tech (format); stage docs (records) |
| `$6300-$63FF` | 256 | run block | systems' run block (≈ 24 B), scorecard counters (≈ 48 B), announcer queue (16 × 2 B), commentator cooldowns (16 B), T3 channels `CHAN[16]`, meta's stage counters for the `$4n` predicates (8 B), key counter, T1-lite director state (16 B); ≈ 72 B spare | systems / meta / tech, sub-ranges in the registry |
| `$6400-$65DF` | 480 | raster list | 2 buffers × 24 bands × 10 arrays (§8.1) | tech |
| `$65E0-$65FF` | 32 | compositor | band-compositor inputs: stage preset, window request, director requests, priorities | tech |
| `$6600-$6BFF` | 1,536 | object list | the object-list copy, 6 arrays × 256 (§7.3) | tech |
| `$6C00-$6DFF` | 512 | text | glyph reverse map (256), decoded page (128), ExRAM write queue (64), strip ids (32), runner state (32) (§11) | tech |
| `$6E00-$6EFF` | 256 | staging | CHR/VRAM stream staging buffer, read by the unrolled copier in ROM (§15.3) | tech |
| `$6F00-$6FFF` | 256 | MMC5 sound | the second driver instance's channel state (Could; reserved so nothing moves if it ships) | tech |
| `$7000-$70FF` | 256 | edit log | map-edit log, 64 entries × 4 B (§5.6) | tech |
| `$7100-$71FF` | 256 | queues | repaint queue (32 × 4 B), CHR stream queue (8 × 8 B), poke-list scratch (64 B) | tech |
| `$7200-$73FF` | 512 | DEV ring | the last 64 events × 8 B (DEV builds; unused in release) | tech |
| `$7400-$75FF` | 512 | LIVE FILE | `meta.md` §1.2, at meta's CPU address, in page 1 (§13) | meta |
| `$7600-$79FF` | 1,024 | LIVE SYS | `meta.md` §1.2 | meta |
| `$7A00-$7AFF` | 256 | player block | `CHAR` and the stashed HP (Should, §7.9), attach/vehicle state (32 B), pad history ring (64 B, T7), utility bookkeeping for slots 4-7 | tech / systems |
| `$7B00-$7FFF` | 1,280 | free | handed out by the registry with an owner per range: venue objects' persistent state, the GP Rush runner (Could, ≈ 64 B) | registry |
| | **8,192** | | | |

What changed against round 1's over-committed page (feasibility-12): the 1,280-B borrowed-tile buffer is gone (tiles
are restored from ROM, §11.4); the unrolled copier moved to ROM bank `$46`, leaving a 256-B staging buffer; the map-edit
log shrank to 256 B; F-GRID is deleted; the raster list's auxiliary arrays, the T7 ring, the return-to snapshot and the
player-variant state now have ranges. 1,280 B stay free.

---

## 4. Stage ids, the stage-attribute record, stage changes and the fight loader

### 4.1 Why the id space breaks today

`$51` is read by **45 executed instructions** (`build/research/rm6/rm6-critic/stage_id_sites.txt`, each disassembled in
context in `sites51.txt`). A stage id ≥ 16 has bit 3 clear, so every "is this a fortress?" test treats it as a Robot
Master stage; the stage table `$3E:$DF25` (9 × 16), the object-list tables `$3A:$80BF/$80CF/$80DF` and the collision
groups `$3E:$DB03` are 16 entries packed against code; several tables are 8 entries (`rm6/engine.md` §9).

**When it must be fixed** (R1.2, scope-12): the venues keep ids 0-7, so vanilla's readers already treat them right, and
the Blizzard slice needs none of this. The 45 readers are rewritten at **M5**, before the first id ≥ `$10` (the
Opening). What M2 needs is only the record and its init hook (§4.5), read by GP code.

### 4.2 The id map (binding, R1.2)

This map is binding on every doc (R1.2; feasibility-2, consistency-2, scope-12). `fortress.md`, `meta.md` and
`story.md` renumber to it; the **meta index** (`meta.md` §1.8) is unchanged and decouples the save format from these ids.

| Engine id | Stage | Class | Meta index | Tier | Data |
|---|---|---|---|---|---|
| `$00-$07` | the 8 venues, **vanilla ids kept** (Blizzard 0, Wind 1, Plant 2, Flame 3, Yamato 4, Tomahawk 5, Knight 6, Centaur 7) | VENUE | 1-8 | Must | own tileset slot each (§5.3), layouts in `$32/$33` in place (§1.2) |
| `$08-$0F` | **legacy** Mr. X 1-4, Wily 1-4, unchanged | LEGACY | none | Must (regression) | vanilla data: the regression movies, the 1993 data rows (Could), the `???` fight (fight `$27` = id `$0F`, room 06, under RULESET 1993; Could with GP Rush) |
| `$10` | Opening Ceremony | SPECIAL | 0 | Must (Opening-lite) | TS_STADIUM |
| `$11` | **HALFTIME RIOT** (R4.3) | SPECIAL | 9 | Must | TS_STADIUM |
| `$12-$15` | Exhibitions E1-E4 | EXHIBITION | 10-13 | Could (R3.7; E4 Won't) | TS_ARCADE |
| `$16-$1A` | Hall of Fame H1-H5 | FORTRESS | 14-18 | H1/H3/H5 Must; H2/H4 Should | copies of vanilla tileset pages (§5.3) |
| `$1B-$1D` | Super Wily Castle W1-W3 | FORTRESS | 19-21 | W2/W3 Must; W1 Could | |
| `$1E` | victory-lap credits | SPECIAL | 23 | Could (R0.3 item 8) | TS_STADIUM |
| `$1F` | Mr. X Returns | FORTRESS | 22 | Won't (v1) | points at id `$08`'s layout and tileset |
| `$20` | DEV sandbox | DEV | none | Must (DEV builds) | a copy of any stage, for tests |
| `$21` | YOU GET room (pseudo-row, never a value of `$51` after init) | PSEUDO | none | Must | vanilla Tomahawk's section, copied (§1.2) |

All 32 ids are taken; the table has 34 rows in every build (`$20` is reachable only in DEV builds). Nothing in the new
code assumes ids < 32 except table sizes; the field widths allow 64.

- Legacy ids keep vanilla fortress rules (CONTINUE-only game over, no weapon get) unless a fight record overrides them
  through RULESET (consistency decision 37).
- The GP Rush lobby (Could) is **screen `$1D` of the Opening's layout** on TS_STADIUM, entered by the warp to stage `$10`
  screen `$1D`; it has no id and no slot of its own (consistency-31).
- The HALFTIME RIOT (`$11`) and the Opening (`$10`) are why the attribute readers are rewritten at M5, not M2.

### 4.3 The 45 `$51` readers and their replacements [new-code] M · Must (M5, part of D8)

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
| `$3F:$F4EB` | boss and plate flags only for stages < 8 (`$F6B3/$F6BB/$F6C3`, plate screen `$F518`) | `SA.FLAGIDX` (a bit index into the LIVE FILE) + `SA.SECRET_SCR` |
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
| `$3B:$BD20` | saves `$51`, loads stage 5's data for the YOU GET room, restores | operand `$BD24` `#$05` → `#$21`, the YOU GET pseudo-row (§1.2) [new-code] S |
| `$3C:$80D6`, `$8147`, `$8178`, `$8185` | boss intro: CHR `$F210`, anim `$F200`, palette `$F218`, anim `$F208` (8 entries each) | `Y = SA.INTRO`; the four tables relocated to N entries |
| `$3C:$81B1` | data-panel record `$8606/$860E` | `Y = SA.INTRO`; table relocated |
| `$3E:$CDF2` | `JSR $F533`: stage already cleared → revisit palettes (`$06A0`) | LIVE FILE `STAGE_CLEAR[SA.META]` and `SA.FLAGS1.REVISIT` |
| `$3F:$F94F` | `JSR $F527`: boss already beaten → beam out (no rematch) | `SA.FLAGS1.REMATCH` (meta.md and systems.md remove the beam-out) |
| `$3E:$CE07` | `JSR $DBDB` with A = `$51` (stage init on respawn) | the stage-init hook (§4.5) |
| `$3E:$DA1C` | `LDA $51 / BNE`: Blizzard's ship-deck collision offset | `SA.EFFECTS.SHIP` |
| `$3E:$DAEE` | collision group `$DB03,Y`, then `$DB13[group*16+type]` | `LDY $11 / LDA GRP_ROW,Y`: the stage's 16-byte remap row is copied into WORK at init (§4.5); 16 groups available |
| `$3B:$BB82`, `$BBC2`, `$BBD6`, `$BBE4` | fortress-map dot positions (`$BC5D`, `$BC86`) | retired (fortress map) |

**E. The 11 readers of `$063D`** (`stage & 7`, executed): `$31:$98B7/$98C1/$9930` (intro tables), `$31:$98F6` (`$9B82`),
`$31:$993D` (boss type `$9D43`), `$31:$99D9` (table `$9A35`, next to the weakness table `$9A45`), `$31:$9A1A` (Centaur's
death), `$39:$8E8C/$8E9A/$8F42` (Wily 3 refight room, palette, alcove), `$3F:$FA66` (boss sprite CHR `$FA5B`). They keep
working if `$063D` holds the **Robot Master slot** 0-7: init writes `SA.RM_SLOT` there instead of `stage & 7`, and the
Wily-3-style rush overwrites it per fight, as vanilla does.

**Unexecuted readers.** M0's static scan of every code bank for `$51` and `$063D` (§16.3) catches readers the
139,200-frame tour did not execute; any it finds join these tables before M5 (round 1 risk 9).

### 4.4 The stage-attribute record (48 bytes) [new-code] M · Must

R1.14 widens the record from 32 to 48 bytes (feasibility-18, consistency-21). It is stored as 48 tables of 34 entries
(1,632 B) in core bank `$3E` (new), the 4MI lesson of "a bank byte beside every pointer" applied. At stage init the record
is copied to `SA_CUR` (`$6200`), so patched readers use absolute addressing and never map a bank.

| Off | Field | Meaning (vanilla source) |
|---|---|---|
| `$00` | `CLASS` | 0 VENUE, 1 FORTRESS, 2 EXHIBITION, 3 SPECIAL, 4 LEGACY, 5 DEV, 6 PSEUDO |
| `$01` | `FLAGS1` | b0 FORT (fortress rules), b1 YOUGET, b2 REMATCH, b3 KEEPWE, b4 **HUB** (a return-to target, §4.6), b5 REVISIT (bank-`$28` palettes when cleared), b6 TA_OK (Time Attack eligible), b7 NO_SAVE (credits, sandbox) |
| `$02` | `RM_SLOT` | → `$063D` |
| `$03` | `META` | `meta.md`'s meta index, `$FF` none |
| `$04` | `NEXT` | next id on clear, `$FF` map, `$FE` ending |
| `$05` | `MAP` | which map/bracket screen follows (`meta.md` / `fortress.md` enumerate) |
| `$06` | `MUSIC` | `$DFA5` |
| `$07` | `BOSS_MUSIC` | `$0C`; `$18` for the Wily Machine (`$FA13`) |
| `$08` | `PALETTE` | start palette `$DF95` |
| `$09` | `CHR_BASE` | base BG CHR set `$DF85` |
| `$0A` | `COLL_GROUP` | remap row 0-15 (`$DB03`) |
| `$0B` | `LIST_ID` | object list of section 0 (into the list table, §7.3) |
| `$0C-$0D` | `LAYOUT_SRC` | ROM bank and page of section 0's layout (`$DF25`, `$DF45`) |
| `$0E-$0F` | `TILE_SRC` | ROM bank and slot (0/1) of the tileset (§5.3; vanilla rows: `$DF55`, `$DF65`) |
| `$10-$11` | `ALT_SRC` | ROM bank and index of the alternate set (vanilla: `TILE_SRC` bank, `$9B`) |
| `$12` | `SECT` | index into the section table, `$FF` none (sections are Should) |
| `$13` | `EFFECTS` | b0 SHIP, b1 TIDE, b2 CEILING, b3 WM_FLOOR, b4 T1-lite rides present, b5 T6 cells present, b6 pop-ups at the bottom (default top, §11.3), b7 no pop-ups |
| `$14` | `EFX_PARAM` | effect parameter (tide dwell, ceiling HP, ceiling special screen; vanilla's `$57 = 6` test in handler 11) |
| `$15` | `FORT_COL` | `systems.md`'s boss row / fortress damage column |
| `$16` | `INTRO` | boss-intro record, `$FF` none |
| `$17` | `YOUGET` | YOU GET record: index into `systems.md`'s venue id → weapon slot table (consistency-37) and the text id |
| `$18-$19` | `SHUT1/2` | `$9A96/$9AA6` |
| `$1A` | `SECRET_SCR` | renamed from `PLATE_SCR` (consistency-21): a boss kill on this screen sets SECRETS b0 and drops the stage's plate (`$F518`; `$FF` none) |
| `$1B` | `FLAGIDX` | LIVE FILE bit set on the champion's or boss's kill (replaces `$F6B3/$F6BB/$F6C3`) |
| `$1C` | `POKE_LIST` | head of section 0's poke-list chain, all tiers (§5.5; round 1's `HARD_LIST`) |
| `$1D` | `SCORE_ID` | `systems.md`'s scoring boss / `meta.md`'s secret list |
| `$1E` | `PAR` | par time in 4-s units (`systems.md` §6.3) |
| `$1F` | `VARIANT` | variant row (§4.3 C) |
| `$20-$23` | `NO_TAG` | **32-bit screen mask** (R1.14): bit n set = Break Man's call is disabled on screen n. Read only by the tag-partner code (Should); 0 in v1.0 data unless a stage owner fills it early |
| `$24-$25` | `OWNED` | owned weapons/forms override for this stage, `$0000` none (Exhibitions, Could) |
| `$26` | `ERA` | F-ERA era (W1, Could), 0 none |
| `$27` | `PLATE_OBJ` | sub-id of the stage's plate-drop object (`venues_a.md` §0.1), `$FF` none |
| `$28-$2A` | `LOCAL_CHR` | bank and address of the stage-local CHR set table (ids `$E0-$FB`, §7.6) |
| `$2B` | `HUD_ID` | the stage's HUD widget list (§7.13), `$FF` none |
| `$2C` | `COMM_ID` | the stage's commentator table (`story.md`'s lines, §11.7) |
| `$2D` | `CK_TABLE` | checkpoint table for EXTRA CONFIG's CP field and the mailbox (`meta.md` §9.6) |
| `$2E` | `FIGHT_ROW` | this stage's boss in `meta.md`'s fight table (`$FF` none) |
| `$2F` | spare | |

Rows for ids 0-15 are generated from the vanilla tables by `tools/build/stagetab.py`, and a test asserts that every vanilla
id's record reproduces the vanilla values (the M0 census and the M5 gate). Rows `$10-$21`, and each venue's row once
its GP layout lands, are generated from the stage owners' `.lvl` headers (§6.2).

### 4.5 Stage init and the relocated tables [new-code] M · Must

The hook sits at the entry of `$3E:$DBDB` (A = stage id), called from `$CD3B`/`$CD43` (new stage), `$CE07` (respawn)
and `$3B:$BD25` (the YOU GET room, A = `$21` after M5). The two new-stage entries also set `GP_HOT`'s "new stage" bit,
so the hook knows which case it is.

1. `$51` = id; copy the record to `SA_CUR`; `$063D = SA.RM_SLOT`; copy the 16-byte collision row to `GRP_ROW`; load the
   `VARIANT` row into WORK; compute `LAYOUT_TIER` from RULESET (§5.5).
2. **The stage changes** (`RAM_ID` ≠ id): first **`CALL7E $CE44`**, which clears `$0340-$035F` (alternate-metatile bits)
   and `$0650-$066F` (the list's kill field) [code: `LDA #0 / LDX #$1F / STA $0650,X / STA $0340,X / DEX / BPL`].
   Vanilla runs it only on the new-stage path (`$CE52`, from `$CD43`), so a respawn warp into another stage kept the old
   bits; feasibility-3 measured the result (Knight drawn with alternate metatiles, its type-`$80` screen script never
   spawned). R1.7 makes the clear run on **every** id change. Then, if `RET_FLAGS` b7 (restore pending, set by
   `fight_return`, §4.6) is set and id = `RET_ID`, restore `RET_SNAP` into `$0340/$0650` and clear the flag. Then build
   the RAM images (§5.2), apply the poke lists (§5.5), copy the object list to WORK (§7.3), clear the map-edit log, set
   `RAM_ID`. The YOU GET room and every fight-loader warp enter through the respawn path (`$F0 = 2`), not the new-stage
   entries, and are covered by this test. A plain respawn in the same stage keeps the image (and its edits), as vanilla
   keeps `$0340`.
3. Set the zero-page level pointers exactly as `$DBFB-$DC17` did, but from RAM ids: `$6E = $83`, `$6F = $82`, `$52 = 0`,
   `$53 = $A0 + 8*SECTION`, `$63 = $80` (or `$89` for slot B), `$67 = $63 + 5`; `$064E = SA.CHR_BASE`; palette
   (`$C9EF` via `CALL7E`), music to `$DC`, HP `$1B`. In a fight (§4.6), slot 0's X/Y come from the fight record.
4. Return into vanilla at `$DC1F` (thread setup, PPU off, variable clears, checkpoint screen `$0684`, paint).

**Staging.** M2 builds steps 1-4 with the records for ids 0-15 and leaves every `$51` reader alone (D8). M5 adds the
reader rewrite of §4.3, the relocated tables below, ids `$10-$21`, and the YOU GET operand.

Relocated tables (all in core bank `$3E`, read only by GP code or by patched operands; M5): the stage table
`$DF25-$DFB4` (replaced by the record); object lists `$3A:$80BF/$80CF/$80DF` (replaced by the list table with bank
bytes, §7.3); `$DB03/$DB13` (16 groups); `$F518`, `$F6B3/$F6BB/$F6C3`, `$F704`; intro `$F200/$F208/$F210/$F218` and
panel `$3C:$8606/$860E` (N records); shutters `$39:$9A96/$9AA6`. Freed vanilla bytes are returned to the allocator only
after the M5 gate passes.

### 4.6 Stage changes, FIGHT_CTX and the fight loader [new-code] M · Must (R1.7)

**The fight loader is Must and tech's** (R1.7; scope-6, scope-12 and scope decision 12). `meta.md` owns the fight table and its
10-byte records (`meta.md` §9.2.1: stage id, room screen, spawn X/Y, CHR, palette, music, icon, name, flags); this
section owns the code that loads one and comes back.

```
fight_load(fight_id, ctx):
    rec = FIGHT_TABLE[fight_id]                       ; meta's record
    if ctx.return_kind != NONE:                       ; remember where to come back to
        RET_ID = $51; RET_SCREEN/CHR/PAL = $0684-$0686; RET_SECTION = CK_SECTION
        RET_SNAP[0..31] = $0340-$035F; RET_SNAP[32..63] = $0650-$066F           ; 64 B (R1.7)
    FIGHT_CTX = ctx | $80; FIGHT_ID = fight_id; FIGHT_RESULT = 0; GP_HOT.b7 = 1
    RULESET from the record's flags (meta's choke point)
    $51 = rec.stage; $0684 = rec.screen; $0685 = rec.chr; $0686 = rec.pal; $F0 = 2    ; vanilla's warp
```

The stage-init hook (§4.5) then clears the stale bits (the id changed) and builds the arena; with clean fields the
vanilla warp into a boss room spawns the boss intro (`$93` → `$95`, measured by feasibility's `bosswarp.py`).

**`FIGHT_CTX`** (WORK `$6260`): b7 active; b6 ONE_LIFE (a death ends the bout as a loss); b5 NO_SAVE (always set by
the loader); b0-2 return kind: 0 none, 1 hub (W2), 2 lobby (GP Rush, Could), 3 EXTRA CONFIG, 4 mailbox test, 5 the H3
room (Doc Robot MK-VI, Should). Every path that would end or restart the stage tests it:

| Path | Vanilla site | With FIGHT_CTX b7 set |
|---|---|---|
| after the boss dies (weapon get or not) | `$3F:$F9A0` | `FIGHT_RESULT = WIN`; skip YOU GET, `FLAGIDX`, `SECRET_SCR`, `NEXT`, the autosave and the debrief; `fight_return()` |
| stage clear | `$3F:$F0FB`, the player's end-of-stage path `$38:$916B` | as above |
| player death | the respawn through `$3E:$CE07` | ONE_LIFE: `FIGHT_RESULT = LOSS`, `fight_return()`; else respawn in the arena, as vanilla |
| game over | `$3C:$805F` | `FIGHT_RESULT = LOSS`, `fight_return()`; the lives policy is RULESET's |
| autosave points | `meta.md` §1.5 | skipped (NO_SAVE) |

`fight_return()` clears `FIGHT_CTX`, then by return kind: warp back (`RET_FLAGS` b7 = restore pending, `$51 = RET_ID`,
`$0684-$0686 = RET_*`, `$F0 = 2`; the init hook clears the bits, then restores `RET_SNAP`, and the hub's objects respawn
under the restored kill bits), or go to EXTRA CONFIG, or stop with `FIGHT_RESULT` left in WORK for the test to read. The
hub reads `FIGHT_RESULT` and does its own bookkeeping (W2 closes an alcove by setting its `$0340` bit: `fortress.md`'s
mechanic).

**Rule for hubs and lobbies** (`SA.FLAGS1.HUB`): their state lives in `$0340/$0650` (the snapshot) and in save flags.
They never rely on `map_set` edits surviving a fight; an edit there is replayed by the hub's init from flags. That keeps
the snapshot at 64 B.

**Users:** W2's pair bouts (Must, M8; `fortress.md` retags its §5.2.1 [new-code] M, feasibility-3/19), EXTRA CONFIG's
`FIGHT n` and the mailbox's fight command (Must, from M7), Doc Robot MK-VI (Should, R3.6: he copies a Rockman 2 boss and
is reached only through this loader, never by running champion AI in H3's room), GP Rush and Time Attack (Could/Should).

---

## 5. WRAM-resident layouts, the tileset-slot table, poke lists and the map-edit service

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
- Each slot has **its own alternate set** (`venues_b.md`'s request) without a whole 8 KB ROM bank per venue: the loader
  copies slot pages and the alternate set from independent sources, so two stages share one ROM bank (§5.3).
- Cost: about 5.5 KB copied at a new stage start (2 KB layout section 0, 2.25 KB tileset slot, 1.25 KB alternate set;
  sections 1-3 and slot B on demand) with an unrolled copy, ≈ 50,000 cycles ≈ 1.7 frames, while the screen is already off
  for the 30-row paint.

### 5.3 The tileset-slot table [new-code] S · Must (R1.10)

**One table, owned here** (R1.10; scope-11, consistency-9, feasibility-17). Every stage row names its slot and its
alternate-set source (`TILE_SRC`, `ALT_SRC`, §4.4); `art_audio.md` lists content and block counts only and regenerates its
table from this one; `fortress.md` and the venue docs cite it. Under the RAM image each slot brings **its own alternate
set**, so art's round-1 rule "two alternate-heavy stages must not share a bank" and `venues_b.md`'s "a whole bank per
venue" both retire.

**ROM packing: 2 slots per bank** (R1.10):

| Bank offset | Contents | Size |
|---|---|---|
| `+$0000-$08FF` | slot 0: 5 metatile pages + 4 block pages | 2,304 B |
| `+$0900-$11FF` | slot 1 | 2,304 B |
| `+$1200-$16FF` | slot 0's alternate set | 1,280 B |
| `+$1700-$1BFF` | slot 1's alternate set | 1,280 B |
| `+$1C00-$1FFF` | the two slots' T6 transition tables (§10) | 2 × 512 B |

The loader copies a slot to `$8000` (slot A) or `$8900` (slot B) of the TILES page and its alternate set to `$9B00`,
where the vanilla readers expect it (`$9B-$9F`), and the T6 table to `$9200`.

**The slots** (26 in the full design, 13 banks `$62-$6E`; v1.0 uses 14 slots in 7 banks):

| Bank | Slot 0 | Slot 1 | Tier |
|---|---|---|---|
| `$62` | Blizzard (from `$2E:$80`) | Wind (from `$2C:$80`) | Must |
| `$63` | Plant (from `$2E:$92`) | Flame (from `$2F:$80`) | Must |
| `$64` | Yamato (from `$2E:$89`) | Tomahawk (from `$2C:$89`) | Must |
| `$65` | Knight (from `$2D:$80`) | Centaur (from `$2D:$89`) | Must |
| `$66` | **TS_STADIUM**: the Opening, the HALFTIME RIOT, the lap and the GP Rush lobby screen | H1 (from Wily 2's `$2A:$89`) | Must |
| `$67` | H3 (from Mr. X 3's `$2F:$92`) | H5 (from Mr. X 4's `$2B:$80`) | Must |
| `$68` | W2 (from Wily 3's `$2A:$92`) | W3 (from Wily 4's `$2B:$89`; the v1.0 escape uses it too) | Must |
| `$69` | H2 (from Wily 1's `$2A:$80`) | H4 (from Mr. X 2's `$2F:$89`) | Should |
| `$6A` | TS_LAB (W1, the escape's eras) | TS_ARCADE (E1-E4, one CHR third each) | Could |
| `$6B-$6E` | the 8 venues' second slots, reached through the section switch (§5.4) | | Should |

Vanilla sources are read from `$DF55/$DF65` [code]; vanilla's own tileset banks `$2A-$2F` stay untouched (the legacy
ids and the 1993 rows still load them). The MUSEUM third shared by the H wings and the venue thirds are CHR sets (§7.6),
not slots.

### 5.4 Decision, and sections (Should)

**Pros and cons:**

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
| Emulator dependence | needs 32 KB PRG-RAM and RAM in `$8000-$BFFF` (both confirmed on FCEUmm [seen]; Mesen checked by the go/no-go spike, §1.10) | none |

**Adopt it (Must)**, in the RAM-image form above, because T6 (BRIEF §4, `venues_b.md` Blizzard), the map-edit service,
the CASUAL poke lists (R2.9) and per-slot alternate sets all need it, and it costs no reader changes. **Sections:
Should**: the format reserves 4 × 32 screens per stage, but no v1.0 stage needs more than 32 (consistency decision 37:
fortress stages ≤ 26 screens, venues ≤ 32), so `SECTION` stays 0 in v1.0. The **slot-B section switch** (an exit that
moves `$63/$67` to slot B, art's "section switch") is Should with the venues' second slots (§5.3). **LZ compression:
Won't (v1)**: raw layouts fit (23 stage sections × 2 KB ≈ 46 KB in the 8 layout banks of §1.2).

**Section mechanics (Should):** an exit target byte `$A0-$FF` (bit 7 = explicit target, as vanilla, plus bits 5-6 =
section) means "section `(t >> 5) & 3`, screen `t & $1F`". Inside a script, any byte ≥ `$80` after an exit's palette
byte is read as its target and exit types are 1-6, so these bytes cannot be mistaken for a list terminator. The exit
handler hook (`$D6F5` path, `rm6/levels.md` §9) copies the section's layout if it is not resident, sets `SECTION`, `$53`
and the section's object list (§7.3), then runs the vanilla transition. Checkpoints store `CK_SECTION` beside
`$0684-$0686`. Vanilla targets already use bit 7 with screens `$00-$1F` (bits 5-6 clear), so every vanilla exit keeps
its meaning.

### 5.5 Poke lists: one format, four tiers [new-code] S · Must

**One format** (R1.10, scope-25): this one. `systems.md`'s 3-byte draft is retired; the `.lvl` `hard` and `casual`
lines compile to it. Applied right after a section is copied:

```
list:   tier mask (b0 CASUAL, b1 NORMAL, b2 HARD, b3 1993), then entries:
        page_id (01 WORK, 02 LAYOUT, 03 TILES), offset_hi, offset_lo, value
        ... terminated by page_id $FF; lists chain, the chain ends with mask $00
```

A list applies when `mask & (1 << LAYOUT_TIER)` ≠ 0, so one list can serve CASUAL and NORMAL. **`LAYOUT_TIER`** is
derived once per stage start (consistency-16), because the file's preset becomes EDIT after any hand change and HARD is
a per-file override: 3 if RULESET says RULES = 1993; else 2 if the HARD bit is set; else 0 if `CFG_CASUAL` is set
(R2.9; `meta.md` owns the bit); else 1. Per section the record's `POKE_LIST` (and the section table) points at the
chain. Object placements are patched the same way (page 1 offsets into the object-list copy).

**Macros** (`src/gp/ai.oph`), generated from `meta.md`'s bit table (`src/gp/bits.inc`) so they cannot drift:

- `IFHARD skip` branches past a block unless HARD is on. Round 1's `BIT DIFF_A / BVC` tested bit 6 (GUARDS) while meta
  put HARD at b5 (consistency-15). Now: if meta moves HARD to b6 (the critic's fix), the macro assembles to
  `BIT RULESET_DIFF / BVC skip`; otherwise to `LDA RULESET_DIFF / AND #HARD / BEQ skip`. A unit test asserts that
  `IFHARD` follows HARD and nothing else.
- `IFCASUAL skip`, and `TIERVAL casual, normal, hard` (`LDY LAYOUT_TIER / LDA table,Y`, 1993 using the NORMAL value).

**The CASUAL lever list** (R2.9, design-7). Every stage fills in the same five levers; this is how each one is built:

| Lever | Mechanism |
|---|---|
| reflex windows × 2 | `TIERVAL` on the AI's window constant |
| mash counts −40 % (hold to struggle allowed) | `TIERVAL`; the struggle helper `MASH n` counts a held button as one press per 6 f under CASUAL |
| set-piece timers +50 % | `TIERVAL`, or a CASUAL poke on the object's `arg` in the list copy |
| +1 checkpoint per section | the level build places a dormant object (family `$F7`, sub `DORMANT`); a CASUAL poke rewrites its sub-id to `CHECKPOINT`, which writes `$0684-$0686` when Rock passes, as a script checkpoint does (`.lvl`: `casual checkpoint <screen> <x> <y>`) |
| skill-gated secrets relaxed one step | CASUAL pokes on the layout (a ledge block, a narrower gap) or the object list |

**HARD in v1.0** (R2.9, scope-19) is ×1.5 damage, drops LESS and no refill, all through RULESET; the framework above
stays. Per-stage HARD poke lists and boss AI branches are **Should**, added stage by stage.

### 5.6 The map-edit service [new-code] S · Must (R1.10)

**One service** (R1.10, scope-10) for everything that changes the BG or collision at run time. Two primitives and one
repaint queue:

- **`map_set(section, screen, row, col, block)`** writes a layout byte in the LAYOUT page, appends `(where, old block)`
  to the edit log, and queues a repaint of the block's on-screen cells.
- **`alt_flip(id, on)`** sets or clears vanilla's alternate-metatile bit for metatile `id` in `$0340-$035F` (one bit per
  id, vanilla's breakable mechanism) and queues a repaint of the visible cells that use `id`. The level build lists, per
  screen, the cells of every flippable id (at most 8 per id per screen, a build check), so nothing is scanned at run time.
- **The repaint queue** (32 entries × 4 B, WORK `$7100`) holds two kinds: CELL, one 16×16 metatile (2 × 2 tiles through
  the vanilla VRAM buffer plus its attribute byte, recomputed from the 32×32 block), and COLUMN, an 8-px column through
  the vanilla painter (`$D8AF/$D904/$D1FF`, the oil-ignition pattern `$3E:$DE03-$DE5C`). **Per-frame budget: 4 CELLs or 1
  COLUMN**, and none on a frame that already paints a scroll column. Off-screen cells are not queued: the column painter
  reads the RAM layout, so they appear correctly when they scroll in.
- **The edit log** (WORK `$7000`, 64 entries × 4 B = 256 B, R1.6): `section<<5 | screen`, `col<<3 | row`, old block,
  flags. `map_undo_all()` restores a boss room after a death; EXTRA CONFIG lists the edits. Edits flagged persistent
  survive deaths; when the log is full, the oldest non-persistent entry is dropped.

Built on it, and nowhere else: **T6** (§10, variant blocks), **VA-TIMED** (`venues_a.md`: a toggling floor is `alt_flip`
on a timer), T3's walls (§7.10), **F-PIECES** (`fortress.md`: the Yellow Devil's BG body is layout blocks; a piece that
flies off is a `map_set` to empty plus a sprite, a piece that lands is a `map_set` to a piece block; Must with H1, M7), and
any grid the Exhibitions need if they return. **F-GRID is deleted.** Vanilla's oil ignition keeps its logic, but its
repaint joins the queue through the `$3E:$DDFC` hook (`venues_b.md`; `systems.md`'s F.BLAST ignition rule).

---

## 6. Level and art pipelines

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
tileset  wind_a                   # a slot of the §5.3 table: assets/tilesets/wind_a/ (blocks, metatiles, chr sets)
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
  casual checkpoint 60 A0         # dormant object made live by a CASUAL poke (§5.5)
  script init=VA_GUST(1) pf=-

link 06.up -> 18                  # explicit-target exit (hidden room)
link 07.right -> S1:00            # section 1, screen 00 (Should)
casual 05 row=6 col=2 = 2C        # poke list entries (§5.5): casual / hard (Should) / 1993
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
6. **worst-case occupied object slots per screen ≤ 9** (R1.8, §15.1): the player, the screen script, 3 shots where the
   buster is allowed, the utilities the equipped weapons can place (`systems.md`'s caps), the most enemies alive at once
   (placements plus each director's declared child cap), effects, and any director not folded into the script;
7. block/tile budget report per tileset (blocks used / 256, BG tile ids used / 256);
8. every flippable metatile id appears in at most 8 cells per screen (§5.6);
9. every text trigger on a screen (TALK, NPC, plaque) fits that screen's glyph strip (§11.4); pop-ups are checked
   against the screen's free-id count and reported where they would be deferred.

Outputs: the ROM regions, `build/maps/<stage>.png` (the existing renderer), and the **free-id table** for the glyph
strip (§11.4): per screen, up to 2 runs of BG tile ids that neither the screen nor its scroll neighbours reference, plus
the ids free on the frozen view alone and the CHR source (bank, offset) behind every BG id on that screen, so borrowed
tiles can be restored from ROM. **The free-id scan runs before text v1a** (R1.14, scope-24): in M2 it first runs as a
stand-alone script over the 16 vanilla stages, and the level build then takes it over.

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

### 6.7 The art pipeline: minimal tools first [new-code] M · Must (R1.13)

No new art can reach the screen without these, so they are scheduled before any (R1.13, scope-6). `art_audio.md` §10
specifies their inputs and checks; tech builds and runs them.

| Tool | Does | When |
|---|---|---|
| CHR set table v2 (§7.6) | 8-bit source bank and stage-local ids, so CHR in banks above `$3F` is reachable | M2, before any new art |
| `tools/build/chr.py` | PNG ↔ 2-bpp CHR, de-duplication, the CHR set manifest and packer into the CHR banks (§1.2) | M2 |
| `tools/build/sprites.py` | the metasprite compiler of §7.5 (PNG + JSON → vanilla frame, layout and animation tables) | M2 |
| `tools/build/palettes.py` | palette sets and per-screen palette deltas; the checkpoint self-containment check (§6.3 check 4) | M2 |
| `tools/build/artcheck.py` | the art gate: sprite-set overlaps, palettes, the free-id map (§6.3), flicker, stream sizes, **weapon-slot sets ≤ 15 tiles** (R2.3; set pieces that change Rock's body use a set-piece player sheet streamed at a locked moment), the worst-case occupied slots per screen (§6.3 check 6) | M2 |
| `tools/build/bgboss.py` | BG-boss poses, deltas, hit boxes and streams | M7, before the H wings |

Art acceptance (R5.1): every milestone gate includes screenshots for the user, produced by the golden-movie runner
(§14.4).

---

## 7. Object / AI framework (families, slot plan, frozen handlers, player states, HUD widgets)

### 7.1 What exists [done by research]

23 slots × 29 arrays at `$03A0`; type tables `$3A:$82C9/$83C9/$84C9/$85C9`; init `$3A:$81F0`; the 6-byte AI header read by
`$EBD5` (anim, palette, CHR set, hit box, HP, attack); coroutines (`JSR $E46C` yield, `JMP $E45A` delete, `$E47B` end turn);
allocators `$E514` (shots), `$E59F`/`$E5AF` (enemies); the metasprite format (118/118 verified); the damage routines
(`rm6/engine.md` §1-2).

### 7.2 Free type ids and GP families [new-code] M · Must

Types with AI pointer `$0000` (clean): `$42 $7B-$7E $BA-$BF $CE $D7 $DB-$DF $F4-$FF` = **30**. `$CF` and `$D2` point at
filler and are listed free in `rm6/engine.md`, but `$D2` is also named as a Mr. X 4 part there: both stay reserved until
checked. The stage docs ask for far more object kinds than that (about 155 in the full design, about 100 in v1.0), so
**one type id per kind cannot work**. GP uses **families**: a type id plus a sub-id, the 4MI `$5E` pattern.

| Type | Family | Examples |
|---|---|---|
| `$F4` | GP enemy | venue and fortress enemies (Metslime, scorpions, Toppy seals, the Riot's rejects) |
| `$F5` | director / set piece | wave director (T1-lite), raster-band object, T3 switches and targets, gust zone, search spot, pendulums |
| `$F6` | pickup | bolts, chips, sponsor envelopes (R2.7), plates as pickups (PARTs only if the Could bundle ships) |
| `$F7` | event / NPC | commentator hooks, NPC talk, dialogue starters, debrief predicates, **the NPC Break Man** (§7.9), dormant CASUAL checkpoints (§5.5) |
| `$F8` | boss controller | GP bosses and reworked champions' controllers |
| `$F9` | boss part | hit boxes and segments (T8) |
| `$FA` | enemy projectile | |
| `$FB` | player-side GP object | GP shots for the weapon taps, the Ice Block (the slice's alt prototype, R2.4), the utilities of slots 4-7 (§7.12); later the alts and synergies |
| `$FC` | reserve | round 1's Break Man family, **dropped** (R1.12: he is a slot-0 variant, §7.9) |
| `$FD` | effect | swap flash, debris, WEAK! pop (art's 3-tile build in GP-COMMON; consistency-24) |
| `$FE` | DEV probe | test objects |
| `$FF` | system coroutine | the text runner (slot `$15`, §11.6) |
| `$42 $7B-$7E $BA-$BF $CE $D7 $DB-$DF` | single-purpose ids | handed out only when vanilla code tests a type id directly (as the tide moves type `$72`) |

**Per-sub-id record** (6 B, per family, in core bank `$3E`, ≤ 256 entries): AI entry (lo, hi), AI bank pair, sprite
bank pair, a GP flag byte (WRAP, NOPARRY, no sprite, persistent across deaths), and `FRZ_KIND` (§7.7). The 6-byte AI
header still sits in front of the AI entry and is read by `$EBD5` as usual.

**Dispatch costs nothing at run time**: the family's own entry in `$3A:$82C9/$83C9/$84C9` points at a small resolver, but
the init hook (`$3A:$81F0`, far fn 1, Y = type, X = slot) writes the sub-id's real AI address, bank (`$0441`) and sprite
bank (`$0458`) into the slot directly, so the object loop never sees the resolver. `$0458` is per slot already (the OAM
builder reads it per object, `rm6/engine.md` §1.5), so families are not bound to `$85C9`'s 16-type rows.

Spawning: level placements carry the sub-id (§7.3); child objects use `gp_spawn(family, sub, arg)` = `$E59F` (allocate),
write `GP_SUBID,X` / `GP_ARG,X`, then init. Plain `LDY #type / JSR $E5AF` keeps working for vanilla types. Player-side
objects use `util_spawn` (§7.12).

### 7.3 Object lists in WORK [new-code] S · Must

Vanilla lists are 4 parallel arrays with sentinels (`screen, X, Y, type`), sorted by (screen, X), read through zero-page
pointers `$74/$78/$7C/$7E` set by `$3A:$8032` from `$80BF/$80CF/$80DF` [code]. GP:

- **ROM format v2** adds two arrays, `sub` and `arg` (6 × n + 6 bytes); vanilla lists stay in v1 where they are.
- At stage or section load, the list is copied to WORK `$6600` (§3.4; v1 lists get zero `sub`/`arg`), and `$3A:$8032` is
  patched to load the count and pointers from 3 fixed WORK bytes (`LDA $80DF,Y` → `LDA LIST_N` etc., same length), so
  the spawner `$3A:$8120` and the kill bitfield `$0650` work unchanged.
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
- Ophis macros (`src/gp/ai.oph`): `YIELD`, `WAIT n`, `DIE`, `ANIM id`, `MOVE`, `SPAWN fam,sub,arg`, `TELL id` (queue a
  commentator line), `TALK id` (open a dialogue and wait for it, §11.6), `ONHIT` (read and clear the latch `$056C` through
  the damage routines `systems.md` picks), `DMGSTEP` (the standard damage step; declares `FRZ_KIND` STD, §7.7), the tier
  macros `IFHARD`, `IFCASUAL`, `TIERVAL` (§5.5), `MASH n` (the struggle helper, §5.5), and **`IFINTERACT`** (R2.10,
  design-21): true on an UP press (`$42` bit) with B not held (`$40`) and the 10-frame post-alt lock in `SYS_HOT` at 0.
  Doors, signs, NPCs, plaques and every UP-to-interact object use it, so no object reads UP on its own.
- **Frame-waiting code is a coroutine**: anything that waits for frames (TALK, CHOICE, NPC menus, fades) yields with
  `$E46C` from its own AI bank in stages (on menu screens, through the scheduler wait, §11.6) and never runs in the
  C-window (R1.4, §1.9).

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

Vanilla sprite banks have 1.2 / 2.3 / 4.3 KB of fill (`$20/$22/$24`); GP objects go in the new pairs `$4E-$53` (§1.2).

### 7.6 CHR sets: table v2 and the conflict check [new-code] S · Must

**CHR set table v2** (R1.13, scope-6; specified with `art_audio.md` §2.1). Vanilla's 4-byte entries carry a 6-bit source
bank (only banks `$00-$3F`), so no new CHR in `$54-$61` can load until this exists. It comes before any new art (M2).

- **Global ids `$00-$DE`**: vanilla's sets unchanged, plus GP globals in the free ids `$7C-$7F` and `$DF` (GP-COMMON, the
  text-window frame, the swap flash, two spares).
- **Stage-local ids `$E0-$FB`** (28 per stage), resolved through the table `SA.LOCAL_CHR` points to (§4.4). An AI header
  byte (AI-4), an exit's CHR byte or a checkpoint byte (`$0685`) that names `$E0+n` means "this stage's set n", so every
  one-byte format stays one byte.
- **Entry v2**: 5 bytes (count, PPU / 16, source offset / 16, **source bank (8 bits)**, flags: b7 PPU `+$1000`, b0 source
  `+$1000`). The loader `$C95C` reads v2 entries for local ids and for any global id whose v1 entry carries the escape
  pattern; vanilla's 4-byte entries keep working.

**Sprite CHR conflicts.** When the camera enters a screen, `$3A:$826F` queues the CHR set (AI-4) of each object type on
that screen unless it is in the 8-entry recently-loaded list `$07E8-$07EF`; the NMI drains the 8-entry ring `$07F0`
(`rm6/levels.md` §6). Two sets that overlap in `$1000-$1FFF` cannot share a screen. For families, the hook makes `$826F`
read the set from the sub-id's header. The build check: for every screen, the union of sets queued on it **and on the
screens the camera can reach without a transition** (sets persist), as PPU tile ranges; any overlap between sets used
together is an error, with the offending objects named. It also reports the per-screen free sprite tiles. For scale:
across 73 vanilla in-stage scenes only 11 sprite tile ids were never shown (`$3B-$3D $4D $4F $7D-$80 $8A-$8B`) [seen:
`sprtiles.py`], so the sprite table is effectively full and new enemies must replace, not add.

### 7.7 Collision, damage and frozen objects [new-code] S · Must

- **Numbers belong to `systems.md`**: damage tables, special cases, i-frames. Tech provides the hook points it lists
  (its §15.1) in the registry.
- **No punch re-class** (R2.1, feasibility-5). Vanilla attack bytes `$11-$14` stay, so the 21 enemy-AI latch compares
  feasibility found (`LDA $056C,X / CMP #$14` and kin) keep vanilla behaviour and are not patched.
- **The latch source** (consistency-20: `systems.md`'s definition is the source of truth). Where the shot-vs-enemy routine
  `$38:$8FDF` copies the attack byte into `$056C`, an inline `$7F` patch also writes `LATCHSRC,X` (WORK `$6080`) in
  systems' format: bits 0-4 the source column (BUSTER, CHARGE, PUNCH, PUNCH★, FIST, PARRY, the 8 weapons, BREAK,
  BREAK★, M.BEAM, HAZARD, RULE), b6 alt, b7 synergy. The column is derived at latch time from the shooter: a 256-entry
  `SRCTAB[type]` for vanilla shot types (the buster and punch types pick BUSTER / CHARGE / PUNCH / PUNCH★ by the attack
  byte), and the shot's own `GP_ARG` / `GP_OFLAGS` for family `$FB` objects, which carry their column and the alt and
  synergy flags. `LASTHIT,X` keeps the attack byte. Utilities that deal damage call `$38:$8FDF` themselves (R1.11), so
  they latch and attribute the same way.
- **Frozen objects keep taking damage** (R2.2, feasibility-6). `FREEZE,X` (WORK `$60C0`) counts frames. The **frozen
  tick** is an inline `$7F` patch in the object loop `$3F:$E438`, before the bank map: if `FREEZE,X` ≠ 0, decrement it and
  dispatch on the slot's `FRZ_KIND` (≈ 8 cycles per live slot when nothing is frozen):

| `FRZ_KIND` | Who | While frozen |
|---|---|---|
| 0 NOFREEZE | every type not listed below: BG bosses, big parts, custom damage steps | never frozen: Time Stop and the Ice Block do not set `FREEZE` on it, and it still takes hits normally |
| 1 STD | AIs whose per-frame damage step is `$E9D7` | the frozen handler runs `$E9D7`'s damage half (hit-flash bit `$03B7`, off-screen check `$E489`, latch → HP through systems' rules, SFX `$35`, death through the same `LDY #$17 / JSR $CB28`) **without the AI and without its yield**, then ends the slot's turn; the resume point is untouched, so the AI continues where it stopped |
| 2 STD2 | AIs using `$EA20` | the same, in `$EA20`'s order (the flash after `$EB76`) |
| 3 NODMG | AIs using `$EA6E` (immune: it clears the latch) | clear the latch, off-screen check, end the turn |
| 4 BOSS | bosses and controllers (family `$F8`, the reworked champions) | not skipped: the boss AI runs and reads `FREEZE,X` itself, a **boss-side frozen state** (hold the pose, keep processing GP_BOSSHIT). `systems.md` decides which freezes touch bosses |
| 5 CUSTOM | a GP sub-id with its own handler | a pointer in the sub-id record |

  Default kinds for vanilla types are **derived by the build** from a static scan of each type's AI for its damage-step
  calls. Round 2's census (`dmgstep.py`, JSR/JMP sites in all banks): `$E9D7` **134** (bank `$29` 65, `$30` 50, `$3B` 14,
  `$39` 3, `$31` 1, `$3F` 1), `$EA20` **18**, `$EA6E` **126**; `$EA80` (2 sites) and the punch-only `$EA99` (8) default
  to NOFREEZE. A type whose AI uses more than one step, or none, is NOFREEZE unless `systems.md`'s table says otherwise.
  GP sub-ids written with the `DMGSTEP` macro declare STD. `systems.md`'s NOFREEZE list overrides the derived kinds; the
  venue docs' NOFREEZE notes feed that list. The Ice Block in the Blizzard slice (R2.4) is the first user and the test.
- **Death-hook audit** (`systems.md` asks): a static scan for stores of the death types `$17`/`$25` into `$03A0,X` and
  for calls of `$ED42`, cross-checked with shadow6 coverage of every boss kill in the golden suite, lists every custom
  death path (M3).

### 7.8 RNG

Vanilla's RNG `$DF-$E1` is advanced every NMI (`$C88D`) [code], so it depends on lag. GP's **LFSR** (16-bit Galois, taps
`$B400`, in `LFSR`) advances only when called, is seeded at stage start from a per-stage constant (Time Attack fairness:
venues_a's quick-draw delay) and in normal play is mixed with the frame counter at the first input of the stage.

### 7.9 Player extensions, the `$9B` audit and Break Man [new-code]

Rockman is slot 0's coroutine (AI `$38:$802D`; resume points stand `$8055`, tiptoe `$808A`, walk `$80AF`, air `$810B`, pit
death `$8F13`, HP death `$8E7F`, `rm6/ram.md`). Everything here builds on that. **One attach state and one free-flight
vehicle state** serve every set piece (R1.10, scope-17); poses that change Rock's body come from a **set-piece player
sheet** streamed at a locked moment (R2.3, feasibility-8), never from the 15-tile weapon slot.

| Item | What | Tier · when |
|---|---|---|
| **GP player states** | GP code takes slot 0 over by writing `$0441` (its bank pair) and `$0413/$042A` (its routine), sets `$94` to a GP value (`$10+`), and hands back by writing the vanilla air or stand resume address. No dispatch hook. The base of every row below | S · Must, M3 |
| **X-WRAP** (`venues_b.md`) | a post-move hook on slot 0 (and on objects whose `GP_OFLAGS` has WRAP): in a locked room, X < `$08` becomes `$F0` and back, unless the row is flagged as an exit | S · Must, M3 |
| **X-BONK** (ceiling probe callback, for T6) | a hook where the player's upward collision stops the jump, passing the cell's collision type and position | S · Must, M3 (with T6) |
| **The attach state** | one record: parent slot, `dx/dy`, input rule (swing / shimmy / ride / none), release (A = jump with the parent's velocity; the parent's death = fall), weapon rule (buster only / none). Serves the vine and T5's pendulum (the pendulum is the vine's parent object, family `$F5`), Plant's balloon, Blizzard's condor, the claw and the arrow ride | M · Must, M5 (Plant first) |
| **The free-flight vehicle state** | 8-way movement without gravity, a per-vehicle speed table, a **lane flag** (none / lane), the buster mapped to the vehicle's shot, exits off until the ride's END. SKY ACE (Wind's sortie, with T1-lite) uses "none"; CANNON uses "lane" if the Exhibitions return | S · Must, M6 |
| **X-EXWP** (Yamato's pogo, `venues_b.md`; R3.2 keeps it) | a set-piece weapon: a GP player state with its own physics (bounce on enemies and spikes), taken from a rack object, dropped at the rack's partner | S · Must, M5 |
| **Pad history** (T7) | a 64-frame ring of `$40` in the player block (WORK `$7A40`), written by a 4-byte hook at the end of the joypad read `$3E:$C711`; the mirror object replays it with LEFT/RIGHT swapped. Flame's Shadow Rock is the one user (H3's Gemini uses its laser fallback, R3.1) | M · Must, M5 |
| **Exit type 7** (X-UPEXIT) | the exit handler table is 7 entries, `$39:$9A88` (lo) / `$9A8F` (hi), type 0 unused, handlers `$D587 $D612 $D540 $D5D1 $D653 $D6B3`, read at `$A290/$A295` (bank `$3A` mapped at `$A000`) [code]; the shutter tables follow at `$9A96`, so the table is relocated to `$3A`'s free space with room for types 7-9 and the two operands are patched. Type 7 fires when the player is rising, `Y < $0B`, and the cells above are open; it reuses the type-2 scroll-in (`$D82D`) with a small upward boost | S · Could |

**The `$9B` audit** (R1.12, feasibility-14) [new-code] S · Must. `$9B` is the current form (0 normal, 1 Power, 2 Jet).
SUPER as form 3 would overrun every table sized for 3 forms, so the `$9B` readers get the same static and coverage audit
as the `$51` readers, **before SUPER becomes form 3** (H3, M7). Round 2's census (`build/revise/tech/form9b.py`, output
`form9b.txt`; a static scan of the code banks `$29`, `$30`, `$31` and `$38-$3F`, and the research tour's coverage):

- **30 static reads, 18 executed** (16 in bank `$38`, `$3E:$CF92`, `$3F:$E105`), and 6 static writes (5 executed).
- **5 executed reads index a table**: `$38:$8153` → `$802A`, `$38:$84B5` → `$852E`, `$38:$95CC` → `$9614`, `$38:$9646` →
  `$96CD`, and `$3F:$E105 LDY $9B / ADC $E115,Y` (3 entries, running straight into `$E118`, as feasibility found).
- **One read computes a type id**: `$38:$964E LDA #$9F / CLC / ADC $9B / TAY / JMP $E526` spawns the form's effect object,
  types `$9F-$A1`; form 3 would spawn vanilla type `$A2`. It gets a 4-entry table pointing SUPER at a family `$FD` effect.
- The 12 static-only reads are classified by disassembly (code or data) in M0; any code site joins the list.

M0 records the census; M7 relocates each indexed table with a 4th (SUPER) row and patches its operand through the
registry, and a coverage movie must execute every reader with `$9B = 3`. `systems.md` owns what SUPER does; this audit
only makes form 3 safe.

**Break Man is a slot-0 character variant** (R1.12, feasibility-14) [new-code] M · **Should** (ships with the tag
partner, R0.3 item 2). Not an object: as an object every player-only routine (camera follow, screen exits, ladders,
shutters, pickups, contact damage `$38:$8F72`, pits, spikes, scripts that wait on the player's position) would need a
rewrite. As slot 0 they all keep working. The design:

- `CHAR` (player block, WORK `$7A00`): 0 Rock, 1 Break Man; the other character's HP is stashed beside it.
- The call (a pause-menu row confirmed with A, R2.10): Rock beams out with vanilla's teleport animation, `CHAR = 1`, the
  HPs swap, **his 2 KB sheet streams behind the beam-in** (§15.3), `$9B` is forced to 0 (no forms).
- Physics: a per-character constant table (walk speed, jump impulse, gravity, slide on or off). A static audit of the
  player code's speed and jump immediates in bank `$38` decides which sites read the table (part of the v1.1 sizing).
- His shield: a check in the player's hit path while `CHAR = 1` and airborne. Family `$FC` is dropped.

**The NPC Break Man** (R4.2, scope-15) [new-code] S · **Must**: an ordinary family `$F7` NPC sub-id with a composite
sheet of about 10 frames built from Rock's (visor, scarf, palette; `art_audio.md`'s), for cutscenes, the HALFTIME RIOT,
H5 and W3. No player code is involved. H5's Dark Man disguise is a 40-tile enemy-area set (feasibility-14; art's budget).

### 7.10 T3: switch → target [new-code] M · Must

Family `$F5`, two kinds of sub-id joined by a **channel** (the placement's `arg`, 0-15). WORK holds `CHAN[16]` (state bytes)
in the run block; channels that must persist across deaths are flagged in the stage data and saved in the map-edit log.

| Switch kinds | Target kinds |
|---|---|
| shot (any class, or one weapon class), touch, plate (standing on it, the vanilla class-2/5/9 platform contact `$38:$8F96`), key (consumes a per-stage key counter in the run block: venues_a's question 6), timer, all-of-N (counts channel hits) | door (UP to enter → exit with an explicit target), gate (a solid object, class 2/5/9, that slides away), wall (`map_set` + repaint, §5.6), warp (`$39:$89F5`), lift (rides through a down exit), spawner, palette/music change (CX's object `$40` idea) |

A target reacts on the frame its channel changes; every link is checked by the level build (§6.3).

### 7.11 T8: multi-part bosses [new-code] M · Must

The vanilla pattern (the gorilla tank `$50-$53`, the Wily Machine's `$E9` boxes, `rm6/engine.md` §1.4) as a library: the
controller (family `$F8`) sits in slot 8 and owns the boss bar (`$0642`); parts (family `$F9`) are glued each frame at
`controller + offset` (per-part offset tables), use class 0 hit boxes (shots pass through and latch, `$38:$9021`), and
forward their latch to the controller with a per-part multiplier, so systems.md's damage and i-frame tables still decide.
`part_spawn(offset, sub)`, `parts_glue()`, `parts_kill()`. Used by `venues_a.md`'s AYACO bomber and `venues_b.md`'s
Daruma (Yamato keeps the Daruma, R3.2), so it is Must from M5.

### 7.12 The object-slot plan [new-code] S · Must (R1.11)

R1.11 (feasibility-9). The vanilla shot allocator `$3F:$E514` searches slots 3..0 (`LDX #$03 / LDA $03A0,X / BEQ / DEX /
BPL`; slot 0 is always the player), and the enemy allocator `$E59F` searches `$15` down to 8 (`LDX #$15 ... CPX #$08`)
[code]. Round 2 measured what vanilla puts in 4-7 (`build/revise/tech/slots47.py`, static scan plus the tour's coverage):
slot 4 is Beat and Rush (`$38:$9661` spawns there; `$38:$8E6D` and `$903F` clear it), slot 6 hosts the underwater bubble
(type `$40`, AI `$3B:$9647`, spawned by `$38:$89DC` only while slot 6 is empty; executed in Centaur and Wily 3), and slots
5 and 7 are unused.

| Slot | Role | Allocator |
|---|---|---|
| 0 | the player (Rock; Break Man as a `CHAR` variant, Should, §7.9) | — |
| 1-3 | player shots: buster, weapon taps, the Ice Block in the slice; alts later | vanilla `$E514` |
| 4 | Beat's rescue (R1.11), Rush (vanilla), or one GP utility | `util_spawn`, last choice |
| 5, 7 | one GP utility each | `util_spawn`, first choices |
| 6 | one GP utility, else vanilla's underwater bubble (a utility there only pauses the bubbles) | `util_spawn`, third choice |
| `8-$14` | enemies, items, bosses (the boss or controller in 8) | vanilla `$E59F`, its `LDX #$15` operand patched to `#$14` |
| `$15` | the text runner (§11.6) | fixed |
| `$16` | the screen script (type `$80`), with directors folded in where possible (R1.8) | vanilla |

- **Utilities** (persistent player-side objects: the M.BEAM beam, a Wall Spear platform, the Ice Block, an Updraft
  column, the Centurion bot) take one slot each in 4-7 through `util_spawn(kind)`, which searches 5, 7, 6, then 4 and
  fails cleanly when none is free. At most 4 exist, minus Beat or Rush when out, minus the bubble underwater; **`systems.md`
  caps each weapon to fit** (e.g. M.BEAM max 2). Utilities that deal damage call `$38:$8FDF` (§7.7).
- Vanilla clears slots 1-7 when the pause menu closes and on death (`$38:$9624`: `LDX #7 / STA $03A0,X / DEX / BNE`,
  executed in the pause and game-over scenes), so utilities vanish on a pause, as Rush does. The GP per-slot arrays of a
  cleared slot are reset by the next spawn's init, so nothing dangles.
- Shots that need more than 3 slots at once (Petal Shot's 4, Feather Fan's 3 alongside the buster) are Should alts; when
  they return they borrow utility slots, as vanilla B.ATTACK uses 1-4.
- **Every occupied slot counts in the lag cap** (§15.1), utilities and the text runner included.

### 7.13 The HUD widget module [new-code] M · Must (R1.10)

**One module, data-driven** (R1.10, scope-16), for the ~15 counters and meters the stage docs specify separately
(X-METER, X-LABEL, F-CLOCK, H1's score balls, Knight's keys, the Riot's auditions, the LOOP icons and POW states, the
low-fuel pip, …).

- **Widget record**, 8 B (WORK `$62C0`, 8 records): kind, X, Y, value source (WORK address lo/hi), max or digit count,
  tile base (GP-COMMON or a stage set), palette and flags (b7 visible, b6 blink).
- **Kinds**: DIGITS (2-4 digits; with tenths it is F-CLOCK), LABEL (a 4-tile word: ZONE, PASS 1/3, ACE 100%), METER (a
  bar of up to 8 units, vertical or horizontal: the bonus timer, fuel), ICONROW (up to 8 icons: LOOP, POW, letters).
- **Drawing**: sprites appended by a hook after the OAM builder's object pass. Budget: ≤ 4 widgets, ≤ 12 sprites, ≤ 6 on
  one scanline (art places them; artcheck checks them).
- The stage's `HUD_ID` (§4.4) lists its widgets; set pieces show and hide them by index.
- **"Collect N" secrets** (at most one per stage, R3.1) count in `meta.md`'s stage counter (the `$4n` debrief predicate,
  run block) and show it with a DIGITS or ICONROW widget, so a new counter costs data, not code.

---

## 8. The generic raster list [new-code] M · Must

### 8.1 Format

Double-buffered, **24 bands per buffer** (R1.9; feasibility-15 and its decision 13), struct-of-arrays in WORK
(`$6400-$65DF`); buffer A = index 0-23, buffer B = 24-47. Game code builds the **staging** buffer at any time; the NMI
swaps buffers (no copying) when `RL_FLAGS` b7 is set, the 4MI commit rule (`r4mi/engine.md` §4.2) without 4MI's copy
loop.

| Array | Field | Meaning |
|---|---|---|
| `$6400,X` | `LINE` | absolute scanline 1-239 at which this band starts; `$FF` ends the list |
| `$6430,X` | `OPS` | b0 write PPUADDR (`$2006` hi/lo), b1 write scroll (with b0: the 4-write `$2006/$2005/$2005/$2006` split that sets X, Y and nametable), b2 PPUCTRL, b3 PPUMASK, b4 `$5105` (nametable mapping: window bands), b5 call the sound update after this band, b6 call a band routine, b7 palette swap (rendering off, 4 BG colours, rendering on: **only allowed in the last band**, §8.4) |
| `$6460,X` / `$6490,X` | `HI` / `LO` | PPUADDR, or the two precomputed `$2006` bytes of a scroll split |
| `$64C0,X` | `SX` | fine/coarse X |
| `$64F0,X` | `SY` | Y for scroll splits |
| `$6520,X` | `CTRL` | PPUCTRL value |
| `$6550,X` | `MASK` | PPUMASK value (4MI's water tint and sprite-free bars, CX's effect 8) |
| `$6580,X` | `ARG` | band-routine index and repeat count, or the palette set of a b7 band |
| `$65B0,X` | `MAP` | the `$5105` value of a b4 band |

10 arrays × 48 = 480 B; the compositor's inputs sit in `$65E0-$65FF` (§3.4).

### 8.2 The walker

In `$7F` (fast, no window switch). NMI: if the staging flag is set, flip `RL_BASE`; `RL_CUR = RL_BASE`; `$5203 =
LINE[RL_CUR]`; `$5204 = $80` (or 0 for an empty list). IRQ: `LDA $5204` (ack), load band `RL_CUR`, do its ops in the
order CTRL → `$5105` → PPUADDR/scroll → MASK (the order 4MI and CX use), increment the cursor, arm the next `LINE` or
disable, run the band's routine and sound flags, RTI. ~70-90 cycles per band. **Band routines live in `$7E/$7F`**, never
in the C-window (R1.4). A per-line effect is a band routine that keeps the cursor on its band and re-arms itself
(`$5203` = current + step, `ARG` times), like vanilla handlers 9 and F.

### 8.3 Presets that replace the 27 chains (M2), and the new ones

| Preset | Bands | Replaces | Used by | Tier |
|---|---|---|---|---|
| `RL_FLOOR(line, addr, scroll)` | 1 | 7, 1A, 19 (with drift in `irq_logic_tick`) | Plant 0E, Mr. X 2/3, Wily 2, Wily Machine; BG bosses (H wings) | Must |
| `RL_SHIP(...)` | 3 | 1-2-3 | Blizzard ship (`venues_b.md` keeps it). Its effect thread (thread 3 at `$3E:$D4BF`) gets a hook where the roll changes direction that sets `SHIP_TURN` in the run block, so `venues_b.md`'s icicles shake loose on the turn ([new-code] S, with the slice) | Must |
| `RL_PARALLAX(line, divisor)` | 2 | C-D | Tomahawk, `venues_a.md` T4; W2/W3 parallax | Must |
| `RL_SHIMMER(line, n)` | **2** | E-F-10 | Tomahawk sunset. Entry 1 resets the scroll at `line`; entry 2 is a self-re-arming routine that alternates the X scroll every 2 lines, `n` times (vanilla n = 20), so the preset never costs 21 bands (R1.9, feasibility-15b) | Must |
| `RL_CEILING(h)` / `RL_TIDE(h)` | 2 | 11-12 / 14-15 (logic in `irq_logic_tick`, §1.8) | Knight, Centaur; Yamato's nightingale floor (R3.2) | Must |
| `RL_MULTI(...)` | 2 | 16-13 | Mr. X 4 machine, reveal (legacy ids) | Must |
| `RL_WEAPONGET` | 2 | 17-18 | YOU GET | Must |
| `RL_MENUSLIDE` | 2 | 4-5 | adaptor change (`systems.md`'s quick swap skips it; the docking cutscene plays once per form per save, R2.3) | Must |
| `RL_STORY` | n | 8-9, A-B | vanilla opening (legacy regression only) | Must |
| `RL_SOUNDPLAYER` | 1 | 0 | the bank-`$28` debug sound player, **kept as a preset** (R1.14, feasibility-21) for a VAULT if one ever ships | Must (data) |
| `RL_WINDOW(top, rows)` | 2 | new | the pop-up (top) and the dialogue window (bottom), §11.3; its first band also flushes the ExRAM queue | Must |
| `RL_FLUSH` | 1 | new | a 1-line band at line 8 that flushes the ExRAM queue when no window is open (§3.3) | Must |
| `RL_BANDS(list)` | ≤ 6 | new | `venues_a.md` T4 rides, T1-lite (§9.1) | Must |
| `RL_FLOOR8(...)` | 8 | new | W3's programmatic floor with the Mode-7 joke (R3.6) | Must |
| `RL_SPLIT_PT(line)` | 1 | new | the pattern-table split for menus (BG from `$1000` below a line, `art_audio.md` §2.8); never in stages | Must (M5) |
| `RL_PALBAND(line, set)` | 1 | new | one bottom palette band (W2/W3 "SUPER colour", R1.3); last band only | Must |
| `RL_FLOOR16(...)` | 16 | new | W3's 16-band floor with drive-toward-camera sizes (F-SIZES) | Should (R3.6) |

A **band compositor** merges the stage's preset, the window bands and any director-object bands by line, and writes the
staging buffer once per frame. Priorities: window and flush bands first, then the stage preset, then director bands;
if more than 24 are asked for, the lowest priority band is dropped. CX's trick of an invisible object whose position gives
a band's line and height (`cx/engine.md` §8) is family `$F5` sub `BAND`. **Each stage doc records its band budget per
scene** (scope-5): window (2) + the stage's bands ≤ 24. W3's fight, for instance, is `RL_FLOOR8` + 2 window bands = 10
(consistency-27 resolved by R3.6's 8-band floor).

### 8.4 Rules

1. **Rendering-off writes end the list.** MMC5 counts scanlines only while the PPU renders; a palette swap (rendering
   off) resets its counter, so no IRQ can follow in that frame. Palette-swap bands are therefore last (the bottom
   dialogue window or `RL_PALBAND`); a top pop-up uses one of the stage's own BG palettes. E3's two-colour cellophane
   (Could, with the Exhibitions) uses BG attribute palettes, not two palette bands (feasibility-15c).
2. **Sound in the IRQ** (R1.9, feasibility-15d). Vanilla's reason is kept: when the list has a band above line 112
   (`$70`), the NMI skips the sound update so it cannot delay an early split. The update then runs at the end of **the
   first band followed by ≥ 36 band-free lines** (the update is 3,700-3,900 cycles ≈ 33 lines). If no band qualifies,
   the compositor drops the lowest-priority band in the way. With no band above line 112, sound stays in the NMI.
3. Lag frames re-arm the same list (vanilla's lag path `$C0C4` does the same for chains).
4. Line budget: a band's writes must land in h-blank; the walker is calibrated once against vanilla splits (§14.4). The
   ExRAM flush (≤ 32 B, ≈ 260 cycles) runs after the band's split writes, never before.

### 8.5 The palette-flash and lighting service [new-code] S · Must (M6)

Every full-screen or large-area flash in the game goes through `pal_flash(kind, frames)`, so R3.5's rule (design-13) is
enforced in one place. In the default FLASHES mode the service rate-limits large flashes to **3 per second** (a request
inside the window is merged into the running one); in REDUCED every flash becomes an 8-frame fade. The HALFTIME RIOT's
"lights on a timer" (R3.1: the one timed dark-room set piece) is a palette blackout plus a PPUMASK band driven by the same
service, as is any other stage darkness its owner keeps (Centaur's black zone). The health notice at boot is
`meta.md`'s screen; the quick-draw windows and the INPUT LAG offset are `systems.md`'s numbers.

---

## 9. Autoscroll (T1)

### 9.1 T1-lite: fixed-camera rides [new-code] M · Must (M6)

Accepting venues_a's proposal (its §0.4 and open question 1): **the camera is locked** (screen-script mode 0, vanilla),
**raster bands scroll by time** (and by camera for parallax) through `RL_BANDS`, and a **wave director** spawns enemies
from a list `[frame, family, sub, x, y, path, arg]`, counted from the screen lock so every run is identical (golden
movies, Time Attack). Nothing solid moves, so collision, spawning and exits stay vanilla. The ride ends at
the list's `END` entry, which unlocks the screen (mode 1).

- In a locked room the director may switch `$FB` to vertical mirroring (two nametables side by side) so band art loops
  every 512 px instead of 256; the exit restores it.
- **The director lives in the slot-22 screen script** (R1.8): the script switches its own bank pair to the director's
  GP bank, as §6.6's waiting routines do, so the director costs no slot. Family `$F5` sub `WAVES` remains only for a
  room whose script is already busy.
- **Cap**: the player, the script, 3 shots and the director's live children count against the 9-slot cap (§15.1), so a
  ride has **at most 4 enemies or enemy shots alive** until M3's re-measure. Round 1's sortie budget ("5 planes + 2
  bullets + 3 shots = 10", feasibility-4) is re-cut by `venues_a.md` to fit. The player rides in the free-flight vehicle
  state (§7.9).
- Used by: Wind's sortie (01) and wing arena (1D), Tomahawk's train (10-11) (venues_a). venues_b's ski run needs none (a
  forced-slide floor type, X-FLOOR).

### 9.2 T1-full: forced horizontal scroll [new-code] M · Won't (v1)

No venue needs terrain that moves (consistency decision 37), so this is Won't (v1). The design is kept for a later
version:

- a speed (8.8) and flags in WORK are set by a script init; the camera-follow step in the horizontal scroll routines
  (`$3E:$DCE2` right / `$DD42` left, `rm6/levels.md` §5) uses `camera += speed` instead of following the player; the
  column painter runs unchanged as the camera crosses 8-px boundaries.
- The player is pushed by the existing left clamp `$A8` (camera-relative, `$10`, `$38:$8F31`) and stopped by a new right
  clamp (`camera + $F0`). **Crush**: pushed by the clamp while a wall blocks him on the left → the pit-death path
  (`$38:$8F13`).
- Every screen in the run is mode 3 (free); the last screen's script clears the speed.
- Vertical autoscroll: **Won't (v1)**; vanilla scrolls vertically only during scripted transitions.

---

## 10. Per-position destructible tiles (T6) [new-code] M · Must (M3)

Vanilla breakables are **one bit per metatile id** in `$0340` (all blocks sharing the id open together; only the full punch
`$14` or F.BLAST), so they cannot break one cell of an ice floor (`rm6/SUMMARY.md` §1.6, lesson 6).

**Design: rewrite the RAM layout with authored variant blocks, through the map-edit service (§5.6).** This is the only
T6 (R1.10, scope-10): round 1's bitmap fallback is dropped.

1. **Mark**: metatile attribute **bit 2** = DESTRUCT (bits 2-3 are 0 in every metatile of every vanilla stage [code]).
   Collision ignores the bit.
2. **Author**: the tileset tool expands every block that contains DESTRUCT metatiles into its **variants** (each subset
   of those quadrants replaced by the tileset's RUBBLE metatile, usually air): 2^k − 1 extra block ids for k breakable
   quadrants, plus a **transition table** `(block, quadrant) → block`: in ROM 512 B per slot (a 256-B block index and up
   to 64 breakable source blocks × 4 quadrants, §5.3), copied to `$9200` of the TILES page. A floor block with 2
   breakable cells costs 3 ids; the build reports the total against the 256-block budget.
3. **Break**: a trigger calls `t6_break(x, y)`: venues_b's head-bonk X-BONK (a callback on the player's ceiling probe),
   a weapon class hit, or the punch. It finds the layout byte and quadrant, looks up the transition, writes the new block
   id through `map_set` (which logs the old byte, §5.6), spawns debris (family `$FD`), and queues the repaint.
   **Collision changes on the next probe**, because `$DA6C` reads the RAM layout.
4. **Repaint**: CELL entries of the map-edit queue (one per broken quadrant), within its 4-cells-per-frame budget. At
   most one break starts per frame; more are queued.
5. **Refill** (venues_b's Ice Climber floors): `t6_refill()` writes the logged byte back and repaints.
6. **Persistence**: broken cells survive deaths and reset at the next stage start (vanilla breakables' rule); a stage flag
   can refill on respawn instead.

**The bitmap is dropped** (R1.10): it would have patched the three hottest level routines (`$DA6C` and both painters;
collision alone is 7 % of the frame, `rm6/engine.md` §8). A venue that runs out of block ids gives up breakable cells
instead.

---

## 11. Text engine [new-code] L · Must

R1.4 (feasibility-10, feasibility-11, consistency-3) fixes the model: **a fixed-cell glyph cache in an ExRAM window**,
EN in ALL CAPS, JP kana, no VWF; pop-up 2 × 28 cells with ≤ 24 glyph ids; dialogue, debrief and help pages 4 × 28;
borrowed BG tiles restored from ROM; TALK, CHOICE and every frame-waiting UI as yielding coroutines; dictionary
compression Must; v1a before the slice, v1b before Knight. `story.md` owns every word and the writing rules; this section
owns the engine and the compiler.

### 11.1 Two engines

| Engine | Surfaces | Notes |
|---|---|---|
| **Vanilla PPU scripts** (`$3C:$8631`, 168 scripts, typewriter via `$069F/$06AC/$06A6`) | boot and license, YOU GET, the boss panel (`$3C:$81B1`), the CAPCOM TIMES driver (`$3B:$A886`), the staff roll, TO BE CONTINUED | kept with their fonts and quirks (`story.md` §10.1); a language hook picks EN tables (§11.2) |
| **The new engine** | every GP sentence: pop-ups, dialogue, the debrief, help pages, NPC menus, plaques and crawl pages | §11.3-11.8 |

### 11.2 The language hook and the boss panel [new-code] S · Must

- **Language hook** at **`$3C:$8636`**, where the interpreter reads the script pointer from `$8787/$882F`
  (`rm6/text.md` §8). Tech is the source of truth for this address (consistency-41); `meta.md` and `story.md` cite
  `$8636`. It picks the pointer table by `LANGUAGE`. EN scripts live in a GP text bank, so the interpreter (~370 bytes)
  is copied into that bank pair and reached through `FAR`; the far-call slot table `$CB5F` (4 slots, all used) is not
  touched. GP replaces almost all of vanilla's JP-only scripts; the hook serves the few kept (the newspaper's last pages
  `$95/$96` with EN versions added; `story.md` §10.4). Line breaks are command addresses, so EN layouts are re-flowed by
  the encoder (`rm6_ppuscript.py` already encodes `row, col, "text"`).
- **Boss-panel extension** (`$3C:$81B1`, M5): panel records indexed by fight id (`SA.FIGHT_ROW`, meta's fight table)
  instead of `$51`, a 10th field (`$0624` starts at 9), and a re-type entry for Dark Man's lying panel (`fortress.md`).
  The panel stays English in both languages, as vanilla.

### 11.3 Windows

- **Nametable**: ExRAM in mode 0 (§3.3). A window's first band (`RL_WINDOW`) sets `$5105 = $AA` (all four slots →
  ExRAM) and points the scroll at the window rows; its second band restores the stage's mapping and scroll. No vanilla
  nametable byte is touched, so the playfield never needs repainting. The first band also flushes the ExRAM queue.
- **Pop-up** (live, the world keeps running): **top of the screen by default** (consistency-26: pits stay visible and the
  bottom band stays free for palette swaps); at the bottom only where `SA.EFFECTS` b6 says so, i.e. where the top is a
  raster set piece (Wind 01, Tomahawk 10-11). 4 rows (border, 2 text rows, border), lines 8-39 at the top. Columns 0-1
  hold the **16×16 face icon** (4 BG tiles, R5.1), columns 2-29 the **28 text cells**, 30-31 the border. Sprites stay on
  (the life bars). The palette is one of the stage's BG palettes, chosen by the build for contrast (no swap at the top,
  §8.4).
- **Dialogue, debrief and help pages**: the bottom window, 6 rows (border, 4 × 28 text, border). Its band swaps BG
  palette 3 (rendering off for 1-2 lines at the border, the CX effect-10 trick, `cx/engine.md` §3.2); the NMI restores it
  from the `$0360` buffer while the window is open. The band turns sprites off (PPUMASK).
- **Full-screen pages** (plaques, the crawl, scene cards): ExRAM rows 0-29 as the whole screen, up to 9 × 28 cells.
- **Knight's battle log** uses the pop-up window, with the commentators muted (consistency decision 28).

### 11.4 The glyph cache

- **Glyphs**: 1-bpp 8×8 in a text bank, about 240 of them (≈ 2 KB): Latin capitals, digits, `. , ! ? ' " : ; - / & %
  ( ) ★ ♥ ♪ β × ▶ ・ …`, hiragana and katakana with voiced and semi-voiced forms precomposed (one cell each, unlike
  vanilla's separate `゛`), small kana, `ー 「 」 『 』 、 。 ~` (`story.md` §10.2). **EN is ALL CAPS** (no lowercase set;
  art's mixed-case set is dropped). **JP is kana only**: no kanji (consistency decision 5).
- **Cells are fixed**: 8 px, one glyph per cell. The VWF is dropped (R1.4).
- **Per page**, the compiler emits the list of the page's distinct glyphs. On open the runner renders each into a strip
  tile (1-bpp → 2-bpp in the window's two colours, 16 B a tile) into the staging buffer, streams it (§15.3), then writes
  the cells, as strip tile ids, into the ExRAM queue. `*word*` highlights use the second colour.
- **Strip sizes**: a pop-up uses **≤ 24 glyph ids + 4 icon tiles = 28 ids** (≤ 448 B, 3 frames of stream); dialogue,
  debrief and help ≤ 96; full-screen pages ≤ 128. The compiler splits pages to fit (story measured a median of 12-13
  distinct glyphs per pop-up page; about 1 JP page in 12 needs a split).
- **Where a pop-up's strip comes from** (live): the screen's free-id table (§6.3), up to 2 runs of BG ids that neither the
  screen nor its scroll neighbours reference. ≥ 28 free: icon and text. 24-27: text with the name label only. Fewer than
  24: the line waits in the announcer queue (max age 8 s) until a screen with room, a death, a respawn or a boss intro
  (boss rooms reference only 52-195 BG tiles, `art_audio.md` §1.4). Deferral is accepted except for P1 lines, shown on
  READY when the screen is quiet (consistency decision 36).
- **Where a dialogue's strip comes from** (world frozen): the ids **the frozen view does not reference** above the window
  (a per-screen list from the build, far larger than the live set). Scroll neighbours may use them, so they are
  **borrowed, and restored from ROM on close**: the build knows every screen's CHR state (the source bank and offset
  behind every BG id), and the runner re-streams the borrowed tiles from there (16 B a tile; 96 tiles = 1.5 KB, 8-12
  frames while the window closes). **No read-back buffer** (R1.4, feasibility-11). A page that needs more glyphs than its
  screen's frozen view frees fails the build (§6.3 check 9), and the compiler splits it.
- **Menu screens** (the judges' desk, the bracket, the pit stop, the pause CHIPS page) have their own CHR; the build
  measures their free ids (the pause menu has 108 free BG tiles, `art_audio.md` §9.7).

### 11.5 Pages, dictionary compression and the compiler

- **Source**: `story.md`'s `text/*.tsv` (`id, surface, speaker, EN, JP, ENGRISH, max_lines, notes`). ENGRISH is Could
  (a sparse override table that falls back to EN).
- **Byte codes**: `$00-$EF` glyph ids; `$F0-$FF` controls:

| Code | Meaning |
|---|---|
| `$F0` | NL |
| `$F1` | WAIT for A/START (START skips the rest of the window) |
| `$F2` | CLEAR |
| `$F3 n` / `$F4 n` | PAUSE n frames / SPEED n |
| `$F5 id` | SPEAKER: face icon, name label, blip |
| `$F6` | highlight on/off |
| `$F7 v` | VAR v: print a variable at its reserved width (`%N%`, `%T%`, `%TIME%`, `%NAME%`, …; CX's NUM) |
| `$F8 n ids…` | CHOICE, 2-4 options; result in A and carry |
| `$F9 n skip` | SKIPIF n (branch on the last CHOICE; CX `0C`) |
| `$FA f skip` | IFFLAG f (branch on a LIVE FILE flag) |
| `$FB id` | CALL id: a routine from a fixed table (give an item, start a fight through the fight loader, set a flag) |
| `$FC i` / `$FD i` | dictionary entry i / 256 + i |
| `$FE` | CLOSE |
| `$FF` | END |

- **Dictionary compression** (Must, R1.4). Per language the compiler picks up to 512 frequent substrings (2-12 glyphs)
  by greedy savings over the whole table and replaces them with the 2-byte codes `$FC/$FD`; the dictionary (≈ 3 KB per
  language) sits beside the decoder's tables. It is measured on story's v1.0 strings at text v1a (M2), before the bank
  allocation freezes (consistency-4).
- Each page has a header: window kind, line count, the distinct-glyph list. A 16-bit string id table per language holds
  3 bytes per id (bank, address); a page never crosses a bank.
- **Compiler checks** (`story.md` §10.3): 28 cells per line; pop-up ≤ 2 lines, dialogue, debrief and help ≤ 4; glyph
  sets per surface (vanilla-font surfaces: the pause font's D/Q/Z and `ZERO_O`, the bracket's missing punctuation);
  variable widths; every id has EN and JP; **the release build fails on `WIP`, `TODO`, `TBD`, `XXX`** or an empty credit
  field.
- **Size**: v1.0's ≈ 350 Must strings (R4.5) in two languages, compressed, plus glyphs and dictionaries ≈ 30 KB: text
  banks T1-T4 (§1.2). The full design (≈ 1,100 strings, 70-90 KB before compression) needs the 9 banks after
  compression.

### 11.6 Execution: coroutines, never the C-window (R1.4, feasibility-10)

- **The text runner is a coroutine** (family `$FF`, slot `$15` in stages, §7.12). It yields with `$E46C` every frame from
  its AI bank pair. The typewriter, TALK, CHOICE and NPC menus all run in it.
- The C-window holds only **non-waiting services**, called by the runner through CW: `page_decode` (dictionary expansion
  into the decoded-page buffer, WORK `$6D00`), `glyph_render` (n glyphs into the staging buffer), `strip_alloc` (strip
  ids from the free-id table), `exq_put` (cells into the ExRAM queue).
- **Pop-ups** (`TELL id`): queued in the run block (16 entries) by the commentator bus (§11.7). The runner takes slot
  `$15` when a line is due **and the screen is below the 9-slot cap**; otherwise the line waits, so a pop-up never pushes
  a screen into lag (§15.1). The world keeps running.
- **Dialogue** (`TALK id`): the caller (an NPC, a script) starts the runner and yields until it signals done. **World
  freeze**: `GP_HOT` b1 makes the object loop skip every slot except `$15` (one more test in the frozen tick's inline
  patch at `$3F:$E438`, §7.7; the OAM builder still draws them all), and threads 1-2 are suspended as the pause menu
  does (`$22`/`$23` = `$80`, `rm6/ram.md`).
- **Menu screens** (the bracket, the desk, the pit stop, pause help pages) run in a scheduler thread (`meta.md`'s code);
  their text calls run the same runner logic, which waits through the thread wait `JSR $C62B` (one frame; `$C5F6` with
  A frames) [code: `$3E:$C5F6-$C62B` saves `$10`, the banks and S, then returns to the scheduler]. Either way every wait
  passes through vanilla's scheduler, so `$F2` clears and the NMI uploads glyphs and reads the pad every frame: the
  lag-frame trap of feasibility-10 cannot occur.
- **Typewriter**: CONFIG TEXT SPEED (2 / 1 / 0 / 4 frames per cell, `meta.md` §11.1), a per-speaker blip (vanilla's
  `$06A6` mechanism), free spaces.

### 11.7 The commentator event bus [new-code] M · Must (M3)

Hooks raise events: `EV_DEATH` (with the cause byte, from the player-death hook site), `EV_WEAK_FIRST` (GP_BOSSHIT's
first weakness hit), `EV_SECRET`, `EV_PLATE`, `EV_RESPAWN_HECKLE` (P1) and stage hooks. The bus picks a line from the
stage's table (`SA.COMM_ID`; `story.md`'s lines, 4 death lines per stage in v1.0, R4.5), rotates it, applies per-event
cooldowns (run block) and the ANNOUNCER setting (on / deaths only / off), and queues a `TELL`. P1 lines jump the queue
and show on READY. `story.md` owns every line; the WEAK! pop and stagger are `systems.md`'s.

### 11.8 Text v1a and v1b

| Version | Contents | When |
|---|---|---|
| **v1a** | the ExRAM window, `RL_WINDOW`/`RL_FLUSH`, the glyph cache, the compiler with dictionary compression, the pop-up runner, the debrief and help windows on menu screens, the language hook, EN and JP | M2, before the Blizzard slice, after the free-id scan (R1.14) |
| **v1b** | dialogue in stages with the world freeze and the ROM restore, CHOICE, NPC menus (Knight's command window), full-screen pages | M6, before Knight |

**Portraits** (32×32, 16 tiles, a `PORTRAIT` control) are **Should** (R5.1): v1.0 uses the 16×16 face icons and name
labels. The icons are `story.md`'s 7 speakers, Light as a radio frame (consistency-40).

---

## 12. Sound

### 12.1 What exists [done by research]

Requests through `$DC` into the ring `$B0-$BF`, serviced at `$3E:$C8C1` (`$8003` play, `$8000` update); 102-entry big-endian
table `$34:$8A40` (36 music, 65 SFX, commands `$F0-$F7`); data in a 24 KB sound space (`$34`, `$35`, and `$36` through the
reader `$34:$803A`); the channel command set `$00-$18` decoded (`rm6/engine.md` §5.3); `songdec.py` decodes any track. Free:
449 B at the end of `$36`, **reserved for SFX** (R1.14: `art_audio.md`'s Must SFX, never a general allocator seed); ids
`$1A` (empty stub) and SFX `$3D/$3E/$4D/$51` (never requested) can be recycled.

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
| `@ n` | `08` instrument (8-byte entries at the table `$34:$8A41` points to; a relocated, larger table is D3, Should) | |
| `o n` | `09` octave | |
| `K n` / `k n` | `0A` global transpose / `0B` transpose | |
| `D n` / `s n` | `0C` detune / `0D` slide | |
| `[ … \| … ]n` | `0E-11` loop 1-4 / `12-15` break 1-4 | 4 nesting levels |
| `L` | `16` jump (loop point) | |
| `!` | `17` end | |
| `w n` | `18` duty | |

Sound effects keep vanilla's format (priority byte + register stream, player `$34:$8251`) and are written as YAML register
frames. **Round trip test**: `mml.py decompile` turns all 36 vanilla music ids into MML and `compile` must give the same
bytes; it gates the compiler (M0). New stages reuse vanilla tracks until their songs exist; every Should track has a
vanilla fallback (`$0B`, `$18`; R5.2).

### 12.4 Budget

`art_audio.md` owns the one track list and its byte budget (R5.2); tech owns the banks. Music and SFX get **5 banks**,
`$75-$79` (R1.5; round 1's "16 banks (`$70-$77` + `$0B-$0F`)" was 13, consistency-41). v1.0 needs about one: G00-G04,
the ending's lights-out arrangement (2A03 stems), a 2-second whistle jingle (R5.2) and the track table v2; the Must SFX
sit in the `$36` tail: **21 new Must SFX in 392 of its 449 B** (`art_audio.md` §12.8; 57 B spare), confirmed, so the SFX
player needs no new reader. Of `art_audio.md`'s driver items, D1, D2, D4, D6, D9 and D11 are Must (M1-M2); new songs use
the 71 vanilla instruments until D3 (the instrument table moved, Should) lands. The full design (≈ 29.6 KB, all tiers)
uses `$75-$78`; **`$79` stays spare**, the donor if text needs a tenth bank (R8.7).

### 12.5 MMC5 pulses [new-code] M · Could

A **second driver instance** for the two MMC5 pulses: the M0 disassembly of `$34:$8000-$8A3F` (2.6 KB) becomes Ophis source
with symbolic RAM and register bases, assembled twice: once in place (4 channels, `$4000`, vanilla RAM `$0700-$07EF`) and once
in a GP bank (2 channels, `$5000-$5007`, state in WORK `$6F00`). A `COMPANION[id]` table names the 2-channel stream that
starts with a track when CONFIG "MMC5 AUDIO" is on; both instances tick in the same update call with identical tempo
commands, so they cannot drift. `$5015` is set only when the config is on (BRIEF §5.7: MMC5 audio on/off; music must stand on
the 5 core channels). With it (D7, `art_audio.md`): 4MI's charge-shot loop on MMC5 pulse 1, so the charge never steals a
music channel (`r4mi/engine.md` §9.2).

**Reading R1.3 with R5.2.** R1.3 lists "the MMC5 audio" in v1.0's SUPER colour, while R5.2 and BRIEF §9 keep MMC5
arrangements Could. This doc takes the conservative reading: v1.0's audio part of SUPER colour is the channel drop
(§12.6, Must), and the MMC5 pulses join it if they ship.

### 12.6 The channel mute mask (D9) [new-code] S · Must

R1.3 and R5.2 make D9 Must (scope-3: the lights-out ending needs it). `MUTE` (hot RAM `$06DC`, read by the driver inside
interrupts) has one bit per **music** channel: b0 pulse 1, b1 pulse 2, b2 triangle, b3 noise, b5-6 the MMC5 pulses (if
they ship). In the reassembled driver (§14.2) the channel output step writes silence for a masked channel (volume 0 for
the pulses and noise, `$4008 = $00` for the triangle) while its stream keeps advancing, so unmuting re-enters in time.
SFX are not masked: an SFX on a muted channel still plays. Users: the ending's LIGHTS OUT (`story.md` S42: the channels go
out one at a time and **the last sound is pulse 1 alone**, R4.1), and the "music channel drop" of W2, W3 and the escape
(R1.3). Cost: one `AND` per channel per update.

**DPCM**: none in v1 (consistency decision 36). If a sample is ever added, it lives in `$7F` (R1.14), because the
C-window switches `$C000` and DPCM fetches from `$C000-$FFFF`.

---

## 13. Saves (implementation; the format is meta.md's) [new-code] S · Must

- **Where**: page 0 (SAVE), meta.md's map at page offsets `$0000-$1A1F` (SYS-A/B, FILE1-3 A/B, test mailbox `$1A00`).
  **Changed from meta.md's table**: the LIVE FILE and LIVE SYS images sit in **page 1 (WORK)** at the same CPU addresses meta
  gives (`$7400-$75FF`, `$7600-$79FF`), because WORK is the page mapped at `$6000` during play; page 0 offsets
  `$1400-$19FF` become reserve. `meta.md` accepted this (consistency decision 37).
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
text, sound, sprites, CHR → header → `build/r6gp.nes` + `build/r6gp.bps` + `build/r6gp.map` (symbols), and prints the
**bank ledger** (§1.2: role, owner and bytes used per bank, total 1,024 KB) and the **WORK ledger** (§3.4) on every build.
The allocator refuses a segment whose bank role does not match.

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
executed. Allocator seeds for small data: `$3F:$FAC0-$FF1F` minus `$FFE0-$FFEF` (§1.3); `$3A:$95D4-$9FFF`; text-bank holes
`$3C:$9D16-$9FE1`, `$3D:$BA8D-$BCFF`, `$3D:$BF42-$BFFF`; the empty tileset pages `$2B:$9200`, `$2D:$9200`; sprite-bank
fill; after M2, `$3E:$C163-$C51D` (retired IRQ handlers). The `$36` tail is **SFX only** (R1.14). Whole banks are placed
by role (§1.2).

**The reassemblable source** (M0): Ophis source of the fixed banks `$3E/$3F` (16 KB) and the sound driver
`$34:$8000-$8A3F`, byte-identical when assembled, with the code/data split taken from shadow6 coverage. The IRQ port, the
raster walker, the mute mask and the second driver instance are edits of this source, reviewed through the registry.

### 14.3 BPS [new-code] S · Must

`tools/build/bps.py`: SourceRead / TargetRead / SourceCopy / TargetCopy with source, target and patch CRC32. The release is
the BPS against the vanilla ROM; no Capcom bytes ship (BRIEF §7.4). Tested by applying with the tool itself and with Rom
Patcher JS / Floating IPS at M9.

### 14.4 Golden movies and shadow6 [new-code] M · Must

- **Movies** are `frame:buttons` text plus checkpoints (RAM asserts, frame hashes, screenshots), run headless on FCEUmm
  (`tools/analysis/emu.py`).
- **Testing policy** (RULINGS §6, scope-26): golden movies run on **NORMAL + EN only**; every other setting (CASUAL, HARD,
  JP, ANNOUNCER off, MMC5 audio off) gets **one smoke movie per milestone**; movies are re-recorded only at ⛳ gates; the
  test overhead (about 10 % of code sessions) is in the ledger. Vanilla stages 0-7 keep their golden movies until their
  venue layout replaces them (§1.2); legacy ids `$08-$0F` keep theirs for good.
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

### 14.5 Test mailbox, warps and the DEV combos [new-code] S · Must

- **Warp** (vanilla, `rm6/cheats.md`): write `$51`, `$0684-$0686`, set `$F0 = 2`. GP adds `CK_SECTION`. A warp into
  another stage now clears the stale bits (§4.5).
- **Mailbox** (`meta.md` §9.6, 32 B at page 0 offset `$1A00`): RESET reads a command, clears it, and builds that state
  without menus. Tests write the mailbox into the `.sav` before boot, replacing savestates (vanilla states cannot load
  into the MMC5 build). Command 2 (fight) runs through the fight loader (§4.6) with return kind 4; the test reads
  `FIGHT_RESULT` from WORK when the bout ends.
- **DEV combos: one meaning each** (R1.14, feasibility-21). In stages, pad 1's SELECT means only the quick swap and the
  last-weapon toggle (R2.10), so every in-stage DEV combo is on pad 2, which vanilla never reads (§15.4); pad 2's A and B
  stay free for `systems.md`'s 2P SHIFT (Should).

| Combo | Where | Meaning |
|---|---|---|
| pad 1 SELECT + START held | the title screen, DEV builds | open EXTRA CONFIG (`meta.md` §9.6) |
| pad 2 SELECT held 1 s | in a stage, DEV builds | kill and respawn at the current checkpoint (4MI lesson 10's one-byte respawn) |
| pad 2 START | in a stage, DEV builds, with FRAME STEP enabled in EXTRA CONFIG's DEBUG group | freeze / unfreeze |
| pad 2 RIGHT | while frozen | step one frame |

  `meta.md`'s FRAME STEP ("SELECT+START freezes; SELECT steps") moves to these pad-2 buttons.

### 14.6 EXTRA CONFIG and the DEV build [new-code] M · Must

`meta.md` designs the screen (WHERE / STAGE / CP / SCREEN / ENTER STAGE / FIGHT n, a RAM editor in the 4MI pattern: a
table of RAM pointers and help strings). Tech: code in bank `$47` (§1.2); entered only when the build has `DEV = 1` (a
byte in the header-adjacent version block) or after `meta.md`'s unlock; any use sets `DEV_FLAGS` and meta's
FILEFLAGS.EDITED; the DEV ring buffer at `$7200` logs hooks, warps, fights and saves. ENTER STAGE exists from M2; FIGHT n
arrives with the fight loader (M7). User gates (⛳) always include a Mesen run, to catch header and timing issues FCEUmm
forgives (§1.1, D6).

### 14.7 CI-like runs [new-code] S · Must

`tools/build/check.py`:

| Suite | Contents | When | Time |
|---|---|---|---|
| static | hook registry, allocator, **bank ledger and WORK ledger** (§1.2, §3.4), header, `$FFE0-$FFEF` guard, stage-attribute vanilla rows, the tileset-slot table, level checks (§6.3) including the slot cap, sprite CHR conflicts, artcheck | every build | seconds |
| unit | `levels` round trip (bank + text format), MML round trip, PPU-script selftest (168/168), the text compiler (widths, splits, dictionary round trip), `IFHARD`/`TIERVAL` tier tests, BPS round trip | every build | < 1 min |
| smoke | boot, title, file select, the venues that exist × 600 frames, one save/load, one fight-loader round trip | every commit | ~2 min |
| full | all of §14.4, every route movie that exists, the lag report, the art-acceptance screenshots | milestone gates | ~15 min |

Every session ends green, committed, with `docs/STATUS.md` updated (PLAN §10 kept).

---

## 15. Lag plan

### 15.1 Baseline and the rule (R1.8)

~21,000 of 29,780 CPU cycles per frame are busy in play; a lag frame needs ~29,000. OAM builder 23 % (4,800), sound driver
18 % (3,700-3,900, the multiply loop hottest), bank switching 12-13 % (2,700), terrain collision 7 %, object loop 7 %,
hit-box overlap 5-8 %, object scan 4 %, player 4 %, NMI + PPU 7 %; each extra live object costs ~1,760 cycles; enemy AI
itself is under 1 %. Music keeps tempo during lag (`rm6/engine.md` §8). The measured lag table counts **occupied
slots**, and a quiet screen already holds two (the player, type `$04`, and the screen script, type `$80`; feasibility-4):

| Occupied slots | ≤ 5 | 6 | 7-8 | 9-10 | 11-15 | 16-23 |
|---|---|---|---|---|---|---|
| lag frames | < 1 % | 2 % | 6-7 % | 9-10 % | 25-40 % | 30-50 % |

**The rule** (R1.8, feasibility-4): count **every occupied slot**: the player, the screen script, directors (unless
folded into the script), shots, utilities, effect objects and the text runner. **The cap is 9** until M3 measures the
OAM-builder gain (§15.2 steps 3-4); then the measured cap is published here and in artcheck. Directors fold into the
slot-22 screen script where possible (§9.1). Enforcement: the level build's check 6 (§6.3), artcheck, and the full suite,
which fails a stage whose lag frames rise by more than 2 points. At the cap a screen holds the player, the script, 3
shots and **4 more** (enemies, enemy shots, utilities, effects); the caps the stage docs wrote at 10-13 (the sortie,
AYACO, the train, Paddle Man, the Reaplet alarm, Flame 0B) are re-cut by their owners.

GP's own per-frame costs are budgeted against the savings below: the frozen-tick test (≈ 8 cycles per live slot), the
LATCHSRC write, `systems.md`'s SELECT filter and scorecard timers, ~70-90 cycles per raster band, ~110 cycles per CW call
(hot paths are inline in `$7F`, §1.9).

### 15.2 Savings, in order of cost

| Step | Where | Expected | Tier |
|---|---|---|---|
| 1 | hardware multiply in the sound driver (§12.2) | −1,000 to −1,500 cycles [guess, 4MI's factor] | Must (M2) |
| 2 | MMC5 helpers (§1.4) | −8 cycles per `$CBC0`, more per `$CB91` path | Must (M1) |
| 3 | drop the placeholder `LDA #$7E / JSR $CB91` pair at `$E204`/`$E430` if shadow6 confirms nothing reads the window (critic: nothing does) | one `$CB91` round trip per object per pass [guess: ~1,000 cycles at 10 objects] | **Must (M3)**, R1.8 |
| 4 | OAM builder: unflipped fast path, early off-screen cull, unrolled pair writes | −20-25 % of 4,800 | **Must (M3)**, R1.8 |
| 5 | the unrolled CHR/VRAM copier, **in ROM** (§15.3) | VBlank headroom for streams | Must (M2) |

Steps 3-4 were Should in round 1; they are Must now because the cap of 9 is re-measured after them. Each step is measured
with the shadow6 profiler on the same input.

### 15.3 VBlank budget and the CHR stream (R1.6, R2.3)

NTSC vblank ≈ 2,273 CPU cycles. The NMI spends ~550 on OAM DMA and setup, and runs **one** of: the VRAM buffer + column
paint chain (`$C69E/$C6D7/$C7DE`), or the CHR-set copy `$C79C`, which vanilla runs only when nothing else is pending and
which moves 16/32/48/64 bytes per frame (`$C7D6` = `40 10 20 30`) at ~16 cycles per byte [code]. A column paint costs
~600-700 cycles.

**GP's CHR stream** (form swaps, glyph strips, pinch sets, set-piece player sheets, T6 debris, restores of borrowed
tiles) uses an **unrolled copier in ROM** (R1.6, feasibility-12): bank `$46`, which the NMI maps at `$8000` the way the
vanilla CHR copy maps `$8A` at `$C7AD`. It is `LDA $6E00+i / STA $2007` repeated, 8 cycles and 6 code bytes per byte
(1.5 KB of code for 256 B), with one entry point per length. It reads the **256-B staging buffer** in WORK (`$6E00`),
which the main thread fills the frame before (from ROM, or from the glyph renderer). One stream at a time, from an
8-entry queue (WORK `$7100`). Mapping `$46` at `$8000` inside the NMI is safe for the same reason vanilla's CHR copy is:
streams run only on non-lag frames, when the main thread waits in the scheduler's idle loop (`$C581`), and the scheduler
maps each thread's own banks before resuming it (`$C588-$C593`) [code].

| Frame has | Stream budget |
|---|---|
| no column paint, no VRAM buffer | **192 B** (≈ 1,570 cycles left after OAM DMA and the NMI's own work) |
| the same, with an 8-line blank band at the top (spike test 5, §1.10) | 256 B (Could) |
| a column paint | **96 B** |
| a full VRAM buffer (menus, text) | 32 B |

**The form swap** (R2.3, feasibility-7, consistency-5) streams the whole 2,048-B sheet: **11 frames** standing still,
about 13 while walking (a scroll column every ~5 frames), at most 22 when a column is painted every frame. So
`systems.md`'s **16-20-frame swap behind the flash** holds. The equipped weapon's set (+240 B) is queued after the sheet;
the swap's cooldown is "until the stream completes"; 8 KB CHR-RAM stays. Round 1's "≤ 1 KB, 8-16 frames" was wrong.

### 15.4 Joypad 2 (`systems.md` asks)

Vanilla reads **both** pads every frame (`$3E:$C711`, X = 1 then 0, `AND #$03` so Famicom expansion pads count) into
`$41/$43`, but **no executed instruction reads `$41` or `$43`** outside that loop in the 139,200-frame coverage set [code +
coverage]. Controller 2 is free: `systems.md`'s 2P SHIFT (Should) uses its A and B, and the DEV combos use its SELECT,
START and RIGHT (§14.5).

---

## 16. Milestones M0-M9

RULINGS §6 replaces PLAN §8 and round 1's M0-M3 ordering (scope-4): a minimal engine first, then the **Blizzard
vertical slice at about 115 sessions**, instead of all foundations followed by Opening + Wind + Knight at about 180.

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
| (round 2) `$9B` census, damage-step census, vanilla users of slots 4-7, the scheduler's wait entry points, the helpers' return values, `$CE44`, the venue layout banks | **done** | §7.9, §7.7, §7.12, §11.6, §1.4, §4.5, §1.2; `build/revise/tech/` |
| (new) warps, godmode, password codec, 87 savestates | **done** | `rm6/cheats.md`, `build/research/rm6/states/` |
| (new) MMC5 hardware probes (RAM pages, RAM in `$8000-$DFFF`, CHR-RAM size, multiplier, ExRAM mode 2, ExRAM as a nametable from a mid-frame `$5105` write, no in-frame flag) | **done** for FCEUmm | `build/design/design-tech/probe/` |

### 16.2 The milestones and tech's share

Each milestone ends with a playable build, the suites green, `docs/STATUS.md` updated, the bank ledger printed and, at
every gate, art-acceptance screenshots for the user (R5.1). ⛳ = the user plays it (in Mesen as well as FCEUmm). Session
counts are tech's share from the ledger; the cumulative column is RULINGS §6's for all docs.

| M | Contents (RULINGS §6) | Cumulative, all docs | Tech sessions |
|---|---|---|---|
| **M0** | Workbench; **the MMC5 go/no-go spike on Mesen** | [12] | 12.5 |
| **M1** | Literal MMC5 port with golden equivalence; PRG-RAM, save skeleton, mailbox | [25] | 13 |
| **M2** | Slice engine (tech's part below; meta's save, file-select-lite, bracket-lite, results, debrief and EXTRA CONFIG UI are theirs) | [70] | 31.5 |
| **M3** | Slice systems (tech's part below; `systems.md`'s SELECT, form swap, taps, adaptors, GP_BOSSHIT, WEAK!, scorecard, bolts and shop are theirs) | [95] | 11.5 |
| **M4** ⛳⛳ | **BLIZZARD end to end (v0.1)**; re-estimate the ledger | [~115] | support only |
| **M5** | Stage-attribute table; Opening-lite; Flame, Plant, Centaur, Yamato | [~205] | 15.5 |
| **M6** ⛳ | Text v1b; T1-lite; Knight, Tomahawk, Wind; HALFTIME RIOT (**v0.5 "Round One"**) | [~285] | 8.5 |
| **M7** | BG-boss tooling, the fight loader; H1, H3, H5 | [~340] | 8 |
| **M8** ⛳ | W2, W3, ending | [~380] | 1.5 |
| **M9** | Native-JP review, balance, emulator and hardware matrix, BPS release (**v1.0**) | [~440] | ledger `overhead` |
| | | | **102** |

### 16.3 M0: Workbench and the go/no-go spike (12.5)

1. **M0.0 (1.5)** The MMC5 go/no-go spike (§1.10): six probe ROMs on Mesen and the user's cart. Gate: go, or one of
   §1.10's contingencies, recorded in STATUS.
2. **M0.1 (1)** Repo scaffold (`src/`, `assets/`, `tools/build/`, `tests/`); `build.py` no-op path (vanilla in → vanilla
   out, MD5 check) and `bps.py` with a round-trip test.
3. **M0.2 (1.5)** Hook registry and allocator skeleton (§14.2), seeded with the verified free ranges; static checks
   including the `$FFE0-$FFEF` guard; the bank ledger and WORK ledger files and their printouts (§1.2, §3.4).
4. **M0.3 (1.5)** `tests/run.py` on `emu.py`: movies = inputs **plus scripted RAM pokes** (so a warp at frame N runs
   identically on vanilla and on later MMC5 builds, which cannot load vanilla savestates); record the vanilla golden suite
   on NORMAL + EN (§14.4).
5. **M0.4 (3)** Reassemblable Ophis source of `$3E/$3F` and the sound driver (§14.2), byte-identical when assembled.
6. **M0.5 (1)** `.lvl` text format: decompile and rebuild all 16 stages byte-identically (§6.2).
7. **M0.6 (1)** `mml.py` decompile/compile round trip of the 36 vanilla songs (§12.3).
8. **M0.7 (1)** Censuses: static scans of every code bank for `$51`/`$063D` readers (§4.3) and `$9B` readers (§7.9,
   seeded by `form9b.py`); the sound-stream readers (§12.2); the damage-step kind of every vanilla type (§7.7, seeded by
   `dmgstep.py`); the floor-handler table near `$38:$875A` (X-FLOOR, Could).
9. **M0.8 (1)** `stagetab.py`: 48-byte rows 0-15 and variant rows, with a test that they reproduce every vanilla value.

**Exit**: the spike says go; vanilla round-trips through `build.py`; unit suite green (levels, MML, PPU scripts 168/168,
BPS); vanilla golden suite recorded.

### 16.4 M1: Literal MMC5 port (13)

1. **M1.1 (2.5)** 1 MB insertion (§1.2), header (§1.1), RESET and `mmc5_init` (§1.3), the NMI and IRQ stubs that save
   the interrupted window, the re-entrant CW, `CALL7E` and `FAR` (§1.9).
2. **M1.2 (2)** Bank helpers with vanilla return values, sound service, NMI CHR-copy bank, sound reader (§1.4);
   `$E204/$E430` operands (§1.6); mirroring (§1.5).
3. **M1.3 (3.5)** IRQ literal port: the two NMI arm paths, the entry, the 15 latch and 12 disable writes, `$FF96` (§1.7);
   calibrate `K` and the per-handler delays against vanilla frames.
4. **M1.4 (2.5)** shadow6 MMC5 support (§14.4); golden equivalence green (RAM + frames); coverage shows every ported site
   executed and lists every `$4C` reader.
5. **M1.5 (2.5)** PRG-RAM pages, `ram_probe`, WORK clear, page 0 never cleared; the save module skeleton (A/B commit,
   checksum, load fallback) on a test block; the mailbox read at RESET; a Mesen re-check of the port; the lag baseline
   within 2 % of vanilla's (shadow6 profile).

**Exit**: golden equivalence green on FCEUmm; the port checked once on Mesen.

### 16.5 M2: Slice engine (31.5)

1. **M2.1 (1)** Stage record v0 (§4.4-4.5): the 48-byte table for ids 0-15, `SA_CUR`, the init hook, `$CE44` on every id
   change, `LAYOUT_TIER`. No `$51` reader changes. Gate: every vanilla id plays its golden movie identically.
2. **M2.2 (3)** WRAM-resident layouts (§5.2), the tileset-slot loader (§5.3), poke lists with tiers (§5.5), the map-edit
   service and log (§5.6). Gate: vanilla stages run from RAM, identical in the golden suite.
3. **M2.3 (3)** Families and sub-ids, object lists v2 in WORK, init and spawn hooks, `gp_spawn`, `util_spawn` and the
   slot plan (§7.2-7.3, §7.12); one test object per family.
4. **M2.4 (2)** CHR set table v2 and stage-local ids (§7.6), before any new art (R1.13).
5. **M2.5 (5)** The minimal art pipeline: `chr.py`, `sprites.py`, `palettes.py`, `artcheck.py` (§6.7).
6. **M2.6 (3)** The level pipeline (§6): `.lvl` build, checks 1-9, maps. **The free-id scan runs first** (R1.14), as a
   stand-alone script over the 16 vanilla stages, then inside the build.
7. **M2.7 (4)** The raster list (24 bands) and presets; all chains migrated; the logic out of the IRQ into
   `irq_logic_tick` in `$7E`; the compositor and the sound-band rule (§8, §1.8); the old handler space freed. Gate:
   golden equivalence except Knight and Centaur, which pass behaviour-equivalence.
8. **M2.8 (3.5)** Text v1a (§11.8): the ExRAM window, the glyph cache, the compiler with dictionary compression, the
   pop-up runner, the debrief and help windows, the language hook; samples in JP and EN.
9. **M2.9 (4)** Sound (§12.2-12.3, §12.6): track table v2, bank bytes, reader range, hardware multiply, play-time clock,
   `mml.py` compile, the D9 mute mask; the first new song plays in a vanilla stage.
10. **M2.10 (1.5)** The DEV build: EXTRA CONFIG engine (ENTER STAGE), warps, the DEV combos, the ring buffer (§14.5-14.6).
11. **M2.11 (1.5)** The CHR stream: the ROM copier in `$46`, the staging buffer, the queue, the budgets of §15.3; lag
    steps 1 and 5.

**Exit** (tech side): vanilla content runs on the new engine (record, RAM layouts, raster list) and passes the suite; a
pop-up plays inside a vanilla stage and a debrief page on a menu screen, in JP and EN; a new song plays; a sprite made by
the art pipeline appears in a vanilla stage.

### 16.6 M3: Slice systems (11.5)

1. **M3.1 (1.5)** LATCHSRC in `systems.md`'s format, the frozen tick and frozen handlers with build-derived `FRZ_KIND`,
   the LFSR, the death-hook audit (§7.7-7.8). Gate: an Ice-Blocked snow robot keeps taking damage and dies frozen.
2. **M3.2 (2.5)** T6 variant blocks and X-BONK on the map-edit service (§10); a test climb with break and refill.
3. **M3.3 (1)** GP player-state takeover and X-WRAP (§7.9).
4. **M3.4 (2)** The HUD widget module (§7.13).
5. **M3.5 (2.5)** The commentator event bus (§11.7): death and first-weakness lines through pop-ups.
6. **M3.6 (2)** Lag steps 3-4 (the OAM builder) and the re-measured slot cap, published in §15.1 and artcheck (R1.8).

**Exit** (tech side): the slice's mechanics (T6, X-BONK, X-WRAP, frozen damage, HUD, commentary) pass their demo movies;
the new cap is published.

### 16.7 M4 ⛳⛳: BLIZZARD end to end (v0.1)

No new tech items. Tech's part: Blizzard's layout replaces `$32:$A000` and its vanilla movie retires (§1.2); its slot
lands in bank `$62`; the full suite and the lag report run on the slice; **the ledger is re-estimated from actual
session counts** (R0.1), and this section's numbers are revised with it.

### 16.8 M5: the attribute table and the first four venues (15.5)

1. **M5.1 (3)** The stage-attribute table proper (§4.3): the 45 `$51` and 11 `$063D` readers, the relocated tables, ids
   `$10-$21`, the YOU GET operand (§1.2). Gate: every legacy id and every venue built so far plays its movie identically.
2. **M5.2 (2.5)** T3 switch → target (§7.10).
3. **M5.3 (2)** T7 pad history (§7.9), for Flame's Shadow Rock.
4. **M5.4 (2)** T8 multi-part bosses (§7.11), for Yamato's Daruma.
5. **M5.5 (2)** The attach state (§7.9), for Plant's vines and balloon.
6. **M5.6 (1.5)** X-EXWP (§7.9), for Yamato's pogo.
7. **M5.7 (1.5)** The boss-panel extension (§11.2).
8. **M5.8 (1)** The pattern-table split for menus (§8.3).

### 16.9 M6 ⛳: the rest of Round One (8.5)

1. **M6.1 (2.5)** Text v1b (§11.8), before Knight.
2. **M6.2 (3)** T1-lite (§9.1), for Wind's sortie and Tomahawk's train.
3. **M6.3 (1.5)** The free-flight vehicle state (§7.9), for SKY ACE.
4. **M6.4 (1.5)** The palette-flash and lighting service (§8.5), for the HALFTIME RIOT.

**Exit**: v0.5 "Round One", the scope checkpoint; the ledger is re-estimated again.

### 16.10 M7: the H wings (8)

1. **M7.1 (2)** `bgboss.py` (§6.7), before the H wings (R1.13).
2. **M7.2 (2.5)** The fight loader, FIGHT_CTX and the return-to snapshot (§4.6); EXTRA CONFIG's FIGHT n and the mailbox
   fight command. Gate: a hub → arena → hub round trip with the snapshot restored, for a win and for a loss.
3. **M7.3 (2.5)** F-PIECES on the map-edit service (§5.6), for H1's Yellow Devil.
4. **M7.4 (1)** The `$9B` tables with a 4th row (§7.9), before SUPER in H3; a coverage movie with `$9B = 3`.

### 16.11 M8 ⛳ and M9

- **M8 (1.5)**: `RL_FLOOR8` (§8.3) for W3. W2 runs on the fight loader (M7); the ending uses the D9 mask (M2) and the
  vanilla staff-roll engine through the language hook.
- **M9** (ledger `overhead`): the BPS release, tested with the tool itself and with Rom Patcher JS / Floating IPS
  (§14.3); the emulator and hardware matrix (FCEUmm, Mesen, the user's cart, RULINGS §7 question 1); the final ledgers.

### 16.12 After v1.0

The v1.1+ tech items, in the order the cut line (R0.3) brings back their users: the Break Man slot-0 variant (with the
tag partner, item 2), per-stage HARD poke lists (item 3), the venues' second slots and the section switch (item 4),
F-SIZES and the 16-band floor (Should with R3.6's W3 sizes), then the Could tier: F-ERA, ExGrafix rooms and TS_LAB with
W1 (item 5), TS_ARCADE with the Exhibitions (item 6), the MMC5 pulse driver, X-UPEXIT, X-FLOOR, the OAM priority override.

---

## Lessons applied

- **CX 8** (engine): a bank byte beside every pointer table (tracks, lists, sections, families, the stage record); raster
  effects behind one walker with their parameters in dedicated RAM (§8); interrupt-safe banking through shadows, now with
  the interrupted window saved by the stubs (§1.4, §1.9); old entry points kept by rewriting the helpers in place, with
  vanilla's return values (§1.4). **CX 9**: a test harness from day one (mailbox, warps, the fight loader as a test
  entry, dialogue injection through `TALK id`, damage sweeps via EXTRA CONFIG). CX's text lessons: an opcode set with
  `CALL` and `SKIPIF`, scripts started from object data, a highlight plane, text kept out of code banks (§11).
- **4MI 8**: level data in RAM, connectivity as data, difficulty as poke lists, now four tiers (§5). **4MI 11**: a
  generic double-buffered raster list (§8). **4MI 12**: an accurate target and a correct NES 2.0 PRG-RAM size, a boot
  probe, and now a go/no-go spike before the port (§1.1, §1.10, §2.3). **4MI 13**: resolve placements statically (§6.3,
  §7.6). 4MI's per-message canvas, generalised into the glyph cache (§11.4). PPUMASK as an effects register, spare
  attribute bits instead of new formats (T6's bit 2), shared hardware guarded (the multiplier belongs to the sound
  driver), an unrolled VBlank copy (§15.3). 4MI's 97 % fill is why the bank ledger exists (§1.2).
- **RM6 1**: ids past 15 only after the 45 readers are rewritten and the packed tables relocated (§4), and the same audit
  for `$9B` before a 4th form (§7.9). **RM6 2**: the block table as the art budget (T6 variants are reported in block
  ids; each slot gets its own alternate set). **RM6 3**: the 89 free bytes for hot hooks only (§3.1). **RM6 4**: the
  corrected porting checklist, completed (§1.4-1.7). **RM6 5**: new enemies as families with the 6-byte header and a
  CHR-conflict check (§7). **RM6 6**: per-position destruction (§10). **RM6 8**: quirks kept (oil ignition's repaint
  reused through the queue, the `$FFE0` check respected, C.FLRSH and TO BE CONTINUED untouched by the text hook, the
  bubble in slot 6).

## Risks

1. **Hardware and flash-cart support** for MMC5 + 8 KB CHR-RAM + 32 KB PRG-RAM is unverified; 4MI's MMC5 build proves
   it only on emulators. Mitigation: the go/no-go spike before M1 (§1.10) with a defined fallback, the boot probe's clear
   message, Mesen at every gate; the user names the cart (open question 1).
2. **FCEUmm forgives too much**: it always gives 64 KB of PRG-RAM and wraps CHR-RAM at 8 KB [seen], and its MMC5 timing
   may differ from Mesen's. Mitigation: Mesen in the spike and in every ⛳; a headless Mesen in CI if one can run here.
3. **IRQ calibration** may not hit h-blank identically on both emulators. Mitigation: per-band timing tests on both;
   prefer PPUMASK/PPUCTRL bands where a design allows.
4. **ExRAM writes count only while rendering**, and FCEUmm lacks the in-frame flag. Mitigation: every ExRAM write goes
   through the queue flushed inside an IRQ band (§3.3).
5. **Glyph strips**: dense screens (Plant has 0 free BG ids) defer pop-ups; a ROM restore that does not match a screen's
   real CHR state would corrupt visible tiles. Mitigation: the build derives the CHR state from the same data the game
   loads, and every dialogue screen gets a movie with a frame hash after the window closes.
6. **Moving the logic out of IRQs** changes Knight's and Centaur's timing by part of a frame: exact golden equality is
   lost there (behaviour tests instead).
7. **WRAM layouts**: a stray write corrupts the current stage. Mitigation: DEV builds compare the LAYOUT page with the
   ROM image plus the edit log at every screen exit.
8. **T6 block-id cost** on full tilesets, now without the bitmap fallback (R1.10): a venue that runs out of block ids gives
   up breakable cells.
9. **The 9-slot cap is tight.** The stage docs wrote set-piece caps of 10-13; they are re-cut, and M3's OAM work may raise
   the cap. If it does not, several set pieces lose objects.
10. **The fight context** must catch every path that ends or restarts a stage; a missed vanilla path would run a venue's
   clear inside a W2 bout. Mitigation: the death-hook audit's site list plus coverage of every boss kill in fight mode.
11. **CW costs ≈ 110 cycles** now that it is re-entrant. Mitigation: hot paths stay inline in `$7F`; the profiler counts
   CW calls per frame.
12. **Cartridge space**: the full design fills the bank ledger exactly (§1.2); v1.0 uses about 41 of 64 new banks. Growth
   after v1.0 must displace something; the ledger is re-totalled at every gate.
13. **Sound driver reassembly** (M0.4) is delicate, and the mute mask now depends on it (Must).
14. **Vanilla savestates cannot load into MMC5 builds**: all tests boot and warp (mailbox, scripted pokes).

## Open questions

1. **(User, RULINGS §7 question 1)** Which hardware target: EverDrive N8 Pro, another cart, or none? It decides how
   strict the spike is.
2. Can a headless Mesen run in this environment, for CI and the spike? If not, the user runs the six probe ROMs and
   reports a screenshot each.
3. **`meta.md`**: will HARD move to DIFF A b6 (consistency-15)? `IFHARD` works either way (§5.5); BIT/BVC is cheaper.
   Where does `CFG_CASUAL` (R2.9) live in the file?
4. **`systems.md`**: the per-weapon utility caps that fit the slot plan (§7.12), and whether utilities should survive a
   pause (vanilla's `$38:$9624` clears slots 1-7).
5. **`venues_a.md`, `venues_b.md`, `fortress.md`**: the set-piece caps re-cut to 9 occupied slots (§15.1).
6. **`art_audio.md`**: confirm 14 CHR banks, 3 sprite pairs and the 26-slot table (§1.2, §5.3) after its R5.3 re-run.
7. **`story.md`**: the compressed size of the v1.0 strings, measured at M2, before the text banks freeze.
8. **Director**: R1.3 lists "the MMC5 audio" in v1.0's SUPER colour while R5.2 keeps MMC5 arrangements Could. This doc
   reads it conservatively (§12.5): the channel drop is Must, the MMC5 pulses are Could.

Round 1's questions are closed: the id map (R1.2), the LIVE images in page 1, the pop-up position (top), sections (no
stage over 32 screens), T1-full (not needed), kanji (kana only), and legacy ids' rules (vanilla unless RULESET says
otherwise) (consistency decisions 1, 5, 28, 37).

## Cross-doc dependencies

| Doc | Must agree with |
|---|---|
| `meta.md` (save bytes, bracket, events, debrief, RULESET, the fight table) | the PRG-RAM page 0 map unchanged, LIVE images in page 1 at meta's CPU addresses (§13); the mailbox at page 0 `$1A00`, its fight command through the fight loader (§4.6, §14.5); EXTRA CONFIG's UI on tech's warp, DEV flags, ring buffer and the pad-2 DEV combos (§14.5); `SA.META` = the meta index, fight records pointing at the engine ids of §4.2 (fight `$27` → legacy `$0F`, room 06, RULESET 1993); RULESET at WORK `$6270` (§3.4); the DIFF bits behind `IFHARD` and `LAYOUT_TIER`, and `CFG_CASUAL` (§5.5); the language hook at `$3C:$8636` (§11.2); the stage counters of the `$4n` predicates in the run block (§7.13) |
| `systems.md` (combat, economy, chip numbers) | hot bytes `$06BD-$06C8`, per-slot arrays at `$6000+` (§3.1, §3.4); LATCHSRC in systems' format, written at `$38:$8FDF`; no punch re-class (§7.7, R2.1); frozen handlers, `FRZ_KIND`, its NOFREEZE list overriding the derived kinds (§7.7, R2.2); the slot plan, `util_spawn`, per-weapon caps (§7.12, R1.11); the stream budget 192 / 96 / 32 B and the 16-20-frame form swap (§15.3, R2.3); controller 2 (§15.4); the poke-list format and `TIERVAL` for the CASUAL levers (§5.5, R2.9); the `$9B` audit before SUPER (§7.9); Break Man as a slot-0 variant (Should, §7.9); stage fields `FORT_COL`, `SCORE_ID`, `PAR`, `NO_TAG` (a mask), `KEEPWE`, `YOUGET` → its weapon-order table (§4.4) |
| `venues_a.md` (staging, mechanics) | T1-lite with the director in the script slot and ≤ 4 enemies alive (§9.1); T4 through `RL_BANDS` ≤ 6 + the window (§8.3); text v1b before Knight; the battle log in the pop-up window with the commentators muted (§11.3); T3, the attach state (the T5 vines), the VA-* objects on families `$F4/$F5`; VA-TIMED = `alt_flip` (§5.6); the Knight ceiling out of the IRQ with parameters (§1.8); its slots (§5.3); caps re-cut to 9; no BG tile ids are freed by MMC5 (8 KB CHR-RAM, no banking, ExGrafix only in W1's rooms: D6, R1.3), so Plant keeps its canopy redraw |
| `venues_b.md` (staging, mechanics) | T6 = variant blocks only (§10); X-BONK; X-GPOBJ = families; ship, tide and ceiling as `EFFECTS` bits with `EFX_PARAM` (tide dwell); X-UPEXIT and X-FLOOR Could; the pogo = X-EXWP, the Daruma = T8, Shadow Rock = T7 (all Must); sponsor envelopes as family `$F6` pickups; one slot per venue (§5.3); the ignition hook on `$3E:$DDFC` repaints through the queue; the ship thread's `SHIP_TURN` event (§8.3) |
| `fortress.md` (staging, mechanics) | the ids of §4.2 (R1.2); TS_STADIUM for the Opening, the Riot and the lap, and the slots of §5.3; BG bosses on `RL_FLOOR`; F-PIECES on the map-edit service; W3 on `RL_FLOOR8` + 2 window bands; W2 through the fight loader with its hub state in `$0340/$0650` (§4.6; its §5.2.1 retagged [new-code] M); no ExGrafix in v1.0 (§3.3: Could, W1 and METALL 16 rooms only); SUPER colour = palettes, bands and the channel drop; the NPC Break Man = family `$F7`; F-GRID deleted; `NO_TAG` mask, `ERA`, `OWNED` (§4.4); Pi-kun at one size (F-SIZES Should) |
| `story.md` (every word, the ending) | the engine of §11: glyph cache, EN ALL CAPS, JP kana; POP 2 × 28 cells with ≤ 24 glyph ids + a face icon; dialogue, debrief and help pages 4 × 28; full-screen pages 9 × 28 with ≤ 128 glyph ids; the control codes (§11.5); the TSV source; dictionary compression; ≈ 350 Must strings in text banks T1-T4 (§1.2); the hook at `$8636`; the mute mask for S42 (§12.6); 7 face icons |
| `art_audio.md` (tile, byte and track budgets) | 8 KB CHR-RAM and no extra page (D6, R1.3); the tileset-slot table is tech's (§5.3), art's is regenerated from it; CHR set table v2 (§7.6); the minimal pipeline (§6.7); weapon-slot sets ≤ 15 tiles and set-piece player sheets (R2.3); the 1-bpp glyph set without lowercase; 16×16 face icons (portraits Should); 5 music banks and SFX in the `$36` tail (§12.4); the stream budget (§15.3); the ledger rows for CHR (14), sprites (3 pairs), tilesets (13) and music (5) |

## Changes in round 2

Every change, with the ruling or finding that caused it. Finding ids refer to `review_feasibility_design.md` and
`review_consistency_scope.md`; R-numbers to `RULINGS.md`.

| # | Change | Ruling / finding |
|---|---|---|
| 1 | New **v1.0 scope** section: 43 Must items with milestone and sessions (tech = 102 in `tight.py`), and the Should / Could / Won't lists | R0.1-R0.4; scope-1, scope-2 |
| 2 | Tiers redefined (Must = v1.0, Should = v1.1+, Could, Won't) and every section re-tiered; Must items depend only on Must items | R0.2, R0.3, R0.4; scope-3 |
| 3 | §0 decisions rewritten (D1-D14) and extended (D15-D22: bank ledger, WORK ledger, stage changes, lag rule, unified engines, slot plan, frozen handlers, Break Man and `$9B`) | R1.1-R1.14, R2.2 |
| 4 | §1.2 **bank ledger**: a printed table of all 128 banks (1,024 KB), roles and owners; music 5, text 9 (4 new + `$0B-$0F`), layouts 8 (6 new + `$32/$33`), tilesets 13, CHR 14; v1.0 ≈ 41 of 64 new banks; the full design fills the ledger | R1.5; feasibility-13, consistency-4, consistency-41 |
| 5 | Venue layouts overwrite `$32/$33` in place (verified: stages 0-3 in `$32`, 4-7 in `$33`); vanilla 0-7 regression-tested until replaced; **the YOU GET room's borrowing of stage 5 found and kept working** through pseudo-row `$21` with a copy of vanilla Tomahawk's section | R1.5 (finding from re-reading `$3B:$BD20`) |
| 6 | `$36`'s 449-B tail reserved for SFX and removed from the allocator seeds | R1.14; feasibility-21 |
| 7 | §1.4 helpers return vanilla's registers (A = bank / 7 / preserved / `$17`), re-read from the ROM | R1.14; feasibility-22 |
| 8 | IRQ handler 0 kept as the preset `RL_SOUNDPLAYER` | R1.14; feasibility-21 |
| 9 | §1.8 `irq_logic_tick` lives in `$7E` and never uses CW; the ceiling's reuse limited to Knight and Yamato | R1.4; R3.1, R3.2 |
| 10 | §1.9 CW is re-entrant (pushes the previous `$5116` and registers); the NMI and IRQ stubs save and restore the interrupted window; CW is forbidden in interrupt code and never waits | R1.4; feasibility-10 |
| 11 | §1.10 **MMC5 go/no-go spike** before M1.1: six tests, pass criteria, outcomes, the MMC3 fallback | R1.1; scope-5, scope-11 |
| 12 | D3 corrected to PRG-RAM ids `$80-$83` | consistency-41 |
| 13 | §3.1 hot RAM: CW, interrupt-stub and mute-mask bytes added; `ASCROLL` removed; raster cursor 0-47 | R1.4, R1.9, R5.2 |
| 14 | §3.3 **ExRAM in mode 0 for the whole game**; ExGrafix only as a Could in text-free locked rooms (W1's 16-bit section, the METALL 16 arena), filled in mode 2 while blanked, commentary held; no extra 4 KB CHR page; v1.0 SUPER colour = palettes, bands and the channel drop; an ExRAM row map; no WORK mirror | R1.3; blocker feasibility-1, consistency-1, scope decision 17 |
| 15 | §3.4 **WORK ledger**: every range of page 1 with an owner, totalling 8,192 B; the unrolled copier moved to ROM (256-B staging buffer); map-edit log 256 B; ranges for the fight block, RULESET, the return-to snapshot, HUD records and the player block; 1,280 B free | R1.6; feasibility-12 |
| 16 | §4.2 the id map is binding; HALFTIME RIOT; tiers per id; the YOU GET pseudo-row; the GP Rush lobby is Opening screen `$1D` with no slot | R1.2, R4.3; feasibility-2, consistency-2, scope-12, consistency-31 |
| 17 | Attribute work split: the record and init hook at M2 (GP code only), the 45 + 11 readers at M5 before the first id ≥ `$10` | R1.2; scope-12 |
| 18 | §4.4 record widened to **48 bytes**: `NO_TAG` becomes a 32-bit screen mask; `HUB`; `SECRET_SCR` (renamed from `PLATE_SCR`); `OWNED`, `ERA`, `PLATE_OBJ`, `LOCAL_CHR`, `HUD_ID`, `COMM_ID`, `CK_TABLE`, `FIGHT_ROW`; `POKE_LIST` replaces `HARD_LIST` | R1.14; feasibility-18, consistency-21 |
| 19 | §4.5 `$CE44` runs on every stage-id change (verified in ROM; vanilla only on the new-stage path) | R1.7; feasibility-3 |
| 20 | §4.6 **the fight loader**, owned by tech and Must: `fight_load`, `FIGHT_CTX` and the paths it reroutes, the 64-B return-to snapshot, the hub rule; W2's alcove loader retagged [new-code] M | R1.7; feasibility-3, feasibility-19, scope-6, scope decision 12 |
| 21 | §5.3 **one tileset-slot table**: 2 slots per bank with independent alternate sets, 26 slots in 13 banks, 14 in v1.0; TS_STADIUM serves the Opening, the Riot and the lap; art's no-sharing rule and venues_b's bank-per-venue request retired | R1.10; scope-11, consistency-9, feasibility-17 |
| 22 | §5.4 sections stay Should: no v1.0 stage exceeds 32 screens; the slot-B section switch is Should | consistency decision 37 |
| 23 | §5.5 **one poke-list format** with four tiers; `LAYOUT_TIER` derived per stage; `CFG_CASUAL` and the CASUAL lever list built from `TIERVAL`, dormant checkpoints and pokes; `IFHARD` generated from meta's bits (the round-1 macro tested GUARDS); HARD content Should | R1.10, R2.9; scope-25, consistency-15, consistency-16, design-7, scope-19 |
| 24 | §5.6 **one map-edit service** (`map_set`, `alt_flip`, one repaint queue with a 4-cell / 1-column budget, a 256-B log); T6, VA-TIMED, T3 walls and F-PIECES built on it; **F-GRID deleted** | R1.10, R1.6; scope-10 |
| 25 | §6.3 check 6 counts every occupied slot (≤ 9); checks 8-9 added; the free-id table replaces the canvas table and its scan runs before text v1a | R1.8, R1.14; feasibility-4, scope-24 |
| 26 | §6.7 the minimal art pipeline scheduled (`chr.py`, `sprites.py`, `palettes.py`, `artcheck.py` in M2; `bgboss.py` in M7); artcheck rejects weapon-slot sets over 15 tiles; art-acceptance screenshots at every gate | R1.13, R2.3, R5.1; scope-6, feasibility-8 |
| 27 | §7.2 family `$FC` dropped; `$FF` = system coroutines (the text runner); the sub-id record gains `FRZ_KIND` | R1.12, R2.2; feasibility-14 |
| 28 | §7.4 `IFINTERACT` (UP press, B not held, 10-frame post-alt lock), `TALK`, `DMGSTEP`, tier macros; frame-waiting code is a coroutine | R2.10, R1.4; design-21, feasibility-10 |
| 29 | §7.6 CHR set table v2 specified and scheduled before any new art | R1.13; scope-6 |
| 30 | §7.7 no punch re-class (the 21 latch compares stay vanilla); LATCHSRC in systems' format, derived at latch time; **frozen handlers** per type or family + sub-id with NOFREEZE and a boss-side frozen state, kinds derived by the build (census: `$E9D7` 134, `$EA20` 18, `$EA6E` 126 sites) | R2.1, R2.2; feasibility-5, feasibility-6, consistency-20 |
| 31 | §7.9 one attach state and one free-flight vehicle state; set-piece player sheets; **the `$9B` audit** with census results (30 static / 18 executed readers, 5 table indexes, the `$9F + form` type spawn); **Break Man as a slot-0 variant** (Should) and the NPC Break Man (Must); X-UPEXIT Could; T7 Must | R1.10, R1.12, R2.3, R4.2; scope-17, feasibility-8, feasibility-14, scope-15 |
| 32 | §7.11 T8 Must (Yamato keeps the Daruma; AYACO) | R3.2 |
| 33 | §7.12 **object-slot plan**, with the measured vanilla users of slots 4-7 (Beat/Rush in 4, the bubble in 6, the pause-menu clear of 1-7); `$E59F` capped at `$14`; the text runner in `$15` | R1.11; feasibility-9 |
| 34 | §7.13 **one HUD widget module**; collect-N secrets on meta's stage counters | R1.10, R3.1; scope-16 |
| 35 | §8 **24 bands** per buffer; `RL_SHIMMER` = 2 entries; the sound band must be followed by ≥ 36 band-free lines; band routines in `$7E/$7F`; `RL_FLOOR8` Must, the 16-band floor Should; a band budget per scene; E3 uses attribute palettes | R1.9, R1.14, R3.6; feasibility-15, consistency-27, scope-5 |
| 36 | §8.5 the palette-flash service enforces ≤ 3 large flashes per second and REDUCED fades; the Riot's blackout is the one dark-room set piece | R3.5, R3.1; design-13, design-5 |
| 37 | §9.1 the wave director folds into the slot-22 script, ≤ 4 enemies alive; §9.2 T1-full Won't | R1.8; feasibility-4, consistency decision 37 |
| 38 | §10 T6 is variant blocks only; the bitmap fallback is dropped | R1.10; scope-10 |
| 39 | §11 **text rewritten**: a fixed-cell glyph cache; EN ALL CAPS; JP kana, no kanji; pop-ups 2 × 28 with ≤ 24 glyph ids + a face icon; dialogue, debrief and help 4 × 28; borrowed tiles restored from ROM (no read-back); coroutines (`$E46C` in stages, the scheduler wait on menu screens); dictionary compression Must; v1a / v1b; pop-ups at the top by default; the hook at `$8636` is the reference; portraits Should; the commentator bus | R1.4, R5.1; feasibility-10, feasibility-11, consistency-3, consistency-26, consistency-40, consistency-41, scope-5, scope decision 14, consistency decisions 4, 5, 29 |
| 40 | §12 5 music banks; the D9 channel mute mask is Must; of art's driver items D1, D2, D4, D6, D9, D11 are Must and D3 (instrument table) Should; DPCM none (in `$7F` if ever); MMC5 pulses Could, with the conservative reading of R1.3 | R1.5, R1.3, R5.2, R1.14; scope-3, scope-23, consistency-41, consistency decision 36 |
| 41 | §14 bank and WORK ledgers printed per build; the testing policy (golden movies NORMAL + EN, one smoke movie per other setting, re-record at gates); **DEV combos with one meaning each**, in stages on pad 2; BPS tests at M9 | R1.5, R1.6, R1.14, R2.10, RULINGS §6; scope-26, feasibility-21 |
| 42 | §15 the lag rule (every occupied slot, cap 9 until M3); OAM-builder steps promoted to Must at M3; the VBlank budget recomputed for the ROM copier (192 / 96 / 32 B); the form swap is 11-22 frames, so 16-20 frames behind the flash holds | R1.8, R1.6, R2.3; feasibility-4, feasibility-7, feasibility-12, consistency-5 |
| 43 | §16 milestones rewritten to RULINGS §6 (M0-M9) with tech task lists and session counts per task | RULINGS §6, R0.1; scope-1, scope-4 |
| 44 | `tools/plan/tight.py`: tech re-itemised to 102 (fight loader moved in from meta, +2 OAM, +1 `$9B`, −1.5 F-SIZES), meta −2.5; `tools/plan/tally.py`: the fight loader moved to tech, proposed tiers updated (F-SIZES S, OAM builder M, `$9B` audit added, F-GRID and the T6 bitmap W) | R0.1, R1.7, R1.8, R1.12, R3.6, R1.10 |
| 45 | Risks, open questions and the cross-doc table rewritten; round 1's ten open questions closed | consistency decisions 1, 5, 28, 37; R1.2 |
| 46 | `[engine-ok]` tags that need code retagged (the YOU GET operand; W2's loader in `fortress.md`) | R1.14; feasibility-19 |
| 47 | `fight_return` sets a restore-pending flag (`RET_FLAGS` b7) so the init hook restores the hub's snapshot after the `$CE44` clear; world freeze is one more test in the frozen tick's inline patch; the NMI's mapping of the copier bank is justified by the scheduler's own remap (`$C588-$C593`) | R1.7, R1.4, R1.6 (implementation detail) |
