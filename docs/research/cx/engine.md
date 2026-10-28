# Rockman CX engine teardown: mapper conversion, bank map, raster effects, sound, objects, saves (cx-engine)

Static and technical deep dive into how Himajin Jichiku turned Rockman 2 (MMC1, 256 KB) into Rockman CX (MMC3,
512 KB). Every address was read from `roms/cx_en.nes` (identical code in `roms/cx_jp.nes` unless noted) and checked
against `roms/rm2j.nes`. Bank numbers are **8 KB banks**. `$3C:8588` means "bank `$3C` mapped so that this CPU
address is inside it". Tags: **[code]** disassembly/data, **[seen]** emulator, **[guess]** inference.

Scripts (all in `build/research/cx/cx-engine/`, run with `python3 -I` from the repo root):

| Script | What it does |
|---|---|
| `dis.py ROM B8000 BA000 ADDR N` | py65 disassembler with any two banks at `$8000`/`$A000` and `$3E`/`$3F` fixed |
| `bankstats.py` | per-bank: % equal to RM2, % empty, JP/EN diff count, JSR/RTS counts, tile-likeness |
| `chrall.py FIRST LAST OUT` | every bank in a range as a 2bpp tile sheet (for eyeballing graphics vs code vs data) |
| `farcalls.py`, `xrefs.py` | bank-switch call sites and which bank calls which |
| `romwrites.py` | every store into `$8000-$FFFF` (mapper register writes) by bank |
| `objtable.py` | the 192-entry object handler table, compared with RM2's 128-entry table |
| `sound.py` | the 96-entry sound table (bank, pointer), music vs SFX, which tracks are RM2's |
| `irqscan.py`, `irqtrace.py`, `irqshots.py` | sample the IRQ shadows `$80`/`$81`/`$84-$8F`, music id, banks from every savestate |
| `wram.py` | which WRAM pages are used across all 89 shared savestates |
| `pcmwatch.py` | watches for the raw-PCM player running |

---

## 0. The short version

- **Mapper conversion** [code]: every MMC1 serial write (15× `STA $FFF0`, 5× `$9FFF`, 5× `$BFFF`, 5× `$DFFF`, the
  `INC $FFE1` reset trick) is gone. RM2's 16 KB bank-switch entry `$C000` now holds a single `ASL A` that falls into
  a new MMC3 routine at `$C001` → `$F859`, so RM2's ~16 untouched `LDA #bank16 / JSR $C000` calls still work. The
  bank in `$8000` is shadowed in `$61`, the bank in `$A000` in `$62`, and the last value written to `$8000` (the
  MMC3 bank-select register) in `$63`; NMI and IRQ restore all three, which makes bank switching interrupt-safe
  without RM2's "switch in progress" flag dance.
- **Layout**: PRG mode 0 (`$C000` = `$3E`, `$E000` = `$3F` fixed), CHR-RAM with the six CHR registers set once to
  identity (`$FB62`), WRAM enabled (`$A001 = $80`), mirroring shadow `$0723` written to `$A000` every NMI.
- **The new half** (`$1C-$3B`): IRQ effect code (`$1C`), new engine/menu/script/object code (`$1D-$20`, `$24`,
  `$25`, `$30`, `$31`), three banks of **new music** (`$21-$23`), the dialogue engine and scripts (`$26`), and the
  rest graphics (`$27-$2F`, `$34`, `$35`, `$38-$3B`). **`$31-$34` hold a 21.7 KB raw 8-bit PCM voice clip**, and
  `$36` is completely empty.
- **IRQ**: one handler (`$F87A` → `$1C:8000`) with **13 effects** chosen by `$81` (`$1C:8AFE` jump table), line in
  `$80`. Seen in use: Kamen Rider's half-speed parallax skyline (effect 9), the dialogue box's own palette under
  line 184 (effect 10, a mid-frame palette rewrite), the giant Guts Tank's fixed floor (effect 1), the giant
  Dr. Light's split and wobble (effects 12/13), the weapon-get colour wipe (effects 3-4 / 6-7), and a mid-frame
  **second OAM DMA from WRAM `$7D00`** (effect 11).
- **Sound**: RM2's driver (banks `$18`/`$19`) is kept but patched so every track has its own **bank byte**
  (`$18:97B7+id`) and split pointer tables (`$8A40`/`$8AA0`); the track's data is paged into `$A000` on the fly. 96
  ids: **42 music** slots (38 new, 4 RM2 songs kept) and **54 SFX**. Plus a 337-byte DPCM "thump" in the fixed bank
  (`$FB80`) and the PCM clip.
- **Objects**: the handler table grew from 128 to **192 types** (`$3C:92F0` lo / `$93B0` hi) and gained a
  per-type **bank table** (`$3F:FA50`), so object AI can live in any bank: 91 handlers in `$3D` (RM2's), 26 in
  `$20`, 7 in `$25`, 4 in `$24`, 28 in the fixed bank. 69 of RM2's 128 slots were repointed. The boss dispatcher
  (`$16:8003`, table `$803D`/`$804C`) has **15** entries (RM2: 14); bank `$16` was rewritten almost completely
  (5% of its bytes still match RM2).
- **Saves**: only 42 bytes of the 8 KB WRAM are battery data (`$7420-$7449`, three interleaved slots of 14 fields);
  WRAM is otherwise used as a PPU upload queue (`$7E00`), a second sprite page (`$7D00`), palettes (`$7FE0`), and
  live copies of slot and heart flags (`$7FF0`, `$7FF8-$7FFF`).

(Sections below are filled in as the investigation proceeds.)
