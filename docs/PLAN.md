# ROCKMAN 6 GP: the plan (v2)

> **ロックマン6 GP 史上最大の再会!!** (*Shijō Saidai no Saikai*) / *Mega Man 6 GP: The Greatest Reunion in History*
> Codename **`r6gp`**. The title is a working title (question 4 in §9).

This is the front door to the project. It says what the game is, what v1.0 contains, how it gets built, and how the
next session starts. The detail lives in the design docs it indexes (§11). Read in this order:

1. this file;
2. [`design/RULINGS.md`](design/RULINGS.md): the director's binding rulings. They override everything else in `design/`;
3. [`design/BRIEF.md`](design/BRIEF.md): the founding decisions (identity, cast, conventions);
4. the design doc for the area you are working on (§11);
5. the research for facts about the ROMs ([`research/README.md`](research/README.md)). **The research wins on facts**,
   RULINGS wins on decisions.

v1 of this plan was written from the hacks' readme files. v2 comes after a deep teardown: the three games were
disassembled, played headlessly, cheated through and mapped (about 16,000 lines of research with screenshots and full
stage maps). Eight design docs were then written, reviewed by four critics (feasibility, design quality, consistency,
scope) and revised against [`RULINGS.md`](design/RULINGS.md). A third round settled the revisers' open questions
(RULINGS §8), applied their 59 cross-doc requests ([`reconcile.md`](design/reconcile.md)) and ran four cross-doc
consistency critics, whose 84 findings were verified and fixed. [`STATUS.md`](STATUS.md) is the hand-off log.

---

## 0. In one page

- **The premise:** the World Robot Tournament from Rockman 6 is real this time. Every stage is a **match**, every clear
  is **judged**, the stage select is a **bracket**, money is **prize money**, and the commentators react to everything
  you do. The venues are tributes to eras of game history, the fortress is a **museum of Rockman 1-5**, and the final
  castle is the villain's **"16-bit upgrade"**: the farewell of the last NES Rockman.
- **The loop:** clear a venue → the judges score it (TIME, DAMAGE, VARIETY, SECRETS, STYLE) → bolts → Eddie's Pit Stop
  → chips → the next venue plays differently. Using your whole arsenal is literally how you earn money.
