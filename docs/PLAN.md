# ROCKMAN 6 GP: the plan

> **ロックマン6 GP 史上最大の再会!!** (*Shijō Saidai no Saikai*) / *Mega Man 6 GP: The Greatest Reunion in History*
> Codename **`r6gp`**.

This document describes the game, what version 1.0 contains, how it will be built, and how the first build session
starts. The detail lives in the design documents indexed in §11. Read in this order:

1. this file;
2. [`design/RULINGS.md`](design/RULINGS.md), the binding decisions. §9 records the user's directions and overrides
   every other section and document;
3. [`design/BRIEF.md`](design/BRIEF.md), the founding decisions on identity, cast and conventions;
4. the design document for the area in question (§11);
5. the research, for facts about the ROMs ([`research/README.md`](research/README.md)). The research is authoritative on
   facts; RULINGS is authoritative on decisions.

The plan rests on a teardown of three games. Rockman 6, Rockman CX and Rockman 4 Minus Infinity were disassembled,
played headlessly, cheated through and mapped, which produced about 16,000 lines of research with screenshots and full
stage maps. Eight design documents were written from that research, reviewed by four critics, revised twice and checked
for consistency with each other. [`STATUS.md`](STATUS.md) is the hand-off log.

---

## 0. Summary

- **Premise.** The World Robot Tournament from Rockman 6 becomes a real Grand Prix. Each stage is a match, each clear is
  scored by a panel of judges, the stage select is a tournament bracket, and the commentators react to deaths, secrets
  and weakness hits. The venues are tributes to eras of game history, the fortress is a museum of Rockman 1 to 5, and
  the final castle is the villain's "16-bit upgrade", a farewell to the last Rockman on the NES.
- **Core loop.** Clear a venue; the judges score it on time, damage, weapon variety, secrets and style; the score pays
  out bolts; bolts buy chips at Eddie's Pit Stop; the chips change how the next venue plays. Using the whole arsenal
  earns the most money.
- **Signature mechanic.** The Rush adaptors can fire weapons, which they cannot do in Rockman 6, and Rock switches
  between them instantly with SELECT.
- **Secrets.** Every venue has a secret exit, a hidden room and a chip earned by how the stage is played. After each
  clear, the judges give a hint toward the first secret the player missed.
- **Size.** Version 1.0 is the complete game: the Opening, eight venues with all their set pieces, four Exhibitions,
  the Halftime Riot, five Hall of Fame wings, three castle stages, the escape and the ending, all with new music. The
  current estimate is about 670 focused work sessions, delivered in four playable releases (§4).
- **Platform.** MMC5, 1 MB of PRG-ROM, 8 KB of CHR-RAM and 32 KB of battery-backed PRG-RAM. The game targets
  emulators; real hardware is welcome but not required. The first task is a test of the MMC5 configuration on Mesen.

---

## 1. Vision

### 1.1 Why Rockman 6

Rockman CX and Minus Infinity share a structure: one premise carried through every layer of the game, a combat economy
built around the whole arsenal, secrets that feed a meta-score, deep configuration, a doubled cartridge, a fortress
built from set pieces, and humour throughout. GP uses that structure, but builds each part from what is particular to
Rockman 6.

| Rockman 6 has | GP builds on it |
|---|---|
| A World Robot Tournament premise | A real tournament with matches, judges, prize money, a bracket, a rival entrant and a championship |
| The subtitle 史上最大の戦い, "the greatest battle in history" | Venues that pay tribute to game history; a Hall of Fame that tours Rockman's own history |
| Robot Masters designed by fans in a worldwide contest | The eight return as good-natured champions, each with a reworked fight and a stage built around them |
| Rush Power and Rush Jet | Instant form changes, forms that fire every weapon, and a late Super Adaptor |
| Branching stages and Beat's plates | A secret exit in every venue; plates that add chip slots |
| Its place as the last NES Rockman (1993) | A villain who wants to "upgrade" the world to 16-bit, a castle that does so as you climb it, and an ending that turns the music off one channel at a time |

### 1.2 The three layers

1. **The tournament** supplies the mechanics: scorecards, judges, bolts, the bracket, commentary, rematches and a
   championship rating.
2. **Game history** supplies the content. Each venue borrows a mechanic from a classic game and turns it into a Mega Man
   stage. A homage is always a mechanic, never only a sprite, and it never replaces running, jumping and shooting.
3. **The farewell to 8-bit** supplies the story: Mr. Y's Project SUPER, the museum of Rockman 1 to 5, the castle that
   upgrades itself, and the ending.

The sponsor Mr. Y is plainly Dr. Wily, and the game treats this as an open secret from the first scene to the last.

### 1.3 What it looks like in play

These are some of the moments the design documents are built around.

**The Opening.** Rock walks out of the players' tunnel into a stadium at night. Four warm-up lanes teach the scorecard:
a judge with a clipboard scores the jump course, the limbo under a closing gate, and a high striker that only a full
charge rings. The eight champions ride past on parade floats over a fountain moat, and Rock can high-five each one. Then
Mr. Y presses a button marked UPGRADE, and the tournament mascot, filled with his brand of helium, swells into PI-KUN
16-BIT EDITION and has to be fought across the stadium roof.

