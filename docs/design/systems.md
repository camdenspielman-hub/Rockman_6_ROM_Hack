# Rockman 6 GP: player-facing systems

Author: design-systems. Status: **round 3** (revised against [`RULINGS.md`](RULINGS.md) §0-§8, which is binding and
overrides [`BRIEF.md`](BRIEF.md) where they differ; round 3's changes are listed at the end). Facts come from `docs/research/*`. Numbers measured for round 1 are tagged
**[seen, ds]** (scripts in `build/design/design-systems/`); facts re-checked in the ROM or emulator for round 2 are
tagged **[code, r2]** or **[seen, r2]** (scripts in `build/revise/systems/`: `verify_r2.py`, `chrsets_formslot.py`,
`cflash_strobe.py`). Every number is grounded in vanilla, argued in the text, or marked **(tune)**.

Tags (BRIEF §8, RULINGS §0):

- **[engine-ok]**: vanilla does it, or it is a data change;
- **[new-code]**, **[new-art]**, **[new-music]**;
- sizes **S/M/L**; tiers **Must** (v1.0) / **Should** (v1.1+, in the cut-line order of RULINGS R0.3) / **Could** /
  **Won't (v1)**. A Must depends only on Musts (R0.4); §15.3 lists what each Must leans on.

Every item has an id (`SYS-…`), so other docs can cite it. Single sources of truth (RULINGS, consistency critic):
**this doc owns combat, economy and chip numbers**; `meta.md` owns save bytes, the bracket, events and the debrief;
`tech.md` owns ids, memory, the raster list, CHR/ExRAM limits and the bank ledger; the venue docs and `fortress.md` own
staging and stage mechanics; `story.md` owns every word (help pages, commentator lines, headlines); `art_audio.md`
owns tile, byte and track budgets.

---

## v1.0 scope

What of this doc ships in **v1.0 "Championship"** (RULINGS R0.2), with the release rung where each item first lands
(v0.1 = the Blizzard slice, M3-M4; v0.5 = Round One, M5-M6; v1.0 = M7-M8) and its estimate in focused sessions. The
ledger baseline is `tools/plan/tight.py` (systems block) and `tools/plan/tally.py` (systems rows); both were updated
with this revision and agree on **49.5 sessions** of Must systems code, data and tests (the round-1 tight estimate was
46.5: +1.5 for the Ice Block that R2.4 puts in the slice, +1 for the CASUAL lever framework of R2.9 and INPUT LAG of
R3.5, +0.5 for the flash-safety rule of R3.5, +0.5 for SC11 and +0.5 for the input rules of R2.10, −1 for moving the
Y.SPEAR pierce and PLANT.B's two-contact barrier to Should). Round 2 moved `tight.py`'s total by +3; after every doc's
round-2 changes the tight Must is **about 450 sessions** (R8.1), and RULINGS §6's cumulative column adds up this table's
per-rung figures. The full inventory in `tally.py` lists systems at Must 49.5, Should 35.5, Could 12 and Won't 1.5.
**Round 3 (R8.2)** moves about 5 of these sessions from the slice to Round One (items 2-4: a new file owns no forms, so
the slice cannot reach them); the total is unchanged.

| # | Item (ids) | What ships | Rung | Sessions |
|---|---|---|---|---|
| 1 | SELECT modifier, last-weapon toggle, input rules (SYS-CTL-1, -2, -5) | SELECT + Up/Down weapon cycle (Normal form's slot-set stream), tap toggle, UP-interact rule, 10-f alt lock, the mash and reflex helpers, buster only while attached (the condor); the form cycle lands with item 2 | v0.1 | 2 |
| 2 | Quick form swap (SYS-CTL-4) | 2 KB stream behind a 16-20 f flash, the per-form `$71-$7F` slot-set map, the SELECT + Left/Right form cycle, the set-piece-sheet hook, the once-per-form docking debut | v0.5 (M5, R8.2) | 3 |
| 3 | Forms fire every tap (SYS-FRM-1) | the weapon × {tap, alt, synergy} dispatch table with Normal form's tap column and the Ice Block (slice, 1); the Power and Jet rows (M5, R8.2, 1) | v0.1 / v0.5 | 2 |
| 4 | Adaptors by win count (SYS-FRM-2) | Power at 2 wins, Jet at 4, FORMS.SUPER on Rush's dock in H3 | v0.5 (M5, R8.2) | 1 |
| 5 | B.ATTACK's Ice Block (SYS-WPN-3A) | the one alt in v1.0: the alt-dispatch and frozen-tick prototype | v0.1 | 1.5 |
| 6 | Frozen tick (SYS-CMB-3) | three frozen handlers (`$E9D7`/`$EA20`/`$EA6E` kinds), the NOFREEZE override list, the boss stall | v0.1 | 2.5 |
| 7 | GP_BOSSHIT (SYS-CMB-1) | damage and i-frame tables for the v1.0 boss list, the generator and the chart | v0.1 | 2.5 |
| 8 | Normal-enemy rules (SYS-CMB-2) | low nibble, lingering re-hit timer, featured-enemy tell tables (no PART drop) | v0.1 | 1 |
| 9 | Weakness feedback and flash safety (SYS-WK-1, SYS-FX-1) | WEAK! pop, stagger, SFX, announcer events; the 3-per-second flash rule for every effect this doc owns | v0.1 | 2 |
| 10 | Attribution (SYS-SC-4) | LATCHSRC written at every latch store, read at the death and boss-hit hooks; **no punch re-class** | v0.1 | 2.5 |
| 11 | Scorecard (SYS-SC-1, -3) | counters, formulas, pars, STYLE, medals and pay, replay tokens | v0.1 | 3 |
| 12 | Bolts and the Pit Stop (SYS-ECO-1) | income rules and caps, envelopes, v1.0 stock and prices | v0.1 | 2 |
| 13 | Chip framework (SYS-CHP-1) | 3-byte bit fields, slots, equip rules, the second-wind family | v0.1 | 2 |
| 14 | Shop chips and the Balancer (SYS-CHP-2) | SHOCK ABSORBER, SPIKE GUARD, CHARGE KIT in the slice; EXCHANGER, ENERGY SAVER, ENERGY BALANCER in Round One | v0.1 / v0.5 | 2 |
| 15 | The 8 venue behaviour chips (SYS-CHP-2) | effects of YASHICHI, KAISHIN, SHERIFF STAR, AUTO RECOVER, SNOW CHAINS, FIREPROOF, CENTURION, DARUMA (SNOW CHAINS in the slice) | v0.1 / v0.5 | 3 |
| 16 | Pickups (SYS-PU-1, -2, -3) | routing, drops presets, respawn refill, game over | v0.1 | 2 |
| 17 | Difficulty (SYS-DIF-1, -4) | presets (CASUAL / NORMAL / HARD v1.0), the DIFF bits, the layout tier, the CASUAL lever helpers, INPUT LAG | v0.1 | 3 |
| 18 | Tap tweaks (SYS-WPN-0) | B.ATTACK cost 2, PLANT.B cost 3, C.FLASH lights dark rooms | v0.5 | 0.5 |
| 19 | Plates and Beat (SYS-BT-1) | plates → slots; Beat's pit rescue, once per screen | v0.5 | 2 |
| 20 | HARD framework (SYS-DIF-2) | `IFHARD`, the layout tier keyed poke lists (no per-stage content in v1.0) | v0.5 | 1.5 |
| 21 | Special cases (SYS-SC-CASES) | SC1 Knight's shield, SC6 Bass β, SC8 the quick-draw, SC9 venue reactions (v0.5); SC5 Gamma, SC11 CHAMPION BUSTER (v1.0) | v0.5 / v1.0 | 3.5 |
| 22 | MAGNET BEAM (SYS-WPN-9) | the build tap, max 2 beams | v1.0 | 2 |
| 23 | Super Adaptor (SYS-FRM-5) | rocket fist with homing return, jet hop; needs tech's `$9B` audit | v1.0 | 3 |
| | **Total Must** | | | **49.5** |

By rung (round 3, R8.2): about **28** sessions land in the slice (items 1, 5-13, 16-17, item 3's dispatch table with
Normal's taps, three shop chips, SNOW CHAINS), about **15.5** in Round One (items 2 and 4 and the Power and Jet rows of
item 3 now open it, at M5), about **6** in v1.0. **A new file owns no forms** (Power comes with the 2nd win), so the
slice has no form swap, no form cycle and no adaptors. RULINGS §6 (R8.1) now adds these figures up: M3 is about 44
sessions (79 → ~123) for all slice systems, this doc's and tech's T6, X-BONK, X-WRAP, HUD widgets, commentator bus and
the attach state's core, so round 2's shortfall (Risk 1) is closed by the re-baseline; the M4 re-estimate calibrates
the rest (R0.1).

**Should (v1.1+), in the order they come back** (RULINGS R0.3; sessions):

1. Cut-line item 1, **the alts and synergies**, one weapon at a time: Time Stop + SC2 (2), Wall Spear (1), Updraft (1),
   KNIGHT.C Hold (1), the 8 synergies (9, Pogo and Burning Knuckle first), then Flare, Feather Fan and Petal Shot
   (3.5, last, because no stage uses them as tools: design-6), the M.BEAM magnet (0.5), and tap polish (Y.SPEAR pierce,
   PLANT.B's two-contact barrier, 1).
2. Cut-line item 2, **the Break Man tag partner** (5): slot-0 character variant, call row, moveset, tag gates.
3. Cut-line item 3, **HARD per-stage poke lists and boss branches** (8, mostly counted in the stage docs).
4. Small Shoulds: SC4's own-weapon hook (1), SC10 COUNTER (fortress, 0.5), controller-2 pseudo L/R (0.5), W-tank,
   E-tank ×2, overflow bolts and the low-fuel pip (1.5).

**Could:** cut-line item 9, **the PARTs + garage + Mr. Y booth + Y-TURBO bundle** (4.5), which ships together with the
tag partner; cut-line item 10, **1993 RULES** (3); the parry (2); Power ice grip, the weakness ★, RACING COLOURS, SC3,
SC7, the exhibitions' RULE column and OWNED override (2.5 together).

**Won't (v1):** criticals (KAISHIN keeps its deterministic EXCELLENT MOVE); the chips AFTERIMAGE, GLIDER and JET
TUNER; the half-charge damage bump (it would change a vanilla attack byte, R2.1); Jet air-dash; the overheat stall.

---

## 0. Scope and the decisions in one page

This doc owns what the player touches in every stage:

- controls; forms and physics;
- the weapons, Magnet Beam and the Break Man moveset;
- the damage and i-frame tables; weakness feedback; the flash rule for its own effects;
- the scorecard; bolts, the shop and chips; slots and plates;
- the tag partner rules; pickups and economy; difficulty, including the CASUAL lever list.

It does not own stage layouts, boss patterns, words, UI art, save bytes or the memory map. It states what it needs from
each (§15).

**The decisions (round 2):**

1. **SELECT is a modifier** (§1). In a stage SELECT means only the quick swap and the last-weapon toggle (R2.10):
   hold SELECT + Up/Down cycles weapons, + Left/Right cycles forms; a tap toggles the last weapon. Interaction (doors,
   NPCs, plaques) happens on an UP press with B not held, and never within 10 frames of an alt.
2. **The quick form swap has no cutscene** (§1.3). It streams the form's whole 2 KB sheet in **16-20 frames** behind a
   swap flash (R2.3), with CHR-RAM kept at 8 KB. The weapon slot `$71-$7F` follows a per-form map (§1.4). The vanilla
   Rush-docking cutscene plays once per form per save. It lands at M5 (v0.5): a new file owns no forms, so the slice
   cannot reach it (R8.2).
3. **Forms fire every weapon's tap** (§3; the Power and Jet rows at M5, R8.2). The dispatch table has alt and synergy
   columns, but in v1.0 only one alt
   ships: **B.ATTACK's Ice Block**, built in the Blizzard slice as the prototype for alt dispatch and the frozen tick
   (R2.4). The other 7 alts and the 8 synergies are Should, added one weapon at a time.
4. **Combat = two tables, 4MI-style (credit: Puresabe)** (§4). Weakness 4 dmg / 16 f, good 3/20, neutral 2/30,
   resisted 1/45, buster 1/60 (vanilla). The vanilla weakness cycle is kept. The tables cover the v1.0 boss list (§4.5).
5. **Scoring comes from LATCHSRC, not from re-classed shots** (§6.4, R2.1). Vanilla attack bytes `$11-$14` stay, so no
   enemy AI latch compare is patched. Every latch store also writes the source column; the death and boss-hit hooks
   read it.
6. **Frozen objects keep taking damage** (§4.8, R2.2). Enemies whose damage step is `$E9D7`, `$EA20` or `$EA6E` get a
   frozen handler; every other type is NOFREEZE (it ignores freezes, still takes hits). Bosses get a stall, not a
   skipped AI.
7. **The economy has no grind** (§7-§8). Bolts come only from scorecards (best score per stage, paid once), one sponsor
   envelope per hidden room, and capped prizes (≤ 60 per stage, venue or not). venues_b's bags become envelopes (R2.7).
8. **Fourteen chips in v1.0** (§9, R2.5): the 8 venue behaviour chips, the Energy Balancer, and 5 shop chips (SHOCK
   ABSORBER, SPIKE GUARD, CHARGE KIT, EXCHANGER, ENERGY SAVER). AFTERIMAGE, GLIDER and JET TUNER are cut. **PARTs, the
   garage, Mr. Y's booth and Y-TURBO are one Could bundle** that ships with the tag partner (§9.4).
9. **Safety nets don't stack** (R2.6): Beat's rescue works once per screen; YASHICHI and DARUMA are one mutually
   exclusive "second wind" family; a Break Man retreat (when the partner ships) uses up his call for the stage.
10. **Beat** (§10): each plate adds a chip slot (2 + 4 = 6); B-E-A-T complete makes Beat the pit rescue; vanilla's BEAT
    slot 9 becomes MAGNET BEAM.
11. **Break Man the partner is Should** (§11; R4.2): a slot-0 character variant (R1.12), called from a pause-menu row
    confirmed with A. **Break Man the NPC is Must, and is not a systems item.**
12. **Difficulty** (§13): CASUAL gets its own bit, layout tier and a standard lever list every stage fills in; **HARD in
    v1.0 = ×1.5 damage, drops LESS, no refill**, with the framework hooks kept; **1993 RULES is Could** (R2.9).
13. **Criticals are Won't** (R2.4). KAISHIN is always the deterministic EXCELLENT MOVE: +2 on every 12th boss hit.
14. **Gamma** (R2.11): POWER, owned from the 2nd win, may be required in the fortress, with a tell. That is SC5, the only
    form gate on a main route.

### 0.1 Item index

| Id | Item | Tags | Size | Tier |
|---|---|---|---|---|
| SYS-CTL-1 | SELECT modifier: weapon and form cycle | new-code | S | Must |
| SYS-CTL-2 | Last-weapon toggle (SELECT tap) | new-code | S | Must |
| SYS-CTL-3 | Controller-2 pseudo L/R | new-code | S | Should |
| SYS-CTL-4 | Quick form swap with the 2 KB stream | new-code, new-art (1 tile) | M | Must |
| SYS-CTL-5 | Input rules: UP-interact predicate, alt lock, mash and reflex helpers, INPUT LAG | new-code | S | Must |
| SYS-FRM-1 | Forms fire weapon taps (dispatch table with alt and synergy columns) | new-code | M | Must |
| SYS-FRM-2 | Adaptors by win count (Power 2nd, Jet 4th), FORMS.SUPER on the H3 dock | new-code (patch `$38:$931D`, `$3B:$BA3F`) | S | Must |
| SYS-FRM-3 | Power parry | new-code, new-art (1 spark) | M | Could |
| SYS-FRM-4 | Power ice grip | new-code | S | Could |
| SYS-FRM-5 | Super Adaptor: rocket fist with homing return, jet hop | new-code, new-art | L | Must (with H3) |
| SYS-FRM-6 | Jet low-fuel pip | new-code | S | Should |
| SYS-WPN-0 | Tap tweaks (costs, C.FLASH lights dark rooms) | engine-ok + new-code | S | Must |
| SYS-WPN-1..8 | The eight boss weapons: **tap** | engine-ok + new-code | M total | Must |
| SYS-WPN-3A | B.ATTACK alt: Ice Block | new-code, new-art (4 tiles) | M | Must (slice) |
| SYS-WPN-ALT | The other 7 alts | new-code, new-art | L total | Should (cut-line 1) |
| SYS-WPN-SYN | The 8 form synergies | new-code, new-art | L total | Should (cut-line 1) |
| SYS-WPN-9 | MAGNET BEAM (slot 9): build | new-code, new-art | M | Must (H1 is Must); magnet alt Should |
| SYS-WPN-10 | Buster charge rules (vanilla thresholds and bytes) | engine-ok | S | Must |
| SYS-CMB-1 | Boss damage + i-frame tables, one lookup | new-code | M | Must |
| SYS-CMB-2 | Normal-enemy rules (low nibble, featured-enemy tells, re-hit timer) | engine-ok + new-code | S | Must |
| SYS-CMB-3 | Frozen tick (frozen handlers, boss stall) | new-code | M | Must |
| SYS-WK-1 | WEAK! pop, stagger, SFX, announcer event | new-code, new-art (3 tiles) | S | Must |
| SYS-FX-1 | Flash safety for this doc's effects (C.FLASH, WEAK flash, machine hit pulse) | new-code | S | Must |
| SYS-SC-1 | Scorecard counters and formulas | new-code | M | Must |
| SYS-SC-2 | Results screen (judges) | new-code, new-art | M | Must (owner: meta.md) |
| SYS-SC-3 | Secret tokens on replays | new-code | S | Must |
| SYS-SC-4 | Attribution through LATCHSRC | new-code | M | Must |
| SYS-SC-CASES | Special cases SC1-SC11 (SC12-SC14 are stage-owned, counted by their docs) | new-code | S each | per row, §4.6 |
| SYS-ECO-1 | Bolts, income caps, Eddie's Pit Stop stock and prices | new-code | M | Must |
| SYS-CHP-1 | Chip framework (bits, slots, equip rules) | new-code | M | Must |
| SYS-CHP-2 | The 14 v1.0 chips | new-code, new-art (1 tile) | M | Must |
| SYS-CHP-3 | PARTs and the garage | new-code, new-art (8 icons) | M | Could (bundle) |
| SYS-CHP-4 | Mr. Y's booth and Y-TURBO | new-code | S | Could (bundle) |
| SYS-BT-1 | Plates → slots; Beat's pit rescue | new-code | M | Must |
| SYS-TAG-1 | Break Man tag partner | new-code, new-art (sheet), new-music (whistle, Must via R5.2) | L | Should (cut-line 2) |
| SYS-PU-1 | Pickup routing (HP conversion, Balancer, Exchanger) | new-code | S | Must |
| SYS-PU-2 | Drops table and presets | engine-ok (data) + new-code | S | Must |
| SYS-PU-3 | Pit-crew refill on respawn; game over rule | new-code | S | Must |
| SYS-PU-4 | W-tank; E-tank heal ×2; overflow bolts | new-code | S | Should |
| SYS-DIF-1 | Presets and overrides | new-code | M | Must |
| SYS-DIF-2 | HARD framework (`IFHARD`, layout tier); per-stage HARD content | new-code | M | Must (framework); Should (content, cut-line 3) |
| SYS-DIF-3 | 1993 RULES | new-code | M | Could (cut-line 10) |
| SYS-DIF-4 | CASUAL tier and the standard lever list | new-code | S | Must |
| SYS-CRT-1 | Criticals | | | Won't (v1) |

---

## 1. Controls

Vanilla facts: joypad 1 held/new = `$40`/`$42`, joypad 2 = `$41`/`$43`; A=$80 B=$40 SELECT=$20 START=$10 UP=$08
DOWN=$04 LEFT=$02 RIGHT=$01. The read routine is `$3E:$C711`. The only SELECT test in the ROM is the dead sound player
(`$28:$813C`), and holding SELECT for 240 frames in 8 game states changes nothing (`rm6/ram.md`). **SELECT is free.**
Controller 2 is read into `$41/$43` every frame and never consumed (`tech.md` §15.4).

**R2.10: in a stage, SELECT means only the quick swap (§1.1) and the last-weapon toggle (§1.2).** It has no meaning in
the pause menu. The bracket screen's SELECT (open the Pit Stop) is `meta.md`'s and is not in a stage.

### 1.1 SYS-CTL-1: the SELECT modifier [new-code] S, Must (v0.1; the form cycle v0.5)

One filter runs right after the joypad read. It is active only in stage play: not paused, not in a transition, no
cutscene, no set-piece sheet and no attach state (§1.4), not playing Break Man. It changes `$40/$42` before the player
AI sees them.

**R8.2:** the slice (v0.1) builds SELECT + Up/Down (weapons) and the last-weapon toggle. The form cycle (SELECT +
Left/Right) arrives with the quick form swap at M5, because a new file owns no forms until the 2nd win.

```
if SELECT held:
    on UP edge    -> weapon_prev()        on DOWN edge  -> weapon_next()
    on LEFT edge  -> form_prev()          on RIGHT edge -> form_next()
    any D-pad edge sets SEL_USED
    UP and DOWN are removed from $40/$42 while SELECT is held (no ladder grab, no slide)
    a LEFT/RIGHT edge sets that direction's bit in SWAPMASK
SWAPMASK bits are removed from $40/$42 until that direction is released
```

Why the mask works this way:

- Walking right with RIGHT held, then pressing SELECT + LEFT, swaps the form while Rock keeps walking right. LEFT is
  masked; RIGHT is untouched.
- Swapping in mid-air keeps the player's air control, which a full D-pad mask (CX's rule) would not. RM6 air control
  is direct, so a full mask would kill the jump.

Cycle orders (skip what is not owned):

- **Weapons**: BUSTER, Y.SPEAR, W.STORM, B.ATTACK, F.BLAST, PLANT.B, KNIGHT.C, SILVER.T, C.FLASH, M.BEAM, wrapping.
  This is the vanilla menu order, `$0688-$0691`, with slot 9 renamed (§3.10). A slot is owned when its energy byte is
  not `$80` (energy is 0..`$1B`, `rm6/ram.md`).
- **Forms**: NORMAL, POWER, JET, SUPER, wrapping.

The venue id → weapon slot map is vanilla's `$3F:$F704` = `03 02 05 04 01 07 06 08` [code, r2]: Blizzard → 3 B.ATTACK,
Wind → 2 W.STORM, Plant → 5 PLANT.B, Flame → 4 F.BLAST, Yamato → 1 Y.SPEAR, Tomahawk → 7 SILVER.T, Knight → 6 KNIGHT.C,
Centaur → 8 C.FLASH. meta.md's WEAPONS bits (by venue id), tech and EXTRA CONFIG cite this table (consistency-37); GP
relocates it with the stage-attribute work.

Feedback: the weapon bar recolours at once (vanilla's per-weapon palette table `$38:$962F`), plus a short tick SFX.
Vanilla's menu blip `$32` is the placeholder.

What a swap keeps (CX lesson: "decide what survives a swap"), refined for the CHR rules of §1.4:

- Weapon shots already in flight finish, and they keep their LATCHSRC column for scoring.
- **A form swap** keeps every lingering object (the Ice Block, M.BEAM beams), because the weapon's tile set is
  re-streamed unchanged. It deletes **slot-0 shots** in flight (buster pellets, a fist): their tiles are the old form's.
- **A weapon change** ends the old weapon's lingering objects (they shatter over 8 f), because their tiles leave the
  weapon slot. It is **refused (a buzz) while Rock stands on one of them**, so a swap never deletes the platform under
  you (CX's trap).
- Swapping away from the buster, or changing form, clears the charge (`$9E` = 0).
- **The pause menu** (tech's open question 4, R8.7): vanilla clears slots 1-7 when the menu closes (`$38:$9624`). GP keeps
  that for shots, Beat and Rush but **keeps every utility (slots 4-7) when the weapon is unchanged**, so pausing on a beam
  over a pit is safe. **tech owns the patch** of the pause-close clear at `$38:$9624` (R8.7; §15.2); this doc owns the
  rule. A weapon change in the menu ends the old weapon's utilities like a SELECT change; a menu is a
  deliberate act, so it is not refused there, and the M.BEAM help page says so. Deaths clear everything (vanilla).

Config: **SELECT SWAP = FULL / WEAPONS ONLY / OFF** (OFF for players who want vanilla feel; `meta.md` places it).

### 1.2 SYS-CTL-2: last-weapon toggle [new-code] S, Must (v0.1)

- A SELECT press released within **15 frames (tune)** with no D-pad edge swaps the current weapon and `LASTW`.
- `LASTW` is written by every weapon change: the cycle, the pause menu, the toggle itself.
- If `LASTW` is no longer owned (W2's bracket rush can withhold weapons), the toggle goes to the buster.
- Holding SELECT longer than 15 frames with no D-pad does nothing. It is safe to "rest" on SELECT.

### 1.3 SYS-CTL-4: quick form swap with the 2 KB stream [new-code] M, Must (v0.5, M5: R8.2); [new-art] 1 tile

**R8.2:** a new file owns no forms (Power comes with the 2nd win), so the slice cannot reach the swap; it is built at M5
with the Power and Jet rows of the dispatch table (§3.0) and the adaptors (§2.3).

**Vanilla** [code, r2]: closing the pause menu with a form (`$38:$93F7`) resets the weapon to the buster (`$0699` = 0),
plays sound `$33` and runs the docking sequence `$38:$965F`; the menu-close path then loads the form's sprite set from
`$38:$96C7` = `00 02 03` (Normal set `$00`, Jet set `$02`, Power set `$03`: 128 tiles each at sprite `$00-$7F`, all in
bank `$00`) and, if a weapon is equipped, that weapon's set from `$3F:$F70C` (`$38:$95CC-$95F5`). Sets `$02` and `$03`
differ from the normal sheet in **119 of 128 positions** (104 in `$00-$70`, all 15 in `$71-$7F`), so a form change is a
whole-sheet load (feasibility-7, consistency-5). Poking `$9B` alone shows garbled sprites (`rm6/cheats.md`). GP drops
the buster reset and, after the first time, the cutscene.

**The swap** (R2.3: 16-20 frames behind the flash; CHR-RAM stays 8 KB):

| Frame | What happens |
|---|---|
| 0 | `$9B` = new form. Physics switch at once. The charge is cleared. Slot-0 shots are deleted. The OAM builder skips slot 0 while `SWAPSTATE` ≠ 0, and a **swap-flash** effect (tech's family `$FD`, one GP-COMMON tile drawn 4-way mirrored as a 16×16 burst, sprite palette 0) is drawn over Rock |
| 1..n | tech's CHR stream copies the new sheet's **113 body tiles** (`$00-$70`, 1,808 B), then the **slot set** (`$71-$7F`, ≤ 240 B, §1.4) |
| n+1 | Rock is drawn again with the new tiles; the flash fades over 4 frames |

Stream time at tech's rates (`tech.md` §15.3, the unrolled copier in ROM: 192 B on a still frame, 96 B with a column
paint, 32 B with a full VRAM buffer) for 2,048 B:

| Situation | Stream frames |
|---|---|
| standing still | **11** |
| walking (a scroll column about every 5 frames) | **≈ 13** |
| a column painted every frame (fast autoscroll) | ≤ 22 |
| with tech's 8-line blank band (256 B/frame, Could; the M1 spike's test 5) | 8 |

**The swap is a fixed 16 frames** (R2.3: 16-20 behind the flash): Rock reappears at frame 16, or on the frame after the
stream ends if that is later (only the every-frame-column case, ≤ 22). A constant length reads better than a variable
one, and the flash hides every partial sheet.

Rules:

- **No i-frames during the swap.** Otherwise swap spam would be invincibility.
- **The cooldown is "until the stream completes"**, not a fixed count (consistency-5). A press during a stream is
  queued, one deep.
- The swap is queued behind any CHR stream already running (pop-up glyphs, a boss pinch set): one stream at a time.
- Not allowed: on a ladder (`$94` = 4), in knockback, while sliding, while a set-piece sheet is active (§1.4), during a
  boss bar fill, while playing Break Man.
  - In Jet flight a swap out of Jet is allowed: Rock falls with his current Y speed.
  - A swap into Jet in mid-air may fly at once if the fuel `$9C` > 0.
- The fuel `$9C` and its regen keep running in every form. Vanilla's HUD routine `$3E:$CF90` already refills it
  whenever Rock is not flying.
- **First use of each form per save** plays the vanilla Rush-docking sequence (`$38:$965F`) once, as a "transformation
  debut". After that only the quick path runs. Cost: one FORM_DEBUT bit per form (`meta.md`). The debut clears player
  slots 1-4 and uses slots 6-7 for its Rush objects [code, r2: stores at `$38:$9663`, `$9659`, `$97CD`], so it ends
  any GP utility object; that is accepted for a once-per-form event.
- The pause-menu form selection uses the quick path too. Under 1993 RULES (Could) it always plays the vanilla cutscene
  (§13.6).
- **The swap-flash tile**: 1 tile in GP-COMMON (§15.3 art asks), mirrored 4 ways.

### 1.4 The weapon slot `$71-$7F`: one owner per form (SYS-CTL-4) [new-code] S, Must (v0.1 for Normal form's weapon sets; the per-form map v0.5, R8.2)

R2.3 asks for a per-form `$71-$7F` map. The facts [code, r2]:

| Set | Loaded by | Sprite tiles |
|---|---|---|
| `$00` Normal, `$02` Jet, `$03` Power | the form (`$38:$96C7`) | `$00-$7F`: body `$00-$70` **and** a 15-tile slot set `$71-$7F` |
| `$57` | Y.SPEAR (slot 1) | 2 at `$71-$72` |
| `$5D` | W.STORM (slot 2) | 15 at `$71-$7F` |
| `$58` | B.ATTACK (slot 3) | 3 at `$73-$75` |
| `$59` | F.BLAST (slot 4) | 9 at `$76-$7E` |
| `$5A` | PLANT.B (slot 5) | 1 at `$71` |
| `$5C` | KNIGHT.C (slot 6) | 2 at `$77-$78` |
| `$5B` | SILVER.T (slot 7) | 5 at `$72-$76` |
| none | C.FLASH (slot 8) | (no projectile) |
| `$29` (bank `$02`) | BEAT (slot 9) | 15 at `$71-$7F` |

**The rule: `$71-$7F` has exactly one owner at a time.**

| Form (sheet) | `$00-$70` | `$71-$7F`, slot 0 equipped | `$71-$7F`, weapon w equipped |
|---|---|---|---|
| NORMAL (set `$00`) | normal body | the normal sheet's slot tiles (buster pellets and charge shots) | weapon w's set |
| JET (set `$02`) | Jet body | the Jet sheet's slot tiles (its buster) | weapon w's set |
| POWER (set `$03`) | Power body | the Power sheet's slot tiles (the fist) | weapon w's set |
| SUPER (new sheet, `art_audio.md`) | Super body | the Super sheet's slot tiles (tap fist and rocket fist, ≤ 15) | weapon w's set |
| a set-piece sheet (venue) | the set-piece poses | the sheet's own buster tiles | none: buster only |
| Break Man (Should) | his body | his shot tiles | none: buster only |

Consequences, all Must:

- **Taps never need two owners.** With a weapon equipped, B fires the weapon in every form; slot 0 (buster or punch)
  is only usable with slot 0 equipped. So "forms fire every tap" fits the 15 tiles.
- **A weapon change streams one slot set** (≤ 240 B: 2 frames still, 3 while scrolling); B is ignored until it lands.
- **The Ice Block** (the one v1.0 alt) adds 4 tiles to B.ATTACK's set: GP's B.ATTACK set is 7 tiles at `$73-$79`.
- **Beat's pit rescue** (§10) streams set `$29` (Beat, 15 tiles) at its locked moment and restores the slot set when Rock
  lands. It ends the weapon's lingering objects first.
- **Set pieces that change Rock's body** (Wind's sortie, Yamato's pogo rack) use a **dedicated 128-tile set-piece
  player sheet** streamed at a locked moment (a catapult, a cutaway), never the weapon slot (R2.3, feasibility-8).
  Systems provides `gp_player_sheet(id)` and `gp_player_sheet_end()` on the same stream as the form swap (M5, with
  Yamato's pogo); while a sheet is active only the buster fires (its tiles are in the sheet) and the SELECT form cycle is
  off.
- **The attach state** (tech's; Blizzard's condor, Plant's vines and balloon) needs no sheet: Rock uses vanilla's
  ladder-climb and ladder-shoot poses. On the grab the weapon switches to the buster, only the buster fires and SELECT
  is off; the equipped weapon returns on release. This is the venue docs' "buster only on vines and the condor" rule
  (consistency-43). **R8.2:** the attach state's core is built at M3 with the condor (Blizzard's secret exit) as its
  first user, so this rule is in the slice; vines (T5) and the balloon follow at M5.
- **artcheck rejects any weapon-slot set over 15 tiles** (R2.3) and any non-weapon object that draws from `$71-$7F`.

Free tiles per weapon set for the Should alts and synergies (15 − set size): Y.SPEAR 13, W.STORM 0 (its Updraft and
Tailwind must re-pack the tornado set), B.ATTACK 8 after the Ice Block, F.BLAST 6, PLANT.B 14, KNIGHT.C 13, SILVER.T 10,
C.FLASH 15, M.BEAM 15 minus its beam tiles. **A synergy (Should) names one combined set per (form, weapon) pair, ≤ 15
tiles**, holding both the weapon's and the synergy's tiles (Burning Knuckle = F.BLAST's 9 + at most 6 knuckle tiles).

### 1.5 SYS-CTL-3: controller-2 pseudo L/R [new-code] S, Should

The 4MI precedent: controller 2's A/B cycle weapons.

| P2 input | Action |
|---|---|
| A | next weapon |
| B | previous weapon |
| A+B (both held on the same frame) | buster |
| LEFT / RIGHT | previous / next form |
| UP | last-weapon toggle |

- A Famicom pad II has A/B and the D-pad but no SELECT/START, so everything above is reachable on real hardware.
- Emulator users can bind P2 A/B to shoulder buttons.
- Config **2P SHIFT = ON (default) / OFF**.
- Vanilla never consumes `$41/$43` (`tech.md` §15.4), so no guard is needed.

### 1.6 SYS-CTL-5: input rules [new-code] S, Must (v0.1)

- **Alternate fire = UP+B**: a B press edge while UP is held. "Hold" alts (KNIGHT.C, M.BEAM's magnet) are Should.
  On a ladder only the tap fires, because UP means "climb" there. RM6 has no up-aim, so UP+B steals no shot.
- **Interaction** (R2.10, design-21): one predicate, tech's macro `IFINTERACT`, used by every door, scroll, sign, NPC,
  plaque and T3 door target in every stage:

  ```
  IFINTERACT = (UP edge in $42) and (B not held in $40) and (ALT_LOCK = 0)
  ALT_LOCK   = 10 on every alt fire, minus 1 per frame        (a SYS_HOT byte)
  ```

- **Pause menu**: Break Man's call is a pause-menu **row confirmed with A** (Should, with the partner). On the CHIPS
  page, **B opens the selected chip's help page** (a 4 × 28 window, `story.md` §8's text). SELECT does nothing there.
- **Mash, reflex and timer rules** (shared by every stage; the CASUAL lever list of §13.4). This doc owns the numbers;
  tech's macros apply them (`tech.md` §5.5: `TIERVAL casual, normal, hard` reads a 3-value table by `LAYOUT_TIER`, 1993
  using NORMAL; `MASH n` is the struggle helper). Reflex windows add INPUT_LAG at run time (a `REFLEX` macro = `TIERVAL`
  + `INPUT_LAG`, asked of tech):

  | Rule | NORMAL | CASUAL | HARD (v1.0) |
  |---|---|---|---|
  | mash: presses of A or B in the window (`MASH n`) | n | ⌈0.6 n⌉; **holding A or B also counts one press per 6 f** (hold-to-struggle, tech's figure, tune) | n |
  | reflex: a reaction window in frames (`REFLEX`) | n + INPUT_LAG | 2n + INPUT_LAG | n + INPUT_LAG |
  | timer: a set-piece timer in frames (`TIERVAL`) | n | ⌈1.5 n⌉ | n |
  | the quick-draw window (SC8, R3.5) | 24 + INPUT_LAG | 40 + INPUT_LAG | 18 + INPUT_LAG |

  Per-stage HARD values are Should (cut-line 3); the quick-draw's HARD 18 f is the one HARD number R3.5 sets for v1.0.
- **INPUT LAG** (R3.5): a global CONFIG setting, **0-6 frames, default 0**, added to every reflex window (never to
  mash counts or timers). `meta.md` places it in the system block and the CONFIG page; `story.md` writes its line
  (intent: "ADD FRAMES TO EVERY QUICK REACTION. SET IT TO YOUR TV'S LAG.").

---

## 2. Forms and physics

### 2.1 Vanilla numbers (the ground truth)

| | Normal | Jet (`$9B` = 1) | Power (`$9B` = 2) | Source |
|---|---|---|---|---|
| Walk | 1.297 px/f (`$01.4C`) | same | same | engine.md §3.2 |
| Jump | stored vy `$FA.CC` (-5.20 px/f), gravity +0.25 px/f², peak 51 px, 42 f airtime | same start, then flight while A is held | same as normal | ram.md, critic |
| Slide | DOWN+A, 2.5 px/f, 40 px in 16 f | none | none | engine.md |
| Charge `$9E` | +1/f; half at `$24` (36 f), full at `$5A` (90 f, `$06AB`) | none (always shot `$09`) | +2/f, full in 45 f | `$38:$8651`, table `$38:$854A` = `09 0A 0B 09 / 09 09 09 09 / 0C 0E 0F 09` |
| Shot types and attack bytes [code, r2] | `$09` tap `$11`, `$0A` half `$11`, `$0B` full `$13` | `$09` `$11` | `$0C` tap `$12`, `$0E` half `$13`, `$0F` full `$14` | `objtypes.json` AI headers |
| Fuel `$9C` | regenerates | 19 units; −1 per 4 f of flight (76 f full tank); +1 per 2 f when not flying, even in mid-air | regenerates | engine.md |
| Flight [seen, ds] | | holding A from the floor: Y 175 → 42 (133 px) in ~70 f, holds height, then falls at −1. Fuel back to 19 about 40 f after landing. **Pulsing A (4/2, 6/2, 8/4, 3/3 frames) never sustains altitude**, so vanilla has no infinite-hover exploit | | `jet.py`, `jet2.py` |
| Punch [seen] | | | fist appears 6 f after B at +21 px, flies 4 px/f to +81 px, holds ~10 f, gone at 32 f; hits 16-80 px | engine.md `punch.py` |
| Hurt [seen, ds] | 30 f knockback state at 0.5 px/f (14 px), then 60 f of blinking i-frames (2 on / 2 off): **90 f of safety per hit**. Power form identical | | | `dbg2.py` |

Floor types (`$064B` / latch `$A7`):

| Type | Floor | Effect |
|---|---|---|
| 5 / `$15` | ice | momentum `$A1.$A0`, ±`$00.06` per frame; 24-36 px of slide after letting go |
| 9 | oil | jump `$FB.CC` (−4.20 px/f, peak ≈ 35 px), walk 0.5 px/f |
| 8 | water | gravity `$00.18` |
| A / C | updraft / fan | |
| E | blocks Jet thrust | |
| 6 | ship deck | |

### 2.2 What GP changes, per form

**NORMAL** [engine-ok]: unchanged. It stays the reference feel and the only form with a slide and a charge buster.

**POWER** (after the 2nd win, SYS-FRM-2):

- Walk, jump and charge as vanilla. The punch keeps its reach, timing, **shot types and attack bytes** (`$12/$13/$14`,
  R2.1). It is **not** re-classed: the 21 enemy AI sites that compare the latch with `$14`, `$13` or `$1A`
  (feasibility-5's scan, re-run for round 2) keep working untouched. Its scoring category and boss column come from
  LATCHSRC (§6.4).
- With a weapon equipped, B fires the weapon's tap. The punch is the Power form's slot 0.
- **SYS-FRM-3 Parry** [new-code] M, **Could** (R2.4). Vanilla precedent: the full punch rebounds projectiles in Wily 1 as
  player objects `$DA/$E4`, attack `$1A` (engine.md §1.2). GP would generalise it:
  - In the class-4 handler `$38:$9028` (enemy bullets, which writes no latch [code, r2]), a punch fist of any level
    that touches a bullet not listed in a NOPARRY type table replaces it with a reflected `$DA`-style object.
  - The reflected object reverses the bullet's velocity at 1.5× speed; its LATCHSRC column is PARRY (2/20 on bosses).
  - Feedback: a "ting" SFX and a 1-sprite spark. Rock gets 12 i-frames without blinking (tune).
  - NOPARRY holds beams, big boss bodies and anything a venue marks. The first parry per stage is a STYLE act.
- **SYS-FRM-4 Ice grip** [new-code] S, Could. On type 5/`$15` floors Power's momentum decays at 2× (`$00.0C`/f), so it
  slides 12-18 px instead of 24-36. The "heavy form" identity for the Blizzard venue. (SNOW CHAINS does the full grip.)

**JET** (after the 4th win):

- Keep the 19-unit stamina bar exactly. It is not exploitable (measured above), so the BRIEF's overheat stall adds
  nothing and is **Won't**.
- Jet still cannot charge (the buster always fires `$09`).
- With a weapon equipped, B fires the weapon's tap in flight.
- **SYS-FRM-6 Low-fuel pip** [new-code] S, Should. When the weapon bar shows a weapon (not fuel), fuel is invisible. A
  single pip under Rock blinks when `$9C` < 5 (20 frames of flight left), built on tech's HUD widget module (R1.10). With
  the buster equipped, the weapon bar shows fuel as in vanilla (`$3E:$CF90`).
- Floor type E keeps blocking thrust. It is the venue designers' anti-Jet tool, and they should use it to protect
  intended routes.
- Air-dash (the PLAN idea) is **Won't (v1)**: it needs double-tap detection and fights with the SELECT filter.

**SUPER** (H3 reward, SYS-FRM-5) [new-code] L, Must with H3 (v1.0); [new-art] the Super Rock sheet (`art_audio.md`):

The design rule from PLAN: weaker than each specialist, no gauge.

| | Super | Compared with |
|---|---|---|
| Walk / jump | Normal's (1.297, `$FA.CC`) | |
| Slide | no | Normal |
| **Jet hop** | the second A press in the air (once per airtime): vy := `$FC.40` (−3.75 px/f), ≈ +28 px. Max height ≈ 51 + 28 = **79 px (tune)** | Jet: 133 px |
| Tap B (slot 0) | a short punch, attack `$12` (2 to mooks), column PUNCH | |
| **Rocket fist** (hold B, +2/f, full at 45 f like Power) | flies straight ahead at 5 px/f up to 112 px or until it hits, then **homes back** at 6 px/f, re-aiming at Rock each frame with ±2 px/f of lateral correction. Outward leg: attack **`$14`**, a **full-power blow** (4 to mooks; it opens punch-only enemies and passes Knight's shield, exactly as vanilla treats `$14`, and it calls the full punch's cracked-block routine for `$B`); return leg: attack `$12` (2). Column FIST on both legs. One fist at a time | Power full punch: 4 to mooks, reach 81 px |
| Weapons | all taps, no synergies (the 8 synergies are Power or Jet only, and Should) | |

The homing return lets the fist hit an enemy *behind* Rock on the way back. That is the trick H5 and Super Wily Castle
can build rooms around. Super arrives only after H3's Gamma, which is a Power test (SC5).

**Prerequisite** (R1.12, feasibility-14): SUPER is `$9B` = 3. About 30 executed-code readers of `$9B` index tables sized
for 3 forms; for example the shooting-pose table `$3F:$E130` has exactly three 8-byte rows (`18 18 0c ff 0f 0f 08 08 /
1f 1f 1e ff 2f 2f 26 67 / 34 34 34 ff 22 22 33 33`) followed by code (`A9 00`) [code, r2], so form 3 would read
instructions. `tech.md` audits every `$9B` reader (static scan plus coverage) and relocates those tables with a fourth row
**before** SUPER becomes form 3 (M7, before H3). The fortress fist-ride and SC5 do not depend on SUPER.

### 2.3 SYS-FRM-2: acquisition [new-code] S, Must (v0.5, M5: R8.2)

Per BRIEF §4 (a new file owns no forms, so the slice has none; this lands at M5 with the form swap, R8.2):

- `$38:$931D` (menu) and `$3B:$BA3F` (stage start) derive the forms from `meta.md`'s **FORMS** save bits instead of the
  Plant and Flame flags. FORMS.POWER is set when WINS reaches 2 and FORMS.JET at 4, by the bracket's hand-over events
  (`meta.md` EVENTS b0/b1). WINS = the number of venue champion flags set.
- **FORMS.SUPER is set when Rush docks in H3 screen 12, with no YOU GET card** (consistency-28: story's rule that
  adaptors are never announced on YOU GET; fortress's demo walk-out right after needs the bit already set). Roll's map
  scene (`story.md` S29, `meta.md` EVENTS2 b4) follows on the next bracket visit.

The announcer celebrates each new form at the next stage start (`story.md` writes the line).

### 2.4 The normal-route rule (shared with the venue docs and fortress)

**A normal exit never needs a form, an alt fire, a synergy, Break Man, or any Should or Could item.** Secret exits,
hidden rooms and venue chips (Must) may need forms, taps and the Ice Block. Anything that needs another alt, a synergy
or Break Man needs a fallback that works without it (R0.4): TAG rooms become full-charge doors (R4.2), and keys that
want Time Stop wait for the alts (R3.1).

- It keeps the sequence free: forms arrive by count, so any venue can be first.
- It keeps 1993 RULES (Could) finishable when it is built.

**Two exceptions, both ruled:**

1. **POWER, owned from the 2nd win, may be required in the fortress, with a tell** (R2.11, design-3, consistency-12).
   In v1.0 that is exactly one place: **Gamma MK-VI phase 2 (SC5)**. Its plaque is the tell, and H3 adds a no-risk
   fist-ride practice beat before the fight (fortress stages it). The Super Adaptor is not lent.
2. **The Magnet Beam, from H1 on** (fortress §0.2).

**Vehicles are not forms** (consistency-36). A stage-lent vehicle (SKY ACE's sortie, with Rush in a RENTAL bib; the
Exhibitions' CANNON if they return) is tech's one free-flight vehicle state (R1.10), not `$9B`: it is NO TAG, works
under 1993 rules, and gives no form-based VARIETY.

---

## 3. The weapon roster

### 3.0 Rules shared by every weapon

- **Tiers** (R2.4, scope-8, design-6). **Must: every form fires every weapon's tap.** The dispatch table has alt and
  synergy columns from day one. **Should (v1.1, cut-line item 1): the 8 alts and 8 synergies, added one weapon at a
  time** (order in §3.12), except **B.ATTACK's Ice Block, which ships in the Blizzard slice** as the prototype for alt
  dispatch and the frozen tick. Bosses may preview their weapon's alt as a boss move: that is AI, owned by the venue
  docs, not player code.
- **Inputs.** Tap = B. Alt = UP+B (§1.6), or "hold B" where stated. A synergy is what the tap or hold becomes in the
  named form; in the other forms the weapon behaves as in Normal.
- **Dispatch** (SYS-FRM-1) [new-code] M, Must.
  - Vanilla's fire jump table `$38:$856A` (lo `$8556`, hi `$8560`, indexed by `$0699`) becomes a **weapon × {tap, alt,
    synergy}** table of 3 × 10 entries. In v1.0 the tap column is vanilla's routines, the alt column holds only the Ice
    Block (others point at the tap), the synergy column points at the tap. Adding a Should behaviour is one entry plus
    its object.
  - Vanilla forms cannot fire weapons only because the menu resets `$0699` when a form is chosen (`$38:$93FE`) [code,
    r2]; GP removes that reset, and the fire routines use the form's shooting pose from `$3F:$E130[form*8 + $94]`
    (relocated with a 4th row for SUPER, §2.2).
  - **Rungs (R8.2):** the table itself, with Normal form's tap column and the Ice Block in the alt column, is built in
    the slice (M3). **The Power and Jet rows** (the buster-reset removal and the form shooting poses above) move to M5
    with the form swap: a new file owns no forms, so the slice cannot reach them.
  - The vanilla fire routines (`$8582` one at a time in slot 3, `$857A/$857E` two in slots 2-3, `$85D9` spreads that
    need slots 1-4 empty) are kept for the taps.
- **Player-side object slots** (R1.11, feasibility-9; tech owns the plan, `tech.md` §7.12): slot 0 is Rock (Break Man
  is a slot-0 character variant, Should); **shots use 1-3** (the vanilla allocator `$3F:$E514`; the spreads also take
  4, as in vanilla); **utilities** (persistent player-side objects) take one slot each in 4-7 through tech's
  `util_spawn`, which tries 5, 7, 6 (the underwater bubble's slot), then 4 (Beat's and Rush's). This doc sets **the caps
  per weapon so they fit**:

  | Utility | Cap | Tier |
  |---|---|---|
  | the Ice Block (thrown, landed or shelling an enemy) | 1 | Must |
  | M.BEAM beams | 2 | Must |
  | the CENTURION bot (boss fights only) | 1 | Must |
  | Wall Spear, Updraft column, Flare column | 1 each | Should |

  At most 4 utilities exist (fewer while Beat or Rush is out, or underwater). If `util_spawn` finds no slot, the weapon
  buzzes and spends no energy. Beat's pit rescue reuses slot 4 (R1.11). Utilities that deal damage call the shot-vs-enemy
  routine `$38:$8FDF` themselves. Utilities that are platforms (the landed Ice Block, beams) need **the player-contact
  search extended to slots 4-7** for platform contact only: vanilla's `$38:$8EA0` tests enemy slots through `$3F:$ECCD`
  [code, r2]. [new-code] S, tech registers the hook.
- **Energy** is spent through vanilla `$38:$9E8E` on the first frame (bar = 28 units, `$00-$1B`). A weapon at 0 can't
  fire. The ENERGY SAVER chip halves costs (§9).
- **Normal-enemy damage** = the low nibble of the shot's attack byte (vanilla `$3F:$E9D7`). The taps keep their vanilla
  bytes; new objects use their weapon's class nibble.
- **Boss damage** comes from §4 through the LATCHSRC column (§6.4). An alt or synergy uses its weapon's cell unless
  stated.
- **LATCHSRC** carries the column plus three flags: FULL (a full-power blow), ALT, SYN (§6.4). Alts and synergies count
  for their weapon in VARIETY.
- **Help pages** (4MI lesson: one per weapon from day one) are `story.md`'s words; each section gives only the page's
  intent.

### 3.1 R.BUSTER (slot 0) [engine-ok] S, Must

| Level | Hold | Shot (vanilla type) | Attack byte | Mook dmg | Boss column |
|---|---|---|---|---|---|
| tap | - | `$09` | `$11` | 1 | BUSTER |
| half | ≥ 36 f (`$24`) | `$0A` | `$11` (vanilla) | 1 | BUSTER |
| full | ≥ 90 f (`$5A`) | `$0B` | `$13` | 3, flies on through what it kills (vanilla) | CHARGE (FULL) |
| Jet form | no charge | `$09` | `$11` | 1 | BUSTER |

- Up to 3 tap shots on screen, as in vanilla.
- **The half charge stays vanilla** (`$11`, 1 damage). Round 1's bump to `$12` would have changed a vanilla attack byte,
  which R2.1 rules out: Won't (v1).
- CHARGE KIT (§9) moves the thresholds to 24 / 60 frames.
- A held charge survives the pause menu (vanilla, measured by the critic).
- `$13` is also the Power half punch's byte (vanilla). Objects that react to "a charged shot" test the FULL flag in
  LATCHSRC, or `$13`/`$14` if they are vanilla AIs (§6.4).

Help intent: hold to charge; a full charge flies through what it destroys; the judges call it "reliable".

### 3.2 Y.SPEAR (Yamato, slot 1)

Vanilla: shot `$81`, attack `$52`, one at a time, cost 1, mook 2, set `$57` (2 tiles). It is Knight Man's weakness, and
**it already passes class-3 shields** in vanilla: `$38:$90A9` tests the class nibble `$50` before the facing test
[code, r2]. SC1 lists it.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Spearhead straight ahead (vanilla) | 1 | 2 | **Must** |
| Tap polish: pierce | | The spear passes through the first enemy it does not kill, then stops on the next (a GP branch in `$38:$9067`'s vanish path) | | | Should |
| Alt: **Wall Spear** | UP+B | A thrown spear that sticks in the first wall it reaches and becomes a 16×8 **one-way platform** (class 9 contact) for 240 f (tune). Max 1 (a utility). If it hits an enemy first, it deals 2 and makes no platform | 3 | 2 | Should |
| Synergy: **Pogo** (Power) | hold DOWN in the air | Rock rides the spear point-down (the DuckTales pogo; Capcom, 1989). **On an enemy**: 3 damage and a bounce (vy `$FB.00`, or `$FA.CC` with A held). **On spikes**: a safe bounce that costs 1 energy per bounce; at 0 energy spikes kill as usual. On a boss: the Y.SPEAR cell. On the floor: a normal landing. The pose uses Power's crouch frames with the spear under the feet, so it needs no new body tiles (§1.4) | 1 per spike bounce | 3 | Should |

Tags: tap [engine-ok]; pierce [new-code] S; Wall Spear [new-code] S, [new-art] 2 tiles; Pogo [new-code] M, [new-art] 2
tiles in the Power + Y.SPEAR synergy set.

Help intent: UP+B leaves a spear in the wall; in Power form, hold DOWN in the air; spikes are a problem only without one.

### 3.3 W.STORM (Wind, slot 2)

Vanilla: `$82`, attack `$62`, cost 1, mook 2, set `$5D` (15 tiles). It is Flame Man's weakness. Wind Man takes only one
hit from it per vanilla quirk (stages_b.md). A W.STORM hit that kills a standard enemy blows it up off the screen
(`$3F:$EB8B`, the class-6 entry of the hit-effect table `$EBB5/$EBC5`) [code, r2].

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Vanilla tornado. **On a frozen enemy it thaws it** (it blows the ice away, §4.8) | 1 | 2 | **Must** |
| Alt: **Updraft** | UP+B | A 16×64 updraft column in front of Rock for 150 f (a utility). Inside it Rock's gravity becomes −0.5 px/f² until vy reaches −2.0 px/f, so he rises to the column top: a Normal-form climbing tool, the same idea as the vanilla updraft floor types A/C. Enemies inside take 1 per 8 f | 3 | 1 / 8 f | Should |
| Synergy: **Tailwind** (Jet) | B in flight | The tornado peels off behind Rock. For 90 f the fuel does not drain and the flight X speed is ×1.5 | 4 | (2 to what the tornado hits) | Should |

Tags: Updraft [new-code] S, [new-art] 4 tiles (the tornado set must be re-packed: it has 0 free); Tailwind [new-code] S.

Help intent: UP+B makes a column of wind you can ride; in flight it pushes you instead; Wind Man says it was his idea.

### 3.4 B.ATTACK (Blizzard, slot 3)

Vanilla: `$83` spawns 4 × `$8E` in a spread, attack `$72`, cost 3, 2 per flake, set `$58` (3 tiles at `$73-$75`). It
needs player slots 1-4 empty. It kills the fire robots `$2A/$2C` outright (thematic table). It is Plant Man's weakness.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | 4-flake spread (vanilla) | **2** (vanilla 3) | 2 per flake | **Must** |
| Alt: **Ice Block** (SYS-WPN-3A) | UP+B | below | 2 | 1, plus the freeze | **Must (the slice)** |
| Synergy: **Snow Bomb** (Jet) | B in flight | The 4 flakes fall straight down in a 32-px spread at 3 px/f | 2 | 2 per flake | Should |

The cost cut from 3 to 2 (data only) is because the flakes no longer stack on bosses: i-frames eat the extra flakes. The
weapon is judged by its crowd value.

**The Ice Block** [new-code] M, [new-art] 4 tiles (GP's B.ATTACK set = 7 tiles at `$73-$79`), Must (v0.1). venues_b's
proposal, merged with an encase effect, and the prototype for every later alt:

- **Throw.** A 32×16 ice block lobbed forward as a utility (`util_spawn`; vx 2 px/f, vy −3 px/f, gravity 0.25 px/f²;
  tune). One at a time. It is drawn from the weapon slot in sprite palette 1 (black outline, white body), so its look does not depend on
  the weapon colours. LATCHSRC = B.ATTACK + ALT.
- **On a normal enemy whose `FRZ_KIND` is not NOFREEZE** (§4.8): it deals 1 through `$38:$8FDF`, then **encases** it for
  **150 f (tune)**: `FREEZE,X` = 150; the enemy's class nibble in `$0583,X` is saved in `ENC_CLASS,X` (a per-slot WORK
  byte) and set to **9**. Class 9 is vanilla's solid platform for the player (`$38:$8F96`), so **Rock can stand on it**
  and touching it is harmless; shots still hit it through `$38:$9067`; and it **keeps taking damage** (R2.2). The block
  becomes the shell, glued to the enemy and drawn over it. At thaw or death the class is restored and the shell shatters.
- **On a NOFREEZE enemy**: it deals 1 and shatters. Fire enemies die (the vanilla thematic table reads class 7).
- **On a boss**: 1 damage with 30 i-frames (the ALT override row of GP_BOSSHIT, §4.8), never frozen.
- **The 1 damage comes first**, so an enemy with 1 HP dies instead of being encased. A stage doc that wants an enemy to be
  an ice step gives it at least 2 HP: Blizzard's bird has 2 for this (venues_b §1.7).
- **Otherwise it lands** as a solid 32×16 block for 240 f, blinking the last 30 f.
- **A weapon change shatters it** (and thaws the enemy), and is refused while Rock stands on it (§1.1).
- STYLE: the FROZEN STEP act (stood on an encased enemy).
- Should (with Flame's revisit content): **on burning oil** it freezes the strip into ice for 300 f through tech's
  map-edit service, and the landed block's top is slippery (ice momentum).

Help intent: UP+B throws a block of ice; whatever it lands on holds still and holds you up; please wipe your feet.

### 3.5 F.BLAST (Flame, slot 4)

Vanilla: `$84`, attack `$84`, cost 1, mook 4, set `$59` (9 tiles). It breaks collision `$D` and kills the snow robot
`$4D` outright. It is Blizzard Man's weakness.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Vanilla fireball → floor pillar. **It ignites oil** through `$3E:$DDFC`, made explicit GP behaviour whatever vanilla does (consistency decision 35). Enemies killed by oil the player lit score as HAZARD | 1 | 4 | **Must** |
| Alt: **Flare** | UP+B | A 16×80 fire column straight up from Rock for 20 f (a utility); 2 per 8 f to enemies. It melts F.BLAST blocks (`$D`) above, and lights "fuse" objects that venues may place | 2 | 2 / 8 f | Should (late, §3.12) |
| Synergy: **Burning Knuckle** (Power) | hold B (45 f, like the punch), release | A flaming full punch: attack `$84` (F.BLAST cell) with the FULL flag. It breaks both `$B` and `$D` blocks and ignites oil it touches. A tap in Power form still throws a normal fireball | 2 | 4 | Should |

Tags: Flare [new-code] S, [new-art] 3 tiles; Burning Knuckle [new-code] S, [new-art] ≤ 6 tiles (F.BLAST's 9 + 6 = 15).

Help intent: UP+B sets the ceiling on fire; in Power form, hold B; fire insurance not included in the entry fee.

### 3.6 PLANT.B (Plant, slot 5)

Vanilla: `$85` spawns 4 orbiting leaves `$8D`, attack `$94`, cost 4, mook 4, set `$5A` (1 tile). One contact removes all
four (`$38:$9034` clears slots 1-4 [code, r2]); it deletes enemy bullets (class 4, `$38:$9028`). It does **0 to every
boss but Tomahawk** in vanilla.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Orbiting barrier as in vanilla. Against bosses it now does its PLANT.B cell (§4.3) instead of vanilla's 0: the BRIEF's "every weapon useful" comes free with GP_BOSSHIT | **3** (vanilla 4) | 4 | **Must** |
| Tap polish: 2 contacts | | The barrier survives 2 contacts (enemy or bullet) instead of 1 and lasts until broken or 600 f (tune): a GP branch at `$38:$9034` | | | Should |
| Alt: **Petal Shot** | UP+B while a barrier is up | The 4 leaves fly off in a forward fan (±15°, ±35°) | 0 (spends the barrier) | 2 each | Should (late, §3.12) |
| Synergy: **Petal Storm** (Jet) | B in Jet form | Radius ×1.6 (tune). For 180 f bullets are deleted without breaking it; it breaks after 3 enemy contacts. Built for bullet-curtain set pieces | 4 | 4 per contact | Should |

Tags: [new-code] S each.

Help intent: two hits now, by popular demand; UP+B throws the petals; in flight, it blooms.

### 3.7 KNIGHT.C (Knight, slot 6)

Vanilla: `$86`, attack `$A3`, cost 1, mook 3, two on screen, set `$5C` (2 tiles). It is Centaur Man's weakness.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | The mace flies out and returns (vanilla) | 1 | 3 | **Must** |
| Alt: **Hold** | keep B held after the throw | The mace stops at its farthest point and hangs there while B is held, then returns. It hits what touches it (3 per 8 f) and **catches pickups and envelopes**, which ride back to Rock (the 4MI Ring precedent) | 1 per 30 f held (min 1) | 3 / 8 f | Should |
| Synergy: **Morning Star** (Power) | B in Power form | A giant 32×32 flail with the FULL flag. It **breaks cracked blocks (`$B`) with no charge** and passes and breaks Knight Man's shield (SC1) | 2 | 4 | Should |

Tags: Hold [new-code] S; Morning Star [new-code] M, [new-art] ≤ 13 tiles.

Help intent: hold B and it waits for you, like a good mace; in Power form, bigger, much bigger.

### 3.8 SILVER.T (Tomahawk, slot 7)

Vanilla: `$87`, attack `$B3`, cost 1, mook 3, two on screen, set `$5B` (5 tiles). It is Yamato Man's weakness, and the
Wily Machine's and the Capsule's.

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Thrown in an upward arc (vanilla) | 1 | 3 | **Must** |
| Alt: **Feather Fan** | UP+B | Three feathers (Tomahawk Man's own attack) fanned at 30°/45°/60° up-forward; needs slots 1-3 empty | 1 | 2 each | Should (late, §3.12) |
| Synergy: **Dive Throw** (Jet) | B in flight | Thrown 45° down-forward at 1.5× speed | 1 | 3 | Should |

Tags: [new-code] S, [new-art] feather 2 tiles.

Help intent: UP+B throws three feathers; from the air it goes down, which is where the enemies are.

### 3.9 C.FLASH (Centaur, slot 8; vanilla spelling C.FLRSH kept on the YOU GET card, BRIEF §6)

Vanilla: `$88` (`$38:$9E52`) spends 4 energy, writes `$C4` straight into the latch of every object of class 1, 3 or F
in slots 8-`$15` (`$38:$9E74`), strobes the palette, then waits 16 f. It does 0 to every boss but Wind Man.

**The vanilla strobe breaks the R3.5 flash rule** [seen, r2: `cflash_strobe.py`]: `$3E:$DECD` calls `$DEF2` six times,
each turning every non-black BG colour white for 2 frames then restoring it for 2, so the whole screen flashes
**6 times in 24 frames (15 Hz)**. GP replaces it (SYS-FX-1, §5.1).

| | Input | Behaviour | Cost | Mook dmg | Tier |
|---|---|---|---|---|---|
| Tap | B | Screen-wide hit (vanilla latch writes). Bosses take their C.FLASH cell. **The flash is one 4-frame white-out then a 3-step fade** (12 f), and a new white-out is skipped if the last one began < 20 f ago; REDUCED FLASHES uses a 2-step darken instead. **It lights a dark room for 240 f** (tech's lighting service: wherever a stage darkens a screen) | 4 | 4 to all on screen | **Must** |
| Alt: **Time Stop** (Flash Man nod, RM2) | UP+B | For 90 f every frozen-capable enemy (`FRZ_KIND` 1-3 or 5) and every frozen-capable enemy bullet freezes; the frozen handlers keep applying damage. **Bosses stall for at most 45 f** (the boss stall, §4.8), then ignore Time Stop for 120 f. **Centaur Man is immune** (SC2). Darker palette (a darken, not a flash); the music keeps playing | 7 | - | Should (first alt after the slice, §3.12) |
| Synergy: **Time Fist** (Power) | B in Power form | A 60-f Time Stop in which **B is always the punch and every punch is a full punch** (`$14`, FULL) | 6 | 4 per punch | Should |

Tags: tap flash change [new-code] S (SYS-FX-1); Time Stop [new-code] M (needs SYS-CMB-3); Time Fist [new-code] S. The
announcer's "TIME, STOP!" is a `story.md` line.

Help intent: UP+B stops the clock, not his though; in Power form, punch the moment.

### 3.10 MAGNET BEAM (H1 reward, slot 9) [new-code] M, Must (v1.0); [new-art] beam set

Slot 9 was vanilla's BEAT weapon. Beat becomes the pit rescue (§10), so the slot and its energy byte `$0691` are free.
GP's beam set replaces BEAT's set `$29` in `$3F:$F70C`'s slot 9 (≤ 15 tiles; target 6: head, two body tiles, end cap,
two blink tiles), with a new weapon palette in `$38:$962F`. An MM1 tribute and a nod to CX's Instant Floor.

| | Input | Behaviour | Cost | Tier |
|---|---|---|---|---|
| Build | hold B | A beam grows forward from Rock's hand at 4 px/f. On release, or at **64 px**, it freezes into an 8-px-tall solid platform for 240 f, blinks for 30 f and vanishes. **Max 2 beams** (two utility slots, R1.11) | 1 per 16 px (1-4) | **Must** |
| Alt: **Magnet** | hold UP+B | While held, pickups and envelopes within 80 px drift toward Rock at 2 px/f | 1 per 60 f | Should |
| Damage | | none: beams pass through enemies; LATCHSRC column M.BEAM scores nothing | | |

- **64 px per beam is the source of truth** (consistency-17): fortress sizes the H1 gap for one or two beams (two cover
  up to 128 px of gap with a beam's width of standing room each).
- No synergy (the 8 synergies are for the 8 boss weapons). **Emergent and allowed**: Jet + M.BEAM. Land on a beam in
  mid-air and the fuel regenerates. Energy limits it to about 7 beams per bar. Venues that must stop it use floor type E
  (no thrust) or ceilings.
- The beams are platforms through the utility-slot contact extension (§3.0); a SELECT weapon change is refused while
  Rock stands on one, and a pause with the weapon unchanged keeps them (§1.1).

Help intent: hold B to build, let go to stop; two at a time, because the museum only had two in stock.

### 3.11 Break Man's moveset (the tag partner, §11) [new-code] L, Should (cut-line item 2)

His design brief: no forms, a different body, buster only. He is a **slot-0 character variant** (R1.12): a character
byte, his own physics constants, stashed HP, and his sheet streamed at beam-in (§11).

| | Break Man | Rock (for comparison) |
|---|---|---|
| HP | **20** (own bar), full on every call | 27 |
| Walk | 1.50 px/f (`$01.80`) | 1.297 |
| Jump | vy `$FA.4C` (−5.70 px/f) → peak ≈ 64 px | 51 px |
| Slide | yes (Rock's slide code) | yes |
| Tap shot | attack `$11` (1 to mooks), 3 on screen, column BREAK | buster `$11` |
| **Break Shot** | hold B 60 f → a big shot, attack **`$14`** (a full-power blow: 4 to mooks, flies on through what it kills, **breaks cracked blocks `$B`**), column BREAK★ | full charge 90 f, `$13` |
| **Shield** | while airborne and not shooting, enemy bullets (class 4) that touch the front half of his box are deleted (a GP branch in `$38:$9028`); bodies still hurt | - |
| **Double knockback** | knockback 28 px over 30 f (Rock: 14 px). Same 60 f of blink afterwards | 14 px |
| Weapons, forms, chips | none. Body chips (SHOCK ABSORBER, SPIKE GUARD, YASHICHI, SNOW CHAINS, FIREPROOF, CENTURION, DARUMA; the bundle's IRON HELMET) apply to Rock only. Economy chips (ENERGY BALANCER, EXCHANGER, SHERIFF STAR) still work | |

Why buster only: a weaponless body makes the call a change of pace rather than a better Rock; weapon energy stays Rock's
resource; it saves a second fire dispatch; and the Break Shot, the higher jump and the shield earn his keep.

### 3.12 The v1.1 order for the alts and synergies (cut-line item 1)

One weapon at a time, each a self-contained v1.1.x update (object + dispatch entry + cell + help page + tests):

1. **Time Stop** + SC2 (the frozen tick and the boss stall already exist; R3.1's Time Stop keys can then be added).
2. **Wall Spear**, **Updraft**, **KNIGHT.C Hold** (the stage tools venue revisits want most).
3. The synergies, **Pogo** and **Burning Knuckle** first (they have set-piece uses), then Morning Star, Time Fist,
   Tailwind, Snow Bomb, Petal Storm, Dive Throw.
4. **Flare, Feather Fan, Petal Shot** last: no stage uses them as tools (design-6 proposed Could; the ruling keeps them
   Should, at the end of the line).
5. M.BEAM's magnet and the tap polish (Y.SPEAR pierce, PLANT.B's two contacts).

Every one ships with its row in the damage tables (it already has its column) and its smoke movie (§13.7).

---

## 4. The combat model: "the judges like variety"

### 4.1 What vanilla does (measured)

- **Robot Masters** [seen, ds `iframes.py`]: after *every* hit, by any weapon, the boss blinks for **60 frames**
  (`$31:$9A01 LDA #$3C / STA $0640`).
  - Blizzard: buster, F.BLAST (weak) and Y.SPEAR all landed exactly 60 f apart under 4- and 6-frame refire. So did
    Knight + Y.SPEAR and Flame + W.STORM.
  - The blink is 2 frames hidden / 2 frames shown.
  - Damage cells (`$31:$9A45`): weakness 4, most weapons 1, PLANT.B and C.FLASH 0, buster 1, charge 3. The full punch
    is special-cased to 2 (`$9AD6`), and only while the boss's AI holds `$063E` ≠ 0 [code, r2].
  - Best-case vanilla kills (28 HP): weakness 7 × 60 = **420 f (7 s)**; buster 28 × 60 = **1,680 f (28 s)**.
  - [code, r2] `$31:$997D` is the champions' per-frame "take damage, then yield" step: it ends with `JMP $E46C` and is
    reached by `JSR $997D` from 81 sites in bank `$31`. The boss stall (§4.8) is built on that.
- **Fortress bosses** [seen, ds `iframes2.py`: Mr. X 2, Mr. X 4, Wily 2]: **32 frames** after every hit (`$05DF`),
  damage from `$3F:$EFE4`. The full punch does 4 there (the class-1 low-nibble rule). [code, r2] `$3F:$EF64` (slot 8
  only) also ends with `JMP $E46C`, and its hit flash swaps the boss palette to `$BB` every 8 frames for 4 frames, 4
  times: a **7.5 Hz** pulse (§5.1).
- **Normal enemies** [seen, ds `enemy_iframes.py`]: **no i-frames**. A buster fired every 4 frames into a HP-15 enemy
  hit every 4 frames. The shot vanishes unless it kills (`$38:$9067`).
- **Rock** [seen, ds]: 30 f of knockback (14 px), then 60 f of blinking. Contact damage = the enemy's low nibble.

So vanilla's weakness is pure damage (4 vs 1), and every boss hit costs the same 60 frames. The result is a buster that
is as good as any non-weak weapon, and weapons that are pointless against bosses.

### 4.2 The GP model

Two tables, **damage** and **i-frames**, per boss row × source column. The 4MI model, credited in the readme (and in
the Museum if it ever ships). Damage stays 1-4. The weakness lives mostly in the i-frames.

| Grade | Damage / i-frames | Meaning | Reaction | Tier |
|---|---|---|---|---|
| **W**eak | **4 / 16** | the vanilla weakness, kept | WEAK! pop, stagger, announcer (§5) | Must |
| **G**ood | 3 / 20 | a second, thematic answer | short blink | Must |
| **N**eutral | 2 / 30 | "any special weapon fights decently" (4MI) | | Must |
| **R**esisted | 1 / 45 | worse than a charged buster | after 3 in a row the announcer hints | Must |
| **O**wn weapon | 1 / 60; the first hit's joke reaction is SC4 | refights and replays only | | Must (cell); Should (SC4) |
| **BUSTER** | 1 / 60 | vanilla feel, unchanged | the long blink *is* the information | Must |
| **CHARGE** | 3 / 60 | vanilla | | Must |
| **PUNCH** tap/half | 2 / 40 | Power's free option | | Must |
| **PUNCH★** full | 3 / 30 | vanilla 2 → 3: Power is the "no-energy" boss form, but it is close range | | Must |
| **FIST** (Super) | 3 / 40 | weaker than PUNCH★ by design | | Must |
| **M.BEAM**, **HAZARD** | 0 | utilities. Bosses ignore player-lit oil, so no cheese | | Must |
| **CHAMP.B** | 4 / 8 on the W3 Capsule only | Break Man's gift (SC11) | | Must (W3) |
| **BREAK** / **BREAK★** | 1 / 40, 3 / 40 | the partner's buster is better than Rock's, as it should be | | Should |
| **PARRY** | 2 / 20 | rewards the skill | | Could |
| **RULE** | 4 / 12 with the WEAK bit on the exhibition guests | the arena event (consistency-18) | | Could (with E1-E4) |

**Why 16 frames for a weakness and not 4MI's 1-8.** A refire rate of about 12-16 f is typical for RM6's one-at-a-time
weapons. A 16-f window means a well-placed weakness weapon lands every shot that connects, so the weakness feels like
4MI's ("the boss melts"), but the boss can't be drained by a held hitbox. Best-case weakness kill: 7 × 16 = 112 f. In
practice the boss pattern decides, about 3-5 s.

**Why the buster stays at 60.** It is exactly vanilla. A buster-only player loses nothing compared with RM6. Every
weapon got better, so the carrot is in the weapons, not a stick on the buster. The BRIEF's "≈ 60, gentler than 4MI's
127" is met.

**Best-case frames to kill 28 HP** (every hit lands when the i-frames end; refire assumed 12 f where not stated):

| Source | Frames | Seconds | vs vanilla |
|---|---|---|---|
| Weak (4/16) | 112 | 1.9 | 420 |
| Good (3/20) | 200 | 3.3 | 1,680 |
| Neutral (2/30) | 420 | 7.0 | 1,680 |
| PUNCH★ (3/30, 45-f charge) | 450 | 7.5 | 840 (vanilla: 2 / 60) |
| PUNCH tap (2/40, 32-f fist) | 560 | 9.3 | 840 |
| FIST (3/40, 45-f charge + flight) | ≈ 600 | 10 | - |
| CHARGE (3/60, 90-f charge) | 900 | 15 | 900 |
| Resisted (1/45) | 1,260 | 21 | 1,680 |
| BUSTER tap (1/60) | 1,680 | 28 | 1,680 |

Energy is the real limit on the good options: neutral needs 14 hits (half a bar of a cost-1 weapon, a whole bar of
B.ATTACK at cost 2, impossible with C.FLASH at cost 4); the weakness needs 7 hits (a quarter bar). So mixing weapons is
both the fastest and the cheapest way to fight. That is the premise, and it holds with taps alone.

### 4.3 Table 1: damage, the 8 champions (rows = source, columns = boss)

Assignments:

- **W** = the vanilla weakness cycle (Flame > Blizzard > Plant > Tomahawk > Yamato > Knight > Centaur > Wind > Flame,
  read "F.BLAST beats Blizzard"…).
- **G** and **R** are two more permutations. Each weapon is W for one champion, G for one, R for one, own for one and N
  for four. No weapon is worse overall than another.
- The same rows serve the 8 SUPER copies in W2's bracket rush, own-weapon cells included.

| Source | Blizzard | Wind | Plant | Flame | Yamato | Tomahawk | Knight | Centaur |
|---|---|---|---|---|---|---|---|---|
| BUSTER (tap, half, Jet) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| CHARGE | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| PUNCH (tap, half) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| PUNCH★ (full) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| FIST (Super) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Y.SPEAR | 2 | 3 G | 2 | 2 | 1 own | 2 | **4 W** | 1 R |
| W.STORM | 1 R | 1 own | 2 | **4 W** | 2 | 3 G | 2 | 2 |
| B.ATTACK | 1 own | 2 | **4 W** | 3 G | 2 | 1 R | 2 | 2 |
| F.BLAST | **4 W** | 2 | 3 G | 1 own | 2 | 2 | 1 R | 2 |
| PLANT.B | 2 | 1 R | 1 own | 2 | 3 G | **4 W** | 2 | 2 |
| KNIGHT.C | 3 G | 2 | 2 | 2 | 1 R | 2 | 1 own | **4 W** |
| SILVER.T | 2 | 2 | 2 | 1 R | **4 W** | 1 own | 2 | 3 G |
| C.FLASH | 2 | **4 W** | 1 R | 2 | 2 | 2 | 3 G | 1 own |
| M.BEAM, HAZARD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BREAK (Should) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| BREAK★ (Should) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| PARRY (Could) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

Thematic reading of G and R (all tunable):

| Boss | Good (G) | Resisted (R) |
|---|---|---|
| Blizzard | KNIGHT.C: a mace smashes ice | W.STORM: a blizzard enjoys wind |
| Wind | Y.SPEAR: jams the fan | PLANT.B: leaves get blown away |
| Plant | F.BLAST: the vanilla second weakness, 2 in `$9A45`, promoted | C.FLASH: photosynthesis |
| Flame | B.ATTACK: ice puts out fire, as the vanilla thematic table already says for the fire robots | SILVER.T: a wooden haft burns |
| Yamato | PLANT.B: vines tangle armour joints | KNIGHT.C: armour vs armour |
| Tomahawk | W.STORM: a dust devil on a showman's hat | B.ATTACK: desert heat |
| Knight | C.FLASH: a flash goes around a shield, as vanilla C.FLASH latches class-3 shields | F.BLAST: plate armour is heat-proof |
| Centaur | SILVER.T: a hunter's axe | Y.SPEAR: hooves kick spears away |

### 4.4 Table 2: i-frames (frames), the 8 champions

| Source | Blizzard | Wind | Plant | Flame | Yamato | Tomahawk | Knight | Centaur |
|---|---|---|---|---|---|---|---|---|
| BUSTER (tap, half, Jet) | 60 | 60 | 60 | 60 | 60 | 60 | 60 | 60 |
| CHARGE | 60 | 60 | 60 | 60 | 60 | 60 | 60 | 60 |
| PUNCH | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| PUNCH★ | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| FIST | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| Y.SPEAR | 30 | 20 | 30 | 30 | 60 | 30 | **16** | 45 |
| W.STORM | 45 | 60 | 30 | **16** | 30 | 20 | 30 | 30 |
| B.ATTACK | 60 | 30 | **16** | 20 | 30 | 45 | 30 | 30 |
| F.BLAST | **16** | 30 | 20 | 60 | 30 | 30 | 45 | 30 |
| PLANT.B | 30 | 45 | 60 | 30 | 20 | **16** | 30 | 30 |
| KNIGHT.C | 20 | 30 | 30 | 30 | 45 | 30 | 60 | **16** |
| SILVER.T | 30 | 30 | 30 | 45 | **16** | 60 | 30 | 20 |
| C.FLASH | 30 | **16** | 45 | 30 | 30 | 30 | 20 | 60 |
| M.BEAM, HAZARD | - | - | - | - | - | - | - | - |
| BREAK, BREAK★ (Should) | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| PARRY (Could) | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |

The flash is the boss blink, kept at vanilla's 2-hidden/2-shown rhythm for the whole i-frame time: a 16-f flicker reads
as a "stutter" (4 blinks); 60 f reads as the familiar long blink (15 blinks). That is BRIEF §5.1's "readable on screen"
without new art. A sprite blink is small and is information, so the flash rule (§5.1) leaves it alone.

### 4.5 The other v1.0 boss rows

These bosses belong to `fortress.md` and the venue docs; the values are **defaults those docs may override** (fortress
§8 matches them cell for cell). Cells are "damage / i-frames". Two families:

- **Machines** (BG-drawn or vehicle bosses) keep vanilla's fortress base of **32 f** for the buster. The full punch
  does **4** to them, vanilla's "Power is the fortress weapon" rule, kept on purpose.
- **Robots** (Bass β, Dark Man) use the champion scale.

**v1.0 rows** (the boss list of RULINGS R3.6: Grand Pi-kun one size; WILY MACHINE 6.5 on vanilla Wily Machine 6 art; Bass
β; Gamma head and fists; no Doc Robot):

| Source | Grand Pi-kun (Opening) | Bass β (Riot, W2) | H1 Yellow Devil MK-VI | H3 Gamma MK-VI phase 1 / phase 2 (head) | H5 Dark Man MK-VI | W3 WILY MACHINE 6.5 | W3 Wily Capsule SUPER | Mid-boss default | Machine default |
|---|---|---|---|---|---|---|---|---|---|
| BUSTER | 1/30 | 1/40 | 1/32 | 1/32 / 0 | 1/60 | 1/32 | 1/32 | 1/20 | 1/32 |
| CHARGE | 3/30 | 3/40 | 3/32 | 3/32 / 0 | 3/60 | 3/32 | 3/32 | 3/20 | 3/32 |
| PUNCH | - | 2/30 | 2/32 | 2/32 / **2/30** | 2/40 | 2/32 | 2/32 | 2/16 | 2/32 |
| PUNCH★ | - | 3/30 | **4/24** | 4/24 / **4/12** | 3/30 | **4/24** | **4/24** | 4/16 | 4/24 |
| FIST | - | 3/30 | 3/32 | 3/32 / **3/20** | 3/40 | 3/32 | 3/32 | 3/16 | 3/32 |
| Y.SPEAR | - | 2/24 | 3/16 G | 2/24 / 0 | 2/30 | 1/32 R | 2/24 | 2/16 | 2/24 |
| W.STORM | - | 2/24 | 2/24 | **4/12 W** / 0 | 2/30 | 2/24 | 2/24 | 2/16 | 2/24 |
| B.ATTACK | - | 2/24 | 2/24 | 3/16 G / 0 | 2/30 | 2/24 | 2/24 | 2/16 | 2/24 |
| F.BLAST | - | 2/24 | 2/24 | 2/24 / 0 | **4/16 W** | 2/24 | 2/24 | 2/16 | 2/24 |
| PLANT.B | - | 2/24 | 1/32 R | 2/24 / 0 | 3/20 G | 2/24 | 2/24 | 2/16 | 2/24 |
| KNIGHT.C | - | 2/24 | 2/24 | 2/24 / 0 | 2/30 | 3/16 G | **4/12 W** | 2/16 | 2/24 |
| SILVER.T | - | 2/24 | 2/24 | 2/24 / 0 | 1/45 R | **4/12 W** | 3/16 G | 2/16 | 2/24 |
| C.FLASH | - | 2/24 | **4/12 W** | 1/32 R / 0 | 2/30 | 2/24 | 1/32 R | 2/16 | 2/24 |
| Ice Block (ALT override) | - | 1/30 | 1/30 | 1/30 / 0 | 1/30 | 1/30 | 1/30 | 1/30 | 1/30 |
| CHAMP.B | - | - | - | - | - | - | **4/8 W** (SC11) | - | - |
| BREAK / BREAK★ (Should) | - | 1/40, 3/40 | 1/32, 3/24 | 1/32, 3/24 / 0 | 1/40, 3/40 | 1/32, 3/24 | 1/32, 3/24 | 1/20, 3/16 | 1/32, 3/24 |
| PARRY (Could) | - | 2/20 | 2/20 | 2/20 / 0 | 2/20 | 2/20 | 2/20 | 2/16 | 2/20 |
| **Rule** | HP 14 (tune). A charge tutorial: the buster is all you own | **Adaptive armour (SC6)** | eye only | **Phase 2: fists only (SC5)** | | Vanilla homage: SILVER.T was the Wily Machine 6's weakness, KNIGHT.C its second | Vanilla homage: the Capsule ignored C.FLASH | | |

Notes:

- The legacy weaknesses echo their home games where the arsenal allows: Yellow Devil fell to a beam (C.FLASH); Gamma's
  head falls to a body blow (punches, the Top Spin nod).
- **Mid-boss default** serves, unless their doc says otherwise: H1's Big Eye MK-VI, H3's mid-boss (a re-skinned vanilla
  mid-boss in v1.0, R3.6), W3's Trophy Dispenser, and the venue mid-bosses (AYACO, Metal Metslime, Six-Shot Sam,
  Sidewinder, CONGA, Shadow Rock, …).
- **Machine default** serves any machine-family fight that has no row.
- "-" in Grand Pi-kun's column means the player cannot own that source in a first run of the Opening. On replays the
  mid-boss default column applies.
- The SC5 cells of Gamma phase 2 in v1.1: Time Fist punches 4/12 and Morning Star 3/20 (Should synergies).
- In v1.0 Gamma is drawn as **head and fists only** (about 100 tiles, R2.11); fortress gives phase 1's row to **the chin
  cannon only** (fortress §8; round 1 used a chest core).

**v1.1+ rows** (defaults kept for the stages and bosses that come back later; H2 and H4 are Should, R0.3 item 5):

| Source | H2 Mecha Dragon MK-VI (Should, with H2) | H4 Cossack Catcher MK-VI (Should, with H4) | W1 METALL 16 (Could, with W1) | E1-E4 guests (Could) | Air Man (Doc Robot MK-VI's copy; Should, with him) |
|---|---|---|---|---|---|
| BUSTER / CHARGE | 1/32, 3/32 | 1/32, 3/32 | helmet up only: 1/32, 3/32 | 1/32, 1/32 | 1/60, 3/60 (the robot scale) |
| PUNCH / PUNCH★ / FIST | 2/32, **4/24**, 3/32 | 2/32, **4/24**, 3/32 | helmet down: full blows only (`$14`, FULL) | 1/32 | 2/40, 3/30, 3/40 |
| W / G / R | KNIGHT.C 4/12, SILVER.T 3/16, F.BLAST 1/32 | Y.SPEAR 4/12, W.STORM 3/16, KNIGHT.C 1/32 | W.STORM 4/12 + FLIP (an SC9 reaction), SILVER.T 3/16, F.BLAST 1/32 | the RULE column 4/12 W; weapons 1/32 | **PLANT.B 4/12 W** (the Leaf Shield echo, fortress §8); no G or R |
| other weapons | 2/24 | 2/24 | 2/24 | 1/32 | 2/30 |

Doc Robot MK-VI (Should, R3.6; fight `$29`) copies **AIR MAN** through the fight loader (fortress §8) and uses the Air
Man row above, row 22 of §4.8, added with him.

**The 1993 column** (Could, with 1993 RULES; design-18, consistency-39): every row above gets a "1993" twin generated
by family: machines 32 f with the full punch at 4 and the vanilla-style weakness at 4 on the W cell, everything else 1;
robots and champions 60 f with the weakness at 4, the full punch 2, everything else 1, PLANT.B and C.FLASH 0 except where
vanilla had 4. SC5 stays on under 1993; SC6, COUNTER and Knight's HEALMORE are off. The legacy stages `$08-$0F` and the
`???` fight use vanilla `$EFE4` untouched.

### 4.6 Special cases, in visible code (CX lesson 7: never by table fall-through)

| Id | Case | Rule | Tags | Tier |
|---|---|---|---|---|
| SC1 | Knight Man's shield (class 3, `$38:$90A2`) | Frontal shots reflect, except: **Y.SPEAR** (class 5) and the **`$14` full-power blows** (PUNCH★, the Super fist's outward leg, the Break Shot), which vanilla already lets through [code, r2: `$38:$90A9-$90B7`], and **C.FLASH** (latched directly). Y.SPEAR pierces without breaking it (consistency-35; story's KNT-08 line stands). A FULL-flagged hit on the shield from the front **breaks the shield**: systems' default is 180 f (tune); venues_a's rework makes it permanent for the fight ("THE SHIELD BROKE!"), and the venue decides | new-code S | Must |
| SC2 | Centaur Man vs Time Stop | Immune to Time Stop and Time Fist's stop; announcer "He galloped right through it!" | new-code S | Should (with Time Stop) |
| SC3 | Plant Man vs C.FLASH | "Photosynthesis": the first C.FLASH of each fight **heals him 2** (the bar rises, with a "?!" pop). After that, R 1/45. venues_b's Flame ABSORB (heals 1) is a named exception of the same kind, listed under SC4 | new-code S | Could |
| SC4 | Own weapons (refights, and any fight where the player already owns it) | The **first** own-weapon hit per fight does **0 damage** and plays the champion's joke reaction (≤ 60 f). After that it is the O cell (1/60). The OWN MOVE style act. The reactions belong to the venue docs. Without SC4 the O cell simply applies from the first hit. **Named exception: Flame Man's ABSORB** (venues_b §2.8, consistency-33): his first F.BLAST hit **heals him 1** instead of doing 0, and PILLARS fires three flames for 300 f | new-code M | Should |
| SC5 | Gamma MK-VI phase 2 | Only fists hurt the head: the tap punch (2/30), PUNCH★ (4/12) and, on replays, the Super fist (3/20); in v1.1 Time Fist (4/12) and Morning Star (3/20). Everything else dinks (`$27`). The telegraph: the plaque reads "THE HEAD RESPECTS ONLY A FIST" (`story.md` owns the words), and H3 adds a no-risk fist-ride practice beat before the fight (R2.11). **Under 1993 RULES SC5 stays on**: Power is reached through the pause menu's vanilla transform, and the punch is the 1993 player's answer too | new-code S | Must (H3) |
| SC6 | Bass β adaptive armour | The 3rd consecutive damaging hit from the same column makes that column 1/45 until a *different* column hits him. Announcer: "He's adapting!". In W2 the armour starts adapted to the column the player used most in the Riot duel (meta's BASS_ADAPT byte). The rival literally punishes a one-weapon player: the premise in one rule. Off under 1993 RULES. His copy attack uses only the weapons whose tiles are pre-drawn in his own boss set: **B.ATTACK, F.BLAST, KNIGHT.C and SILVER.T** (4, R3.6; fortress §9.2's pick) | new-code S | Must |
| SC7 | Yellow Devil MK-VI "SELECT trick" | A nod to RM1's famous pause bug: a weapon swap within 2 frames of a WEAK hit clears the eye's i-frames, once per eye opening. Hinted in the H1 plaque only | new-code S | Could |
| SC8 | Tomahawk Man's quick-draw (venues_a §3.5, VA-DRAW) | A won draw deals a **free hit of 3** with 30 i-frames, whatever is equipped; booked as BUSTER for VARIETY. **The window is NORMAL 24 f, HARD 18 f, CASUAL 40 f (R8.6), plus INPUT LAG (0-6 f, R8.7)**, in every VA-DRAW (the saloon's and the boss's; R3.5, §1.6). The draw is staged by the venue as a judged tournament event (R3.4) | new-code S | Must |
| SC9 | Venue-defined weak reactions | A venue's WEAK reaction (Wind's STALL 120 f, Tomahawk's HAY FEVER, Blizzard's MELT 40 f, METALL 16's FLIP…) **replaces** the generic 10-f stagger of §5. It is an AI state, not a freeze, so damage keeps working. The 90-f re-trigger rule and the 16-f i-frames still apply. Venue proposals of 8-f weakness i-frames are overridden by the 16 f of Table 2 | data | Must |
| SC10 | Bass β COUNTER (fortress §2.4) | When Bass fires a copy, the same weapon from Rock cancels it; Rock's next hit with that weapon within 60 f is a COUNTER!: 3/16, outside SC6. Off under 1993 RULES | new-code S | Should |
| SC11 | The CHAMPION BUSTER (fortress §5.3.3, Break Man's or Roll's gift in W3) | While held it replaces the buster and the weapon menu (HUD `WPN: CB`); its column CHAMP.B is **4/8 with the WEAK bit on the Capsule row** and 0 elsewhere; **while it is held any hit of 2 or more on Rock becomes 1** (a branch in the hurt routine `$38:$8F72`). A death after the gift keeps it on respawn | new-code S | Must (W3) |

**Stage-owned special cases.** These live in the same visible-code list, never in a table cell; the owner doc stages
them, sets the tier and counts the code:

| Id | Case (owner) | Rule | Tier |
|---|---|---|---|
| SC12 | Metal Metslime (venues_a §2.7, KAISHIN's gate; mid-boss fight `$09`) | **Every hit does exactly 1**, whatever the source, with 2-f i-frames: a substitution before the mid-boss default cell. NOFREEZE | Must |
| SC13 | Kamegoro Maker MK-VI (fortress §4.3, H3's mid-boss) | **Each turtle destroyed also costs the machine 2 HP** (the turtle's death hook calls the machine's HP step) | Must |
| SC14 | Dark Man MK-VI's **WRONG NOTE** (fortress §4.5) | A FULL-flagged hit while the red note is up sets his HP to min(HP, 14) and plays the exposure (the boss panel's third record, R8.5). With the partner (Should), calling Break Man in phase 1 does the same | Must |

fortress's other visible cases (Pi-kun's reflect outside the valve, Gamma's chin and cockpit boxes, WILY MACHINE 6.5's
drag, the SUPER copies' per-fight pinch byte) sit in the same list, as fortress §8 states them.

### 4.7 SYS-CMB-2: normal enemies [engine-ok] + [new-code] S, Must (v0.1)

- **Damage = the low nibble of the shot's attack byte** (vanilla `$E9D7`), as listed per weapon in §3. Fixed damage per
  weapon is already vanilla.
- **Mook HP stays vanilla** (AI header byte AI-2; 0-5 for most).
- **No i-frames on hit**, as in vanilla [seen, ds], **except lingering hitboxes**: in v1.0 only the Super rocket fist
  (both legs); in v1.1 Updraft, Flare, the held mace, Petal Storm, the Pogo and Morning Star. A given enemy takes a
  lingering hitbox at most once per **8 f**, through the per-slot WORK re-hit timer `REHIT`.
- **Thematic one-shots.** Vanilla has 3 per-class tables (`$3F:$EB46/$EB56/$EB66`): B.ATTACK kills Knight's blue-hall
  enemies and the fire robots; F.BLAST kills the snow robot and walkers. GP keeps them and adds one table per venue
  **featured enemy** family (8 in all; each venue doc names its own: venues_a picks Wind's shield-cars `$34`, Knight's
  lance knights `$6E`, Tomahawk's cowboy gunners `$6C` and Plant's scorpions; the defaults for the other four are the
  snow robot `$4D`, Fire Telly `$2C`, the samurai `$A2` and the seahorse `$C4`). Each dies outright to **its champion's
  weakness weapon**, which always comes from another venue: an **in-stage tell** for the boss (CX lesson 6). **In v1.0
  there is no PART drop** (R2.5); the drop returns with the Could bundle. "Totem" is not a featured enemy (R3.4).
- **Punch-only enemies** (`$3F:$EA99`: Metalls `$15/$18`, `$24`, `$A3`) accept latch `$14` only, as in vanilla. Every
  GP full-power blow that should open them carries attack byte **`$14`**: PUNCH★, the Super fist's outward leg, the
  Break Shot, and in v1.1 Morning Star and Time Fist. Their scoring and boss column come from LATCHSRC, so `$14` stays
  one byte with one meaning to the 21 vanilla compare sites.
- **"A full-power blow" for new GP objects** (the Riot's auditions, Centurion statues, skeletons) is the **FULL flag
  of LATCHSRC** (§6.4): the full charge, PUNCH★, the Super fist out, BREAK★, Burning Knuckle, Morning Star, Time Fist.
  Vanilla AIs keep testing `$13`/`$14`. The Super fist counts (fortress's proposal, accepted).

### 4.8 SYS-CMB-1, SYS-CMB-3: how it is built [new-code] M, Must (v0.1)

**One lookup, `GP_BOSSHIT(row, col)`.**

- It replaces `$31:$997D`'s class lookup (from `$99B7`: `$9A45 + 16*(stage&7) + class`), the full-punch special case
  `$9AD6` and the constant at `$31:$9A01` (`LDA #$3C / STA $0640`). On the fortress side it replaces `$3F:$EF64`'s
  `$EFE4` lookup and its 32-f store into `$05DF`.
- **Vanilla gates kept** (conservative default): a latch of `$30` is ignored; a boss whose own class is A or 6 takes no
  damage; on the champions' path PUNCH★ lands only while the boss's AI holds `$063E` ≠ 0 (reworked champions set it in
  their punchable states).
- **row** = `BOSS_ROW`, set when a boss bar starts: the venue id for the champions (vanilla `$063D`), the stage record's
  boss-row field for fortress bosses on the `$EF64` path (tech's `FORT_COL`), or the sub-id record's row byte for GP
  bosses (tech's families `$F8/$F9`). The stage record v0 exists from M2.1, so the slice reads it too: **no stage-`$00`
  stop-gaps** (R8.2).

  | Row | Boss | Row | Boss |
  |---|---|---|---|
  | 0-7 | the champions (and their W2 SUPER copies) | 14 | WILY MACHINE 6.5 |
  | 8 | Grand Pi-kun | 15 | Wily Capsule SUPER |
  | 9 | Bass β | 16 | mid-boss default |
  | 10 | Yellow Devil MK-VI | 17 | machine default |
  | 11 / 12 | Gamma MK-VI phase 1 / phase 2 | 18-21 | v1.1+: Mecha Dragon, Cossack Catcher, METALL 16, exhibition guest |
  | 13 | Dark Man MK-VI | 22 | v1.1+: Air Man (Doc Robot MK-VI's copy, Should) |
  | | | 23-31 | spare (legacy) |

- **col** = `LATCHSRC,X` bits 0-4 (§6.4):

  | Col | Source | Col | Source |
  |---|---|---|---|
  | 0 | none: vanilla rule for that path, no scoring | 11 | KNIGHT.C |
  | 1 | BUSTER (tap, half, Jet) | 12 | SILVER.T |
  | 2 | CHARGE | 13 | C.FLASH |
  | 3 | PUNCH (tap, half; Super tap) | 14 | M.BEAM |
  | 4 | PUNCH★ | 15 | HAZARD |
  | 5 | FIST (Super) | 16 | CHAMP.B |
  | 6 | Y.SPEAR | 17 | BREAK (Should) |
  | 7 | W.STORM | 18 | BREAK★ (Should) |
  | 8 | B.ATTACK | 19 | PARRY (Could) |
  | 9 | F.BLAST | 20 | RULE (Could) |
  | 10 | PLANT.B | 21-31 | spare |

- **Cell format:** 1 byte: bits 0-2 = damage (0-7); bits 3-6 = i-frame class (0 immune/dink, 1: 8, 2: 12, 3: 16, 4: 20,
  5: 24, 6: 30, 7: 32, 8: 40, 9: 45, 10: 60, 11: 90 f); bit 7 = WEAK. Size: 32 rows × 20 columns = 640 B (v1.0 fills 18
  rows). An **ALT override** table (one cell per weapon's alt, `$00` = use the weapon's cell) holds the Ice Block's 1/30.
- **Order of a hit**: read the latch → vanilla gates → cell (or ALT override, or an SC substitution) → if the boss's
  i-frames are running, nothing → damage 0 plays the dink `$27` (EV_IMMUNE once per fight) → else HP −= damage (+2 for
  KAISHIN's 12th hit, §9.2) and the i-frame count from the class goes into `$0640` (champions) or `$05DF` (fortress
  path) → `CATS |= category(col)` (§6.4) → the WEAK bit runs §5 → the vanilla death paths (`$ED42`, `$EF64`'s) with the
  death hook → exit through the boss stall below.
- **The chart is generated from the source data** (CX lesson 7) by `tools/build/dmgchart.py` (tech), which prints this
  section's tables; these tables are its seed data. A test asserts every v1.0 row has every Must column filled.

**The frozen tick (SYS-CMB-3), R2.2 (feasibility-6).** Damage continues while frozen. In v1.0 the freezes are the Ice
Block's encase and the WEAK stagger; Time Stop joins in v1.1.

- **Normal enemies: frozen handlers.** Every type (and every GP family sub-id) has a **`FRZ_KIND`** (tech §7.7: 0
  NOFREEZE, 1 STD for `$E9D7`, 2 STD2 for `$EA20`, 3 NODMG for `$EA6E`, 4 BOSS, 5 CUSTOM). The build derives the vanilla
  kinds from tech's damage-step scan (`dmgstep.py`); the research damage map is the cross-check [code, r2:
  `verify_r2.py`]: **35 types use `$E9D7`, 5 use `$EA20`, 62 use `$EA6E`**; the 29 types with any other or mixed damage
  step (punch-only `$EA99`, the thematic tables `$EAB7`, `$EA80`, the Robot Masters, the fortress bosses, mixed entries)
  and the 125 with none are NOFREEZE: they ignore freezes but still take hits. **This doc's NOFREEZE override list**
  (which wins over the derived kinds): every type a venue or fortress doc marks NOFREEZE, plus any type whose AI moves
  other objects (carriers, spawners, the gorilla tank's parts). Adding the `$EAB7` and `$EA99` types (the snow robot, the
  Metalls) is a v1.1 candidate after the M4 measurement. A freezing weapon never sets `FREEZE` on a NOFREEZE slot.
- **The object-loop patch** (tech's inline `$7F` hook at `$3F:$E443`, before the bank map): if `FREEZE,X` ≠ 0 and the
  kind is 1-3 or 5, decrement it; at 0, thaw (restore `ENC_CLASS,X`, shatter the shell) and run the AI normally this
  frame; otherwise call the frozen handler for the kind and end the slot's turn. The OAM builder draws the object anyway
  (a separate pass). Kind 4 (BOSS) is never skipped: see the boss stall below.
- **Why handlers and not the vanilla routines** [code, r2]: `$E9D7` is not a pure damage function. It clears the hit
  flash, runs the off-screen check `$E489`, applies the class hit effect `$EB76`, subtracts HP, and then either converts
  the slot to the explosion (`LDY #$17 / JSR $CB28 / .byte $41 / JMP $E47B`) or **yields** (`JMP $E46C`), which would
  store a resume address inside the object loop. `$EA20` is the same with type `$25`; `$EA6E` clears the latch and
  yields. So each frozen handler is a **copy of its routine with the yield replaced by `JMP $E47B`** (end turn, resume
  address untouched), ≈ 40 B each in `$7F`:

  ```
  frz_std17:  LDX $8F ; clear $03B7 b0 ; JSR $E489 ; BCS gone
              LDA $056C,X ; BEQ done
              class 6 (W.STORM)? -> FREEZE,X = 0 ; restore class ; JMP $E47B   ; the vanilla tick takes the hit next frame
              set $03B7 b0 ; damage = latch & $0F ; SFX $35 ; $056C,X = 0 ; HP -= damage ; BPL done
              FREEZE,X = 0 ; restore class ; LDY #$17 ; JSR $CB28 ; .byte $41 ; JMP $E47B   ; dies (the death hook runs)
  done:       LATCHSRC,X = 0 ; JMP $E47B
  gone:       JMP $E45A
  ```

  `frz_std25` dies to type `$25` with HP `$FF`; `frz_immune` clears the latch, runs `$E489` and ends the turn. The
  W.STORM case avoids `$EB8B`'s blow-away loop, which yields from inside the hit effect.
- **Bosses (kind 4): the boss stall**, tech's "boss-side frozen state", not a skipped AI. The champions' `$997D` and the
  fortress `$EF64` both end in a yield reached by `JSR` from the boss's own code (§4.1). GP_BOSSHIT's exit tests the
  boss slot's `FREEZE,X`: if it is non-zero it decrements it, shakes the boss ±1 px every 2 f, and **re-points the
  resume address at the boss's own `JSR`** (pull the return address, subtract 2, store into `$042A,X/$0413,X`,
  `JMP $E47B`). The boss then re-runs its damage step every frame, keeps blinking and keeps taking damage, but its
  pattern does not advance. That works for the 81 unmodified champion call sites without touching their AI. The WEAK
  stagger sets `FREEZE` = 10 on the boss slot; Time Stop (v1.1) sets 45. GP bosses (family `$F8`) call the same exit. A
  boss that reaches its damage routine by `JMP` instead of `JSR` is listed NOSTALL at M3 and only gets the shake.
- **IRQ-logic bosses** (Knight's ceiling, Centaur's tide, the Wily Machine floor) keep moving during a stall unless
  their logic checks it; tech moves that logic out of the IRQ in M2 (`tech.md` §1.8, BRIEF §7.1), and it tests the boss
  slot's `FREEZE` there.

---

## 5. Weakness feedback (SYS-WK-1) [new-code] S, [new-art] 3 tiles, Must (v0.1)

BRIEF §5.1: a "WEAK!" pop, a stagger and a commentator line on the first weakness hit. Each fires on a cell with the
WEAK bit (§4.8):

1. **The WEAK! pop.** tech's effect family `$FD`, one sub-id (consistency-24). Its tiles are art's GP-COMMON build:
   **W, K and ! (3 new tiles)**, with E and A taken from READY (`$99-$9D`). It spawns at the shot's position, rises
   1 px/f for 24 f, and cycles yellow/white every 4 f. At most one per boss per 30 f. It counts as an occupied slot in
   the lag budget (R1.8); in a boss room that is the boss, the pop, Rock and up to 3 shots. **It takes a free slot
   only**: it spawns only while fewer than 3 boss-side objects are out, and otherwise it is skipped while the stagger,
   the crunch and the announcer still play (venues_b §0.2's boss-room rule, applied to every boss).
2. **The stagger.** The boss stall for **10 f** (`FREEZE` = 10 on the boss slot; damage keeps working), with the ±1-px shake. That is a
   hit-stop. Only if **≥ 90 f** have passed since the boss's last stagger (`WEAK_GATE`); otherwise 16-f i-frames plus
   10-f staggers would stunlock. **Unique reaction** (SC9): if the boss's AI defines a "weak" entry, the stagger calls it
   instead of the generic shake.
3. **The sound.** A new "crunch" SFX. Free ids exist: the SFX `$3D/$3E/$4D/$51` look unused (engine.md §5).
4. **The flash.** The boss palette goes white for 2 frames, at most once per 90 f (the stagger gate), so it is far under
   3 per second. Off under REDUCED FLASHES; the shake stays.
5. **The announcer** (`story.md` writes the lines; the commentator bus is tech's):
   - `EV_WEAK_FIRST`, once per fight → a commentator pop-up (1-2 lines per champion: Must text, R4.5). Its face icon is
     4 BG tiles inside the pop-up's glyph strip (consistency decision 29), so it works in boss rooms whose sprite area is
     full.
   - `EV_RESIST`: the 3rd resisted hit in a row → a hint line.
   - `EV_IMMUNE`: the first dink. Vanilla's dink `$27` already plays.
6. **Memory** (Could). A save bit per boss row records "weakness found" (meta's WEAKFOUND); the pause menu's weapon page
   then shows a ★ next to that weapon during that boss's fight.

The i-frame blink length (16 vs 30 vs 60 f) is itself the second, quieter feedback (4MI's "read the weakness from the
flashing time").

### 5.1 Flash safety for this doc's effects (SYS-FX-1) [new-code] S, Must (v0.1)

**R3.5: in the default mode no effect flashes a large area more than 3 times per second; REDUCED turns every flash into
a fade.** A "large area" is any BG palette change or any object larger than 64 × 64 px. One shared gate,
`FLASH_GATE` (frames since the last large flash), lets a new large flash start only when it is ≥ 20; tech exposes it to
every doc as `gp_flash_ok()`, so venue storms and fortress effects obey the same budget.

| Effect | Vanilla [code, r2] | GP default | REDUCED |
|---|---|---|---|
| C.FLASH | 6 white flashes, 2 f on / 2 f off, in 24 f (15 Hz, whole screen) | one 4-f white-out, then a 3-step fade over 12 f; skipped if `FLASH_GATE` < 20 | a 2-step darken |
| WEAK flash | (new) | 2 f white boss palette, ≤ 1 per 90 f | off |
| Machine / BG-boss hit flash (`$EF64` path) | palette `$BB` 4 f on / 4 f off, 4 times per hit (7.5 Hz) | one 4-f pulse per hit, and only if `FLASH_GATE` ≥ 20 (a 12-f weak cell lands more often than that, so some hits do not pulse) | no palette pulse: the boss bar blinks |
| Sprite boss blink | 2 f hidden / 2 f shown | unchanged: a small area, and it is information | unchanged |
| Time Stop tint (v1.1) | (new) | a darken held for the stop, not a flash | same |
| Swap flash, WEAK! pop | (new) | small (16 × 16), exempt | same |
| YASHICHI, DARUMA, Beat's rescue | (new) | no flash: an SFX, the HP bar fill and a pop line | same |

The boot health notice is `meta.md`'s screen with `story.md`'s words (R3.5).

---

## 6. The scorecard (SYS-SC-1) [new-code] M, Must (v0.1)

Every cleared stage is judged out of 100 (BRIEF §5.3): TIME 20, DAMAGE 20, VARIETY 25, SECRETS 20, STYLE 15. The
results screen (judges, slide-in rows, comments) belongs to `meta.md`; the formulas are here.

### 6.1 Counters (per run; reset at stage start, kept through deaths and fight-loader warps in the same run)

| Counter | Meaning |
|---|---|
| `T` | In-stage frames, counted while `$F0` = 0. Excludes pause, the boss bar fill (`$0642` = `$FF`) and the post-kill sequence. **Includes** death and respawn time (dying costs time) |
| `L` | HP lost by Rock (and Break Man, when he ships): damage after the multiplier, capped at the HP they had |
| `K` | Lives lost (pits, spikes, HP) |
| `CATS` | 16-bit set of scoring categories that killed a normal enemy **or** damaged a boss (§6.4) |
| `OWNED` | Categories the player can use at stage start: BUSTER always; PUNCH once Power is owned; each weapon owned; BREAK only once FORMS.TAG is set and RATEFLAGS.DOPED is clear (consistency-38; never in v1.0) |
| `SECR` | Secret predicates met this run |
| `STY` | Style flags (§6.5) |
| `TANKS` | E-tanks (and, in v1.1, W-tanks) used this run |

A CONTINUE after a game over starts a new run. That run's lost progress is the game-over penalty; there is no E-tank
halving (CX) in GP.

**A fight-loader warp does not reset the run block** (meta §9.2.1). W2's pair bouts are part of W2's own run: their
kills, boss hits, HP lost and frames count in W2's scorecard, and only W2's clear pays, saves and goes to the desk.

### 6.2 Formulas

```
TIME     = 20                                    if T <= P
         = max(0, 20 - ceil(20 * (T - P) / P))   otherwise          (0 at twice the par)
DAMAGE   = max(0, 20 - ceil(L / 3) - 4 * K)                         (a full bar lost, no death = 11)
VARIETY  = floor(25 * min(|CATS|, Pv) / Pv),  Pv = min(5, |OWNED|)  (the par grows with the arsenal)
SECRETS  = floor(20 * sum(w found) / sum(w all))                    (a stage with no secrets scores 20)
STYLE    = 4*WEAK_FINISH + 4*BOSS_NO_HIT + 2*NO_TANKS + min(5, style acts)
```

Why each formula:

- **TIME** is relative to par, so short and long stages weigh the same.
- **DAMAGE** counts HP, not hits. A big boss hit costs more than chip damage. Deaths cost an extra flat 4, so a death
  with a full bar lost scores about 3-7.
- **VARIETY** has a par that grows: Pv = 1 in the first venue (buster only), 2-5 later, and 5 from the 4th weapon on.
  So nobody is punished for an early stage, and **a buster-only run still clears, it just earns less**. Taps alone
  reach it.
- **SECRETS** weights (default): secret exit 3, hidden room 2, behaviour-gated chip 2, Beat plate 1, venue extras 1.
  The predicate list is the same one the judges' debrief walks (`meta.md` §4).

Calibration [guess, checked by playtest at M4]:

| Run | TIME | DAMAGE | VARIETY | SECRETS | STYLE | Total | Medal |
|---|---|---|---|---|---|---|---|
| Decent first clear: 30 % over par, 27 HP lost, Pv met, 2 of 7 secret weight, weak finish + 2 acts | 14 | 11 | 25 | 5 | 6 | **61** | Silver |
| Platinum | 20 | ≥ 18 (≤ 6 HP lost) | 25 | 20 | ≥ 12 | ≥ 95 | Platinum |

### 6.3 Pars

- The par `P` is a per-stage field in the stage-attribute table (`tech.md` `PAR`, in 4-s units, rounded up). It is in
  the 48-byte stage record v0 from M2.1, so the slice reads it there: no stage-`$00` stop-gap (R8.2).
- **Rule for setting it**: P = 1.25 × the golden-movie reference route (normal exit, no deaths, a competent player),
  rounded up to 10 s. The golden movies exist from M0, so pars are measured, not guessed.
- Placeholder pars until the routes exist **(tune)**: Opening-lite 120 s, HALFTIME RIOT 150 s, H1/H3/H5 200 s each,
  W2 300 s, W3 240 s. v1.1+: H2/H4 200 s, W1 200 s, each Exhibition 90 s.
- Venue pars are the venue docs' (§0.8 of venues_a, §5.3 of venues_b): Wind 4:30 (the sortie is a fixed 2:00), Knight
  4:30, Tomahawk 5:00 (the train is a fixed 0:55), Plant 4:00; Blizzard 330 s (with its 40-s bonus round), Flame
  300 s, Centaur 300 s, Yamato 300 s. A set piece with a fixed length is part of the par, so it never costs TIME.
- **Replay skips** (R3.8): after the first clear, a fixed-length set piece may be skipped. A skip **adds the piece's
  fixed length to that run's `T`** at the moment it is taken, so the par stays one field and the skip neither buys nor
  costs TIME; that run cannot meet the piece's secret predicates or its VENUE ACT, so SECRETS and STYLE drop instead:

  | Skip (after the first clear) | Piece skipped | Added to `T` |
  |---|---|---|
  | SKY ACE's **LAND** (the run is marked LANDED) | the 2:00 sortie | **7,200 f** |
  | HIGH NOON's **EXPRESS** | the 0:55 train | **3,300 f** |
  | Blizzard's replay skip door on 0F | the 40-s bonus summit | **2,400 f** |
- VARIETY's par is Pv (above). DAMAGE has no par. The SECRETS par is "all".

### 6.4 Attribution: LATCHSRC (SYS-SC-4) [new-code] M, Must (v0.1)

Vanilla: a player shot touching an enemy copies its attack byte (`CCCC DDDD`, class/power) into the victim's hit latch
`$056C`, and the victim's damage routine reads it and **clears it** (engine.md §2.1). The class nibble already separates
the eight weapons (5-C), but class 1 is shared by the buster, the charge, the Jet buster and all three punch levels, and
`$13` is both the full buster and the half punch.

**R2.1: vanilla attack bytes stay (`$11-$14`), there is no re-class, and no enemy AI latch compare is patched**
(feasibility-5: 21 AI sites compare the latch with `$14`, `$13` or `$1A`). The scoring category comes from a second,
GP-only byte:

1. **The column, derived at latch time** from the shooter (tech §7.7): for vanilla shot types tech's 256-entry
   `SRCTAB[type]` (the class-1 types pick their column by the attack byte), for GP objects their sub-id record:

   | Vanilla type | Attack | Column | Flags |
   |---|---|---|---|
   | `$09`, `$0A` (buster tap, half; Jet buster) | `$11` | BUSTER | |
   | `$0B` (full charge) | `$13` | CHARGE | FULL |
   | `$0C`, `$0E` (punch tap, half) | `$12`, `$13` | PUNCH | |
   | `$0F` (full punch) | `$14` | PUNCH★ | FULL |
   | `$81`, `$82`, `$8E` (flake), `$84`, `$8D` (leaf), `$86`, `$87` | `$52 $62 $72 $84 $94 $A3 $B3` | the weapon | |
   | `$DA`, `$E4` (Wily 1's punch rebound) | `$1A` | PUNCH | |

   GP objects (family `$FB` shots and the utilities) carry the column and flags in their sub-id record (`GP_ARG` /
   `GP_OFLAGS`): Super tap PUNCH, rocket fist FIST (FULL outward), Ice Block B.ATTACK + ALT, M.BEAM M.BEAM, CHAMPION
   BUSTER CHAMP.B, and in v1.1 every alt (ALT) and synergy (SYN).
2. **LATCHSRC at every latch store.** Each `STA $056C,Y` that copies a player attack byte becomes `JSR gp_latch` (3
   bytes for 3). `gp_latch` stores `$056C,Y`, `LASTHIT,Y` (the attack byte, which the victim does not clear) and
   `LATCHSRC,Y` (the shooter X's column and flags), and returns with A = the attack byte (`$38:$906D` compares it next).
   The sites [code, r2: `verify_r2.py`]:

   | Site | Handler |
   |---|---|
   | `$38:$9024` | class 0, pass-through boxes (`$9021`) |
   | `$38:$906A` | the normal hit (`$9067`), also reached from the shield handler `$90A2` for Y.SPEAR, `$14` and hits from behind |
   | `$38:$90E1` | the reflect path (`$90D6`), which latches the victim too |
   | `$38:$9E74` | C.FLASH's direct `$C4` write (column C.FLASH, no shot slot) |
   | `$30:$8ADD` | an enemy-side object that latches `$13` into other objects: a variant, `gp_latch0`, writes LATCHSRC = 0 (none), so enemy-on-enemy damage never scores |

   The class-4 bullet handler `$38:$9028` writes no latch; `$38:$9063` writes into a shot's own latch (the W.STORM path)
   and is not a scoring site. LATCHSRC is **23 bytes of WORK at tech's `$6080`**, one per slot: bits 0-4 the column
   (§4.8), **b5 FULL** (a full-power blow), **b6 ALT**, **b7 SYN**. tech §7.7's "the shot's weapon slot" is replaced by
   this definition (consistency-20).
3. **Read where deaths converge, and at boss hits.** Normal enemies die by turning into the explosion type `$17`
   (`$30:$81C7`) or `$25`; Robot Masters through `$3F:$ED42`; fortress bosses through `$EF64`'s death path. At those
   inits GP adds `category(LATCHSRC[slot])` to `CATS`, counts the kill, runs the multi-kill timer and (v1.1) the
   synergy-kill flag, then clears LATCHSRC. `GP_BOSSHIT` adds the category on every damaging hit (VARIETY counts boss
   hits: consistency decision 35). The frozen handlers and GP's surviving-hit paths clear LATCHSRC, so a stale column
   never credits a later, unattributed death. Custom deaths (the gorilla tank, the Mr. X 1 riders `$3B:$827A`, new GP
   enemies) call the same hook; tech's death-hook audit finds them with shadow6 coverage.

Categories (the `CATS` bits): 0 BUSTER (columns BUSTER, CHARGE, CHAMP.B), 1 PUNCH (PUNCH, PUNCH★, FIST, PARRY), 2 HAZARD
(HAZARD, RULE), 3-10 the eight weapons, 11 BREAK (BREAK, BREAK★). M.BEAM and "none" score nothing.

`CATS` is a set, so farming a respawning enemy with one weapon earns nothing extra. Vanilla's kill bitfield `$0650+`
already stops list enemies from respawning. **HAZARD** kills are enemies killed by oil the player lit or by a venue trap
the player set off; the venue doc's trap object writes LATCHSRC = HAZARD when it latches.

### 6.5 STYLE

| Item | Points | Rule | Tier |
|---|---|---|---|
| WEAK FINISH | 4 | The killing hit on the stage's scoring boss (tech's `SCORE_ID`) is a WEAK cell; in v1.1 a synergy shot also counts (a "form finish") | Must |
| BOSS NO-HIT | 4 | No HP lost from the boss bar filling until the kill | Must |
| NO TANKS | 2 | No tank used in the run | Must |
| Style acts | 1 each, max 5 | MULTI-KILL (2 kills by the same category within 8 f) · FROZEN STEP (stood on an encased enemy) · CLOSE CALL (boss killed with Rock at HP ≤ 4) · EXCELLENT MOVE (KAISHIN's 12th hit landed) · VENUE ACT (one per venue, named by its doc: ACE (Wind), SPELLBREAKER (Knight), QUICKEST GUN (Tomahawk), VINE KILL (Plant); "CONDOR, FIRST PASS" (Blizzard), CLEAN DUEL (Flame), NO WRONG DOOR (Centaur), SPEAR DANCER (Yamato)) | Must |
| Style acts, later | | SYNERGY KILL (v1.1) · OWN MOVE (SC4, v1.1) · TAG TEAM (the partner scored, v1.1) · PARRY (Could) | Should / Could |

### 6.6 Medals and pay

- **Medals:** Bronze ≥ 40, Silver ≥ 60, Gold ≥ 80, Platinum ≥ 95 (BRIEF).
- **Bonus bolts:** 0 / 10 / 20 / 40 / 60 for none / B / S / G / P **(tune)**.
- `PAY(run) = score + bonus(medal)`, at most 160 per stage.
- **Replays pay only the improvement:** `max(0, PAY(new) − PAY(best))`. So the total ever paid per stage = the best
  PAY. A stage cannot be farmed.
- Saved per stage in `meta.md`'s STAGEREC (by meta index, 24 rows: consistency-11): the best score, the medal's preset
  badge (C/N/H/93), the best PAY, and the asterisk bit (used only by the Could bundle).
- Medal points for `meta.md`: B 1, S 2, G 3, P 4.

### 6.7 SYS-SC-3: secret tokens on replays [new-code] S, Must (v0.1)

A collected plate, chip capsule or envelope does not respawn. Without a fix, a replay could never re-earn SECRETS. On
replays such objects spawn as a **token**: a small rotating judge's-pin sprite; touching it sets the secret predicate
and gives nothing else. Secret exits and hidden rooms are re-earned simply by taking them. (PARTs join the list with the
Could bundle.)

---

## 7. Bolts and the income model (SYS-ECO-1) [new-code] M, Must (v0.1)

Money is prize money (BRIEF §1). **Bolts never drop from enemies.** That and the improvement-only rule make the economy
grind-proof.

| Source | Bolts | Notes | Tier |
|---|---|---|---|
| Scorecard, first clear | score + medal bonus (≤ 160) | the 15 v1.0 stages | Must |
| Scorecard, replay | the improvement only | | Must |
| **Sponsor envelope** | 30, once per save | **one in every hidden room**: the 8 venue rooms (venues_b's 50-bolt bags and 100-bolt chest become envelopes: R2.7, consistency-10) and each fortress stage's hidden room, the Opening-lite's dressing room included (fortress §1.5). Each counts as a secret (SECRETS b4 for venues) | Must |
| **Prizes** (bounties, treasures, vegetables, showpieces, props) | set by the stage docs | paid once per save per placed prize, **≤ 60 per stage, venue or not** (R2.7, consistency-19); a replay shows them as tokens. venues_b re-prices Blizzard's vegetables to ≤ 60 in all (the critic's 5/5/5/10/10/10/15) and fits Y.SPEAR's ledge bolts inside the cap; fortress's 30-bolt showpiece payouts count against it. `meta.md` stores one PRIZES bit per placed prize | Must |
| 1UP picked up at 9 lives | 10 ("fan tip") | no dead pickups | Should (SYS-PU-4) |
| E-tank picked up while holding 4 | 20 | | Should |
| Exhibition first clear | 100 + an exclusive racing colour | fixed prizes, not chips | Could (with E1-E4) |
| Mr. Y's respawn insurance (the fortress heckle's YES) | **−1**, never below 0 | R4.3: CX's "Yes, that hurts" at a harmless scale; `story.md` owns the gag | with story's heckle table |

The counter caps at 999.

**Income model, v1.0** (the prices in §8 are sized against it):

| Player | After the Opening + 4 venues | After Round One (Opening, 8 venues, Riot) | Full v1.0 (15 stages) |
|---|---|---|---|
| Typical (≈ 62 + Silver per stage, half the envelopes and prizes) | ≈ 635 | ≈ 1,270 | ≈ 1,905 |
| Completionist (Platinum everywhere, every envelope and prize) | ≈ 1,250 | ≈ 2,500 | ≈ 3,750 |

The arithmetic: a typical clear pays 62 + 20 = 82 and a stage with a hidden room adds (30 + 60) / 2 = 45; a
completionist clear pays 160 + 90. **The Opening-lite keeps its hidden room** (Pi-kun's dressing room, with the first
envelope, +30) and its two 30-bolt prizes (fortress §1.5), so all 15 stages add the extras: 5 × 82 + 5 × 45 = 635;
10 × 82 + 10 × 45 = 1,270; 15 × 82 + 15 × 45 = 1,905 (round 2's model left the Opening out: +45 typical, +90
completionist).

- The 5 v1.0 shop chips cost **740** in all.
- A typical player can afford 2-3 chips plus tanks by the middle of Round One, and the whole catalogue around the Riot.
- Slots (2-6), not money, are the real limit late on. In v1.0 money has few late sinks (E-tanks and 1UPs); the W-tank
  (Should) and RACING COLOURS (Could) restore them. Risk 9.

---

## 8. Eddie's Pit Stop: stock and prices (SYS-ECO-1)

Reached from the bracket screen (`meta.md` owns the UI). It opens **after the Opening, at 0 wins** ("start" below), as
meta and the revised story sign say (consistency decision 14). Stock unlocks by WINS, so money can't be front-loaded.

| Item | Price | Max held | Unlock | Tier |
|---|---|---|---|---|
| E-TANK | 40 | 4 | start | Must |
| 1UP | 30 | lives 9 | start | Must |
| SHOCK ABSORBER (chip) | 120 | - | start | Must (slice) |
| SPIKE GUARD (chip) | 150 | - | start | Must (slice) |
| CHARGE KIT (chip) | 120 | - | start | Must (slice) |
| EXCHANGER (chip) | 100 | - | 3 wins | Must |
| ENERGY SAVER (chip, 2 slots) | 250 | - | 6 wins | Must |
| W-TANK (refills every weapon; pause label `W.TANK`, consistency-23) | 50 | 2 | 3 wins | Should |
| RACING COLOURS (×4 palettes, data only) | 150 each | - | 8 wins | Could |
| GARAGE tab (§9.4) | free | - | the first PART owned | Could (bundle) |
| AFTERIMAGE 120, JET TUNER 150 | | | | Won't (cut, R2.5) |

- Prices do not change with difficulty. Difficulty lives in combat, not in the till. 1993 RULES (Could) closes the shop.
- **Why these prices:** E-tank 40 ≈ half a Bronze clear; the starting chips (120-150) ≈ two decent clears each, bought
  around the 3rd-4th venue; ENERGY SAVER (250, 2 slots) is the luxury; the +20 % bolt chip is a *prize* (SHERIFF STAR),
  not a purchase, so money can't buy more money.
- In the slice (v0.1) the shop sells the E-tank, the 1UP and the three starting chips.

---

## 9. Chips (SYS-CHP-1/2) [new-code] M, Must

### 9.1 The framework (SYS-CHP-1) [new-code] M, Must (v0.1)

- Chips are passive, one bit each, in `meta.md`'s **3-byte CHIPS_OWNED and CHIPS_EQ** (the bit order is §9.2's; meta
  owns the bytes, consistency-11). v1.0 uses bits 0-13; bits 14-17 are reserved now for the Could bundle so the save
  layout, frozen at v1.0, never needs a migration for it; 18-23 are spare.
- Equip and unequip them at the Pit Stop, or on the pause menu's CHIPS page, at any time. 4MI's items are always on;
  GP lets you choose because the slots are limited. On the CHIPS page **B opens the help page** (R2.10).
- Each chip costs 1 slot. ENERGY SAVER and DARUMA cost 2. Slots = 2 + one per Beat plate, max 6 (§10).
- **The second-wind family** (R2.6, design-9): **YASHICHI and DARUMA cannot be equipped together**; equipping one greys
  the other out, and both help pages say so.
- Each chip has a **help page** (a 4 × 28 window; `story.md` §8 owns every word, EN and JP, and marks the pages that
  are cryptic on purpose). Help pages for the 14 v1.0 chips are Must text (R4.5).
- Body effects (knockback, i-frames, spikes, damage, the second wind) apply to Rock only, never to Break Man.
- A **source attribute** per chip (0 found, 1 shop, 2 venue, 3 garage, 4 moral) is the rating's input (§9.5).

**Why 14** (R2.5, design-6, scope-21): the 8 venue behaviour chips are the 4MI lesson-3 family (prizes for *how* you
play, BRIEF §5.4), the Energy Balancer is vanilla's own passive item, and 5 shop chips give Eddie a catalogue. That is
the BRIEF's "about 14". With 2-6 slots, 14 chips are real choices, not more power.

### 9.2 The fourteen v1.0 chips (SYS-CHP-2) [new-code] M, Must

The venue docs own the gates; this doc fixes the effects, so no two chips do the same thing. Every venue gate is Must
(R2.5, scope-3), so each venue doc must make the gate's set piece Must too (R0.4): Yamato's DARUMA chip needs its daruma
otoshi (T8) in the Must core, or another Must gate.

| Bit | Chip | Exact effect | Source | Slots | Rung |
|---|---|---|---|---|---|
| 0 | **ENERGY BALANCER** | A weapon-energy pickup the equipped weapon can't take (slot 0 equipped, the weapon full, or Break Man in) goes to the **owned, non-full weapon with the least energy** (ties: menu order). If all are full, it falls through to the base rule (§12.2). The vanilla behaviour as measured by the critic (buster equipped → lowest weapon), extended to the "weapon full" case | **Found**: Tomahawk room 1C, vanilla object `$8A`, kept (venues_a §3) | 1 | v0.5 |
| 1 | **SHOCK ABSORBER** | No knockback: the 30-f hurt state is skipped and Rock keeps control. The blink is unchanged, so total safety per hit drops from 90 f to 60 f (the trade-off) | Shop 120 | 1 | v0.1 |
| 2 | **SPIKE GUARD** | Once per life, touching spikes at HP ≥ 2 sets HP to 1 instead of killing; 120 i-frames (4MI's SHOCK GUARD, which was unlimited). "Spikes" include any stage hazard a doc flags SPIKE (fortress's force beams, when H2 returns) | Shop 150; free and slotless in CASUAL (GUARDS) | 1 | v0.1 |
| 3 | **CHARGE KIT** | Buster charge thresholds 36/90 → 24/60 f. Power and Super 45 → 30 f (Burning Knuckle too, in v1.1). Break Man unaffected | Shop 120 | 1 | v0.1 |
| 4 | **EXCHANGER** | A life pickup at full HP becomes weapon energy 2:1 (small 1, large 5), routed by §12.2 (4MI's EXCHANGER, credited) | Shop 100 | 1 | v0.5 |
| 5 | **ENERGY SAVER** | Weapon costs halved, rounded with a per-weapon carry bit: a cost-1 weapon charges every other shot; 3 → 2, 1, 2… | Shop 250 | **2** | v0.5 |
| 6 | **YASHICHI** | Once per stage, the first time HP falls to 4 or less (and Rock survives), it **refills HP to full**. The Yashichi was Capcom's full-restore item. Second-wind family. Feedback: the refill sound, the bar filling and a pop line; a pinwheel sprite is Should | **Venue, Wind**: juggle one POW through 8 hits (venues_a §1.6) | 1 | v0.5 |
| 7 | **KAISHIN** | Every **12th damaging hit on a boss** in a fight is an **EXCELLENT MOVE**: +2 damage (the cell's damage + 2, at most 6), a chime SFX and the EXCELLENT MOVE style act. Deterministic, so records stay fair; criticals are Won't (R2.4). `EXC_COUNT` resets when a boss bar fills | **Venue, Knight**: kill the Metal Metslime (venues_a §2.7) | 1 | v0.5 |
| 8 | **SHERIFF STAR** | +20 % on every scorecard payout (replay improvements included) and on prize bolts, rounded down | **Venue, Tomahawk**: reach the Sheriff with no townsfolk hit (venues_a §3.7) | 1 | v0.5 |
| 9 | **AUTO RECOVER** | After 60 f with no input, +1 HP every 30 f up to max. Off while a boss bar is shown | **Venue, Plant**: the PITFALL PERFECT (venues_a §4.4) | 1 | v0.5 |
| 10 | **SNOW CHAINS** | Ice floors (types 5/`$15`) grip like normal floor: no momentum. Falling icicles bounce off the helmet harmlessly | **Venue, Blizzard**: never destroy a Toppy (venues_b §1.5.3) | 1 | v0.1 (the slice's venue chip) |
| 11 | **FIREPROOF** | Burning oil and other fire floors (the ignited collision `$F`) deal 4 with knockback instead of killing. Fire projectiles (a FIRE flag per type) do half, rounded up | **Venue, Flame**: reach the shutter with no oil ignited (venues_b §2.5.3) | 1 | v0.5 |
| 12 | **CENTURION** | When a boss bar finishes filling, a Centurion-bot hovers beside Rock and absorbs the first 3 projectiles that would hit him. One utility (§3.0), one GP-COMMON tile, and a GP branch in the bullet handler `$38:$9028` | **Venue, Centaur**: free the three statues with full charges (venues_b §3.6.3) | 1 | v0.5 |
| 13 | **DARUMA** | Once per life, a hit that would kill at HP ≥ 2 leaves 1 HP. Pits and spikes excluded (4MI's SKULL AMULET, once per life). Second-wind family. story's proposed hidden function (twice per life after 7 KOs) is **rejected** (consistency decision 33); story's page uses its fallback last line | **Venue, Yamato**: win the daruma otoshi without touching its head (venues_b §4.6.3) | **2** | v0.5 |
| 14-17 | IRON HELMET, THERMOS, BIRD SEED, Y-TURBO | reserved for the Could bundle (§9.4) | | | |

### 9.3 The cut chips: Won't (v1) (R2.5)

Kept here as notes for a later version, not as v1.x content:

- **AFTERIMAGE** (shop 120): the post-hit blink lasts 90 f instead of 60. Cut: a pure safety net (R2.6).
- **GLIDER** (garage GUST + FEATHER): in Jet form, holding A with an empty tank glides at ≤ 1 px/f.
- **JET TUNER** (shop 150): fuel 19 → 27 units. Cut: the Jet is already the strongest traversal tool.

### 9.4 The Could bundle: PARTs, the garage, Mr. Y's booth and Y-TURBO (SYS-CHP-3/4) [new-code] M, Could (cut-line 9)

R2.5: these four ship **together, and together with the tag partner**, because the booth's cost is the partner.

**PARTs (SYS-CHP-3).** The featured-enemy tells already exist in v1.0 (§4.7). With the bundle, **the first thematic kill
of a venue's featured enemy per save drops its PART**, a gear capsule stamped with the venue's letter (meta's
PARTS_GOT). Later thematic kills drop a normal item.

| PART | Venue | Featured enemy (the venue doc's choice) | Thematic weapon (= the champion's weakness) |
|---|---|---|---|
| SNOW | Blizzard | snow robot `$4D` (default) | F.BLAST |
| GUST | Wind | shield-cars `$34` (venues_a) | C.FLASH |
| SEED | Plant | scorpions (venues_a) | B.ATTACK |
| EMBER | Flame | Fire Telly `$2C` (default) | W.STORM |
| KATANA | Yamato | samurai `$A2` (default) | SILVER.T |
| **SPUR** (was FEATHER: design-11) | Tomahawk | cowboy gunners `$6C` (venues_a; no totem, R3.4) | PLANT.B |
| CREST | Knight | lance knights `$6E` (venues_a) | Y.SPEAR |
| SHELL | Centaur | seahorse `$C4` (default) | KNIGHT.C |

**The garage** (a Pit Stop tab, free to use) builds from pairs. Owning one PART of a pair shows "KATANA + ???", the
in-menu hint.

| Recipe | Result | Why the pair |
|---|---|---|
| KATANA + CREST | **IRON HELMET** (bit 14): a hit of 2+ is halved (rounded up) on 1 frame in 8 (LFSR), and always at HP ≤ 4 (4MI's METALL'S HELMET, credited) | a sword and a shield, forged into a helmet |
| SNOW + EMBER | **THERMOS** (bit 15): using an E-tank also adds 10 to every owned weapon, and the tank pours at 1 HP per frame | hot and cold, kept apart |
| SEED + SHELL | **BIRD SEED** (bit 16): Beat's rescue costs 2 HP instead of 4 and works from HP ≥ 3 | bird food and grit, for Beat |
| GUST + SPUR | **TANK RACK** (not a chip, one save bit): hold 5 E-tanks instead of 4 | wind and a spur, for Rush's saddlebags (GLIDER is cut) |

**Mr. Y's booth and Y-TURBO (SYS-CHP-4): doping in a sports tournament** (the 4MI precedent: inhale Eddie, get the
ENERGY SPLITTER, lose a friend).

- After the HALFTIME RIOT a shady booth appears at the edge of the bracket screen ("MR. Y PERFORMANCE PARTNERS").
  Mr. Y, unconvincingly disguised, offers **Y-TURBO** (bit 17: +1 damage on every hit against bosses, cap 4, and
  charges fill 2× faster) for **any one PART**.
- He asks twice. **The second confirmation states the cost plainly: "BREAK MAN WILL WALK."** (R2.8, design-8; `story.md`
  owns every other word.)
- The cost, permanent for that save (R2.8): **the partner** (FORMS.TAG is cleared, the CALL row greys out, meta's
  BREAK MAN WALKS event plays); **the asterisk** on every medal earned with TURBO equipped; **rating T1**; and **the
  CAPCOM TIMES headline** (story's wording). The PART is spent too, so that pair's honest result can never be built.
- **No secret is lost**: on a doped file every TAG-gated secret uses its full-charge-door fallback (R2.8), and OWNED
  drops BREAK (consistency-38).
- Y-TURBO is inert in Super Wily Castle (its CHIPS row reads `WARRANTY VOID`), story's proposal, accepted inside the
  bundle (consistency decision 32). TURBO stays permanent.
- The judges' debrief never hints at the booth, like 4MI's Energy Splitter.

### 9.5 Rating inputs (R2.7; `meta.md` owns the rows)

R2.7 asks for a rating that reaches 100 with v1.0 content. This doc supplies the chip and economy inputs:

- **T5 (venue chips)**: all 8 venue chips, bits 6-13, all Must.
- **T6 (Eddie's chips)**: the chips with source "shop": **5 in v1.0** (bits 1-5). With the bundle, the garage's 3 chips
  join them (8).
- **T7 (the TURBO trap)** and **T1 (the partner)** exist only when the bundle and the partner ship; **T3 (Exhibitions)**
  is removed in v1.0 (scope-3, decision 8).

A re-derivation that sums to exactly 100 with v1.0 content, offered to meta: CHAMPIONSHIP 40; TEAM 10 = Beat rebuilt 5
+ a partner-free test 5 (R4.2's example: the Riot won without the help capsule); ROUTE 16 = secret exits 8 + all 8 hidden
rooms **4** + all 8 venue chips **4**; GEAR 10 = **2 per shop chip** × 5; MEDALS 9; FAIR PLAY 10; BONUS 5. With the bundle,
meta restores T1, T7's +2 trap and the garage chips in GEAR.

---

## 10. Slots and Beat plates (SYS-BT-1) [new-code] M, Must (v0.5)

- **Slots** = 2 + one per Beat plate, max 6 (BRIEF §5.3). The vanilla plate count is exactly 4.
- **Plates** are in 4 venues: the vanilla four (B Tomahawk, E Yamato, A Knight, T Centaur) or re-homed by the venue docs.
  - GP places each plate as a pickup object (tech's family `$F6`), simpler than vanilla's "boss killed in the second
    room" rule (`$3F:$F518`).
  - They are saved in meta's SECRETS b3. On replays they become tokens (§6.7).
- **B-E-A-T complete → Beat joins as the pit rescue** (vanilla's BEAT weapon slot becomes MAGNET BEAM, §3.10). 4MI's
  "friends are mechanics", made friendlier:
  - **Trigger**: Rock falls into a pit with HP ≥ 5, **and Beat has not rescued on this screen yet in this stage run**
    (R2.6: once per screen; a per-run mask of screen ids, `BEAT_USED`, deaths included).
  - **Effect**: Beat (player slot 4) swoops in and drops Rock on the **last safe ground**: the last position where Rock
    stood ≥ 8 f on a solid, non-hazard floor (`LASTSAFE` in the run block). This is a locked moment: Beat's set `$29`
    (15 tiles) streams into the weapon slot, the weapon's lingering objects end first, and the slot set streams back
    when Rock lands (§1.4).
  - **Cost**: **4 HP**, then 60 i-frames. No life is lost.
  - CASUAL lends Beat from the start (GUARDS, "Beat on loan"). Under 1993 RULES (Could), complete plates give the rescue:
    the closest thing to vanilla's BEAT weapon (design-18).
- The 4MI precedent was 3 HP at HP ≥ 4. GP's 4/5 matches RM6's harsher contact damage (bosses hit for 4-5) **(tune)**.
  The bundle's BIRD SEED lowers it to 2 HP from HP ≥ 3.

---

## 11. The tag partner: Break Man (SYS-TAG-1) [new-code] L, Should (cut-line item 2)

**R4.2: the playable partner is Should; the NPC Break Man is Must and is not a systems item** (cutscenes, the Riot, H5,
W3 and the debrief are `story.md`'s and `fortress.md`'s, drawn as an NPC composite from Rock's sheet). The moveset is in
§3.11. These are the rules (CX's Quick Man pattern, credited):

| Rule | Value |
|---|---|
| Joins | at **HALFTIME RIOT 0E**, with story S20's Rule 9 lines played in place (R4.2). That sets FORMS.TAG (`meta.md`) when the partner ships |
| Body | a **slot-0 character variant** (R1.12, feasibility-14): a character byte (0 Rock, 1 Break Man), his own physics constants (§3.11), Rock's HP stashed in WORK, and his 128-tile sheet streamed during the beam-in, on the form-swap stream (16-20 f, the beam-in animation covers it). No separate object family (tech drops `$FC`) |
| Call | a **pause-menu row, `CALL`, confirmed with A** (R2.10). Rock beams out; Break Man beams in at the same spot with **20 HP** and his whistle jingle (the 2-s jingle is Must music anyway, R5.2, for the NPC) |
| Frequency | once per life: the call flag resets at respawn and at stage start |
| Swap back | **START** (he has no pause menu). Rock beams back in with **the HP he left with**, his form sheet and slot set re-streamed. Break Man's remaining HP is discarded |
| Retreat | Break Man at 0 HP, in a pit or on spikes **retreats** ("Tch. Your turn.", story's words): no life is lost and Rock returns with his HP, **but the call is used up for the rest of the stage** (R2.6, design-9) |
| Not allowed | while a boss bar fills; in the Opening; on screens in the stage's NO_TAG mask (tech's 32-bit screen mask, R1.14); during a set-piece sheet; on a doped file (§9.4) |
| Pickups | life heals him; weapon energy routes as if slot 0 were equipped (§12.2); no tanks (no menu) |
| Scoring | his HP loss counts in `L`; his kills and boss hits are category BREAK; the TAG TEAM style act |
| Tag gates | shutters stamped with **his yellow-scarf emblem** open only to Break Man, and lead only to optional content. **Without the partner (v1.0) and on a doped file, every TAG room is a full-charge door** (R4.2, R2.8) |
| Rating | T1 exists only when the partner ships (§9.5) |

Why the retreat costs the rest of the stage and not a life: the call is still meant to be used (a spare body that can
cost a life gets saved for emergencies and never used; CX's Quick Man is rarely seen), but it must not be a renewable
safety net (R2.6). 20 HP plus double knockback keeps him from being a better Rock.

---

## 12. Pickups and economy rules

### 12.1 Vanilla, measured [seen, ds `items.py`]

| Type | Pickup | Effect |
|---|---|---|
| `$38` | small life | +2 HP |
| `$39` | large life | +10 HP |
| `$49` | small weapon energy | +2 |
| `$4A` | large weapon energy | +10 |
| `$37` | 1UP | +1 life |
| `$1D` | E-tank | +1 |

**Drops** [code, ds]: when a normal enemy dies, its explosion (type `$17`, `$30:$81E8`) picks with `$3E:$CC54` (a
cumulative-weights pick against RNG `$DF`).

- First table `$30:$8212` = `1F E0`: **31/256 = 12.1 %** of kills drop something.
- After an LFSR step (`$3E:$C88D`), a second table `$30:$8214` = `18 5F 20 58 10` picks from `$30:$8219` =
  `39 38 4A 49 37`:

| Item | Share of drops | Share of kills |
|---|---|---|
| small life | 37.1 % | |
| small weapon | 34.4 % | |
| large weapon | 12.5 % | |
| large life | 9.4 % | |
| 1UP | 6.3 % | ≈ 0.76 % |

**Deaths** [seen, ds `jet.py`]: HP refills; **weapon energy does not** (Y.SPEAR 5 and W.STORM 0 stayed after a respawn).

**Energy Balancer** (critic): with the buster equipped, a weapon pickup goes to the lowest weapon. Without the Balancer
it is wasted. With a weapon equipped it refills that weapon.

### 12.2 SYS-PU-1: GP routing [new-code] S, Must (v0.1)

A **weapon-energy** pickup:

1. If a weapon is equipped and not full, it goes to that weapon (vanilla).
2. Otherwise, with the BALANCER chip, it goes to the lowest non-full owned weapon.
3. Otherwise it becomes **HP at half value** (small +1, large +5; CX's rule, credited). If HP is full, it is wasted.

A **life** pickup:

1. It goes to HP.
2. At full HP with the EXCHANGER chip, it becomes weapon energy at 2:1, routed as above.
3. Otherwise it is wasted.

Why rule 3: vanilla wastes the pickup, which the critic saw. Turning it into HP removes dead pickups. The Balancer then
becomes a *choice* (energy instead of HP) rather than the only way not to waste a capsule. That is fair now that it
costs a slot.

### 12.3 Other rules

| Rule | Value | Tags | Tier |
|---|---|---|---|
| **Drops** (SYS-PU-2) | One byte selects the first weight (data only): NONE 0 / LESS 16 (6.3 %) / **NORMAL 40 (15.6 %)** / MORE 256 (every kill). The vanilla item mix is kept. NORMAL sits slightly above vanilla's 12.1 % because GP's weapons are used more. 1993 RULES' "vanilla 12.1 %" is derived from the RULES bit, not a DROPS value (consistency-11) | engine-ok + new-code S | Must |
| **Pit-crew refill** (SYS-PU-3) | On respawn after a death: NORMAL gives every owned weapon +max(4, ⌊missing/2⌋) (4MI's ENERGY CHARGER, credited); CASUAL refills them fully; **HARD gives nothing** (R2.9) | new-code S | Must |
| **Game over** (SYS-PU-3) | CONTINUE restarts the stage (vanilla) with the preset's lives, full weapons and the E-tank floor. No tank penalty: the lost run is the penalty | new-code S | Must |
| **Envelopes** | sponsor envelopes (+30 bolts) in every hidden room (§7) | new-code S, new-art 1 icon | Must |
| **E-tank** (SYS-PU-4) | heals +1 HP per **2** f (vanilla 4 f, `$38:$9537`): a full bar in 54 f instead of 108. Hold max 4 (shop cap) | new-code S | Should |
| **W-tank** (SYS-PU-4) | a new pause-menu item (`W.TANK`) beside the E-tank: refills every weapon. Hold max 2. Shop (3 wins) and rare hidden placements | new-code S, new-art 1 icon | Should |
| **Overflow** (SYS-PU-4) | a 1UP at 9 lives → +10 bolts; an E-tank at 4 held → +20 bolts | new-code S | Should |

---

## 13. Difficulty and configuration (SYS-DIF-1/2/3/4)

### 13.1 Settings

Each setting is read at one place, the 4MI lesson: "accessibility knobs belong in the combat code". `meta.md` owns
where each byte lives: the difficulty group is per file (meta §11.2, accepted), the rest is global.

| Setting | Values | Read by | Scope | Tier |
|---|---|---|---|---|
| DAMAGE | ×0.5 / ×1 / ×1.5 / ×2 (round up, as in 4MI) | player hurt `$38:$8F72` | file | Must |
| LIVES | 1-9 (start and continue) | new game / continue | file | Must |
| E-TANK FLOOR | 0-4 | new game / continue | file | Must |
| DROPS | NONE / LESS / NORMAL / MORE | `$30:$8212` weight | file | Must |
| REFILL | NONE / HALF / FULL | respawn | file | Must |
| GUARDS | OFF / ON (SPIKE GUARD + Beat on loan, slotless) | stage start | file | Must |
| CASUAL | OFF / ON (the CASUAL layout tier and lever values, §13.4) | stage start (`LAYOUT_TIER`) | file | Must |
| HARD | OFF / ON (the framework; §13.5) | `IFHARD`, `LAYOUT_TIER` | file | Must |
| RULES | GP / 1993 | everywhere (§13.6) | file, NEW GAME only | Could |
| ANNOUNCER | ON / DEATHS ONLY / OFF | the commentator bus | global | Must |
| FLASHES | NORMAL / REDUCED | SYS-FX-1 and every doc's flashes | global | Must |
| INPUT LAG | 0-6 frames | `REFLEX`, the quick-draw (§1.6) | global | Must |
| MMC5 AUDIO | ON / OFF | sound driver (`art_audio.md`) | global | art_audio's tier |
| SELECT SWAP | FULL / WEAPONS / OFF | §1.1 | global | Must |
| 2P SHIFT | ON / OFF | §1.5 | global | Should |
| LANGUAGE | JAPANESE / ENGLISH (ENGRISH is Could) | text engine | global | Must |

CRITICALS is gone (criticals are Won't, §14). Any hand edit after choosing a preset shows the preset as **EDIT** (4MI).

### 13.2 Presets

| | CASUAL | NORMAL | HARD (v1.0) | 1993 RULES (Could) |
|---|---|---|---|---|
| DAMAGE | ×0.5 | ×1 | ×1.5 | ×1 |
| LIVES | 5 | 3 | 3 | 3 |
| E-TANK FLOOR | 2 | 0 | 0 | 0 |
| DROPS | MORE | NORMAL | **LESS** | vanilla 12.1 % (from the RULES bit) |
| REFILL | FULL | HALF | **NONE** | NONE |
| GUARDS | ON | OFF | OFF | OFF |
| CASUAL | **ON** | OFF | OFF | OFF |
| HARD | OFF | OFF | **ON** | OFF |
| RULES | GP | GP | GP | **1993** |
| Bolts | yes | yes | yes | none (the card is shown "for the record") |

- **Scores use the same formulas in every preset.** The record shows a C/N/H/93 badge per medal. Accessibility is not
  punished, and records stay honest.

### 13.3 The DIFF bits and the layout tier (proposal to `meta.md`, which owns the bytes)

consistency-15 found that the three docs' HARD tests named three different bits. With criticals gone, DIFF A becomes:

| Bit | Meaning |
|---|---|
| b0-1 | DAMAGE (0 ×1, 1 ×0.5, 2 ×1.5, 3 ×2) |
| b2-3 | DROPS (0 NORMAL, 1 LESS, 2 MORE, 3 NONE) |
| **b4** | **CASUAL** (`CFG_CASUAL`, R2.9; was CRITICALS) |
| **b5** | **GUARDS** (moved from b6) |
| **b6** | **HARD** (moved from b5, so `BIT DIFF_A` puts it in V) |
| b7 | RULES = 1993 (N) |

Every doc's code uses **tech's macros, never raw bits**: `IFHARD` = `BIT DIFF_A / BVC skip`; `IF1993` =
`BIT DIFF_A / BPL skip`; `IFCASUAL` = `LDA DIFF_A / AND #$10 / BEQ skip`.

**The layout tier** `LAYOUT_TIER` is computed by tech once at stage start (consistency-16, `tech.md` §5.5): 3 (1993) if
RULES; else 2 (HARD) if HARD; else 0 (CASUAL) if CASUAL; else 1 (NORMAL). tech's poke-list header mask (b0 CASUAL, b1
NORMAL, b2 HARD, b3 1993) applies a list when `mask & (1 << LAYOUT_TIER)` ≠ 0. So a NORMAL file with HARD switched on (preset EDIT) gets the HARD tier,
and CASUAL has a tier of its own.

### 13.4 SYS-DIF-4: CASUAL and the standard lever list [new-code] S, Must (v0.1)

R2.9 (design-7): CASUAL gets a bit, CASUAL poke lists in tech's format, and **one standard lever list that every stage
fills in**. The stage docs own the values; this doc owns the levers and the helpers that apply them (§1.6).

| Lever | CASUAL rule | Mechanism |
|---|---|---|
| Reflex windows | ×2 (the quick-draw: 40 f, R3.5) | `REFLEX` (tech's `TIERVAL` + INPUT_LAG), the quick-draw table |
| Mash counts | −40 % (⌈0.6 n⌉); **hold-to-struggle allowed** (a held A or B counts once per 6 f) | `MASH n` |
| Set-piece timers | +50 % | `TIERVAL`, or a CASUAL poke on the object's `arg` |
| Checkpoints | +1 per section | a dormant checkpoint object woken by a CASUAL poke (`tech.md` §5.5) |
| Skill-gated secrets | relaxed by one step, which the stage doc names (e.g. "8 POW hits → 6", "no townsfolk hit → at most 1") | `IFCASUAL` in the secret's predicate, or a CASUAL poke list |

The table every stage doc carries (one row per lever it uses; "none" is a valid answer):

| Lever | Where (screen, object) | NORMAL | CASUAL | How |
|---|---|---|---|---|
| reflex | e.g. the quick-draw at Tomahawk's arena | 24 f | 40 f | SC8 table |
| mash | e.g. a GRAB | 10 presses / 90 f | 6, or hold | `MASH 10` |
| timer | e.g. a bonus round | 40 s | 60 s | `TIERVAL` |
| checkpoint | section 1 | 2 | 3 | tech's dormant checkpoint object, woken by a CASUAL poke |
| secret step | the venue chip's gate | as designed | one step easier | `IFCASUAL` |

The venue and fortress docs' earlier one-off CASUAL ideas (venues_b's Toppy refill, fortress's POCKET slide and H1
ledge) are re-expressed as rows of this table, or dropped.

### 13.5 SYS-DIF-2: HARD [new-code] M; framework Must (v0.5), content Should (cut-line 3)

- **v1.0 HARD = ×1.5 damage, drops LESS, no refill** (R2.9, scope-19). The framework hooks stay: `IFHARD`, the layout
  tier, HARD poke lists in tech's format and the stage record's `POKE_LIST`. The only per-stage HARD number in v1.0 is the
  quick-draw's 18 f (R3.5).
- **Should (v1.1, cut-line item 3)**: per-stage HARD poke lists ("one meaner screen per section", 4-12 pokes per venue)
  and boss AI branches (`IFHARD`; 4MI has 121 such tests), added stage by stage from the data the stage docs already
  wrote.
- The combat tables do not change in HARD; the ×1.5 damage and (later) the patterns do the work.
- **One poke-list format**: tech §5.5's (scope-25, R1.10). Round 1's 3-byte systems format is withdrawn.

### 13.6 SYS-DIF-3: 1993 RULES [new-code] M, Could (cut-line 10)

design-18: **the rules change, the content does not.** A NEW GAME choice only (meta).

- **Forms**: change only through the pause menu, with the full vanilla transform. The weapon resets to the buster
  (`$38:$93F7`). Forms cannot fire weapons.
- **Combat**: the 1993 column of §4.5 for every fight, new ones included: vanilla damage and i-frames by family.
  Vanilla's Knight shield is kept. **SC5 stays on** (the punch is the 1993 player's answer to Gamma, reached through the
  menu); SC6, COUNTER (SC10) and Knight's HEALMORE are off.
- **Off**: alt fires, synergies, the parry, chips, the shop, bolts, the respawn refill.
- **On**: saves; **the Beat rescue once the plates are complete** (the closest thing to vanilla's BEAT weapon); the
  SELECT weapon cycle (a control, not a rule; it can be turned off); M.BEAM and the Super Adaptor (through the menu).
- **The Energy Balancer** is the vanilla passive item, found where GP places the chip.
- It is finishable because of the normal-route rule (§2.4).

### 13.7 Test matrix (scope-26, RULINGS §6)

- Golden movies run on NORMAL + EN only. One smoke movie per other setting per milestone: CASUAL, HARD, REDUCED FLASHES,
  SELECT SWAP OFF, INPUT LAG 6, JP. Movies are re-recorded only at gates. Test overhead is about 10 % of code sessions,
  in the ledger's overhead rows.
- Systems' own checks: the GP_BOSSHIT chart assertion (every v1.0 row has every Must column); the FRZ_KIND movie (the Ice
  Block encases every placed freezable type, and no NOFREEZE type freezes); the death-hook coverage readout (EXTRA
  CONFIG's "last kill category"); the stream timing (swap frames logged in the lag report).
- **The safety-net measurement** (R2.6): deaths per stage with a full loadout against an empty one, on Blizzard at M4
  and on all 8 venues at M6. If the full loadout cuts deaths by more than about half, the nets are tuned (Beat's cost,
  YASHICHI's threshold) before new content.
- Every v1.1 alt or synergy ships with its own smoke movie.

---

## 14. Criticals: Won't (v1) (SYS-CRT-1)

R2.4 (design-6): criticals are cut. **KAISHIN is always the deterministic EXCELLENT MOVE** (+2 on every 12th boss hit,
§9.2), so the Knight venue's prize works and records stay fair.

- Gone with them: the CRITICALS setting (DIFF A b4 now holds CASUAL), the "CRIT!" pop (its GP-COMMON tiles are freed),
  the "pikoon" SFX, the CRITICAL style act, and the need for Time Attack and GP Rush to force anything off.
- The dropped design, for the record only: an LFSR roll (`$3E:$C88D`, never the frame counter) at 1/128, ×4 at HP ≤ 4;
  +2 damage on bosses (cap 6), ×8 on mooks.

---

## 15. What this doc needs from the others

### 15.1 Data and RAM (for `tech.md`, which owns the map)

Following rm6 lesson 3, GP state lives in PRG-RAM (WORK). Only hot, per-frame bytes go in vanilla's free RAM.

| Where | Bytes | Contents |
|---|---|---|
| Free RAM, tech's `SYS_HOT` `$06BD-$06C8` | 12 | `SELHOLD` (SELECT hold timer), `SELFLAGS` (SEL_USED, SWAPMASK), `LASTW`, `SWAPSTATE` (swap frame count, queued form), `WEAK_GATE`, `FLASH_GATE`, `ALT_LOCK` (the 10-f interact lock), `BOSS_ROW`, `EXC_COUNT` (KAISHIN), `MULTI_T` (multi-kill timer), `TSTOP` (Time Stop, v1.1), 1 spare |
| WORK, per object slot (tech's `$6000-$61FF`, stride 32) | 4 arrays × 23, + 1 | `LASTHIT` (`$6060`), `LATCHSRC` (`$6080`), `REHIT` (`$60A0`), `FREEZE` (`$60C0`; on a boss slot it is the stall count), and **`ENC_CLASS`** (the encased enemy's saved class nibble), which tech places in its WORK ledger. It cannot share a GPV that a GP sub-id's AI uses |
| WORK, run block (tech's `$6250-$62FF`) | ≈ 32 | T (3), L (2), K, CATS (2), OWNED (2), SECR, STY, TANKS, the kill count, run flags (YASHICHI used; DARUMA, SPIKE GUARD and the partner's call used this life; the call used up for the stage), `BEAT_USED` (4: screen mask), `LASTSAFE` (3: screen, X, Y), `MULTI_CAT`. (`LAYOUT_TIER` is tech's loader byte) |
| Save (`meta.md` owns the bytes) | | BOLTS (2); CHIPS_OWNED (3) and CHIPS_EQ (3) in §9.2's order; E-TANKS; W-TANKS (Should); FORMS (POWER, JET, SUPER, TAG); FORM_DEBUT; plates (SECRETS b3) and envelopes (SECRETS b4); **PRIZES** (4 B, one bit per placed prize); STAGEREC[24]: best score + preset badge, best PAY, asterisk bit; BASS_ADAPT; WEAKFOUND (Could). Bundle (reserved now): PARTS_GOT, PARTS_USED, TANK RACK, RATEFLAGS.DOPED. **Removed**: METALLS, the DOVE flag; BREAK_JOINED is FORMS.TAG (consistency-11) |
| Per-file DIFF bytes and the system block (`meta.md`) | | the §13.1 settings; DIFF A as §13.3; INPUT LAG global |
| ROM tables (`$7F` or a systems bank) | ≈ 1.5 KB | GP_BOSSHIT cells (640 B); the ALT override (10); i-frame class → frames (16); column → category (32); the NOFREEZE override list (tech's `SRCTAB` and derived `FRZ_KIND` tables are tech's); the 8 featured-enemy tables (8 × 16); chip data and source bytes (18 × 4); the 3 frozen handlers (≈ 120); the venue → weapon-slot map (8) |

### 15.2 Hook sites (tech confirms them and lists them in the hook registry)

| Area | Addresses |
|---|---|
| Input | joypad read `$3E:$C711` |
| Firing | fire dispatch `$38:$856A` (tables `$8556/$8560`); shooting poses `$3F:$E130` (relocate, 4th row); shot by form × level `$38:$854A`; charge `$38:$8651`; shot allocator `$3F:$E514/$E516`; `util_spawn` (tech) |
| Menu and forms | buster reset `$38:$93FE`; docking `$38:$965F`; menu-close CHR loads `$38:$95CC-$95F5` (form sets `$38:$96C7`, weapon sets `$3F:$F70C`, weapon palettes `$38:$962F`); adaptor derivation `$38:$931D`, `$3B:$BA3F` |
| Shot vs enemy | latch stores `$38:$9024`, `$38:$906A`, `$38:$90E1`, `$38:$9E74`, `$30:$8ADD`; shield `$38:$90A2`; bullets `$38:$9028`; PLANT.B break `$38:$9034`; energy `$38:$9E8E`; C.FLASH strobe `$3E:$DECD` |
| Player contact | `$38:$8EA0` (extend to utility slots 4-7 for platforms); the pause-close clear `$38:$9624` (keep utilities when the weapon is unchanged); platform `$38:$8F96`; hurt `$38:$8F72` (`$A2`; the DAMAGE multiplier, SC11) |
| Damage | champions `$31:$997D` (`$99B7-$9A2F`, `$9AD6`); fortress `$3F:$EF64` (`$EF66-$EFE1`); normal `$3F:$E9D7/$EA20/$EA6E/$EA99/$EAB7`; hit effects `$3F:$EB76` |
| Deaths | `$30:$81C7` (type `$17`), the type `$25` init, `$3F:$ED42` |
| Drops | `$30:$81E8` (weights `$8212`) |
| Objects | object loop `$3F:$E438` (the frozen tick at `$E443`); yield `$E46C`; end turn `$E47B` |
| Player | E-tank `$38:$9537`; Jet HUD `$3E:$CF90` |

### 15.3 Cross-doc dependencies (each doc must agree with these)

**What the Musts lean on (R0.4)**, all Must in their owners' docs: tech's CHR stream with the unrolled copier, the
`$9B` audit (before H3), families `$FB`/`$FD`, the frozen-tick patch, the commentator bus, the stage-attribute fields
(`FORT_COL`, `SCORE_ID`, `PAR`, `POKE_LIST`, the NO_TAG mask), the poke lists and the map-edit service; meta's results
screen, Pit Stop, CONFIG and save fields; story's first-weakness lines and the 14 chip help pages (R4.5); art's
GP-COMMON tiles, the Ice Block and M.BEAM tiles, the Super Rock sheet, the KAISHIN chime and the 2-s whistle jingle; the
venue docs' chip gates and hidden rooms; fortress's H1, H3 (with its practice beat), the Riot, W2 and W3 (with the gift).

- **venues_a.md / venues_b.md**:
  - **Normal routes:** never need a form, an alt, a synergy or Break Man (§2.4). Use floor type E where Jet must not skip.
  - **Weapon tools in v1.0:** the taps, the forms and the Ice Block. Pogo, Wall Spear, Updraft, the held mace, Burning
    Knuckle, Morning Star and Time Stop are Should: any Must secret that uses one needs a fallback (R0.4, R3.1).
  - **Featured enemy:** each venue names one, which dies outright to the champion's weakness weapon: a tell only in v1.0,
    a PART with the Could bundle. No totem; Tomahawk's PART is SPUR (R3.4, design-11).
  - **Scoring data:** each venue gives its VENUE ACT, its secret list and weights (exit 3, hidden room 2, behaviour chip
    2, plate 1), and its TIME par; a replay skip subtracts the piece's length from the par (§6.3).
  - **Money:** one sponsor envelope per hidden room; prizes ≤ 60 per venue. venues_b replaces its bags and chest with
    envelopes, re-prices the vegetables, and fits Y.SPEAR's ledge bolts in the cap (R2.7, consistency-10).
  - **Placements:** 4 venues hold plates; Tomahawk room 1C holds the ENERGY BALANCER.
  - **Chips:** every venue chip's gate is a Must set piece (R2.5, R0.4), Yamato's daruma otoshi included.
  - **Bosses:** each champion's WEAK reaction (SC9), its G/R thematics (§4.3), its own-weapon reaction (SC4, Should),
    and the NOFREEZE notes for their new enemies (`FRZ_KIND`).
  - **CASUAL:** the lever table of §13.4 per venue. **HARD** content is Should.
  - **Set pieces** that change Rock's body use `gp_player_sheet` (buster only on vines and the condor). Every UP verb
    uses `IFINTERACT`.
  - **Answers to their questions:** the vanilla weakness cycle is kept; weakness i-frames are 16 f (venues_b's 8 are
    superseded); Y.SPEAR pierces Knight's shield, and vanilla already did (SC1); Y.SPEAR's tap is vanilla's single spear
    (the pierce is Should polish; Yamato Man may throw volleys himself); DARUMA is once per life at 2 slots; Flame's ABSORB
    heal is a named exception like SC3; objects that react to "a charged shot" test the FULL flag (vanilla AIs keep
    `$13`/`$14`); the rental Jet is a vehicle, not a form (§2.4); the quick-draw windows are 24/18/40 + INPUT LAG.
- **fortress.md**: the v1.0 rows of §4.5 (they may override them) and the v1.1+ rows; SC5 (Gamma: POWER required with
  its plaque, plus the no-risk fist-ride practice beat, R2.11), SC6 (Bass copies only the 4 weapons pre-drawn in his set,
  R3.6), SC10 COUNTER (Should), SC11 CHAMPION BUSTER; the Magnet Beam's 64 px per beam and max 2 (the H1 gap); FORMS.SUPER
  on the H3 screen-12 dock with no YOU GET card; TAG rooms as full-charge doors; envelopes and ≤ 60 prizes per stage; the
  mid-boss and machine defaults; the Riot's auditions on the FULL flag; force beams flagged SPIKE; the RULE column,
  OWNED override and 4 exhibition racing colours (Could, with the Exhibitions); the victory lap's character swap through
  the pause CALL row, when it is built (consistency-30).
- **story.md** (every word): help pages (4 × 28) for the 14 chips and the weapons; commentator lines (`EV_WEAK_FIRST`
  is Must text; `EV_RESIST`, `EV_IMMUNE`, new forms, medals, EXCELLENT MOVE, the YASHICHI and DARUMA pops); the CONFIG
  lines for CASUAL and INPUT LAG; the boot health notice; the partner's lines (Should); the booth's lines and the doped
  headline (Could; "BREAK MAN WILL WALK." is fixed by R2.8); DARUMA's fallback last line; TURBO's WARRANTY VOID (bundle);
  the 1-bolt insurance gag.
- **meta.md**: the results screen; the Pit Stop (v1.0: 5 chips, E-tank, 1UP; garage and booth with the bundle); 3-byte
  CHIPS_OWNED/EQ in §9.2's bit order; PRIZES; STAGEREC[24]; FORMS.TAG (not BREAK_JOINED); DIFF A as §13.3; INPUT LAG in
  CONFIG; the health notice screen; the rating inputs (§9.5); Time Attack and GP Rush use drops NONE (no criticals to
  force off); METALLS and DOVE removed; BASS_ADAPT; WEAKFOUND (Could).
- **tech.md** (round 2, already aligned on most of this): the CHR stream (192 / 96 / 32 B) for form swaps (2 KB),
  slot sets, set-piece sheets and Beat's set, one stream at a time; the M1 spike's 256-B test; the `$9B` audit and the
  `$E130` relocation before H3; family `$FD` for the WEAK! pop and the swap flash; family `$FB` shots with column and
  flags in the sub-id record; `util_spawn` with this doc's caps (§3.0) and the player-contact extension; the
  pause-close clear keeping utilities when the weapon is unchanged (its open question 4); the frozen-tick patch and
  `FRZ_KIND` with this doc's NOFREEZE overrides and the boss stall on the boss slot's `FREEZE` (feasibility-6); LATCHSRC
  in §6.4's format, **including b5 FULL**, at the five latch sites (consistency-20); `ENC_CLASS`; `BOSS_ROW` from
  `FORT_COL` or the sub-id record; `SYS_HOT`; the run block; `IFHARD`/`IF1993`/`IFCASUAL`, `TIERVAL`, `MASH n`,
  `IFINTERACT` and a `REFLEX` macro (`TIERVAL` + INPUT_LAG); `LAYOUT_TIER`-keyed poke lists; `gp_flash_ok()`; the
  death-hook audit; Break Man as a slot-0 character variant (family `$FC` dropped); the IRQ-logic bosses testing the
  stall.
- **art_audio.md**: GP-COMMON tiles (WEAK!: W, K, ! = 3; the swap flash 1; CENTURION 1; 1 spare); the Ice Block's 4
  tiles in B.ATTACK's set; M.BEAM's set (≤ 15); the Super Rock sheet (Must with H3); the envelope icon; SFX: the cycle
  tick, the weak crunch and the KAISHIN chime (Must), the parry ting (Could); the 2-s whistle jingle (Must, R5.2); no
  CRIT! tiles; "?!" only with SC3 (Could); PART icons with the bundle. The form sheets the menu loads are sets `$02`/`$03`
  in bank `$00` (§1.3).

---

## Lessons applied

| Source | Lesson | Where |
|---|---|---|
| 4MI 1 | **Put the weakness in the i-frames**, keep damage 1-4, make the buster a deliberate (but vanilla-gentle) handicap | §4.2-§4.4 |
| 4MI 2 | Separate the mook and boss rules: no i-frames on mooks, only a lingering-hitbox timer | §4.7 |
| 4MI 3 | Behaviour-gated items: the 8 venue chips, effects fixed here; crafting and a moral trade-off kept as one Could bundle | §9.2, §9.4 |
| 4MI 4 | Friends are mechanics: Beat = pit rescue; Break Man = spare body (Should); the booth costs a friend (Could) | §10, §11, §9.4 |
| 4MI 5 | One predicate list drives both the score and the debrief | §6.2 SECRETS |
| 4MI 6 | Old weapons, new jobs: the full punch remains the fortress weapon (vanilla's 4); Knight's shield yields to `$14` | §4.5, SC1 |
| 4MI (systems) | Accessibility knobs read at one place; CASUAL as a real tier, not just numbers; help pages from day one | §13, §3 |
| CX 4 | A partner as a second body with separate HP | §11 |
| CX 6 | Telegraph tools: the scarf emblem on tag gates; featured enemies die to the boss's weakness (an in-stage tell) | §11, §4.7 |
| CX 7 | Damage in tables, the chart generated from them, special cases in visible code | §4.6, §4.8 |
| CX (systems) | A swap must clean up on purpose: lingering objects survive form swaps, and a weapon swap is refused while Rock stands on one; unusable weapon energy becomes HP | §1.1, §12.2 |
| RM6 7 | Adaptors are derived bits, patched at `$38:$931D` / `$3B:$BA3F`; forms couldn't fire weapons only because the menu reset `$0699` | §2.3, §3.0 |
| RM6 8 | Keep quirks on purpose: C.FLRSH, igniting oil, Knight's shield (and Y.SPEAR's vanilla pass), Wind Man's one-hit W.STORM, the Jet sky bypass | §3.9, §3.5, SC1, SC4, §2.2 |
| RM6 3 | GP state in WORK; free RAM only for hot bytes | §15.1 |
| RM6 (vanilla data) | Vanilla's attack bytes are an interface 21 AIs read: keep them, score from a side byte | §6.4 |

## Risks

1. **Slice schedule.** This doc's slice share is about 33 sessions, against RULINGS §6's 25 for all M3 slice systems.
   *Mitigation:* pull the scorecard, bolts and chip framework into M2's results and save work; re-estimate at M4 (R0.1).
2. **The CHR stream.** 2 KB per form swap is 11-13 stream frames at tech's rates (up to 22 with a column paint every
   frame), inside a fixed 16-frame swap. *Mitigation:* the M1 spike measures the copier; a stream is never cut short; the
   flash hides Rock until it ends; one stream at a time, so a swap may wait behind a pop-up's glyphs.
3. **Lag** (R1.8: every occupied slot counts, cap 9). A boss room holds the boss, Rock, up to 3 shots, the WEAK! pop
   and maybe CENTURION and a beam. *Mitigation:* profile on the M4 slice; the pop is optional under load.
4. **Balance.** A 16-f weakness may be too fast with multi-hit weapons; the stagger may still lock some patterns.
   *Mitigation:* everything is one table byte; playtest at M4, with 20 f as the fallback.
5. **Attribution holes.** Enemies with custom death code may skip the death hook, and VARIETY would silently
   under-count. *Mitigation:* shadow6 coverage of every death path; the "last kill category" readout.
6. **`FRZ_KIND` errors.** A wrong kind makes an enemy immortal or fragile while frozen. *Mitigation:* tech derives the
   kinds from a static scan and `dmgmap.json` cross-checks them; the FRZ_KIND movie encases every placed type.
7. **The boss stall** assumes the boss reaches its damage step by `JSR`. *Mitigation:* the M3 check lists NOSTALL
   bosses (shake only); IRQ-logic bosses test the stall once tech moves their logic out of the IRQ.
8. **The weapon-change rule** (lingering objects end) may surprise players used to CX. *Mitigation:* the buzz when
   standing on one, the shatter animation, and the help page.
9. **The v1.0 economy may be rich late** (≈ 1,905 typical against 740 of chips). *Mitigation:* slots bind first; prices
   are one table; the M9 balance pass; the W-tank and colours return as sinks in v1.1.
10. **Safety nets.** Even after R2.6, a 6-slot loadout of SPIKE GUARD, a second wind, CENTURION and AUTO RECOVER is
    strong. *Mitigation:* the M4/M6 measurement (§13.7).
11. **Chip gates on Should set pieces** (a venue chip whose gate a venue tiers Should) would break R0.4. *Mitigation:*
    the gate rule in §9.2 and §15.3.
12. **The Could bundle's doping is permanent.** *Mitigation:* the double confirmation naming the cost, no lost secrets,
    and it ships only with the partner.

## Open questions

1. Does the M1 spike confirm tech's 192 B/frame copier (an 11-frame stream standing still), and is the 256-B blank-band
   mode worth it for the swap?
2. Do all fortress bosses that keep the `$EF64` path reach it by `JSR` (the boss stall)? Checked at M3.
3. Which 4 weapons are pre-drawn in Bass β's set? fortress picks, art budgets (R3.6).
4. Will meta adopt §9.5's rating re-derivation, or another one that also reaches 100 with v1.0 content?
5. Is 0-6 frames of INPUT LAG enough for the user's TV (RULINGS §7 asks about the hardware)?
6. The Plant Barrier's duration and radius (for Petal Storm, Should): measured at M3.

Round 1's questions, resolved: OQ1 F.BLAST's oil ignition is explicit GP behaviour (consistency decision 35); OQ2 the
form sheets differ in 119 of 128 tiles (§1.3); OQ3 tech answered the VBlank budget; OQ4 controller 2 is free; OQ6
VARIETY counts boss hits; OQ7 TURBO is permanent (inside the bundle); OQ8 a retreat uses up the stage's call (R2.6, over
consistency's "keep the free retreat"); OQ9 Exhibition rewards are fixed prizes; OQ10 the Mr. X 1 riders matter only for
Mr. X Returns (Won't); OQ11 criticals are Won't; OQ12 the ★ stays Could.

---

## Changes in round 2

Every change from round 1, with the ruling (`R…`, [`RULINGS.md`](RULINGS.md)) or finding id (`feasibility-…`,
`design-…` in [`review_feasibility_design.md`](review_feasibility_design.md); `scope-…`, `consistency-…` in
[`review_consistency_scope.md`](review_consistency_scope.md)) that caused it.

**Scope and tiers**

1. Added **"v1.0 scope"** with a session estimate and release rung per item; Must totals 49.5 sessions. Updated the
   ledger: `tools/plan/tight.py`'s systems block (46.5 → 49.5) and `tools/plan/tally.py`'s systems rows (re-tiered to the
   round-2 tiers, Must rows summing to the same 49.5). R0.1, R0.2, scope-1, scope-2.
2. Re-tiered every item to Must / Should (v1.1+, in cut-line order) / Could / Won't; the item index (§0.1) and every
   section carry the tier. R0.2, R0.3.
3. Listed what each Must leans on and checked that all of it is Must in its owner's doc (§15.3); secrets may no longer
   rely on a Should tool without a fallback (§2.4). R0.4, scope-3.

**Combat and weapons**

4. Removed the punch re-class: vanilla attack bytes `$11-$14` stay; no AI latch compare is patched (§2.2, §6.4). R2.1,
   feasibility-5.
5. Replaced class-nibble scoring with **LATCHSRC at every latch store** (b0-4 column, b5 FULL, b6 ALT, b7 SYN; the
   column derived at latch time through tech's `SRCTAB` or the GP sub-id record), with the verified store sites
   `$38:$9024/$906A/$90E1/$9E74` and the enemy-side `$30:$8ADD`; LATCHSRC's meaning replaces round 1 tech's "weapon
   slot". R2.1, consistency-20.
6. The half-charge damage bump (`$11` → `$12`) is Won't: it would change a vanilla attack byte. R2.1.
7. Every GP full-power blow (PUNCH★, the Super fist's outward leg, the Break Shot, later Morning Star and Time Fist)
   carries `$14`, so vanilla's punch-only enemies and shield accept it; new objects test the FULL flag. The Super fist
   counts as a full-power blow (fortress's proposal). R2.1, crossrefs.
8. **Frozen tick rewritten**: tech's `FRZ_KIND` per type (cross-checked: 35 `$E9D7`, 5 `$EA20`, 62 `$EA6E`, the rest
   NOFREEZE) with this doc's NOFREEZE override list, three frozen handlers that copy `$E9D7/$EA20/$EA6E` with the yield
   replaced by an end-turn, W.STORM thaws, and a **boss stall** on the boss slot's `FREEZE` that re-points the resume
   address at the boss's own `JSR` (§4.8). R2.2, feasibility-6.
9. **Forms fire every tap** (Must); the dispatch table has alt and synergy columns; the 7 other alts and 8 synergies are
   Should, in a v1.1 order (§3.12) that puts Flare, Feather Fan and Petal Shot last. R2.4, scope-8, design-6.
10. **B.ATTACK's Ice Block is Must, in the Blizzard slice**, fully specified (throw, encase via class 9, shell, boss
    1/30, weapon-change shatter; the oil freeze and slippery top are Should). R2.4.
11. **The parry is Could; criticals are Won't**; KAISHIN is the deterministic EXCELLENT MOVE (+2 on every 12th boss
    hit); the CRITICALS setting, CRIT! tiles and pikoon SFX are gone (§14). R2.4, design-6.
12. Y.SPEAR's pierce and PLANT.B's two-contact barrier moved to Should (tap polish); B.ATTACK's and PLANT.B's cost cuts
    and C.FLASH's dark-room lighting stay Must. scope-2.
13. **SC1 lists Y.SPEAR**, which vanilla already passes through class-3 shields (`$38:$90A9`, verified). consistency-35.
14. **Damage and i-frame tables updated for the v1.0 boss list** (§4.5): Grand Pi-kun (one size), Bass β, Yellow Devil
    MK-VI, Gamma MK-VI phases 1/2, Dark Man MK-VI, **WILY MACHINE 6.5** (vanilla Wily Machine 6 art), the Capsule, the
    mid-boss and machine defaults; Mecha Dragon, Cossack Catcher, METALL 16 and the exhibition guests moved to v1.1+
    rows; Doc Robot (Should) uses a copied Rockman 2 boss's row. Added the Ice Block ALT override, the CHAMP.B column, a
    reserved RULE column, the row and column id tables, and the 1993 column rules. R3.6, R3.7, consistency-18,
    consistency-39, design-18.
15. Added **SC10** (Bass's COUNTER, Should) and **SC11** (the CHAMPION BUSTER, 4/8 and "hits of 2+ become 1", Must with
    W3); SC6's copies use only Bass's pre-drawn weapons; SC5 states its 1993 behaviour and the practice beat; SC4 is
    Should. R3.6, R2.11, crossrefs (fortress proposals).
16. The vanilla `$063E` gate on PUNCH★ against champions is kept (the conservative default), and documented.

**Forms and controls**

17. **Quick swap re-budgeted for the 2 KB sheet**: a fixed 16-frame swap (up to 22 in the worst scroll case) over
    tech's 192 / 96 / 32 B stream, cooldown = stream completion, queued behind other streams, with measured facts on
    the form sets the menu loads (sets `$02`/`$03`, 119 of 128 tiles differ). R2.3, feasibility-7, consistency-5.
18. Added **the per-form `$71-$7F` map** (one owner at a time, the verified weapon-set table), the weapon-change and
    form-change survival rules, the set-piece player sheet (`gp_player_sheet`), Beat's streamed set, and the artcheck
    15-tile rule (§1.4). R2.3, feasibility-7, feasibility-8, consistency-43.
19. **Player-side slots** follow tech's plan (shots 1-3, utilities in 4-7 through `util_spawn`, Beat's rescue in 4);
    this doc sets the caps (Ice Block 1, M.BEAM 2, CENTURION 1, the Should alts 1 each); utilities call `$38:$8FDF`;
    the player-contact search is extended to slots 4-7; utilities survive a pause when the weapon is unchanged (tech's
    open question 4). R1.11, feasibility-9.
20. **SUPER needs tech's `$9B` audit first**; the shooting-pose table `$3F:$E130` has only 3 rows (verified). R1.12,
    feasibility-14.
21. **FORMS.SUPER is set when Rush docks in H3 screen 12, with no YOU GET card.** consistency-28.
22. **Input rules** (SYS-CTL-5): in-stage SELECT = quick swap and toggle only; `IFINTERACT` (UP press, B not held,
    no alt in the last 10 f); Break Man's call is a pause row confirmed with A; help pages open with B on the CHIPS page.
    R2.10, design-21.
23. Added the **mash, reflex and timer helpers**, hold-to-struggle, the quick-draw windows (24 / 18 / 40 f) and the
    **INPUT LAG** setting (0-6 f). R3.5, R2.9, design-13.
24. **§2.4 normal-route rule**: POWER may be required in the fortress with a tell (Gamma phase 2 only in v1.0, with a
    practice beat; no Super lending); stage-lent vehicles are not forms. R2.11, design-3, consistency-12,
    consistency-36.
25. Published the venue id → weapon slot table (`$3F:$F704`, verified). consistency-37.
26. Air-dash and the overheat stall are Won't; the low-fuel pip is Should and uses tech's HUD widget module. R1.10.

**Feedback and accessibility**

27. Added **SYS-FX-1, the flash rule** for this doc's effects: C.FLASH's vanilla strobe (6 flashes in 24 f, 15 Hz,
    measured) becomes one white-out and a fade; machine hit pulses (7.5 Hz in `$EF64`) become one rate-limited pulse;
    a shared `FLASH_GATE`; REDUCED fades. R3.5, design-13.
28. The WEAK! pop is tech's family `$FD` sub-id with art's 3-tile build; the first-weakness icon is a BG icon in the
    glyph strip. consistency-24, consistency decision 29.

**Scoring and economy**

29. Pars renamed and re-listed for v1.0 (Opening-lite, HALFTIME RIOT); **replay skips subtract the piece's length from
    the par** and forfeit its secrets and act. R3.8, R4.3.
30. STYLE acts tiered (SYNERGY KILL, OWN MOVE, TAG TEAM Should; PARRY Could; CRITICAL removed; EXCELLENT MOVE kept).
    R2.4.
31. **Income model re-run for v1.0's 15 stages** (typical ≈ 1,860, completionist ≈ 3,660; 740 of chips). R2.7.
32. **One envelope per hidden room, venues_b's bags and chest included; prizes ≤ 60 per stage, venue or not**; venues_b
    re-prices its vegetables. R2.7, consistency-10, consistency-19.
33. Added Mr. Y's 1-bolt respawn insurance as a bolt flow. R4.3, consistency decision 27.
34. Pit Stop v1.0 stock: E-tank, 1UP, 5 chips; W-tank Should, colours Could, garage Could, AFTERIMAGE and JET TUNER
    cut; the shop opens at 0 wins; the `W.TANK` label. R2.5, consistency-23, consistency decision 14.
35. Exhibition income, the RULE column, the OWNED override and the 4 exhibition racing colours are Could, with the
    Exhibitions. R3.7, consistency decision 20.

**Chips**

36. **14 chips in v1.0** (8 venue, the Balancer, 5 shop) in a **final 3-byte bit order** with bits 14-17 reserved for
    the bundle, so meta's FILE block freezes once. R2.5, design-6, scope-21, consistency-11.
37. **PARTs, the garage, Mr. Y's booth and Y-TURBO are one Could bundle** shipped with the partner; featured enemies
    stay as tells with no PART drop; GUST + SPUR now builds a TANK RACK because GLIDER is cut. R2.5, scope-21.
38. **Safety nets don't stack**: YASHICHI and DARUMA are one exclusive second-wind family; Beat's rescue works once per
    screen; the partner's retreat uses up his call for the stage; the M4/M6 measurement. R2.6, design-9.
39. **Doping (with the bundle)**: the cost is the partner, the asterisk, T1 and the headline; TAG secrets use their
    full-charge fallbacks; OWNED drops BREAK; the second confirmation says "BREAK MAN WILL WALK."; TURBO's WARRANTY VOID
    accepted inside the bundle. R2.8, design-8, consistency-38, consistency decision 32.
40. **Rating inputs re-derived** so 100 is reachable with v1.0 content (§9.5); T1 and T7 only with the bundle; T3 removed.
    R2.7, scope-3.
41. The FEATHER PART is renamed **SPUR**, and "totem" is no featured enemy. R3.4, design-11.
42. DARUMA's hidden function (story's proposal) rejected. consistency decision 33.
43. Help-page drafts removed from this doc: `story.md` §8 owns every word; 14 chip pages are Must text. R4.1, R4.5.

**Partner, Beat, difficulty**

44. **Break Man the partner is Should and a slot-0 character variant**; the NPC is Must and not a systems item; he
    joins at HALFTIME RIOT 0E; TAG rooms are full-charge doors without him; NO_TAG is a screen mask. R4.2, R1.12, R1.14,
    scope-15.
45. Break Man's shots use `$11` and `$14` (the Break Shot is a full-power blow) instead of new class-E bytes. R2.1.
46. Beat's rescue streams set `$29` at its locked moment; under 1993 RULES complete plates give the rescue. R2.3,
    design-18.
47. **CASUAL** gets a bit (DIFF A b4), a layout tier and the **standard lever list** with a template for every stage doc
    (§13.4). R2.9, design-7, consistency-16.
48. **HARD v1.0 = ×1.5 damage, drops LESS, no refill**; per-stage content is Should; one poke-list format (tech's).
    R2.9, scope-19, scope-25.
49. **DIFF A bits proposed to meta** (CASUAL b4, GUARDS b5, HARD b6) with `IFHARD`/`IF1993`/`IFCASUAL` macros, fixing the
    three docs' different HARD bits. consistency-15.
50. **1993 RULES is Could**, "the rules change, the content does not": a 1993 column for every fight, SC5 on, SC6,
    COUNTER and HEALMORE off, the Beat rescue from plates. R2.9, design-18, scope-20, consistency-39.
51. 1993's "vanilla drops" come from the RULES bit, not a DROPS value. consistency-11.
52. Added the **test matrix** and systems' own checks (§13.7). RULINGS §6, scope-26.

**Data and dependencies**

53. §15.1 rewritten: `SYS_HOT`'s 12 named bytes, the per-slot arrays plus `ENC_CLASS`, the run block, the save fields meta
    must hold (3-byte chips, PRIZES, STAGEREC[24], FORMS.TAG) and drop (METALLS, DOVE, BREAK_JOINED). consistency-11.
54. §15.2 hook sites corrected and extended from the round-2 disassembly (menu-close loads `$38:$95CC-$95F5`, the buster
    reset at `$38:$93FE`, the latch stores, the C.FLASH strobe `$3E:$DECD`, the frozen-tick patch point `$E443`).
55. §15.3 rewritten per owner, with the answers to venues_a's and venues_b's questions and fortress's and story's
    proposals. crossrefs, consistency decisions 17-20, 32-35.
56. Risks and open questions re-written for the round-2 design; round 1's 12 open questions resolved.