- **The signature:** **Rush forms can fire weapons** (vanilla forms can't), swapped instantly with SELECT.
- **The secrets:** every venue has a secret exit, a hidden room and a chip earned by *how* you play, and the judges'
  debrief hints at the first one you missed (4MI's predicate table).
- **The size:** v1.0 is 8 reworked venues, the Opening, a mid-game riot with the rival, 3 museum wings, 2 castle
  stages, an escape and the ending. That is about **450 focused work sessions** (the ledger, §4), delivered as three
  playable releases: **v0.1** (one venue, end to end, at about 150), **v0.5** (all 8 venues, about 342) and **v1.0**.
- **The platform:** MMC5, 1 MB PRG, 8 KB CHR-RAM, 32 KB battery PRG-RAM. First job: a **go/no-go spike on Mesen** (§7).
- **The rule that keeps it finishable:** a Must item may depend only on Must items, and the ledger, not enthusiasm,
  decides scope.

---

## 1. Vision

### 1.1 Why this game, built on this ROM

Rockman CX and Rockman 4 Minus Infinity share a skeleton (the summaries in `research/cx/` and `research/r4mi/`): one
premise followed through every layer, an arsenal-centred combat economy, earned secrets with a meta-score, deep
configuration, a doubled cartridge, a fortress built as set pieces, and humour everywhere. GP uses that skeleton but
builds every bone from what is unique to Rockman 6:

| What RM6 uniquely has | How GP amplifies it |
|---|---|
| A **World Robot Tournament** premise | A real tournament: matches, judges, prize money, a bracket, a rival entrant, a championship |
| Its subtitle, *"The Greatest Battle in **History**"* | Every venue is a tribute to an era or genre of **game history**; the fortress is a museum of **Rockman history** |
| Bosses **designed by fans** in a worldwide contest | The eight return as good-natured champions, reworked the way 4MI reworked RM4's bosses (their credit cards DWNB-41..48 name their designers) |
| **Rush Power / Rush Jet** | A second axis of play: instant swaps, forms that fire every weapon, and a late **Super Adaptor** |
| **Branching stages** and **Beat** plates | Every venue gets a secret exit; plates become chip slots |
| The **last** NES Rockman (1993) | The villain's scheme is a "16-bit upgrade"; the castle gains colour, bands and channels; the ending turns the lights off one channel at a time |

### 1.2 The three layers

1. **The tournament** (mechanics): scorecard, judges, bolts, bracket, commentary, rematches, a championship rating.
2. **Game history** (content): each venue is a playable homage built from a *mechanic* of its genre, never just a sprite
   (CX lesson 2). Names are parodies; plaques describe and never name third-party games (R3.3).
3. **The farewell to 8-bit** (story): Mr. Y's Project SUPER, the museum of Rockman 1-5, the castle that "upgrades", and
   LIGHTS OUT.

Running gag: the sponsor **Mr. Y** is obviously Dr. Wily, and everyone says so.

### 1.3 How crazy it gets (a few of the screenshot moments)

From the design docs' screenshot lists. Every venue and boss has at least one.

- Rockman breaks ice with his **head**, floor after floor, while a seal patiently fills the holes back in (SUMMIT CLIMBER).
- A 40-second **bonus round** in a Rockman game, paying out vegetables; then Rockman hangs from a condor's feet.
- **"A METSLIME DRAWS NEAR! COMMAND?"**, a spike ceiling with an HP bar that dies, and a boss who announces every attack
  in a battle log (HERO'S QUEST).
- The flag drops, **"DRAW!"**, and the scoreboard reads **0.23** (HIGH NOON FRONTIER).
- A 2-minute 1943-style sortie on Rush, juggling a POW through power-ups until it spins into a Yashichi (SKY ACE).
- Rockman meets his own shadow, and the winning move is a hug (PERSIAN PALACE).
- A door labelled 99 that lies, and Centaur Man's ABILITY UNKNOWN turning out to be a slot machine (ATLANTIS RUINS).
- A giant daruma otoshi you win by never touching the head, and Yamato Man's helmet flying off as his MOBILE stat jumps
  to 99 (EDO NINJA ROW).
- Bass β throwing **your** Knight Crusher back at you, with `NO DATA` over his head (HALFTIME RIOT).
- Hall of Fame doors that read `CLOSED FOR RENOVATION`, and a castle whose panel reads **WILY MACHINE 6.5**.
- The last sound of the game is pulse 1, alone.

---

## 2. Cast and story (story.md owns every word)

| Who | Role |
|---|---|
| **Rockman** | Entrant 9. Normal / Power / Jet forms; the Super Adaptor in the Hall of Fame |
| **Break Man** (= Blues, his Rockman 3 alias) | The masked 10th entrant. Introduced in the Opening roll call with no name spoken; joins at the HALFTIME RIOT. **His disguise is respected**: only Rock says "Blues?" (twice) and Light says the name once, at the very end (R4.2). In v1.0 he is an NPC; the playable tag partner is v1.1 |
| **Bass β** (Forte β) | Mr. Y's entrant, "entrant β", the rival. Duel 1 at the Riot, duel 2 in Super Wily Castle |
| **Dr. Cossack and Kalinka** | The commentators (pop-ups on deaths, weaknesses, secrets) |
| **Eddie** | Runs the Pit Stop shop |
| **Beat** | Plates become chip slots; complete B-E-A-T and he rescues you from pits |
| **Dr. Light** | Rock's sponsor. Vanilla RM6 gives him no lines, so all of his are new |
| **Mr. Y** | The sponsor. Obviously Wily. Unmasked in the Hall of Fame (two masks) |
| **The 8 champions** | Blizzard, Centaur, Flame, Knight, Plant, Tomahawk, Wind, Yamato: good-natured rivals |

**The arc.** A year after Mr. X was unmasked, the Committee stages the Grand Prix to restore the tournament's honour.
Mr. Y enters Bass β and sabotages the Opening. At halftime the stadium is overrun by the fortress's rejects; Break Man
holds the crowd and Bass β fights you on the roof. After the eighth win the trophies are stolen and taken to the
**Hall of Fame**; Mr. Y is unmasked there. Beyond it, **Super Wily Castle** upgrades as you climb: the BRACKET OF DOOM
rematches every champion in SUPER colour, then WILY MACHINE 6.5 and the escape.

**The ending** (R4.1, binding order): the escape → the castle pixelates → Break Man catches Rock and Wily → the arrest,
with one use of the Mr. Y / Mr. Z gag → the podium and Bass's vow → the CAPCOM TIMES → credits on the vanilla staff-roll
engine with GP text and the champions' cards → the championship rating and Break Man's debrief → **LIGHTS OUT** → the
sixth-wing plaque → TO BE CONTINUED.

Text in v1.0: 397 Must strings in EN and JP (R4.5 and R8.4). The Opening is capped at about 15 scene pages (R4.4)
and uses 12.5.
Details: [`design/story.md`](design/story.md).

---

## 3. The v1.0 game at a glance

### 3.1 Flow

```
NEW GAME ─► OPENING CEREMONY (Opening-lite: warm-up lanes teach the scorecard; parade; Grand Pi-kun)
        ─► THE BRACKET: 8 Heritage Venues, any order
              Power adaptor after the 2nd win, Jet after the 4th (stored as save flags, 4MI precedent)
              HALFTIME RIOT after the 4th win (Bass β duel 1; Break Man joins)
        ─► the trophy theft ─► HALL OF FAME: H1 → H3 → H5 (H2 and H4 "CLOSED FOR RENOVATION" until v1.1)
        ─► SUPER WILY CASTLE: W2 BRACKET OF DOOM → W3 WILY MACHINE 6.5 → the escape
        ─► the championship ending ─► rating ─► LIGHTS OUT
```

Saves after every stage (3 files). Every stage can be replayed from the bracket or the fortress maps for a better score
(replays pay only the improvement).

### 3.2 The eight Heritage Venues

Every venue ships its **core** in v1.0 (R0.2): the homage mechanic, a secret exit, a hidden room, a behaviour chip and the
boss rework. Its second set piece and secret-arena twist are v1.1.

| Venue (champion) | Homage | Core mechanic | Secret exit | Hidden room | Chip (how it's earned) |
|---|---|---|---|---|---|
| **SUMMIT CLIMBER** (Blizzard) · v0.1 slice | the mountain-climbing arcade game | rocking ship with falling icicles; head-bonk ice climb with seals refilling the holes; a 40-s vegetable bonus summit | the **condor** over the bonus summit | the Vegetable Cellar | **SNOW CHAINS**: grip on ice (never destroy a Toppy) |
| **SKY ACE** (Wind) | the WWII shooter (Capcom's own 1943) | catapult launch; a 2-minute sortie on the free-flight vehicle state: LOOP, POW cycling, red squadrons, the AYACO | the lamp board and the ACES ONLY elevator | WEATHER BALLOON | **YASHICHI**: one full refill at low HP (juggle a POW through 8 hits) |
| **HERO'S QUEST** (Knight) | the 1986 console RPG | talk and search verbs, MAGIC KEYS, two ENCOUNTER! command windows, a spike ceiling with HP | the stairs behind the empty throne (key check) | LIGHT'S TABLET | **KAISHIN**: every 12th boss hit is a SPLENDID STRIKE (+2) (beat the Metal Metslime) |
| **HIGH NOON FRONTIER** (Tomahawk) | the Capcom western (Gun.Smoke) | WANTED board and bounties; an alley shooting gallery; a judged quick-draw (24/18/40 f); the 4:50 train with Sidewinder | the Sheriff's back way | THE OUTHOUSE | **SHERIFF STAR**: +20 % prize money (no townsfolk hit) |
| **LOST JUNGLE** (Plant) | the 1982 jungle run | vines, croc heads, rolling logs, a breathing tar pit; the underground where 3 screens cover 9 | the robot cat, the Lost Caverns and the balloon | TREETOP HUT | **AUTO RECOVER**: slow HP regen when idle (the PITFALL PERFECT) |
| **PERSIAN PALACE** (Flame) | the 1989 rotoscoped platformer | plates, portcullises, loose tiles; palace guards with a spacing parry; chandeliers over oil | merge with **Shadow Rock** | the mouse room | **FIREPROOF**: fire floors hurt instead of kill (no oil ignited) |
| **ATLANTIS RUINS** (Centaur) | the 1986 Famicom ZONE-door maze; the Underworld climb | ZONE cards; honest, lying and fake doors; the tide as a lift and a lock; a tidal shaft that floods as you climb | **ZONE 100** | ZONE 0 | **CENTURION**: a bot that absorbs 3 boss shots (free the three statues) |
| **EDO NINJA ROW** (Yamato), trimmed | the 1985 ninja platformer that bonks from below; Capcom's own pogo cane (DuckTales) | rooftop bonk-stun through the floorboards; spinning scrolls; the spear pogo over caltrops; the Daruma | the draft in the hall of scrolls | the crest-trapdoor vault | **DARUMA**: survive one lethal hit per life (win the daruma otoshi) |

Cultural fixes are Must (R3.4): HIGH NOON MESA has no graves and Tomahawk Man is a rodeo showman strict about duel
etiquette; PERSIAN PALACE has no "Oil Sultanate", no minarets or crescent, and its jokes aim at the platformer's mechanics.
Every venue fills in a CASUAL lever list and has a flash-safe default (R2.9, R3.5).

Details: [`design/venues_a.md`](design/venues_a.md) (Wind, Knight, Tomahawk, Plant) and
[`design/venues_b.md`](design/venues_b.md) (Blizzard, Flame, Centaur, Yamato).

### 3.3 The special stages and the fortress

| Stage | Id | Milestone | v1.0 core |
|---|---|---|---|
| **OPENING CEREMONY** (Opening-lite) | `$10` | M5 | the players' tunnel; four warm-up lanes whose judges each teach one scorecard row; the parade of floats; Mr. Y's sabotage; **Grand Pi-kun** (one size). ≤ 15 scene pages |
| **HALFTIME RIOT** | `$11` | M6 | the stadium at night, overrun by the fortress's **rejects** (VENDING MAN, CHEER MAN); one lights-on-a-timer set piece; Break Man holds the crowd and joins (0E); **Bass β duel 1** |
| **H1 ROCKMAN** | `$16` | M7 | Wily 2 remix; the useless SCORE; the **Magnet Beam** and the gap that needs it; Elec Man's beams, Fire Man's pillars; **Yellow Devil MK-VI** |
| **H3 ROCKMAN 3** | `$18` | M7 | Mr. X 3 remix; Needle Man's presses; Gemini Man's laser hall; a no-risk fist-ride practice; **Gamma MK-VI** (head and fists; POWER required in phase 2, with a tell); the **Super Adaptor** dock |
| **H5 ROCKMAN 5** | `$1A` | M7 | Mr. X 4 remix; Star Man's low gravity; Crystal Man's crystals; the Super Arrow ride; **Dark Man MK-VI** with a lying boss panel; **Mr. Y's unmasking** |
| **W2 BRACKET OF DOOM** | `$1C` | M8 | Wily 3 remix in SUPER colour; the hub is a bracket board; pair bouts in each champion's own arena via the fight loader; **Bass β duel 2** |
| **W3 WILY MACHINE 6.5** | `$1D` | M8 | Wily 4 remix; the Trophy Dispenser; **WILY MACHINE 6.5** (vanilla art, retinted, over an 8-band floor); the Wily Capsule SUPER; **the escape** with crumbling ladders |
| **The ending** | - | M8 | R4.1's scene order (§2) |

Only two main-route requirements beyond the buster and slide: the Magnet Beam from H1 on, and POWER at Gamma's phase 2
(R2.11). Every other form, alt, weapon and partner gate is on optional content.

Details: [`design/fortress.md`](design/fortress.md).

### 3.4 Core systems

| Area | v1.0 |
|---|---|
| **Controls** | SELECT is a modifier: hold + Up/Down cycles weapons, + Left/Right cycles forms; a tap toggles the last weapon. Interaction is UP with B not held |
| **Forms** | Instant swap with no cutscene (a 2 KB sheet streamed behind a 16-20 frame flash). **Every form fires every weapon's tap.** Power after the 2nd win, Jet after the 4th; the Super Adaptor (rocket fist with homing return, jet hop) in H3 |
| **Weapons** | Taps in all forms. One alt ships: **B.ATTACK's Ice Block** (freeze an enemy, stand on it), the prototype for the 7 other alts and 8 form synergies of v1.1. Slot 9 is the **MAGNET BEAM** |
| **Combat** | Two tables per boss × weapon, 4MI-style (credited): damage and post-hit invincibility. Weakness 4 dmg / 16 f, good 3/20, neutral 2/30, resisted 1/45, buster 1/60. A WEAK! pop, a stagger and a commentator line on the first weakness hit. Frozen enemies keep taking damage. No criticals; KAISHIN is deterministic |
| **Scorecard** | Out of 100: TIME 20, DAMAGE 20, VARIETY 25, SECRETS 20, STYLE 15. The VARIETY par grows with your arsenal, so a buster-only run still clears, it just earns less |
| **Economy** | No grind: bolts come only from scorecards (best score, paid once), one sponsor envelope per hidden room, and capped prizes (≤ 60 per stage) |
| **Chips (14)** | 8 venue behaviour chips (§3.2), the ENERGY BALANCER, and 5 shop chips: SHOCK ABSORBER, SPIKE GUARD, CHARGE KIT, EXCHANGER, ENERGY SAVER. Slots: 2, +1 per Beat plate, max 6. Safety nets don't stack (YASHICHI and DARUMA exclude each other) |
| **Difficulty** | CASUAL (a standard lever list per stage: reflex windows ×2, mash −40 %, timers +50 %, +1 checkpoint, secrets one step easier), NORMAL, HARD (×1.5 damage, fewer drops, no refill). 1993 RULES is v1.1+ |
| **Accessibility** | No large flash more than 3 times per second by default; REDUCED turns flashes into fades; an INPUT LAG offset for the quick-draw; a health notice at boot |

Details: [`design/systems.md`](design/systems.md).

### 3.5 Meta

Three save files on battery RAM (A/B copies with a commit marker), a title with a health notice, file select with the
difficulty pick, **the bracket** (node states, rematches, the Riot trigger, the adaptor events), **the judges' desk**
(slide-in score rows, medal stamp, prize line) and **the debrief** (a one-line hint for the first secret you missed,
4MI's predicate walk), medals and Hall of Fame points, CONFIG (language JP/EN, announcer, text speed, flashes, screen
shake, input lag, button swaps), the fortress maps, RECORDS, the **championship rating** re-derived so 100 is reachable,
and **EXTRA CONFIG**: a built-in level select and RAM editor that doubles as the test entry point.

Details: [`design/meta.md`](design/meta.md).

---

## 4. Scope: the ledger, the release ladder and the cut line

### 4.1 The ledger

The session ledger (`tools/plan/tight.py`, `tools/plan/tally.py`) is the scope authority (R0.1). A session is one focused
Claude work session. It is re-estimated from actual counts after the slice (M4) and at every ⛳ gate.

| Area | v1.0 Must (sessions) | Owner doc |
|---|---|---|
| Engine and platform | 102.5 | `tech.md` |
| Systems | 49.5 | `systems.md` |
| Meta | 31 | `meta.md` |
| The 8 venues | 109 (56 + 53) | `venues_a.md`, `venues_b.md` |
| Opening, Riot, fortress, ending | 70 | `fortress.md` |
| Release overhead (balance, tests, hardware matrix) | 16 | ledger |
| **Code total** | **378** | |
| Art (no pixel artist; R5.1) | ≈ 51.6 | `art_audio.md` |
| Music and SFX | ≈ 9 | `art_audio.md` |
| Text (397 Must strings, EN + JP, compiled and fitted) | ≈ 12 | `story.md` |
| **v1.0 total** | **≈ 451** | |

The full design (Must + Should + Could) is about 581 code sessions plus art, music and text. CX took about 5 years and
4MI about 8; v1.0 at about 450 sessions is a long project even with AI help, which is why every rung of the ladder is a
playable, shareable build (R0.5).

### 4.2 The release ladder

| Release | Contents | ≈ sessions (cumulative) |
|---|---|---|
| **v0.1 "Blizzard slice"** (M4) | new game → bracket → SUMMIT CLIMBER end to end (secret exit, hidden room, SNOW CHAINS, the Ice Block, the boss) → judges → save, reload, replay. A new file owns no forms, so the form swap comes at M5 | ~150 |
| **v0.5 "Round One"** (M6) | Opening-lite, all 8 venues, HALFTIME RIOT; the forms; the scope checkpoint | ~342 |
| **v1.0 "Championship"** (M9) | + H1, H3, H5, W2, W3, the ending; native-JP review; BPS release | ~451 |
| v1.1+ | the cut line below, re-added from the top | - |

### 4.3 The cut line (out of v1.0; comes back in this order)

1. Weapon alts and form synergies (one weapon at a time).
2. Break Man as a playable tag partner (the NPC stays in v1.0).
3. HARD per-stage poke lists and boss AI branches.
4. Each venue's second set piece and secret-arena twist.
5. H2, H4 and W1 Upgrade Lab (with ExGrafix, F-ERA, POCKET).
6. The Exhibitions, as single arenas (E4 Maze is Won't).
7. Time Attack.
8. The playable victory-lap credits (one lap).
9. The PARTs + garage + Mr. Y booth + TURBO bundle (ships with the tag partner).
10. The 1993 RULES preset.
11. GP Rush, courses, MY GP.
12. Achievements, ENGRISH, the attract crawl.

**Won't (v1):** KNOCKOUT, Exhibition Rules, the Museum/VAULT, Bass Mode, Mr. X Returns, criticals.
**If the budget tightens below v1.0's line**, cut next: merge H5's unmasking into H3; make W2 a single-arena Bass final;
reduce the Opening to 3 tutorial screens.

---

## 5. Platform and engine (tech.md owns it)

| Decision | Summary |
|---|---|
| **Cartridge** | MMC5, 1 MB PRG by **insertion**: vanilla banks `$00-$3D` stay put, new banks `$3E-$7D`, the fixed banks move to `$7E/$7F`. PRG mode 3 keeps MMC3's window shape, so every vanilla `LDY #bank / JSR $CBC0` stays valid. A go/no-go spike on Mesen comes first; the fallback is MMC3 with a re-cut scope |
| **Memory** | 8 KB CHR-RAM (no extra CHR pages). 32 KB battery PRG-RAM in 4 pages: SAVE, WORK, LAYOUT, TILES. A bank byte `$80-$83` means a RAM page, so vanilla tables can point at RAM unchanged. Bank and WORK ledgers are printed on every build |
| **Service code** | The re-entrant **C-window**: GP code runs in the `$C000` window through a `$7F` stub; the NMI and IRQ stubs save and restore the interrupted bank |
| **Stage ids** | 32 ids with a 48-byte stage-attribute record each. `$00-$07` venues, `$08-$0F` vanilla fortress (kept for regression), `$10` Opening, `$11` Riot, `$12-$15` Exhibitions, `$16-$1A` H1-H5, `$1B-$1D` W1-W3, `$1E` lap, `$20` DEV. The 45 `$51` readers are rewritten at M5 |
| **Layouts** | WRAM-resident "RAM image" layouts read by the vanilla painters unchanged, which gives one **map-edit service**, destructible blocks (T6), and CASUAL/HARD poke lists |
| **Raster** | The 27 vanilla IRQ chains are ported literally first (golden equivalence), then replaced by a double-buffered **raster list** of 24 bands; logic moves out of the IRQ |
| **Text** | A new engine: a fixed-cell **glyph cache** in an ExRAM text window (mode 0 for the whole game), EN in ALL CAPS, JP kana, pop-ups 2 × 28, dialogue and debrief 4 × 28, dictionary compression, yielding coroutines |
| **Sound** | The vanilla driver kept and reassembled; a per-track bank table; an MML compiler proven by a byte-exact round trip; a channel mute mask (the ending needs it). MMC5 pulse channels are Could |
| **Objects** | Families and sub-ids, object lists v2, a slot plan, frozen handlers, one attach state, one free-flight vehicle state, one HUD widget module; a lag cap of **9 occupied slots** until M3 re-measures |
| **The fight loader** | FIGHT_CTX lets any boss be fought from a hub, the test mailbox or EXTRA CONFIG and return correctly (W2 is built on it) |
| **Dev tooling** | BPS builds, a hook registry and allocator, EXTRA CONFIG, warps, a test mailbox, golden movies with RAM pokes on FCEUmm (headless) and checks on Mesen |

What the research already finished (tech §16.1): the RAM map, linear disassemblies of every bank, the level
extractor/renderer with a byte-exact round trip and 16 full stage maps, the object/AI/damage tables, the sound decoder,
the 168 text scripts, the metasprite format, the IRQ chain map, the 45 stage-id readers, warps and 87 savestates, and
MMC5 probes on FCEUmm.

Details: [`design/tech.md`](design/tech.md).

---

## 6. Art and audio (art_audio.md owns the budgets)

- **No pixel artist is assumed** (R5.1). Reuse, recolours, composites of vanilla RM6 sprites and programmatic art come
  first; Claude's drafts are final, and a human pass is optional polish.
- **Never overwrite Capcom art in place**: new tiles go in new banks and tileset slots. No byte imports from other
  Rockman ROMs in v1.
- **Break Man and Bass β are composited from Rock's sheet.** 16×16 face icons with name labels instead of portraits in
  v1.0. One size per background boss. Frame caps: 8 per enemy, 16 per boss.
- **An art-acceptance gate** with screenshots for the user at every milestone.
- **Must art:** 2,567 background and 1,968 sprite tiles (36 % of them reuse or composites) and 354 frames, ≈ 51.6
  sessions. Each asset is costed by method: reuse, composite, programmatic or Claude draft.
- **Must music:** G00 GRAND PRIX MARCH through G04 (BETA's theme), the ending's LAST MATCH arrangement (2A03 stems), a
  2-second whistle jingle, 21 new SFX, and the channel mute mask. Everything else falls back to vanilla tracks
  until v1.1.

Details: [`design/art_audio.md`](design/art_audio.md).

---

## 7. Milestones

From RULINGS §6 (re-baselined by R8.1). Cumulative sessions in brackets. ⛳ = the user plays it. Every milestone ends with a playable build,
green test suites, `STATUS.md` updated, the bank ledger printed and art-acceptance screenshots.

| M | Contents | ≈ |
|---|---|---|
| **M0** | Workbench: scaffold, build, BPS, hook registry, allocator, test runner, vanilla golden suite, ledgers; reassemblable fixed banks and sound driver; round trips and censuses. **MMC5 go/no-go spike on Mesen** | [13] |
| **M1** | Literal MMC5 port with golden equivalence; PRG-RAM, save skeleton, test mailbox | [26] |
| **M2** | Slice engine: families and sub-ids; WRAM layouts and the map-edit service; CHR set table v2 and the minimal art tools; level pipeline; raster list; **text v1a**; track table and MML; save, file-select-lite, bracket-lite, results, debrief, EXTRA CONFIG | [79] |
| **M3** | Slice systems: SELECT (weapons); taps; the boss tables, WEAK!, the frozen tick, the Ice Block; scorecard and bolts; shop (3 chips); T6, X-BONK, X-WRAP; HUD widgets; the commentator bus; the attach state's core (the condor) | [~124] |
| **M4** ⛳⛳ | **SUMMIT CLIMBER end to end (v0.1)**. Re-estimate the ledger | [~150] |
| **M5** | Stage-attribute table; the form swap, forms firing taps, adaptors by win count; Opening-lite; PERSIAN PALACE, LOST JUNGLE, ATLANTIS RUINS, EDO NINJA ROW | [~258] |
| **M6** ⛳ | Text v1b; T1-lite; HERO'S QUEST, HIGH NOON FRONTIER, SKY ACE; HALFTIME RIOT (**v0.5 "Round One"**) | [~342] |
| **M7** | BG-boss tooling, the fight loader; H1, H3, H5 | [~398] |
| **M8** ⛳ | W2, W3, the ending | [~434] |
| **M9** | Native-JP review, balance, emulator and hardware matrix, BPS release (**v1.0**) | [~451] |

The cumulative figures add up each design doc's own per-milestone estimates (RULINGS R8.1). Round 1 had put the slice
at about 115; counted honestly it is about 150, because the slice builds most of the engine, the whole scorecard and
economy, and the art and music pipeline before the first venue.

**M0 in detail** (tech §16.3; 12.5 sessions):

1. **M0.0** The MMC5 go/no-go spike: six probe ROMs on Mesen (and the user's cart, if any): NES 2.0 header, 32 KB
   PRG-RAM pages, ExRAM as a nametable from a mid-frame `$5105` write, IRQ line timing, 256 B/frame CHR streaming.
   Record go, or a contingency, in `STATUS.md`.
2. **M0.1** Repo scaffold (`src/`, `assets/`, `tools/build/`, `tests/`); `build.py` no-op path (vanilla in → vanilla out,
   MD5 check); `bps.py` with a round-trip test.
3. **M0.2** Hook registry and allocator, seeded with the verified free ranges; the bank and WORK ledgers.
4. **M0.3** `tests/run.py` on `tools/analysis/emu.py`: movies = inputs plus scripted RAM pokes; record the vanilla golden
   suite (NORMAL + EN).
5. **M0.4** Reassemblable Ophis source of `$3E/$3F` and the sound driver, byte-identical.
6. **M0.5** `.lvl` text format: all 16 stages rebuilt byte-identically.
7. **M0.6** `mml.py` round trip of the 36 vanilla songs.
8. **M0.7** Censuses: `$51`/`$063D`/`$9B` readers, sound-stream readers, damage-step kinds.
9. **M0.8** `stagetab.py`: the 48-byte rows reproduce every vanilla value.

**Exit:** the spike says go; vanilla round-trips through `build.py`; the unit suite is green; the vanilla golden suite is
recorded.

**Testing policy:** golden movies on NORMAL + EN only; one smoke movie per other setting per milestone; movies
re-recorded only at gates; test overhead about 10 % of code sessions.

---

## 8. Top risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Scale.** ≈ 450 sessions is years of part-time work | The release ladder makes every rung shareable; the ledger is re-estimated at M4 and every gate; the cut line is pre-ordered |
| 2 | **MMC5 on real hardware and flash carts** is unverified; FCEUmm is too forgiving (64 KB PRG-RAM, CHR wrap, timing) | The Mesen spike before any port work; every gate checked on Mesen; the MMC3 fallback |
| 3 | **The slice is big** (~150 sessions before the first playable venue) | Forms moved out of the slice (R8.2); the M4 re-estimate calibrates everything after it |
| 4 | **Lag.** Set pieces sit at the 9-slot cap | Count every occupied slot; M3's OAM-builder work may raise the cap; artcheck enforces it |
| 5 | **Text space.** Dense screens (Plant: 0 free BG tiles) defer pop-ups; Must strings run over ~350 | Glyph cache with ROM restore; story's trim order |
| 6 | **IRQ timing** differs between emulators and hardware (the 8-band floor, the train) | Per-band timing tests on both emulators; the floor is decoration, collision is not raster-based |
| 7 | **No pixel artist.** Break Man, Bass β, Gamma and Dark Man are composites and drafts | Art gates with screenshots at every milestone; a human pass stays optional |
| 8 | **Attribution holes.** Enemies with custom death code could skip the scoring hook | The M0 censuses and coverage runs list every death path |
| 9 | **Cartridge space** | v1.0 uses about 41 of 64 new banks; the bank ledger is printed on every build |
| 10 | **Native-JP review** is an external dependency that gates release | Ask early (§9); EN can ship first if needed |

Each design doc has its own risk list; tech's (14 items) is the longest.

---

## 9. The user's answers (2026-10-29)

1. **Hardware:** emulator-only is acceptable; real hardware is a nice-to-have, never a reason for an exotic cart.
2. **Art:** no artist yet. Commissioning depends on how Claude's sprites look, so a sample sprite or two comes early
   (an M2 art-pipeline deliverable, shown at the first art gate).
3. **Japanese review:** same answer as art; decide later. JP text stays draft until then.
4. **Title:** **ROCKMAN 6 GP: 史上最大の再会!!** (*Shijō Saidai no Saikai*, "The Greatest Reunion in History"), a
   pun on the original 史上最大の戦い (*Tatakai*): the returning champions, and the returning villain. Chosen by the user.
5. **Pace:** about 2 sessions a week if sessions are as heavy as the planning one, 3-4 if lighter; build sessions should
   be lighter. At 3 a week the slice (~150) is about a year and v1.0 (~451) about three, before any gain from better or
   cheaper models.

## 10. How the next session starts (copy this checklist)

1. Upload `Rockman 6 - Shijou Saidai no Tatakai!! (Japan).nes` and say **"begin M0"**.
2. Claude runs `tools/setup_env.sh` (Python packages into `.pylib/`; PyPI works, GitHub downloads are blocked in the cloud
   environment), places the ROM at `roms/rm6j.nes` and verifies MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`.
3. Claude boots it headlessly with `tools/analysis/emu.py` (`Emu('roms/rm6j.nes')`, then `run`, `shot`; see
   `tools/analysis/README.md`) and checks the title screen.
4. Claude starts **M0.0, the MMC5 go/no-go spike** (§7). Mesen isn't available in the cloud container, so the spike's probe
   ROMs are built and run on FCEUmm there, and **the user runs them on Mesen** (and any cart) and reports back. That
   report is the gate.
5. Then M0.1 onward: read `STATUS.md` → the next unchecked task → work → tests → commit → update `STATUS.md`.
6. Optional but valuable: play vanilla RM6 in **Mesen 2** with the **Code/Data Logger** on (Debug → Code/Data Logger),
   touching every stage once, then upload the `.cdl` file. It confirms code, data and free space beyond the shadow6
   coverage the research already has.

---

## 11. Document index

### Design (`docs/design/`)

| Doc | Owns | Size |
|---|---|---|
| [`RULINGS.md`](design/RULINGS.md) | Binding rulings: after the round-1 review (§0-§7: scope, platform, combat, content, story, art, milestones, user questions) and after round 2 (§8: the re-baselined ledger and ladder, what the slice builds, the channel drop, text, the ending's gags and names, staging, engine) | ≈ 540 lines |
| [`reconcile.md`](design/reconcile.md) | Round 3: every cross-doc request left by round 2, routed to its owner doc, with its outcome | ≈ 90 |
| [`BRIEF.md`](design/BRIEF.md) | Founding decisions: identity, cast, structure, corrections to v1, conventions | ≈ 230 |
| [`tech.md`](design/tech.md) | Cartridge and bank ledger, PRG-RAM, memory map, stage ids and the fight loader, WRAM layouts and map edits, pipelines, object framework, raster list, text and sound engines, saves, dev tooling, lag, milestones | ≈ 2,350 |
| [`systems.md`](design/systems.md) | Controls, forms, weapons, combat tables, weakness feedback, scorecard, bolts, shop, chips, Beat, the tag partner, pickups, difficulty | ≈ 2,100 |
| [`meta.md`](design/meta.md) | Save model, title and file select, the bracket and pit stop, the judges' desk and debrief, medals, the rating, unlocks, CONFIG, EXTRA CONFIG, post-game modes | ≈ 1,860 |
| [`venues_a.md`](design/venues_a.md) | SKY ACE, HERO'S QUEST, HIGH NOON FRONTIER, LOST JUNGLE, screen by screen | ≈ 1,640 |
| [`venues_b.md`](design/venues_b.md) | SUMMIT CLIMBER (the slice, specified completely), PERSIAN PALACE, ATLANTIS RUINS, EDO NINJA ROW | ≈ 2,000 |
| [`fortress.md`](design/fortress.md) | Opening, HALFTIME RIOT, Exhibitions, Hall of Fame H1-H5, Super Wily Castle W1-W3, the ending, Mr. X Returns | ≈ 2,230 |
| [`story.md`](design/story.md) | Every word: scenes, commentary, death tables, hints, plaques, help pages, the ending; EN and JP | ≈ 2,400 |
| [`art_audio.md`](design/art_audio.md) | Tile, frame and byte budgets per asset; tileset slots; the no-artist art method and acceptance gate; the track list and SFX | ≈ 1,930 |
| [`crossrefs.md`](design/crossrefs.md) | Round-1 cross-references between the docs | ≈ 460 |
| [`review_feasibility_design.md`](design/review_feasibility_design.md), [`review_consistency_scope.md`](design/review_consistency_scope.md) | The four critics' findings (the ids RULINGS cites) | ≈ 2,370 |

Each design doc opens with a "v1.0 scope" section (what ships, sessions, milestones) and ends with Lessons applied, Risks,
Open questions and Changes in round 2.

### Research (`docs/research/`)

| Where | What |
|---|---|
| [`research/README.md`](research/README.md) | Field guide: how the research was done and where everything is |
| `research/rm6/` | Vanilla Rockman 6: RAM, engine, levels (format, renderer, 16 full maps), stages, fortress, text, cheats; `SUMMARY.md` §4 audits plan v1 |
| `research/cx/` | Rockman CX: engine, systems, stages, fortress, graphics, text, cheats; `SUMMARY.md` |
| `research/r4mi/` | Rockman 4 Minus Infinity: engine (MMC5), systems, stages, Cossack and Wily, modes, graphics, text, cheats; `SUMMARY.md` |
| [`DECONSTRUCTION.md`](DECONSTRUCTION.md) | The first, readme-level teardown (superseded in depth by the summaries) |

### Tools

| Where | What |
|---|---|
| `tools/setup_env.sh` | Installs the toolchain into `.pylib/` (Ophis, py65, stable-retro FCEUmm, numpy, pillow) |
| `tools/analysis/` | `emu.py` (headless FCEUmm harness: run, poke, freeze, save/load, screenshots, PPU dumps), patchers (`ips.py`, `cxpatch.py`, `pbtps.py`), bank maps, disassembler, per-game tools (`rm6/levels.py`, `rm6/shadow6.py`, …). See its README |
| `tools/plan/` | The session ledger: `tight.py` (v1.0) and `tally.py` (every item by tier) |
