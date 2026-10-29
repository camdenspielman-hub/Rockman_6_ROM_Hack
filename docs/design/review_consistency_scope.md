
# critic-scope

## Verdict

This is an inventive design, specified in enough detail to implement. Nearly every item has a tier, a size, a fallback and vanilla evidence behind it.

As written, though, it is about 830 focused sessions (Must about 550), roughly 8 times what PLAN §8 budgets, with about 95 % of the new art assigned to a pixel artist the project does not have.

The Must tier is a complete, fun game in content (about 15 stages), but it is not self-contained. It relies on Should or Could items:
- the Break Man sheet;
- the GP Rush fight loader;
- F-ERA and ExGrafix;
- the D9 mute mask;
- venues_b's Should chips and Flame's Should room.

The rating cannot reach 100 without Should content.

Recommendations:
1. Re-baseline on a session ledger.
2. Adopt a tight Must of about 440 sessions:
   - weapon taps only (alts and synergies become Should);
   - venues kept to their core;
   - single-size BG bosses; no portraits;
   - an NPC-only Break Man;
   - no Exhibitions, HARD content, 1993 or post-game beyond EXTRA CONFIG and RECORDS.
3. Run an MMC5 go/no-go spike on Mesen before M1.
4. Schedule the missing prerequisites: CHR set table v2, the art tools and the fight loader.
5. Build Blizzard as the vertical slice at about 115 sessions instead of Opening + Wind + Knight at about 180.
6. Merge the duplicated runtime-BG-edit, HUD, attach-state, tileset-slot and poke-list systems.

The scratch ledger is at /home/user/Rockman_6_ROM_Hack/build/review/critic-scope/tally.py, and the tight-Must estimate at /home/user/Rockman_6_ROM_Hack/build/review/critic-scope/tight.py.

## Strengths

- Every item has a tag, a size and a tier, and most docs already give fallbacks and cut orders (meta Risk 7, art_audio Risk 10, venues_a §6, venues_b §5.2, fortress Risk 1). Re-tiering is therefore mechanical.
- The normal-route rule (systems §2.4, fortress §0.2: no form, alt, synergy or Break Man on a main path) makes most expensive features cleanly deferrable without redesigning any level.
- Assets are decoupled from code: the placeholder-first art rule (art_audio §11.1) and a vanilla fallback id for every new track (art_audio §12.1) mean code and levels never wait for art or music.
- tech §16 turns M0-M3 into concrete task lists, and records which PLAN M0 items the research already finished (§16.1). The foundations are well specified.
- Strong reuse of vanilla engine set pieces with one twist each (fortress §0.6). The H/W wings start from vanilla layouts; BG bosses ride on vanilla split techniques.
- Testability is built in: the test mailbox, golden movies with scripted pokes, deterministic wave directors and fixed encounter triggers. QA cost per content item stays low.
- Content is data-driven (bracket events, debrief predicates, rating tests, the fight table, poke lists), so new content after v1.0 costs data rather than code.
- The vanilla-fact measurements (free tiles per screen, enemy-area budgets, form-sheet differences, VBlank costs) make the art and CHR budgets enforceable by artcheck.py, not guesses.

## Findings (26: blocker 0, major 15, minor 11)

### scope-1. [MAJOR] all (BRIEF.md §9, PLAN.md §8, art_audio.md §13, story.md §10.4, tech.md §16) · Production inventory and estimate

**Issue.** As written, the design is about 830 focused AI-assisted sessions, and the Must tier alone is about 550. That is roughly 8x what PLAN §8 budgets, and no doc ties the tiers to a budget.

INVENTORY (from the docs):
- Stages: 22, plus the victory lap and Mr. X Returns; tech §4.2 uses all 32 stage ids.
- Screens: about 467 against vanilla's 361.
  - Venues: 237 (Wind 29, Knight 28, Tomahawk 32, Plant 32, Blizzard 28, Flame 28, Centaur 30, Yamato 30).
  - Non-venue: about 230 (Opening 14, Semifinal 16, E1-E4 28, H1-H5 110, W1-W3 54, victory lap 8).
- Boss-scale encounters: 45 distinct, about 34 of them Must, plus 8 SUPER copies and the 1993 ??? fight. 9 are BG bosses.
  - 8 reworked champions;
  - 8 secret-arena variants;
  - 8 venue mid-bosses or set-piece fights (AYACO, the ceiling with HP, Metal Metslime, Six-Shot Sam, Sidewinder, CONGA, Shadow Rock, Daruma);
  - 21 non-venue bosses and mid-bosses.
- New object and enemy kinds: about 155 (venues_a ~45, venues_b ~46, fortress ~40, systems ~25), against 30 free type ids.
- Code: about 60 shared engine and system modules, plus about 85 venue- or stage-specific mechanics.
- Art: 6,793 new tiles (4,508 BG + 2,285 sprite) and 573 frames. Must is 4,851 tiles and 421 frames. That fills 14-16 CHR banks, 10 tileset banks and 3 sprite bank pairs.
- Music: 37 compositions plus 2 MMC5 layers (51 ids, 27.5 KB; 5 Must), plus at least 4 more that fortress.md and story.md ask for. About 70 SFX, about 20 Must.
- Text: about 1,100 strings in both EN and JP (about 600 Must), 70-90 KB, plus about 25 ENGRISH overrides. Every JP line needs a native-speaker review.

ESTIMATE (1 session = 1 well-scoped task; itemised in build/review/critic-scope/tally.py):
- Code, data and tests: 650 sessions. Must is 456: tech 100, systems 78, meta 33, venues 133, fortress 94, overhead 19.
- Art: about 100 (Must about 73), at Claude-only draft speed of about 80 BG tiles or 12 animated frames per session.
- Music: about 54 (Must about 9).
- Text: about 24 (Must about 13).
- Total: about 830; Must about 550.
- One venue costs about 26 sessions: 17 code, 7 art, 1.5 text, 1 music.

The docs size much of this far lower:
- PLAN M5 gives each venue 'One L task' (L = 3+).
- tech §16's own S/M/L for M0-M3 adds up to about 30-50 sessions; my itemised count for that scope, including the unscheduled items, is about 100.
- tech M3.2 gives the whole systems.md hook set one M. systems.md itself sizes that work at about 25-35 sessions.

**Evidence.** art_audio §17 risk 10: "Scale creep: 6,793 tiles is more than 4MI's 5,266."
story Risks 1: "About 1,100 strings in two languages is a lot of text for a fan project."
PLAN §8 M5: "One L task per venue".
PLAN §8.4: "Session/credit budget | H".
tech §16.5: "M3.2 (M) systems.md's hook set (its §15.1): SELECT quick swap with the form CHR stream, weapon alt/synergy dispatch, damage and i-frame tables, adaptor by win count..., WEAK! pop, commentator events."
systems Risk 2: "Forms × weapons × alts × synergies is about 24 new behaviours... It is the largest systems item."
venues_b §5.1: "New object kinds... ~46".
fortress Risks 1: "14 stages, 22 bosses and mid-bosses and about 40 new objects."

**Recommendation.** 1. Make a session ledger the scope authority. Seed it from tally.py and re-estimate it from actual session counts after the vertical slice.
2. Re-baseline PLAN §8, and tech §16 M3 in particular, with a session count per item instead of a single S/M/L per milestone.
3. Adopt the tight Must proposed in the next finding (about 440 sessions).
4. Treat the 'Round One' build (Opening, 8 venues and the Semifinal, about 290 sessions) as a scope checkpoint.

### scope-2. [MAJOR] BRIEF.md §9; systems.md; meta.md §13; fortress.md; venues_a/b.md · MoSCoW: is Must alone a shippable game?

**Issue.** In content, Must is a complete and fun game: Opening, 8 venues, Semifinal, H1/H3/H5, W2/W3 and the ending make about 15 stages, against vanilla's 16.

The problem is size. At about 550 sessions, Must is most of the project, because:
- each venue doc puts its full feature set in Must;
- BRIEF §5.1 makes all 24 weapon behaviours Must;
- the scaffolding layers (HARD content, two-tier hints, about 300 commentary lines, 12 portraits) are all Must.

Most of these can be deferred cleanly, because systems §2.4 and fortress §0.2 guarantee that no normal route needs an alt, a synergy, a form or Break Man.

Proposed TIGHT MUST (v1.0, about 440 sessions: code 367, art about 50, music about 10, text about 12; computed in build/review/critic-scope/tight.py):
- All tech foundations.
- Systems:
  - SELECT swap, the quick form swap, and forms firing every weapon's TAP;
  - adaptors by win count; the Super fist; M.BEAM;
  - GP_BOSSHIT, the frozen tick, WEAK!, and the special cases SC1/5/6/8/9;
  - attribution, the scorecard and bolts;
  - the shop with about 6 chips plus the Balancer, and the 8 venue chips;
  - plates and Beat; pickups; presets; the HARD framework.
- Meta: saves, title, file select, bracket, results, debrief (tier B only), pit stop, game over and RETIRE, medals, a rating with no TURBO trap, fortress maps, the fight loader, RECORDS 1-3, EXTRA CONFIG and the mailbox, CONFIG.
- 8 venues, each kept to its core: homage mechanic, secret exit, hidden room, behaviour chip, boss rework. Secret arenas reuse the boss room with a new palette.
- Opening-lite, the Semifinal, H1/H3/H5, W2, W3, and the ending with a vanilla-style staff roll.

CUT LINE, in priority order (everything below moves to v1.1 or later):
1. Weapon alts and form synergies (about 19 sessions).
2. The Break Man tag partner (5 code + L art; his NPC role stays Must).
3. HARD poke lists and AI branches (about 8).
4. Each venue's second set piece and secret-arena twist (about 29).
5. H2, H4, W1 (about 39).
6. Exhibitions (about 34; E4 Won't).
7. Time Attack.
8. The victory lap (8).
9. PARTs, the garage, the Mr. Y booth and TURBO.
10. The 1993 preset.
11. GP Rush runner, courses and MY GP.
12. Achievements, ENGRISH, the attract crawl.
13. Won't (v1): KNOCKOUT, Exhibition Rules, Museum and VAULT, Bass Mode, Mr. X Returns.

If the budget is below 440, cut next (in this order):
- merge H5's unmasking into H3 (minus about 9);
- make W2 a single-arena Bass final (minus about 5);
- turn the Opening into 3 tutorial screens (minus about 4).

**Evidence.** BRIEF §9 Must: "Systems §5.1-5.3; 8 venues with secret exits; Opening; Semifinal; H1, H3, H5; W2 + W3; ending; saves and config; JP + EN; dev tooling".
systems §0.1: "SYS-WPN-1..8 | Eight boss weapons: tap, alt, synergy | ... | L total | Must (tap, alt, synergy)".
systems §2.4: "A normal exit never needs a form, an alt fire, a synergy or Break Man."
fortress §0.2: "Every punch, form, alt, synergy, weapon and Break Man gate is on optional content."
meta Risk 7 already gives a cut order: "KNOCKOUT → Museum → Exhibition Rules → MY GP → GP Rush courses beyond OPEN."

**Recommendation.** 1. Rule the tight Must above as the v1.0 definition, and amend BRIEF §9 and §5.1.
2. Have each venue and fortress doc re-tag its items against it.
3. Publish the cut line as an ordered list in PLAN, so later cuts are mechanical.

### scope-3. [MAJOR] fortress.md, meta.md, art_audio.md, venues_b.md, story.md · Must depends on Should/Could content

**Issue.** Several Must items need Should or Could items to work, so a Must-only build is broken or inconsistent.

- **Break Man.** The Semifinal (Must) lists 'Break Man (the tag partner's set)' as Must art, but art_audio §7.1 rates the sheet Should and systems rates SYS-TAG-1 Should. Dark Man MK-VI (H5, Must) wears the same sprite set.
- **W2.** W2 (Must) runs its pair bouts through the GP Rush fight loader, which meta §13 rates Should.
- **ExGrafix.** W2's moat (a scrolling stage) and W3 use SUPER colour through ExGrafix. art_audio §2.7 rates that Could, and tech D6 rules out ExGrafix in scrolling stages entirely.
- **The escape.** The W3 escape (Must) 'runs F-ERA in reverse', but F-ERA is Should (fortress §5.0).
- **The ending.** Its lights-out scene (Must) needs the channel mute mask D9 (Should). Its new arrangement is not among art_audio's 5 Must tracks.
- **The rating** (Must) can reach only about 81/100 with Must content:
  - T1 (Break Man) fails: minus 5;
  - T3 (Exhibitions) fails: minus 4;
  - T4 needs all 8 hidden rooms, but Flame's mouse room is Should: minus 2;
  - T5 needs all 8 venue chips, but venues_b's four are Should: minus 2;
  - T6 counts Eddie's chips, and Must has only 4 shop chips: 4 of 10;
  - T7 needs TURBO (Should).

  The 'exactly 100' arithmetic exists only with Should content.
- **Venue tiers disagree.** venues_a makes its 4 behaviour chips Must; venues_b makes its 4 Should. BRIEF §5.4 requires one hidden room and one behaviour item in every venue.

**Evidence.** fortress §2.1: "Break Man (the tag partner's set, `systems.md` §11)... | [new-art] L, Must".
fortress §4.5.2: "Phase 1 uses the tag partner's own Break Man sprite set".
fortress §5.2.1: "an alcove calls the GP Rush fight loader (`meta.md` §9.2.1...)"
meta §13: "GP Rush engine: fight table, runner, lobby, courses | ... | M | Should".
tech D6: "no ExGrafix in scrolling stages".
fortress §5.2: "ExGrafix data for the moat... Must".
fortress §5.4: "the escape runs F-ERA in reverse"; §5.0 "F-ERA [new-code] M, Should".
art_audio D9: "Channel mute mask... | S | Should".
venues_b §5.2 Should row: "SNOW CHAINS... mouse room; FIREPROOF... CENTURION... DARUMA chip".
meta §6.1 T4/T5/T6 rows.

**Recommendation.** 1. Rule that a Must item may depend only on Must items.
2. Then make these fixes:
   - Break Man as an NPC (a composite of about 10 frames) becomes Must; the playable partner stays Should.
   - The fight loader becomes Must.
   - D9 becomes Must.
   - W2/W3/escape 'SUPER' becomes palette plus music only in v1.0; ExGrafix and F-ERA flip-screens go with W1 (Could).
   - All 8 venue chips and hidden rooms become Must.
3. Recompute the rating rows so that 100 is reachable with v1.0 content. Make the TURBO trap conditional on the booth shipping.

### scope-4. [MAJOR] PLAN.md §8 M4; tech.md §16 · Vertical slice and milestone order

**Issue.** The vertical slice arrives late, and it is the heaviest possible choice.

It comes only after M0-M3 are complete: by my count about 130 sessions, once the systems work under-budgeted in M3.2 is included. PLAN M4 then builds three slices at once, each using the riskiest technology:
- Opening: TS_STADIUM (L art) and F-SIZES for Pi-kun's 3 sizes;
- Wind: the T1-lite shmup engine, AYACO (T8), the POW/LOOP rules;
- Knight: the full T2 text engine with menus, NPCs and a battle log.

The first playable judgement on scope and fun would come at about 180 sessions.

BLIZZARD (SUMMIT CLIMBER) is the cheapest complete venue that still tests the whole loop:
- It keeps stage id 0, so the vanilla ship and slippery ice work before the stage-attribute table exists.
- It has the smallest new BG art (art_audio §4.9: 70 BG tiles).
- It needs no T1 and no T2 dialogue menus; only pop-ups and the debrief.
- It uses T6 and X-BONK, which Flame, Yamato and E2 reuse.
- It awards B.ATTACK, whose Ice Block alt (with the frozen tick) can serve as the alt-dispatch prototype.

**Evidence.** PLAN §8 M4: "M4.1 (L) Opening Ceremony stage + Grand Pi-kun. M4.2 (L) Wind Man venue (T1, the shmup segment, the AYACO bomber...) M4.3 (L) Knight Man venue (T2 full, T3, the ENCOUNTER gag...)".
tech §16.5: "Then M4 (vertical slice) can start on real venue data."
venues_a Risk 5: "Knight depends on T2."
venues_b §0.2: "keeping the ids keeps both set pieces working before the stage-attribute table... lands."
art_audio §4.9: "Blizzard | 70 | 126 (+12 Could) | 41".

**Recommendation.** Use this milestone order. Cumulative session counts are in brackets.

- **M0'** Workbench, plus a Mesen MMC5 go/no-go spike (about 12) [12].
- **M1** Literal MMC5 port with golden equivalence (about 13) [25].
- **M2'** Slice engine (about 45) [70]:
  - families and sub-ids; WRAM layouts and map_set;
  - CHR set table v2 and minimal chr/sprites/artcheck tools;
  - level pipeline with the canvas table; raster list;
  - text engine v1a (pop-up and debrief window, EN and JP kana);
  - track table and MML;
  - save module and file-select-lite; bracket-lite; results and debrief; EXTRA CONFIG and the mailbox.
