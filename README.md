# Rockman 6 GP (working title)

A large-scale Rockman 6 (Famicom) ROM hack, in the spirit of *Rockman CX* and *Rockman 4 Minus Infinity*.
The World Robot Tournament becomes a real Grand Prix through tribute venues to game history, a Hall of Fame museum of
the Rockman series, and a final castle that "upgrades" to 16-bit.

- `docs/DECONSTRUCTION.md`: technical and design teardown of Rockman CX and Rockman 4 Minus Infinity.
- `docs/PLAN.md`: the full design and build plan for this hack (start here).
- `docs/STATUS.md`: hand-off log and the next task.
- `tools/analysis/`: measurement scripts (patch re-implementations, bank maps, disassembly, headless boot).

**ROMs are not included and must never be committed.** The base is *Rockman 6 - Shijou Saidai no Tatakai!! (Japan)*,
MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`. Put it at `roms/rm6j.nes`.

```bash
tools/setup_env.sh
```