**SUMMIT CLIMBER (Blizzard Man).** The stage opens on an icebreaker, the MR. Y MARU, rolling so hard in the swell that
icicles shake loose from the rigging. Ashore, the climb is built like Ice Climber: Rock breaks the ice ceiling with his
head to climb floor by floor, while seals waddle out and patiently fill the holes back in. Kill a seal and its hole
stays open; spare them all and the judges notice. At the top, a forty-second bonus round pays out in vegetables, and a
condor sweeps past. Catch its feet and it carries Rock over a sea of cloud to the secret exit.

**SKY ACE (Wind Man).** Rush is fired off a carrier deck by catapult, wearing a rental bib, into a two-minute sortie
staged like 1943: a fuel bar that drains, red squadrons that pay a bonus if every plane is downed, and a POW capsule that
changes power-up each time it is shot. Juggle one POW through eight hits and it turns into a Yashichi. The sortie ends
when a giant bomber, the AYACO, falls out of the sky in smoke, and the deck crew announces the shooting-down rate. Four
lamps on the hangar wall decide whether the ACES ONLY elevator will open.

**HERO'S QUEST (Knight Man).** A king greets Rock as a descendant of Light. Rock talks to townsfolk and searches
bookshelves with UP, collects magic keys that doors consume, and walks into turn-based encounters: the screen freezes, a
command window opens, and "A METSLIME DRAWS NEAR!" A spike ceiling in the trap hall has its own health bar and can be
destroyed. Knight Man narrates his attacks in a battle log and pauses mid-fight to cast a healing spell that a quick
player can interrupt.

**HIGH NOON FRONTIER (Tomahawk Man).** A WANTED board posts three bounties. The saloon has a sign asking patrons not to
shoot the pianist, and a shooting gallery in the alley rewards restraint: hit a townsperson and the sheriff's star is
lost. The 4:50 train crosses the desert on three parallax bands while a robot horse gallops along the ridge and leaps
onto the caboose. The boss fight opens with a judged quick-draw on a mesa: a flag judge drops the flag, the scoreboard
shows the reaction time, and the rodeo showman tips his hat.

**LOST JUNGLE (Plant Man).** The first three screens are a 1982 jungle run in Rockman's engine: rolling logs, a vine
over a tar pit that breathes, and crocodile heads that open and close beneath Rock's feet. Underground, three screens
loop to cover nine. A robot cat walks across a floor that is not there, and following it leads to a cavern river, which
Rock rides up on a balloon while bats try to pop it. In a storm, lightning briefly reveals a rope ladder in the canopy.

**PERSIAN PALACE (Flame Man).** Rock slides under a closing portcullis at the last moment, steps on loose tiles that fall
away, and fences with palace guards who parry any shot fired from too close. Chandeliers hang over pools of oil; drop
one onto a guard standing in the oil and the pool burns for the rest of the visit. In a hall of mirrors Rock meets his
own shadow, and the way past it is to walk into it and merge. Flame Man fights with a flaming sword and the same parry.

**ATLANTIS RUINS (Centaur Man).** Every room has a ZONE number, and the doors cannot be trusted: a door in ZONE 12 sends
Rock back to ZONE 8, a door marked 99 lies, and ZONE 0 exists only in the dark. The tide is the stage's machine. It
lifts Rock to ledges at high water, locks the ZONE 100 door at low water, and floods a drowned tower as he climbs it.
Centaur Man's boss card reads ABILITY UNKNOWN until a slot machine above his head stops spinning; then he freezes time
and lines up three arrows while Rock stands there, greyed out.

**EDO NINJA ROW (Yamato Man).** On the town's rooftops, Rock stuns ninjas by jumping into the floorboards beneath them.
Inside the mansion, hanging scrolls spin him through the walls. A giant daruma otoshi has to be knocked apart block by
block without touching the head; win, and it paints in its own eye. The caltrop hall is crossed on a spear used as a
pogo stick, bouncing off the guards' heads. In the last hall five scrolls hang still, but a lantern flame leans toward
one of them.

**The Exhibitions.** Four guest robots each bring a classic arcade rule into a single arena. Block Man's arena is a
falling-block well where the buster nudges the pieces; Paddle Man's is a brick wall where Rock is the paddle; Invader
Man's formation speeds up as it thins out; and Girder Man rolls barrels down a stack of girders.

**The Halftime Riot.** At halftime the rejected entries from the robot design contest storm the stadium. A vending
machine robot takes a full charge, stamps it ACCEPTED and leaves a can of energy behind. The lights go out, and a masked
stranger with a whistle holds the crowd back while Rock restores the power. On the roof, under the floodlights, Bass β
fights with copies of the weapons Rock has won, and throws Knight Crusher back at him in Knight Man's green.