- **M3'** Slice systems (about 25) [95]:
  - SELECT and the form swap; taps in all forms; adaptors;
  - GP_BOSSHIT, WEAK!, the frozen tick;
  - scorecard and bolts; shop and chips (3);
  - T6, X-BONK, X-WRAP; HUD widgets; commentator bus (deaths and weakness lines).
- **M4** BLIZZARD end to end (about 20 including art) [about 115] ⛳⛳. The path: new game, bracket, venue (exit, room, chip, boss), judges, save, reload, replay. Re-estimate the ledger here from actual counts.
- **M5** Stage-attribute table, Opening-lite, Flame, Plant, Centaur, Yamato (about 90) [about 205].
- **M6** Text v1b (dialogue and choices), T1-lite, Knight, Tomahawk, Wind, Semifinal (about 80) [about 285]. 'Round One' checkpoint ⛳.
- **M7** BG-boss tooling and the fight loader; H1, H3, H5 (about 55) [about 340].
- **M8** W2, W3, ending (about 40) [about 380].
- **M9** JP native review, balance, emulator matrix, release (about 20).

### scope-5. [MAJOR] tech.md §1, §2, §4, §7.2, §8, §9, §11, §16 · Critical path and riskiest prerequisites

**Issue.** Critical path:
1. MMC5 port.
2. Families, WRAM layouts, CHR set table v2, art and level pipelines.
3. Raster list.
4. Text engine.
5. Per-venue tech: T6, then T3/T7/T5, then T1-lite.
6. Venues.
7. Fight loader and BG-boss tooling.
8. H1/H3/H5.
9. W2.
10. W3, then the ending.

Risk ranking:
1. **MMC5 on anything except FCEUmm.** Every probe ran on the bundled FCEUmm, which forgives header, PRG-RAM and CHR mistakes. The Mesen check is M1.6, scheduled AFTER the port (M1.1-1.5). Headless Mesen and the hardware target are both open questions.
2. **Text engine** (L, Must). It rests on ExRAM as a nametable, probed on FCEUmm only, and on borrowing and restoring BG tiles. Knight, all commentary, the debrief, NPCs, scenes, plaques and help pages depend on it.
3. **Raster list.** It needs calibration on two emulators, and 16 bands per buffer are shared by:
   - the text window band;
   - venue bands (3-4 plus the window);
   - W3's 16-band floor.
4. **Stage-id table.** 45 + 11 readers, plus readers the tour never executed. The id map itself is disputed (see the separate finding). It is not needed for a venue slice, only before ids 16 and up (Opening, Semifinal) and before the ceiling and tide are re-homed.
5. **Sub-id dispatcher.** Low technical risk (4MI precedent), but about 155 object kinds depend on it, so build it first.
6. **T1-lite.** Low risk (nothing solid moves); it is needed only before Wind, Tomahawk and the W3 escape ride.

**Evidence.** tech §1.1: "The test emulator cannot catch a header mistake: the bundled FCEUmm gave 8 distinct PRG-RAM pages (64 KB) for every byte-10 value tried."
tech D6: "the bundled FCEUmm wraps MMC5 CHR-RAM at 8 KB whatever the header says".
tech §16.3: M1.6 "Spike ROMs... all on Mesen" comes after M1.1-M1.5.
tech Open questions 4-5: "Can a headless Mesen run in this environment...?" / "Which hardware target matters...?"
tech Risk 11: "Text engine size (L): Knight's venue depends on it."
venues_a Risk 3: "The sortie and the train need 3-4 raster bands plus the commentator window band in the same frame."

**Recommendation.** 1. Move a 1-2 session MMC5 spike before M1.1, as a formal go/no-go gate. Run it on Mesen, plus the user's cart if one exists: the header, 32 KB PRG-RAM pages, ExRAM-as-nametable through a mid-frame $5105, and IRQ line timing.
2. Get the user's answer on the hardware target now.
3. Split the text engine into v1a (pop-up and debrief) before the slice and v1b (dialogue, choices, NPC menus) before Knight.
4. Before writing venue band layouts, fix a band budget per stage: window band plus N stage bands, at most 16.

### scope-6. [MAJOR] tech.md §16; art_audio.md §2.1, §10, §14; meta.md §9.2.1 · Hidden critical-path items not in any milestone

**Issue.** Several Must prerequisites appear in no milestone list.

1. **The CHR set table v2** (5-byte entries with an 8-bit source bank, plus stage-local ids $E0-$FB). art_audio says tech builds it; tech §16 never schedules it. tech §1.2 puts all new CHR in banks $5A-$63 and $78-$7B, which vanilla's 6-bit source-bank field cannot address. So no new art can reach the screen until v2 exists.
2. **The art pipeline:** chr.py, sprslice.py, palettes.py, bgboss.py and artcheck.py, all tagged M Must in art_audio §14. tech schedules only the metasprite compiler (§7.5), and only implicitly.
3. **The GP Rush fight loader.** It is Should in meta, yet W2 (Must), Doc Robot (H3, Must), Time Attack, EXTRA CONFIG 'FIGHT n' and the mailbox all rely on it.
4. **T5, T7, T8, X-EXWP, the F-* engines and the commentator event bus** are not in tech's M0-M3.

Together these add about 25 sessions that no milestone budgets.

**Evidence.** art_audio §2.1: "CHR set table v2 [new-code] S · Must (built by tech.md)".
art_audio §1.2: "bits 1-6 = 8 KB source bank, so only banks $00-$3F are addressable".
tech §1.2: "$5A-$63 | new CHR source data (80 KB = 5,120 tiles)".
art_audio §14: "Pipeline: chr.py, sprites.py, sprslice.py, bgboss.py, palettes.py | ... | M | Must"; "artcheck.py ... | M | Must".
fortress §5.2.1: "an alcove calls the GP Rush fight loader".

**Recommendation.** 1. Add to tech §16:
   - M2.x 'CHR set table v2 and stage-local ids' (S-M), before any new art;
   - M2.x 'art pipeline (chr, sprites, palettes, artcheck minimum)' (M);
   - M7 'bgboss.py' (M).
2. Promote the fight loader to Must and give it to tech or meta as a single owner.
3. Schedule T5/T7/T8/X-*/F-* in the venue tranches that first need them.

### scope-7. [MAJOR] art_audio.md §11, §17, §18 · Art: programmatic vs human split

**Issue.** The art plan is not credible without a pixel artist, and the BRIEF confirms there is none.

art_audio's own ledger assigns:
- 1,368 BG tiles, 1,594 sprite tiles and 419 frames to a human (H);
- 2,630 BG tiles, 649 sprite tiles and 147 frames to 'Claude drafts, a human cleans' (D).

Only 510 BG tiles (11 %) are programmatic, and only 6 sprite tiles are counted as mechanical reuse. So about 95 % of the new art depends on human skill, and Must alone is about 660 human-hours.

The heaviest human items are all Must:
- the MODE-7 Machine's 3 sizes (340 BG tiles);
- Gamma (200);
- Grand Pi-kun's 3 sizes (about 150);
- Bass β (90 tiles, 22 frames);
- 12 portraits plus mouth frames (216 tiles);
- 10 match-card portraits (160);
- the venue enemy casts (about 300 frames).

The stated fallback ('D items become final, H characters drafted by composing vanilla parts') is the actual plan, but the budget and tiers are written for the other plan.

**Evidence.** art_audio §11.2 table: "Human (H) | 1,368 | 1,594 | 419"; "Claude programmatic (C) | 510 | 36 | 4"; "Reuse (R) | 0 | 6 | 3".
art_audio §11.2: "Must | ≈ 660 | about 16 weeks at 40 h".
art_audio §17 risk 1: "No pixel artist... Bass β, the BG bosses and the portraits would look amateur."
art_audio §18 q3: "Will the project recruit a pixel artist...?"

**Recommendation.** Rewrite §11 for the no-artist case as the baseline, with a human pass as optional polish.

1. Make reuse the default. Every new enemy starts as a recolour or composite of vanilla RM6 sprites (CX recoloured 71 % of its reused sprites). Count R honestly in the ledger.
2. Draw BG bosses at one size each:
   - the W3 machine reuses vanilla Wily Machine 6 art ($BE, 202 tiles) retinted, and the floor bands (programmatic) carry the 'Mode 7' joke;
   - Pi-kun gets one size;
   - Gamma shrinks to head and fists (about 100 tiles).
3. Replace portraits and match-card portraits with the 16x16 face icons and name labels in v1.0; portraits become Should.
4. Build Break Man and Bass β from Rock's sheet (visor/scarf, palette, helmet fins).
5. Cap new frames per character, for example 8 for enemies and 16 for bosses.
6. Keep the placeholder-first rule, and add one 'art acceptance' review gate per milestone with screenshots for the user.

This brings Must art to about 3,900 tiles and 350 frames, about 50 Claude sessions.

### scope-8. [MAJOR] BRIEF.md §5.1; systems.md §3 · Weapon alts and form synergies are Must but optional

**Issue.** The 8 alts and 8 synergies are 16 new player behaviours. Each needs:
- its own object;
- tiles in the 15-tile weapon slot;
- a damage cell and balance tuning;
- tests in every form.

They cost about 19 sessions of code plus art and balance, and they multiply the test matrix (forms × weapons × presets). Yet by systems' own rule, no normal route needs them, and no Must secret needs them either. Every venue and fortress use of an alt (Updraft to a ladder, Wall Spear perches, Time Stop on force beams, Ice Block on oil) is optional or a revisit pocket.

**Evidence.** BRIEF §5.1: "Each of the 8 weapons gets: a tap behaviour; one alternate (UP+B or hold); one form synergy."
systems §0.1: "Must (tap, alt, synergy)".
systems Risk 2: "about 24 new behaviours... It is the largest systems item."
systems §2.4: "A normal exit never needs a form, an alt fire, a synergy or Break Man."

**Recommendation.** 1. Amend BRIEF §5.1 as follows.
   - Must: forms fire every weapon's tap, and the dispatch table carries columns for alt and synergy.
   - Should (v1.1): the alts and synergies themselves, added one weapon at a time.
2. Ship one alt, B.ATTACK's Ice Block, in the Blizzard slice to prove the dispatch and the frozen tick.
3. Bosses can still preview their weapon's alt as a boss move: that is AI, not player code.

### scope-9. [MAJOR] fortress.md §3; meta.md §6.1 T3 · Exhibitions: four bespoke mini-game engines

**Issue.** Each exhibition is a new game engine rather than a Rockman stage with a twist:
- E1: falling blocks with push, rotate and bonk, a ghost piece, a 7-bag, line clears and garbage;
- E2: brick-breaker ball physics with 5 deflection zones, capsules, floor erosion and multiball;
- E3: an invader formation drawn as BG under the chain $16 split, with a step rule, bunker erosion and a UFO shot count;
- E4: a top-down MAZE mode, which is a new player-control model, with 4 ghost AIs, scatter/chase and pellets.

They also need F-GRID, TS_ARCADE plus 4 thirds, 4 guest bosses, 4 songs and their own text. About 34 sessions of code plus art, for optional bonus stages. They are also the least 'Rockman' content, and the most trademark-exposed (fortress Risk 10).

**Evidence.** fortress §3.4: "MAZE mode | Rock on the Jet, top-down sprite... moves on an 8-px lattice... pre-turn buffering".
fortress §0.7: "F-GRID | A WRAM cell grid (up to 16×14) mapped to BG tiles and collision, with a paint queue".
fortress Risk 10: "the exhibitions imitate famous games."

**Recommendation.** 1. Demote E1-E3 to Could (v1.1). E4 Maze is Won't for v1.
2. If any ship, redesign each as one arena: a lobby plus a 'rule boss' room, with no 3-screen lesson ladder. That is about 3-4 sessions each.
3. Build them on map_set and T6, not a separate F-GRID.
4. Remove T3 from the v1.0 rating.

### scope-10. [MAJOR] tech.md §5.6, §10; venues_a.md §0.4 VA-TIMED; venues_b.md §0.4 T6; fortress.md §0.7 F-GRID, F-PIECES · Duplicated systems: runtime BG modification

**Issue.** Five or six separately specified mechanisms all write the BG or collision at run time:
1. tech's map_set and repaint queue;
2. T6 variant blocks with a transition table;
3. venues_b's T6 bitmap, kept as tech's fallback;
4. VA-TIMED alternate-metatile toggles through $0340;
5. F-GRID, a WRAM cell grid with its own paint queue;
6. F-PIECES, which erases and paints 16x16 BG pieces in NT0/NT1.

Vanilla oil ignition by metatile id is a seventh. Each would get its own repaint scheduling and VBlank contention, and its own bugs. F-GRID in particular duplicates the RAM-resident layout that tech already provides.

**Evidence.** tech §5.6: "map_set(section, screen, row, col, block) writes a layout byte and queues a repaint".
tech §10: "Design: rewrite the RAM layout with authored variant blocks... Alternative kept as fallback: a 1-bit-per-16×16-cell bitmap".
venues_a §0.4: "toggling floor: flip the alternate-metatile bits in $0340 on a timer and repaint".
fortress §0.7: "F-GRID | A WRAM cell grid... with a paint queue (≤ 8 cells per frame)"; "F-PIECES | ... erase a piece (4 tiles through the VRAM buffer)... paint it back elsewhere".

**Recommendation.** Rule a single 'map edit' service owned by tech, with two primitives:
- a per-cell write (map_set);
- a per-id alternate flip, as vanilla does.

Both go through one repaint queue with a per-frame budget. Build T6 (pick ONE: variant blocks, or the bitmap), VA-TIMED, F-PIECES and any exhibition grid on top of it. Delete F-GRID as a separate engine.

### scope-11. [MAJOR] tech.md §1.2, §5.2; art_audio.md §2.2; venues_b.md §0.2; fortress.md §0.1 · Tileset-slot plans conflict (a prerequisite of every stage)

**Issue.** Four incompatible slot plans exist, and every venue and fortress stage needs one before any layout is authored:
- tech: banks $64-$6B with 2 slots per bank, each slot with its own alternate set;
- art_audio: 10 banks with 3 slots each, the slots sharing one alternate set. It puts the Opening in TS-TMH $92, the Semifinal in TS-FLM $92, H5 in TS-KNT, W2 in TS-CTR and E1-E4 in the venue banks;
- venues_b: a whole 8 KB bank per venue;
- fortress: separate TS_STADIUM (Opening, Semifinal, lobby, lap), TS_ARCADE (E1-E4) and TS_LAB, plus copies for TS_H1-H5, W2 and W3.

The same art (the stadium, the arcade) is planned twice in different places.

**Evidence.** tech §1.2: "$64-$6B | tileset slots (2 per bank, each with its own alternate set, §5.2)".
art_audio §2.2: "10 new 8 KB banks (80 KB) for 30 slots"; "TS-FLM | ... | Semifinal Riot"; "TS-TMH | ... | Opening Ceremony".
venues_b §0.2: "I ask for a whole 8 KB tileset bank per venue".
fortress §0.1: "TS_STADIUM (Opening, Semifinal, GP Rush lobby, lap), TS_ARCADE (the four exhibitions), TS_LAB".

**Recommendation.** Rule tech as the single owner of one slot-allocation table. Recommendation: tech's 'RAM image' model, with 2 slots per bank and an independent alternate set per slot, which satisfies venues_b's need. Then:
- fortress's TS_STADIUM serves the Opening, the Semifinal and the lap;
- TS_ARCADE exists only if the Exhibitions ship;
- art_audio's table is regenerated from tech's.

### scope-12. [MAJOR] tech.md §4.2; fortress.md §0.1, §8 · Stage-id map conflict (critical-path prerequisite)

**Issue.** tech and fortress assign ids differently.
- **tech:** keeps vanilla's 8-15 as LEGACY, for regression movies, legacy fights and Mr. X Returns. It puts the Opening at $10, the Semifinal at $11, E1-E4 at $12-$15, H1-H5 at $16-$1A, W1-W3 at $1B-$1D, the lap at $1E and Mr. X Returns at $1F.
- **fortress:** puts H1-H5 and W1-W3 at 8-15 'so every vanilla AND #$08 test still works'. Opening 16, Semifinal 17, E 18-21, Mr. X 22, lap 23.

fortress's plan removes vanilla fortress stages from the id space. That breaks:
- the vanilla golden-movie regression of stages 8-15 (tech §14.4);
- fortress's own '???' fight ($27 = vanilla Wily 4 untouched);
- loading vanilla Mr. X 1 for Mr. X Returns.

Its 'cheaper' argument also fails, because tech M2.1 rewrites all 45 readers anyway.

**Evidence.** fortress §0.1: "H1-H5 and W1-W3 therefore keep the fortress ids 8-15."
tech §4.2: "$08-$0F | legacy Mr. X 1-4, Wily 1-4, unchanged | LEGACY".
fortress §8: "$27... it is vanilla Wily 4's whole final fight, untouched... in vanilla room 06".
tech §14.4: "each of the 16 stages for 600 frames".

**Recommendation.** 1. Rule tech's map.
2. fortress and meta re-number to it: the meta index is unchanged, and engine ids come from tech §4.2.
3. The stage-attribute table (M2.1) is then needed before the Opening and Semifinal, but not before the first venue slice.

