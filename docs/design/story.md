# Rockman 6 GP: narrative bible and script (story.md)

Owner: design-story. Status: **round 3**: RULINGS §8 (R8.1-R8.8) and `reconcile.md`'s story table applied (see
"Changes in round 3" at the end). Round 2 revised it against [`RULINGS.md`](RULINGS.md) (binding: it overrides
[`BRIEF.md`](BRIEF.md) and everything else), the four critic reports (`review_feasibility_design.md`,
`review_consistency_scope.md`), `crossrefs.md`, and the round-2 revisions of `tech.md`, `systems.md`, `meta.md`,
`venues_a.md`, `venues_b.md` and `fortress.md`. Scratch: `build/revise/story/` (round 1's text is kept there as
`story_round1.md`; `fit.py` checks every line of this doc and counts the strings; `decisions.txt` is the decision log).

**This doc owns every word and the ending** (R4.1): every line the player reads or hears said, in EN and JP; the scene
list S01-S51 and the ending's order; the tone guide and the cast's voices; the boss-card records; the commentator, heckle,
debrief and help-page text; the labels' wording; and the fact sheet behind every game-history claim (Appendix A).

**Single sources of truth for everything else** (consistency critic, RULINGS R1.10/R4.1/R5.2):

| Doc | Owns | What this doc takes from it |
|---|---|---|
| `systems.md` | combat, the economy, the 14 chips | weaknesses, special cases (SC5, SC6, SC11), chip effects, prices, the booth's "BREAK MAN WILL WALK." |
| `meta.md` | save bytes, the bracket, events, the debrief engine, the rating | STORY_BEAT's slot, EVENTS bits, hint ids and order, the rating tests T0-T15 |
| `tech.md` | ids, memory, raster, CHR, the text engine | the text model (R1.4), the language hook at `$3C:$8636`, text banks T1-T4, the D9 mute mask |
| `fortress.md`, `venues_a.md`, `venues_b.md` | staging: screens, set pieces, scene placement and order | where each scene plays, hook ids and triggers, the tier B hint drafts |
| `art_audio.md` | tile, byte and track budgets | face icons, the whistle jingle, G37 LAST MATCH, the plaque frame |

**How to read the scripts.** Every string is one row:

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|

- **Tier**: `M` Must (v1.0), `S` Should (v1.1+), `C` Could, `W` Won't (v1) (R0.2-R0.3). A Must line never depends on a
  Should mechanic (R0.4).
- **Kind** (R4.5's categories): `scene`, `death`, `weak` (the first-weakness line), `secret` (secret, plate and tell
  lines), `hint` (debrief), `help` (chip help page), `stage` (in-stage text a venue or fortress mechanic needs: NPC
  windows, the battle log, signs, plaques that are tells), `plaque`, `heckle`, `sys` (boot, menus' sentences), `flavour`.
- **Surf** (R1.4, tech §11.3): `POP` pop-up, 2 lines × 28 cells, at most 24 distinct glyph ids per page (plus the 4-tile
  face icon); `WIN` the 4 × 28 window (dialogue, scenes, the debrief, help pages); `PLQ` a full-screen page, up to 9 × 28;
  `NEWS` the vanilla newspaper driver, 2 × 28; `LBL` a label: **English in both languages**, as vanilla's labels are
  (§10.1), so it has no JP column.
- **EN is ALL CAPS** (R1.4) and uses only the glyph cache's set (§10.2). ` / ` is a forced line break. `*WORD*` is the
  window's highlight colour. `▶YES NO` is a choice. `%N%` and kin are variables at their reserved width (§10.3).
- **JP is kana only**, phrases separated by spaces (vanilla's wakachigaki), ` / ` the same line break. JP is a draft for
  the native-speaker review, which gates release (R4.5; Risks 2).
- **Who**: **R** Rockman, **L** Dr. Light (radio), **Ro** Roll (radio), **C** Dr. Cossack, **K** Kalinka, **E** Eddie,
  **BM** Break Man, **B** Bass β, **Y** Mr. Y, **W** Dr. Wily (after the unmasking), **DM** Dark Man, **PA** a public
  address, **KN** Knight Man's battle log, and the venue NPCs by name. One speaker per page (§2.7's rule).

`fit.py` reads exactly these rows. It checks every Must, Should and Could line against its surface (28 cells per line,
the line count, ≤ 24 glyphs on a pop-up page, the EN glyph set) and counts them by tier and kind; §10.4's inventory is
its output. Won't rows are kept as records and not fitted.

---

## v1.0 scope

### What ships in v1.0 (Must)

v1.0 is RULINGS R0.2's tight Must. Its text is the words of every v1.0 stage, screen and system, cut to R4.5's list:

| Area | v1.0 text (Must) | Where |
|---|---|---|
| Boot and menus | the license line, the **health notice** (R3.5), the three difficulty descriptions, the CONFIG help lines for INPUT LAG, FLASHES and CASUAL, the lowering warning; every label | §4 S01, §10.5 |
| **Opening-lite** (M5) | S03, S04, the four lane judges' lines (S07 folded in, R4.4), the scoreboard pages, one parade line, S06 (masked, **no name spoken**, R4.2), S08 (the one Wily gag of Act 0), Break Man's charge tip after a death to Pi-kun: **12.5 scene pages** (25 pop-up pages) against R4.4's cap of 15 | §4 Act 0 |
| The bracket and the pit stop | S09, S10, S12, S13, S14, S16, S24, S49 at their core lines; the debrief's requirement hint R2 (the only one v1.0's predicate table uses), scorecard and perfect lines | §4, §7.3 |
| **8 venues** | per venue: the champion's bar-fill line (S11), **4 death lines**, the first-weakness line, the hooks that are a Must secret's tell, the **tier B hints**, and the venue's Must mechanic text (Knight's command windows and battle log, Tomahawk's posters, conductor and Sheriff, the signs) | §4 S11, S15; §6.3; §7.1 |
| **HALFTIME RIOT** (M6) | S17-S19 for the rejects (R4.3); Break Man's help, block and reveal; **Rock's first "Blues?"** at 0E; S20 pages 1-2 in place (R4.2) | §4 Act II |
| **Hall of Fame H1, H3, H5** (M7) | S25 (the theft closes Act III), S26, the H1/H3/H5 plaques (they describe and say BLUES, R3.3/R3.9), S28's core lines, S29, S30 in its WRONG NOTE staging, S32, S33 (two masks, "WE KNOW."), Mr. Y's heckles at v1.0 size | §4 Act IV, §6.5 |
| **W2, W3** (M8) | S34, S36-S39, the gift line, the escape PA, Wily's heckles at v1.0 size | §4 Act V |
| **The ending** (M8) | R4.1's order: S40 (the catch, Rock's second "Blues?"), S41 (the arrest with **the one Mr. Y gag**, the ending's only alias gag, R8.5), the podium and Bass's vow, S44 (no `$94`; page 4 is S44.4F, no Mr. Z), the credits' text, S46-S47, **S42 LIGHTS OUT** (Light says "Blues" once), S43, S48 | §4 Act VI |
| Systems text | the 14 chip help pages; the generic secret and plate lines | §8, §6.2 |

**The counts** (`fit.py` over this doc; §10.4 breaks them down):

| | Must (v1.0) | Should (v1.1+) | Could | Won't |
|---|---|---|---|---|
| Translated strings (EN + JP) | **397** | 362 | 90 | 5 |
| of which R4.5's six kinds (deaths, heckles, first weaknesses, secrets, scenes and plaques, tier B hints, help pages) | **333** | | | |
| of which a Must mechanic's own text and the system sentences (R0.4, R3.5) | 64 | | | |
| Labels (English in both) | 28 | 3 | 5 | 0 |
| Boss-panel records (English in both) | 18 | 3 | 4 | 2 |
| Debrief: tier B hints | 44 | 3 | | |
| Debrief: tier A riddles | | 26 | | |
| Debrief: generic lines (requirement, scorecard, perfect) | 7 | 7 | | |

R4.5 asked for about 350 Must strings: R4.5's own kinds come to **333**; the Must mechanics' text (Knight's windows and battle log, Tomahawk's posters and NPCs, the signs that are tells) and the system sentences add 64, for **397** in all. **R8.4 accepts this reading** ("about 400 Must strings"); §10.4's trim list is the reserve, not a plan. Round 3 moved the three requirement hints no v1.0 predicate uses (R1, R3, R5) to Should (§7.3), and swapped S44's Mr. Z page for its fallback (R8.5); these counts are the single source the venue and fortress docs cite (R8.4; §10.4 gives them by area).

### Sessions (the ledger, R0.1)

Text is its own ledger line (`tools/plan/tight.py`: **text 12**; `tools/plan/tally.py` carries the same figure and the
v1.1+ estimate). One session writes, fits and compiles about 40 strings in both languages and runs the compiler's
checks on them (397 Must strings over 9.5 writing sessions, plus the M2 setup and the M9 fixes); the native-JP review
is external (below).

| Milestone | Text work | Sessions |
|---|---|---|
| M2 | The TSV source, house style and compiler fixtures; boot, health notice, menus, CONFIG; the debrief's generic lines; dictionary measurement with tech (consistency-4) | 1.5 |
| M3 | S10 and S16's game-over lines, for meta's M3 pit stop and game over | 0.25 |
| M4 | The Blizzard slice: its card (in the slice, vanilla's 9-field BLIZZARDMAN record; VENUE `SUMMIT CLIMBER` and the secret arena's `ABOVE THE CLOUDS` arrive with tech's panel extension at M5), hooks, deaths, hints; the bracket lines it uses; the slice's help pages | 0.75 |
| M5 | Opening-lite (S03-S08 as pop-up sequences on text v1a); Plant, Flame, Centaur, Yamato; S12-S13, the adaptor hand-offs with meta's M5 events | 2 |
| M6 | Knight (≈ 33 mechanic strings on text v1b), Tomahawk, Wind; the HALFTIME RIOT; S14, S24 | 2 |
| M7 | H1, H3, H5: S25-S33, the plaques, the heckles; the Appendix A fact pass on the plaques | 2.5 |
| M8 | W2, W3, the ending (S40-S48), the credits text, Break Man's debrief | 2 |
| M9 | Fixes from the native-JP review (fit, glyph splits, register) | 1 |
| | **Total** | **12** |

v1.1+ text (`tally.py`): Should ≈ 7 sessions (tier A riddles, flavour hooks, heckle variants, the float lines, the W2
shouts, the partner's lines, H2/H4), Could ≈ 3 (the crawl, the Exhibitions, the lap's lines, the bundle's booth,
ENGRISH), Won't ≈ 0.5 if ever (Mr. X Returns, Bass Mode).

### What v1.0 text depends on (all Must, R0.4)

| Owner | Piece | Used by |
|---|---|---|
| tech | Text v1a (pop-up, the debrief and help windows, the compiler with dictionary compression) at M2; v1b (dialogue, CHOICE, NPC menus, full-screen pages) at M6 | every surface |
| tech | The commentator event bus (§11.7 there, M3), the language hook at `$3C:$8636`, the boss-panel record by fight id and its 10th field | §5, §6 |
| tech | The D9 mute mask | S42 |
| art_audio | the 7 face icons (§6.1), the whistle jingle, G37 LAST MATCH (the lights-out arrangement, 2A03 stems), the plaque frame, the CAPCOM TIMES headline | S06-S47 |
| meta | STORY_BEAT (`$013`), EVENTS b0-b4/b6/b7, EVENTS2 b4, COMMFLAGS (`$04A`), the debrief tables, the rating tests | §0, §6, §7, S47 |
| fortress, venues | every scene's placement and trigger; the NPC Break Man (Must) | §3, §4 |

No v1.0 line needs the tag partner, the booth, the Exhibitions, W1, H2, H4, the victory lap or the crawl: every line
that does is Should or Could, and the v1.0 staging it replaces is written beside it.

### Not in v1.0 (kept below, each marked in place)

| Tier | Text (R0.3 cut-line item) |
|---|---|
| **Should (v1.1+)** | the **tier A riddles** (R4.5); the requirement hints no v1.0 predicate uses (R1, R3, R5; §7.3); the flavour hooks of every stage; the generic death table and heckle variants; the **float lines** (the roll call, fortress's first trim); the W2 champions' shouts; the champions' defeat lines; the secret-arena bar fills except the Rodeo Ring's and the Knightlord's; the partner's lines (S20 pages 3-6, S30's TWO BREAK MEN, S40's carry art, the call lines, S47's T1 "never called": item 2); H2 and H4 (plaques, exhibits, thanks plaques: item 5); Doc Robot MK-VI; Roll's line in S42 |
| **Could** | the **attract crawl** (S02, item 12); the Exhibitions (S22-S23 and their plaques, item 6); the victory lap's lines (S45, item 8); W1 (S35, item 5); the booth and BREAK MAN WALKS (S21, item 9); the 1993 RULES lines (item 10); ENGRISH (§9, item 12) |
| **Won't (v1)** | Mr. X Returns (S50), Bass Mode (S51), E4 Maze Man's lines, the sekisho's lines (R3.2), the Museum's plaque gallery, S44.4's Mr. Z page (R8.5: the alias gag plays once in the ending, at the arrest) |

**The native-JP review** (R4.5) is a dated external dependency that gates release: it is booked for M9 (RULINGS §6) and
its date is the user's to set (RULINGS §7 question 3). Until it happens, every JP line here is a draft.

---
## 0. The story in one page

**Logline.** One year after "Mr. X" was unmasked as Dr. Wily, the World Robot Championship returns as the **Grand
Prix**: a real tournament with venues, judges, prize money and live commentary. Its new sponsor, **Mr. Y**, is
obviously Wily. Everyone says so, once an act, in a new way each time. He is.

**The two layers** (BRIEF §1): a sports tournament played straight (matches, scorecards, a bracket, a rival, a
championship), and a love letter to game history (venues that are eras of games, a museum of Rockman 1-5, and a villain
whose plan is to force the whole world to upgrade to 16 bits, told in the last NES Rockman).

| Act | Where (engine id, meta index) | What happens | Scenes | Tier |
|---|---|---|---|---|
| **0. Opening** | Opening-lite (`$10`, meta 0); the attract crawl (Could) | NEW GAME goes straight to the players' tunnel (R4.4). Four lane judges teach the scorecard; the parade passes; the masked **entrant 10** (no name spoken) and the late **entrant β**; Mr. Y "upgrades" the mascot | S01-S08 | Must (S02, S05 lines: Could, Should) |
| **I. Round one** | the bracket; any 4 venues (`$00-$07`, meta 1-8) | Matches, scorecards, prize money. POWER after the 2nd win, JET after the 4th. Bass β crashes the bracket and every other match is POSTPONED | S09-S16 | Must |
| **II. HALFTIME RIOT** | `$11`, meta 9 | The stadium at night, overrun by the **rejects** Mr. Y hired. Entrant 10 holds the crowd, blocks Bass's last shot and names himself: **"Break Man."** Rule 9 is invoked | S17-S20 | Must (S20 pages 3-6 Should; S21 Could) |
| **III. Round two** | the other 4 venues | The countdown; the trophy ceremony; Mr. Y steals the GP Cup with a crane claw and flies it to his museum | S22-S25 | Must (S22-S23 Could) |
| **IV. Hall of Fame** | H1, H3, H5 (`$16`, `$18`, `$1A`; meta 14, 16, 18); H2, H4 Should | A museum of Rockman 1-5 whose exhibits Mr. Y has "upgraded" to MK-VI. Plaques; the Super Adaptor; a fake Break Man; **the unmasking** in H5's throne room, two masks deep: "WE KNOW." Project SUPER | S26-S33 | Must (H2, H4 lines Should) |
| **V. Project SUPER** | W2, W3 (`$1C`, `$1D`; meta 20, 21); W1 Could | The Bracket of Doom (data copies), Bass β's second duel, WILY MACHINE 6.5 over a "Mode 7" floor, the Capsule and Break Man's gift, the escape; Break Man catches Rock and Wily; the arrest | S34-S41 | Must (S35 Could) |
| **VI. The ending** | the stadium; the Hall | R4.1's order: the podium and Bass's vow; the CAPCOM TIMES; the credits; the rating and Break Man's debrief; **LIGHTS OUT**; the sixth wing; TO BE CONTINUED. The last sound is pulse 1 alone | S42-S48 | Must (S45 Could) |
| **Post-game** | the bracket | "Welcome back, champion." | S49 | Must (S50, S51 Won't) |

**STORY_BEAT** (FILE `$013`, `meta.md` §1.6; this doc owns the values). A monotonic act counter used to pick dialogue
variants. The bracket logic reads STAGE_CLEAR and EVENTS (`meta.md` §3.6), never this byte.

| Value | Name | Set when | What it changes in text |
|---|---|---|---|
| `$00` | NEW | file created | — |
| `$01` | OPENED | Opening-lite cleared | bracket lines start |
| `$02` | RIOT_DONE | HALFTIME RIOT cleared (EVENTS b3) | the countdown (S24) |
| `$03` | CUP_STOLEN | the trophy theft (EVENTS b4) | the Hall of Fame map lines; Mr. Y's heckles |
| `$04`-`$08` | H1 … H5 | the highest wing cleared (H2 and H4's values are skipped while they are Should) | heckle variants |
| `$09` | UNMASKED | the unmasking (EVENTS b6) | the speaker "MR. Y" becomes "DR. WILY" in every table |
| `$0A`-`$0B` | W1, W2 | castle stages cleared (W1 is Could; its value is skipped in v1.0) | W3 heckles |
| `$0C` | CHAMPION | W3 cleared (the ending seen) | the post-game line (S49); the file card's ★ |
| `$0D`-`$FF` | reserved | | |

---

## 1. Tone guide

### 1.1 The four voices

The game speaks in four registers. Every line belongs to one; a scene may mix them, a single line should not.

| Voice | What it sounds like | Model | Example |
|---|---|---|---|
| **Sports broadcast, played straight** | Cossack and Kalinka call the action like a real tournament: stats, rules, "the judges are not pleased". The comedy is treating a robot brawl as a sporting event | CX's straight-faced villain inversion (cx SUMMARY §5) | C: "A CLEAN MATCH FROM ROCKMAN. THE JUDGES WILL REMEMBER THAT SLIDE." |
| **CX-level silliness** | Absurd escalation, fourth-wall winks, jokes that are mechanics (a YES that costs a bolt, a seal union, a mascot full of the sponsor's helium) | CX's 24 moments; 4MI's ENGRISH | K: "DON'T HURT THE SEALS! THEY'RE UNION WORKERS!" |
| **Sincere game-history affection** | Plaques, credits, thanks to fan designers, true trivia told with care. Never sarcastic about the games it quotes | 4MI's tributes | A plaque: "BEAT A MASTER, TAKE HIS WEAPON: THE RULE EVERY ROCKMAN SINCE HAS FOLLOWED." |
| **The farewell to 8-bit** | Quiet, warm, a little sad. Used rarely: Wily's speech, WILY MACHINE 6.5, the lights going out channel by channel, the sixth wing | the last NES Rockman (1993) | L: "EVERY MACHINE I BUILD WILL BE OUTDONE BY THE NEXT ONE. THAT ISN'T SAD, ROCK. THAT'S THE JOB." |

### 1.2 Rules

1. **A joke should be a mechanic or sit on one** (CX lesson 2). The best lines comment on what the player just did: a
   death, a secret, a weakness.
2. **Nobody is cruel.** The champions are good-natured rivals rebuilt by their fan designers (BRIEF §2): they
   trash-talk and they lose gracefully. Kalinka is a child: her jokes are never mean. Deaths are teased, never mocked.
3. **Content notes (R3.4, Must; design-11, design-12).** Tomahawk Man and Flame Man draw on real cultures in vanilla.
   GP's jokes target the *game genres* their venues quote, never a culture.
   - **Tomahawk Man is the frontier's rodeo showman, strict about duel etiquette**: a champion and the Sheriff's friend,
     never the outlaw, never the stoic-noble type. His arena is the **HIGH NOON MESA** (no graves), his secret arena
     **THE RODEO RING**, and the draw is a **judged tournament event** (a flag judge, the scoreboard). No Boot Hill line,
     no totems; his weakness gag is a sneeze.
   - **Flame**: no "Oil Sultanate" anywhere; the joke is the oil field and Prince of Persia's mechanics (pressure
     plates, loose floors, the shadow, the hourglass). Screen 18's backdrop is domes and a full moon (art). The vizier
     exists only as an obvious Wily-in-costume gag (Should); in v1.0 the venue's Mr. Y gag is a sponsor tapestry.
   - Cossack is a scientist and a father, not a Russian caricature: one "in my country" joke per venue at most.
   - The doping trade-off (Y-TURBO, Could) is about **cheating**, never drugs: it is a chip.
4. **Every fact is true.** A line that states game history must match Appendix A, with its source and confidence. A
   riddle may be oblique; it may not be wrong. Folklore is worded as folklore ("THEY SAY…", R3.9).
5. **Names (R3.3).** The on-screen venue names are SUMMIT CLIMBER, SKY ACE, LOST JUNGLE, PERSIAN PALACE, EDO NINJA ROW,
   HIGH NOON FRONTIER, HERO'S QUEST and ATLANTIS RUINS. **No third-party trademark or character name appears on
   screen**: not in a title, a joke, a hint or a plaque. That includes other companies' consoles and handhelds: plaques
   say "THE 8-BIT CONSOLE", "THE 16-BIT CONSOLE", "THE HANDHELD" (the venue docs set the precedent by cutting "From the
   Game Boy?"). **Plaques describe; they don't name** ("A FALLING-BLOCK PUZZLE BORN IN MOSCOW IN 1984"), which keeps the
   commentators' "can't say the trademark" gag coherent. Capcom's own names may be nodded to: 1942, 1943, Gun.Smoke,
   DuckTales, Tango, the Sakugarne, the Yashichi. Design notes in this doc may name anything.
6. **Short, and fitted** (R1.4). A pop-up page is ≤ 2 lines × 28 cells with ≤ 24 distinct glyphs; a window page ≤ 4
   lines; a plaque ≤ 9. If a line needs more, it is two pages or it is cut. `fit.py` enforces it.
7. **Toggleable.** Every commentator line obeys CONFIG ANNOUNCER (ON / DEATHS ONLY / OFF, `meta.md` §11.1). Scenes and
   the debrief are not commentary and always play; START skips a scene after its first viewing (R3.8).
8. **ENGRISH (Could) never touches story text, hints or help pages** (`meta.md` §12): it is a menu joke (§9), with one
   deliberate exception, Break Man's perfect-score line, a nod to 4MI's (S47).
9. **The Wily gag plays once per act, in new words each time** (R4.4, R3.9; §1.3). Nobody repeats "It's definitely
   Wily."
10. **Break Man's disguise is respected** (R4.2; §1.3's mirror gag). Only Rock says "Blues?", twice; Light says the name
    once, at the very end. **The plaques are the one exception** (R3.9, design-23): a museum labels its exhibits by
    their real names, so the Rockman 3-5 plaques say BLUES.
11. **Quoted lines from other games are paraphrased, never verbatim, in both languages** (R8.4, R3.3's spirit). A joke
    on a famous line keeps its rhythm in new words (HERO'S QUEST's King, Princess and Knightlord; ENGRISH's classics).
    The genre's formulas with GP's own nouns ("A METSLIME DRAWS NEAR!", the command menu) are conventions, not quotes.
    Vanilla Rockman 6's own text is this game's, and is kept verbatim where §5.2, S44 and S45 say so.

### 1.3 The running gag: Mr. Y is Wily, once per act

The gag escalates without the villain ever conceding, until the unmasking, where he concedes too eagerly and nobody
cares. R4.4 and R3.9 make it **once per act, with new wording each time**:

| Act | Where | The gag | Tier |
|---|---|---|---|
| 0 | S08, the sabotage | Kalinka asks if Mr. Y is Wily; Cossack: "HIS PAPERS SAY MR. Y. ...IN CRAYON." | Must |
| I | S14, the Riot intro | "Registered, actually. Entrant β. Sponsor: Mr. Y." Kalinka doesn't even need to finish the thought | Must |
| II | S17, Riot night | The rejects in the stands: "MR. Y HIRED THEM ALL." | Must |
| III | S25, the theft | His saucer has a Y painted over a W; Light, quietly: "...THAT WAS WILY." | Must |
| IV | S33, the unmasking | Two masks deep. "SURPRISE! IT'S ME, DR. WI-" "WE KNOW." | Must |
| V | S41, the arrest | "IT WAS MR. Y'S IDEA!" "YOU ARE MR. Y." "...MR. Y IS VERY PERSUASIVE." **The one Mr. Y gag of the ending**, and its only alias gag (R4.1 step 4, R8.5) | Must |
| VI | S44, the CAPCOM TIMES | Page 1: "MR. Y WAS DR. WILY. WE KNEW." (the press answers S33's "WE KNOW."). Page 4 is the fallback S44.4F, "NEXT YEAR'S SPONSOR: NOT YET ANNOUNCED. COSSACK RELAXES.": **no Mr. Z** (R8.5) | Must |
| — | every venue | one cheap prop, never a line in v1.0: the MR. Y MARU icebreaker, Flame's sponsor tapestry, the Y-MAN mural, the million-ryo poster, the WANTED: ROCKMAN poster (venue docs). Their hooks (BLZ-04, FLM-08, YAM-02, …) are Should, each in its own words | art Must, lines Should |
| — | the judges' desk | a cardboard Mr. Y on the sponsor's chair holds up a "1"; BACK SOON from S26, RESERVED from S33 (`meta.md` §4.0: the chair and its signs are Should) | Should |
| — | Mr. Y's heckles | in JP he speaks an absurdly polite わたくし … でございます and slips into Wily's わし … じゃ when excited; in EN he slips on names: "WELCOME TO MY- TO *A* MUSEUM!" | Must (the v1.0 lines) |

**The mirror gag: Break Man** (R4.2, design-2). Mr. Y's disguise is transparent and he insists on it; everyone calls him
Wily anyway. Break Man's disguise is just as transparent (a visor and a scarf), and **everyone politely plays along**,
because he is honest. His name is not spoken in the Opening (he is "entrant ten"); he names himself at the Riot's 0E.
**Rock says "Blues?" exactly twice** (the Riot's 0E and S40), and Break Man answers "BREAK MAN." both times. **Light
says the name once, in S42**, near the very end. Nobody else says it; the plaques (§1.2 rule 10) are the museum's, not a
character's.

### 1.4 The farewell to 8-bit

The game is the last NES Rockman, and Project SUPER is an upgrade the world did not ask for. The farewell surfaces
four times in v1.0, each in the quiet voice:

1. **Wily's speech** after the unmasking: he is not wrong that the 8-bit era is ending; he is wrong to force it (S33).
2. **WILY MACHINE 6.5**: a machine halfway between 6 and 7, literally, on a floor that only pretends to rotate (S38).
3. **LIGHTS OUT**: the stadium shuts down one sound channel at a time, Light says why that isn't sad, and the last
   sound is pulse 1 alone (S42).
4. **The sixth wing**: the Hall of Fame opens a wing for ROCKMAN 6 (1993), with this game's true history (S43). The
   museum of the past ends on the game you are playing, in silence.

(W1's Upgrade Lab, Could, adds a fifth: the castle upgrading its own palette as you climb, S35.)

### 1.5 Voice per surface

| Surface | Speaker | Register |
|---|---|---|
| In-stage pop-ups | Cossack, Kalinka; Mr. Y (H wings) and Wily (W stages) on respawn; Roll by radio for adaptors; Break Man's whistle lines | broadcast + silliness |
| Story scenes | everyone | all four |
| Boss cards | the panel (English in both languages, as vanilla) | broadcast |
| Judges' debrief | Kalinka | v1.0: tier B, a plain instruction (Must). v1.1: tier A, a riddle that rewards knowing the homage (Should) |
| Chip help pages | the shop's catalogue (Eddie's) | dry, sometimes cryptic |
| Plaques | the museum | sincere; one joke per plaque at most, always last |
| Break Man's debrief | Break Man | terse, fond, never says "good job" outright |

v1.0 draws every speaker as a **16×16 face icon with a name label** (R5.1); portraits are Should.

---

## 2. The cast

Each sheet gives the role, the voice in EN and JP, and the rules for writing them.

### 2.1 Rockman (ロックマン / ロック)

- **Role:** the player; Dr. Light's entrant 9 (he did not compete in the 1st Championship; he stopped it).
- **Arc:** competes in good faith in a tournament everyone knows is rigged, and proves it can be won cleanly.
- **Voice EN:** earnest, polite, brief; deadpan when stating the obvious ("YOU ARE MR. Y."). **JP:** ぼく; です/ます to
  Light (はかせ), plain to friends; vanilla's battle cry 「ゆくぞ!! ラッシュ!」 is kept.
- **Rules:** he speaks only in scenes, never in pop-ups. He says "Blues?" twice (the Riot's 0E, S40). He never calls
  Mr. Y anything but Wily, and only from S25 on.

### 2.2 Break Man (ブレイクマン) = Blues

- **Role:** the masked **entrant 10** (BRIEF §2), Rockman 3's alias. **The NPC is Must** (R4.2): a composite of about
  10 frames from Rock's sheet (visor, scarf, palette; tech's family `$F7`) for the Opening, the Riot, H5's whistle, W3's
  gift, the catch and the debrief. **The playable tag partner is Should** (R0.3 item 2).
- **Arc in v1.0:** registers alone, with no sponsor and no data, and no name on the board (S06); teaches the charge
  shot after a death to the mascot; holds the rioting crowd; blocks Bass's last shot; names himself on the roof (0E);
  answers the fake's whistle in H5 from somewhere off screen; throws Rock the CHAMPION BUSTER when he is losing; catches
  Rock and Wily as the castle falls; gives the debrief. **v1.1 adds** the join (S20 pages 3-6), the call, and the
  walk-out if Rock dopes (S21, Could).
- **Voice EN:** two to six words. "HMPH." "HOLD B." "YOUR TURN." Never explains himself. His whistle comes first.
  **JP:** おれ; 「・・・ふん。」; plain, clipped (だ, しろ); calls Rock 「ロック」.
- **Rules:** never jokes, but is the target of gentle ones (C: "HE BROUGHT HIS OWN THEME MUSIC."). His only long text is
  the debrief (S47).

### 2.3 Bass β (フォルテβ, "Bass beta")

- **Role:** Mr. Y's entrant and the rival. Built from Rockman's own tournament data, gathered by the judges' cameras
  Mr. Y sponsored. The **β** is a version number: he is the beta of the robot Wily will finish in 1995 (Rockman 7's
  Bass), and he hates hearing it.
- **Registration** (R4.3): the bracket has ten numbered slots (the 8 champions, Rockman 9, Break Man 10), so Mr. Y
  registers him as **entrant β**. The Committee is still arguing whether a Greek letter counts as a number.
- **Arc:** sneers at the "original"; crashes the bracket (S14); copies four champions' weapons in duel 1 and blames
  bugs; comes back patched in duel 2 and loses again; at the podium promises the next one "WON'T BE 8-BIT".
- **Voice EN:** loud, contemptuous, insecure about the β. "I'M THE FINAL VERSION!" Calls Rockman "ORIGINAL". **JP:**
  オレ; だ, ぜ, しろ; 「オリジナル」 in katakana; 「オレは さいしゅうばん だ!」.
- **Rules:** never wins a scene; always gets the last word anyway.

### 2.4 Mr. Y (Mr.Y) = Dr. Wily (Dr.ワイリー)

- **Role:** the sponsor; obviously Wily (§1.3). Before the unmasking every table names him "MR. Y"; from STORY_BEAT
  `$09` the same slots read "DR. WILY".
- **The disguise, two masks deep:** a Mr. Y mask (last year's Mr. X face with sunglasses, a Y badge and a second
  moustache) worn over last year's Mr. X mask, worn over Wily. Strictly less effort than last year. The unmasking peels
  both (fortress §4.6).
- **The plan, Project SUPER:** the scorecard cameras record every match; the GP Cup is the data core; with the data he
  built Bass β and the SUPER upgrade, a forced 16-bit conversion of every robot on Earth, all running Wily's own system.
  The trophy is the plan.
- **Voice EN (as Mr. Y):** a game-show host's smarm. "HO HO HO!" Slips: "WELCOME TO MY- TO *A* MUSEUM!" **(as Wily):**
  the classic ranting genius; begs on his knees when beaten. **JP (as Mr. Y):** わたくし, ございます, ございましょう;
  slips into わし and じゃ when excited. **(as Wily):** わし, じゃ, ぞ; 「ワーッハッハッハ!」.
- **Rules:** he never admits it before S33.

### 2.5 Dr. Light (Dr.ライト)

- **Role:** Rockman's sponsor and creator. **Vanilla RM6 gives Light no lines** (`rm6/text.md` §5.7), so every line
  here is new. He speaks by radio (a static frame for a face icon).
- **Voice EN:** warm, wry, tired of Albert's nonsense; the only adult who never raises his voice. **JP:** わし; じゃ,
  のう; calls Rock 「ロック」 and Wily 「ワイリー」.
- **Rules:** Light jokes only about Wily. He says "ALBERT" once (S33, both languages) and "BLUES" once (S42).

### 2.6 Roll (ロール)

- **Role:** pit crew, by radio in v1.0 (her face icon): Rush's adaptors (S04, S12, S13, S29). Princess Roll in HERO'S
  QUEST (`venues_a.md` §2.6, approved: the YES-or-ask-again loop is hers, in new words, KNT.S23, R8.4) is Should with
  the Inn.
- **Voice EN:** brisk, practical, proud of Rush's fittings; she teaches controls in-world. **JP:** わたし; よ, ね;
  「ロック!」.

### 2.7 Dr. Cossack (Dr.コサック) and Kalinka (カリンカ): the commentators

- **Role:** Cossack is head judge and play-by-play; Kalinka is colour commentary and the debrief's speaker
  (`meta.md` §4.1). They sit at the judges' desk.
- **Cossack EN:** a scientist doing sports: precise, dry, fond of statistics and of "LAD". **JP:** わたし; だ, だな;
  「ロックマン」.
- **Kalinka EN:** quick, excited, knows game trivia nobody asked for, calls her father "PAPA". She "hears things": she
  is the one who knows where secrets are. **JP:** わたし; だよ, だね; 「パパ」.
- **Rules:** **one speaker per page**; an exchange is two pages. Cossack states, Kalinka reacts, or the reverse; the
  punchline goes to whoever did not set it up.

### 2.8 Eddie (エディ)

- **Role:** runs **Eddie's Pit Stop**, open from 0 wins after the Opening (`meta.md` §3.8, consistency decision 14).
  Speaks in shopkeeper bleeps. **EN:** "WELCOME! *PIPIPI*" **JP:** 「ピピッ! いらっしゃいませ!」.
- **Rule:** Eddie is never the butt of a moral joke (the venue docs deleted round 1's shoot-Eddie trade-off).

### 2.9 Beat (ビート) and Rush (ラッシュ)

- **Beat:** collected as plates B-E-A-T; each plate is a chip slot (`systems.md` §10). Speaks only "PEEP!" / 「ピィ!」.
  Cossack built Beat in Rockman 5 (A-5.4), so the save's first plate gets a proud Cossack line (§6.2).
- **Rush:** "WOOF!" / 「ワン!」. Wears a **RENTAL** bib on the Committee's loaner jet in SKY ACE's sortie (approved).

### 2.10 The eight champions

Rebuilt by their original fan designers (the vanilla credit cards name them, `rm6/text.md` §5.6). Entrants 1-8 of the
bracket. Each has one personality hook, which drives the bar-fill line (S11) and, in v1.1, the float line, the defeat
line and the W2 shout.

| Champion (DWNB card) | Designer (vanilla card) | Venue (R3.3) | Personality | EN voice | JP voice |
|---|---|---|---|---|---|
| **Blizzard Man** (41) | HIROFUMI OGAWA | SUMMIT CLIMBER | A sunny optimist on a glacier who runs on SOLAR ENERGY and keeps trying to tan | "FRESH POWDER, ROCKMAN!" | おれ, だぜ |
| **Centaur Man** (42) | KAZUKI KIDOGUCHI | ATLANTIS RUINS | A gentleman with a secret even from himself: ABILITY UNKNOWN (it turns out to be gambling) | "EXCITING, IS IT NOT?" | わたし, ですな |
| **Flame Man** (43) | NORITSUGU KUROKAWA | PERSIAN PALACE | A theatrical duelist who bows before every fight and keeps his distance | "EN GARDE!" | わがはい, だ |
| **Knight Man** (44) | DANIEL VALLIE | HERO'S QUEST | A chivalric ham who narrates his own attacks in a battle log | "HARK! HAVE AT THEE!" | われ, であるぞ; なんじ |
| **Plant Man** (45) | NOBUHIRO HOSHINO | LOST JUNGLE | A gentle gardener-explorer; apologises to the flowers | "PLEASE MIND THE PETUNIAS." | わたし, ですよ |
| **Tomahawk Man** (46) | YOSHINOBU SUDA | HIGH NOON FRONTIER | **The frontier's rodeo showman, strict about duel etiquette** (R3.4): tips his hat to the flag judge, waits for the flag every time, bows to the crowd | "STEP RIGHT UP! NOBODY DRAWS BEFORE THE FLAG." | おれ, だぜ; 「さあ ごらんあれ!」 |
| **Wind Man** (47) | MICHAEL LEADER | SKY ACE | A would-be ace pilot with a short attention span | "TALLY-HO! TRY TO KEEP UP!" | おれさま, だぜ |
| **Yamato Man** (48) | RAI ICHIKAWA | EDO NINJA ROW | An honourable samurai, immovable and proud of it (DEFENCE 185, MOBILE 31) | "THIS ONE SHALL NOT MOVE." | せっしゃ, でござる |

### 2.11 Exhibition guests (E1-E3 Could; E4 Won't)

Arcade legends who play by their own games' rules (R3.7: one lobby and one rule-boss arena each; `fortress.md` §3).
Parody names; **the plaques describe the games and never name them** (R3.3).

| Guest | Homage (design notes only) | Personality | Tier |
|---|---|---|---|
| **Block Man** (E1) | a 1984 falling-block puzzle | silent, orderly, mildly annoyed by gaps; speaks by clearing lines | Could |
| **Paddle Man** (E2) | the 1976 brick-breaking game and its 1986 space-paddle successor | a bored goalkeeper who has returned the same ball for decades | Could |
| **Invader Man** (E3) | the 1978 alien-invasion shooter | marches everywhere in step; speaks in descending tones | Could |
| **Maze Man** (E4) | the 1980 maze-chase game | polite, always hungry | Won't (v1) |

"Block Man" is also Rockman 11's Robot Master (2018, Capcom's own): the joke is kept on purpose (S22, Could).

### 2.12 The legacy bosses (the Hall of Fame's MK-VI exhibits)

Museum pieces Mr. Y "upgraded". They do not speak (they are machines); their cards (§5.4) and the plaques (S27) speak
for them. Dark Man MK-VI speaks only in disguise, badly.

| Exhibit | From | Its joke | Tier |
|---|---|---|---|
| **Yellow Devil MK-VI** (H1) | Rockman (1987) | it flies across the room in pieces; knock a piece down and it can't rebuild | Must |
| **Kamegoro Maker MK-VI** (H3 mid-boss) | Rockman 3 (1990) | the turtle machine; its turtles are the way to beat it (fortress §4.3.3) | Must |
| **Gamma MK-VI** (H3) | Rockman 3 (1990) | built by Light and Wily together "for peace"; its head respects only a fist, so you ride its own fist up | Must |
| **Dark Man MK-VI** (H5) | Rockman 5 (1992) | disguised as Break Man, with a flat whistle and an orange scarf; the boss card lies | Must |
| Big Eye MK-VI (H1 mid-boss) | Rockman (1987) | no lines | Must |
| Mecha Dragon MK-VI (H2), Cossack Catcher MK-VI (H4), Doc Robot MK-VI (H3, copying AIR MAN) | Rockman 2, 4, 3 | kept in §4 S28 | Should |

### 2.13 Others

- **Grand Pi-kun** (グランピーくん): the GP mascot, an inflatable robot chick, grumpy because nobody watches the mascot
  (a pun on グランプリ and "grumpy"). Filled with Mr. Y-brand helium, it goes rogue in the Opening. Squeaks only.
- **The rejects** (R4.3; `fortress.md` §2.2): VENDING MAN and CHEER MAN (UMBRELLA MAN Should), the losing entries of
  the fan design contest, hired by Mr. Y for the Riot. They never speak; their `REJECTED` tags and `ACCEPTED!` stamps
  do it for them.
- **The Committee**: offstage; represented by the rulebook, which Cossack reads aloud and occasionally disagrees with.
- **Mr. X, the real one** (Won't, with Mr. X Returns): only his business card ships (H5, S28).
- **Venue NPCs** (the King, the Sage, the Sheriff, the conductor, Six-Shot Sam, the seals' union, the mouse, Tango the
  cat, …): their v1.0 lines are in §4 S15, finalised from the venue docs' drafts.

---
## 3. The scene list, in play order

"Surface" is §10.1's: **POP** = the in-stage pop-up (2 × 28, face icon); **WIN** = the 4 × 28 window (scenes on menu
screens and frozen stages, the debrief, help pages, NPC windows); **PLQ** = a full-screen page; **PNL** = vanilla's boss
panel typer `$3C:$81B1`; **PPU** = a vanilla PPU script; **NEWS** = the vanilla newspaper driver. Placement and order are
the staging docs' (`fortress.md` for non-venue stages, the venue docs for venues; consistency decision 8); this doc owns
the words. Scene ids are stable (other docs cite them), so the ending's play order differs from its numbering: the last
column gives R4.1's step.

| Id | Scene | Trigger and placement (owner) | Surface | Seen / beat | Tier | M | R4.1 step |
|---|---|---|---|---|---|---|---|
| S01 | License line | boot (vanilla script `$1F` + one GP line) | PPU | — | Must | M2 | |
| S02 | Attract crawl | title idle (`meta.md` §2.1) | crawl driver | — | **Could** (R0.3 item 12; meta) | — | |
| S03 | The players' tunnel | Opening 00, READY (fortress §1.3) | POP sequence, script lock | — | Must | M5 | |
| S04 | Roll by radio; the shut stall | Opening 00 | POP | — | Must | M5 | |
| S05 | The parade | Opening 07-08 | POP | — | Must (one line); the float lines **Should** | M5 | |
| S06 | Entrants 10 and β | Opening 08, the last float | POP sequence | — | Must; **no name spoken** (R4.2) | M5 | |
| S07 | The rulebook, folded into the lanes (R4.4) | Opening 01-05: the lane judges, the scoreboard | POP | — | Must | M5 | |
| S08 | Grand Pi-kun; Break Man's tip; the bracket | Opening 09-0B | POP sequence; the tip after a first death to Pi-kun | STORY_BEAT → `$01` | Must | M5 | |
| S09 | Bracket lines | the bracket (`meta.md` §3.3-3.4) | WIN | — | Must | M2/M5 | |
| S10 | Eddie's Pit Stop | the pit stop (`meta.md` §3.8) | WIN | — | Must | M3 | |
| S11 | Per match: card, bar fill, defeat, YOU GET | every champion match | PNL + POP + PPU | — | Must (the defeat line **Should**) | M4-M6 | |
| S12 | POWER hand-off | bracket, 2nd win | WIN | EVENTS b0 | Must | M5 | |
| S13 | JET hand-off | bracket, 4th win | WIN | EVENTS b1 | Must | M5 | |
| S14 | The Riot intro | bracket, after S13 | WIN | EVENTS b2 | Must (the animation Could, meta) | M6 | |
| S15 | Venue NPCs, windows and signs | the 8 venues | WIN / POP | — | Must as listed per venue | M4-M6 | |
| S16 | Game over, RETIRE, unplug | game over; the first RETIRE; a load with IN_MATCH | WIN | — | Must (game over); Should (RETIRE, unplug: meta §1.7) | M3 | |
| S17 | Halftime night | Riot 00 (fortress §2.3) | POP | — | Must | M6 | |
| S18 | Break Man holds the crowd | Riot 06, merged with the help beat (fortress §2.6) | POP sequence | — | Must | M6 | |
| S19 | Bass β, duel 1, and the block | Riot 0D | PNL + POP | RATEFLAGS b2, b4 | Must | M6 | |
| S20 | The reveal and Rule 9 | Riot 0E, in place (R4.2) | WIN | EVENTS b3 on the next bracket visit; b5 Should | Must (the reveal, pages 1-2); **Should** (pages 3-6, the join) | M6 | |
| S21 | Mr. Y's booth; Break Man walks | pit stop row; bracket | WIN | EVENTS2 b5 | **Could** (the bundle, R2.5) | — | |
| S22 | Exhibition badges light | bracket | WIN | EVENTS2 b0-3 | **Could** (R3.7) | — | |
| S23 | Exhibition matches | E1-E3 | PNL + POP + PLQ | — | **Could**; E4 Won't | — | |
| S24 | The countdown | bracket centre, from EVENTS b3 | WIN | — | Must | M6 | |
| S25 | Trophy ceremony and theft | bracket, START on the lit trophy | WIN | EVENTS b4; STORY_BEAT → `$03` | Must | M7 | |
| S26 | The Hall of Fame map | the map, first visit | WIN | — | Must | M7 | |
| S27 | Museum plaques | H1, H3, H5 (fortress §4); the hidden rooms | PLQ | — | Must (H1, H3, H5 as listed); Should (H2, H4 and the rest) | M7 | |
| S28 | Exhibit lines; Mr. X's card | the wing bosses; H5 room 19 | POP; PLQ | RATEFLAGS b1 | Must / Should as listed | M7 | |
| S29 | The Super Adaptor | the Hall of Fame map after H3 (FORMS.SUPER is set at H3 12, no YOU GET card) | WIN | EVENTS2 b4 | Must | M7 | |
| S30 | H5: the fake Break Man | H5 15 (fortress §4.5.2) | PNL + POP | — | Must (the WRONG NOTE staging); **Should** (TWO BREAK MEN) | M7 | |
| S31 | Mr. Y's and Wily's heckles | every respawn in H1-W3 (P1) | POP | — | Must (the v1.0 lines, §6.5) | M7-M8 | |
| S32 | The cup on the pedestal | H5 15, after Dark Man (fortress §4.6 step 1) | WIN | — | Must | M7 | |
| S33 | The unmasking; Project SUPER | H5 15 (fortress §4.6) | WIN + a typed black page | EVENTS b6; STORY_BEAT → `$09` | Must | M7 | |
| S34 | The Super Wily Castle map | the map, first visit | WIN | — | Must | M8 | |
| S35 | W1: the Upgrade Lab | W1 | POP | — | **Could** (R0.3 item 5) | — | |
| S36 | W2: the Bracket of Doom | W2 08, the hub; the TAG! card | POP | — | Must (the hub, TAG!); **Should** (the shouts) | M8 | |
| S37 | Bass β, duel 2 | W2 11, the Championship Ring | PNL + POP | — | Must | M8 | |
| S38 | WILY MACHINE 6.5 | W3 05-06 | PNL + POP | — | Must | M8 | |
| S39 | The Capsule; the gift; the PA; the jammed pod | W3 06, the escape 07-0C | POP | — | Must | M8 | 1 (the escape) |
| — | The castle pixelates | ending, fortress §6.1 scene 2 | (no text) | — | Must | M8 | 2 |
| S40 | Break Man catches Rock and Wily | ending scene 3, the bay | WIN | — | Must; the carry art **Should** | M8 | 3 |
| S41 | The arrest; the podium and Bass's vow | ending scenes 4-5 | WIN | STORY_BEAT → `$0C` | Must | M8 | 4, 5 |
| S44 | The CAPCOM TIMES | ending scene 6 | NEWS | — | Must | M8 | 6 |
| S45 | The credits | ending scene 7: v1.0 the vanilla staff roll with GP text and the DWNB cards (fortress §6.2); the victory lap **Could** | PPU (+ POP on the lap) | — | Must (the roll's text); **Could** (the lap) | M8 | 7 |
| S46 | The championship rating | ending scene 8 (`meta.md` §6) | meta's screen | — | Must (labels) | M8 | 8 |
| S47 | Break Man's debrief | ending scene 8 | WIN | — | Must | M8 | 8 |
| S42 | LIGHTS OUT | ending scene 9 | WIN | — | Must | M8 | 9 |
| S43 | The sixth wing | ending scene 10, H5 room 19 finished | PLQ (silent) | — | Must | M8 | 10 |
| S48 | TO BE CONTINUED | ending scene 11 (vanilla `$88`, typed in silence) | PPU | — | Must | M8 | 11 |
| S49 | Post-game bracket intro | bracket, first visit after the ending | WIN | EVENTS b7 | Must | M8 | |
| S50 | Mr. X Returns | — | — | — | **Won't** (v1) | — | |
| S51 | Bass Mode line swaps | — | — | — | **Won't** (v1) | — | |

**The ending, in R4.1's order** (`fortress.md` §6.1 stages it): the escape (S39) → the castle pixelates → Break Man
catches Rock and Wily (S40) → the arrest, with **one** use of the Mr. Y gag (S41) → the podium and Bass's vow (S41) →
the CAPCOM TIMES, no `$94` (S44) → the credits (S45) → the rating and Break Man's debrief (S46, S47) → **LIGHTS OUT**
(S42) → the sixth wing (S43, silent) → TO BE CONTINUED (S48, silent). **The last sound is pulse 1 alone.** Round 1's
order (lights out, sixth wing, newspaper, lap, rating) and fortress round 1's door-holding and roof Break Man variants
are withdrawn (design-1).

---
## 4. Scripts

Each scene: where it plays (the staging doc's placement), then its rows. Line widths obey §10.3 (`fit.py`).

### 4.0 The arcs at a glance

**Break Man's beats** (the 4MI Proto Man pattern; the CX Quick Man pattern returns with the partner in v1.1):

| # | Scene | What he does | Helps how | v1.0 / later |
|---|---|---|---|---|
| BM-1 | S06, the Opening | Rides the last float, masked, as **entrant ten**; no name is spoken (R4.2) | — | Must |
| BM-2 | S08, after a first death to Pi-kun | His whistle, then "HOLD B. LET GO WHEN YOU GLOW." (design-2: the high striker teaches the charge first) | the charge tip | Must |
| BM-3 | S18, Riot 06 | Breaks the rubble, then holds the reject crowd: "GO. I'VE GOT THE CROWD." | clears the set piece | Must |
| BM-4 | S19, Riot 0D | Steps in front of the BASS BLASTER; to Bass: "ENTRANT NUMBER TEN." | blocks the overdrive | Must |
| BM-5 | S20, Riot 0E | "...BLUES?" "BREAK MAN." The first time the name is spoken; Rule 9's pages 1-2 | — | Must; the join (pages 3-6) Should |
| BM-6 | S30, H5 | His real whistle answers the fake's wrong note, from off screen | ends the disguise | Must; TWO BREAK MEN (in person) Should |
| BM-7 | S39, W3 | The gift: the CHAMPION BUSTER when Rock's HP falls below 6 | SC11 | Must |
| BM-8 | S40, the bay | Catches Rock and Wily: "THIS TIME." "BLUES?" "BREAK MAN." | Rockman 3's ending, answered | Must; the carry art Should |
| BM-9 | S47 | The debrief, then "...HMPH." | the post-game hint | Must |
| (bundle) | S21 | Walks if Rock takes Y-TURBO; pause row `N0` | the moral cost | Could |

**Bass β's beats:** S06 (entrant β, "I'M THE FINAL VERSION!"), S14 (the bracket), S19 (duel 1, the copies, "THE BETA BUILD HAS... BUGS!"),
S37 (duel 2, patched against your favourite weapon), S41 (the podium vow: "NEXT TIME IT WON'T BE 8-BIT").

**Mr. Y / Wily:** §1.3's ladder; S25 (theft), S26 (map), §6.5 (heckles), S32-S33 (the unmasking and Project SUPER),
S34-S39 (the castle), S41 (the arrest: the ending's one alias gag), S44 (the press: "WE KNEW."; no Mr. Z, R8.5).

### Act 0: the Opening

#### S01 License line [engine-ok] · Must

Vanilla script `$1F` (the copyright lines) plus one line, English in both languages, as vanilla's boot screen is. The
main font (A=`$0B`) has `:` but no `-`.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S01.1 | M | sys | LBL | — | ROCKMAN 6 GP: A FAN PATCH. / NOT MADE BY CAPCOM. | |

#### Boot and menus: the health notice and the menu sentences · Must

`meta.md` §2.1 step 3 and §11: the notice shows on every power-on for at least 120 frames (R3.5). The difficulty panels
carry one description each; HARD describes v1.0's HARD (R2.9). Every other menu word is a label (§10.5).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| SYS.HEALTH | M | sys | WIN | — | THIS GAME HAS FLASHES. / IN CONFIG, FLASHES: REDUCED / TURNS EVERY FLASH INTO A / GENTLE FADE. | このゲームには てんめつする / えんしゅつが あります。 / CONFIGの FLASHESを REDUCEDに / すると すべて フェードに なります。 |
| SYS.CASUAL | M | sys | WIN | — | HALF DAMAGE, MORE LIVES AND / KINDER TIMING EVERYWHERE. | ダメージ はんぶん、ざんき おおめ。 / タイミングも ゆったり。 |
| SYS.NORMAL | M | sys | WIN | — | THE GRAND PRIX AS INTENDED. / THE JUDGES ARE WATCHING. | ほんらいの グランプリ。 / しんさいんが みているぞ。 |
| SYS.HARD | M | sys | WIN | — | 1.5X DAMAGE, FEWER DROPS, NO / REFILL ON RESPAWN. / GOOD LUCK. | ダメージ 1.5ばい、アイテム すくなめ。 / ふっかつ しても かいふく なし。 |
| SYS.LAG | M | sys | WIN | — | SET IT TO YOUR TV'S LAG. IT / WIDENS EVERY REFLEX WINDOW. | テレビの おくれに あわせて。 / はんしゃの ゆうよが のびる。 |
| SYS.FLASH | M | sys | WIN | — | REDUCED TURNS EVERY FLASH / INTO A GENTLE FADE. | REDUCEDで てんめつが / やさしい フェードに なる。 |
| SYS.CASUALBIT | M | sys | WIN | — | WIDER REFLEX WINDOWS, LONGER / TIMERS, MORE CHECKPOINTS AND / EASIER SECRETS. NO SHAME. | はんしゃの ゆうよ ひろめ、 / タイマー ながめ、チェックポイント / ふえる。ひみつも みつけやすい。 |
| SYS.LOWER | M | sys | WIN | — | THIS MAKES THE FILE EASIER / THAN IT STARTED, FOR GOOD. / ▶NO YES | ファイルが はじめより やさしく / なります。もとには もどせません。 / ▶いいえ はい |

#### S02 Attract crawl · Could (R0.3 item 12; `meta.md` §2.1)

Replaces vanilla scripts `$50-$5E` (`rm6/text.md` §5.1) when it ships. It keeps vanilla's first card, `IN THE YEAR
20XX AD・・・`, untouched, and vanilla's bytecode driver (`$3D:$BD00`); any button skips it. **R4.4: this is the one
intro**; NEW GAME never plays it, it goes straight to the tunnel. Panel 5's Mr. Y is drawn as last year's Mr. X with a Y
badge and a second moustache (the X→Y repaint fortress round 1 had in its intro); the crawl does **not** say "Wily":
Act 0's one Wily gag is S08's.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S02.1 | C | scene | PLQ | — | A YEAR AGO, ITS OWN SPONSOR, / MR. X, HIJACKED THE FIRST / WORLD ROBOT CHAMPIONSHIP. / ROCKMAN STOPPED HIM. MR. X / WAS DR. WILY ALL ALONG. | きょねん だい1かい せかいロボット / せんしゅけんは スポンサーの / Mr.Xに のっとられた。 / ロックマンが それを とめた。 / Mr.Xの しょうたいは / Dr.ワイリー だった。 |
| S02.2 | C | scene | PLQ | — | WILY WENT TO JAIL. / THE CAPCOM TIMES WARNED HE / COULD BUILD A JAILBREAK / ROBOT IN HIS CELL. THIS YEAR / THE JAIL SAYS HE IS STILL / THERE. | ワイリーは ろうやへ。 / カプコンタイムスは 「ろうやで / だつごくよう ロボットを / つくるかも」と かいた。 / ことし けいむしょは / 「まだ いる」と はっぴょう。 |
| S02.3 | C | scene | PLQ | — | NOW THE COMMITTEE WANTS ITS / HONOUR BACK. PRESENTING THE / WORLD ROBOT GRAND PRIX! / EIGHT VENUES. EIGHT / CHAMPIONS. REAL JUDGES. REAL / PRIZE MONEY! | いいんかいは めいよばんかいを / ちかった。 / せかいロボット グランプリ / かいさい! 8つの かいじょう、 / 8にんの チャンピオン、 / ほんものの しんさと しょうきん! |
| S02.4 | C | scene | PLQ | — | THE CHAMPIONS ARE BACK, / REBUILT BY THE FANS WHO / DESIGNED THEM. | チャンピオンたちが かえってきた。 / かれらを うみだした ファンの / てで パワーアップ して! |
| S02.5 | C | scene | PLQ | — | AND THIS YEAR'S SPONSOR: / THE GENEROUS, THE / MYSTERIOUS... MR. Y! | そして ことしの スポンサーは・・・ / ナゾの だいふごう / Mr.Y! |
| S02.6 | C | scene | PLQ | L | WHOEVER MR. Y IS, IF HE'S / PAYING, SOMEONE HONEST HAD / BETTER WIN IT. ENTER, ROCK. | Mr.Yが だれで あれ、 / かねを だすなら / しょうじきものが かたねば。 / でるのじゃ ロック。 |
| S02.7 | C | scene | PLQ | R | LET'S GO, RUSH! | ゆくぞ!! ラッシュ! |

S02.7's JP is vanilla's own line (`$4A`). S02.2 sets up S44's page 2 (the cardboard Wily) without reprinting `$94`.

#### S03 The players' tunnel · Must

Opening 00 (fortress §1.3): READY, then a pop-up sequence under a script lock (text v1a at M5, fortress §1.1). Light
speaks by radio.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S03.1 | M | scene | POP | L | THIS YEAR IT'S A REAL / TOURNAMENT, ROCK. | ロック、ことしは ほんものの / たいかい じゃ。 |
| S03.2 | M | scene | POP | L | JUDGES, POINTS, PRIZE MONEY. / WIN IT CLEANLY. | しんさいん、てんすう、しょうきん。 / せいせいどうどうと かつのじゃぞ。 |
| S03.3 | S | flavour | POP | R | AND MR. Y, DOCTOR? | Mr.Yの ことは? |
| S03.4 | S | flavour | POP | L | WIN CLEANLY, AND KEEP AN EYE / ON HIM. | せいせいどうどうと。そして / あいつから めを はなすな。 |

#### S04 Roll by radio; the shut stall · Must

Opening 00. Roll is a face icon on the radio (no Roll sprite). Eddie's stall has its shutter down; the shop opens after
the ceremony (consistency decision 14, `meta.md` §3.8).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S04.1 | M | scene | POP | Ro | PIT CREW HERE! RUSH GETS HIS / ADAPTORS LATER. GOOD LUCK! | ピットクルーよ! ラッシュの / アダプターは あとでね! |
| S04.2 | M | stage | LBL | sign | PIT STOP OPENS AFTER THE / CEREMONY | |
| S04.3 | S | flavour | POP | E | *PIPIPI* ...CLOSED! / BACK AFTER THE CEREMONY! | ピピッ・・・ じゅんびちゅう! / かいかいしきの あとで! |

#### S07 The rulebook, folded into the lanes · Must

R4.4 and design-4: the rules are not a lecture. Each lane judge announces his own scorecard row as Rock finishes the lane
(fortress §1.3: OPN-02…05); Cossack reads the card over the PA. The scoreboard at 05 adds the fifth judge, the medals and
Rule 9 (the setup for S20). Rule 8 is Should.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S07.1 | M | scene | POP | C | DAMAGE JUDGE: %N% OUT OF 10. / A SPLASH OR A FALL COSTS 3. | ダメージしんさ %N%てん! / おちたり ぬれたら マイナス3。 |
| S07.2 | M | scene | POP | C | TIME JUDGE: %N% OUT OF 10. / BEAT THE LIMBO CLOCK FOR 10. | タイムしんさ %N%てん! / じかんない なら 10てん。 |
| S07.3 | M | scene | POP | C | STYLE JUDGE: %N% OUT OF 10. / RING IT FIRST TRY FOR A 10! | スタイルしんさ %N%てん! / いっぱつで ならせば 10てん! |
| S07.4 | M | scene | POP | C | SECRETS JUDGE: %N% OUT OF 10. / YOU FOUND THE HIDDEN ROOM! | シークレットしんさ %N%てん! / かくしべやを みつけたな! |
| S07.5 | M | scene | POP | C | SECRETS JUDGE: ? / THE JUDGES KNOW EVERY ROOM. | シークレットしんさ ? / しんさいんは かくしべやを しってる。 |
| S07.6 | M | scene | POP | C | FOUR JUDGES: %N% OF 40. / THE FIFTH SCORES VARIETY! | 4にんの しんさで %N%てん! / 5にんめは バラエティを みるぞ。 |
| S07.7 | M | scene | POP | K | VARIETY IS WORTH THE MOST! / THE JUDGES *LIKE VARIETY*! | バラエティが いちばん たかいよ! / しんさいんは *いろんな ぶきが すき*! |
| S07.8 | M | scene | POP | C | MEDALS AT 40, 60, 80 AND 95. / PRIZES ARE PAID IN BOLTS. | メダルは 40 60 80 95てん。 / しょうきんは ボルトで しはらう。 |
| S07.9 | M | scene | POP | C | AND RULE 9: IF A SPONSOR / MEDDLES, NAME A TAG PARTNER. | ルール9: スポンサーが じゃまを したら / タッグを くめる! |
| S07.10 | S | flavour | POP | K | WHAT HAPPENED TO RULE 8? | ルール8は? |
| S07.11 | S | flavour | POP | C | RULE 8: DO NOT ASK ABOUT / RULE 8. | ルール8: ルール8に ついて / きいては ならない。 |

S07.4 and S07.5 are one judge's two outcomes (the dressing room found, or not: fortress §1.3, 04).

#### S05 The parade · Must (one line); the float lines · Should

Opening 07-08 (fortress §1.4): one float on screen at a time, each with its champion's idle frame. v1.0 plays one line
as the parade begins (it is also the CROWD FAVOURITE tell); **the float lines are Should** (fortress's first text trim),
one line per champion as Rock reaches the float (R4.4: "the roll call is the float lines only").

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S05.0 | M | scene | POP | K | THE CHAMPIONS' PARADE! / HIGH-FIVE THEM AS THEY PASS! | チャンピオンの パレード! / とおりすがりに ハイタッチ! |
| S05.1 | S | flavour | POP | Blizzard | BRING SUNSCREEN TO MY MATCH, / ROCKMAN. I'M SERIOUS! | ひやけどめを もってこいよ! / マジだぜ! |
| S05.2 | S | flavour | POP | Wind | ACE PILOT WIND MAN! TRY TO / KEEP UP. NOBODY DOES! | エース ウインドマンさまだ! / ついてこれるかな? |
| S05.3 | S | flavour | POP | Plant | WELCOME! PLEASE MIND THE / FLOWERS IN MY JUNGLE. | ようこそ! ジャングルの おはなを / ふまないで くださいね。 |
| S05.4 | S | flavour | POP | Flame | WELCOME TO MY PALACE. THE / FLOOR IS... MOSTLY SAFE. | わがはいの きゅうでんへ ようこそ。 / ゆかは・・・ だいたい あんぜんだ。 |
| S05.5 | S | flavour | POP | Yamato | THIS ONE SHALL WAIT FOR YOU. / THIS ONE NEVER MOVES. | せっしゃ まって おるで ござる。 / せっしゃは けっして うごかぬ。 |
| S05.6 | S | flavour | POP | Tomahawk | STEP RIGHT UP! TWELVE PACES, / AND NOBODY DRAWS EARLY! | さあ ごらんあれ! 12ほ はなれて / フライングは なしだぜ! |
| S05.7 | S | flavour | POP | Knight | HARK! A CHALLENGER NEARS! / ...THAT IS THEE. HARK! | きけ! ちょうせんしゃが きたぞ! / ・・・なんじの ことだ。 |
| S05.8 | S | flavour | POP | Centaur | MY SPECIALTY? ABILITY / UNKNOWN. EVEN TO ME! | わたしの とくぎ? ふめい です。 / わたしにも わかりません! |

#### S06 Entrants 10 and β · Must

Opening 08, at the parade's end (fortress §1.3): the last float carries the NPC Break Man in a dimmed, masked palette.
His whistle (the Must jingle) plays first. **No name is spoken** (R4.2): he is "entrant ten" until the Riot's 0E.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S06.1 | M | scene | POP | K | ENTRANT TEN! SPONSOR: NONE. / DATA: NONE. NAME: ...NONE? | エントリー10! スポンサー なし。 / データ なし。なまえ・・・ なし? |
| S06.2 | M | scene | POP | C | HE BROUGHT HIS OWN / THEME MUSIC. | テーマソングは もちこみ / らしい。 |
| S06.3 | M | scene | POP | K | AND A LATE ENTRY, WITH ONE / MINUTE TO SPARE: ENTRANT β! | そして かけこみ エントリー! / ぎりぎり とうろく: ナンバーβ! |
| S06.4 | M | scene | POP | B | SO YOU'RE THE ORIGINAL. / I'M THE FINAL VERSION! | おまえが オリジナルか。 / オレは さいしゅうばん だ! |
| S06.5 | S | flavour | POP | C | β IS A VERSION NUMBER. MR. Y / SAYS HIS ROBOT IS IN BETA. | βは バージョンだ。Mr.Yいわく / まだ ベータばん だそうだ。 |

Bass drops in, shakes the screen on S06.4, and dashes off (fortress §1.3, 08).

#### S08 Grand Pi-kun; Break Man's tip; the bracket · Must

Opening 09 (the sabotage, ≈ 6 s, controls locked), 0A (the boss), 0B (the walk-out). S08.2-S08.4 are **Act 0's one
Wily gag** (R4.4). Break Man's tip plays **only after a first death to Pi-kun** (design-2), as a pop-up with his face
icon and his whistle first; he is not on screen. The bracket line plays in the bracket's window on its first frame.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S08.1 | M | scene | POP | K | GIVE IT UP FOR OUR MASCOT: / GRAND PI-KUN! | マスコットの グランピーくん / です! はくしゅ~! |
| S08.2 | M | scene | POP | C | WHO FILLED THE MASCOT WITH / MR. Y BRAND HELIUM? | だれだ? マスコットに Mr.Yの / ヘリウムを いれたのは。 |
| S08.3 | M | scene | POP | K | PAPA... IS MR. Y ACTUALLY / WILY? | パパ・・・ Mr.Yって ほんとは / ワイリーじゃ ないの? |
| S08.4 | M | scene | POP | C | HIS PAPERS SAY MR. Y. / ...IN CRAYON. | しょるいには Mr.Yと ある。 / ・・・クレヨンで。 |
| S08.5 | M | scene | POP | BM | HOLD B. / LET GO WHEN YOU GLOW. | Bを おしつづけろ。 / ひかったら はなせ。 |
| S08.6 | M | scene | POP | K | THE MASCOT IS DOWN! THE / GRAND PRIX IS OPEN! | マスコット ダウン! / グランプリ かいまく~! |
| S08.7 | M | scene | WIN | K | HERE'S THE BRACKET! PICK ANY / VENUE. SELECT: PIT STOP. | これが トーナメントひょう! すきな / かいじょうを えらんでね。セレクトで ピット! |
| S08.8 | S | flavour | POP | C | SOMEONE PLEASE RETURN THE / MASCOT TO THE GIFT SHOP. | だれか マスコットを ばいてんへ / もどして おいてくれ。 |
| S08.9 | M | stage | LBL | board | PI-KUN 16-BIT EDITION | |

The Opening's hooks, deaths and hints are §6.4 and §7.2. **Opening page count** (R4.4): the Must scene rows of S03-S08
are 25 pop-up pages = **12.5 scene pages** of 4 × 28, against the cap of 15 (`fit.py` counts them; a WIN row counts as
two pop-up pages).

### Act I: round one

#### S09 Bracket lines · Must

Kalinka in the bracket's window (`meta.md` §3.3-3.4 own the states). The bracket's node labels use the stage-select font,
which has no `! ? ' :` (§10.1), so every sentence is in the new engine's window.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S09.1 | M | scene | WIN | K | THE FINAL? WIN SOME MATCHES / FIRST! | けっしょう? まずは / しあいに かってから! |
| S09.2 | M | scene | WIN | K | RAIN DELAY! ...IT ISN'T / RAINING. IT'S BASS. | あめで えんき! ・・・ふってないけど。 / フォルテの せい。 |
| S09.3 | S | flavour | WIN | K | A REMATCH! THE JUDGES LOVE A / COMEBACK. | さいせん! しんさいんは / カムバックが だいすき。 |
| S09.4 | S | flavour | WIN | K | THAT STAR MEANS YOU FOUND / THE BACK WAY. | その ほしは うらみちを / みつけた しるし。 |
| S09.5 | C | flavour | WIN | K | ONE MORE SECRET EXIT: / %NAME%'S VENUE! | あと ひとつ! / %NAME%の ひみつの でぐち! |

S09.5 is the Exhibition badge's HALF state (Could, with the Exhibitions).

#### S10 Eddie's Pit Stop · Must

The pit stop window (`meta.md` §3.8). Bleeps are text, not SFX.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S10.1 | M | scene | WIN | E | WELCOME! *PIPIPI* / BOLTS IN, CHIPS OUT! | ピピッ! いらっしゃいませ! / ボルトを いれると チップが でます! |
| S10.2 | M | scene | WIN | E | THANK YOU! *PIPIPI* | まいど! ピピッ! |
| S10.3 | M | scene | WIN | E | NOT ENOUGH BOLTS! / GO WIN SOMETHING! | ボルトが たりません! / かってきて! |
| S10.4 | S | flavour | WIN | E | NO REFUNDS. I DON'T HAVE / ARMS. | へんぴんは できません。 / うでが ないので。 |
| S10.5 | S | flavour | WIN | E | EVERY CHIP IS AN EXCELLENT / CHOICE. THAT ONE TOO. | どの チップも おめが たかい。 / それも。 |
| S10.6 | S | flavour | WIN | E | SLOTS? BEAT'S PLATES MAKE / SLOTS. I JUST SELL. | スロットは ビートの プレートで / ふえます。わたしは うる だけ。 |
| S10.7 | S | flavour | WIN | E | COME BACK SOON! I'M HERE. / I'M A SHOP. | また きてね! ずっと います。 / おみせ なので。 |
| S10.8 | C | flavour | WIN | E | TWO PARTS, ONE CHIP. / EDDIE'S MATH! | パーツ ふたつで チップ ひとつ。 / エディけいさん! |
| S10.9 | C | flavour | WIN | E | SHOP'S CLOSED. IT'S 1993! / *PIPI...* | おみせは おやすみ。 / 1993ねん なので! ピピ・・・ |

S10.8 is the garage (Could bundle); S10.9 a 1993 RULES file (Could).

#### S11 Per match: card, bar fill, defeat, YOU GET · Must

1. **The match card** (PNL): §5.2's record, typed by vanilla's `$3C:$81B1`, plus the VENUE field (R3.3's names).
2. **The bar fill** (POP, the champion speaks; Must). Knight's is his battle log's first window (S15). A rematch plays
   it again; the secret arena plays its own line (Should, below; the Rodeo Ring's and the Knightlord's are Must, S15).
3. **The defeat line** (POP, after the explosion, before YOU GET): **Should**.
4. **YOU GET** (PPU, vanilla `$60 + $51 + $06A5`): the weapon (a label), plus the plate where it comes with the kill.
   **Adaptors are never announced on YOU GET** (Roll does it: S12, S13, S29). `C.FLRSH` stays misspelled on the card in
   every language (`systems.md` §3.9).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S11.BLZ | M | scene | POP | Blizzard | FRESH POWDER, SOLAR PANELS. / LET'S GO, ROCKMAN! | しんせつと ソーラーパネル! / いくぜ ロックマン! |
| S11.WND | M | scene | POP | Wind | TALLY-HO! WIND MAN, CLEARED / FOR COMBAT! | タリホー! ウインドマン / せんとう かいし! |
| S11.PLT | M | scene | POP | Plant | PLEASE DON'T TRAMPLE / ANYTHING. INCLUDING ME. | なにも ふまないで くださいね。 / わたしも ふくめて。 |
| S11.FLM | M | scene | POP | Flame | EN GARDE! AND KEEP YOUR / DISTANCE... IF YOU CAN. | アン・ギャルド! まあいを / とれるものなら とってみよ。 |
| S11.YAM | M | scene | POP | Yamato | THIS ONE SHALL NOT MOVE. / COME TO ME. | せっしゃは うごかぬ。 / かかって まいれ。 |
| S11.TMH | M | scene | POP | Tomahawk | A FAIR DRAW! THE CROWD LOVES / A FAIR DRAW. NOW, ROUND TWO! | フェアな ドローだ! おきゃくも / おおよろこび! さあ つぎだ! |
| S11.CEN | M | scene | POP | Centaur | SHALL WE FIND OUT MY ABILITY / TOGETHER? | わたしの のうりょく、いっしょに / たしかめましょうか? |
| S11.BLZ.D | S | flavour | POP | Blizzard | BRR... I'LL GO THAW OUT. / GOOD MATCH, ROCKMAN! | さむっ・・・ とけて くるぜ。 / いい しあい だったな! |
| S11.WND.D | S | flavour | POP | Wind | MAYDAY... GOOD FLYING. NEXT / TIME I'M THE ACE. | メーデー・・・ いい フライトだ。 / つぎは おれが エースだ。 |
| S11.PLT.D | S | flavour | POP | Plant | OH... YOU WERE GENTLE WITH / THE FLOWERS. THANK YOU. | ああ・・・ おはなを だいじに / して くれましたね。ありがとう。 |
| S11.FLM.D | S | flavour | POP | Flame | TOUCHE! A SPLENDID DUEL. THE / PALACE SALUTES YOU! | まいった! みごとな けっとうだ。 / きゅうでんが きみを たたえる! |
| S11.YAM.D | S | flavour | POP | Yamato | THIS ONE... MOVED. A LITTLE. / WELL FOUGHT. | せっしゃ・・・ うごいて しもうた。 / みごとで ござる。 |
| S11.TMH.D | S | flavour | POP | Tomahawk | YOU'RE QUICK, ROCKMAN! TAKE / A BOW. YOU EARNED IT. | はやいな ロックマン! / おじぎを しな。おまえの かちだ。 |
| S11.KNT.D | S | flavour | POP | Knight | THOU HAST BESTED ME. A FINE / BOUT! HUZZAH! | なんじの かちだ。みごとな / しょうぶで あった! ばんざい! |
| S11.CEN.D | S | flavour | POP | Centaur | SO IT WAS LUCK ALL ALONG! / HOW EXCITING. I LOST. | けっきょく うん だったの ですな。 / たのしかった! まけましたが。 |
| S11.BLZ.X | S | flavour | POP | Blizzard | UP HERE THE SUN NEVER SETS! / ...IT'S BEHIND A CLOUD, BUT! | ここなら たいようが しずまない! / ・・・くもに かくれてるけどな! |
| S11.WND.X | S | flavour | POP | Wind | A FIGHT ABOVE THE CLOUDS! / NOW THIS IS FLYING! | くもの うえで しょうぶ! / これぞ フライトだ! |
| S11.PLT.X | S | flavour | POP | Plant | YOU FOUND THE LOST CITY! / THEN LET'S FIGHT FOR REAL. | ロストシティを みつけましたね! / では ほんきで いきます。 |
| S11.FLM.X | S | flavour | POP | Flame | THROUGH THE MIRROR, ARE WE? / THEN MEET MY SHADOW. | かがみを ぬけて きたか? / ならば わがはいの かげと たたかえ。 |
| S11.YAM.X | S | flavour | POP | Yamato | THE STAGE TURNS, BUT THIS / ONE DOES NOT. | ぶたいは まわれど / せっしゃは まわらぬ。 |
| S11.CEN.X | S | flavour | POP | Centaur | I'M A SEA-CENTAUR DOWN HERE. / A FIRST, EVEN FOR ME. | ここでは わたしは うみの / ケンタウロス。はじめて です。 |

S11.FLM's "keep your distance" is the tell for Flame Man's spacing duel (R3.1: he parries shots fired within 48 px).
S11.TMH plays after the HIGH NOON draw (venues_a §3.8.1). The `.X` lines need their arena twists (Should); in v1.0 the
secret arenas are the boss rooms re-paletted, and they replay the `.` line.

#### S12 POWER hand-off (EVENTS b0) · Must

On the bracket after the 2nd win; Roll's face icon. The vanilla docking cutscene then plays the first time the form is
used (`systems.md` §1.3, FORM_DEBUT).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S12.1 | M | scene | WIN | Ro | ROCK! RUSH'S POWER ADAPTOR / PASSED INSPECTION! | ロック! ラッシュの パワー / アダプター けんさ ごうかく! |
| S12.2 | M | scene | WIN | Ro | HOLD SELECT, PRESS LEFT OR / RIGHT TO DOCK. THE PUNCH / BREAKS CRACKED BLOCKS. THE / JUDGES COUNT IT AS A WEAPON! | セレクトを おしながら ひだりか / みぎで ドッキング。パンチは / ひびわれた ブロックを こわすし / ぶきの ひとつに かぞえられるわ! |

#### S13 JET hand-off (EVENTS b1) · Must

On the bracket after the 4th win, then S14 at once (`meta.md` §3.5: JET, then the Riot).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S13.1 | M | scene | WIN | Ro | JET ADAPTOR FITTED! NINETEEN / UNITS OF FUEL. IT REFILLS / WHEN YOU'RE NOT FLYING. | ジェットアダプター そうちゃく! / ねんりょうは 19。とんで いない / ときは かってに たまるわ。 |
| S13.2 | M | scene | WIN | Ro | SAME CONTROLS. ...ROCK? WHY / IS THE BRACKET SHAKING? | そうさは おなじよ。・・・あれ? / トーナメントひょうが ゆれてる? |

#### S14 The Riot intro (EVENTS b2) · Must (lines); the animation · Could

`meta.md` §3.5 stages it (the stamps, the cracked FINAL frame). S14.2-S14.3 are **Act I's Wily gag**.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S14.1 | M | scene | WIN | K | AN UNREGISTERED ENTRANT IS / ATTACKING THE BRACKET! | みとうろくの せんしゅが / トーナメントひょうを こうげきちゅう! |
| S14.2 | M | scene | WIN | C | REGISTERED, ACTUALLY. / ENTRANT β. SPONSOR: MR. Y. | ・・・とうろくずみ だ。エントリーβ。 / スポンサーは Mr.Y。 |
| S14.3 | M | scene | WIN | K | ...OF COURSE IT IS. | ・・・やっぱりね。 |
| S14.4 | M | scene | WIN | B | FOUR WINS? CUTE. EVERY OTHER / MATCH IS POSTPONED. NEXT, / YOU FIGHT ME, ORIGINAL. | 4しょう? かわいい もんだ。ほかの / しあいは ぜんぶ えんき。つぎは / オレと やれ、オリジナル。 |
| S14.5 | S | flavour | WIN | C | THE COMMITTEE HAS APPROVED / THIS. BY FAX. FROM MR. Y'S / OFFICE. | いいんかいは これを しょうにん / した。ファックスで。Mr.Yの / じむしょから。 |

#### S15 Venue NPCs, windows and signs · Must as listed

`story.md` owns these words now (R4.1); the venue docs place them and own their triggers. EN finalises the venue docs'
drafts; JP follows each venue's register rule. The hooks, deaths and hints of each venue are in §6.3 and §7.1.

| Venue | JP register, and the real quote it rests on |
|---|---|
| HERO'S QUEST | the 1986 RPG's archaic register (わし / なんじ / じゃ). **Its famous lines are paraphrased, never quoted** (R8.4, §1.2 rule 11): the King's death line keeps the scolding's 「おお ロックよ!」 rhythm in new words (§6.3), the RUN refusal is 「しかし にげみちを ふさがれた!」, the critical hit 「みごとな いちげきが きまった!」, and the Knightlord's offer and the Princess's loop are re-worded too. No title, spell or character name of that game appears (R3.3), so the spells are "a fire spell" and "a healing spell" |
| HIGH NOON FRONTIER | plain western 「〜だぜ」 for Sam and the robbers, polite for the Sheriff and the conductor. The pianist sign is the one Oscar Wilde reported from a Leadville saloon (A-8.9), trimmed to 2 lines |
| SKY ACE | military radio: 「りょうかい!」, 「メーデー!」. Its in-stage words are labels |
| LOST JUNGLE | the cat only says 「ニャー」; Kalinka's "IS THAT... TANGO?" (Capcom's own cat) drops round 1's "From the Game Boy?" (R3.3) |
| SUMMIT CLIMBER | seals 「キュー」; the union sign 「アザラシ ろうどうくみあい」 (art) |
| PERSIAN PALACE | the mouse 「チュー」 |
| ATLANTIS RUINS | zone plaques are numerals (art) |
| EDO NINJA ROW | the fortune slip's 大凶 is art (the text engine is kana-only). The sekisho guard's line is retired with the sekisho (R3.2) |

**HERO'S QUEST** (`venues_a.md` §2; text v1b, built at M6; about 33 strings, the most of any venue: the venue is its
verbs and windows).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| KNT.S01 | M | stage | WIN | Sage | PRESS UP TO TALK. TO SEARCH, / STAND STILL AND HOLD DOWN. | はなすときは うえ。しらべるときは / たちどまって したを おしつづけるのじゃ。 |
| KNT.S02 | M | stage | WIN | Sage | THE THRONE OF A LORD WHO / NEVER SITS HIDES SOMETHING. | すわらぬ あるじの ぎょくざには / なにかが かくされて おる。 |
| KNT.S03 | M | stage | WIN | King | O DESCENDANT OF LIGHT! THE / KNIGHTLORD AWAITS. TAKE THIS / KEY. | おお ライトの ちを ひく ものよ! / ナイトロードが まって おる。 / この かぎを さずけよう。 |
| KNT.S04 | M | stage | POP | — | THOU HAST FOUND A MAGIC KEY! | まほうの かぎを てに いれた! |
| KNT.S05 | M | stage | POP | — | THOU HAST NO KEY. | かぎを もって いない。 |
| KNT.S06 | M | stage | POP | — | THOU FINDEST NOTHING. THIS / IS NOT THAT THRONE. | なにも みつからなかった。 / この ぎょくざでは ないようだ。 |
| KNT.S07 | M | stage | POP | — | THE CEILING DRAWS NEAR! | てんじょうが せまって きた! |
| KNT.S08 | M | stage | POP | — | THE CEILING IS DEFEATED! / ROCK GAINED 8 EXP. | てんじょうを やっつけた! / けいけんち 8ポイント かくとく! |
| KNT.S09 | M | stage | WIN | — | A METSLIME DRAWS NEAR! / COMMAND? / ▶FIGHT RUN SPELL ITEM | メットスライムが あらわれた! / どうする? / ▶たたかう にげる じゅもん どうぐ |
| KNT.S10 | M | stage | WIN | — | KNIGHT GUARDS DRAW NEAR! / COMMAND? / ▶FIGHT RUN SPELL ITEM | ナイトガードたちが あらわれた! / どうする? / ▶たたかう にげる じゅもん どうぐ |
| KNT.S11 | M | stage | WIN | — | BUT THE WAY WAS BARRED! | しかし にげみちを ふさがれた! |
| KNT.S12 | M | stage | WIN | — | ROCK RAN AWAY. | ロックは にげだした。 |
| KNT.S13 | M | stage | WIN | — | THOU HAST DONE WELL. ROCK / GAINED 12 EXP. | みごとだ! ロックは けいけんち / 12ポイントを かくとく! |
| KNT.S14 | M | stage | POP | — | A METAL METSLIME APPEARS! | メタルメットスライムが あらわれた! |
| KNT.S15 | M | stage | POP | — | THE METAL METSLIME ESCAPED! | メタルメットスライムは にげだした! |
| KNT.S16 | M | stage | POP | — | A SPLENDID STRIKE! / ROCK GAINED 1000 EXP. | みごとな いちげきが きまった! / ロックは けいけんち 1000 かくとく! |
| KNT.S17 | M | stage | POP | — | THOU HAST BUT 1 KEY. TWO / DOORS LIE BELOW. | かぎは ひとつ しかない。 / したには とびらが ふたつ。 |
| KNT.S18 | M | stage | POP | — | THOU HAST NO KEY. TWO DOORS / LIE BELOW. | かぎが ない。 / したには とびらが ふたつ。 |
| KNT.S19 | M | stage | WIN | tablet | I, THOMAS LIGHT, HAVE LEFT / THIS FOR MY DESCENDANT. TELL / NO ONE. ESPECIALLY NOT WILY. | わたし トーマス・ライトは / しそんの ために これを のこす。 / だれにも いうな。 / とくに ワイリーには。 |
| KNT.L01 | M | stage | WIN | KN | KNIGHT MAN DRAWS NEAR! / COMMAND? / ▶FIGHT RUN | ナイトマンが あらわれた! / どうする? / ▶たたかう にげる |
| KNT.L02 | M | stage | POP | KN | KNIGHT MAN ATTACKS! | ナイトマンの こうげき! |
| KNT.L03 | M | stage | POP | KN | KNIGHT MAN IS GUARDING. | ナイトマンは みを まもっている。 |
| KNT.L04 | M | stage | POP | KN | KNIGHT MAN CASTS A FIRE / SPELL! | ナイトマンは ほのおの じゅもんを / となえた! |
| KNT.L05 | M | stage | POP | KN | KNIGHT MAN SWINGS THE / MORNING STAR! | ナイトマンは モーニングスターを / ふりまわした! |
| KNT.L06 | M | stage | POP | KN | KNIGHT MAN CASTS A HEALING / SPELL! | ナイトマンは かいふくの じゅもんを / となえた! |
| KNT.L07 | M | stage | POP | KN | THE SPELL FIZZLED! | じゅもんは かきけされた! |
| KNT.L08 | M | stage | POP | KN | THE SPEAR PIERCED THE / SHIELD! | やりが たてを つらぬいた! |
| KNT.L09 | M | stage | POP | KN | THE SHIELD BROKE! | たてが くだけた! |
| KNT.L10 | M | stage | POP | KN | KNIGHT MAN IS ENRAGED! | ナイトマンは いかりくるっている! |
| KNT.K01 | M | stage | WIN | Knightlord | STAND AT MY SIDE, AND HALF / THE BRACKET SHALL BE THINE. / ▶YES NO | わしの がわに つけば / トーナメントの はんぶんを / くれて やろう。 ▶はい いいえ |
| KNT.K02 | M | stage | WIN | Knightlord | SO BE IT. THY HALF IS / WAITING FOR THEE... | よかろう。なんじの ぶんは / ちゃんと とって あるぞ・・・ |
| KNT.K03 | M | stage | WIN | Knightlord | THY TOURNAMENT ENDS HERE. / SLEEP NOW, AND SLEEP LONG. | なんじの たいかいは ここまで。 / ながい ねむりに つくが よい。 |
| KNT.K04 | M | stage | WIN | Knightlord | REFUSED? THEN FOLLY IS / THINE, AND SO IS THIS FIGHT! | ことわるか! ならば その おろかさ / ここで おもいしらせて くれよう! |
| KNT.S20 | S | flavour | WIN | Innkeeper | WELCOME TO THE INN. ONE / NIGHT IS 20 BOLTS. ▶YES NO | やどやへ ようこそ。ひとばん / 20ボルト です。 ▶はい いいえ |
| KNT.S21 | S | flavour | WIN | Innkeeper | GOOD MORNING. THOU SEEMST TO / HAVE SLEPT WELL. | おはよう ございます。 / よく ねむれましたか? |
| KNT.S22 | S | flavour | WIN | Roll | DOST THOU LOVE ME, ROCK? / ▶YES NO | ロック、わたしを あいしてる? / ▶はい いいえ |
| KNT.S23 | S | flavour | WIN | Roll | NAY! THOU SHALT SAY YES! | いいえ なんて いわせない! |
| KNT.S24 | S | flavour | WIN | Roll | ...FINE. THE COSTUME IS HOT, / ROCK. | ・・・もういい。この いしょう / あついのよ ロック。 |
| KNT.S25 | S | flavour | LBL | sign | THY DEEDS ARE RECORDED. | |
| KNT.S26 | C | flavour | POP | — | ROCK'S LEVEL WENT UP! (ROBOT / MASTERS DO NOT LEVEL UP.) | ロックの レベルが あがった! / (ボスは レベルアップ しません。) |

The Inn, Princess Roll and the record sign are the venue's second set piece (Should, R0.3 item 4); EXP levels are Could.
The battle log uses
the pop-up window with the commentators muted (consistency decision 28). KNT.K01-K04 are the secret arena's offer:
YES costs a life (CX's "a YES that hurts").

**HIGH NOON FRONTIER** (`venues_a.md` §3; built at M6).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| TMH.S01 | M | stage | WIN | poster | WANTED: DOMINGO DOME. / CLAIM-JUMPING. 15 BOLTS. | おたずねもの: ドミンゴ・ドーム。 / さいくつけん どろぼう。15ボルト。 |
| TMH.S02 | M | stage | WIN | poster | WANTED: SIX-SHOT SAM. / CARD SHARP. 20 BOLTS. | おたずねもの: シックスショット・サム。 / いかさま カードし。20ボルト。 |
| TMH.S03 | M | stage | WIN | poster | WANTED: SIDEWINDER. / TRAIN ROBBERY. 25 BOLTS. | おたずねもの: サイドワインダー。 / れっしゃごうとう。25ボルト。 |
| TMH.S04 | M | stage | POP | sign | DON'T SHOOT THE PIANIST. / HE IS DOING HIS BEST. | ピアニストを うたないで! / いっしょうけんめい なんです。 |
| TMH.S05 | M | stage | POP | E | HEY! I'M ON YOUR TEAM! | ちょっと! みかた だってば! |
| TMH.S06 | M | stage | POP | Sam | COME BACK WHEN YOU'RE / FASTER. | もっと はやく なってから / でなおしな。 |
| TMH.S07 | M | stage | WIN | conductor | BOUNTIES: %N% OF 3. / SIDEWINDER RIDES THE 4:50. | しょうきんくび: %N%にん。 / サイドワインダーは 4じ50ぷんの きしゃ。 |
| TMH.S08 | M | stage | WIN | conductor | ALL THREE? THEN ENJOY THE / RIDE, DEPUTY. ALL ABOARD! | 3にん ぜんぶ? では ごゆっくり / ほあんかんどの。ごじょうしゃ! |
| TMH.S09 | M | stage | WIN | conductor | ALL ABOARD THE 4:50, OR / EXPRESS? ▶ALL ABOARD EXPRESS | 4じ50ぷんに のる? それとも / きゅうこう? ▶のる きゅうこう |
| TMH.S10 | M | stage | POP | conductor | JUNCTION! ALL OFF! | ジャンクション! おおりください! |
| TMH.S11 | M | stage | POP | — | SIDEWINDER GOT AWAY! | サイドワインダーに にげられた! |
| TMH.S12 | M | stage | WIN | Sheriff | BOUNTIES: %N% OF 3. THE BACK / WAY IS FOR DEPUTIES. | しょうきんくび %N%にん。うらみちは / ほあんかん せんよう です。 |
| TMH.S13 | M | stage | WIN | Sheriff | WELL I'LL BE. YOU'VE EARNED / THE BACK WAY, DEPUTY. | これは おどろいた。うらみちを / どうぞ、ほあんかんどの。 |
| TMH.S14 | M | stage | WIN | Sheriff | NOT ONE TOWNSFOLK HURT. / WEAR THIS, DEPUTY. | まちの ひとは だれも けがなし。 / これを どうぞ、ほあんかんどの。 |
| TMH.S15 | M | stage | POP | Tomahawk | A RODEO AT DUSK? NOW THAT'S / A SHOW! WAIT FOR THE FLAG. | ゆうぐれの ロデオか! こいつは / みものだぜ。はたを まて! |
| TMH.S16 | S | flavour | POP | Tomahawk | MR. Y PUT UP THAT POSTER. / I'M NOT COLLECTING. | あの てはいしょ? Mr.Yが はったんだ。 / おれは しらないぜ。 |
| TMH.S17 | M | stage | LBL | — | READY... · DRAW! · FOUL! · HEY! | |

TMH.S15 is the RODEO RING's opening line in v1.0 (the mesa at dusk, the flag judge on his stand; R3.4). TMH.S16 waits for
the ring's fence and its WANTED: ROCKMAN poster (Should, the arena twist). The draw's words (TMH.S17) are sprites.

**The other venues' words** (signs read with UP, pop-ups; the venue docs' requests).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| BLZ.S01 | M | stage | POP | sign | BONK THE ICE ABOVE YOU. THE / SEALS WILL FIX IT. | うえの こおりを ずつきで わろう。 / アザラシが なおします。 |
| BLZ.S02 | M | stage | POP | sign | SUMMIT BONUS: 40 SECONDS. / THE CONDOR WAITS FOR NO ONE. | ちょうじょう ボーナス 40びょう。 / コンドルは まって くれない。 |
| CEN.S01 | M | stage | POP | tablet | DOORS GO WHERE THEY SAY. / CRACKS LIE. PAINT IS PAINT. | とびらは ばんごうの ゾーンへ。 / ひびは うそ。えは ただの え。 |
| CEN.S02 | M | stage | POP | inscription | ZONE 0: BEFORE THE FIRST. / YOU WERE NOT SUPPOSED TO. | ゾーン0: さいしょの まえの ゾーン。 / みつかる はずでは なかった。 |
| YAM.S01 | M | stage | POP | sign | ALL GOLD ON LOAN FROM THE / TOURNAMENT. -THE SPONSOR | この こばんは たいかいからの / かしだし です。スポンサーより |
| PLT.S01 | M | stage | POP | — | A RHINESTONE RING. THE / JUDGES SAY IT'S WORTHLESS. | イミテーションの ゆびわ。 / しんさいんいわく かちは ゼロ。 |
| PLT.S02 | M | stage | LBL | — | TREASURE %N% OF 4 - LOGS %M% | |
| WND.S01 | M | stage | LBL | — | TAKE OFF! · COMMITTEE LOANER / JET · SHOOTING DOWN %N%% | |
| WND.S02 | M | stage | LBL | — | LANDED · ▶LAND CONTINUE · / ACES ONLY · RENTAL | |
| WND.S03 | S | flavour | LBL | — | NO PASSENGERS | |

BLZ.S02 is the condor's sign on 0F (the exit's tell, venues_b §1.6.1); CEN.S01 is the door rules' tablet at 06 (the
maze's one tell, venues_b §3.3), naming all three doors (honest, cracked, painted) on one page. Centaur lands at M5,
before text v1b (M6), so its tablet and ZONE 0's inscription use the v1a pop-up like every other sign (venues_b §0.6),
never the 4 × 28 window. PLT.S01 is the rhinestone's pop (the AUTO RECOVER tell). WND.S03 needs the partner.

#### S16 Game over, RETIRE and unplug · Must (game over)

The window under vanilla's `GAME OVER` (`meta.md` §3.7). The generic table rotates; in H1-H5 the line is Mr. Y's, in
W2-W3 Wily's. RETIRE's and the unplug's lines are Should (`meta.md` §1.7 makes the unplug line Should).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S16.1 | M | scene | WIN | K | HE'LL BE BACK. THEY ALWAYS / COME BACK. | きっと もどってくる。 / みんな もどって くるんだよ。 |
| S16.2 | M | scene | WIN | K | PAPA SAYS A GAME OVER IS A / VERY LONG PIT STOP. | パパが いってた。ゲームオーバーは / ながーい ピットストップ だって。 |
| S16.3 | M | scene | WIN | K | INSERT COIN! ...KIDDING. / PRESS START. | コインを いれてね! ・・・うそ。 / スタートで いいよ。 |
| S16.4 | M | scene | WIN | Y | GAME OVER! MR. Y THANKS YOU / FOR YOUR PARTICIPATION! | ゲームオーバー! Mr.Yより / ごさんか ありがとう ございました! |
| S16.5 | M | scene | WIN | W | HA! COME BACK WHEN YOU'RE / 16-BIT! | ワハハ! 16ビットに なってから / でなおして こい! |
| S16.6 | S | flavour | WIN | K | THE CROWD IS CHANTING YOUR / NAME. WELL, THE ONES WHO / STAYED. | かんきゃくが なまえを よんでるよ。 / のこってる ひとたちが。 |
| S16.7 | S | flavour | WIN | K | EVERY CHAMPION HAS LOST A / MATCH. MOSTLY TO YOU, LATER. | チャンピオンだって まけるよ。 / あとで あなたに まけるの。 |
| S16.8 | S | flavour | WIN | K | TACTICAL RETREAT! THE / JUDGES ALLOW IT. | さくせんてき てったい! / しんさいんも みとめてるよ。 |
| S16.9 | S | flavour | WIN | K | WE LOST THE FEED IN / %NAME%'S MATCH! / DID SOMEONE TRIP ON A CABLE? | %NAME%の しあいちゅうに / ちゅうけいが きれちゃった! / だれか ケーブルに つまずいた? |
| S16.10 | S | flavour | WIN | C | A POWER CUT MID-MATCH. THE / JUDGES RECORDED IT AS... / WEATHER. | しあいちゅうの ていでん。 / しんさいんは 「てんこう」と / きろく した。 |
| S16.11 | S | flavour | WIN | K | THE STADIUM WENT DARK. PAPA / THINKS IT WAS A SQUIRREL. | スタジアムが まっくら。 / パパは リスの しわざ だって。 |

S16.8 plays on a file's first RETIRE; S16.9-S16.11 on a load with IN_MATCH set.

---
### Act II: the HALFTIME RIOT

`fortress.md` §2 stages it: the GP Stadium at night, in a blackout, overrun by **the rejects** (R4.3: Mr. Y's hired
crowd is the losing contest entries, because they are mechanics: the audition rule and TALENT SCOUT). Round 1's Sniper
Joes in Bass scarves are withdrawn (consistency-7, consistency decision 12).

#### S17 Halftime night · Must

Riot 00, on READY (POP). S17.2 is **Act II's Wily gag** and the first-reject hook (RIO-01).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S17.1 | M | scene | POP | K | HALFTIME RIOT! THE STANDS / ARE FULL OF... ROBOTS? | ハーフタイム・ライオット! / きゃくせきに・・・ ロボット? |
| S17.2 | M | scene | POP | C | REJECTED CONTEST ENTRIES. / MR. Y HIRED THEM ALL. | コンテストの おちた ロボットだ。 / Mr.Yが やとった。 |
| S17.3 | S | flavour | POP | K | THEY'RE CHEERING FOR BASS! / ...FOR MONEY. | フォルテを おうえん してる! / ・・・おかねで。 |

#### S18 Break Man holds the crowd · Must

Riot 06, merged with fortress round 1's help beat (fortress §2.6): rubble seals the tunnel and the rejects pour out of
the stands. His whistle; the masked NPC drops in, breaks the rubble with one Break Shot, turns to the crowd with his
shield up, and stays. **Nobody names him** (R4.2): Kalinka still calls him entrant ten, and Rock says nothing (round 1's
"Break Man!" from Rock is withdrawn: the name is first spoken at 0E).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S18.1 | M | scene | POP | BM | GO. I'VE GOT THE CROWD. | いけ。きゃくせきは おれが / おさえる。 |
| S18.2 | M | scene | POP | K | IS ENTRANT TEN ALLOWED TO / DO THAT? | 10ばんって あんなこと / して いいの? |
| S18.3 | S | flavour | POP | C | NO RULE AGAINST IT. I / CHECKED. THERE IS RULE 8. | きんし する ルールは ない。 / しらべた。ルール8なら あるが。 |

#### S19 Bass β, duel 1, and the block · Must

Riot 0D (fortress §2.4). The bar-fill exchange plays in the window while the intro freezes the fight. RIO-06 is the
duel's teaching line (the first copy), RIO-07 is SC6's (systems), RIO-09 the overdrive. At 0 HP Bass charges the BASS
BLASTER; at f100 the whistle, and the NPC steps in front of it; then the block exchange, then Bass's exit.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S19.1 | M | scene | WIN | B | YOUR DATA'S IN ME, ORIGINAL. / EVERY SLIDE. EVERY CHARGE. / I KNOW WHAT YOU'LL DO. | おまえの データは オレの なかだ。 / スライディングも チャージも。 / うごきは おみとおしだ。 |
| S19.2 | M | scene | WIN | R | THEN YOU KNOW I WON'T QUIT. | なら ぼくが あきらめない ことも / わかるよね。 |
| S19.3 | M | scene | WIN | B | ...SHUT UP AND FIGHT! | ・・・うるさい! かかってこい! |
| RIO-06 | M | secret | POP | K | THAT'S YOUR WEAPON! HE / COPIED IT! | あれ ロックマンの ぶきだよ! / コピーしてる! |
| RIO-07 | M | secret | POP | C | HE'S ADAPTING! CHANGE / WEAPONS, ROCKMAN! | てきおう している! / ぶきを かえろ ロックマン! |
| RIO-08 | S | flavour | POP | K | NO DATA! HE HASN'T SEEN / YOUR WEAPONS YET! | ノーデータ! まだ ぶきを / みられて ないんだ! |
| RIO-09 | M | scene | POP | C | β OVERDRIVE?! THAT'S AGAINST / EVERY RULE IN THE BOOK! | βオーバードライブ!? / ルール いはん だぞ! |
| S19.4 | M | scene | POP | B | WHO ARE YOU SUPPOSED TO BE? | おまえは なにものだ? |
| S19.5 | M | scene | POP | BM | ENTRANT NUMBER TEN. | エントリー ナンバー10。 |
| S19.6 | M | scene | POP | B | THIS DOESN'T COUNT! THE BETA / BUILD HAS... BUGS! | こんなの ノーカンだ! / ベータばんには バグが・・・! |
| S19.7 | M | scene | POP | K | HE BLAMED THE BUGS! | バグの せいに した! |
| S19.8 | S | flavour | POP | C | IN FAIRNESS, THAT IS WHAT / BETAS ARE FOR. | まあ ベータばんとは / そういう ものだ。 |
| S19.9 | S | flavour | POP | K | NOT A SCRATCH! BASS IS GOING / TO BE SO MAD. | むきず! フォルテ ぜったい / おこってるよ! |

RIO-07 is RIO's adapt line and the source of Bass's first-weakness slot (§6.2). S19.9 is the RIVAL test's flavour
(RATEFLAGS b2, rating T13). The help capsule at HP < 6 (the SOLO RIOT test, T1) has no words: the whistle is enough.

#### S20 The reveal and Rule 9 · Must (the reveal, pages 1-2); Should (pages 3-6)

Riot 0E (fortress §2.6), **in place** (R4.2): Bass is gone; the masked robot stands at the roof's edge. **Rock's first
"Blues?"** (§1.3), and the first time "Break Man" is spoken. Then Rule 9's pages 1-2. In v1.0 he leaves over the roof's
edge (S20.6). With the partner (Should), pages 3-6 replace S20.6 and set FORMS.TAG and EVENTS b5; the bracket's EVENTS
b3 (the stamps peel off) plays on the next bracket visit either way, with S24.1.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S20.1 | M | scene | WIN | K | WHO IS THAT? | あれは だれ? |
| S20.2 | M | scene | WIN | R | ...BLUES? | ・・・ブルース? |
| S20.3 | M | scene | WIN | BM | BREAK MAN. | ブレイクマンだ。 |
| S20.4 | M | scene | WIN | K | RULE 9! THE SPONSOR'S ROBOTS / INVADED A MATCH! | ルール9 てきよう! スポンサーの / ロボットが しあいに らんにゅう! |
| S20.5 | M | scene | WIN | C | ROCKMAN MAY NAME A TAG / PARTNER. AND THE OTHER FOUR / MATCHES ARE BACK ON. | ロックマンは タッグパートナーを / よべる。のこりの 4しあいも / さいかい だ。 |
| S20.6 | M | scene | WIN | K | ...AND THE MASKED ONE IS / GONE AGAIN. | ・・・かめんの ひと、 / また いなくなっちゃった。 |
| S20.7 | S | scene | WIN | BM | ...I'LL GO WITH HIM. | ・・・おれが いく。 |
| S20.8 | S | scene | WIN | BM | PAUSE. CALL. CONFIRM WITH A. / DON'T WASTE ME. | ポーズして CALL。Aで けってい。 / むだに するな。 |
| S20.9 | S | scene | WIN | C | THAT IS THE MOST HE HAS EVER / SAID. | かれが こんなに しゃべったのは / はじめてだ。 |
| S20.10 | S | stage | LBL | banner | BREAK MAN JOINS! | |

S20.8 points at the pause menu's CALL row confirmed with A (R2.10), not at SELECT.

#### S21 Mr. Y's booth; Break Man walks · Could (the bundle: R2.5, R2.8)

`systems.md` §9.4 owns the offer and the cost; `meta.md` §3.8 the row. The second confirmation states the cost in
`systems.md`'s words, **"BREAK MAN WILL WALK."** (R2.8). It ships only with the partner.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S21.0 | C | stage | LBL | sign | MR. Y PERFORMANCE PARTNERS | |
| S21.1 | C | scene | WIN | Y | PSST. CHAMP. FEELING SLOW? / TRY Y-TURBO! ONE PART, ONE / CHIP. *RESULTS GUARANTEED.* / ▶NO YES | もしもし チャンピオン。おつかれ? / Y-ターボ いかが? パーツ ひとつで / チップ ひとつ。*こうか ほしょう*。 / ▶いいえ はい |
| S21.2 | C | scene | WIN | Y | THINK IT OVER! MR. Y WILL / ALWAYS BE RIGHT HERE. | ごけんとうを! わたくし Mr.Yは / いつでも ここに おります。 |
| S21.3 | C | scene | WIN | Y | SPLENDID! ONE TEENY DETAIL: / BREAK MAN WILL WALK. / STILL YES? ▶NO YES | すばらしい! ひとつだけ: / ブレイクマンは さって いきますよ。 / それでも はい? ▶いいえ はい |
| S21.4 | C | scene | WIN | Y | YOUR LOSS! PROBABLY / LITERALLY! | ざんねん! きっと / まけますぞ! |
| S21.5 | C | scene | WIN | Y | PLEASURE DOING BUSINESS! / RESULTS GUARANTEED! | まいど ありがとう ございます! / こうかは ほしょう いたします! |
| S21.6 | C | flavour | WIN | Y | Y-TURBO! NOW 20% MORE Y! | Y-ターボ! いまなら Yが 20% ぞうりょう! |
| S21.7 | C | flavour | WIN | Y | MY LAWYERS SAY IT IS LEGAL / IN AT LEAST ONE COUNTRY. | べんごしに よれば すくなくとも / ひとつの くにでは ごうほうです。 |
| S21.8 | C | flavour | WIN | Y | YOUR RIVAL USES IT! ...HE IS / IT, ACTUALLY. | ライバルも つかって おります! / ・・・というか かれ そのもの です。 |
| S21.9 | C | scene | WIN | BM | YOU TOOK Y'S MONEY. FIGHT / YOUR OWN MATCHES. | Mr.Yの かねを うけとったな。 / じぶんの しあいは じぶんで やれ。 |
| S21.10 | C | scene | WIN | K | ...PAPA? WHERE'S HE GOING? | ・・・パパ? どこ いくの? |
| S21.11 | C | scene | WIN | C | HOME, I THINK. | かえるの だろう。 |
| S21.12 | C | flavour | POP | C | IS THAT... A SPONSOR PATCH? | あれは・・・ スポンサーの ワッペンか? |
| S21.13 | C | flavour | POP | K | PAPA, DON'T LOOK. | パパ、みちゃ だめ。 |
| S21.14 | C | stage | LBL | pause | N0 | |

S21.4's JP slips into Wily's ぞ. After BREAK MAN WALKS (EVENTS2 b5) the pause menu shows his row greyed as **N0**: the
pause font has no O, so it is spelled with a zero, like vanilla's `N0R` and `P0W` (`rm6/text.md` §5.3).

### Act III: round two

#### S22 Exhibition badges light · Could (R3.7)

Cossack announces each guest when its badge lights (`meta.md` §3.1's pairs). The years are the original games'; no game
is named (R3.3). E4 is Won't.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S22.1 | C | scene | WIN | C | EXHIBITION UNLOCKED! FROM / 1984, THE ROBOT WHO FILLS / EVERY GAP... BLOCK MAN! | エキシビション かいほう! / 1984ねんから すきまを うめる / おとこ・・・ ブロックマン! |
| S22.2 | C | flavour | WIN | K | BLOCK MAN? ISN'T THAT NAME / TAKEN? | ブロックマン? その なまえ / つかわれて なかった? |
| S22.3 | C | flavour | WIN | C | NOT UNTIL 2018. | 2018ねん までは まだだ。 |
| S22.4 | C | scene | WIN | C | FROM 1976 AND 1986, THE / WALL'S BEST FRIEND... / PADDLE MAN! | 1976ねんと 1986ねんから / かべの しんゆう・・・ / パドルマン! |
| S22.5 | C | flavour | WIN | K | HE'S RETURNED THE SAME BALL / FOR DECADES! | なんじゅうねんも おなじ ボールを / うちかえしてるんだって! |
| S22.6 | C | scene | WIN | C | FROM 1978, COMING DOWN ONE / STEP AT A TIME... / INVADER MAN! | 1978ねんから 1だんずつ / おりてくる・・・ / インベーダーマン! |
| S22.7 | C | flavour | WIN | K | PAPA, WHAT'S THE NAGOYA / ATTACK? | パパ、なごやうち って なに? |
| S22.8 | C | flavour | WIN | C | SOMETHING YOUR GRANDFATHER / WAS VERY PROUD OF. | おじいちゃんの じまんの / わざ だよ。 |
| S22.9 | W | scene | WIN | C | FROM 1980, THE HUNGRIEST / ENTRANT IN HISTORY... MAZE MAN! | (round 1's draft) |

#### S23 Exhibition matches · Could (R3.7); E4 Won't

`fortress.md` §3 stages each as one lobby and one rule-boss arena. Each guest gets a card (§5.3), a bar fill, a defeat
line and a plaque on the first clear (the Museum is Won't, so the plaque shows on the results screen). **The plaques
describe and never name the games** (R3.3), so the commentators' "can't say the trademark" gag stays coherent.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S23.1 | C | scene | POP | K | ...A SINGLE LINE CLEARED. I / THINK THAT WAS HELLO. | ・・・1れつ きえた。いまの / あいさつ かな? |
| S23.2 | C | scene | POP | C | A PERFECT FIT. HE SEEMS AT / PEACE. | ぴったり おさまった。 / まんぞく そうだ。 |
| S23.3 | C | flavour | POP | K | A TET- ...A FOUR-ROW CLEAR! / I'M NOT ALLOWED TO SAY IT. | テト・・・ じゃなくて 4れつけし! / いっちゃ いけないんだった。 |
| S23.4 | C | scene | POP | Paddle | SAME BALL. EVERY DAY. SAME / BALL. | おなじ ボール。まいにち。 / おなじ ボール。 |
| S23.5 | C | scene | POP | Paddle | A DIFFERENT BALL. FINALLY. | ・・・ちがう ボールだ。やっと。 |
| S23.6 | C | scene | POP | Invader | WE. ARE. COMING. DOWN. | ワレワレハ。オリテ。イク。 |
| S23.7 | C | scene | POP | Invader | WE. HAVE. COME. DOWN. | ワレワレハ。オリテ。キタ。 |
| S23.8 | C | plaque | PLQ | — | AFTER A FALLING-BLOCK PUZZLE / BORN IN MOSCOW IN 1984. FIVE / YEARS LATER IT CAME PACKED / WITH A HANDHELD IN AMERICA. | 1984ねん モスクワで うまれた / おちものパズルに ささぐ。 / 5ねんご アメリカで けいたいきに / どうこん された。 |
| S23.9 | C | plaque | PLQ | — | AFTER THE 1976 ARCADE GAME / WHERE A PADDLE BROKE A WALL, / AND ITS 1986 HEIR, WHERE THE / PADDLE WAS A SPACESHIP. | 1976ねんの パドルで かべを くずす / ゲームと、1986ねんの あとつぎに / ささぐ。そこでは パドルが / うちゅうせん だった。 |
| S23.10 | C | plaque | PLQ | — | AFTER THE 1978 ARCADE GAME / OF INVADERS FROM SPACE. THEY / SPED UP AS YOU SHOT THEM, AS / THE MACHINE HAD FEWER TO / DRAW. | 1978ねんの うちゅうから せめてくる / ゲームに ささぐ。てきは へるほど / はやく なった。えがく かずが / へって きかいが らくに なったから。 |
| S23.11 | C | plaque | PLQ | — | IN 1976 THE CONTROLLER WAS A / KNOB. IN 1993 WE HAD A / D-PAD. PROGRESS. | 1976ねん コントローラーは つまみ / だった。1993ねんには じゅうじキー。 / しんぽ である。 |
| S23.12 | C | plaque | PLQ | — | THEY SAY THIS GAME CAUSED A / COIN SHORTAGE. THE BUSTER IS / FREE. | この ゲームで こうかが / たりなく なった という。 / バスターは ただ です。 |

S23.11 is E2's backroom plaque and S23.12 E3's (`fortress.md` §3.2-§3.3; R3.9 words the coin shortage as folklore).
Round 1's E4 lines and plaque (Maze Man) are kept in the scratch copy as Won't.

#### S24 The countdown · Must

Kalinka on the centre node once the Riot is won (`meta.md` §3.4). S24.1 also plays with EVENTS b3 (the stamps peel
off).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S24.1 | M | scene | WIN | K | %N% TO GO! THEN THE FINAL! | あと %N%つ! そしたら けっしょう! |
| S24.2 | M | scene | WIN | K | ALL EIGHT! THE CEREMONY IS / AT THE CENTRE! | 8しょう! ひょうしょうしきは / まんなかで! |
| S24.3 | S | flavour | WIN | K | THREE TO GO! THEY'RE / POLISHING THE TROPHY. | あと 3つ! トロフィーを / みがいてる ところ。 |
| S24.4 | S | flavour | WIN | K | TWO MORE! PAPA'S PRACTISING / HIS SPEECH. | あと 2つ! パパが スピーチの / れんしゅう ちゅう。 |
| S24.5 | S | flavour | WIN | K | ONE MORE! I CAN SEE THE / TROPHY FROM HERE! | あと 1しあい! ここから / トロフィーが みえるよ! |

#### S25 Trophy ceremony and theft (EVENTS b4) · Must

START on the lit trophy (`meta.md` §3.4); fortress §4.0 stages it: a UFO-catcher crane (the Cossack Catcher's claw, a
first look at H4) lowers from a saucer with a Y painted over its W and takes the GP Cup. S25.6 is **Act III's Wily
gag**, quietly.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S25.1 | M | scene | WIN | C | AFTER EIGHT MATCHES, THE / WINNER OF THE GRAND PRIX / ROUNDS: ROCKMAN! | 8しあいを かちぬいた / グランプリ よせんの しょうしゃは・・・ / ロックマン! |
| S25.2 | M | scene | WIN | C | THE CUP GOES ON DISPLAY / UNTIL THE FINAL. HOLD IT UP / FOR THE CAMERAS, LAD... | けっしょうまで カップは / てんじ される。カメラに むけて / かかげて くれ・・・ |
| S25.3 | M | scene | WIN | C | THAT IS MY CLAW! | わたしの アームだ! |
| S25.4 | M | scene | WIN | Y | CORRECTION, DOCTOR: MY CLAW. / I BOUGHT IT IN THE MUSEUM / GIFT SHOP! | ていせい いたします、はかせ。 / わたくしの アームで ございます。 / はくぶつかんの おみやげやで / かいました! |
| S25.5 | M | scene | WIN | Y | THE FINAL WILL BE AT MY / VENUE: THE HALL OF FAME! / COME AND GET IT, ROCKMAN! / WAHAHA- I MEAN, HO HO HO! | けっしょうは わたくしの / かいじょう ホール・オブ・フェイムにて! / とりに いらっしゃい! ワーッハッハ・・・ / いえ、ホッホッホ! |
| S25.6 | M | scene | WIN | L | ...THAT WAS WILY, ROCK. GO / AND GET THAT CUP BACK. | ・・・ワイリーじゃな、ロック。 / カップを とりもどして こい。 |
| S25.7 | S | flavour | WIN | K | THE GP CUP! PAPA, IT'S SO / SHINY! | GPカップだ! パパ、 / ぴかぴか! |
| S25.8 | S | flavour | WIN | K | THAT SAUCER HAS A Y PAINTED / OVER A W. | あの ユーフォー、Wの うえに / Yって ぬってある。 |

### Act IV: the Hall of Fame

#### S26 The Hall of Fame map · Must

First visit to the map (`meta.md` §3.9): Mr. Y on the museum's video wall. In v1.0 the 1988 and 1991 doors read
`CLOSED FOR RENOVATION` and the tour is H1 → H3 → H5 (fortress §4.0).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S26.1 | M | scene | WIN | Y | WELCOME TO THE HALL OF FAME! / EVERY EXHIBIT HAS BEEN... / *UPGRADED*. BY ME. A STRANGER. | ホール・オブ・フェイムへ ようこそ! / てんじひんは すべて・・・ / *アップグレード*ずみ。とおりすがりの / わたくしが。 |
| S26.2 | S | flavour | WIN | K | HE KEEPS SAYING STRANGER. | 「とおりすがり」って いいはってる。 |
| S26.3 | S | flavour | WIN | C | THREE WINGS OPEN, TWO CLOSED / FOR RENOVATION. THE CUP IS / AT THE END. | ウイングは 3つ あいてて 2つは / かいそうちゅう。カップは / そのさき だ。 |
| S26.4 | M | stage | LBL | door | CLOSED FOR RENOVATION | |
| S26.5 | M | stage | LBL | door | 1993 - UNDER CONSTRUCTION | |

#### S27 Museum plaques · Must (H1, H3, H5 as listed); Should (H2, H4 and the rest)

A plaque is an F-PLAQUE full-screen page (9 × 28, text v1b; fortress §0.7), opened with UP while B is not held (R2.10).
The text is **true** (Appendix A), **describes rather than names** anything not Capcom's own (R3.3), and **says BLUES**
for Rockman 3-5's mysterious robot (R3.9). One joke per plaque, always last. Kind `plaque` is a museum page; kind
`stage` marks the two plaques that are a boss's tell (H1 0E for the Yellow Devil's shelf, H3 10 for Gamma's fists).

**H1 ROCKMAN (1987)** (fortress §4.1)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PLQ.H1 | M | plaque | PLQ | — | ROCKMAN. 17 DECEMBER 1987, / FOR THE 8-BIT CONSOLE. / DR. WILY TOOK OVER SIX OF / DR. LIGHT'S ROBOTS. LIGHT'S / HELPER ROCK VOLUNTEERED TO / STOP THEM. BEAT A MASTER, / TAKE HIS WEAPON: EVERY / ROCKMAN SINCE KEPT THE RULE. / THE SCORE DID NOTHING. | ロックマン。1987ねん12がつ17にち / 8ビットの ゲームきで はつばい。 / ワイリーは ライトはかせの / ロボット 6たいを のっとった。 / じょしゅの ロックは じぶんから / たたかうと いった。ボスを たおし / ぶきを てに いれる。いまに つづく / ルールの はじまりだ。 / スコアは なんの やくにも たたない。 |
| PLQ.H1.03 | M | plaque | PLQ | — | MAGNET BEAM (1987). IT WAS / HIDDEN IN ELEC MAN'S STAGE, / BEHIND BLOCKS ONLY THE SUPER / ARM COULD LIFT. PLAYERS WHO / MISSED IT COULD NOT FINISH / THE GAME, SO THE MUSEUM PUT / IT ON THE MAIN PATH. TWO / BEAMS AT A TIME: WE ONLY HAD / TWO IN STOCK. | マグネットビーム (1987)。 / エレキマンステージの スーパーアーム / で しか どかせない ブロックの / おくに あった。とりのがすと / さいごまで すすめなかったので / はくぶつかんは みちの とちゅうに / おいた。どうじに 2ほんまで。 / ざいこが 2ほん しか ないので。 |
| PLQ.H1.0E | M | stage | PLQ | — | THE YELLOW DEVIL (1987) FLEW / ACROSS ITS ROOM IN PIECES / AND REBUILT ITSELF ON THE / OTHER SIDE. AN ELEC BEAM TO / THE EYE WAS THE CURE. / VISITORS NOTE: ITS PIECES / NEVER FLY HIGHER THAN A / MAGNET BEAM BUILT AT THE TOP / OF A JUMP. | イエローデビル (1987)は / バラバラに なって へやを / とびこえ むこうで がったいした。 / めに サンダービームが きりふだ。 / ごらいじょうの みなさまへ: / パーツは ジャンプの てっぺんで / つくった マグネットビームより / たかくは とびません。 |
| PLQ.H1.13 | S | plaque | PLQ | — | SOME EXHIBITS ARE KEPT IN / STORAGE FOR EVERYONE'S / SAFETY. | いくつかの てんじひんは / みなさまの あんぜんの ため / そうこに しまって あります。 |
| H1.LBL1 | M | stage | LBL | case | MAGNET BEAM (1987). / HANDLE WITH CARE. | |
| H1.LBL2 | M | stage | LBL | sign | NO RUSH JET: AUTHENTIC / 1987 EXPERIENCE · BUILD A / BEAM. WALK IT. JUMP. | |
| H1.LBL3 | M | stage | LBL | crate | ROCKMAN (1987): OVERSEAS / PACKAGING. DO NOT DISPLAY. | |

The Devil's JP plaque calls the Elec Beam by its Japanese name, サンダービーム (A-1.4). H1.LBL2's second line is the gap's instruction (fortress §4.1, 0B: one 64-px beam, then
jump the last 32 px).

**H3 ROCKMAN 3 (1990)** (fortress §4.3)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PLQ.H3 | M | plaque | PLQ | — | ROCKMAN 3: DR. WILY NO / SAIGO!? 28 SEPTEMBER 1990. / NOTE THE QUESTION MARK. / IT BROUGHT THE SLIDE, RUSH, / AND BLUES, A STRANGER WITH A / WHISTLE. / DR. LIGHT AND DR. WILY BUILT / GAMMA TOGETHER, FOR PEACE. / DR. WILY HAD OTHER PLANS. | ロックマン3 Dr.ワイリーの さいご!? / 1990ねん9がつ28にち はつばい。 / 「!?」に ちゅうもく。 / スライディング、ラッシュ、 / そして くちぶえの ブルースが / はじめて とうじょう。 / ライトはかせと ワイリーは へいわの / ために ガンマを つくった。 / ワイリーには べつの もくろみが。 |
| PLQ.H3.02 | M | plaque | PLQ | — | BLUES (1990). HE ARRIVED / WITH A WHISTLE AND LEFT / WITHOUT A WORD. | ブルース (1990)。くちぶえと ともに / あらわれ ひとことも いわずに / さっていった。 |
| PLQ.H3.10 | M | stage | PLQ | — | GAMMA (1990). BUILT BY DR. / LIGHT AND DR. WILY TO KEEP / THE PEACE. ITS LAST FORM / FELL TO THE TOP SPIN. / THIS ONE RESPECTS ONLY A / FIST. VISITORS MAY PRACTISE / ON THE FIST BELOW. PLEASE / HIT THE BAG, NOT THE STAFF. | ガンマ (1990)。へいわの ために / ライトはかせと ワイリーが / つくった。さいごの すがたは / トップスピンで たおれた。 / この ガンマは こぶし しか / みとめない。したの こぶしで / れんしゅう できます。なぐるのは / サンドバッグだけに して ください。 |
| PLQ.H3.0B | S | plaque | PLQ | — | GEMINI MAN'S LASER (1990) / BOUNCED OFF EVERY WALL. SO / DOES THIS ONE. MIND THE / MIRRORS. | ジェミニマンの レーザー (1990)は / かべで はねかえった。これも / そう。かがみに ちゅうい。 |
| H3.LBL1 | M | stage | LBL | sign | RUSH COIL. PLEASE DO NOT / JUMP ON THE EXHIBIT. | |
| H3.LBL2 | M | stage | LBL | sign | STAFF ONLY | |
| H3.LBL3 | M | stage | LBL | capsule | RUSH SUPER ADAPTOR. / PROTOTYPE. ON LOAN FROM THE / FUTURE (1995). | |
| H3.LBL4 | M | stage | LBL | shelf | METAL · QUICK · AIR · CRASH · / FLASH · BUBBLE · WOOD · HEAT · / MK-VI: BACK SOON | |
| H3.LBL5 | M | stage | LBL | pop | FISTS ONLY · UPPERCUT! | |

H3.LBL4 labels the Doc Robot skulls in the workshop (b1): Rockman 3's Doc Robot fought with Rockman 2's eight bosses
(A-3.4); MK-VI returns in v1.1, copying AIR MAN (Should).

**H5 ROCKMAN 5 (1992)** (fortress §4.5)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PLQ.H5 | M | plaque | PLQ | — | ROCKMAN 5: BLUES NO WANA!? / 1992. A ROBOT WHO LOOKED / LIKE BLUES KIDNAPPED DR. / LIGHT. IT WAS DARK MAN, / BUILT BY DR. WILY. WHEN THE / REAL BLUES CAME, THE / DISGUISE FELL. MEANWHILE DR. / COSSACK BUILT ROCK A BIRD: / BEAT. | ロックマン5 ブルースの わな!? / 1992ねん。ブルースに にた / ロボットが ライトはかせを / さらった。しょうたいは ワイリーの / ダークマン。ほんものの ブルースが / あらわれ へんそうは はがれた。 / そのころ コサックはかせは / ロックに とりを つくった。 / ビートである。 |
| PLQ.H5.19 | M | plaque | PLQ | — | WING 6: ROCKMAN 6 (1993). / EXHIBIT IN PROGRESS. THE / DIORAMA SHOWS MR. X'S / FORTRESS, AS IT WAS. / PLEASE COME BACK AFTER THE / GRAND PRIX. | ウイング6: ロックマン6 (1993)。 / じゅんびちゅう。ジオラマは / Mr.Xの ようさい そのまま。 / グランプリの あとで また / おこし ください。 |
| PLQ.H5.12 | S | plaque | PLQ | — | SUPER ARROW (1992). A WEAPON / YOU COULD STAND ON. YOU / STILL CAN. | スーパーアロー (1992)。 / のれる ぶき だった。 / いまも のれる。 |
| H5.LBL1 | M | stage | LBL | door | ROCKMAN 6 (1993): WING / UNDER CONSTRUCTION. KNOCK. | |

PLQ.H5.19 is the hidden room's plaque (b1: the 1993 wing, where Mr. X's card lies) and the setup for S43, when the wing
opens. The eight letter plates (b0) need no plaque: the letters are the game's own, and they spell **`ROCKMAN5`**, the
Japanese release's word, in both languages (R8.5; A-5.3).

**H2 ROCKMAN 2 and H4 ROCKMAN 4** (Should, with H2 and H4; R0.3 item 5) and the two thanks plaques

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PLQ.H2 | S | plaque | PLQ | — | ROCKMAN 2: DR. WILY NO NAZO. / 24 DECEMBER 1988. CAPCOM'S / ROBOT-DESIGN CONTESTS FOR / FANS BEGAN WITH IT. IT MADE / EIGHT BOSSES THE RULE, AND / BROUGHT THE E-TANK AND / PASSWORDS. / THE MECHA DRAGON CHASED ROCK / ACROSS THE SKY. HUM ALONG. | ロックマン2 Dr.ワイリーの なぞ。 / 1988ねん12がつ24にち はつばい。 / ファンから ボスを ぼしゅうする / でんとうは ここから。ボスは / 8たいが きほんに なった。 / Eかんと パスワードも ここから。 / メカドラゴンが そらを / おいかけて きた。 / あの きょく、くちずさめる でしょう? |
| PLQ.H2.T | S | plaque | PLQ | — | WITH THANKS TO ROCKMAN CX, / BY HIMAJIN JICHIKU, WHICH / PLAYED THIS GAME FROM THE / OTHER SIDE AND TAUGHT US / THAT A DEATH CAN BE A LINE / OF DIALOGUE. / ALSO: AIR MAN IS STILL HARD / TO SEE. | ロックマンCX (HIMAJIN JICHIKU / さく)に かんしゃを こめて。 / この ゲームを うらがわから / あそび、しぬことも セリフに / なると おしえて くれた。 / あと エアーマンは あいかわらず / みえにくい。 |
| PLQ.H4 | S | plaque | PLQ | — | ROCKMAN 4: ARATANARU YABO!! / 6 DECEMBER 1991. IT BROUGHT / THE CHARGE SHOT, EDDIE, DR. / COSSACK AND KALINKA. / WILY HELD KALINKA HOSTAGE, / SO DR. COSSACK BUILT EIGHT / ROBOTS FOR HIM. BLUES / BROUGHT HER HOME. DR. / COSSACK HAS APOLOGISED. | ロックマン4 あらたなる やぼう!! / 1991ねん12がつ6にち はつばい。 / チャージショット、エディ、 / コサックはかせと カリンカが とうじょう。 / ワイリーに カリンカを ひとじちに / され コサックは ロボットを つくった。 / カリンカを つれかえったのは / ブルース。コサックはかせは / もう あやまった そうです。 |
| PLQ.H4.T | S | plaque | PLQ | — | WITH THANKS TO ROCKMAN 4 / MINUS INFINITY, BY PURESABE / (2008-2016), WHICH REBUILT / THIS GAME, HID A FRIEND IN A / WALL, AND TAUGHT US TO READ / A WEAKNESS IN THE FLASHING. | ロックマン4 ミナスインフィニティ / (PURESABE さく 2008-2016)に / かんしゃを こめて。この ゲームを / つくりなおし、かべの なかに / なかまを かくし、てんめつで / じゃくてんを よむことを / おしえて くれた。 |

The H4 plaque says BLUES (R3.9; round 1 said Break Man there and Blues in H5). The thanks plaques name two fan works in
Latin letters until their authors' kana are confirmed (Open question 4).

#### S28 Exhibit lines; Mr. X's card · Must as listed

Each wing boss's bar fill and one tell (POP); the first-weakness lines are §6.2's. H1-01 plays with the M.BEAM case's
weapon-get screen (fortress §4.1, 03).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H1-01 | M | secret | POP | C | THE MAGNET BEAM, ON LOAN! / BUILD A BRIDGE WITH IT, LAD. | マグネットビーム! せんしゅに / かしだし ちゅうだ。はしを かけろ。 |
| S28.1 | M | scene | POP | K | HE COMES APART AND FLIES / ACROSS THE ROOM! | バラバラに なって / とんで くるよ! |
| H1-06 | M | secret | POP | K | YOU KNOCKED A PIECE DOWN! / NOW IT CAN'T REBUILD! | パーツを うちおとした! / これで もとに もどれないよ! |
| S28.2 | S | flavour | POP | C | WATCH THE EYE. ONLY THE EYE. | めを ねらえ。めだけを。 |
| S28.3 | S | flavour | POP | C | IT WON'T BE REASSEMBLING / THIS TIME. | こんどは がったい できまい。 |
| S28.4 | S | flavour | POP | Y | THAT WAS A MUSEUM PIECE! | てんじひん なのに! |
| H3-03 | S | flavour | POP | K | A TURTLE MACHINE? WHERE'S / DOC ROBOT? | カメの マシン? / ドクロボットは? |
| H3-03b | S | flavour | POP | C | HIS EXHIBIT IS BEING / REFURBISHED. | かれの てんじは / ただいま しゅうりちゅう だ。 |
| H3-04 | M | secret | POP | C | SLIDE, LAD! THE STRIPED / PRESSES LEAVE A GAP! | スライディングだ! しまもようの / プレスには すきまが ある! |
| H3-05 | M | secret | POP | K | ONLY A FIST WORKS ON THAT / BAG. AND ON GAMMA! | あの サンドバッグには / パンチしか きかない。ガンマもね! |
| S28.5 | M | scene | POP | L | WE BUILT GAMMA FOR PEACE, / WILY AND I. DON'T HOLD BACK. | ガンマは へいわの ために わしらが / つくった。えんりょは いらんぞ。 |
| S28.6 | M | scene | POP | C | MR. Y IS AT THE CONTROLS! / RIDE THE FIST AND PUNCH! | コクピットに Mr.Y! / こぶしに のって パンチだ! |
| S28.7 | M | scene | POP | Y | MY BEAUTIFUL EXHIBIT! THIS / IS NOT OVER! HO HO HO! | わたくしの てんじひんが! / まだ おわりませんぞ! ホッホッホ! |
| S28.8 | S | flavour | POP | K | GAMMA'S DOWN! AGAIN! | ガンマ ダウン! また! |
| H5-04 | M | secret | POP | door | WHO'S THERE? ...KNOCK / PROPERLY! SIX TIMES, FAST! | どなた? ・・・ちゃんと ノックして! / 6かい すばやく! |
| S28.9 | M | secret | WIN | card | A BUSINESS CARD: MR. X. / INTERNATIONAL ROBOT / FINANCIER. THE ADDRESS AND / PHONE NUMBER LOOK REAL. | めいしだ。「Mr.X / こくさい ロボット とうしか」。 / じゅうしょも でんわばんごうも / ほんもの らしい。 |
| S28.10 | S | flavour | WIN | K | PAPA... IS THERE A REAL / MR. X? | パパ・・・ ほんものの Mr.Xって / いるの? |
| S28.11 | S | flavour | WIN | C | ...LET'S NOT THINK ABOUT IT. | ・・・かんがえないで おこう。 |
| S28.12 | S | flavour | POP | K | I CAN HEAR THE MUSIC IN MY / HEAD! | あたまの なかで あの きょくが / ながれてる! |
| S28.13 | S | flavour | POP | C | DON'T LOOK DOWN, LAD. THERE / IS NO DOWN. | したを みるな。 / したは ない。 |
| S28.14 | S | flavour | POP | K | IT'S FALLING! LIKE IN 1988! | おちていく! 1988ねんと おなじ! |
| S28.15 | S | flavour | POP | C | THAT IS... MY MACHINE. ON / LOAN. I SIGNED THE FORM. | あれは・・・ わたしの マシンだ。 / かしだし ちゅう。サインした。 |
| S28.16 | S | flavour | POP | K | PAPA! COMMENTATE! | パパ! じっきょう して! |
| S28.17 | S | flavour | POP | C | ROCKMAN AVOIDS THE CLAW. / GOOD. I AM SO SORRY. | ロックマン アームを かわした。 / よし。ほんとうに すまない。 |
| S28.18 | S | flavour | POP | C | I FEEL MUCH BETTER NOW. / THANK YOU, ROCKMAN. | すっきり した。 / ありがとう ロックマン。 |

S28.5 is Light's radio line as Gamma's bar fills; S28.6 is phase 2 (SC5's tell, fortress H3-08); S28.7 plays as the
uppercut sends Mr. Y off in his pod (the uppercut pop is a label, H3.LBL5). S28.9 is the card's text (consistency
decision 10: story's words; fortress round 1's "NO RELATION" card is withdrawn); taking it sets RATEFLAGS b1 (rating
T14). S28.12-S28.18 are the Mecha Dragon's (H2) and the Cossack Catcher's (H4), Should with their wings.

#### S29 The Super Adaptor (EVENTS2 b4) · Must

On the Hall of Fame map after H3 (`meta.md` §3.6). FORMS.SUPER was set in-stage when Rush docked at H3 12, with **no
YOU GET card** (S11's rule, consistency-28); Roll explains it here.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S29.1 | M | scene | WIN | Ro | ROCK! THE MUSEUM'S PROTOTYPE / FITS RUSH PERFECTLY! SUPER / ADAPTOR, FITTED! | ロック! はくぶつかんの しさくひん、 / ラッシュに ぴったり! / スーパーアダプター そうちゃく! |
| S29.2 | M | scene | WIN | Ro | A ROCKET FIST THAT RETURNS, / A LITTLE JET HOP, NO FUEL. / SELECT AND LEFT OR RIGHT, AS / ALWAYS. | もどってくる ロケットパンチと / ちいさな ジェットジャンプ。ねんりょう / いらず。そうさは いつもどおりよ。 |
| S29.3 | S | flavour | WIN | Ro | THE DOCTOR SAYS TO BRING IT / BACK BY 1995. | はかせが 1995ねんまでに / かえしなさい って。 |

#### S30 H5: the fake Break Man · Must (the WRONG NOTE staging); Should (TWO BREAK MEN)

H5 15 (fortress §4.5.2). The boss card lies (`BREAKMAN` / `DEFINITELY BREAKMAN`, §5.4) and later re-types itself. **The
tell is the scarf's colour, orange** (fortress §4.5.2, consistency-8: round 1's "wrong side" is withdrawn), and the
whistle's one wrong note. **v1.0 plays round 1's "walked" staging** because the partner is Should: a full charge on the
red note brings the real whistle from off screen, in tune, and the disguise falls (b2, WRONG NOTE); otherwise the mask
slips at HP 14. **Nobody says Blues** here.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S30.1 | M | scene | POP | DM | IT'S ME. BREAK MAN. YOUR... / BROTHER? HAND IT OVER. | おれだ。ブレイクマンだ。 / おまえの・・・ あに? よこせ。 |
| S30.2 | M | secret | POP | K | HIS WHISTLE IS FLAT. AND HIS / SCARF IS ORANGE! | くちぶえ おんち だよ。それに / マフラーが オレンジいろ! |
| S30.3 | M | secret | POP | K | THAT NOTE WAS WRONG! | いまの おと、はずれてる! |
| S30.4 | M | scene | POP | C | ...THAT WHISTLE. HE CAME. | ・・・あの くちぶえ。 / きて くれたのか。 |
| S30.5 | M | scene | POP | K | FAKE! FAKE FAKE FAKE! | にせもの! にせものー! |
| S30.6 | S | flavour | POP | C | MADE BY MR. Y. OF COURSE. | Mr.Yせい。やはりな。 |
| S30.7 | S | scene | POP | BM | ...BREAK MAN. | ・・・ブレイクマンだ。 |
| S30.8 | S | scene | POP | K | TWO BREAK MEN! | ブレイクマンが ふたり! |
| S30.9 | S | scene | POP | C | ONE AND A HALF. | ひとりと はんぶん だな。 |
| S30.10 | S | scene | POP | BM | HE'S YOURS, ROCK. | こいつは おまえの ぶんだ、ロック。 |

S30.2 plays as the bar fills; S30.3 on the first red note (H5-05, b2's tell); S30.4 when the real whistle answers
(H5-07); S30.5 when the disguise falls by either route (H5-06). S30.6 reads the `MADE BY MR. Y` stamp in his visor
(fortress's defeat). S30.7-S30.10 are the partner's version (TWO BREAK MEN, H5-05 called in person). This is Rockman 5's
own reveal (A-5.2): the real Blues shows up and the fake is unmasked.

#### S31 Mr. Y's and Wily's heckles

The CX Light 6 pattern: one P1 line per respawn in H1-W3, replacing the death line. The tables are §6.5.

#### S32 The cup on the pedestal · Must

H5's throne room after Dark Man (fortress §4.6 step 1): the GP Cup on the pedestal, cables running into the walls.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S32.1 | M | scene | WIN | K | THE CUP! IT'S PLUGGED INTO / SOMETHING! | カップだ! なにかに / つながってる! |
| S32.2 | M | scene | WIN | Y | CONGRATULATIONS! YOU HAVE / REACHED THE FINAL EXHIBIT... / ME! | おめでとう ございます! / さいごの てんじひんは・・・ / わたくし で ございます! |
| S32.3 | S | flavour | WIN | C | INTO EVERYTHING, BY THE LOOK / OF IT. | みたところ なにもかもに だな。 |

#### S33 The unmasking; Project SUPER (EVENTS b6) · Must

H5 15 (fortress §4.6, on vanilla's Mr. X reveal: the pod, the typed speech, the flight path). **Two masks** (fortress
§4.6, consistency-6): the Y mask comes off and shows last year's Mr. X face; the X mask comes off and shows Wily. "WE
KNOW." plays in five windows at once, one per face icon (Cossack, Kalinka, Rock; Light and Roll on the radio): **Act
IV's Wily gag**. Light says "Albert" here, once. Then the pod's claw takes the cup (it turns up again in W3's Trophy
Dispenser), the typed black page, and vanilla's Wily Fortress picture in four greens stepping up to the SUPER palettes.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S33.1 | M | scene | WIN | Y | IT IS TIME YOU LEARNED THE / TRUTH. MR. Y IS... / ACTUALLY... | しんじつを おしえて しんぜよう。 / Mr.Yの しょうたいは・・・ / じつは・・・ |
| S33.2 | M | scene | WIN | K | ...MR. X?! | ・・・Mr.X!? |
| S33.3 | M | scene | WIN | W | SURPRISE! IT'S ME, DR. WI- | ジャーン! わしじゃ! Dr.ワイ・・・ |
| S33.4 | M | scene | WIN | R, L, Ro, C, K | WE KNOW. | しってる。 |
| S33.5 | S | flavour | WIN | W | ...HOW?! | ・・・なぜじゃ!? |
| S33.6 | M | scene | WIN | C | YOU WORE LAST YEAR'S MASK / UNDER THIS YEAR'S. | きょねんの マスクの うえに / ことしの マスクを かぶってたな。 |
| S33.7 | M | scene | WIN | L | I'D KNOW YOU ANYWHERE, / ALBERT. | アルバート、おまえの ことは / どこに いても わかるわい。 |
| S33.8 | M | scene | WIN | W | BAH! DO YOU KNOW WHAT THAT / CUP IS? EVERY MATCH OF THIS / GRAND PRIX, RECORDED BY MY / CAMERAS. ALL IN THE CUP! | ええい! あの カップが なにか / わかるか? この グランプリの しあいは / すべて わしの カメラが きろく / した。ぜんぶ カップの なかじゃ! |
| S33.9 | M | scene | WIN | W | WITH IT I BUILT BASS β. NEXT / I UPGRADE EVERY ROBOT ON / EARTH TO 16 BITS, RUNNING / WILY OS. PROJECT SUPER! | それで フォルテβを つくった。 / つぎは ちきゅうの ロボットを / すべて 16ビットに。ワイリーOSで! / プロジェクト・スーパーじゃ! |
| S33.10 | M | scene | WIN | W | THREE COLOURS A SPRITE! / EIGHT SPRITES A LINE! FIVE / SOUND CHANNELS! THE FUTURE / HAS MORE, ROCKMAN! | スプライト ひとつに 3しょく! / よこに 8まい! おとは 5チャンネル! / みらいには もっと あるのじゃ! |
| S33.11 | M | scene | WIN | L | YOU CAN'T FORCE AN UPGRADE / ON THE WORLD. PEOPLE MOVE ON / WHEN THEY'RE READY. | アップグレードを せかいに / おしつける ことは できんぞ。ひとは / じゅんびが できたら すすむ ものじゃ。 |
| S33.12 | M | scene | WIN | W | WATCH ME! SUPER WILY / CASTLE... RISE! | みておれ! スーパー ワイリー / キャッスル・・・ しゅつげん!! |
| S33.13 | M | scene | PLQ | — | THIS TIME, IT'S A SUPER / SERIOUS MATCH!! | こんどは スーパー / しんけんしょうぶ だ!! |
| S33.14 | M | scene | WIN | K | PAPA... WHY IS IT GREEN? | パパ・・・ なんで みどりいろ なの? |
| S33.15 | M | scene | WIN | C | IT IS STARTING FROM THE / BOTTOM. | いちばん したから はじめる らしい。 |

S33.10 is accurate NES trivia (3 colours plus transparency per sprite palette; 8 sprites per scanline; 2 pulse,
triangle, noise and DPCM channels: A-6.4). Wily is half right, which is the point of §1.4. S33.13 puns on vanilla's own
typed line `$6E`, 「こんどは しんけんしょうぶ だ!!」 (`rm6/text.md`).

---
### Act V: Project SUPER

#### S34 The Super Wily Castle map · Must

First visit (`meta.md` §3.9). In v1.0 W1's door is shut and the route is W2 → W3.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S34.1 | M | scene | WIN | W | WELCOME TO MY CASTLE! THE / HIGHER YOU CLIMB, THE BETTER / IT LOOKS. LITERALLY! | スーパー ワイリー キャッスルへ / ようこそ! のぼれば のぼるほど / きれいに なるぞ。もじどおり! |
| S34.2 | S | flavour | WIN | K | HE'S RIGHT. THAT'S THE WORST / PART. | ほんとう なのが くやしい。 |

#### S35 W1: the Upgrade Lab · Could (R0.3 item 5)

`fortress.md` §5.1. **The W1 boss is METALL 16** (R3.6, design-24: round 1's THE UPGRADER is withdrawn), and its "INSTALLING
3%" joke moves to the FORMAT CHECK gate at 00 (consistency-6). The 32-BIT room's plaque is here too.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S35.1 | C | scene | POP | PA | FORMAT CHECK: ROCKMAN IS / OBSOLETE. DOWNGRADING... 3% | チェック: ロックマンは ふるい! / ダウングレード 3% |
| S35.2 | C | scene | POP | PA | PLEASE DO NOT TURN OFF YOUR / ROBOT. | ロボットの でんげんを / きらないで ください。 |
| S35.3 | C | flavour | POP | K | DON'T TURN HIM OFF! | きっちゃ だめー! |
| S35.4 | C | flavour | POP | K | EVERYTHING'S GREEN! LIKE A / HANDHELD! | ぜんぶ みどり! / けいたいき みたい! |
| S35.5 | C | flavour | POP | C | FOUR SHADES. VERY / ECONOMICAL. | 4しょく だけ。 / けいざいてき だな。 |
| S35.6 | C | flavour | POP | K | COLOURS! OUR COLOURS! | いろが ついた! いつもの いろ! |
| S35.7 | C | flavour | POP | C | THE MUSIC HAS... MORE / CHANNELS. | おんがくの チャンネルが・・・ / ふえている。 |
| S35.8 | C | flavour | POP | K | PAPA, THE BLOCKS HAVE / *GRADIENTS*. | パパ、ブロックに / *グラデーション*が ある! |
| S35.9 | C | flavour | POP | W | BEHOLD! SIXTEEN BITS! | みよ! 16ビット じゃあ! |
| S35.10 | C | flavour | POP | K | IT'S WAVING A WHITE FLAG! | しろはた あげてる! |
| S35.11 | C | plaque | PLQ | — | ROCKMAN 8 (1996) IS ON LOAN / FROM A FUTURE THAT IS NOT / READY YET. PLEASE DO NOT / SCRATCH THE DISC. | ロックマン8 (1996)は まだ / じゅんびの できて いない / みらいからの かしだし。 / ディスクに きずを つけないで ください。 |

S35.7 plays only if the MMC5 voices ship as well (R8.3: they are Could, and the castle adds them); without them W1 skips
it, since every 2A03 channel already plays in the castle and nothing is added.

#### S36 W2: the Bracket of Doom · Must (the hub, TAG!); Should (the shouts)

`fortress.md` §5.2: the hub is a bracket board; each pair bout runs through tech's fight loader into the champion's own
arena; between the two bouts of a pair, the TAG! card. The copies are **data copies** built from the cup; the real
champions watch from the stands, and their shouts on each copy's bar fill are **Should** (fortress's second trim). The
copies' cards read `BLIZZARD.EXE` and kin (§5.2).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S36.1 | M | scene | POP | W | THE BRACKET OF DOOM! EVERY / FOE REBUILT FROM YOUR DATA! | ドゥーム トーナメント! あいては / おまえの データで つくった! |
| S36.2 | M | scene | POP | K | THOSE AREN'T THE REAL / CHAMPIONS! THEY'RE COPIES! | ほんものの チャンピオンじゃ ない! / コピーだよ! |
| W2-03 | M | scene | POP | C | TAG! THE SECOND COPY IS IN! | タッチ! 2たいめの コピーだ! |
| S36.3 | S | flavour | POP | C | THE REAL ONES ARE IN THE / STANDS. BOOING. | ほんものは かんきゃくせきに / いる。ブーイング ちゅうだ。 |
| S36.4 | S | flavour | POP | Blizzard | HEY! THAT COPY'S GOT MY / SKIS! GET HIM! | おい! あの コピー おれの / スキー はいてるぞ! やっちまえ! |
| S36.5 | S | flavour | POP | Wind | MY COPY CAN'T EVEN FLY / STRAIGHT! SHOOT HIM DOWN! | おれの コピー まっすぐ / とべて ないぜ! うちおとせ! |
| S36.6 | S | flavour | POP | Plant | OH NO, HE'S TRAMPLING / EVERYTHING. PLEASE HURRY. | ああ なにもかも ふみつけて。 / いそいで ください。 |
| S36.7 | S | flavour | POP | Flame | AN IMPOSTOR! DUEL HIM FOR / MY HONOUR! | にせものめ! わがはいの / めいよの ために たたかえ! |
| S36.8 | S | flavour | POP | Yamato | THAT ONE MOVES TOO MUCH. IT / IS NOT ME. | あやつは うごきすぎる。 / せっしゃ では ない。 |
| S36.9 | S | flavour | POP | Tomahawk | THAT COPY DREW BEFORE THE / FLAG! FOUL! | あの コピー はたの まえに / ぬいたぞ! フライングだ! |
| S36.10 | S | flavour | POP | Knight | A FALSE KNIGHT! SMITE HIM, I / BESEECH THEE! | にせの きしめ! なんじ / たのむ、うちたおせ! |
| S36.11 | S | flavour | POP | Centaur | DOES THE COPY KNOW MY / ABILITY? I'D LOVE TO KNOW. | コピーは わたしの のうりょくを / しってるのかな? しりたい。 |

#### S37 Bass β, duel 2 · Must

W2 11, the Championship Ring (fortress §5.2.3). SC6 starts adapted to the column Rock used most in duel 1
(`BASS_ADAPT`); S37.1 names it through the `%WEAPON%` variable, so the script tells the player what to do (W2-05). At 0
HP he drops to one knee and teleports; **his vow waits for the podium** (S41.5).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S37.1 | M | scene | WIN | B | ROUND TWO, ORIGINAL. I'VE / BEEN PATCHED. YOUR %WEAPON% / WON'T WORK ON ME NOW. | 2ラウンドめだ、オリジナル。 / パッチは あてた。%WEAPON%は / もう きかないぜ。 |
| S37.2 | M | scene | WIN | R | THEN I'LL USE THE OTHERS. | なら ほかの ぶきを つかうよ。 |
| S37.3 | S | flavour | WIN | B | ...HUH? | ・・・は? |
| S37.4 | M | scene | POP | B | TCH... THIS ISN'T OVER, / ORIGINAL. | ちっ・・・ これで おわりじゃ / ねえぞ、オリジナル。 |

#### S38 WILY MACHINE 6.5 · Must

W3 05-06 (fortress §5.3.2): vanilla's Wily Machine 6, retinted, over the 8-band floor. Kalinka is right: the "Mode 7"
floor is a per-band scroll (tech's `RL_FLOOR8`), the honest NES answer to a 16-bit feature; the joke is the effect's own
credit line. W3-02 is the mortar shadow's tell; W3-03 is S38.4-S38.5.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| W3-01 | S | flavour | POP | W | WELCOME TO THE FINAL ROUND! / ENTRY FREE. EXIT? NOT FREE. | さいしゅうせんへ ようこそ! / はいるのは ただ。でるのは・・・ |
| S38.1 | M | scene | POP | W | BEHOLD: WILY MACHINE 6.5! / HALFWAY TO THE FUTURE! | みよ! ワイリーマシーン 6.5ごう! / みらいへの はんぶん じゃ! |
| S38.2 | S | flavour | POP | K | SIX POINT FIVE? | 6.5? |
| S38.3 | M | scene | POP | C | SIX POINT FIVE. HE COULDN'T / WAIT FOR SEVEN. | 6.5ごう。7まで / まてなかった らしい。 |
| W3-02 | M | secret | POP | C | WATCH THE SHADOWS! THAT'S / WHERE THE SHELLS LAND. | かげを みろ! そこに / ほうだんが おちてくる! |
| S38.4 | M | scene | POP | W | MODE 7! THE FLOOR ROTATES! / ...IT'S SUPPOSED TO ROTATE. | モード7! ゆかが かいてん するのじゃ! / ・・・する はず なのじゃ。 |
| S38.5 | M | scene | POP | K | IT'S JUST SCROLLING IN / STRIPS. | よこじまで スクロール / してる だけ だよ。 |
| S38.6 | S | flavour | POP | C | IT'S A VERY GOOD EFFORT. | よく がんばって いる。 |
| S38.7 | S | flavour | POP | W | NOT YET! NOT YET! | まだじゃ! まだ おわらんぞ! |

#### S39 The Capsule; Break Man's gift; the dogeza; the escape · Must

W3 06 and the escape 07-0C (fortress §5.3.3, §5.4). **The gift** (SC11): when Rock's HP falls below 6 in the Capsule
phase, the screen darkens with yellow sparkles, the whistle plays, the NPC beams in, says one line and throws the orb;
**nobody says Blues**. **The dogeza** (vanilla's ending art) keeps only its begging line: the one Mr. Y gag of the ending
belongs to the arrest (R4.1 step 4; fortress open question 3: no Mr. Y line here). Then the PA, the clock and the
collapse; at 0C Wily's pod is jammed in the exit door and Rock pulls him out by the collar as the floor gives way.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S39.1 | S | flavour | POP | W | THE CAPSULE HAS THREE NEW / COLOURS! | カプセルには あたらしい いろが / 3つも あるのじゃ! |
| W3-04 | S | flavour | POP | K | THREE CAPSULES?! ONLY ONE / HAS THE BADGE! | カプセルが 3つ!? / バッジが あるのは ひとつ! |
| S39.2 | M | scene | POP | BM | ...TAKE IT. FINISH THIS. | ・・・うけとれ。けりを つけろ。 |
| S39.3 | M | scene | POP | W | F-FORGIVE ME! I'LL NEVER DO / IT AGAIN! ...PROBABLY! | ゆ、ゆるして くれ~! もう しない! / ・・・たぶん! |
| S39.4 | M | scene | POP | PA | PROJECT SUPER WILL NOW / SELF-DESTRUCT. THANK YOU! | スーパーけいかく、じばく します。 / ありがとう ございました! |
| W3-06 | M | scene | POP | K | ONE MINUTE! RUN, ROCKMAN! | あと 1ぷん! はしって ロックマン! |
| W3-07 | M | scene | POP | W | MY POD'S STUCK! ROCKMAN, / PULL ME OUT! PLEASE? | ポッドが つまった! ロックマン、 / ひっぱりだして くれ! たのむ! |
| S39.5 | M | stage | LBL | HUD | WPN: CB · TIME! · INJURY TIME: 30 | |

S39.4 credits 4MI's self-destruct announcement. The escape's mercy (60 → 90 s from the 4th attempt) is never explained
in the stage; Cossack confesses it at the podium (S41.8).

### Act VI: the ending

R4.1's order, staged by `fortress.md` §6.1. The castle pixelating (scene 2) has no words.

#### S40 Break Man catches Rock and Wily · Must (lines); Should (the carry art)

Scene 3: the whistle over the white-out; on the grass by the bay the NPC sets Rock and Wily down. **Rock's second and
last "Blues?"** (§1.3). In v1.0 the catch happens inside the white-out and the scene uses the NPC's stand and walk
frames; the carry art is Should. "This time" answers Rockman 3, which ended with Break Man pulling Rock out of the
collapsing fortress and Wily left in the rubble (A-3.5).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S40.1 | M | scene | WIN | BM | ...TCH. I'LL TAKE HIM TOO. / THIS TIME. | ・・・ちっ。そいつも つれていく。 / こんどは な。 |
| S40.2 | M | scene | WIN | R | BLUES? | ブルース? |
| S40.3 | M | scene | WIN | BM | BREAK MAN. | ブレイクマンだ。 |
| S40.4 | C | scene | WIN | K | ...WAS THAT...? | ・・・いまのは・・・? |
| S40.5 | C | scene | WIN | C | YES. | ああ。 |

S40.4-S40.5 replace S40.1-S40.3 on a doped file (Could, with the bundle): he catches them, sets them down and walks
off without a word, and Rock does not ask.

#### S41 The arrest; the podium and Bass's vow · Must

Scene 4: two Committee guards (recoloured vanilla robots) lead Wily away, under vanilla's Wily-behind-bars art. **The
one Mr. Y gag of the ending** (R4.1 step 4), and Act V's: R8.5 makes it the ending's only alias gag. Scene 5: the GP
Stadium by day; Rock on the top step holding the GP Cup he recovered in W3; the champions applaud below **in pairs**
(R8.6: 0 new tiles; the all-eight BG row is Should); Bass β beams in at the pitch's edge for his vow (PLAN's
Rockman 7 nod, A-7.1) and leaves in a multicoloured beam. If the escape's mercy fired, Cossack confesses (4MI's "who
lowered the output?" in tournament clothes). STORY_BEAT → `$0C`.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S41.1 | M | scene | WIN | W | IT WAS MR. Y'S IDEA! MR. Y / MADE ME DO IT! | Mr.Yの さしがね なのじゃ! / Mr.Yに やらされたのじゃ! |
| S41.2 | M | scene | WIN | R | YOU ARE MR. Y. | あなたが Mr.Y です。 |
| S41.3 | M | scene | WIN | W | ...MR. Y IS VERY PERSUASIVE. | ・・・Mr.Yは くちが うまいのじゃ。 |
| S41.4 | M | scene | WIN | C | LADIES, GENTLEMEN, ROBOTS: / YOUR GRAND PRIX CHAMPION, / ROCKMAN! | みなさん! グランプリ / チャンピオンは・・・ / ロックマン! |
| S41.5 | M | scene | WIN | B | ENJOY IT, ORIGINAL. NEXT / TIME, IT WON'T BE 8-BIT. | せいぜい よろこべ、オリジナル。 / つぎは 8ビットじゃ ねえぞ。 |
| S41.6 | S | flavour | WIN | K | NEXT TIME? | つぎ? |
| S41.7 | S | flavour | WIN | C | HE SOUNDED VERY SURE. | ずいぶん じしん ありげ だったな。 |
| S41.8 | M | scene | WIN | C | ABOUT THAT ESCAPE CLOCK: THE / REFEREE ADDED INJURY TIME. / DON'T TELL ANYONE. | だっしゅつの とけいの こと だが・・・ / しんぱんが ロスタイムを たした。 / ないしょ だぞ。 |

#### S44 The CAPCOM TIMES · Must

Scene 6: vanilla's newspaper driver (`$3B:$A886`), its masthead `CAPCOM TIMES ●▲.●▲.20XX` kept, the headline picture
redrawn, two lines a page. The last two pages are **vanilla's own `$95/$96`, word for word in JP** (the 1993 game's
sincere last sentence); EN translates them. **`$94` is not reprinted** (R4.1): S02 quoted it, and page 2 answers it.
**R8.5: the alias gag plays once in the whole ending, at the arrest**, so page 4 is the fallback S44.4F (no Mr. Z) and
Act VI's Wily gag is page 1's "WE KNEW.", the press's answer to S33's "WE KNOW.".

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S44.0 | M | stage | LBL | headline | ROCKMAN WINS GP!! | |
| S44.1 | M | scene | NEWS | — | ROCKMAN WINS THE GRAND PRIX! / MR. Y WAS DR. WILY. WE KNEW. | ロックマン グランプリ ゆうしょう! / Mr.Yの しょうたいは ワイリー。 |
| S44.2 | M | scene | NEWS | — | WILY IS BACK IN JAIL. GUARDS / CHECK DAILY: NOT CARDBOARD. | ワイリーは ふたたび ろうやへ。 / だんボールで ないか まいにち かくにん。 |
| S44.3 | M | scene | NEWS | — | THE ROBOT BASS IS STILL AT / LARGE. HE SAID: NEXT TIME. | ナゾの ロボット フォルテは / ゆくえふめい。「つぎは」と いっていた。 |
| S44.4F | M | scene | NEWS | — | NEXT YEAR'S SPONSOR: NOT YET / ANNOUNCED. COSSACK RELAXES. | らいねんの スポンサーは みてい。 / コサックは ほっと している。 |
| S44.4 | W | scene | NEWS | — | NEXT SPONSOR: MR. Z. COSSACK / ASKS FOR A LONGER ALPHABET. | らいねんの スポンサーは Mr.Z。 / コサックは ながい アルファベットを ようきゅう。 |
| S44.5 | M | scene | NEWS | — | A HEART FOR PEACE, AND A / STRENGTH NO EVIL CAN BEAT... | しかし へいわを あいする こころと / あくに まけない ちからを もった |
| S44.6 | M | scene | NEWS | — | AS LONG AS ROCKMAN IS HERE, / PEACE WILL SURELY LAST!! | さいきょうのロボット ロックマンが / いるかぎり このへいわは つづくだろう!! |
| S44.7 | C | stage | LBL | headline | CHAMPION'S CHIP UNDER REVIEW | |
| S44.8 | C | scene | NEWS | — | JUDGES REVIEW A CHIP STAMPED / Y. THE WIN GETS AN ASTERISK. | しんさいんは 「Y」の チップを / ちょうさちゅう。けっかは ほしじるしつき。 |

S44.4F is page 4 (R8.5); S44.4's Mr. Z page is kept as a Won't record (round 2 had it Must). S44.5-S44.6's JP is vanilla's text verbatim; the EN is GP's translation (the vanilla game had no EN for them). S44.7-S44.8
are the doped file's headline and page 1 (Could, with the bundle); the wording `UNDER REVIEW` is story's (consistency
decision 10), and systems §9.4 and fortress cite it.

#### S45 The credits · Must (the roll's text); the victory lap · Could

Scene 7: **v1.0 uses the vanilla staff-roll engine** with GP text and the DWNB cards (R4.1 step 7; fortress §6.2): each
champion fights in his own GP room (a credits mode, or his card strip only), then his vanilla card types, **verbatim**,
including vanilla's spellings (`DWNB-41 BLIZZARD-MAN / DESIGNER HIROFUMI OGAWA` … `DWNB-48 YAMATOMAN / DESIGNER RAI
ICHIKAWA`). These eight people are the reason the game exists. Then the staff roll on the starfield, English in both
languages as vanilla's is: the GP staff by role (the release build refuses an empty role: 4MI's WIP lesson), vanilla's
1993 roll (`$81-$86`) unchanged under a `ROCKMAN 6 (1993)` header, special thanks, and vanilla's `PRESENTED BY CAPCOM`
last.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S45.1 | M | stage | LBL | roll | ROCKMAN 6 GP STAFF · ROCKMAN / 6 (1993) · SPECIAL THANKS | |
| S45.2 | M | stage | LBL | roll | ROCKMAN CX (HIMAJIN JICHIKU) / ROCKMAN 4 MINUS INFINITY / (PURESABE) | |
| S45.3 | M | stage | LBL | roll | AND EVERY FAN WHO EVER / MAILED A ROBOT TO CAPCOM. | |
| S45.4 | C | stage | LBL | roll | TRANSLATION: (RESERVED) | |

**The victory lap** (Could, R0.3 item 8; fortress §6.3: one lap, more optional) replaces the roll when it ships. Touch a
champion for his card and his line; the roll call **ALL ENTRANTS** lists every enemy as an entrant, each one
`ELIMINATED` (4MI's FABRICATED ENEMIES), generated at build time from the object families' name fields (consistency
decision 41), ending `GRAND PI-KUN ...DEFLATED` and `BASS β ...ESCAPED`.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S45.10 | C | flavour | POP | Blizzard | GOOD MATCH, CHAMP! THE SUN / CAME OUT FOR YOU! | いい しあい だったぜ! / おまえの ために たいようが でたな! |
| S45.11 | C | flavour | POP | Centaur | I FOUND MY ABILITY! IT'S / CHEERING! | わたしの のうりょくが / わかりました! おうえん です! |
| S45.12 | C | flavour | POP | Flame | A BOW FOR THE CHAMPION! | チャンピオンに けいれい! |
| S45.13 | C | flavour | POP | Knight | HUZZAH! ALL HAIL THE / CHAMPION! | ばんざい! チャンピオンに / えいこう あれ! |
| S45.14 | C | flavour | POP | Plant | I PLANTED SOMETHING FOR YOU. / IT WILL BLOOM NEXT YEAR. | あなたの ために たねを / まきました。らいねん さきます。 |
| S45.15 | C | flavour | POP | Tomahawk | TAKE A BOW, CHAMP! THE / CROWD IS ALL YOURS. | おじぎしな、チャンピオン! / きゃくは おまえの ものだ! |
| S45.16 | C | flavour | POP | Wind | OKAY. YOU'RE THE ACE. THIS / TIME. | わかったよ。エースは おまえだ。 / こんかいは な。 |
| S45.17 | C | flavour | POP | Yamato | THIS ONE... MOVES. FOR YOU. / A LITTLE. | せっしゃ・・・ うごく。そなたの / ために。すこしだけ。 |
| S45.18 | C | flavour | POP | K | AND THE WINNER IS... | そして ゆうしょうは・・・ |
| S45.19 | C | stage | LBL | roll | ALL ENTRANTS · ELIMINATED · / DEFLATED · ESCAPED | |

Yamato takes one step on S45.17.

#### S46 The championship rating · Must (labels)

Scene 8, `meta.md` §6's screen: seven rows and a rank title under the number. Labels, English in both languages (the
rating panel is a menu, §10.1).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S46.1 | M | sys | LBL | rating | CHAMPIONSHIP RATING · / CHAMPIONSHIP · TEAM · ROUTE · / GEAR · MEDALS · FAIR PLAY · / BONUS | |
| S46.2 | M | sys | LBL | rating | GRAND CHAMPION · CHAMPION · / FINALIST · SEMIFINALIST · / QUARTERFINALIST · PARTICIPANT | |
| S46.3 | M | sys | LBL | rating | RESULT UNDER REVIEW | |

#### S47 Break Man's debrief · Must

Scene 8, after the rating (`meta.md` §6.2): one greeting, then the entry for the **first failed test** in meta's table
order, then "...HMPH." The NPC speaks through his face icon (R5.1). T1 in v1.0 is **SOLO RIOT** (the Riot won without his
help capsule, R4.2); the partner's entries return with the partner.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S47.0 | M | scene | WIN | BM | ...YOU WON. NOT BAD, ROCK. | ・・・かったか。わるくない、ロック。 |
| S47.T0 | M | scene | WIN | BM | THAT BIRD'S STILL IN PIECES. / B. E. A. T. SPELL IT. | あの とりは まだ バラバラだ。 / B、E、A、T。ぜんぶ あつめろ。 |
| S47.T1 | M | scene | WIN | BM | IN THE RIOT YOU NEEDED MY / HELP AGAINST BASS. NEXT / TIME, STAY ABOVE SIX. | ライオットの フォルテせんでは / おれの たすけが いったな。 / つぎは 6より うえで ねばれ。 |
| S47.T2 | M | scene | WIN | BM | THE JUDGES COUNTED %N% SECRET / EXITS. THERE ARE 8. ONE PER / VENUE. | ひみつの でぐちは %N%こ。 / ぜんぶで 8こ。かいじょうに 1こずつ。 |
| S47.T4 | M | scene | WIN | BM | EVERY VENUE HIDES ONE ROOM, / ONE SCREEN BIG. LISTEN TO / THE JUDGES. | どの かいじょうにも かくしべやが / ひとつ。しんさいんの ヒントを きけ。 |
| S47.T5 | M | scene | WIN | BM | SOME PRIZES AREN'T WON BY / WINNING. THEY'RE WON BY / ACTING STRANGE. | かって もらえない しょうひんも / ある。かわった ことを して / もらうんだ。 |
| S47.T6 | M | scene | WIN | BM | EDDIE'S SHELF ISN'T EMPTY. | エディの たなは まだ からじゃない。 |
| S47.T8 | M | scene | WIN | BM | GOLD IN EVERY VENUE. YOU / KNOW WHAT TO DO. | ぜんぶの かいじょうで ゴールド。 / わかるな。 |
| S47.T9 | M | scene | WIN | BM | NINETY-FIVE IS A PERFECT / RUN. GET THREE. | 95てんは かんぺきな しあい。 / 3つ とれ。 |
| S47.T10 | M | scene | WIN | BM | %N% GAME OVERS. A CHAMPION / DOESN'T PAY THE ENTRY FEE / TWICE. | ゲームオーバー %N%かい。 / チャンピオンは さんかひを / 2どは はらわない。 |
| S47.T11 | M | scene | WIN | BM | %H%:%MM% ON THE CLOCK. A / FIRST TITLE TAKES UNDER / THREE HOURS. | %H%じかん %MM%ふん。はじめての / ゆうしょうなら 3じかん いないだ。 |
| S47.T12 | M | scene | WIN | BM | THE STADIUM LOST POWER %N% / TIMES IN YOUR MATCHES. / FUNNY. IT NEVER DOES. | おまえの しあいの ときだけ / スタジアムが %N%かい ていでん。 / ふしぎ だな。 |
| S47.T13 | M | scene | WIN | BM | BASS TELLS EVERYONE HE HIT / YOU IN THE RIOT. MAKE HIM A / LIAR. | フォルテは ライオットで おまえに / あてたと いいふらしてる。 / うそに してやれ。 |
| S47.T14 | M | scene | WIN | BM | A CARD LIES IN THE 1993 / WING. MR. X. A REAL ONE? | 1993ねんの ウイングに めいしが / おちてる。Mr.X。ほんものか? |
| S47.T15 | M | scene | WIN | BM | YOU FELL IN A CHAMPION'S / RING. TOP SEEDS DON'T. | チャンピオンの リングで / たおれたな。トップシードは たおれない。 |
| S47.P | M | scene | WIN | BM | NOTHING TO ADD. YOU'RE THE / CHAMPION. GO HOME, ROCK. / WILY WON'T STAY PUT. | いうことは ない。チャンピオンは / おまえだ。かえれ ロック。 / ワイリーは じっと して いない。 |
| S47.Z | M | scene | WIN | BM | ...HMPH. | ・・・ふん。 |
| S47.T1S | S | scene | WIN | BM | YOU BARELY CALLED ME. PAUSE, / CALL, A. I'D HAVE COME. | ほとんど よばなかったな。 / ポーズして CALL、A。よべば いった。 |
| S47.T1D | C | scene | WIN | BM | YOU TOOK Y'S CHIP. I DON'T / TAG WITH CHEATS. | Mr.Yの チップを つかったな。 / ずるを する やつとは くまない。 |
| S47.T3 | C | scene | WIN | BM | FOUR BADGES ON THAT BRACKET. / TWO SECRET EXITS LIGHT EACH. | ひょうに バッジが 4つ。 / ひみつの でぐち 2つで 1つ ひかる。 |
| S47.PE | C | scene | WIN | BM | ADVICE? I HAVE NONE. / YOU ARE REAL CHAMPION! | (EN) |

S47.T11's "three hours" follows meta's T11 threshold (3:00:00, tuned at M9): if meta changes it, the line changes with
it. S47.P points at Rockman 7, which opens with Wily breaking out of jail (A-7.2). S47.T1S points at the pause menu's
CALL row confirmed with A (R2.10; `meta.md` §6.2), not at SELECT. **S47.T1 is v1.0's T1, SOLO RIOT** (meta RATEFLAGS
b4: Bass β duel 1 won without the capsule Break Man throws below 6 HP); it names the Riot, never a call or SELECT.
S47.PE is the ENGRISH perfect line (Could), a nod to 4MI's "I HAVE NO ADVICE. YOU ARE REAL HERO." (`r4mi/text.md` §4) in
new words (R8.4): the one ENGRISH line in story text, on purpose; its JP is the normal S47.P.

#### S42 LIGHTS OUT · Must

Scene 9 (fortress §6.1): night, the empty stadium. Rock and Dr. Light sit in the stands, with Roll, Rush, and Beat if
B-E-A-T is complete. The GP theme plays in **the lights-out arrangement** (G37 LAST MATCH, 2A03 stems; art_audio adds
it, consistency-13). The floodlight towers switch off one by one, and **each takes a music channel with it** through
tech's D9 mute mask, in `art_audio.md` §12.9's order: **the MMC5 voices first** (G37x, Could, only if they ship and
are on), **then noise, triangle and pulse 2; pulse 1 plays the melody alone**, and the last tower goes dark on its last
note (consistency decision 25: round 1's DPCM cue is deleted). **This is the game's only channel drop, and it is Must**
(R8.3): W2, W3 and the escape keep every 2A03 channel (their SUPER colour is palettes, parallax and palette bands), and
the escape's drop, if the MMC5 voices ship, takes only those voices: they are the only sound "already silenced when the
castle fell" (G37x, if it ships, voices them again for cue 0 below). Each switch-off is a palette step, never a
flash. **Light says "Blues" here, once** (R4.2).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S42.1 | M | scene | WIN | L | WILY WASN'T WRONG, YOU KNOW. / THE 16-BIT MACHINES ARE / COMING. BIGGER, FASTER, MORE / COLOURS. | ワイリーの いうことも / まちがっては おらん。16ビットの / マシンは もうすぐ くる。 / おおきく はやく いろも ゆたかに。 |
| S42.2 | M | scene | WIN | R | WILL I HAVE TO UPGRADE TOO, / DOCTOR? | ぼくも アップグレード / しなくちゃ いけないん ですか? |
| S42.3 | M | scene | WIN | L | SOMEDAY. WHEN YOU'RE READY. / NOT BY FORCE. NOT TONIGHT. | いつかは な。じゅんびが できたら。 / むりやり では なく。こんや でも なく。 |
| S42.4 | M | scene | WIN | L | EVERY MACHINE I BUILD WILL / BE OUTDONE BY THE NEXT ONE. / THAT ISN'T SAD, ROCK. THAT'S / THE JOB. | わしが つくる マシンは みな / つぎの マシンに こえられる。 / それは かなしい ことでは ない。 / それが しごと なのじゃ。 |
| S42.5 | S | flavour | WIN | Ro | THEY'RE CLOSING THE STADIUM, / YOU TWO. | スタジアム しまっちゃうわよ、 / ふたりとも。 |
| S42.6 | M | scene | WIN | L | AND ROCK... TELL BLUES HE / CAN COME HOME TOO. WHENEVER / HE'S READY. | それと ロック・・・ ブルースにも / いつでも かえって おいでと。 / じゅんびが できたらな。 |
| S42.7 | M | scene | WIN | R | LET'S GO HOME. | かえろう。 |

The cues, in §12.9's order (no DPCM cue; G37's sync marker switches each tower, so the picture follows the music):

| Cue | Tower and channel that go dark | Where |
|---|---|---|
| 0 | the two MMC5 towers (only with G37x and the MMC5 voices on; Could) | before S42.1 opens |
| 1 | **noise** | as S42.3 opens |
| 2 | **triangle** | as S42.4 opens |
| 3 | **pulse 2** | as S42.6 opens |
| 4 | **pulse 1** plays four bars alone after S42.7; the last tower goes dark on its last note; 60 frames of silence follow | the end |

S42.1 opens with the 2A03's four channels playing. Without MMC5 audio cue 0 does not exist and the scene starts with
four towers lit.

#### S43 The sixth wing · Must

Scene 10: the Hall of Fame the next morning, H5's room 19 finished, the GP Cup under its plaque. **Silent**: no music,
no typing blips, so pulse 1 stays the last sound (R4.1). The museum of the past ends on the game being played; PLQ.H5.19
set it up.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S43.1 | M | plaque | PLQ | — | WING 6: ROCKMAN 6 (1993). / 5 NOVEMBER: THE LAST ROCKMAN / ON THE 8-BIT CONSOLE. FANS / DESIGNED ITS EIGHT ROBOT / MASTERS. SIX WEEKS LATER, ON / 17 DECEMBER, ROCKMAN X CAME / TO THE 16-BIT CONSOLE: SIX / YEARS TO THE DAY AFTER THE / FIRST. EXHIBIT: THE GP CUP. | ウイング6: ロックマン6 (1993)。 / 11がつ5にち はつばい。8ビット / ゲームきで さいごの ロックマン。 / 8たいの ボスは ファンの デザイン。 / 6しゅうかんごの 12がつ17にち / ロックマンXが 16ビットきで / はつばい。さいしょの ロックマンから / ちょうど 6ねんごの おなじ ひ。 / てんじひん: GPカップ。 |

#### S48 TO BE CONTINUED [engine-ok] · Must

Scene 11: vanilla script `$88`, typed in silence (4 f/tile), English in both languages, kept on purpose (rm6 lesson 8);
START returns to the title. On the first clear the special-events line follows (`meta.md` §6.2).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S48.1 | M | stage | LBL | — | TO BE CONTINUED · (SPECIAL / EVENTS ARE NOW OPEN) | |

### Post-game

#### S49 Post-game bracket intro (EVENTS b7) · Must

The bracket, first visit after the ending (`meta.md` §3.6 makes EVENTS b7 Must).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| S49.1 | M | scene | WIN | K | WELCOME BACK, CHAMPION! / EVERY MATCH IS OPEN AGAIN. | おかえり チャンピオン! / ぜんぶの しあいで さいせん できるよ。 |
| S49.2 | S | flavour | WIN | C | ALSO, THE MUSEUM HAS A NEW / WING. SOMEONE DONATED A CUP. | それと はくぶつかんに あたらしい / ウイングが できた。カップを きぞう / した ものが いるそうだ。 |

#### S50 Mr. X Returns · Won't (v1) · S51 Bass Mode line swaps · Won't (v1)

R0.3 puts both in Won't. Their round-1 scripts (the real Mr. X, "THE REAL ONE", furious that Wily borrowed his name
twice; Bass's swaps at S02, S06, S14, S20, S33, S42) are kept in `build/revise/story/story_round1.md` for a later
release, with `meta.md` §9.7-§9.8's records. Two of their setups stay in v1.0 because they cost nothing: Mr. X's
business card (S28.9) and the `%PLAYER%` variable.

---
## 5. Boss intro cards (vanilla's boss panel, extended)

### 5.1 Format [engine-ok] + [new-code] S · Must

Vanilla's panel (`rm6/text.md` §4.4): after the frame (script `$13`) and CHR set `$8F` load, `$3C:$81B1` types one
**record** per boss: 9 fields, each ended by a byte with bit 7 set, chosen by `$51` through the pointer tables at
`$3C:$8606/$860E`. Field addresses and delays are tables (`$85EE-$8615`), so the layout can be re-flowed without code.

GP keeps the record format and its English text **in both languages** (vanilla's panel is English even in the JP game;
kept as a quirk, rm6 lesson 8). `tech.md` §11.2 builds the extension (M5, 1.5 sessions) and `art_audio.md` §9.2 draws
it. The M4 slice comes first, so it types vanilla's 9-field `BLIZZARDMAN` record by `$51`; Blizzard's VENUE
(`SUMMIT CLIMBER`, and `ABOVE THE CLOUDS` in the secret arena) arrives with the extension at M5:

1. **Records by fight id**, not `$51` (meta's fight table), so the champions, Bass β, the Hall of Fame exhibits and the
   castle bosses all get cards. ENTRANT FILES (`meta.md` §9.5, Should) reuses the same records.
2. **A tenth field, VENUE** (≤ 20 characters), in a strip the art adds to the panel frame (`$0624` starts at 9).
3. **A re-type entry**: a second record typed over the first, for Dark Man's lying panel (§5.4).
4. **Five glyphs added to the panel's bold set**: `-` `?` `!` `'` `β` (the panel CHR has 87 free tiles,
   `rm6/text.md` §7).
5. A **BG boss** (Grand Pi-kun, the Yellow Devil, Gamma, WILY MACHINE 6.5) shows its 16 × 16 face icon on the panel in
   place of a pose (art_audio §9.2).

| Field | Width | Vanilla address | Rule |
|---|---|---|---|
| HEIGHT / WEIGHT / ATTACK / DEFENCE / MOBILE | 3 each | `$206A` `$2079` `$20AA` `$20B9` `$20EA` | digits, right-aligned with spaces |
| ENERGY | ≤ 13 | `$20F1` | |
| LOCATION | ≤ 20 | `$2126` | |
| SPECIALTY | ≤ 19 | `$22E6` | |
| NAME | ≤ 12 | `$22AA` (8 f/tile, sound `$27`) | vanilla style: **no space in a Robot Master's name** (`BLIZZARDMAN`, so `BREAKMAN`, `DARKMAN`) |
| VENUE (new) | ≤ 20 | art places it | |

Glyphs on the panel: `0-9 A-Z . space` (vanilla) plus the five above. `fit.py` checks every record below for widths
and glyphs (§10.3). The panel is **labels** (English in both languages), counted apart from the translated strings
(§10.4).

After the panel, the stage loads, and when the boss bar fills the **bar-fill line** (POP) plays: S11 for champions,
S19/S37 for Bass β, S28 for the exhibits, S38-S39 for the castle.

**On-screen venue names are R3.3's** (§1.2 rule 5): SUMMIT CLIMBER, SKY ACE, LOST JUNGLE, PERSIAN PALACE, EDO NINJA
ROW, HIGH NOON FRONTIER, HERO'S QUEST, ATLANTIS RUINS. All fit the 20-character field.

### 5.2 The eight champions: vanilla's records, kept verbatim · Must

The 1993 numbers are canon and carry three of the venue jokes (SOLAR ENERGY on a glacier, MOBILE 31, ABILITY UNKNOWN).
Only VENUE is new.

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE | Tier |
|---|---|---|---|---|---|---|---|---|---|---|
| BLIZZARDMAN | 163 | 167 | 88 | 42 | 113 | SOLAR ENERGY | FROZEN ISLAND | MASTER OF SNOW | SUMMIT CLIMBER | M |
| WINDMAN | 169 | 173 | 66 | 129 | 51 | WIND ENERGY | MECHANICAL TOWER | MASTER OF WIND | SKY ACE | M |
| PLANTMAN | 143 | 111 | 42 | 103 | 98 | SOLAR ENERGY | FORGOTTEN AREA | FLOWER FANCIER | LOST JUNGLE | M |
| FLAMEMAN | 155 | 98 | 84 | 93 | 88 | THERMAL POWER | OIL FIELD | MASTER OF FLAME | PERSIAN PALACE | M |
| YAMATOMAN | 161 | 149 | 199 | 185 | 31 | SOLAR POWER | IMPREGNABLE FORTRESS | MASTER OF SPEAR | EDO NINJA ROW | M |
| TOMAHAWKMAN | 177 | 87 | 157 | 71 | 149 | SOLAR POWER | RESTRICTED AREA | MASTER OF TOMAHAWK | HIGH NOON FRONTIER | M |
| KNIGHTMAN | 158 | 146 | 121 | 204 | 60 | SOLAR POWER | CAPITAL OF SCIENCE | MASTER OF MACE BALL | HERO'S QUEST | M |
| CENTAURMAN | 155 | 172 | 35 | 47 | 205 | DRY BATTERY | ANCIENT CITY | ABILITY UNKNOWN | ATLANTIS RUINS | M |

**Secret arenas** use the same record with VENUE replaced. In v1.0 every secret arena is the venue's boss room with a
new palette (the venue docs, R0.3 item 4), so the v1.0 names describe what is on screen; the twist arenas' names come
back with them (Should).

| Venue | v1.0 VENUE (Must) | What the screen shows (venue doc) | With the twist (Should) |
|---|---|---|---|
| Blizzard | `ABOVE THE CLOUDS` | the sun deck above the clouds at sunset (venues_b §1.11) | `CLOUD SUMMIT` |
| Wind | `TOWER TOP AT NIGHT` | room 13 under the stars (venues_a §1.7.4) | `WING WALKER` |
| Plant | `LOST JUNGLE BY NIGHT` | room 17 in a night palette (venues_a §4.7.5) | `THE LOST CITY` |
| Flame | `THE PALACE AT NIGHT` | the boss arena at night, the hourglass mural (venues_b §2.9) | `THE THRONE ROOM` |
| Yamato | `THE THEATRE SET` | the castle hall before a striped curtain (venues_b §4.9) | `THE KABUKI STAGE` |
| Tomahawk | `THE RODEO RING` | room 17 at dusk with the flag judge (venues_a §3.8.5, R3.4) | (same) |
| Knight | `THE KNIGHTLORD` | room 1A in the revisit palette (venues_a §2.8.4) | (same) |
| Centaur | `TEMPLE OF TIDES` | the Temple of Tides in the revisit palette (venues_b §3.11) | `THE SUNKEN THRONE` |

**W2 refights** replace NAME with the copy's and VENUE with `BRACKET OF DOOM`: `BLIZZARD.EXE` (12), `WIND.EXE`,
`PLANT.EXE`, `FLAME.EXE`, `YAMATO.EXE`, `TOMAHAWK.EXE` (12), `KNIGHT.EXE`, `CENTAUR.EXE`. The joke is that the copies
are files (fortress §5.2; consistency-22). Must, with W2.

### 5.3 New entrants

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE | Tier |
|---|---|---|---|---|---|---|---|---|---|---|
| GRAND PI-KUN | 250 | 8 | 10 | 5 | 120 | HOT AIR | GP STADIUM | BEING ADORABLE | OPENING CEREMONY | M |
| BASS β | 133 | 105 | 199 | 99 | 199 | SPONSOR MONEY | MR.Y LABORATORY | BEATING ROCKMAN | HALFTIME RIOT | M |
| BASS β | 133 | 105 | 255 | 199 | 255 | SPONSOR MONEY | SUPER WILY CASTLE | FINAL VERSION | CHAMPIONSHIP RING | M |
| BLOCKMAN | 4 | 4 | 1 | 4 | 1 | GRAVITY | THE WELL | LINE CLEAR | EXHIBITION 1 | C |
| PADDLEMAN | 8 | 32 | 1 | 999 | 255 | BOUNCING | THE BRICK WALL | RETURNING BALLS | EXHIBITION 2 | C |
| INVADERMAN | 16 | 16 | 10 | 1 | 8 | 100 YEN COINS | TABLE CABINET | MARCHING DOWN | EXHIBITION 3 | C |
| MAZEMAN | 16 | 16 | 4 | 1 | 88 | POWER PELLETS | LEVEL 256 | EATING | EXHIBITION 4 | W |

- **Grand Pi-kun** (fortress §1.6: one size, 80 px tall, the Mr. X 2 pod technique): an inflatable mascot that weighs
  8 kg. HEIGHT 250 is the costume's claim, not the sprite's.
- **Bass β**, the Riot (fortress §2.6): one centimetre taller than Rockman's commonly given 132 cm (Appendix A, A-6.5).
  The SPECIALTY is never true. In W2 (fortress §5.2.3) he typed FINAL VERSION himself; the β stays on the NAME.
- **The Exhibition guests are Could** (R3.7); Maze Man is Won't (v1). Their panels keep vanilla's no-space style
  (`BLOCKMAN`, §5.1, R8.5); the dialogue says BLOCK MAN. Block Man shares his name with Rockman 11's (2018) Robot
  Master; Capcom's own name, kept as an in-joke (round 1's open question, closed). Block Man's "well" is the
  falling-block game's playfield; Invader Man's coins are the folklore R3.9 words as "THEY SAY THIS GAME CAUSED A
  COIN SHORTAGE" (Appendix A, A-8.12).

### 5.4 Hall of Fame exhibits and the castle

The exhibit cards are museum labels: LOCATION carries the year of the original fight.

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE | Tier |
|---|---|---|---|---|---|---|---|---|---|---|
| YELLOW DEVIL | 480 | 999 | 140 | 120 | 160 | CENTRAL EYE | WILY CASTLE 1987 | REASSEMBLY | HALL OF FAME 1 | M |
| MECHA DRAGON | 600 | 999 | 180 | 150 | 140 | DRAGON FIRE | WILY CASTLE 1988 | CHASING | HALL OF FAME 2 | S |
| GAMMA MK-VI | 999 | 999 | 200 | 200 | 10 | PEACEKEEPING | WILY CASTLE 1990 | KEEPING THE PEACE | HALL OF FAME 3 | M |
| DOC ROBOT | 180 | 220 | 120 | 110 | 90 | SKULL CORE | NEEDLE STAGE 1990 | COPY OF AIR MAN | HALL OF FAME 3 | S |
| C.CATCHER | 300 | 450 | 90 | 130 | 180 | PRIZE TOKENS | COSSACK CITADEL 1991 | GRABBING PRIZES | HALL OF FAME 4 | S |
| BREAKMAN | 170 | 120 | 150 | 140 | 100 | SOLAR POWER | BLUES CASTLE 1992 | DEFINITELY BREAKMAN | HALL OF FAME 5 | M |
| DARKMAN | 170 | 120 | 150 | 140 | 100 | SOLAR POWER | BLUES CASTLE 1992 | BAD DISGUISES | HALL OF FAME 5 | M |
| DARKMAN | 170 | 120 | 150 | 140 | 100 | SOLAR POWER | BLUES CASTLE 1992 | BAD DISGUISES | EXPOSED BY A WHISTLE | M |
| METALL 16 | 16 | 256 | 16 | 128 | 8 | 16 BIT CORE | SUPER WILY CASTLE | FORCED UPDATES | UPGRADE LAB | C |
| WILY MACHINE | 999 | 999 | 250 | 250 | 65 | PROJECT SUPER | SUPER WILY CASTLE | VERSION 6.5 | FINAL ROUND | M |
| WILY CAPSULE | 200 | 300 | 160 | 80 | 220 | PURE GENIUS | SUPER WILY CASTLE | ESCAPING | FINAL ROUND | M |
| MR.X | 175 | 70 | 50 | 50 | 50 | OLD MONEY | MR.X FORTRESS 1993 | BEING MR.X | MR.X RETURNS | W |

Notes:

- **Dark Man's panel lies with a straight face** (fortress §4.5.2; consistency-8). The first record types
  `BREAKMAN` / `DEFINITELY BREAKMAN` with no question mark (round 1's `BREAK MAN?` card is withdrawn). At THE MASK SLIPS
  the re-type entry types the second record over it: `DARKMAN` / `BAD DISGUISES`. When the WRONG NOTE exposes him
  (b2), the third record adds the "one extra line" fortress asks for, VENUE `EXPOSED BY A WHISTLE`. LOCATION is true
  in every version: in Rockman 5 Dark Man waited in what was believed to be Blues' castle (Appendix A, A-5.2), so the
  disguise's own card gives him away to anyone who reads it. fortress wrote `BREAK MAN` / `DARK MAN` with a space;
  this doc owns the words and keeps vanilla's no-space style, as R8.5 rules (§12); tech's panel re-type types all
  three records.
- **GAMMA MK-VI** is fortress's name (§4.3.6). Gamma was built by Light and Wily together as a peacekeeping robot in
  Rockman 3 (1990), hence ENERGY and SPECIALTY. **DOC ROBOT** (Should with his room, R3.6) fought in Rockman 3's four
  revisited stages (1990), two per stage, copying the eight Rockman 2 bosses; his AIR MAN copy waited in Needle Man's
  stage (Appendix A, A-3.4), and H3 is Needle Man's press hall, so LOCATION says so.
- **WILY MACHINE**'s panel reads `WILY MACHINE` … `VERSION 6.5` (R3.6's "WILY MACHINE 6.5" in the NAME's 12 cells);
  MOBILE 65 is "6.5". ENERGY is `PROJECT SUPER` (fortress §5.3.2, consistency-6); the GP Cup is no longer its core
  (round 1): the cup is recovered from the Trophy Dispenser (S39). VENUE `FINAL ROUND` is W3's welcome (W3-01).
- **METALL 16** is the W1 boss (R3.6; Could with W1). Round 1's THE UPGRADER is withdrawn. Its numbers are powers of
  two.
- **MR.X** (Won't, with Mr. X Returns, S50) is kept as a note.
- **Mid-bosses** (AYACO, CONGA, the Daruma, the Metal Metslime, Sidewinder, Shadow Rock, the Kamegoro Maker…) get
  records for ENTRANT FILES only (Should, with that page); their owners fill the fields with the same width rules.
  They show no card in play, as vanilla shows none for mid-bosses.

---

## 6. The commentator system

### 6.1 How it works [new-code] M · Must (M3, "commentator bus")

BRIEF §5.5: the commentators react to deaths with a rotating table per venue plus generic lines; in the fortress,
Mr. Y heckles between lives; lines are ≤ 2 lines and can be switched off. This is the engine that delivers them; the
pop-up itself is tech's text v1a (R1.4).

**Events.** Gameplay code raises an event id (one byte) with one argument byte. The v1.0 column is R4.5's: deaths,
first weaknesses, secret, plate and tell lines and the heckles are Must; flavour is Should.

| Event | Raised by | Argument | Table | Priority | v1.0 |
|---|---|---|---|---|---|
| `EV_DEATH` | the player-death path (exit code `$F0` = 2 or 3, `rm6/SUMMARY.md` §3; tech names the hook site) | cause: 0 enemy, 1 pit, 2 spike, 3 boss room | §6.3 venue table or §6.4's Opening and Riot tables; the generic table (§6.4) | P1 | **Must** (4 lines per stage); generic table **Should** |
| `EV_RESPAWN_HECKLE` | respawn in H1-W3 (meta 14-21) | — | §6.5 | P1 | **Must** (Mr. Y 6, Wily 4) |
| `EV_WEAK_FIRST` | `systems.md` §5, once per fight | fight id | §6.2 / §6.3 | P2 | **Must** |
| `EV_SECRET`, `EV_PLATE` | exit / room / item / envelope collected; a plate (tech §11.7 raises it apart) | kind 0-4 | the stage's own line if it has one, else §6.2 | P2 | **Must** |
| `EV_HOOK` | a stage object (stable ids: `BLZ-07`, `WND-08`, `OPN-08`, …) | hook id | §6.3, §6.4 | P2 (tells, secrets) / P3 (flavour) | **Must** for the tells and secret lines marked M; flavour **Should** |
| `EV_RESIST`, `EV_IMMUNE` | `systems.md` §5 | fight id | §6.2 | P3 | Should |
| `EV_OWN_WEAPON` | SC4, once per fight | fight id | §6.3 | P2 | Should (SC4 is Should) |
| `EV_PINCH` | boss enters pinch | fight id | §6.3 | P3 | Should |
| `EV_NODMG_BOSS` | boss killed with BOSS NO-HIT set (`systems.md` §6.5) | — | §6.2 | P2 | Should |
| `EV_EXCELLENT` | KAISHIN's strengthened hit (G.EX's "A SPLENDID STRIKE!"), first per stage visit (criticals are Won't, R2.4) | — | §6.2 | P4 | Should |
| `EV_CLOSE_CALL` | HP ≤ 3 and alive 300 f later, once per stage visit | — | §6.2 | P4 | Should |
| `EV_FORM_FIRST` | first use of POWER / JET / SUPER, once per save | form | §6.2 | P3 | Should |
| `EV_TIMESTOP_FIRST` | first C.FLASH Time Stop, once per save | — | §6.2 | P3 | Should |
| `EV_TANK` | E-tank or W-tank used, first per stage visit | — | §6.2 | P4 | Should |
| `EV_SYNERGY_FIRST` | first use of a synergy, once per save | synergy 0-7 | §6.2 | P3 | Should (with the synergies, R0.3 item 1) |
| `EV_TAG` | Break Man called / retreats | 0 call, 1 retreat | §6.2 | P3 | Should (with the partner, R4.2) |
| `EV_PARRY` | parry (first, and the 5th, per stage visit) | count | §6.2 | P3 | Could (PARRY is Could) |

**Priorities and the queue.**

- **P0** is story (scenes), outside this system: it always plays and pauses the game.
- **P1** (death, heckle) plays on the respawn's READY, held 2 s or until any button.
- **P2-P4** play in the pop-up during play, auto-advancing after `60 + 2 × characters` frames (90 minimum, 240
  maximum). No button dismisses a pop-up (the buttons are gameplay); START pauses it with the game.
- The queue holds 2 entries. A higher priority goes ahead; a P3/P4 entry older than 120 f is dropped.
- **Cooldown:** after a P3/P4 line, no other P3/P4 line for 600 f. P1/P2 ignore it.
- **Never** during a reaction-time prompt: READY's countdown, a quick-draw (`venues_a.md` VA-DRAW), a tunnel warning, a
  battle-log line (Knight), the boss panel, a dialogue window, or a boss's own bar-fill line. Time Attack (when built)
  plays none; GP Rush (when built) plays P1 only.
- **ANNOUNCER** (`meta.md` §11, DISPLAY `$009` b0-1): ON = all; DEATHS ONLY = P1 (+ P0); OFF = P0 only.

**The window** (R1.4): 2 × 28 cells, ≤ 24 glyph ids per page (`fit.py` checks every pop-up row in this doc), at the top
of the screen by default; the screen scripts of Wind 01 and Tomahawk 10-11 move it to the bottom (venues_a §0.6, tech
`EFFECTS` b6). The speaker's **face icon is 4 BG tiles inside the window**, never a sprite, so a pop-up occupies no
object slot and costs nothing against R1.8's cap of 9 occupied slots. **One speaker per page** (§2.7): round 1's
two-speaker lines are split into two rows or given to one speaker.

**Rotation.** A stage's death table plays **in order**, one line per KO in that stage visit. In v1.0 it loops its 4
Must lines; with the Should rows it runs 6, then hands over to the generic table (§6.4, Should) at a save-wide
rotating pointer. Cause-specific generic lines (pit, spike, boss room) are preferred when the cause matches. "First"
events use a 32-bit once-per-visit field in WRAM; once-per-save flags use COMMFLAGS (`meta.md` FILE `$04A`, story's
byte): b0 POWER, b1 JET, b2 SUPER, b3 Time Stop (the four first-use lines, Should), **b4 the first plate and b5 the
first envelope (Must: §6.2's plate and envelope lines)**, b6 Y-TURBO noticed (Could), b7 Break Man's first call
(Should).

**Data.** A line record is 6 bytes: speaker (face icon id), flags (variant selectors: before/after the unmasking,
DOPED, TAG, BASS), EN pointer, JP pointer. Stage tables are byte lists of line ids. The strings live in tech's text
banks, dictionary-compressed (R1.4); §10.4 counts them. [new-code] M (the bus, queue and window: tech's M3 item),
text per milestone.

**Speakers** (face icons, `art_audio.md` §9.4): Cossack (C), Kalinka (K), Mr. Y (Y), Wily (W), Roll (Ro), Break Man
(BM), Light (L, a radio frame), Eddie (E), Bass β (B), the champions; NPCs without an icon (the King, the battle log,
the PA) speak in an icon-less pop-up. Four typing blips (§10.2).

### 6.2 Generic event lines

**First weakness on a non-venue boss** (`EV_WEAK_FIRST`; weaknesses per `systems.md` §5's v1.0 rows). The venue
champions' lines are in §6.3. Bass β has no WEAK cell: RIO-07 and W2-05 (SC6's tell) serve (S19, S37).

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| OPN-11 | M | weak | POP | K | HIT THE VALVE! CHARGED SHOTS / POP BALLOONS! | バルブを ねらって! / チャージで ふうせんが われる! |
| H1-05 | M | weak | POP | K | THE EYE FLINCHED! | めが ひるんだ! |
| H3-07 | M | weak | POP | K | RIGHT ON THE CHIN! IT'S / WOBBLING! | あごに めいちゅう! / ぐらついてる! |
| H5-08 | M | weak | POP | K | HE CAN'T TAKE THE HEAT! | あつさに よわい みたい! |
| WK-WM | M | weak | POP | C | SILVER TOMAHAWK! JUST LIKE / 1993! | シルバートマホーク! / 1993ねんと おなじだ! |
| WK-WC | M | weak | POP | K | BONK! THAT'S THE SPOT! | ゴツン! そこだよ! |
| WK-EX | C | weak | POP | K | THAT'S HOW YOU PLAY IT! | そう やって あそぶんだよ! |

SILVER.T was the Wily Machine 6's weakness in vanilla (`systems.md` §5 note; Appendix A, A-6.8), so WK-WM is true for
1993. WK-EX is the Exhibitions' (Could).

**Secrets** (`EV_SECRET`; the stage's own line plays instead where §6.3 or §6.4 has one) · Must:

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| G.SX1 | M | secret | POP | K | A SECRET EXIT! THE JUDGES / LOVE THIS! | ひみつの でぐち! / しんさいん だいこうぶつ! |
| G.SX2 | S | flavour | POP | C | OFF THE MAP. LITERALLY. | ちずに ない みちだ。 |
| G.SR | M | secret | POP | K | A HIDDEN ROOM! I KNEW IT / WAS THERE! | かくしべや! ぜったい あると / おもってた! |
| G.SI | M | secret | POP | C | A PRIZE FOR HOW YOU PLAYED. / THE JUDGES NOTICED. | あそびかたへの しょうひんだ。 / しんさいんは みていた。 |
| G.SP1 | M | secret | POP | C | BEAT'S PARTS! I BUILT THAT / BIRD, YOU KNOW. | ビートの パーツ! あの とりは / わたしが つくったんだぞ。 |
| G.SP2 | M | secret | POP | K | ANOTHER PIECE OF BEAT! | ビートの パーツ また ひとつ! |
| G.SE | M | secret | POP | C | A SPONSOR ENVELOPE, 30 / BOLTS. FROM MR. Y. COUNT IT. | ふうとうだ! 30ボルト。 / Mr.Yから だ。かぞえて おけ。 |

Cossack really did build Beat, in Rockman 5 (Appendix A, A-5.4). G.SP1 plays on the first plate of the save
(COMMFLAGS b4), G.SP2 after; G.SE on the first envelope (b5), later envelopes use G.SR's room line only.

**Resisted and immune** · Should:

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| G.RS1 | S | flavour | POP | C | THAT'S BARELY SCRATCHING / HIM! | ほとんど きいて いない! |
| G.RS2 | S | flavour | POP | K | TRY SOMETHING ELSE! THE / JUDGES LIKE VARIETY! | べつの ぶきを! しんさいんは / バラエティが すき! |
| G.RS3 | S | flavour | POP | C | WATCH THE FLASHING. HE / SHRUGS THAT OFF. | てんめつを みろ。 / へいき そうだ。 |
| G.IM | S | flavour | POP | K | NOT A SCRATCH! | きず ひとつ ない! |

G.RS3 teaches the i-frame read (4MI's "read the weakness from the flashing", BRIEF §5.1).

**Style, forms, partner, tanks** · Should (Could where marked):

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| G.ND1 | S | flavour | POP | K | NOT A SCRATCH ON HIM! A / PERFECT MATCH! | むきず! パーフェクト! |
| G.ND2 | S | flavour | POP | C | THE JUDGES ARE STANDING. TWO / OF THEM. ONE IS CARDBOARD. | しんさいんが たった。ふたり。 / ひとりは だんボール。 |
| G.ND2b | S | flavour | POP | C | THE JUDGES ARE STANDING. / ALL OF THEM. | しんさいんが たった。 / ぜんいんだ。 |
| G.ND3 | S | flavour | POP | C | FLAWLESS. WRITE THAT DOWN, / KALINKA. | かんぺきだ。 / メモして くれ カリンカ。 |
| G.EX | S | flavour | POP | K | A SPLENDID STRIKE! | みごとな いちげきが きまった! |
| G.CC1 | S | flavour | POP | K | HANGING ON BY ONE BOLT! | ボルト いっぽんで / ふみとどまってる! |
| G.CC2 | S | flavour | POP | C | LOW ON ENERGY. HIGH ON / SPIRIT. | エネルギーは ひくい。 / きあいは たかい。 |
| G.F1 | S | flavour | POP | K | RUSH POWER! LOOK AT THOSE / FISTS! | ラッシュパワー! / すごい こぶし! |
| G.F2 | S | flavour | POP | C | NINETEEN UNITS OF FUEL. / SPEND THEM WISELY. | ねんりょうは 19。 / だいじに つかえ。 |
| G.F3 | S | flavour | POP | K | SUPER ROCKMAN! IT'S ON LOAN, / SO IT'S LEGAL. | スーパーロックマン! / かりものだから セーフ! |
| G.TS | S | flavour | POP | K | TIME STOP! THAT'S FLASH / MAN'S OLD TRICK! | ときを とめた! / フラッシュマンの わざだ! |
| G.TK | S | flavour | POP | C | A TANK! THERE GO THE NO / TANKS POINTS. | タンクを つかった! / ノータンク ポイントは なしだ。 |
| G.T1 | S | flavour | POP | K | BREAK MAN IS IN! TAG TEAM! | ブレイクマン とうじょう! / タッグだ! |
| G.T2 | S | flavour | POP | C | ENTRANT 10 ENTERS THE MATCH. | 10ばん さんせん。 |
| G.T3 | S | flavour | POP | BM | TCH. YOUR TURN. | ちっ。おまえの ばんだ。 |
| G.SY1 | S | flavour | POP | K | A POGO! LIKE THE DUCK WITH / THE CANE! | ホッピング! ステッキの / アヒルさん みたい! |
| G.SY2 | S | flavour | POP | C | TAILWIND! RUSH HAS NEVER / FLOWN THAT FAST. | おいかぜ! ラッシュが / こんなに はやい! |
| G.SY3 | S | flavour | POP | K | SNOW BOMBS! LOOK OUT BELOW! | ゆきの ばくだん! / したに ちゅうい! |
| G.SY4 | S | flavour | POP | K | BURNING KNUCKLE! LIKE A / FIGHTING GAME! | バーニングナックル! / かくとうゲーム みたい! |
| G.SY5 | S | flavour | POP | K | A PETAL STORM! PRETTY, AND / BULLETPROOF! | はなふぶき! きれいで / ぼうだん! |
| G.SY6 | S | flavour | POP | C | A GIANT FLAIL! KNIGHT MAN IS / TAKING NOTES. | きょだいな フレイル! / ナイトマンが メモ してる。 |
| G.SY7 | S | flavour | POP | K | DIVE-BOMBING TOMAHAWKS! | きゅうこうか トマホーク! |
| G.SY8 | S | flavour | POP | K | A TIME FIST! PUNCH, PUNCH, / PUNCH, PUNCH! | タイムフィスト! / パンチ パンチ パンチ! |
| G.PR1 | C | flavour | POP | K | PARRY! HE PUNCHED A BULLET! | パリィ! たまを なぐりかえした! |
| G.PR2 | C | flavour | POP | C | FIVE PARRIES. SOMEBODY'S / BEEN PRACTISING. | パリィ 5かい。 / だれかさん れんしゅう したな。 |

G.ND2 plays until S33 (the third judge is a cardboard cut-out of Mr. Y), G.ND2b after. G.SY1 names DuckTales by its
hero, Capcom's own (1989; `systems.md` §3.2 credits it). G.TS: Flash Man's Time Stopper is Rockman 2's (Appendix A).
Round 1's "ORA ORA" (a third-party catchphrase) is replaced by plain punches (R3.3).

### 6.3 Venue tables: hooks and deaths

The venue docs own the triggers and the tiers (venues_a §1.10, §2.11, §3.11, §4.11; venues_b §1.13, §2.11, §3.13,
§4.12); the ids are theirs. In v1.0 each venue plays its **tells and secret lines, its first-weakness line and 4 death
lines** (R4.5); the flavour hooks and death lines 5-6 are Should. Death lines are one speaker each.

#### Wind: SKY ACE (`venues_a.md` §1.10)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| WND-01 | S | flavour | POP | C | ROCKMAN IS CLEARED FOR / TAKEOFF! | ロックマン はっしん よし! |
| WND-02 | S | flavour | POP | K | IT CHANGES WHEN YOU SHOOT / IT! | うつと かわるよ! |
| WND-03 | S | flavour | POP | K | RED SQUADRON DOWN! | あかい へんたい げきつい! |
| WND-04 | S | flavour | POP | C | THAT'S NOT A PLANE. THAT'S A / BIGGER PLANE. | あれは ひこうきでは ない。 / もっと おおきな ひこうきだ。 |
| WND-05 | S | flavour | POP | K | AYACO IS GOING DOWN! | アヤコ ついらく! |
| WND-06 | S | flavour | POP | C | ONE HUNDRED PERCENT! IN MY / DAY, WE CALLED THAT AN ACE. | げきついりつ 100%! / むかしは それを エースと よんだ。 |
| WND-07 | S | flavour | POP | K | WATCH THE WINDSOCK, ROCKMAN! | ふきながしを みて! |
| WND-08 | M | secret | POP | C | THE ELEVATOR'S MOVING! IT / ONLY TAKES ACES! | エレベーターが うごいた! / エースしか のせないんだ! |
| WND-09 | S | flavour | POP | K | HE LIKES THAT! | よろこんでる! |
| WND-10 | M | weak | POP | C | HIS ENGINES STALLED! NO / WIND, NO WIND MAN! | エンジン ていし! かぜが / なければ ウインドマンも ない! |
| WND-11 | S | flavour | POP | K | A LOOP! HE'S SHOWING OFF! | ループ! かっこつけてる! |
| WND.D1 | M | death | POP | K | MAYDAY, MAYDAY! | メーデー、メーデー! |
| WND.D2 | M | death | POP | C | HE FORGOT THE LOOP BUTTON. | ループを わすれたな。 |
| WND.D3 | M | death | POP | K | THAT CLOUD WAS NOT A FLOOR! | あの くもは ゆかじゃ ないよ! |
| WND.D4 | M | death | POP | C | THE WINDSOCK TRIED TO WARN / HIM. | ふきながしは ちゃんと / おしえて いた。 |
| WND.D5 | S | death | POP | K | GONE WITH THE WIND. | かぜと ともに さりぬ・・・ |
| WND.D6 | S | death | POP | C | EVEN 1942 GAVE YOU THREE / LOOPS! | 1942でさえ ループは / 3かい あったぞ! |

AYACO is 1943's own boss, a Capcom name. WND.D6: 1942 (Capcom, 1984) gave the player three loops (Appendix A, A-8.2).

#### Knight: HERO'S QUEST (`venues_a.md` §2.11)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| KNT-01 | S | flavour | POP | C | A RANDOM ENCOUNTER? IT IS / NOT RANDOM. I CHECKED. | ランダム エンカウント? / ランダムでは ない。しらべた。 |
| KNT-02 | S | flavour | POP | C | YOU CANNOT RUN FROM A / TOURNAMENT, ROCKMAN. | たいかいからは / にげられんぞ。 |
| KNT-03 | S | flavour | POP | K | HE BEAT THE CEILING. CAN YOU / DO THAT? | てんじょうに かっちゃった。 / そんなこと できるの? |
| KNT-04 | S | flavour | POP | C | THEY ALWAYS GET AWAY. / ALWAYS. | あいつらは かならず にげる。 / かならずだ。 |
| KNT-05 | M | secret | POP | K | STAIRS! BEHIND THE THRONE! / JUST LIKE THE OLD DAYS! | かいだん! ぎょくざの うしろ! / むかしと おなじ! |
| KNT-06 | M | secret | POP | K | THAT IS NOT HOW YOU FIND / SECRET STAIRS! | かくしかいだんは そうやって / さがすものじゃ ない! |
| KNT-07 | S | flavour | POP | C | SHIELD DOWN! NOW WE HAVE A / FIGHT! | たてが こわれた! / これで しょうぶに なる! |
| KNT-08 | M | weak | POP | K | RIGHT THROUGH THE SHIELD! | たてを つらぬいた! |
| KNT-09 | M | scene | POP | K | PAPA! HE TOOK THE DEAL! HE / PRESSED YES! | パパ! とりひきに のった! / はいを おしちゃった! |
| KNT-10 | S | flavour | POP | C | MACE MEETS MACE! | てつきゅう たい てつきゅう! |
| KNT.D1 | M | death | POP | King | O ROCK! TO FALL SO SOON! / ARISE, AND TRY AGAIN! | おお ロックよ! もう たおれたのか! / さあ たて! もういちど ゆけ! |
| KNT.D2 | M | death | POP | C | ROCKMAN WAS DEFEATED. THE / JUDGES ARE NOT PLEASED. | ロックマンは ちからつきた。 / しんさいんは ごきげんななめ。 |
| KNT.D3 | M | death | POP | C | THE CEILING WON THAT ROUND. | この ラウンドは / てんじょうの かち。 |
| KNT.D4 | M | death | POP | K | THAT CHEST HAD TEETH! | あの たからばこ はが あった! |
| KNT.D5 | S | death | POP | K | HE SHOULD HAVE STAYED AT THE / INN. | やどやに とまれば / よかったのに。 |
| KNT.D6 | S | death | POP | K | THOU ART... OUT OF HP. | HPが・・・ つきた。 |

KNT.D1 is the King's (venues_a §2.11: "the King, 1 + his death line"), in the icon-less pop-up. It nods to the genre's
famous scolding in new words, in both languages (R3.3, R8.4: round 2's JP kept the original's 「なさけない」; it is
gone). KNT.D4's Killer Chest is a Must enemy (venues_a SET-KN2); KNT.D5 waits for
the Inn (Should).

#### Tomahawk: HIGH NOON FRONTIER (`venues_a.md` §3.11)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| TMH-01 | S | flavour | POP | C | THREE BOUNTIES. KALINKA, MY / READING GLASSES. | しょうきんくびが 3にん。 / カリンカ、めがねを。 |
| TMH-02 | S | flavour | POP | K | NOT THE PIANIST! | ピアニストは だめ! |
| TMH-03 | S | flavour | POP | K | %T% SECONDS! WHAT A DRAW! | %T%びょう! すごい! |
| TMH-04 | S | flavour | POP | C | HE JUMPED THE FLAG! FOUL! | フライングだ! ファウル! |
| TMH-05 | S | flavour | POP | C | MIND YOUR HEAD, ROCKMAN! | あたまに きを つけろ! |
| TMH-06 | S | flavour | POP | K | HE GOT AWAY! NEXT TIME! | にげられた! つぎこそ! |
| TMH-07 | M | secret | POP | C | DEPUTY ROCKMAN! I ALWAYS / KNEW IT. | ほあんかん ロックマン! / わかって いたとも。 |
| TMH-08 | S | flavour | POP | C | THE OLD PIPE ROOM! STILL / HERE AFTER ALL THESE YEARS. | むかしの パイプべや! / まだ あったのか。 |
| TMH-09 | S | flavour | POP | K | HE'S TAKING THE HIGH ROAD! | そらの みちを いく つもりだ! |
| TMH-10 | M | weak | POP | K | BLESS YOU! HE DROPPED HIS / TOMAHAWK! | おだいじに! / トマホークを おとした! |
| TMH-11 | S | flavour | POP | C | NOT THE WHISTLE! | くちぶえは だめだ! |
| TMH-12 | S | flavour | POP | K | HE CAUGHT IT! | キャッチした! |
| TMH.D1 | M | death | POP | C | TOO SLOW ON THE DRAW. | ぬくのが おそかった。 |
| TMH.D2 | M | death | POP | K | THE 4:50 DOESN'T STOP FOR / ANYONE. | 4じ50ぷんの きしゃは / だれも まって くれない。 |
| TMH.D3 | M | death | POP | K | THE PIANIST IS FINE, BY THE / WAY. | ちなみに ピアニストは / ぶじです。 |
| TMH.D4 | M | death | POP | K | ALWAYS CHECK THE OUTHOUSE / FIRST. | まず トイレを しらべること。 |
| TMH.D5 | S | death | POP | C | THAT WAS A BAD TRADE, / PARTNER. | わるい とりひき だったな。 |
| TMH.D6 | S | death | POP | K | THE FLAG JUDGE SAYS: UP YOU / GET, AND WAIT FOR THE FLAG! | はたの しんぱんいわく: / たって はたを まて! |

Round 1's "Boot Hill" death line is dropped (R3.4); TMH.D6 is the new sixth, on the judged-event staging. TMH-04
follows the flag judge (R3.4: the draw is a judged tournament event). TMH-08: the Energy Balancer's pipe room is
vanilla's own (`rm6/SUMMARY.md` §1.3).

#### Plant: LOST JUNGLE (`venues_a.md` §4.11)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PLT-01 | C | flavour | POP | C | TWENTY MINUTES! ...IT DOES / NOTHING. OLD RULES. | のこり 20ぷん! ・・・なにも / おきない。むかしの ルールだ。 |
| PLT-02 | S | flavour | POP | C | HOLD ON TIGHT, ROCKMAN! | しっかり つかまれ! |
| PLT-03 | S | flavour | POP | K | CROCODILES! STAND ON THEIR / HEADS WHEN THEY CLOSE! | ワニだ! くちを とじたら / あたまに のって! |
| PLT-04 | S | flavour | POP | K | TIMBER! | たおれるぞー! |
| PLT-05 | S | flavour | POP | K | TREASURE! THAT'S %N% OF FOUR! | おたから! これで %N%こめ! |
| PLT-06 | S | flavour | POP | C | THAT'S PASTE. THE JUDGES / WANT REAL TREASURE. | それは イミテーションだ。 / ほんものを さがせ。 |
| PLT-07 | S | flavour | POP | K | EEK! | きゃっ! |
| PLT-08 | M | secret | POP | K | IS THAT... TANGO? WHERE IS / HE GOING? | あれって・・・ タンゴ? / どこへ いくの? |
| PLT-09 | S | flavour | POP | C | NINE SCREENS IN THREE! THE / UNDERGROUND IS FASTER! | 3がめんで 9がめんぶん! / ちかの ほうが はやい! |
| PLT-10 | M | weak | POP | K | HE'S WILTING! | しおれてる! |
| PLT-11 | S | flavour | POP | C | FULL BLOOM! CAREFUL, / ROCKMAN! | まんかいだ! / きを つけろ! |
| PLT-12 | S | flavour | POP | K | BOTH BARRIERS POPPED! | バリアが どっちも はじけた! |
| PLT.D1 | M | death | POP | C | SEE YOU LATER, ALLIGATOR! | ワニに たべられちゃった・・・ |
| PLT.D2 | M | death | POP | K | STUCK IN THE TAR! | タールに はまった! |
| PLT.D3 | M | death | POP | C | HE LET GO TOO EARLY. | てを はなすのが はやすぎた。 |
| PLT.D4 | M | death | POP | K | THE JUNGLE ALWAYS WINS THE / FIRST ROUND. | さいしょの ラウンドは / いつも ジャングルの かち。 |
| PLT.D5 | S | death | POP | C | WATCH THE EYES ON THOSE / CROCS! | ワニの めを よく みろ! |
| PLT.D6 | S | death | POP | K | THAT WASN'T A FLOOR, / ROCKMAN. | あれは ゆかじゃ なかったよ。 |

PLT-06 and PLT-08 lose round 1's "Harry" and "Game Boy" (R3.3); Tango is Capcom's own (Rockman World 5, 1994). PLT-01
is Could with the 20:00 clock (the 1982 jungle game gave its explorer 20 minutes, Appendix A, A-8.3). PLT.D1 is the
rhyme in EN; JP says what happened.

#### Blizzard: SUMMIT CLIMBER (`venues_b.md` §1.13)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| BLZ-01 | S | flavour | POP | K | SOLAR ENERGY... ON A / GLACIER? | ソーラーエネルギー・・・ / ひょうがの うえで? |
| BLZ-02 | S | flavour | POP | C | ICE IS SLIPPERY, ROCKMAN. / SCIENCE! | こおりは すべる。 / かがくだ! |
| BLZ-03 | S | flavour | POP | K | THE SHIP IS SHAKING THE / ICICLES LOOSE! | ふねの ゆれで / つららが おちてくる! |
| BLZ-04 | S | flavour | POP | C | THE MR. Y MARU. HE NAMED AN / ICEBREAKER AFTER HIMSELF. | Mr.Y まる。じぶんの なまえを / ふねに つけたのか。 |
| BLZ-05 | S | flavour | POP | C | USE YOUR HEAD! LITERALLY! | あたまを つかえ! もじどおり! |
| BLZ-06 | S | flavour | POP | K | HEY! IT FILLED THE HOLE BACK / IN! | ちょっと! / あなを うめちゃった! |
| BLZ-07 | M | secret | POP | K | DON'T HURT THE SEALS! / THEY'RE UNION WORKERS! | アザラシを いじめないで! / くみあいいん なんだから! |
| BLZ-08 | C | flavour | POP | C | A POLAR BEAR IN SUNGLASSES? | サングラスの シロクマ? |
| BLZ-09 | S | flavour | POP | K | HE'S SKIING! DOES HE EVEN / HAVE SKIS? | すべってる! / スキー もってたっけ? |
| BLZ-10 | M | secret | POP | K | THE CONDOR! JUMP FOR ITS / FEET! | コンドルだ! / あしに とびついて! |
| BLZ-11 | S | flavour | POP | C | NEXT STOP: THE CLOUDS! HOLD / ON, LAD! | つぎは くもの うえだ! / はなすなよ! |
| BLZ-12 | M | weak | POP | K | HE'S MELTING! SOLAR POWER / WON'T SAVE HIM NOW! | とけてる! / ソーラーでも まにあわない! |
| BLZ-13 | S | flavour | POP | C | A SNOWMAN, MID-MATCH! THE / JUDGES LOVE IT. | しあいちゅうに ゆきだるま! / しんさいんは だいよろこびだ。 |
| BLZ-14 | S | flavour | POP | K | IS HE... YODELLING? / AVALANCHE! | あれって ヨーデル? / なだれだ! |
| BLZ-15 | S | flavour | POP | C | YOU BROKE A SEAL. THE UNION / WILL HEAR ABOUT THIS. | アザラシを こわしたな。 / くみあいに ほうこくされるぞ。 |
| BLZ.D1 | M | death | POP | C | UP, LAD! IT'S ONLY MINUS / FORTY! | おきろ! たったの / マイナス40どだ! |
| BLZ.D2 | M | death | POP | C | IN MY COUNTRY WE CALL THIS / WEATHER "SPRING". | わたしの くにでは これを / 「はる」と いう。 |
| BLZ.D3 | M | death | POP | K | THE SEALS ARE CLAPPING. I / THINK THAT'S BAD. | アザラシが はくしゅしてる。 / よくない かんじ。 |
| BLZ.D4 | M | death | POP | K | HELMETS ARE FOR BONKING, NOT / FOR LANDING! | ヘルメットは ずつきよう。 / ちゃくちよう じゃない! |
| BLZ.D5 | S | death | POP | K | BRR! ROCKMAN'S TAKING A / COLD NAP. | ブルッ! ロックマン / おひるねちゅう。 |
| BLZ.D6 | S | death | POP | K | THE SEAL FOREMAN SAYS: / "WATCH YOUR STEP." | アザラシの おやかたいわく: / 「あしもとに ちゅうい」 |

BLZ-04 is reworded so that it is no Wily gag (R3.9; Act I's gag is S14). Round 1's line 4 repeated Plant's and line 6
named another company's climbers (R3.3); both are replaced. BLZ.D2 is this venue's one "in my country" joke (§1.2).

#### Flame: PERSIAN PALACE (`venues_b.md` §2.11)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| FLM-01 | S | flavour | POP | K | A PALACE ON AN OIL FIELD! / WHAT COULD GO WRONG? | ゆでんの うえに きゅうでん! / なにが おきるやら! |
| FLM-02 | M | secret | POP | C | SHOOT IT BEFORE IT DROPS! / LIT OIL STAYS LIT. | おとす まえに うて! / ついた ひは きえないぞ。 |
| FLM-03 | S | flavour | POP | K | A PRESSURE PLATE! LIKE THE / OLD COMPUTER GAMES! | スイッチの ゆか! / むかしの パソコンゲーム みたい! |
| FLM-04 | S | flavour | POP | C | THAT'S THE "LOOSE" IN / "LOOSE FLOOR". | だから 「くずれる ゆか」と / いうのだ。 |
| FLM-05 | S | flavour | POP | K | SLIDE! TIPTOE! DO SOMETHING! | スライディング! ぬきあし! / なんとか して! |
| FLM-06 | S | flavour | POP | C | TOO CLOSE! HE PARRIES / POINT-BLANK. BACK UP! | ちかすぎる! ちかい たまは / はじかれる。さがれ! |
| FLM-07 | S | flavour | POP | C | THE GALLERY'S ON FIRE. / EFFECTIVE. EXPENSIVE. | ギャラリーが もえてる。 / こうかてき。たかくつく。 |
| FLM-08 | S | flavour | POP | C | MR. Y SENT THE PALACE A / TAPESTRY OF HIMSELF. | Mr.Yが じぶんの タペストリーを / おくったらしい。 |
| FLM-09 | M | secret | POP | C | HE COPIES YOU. HOLD YOUR / FIRE, AND HE HOLDS HIS. | かれは まねを する。うたなければ / かれも うたない。 |
| FLM-10 | S | flavour | POP | K | THEY... MERGED? | ・・・ひとつに なった? |
| FLM-11 | S | flavour | POP | C | YOU BEAT YOURSELF. / PHILOSOPHICALLY TROUBLING. | じぶんに かった。 / てつがくてきに なやましい。 |
| FLM-12 | S | flavour | POP | K | A MOUSE! IT'S PRESSING THE / PLATE! GOOD MOUSE! | ネズミ! スイッチを ふんでる! / いいこ! |
| FLM-13 | S | flavour | POP | K | THE FIRE MARSHAL IS TUTTING / AT YOU. | しょうぼうかんが / したうち してる。 |
| FLM-14 | M | weak | POP | K | HIS FLAME WENT OUT! | ひが きえた! |
| FLM-15 | S | flavour | POP | C | YOU FED HIM? | えさを やったのか? |
| FLM-16 | S | flavour | POP | K | THE WHOLE FLOOR'S ON FIRE! | ゆかが ぜんぶ もえてる! |
| FLM.D1 | M | death | POP | C | THE PALACE HAS A STRICT / NO-RUNNING POLICY. | きゅうでんは / はしり きんしだ。 |
| FLM.D2 | M | death | POP | C | OIL AND FIRE. WHO COULD HAVE / PREDICTED THIS? | あぶらと ひ。 / だれが よそう できた ことか。 |
| FLM.D3 | M | death | POP | K | THE FLOOR FELL! IT SAID / "LOOSE" ON THE BROCHURE! | ゆかが おちた! パンフに / 「くずれる」って かいてたよ! |
| FLM.D4 | S | death | POP | C | THE HOURGLASS DOESN'T STOP / FOR RETRIES. | すなどけいは リトライでも / とまらない。 |
| FLM.D5 | S | death | POP | K | THE VIZIER IS LAUGHING. / ...HE HAS WILY'S LAUGH. | だいじんが わらってる。 / ・・・ワイリーの わらいかた。 |
| FLM.D6 | M | death | POP | K | THE OLD GAME GAVE YOU AN / HOUR. THIS ONE GIVES LIVES. | むかしの ゲームは 60ぷん。 / この ゲームは ざんき。 |

FLM-01 has no "Oil Sultanate" (R3.4); the jokes aim at the 1989 palace game's mechanics (plates, loose floors, the
hour limit, the shadow), never at a culture. FLM-06 is rewritten for the 48-px spacing parry (venues_b §2.11). FLM-09 is
the merge tell, worded for R3.9 (Shadow Rock is harmless while you have not fired). FLM.D5 needs the vizier (Should, an
obvious Wily-in-costume gag, R3.4). FLM.D6: that game's limit was 60 minutes (Appendix A, A-8.4).

#### Centaur: ATLANTIS RUINS (`venues_b.md` §3.13)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| CEN-01 | S | flavour | POP | K | ABILITY UNKNOWN! EVEN THE / JUDGES DON'T KNOW. | とくぎ ふめい! / しんさいんにも わからない。 |
| CEN-02 | S | flavour | POP | C | ZONE 1. ATLANTIS HAS OVER A / HUNDRED. | ゾーン1。アトランティスには / 100いじょう ある。 |
| CEN-03 | S | flavour | POP | C | DOORS IN ATLANTIS GO WHERE / THEY LIKE. | アトランティスの とびらは / すきな ところへ つながる。 |
| CEN-04 | S | flavour | POP | K | "A CRACKED DOOR LIES." / HELPFUL! | 「ひびの とびらは うそつき」 / たすかる! |
| CEN-05 | S | flavour | POP | K | BACK TO ZONE %N%?! THAT'S SO / MEAN! | ゾーン%N%に もどされた!? / ひどい! |
| CEN-06 | S | flavour | POP | K | IT'S A PAINTING! | えだった! |
| CEN-07 | M | secret | POP | C | CAN'T SEE? THEN LOOK FOR / WHAT SHINES. | みえないなら / ひかる ものを さがせ。 |
| CEN-08 | S | flavour | POP | K | THE STATUE SAID THANK YOU! | せきぞうが ありがとうって! |
| CEN-09 | S | flavour | POP | K | AN EGGPLANT! DON'T TOUCH IT! | ナスだ! さわらないで! |
| CEN-10 | S | flavour | POP | C | A HOT SPRING! EVEN ROBOTS / NEED A SOAK. | おんせんだ! / ロボットだって つかりたい。 |
| CEN-11 | S | flavour | POP | K | IT SAW YOU! RUN! | みつかった! にげて! |
| CEN-12 | S | flavour | POP | C | HIGH TIDE! YOU'LL JUMP LIKE / A FISH. | まんちょうだ! / さかなの ように とべるぞ。 |
| CEN-13 | S | flavour | POP | K | ZONE 100?! THAT'S THE WHOLE / GAME! | ゾーン100!? / ぜんクリア じゃん! |
| CEN-14 | S | flavour | POP | C | A JESTER WITH SNAKES. / BUDGET CUTS. | ヘビつきの ピエロ。 / よさん さくげんだ。 |
| CEN-15 | S | flavour | POP | C | WINGS! WELL, A DOG. CLOSE / ENOUGH. | つばさだ! まあ いぬだが。 / にたような ものだ。 |
| CEN-17 | M | weak | POP | K | HIS LEGS BUCKLED! | あしが くずれた! |
| CEN-18 | S | flavour | POP | C | HE'S POSING FOR THE PHOTO! / SAY CHEESE! | ポーズを とってる! / はい チーズ! |
| CEN-19 | S | flavour | POP | K | SO THAT'S HIS ABILITY... / GAMBLING? | それが のうりょく・・・ / ギャンブル? |
| CEN-20 | S | flavour | POP | C | C.FLRSH? THE ENGRAVER WAS / PAID BY THE LETTER. | C.FLRSH? / ちょうこくしの うっかりだ。 |
| CEN-21 | M | secret | POP | K | THAT STATUE... BLINKED? | あの せきぞう・・・ / まばたき した? |
| CEN-22 | S | flavour | POP | C | THE WATER'S LIFTING YOU! / RIDE IT UP! | みずが もちあげてる! / のって のぼれ! |
| CEN.D1 | M | death | POP | C | IN ATLANTIS, EVERY DOOR IS / THE WRONG DOOR. | アトランティスでは どの / とびらも まちがいだ。 |
| CEN.D2 | M | death | POP | C | CENTAUR MAN RUNS ON A DRY / BATTERY. YOU DON'T. | ケンタウロスマンは かんでんち。 / きみは ちがう。 |
| CEN.D3 | M | death | POP | K | TIME AND TIDE WAIT FOR NO / ROBOT. | さいげつ ロボットを またず。 |
| CEN.D4 | M | death | POP | C | ONLY NINETY-NINE ZONES TO / GO. | のこり たったの 99ゾーン。 |
| CEN.D5 | C | death | POP | K | A VEGETABLE HAS FALLEN. | やさいが たおれた。 |
| CEN.D6 | S | death | POP | K | THE CENTURIONS SALUTE YOU. / NOW GET UP! | ケンタウロスの へいしが / けいれい! さあ たって! |

CEN-02: the 1986 Atlantis game has 100 zones plus a secret final one (Appendix A, A-8.6), hence "over a hundred".
CEN-20: the YOU GET data spells `C.FLRSH`; the bold font draws it as "C.FLASH" (`rm6/text.md` §1). CEN.D5 needs the
eggplant curse (Could). Round 1's line 6 named a third-party hero (R3.3); CEN.D6 replaces it.

#### Yamato: EDO NINJA ROW (`venues_b.md` §4.12)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| YAM-01 | S | flavour | POP | C | DEFENCE 185 AND MOBILE 31. / HE ISN'T GOING ANYWHERE. | DEFENCE 185、MOBILE 31。 / どこにも いかない。 |
| YAM-02 | S | flavour | POP | K | WANTED: MR. Y, A MILLION / RYO. ...WHO PUT THAT UP? | てはいしょ: Mr.Y 100まんりょう。 / だれが はったの? |
| YAM-03 | S | flavour | POP | C | KNOCK THEM FROM BELOW! NINJA / MANNERS. | したから つきあげろ! / にんじゃの さほうだ。 |
| YAM-06 | S | flavour | POP | K | SHH! THE FLOOR SINGS WHEN / YOU WALK! | しーっ! / あるくと ゆかが なく! |
| YAM-07 | S | flavour | POP | C | EDO ARCHITECTURE: BEAUTIFUL / AND LETHAL. | えどの けんちく。 / うつくしく そして きけん。 |
| YAM-08 | S | flavour | POP | K | THE WALL TURNED AROUND! | かべが まわった! |
| YAM-09 | S | flavour | POP | K | IT'S JUST A SCROLL. | ただの かけじくだね。 |
| YAM-10 | M | secret | POP | K | DARUMA OTOSHI! KNOCK OUT THE / BLOCKS, NEVER THE HEAD! | だるまおとし! ブロックを ぬいて。 / あたまは だめ! |
| YAM-11 | S | flavour | POP | C | YOU HIT THE HEAD. THE DARUMA / IS NOT AMUSED. | あたまを たたいたな。 / だるまは ごりっぷくだ。 |
| YAM-12 | S | flavour | POP | K | IT PAINTED ITS OTHER EYE! / WISH GRANTED! | もう かたほうの めを いれた! / ねがいが かなった! |
| YAM-13 | S | flavour | POP | C | A POGO WITH A SPEAR? WE USED / TO CALL THAT A SAKUGARNE. | やりつきの ホッピング? / むかしは サクガーンと よんだ。 |
| YAM-15 | S | flavour | POP | K | WHO TURNED OFF THE LIGHTS?! | でんき けしたの だれ!? |
| YAM-16 | M | weak | POP | K | HE CHOPPED THE SPEAR IN / HALF! | やりを まっぷたつ! |
| YAM-17 | S | flavour | POP | C | A SAMURAI NEVER DROPS HIS / SPEAR. HE THROWS YOURS BACK. | さむらいは やりを おとさない。 / きみの やりを なげかえす。 |
| YAM-18 | S | flavour | POP | C | HIS HELMET FLEW OFF! MOBILE / 31... NOW 99! | かぶとが とんだ! / MOBILE 31が 99に! |
| YAM-19 | S | flavour | POP | crowd | YAMATO-YA! | やまとや! |
| YAM-21 | S | flavour | POP | C | IS THERE A DRAFT IN HERE? / THE LANTERN'S LEANING. | すきま かぜか? / ちょうちんの ひが ゆれている。 |
| YAM.D1 | M | death | POP | K | SHURIKEN! DUCK! ...HE DID / NOT DUCK. | しゅりけん! ふせて! / ・・・ふせなかった。 |
| YAM.D2 | S | death | POP | C | THE FLOOR SANG YOU A SAD / SONG, ROCKMAN. | ゆかが かなしい うたを / うたって いる。 |
| YAM.D3 | S | death | POP | K | THE CEILING CAME DOWN! / BEAUTIFUL AND LETHAL. | てんじょうが おちてきた! / うつくしく そして きけん。 |
| YAM.D4 | M | death | POP | C | DEFENCE 185, MOBILE 31, AND / STILL FASTER THAN YOU. | MOBILE 31でも / きみより はやい。 |
| YAM.D5 | M | death | POP | K | FALL SEVEN TIMES, STAND UP / EIGHT! | ななころび やおき! |
| YAM.D6 | M | death | POP | K | NINJA RULE 1: DON'T BE SEEN. / RULE 2: DON'T BE HIT. | にんじゃの おきて その1: / みつかるな。その2: あたるな。 |

YAM-02 is no longer a Wily gag (one per act, R4.4). YAM-04, -05, -14 and -20 are retired with the sekisho and the
plate line (venues_b §4.12). YAM-06, -07 and YAM.D2-D3 come back with the nightingale floor (Should). YAM-13: the
Sakugarne is Quint's pogo from Rockman World 2 (1991), Capcom's own. Panel labels (DEFENCE, MOBILE) stay in Latin in
JP, as on the card.

### 6.4 Hooks and deaths outside the venues; the generic table

`fortress.md` owns the triggers and tiers (§1.7, §2.7, §4.1-§4.6, §5.2-§5.4); story owns the words. Lines already
written in the scene sections are cited, not repeated. **Secret lines** (R4.5): each stage's **b0 showpiece has its
own line (Must)** and the tells fortress marks Must keep theirs. The **b1 hidden-room and b2 behaviour-prize lines are
Should**: in v1.0 §6.2's generic G.SR and G.SI play for them (R4.5's budget; fortress asked for all three as Must, §12).

**Opening** (fortress §1.7). OPN-01 is S03.1; OPN-02…05 are S07.1-S07.5; OPN-11 is in §6.2.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| OPN-06 | S | flavour | POP | K | IT'S ONLY KNEE-DEEP, / ROCKMAN! | ひざまでの ふかさだよ! |
| OPN-07 | S | flavour | POP | K | WHY IS THERE A MR. Y / COSTUME IN HERE? | なんで ここに Mr.Yの / いしょうが あるの? |
| OPN-08 | S | secret | POP | K | EIGHT HIGH FIVES! CROWD / FAVOURITE! | ハイタッチ 8かい! / かんきゃくの にんきもの! |
| OPN-09 | S | flavour | POP | K | UP TOP! | イエーイ! |
| OPN-10 | S | flavour | POP | C | ENTRANT TEN IS... MASKED. | 10ばんは・・・ かめん? |
| OPN-12 | S | secret | POP | C | PI-KUN'S DRESSING ROOM. THE / JUDGES SAW THAT. | ピーくんの がくや。 / しんさいんは みていたぞ。 |
| OPN-13 | M | secret | POP | K | FOUR TENS! A PERFECT / WARM-UP! | 10てんが 4つ! / パーフェクト ウォームアップ! |
| OPN.D1 | M | death | POP | K | IT'S ONLY A WARM-UP! | ただの ウォームアップだよ! |
| OPN.D2 | M | death | POP | C | HE GOT BOUNCED. | はねかえされたな。 |
| OPN.D3 | M | death | POP | C | CHARGE IT, LAD. CHARGE IT! | チャージだ。チャージ するんだ! |
| OPN.D4 | M | death | POP | K | POP GOES THE ENTRANT! | ポンッ! せんしゅが はじけた! |

**HALFTIME RIOT** (fortress §2.7). RIO-01 and RIO-06…09 are in S17-S19.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| RIO-02 | S | flavour | POP | K | HE'S CHEERING FOR THE WRONG / TEAM! | おうえんする あいてが / ちがうよ! |
| RIO-03 | M | scene | POP | K | BASS IS WRECKING THE TICKET / HALL! | フォルテが きっぷうりばを / こわしてる! |
| RIO-04 | M | secret | POP | C | A FULL-POWER AUDITION. / ACCEPTED! RULES ARE RULES. | フルパワーの オーディション。 / ごうかく! ルールは ルールだ。 |
| RIO-05 | M | secret | POP | K | LIGHTS! THE MAIN EVENT CAN / START! | ライトが ついた! / メインイベント かいし! |
| RIO.D1 | M | death | POP | K | REJECTED! | ふごうかく! |
| RIO.D2 | M | death | POP | C | THE CROWD DIDN'T SEE THAT. / THE LIGHTS WERE OFF. | かんきゃくには みえなかった。 / ていでん ちゅう だからな。 |
| RIO.D3 | M | death | POP | K | BASS IS COPYING HIS FALLS / NOW TOO! | フォルテ、ころびかたまで / コピーしてる! |
| RIO.D4 | M | death | POP | C | THAT'S A HALFTIME EXIT. | ハーフタイムで たいじょうか。 |

**H1 ROCKMAN** (fortress §4.1). H1-01 and H1-06 are in S28; H1-04 is S28.1; H1-05 is in §6.2.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H1-02 | S | flavour | POP | K | SCORE BALLS! THIS WING STILL / KEEPS SCORE! | スコアボール! この ウイングは / まだ スコアが あるんだ! |
| H1-03 | S | flavour | POP | C | MIND THE GAP. THE SIGN MEANS / IT. | すきまに ちゅうい。 / ほんきの かんばんだ。 |
| H1-07 | M | secret | POP | K | ALL 24 SCORE BALLS! THE / SCORE COUNTS AGAIN! | スコアボール 24こ ぜんぶ! / スコアが ふっかつ! |
| H1-08 | S | secret | POP | C | THE BOX ART STOREROOM. NONE / OF THEM LOOK LIKE YOU. | パッケージの そうこだ。 / ちっとも にて いないな。 |
| H1-09 | S | secret | POP | K | HE NEVER PUT HIMSELF BACK / TOGETHER! | もう がったい できない! |

**H3 ROCKMAN 3** (fortress §4.3). H3-03…05 and H3-08 are in S28; H3-06 is S28.5; H3-07 is in §6.2; H3-09 is the
`UPPERCUT!` label and S28.7.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H3-01 | S | flavour | POP | K | A RUSH COIL SIGN! THAT'S / WHERE RUSH STARTED. | ラッシュコイルの かんばん! / ラッシュは ここから。 |
| H3-02 | S | flavour | POP | K | A STATUE OF BREAK MAN! HE / WOULD HATE THAT. | ブレイクマンの ぞう! / ほんにんは いやがりそう。 |
| H3-10 | M | secret | POP | C | NOT A SCRATCH IN THE PRESS / HALL. TOP OF THE CLASS! | プレスの へやを むきずで! / クラスで いちばんだ! |
| H3-11 | S | secret | POP | K | DOC ROBOT'S WORKSHOP! UP A / STAIR OF MAGNET BEAMS! | ドクロボットの こうぼう! / マグネットビームの かいだん! |
| H3-12 | S | secret | POP | C | DING! THE PRACTICE BELL. / PERFECT FORM, LAD. | チーン! れんしゅうの ベル。 / みごとな フォームだ。 |

**H5 ROCKMAN 5** (fortress §4.5). H5-04…07 are in S28 and S30; H5-08 is in §6.2.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H5-01 | S | flavour | POP | K | STAR MAN'S SPACE! JUMP HIGH! | スターマンの うちゅう! / たかく とんで! |
| H5-02 | S | flavour | POP | C | CRYSTALS. THEY BOUNCE OFF / EVERYTHING. | クリスタルは なんでも / はねかえる。 |
| H5-03 | S | flavour | POP | K | RIDE THE ARROW! | やに のって! |
| H5-09 | M | secret | POP | K | ALL EIGHT LETTERS! THAT'S / HOW BEAT WAS BUILT! | もじが 8つ ぜんぶ! / ビートは こうして できたんだ! |
| H5-10 | S | secret | POP | C | THE 1993 WING. SOMEONE HAS / BEEN BUILDING THIS. | 1993ねんの ウイング。 / だれかが つくって いたな。 |
| H5-11 | S | secret | POP | K | WRONG NOTE! THE JUDGES HEARD / IT TOO! | おんちだ! しんさいんにも / きこえてたよ! |

H5-09 does not spell the letters; the plates themselves spell `ROCKMAN5` in both languages (R8.5; Appendix A, A-5.3),
so the line stays true whatever a player calls the game.

**W2 THE BRACKET OF DOOM** (fortress §5.2). W2-01 is S36.1; W2-02 the shouts (S36, Should); W2-03 and W2-05/06 are in
S36-S37.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| W2-04 | S | flavour | POP | C | A PAIR FINISHED. ONE MORE / LINE LIT! | ペア クリア。 / ラインが また ひとつ ついた! |
| W2-07 | M | secret | POP | K | EIGHT COPIES, EIGHT WAYS TO / WIN! A PERFECT BRACKET! | 8たいを 8とおりで! / パーフェクト トーナメント! |
| W2-08 | S | secret | POP | C | THE LOSERS' BRACKET. EVERY / TOURNAMENT HAS ONE. | はいしゃふっかつせん。 / どの たいかいにも ある。 |
| W2-09 | S | secret | POP | K | UNDEFEATED! NOT ONE FALL! | ぜんしょう! いちども / たおれなかった! |

**W3 PROJECT SUPER** (fortress §5.3-§5.4). W3-01…07 are in S38-S39.

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| W3-08 | M | secret | POP | C | OUT IN THREE TRIES! NO / INJURY TIME NEEDED. | 3かい いないに だっしゅつ! / ロスタイムは いらなかった。 |
| W3-09 | S | secret | POP | K | WILY'S TROPHY ROOM! IT'S ALL / STOLEN CUPS! | ワイリーの トロフィーべや! / ぜんぶ ぬすんだ カップ! |
| W3-10 | S | secret | POP | C | NO GIFT NEEDED. A PURIST'S / WIN. | おくりもの なしで かった。 / じゅんすいな しょうりだ。 |

**Exhibitions** (Could, R3.7; 2 deaths per guest; Maze Man is Won't):

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| E1.D1 | C | death | POP | K | WAIT, YOU STILL HAVE LIVES! | まって、まだ ざんきが ある! |
| E1.D2 | C | death | POP | C | TOO MANY GAPS. | すきまが おおすぎる。 |
| E2.D1 | C | death | POP | K | HE RETURNED YOU! | ロックマンを うちかえした! |
| E2.D2 | C | death | POP | C | SAME BALL, DIFFERENT ROBOT. | おなじ ボール、 / ちがう ロボット。 |
| E3.D1 | C | death | POP | K | THEY REACHED THE BOTTOM! | したまで きちゃった! |
| E3.D2 | C | death | POP | C | YOUR GRANDFATHER WOULD BE / DISAPPOINTED. | おじいちゃんが / がっかり するぞ。 |

**The generic table** (Should; by cause where it matches, else rotating):

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| G.DP1 | S | death | POP | K | MIND THE GAP! | すきまに ちゅうい! |
| G.DP2 | S | death | POP | C | THAT PIT HAD NO BOTTOM. MOST / DON'T. | そこなしの あなだ。 / たいてい そうだ。 |
| G.DP3 | S | death | POP | K | WHERE'S BEAT WHEN YOU NEED / HIM? | こんな とき ビートが / いれば! |
| G.DP4 | S | death | POP | C | GRAVITY: STILL UNDEFEATED. | じゅうりょく いまだ むはい。 |
| G.DS1 | S | death | POP | K | SPIKES! THE CLASSIC! | トゲ! おやくそく! |
| G.DS2 | S | death | POP | C | ONE TOUCH. ALWAYS ONE TOUCH. | さわれば おわり。いつもだ。 |
| G.DS3 | S | death | POP | K | THERE'S A CHIP FOR THAT, YOU / KNOW. | それよけの チップも あるよ。 |
| G.DS4 | S | death | POP | C | SPIKES. UNDEFEATED SINCE / 1987. | トゲは 1987ねんから むはい。 |
| G.DB1 | S | death | POP | K | SO CLOSE! LOOK AT HIS HEALTH / BAR! | おしい! / たいりょく ゲージを みて! |
| G.DB2 | S | death | POP | C | TRY HIS WEAKNESS. THE / FLASHING TELLS YOU. | じゃくてんを ためせ。 / てんめつが おしえて くれる。 |
| G.DB3 | S | death | POP | C | THE CHAMPION IS BREATHING / HARD TOO. | チャンピオンも / いきが あがって いるぞ。 |
| G.D01 | S | death | POP | K | OOH! THAT'S GOING TO COST / DAMAGE POINTS. | いたっ! / ダメージてんが へっちゃう。 |
| G.D02 | S | death | POP | C | DOWN GOES ROCKMAN! THE CROWD / GASPS. | ロックマン ダウン! / かんきゃくが いきを のむ。 |
| G.D03 | S | death | POP | K | SHAKE IT OFF! YOU'VE GOT / THIS! | きにしない! いけるよ! |
| G.D04 | S | death | POP | C | THE JUDGES HAVE NOTED IT. IN / LARGE LETTERS. | しんさいんが メモした。 / おおきな じで。 |
| G.D05 | S | death | POP | K | REPLAY! ...NO. LET'S NOT / SHOW THE REPLAY. | リプレイ! ・・・は / やめとこう。 |
| G.D06 | S | death | POP | C | EVERY CHAMPION FALLS. THE / GOOD ONES GET UP. | チャンピオンも たおれる。 / いい チャンピオンは たちあがる。 |
| G.D07 | S | death | POP | K | TIUN TIUN TIUN... | ティウン ティウン ティウン・・・ |
| G.D08 | S | death | POP | C | A SETBACK. STATISTICALLY, A / TEMPORARY ONE. | つまずいた。とうけいてきには / いちじてき。 |
| G.D09 | S | death | POP | C | ROCKMAN RETURNS TO THE START / LINE. WITH DIGNITY. | ロックマン スタートラインへ。 / ほこりたかく。 |
| G.D10 | S | death | POP | K | MR. Y JUST BOUGHT A SHIRT / THAT SAYS "I SAW THAT". | Mr.Yが 「みたぞ」って / Tシャツ かってる。 |
| G.D11 | S | death | POP | C | IN MY DAY WE HAD THREE LIVES / AND NO CONTINUES. | むかしは ざんき 3で / コンティニュー なしだった。 |

G.DS3 plays only while SPIKE GUARD is not owned; G.DP3 only while Beat is incomplete. G.D10 reads "WILY" after S33.
G.D07 is the death sound's own name: Japanese players call it "tiun tiun" (ティウンティウン), and 4MI heads its death
counter TIWNS (`r4mi/text.md` §0).

### 6.5 The heckles between lives (the CX Light 6 table)

CX's Dr. Light speaks once per respawn in the final fortress, from a 12-line table that includes a Yes/No where YES
kills you (`cx/SUMMARY.md` §2 item 20). GP gives the table to Mr. Y for every respawn in **H1-H5** (meta 14-18), then
to Wily for **W1-W3** (meta 19-21). It **replaces** the death line in those stages (`EV_RESPAWN_HECKLE`, P1;
consistency-25). **The YES/NO is Mr. Y's 1-bolt respawn insurance** (R4.3; `systems.md` §7: −1 bolt, never below 0):
CX's "a Yes that hurts", at a harmless size.

The index is the file's fortress KO count (the sum of meta 14-21's stage KOs), so the lines advance across stages and
sessions. v1.0 ships **Mr. Y's 6 and Wily's 4** (R4.5); after the last line the table loops from its second line (the
first is an introduction). The insurance offer waits for the answer (a T2 choice in the 4 × 28 window, the respawn
frozen behind it).

**H1-H5: Mr. Y** (polite わたくし … ございます; the Wahaha slip is the Act IV foreshadowing, not a Wily gag: nobody
says the name)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| HY.01 | M | heckle | POP | Y | HO HO HO! WELCOME TO MY... / TO A MUSEUM! | ホッホッホ! わたくしの・・・ いえ / はくぶつかんへ ようこそ! |
| HY.02 | M | heckle | POP | Y | EXHIBITS ARE NOT TO BE / TOUCHED. OR TO TOUCH YOU. | てんじひんには てを / ふれないで くださいませ。 |
| HY.03 | M | heckle | POP | Y | IN 1987 YOU COULDN'T EVEN / SLIDE. YOU'VE COME SO FAR. | 1987ねんは スライディング / できなかった のにねえ。 |
| HY.04 | M | heckle | WIN | Y | MR. Y'S RESPAWN INSURANCE! / ONLY 1 BOLT! / ▶YES NO | Mr.Yの ふっかつ ほけん! / たったの 1ボルト! / ▶はい いいえ |
| HY.04Y | M | heckle | WIN | Y | THANK YOU! YOUR POLICY DOES / NOT COVER FALLING OVER. / HO HO HO! | まいど! なお ころんだ ばあいは / ほしょうの たいしょうがいで / ございます。ホッホッホ! |
| HY.04N | M | heckle | WIN | Y | UNINSURED! HOW BRAVE! | むほけん! ゆうかん ですこと! |
| HY.05 | M | heckle | POP | Y | EVERY FALL IS RECORDED. FOR / SCIENCE! AND THE HIGHLIGHTS. | たおれる たびに ろくが します。 / かがくと ハイライトの ために! |
| HY.06 | M | heckle | POP | Y | WAHAHAHA... AHEM. HO. HO. / HO. | ワーッハッハッハ・・・ ゴホン。 / ホッ。ホッ。ホッ。 |
| HY.07 | S | heckle | POP | Y | THAT WILY FELLOW? NEVER MET / HIM. HANDSOME, I HEAR. | ワイリーという かた? ぞんじません。 / ハンサム だそうで。 |
| HY.08 | S | heckle | POP | Y | BASS NEVER FALLS THIS MUCH. / BASS IS PERFECT. IN BETA. | フォルテは たおれません。 / かんぺき。ベータばん ですが。 |
| HY.09 | C | heckle | POP | Y | HAVE YOU CONSIDERED Y-TURBO? / HAVE YOU CONSIDERED IT NOW? | Y-ターボは いかが? / いまなら いかが? |
| HY.09D | C | heckle | POP | Y | HOW IS YOUR Y-TURBO? READ / THE WARRANTY YET? | Y-ターボの ぐあいは? / ほしょうしょは およみに? |
| HY.10 | S | heckle | POP | Y | LIGHT'S ROBOT, FALLING OVER. / I WOULD PUT THAT IN A WING. | ライトの ロボットが ころんでる。 / それこそ てんじ したいですわ。 |
| HY.11 | S | heckle | POP | Y | IN MY DAY... IN MR. Y'S DAY, / ROBOTS STAYED DOWN! | わしの ころは・・・ いえ わたくしの / ころは、ロボットは おきなかった! |
| HY.11K | S | heckle | POP | K | HE SAID "MY DAY"... THEN HE / SAID "MR. Y'S DAY". | いま 「わし」って いった! |
| HY.12 | S | heckle | POP | Y | HAVE YOU HEARD OF SIXTEEN / BITS? YOU WILL. | 16ビットを ごぞんじ? / いずれ ごぞんじに なりますよ。 |
| HY.13 | S | heckle | POP | Y | KALINKA, DEAR, TELL ROCKMAN / HE IS DOING BADLY. | カリンカさま、ロックマンに / へただと おつたえください。 |
| HY.13K | S | heckle | POP | K | HE'S DOING GREAT! | すっごく じょうずだよ! |
| HY.14 | S | heckle | POP | Y | THE GIFT SHOP SELLS YOUR / HELMET NOW. HALF PRICE. | あなたの ヘルメット、 / おみやげやで はんがくです。 |
| HY.15 | S | heckle | POP | Y | AGAIN? I'M RUNNING OUT OF / THINGS TO SAY. ...KIDDING. | また? いうことが なくなって / きました。・・・うそです。 |
| HY.H1a | S | heckle | POP | Y | MY YELLOW DEVIL WAS THE / HARDEST BOSS OF 1987. | わたくしの イエローデビルは / 1987ねんで いちばん! |
| HY.H1b | S | heckle | POP | Y | SCORE: ZERO. HOW VERY 1987. | スコア ゼロ。 / じつに 1987ねんらしい。 |
| HY.H3a | S | heckle | POP | Y | MY GAMMA IS TWICE AS TALL / IN PERSON. | わたくしの ガンマは じつぶつ / だと 2ばいの おおきさ! |
| HY.H3b | S | heckle | POP | Y | DOC ROBOT IS ON A COFFEE / BREAK. | ドクロボットは / コーヒー ブレイク ちゅう。 |
| HY.H5a | S | heckle | POP | Y | MY DARK MAN IS A MASTER OF / DISGUISE. LIKE ME! | わたくしの ダークマンは / へんそうの めいじん。わたくしも! |
| HY.H5b | S | heckle | POP | Y | THAT CASTLE IN 1992? MINE / ALL ALONG! LIKE EVERYTHING! | 1992ねんの あの しろ? / ぜんぶ わたくしの もの! |

HY.01-HY.06 are v1.0's six. HY.04's three pages are one heckle (the offer and its two answers). Round 1's other YES/NO
("let's make a deal… I lied!") is withdrawn: R4.3 makes the insurance the one YES/NO. HY.H1a-HY.H5b are fortress's
wing-tagged drafts (Should), worded so Mr. Y never says "Blues" (R4.2). HY.11K is the JP-first joke: Kalinka catches
the わし (Wily's "I") slip.

**W1-W3: Dr. Wily** (after the unmasking; わし … じゃ)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| HW.01 | M | heckle | POP | W | WAHAHAHA! NO MORE MASKS! NO / MORE "HO HO HO"! | ワーッハッハッハ! もう かめんも / 「ホッホッホ」も いらんわ! |
| HW.02 | M | heckle | POP | W | FALL ALL YOU LIKE! EVERY / FALL FEEDS PROJECT SUPER! | いくらでも おちるが よい! / それも ぜんぶ データじゃ! |
| HW.03 | M | heckle | POP | W | LIGHT! ARE YOU WATCHING? / YOUR BOY IS LYING DOWN! | ライト! みておるか? / おまえの ロボット ねておるぞ! |
| HW.04 | M | heckle | POP | W | SHALL I LOWER THE / DIFFICULTY? NO! WAHAHA! | なんいどを さげて やろうか? / いやじゃ! ワハハ! |
| HW.05 | S | heckle | POP | W | IN SIXTEEN BITS, THAT PIT / WOULD HAVE A BOTTOM. MAYBE. | 16ビットなら あの あなにも / そこが あった かもな。 |
| HW.05D | C | heckle | POP | W | DID YOU THINK MY OWN CHIP / WOULD WORK AGAINST ME? | わしの チップが わしに / きくと おもったか? |
| HW.06 | S | heckle | POP | W | BASS! WRITE THIS DOWN! / "ROCKMAN: FALLS OVER." | フォルテ! メモ しておけ! / 「ロックマン: ころぶ」! |
| HW.07 | S | heckle | POP | W | I'VE LOST SIX TIMES, AND / LOOK AT ME NOW! | わしは 6かい まけた。 / だが みよ この とおり! |
| HW.07K | S | heckle | POP | K | TEN, WITH THE HANDHELD ONES! | けいたいきの ぶんも いれたら / 10かい だよ! |
| HW.08 | C | heckle | POP | W | EVERY CHANNEL OF THIS MUSIC / IS MINE! HEAR IT LAUGH! | この おんがくは ぜんぶ わしの / ものじゃ! わらって おるわ! |
| HW.09 | S | heckle | POP | W | MR. Y SAYS HELLO. ...I'M / MR. Y. I SAY HELLO. | Mr.Yが よろしくと。 / ・・・わしが Mr.Yじゃ。 |
| HW.10 | S | heckle | WIN | W | GIVE UP, AND YOU'LL BE THE / FIRST ROBOT I UPGRADE! FREE! / ▶YES NO | あきらめれば いちばんに / アップグレード して やるぞ! / ▶はい いいえ |
| HW.10Y | S | heckle | WIN | W | ...REALLY? I HADN'T PLANNED / FOR THAT. ER. CARRY ON! | ・・・ほんとうに? そこまでは / かんがえて なかった。 / ええい つづけろ! |
| HW.10N | S | heckle | WIN | W | FOOL! | ばかめ! |
| HW.11 | S | heckle | POP | W | YOUR BROTHER ISN'T COMING, / YOU KNOW. ...A WHISTLE? | おまえの あにきは こんぞ。 / ・・・いまのは くちぶえか? |
| HW.12 | S | heckle | POP | W | WAHAHAHA... COUGH... HAHA. | ワーッハッハッハ・・・ ゴホゴホ / ・・・ハッハ。 |
| HW.W3a | S | heckle | POP | W | YOU CAN'T HIT WHAT YOU CAN'T / SCALE! | スケールできない ものは / うてまい! |
| HW.W3b | S | heckle | POP | W | MY CAPSULE HAS AFTERIMAGES. / DOES YOURS? | わしの カプセルには ざんぞうが / ある。おまえのは? |

HW.01-HW.04 are v1.0's four. HW.07: by the end of 1993 Wily had lost in Rockman 1-6 and in Rockman World 1-4 on the
handheld (Appendix A, A-6.6); the line says "handheld", not the console's trademark (R3.3). HW.05D is the DOPED variant
(Could, with Y-TURBO; `systems.md` decides whether the chip is inert in the castle). HW.08 needs W1 (Could). HW.10 is
Wily's own offer, kept Should: the "Yes that hurts" here costs nothing. HW.11 needs the partner (Should); the WRONG NOTE
whistle is not the partner, so v1.0 never plays it.

### 6.6 Difficulty and mode variants

| Setting | What changes in the text | Tier |
|---|---|---|
| CASUAL | Death lines unchanged (they never mock). The first death of a CASUAL file adds G.CA (below) | Should |
| HARD | The first READY of a HARD file adds G.HD | Should |
| 1993 ruleset | No shop, no bolts, no chips (`systems.md` §13.3): Eddie's closed line (S10), no envelope, chip or insurance lines (the insurance offer is skipped). The commentators stay: they are flavour, not rules | Must (with the ruleset) |
| ANNOUNCER = DEATHS ONLY / OFF | §6.1 | Must |
| Time Attack, GP Rush | §6.1 (when built) | with meta |
| BASS file | S51; `%PLAYER%` (width 7) in generic lines | Won't (v1) |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| G.CA | S | flavour | POP | K | CASUAL MEANS HAVING FUN, / RIGHT, PAPA? | カジュアルって たのしむ / ことだよね パパ? |
| G.HD | S | flavour | POP | C | HARD MODE. WATCH, KALINKA. / THIS IS HOW LEGENDS START. | ハードモードだ。みて いなさい。 / でんせつは こうして はじまる。 |

**CASUAL levers (R2.9).** Story owns no stage, so it has no CASUAL lever list: the staging docs carry theirs (venues
§x.8, fortress §1.8 and kin). The only CASUAL text is G.CA. **Lag (R1.8)**: no story element occupies an object slot.
Pop-ups, plaques and windows are BG; the scene sprites (S03's tunnel crowd, S41's podium) are the staging docs' and
are counted there.

---

## 7. The judges' debrief: one hint per secret

`meta.md` §4 owns the engine (4MI's predicate table, per stage: the first missed secret, by weight, picks the line;
a requirement hint when only tool-gated secrets remain). This section is the final text of every entry, EN and JP,
spoken by **Kalinka** at the commentary desk (meta §4.1). Rules:

- **v1.0 ships tier B only** (R4.5; meta §4.1): the plain instruction, from the first miss. **Tier A riddles are
  Should** (v1.1): the escalation then runs riddle, riddle, instruction.
- **Tier B is the stage owner's own line** (the venue docs, `fortress.md` §0.4 tables), word for word except where a
  line had to fit 4 × 28; every entry here is pre-wrapped by `gen_p08.py` and checked by `fit.py`.
- **Tier A rewards knowing the homage game, and every fact in it is true** (Appendix A). Under R3.3 a riddle
  **describes** a third-party game ("the 1984 sequel", "a 1986 myth game") and never names it or its characters;
  round 1's Harry, Quickclaw, Erdrick, Scrooge, Goemon and Pit are gone. Capcom's own games may be named (1943).
- A riddle may be oblique. It may not point at the wrong place.

### 7.1 Venue hints · tier B Must, tier A Should

**Blizzard: SUMMIT CLIMBER** (venues_b §1.14)

| Secret | Ids |
|---|---|
| exit: the condor | BL0.B, BL0.A |
| room: the no-wrap floor | BL1.B, BL1.A |
| item: SNOW CHAINS | BL2.B, BL2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| BL0.B | M | hint | WIN | K | THE SUMMIT CONDOR ONLY / CARRIES CLIMBERS WHO REACH / IT WITH TIME ON THE CLOCK. / JUMP FOR ITS FEET. | ちょうじょうの コンドルは じかんが のこって いる / クライマーだけを はこぶ。 あしに とびつけ。 |
| BL1.B | M | hint | WIN | K | ON THE MOUNTAIN, ONE FLOOR / DOESN'T WRAP AROUND. WATCH / WHERE THE SEALS WALK. | やまの ゆかで ひとつだけ はしが つながって いない。 / アザラシの いく さきを みて。 |
| BL2.B | M | hint | WIN | K | THE SEALS ARE ONLY DOING / THEIR JOB. A CLIMBER WHO / NEVER BREAKS ONE EARNS A SET / OF CHAINS. | アザラシは しごとを してる だけ。 ひとつも / こわさなかった クライマーには チェーンが もらえる。 |
| BL0.A | S | hint | WIN | K | THE CONDOR NEVER WAITS FOR / SLOW CLIMBERS. RACE THE / BONUS CLOCK TO THE TOP. | コンドルは おそい クライマーを まって くれない。 / ボーナスの とけいと きょうそう して うえまで。 |
| BL1.A | S | hint | WIN | K | THE SEALS KNOW EVERY FLOOR / OF THAT MOUNTAIN. ONE OF / THEM NEVER COMES BACK. | アザラシは やまの ゆかを ぜんぶ しっている。 / もどって こない ゆかが ひとつ ある。 |
| BL2.A | S | hint | WIN | K | THE SEALS ARE UNION WORKERS. / THE UNION REMEMBERS WHO WAS / NICE TO THEM. | アザラシは くみあいいん。 くみあいは やさしく された / ことを わすれない。 |

**Wind: SKY ACE** (venues_a §1.5-§1.6)

| Secret | Ids |
|---|---|
| exit: the ace's elevator | WI0.B, WI0.A |
| room: WEATHER BALLOON | WI1.B, WI1.A |
| item: YASHICHI | WI2.B, WI2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| WI0.B | M | hint | WIN | K | FOUR RED SQUADRONS, FOUR / LAMPS. THE ELEVATOR ONLY / TAKES ACES. | あかい へんたいが 4つ、 ランプも 4つ。 / エレベーターは エースしか のせない。 |
| WI1.B | M | hint | WIN | K | A SEAGULL WAS STANDING ON A / CLOUD. CLOUDS AREN'T / FLOORS... ARE THEY? | カモメが くもの うえに たって いた。 くもは / ゆかじゃ ない・・・ よね? |
| WI2.B | M | hint | WIN | K | SHOOT THE POW. THEN KEEP / SHOOTING IT. | POWを うって。 そして うちつづけて。 |
| WI0.A | S | hint | WIN | K | IN 1943, WIPING OUT A RED / SQUADRON LEFT A POW. AN ACE / LEAVES NONE OF THEM FLYING. | 1943では あかい へんたいを ぜんめつ させると / POWが でた。 エースは 1きも にがさない。 |
| WI1.A | S | hint | WIN | K | SEAGULLS NEVER STAND ON / NOTHING. ASK ONE WHERE IT'S / STANDING. | カモメは なにも ない ところには とまらない。 どこに / とまって いるか みて。 |
| WI2.A | S | hint | WIN | K | CAPCOM'S OLDEST SECRET IS A / PINWHEEL. IT HIDES IN / SOMETHING YOU SHOOT. | カプコンで いちばん ふるい ひみつは かざぐるま。 / うつ ものの なかに かくれて いる。 |

**Plant: LOST JUNGLE** (venues_a §4.4-§4.8)

| Secret | Ids |
|---|---|
| exit: follow the cat | PL0.B, PL0.A |
| room: TREETOP HUT | PL1.B, PL1.A |
| item: AUTO RECOVER (the explorer's perfect) | PL2.B, PL2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| PL0.B | M | hint | WIN | K | THE CAT KNEW A WAY DOWN. / NEXT TIME, FOLLOW IT. | ねこは したへの みちを しっていた。 こんどは ついて / いって。 |
| PL1.B | M | hint | WIN | K | WHEN THE LIGHTNING STRUCK, A / LADDER APPEARED IN THE / TREES. | いなずまが ひかった とき、 きの うえに はしごが / みえた。 |
| PL2.B | M | hint | WIN | K | FOUR TREASURES, ZERO LOGS. / THE DIAMOND IS SHY. | たからは 4つ、 まるたは 0。 ダイヤは / はずかしがりや。 |
| PL0.A | S | hint | WIN | K | THE 1984 SEQUEL SENT ITS / EXPLORER AFTER A LOST PET. / HERE, THE PET KNOWS THE WAY. | 1984ねんの つづきでは たんけんかが ペットを / さがした。 ここでは ペットが みちを しっている。 |
| PL1.A | S | hint | WIN | K | THE STORM SHOWS MORE THAN / RAIN. WATCH THE TREES WHEN / THE SKY LIGHTS UP. | あらしが みせるのは あめ だけ じゃない。 そらが / ひかったら きを みて。 |
| PL2.A | S | hint | WIN | K | THE 1982 EXPLORER'S PERFECT / RUN NEVER LET A LOG TOUCH / HIM. NOT ONE. | 1982ねんの たんけんかの パーフェクトは まるたに / いちども ぶつからない こと。 |

**Flame: PERSIAN PALACE** (venues_b §2.12)

| Secret | Ids |
|---|---|
| exit: the shadow (the mirror glows, R3.9) | FL0.B, FL0.A |
| room: the mouse | FL1.B, FL1.A |
| item: FIREPROOF | FL2.B, FL2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| FL0.B | M | hint | WIN | K | YOUR SHADOW ONLY FIGHTS IF / YOU FIGHT. HOLD YOUR FIRE / UNTIL THE MIRROR GLOWS, THEN / WALK INTO IT. | かげは きみが たたかう ときだけ たたかう。 かがみが / ひかるまで うたずに かげへ あるいて いけ。 |
| FL1.B | M | hint | WIN | K | SOMETHING SMALL LIVES BEHIND / A GATE IN THE FIRE VAULT. / STAND STILL AND LISTEN. | ほのおの ちかしつの もんの おくに ちいさな なにかが / いる。 じっと して みみを すませて。 |
| FL2.B | M | hint | WIN | K | THE PALACE FIRE MARSHAL / REWARDS ENTRANTS WHO LEAVE / THE OIL UNLIT. SHOOT THE / FIRE-DROPPERS FIRST. | しょうぼうかんは あぶらに ひを つけなかった / せんしゅを ほめる。 ひを おとす てきを さきに / うて。 |
| FL0.A | S | hint | WIN | K | THE PRINCE NEVER BEAT HIS / SHADOW. HE DID SOMETHING / SMARTER WITH IT. | おうじは かげに かたなかった。 もっと かしこい / ことを した。 |
| FL1.A | S | hint | WIN | K | IN 1989 A MOUSE SAVED THE / PRINCE. MICE STILL LIVE IN / THAT PALACE. | 1989ねん ネズミが おうじを すくった。 その / きゅうでんには いまも ネズミが すんで いる。 |
| FL2.A | S | hint | WIN | K | THE FIRE MARSHAL HATES / BONFIRES. HE COUNTS EVERY / POOL YOU LIGHT. | しょうぼうかんは たきびが きらい。 きみが つけた / ひを ぜんぶ かぞえて いる。 |

**Yamato: EDO NINJA ROW** (venues_b §4.13)

| Secret | Ids |
|---|---|
| exit: the draft (the turning scroll; R3.2) | YA0.B, YA0.A |
| room: the gold crest | YA1.B, YA1.A |
| item: DARUMA | YA2.B, YA2.A |
| plate E (JET) | YA3.B, YA3.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| YA0.B | M | hint | WIN | K | IN THE LAST HALL OF SCROLLS, / WATCH THE LANTERN. ITS FLAME / POINTS AT THE SCROLL THAT / TURNS. | さいごの かけじくの ひろまで ちょうちんを みて。 / ひが かたむく さきの かけじくが まわる。 |
| YA1.B | M | hint | WIN | K | EDO'S GOLD IS UNDER THE / FLOOR. POGO ON THE CREST IN / THE CALTROP HALL. | えどの こばんは ゆかの した。 まきびしの ひろまの / もんしょうで ホッピング して。 |
| YA2.B | M | hint | WIN | K | KNOCK OUT EVERY BLOCK, NEVER / TOUCH THE HEAD, AND THE / DARUMA PAINTS ITS OTHER EYE. | ブロックを ぜんぶ ぬいて あたまに さわらなければ、 / だるまが もう かたほうの めを いれる。 |
| YA3.B | M | hint | WIN | K | BEAT'S E-PLATE SHINES ON THE / CASTLE ROOF. THE LADDER OVER / THE COURTYARD LEDGE NEEDS A / JET. | ビートの Eプレートは おしろの やねで ひかって / いる。 なかにわの はしごには ジェットが いる。 |
| YA0.A | S | hint | WIN | K | NINJA HOUSES HID THEIR DOORS / BEHIND SCROLLS. A HIDDEN / DOOR STILL LETS A DRAFT / THROUGH. | にんじゃやしきは かけじくの うらに とびらを / かくした。 かくし とびらからは かぜが はいる。 |
| YA1.A | S | hint | WIN | K | A 1989 CANE-POGO FOUND / TREASURE WHERE OTHERS SAW / ONLY FLOOR. | 1989ねんの ステッキ ホッピングは ただの ゆかに / たからを みつけた。 |
| YA2.A | S | hint | WIN | K | DARUMA OTOSHI: KNOCK OUT THE / BLOCKS, NOT THE HEAD. KEEP / HIS FACE ON. | だるまおとし。 たたくのは ブロック。 あたまは だめ。 / かおを おとさないで。 |
| YA3.A | S | hint | WIN | K | BEAT'S E-PART IS ON THE / CASTLE ROOF, WHERE ONLY / FLYING NINJAS GO. | ビートの Eパーツは おしろの やね。 とべる にんじゃ / しか いけない。 |

**Tomahawk: HIGH NOON FRONTIER** (venues_a §3.7)

| Secret | Ids |
|---|---|
| exit: the back way (+ plate B) | TO0.B, TO0.A |
| room: THE OUTHOUSE | TO1.B, TO1.A |
| item: SHERIFF STAR | TO2.B, TO2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| TO0.B | M | hint | WIN | K | THE SHERIFF ONLY OPENS THE / BACK WAY FOR A DEPUTY WITH / THREE BOUNTIES. | シェリフは しょうきんくびを 3にん とらえた / ほあんかんにだけ うらみちを ひらく。 |
| TO1.B | M | hint | WIN | K | SOMETHING IN TOWN WAS / RATTLING. OUT WEST, YOU / SHOOT WHAT LOOKS ODD. | まちで なにかが ガタガタ いって いた。 にしぶでは / あやしい ものは うつ。 |
| TO2.B | M | hint | WIN | K | THE SHERIFF SAW YOU SHOOT AT / TOWNSFOLK. READ THE SIGN BY / THE PIANO. | シェリフは きみが まちの ひとを うつのを みた。 / ピアノの そばの はりがみを よんで。 |
| TO0.A | S | hint | WIN | K | THREE FACES ON THE WANTED / POSTERS. THE SHERIFF KNOWS / WHO COLLECTS. | てはいしょに 3つの かお。 だれが しょうきんを / うけとるか シェリフは しっている。 |
| TO1.A | S | hint | WIN | K | "OCCUPIED," SAYS THE SIGN. / IT HAS SAID SO ALL DAY. / KNOCK LOUDER. | 「しようちゅう」と ふだに ある。 あさから ずっと。 / もっと つよく ノックして。 |
| TO2.A | S | hint | WIN | K | PLEASE DO NOT SHOOT THE / PIANIST. OR ANYONE ELSE WHO / ISN'T WANTED. | ピアニストを うたないで ください。 てはい されて / いない ひとも ぜんいん。 |

**Knight: HERO'S QUEST** (venues_a §2.5-§2.7)

| Secret | Ids |
|---|---|
| exit: the stairs behind the empty throne (+ plate A) | KN0.B, KN0.A |
| room: LIGHT'S TABLET | KN1.B, KN1.A |
| item: KAISHIN | KN2.B, KN2.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| KN0.B | M | hint | WIN | K | THE KNIGHTLORD'S THRONE IS / EMPTY. WHY? SEARCH WHERE NO / ONE SITS. | ナイトロードの ぎょくざは からっぽ。 なぜ? だれも / すわって いない ところを しらべよ。 |
| KN1.B | M | hint | WIN | K | SOMETHING GLITTERED ON THE / FLOOR OF THE HALL. THOU / DIDST NOT SEARCH. | ひろまの ゆかで なにかが ひかって いた。 なんじは / しらべなかった。 |
| KN2.B | M | hint | WIN | K | METAL ONES FLEE FAST. HIT / THEM OFTEN, NOT HARD. | メタルは すぐ にげる。 つよく より なんども / たたけ。 |
| KN0.A | S | hint | WIN | K | IN 1986 THE REAL LORD WAITED / BELOW HIS OWN EMPTY THRONE. / OLD HABITS... | 1986ねん ほんとうの まおうは からっぽの / ぎょくざの したで まって いた。 むかしの / くせは・・・ |
| KN1.A | S | hint | WIN | K | A HERO OF OLD LEFT A TABLET / FOR HIS HEIR. SOMEONE ELSE / LEFT ONE HERE. | むかしの ゆうしゃは しそんに せきばんを のこした。 / ここにも だれかが のこして いる。 |
| KN2.A | S | hint | WIN | K | METAL ONES ARE WORTH A / FORTUNE IN EXP. THEY KNOW / IT. THEY WON'T WAIT AROUND. | メタルは けいけんちの かたまり。 じぶんでも / しっている。 まっては くれない。 |

**Centaur: ATLANTIS RUINS** (venues_b §3.14)

| Secret | Ids |
|---|---|
| exit: ZONE 100 | CE0.B, CE0.A |
| room: ZONE 0 | CE1.B, CE1.A |
| item: CENTURION | CE2.B, CE2.A |
| plate T (JET) | CE3.B, CE3.A |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| CE0.B | M | hint | WIN | K | THE ZONE 100 DOOR IN ZONE 15 / ONLY OPENS AT THE LOWEST / TIDE. WAIT FOR THE WATER TO / DROP. | ゾーン15の 100の とびらは しおが いちばん / ひいた ときだけ ひらく。 みずが ひくのを まて。 |
| CE1.B | M | hint | WIN | K | IN THE BLACK ZONE ONE DOOR / ONLY SHINES IN THE DARK. / DON'T LIGHT THE ROOM. CLIMB / TO IT. | くらやみの ゾーンで ひとつの とびらは くらい / ときだけ ひかる。 あかりを つけずに のぼれ。 |
| CE2.B | M | hint | WIN | K | THREE STONE SOLDIERS IN THE / RUINS ARE NOT STATUES. A / FULL CHARGE WAKES THEM UP. | いせきの いしの へいし 3にんは せきぞう では / ない。 フルチャージで めを さます。 |
| CE3.B | M | hint | WIN | K | BEAT'S T-PLATE RESTS IN A / TEMPLE PAST THE PEGASUS GAP. / YOU NEED WINGS, OR A JET. | ビートの Tプレートは ペガサスの すきまの むこうの / しんでんに ある。 つばさか ジェットが いる。 |
| CE0.A | S | hint | WIN | K | ATLANTIS HID ITS LAST ZONES / BEST. HERE THE LAST ONE IS / MOSTLY UNDERWATER. | アトランティスは さいごの ゾーンほど よく かくした。 / ここでは さいごの ゾーンは みずの なか。 |
| CE1.A | S | hint | WIN | K | ZONE 0 IS ON NO MAP. IT ONLY / SHOWS UP WHEN THE LIGHTS GO / OUT. | ゾーン0は どの ちずにも ない。 あかりが きえた / ときだけ あらわれる。 |
| CE2.A | S | hint | WIN | K | IN A 1986 MYTH GAME, FREED / STONE SOLDIERS JOINED THE / BOSS FIGHT. THREE HERE ARE / WAITING. | 1986ねんの しんわの ゲームでは いしから とけた / へいしが ボスせんに きた。 ここにも 3にん / まっている。 |
| CE3.A | S | hint | WIN | K | PEGASUS CROSSED THAT GAP / WITH WINGS. YOU HAVE A DOG / WITH A JETPACK. | ペガサスは つばさで その すきまを こえた。 きみには / ジェットの いぬが いる。 |

Fact notes (Appendix A): WI0, 1943's POW rule; WI2, the Yashichi has been in Capcom games since 1984; PL0, the
1984 sequel's explorer searched for his niece, his pet and a diamond, and sources disagree on whether the pet is a cat
or a mountain lion, so the riddle says "pet"; PL2, the 1982 jungle game's perfect score needs every treasure and no
log hits; FL0-FL1, the 1989 palace game's prince merges with his shadow and is saved by a mouse; YA0, the turning
panels of Edo-period ninja houses (donden-gaeshi); YA1, DuckTales (Capcom, 1989), whose cane is a pogo; KN0, the 1986
quest's last lord sat below a throne with stairs behind it; KN2 drops round 1's "1000 EXP", which was not true of the
first metal monster; CE0, the 1986 Atlantis game's 100 zones plus a secret one; CE2, the 1986 myth game's freed stone
soldiers join its boss fights. YA0's tier A is new: round 1's riddle was about the sekisho, which is cut (R3.2).

### 7.2 Fortress stages · tier B Must (fortress §0.4's lines); no tier A

These stages have no homage riddle: their b0-b2 are GP's own inventions, so tier A is absent and the engine shows tier
B (meta §4.1). W3 has no judges' desk in v1.0 (meta §3.9), so its three lines are **Should** and wait for a desk.
H5's b3 (Mr. X's card) has no hint: T14's hint is Break Man's (S47).

**Opening-lite (meta 0)** (fortress §1.5)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| OP0.B | M | hint | WIN | K | GET A 10 FROM ALL FOUR LANE / JUDGES. THE LAST ONE WANTS / TO KNOW ABOUT THE ROOM / BEHIND THE LIMBO. | 4にんの しんぱん ぜんいんから 10てんを。 さいごの / ひとは リンボの うらの へやを しりたがってる。 |
| OP1.B | M | hint | WIN | K | SLIDE UNDER THE WALL AFTER / THE LAST LIMBO BAR. | さいごの リンボの バーの あと、 かべの したを / スライディング。 |
| OP2.B | M | hint | WIN | K | JUMP INTO EVERY CHAMPION'S / RAISED GLOVE DURING THE / PARADE. | パレードで チャンピオン みんなの あげた てに / ジャンプで タッチ。 |

**HALFTIME RIOT (meta 9)** (fortress §2.5)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| RI0.B | M | hint | WIN | K | ON THE SCOREBOARD SCAFFOLD, / JUMP FROM THE TOP OF A / LADDER TO THE BIG RED / BREAKER AND SHOOT IT. | スコアボードの あしばで はしごの うえから とんで、 / あかい ブレーカーを うって。 |
| RI1.B | M | hint | WIN | K | THE EMBLEM DOOR IN THE / TUNNEL OPENS FOR A FULLY / CHARGED SHOT. | トンネルの もんしょうの とびらは フルチャージで / ひらく。 |
| RI2.B | M | hint | WIN | K | KNOCK OUT 9 REJECTED / ENTRANTS WITH A FULL CHARGE / OR A FULL PUNCH. THEY WALK / AWAY HAPPY. | おちた せんしゅ 9にんを フルチャージか フルパンチで / たおして。 みんな よろこんで かえるよ。 |

**H1 ROCKMAN (meta 14)** (fortress §4.1)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H10.B | M | hint | WIN | K | COLLECT ALL 24 SCORE BALLS / ON THE MAIN ROUTE OF THE / 1987 WING. EVERY ENEMY THERE / DROPS ONE. | 1987ねんの ウイングの スコアボール 24こを / ぜんぶ。 てきは みんな 1こずつ おとすよ。 |
| H11.B | M | hint | WIN | K | IN THE ARCHIVE BRANCH, BURN / THE CHARRED CRATE WITH / F.BLAST. | しりょうしつの わきみちで こげた はこを / フレイムブラストで もやして。 |
| H12.B | M | hint | WIN | K | KNOCK DOWN AT LEAST ONE / FLYING PIECE EVERY CROSSING / WITH A FULL CHARGE OR A FULL / PUNCH. | とんでくる パーツを まいかい ひとつは フルチャージか / フルパンチで うちおとして。 |

**H3 ROCKMAN 3 (meta 16)** (fortress §4.3)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H30.B | M | hint | WIN | K | GET THROUGH NEEDLE MAN'S / PRESS HALL WITHOUT A / SCRATCH. SLIDE UNDER THE / YELLOW-STRIPED PRESSES. | ニードルマンの プレスの へやを むきずで。 きいろい / しまの プレスは スライディングで くぐって。 |
| H31.B | M | hint | WIN | K | AT THE FIRST CHECKPOINT, / BUILD TWO MAGNET BEAMS AS A / STAIR UP TO THE LIT WINDOW. | さいしょの チェックポイントで マグネットビームを / 2ほん かいだんに して あかるい まどへ。 |
| H32.B | M | hint | WIN | K | ON THE PRACTICE FIST BEFORE / GAMMA, RIDE TO THE TOP AND / RING THE BELL WITH A FULLY / CHARGED PUNCH. | ガンマの まえの れんしゅうの こぶしに のって / うえまで。 フルパンチで ベルを ならして。 |

**H5 ROCKMAN 5 (meta 18)** (fortress §4.5)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| H50.B | M | hint | WIN | K | FIND THE EIGHT LETTER PLATES / IN THE 1992 WING. THE / SHORTCUT HAS TWO. | 1992ねんの ウイングで もじの プレートを 8まい。 / ちかみちに 2まい あるよ。 |
| H51.B | M | hint | WIN | K | KNOCK SIX TIMES, FAST, ON / THE UNDER-CONSTRUCTION DOOR / BEFORE DARK MAN. | ダークマンの まえの こうじちゅうの とびらを はやく / 6かい ノックして。 |
| H52.B | M | hint | WIN | K | WHEN THE FAKE BREAK MAN / WHISTLES, HIT HIM WITH A / FULL CHARGE ON THE WRONG / NOTE. | にせ ブレイクマンが くちぶえを ふいたら、 はずれた / おとに あわせて フルチャージ! |

**W2 THE BRACKET OF DOOM (meta 20)** (fortress §5.2)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| W20.B | M | hint | WIN | K | FINISH EACH OF THE EIGHT / COPIES WITH A DIFFERENT / WEAPON. THE BOARD SHOWS / WHICH YOU USED. | 8たいの コピーを ぜんぶ ちがう ぶきで しとめて。 / ボードに つかった ぶきが でるよ。 |
| W21.B | M | hint | WIN | K | THE SEALED ALCOVE UNDER THE / ?? ON THE BRACKET BOARD / OPENS FOR A FULLY CHARGED / SHOT. | ボードの ?? の したの とじた へやは / フルチャージで ひらく。 |
| W22.B | M | hint | WIN | K | CLEAR ALL FOUR BOUTS AND THE / FINAL WITHOUT DYING. | 4つの しあいと けっしょうを いちども たおれずに。 |

**W3 PROJECT SUPER (meta 21; no desk in v1.0)** (fortress §5.3-§5.4)

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| W30.B | S | hint | WIN | K | ESCAPE THE CASTLE IN YOUR / FIRST THREE ATTEMPTS. | 3かい いないに しろから だっしゅつ して。 |
| W31.B | S | hint | WIN | K | AT THE BARRED WINDOW NEAR / THE START, THROW THE SUPER / FIST PAST THE KEYHOLE. IT / HITS ON THE WAY BACK. | スタートちかくの てつごうしの まどで スーパーの / こぶしを かぎあなの むこうへ。 もどりで あたる。 |
| W32.B | S | hint | WIN | K | BEAT THE WILY CAPSULE / WITHOUT FALLING BELOW 6 HP, / SO BREAK MAN NEVER STEPS IN. | HPを 6より へらさずに ワイリーカプセルを / たおして。 ブレイクマンの でばんは なし。 |

H50 does not spell the plates' letters (§6.4, H5-09; Appendix A, A-5.3). RI0, RI1, W21: "fully charged" is the
v1.0 key for the partner's doors (R4.2).

### 7.3 Generic debrief lines (meta §4.5's ids)

Requirement hints play when only tool-gated secrets remain; scorecard hints (G) when every secret is found but a
medal is not, chosen by the weakest row; perfect lines when nothing is left. **v1.0's predicate table uses only R2**
(the E and T plates: `meta.md` §4.3, where no venue exit, room or item needs an adaptor and the fortress stages'
`require` values are none), so **R1, R3 and R5 are Should** (round 3; meta §4.5 follows), written now for the stages
that will need them (H4's SUPER-gated prize and kin).

| Id | Tier | When |
|---|---|---|
| R1 | S | POWER missing (no v1.0 predicate) |
| R2 | M | JET missing (Yamato E, Centaur T) |
| R3 | S | SUPER missing (H4's prize, Should) |
| R4 | S | the partner missing (Should) |
| R5 | S | a weapon missing (no v1.0 predicate) |
| G-TIME | M | weakest row TIME |
| G-DAMAGE | M | weakest row DAMAGE |
| G-VARIETY | M | weakest row VARIETY |
| G-SECRETS | M | weakest row SECRETS |
| G-STYLE | M | weakest row STYLE |
| P1 | M | perfect stage |
| P2 | S | perfect, rotation |
| P3 | S | perfect, rotation |
| P4 | S | perfect, rotation |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| DB.R1 | S | hint | WIN | K | THIS STAGE NEEDS MORE PUNCH. / COME BACK AFTER YOUR 2ND / WIN! | ここは パンチりょくが たりない。 2しょうめの あとに / また きてね! |
| DB.R2 | M | hint | WIN | K | THERE'S A ROUTE HERE FOR / ENTRANTS WHO FLY. COME BACK / AFTER YOUR 4TH WIN. | ここには とぶ せんしゅ むけの みちが ある。 / 4しょうめの あとに また きてね。 |
| DB.R3 | S | hint | WIN | K | A NEW ADAPTOR IS HIDDEN IN / THE HALL OF FAME. SOMETHING / HERE IS WAITING FOR IT. | ホール・オブ・フェイムに あたらしい アダプターが / かくれてる。 ここで なにかが それを まってる。 |
| DB.R4 | S | hint | WIN | K | SOME PLACES NEED TWO. YOU'LL / HAVE A TAG PARTNER SOON. A / MASKED ONE. | ふたりなら いける ばしょが ある。 もうすぐ / タッグパートナーが できるよ。 かめんの ひとが。 |
| DB.R5 | S | hint | WIN | K | THE JUDGES THINK ANOTHER / CHAMPION'S WEAPON IS THE KEY / HERE. %WEAPON%, MAYBE? | しんさいんの みたてでは べつの チャンピオンの ぶきが / かぎ。 %WEAPON% かも? |
| DB.G-TIME | M | hint | WIN | K | TOO SLOW FOR THE JUDGES! PAR / HERE IS %PAR%. YOU TOOK / %TIME%. | しんさいんには おそすぎ! ここの パーは / %PAR%。 きみは %TIME%。 |
| DB.G-DAMAGE | M | hint | WIN | K | THE JUDGES COUNT EVERY HIT / YOU TAKE. FEWER HITS, BIGGER / PRIZE. | しんさいんは ダメージを ぜんぶ かぞえてる。 へらせば / しょうきん アップ。 |
| DB.G-VARIETY | M | hint | WIN | K | THE JUDGES LOVE VARIETY! WIN / WITH LOTS OF WEAPONS AND / FORMS FOR THE BIGGEST PRIZE. | しんさいんは バラエティが だいすき! いろんな ぶきと / フォームで たおすと いちばん もうかる。 |
| DB.G-SECRETS | M | hint | WIN | K | THERE'S STILL A SECRET HERE. / FIND ONE, AND I'LL TELL YOU / ABOUT THE NEXT. | ここには まだ ひみつが ある。 ひとつ みつけたら / つぎを おしえて あげる。 |
| DB.G-STYLE | M | hint | WIN | K | FINISH CHAMPIONS WITH THEIR / WEAKNESS, AND KEEP THE / E-TANK IN YOUR POCKET. | チャンピオンには じゃくてんで とどめを。 Eかんは / ポケットに しまって おいて。 |
| DB.P1 | M | hint | WIN | K | PERFECT! PAPA IS CRYING. HE / SAYS IT'S THE STADIUM / LIGHTS. | パーフェクト! パパが ないてる。 スタジアムの / ライトの せい だって。 |
| DB.P2 | S | hint | WIN | K | NOTHING LEFT TO FIND! THE / JUDGES HAVE RUN OUT OF / HINTS. | もう さがす ものは ない! しんさいんも ヒントが / きれちゃった。 |
| DB.P3 | S | hint | WIN | K | EVEN MR. Y'S JUDGE GAVE YOU / A 10! HE TOOK IT BACK, BUT / WE ALL SAW IT. | Mr.Yの しんさいんまで 10てんを あげた! すぐ / ひっこめた けど みんな みたよ。 |
| DB.P4 | S | hint | WIN | K | THIS STAGE IS 100% CLEAR. / YOU CAN STOP NOW. ...NO? / THEN I'LL KEEP WATCHING. | この かいじょうは 100% クリア。 もう やめて / いいよ。 ・・・やめない? じゃあ また みてる。 |

G-STYLE matches `systems.md` §6.5's WEAK FINISH (4 points) and NO TANKS (2 points). P3 reads "WILY'S JUDGE" after S33
(a variant flag, not a new string). The ENGRISH perfect line (meta §4.5) is §9's.

---

## 8. Chip help pages

`systems.md` §9.2 owns the chips and their exact effects; this section owns every word of their help pages: a **4 × 28
window** (R1.4; round 1 had 3 lines), opened with B on the CHIPS page. The catalogue voice is Eddie's shop. **◊ marks a
page that is cryptic on purpose** (4MI's help pages, whose readme warned that some hide functions, `r4mi/text.md` §2);
its meaning is given for the designers and never ships. **v1.0's 14 pages are Must** (R4.5); the Could bundle's four
come back with it; the three cut chips' pages are kept as Won't notes.

- **YASHICHI and DARUMA cannot be equipped together, and both pages say so** (`systems.md` §9.1, R2.6).
- **DARUMA has no hidden function**: round 1's proposal (twice per life after the 7th KO) is rejected (consistency
  decision 33), so its page uses the fallback last line and states the rule plainly.
- Round 1's Y-TURBO proposal (inert in Super Wily Castle) stays a proposal for `systems.md` with the Could bundle;
  HW.05D (§6.5) is its line.

| Bit | Chip | Tier | ◊ and what it hides |
|---|---|---|---|
| 0 | ENERGY BALANCER | M | — |
| 1 | SHOCK ABSORBER | M | — |
| 2 | SPIKE GUARD | M | — |
| 3 | CHARGE KIT | M | — |
| 4 | EXCHANGER | M | — |
| 5 | ENERGY SAVER | M | — |
| 6 | YASHICHI | M | ◊ once per stage, at HP ≤ 4, a full refill |
| 7 | KAISHIN | M | — |
| 8 | SHERIFF STAR | M | — |
| 9 | AUTO RECOVER | M | ◊ 60 f without input, then +1 HP every 30 f; off during a boss fight |
| 10 | SNOW CHAINS | M | — |
| 11 | FIREPROOF | M | — |
| 12 | CENTURION | M | — |
| 13 | DARUMA | M | — |
| 14 | IRON HELMET | C | ◊ halves a hit on 1 frame in 8, and always at HP ≤ 4 ("late" = low HP) |
| 15 | THERMOS | C | — |
| 16 | BIRD SEED | C | ◊ the pit rescue costs 2 HP instead of 4 and works from HP ≥ 3 |
| 17 | Y-TURBO | C | ◊ the warranty: systems decides whether it is inert in Super Wily Castle |
| - | AFTERIMAGE | W | — |
| - | GLIDER | W | ◊ hold A with an empty Jet tank to glide |
| - | JET TUNER | W | — |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| HLP.ENERGY_BALANCER | M | help | WIN | E | SPARE WEAPON ENERGY GOES TO / THE EMPTIEST WEAPON YOU OWN. / THE 1993 ORIGINAL. ACCEPT NO / COPIES. | あまった エネルギーは いちばん へった ぶきへ。 / 1993ねんの げんてんモデル。 にせものに / ごちゅうい。 |
| HLP.SHOCK_ABSORBER | M | help | WIN | E | NO MORE FLINCHING. YOU STILL / BLINK. YOU JUST BLINK / STANDING UP, AND NOT FOR AS / LONG. | もう のけぞらない。 てんめつは する。 たった まま / すこし みじかく てんめつ する。 |
| HLP.SPIKE_GUARD | M | help | WIN | E | ONCE PER LIFE, SPIKES LEAVE / YOU AT 1 HP INSTEAD. THE / SECOND SPIKE IS STILL A / SPIKE. | 1いのちに 1かい トゲに ふれても HP1で たえる。 / 2ほんめの トゲは トゲ。 |
| HLP.CHARGE_KIT | M | help | WIN | E | CHARGES FASTER, PUNCHES TOO. / THE JUDGES CALL IT / "EFFICIENT". THIS TIME THEY / MEAN IT NICELY. | チャージも パンチも はやくなる。 しんさいんいわく / 「こうりつてき」。 こんどは ほめことば。 |
| HLP.EXCHANGER | M | help | WIN | E | LIFE YOU CAN'T USE BECOMES / ENERGY YOU CAN. TWO FOR ONE. / EDDIE'S MATH. | つかえない ライフを つかえる エネルギーに。 / 2たい1。 エディけいさん。 |
| HLP.ENERGY_SAVER | M | help | WIN | E | EVERY WEAPON SIPS INSTEAD OF / GULPING. TAKES TWO SLOTS. / WORTH IT? DISCUSS. | どの ぶきも ちびちび のむ。 スロットを 2つ / つかう。 その かちは? ぎろん しよう。 |
| HLP.YASHICHI | M | help | WIN | E | IT SPINS WHEN YOU NEED IT / MOST. ONCE. THEN IT RESTS / UNTIL THE NEXT STAGE. NOT / WITH DARUMA. | いちばん ひつような ときに まわる。 1どだけ。 / つぎの ステージまで やすむ。 ダルマとは いっしょに / つけられない。 |
| HLP.KAISHIN | M | help | WIN | E | A SPLENDID STRIKE! EVERY / 12TH HIT ON A BOSS LANDS / HARDER. COUNT ALONG AT HOME. | みごとな いちげき! ボスへの 12はつめごとに / いちげきが おもくなる。 いっしょに かぞえよう。 |
| HLP.SHERIFF_STAR | M | help | WIN | E | DEPUTIES GET PAID BETTER: / 20% MORE PRIZE MONEY. THAT / IS THE WHOLE POINT OF BEING / A DEPUTY. | ほあんかんは きゅうりょうが いい。 しょうきん 20% / アップ。 ほあんかんに なる りゆうは それだけ。 |
| HLP.AUTO_RECOVER | M | help | WIN | E | STAND STILL AND LISTEN. / SOMETHING IS GROWING BACK. / THE JUNGLE IS PATIENT. / CHAMPIONS ARE NOT. | じっと して みみを すませて。 なにかが はえて / くる。 ジャングルは きが ながい。 チャンピオンは / みじかい。 |
| HLP.SNOW_CHAINS | M | help | WIN | E | ICE HOLDS STILL UNDER YOUR / BOOTS. ICICLES BOUNCE OFF. / THE SEALS TAUGHT YOU THIS. | こおりでも すべらない。 つららも はねかえす。 / アザラシたちに おそわった。 |
| HLP.FIREPROOF | M | help | WIN | E | FIRE HURTS. FIRE NO LONGER / ENDS THE MATCH. THE FIRE / MARSHAL APPROVES. | ひは いたい。 でも ひで しあいは おわらない。 / しょうぼうかんも にっこり。 |
| HLP.CENTURION | M | help | WIN | E | A FRIEND FROM THE RUINS / WAITS AT EVERY TITLE FIGHT. / HE STOPS THREE SHOTS FOR / YOU. | いせきの ともだちが ボスせんで まって いる。 たまを / 3はつ とめて くれる。 |
| HLP.DARUMA | M | help | WIN | E | FALL SEVEN TIMES, STAND UP / EIGHT. WELL: ONCE PER LIFE, / NOT ON PITS OR SPIKES. TWO / SLOTS. NOT WITH YASHICHI. | ななころび やおき。 まあ 1いのちに 1かい。 あなと / トゲは だめ。 スロット 2つ。 ヤシチとは いっしょに / つけられない。 |
| HLP.IRON_HELMET | C | help | WIN | E | HAMMERED FROM A SWORD AND A / SHIELD. SOME BLOWS FORGET / THEMSELVES. LATE, ALWAYS. | かたなと たてから きたえた。 ときどき いちげきが / じぶんを わすれる。 よわれば かならず。 |
| HLP.THERMOS | C | help | WIN | E | KEEPS TANKS HOT AND WEAPONS / COLD. OR THE OTHER WAY / ROUND. DRINK UP. | タンクは あつく ぶきは つめたく。 はんたい かも。 / ぐいっと どうぞ。 |
| HLP.BIRD_SEED | C | help | WIN | E | BEAT SAYS THANK YOU. BEAT / SAYS IT WITH LESS PECKING. | ビートが ありがとう って。 つつくのは すくなめに / して くれる そうです。 |
| HLP.Y_TURBO | C | help | WIN | E | MR. Y GUARANTEES RESULTS. / MR. Y GUARANTEES A LOT OF / THINGS. SEE WARRANTY. | Mr.Yは けっかを ほしょう いたします。 いろいろ / ほしょう いたします。 ほしょうしょ さんしょう。 |
| HLP.AFTERIMAGE | W | help | WIN | E | AFTER A HIT YOU STAY A BLUR / A LITTLE LONGER. ENEMIES / HATE THAT. | ダメージの あと すこし ながく ぶれて いられる。 / てきは それが きらい。 |
| HLP.GLIDER | W | help | WIN | E | WIND AND FEATHERS. WHEN THE / TANK IS DRY, KEEP HOLDING / ON. | かぜと はね。 タンクが からに なっても にぎった / ままで。 |
| HLP.JET_TUNER | W | help | WIN | E | BIGGER TANK, SAME RUSH. DO / NOT TELL HIM ABOUT THE EXTRA / WEIGHT. | タンクは おおきく ラッシュは そのまま。 おもくなった / ことは ないしょ。 |

Facts: the Energy Balancer is vanilla Rockman 6's own passive item (`rm6/SUMMARY.md` §1.3); the Yashichi was Capcom's
full-restore item; "fall seven times, stand up eight" is the daruma's proverb; IRON HELMET credits 4MI's METALL'S
HELMET (systems §9.4).

---

## 9. ENGRISH · Could (R0.3 item 12; meta §12)

`meta.md` §12 owns the mechanism (a sparse override table, EN fallback, the letter O for zero in numbers); this is the
final list. **Rules:** menus only (never story, hints or help pages; the one exception is meta's ENGRISH perfect line, a
deliberate 4MI tribute); affectionate, never mocking; the classics nodded to in new words, never quoted verbatim
(R8.4); every string legal in its
surface's font (§10.1: the pause font has no D, O, Q or Z, so ENGRISH there spells around them too). All rows are
labels (LBL, EN only by definition) and **Could**.

| Surface | ENGLISH | ENGRISH | Note |
|---|---|---|---|
| Title | GAME START | GAME STARTING | |
| Title | CONFIG | CONFIGULATION | |
| CONFIG, language row | ENGRISH | ENGRISH (ENGLISH IS COME!!) | 4MI's "ENGLISH COMING SOON", answered |
| File select | NEW ENTRANT | NEW CHALLENGER IS HERE | |
| File select | ERASE / COPY | ERASE IT!! / COPY IT | |
| File select | BROKEN DATA | DATA IS BROKEN. SORRY | |
| Saving icon | SAVING | NOW SAVING... | the "NOW LOADING" family |
| Difficulty | CASUAL / HARD | CASUALLY / VERY HARD | |
| Bracket | PUSH START | PUSH START BUTTON | |
| Bracket | HALFTIME RIOT | HALF TIME LIOT | R4.3's name; stage-select font: letters, `.` and `-` only |
| Bracket | 4 TO GO | 4 MORE TO GOING | |
| YOU GET | YOU GET | YOU GOT A | |
| Pause, weapons | C.FLASH | C.FLRSH | vanilla's own misspelling (`rm6/text.md` §1) |
| Pause | RETIRE | GIVE UP | pause-font legal |
| Scorecard | MEDAL / PLATINUM / BOLTS | METAL / PLATINAM / BORTS | |
| Scorecard | NO IMPROVEMENT / NEW RECORD!! | NOT IMPROVE. SAD / NEW RECORDS!! | |
| Shop | WELCOME! | ALL YOUR BOLTS ARE BELONG TO EDDIE | a 1989 shooter's famous line, as Europe saw it in 1991 |
| Pit stop | SAVE & QUIT | SAVE AND GOODBYE | |
| Game over | GAME OVER / CONTINUE | GAME IS OVER / CONTINUE? YOU CAN | |
| GP Rush (Could) | ELIMINATED / CHAMPION | YOU ARE ELIMINATE / A CHAMPION IS YOU | a 1986 wrestling game's victory screen, in new words |
| Records | KNOCKOUTS / TOTAL | TIWNS / TOTALLY | 4MI's heading (meta §9.4) |
| Rating, header | CHAMPIONSHIP RATING | CONGLATULATE !!! | a 1988 ghost-catching game's ending screen, in new words |
| Rating | GRAND CHAMPION / PARTICIPANT | GRAND CHAMPIOM / THANK YOU FOR PARTICIPATE | |
| Credits | TRANSLATION: (name) | TRANSLATION: (RESERVED) | 4MI's credit |

The classics are nodded to, never quoted (R8.4): the originals ("ALL YOUR BASE ARE BELONG TO US", "A WINNER IS YOU",
"CONGLATURATION !!!", Appendix A, A-8.14) keep their rhythm in new words: ALL YOUR BOLTS…, A CHAMPION IS YOU,
CONGLATULATE !!!. The notes describe the games (R3.3); no string names one. Round 1's SEMIFINAL row became HALFTIME
RIOT (R4.3); the 1993 difficulty row is gone with
1993 RULES (Could, meta). Digits print with O for zero (`1OO`), the mirror of vanilla's pause font, which writes O
with a zero.

---

## 10. Text engines, fonts and bilingual output

### 10.1 Every text surface, its engine and its font (from `rm6/text.md`; tech §11)

Vanilla's fonts differ per screen: the same byte is a different letter on different screens (`rm6/text.md` §1, §6).
GP keeps the vanilla surfaces with their fonts (and their quirks) and puts every sentence it adds in **one new engine**
(tech §11: R1.4's fixed-cell glyph cache). The rule that keeps this simple, taken from vanilla itself:

> **Labels stay English in both languages; sentences are translated.** Vanilla's JP game shows GAME START, PASS WORD,
> STAGE SELECT, CONTINUE, the pause labels, the boss panel and YOU GET in English (`rm6/text.md` §5). GP does the
> same for every menu label (the `LBL` rows), and translates only sentences: dialogue, commentary, hints, help pages,
> plaques, descriptions.

| Surface (this doc's code) | Engine | Font | Glyphs available | Limits | Language |
|---|---|---|---|---|---|
| Boot and license (PPU) | PPU script `$1F` | main `$0B` | `0-9 A-Z . ー ゜ ? ! 「 」 ' : ,` `・ © 。`, 46 hiragana, 16 katakana | no `-`: S01 uses `ー` or adds one tile | EN in both |
| Health notice, difficulty and CONFIG descriptions (WIN) | new engine | glyph cache | full (§10.2) | 4 × 28 | translated |
| Title, CONFIG, file select (LBL) | meta / art_audio's menu font | GP menu font | caps, digits, `. - : ! ? ' / ( )` | labels only | EN in both |
| Bracket node labels (LBL) | PPU (stage-select font) | stage select `$2B` | **`0-9 A-Z . -` and blank only** | the bracket shows **champion names**, not venue names (meta §3.2: HERO'S QUEST has an apostrophe) | EN in both |
| Bracket, pit stop, scene windows (WIN) | new engine | glyph cache | full | 4 × 28 | translated |
| Boss panel (PNL) | `$3C:$81B1` | panel bold set | `0-9 A-Z .` + GP's `- ? ! ' β` (§5.1) | field widths §5.1 | **English in both** (vanilla quirk) |
| YOU GET (PPU) | PPU `$60+` | YOU GET bold set | `0-9 A-Z .`, `-` = `$B8`; R and A look alike | `C.FLRSH` kept on the card | EN in both |
| Pause menu, weapon page (LBL) | PPU `$0A`, `$38-$40` | pause `$20` | **no D, O, Q or Z** (their slots hold icons); `.` but no `-` | O is written **0** (`N0R`, `P0W`, `W.ST0RM`); `M.BEAM`, `RETIRE`, `SUPER`, `CHIPS` are legal; `CALL` (Should) | EN in both |
| Pause CHIPS page and help pages (WIN) | new engine | glyph cache | full | 4 × 28 per help page (§8) | translated |
| Pop-ups (POP) | new engine | glyph cache | full | 2 × 28, ≤ 24 glyph ids per page + the 4-tile BG face icon | translated |
| Plaques, the crawl, full-screen cards (PLQ) | new engine | glyph cache | full | up to 9 × 28, ≤ 128 glyph ids | translated |
| Game over / continue | PPU `$18/$19/$1A` + `RETIRE` | main `$0B` | as boot | Kalinka's line in the WIN window | labels EN |
| CAPCOM TIMES (NEWS) | vanilla driver `$3B:$A886` for the masthead, picture and `$95/$96`; **GP's pages typed by the new engine in the driver's text rows** | main `$0B` (vanilla pages); glyph cache (GP pages) | GP's JP needs katakana the main font lacks (フォルテ) | 2 lines a page, blip `$27` | translated; `$95/$96` verbatim in JP |
| Ending robot cards (PPU) | PPU `$71-$80` | stage select `$2B` | as bracket | kept verbatim (`DWNB-41 BLIZZARD-MAN`…) | EN in both |
| Staff roll (PPU) | PPU `$81-$87` | roles `$80` (cyan) + main | caps | names in romaji capitals | EN in both |
| TO BE CONTINUED (PPU) | PPU `$88` | main | — | kept, typed in silence | EN in both |

**Main-font katakana.** Vanilla's main font has only 16 katakana (イ ク シ ス ト フ ホ マ ラ リ ル ロ ワ ン and small ッ ュ;
voiced forms use a separate ゛ tile; `rm6/text.md` §6): enough for ロックマン, ロボット, ラッシュ and Dr.ワイリー, not for
フォルテ, ブレイクマン or コサック. So **no GP JP sentence is drawn in a vanilla font**; they all go through the glyph cache.
The newspaper's GP pages are the one place two engines share a screen (§12 asks tech to confirm).

### 10.2 What the text needs from the new engine (tech §11) [new-code] M · Must

`tech.md` §11 builds it (R1.4); this is what the words need.

| Window | Lines × cells | Glyph ids | Where (tech §11.3) |
|---|---|---|---|
| POP (in-stage, live) | 2 × 28 | **≤ 24** + the 16 × 16 face icon (4 BG tiles in the window's first two columns) | top of the screen by default; the bottom on Wind 01 and Tomahawk 10-11 |
| WIN (dialogue, scenes, debrief, help, NPC menus) | 4 × 28 | ≤ 96 | the bottom window (6 rows); the world frozen, sprites off; borrowed tiles restored from ROM |
| PLQ (plaques, crawl, cards) | up to 9 × 28 | ≤ 128 | the full screen |

**Measured against this doc's lines** (`fit.py`): every Must, Should and Could pop-up page fits 24 distinct glyphs in
both languages; the lines that did not were rewritten (round 1's measure: a median of 12 EN and 13 JP glyphs per page).
A pop-up whose screen has fewer than 24 free ids waits in the announcer queue (tech §11.4); P1 lines play on READY.

**Glyph set** (tech §11.4, ≈ 240 glyphs at 8 B):

- Latin capitals, digits, `. , ! ? ' " : ; - / & % ( ) ★ ♥ ♪ β × ▶ ・ …` (EN is ALL CAPS, R1.4: no lowercase set);
- hiragana and katakana with voiced and semi-voiced forms precomposed, small kana, `ー 「 」 『 』 、 。 ~`;
- **one lowercase `r`**, for JP's `Mr.Y`, `Mr.X` and `Dr.` (vanilla's JP writes `Dr.ライト` with a lowercase r;
  EN writes `MR. Y` and `DR.` in capitals). This is the one glyph this doc asks tech to add (§12);
- no kanji (vanilla's JP text has none; the only kanji in RM6 are the logo's).

**Typewriter.** Speed from CONFIG TEXT SPEED (meta §11). A per-speaker blip (vanilla's mechanism, `$06A6`): v1.0 has
**4 blips** (art_audio §12.6): Cossack low, Kalinka high, and Mr. Y's cash-register "ching" (before S33) and Wily's
cackle (after it), two blip ids that the line record's unmasking flag picks between. Everyone else, the icon-less
pop-ups included, types with the neutral blip, which is vanilla's own typing blip `$27` (no new sound). Light's "radio
static" is his face icon's static frame (art_audio §9.4), not a sound; Break Man's pages open on his whistle (the
whistle jingle, R5.2). Spaces are free.

**Highlight.** `*WORD*` draws in the window's second colour (CX does this, `cx/SUMMARY.md` §4). **Choices**: `▶YES NO`
and up to 4 items (tech's CHOICE); in JP `▶はい いいえ`.

### 10.3 Writing rules (enforced by tech's compiler and by `fit.py` here)

1. **EN is ALL CAPS** (R1.4). It is the house style of every NES Rockman script, vanilla's fonts are capitals, and a
   caps-only cache needs about a third fewer distinct glyphs per page. art_audio drops its mixed-case set.
2. **JP is kana only**, with spaces between phrases (vanilla's style: 「8つの ちいきから えらびぬかれた」). Katakana for
   loanwords and robot names; Latin for `Mr.Y`, `Dr.`, `GP`, `DEFENCE`/`MOBILE` (as on the card), `B` (the button),
   `HP`; Arabic digits; 「」 for quotes; `・・・` for ellipses (vanilla's).
3. **Widths:** 28 cells per line; POP ≤ 2 lines, NEWS ≤ 2, WIN ≤ 4, PLQ ≤ 9. A JP line is counted in cells, one per
   kana.
4. **Glyphs per page:** POP ≤ 24 distinct glyph ids (variables count at their width, up to 10).
5. **Per-surface glyph check:** every string against its surface's font (§10.1): on the pause surface D, Q, Z are
   rejected and O converts to 0 when flagged `ZERO_O`; on the bracket `! ? ' :` are rejected; on the panel only §5.1's
   set passes (`fit.py` checks the panel records).
6. **No WIP text ships.** The release build fails on `WIP`, `TODO`, `TBD`, `XXX` or an empty credit field (4MI shipped
   "WIP WIP WIP / UNDER CONSTRUCTION", `r4mi/text.md` §0).
7. **Variables** reserve their width: `%N%` 2, `%M%` 2, `%T%` 4, `%PAR%` / `%TIME%` 7, `%H%` 1, `%MM%` 2, `%NAME%` 12,
   `%WEAPON%` 8, `%PLAYER%` 7, `%ROW%` 8.
8. **Variant selectors** per line: before/after the unmasking (STORY_BEAT ≥ `$09`), DOPED (Could), TAG (Should), BASS
   (Won't), and the cause byte for deaths.
9. **One speaker per page**; a page is one face icon.
10. **R3.3 on screen**: no third-party trademark, console name or character name in any EN or JP string; plaques and
    riddles describe. Capcom's own names (1942, 1943, Gun.Smoke, DuckTales, AYACO, Tango, Quint's Sakugarne) may appear.

### 10.4 Bilingual output, the v1.0 inventory and the text budget

- **One setting:** SYS `$008` LANGUAGE = 0 JAPANESE, 1 ENGLISH, 2 ENGRISH (Could) (`meta.md` §8).
- **One id per string, one table per language.** Source: `text/*.tsv` (`id, surface, speaker, EN, JP, ENGRISH,
  max_lines, notes`), which this doc's rows become one for one (the Id column is the TSV id). tech's compiler emits
  `TXT_EN`, `TXT_JP` and the sparse `TXT_ENGRISH`, dictionary-compressed (R1.4), with the coverage report.
- **The new engine** reads LANGUAGE once per page. **Vanilla PPU scripts** go through the language hook at
  **`$3C:$8636`** (tech §11.2), which serves the few vanilla JP scripts GP keeps: the newspaper's `$95/$96` (EN added).
- **The boss panel, YOU GET, the staff roll and TO BE CONTINUED do not branch**: English in both, as vanilla.
- **A language switch** (CONFIG) takes effect at the next page.

**The inventory** (`fit.py` over this doc; a "string" is one id with its EN and JP; labels have EN only):

| Kind | Must | Should | Could | Won't | What it is |
|---|---|---|---|---|---|
| `scene` | 158 | 8 | 32 | 2 | Must scenes (R4.5) |
| `plaque` | 7 | 7 | 6 | 0 | plaques (Must scenes, R4.5) |
| `death` | 40 | 37 | 7 | 0 | death tables, 4 per stage (R4.5) |
| `heckle` | 12 | 28 | 4 | 0 | heckles (death lines in H1-W3, R4.5) |
| `weak` | 14 | 0 | 1 | 0 | first-weakness lines (R4.5) |
| `secret` | 37 | 12 | 0 | 0 | secret, plate and tell lines (R4.5) |
| `hint` | 51 | 36 | 0 | 0 | debrief hints, tier B (R4.5); R1, R3, R5 Should (§7.3) |
| `help` | 14 | 0 | 4 | 3 | chip help pages (R4.5) |
| `stage` | 56 | 0 | 0 | 0 | a Must mechanic's own text (R0.4) |
| `sys` | 8 | 0 | 0 | 0 | boot, health notice, CONFIG (R3.5, R0.4) |
| `flavour` | 0 | 234 | 36 | 0 | flavour (Should by R4.5) |
| **translated strings** | **397** | **362** | **90** | **5** | EN + JP |
| labels (`LBL`) | 28 | 3 | 5 | 0 | English in both |
| boss-panel records (§5) | 18 | 3 | 4 | 2 | English in both |

**Against R4.5's ≈ 350.** R4.5 lists six Must kinds: death tables (4 per stage), first-weakness lines, secret and
plate lines, Must scenes, tier B hints and the 14 help pages. Those kinds total **333** here (`death`, `heckle`,
`weak`, `secret`, `scene`, `plaque`, `hint`, `help`), inside the ruling. On top sit **64** strings R4.5's list
does not name but R0.4 makes Must, because a Must mechanic cannot run without them: Knight's command windows, Sage,
King, Knightlord and battle log (≈ 33), Tomahawk's posters, conductor and Sheriff (≈ 15), the other venues' and
stages' tells written as signs (`stage`), and the boot and CONFIG sentences, among them R3.5's health notice (`sys`).
**Total v1.0: 397 translated strings**, plus 28 labels and 18 panel records in English only. **R8.4 accepts this
reading** ("about 400 Must strings").

**By area** (R8.4: these counts are the single source; the venue and fortress docs cite them instead of their own
estimates). Must rows only, from the same `fit.py` pass, grouped by Id (a venue's row includes its S11 bar fill, S15
words, §6.3 hooks and deaths and §7.1 hints; a fortress stage's includes its scenes, §6.4 lines and §7.2 hints):

| Area (owner) | Strings | Labels | Area (owner) | Strings | Labels |
|---|---|---|---|---|---|
| Boot and menus (meta) | 8 | 1 | HALFTIME RIOT (fortress) | 30 | 0 |
| Opening-lite (fortress) | 33 | 3 | Hall of Fame scenes S25-S33, Mr. Y's heckles (fortress) | 43 | 2 |
| Bracket, pit stop, debrief generic lines, help pages, generic secret lines (meta, systems) | 48 | 0 | H1 (fortress) | 10 | 3 |
| Blizzard (venues_b) | 13 | 0 | H3 (fortress) | 10 | 5 |
| Wind (venues_a) | 10 | 2 | H5 (fortress) | 8 | 1 |
| Plant (venues_a) | 11 | 1 | W2, W3, Wily's heckles (fortress) | 28 | 1 |
| Flame (venues_b) | 11 | 0 | The ending S40-S48 (fortress) | 39 | 8 |
| Yamato (venues_b) | 12 | 0 | **venues_a** (Wind, Knight, Tomahawk, Plant) | **90** | **4** |
| Tomahawk (venues_a) | 25 | 1 | **venues_b** (Blizzard, Flame, Yamato, Centaur) | **50** | **0** |
| Knight (venues_a) | 44 | 0 | **fortress** (Opening to the ending) | **201** | **23** |
| Centaur (venues_b) | 14 | 0 | **Total** | **397** | **28** |

**Size.** 397 strings × 2 languages ≈ 34 KB raw (about 42 B a string-language), ≈ 22 KB after dictionary
compression, plus ≈ 2 KB of glyphs and ≈ 6 KB of dictionaries: inside tech's text banks T1-T4 (tech §11.5, which
budgeted ≈ 30 KB for ≈ 350). The full design (850 strings with Should and Could) is ≈ 60-70 KB before compression,
under round 1's 1,100-string estimate, and fits the 9 banks tech reserves; if text ever needs a 10th, it is music's
spare bank `$79`, never a CHR bank (R8.7).

**The reserve trim list** (R8.4: held in reserve, not planned; used only if the M4 re-estimate or a later gate needs
it), in order (each keeps every Must mechanic playable):

1. Knight's battle log to the 5 lines that carry a tell (KNT.L03, L04, L06, L08, L09): −5.
2. The Knightlord's refusal (KNT.K04) and the second key line (KNT.S18) folded into one: −2.
3. The fortress b0 showpiece lines (H1-07, H3-10, H5-09, W2-07, W3-08) to §6.2's generic secret line: −5.
4. Tomahawk's three posters become one poster window with three names: −2.
5. The venue tells that a sign or a plaque already gives (FLM-02, CEN-07, BLZ-07): −3.
6. The heckles to Mr. Y 4 and Wily 3 (HY.02, HY.05, HW.04 to Should): −3.
7. S33's green-castle pages (S33.14-S33.15), S33.6's evidence line and S41.8's injury-time confession: −4.
8. *(Applied in round 3: the requirement hints no v1.0 predicate uses, R1, R3 and R5, are Should, §7.3; −3 taken.)*
9. The game-over lines to one (S16): −2.
10. The scoreboard pages folded into the lane judges' cards (S07.6-S07.9): −4.

The reserve is −30 (items 1-7, 9-10), to ≈ 367; the rest would have to come from venue mechanics themselves (a
Must-list change, not a text change). R8.4 keeps the 397: the overage is the mechanics' own text, and the session
estimate below already carries it.

**Sessions** (the v1.0 scope's table): **12** for v1.0 (≈ 40 strings a session written, fitted and compiled in both
languages, plus the M2 setup and the M9 review fixes); Should ≈ 7 (362 strings, mostly one-line pop-ups already
drafted, at ≈ 50 a session); Could ≈ 3 (90); Won't ≈ 0.5. Round 3's moves (three hints to Should, one page swapped)
change no session figure. `tools/plan/tight.py` (text 12) and `tools/plan/tally.py`
carry these figures.

### 10.5 Labels and what the vanilla constraints mean for the script

**Labels.** Menu, HUD and screen labels are story's words (meta §0); this doc approves meta's, tech's and the stage
docs' working labels as written, with these decisions:

| Label | Decision | Why |
|---|---|---|
| `HALFTIME RIOT` | the bracket node and every screen (R4.3) | was SEMIFINAL RIOT |
| The bracket's nodes | champion names (`BLIZZARD MAN`…), not venue names | the stage-select font has no apostrophe (meta §3.2) |
| Venue names | R3.3's eight, on the panel's VENUE field, the results screen and records | §5.1 |
| `KNOCKOUTS` | the records' KO heading (ENGRISH `TIWNS`, Could) | meta §9.4 |
| The entrant board (BOARD.1 below); the Riot's locker `β` | story's numbering (R4.3, consistency-29) | Rockman is entrant 9, Break Man 10 (masked, no name, R4.2), Bass "entrant β" |
| `PI-KUN 16-BIT EDITION` | the scoreboard during the sabotage (S08.9) | fortress §1.5 |
| `UNDER REVIEW` | the doped headline (S44.7, Could) | consistency decision 10 |
| `WARRANTY VOID` | Y-TURBO's CHIPS row in the castle (Could, if systems takes the proposal) | §8 |
| `WPN: CB`, `TIME!`, `INJURY TIME: 30` | W3's HUD (S39.5) | fortress §5.4 |
| Panel strings | §5's records (`BREAKMAN`, `DARKMAN`, `WILY MACHINE` / `VERSION 6.5`, `BLIZZARD.EXE`…) | vanilla's no-space style |

| Id | Tier | Kind | Surf | Who | EN | JP |
|---|---|---|---|---|---|---|
| BOARD.1 | M | stage | LBL | board | 9 ROCKMAN (DR. LIGHT) · 10 ?????? (MASKED) · β BASS β (SPONSOR: MR. Y) | |

| Constraint (`rm6/text.md`) | Consequence in this doc |
|---|---|
| The pause font has no D, O, Q, Z | Pause labels avoid D/Q/Z; O is written 0 |
| The stage-select font has no punctuation | Kalinka's bracket lines live in the WIN window; nodes are champion names |
| The panel is English in JP; 12 cells for a name | Cards in English (§5); W2 copies named `BLIZZARD.EXE` (12) |
| The YOU GET font draws R like A | `C.FLRSH` kept: it reads "C.FLASH" on screen and is a joke in CEN-20 |
| No kanji anywhere but the logo | JP is kana-only, spaced (§10.3); GP's subtitle 史上最大の再会!! is logo art like vanilla's |
| The main font has 16 katakana | All GP JP goes through the glyph cache |
| Typing speed and blip are per-call variables | Per-speaker blips (§10.2) |
| Text timing is fixed waits after typing | Scenes advance on a button; pop-ups on a length-based timer (§6.1) |

---

## 11. How crazy it gets: the story's screenshot moments

The staging docs list their own; these are the story's. v1.0 unless marked.

1. A players' tunnel, a crowd chanting, and a masked entrant number 10 with no sponsor and no name (S03, S06).
2. Rule 9 of the tournament: "IF A SPONSOR MEDDLES, NAME A TAG PARTNER." Rule 8 is "do not ask about Rule 8" (Should).
3. The GP mascot, pumped with Mr. Y-brand helium, turns into PI-KUN 16-BIT EDITION; a masked voice after your first
   fall: "HOLD B. LET GO WHEN YOU GLOW." (S08)
4. Bass β is registered as **entrant β**, because Mr. Y ran out of numbers (S14).
5. *(Should)* The judges' desk always has a cardboard Mr. Y on the sponsor's chair, holding up a 1 (meta §4.0).
6. At halftime the rejected contest entries riot, the lights go out, and a masked stranger holds the crowd back.
   Rock: "...BLUES?" "BREAK MAN." (S17-S20)
7. The trophy is stolen in front of everyone by a claw on Mr. Y's pod (S25).
8. A museum of Rockman 1-5 whose plaques are true and say BLUES, and whose exhibits fight back (S27-S28).
9. A fake Break Man with a flat whistle and an **orange** scarf; hit the wrong note, and the real whistle answers from
   the doorway, in tune (S30).
10. Mr. Y's mask comes off to show Mr. X; Mr. X's comes off to show Wily. Five faces, one page: "WE KNOW." (S33)
11. Wily's 16-bit speech, which is half right: three colours a sprite, eight sprites a line, five channels (S33).
12. The refights are data copies named `BLIZZARD.EXE` (S36).
13. WILY MACHINE 6.5, whose "MODE 7" floor Kalinka exposes as scrolling strips (S38).
14. Break Man catches Rock in the falling castle, and Wily too (S40). In 1990 he pulled Rock from the rubble; this
    time he took Wily as well.
15. Wily blames Mr. Y. "YOU ARE MR. Y." "...MR. Y IS VERY PERSUASIVE." (S41)
16. The ending turns the music off one sound channel at a time while Light explains why that isn't sad; the last sound
    is pulse 1 alone (S42).
17. The Hall of Fame opens a sixth wing for the game you are playing, and its plaque is true (S43).
18. The CAPCOM TIMES reports "MR. Y WAS DR. WILY. WE KNEW.", finds no sponsor for next year (Cossack relaxes), and
    ends on vanilla's own last sentence (S44).
19. The credits keep the 1993 fan designers' cards exactly as Capcom printed them (S45).
20. *(Could)* A booth sells a chip "legal in at least one country"; take it and Break Man walks off the bracket (S21).

---

## 12. Cross-doc dependencies

| Doc | This doc needs (asks) | This doc gives |
|---|---|---|
| `meta.md` | STORY_BEAT at FILE `$013` with §0's values; EVENTS b0-b4/b6/b7 and EVENTS2 b4 (Must), b5 and EVENTS2 b0-3/b5 (Should, Could); COMMFLAGS at FILE `$04A` (b4-b5 Must, §6.1); the sponsor chair's `BACK SOON` from STORY_BEAT `$03` and `RESERVED` from `$09` (the chair and its signs are Should); **W3 has no desk, so its three hints are Should** (§7.2); v1.0's predicate table uses only R2, so **R1, R3 and R5 are Should here** (§7.3) and meta §4.5 should read the same (META-04) | every word meta asked for: the hints (tier B Must, tier A Should), the generic debrief lines, Break Man's debrief (S47), the post-game intro, the bracket lines, the health notice and CONFIG descriptions, the labels' decisions (§10.5), ENGRISH (Could) |
| `systems.md` | The v1.0 weakness rows (§5) for the first-weakness lines; SC5, SC6, SC11 for S28, S19/S37, S39; the 1-bolt insurance (−1, never below 0) for HY.04; the 14 chips' exact effects for §8 | the 14 help pages (YASHICHI and DARUMA both say they exclude each other; DARUMA's page uses the fallback line, its hidden function rejected); `UNDER REVIEW`; the Could bundle's four pages; the Y-TURBO warranty proposal stays with the bundle |
| `venues_a.md` | Its hooks, tiers and triggers are taken as written. Cite §10.4's counts by area instead of its own ≈ 86 (R8.4); HERO'S QUEST's quoted lines are now paraphrased here (R8.4: KNT.S11, S16, S23, K01-K04, D1's JP), so its drafts should follow | final EN/JP of `WND-`, `KNT-`, `TMH-`, `PLT-`; the new sixth Tomahawk death line (TMH.D6); PLT-06 and PLT-08 without "Harry" and "Game Boy"; TO1 without a game's name; Tomahawk Man's showman voice (§2.10); the secret arenas' v1.0 VENUE names (§5.2); KNT.D1 as the King's line |
| `venues_b.md` | Cite §10.4's counts by area (R8.4) | final EN/JP of `BLZ-`, `FLM-`, `CEN-`, `YAM-`; the replacement sixth death lines (BLZ.D6, CEN.D6); FLM-06 for the spacing parry; BLZ-04 and YAM-02 without a Wily gag; YA0's new tier A; the secret arenas' v1.0 VENUE names |
| `fortress.md` | (1) **§0.5 and §2.6** follow R8.5: Rock's first "Blues?" is at the Riot's 0E reveal (S20.2), not S06 (S06 speaks no name), the second at S40; fortress §0.5 said "S06 and S40". (2) **Panel names** in vanilla's no-space style (R8.5): `BREAKMAN` / `DEFINITELY BREAKMAN` → `DARKMAN` / `BAD DISGUISES`, and the WRONG NOTE's extra line is the VENUE field `EXPOSED BY A WHISTLE` (§5.4). (3) The **b1 and b2 secret lines are Should** in v1.0 (§6.4: the generic lines play); b0 and the tells are Must (R8.6). (4) **H5's b0 letters spell `ROCKMAN5`** in both languages (R8.5); this doc's lines spell no letters. (5) New hook ids **WK-WM, WK-WC** (W3's first-weakness lines). (6) The dogeza (S39) has no Mr. Y line: the arrest (S41) carries the ending's one Mr. Y gag and its only alias gag; S44 uses S44.4F, no Mr. Z (R8.5). (7) W3's VENUE on the panel is `FINAL ROUND`. (8) Cite §10.4's string counts by area, not fortress's own ≈ 230 (R8.4) | every line in its stages (S03-S08, S17-S20, S25-S48, §6.4's OPN-/RIO-/H1-/H3-/H5-/W2-/W3- lines, the 4 death lines of the Opening and the Riot, the heckle tables with its wing-tagged drafts as Should variants); the plaques; the panel records; the tier B hints fitted |
| `art_audio.md` | Face icons for the POP speakers (Cossack, Kalinka, Mr. Y/Wily, Roll, Break Man, Light as a radio frame, Eddie; Bass β and the champions); **4 blips**; the whistle jingle (Must) at Break Man's pages and the WRONG NOTE; G37 LAST MATCH with **one stem per 2A03 channel**, dropped in §12.9's order MMC5 (if on), noise, triangle, pulse 2, pulse 1, **no DPCM cue**: the game's only channel drop (R8.3; W2, W3 and the escape keep every 2A03 channel); the panel's bold `- ? ! ' β` and VENUE strip; one CAPCOM TIMES headline (the doped one Could); no mixed-case EN set; the S40 carry art Should; the crawl's pictures Could | the glyph list (§10.2); the per-window glyph budgets; which speakers need icons |
| `tech.md` | The glyph cache with **one added glyph, lowercase `r`** (JP's `Mr.`/`Dr.`); the CAPCOM TIMES' GP pages typed by the new engine in the vanilla driver's text rows (§10.1); the panel's re-type entry able to type a third record (§5.4); `EV_PLATE` and `EV_SECRET` as in §6.1; ≈ 30 KB of text in T1-T4 for v1.0's 397 strings (§10.4); a 10th text bank, if ever needed, from music's spare `$79` (R8.7) | the string inventory and sizes (§10.4); the TSV ids (every row's Id) |

## Lessons applied

| Source | Lesson | Where |
|---|---|---|
| CX 1 | One premise in every layer: the menus speak tournament (entrant β, Rule 9, the judges' desk, ALL ENTRANTS) | §3-§4, §11 |
| CX 2 | Jokes sit on mechanics: the helium mascot is the charge tutorial; the "Mode 7" joke is the effect's own credit; the WRONG NOTE is a full charge on a sound | S08, S38, S30 |
| CX 3 | The villain's voice on failure: one heckle per respawn, with a Yes/No that (barely) hurts: the 1-bolt insurance | §6.5 |
| CX 5 | Reuse the engine's set pieces with one twist: vanilla's boss panel becomes the match card and lies once; vanilla's newspaper ends the game again, with its own last sentence | §5, S44 |
| CX 6 | Telegraph the tool: the tells are Must lines; "watch the flashing"; the requirement hints | §6.2, §6.3, §7 |
| CX (text) | Light's lines, a voice vanilla left silent; the dogeza kept | §2, S39 |
| 4MI 4 | Friends are mechanics and story beats: Break Man's help, block, catch and debrief | S18-S20, S40, S47 |
| 4MI 5 | The debrief as hints, with **no WIP text** (a build check) | §7, §10.3 |
| 4MI (help) | Help pages that are cryptic on purpose (◊) | §8 |
| 4MI (voice) | ENGRISH, TIWNS, `(RESERVED)` | §9 |
| RM6 8 | Vanilla quirks kept on purpose: C.FLRSH, N0R/P0W, the English panel in JP, SOLAR ENERGY, ABILITY UNKNOWN, MOBILE 31, TO BE CONTINUED, the newspaper's last lines, the DWNB cards | §5, §10, S44-S48 |
| RM6 text lessons | PPU-script hook for the few kept JP scripts; per-screen fonts respected; JP kana-only | §10 |
| Round 1 critics | Write to the engine you have: every line fitted to 2 × 28 / 4 × 28 and ≤ 24 glyphs by a checker, not by eye | `fit.py`, §10.4 |

## Risks

1. **Text volume.** v1.0 has 397 translated strings against R4.5's ≈ 350; R4.5's own kinds are 333, and the
   rest is Must mechanics' text. R8.4 accepts about 400. *Mitigation:* §10.4's reserve trim list (−30) if the M4
   re-estimate needs it; the session estimate already carries the full count.
2. **JP quality.** The JP drafts are a non-native pass. Register is the main risk (Mr. Y's わたくし, the hero's-quest
   archaic forms, Yamato's ござる). *Mitigation:* the native review gates release (R4.5), booked at M9; its date is the
   user's to set.
3. **The pop-up strip.** All pop-up pages fit 24 glyphs now; a screen with fewer than 24 free ids defers a line (tech
   §11.4). *Mitigation:* P1 lines play on READY; tells are placed on screens the build reports as roomy.
4. **Pop-up noise.** CX speaks on failure, not constantly. *Mitigation:* v1.0 plays only deaths, tells, secrets and
   first weaknesses (flavour is Should), the 600-f cooldown, DEATHS ONLY, and a playtest metric of no more than one
   P3/P4 line per 20 s.
5. **Facts.** A wrong fact on a plaque is worse than no plaque. *Mitigation:* Appendix A, with confidence; the
   round-2 fact pass corrected Gamma's Top Spin and the Beat letters, and the medium claims are worded to stay true.
6. **Trademarks.** Resolved by R3.3: plaques and riddles describe; the commentators' "can't say the trademark" gag
   stays coherent. Capcom's own names are used.
7. **Gag repetition.** The Wily gag plays once per act, worded differently each time (§1.3's ladder); every other
   "it's Wily" line was cut or reworded (BLZ-04, YAM-02, FLM-08).
8. **Should dependencies.** No v1.0 line needs the partner, the booth or the Exhibitions (§v1.0 scope); the NPC Break
   Man (Must) carries the arc.

## Open questions

1. *Resolved (R8.4):* about 400 Must strings are accepted (the six kinds plus the Must mechanics' text); §10.4's
   trim list is the reserve.
2. *Resolved (R8.5):* the alias gag plays once in the whole ending, at the arrest (S41); S44 uses S44.4F.
3. *Resolved (R8.4):* JP says アルバート for Light's one use of Wily's first name. Story places that use in S33.7, not
   S42, so S42 has no first name and S33.7's JP already reads アルバート.
4. **The thanks plaques' author names** in kana for JP (H2/H4, Should): kept in Latin letters until the authors' own
   preference is known.
5. *Resolved (R8.5):* H5's letters spell `ROCKMAN5` in both languages.
6. **The victory lap's ALL ENTRANTS roll** (Could): generated from the object lists at build time, or written by hand?

---

## Appendix A. Fact sheet (every game-history claim in the text)

Confidence: **high** = confirmed from a cited source (round 1's checks, named) or from the project's own research docs;
**medium** = widely reported, and worded so a small error would not make the line false. **Round 2's fact pass**
(the task's "check the facts on the plaques") re-read every plaque and riddle against this table: two lines were wrong
and are fixed (Gamma's last form fell to the **Top Spin**, not a kick; Rockman 8 is a **disc** game, not a polygon
one), one claim moved from a statement to folklore (the coin shortage, R3.9), and the third-party names left the
screen (R3.3) while staying here, in the design notes, where R3.3 allows them.

| Id | Claim | Used in | Confidence and source |
|---|---|---|---|
| A-1.1 | Rockman (Famicom) was released on 17 December 1987; Mega Man in America the same month | PLQ.H1, S43 | high: gamer.ne.jp, Famitsu |
| A-1.2 | Wily reprogrammed six of Light's robots: Cut, Guts, Ice, Bomb, Fire, Elec; Rock volunteered | PLQ.H1 | high (series canon) |
| A-1.3 | Rockman 1 is the only numbered Rockman with a points score | PLQ.H1, H1-02, H1-07 | high |
| A-1.4 | The Yellow Devil splits into pieces, flies across, reassembles; weak to the Elec Beam (JP サンダービーム) | PLQ.H1, §5.4 | high |
| A-1.5 | The Magnet Beam is in Elec Man's stage, behind blocks the Super Arm lifts | H1.LBL1 | high |
| A-1.6 | In Rockman 1, pausing with SELECT lets the Thunder Beam hit the Yellow Devil again | PLQ.H1 (SC7, Could) | high: Mega Man Glitches wiki |
| A-1.7 | Mega Man's 1987 North American box art famously looks nothing like the game's hero | H1.LBL3, H1-08 | high (widely documented) |
| A-2.1 | Rockman 2: Dr. Wily no Nazo, released 24 December 1988 | PLQ.H2 (Should) | high |
| A-2.2 | Capcom's fan robot-design contests began with Rockman 2 (1988) | PLQ.H2 | high |
| A-2.5 | The Mecha Dragon chases Rock in Wily stage 1 | S28 (Should), §5.4 | high |
| A-2.6 | Flash Man's Time Stopper | G.TS | high |
| A-3.1 | Rockman 3: Dr. Wily no Saigo!?, released 28 September 1990 | PLQ.H3 | high: Nintendo's VC page, Famitsu |
| A-3.2 | Rockman 3 introduced the slide, Rush and Break Man (Blues) with his whistle | PLQ.H3, PLQ.H3.02, H3-01, HY.03 | high: Famitsu |
| A-3.3 | Light and Wily built Gamma together as a peacekeeping robot; its last form falls to the Top Spin | PLQ.H3, PLQ.H3.10, S28.5, §5.4 | high (canon) |
| A-3.4 | Doc Robot copies the eight Rockman 2 bosses, two in each of Rockman 3's four revisited stages; the Air Man copy is in Needle Man's | H3.LBL4, §5.4 (Doc Robot, Should) | high (the eight); medium (which stage) |
| A-3.5 | At Rockman 3's end Break Man pulls Rock from the rubble | S40 | high: Mega Man wiki |
| A-3.7 | Gemini Man's Gemini Laser bounces off walls | PLQ.H3.0B (Should) | high |
| A-3.8 | The Kamegoro Maker (Rockman 3, Wily stage) releases turtles, and destroying them is how it is beaten | §2 legacy bosses, H3-03 (fortress §4.3.3) | high |
| A-4.1 | Rockman 4: Aratanaru Yabō!!, released 6 December 1991 | PLQ.H4 (Should) | high |
| A-4.2 | Rockman 4 introduced the charge shot, Eddie, Dr. Cossack and Kalinka | PLQ.H4 | high |
| A-4.3 | Wily held Kalinka hostage to force Cossack; Blues brought her back | PLQ.H4, the H4 thanks plaque | high |
| A-4.4 | The Cossack Catcher is a crane-game machine | §5.4 | high |
| A-4.5 | Rockman 4 Minus Infinity is by Puresabe, 2008-2016 | S45.2, the H4 thanks plaque | high: `r4mi/SUMMARY.md` |
| A-4.6 | Rockman CX is by Himajin Jichiku (ver 1.1, 2017); its Light is the villain | S45.2, the H2 thanks plaque | high: `cx/SUMMARY.md` |
| A-5.1 | Rockman 5: Blues no Wana!?, 1992 | PLQ.H5, §5.4 | high (year; the day is not printed) |
| A-5.2 | A Blues look-alike kidnapped Light; it was Dark Man, built by Wily; the real Blues appeared and the disguise fell | PLQ.H5, S30, §5.4 | high: Mega Man wiki |
| A-5.3 | The Beat plates spell `ROCKMAN5` in Japan and `MEGAMANV` abroad | H5's b0 plates spell `ROCKMAN5` in both languages (R8.5); H5-09 spells no letters | high (round 1: TCRF, regional differences) |
| A-5.4 | Dr. Cossack built Beat in Rockman 5 | PLQ.H5, G.SP1 | high |
| A-5.6 | Rockman 5's first fortress is Blues' castle, where Dark Man waits | §5.4 (Dark Man's LOCATION) | medium-high (canon; stage names vary by region) |
| A-6.1 | Rockman 6 was released on 5 November 1993, the last Rockman on the Famicom | S43, PLQ.H5.19 | high |
| A-6.2 | All eight RM6 Robot Masters came from fan designs | S43, S45 | high; the DWNB cards name the designers (`DANIEL VALLIE` kept verbatim) |
| A-6.4 | NES: a sprite has 3 colours plus transparency; 8 sprites per scanline; 5 sound channels (2 pulse, triangle, noise, DPCM); MMC5 adds 2 pulses | S33.10, S42 | high (hardware) |
| A-6.5 | Rockman's commonly given height is 132 cm | §5.3 (Bass β's 133) | medium: worded "commonly given" |
| A-6.6 | By the end of 1993 Wily had lost in Rockman 1-6 and in Rockman World 1-4 (the handheld; RW4 is 1993) | HW.07, HW.07K | high |
| A-6.7 | Rockman X was released on 17 December 1993, six years to the day after Rockman 1 and six weeks after Rockman 6 | S43 | high: Famitsu |
| A-6.8 | In vanilla Rockman 6, Silver Tomahawk is the Wily Machine 6's weakness and the Capsule ignores Centaur Flash | WK-WM, `systems.md` §5 | high: `rm6/` research, systems §5 note |
| A-6.9 | Rockman 8 was released in 1996, on disc (PlayStation, Saturn) | S35.11 (Could) | high |
| A-7.1 | Bass (Forte) debuts in Rockman 7 (1995), which also introduces the Super Adaptor | S37, H3.LBL3 | high |
| A-7.2 | Rockman 7 opens with Wily breaking out of jail | S47 | high |
| A-7.3 | Tango debuts in Rockman World 5 (the handheld, 1994) | PLT-08 | high |
| A-7.4 | The Sakugarne is Quint's pogo in Rockman World 2 (1991) | YAM-13 | high |
| A-7.5 | "Block Man" is a Rockman 11 Robot Master (2018) | §5.3 (Could) | high |
| A-8.1 | Dragon Quest (1986): the hidden stairs behind the last lord's empty throne; the hero's ancestor's tablet; the King's scolding at a death; the Princess's "But thou must!"; "an excellent move"; "half the world" | KN0-KN2, KNT.D1, KNT.S11, KNT.S16, KNT.S23, KNT.K01-K04, HLP.KAISHIN, G.EX | high; the text paraphrases these lines in new words, never quotes them (R3.3, R8.4) |
| A-8.2 | *1943*: shooting a POW cycles its item, the Yashichi among them; the Yashichi first appeared in *Vulgus* (1984), Capcom's first arcade game; *1942* gives three loops; AYAKO is a *1943* boss | WI0, WI2, WND.D6, WND-05 | high: Sega Retro, Giant Bomb |
| A-8.3 | *Pitfall!* (1982) has a 20-minute clock and logs cost points; in *Pitfall II* (1984) the explorer seeks his niece, a pet (cat or mountain lion, by source) and a diamond | PLT-01, PL0, PL2 | high |
| A-8.4 | *Prince of Persia* (1989): the mouse opens a gate; the prince merges with his shadow; 60 minutes | FL0, FL1, FLM-03, FLM.D6 | high |
| A-8.6 | *Atlantis no Nazo* (1986): 100 zones plus a secret final one | CEN-02, CE0 | high |
| A-8.7 | *Kid Icarus* (1986): Centurions freed from stone help at the boss; the Eggplant Wizard; a snake-haired boss | CE2, CEN-09, CEN-14 | high |
| A-8.8 | *Ice Climber*: the seals (Topi in the Famicom version) refill holes; the bonus stage's condor | BL0-BL2, BLZ-06 | high |
| A-8.9 | *Gun.Smoke* (Capcom, 1985): wanted posters; shooting odd objects reveals items; "Please do not shoot the pianist" is the saloon sign Oscar Wilde reported from Leadville | TO0-TO2, TMH.S04 | high |
| A-8.10 | The falling-block puzzle was born in Moscow in 1984 | E1 plaque (Could) | high |
| A-8.11 | Block breakers: the 1976 original and its 1986 descendant with a named paddle | E2 plaque (Could) | high |
| A-8.12 | The 1978 fixed shooter's invaders speed up as fewer are drawn; **"they say"** it caused a 100-yen coin shortage (disputed folklore) | E3 plaques, §5.3 (Could) | high (speed-up); folklore, worded so (R3.9) |
| A-8.14 | The ENGRISH classics: "ALL YOUR BASE ARE BELONG TO US" (a 1989 shooter, Europe 1991), "A WINNER IS YOU" (a 1986 wrestling game), "CONGLATURATION !!!" (a 1988 ghost-catching game) | §9 (Could; nodded to in new words, R8.4) | high |
| A-8.15 | Fireworks call "Tamaya!"; the daruma's eyes; 七転び八起き; the nightingale floor; kabuki shouts of the actor's house name; ninja houses' turning panels (donden-gaeshi) | YAM lines, YA0, HLP.DARUMA | high (cultural) |
| A-8.16 | *DuckTales* (Capcom, 1989): the cane works as a pogo and finds hidden treasure | YA1, G.SY1 | high |
| A-8.18 | Rockman's death sound is called "tiun tiun" by Japanese players; 4MI's TIWNS | G.D07, §9 | high: `r4mi/text.md` §0 |

**Retired with the lines that used them:** A-2.3, A-2.4 (H2 details now Should and unchanged), A-3.6 (the controller-2
super jump, no longer cited), A-6.3 (the North American publisher, no longer on screen), A-8.5 (the sekisho's three
passes, cut with the sekisho, R3.2), A-8.13 (Maze Man, Won't), A-8.17 (the "ORA ORA" synergy line, reworded under R3.3).

---

## Changes in round 2

| # | Change | Rulings and findings |
|---|---|---|
| 1 | **v1.0 scope** section added; every string row carries a tier (M/S/C/W); a Must line depends only on Must mechanics (the partner, booth, Exhibitions, W1, H2/H4, the lap and the crawl are Should/Could, with the v1.0 staging written beside them) | R0.1-R0.4; scope-1, scope-3 |
| 2 | **Text model**: every line rewritten in ALL CAPS and re-fitted to its surface: pop-ups 2 × 28 with ≤ 24 glyph ids, dialogue, scenes, debrief and help 4 × 28, full-screen pages 9 × 28; one speaker per page; the face icon is 4 BG tiles. `fit.py` checks every row (0 problems) and counts them | R1.4; feasibility-11, consistency-3, consistency-14, consistency-40 |
| 3 | **The ending** rewritten in R4.1's order (escape, pixelation, S40 the catch, S41 the arrest and the podium with Bass's vow, S44 without `$94`, the credits, S46-S47, S42 LIGHTS OUT, S43, S48); round 1's order and fortress's door-holding and roof variants withdrawn; S42's channel drop is MMC5 (if on), noise, triangle, pulse 2, pulse 1, with no DPCM cue; **the last sound is pulse 1 alone** | R4.1, R5.2; design-1, consistency-6, consistency-13, scope-23 |
| 4 | **Break Man**: the disguise is respected; S06 speaks no name; Rock's two "Blues?" are at the Riot's 0E reveal and S40; Light says "Blues" once (S42); every "OBVIOUSLY Blues" deleted; he joins at Riot 0E with Rule 9 played in place (pages 1-2 Must, the join pages Should); the NPC is Must and the partner Should; rating T1 becomes SOLO RIOT | R4.2; design-2, consistency-7, scope-15 |
| 5 | **Renames and identities**: HALFTIME RIOT everywhere; entrant 9 (Rockman), 10 (masked), β (Bass) on the board and the locker; the Riot crowd is fortress's rejects (S17-S18 rewritten); the one YES/NO heckle is Mr. Y's 1-bolt respawn insurance (round 1's "deal" heckle withdrawn) | R4.3; design-14, consistency-29, consistency-25, design-24 |
| 6 | **The Opening** capped: one intro (S02 is the attract crawl, Could, without "Wily"); NEW GAME goes straight to the tunnel; the rules are folded into the four lane judges; the roll call is the float lines (Should); 12.5 scene pages against the cap of 15 (`fit.py` counts them) | R4.4; design-4 |
| 7 | **The Wily gag plays once per act, worded differently each time** (§1.3's ladder); the acts re-cut so Act III ends with the theft; BLZ-04, YAM-02 and FLM-08 lose their extra Wily gags; the dogeza has no Mr. Y line; the arrest carries the ending's one Mr. Y gag; S44's Mr. Z is Act VI's own (fallback S44.4F if the ruling means one for the whole ending) | R4.4, R4.1 step 4, R3.9; design-23 |
| 8 | **Names**: R3.3's eight venue names on every screen; no third-party trademark, console or character name on screen (Game Boy, Famicom, Harry, Quickclaw, Popo and Nana, Pit, Erdrick, Scrooge, Goemon and "ORA ORA" removed); plaques and riddles describe ("the 1984 sequel", "a 1986 myth game"); Capcom's own names kept | R3.3; design-10, consistency-42 |
| 9 | **Cultural fixes**: Tomahawk Man is the rodeo showman strict about duel etiquette; the Boot Hill line is dropped and TMH.D6 written; the draw is a judged event (TMH-04, the flag judge); the Rodeo Ring; Flame has no "Oil Sultanate" and the vizier is only Wily in costume | R3.4; design-11, design-12 |
| 10 | **Accessibility text**: the health notice, FLASHES: REDUCED and INPUT LAG descriptions (S01 area), CASUAL's description | R3.5; design-13 |
| 11 | **Bosses**: METALL 16 replaces THE UPGRADER (Could, with W1); WILY MACHINE 6.5's panel; Grand Pi-kun one size; Doc Robot Should, copying AIR MAN; Dark Man's panel lies with no "?" and re-types (a third record carries the WRONG NOTE's line); secret arenas' v1.0 VENUE names describe the re-paletted rooms; W2 copies are `.EXE` files; panel records checked by `fit.py` | R3.6; design-24, consistency-8, consistency-22 |
| 12 | **Exhibitions** Could (S22-S23, their cards, plaques and deaths); Maze Man Won't | R3.7; scope-9 |
| 13 | **Replays**: the EXPRESS and LAND skips' words; the conductor reads the bounty count before boarding | R3.8; design-15, design-16, design-20 |
| 14 | **Small rulings**: the coin shortage is folklore ("THEY SAY"); plaques say BLUES (the tone rule's one exception); the Shadow Rock tell (FLM-09, FL0) worded for "harmless until you fire" and the glowing mirror; W1's half-damage line removed | R3.9; design-17, design-19, design-22, design-23 |
| 15 | **Commentators**: v1.0 plays 4 death lines per stage, the first-weakness lines, the secret, plate and tell lines, and the heckles (Mr. Y 6, Wily 4); flavour hooks, death lines 5-6, the generic table and heckle variants are Should; the events table gains a tier column; in H1-W3 one P1 heckle replaces the death line; fortress's Opening and Riot death drafts adopted; its wing heckles are Should variants; fortress stages' b1/b2 secret lines Should (the generic lines play) | R4.5; consistency-25, scope-18 |
| 16 | **Debrief**: tier B Must, the owners' lines fitted to 4 × 28; tier A Should and R3.3-clean; YA0's riddle is new (the sekisho is cut); the fortress stages' tier B lines (no tier A); W3's lines Should (no desk); the generic lines' EN now lives here | R4.5, R3.2, R3.3; consistency-42; meta §4.4-§4.5 |
| 17 | **Chip help pages**: the 14 v1.0 pages are Must at 4 × 28; YASHICHI and DARUMA say they exclude each other; DARUMA's hidden function rejected (fallback line); the Could bundle's four pages; AFTERIMAGE, GLIDER and JET TUNER kept as Won't | R2.5, R2.6, R4.5; consistency decision 33 |
| 18 | **Text budget**: per-tier counts from `fit.py`; R4.5's kinds come to 336, the Must mechanics' text and system sentences add 64 (400 in all), plus 28 labels and 18 panel records; the size fits T1-T4; a trim list to ≈ 367 if the director holds 350 in total | R4.5, R1.5; feasibility-13, consistency-4, scope-18 |
| 19 | **Single sources of truth**: the ownership table at the top; the scene list carries the staging docs' placement and R4.1's step; every scene's placement now matches the revised `fortress.md` and venue docs (S03-S08, S17-S20, S25-S33, S36-S41) | R1.10, R4.1; consistency decision 8 |
| 20 | **Meta hooks**: STORY_BEAT values; EVENTS b5 Should (the join), b7 Must; EVENTS2 b4 is the SUPER scene, with FORMS.SUPER set at H3 12 without a YOU GET card; COMMFLAGS b4-b5 Must; the language hook cited at `$3C:$8636` | consistency-28, consistency-41, design-14 |
| 21 | **Fact pass** on the plaques and riddles: Gamma's Top Spin, Rockman 8 on disc, Doc Robot's stage, the Beat letters (neither spelling on screen), the coin shortage; new facts A-1.7, A-3.7, A-3.8, A-5.6, A-6.8, A-6.9; retired facts listed | the task's fact check; R3.3, R3.9; design-23 |
| 22 | **Lag and CASUAL**: no story element occupies an object slot (pop-ups, plaques and windows are BG); story owns no stage, so it has no CASUAL lever list | R1.8, R2.9 |
| 23 | **Ledger**: text v1.0 stays 12 sessions (`tools/plan/tight.py`); `tools/plan/tally.py`'s text line now reads Must 400 strings ≈ 12, Should ≈ 7, Could ≈ 3, with the native-JP review as a dated external gate | R0.1, R4.5 |
| 24 | **Asks to other docs** recorded in §12: fortress §0.5's "S06 and S40", the no-space panel names, the H5 letters, the new WK-WM / WK-WC ids; tech's lowercase `r` and the newspaper's GP pages; meta's W3 hints and R1/R3/R5 | consistency decision 8; R4.1 |

---

## Changes in round 3

RULINGS §8 (R8.1-R8.8) and the "## story.md" table of `reconcile.md`. `fit.py` re-run: 0 problems; Must 397, Should
362, Could 90, Won't 5 translated strings; 28 labels and 18 panel records unchanged. Text stays **12 sessions**
(verify-4 moves 0.25 from M4 to a new M3 row; no other milestone figure changes). The "Changes in round 2" table above
is history: where it says S44's Mr. Z is Act VI's gag or the trim list is −33, this round supersedes it.

| Request | Outcome | Section | Note |
|---|---|---|---|
| STORY-01 | applied | §4 S47; §1.3; §11 | S47.T1 now names the Riot, and the note says T1 is SOLO RIOT (RATEFLAGS b4), never a call or SELECT. Already there: YA0.A (§7.1), SYS.HARD = ×1.5 damage, fewer drops, no refill; SYS.HEALTH, SYS.LAG, SYS.CASUAL and SYS.CASUALBIT (Boot and menus); the sponsor's chair Should (§1.3, now also marked in §11 item 5) |
| STORY-02 | already | §6.3 Tomahawk, Plant; §2.10; S15 | TMH.D6 replaces Boot Hill; PLT-06/PLT-08 name no Harry or Game Boy; the rodeo showman; WND.S02 (LAND, LANDED), TMH.S07/S09 (the count, EXPRESS), KNT.S17/S18 (the stairs check), KNT.S02 (the Sage's after-death tell), TMH.S15 (the RODEO RING) |
| STORY-03 | already | §6.3 Blizzard, Flame, Centaur, Yamato | BLZ.D6 and CEN.D6 replaced; BLZ-04 is no Wily gag at all (one per act, R4.4); FLM-06 teaches the 48-px spacing; CEN-21, CEN-22, YAM-21 exist; sekisho and hanabi lines retired |
| STORY-04 | applied | §4 S42; §12 art_audio row | S42's cues are a table in art_audio §12.9's order (MMC5 if on, noise, triangle, pulse 2, pulse 1), no DPCM; "already silenced when the castle fell" applies only to the MMC5 voices (R8.3). Already there: one Must headline (S44.7 Could), 4 blips (§10.2), the S40 carry art Should, the crawl Could |
| STORY-05 | already | §4 Acts 0, II, IV, V; §6.4; S30; §5.4; Appendix A | fortress §9.4's new lines exist (lane judges, the `?` card S07.5, the breaker RIO-05, NO DATA RIO-08, the turtles H3-03, FISTS ONLY, TAG! W2-03, the gap sign's second line H1.LBL2, the jammed pod W3-07); the orange scarf (S30.2); no-space panels; facts A-3.4, A-3.8, A-8.12, A-6.9 |
| STORY-06 | applied | §7.3; v1.0 scope; §10.4 | v1.0's predicate table uses only R2 (meta §4.3), so R1, R3 and R5 (and DB.R1, DB.R3, DB.R5) are Should: Must −3 (400 → 397), Should +3; the trim list's item 8 is taken |
| STORY-07 | applied | §1.2 rule 11; S15; §6.3 Knight; §6.2 G.EX; §8 HLP.KAISHIN; §9; S47; §1.3; S41; S44; S27; §6.4 H5; Open questions | R8.4: 397 Must strings accepted, the trim list is the reserve; quoted lines paraphrased in both languages (KNT.S11, S16, S23, K01-K04, KNT.D1's JP, G.EX, HLP.KAISHIN, ENGRISH's A CHAMPION IS YOU and CONGLATULATE !!!, S47.PE); Light's one first-name use is S33.7, whose JP already says アルバート. R8.5: the alias gag only at the arrest (S41), S44.4F is Must and S44.4 Won't; the H5 plates spell ROCKMAN5 in both languages |
| R8.3 (extra) | applied | §4 S35 | S35.7 ("MORE CHANNELS") plays only if the MMC5 voices ship; W2, W3 and the escape keep every 2A03 channel (S42 prose) |
| R8.4 (extra) | applied | §10.4; §12 | A by-area table of Must strings, the single source the venue and fortress docs cite (venues_a 90 + 4 labels, venues_b 50, fortress 201 + 23 labels); the reserve trim list is −30 |
| R8.5 (extra) | applied | §5.4; §12 fortress row; §4.0; §11 item 18 | no-space panel names and the third record cited to R8.5; the press's "WE KNEW." is Act VI's Wily gag; no Mr. Z anywhere in v1.0 |
| R8.6 (extra) | applied | §4 S41 | the champions applaud in pairs (0 new tiles; the all-eight row Should). Already: fortress b1/b2 lines Should, the nightingale floor Should (YAM-06, -07, YAM.D2-D3) |
| R8.7 (extra) | applied | §10.4; §12 tech row | a 10th text bank, if ever needed, is music's spare `$79`, never CHR |
| R8.1, R8.2, R8.8 | already | v1.0 scope | no stale ledger total or cumulative figure, slice form, attach-state or stage-`$00` text in this doc; story's milestone table (12 sessions) is one of R8.1's inputs, unchanged |
| verify-1 | fixed | §5.3 | the Exhibition panels' NAME cells are `BLOCKMAN`, `PADDLEMAN`, `INVADERMAN`, `MAZEMAN` (vanilla's no-space style, §5.1, R8.5); the dialogue keeps BLOCK MAN etc. |
| verify-2 | fixed | §5.3; §6.1; §7.2 | §5.3's quote of a Kalinka line "(S19.2)" that no row holds is deleted (S19.2 is Rock's); §6.1's speaker list says Roll (Ro), the Who key's code; §7.2 cites A-5.3 (the plate letters), not A-5.4 |
| verify-3 | fixed | §6.3 "The other venues' words" | CEN.S01 (the tablet) and CEN.S02 (ZONE 0's inscription) move from WIN to POP: Centaur lands at M5, before text v1b (M6), so they use the v1a pop-up like every sign (venues_b §0.6). Each is re-fitted to one 2 × 28 page (the tablet still names all three doors), so the counts are unchanged (`fit.py`: 0 problems, Must 397) |
| verify-4 | fixed | v1.0 scope (sessions) | the milestone table follows the scene list and meta's milestones: a new M3 row (S10, S16's game-over lines, 0.25) for meta's M3 pit stop and game over, M4 1 → 0.75; S12-S13 move from M6 to M5 with meta's adaptor events; M6 keeps S14 and S24. Total still 12 |
| verify-5 | fixed | v1.0 scope (sessions, M4); §5.1 | the slice's card is vanilla's 9-field `BLIZZARDMAN` record typed by `$51`; its VENUE `SUMMIT CLIMBER` and the secret arena's `ABOVE THE CLOUDS` arrive with tech's panel extension at M5 (tech row 33) |
| verify-6 | fixed | §8 HLP.KAISHIN | EN line 2 reads "12TH HIT ON A BOSS LANDS" (systems §9.2 #7, R2.4: every 12th boss hit), matching the JP ボスへの |
| verify-7 | fixed | §10.2 | art_audio's request: the 4 blips are Cossack, Kalinka, Mr. Y's ching and Wily's cackle (two ids picked by the line record's unmasking flag, art_audio §12.6); the neutral blip is vanilla's typing blip `$27`; Light's "radio static" is his face icon's static frame (art_audio §9.4), not a sound |
