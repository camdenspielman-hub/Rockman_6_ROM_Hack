
# critic-design

## Verdict

The design clears the 'how crazy it gets' bar almost everywhere: each venue's homage is a mechanic and every boss has a screenshot moment. Telegraphing is a real strength. Its problems are about volume and coherence, not a lack of ideas. Story and fortress disagree on the ending, on Break Man's gag and join point, and on the Opening, and the ending buries its farewell under gags. Set pieces repeat heavily across the 22 stages (four spike ceilings, five or more dark rooms, six copy bosses, seven full-charge hidden rooms). The systems layer is heavier than 4MI's: 24 weapon behaviours, 21 chips, crafting, and a post-game with 7 modes. CASUAL and 1993 are not coherent across the docs. Third-party trademarks still reach the screen. The Tomahawk and Flame venues still carry cheap-to-fix cultural framing problems. There are no blockers. Thirteen majors need director rulings, chiefly: one ending owned by story.md, the 'respect the disguise' rule for Break Man, the cut list, and a CASUAL framework. After those, the game would be tighter and more memorable.

## Strengths

- Every venue turns its homage into rules, not costumes: 1943's POW cycling and loops, Dragon Quest's command windows and stairs behind the throne, Wild Gunman's timer, Pitfall's 3-for-1 underground, Ice Climber's head-bonk with seals patching the holes, Prince of Persia's shadow merge, Atlantis's lying doors and the tide used as a lift and a lock. This meets CX lesson 2.
- Vanilla set pieces each get one sharp twist: the spike ceiling has HP, the icebreaker shakes icicles loose, igniting oil becomes a permanent choice, the tide becomes a lift and a lock, and the Mr. X reveal becomes a two-mask unmasking.
- Secrets are telegraphed consistently, with named tells, tier A/B debrief escalation and requirement hints that never hide a hint you can use now (CX lesson 6, 4MI lesson 5).
- Every champion has a WEAK reaction, an own-weapon joke and a themed pinch (the slot-reel ABILITY UNKNOWN, HELMET OFF / MOBILE 99, an interruptible HEALMORE, the snowman). The fortress bosses reach CX's bar: Dark Man's lying boss panel, riding Gamma's fist to punch Mr. Y, METALL 16 upgrading its era between bars, and the Mode-7 floor.
- The farewell-to-8-bit layer (lights going out one channel at a time, Wily Machine 6.5, the sixth wing for the game you are playing) gives the hack an emotional spine that neither reference had.
- The combat model keeps vanilla's buster feel while making every weapon worth using, and the economy cannot be farmed (replays pay only the improvement, and no bolts drop from enemies).
- The story's tone rules and its fact appendix with sources are unusually careful, including the cultural rules and the ban on shipping WIP text.

## Findings (25: blocker 0, major 13, minor 12)

### design-1. [MAJOR] story.md, fortress.md · fortress §5.3.3, §5.4 (0C), §6.1; story S39-S48

**Issue.** The ending exists in two incompatible versions, and both bury the emotional climax under gags. Wily's fate, Break Man's exit, the scene order, the channel drop order and the newspaper text all differ between the two docs.

