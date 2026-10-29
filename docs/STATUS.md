# STATUS: hand-off log

Update this at the end of every session: what was done, what's next, and anything surprising.

## Current state

- **Phase:** design complete (round 3: reconciled and verified). **Next task: M0.0, the MMC5 go/no-go spike** (`docs/PLAN.md` §7 and §10;
  `docs/design/tech.md` §1.10 and §16.3).
- **Build:** none yet. Analysis tools live in `tools/analysis/` (see its README); the session ledger in `tools/plan/`.
- **Scope:** v1.0 = the tight Must, ≈ 451 sessions (`python3 tools/plan/tight.py`). Release ladder (RULINGS R8.1): v0.1 Blizzard slice
  (M4, ~150), v0.5 Round One (M6, ~342), v1.0 Championship (M9, ~451).
- **User answers** are in `docs/PLAN.md` §9: emulator-only is fine; art and JP review undecided (show a sample sprite
  early); title ROCKMAN 6 GP, subtitle pun to pick; pace 2-4 sessions a week.

## Session log

### 2026-10-29 (later): Design round 3, reconciliation and verification

- **Director's rulings §8** (`design/RULINGS.md`): the ledger and the release ladder re-baselined by adding up each doc's
  own per-milestone figures (the slice is ≈ 150 sessions, not ≈ 115); forms out of the slice and the attach state's core
  into it; the channel drop is LIGHTS OUT's alone; 397 Must strings; one alias gag; `BREAKMAN`/`DARKMAN`; `ROCKMAN5`;
  SPLENDID STRIKE; the podium in pairs; the nightingale floor Should; the pause keeps utilities.
- **Reconciliation** (`design/reconcile.md`): the 59 cross-doc requests round 2 left were routed to their owner docs;
  51 applied, 8 already done, 0 declined.
- **Verification:** four cross-doc critics (ids/memory/numbers, names/words/story, tiers/dependencies/milestones,
  mechanics/values) plus the reconcilers' 17 follow-ups: 84 findings (17 major, 0 blockers), 82 fixed after each fixer
  re-checked the text, 1 not a problem. Examples of what it caught: tech had Power and Jet swapped in the `$9B` form
  byte; systems' run block overlapped tech's fight-loader WORK range; the flash-safety service was scheduled after the
  slice that needs it; Flame could never reach Platinum because its secret exit bypasses its hidden room.
- Every design doc ends with a "Changes in round 3" table.

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