**The Hall of Fame.** The trophies are stolen by a claw on Mr. Y's pod and taken to a museum of Rockman 1 to 5. Each wing
remixes one game: the first game's useless score counter and the Yellow Devil; Rockman 2's force-beam shaft and the
Mecha Dragon; the Rockman 3 wing, where Gamma's fist has to be ridden; the Rockman 4 wing, built as a photo puzzle lit by
Bright Man's flash; and the Rockman 5 wing, where a fake Break Man with an orange scarf whistles flat. At the end Mr. Y's
mask comes off to reveal Mr. X, and Mr. X's mask comes off to reveal Wily. The crowd's answer is "WE KNOW."

**Super Wily Castle.** The castle's lab scans Rock, declares him obsolete and downgrades him to a monochrome pocket
screen. He fights his way back up, through an upgrade gate to NES colour and then to 16-bit, where the castle becomes
the most detailed and colourful part of the game and the music gains channels. The Bracket of Doom rematches all eight
champions as SUPER copies in their own arenas. WILY MACHINE 6.5 drives over a floor that Kalinka exposes as scrolling
strips, and the castle crumbles around the escape.

**The ending.** Break Man catches Rock, and Wily, as the castle falls. Wily blames Mr. Y. The champions applaud on the
podium, Bass promises that next time it will not be 8-bit, and the music stops one channel at a time until a single
pulse wave plays alone. The Hall of Fame then opens a sixth wing, for this game.

---

## 2. Cast and story

`design/story.md` owns every word of the game.

| Character | Role |
|---|---|
| **Rockman** | Entrant 9. Normal, Power and Jet forms; the Super Adaptor in the Hall of Fame |
| **Break Man** | The masked tenth entrant. Nobody names him: Rock wonders aloud twice whether he is Blues, and Dr. Light says the name once, at the very end. He helps at the Riot and in the castle; in v1.1 he becomes a playable tag partner |
| **Bass β** | Mr. Y's entrant, registered as entrant β. The rival, fought at the Riot and in the castle |
| **Dr. Cossack and Kalinka** | The commentators |
| **Eddie** | Runs the Pit Stop |
| **Beat** | Beat's plates add chip slots; with all four, he rescues Rock from pits |
| **Dr. Light** | Rock's sponsor. Rockman 6 gives him no lines, so all of his dialogue is new |
| **Mr. Y** | The sponsor, and Dr. Wily |
| **The eight champions** | Blizzard, Centaur, Flame, Knight, Plant, Tomahawk, Wind and Yamato Man, rebuilt by their original fan designers |

**Story.** A year after Mr. X was unmasked, the Tournament Committee stages a Grand Prix to restore the event's
reputation. Mr. Y enters Bass β and sabotages the Opening. At halftime the stadium is overrun, Break Man holds the crowd
and Bass β fights Rock on the roof. After the eighth win the trophies are stolen and taken to the Hall of Fame, where
Mr. Y is unmasked. Beyond it stands Super Wily Castle, which upgrades itself as Rock climbs.

**Ending sequence:** the escape; the castle breaks up into pixels; Break Man catches Rock and Wily; the arrest; the
podium and Bass's promise; the CAPCOM TIMES; the credits with the fan designers' cards; the championship rating and
Break Man's debrief; LIGHTS OUT; the sixth wing; TO BE CONTINUED.

v1.0 has 397 translated strings in English and Japanese, plus labels.

---

## 3. The game

### 3.1 Flow

```
NEW GAME ─► OPENING CEREMONY (warm-up lanes, the parade, Grand Pi-kun)
        ─► THE BRACKET: 8 venues in any order
              Rush Power after the 2nd win, Rush Jet after the 4th
              HALFTIME RIOT after the 4th win (Bass β, first duel)
              EXHIBITIONS E1-E4, opened by pairs of venue secret exits
        ─► the trophy theft ─► HALL OF FAME: H1 → H2 → H3 → H4 → H5
        ─► SUPER WILY CASTLE: W1 UPGRADE LAB → W2 BRACKET OF DOOM → W3 WILY MACHINE 6.5 → the escape
        ─► the ending ─► the championship rating ─► LIGHTS OUT
```

The game saves after every stage, to one of three files. Any cleared stage can be replayed from the bracket or the
fortress map for a better score; a replay pays only the improvement.

### 3.2 The eight venues

**Rule for every venue:** it plays as a Mega Man stage first. Running, jumping, sliding and shooting remain the core of
every screen, with enemies placed for buster play, checkpoints and a Robot Master at the end. The homage mechanic
changes how a section plays; it does not replace the platformer.