**Evidence.** Wily: fortress §5.3.3 has him jump into a pod ('PSYCH!') and §6.1 scene 2 has the pod crash on the pitch with Rock holding his collar. Story S39-S40 has him kneeling, then Break Man carrying Rock AND Wily out ('This time.'). Break Man ends up in three places: holding the door at escape 0C ('Go! I'll be right behind you'), on the stadium roof (fortress §6.1 scene 5), and carrying Rock out (story S40). Order: fortress runs podium → CAPCOM TIMES → lights out → 'the scoreboard flickers back on: VICTORY LAP'; story runs S42 lights out → S43 sixth wing → S44 newspaper → S45 lap → S46 rating. Channels: fortress drops MMC5 p2, then p1, then the 2A03 channels, while story S42 says the MMC5 pulses 'were already silenced when the castle fell'. Newspaper: fortress reprints vanilla $94 verbatim; S44 says $94 'is not reprinted'. The 'It was all Mr. Y's idea' / 'YOU are Mr. Y' gag appears in both fortress scene 2 and story S39. In both orders the quiet farewell is followed by Wily caged on a float, Rush and Beat pinning him, and 'Mr. Z'.

**Recommendation.** Make story.md the single owner of the ending and use this order: escape → castle pixelates → Break Man catches Rock and Wily (S40, the strongest Break Man beat) → arrest with one use of the Mr. Y/Mr. Z gag → podium and Bass's vow → CAPCOM TIMES (drop $94, since S02 already quotes it) → victory lap → rating and Break Man's debrief → LIGHTS OUT (S42) → sixth-wing plaque (S43) → TO BE CONTINUED. The last thing the player hears should be pulse 1 alone, not a gag. Delete the door-holding and roof variants from fortress.md and adopt story's channel order.

### design-2. [MAJOR] fortress.md, story.md · fortress §1.3 (05), §2.4-2.6, §4.5, §5.3.3 hooks; story §1.3, S06, S08, S17-S20

**Issue.** Break Man's running gag and his introduction contradict each other. Fortress has everyone shout 'OBVIOUSLY Blues', which turns him into a second copy of the Mr. Y joke. Story's rule is the opposite: everyone politely respects his disguise. The two docs also disagree on when he is introduced and when he joins, on Bass's entrant number, and on who the Semifinal crowd is.

**Evidence.** Story §1.3: 'everyone politely plays along... Rock says Blues? exactly twice; Light never says the name until the very last scene.' Fortress §2.6 0E: C 'That's Blues.' K 'That's OBVIOUSLY Blues.'; §5.3.3: 'Is that... Blues?' 'OBVIOUSLY Blues.'; H5 hooks: 'Obviously not Blues.' Introduction: story S06 introduces him by name in the Opening, and in S08 he teaches the charge. Fortress Opening shows '10 ?????? (MASKED)' with 'No... Break Man', and at the Semifinal Bass asks 'Who are YOU supposed to be?'. Join: story S20 (on the bracket, Rule 9) vs fortress 0E banner 'BREAK MAN JOINS!'. Numbering: the fortress board reads '9 BASS β' and 'CHALLENGER: ROCKMAN'; story makes Rockman 9 and Bass 'entrant β'. Crowd: story S17-S18 has Sniper Joes in Bass scarves and Break Man 'holds the crowd'; fortress has rejected entrants and has Break Man break a rubble wall at 06.

**Recommendation.** Adopt story's rule: the good-side gag is that the disguise is respected, which keeps it distinct from Mr. Y's. Remove every 'OBVIOUSLY Blues' line from fortress.md. Use story's numbering. Use one join point: play S20's Rule 9 lines in place at Semifinal 0E, where the TAG banner has context. In the Opening, keep the masked board line and S06's roll call, let the high striker teach the charge, and play Break Man's whistle tip only after a death to Pi-kun. Make the crowd the fortress's rejects, because they are mechanics, and rewrite S17/S18 to match.

### design-3. [MAJOR] fortress.md · §0.2, §4.3.4; systems.md §2.4

**Issue.** The fortress's own rule ('only M.BEAM is ever required') is broken by a Must boss. Gamma's phase 2 can only be damaged by fists, so the Power form is required on H3's main route.

**Evidence.** §0.2: 'the buster's full charge..., the Magnet Beam..., and nothing else. Every punch, form... is on optional content. There is exactly one such gate in the whole fortress: H1 0B.' But §4.3.4 says 'SC5: only fists hurt the cockpit (tap punch, PUNCH★, Time Fist, Morning Star, the Super fist on replays; everything else dinks)', with the cockpit 120 px up, reached by riding a fist. The skill route ('Jet up, then swap to Power') needs the quick swap, which 1993 removes (systems §13.3).

**Recommendation.** Keep the fists-only joke, which is the best boss idea in the Hall of Fame, and amend the rule instead: 'POWER (owned from the 2nd win) may be required in the fortress, with a tell.' The plaque at 10 already supplies the tell. Add a no-risk fist-ride practice before the fight (screen 10, with a resting fist prop). State SC5's 1993 behaviour explicitly.

### design-4. [MAJOR] story.md, fortress.md · story S02-S08; fortress §1.1, §1.3-1.4

**Issue.** The Opening Ceremony is a wall of text, which contradicts its own pitch ('teaches by being the event, not by stopping the game'). It has two different intros, a 14-page rules lecture and duplicated roll calls, and repeats the same Wily gag three times in five minutes.

**Evidence.** Text before the first bracket: an intro (fortress §1.1, 6 steps, about 55 s; story S02 is a different 7-panel crawl covering the same beats), S03 (3 pages), S04 (4), S05 (16 POPs: 8 champions × 2), S06 (9), S07 (14 rows, although the text says '11 pages'), S08 (7), plus the chairman's speech and the lane judges' cards. That is about 60 pages. The parade appears twice: fortress §1.4 has each champion speak one line from his float, and S05 has two more pages per podium. 'It's definitely Wily' appears in fortress §1.1 step 6, S02 panel 6 and S07 page 11.

**Recommendation.** Cap the Opening at about 15 SCN pages. Use one intro: story's S02 as the attract crawl, with NEW GAME going straight to the tunnel. Fold S07 into the lanes: each lane judge announces his own scorecard row, and the scoreboard at 05 shows VARIETY and SECRETS. Make the roll call the float lines only, one line each. Keep S06 and Pi-kun's sabotage. Play the Wily gag once per act and vary its wording.

### design-5. [MAJOR] venues_a.md, venues_b.md, fortress.md · many (listed in evidence)

**Issue.** Many set pieces and secret patterns are reused across the game, so the 22 stages blur together. The most common pattern for a non-venue secret is 'hit the odd-looking thing with a full charge'.

**Evidence.** (a) Knight's IRQ spike ceiling is used 4 times: Knight Trap Hall, Yamato nightingale floor, H4 compactor 09-0D, escape 0A. (b) Dark rooms or lights on a timer, 5+: Knight basement, Yamato dark room, Centaur black zone, Semifinal BLACKOUT 04/08, H4 Bright Man 03-05. (c) Wrap-around vertical towers twice: Blizzard 09-0E and Centaur 10-13, both X-WRAP + X-UPEXIT. (d) The input-mirror twin 3 times: Shadow Rock, Shadow Flame Man, Gemini Rock. (e) 'A copy of you or your opponents' 6 times; the champion from your worst venue is fought by Doc Robot, then again in W2. (f) 'A guard checks for 3 collected items, then the side gate opens' twice: Tomahawk's Sheriff and Yamato's sekisho. (g) Hidden rooms opened by a full charge or punch on an odd object: H2, H3, H4, W1, W3, plus the identical OUT OF ORDER cabinet in all four Exhibitions. (h) A front-shield boss with shielded guards twice: Knight (SC1) and Flame's guard-bots plus Flame Man's DUEL class-3 guard. (i) Collect-N secrets in almost every non-venue stage: 8 high fives, 6 fuse boxes, 12 auditions, 24 score balls, 8 letters, 8 bells.

**Recommendation.** Cuts and swaps: H4 compactor → Dust Man conveyors without the ceiling chain; escape 0A → crumbling ladders. Keep one 'lights on a timer' set piece (the Semifinal's, which hosts Vending Man's glow); make H4 a flash-bulb photo puzzle instead. Centaur 10-13: replace the wrap tower with a tidal shaft that floods as you climb, keeping the Reap-bot, so the tide is the venue's spine. H3 Gemini → its own laser fallback, which is cheaper. Doc Robot MK-VI copies a Rockman 2 boss as in Rockman 3 (the plaque and workshop already set this up), not your worst champion. Flame Man's DUEL drops the shield and becomes a spacing duel: he parries only shots fired within 48 px, with a blade-glint tell, so Knight owns the shield. Yamato's sekisho: one pass plus a bribe in ryo, or the scroll gate alone. Non-venue hidden-room keys should use the new tools: an M.BEAM stair to a high window, Time Stop on a revolving door, the Super fist's return. Allow at most one collect-N secret per stage.

### design-6. [MAJOR] systems.md, meta.md · systems §0, §3, §9, §9.3; meta §9

**Issue.** There are too many systems and verbs for a NES Rockman, more than 4MI had. Every layer has been filled to its maximum.

**Evidence.** 5 bodies (4 forms plus Break Man); 8 weapons × tap/alt/synergy = 24 behaviours, plus M.BEAM build/magnet and the parry. 21 chips (BRIEF said 'about 14'). 8 PARTs and a garage with 4 recipes. The Y-TURBO booth. E-tanks, W-tanks, envelopes, venue prizes, tokens and racing colours. A 16-test rating. 7 post-game modes, 13 GP Rush courses, MY GP, KNOCKOUT and 12 Exhibition Rules. SELECT has four meanings (§1.1, §1.5, meta §3.8). systems itself names AFTERIMAGE and GLIDER as first cuts and flags the economy as too rich (Risks 10 and 12).

**Recommendation.** Cut PARTs and the garage. Keep 'the featured enemy dies to the champion's weakness weapon' only as an in-stage tell. That removes 4 chips; also cut AFTERIMAGE, GLIDER and JET TUNER, which brings the total to 14 as the BRIEF intended. Y-TURBO then costs bolts plus Break Man instead of a PART. Cut criticals and make KAISHIN always the deterministic EXCELLENT MOVE. Demote the parry and the Petal Shot, Feather Fan and Flare alts to Could, since no stage uses them as tools. Cut KNOCKOUT, Exhibition Rules and MY GP now rather than at crunch time.

### design-7. [MAJOR] systems.md, venues_a.md, venues_b.md, fortress.md · systems §13; venues_a §3.5, Risk 12; venues_b §0.2, Q7; fortress §4.4.1, §5.0, Risk 12

**Issue.** CASUAL has no per-stage mechanism, yet every stage doc assumes per-stage CASUAL levers, each invented independently.

**Evidence.** HARD gets poke lists plus 'BIT CFG_HARD' branches; CASUAL gets only global knobs (§13.2). Meanwhile: quick-draw 40 f, squadron counts at 4 of 5, Sidewinder HP 7 (venues_a); '(CASUAL)' checkpoints and a Toppy refill of 600 f (venues_b); CASUAL keeps the slide in POCKET, a mid-gap ledge at H1 0B, a 6-press grab (fortress). venues_b Q7 asks whether CASUAL is 'only damage and checkpoints'.

**Recommendation.** Add a CFG_CASUAL bit and per-section CASUAL poke lists in the HARD format. Publish one standard lever list that every stage fills in: reflex windows ×2, mash counts −40%, set-piece timers +50%, one extra checkpoint per section, and skill-gated secrets relaxed by one step.

### design-8. [MAJOR] systems.md, meta.md, fortress.md · systems §9.4; meta §6.3; fortress §2.5 b1, §4.5.3 b2, §5.2.4 b1

**Issue.** Doping silently and permanently removes three fortress secrets, so Platinum on those stages becomes impossible. The booth never warns about this, and the debrief never hints at it.

**Evidence.** Doping clears FORMS.TAG. The Semifinal LOCKER ROOM, H5's TWO BREAK MEN and W2's LOSERS' BRACKET are all TAG-gated. 'The judges' debrief never hints at the booth.' The fortress already defines non-TAG fallbacks for when Break Man is cut (Risk 7: 'tag gates become ordinary doors opened by a full charge'), and story S30 already has a 'walked' variant where the offscreen whistle unmasks Dark Man.

**Recommendation.** When RATEFLAGS.DOPED is set, apply the cut fallbacks so those secrets stay reachable. The cost stays as the partner, the asterisk, T1 and the headline. Make Mr. Y's second confirmation name the cost plainly ('Break Man will walk.').

### design-9. [MAJOR] systems.md, venues_*.md, fortress.md · systems §9.2, §10, §11, §12.3

**Issue.** Safety nets stack until the late-game difficulty curve flattens. Player power grows with the number of slots much faster than stage difficulty.

**Evidence.** Break Man is a second 20-HP body once per life, and he retreats 'with no life lost'. Beat's rescue is unlimited while HP ≥ 5. YASHICHI fully heals once per stage. DARUMA, SPIKE GUARD and CENTURION each block a death or hits. AUTO RECOVER. A respawn weapon refill. E-tanks heal 2× faster. The CHAMPION BUSTER caps every hit at 1. The escape clock gets +30 s after three tries. With 6 slots, NORMAL can carry 4-5 of these at once.

**Recommendation.** Take systems' Open Question 8 alternative: a Break Man retreat uses up his call for the rest of the stage. Beat's rescue works once per screen. YASHICHI and DARUMA are mutually exclusive, as one 'second wind' family. Tune at M4 by measuring deaths per stage with a full loadout against an empty one.

### design-10. [MAJOR] story.md, venues_a.md, venues_b.md, fortress.md · story §5.2, §6.3, S15, S23; venues_b title; fortress §3.1-3.4 deaths

**Issue.** Third-party trademarks reach the screen, despite BRIEF §6's 'parody names'. In addition, the 'commentators can't say the trademark' gag is undercut by plaques that name the games outright.

**Evidence.** The boss-panel VENUE field (story §5.2) types 'DRAGON QUESTLIKE' (Square Enix) and 'JUNGLE PITFALL' (Activision). venues_b's on-screen name is still 'PRINCE OF PERSIA PALACE'; only story renames it. Jokes name third-party characters: 'Blinky says hi' (E4 deaths), 'Popo and Nana' (BLZ death 6), 'Even Pit fell down a lot' (CEN death 6), 'Harry never let a log touch him' (PLT-06). Fortress builds a running gag ('TETR-... FALLING-BLOCK-FOUR-LINE-CLEAR!', 'Wakka wak- no. No trademarks.'), while S23's plaques print Tetris, Space Invaders, Pac-Man and Breakout by name.

**Recommendation.** Rename on screen: DRAGON QUESTLIKE → HERO'S QUEST (or TANTE-GP CASTLE), JUNGLE PITFALL → LOST JUNGLE, and adopt PERSIAN PALACE in venues_b. Remove third-party character names from jokes. Pick one plaque policy. Recommended: plaques use descriptions ('a falling-block puzzle born in Moscow, 1984'), so the 'can't say it' gag stays coherent and safer.

### design-11. [MAJOR] venues_a.md, systems.md, story.md · venues_a §3.1 T-BOOTHILL, §3.8.5, §3.10 deaths, §3.13; systems §9.3; story §2.10

**Issue.** The Tomahawk content note is good, but the venue's staging still frames the Native-coded champion as the outlaw of a cowboy town. Each fix is cheap.

**Evidence.** The boss arena T-BOOTHILL is a 'high-noon mesa top with grave markers', and death line 5 is 'Boot Hill has room for one more'. His secret arena is 'THE HIDEOUT' under a WANTED poster. The HIGH NOON duel casts him as the gunslinger the cowboy hero beats. systems §9.3 harvests a FEATHER PART from 'the venue's totem or vulture'. The totem walkers $12 stay on Must screens 03-04 and 12; their re-skin is only Could. story §2.10's 'laconic... dignified' is close to the stoic-noble stereotype.

**Recommendation.** Rename the arena HIGH NOON MESA and remove the graves; remove the Boot Hill line. Make the secret arena the Sheriff's office or a rodeo ring; the 'WANTED: ROCKMAN' gag still works there. Rename the FEATHER PART (e.g. SPUR) and drop 'totem' as a featured enemy. Make the cactus re-skin of $12 Must in this venue. Stage the draw as a judged tournament event, with a flag judge and the scoreboard. Give him a specific personality, such as a rodeo showman who is strict about duel etiquette, instead of stoicism. Keep the sneeze.

### design-12. [MAJOR] venues_b.md · §2.1 pitch, §2.3 screen 18, §2.11 FLM-01/FLM-08

**Issue.** The Flame venue is now the larger cultural risk, and venues_b still carries text that story already removed. Oil, a sultanate, a turbaned vizier, minarets and a crescent moon stack a regional stereotype, and the minaret plus crescent are religious symbols used as a combat backdrop.

**Evidence.** venues_b line 415, 'The Palace of the Oil Sultanate', and FLM-01 at line 632 are unchanged (story only dropped them in its own copy). Screen 18: 'domes, minarets, a crescent moon'. FLM-08 and §2.1: 'The vizier on the balcony is Mr. Y', with a turban.

**Recommendation.** Remove 'Oil Sultanate' from venues_b. On screen 18, draw domes and a full moon, with no minarets or crescent. Keep the vizier only as an obvious Wily-in-costume gag; the moustache is the joke. Aim the venue's jokes at Prince of Persia's mechanics, as story rule 3 already says.

### design-13. [MAJOR] venues_a.md, fortress.md, systems.md · venues_a §3.5, §4.8; fortress §2.3, §4.4.1, §5.3.3; systems §13.1

**Issue.** Accessibility defaults are unsafe: flash patterns are on by default, and the reflex windows ignore display lag.

**Evidence.** The Plant storm flashes 'bright 4 f, off 2 f, on 3 f' every 6-10 s across four screens, with FLASHES defaulting to NORMAL. The Semifinal floodlights 'flicker 20 f'. W3's 16-BIT BLAST flashes a row of the screen for 40 f. The escape ends with 'a red flash, a white flash'. The quick-draw window is NORMAL 20 f (333 ms) and HARD 12 f (200 ms), and it is used three times in Tomahawk (Sam, HIGH NOON, SHOWDOWN every 300 f); on a TV with 50-100 ms of lag, HARD is close to a coin flip. The Cossack Catcher's GRAB needs 10 presses in 90 f.

**Recommendation.** Add one cross-doc rule: in the default mode no effect flashes more than 3 times per second over a large area, and REDUCED turns every flash into a fade. Add a health notice at boot. Set the quick-draw to NORMAL 24 f and HARD 18 f, and add an INPUT LAG offset to CONFIG. Allow 'hold to struggle' as an alternative to mashing.

### design-14. [MINOR] meta.md, story.md · meta §3.5; story S14, S20, S24

**Issue.** The 'Semifinal' comes halfway through the first round, which breaks the tournament logic the premise is built on.

**Evidence.** Four venues are won, then the 'Semifinal', then 'the other four matches are back on', then 'Four venues to go! Then the final!'.

**Recommendation.** Rename the stage HALFTIME RIOT, or RIVAL MATCH. It happens at the bracket's halfway point, and a stadium riot at halftime is a ready-made sports joke. Alternatively keep the name and have Cossack lampshade it once.

### design-15. [MINOR] venues_a.md · §3.3, §3.6, §3.7

**Issue.** A missed train bounty is only revealed after the point of no return.

**Evidence.** 'once checkpoint 2 (12) is reached, only a replay brings the train back'. The Sheriff's count is shown at 12, after the train. With 32 of 32 screens used, there is no room for a retry loop.

**Recommendation.** Have the conductor at 0F read the bounty count before you board ('2 OF 3. SIDEWINDER RIDES THE 4:50.'). Optionally, let the 12 platform re-board the 4:50 once.

### design-16. [MINOR] venues_a.md, venues_b.md · venues_a §1.2-1.3, §3.6; venues_b §1.5.1

**Issue.** Fixed-length set pieces on the main route must be replayed in full on every revisit for medals or secrets. Wind is also thin outside the sortie, because all three of its secrets live in one 2-minute shmup.

**Evidence.** Wind's sortie lasts 2:00, and a death there restarts at 00. Tomahawk's train lasts 0:55 and Blizzard's bonus 0:40. Wind's 03-14 are vanilla screens with gust zones. The exit (4 squadrons), YASHICHI and the ACE act are all on screen 01.

**Recommendation.** After the first clear, offer a LAND option on the carrier that goes straight to the 02 checkpoint, at the cost of the sortie's secrets for that run. Shorten Wind's tower by merging 0E-12, and add one callback to the sortie in it: the destroyer's BG turrets firing up the shaft, or a POW riding a gust.

### design-17. [MINOR] venues_b.md · §2.5.1

**Issue.** The rule for merging with your shadow is partly untelegraphed and punishes the very behaviour it wants. Walking toward the mirror closes the gap at double speed, so a player who never fires still touches the shadow in under 5 s and takes damage.

**Evidence.** The merge requires 'have not fired since it appeared, for at least 5 s'. Shadow Rock has 'HP 12; contact 4'. The 5-s timer is invisible.

**Recommendation.** Make contact harmless while the player has not fired. Show a visible cue when the merge becomes possible: the shadow lowers its arm, or the mirror glows.

### design-18. [MINOR] systems.md, meta.md · systems §13.3; meta §2.3

**Issue.** The 1993 preset ('Vanilla rules... Like it's 1993') is incoherent. It promises vanilla but plays GP content with GP tools, and it removes a vanilla reward.

**Evidence.** M.BEAM and the Super Adaptor are kept. The '1993 row set' is generated from vanilla tables, but no vanilla row exists for Pi-kun, Bass β, the MK-VIs or the guests. GP bosses (Knight's HEALMORE +6, the snowman shield, Bass's SC6) are tuned for 16-f weakness kills, not 60 f per hit. Slot 9 is M.BEAM and the Beat rescue is off, so the B-E-A-T plates give nothing, whereas vanilla's plates gave the BEAT weapon.

**Recommendation.** Rename it '1993 RULES': the rules change, the content does not. Define the 1993 column for every new fight. Skip HEALMORE and SC6 under 1993. Let complete plates give the Beat rescue, the closest vanilla analogue.

### design-19. [MINOR] fortress.md · §5.0, §5.1 (01-05, 0D-10)

**Issue.** W1 is the showpiece of the premise, but it stacks two 'you are weaker' gimmicks in a row before the final stretch, and the second one only adds tedium.

**Evidence.** POCKET: firmware 1.0 (no slide, charge or forms), a 160×144 view, and 'the blind jump: the next ledge is outside the window'. Then SUPER: 'upgraded enemies take half damage... unless he is in 16-BIT MODE'.

**Recommendation.** Drop the half-damage rule. NOT COMPATIBLE becomes cosmetic, and Roll's patches become a pure power-up reward. Let the blind jump's ledge show 8 px inside the window.

### design-20. [MINOR] fortress.md · §6.3; §3.0

**Issue.** The victory lap loops the same 8 screens about 3 times (about 4 min). Separately, all four Exhibitions share an identical hidden room.

**Evidence.** §6.3: 'the lap repeats until the credits are done (about 3 laps, ≈ 4 min)'. §3.0: b1 is 'the BACKROOM behind the lobby's OUT OF ORDER cabinet... one rule for all four'.

**Recommendation.** Make the lap one denser lap; further laps optional (A to continue, START to finish). Drop b1 from the Exhibitions, or give each cabinet its own game's trick (E3: the UFO hit on the 23rd shot; E4: idle in the tunnel).

### design-21. [MINOR] systems.md, venues_*.md · systems §1.5, §11; meta §3.8; venue door, scroll and NPC verbs

**Issue.** Input overloads. UP+B alt-fire clashes with UP to interact (doors, scrolls, signs, NPCs, plaques). SELECT means four different things.

**Evidence.** 'RM6 has no up-aim, so UP+B steals nothing', but Centaur doors, Yamato scrolls, Knight signs and NPCs, Tomahawk posters and the outhouse, and every F-PLAQUE use UP. In the pause menu SELECT calls Break Man, while on the CHIPS page SELECT shows the help page.

**Recommendation.** Interact only on an UP press with B not held, and suppress interaction for 10 f after an alt. Make Break Man's call a pause-menu row confirmed with A.

### design-22. [MINOR] venues_a.md · §2.2 key economy, §2.5

**Issue.** In Knight's secret basement, a player can be stuck behind a door they cannot open. RETIRE prevents a hard lock, but the run is wasted.

**Evidence.** 'a player who runs needs the charged Power punch for one of the basement doors'. Knight may be the first venue, with no Power yet. No way back up is listed for 15 ↓ 18.

**Recommendation.** Have the stairs check the key count ('THOU HAST BUT 1 KEY'), or add a ladder back to 15 in 18. Let Break Man's Break Shot open the doors too.

### design-23. [MINOR] story.md, fortress.md · fortress §3.3 (1E plaque); story S27 H4/H5 plaques; §1.3 ladder

**Issue.** Small fact and voice slips.

**Evidence.** E3 plaque: 'IN 1978 THIS GAME CAUSED A COIN SHORTAGE' is stated as fact, although the doc says it is 'worded as folklore' (the story is disputed). The sincere plaques use two names: H4 says 'Break Man brought her home', H5 says 'the real Blues appeared'. 'It's definitely Wily' appears word for word in fortress §1.1, S07 p11, S25 and BLZ-04.

**Recommendation.** Reword to 'THEY SAY THIS GAME CAUSED A COIN SHORTAGE'. Use one name on the plaques (BLUES; story §1.3 needs a plaques exception) and vary the Wily line at each step of the ladder.

### design-24. [MINOR] story.md, fortress.md, meta.md · story S35, §5.4, S38; fortress §5.1.4, §5.3.2, §0.5; meta §1.6, §3.8

**Issue.** Names and counts the player sees disagree between docs.

**Evidence.** The W1 boss is 'THE UPGRADER' (story, which 'grabs Rockman') but METALL 16 in fortress. The final machine is 'WILY MACHINE 6.5' in story and 'MODE-7 MACHINE' in fortress. meta shows 'a grid of the 15 chips' with a 16-bit CHIPS_OWNED; systems has 21 chips and 24 bits. Mr. Y's YES/NO heckle is a fake commercial in fortress but '1-bolt respawn insurance' in story.

**Recommendation.** Use METALL 16. Name the panel WILY MACHINE 6.5, with Mode 7 as its gimmick. Update meta to the final chip count. Use story's insurance gag (the CX 'Yes that hurts').

### design-25. [MINOR] venues_b.md · §4 (Yamato)

**Issue.** Yamato is overstuffed: three homages plus four cultural set pieces in 30 screens, and the most new object kinds of any venue (about 14).

**Evidence.** Jajamaru bonk-stun, Goemon passes and the sekisho, spinning scrolls, the nightingale floor with Knight's ceiling, the Daruma (T8), the DuckTales pogo EXWP, hanabi, the kabuki arena, kites and ashigaru.

**Recommendation.** Cut the kite run (19 becomes plain sunset roofs) and either the bonk-stun or the sekisho (see the repetition finding), so that the pogo, the Daruma and the nightingale floor carry the venue.

## Decisions needed (15)

1. **Break Man's disguise: do characters respect it (story §1.3), or call it out as 'OBVIOUSLY Blues' (fortress)?**
   - Options: A) Respect it; only Rock says 'Blues?' twice, and Light says the name once at the end. B) Everyone calls it out, as with Mr. Y.
   - Recommended: A. It gives the good-side gag its own flavour; B duplicates the Mr. Y joke.
   - Affects: fortress §2.6, §4.5, §5.3.3; story §1.3

