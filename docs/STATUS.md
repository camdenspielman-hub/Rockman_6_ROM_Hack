# STATUS: hand-off log

Update this at the end of every session: what was done, what's next, and anything surprising.

## Current state

- **Phase:** design complete (round 2). **Next task: M0.0, the MMC5 go/no-go spike** (`docs/PLAN.md` §7 and §10;
  `docs/design/tech.md` §1.10 and §16.3).
- **Build:** none yet. Analysis tools live in `tools/analysis/` (see its README); the session ledger in `tools/plan/`.
- **Scope:** v1.0 = the tight Must, ≈ 455 sessions (`python3 tools/plan/tight.py`). Release ladder: v0.1 Blizzard slice
  (M4, ~115), v0.5 Round One (M6, ~285), v1.0 Championship (M9).
- **Waiting on the user** (none blocks M0): hardware target, pixel artist, JP reviewer, title, pace (`docs/PLAN.md` §9).

## Session log

### 2026-10-29: Deep research, design round 1, review, rulings, round 2

- **Research** (`docs/research/`, ≈ 16,000 lines plus images): CX, 4MI and vanilla RM6 were disassembled, played
  headlessly on FCEUmm (`tools/analysis/emu.py`), cheated through and mapped, then each set was audited by a critic that
  re-verified the load-bearing claims and wrote a `SUMMARY.md`. Highlights:
  - RM6: RAM map with free RAM proven over 232,722 frames; linear disassemblies and shadow6 coverage; the level format
    decoded with a byte-exact round trip and 16 full stage maps (`rm6/img/maps/`); object, AI and damage tables; the
    sound command set; the 168 PPU text scripts; the metasprite format; the 27 IRQ chains; the 45 stage-id readers; warps
    and 87 savestates. `rm6/SUMMARY.md` §4 audits plan v1 (e.g. vanilla forms can't fire weapons; only 4 stages branch;
    the Jet already has a stamina bar).
  - CX and 4MI: how each is built (CX's zero-insertion preprocessing, 4MI's PBTPS script and MMC5 build), and "how
    crazy it gets", stage by stage.
- **Design round 1:** eight docs in `docs/design/` (tech, systems, meta, venues_a, venues_b, fortress, story,
  art_audio) from `BRIEF.md`.
- **Review:** four critics (feasibility, design quality, consistency, scope) found 2 blockers and ≈ 54 majors
  (ExRAM used two ways, three stage-id maps, two text models, ≈ 830 sessions of scope). `design/RULINGS.md` resolves all
  of them and sets the release ladder, the cut line and the milestones M0-M9.
- **Design round 2:** every doc revised against the rulings, each opening with a "v1.0 scope" section and ending with
  "Changes in round 2". The ledger (`tools/plan/`) was updated with them.
- **`docs/PLAN.md` v2:** the overview and index of all of the above.
- Surprises worth remembering:
  - The cloud container restarts kill background work but keep files; long jobs should write as they go.
  - FCEUmm is forgiving about MMC5 (64 KB PRG-RAM always, CHR-RAM wrap at 8 KB), so Mesen checks are required at
    every gate.
  - Subagents can't write files whose names contain "summary" or "report".

### 2026-10-28: Deconstruction & plan v1

- Patched and booted both reference hacks headlessly:
  - 4MI (MMC3 + MMC5): via a Python re-implementation of its PBTPS patcher.
  - CX: preprocessing solved (insert 256 KB of zeros before RM2's last 32 KB, then IPS). Byte-identical to the official
    JP output.
- Measured the RM6 engine basics: vectors, fixed banks, bank-switch helpers, sound driver entry and queue, NMI
  shadows, IRQ use, free space (banks `$0B–$0F`, fixed-bank fill at `$FAC0–$FF20`) and text tables.
- Verified the toolchain from PyPI: Ophis assembler, py65, cynes, stable-retro (FCEUmm). GitHub downloads are blocked
  (403) in the cloud environment.
- Wrote `docs/DECONSTRUCTION.md` and plan v1.

## Open questions for the user

See `docs/PLAN.md` §9 (hardware target, art, Japanese review, title, pace).
