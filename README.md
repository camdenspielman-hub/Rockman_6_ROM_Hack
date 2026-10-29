# Rockman 6 GP (working title)

A large-scale Rockman 6 (Famicom) ROM hack, in the spirit of *Rockman CX* and *Rockman 4 Minus Infinity*.
The World Robot Tournament becomes a real Grand Prix: eight venues that are playable tributes to game history, a
Hall of Fame museum of Rockman 1-5, and a final castle that "upgrades" to 16-bit.

- `docs/PLAN.md`: **start here.** The game, the v1.0 scope, the milestones, the risks and the first-session checklist,
  with an index of everything else.
- `docs/design/`: the design docs (tech, systems, meta, venues, fortress, story, art and audio) and the director's
  binding `RULINGS.md`.
- `docs/research/`: the teardown of vanilla Rockman 6, Rockman CX and Rockman 4 Minus Infinity (engines, stages,
  systems, text, graphics, full stage maps).
- `docs/STATUS.md`: hand-off log and the next task.
- `tools/analysis/`: the headless emulator harness and measurement scripts; `tools/plan/`: the session ledger.

**ROMs are not included and must never be committed.** The base is *Rockman 6 - Shijou Saidai no Tatakai!! (Japan)*,
MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`. Put it at `roms/rm6j.nes`.

```bash
tools/setup_env.sh
```