2. **Where does Break Man join, and how is he introduced?**
   - Options: A) Opening roll call (masked, named) → help at the Semifinal → joins at Semifinal 0E with Rule 9 played in place. B) Story's version: joins on the bracket after the stage. C) Fortress's version: no Opening appearance, revealed at the Semifinal.
   - Recommended: A
   - Affects: story S06, S08, S18, S20; fortress §1, §2.6; meta EVENTS b5

3. **What is the single ending order, and how does Break Man exit?**
   - Options: A) Story's scenes, reordered so LIGHTS OUT and the sixth wing come last before TO BE CONTINUED, with Break Man carrying Rock and Wily out (S40). B) Fortress's order (lights out mid-sequence, then the lap). C) Story's current order.
   - Recommended: A, with story.md owning it. Drop the door-holding and roof variants.
   - Affects: fortress §5.4, §6.1-6.3; story S39-S48; art_audio ending stems

4. **Should 'SEMIFINAL RIOT' be renamed, given it happens halfway through round one?**
   - Options: A) HALFTIME RIOT. B) RIVAL MATCH. C) Keep SEMIFINAL and lampshade it once.
   - Recommended: A
   - Affects: BRIEF §3, meta §3.4-3.5, story S14-S24, fortress §2

5. **Gamma's fists-only phase 2 makes POWER a required tool in H3. Change the boss or the rule?**
   - Options: A) Amend the fortress rule: POWER (owned from win 2) may be required, with a tell. B) Let the full charge also hurt the cockpit.
   - Recommended: A, plus a no-risk fist-ride practice beat before the fight.
   - Affects: fortress §0.2, §4.3.4; systems §2.4, SC5, §13.3