### scope-13. [MAJOR] fortress.md §4.3.3, §2.4 · Hidden costs in Must bosses (Doc Robot, Bass β copies)

**Issue.** Two Must bosses hide portability work.

**Doc Robot MK-VI** (H3, Must) runs the worst-scored champion's GP AI and boss sprite set inside H3's room. That means making all 8 reworked champion AIs and their 96-tile boss sets work outside their arenas. fortress itself argues against this for W2.

**Bass β** (Semifinal and W2, Must) copies 4, then 8, of the player's weapons 'as the player's own weapon projectile objects... their tiles are already in the player's sprite CHR'. But only the EQUIPPED weapon's shot tiles are resident ($71-$7F). Each copy therefore needs a CHR stream, or tiles placed in the boss set, and 8 enemy-side behaviours.

**Evidence.** fortress §4.3.3: "It runs that champion's own GP AI with that champion's sprite in a grey X-ray palette".
fortress §5.2.1: "the venue reworks... live in their arenas, and a generic room would break them."
fortress §2.4: "their tiles are already in the player's sprite CHR, so no CHR clash".
art_audio §1.1: "$71-$7F (15) | the equipped weapon's shot tiles | ... weapon change".

**Recommendation.** 1. Doc Robot: either warp through the fight loader into the copied champion's own arena with a grey palette (consistent with W2), or fix him to one champion. Budget it either way.
2. Bass β: copy only the weapon tiles already present in his own boss set (4 copies, pre-drawn into his 90 tiles), or stream the copied weapon's 15-tile set during the 30-frame ANALYZING tell. Budget it as 2-3 sessions in the Semifinal.

### scope-14. [MAJOR] fortress.md §1.6, §5.3; art_audio.md §6 · Poor value for cost: multi-size BG bosses on the critical path

**Issue.** The two most art-expensive bosses sit at the two ends of the critical path.

**Grand Pi-kun**, the tutorial's first boss, needs:
- the F-SIZES engine;
- 3 pre-drawn sizes (about 150 tiles);
- the pod-column split.

The Opening, the first stage every player sees, therefore depends on L art and the riskiest streaming code.

**The MODE-7 Machine** (W3, Must) needs:
- 3 sizes (340 BG tiles, the biggest single art item);
- F-SIZES;
- a 16-band floor (16 IRQs per frame with mid-frame Y scroll).

In both cases the joke is carried by one cheap element (the valve and charge lesson for Pi-kun, the rushing checkerboard for the Machine). The size streaming adds little.

**Evidence.** fortress §1.6: "three pre-drawn sizes (S 48 px, M 80 px, L 128 px) are streamed... [new-code] M (F-SIZES), [new-art] M (three sizes ≈ 150 tiles), Must."
art_audio §11.2: "the MODE-7 Machine's three sizes (340 BG tiles ≈ 28 h)".
fortress Risk 2: "The 16-band floor (W3) needs 16 IRQs per frame..."

**Recommendation.** For v1.0:
- Pi-kun: one size, using the Mr. X 2 pod technique.
- MODE-7: vanilla Wily Machine 6 art (kept, retinted), the 8-band programmatic floor, and the phases unchanged. The 'drives toward the camera' sizes and the 16-band floor become Should.

F-SIZES then becomes Should, with METALL 16 (W1).

### scope-15. [MAJOR] systems.md §11; fortress.md §2.6, §4.5, §5.3; meta.md §6; story.md §2.2 · Break Man: Should partner, Must character

**Issue.** The tag partner is Should (SYS-TAG-1, sheet L Should). But Break Man appears throughout Must content:
- the Opening's tip;
- the Semifinal help, block and reveal;
- the H5 disguise sprite;
- the W3 gift and the door hold;
- S40's carry;
- S47's debrief, with a portrait.

The rating's T1, the doping cost and two TAG-gated hidden rooms also depend on him. The docs give partial fallbacks: Roll brings the gift; tag doors become full-charge doors. But no doc separates 'NPC Break Man' from 'playable Break Man' in tiers or art.

**Evidence.** systems §0.1: "SYS-TAG-1 | Break Man tag partner | ... | L | Should".
art_audio §7.1: "Break Man (tag partner) | new... | 113 | 28 | ... | [new-art] L Should".
fortress Risk 7: "Break Man is a Should. If he is cut: the Semifinal's help and reveal still play (he leaves instead of joining)..."

**Recommendation.** 1. Rule two items.
   - Break Man NPC (Must): about 8-10 frames composited from Rock's sheet with visor, scarf and palette, used for cutscenes, the Semifinal, H5 and W3.
   - Break Man partner (Should): the full sheet, the call/swap code, tag gates.
2. Without the partner:
   - the TAG hidden rooms become full-charge doors;
   - rating T1 is replaced (for example 'Semifinal won without the HP<6 capsule');
   - the doping cost moves to the asterisk and the headline (it ships only with the booth).

### scope-16. [MINOR] venues_a/b.md, fortress.md, meta.md §9.1 · Duplicated systems: HUD widgets and counters

**Issue.** At least 15 HUD elements are specified separately:
- X-METER (bonus timer);
- X-LABEL (ZONE card, PASS n/3, FW 1.0);
- F-CLOCK (the escape);
- H1's SCORE counter and 'BALLS 17/24';
- Time Attack's HUD timer and splits;
- Knight's key count;
- Plant's treasure and log counter;
- the Semifinal's 'AUDITIONS 7/12';
- E2's rally counter;
- H5's MEGAMAN V letter row;
- the LOOP icons and POW states;
- the low-fuel pip;
- the lamp board;
- Knight's battle-log line.

Most are also 'collect N' predicates for secrets.

**Evidence.** venues_b §0.4: "X-METER... X-LABEL".
fortress §0.7: "F-CLOCK | A countdown in seconds and tenths drawn with sprites".
fortress §4.1: "a counter `BALLS 17/24` sits under the SCORE".
fortress §2.5: "a counter `AUDITIONS 7/12` appears".

**Recommendation.** 1. Build ONE sprite-HUD widget module (digits, label, meter, icon row) driven by data records. Size: M, owner: tech.
2. Back every 'collect N' secret with meta's stage-counter predicate ($4n), so a new counter costs data, not code.

### scope-17. [MINOR] venues_a.md T5; venues_b.md §1, §4; fortress.md §3, §4, §5 · Duplicated systems: attach and vehicle player states

**Issue.** About 11 bespoke player states are specified.

Attach states:
- vine hang (T5);
- Plant balloon hang;
- Blizzard condor carry;
- H4 claw GRAB;
- H4 Cossack Balloon;
- H5 Super Arrow ride;
- W3 Rush catch;
- the pogo EXWP.

Vehicle modes:
- SKY ACE: 8-way flight, no gravity;
- E3 CANNON: lane-locked;
- E4 MAZE: top-down on a lattice.

**Evidence.** art_audio §2.4 adds a pose set for each: "the vine-hang and carry poses (Plant, Blizzard condor...)", "the Rock-on-Rush loop poses (Wind sortie...)".
fortress §3.3: "CANNON mode"; §3.4: "MAZE mode".

**Recommendation.** 1. Build one 'attach to object' state: an offset, input rules and a release on A, using tech §7.9's GP player states. Vine, balloon, condor, claw and arrow all use it.
2. Build one 'free-flight vehicle' state with a constraint flag (none / lane). SKY ACE and CANNON both use it.
3. Cut MAZE.

### scope-18. [MINOR] story.md §6, §7; meta.md §4.1-§4.4 · Text volume in Must

**Issue.** About 600 Must strings, all in both EN and JP, with an external native-JP review on the release path.

The Must set includes:
- about 300 commentator lines: venue hooks plus 6 death lines per stage, generic tables, 16 + 12 heckles;
- two hint tiers per secret (a riddle plus an instruction) for 22 stages;
- Break Man's 18-entry debrief.

The flavour hooks add little at Must and risk 'chatty' pacing, which story itself flags.

**Evidence.** story §6.1: "About 300 lines × 2 languages × ~45 bytes ≈ 27 KB".
story Risk 4: "300 lines can feel chatty."
meta §4.1: "tier = (SECRETS[m].MISS >= 2) ? B : A".
story Risk 2: "These JP drafts were written by a non-native pass."

**Recommendation.** 1. Must text:
   - death tables, cut to 4 per stage;
   - first-weakness lines;
   - secret and plate lines;
   - Must scenes;
   - tier B hints;
   - help pages for the v1.0 chips;
   - about 350 strings in all.
2. Should text: the flavour hooks, tier A riddles, heckle variants, Bass Mode and the post-game.
3. Book the native-JP review as an external dependency with a date, because it gates release.

### scope-19. [MINOR] systems.md §13; venues_a/b.md HARD tables; fortress.md HARD tables · HARD content per stage

**Issue.** The HARD framework is Must, and every venue and fortress section designs HARD poke lists and AI branches. That is 22 stages and about 45 bosses with 'pinch at HP 13/14' style branches, plus a doubled test pass.

It is roughly 8 sessions of content plus testing, for a mode most players never select in a first release.

**Evidence.** systems §13.2: "HARD (SYS-DIF-2) [new-code] M, Must as a framework (content per venue)... Target: 4-12 pokes per venue".
venues_a §1.8, §2.9, §3.9, §4.9; venues_b §1.10 etc.; fortress §1.8, §2.8 and per wing.

**Recommendation.** 1. v1.0 HARD = ×1.5 damage, drops LESS, no refill, keeping the framework hooks.
2. Per-stage poke lists and boss AI branches become Should (v1.1), added stage by stage, using data that already exists in the docs.

### scope-20. [MINOR] systems.md §13.3; meta.md §2.3, §11.2 · Poor value for cost: the 1993 preset

**Issue.** The 1993 rules need:
- a generated vanilla row set;
- the vanilla transform cutscene path;
- the shop, chips, bolts, Beat rescue and refill switched off;
- a NEW-GAME-only flag;
- its own achievement and records badge.

systems says it 'doubles the test matrix'. The cost is real for a niche purist mode.

**Evidence.** systems Risk 9: "The 1993 preset doubles the test matrix."
meta Risk 8: "The 1993 preset's promise... rests on systems.md §13.3's generated '1993' row set (a Should)."

**Recommendation.** Demote 1993 to Could (post v1.0). Keep only the 'vanilla rules' data rows, which also serve the '???' fight if it ships.

### scope-21. [MINOR] systems.md §9; meta.md §6.1, §6.3 · Chip count and the crafting/doping web

**Issue.** 21 chips, against the BRIEF's 'about 14'. On top of the chips come:
- PARTs on 8 featured enemies;
- a garage with 4 recipes;
- Mr. Y's booth and Y-TURBO, with asterisks and a BREAK MAN WALKS event;
- a rating trap whose arithmetic relies on the partner (a Should).

This interlocked web touches systems, meta, story and every venue (featured-enemy tables). Each piece is small; together they are about 10 sessions plus balance, and any cut forces the rating to be re-derived.

**Evidence.** systems §9.1: "Why 21 and not the BRIEF's 'about 14'".
systems Risk 12: "the first cuts would be AFTERIMAGE and GLIDER".
meta §6.3: "If the tag partner (a Should) does not ship, the cost moves to FAIR PLAY... the trap's arithmetic must be re-checked".

**Recommendation.** 1. v1.0 ships about 14 chips: the 8 venue chips, the Balancer and 5 shop chips.
2. PARTs, the garage, the booth and TURBO move to Could, as one bundle that ships together with the partner.
3. Featured-enemy one-shots stay as in-stage tells, with no PART drop.

### scope-22. [MINOR] fortress.md §6.3; meta.md §9 · Poor value for cost: victory lap and post-game breadth

**Issue.** **The victory-lap credits** (Should) need:
- 8 looping screens;
- crowd card stunts per credit;
- 8 champions with idle animations and venue backdrop strips;
- a caged Wily on a float;
- the PHOTO FINISH still.

That is about 8 code sessions plus art, for the credits.

**The post-game** adds:
- Time Attack;
- 16 GP Rush courses (9 one-weapon cups, ALL-STAR, TRUE GP, MY GP);
- KNOCKOUT with simulated brackets;
- Exhibition Rules (12 rules, including TURBO);
- the Museum with a VAULT launcher for bank $28;
- 16 achievements;
- Bass Mode;
- Mr. X Returns.

About 50 sessions, mostly Could already.

**Evidence.** fortress §6.3: "[new-code] M, [new-art] M, Should".
meta §13 build list rows for KNOCKOUT (M Could), Museum (M Could), Mr. X Returns (M Could), TURBO rule (M Could).
meta Risk 7: "The post-game is large."

**Recommendation.** 1. v1.0 credits: the vanilla staff-roll engine with GP text and the DWNB cards kept (S, Must).
2. The victory lap moves to Could.
3. Post-game: EXTRA CONFIG and RECORDS 1-3 (Must), Time Attack (Should).
4. Everything else is Could or Won't (v1): KNOCKOUT, Exhibition Rules, Museum/VAULT, Bass Mode and Mr. X Returns are Won't.
5. The fight loader is Must regardless (W2).

### scope-23. [MINOR] art_audio.md §12.3-§12.5; fortress.md §0.1, §9.6; story.md S42 · Music: the Must count is too low, and tracks are missing

**Issue.** art_audio's Must music is G00-G04 only. But:
- story S42 and fortress §6.1 make the lights-out ending arrangement ('one stem per channel') Must;
- the Semifinal (Must) plays Break Man's whistle, which art_audio rates G27 Should.

fortress also asks for tracks that are not in art_audio's list at all:
- GP STADIUM (as distinct from G00);
- RIOT;
- FINAL LAP (the escape);
- the POCKET arrangements (W1, the escape, METALL 16).

The track list and the byte budget are therefore short by about 4-6 tracks.

**Evidence.** art_audio §12.5: "Must 2,990" (G00-G04).
story S42: "[new-music] S (an ending arrangement with per-channel stems) | Must".
fortress §0.1 W3 music: "new: FINAL LAP (escape)".
fortress §9.6: "RIOT... UPGRADE LAB (POCKET / 2A03 / MMC5), FINAL LAP...".

**Recommendation.** 1. Reconcile one track list owned by art_audio.
2. Must = G00-G04, the ending lights-out arrangement (2A03 only; MMC5 stems Could) and a 2-second whistle jingle.
3. RIOT, FINAL LAP and the POCKET arrangements are Should, with vanilla fallbacks ($0B, $18).

### scope-24. [MINOR] tech.md §6.3, §11.4, §16.4 · Dependency inversion: text canvas before level pipeline

**Issue.** In-stage pop-ups need a per-screen table of free BG tile ids (the canvas), and the level build produces that table (M2.7). But the text engine (M2.5), whose exit test is 'a dialogue and a pop-up play inside a vanilla stage', is scheduled first.

**Evidence.** tech §11.4: "The level build computes, per screen, the BG tile ids that neither that screen nor its scroll neighbours reference...".
tech §6.3: "Outputs: ... a per-screen table for the text engine's canvas (§11.4)."
tech §16.4: M2.5 (text) before M2.7 (level pipeline).

**Recommendation.** Order the free-id scan (part of M2.7, or a stand-alone script over the 16 vanilla stages) before M2.5. Alternatively, let M2.5's exit use a hand-made canvas table for one vanilla screen.

### scope-25. [MINOR] tech.md §5.5; systems.md §13.2 · Duplicated formats: HARD poke lists

**Issue.** Two poke-list formats are specified for the same data:
- tech: 4-byte entries `page_id, offset_hi, offset_lo, value` with a difficulty mask header;
- systems: 3-byte entries `[kind << 5 | screen] [offset] [value]`.

Venue docs write HARD tables without picking either.

**Evidence.** tech §5.5: "page_id (02 LAYOUT, 03 TILES, 01 WORK), offset_hi, offset_lo, value".
systems §13.2: "Proposed entry: 3 bytes, `[kind << 5 | screen] [offset] [value]`".

**Recommendation.** Rule tech's format (it covers layout, tiles and object lists in RAM). systems' text points to it, and the .lvl 'hard' lines compile to it.

### scope-26. [MINOR] tech.md §14; systems.md §13; meta.md §11 · Test matrix

**Issue.** These settings multiply:
- presets: CASUAL, NORMAL, HARD, 1993;
- languages: JP, EN, ENGRISH;
- MMC5 audio: on, off;
- ANNOUNCER: on, deaths-only, off;
- the Break Man partner: present, walked;
- per-venue route movies (normal exit, secret exit, plate route).

Without a stated policy, golden-movie maintenance becomes a hidden budget line on every content change.

**Evidence.** tech §14.7: "full | all of §14.4 + every venue route movie that exists + lag report".
systems Risk 9: "The 1993 preset doubles the test matrix."

**Recommendation.** 1. Golden movies run on NORMAL + EN only.
2. Each other setting gets one smoke movie per milestone.
3. Movies are re-recorded only at milestone gates.
4. Put the per-milestone test overhead in the ledger: about 10 % of the code sessions.

## Decisions needed (18)

