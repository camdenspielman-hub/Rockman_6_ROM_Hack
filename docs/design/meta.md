# Rockman 6 GP: progression, meta-game and modes (meta.md)

Owner: design-meta. Status: **round 3**, revised against [`RULINGS.md`](RULINGS.md) (round 3: §8, R8.1-R8.8, and the
"meta.md" requests of [`reconcile.md`](reconcile.md)), which is binding and overrides [`BRIEF.md`](BRIEF.md) where they
differ. Facts come from `docs/research/*/` (cited as `rm6/ram.md`, `r4mi/modes.md`,
and so on). Facts re-checked in the ROM or emulator for round 2 are tagged **[code, r2]** or **[seen, r2]**; the scripts
are in `build/revise/meta/` (`flagscan.py`, `rematch.py`, `notes.txt`). The round-1 text is in git (commit
`95288ee`) and, locally, in `build/revise/meta/meta_r1.md`.

**What this doc owns** (the single sources of truth, RULINGS and the consistency critic): **save bytes** (the FILE and
SYSTEM blocks, their trailer, commit and load rules, the test mailbox's format), **the bracket** (and the fortress maps),
**events** (the bracket event queue and every seen bit), **the judges' debrief** (the predicate engine and tables), the
medals and HoF points, the championship rating's rows and tests, the unlock chain, RULESET, the fight table's data, the
post-game menus, CONFIG's menus and storage, and EXTRA CONFIG's screen.

It **cites** the other owners:

- `systems.md`: combat, the economy, chip numbers, the scorecard formulas, what each setting does;
- `tech.md`: stage ids, memory (PRG-RAM pages, the WORK ledger), the raster list, CHR/ExRAM limits, the bank ledger, the
  text engine, **the fight loader's code** (§9.2.1 gives its interface);
- `venues_a.md`, `venues_b.md`, `fortress.md`: staging, mechanics, each stage's secrets and where they sit;
- `story.md`: **every word** (hints, Break Man's debrief, menu labels, ENGRISH, the health notice) and the ending;
- `art_audio.md`: tile, byte and track budgets.

**Tiers** follow RULINGS §0: **Must** = v1.0 (the tight Must), **Should** = v1.1+ (re-added in R0.3's cut-line order),
**Could**, **Won't (v1)**. A Must depends only on Musts (R0.4). Tags: **[engine-ok]**, **[new-code]**, **[new-art]**,
**[new-music]**; sizes **S/M/L**. Session counts come from the ledger (`tools/plan/tight.py`, `tools/plan/tally.py`).

Contents: v1.0 scope · 0 The meta layer in one page · 1 Saves · 2 Title and file select · 3 The bracket, the pit stop
and the fortress maps · 4 The judges' desk and debrief · 5 Medals and HoF points · 6 The championship rating · 7 The
unlock chain · 8 The SYSTEM block · 9 RULESET, the fight table, RECORDS, EXTRA CONFIG and the post-game modes ·
10 Achievements · 11 CONFIG · 12 ENGRISH · 13 Build list · 14 Lessons applied · 15 Cross-doc dependencies · 16 Risks ·
17 Open questions · Changes in round 2 · Changes in round 3.

---

## v1.0 scope

v1.0 is RULINGS R0.2's tight Must. Meta's share is **31 sessions** of code, data and tests (`tools/plan/tight.py`, area
`meta`; the `tally.py` meta rows marked Must sum to the same 31). Round 1's tight estimate was 33.5; the fight loader
(2.5) moved to `tech.md` (R1.7). This revision re-itemises the remaining 31 without changing the total:

- **+0.5** RULESET and the bit table that tech's `IFHARD`/`IFCASUAL`/`LAYOUT_TIER` macros are generated from (round 1
  listed RULESET as a Must item but the ledger had no row);
- **+0.5** the v1.0 fight table and the loader interface (data; the loader's code is tech's);
- **−0.5** title: the attract crawl and the PASS WORD gag are Could (R0.3 item 12); the health notice (R3.5) is one
  text-window page;
- **−0.5** fortress maps: they reuse the bracket's node table and renderer (§3.9).

Everything in this table is **Must** and depends only on Must items (R0.4). Milestones are RULINGS §6's.

| # | Item (section) | What ships in v1.0 | M | Sessions |
|---|---|---|---|---|
| 1 | Save module (§1) | 3 files + system block, A/B ping-pong copies, trailer and commit marker, load with BROKEN paths, migrations, autosave points 1-9, IN_MATCH and UNPLUGS, the save tests of §1.9 | M2 | 3.5 |
| 2 | Title and boot (§2.1) | license line, **health notice** (R3.5), title menu (GAME START, CONFIG, SPECIAL EVENTS once unlocked) | M2 | 1.5 |
| 3 | File select and NEW GAME (§2.2-2.3) | 3 cards, NEW / START / ERASE with the START+A guard, the CASUAL / NORMAL / HARD pick | M2 | 2.5 |
| 4 | The bracket (§3.1-3.7) | node table, node states, centre logic, rematches (the `H_REMATCH` operand hook at `$3F:$F952`), the HALFTIME RIOT trigger and POSTPONED, the event queue (POWER, JET, the Riot, the theft), game over and RETIRE entry points | M2 1.5, M5 1.5, M6 1 | 4 |
| 5 | Results screen (§4.0) | the judges' desk, slide-in rows, TOTAL, medal stamp with the preset badge, prize line, secret icons | M2 | 2.5 |
| 6 | Debrief engine and predicate tables (§4.1-4.6) | the 4MI predicate walk per stage, requirement hints, **tier B only** (tier A is Should, R4.5), the stage counters behind every collect-N secret (R1.10) | M2 | 2 |
| 7 | Medals, HoF points, unlock bits (§5, §7) | medals derived from the best score, HoF points over the shipped stages, the v1.0 unlocks (RECORDS, EXTRA CONFIG) | M2 | 1 |
| 8 | RULESET and the bit table (§9.0) | the 16-byte choke point at WORK `$6270`; `src/gp/bits.inc` generated from §1.6's DIFF A table | M2 | 0.5 |
| 9 | CONFIG (§11) | global: LANGUAGE, ANNOUNCER, TEXT SPEED, FLASHES (REDUCED), SCREEN SHAKE, **INPUT LAG**, SELECT SWAP, A/B SWAP; per file: the difficulty group including the **CASUAL** bit | M2 | 1.5 |
| 10 | EXTRA CONFIG and the test mailbox (§9.6) | the field editor on a scratch file, ENTER STAGE, TO BRACKET, WRITE FILE (marks EDITED), the mailbox format (M2); `FIGHT n` through tech's loader (M7) | M2 2.5, M7 0.5 | 3 |
| 11 | Pit stop (§3.8) | SHOP, the 14-chip grid with B help pages (R2.10), the file's CONFIG page, SAVE & QUIT | M3 | 2.5 |
| 12 | Game over, RETIRE, unplug (§3.7, §1.7) | CONTINUE / RETIRE, the pause-menu RETIRE row, the unplug count | M3 | 1.5 |
| 13 | RECORDS pages 1-3 (§9.4) | FILE RESULTS, FILE TOTALS, LIFETIME with the venue mini-records | M6 | 1.5 |
| 14 | Fight table, v1.0 rows, and the loader interface (§9.2.1) | the ids for every fight, and 11-byte records (with the per-fight pinch byte) for every v1.0 boss (the mid-boss records, which only GP Rush needs, are Could); the calls and results meta uses | M7 | 0.5 |
| 15 | Fortress maps (§3.9) | the Hall of Fame map (H1, H3, H5) and the Castle map (W2, W3), REPLAY, **BACK TO BRACKET**, per-wing saves | M7 | 1.5 |
| 16 | Championship rating and Break Man's debrief (§6) | the rows **re-derived so 100 is reachable with v1.0 content** (R2.7), the first-failed-test debrief | M8 | 1.5 |
| | **Meta Must total** | | M2-M8 | **31** |

Per milestone: **M2 19** (save, title, file-select-lite, bracket-lite, results, debrief, medals, RULESET, CONFIG,
EXTRA CONFIG: RULINGS §6's M2 list for meta), **M3 4** (pit stop with 3 shop chips, game over and RETIRE), **M4 0**
(the Blizzard slice uses items 1-12), **M5 1.5** (the full 8-venue bracket and the adaptor events), **M6 2.5** (the
HALFTIME RIOT trigger, RECORDS), **M7 2.5** (the fight table and `FIGHT n`, the fortress maps), **M8 1.5** (the
rating). M9's balance pass (T11's time limit, the medal thresholds) and the hardware power-cycle test of the save are in
the ledger's `overhead` rows.

**The slice (v0.1) path through meta**: power on → health notice → title → FILE SELECT → NEW (difficulty) → the bracket
(Blizzard's node; the Opening is a v0.5 stage, so the slice's new file starts at the bracket) → SUMMIT CLIMBER → judges'
desk with the BL0-BL2 debrief → autosave → reset → reload → REMATCH from the bracket. The mailbox drives the same path in
the test suite. The slice's new file owns no forms (POWER comes with the 2nd win), so no slice screen depends on FORMS;
the POWER and JET events (§3.6) arrive with the full bracket at M5 (R8.2). Meta's slice code reads the stage record v0 that
exists from M2.1 (`SA.META`, `SA.FLAGS1` b2 REMATCH for `H_REMATCH`) exactly as later stages do: there is no stage-`$00`
stop-gap (R8.2, `tech.md` §4.1).

**Testing policy hooks** (RULINGS §6, scope-26): golden movies run on NORMAL + EN, which are the mailbox defaults; every
other meta setting gets one smoke movie per milestone, set through the mailbox's override bytes (§9.6) instead of menus;
movies are re-recorded only at ⛳ gates; the save module has offline `.sav` fuzz tests (§1.9). The ~10 % test overhead is
in the ledger's `overhead` rows, not in the items above.

**Not in v1.0** (designs kept below as v1.1+ material, each marked in place):

| Tier | Items (cut-line item, R0.3) |
|---|---|
| **Should (v1.1+)** | tier A debrief riddles (text, R4.5); the requirement hints R1, R3 and R5 and W3's three hints (text: no v1.0 predicate or desk uses them, §4.4-§4.5); Knight's mini-record (§9.4); Doc Robot MK-VI's fight record `$29` (§9.2.1); Time Attack (item 7); file COPY; the sponsor's-chair gag and the Eddie SAVING icon; the HUD TIMER option; Break Man joining (EVENTS b5, with the tag partner, item 2) |
| **Could** | the attract crawl, ENGRISH and achievements (item 12); GP Rush runner, lobby, courses and MY GP (item 11); the 1993 RULES preset's meta hooks (item 10); the Could bundle's pit-stop rows, the TURBO trap and BREAK MAN WALKS (item 9); the Exhibition layer and badges (item 6); the Riot intro animation; the hidden PASS WORD gag; RECORDS pages 5-6; the MMC5 AUDIO options (with the MMC5 pulse driver) |
| **Won't (v1)** | KNOCKOUT, Exhibition Rules (and its TURBO rule), the Museum and its VAULT, Bass Mode, Mr. X Returns (R0.3) |

---

## 0. The meta layer in one page

The premise reaches the menus too (CX lesson 1):

- the file select is an **entrant registration desk**;
- the stage select is a **bracket**;
- every clear ends at the **judges' desk** with a scorecard and one hint;
- the ending prints a **championship rating** out of 100, and Break Man gives the 4MI-style debrief;
- the post-game is **SPECIAL EVENTS**: in v1.0, RECORDS and EXTRA CONFIG; Time Attack (Should) and GP Rush (Could) join
  it later.

**Progression flow (v1.0):**

```
POWER ON → RAM probe (tech) → mailbox check (tech) → license → HEALTH NOTICE → TITLE
TITLE → GAME START → FILE SELECT (3 files)
   new file  → pick CASUAL / NORMAL / HARD → OPENING CEREMONY (meta 0, engine $10) → BRACKET
   old file  → BRACKET  (or the fortress map, if the file is inside H1-W3)
BRACKET (8 venues, any order; SELECT = PIT STOP; replays allowed)
   2nd win → POWER hand-off event     4th win → JET hand-off event, then the HALFTIME RIOT intro
   HALFTIME RIOT (meta 9, engine $11, the centre node) must be won before the other 4 venues reopen
   8 wins → centre = TROPHY → theft scene → HALL OF FAME map (H1 → H3 → H5) → unmasking
          → SUPER WILY CASTLE map (W2 → W3) → the ending (story's order, R4.1), which includes the
            CHAMPIONSHIP RATING and Break Man's debrief → TO BE CONTINUED
   → title; SPECIAL EVENTS (RECORDS, EXTRA CONFIG) on the title menu; the file reopens in the post-game bracket
```

| Layer | Must (v1.0) | Should (v1.1+) | Could / Won't |
|---|---|---|---|
| Saves | 3 files, A/B copies, checksums, autosave, migrations, BROKEN paths | file COPY | — |
| Front end | boot with the health notice, title, file select, CONFIG | — | attract crawl, PASS WORD gag (Could) |
| Bracket | 8 venues, rematches, the Riot trigger, centre progression, pit stop, event queue, fortress maps | — | Exhibition layer, Riot intro animation (Could) |
| Judging | results screen, debrief predicates with tier B hints, medals, HoF points | tier A riddles, the sponsor's-chair gag | — |
| Ending | championship rating (100 reachable in v1.0), Break Man's debrief | — | the partner row T1 and the TURBO trap (with the Could bundle) |
| Post-game | EXTRA CONFIG (also the dev tool), RECORDS 1-3, the fight table | Time Attack (and RECORDS page 4) | GP Rush, MY GP, achievements, ENGRISH, RECORDS 5-6 (Could); KNOCKOUT, Exhibition Rules, Museum, Bass Mode, Mr. X Returns (Won't) |

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

PRG-RAM is 32 KB, battery-backed, in 4 pages (`tech.md` §2, D5; R1.6). The saves live in **page 0 (SAVE)**. The running
images live in **page 1 (WORK)**, which is always mapped at `$6000` (`tech.md` §3.4, §13; consistency decision 37).

- The NES 2.0 header declares the 32 KB as **PRG-NVRAM**. 4MI's header declares PRG-RAM size 0, the r4mi lesson 12
  warning (`tech.md` §1.1 owns the header; its boot RAM probe stops with a message if fewer than 32 KB are present).
- **Page 0 is mapped only inside the save module**: `save_commit` and `save_load` map it at `$A000` (`$5115 = $00`,
  shadow `$4B = $80`), copy, and map `$A000` back (`tech.md` §13). RESET maps it briefly to read the test mailbox.
- **Write protection is by isolation**, not by MMC5's gate. MMC5's `$5102/$5103` gate covers all PRG-RAM at once, so it
  stays open while WORK is in use (`tech.md` §2.2). Since no code but the save module maps page 0, a runaway write lands
  in WORK or in the current layout page (both rebuilt), never in the saves. The A/B copies and checksums (§1.3) are the
  second line of defence, and they are designed to be enough on their own.

**Page 0 map** (offsets in the page; CPU address = `$A000` + offset while the save module has it mapped):

| Offset | Size | Use |
|---|---|---|
| `$0000-$03FF` | 1 KB | SYS-A: system block, copy A |
| `$0400-$07FF` | 1 KB | SYS-B |
| `$0800-$09FF` | 512 B | FILE1-A |
| `$0A00-$0BFF` | 512 B | FILE1-B |
| `$0C00-$0DFF` | 512 B | FILE2-A |
| `$0E00-$0FFF` | 512 B | FILE2-B |
| `$1000-$11FF` | 512 B | FILE3-A |
| `$1200-$13FF` | 512 B | FILE3-B |
| `$1400-$19FF` | 1.5 KB | reserve (round 1 put the LIVE images here; they moved to WORK) |
| `$1A00-$1A1F` | 32 B | **TEST MAILBOX** (§9.6) |
| `$1A20-$1FFF` | 1,504 B | reserve (save growth before v1.0: with `$1400-$19FF` the FILE blocks can grow to 768 B each, §16 risk 3) |

**The running images** (WORK, page 1, `tech.md` §3.4):

| CPU address | Size | Use |
|---|---|---|
| `$7400-$75FF` | 512 B | **LIVE FILE**: the running game's file image, laid out exactly like a file block (§1.6) |
| `$7600-$79FF` | 1 KB | **LIVE SYS**: the running system block (§8) |
| `$6270-$627F` | 16 B | RULESET (§9.0) |

**The LIVE FILE is the format.** A file's saved payload and the running state are the same 512-byte image, so a save
is "checksum + copy" with no serialiser to keep in sync.

The vanilla variables that stay in CPU RAM are gathered into the image at each commit and scattered back at load,
as 4MI does at `$40:$AF1F` / `$A9A3`:

- weapons `$0688-$0691` (owned bits only; energy is never saved);
- E-tanks `$06A1`;
- lives `$A9`.

The play-time counter ticks in CPU RAM or the run block, never inside LIVE, so the NMI can never change the image while
it is being checksummed. It is folded in just before each commit.

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

**Commit (save) one block** (`save_commit(block)`, tech's C-window service in core bank `$3E`, `tech.md` §13):

1. Fold the play-time counter and the CPU-RAM variables into LIVE.
2. Increment LIVE's generation (16-bit) and compute the trailer in LIVE.
3. Map page 0. Pick the **target copy**: an invalid copy if there is one, else the one with the older generation.
4. Invalidate the target first: write magic byte 0 = `$00` and marker +E = `$00`.
5. Copy bytes `$001` to the end of the trailer except the marker.
6. Write magic byte 0, then marker +E/+F last. Map `$A000` back.

**The scratch image never commits**: if LIVE's magic byte 3 is `'S'` (EXTRA CONFIG's scratch file, §9.6) or RULESET
says NO_SAVE (a fight-loader bout, `tech.md` §4.6), `save_commit` returns at once.

A file commit checksums and copies 512 bytes: about 10,000 CPU cycles for the checksum and 7,000 for the copy, or 0.6 of
a frame (a system commit is twice that). It runs at meta's commit points (§1.5), never mid-action. On menu screens a
`SAVING` label shows for 30 frames so the player trusts it (story's word); in stages the commits (entry, death) are
silent. The Eddie-with-a-clipboard icon is Should.

**Load one block:**

- **Both copies valid:** take the newer generation. Compare by serial-number arithmetic:
  `(int16)(genA - genB) > 0` means A is newer.
- **One copy valid:** take it. The next commit overwrites the bad one, so the block repairs itself.
- **Neither valid:** the file is **BROKEN**. The file card says `BROKEN DATA` and offers ERASE only. **No screen ever
  hangs on a broken block**: every reader (title, file select, RECORDS, EXTRA CONFIG) has a BROKEN path. A broken
  system block re-initialises to defaults with a one-line notice.

**Version migration.** Header byte +4 is the layout version, **1 at the v1.0 release** (the layout is frozen then).
On load, a block with an older version runs a migration routine per step (v1→v2, …) before use. New fields only ever
take reserved bytes, so a v1.0 save still loads in v1.1. That is also why §1.6 and §8 **already allocate the fields
of every Should and Could item** (the chip bundle's bits, TAG_STAGES, the Time Attack and GP Rush records): adding them
in v1.1 needs no migration [new-code] S · Must.

**COPY** (Should): copy the source's newest valid copy into the target's LIVE image, set the slot byte and generation
1, and commit twice so both copies are fresh.

**ERASE:** zero the magic of both copies. It asks for START+A (§2.2).

### 1.5 Autosave points [new-code] S · Must

| # | When | What changes | Why |
|---|---|---|---|
| 1 | The NEW GAME difficulty is confirmed | the new file (both copies) | The file exists before the Opening starts |
| 2 | **Stage entry** (after READY) | `IN_MATCH` = meta index + 1; attempts | The unplug detector (§1.7) |
| 3 | **Every death** (during the death fade) | KOs, lives, stage KOs, CHAMP_KO, bolts (the 1-bolt insurance, R4.3) | Deaths count, as in 4MI; resetting cannot hide them |
| 4 | **Stage clear**, after the scorecard and bolts (§4.0 step 7) | clears, secrets, prizes, best score/time/PAY, weapons, `IN_MATCH = 0` | The main progress save |
| 5 | Leaving the **pit stop** | bolts, chips, consumables, the file's CONFIG page | Purchases stick |
| 6 | The game-over choice | game overs, lives refill, `IN_MATCH = 0` | |
| 7 | After each **bracket or map event** plays (§3.6) | EVENTS, EVENTS2, FORMS | Story beats play once |
| 8 | **W3 cleared** (before the ending starts), then again after the rating screen | CLEARED, CHAMP_TIME; then BEST_RATING, LAST_RATING, LAST_ROWS | A reset during the long ending loses nothing |
| 9 | Leaving CONFIG, a new record, an unlock | **system block** only | |

**No autosave runs under FIGHT_CTX** (W2's bouts, EXTRA CONFIG's `FIGHT n`, the mailbox fight): tech's loader sets
NO_SAVE (`tech.md` §4.6), and the hub's own clear saves afterwards.

**Not saved** (each is restored to a fixed value instead):

| Not saved | On load it becomes |
|---|---|
| HP | full |
| weapon energy | full; vanilla fills it from the owned flags at stage start, `$3B:$BA3F` |
| checkpoint | the stage start; a load never resumes mid-stage |
| current form | Normal |
| the run block (scorecard counters, Beat's per-screen mask, the second-wind flags) | cleared at stage start (`systems.md` §15.1) |

A loaded file always resumes at the **bracket**, or at the **fortress map** of the next uncleared H or W stage
(§3.9). Vanilla never saved fortress progress; GP saves after every fortress stage.

### 1.6 FILE block layout (512 B) [new-code] S · Must

"Meta index" is the stage's row in the meta tables (§1.8), not the engine stage id: `tech.md` §4.2 owns the ids, and the
stage-attribute record carries the meta index in `SA.META`. Multi-byte values are little-endian. **This is the final
layout** (consistency-11): it applies `systems.md`'s round-2 list (§15.1 there), frees the stale fields, and reserves
every v1.1+ field now, because the layout freezes at v1.0.

| Offset | Size | Field | Notes | Tier |
|---|---|---|---|---|
| `$000` | 4 | magic `'R' '6' 'F' n` | n = `'1'`..`'3'`; `'S'` = scratch (never committed) | Must |
| `$004` | 1 | layout version | 1 at v1.0 | Must |
| `$005` | 1 | FILEFLAGS | b0 ACTIVE; b1 CLEARED (won the championship once); b2 **EDITED** (EXTRA CONFIG wrote it, §9.6); b3 HARD_CLEAN (the HARD preset with every sub-setting unchanged since NEW GAME, never lowered); b4 R1993_CLEAN (likewise for 1993 RULES; Could); b5 BASS (Bass Mode; Won't, reserved); b6-7 reserved | Must |
| `$006` | 2 | generation | | Must |
| `$008` | 1 | IN_MATCH | 0 = none, else meta index + 1 | Must |
| `$009` | 1 | DIFF preset | 0 CASUAL, 1 NORMAL, 2 HARD, 3 1993 RULES (Could), 4 EDIT | Must |
| `$00A` | 1 | **DIFF A** | **b0-1** DAMAGE (0 ×1, 1 ×0.5, 2 ×1.5, 3 ×2); **b2-3** DROPS (0 NORMAL, 1 LESS, 2 MORE, 3 NONE); **b4 CASUAL** (`CFG_CASUAL`, R2.9); **b5 GUARDS**; **b6 HARD** (in V for `BIT`); **b7 RULES = 1993** (in N for `BIT`; Could). Criticals are gone (R2.4) | Must |
| `$00B` | 1 | DIFF B | b0-3 LIVES 1-9; b4-6 E-TANK FLOOR 0-4; b7 reserved | Must |
| `$00C` | 1 | LOWEST | the easiest setting ever active on this file, as a preset number (0 CASUAL < 1 NORMAL < 2 HARD); for achievements | Must |
| `$00D` | 1 | DIFF C | b0-1 REFILL on respawn (0 NONE, 1 HALF, 2 FULL); b2-7 reserved | Must |
| `$00E` | 2 | reserved | | |
| `$010` | 3 | STAGE_CLEAR | 24 bits by meta index: bit m = meta stage m cleared at least once. Read by the bracket, LAND, EXPRESS and Blizzard's replay-skip door (the venue docs) | Must |
| `$013` | 1 | STORY_BEAT | Story position; `story.md` §0 owns the values (`$00`-`$0C`). Meta reads it only for the sponsor's chair (§4.0) and the load target | Must |
| `$014` | 1 | EVENTS | b0 POWER handed over; b1 JET handed over; b2 Riot intro; b3 HALFTIME RIOT won; b4 trophy theft; b5 Break Man joins (Should, with the partner); b6 Mr. Y unmasked; b7 post-game bracket intro (§3.6) | Must |
| `$015` | 1 | EVENTS2 | b0-3 badges E1-E4 lit (Could); b4 SUPER adaptor scene (Roll on the map, story S29); b5 BREAK MAN WALKS (Could bundle); b6-7 reserved | Must |
| `$016` | 1 | FORMS | b0 POWER; b1 JET; b2 SUPER (real save flags, BRIEF §4; SUPER is set when Rush docks in H3 screen 12, consistency-28); b3 TAG (Break Man callable; Should); b4-7 reserved | Must |
| `$017` | 1 | FORM_DEBUT | b0 POWER, b1 JET, b2 SUPER: the vanilla Rush-docking cutscene has played once for this form (`systems.md` §1.3, R2.3) | Must |
| `$018` | 24 | SECRETS[24] | By meta index. **b0** SECRET EXIT (fortress: the showpiece); **b1** HIDDEN ROOM; **b2** BEHAVIOUR ITEM (venues: the chip; fortress: the prize); **b3** PLATE (venues; fortress: H5's Mr. X card); **b4** SPONSOR ENVELOPE taken (30 bolts once, `systems.md` §7); **b5-7** MISS (§4.1, saturates at 7). The 4 plates sit at meta 5 (E), 6 (B), 7 (A), 8 (T) | Must |
| `$030` | 2 | WEAPONS | `$030` b0-7 = the 8 champion weapons **by venue id** (b0 B.ATTACK … b7 C.FLASH); the menu slot comes from `systems.md`'s venue id → weapon slot table (consistency-37); `$031` b0 MAGNET BEAM (slot 9); b1-7 reserved | Must |
| `$032` | 1 | E-TANKS | max 4 (5 with the bundle's TANK RACK) | Must |
| `$033` | 1 | W-TANKS | max 2 | Should |
| `$034` | 1 | LIVES | On load: lives = max(saved, the file's LIVES setting), as in 4MI | Must |
| `$035` | 3 | reserved | consumables, if `systems.md` adds any | |
| `$038` | 2 | BOLTS | 0-999 (`systems.md` §7 caps the counter) | Must |
| `$03A` | 3 | **CHIPS_OWNED** | 24 bits in `systems.md` §9.2's order: bits 0-13 the 14 v1.0 chips; **bits 14-17 reserved for the Could bundle** (IRON HELMET, THERMOS, BIRD SEED, Y-TURBO); 18-23 spare | Must |
| `$03D` | 3 | **CHIPS_EQ** | equipped chips, same bits (a bitmask, not slot positions) | Must |
| `$040` | 4 | **PRIZES** | 32 bits, one per placed prize, paid once per save; bit = `PRIZE_BASE[meta]` + the stage's prize index (§1.6.1) | Must |
| `$044` | 1 | PARTS_GOT | 8 bits, SNOW GUST SEED EMBER KATANA SPUR CREST SHELL (`systems.md` §9.4) | Could (bundle) |
| `$045` | 1 | PARTS_USED | spent in the garage or at Mr. Y's booth | Could (bundle) |
| `$046` | 1 | GARAGE | b0 TANK RACK built; b1-7 reserved | Could (bundle) |
| `$047` | 1 | RATEFLAGS | b0 **DOPED** (Y-TURBO taken; bundle); b1 MR. X'S CARD found; b2 RIVAL (Bass β duel 1 with no damage); b3 **CHAMP_KO** (died in a champion's boss room; negative); b4 **SOLO RIOT** (Bass β duel 1 won without Break Man's capsule, §6.1; `fortress.md`'s round-2 "NO-CAPSULE" bit is this bit, R8.5); b5-7 reserved | Must |
| `$048` | 1 | BASS_ADAPT | the damage column used most in Bass β duel 1; his duel-2 armour starts adapted to it (`systems.md` SC6) | Must |
| `$049` | 1 | reserved | | |
| `$04A` | 1 | COMMFLAGS | `story.md`'s once-per-save commentator flags, b0-7 (story §6.1 owns the meanings) | Must |
| `$04B` | 3 | TAG_STAGES | 24 bits: meta stages where Break Man was called | Should |
| `$04E` | 4 | WEAKFOUND | 32 bits, one per boss row: weakness found (`systems.md`) | Could |
| `$052` | 14 | reserved | `systems.md` / `story.md` growth | |
| `$060` | 240 | STAGEREC[24] × 10 | by meta index. +0 best score (0-100, `$FF` none); +1 badge: b0-1 the preset of that best score (0 C, 1 N, 2 H, 3 93), b2 **asterisk** (earned with Y-TURBO equipped; bundle), b3-7 reserved; +2 best PAY (0-160, `systems.md` §6.6: a replay pays the improvement over this); +3 clears (saturates at 255); +4/5 best clear time in frames (saturates at `$FFFF`); +6/7 KOs; +8/9 time spent, in 256-frame units | Must |
| `$150` | 4 | PLAYTIME | frames, 32-bit (ticks only while a file is active) | Must |
| `$154` | 4 | CHAMP_TIME | PLAYTIME at the first championship; 0 = none | Must |
| `$158` | 2 | KOS | total deaths | Must |
| `$15A` | 2 | GAMEOVERS | | Must |
| `$15C` | 1 | UNPLUGS | saturates at 255 | Must |
| `$15D` | 3 | BOLTS_EARNED | 24-bit | Must |
| `$160` | 3 | BOLTS_SPENT | 24-bit (the 1-bolt insurance counts) | Must |
| `$163` | 2 | TAG_CALLS | Break Man calls | Should |
| `$165` | 2 | ETANKS_USED | | Must |
| `$167` | 2 | WEAK_HITS | first-weakness pops | Must |
| `$169` | 1 | BEST_RATING | 0-100, `$FF` = none | Must |
| `$16A` | 1 | LAST_RATING | | Must |
| `$16B` | 7 | LAST_ROWS | the seven rating rows (§6.1) | Must |
| `$172` | 126 | reserved | growth (§16 risk 3) | |
| `$1F0` | 16 | trailer | §1.3 | Must |

**Removed** (consistency-11, `systems.md` §15.1): METALLS (IRON HELMET is crafted now), the DOVE flag, CRITICALS (DIFF A
b4 now holds CASUAL), round 1's 16-bit chip fields. BREAK_JOINED is FORMS.TAG. DROPS has no VANILLA value: under
RULES = 1993 the drop reader uses vanilla's weights whatever b2-3 say (consistency-11, the conservative option).

**The DIFF A bit table is the source of `src/gp/bits.inc`** (consistency-15, `tech.md` §5.5): every doc's code uses the
generated macros, never raw bits. `IFHARD` = `BIT RS_DIFF / BVC skip`; `IF1993` = `BIT RS_DIFF / BPL skip`;
`IFCASUAL` = `LDA RS_DIFF / AND #$10 / BEQ skip`, where `RS_DIFF` is RULESET's copy of DIFF A (§9.0), so Time Attack,
GP Rush and fight records can override it in one place. A unit test asserts each macro follows its bit and nothing else.

#### 1.6.1 Prize bits [data] S · Must

One ROM table `PRIZE_BASE[24]` (by meta index) gives each stage's first PRIZES bit; a stage's prize object carries its
local index n (`GP_ARG`), and the collector sets bit `PRIZE_BASE[m] + n`. The indexes are the venue docs':

| Bits | Stage | Prizes (the stage doc's indexes) |
|---|---|---|
| 0-3 | Blizzard (meta 1) | the 4 bonus vegetables, 10 / 10 / 15 / 25 = 60 (`venues_b.md` §0.9) |
| 4-7 | Plant (meta 3) | the 4 treasures #0-#3, 10 / 15 / 15 / 20 = 60 (`venues_a.md` §0.8) |
| 8-10 | Tomahawk (meta 6) | the 3 bounties #0-#2, 15 / 20 / 25 = 60 |
| 11 | Knight (meta 7) | the torch-pocket pouch #0, 20 |
| 12-31 | spare | |

Wind, Flame, Yamato and Centaur have no prizes. **The non-venue stages use no PRIZES bits** (`fortress.md` §0.4, §9.3;
consistency-19): their prize bolts (≤ 30 on b0, ≤ 30 on b2) are paid once when SECRETS b0 / b2 is first set, so those
bits already record them, and their `PRIZE_BASE` entries are unused. The ≤ 60-per-stage cap is `systems.md`'s (R2.7);
the build checks it against this table.

### 1.7 The unplug detector [new-code] S · Must (the count); the line is Should

`IN_MATCH` is set at stage entry (autosave 2) and cleared at a clear, a RETIRE or a game over. If a file loads with
`IN_MATCH ≠ 0`, the stage was abandoned by power-off or reset. The load then:

- adds 1 to UNPLUGS and to that stage's KOs;
- queues a commentator line for the bracket (story S16's words; Should: if the line is not in the build, nothing shows).

Deaths are already saved on the spot (autosave 3), so unplugging gains nothing. The counter is flavour, plus rating T12
(§6.1). It is Must because T12 is.

### 1.8 Meta index and engine ids (save-table rows)

The meta index is unchanged from round 1, so the id-map dispute never touched the save format (consistency strength).
Engine ids are `tech.md` §4.2's binding map (R1.2); `SA.META` maps one to the other.

| Meta | Stage | Engine id | Tier |
|---|---|---|---|
| 0 | Opening Ceremony (Opening-lite) | `$10` | Must |
| 1-8 | the 8 venues, in vanilla stage-id order: Blizzard, Wind, Plant, Flame, Yamato, Tomahawk, Knight, Centaur (meta = vanilla id + 1) | `$00-$07` | Must |
| 9 | **HALFTIME RIOT** (R4.3) | `$11` | Must |
| 10-13 | Exhibitions E1-E4 | `$12-$15` | Could (R3.7; E4 Won't) |
| 14-18 | Hall of Fame H1-H5 | `$16-$1A` | H1, H3, H5 Must; H2, H4 Should |
| 19-21 | Super Wily Castle W1-W3 | `$1B-$1D` | W2, W3 Must; W1 Could |
| 22 | Mr. X Returns | `$1F` | Won't (v1) |
| 23 | Victory lap (the playable credits) | `$1E` | Could (R0.3 item 8) |

Legacy ids `$08-$0F` (vanilla Mr. X 1-4, Wily 1-4) have no meta index: they are regression data and fight-table arenas.

Medals and HoF points count **the stages a build ships**: in v1.0, meta 0-9, 14, 16, 18, 20 and 21 (15 stages).

### 1.9 Save tests (the testing-policy hooks) [new-code] S · Must (inside item 1's 3.5 sessions)

- **Offline fuzz** (`tools/test/savefuzz.py`, every build's unit suite): it writes 32 KB `.sav` images (page 0 at file
  offset `$0000`) for each case, boots the build headless to the file select, and asserts the card state from RAM:
  both copies valid (newer generation wins), generation wrap (`$FFFF` vs `$0000`), one copy torn (marker missing), one
  copy with a bad checksum byte, both bad (`BROKEN DATA`, ERASE only), an older layout version (the migration runs), a
  newer one (BROKEN, never loaded), a broken system block (defaults plus the notice).
- **Round trip**: a mailbox run plays Blizzard to the clear, resets, reloads, and compares LIVE FILE byte for byte with
  the image before the reset (play time masked).
- **Power cut on hardware** (M9, the user's cart, RULINGS §7 question 1): power off during a commit, 20 times at random
  frames; every reload must show either the old or the new state, never BROKEN for both copies.

---

## 2. Title flow and file select

Every label and line on these screens is `story.md`'s (R4.1); the names below are identifiers. Menu screens run in a
scheduler thread (code in meta's banks `$42-$43`, `tech.md` §1.2) and wait through `JSR $C62B` / `$C5F6`, so text and
glyph uploads never hit the lag-frame trap (`tech.md` §11.6). Their pages use the 4 × 28 window (R1.4).

### 2.1 Boot, health notice and title [new-code] S · Must; [new-art] S · Must (art_audio's title plan)

1. **RAM probe and mailbox** (`tech.md` §2.3, §14.5): a short-RAM emulator stops with tech's message; a valid test
   mailbox (§9.6) jumps straight to its command.
2. **License screen**: vanilla script `$1F` (`rm6/text.md` §5.1) plus one GP line (story S01's words) [engine-ok + text].
3. **Health notice** (R3.5) [new-code] S · Must: one 4 × 28 page in the text window on a black menu screen (text v1a),
   story's words, telling the player that the game has flashing effects and that CONFIG → FLASHES → REDUCED turns every
   flash into a fade. It shows on every power-on and reset, for at least 120 frames, then any button continues. No save
   bit: it is never skipped for good.
4. **Title**: `art_audio.md`'s plan: the vanilla logo and moon backdrop kept, a GP sprite badge, the subtitle with
   グランプリ in place of 戦い, the menu under the pattern-table split (`tech.md` §16.8 M5.8; the slice's title uses a
   plain text menu until then). Music: vanilla `$19`, or art_audio's fanfare when it exists.
5. **Attract crawl** (Could, R0.3 item 12): story S02's GP opening in typed panels after 30 s idle on the title; START
   skips. Without it the title idles as vanilla does.

Title menu (cursor ▶, vanilla style):

| Item | When shown | Does | Tier |
|---|---|---|---|
| GAME START | always | → FILE SELECT | Must |
| SPECIAL EVENTS | once U0.0 is set (§7) | → the post-game menu (§9) | Must |
| CONFIG | always | → CONFIG (§11), global settings only; the difficulty group is per file | Must |
| *(hidden)* PASS WORD | hold SELECT on the title for 2 s | the vanilla password grid, fully working through the vanilla codec `$3F:$F3D0` (`tech.md` §13); a valid vanilla password gets a Kalinka line (story) and sets no progress. A quirk kept on purpose (rm6 lesson 8) | Could |

### 2.2 FILE SELECT: "ENTRANT REGISTRATION" [new-code] M · Must, [new-art] S · Must

Three cards stacked vertically, each 6 tiles tall. Kalinka holds the clipboard at the right (her 16×16 face icon in
v1.0; R5.1).

```
┌ FILE 1 ───────────────────────── NORMAL ┐
│ [8 venue icons: lit = won, medal colour]  │
│  H ▮▯▮▯▮   W ▯▮▮        RIOT ✓            │
│  HOF PTS 37    BOLTS 625     12:34:56     │
│  ★ RATING 87 (FINALIST)        KOS 143     │
└───────────────────────────────────────────┘
```

| Card shows | From | Tier |
|---|---|---|
| venue icons, coloured by medal (none / bronze / silver / gold / platinum) | STAGEREC best score | Must |
| HALFTIME RIOT, Hall of Fame and Castle progress (only the wings the build ships; the others draw as closed) | STAGE_CLEAR | Must |
| Exhibition progress E1-E4 | STAGE_CLEAR 10-13 | Could (with the Exhibitions) |
| HOF PTS | §5.2 | Must |
| BOLTS | `$038` | Must |
| play time h:mm:ss | `$150` | Must |
| difficulty badge (C / N / H, `93` with 1993 RULES, plus `EDIT` if any override is set) | `$009` | Must (93: Could) |
| ★ and the best rating, if CLEARED (with `*` if DOPED) | `$169` | Must (`*`: bundle) |
| a red `*` if EDITED | FILEFLAGS | Must |
| KOs | `$158` | Must |

An empty file shows `NEW ENTRANT`; a broken one shows `BROKEN DATA` (§1.4).

Commands (UP/DOWN pick the card, A/START open a command row under it):

| Command | Rule | Tier |
|---|---|---|
| **START** (on a used file) | Load; go to the bracket or the fortress map (§3.9) | Must |
| **NEW** | On an empty file: go straight to the difficulty pick. On a used file: `OVERWRITE? NO / YES`, with NO first, and YES needs **START+A** (4MI's stray-START guard, `r4mi/modes.md` §4) | Must |
| **ERASE** | `ERASE? NO / YES`, START+A | Must |
| **COPY** | Pick the target file; the same overwrite guard | Should |
| **ENTRANT** | Toggles ROCKMAN / BASS β for a NEW file (§9.7) | Won't (Bass Mode) |

### 2.3 NEW GAME: difficulty pick [new-code] S · Must

Big panels, each with one line of description (story's words; the HARD line must describe v1.0's HARD, not remixed
stages, R2.9):

| Preset | Sets (`systems.md` §13.2) | Tier |
|---|---|---|
| CASUAL | DAMAGE ×0.5, LIVES 5, E-TANK FLOOR 2, DROPS MORE, REFILL FULL, GUARDS on, **CASUAL on** | Must |
| NORMAL | ×1, 3, 0, NORMAL, HALF | Must |
| HARD | ×1.5, 3, 0, **LESS**, **NONE**, **HARD on** (v1.0 HARD = ×1.5 damage, drops LESS, no refill, the 18-f quick-draw; per-stage HARD content is Should, R2.9) | Must |
| 1993 RULES | ×1, 3, 0, vanilla drops, NONE, RULES = 1993 (`systems.md` §13.6: the rules change, the content does not) | Could (R0.3 item 10) |

The pick writes DIFF preset, A, B, C and LOWEST, and sets HARD_CLEAN (or R1993_CLEAN) when the preset is HARD (or
1993). Autosave 1 runs, then the Opening Ceremony starts (in the v0.1 slice, before the Opening exists, the bracket).
Overrides live in the pit stop's CONFIG page (§11.2). Changing anything below the starting preset clears the `_CLEAN`
bit for good (4MI's HARD ROCK rule, `r4mi/modes.md` §5).

---

## 3. The bracket, the pit stop and the fortress maps

### 3.1 From vanilla's grid [new-code] M · Must, [new-art] M · Must

Vanilla facts (`rm6/ram.md`):

- **Grid.** The 3×3 grid is `$3F:$F232` = `00 01 03 FF / 02 FF 05 FF / 04 06 07 FF`; it is read once, at `$3F:$F182`
  [code, r2: `flagscan.py`]. The centre gives stage 8 only when `$05C8` = 0, that is, once all eight are beaten.
- **Beaten stages.** A beaten portrait becomes Rockman's head (the stage select asks `$3F:$F520`, "is this boss
  beaten?", at `$F0D6` [code, r2]), and a plate stage shows its B/E/A/T letter.
- **Rematches.** A beaten boss's room beams Rockman out: there are no rematches (§3.2 has the site).
- **Text.** Script `$12` draws `PUSH START` and the names.

GP keeps the shape (three rows of three frames and a centre) and the vanilla cursor feel, but redraws the screen as a
**bracket** and replaces the cell table with a node table. The whole vanilla stage-select routine is retired (`tech.md`
§4.3 "retired" rows); the bracket is meta's thread code.

**Layout and pairing.** Four portraits stay in their vanilla cells (Blizzard, Wind, Tomahawk, Yamato). Four move so that
each Exhibition pair meets at one of the four inner crossings around the centre: a 5×5 grid with the frames on the even
rows and columns and the badges on the four inner crossings. The pinwheel is kept in v1.0 even though the Exhibitions are
Could (R3.7): the badges then draw as plain rivets (state DARK for good), the B layer is off, and v1.1 only has to light
them.

| | col 0 | (gap) | col 1 | (gap) | col 2 |
|---|---|---|---|---|---|
| **row 0** | BLIZZARD (0) | | WIND (1) | | KNIGHT (6) |
| (gap) | | **E3** ◆ Blizzard + Flame | | **E1** ◆ Wind + Knight | |
| **row 1** | FLAME (3) | | **FINAL** (centre) | | TOMAHAWK (5) |
| (gap) | | **E4** ◆ Yamato + Centaur | | **E2** ◆ Tomahawk + Plant | |
| **row 2** | YAMATO (4) | | CENTAUR (7) | | PLANT (2) |

Numbers in brackets are the engine stage ids (= vanilla ids, `tech.md` §4.2). The frames show the **champions' names**,
not the venue names: the bracket font has `0-9 A-Z . -` and blank only (`story.md` §10.1), and HERO'S QUEST has an
apostrophe. The venue names appear on the match card's VENUE field, which allows `'` (§3.2).

| Badge | Crossing | Wired to | Unlocked by both secret exits of | Tier |
|---|---|---|---|---|
| **E1** | top right | Wind, Knight | Wind + Knight | Could |
| **E2** | bottom right | Tomahawk, Plant | Tomahawk + Plant | Could |
| **E3** | top left | Blizzard, Flame | Blizzard + Flame | Could |
| **E4** | bottom left | Yamato, Centaur | Yamato + Centaur | Won't (E4 Maze is Won't, R3.7) |

The art is bracket lines in the BG (gold when lit, grey when not), 32×32 champion portraits (vanilla's, kept), and
16×16 badges drawn as sprites so they can blink.

**Node table** (data, replacing `$F232`): 13 nodes × 6 bytes, shared with the fortress maps (§3.9).

| Byte | Contents |
|---|---|
| +0 | meta index |
| +1 | x |
| +2 | y |
| +3 | neighbour UP/DOWN (two nibbles) |
| +4 | neighbour LEFT/RIGHT (two nibbles) |
| +5 | layer (0 = ring, 1 = badge) and flags (b7 = not in this build) |

There are 9 ring nodes and 4 badge nodes. Navigation skips nodes that cannot be selected, and nodes flagged "not in this
build".

### 3.2 Controls on the bracket [new-code] S · Must

| Button | Does | Tier |
|---|---|---|
| D-pad | Moves within the current layer | Must |
| START / A | Selects. A venue → the **match card** (vanilla's typed boss-intro panel `$3C:$81B1`, extended by tech to records by fight id with a 10th VENUE field, `tech.md` §11.2) → the stage. A cleared stage first shows a confirm card: best score, medal, best time, the secret icons, and `REMATCH? NO/YES` | Must |
| **SELECT** | **PIT STOP** (§3.8). SELECT is free outside stages (`rm6/ram.md`); in stages it means only the quick swap and the last-weapon toggle (R2.10) | Must |
| **B** | Toggles the **Exhibition layer**: the cursor jumps to the 2×2 grid of badges, B again returns to the ring. The prompt `B EXHIBITIONS` (no `:`: the bracket font has none, consistency-23) shows only once a badge is lit | Could |

**The on-screen venue names** (R3.3, consistency-42; all ≤ 20 characters, the VENUE field's limit):

| Venue (id) | Name | Venue (id) | Name |
|---|---|---|---|
| Blizzard (0) | SUMMIT CLIMBER | Yamato (4) | EDO NINJA ROW |
| Wind (1) | SKY ACE | Tomahawk (5) | HIGH NOON FRONTIER |
| Plant (2) | LOST JUNGLE | Knight (6) | HERO'S QUEST |
| Flame (3) | PERSIAN PALACE | Centaur (7) | ATLANTIS RUINS |

No third-party trademark or character name appears on screen (R3.3); the debrief, panels and RECORDS use these names.

**Rematches are allowed** in GP: medals need replays (BRIEF §5.3). [code, r2] [seen, r2] The vanilla beam-out is one
test in the boss-room routine: **`$3F:$F951 JSR $F527 / BCS $F9A0`** (bytes `20 27 F5 B0 4A`). `$F527` returns carry
set when the boss of the current screen is already beaten (it reads `$0692,X` with the mask from `$F6BB`, or `$F6C3`
when `$57` = the plate screen `$F518`); `BCS $F9A0` then skips the fight and the flag set (`JSR $F4EB` at `$F99D`) and
jumps to the post-kill end path. Measured (`rematch.py`): from Flame's boss shutter with all 8 bosses marked beaten,
vanilla enters screen `$17`, no boss spawns, and `$F0` = 1 (stage over); with the branch replaced by two NOPs the boss
intro spawns (slot 8 type `$93`, bar `$FF`) and the refight starts. GP's hook (registry entry `H_REMATCH`, kind `operand`, owner meta;
`tech.md` §14.2) re-points the JSR operand at `$3F:$F952` to `gp_rematch`, a stub in `$7F` that returns carry clear
when `SA.FLAGS1` b2 REMATCH is set (every venue and every GP stage) and otherwise falls through to `$F527`, so legacy
ids keep vanilla's answer. `BCS $F9A0` stays as it is. On a replay (STAGE_CLEAR bit m already set) the
post-kill path skips the YOU GET card (the weapon is already owned) and goes to the judges' desk; tech's `$3F:$F9A0`
hook (`tech.md` §4.6) carries the test. A replay pays only the score improvement (`systems.md` §6.6).

### 3.3 Node states and what they draw [new-code] S · Must

| State | Ring frame draws | Selectable | Tier |
|---|---|---|---|
| OPEN | The champion's portrait, name | yes | Must |
| WON | The portrait with a **medal ribbon** sprite (bronze/silver/gold/platinum colour); a ★ on the frame if its secret exit is found; the plate letter B/E/A/T in the frame corner if the plate is held | yes (rematch) | Must |
| POSTPONED | The portrait under a red **POSTPONED** stamp (sprite overlay) | no: a Kalinka line (story S09.2) | Must |
| Badge DARK | A plain rivet | no | Must (drawn) |
| Badge HALF | One of its two lines lit, the badge dim and showing `?` | no; START names the missing venue (story) | Could |
| Badge LIT | Blinking badge with the guest's icon | yes | Could |
| Badge WON | Solid badge plus the medal ribbon | yes | Could |

### 3.4 Centre node: the FINAL frame [new-code] S · Must

| Condition (checked in order) | Centre shows | START does |
|---|---|---|
| fewer than 4 venue wins | The GP trophy silhouette with `?` | a Kalinka line (story) |
| 4+ wins and the HALFTIME RIOT not won | **BASS β** portrait, cracked frame, `HALFTIME` | → the HALFTIME RIOT (meta 9, engine `$11`) |
| Riot won, fewer than 8 wins | Trophy, `4 TO GO` → `1 TO GO` | Kalinka counts down (story S24) |
| 8 wins, H1 not cleared | **Lit trophy** | First time: the trophy theft (story S25, EVENTS b4), then the HALL OF FAME map (§3.9) |
| inside H1-W3 | The fortress logo of the current map | → that map |
| CLEARED file | The trophy with Rockman's face | → the **replay list** of meta 0, 9 and the cleared H/W stages |

### 3.5 The HALFTIME RIOT trigger [new-code] S · Must

**HALFTIME RIOT** is the stage's name everywhere (R4.3, design-14): it happens at the bracket's halfway point, and a
stadium riot at halftime is the joke. The rule: **venue wins = popcount(STAGE_CLEAR bits 1-8)**.

- When it reaches **4** and STAGE_CLEAR bit 9 (the Riot) is clear, the bracket is **RIOT_PENDING**.
- While RIOT_PENDING, every unbeaten venue frame is POSTPONED.
- Won venues stay selectable for medal replays, and the pit stop stays open. The player cannot strand themselves,
  because the Riot is selectable at once (§16 risk 5 has the test).
- The Riot's clear sets bit 9. The POSTPONED stamps peel off (event b3), and the last 4 venues reopen.

**The Riot intro** (event b2) plays once, before the Riot opens:

- **Must:** the music cuts, the POSTPONED stamps appear on the unbeaten frames, the centre turns to Bass β's cracked
  frame, the cursor moves to it, and story S14's lines play in the bracket's message window.
- **Could:** the animation (≈ 6 s): an 8-frame scroll shake; Bass β's sprite drops in at the top centre, lands on the
  FINAL frame and fires three buster shots at it (the frame tiles swap to the cracked version); he dashes across the
  four unbeaten portraits, stamping each one as he passes.

The adaptors arrive by win count (BRIEF §4, `systems.md` §2.3):

- **POWER after the 2nd win, JET after the 4th**, stored in FORMS.
- They are handed over as bracket events b0 and b1: Roll's pit-crew pop-up on the bracket (story S12, S13). The words
  belong to `story.md`; the bits and the order belong here.
- On the 4th win the order is **JET event → Riot intro**.

### 3.6 The event queue [new-code] S · Must

Story beats on the bracket and on the fortress maps are **data**: a table of `{condition, event script id, seen bit}`.
The screen runs the first unseen event whose condition holds, sets its seen bit, saves (autosave 7), and repeats until
none are left. Conditions are predicates over STAGE_CLEAR, FORMS, EVENTS, RATEFLAGS and STORY_BEAT, on the same
predicate engine as §4 (CX lesson 7: special cases in visible tables).

| Seen bit | Screen | Condition | Event (story's scene) | Tier |
|---|---|---|---|---|
| EVENTS b0 | bracket | venue wins ≥ 2 | Roll: POWER ready (S12) + `FORMS.POWER` | Must |
| EVENTS b1 | bracket | venue wins ≥ 4 | Roll: JET ready (S13) + `FORMS.JET` | Must |
| EVENTS b2 | bracket | wins ≥ 4 and the Riot not won | the Riot intro (§3.5, S14) | Must (animation Could) |
| EVENTS b3 | bracket | the Riot won | the stamps peel off; "the bracket resumes" | Must |
| EVENTS b4 | bracket (START on the lit trophy) | 8 wins | the trophy theft (S25); STORY_BEAT → `$03` | Must |
| EVENTS b6 | Hall of Fame map | H5 cleared | the unmasking (S33); STORY_BEAT → `$09` | Must |
| EVENTS2 b4 | Hall of Fame map | FORMS.SUPER (set in-stage when Rush docks in H3 screen 12, consistency-28) | Roll explains the Super Adaptor (S29) | Must |
| EVENTS b7 | bracket | CLEARED | the post-game intro: "welcome back, champion" | Must |
| EVENTS b5 | (in-stage) | HALFTIME RIOT screen `0E` | Break Man joins through Rule 9 (S20, played in place, R4.2) and sets `FORMS.TAG` | Should (the tag partner) |
| EVENTS2 b0-3 | bracket | badge n becomes LIT | the badge lights; Cossack announces the guest (S22) | Could |
| EVENTS2 b5 | bracket | RATEFLAGS.DOPED | **BREAK MAN WALKS**: he stands at the bracket's edge, says one line, and leaves for good (S21) | Could (bundle) |

Without the tag partner (v1.0) the Riot still plays Break Man's NPC beats (fortress, story; R4.2), but nothing joins and
b5 stays clear.

### 3.7 Game over and RETIRE [new-code] S · Must

**RETIRE** is a new pause-menu row, available in every stage (the pause font has no D, O, Q or Z, so the label is
`RETIRE`; consistency-23).

- It returns to the bracket (or the fortress map) at once: no life is lost and no scorecard is shown.
- It clears `IN_MATCH`, so it never counts as an unplug.
- On an uncleared stage nothing is saved but the death counters already written.
- The Opening Ceremony has no RETIRE: it is the tutorial, and the bracket does not exist yet.
- Under FIGHT_CTX (a W2 bout) RETIRE leaves the whole hub stage, as a game over would.

**GAME OVER** replaces vanilla's password screen.

- Vanilla shows GAME OVER over the password grid, with STAGE SELECT / CONTINUE (`rm6/text.md` §5.4; music `$14`,
  then `$15`). GP keeps both jingles and the two-choice shape, minus the grid:

  | Choice | Does |
  |---|---|
  | **CONTINUE** | Restart this stage from its start: lives = the file's LIVES, E-tanks = max(held, the E-TANK FLOOR) |
  | **RETIRE** | Back to the bracket or the fortress map. Vanilla's fortress game over offered CONTINUE only (`$3C:$805F`'s fortress test, `tech.md` §4.3), but GP saves per stage, so retiring from a fortress loses nothing |

- GAMEOVERS +1 is saved first (autosave 6).
- One line from story S16's table: Kalinka's rotating lines elsewhere, Mr. Y's (S16.4) in H1-H5, Wily's (S16.5) in
  W2-W3.
- There is no E-tank halving (CX) and no other penalty: the cost is the run, and FAIR PLAY's 4 points (§6).

### 3.8 The PIT STOP [new-code] M · Must (v1.0 rows); the bundle rows Could

`systems.md` §8-§9 own the stock, the prices and the chips. This is the screen. It opens with SELECT on the bracket or
a fortress map, from 0 wins on (after the Opening; consistency decision 14): Eddie behind a counter (Eddie is new art, a
composite, not a vanilla sprite: R8.6, `art_audio.md`), the bolt total top right, and a row list on the left.

| Row | Contents | Tier |
|---|---|---|
| **SHOP** | The stock list: name, price, held / max. A greyed row reads `???` with its unlock (`AFTER 3 WINS`). Buying asks `BUY? NO/YES`; Eddie's line (story S10). v1.0 stock: E-TANK, 1UP, SHOCK ABSORBER, SPIKE GUARD, CHARGE KIT (the slice), EXCHANGER, ENERGY SAVER; W-TANK is Should | Must |
| **CHIPS** | A 7 × 2 grid of the **14 v1.0 chips** (bits 0-13; owned lit, unowned `?`), `SLOTS n/m` at the top. **A** toggles equip (refused with a buzz if the slots are full or the second-wind family is taken, `systems.md` §9.1); **B opens the help page** (4 × 28, story §8's words; R2.10). SELECT does nothing here. With the bundle, a third row shows bits 14-17 | Must |
| **CONFIG** | The file's difficulty page (§11.2) | Must |
| **SAVE & QUIT** | Commits, then returns to the title | Must |
| **GARAGE** | Appears once a PART is owned. The four recipes as `SNOW + EMBER → THERMOS`, unowned PARTs shown as `???` (`systems.md` §9.4). BUILD consumes both PARTs | Could (bundle) |
| **MR. Y'S BOOTH** | After the HALFTIME RIOT, until Y-TURBO is taken: a shady booth sprite stands at the bracket's bottom-right edge under a sign (story's words), and this row runs the offer. He asks twice; the second confirmation reads **"BREAK MAN WILL WALK."** (R2.8). The booth packs up once TURBO is taken | Could (bundle) |

Leaving the pit stop is autosave 5. On a 1993 RULES file (Could) SHOP, CHIPS, GARAGE and the booth are hidden
(`systems.md` §13.6 closes the shop).

### 3.9 The fortress maps [new-code] S · Must, [new-art] S (fortress.md's map art)

Two maps, drawn by `fortress.md` / `art_audio.md`, driven by meta's node table and renderer (§3.1), so they cost a node
list each:

| Map | Nodes (meta) | v1.0 | Opens |
|---|---|---|---|
| **HALL OF FAME** | H1 (14), H2 (15), H3 (16), H4 (17), H5 (18): a line of wings | H1 → H3 → H5; H2 and H4 draw as closed wings (flag b7 "not in this build"; Should), their doors reading `CLOSED FOR RENOVATION` (story S26.4, `fortress.md` §0.3) for as long as those stages are Should | after the trophy theft (EVENTS b4) |
| **SUPER WILY CASTLE** | W1 (19), W2 (20), W3 (21) | W2 → W3; W1 draws closed (Could) | after the unmasking (EVENTS b6) |

| Button | Does |
|---|---|
| START / A on the next uncleared wing | the stage (a match card for its first boss is the stage's own business) |
| START / A on a cleared wing | `REPLAY? NO/YES` (medal replays; the improvement rule) |
| **SELECT** | the PIT STOP (§3.8) |
| **B** | **BACK TO BRACKET**: the bracket, for venue replays, the Riot replay and the pit stop. The centre node leads back here (§3.4) |

- **Saves per wing**: every H or W clear is autosave 4, and a load resumes on this map (§1.5). Vanilla never saved
  fortress progress.
- **The load target**: if EVENTS b4 is set and the file is not CLEARED, the file loads to the Hall of Fame map while an
  H wing the build ships is uncleared, else to the Castle map.
- Events on the maps run through the same queue (§3.6): EVENTS2 b4 (S29) and EVENTS b6 (S33).
- **W3 has no judges' desk**: its clear runs the ending (story's order, R4.1), whose rating screen is the game's
  debrief. W3's scorecard is still computed and stored (STAGEREC, PAY) silently before the ending starts (autosave 8).

---

## 4. The judges' desk and debrief

### 4.0 The results screen (SYS-SC-2's presentation) [new-code] M · Must; the sponsor's chair Should

`systems.md` §6 owns the numbers; this is the screen. It is a black-backed **judges' desk** drawn in the top third:
Cossack (head judge) in the centre and Kalinka (commentary) at the left, drawn as their 16×16 face icons with name labels
in v1.0 (R5.1; desk portraits are Should).

**The sponsor's chair** (Should, one sprite): at the right a cardboard Mr. Y cut-out always holds up a "1". From
STORY_BEAT `$03` (S26, the cup stolen) the chair carries a `BACK SOON` sign, and from `$09` (S33, the unmasking) a
`RESERVED` sign (story's request; its words).

The sequence (about 6 s, A skips each step):

| Step | What appears | Frames |
|---|---|---|
| 1 | `MATCH RESULT` with the venue or stage name (§3.2) and the stage time | 20 |
| 2 | Five rows slide in from the right, one by one: `TIME 14/20`, `DAMAGE 11/20`, `VARIETY 25/25`, `SECRETS 5/20`, `STYLE 6/15`, each with a tick SFX | 5 × 16 |
| 3 | The TOTAL counts up | 30 |
| 4 | The **medal stamp** (or none), with the C/N/H preset badge (`93` with 1993 RULES, Could) and, with Y-TURBO equipped, the `*` (bundle) | 20 |
| 5 | `PRIZE +81 BOLTS`. On a replay: `IMPROVEMENT +12` or `NO IMPROVEMENT` (`systems.md` §6.6) | 20 |
| 6 | Secret icons for this stage: exit, room, item, plate and envelope; found ones lit, this run's new ones flashing | 20 |
| 7 | The debrief hint types into the 4 × 28 window below (§4.1) | text |

Then autosave 4 runs, and the bracket (or the fortress map) returns. W3 skips the desk (§3.9). Under FIGHT_CTX there is
no desk (`tech.md` §4.6).

### 4.1 How the debrief plays [new-code] M · Must (tier B); tier A Should

Every stage clear ends at the desk. **One debrief hint** types into a box under the scorecard: 4 lines × 28 cells
(R1.4), pre-wrapped by the text compiler. The speaker is **Kalinka** at the commentary desk (story §7 confirms: she
"hears things").

The line is chosen 4MI's way (`r4mi/modes.md` §1.5: entry = first failed test), but **per stage**:

```
blocked = none
for each predicate p of this stage, in table order:
    if p passes: continue
    if p.require is not met:
        if blocked == none: blocked = p                         (remember it, keep looking)
        continue
    tier = (SECRETS[m].MISS >= 2) ? B : A                       (escalation)
    if HINT[p.hint].A is absent: tier = B                       (v1.0: tier A is Should, R4.5)
    show HINT[p.hint].tier; goto done
if blocked: show REQ_HINT[blocked.require]; goto done           (CX lesson 6: telegraph the tool)
show a "perfect venue" line
done: if any predicate failed, SECRETS[m].MISS += 1 (saturating at 7)
```

A predicate that needs a tool the player lacks never hides a hint the player can use now. The "come back with JET" line
appears only when everything left is tool-gated.

- **v1.0 (Must):** tier B only (R4.5, scope-18): every hint is the plain instruction from the first miss on. The tier
  A slots are compiled as absent, so the engine falls back to B.
- **v1.1 (Should):** tier A riddles fill in from `story.md` §7.1, and the escalation runs: a riddle on the first two
  clears with a miss, the instruction from the third. Players who like to puzzle keep the puzzle; players who are stuck
  get unstuck.
- Nothing ships as WIP text (4MI's EN debrief shipped "WIP WIP WIP", `r4mi/text.md` §4): the text compiler's release
  check fails on it (`tech.md` §11.5).

### 4.2 Predicate record format [new-code] S · Must

One record per meta stage (24 records × 24 B = 576 B, in meta's data bank):

| Byte | Contents |
|---|---|
| +0 | n = number of predicates (0-6) |
| +1..+18 | n × 3 bytes: `test`, `require`, `hint` |
| +19 | c = number of stage counters this stage uses (0-2) |
| +20..+21 | the counters' targets (§4.6) |
| +22..+23 | `HINT_BASE`: the stage's first string id in story's hint table (16-bit) |

**`test`** (high nibble = type, low nibble = argument):

| Type | Test passes when | Argument |
|---|---|---|
| `$0n` | SECRETS[m] bit n set | n = 0 exit, 1 room, 2 item, 3 plate (or the stage owner's meaning, §1.6) |
| `$1n` | best medal ≥ n | 1 bronze … 4 platinum |
| `$2n` | the last scorecard's row n is at its maximum | 0 TIME … 4 STYLE |
| `$3n` | RATEFLAGS bit n set (inverted for CHAMP_KO) | |
| `$4n` | stage counter n ≥ its target (§4.6) | n = 0-1 |
| `$FF` | — | end of list |

**`require`:**

| Value | Requirement | Tier |
|---|---|---|
| 0 | none | Must |
| 1 | POWER | Must |
| 2 | JET | Must |
| 3 | SUPER | Must |
| 4 | TAG | Should (no v1.0 stage uses it: without the partner every TAG room is a full-charge door, R4.2) |
| `$10+w` | weapon w owned (w = venue id 0-7; 8 = MAGNET BEAM) | Must |
| `$20+v` | venue v won | Must |

**v1.0's predicate table uses only `require` 2 (JET)**, for Yamato's E and Centaur's T plates (§4.3); the fortress
stages' values are none. The other codes stay in the engine (they cost nothing), but no v1.0 predicate names them, so
their requirement hints R1, R3 and R5 are Should (§4.5, `story.md` §7.3). The text compiler's release check fails if a
predicate names a requirement whose hint string is absent.

**`hint`**: the predicate's local hint index h. The text compiler emits, per stage, a table of 16-bit string ids from
`HINT_BASE`: entry 2h is tier A, entry 2h + 1 is tier B; `$0000` = absent. Story owns every string (R4.1). The engine
falls back only from A to B (§4.1), so the release check also fails if a predicate of a stage with a desk (every stage
but W3, §3.9) names a hint with no tier B string.

### 4.3 The venue predicate table [new-code + data] S · Must

**One rule for every stage: predicates run in descending `systems.md` SECRETS weight** (exit 3, room 2, item 2, plate 1;
`systems.md` §6.2), then **Gold**, then **Platinum**. So each hint points at the biggest gain still on the table. Room
comes before item on the tie, as both venue docs do. Both venue docs now follow this order (venues_a §0.2, venues_b
§0.9). The table is data, so a venue owner can still argue a reorder in its own row.

**Where plates sit:**

- In **Knight** (A) and **Tomahawk** (B) the plate sits in the secret boss room (`venues_a.md` §0.2), so it is set
  together with the exit and needs no predicate of its own.
- In **Yamato** (E) and **Centaur** (T) the plate is a separate JET-gated predicate (`venues_b.md`).
- Wind, Plant, Blizzard and Flame have no plate.

| Meta | Venue (R3.3 name) | Predicates, in order (test / require / hint id) |
|---|---|---|
| 1 | Blizzard: SUMMIT CLIMBER | `$00`/–/BL0 · `$01`/–/BL1 · `$02`/–/BL2 · `$13`/–/G · `$14`/–/G |
| 2 | Wind: SKY ACE | `$00`/–/WI0 · `$01`/–/WI1 · `$02`/–/WI2 · `$13` · `$14` |
| 3 | Plant: LOST JUNGLE | `$00`/–/PL0 · `$01`/–/PL1 · `$02`/–/PL2 · `$13` · `$14` |
| 4 | Flame: PERSIAN PALACE | `$00`/–/FL0 · `$01`/–/FL1 · `$02`/–/FL2 · `$13` · `$14` |
| 5 | Yamato: EDO NINJA ROW | `$00`/–/YA0 · `$01`/–/YA1 · `$02`/–/YA2 · `$03`/JET/YA3 · `$13` · `$14` |
| 6 | Tomahawk: HIGH NOON FRONTIER | `$00`/–/TO0 (plate B with it) · `$01`/–/TO1 · `$02`/–/TO2 · `$13` · `$14` |
| 7 | Knight: HERO'S QUEST | `$00`/–/KN0 (plate A with it) · `$01`/–/KN1 · `$02`/–/KN2 · `$13` · `$14` |
| 8 | Centaur: ATLANTIS RUINS | `$00`/–/CE0 · `$01`/–/CE1 · `$02`/–/CE2 · `$03`/JET/CE3 · `$13` · `$14` |
| 0, 9, 14, 16, 18, 20, 21 | Opening-lite, HALFTIME RIOT, H1, H3, H5, W2, W3 (W3 has no desk, §3.9) | the SECRETS bits each stage's owner defines in `fortress.md` §0.4 (b0 showpiece 3, b1 room 2, b2 prize 2; H5's b3, the Mr. X card, is scored by rating T14 and has no debrief predicate), by the same weight rule, then `$13`, `$14`. Their `require` values in v1.0 are none: the TAG rooms are full-charge doors (R4.2), and H4's SUPER-gated prize is Should |

**No venue secret exit, room or item needs an adaptor** (`venues_a.md` §0.3, `venues_b.md` §0.3, `systems.md` §2.4).
Only Yamato's E and Centaur's T plates need JET, as in vanilla. Knight's stairs can also be opened by vanilla's
charged-punch pillar, but they never require it. The adaptor-gated *extras* (Tomahawk's Energy Balancer room and sky
bypass, item pockets) are not predicates.

`G` is the generic scorecard hint, chosen by the **weakest row** of this run's scorecard (§4.5).

### 4.4 Hint ids (the words are `story.md` §7)

`story.md` owns every word (R4.1): §7.1 holds the final EN and JP text of both tiers for every id below, with tier B
taken verbatim from the venue docs (venues_a §1.5-§4.8, venues_b §1.14, §2.12, §3.14, §4.13) and fitted to 4 × 28.
This doc owns the ids, the order and which secret each id points at. Ids end in 0 for the exit (or showpiece), 1 for the
room, 2 for the item, 3 for the plate.

| Venue | Id | Secret | v1.0 (tier B) | Notes |
|---|---|---|---|---|
| Blizzard | BL0 / BL1 / BL2 | the condor / the no-wrap floor / SNOW CHAINS | Must | |
| Wind | WI0 / WI1 / WI2 | the ace's elevator / WEATHER BALLOON / YASHICHI | Must | |
| Plant | PL0 / PL1 / PL2 | follow the cat / TREETOP HUT / AUTO RECOVER (the explorer's perfect) | Must | tier A: PL0's riddle loses the explorer's name (R3.3) |
| Flame | FL0 / FL1 / FL2 | don't fight your shadow (the mirror glows, R3.9) / the mouse / FIREPROOF | Must | FL0's tier B is reworded for the glow (venues_b §2.12) |
| Yamato | YA0 / YA1 / YA2 / YA3 | **the draft** (the turning scroll; the sekisho is cut, R3.2) / the gold crest / DARUMA / plate E | Must | YA0's round-1 tier A riddle (the sekisho) is retired; its tier A is story's new draft riddle, YA0.A (§7.1, Should), and its tier B is venues_b §4.13's |
| Tomahawk | TO0 / TO1 / TO2 | the back way (+ plate B) / THE OUTHOUSE / SHERIFF STAR | Must | TO1 no longer names a game (venues_a) |
| Knight | KN0 / KN1 / KN2 | the stairs behind the empty throne (+ plate A) / LIGHT'S TABLET / KAISHIN | Must | |
| Centaur | CE0 / CE1 / CE2 / CE3 | ZONE 100 / ZONE 0 / CENTURION / plate T | Must | |
| Opening, Riot, H1, H3, H5, W2 | `OP`, `RI`, `H1`, `H3`, `H5`, `W2` + 0-2 (no stage here has a hinted b3: H5's card has no hint, `story.md` §7.2) | per `fortress.md` §0.4 | Must where the secret is in v1.0 | |
| W3 | `W3` + 0-2 | per `fortress.md` §0.4 | **Should** | W3 has no judges' desk in v1.0 (§3.9), so its three hints wait for a desk (`story.md` §7.2); its SECRETS bits are still set and scored silently (§3.9) |

Round 1's riddle and instruction text moved to `story.md` §7 (which already corrected four riddles' facts); the
round-1 draft is in git (commit `95288ee`).

### 4.5 Generic lines (ids; the words are `story.md` §7.3)

| Group | Ids | v1.0 |
|---|---|---|
| **Requirement hints** (the tool is missing; CX lesson 6) | R2 JET: the only one v1.0's predicate table uses (Yamato's E and Centaur's T plates, §4.2-§4.3) | Must |
| | R1 POWER, R3 SUPER, R5 weapon w (with the `%WEAPON%` variable): no v1.0 predicate needs them (H4's SUPER-gated prize and kin will) | Should (`story.md` §7.3) |
| | R4 TAG | Should (with the partner) |
| **Scorecard hints** (G), chosen by the weakest row as a fraction of its maximum; they must match `systems.md` §6.2's rules | G-TIME (with `%PAR%` and `%TIME%`), G-DAMAGE, G-VARIETY, G-SECRETS, G-STYLE | Must |
| **Perfect-venue lines** (rotate by the frame counter) | P1 | Must (one line) |
| | P2-P4 | Should (rotation) |

### 4.6 Stage counters: every "collect N" secret [new-code] S · Must

R1.10 and scope-16: one mechanism for every counted secret (Plant's treasures, Tomahawk's bounties, Wind's squadrons,
Centaur's three statues, the Riot's auditions, H1's score balls, …), so a new counter costs data, not code. R3.1 allows
**at most one collect-N secret per stage**.

- **Storage**: `STAGE_CNT[2]`, 2 of the 8 bytes tech's run block reserves for "meta's stage counters" (WORK `$6300`
  range, `tech.md` §3.4; the other 6 stay spare), cleared
  at stage start, kept through deaths in the same run (a CONTINUE starts a new run).
- **Writers**: a stage object increments counter n through `cnt_add(n)` (a C-window service in meta's code bank; 1 byte
  of `GP_ARG` names n). The HUD widget module shows it with a DIGITS or ICONROW widget (`tech.md` §7.13).
- **Readers**: one predicate routine, `pred_test(test)`, serves both the in-stage reward (the object that gives the
  chip or opens the door calls `pred_test($4n)` when Rock reaches it) and the debrief (§4.1). So the gate and its hint
  can never disagree.
- **Targets**: the stage's predicate record (§4.2, +20..+21). A CASUAL target (one step easier, R2.9) is a CASUAL
  poke on the record copy, or `TIERVAL` in the reward object (`systems.md` §13.4).
- When the counted secret is a SECRETS bit (the usual case: the behaviour item, b2), the reward sets the bit and the
  debrief tests `$02`; `$4n` is for stage-owner extras that have no bit of their own.

---

## 5. Medals and Hall of Fame points

### 5.1 Medals [new-code] S · Must (thresholds: `systems.md`)

The scorecard is out of 100 (`systems.md` §6, BRIEF §5.3). The medal comes from the **best** score ever on that meta
stage (STAGEREC +0):

| Medal | Best score | HoF points |
|---|---|---|
| — | 0-39 | 0 |
| BRONZE | 40-59 | 1 |
| SILVER | 60-79 | 2 |
| GOLD | 80-94 | 3 |
| PLATINUM | 95-100 | 4 |

The medal is never stored, only derived from the best score, so the thresholds can be retuned without breaking saves.

### 5.2 Hall of Fame points [new-code] S · Must

**HOF PTS = the sum of the medal points over the stages the build ships** (§1.8). The v1.0 maximum is 15 × 4 = **60**
(the full design's 22 stages give 88). The file card and the bracket's top bar show it.

HoF points are the currency of the global unlocks (§7). At every file commit, the system block's unlocks are re-checked
against that file's HoF points (unlocks never re-lock). Medal ribbons on the bracket frames show where the points are.

---

## 6. The championship rating (the Hero Score analogue)

### 6.1 v1.0 rows and tests [new-code] M · Must

R2.7 and scope-3 (decision 8): **the rating is re-derived so that 100 is reachable with v1.0 content**. T1 (the
partner) and T7 (the TURBO trap) exist only when the Could bundle and the tag partner ship; T3 (Exhibitions) is removed
in v1.0. Every test below reads Must content only (R0.4); the right-hand column names it.

The **CHAMPIONSHIP RATING** screen fills seven rows one by one, like 4MI's RESULT (`r4mi/modes.md` §1), during the
ending at the place story's order gives it (R4.1, step 8). Every point comes from one test in a single jump table, and
**the same table, in the same order, picks Break Man's debrief** (the first failed test).

| Test | Row | Points | Passes when | Must content it reads |
|---|---|---|---|---|
| — | **CHAMPIONSHIP** | 40 | constant: you won | W3 |
| T0 | TEAM | 5 | **Beat rebuilt**: all 4 plates (SECRETS b3 on meta 5, 6, 7, 8) | the 4 plate venues (`venues_a.md`, `venues_b.md`) |
| T1 | TEAM | 5 | **SOLO RIOT** (R4.2's partner-free test, R8.5): Bass β duel 1 won **without Break Man's capsule** (RATEFLAGS b4, set at the Riot clear when the capsule never dropped in that run; fortress's "NO-CAPSULE" bit is this bit) | the HALFTIME RIOT's NPC Break Man beat: the whistle and the life capsule when Rock's HP falls below 6 in the pinch (`fortress.md` §2.4) |
| T2 | ROUTE | 1 each, 8 max | secret exits found (SECRETS b0, meta 1-8); the test passes at 8/8 | the 8 venues' secret exits |
| T4 | ROUTE | **4** | all 8 venue hidden rooms (SECRETS b1, meta 1-8) | the 8 hidden rooms, Flame's mouse room included (Must, R0.4) |
| T5 | ROUTE | **4** | all 8 venue behaviour chips (CHIPS_OWNED bits 6-13) | the 8 venue chips (R2.5) |
| T6 | GEAR | **2 each**, 10 max | Eddie's chips owned (`systems.md` source "shop": bits 1-5); the test passes at 5/5 | the v1.0 shop (740 bolts in all; `systems.md` §7 puts a typical player's v1.0 income at ≈ 1,905) |
| T8 | MEDALS | 5 | GOLD or better on all 8 venues | the venues |
| T9 | MEDALS | 4 | at least 3 PLATINUMs (any stages) | any stage |
| T10 | FAIR PLAY | 4 | GAMEOVERS = 0 | |
| T11 | FAIR PLAY | 4 | CHAMP_TIME < 648,000 frames (3:00:00) **(tune at M9** with v1.0's 15 stages) | |
| T12 | FAIR PLAY | 2 | UNPLUGS = 0 (§1.7) | the unplug count (Must) |
| T13 | BONUS | 2 | **RIVAL**: Bass β duel 1 won with no damage from the bar fill to the overdrive (RATEFLAGS b2; `fortress.md` §2.4) | the Riot |
| T14 | BONUS | 2 | **MR. X'S CARD** (RATEFLAGS b1; H5's hidden room, `fortress.md` §4.5.3) | H5 and its card (Must, §15) |
| T15 | BONUS | 1 | **TOP SEED**: never KO'd in a champion's boss room (CHAMP_KO clear) | |
| T16 | — | — | sentinel: always fails → the "perfect" debrief | |

Row maxima: CHAMPIONSHIP 40 + TEAM 10 + ROUTE 16 + GEAR 10 + MEDALS 9 + FAIR PLAY 10 + BONUS 5 = **100**, and every point
is reachable on one v1.0 file. The readme prints the sum.

**Fallbacks**, so the table never depends on content a build lacks (R0.4): if `fortress.md` cannot keep the Riot's
capsule beat in v1.0, T1 becomes "the HALFTIME RIOT won with no E-tank used"; if the Mr. X card is not in a v1.0 room,
T14 becomes "every hidden room of the v1.0 non-venue stages". Both are one-line changes in the test table.

**Rank titles** under the number (words: `story.md` S46):

| Rating | Title |
|---|---|
| 100 | GRAND CHAMPION |
| 90-99 | CHAMPION |
| 80-89 | FINALIST |
| 70-79 | SEMIFINALIST |
| 55-69 | QUARTERFINALIST |
| < 55 | PARTICIPANT, with a participation-ribbon sprite |

**Asterisks.** An EDITED file reads `RESULT UNDER REVIEW *` and grants no achievement (§10). With the bundle, a doped
file prints its number with `*` (§6.3).

**When it is computed.** At every championship win: a cleared file can replay W3 and see the ending again (START skips
each scene page). BEST_RATING keeps the maximum. T11 always uses CHAMP_TIME, the time of the *first* win. The screen's
background in v1.0 is the judges' desk; fortress's PHOTO FINISH still joins with the victory lap (Could).

### 6.2 Break Man's debrief [new-code + text] S · Must

After the rating, Break Man (4MI's Proto Man pattern; BRIEF §2) speaks: one greeting, then the entry for the **first
failed test**, then his close and `TO BE CONTINUED` (vanilla's last line, kept on purpose). On the first clear only,
`(SPECIAL EVENTS ARE NOW OPEN)` follows. The NPC Break Man is Must (R4.2); in v1.0 he speaks through his 16×16 face icon
and name label (R5.1).

`story.md` S47 owns every word. This doc owns the entries, one per test, and their order:

| Entry | Shown when | v1.0 |
|---|---|---|
| greeting | always | Must |
| T0 Beat | T0 failed | Must |
| T1 SOLO RIOT | T1 failed (v1.0: "you needed help against Bass") | Must (new: story writes it) |
| T2 exits | T2 failed (`%N%` = exits found) | Must |
| T4 rooms, T5 chips, T6 gear, T8 gold, T9 platinum, T10 game overs (`%N%`), T11 time (`%H%:%MM%`), T12 unplugs (`%N%`), T13 rival, T14 card, T15 top seed | that test failed | Must |
| perfect | every test passed | Must |
| T1 partner: never called / doped; T3 exhibitions | with the bundle and the partner; with the Exhibitions | Should / Could |
| perfect (ENGRISH) | LANGUAGE = ENGRISH: story's S47.PE, a nod to 4MI's line (`r4mi/text.md` §4 entry 15) **in new words**, never the quote (R8.4) | Could |

Story S47's T1 "never called" line must point at the pause menu's **CALL row confirmed with A** (R2.10), not at SELECT.

### 6.3 With the bundle: the partner and the TURBO trap [new-code] S · Could (cut-line 9, with the partner)

`systems.md` §9.4 owns the doping trade-off (SYS-CHP-4); this doc only scores it. When the bundle and the tag partner
ship together (R2.5):

- **T1 becomes PARTNER** (5): Break Man called in at least 3 different stages (TAG_STAGES ≥ 3 bits) **and** he has not
  refused you (RATEFLAGS.DOPED clear). SOLO RIOT stays recorded but scores nothing.
- **T6 becomes** 1 per Eddie chip (shop 5 + garage 3: IRON HELMET, THERMOS, BIRD SEED) + 2 for the TANK RACK, 10 max.
- **T7 TURBO** (+2, GEAR): Y-TURBO owned. **The trap.** It is bonus-shaped: the debrief skips it (a hint that says "go
  and dope" would be wrong), so in the jump table it returns "passed" for the debrief and adds its 2 points to the row.

**The arithmetic hides a trade-off**, as 4MI's does (`r4mi/modes.md` §1.2). The row maxima are 40 + 10 + 16 + 12 + 9 +
10 + 5 = **102**, but the readme says 100. TURBO's +2 costs Break Man's 5 (T1) and the PART it is bought with breaks one
garage pair (−1 or −2 in GEAR):

- **With TURBO**, the most you can score is 96.
- **Without it**, exactly 100.

The off-by-two between the printed rows and the readme is a clue players can solve, as 4MI's was.

What doping does to the meta layer (R2.8, design-8):

- It sets RATEFLAGS.DOPED (b0) and plays bracket event EVENTS2 b5, **BREAK MAN WALKS** (story S21): like 4MI's Eddie,
  the cost is shown, not explained.
- **No secret is lost**: TAG-gated secrets use their full-charge-door fallbacks on a doped file (R2.8; this replaces
  consistency-38's "TAG secrets void" note). `systems.md`'s OWNED drops BREAK.
- In RECORDS and on the file card, a `*` follows the rating and the TOTALS page reads `TURBO: YES`; medals earned with
  Y-TURBO equipped carry STAGEREC's asterisk bit; the CAPCOM TIMES headline changes (story).
- The judges never mention it. Break Man does (T1's doped entry).

**1993 RULES** (Could, cut-line 10): chips and the shop are off on a 1993 file, so T5 and T6 cannot pass. On a
RULES = 1993 file the GEAR row and T5's 4 points are replaced by a constant **1993 ROW** of 14 ("won under 1993 rules"),
which keeps the maximum at 100.

**Bass Mode** (Won't, v1): TEAM is re-labelled SOLO and passes automatically; the full round-1 treatment is in git (commit
`95288ee`, §9.7).

### 6.4 Data [new-code] S · Must

- **Test table:** 17 entries × 4 bytes `{routine lo, routine hi, points, row}`; v1.0 compiles T1 = SOLO RIOT and leaves
  T3 and T7 as "absent" entries (0 points, never failed). The bundle build swaps T1's routine, T6's points rule, and
  T7's points in by a build flag (`BUNDLE = 1`); a unit test asserts the row maxima sum to 100 (v1.0) or 102 (bundle).
- **Row sums:** stored in LAST_ROWS, the total in LAST_RATING, the maximum in BEST_RATING.
- **Debrief index:** first failed test + 1, as 4MI does at `$4D:$9BDB`.

---

## 7. The unlock chain [new-code] S · Must (the v1.0 bits)

All unlocks are **global** (system block `$010`, one bit each; consistency decision 34: global is simpler and kinder).
Any file can earn them, and they never re-lock. The SPECIAL EVENTS menu reveals its items word by word as the bits
arrive (4MI `$4C:$811A`). Locked items show as `??? ???` with a one-line condition (4MI lesson: be exact, and show it).
Files played on 1993 RULES earn unlocks as normal (decision 34).

| Step | You do | You get (bit) | Tier |
|---|---|---|---|
| 1 | Reach **20 HoF points** on any file (possible mid-game) | SPECIAL EVENTS on the title, with RECORDS (U0.0, U0.2) | Must |
| 2 | **Win the championship** | **EXTRA CONFIG** (U1.1) | Must |
| 2 | **Win the championship** | TIME ATTACK (U0.4) | Should |
| 2 | **Win the championship** | GP RUSH: OPEN BRACKET (U0.5) | Could |
| 3 | Clear the **OPEN BRACKET** | GP RUSH: the 9 ONE-WEAPON CUPS and ALL-STAR (U0.7) | Could |
| 4 | Clear **any one cup** | MY GP (U1.0), TRUE GP (U1.2) | Could |
| 5 | Clear **TRUE GP** | the `???` fight's name is revealed (U1.4) | Could |
| — | (round 1: 20 HoF → MUSEUM; 40 HoF → EXHIBITION RULES; championship → ENTRANT: BASS β; OPEN → KNOCKOUT; TRUE GP → the VAULT; all Gold + the card → MR. X RETURNS; every DEV time → the DEV ROOM) | U0.1, U0.3, U0.6, U1.3, U1.5, U1.6, U1.7 | Won't (v1); the bits stay reserved |

EXTRA CONFIG is Must as a **dev tool** (BRIEF §7.3). In DEV builds (`DEV = 1`) every unlock bit reads as set, and EXTRA
CONFIG opens from the title with pad 1 SELECT + START held and from the pause menu's `TEST` row (§9.6). In release
builds it unlocks with the championship: round 1's "clear any cup" depended on GP Rush, which is Could (R0.4).
**R8.8 keeps these unlock points** (RECORDS at 20 HoF points, EXTRA CONFIG at the championship) as the defaults; the
user may change them.

**System block unlock bits** (`$010-$017`):

| Byte.bit | Unlock | Byte.bit | Unlock |
|---|---|---|---|
| U0.0 | SPECIAL EVENTS menu | U1.0 | MY GP (Could) |
| U0.1 | MUSEUM (Won't) | U1.1 | **EXTRA CONFIG** |
| U0.2 | **RECORDS** | U1.2 | TRUE GP (Could) |
| U0.3 | EXHIBITION RULES (Won't) | U1.3 | KNOCKOUT format (Won't) |
| U0.4 | TIME ATTACK (Should) | U1.4 | `???` name revealed (Could) |
| U0.5 | GP RUSH: OPEN (Could) | U1.5 | MR. X RETURNS (Won't) |
| U0.6 | ENTRANT: BASS β (Won't) | U1.6 | MUSEUM VAULT (Won't) |
| U0.7 | GP RUSH: CUPS + ALL-STAR (Could) | U1.7 | MUSEUM DEV ROOM (Won't) |
| U2-U7 | reserved | | |

---

## 8. SYSTEM block layout (1 KB) [new-code] S · Must

Every v1.1+ record is allocated now (§1.4: the layout freezes at v1.0).

| Offset | Size | Field | Notes | Tier |
|---|---|---|---|---|
| `$000` | 4 | magic `'R' '6' 'S' 'Y'` | | Must |
| `$004` | 1 | layout version | 1 at v1.0 | Must |
| `$005` | 1 | SYSFLAGS | b0 INITIALISED; b1 a DEV build has written this block (release builds show `DEV SAVE` on the title) | Must |
| `$006` | 2 | generation | | Must |
| `$008` | 1 | LANGUAGE | 0 JAPANESE, 1 ENGLISH, 2 ENGRISH (Could) | Must |
| `$009` | 1 | DISPLAY | b0-1 ANNOUNCER (0 ON, 1 DEATHS ONLY, 2 OFF); b2 **FLASHES REDUCED**; b3 HUD TIMER (Should); b4-5 TEXT SPEED (0 NORMAL, 1 FAST, 2 INSTANT, 3 SLOW); b6 SCREEN SHAKE OFF; b7 reserved | Must |
| `$00A` | 1 | AUDIO | b0 MMC5 AUDIO OFF; b1 MMC5 ARRANGEMENTS (both Could, with the MMC5 pulse driver; MMC5 AUDIO defaults to ON, consistency decision 36); b2-7 reserved | Could |
| `$00B` | 1 | CONTROLS | b0-1 SELECT SWAP (0 FULL, 1 WEAPONS ONLY, 2 OFF); b2 2P SHIFT OFF (Should); b3 A/B SWAP; b4-7 reserved | Must |
| `$00C` | 1 | **INPUT LAG** | b0-2: 0-6 frames, default 0, added to every reflex window (R3.5, `systems.md` §1.6); b3-7 reserved | Must |
| `$00D` | 3 | reserved config | | |
| `$010` | 8 | UNLOCKS | §7 | Must |
| `$018` | 2 | ACHIEVEMENTS | §10 | Could |
| `$01A` | 2 | ACH_NEW | shows NEW! until RECORDS has shown it | Could |
| `$01C` | 4 | reserved | | |
| `$020` | 3 | CLEARED_ANY | 24 bits by meta index: cleared on any file (feeds the Time Attack list) | Must |
| `$023` | 3 | ENTERED_ANY | entered on any file (otherwise the lists show `???`) | Must |
| `$026` | 1 | BEST_RATING_EVER | unedited files only | Must |
| `$027` | 1 | reserved | | |
| `$028` | 120 | LIFE_STAGE[24] × 5 | lifetime KOs (16-bit) + time (24-bit, 256-frame units) | Must |
| `$0A0` | 32 | LIFE_TOTALS | play (32-bit, 256-frame units), KOs (24), game overs (16), unplugs (16), boots (16), championships (16), bolts earned (32), weakness hits (24), tag calls (16), reserved | Must |
| `$0C0` | 264 | TA_REC[24] × 11 | best time (24-bit frames) + 4 checkpoint splits of that run (16-bit frames from the start) | Should |
| `$1C8` | 72 | TA_BASS[24] × 3 | Bass Mode best times | Won't (reserved) |
| `$210` | 96 | RUSH_REC[16] × 6 | per course: best time (24-bit frames), tries (16-bit), clears (8-bit) | Could |
| `$270` | 18 | KO_REC[3] × 6 | KNOCKOUT 8 / 16 / 32 | Won't (reserved) |
| `$282` | 72 | MYGP[3] × 24 | saved MY GP setups (§9.2.5) | Could |
| `$2CA` | 48 | RULES_BOOK[24] × 2 | the Exhibition Rules sticker book | Won't (reserved) |
| `$2FA` | 16 | HEARD | 128 bits: tracks heard (the Museum's sound test) | Won't (reserved) |
| `$30A` | 8 | PLAQUES | 64 bits: plaques read (the Museum's gallery) | Won't (reserved) |
| `$312` | 6 | WEAK_SEEN | 48 bits by fight id: weakness landed at least once | Could (achievements) |
| `$318` | 6 | FIGHT_SEEN | 48 bits by fight id: reached (EXTRA CONFIG's FIGHT list and the GP Rush lobby show `???` otherwise) | Must |
| `$31E` | 16 | VENUE_REC[8] × 2 | one lifetime mini-record per venue, by venue id (§9.4) | Must (per venue as listed there) |
| `$32E` | 194 | reserved | | |
| `$3F0` | 16 | trailer | §1.3 | Must |

---

## 9. RULESET, the fight table, RECORDS, EXTRA CONFIG and the post-game modes

**SPECIAL EVENTS** is a list on the title (vanilla font) that grows with the unlocks (§7):

| Item | Section | Tier |
|---|---|---|
| RECORDS | §9.4 | Must |
| EXTRA CONFIG | §9.6 | Must |
| TIME ATTACK | §9.1 | Should |
| GP RUSH | §9.2 | Could |
| (achievement plates, a strip under the list) | §10 | Could |
| EXHIBITION RULES, MUSEUM, MR. X RETURNS | §9.3, §9.5, §9.8 | Won't (v1) |

### 9.0 RULESET: one choke point [new-code] S · Must

4MI lesson: modes override config through one set of globals (`r4mi/modes.md` §5). At every stage start (and at every
fight-loader warp) the 16-byte **RULESET** in WORK (`$6270-$627F`, owner meta, `tech.md` §3.4) is filled from exactly
one source, then the engine reads only RULESET:

| Mode (`RS_MODE`) | Source | Tier |
|---|---|---|
| 0 main game | the file's DIFF bytes (§1.6) and the global INPUT LAG | Must |
| 3 EXTRA CONFIG scratch | the scratch file's DIFF, then the CHEATS group ORed in | Must |
| 4 mailbox test | the mailbox's source file, then its overrides (§9.6) | Must |
| 5 fight-loader bout | the current mode's ruleset, then the fight record's flags and pinch byte (§9.2.1) | Must |
| 1 Time Attack | the TA preset (§9.1) | Should |
| 2 GP Rush | the course setup (§9.2.4) | Could |

| Byte | Name | Contents |
|---|---|---|
| +0 | `RS_DIFF` | DIFF A's format (§1.6): DAMAGE, DROPS, **CASUAL**, GUARDS, **HARD**, RULES 1993. `IFHARD`, `IFCASUAL`, `IF1993` and tech's `LAYOUT_TIER` read this byte (`tech.md` §5.5) |
| +1 | `RS_LIVES` | b0-3 lives at start and continue; b4 ONE_LIFE (a death ends the run); b5 LIVES LOCK (cheat) |
| +2 | `RS_TANKS` | b0-2 E-TANK FLOOR; b4-7 E-tanks given at start (TA, Rush) |
| +3 | `RS_REFILL` | b0-1 REFILL on respawn; b2 refill at pause (Rush cups, cheat); b3 checkpoints off (reserved) |
| +4 | `RS_WPN` | allowed weapons by venue id (`$FF` all) |
| +5 | `RS_WPN2` | b0 buster; b1 M.BEAM; b2 POWER; b3 JET; b4 SUPER; b5 TAG; b6 chips on; b7 Beat rescue |
| +6 | `RS_MAXHP` | max HP (vanilla's full bar by default) |
| +7 | `RS_ICAP` | i-frame cap (0 = none; Rush cups 30) |
| +8/+9 | `RS_RULES` | the Exhibition Rules mask: always 0 in v1 (Won't) |
| +10 | `RS_CHEAT` | b0 GOD; b1 BOSS HP 1; b2 RNG LOCK; b3 REFILL AT PAUSE; b7 any cheat used (records off) |
| +11 | `RS_MODE` | the mode number above |
| +12 | `RS_HUD` | b0 timer shown (Should) |
| +13 | `RS_LAG` | INPUT LAG 0-6, copied from the system block, read by `systems.md`'s `REFLEX` macro |
| +14 | `RS_FLAGS` | b0 NO_SAVE (no commit, §1.4); b1 NO_RECORDS (no records, achievements or BEST_RATING_EVER); b2 NO_DESK (no judges' desk) |
| +15 | `RS_PINCH` | the boss's pinch threshold in HP; 0 = the boss's own default (0 in every mode but 5; mode 5 copies the fight record's +10, §9.2.1). The venue bosses' pinch tests read it (W2's SUPER copies: 14) |

`systems.md` and `tech.md` read the same block. The bit names come from the generated `src/gp/bits.inc` (§1.6).

### 9.1 TIME ATTACK [new-code] M · Should (cut-line item 7)

- **List:** every meta stage cleared on any file (CLEARED_ANY) among the stages the build ships, plus the victory lap
  (meta 23) once it exists. Each row shows `RECORD m:ss.cc` and `DEV m:ss.cc`; a ★ means the record beats the DEV time.
- **Regulation loadout** (fixed, so records compare; 4MI's TA fixes its loadout too, `r4mi/modes.md` §2):
  - the buster and all 8 weapons, full; M.BEAM from H1 on (meta 14+);
  - forms: none in the Opening (meta 0), POWER + JET everywhere else, and SUPER after H3 (meta 17-21). A venue's TA
    therefore allows its adaptor-gated routes, and every record is set with the same tools;
  - no chips, no tag partner (consistency decision 34), 0 E-tanks, one life, full HP;
  - NORMAL rules, drops NONE (`systems.md`: records modes have no dice; criticals no longer exist).
- **Story state:** STORY_BEAT and FORMS are preset per stage from a 24-entry table, as 4MI presets PROG per fortress
  stage.
- **Entry and return:** the stage is entered through tech's fight-loader path with a stage target instead of a fight
  record, and **return kind 6 (TA list)**, ONE_LIFE and NO_SAVE set (a request to `tech.md` §4.6; Should). The clear and
  death paths return to the list; no YOU GET, flags, desk or autosave run.
- **Timer:** from the first frame of control after READY to the frame the boss's bar empties (for the lap, to the last
  name), shown as a HUD widget (DIGITS with tenths, `tech.md` §7.13) when CONFIG's HUD TIMER is on (always in TA). At
  each checkpoint a split pops up for 60 frames: `+0:01.23` (red) or `-0:00.40` (green) against the record run's split.
- **Pause menu:** RETRY (restart the stage at once) and `EXIT` (the pause font has no Q, consistency-23).
- **Result:** `TIME 1:23.45` under `RECORD`, and `NEW RECORD!!` (which 4MI's TA lacks). The system block commits.
- **DEV times:** a 24-entry ROM table, filled from the developers' golden-movie runs (§9.6).

### 9.2 GP RUSH: a boss rush on one fight table [new-code] M · Could (cut-line item 11); the fight table Must

The design copies two proven things:

- **Vanilla Wily 3's data-driven rush** (`rm6/fortress.md` §7): a hub screen; one room per boss at `$09 + id`; tables
  `$39:$8EC8` (X), `$8ED2` (boss stage id) and `$8EDC` (alcove metatiles); palette `$9A + id`; a big life capsule that
  returns you to the hub; alcoves closed through the `$0340` bitfield; a ninth teleporter after the eighth win.
- **4MI's arena family** (`r4mi/modes.md` §3): one 45-entry fight table with block markers; a 6-byte fight bitmask and
  seven presets of about 19 bytes; a list builder (`$4C:$9762`) that keeps table order, plus four shufflers; a runner
  whose step counter makes even steps lobbies and odd steps fights; one lobby with a NEXT / LEFT panel, gift bits and an
  exit; 24-bit frame-count records.

#### 9.2.1 The fight table and the fight-loader interface [data] S · Must

R1.7 (scope-6, scope decision 12): **the fight loader is Must and `tech.md`'s** (§4.6 there: `fight_load`, `FIGHT_CTX`,
the 64-byte return-to snapshot, the stale-bit clear). **This doc owns the fight table** (ids, records, run order) and
the calls it makes. In v1.0 the table serves W2's pair bouts (`fortress.md`), EXTRA CONFIG's `FIGHT n` and the test
mailbox's fight command; GP Rush (Could), Time Attack (Should) and Doc Robot MK-VI (Should) use it later.

**Fight ids** are fixed by type (consistency-44, fortress §9.3). The ids and arenas are assigned now for all of them; a
record is **Must** when a v1.0 caller needs it (W2's bouts, the tests of every v1.0 boss), and the mid-boss records,
which only GP Rush needs, are Could (the venue docs list their arenas "for GP Rush when it ships"). A separate **run order** list sets GP Rush's play order
and shuffle blocks (bit 7 marks a block start, as at 4MI `$4C:$97A3`).

| Ids | Fights | Arena (stage, screen) | Tier of the record |
|---|---|---|---|
| `$00-$07` | the 8 champions, venue id order | each venue's boss room | Must (W2, tests) |
| `$08` | AYACO | Wind, 01 (the sortie) | Could (with GP Rush) |
| `$09` | METAL METSLIME | Knight, 12 | Could |
| `$0A` | DOMINGO DOME | Tomahawk, 05 | Could |
| `$0B` | SIX-SHOT SAM | Tomahawk, 0D | Could |
| `$0C` | SIDEWINDER | Tomahawk, 10-11 | Could |
| `$0D` | CONGA | Plant, 08 | Could |
| `$0E` | SHADOW ROCK | Flame (venues_b) | Could |
| `$0F` | GAMARN & GAMADAYU | Yamato (venues_b) | Could |
| `$10` | DARUMA | Yamato (venues_b) | Could |
| `$11-$12` | spare (venues) | | |
| `$13` | Big Eye MK-VI (`fortress.md` §9.3 assigns `$13-$17`) | H1 | Could (with GP Rush) |
| `$14` | Picopico-kun MK-VI (H2 is Should) | H2 | Could |
| `$15` | **KAMEGORO MAKER MK-VI**, H3's mid-boss (a re-skinned vanilla dispenser, R3.6; round 1 had Doc Robot here) | H3 | Could |
| `$16` | Enker MK-VI (W1 is Could) | W1 | Could |
| `$17` | the Trophy Dispenser | W3 | Could |
| `$18-$1B` | Exhibition guests E1-E4 | E1-E4 | Could (E4 Won't) |
| `$1C-$20` | Hall of Fame MK-VI bosses H1-H5 (Yellow Devil, Mecha Dragon, Gamma, Cossack Catcher, Dark Man) | H1-H5 | `$1C`, `$1E`, `$20` Must; `$1D`, `$1F` Should |
| `$21` | Bass β, duel 1 (HALFTIME RIOT) | `$11` | Must |
| `$22` | METALL 16 (the W1 boss, R3.6) | W1 | Could |
| `$23` | Bass β, duel 2 (Castle) | W2 | Must |
| `$24` | WILY MACHINE 6.5 (R3.6) | W3 | Must |
| `$25` | the Wily Capsule SUPER | W3 | Must |
| `$26` | Grand Pi-kun (Opening-lite, one size) | `$10` | Must |
| `$27` | **`???`**: vanilla Wily 4's whole final fight, untouched: engine id `$0F`, room 06, under RULESET 1993 (feasibility-2, consistency decision 40) | legacy `$0F` | Could (with GP Rush) |
| `$28` | Mr. X | Mr. X Returns | Won't |
| `$29` | **Doc Robot MK-VI** (the AIR MAN copy; H3's workshop room, entered through `FIGHT_CTX` return kind 5) | H3 (a small arena, `fortress.md` §4.3) | Should |
| `$2A-$2F` | spare | | |

W2's SUPER copies use the champions' own records `$00-$07` (`fortress.md` §5.2.2): the SUPER palette is the record's +5
and the raised pinch is its +10, so they need no ids of their own.

**Fight record, 11 bytes** (the format tech's `fight_load` reads):

| Byte | Contents |
|---|---|
| +0 | engine stage id (`tech.md` §4.2) |
| +1 | room screen (→ `$0684`) |
| +2 / +3 | spawn x / y (slot 0) |
| +4 | room CHR set (→ `$0685`) |
| +5 | palette (→ `$0686`) |
| +6 | music |
| +7 | face icon id (R5.1; a portrait id when portraits ship) |
| +8 | name text id (story's string; the `???` gag swaps it, below) |
| +9 | flags: b0 needs JET; b1 needs POWER; b2 BG boss; b3 multi-part; b4 SECRET name; **b5 RULES_1993** (the bout runs with `RS_DIFF` b7 forced on: fight `$27`); b6-7 reserved |
| +10 | **PINCH**: the boss's pinch threshold in HP, copied to RULESET's `RS_PINCH` (§9.0); 0 = the boss's own default. W2's SUPER copies (`$00-$07`) pinch at **14** instead of 9 (`fortress.md` §5.2.2); both venue docs' bosses read it. Every other v1.0 record holds 0 |

Round 1's three "block" bits in +9 are dropped: the run-order list already marks the blocks, and b5 is needed for the
1993 bout. Round 3 adds +10 (fortress's request): the pinch value needs a whole byte, and flags b6-7 stay free. The
table is 48 records × 11 B = 528 B of meta's data bank.

**The interface** (what meta calls, what it reads back; tech implements):

| Caller | Call | Return kind (`FIGHT_CTX` b0-2) | Meta reads afterwards | Tier |
|---|---|---|---|---|
| W2's hub (fortress's mechanic) | `fight_load(id, HUB)` | 1 hub | — (the hub reads `FIGHT_RESULT`, WORK `$6262`, and closes its alcove) | Must |
| EXTRA CONFIG `FIGHT n` | `fight_load(n, XCONFIG)` | 3 | `FIGHT_RESULT` → `WIN` / `LOSS` on the EXTRA CONFIG screen | Must (M7) |
| the mailbox, command 2 | `fight_load(+17, TEST)` (tech's RESET code) | 4 | the test reads `FIGHT_RESULT` from WORK | Must (M7) |
| GP Rush runner | `fight_load(list[step/2], LOBBY)` with ONE_LIFE when lives run out | 2 | `FIGHT_RESULT`, time | Could |
| Time Attack | the stage-target variant (§9.1) | 6 (requested) | the timer | Should |
| H3's Doc Robot workshop (fortress's mechanic) | `fight_load($29, H3ROOM)` | 5 | — (the room reads `FIGHT_RESULT`) | Should |

- `fight_load` fills RULESET (§9.0) with `RS_MODE = 5` from the caller's ruleset and the record's flags: b5 forces 1993
  rules; `RS_FLAGS` gets NO_SAVE and NO_DESK; `RS_PINCH` gets the record's +10; legacy ids keep vanilla fortress rules unless the record overrides them
  (consistency decision 37).
- A bout is not a stage clear: no YOU GET, no `FLAGIDX`, no SECRETS, no STAGEREC, no autosave, no desk (`tech.md`
  §4.6). In W2 the bouts are part of W2's own run: the scorecard counts them, and W2's clear is the one that saves and
  goes to the desk (a request to `systems.md`: the run block is not reset by a fight warp).
- `FIGHT_SEEN` (SYS `$318`) gets the fight's bit when the bout starts; `WEAK_SEEN` (Could) when its first weakness lands.

**The `???` gag** (Could, a running gag on Mr. Y). Until U1.4, the lobby panel names fight `$27` **`MR. Y'S ???`**; after
the TRUE GP clear, `DR. WILY (OBVIOUSLY)` (story's words). This is 4MI's `???` → COCKROACH OMEGA trick (`r4mi/modes.md`
§3.6), at the cost of one byte test.

#### 9.2.2 The lobby: "PLAYERS' TUNNEL" [new-code] S · Could, [new-art] S · Could

**Screen `$1D` of the Opening's layout**, on TS_STADIUM, entered by the warp to stage `$10` screen `$1D` (`tech.md`
§4.2, consistency-31): it has no stage id and no tileset slot of its own (art_audio's dedicated slot is dropped). It needs
a tunnel interior, a scoreboard and a gate of light at the right. The Opening's layout owner (`fortress.md`) places it.

**The scoreboard** (text window) reads `NEXT LEFT 16`, then the face icon and the name.

**Gifts**, one per GIFTS bit: b0 **Eddie** (touch him for a random item: 1UP / E-tank / big life / big weapon energy);
b1-b2 **Roll's** HP refills, left and right; b3 **Beat** refills every weapon; b4 **Break Man** recharges the tag call
(with the partner).

**Exit:** stand in the gate and press UP (`IFINTERACT`, `systems.md` §1.6). The camera flashes (through tech's
rate-limited flash service) and `ROUND n` is announced. START in the lobby opens the normal pause menu, for weapon and
chip choices.

#### 9.2.3 The runner [new-code] S · Could

```
step = 0; list = build(mask, run_order, shuffle)       ; 4MI $4C:$9762, shufflers at $97DB
loop: if step even: if GIFTS == 0 → heal HEAL HP, step++  else → LOBBY until gate
      if step odd : fight_load(list[step/2], LOBBY); on FIGHT_RESULT = WIN → step++
      on LOSS: lives-- ; lives < 0 → ELIMINATED screen
      step/2 == count → CHAMPION screen
```

The runner's state (≈ 64 B: the list, step, lives, timer) takes a range from WORK's free 1,280 B through the registry
(`tech.md` §3.4; feasibility-12). **ELIMINATED** (`ELIMINATED IN ROUND 5 / BY PLANT MAN`, tournament language, with the
time and the round record) and **CHAMPION** (the time, `NEW RECORD!!`, the unlocks of §7) are one screen each.

#### 9.2.4 Courses (presets) [data] S · Could

Each course is a 24-byte setup in ROM, in the MY GP format (§9.2.5). Course n saves to RUSH_REC[n]. Every course runs
with drops NONE (`systems.md`: records modes have no dice).

| # | Course | Fights | Weapons | Gifts | Tanks | Other |
|---|---|---|---|---|---|---|
| 0 | **OPEN BRACKET** | the 8 champions, shuffled | all + forms | all | 4 E | one life |
| 1-9 | **ONE-WEAPON CUPS**: BUSTER CUP, then Y.SPEAR … C.FLASH CUP | the 8 champions | that weapon only (+ forms; only the BUSTER CUP has the buster, as 4MI's SUPPIN) | none; HEAL 5 | 9 E | refill at pause; i-frame cap 30 (4MI's SHORT INV) |
| 10 | **ALL-STAR** | every non-secret fight the build ships, shuffle 3 (within blocks) | all + forms | all | 4 E | one life |
| 11 | **TRUE GP**: "THE GREATEST GRAND PRIX IN HISTORY" | **all**, secrets included, shuffle 3, finale fixed | all | all | 9 E | HARD, one life |
| 12 | **MY GP** | user | user | user | user | user |
| 13 | **1993 CUP** | the 8 champions in vanilla Wily 3 hub order, in the legacy rooms (ids `$08-$0F`) | vanilla weapons, no forms | none | 0 | 1993 rules: the nostalgia course (with 1993 RULES) |
| 14-15 | reserved | | | | | |

Weapon cups never need to drop fights, unlike 4MI's three "(15 STAGES)" courses: under BRIEF §5.1 every weapon does 1-4
to every boss.

#### 9.2.5 MY GP: the bracket editor [new-code] S · Could

A bit-grid editor over a 24-byte setup, 4MI's MY ARENA (`r4mi/modes.md` §3.5):

| Byte | Field | Format |
|---|---|---|
| +0..+5 | FIGHTS | 48-bit mask by fight id (they always run in run order, shuffled by SHUFFLE) |
| +6 | WEAPONS A | b0-7 = the 8 champion weapons by venue id |
| +7 | WEAPONS B | b0 BUSTER; b1 POWER; b2 JET; b3 SUPER; b4 TAG (Break Man); b5 M.BEAM; b6 BEAT RESCUE (`systems.md` §10); b7 reserved |
| +8 | GIFTS | lobby bits (§9.2.2); 0 = no lobby |
| +9 | SHUFFLE | 0 fixed, 1 all, 2 all but the finale block, 3 within blocks |
| +10 | TANKS | low nibble E-tanks 0-9, high nibble W-tanks |
| +11 | HEAL | HP restored between fights when there is no lobby |
| +12 | LIVES | 0-9 (0 = one life) |
| +13 | DIFF | b0 HARD; b1 reserved; b2-3 DAMAGE; b4 SHORT I-FRAMES (cap 30); b5 REFILL AT PAUSE; b6 CHIPS ON; b7 reserved |
| +14..+15 | RULES | the Exhibition Rules mask (Won't: always 0) |
| +16..+18 | CHIPS | the chip set used when CHIPS ON (24 bits, `systems.md` §9.2 order); slot limits are ignored here |
| +19 | reserved | |
| +20 | ORIGIN | the preset it was loaded from |
| +21..+23 | reserved | |

- **Commands:** EDIT, LOAD PRESET ◀▶, SAVE / LOAD (3 slots in the system block), START.
- **Field help:** one help line per field, from the same help-string engine as EXTRA CONFIG.
- **A one-fight MY GP is a boss select**, which is also how 4MI's scout built its 45 `fight_XX` states; GP's tests use
  the mailbox's fight command instead (§9.6), which needs no MY GP.

#### 9.2.6 KNOCKOUT format [new-code] M · Won't (v1)

A real single-elimination bracket of 8, 16 or 32 entrants: only Rockman's matches are played (3-5 fights); the others
are simulated from a POWER byte per fight id (`winner = higher (POWER + rand 0-7)`), with commentary between rounds
("UPSET!"), on the bracket renderer with a tree layout. Cost: a 48-byte POWER table, the simulator, the tree nametable,
records per size. Won't (R0.3). If it ever returns, its seed is shown and can be entered (consistency decision 34: the
NES has no clock, so a "daily" seed is impossible).

### 9.3 EXHIBITION RULES (modifiers) [new-code] S-M · Won't (v1)

Kept as a record (R0.3: Won't). Any cleared stage, a 4×4 grid of rules, unranked runs (scorecard, no bolts, no medals),
a sticker per active rule in RULES_BOOK, the same mask in MY GP. The rules: 0 BUSTER ONLY; 1 NO FORMS; 2 ONE HIT (4MI's
"Owata-shiki" nod); 3 FAMICOM RULES (no checkpoints: the `$0684` write suppressed except at the start); 4 ICE AGE (the
floor-type latch `$A7` forced to 5 on solid ground); 5 MOON BOOTS (the water gravity `$00.18` without water); 6 SUDDEN
DEATH (damage ×2 both ways); 7 NO CHIPS; 8 PACIFIST; 9 ROULETTE (the weapon changes every 600 frames); 10 NO HUD;
11 TURBO (enemy AI twice every 4th frame: a lag risk under the 9-slot cap, R1.8). `RS_RULES` keeps its two bytes so the
mode can return without a layout change.

### 9.4 RECORDS [new-code] M · Must (pages 1-3); page 4 Should, 5-6 Could, 7 Won't

Pages with NEXT / PREV; a page whose mode is not in the build is skipped. Times are frame counts, formatted `h:mm:ss`
or `m:ss.cc` (60 frames = 1 s, 4MI's convention).

| Page | Contents | Tier |
|---|---|---|
| 1 **FILE RESULTS** (pick a file) | per meta stage the build ships: the medal, best score, best time, KOs and clears. The KO column's heading is story's (`KNOCKOUTS` in EN; `TIWNS` in ENGRISH, 4MI's heading, `r4mi/modes.md` §7) | Must |
| 2 **FILE TOTALS** | play time, KOs, game overs, unplugs, bolts earned and spent, E-tanks used, weakness hits, HoF points, and the best rating with its seven rows (tag calls and `TURBO: YES` with the bundle) | Must |
| 3 **LIFETIME** (system block) | per-stage KOs and time, the totals, and the **venue mini-records** (below) | Must |
| 4 TIME ATTACK | records, DEV times, ★, the total of all records | Should |
| 5 GP RUSH | per course: the best time, tries and clears | Could |
| 6 ACHIEVEMENTS | every plate with its **exact condition** and its state | Could |
| 7 RULES | the sticker grid | Won't |

**Venue mini-records** (`VENUE_REC[8] × 2`, by venue id; a ROM table gives each label, its direction and its tier; the
venue's code writes it):

| Venue | Record | Better | Tier |
|---|---|---|---|
| Wind (1) | best SHOOTING DOWN % in the sortie | higher | Must (`venues_a.md`) |
| Tomahawk (5) | best quick-draw reaction, in frames | lower | Must (`venues_a.md`) |
| Knight (6) | fastest Metal Metslime kill, in frames | lower | Should (round 3: **yes**, venues_a's question 3; the slot is allocated now, the label row and the writer ship in v1.1) |
| Blizzard (0) | most bonus-meter time left at the condor grab | higher | Could (`venues_b.md`'s proposal) |
| Plant, Flame, Yamato, Centaur | none (the slot stays free; round 3: Plant gets no record, its treasures already pay as prizes) | | |

### 9.5 MUSEUM and sound test [new-code] M · Won't (v1)

Kept as a record (R0.3: Museum/VAULT is Won't): a BROADCAST BOOTH sound test (only HEARD tracks; live channel meters;
Rockman and Roll dancing), a PLAQUE GALLERY (every plaque read, plus thanks plaques for CX, 4MI and the 8 fan
designers), ENTRANT FILES (the vanilla boss panel for every fight in FIGHT_SEEN), the **VAULT: 1993** (vanilla's
unreachable debug SOUND PLAYER in bank `$28`, given a door; it needs its own band setup, since tech keeps IRQ handler 0
only as a preset, feasibility-21), and a DEV ROOM of commentary plaques. The SYS fields HEARD and PLAQUES stay allocated;
`fortress.md`'s F-PLAQUE may set PLAQUES bits so a returning Museum has data.

### 9.6 EXTRA CONFIG: RAM editor, level select, dev tool [new-code] M · Must

4MI's EXTRA CONFIGURATION (`r4mi/cheats.md` §5) is a page of binary fields, each pointing straight at live RAM, with
one help line per field. GP does the same, in hex and bit grids. Tech builds the engine (bank `$47`, warps, the DEV flag
and ring buffer, `tech.md` §14.6); this doc designs the screen.

**How it works:**

- **Data-driven:** a field table `{RAM address lo/hi, format, help id}`.
- **Formats:** hex byte, bit grid with labels, decimal 0-999.
- **On open:** pick a source: FILE 1-3 or DEFAULTS. It loads into the **scratch file** (magic `'S'`, never committed,
  §1.4), and every edit changes the scratch LIVE image. RULESET mode 3.

**Fields:**

| Group | Fields | Tier |
|---|---|---|
| WHERE | STAGE (meta 0-23 → engine id via §1.8; stages not in the build are skipped) · CP (checkpoint 0-7, from the stage record's `CK_TABLE`, `tech.md` §4.4) · SCREEN (raw `$0684` override, `FF` = use CP) | Must |
| PROGRESS | CLEAR (24-bit STAGE_CLEAR) · STORY · EVENTS · EVENTS2 · FORMS `TAG SUP JET POW` | Must |
| SECRETS | 24 × 5-bit grid `ENV PLT ITM RM EX`, one row per meta stage · PRIZES (32-bit) | Must |
| LOADOUT | WPN `CEN KNI TOM YAM FLA PLA WIN BLI` (venue-id bits) · WPN2 `M.BEAM` · E-TANK · LIVES · BOLTS · CHIPS (24-bit owned) · EQUIP (24-bit equipped) · RATEFLAGS `SOLO KO RIV CARD DOPE` | Must |
| | W-TANK; PARTS / PARTS USED / GARAGE | Should; Could (bundle) |
| RULES | DIFF preset · DIFF A (bits labelled `93 HRD GRD CAS DROP DMG`) · DIFF B · DIFF C | Must |
| CHEATS | LIVES LOCK · REFILL AT PAUSE · GOD (HP pinned, pits and spikes respawn you in place) · BOSS HP 1 · RNG LOCK (seed 16-bit) | Must |
| DEBUG | LAG BAR (PPUMASK grey bit on while the main thread runs) · OBJ COUNT (occupied slots in the corner, the R1.8 cap) · LAST KILL (the last death hook's LATCHSRC category, `systems.md` §13.7) · FRAME STEP (enables pad 2's START/RIGHT, below) | Must |
| | HITBOXES | Could |

**Actions:**

| Action | Does | Tier |
|---|---|---|
| ENTER STAGE | Load STAGE/CP with the edited state, through the vanilla warp (`$51`, `$0684-$0686`, `$F0 = 2`; 4MI lesson 10's one-byte respawn), which now clears stale bits on an id change (`tech.md` §4.5) | Must (M2) |
| TO BRACKET | Open the bracket with the edited bits | Must (M2) |
| FIGHT n | `fight_load(n, XCONFIG)` (§9.2.1); shows WIN / LOSS on return | Must (M7) |
| WRITE FILE n | Commit the scratch image into file n, which sets **EDITED** for good | Must |
| RESET COUNTERS | | Must |

**Disqualifier.** Anything played from EXTRA CONFIG runs on the scratch file, which never saves and never earns
achievements or records. WRITE FILE marks the target EDITED. An EDITED file still plays, and its rating shows with `*`
(`RESULT UNDER REVIEW`), but it grants no achievements. This is 4MI's `$7697 = 3` rule (`r4mi/modes.md` §6), except
that GP **marks the file** instead of silently voiding it.

**DEV entry points: one meaning each** (R1.14, feasibility-21, `tech.md` §14.5). In DEV builds (`DEV = 1`):

| Combo | Where | Meaning |
|---|---|---|
| pad 1 SELECT + START held | the title | open EXTRA CONFIG |
| the pause menu's `TEST` row (not "DEBUG": the pause font has no D, consistency-23) | in a stage | open EXTRA CONFIG |
| pad 2 SELECT held 1 s | in a stage | kill and respawn at the current checkpoint |
| pad 2 START / pad 2 RIGHT | in a stage, with FRAME STEP on | freeze / step one frame (round 1's pad-1 "SELECT+START freezes" is gone: pad 1's SELECT means only the swap in stages, R2.10) |

**The test mailbox** (BRIEF §7.3; the regression entry point) [new-code] S · Must. 32 B at **page 0 offset `$1A00`**
(§1.2). RESET maps page 0, reads it, **clears the magic first**, then builds that state without menus (`tech.md`
§14.5). Tests write it into the `.sav` before boot, which replaces savestates (vanilla states cannot load into the MMC5
build).

| Bytes | Contents |
|---|---|
| +0..+7 | magic `"R6GPTEST"` |
| +8 | command: 1 enter stage; 2 fight (through the fight loader, return kind 4; from M7); 3 bracket; 4 title with a file loaded; 5 run the TA timer (Should); 6 **judges' desk** for the meta stage with the given SECRETS (screenshots every debrief, §16 risk 1) |
| +9 | meta stage |
| +10 | CP |
| +11 | file source (0 defaults, 1-3 a file) |
| +12 | **DIFF preset override** (`$FF` = keep the source's) |
| +13 | **global overrides**: b7 apply; b0-1 LANGUAGE; b2-3 ANNOUNCER; b4 FLASHES REDUCED; b5 SELECT SWAP OFF; b6 A/B SWAP |
| +14 | cheats (`RS_CHEAT` bits) |
| +15..+16 | RNG seed |
| +17 | fight id |
| +18..+19 | WEAPONS |
| +20 | FORMS |
| +21..+23 | CHIPS_OWNED |
| +24..+26 | CHIPS_EQ |
| +27 | E-tanks |
| +28 | lives |
| +29 | INPUT LAG |
| +30 | b0 the loadout bytes +18..+29 are valid; b1-7 reserved |
| +31 | checksum (sum of +0..+30) |

- **Why a mailbox:** golden movies, damage sweeps and per-stage states (the CX lesson 9 harness) become one Python line
  that pokes the `.sav` before the first frame. This is 4MI's injected-save trick (`r4mi/cheats.md` §10), made explicit.
- **The testing policy** (RULINGS §6): golden movies run with +12 = `$FF` and +13 = 0 on a NORMAL source file, i.e.
  NORMAL + EN; the smoke movie for each other meta setting (CASUAL, HARD, JP, ANNOUNCER OFF, FLASHES REDUCED, A/B SWAP,
  INPUT LAG 6, SELECT SWAP OFF) is the same movie with one override byte changed, recorded once per milestone and
  re-recorded only at ⛳ gates.
- **It is kept in release builds**, so the tests run on the shipped ROM. The magic plus the checksum make a false
  trigger from garbage RAM a 1-in-2^72 event.

### 9.7 BASS MODE [new-code] L · Won't (v1)

Kept as a record: a NEW-file ENTRANT toggle (U0.6), FILEFLAGS.BASS, records in TA_BASS, story line swaps at the key
beats (the Riot intro becomes Rockman crashing Bass's bracket), the rating's TEAM row re-labelled SOLO, a Bass solution
for every adaptor gate (PLAN §2.8; the venue owners mark which). The FILEFLAGS bit and the SYS field stay reserved.

### 9.8 MR. X RETURNS [new-code] M · Won't (v1)

Kept as a record: unlocked by Gold on every stage plus the Mr. X card (U1.5); the *original* Mr. X turns out to be real
and furious that Wily borrowed his name twice; built cheaply on vanilla **Mr. X Fortress 1** untouched (engine id `$1F`
points at legacy `$08`'s layout and tileset `$2C:$92`, `tech.md` §4.2; vanilla music `$09`, vanilla boss), a one-screen
exchange, and a final fight against Mr. X's flying chair (fight `$28`). Its reward was the achievement THE X-FILES and
the TRUE GP finale `$28`.

---

## 10. Achievements [new-code] S · Could (cut-line item 12)

There are up to 16 plates in a strip under the SPECIAL EVENTS menu (4MI shows 3). Each bit is set at the moment the
condition is met, and **never on an EDITED file, the scratch file, or with `RS_CHEAT` b7 set**. Every condition is
printed in RECORDS page 6: 4MI's HARD ROCK silently required six sub-settings, and GP will not repeat that. A plate
exists only in a build that ships what its condition reads; the plate's tier is the highest tier among its
dependencies.

| Bit | Plate | Exact condition | Needs |
|---|---|---|---|
| 0 | **GRAND CHAMPION** | championship rating 100 | Could |
| 1 | **IRON ENTRANT** | win the championship with HARD_CLEAN (the HARD preset, all its sub-settings unchanged since NEW GAME) and GAMEOVERS = 0 | Could |
| 2 | **1993** | win with R1993_CLEAN | 1993 RULES (Could) |
| 3 | **FULL BRACKET** | every Exhibition the build ships cleared | the Exhibitions (Could) |
| 4 | **ALL GOLD** | GOLD or better on every stage the build ships | Could |
| 5 | **PLATINUM ROW** | PLATINUM on all 8 venues | Could |
| 6 | **TOURNAMENT HISTORIAN** | every SECRETS bit the shipped stages define | Could |
| 7 | **THE GREATEST GP IN HISTORY** | clear TRUE GP | GP Rush (Could) |
| 8 | **CUP COLLECTOR** | clear all 9 one-weapon cups | GP Rush (Could) |
| 9 | **SPEED KING** | CHAMP_TIME < 324,000 frames (1:30:00) (tune) | Could |
| 10 | **WEAK SPOT** | WEAK_SEEN covers every non-secret fight id the build ships | Could |
| 11 | **DEV TIME** | ★ on every Time Attack stage | Time Attack (Should) |
| 12 | **INCORRUPTIBLE** | win a file on which Mr. Y's booth offered TURBO and you never took it; hidden as `???` until earned | the bundle (Could) |
| 13 | **ONE HIT WONDER** | all 8 venues with the ONE HIT rule | Won't (Exhibition Rules) |
| 14 | **BASS CLEAR** | win on a BASS file | Won't (Bass Mode) |
| 15 | **THE X-FILES** | beat MR. X RETURNS; hidden until earned | Won't |

---

## 11. CONFIG

`systems.md` §13 owns what each setting does and where it is read. This section owns the menus, the storage, and the
split between **global** settings (system block) and **per-file** settings (the file's DIFF bytes). Every label and
help line is story's.

**Why per file** (accepted by `systems.md` §13.1): three files are often three players. Each file's achievements and
its records' C/N/H badges must reflect the settings that file was played on. So the difficulty group lives in the file,
and everything about the person or the TV is global.

### 11.1 Global options (title → CONFIG; system block `$008-$00C`) [new-code] S · Must

| Option | Values (default first) | Effect | Tier |
|---|---|---|---|
| LANGUAGE | ENGLISH / JAPANESE | text table selection: the new engine's string tables, and the vanilla PPU-script hook at **`$3C:$8636`**, where the interpreter reads the script pointer (`tech.md` §11.2 is the source of truth; consistency-41) | Must |
| | ENGRISH | §12 | Could |
| ANNOUNCER | ON / DEATHS ONLY / OFF | commentator pop-ups (BRIEF §5.5, `tech.md` §11.7). DEATHS ONLY keeps the death and P1 lines. The judges' debrief and scenes are unaffected | Must |
| TEXT SPEED | NORMAL / FAST / INSTANT / SLOW | typewriter frames per cell: 2 / 1 / 0 / 4 | Must |
| FLASHES | NORMAL / REDUCED | **R3.5**: in NORMAL no effect flashes a large area more than 3 times per second (tech's flash service enforces it, `tech.md` §8.5; `systems.md` §5.1); REDUCED turns every flash into a fade (C.FLASH, the WEAK flash, boss hit pulses, the Riot blackout, explosions) | Must |
| SCREEN SHAKE | ON / OFF | | Must |
| **INPUT LAG** | 0-6 frames (default 0) | **R3.5**: added to every reflex window, never to mash counts or timers (`systems.md` §1.6: the quick-draw is 24 / 18 / 40 f + INPUT LAG). Story's help line tells the player to set it to the TV's lag | Must |
| SELECT SWAP | FULL / WEAPONS ONLY / OFF | `systems.md` §1.1: hold SELECT + D-pad cycles weapons (and forms, in FULL); a tap toggles the last weapon. OFF = vanilla feel | Must |
| A/B SWAP | OFF / ON | jump on B, fire on A. [code, r2] The joypad read `$3E:$C711` builds each pad's held byte in `$40,X` and its new-press byte with `AND $44,X / STA $42,X` at `$C732`; the swap is a conditional `EOR #$C0` on `$40` (when exactly one of A and B is held) just before `$C732`, in the same registry hook as `systems.md`'s SELECT filter | Must |
| HUD TIMER | OFF / ON | the in-stage timer widget (always on in Time Attack) | Should |
| 2P SHIFT | ON / OFF | controller 2's A/B cycle weapons (`systems.md` §1.5) | Should |
| MMC5 AUDIO | ON / OFF | the extra pulse channels; OFF for consoles without expansion audio; default ON, every track being complete on the 4 base channels (consistency decision 36) | Could (with the MMC5 pulse driver, `tech.md` §12.5) |
| MMC5 ARRANGEMENTS | OFF / ON | arranged tracks where `art_audio.md` makes them | Could |
| SOUND TEST | → | a shortcut to the Museum booth | Won't |
| LOAD DEFAULTS | | everything above except LANGUAGE | Must |

### 11.2 Per-file options (pit stop → CONFIG; DIFF bytes `$009-$00D`) [new-code] S · Must

The preset values are `systems.md` §13.2's:

| Option | Values | CASUAL | NORMAL | HARD | 1993 RULES (Could) |
|---|---|---|---|---|---|
| DIFFICULTY | the presets, or EDIT after any hand change | | | | |
| DAMAGE (to Rockman) | ×0.5 / ×1 / ×1.5 / ×2, rounded up | ×0.5 | ×1 | ×1.5 | ×1 |
| LIVES (start and continue) | 1-9 | 5 | 3 | 3 | 3 |
| E-TANK FLOOR | 0-4 | 2 | 0 | 0 | 0 |
| DROPS | NONE / LESS / NORMAL / MORE | MORE | NORMAL | LESS | vanilla (from the RULES bit) |
| REFILL on respawn | NONE / HALF / FULL | FULL | HALF | NONE | NONE |
| GUARDS (SPIKE GUARD + Beat on loan, slotless) | OFF / ON | ON | OFF | OFF | OFF |
| **CASUAL** (the CASUAL layout tier and lever values: reflex ×2 except the quick-draw, which is 40 f (R8.6), mash −40 % or hold, timers +50 %, +1 checkpoint per section, skill-gated secrets one step easier; R2.9) | OFF / ON | ON | OFF | OFF | OFF |
| HARD (the HARD tier: in v1.0 the 18-f quick-draw; per-stage HARD content is Should) | OFF / ON | OFF | OFF | ON | OFF |
| RULES | GP / 1993 | GP | GP | GP | 1993 |

CRITICALS is gone (R2.4). **1993 RULES is a NEW GAME choice only** (Could; `systems.md` §13.6 lists what it switches
off): switching a file into or out of 1993 would strand owned chips and bolts, so the RULES row is greyed out after NEW
GAME.

**Lowering a setting.** If the file becomes easier than its starting preset on any row (DAMAGE lower, LIVES higher, DROPS
more, REFILL more, GUARDS on, **CASUAL on**, HARD off), HARD_CLEAN clears for good and LOWEST updates. The pit stop warns
first (story's words). The records keep each medal's preset badge (`systems.md` §13.2: accessibility is never punished in
the score, only labelled).

### 11.3 The health notice (R3.5) [new-code] S · Must

The boot screen of §2.1 step 3. It is the one place the game tells the player about REDUCED before any flash can play.
`story.md` writes it (EN and JP); `systems.md` §5.1 and `tech.md` §8.5 are what make it true.

---

## 12. ENGRISH [new-code + text] S · Could (cut-line item 12)

**What it is.** A joke tribute to 4MI, whose language option offers JAPANESE / ENGRISH with "ENGLISH COMING SOON"
(`r4mi/modes.md` §5). GP has real English, so ENGRISH is a third choice that swaps deliberately broken strings into a
handful of **menus**. Dialogue, hints and help pages stay ENGLISH, so nothing becomes unreadable.

**How it works:**

- `LANGUAGE = 2` reads a sparse override table (sorted string ids → pointers); missing ids fall back to ENGLISH
  (`tech.md` §11.5: the TSV's ENGRISH column).
- **Digits:** ENGRISH prints numbers with the letter **O for zero** (`1OO`, `TIME 1:O3.45`). This is 4MI's zero-less
  font, mirrored: vanilla RM6's pause font has no O and writes `N0R`, `P0W`, `W.ST0RM` with zeros (`rm6/text.md` §5.3).
- **C.FLRSH:** the ENGRISH pause-menu weapon name is vanilla's own data misspelling (`rm6/SUMMARY.md` §1.2); the YOU GET
  card keeps C.FLRSH in every language (`systems.md` §3.9).
- **The list** (title, file select, difficulty, bracket, YOU GET, scorecard, shop, pause, game over, RECORDS, rating,
  Break Man's perfect line, the translation credit) is `story.md` §9's final list; round 1's draft is in git
  (`95288ee`). Rule for the text pass: ENGRISH is affectionate, never mocking, and never in story text, hints or help
  pages (one deliberate exception: Break Man's perfect line, story's S47.PE, which nods to 4MI's line in new words: like
  every line quoted from another game, it is paraphrased, never verbatim, R8.4).

---

## 13. Build list (tags, sizes, tiers, sessions)

The ledger rows (`tools/plan/tally.py`, area `meta`); the Must rows sum to 31, the same as `tight.py`'s meta block.

| Item | Tags | Size | Tier | Sessions |
|---|---|---|---|---|
| Save module: A/B copies, trailer, commit, load, migration, BROKEN paths, autosaves, IN_MATCH, save tests | [new-code] | M | Must | 3.5 |
| Title and boot: license line, health notice, menu | [new-code][new-art] | S | Must | 1.5 |
| File select (cards, NEW/START/ERASE guards) and the difficulty pick | [new-code][new-art] | M | Must | 2.5 |
| Bracket: node table, states, centre logic, rematch hook, Riot trigger and POSTPONED, event queue | [new-code][new-art] | M | Must | 4 |
| Results screen: judges' desk, slide-in rows, medal stamp, prize line, secret icons | [new-code][new-art] | M | Must | 2.5 |
| Debrief engine, predicate tables (tier B), stage counters | [new-code] | M | Must | 2 |
| Medal derivation, HoF points, unlock bits | [new-code] | S | Must | 1 |
| RULESET choke point and the generated bit table | [new-code] | S | Must | 0.5 |
| CONFIG global + per file (INPUT LAG, CASUAL, FLASHES, A/B SWAP) | [new-code] | S | Must | 1.5 |
| EXTRA CONFIG UI, actions, scratch file, test mailbox, DEV entry points | [new-code] | M | Must | 3 |
| Pit stop: shop, 14-chip grid with help pages, file CONFIG, SAVE & QUIT | [new-code][new-art] | M | Must | 2.5 |
| Game over screen, pause RETIRE, unplug count | [new-code] | S | Must | 1.5 |
| RECORDS pages 1-3 with the venue mini-records | [new-code] | S | Must | 1.5 |
| Fight table: v1.0 records, run order, the loader interface (the loader is tech's) | [data] | S | Must | 0.5 |
| Fortress maps (H, W) with REPLAY and BACK TO BRACKET | [new-code][new-art] | S | Must | 1.5 |
| Championship rating (re-derived) and Break Man's debrief | [new-code] | M | Must | 1.5 |
| **Must total** | | | | **31** |
| Time Attack (+ splits, DEV times, story presets, return kind 6, HUD TIMER, RECORDS page 4) | [new-code] | M | Should | 3 |
| File COPY | [new-code] | S | Should | 0.5 |
| Sponsor's-chair gag, Eddie SAVING icon, tier A escalation data | [new-code][new-art] | S | Should | 0.5 |
| Attract crawl | [new-code][new-art] | S | Could | 1.5 |
| Hidden PASS WORD gag | [engine-ok][new-code] | S | Could | 0.5 |
| Exhibition layer (B) and badges | [new-code][new-art] | S | Could | 1.5 |
| Riot intro animation | [new-code][new-art] | S | Could | 1 |
| Bundle hooks: garage and booth rows, DOPED, BREAK MAN WALKS, asterisks, the T1/T6/T7 bundle rows | [new-code] | S | Could | 1.5 |
| 1993 RULES meta hooks (NEW GAME choice, R1993_CLEAN, the 93 badge, the 1993 ROW) | [new-code] | S | Could | 0.5 |
| GP Rush: runner, lobby, courses, MY GP | [new-code][new-art] | M | Could | 5 |
| RECORDS pages 5-6 and achievements (page 4 is Time Attack's) | [new-code][new-art] | S | Could | 2.5 |
| ENGRISH override table | [new-code] | S | Could | 1 |
| KNOCKOUT | [new-code][new-art] | M | Won't | 3 |
| Exhibition Rules and the TURBO rule | [new-code] | S-M | Won't | 3.5 |
| Museum, VAULT, plaque gallery | [new-code][new-art] | M | Won't | 3.5 |
| Bass Mode (player sheet code, meta hooks, level answers) | [new-code][new-art] | L | Won't | 10 |
| Mr. X Returns (and the chair boss) | [new-code] | M | Won't | 4 |

Moved out of this doc: **the fight loader** (2.5, now `tech.md`'s item 40, R1.7); the GP fanfare (`art_audio.md`'s
track list, R5.2).

---

## 14. Lessons applied

- **CX 1, one premise everywhere:** the file select is a registration desk, the stage select a bracket, every clear a
  judging, the halftime riot a stadium joke, the rating a championship.
- **CX 3, voice on failure:** the unplug line, the game-over table, BREAK MAN WALKS (with the bundle).
- **CX 6, telegraph the tool:** requirement hints override instructions when the needed form is missing.
- **CX 7, special cases in visible tables:** the event queue, debrief predicates, rating tests, the fight table and the
  prize-bit table are all data.
- **CX 9, a test harness:** crafted saves with checksums become the TEST MAILBOX, with override bytes for the smoke
  matrix.
- **CX saves:** three slots. The silent "bad sum = new game" failure is *not* kept; GP shows BROKEN DATA.
- **4MI 5, one predicate table for score and hints:** used twice, per stage (judges) and per game (rating + Break Man);
  the same routine gates collect-N rewards in the stage.
- **4MI's 102→100 trade-off:** kept for the bundle build (TURBO +2 costs Break Man −5); v1.0 reaches exactly 100.
- **4MI 9, boss rushes on one fight table with one lobby:** the fight table is Must data now; the rush modes reuse it.
- **4MI 10, a level select and RAM editor from day one:** EXTRA CONFIG plus the mailbox.
- **4MI, the double copy and a strong checksum:** kept and improved (ping-pong, commit marker), with graceful BROKEN
  handling everywhere, and fuzz-tested.
- **4MI, START+A to overwrite.**
- **4MI, modes override config through one choke point:** RULESET, now also the fight loader's and the macros' source.
- **4MI, exact achievement rules, shown in game** (Could).
- **4MI, frame-count records.**
- **RM6 3:** GP state lives in PRG-RAM, not in the 89 free CPU bytes.
- **RM6 7:** adaptors become real save flags.
- **RM6 8, vanilla quirks kept on purpose:** TO BE CONTINUED ends the rating; C.FLRSH (ENGRISH, Could); the password
  grid gag (Could).
- **RM6 fortress.md:** the Wily 3 rush shows the rush is data; fights load through the vanilla warp (`$51`,
  `$0684-$0686`, `$F0 = 2`), wrapped by tech's loader.

---

## 15. Cross-doc dependencies

**What the Musts here lean on (R0.4)**, all Must in their owners' docs: tech's PRG-RAM pages and save module service,
the WORK ledger ranges (LIVE images, RULESET, the run block's stage counters, the fight block), the stage record's
`META`, `FLAGS1.REMATCH`, `CK_TABLE` and `FIGHT_ROW`, the fight loader, the text engine v1a (menu-screen windows) and the
mailbox read in RESET; systems' scorecard, prices, chips and settings; story's strings; the fortress's map art, the
Riot's capsule beat and H5's card; the venue docs' secrets, prizes and mini-records.

| Doc | Must agree on |
|---|---|
| `systems.md` | **Adopted:** 3-byte CHIPS_OWNED/EQ in §9.2's order with bits 14-17 reserved for the bundle; PRIZES (4 B); STAGEREC[24]; FORMS.TAG (not BREAK_JOINED); DIFF A = DAMAGE b0-1, DROPS b2-3, CASUAL b4, GUARDS b5, HARD b6, 1993 b7; INPUT LAG global (SYS `$00C`, copied to `RS_LAG` for `REFLEX`); medal points B1/S2/G3/P4; best PAY and the C/N/H badge; the §9.5 rating inputs (implemented as §6.1); METALLS and DOVE removed; the difficulty group per file (accepted in its §13.1). **Asks:** W2's run block survives the bout warps, so the bouts count in W2's scorecard (§9.2.1); its `REFLEX` reads `RS_LAG`; its code says `IFHARD` etc., which read `RS_DIFF`, not the file byte |
| `story.md` | **Owns every word**: hint text (§7, both tiers, with YA0's new riddle and PL0's without the explorer's name), generic debrief lines (§7.3: only the requirement hint R2 is Must, R1, R3 and R5 Should), the fortress stages' hints (§7.2, W3's three Should), Break Man's debrief (S47, with a new T1 SOLO RIOT entry, and the "never called" line pointing at the pause **CALL row with A**, R2.10), rank titles (S46), every menu label, the HARD description that matches v1.0's HARD, the health notice, INPUT LAG and CASUAL help lines, the Riot intro lines (S14), the adaptor hand-offs (S12, S13, S29), the theft (S25), the unmasking (S33), the game-over and unplug lines (S16), the sponsor's-chair signs, ENGRISH's list (§9; the perfect line S47.PE paraphrased, R8.4), the H2/H4 door label `CLOSED FOR RENOVATION` (S26.4). **Kept here as story asked:** STORY_BEAT at FILE `$013` with story's values; COMMFLAGS at FILE `$04A`; the chair's `BACK SOON` from STORY_BEAT `$03` and `RESERVED` from `$09`; `B EXHIBITIONS` without a colon (Could) |
| `venues_a.md` / `venues_b.md` | SECRETS b0-b4 per venue and the debrief order (§4.3, the weight rule they both now follow); tier B hints verbatim (through story §7); PRIZES indexes (§1.6.1: Blizzard 4, Plant 4, Tomahawk 3, Knight 1); VENUE_REC (§9.4: Wind and Tomahawk Must, Knight Should, Blizzard Could, Plant none); each champion boss reads `RS_PINCH` (the fight record's +10) for its pinch threshold, 0 meaning its own default (W2's SUPER copies, §9.2.1); STAGE_CLEAR read by LAND, EXPRESS and Blizzard's replay-skip door; `CFG_CASUAL` = DIFF A b4; mid-boss fight ids `$08-$10` with their arenas (§9.2.1); the R3.3 venue names (§3.2); every collect-N secret on the stage counters (§4.6), at most one per venue |
| `fortress.md` | SECRETS b0-b3 for meta 0, 9, 14-21 and their tier B hints; **the Riot's capsule beat (Bass β duel 1: Break Man's whistle and a life capsule below 6 HP) stays Must**, and Bass β's death sets RATEFLAGS b4 SOLO RIOT when the capsule never dropped in that run (and b2 RIVAL as before), since rating T1 reads it (else §6.1's fallback); **Mr. X's card in H5's hidden room stays Must** (T14; else the fallback); RIVAL (no damage from the bar fill to the overdrive); fight ids `$13-$17`, `$1C-$28` and `$29` (Doc Robot MK-VI, Should) and their arenas (`$15` = Kamegoro Maker); the per-fight pinch byte (record +10) for W2's SUPER copies; **no PRIZES bits** (prize bolts key on SECRETS b0/b2, §1.6.1); the HoF and Castle maps' art, with H2, H4 and W1 drawn as closed wings in v1.0 (H2's and H4's doors read `CLOSED FOR RENOVATION`); the GP Rush lobby as Opening screen `$1D` (Could); W2's hub calls `fight_load(id, HUB)` and reads `FIGHT_RESULT`; W3's clear runs the ending without a desk; F-PLAQUE may set SYS PLAQUES bits |
| `tech.md` | Page 0 map (§1.2) at page offsets `$0000-$1A1F`, LIVE images in WORK at `$7400`/`$7600`, write protection by isolation; `save_commit` refuses the scratch magic and NO_SAVE; RULESET at `$6270` with `RS_DIFF` as the macros' source and `bits.inc` generated from §1.6; the stage counters (2 B) in the run block; the mailbox at page 0 `$1A00` with §9.6's format and the fight command through the loader (return kind 4); the rematch hook `H_REMATCH` at `$3F:$F952` (the operand of `JSR $F527` at `$F951`) and the replay test in the `$F9A0` hook (skip YOU GET); the A/B SWAP edit at `$3E:$C732` inside the joypad hook; return kind 6 for Time Attack (Should); the 11-byte fight record, with `fight_load` copying +10 into `RS_PINCH`; the stage record v0 from M2.1 for the slice's `SA.META` and `FLAGS1.REMATCH` reads (R8.2); the language hook at `$3C:$8636`; the DEV entry points of §9.6; meta's thread code in banks `$42-$43` |
| `art_audio.md` | The title (vanilla logo + GP badge + subtitle), the bracket nametable, medal ribbons, the POSTPONED stamp, the cracked frame, Bass β's portrait, the trophy states, the file cards, the judges' desk with face icons (the rating screen draws over it, R8.6), the pit-stop counter with Eddie (new art, a composite, R8.6), the fortress maps (with closed wings), the participation ribbon; Could: badges, the booth sprite, the lobby tunnel, achievement plates, Eddie's SAVING icon (Should), the sponsor's-chair cut-out (Should) |

## 16. Risks

1. **The slice is overloaded.** Meta's M2-M3 share is 23 sessions (items 1-12). RULINGS §6, re-baselined by R8.1 from
   each doc's own figures, now gives about 53 sessions for all of M2 (26 → 79) and about 46 for all of M3 (79 → ~124);
   tech's M2 is 31.5 and systems' slice about 28 (R8.2 moved the form swap and the adaptors to M5). Round 1's 45 and
   25 had under-counted the slice. Mitigation: file-select-lite and bracket-lite in M2 (one node, no centre logic), the
   title as a plain text menu until M5's pattern-table split, RECORDS at M6; the M4 re-estimate decides the rest.
2. **Hint text drifting from the venues.** The tier B lines are the venue owners', through story §7. Mitigation: every
   hint id is listed per venue (§4.4); mailbox command 6 screenshots every stage's desk with SECRETS = 0 at each gate,
   and the M9 text pass checks each predicate against its venue doc.
3. **Save size and the layout freeze.** The FILE block keeps 126 reserved bytes and the system block 194, after
   allocating every v1.1+ field. If more is needed before v1.0 (per-row scorecard bests would take 120 B), the FILE blocks
   can grow to 768 B each into page 0's 3 KB of reserve; after release, only migrations.
4. **Rating balance.** T11's 3 hours and SPEED KING's 1:30 are guesses for 15 stages; T1 and T13 both read the same
   duel (a perfect duel passes both). Tune at M9 against playtest saves (RECORDS' totals exist for this).
5. **Riot soft lock.** POSTPONED must never leave a player with nothing selectable. The Riot is always selectable and
   the pit stop reachable. A test: a file with 4 wins, 0 lives and 0 bolts must still reach the Riot.
6. **The rating's two fortress dependencies** (the Riot capsule, the Mr. X card). If either leaves v1.0, §6.1's
   fallbacks apply; the unit test of §6.4 asserts the sum is still 100.
7. **Power-cycle safety on hardware.** The ping-pong copies and the commit marker are designed for torn writes, but the
   real test is the M9 hardware run (§1.9), which depends on the user's cart (RULINGS §7 question 1).
8. **The bundle's arithmetic.** When the bundle returns, T1, T6 and T7 change together; §6.4's build flag and unit test
   (102 printed, 100 reachable, 96 with TURBO) keep it honest.

## 17. Open questions

Round 1's seven questions are closed (consistency decision 34): the POSTPONED lock, not a forced Riot; RETIRE is free;
Kalinka speaks the debrief; no tag call in Time Attack; unlocks are global; KNOCKOUT's seed would be shown and enterable
(KNOCKOUT is Won't); 1993 files may earn unlocks.

Still open:

1. **The hardware target** (RULINGS §7 question 1) decides how §1.9's power-cut test runs.
2. *(Settled by R8.8: EXTRA CONFIG keeps the championship unlock, since it marks files EDITED and the championship is
   the natural "you have seen everything" point. The user may still move it, for example to 40 HoF points.)*
3. *(Settled by R8.8: RECORDS keeps 20 HoF points, for the 4MI-style reveal, around the 6th venue. The user may still
   choose to show SPECIAL EVENTS from the first save.)*

---

## Changes in round 2

| # | Change | Ruling / finding |
|---|---|---|
| 1 | Added **"## v1.0 scope"**: 16 Must items with milestones and sessions, 31 in all (round 1's tight 33.5 minus the fight loader's 2.5, now tech's); per-milestone split; the slice path; the testing-policy hooks; Should/Could/Won't lists | R0.1, R0.2, R0.4, R1.7; scope-1, scope-2, scope-3 |
| 2 | Re-tiered every section to Must / Should / Could / Won't (v1); each table row carries its tier; the build list (§13) carries sessions | R0.2, R0.3, R0.4; scope-2, scope-22 |
| 3 | Post-game per R0.3: EXTRA CONFIG and RECORDS 1-3 Must; Time Attack Should; GP Rush, MY GP, achievements, ENGRISH, the attract crawl, RECORDS 5-6 Could (page 4 goes with Time Attack); KNOCKOUT, Exhibition Rules, Museum/VAULT, Bass Mode, Mr. X Returns Won't (kept as short records) | R0.3; scope-22, design-6 |
| 4 | §1.2: page 0 as page offsets mapped at `$A000` only inside the save module; LIVE FILE / LIVE SYS in WORK at `$7400`/`$7600`; write protection by isolation; the mailbox at page 0 `$1A00` | R1.6; tech §2.2, §13; consistency decision 37 |
| 5 | §1.6 FILE block re-laid as the final layout: 3-byte CHIPS_OWNED/EQ (14 v1.0 bits, 14-17 reserved for the bundle), PRIZES (4 B) with a prize-bit table (§1.6.1), RATEFLAGS b4 SOLO RIOT, COMMFLAGS kept at `$04A`, every v1.1+ field pre-allocated; METALLS, DOVE and CRITICALS removed; DROPS VANILLA derived from the RULES bit; FILEFLAGS bits re-packed | consistency-11; R2.5, R2.7; systems §15.1; story's `$04A` request |
| 6 | DIFF A: CASUAL b4 (new `CFG_CASUAL`), GUARDS b5, HARD b6 (so `BIT`/`BVC` tests HARD), 1993 b7; `bits.inc` generated from this table; macros read RULESET's copy | consistency-15, consistency-16; R2.9, R1.10; design-7 |
| 7 | §1.8 meta index table now names each engine id from tech §4.2 and its tier; HoF points and medals count only shipped stages | R1.2; feasibility-2, consistency-2, scope-12 |
| 8 | §1.9 save tests: offline `.sav` fuzz cases, a save/reset/reload round trip, the M9 hardware power-cut test | RULINGS §6 testing policy; scope-26 |
| 9 | **SEMIFINAL RIOT renamed HALFTIME RIOT** everywhere (centre node, trigger, events, RIVAL) | R4.3; design-14 |
| 10 | Rematches: located vanilla's no-rematch beam-out at `$3F:$F951 JSR $F527 / BCS $F9A0`, verified in the emulator (a refight spawns with the branch removed), and specified the `H_REMATCH` hook and the replay skip of YOU GET | R0.2 (the slice's replay); venues_b decision 38 |
| 11 | On-screen venue names fixed to R3.3's list (all ≤ 20 characters); the bracket shows champion names (its font has no apostrophe); no third-party names in hint ids or screens | R3.3; consistency-42, design-10 |
| 12 | The Exhibition layer and badges are Could (badges draw as rivets in v1.0; E4 Won't); `B EXHIBITIONS` without a colon | R3.7; scope-9; consistency-23 |
| 13 | Riot intro: stamps and lines Must, the animation Could | R0.3 item 12 (scope tally); story S14 |
| 14 | Event queue rewritten with tiers and story scene ids; EVENTS b5 (Break Man joins at Riot 0E with Rule 9 played in place) is Should with the partner; EVENTS2 b4 follows FORMS.SUPER set at the H3 screen-12 dock | R4.2; consistency-28; consistency decision 11 |
| 15 | Pit stop: v1.0 rows SHOP, CHIPS (14-chip grid, B opens the 4 × 28 help page), CONFIG, SAVE & QUIT; GARAGE and MR. Y'S BOOTH are the Could bundle, with "BREAK MAN WILL WALK." on the second confirmation | R2.5, R2.8, R2.10; design-21, design-24, scope-21 |
| 16 | New §3.9 fortress maps (Must): node-table driven, H2/H4/W1 closed in v1.0, REPLAY, BACK TO BRACKET (now Must), per-wing saves, the load target; W3 runs the ending without a desk | R0.2; fortress §9.3 requests |
| 17 | Debrief: tier B Must, tier A Should, with the engine falling back to tier B when tier A is absent; requirement hint R4 TAG Should; perfect-line rotation Should | R4.5; scope-18 |
| 18 | Hint and debrief **text removed** from this doc: story owns every word (§7, S46, S47, §9); meta keeps ids, order and the secrets they point at; YA0 is now the draft (the sekisho is cut) | R4.1, R3.2; consistency-6; story §7 |
| 19 | Predicate record widened to 24 B (counter targets, `HINT_BASE`); `require` codes tiered (TAG Should; weapon 8 = M.BEAM) | R1.10, R4.2 |
| 20 | New §4.6 stage counters: one `pred_test` routine gates collect-N rewards in the stage and drives the debrief; at most one per stage | R1.10, R3.1; scope-16, design-5 |
| 21 | **Rating re-derived so 100 is reachable with v1.0 content**: T1 = SOLO RIOT (the Riot won without Break Man's capsule), T3 removed, T4 and T5 4 points each, T6 2 per shop chip; every test reads Must content; fallbacks for the two fortress dependencies; the T1 partner / T7 TURBO trap / garage rows move to the Could bundle (102 printed, 100 reachable, 96 with TURBO); a 1993 ROW for 1993 files | R2.7, R2.8, R4.2, R0.4; scope-3, scope-15, scope-21, consistency decisions 8 and 31; systems §9.5 |
| 22 | Doping: TAG-gated secrets use their full-charge-door fallbacks (nothing is lost); OWNED drops BREAK; consistency-38's "void" note superseded | R2.8; design-8, consistency-38 |
| 23 | Unlock chain: EXTRA CONFIG unlocks with the championship (round 1's "any cup" depended on Could GP Rush); RECORDS at 20 HoF; Won't unlocks kept as reserved bits | R0.4, R0.3 |
| 24 | §8 SYSTEM block: INPUT LAG at `$00C`; every record field tiered (TA Should, Rush and MY GP Could, KNOCKOUT/rules/Museum Won't reserved); FIGHT_SEEN Must for EXTRA CONFIG's list | R3.5, R0.3 |
| 25 | New §9.0 RULESET: the 16 bytes specified at WORK `$6270`, the mode table, `RS_DIFF` as the macros' source, `RS_LAG`, NO_SAVE / NO_DESK flags | R1.6, R2.9, R1.10; consistency-16; tech §3.4 |
| 26 | §9.2.1 **fight table is Must data**; the fight loader is tech's (R1.7); the interface table (callers, return kinds, `FIGHT_RESULT`); record flag b5 RULES_1993 for fight `$27` → legacy id `$0F` room 06; venue mid-boss ids `$08-$10` assigned; Doc Robot via the loader (Should); bouts never autosave | R1.7; scope-6, feasibility-3, feasibility-19, consistency-44, consistency decisions 12, 37, 40; R3.6 |
| 27 | GP Rush lobby = Opening layout screen `$1D` on TS_STADIUM (no id, no slot); runner state from WORK's free range; courses drop the criticals rule (criticals are Won't) | consistency-31, feasibility-12, R2.4 |
| 28 | RECORDS: pages tiered; venue mini-records assigned (Wind, Tomahawk Must; Knight Should; Blizzard Could) | venues_a / venues_b requests; R0.3 |
| 29 | EXTRA CONFIG: fields updated (24-bit chips, PRIZES, RATEFLAGS, DIFF A labels, LAST KILL, OBJ COUNT as the R1.8 cap); `FIGHT n` through tech's loader (M7); DEV combos with one meaning each (pause row `TEST`, frame step on pad 2) | R1.14, R1.8, R2.10; feasibility-21, consistency-23 |
| 30 | Mailbox: round 1's RULES bytes replaced by a DIFF preset override and a global-settings override, so each setting's smoke movie needs no menus; loadout overrides widened to 24-bit chips and INPUT LAG; command 6 (judges' desk for screenshots) | RULINGS §6 testing policy; scope-26 |
| 31 | CONFIG: **INPUT LAG** (0-6 f), FLASHES REDUCED tied to the 3-per-second rule, the boot **health notice** (§2.1, §11.3), the **CASUAL** row; CRITICALS removed; MMC5 AUDIO options Could; SOUND TEST Won't; A/B SWAP's patch site verified at `$3E:$C711-$C734` | R3.5, R2.9, R2.4, R1.3, R5.2; design-13, design-7; consistency decision 36 |
| 32 | Language hook cited at `$3C:$8636` (tech is the source of truth) | consistency-41 |
| 33 | Text windows: debrief, help and dialogue 4 × 28 (the CHIPS help page was 3 × 28); menu screens wait through the scheduler | R1.4; feasibility-10, feasibility-11, consistency-3 |
| 34 | Pause labels fit the pause font: `RETIRE`, `EXIT` (not QUIT), `TEST` (not DEBUG) | consistency-23 |
| 35 | Face icons and name labels replace desk and match-card portraits in v1.0 | R5.1 |
| 36 | Difficulty pick: CASUAL / NORMAL / HARD in v1.0 (HARD = ×1.5, drops LESS, no refill, 18-f quick-draw); 1993 RULES Could, with its rename; the HARD line must not promise remixed stages | R2.9, R3.5; design-18, scope-19, scope-20 |
| 37 | Title per art_audio's plan (vanilla logo + GP badge + subtitle); attract crawl and PASS WORD gag Could; the GP fanfare moved to art_audio's track list | R5.2, R0.3; scope-23 |
| 38 | Ledger: `tools/plan/tight.py` meta block re-itemised to these 16 Must rows (total unchanged at 31); `tools/plan/tally.py` meta rows rebuilt with round-2 tiers (Must 31, Should 4, Could 15, Won't 24) | R0.1; scope-1 |
| 39 | Cross-doc dependencies, risks and open questions rewritten; round 1's 7 open questions closed | consistency decision 34 |

## Changes in round 3

Requests are [`reconcile.md`](reconcile.md)'s "meta.md" table; rulings are [`RULINGS.md`](RULINGS.md) §8. Meta's
session total is unchanged at **31** (M2 19, M3 4, M5 1.5, M6 2.5, M7 2.5, M8 1.5): every change below is data, text
tiering or a clarification.

| Id | Outcome | Section | Note |
|---|---|---|---|
| META-01 | applied | §1.6.1, §4.4, §9.4, §15 | The PRIZES bits were already placed to venues_a §0.8 (Plant 4-7, Tomahawk 8-10, Knight 11) and PL0's tier A was already marked explorer-free and Should; round 3 answers venues_a's question 3: Knight **gets** its VENUE_REC (fastest Metal Metslime kill, Should), Plant gets none |
| META-02 | applied | §3.2, §4.3-§4.4, §1.6.1, §9.2.1 | Already: PERSIAN PALACE everywhere (no PRINCE OF PERSIA string left), Blizzard's 4 PRIZES bits only, fight ids `$0E` SHADOW ROCK, `$0F` GAMARN & GAMADAYU, `$10` DARUMA, tier B cited from venues_b §1.14/§2.12/§3.14/§4.13. Changed: YA0's tier A now names story's new draft riddle YA0.A (§7.1); the sekisho riddle stays retired |
| META-03 | applied | §9.0, §9.2.1, §1.6.1, §3.9, §15 | Fight record grows to **11 bytes**: +10 PINCH, copied by `fight_load` to RULESET +15 `RS_PINCH` (W2's SUPER copies 14, else 0 = the boss's default); explicit ids `$13-$17` with `$15` KAMEGORO MAKER MK-VI, and `$29` Doc Robot MK-VI (Should) with its kind-5 call; **no PRIZES bits** for fortress stages (bits 12-31 spare); H2/H4 doors read `CLOSED FOR RENOVATION` (story S26.4) while Should. HALFTIME RIOT was already the name everywhere (SEMIFINALIST is a rank title) |
| META-04 | applied | §4.2, §4.4, §4.5, v1.0 scope | v1.0 uses only `require` 2 and requirement hint **R2 JET** (Must); R1, R3, R5 are Should (R4 TAG already was); a release check fails on a predicate whose requirement hint is absent; new W3 row: its three hints are Should (no desk) |
| META-05 | applied | §1.6 RATEFLAGS, §6.1 T1, §7, §17 | fortress's "NO-CAPSULE" bit is RATEFLAGS b4 SOLO RIOT (R8.5), said at the field and at T1; R8.8 keeps RECORDS at 20 HoF and EXTRA CONFIG at the championship (§7 already had them), so open questions 2-3 are closed as the user's defaults |
| R8.1 | applied | §16 risk 1 | The slice risk now cites RULINGS §6's re-baselined M2 ≈ 53 (26 → 79) and M3 ≈ 44 (79 → ~123) instead of round 1's 45 and 25; systems' slice ≈ 28. Meta's own per-milestone figures are unchanged |
| R8.2 | applied | v1.0 scope (slice path), §15 tech row | The slice owns no forms; POWER/JET events stay at M5 (already); meta's slice code reads the stage record v0 from M2.1 (`SA.META`, `FLAGS1.REMATCH`), no stage-`$00` stop-gap |
| R8.4 | applied | §6.2, §12, §15 story row | The ENGRISH perfect line is story's S47.PE, a paraphrase of 4MI's line, never the quote (was "4MI's own line") |
| R8.6 | applied | §11.2, §3.8, §15 art_audio row | CASUAL's reflex ×2 excepts the quick-draw, which is 40 f (§11.1 already said 24 / 18 / 40 f); Eddie at the pit stop is new art, a composite; the rating screen draws over the judges' desk (§6.1 already) |
| R8.3, R8.5 (names), R8.7 | already | §11.1, §8, §9.2.1 | MMC5 AUDIO and ARRANGEMENTS were already Could with the MMC5 pulse driver (no SUPER-colour audio, no channel drop here); no panel strings, alias gag, S06 name or plates in this doc; INPUT LAG was already 0-6 f |
| — | applied | §4.5 heading, §15 story row | Cross-reference fixed: the generic lines are `story.md` §7.3 (§7.2 is the fortress stages' hints) |
| verify 1 | applied | v1.0 scope row 4, §15 tech row | `H_REMATCH` is the operand hook at `$3F:$F952` (the operand of `JSR $F527` at `$F951`), as §3.2 and `tech.md` §14.2 say; the two places that gave `$F951` are fixed |
| verify 2, verify 5 | applied | §6.1 T6 | Systems' typical v1.0 income is ≈ 1,905 (`systems.md` §7, with the Opening's extras), was ≈ 1,860 |
| verify 3 | applied | §4.2, §4.3, §4.4 | H5's b3 (Mr. X's card) has no debrief predicate or hint (`story.md` §7.2, `fortress.md` §4.5.3: T14's hint is Break Man's); the fortress hint ids are + 0-2; the release check also fails on a desk stage's predicate whose hint has no tier B string (the engine falls back only from A to B) |
| verify 4 | applied | §3.3, §3.7 | The POSTPONED node's line is story S09.2 (S14 is the Riot intro); game over's line follows S16's table: Kalinka's rotation, Mr. Y's S16.4 in H1-H5, Wily's S16.5 in W2-W3 |