6. **On-screen venue names and the plaque naming policy?**
   - Options: Venue names: rename DRAGON QUESTLIKE, JUNGLE PITFALL and PRINCE OF PERSIA PALACE, or keep them. Plaques: name the real games, or describe them.
   - Recommended: Use HERO'S QUEST, LOST JUNGLE and PERSIAN PALACE. Plaques describe rather than name, keeping the 'can't say the trademark' gag. Remove third-party character names (Blinky, Popo and Nana, Pit, Harry) from jokes.
   - Affects: story §5.2, §6.3, S23; venues_a/b titles; fortress §3

7. **Which complexity cuts should be made now?**
   - Options: PARTs and the garage; chips down to about 14; criticals; the parry and the weak alts (Petal Shot, Feather Fan, Flare); KNOCKOUT, Exhibition Rules and MY GP.
   - Recommended: Cut all of them now. Y-TURBO then costs bolts plus Break Man instead of a PART.
   - Affects: systems §3, §9, §14; meta §3.8, §6.1 T6, §9; story §8

8. **How far does the doping cost reach?**
   - Options: A) As designed: the partner and the TAG-gated secrets are lost forever. B) The partner, the asterisk and T1 are lost; TAG-gated secrets use the existing 'Break Man cut' fallbacks. C) TURBO can be returned to Mr. Y for all your bolts.
   - Recommended: B, and the second confirmation states 'Break Man will walk.'
   - Affects: systems §9.4; meta §6.3; fortress Semifinal b1, H5 b2, W2 b1

9. **Should CASUAL get its own per-stage mechanism?**
   - Options: A) A CFG_CASUAL bit, CASUAL poke lists and a standard lever list for every stage. B) Global knobs only, with the venue-specific CASUAL tweaks removed.
   - Recommended: A
   - Affects: systems §13; tech poke-list format; every venue and fortress section that mentions CASUAL

10. **Flash safety and reflex windows: what are the defaults?**
   - Options: Flash rule: no more than 3 large flashes per second in default mode, a health notice at boot, REDUCED turns flashes into fades. Quick-draw: 20/12 f as now, or 24/18 f plus an INPUT LAG offset.
   - Recommended: Adopt the flash rule. Set the quick-draw to 24 f (NORMAL) and 18 f (HARD) with an INPUT LAG offset; CASUAL stays at 40 f.
   - Affects: systems §13.1; venues_a §3.5, §4.8; fortress §2.3, §5.3; art_audio

11. **What is the 1993 preset's scope?**
   - Options: A) '1993 RULES': vanilla combat rules over GP content, with a defined 1993 column for new fights and plates giving the Beat rescue. B) Remove the GP-only tools (M.BEAM and Super) under 1993.
   - Recommended: A
   - Affects: systems §13.3; meta §2.3, §6.1; fortress §0.2

12. **Which repeated set pieces should be cut or swapped?**
   - Options: H4 ceiling compactor; escape 0A ceiling; H4 Bright rooms vs the Semifinal blackout; Centaur's wrap tower; H3's Gemini Rock; Doc Robot copying your worst champion; Flame Man's shield DUEL; Yamato's 3-pass sekisho vs Tomahawk's 3-bounty Sheriff gate; full-charge hidden-room keys; collect-N secrets.
   - Recommended: Swap all as listed in the repetition finding. Centaur becomes a tidal shaft, Doc Robot copies a Rockman 2 boss, Flame's duel becomes about spacing, Yamato uses a bribe or a single pass, and each stage has at most one collect-N secret.
   - Affects: venues_b §2, §3, §4; fortress §2, §4, §5

13. **How should the Tomahawk venue be staged?**
   - Options: Arena T-BOOTHILL vs HIGH NOON MESA; secret arena THE HIDEOUT vs the Sheriff's office or a rodeo ring; FEATHER PART renamed; cactus re-skin of $12 as Must.
   - Recommended: HIGH NOON MESA without graves; the Sheriff's office or a rodeo ring; rename the PART; make the re-skin Must; drop the Boot Hill death line; give him a specific non-stoic personality.
   - Affects: venues_a §3; systems §9.3; story §2.10, §6.3

14. **What is the Opening's text budget?**
   - Options: A) About 15 SCN pages, one intro, rules folded into the lane judges. B) As written (about 60 pages).
   - Recommended: A
   - Affects: story S02-S08; fortress §1.1, §1.3-1.4; meta §2.1

15. **Should replays offer skips for fixed-length set pieces, and how long is the victory lap?**
   - Options: A LAND option after the first clear for Wind's sortie, plus auto-skipped NPC text on replays. Victory lap: one lap vs about 3.
   - Recommended: Offer the skips; they forfeit that set piece's secrets and score rows for the run. Use one lap, with further laps optional.
   - Affects: venues_a §1.2, §3.6; venues_b §1.3; fortress §6.3

# critic-feasibility

## Verdict

The engine plan can be built, but not as the eight docs are written now. I found 1 blocker and 13 major problems. The blocker is that ExRAM is assigned to two incompatible jobs. The major ones are:
- two incompatible stage-id maps;
- arena warps that carry the previous stage's breakable and kill bits (measured);
- a lag budget that leaves out the player and the screen-script slots;
- a punch re-class that misses 18 of 21 latch tests;
- tech and systems disagreeing on what the frozen tick does;
- the form-swap and weapon-slot CHR budgets;
- player shots having only 3 slots;
- C-window re-entrancy and a lag-frame trap for blocking text;
- the text model and line widths;
- WORK RAM and the 1 MB ROM both over-committed;
- unaudited player variants (SUPER as form 3, and Break Man).

Many claims hold up, and I re-checked them in the ROM and emulator:
- the MMC5 port list is complete for the fixed banks;
- the IRQ table, the 30 free type ids, the free ROM and sound space, and the $FFE0 guard are all as stated;
- the vanilla warp into a boss room works when the bitfields are clean;
- FCEUmm does emulate ExGrafix with 8 KB CHR-RAM.

The fixes are mostly re-specification and re-budgeting, not new tech, but they must land in tech.md before M2. Scripts, probe ROM and screenshots are in /home/user/Rockman_6_ROM_Hack/build/review/critic-feasibility/.

## Strengths

- MMC5 port list (tech §1.4-§1.7) is complete for the fixed banks. A full scan of $3E/$3F/$34/$38 for MMC3 register stores matches it exactly: 15 latch and 12 disable writes, the ack pair, two NMI arm paths, the helpers, the sound service and reader, the NMI CHR copy at $C7AF/$C7B4, $FF96/$FFC9/$FFCE/$FFD4, and 4 real $A000 writes. Other hits are data in the CHR banks or bank $39.
- Verified in ROM: $C51E's guard ($FFE0-$FFEF = FF, compared against a table at $C53E, and $FFF8 = $08); 'A9 3E 20 91 CB' at $E204 and $E430; 'A5 FB 8D 00 A0' at $C01F; $C7D6 = 40 10 20 30; the IRQ table at $C116 with 27 entries, where index $1B reads $8A48; 30 free type ids, $F4-$FF clean, $CF/$D2 pointing at filler; the 449-byte $36 tail; the 1,120-byte $FAC0-$FF1F hole; the 9×16 stage table; $F232 and $F518 as quoted; the multiply loop at $34:$8006; the reader's $C000 → bank $36 range at $803A; the interpreter entry $3C:$8631 with the pointer read at $8636.
- Verified in the emulator: the vanilla respawn warp straight into a boss room spawns the boss intro ($93 → $95), so meta's fight loader is sound once the bitfields are cleared. FCEUmm emulates ExGrafix (ExRAM mode 1) with 8 KB CHR-RAM, which makes art_audio's per-tile-palette spike viable.
- The save model (meta §1: ping-pong A/B copies, commit marker, a BROKEN path on every screen, LIVE image = format), page isolation and the boot RAM probe are robust and implementable.
- art_audio's measured facts hold: form sheets differ in 118 of 128 positions, and the CHR set table format is bank in bits 1-6, +$1000 in bit 0.

