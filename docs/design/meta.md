# Rockman 6 GP: progression, meta-game and modes (meta.md)

Owner: design-meta. Status: **v1**. Scope: everything outside a stage's own screens. That covers saving and loading,
the title and file select, the bracket stage select, the judges' debrief, medals and Hall of Fame points, the
championship rating, the unlock chain, every post-game mode, achievements, CONFIG and ENGRISH. The doc also gives the
byte layouts for the save and unlock flags.

Out of scope, owned elsewhere:

- the scorecard maths, bolts, chips and the shop (`systems.md`);
- stage and boss content (`venues_a.md`, `venues_b.md`, `fortress.md`);
- dialogue and cast beats (`story.md`);
- the MMC5 port, bank and stage-id allocation (`tech.md`);
- the art and music lists (`art_audio.md`).

Where this doc needs something from those, it says so in **Cross-doc dependencies** (§15).

Tags follow BRIEF §8: **[engine-ok]**, **[new-code]**, **[new-art]**, **[new-music]**, size **S/M/L**, tier
**Must/Should/Could**. Facts come from `docs/research/*/` (cited as `rm6/ram.md`, `r4mi/modes.md`, and so on).

---

## 0. The meta layer in one page

The premise reaches the menus too (CX lesson 1):

- the file select is an **entrant registration desk**;
- the stage select is a **bracket**;
- every clear ends at the **judges' desk** with a scorecard and one hint;
- the ending prints a **championship rating** out of 100, and Break Man gives the 4MI-style debrief;
- the post-game is **SPECIAL EVENTS**: Time Attack, GP Rush (a boss rush on one fight table), Exhibition Rules,
  Records, the Museum and EXTRA CONFIG.

**Progression flow:**

```
POWER ON → license → attract crawl → TITLE
TITLE → GAME START → FILE SELECT (3 files)
   new file  → pick difficulty → OPENING CEREMONY (M00) → BRACKET
   old file  → BRACKET  (or the fortress map, if the file is inside H1-W3)
BRACKET (8 venues, any order; SELECT = PIT STOP, B = Exhibition layer)
   2nd win → POWER adaptor event     4th win → JET adaptor event + SEMIFINAL RIOT intro
   SEMIFINAL (M09, centre) must be cleared before the other 4 venues reopen
   pairs of secret exits light Exhibition badges E1-E4 (SELECT layer)
   8 wins → centre = TROPHY → theft scene → HALL OF FAME map H1-H5 → unmask → SUPER WILY CASTLE W1-W3
   → ending → playable victory-lap credits → CHAMPIONSHIP RATING + Break Man's debrief → TO BE CONTINUED…
   → title; SPECIAL EVENTS now on the title menu; the file reopens in the post-game bracket
```

| Layer | Must | Should | Could |
|---|---|---|---|
| Saves | 3 files, A/B copies, checksums, autosave | file COPY | — |
| Front end | title, file select, CONFIG | attract crawl | hidden PASS WORD gag |
| Bracket | 8 venues, Semifinal trigger, centre progression, pit stop | Exhibition layer | animated Riot intro |
| Judging | debrief predicates + hints, medals, HoF points | escalating hints | — |
| Ending | championship rating, Break Man debrief | — | — |
| Post-game | EXTRA CONFIG (it is also the dev tool), RECORDS | Time Attack, GP Rush, achievements | Exhibition Rules, Museum, KNOCKOUT, Bass Mode, Mr. X Returns, ENGRISH |

---

## 1. The save model

### 1.1 What vanilla and the references do (facts)

- **Vanilla RM6** has no save at all. Passwords hold 13 bits: 8 bosses, 4 plates and the Balancer, encoded in 8,192
  states, two encodings each. Fortress progress, lives and E-tanks are never kept, and WRAM is never enabled
  (`rm6/engine.md` §7, `rm6/SUMMARY.md` §3).
- **CX** has 3 battery slots, but they are 42 bytes of WRAM, interleaved, with an 8-bit ADC checksum. A bad sum
  silently resets the slot to a new game. HP, energy and the checkpoint are not saved. The game saves after bosses,
  heart tanks and stage exits, and from the game-over menu (`cx/engine.md` §7).
- **4MI** has one save file plus a system block. Each block has a **persistent copy and a working copy**, a strong
  cheap checksum, and autosaves on every death and clear. Its checksum is a 16-bit sum, a XOR, even and odd XORs, an
  inverted copy of each, and a combined byte (`r4mi/cheats.md` §3).

**The 4MI double-copy lesson** has two halves:

1. **Keep two copies and a strong checksum.** A torn write (power cut, reset) then never destroys the only good
   copy.
2. **Handle a bad block gracefully, on every screen that reads it.** 4MI forgot this half. If the game block is
   invalid when SPECIAL MODE opens, `$4C:$9D55` calls the check at `$40:$AA09`, which branches into a "SAVE DATA
   BROKEN" handler that loops forever on a black screen (`r4mi/cheats.md` §2).

GP keeps both halves. It goes one step further than 4MI's commit-from-working-copy: the copies **ping-pong**. Each
write goes to the *older* copy, so the newest good copy is never touched.

### 1.2 Hardware and placement [new-code] S · Must

The save lives in **PRG-RAM page 0** (8 KB, battery-backed), mapped at `$6000-$7FFF` with `$5113 = 0`.

- The NES 2.0 header must declare this page as **PRG-NVRAM**. 4MI's header declares PRG-RAM size 0, the r4mi lesson
  12 warning (`tech.md` owns the header).
- If `tech.md` gives GP more PRG-RAM (16-32 KB of WRAM-resident stage sections), pages 1+ are work RAM. The save
  module then maps page 0 at `$6000` only while it loads or commits; MMC5 can also map RAM pages at
  `$8000-$DFFF` through `$5114-$5116` with bit 7 clear.
- **Write protection** (`$5102 = 2`, `$5103 = 1` to write): if every work-RAM byte sits in other pages, the save
  routine opens the gate only around a commit and closes it after (`$5102 = 0`). If work RAM shares page 0, the gate
  must stay open, and the A/B copies plus checksums are the only defence. They are designed to be enough on their
  own.

**Page 0 map:**

| Range | Size | Use |
|---|---|---|
| `$6000-$63FF` | 1 KB | SYS-A: system block, copy A |
| `$6400-$67FF` | 1 KB | SYS-B |
| `$6800-$69FF` | 512 B | FILE1-A |
| `$6A00-$6BFF` | 512 B | FILE1-B |
| `$6C00-$6DFF` | 512 B | FILE2-A |
| `$6E00-$6FFF` | 512 B | FILE2-B |
| `$7000-$71FF` | 512 B | FILE3-A |
| `$7200-$73FF` | 512 B | FILE3-B |
| `$7400-$75FF` | 512 B | **LIVE FILE**: the running game's file image, laid out exactly like a file block (§1.6) |
| `$7600-$79FF` | 1 KB | **LIVE SYS**: the running system block |
| `$7A00-$7A1F` | 32 B | **TEST MAILBOX** (§9.6) |
| `$7A20-$7FFF` | 1,504 B | free for `tech.md` (work RAM if page 0 is the only page) |

**The LIVE FILE is the format.** A file's saved payload and the running state are the same 512-byte image, so a save
is "checksum + copy" with no serialiser to keep in sync.

The vanilla variables that stay in CPU RAM are gathered into the image at each commit and scattered back at load,
as 4MI does at `$40:$AF1F` / `$A9A3`:

- weapons `$0688-$0691`;
- E-tanks `$06A1`;
- lives `$A9`.

The play-time counter ticks in CPU RAM or work RAM, never inside LIVE, so the NMI can never change the image while it
is being checksummed. It is folded in just before each commit.

### 1.3 Block trailer and checksum [new-code] S · Must

Every block (file: payload `$000-$1EF`; system: payload `$000-$3EF`) ends in a 16-byte trailer. The checksum is 4MI's
scheme (`r4mi/cheats.md` §3, about 40 lines of 6502), with a commit marker added:

| Trailer offset | Contents |
|---|---|
| +0 / +1 | SUM: 16-bit sum of the payload bytes, lo / hi |
| +2 | XOR of all payload bytes |
| +3 | XOR of the even offsets |
| +4 | XOR of the odd offsets |
| +5..+9 | +0..+4, each XOR `$FF` |
| +A | MIX = +0 ^ +1 ^ +2 ^ +3 ^ +4 |
| +B | layout version (a copy of header +4) |
| +C / +D | generation (a copy of header +6/+7) |
| +E / +F | **COMMIT marker `$A5 $5A`**, written last |

A copy is **valid** only if all of these hold:

- the magic matches;
- the commit marker is `$A5 $5A`;
- every checksum byte matches;
- the version is not newer than the ROM's;
- the trailer's generation equals the header's.

### 1.4 Write and load rules [new-code] S · Must

**Commit (save) one block:**

1. Fold the play-time counter and the CPU-RAM variables into LIVE.
2. Increment LIVE's generation (16-bit) and compute the trailer in LIVE.
3. Pick the **target copy**: an invalid copy if there is one, else the one with the older generation.
4. Invalidate the target first: write magic byte 0 = `$00` and marker +E = `$00`.
5. Copy bytes `$001` to the end of the trailer except the marker.
6. Write magic byte 0, then marker +E/+F last.

A file commit checksums and copies 512 bytes: about 10,000 CPU cycles for the checksum and 7,000 for the copy, or
0.6 of a frame (a system commit is twice that). So it fits anywhere. It runs with the
PPU idle or during a fade, and shows a 30-frame **SAVING** icon (Eddie with a clipboard) so the player trusts it.

**Load one block:**

- **Both copies valid:** take the newer generation. Compare by serial-number arithmetic:
  `(int16)(genA - genB) > 0` means A is newer.
- **One copy valid:** take it. The next commit overwrites the bad one, so the block repairs itself.
- **Neither valid:** the file is **BROKEN**. The file card says `BROKEN DATA` and offers ERASE only. **No screen ever
  hangs on a broken block**: every reader (title, file select, RECORDS, EXTRA CONFIG) has a BROKEN path. A broken
  system block re-initialises to defaults with a one-line notice.

**Version migration.** Header byte +4 is the layout version, starting at 1. On load, a block with an older version
runs a migration routine per step (v1→v2, …) before use. New fields only ever take reserved bytes, so a v1.0 save
still loads in v1.1. This matters for a patch that will see bug-fix releases [new-code] S · Must.

**COPY** (Should): copy the source's newest valid copy into the target's LIVE image, set the slot byte and generation
1, and commit twice so both copies are fresh.

**ERASE:** zero the magic of both copies. It asks for START+A (§2.3).

### 1.5 Autosave points [new-code] S · Must

| # | When | What changes | Why |
|---|---|---|---|
| 1 | The NEW GAME difficulty is confirmed | the new file (both copies) | The file exists before the Opening starts |
| 2 | **Stage entry** (after READY) | `IN_MATCH` = meta index + 1; attempts | The unplug detector (§1.7) |
| 3 | **Every death** (during the death fade) | KOs, lives, stage KOs, CHAMP_KO | Deaths count, as in 4MI; resetting cannot hide them |
| 4 | **Stage clear**, after the scorecard and bolts | clears, secrets, best score/time, weapons, `IN_MATCH = 0` | The main progress save |
| 5 | Leaving the **pit stop** | bolts, chips, consumables | Purchases stick |
| 6 | The game-over choice | game overs, lives refill, `IN_MATCH = 0` | |
| 7 | After each **bracket event** plays (§3.6) | EVENTS_SEEN | Story beats play once |
| 8 | The championship result | rating, CHAMP TIME, CLEARED flag | |
| 9 | Leaving CONFIG, a new TA/Rush record, an unlock or achievement | **system block** only | |

**Not saved** (each is restored to a fixed value instead):

| Not saved | On load it becomes |
|---|---|
| HP | full |
| weapon energy | full; vanilla fills it from the owned flags at stage start, `$3B:$BA3F` |
| checkpoint | the stage start; a load never resumes mid-stage |
| current form | Normal |
| Break Man's per-life call | available |

A loaded file always resumes at the **bracket**, or at the **fortress map** of the next uncleared H/W stage.
Vanilla never saved fortress progress; GP saves after every fortress stage.

### 1.6 FILE block layout (512 B) [new-code] S · Must

"Meta index" is the stage's row in the meta tables (§1.8), not the engine stage id: `tech.md` owns the ids, and the
stage-attribute table carries a `meta` column. Multi-byte values are little-endian.

