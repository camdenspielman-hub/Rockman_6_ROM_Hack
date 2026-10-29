# Cross-document dependencies and open questions (design round 1)
Collected from the eight section designers' returned results, for the review phase. Each item names the doc that raised it.

## design-meta (docs/design/meta.md)

### Key decisions

- Saves are 3 files plus a system block in PRG-RAM page 0. Each block keeps A/B copies that ping-pong: every write goes to the older copy, so the newest good copy is never touched. Each block ends in 4MI's checksum (sum16, XOR, even/odd XOR, inverted copies, mix) plus a version, the generation and a COMMIT marker ($A5 $5A) written last. Every screen has a BROKEN DATA path, so there is no 4MI-style black-screen hang. Layout versions get migrations.
- The running game's file image (LIVE FILE, $7400) has exactly the save format, so a save is just checksum + copy. Full byte maps are given: FILE block (512 B: progress, secrets, inventory, chips/PARTs, rating flags, 24 per-stage records with best PAY, preset badge and TURBO asterisk, totals) and SYSTEM block (1 KB: config, unlocks, achievements, lifetime stats, TA/Rush records, MY GP setups, rules sticker book, venue mini-records). A 32-byte TEST MAILBOX sits at $7A00.
- Autosave runs on NEW GAME, stage entry (the IN_MATCH unplug detector), every death, every clear, pit stop exit, game over, bracket events, the championship result, and system changes. A load always resumes at the bracket or the fortress map; GP saves per fortress stage, which vanilla never did.
- The bracket keeps the 3x3 shape with four portraits in their vanilla cells. The four Exhibition pairs (E1 Wind+Knight, E2 Tomahawk+Plant, E3 Blizzard+Flame, E4 Yamato+Centaur) meet as badges at the four inner crossings, in a pinwheel wired to the FINAL centre. A 13-node table replaces $3F:$F232. Controls: SELECT opens the PIT STOP (matching systems.md), B toggles the Exhibition layer. Badges go DARK, then HALF, then LIT as secret exits are found.
- Semifinal trigger: once popcount(venue wins) = 4 and the Semifinal is not cleared, the unbeaten frames are stamped POSTPONED and the centre becomes Bass β (Riot intro: Bass crashes the bracket screen). The pit stop and replays stay open, so there is no soft lock. A data-driven bracket event queue plays POWER (2nd win), JET (4th), the Riot, Break Man joining, badge lighting and BREAK MAN WALKS (doping).
- The judges' debrief is a 4MI predicate table per stage, run in descending systems.md SECRETS weight (exit, room, item, plate, then Gold and Platinum); tool-gated predicates never hide usable hints. Hints come in two tiers: A is a homage riddle (this doc), B is the venue owner's own hint verbatim, and it takes over from the third clear. Full EN hint list for all 8 venues using venues_a/venues_b's real secrets, plus requirement, scorecard and perfect lines.
- Medals derive from the best score and are never stored. HoF points are B1/S2/G3/P4 over the 22 stages, 88 at most, and they drive the global unlocks.
- Championship rating: CHAMPIONSHIP 40, TEAM 10 (Beat, Break Man partner), ROUTE 16, GEAR 12 (Eddie's chips 10 + Y-TURBO +2), MEDALS 9, FAIR PLAY 10 (no game over, under 3 h, no unplug), BONUS 5 (rival no-damage, Mr. X card, top seed). That lists 102, but TURBO costs Break Man's 5, so the real maximum is exactly 100: the 4MI Eddie arithmetic, built on systems.md's doping trade-off. Break Man gives the first-failed-test debrief, then TO BE CONTINUED.
- The unlock chain runs on global bits. 20 HoF: Museum + Records. 40 HoF: Exhibition Rules. The championship: Time Attack, GP Rush OPEN, Bass entrant. OPEN cleared: cups + ALL-STAR + KNOCKOUT. Any cup: MY GP, EXTRA CONFIG, TRUE GP. TRUE GP: the ??? name reveal and the Vault. All Gold + the Mr. X card: Mr. X Returns. DEV builds unlock everything.
- GP Rush has one fight table (48 ids by type, a run-order list with block markers, 10-byte records) and loads each fight in the boss's own arena via the vanilla warp ($51, $0684-$0686, $F0=2). One PLAYERS' TUNNEL lobby holds gift bits; the runner alternates lobby and fight steps. Courses: OPEN, 9 one-weapon cups, ALL-STAR, TRUE GP, MY GP, 1993 CUP, all with criticals off and drops none. The final ??? fight is 'MR. Y'S ???', which becomes 'DR. WILY (OBVIOUSLY)' after TRUE GP.
- One RULESET choke point (4MI lesson) is filled from the file's DIFF, the TA preset or the Rush course, ORed with the Exhibition Rules (12 bits: BUSTER ONLY, NO FORMS, ONE HIT, FAMICOM RULES, ICE AGE via $A7, MOON BOOTS via the water gravity, etc.) and the EXTRA CONFIG cheats.
- EXTRA CONFIG is the Must dev tool: a data-driven live-RAM field editor working on a never-saved scratch file. WRITE FILE marks a file EDITED: it keeps an asterisk and gets no achievements. The TEST MAILBOX (magic + checksum) lets harnesses boot straight into any stage, fight or bracket state, and stays in release builds.
- CONFIG is split. Global: language, announcer, text speed, flashes, shake, HUD timer, SELECT SWAP, 2P SHIFT, A/B swap, MMC5 audio. Per file: systems.md §13's difficulty group, with its preset values. 1993 is a NEW-GAME-only ruleset. Lowering below the start preset clears HARD_CLEAN for good.
- ENGRISH is a third language: a sparse override table over ~25 menu strings, letter-O digits mirroring vanilla's N0R/P0W, C.FLRSH, TIWNS in Records, and Break Man's 'YOU ARE REAL CHAMPION!' perfect line. It never touches story text, hints or help pages.
- Vanilla quirks are kept as features: a hidden working PASS WORD grid gag, the bank $28 debug sound player as a Museum vault exhibit, Mr. X Returns built on the untouched vanilla Mr. X Fortress 1, and TO BE CONTINUED after the rating.

### Cross-doc dependencies

- systems.md: adopted its doping trade-off (Y-TURBO from Mr. Y's booth, Break Man refuses, per-stage asterisk); meta scores it (rating T1/T7) and stores RATEFLAGS.DOPED plus the BREAK MAN WALKS event. Also adopted: SELECT opens the pit stop from the bracket; medal points B1/S2/G3/P4; best PAY and the C/N/H/93 badge per stage; TA and GP Rush with criticals OFF and drops NONE; its whole §15.1 save list (BOLTS cap 999, CHIPS_OWNED/EQ 16-bit, PARTS_GOT/USED, METALLS, WEAKFOUND, FORM_DEBUT, BASS_ADAPT, plates) placed in the FILE block.
- systems.md (amendment): meta stores the difficulty group per file, not in the system block as systems.md §13.1 says. The setting meanings, preset values and readers stay systems.md's.
- systems.md: chip id order and a chip-source attribute per chip (shop / garage / venue / TURBO) for rating T6; SECRETS weights (exit 3, room 2, item 2, plate 1) for the debrief order; kill attribution for PACIFIST and the VARIETY hints; scorecard rows for the generic hints; removal of vanilla's no-rematch beam-out; the RULESET fields it reads.
- venues_a.md / venues_b.md: their secrets are used as written, and their debrief hints are tier B verbatim. The debrief ORDER is meta's weight rule (exit → room → item → plate → Gold → Platinum), overriding venues_a's room → item → exit and venues_b's exit → room → chip. venues_b should add tier B lines for Yamato and Centaur. Each venue provides one mini-record for SYS VENUE_REC (Wind's SHOOTING DOWN %, Tomahawk's quick-draw time) and mid-boss fight ids $08-$17 with their arenas.
- Exhibition owner: pairs E1 Wind+Knight, E2 Tomahawk+Plant, E3 Blizzard+Flame, E4 Yamato+Centaur (both venue docs already agree); guest fight ids $18-$1B.
- fortress.md: BACK TO BRACKET on the Hall of Fame and Castle maps; saves per wing; one MR. X business-card pickup in H1-H5 (rating T14, Mr. X Returns unlock); SECRETS bits and pars for non-venue stages; fight ids $1C-$25; the ??? finale; Mr. X Returns' chair fight; whether W2's refight hub reuses vanilla Wily 3's tables.
- story.md: STORY_BEAT values; Break Man's join condition and his debrief voice (one hint per rating test); Kalinka as the per-stage debrief speaker; the Riot intro, Roll's adaptor hand-offs, the trophy theft, BREAK MAN WALKS and game-over lines; ENTRANT FILES boss-panel data; the attract crawl; Bass Mode line swaps; the Mr. X Returns premise; all JP text.
- tech.md: PRG-RAM size and the NES 2.0 NVRAM declaration; page 0 $6000-$7A1F reserved for saves, LIVE images and the mailbox (1.5 KB free at $7A20); work-RAM placement; a meta-index column in the stage-attribute table; stage ids for the fight table; keeping vanilla Mr. X 1's layout and tileset in ROM; the language hook and ENGRISH override table; the DEV build flag and mailbox handling in RESET.
- art_audio.md: the title logo, bracket nametable, badges, medal ribbons, POSTPONED stamp, Bass β and trophy portraits, judges' desk with the Mr. Y cut-out, pit-stop counter, booth sprite, file cards, participation ribbon, lobby tunnel, achievement plates, Museum meters, and the GP fanfare.
- Opening Ceremony owner: one extra players'-tunnel screen in the stadium tileset, to serve as the GP Rush lobby.

### Risks

- The tier A riddles and the Yamato/Centaur tier B lines (written from venues_b's gate matrix only) can drift from the final venue content. Mitigation: a per-id hint list, an M10 text pass, and a mailbox test scenario that screenshots every debrief.
- If work RAM shares PRG-RAM page 0, MMC5 write protection cannot be used. The ping-pong copies plus the commit marker are designed for this, but they need power-cycle testing on real hardware (EverDrive) before release.
- Save growth: about 150 bytes are reserved in the FILE block and about 200 in the SYS block. The layout can grow to 1 KB per file only before v1.0; after that, migrations only.
- Rating balance guesses: T11's 3-hour limit, SPEED KING at 1:30, and TOP SEED's strictness. Tune them against playtest saves.
- The doping trade-off's arithmetic depends on the tag partner, a Should. If Break Man is cut, the cost must move (proposed: into FAIR PLAY) and the 102/100 arithmetic must be re-checked.
- Exhibition Rules' TURBO doubles enemy AI and can blow the ~10-object lag budget. It stays Could, behind per-venue playtests.
- Post-game scope is large. Cut order: KNOCKOUT, Museum, Exhibition Rules, MY GP, courses beyond OPEN. Keep the kernel: saves, the bracket, the debrief and rating, EXTRA CONFIG and the mailbox, RECORDS 1-3, Time Attack.
- The 1993 preset's full promise (vanilla damage tables, forms that cannot fire) relies on systems.md §13.3's generated row set, a Should.

### Open questions

- Force the Semifinal immediately after the 4th win, or keep the POSTPONED lock (the doc's choice), which lets the player shop and replay first?
- Should RETIRE from an uncleared stage cost a life? The doc says no.
- Kalinka or Cossack as the per-stage debrief speaker? The doc picks Kalinka.
- Should Time Attack's regulation loadout include Break Man's call? The doc says no.
- Unlocks per file instead of global? The doc says global, as 4MI does.
- Should KNOCKOUT use a fixed daily seed so friends can race the same bracket?
- Can 1993 files earn unlocks? The doc says yes.
- If the tag partner (Should) is cut, where does the doping cost go? The doc proposes FAIR PLAY.

## design-systems (docs/design/systems.md)

### Key decisions

- SELECT modifier: hold SELECT + Up/Down cycles weapons, + Left/Right cycles forms; a tap (released within 15 f, no D-pad) toggles the last weapon; a filter after the joypad read at $3E:$C711 masks UP/DOWN while SELECT is held and masks a swapped direction until it is released, so air control survives. Controller 2 A/B/Left/Right/Up = pseudo L/R (default ON).
- Quick form swap: no cutscene; the form's difference tiles stream at 128 B/frame behind a 12-frame swap flash; no i-frames; 20-f cooldown; the vanilla Rush-docking cutscene plays once per form per save. The vanilla reset to the buster ($38:$93F7) is removed.
- Measured vanilla: Robot Masters get 60 f of i-frames after any hit ($31:$9A01), fortress bosses 32 f ($05DF), normal enemies none; Rock gets 30 f knockback (14 px) then 60 f of blink; Jet pulsing cannot sustain altitude, so the overheat stall is dropped.
- Combat = two tables (4MI model, credited). Champions: weak 4/16 f (vanilla weakness cycle kept), good 3/20, neutral 2/30, resisted 1/45, own weapon 0-then-1/60, buster 1/60 (= vanilla), charge 3/60, punch 2/40, full punch 3/30, Super fist 3/40, parry 2/20, Break Man 1/40 and 3/40. G and R are permutations, so each weapon is W, G, R and own once each and N four times. Machines keep vanilla's 32-f base and the full punch does 4 to them.
- One lookup GP_BOSSHIT(row, col) replaces $31:$997D's class table, the $9AD6 punch special case and the 60-f constant, plus $3F:$EF64. Cells are 1 byte: damage bits 0-2, i-frame class bits 3-6, WEAK bit 7 (about 470 B). The chart is generated from the data. Special cases SC1-SC9 are in visible code (Knight's shield, Centaur ignores Time Stop, own-weapon joke reactions, Gamma's head takes fists only, Bass β's adaptive armour, the Yellow Devil SELECT trick, Tomahawk's quick-draw free hit, venue weak reactions).
- Forms fire every weapon. Synergies: Power = Y.SPEAR Pogo, F.BLAST Burning Knuckle, KNIGHT.C Morning Star, C.FLASH Time Fist; Jet = W.STORM Tailwind, B.ATTACK Snow Bomb, PLANT.B Petal Storm, SILVER.T Dive Throw. Alts (UP+B or hold): Wall Spear, Updraft, Ice Block (encases an enemy as a platform), Flare, Petal Shot, held mace that carries pickups, Feather Fan, Time Stop. C.FLASH also lights dark rooms.
- Slot 9 (vanilla BEAT) becomes MAGNET BEAM (H1; up to 3 beam platforms; magnet alt). Beat becomes the pit rescue once B-E-A-T is complete (4 HP, from HP 5 or more, no life lost). Each plate adds a chip slot (2 to 6).
- Super Adaptor: Normal walk and jump plus a once-per-airtime hop ($FC.40, about +28 px) and a 45-f rocket fist (5 px/f out to 112 px, then a homing return that hits on both legs); no gauge, no synergies.
- Attribution: player shots re-classed so class nibble = scoring category (1 buster, 2 punch, 4 hazard, 5-C weapons, D Magnet Beam, E Break Man). Every latch store also writes LASTHIT and LATCHSRC to WRAM (the victim clears $056C). Death convergence points ($30:$81C7, type $25, $3F:$ED42) OR the class into CATS. Boss hits count too.
- Scorecard: TIME = 20 at or under par, falling to 0 at 2× par; DAMAGE = 20 − ceil(HP lost / 3) − 4 per death; VARIETY = floor(25 × min(categories, Pv) / Pv) with Pv = min(5, owned); SECRETS weighted (exit 3, room 2, behaviour item 2, plate 1); STYLE = weak or form finish 4 + boss no-hit 4 + no tanks 2 + up to 5 acts. Medals 40/60/80/95, bonus 0/10/20/40/60, replays pay the improvement only. Par = 1.25 × the golden-movie route.
- Economy has no grind: bolts come only from scorecards, sponsor envelopes (30), Exhibition prizes (100) and venue prizes (once per save, at most 60 per venue); none drop from enemies. Typical full game about 2,560 bolts, completionist about 4,640. Shop: E-tank 40 (hold 4), 1UP 30, W-tank 50 (new), 7 chips totalling 1,010, Racing Colours 150 each; stock unlocks at 0/3/4/6/8 wins.
- 21 chips: 7 shop (Shock Absorber, Spike Guard, Charge Kit, Jet Tuner, Exchanger, Afterimage, Energy Saver), 4 garage (Iron Helmet, Thermos, Bird Seed, Glider), Energy Balancer (found, vanilla room 1C), 8 venue behaviour prizes with effects fixed here (Yashichi, Kaishin, Sheriff Star, Auto Recover, Snow Chains, Fireproof, Centurion, Daruma), and Y-TURBO. Each has an EN help page; some are cryptic on purpose.
- RM6-native crafting: vanilla's thematic one-shot tables become PARTs. Each venue's featured enemy dies outright to its champion's weakness weapon (an in-stage tell for the boss) and drops a PART once per save; Eddie's garage makes Rush, Beat and tank chips from PART pairs.
- Moral trade-off: Mr. Y's booth trades any PART for Y-TURBO (+1 boss damage, double-speed charge). The PART is lost forever, Break Man refuses to partner you, medals earned with it equipped get an asterisk, and the ending headline changes. The debrief never hints at it.
- Break Man: 20 HP, once per life from the pause menu (SELECT), START swaps back with Rock's HP kept; retreats at 0 HP with no life lost; buster only plus a Break Shot that breaks cracked blocks, an airborne shield, a higher jump (about 64 px) and double knockback (28 px). Tag gates carry his scarf emblem and lead only to optional content.
- Pickups (measured): small/large life +2/+10, weapon energy +2/+10; vanilla drops 31/256 of kills (mix 37/34/12.5/9.4/6.3%); weapon energy is not refilled on death. GP: an unusable weapon pickup becomes half-value HP, or goes to the lowest weapon with the Balancer chip. Drops NONE/LESS/NORMAL (40/256)/MORE. Respawn refill +max(4, half the missing) on NORMAL. E-tank heals 2× faster.
- Presets: CASUAL (×0.5 damage, 5 lives, E-tank floor 2, drops MORE, full refill, free guards), NORMAL, HARD (×1.5, drops LESS, no refill, poke lists + `BIT CFG_HARD` AI branches), 1993 (vanilla combat and forms, no chips, shop or bolts). Scores use the same formulas in every preset; records carry a preset badge.
- Normal routes never need a form, an alt fire, a synergy or Break Man; that keeps 1993 finishable and keeps the venues sequence-free.
- Criticals are a Could: rolled from the vanilla LFSR ($C88D), 1/128 base, ×4 at HP 4 or less; +2 damage on bosses, ×8 on mooks; forced OFF in Time Attack, GP Rush and 1993. If criticals are cut, KAISHIN falls back to a deterministic +2 on every 12th boss hit.

### Cross-doc dependencies

- venues_a.md / venues_b.md: normal exits never need a form, an alt fire, a synergy or Break Man; use floor type E where the Jet must not skip.
- venues_a.md / venues_b.md: each venue names one featured enemy family that dies outright to its champion's weakness weapon and drops that venue's PART (SNOW, GUST, SEED, EMBER, KATANA, FEATHER, CREST, SHELL).
- venues_a.md / venues_b.md: each venue provides its secret list with weights, a TIME par, one venue style act, one sponsor envelope per hidden room, prize-bolt placements (once per save, at most 60 per venue), HARD poke lists and AI branches, NOPARRY/NOFREEZE entries, and its WEAK and own-weapon reactions (SC4, SC9).
- venues_a.md: YASHICHI's effect changes to a once-per-stage full HP refill (no longer a last stand); KAISHIN = crits 1/16 or the deterministic EXCELLENT MOVE; SHERIFF STAR = +20% on payouts; AUTO RECOVER = +1 HP per 30 f after 60 f idle; Tomahawk's quick-draw free hit = 3 damage, 30 i-frames (SC8); Knight's shield break may be permanent for the fight (SC1); the Energy Balancer is a chip in room 1C.
- venues_b.md: weakness i-frames are 16 f, not 8; B.ATTACK's alt is their Ice Block, merged with an encase effect; Y.SPEAR's tap stays single with one pierce; C.FLASH lights dark rooms for 240 f; Pogo, Wall Spear, Burning Knuckle and Time Stop as they proposed; SNOW CHAINS, FIREPROOF, CENTURION and DARUMA effects are fixed in §9.2; plates are pickups; objects that react to a charged shot test for the attack byte $13.
- fortress.md: the placeholder rows in §4.5 (Grand Pi-kun, Bass β, Yellow Devil/Mecha Dragon/Gamma/Cossack Catcher/Dark Man MK-VI, W3 machine and Capsule, Exhibition guests, mid-bosses); SC5 Gamma's head takes fists only; SC6 Bass β's adaptive armour with the saved byte; SC7 the Yellow Devil SELECT trick; Magnet Beam from H1 and the Super Adaptor from H3; the W2 rush uses the champion tables including own-weapon cells.
- story.md: the Break Man join beat; the Mr. Y booth beat and the TURBO consequences (refusal line, CAPCOM TIMES variant); announcer lines for EV_WEAK_FIRST, EV_RESIST, EV_IMMUNE, first parry and first synergy, TIME STOP, crits, close calls, Break Man's call and retreat, new forms, medals; JP text for every weapon and chip help page.
- meta.md: its draft cites my early draft. CHIPS_OWNED and CHIPS_EQ must grow to 24 bits (21 chips, §9.2 order); T6 '7 bought + 4 crafted' still holds with new names; T5 = §9.2 rows 13-20; the METALLS counter and DOVE flag are no longer used. Also: medal points B1/S2/G3/P4, results screen and Pit Stop/garage UI, preset badges and asterisks, the debrief predicate list shared with SECRETS, Time Attack and GP Rush with criticals OFF and drops NONE, Exhibition rewards as fixed prizes rather than chips. Its per-file difficulty bytes and ANNOUNCER = DEATHS ONLY are accepted.
- tech.md: VBlank budget for CHR streaming (128 B/frame assumed); whether vanilla reads joypad 2 ($41/$43); the frozen tick in the object loop $3F:$E438 with a 256-entry type → damage-routine table; LASTHIT/LATCHSRC/REHIT/FREEZE arrays in WRAM; stage-attribute fields (boss row, scoring boss, par, secret list, NO TAG); the HARD poke-list format; the death-hook audit of custom death paths; the hook-site list in §15.1.
- art_audio.md: form difference tiles (target 64 or fewer per form), swap flash (2 tiles), WEAK!/CRIT!/?! pop (about 8 tiles), 8 PART icons, token/envelope/W-tank icons, alt-fire tiles listed per weapon, Super Rock and Break Man sprite sets, Racing Colours palettes; SFX (cycle tick, swap, parry ting, weak crunch, pikoon) and Break Man's whistle jingle.

### Risks

- The CHR streaming budget: if a form differs by close to vanilla's 2,048 bytes, the swap flash becomes 16-20 frames and VBlank may be tight on scrolling frames.
- Code volume: forms × weapons × alts × synergies is about 24 new behaviours plus the frozen tick, parry and attribution hooks; the largest systems item.
- Lag: lingering hitboxes, frozen enemies that are still drawn, Time Stop and the Centurion object press on the ~10-object budget.
- Balance: 16-f weakness i-frames may be too fast with multi-hit weapons, and staggers could lock some patterns; everything is one table byte and is tuned at the M4 gate.
- Attribution holes: custom death paths (gorilla tank, Mr. X 1 riders, new enemies) may skip the death hook and silently under-count VARIETY.
- A wrong entry in the frozen-tick type → damage-routine table makes an enemy immortal or fragile while frozen.
- Time Stop vs bosses whose logic runs in the IRQ (Knight's ceiling, Centaur's tide, the Wily Machine floor): they keep moving unless their handlers also check the stop.
- The doping trade-off is permanent and may feel unfair, though it is optional and double-confirmed.
- The 1993 preset doubles the test matrix.
- The economy may be too rich (about 2,560 typical bolts against 1,010 of chips plus 600 of colours).
- Chip bloat: 21 chips against the brief's 'about 14' after the venues added 8; the first cuts would be Afterimage and Glider.
- Break Man needs a full sprite set (art L) and is a Should; the scoring hooks degrade cleanly without him.

### Open questions

- Does the player's F.BLAST already ignite oil in vanilla, or only Fire Telly drops and enemy flames?
- How many sprite tiles really differ between the Normal, Power and Jet sets in bank $01?
- What VBlank budget is left beside the column paints on a scrolling frame?
- Does any vanilla code read joypad 2 ($41/$43)?
- What are the vanilla Plant Barrier's duration and radius (needed to tune Petal Storm)?
- Should VARIETY count boss hits (current proposal) or kills only?
- Should TURBO stay permanent, or be returnable to Mr. Y at a cost?
- Is Break Man's free retreat too generous, versus losing the call for the rest of the stage?
- Are Exhibition rewards chips or fixed prizes (proposed: fixed prizes)?
- The Mr. X 1 riders' charged-buster damage: measured 1, but the code predicts 3; it matters if fortress.md reuses them.
- Do criticals ship?
- Is the pause-menu weakness star too much hand-holding next to the featured-enemy tell?

## design-art-audio (docs/design/art_audio.md)

### Key decisions

- Measured, not guessed: in play the sprite table is player $00-$70, weapon shots $71-$7F, common $80-$9F and a 96-tile enemy area $A0-$FF. 223 of the 256 CHR set ids are used and 33 are free. 1,126 gap tiles are free outside banks $0B-$0F. On a vanilla screen the enemy area has a median of 62-93 free tiles, and the boss sets fill it (Wind, Yamato and Knight have 0 spare). The title uses 252 BG tiles. Vanilla flicker: stages stay at 8 or fewer sprites per line, bosses peak at 9-13. Music data is 18,788 B with 449 B free.
- CHR set table v2 (Must, built by tech.md): 5-byte entries with an 8-bit source bank, so banks above $3F are reachable. Global ids $00-$DE plus GP globals $7C-$7F and $DF. Ids $E0-$FB (28) are stage-local, resolved through the stage-attribute table. AI-header bytes, exit bytes and checkpoint bytes all stay one byte.
- Tileset slot plan: 10 new 8 KB tileset banks give 30 slots. Each venue gets its own bank with its own alternate metatile set. Slot $89 holds the venue's second section, through a Should exit-driven 'section switch'. Slot $92 hosts an Exhibition, the Opening, the Semifinal, H5 or W2. Two shared banks hold H1-H4, W1 and W3. The 2 empty vanilla slots go to the victory-lap credits ($2B:$92) and the GP Rush lobby ($2D:$92). Vanilla tables stay untouched.
- New BG art enters only as swapped-in thirds proven safe by a per-screen free-id map. Every venue's new sprite sets have fixed enemy-area addresses, and I checked them against the vanilla enemy sets that share their screens. For example, Tomahawk's cowboys ($6C, A0-CF) stay out of the town, and Yamato's samurai ($A2, all 96 tiles) gets nothing new beside it.
- The form swap streams the whole 2 KB sheet: 109-114 of 128 tiles differ per form, so systems.md's target of 64 tiles or fewer cannot be met. That is 16 frames at 128 B/frame or 8 at 256 B/frame. I recommend an unrolled VBlank copy and one stream at a time.
- WEAK! costs only 3 new tiles (W, K, !) because E and A already exist in the READY letters ($99-$9D) of the common row. CRIT! and ?! add 4 more. They go in a GP-COMMON copy of set $01, in 6 never-drawn slots that a full-game OAM census must confirm first.
- New champion frames go in a 16-24-tile pinch set, streamed during an invincible beat that already exists in each pattern. Each boss set is rebuilt so phase 1 fits in 96 tiles.
- Big bosses are BG art reusing vanilla code: Yellow Devil MK-VI on X Crusher or the Wily Machine floor split, Gamma on Mechazaurus, Cossack Catcher on Metonger Z, Mecha Dragon on the Wily Machine. Dark Man is a sprite boss whose disguise copies 40 tiles of Break Man with the scarf one shade off. The MODE-7 Machine drives toward the camera in 3 sizes streamed into CHR, CX's giant-Light technique.
- Cheap reuse is part of the plan: Mr. Y is vanilla Mr. X's sprite plus a moustache and a 'Y' pin. Shadow Rock is a dark palette. Metal Metslime is a grey palette. Maze Man's ghosts are Metalls in ghost palettes. Grand Pi-kun's costume head pops off to show a Met. The title keeps the vanilla logo and moon, adds a 'GP' sprite badge, and turns 戦い into グランプリ.
- In-stage commentator pop-ups never show a full portrait. They use a 16x16 face icon in sprite tiles, and their distinct glyphs (18-26) go into free BG ids found by a build-time free-id map. If a screen has too few free ids the line is deferred. Boss rooms always have room. Menus use a pattern-table split so the rows below a line read BG tiles from the sprite table.
- Art totals: 6,793 new tiles (4,508 BG + 2,285 sprite) and 573 metasprite frames. Must is 4,851 tiles and 421 frames. That is about 106 KB of CHR in 14-16 banks, plus 3 sprite bank pairs. Human workload is about 890 h (about 660 for Must). A human pixel artist does 1,368 BG tiles and 419 frames; Claude drafts or generates 3,140 BG tiles and 151 frames. Everything starts as a placeholder.
- Music policy: the vanilla stage and boss themes stay. There are 37 new compositions (51 track ids, 27.5 KB): 5 Must (G00 GRAND PRIX MARCH, G01 fanfare, G02 judges, G03 medal stamp, G04 Bass β theme, 3.0 KB), 24 Should and 8 Could, plus 2 MMC5 layers. Every new track has a vanilla fallback id. Homages are evoked, never quoted. The exceptions are the public-domain Korobeiniki (E1) and Kalinka (Kalinka's own sting), and Capcom's own Rockman 1-5 music for the Hall of Fame and Break Man's whistle.
- Sound driver work: D1 per-track bank byte, D2 a 240-id table, D4 the MMC5 port and D11 multi-entry songs are Must. D5, a second channel-interpreter instance for the MMC5 pulses, is Could and never ships without D6 (the hardware multiplier, since the driver is already 18 % of the frame). D7 puts the charge sound on MMC5 pulse 1. D9 adds a channel mute mask (W1's tiers) and D10 a tempo override (E3's formation, Blizzard's countdown). DPCM drums and a voice clip are Could. Total new sound data is about 35.9 KB in 5 banks (Must + Should fit in 3). The ≈ 20 Must SFX fit the 449 B tail of bank $36.
- Pipeline: chr.py round-trips every vanilla CHR set first. sprites.py compiles metasprite JSON into Capcom's exact frame/layout/animation format with layouts deduplicated. sprslice.py imports Aseprite strips. bgboss.py handles BG-boss poses, pose deltas, attributes, hit boxes and streams. artcheck.py checks enemy-area overlap, palette conflicts, the free-id map, flicker, stream budgets, that Capcom's art is untouched, and novelty ghost frames. mml.py compiles and decompiles music, with a byte-exact round trip of all 36 vanilla tracks as its first test. fms2mml.py imports FamiStudio. sndtest.py renders WAV and reports driver cycles.

### Cross-doc dependencies

- tech.md: the CHR set table v2 and stage-local ids $E0-$FB; 10 tileset banks plus the section switch; bank numbers for 14-16 CHR banks, 3 sprite bank pairs and 5 music banks; the X-GPOBJ sub-id to sprite-bank table; a VBlank CHR stream path at 128-256 B/frame, one stream at a time; raster-list entries for the menu pattern-table split and the MODE-7 road; whether $C000-$DFFF stays switchable (DPCM); WRAM for the second MMC5 channel block; driver items D1-D11; the ExGrafix spike; measuring a 32 KB CHR-RAM option.
- systems.md: the form swap streams the full 2 KB sheet (109-114 of 128 tiles differ), not 64 tiles or fewer; WEAK!, CRIT! and ?! cost 3 + 4 tiles via the READY glyphs; 21 chip icons and 8 PART icons at 16x16; alt-fire tiles live in each weapon's 15-tile slot $71-$7F; Break Man's sheet is Should; the SFX list; the whistle jingle G27.
- venues_a.md and venues_b.md: the enemy-area placements and conflicts of §4. Wind 01 has no vanilla enemy (WS1-3 fill all 96 tiles). Tomahawk's cowboys stay out of the town, saloon and train sets. Flame's dungeon has no Metalls and the 0B chandeliers live inside SET-FL1. Blizzard's count bombs stay off the Toppy screens. Yamato's samurai screens get nothing new. Centaur SET-CT1 sits at B0. The buster is the only weapon while on a vine or carried by the condor, because those poses share its weapon slot. Per-venue tile and frame counts; one Should set-piece music cue per venue, the rest Could; the vanilla stage themes kept.
- fortress.md: the non-venue stage art of §5 (Opening stadium, Semifinal, H-wing palette eras, W1 tiers, W2 hub, W3 core, credits, lobby); the BG-boss techniques and tile budgets of §6 (Yellow Devil on X Crusher / Wily Machine, Mecha Dragon on the Wily Machine, Gamma on Mechazaurus, Cossack Catcher on Metonger Z, Dark Man on the RM framework using Break Man tiles, the MODE-7 Machine with 3 streamed sizes); the music of §12.3.
- meta.md: the title (vanilla logo + GP sprite badge + new subtitle, menu under the pattern-table split); file cards, bracket art (vanilla portraits kept), badges, ribbons, POSTPONED stamp; the judges' desk with the Mr. Y cut-out; the pit stop; the lobby built from the Opening set; the museum sound test using channel meters (D9); the GP fanfare G01; MMC5 AUDIO in CONFIG; vanilla $0F stays as the bracket theme.
- story.md: 12 portraits and 6 in-stage face icons; in-stage pop-ups have no full portrait and may be deferred when a screen has fewer than 24 free BG ids; Kalinka's public-domain folk-song sting; Mr. Y is drawn as Mr. X with a moustache; match-card portraits for the BG bosses.

### Risks

- No pixel artist: Must art is about 660 human hours. Claude drafts would ship as final, and the characters, BG bosses and portraits would look amateur. Mitigation: placeholders first, composites from vanilla parts, and cutting the Should bosses first.
- 8 KB CHR-RAM is the real limit: pop-up glyphs need free BG ids that a full venue screen may lack, so commentary may be deferred.
- The form swap streams 2 KB (16 frames at 128 B/frame), heavier than systems.md hoped; it needs an unrolled 256 B/frame copy or 32 KB CHR-RAM.
- Champion pinch sets require rebuilding the boss sets; Wind, Yamato and Knight have 0 spare tiles, so some vanilla frames must be dropped.
- Sprite-set conflicts are tight in Blizzard, Flame and Tomahawk; a late layout change can break a screen, so artcheck.py must run from the first venue build.
- MMC5 audio is absent on an unmodded NES-001 and some flash carts; the 4-channel rule keeps every track complete and the MMC5 voices stay Could.
- Two more sound channels without the hardware multiplier would add lag (the driver is already 18 % of the frame).
- Arranging Capcom's RM1-5 music is fan-hack tradition but still Capcom's; all non-Capcom homages stay original, and only public-domain folk songs are quoted.
- ExGrafix on CHR-RAM may not be emulated everywhere; it sits behind a spike.
- Scale creep: 6,793 tiles exceeds 4MI's 5,266. The Must line of 4,851 is the plan, with a fixed cut order (Could, then Should bosses, W-HANGAR, T-BOOTHILL, AYACO BG).

### Open questions

- Can tech.md measure MMC5 with 32 KB CHR-RAM and CHR banking on FCEUmm, Mesen and flash carts? It would make form swaps, pinch sets and BG-boss poses 0-frame bank switches and allow in-stage portraits, but BRIEF §7.1 currently fixes 8 KB.
- Does $C000-$DFFF stay switchable under MMC5 (needed for DPCM drums), or is it fixed with the moved fixed banks?
- Will the project recruit a pixel artist and a composer, and for which tier? Must art alone assumes about 660 human hours.
- Do story.md and the venue docs accept deferred pop-ups on screens without 24 free BG ids, or must some lines always show? The weakness line is safe because boss rooms have room.
- Hall of Fame music: arrangements of RM1-5 themes (the current plan), or originals in each game's style?
- Is vanilla $0F acceptable as the bracket theme for the whole game?
- Do the venue designers accept the enemy-area placements of §4?
- What emulator and hardware matrix sets the MMC5 AUDIO default?

## design-tech (docs/design/tech.md)

### Key decisions

- MMC5, 1 MB by insertion: vanilla banks $00-$3D stay in place, new banks $3E-$7D, vanilla fixed banks $3E/$3F move to $7E/$7F. PRG mode 3. NES 2.0 header 4E 45 53 1A 40 00 52 08 00 00 90 07 00 00 00 01 (32 KB PRG-NVRAM, 8 KB CHR-RAM).
- Bank-id convention: $00-$7F is a ROM bank and $80-$87 is a PRG-RAM page. The ported helpers do EOR #$80 / STA $5114, so vanilla bank bytes ($6E, $6F, $0441) can point at RAM with no reader changes. FCEUmm probe confirmed RAM in the $8000/$A000/$C000 windows.
- The 'C-window': GP service code runs in a switchable $C000 window through a $7F stub (JSR CW / .byte n), so hooks never disturb the caller's $8000/$A000 banks. The NMI and IRQ vectors move to $7F stubs that restore $7E; C-window code never yields. Vanilla code banks $3E and $38 have 0 bytes of fill (measured).
- Full MMC5 port checklist with sites: helpers $CBAF/$CBC0/$CBDA/$CBE9, sound service $C8C1 (its $4C restore dropped), NMI CHR-copy bank $C7AD-$C7B4, sound reader $34:$804C-$8062, mirroring $C021/$38:$9295/$38:$95BA/$FFC9 (via a mirtab $44/$50), $E204/$E430 operand $3E->$7E, RESET $FF96 and $FFC9-$FFD9 replaced by mmc5_init. Gotcha found: $C51E halts unless $FFE0-$FFEF = FF and $FFF8 = $08, so the allocator must never touch those bytes.
- IRQ: literal port first (M1). Each STA $C000 latch L becomes an absolute line (IRQ_LINE += L+1 -> $5203), moved to the end of its handler; each STA $E000 becomes a $5204 disable; the entry ack becomes LDA $5204; both NMI arm paths ($C066/$C0C4) are converted. All 27 handlers are tabulated with the 15 latch and 12 disable sites. There are four logic-in-IRQ handlers (11 Knight ceiling, 14 Centaur tide, 19 Wily Machine floor, and 1A Mr. X 3, which the research summaries missed). In M2 that logic moves to an NMI-time irq_logic_tick.
- PRG-RAM is 32 KB, all battery-backed, in 4 pages: 0 SAVE (mapped only by the save module, at $A000), 1 WORK (always at $6000), 2 LAYOUT, 3 TILES. MMC5's write gate is global, so the save is protected by page isolation. A boot RAM probe shows an error instead of corrupting saves. FCEUmm gives 64 KB whatever the header says (measured), so Mesen must check the header.
- WRAM-resident layouts adopted (Must) as a raw 'RAM image of the ROM bank': same page layout, so $53/$63/$67 keep their meaning and the painters and collision ($D1FF/$D322/$D904/$DA6C) are unchanged. It enables map edits, T6, HARD/CASUAL poke lists (format given) and a separate alternate set per venue. Sections are Should (4 x 32 screens; exit targets $A0-$FF carry the section). LZ compression is Won't.
- Stage ids 0-31: venues keep vanilla ids 0-7; 8-15 stay legacy fortresses; $10-$1F hold Opening, Semifinal, E1-E4, H1-H5, W1-W3, credits and Mr. X Returns; $20 is a DEV-only sandbox. A 32-byte stage-attribute record (all fields specified) is copied to SA_CUR in WORK at init. All 45 $51 readers are tabulated with replacements, plus the 11 $063D readers (kept, with $063D = RM_SLOT). The 9 enemy-palette CMP specials become 'variant rows'. The stage-init hook rebuilds the RAM images whenever RAM_ID differs from the stage being loaded; this covers the YOU GET room's borrowing of stage 5 and meta's fight-table warps.
- Objects use families instead of single type ids: types $F4-$FF, each with a sub-id table. An init hook writes the real AI, bank and sprite bank into the slot, so dispatch costs nothing at run time. Object lists are copied to WORK in a v2 format (adds sub and arg arrays). Also specified: the metasprite pipeline (vanilla format), a static sprite-CHR conflict check, coroutine rules, a frozen tick, a latch-source hook, an LFSR, player states taken over through slot 0's resume address, exit type 7, T3 channels and the T8 multi-part boss library.
- Generic raster list: 2 x 16 bands, double-buffered by flipping a pointer, with the walker in $7F. A band whose palette swap turns rendering off must be last, because MMC5 stops counting lines then. Presets replace all 27 chains, and a band compositor merges stage, window and director bands.
- T1: T1-lite (fixed camera + time-scrolled bands + a deterministic wave director) is Must. A true forced horizontal scroll is Could, using the existing left clamp $A8 plus crush detection. Vertical autoscroll is Won't.
- T6: rewrite the RAM layout with authored variant blocks (metatile attribute bit 2 = DESTRUCT, plus a transition table) and repaint using the oil-ignition column routine $3E:$DE03-$DE5C. Collision updates on the next probe; refill and persistence rules are given. The per-cell bitmap (4MI style) is the fallback.
- Text: ExRAM in mode 0 serves as the window nametable, switched in by $5105=$AA from an IRQ band. Verified on FCEUmm: ExRAM showed from exactly scanline 120. FCEUmm lacks the $5204 in-frame flag, so ExRAM writes are flushed from a line-8 IRQ band. Glyphs are drawn into borrowed BG tile ids: the level build computes free ids per screen for live pop-ups, and frozen dialogue saves and restores the tiles it borrows. EN uses a CX-style VWF; JP is 8 px kana with dakuten composed into one glyph, plus optional kanji. The control-code set and the ENGRISH override table are specified, and full-screen text keeps the vanilla PPU-script engine behind a language hook at $3C:$8636.
- Sound: a 240-entry track table with a bank byte per track; the reader gains an $E000-$FFFF 'own bank' range; the hardware multiplier is reserved for the sound driver; the play-time clock ticks in the $C8C1 wrapper. An MML dialect maps 1:1 onto commands $00-$18 and is gated by a byte-exact round trip of the 36 vanilla songs. MMC5 pulses are a Could, via a second driver instance and companion streams.
- VBlank budget answered for systems.md: the CHR stream gets 128 B per frame normally, 64 B on column-paint frames, and 32 B with a full VRAM buffer (vanilla CHR copy measured at 16-64 B per frame, about 16 cycles per byte). Controller 2 is read but never consumed (coverage-checked), so it is free.
- Tooling: a hook registry (YAML, with original-byte, overlap and instruction-boundary checks), an allocator seeded with verified free ranges, BPS, movies made of inputs plus scripted RAM pokes (vanilla savestates cannot load into MMC5 builds), a test mailbox, shadow6 ported to MMC5 with coverage and profiling, and a 4-suite check.py. M0-M3 are rewritten as concrete task lists, with a table of what the research already finished.

### Cross-doc dependencies

- meta.md: the PRG-RAM page 0 map is kept as written; LIVE images move to page 1 at the same CPU addresses; test mailbox at page 0 offset $1A00; the EXTRA CONFIG UI sits on tech's warp, DEV flag and ring buffer; SA.META holds its meta index; its fight table points at engine ids (legacy $08-$0F); ENGRISH works as an override table; its difficulty bytes are read by IFHARD and the poke lists.
- systems.md: its hot bytes live at $06BD-$06C8 and its per-slot arrays at WORK $6000+; its hook sites go in the registry; VBlank stream budget is 128/64/32 B per frame; controller 2 is free; tech provides the frozen tick, latch source (LATCHSRC), LFSR and death-hook audit; game code must not use the hardware multiplier; stage fields FORT_COL, SCORE_ID, PAR, NO_TAG and KEEPWE are in the attribute record.
- venues_a.md: T1-lite is accepted; T4 runs through RL_BANDS (up to 6 bands plus the window band); T2 text window with YES/NO and menus; T3, T5 and the VA-* objects are built on families $F4/$F5 and GP player states; the Knight ceiling leaves the IRQ with parameters (EFFECTS/EFX_PARAM); two tileset slots per ROM bank, each with its own alternate set.
- venues_b.md: T6 is a layout rewrite with variant blocks (their bitmap proposal becomes the fallback); X-BONK is a ceiling-probe callback; X-GPOBJ means the families; ship, tide and ceiling become EFFECTS bits, and the tide dwell is EFX_PARAM; X-UPEXIT is exit type 7 after relocating the $39:$9A88/$9A8F table; X-FLOOR needs new collision groups (GRP_ROW) once M0.7 decodes the floor handlers; the ignition hook on $3E:$DDFC goes in the registry.
- fortress.md: ids $16-$1D and $1F; BG bosses use RL_FLOOR; legacy ids serve refights; T8 parts library; sections for any wing over 32 screens.
- story.md: the text control codes; pop-up limit is 2 lines x 16 tiles (~22 EN VWF characters or 16 JP); dialogue is 3 lines x 26 columns with a 32x32 portrait; speaker ids with blips; kana-only vs kanji decision.
- art_audio.md: 8 KB CHR-RAM with no banking; sprite input is PNG + JSON (vanilla metasprite format); fonts are 1bpp at 8 px; portraits are 32x32; the MML dialect; 16 music banks; MMC5 companion streams; tile counts per form.

### Risks

- Real-hardware and flash-cart support for MMC5 with 8 KB CHR-RAM and 32 KB PRG-RAM is unverified; 4MI's MMC5 build only proves it on emulators.
- FCEUmm is lenient: it always gives 64 KB of PRG-RAM, wraps CHR-RAM at 8 KB and lacks the in-frame flag, so some bugs only Mesen shows will reach the user late unless Mesen runs at every gate.
- IRQ calibration (the constant K and per-handler delays) may differ between emulators, so splits could shimmer by a line.
- ExRAM writes only count while rendering, so the window cannot change on rendering-off screens.
- On dense screens (Plant has 0 free BG ids) live pop-ups have to wait. A bug in dialogue CHR borrow/restore would corrupt visible tiles, so every dialogue screen needs a movie.
- Moving the IRQ logic out of the interrupt in M2 loses exact golden equality for Knight and Centaur; those two stages get behaviour-equivalence tests instead.
- WRAM layouts: a stray write corrupts the current stage. Mitigation: a DEV-build comparison of the RAM image against ROM plus the edit log.
- T6 variant blocks cost block ids on tilesets that are already nearly full; the bitmap fallback exists.
- Stage-id readers that the 139,200-frame tour never executed may exist; the M0.7 static scan is meant to catch them.
- Reassembling the sound driver for MMC5 pulses is delicate, which is why it stays Could.
- The text engine is size L and the Knight venue depends on it.
- Cartridge space: 4MI filled 1 MB to 97%, so per-bank usage reports are needed from day one.
- Vanilla savestates are unusable on MMC5 builds, so the whole test suite must boot and warp.

### Open questions

- fortress.md: does it need engine ids beyond $16-$1D and $1F? Which legacy ids ($09-$0F) can be reclaimed?
- meta.md: will it accept the LIVE FILE and LIVE SYS images moving to PRG-RAM page 1 at the same CPU addresses ($7400/$7600)?
- Commentator pop-up default position: top band (keeps floors and pits visible) or bottom (what venues_a and venues_b assumed)?
- Can a headless Mesen run in this environment for CI, or is it a user-gate tool only?
- Which real hardware or flash cart matters (Everdrive N8 Pro, PowerPak, none)?
- art_audio.md: how many tiles differ per form for the quick swap, and how many portraits?
- Does any venue need T1-full (terrain moving under a forced camera)?
- story.md: should JP dialogue use a small kanji set (about 1.6 KB of PRG) or stay kana-only like vanilla?
- Does any stage need more than 32 screens? That would move sections from Should to Must.
- When the fight table loads legacy ids 8-15, should they keep vanilla fortress rules?

## design-venues-b (docs/design/venues_b.md)

### Key decisions

- Venues keep their vanilla stage ids (Blizzard 0, Flame 3, Yamato 4, Centaur 7). The ship's and the tide's collision offsets are hard-wired to ids 0 and 7, so both set pieces keep working before the stage-attribute table lands. Yamato's borrowed Knight ceiling (stage-6 only) needs that table.
- Each venue fits one 32-screen layout: Blizzard 28, Flame 28, Centaur 30, Yamato 30. The main route counts up from 00; branches, secret arenas and the hidden room sit in the high screens. Each venue asks for its own 8 KB tileset bank, with its own alternate set at $9B-$9F.
- The four gates use four different kinds of challenge, and none of the four secret exits needs an adaptor. Blizzard: catch the condor in a 40-s bonus round (timing). Flame: don't fight your shadow, merge with it (behaviour). Centaur: the ZONE 100 door, open only at low tide (observation and timing). Yamato: carry three Goemon travel passes to the sekisho gate (collection). E3 and E4 can therefore open early.
- Hidden rooms: Blizzard's non-wrapping floor (tell: the seal walks off and doesn't come back); Flame's mouse that presses the plate if you wait 10 s; Centaur's ZONE 0 door, which glows only in the dark; Yamato's DuckTales trapdoor, opened by pogo-landing on the gold crest.
- Behaviour-gated chips (proposals for meta.md): SNOW CHAINS (never destroy a Toppy seal-bot; trade-off: they refill your holes); FIREPROOF (no oil ignited; trade-off: chandeliers are the easy way past the guards); CENTURION (free three petrified Centurions with a charged shot; they block arrows at the boss); DARUMA (win the daruma otoshi without hitting the head; the daruma paints its second eye; once-per-stage survive-at-1-HP).
- Plates E and T keep vanilla's Jet geometry exactly (the Yamato 0B ledge, the Centaur 112-px gap). They become altar pickups on sky routes that rejoin the main route, instead of second boss rooms. Vanilla's YOU GET text, C.FLRSH typo included, still plays.
- Yamato keeps the charged-punch bypass and the dark GAMARN & GAMADAYU room (twist: Gamadayu's fireworks light the room for 24 f). It adds the Jajamaru floor-bonk stun, revolving hanging scrolls (tell: they flutter), a nightingale floor that drives Knight's spike ceiling (sliding is silent), a T8 Daruma Otoshi, a DuckTales spear-pogo set piece (EXWP) and a kabuki revolving-stage secret arena (a scene swap through the $0340 alternate set).
- Each vanilla set piece gets one twist. The ship's rock turns drop icicles. Oil ignition becomes a permanent player choice: drop a chandelier to burn the guards and lose that floor for the visit. The tide gets a 60-f dwell, so it works as a lift (high-tide swim-jumps reach about 90 px against 52 on land) and as a lock (the ZONE 100 door).
- Every boss fight shows its weapon's alternate and synergy before the player owns it: Blizzard's flakes leave an ice block; Flame's pinch has a rising fire column and a flaming lunge; Centaur's time stop; Yamato's wall spears and pole-vault pogo. Each boss has a weakness reaction and a no-damage self-weapon reaction (snowman, ABSORB, SAY CHEESE, PARRY). Pinch modes: AVALANCHE, THE PALACE BURNS, the ABILITY UNKNOWN slot reel, HELMET OFF (MOBILE 31 becomes 99).
- Two new mechanics were measured in the emulator. Rockman's jump rises 52 px, so Ice Climber floors sit 48 px apart. The buster shot spawns 1 px above his centre (about 12 px above the feet), which is what makes 'shoot from the floor, never hit the head' the Daruma's rule.
- New shared mechanics proposed for tech.md: X-BONK, X-WRAP, X-UPEXIT (argued up from Could to Should, with a ladder-stub fallback), X-METER, X-LABEL, X-EXWP, X-FLOOR, X-GPOBJ, plus T3, T6, T7 and T8 from PLAN.

### Cross-doc dependencies

- systems.md: weapon proposals. B.ATTACK: ice-block alternate, Jet bomb synergy, freezes burning oil. F.BLAST: upward-column alternate, Burning Knuckle Power synergy, ignites oil, burns shoji. C.FLASH: time-stop alternate, Power x3 punch, lights dark rooms. Y.SPEAR: wall-spear alternate, the DuckTales pogo as its Power synergy.
- systems.md: four boss rows (weakness 4 dmg / 8 i-frames; others 2/30; buster 1/60), the four self-weapon reactions as visible special cases, the charged-shot rules for Centurion statues and skeletons, and whether the vanilla weakness cycle stays.
- meta.md: the chips SNOW CHAINS, FIREPROOF, CENTURION and DARUMA with their effects; four secret-exit save flags; plates as pickups; bolt values for vegetables and treasure bags; debrief predicate order and hint text; STYLE credit for self-weapon reactions; venue replays; par times (Blizzard 330 s, Flame 300 s, Centaur 300 s, Yamato 330 s).
- story.md: commentator hook ids BLZ-01..15, FLM-01..16, CEN-01..20 and YAM-01..20; 20 death lines; 13 debrief hints; the Mr. Y gag per venue; Roll's optional cameo line; JP kana versions.
- tech.md: T3 (switch/target, doors, gates, sekisho), T6 (per-position tiles), T7 (input mirror), T8 (multi-segment boss); X-BONK, X-WRAP, X-UPEXIT, X-METER, X-LABEL, X-EXWP, X-FLOOR, X-GPOBJ; the stage-attribute table (ship, tide and ceiling chains in any stage); one 8 KB tileset bank per venue; the tide dwell; an ignition hook at $3E:$DDFC; the ship thread's turn event for icicles; the reduced-flash option.

### Risks

- Object ids: about 46 new object kinds in these four venues alone, against 30-32 free type ids for the whole game. A generic GP-object type with sub-ids (4MI's $5E pattern) is mandatory and should be built first.
- T6 per-position tiles add a lookup to the painters and the collision read, which is about 20% of the frame. Mitigation: a per-screen flag so ordinary screens skip the lookup.
- The tide ($C3D8) and the spike ceiling ($C337) run game logic inside the IRQ. The tide dwell and the chirp-driven ceiling should wait for the MMC5 raster-list port. Fallbacks are documented: a 24-px tide window, sprite spike blocks.
- X-UPEXIT is a Could in BRIEF §4. Without it the Ice Climber climb and the Kid Icarus tower use ladder stubs, which feels less like the homage.
- Lag hotspots to profile: Flame 0B (three guards plus three chandeliers) and Centaur 11-12 (Reaplet alarms). All screens are planned at 8 or fewer objects, player included, shots excluded.
- Screen budgets are tight: Yamato and Centaur have two spare screens each.
- Fairness: a first-time player can lose FIREPROOF on screen 01 (the lesson gives a 120-f hover). SNOW CHAINS punishes the charged shot, so its tell fires on the first hit.
- The Toppy refills may make the climb tedious. CASUAL raises the refill delay to 600 f; the climb has a mid checkpoint.
- Flash-heavy moments (fireworks, C.FLASH, the merge, the black zone) must honour the reduced-flash option.
- New player graphics are needed: two pogo frames, and the eggplant curse (Could). They compete with form-swap CHR streaming.
- Text volume: about 70 commentator hooks plus 20 death lines for four venues. They need a priority scheme.
- In Centaur and Yamato the plate route and the secret exit branch off at different points, so getting both takes two visits. This relies on venue replays being allowed.

### Open questions

- Does systems.md keep the vanilla weakness cycle? The boss rows assume it.
- Are the plates pickups (this doc) or still boss-kill rewards in second boss rooms (vanilla $F518)?
- Can a cleared venue be replayed for its other exit (the SMW model)? Vanilla beams you out of a beaten boss's room.
- Does a secret-arena win also award the weapon? Assumed yes.
- Should the four behaviour chips be unique to their venues, or may they overlap with shop chips?
- May venues place tag-only Break Man shortcuts (all marked Could), and can he be called in boss rooms?
- Which levers does CASUAL use beyond damage and checkpoints (Toppy refill delay, the Daruma head's anger, the merge wait)?
- Is X-UPEXIT accepted as a Should, or do the climbs ship with ladder stubs?

## design-venues-a (docs/design/venues_a.md)

### Key decisions

- Every venue uses one secret structure: the secret exit is an alternate route ending in a second boss room. The boss-screen test from vanilla `$3F:$F518` moves into the stage-attribute table, so the kill there sets the secret-exit flag. Plates A and B are pickup objects (systems.md §10) that drop in the vanilla secret boss rooms (Knight 1A, Tomahawk 1F), so each is collected together with its exit.
- Screen use: Wind 29 of 32 screens, Knight 28, Tomahawk 32, Plant 32. Main routes keep vanilla's length. No design needs the new 'enter a screen from below without a ladder' exit: every upward exit is a ladder, and every balloon or lift ride stays inside one screen.
- 'T1-lite' replaces true autoscroll. The camera locks on one or two screens, raster bands scroll by time (plus camera), and a data-driven wave director spawns enemies. Wind's sortie, the secret wing arena and Tomahawk's train use it; 4MI's fixed-screen Cossack 1 shoot-'em-up is the precedent.
- Wind, SKY ACE 1943. A 2-minute sortie played by 1943's rules: life drains 1 HP per 600 f, POWs change when shot (POW → 3-WAY → AUTO), 8 hits turn a POW into the YASHICHI, there are 3 LOOPs and 4 red squadrons, AYACO is the giant bomber, and the landing shows 'SHOOTING DOWN %'. The Jet is lent by the stage if not yet owned. Wind Man's own pull code becomes the gust zones (windsock tell).
- Wind secrets. Exit: wipe all 4 red squadrons → elevator lamp board → hangar → WING WALKER fight. Hidden room: the one solid cloud, with a seagull standing on it. Behaviour item: the YASHICHI. Boss: a new HEADWIND (blow) phase, a 1943-loop pinch that calls a red squadron, C.FLASH STALL as the weak reaction, and the first W.STORM hit absorbed (systems SC4).
- Knight, DRAGON QUESTLIKE. ENCOUNTER! command windows are fixed triggers, never random. RUN fails once, then works but forfeits the chest. MAGIC KEYS are consumable: 3 keys for 3 doors. A search verb (DOWN held 24 f) is taught by a Sage. The vanilla IRQ spike ceiling becomes a monster with HP: kill its 4 winches and it retracts.
- Knight secrets. Exit: search behind the empty throne on 15 (Dragon Quest's hidden stairs); the vanilla charged-punch pillar still opens it. This leads to a dark basement (each shot lights it briefly, two sconces light it for good) and the Knightlord, whose 'join me' offer costs a life on YES. Hidden room: Light's tablet under a glinting floor tile. Behaviour item: KAISHIN, from the Metal Metslime (1 damage per hit; flees at f240). Boss: every attack is announced in a battle log; HEALMORE can be interrupted; Y.SPEAR pierces the shield; PUNCH★ breaks the shield for the rest of the fight.
- Tomahawk, GUN.SMOKE FRONTIER. Three bounties: the vanilla dome dispenser, a best-of-three saloon quick-draw (window 20 f; CASUAL 40, HARD 12; Wild Gunman's reaction timer), and a train outlaw. Together they open the Sheriff's gate on the vanilla B-plate ladder, a deliberate re-homing of that gate. The Energy Balancer room 1C and the Jet sky bypass (cut from 4 to 3 screens) are kept. The train uses chains C and E/F as bands with a time term. A Hogan's Alley gallery awards the SHERIFF STAR. The boss opens with a HIGH NOON draw and draws again mid-fight in pinch; PLANT.B makes him sneeze and drop his tomahawk; the first SILVER.T hit is caught and thrown back.
- Plant, JUNGLE PITFALL. Vines (scripted pendulum), croc heads (rideable when closed), logs (F.BLAST burns them), a tar pit that opens and closes by toggling alternate metatiles, and a 3-for-9 underground shortcut. Secret exit: follow a robot cat through a false floor → Lost Caverns → balloon ride → Lost City. Hidden room: lightning reveals a rope ladder. Behaviour item: AUTO RECOVER, for 4 treasures with 0 log hits (the Pitfall perfect). Only one gorilla room remains (the lag fix), and it throws logs.
- Plant art plan, measured with new scripts (planttiles.py, swapcap.py). The vanilla jungle screens use 201-235 of the 256 tile ids, and only 2 ids belong to the lodge alone, so the lodge art cannot be swapped out. The new Pitfall art therefore replaces the 96-tile canopy third and redraws it as a 2600-style canopy in about 40 tiles. The free tile-id ranges quoted for the Wind, Knight and Tomahawk art come from the same measurement.
- Boss reworks keep the vanilla rhythm, measured with a new script (bossmove.py: 1,440 f per boss against a moving player), and add one signature mechanic per boss from its venue: wind phases, battle log, dust devil, vine swing. Each weakness has a unique reaction that replaces the generic freeze (systems SC9).
- Aligned with systems.md and meta.md: vanilla weakness cycle; weakness 4 damage / 16 f; SC1, SC4 and SC8 rules; chip effects; venue prize bolts capped at 60 per venue (bounties now 15/20/25, treasures 10/15/15/20); one sponsor envelope per hidden room; debrief ordered by SECRETS weight (exit → room → item). Each venue also names its featured enemy (PART drop), its VENUE ACT style point and a TIME par.

### Cross-doc dependencies

- systems.md: add Y.SPEAR to SC1's shield pass-through list; specify the weapon behaviours this doc previews in its boss fights (W.STORM updraft, C.FLASH time stop, KNIGHT.C orbit and return, SILVER.T boomerang and Jet dive, PLANT.B launch and Petal Storm); approve the lent Jet; adopt the VENUE ACTs, par times and featured-enemy PARTs in §0.8.
- systems.md (already agreed and used): weakness 4 damage / 16 f; SC1, SC3, SC4, SC8 and SC9; the effects of YASHICHI, KAISHIN, SHERIFF STAR, AUTO RECOVER and the Energy Balancer; prize bolts ≤ 60 per venue; sponsor envelopes; plates as pickups; SECRETS weights.
- story.md: final JP and EN text for every draft line (King, Sage, Innkeeper, Princess Roll, the Knightlord, Sam, the Sheriff, the conductor, posters, battle log, commentator hooks and death tables); the Roll and Tango cameos; the 'WANTED: ROCKMAN' gag.
- meta.md: four secret-exit flags (SECRETS b0 for meta 2, 3, 6, 7); E1 = Wind + Knight and E2 = Tomahawk + Plant (already wired); Records for best quick-draw time and best SHOOTING DOWN %; the debrief already uses this doc's hints as tier B.
- tech.md: T1-lite and the wave director; T4 raster bands (≥ 4 plus the window band) with chains C, E/F and 7 as presets; the T2 text window and menus; T3 doors, keys, gates and lifts; the T5 pendulum; VA-GUST, VA-TIMED, VA-SEARCH, VA-DRAW and VA-ENCOUNTER; the generic object dispatcher; four tileset slots and their banks; new stage-attribute fields (secret-boss screen, plate drop, flag index, HARD poke list); Knight's ceiling logic moved out of IRQ `$11`.
- venues_b.md: share tech (T1, T3, the falling ceiling); avoid a second train, shoot-'em-up or quick-draw; keep the E1-E4 pairing consistent.
- Exhibitions doc: E1 and E2 unlock from these four secret exits.

### Risks

- Screen budget: Tomahawk and Plant use all 32 screens. Fallbacks: merge Plant's 1B and 1C into one cavern screen; shorten Tomahawk's sky bypass to 2 screens.
- Plant tiles: only the canopy third can be swapped (measured), so the 2600-style canopy must still read as a jungle in about 40 tiles. Fallback: keep vanilla's canopy (`$92`) and build the tar and croc water from black tiles plus sprites.
- The sortie and the train need 3-4 raster bands plus the commentator window band in one frame. This depends on the generic raster list and MMC5's scanline IRQ. Fallback: 2 bands.
- Lag and flicker: formations of 5 planes. Caps are stated per set piece (≤ 10 objects), with wave paths staggered so no 16-px row holds more than 4 planes.
- Knight depends heavily on the T2 text engine (encounters, battle log, NPCs, the offer). Fallback: 4MI-style sprite words.
- Knight's spike-ceiling logic runs inside IRQ handler `$11`; adding the retract flag there is fragile. Moving it to a per-frame object during the port is recommended.
- The quick-draw is a reflex test. Mitigations: CASUAL 40-f window, a bell as an audio cue, losing only costs the bounty, and the RNG delay must be replayable for Time Attack.
- The sortie's lent Jet seems to contradict 'Jet after the 4th win'. It needs systems.md and story.md sign-off.
- Trademark words appear in the venue titles (Dragon Quest, Pitfall, Gun.Smoke, 1943). On-screen, use parody names and no logos; meta.md should rule on the final titles.
- Cultural sensitivity in the Tomahawk venue: no jokes aimed at the headdress or culture (content note §3.13).
- About 45 new object kinds in these four venues alone, against about 30 free vanilla type ids. The generic id + sub-id dispatcher is a hard prerequisite.
- Two secrets are skill gates (Wind's 4 full squadrons, Tomahawk's Sidewinder). CASUAL eases both.
- Bass Mode (a Could) would need answers for the sky-bypass ladder, the Power walls and the sortie.

### Open questions

- Does tech.md accept T1-lite (fixed camera plus scrolling bands) instead of true autoscroll for the sortie and the train?
- Is the lent ('rental') Jet acceptable, or should the sortie use a Committee glider that is not Rush at all?
- Will systems.md add Y.SPEAR to SC1's pass-through list, so it can pierce Knight Man's shield?
- Do Knight's keys need a general T3 counter, or a venue-local byte?
- Will story.md let Roll play the DQ princess and Tango cameo as the cat?
- Where does Knight Man's battle log go: the bottom window or a top line?
- Music budget: at most one new track per venue at Should, plus short stingers. Is that within the sound plan?
- If tech.md frees BG tile ids (MMC5 extended attributes or CHR banking), Plant can drop its canopy redraw. Will it?
- Does Plant's collision group 1 leave `$F` deadly? The tar pits and croc water assume so.
- Should the distinct secret-boss arenas (WING WALKER, LOST CITY at night, T-BOOTHILL) be promoted from Should to Must?
- Does systems.md agree that a vehicle the stage lends (the sortie's Jet) satisfies 'normal routes never need a form'?

## design-fortress (docs/design/fortress.md)

### Key decisions

- H1-H5 and W1-W3 are exactly eight stages, and vanilla has exactly eight fortress slots. They keep ids 8-15, so every vanilla AND #$08 / CPY #$08 / $EFE4 fortress test still works. Only the Opening (16), the Semifinal (17) and E1-E4 (18-21) need the stage-attribute class field from day one. Mr. X Returns is 22 (vanilla Mr. X 1, untouched) and the victory lap is 23.
- Base layouts (copies, remixed): H1 = Wily 2, H2 = Wily 1, H3 = Mr. X 3, H4 = Mr. X 2, H5 = Mr. X 4, W2 = Wily 3 (hub and rush tables), W3 = Wily 4 plus a new escape. New tileset slots: TS_STADIUM (Opening, Semifinal, GP Rush lobby, lap), TS_ARCADE (the four exhibitions), TS_LAB (W1 and the escape). The five wings share one MUSEUM CHR third.
- Each vanilla fortress technique is reused with exactly one twist. Mr. X 2's pod column becomes Grand Pi-kun, a balloon whose size frames are streamed into CHR-RAM. Wily 2's walker becomes the Yellow Devil, a BG body that comes apart piece by piece; knocked-down pieces become platforms. The X Crusher becomes the Mecha Dragon over Heat Man appearing blocks. Mechazaurus becomes Gamma, whose rocket fists you ride up to punch its cockpit. Power Piston becomes the Cossack Catcher, a crane cabin with a claw that grabs Rock. The Robot Master framework becomes Dark Man, whose boss panel lies. Metonger Z becomes METALL 16, which upgrades its era between bars. The Wily 3 rush becomes pair bouts. The Wily Machine floor becomes a 16-band Mode-7 floor with depth sizes. The Capsule gets afterimage decoys.
- Only one tool is ever required on a main route: the Magnet Beam. It is taken from a display case at H1 03, which every route passes, before the gap at H1 0B. That is the Rockman 1 homage and a CX lesson 6 telegraph. Everything else is optional: punches, forms, alt fires, synergies, Break Man.
- The Super Adaptor comes out of Gamma's head at the end of H3, as systems.md and meta.md assume. Gamma's finale is a Power uppercut (SC5: fists only), and the Super fist works on replays.
- Break Man helps at the Semifinal: he breaks the rubble, then blocks Bass's β OVERDRIVE. He reveals himself ('Entrant number ten.' / 'That's OBVIOUSLY Blues.') and joins as tag partner there. He exposes the fake Break Man (Dark Man) in H5 and gives the 4MI-style gift in W3: at HP < 6 in the Capsule fight, the CHAMPION BUSTER (4 damage, 8 i-frames, hits of 2+ on Rock become 1). If the player doped, Roll brings the gift instead.
- Bass β copies the champions' weapons the player owns: four at the Semifinal, all eight in W2. In W2 he counter-copies the last weapon that hit him, and SC6's armour starts pre-adapted from BASS_ADAPT. Reading his copy tell earns a COUNTER cell.
- W2 Bracket of Doom keeps vanilla's hub, alcove tables and ninth teleporter, but each alcove calls the GP Rush fight loader into the champion's own venue arena. The twist is pair bouts on the Exhibition pairs: a TAG! warp sends Rock straight into the partner's arena. The bout pits Rock against Project SUPER copies (pinch at HP 14), and the final is Bass in the Championship Ring.
- Super Wily Castle has three eras (F-ERA): POCKET (a 160x144 flip-screen window in four greens, firmware 1.0 with no slide, charge or forms), NES, and SUPER (MMC5 ExGrafix on the background plus the MMC5 pulse channels; Rock is 'not compatible' until he takes Roll's SUPER PATCH capsules). The escape runs the eras in reverse, and the ending's lights go out one audio channel at a time.
- Escape mercy: the match clock is 60 s for the first three attempts, then 90 s with a yellow '+30 INJURY TIME'. The head judge (Cossack) admits it in the ending. Friends during the escape: Flip-Top Jr. (if freed in H4 with the Super fist's homing return), Beat's pit rescue, Rush's automatic catch, Break Man (or Roll) holding the exit door.
- Exhibitions are about 6 screens each, and each rule is the real mechanic: shooting tetrominoes to move and rotate them, with Block Man falling as a piece; a ball that erodes the floor instead of costing lives; a one-shot cannon against a formation that speeds up as it shrinks; four Met-ghosts with the four classic targets. The rule does 4/12 to the guest and weapons only chip. The reward is 100 bolts, an exclusive racing colour and a Museum trophy, not a chip, so the chip count stays at 21.
- Non-venue SECRETS layout: b0 = showpiece secret (weight 3, replacing the secret exit, which only venues have), b1 = a one-screen hidden room with a tell, b2 = a behaviour-gated prize (never a chip), b3 = Mr. X's business card (H5 only). Both hint tiers are written for every stage. The card sits in H5's hidden room, the 1993 wing, reached by knocking six times on the 'under construction' door; it is a diorama of vanilla Mr. X 1 screen 00 and the later entrance to Mr. X Returns.
- Fight ids: this doc's five mid-bosses take $13-$17 (Big Eye, Picopico-kun, Doc Robot, Enker, Trophy Dispenser), leaving $08-$12 to the venues. The '???' fight ($27) is vanilla Wily 4's whole 1993 final under 1993 rules, revealed as DR. WILY (OBVIOUSLY).
- The victory lap is the playable credits: 99 lives and 99 E-tanks on a looping stadium track. Names appear on the scoreboard, banners, the grass and crowd card stunts. Touching a champion types his vanilla DWNB card plus WINS/LOSSES. Wily rides caged on Eddie's float and ends pinned by Rush and Beat in a PHOTO FINISH, which becomes the rating screen's background.
- Mr. Y's unmasking reuses the vanilla Mr. X reveal with two masks: Y comes off to show X, X comes off to show Wily, and everyone says 'WE KNOW.' Vanilla's Wily Fortress picture then upgrades into ExGrafix colour as SUPER WILY CASTLE.

### Cross-doc dependencies

- tech.md: keep H1-H5/W1-W3 at fortress ids 8-15. New ids: 16-21 for Opening, Semifinal and E1-E4; 22 Mr. X Returns (vanilla Mr. X 1 layout and tileset kept intact); 23 victory lap.
- tech.md: tileset slots TS_STADIUM, TS_ARCADE, TS_LAB, copies for TS_H1-H5/TS_W2/TS_W3, and the shared MUSEUM CHR third swapped in at $0A00-$0FFF.
- tech.md: the generic raster list must carry W3's 16-band floor (fallback 8), the POCKET letterbox bands, the PPUMASK water band, and vanilla chains 7/$16/$19/$1A as presets.
- tech.md: ExGrafix (ExRAM mode 1) streamed with nametable columns; MMC5 pulse channels in the sound driver; the VBlank budget for F-SIZES.
- tech.md: the generic GP object id + sub-id for about 40 new object kinds; stage-attribute fields for collision group (crumbling $1D in the Semifinal and escape, group 0 for H1's F.BLAST plug), the Knight-ceiling logic outside stage 6 (H4, escape), NO TAG per screen, OWNED override, era, par.
- tech.md: flip-screen teleport exits for POCKET rooms via $39:$89F5; boss-panel re-type (Dark Man) and new panel records in $3C:$81B1 / $3C:$85EE-$8615.
- systems.md (accepted answers): exhibition rewards are fixed prizes, not chips; fortress adds 8 envelopes and 30-bolt showpiece/prize payouts; Super Adaptor from Gamma at the end of H3; Magnet Beam from a case at H1 03.
- systems.md (proposals): exhibition rule damage booked as class 4 (HAZARD) plus a per-stage OWNED override for VARIETY; 4 exhibition-only racing colours; force beams count as spikes for SPIKE GUARD; the CHAMPION BUSTER column (4/8) and its 'hits of 2+ become 1' rule; Bass's COUNTER cell (3/16); METALL 16's W.STORM FLIP as an SC9 reaction; the Super fist counts as a full-power blow for punch-only enemies and auditions.
- systems.md: uses SC4 (Doc Robot), SC5 (Gamma phase 2), SC6 (Bass, both duels, with BASS_ADAPT), SC7 (Yellow Devil, Could), SC9.
- meta.md: SECRETS b0-b3 definitions and two-tier hints for meta 0 and 9-21; require values TAG (Semifinal b1, H5 b2, W2 b1) and SUPER (H4 b2); Mr. X card in H5 room 19 (RATEFLAGS b1).
- meta.md: fight ids $13-$17 for fortress mid-bosses (venues keep $08-$12); $18-$28 as in fortress.md §8; $27 = vanilla 1993 Wily final under 1993 rules; $28 = Mr. X.
- meta.md: GP Rush lobby = Opening screen 06; fortress maps with NEXT WING / REPLAY / BACK TO BRACKET; EVENTS b4 = crane theft, b5 = Break Man joins at the Semifinal, b6 = unmasking after H5, EVENTS2 b4 = Super after H3; PHOTO FINISH as the rating screen's background.
- story.md: all quoted lines are drafts. Beats to keep: X->Y intro picture, Semifinal help/block/reveal, crane theft, two-mask unmasking with 'WE KNOW', Dark Man's lying panel, W3 gift line (Roll variant), escape PA, injury-time confession, Bass's 'won't be 8-bit' vow, CAPCOM TIMES with vanilla's jailbreak line, Light's 'last match of the season', champion job titles, Mr. Y heckle tables, plaques.
- venues_a.md / venues_b.md: their T1-lite, T2, T3, T4, VA-GUST, VA-TIMED, T6, T7, X-WRAP, X-LABEL, X-METER and X-GPOBJ must stay generic for reuse. Every venue boss must run when loaded through the GP Rush fight loader (W2 SUPER copies) with a per-fight pinch byte. Each champion needs an idle frame, an idle animation and a venue backdrop strip (parade, lap).
- art_audio.md: TS_STADIUM/TS_ARCADE/TS_LAB, MUSEUM third, 5 wing thirds, Bass β, rejects, Grand Pi-kun sizes, MK-VI bosses (the Mecha Dragon in the $8B budget, Gamma about 160 tiles), METALL 16 eras, MODE-7 Machine sizes, exhibition guests, mid-bosses, ending pictures, crowd card stunts. Music listed in fortress.md §9.6, including POCKET/2A03/MMC5 arrangements and the lights-out channel arrangement.

### Risks

- Scope: 14 stages, 22 bosses and mid-bosses, about 40 new objects. If cut, these degrade cleanly: W1, H2, H4, the exhibitions, the victory lap, Mr. X Returns. The Should pieces inside stages (Gemini Rock via T7, gravity flips, SUPER patches) have Must fallbacks.
- W3's 16-band perspective floor needs 16 MMC5 scanline IRQs per frame with mid-frame Y scroll. The fallback is 8 bands; the floor is visual only (collision is a flat line).
- ExGrafix with horizontal scrolling requires streaming ExRAM columns together with the nametable columns. Test on hardware and Mesen early.
- Sprite-per-scanline limits in Gamma (two fists beside Rock), Block Man's pieces and METALL 16's paratroopers. Sizes were chosen to stay at or under 8 per line.
- F-SIZES streaming costs 8-20 VBlank frames per size change. It must always happen in locked rooms, behind motion or a flash.
- The POCKET section is deliberately cramped (no slide or charge). Kept short; CASUAL keeps the slide.
- Break Man is Should. His fallbacks must ship: the reveal without the join, tag gates re-gated to full charges, Roll bringing the gift, Dark Man's disguise drawn as a Rock palette swap.
- Plaque facts about other games (dates, the UFO shot-count trick, the coin-shortage story, the handheld game's missing moves, Rockman 2's Mecha Dragon weakness) need a fact pass. Folklore is worded as folklore.
- Trademark exposure in the exhibitions: parody names only, no logos, guests designed as Rockman robots. The commentators' 'can't say the trademark' gag is part of the design.
- W2 pair bouts load two venue arenas back to back. The 90-frame TAG! card must hide the warp, and the GP Rush loader must be proven first.
- Block Man shares a name with Rockman 11's 2018 Robot Master.

### Open questions

- Does tech.md accept keeping the eight H/W stages in the vanilla fortress ids 8-15?
- Should a doped file get Roll as the victory-lap partner instead of nobody?
- W1 is Should. If cut, does the POCKET/NES/SUPER idea live only in the escape?
- Should Gamma's phase 2 lend the Super Adaptor temporarily, so the uppercut uses it on the first run, instead of awarding it after the fight as systems.md and meta.md assume?
- Should the Hall of Fame stay linear (chronological, fixes when M.BEAM and Super arrive) or be free-order?
- Will systems.md accept 4 exhibition-only racing colours beside the shop's 4?
- Is a one-fight 1993-rules switch acceptable for the '???' fight in TRUE GP, or should it run under GP rules with 1993 art only?
- Keep the name Block Man (it collides with Rockman 11's Robot Master) or rename it, for example TETRO MAN?
- Doc Robot MK-VI copies the champion of the player's worst venue score. Is reading STAGEREC fine, or should it be the champion the player lost to most?
- Is the 32-bit room's Rockman 8 (1996) joke acceptable, given the 'on loan from the future' running gag and the farewell tone?

## design-story (docs/design/story.md)

### Key decisions

- Story spine in six acts (Opening, round one, Semifinal, round two, Hall of Fame, Project SUPER, ending) with 51 scenes S01-S51 in play order, each with EN draft, JP kana draft, engine, seen-bit and tier. STORY_BEAT (FILE $013) values $00-$0C defined.
- Entrant numbering: champions 1-8, Rockman 9 (wildcard), Break Man 10 (BRIEF), Bass beta registered as 'entrant β' because the bracket ran out of numbers; the β is his version number (the beta of Rockman 7's Bass).
- Project SUPER motive tied to the meta layer: Mr. Y sponsored the judges' scorecard cameras; the GP Cup is the data core holding every match; with it he built Bass β and plans a forced 16-bit upgrade of every robot (Wily's speech S33 is half right on NES limits, the point of the farewell theme).
- Running gag ladder for Mr. Y = Wily (10 steps, JP slip from わたくし…ございます into わし…じゃ, unmasking 'WE KNOW', CAPCOM TIMES 'MR. Z'), mirrored by Break Man whose transparent disguise everyone respects; Rock says 'Blues?' exactly twice (S06, S40).
- Break Man arc as 8 beats BM-1..BM-8 (charge tip in the Opening, holds the Semifinal crowd, joins via the tournament's Rule 9 tag-team clause, walks if you dope with pause portrait 'N0' spelled with a zero like vanilla's N0R, unmasks fake Dark Man in H5 as in Rockman 5, carries Rock AND Wily out of the castle 'This time' answering Rockman 3's ending, gives the debrief), with partner / walked / no-tag variants.
- Ending: the stadium's music drops one sound channel at a time while Light delivers the farewell line; a sixth Hall of Fame wing ROCKMAN 6 (1993) with a true plaque; CAPCOM TIMES ends on vanilla's own $95/$96 text kept verbatim; victory-lap credits keep the vanilla DWNB-41..48 fan-designer cards verbatim and list every enemy as an 'entrant… ELIMINATED'; TO BE CONTINUED kept.
- Boss intro cards: vanilla 9-field panel kept English in both languages, records selected by fight id, plus a 10th VENUE field and 5 added glyphs (- ? ! ' β); champions keep vanilla numbers verbatim; new cards for Grand Pi-kun, Bass β x2, 4 guests, 5 MK-VI exhibits (year in LOCATION; Dark Man's card reads 'BREAK MAN?'), W1 boss (proposed THE UPGRADER), WILY MACHINE 'VERSION 6.5' powered by THE GP CUP, Wily Capsule, Mr. X. Field widths machine-checked.
- Commentator system specified as an event bus: 17 event types, priorities P0-P4, 2-entry queue, 600-frame cooldown for flavour lines, ANNOUNCER ON/DEATHS ONLY/OFF, venue death tables of exactly 6 lines played in order then a generic table (12 any-cause + 11 cause-specific), first-weakness lines for every boss, secret/parry/synergy/no-damage/close-call/form/tag/tank lines, and Mr. Y's 16-line per-respawn heckle table (H1-H5) plus Wily's 12-line table (W1-W3) indexed by the file's fortress KO count, with CX-style Yes/No (a 1-bolt 'respawn insurance').
- All venue hook drafts from venues_a/b adopted by stable id (BLZ/FLM/CEN/YAM, and WND/KNT/TMH/PLT assigned here) with final EN+JP and a 6th death line added where missing; FLM-01 drops 'Oil Sultanate'.
- Debrief: Kalinka speaks; tier B = venue owners' words verbatim; four of meta.md's tier-A riddles rewritten for accuracy (WI0 red-squadron 'fives', PL0 Quickclaw's species, YA1 DuckTales 'floors open', KN2 '1000 EXP', CE0 '100 zones' -> more than a hundred). JP for every hint and generic line.
- Chip help pages rewrapped to 3x28 with JP; ◊ pages documented; two proposed hidden functions: DARUMA works twice per life after the 7th KO in a stage visit (proverb made literal), Y-TURBO inert in Super Wily Castle with 'WARRANTY VOID'.
- Text engine rules: labels stay English in both languages (vanilla precedent), sentences are translated; all new text via a glyph-cache window (font in PRG, only a page's distinct glyphs uploaded; 24-tile in-stage strip measured against this doc: median 12-13 distinct glyphs/page); EN is ALL CAPS; JP kana-only with phrase spacing and precomposed dakuten; pause font has no D/O/Q/Z (O written 0); bracket font has no punctuation; text compiler enforces widths, per-surface glyphs, and a no-WIP release check.
- ENGRISH final list for menus only (quotes Zero Wing, Pro Wrestling 'A WINNER IS YOU', Ghostbusters 'CONGLATURATION !!!', vanilla C.FLRSH, 4MI TIWNS/(RESERVED)), with one deliberate story exception (Break Man's perfect line, 4MI's own).
- On-screen name PERSIAN PALACE proposed for Flame's venue (23-char 'PRINCE OF PERSIA PALACE' exceeds the 20-char field and is a third-party trademark as a title).
- Appendix A fact sheet lists ~50 game-history claims with confidence and sources; release dates verified this session (RM1 17 Dec 1987, RM2 24 Dec 1988, RM3 28 Sep 1990, RM4 6 Dec 1991, RM6 5 Nov 1993, Rockman X 17 Dec 1993 = 6 years to the day after RM1 and 6 weeks after RM6), Nintendo published MM6 in NA (Mar 1994), Knight/Wind Man from a Nintendo Power contest, Cossack built Beat (MM5), real Blues unmasks Dark Man (MM5), Break Man saves Rock and leaves Wily (MM3 ending), MM3 controller-2 RIGHT super jump removed in Europe, Tango debuts in Rockman World 5 (1994).

### Cross-doc dependencies

- meta.md: STORY_BEAT at FILE $013 uses this doc's values; FILE $04A b0-7 requested for once-per-save commentator flags; amend §4.0 so the sponsor chair shows a 'BACK SOON' sign from S26 and 'RESERVED' from S33; bracket strings like 'B: EXHIBITIONS' need a ':' glyph or rewording in the stage-select font; tier-A riddles WI0/PL0/YA1/KN2/CE0 replaced by §7.1 versions.
- systems.md: three proposals (DARUMA hidden function after 7 KOs; Y-TURBO inert in W1-W3 with 'WARRANTY VOID'; 1-bolt respawn-insurance choice in Mr. Y's heckles, Could); help pages rewrapped to 3x28 (its drafts ran to 37 cells); synergy names and §4.5 weakness columns used as given.
- venues_a.md: final EN/JP of WND-/KNT-/TMH-/PLT- hooks and 6 death lines each; approvals (rental Jet and RENTAL bib, Princess Roll, Tango cat, WANTED: ROCKMAN); YOU GET never shows adaptors (Roll announces them on the bracket), which removes the vanilla 'AND RUSH JET ADAPTOR' coupling.
- venues_b.md: agree to on-screen name PERSIAN PALACE for Flame's venue; FLM-01 rewritten without 'Oil Sultanate'; 6th death line added to BLZ/FLM/CEN/YAM; CEN-16 loses 'I built that bird' to the save's first plate line.
- fortress.md: place the Opening's tunnel, pit, parade podiums and big screen (S03-S07), the Semifinal crowd set piece (S18), the H2 and H4 thanks-plaque hidden rooms, Mr. X's business card, the post-H5 central gallery (S32), W1's three palette tiers (S35), W2's refight stands (S36), the escape's end (S40), the victory lap (S45); name the W1 boss (proposal THE UPGRADER).
- art_audio.md: portraits and 16x16 face icons for all speakers; three new crawl pictures; plaque frame; claw and saucer; three CAPCOM TIMES headlines; an ending arrangement with one stem per channel (S42); per-speaker typing blips; please drop the planned mixed-case EN font set (this doc makes EN ALL CAPS); add - ? ! ' β to the boss-panel bold set and a VENUE strip to the panel frame.
- tech.md: glyph-cache text window (24-tile in-stage strip), text compiler with the §10.3 checks (widths, per-surface glyph sets, ZERO_O conversion on the pause font, no-WIP release check), language hook at $3C:$8631 for the few kept vanilla JP scripts, boss-panel record pointer by fight id plus a 10th field ($0624 starts at 9), the commentator event bus/queue/cooldown, the player-death hook site for EV_DEATH, and roughly 70-90 KB of text banks.

### Risks

- Text volume: about 1,100 strings x 2 languages (~600 for the Must set) is large for a fan project; every JP line needs a native-speaker pass (register risks: Mr. Y's over-polite わたくし, DQ archaic forms, Yamato's ござる, Invader Man's katakana).
- The 24-tile in-stage pop-up glyph strip (art_audio's budget) is exceeded by about 1 JP page in 12; the compiler must split pages unless tech.md finds 32 tiles.
- Commentary noise: ~300 lines could feel chatty; mitigated by the 600-f cooldown, DEATHS ONLY, and a playtest target of at most one flavour line per 20 s.
- Fact accuracy in plaques: three claims are medium confidence (RM5's day, Rockman's 132 cm height, Quickclaw's species) and are worded to stay true; any new trivia must go through Appendix A.
- Third-party game names appear in plaques and riddles (credit text, no logos); if the project wants none, riddles were written to work with the names removed.
- Break Man's arc depends on the Should-tier tag partner (SYS-TAG-1); fallback variants are written (no-tag path keeps S18, S30/S40 walked variants, S47).
- Several scenes depend on fortress.md, which is still a skeleton: Opening layout beats, the Semifinal crowd set piece, the H2/H4 thanks-plaque rooms, the central gallery, W1 palette tiers, W2 stands, the escape end and the victory lap; the W1 boss is only a proposal (THE UPGRADER).

### Open questions

- Is 'entrant β' (Bass β registered with a Greek letter because the bracket has 10 numbered slots) acceptable, given PLAN called Bass 'a ninth entrant'?
- Will venues_b.md accept PERSIAN PALACE as the on-screen name of Flame's venue?
- ALL CAPS EN (this doc) versus art_audio.md §3.5's mixed-case EN font set: which does the project want?
- Keep the Block Man name clash with Rockman 11 (2018) as a written-in joke, or rename the E1 guest (e.g. TETRA MAN)?
- Should Light call Wily 'Albert' (an English-language canon name) in S33, and アルバート in JP, or ワイリー in JP?
- The kana/kanji spelling of the CX author's name (HIMAJIN JICHIKU) for the JP thanks plaque, and of PURESABE.
- Should Mr. Y's 1-bolt 'respawn insurance' really deduct a bolt (CX's Yes that hurts) or only pretend to?
- Should the victory lap's ALL ENTRANTS roll be generated from the object lists at build time (proposed) or written by hand?