## Findings (22: blocker 1, major 13, minor 8)

### feasibility-1. [BLOCKER] fortress.md vs tech.md (also art_audio.md, story.md) · fortress §5.0 table row 'Palette' and §5.1-§5.3 ('W2 and W3 stay 16-bit'); tech D6, D7, §3.3, §11.3

**Issue.** ExRAM has two incompatible jobs.
- tech uses ExRAM in mode 0 as the nametable for every text window and pop-up 'for the whole game' (D7).
- fortress makes W1-SUPER, W2 and W3 into ExGrafix stages (ExRAM mode 1, per-tile attributes). W2 and W3 are Must.
- ExRAM is 1 KB and runs in one mode at a time. In mode 1, 960 of its bytes are attributes. So in those stages no pop-up, Mr. Y/Wily heckle, W2 bout commentary or Break Man gift dialogue can display.
- fortress says 'tech.md confirms' ExGrafix works with scrolling, but tech D6 says the opposite: 'no ExGrafix in scrolling stages'.
- fortress's 'one extra 4 KB CHR page of 16-bit detail tiles' (§5.1 Tileset) cannot exist with 8 KB CHR-RAM: the page bits reach only $0000 or the sprite table at $1000. 245 of the 256 sprite-table tiles are drawn in play (tech §7.6).
- In mode 1, CPU writes count only during rendering (tech §3.3). The ExRAM column stream cannot ride the NMI column painter; it needs an IRQ-band write timed to the frame the column appears.

**Evidence.** Probe ROM build/review/critic-feasibility/probe/exgfx.nes on the bundled FCEUmm: ExRAM was filled in mode 2, then switched to mode 1.
- Left half: palette 1 per tile gave green (72,220,72).
- Right half: palette 2 with page bit 1 drew tile 1 from $1010, the sprite table: (56,188,248).
So per-tile palettes work with CHR-RAM, and the page bits select only the BG or the sprite pattern table.
The docs as quoted: tech D7 says 'ExRAM in mode 0 = a spare nametable for text windows' and §3.3 'Mode 0 for the whole game'; fortress §5.0 says 'SUPER is ExGrafix data per screen (1 KB of ExRAM per screen ...): tech.md confirms'.

**Recommendation.** Rule that ExRAM stays in mode 0 globally. Allow ExGrafix only in locked rooms with no text: the W1 16-bit section 0C-12 and the METALL 16 arena, filled in mode 2 while the screen is blanked and then switched to mode 1, with commentary suppressed there.
- W2 and W3 get 'SUPER colour' through palettes, parallax and MMC5 audio only.
- Drop the extra 4 KB page.
- If ExGrafix is wanted on scrolling screens anyway, specify a non-ExRAM text fallback (a nametable row reserved by the level build, or sprite text) for every ExGrafix stage, plus the IRQ-timed column writer, and budget both as [new-code] M.

### feasibility-2. [MAJOR] tech.md vs fortress.md (and meta.md) · tech §4.2 id map; fortress §0.1 'H1-H5 and W1-W3 therefore keep the fortress ids 8-15'; tech cross-doc table ('fortress.md: ids $16-$1D, $1F')

**Issue.** The two docs give incompatible stage-id maps.
- tech: venues $00-$07; legacy Mr. X and Wily $08-$0F unchanged; Opening $10, Semifinal $11, E1-E4 $12-$15, H1-H5 $16-$1A, W1-W3 $1B-$1D, lap $1E, Mr. X Returns $1F, DEV $20.
- fortress: H/W reuse 8-15, Opening 16, Semifinal 17, E 18-21, Mr. X Returns 22, lap 23.
fortress's argument that the vanilla AND #$08 and CPY #$08 tests keep working 'with no code change' is moot: tech M2.1 rewrites all 45 $51 readers anyway (Must). It is also wrong for its own ids 22 and 23, which have bit 3 clear and so need the attribute table too.
Under fortress's map the vanilla fortresses can no longer be loaded by id. That breaks:
- tech's M1 golden suite ('each of the 16 stages');
- the TRUE GP '???' fight, which is vanilla Wily 4 (fortress §0, meta §9.2.1);
- meta's 1993 CUP, which uses vanilla Wily 3's refight rooms.

**Evidence.** tech §4.2: 'All 32 ids are taken ... legacy block $09-$0F is the flex'. fortress §0.1 table: 'H1 ROCKMAN | 8 | Wily 2 ...', 'Opening Ceremony | 16'. meta §9.2.4 course 13: '1993 CUP ... the 8 champions in vanilla Wily 3 hub order'.

**Recommendation.** Adopt tech's map. Renumber fortress (H1-H5 = $16-$1A, W1-W3 = $1B-$1D, lap $1E, Mr. X Returns $1F) and keep legacy $08-$0F for regression, Mr. X Returns, the ??? fight and the 1993 CUP. fortress's stage rows then set CLASS = FORTRESS and FORT_COL in the attribute table.

### feasibility-3. [MAJOR] tech.md, meta.md, fortress.md · tech §4.5 step 2 (stage-init hook); meta §9.2.1 ('Loading a fight uses vanilla's own warp'); fortress §5.2.1-§5.2.2 (W2 alcoves call the fight loader, TAG! warps)

**Issue.** The respawn warp across stages keeps the previous stage's alternate-metatile bits ($0340) and kill field ($0650). The arena then loads with corrupted terrain, and its list objects, the boss-room screen script included, can fail to spawn. That is a soft lock in W2 (Must) and in GP Rush.
Clearing the bits is not enough either: vanilla Wily 3, the base of W2, records closed alcoves in $0340. A trip to a venue arena and back would therefore reopen every alcove.
No doc specifies either:
- a hub-state snapshot;
- a 'fight context' that stops the venue's own clear path (YOU GET, FLAGIDX, NEXT, autosave 4, debrief) and its death respawn from running after a W2 or GP Rush bout.

**Evidence.** Measured (build/review/critic-feasibility/warpstale.py): from Blizzard start, $0650-$066F and $0340-$035F were set to $FF, then a warp to Knight with $F0 = 2.
- After the warp both fields still read FF; screen 00 drew with alternate metatiles (screenshot warp_stale_knight.png vs warp_clean_knight.png).
- The type-$80 screen script never spawned: 1 live slot, against 2 in the clean control.
Code: the clear $3E:$CE44 is called only from $CE52, which runs on the new-stage path at $CD43, not on respawn.
Control (bosswarp.py): with clean fields, a warp straight into Knight's boss room (screen $17) does spawn the $93 intro, which becomes $95. So the loader idea itself works.

**Recommendation.** - Make the stage-init hook call $CE44 whenever RAM_ID ≠ the new id.
- Add a 64-byte WORK snapshot of $0340/$0650 (plus the map-edit log) for a 'return-to' stage, so W2's hub and the GP Rush lobby restore on return.
- Add a FIGHT_CTX byte that the boss-death, stage-clear and respawn paths test: return to the hub or lobby, skip the venue's YOU GET, flags and save.
- Retag W2 §5.2.1 from '[engine-ok] data + [new-code] S' to [new-code] M.

### feasibility-4. [MAJOR] venues_a.md, venues_b.md, fortress.md, tech.md · venues_a §0.5 and its caps (e.g. §1 sortie 'Lag cap: 5 planes + 2 enemy bullets + 3 shots = 10'); venues_b §0.2 ('player included and shots excluded; target ≤ 8'); fortress §0.8 and caps (E2 '= 10 (the cap)'); tech §6.3 check 6 ('≤ 8 plus shots'), §15.2

**Issue.** The ~10-object budget is counted three different ways, and every way undercounts against the measurement it cites.
- The measured lag table counts occupied slots, and those include slot 0 (the player) and slot 22 (the screen script).
- At 9-10 slots, 9-10% of frames lag; at 11-15 slots, 25-40%.
What the plans give in real slots:
- venues_a's '10' leaves out the player, the script and the wave director: 13 slots.
- venues_b's and tech's '8 + shots': 8 + 3 + script = 12 slots.
All of these sit in the 25-40% lag band before GP adds per-frame costs:
- the frozen-tick test per slot;
- LASTHIT/LATCHSRC writes;
- the SELECT filter and scorecard timers;
- IRQ bands at about 100 cycles each;
- C-window dispatch at about 55 cycles per call.
The planned savings that would pay for them are Should (M3 OAM builder), not Must.

**Evidence.** engine.md §8.2 table: '9-10 → 9-10%; 11-15 → 25-40%'. build/research/rm6/rm6-engine/tour.py: nobj = count of non-zero $03A0+s for s in 0..$16. Emulator: a quiet Knight 00 / Blizzard 00 screen already holds 2 live slots, types $04 (player) and $80 (script).

**Recommendation.** Set one rule in tech §15: count every occupied slot (player, script, directors, shots, effect objects). Budget 9 slots until M3.8 measures the real gain.
- Make tech §6.3 and artcheck enforce it.
- Fold directors and band objects into the slot-22 screen script where possible.
- Re-check the caps already at their limit (sortie, AYACO, train, Paddle Man, Reaplet alarm, Flame 0B).

### feasibility-5. [MAJOR] systems.md · §2.2 POWER ('The punch moves to its own shot class: tap $22, half $23, full $24 ... test $24 instead of $14'), §6.4 item 1 ('Vanilla routines that test $14 ($EA99, $90A2, $31:$9AD6) are rewritten')