1. **What is v1.0's scope, and who keeps the budget?**
   - Options: (a) Keep BRIEF §9 Must as written (about 550 sessions; about 830 in total).
(b) Tight Must (about 440).
(c) Release 'Round One' first, then v1.0.
   - Recommended: Make a session ledger the scope authority, and adopt the tight Must as the v1.0 definition (about 440 sessions):
- all tech foundations;
- core systems with weapon taps only;
- meta core;
- 8 venues cut to their core;
- Opening-lite, the Semifinal, H1/H3/H5, W2, W3, the ending and a vanilla-style staff roll.

Use 'Round One' (Opening, 8 venues and the Semifinal, about 290 sessions) as a scope checkpoint.
   - Affects: BRIEF §9, PLAN §8, the tier tags in all 8 docs

2. **What tier are the weapon alts and form synergies?**
   - Options: (a) Keep all 24 behaviours Must.
(b) Alts Must, synergies Should.
(c) Taps Must; alts and synergies Should.
   - Recommended: Must: forms fire every weapon's tap, and the dispatch table has alt and synergy columns. The 8 alts and 8 synergies themselves are Should (v1.1). B.ATTACK's Ice Block ships in the Blizzard slice as the prototype.
   - Affects: BRIEF §5.1, systems §3 and §4.8, art_audio §2.4, the venue and fortress 'weapons as tools' sections

3. **Which venue is the vertical slice, and when?**
   - Options: (a) PLAN M4: Opening + Wind + Knight.
(b) Blizzard.
(c) Flame.
   - Recommended: BLIZZARD end to end, about 115 sessions in: new game, bracket, venue, judges' desk, save, reload, replay. It comes after the minimal foundations, not after all of M0-M3.
   - Affects: PLAN §8 M4-M6, tech §16, venue build order

4. **What is the art staffing baseline?**
   - Options: (a) Recruit a pixel artist for the H list (about 660 h of Must).
(b) No artist, with the scope cut.
(c) Ship Claude drafts with the current scope.
   - Recommended: Plan for no pixel artist:
- reuse, composites and programmatic art first; Claude's drafts are final;
- one size per BG boss, with the W3 machine on vanilla Wily Machine 6 art;
- face icons instead of portraits and match-card portraits in v1.0;
- Break Man and Bass β composited from Rock's sheet.

A human pass is optional polish.
   - Affects: art_audio §6, §9.4, §11 and §13; fortress §1.6 and §5.3; meta and story portrait use

5. **How is Break Man split into tiers?**
   - Options: (a) Partner Must.
(b) NPC Must, partner Should.
(c) Cut him to story only.
   - Recommended: Break Man NPC (a composite of about 10 frames, for cutscenes, the Semifinal, H5 and W3) is Must. The playable tag partner is Should. Without the partner:
- the TAG rooms become full-charge doors;
- rating T1 is replaced;
- the doping cost ships only with the booth.
   - Affects: systems §3.11 and §11; fortress §2, §4.5 and §5.3; meta §6; story §2.2 and S20/S21/S47; art_audio §7.1

6. **Which stage-id map do we use?**
   - Options: (a) tech's map.
(b) fortress's (H/W at 8-15).
   - Recommended: tech §4.2: venues 0-7, legacy 8-15 kept, new stages $10-$1F. fortress and meta re-number to it.
   - Affects: tech §4; fortress §0.1 and §8 (the ??? fight, Mr. X Returns); meta fight table; golden-movie regression

7. **Should the Exhibitions be in v1.0?**
   - Options: (a) Keep all four as designed (Should).
(b) Simplify to single arenas.
(c) Defer to v1.1.
   - Recommended: No: Could (v1.1), and E4 Maze is Won't for v1. If they ship, each is redesigned as one arena with a lobby and a 'rule boss', built on map_set and T6. Rating T3 is removed from v1.0.
   - Affects: fortress §3, meta §3.1 and §6.1, art_audio §8 and G18-G21, story S22/S23

8. **Should the championship rating's maximum depend on Should content?**
   - Options: (a) Keep the 102/100 trap as designed.
(b) Re-derive per release tier.
   - Recommended: No. Re-derive the rows so that 100 is reachable with v1.0 content. Keep the TURBO trap and T1 only when the booth and partner ship.
   - Affects: meta §6, systems §9.4

9. **How do we unify duplicated engines?**
   - Options: (a) Unify as above.
(b) Leave per-doc implementations.
   - Recommended: Build one each, all owned by tech:
- one map-edit service (map_set plus an alternate-id flip, one repaint queue), under T6, VA-TIMED, F-PIECES and any grid; T6 is EITHER variant blocks OR the bitmap;
- one HUD widget module;
- one attach state and one vehicle state;
- one poke-list format (tech §5.5).
   - Affects: tech §5, §7.9 and §10; venues_a §0.4; venues_b §0.4; fortress §0.7; systems §13.2

10. **Which tileset-slot allocation do we use?**
   - Options: (a) tech §1.2.
(b) art_audio §2.2 (3 slots per bank, shared alternate set).
(c) One bank per venue (venues_b).
   - Recommended: tech owns one table, with 2 slots per bank and an independent alternate set per slot. TS_STADIUM serves the Opening, the Semifinal and the lap. art_audio's table is regenerated from tech's.
   - Affects: tech §1.2 and §5.2; art_audio §2.2; venues_b §0.2; fortress §0.1

11. **When is the MMC5 platform validated, and on what?**
   - Options: (a) Keep M1.6 after the port.
