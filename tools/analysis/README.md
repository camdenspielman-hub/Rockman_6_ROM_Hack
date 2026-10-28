# Analysis tools

Small, dependency-light scripts used for the deconstruction in `docs/DECONSTRUCTION.md`.
Run `tools/setup_env.sh` first; `LIB` below means the repo's `.pylib` directory.
ROMs are never committed. Put them in `roms/` (gitignored).

| Script | What it does | Usage |
|---|---|---|
| `ips.py` | Minimal IPS applier (RLE + truncation aware) | `python3 ips.py base.nes patch.ips out.nes` |
| `cxpatch.py` | Rebuilds Rockman CX without its Windows patcher (zero-insertion expansion, then IPS); byte-identical to the official output | `python3 cxpatch.py rm2j.nes "Rockman CX.ips" out.nes` |
| `pbtps.py` | Re-implementation of Minus Infinity's PBTPS patch-script engine (`copy DST LEN SRC`, `revbit`, `insert`, `write_i`, `ips_o`, `include`) | `python3 pbtps.py rockman4.nes path/to/rockman4_mi_MMC5.pbtps out.nes` |
| `banks.py` | Per-8KB-bank free-space map, or best-match bank diff vs. an original | `python3 banks.py free rom.nes` / `python3 banks.py diff orig.nes hack.nes` |
| `regs.py` | Counts absolute-addressed mapper register accesses (MMC3 + MMC5); heuristic, includes data false positives | `python3 regs.py rom.nes` |
| `rel.py` | Relative search, which finds a text encoding by the spacing between letters | `python3 rel.py rom.nes BLIZZARD TOMAHAWK` |
| `dump.py` | Dump a region decoded with an `A = <byte>` letter table | `python3 dump.py rom.nes 2EE00 600 1` |
| `disasm.py` | Disassemble an 8KB bank at a CPU address (fixed banks auto-mapped) via py65 | `python3 disasm.py LIB rom.nes 3F E000 FF70 40` or `... 3F E000 vec` |
| `boot.py` / `montage.py` | Fast headless boot + screenshot with **cynes** (MMC3 OK; fails on battery-RAM hacks) | `python3 montage.py LIB rom.nes 150,300 "290:8" out.png` |
| `retroshot.py` | Accurate-ish headless boot with **stable-retro / FCEUmm** (MMC5 + CHR-RAM + battery OK) | `python3 retroshot.py LIB rom.nes 200,500 "450:8,470:0" out.png` |

Input strings are `frame:mask` pairs. The mask is bit 0 = A and bit 3 = Start (`retroshot.py`), or the raw
cynes controller byte (`boot.py`/`montage.py`: A=1, B=2, Select=4, Start=8, Up=16, Down=32, Left=64, Right=128).

Run Python on untrusted ROM files with `python3 -I`.