| Offset | Size | Field | Notes |
|---|---|---|---|
| `$000` | 4 | magic `'R' '6' 'F' n` | n = `'1'`..`'3'`, `'S'` = scratch (never committed) |
| `$004` | 1 | layout version | 1 |
| `$005` | 1 | FILEFLAGS | b0 ACTIVE; b1 CLEARED (won the championship once); b2 **EDITED** (EXTRA CONFIG wrote it, §9.6); b3 BASS (Bass Mode file); b4 HARD_CLEAN (HARD preset with all sub-settings since NEW GAME, never lowered); b5 R1993_CLEAN (likewise for 1993); b6-7 reserved |
| `$006` | 2 | generation | |
| `$008` | 1 | IN_MATCH | 0 = none, else meta index + 1 |
| `$009` | 1 | DIFF preset | 0 CASUAL, 1 NORMAL, 2 HARD, 3 1993, 4 EDIT |
| `$00A` | 1 | DIFF A | b0-1 DAMAGE (0 ×1, 1 ×0.5, 2 ×1.5, 3 ×2); b2-3 DROPS (0 NORMAL, 1 LESS, 2 MORE, 3 NONE); b4 CRITICALS on; b5 HARD on; b6 GUARDS on; b7 RULES = 1993 (`systems.md` §13.1) |
| `$00B` | 1 | DIFF B | b0-3 LIVES 1-9; b4-6 E-TANK FLOOR 0-4; b7 reserved |
| `$00C` | 1 | LOWEST | The easiest preset ever active (0 CASUAL < 1 NORMAL < 2 HARD); for achievements |
| `$00D` | 1 | DIFF C | b0-1 REFILL on respawn (0 NONE, 1 HALF, 2 FULL); b2-7 reserved |
| `$00E` | 2 | reserved | |
| `$010` | 3 | STAGE_CLEAR | 24 bits by meta index: bit m = meta stage m cleared at least once |
| `$013` | 1 | STORY_BEAT | Story position; `story.md` defines the values. Meta reads only the bracket states (§3.5) |
| `$014` | 1 | EVENTS_SEEN | b0 POWER handed over; b1 JET handed over; b2 RIOT intro; b3 RIOT lifted (Semifinal won); b4 TROPHY theft; b5 BREAK MAN joins; b6 Mr. Y unmasked; b7 post-game bracket intro |
| `$015` | 1 | EVENTS_SEEN2 | b0-3 badge E1-E4 lit; b4 SUPER adaptor handed over; b5 BREAK MAN WALKS (doping, §6.3); b6-7 reserved |
| `$016` | 1 | FORMS | b0 POWER; b1 JET; b2 SUPER (real save flags, BRIEF §4); b3 TAG (Break Man callable); b4-7 reserved for `systems.md` |
| `$017` | 1 | FORM_DEBUT | b0 POWER, b1 JET, b2 SUPER: the vanilla Rush-docking cutscene has played once for this form (`systems.md` §1.3) |
| `$018` | 24 | SECRETS[24] | By meta index. b0 SECRET EXIT; b1 HIDDEN ROOM; b2 BEHAVIOUR ITEM (chip); b3 PLATE; b4 SPONSOR ENVELOPE taken (`systems.md` §7: 30 bolts, once per save); b5-7 MISS (§4.1; saturates at 7). For non-venue stages, b0-4 mean what the stage's owner defines. The 4 plate bits (Tomahawk, Yamato, Knight, Centaur) are `systems.md`'s PLATES |
| `$030` | 2 | WEAPONS | `$030` b0-7 = the 8 champion weapons by venue id; `$031` b0 MAGNET BEAM (slot 9, `systems.md` §3.10); b1-7 reserved |
| `$032` | 1 | E-TANKS | max 4 (`systems.md` §8) |
| `$033` | 1 | W-TANKS | max 2 |
| `$034` | 1 | LIVES | On load: lives = max(saved, the file's LIVES setting), as in 4MI |
| `$035` | 3 | reserved | consumables, if `systems.md` adds any |
| `$038` | 2 | BOLTS | 0-999 (`systems.md` §7 caps the counter at 999) |
| `$03A` | 2 | CHIPS_OWNED | 16 bits, in `systems.md` §9.2's order (15 chips) |
| `$03C` | 2 | CHIPS_EQ | 16 bits: equipped chips (`systems.md` §9.1 uses a bitmask, not slot positions) |
| `$03E` | 1 | PARTS_GOT | 8 bits, SNOW GUST SEED EMBER KATANA FEATHER CREST SHELL (`systems.md` §9.3): PART dropped once per save |
| `$03F` | 1 | PARTS_USED | spent in the garage or at Mr. Y's booth |
| `$040` | 1 | METALLS | Full-power Metall kills, saturating at 255 (IRON HELMET at 20, `systems.md` §9.2) |
| `$041` | 4 | WEAKFOUND | 32 bits, one per boss row: weakness found (`systems.md` §5 item 6, Could) |
| `$045` | 1 | RATEFLAGS | b0 **DOPED** (Y-TURBO taken at Mr. Y's booth, §6.3); b1 MR. X CARD found; b2 RIVAL (Semifinal won with no damage); b3 **CHAMP_KO** (died in a champion's boss room; negative); b4 DOVE run achieved (`systems.md` chip 10); b5-7 reserved |
| `$046` | 3 | TAG_STAGES | 24 bits: meta stages where Break Man was called |
| `$049` | 1 | BASS_ADAPT | The damage column the player used most in the Semifinal duel; Bass β's W2 armour starts adapted to it (`systems.md` SC6) |
| `$04A` | 6 | reserved | `systems.md` / `story.md` |
| `$050` | 240 | STAGEREC[24] × 10 | +0 best score (0-100, `$FF` = none); +1 badge: b0-1 the preset of that best score (0 C, 1 N, 2 H, 3 93), b2 **asterisk** (earned with Y-TURBO equipped), b3-7 reserved; +2 best PAY (0-160, `systems.md` §6.6: a replay pays the improvement over this); +3 clears (saturates at 255); +4/5 best clear time in frames (saturates at `$FFFF`); +6/7 KOs; +8/9 time spent, in 256-frame units |
| `$140` | 4 | PLAYTIME | frames, 32-bit (ticks only while a file is active) |
| `$144` | 4 | CHAMP_TIME | PLAYTIME at the first championship; 0 = none |
| `$148` | 2 | KOS | total deaths |
| `$14A` | 2 | GAMEOVERS | |
| `$14C` | 1 | UNPLUGS | saturates at 255 |
| `$14D` | 3 | BOLTS_EARNED | 24-bit |
| `$150` | 3 | BOLTS_SPENT | 24-bit |
| `$153` | 2 | TAG_CALLS | Break Man calls |
| `$155` | 2 | ETANKS_USED | |
| `$157` | 2 | WEAK_HITS | first-weakness pops |
| `$159` | 1 | BEST_RATING | 0-100, `$FF` = none |
| `$15A` | 1 | LAST_RATING | |
| `$15B` | 7 | LAST_ROWS | the seven rating rows (§6) |
| `$162` | 142 | reserved | growth (§16 risk 3) |
| `$1F0` | 16 | trailer | §1.3 |

### 1.7 The unplug detector [new-code] S · Should

`IN_MATCH` is set at stage entry and cleared at a clear, a RETIRE or a game over. If a file loads with
`IN_MATCH ≠ 0`, the stage was abandoned by power-off or reset. The load then:

- adds 1 to UNPLUGS and to that stage's KOs;
- queues a commentator line for the bracket. Kalinka: *"We lost the feed during WIND MAN's match! …Did someone trip
  over the stadium cable?"*

Deaths are already saved on the spot (autosave 3), so unplugging gains nothing. The counter is flavour, plus one
rating point (§6).

### 1.8 Meta index (save-table rows)

| Meta | Stage | Meta | Stage |
|---|---|---|---|
| 0 | Opening Ceremony | 14-18 | Hall of Fame H1-H5 |
| 1-8 | the 8 venues, in vanilla stage-id order: Blizzard, Wind, Plant, Flame, Yamato, Tomahawk, Knight, Centaur (meta = vanilla id + 1) | 19-21 | Super Wily Castle W1-W3 |
| 9 | Semifinal Riot | 22 | Mr. X Returns (Could) |
| 10-13 | Exhibitions E1-E4 | 23 | Victory lap (the playable credits; Time Attack only) |

Medals and HoF points count meta 0-21: the BRIEF's 22 stages.

---

## 2. Title flow and file select

### 2.1 Boot and attract [new-code] S · Must, [new-art] M · Must

1. **License screen**: vanilla script `$1F` (`rm6/text.md` §5.1), plus one new line, `ROCKMAN 6 GP — FAN PATCH`
   [engine-ok + text].
2. **Attract crawl**: replaces vanilla's "IN THE YEAR 20XX…" (scripts `$50-$5E`). It is `story.md`'s GP opening
   told in 6 typed panels; START skips it.
3. **Title**:
   - the new logo **ROCKMAN 6 GP**, subtitle **史上最大のグランプリ!!** (logo art; vanilla's only kanji were logo art
     too);
   - the vanilla moon backdrop, kept;
   - music: the vanilla title `$19` until `art_audio.md` supplies a GP fanfare.

Title menu (cursor ▶, vanilla style):

| Item | When shown | Does |
|---|---|---|
| GAME START | always | → FILE SELECT |
| SPECIAL EVENTS | once any unlock bit is set (§7) | → the post-game menu (§9) |
| CONFIG | always | → CONFIG (§11), global settings only; the difficulty group is per file |
| *(hidden)* PASS WORD | hold SELECT on the title for 2 s | The vanilla password grid, fully working. A valid vanilla password gets Kalinka: *"Passwords? It's 20XX! We have batteries now."* It sets no progress. Could, S: a quirk kept on purpose (rm6 lesson 8). The vanilla codec `$3F:$F3D0` is reused |

### 2.2 FILE SELECT: "ENTRANT REGISTRATION" [new-code] M · Must, [new-art] S · Must

Three cards stacked vertically, each 6 tiles tall. Kalinka holds the clipboard at the right.

```
┌ FILE 1 ───────────────────────── NORMAL ┐
│ [8 venue icons: lit = won, medal colour]  │
│  E1 E2 E3 E4   H1-H5 ▮▮▮▯▯   W ▯▯▯        │
│  HOF PTS 37    BOLTS 625     12:34:56     │
│  ★ RATING 87 (FINALIST)        TIUNS 143   │
└───────────────────────────────────────────┘
```

| Card shows | From |
|---|---|
| venue icons, coloured by medal (none / bronze / silver / gold / platinum) | STAGEREC best score |
| Exhibition, Hall of Fame and Castle progress | STAGE_CLEAR |
| HOF PTS | §5.2 |
| BOLTS | `$038` |
| play time h:mm:ss | `$140` |
| difficulty badge (CASUAL / NORMAL / HARD / 1993, plus `EDIT` if any override is set) | `$009` |
| ★ and the best rating, if CLEARED (with `*` if DOPED) | `$159` |
| a red `*` if EDITED, a Bass icon if BASS | FILEFLAGS |
| KOs (EN "KNOCKOUTS", ENGRISH "TIWNS", §12) | `$148` |

An empty file shows `NEW ENTRANT`; a broken one shows `BROKEN DATA` (§1.4).

Commands (UP/DOWN pick the card, A/START open a command row under it):

| Command | Rule |
|---|---|
| **START** (on a used file) | Load; go to the bracket or the fortress map |
| **NEW** | On an empty file: go straight to the difficulty pick. On a used file: `OVERWRITE? NO / YES`, with NO first, and YES needs **START+A** (4MI's stray-START guard, `r4mi/modes.md` §4) |
| **COPY** (Should) | Pick the target file; the same overwrite guard |
| **ERASE** | `ERASE? NO / YES`, START+A |
| **ENTRANT** (after the first clear, Could) | Toggles ROCKMAN / BASS β for a NEW file (§9.7) |

### 2.3 NEW GAME: difficulty pick [new-code] S · Must

There are four big panels, each with one line of description:

| Preset | Line |
|---|---|
| CASUAL | "Half damage, safety net, extra lives. The crowd is on your side." |
| NORMAL | "The Grand Prix as designed." |
| HARD | "Remixed venues, meaner champions, no free drops." |
| 1993 | "Vanilla rules. No chips, no shop, no mercy. Like it's 1993." |

The pick writes DIFF preset, A, B and LOWEST, and sets HARD_CLEAN or R1993_CLEAN when the preset is HARD or 1993.
After the first save, the Opening Ceremony starts. Overrides live in the pit stop's CONFIG page (§11.2). Changing
anything below the starting preset clears the `_CLEAN` bit for good (4MI's HARD ROCK rule, `r4mi/modes.md` §5).

---

## 3. The bracket stage select

### 3.1 From vanilla's grid [new-code] M · Must, [new-art] M · Must

Vanilla facts (`rm6/ram.md`):

- **Grid.** The 3×3 grid is `$3F:$F232` = `00 01 03 FF / 02 FF 05 FF / 04 06 07 FF`. The centre gives stage 8 only
  when `$05C8` = 0, that is, once all eight are beaten.
- **Beaten stages.** A beaten portrait becomes Rockman's head, and a plate stage shows its B/E/A/T letter.
- **Rematches.** A beaten boss's room beams Rockman out: there are no rematches.
- **Text.** Script `$12` draws `PUSH START` and the names.

GP keeps the shape (three rows of three frames and a centre) and the vanilla cursor feel, but redraws the screen as a
**bracket** and replaces the cell table with a node table.

**Layout and pairing.** Four portraits stay in their vanilla cells (Blizzard, Wind, Tomahawk, Yamato). Four move so
that each Exhibition pair (the PLAN §3.3 pairs) meets at one of the four inner crossings around the centre:

The screen as a 5×5 grid. The frames sit on the even rows and columns, the badges on the four inner crossings:

| | col 0 | (gap) | col 1 | (gap) | col 2 |
|---|---|---|---|---|---|
| **row 0** | BLIZZARD (0) | | WIND (1) | | KNIGHT (6) |
| (gap) | | **E3** ◆ wired to Blizzard + Flame | | **E1** ◆ wired to Wind + Knight | |
| **row 1** | FLAME (3) | | **FINAL** (centre) | | TOMAHAWK (5) |
| (gap) | | **E4** ◆ wired to Yamato + Centaur | | **E2** ◆ wired to Tomahawk + Plant | |
| **row 2** | YAMATO (4) | | CENTAUR (7) | | PLANT (2) |

Each badge touches four cells: its two venues, the FINAL, and one other frame. Its two bracket lines run from the
inner edges of its venues' frames into the badge, and one line runs from the badge into the FINAL's corner. Numbers
in brackets are the vanilla stage ids.

| Badge | Crossing | Wired to | Unlocked by both secret exits of |
|---|---|---|---|
| **E1** | top right | Wind (top middle), Knight (top right) | Wind + Knight |
| **E2** | bottom right | Tomahawk (middle right), Plant (bottom right) | Tomahawk + Plant |
| **E3** | top left | Blizzard (top left), Flame (middle left) | Blizzard + Flame |
| **E4** | bottom left | Yamato (bottom left), Centaur (bottom middle) | Yamato + Centaur |

Each pair is a corner plus the edge next to it, a pinwheel. Each badge is wired into the centre, the FINAL. The art
is bracket lines in the BG (gold when lit, grey when not), 32×32 portraits, and 16×16 badges drawn as sprites so
they can blink.

**Node table** (data, replacing `$F232`): 13 nodes × 6 bytes.

| Byte | Contents |
|---|---|
| +0 | meta index |
| +1 | x |
| +2 | y |
| +3 | neighbour UP/DOWN (two nibbles) |
| +4 | neighbour LEFT/RIGHT (two nibbles) |
| +5 | layer (0 = ring, 1 = badge) |

There are 9 ring nodes and 4 badge nodes. Navigation skips nodes that cannot be selected.

### 3.2 Controls on the bracket [new-code] S · Must

| Button | Does |
|---|---|
| D-pad | Moves within the current layer |
| START / A | Selects. A venue → the **match card** (`MATCH: ROCKMAN vs BLIZZARD MAN / VENUE: SUMMIT CLIMBER`, `venues_b.md` §0.6; it is vanilla's typed boss-intro panel, `$3C:$81B1`, extended to new entrants) → the stage. A cleared stage first shows a confirm card: best score, medal, best time, the 4 secret icons, and `REMATCH? NO/YES` |
| **SELECT** | **PIT STOP**: Eddie's shop, chips, the garage, CONFIG (difficulty group), `SAVE & QUIT` (back to the title). This matches `systems.md` §1.5. SELECT is free outside stages (`rm6/ram.md` "SELECT is free") |
| **B** | Toggles the **Exhibition layer**: the cursor jumps to the 2×2 grid of badges, and B again returns to the ring. The prompt `B: EXHIBITIONS` shows only once a badge is lit |

**Rematches are allowed** in GP: medals need replays. The vanilla beam-out on a beaten boss's room must be removed
(`systems.md` / `tech.md`, §15). A replay pays only the score improvement (BRIEF §5.3).

### 3.3 Node states and what they draw [new-code] S · Must

| State | Ring frame draws | Selectable |
|---|---|---|
| OPEN | The champion's portrait, name | yes |
| WON | The portrait with a **medal ribbon** sprite (bronze/silver/gold/platinum colour); a gold line to its badge; a ★ on the line if its secret exit is found; the plate letter B/E/A/T in the frame corner if the plate is held | yes (rematch) |
| POSTPONED | The portrait under a red **POSTPONED** stamp (sprite overlay) | no: Kalinka *"Rain delay! …It's not raining. It's Bass."* |
| Badge DARK | A plain rivet | no |
| Badge HALF | One of its two lines lit, the badge dim and showing "?" | no; START shows the pair's names: *"One more secret exit: KNIGHT MAN's venue!"* |
| Badge LIT | Blinking badge with the guest's icon | yes |
| Badge WON | Solid badge plus the medal ribbon | yes |

### 3.4 Centre node: the FINAL frame [new-code] S · Must

| Condition (checked in order) | Centre shows | START does |
|---|---|---|
| fewer than 4 venue wins | The GP trophy silhouette with `?` | Kalinka: *"The final? Win some matches first!"* |
| 4+ wins and the Semifinal not cleared | **BASS β** portrait, cracked frame, `SEMIFINAL` | → the Semifinal Riot (meta 9) |
| Semifinal cleared, fewer than 8 wins | Trophy, `4 TO GO` → `1 TO GO` | Kalinka counts down |
| 8 wins, H1 not cleared | **Lit trophy** | First time: the trophy theft scene (`story.md`), then the HALL OF FAME map |
| inside H1-W3 | The fortress logo of the current map | → that map (H or W) |
| CLEARED file | The trophy with Rockman's face | → the **replay list** of meta 0, 9 and 14-21 (any cleared stage) |

The fortress maps (`fortress.md`) get one extra item, **BACK TO BRACKET** [new-code] S · Should. A player inside the
Hall of Fame can still go back for Exhibitions or medal replays. Vanilla never allowed this, but GP saves per wing,
so nothing is lost.

### 3.5 The Semifinal trigger [new-code] S · Must, [new-art] S · Should

The rule: **venue wins = popcount(STAGE_CLEAR bits 1-8)**.

- When it reaches **4** and STAGE_CLEAR bit 9 (the Semifinal) is clear, the bracket is **SEMI_PENDING**.
- While SEMI_PENDING, every unbeaten venue frame is POSTPONED.
- Won venues stay selectable for medal replays, and the pit stop stays open. The player cannot strand themselves,
  because the Semifinal is selectable at once.
- The Semifinal clear sets bit 9. The POSTPONED stamps peel off (event b3), and the last 4 venues reopen.

The "Riot" intro (event b2, plays once, about 6 s, Should; the stamps alone are Must) is a screenshot moment:

1. The bracket draws normally. Then the music cuts and the screen shakes (scroll jitter, 8 frames).
2. Bass β's sprite drops in at the top centre, lands on the FINAL frame and fires three buster shots at it (the frame
   tiles swap to a cracked version).
3. He dashes across the four unbeaten portraits. Each one gets a POSTPONED stamp as he passes.
4. Commentary (`story.md` writes it): Kalinka *"An unregistered entrant is attacking the bracket!"* Cossack
   *"…Registered, actually. Sponsor: Mr. Y."* Kalinka *"Of course it is."*
5. The centre shows BASS β; the cursor moves to it.

The adaptors arrive by win count (BRIEF §4):

- **POWER after the 2nd win, JET after the 4th**, stored in FORMS.
- They are handed over as bracket events b0 and b1: Roll's pit-crew pop-up on the bracket. The event text belongs to
  `story.md`; the bits and the order belong here.
- On the 4th win, the order is **JET event → Riot intro**.

### 3.6 Bracket event queue [new-code] S · Must

Story beats on the bracket are **data**: a table of `{condition, event script id, seen bit}`. The bracket runs the
first unseen event whose condition holds, sets its seen bit, saves (autosave 7), and repeats until none are left.

Conditions are predicates over STAGE_CLEAR, FORMS, FLAGS and STORY_BEAT, the same predicate engine as §4. This keeps
the bracket code free of story special cases (CX lesson 7: special cases in visible tables).

| Seen bit | Condition | Event |
|---|---|---|
| EVENTS b0 | venue wins ≥ 2 | Roll: "POWER adaptor ready" + `FORMS.POWER` |
| EVENTS b1 | venue wins ≥ 4 | Roll: "JET adaptor ready" + `FORMS.JET` |
| EVENTS b2 | wins ≥ 4 and the Semifinal not cleared | Riot intro (§3.5) |
| EVENTS b3 | Semifinal cleared | Stamps peel off; Kalinka: "the bracket resumes" |
| EVENTS b5 | the `story.md` join condition | Break Man joins: `FORMS.TAG` |
| EVENTS2 b0-3 | badge n becomes LIT | The badge lights: Cossack announces the exhibition guest |
| EVENTS2 b5 | RATEFLAGS.DOPED set | BREAK MAN WALKS: he stands at the bracket's edge, says one line, and leaves for good (§6.3) |
| EVENTS b7 | CLEARED | The post-game bracket intro: "Welcome back, champion" |

---

## 4. The judges' debrief

### 4.1 How it plays [new-code] M · Must

Every stage clear ends at the **judges' desk**:

1. The scorecard slides in (`systems.md`: TIME / DAMAGE / VARIETY / SECRETS / STYLE, a medal, bolts).
2. **One debrief hint** types into a box under it: 4 lines × 28 characters, pre-wrapped by the text build tool. The
   speaker is **Kalinka** at the commentary desk (she "hears things"; `story.md` may swap the speaker).

The line is chosen 4MI's way (`r4mi/modes.md` §1.5: entry = first failed test), but **per stage**:

```
blocked = none
for each predicate p of this stage, in table order:
    if p passes: continue
    if p.require is not met:
        if blocked == none: blocked = p                         (remember it, keep looking)
        continue
    tier = (SECRETS[m].MISS >= 2) ? B : A                       (escalation)
    show HINT[p.hint + tier]; goto done
if blocked: show REQ_HINT[blocked.require]; goto done           (CX lesson 6: telegraph the tool)
show a "perfect venue" line (rotating, 4 lines)
done: if any predicate failed, SECRETS[m].MISS += 1 (saturating at 7)
```

A predicate that needs a tool the player lacks never hides a hint the player can use now. The "come back with JET"
line appears only when everything left is tool-gated.

So the first clears get a riddle (tier A), and from the third clear on the judges get blunt (tier B). Players who
like to puzzle keep the puzzle; players who are stuck get unstuck. Nothing ships as WIP text (4MI's EN debrief shipped
"WIP WIP WIP", `r4mi/text.md` §4).

### 4.2 Predicate record format [new-code] S · Must

One record per meta stage (22 records × 20 B = 440 B, in a data bank):

| Byte | Contents |
|---|---|
| +0 | n = number of predicates (0-6) |
| +1.. | n × 3 bytes: `test`, `require`, `hint` |
| pad | to 20 bytes |

**`test`** (high nibble = type, low nibble = argument):

| Type | Test passes when | Argument |
|---|---|---|
| `$0n` | SECRETS[m] bit n set | n = 0 exit, 1 room, 2 item, 3 plate |
| `$1n` | best medal ≥ n | 1 bronze … 4 platinum |
| `$2n` | the last scorecard's row n is at its maximum | 0 TIME … 4 STYLE |
| `$3n` | RATEFLAGS bit n set (inverted for CHAMP_KO) | |
| `$4n` | stage counter n ≥ its table target | for stage-owner extras |
| `$FF` | — | end of list |

**`require`:**

| Value | Requirement |
|---|---|
| 0 | none |
| 1 | POWER |
| 2 | JET |
| 3 | SUPER |
| 4 | TAG |
| `$10+w` | weapon w owned |
| `$20+v` | venue v won |

**`hint`**: the index of tier A in the hint table; tier B is the next entry.

### 4.3 The venue predicate table [new-code + text] S · Must

**One rule for every stage: predicates run in descending `systems.md` SECRETS weight** (exit 3, room 2, item 2,
plate 1; §6.2), then **Gold**, then **Platinum**. So each hint points at the biggest gain still on the table. Room
comes before item on the tie, as both venue docs do.

The two venue docs proposed different orders: `venues_a.md` room → item → exit, `venues_b.md` exit → room → chip.
This doc owns the debrief and picks the weight rule for consistency. The table is data, so a venue owner can still
argue a reorder in its own row.

**Where plates sit:**

- In **Knight** (A) and **Tomahawk** (B) the plate sits in the secret boss room (`venues_a.md` §0.2), so it is set
  together with the exit and needs no predicate of its own.
- In **Yamato** (E) and **Centaur** (T) the plate is a separate JET-gated predicate (`venues_b.md` §0.3).
- Wind, Plant, Blizzard and Flame have no plate.

**The text.** Tier B is **the venue owner's own hint, word for word** (`venues_a.md` §1.5-§4.8, `venues_b.md`
§1.12, §2.12; this doc writes tier B for Yamato and Centaur until venues_b adds theirs). Tier A is a riddle this doc
adds: **tier A rewards knowing the homage game; tier B is an instruction.**

| Meta | Venue | Predicates, in order (test / require / hint id) |
|---|---|---|
| 1 | Blizzard: SUMMIT CLIMBER | `$00`/–/BL0 · `$01`/–/BL1 · `$02`/–/BL2 · `$13`/–/G · `$14`/–/G |
| 2 | Wind: SKY ACE 1943 | `$00`/–/WI0 · `$01`/–/WI1 · `$02`/–/WI2 · `$13` · `$14` |
| 3 | Plant: JUNGLE PITFALL | `$00`/–/PL0 · `$01`/–/PL1 · `$02`/–/PL2 · `$13` · `$14` |
| 4 | Flame: PRINCE OF PERSIA PALACE | `$00`/–/FL0 · `$01`/–/FL1 · `$02`/–/FL2 · `$13` · `$14` |
| 5 | Yamato: EDO NINJA ROW | `$00`/–/YA0 · `$01`/–/YA1 · `$02`/–/YA2 · `$03`/JET/YA3 · `$13` · `$14` |
| 6 | Tomahawk: GUN.SMOKE FRONTIER | `$00`/–/TO0 (plate B with it) · `$01`/–/TO1 · `$02`/–/TO2 · `$13` · `$14` |
| 7 | Knight: DRAGON QUESTLIKE | `$00`/–/KN0 (plate A with it) · `$01`/–/KN1 · `$02`/–/KN2 · `$13` · `$14` |
| 8 | Centaur: ATLANTIS RUINS | `$00`/–/CE0 · `$01`/–/CE1 · `$02`/–/CE2 · `$03`/JET/CE3 · `$13` · `$14` |
| 0, 9-21 | Opening, Semifinal, Exhibitions, fortress | whatever SECRETS bits the stage's owner defines (same weight rule), then `$13`, `$14`. The Mr. X card (§6.1, T14) is one of them, in the Hall of Fame |

**No venue secret exit, room or item needs an adaptor**:

- `venues_a.md` §0.3 and `venues_b.md` §0.3 both say so.
- Only Yamato's E and Centaur's T plates need JET, as in vanilla.
- Knight's stairs can also be opened by vanilla's charged-punch pillar, but they never require it.

The adaptor-gated *extras* (Tomahawk's Energy Balancer room and sky bypass, item pockets) are not predicates.

`G` is the generic scorecard hint, chosen by the **weakest row** of this run's scorecard (§4.5).

### 4.4 Hint text list (EN; JP in the text pass)

An entry is at most 4 lines of 28 characters, wrapped by the text tool. " / " marks a forced break in tier A. Ids end
in 0 for the exit, 1 for the room, 2 for the item and 3 for the plate.

**Blizzard: SUMMIT CLIMBER** (*Ice Climber*; secrets `venues_b.md` §1.5, tier B §1.12)

| Id | Secret | Tier A (riddle, this doc) | Tier B (the venue owner's hint) |
|---|---|---|---|
| BL0 | exit: catch the condor | THE CONDOR NEVER WAITS FOR / SLOW CLIMBERS. RACE THE / BONUS CLOCK TO THE TOP. | The summit condor only carries climbers who reach it with time on the clock. Jump for its feet. |
| BL1 | room: the no-wrap floor | THE SEALS KNOW EVERY FLOOR / OF THAT MOUNTAIN. ONE OF / THEM NEVER COMES BACK. | On the mountain, one floor doesn't wrap around. Watch where the seals walk. |
| BL2 | item: SNOW CHAINS | THE SEALS ARE UNION / WORKERS. THE UNION REMEMBERS / WHO WAS NICE TO THEM. | The seals are only doing their job. A climber who never breaks one earns a set of chains. |

**Wind: SKY ACE 1943** (*1942/1943*; `venues_a.md` §1.5-§1.6)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| WI0 | exit: the ace's elevator | IN 1943 THE RED PLANES / CAME IN FIVES. AN ACE / LEAVES NONE OF THEM FLYING. | FOUR RED SQUADRONS, FOUR LAMPS. THE ELEVATOR ONLY TAKES ACES. |
| WI1 | room: WEATHER BALLOON | SEAGULLS NEVER STAND ON / NOTHING. ASK ONE WHERE / IT'S STANDING. | A SEAGULL WAS STANDING ON A CLOUD. CLOUDS AREN'T FLOORS... ARE THEY? |
| WI2 | item: YASHICHI | CAPCOM'S OLDEST SECRET IS / A PINWHEEL. IT HIDES IN / SOMETHING YOU SHOOT. | SHOOT THE POW. THEN KEEP SHOOTING IT. |

**Plant: JUNGLE PITFALL** (*Pitfall!*, *Pitfall II*; `venues_a.md` §4.4-§4.8)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| PL0 | exit: follow the cat | IN PITFALL II, HARRY HAD / TO FIND HIS CAT. THIS / ONE IS TRYING TO FIND YOU. | THE CAT KNEW A WAY DOWN. NEXT TIME, FOLLOW IT. |
| PL1 | room: TREETOP HUT | THE STORM SHOWS MORE THAN / RAIN. WATCH THE TREES / WHEN THE SKY LIGHTS UP. | WHEN THE LIGHTNING STRUCK, A LADDER APPEARED IN THE TREES. |
| PL2 | item: PITFALL PERFECT | HARRY'S PERFECT SCORE / NEVER LET A LOG TOUCH / HIM. NOT ONE. | FOUR TREASURES, ZERO LOGS. THE DIAMOND IS SHY. |

**Flame: PRINCE OF PERSIA PALACE** (*Prince of Persia*; `venues_b.md` §2.5, tier B §2.12)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| FL0 | exit: don't fight your shadow | THE PRINCE NEVER BEAT HIS / SHADOW. HE DID SOMETHING / SMARTER WITH IT. | Your shadow only fights if you fight. Hold your fire and walk into it. |
| FL1 | room: the mouse | IN 1989 A MOUSE SAVED THE / PRINCE. MICE STILL LIVE IN / THAT PALACE. | Something small lives behind a gate in the fire vault. Stand still and listen. |
| FL2 | item: FIREPROOF | THE FIRE MARSHAL HATES / BONFIRES. HE COUNTS EVERY / POOL YOU LIGHT. | The palace fire marshal rewards entrants who leave the oil unlit. Shoot the fire-droppers first. |

**Yamato: EDO NINJA ROW** (*Jajamaru*, *Goemon*, *DuckTales*; secrets `venues_b.md` §0.3; tier B by this doc until
venues_b writes its own)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| YA0 | exit: the sekisho back road | NO TRAVELLER PASSES THE / SEKISHO WITHOUT PAPERS. / GOEMON KNEW THAT. | Collect all 3 travel passes and show them at the checkpoint gate. The back road opens. |
| YA1 | room: the gold crest | SCROOGE KNEW IT: SOME / FLOORS ONLY OPEN IF YOU / BOUNCE ON THEM. | Pogo on the gold crest in the caltrop hall. A trapdoor opens. |
| YA2 | item: DARUMA | DARUMA OTOSHI: KNOCK OUT / THE BLOCKS, NOT THE HEAD. / KEEP HIS FACE ON. | Win the daruma otoshi without ever hitting its head. |
| YA3 | plate E (JET) | BEAT'S E-PART IS ON THE / CASTLE ROOF, WHERE ONLY / FLYING NINJAS GO. | Fly up to the castle roof with Rush Jet. Plate E is up there. |

**Tomahawk: GUN.SMOKE FRONTIER** (*Gun.Smoke*, *Wild Gunman*; `venues_a.md` §3.7)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| TO0 | exit: the back way (+ plate B) | THREE FACES ON THE WANTED / POSTERS. THE SHERIFF / KNOWS WHO COLLECTS. | THE SHERIFF ONLY OPENS THE BACK WAY FOR A DEPUTY WITH THREE BOUNTIES. |
| TO1 | room: THE OUTHOUSE | "OCCUPIED," SAYS THE SIGN. / IT HAS SAID SO ALL DAY. / KNOCK LOUDER. | SOMETHING IN TOWN WAS RATTLING. IN GUN.SMOKE YOU SHOOT WHAT LOOKS ODD. |
| TO2 | item: SHERIFF STAR | PLEASE DO NOT SHOOT THE / PIANIST. OR ANYONE ELSE / WHO ISN'T WANTED. | THE SHERIFF SAW YOU SHOOT AT TOWNSFOLK. READ THE SIGN BY THE PIANO. |

**Knight: DRAGON QUESTLIKE** (*Dragon Quest*; `venues_a.md` §2.5-§2.7)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| KN0 | exit: the stairs behind the empty throne (+ plate A) | IN 1986 THE REAL LORD / HID UNDER HIS OWN EMPTY / THRONE. OLD HABITS... | THE KNIGHTLORD'S THRONE IS EMPTY. WHY? SEARCH WHERE NO ONE SITS. |
| KN1 | room: LIGHT'S TABLET | ERDRICK LEFT A TABLET FOR / HIS HEIR. SOMEONE ELSE / LEFT ONE HERE. | SOMETHING GLITTERED ON THE FLOOR OF THE HALL. THOU DIDST NOT SEARCH. |
| KN2 | item: KAISHIN | A METAL ONE IS WORTH 1000 / EXP. IT KNOWS THAT. IT / WON'T WAIT AROUND. | METAL ONES FLEE FAST. HIT THEM OFTEN, NOT HARD. |

**Centaur: ATLANTIS RUINS** (*Atlantis no Nazo*, *Kid Icarus*; secrets `venues_b.md` §0.3; tier B by this doc until
venues_b writes its own)

| Id | Secret | Tier A | Tier B |
|---|---|---|---|
| CE0 | exit: ZONE 100 | ATLANTIS HAD 100 ZONES. / THE LAST ONE IS UNDER WATER / MOST OF THE TIME. | A sunken door in the ruins opens only at low tide. Wait for the water to drop, then go in. |
| CE1 | room: ZONE 0 | ZONE 0 IS ON NO MAP. IT / ONLY SHOWS UP WHEN THE / LIGHTS GO OUT. | In the black zone, one door glows only in the dark. Don't light the room: look for it. |
| CE2 | item: CENTURION | THREE STONE SOLDIERS STILL / GUARD THE RUINS. THEY'D / LIKE TO STOP GUARDING. | Free all three petrified Centurion-bots with a charged shot. |
| CE3 | plate T (JET) | PEGASUS CROSSED THAT GAP / WITH WINGS. YOU HAVE A DOG / WITH A JETPACK. | Fly across the Pegasus gap with Rush Jet. Plate T is on the far side. |

Text rules for the pass: the debrief font is upper case, so tier B strings are set in capitals at build time. Each
venue owner may rewrite its tier B line, and this doc's tier A line then gets checked against it. JP lines are
written for both tiers in the text pass (`story.md`).

### 4.5 Generic lines

**Requirement hints** (the tool is missing; CX lesson 6):

| Id | Text |
|---|---|
| R1 POWER | THIS ONE NEEDS MORE PUNCH / THAN YOU HAVE. COME BACK / AFTER YOUR 2ND WIN! |
| R2 JET | SOME ROUTES HERE ARE FOR / ENTRANTS WHO FLY. COME / BACK AFTER YOUR 4TH WIN. |
| R3 SUPER | THE HALL OF FAME HIDES A / NEW ADAPTOR. SOMETHING / HERE IS WAITING FOR IT. |
| R4 TAG | TWO CAN GO WHERE ONE / CAN'T. YOU'LL HAVE A TAG / PARTNER SOON. A MASKED ONE. |
| R5 weapon w | THE JUDGES THINK ANOTHER / CHAMPION'S WEAPON OPENS / THIS. %WEAPON%, MAYBE? |

**Scorecard hints (G)**, chosen by the weakest row as a fraction of its maximum. They must match `systems.md`'s rules;
these are the v0 lines:

| Row | Text |
|---|---|
| TIME | TOO SLOW FOR THE JUDGES! / PAR HERE IS %PAR%. YOU / TOOK %TIME%. |
| DAMAGE | THE JUDGES COUNT EVERY / HIT YOU TAKE. FEWER HITS, / BIGGER CHEQUE. |
| VARIETY | THE JUDGES LOVE VARIETY! / KILLS WITH LOTS OF WEAPONS / AND FORMS PAY THE MOST. |
| SECRETS | THIS VENUE STILL HIDES / THINGS. FIND ONE AND I'LL / TELL YOU THE NEXT. |
| STYLE | FINISH THE CHAMPION WITH / HIS WEAKNESS, AND KEEP / THE E-TANK IN YOUR POCKET. |

**Perfect-venue lines** (rotate by the frame counter):

1. PERFECT VENUE! PAPA IS / CRYING. HE SAYS IT'S THE / STADIUM LIGHTS.
2. NOTHING LEFT TO FIND! THE / JUDGES ARE OUT OF HINTS / AND OUT OF CARDS.
3. EVEN MR. Y'S JUDGE HELD / UP A 10! THEN HE TOOK IT / BACK. BUT WE ALL SAW IT.
4. THIS VENUE IS 100% DONE. / YOU CAN STOP NOW. …NO? / OKAY. I'LL WATCH AGAIN.

---

## 5. Medals and Hall of Fame points

### 5.1 Medals [engine: systems.md] · Must

The scorecard is out of 100 (`systems.md`, BRIEF §5.3). The medal comes from the **best** score ever on that meta
stage (STAGEREC +0):

| Medal | Best score | HoF points |
|---|---|---|
| — | 0-39 | 0 |
| BRONZE | 40-59 | 1 |
| SILVER | 60-79 | 2 |
| GOLD | 80-94 | 3 |
| PLATINUM | 95-100 | 4 |

The medal is never stored, only derived from the best score, so the thresholds can be retuned without breaking
saves.

### 5.2 Hall of Fame points [new-code] S · Must

**HOF PTS = the sum of the medal points over meta 0-21.** The maximum is 22 × 4 = **88**. The file card and the
bracket's top bar show it.

HoF points are the currency of the global unlocks (§7). At every file commit, the system block's unlocks are
re-checked against that file's HoF points (unlocks never re-lock). Medal ribbons on the bracket frames show where the
points are.

---

## 6. The championship rating (the Hero Score analogue)

### 6.1 Rows and tests [new-code] M · Must

After the victory-lap credits, the **CHAMPIONSHIP RATING** screen fills seven rows, one by one, like 4MI's RESULT
(`r4mi/modes.md` §1). Every point comes from one test in a single jump table, and **the same table, in the same
order, picks Break Man's debrief** (the first failed test).

| Test | Row | Points | Passes when |
|---|---|---|---|
| — | **CHAMPIONSHIP** | 40 | Constant: you won |
| T0 | TEAM | 5 | **Beat rebuilt**: all 4 plates (B-E-A-T) |
| T1 | TEAM | 5 | **Break Man is your partner**: TAG_STAGES has ≥ 3 bits (you called him in 3 different stages), **and** he has not refused you (RATEFLAGS.DOPED clear, §6.3) |
| T2 | ROUTE | 1 each, 8 max | Secret exits found (SECRETS b0, meta 1-8). The test passes at 8/8 |
| T3 | ROUTE | 1 each, 4 max | Exhibitions cleared (STAGE_CLEAR 10-13) |
| T4 | ROUTE | 2 | All 8 venue hidden rooms |
| T5 | ROUTE | 2 | All 8 venue behaviour chips |
| T6 | GEAR | 1 per chip, 10 max | Chips owned from **Eddie**: bought at the shop or built in the garage from PARTs (`systems.md` §9: 7 bought + 4 crafted = 11, so one may be missed). The test passes at 10 |
| T7 | GEAR | +2 | **TURBO** owned: the doping chip from Mr. Y's booth. **The trap** (§6.3) |
| T8 | MEDALS | 5 | GOLD or better on all 8 venues |
| T9 | MEDALS | 4 | At least 3 PLATINUMs (any stages) |
| T10 | FAIR PLAY | 4 | GAMEOVERS = 0 |
| T11 | FAIR PLAY | 4 | CHAMP_TIME < 648,000 frames (3:00:00) |
| T12 | FAIR PLAY | 2 | UNPLUGS = 0 (§1.7) |
| T13 | BONUS | 2 | **RIVAL**: the Semifinal won with no damage taken in Bass β's fight (RATEFLAGS b2) |
| T14 | BONUS | 2 | **MR. X'S CARD**: a business card hidden somewhere in the Hall of Fame (RATEFLAGS b1; `fortress.md` places one pickup) |
| T15 | BONUS | 1 | **TOP SEED**: never KO'd in a champion's boss room (CHAMP_KO clear) |
| T16 | — | — | Sentinel: always fails → the "perfect" debrief |

T7 is a *bonus-shaped* test: it never picks the debrief, because the debrief skips T7 (a hint that says "go and dope"
would be wrong). In the jump table it returns "passed" for the debrief's purposes and adds its 2 points only to the
rows.

**The arithmetic hides a trade-off**, as 4MI's does (`r4mi/modes.md` §1.2). The row maxima are 40 + 10 + 16 + 12 + 9
+ 10 + 5 = **102**, but the readme says 100. The 2-point TURBO chip can only be had by doping, and doping costs Break
Man's partnership, worth 5 TEAM points:

- **With TURBO**, the most you can score is 97.
- **Without it**, exactly 100.

The readme can print the honest sum `40 + 10 + 16 + 10 + 9 + 10 + 5 = 100`, and the off-by-two is a clue players can
solve, as 4MI's was.

**Rank titles** under the number (EN; JP in the text pass):

| Rating | Title |
|---|---|
| 100 | GRAND CHAMPION |
| 90-99 | CHAMPION |
| 80-89 | FINALIST |
| 70-79 | SEMIFINALIST |
| 55-69 | QUARTERFINALIST |
| < 55 | PARTICIPANT, with a participation-ribbon sprite |

**Asterisks.** A doped file prints its number with `*` and the title gets `(TURBO)`, which honours `systems.md`'s
"your records carry an asterisk". An EDITED file reads `RESULT UNDER REVIEW *` and grants no achievement (§10).

**When it is computed.** The rating is computed at every championship win: a cleared file can replay W3 and see the
ending again. BEST_RATING keeps the maximum. T11 always uses CHAMP_TIME, the time of the *first* win.

### 6.2 Break Man's debrief [new-code + text] S · Must

After the rating, Break Man (4MI's Proto Man pattern; BRIEF §2) speaks: one greeting, then the entry for the **first
failed test**, then `TO BE CONTINUED`. That is vanilla's last line, kept on purpose. On the first clear only, a second
line follows: `(SPECIAL EVENTS ARE NOW OPEN)`.

EN v0 (`story.md` may restyle the voice, but must keep one hint per test):

| Entry | Text |
|---|---|
| greeting | …SO YOU WON. NOT BAD, / ROCK. FOR A BUSTER WITH / LEGS. |
| T0 Beat | THAT BIRD OF YOURS IS / STILL IN FOUR PIECES. B, / E, A, T. SPELL IT OUT. |
| T1 tag (never called) | YOU NEVER CALLED ME. I / WASN'T WAITING. BUT THE / PAUSE MENU HAS A BUTTON. |
| T1 tag (doped) | YOU TOOK MR. Y'S CHIP. I / DON'T TAG WITH CHEATS. / THE JUDGES NOTICED TOO. |
| T2 exits | THE JUDGES COUNTED %N% / SECRET EXITS. THERE ARE 8. / ONE PER VENUE. |
| T3 exhibitions | FOUR BADGES ON THAT / BRACKET. TWO SECRET EXITS / LIGHT EACH ONE. |
| T4 rooms | EVERY VENUE HIDES ONE / ROOM, ONE SCREEN BIG. THE / JUDGES DROP HINTS. LISTEN. |
| T5 chips | SOME PRIZES AREN'T WON BY / WINNING. THEY'RE WON BY / ACTING STRANGE. |
| T6 gear | EDDIE STILL HAS CHIPS ON / HIS SHELF, AND PARTS IN / HIS GARAGE. GO SHOPPING. |
| T8 gold | GOLD IN EVERY VENUE IS / WHAT CHAMPIONS GET. YOU / GOT SOME. GET THE REST. |
| T9 platinum | 95 IS A PERFECT RUN. THE / JUDGES WANT THREE. PICK / YOUR BEST VENUES. |
| T10 game over | %N% GAME OVERS. A CHAMP / DOESN'T PAY THE ENTRY / FEE TWICE. |
| T11 time | %H%:%MM% ON THE CLOCK. A / CHAMPION'S FIRST TITLE / TAKES UNDER 3 HOURS. |
| T12 unplug | THE STADIUM LOST POWER %N% / TIMES DURING YOUR MATCHES. / FUNNY. IT NEVER DOES. |
| T13 rival | BASS TELLS EVERYONE HE / HIT YOU IN THE SEMIS. / MAKE HIM A LIAR. |
| T14 card | SOMEONE DROPPED A CARD IN / THE HALL OF FAME. IT SAYS / "MR. X". A REAL ONE? |
| T15 top seed | YOU WENT DOWN IN A CHAMP'S / RING. TOP SEEDS DON'T. / NOT EVEN ONCE. |
| perfect | NOTHING TO ADD. YOU ARE / THE REAL CHAMPION. NOW GO / HOME BEFORE WILY DOES. |
| perfect (ENGRISH) | I HAVE NO ADVICE. / YOU ARE REAL CHAMPION! (a 4MI tribute, `r4mi/text.md` §4 entry 15) |

### 6.3 The trade-off: doping (owned by `systems.md` SYS-CHP-4) [new-code] S · Should

`systems.md` §0 decision 7 defines the moral trade-off, and this doc only scores it:

- **The offer.** Mr. Y's booth buys a PART from you and gives you the **TURBO** chip.
- **The cost.** Break Man refuses to partner you for the rest of the file (`FORMS.TAG` is cleared and the pause-menu
  CALL greys out), and your records carry an asterisk.

What it does to the meta layer:

- It sets RATEFLAGS.DOPED (b0).
- It plays bracket event EVENTS2 b5, **BREAK MAN WALKS**: on the next bracket visit Break Man's sprite stands at the
  bracket's edge, says one line (`story.md`), and leaves. Like 4MI's Eddie, the cost is shown, not explained.
- In the rating, TURBO adds +2 (T7) and costs T1's 5.
- In RECORDS and on the file card, a `*` follows the rating and the TOTALS page reads `TURBO: YES`.
- In GP Rush, a MY GP run with TURBO in its chip set marks its record with `*`.

The judges never mention it. Break Man does (T1, doped variant).

If the tag partner (a Should) does not ship, the cost moves to FAIR PLAY: T12 becomes "no unplugs and no TURBO", and
the trap's arithmetic must be re-checked in that build.

### 6.4 Data [new-code] S · Must

- **Test table:** 17 entries × 4 bytes `{routine lo, routine hi, points, row}`.
- **Row sums:** stored in LAST_ROWS, the total in LAST_RATING.
- **Debrief index:** first failed test + 1, as 4MI does at `$4D:$9BDB`.

---

## 7. The unlock chain

All unlocks are **global** (system block `$010`, one bit each). Any file can earn them, and they never re-lock. The
SPECIAL EVENTS menu reveals its items word by word as the bits arrive (4MI `$4C:$811A`). Locked items show as `??? ???`
with a one-line condition (4MI lesson: be exact, and show it).

| Step | You do | You get (bit) | Tier |
|---|---|---|---|
| 1 | Reach **20 HoF points** on any file (possible mid-game) | SPECIAL EVENTS on the title, with MUSEUM (sound test, the plaques you have read) and RECORDS (U0.0, U0.1, U0.2) | Should |
| 2 | Reach **40 HoF points** | EXHIBITION RULES (U0.3) | Could |
| 3 | **Win the championship** | TIME ATTACK (U0.4), GP RUSH: OPEN BRACKET (U0.5), the ENTRANT option (Bass Mode, U0.6) | Should / Could |
| 4 | Clear the **OPEN BRACKET** | GP RUSH: the 9 ONE-WEAPON CUPS and ALL-STAR (U0.7); KNOCKOUT (U1.3) | Should / Could |
| 5 | Clear **any one cup** | MY GP (U1.0), **EXTRA CONFIG** (U1.1), TRUE GP (U1.2) | Should / Must (EXTRA CONFIG) |
| 6 | Clear **TRUE GP** | The `???` fight's name is revealed (U1.4); MUSEUM VAULT (U1.6); achievement | Should |
| 7 | All 22 stages GOLD or better, and the Mr. X card on the same file | **MR. X RETURNS** (U1.5) | Could |
| 8 | Beat every **DEV** time in Time Attack | MUSEUM DEV ROOM: the developers' commentary plaques (U1.7) | Could |

EXTRA CONFIG is Must as a **dev tool** (BRIEF §7.3). In development builds (`DEV=1`) every unlock bit reads as set,
and EXTRA CONFIG is also on the title (SELECT+START) and in the pause menu. In release builds it unlocks at step 5,
as in 4MI.

**System block unlock bits** (`$010-$017`):

| Byte.bit | Unlock | Byte.bit | Unlock |
|---|---|---|---|
| U0.0 | SPECIAL EVENTS menu | U1.0 | MY GP |
| U0.1 | MUSEUM | U1.1 | EXTRA CONFIG |
| U0.2 | RECORDS | U1.2 | TRUE GP |
| U0.3 | EXHIBITION RULES | U1.3 | KNOCKOUT format |
| U0.4 | TIME ATTACK | U1.4 | `???` name revealed |
| U0.5 | GP RUSH: OPEN | U1.5 | MR. X RETURNS |
| U0.6 | ENTRANT: BASS β | U1.6 | MUSEUM VAULT (the 1993 debug sound player) |
| U0.7 | GP RUSH: CUPS + ALL-STAR | U1.7 | MUSEUM DEV ROOM |
| U2-U7 | reserved | | |

---

## 8. SYSTEM block layout (1 KB) [new-code] S · Must

| Offset | Size | Field | Notes |
|---|---|---|---|
| `$000` | 4 | magic `'R' '6' 'S' 'Y'` | |
| `$004` | 1 | layout version | 1 |
| `$005` | 1 | SYSFLAGS | b0 INITIALISED; b1 a DEV build has written this block (release builds show `DEV SAVE` on the title) |
| `$006` | 2 | generation | |
| `$008` | 1 | LANGUAGE | 0 JAPANESE, 1 ENGLISH, 2 ENGRISH |
| `$009` | 1 | DISPLAY | b0-1 ANNOUNCER (0 ON, 1 DEATHS ONLY, 2 OFF); b2 FLASHES REDUCED; b3 HUD TIMER; b4-5 TEXT SPEED (0 SLOW … 3 INSTANT); b6 SCREEN SHAKE OFF; b7 reserved |
| `$00A` | 1 | AUDIO | b0 MMC5 CHANNELS OFF; b1 MMC5 ARRANGEMENTS (Could); b2-7 reserved |
| `$00B` | 1 | CONTROLS | b0-1 SELECT SWAP (0 FULL, 1 WEAPONS ONLY, 2 OFF); b2 2P SHIFT OFF; b3 A/B SWAP; b4-7 reserved |
| `$00C` | 4 | reserved config | |
| `$010` | 8 | UNLOCKS | §7 |
| `$018` | 2 | ACHIEVEMENTS | §10 |
| `$01A` | 2 | ACH_NEW | Shows NEW! until RECORDS has shown it |
| `$01C` | 4 | reserved | |
| `$020` | 3 | CLEARED_ANY | 24 bits by meta index: cleared on any file (feeds the Time Attack and Rules menus) |
| `$023` | 3 | ENTERED_ANY | Entered on any file (otherwise the menus show `???`) |
| `$026` | 1 | BEST_RATING_EVER | Unedited files only |
| `$027` | 1 | reserved | |
| `$028` | 120 | LIFE_STAGE[24] × 5 | Lifetime KOs (16-bit) + time (24-bit, 256-frame units) |
| `$0A0` | 32 | LIFE_TOTALS | play (32-bit, 256-frame units), KOs (24), game overs (16), unplugs (16), boots (16), championships (16), bolts earned (32), weakness hits (24), tag calls (16), reserved |
| `$0C0` | 264 | TA_REC[24] × 11 | Best time (24-bit frames) + 4 checkpoint splits of that run (16-bit frames from the start) |
| `$1C8` | 72 | TA_BASS[24] × 3 | Bass Mode best times (Could) |
| `$210` | 96 | RUSH_REC[16] × 6 | Per course: best time (24-bit frames), tries (16-bit), clears (8-bit) |
| `$270` | 18 | KO_REC[3] × 6 | KNOCKOUT 8 / 16 / 32 |
| `$282` | 72 | MYGP[3] × 24 | Saved MY GP setups (§9.2.5) |
| `$2CA` | 48 | RULES_BOOK[24] × 2 | Exhibition Rules sticker book: bit r = cleared with rule r on |
| `$2FA` | 16 | HEARD | 128 bits: tracks heard (sound test list) |
| `$30A` | 8 | PLAQUES | 64 bits: Museum plaques read |
| `$312` | 6 | WEAK_SEEN | 48 bits by fight id: weakness landed at least once |
| `$318` | 6 | FIGHT_SEEN | 48 bits by fight id: reached (lobby names show `???` otherwise) |
| `$31E` | 16 | VENUE_REC[8] × 2 | One lifetime mini-record per venue, defined by its venue doc: Wind's SHOOTING DOWN % (higher is better), Tomahawk's quick-draw reaction time in frames (lower is better), …; a ROM table gives each venue's label and direction |
| `$32E` | 194 | reserved | |
| `$3F0` | 16 | trailer | §1.3 |

---

## 9. Post-game: SPECIAL EVENTS

The menu is a list (vanilla font) with the achievement plates in a strip at the bottom (§10).

| Item | Section |
|---|---|
| TIME ATTACK | §9.1 |
| GP RUSH | §9.2 |
| EXHIBITION RULES | §9.3 |
| RECORDS | §9.4 |
| MUSEUM | §9.5 |
| EXTRA CONFIG | §9.6 |
| MR. X RETURNS | §9.8 |

**One ruleset choke point** [new-code] S · Must (4MI lesson: modes override config through one set of globals,
`r4mi/modes.md` §5). At every stage start a 16-byte **RULESET** in work RAM is filled from exactly one source:

| Mode | Source |
|---|---|
| main game | the file's DIFF |
| Time Attack | the TA preset |
| GP Rush | the course setup |
| any mode | ORed with the Exhibition Rules mask and the EXTRA CONFIG cheats |

The engine reads only RULESET:

- damage multiplier, drops, criticals, HARD;
- lives policy, E-tank floor, safety net;
- allowed weapons, forms and tag;
- chips on/off;
- checkpoints on/off, max HP, refill at pause;
- i-frame cap;
- rules bits, cheat bits;
- HUD timer.

`systems.md` and `tech.md` read the same block (§15).

### 9.1 TIME ATTACK [new-code] M · Should

- **List:** every meta stage 0-21 cleared on any file, plus the victory lap (meta 23). Each row shows `RECORD
  m:ss.cc` and `DEV m:ss.cc`; a ★ means the record beats the DEV time.
- **Regulation loadout** (fixed, so records compare; 4MI's TA fixes its loadout too, `r4mi/modes.md` §2):
  - the buster and all 8 weapons, full;
  - forms: none in the Opening (meta 0), POWER + JET everywhere else, and SUPER from H4 (meta 17) on, since H3
    awards it. A venue's TA therefore allows its adaptor-gated routes (plates, sky routes), and every record is set
    with the same tools;
  - no chips, no tag partner, 0 E-tanks, one life, max HP 28;
  - NORMAL rules, criticals off, drops off. That is 4MI's STABLE, its "no luck" setting.
- **Story state:** STORY_BEAT and FORMS are preset per stage from a 24-entry table, as 4MI presets PROG per fortress
  stage.
- **Timer:**
  - It runs from the first frame of control after READY to the frame the boss's bar empties; for the victory lap, to
    the last name.
  - It is shown when CONFIG HUD TIMER is on: 7 sprite digits under the HP bar.
  - At each checkpoint, a split pops up for 60 frames: `+0:01.23` (red) or `-0:00.40` (green) against the record
    run's split.
- **Pause menu:** RETRY (restart the stage at once) and QUIT. A death goes straight back to the list.
- **Result:** `TIME 1:23.45` under `RECORD`, and `NEW RECORD!!` (which 4MI's TA lacks). The system block commits.
- **DEV times:** a 24-entry ROM table, filled from the developers' golden-movie runs (§9.6).

### 9.2 GP RUSH: a boss rush on one fight table [new-code] M · Should

The design copies two proven things:

- **Vanilla Wily 3's data-driven rush** (`rm6/fortress.md` §7):
  - a hub screen;
  - one room per boss at `$09 + id`;
  - tables `$39:$8EC8` (X), `$8ED2` (boss stage id) and `$8EDC` (alcove metatiles);
  - palette `$9A + id`;
  - a big life capsule that returns you to the hub;
  - alcoves closed through the `$0340` bitfield;
  - a ninth teleporter after the eighth win.
- **4MI's arena family** (`r4mi/modes.md` §3):
  - one 45-entry fight table with block markers;
  - a 6-byte fight bitmask and seven presets of about 19 bytes;
  - a list builder (`$4C:$9762`) that keeps table order, plus four shufflers;
  - a runner whose step counter makes even steps lobbies and odd steps fights;
  - one lobby with a NEXT / LEFT panel, gift bits and an exit;
  - 24-bit frame-count records.

#### 9.2.1 The fight table [new-code] S · Should

Fight ids are fixed by type. A separate **run order** list sets the play order and the shuffle blocks (bit 7 marks a
block start, as at 4MI `$4C:$97A3`).

| Ids | Fights | Block |
|---|---|---|
| `$00-$07` | the 8 champions (venue id order) | CHAMPIONS |
| `$08-$17` | up to 16 mid-bosses and set-piece fights (AYACO, the Daruma, …), assigned by the venue and fortress owners | MID |
| `$18-$1B` | Exhibition guests E1-E4 | GUESTS |
| `$1C-$20` | Hall of Fame MK-VI bosses H1-H5 | LEGACY |
| `$21` | Bass β (Semifinal) | CASTLE |
| `$22` | the W1 boss | CASTLE |
| `$23` | Bass β (Castle duel) | CASTLE |
| `$24` | the W3 machine | CASTLE |
| `$25` | the Wily Capsule | CASTLE |
| `$26` | the Opening Ceremony boss | MID |
| `$27` | **`???`**: the Castle's final form, renamed (below) | SECRET |
| `$28` | Mr. X (Could, §9.8) | SECRET |
| `$29-$2F` | spare | |

Run order: `[$26 $08-$17] [$00-$07] [$18-$1B] [$1C-$20] [$21-$25] [$27 $28]`.

**Fight record, 10 bytes:**

| Byte | Contents |
|---|---|
| +0 | engine stage id |
| +1 | room screen (written to `$0684`) |
| +2 / +3 | spawn x / y |
| +4 | room CHR set (to `$0685`) |
| +5 | palette (to `$0686`) |
| +6 | music |
| +7 | portrait id |
| +8 | name text id |
| +9 | flags: b0 needs JET; b1 needs POWER; b2 BG boss; b3 multi-part; b4 SECRET name; b5-7 block |

**Loading a fight uses vanilla's own warp:** write `$51`, `$0684-$0686`, then `$F0 = 2` (`rm6/SUMMARY.md` §3). The
fight therefore loads in **the boss's own arena**, with its real stage data, as 4MI's arenas do. The legacy fights
need no hub-room art.

**The `???` gag (a running gag on Mr. Y).** Until U1.4, the lobby panel names fight `$27` **`MR. Y'S ???`**. After
the TRUE GP clear it reads **`DR. WILY (OBVIOUSLY)`**. This is 4MI's `???` → COCKROACH OMEGA trick (`r4mi/modes.md`
§3.6), at the cost of one byte test. If Mr. X Returns ships, `$28` follows it, named `???` → `MR. X (THE REAL ONE)`.

#### 9.2.2 The lobby: "PLAYERS' TUNNEL" [new-code] S · Should, [new-art] S · Should

One screen, built from the Opening Ceremony's stadium tileset: GP's home stadium, as 4MI's lobby is its own home city
(`r4mi/modes.md` §3.1). It needs a tunnel interior, a scoreboard and a gate of light at the right.

**The scoreboard** (text window) reads `NEXT  LEFT:16`, then the portrait and the name.

**Gifts**, one per GIFTS bit:

| Bit | Gift |
|---|---|
| b0 | **Eddie**: touch him for a random item (1UP / E-tank / big life / big weapon energy) |
| b1 | **Roll's** HP refill, left |
| b2 | **Roll's** HP refill, right |
| b3 | **Beat**: refills every weapon |
| b4 | **Break Man**: recharges the tag call |

**Exit:** stand in the gate and press UP. The camera flashes and `ROUND n` is announced.

START in the lobby opens the normal pause menu, for weapon and chip choices.

#### 9.2.3 The runner [new-code] S · Should

```
step = 0; list = build(mask, run_order, shuffle)       ; 4MI $4C:$9762, shufflers at $97DB
loop: if step even: if GIFTS == 0 → heal HEAL HP, step++  else → LOBBY until gate
      if step odd : fight list[step/2] via the warp; on boss death → step++
      on player death: lives-- ; lives < 0 → ELIMINATED screen
      step/2 == count → CHAMPION screen
```

- **ELIMINATED** screen: `ELIMINATED IN ROUND 5 / BY PLANT MAN`, in tournament language, with the time and the round
  record.
- **CHAMPION** screen: the time, `NEW RECORD!!`, and the unlocks (§7).

#### 9.2.4 Courses (presets) [data] S · Should

Each course is a 24-byte setup in ROM, in the same format as MY GP (§9.2.5). Course n saves to RUSH_REC[n].

| # | Course | Fights | Weapons | Gifts | Tanks | Other |
|---|---|---|---|---|---|---|
| 0 | **OPEN BRACKET** | the 8 champions, shuffled | all + forms | all | 4 E | one life |
| 1-9 | **ONE-WEAPON CUPS**: BUSTER CUP, then Y.SPEAR … C.FLASH CUP | the 8 champions | that weapon only (+ forms; only the BUSTER CUP has the buster, as 4MI's SUPPIN) | none; HEAL 5 | 9 E | refill at pause; i-frame cap 30 (4MI's SHORT INV) |
| 10 | **ALL-STAR** | every non-secret fight, shuffle 3 (within blocks) | all + forms | all | 4 E | one life |
| 11 | **TRUE GP**: "THE GREATEST GRAND PRIX IN HISTORY" | **all**, secrets included, shuffle 3, finale fixed | all | all | 9 E | HARD, one life |
| 12 | **MY GP** | user | user | user | user | user |
| 13 | **1993 CUP** (Could) | the 8 champions in vanilla Wily 3 hub order | vanilla weapons, no forms | none | 0 | 1993 rules: the nostalgia course |
| 14-15 | reserved | | | | | |

Every course runs with criticals OFF and drops NONE (`systems.md` §14, §15.2: records modes have no dice).

Weapon cups never need to drop fights, unlike 4MI's three "(15 STAGES)" courses. Under BRIEF §5.1 every weapon does
1-4 to every boss.

#### 9.2.5 MY GP: the bracket editor [new-code] S · Should

A bit-grid editor over a 24-byte setup, 4MI's MY ARENA (`r4mi/modes.md` §3.5):

| Byte | Field | Format |
|---|---|---|
| +0..+5 | FIGHTS | 48-bit mask by fight id (they always run in run order, shuffled by SHUFFLE) |
| +6 | WEAPONS A | b0-7 = the 8 champion weapons |
| +7 | WEAPONS B | b0 BUSTER; b1 POWER; b2 JET; b3 SUPER; b4 TAG; b5 BEAT; b6-7 extra weapons |
| +8 | GIFTS | lobby bits (§9.2.2); 0 = no lobby |
| +9 | SHUFFLE | 0 fixed, 1 all, 2 all but the finale block, 3 within blocks |
| +10 | TANKS | low nibble E-tanks 0-9, high nibble W-tanks |
| +11 | HEAL | HP restored between fights when there is no lobby (0-28) |
| +12 | LIVES | 0-9 (0 = one life) |
| +13 | DIFF | b0 HARD; b1 reserved (criticals are always OFF in GP Rush, `systems.md` §14); b2-3 DAMAGE; b4 SHORT I-FRAMES (cap 30); b5 REFILL AT PAUSE; b6 CHIPS ON; b7 reserved |
| +14..+15 | RULES | Exhibition Rules mask (§9.3) |
| +16..+19 | CHIPS | the chip set used when CHIPS ON (owned-chip bit order) |
| +20 | ORIGIN | the preset it was loaded from |
| +21..+23 | reserved | |

- **Commands:** EDIT, LOAD PRESET ◀▶, SAVE / LOAD (3 slots in the system block), START.
- **Field help:** one help line per field, from the same help-string engine as EXTRA CONFIG.
- **A one-fight MY GP is a boss select**, which is also how the test harness builds per-boss states (4MI's scout built
  its 45 `fight_XX` states this way).

#### 9.2.6 KNOCKOUT format [new-code] M · Could, [new-art] S

**What it is.** A real single-elimination bracket of 8, 16 or 32 entrants. Rockman is one entrant; the others are
drawn from the champions, guests, mid-bosses and legacy bosses.

**How a round plays:**

- Only **Rockman's** matches are played: 3, 4 or 5 fights.
- The other matches are **simulated** from a POWER byte per fight id (1-15): `winner = higher (POWER + rand 0-7)`.
- Commentary pops up between rounds: *"UPSET! PLANT MAN knocks out BASS β!"* (lower POWER won) or *"WIND MAN
  wins on a technical decision."*
- The bracket screen fills in after each round, which reuses the bracket renderer with a classic tree layout.

**What it costs:** a 48-byte POWER table, the simulator, the tree nametable, and records per size. The premise
reaches even the post-game (CX lesson 1).

### 9.3 EXHIBITION RULES (modifiers) [new-code] S-M · Could

- **Choose:** any meta stage cleared on any file, then toggle rules on a 4×4 grid, then START.
- **Scoring:** the scorecard shows, but there are no bolts and no medals (rules runs are unranked).
- **Sticker book:** a clear sets one sticker per active rule in RULES_BOOK[m].
- **In GP Rush:** the same mask works inside MY GP.

| Bit | Rule | Effect, and the hook | Size |
|---|---|---|---|
| 0 | **BUSTER ONLY** | The weapon menu locks to R.BUSTER; forms allowed | S |
| 1 | **NO FORMS** | The POWER and JET menu entries are disabled; the form swap does nothing | S |
| 2 | **ONE HIT** | Max HP 1 (4MI's "Owata-shiki" nod) | S |
| 3 | **FAMICOM RULES** | No checkpoints: the checkpoint write `$0684` is suppressed except at the stage start | S |
| 4 | **ICE AGE** | Every solid floor reads as slippery ice: the floor-type latch `$A7` forced to type 5 on solid ground (vanilla momentum `$A1.$A0`) | S |
| 5 | **MOON BOOTS** | Low gravity: the water gravity `$00.18` without water (no bubbles, normal speed) | S |
| 6 | **SUDDEN DEATH** | All damage ×2, both ways | S |
| 7 | **NO CHIPS** | Equipped chips ignored | S |
| 8 | **PACIFIST** | Killing any normal enemy is a KO (`systems.md`'s kill attribution) | S |
| 9 | **ROULETTE** | The equipped weapon changes at random every 600 frames, announced with a slot-machine jingle (a nod to 4MI Pharaoh's curse of that name) | S |
| 10 | **NO HUD** | HP and weapon bars hidden | S |
| 11 | **TURBO** | Enemy AI runs twice every 4th frame. **Lag risk**: playtest per venue first | M |
| 12-15 | reserved | | |

### 9.4 RECORDS [new-code] M · Must (pages 1-3), Should (the rest)

Seven pages, with NEXT / PREV:

1. **FILE RESULTS** (pick a file): per meta stage, the medal, best score, best time, KOs and clears. The KO column is
   headed `KNOCKOUTS` in EN, `ティウン` in JP, and **`TIWNS`** in ENGRISH (4MI's heading, `r4mi/modes.md` §7).
2. **FILE TOTALS:** play time, KOs, game overs, unplugs, bolts earned and spent, tag calls, weakness hits, E-tanks used,
   HoF points, and the best rating with its seven rows.
3. **LIFETIME** (system block): per-stage KOs and time, the totals, and the 8 **venue mini-records** (`VENUE_REC`).
4. **TIME ATTACK:** records, DEV times, ★, and the total of all records.
5. **GP RUSH:** per course, the best time, tries and clears; KNOCKOUT sizes.
6. **RULES:** the 22 × 12 sticker grid.
7. **ACHIEVEMENTS:** every plate with its **exact condition** and its state.

Times are frame counts, formatted `h:mm:ss` or `m:ss.cc` (60 frames = 1 s, 4MI's convention).

### 9.5 MUSEUM and sound test [new-code] M · Could, [new-art] S

| Room | Contents |
|---|---|
| **BROADCAST BOOTH** (sound test) | The track list by name (JP/EN). Only HEARD tracks are listed; the rest show `??????`. Live meters for the 5 channels plus the 2 MMC5 pulses (note name, volume and duty per channel, as 4MI's AUDIO PLAYER does), and Rockman and Roll dancing on the right. SELECT holds a note (4MI's `SEL=HOLD`) |
| **PLAQUE GALLERY** | Every plaque read: the 5 Hall of Fame wing plaques, the 8 venue homage plaques and the 4 Exhibition plaques. Thanks plaques for Rockman CX, Rockman 4 Minus ∞, and the 8 fan designers (vanilla's DWNB-41..48 credit cards, `rm6/SUMMARY.md` §1.7) |
| **ENTRANT FILES** | The vanilla boss-intro data panel (HEIGHT / WEIGHT / ATTACK / DEFENCE / MOBILE / ENERGY / LOCATION / SPECIALTY, typed by `$3C:$81B1`) for **every fight in FIGHT_SEEN**. The new entrants need panel data (`story.md`), and Centaur Man keeps "ABILITY UNKNOWN" |
| **VAULT: 1993** (U1.6) | Launches vanilla's **hidden debug SOUND PLAYER** from bank `$28` (`SEQ COL TBL TMR SOUND PLAYER`). Capcom left it in the ROM unreachable; GP gives it a door. Plaque: *"Found in bank $28 of the 1993 cartridge. Nobody could reach it. Until now."* It needs a launcher that sets up its thread and CHR sets `$FC-$FF`, plus a START+SELECT exit hook. S, Could |
| **DEV ROOM** (U1.7) | The developers' commentary plaques: one per venue, on how it was built |

### 9.6 EXTRA CONFIG: RAM editor, level select, dev tool [new-code] M · Must

4MI's EXTRA CONFIGURATION (`r4mi/cheats.md` §5) is a page of binary fields, each pointing straight at live RAM, with
one help line per field. GP does the same, in hex and bit grids.

**How it works:**

- **Data-driven:** a field table `{RAM address lo/hi, format, help id}`.
- **Formats:** hex byte, bit grid with labels, decimal 0-999.
- **On open:** pick a source: FILE 1-3 or DEFAULTS. It loads into the **scratch file** (magic `'S'`, never committed),
  and every edit changes the scratch LIVE image.

**Fields:**

| Group | Fields (help line in brackets) |
|---|---|
| WHERE | STAGE (meta 0-23 → stage id) · CP (checkpoint 0-7, from the stage's checkpoint table) · SCREEN (raw `$0684` override, `FF` = use CP) |
| PROGRESS | CLEAR (24-bit STAGE_CLEAR) · STORY · EVENTS · EVENTS2 · FORMS `TAG SUP JET POW` |
| SECRETS | 24 × 4-bit grid `PLT ITM RM EX`, one row per meta stage |
| LOADOUT | WPN `CEN KNI TOM YAM FLA PLA WIN BLI` · WPN2 · E-TANK · W-TANK · LIVES · BOLTS · CHIPS (32-bit) · EQUIP (6 slots) |
| RULES | DIFF preset · DIFF A · DIFF B · RULES mask (§9.3) |
| CHEATS | LIVES LOCK · REFILL AT PAUSE · GOD (HP pinned, pits and spikes respawn you in place) · BOSS HP 1 · RNG LOCK (seed 16-bit) |
| DEBUG | LAG BAR (PPUMASK grey bit on while the main thread runs, so lag is visible as a bar) · OBJ COUNT (live objects in the corner) · FRAME STEP (SELECT+START freezes; SELECT steps one frame) · HITBOXES (Could) |

**Actions:**

| Action | Does |
|---|---|
| ENTER STAGE | Load STAGE/CP with the edited state, through the vanilla warp (`$51`, `$0684-$0686`, `$F0 = 2`; 4MI lesson 10's one-byte respawn) |
| TO BRACKET | Open the bracket with the edited bits |
| FIGHT n | A one-fight GP Rush on a fight id |
| WRITE FILE n | Commit the scratch image into file n, which sets **EDITED** for good |
| RESET COUNTERS | |

**Disqualifier.** Anything played from EXTRA CONFIG runs on the scratch file, which never saves and never earns
achievements or records. WRITE FILE marks the target EDITED. An EDITED file still plays, and its rating shows with
`*` (`RESULT UNDER REVIEW`), but it grants no achievements. This is 4MI's `$7697 = 3` rule (`r4mi/modes.md` §6),
except that GP **marks the file** instead of silently voiding it.

**The dev-tool half** (BRIEF §7.3; the regression entry point) [new-code] S · Must:

- **TEST MAILBOX** (PRG-RAM page 0 `$7A00-$7A1F`). At boot, before the title, the reset code checks it.

  | Bytes | Contents |
  |---|---|
  | +0..+7 | magic `"R6GPTEST"` |
  | +8 | command: 1 enter stage, 2 fight, 3 bracket, 4 title with a file loaded, 5 run the TA timer |
  | +9 | meta stage |
  | +10 | CP |
  | +11 | file source (0 defaults, 1-3 a file) |
  | +12..+13 | RULES |
  | +14 | cheats |
  | +15..+16 | RNG seed |
  | +17 | fight id |
  | +18..+30 | loadout overrides (WEAPONS, FORMS, CHIPS, E-tanks) |
  | +31 | checksum (sum of +0..+30) |

  If it is valid, the boot code consumes it: it clears the magic first, then goes straight there.
- **Why a mailbox:** golden movies, damage sweeps and per-stage states (the CX lesson 9 harness) become one Python line
  that pokes WRAM before the first frame. This is 4MI's injected-save trick (`r4mi/cheats.md` §10), made explicit.
- **It is kept in release builds**, so the tests run on the shipped ROM. The magic plus the checksum make a false
  trigger from garbage RAM a 1-in-2^72 event.
- **Also from day one** (BRIEF §7.3): the pause-menu `DEBUG` item and SELECT+START on the title, in `DEV=1` builds.

### 9.7 BASS MODE [new-code] L · Could, [new-art] L

This section covers only the meta-side hooks. The moveset is PLAN §2.8's; the art is `art_audio.md`'s.

- **NEW GAME:** `ENTRANT: ROCKMAN / BASS β` on the file select (after U0.6). FILEFLAGS.BASS is set on the file.
- **File card:** a Bass icon. Records go to TA_BASS.
- **Story:** `story.md` swaps lines at the key beats, gated on the BASS flag. The Riot intro becomes **Rockman**
  crashing *Bass's* bracket, the same script with the actors swapped.
- **Rating:** TEAM is re-labelled **SOLO**:
  - T0 counts "Treble's parts" if `systems.md` re-homes the plates, else it passes automatically;
  - T1 passes automatically (*"Bass works alone. He says."*);
  - there is nobody to refuse him, so TURBO costs Bass nothing: Mr. Y is his own sponsor. On a BASS file T7's +2
    is not counted, which keeps the maximum at 100, and the trap shrinks to the asterisk alone (Break Man's T1
    line becomes *"Even Wily's own robot gets an asterisk."*). The rating is also clamped to 100 in every case.
- **Levels:** every adaptor gate needs a Bass solution (PLAN §2.8). The venue owners mark which.

### 9.8 MR. X RETURNS [new-code] M · Could

- **Unlock:** U1.5 (all 22 Gold+ and the Mr. X card).
- **Premise (PLAN §4):** the *original* Mr. X turns out to be a real, separate person after all, and he is furious
  that Wily borrowed his name twice.
- **Cheap build: the 1993 fortress, untouched.**
  - **Map:** vanilla **Mr. X Fortress 1** (22 screens). Its layout data stays in ROM when `tech.md` relocates the
    tables, and its tileset `$2C:$92` is vanilla. It plays with the **vanilla music `$09`** and the vanilla boss
    (Rounder II).
  - **Ending:** a one-screen exchange (`story.md`), then a new final fight against Mr. X's flying chair (fight `$28`;
    `fortress.md` or `story.md` designs the pattern).
  - **The stage itself:** the museum of the 1993 game, played as it was.
- **Rewards:** achievement **THE X-FILES**, and the TRUE GP finale `$28`.

---

## 10. Achievements [new-code] S · Should

There are 16 plates in a strip under the SPECIAL EVENTS menu (4MI shows 3). Each bit is set at the moment the
condition is met, and **never on an EDITED file or the scratch file**. Every condition is printed in RECORDS (§9.4):
4MI's HARD ROCK silently required six sub-settings, and GP will not repeat that.

| Bit | Plate | Exact condition |
|---|---|---|
| 0 | **GRAND CHAMPION** | Championship rating 100 |
| 1 | **IRON ENTRANT** | Win the championship with HARD_CLEAN (the HARD preset, all its sub-settings unchanged since NEW GAME) and GAMEOVERS = 0 |
| 2 | **1993** | Win with R1993_CLEAN |
| 3 | **FULL BRACKET** | All 4 Exhibitions cleared |
| 4 | **ALL GOLD** | GOLD or better on all 22 stages |
| 5 | **PLATINUM ROW** | PLATINUM on all 8 venues |
| 6 | **TOURNAMENT HISTORIAN** | Every SECRETS bit the 22 stages define, and every plaque read |
| 7 | **THE GREATEST GP IN HISTORY** | Clear TRUE GP |
| 8 | **CUP COLLECTOR** | Clear all 9 one-weapon cups |
| 9 | **SPEED KING** | CHAMP_TIME < 324,000 frames (1:30:00) |
| 10 | **ONE HIT WONDER** | Clear all 8 venues with the ONE HIT rule (RULES_BOOK bit 2) |
| 11 | **WEAK SPOT** | WEAK_SEEN covers every non-secret fight id |
| 12 | **DEV TIME** | ★ on every Time Attack stage |
| 13 | **INCORRUPTIBLE** | Win a file on which Mr. Y's booth offered TURBO and you never took it (RATEFLAGS.DOPED clear). Hidden as `???` until earned, so the trap stays a surprise |
| 14 | **BASS CLEAR** | Win on a BASS file (Could) |
| 15 | **THE X-FILES** | Beat MR. X RETURNS (Could). Hidden until earned |

---

## 11. CONFIG

`systems.md` §13 owns what each setting does and where it is read. This section owns the menus, the storage, and the
split between **global** settings (system block) and **per-file** settings (the file's DIFF bytes).

**Why per file** (an amendment to `systems.md` §13.1, which put every setting in the system block): three files are
often three players. Each file's achievements (IRON ENTRANT, 1993) and its records' C/N/H/93 badges must reflect the
settings that file was played on. So the difficulty group lives in the file, and everything about the person or the
TV is global.

### 11.1 Global options (title → CONFIG; system block `$008-$00B`) [new-code] S · Must

| Option | Values (default first) | Effect |
|---|---|---|
| LANGUAGE | ENGLISH / JAPANESE / ENGRISH | Text table selection through the one hook at `$3C:$8631` (`rm6/SUMMARY.md` §4, 2.7) and the new text engine. ENGRISH: §12 |
| ANNOUNCER | ON / DEATHS ONLY / OFF | Commentator pop-ups (BRIEF §5.5). DEATHS ONLY keeps the death lines and mutes the rest (an extension of `systems.md`'s ON/OFF). The judges' debrief is unaffected |
| TEXT SPEED | NORMAL / FAST / INSTANT / SLOW | Typewriter frames per character: 2 / 1 / 0 / 4 |
| FLASHES | NORMAL / REDUCED | C.FLASH, the WEAK flash, the Time Stop tint, explosions and the Riot shake use a 2-step palette dim instead of full-white frames; no frame-alternating flicker above 10 Hz |
| SCREEN SHAKE | ON / OFF | |
| HUD TIMER | OFF / ON | In-stage timer sprite (always on in Time Attack) |
| SELECT SWAP | FULL / WEAPONS ONLY / OFF | `systems.md` §1.1: hold SELECT + D-pad cycles weapons (and forms, in FULL); a tap toggles the last weapon. OFF = vanilla feel |
| 2P SHIFT | ON / OFF | Controller 2's A/B cycle weapons (`systems.md` §1.4, 4MI) |
| A/B SWAP | OFF / ON | Jump on B, fire on A (one EOR at the joypad read `$3E:$C711`) |
| MMC5 AUDIO | ON / OFF | The extra pulse channels; OFF for consoles without expansion audio (BRIEF §5.7) |
| MMC5 ARRANGEMENTS | OFF / ON | Could: arranged tracks where `art_audio.md` makes them |
| SOUND TEST | → | A shortcut to the Museum booth once it is unlocked |
| LOAD DEFAULTS | | Everything above except LANGUAGE |

### 11.2 Per-file options (pit stop → CONFIG; DIFF bytes `$009-$00D`) [new-code] S · Must

The preset values are `systems.md` §13.2's:

| Option | Values | CASUAL | NORMAL | HARD | 1993 |
|---|---|---|---|---|---|
| DIFFICULTY | the 4 presets, or EDIT after any hand change | | | | |
| DAMAGE (to Rockman) | ×0.5 / ×1 / ×1.5 / ×2, rounded up | ×0.5 | ×1 | ×1.5 | ×1 |
| LIVES (start and continue) | 1-9 | 5 | 3 | 3 | 3 |
| E-TANK FLOOR | 0-4 | 2 | 0 | 0 | 0 |
| DROPS | NONE / LESS / NORMAL / MORE | MORE | NORMAL | LESS | vanilla |
| REFILL on respawn | NONE / HALF / FULL | FULL | HALF | NONE | NONE |
| GUARDS (Spike Guard + Beat on loan, slotless) | OFF / ON | ON | OFF | OFF | OFF |
| HARD (poke lists + AI branches) | OFF / ON | OFF | OFF | ON | OFF |
| CRITICALS (if they ship) | OFF / ON | OFF | ON | ON | OFF |
| RULES | GP / 1993 | GP | GP | GP | 1993 |

**1993 is a NEW GAME choice only** (`systems.md` §13.3 lists what it switches off: alt fires, synergies, the parry,
chips, the shop, bolts, the Beat rescue, criticals, the refill). Switching a file into or out of 1993 would strand
owned chips and bolts, so the RULES row is greyed out after NEW GAME.

**Lowering a setting.** If the file becomes easier than its starting preset on any row (DAMAGE lower, LIVES higher,
DROPS more, REFILL more, GUARDS on, HARD off, criticals don't count), HARD_CLEAN clears for good and LOWEST updates.
The pit stop warns first: *"The judges will note this."* The records keep each medal's preset badge
(`systems.md` §13.2: accessibility is never punished in the score, only labelled).

## 12. ENGRISH [new-code + text] S · Could

**What it is.** A joke tribute to 4MI, whose language option offers JAPANESE / ENGRISH with "ENGLISH COMING SOON"
(`r4mi/modes.md` §5). GP has real English, so ENGRISH is a third choice that swaps deliberately broken strings into a
handful of **menus**. Dialogue and hints stay ENGLISH, so nothing becomes unreadable.

**How it works:**

- `LANGUAGE = 2` reads a sparse override table (sorted string ids → pointers); missing ids fall back to ENGLISH.
- **Digits:** ENGRISH prints numbers with the letter **O for zero** (`1OO`, `TIME 1:O3.45`). This is 4MI's zero-less
  font, mirrored: vanilla RM6's pause font has no O and writes `N0R`, `P0W`, `W.ST0RM` with zeros
  (`rm6/text.md` §5.3).
- **C.FLRSH:** the ENGRISH weapon name is vanilla's own data misspelling (`rm6/SUMMARY.md` §1.2).

| Where | ENGLISH | ENGRISH |
|---|---|---|
| Title | GAME START | GAME STARTING |
| Title | CONFIG | CONFIGULATION |
| Title | SPECIAL EVENTS | SPECIAL EVENT IS HAPPEN |
| Language row | ENGRISH | ENGRISH (ENGLISH IS COME!!) |
| File select | NEW ENTRANT | NEW CHALLENGER IS HERE |
| File select | ERASE | ERASE IT!! |
| File select | BROKEN DATA | DATA IS BROKEN. SORRY |
| Difficulty | CASUAL / HARD | CASUALLY / VERY HARD |
| Bracket | PUSH START | PUSH START BUTTON |
| Bracket | SEMIFINAL | SEMI-FAINAL |
| Bracket | POSTPONED | POSTPONE |
| Bracket | EXHIBITIONS | EXHIBITON MATCH |
| Weapon get | YOU GET | YOU GOT A |
| Weapon names | C.FLASH | C.FLRSH |
| Scorecard | MEDAL / PLATINUM / BOLTS | METAL / PLATINAM / BORTS |
| Shop | WELCOME! | ALL YOUR BOLTS ARE BELONG TO EDDIE |
| Pause | CALL / RETIRE | CALL HIM / GIVE UP |
| Game over | GAME OVER / CONTINUE | GAME IS OVER / CONTINUE? YOU CAN |
| Records | KNOCKOUTS / TOTAL | TIWNS / TOTALLY |
| Rating | GRAND CHAMPION / PARTICIPANT | GRAND CHAMPIOM / THANK YOU FOR PARTICIPATE |
| Break Man (perfect) | NOTHING TO ADD… | I HAVE NO ADVICE. / YOU ARE REAL CHAMPION! |
| Translation credit | TRANSLATION: (name) | TRANSLATION: (RESERVED) (4MI's credit) |

Rule for the text pass: ENGRISH is affectionate, never mocking, and never in story text, hints or help pages.

---

## 13. Build list (tags, sizes, tiers)

| Item | Tags | Size | Tier |
|---|---|---|---|
| Save module: A/B copies, trailer, commit, load, migration, BROKEN paths | [new-code] | M | Must |
| LIVE FILE / LIVE SYS gather and scatter, play-time fold | [new-code] | S | Must |
| Autosave points 1-9 | [new-code] | S | Must |
| Unplug detector | [new-code] | S | Should |
| Title (new logo) + menu | [new-code][new-art] | M | Must |
| Attract crawl | [new-code][new-art] | S | Should |
| Hidden PASS WORD gag | [engine-ok][new-code] | S | Could |
| File select (cards, NEW/ERASE guards) | [new-code][new-art] | M | Must |
| File COPY | [new-code] | S | Should |
| Difficulty pick | [new-code] | S | Must |
| Bracket screen, node table, node states, centre logic, pit-stop access | [new-code][new-art] | M | Must |
| Exhibition layer (B) + badges | [new-code][new-art] | S | Should |
| Semifinal trigger + POSTPONED | [new-code] | S | Must |
| Riot intro animation | [new-code][new-art] | S | Should |
| Bracket event queue | [new-code] | S | Must |
| Fortress map BACK TO BRACKET | [new-code] | S | Should |
| Judges' debrief engine + predicate tables + hint text (EN/JP) | [new-code] | M | Must |
| Medal derivation + HoF points | [new-code] | S | Must |
| Championship rating + Break Man debrief | [new-code][new-art] | M | Must |
| Doping hooks: DOPED flag, BREAK MAN WALKS event, asterisks | [new-code] | S | Should (with `systems.md` SYS-CHP-4) |
| Unlock bits + SPECIAL EVENTS menu with word reveals | [new-code] | S | Should |
| RULESET choke point | [new-code] | S | Must |
| Time Attack (+ splits, DEV times) | [new-code] | M | Should |
| GP Rush engine: fight table, runner, lobby, courses | [new-code][new-art] | M | Should |
| MY GP editor | [new-code] | S | Should |
| KNOCKOUT | [new-code][new-art] | M | Could |
| Exhibition Rules (bits 0-10) | [new-code] | S | Could |
| TURBO rule | [new-code] | M | Could |
| RECORDS pages 1-3 | [new-code] | S | Must |
| RECORDS pages 4-7 | [new-code] | S | Should |
| Museum booth, plaques, entrant files | [new-code][new-art] | M | Could |
| VAULT: 1993 debug sound player | [engine-ok][new-code] | S | Could |
| EXTRA CONFIG editor + actions + scratch file | [new-code] | M | Must |
| TEST MAILBOX + DEV build switches | [new-code] | S | Must |
| Achievements | [new-code][new-art] | S | Should |
| CONFIG global + per file | [new-code] | S | Must |
| ENGRISH table | [new-code] | S | Could |
| Bass Mode meta hooks | [new-code] | S (meta only) | Could |
| Mr. X Returns | [new-code] | M | Could |
| GP fanfare for the title / rating screens | [new-music] | S | Should |

---

## 14. Lessons applied

- **CX 1, one premise everywhere:** the file select is a registration desk, the stage select a bracket, every clear a
  judging, the boss rush a tournament with simulated upsets, the rating a championship.
- **CX 3, voice on failure:** unplug lines, the ELIMINATED screen, BREAK MAN WALKS.
- **CX 6, telegraph the tool:** requirement hints override riddles when the needed form is missing.
- **CX 7, special cases in visible tables:** bracket events, debrief predicates and rating tests are all data tables.
- **CX 9, a test harness:** crafted saves with checksums become the TEST MAILBOX.
- **CX saves:** three slots. The silent "bad sum = new game" failure is *not* kept; GP shows BROKEN DATA.
- **4MI 5, one predicate table for score and hints:** used twice, per stage (judges) and per game (rating + Break Man).
- **4MI's 102→100 trade-off:** TURBO (+2) costs Break Man (−5).
- **4MI 9, boss rushes on one fight table with one lobby:** presets, cups, MY GP and the boss select all share it.
- **4MI 10, a level select and RAM editor from day one:** EXTRA CONFIG plus the mailbox.
- **4MI, the double copy and a strong checksum:** kept and improved (ping-pong, commit marker), with graceful BROKEN
  handling everywhere.
- **4MI, START+A to overwrite.**
- **4MI, modes override config through one choke point:** RULESET.
- **4MI, hidden names behind achievements:** `MR. Y'S ???` → `DR. WILY (OBVIOUSLY)`.
- **4MI, exact achievement rules, shown in game.**
- **4MI, frame-count records.**
- **4MI's ENGRISH and TIWNS:** a tribute.
- **RM6 3:** GP state lives in PRG-RAM, not in the 89 free CPU bytes.
- **RM6 7:** adaptors become real save flags.
- **RM6 8, vanilla quirks kept on purpose:**
  - TO BE CONTINUED ends the rating;
  - C.FLRSH appears in ENGRISH;
  - the password grid survives as a gag;
  - the debug sound player gets a museum door;
  - Mr. X Fortress 1 is replayed as it was.
- **RM6 fortress.md:** the Wily 3 rush shows the rush is data, and GP Rush generalises its tables. Fights load through
  the vanilla warp (`$51`, `$0684-$0686`, `$F0 = 2`).

## 15. Cross-doc dependencies

| Doc | Must agree on |
|---|---|
| `systems.md` | The scorecard rows, maxima and medal thresholds 40/60/80/95 (medals derive from the best score). Kill attribution (PACIFIST, VARIETY hints). The chip id order (CHIPS_OWNED bits), a chip-source attribute per chip (shop / garage / venue / TURBO) so rating T6 can count Eddie's chips. **The moral trade-off is `systems.md`'s doping (SYS-CHP-4: TURBO from Mr. Y's booth; Break Man refuses; records get an asterisk)**: this doc scores it (T1, T7) and stores RATEFLAGS.DOPED. The PART inventory, the garage and TURBO's effect are `systems.md`'s. Removing vanilla's no-rematch beam-out. W-tanks and consumables (FILE `$033-$037`). The RULESET fields it reads. Criticals shipping or not |
| `story.md` | STORY_BEAT values. Break Man's join condition (event b5) and his debrief voice. Kalinka as the judges' speaker. The Riot intro lines. Roll's adaptor hand-off lines. The trophy theft. The post-game bracket intro. ENTRANT FILES panel data for new bosses. The Mr. X Returns premise. Bass Mode line swaps. The attract crawl |
| `venues_a.md` / `venues_b.md` | Their secrets are used as written (§4.3-§4.4). Their hints are tier B **verbatim**, and the tier A riddles must be re-checked if they change. **The debrief order is this doc's weight rule** (exit → room → item → plate, then Gold, Platinum), not the per-doc orders they proposed. venues_b to add tier B lines for Yamato and Centaur. Plates: A and B ride on the secret exits (venues_a), E and T are JET predicates (venues_b). Each venue's one **mini-record** (Wind's SHOOTING DOWN %, Tomahawk's quick-draw time, and one per other venue if wanted) goes in SYS `VENUE_REC`. Mid-boss fight ids `$08-$17` with arena screens (CONGA, AYACO, the Daruma, …). Bass solutions for adaptor gates (Could) |
| Exhibition owner (venues or fortress) | **Pairs: E1 Wind + Knight, E2 Tomahawk + Plant, E3 Blizzard + Flame, E4 Yamato + Centaur** (PLAN §3.3). Guest fight ids `$18-$1B` |
| `fortress.md` | The Hall of Fame and Castle maps get BACK TO BRACKET. Saves per wing. **Mr. X's business card**: one pickup somewhere in H1-H5, setting RATEFLAGS.MRX_CARD. The SECRETS bits of non-venue stages. Fight ids `$1C-$25` and their arenas. The `???` finale. Mr. X Returns' chair fight. Whether the W2 refight hub reuses vanilla Wily 3's tables (GP Rush can share the hub art) |
| `tech.md` | PRG-RAM size and the NES 2.0 NVRAM declaration. Page 0 reserved for the save (`$6000-$7A1F`). Work-RAM placement. The meta column in the stage-attribute table. Stage ids for the fight table. Keeping vanilla Mr. X 1's layout and tileset in ROM (Mr. X Returns). The text engine's language hook (ENGRISH override table). The DEV build flag. Mailbox handling in RESET |
| `art_audio.md` | The title logo, bracket nametable, badges, medal ribbons, POSTPONED stamp, Bass β and trophy portraits, the cracked frame, the file cards, the participation ribbon, the lobby tunnel (from the Opening tileset), achievement plates, Museum booth meters, and the GP fanfare |
| Opening Ceremony owner | One extra **lobby screen** (players' tunnel) in the stadium tileset for GP Rush |

## 16. Risks

1. **Hint text drifting from the venues.** The §4.4 tier B lines are the venue docs' own, but the tier A riddles are
   this doc's, and Yamato's and Centaur's tier B lines were written from `venues_b.md`'s gate matrix alone. Mitigation:
   - every hint id is listed per venue;
   - the M10 text pass checks each predicate against its venue doc;
   - a test scenario (mailbox: enter the stage with SECRETS = 0) screenshots each debrief.
2. **PRG-RAM shared with work RAM.** The write gate cannot protect the save then. The ping-pong copies and the commit
   marker are designed for exactly this case, but **power-cycle testing on real hardware** (EverDrive) is needed
   before release.
3. **Save size growth.** The FILE block has 190 reserved bytes and the system block 210. If `systems.md` needs more
   (per-row scorecard bests take 120 B), the FILE block can grow to 1 KB by moving the copies, but only before v1.0:
   after release, only migrations.
4. **Rating balance.**
   - The 3-hour T11 limit and SPEED KING's 1:30 are guesses; tune them against playtest saves (the RECORDS totals
     exist for this).
   - TOP SEED (no champion-room KO) may be harsher than its 1 point suggests; that is fine for a bonus.
5. **Semifinal soft lock.** POSTPONED must never leave a player with nothing selectable. The Semifinal is always
   selectable, and the pit stop stays reachable. A test: a file with 4 wins, 0 lives and 0 bolts must still reach the
   Semifinal.
6. **TURBO and lag.** Doubling enemy AI on a ~10-object budget can push frames over. It stays Could, behind a
   per-venue playtest.
7. **Scope.** The post-game is large. If time runs short, the order to cut: KNOCKOUT → Museum → Exhibition Rules →
   MY GP → GP Rush courses beyond OPEN.

   The kernel to keep:
   - saves;
   - the bracket;
   - the debrief and rating;
   - EXTRA CONFIG and the mailbox;
   - RECORDS 1-3;
   - Time Attack.
8. **The `1993` preset's promise** ("vanilla damage tables, forms that can't fire") needs `systems.md` to keep the
   vanilla tables reachable. If not, 1993 shrinks to "no chips, no shop, no tag, classic lives".

## 17. Open questions

1. Should the Semifinal be **forced at once** after the 4th win (a tighter story) instead of the POSTPONED lock (which
   lets the player shop and replay first)? This doc picks the lock.
2. Should **RETIRE** from an uncleared stage cost a life? This doc says no. RETIRE is free and is not an unplug.
3. Is **Kalinka** the right per-stage debrief speaker, or should the judges be separate characters (PLAN's three judge
   portraits), for example with Mr. Y's sponsor chair always holding up "1"? Art cost against the gag.
4. Does Time Attack's regulation loadout include **Break Man's call** from his join point? This doc says no, to keep
   records pure.
5. Should **unlocks** be per file instead of global (4MI is global)? Global is simpler and kinder.
6. Should KNOCKOUT's simulated results use a **fixed seed per day** (from the play-time counter) so friends can race
   the same bracket?
7. Should **1993** files be allowed to unlock anything? This doc says yes, as normal.