**Issue.** Re-classing the punch changes the attack byte that many enemy AIs compare directly. systems lists 3 routines to patch, but the vanilla hit-latch tests for $14, $13 or $1A number at least 21, most of them inside per-enemy AIs. Every unpatched one stops reacting to the full punch: Metall-style guards, breakable objects, Wily 1's rebound, and so on.

**Evidence.** Static scan (build/review/critic-feasibility/latchscan.py) for 'LDA $056C,X' followed by CMP #$14/#$13/#$1A found 21 sites:
- $29:$AA61, $AA69, $BDC1, $BE2C;
- $30:$8A2D, $92E5, $9625 (#$13), $970C;
- $31:$A40A, $A81A, $B20A, $B696, $B7F4, $B9B7, $BD90;
- $39:$A224, $B28B (#$1A), $B3AB;
- $3B:$A295, $A52F;
- $3F:$EA9B.
Disassembly confirms the pattern, e.g. $30:$8A2D 'LDA $056C,X / CMP #$14 / BNE'.

**Recommendation.** Do not re-class the punch. Keep vanilla attack bytes ($11-$14) and derive the scoring category from LATCHSRC, which systems §6.4 item 2 already writes on every latch store. That removes the need to patch about 20 AI sites and keeps vanilla enemy behaviour exact. If a re-class is still wanted, add every latch-compare site to the hook registry, found by a static scan like the $51 audit.

### feasibility-6. [MAJOR] tech.md vs systems.md · tech §7.7 'Frozen tick ... if FREEZE,X ≠ 0, decrement it and skip the AI call'; systems §4.8 'The object loop therefore calls, for each frozen slot, only that type's damage routine' (Time Stop, Ice Block, WEAK stagger)

**Issue.** The two docs specify incompatible engine behaviour.
- tech's tick skips the AI, so a frozen object processes no damage. Hits only overwrite the latch, and only the last one lands at unfreeze. Time Stop and the Ice Block, whose stated value is 'the frozen tick still applies damage', stop working.
- systems' version calls a per-type 'damage routine', but those routines are not pure damage functions. $3F:$E9D7 is the whole standard enemy tick: off-screen check $E489, hit flash $03B7, SFX $35, and on death a far call into the explosion type through $CB28.
- Boss routines ($31:$997D, $EF64) assume their AI bank and state.
- A 256-entry type → routine table cannot tell sub-ids apart inside the GP families $F4-$FF, where most new enemies live.

**Evidence.** $3F:$E9D7 disassembly: LDX $8F / clear $03B7 b0 / JSR $E489 / BCS ... / LDA $056C,X ... SBC ... / BPL / LDY #$17 / JSR $CB28 (death). tech §7.2: families resolve the AI per sub-id.

**Recommendation.** Rule for systems' semantics: damage continues while frozen. Implement it as a per-(type or family+sub-id) 'frozen handler' pointer in the GP flag table, valid only for enemies whose damage step is $E9D7/$EA20/$EA6E. Every other type is NOFREEZE (it ignores Time Stop and the Ice Block freeze but still takes hits). Bosses use a boss-side 'frozen' state, not a skipped AI. Rewrite tech §7.7 to match.

### feasibility-7. [MAJOR] systems.md (vs art_audio.md, tech.md) · systems §1.3 SYS-CTL-4 ('Target n ≤ 8: at most 64 changed tiles ... a 12-frame flash'); tech §15.3 ('systems.md's form swap (≤ 1 KB) takes 8-16 frames')

**Issue.** A form swap must stream about 1.9 KB.
- At tech's own budgets (128 B/frame when still, 64 B with a column paint) that is 15 frames standing still and about 30 while scrolling, not a 12-frame flash. Tech's '≤ 1 KB, 8-16 frames' is also wrong.
- Every form sheet also fills the weapon slot $71-$7F with 15 form-specific tiles. Under 'forms fire every weapon' the equipped weapon's shot set must be re-streamed after the sheet (+240 B), and synergies that draw both the fist and weapon tiles (Burning Knuckle, Time Fist, Morning Star) compete for the same 15 ids. No doc defines who owns $71-$7F in each form.

**Evidence.** build/review/critic-feasibility/formdiff.py: in each of sets $04-$07 (bank $01; CHR set entries 80 00 00/80 82/83), 118 of 128 tile positions differ from the normal sheet and 109-114 tiles are absent from it. In each form sheet the 15 tiles $71-$7F are non-blank and none equals the normal sheet's buster tiles. art_audio §1.5 agrees with this.

**Recommendation.** - systems: accept a 16-20-frame swap behind the flash, or require tech's 256 B/frame unrolled copy on non-scrolling frames. Measure it in an M1 spike (8 frames still).
- Queue the weapon set after the sheet.
- Have systems and art define a per-form $71-$7F map that lists which synergy tiles must be resident together.
- Update tech §15.3's figure.

### feasibility-8. [MAJOR] art_audio.md (with venues_a.md) · art_audio §2.4 'Weapon slot ($71-$7F, 15 tiles)' and §4.2 'Weapon-slot poses: Rock on Rush, the loop (4 frames) | 24 tiles', §7.1 'Set-piece poses in the weapon slot ... 20 tiles', §4.2 'The sortie (01) carries SET-WS1 + WS2 + WS3 = 96 tiles'

**Issue.** The sprite CHR for Wind's sortie (Must) cannot fit.
- The Rock-on-Rush loop poses (24 tiles) are assigned to the 15-tile weapon slot, and the sortie's enemy area is already 96 of 96.
- More generally, the plan puts 27 alt-fire tiles plus set-piece poses (pogo, vine, condor carry, swap flash) into a slot that some weapon sets fill completely. Sets $56, $5D and $29 are 15 tiles at $71, and each form sheet fills it too.

**Evidence.** CHR set table in ROM ($37:$8000): set $56 = 0F 07 00 80 (15 tiles at $71), set $5D = 15 tiles at $71, set $29 = 15 tiles at $71. art_audio's own tables: 24 tiles in the 15-tile slot.

**Recommendation.** Give set pieces that change Rock's body a dedicated 128-tile 'set-piece player sheet', streamed like a form swap at a locked moment (sortie catapult, vine section entry, pogo rack), instead of the weapon slot. Have artcheck reject any weapon-slot set over 15 tiles, and list per weapon how many tiles its alts actually have free.

### feasibility-9. [MAJOR] systems.md, tech.md · systems §3 (Wall Spear 'Max 2' for 240 f, Ice Block 240 f, Updraft 150 f, M.BEAM 'Max 3 beams' for 240 f, held mace, Petal Shot 4, Feather Fan 3, Centurion bot); tech §7.2 gp_spawn = $E59F

**Issue.** No doc assigns object slots to the new player-side objects. The vanilla shot allocator offers only slots 1-3: it searches 3 down to 0, and slot 0 is the player. Slot 4 is Beat/Rush and 5-7 are 'special'.
- If the persistent platforms take shot slots, three M.BEAM beams lock out every shot for 240 f.
- If they take enemy slots 8-$15 (gp_spawn → $E59F), they count against the enemy cap and the lag budget, and must call the shot-vs-enemy routine $38:$8FDF themselves.
- Feather Fan (3) and Petal Shot (4) need all the shot slots at once, as B.ATTACK does in vanilla (slots 1-4 empty).

**Evidence.** $3F:$E514 'LDX #$03 / LDA $03A0,X / BEQ / DEX / BPL' (slots 3..0); $3F:$E59F 'LDX #$15 ... CPX #$08' (enemy slots $15..8); engine.md: '4 = Beat / Rush, 5-7 special'.

**Recommendation.** Add a slot plan to tech §7, for example:
- shots in 1-3;
- one persistent player utility in each of 4-7 (beam, spear platform, ice block, column, Centurion);
- Beat's rescue reusing 4.
Then cap each weapon to fit the plan (e.g. M.BEAM max 2 if Beat or Break Man needs a slot) and have the utilities call $38:$8FDF where they deal damage.

### feasibility-10. [MAJOR] tech.md · §1.9 C-window rules ('C-window code never yields'; CW saves A/X/Y/P in CW_A-P; returns with CWIN_CUR = $FE; vectors restore CWIN_CUR), §1.2 ('$44-$45 text engine ... C-window'), §11.5 ('TALK id (dialogue, blocking)'), §8.1 OPS b6 band routines, §3.3 line-8 ExRAM flush band

**Issue.** Three execution-model holes.
1) Blocking text in the C-window would hang the game. Code that waits for frames without yielding leaves $F2 ≠ 0, and then the NMI treats every frame as a lag frame: it skips PPU updates and the joypad read. The typewriter could never upload glyphs and WAIT could never see A.
2) CW is not re-entrant. It has one save area and one CWIN_CUR, and it always returns to $FE.
   - A CW target that calls CW returns into $7E instead of its own bank.
   - A CW call from an interrupt (band routine, ExRAM flush, irq_logic_tick) clobbers the main thread's saved registers.
3) The NMI exit restores CWIN_CUR, the main thread's window, even when the NMI interrupted an IRQ handler running from $7E at $C000-$DFFF (M1 literal port). That handler would resume in the wrong bank.

**Evidence.** engine.md §8.1: 'If $F2 is still non-zero the frame is a lag frame: the NMI skips OAM DMA, PPU updates, the frame counter $F3 and the joypad read'. tech §1.9 pseudo-code: 'CWIN_CUR = $FE ; STA $5116 ; RTS'.

**Recommendation.** - Run TALK, CHOICE and any frame-waiting UI as a scheduler thread or object coroutine in an $8000/$A000 bank that yields through $E46C; the C-window keeps only non-waiting services (glyph blit, layout).
- Make CW push the previous $5116 value and the registers on the stack.
- Make the NMI and IRQ stubs push and pull the $C000 bank they interrupted.
- Forbid CW calls from interrupt code: band routines live in $7F.

### feasibility-11. [MAJOR] tech.md vs story.md vs art_audio.md vs meta.md · tech §11.4 (pop-up '2 lines × 16 tiles (32 ids)', EN VWF, dialogue '3 lines × 26 columns'); story §10.1-10.3 (POP 2 × 28 cells, 24-tile glyph cache, SCN 4 × 28, EN ALL CAPS); art_audio §3.5/§9.6 (mixed-case EN set; glyph allocator ≤ 24 ids); meta §4.1 (debrief 4 × 28)

