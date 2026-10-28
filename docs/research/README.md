# Research field guide (for every investigator)

Goal: find out **what is actually inside** Rockman CX, Rockman 4 Minus Infinity (4MI) and vanilla Rockman 6 by
**playing them, reading their decoded text, looking at their graphics, and tracing their code**. The readmes are only
a starting point. Prefer what you saw in the emulator over what you read.

## Setup (already done, do not reinstall)

- Repo root: `/home/user/Rockman_6_ROM_Hack`. Run everything from there.
- Python libs are in `.pylib/`. Harness: `tools/analysis/emu.py` (read its docstring).
- ROMs (gitignored, never commit them):

| File | What it is |
|---|---|
| `roms/rm6j.nes` | vanilla Rockman 6 (J), MMC3 |
| `roms/rm2j.nes` | vanilla Rockman 2 (J), the base for CX |
| `roms/rm4j.nes` | vanilla Rockman 4 (J), the base for 4MI |
| `roms/cx_jp.nes` / `roms/cx_en.nes` | Rockman CX v1.1, Japanese / English text, MMC3 512 KB |
| `roms/r4mi_mmc5.nes` | 4MI v1.01, MMC5 1 MB (preferred) |
| `roms/r4mi_mmc3.nes` | 4MI v1.01, MMC3 build |
| `roms/patches/cx/`, `roms/patches/r4mi/` | the original distribution files (readmes, docs, patches) |

Minimal session:

```python
import sys; sys.path.insert(0, 'tools/analysis')
from emu import Emu, contact, chr_sheet
e = Emu('roms/cx_en.nes')
e.run(600); e.tap('START'); e.run(120)          # buttons: A B SELECT START UP DOWN LEFT RIGHT
frames = e.record(1200, every=60, buttons=['RIGHT'])   # or a callable(emu, i) -> buttons
contact(frames, 'build/research/cx/me/run1.png', cols=5)  # then LOOK at it with the Read tool
e.peek(0x06C0); e.poke(0x06C0, 28); e.freeze(0x00A8, 9)   # RAM: $0000-07FF, ExRAM $5C00-5FFF, WRAM $6000-7FFF
e.save('build/research/cx/states/x.state'); e.load('...')
e.render_nametables('nt.png')   # both nametables (512x240), so you see beyond the visible screen
e.render_chr('chr.png')         # live CHR-RAM (tiles currently loaded)
e.cpu()                         # PC/A/X/Y/S/P at the end of the frame
```

- Save scripts in `python3 -I build/research/<game>/<your-agent-name>/*.py`, and keep scratch files there too.
- Disassembly: `python3 -I tools/analysis/disasm.py .pylib <rom> <bank8k-hex> <cpubase-hex> <addr-hex> <count>`. The
  last two 8 KB banks are auto-mapped at `$C000`/`$E000`. For MMC5 4MI, the fixed banks are `$7E`/`$7F` at
  `$C000`/`$E000`. Use py65 directly if you need emulation of a routine.
- Static graphics: these games store tiles uncompressed in PRG. Use `chr_sheet(rom_bytes[a:b], 'x.png')` to view any
  region as 2bpp tiles.
- Text: `tools/analysis/rel.py` finds encodings by relative search. **CX JP vs. EN differ only in text and fonts**, so
  diffing `roms/cx_jp.nes` against `roms/cx_en.nes` locates every text block. 4MI has an in-game language switch (CONFIG).
  Build `.tbl` tables (byte → character) from the live CHR font while text is on screen.
- Look at your images. The Read tool shows PNGs. Upscale small crops (`e.shot(path, scale=2)`).
- Speed: about 3,400 frames/s. 60 frames = 1 s of game time. A 10-minute stage is about 36,000 frames, roughly 10 s of
  CPU.

## Exploration techniques

- **Cheats via RAM.** Find HP, lives, weapon energy, i-frame timer, stage ID, checkpoint and boss-defeated flags with
  RAM diffing (snapshot RAM, do one thing, diff), then `freeze()` them. With frozen HP and lives, an "autoplayer"
  (hold RIGHT, jump when X stops changing, climb when on a ladder) gets through a surprising amount.
- **Warps.** Set the stage ID / boss flags on the stage-select screen, or edit the save data in WRAM. 4MI's post-game
  **EXTRA CONFIGURATION** mode has STAGE / CHECK POINT / CLEAR FLAG / WEAPONS fields; unlocking it (find the flag in
  WRAM `$6000+`) gives you a built-in level select.
- **Savestates** at every stage start and checkpoint go in `build/research/<game>/states/`. Name them clearly and list
  them in your doc so the other agents can reuse them.
- **Nametable renders** show the whole loaded area, and CHR renders show which tiles a scene uses.
- The game reacts to **input on specific frames**. Hold buttons for at least 2 frames, and give menus time.

## Deliverables

- Write Markdown to `docs/research/<game>/<your-topic>.md`. Put **curated** images in `docs/research/<game>/img/`:
  at most about 25 per agent, PNG at 1× or 2×, and contact sheets are welcome. Every image must be referenced from your
  doc with a one-line caption.
- Tag claims **[seen]** (observed in the emulator), **[code]** (from disassembly or data), **[text]** (in-game text),
  or **[doc]** (from the readmes). Speculation is **[guess]**.
- Quote in-game text exactly (EN, plus JP where it matters).
- Be concrete: stage by stage, screen by screen, boss by boss. Cover enemies, gimmicks, hazards, tricks, secrets,
  jokes and references. **The goal is to capture "how crazy it gets"**: anything that surprises you is gold.
- End every doc with a **"Lessons for Rockman 6 GP"** section (design and technical takeaways).
- Do **not** git commit, and do not edit files that other agents own. You may add new helper scripts under
  `tools/analysis/<game>/` if they are generally useful (unique filenames, documented at the top).