(b) Spike first.
   - Recommended: A 1-2 session go/no-go spike on Mesen (plus the user's cart, if any) BEFORE M1.1: header, 32 KB PRG-RAM pages, ExRAM-as-nametable through a mid-frame $5105, IRQ timing. The user names the hardware target now.
   - Affects: tech §16.3, BRIEF §7.1, tech Risks 1-2

12. **What tier is the fight loader?**
   - Options: (a) Should, as in meta.
(b) Must.
   - Recommended: Must, with a single owner. W2, Doc Robot, Time Attack, the EXTRA CONFIG FIGHT command and the mailbox all use it. The GP Rush runner and courses stay Could.
   - Affects: meta §9.2.1, fortress §4.3.3 and §5.2

13. **How big should the BG bosses be in v1.0?**
   - Options: (a) As designed (3 sizes, 16 bands).
(b) Single size, 8 bands.
   - Recommended: Pi-kun: one size. W3: vanilla Wily Machine 6 art with an 8-band floor. Gamma: head and fists, about 100 tiles. F-SIZES, the 16-band floor and the drive-toward-camera sizes become Should.
   - Affects: fortress §1.6, §4.3.4 and §5.3; art_audio §6; tech §8

14. **How much text is Must?**
   - Options: (a) About 600 Must strings, as story proposes.
(b) About 350.
   - Recommended: About 350 strings:
- death tables (4 per stage);
- first-weakness lines;
- secret and plate lines;
- Must scenes;
- tier B hints only;
- help pages for the v1.0 chips.

EN is caps-only. The native-JP review is booked as a dated external dependency.
   - Affects: story §6-§8 and §10; meta §4; art_audio §3.5

15. **What does HARD mean in v1.0?**
   - Options: (a) Full HARD content in all 22 stages.
(b) Preset-only HARD.
   - Recommended: ×1.5 damage, drops LESS, no refill, with the framework hooks kept. Per-stage poke lists and boss AI branches are Should.
   - Affects: systems §13; every HARD table in venues_a, venues_b and fortress

16. **What happens to the 1993 preset and to the chip, PART and booth system?**
   - Options: (a) As designed.
(b) Trimmed.
   - Recommended: 1993 becomes Could. v1.0 has about 14 chips (8 venue chips, the Balancer, 5 shop). PARTs, the garage, the booth and TURBO are Could, shipped as one bundle together with the partner.
   - Affects: systems §9 and §13.3; meta §2.3, §3.8 and §6; venue featured-enemy tables

17. **Is the 'SUPER' era in W2, W3 and the escape Must?**
   - Options: (a) As designed.
(b) Palette and music only.
   - Recommended: In v1.0 it is palette plus the music channel drop (D9 promoted to Must). ExGrafix, the POCKET flip-screen and the letterbox (F-ERA) go with W1 as Could.
   - Affects: fortress §5.0-§5.4, tech D6, art_audio §2.7 and §12.2

18. **How is Doc Robot MK-VI built?**
   - Options: (a) As designed (any champion in H3).
(b) Fight-loader warp.
(c) Fixed champion.
(d) Cut.
   - Recommended: He warps through the fight loader into the copied champion's own arena (consistent with W2), or he is fixed to one champion. He never runs champion AI in H3's room.
   - Affects: fortress §4.3.3, meta fight table

# critic-consistency

## Verdict

The eight docs agree on the core loop. These all match across systems, meta, story and the venue docs: Power after the 2nd win and Jet after the 4th, the Semifinal at 4 wins with the POSTPONED lock, the E1-E4 pairs, the vanilla weakness cycle, weakness 4/16, the 21 chip names and effects, plates as pickups, Kalinka as the debrief speaker, and the debrief weight order. The fortress damage rows (§8) match systems §4.5 cell for cell.

The docs are not yet consistent enough to build from. Eight conflicts need a ruling before M2:
1. Two incompatible stage-id maps (tech vs fortress).
2. A 'SUPER era' that relies on ExGrafix and an extra 4 KB CHR page. tech forbids both, and tech pins ExRAM as the text window.
3. Three different text-rendering models with different window sizes. The text budget is also about 3x what tech allocates.
4. A form swap that systems budgets at 1 KB and 12 frames. The measured sheet is 2 KB, which takes 16-32 frames at tech's VBlank rates.
5. story.md was written against a skeleton fortress.md, and roughly 15 late-game beats now contradict it: the Semifinal crowd, Break Man's join, the GP Cup, the unmasking, the W1 boss, the W3 boss, the escape, Wily's fate, the ending order, the CAPCOM TIMES and the lights-out cue.
6. art_audio's budget predates fortress v1. Grand Pi-kun, METALL 16, five mid-bosses, the rejects, the MUSEUM third and the six-screen exhibitions are missing or modelled differently.
7. venues_b's bolt bags break systems' economy and leave its four hidden rooms without envelopes.
8. meta's FILE block still carries the 15-chip, METALLS and DOVE draft, and has no storage for prize bits.

About 25 smaller mismatches follow. They are names, numbers, fonts, panel widths and flag bits; one, the IFHARD macro, tests the GUARDS bit instead of HARD.

Single sources of truth:
- systems: combat, economy and chip numbers.
- meta: save bytes, bracket, events and debrief.
- tech: ids, memory, raster and CHR/ExRAM limits.
- fortress and the venue docs: staging, mechanics and scene order.
- story: every word.
- art_audio: tile and byte budgets, re-run after the rulings.

Most of crossrefs' open questions have a clear answer from the other docs; they are resolved under the director decisions below.

## Strengths

- The acquisition order is identical everywhere: Power after the 2nd win, Jet after the 4th, the JET event before the Riot. See systems §2.3, meta §3.5-3.6, story S12-S14, venues_a §0.3, venues_b §0.3 and fortress §2.
- The fortress MK-VI W/G/R cells (fortress §8) match systems §4.5 exactly for the Yellow Devil, Mecha Dragon, Gamma phases 1 and 2, the Cossack Catcher, Dark Man, the W3 machine and the Capsule. The Grand Pi-kun and Bass β rows match too.
- The Exhibition pairs (E1 Wind+Knight, E2 Tomahawk+Plant, E3 Blizzard+Flame, E4 Yamato+Centaur) are consistent across meta, both venue docs and fortress. Fortress reuses them for the W2 pair bouts.
- The chip names, effects and order match between systems §9.2, story §8, art_audio §9.5 and the venue docs. The only stale copy is meta's.
- The meta index (meta §1.8) decouples the save format from engine stage ids, so the id-map dispute does not touch the save layout.
- The debrief order is unified: meta §4.3's weight rule. venues_a's text already follows it. story §7 corrects four factually wrong tier-A riddles.
- Fight ids $18-$28 agree between meta §9.2.1 and fortress §8 ($26 Pi-kun, $21/$23 Bass, $1C-$20 MK-VI, $22 W1, $24/$25 W3, $27 ???, $28 Mr. X).

## Findings (44: blocker 1, major 13, minor 30)

### consistency-1. [BLOCKER] fortress.md · §5.0 F-ERA, §5.1 tileset, §5.2 moat, §4.6 step 7, §9.1 ExGrafix; vs tech.md D6/D7/§3.3/§11.3; art_audio.md §2.7

**Issue.** The SUPER era is built on hardware use that tech rules out. ExGrafix needs ExRAM in mode 1, but tech pins ExRAM to mode 0 for the whole game as the text-window nametable. The 'extra 4 KB CHR page' cannot exist with 8 KB of CHR-RAM. ExGrafix in scrolling stages is forbidden by tech D6, yet W2 (Must, scrolling moat) and W3 use it. As written, no pop-ups, heckles or dialogue could appear on any SUPER screen.

**Evidence.** tech D6: '8 KB CHR-RAM, no CHR banking beyond 8 KB, no ExGrafix in scrolling stages'. tech §3.3: 'Mode 0 for the whole game (D7): ExRAM is a nametable'. fortress §5.0: 'ExGrafix: MMC5 ExRAM mode 1 gives each 8×8 tile its own palette and 4 KB CHR page'. fortress §5.1: 'one extra 4 KB CHR page of "16-bit" detail tiles'. fortress W2 00-05: 'now in SUPER colour'. art_audio §2.7: 'With 8 KB of CHR-RAM the page bits only reach the two pattern tables ... Use it only in W1's "16-bit" tier' (Could). story S36-S39 and the Wily heckle table (§6.5) are Must text in W1-W3.

**Recommendation.** Make tech's rule the source of truth. Redefine the SUPER tier as:
- richer per-screen BG palettes;
- raster palette and parallax bands;
- foreground pillars;
- MMC5 audio.
This is fortress risk 3's own fallback. Allow ExGrafix only as a Could on the static 'SUPER WILY CASTLE' picture (fortress §4.6 step 7), which has no scroll and no text window. Fortress must rewrite the §5.0 table, the §5.1 tileset line, the W2 moat, the ring and §9.1. art_audio §2.7 must narrow its scope to that picture.

### consistency-2. [MAJOR] tech.md / fortress.md · tech §4.2 id map, Open question 1; fortress §0.1, §9.1, Open question 1

**Issue.** There are two incompatible stage-id maps. fortress puts H1-H5 and W1-W3 in the vanilla fortress ids 8-15 and drops the legacy stages. tech keeps 8-15 as untouched legacy stages and puts H/W at $16-$1D. meta's fight table, the ??? fight ($27, vanilla Wily 4 under vanilla rules), the 1993 CUP and Mr. X Returns all need the legacy ids. fortress's own plan gives no id to vanilla Wily 4. It also still needs the attribute table for ids 16-23 (Mr. X Returns at 22 has bit 3 clear).

**Evidence.** tech §4.2: '$08-$0F legacy Mr. X 1-4, Wily 1-4, unchanged ... serve meta.md's fight table (legacy arenas), Mr. X Returns' base map'. tech §4.2: '$16-$1A Hall of Fame H1-H5', '$1B-$1D W1-W3', '$1F Mr. X Returns ... points at id $08's layout'. fortress §0.1: 'H1-H5 and W1-W3 therefore keep the fortress ids 8-15'; 'Mr. X Returns | 22'; 'Victory lap | 23'. fortress §8: '$27 ... vanilla Wily 4's whole final fight, untouched'. tech M2.1 rewrites all 45 $51 readers anyway, which removes fortress's only reason to reuse 8-15.

**Recommendation.** Adopt tech §4.2 as the source of truth. Fortress then updates the 'Proposed id' column of §0.1 and §9.1 (Opening $10, Semifinal $11, E1-E4 $12-$15, H $16-$1A, W $1B-$1D, lap $1E, Mr. X Returns $1F) and drops the 'AND #$08 stays valid' rationale. meta's fight records point $27 at legacy $0F, room 06, with RULESET = 1993.

### consistency-3. [MAJOR] tech.md / story.md / art_audio.md / meta.md · tech §11.1, §11.4; story §10.2; art_audio §9.6, §3.5; meta §4.1

**Issue.** There are three incompatible text-rendering models with different window geometries:
- tech renders a VWF canvas.
- story and art_audio upload a per-page glyph cache of distinct 8×8 glyphs.
The limits differ too:
- Pop-up: tech allows 2 lines × 16 tiles (about 16 JP characters a line); story writes 2 × 28 cells with ≤ 24 glyphs.
- Dialogue: tech allows 3 lines × 26 columns; story SCN pages and meta's debrief are 4 × 28; help pages are 3 × 28.
Story's JP pop-up lines do not fit tech's canvas.

**Evidence.** tech §11.4: 'Pop-up: 2 lines × 16 tiles (32 ids)'; tech cross-doc table: 'pop-up 2 lines × 16 tiles (~22 EN characters with the VWF, 16 JP), dialogue 3 lines × 26 columns'. story §10.2: 'Glyph cache, not a resident font ... POP (in-stage) 2 × 28 ... 24 tiles'; 'SCN 4 × 28'; 'Debrief 4 × 28'. art_audio §9.6: 'a 2-line pop-up uses only its distinct glyphs (typically 18-24 for EN, 20-26 for kana) ... stores up to 32'. meta §4.1: '4 lines × 28 characters'.

**Recommendation.** Make one model binding:
- Rendering: story's per-page glyph cache with fixed 8-px cells; drop the VWF.
- Window: tech's ExRAM-nametable window (D7) and its borrow/restore for frozen dialogue.
- Sizes: POP 2 × 28 with ≤ 24 distinct glyphs, plus a 4-tile face icon; SCN and debrief 4 × 28; help pages 3 × 28; plaques 9 × 28.
- Cases: EN in ALL CAPS, JP kana only.
Rewrite tech §11.4 and its cross-doc row, and art_audio §3.5 and §9.6 (no mixed-case set).

### consistency-4. [MAJOR] tech.md / story.md · tech §1.2 bank roles; story §10.4, §6.1, §12

**Issue.** The text data budget is about a third of the stated need. tech reserves 4 banks (32 KB) for all JP/EN/ENGRISH strings and fonts. story sizes the text at 70-90 KB, with about 27 KB for commentary lines alone. story also says this fits in '2-3 text banks', which is arithmetically impossible with 8 KB banks.

**Evidence.** tech §1.2: '$46-$49 | text data: JP, EN, ENGRISH strings and fonts'. story §10.4: '≈ 70-90 KB with a simple dictionary compression of common words, in 2-3 text banks'. story §6.1: '≈ 27 KB in a text bank'. story §12: '~80 KB of text banks'.

**Recommendation.** tech allocates 10-12 banks to text, from the $7D reserve, the $0B-$0F pool or a rebalance of the 16-bank music reserve, of which art_audio needs only 5. story corrects '2-3 text banks' to '9-11 8 KB banks'. Measure the dictionary compression at M2.5 before freezing the allocation.

### consistency-5. [MAJOR] systems.md · §0 decision 2, §1.3 SYS-CTL-4; vs art_audio §1.5/§2.6; tech §15.3

**Issue.** The quick form swap is budgeted on a false premise. systems targets 64 tiles (1 KB) behind a 12-frame flash, with Rock hidden and a 20-frame cooldown 'so a stream always finishes'. art_audio measured that the whole 2 KB sheet must stream. At tech's VBlank budget (64 B on column-paint frames) a swap while walking takes about 32 frames: longer than the cooldown, with Rock invisible the whole time. tech §15.3 still quotes the old ≤ 1 KB figure. The Gamma 'Jet up, swap to Power' skill route depends on this swap.

**Evidence.** systems §1.3: 'Target n ≤ 8: at most 64 changed tiles (1 KB) ... a 12-frame flash'; 'Rock's sprite is hidden'; '20-frame cooldown (tune) between form swaps, so a stream always finishes'. art_audio §1.5: '109-114 of their tiles exist nowhere in it ... a form swap streams the whole 2 KB sheet'. tech §15.3: 'a column paint 64 B'; 'systems.md's form swap (≤ 1 KB) takes 8-16 frames'.

**Recommendation.** Rewrite SYS-CTL-4 for 2 KB:
- Make the unrolled 256 B/frame copier Must (tech lag step 5 already is).
- Keep the old-form tiles visible and stream into the inactive area, so Rock never disappears for more than the final flip.
- The cooldown is 'until the stream completes', not 20 frames.
- Queue against other streams (pop-up glyphs, pinch sets).
Correct tech §15.3 and fortress §4.3.4's skill route timing.

### consistency-6. [MAJOR] story.md · §0 acts IV-VI, §3 S32-S45, §5.4, §11; vs fortress.md §4.5-§6

**Issue.** story.md was written against a skeleton fortress.md, and its late game now contradicts fortress v1 in at least eleven places:
- (a) The GP Cup sits on a pedestal after H5 and powers 'WILY MACHINE 6.5'; fortress has it recovered from the Trophy Dispenser in W3 before the machine.
- (b) Mr. Y unmasks in a 'central gallery' by tearing off a moustache; fortress uses H5's throne room and two masks (Y→X→Wily).
- (c) The W1 boss is 'THE UPGRADER' in story; fortress has METALL 16 (fight $22).
- (d) The W3 boss is 'WILY MACHINE 6.5' in story; fortress has the MODE-7 MACHINE, and fortress never uses the name.
- (e) The escape ends with Break Man carrying Rock and Wily ('This time'); fortress has Rush catch Rock and Break Man hold the door while Wily flees by pod.
- (f) Wily goes to jail (S41, 'Mr. Z'); fortress has him crash at the stadium and ride caged on Eddie's float in the lap.
- (g) Ending order: story runs lights-out → sixth wing → CAPCOM TIMES → lap; fortress runs CAPCOM TIMES → lights-out → lap.
- (h) CAPCOM TIMES: story drops vanilla $94; fortress keeps $94 verbatim as a beat.
- (i) Story has no scene for Break Man's W3 gift (CHAMPION BUSTER), the injury-time confession, 'PSYCH!', Flip-Top Jr. or the rejects.
- (j) The Mr. X card text differs.
- (k) The doped headline reads 'UNDER REVIEW' in story and 'UNDER INVESTIGATION' in systems and fortress.

**Evidence.** story Risks 7/§12: 'Several scenes depend on fortress.md, which is still a skeleton'; §5.4: 'THE UPGRADER is this doc's proposal for the W1 boss, which fortress.md owns and has not yet named'. fortress §5.1.4: 'Boss: METALL 16 (fight $22)'. story S32: 'the GP Cup sits on a pedestal with cables'; §5.4 WILY MACHINE: 'ENERGY ... THE GP CUP'. fortress §5.3.1: 'when it breaks, the GP CUP falls intact, and Rock picks it up'. story S40: 'Tch. I'll take him too. This time.'. fortress §5.4 0B-0C: 'Rush Jet swoops in and catches Rock'; 'Break Man holds it open'. story S41: 'The Committee's security robots lead Wily away'. fortress §6.3: 'Wily in a cage on a float pulled by Eddie'. story S44: 'Vanilla's own page $94 ... is not reprinted'. fortress §6.1 scene 6: 'vanilla's $94, verbatim'. story S28 card: 'MR. X. INTERNATIONAL ROBOT FINANCIER.'. fortress §4.5.3: 'MR. X. SPONSOR, 1ST WORLD ROBOT CHAMPIONSHIP. (NO RELATION.)'.

**Recommendation.** Split ownership: fortress owns staging, mechanics and scene order; story owns every word. Then story re-syncs:
- Rename and reword S32 (empty pedestal, cables leading to the castle).
- Retitle S35 for METALL 16 and move 'INSTALLING... 3%' to W1 00's FORMAT CHECK.
- Keep the joke card 'WILY MACHINE 6.5' for fortress's MODE-7 Machine, with ENERGY 'PROJECT SUPER'.
- Rewrite S39-S41 around 'PSYCH!', the pod, the door, the stadium crash and the cage.
- Adopt fortress's ending order. The S43 sixth wing becomes the post-game (S49 already references it).
- Add the gift, confession, Flip-Top Jr. and reject lines.
- Pick one headline and one card text: story's words, with systems and fortress updated.

### consistency-7. [MAJOR] story.md / fortress.md · story S04-S08, S17-S20, BM-1..BM-3; fortress §1.3, §1.4, §2.2-§2.6

**Issue.** The Opening and the Semifinal are staged differently, and the docs disagree on where Break Man joins, which decides when FORMS.TAG and EVENTS b5 are set.
- Opening: story has Break Man on stage (BM-1 roll call, BM-2 charge tip), Roll at the pit, eight podiums, and a shop that opens 'after your first match'. fortress says 'no Break Man', uses parade floats, and Eddie says 'opens after the ceremony'.
- Semifinal: story has Sniper Joes in Bass scarves, 'Break Man holds the crowd', and Bass simply teleporting out. fortress has rejected entrants, a rubble help beat and the β OVERDRIVE block.
- Join: fortress sets FORMS.TAG in-stage at 0E with a banner. story joins him on the bracket via Rule 9 (S20, EVENTS b3→b5).

**Evidence.** fortress §1: 'The player owns the buster only. No form, no weapon, no Break Man, no RETIRE.' story BM-2: 'S08 Opening boss | "Hold B. Let go when you glow."'. story S04: 'EDDIE'S PIT STOP. OPENS AFTER YOUR FIRST MATCH.'. fortress 06: '"Pit stop opens after the ceremony!"'. systems §8: E-TANK, 1UP and three chips 'start'. story S17: 'The stands are full. Of Sniper Joes. In Bass scarves.'. fortress §2.2: 'UMBRELLA MAN ... VENDING MAN ... CHEER MAN'. fortress §2.6: 'Sets FORMS.TAG and EVENTS b5 ... Banner: BREAK MAN JOINS!'. story S20: 'On the bracket, right after the Semifinal: the POSTPONED stamps peel off (b3), then the join (b5)'.

**Recommendation.** Use fortress's mechanics with story's words.
- Semifinal: rejects and the β OVERDRIVE block. Story rewrites S17-S19, and S18 becomes the 06 rubble help.
- Reveal vs join: the reveal plays in-stage at 0E, but the join is story's S20 on the bracket. FORMS.TAG and b5 are set by the bracket event; fortress removes the 0E banner and the 'Sets FORMS.TAG'.
- Opening: Break Man's tip is a whistle POP only, with no sprite and no conflict with 'no Break Man' as a playable. S06's roll call plays at the parade's end, and S05's podiums become fortress's floats.
- Shop: the Pit Stop opens after the Opening (0 wins), which matches systems and meta.

### consistency-8. [MAJOR] art_audio.md · §5, §6, §7.2, §8, §13; vs fortress.md §0.6-§6, §9.6

**Issue.** The art budget predates fortress v1. Several fortress assets are missing or modelled differently:
- Grand Pi-kun (Must): a 70-tile sprite boss whose head pops off to show a Met, vs fortress's NT1 BG boss with three streamed sizes (≈ 150 BG tiles, F-SIZES).
- METALL 16 (3 eras, ≈ 160 tiles) is absent.
- The five mid-bosses (Big Eye, Picopico-kun, Doc Robot, Enker, Trophy Dispenser) are absent.
- The Semifinal rejects, the BASS BLASTER and the ACCEPTED stamp are absent.
- The MUSEUM third shared by the five wings is absent.
- The exhibitions are budgeted as 'single-arena guest matches' (92 BG tiles in all), vs fortress's six screens each on a TS_ARCADE base plus four thirds.
- Flip-Top Jr. is absent.
- The BG-boss techniques differ for the Yellow Devil, Mecha Dragon, Cossack Catcher and the MODE-7 floor bands.
- The Dark Man tell differs: fortress uses an orange scarf, art 'one shade off', story the 'wrong side'.
- The victory lap is a 'silhouette walk' in art vs fortress's stadium track with card stunts.

**Evidence.** art_audio §7.2: 'Grand Pi-kun | Opening | 70 | 14: ... head-off (the costume head pops off at pinch to show a Met inside)'. fortress §1.6: 'three pre-drawn sizes (S 48 px, M 80 px, L 128 px) are streamed into CHR-RAM by F-SIZES ... [new-art] M (three sizes ≈ 150 tiles)'. art_audio §5: 'E1-E4 Exhibitions | Single-arena guest matches | 92'. fortress §3.0: 'One tileset, TS_ARCADE ... plus one CHR third per exhibition'. art_audio §6: 'Yellow Devil ... X Crusher ... 64x80'; 'Mecha Dragon ... Wily Machine (NT1 + floor split, chain $19)'; 'Cossack Catcher ... Metonger Z ... chain $1A'. fortress §4.1.2: 'Wily 2's walker room ... chain 7 ... a 3×4 grid of 16×16 pieces (48×64 px)'; §4.2.3: 'Mr. X 4 X Crusher technique ... chain $16'; §4.4.1: 'Mr. X 2 pod-column technique ... chain 7'. grep of art_audio finds no Big Eye, Enker, METALL 16, Picopico, Doc Robot, Trophy Dispenser, Flip-Top or MUSEUM third.

**Recommendation.** fortress owns what each asset is and which technique it uses; art_audio re-runs budget.py against fortress v1. Add Pi-kun's sizes, METALL 16, the mid-bosses, the rejects, the MUSEUM third, TS_ARCADE and the exhibition screens, and Flip-Top Jr. Adopt fortress's precedents per boss and one scarf tell (fortress's orange scarf; story and art follow). Expect the Must tile count to rise above 4,851. Re-check the 660-hour estimate.

### consistency-9. [MAJOR] tech.md / art_audio.md / fortress.md / venues_b.md · tech §1.2, §5.2; art_audio §2.2; fortress §0.1; venues_b §0.2

**Issue.** There are three different tileset-slot architectures:
- tech allocates 8 banks with 2 slots each (16 slots), each slot with its own alternate set via the RAM image.
- art_audio allocates 10 banks with 3 slots each (30 slots) and a shared alternate set per bank. It forbids two alternate-heavy stages in one bank, gives each exhibition, the Opening and the Semifinal its own slot, and puts the lap and lobby in vanilla's empty slots.
- fortress shares slots (TS_STADIUM for the Opening, Semifinal, lobby and lap; one TS_ARCADE; TS_LAB) and adds TS_H1-H5, TS_W2 and TS_W3 copies.
- venues_b asks for 'a whole 8 KB tileset bank per venue'.
The slot demand (about 24) exceeds tech's 16.

**Evidence.** tech §1.2: '$64-$6B | tileset slots (2 per bank, each with its own alternate set, §5.2)'. tech §5.2: 'the loader copies slot pages and the alternate set from two independent sources, so two venues share one ROM bank'. art_audio §2.2: '10 new 8 KB banks (80 KB) for 30 slots ... two alternate-heavy stages must not share a bank'. fortress §0.1: 'TS_STADIUM (Opening, Semifinal, GP Rush lobby, lap), TS_ARCADE (the four exhibitions), TS_LAB (W1 and the escape)'.

**Recommendation.** Make tech's RAM-image model the source of truth: an independent alternate set per slot, which retires art's no-sharing rule and venues_b's whole-bank request. Store 3 slots per ROM bank and use fortress's sharing for the slot list: 8 venues × 2, plus STADIUM, ARCADE, LAB, H1-H5, W2 and W3, about 26 slots in 9-10 banks. Update tech §1.2 ($64-$6D) and art §2.2.

### consistency-10. [MAJOR] venues_b.md · §1.3 screen 10, §1.5.2, §2.5.2, §3.6.2, §4.6.2; vs systems.md §7, §15.2

**Issue.** venues_b's prize money breaks systems' grind-proof economy, and none of its four hidden rooms holds the sponsor envelope that systems, meta (SECRETS b4) and the debrief icons expect. Seven vegetables at 5-20 bolts each, plus a 50-bolt bag (×3) or a 100-bolt chest in each hidden room, put every venue far above the 60-bolt cap. Systems had already answered venues_b with that cap.

**Evidence.** venues_b §1.3: 'prize vegetables (eggplant 5, carrot 10, cabbage 15, corn 20 bolts)' (4 on 10, 3 on 11). venues_b §1.5.2: 'a 50-bolt bag'; §2.5.2: 'a 50-bolt bag'; §3.6.2: 'a 50-bolt bag'; §4.6.2: 'a 100-bolt chest'. grep of venues_b finds no 'envelope'. systems §7: 'Sponsor envelope | 30, once per save | one in each venue's hidden room (8)'; 'at most 60 per venue (tune)'. systems §15.2: 'Venue prize bolts are paid once per save, at most 60 per venue'.

**Recommendation.** systems is the source of truth. Replace each bag or chest with the sponsor envelope (30). Re-price Blizzard's vegetables to total ≤ 60 (for example 5/5/5/10/10/10/15). List Y.SPEAR's 'bolts' ledge on Blizzard 05 inside the cap.

### consistency-11. [MAJOR] meta.md · §1.6 FILE block, §3.8, §9.2.5, §9.6; vs systems.md §9.1-9.3, §15.1

**Issue.** The save layout still carries systems' first draft.
- CHIPS_OWNED and CHIPS_EQ are 16 bits (15 chips); there are 21 chips.
- The pit-stop grid shows '15 chips'; MY GP and EXTRA CONFIG use 16-bit chip fields.
- METALLS 'IRON HELMET at 20' is stale: IRON HELMET is now crafted.
- RATEFLAGS b4 'DOVE run (systems.md chip 10)' is stale: chip 10 is THERMOS and DOVE is cut.
- The garage shows 'THERMO CORE'.
- There is no field for venue prize bits (one per placed prize: bounties, treasures, pouch, vegetables).
- STAGEREC has 24 rows; systems says 32.
- DIFF A's DROPS cannot encode 1993's 'vanilla 12.1 %'.
- systems names BREAK_JOINED where meta uses FORMS.TAG.
The save layout is frozen at v1.0, after which only migrations are allowed.

**Evidence.** meta §1.6: '$03A | 2 | CHIPS_OWNED | 16 bits, in systems.md §9.2's order (15 chips)'; '$040 | METALLS | ... (IRON HELMET at 20'; '$045 RATEFLAGS ... b4 DOVE run achieved (systems.md chip 10)'. meta §3.8: 'A grid of the 15 chips'; 'SNOW + EMBER → THERMO CORE'. systems §9.1: '21 chips in a 24-bit CHIPS_OWNED'. systems §15.2: 'the METALLS counter and the DOVE flag are no longer used'. systems §15.1: 'venue prize bits (8 × 1); per stage × 32'. systems §13.2 1993: 'DROPS ... vanilla 12.1 %'. systems open question 9 still says 'keeps chips at 15'.

**Recommendation.** meta owns the bytes and applies systems' amendments:
- 3-byte CHIPS_OWNED and CHIPS_EQ.
- Remove METALLS and DOVE; free their bytes.
- Name the chip THERMOS.
- Add a 4-byte PRIZES field (bit per placed prize, assigned by the venue docs) from the $162 reserve.
- Keep STAGEREC[24] (meta 0-23 is complete) and fix systems' '×32'.
- Add a DROPS 'VANILLA' encoding, or derive it from the RULES=1993 bit.
- Rename BREAK_JOINED to FORMS.TAG in systems.
- Fix systems open question 9.

### consistency-12. [MAJOR] fortress.md / systems.md · fortress §0.2, §4.3.4; systems §2.4, §13.3, §4.6 SC5

**Issue.** The H3 boss (Must) breaks fortress's own main-route rule. §0.2 says the only tools a main route may require are the full charge and the Magnet Beam, and that every punch or form gate is optional. Gamma phase 2 (SC5) can only be hurt by fists, which needs Power or Super. systems promises 1993 and Bass Mode finishability on the normal-route rule.

**Evidence.** fortress §0.2: 'the buster's full charge ..., the Magnet Beam from H1's display case on, and nothing else. Every punch, form, alt, synergy, weapon and Break Man gate is on optional content.' fortress §4.3.4: 'SC5: only fists hurt the cockpit (tap punch 2/30, PUNCH★ and Time Fist 4/12, Morning Star 3/20, the Super fist 3/20 on replays; everything else dinks)'. systems §2.2: 'Super arrives only after H3's Gamma, which is a Power test (SC5)'. systems §13.3: 'It is finishable because of the normal-route rule'.

**Recommendation.** Amend fortress §0.2. Power, guaranteed from the 2nd win and usable in 1993 through the pause menu, is an allowed required tool exactly once: Gamma phase 2, with the existing plaque as its sign. Do not lend the Super Adaptor. Bass Mode (Could) needs its own Gamma answer, for example the Bass Buster at 1/32.

### consistency-13. [MAJOR] art_audio.md / fortress.md / story.md · art_audio §12.3, §12.5, §1.7; fortress §0.1 music column, §6.1 scene 7, §9.6; story S42

**Issue.** The audio plan is missing Must music, and its names do not map to the stage docs.
- The ending's channel-by-channel 'lights out' arrangement (Must in both fortress and story) is not in art_audio's track list.
- Fortress's FINAL LAP (escape), RIOT and GP STADIUM have no G-number.
- Fortress's 'HALL OF FAME (shared theme, 5 arrangements)' contradicts art's G08-G12, each an arrangement of a different RM1-5 theme.
The channel-drop design itself conflicts:
- Fortress drops the MMC5 pulses first, inside the ending.
- Story says the MMC5 pulses were already silenced when the castle fell.
- Story's cue 'DPCM stops' refers to a channel the driver does not use; DPCM is Could.

**Evidence.** fortress §6.1 scene 7: 'MMC5 pulse 2, MMC5 pulse 1, noise, triangle, pulse 2, until pulse 1 plays the melody alone ... [new-music] M'. story S42: 'an arrangement of the ending theme with one stem per channel'; '| 3 | DPCM stops |'; 'its two extra pulses were already silenced when the castle fell'. art_audio §12.3: 'Ending scenes, newspaper, TO BE CONTINUED | vanilla $08, $1B-$22 | | kept'. art_audio §1.7: 'Channels | pulse 1, pulse 2, triangle, noise. No DPCM'.

**Recommendation.** Add 'G37 LAST MATCH' to art_audio as Must (about 600 B, 4 stems, using D9's mute mask). Order: MMC5 voices first if on, then noise, triangle, pulse 2, pulse 1. Remove the DPCM cue from story. Map fortress's names to G-ids: GP STADIUM = G00 stage cut, RIOT = G04 stage entry, FINAL LAP = a new Should id or G15. Rule on the Hall of Fame concept (see the decisions).

### consistency-14. [MAJOR] art_audio.md / story.md · art_audio §9.4, §1.2, §17 risk 2; story §6.1, §6.2 EV_WEAK_FIRST

**Issue.** The first-weakness commentator line (BRIEF §5.1, Must) plays in boss rooms. Its face icon is planned for the sprite enemy area, which the champion boss sets fill completely: Wind, Yamato and Knight have no spare tiles. art_audio's 'boss rooms always have room' is about BG ids, not the sprite area.

**Evidence.** art_audio §9.4: 'In-stage pop-ups use a 16x16 face icon instead (4 sprite tiles each ...), streamed into the enemy area's free tiles'. art_audio §1.2: 'Boss sprite sets fill the enemy area: ... Wind $3F 96, ... Yamato $3E 96, ... Knight $39 96'. art_audio §18 question 4: 'Boss rooms always have room, so the weakness line is safe'. story §6.2: first-weakness lines for every boss.

**Recommendation.** Draw the face icon as 4 BG tiles inside the pop-up's glyph strip, so the total is 24 glyphs plus 4. BG has room in boss rooms (art §1.4: 52-195 ids used). Alternatively, reserve one generic 'microphone' icon in GP-COMMON. Update art §9.4 and the tech §11.4 canvas count.

### consistency-15. [MINOR] tech.md / meta.md / systems.md · tech §5.5 IFHARD; meta §1.6 DIFF A; systems §13.2

**Issue.** The HARD flag test is wrong. A 6502 BIT copies bit 6 into V and bit 7 into N. tech's 'BIT DIFF_A / BVC' therefore tests bit 6, which is GUARDS, while meta puts HARD at b5. systems' 'BIT CFG_HARD / BMI' tests bit 7, which is RULES = 1993. The three docs name three different bits; a straight implementation would switch HARD behaviour on GUARDS.

**Evidence.** tech §5.5: 'IFHARD = BIT DIFF_A / BVC (b5 HARD on)'. meta §1.6: 'DIFF A | b0-1 DAMAGE ...; b4 CRITICALS on; b5 HARD on; b6 GUARDS on; b7 RULES = 1993'. systems §13.2: 'tests BIT CFG_HARD / BMI'.

**Recommendation.** meta owns the bits. Move HARD to b6 of DIFF A (swap with GUARDS) so 'BIT DIFF_A / BVC' is correct and costs no extra cycles in the 121-style AI tests. systems' text says IFHARD.

### consistency-16. [MINOR] tech.md · §5.5 poke lists; vs systems §13.1, meta §1.6 (DIFF preset 4 = EDIT), venues_b CASUAL levers

**Issue.** Poke lists are keyed to the preset, but HARD is a per-file override and the preset becomes EDIT after any hand change. A NORMAL file with HARD switched on (preset EDIT) gets no HARD layout. CASUAL-only levers, such as venues_b's refill delays and extra checkpoints, have no flag to key on.

**Evidence.** tech §5.5: 'header: difficulty mask (b0 CASUAL, b1 NORMAL, b2 HARD, b3 1993) ... A list applies when mask & current_preset_bit ≠ 0'. meta §1.6: 'DIFF preset | 0 CASUAL, 1 NORMAL, 2 HARD, 3 1993, 4 EDIT'. systems §13.1: 'HARD | OFF / ON | poke lists + AI BIT tests'.

**Recommendation.** Key the list on a derived LAYOUT TIER: HARD if the HARD bit is set, otherwise CASUAL if GUARDS is on, otherwise NORMAL; 1993 if RULES = 1993. Compute it once into RULESET (meta §9). The mask bits stay as they are.

### consistency-17. [MINOR] fortress.md · §4.1 H1 0B and HARD; vs systems §3.10

**Issue.** The arithmetic of the only required fortress gate is wrong. A Magnet Beam stops at 64 px, but the gap is 96 px and the text says 'build a beam, walk across'. HARD's '112 px (two beams)' implies NORMAL needs one.

**Evidence.** systems §3.10: 'On release, or at 64 px, it freezes into an 8-px-tall solid platform ... Max 3 beams'. fortress H1 0B: 'a 96-px gap ... Build a beam, walk across'. fortress H1 HARD: 'the gap 112 px (two beams)'.

**Recommendation.** Either narrow the NORMAL gap to ≤ 56 px (one beam plus the ledge) and HARD to 96 px (two beams), or keep 96 px and teach 'two beams' in the sign and plaque. systems' 64 px is the source of truth.

### consistency-18. [MINOR] fortress.md / systems.md · fortress §3.0, §8; systems §4.2, §4.3, §6.5

**Issue.** Exhibition rule damage is 'booked as class 4 (HAZARD)', but systems defines HAZARD as 0 damage on every boss ('bosses ignore player-lit oil'). The 4/12 rule cell has no column. WEAK FINISH (STYLE 4) is also impossible in exhibitions.

**Evidence.** fortress §3.0: 'rule damage is booked as class 4 (HAZARD)'; 'A guest takes 4 with 12 i-frames from its rule event'. systems §4.2: 'M.BEAM, HAZARD | 0 | utilities. Bosses ignore player-lit oil, so no cheese'. systems Table 1: 'M.BEAM, HAZARD | 0 | ...'.

**Recommendation.** Add a RULE source column to GP_BOSSHIT: 4/12 with the WEAK bit on the E1-E4 rows, 0 elsewhere. Book it as class 4 for VARIETY. With the WEAK bit set, WEAK FINISH works. systems §4.5 adds the column.

### consistency-19. [MINOR] fortress.md / systems.md · fortress §0.4, §9.2; systems §7 income model

**Issue.** Fortress adds 30-bolt payouts for most b0 showpieces and many b2 prizes across 14 stages (up to about 800 bolts) as 'venue-prize-style money'. systems' income model counts only fortress envelopes. systems already flags the economy as possibly too rich.

**Evidence.** fortress §0.4: 'b0 ... 30 bolts (paid once) + a Museum entry'; 'Showpiece and prize bolts (30 per b0) are venue-prize-style money'. systems §7: 'fortress.md may add some' (envelopes only); risk 10 'The economy might be too rich'.

**Recommendation.** Apply the venue cap (≤ 60 per stage) to non-venue stages and add the line to systems §7's income table. The PRIZES save field (above) must cover them, or reuse SECRETS b0/b2.

### consistency-20. [MINOR] tech.md / systems.md · tech §7.7; systems §6.4 item 2, §4.8

**Issue.** LATCHSRC has two meanings. tech writes the shot's weapon slot. systems needs a source column (BUSTER, CHARGE, PUNCH, PUNCH★, FIST, PARRY, the 8 weapons, BREAK, BREAK★, M.BEAM, HAZARD) plus synergy and alt flags, because GP_BOSSHIT's column comes from it.

**Evidence.** tech §7.7: 'writes LATCHSRC,X (WORK $6080) with the shot's weapon slot'. systems §6.4: 'LATCHSRC[victim], the source column for §4 (bits 0-4), plus a synergy flag (bit 7) and an alt flag (bit 6)'.

**Recommendation.** systems' definition is the source of truth. tech derives the column from the attack byte and the shot type at latch time.

### consistency-21. [MINOR] tech.md · §4.4 stage-attribute record; vs fortress §9.1, venues_a §0.1

**Issue.** The 32-byte record is full, and several requested fields are missing:
- the OWNED override (exhibitions);
- the era (F-ERA);
- NO TAG per screen (fortress), where tech has a per-stage bit only;
- a secret-boss screen (venues_a).
PLATE_SCR and FLAGIDX also assume one flag per stage, while venues need a champion flag plus a secret-exit flag.

**Evidence.** fortress §9.1: 'NO TAG per screen, OWNED override (exhibitions), the era (F-ERA), the stage's par'. venues_a §0.1: 'secret-boss screen (the generalised $3F:$F518)'. tech §4.4: '$1A PLATE_SCR', '$1B FLAGIDX | LIVE FILE bit set on the boss kill', 'b4 NO_TAG'.

**Recommendation.** Rename PLATE_SCR to SECRET_SCR: a kill there sets SECRETS b0 and drops the A/B plate. Add a 16-byte per-stage extension record holding the OWNED mask, ERA and a 4-byte NO_TAG screen bitmap.

### consistency-22. [MINOR] fortress.md / story.md · fortress §4.5.2, §4.3.3, §5.2.2; story §5.1, §5.4

**Issue.** The boss-panel text breaks story's panel rules. Fortress uses ':' and '()' (not in the panel glyph set), NAME > 12 and SPECIALTY > 19 characters. Story's 'BREAK MAN?' card also undercuts fortress's 'the panel lies' joke, and the W2 copies are labelled '(SUPER COPY)' in fortress but 'BLIZZARD.EXE' in story.

**Evidence.** story §5.1: 'Glyphs allowed on the panel: 0-9 A-Z . space ... plus - ? ! ' β'; 'SPECIALTY | ≤ 19'; 'NAME | ≤ 12'. fortress §4.5.2: 'SPECIALTY: DEFINITELY BREAK MAN' (20 characters plus ':'), 'DARK MAN MK-VI' (14), 'DISGUISES (BAD)'. fortress §4.3.3: 'DOC ROBOT MK-VI / COPY OF: %CHAMPION% / (YOUR WORST MATCH)'. fortress §5.2.2: 'his boss panel tagged (SUPER COPY)'. story §5.4: 'BREAK MAN? | ... | IMPERSONATION'.

**Recommendation.** story's field rules are binding. Fortress rewrites the panel strings, for example NAME 'BREAKMAN' re-typed as 'DARKMAN', SPECIALTY 'DEFINITELY BLUES' then 'BAD DISGUISES'. Use NAME 'DOCROBOT', SPECIALTY 'COPY OF ' plus the champion, and 'BLIZZARD.EXE' for the W2 copies. Drop the '?' from the in-play card; keep it for ENTRANT FILES only.

### consistency-23. [MINOR] meta.md / systems.md · meta §9.1 TA pause, §9.6 DEV pause item, §3.2 'B: EXHIBITIONS'; systems §12.3 W-tank, §11 'Break Man: SELECT'; vs story §10.1

**Issue.** New labels on vanilla font surfaces use glyphs those fonts lack:
- The pause font has no D, O, Q, Z or '-'. The new pause labels 'QUIT', 'DEBUG' and 'W-TANK' break it.
- The stage-select font has no ':'. 'B: EXHIBITIONS' breaks it.
story's compiler would reject all of these.

**Evidence.** story §10.1: 'Pause menu ... no D, O, Q or Z ... . but no -'; 'Bracket node labels ... 0-9 A-Z . - and blank only: no ! ? ' :'. meta §9.1: 'Pause menu: RETRY ... and QUIT'. meta §9.6: 'the pause-menu DEBUG item'. systems §12.3: 'W-tank | new pause-menu item beside the E-tank'.

**Recommendation.** Use EXIT, TEST, W.TANK and 'B EXHIBITIONS' (or add a ':' tile). Run the per-surface glyph check on meta's and systems' UI strings at M3.

### consistency-24. [MINOR] systems.md / tech.md / art_audio.md · systems §5 item 1, §1.3; tech §7.2 family $FD; art §2.4

**Issue.** The WEAK! pop and the swap flash have two homes. systems makes the pop a single free type id (e.g. $7B) with 5 tiles. tech puts the swap flash, debris and WEAK! pop in family $FD. art builds 'WEAK!' from 3 new tiles plus E and A from READY.

**Evidence.** systems §5: 'A new object type (one of the 32 free ids, e.g. $7B) with 5 sprite tiles, W-E-A-K-!'. tech §7.2: '$FD | effect | swap flash, debris, WEAK! pop'. art §2.4: 'WEAK!: W, K, ! only. E and A are already in READY ... 3 tiles'.

**Recommendation.** Adopt tech's family $FD sub-ids and art's 3-tile GP-COMMON build. systems §5 and SYS-WK-1's '[new-art] 5 tiles' are updated.

### consistency-25. [MINOR] fortress.md / story.md · fortress §0.5; story §6.5, §6.1 P1

**Issue.** The structure of failure lines in fortress stages differs. Fortress gives each H/W stage a 6-line death rotation, 2 wing heckles, and a shared 12-line Mr. Y table with a harmless 'MR. Y PERFORMANCE PARTNERS' YES/NO. story replaces the death line with one heckle per respawn from a 16-line Mr. Y table (H1-H5) and a 12-line Wily table (W1-W3), indexed by the fortress KO count. Its YES/NO costs 1 bolt.

**Evidence.** fortress §0.5: 'On each respawn a line from the stage's 6-line table, then a shared 12-line table ... No mechanical effect'. story §6.5: 'It replaces the venue death line in those stages (EV_RESPAWN_HECKLE, P1)'; 'Mr. Y's respawn insurance! Only 1 bolt!'.

**Recommendation.** Use story's single-P1 rule and tables. Merge fortress's per-wing death and heckle drafts into story's table as wing-tagged variants. Keep one YES/NO: the insurance.

### consistency-26. [MINOR] tech.md / venues_a.md / venues_b.md · tech §11.1, §4.4 EFFECTS b6, Open question 3; venues_a §0.6, §2.8; venues_b §0.4

**Issue.** The default pop-up position conflicts. The venue docs designed for a bottom window; tech defaults to the top. Knight's battle-log position is unresolved.

**Evidence.** venues_a §0.6: 'Cossack (C) and Kalinka (K) pop up in the bottom window'. tech §4.4: 'b6 pop-ups at the bottom (default top)'. venues_a open question 6: 'Where does Knight Man's battle log go'.

**Recommendation.** Default to the top, which keeps pits visible and lets the bottom band carry the palette swap (tech §8.4). Use bottom per stage only where the top band is a raster set piece (Wind 01, Tomahawk 10-11). Knight's battle log uses the same window, with the commentators muted (venues_a already says so).

### consistency-27. [MINOR] fortress.md / tech.md / story.md · fortress §5.3.2; tech §8.1, §8.3; story S38

**Issue.** W3's 16-band perspective floor uses all 16 raster bands, so the compositor would drop the pop-up window band. story writes POP lines into that fight (S38 'MODE 7! The floor ROTATES!' and the K/C replies), and Wily's heckles show on READY there.

**Evidence.** tech §8.1: 'Double-buffered, 16 bands per buffer'; §8.3: 'drops the lowest priority band if more than 16 are asked for'. fortress §5.3.2: 'split into 16 bands of 4 lines'. story S38: '| W | pinch (the Mode 7-style floor starts) | MODE 7! The floor ROTATES!'.

**Recommendation.** Run the floor at 15 bands (or the 8-band fallback) whenever a window is queued, or limit W3 lines to phase transitions and READY. Record the band budget per scene in fortress §5.3.2.

### consistency-28. [MINOR] fortress.md / story.md / systems.md / meta.md · fortress §4.3.5; story Act IV, S11, S29; systems §2.3; meta §3.6 EVENTS2 b4

**Issue.** The docs disagree on when and how the Super Adaptor is handed over.
- Fortress plays the weapon-get 'YOU GET RUSH SUPER ADAPTOR' in H3 screen 12, followed by a demo walk-out that uses Super.
- story says 'Adaptors are never announced on YOU GET' and has Roll fit it on the map after H3; its Act IV says it 'waits under glass in H3'.
- systems sets the bit 'by the H3 clear', which is too late for fortress's screen-12 demo.

**Evidence.** fortress §4.3.5: 'Rush runs in and docks: YOU GET / RUSH SUPER / ADAPTOR (the weapon-get screen, chain $17; FORMS.SUPER ...)'; 'a ledge that needs the jet hop'. story S11: 'Adaptors are never announced on YOU GET'. story §0: 'The Super Adaptor waits under glass in H3'. systems §2.3: 'Super = a save bit set by the H3 clear'.

**Recommendation.** Set FORMS.SUPER when Rush docks in H3 12, without the YOU GET card, following story's rule. S29 becomes Roll's explanation on the map, under EVENTS2 b4. Fix systems §2.3, story's act summary and the art_audio §9.8 'weapon-get cards' line.

### consistency-29. [MINOR] fortress.md / story.md · fortress §1.1 step 5, §1.3 05, §2.5 lockers; story §2.2, §2.3, S06

**Issue.** Entrant numbering conflicts. story makes Rockman entrant 9, Break Man 10 and Bass 'entrant β' (the joke). Fortress's board and lockers make Bass #9 and Rockman 'CHALLENGER', and the intro calls Bass 'a ninth entrant'.

**Evidence.** story §2.3: 'the bracket has ten numbered slots (8 champions, Rockman 9, Break Man 10), so Mr. Y registers him as entrant β'. fortress §1.3 05: 'CHALLENGER: ROCKMAN ... 9 BASS β (SPONSOR: MR. Y) / 10 ??????'. fortress §2.5: '#9 Bass's (dented, KEEP OUT)'.

**Recommendation.** Use story's numbering: board lines '9 ROCKMAN (DR. LIGHT)', '10 ?????? (MASKED)', 'β BASS β (SPONSOR: MR. Y)'; locker 'β'.

### consistency-30. [MINOR] fortress.md / systems.md · fortress §6.3 Player; systems §1.1

**Issue.** In the victory lap 'SELECT swaps who you control', but SELECT is the weapon and form modifier: a tap toggles the last weapon, a hold cycles. The lap gives Rock all weapons and forms.

**Evidence.** fortress §6.3: 'SELECT swaps who you control (CX let you play the partner)'. systems §1.1: 'A SELECT tap toggles the last weapon'.

**Recommendation.** Swap through pause → SELECT (the normal call path), or with controller 2's UP. Keep the SELECT modifier.

### consistency-31. [MINOR] meta.md / fortress.md / art_audio.md / tech.md · meta §9.2.2; fortress §1.3 06, §9.3; art §2.2; tech §4.2

**Issue.** The GP Rush lobby has no single definition:
- fortress: 'the Opening's screen 06', which carries checkpoint 1 and Eddie's 'Pit stop opens after the ceremony!'.
- meta: a one-screen lobby with gift objects, a scoreboard window and a gate.
- art: its own vanilla slot ($2D:$92).
- tech: no stage id at all.

**Evidence.** fortress §9.3: 'The GP Rush lobby is the Opening's screen 06'. meta §9.2.2: 'Gifts ... Eddie ... Roll's HP refill ... Beat ... Break Man'. art_audio §2.2: 'vanilla $2D:$92 (empty) | Players' Tunnel lobby (GP Rush)'.

**Recommendation.** Make the lobby a separate screen in the Opening layout (for example 1D, on TS_STADIUM) with its own object list, entered by the warp to stage $10 screen 1D. Drop art's dedicated slot.

### consistency-32. [MINOR] venues_b.md · §4.6.1, §4.5.3, §5.2 tiers

**Issue.** The Yamato secret exit (Must) needs PASS #3, which only drops when the Daruma (Should) is beaten.

**Evidence.** venues_b §4.6.1: '#3 under the Daruma (11)'. venues_b §4.5.3: 'The Daruma (11) [new-code M · Should] (T8)'. venues_b §5.2: 'Must ... passes + sekisho'.

**Recommendation.** State the fallback: if the Daruma is cut, PASS #3 sits on a pedestal at 11, guarded by two ashigaru.

### consistency-33. [MINOR] venues_b.md · §0.4 T6, §0.5, boss rows §1.8/§2.8/§3.8/§4.8, §4.5.2, §4.6.3, §6 lessons

**Issue.** venues_b still states proposals that systems and tech have overridden:
- weakness '4 / 8' and different G/R grades (Blizzard: C.FLASH 1/40 here, but systems has C.FLASH 2/30 and W.STORM resisted);
- Y.SPEAR as a '3-spear volley';
- C.FLASH Power as '×3 punch damage during a time stop';
- DARUMA 'once per stage' (systems: once per life, 2 slots);
- T6 as a WRAM bitmap (tech: variant blocks);
- pogo bounce heights of 51/72 px vs systems' vy values;
- Flame's ABSORB heals 1, while SC4 says the first own-weapon hit does 0.

**Evidence.** venues_b §1.8: 'F.BLAST 4 / 8 (weakness) ... C.FLASH 1 / 40'. systems §4.6 SC9: 'Venue proposals of 8 f weakness i-frames (venues_b) are overridden by the 16 f of Table 2'. systems Table 1, Blizzard: 'W.STORM 1 R', 'C.FLASH 2'. venues_b §4.6.3: 'once per stage, a hit that would kill you ...'. systems §9.2 #20: 'Once per life ... 2 slots'. venues_b §2.8: 'the first F.BLAST hit heals him 1'.

**Recommendation.** Mark venues_b §0.5 and every 'Proposed row' as superseded by systems §3 and §4, and keep only the reactions. Allow ABSORB's heal as a named SC4 exception (as SC3 does for Plant). Point §0.4 T6 at tech §10.

### consistency-34. [MINOR] venues_a.md · §4.7.4, §3.7 'Moral flavour'

**Issue.** Two venues_a proposals have been overruled elsewhere but remain in its text: Plant's YOU GET adding 'AND RUSH JET ADAPTOR' on the 4th win, and an Eddie-shooting moral trade-off.

**Evidence.** venues_a §4.7.4: 'that line is only shown when this is the 4th win, per systems.md'. story S11: 'Adaptors are never announced on YOU GET'. venues_a §3.7: 'shooting Eddie drops a big bolt sack but closes the shop's discount tier'. story §2.8: 'Eddie is never the butt of a moral joke here'. systems §9.4: doping is the trade-off.

**Recommendation.** Delete both proposals from venues_a.

### consistency-35. [MINOR] systems.md · §4.6 SC1; vs venues_a §2.8.3, story KNT-08

**Issue.** The question 'Y.SPEAR pierces Knight Man's shield' has no answer from systems. venues_a's Must weakness reaction depends on it, and story already wrote the line.

**Evidence.** systems SC1: 'Frontal shots reflect, except PUNCH★, Morning Star, Time Fist, PARRY reflections, BREAK★ and C.FLASH'. venues_a §2.8.3: 'needs Y.SPEAR added to SC1's pass-through list'. story KNT-08: 'Right through the shield!'.

**Recommendation.** Add Y.SPEAR to SC1's pass-through list (it pierces but does not break the shield).

### consistency-36. [MINOR] systems.md · §2.4 normal-route rule; vs venues_a §0.3, fortress §0.2/§3.0

**Issue.** The lent Jet (Wind's sortie and 1D, the E3/E4 loaners) is not covered by systems' rule that 'normal routes never need a form'. venues_a asks twice for a ruling; story has approved the 'RENTAL' bib.

**Evidence.** systems §2.4: 'A normal exit never needs a form, an alt fire, a synergy or Break Man.' venues_a open question 11: 'does systems.md agree that this satisfies the rule?'. fortress §0.2: 'Exhibitions lend their vehicles ("COMMITTEE LOANER JET")'.

**Recommendation.** Add to §2.4: 'A stage-lent vehicle state (SKY ACE, loaner Jet, MAZE or CANNON mode) is not a form; it is NO TAG, works under 1993 rules, and gives no form-based VARIETY.'

### consistency-37. [MINOR] meta.md / systems.md / tech.md · meta §1.6 WEAPONS, §9.2.5 WEAPONS A, §9.6 WPN; systems §1.1, §3; tech §4.3 D SA.YOUGET

**Issue.** Two weapon orders are used without a mapping. meta's bits run by venue id (B.ATTACK, W.STORM, PLANT.B, ...). systems' slots run in vanilla menu order (Y.SPEAR slot 1 ... C.FLASH slot 8).

**Evidence.** meta §1.6: '$030 b0-7 = the 8 champion weapons by venue id'. systems §1.1: 'BUSTER, Y.SPEAR, W.STORM, ... This is the vanilla menu order, $0688-$0691'.

**Recommendation.** systems publishes one table, venue id → weapon slot (vanilla $F704, relocated). meta, tech and EXTRA CONFIG cite it.

### consistency-38. [MINOR] systems.md / meta.md / fortress.md · systems §11, §6.1 OWNED; meta §10 TOURNAMENT HISTORIAN; fortress Semifinal b1, H5 b2, W2 b1

**Issue.** Doping has an undocumented side effect. With TURBO owned Break Man can never be called, so three fortress secrets (all requiring TAG) become impossible. That caps SECRETS on three stages and blocks TOURNAMENT HISTORIAN. OWNED also still counts BREAK 'once he has joined'.

**Evidence.** systems §11: 'Not allowed ... while TURBO is owned'. systems §6.1: 'OWNED ... BREAK once he has joined'. fortress §9.3: 'require values used: TAG (Semifinal b1, H5 b2, W2 b1)'. meta §10: 'TOURNAMENT HISTORIAN | Every SECRETS bit the 22 stages define'.

**Recommendation.** Keep it as part of the cost, but say so: meta's RECORDS notes 'TAG secrets void (TURBO)', and OWNED excludes BREAK when RATEFLAGS.DOPED is set.

### consistency-39. [MINOR] systems.md · §13.3 1993 rules

**Issue.** The 1993 row set is 'generated from vanilla' tables, but most GP bosses (Bass β, the MK-VIs, the guests, METALL 16, Pi-kun, the mid-bosses) have no vanilla rows. Whether SC5 and SC6 run under 1993 rules is unstated. Without SC5's fist rule there is no way to hurt Gamma's cockpit.

**Evidence.** systems §13.3: 'A "1993" row set is generated from $31:$9A45 and $3F:$EFE4: 60 f / 32 f everywhere, the punch 2 on Robot Masters.'

**Recommendation.** Under 1993, GP bosses use their family defaults at vanilla i-frames (machines 32 f with the full punch at 4; robots 60 f with the weakness at 4). SC5 stays on; SC6 and COUNTER are off.

### consistency-40. [MINOR] art_audio.md / story.md / tech.md · art §9.4 portraits and icons; story §6.1 speakers, §12; tech Open question 6

**Issue.** The speaker lists differ. art's 6 face icons omit Wily and Light, both POP speakers in story, and include Eddie, who never speaks in POPs. art's 12 portraits include Beat but not Mr. X (Could in story).

**Evidence.** art §9.4: 'Cossack, Kalinka, Mr. Y, Break Man, Roll, Eddie = 24 tiles'. story §6.1: 'Speakers and icons ... Cossack, Kalinka, Mr. Y, Wily, Roll, Break Man (the visor), Light (radio static frame)'.

**Recommendation.** Icons: story's 7 (Light as the radio frame). Portraits: art's 12, plus Mr. X as Could.

### consistency-41. [MINOR] tech.md · §11.2 hook address, §12.4 bank count, D3

**Issue.** tech has small internal and cross-doc errors:
- The language hook is at $3C:$8636 in tech but at $3C:$8631 in meta and story.
- '16 banks (128 KB) are reserved ($70-$77 + the $0B-$0F pool)' is 13 banks.
- D3 says '$80-$87 is PRG-RAM page 0-7', but only 4 pages exist.

**Evidence.** tech §11.2: 'One hook in the interpreter at $3C:$8636'. meta §11.1: 'the one hook at $3C:$8631'. tech §12.4: '16 banks (128 KB) are reserved ($70-$77 + the $0B-$0F pool)'.

**Recommendation.** tech is the source of truth for addresses; meta and story cite $8636, the point where the pointer is read. Fix the bank arithmetic and D3's page range.

### consistency-42. [MINOR] meta.md / venues_a.md / venues_b.md / story.md · meta §4.3-4.4; venues_b title; story §1.2 rule 5, §5.1; venues_a risk 9

**Issue.** The on-screen venue titles are inconsistent and some carry third-party marks. meta and venues_b show 'PRINCE OF PERSIA PALACE' (23 characters, over the 20-character VENUE field); story proposes 'PERSIAN PALACE'. 'DRAGON QUESTLIKE' and 'JUNGLE PITFALL' carry other publishers' marks, against BRIEF §6 'parody names'. venues_a asks meta to rule.

**Evidence.** meta §4.3: 'Flame: PRINCE OF PERSIA PALACE'. story §5.1: 'PERSIAN PALACE for every on-screen use'. venues_a risk 9: 'meta.md should rule on the final on-screen titles'.

**Recommendation.** See the venue-titles decision below. Adopt story's rule for on-screen titles: Capcom-owned marks are allowed (1943, Gun.Smoke), third-party marks are not. Use PERSIAN PALACE, plus parodies for Knight and Plant.

### consistency-43. [MINOR] art_audio.md / venues_a.md / venues_b.md · art §2.4, §15; venues_a §4.3 OBJ_VINE; venues_b §1.3 screen 17

**Issue.** art_audio sets a buster-only rule on vines and while carried by the condor, because those poses share the buster's 15-tile weapon slot. The venue docs do not carry the rule: the Plant vine says 'B fires toward the swing's direction' and the condor carry says 'you can shoot'.

**Evidence.** art §15: 'while hanging on a vine (Plant) or carried by the condor (Blizzard) only the buster fires'. venues_a §4.3: 'B fires toward the swing's direction'.

**Recommendation.** The venue docs adopt the buster-only rule and state it in the vine and condor specs, with the weapon switching to the buster on grab.

### consistency-44. [MINOR] meta.md / venues_a.md / venues_b.md · meta §9.2.1 ids $08-$17, §15; fortress §9.3

**Issue.** The venue mid-boss fight ids ($08-$12, after fortress took $13-$17) were requested but never assigned. ENTRANT FILES, MY GP and the Doc Robot copy logic all need them.

**Evidence.** meta §15: 'Mid-boss fight ids $08-$17 with arena screens (CONGA, AYACO, the Daruma, …)'. fortress §9.3: '$13-$17 for this doc's five mid-bosses ... leaving $08-$12 to the venues'. Neither venue doc assigns ids.

**Recommendation.** meta assigns them:
- $08 AYACO
- $09 METAL METSLIME
- $0A DOMINGO DOME
- $0B SIX-SHOT SAM
- $0C SIDEWINDER
- $0D CONGA
- $0E SHADOW ROCK
- $0F GAMARN & GAMADAYU
- $10 DARUMA
- $11-$12 spare
Each comes with its arena screen from the venue docs.

## Decisions needed (42)

1. **Stage-id map: tech §4.2 (legacy 8-15 kept, H/W at $16-$1D) or fortress §0.1 (H/W reuse 8-15)?**
   - Options: A) tech's map. B) fortress's map, which needs extra ids for vanilla Wily 4 and Mr. X 1.
   - Recommended: A. tech's map. It keeps the legacy arenas for $27, the 1993 CUP and Mr. X Returns, and M2.1 rewrites the $51 readers anyway.
   - Affects: tech §4.2, fortress §0.1/§9.1, meta §9.2.1 fight records

2. **SUPER era in W1-W3: ExGrafix (fortress), a W1-only Could spike (art), or no ExGrafix in scrolling stages (tech D6)?**
   - Options: A) No ExGrafix in play; SUPER = palettes + raster bands + MMC5 audio. B) ExGrafix on non-scrolling, text-free screens only. C) Full ExGrafix, which needs ExRAM mode switching and drops text windows.
   - Recommended: A, plus B for the static 'SUPER WILY CASTLE' picture (Could).
   - Affects: fortress §5.0-§5.4, §4.6; art §2.7; tech D6/D7

3. **Text rendering model and window sizes.**
   - Options: A) Per-page glyph cache with 8-px cells (story/art) in tech's ExRAM window. B) tech's VWF canvas (2×16 pop-up, 3×26 dialogue).
   - Recommended: A. POP 2×28 (≤ 24 glyphs + a 4-tile face icon in BG), SCN and debrief 4×28, help 3×28, plaques 9×28.
   - Affects: tech §11, story §10, art §9.6, meta §4.1