**Issue.** The docs specify two text-rendering models.
- tech: a VWF canvas. Tiles are not reused, so a pop-up needs 32 free BG ids and holds about 22 EN or 16 JP characters per line.
- story and art: a fixed-cell glyph cache. A pop-up uses at most 24 distinct glyphs over 2 × 28 cells.
The consequences:
- story's ~300 commentator lines were written to 28 cells, which do not fit tech's 16-tile JP pop-up.
- The free-id requirement per screen differs (32 vs 24), and that decides how often pop-ups are deferred on dense venues. Plant has 0 free ids.
- Dialogue is 3 × 26 (tech) but 4 × 28 in story and meta.
- tech §11.4 reads back up to 80 borrowed tiles (64 canvas + 16 portrait = 1,280 B) into WORK, but no WORK range holds them.
- The case set is unresolved: story wants ALL CAPS, art plans mixed case.

**Evidence.** tech cross-doc row: 'pop-up 2 lines × 16 tiles (~22 EN characters with the VWF, 16 JP)'. story §10.2: 'POP (in-stage) | 2 × 28 | 24 tiles'. tech §3.4: the text area $6A00-$6DFF (1 KB) already holds the 768 B canvas buffer.

**Recommendation.** - Pop-ups and help pages: rule for story's fixed-cell glyph cache (ALL CAPS, 2 × 28, ≤ 24 ids, pages split by the compiler). Keep VWF only for frozen full dialogue, if at all.
- Set dialogue to 4 × 28 everywhere.
- When a dialogue closes, restore borrowed tiles from their ROM CHR source (the build knows each screen's CHR state) instead of reading them back. That removes the 1.25 KB buffer.
- Drop art's mixed-case set.

### feasibility-12. [MAJOR] tech.md (all docs' WRAM claims) · tech §3.4 WORK map; §15.2 step 5 / §3.4 '$6E00-$6EFF 256 B: CHR stream queue + WRAM-resident unrolled VRAM copier'; §11.4 borrowed-tile read-back; §7.9 pad history; §8.1 'ARG, MAP5105, palette set in $7A00+'; fortress §0.7 F-GRID; meta §9.2.3 runner

**Issue.** The WORK page is over-committed.
- tech allocates 6.5 KB and leaves 1.5 KB ($7A00-$7FFF) free.
- Unbudgeted claims total about 2.6-3.3 KB: borrowed-tile save 1,280 B; the unrolled copier at 6 B of code per byte copied (768 B for 128 B/frame, 1,536 B for art's 256 B/frame), which cannot share a 256 B slot with the stream queue; F-GRID 16×14 = 224 B; T7 pad ring 64 B; raster auxiliary arrays about 96 B; GP Rush runner list and state about 64 B; the W2/lobby snapshot 64 B; Break Man and Beat state.
- All four 8 KB pages (SAVE, WORK, LAYOUT, TILES) are fully assigned, so nothing absorbs the overflow.

**Evidence.** Sum of tech §3.4 rows: 512+32+48+176+256+1536+1024+256+256+512+512+512+1024 = 6,656 B. 4MI's copier: 'LDA abs / STA $2007' at 8 cycles per byte = 6 code bytes per byte.

**Recommendation.** - Put the unrolled copier in ROM (a GP bank the NMI maps at $8000, as the vanilla CHR copy does at $C7AD), staging only a 128-256 B data buffer in WORK.
- Restore borrowed tiles from ROM (see the text finding).
- Shrink the map-edit log to 256 B.
- Publish a WORK ledger with an owner per range, enforced by the allocator.

### feasibility-13. [MAJOR] tech.md vs story.md, art_audio.md, fortress.md · tech §1.2 bank roles, §5.4 ('22 stages × ~1.3 sections × 2 KB ≈ 60 KB'), §12.4 ('16 banks (128 KB) ... $70-$77 + the $0B-$0F pool'); story §10.4 ('≈ 70-90 KB ... in 2-3 text banks'); art_audio §2.2, §13; fortress §5.0 ('1 KB of ExRAM per screen')

**Issue.** The 1 MB bank map does not match the content plans.
- Text: tech reserves 4 banks (32 KB, $46-$49); story needs 70-90 KB. story's own '2-3 text banks' (16-24 KB) also contradicts its 70-90 KB.
- Layouts: tech gives 4 banks (32 KB, $6C-$6F) shared with object lists, scripts and poke lists, against its own 60 KB layout estimate.
- Tilesets: tech gives 8 banks with 2 slots each; art plans 10 banks with 3 slots each.
- Music: tech reserves '16 banks'. $70-$77 plus $0B-$0F is in fact 13 banks (104 KB), and art needs 5 (35.9 KB).
- ExGrafix: fortress's per-screen attribute data (about 35-40 SUPER screens × 1 KB) is not budgeted anywhere.
- CHR: 112 KB reserved against art's 106 KB.
Adding the plans up gives about 600 KB of demand against 552 KB of clean space (512 KB new + 40 KB in $0B-$0F), before any code-size check. 4MI filled 1 MB to 97%.

**Evidence.** tech §1.2 table ($46-$49 text, $64-$6B tilesets, $6C-$6F layouts, $70-$77 music); story §10.4; art_audio §2.2 ('10 new 8 KB banks (80 KB) for 30 slots') and §12.8 ('≈ 35.9 KB in 5 banks').

**Recommendation.** Have tech own a bank ledger from M0, with per-bank usage printed on every build. Reallocate:
- music down to 5 banks;
- text up to 10 banks, with dictionary compression made Must;
- layouts up to 8 banks;
- tilesets per art.
Store ExGrafix as a per-metatile extended-attribute table (about 1 KB per tileset) derived at paint time, not 1 KB per screen. Consider writing the 8 new venue layouts over vanilla layout banks $32/$33 (GP data, not Capcom art), which frees 32 KB. Re-total against 1 MB with code estimates per subsystem.

### feasibility-14. [MAJOR] systems.md, tech.md, fortress.md · systems §2.2 SUPER (form 3), §3.0 ('$E130[form*8 + $94] is opened for forms 1-3'), §11 Break Man ('Rock beams out; Break Man beams in'); tech §7.2 family $FC 'Break Man: the tag partner body'; fortress §4.5.2 (Dark Man uses 'the tag partner's own Break Man sprite set')

**Issue.** Two new player variants have no engine audit.
- SUPER as $9B = 3: about 30 executed-code readers of $9B index tables sized for 3 forms. An example is $3F:$E105 'LDY $9B / ADC $E115,Y', whose 3-entry table runs straight into $E118, so form 3 reads the next table. systems lists only 3 of these sites.
- Break Man: tech files him as a separate object family ($FC). As a non-slot-0 object, every player-only routine would have to be rewritten: camera follow, screen exits, ladders, shutters, pickups, contact damage $38:$8F72, pits and spikes, scripts that wait on the player's position. systems meanwhile describes a body swap.
- Dark Man 'costs no art' only if Break Man's 113-tile player sheet is re-packed into the 96-tile enemy area. art_audio's 40-tile copy is the real cost.

**Evidence.** A heuristic scan finds about 30 zero-page $9B reads in code banks $30/$38/$39/$3B/$3E/$3F (20 in $38). $3F:$E105-$E10C disassembly as quoted.

**Recommendation.** - Audit the $9B readers as the $51 audit did: a static scan plus coverage, then relocated tables with a 4th (SUPER) row.
- Implement Break Man as a slot-0 'character' variant: a character byte, his own physics constants, stashed HP and his sheet streamed at beam-in. Drop family $FC.
- Budget the Dark Man disguise as a 40-tile enemy-area set (art_audio §6).

### feasibility-15. [MINOR] fortress.md, tech.md, venues_a.md · fortress §5.3.2 (16 floor bands of 4 lines), §2-§3 E3 lobby ('two palette bands'); tech §8.1 (16 bands per buffer), §8.3 'RL_SHIMMER(line, n) | 1 + n', §8.4 rules 1-2

**Issue.** The raster list runs out of room or breaks its own rules in four scenes.
(a) W3: 16 floor bands, plus the pop-up open/close bands, plus the line-8 ExRAM flush, make 19 or more, against a 16-band buffer. The compositor would drop the commentator lines.
(b) RL_SHIMMER as tabulated (1 + n with vanilla's n = 20) needs 21 bands. It must be a self-re-arming OPS b6 routine, as §8.2 says.
(c) The E3 lobby wants red at the top and green at the bottom, which takes two mid-frame palette swaps. Only the last band may turn rendering off.
(d) The 'sound in the first band' rule can put a ~3,700-cycle (~33-line) sound update into the line-8 flush band, which delays any top pop-up band.

**Evidence.** tech §8.4 rule 1: 'Rendering-off writes end the list'. Vanilla handler F repeats 20 times (E sets $0678 = 20).

**Recommendation.** - Size the buffers at 24 bands, or plan W3 at 12 floor bands.
- Define RL_SHIMMER as 2 entries.
- Do E3's cellophane with BG attribute palettes, not raster swaps.
- Rule that the compositor puts OPS b5 (sound) on a band followed by ≥ 36 band-free lines.

### feasibility-16. [MINOR] art_audio.md vs fortress.md · art_audio §6 MODE-7 Machine ('near 192x96 ... 340 over 3 sizes (24 / 96 / 220)'; 'the boss gets the other ≥ 150 BG ids'); fortress §5.3.2 ('S 64 px, M 112 px, L 160 px wide')

**Issue.** The near pose (220 tiles) cannot share the 256 BG ids with the arena (≤ 100 by art's own rule), the checker floor and a glyph window. The two docs also disagree on the sizes.

**Evidence.** 220 + 100 > 256; fortress L = 160 px vs art near = 192 px.

**Recommendation.** Adopt fortress's 160-px L size with a ≤ 150-tile budget. Blank the castle background during the near phase, and give no glyph window there (it is ExGrafix-free per the blocker ruling).

### feasibility-17. [MINOR] art_audio.md vs tech.md vs fortress.md · art_audio §2.2 slot table; tech §1.2 ($64-$6B, 2 slots per bank) and §5.2 (RAM image with an independent ALT_SRC); fortress §0.1 notes (TS_STADIUM/ARCADE/LAB in $2B:$92/$2D:$92)

**Issue.** Three docs give three tileset plans.
- art_audio: 10 ROM banks of 3 slots; $2B:$92 for the credits, $2D:$92 for the lobby.
- fortress: the same two empty slots for TS_STADIUM, TS_ARCADE and TS_LAB, plus 'pages freed by moving the eight fortress layouts', which is wrong: layouts are not tileset pages, and tech keeps the legacy layouts.
- tech: 8 banks of 2.
Under tech's RAM-image loader, art's 'alternate-heavy stages must not share a bank' constraint disappears, because each stage names its own alternate-set source.

**Evidence.** As quoted in the three sections.

**Recommendation.** tech owns the placement: every stage row names its slot and alternate sources. art_audio and fortress list content and block counts only.

### feasibility-18. [MINOR] tech.md · §4.4 stage-attribute record (32 bytes, all used)

**Issue.** Other docs ask for fields the full 32-byte record has no room for:
- fortress: NO TAG per screen (the record has one stage bit), an OWNED override, ERA, crumbling collision group and the Knight ceiling elsewhere;
- venues_a: a separate secret-exit flag and plate-drop object;
- meta: the meta index (present);
- systems: boss row and scoring boss (shared in one byte).

**Evidence.** §4.4 offsets $00-$1F all assigned; fortress §9.1 requests.

**Recommendation.** Widen the record to 48 bytes, or add a per-stage extension pointer. Give NO_TAG a 32-bit screen mask.

### feasibility-19. [MINOR] venues_a.md, fortress.md · venues_a §0.2 ('moved into the stage-attribute table [engine-ok]'); fortress Semifinal 0C ('[engine-ok] gust reuse'), §5.2.1 ('[engine-ok] data + [new-code] S'), H5 01-02 low gravity '[engine-ok]' (needs bubble suppression)

**Issue.** Several items are tagged [engine-ok] but depend on new code: the stage-attribute table, VA-GUST, the fight loader and hub snapshot, and suppressing water bubbles.

**Evidence.** BRIEF §8: [engine-ok] means vanilla as-is or data only.

**Recommendation.** Retag these as [new-code] with their real sizes; W2 §5.2.1 is M.

### feasibility-20. [MINOR] fortress.md, art_audio.md · fortress §5.0 POCKET ('sprite priority behind BG ... emerge from the black'), SUPER 'foreground pillars'; art_audio §8 E4 ('4 Met-ghosts ... in four ghost palettes')

**Issue.** These effects run into NES sprite limits.
- Per-object behind-BG priority needs an override hook in the OAM builder, which is 23% of the frame and untagged as new code.
- Behind-BG sprites still show over BG colour 0, so pillars only work on colour-0 backgrounds.
- Only two enemy sprite palettes exist per screen (art §3.2), so four ghost palettes cannot be on screen together.

**Evidence.** art_audio §3.2: 'Sprite palettes 2-3: the screen's two enemy palettes'.

**Recommendation.** Tag the OAM priority override as [new-code] S in tech. Draw POCKET borders with opaque, non-zero colour tiles. Give the ghosts 2 palettes plus shape differences, or cycle one palette.

### feasibility-21. [MINOR] tech.md, art_audio.md, meta.md · tech §14.2 allocator seed '$36:$BE3F-$BFFF', art_audio §12.6 (Must SFX in the $36 tail); art D12 DPCM vs tech C-window; tech §14.5 / meta §7, §9.6 (SELECT+START); tech §1.7 handler 0 'delete' vs meta §9.5 VAULT

**Issue.** Smaller collisions between docs:
- The 449-byte sound tail is both a general allocator seed and art's home for the Must SFX.
- DPCM samples need a stable $C000-$FFFF mapping, but the C-window switches $C000.
- In DEV builds SELECT+START means three things: respawn here, open EXTRA CONFIG on the title, frame step.
- tech deletes IRQ handler 0, which the bank-$28 debug sound player uses, and meta's Museum VAULT launches that player.

**Evidence.** Verified: the $36:$BE3F-$BFFF tail is 449 bytes of 00/FF.

**Recommendation.** - Reserve the $36 tail for SFX only.
- Keep DPCM (Could) samples in $7F or drop them.
- Give each DEV combo one meaning.
- Keep handler 0 as a preset, or have the vault set up its own band.

### feasibility-22. [MINOR] tech.md · §1.4 helper replacements

**Issue.** The new helpers leave different values in A:
- $CBAF now returns A = bank ^ $80 (vanilla A = bank);
- $CBC0 returns (bank+1) ^ $80 (vanilla A = 7).
Any caller that uses A after the call breaks silently.

**Evidence.** Replacement code as listed in §1.4.

**Recommendation.** End each helper with a re-EOR (or LDA of the shadow) so A matches vanilla, or have shadow6 coverage prove that no caller reads A.

## Decisions needed (13)

1. **Which stage-id map is binding: tech §4.2 (legacy Mr. X/Wily at 8-15, H/W at $16-$1D) or fortress §0.1 (H/W reuse 8-15)?**
   - Options: A) tech's map; B) fortress's map
   - Recommended: A, tech's map. All 45 $51 readers are rewritten in M2.1 anyway, and legacy 8-15 keeps the vanilla regression suite, Mr. X Returns, the '???' vanilla-Wily-4 fight and the 1993 CUP loadable.
   - Affects: tech, fortress, meta (fight table), story (STORY_BEAT gating)

2. **What is ExRAM for?**
   - Options: A) Text-window nametable (mode 0) everywhere, with ExGrafix only in locked rooms that show no text; B) ExGrafix across W1-W3, with a separate text fallback in those stages; C) no ExGrafix
   - Recommended: A. W2 and W3 get palette, parallax and MMC5-audio 'SUPER colour'. ExGrafix is limited to W1's 16-bit section and the METALL 16 arena, filled in mode 2 while the screen is blanked. Drop the 'extra 4 KB CHR page'.
   - Affects: tech (D6/D7, §3.3, §11), fortress §5, art_audio §2.7, story (W1-W3 lines)

