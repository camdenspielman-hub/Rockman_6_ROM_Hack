# Rockman 6 (J) fortresses: Mr. X Fortress 1-4, Wily Fortress 1-4, and the ending (rm6-fortress)

Status: **v0 skeleton, in progress** (written early per the resilience rule; sections are filled in as
they are verified). Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text,
**[guess]** unverified. Scripts: `build/research/rm6/rm6-fortress/`. Static decoder:
`tools/analysis/rm6/rm6_stagemap.py` (format in `stages_a.md` section 0). States: the scout's
`build/research/rm6/states/` (`mrx1..4`, `wily1..4`, `*_ck1`, `*_ck2`, `*_boss`).

## 0. Overview [code]

Eight fortress stages, stage ids `$51` = 8-15. Per-stage tables ($3E:$DF25.. , see `stages_a.md` 0):

| $51 | Stage | $6E (metatiles) | $6F (layout) | page | BG CHR set | palette | music |
|---|---|---|---|---|---|---|---|
| 8 | Mr. X 1 | $2C | $26 | $A0 | $9D | $68 | $09 |
| 9 | Mr. X 2 | $2F | $26 | $A8 | $A4 | $88 | $09 |
| 10 | Mr. X 3 | $2F | $26 | $B0 | $B1 | $AB | $09 |
| 11 | Mr. X 4 | $2B | $26 | $B8 | $C3 | $C8 | $09 |
| 12 | Wily 1 | $2A | $27 | $A0 | $89 | $7C | $0B |
| 13 | Wily 2 | $2A | $27 | $A8 | $A2 | $89 | $0B |
| 14 | Wily 3 | $2A | $27 | $B0 | $A2 | $96 | $0B |
| 15 | Wily 4 | $2B | $27 | $B8 | $BA | $18 | $0B |

(sections below are being filled in)

### Findings so far (v0.1, verified in the emulator) [seen]

- **Bosses** (boss room, controller type in slot 8, all 27 HP = `$1B`):
  Mr. X 1 room $11: two rail riders on a pipe lattice ($B6 x2, controller $B7) [guess: "Rounder II"];
  Mr. X 2 room $11: a dark room, a stack of pods on the right wall throwing rocks ($EB..$EE);
  Mr. X 3 room $11: a pilot pod lands in a big tank ($E8/$E9/$EA) [guess: "Tank CSII"];
  Mr. X 4 room $15: the Mr. X Machine, a huge spiked sphere with Mr. X in the cockpit ($D1-$D4);
  Wily 1 room $13: a long-necked dinosaur robot ($E0-$E3);
  Wily 2 room $0F: an orange walking cannon robot that enters from the right ($E5-$E7);
  Wily 3: **the boss rush** (hub screen $08 with 8 teleporters, rooms $09-$10 = $09 + stage id);
  Wily 4 room $06: **Wily Machine 6** (skull face, $EF) -> the face breaks, Wily visible ($F1) ->
  the machine explodes and the **Wily Capsule** ($F2) rises in the same room. Three bars of 27.
- **Boss rush** (Wily 3 screen $08, script $71 = $39:$8E31/$8E3B): eight alcoves (collision types D/E):
  right top -> Blizzard (room $09), left top -> Yamato ($0D), right middle -> Flame ($0C), left middle ->
  Plant ($0B), right bottom -> Tomahawk ($0E), left bottom -> Knight ($0F), centre left -> Centaur ($10),
  centre right -> Wind ($0A). Table $39:$8EC8 (X), $8ED2 (stage id). A ninth entry X=$80 sets `$F0`=1.
- **Ending**: capsule explodes, Wily falls out and kneels; black screen, Rockman holds Wily; Wily behind
  bars; CAPCOM TIMES newspaper; STAFF; then each Robot Master plays **in its own boss room in the real stage
  engine** (`$51` = its stage) followed by a card strip (DWNB-41.. + DESIGNER), in alphabetical order:
  Blizzard ($00 scr $18), Centaur ($07 scr $17), Flame ($03 $17), Knight ($06 $17), Plant ($02 $17),
  Tomahawk ($05 $17), Wind ($01 $15), Yamato ($04 $1D); then the starfield staff roll, PRESENTED BY
  CAPCOM, TO BE CONTINUED.