4. **EN letter case (story OQ3 / art §3.5).**
   - Options: A) ALL CAPS. B) Mixed case.
   - Recommended: A, ALL CAPS: vanilla house style and fewer glyphs per page. art drops the lowercase set.
   - Affects: art §3.5/§9.6, story §10.3, tech §11.4

5. **JP kanji (tech OQ8).**
   - Options: A) Kana only. B) A small kanji set (~1.6 KB).
   - Recommended: A, kana only, as vanilla. The logo's 史上最大のグランプリ stays art.
   - Affects: tech §11.4, story §10.3

6. **Text bank allocation.**
   - Options: A) 10-12 banks. B) Keep 4 banks and cut text.
   - Recommended: A, taken from the $7D reserve, the $0B-$0F pool and the spare music reserve.
   - Affects: tech §1.2, story §10.4

7. **Form swap with a 2 KB sheet (systems OQ2 / art §1.5).**
   - Options: A) Stream the full sheet at 256 B/frame, keep the old tiles visible, cooldown = until the stream completes. B) Re-pack the sheets so they share tiles. C) 32 KB CHR-RAM.
   - Recommended: A (C is ruled out by tech D6). Make the unrolled copier Must.
   - Affects: systems §1.3, tech §15.3, art §2.6

8. **Who owns the late-game beats where story and fortress disagree?**
   - Options: A) fortress owns staging, mechanics and order; story owns words. B) story owns the beats and fortress changes its mechanics.
   - Recommended: A. story re-syncs S17-S45 to fortress v1: GP Cup from the Trophy Dispenser; two-mask unmasking in H5; W1 boss METALL 16; W3 machine carded 'WILY MACHINE 6.5' with ENERGY 'PROJECT SUPER'; Rush catch and Break Man at the door; Wily caged in the lap; fortress's ending order.
   - Affects: story §3-§5, fortress §4.6-§6

