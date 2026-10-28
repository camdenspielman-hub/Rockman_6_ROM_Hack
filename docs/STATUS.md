# STATUS: hand-off log

Update this at the end of every session: what was done, what's next, and anything surprising.

## Current state

- **Phase:** planning complete. **Next task: M0.1** (see `docs/PLAN.md` §8).
- **Build:** none yet. Analysis tools live in `tools/analysis/` (see its README).

## Session log

### 2026-10-28: Deconstruction & plan
- Patched and booted both reference hacks headlessly:
  - 4MI (MMC3 + MMC5): via a Python re-implementation of its PBTPS patcher.
  - CX: preprocessing solved (insert 256 KB of zeros before RM2's last 32 KB, then IPS). Byte-identical to the official
    JP output.
- Measured the RM6 engine basics: vectors, fixed banks, bank-switch helpers, sound driver entry and queue, NMI
  shadows, IRQ use, free space (banks `$0B–$0F`, fixed-bank fill at `$FAC0–$FF20`) and text tables.
  Recorded in `docs/PLAN.md` §5.
- Verified the toolchain from PyPI: Ophis assembler, py65, cynes, stable-retro (FCEUmm). GitHub downloads are blocked
  (403) in the cloud environment.
- Wrote `docs/DECONSTRUCTION.md` and `docs/PLAN.md`.

## Open questions for the user
See `docs/PLAN.md` §9 (title, rival, hardware priority, art help, difficulty).