3. **Which text model and sizes?**
   - Options: A) Glyph cache for pop-ups (2 × 28 cells, ≤ 24 ids, ALL CAPS) and 4 × 28 dialogue; B) tech's VWF canvas (2 × 16 tiles pop-ups, 3 × 26 dialogue)
   - Recommended: A. Restore borrowed tiles from ROM instead of reading them back, and run TALK as a yielding coroutine outside the C-window.
   - Affects: tech §11, story §10, art_audio §3.5/§9.6, meta §4

4. **Should the punch be re-classed to $22-$24 for scoring?**
   - Options: A) Keep vanilla attack bytes and score from LATCHSRC; B) re-class and patch every latch-compare site
   - Recommended: A. It avoids patching about 21 enemy-AI sites.
   - Affects: systems §2.2/§6.4, tech §7.7

5. **Does a frozen object (Time Stop, Ice Block, stagger) keep taking damage?**
   - Options: A) Yes, through a per-type or per-sub-id frozen handler, with everything else NOFREEZE; B) no, damage waits until unfreeze (tech's current text)
   - Recommended: A
   - Affects: systems §4.8, tech §7.7, venue docs' NOFREEZE lists

6. **How is the lag budget counted, and what is it?**
   - Options: A) Every occupied slot (player, script, directors, shots) ≤ 9 until M3.8 measures the gain; B) keep the docs' current conventions
   - Recommended: A
   - Affects: tech §6.3/§15, venues_a, venues_b, fortress set-piece caps, artcheck

7. **What form-swap timing does SYS-CTL-4 promise?**
   - Options: A) 16-20 frames behind the flash, with an M1 spike to try 256 B/frame; B) keep 12 frames, which needs 32 KB CHR-RAM and so re-opens BRIEF §7.1; C) keep the vanilla cutscene
   - Recommended: A. Keep 8 KB CHR-RAM.
   - Affects: systems §1.3, tech §15.3, art_audio §2.6

8. **How is Break Man implemented?**
   - Options: A) A slot-0 character variant; B) a separate object family $FC
   - Recommended: A
   - Affects: systems §3.11/§11, tech §7.2/§7.9, fortress (Dark Man, W3 gift)

9. **Which slots do persistent player-side objects use?**
   - Options: A) Shots in 1-3, one GP utility each in 4-7, with caps per weapon set to fit; B) take enemy slots through gp_spawn
   - Recommended: A
   - Affects: systems §3, tech §7

10. **Who owns the ROM bank ledger, and how is it rebalanced?**
   - Options: A) tech owns it: music 5 banks, text 10 with compression Must, layouts 8, tilesets per need, ExGrafix stored per metatile, GP venue layouts allowed over vanilla $32/$33; B) keep the current §1.2 map
   - Recommended: A, with per-bank usage reported on every build from M0.
   - Affects: tech §1.2/§12.4, story §10.4, art_audio §13, fortress §5

11. **Where does the WORK RAM overflow (about 1-1.8 KB) go?**
   - Options: A) Move the unrolled copier to ROM and restore dialogue tiles from ROM; B) go to 64 KB PRG-RAM (no matching official board; emulator and flash-cart support uncertain)
   - Recommended: A
   - Affects: tech §3.4/§11/§15

12. **How do W2 bouts and GP Rush fights warp?**
   - Options: A) Clear $0340/$0650 on every stage change, plus a 'return-to' snapshot and a FIGHT_CTX that overrides the venue's clear, death and save paths; B) as written
   - Recommended: A, with W2 §5.2.1 retagged [new-code] M
   - Affects: tech §4.5, meta §9.2, fortress §5.2

13. **How big is the raster list?**
   - Options: A) 24 bands per buffer; B) 16 bands, with W3's floor at 12
   - Recommended: A (it is cheap: 8 arrays × 48 B)
   - Affects: tech §8, fortress §5.3