9. **CAPCOM TIMES: reprint vanilla's $94 jailbreak line or not?**
   - Options: A) Drop $94 (story: S02 already quotes it and page 2 answers it). B) Keep $94 verbatim (fortress).
   - Recommended: A, story's words. fortress §9.4's 'beats to keep' list is updated.
   - Affects: story S44, fortress §6.1 scene 6

10. **Doped CAPCOM TIMES headline and Mr. X card text: which wording?**
   - Options: Headline: 'UNDER REVIEW' (story) or 'UNDER INVESTIGATION' (systems, fortress). Card: story's or fortress's text.
   - Recommended: story's wording for both, as story owns words. systems §9.4 and fortress §4.5.3/§6.1 cite it.
   - Affects: systems §9.4, fortress §4.5.3/§6.1, story S28/S44

11. **Break Man's join point.**
   - Options: A) Reveal in-stage at Semifinal 0E; join on the bracket via Rule 9 (story S20, EVENTS b5). B) Join in-stage at 0E (fortress).
   - Recommended: A. FORMS.TAG is set by the bracket event; fortress drops the 0E banner.
   - Affects: fortress §2.6, story S18-S20, meta §3.6

12. **Semifinal crowd: rejected entrants (fortress) or Sniper Joes in Bass scarves (story)?**
   - Options: A) Rejects. B) Sniper Joes.
   - Recommended: A, the rejects. They are mechanics: the audition rule and TALENT SCOUT. story rewrites S17-S18 and the Semifinal death lines.
   - Affects: story S17-S19, §6.4