| Venue (champion) | Source game | Core mechanic | Secret exit | Hidden room |
|---|---|---|---|---|
| **SUMMIT CLIMBER** (Blizzard) | [Ice Climber](https://en.wikipedia.org/wiki/Ice_Climber#Gameplay) (1985) | the rolling ship; the climb, breaking the ceiling with your head while seals refill the holes; a 40-second bonus summit | riding the condor | the Vegetable Cellar |
| **SKY ACE** (Wind) | [1943: The Battle of Midway](https://en.wikipedia.org/wiki/1943:_The_Battle_of_Midway#Gameplay) (1987) | the catapult launch; a 2-minute sortie with LOOP, fuel drain, POW cycling, red squadrons and the AYACO bomber | the ACES ONLY elevator | WEATHER BALLOON |
| **HERO'S QUEST** (Knight) | [Dragon Quest](https://en.wikipedia.org/wiki/Dragon_Quest_(video_game)#Gameplay) (1986) | talking and searching, magic keys, turn-based encounter windows, a spike ceiling with a health bar | the stairs behind the empty throne | LIGHT'S TABLET |
| **HIGH NOON FRONTIER** (Tomahawk) | [Gun.Smoke](https://en.wikipedia.org/wiki/Gun.Smoke#Gameplay) (1985) | the WANTED board and bounties, a shooting gallery, a judged quick-draw, the 4:50 train | the sheriff's back door | THE OUTHOUSE |
| **LOST JUNGLE** (Plant) | [Pitfall!](https://en.wikipedia.org/wiki/Pitfall!#Gameplay) (1982) | vines, crocodile heads, rolling logs, a tar pit; an underground where three screens cover nine | the cat, the caverns and the balloon | TREETOP HUT |
| **PERSIAN PALACE** (Flame) | [Prince of Persia](https://en.wikipedia.org/wiki/Prince_of_Persia_(1989_video_game)#Gameplay) (1989) | portcullises, loose tiles, palace guards who parry, chandeliers over oil | merging with Shadow Rock | the mouse's room |
| **ATLANTIS RUINS** (Centaur) | [Atlantis no Nazo](https://en.wikipedia.org/wiki/Atlantis_no_Nazo#Gameplay) (1986), with the climb from [Kid Icarus](https://en.wikipedia.org/wiki/Kid_Icarus_(video_game)#Gameplay) (1986) | ZONE numbers, honest and lying doors, the tide as a lift and a lock, a flooding tower | ZONE 100 | ZONE 0 |
| **EDO NINJA ROW** (Yamato) | [Ninja Jajamaru-kun](https://en.wikipedia.org/wiki/Ninja_Jajamaru-kun#Gameplay) (1985), with the pogo from [DuckTales](https://en.wikipedia.org/wiki/DuckTales_(video_game)#Gameplay) (1989) | stunning ninjas through the floor, spinning scrolls, the daruma otoshi, the spear pogo, the nightingale floor | following the draft | the crest vault |

Each venue also has a second set piece and a twist in its secret arena, such as Blizzard's ski run and Wind Man's fight
on the wing of the bomber. Every venue has a CASUAL setting and follows the flash-safety rule.

On-screen text never names a third-party game; plaques describe the source ("a falling-block puzzle from Moscow, 1984").
HIGH NOON FRONTIER's arena is a mesa with no graves, and Tomahawk Man is a rodeo showman with strict duelling manners.
PERSIAN PALACE has domes and a full moon, with no minarets or crescent, and its jokes aim at the source game's
mechanics.

Details: [`design/venues_a.md`](design/venues_a.md) (Wind, Knight, Tomahawk, Plant) and
[`design/venues_b.md`](design/venues_b.md) (Blizzard, Flame, Centaur, Yamato).

### 3.3 The Exhibitions

Four optional arenas, each opened by finding the secret exits of two venues. Each is a lobby and one arena in which a
guest robot fights by the rules of a classic arcade game.

| Exhibition | Source game | The rule |
|---|---|---|
| **E1 BLOCK MAN** | [Tetris](https://en.wikipedia.org/wiki/Tetris#Gameplay) (1984) | pieces fall into a well, and the buster pushes them |
| **E2 PADDLE MAN** | [Breakout](https://en.wikipedia.org/wiki/Breakout_(video_game)#Gameplay) (1976) | Rock is the paddle, and his shots return the ball |
| **E3 INVADER MAN** | [Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders#Gameplay) (1978) | the formation speeds up as it thins, and Rock is the cannon |
| **E4 GIRDER MAN** (proposed) | [Donkey Kong](https://en.wikipedia.org/wiki/Donkey_Kong_(1981_video_game)#Gameplay) (1981) | Rock climbs a stack of girders and ladders while the guest rolls barrels down them; reaching the top exposes him |

### 3.4 The Hall of Fame and Super Wily Castle

| Stage | Tribute to | Highlights |
|---|---|---|
| **H1 ROCKMAN** | [Mega Man](https://en.wikipedia.org/wiki/Mega_Man_(1987_video_game)) (1987) | a score counter that does nothing; the Magnet Beam and the gap that needs it; Elec Man's beams; Guts Man's lifts; Yellow Devil MK-VI |
| **H2 ROCKMAN 2** | [Mega Man 2](https://en.wikipedia.org/wiki/Mega_Man_2) (1988) | Quick Man's force beams down a shaft, Air Man's fans, Heat Man's appearing blocks, Picopico-kun, the Mecha Dragon |
| **H3 ROCKMAN 3** | [Mega Man 3](https://en.wikipedia.org/wiki/Mega_Man_3) (1990) | Needle Man's presses, Gemini Man's laser hall, Doc Robot MK-VI, Gamma MK-VI and the fist that must be ridden, the Super Adaptor |
| **H4 ROCKMAN 4** | [Mega Man 4](https://en.wikipedia.org/wiki/Mega_Man_4) (1991) | a photo puzzle lit by Bright Man's flash, the chapel bells, Dust Man's conveyors, the Cossack Catcher |
| **H5 ROCKMAN 5** | [Mega Man 5](https://en.wikipedia.org/wiki/Mega_Man_5) (1992) | Star Man's low gravity, Crystal Man's crystals, the Super Arrow ride, Dark Man MK-VI, Mr. Y's unmasking |
| **W1 UPGRADE LAB** | the castle | Rock is downgraded to a monochrome pocket screen and fights back up to NES colour and then to 16-bit; METALL 16 |
| **W2 BRACKET OF DOOM** | the castle | the eight champions as SUPER copies, each in its own arena; Bass β, second duel |
| **W3 WILY MACHINE 6.5** | the castle | the machine's approach over a scrolling "Mode 7" floor; the Wily Capsule SUPER; the escape through the crumbling castle |

**The castle is the climax of the game's spectacle.** The 16-bit story depends on how convincingly the castle delivers
it, so the castle gets a dedicated presentation study before it is built: how much colour the MMC5's extended
attributes can add, what the MMC5's two extra pulse channels can do for the music, which raster effects can carry the
"16-bit" look, and how text is shown while extended RAM is used for graphics. The aim is the most ambitious version the
hardware supports. The M0 hardware test includes the extended-attribute mode, so the options are known early.

Only two main-route requirements go beyond the buster and the slide: the Magnet Beam from H1 onward, and Rush Power in
the second phase of the Gamma fight, which the stage teaches beforehand.

Details: [`design/fortress.md`](design/fortress.md).

### 3.5 Core systems

| Area | Design |
|---|---|
| **Controls** | SELECT is a modifier: held with Up or Down it cycles weapons, held with Left or Right it cycles forms, and tapped it returns to the last weapon. Doors and characters respond to UP |
| **Forms** | A form change takes 16-20 frames, with no cutscene. Every form fires every weapon. Rush Power comes with the second win and Rush Jet with the fourth; the Super Adaptor (a rocket fist that returns, and a short jet hop) arrives in H3 |
| **Weapons** | Each weapon has a standard shot in every form. Blizzard Attack's alternate fire, the Ice Block, freezes an enemy into a platform. Slot 9 holds the Magnet Beam. Whether the other alternate fires and form combinations join v1.0 is an open question (§9) |
| **Combat** | Two tables per boss and weapon, after Minus Infinity: damage, and invulnerability after a hit. A weakness deals 4 and leaves the boss open again after 16 frames; the buster deals 1 and leaves 60. The first weakness hit shows WEAK!, staggers the boss and prompts the commentators |
| **Scorecard** | 100 points: time 20, damage 20, variety 25, secrets 20, style 15. The variety target grows with the arsenal, so a buster-only clear is possible but pays less |
| **Economy** | Bolts come only from scorecards (the best score, paid once), one sponsor envelope per hidden room, and capped prizes. There is nothing to farm |
| **Chips** | Fourteen: eight earned in the venues, the Energy Balancer, and five sold by Eddie (SHOCK ABSORBER, SPIKE GUARD, CHARGE KIT, EXCHANGER, ENERGY SAVER). Two slots to start, one more per Beat plate, six at most. Safety nets do not stack |
| **Difficulty** | CASUAL doubles reaction windows, lightens button-mashing, extends timers, adds checkpoints and eases skill-based secrets. HARD raises damage by half, reduces drops and removes the refill on respawn |
| **Accessibility** | By default no large flash repeats more than three times a second; a REDUCED setting turns flashes into fades. An input-lag setting widens reaction windows. A health notice appears at boot |

**The venue chips.** Each is earned by playing a venue a particular way, and each must be worth equipping for the rest of
the game. Four meet that standard as designed. The other four are being redesigned, and the replacements below await
approval.

| Venue | Earned by | Chip | Effect |
|---|---|---|---|
| SKY ACE | juggling one POW through eight hits | YASHICHI | once per stage, the first time health falls to 4 or less, it refills completely |
| HERO'S QUEST | defeating the Metal Metslime | KAISHIN | every 12th hit on a boss is a SPLENDID STRIKE, worth 2 extra damage |
| HIGH NOON FRONTIER | reaching the sheriff without hitting a townsperson | SHERIFF STAR | +20 % on every payout |
| EDO NINJA ROW | winning the daruma otoshi without touching the head | DARUMA | once per life, a hit that would kill leaves 1 health instead |
| SUMMIT CLIMBER | sparing every seal | **CLIMBER'S GRIP** (proposed) | ladders are climbed half again as fast, and a hit never knocks Rock off a ladder; ice floors grip like normal floors |
| PERSIAN PALACE | reaching the end without igniting the oil | **COOL HEAD** (proposed) | taking damage does not cancel a buster or Power charge |
| ATLANTIS RUINS | freeing the three statues with full charges | **ZONE MAP** (proposed) | the pause screen shows which of each stage's secrets are still unfound, and breakable walls and secret doors shimmer faintly |
| LOST JUNGLE | the EXPLORER'S PERFECT: every treasure, no points lost | **FORAGER** (proposed) | every 5th enemy defeated in a row without taking damage drops a small energy capsule, every 10th a large one |

Details: [`design/systems.md`](design/systems.md).

### 3.6 Meta

Three save files, each stored twice with a commit marker; a title screen with the health notice; file select with the
difficulty choice; the bracket, with rematches and the event queue; the judges' desk, where the score rows slide in,
the medal is stamped and the debrief gives a one-line hint toward the first missed secret; medals and Hall of Fame
points; CONFIG (language, commentary, text speed, flashes, screen shake, input lag, button layout); the fortress maps;
RECORDS; the championship rating; and EXTRA CONFIG, a built-in stage select and RAM editor that also serves as the entry
point for automated tests.

Details: [`design/meta.md`](design/meta.md).

---

## 4. Scope and schedule

### 4.1 What is in v1.0

v1.0 contains everything in §3, with new music throughout. The following are deliberately left for later or dropped.

| Item | Status |
|---|---|
| Break Man as a playable tag partner | v1.1 |
| HARD per-stage changes and boss AI branches | v1.1 |
| PARTs, the garage, Mr. Y's booth and the TURBO trap | v1.1 |
| GP Rush (boss rush with courses) | v1.1 |
| Weapon alternate fires (except the Ice Block) and the eight form combinations | open (§9) |
| 1993 RULES, a preset that plays by Rockman 6's original rules | open (§9) |
| Time Attack | not planned for now |
| Playable victory-lap credits; achievements; ENGRISH; the attract-mode crawl | cut |
| Bass Mode; Mr. X Returns; the Museum gallery; KNOCKOUT; Exhibition rule variants; critical hits | not planned |

### 4.2 Estimate

The session ledger (`tools/plan/tight.py`, `tools/plan/tally.py`) prices every item in focused work sessions. Before
the user's review it held about 451 sessions for a smaller v1.0. The content added since (H2, H4, W1 and the castle's
presentation work, every second set piece, the Exhibitions, and new music for every stage) brings the estimate to
**about 670 sessions**, or about 690 if the alternate fires and form combinations are included. The ledger is
re-itemised in the next revision round and re-estimated from real progress after the vertical slice.

At three sessions a week, 670 sessions is a little over four years; at four a week, a little over three.

### 4.3 Releases

| Release | Contents | Approximate cumulative sessions |
|---|---|---|
| **v0.1** | the vertical slice: new game, the bracket, SUMMIT CLIMBER complete, the judges, saving, reloading, replaying | ~155 |
| **v0.5** | the Opening, all eight venues, the Exhibitions, the Halftime Riot | ~435 |
| **v0.8** | the Hall of Fame, H1-H5 | ~535 |
| **v1.0** | Super Wily Castle, the escape, the ending; Japanese review; release | ~670 |

Every release is a complete, playable build that can be shared.

---

## 5. Platform and engine

| Area | Design |
|---|---|
| **Cartridge** | MMC5 with 1 MB of PRG-ROM, built by inserting new banks into the original ROM, so every original bank keeps its number and every original bank switch still works. 32 KB of battery-backed PRG-RAM holds saves, working data, stage layouts and tiles |
| **Stage ids** | 32 stage ids, each described by a 48-byte attribute record, replacing the original game's assumption of 16 stages |
| **Layouts** | Stage layouts are copied into RAM, where the original drawing routines read them unchanged. This gives one service for changing the map at run time (breakable blocks, opening doors, difficulty changes) |
| **Raster effects** | The original game's 27 interrupt chains are first ported exactly, then replaced by a general list of up to 24 screen bands per frame |
| **Text** | A new text engine draws into a window held in the MMC5's extended RAM: 2-line pop-ups and 4-line dialogue, English in capitals and Japanese in kana, with dictionary compression |
| **Sound** | The original sound driver, reassembled from source, with new songs in their own banks and a compiler for a text music format. The MMC5's two extra pulse channels are used in the castle |
| **Objects** | Object families and sub-types, a fixed plan for which object slots hold what, frozen-enemy handling, a shared state for anything Rock holds onto (vines, the condor, the balloon), a shared vehicle state for flying sections, and one module for every on-screen counter |
| **Boss fights** | A fight loader can start any boss fight from a hub, from EXTRA CONFIG or from a test, and return correctly. The Bracket of Doom is built on it |
| **Tooling** | Patch builds, a registry of every code hook, a free-space allocator, EXTRA CONFIG, warps, and recorded test inputs replayed headlessly on FCEUmm, with Mesen checks at every milestone |

The research already supplies the RAM map, disassemblies of every bank, a level extractor and renderer that rebuilds the
original levels byte for byte, all sixteen stage maps, the object and damage tables, the sound format, the text scripts,
the sprite format, the interrupt chains, the stage-id readers, warps and savestates.

Details: [`design/tech.md`](design/tech.md).

---

## 6. Art and music

- **Art.** No pixel artist is assumed. New enemies start from recolours and composites of Rockman 6's own sprites;
  Break Man and Bass β are built from Rock's sprite sheet; new tiles go into new banks, so no Capcom art is overwritten.
  Each milestone ends with an art review: screenshots and an animation gallery sent to the user. The first art
  milestone includes one or two sample sprites drawn from scratch, so the user can judge whether to commission an
  artist.
- **Music.** Every stage gets its own new music. The search for a composer starts now; until one is found, Claude
  sequences the tracks in the text music format. The castle's music uses the MMC5's two extra pulse channels as part of
  the 16-bit upgrade, and the ending's arrangement drops one channel at a time.
- **Budgets.** Before the content added in §4.2, v1.0's art came to about 4,500 new tiles and 350 animation frames, each
  asset costed by method (reuse, composite, programmatic or drawn).

Details: [`design/art_audio.md`](design/art_audio.md).

---

## 7. Milestones

| M | Contents | Release |
|---|---|---|
| **M0** | Workbench: build, patch format, hook registry, allocator, test runner, recorded tests of the original game; reassemblable source for the fixed banks and the sound driver; round-trip tools for levels and music. **The MMC5 hardware test on Mesen**, including the extended-attribute mode. A measurement of the busiest set pieces in CX and Minus Infinity (§8, risk 4) | |
| **M1** | The original game running on MMC5, matching the original frame for frame; PRG-RAM, the save skeleton, the test mailbox | |
| **M2** | Engine for the slice: object families, RAM layouts and the map-edit service, the art tools, the level pipeline, the raster list, the first text engine, music, saves, the bracket, the judges' desk, EXTRA CONFIG. **Sample sprites for the art review** | |
| **M3** | Systems for the slice: SELECT, weapons, the damage tables, WEAK!, frozen enemies, the Ice Block, the scorecard, bolts, the shop, on-screen counters, the commentary | |
| **M4** ⛳ | **SUMMIT CLIMBER end to end.** The ledger is re-estimated from real progress | **v0.1** |
| **M5** | The stage-attribute table; forms and adaptors; the Opening; PERSIAN PALACE, LOST JUNGLE, ATLANTIS RUINS, EDO NINJA ROW | |
| **M6** ⛳ | Dialogue; forced scrolling; HERO'S QUEST, HIGH NOON FRONTIER, SKY ACE; the Exhibitions; the Halftime Riot | **v0.5** |
| **M7** ⛳ | Background-boss tools and the fight loader; H1-H5 | **v0.8** |
| **M8** | The castle presentation study; W1-W3, the escape, the ending | |
| **M9** ⛳ | Japanese review, balance, emulator testing, release | **v1.0** |

⛳ = the user plays the build. M0 is broken into session-sized tasks in `design/tech.md` §16.3.

---

## 8. Risks

| # | Risk | Response |
|---|---|---|
| 1 | **Length.** About 670 sessions is several years of part-time work | Four playable releases; the estimate is revised after the slice and at each release |
| 2 | **MMC5 behaviour differs between emulators.** FCEUmm is more forgiving than Mesen or hardware | The Mesen test comes before any porting; every milestone build is checked on Mesen |
| 3 | **The slice is large**: about 155 sessions before the first playable venue, because it builds most of the engine, the whole scoring economy and the art and music pipelines | Forms are left out of the slice, since a new save file has none; the slice's real cost recalibrates the rest |
| 4 | **Lag.** Rockman 6 starts to slow down at about seven active objects, and several set pieces approach that | Learn from the reference hacks before designing set pieces. Minus Infinity's MMC5 build showed no slowdown in 10,800 measured frames, helped by a faster, unrolled video-memory copy and by tile streaming, both of which GP adopts. M0 adds a measurement of the busiest set pieces in CX and Minus Infinity: how many objects they run, and which effects they draw in the background instead of with sprites. The results become design rules for every stage: set pieces drawn in the background or with map edits where possible, spawns throttled, and the object budget checked by the build |
| 5 | **The castle's 16-bit spectacle** competes with the text window for the MMC5's extended RAM | The castle presentation study (§3.4) settles this before the castle is built |
| 6 | **Text space.** Some stages have no free background tiles for text | Text tiles are borrowed and restored from ROM |
| 7 | **No pixel artist** | Sample sprites at M2, art reviews at every milestone, and the option to commission later |
| 8 | **No composer yet** | Claude sequences the music until a composer is found; the music format is plain text, so tracks can be replaced |
| 9 | **Japanese review** is an outside dependency | Japanese text remains a draft until a reviewer is found; English can ship first |

---

## 9. Decisions

**Made by the user (2026-10-29 and 2026-10-31):**

1. **Hardware.** Emulators are the target. Real hardware is welcome but not worth an unusual cartridge.
2. **Art.** No artist yet. Sample sprites at M2 will inform whether to commission one.
3. **Japanese review.** To be decided later.
4. **Title.** ROCKMAN 6 GP: 史上最大の再会!! (*Shijō Saidai no Saikai*, "The Greatest Reunion in History"), a pun on
   the original subtitle 史上最大の戦い (*Tatakai*).
5. **Pace.** About two sessions a week if sessions are as heavy as the planning sessions; three or four if lighter.
6. **Scope.** v1.0 is the complete game. All Hall of Fame and castle stages, every second set piece, the Exhibitions and
   new music are in, and the releases are the slice, the venues, the Hall of Fame and the castle (RULINGS §9).

**Waiting on the user:**

1. **Weapon alternate fires and form combinations** (about 20 sessions). Each weapon would gain a second fire mode and
   one combination with a Rush form. Are they part of v1.0, or v1.1?
2. **1993 RULES** (about 3 sessions). A preset that plays with Rockman 6's original rules. v1.0, v1.1, or cut?
3. **The four chip replacements** in §3.5.
4. **Girder Man** as the fourth Exhibition (§3.3).

---

## 10. How the first build session starts

1. Upload `Rockman 6 - Shijou Saidai no Tatakai!! (Japan).nes` and say **"begin M0"**.
2. Claude runs `tools/setup_env.sh`, places the ROM at `roms/rm6j.nes` and checks its MD5,
   `d9a4eed8b3c13a6bd74b2e9d20385afb`.
3. Claude boots it headlessly with `tools/analysis/emu.py` and checks the title screen.
4. Claude builds the MMC5 test ROMs. Mesen cannot run in the cloud environment, so the user runs them in Mesen and
   reports the results. That report decides whether MMC5 is used.
5. Work continues task by task from `STATUS.md`, with tests and a commit at the end of each task.
6. Optional: play the original game in Mesen 2 with the Code/Data Logger enabled, visit every stage once, and upload the
   `.cdl` file. It confirms which bytes are code, data or free space.

---

## 11. Document index

### Design (`docs/design/`)

| Document | Contents |
|---|---|
| [`RULINGS.md`](design/RULINGS.md) | The binding decisions. §9 holds the user's directions |
| [`BRIEF.md`](design/BRIEF.md) | The founding decisions: identity, cast, structure, conventions |
| [`tech.md`](design/tech.md) | Cartridge, memory, stage ids, layouts, pipelines, objects, raster effects, text and sound engines, saves, tooling, lag, milestones |
| [`systems.md`](design/systems.md) | Controls, forms, weapons, combat, scorecard, economy, chips, Beat, the tag partner, difficulty |
| [`meta.md`](design/meta.md) | Saves, title, file select, the bracket and Pit Stop, the judges' desk and debrief, medals, the rating, CONFIG, EXTRA CONFIG |
| [`venues_a.md`](design/venues_a.md) | SKY ACE, HERO'S QUEST, HIGH NOON FRONTIER, LOST JUNGLE, screen by screen |
| [`venues_b.md`](design/venues_b.md) | SUMMIT CLIMBER (the slice), PERSIAN PALACE, ATLANTIS RUINS, EDO NINJA ROW |
| [`fortress.md`](design/fortress.md) | The Opening, the Halftime Riot, the Exhibitions, the Hall of Fame, Super Wily Castle, the ending |
| [`story.md`](design/story.md) | Every line of text in English and Japanese |
| [`art_audio.md`](design/art_audio.md) | Art and music budgets, tileset slots, the art method, the track list |
| [`reconcile.md`](design/reconcile.md) | The record of the cross-document consistency pass |
| [`review_feasibility_design.md`](design/review_feasibility_design.md), [`review_consistency_scope.md`](design/review_consistency_scope.md), [`crossrefs.md`](design/crossrefs.md) | The critics' findings and cross-references behind RULINGS |

The design documents still carry the earlier scope tiers (for example, H2 and H4 marked Should). RULINGS §9 overrides
them until the next revision round brings them in line.

### Research (`docs/research/`)

| Where | What |
|---|---|
| [`research/README.md`](research/README.md) | How the research was done and where everything is |
| `research/rm6/` | Rockman 6: RAM, engine, levels and all sixteen stage maps, stages, fortress, text, cheats |
| `research/cx/` | Rockman CX: engine, systems, stages, fortress, graphics, text, cheats |
| `research/r4mi/` | Rockman 4 Minus Infinity: engine, systems, stages, modes, graphics, text, cheats |
| [`DECONSTRUCTION.md`](DECONSTRUCTION.md) | The first teardown, from the hacks' documentation |

### Tools

| Where | What |
|---|---|
| `tools/setup_env.sh` | Installs the toolchain into `.pylib/` |
| `tools/analysis/` | The headless emulator harness (`emu.py`), patchers, bank maps, disassembler and per-game tools |
| `tools/plan/` | The session ledger |
