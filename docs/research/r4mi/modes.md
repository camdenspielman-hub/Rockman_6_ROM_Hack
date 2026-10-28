# 4MI special modes and meta systems, in practice (r4mi-modes)

Scope: every SPECIAL MODE item and every meta system of *Rockman 4 Minus Infinity* v1.01 (MMC5 build), as it
actually plays: the title menu, CONFIGURATION, the RESULT / Hero Score, TIME ATTACK, the arena family (MECHANICAL,
LIMITED, MY, TRUE), EXTRA CONFIGURATION, RECORDS, AUDIO PLAYER and the achievements.

This doc builds on `cheats.md` (RAM/WRAM map, unlock bytes, MY ARENA field map, 45 fight IDs) and `text.md` (every
menu string, the debrief text). It does not repeat their tables; it adds what each mode *does* when played, and the
code behind the scores and unlocks.

Tags: **[seen]** emulator, **[code]** disassembly/data, **[text]** in-game text, **[doc]** readme, **[guess]**.

Status: work in progress (written early; sections are filled as they are verified).

---

## 0. The unlock chain at a glance

| Step | You do | You get (`$7F78` bit) | Evidence |
|---|---|---|---|
| 1 | Beat the game | SPECIAL MODE replaces CONFIGURATION on the title; TIME ATTACK / SPEEDRUN, CONFIGURATION, RECORDS (`$01`+`$02`) | [code][doc] |
| 2 | Beat the game with all three friends (Eddie, Beat, Rush) | THE MECHANICAL ARENA (`$04`) | [code][doc] |
| 3 | Clear THE MECHANICAL ARENA | LIMITED ARENA (`$08`) | [code][doc] |
| 4 | Clear any one LIMITED ARENA course | MY ARENA, AUDIO PLAYER, EXTRA CONFIGURATION, THE TRUE ARENA (`$10 $20 $40`) | [code][doc] |
| 5 | Clear THE TRUE ARENA | achievement PROOF OF OMEGA | [code][doc] |

(TODO: verify each in play.)

---

## Lessons for Rockman 6 GP

(TODO)