13. **Entrant numbering (story OQ1).**
   - Options: A) Champions 1-8, Rockman 9, Break Man 10, Bass 'entrant β'. B) Bass as #9.
   - Recommended: A. fortress updates the entrant board and lockers.
   - Affects: fortress §1.1, §1.3, §2.5; story §2

14. **When does the Pit Stop open?**
   - Options: A) After the Opening (0 wins). B) After the first venue match.
   - Recommended: A, matching systems §8 ('start' stock) and meta §3.2. story S04's sign is changed.
   - Affects: story S04, fortress §1.3 06

15. **Super Adaptor handover.**
   - Options: A) FORMS.SUPER is set when Rush docks in H3 12, with no YOU GET card; Roll's map scene follows. B) A YOU GET card in the stage. C) Set at the H3 clear only, which breaks the demo walk-out.
   - Recommended: A.
   - Affects: fortress §4.3.5, story S11/S29, systems §2.3, meta EVENTS2 b4

16. **Fortress main-route rule vs Gamma SC5 (and fortress OQ4: lend Super to Gamma?).**
   - Options: A) Allow the Power punch as the one required form, at Gamma phase 2, with its plaque. B) Lend Super during phase 2. C) Give the cockpit a non-fist route.
   - Recommended: A. No lending.
   - Affects: fortress §0.2/§4.3.4, systems §2.4/§13.3

17. **Is a stage-lent vehicle acceptable under 'normal routes never need a form' (venues_a OQ2/OQ11)?**
   - Options: Yes, as a defined vehicle state / No (use a Committee glider).
   - Recommended: Yes. Add the vehicle-state clause to systems §2.4: NO TAG, allowed under 1993, the RENTAL bib.
   - Affects: systems §2.4, venues_a §1, fortress §3

18. **Y.SPEAR in SC1's shield pass-through list (venues_a OQ3).**
   - Options: Yes / No.
   - Recommended: Yes: it pierces without breaking the shield. Story's KNT-08 already assumes it.
   - Affects: systems SC1, venues_a §2.8.3

19. **Exhibition rule damage column.**
   - Options: A) A new RULE column (4/12, WEAK bit, class 4 for VARIETY). B) Reuse HAZARD with non-zero guest cells.
   - Recommended: A.
   - Affects: systems §4.5, fortress §3.0/§8

20. **Exhibition rewards and colours (systems OQ9, fortress OQ6).**
   - Options: Chips or fixed prizes; 4 exclusive racing colours yes or no.
   - Recommended: Fixed prizes (100 bolts, a colour, a trophy); chips stay at 21. Yes to the 4 exclusive colours (Could, with RACING COLOURS).
   - Affects: systems §7/§8, fortress §3.0, meta T3

21. **Venue prize economy.**
   - Options: A) systems' cap: ≤ 60 per stage (venue and non-venue) and the 30-bolt envelope in every hidden room. B) Raise the caps and re-price the shop.
   - Recommended: A. venues_b replaces its bags and chest with envelopes and re-prices the vegetables. fortress payouts count against the cap.
   - Affects: venues_b, fortress §0.4, systems §7, meta FILE (PRIZES field)

22. **Tileset slot architecture.**
   - Options: A) tech's RAM image (independent alternate set per slot), 3 slots per ROM bank, fortress's shared slots (about 26 slots in 9-10 banks). B) art's 10-bank / 30-slot plan with shared alternate sets. C) venues_b's one bank per venue.
   - Recommended: A.
   - Affects: tech §1.2/§5.2, art §2.2, fortress §0.1, venues_b §0.2

23. **Grand Pi-kun build: BG boss with 3 streamed sizes (fortress) or a 70-tile sprite (art)?**
   - Options: A) fortress's BG boss with F-SIZES (one-size fallback). B) art's sprite.
   - Recommended: A, as fortress owns bosses. art re-budgets about 150 BG tiles.
   - Affects: art §5/§7.2, fortress §1.6

24. **Hall of Fame music concept (art OQ5 vs fortress §0.1).**
   - Options: A) G08-G12: an arrangement of each RM1-5 fortress theme (art). B) One GP 'HALL OF FAME' theme in 5 era arrangements (fortress). C) Originals in each game's style.
   - Recommended: A, Should, with $09 as the fallback. Capcom's own music, re-sequenced, as art and story assume.
   - Affects: art §12.3/§12.5, fortress §0.1/§9.6

25. **Ending lights-out: channel order and MMC5.**
   - Options: A) MMC5 voices drop first (if on), then noise, triangle, pulse 2, pulse 1; no DPCM. B) story's version (MMC5 gone earlier, DPCM first).
   - Recommended: A. Add G37 LAST MATCH (Must) to art_audio.
   - Affects: art §12, story S42, fortress §6.1 scene 7

26. **Failure lines in fortress stages.**
   - Options: A) story's one P1 heckle per respawn (it replaces the death line), with fortress's wing lines merged in. B) fortress's death line plus a heckle.
   - Recommended: A.
   - Affects: fortress §0.5 and per-wing hooks, story §6.5

27. **Mr. Y's 1-bolt respawn insurance (story OQ7).**
   - Options: Deduct a bolt / pretend.
   - Recommended: Deduct 1 bolt, never below 0: CX's 'Yes that hurts' at harmless scale. It replaces fortress's commercial YES/NO.
   - Affects: story §6.5, fortress §0.5

28. **Pop-up default position (tech OQ3) and Knight's battle log (venues_a OQ6).**
   - Options: Top / bottom.
   - Recommended: Top by default, bottom per stage where the top band is a raster set piece. The battle log uses the pop-up window, with the commentators muted.
   - Affects: tech §11, venues_a §0.6/§2.8, venues_b

29. **Face icon in boss rooms.**
   - Options: A) A 4-tile BG icon inside the glyph strip. B) One generic sprite icon in GP-COMMON. C) No icon in boss rooms.
   - Recommended: A.
   - Affects: art §9.4, tech §11.4, story §6.1

30. **Victory-lap character swap.**
   - Options: Pause → SELECT / SELECT tap / controller 2 UP.
   - Recommended: Pause → SELECT (the call path); keep the SELECT modifier.
   - Affects: fortress §6.3, systems §1.1

31. **If the tag partner (Should) is cut, where does the doping cost go (meta OQ8, story risk 7)?**
   - Options: A) FAIR PLAY (meta: T12 = no unplugs and no TURBO), with the asterisk and headline as flavour. B) The asterisk only.
   - Recommended: A, with meta re-checking the 102→100 arithmetic.
   - Affects: meta §6.3, story S21

32. **TURBO permanent and/or inert in Super Wily Castle (systems OQ7, story proposal).**
   - Options: Permanent / returnable; inert in W1-W3 yes or no.
   - Recommended: Permanent (meta's arithmetic and BREAK MAN WALKS rely on it). Inert in W1-W3 accepted as a Could; story's 'WARRANTY VOID' and Wily line 4 depend on it.
   - Affects: systems §9.4, story §6.5/§8

33. **DARUMA hidden function (twice per life after 7 KOs, story §8).**
   - Options: Accept / reject.
   - Recommended: Reject. Keep systems' once per life at 2 slots and keep the proverb page wording without the 'count your falls' hint.
   - Affects: systems §9.2 #20, story §8

34. **meta's open questions 1-7.**
   - Options: Each yes or no.
   - Recommended: 
- POSTPONED lock (not a forced Semifinal).
- RETIRE is free.
- Kalinka speaks the debrief.
- No tag call in Time Attack.
- Unlocks are global.
- KNOCKOUT seed: user-visible and enterable (the NES has no clock, so 'daily' is impossible).
- 1993 files may earn unlocks.
   - Affects: meta §17

35. **systems' remaining open questions.**
   - Options: Each.
   - Recommended: 
- OQ1: make oil ignition by F.BLAST explicit GP behaviour through the $3E:$DDFC hook, whatever vanilla does.
- OQ5: measure the Plant Barrier at M3.
- OQ6: VARIETY counts boss hits.
- OQ8: keep the free retreat.
- OQ10: Mr. X 1 riders only matter for Mr. X Returns (Could); give them an explicit GP_BOSSHIT row.
- OQ11: criticals stay Could, with KAISHIN's fallback.
- OQ12: keep the ★ as a Could.
   - Affects: systems §15/OQ

36. **art_audio's remaining open questions.**
   - Options: Each.
   - Recommended: 
- 32 KB CHR-RAM: no (tech D6).
- $C000 is switchable (the C-window), but DPCM is Won't for v1 because it would contend with the C-window.
- Recruiting an artist and composer is the user's call; plan placeholders.
- Deferred pop-ups: accepted, except P1 lines (shown on READY) and EV_WEAK_FIRST (BG icon).
- $0F stays the bracket theme.
- The enemy-area placements are accepted by the venue docs.
- MMC5 AUDIO defaults to ON (every track is complete on the 4 base channels).
   - Affects: art §18

37. **tech's remaining open questions.**
   - Options: Each.
   - Recommended: 
- LIVE images move to page 1: yes.
- No stage exceeds 32 screens (fortress ≤ 26, venues ≤ 32), so sections stay Should.
- No venue needs T1-full.
- Legacy ids keep vanilla fortress rules unless a fight record overrides them through RULESET.
- Headless Mesen and the hardware target are user questions.
   - Affects: tech OQ

38. **venues_b's open questions.**
   - Options: Each.
   - Recommended: 
- The weakness cycle is kept.
- Plates are pickups.
- Replays for the other exit are allowed (meta removes the beam-out).
- A secret-arena win awards the weapon.
- Behaviour chips are unique.
- Tag shortcuts are Could; Break Man is callable in boss rooms after the bar fill except where NO TAG.
- CASUAL levers go through the CASUAL layout tier.
- X-UPEXIT is Should, with ladder stubs as the fallback.
   - Affects: venues_b §8

39. **venues_a's remaining open questions.**
   - Options: Each.
   - Recommended: 
- T1-lite is accepted.
- Keys use T3's per-stage key counter.
- Roll as the princess and Tango as the cat are approved (story).
- The music budget is within art's one cue per venue.
- The Plant canopy redraw stays (no extra BG ids are coming).
- Plant's group 1 leaves $F deadly (only 5/D/E are remapped).
- Secret arenas stay Should, with fallbacks.
   - Affects: venues_a §10

40. **fortress's remaining open questions.**
   - Options: Each.
   - Recommended: 
- A doped file gets Roll as the lap partner.
- If W1 is cut, the era idea lives in the escape.
- The Hall of Fame stays linear.
- The ??? fight runs as a one-fight 1993 RULESET switch.
- Keep Block Man (story writes the joke in).
- Doc Robot copies the worst STAGEREC venue.
- Keep the 32-bit room.
   - Affects: fortress OQ

41. **story's remaining open questions.**
   - Options: Each.
   - Recommended: 
- PERSIAN PALACE: yes.
- Light says 'Albert' in EN and アルバート once in JP.
- The CX author's kana: the user confirms; keep Latin until then.
- Generate ALL ENTRANTS from the object families' name fields at build time.
   - Affects: story OQ

42. **On-screen venue titles and trademarks.**
   - Options: A) Capcom-owned marks allowed (SKY ACE 1943, GUN.SMOKE FRONTIER); third-party marks replaced (PERSIAN PALACE; parodies for DRAGON QUESTLIKE and JUNGLE PITFALL). B) Keep the working titles.
   - Recommended: A, with meta publishing the final ≤ 20-character list.
   - Affects: meta §4.3-4.4, story §5.2, venues_a, venues_b
