# Round-3 reconciliation: cross-doc requests

The round-2 revisers returned 73 cross-doc requests and director questions. The director's answers are
[`RULINGS.md`](RULINGS.md) §8 (R8.1-R8.8). Every remaining request is routed below to the doc that must act on it.
Each doc's round-3 reviser marks each request **applied**, **already** (the doc already said it) or **declined**
(with the reason); the outcome column is filled in from their returns.

Items with no action (risks, user questions, measurements scheduled in a milestone) are not listed: the INPUT LAG range
and the hardware target (PLAN §9), the native-JP review date, the medium-confidence facts (story's M7 fact pass), the
vanilla projectile counts (tested at G7 and M5), and the set pieces at exactly the 9-slot cap (M3 re-measures).


## tech.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| TECH-01 | systems | Add the b5 FULL flag in LATCHSRC, a per-slot ENC_CLASS byte in WORK, and a REFLEX macro (TIERVAL + INPUT_LAG, reading RULESET's RS_LAG per meta §9.0). Adopt the hold-to-struggle figure of 6 f. |  | |
| TECH-02 | systems | Patch the pause-close clear at $38:$9624 so utilities (slots 4-7) survive when the weapon is unchanged; deaths still clear slots 1-7. | R8.7 | |
| TECH-03 | systems | Add to the M3 checks: every fortress and GP boss reaches its damage step by JSR, or is listed NOSTALL (the boss stall). |  | |
| TECH-04 | meta | Adopt: the H_REMATCH operand hook at $3F:$F952; a replay test in the $3F:$F9A0 hook (skip YOU GET on replays); the A/B SWAP edit at $3E:$C732 inside the joypad hook; return kind 6 for Time Attack (Should); RS_DIFF as the source of IFHARD/LAYOUT_TIER; save_commit refusing the scratch magic and NO_SAVE. |  | |
| TECH-05 | venues_a | Provide a per-screen pop-up position switch the screen script can set (Wind 01, Tomahawk 10-11), or extend EFFECTS b6 to a screen mask. Confirm the wave director and band control can live in the slot-22 screen script. |  | |
| TECH-06 | venues_b | R8.2: split v1.0 row 31 (the attach state): its core with the condor at M3 (about 1), vines/T5 and the balloon at M5 (about 1). Update §16 and the per-milestone totals. | R8.2 | |
| TECH-07 | venues_b | R8.2: no stage-$00 stop-gaps; state that the slice's GP code reads stage record v0 (M2.1) for SECRET_SCR, PAR and the GP_BOSSHIT row. | R8.2 | |
| TECH-08 | venues_b | Add an M5 check: the tide (chain $14) across vertical exits and a per-room tide base (screen script or EFX_PARAM: decide which); fallback door-joined rooms. |  | |
| TECH-09 | fortress | Add: a stage flag that suppresses bubbles; a credits room table and a CREDITS bit for the in-room boss credits mode (bosses run with no player); phase groups for alt_flip appearing blocks. |  | |
| TECH-10 | art_audio | Confirm the CHR row (v1.0 about 9 of 14 CHR banks; full design about 15.5 using the vanilla blank-gap reserve; 2 sprite pairs suffice) and that a 10th text bank comes from music's spare $79, not CHR. | R8.7 | |
| TECH-11 | art_audio | Specify G37's sync marker (the 04 flags command or a frame-count table); sprites.py overlay composites; artcheck checks 8-13; the art-gate gallery (a local HTML page, R8.8); confirm the 21 Must SFX fit the $36 tail (392 of 449 B). | R8.8 | |
| TECH-12 | story | Add one lowercase 'r' glyph for JP 'Mr.'/'Dr.'. Confirm the CAPCOM TIMES GP pages can be typed by the new text engine inside the vanilla driver's text rows (their JP needs katakana the main font lacks), or say what is needed. |  | |
| TECH-13 | story | The boss panel's re-type must support a third record (the WRONG NOTE exposure line, VENUE "EXPOSED BY A WHISTLE"). Register the new commentator hook ids WK-WM and WK-WC (W3 first-weakness lines); EV_PLATE stays separate from EV_SECRET. | R8.5 | |
| TECH-14 | director | Apply R8.3 (no MMC5 audio in v1.0's SUPER colour; the D9 drop is LIGHTS OUT's) wherever tech still reads R1.3 otherwise; mark the nightingale floor Should (R8.6); update tech's v1.0 scope numbers and §16 cumulative column to RULINGS §6 (R8.1). | R8.1, R8.3, R8.6 | |

## systems.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| SYSTEMS-01 | venues_a | Add Y.SPEAR to SC1's pass-through list (it pierces Knight's shield without breaking it). |  | |
| SYSTEMS-02 | venues_a | Add the clause that a stage-lent vehicle (SKY ACE's sortie, the Exhibitions' CANNON) is not a form: NO TAG, allowed under 1993, no form VARIETY. |  | |
| SYSTEMS-03 | venues_a | Add to the run's T: 7,200 f when SKY ACE's LAND skip is taken and 3,300 f for HIGH NOON's EXPRESS skip (or say how the par handles skips). |  | |
| SYSTEMS-04 | venues_a | Name the Metal Metslime's "every hit does 1" as a visible mid-boss special case; add the INPUT LAG setting (0-6 f) to VA-DRAW's window. | R8.7 | |
| SYSTEMS-05 | venues_b | Confirm: the bird-bot at 2 HP (so the Ice Block encases instead of killing); the ABSORB heal-1 SC4 exception; the four VENUE ACTs; the pars (Yamato is now 300 s); the boss-room lag rules (the WEAK! pop only takes a free slot; the CENTURION helper costs each boss one projectile per move). Fix the chip table's citations: venues_b §1.5.3 → §1.6.3, §3.6.3 → §3.7.3 (check the current section numbers). |  | |
| SYSTEMS-06 | meta | Keep the run block across fight-loader warps, so W2's pair bouts count in W2's scorecard; REFLEX reads INPUT LAG from RULESET's RS_LAG. |  | |
| SYSTEMS-07 | fortress | Add a +30 sponsor envelope for Opening-lite (if within the income model); list the Kamegoro turtle rule and WRONG NOTE as visible special cases; move the H2/H4 GP_BOSSHIT rows to Should (not Could); add an Air Man row for Doc Robot (Should). |  | |
| SYSTEMS-08 | director | R8.2: the quick form swap (SYS-CTL-4), the Power/Jet rows of the dispatch table (SYS-FRM-1) and adaptors by win count (SYS-FRM-2) move from the slice (M3, v0.1) to M5 (v0.5); the dispatch table with Normal form's taps and the Ice Block stays in M3. Update the v1.0 scope table's rungs, the "by rung" sentence and Risk 1. | R8.2 | |
| SYSTEMS-09 | director | R8.6: the CASUAL quick-draw is 40 f; R8.7: pause keeps utilities when the weapon is unchanged (already §1) — make sure the doc says tech owns the $38:$9624 patch. | R8.6, R8.7 | |

## meta.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| META-01 | venues_a | Place the PRIZES bits (Knight 1, Tomahawk 3, Plant 4); decide whether Knight gets a VENUE_REC (fastest Metal Metslime kill); PL0's tier A riddle must not name the jungle explorer (it is Should). |  | |
| META-02 | venues_b | Fix the on-screen name PRINCE OF PERSIA PALACE → PERSIAN PALACE everywhere; retire the stale sekisho riddle (YA0, tier A) for the draft riddle story wrote; use venues_b's new tier B drafts; PRIZES = 4 bits for Blizzard only; the mid-boss fight ids $0E Shadow Rock, $0F GAMARN & GAMADAYU, $10 Daruma. |  | |
| META-03 | fortress | Add a per-fight pinch byte field in the fight record (W2 reads it); confirm no PRIZES bits for fortress stages; fight ids $15 Kamegoro Maker and $29 Doc Robot (Should); the HALFTIME RIOT rename everywhere; H2/H4 map doors read CLOSED FOR RENOVATION while those stages are Should. |  | |
| META-04 | story | W3 has no judges' desk, so its three hints are Should; v1.0's predicate table uses only requirement hint R2: state which requirement hints (R1-R5) v1.0 uses, and mark the rest Should. |  | |
| META-05 | director | R8.5: fortress's NO-CAPSULE bit is meta's RATEFLAGS b4 SOLO RIOT (say so where useful). R8.8: EXTRA CONFIG and RECORDS keep meta's unlock points. | R8.5, R8.8 | |

## fortress.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| FORTRESS-01 | story | §0.5 and §2.6: Rock's first "Blues?" is at the Riot's 0E reveal (S20), the second at S40; S06 speaks no name (R8.5). | R8.5 | |
| FORTRESS-02 | story | Boss-panel strings use no space: BREAKMAN, DARKMAN (R8.5). | R8.5 | |
| FORTRESS-03 | story | Accept story's budget call: b0 secret lines and every tell are Must; b1/b2 lines are Should, with generic lines in v1.0 (R8.6). | R8.6 | |
| FORTRESS-04 | story | H5's letter plates spell ROCKMAN5 in both languages (R8.5). | R8.5 | |
| FORTRESS-05 | story | Register the hook ids WK-WM and WK-WC (W3 first-weakness lines) where fortress lists its hooks. |  | |
| FORTRESS-06 | meta | Keep Must: the HALFTIME RIOT's capsule beat (Bass β duel 1; RATEFLAGS b4 SOLO RIOT for rating T1; rename NO-CAPSULE → SOLO RIOT, R8.5) and Mr. X's card in H5's hidden room (T14). Use tech §4.2's stage ids and meta's fight ids throughout; the maps show H2, H4 and W1 as closed wings. | R8.5 | |
| FORTRESS-07 | systems | Name the 4 weapons pre-drawn in Bass β's set (R3.6); say which hit box Gamma phase 1's GP_BOSSHIT row uses (head and fists only); size H1's gap for at most two 64-px beams (check it is done). |  | |
| FORTRESS-08 | art_audio | R8.6: the podium shows the champions applauding in pairs (0 new tiles); the all-eight BG row is Should. | R8.6 | |
| FORTRESS-09 | art_audio | Eddie is new art (a composite), not vanilla; the rating screen draws over meta's judges' desk, not the stadium at dusk; the trophy theft's claw is Must art and H4's Catcher (Should) reuses it. | R8.6 | |
| FORTRESS-10 | tech | Re-cut set pieces still written for 10-13 slots to the 9-occupied-slot cap (e.g. Paddle Man, the Reaplet alarm, if they are in fortress); check every v1.0 screen's cap. |  | |
| FORTRESS-11 | director | R8.3: in v1.0, W2/W3/the escape keep all 2A03 channels; the channel drop is LIGHTS OUT's; R8.5: the alias gag only at the arrest (S41), the CAPCOM TIMES uses S44.4F; R8.4: cite story's string counts instead of fortress's own ~230 estimate. | R8.3, R8.4, R8.5 | |

## venues_a.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| VENUES_A-01 | systems | Check every venue chip's gate is a Must set piece (R0.4) and every venue fills in systems §13.4's CASUAL lever table (verify; fix any gap). |  | |
| VENUES_A-02 | tech | Check the set pieces are re-cut to the 9-occupied-slot cap: the sortie, AYACO, the train (verify; fix any gap). |  | |
| VENUES_A-03 | fortress | Add a short credits-mode note per boss: the v1.0 credits show each champion fighting in his own room with no Rockman, so each boss AI needs a no-player mode (or the credits use card strips only for that boss). |  | |
| VENUES_A-04 | director | R8.4: paraphrase the quoted 1986-RPG lines (no verbatim quotes); cite story's string counts instead of this doc's own. R8.6: the CASUAL quick-draw is 40 f. | R8.4, R8.6 | |

## venues_b.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| VENUES_B-01 | systems | Check every venue chip's gate is a Must set piece (R0.4) and every venue fills in systems §13.4's CASUAL lever table (verify; fix any gap). |  | |
| VENUES_B-02 | tech | Check Flame 0B and every other set piece is re-cut to the 9-occupied-slot cap (verify; fix any gap). |  | |
| VENUES_B-03 | art_audio | R8.6: Blizzard's FLAKES throws one flake fewer while an Ice Block is out if the flicker simulator fails it (apply at M4). | R8.6 | |
| VENUES_B-04 | fortress | Add a short credits-mode note per boss: the v1.0 credits show each champion fighting in his own room with no Rockman, so each boss AI needs a no-player mode (or the credits use card strips only for that boss). |  | |
| VENUES_B-05 | director | R8.2: the condor uses the attach state's core at M3; no stop-gaps for stage $00 (the slice reads stage record v0 from M2.1); the slice has no forms. R8.6: the nightingale floor is Should. Update §1.0/§5.3 accordingly. | R8.2, R8.6 | |

## story.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| STORY-01 | meta | Check: S47's T1 line refers to SOLO RIOT (the Riot won without the capsule), not to a call or SELECT; a T1 SOLO RIOT debrief entry exists; YA0's new tier A riddle (for the draft) exists; the HARD description matches v1.0's HARD (×1.5 damage, drops LESS, no refill); the health notice, INPUT LAG and CASUAL help lines exist; the sponsor-chair signs are Should (meta). |  | |
| STORY-02 | venues_a | Check (story ran after venues_a): a new sixth Tomahawk death line replaces Boot Hill; PLT-06/PLT-08 have no Harry or Game Boy; Tomahawk Man has the rodeo-showman voice; lines exist for LAND/LANDED, the conductor's count and EXPRESS, the stairs check, the Sage's after-death tell, the RODEO RING. |  | |
| STORY-03 | venues_b | Check: BLZ death 6 (the climbers' names) and CEN death 6 (the Underworld hero) are gone; BLZ-04 has a varied Wily line; FLM-06 fits the spacing rule; CEN-21, CEN-22, YAM-21 exist; the sekisho and hanabi lines are retired. |  | |
| STORY-04 | art_audio | S42's cue table follows art_audio §12.9's order with no DPCM; "already silenced" applies only to the MMC5 voices; v1.0 ships one CAPCOM TIMES headline (the doped one is Could) and 4 speaker blips; the S40 carry art is Should; the attract crawl's pictures are Could. | R8.3 | |
| STORY-05 | fortress | Check fortress's asks are answered: the new lines its hooks need; the orange-scarf tell; panel strings; the fact checks (Kamegoro, Doc Robot, the coin shortage, the Rockman 8 reference). |  | |
| STORY-06 | meta | Align the requirement hints with meta's v1.0 predicate table: hints v1.0 does not use are Should (read meta's current §4 to see which). |  | |
| STORY-07 | director | R8.4: 400 Must strings accepted; paraphrase quoted lines from other games (the 1986-RPG lines included); in JP Light says アルバート if S42 uses Wily's first name. R8.5: the alias gag only at the arrest (S41) and S44.4F for the CAPCOM TIMES; ROCKMAN5 for H5's letters. | R8.4, R8.5 | |

## art_audio.md

| Id | From | Request | Ruling | Outcome |
|---|---|---|---|---|
| ART_AUDIO-01 | story | Confirm the 4-blip mapping, the face-icon list (the King, PA and battle-log pop-ups are icon-less), and the order in which G37's stems drop. | R8.3 | |
| ART_AUDIO-02 | venues_b | The mouse squeak is a Must SFX (the tell of a Must secret) with a vanilla fallback: check it is among the 21. |  | |
| ART_AUDIO-03 | venues_a | Check the budgets carry venues_a's v1.0 changes (Wind seagull Must; windsock and flag-judge stand BG; loop poses on a set-piece player sheet; Wind's pinch set 24 tiles; T-MESA Must; T-RODEO Should; the cactus walker Must; the vine weapon-slot set dropped; the sconce flame Won't). |  | |
| ART_AUDIO-04 | director | R8.3: v1.0's W2/W3/escape keep all 2A03 channels; LIGHTS OUT's drop is Must; G14 POCKET is Could. R8.6: the podium pairs; Eddie is new art. R8.8: the gallery is a local HTML page plus PNGs. Update the doc where it still asks. | R8.3, R8.6, R8.8 | |
