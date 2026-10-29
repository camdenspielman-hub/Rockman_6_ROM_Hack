# Rockman 6 GP: art and audio production plan (art_audio.md)

Owner: design-art-audio. Status: **round 2**, revised against [`RULINGS.md`](RULINGS.md), with every budget re-run
against the revised venue, fortress, systems, meta and tech docs (R5.3).

This doc plans every pixel and every note that GP adds to vanilla Rockman 6: where new art lives in CHR, what each stage
costs in tiles and frames, who makes it (with **no pixel artist**, R5.1), the style rules, the pipeline's art specs, and
the one track list with its byte budget (R5.2).

- **Binding order**: [`RULINGS.md`](RULINGS.md) first, then [`BRIEF.md`](BRIEF.md); the research in `docs/research/` wins
  on facts.
- **What this doc owns** (the single sources of truth): the **tile, byte and track budgets**, the style guide, the art
  inputs and checks of the pipeline, and **the one track list** (R5.2).
- **What it cites**:
  - `systems.md`: combat, economy and chips (chip list, GP-COMMON asks, the per-form `$71-$7F` map);
  - `meta.md`: save bytes, the bracket, events and the debrief (its screens' contents);
  - `tech.md`: ids, memory, raster, CHR limits, **the tileset-slot table** (§5.3) and the bank ledger (§1.2);
  - `venues_a.md`, `venues_b.md` and `fortress.md`: staging (what each stage shows);
  - `story.md`: every word and the ending.
- **Scratch and scripts** (run from the repo root with `python3 -I`):
  - round 1's measurements: `build/design/design-art-audio/` (`chrsets.py`, `chrfree.py`, `sprbudget.py`, `formdiff.py`,
    `flicker.py`, `songsizes.py` and others);
  - round 2: `build/revise/art_audio/`: `budget_r2.py` (**the art ledger**: every asset row with tiles, frames, tier
    and method; `--rows` lists them), `music_r2.py` (the track and SFX ledger), `art_audio_round1.md` (round 1's full
    text, for the designs this revision demotes).

**Tags** (BRIEF §8): **[engine-ok]** vanilla as-is or data only; **[new-code]**; **[new-art]**; **[new-music]**; size
**S / M / L**. **Tiers** (RULINGS §0): **Must** = v1.0, the tight Must; **Should** = v1.1+, re-added in R0.3's
cut-line order; **Could**; **Won't (v1)**. A Must depends only on Musts (R0.4).

**Method codes** (§11), the honest R5.1 count:

| Code | Method | R5.1 counts it as |
|---|---|---|
| **R** | reuse: a copy, recolour, crop or repack of vanilla RM6 tiles | reuse |
| **X** | composite: vanilla RM6 parts plus new pixels on each frame | reuse |
| **C** | programmatic: a generator script is the source | Claude |
| **D** | a Claude draft, **final** (a human pass is optional polish) | Claude |

Tile counts are 8×8 tiles (16 bytes each in CHR). "Frames" are metasprite frames. Vanilla screens are written **vNN**,
GP screens **NN**. Stage ids are tech's (R1.2) and venue names are R3.3's.

---

## v1.0 scope

**What ships in v1.0.** All art and audio that the v1.0 stages, menus and ending need (R0.2), and nothing they don't:

- **The 8 venues' cores** (homage mechanic, secret exit, hidden room, behaviour chip, boss rework; R0.2):
  - their new BG thirds;
  - their Must enemy sets, built as recolours and composites first (R5.1);
  - one pinch set per champion;
  - two **set-piece player sheets** (R2.3): SKY ACE's sortie and EDO NINJA ROW's pogo.
- **The non-venue stages**:
  - Opening-lite and HALFTIME RIOT on **TS_STADIUM**;
  - H1, H3 and H5 with the shared **MUSEUM** third;
  - W2 and W3 with the escape;
  - the ending in R4.1's order.
- **The bosses**:
  - Grand Pi-kun, the Yellow Devil, Gamma (head and fists) and WILY MACHINE 6.5, as **BG bosses at one size each**
    (R3.6, R5.1);
  - Bass β and the NPC Break Man, **composited from Rock's sheet** (R4.2, R5.1);
  - Dark Man and his 40-tile disguise with the **orange scarf**;
  - Big Eye, the Kamegoro Maker and the Trophy Dispenser (re-skins).
- **The UI**:
  - the title with the GP badge;
  - the file cards, the bracket, the judges' desk, the pit stop and the maps;
  - the 14 chip icons;
  - **16×16 face icons with name labels instead of portraits** (R5.1);
  - the 1-bpp glyph set (ALL CAPS EN, kana JP, R1.4);
  - GP-COMMON and the HUD labels.
- **The audio** (R5.2):
  - **G00-G04**;
  - **G27 WHISTLE**, the 2-second jingle;
  - **G37 LAST MATCH**, the lights-out arrangement on 2A03 stems;
  - 21 new SFX in the `$36` tail, plus 15 vanilla SFX reused;
  - the D9 mute mask is Must (tech builds it).

| | v1.0 (Must) | Should (v1.1+) | Could | Won't (v1) |
|---|---|---|---|---|
| **Art: CHR tiles** (BG + sprite) | **4,535** (2,567 + 1,968) + 240 1-bpp glyphs | 2,202 | 1,212 | 299 |
| Art: frames | **354** | 114 | 64 | 63 |
| Art: Claude sessions | **51.6** | 29.7 | 14.5 | 4.6 |
| Music: tracks / bytes | **7 / 3.7 KB** | 18 / 13.2 KB | 15 / 10.6 KB | 2 |
| SFX: new / bytes | **21 / 392 B** (+ 15 vanilla ids) | 35 / 0.9 KB | 7 / 0.2 KB | |
| Music + SFX sessions | **9** | 26.4 | 19.1 | 3 |
| **art_audio sessions** | **60.6** | 56.1 | 33.6 | |

The sources are `budget_r2.py` and `music_r2.py`. `tools/plan/tight.py` carries **art 51.6** and **music 9**, and
`tools/plan/tally.py` carries the four tiers of both. The pipeline tools are tech's sessions, not these:
`chr.py`, `sprites.py`, `palettes.py`, `artcheck.py`, `bgboss.py`, `mml.py` and the driver work (tech §6.7, §12).

**Against R5.1's target** (about 3,900 tiles, 350 frames, about 50 sessions):

- **Frames are on target**: 354.
- **Tiles are 4,535**, but 1,612 of them (36 %) are reuse or composites that cost little drawing:
  - `SET-PARADE`, Bass β's copied weapons and the W2 board's icon copies are pure copies;
  - the venue thirds take their vanilla parts first.
- **Drawn and generated tiles are 2,923**.
- **Sessions are 51.6**, within 2 of the target: composites of Capcom's frames are cheap (§11.4).
- The extra tiles are the honest cost of content that the rulings and the revised stage docs made Must after the
  target was set:
  - the behaviour chips' set pieces (the Daruma, the mouse room, the Centurion statues; R2.5);
  - the cultural fixes (T-MESA, the cactus walkers; R3.4);
  - the hidden rooms' tells (the seagull);
  - the HUD labels;
  - 22 face icons (88 tiles) in place of 12 portraits (192).

**If the ledger tightens** (R0.1): these art-side fallbacks keep every mechanic and recover about 4 sessions. Each one
lowers a look, not a feature. In order:

| # | Fallback | Saves |
|---|---|---|
| 1 | The T-SALOON third is built from the lodge woods and T-TOWN's interior pieces (64 tiles, not 96) | 0.4 |
| 2 | P-UNDER and P-CAVERN take 75 % vanilla pages | 0.3 |
| 3 | The pit stop is a text menu on the vanilla pause frame, with no counter art | 0.6 |
| 4 | The HoF map is drawn by meta's bracket node renderer on a plain frame | 0.5 |
| 5 | Dark Man's true form is a composite of the NPC Break Man with a new helmet (X), not a draft | 0.3 |
| 6 | The desk is drawn from the bracket frame with name plates | 0.5 |
| 7 | Plant keeps vanilla's canopy, and its tar and croc water are black tiles plus sprites (venues_a's own fallback) | 0.6 |
| 8 | The judges and lane props are recoloured Metalls | 0.4 |
| 9 | The CAPCOM TIMES headline is typed in the vanilla bold font, not redrawn | 0.5 |

**Milestones** (RULINGS §6). Approximate art + music sessions per milestone:

| M | Art | Music + SFX | What lands |
|---|---|---|---|
| M2 | 1.2 | 0 | the glyph set and window frame, GP-COMMON, the CHR round trip of every vanilla set (tech's tool, art's test data) |
| M3 | 0.1 | 0 | HUD labels; the first chip icons |
| **M4 ⛳⛳** | 6.2 | 4.5 | SUMMIT CLIMBER; title-lite, file cards, bracket, desk, pit stop and 4 chip icons; Kalinka's, Cossack's and Mr. Y's face icons; **G00 (title cut), G01, G02, G03** and 12 SFX. **The first art-acceptance gate** (§11.5) |
| M5 | 15.5 | 0 | Opening-lite (TS_STADIUM, Pi-kun at one size); PERSIAN PALACE, LOST JUNGLE, ATLANTIS RUINS, EDO NINJA ROW (with the pogo sheet); the title's split menu |
| **M6 ⛳** | 15.2 | 2.7 | HERO'S QUEST, HIGH NOON FRONTIER, SKY ACE (with the sortie sheet); HALFTIME RIOT (Bass β, the NPC Break Man, the rejects); the cast; the rest of the chip icons; **G04, G27** and 8 SFX |
| M7 | 10.4 | 0 | the MUSEUM third and the trophy theft's claw; H1, H3, H5 (the Yellow Devil, Gamma, Dark Man); the Super Rock sheet; the maps |
| **M8 ⛳** | 3 | 1.5 | W2, W3 and the escape; the ending pictures; the rating screen; **G37 LAST MATCH**; the fallback check of every Should cue |

**Every v1.0 art and audio item rests only on Must items** (R0.4):

| v1.0 item | Rests on (all Must) |
|---|---|
| New CHR anywhere | tech's CHR set table v2 (M2), `chr.py`, `sprites.py`, `palettes.py`, `artcheck.py` (M2) |
| BG bosses | `bgboss.py` (M7, before the H wings); `RL_FLOOR`, `RL_FLOOR8`; F-PIECES (tech M7) |
| Face icons in pop-ups | tech's glyph strip (§11.4: ≤ 24 glyphs + 4 icon tiles); text v1a |
| Set-piece player sheets, form swaps | tech's CHR stream (M2) and systems' `gp_player_sheet` (M3) |
| The title's menu | `RL_SPLIT_PT` (tech M5); until then a plain text menu (meta) |
| W2/W3 "SUPER colour" | palettes, `RL_PARALLAX`, `RL_PALBAND`; no ExGrafix (R1.3) |
| Every new track | D1, D2, D4, D6, D11 (tech M2), `mml.py`; every Should track has a vanilla fallback |
| G37 LAST MATCH | **D9 mute mask** (Must, R5.2, tech §12.6) |
| Must SFX | the `$36` tail, reserved for SFX (R1.14) |

**Not in v1.0** (kept below, each marked in place):

| Tier | Art and audio |
|---|---|
| **Should (v1.1+)** | Portraits and match-card portraits (§9.4); Grand Pi-kun's S and L sizes; THE APPROACH's drive-toward-camera sizes; the Break Man playable sheet (with the partner, R0.3 item 2); alt and synergy tiles (item 1); each venue's second-set-piece and arena-twist art (item 4); H2 and H4 with the Mecha Dragon and the Cossack Catcher (item 5); Doc Robot's Air Man; UMBRELLA MAN; the podium's all-eight BG row; G05-G13, G15, G16, G22-G26, G28, G38 RIOT; 35 SFX; D3, D10 |
| **Could** | W1 (TS_LAB, METALL 16, Enker) with ExGrafix in its locked rooms only (R1.3); the Exhibitions E1-E3 as single arenas (R3.7); the victory lap; the MMC5 voices (D5, D7, D8; G14x, G15x, G37x, G34, G35); G14, G17-G20, G29-G33; the attract crawl's pictures; the PART/booth bundle's icons; achievement plates; Mr. X's portrait |
| **Won't (v1)** | E4 Maze art and G21; Bass Mode's player sheet and G36; Mr. X Returns; the Museum's meters; Yamato's sekisho, passes, kites and hanabi (R3.2); DPCM drums (D12) and the PCM announcer (D13); 32 KB CHR-RAM; the extra 4 KB ExGrafix page (R1.3); the mixed-case EN font (R1.4) |

---

## 0. The plan in one page

| Question | Answer |
|---|---|
| Where does new art live? | In **tech's CHR source banks `$54-$61`** (14 banks; v1.0 fills about 9 with **70 KB**), never over Capcom art (BRIEF §7.4). The **1,126 blank tiles** in vanilla CHR banks' gaps (§1.3) stay a reserve |
| How does it reach the screen? | Through vanilla's **CHR set** mechanism, extended to tech's **set table v2** (8-bit source bank, **28 stage-local ids** per stage; tech §7.6, §2.1 here) |
| What limits a stage? | **256 BG tile ids live at once**, a **96-tile sprite enemy area** (`$1A00-$1FFF`) per screen, **two enemy sprite palettes**, and the **9-slot lag cap** (R1.8). Not ROM space. §2 and §3.5 ration them |
| How much new art? | **v1.0: 4,535 CHR tiles and 354 frames** (§13), plus 240 1-bpp text glyphs. All tiers: 7,949 tiles and 532 frames |
| Who draws it? | **Claude, with no pixel artist** (R5.1): 36 % reuse and composites of vanilla RM6 art, 11 % programmatic, 53 % Claude drafts that are final. One size per BG boss; face icons, not portraits; Bass β and Break Man from Rock's sheet; at most 8 frames per enemy and 16 per boss; an art-acceptance gate with screenshots at every milestone (§11) |
| Music? | Vanilla's 36 tracks stay. **v1.0: 7 new tracks (3.7 KB)**: G00-G04, G27 WHISTLE and G37 LAST MATCH, plus 21 new SFX in the `$36` tail. Should: 18 tracks with vanilla fallbacks. Could: 15, including the MMC5 voices. All tiers fit **tech's 5 music banks** `$75-$79` with room (§12) |
| The one technical bet | **8 KB CHR-RAM is the budget** (no extra page, R1.3). Pop-up glyphs, face icons, pinch sets, form swaps and set-piece sheets all stream through tech's one CHR stream (192 B a still frame, tech §15.3) |

---

## 1. Facts this plan stands on (measured)

All measured from `roms/rm6j.nes` and the shared savestates; scripts in `build/design/design-art-audio/`. The critics
re-checked the load-bearing ones (the form-sheet differences and the CHR set table format, feasibility review
"Strengths").

### 1.1 CHR-RAM layout during play [code][seen]

RM6 has **8 KB of CHR-RAM** and writes the CHR registers once (identity map). PPUCTRL is `$88` in stages: **BG uses
pattern table `$0000` (256 tiles), sprites use `$1000` (256 tiles), 8×8 sprites** (`rm6/levels.md` §6, confirmed in
every state sampled).

| Sprite tiles | Contents | Loaded by |
|---|---|---|
| `$00-$70` (113) | Rockman's sheet (normal form: set `$00`, bank `$00`) | stage start; the form sheets on a form change (§1.5) |
| `$71-$7F` (15) | **the slot set**: the equipped weapon's shot tiles, or the form sheet's own (systems §1.4) | weapon or form change |
| `$80-$9F` (32) | **common**: items, explosion, `READY` (`$99-$9D`), HUD pieces (set `$01`) | stage start |
| `$A0-$FF` (96) | **the enemy area**: per-screen enemy sets (16-96 tiles each), or one boss set | camera entering a screen (`$3A:$826F`, AI header byte AI-4) |

`resident.py` drew 73 states for 120 frames each: 111 of the player tiles and 21 of the 32 common tiles were drawn.
`$80`, `$86`, `$87`, `$8A`, `$8B`, `$8D` were never drawn (candidates for GP-COMMON, §2.4); `$99-$9D` are the `READY`
letters, drawn only at (re)spawn. tech's wider census (§7.6) found only 11 sprite tile ids never shown across 73 scenes:
**new enemies replace, they never add**.

**Sprite palettes** (`pals.py`, 6 states):

- palette 0 = Rockman (`0F 2C 11`, recoloured per weapon);
- palette 1 = `0F 20 37` (black / white / skin: Rockman's face, items, common sprites);
- palettes 2-3 = **the two enemy palettes of the screen**, written by the enemies' palette programs (`$C9EF`, which
  start at buffer index `$18`/`$19`).

Colour 1 of every sprite palette is black (`$0F`): the outline.

### 1.2 The CHR set table [code] (`chrsets.py`, output `chrsets.txt`)

- 256 entries of 4 bytes at `$37:$8000`: count, PPU address / 16, source offset / 16, flags (bit 7 = PPU `+$1000`,
  bits 1-6 = **8 KB source bank, so only banks `$00-$3F` are addressable**, bit 0 = source `+$1000`).
- **223 ids are used** (126 sprite sets, 97 BG sets). **33 ids look unused** (all `$00` or all `$FF`): `$7C-$7F`,
  `$DF-$FB`. Ids `$FC-$FF` are the debug sound player's font.
- BG stage sets are 256-tile bases (`$82`-`$C9`) plus "thirds" of 32-128 tiles swapped in by exits; tiny 4-8-tile sets
  animate torches, water and oil (`$9F-$A1`, `$AB-$B0`, `$D8-$DB`).
- **Boss sprite sets fill the enemy area** (`bossets.py`):

  | Champion | Set | Tiles |
  |---|---|---|
  | Blizzard | `$36` | 93 |
  | Wind | `$3F` | 96 |
  | Plant | `$45` | 85 |
  | Flame | `$43` | 73 |
  | Yamato | `$3E` | 96 |
  | Tomahawk | `$44` | 94 |
  | Knight | `$39` | 96 |
  | Centaur | `$46` | 73 |

  Only Flame and Centaur leave 23 tiles; Wind has 8 duplicate (flipped) tiles, the others 0-1. **New champion frames
  therefore cannot just be added** (§2.5), and a sprite face icon cannot share a boss room (consistency-14: icons are BG,
  §9.4).

### 1.3 Free tiles in vanilla CHR banks [code] (`chrfree.py`)

A tile is free if no CHR set reads it and it is blank.

| Banks | Free tiles | Notes |
|---|---|---|
| `$00`, `$03-$07`, `$09`, `$0A` (sprite art) | 830 | gaps between Capcom's sets, in runs of 16-96 (bank `$00` has one run of 96) |
| `$02`, `$08` | 62 | |
| `$17`, `$19`, `$1E`, `$1F` (BG art) | 234 | `$1E` has a run of 78, `$1F` a run of 128 |
| `$10-$16`, `$18`, `$1A-$1D` | 0 | full |
| **Total outside `$0B-$0F`** | **1,126** | 4MI's "fill the gaps" (r4mi/graphics.md §4) |
| `$0B-$0F` | 2,548 | the 40 KB of free ROM; tech's ledger makes them text banks T5-T9 (tech §1.2) |

### 1.4 How much room a screen leaves [code] (`sprbudget.py`, `scenes.py`)

**Sprite enemy area, per vanilla screen** (the union of the sets its objects and exits queue):

| Stage | Median free of 96 | Min free | Screens with ≥ 32 free |
|---|---|---|---|
| Blizzard | 64 | 0 (boss) | 20 / 25 |
| Wind | 67 | 41 | 22 / 22 |
| Plant | 62 | 16 | 21 / 24 |
| Flame | 64 | 36 | 24 / 24 |
| Yamato | 68 | 0 (Gamadayu, boss) | 24 / 30 |
| Tomahawk | 64 | 9 | 28 / 31 |
| Knight | 87 | 0 (boss) | 25 / 26 |
| Centaur | 75 | 0 (boss) | 25 / 26 |
| Mr. X 1-4, Wily 1-4 | 53-93 | 0-37 | |

Vanilla already has **sprite-set conflicts** on four screens (Tomahawk 04 `$09/$61`, 15 `$32/$61`; Wily 1 15 `$42/$61`,
16 `$08/$61`): the `$61` preload of a boss corridor overlaps an enemy set. They are harmless only because the enemies
are gone by then. GP's build checks this automatically (§10.5; tech §7.6).

**BG tiles**: a venue uses 229-256 of its 256 ids over all its CHR states (`rm6/SUMMARY.md` §2), but **one screen
references far fewer**: a boss room 52-195 (Blizzard's 89, Mr. X 2's 52, Wily 1's 195), the stage select 190, the title
252 (`scenes.py`). That is why boss rooms always have room for a pop-up's 28-id strip (tech §11.4).

**Title screen**: 252 BG tiles in use: 142 logo, 90 moon, 16 menu text (`title.py`). 251 sprite tiles are free.

### 1.5 The form sheets [code] (`formdiff.py`; systems §1.3)

The pause menu loads a form's sheet from `$38:$96C7` = `00 02 03`: **sets `$02` (Jet) and `$03` (Power), 128 tiles each
in bank `$00`** (systems' round-2 reading). They differ from the normal sheet in **119 of 128 positions** (104 in
`$00-$70`, all 15 in `$71-$7F`); round 1's scan of the 128-tile sets `$04-$07` in bank `$01` found the same picture
(109-114 tiles absent from the normal sheet). Either way **a form swap streams the whole 2 KB sheet** (2,048 B). At
tech's rates (§2.6) that is **11 frames standing still, about 13 walking, at most 22** with a column every frame, so
systems' **fixed 16-frame swap behind the flash** holds (R2.3, feasibility-7, consistency-5).

### 1.6 Flicker baseline [seen] (`flicker.py`, 240 frames per state, Rockman running and firing)

| State | Max sprites on a line | Frames with > 8 on a line | Max OAM entries |
|---|---|---|---|
| Blizzard start, Plant cp1, Knight cp1 | 6-8 | 0 % | 18-41 |
| Flame, Knight, Centaur boss | 8 | 0 % | 38-46 |
| Blizzard boss | 9 | 56 % | 44 |
| Mr. X 1 / Mr. X 3 / Wily 2 boss | 9-10 | 5-6 % | 36-60 |
| Wily 1 boss (Mechazaurus) | 11 | 21 % | 64 |
| Wily 3 Plant Man refight | 13 | 71 % | 54 |

Vanilla RM6 is **clean in stages and flickers in a few boss rooms**. OAM order is reversed on odd frames (`$07D9`,
`rm6/engine.md` §1.5), so overflow becomes 30 Hz flicker. CX's median state drops sprites in 22 % of samples
(cx/graphics.md §9). GP's budget (§3.4) sits between the two.

### 1.7 Sound [code] (`songsizes.py`, driver facts from `rm6/engine.md` §5)

| Measure | Value |
|---|---|
| Track ids | 102 (`$34:$8A40`); `$00-$22` + `$39` music (36), `$23-$65` SFX (66) |
| Music data | **18,788 B**; stage themes `$00-$07` 617-1,238 B (mean 1,010); Mr. X / Wily stage 788 / 871; boss `$0C` 633; Wily Machine `$18` 575; jingles 116-260; ending scenes 349-546 |
| SFX data | 1,940 B, mean 29 B per effect |
| Free | **449 B** (bank `$36` tail, reserved for SFX by R1.14). `$1A` is an empty stub; SFX `$3D/$3E/$4D/$51` look unused |
| Channels | pulse 1, pulse 2, triangle, noise. **No DPCM**. SFX steal music channels |
| Instruments | table at `$8B0F` (pointer at `$34:$8A41`), 8 bytes each; 71 fit before the first song (`$8D47`) |
| Command set | `$00-$18` decoded (notes ≥ `$20`: 3-bit length index + 5-bit pitch); MML-like |
| Lag | the driver runs in NMI (or the IRQ), so **music keeps tempo during lag** |

---

## 2. Asset architecture: how 512 live tiles carry a 15-stage game

### 2.1 CHR set table v2 [new-code] S · Must (tech §7.6 builds it, M2)

Vanilla's 6-bit source bank cannot reach GP's CHR banks (`$54-$61`, tech §1.2), so **no new art reaches the screen until
v2 exists** (R1.13, scope-6). tech schedules it at M2, before any new art. The format, specified here with tech:

- **Global ids `$00-$DE`**: vanilla's sets, unchanged, plus GP globals in the free ids `$7C-$7F` and `$DF` (5 ids):
  - GP-COMMON (§2.4);
  - the text-window frame;
  - the swap flash;
  - two spares.
- **Stage-local ids `$E0-$FB`** (28 per stage), resolved through the table that the stage-attribute record's
  `SA.LOCAL_CHR` points to. A byte in an AI header (AI-4), an exit or a checkpoint (`$0685`) that names `$E0+n` means "this
  stage's set n". Each stage therefore has 28 ids for its thirds, sprite sets, pinch sets and animation frames. Every
  one-byte format stays one byte.
- **Entry v2**: 5 bytes: count, PPU / 16, source offset / 16, **source bank (8 bits)**, and flags (b7 PPU `+$1000`,
  b0 source `+$1000`). The loader `$C95C` reads v2 entries for local ids and for any global id whose v1 entry carries the
  escape pattern; vanilla's 4-byte entries keep working.

### 2.2 The tileset-slot table (regenerated from tech §5.3) [new-code] S · Must

**tech owns the table** (R1.10; scope-11, consistency-9, feasibility-17). Its model is a RAM image with **2 slots per ROM
bank, each with its own alternate set** and T6 table. Round 1's rule "two alternate-heavy stages must not share a bank"
retires, and so does round 1's 10-bank, 3-slot plan. This doc lists **content and block counts only**.

A slot is 5 metatile pages + 4 block pages (2,304 B); its alternate set (1,280 B) holds breakables, toggling floors,
pressure plates, T6 variants and Power blocks. The loader copies the slot to `$8000` or `$8900` of the TILES page and
its alternate set to `$9B00`, where the vanilla readers expect them. **The CHR thirds of §4-§5 are CHR sets** (§2.1),
not slots: the MUSEUM third, for instance, is one set shared by three slots.

| Bank (tech) | Slot 0: content, vanilla blocks used / 256 | Slot 1: content, vanilla blocks used / 256 | Alternate-set users | Tier |
|---|---|---|---|---|
| `$62` | **Blizzard**, from `$2E:$80`: 255 (the GP layout's reclaimed ids hold the T6 ice-cell variants) | **Wind**, from `$2C:$80`: 232 (24 free + reclaimed; lamp board by `map_set`) | ice cells (T6); none | Must |
| `$63` | **Plant**, from `$2E:$92`: 255 (rebuilt from the GP layout: the second gorilla room and half the lodge go) | **Flame**, from `$2F:$80`: 254 | tar pits (`alt_flip`); plates, oil ignition, loose tiles | Must |
| `$64` | **Yamato**, from `$2E:$89`: 255 (the cut sekisho and kite screens free ids, R3.2) | **Tomahawk**, from `$2C:$89`: 221 (35 free) | the crest cell (T6); gallery windows, the outhouse door | Must |
| `$65` | **Knight**, from `$2D:$80`: 255 blocks but only 155 metatiles (room for 100 new ones) | **Centaur**, from `$2D:$89`: 250 | trapdoor, hidden stairs; zone doors | Must |
| `$66` | **TS_STADIUM**, new (about 160 blocks): the Opening, the HALFTIME RIOT, the lap (Could) and the lobby screen `$1D` (Could) | **H1**, from Wily 2's `$2A:$89`: about 190 | scoreboard and jumbotron by `map_set`; appearing blocks (`alt_flip`), F-PIECES | Must |
| `$67` | **H3**, from Mr. X 3's `$2F:$92`: 255 (the Metonger Z tank's blocks are freed for Gamma) | **H5**, from Mr. X 4's `$2B:$80`: 159 | presses; crystals | Must |
| `$68` | **W2**, from Wily 3's `$2A:$92`: about 160 | **W3**, from Wily 4's `$2B:$89`: 177, plus the escape's crumbling ladders | none; crumbling ladders (T6) | Must |
| `$69` | H2, from Wily 1's `$2A:$80` | H4, from Mr. X 2's `$2F:$89` | Heat blocks, force beams; conveyors | Should |
| `$6A` | TS_LAB (W1, the escape's eras) | TS_ARCADE (E1-E3, one CHR third each) | palette blocks; the arena grids by `map_set` | Could |
| `$6B-$6E` | the 8 venues' second slots, reached by the section switch | | | Should |

**v1.0 uses 14 slots in 7 banks** (`$62-$68`); the full design uses 26 in 13. The empty vanilla tileset pages `$2B:$9200`
and `$2D:$9200` are **not** used (round 1 put the lap and the lobby there; both now live on TS_STADIUM, consistency-31);
tech keeps them as allocator seeds. Vanilla's own tileset banks `$2A-$2F` stay untouched for the legacy ids.

**Section switch** [new-code] S · **Should** (tech §5.4): an exit may move the stage's metatile and block pages to slot B,
as an exit changes the CHR set. No v1.0 stage needs more than 32 screens or more than 256 blocks.

### 2.3 BG tiles: thirds, not additions

Every stage follows the same rule:

1. A venue's **base set** is vanilla's 256-tile set, kept.
2. New art arrives as **thirds** (`$0000-$03FF`, `$0400-$07FF`, `$0A00-$0FFF` and similar 32-128-tile ranges). An exit's
   CHR byte swaps a third in over art the next screens do not show, exactly as vanilla's `$91`/`$95`/`$98` do.
3. The build proves each swap safe: for every screen and its scroll neighbours, every BG id referenced must be present
   after the swap (§10.5, the **free-id map**; tech §6.3).
4. Animated BG tiles (wheels, rain, water, torches, the crowd) are 4-8-tile local sets cycled by a thread, vanilla's
   torch technique (`$39:$888A`).
5. **Reuse first** (R5.1). A third's contents are taken from vanilla pages wherever they exist (4MI: "every tile set is
   just a list of pages", r4mi/graphics.md §8). Examples: Plant's lodge logs for Blizzard's summit lodge; the `$96`/`$84`
   caves and `$AA` water for Plant's caverns; Knight's torches for Flame's dungeon; the `$94` mesas at noon for
   T-MESA; Mr. X 1's night skyline and moon behind the stadium. The ledger counts those tiles as R (§11).

Non-venue stages get **new 256-tile bases** (TS_STADIUM) or copies of the legacy fortress bases (H1-W3), plus thirds.

### 2.4 Sprites: the enemy area, GP-COMMON, the slot set and the set-piece sheets

- **Enemy area** (`$A0-$FF`): each enemy type's AI header names its set (AI-4); sets sit at fixed PPU addresses.
  **Rule**: a new enemy set is 16, 32 or 48 tiles (a boss set up to 96), aligned to 16. The build rejects a screen whose
  sets overlap (§10.5; tech §7.6). §4 places every venue's sets.
- **GP-COMMON** (global id `$7C`) replaces set `$01` with a copy that keeps every vanilla tile and fills the 6 never-drawn
  slots, after the OAM census confirms them (§10.6). The contents are systems' asks:

  | Slots | Tile | Notes |
  |---|---|---|
  | 3 | **W**, **K**, **!** | `WEAK!` uses READY's **E** and **A** (`$99-$9D`). The pop is tech's family `$FD` sub-id (consistency-24) |
  | 1 | the **swap flash** | drawn 4-way mirrored as a 16×16 burst, sprite palette 0 (systems §1.3) |
  | 1 | the **CENTURION** helper | systems §9.2 bit 12 |
  | 1 | spare | `?!` needs 2 (with SC3, Could); a second spare must come from the census |

  `CRIT!` is gone (criticals are Won't, R2.4). The low-fuel pip is Should (systems).
- **The slot set** (`$71-$7F`, 15 tiles): **one owner at a time, per form** (R2.3; systems §1.4 owns the map):

  | Form (sheet) | `$71-$7F` with slot 0 equipped | with weapon w equipped |
  |---|---|---|
  | NORMAL (set `$00`), JET (`$02`), POWER (`$03`) | the sheet's own slot tiles (buster pellets, charge, fist) | weapon w's set |
  | **SUPER** (new sheet, §7.1) | the Super sheet's own: tap fist and rocket fist, **≤ 15 tiles** | weapon w's set |
  | a set-piece sheet | the sheet's own buster tiles | none: buster only |
  | Break Man (Should) | his shot tiles | none: buster only |

  The weapon sets and their free tiles (15 − size), from systems' verified table: Y.SPEAR 2 (13 free); W.STORM 15 (0);
  **B.ATTACK 3 + the Ice Block's 4 = 7 at `$73-$79`** (8 free; the one v1.0 alt, R2.4); F.BLAST 9 (6); PLANT.B 1 (14);
  KNIGHT.C 2 (13); SILVER.T 5 (10); C.FLASH 0 (15); BEAT `$29` 15 (0); **M.BEAM ≤ 15** (its beam and build tiles, new,
  Must). The Should alts and synergies fit those free counts. A synergy names one combined set per (form, weapon) pair,
  ≤ 15 tiles (Burning Knuckle = F.BLAST's 9 + ≤ 6). W.STORM's Updraft and Tailwind must re-pack the tornado set.
  **artcheck rejects any slot set over 15 tiles** and any non-weapon object that draws from `$71-$7F` (R2.3,
  feasibility-8).
- **Set-piece player sheets** (R2.3, feasibility-8). A set piece that changes Rock's body uses a **dedicated 128-tile
  sheet** (`$00-$70` poses + `$71-$7F` its own buster), streamed like a form swap at a locked moment
  (`gp_player_sheet(id)`, systems §1.4). Never the slot set. While a sheet is active only the buster fires and the form
  cycle is off.

  | Sheet | Built from | New tiles | Streamed during | Tier |
  |---|---|---|---|---|
  | **SKY ACE sortie** | the Jet sheet: flight banks L / level / R, 4 loop frames, the RENTAL bib variant | ~24 | the catapult's 60-f cut | Must |
  | **EDO NINJA ROW pogo** | the normal sheet + 2 pogo frames | ~8 | the rack's 24-f take animation | Must |
  | LOST JUNGLE swing poses | the normal sheet + swing frames | ~12 | the 00 → 01 transition | Should |
  | Eggplant-Rock (Centaur's curse) | the normal sheet re-skinned | ~12 | the curse's 20-f puff | Could |

  **Vines, the balloon and the condor carry use vanilla's ladder-climb and ladder-shoot poses** (venues_a §0.7,
  venues_b §1.8): no sheet, and only the buster fires while hanging (consistency-43). Round 1's 12-tile vine set and the
  2 condor-carry tiles are dropped.
- **Player area** (`$00-$70`): the vanilla sheet, untouched. Super Rock and Break Man are whole replacement sheets (§7.1).

### 2.5 Bosses: pinch sets, streamed during an invincible beat [new-code] S · Must

A champion's boss set fills the enemy area (§1.2). New frames go into a **pinch set** of 12-24 tiles that **replaces the
frames the champion no longer needs in that phase**:

- the pinches: Plant's bloom, Blizzard's skis-off, Yamato's flying kabuto;
- the weak reactions (systems SC9).

It streams during an invincible animation that already exists in each design: Plant's 30-f bloom, Knight's ENRAGED log
line, Tomahawk's SHOWDOWN bow. At tech's 192 B per still frame a 24-tile pinch set streams in 2 frames.

**Each champion's GP boss set is rebuilt**: a copy of the vanilla set, with the dropped frames removed and projectiles
first, so that phase 1 fits in 96 tiles and phase 2 = phase 1 − dropped + pinch set. Own-weapon jokes (SC4) are
Should, and so are their frames.

### 2.6 The VBlank streaming budget (tech §15.3's rates)

tech's one CHR stream (an unrolled copier in ROM bank `$46`, a 256-B staging buffer in WORK, one stream at a time from an
8-entry queue, R1.6) moves **192 B on a still frame, 96 B with a column paint, 32 B with a full VRAM buffer**. 256 B
needs an 8-line blank band at the top (Could, the M1 spike's test 5).

| Stream | Bytes | Frames still / walking | When it plays |
|---|---|---|---|
| Form swap (whole sheet, §1.5) | 2,048 | 11 / ≈ 13 (≤ 22) | SELECT swap; systems' fixed 16-f swap behind the flash |
| The slot set after a swap or weapon change | ≤ 240 | 2 / 3 | queued after the sheet; B ignored until it lands |
| Set-piece player sheet | 2,048 | 11 | a locked moment (catapult 60 f, rack 24 f) |
| Super Rock sheet | 2,048 | 11 | a form swap into SUPER |
| Break Man sheet (Should) | 2,048 | 11 | behind his beam-in |
| Beat's set `$29` | 240 | 2 | the pit rescue's locked moment |
| Champion pinch set | 192-384 | 1-2 | the invincible pinch beat |
| **Pop-up strip**: ≤ 24 glyphs + 4 face-icon tiles (§9.4, §9.6) | ≤ 448 | 3 | before the window opens |
| Dialogue strip: ≤ 96 glyph ids | ≤ 1,536 | 8 | the frozen view |
| Restore of borrowed BG tiles from ROM (R1.4) | ≤ 1,536 | 8-12 | as the dialogue closes |
| BG-boss art | up to 3,200 | — | at room entry, with the screen off (one size each, so no poses stream in play in v1.0) |

### 2.7 MMC5 extended attributes (ExGrafix) [new-code] M · Could, with W1 only (R1.3)

ExRAM stays in **mode 0** (the text window's nametable) **for the whole game** (R1.3; the blocker feasibility-1 /
consistency-1). So:

- **No ExGrafix in W2, W3 or the escape**, and **no extra 4 KB CHR page**: with 8 KB CHR-RAM the page bits reach only
  the two pattern tables (the feasibility critic's probe `exgfx.nes`).
- **v1.0's "SUPER colour"** in W2, W3 and the escape is richer per-screen palettes, raster palette and parallax bands
  (`RL_PALBAND`, `RL_PARALLAX`), and the music (§12).
- **ExGrafix is Could**, only in W1's locked, text-free 16-bit rooms and the METALL 16 arena:
  - filled in mode 2 while the screen is blank, then mode 1, with the announcer held (tech §3.3);
  - its data is one extended-attribute byte **per metatile per tileset** (≈ 1 KB for TS_LAB, R1.5), never per screen;
  - the per-tile palette works with 8 KB CHR-RAM on FCEUmm (the feasibility probe). Mesen is checked by the go/no-go
    spike.
- **Also Could**: the castle picture's ExGrafix "bloom" at the unmasking (fortress §4.6 step 8). It is static and
  shows no text.
- If W1 ships without ExGrafix, its 16-bit section is a palette upgrade plus the MMC5 voices, which already sell the
  joke.

### 2.8 Pattern-table split (BG from `$1000` below a line) [new-code] S · Must (tech `RL_SPLIT_PT`, M5)

A mid-frame PPUCTRL write (bit 4) makes the BG rows below a scanline read **the sprite pattern table**. On menu screens the
sprite table is 80-100 % free (`rm6/text.md` §7), so:

- the **title** keeps the vanilla logo and moon (232 tiles) in `$0000` and draws its menu from a font in `$1000`, below
  line 112 (§9.1). The moon's rows below the split are duplicated into `$1000` too (≈ 60 tiles; the title's sprite table
  has 251 free). Until M5 the slice's title uses a plain text menu (meta §2.1);
- the **bracket**, **judges' desk** and **pit stop** get a second 256-tile page for their lower panels;
- it is one band in tech's raster list (`RL_SPLIT_PT`) and is never used in stages, where the sprite table is busy.

---

## 3. Style guide

### 3.1 The house style

- **RM6's Capcom house style, always.** That means thick black outlines (sprite colour 1 is `$0F`), 3-colour sprites
  with one light highlight, 16×16 metatiles and chunky, readable silhouettes. A new enemy should be impossible to tell
  from Capcom's at a glance (4MI's standard, r4mi/graphics.md §8). With no artist (§11), **the surest way to meet it is to
  start from Capcom's own pixels**: recolours and composites of RM6 sprites before any fresh drawing (R5.1).
- **Homage by rules and silhouette, never by logo** (BRIEF §6, R3.3). The venues *quote the look* of their games at
  Rockman's scale (CX's SMB stage, cx/graphics.md §7).
  - No trademark logos, no title-screen lettering of other games, and **no third-party names or characters on screen**.
  - Plaques and signs *describe* (R3.3). Asset names like `P-PITFALL` are internal ids that never reach the screen.
  - Capcom's own marks may be nodded to (1943, Gun.Smoke, DuckTales).
- **One exception per stage may break the house style on purpose**, as a joke the art carries (CX lesson 6): Plant's
  2600-style canopy (fat pixels, 2 colours), the castle picture's four greens, the ending's pixelation. Could: W1's Game
  Boy tier.
- **Cultural rules are Must** (R3.4):
  - HIGH NOON MESA has no graves, and no totem enemy appears (the `$12` walkers become cacti);
  - PERSIAN PALACE shows domes and a full moon, with no minarets and no crescent;
  - the vizier exists only as an obvious Wily in costume (Should);
  - Tomahawk Man's pinch frames show a rodeo showman's etiquette bow, not a stoic.

### 3.2 Palettes

| Rule | Detail |
|---|---|
| Sprite palette 0 | Rockman, recoloured per weapon (vanilla). Super Rock and Break Man get their own palette 0 when played |
| Sprite palette 1 | `0F 20 37` (black / white / skin) is **shared**: Rockman's face, items, GP-COMMON. Never change it per stage |
| Sprite palettes 2-3 | **The screen's two enemy palettes.** Every new enemy is drawn to use **one** of them plus palette 1. Two enemy types on one screen may not need two different palette-2 programs; the build checks this exactly like CHR overlap (§10.5). **A scene can show at most two sprite characters with their own colours** besides Rock (this is why the podium shows the champions in pairs, §3.5) |
| Boss | A boss owns palettes 2 and 3 (vanilla). A weakness flash is 2 frames of white, at most once per 90 f (systems §5) |
| BG | 4 palettes, colour 0 shared (`$0F` in nearly every vanilla stage). A stage's identity comes from palette first: re-use vanilla tiles under a new palette before drawing new ones (4MI's dusk city) |
| Palette tricks to use | dusk and night variants of vanilla sets (Tomahawk's sunset program already cycles; the Riot's NIGHT / BLACKOUT / FIRE); C.FLASH's "lights a dark room" fade; Shadow Rock as Rockman in a dark palette; **Dark Man's disguise as the NPC Break Man with an orange scarf** (fortress's one tell, consistency-8); Mr. Y as Mr. X with a moustache (§7.3); W2/W3's SUPER palettes and the escape's SUPER → NES → greens ramp (R1.3); the castle picture's green → NES → SUPER ramp |
| **Flashes (R3.5)** | In the default FLASHES mode **no effect flashes a large area more than 3 times per second**. **REDUCED turns every flash into a fade** (8 frames, tech §8.5's `pal_flash` service, which rate-limits every flash in one place). A health notice shows at boot (meta §2.1). Round 1's rule ("never repeat faster than every 6 frames", which allowed 10 per second) is withdrawn |

**The flash audit of art-owned effects** (each stage owner audits its own set pieces; fortress §0.9 and the venue docs
have theirs):

| Effect | Rate in the default mode | REDUCED |
|---|---|---|
| WEAK! boss flash (2 f white) | ≤ 1 per 90 f | off (the shake stays) |
| Crowd tiles (2 frames, every 16 f) | not a flash: both frames keep the same mean brightness (a build check on the two CHR frames) | unchanged |
| Pi-kun's 16-BIT EDITION pinch | one palette change | a fade |
| Ramps: the castle picture, the pixelation, the escape's downgrade | 8-f steps that never return to a previous state (a ramp, not a strobe) | 16-f steps |
| LIGHTS OUT's floodlight towers | one palette step per tower, ≥ 1 s apart | unchanged |
| Bass β's leaving beam | a palette cycle ≤ 3 changes per second | a single colour |
| The escape's `TIME!` | one red flash | a fade |

### 3.3 Sizes

| Kind | Size | Hardware sprites | Example |
|---|---|---|---|
| Small enemy | 16×16 | 4 | seal-bot, Metslime, scorpion |
| Standard enemy | 16×24 to 24×24 | 6-9 | guard-bot, outlaw, VENDING MAN |
| Large enemy | 32×32 max | ≤ 16 | Sidewinder on his horse, the condor |
| Robot Master scale (champions, Bass β, Dark Man, the NPC Break Man) | 24×24 to 32×32 | 9-14 | as vanilla |
| Anything bigger | **BG art** + sprite parts; **one size per BG boss** (R5.1) | parts ≤ 12 | Grand Pi-kun, the Yellow Devil, Gamma, WILY MACHINE 6.5 |
| **Face icon** | 16×16 = **4 BG tiles** inside a text strip (R5.1; a sprite copy only on menu screens) | 0 (BG) | the 7 speakers, Rock, Bass β, Eddie, the 8 champions |
| Chip icon | 16×16 sprite | 4 tiles | the 14 v1.0 chips |
| Portrait (Should) | 32×32 BG | 16 tiles | the speakers, the match cards |

**Frame caps** (R5.1): **at most 8 frames per enemy and 16 per boss**; the ledger rejects a row above the cap. **Widths
matter more than heights**: the limit is 8 sprites per scanline, and a 32-px-wide enemy uses 4 of them.

### 3.4 Flicker budget

| Context | Max sprites on any line | Frames with a line over 8 | How |
|---|---|---|---|
| Venue stages | **≤ 8 on 95 % of frames** | ≤ 5 % | at most two 32-px-wide objects side by side; repeated hazards are BG tiles, not sprites (CX lesson 5); bullets 8 px wide |
| Set pieces (sortie, train, gallery, parade) | ≤ 10 | ≤ 15 % | wave directors space enemies vertically by data; the build's flicker simulator (§10.5) runs each wave |
| Boss fights | ≤ 10 | ≤ 25 % | vanilla peaks at 9-11; the HUD bars cost 2 per line |
| Menus and cutscenes | ≤ 8 | 0 % | figures in a row are staggered by ≥ 8 px in height once they would pass 8 on a line |
| HUD widgets (tech §7.13) | ≤ 6 of their own on one line | | ≤ 4 widgets, ≤ 12 sprites |

### 3.5 Lag and flicker of the art-heavy scenes (R1.8)

The lag cap is **9 occupied slots**, every slot counted (R1.8): the player, the screen script, the text runner, shots,
utilities, directors not folded into the script, enemies, enemy shots and effects (tech §15.1). The stage docs own each
screen's count and recounted every set piece in round 2. This table re-checks the scenes where **art** decides the cost
(sizes, palettes, sprites vs BG) against both caps:

| Scene (owner) | Occupied slots, worst case | Sprites on a line | Art's rule |
|---|---|---|---|
| SKY ACE sortie 01 (venues_a) | Rock + script + 3 shots + ≤ 4 enemy-side = **9** | ≤ 3 fighters (2 wide) in any 8-px band + Rock + shots ≤ 10 | AYACO (48 px = 6 sprites) flies with at most one fighter on its lines; explosions use the common row |
| HIGH NOON train (venues_a) | Rock + script + 3 shots + ≤ 4 enemy-side (1 robber) = **9** | Sidewinder 32 px (4) + Rock + 1 outlaw ≤ 10 | the tunnel wall is a sprite only while it passes; the rails are BG |
| SUMMIT CLIMBER boss (venues_b's flicker request) | Rock + script + Blizzard Man + ≤ 3 flakes + 3 shots (the Ice Block is one) = **9** | vanilla: 9 on a line in 56 % of frames | FLAKES spaces flakes ≥ 16 px apart in height; the slush puddle (MELT) is BG; the skis-off frames are 24 px wide. The simulator runs FLAKES with an Ice Block out; if it fails the boss budget, FLAKES drops one flake while an Ice Block exists (an AI rule; venues_b decides) |
| HALFTIME RIOT, Bass β duel 1 (fortress) | Rock + script + Bass + ≤ 3 flakes (the B.ATTACK copy) + 3 shots = **9** | Bass 24 px (3) + flakes 8 px | his 4 pre-drawn copies are 8-16 px wide |
| Grand Pi-kun (BG boss) | Rock + script + the controller + 2 shockwaves or 2 confetti bursts + 3 shots = **8** | the body is BG; valve 16 px | one size: no size streaming |
| Yellow Devil, Gamma (BG bosses) | Rock + script + the controller + 1 flying piece or 2 fists + 3 shots ≤ **8** | 2 fists (3 wide each) + Rock (2-3) = 8-9 | fists are 24 px; the head and body are BG |
| The parade (Opening 07-0A) | float + champion + glove + Rock + script + runner + 3 shots = **9** | the 48×16 deck (6) shares its lines only with Rock | one float per screen (fortress), so one champion palette per screen |
| **The podium** (ending scene 5) | 8 champions + Rock + Bass + script + runner = **12: over the cap**; 8 champion palettes cannot exist (§3.2) | 8 figures in a row ≈ 24 | **Art's recommendation** (a request to fortress, §15): **the champions applaud in pairs**, one pair at a time beside the podium (2 s each; SET-PARADE, two enemy palettes per pair, 0 new tiles): **6 slots**. Should: all eight at once as a **BG applause row** (SET-PARADE converted to BG in 3 BG palettes, 112 tiles) |
| LIGHTS OUT (S42) | Rock, Light, Roll, Rush, Beat + script + runner = **7** | 5 figures: staggered in two rows ≤ 8 | Light in palette 1, Roll and Rush in palette 2, Beat in 3, Rock in 0 |
| S40 catch, the arrest | 3 figures + script + runner = **5** | 3 × 24 px = 9 if level | stagger by 8 px (Wily kneels: the vanilla kneel pose) |
| W2's bracket board | 0 (BG) | 0 | face icons and weapon icons are BG copies |
| The credits' room segments (fortress §6.2) | the boss + its shots + script (no player) | the boss's own caps | |

### 3.6 Text and UI look

- **One text model** (R1.4): a fixed-cell glyph cache, **EN in ALL CAPS** (round 1's mixed-case set is dropped,
  consistency-3), **JP in kana** with precomposed voiced kana, and no VWF. Glyphs are 1-bpp in a text bank, rendered at
  open time in the window's two colours (tech §11.4). The art is the glyph set of §9.6.
- **The window**: black, with a white 1-px frame (7 tiles: corners, edges, blank). Knight's command window uses the same
  frame. A pop-up is 2 × 28 cells with the 16×16 face icon in columns 0-1. Dialogue, debrief and help pages are 4 × 28.
- **Status labels** are 4-tile condensed words (4MI's curse labels), generated from the font (C): `ACE`, `ZONE`, `KEYS`,
  `BOUNTY`, `BALLS`, `TIME!`, `+30 INJURY TIME`. They are drawn by tech's HUD widget module (LABEL kind).
- **Menus** keep vanilla's blue frame tiles and caps font; GP adds only the letters each screen lacks (4MI's title rule).
  Numbers on the scorecard and bolts use vanilla's digit tiles.

---

## 4. Per-venue art budget

The venue docs own *what* each venue shows (`venues_a.md` §1.1/§2.1/§3.1/§4.1 and `venues_b.md` §1.8/§2.6/§3.8/§4.7,
both revised for round 2 with change lists for this re-run). This section turns their lists into a budget the build can
enforce:

- **kept vanilla CHR**;
- **new BG thirds**, with their tiles, ids and screens;
- **sprite sets with their enemy-area placement**, so no two sets that share a screen overlap;
- frames, the champion's pinch set, and the conflicts to respect.

Every row names its **method** (R, X, C or D; §11) and its tier. The rows are `budget_r2.py`'s.

**Enemy-area notation**: `A0+32` = a set of 32 tiles at sprite tiles `$A0-$BF`. Vanilla enemy sets keep their vanilla
addresses (`enemysets.py`). A venue's new sets are stage-local ids `$E0+` (§2.1). "Conflicts with" names the vanilla sets
whose tiles overlap: **those enemies may not share a screen** with the new set (a build check, §10.5).

**Common to all eight** (Must):

- a **tileset slot** from tech's table (§2.2), starting as a byte copy of the venue's vanilla tables, so every vanilla
  block and metatile stays available. New blocks go into the ids the GP layout no longer uses (`levels.py` lists the ids
  a layout references; the rebuild drops the rest);
- a **rebuilt champion boss set** plus a **pinch set** (§2.5);
- the venue's **secret arena = the boss room with a new palette** (R0.2; the arena twists are Should, R0.3 item 4);
- **no PART icon** in v1.0: PARTs are the Could bundle (R2.5).

### 4.1 SUMMIT CLIMBER (Blizzard, `$00`; the v0.1 slice, M4)

Vanilla sets on the climb: snow robot `$4D` (`C0-EF`), count bombs `$19/$21` (`A0-BD`), drone `$24` (`F0-FE`), walker
`$1E` (`C0-DA`); ship riders `$1F/$20` (`C0-DF`); jester head `$10` (`A0-FF`, all 96).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$82` (ice, ledges, girders, skyline), `$85` (ship), `$84` (cave) | | | all | [engine-ok] | |
| **BZ-CLIMB** third at `$0A00` (the climb hides the far skyline): ice cells intact and gone (T6 variants), rock floor, ledge ends, clouds, ladder stubs, hanging and shaking icicle cells, sign boards | 44 (24 re-sourced from `$82` and Wind's clouds, 20 drawn) | | climb, ship | R + D | Must |
| **BZ-SUMMIT** third: peak and flag, the lodge (from Plant's lodge logs), sun deck, MR. Y MARU banner (font), the giant eggplant statue | 30 (12 + 6 + 12) | | 0F-1A | R + C + D | Must |
| **SET-BZ1** `A0+32`: seal-bot (walk ×2, push with cube, stun, bow, sad), ice cube, falling icicle. The seal starts from the snow robot `$4D` | 28 | 8 | climb, ship | X | Must. Conflicts with count bombs, jester. Fits beside the snow robot, drone and ship riders |
| **SET-BZ2** `A0+32`: bird-bot (fly ×2, dive), 4 vegetables, cloud/floe 48×8 | 24 | 8 | climb, bonus summit | D | Must. Never with SET-BZ1 (same slot) |
| **SET-BZ3** `C0+48`: condor 32×24 (2), seal foreman (2) | 36 | 4 | summit, 11, 17 | D | Must. Conflicts with the snow robot, walker and riders: none of them on the summit |
| Champion pinch set: skis-off, slush puddle (MELT), "skis slip" | 16 | 4 | boss 16 | D | Must |
| Ski fence and moguls (BG) | 16 | | ski run | D | Should |
| Rolling snowball (2), snowman SC4 (2), in SET-BZ2's slot | 12 | 4 | ski run, boss | D | Should |
| The sleeping polar bear (a BG cameo) | 12 | | summit | D | Could |

Changes from round 1 (venues_b §1.8's list):

- hanging icicles are BG cells (only the falling frame is a sprite);
- the condor carry uses vanilla's ladder poses (round 1's 2 carry tiles are dropped);
- the snowman and the rolling snowball are Should;
- Shirokuma is a BG cameo (Could).

The ship screens use SET-BZ1 (falling icicles) at `A0-BF` beside the riders at `C0-DF`: no conflict. Palette: the seal and
the bird share the climb's enemy palette 2 (white / light blue) with the snow robot; the vegetables use palette 1.

### 4.2 SKY ACE (Wind, `$01`)

Vanilla sets: panda drums `$27/$28` (`D0-EF`), crawler `$29` (`C0-DF`), bomber `$1B` (`E0-EF`), tops `$36` (`F0-FC`),
stomper `$2D` and beetle `$75` (`D0-D8`), shield-car `$34` (`B0-BF`), big robot `$59` (`C0-F6`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$83` sky, clouds, coral girders, pillars, tower, fans; `$8C`, `$8D`, `$8E` | | | 03-15 | [engine-ok] | |
| **W-CARRIER** third (ids `$54-$B3`; v00's screens leave `$54-$E9` free): steel deck, stripes, catapult track, arresting wires, lamp board (lamps lit by `map_set`), elevator rim, ACES ONLY sign, the LAND hatch and its sign | 96 (40 re-sourced deck and girder tiles, 16 programmatic stripes and signs, 40 drawn) | | 00, 02 | R + C + D | Must |
| **W-SEA** band (ids `$76-$B5`): a 512-px sea loop, distant islands | 48 | | 01 | C | Must |
| **Windsock** (BG, 3 states: limp, left, right) | 8 | | boss rooms 13, 1D | D | Must |
| **SET-WS1** `A0+32`: propeller Met fighter (bank L / level / bank R; green and red by palette), gold leader (2), bullet: the vanilla Metall + the `$1B` bomber's propeller | 32 | 6 | 01 | X | Must |
| **SET-WS2** `C0+16`: POW / 3-WAY / AUTO / YASHICHI icons, LOOP "R", lamp | 16 | 6 | 01, 02 | D | Must |
| **SET-WS3** `D0+32`: the v1.0 AYACO, a 48×24 body with two engine pairs (2 frames each) and a bomb | 32 | 4 | 01 | D | Must |
| **Seagull** (2), the hidden-room tell, at `A0+16`: a recolour of the pelican `$AB` | 8 | 2 | 0A | X | **Must** (round 1: Should; the Must hidden room needs its tell) |
| Champion pinch set: SKY ACE goggles and scarf (12), the red plane (4), a POW (4) | 24 | 4 | 13, 1D | D | Must (round 1: 16) |
| Set-piece player sheet: the sortie (§2.4) | (§7.1) | | 01 | X | Must |
| Destroyer silhouette in W-SEA | 16 | | 01 | C | Should |
| AYACO's 4 separate engines and tail gun (in WS3's `F0-FF`) | 16 | 3 | 01 | D | Should |
| Kite Met (2) at `A0+16`; deck crew Met and bomb cart, SET-WS5 `C0+16` | 24 | 7 | 09-0A, 00, 02, 19-1A | X | Should |
| **W-HANGAR** third; AYACO as BG art in the sky band (one size) | 96 + 110 | | 18-1D, 01 | D | Should |

The sortie (01) carries SET-WS1 + WS2 + WS3 = 80 of 96 tiles, so **no vanilla Wind enemy appears on 01** and explosions
use the common row. **Flicker**: the wave director keeps ≤ 3 fighters in any 8-px band (§3.4); lag is 9 slots (§3.5).

### 4.3 LOST JUNGLE (Plant, `$02`)

Vanilla sets kept: gorilla tank `$50` (`B0-FF`, 80 tiles) and its parts, eye cannon, springs `$57/$5A` (`F0-FF`), `$60`
(`C0-DF`), `$61` (`A0-BF`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$90` base; `$91`/`$92` dark-room swap; `$BB`/`$93` flower swamp; palettes `$32-$35` | | | 03-08, 0F-17 | [engine-ok] | |
| **P-PITFALL** third (`$0A00-$0FFF`, replacing the canopy; an internal id): a **2600-style canopy** (fat pixels, 2 greens; the homage is why it can be smaller than vanilla's 96-tile foliage) + vine knots, the tar surface (2 boiling frames, the torch technique; the "closed" alternates), croc-pond water, ladder-hole rim, trunks, parrot ledge, rope ladder | 96 (40 programmatic canopy, 56 drawn) | | 00-02, 09-0E, 1F | C + D | Must |
| **P-UNDER** third: brick tunnel (recoloured vanilla brick), cracked wall, ladders (vanilla), scorpion nests | 96 (56 re-sourced, 40 drawn) | | 18-1A | R + D | Must |
| **P-CAVERN** third: cave walls (`$96`/`$84`), the underground river and a waterfall (`$AA`'s water and animation), the cavern gate | 96 (64 re-sourced, 32 drawn) | | 1B-1D | R + D | Must |
| **SET-PL1** `A0+48`: vine (11 angle tiles; one object of 5 segments), croc head 32×16 (closed, opening, open), log (2). Tar bubbles are BG animation (lag) | 48 | 7 | jungle | D | Must. Conflicts with `$61`, `$60` |
| **SET-PL2** `D0+32`: 4 treasures, parrot (2) | 32 | 6 | jungle | D | Must. Conflicts with `$60` (keep it in the swamp) |
| **SET-PL3** `A0+48`: scorpion (3), robot cat (3), bat (2), balloon (2) | 44 | 10 | 18-1E | X | Must |
| Vine and balloon poses | 0 | | | vanilla ladder poses (§2.4) | Must |
| Champion pinch set: the bloom form (the 30-f invincible bloom covers the stream), vine lash | 24 | 5 | 17, 1E | D | Must |
| The Lost City's ruins and giant orchid (the 1E twist; v1.0's 1E is the bamboo room at night) | 48 | | 1E | D | Should |
| Eel (2); CONGA's 4-tile log copy (its 80-tile set leaves `A0-AF`); swing poses (a set-piece sheet) | 24 | 6 | swamp, 08, jungle | X | Should |
| P-RAIN (8 tiles × 4 frames, the torch technique) | 32 | | 0B-0E | C | Could |

Plant has **0 free BG tile ids** (`rm6/SUMMARY.md` §2): every new BG tile enters through a third, as venues_a §4.1's
CHR-state table plans. Pop-ups on these dense screens wait for free glyph ids (tech §11.4). Vanilla's worst lag (09-0D)
becomes vine screens within the 9-slot cap.

### 4.4 PERSIAN PALACE (Flame, `$03`)

Vanilla sets: Metall `$18` (`C0-EA`), Fire Telly `$2C` (`EC-FF`) and its drop `$30` (`A0-AF`), dome turret `$2B`
(`C0-E7`), wheel cannons `$C0/$C9` (`D0-EF`), juggler `$2A` (`E0-FF`), mine `$73` (`D0-D8`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$86` oil field, `$87` fire vault; the oil palette cycle and ignite alternates (`$E6-$E9`) | | | oil screens | [engine-ok] | |
| **FL-DUNGEON** third: stone, torches (Knight's `$9F-$A1` animation), columns, arches and PoP-style windows, carpets, pressure plates raised and pressed (the slot's alternate set), the loose tile's socket | 50 (24 + 26) | | 04-0E | R + D | Must |
| **FL-PALACE** third: the mirror 32×48 with its glow palette, the hourglass mural, the mousehole, the sponsor tapestry, the throne backdrop for 1A, rooftop **domes and a full moon** (the vanilla moon), the balcony window. **No minarets, no crescent** (R3.4) | 40 (8 + 32) | | 0F-1A | R + D | Must |
| **SET-FL1** `B0+48`: guard-bot (stand, advance, blade-up glint, lunge, recover), plus a 2-frame chandelier copy for the gallery | 44 | 7 | dungeon, 0B | X | Must. Fits beside the Fire Telly and its drop; conflicts with the Metall, dome, wheel cannon |
| **SET-FL2** `E0+16`: loose tile (2), spike trap (3) | 16 | 5 | dungeon | D | Must. Conflicts with the Telly and juggler: trap rooms have no Telly |
| **SET-FL3** `A0+48`: portcullis 16×48, chandelier 16×24 (2), mouse-bot (2), the fire marshal (2) | 40 | 7 | palace, 1C | D | Must (the mouse room is Must, R2.5) |
| Shadow Rock | 0 | | 0D-0E, 1A | R: Rockman's frames in a dark palette (4MI's Snatchman trick) | Must |
| Champion pinch set: the flaming sword, the head flame guttering (BLOWOUT) | 12 | 3 | 16 | D | Must |
| Chomper slots (BG) | 6 | | dungeon | D | Should |
| Skeleton-bot (walk ×2, collapse, bones), chomper blades (2), **the vizier = Wily in costume** (a composite of the vanilla Wily sprite, R3.4) | 28 | 8 | dungeon, balcony | X | Should |

The gallery (0B) needs only 2 chandeliers (venues_b), so 0B uses SET-FL1 alone (guards + its chandelier copy) and never
needs SET-FL3: round 1's overlap note is resolved.

### 4.5 EDO NINJA ROW (Yamato, `$04`; trimmed, R3.2)

Vanilla sets: lantern robot `$C2` (`C0-DF`), samurai `$A2` (`A0-FF`, all 96), shuriken robot `$69` (`D0-FF`), eye cannon
`$54` (`A0-AF`), springs `$5F` (`B0-BF`); GAMARN & GAMADAYU `$61` (`A0-EF`, 80).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$97` (Fuji vista, castle walls, shoji), `$98` interiors, `$99` dark bypass, the plate route's sunset `$9A-$9C` | | | | [engine-ok] | |
| **YM-EDO** third: shopfronts with noren, kawara roofs, the notice board and WANTED poster, tatami, 3 hanging scrolls (2-frame flutter), the "E" banner | 56 (8 programmatic signs, 48 drawn) | | 00-0B | C + D | Must |
| **YM-CASTLE** third: the caltrop floor (vanilla spikes) and gold crest, the treasure vault, the shachihoko, the theatre curtain and stage for 1D | 36 (8 + 28) | | 0C-1E | R + D | Must |
| **SET-YM1** `A0+32`: Jaja-nin (hop, throw, stunned) + shuriken | 24 | 4 | rooftops | X | Must. Conflicts with the eye cannon and springs |
| **SET-YM2** `A0+32`: ashigaru (3), the paper-lantern flame (2) | 28 | 5 | town edge, 14 | X | Must. Never with SET-YM1 (same slot) |
| **SET-YM3** `A0+64`: **the Daruma** (stack frames, head with one eye and two eyes, angry head, fortune slip) and the pogo rack | 56 | 8 | 11, 12-13 | D | **Must** (round 1: Should; the DARUMA chip's gate, R2.5, R0.4) |
| Set-piece player sheet: the pogo (§2.4) | (§7.1) | | 12-13 | X | Must |
| Champion pinch set: the flying kabuto, the topknot frames | 16 | 4 | 16 | D | Must |
| Gold nightingale boards, the audience and set flats (BG) | 32 | | 0C-11, 1D | D | Should |
| Bells (2), in SET-YM3's spare | 8 | 2 | 0E | D | Should |
| Kuroko stagehands (2) | 8 | 2 | 1D | X | Could |
| The runner ninja and his pass, the sekisho gate and guard, the kite and kite ninja, the hanabi | 72 | 13 | | | **Won't (v1)** (R3.2, R3.1) |

The samurai `$A2` takes all 96 tiles: it keeps its vanilla screens and gets nothing new beside it. The Gamadayu room
keeps `$61` alone (round 1's hanabi copy inside it is gone).

### 4.6 HIGH NOON FRONTIER (Tomahawk, `$05`)

Vanilla sets: cowboy gunner `$6C` (`A0-CF`), walker `$12` (`A0-BF`; the cactus re-skin), dome dispenser `$4F` (`C0-EA`),
`$67` (`A0-CF`), lift `$A0` (`D9-DE`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$94` desert + parallax mesas, `$96` cave, `$95` sunset sky and sun disc, `$D7` boss corridor | | | | [engine-ok] | |
| **T-TOWN** third (ids `$BD-$FF`, free on v0A-0C): false fronts, gallery windows and doors (each opened by `map_set`), boardwalk, water tower, the outhouse (door and OCCUPIED / VACANT by the per-id flip), the WANTED board with three posters, store signs | 64 (8 programmatic signs, 56 drawn) | | 0A-0C | C + D | Must |
| **T-SALOON** third (`$A0-$FF`, free on v0D): bar, bottles, mirror, piano, swinging doors, the skylight | 96 (16 wood tiles from Plant's lodge, 80 drawn) | | 0D | R + D | Must |
| **T-TRAIN** set (fresh ids; the train screens replace v10-v11): car roofs and couplings, station platform, rails and ties (a 512-px near loop), wheels (a 4-frame CHR animation), the TUNNEL! sign | 80 (16 + 24 programmatic rails and wheels + 40) | | 0E-11 | R + C + D | Must |
| **T-MESA** third (ids `$BE-$FF`, free on v17; **replaces T-BOOTHILL**): the HIGH NOON MESA, a flat mesa top at noon and distant buttes (the `$94` mesas re-paletted), **no graves** (R3.4); the flag judge's stand and flag | 40 (24 + 16) | | 17 | R + D | **Must** (R3.4) |
| **SET-TM1** `A0+64`: outlaw (pop up, aim, shoot, hit; a `$6C` recolour), townsfolk (lady with parasol 2, pianist 2, Eddie at a window 2), tumbleweed (2) | 64 | 12 | gallery 0B-0C | X | Must |
| **SET-TM2** `E0+32`: "DRAW!" / "FOUL!" / "HEY!" words, bounty stamp, hat glint, bullet hole (words from the font) | 32 | 7 | 0B-0D, 17 | C | Must |
| **SET-TM3** `A0+64`: Six-Shot Sam (stand, draw, shoot, fall), the Sheriff (2), the conductor (2), **the flag judge** (a vanilla Metall with a flag, 2) | 64 | 10 | 0D-0F, 12 | X | Must |
| **SET-TM4** `A0+64`: Sidewinder on his robot horse (32×32, a 4-frame gallop + shoot), the tunnel wall (32×48), a robber (a local copy of `$6C`) | 64 | 8 | 10-11 | D | Must |
| **Cactus walker**: the `$12` walker recoloured green with new spine tiles; "totem" leaves the venue (R3.4) | 8 | 0 (vanilla frames) | 03-04, 12 | X | **Must** (round 1: Could) |
| Champion pinch set: SHOWDOWN (the hat brim down, the etiquette bow), the draw | 16 | 4 | 17 | D | Must |
| **T-RODEO**: the rodeo ring's fence and stands, the WANTED: ROCKMAN poster (the 1F twist; v1.0's 1F is the mesa at dusk) | 48 | | 1F | D | Should |
| Tunnel bats, TNT crates | 12 | 3 | 10-11 | X | Should |
| Vulture re-skin of the `$64`/`$66` drones | 8 | | desert | X | Could |

The cowboy gunners `$6C` (`A0-CF`) conflict with SET-TM1/3/4: they stay in the desert and the mine (01-09), and on the
train only as SET-TM4's local copy. Vanilla's conflict screens 04 and 15 (the `$61` preload, §1.4) disappear in the GP
layout; the build re-checks. SET-TM2 (`E0-FF`) sits beside SET-TM1 or SET-TM3 (`A0-DF`). The train is the flicker and
lag hot spot (§3.5).

### 4.7 HERO'S QUEST (Knight, `$06`)

Vanilla sets: lance knight `$6E` (`A0-BF`), `$3D` (`F0-FF`), `$65` (`A0-BF`), spearman `$70` (`A0-B9`), `$C6`
(`A0-BF`), `$3A` (`D0-D8`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$9E` castle (green stone, halls, chains, machine hall), the torch animation `$9F-$A1`, the revisit palettes (bank `$28`) | | | all | [engine-ok] | |
| **K-DQ** third (ids `$B5-$DC`, swapped on 01, 0D and 15, which leave `$B5-$FF` free; the machine hall's exit restores `$97-$DF`): two thrones 32×32, the stone tablet, the trapdoor (the alternate of 0D's floor), the hidden-stairs metatiles (the alternate of the v15 pillar) | 40 (12 re-sourced, 28 drawn) | | 01, 0D, 15 | R + D | Must |
| Window frame | 0 | | | the text frame (§3.6) | Must (shared) |
| **SET-KN1** `C0+32`: King (2), Sage (2), chest closed / open (2), MAGIC KEY: vanilla NPC frames, crown and palette new | 32 | 7 | 00-0B | X | Must |
| **SET-KN2** `C0+48`: Metslime (a vanilla Metall helmet on a teardrop body, bounce 3), Metal Metslime (a grey palette + a 2-tile shine), Killer Chest (3), the ceiling winch (2) | 46 | 9 | 03-06, 0C-14 | X | Must. The sconce flame is Won't (R3.1) |
| Champion pinch set: ENRAGED (red eyes, mace raised), "the shield knocked aside" | 12 | 3 | 17 | D | Must |
| The inn bed (BG, swapped on 0A-0B) | 8 | | 0A-0B | D | Should |
| Princess Roll in a gown (2), the Innkeeper (2), Roll's Love heart (in SET-KN1's `E0-EF`) | 18 | 5 | 0A-0B | X | Should |

Every vanilla Knight enemy lives in `A0-BF`, `D0-D8` or `F0-FF`, so `C0+48` is free of conflicts except with `$3A`
(`D0-D8`), which stays out of encounter rooms. SET-KN1 and SET-KN2 share `C0`: NPC rooms and encounter rooms are
different screens. Encounters (0C, 13) put SET-KN2's slimes beside the vanilla lance knights with no change.

### 4.8 ATLANTIS RUINS (Centaur, `$07`)

Vanilla sets: pelicans `$A9` (`FA-FF`) and `$AB` (`D0-F9`), piranha `$C1` and seahorse `$C4` (`A0-AF`), waterfall enemy
`$A5` (`D0-FF`), dome turret `$2B` (`C0-E7`).

| Item | Tiles | Frames | Where | Method | Tier |
|---|---|---|---|---|---|
| Kept: `$AA` (ruins, water, waterfalls, orange castle), the water animation (`$DC-$DF`, `$E8-$EF`) | | | all | [engine-ok] | |
| **CT-ZONE** third: zone doors (honest / lying / fake), plaque numerals 0-9 **as BG tiles** (from the font), the tablet, the Y-MAN mural, painted tide lines, the tidal shaft's ledges and ladder (`$AA`), the sky temple and its altar | 70 (20 re-sourced, 10 programmatic, 40 drawn) | | 06-1C | R + C + D | Must |
| **SET-CT1** `B0+16`: the cloud platform (a copy of Blizzard's), the tide float, the T plate | 16 | 3 | 06-18 | R | Must. Fits beside the piranha, seahorse and pelicans, and beside the dome turret (`C0-E7`) |
| **SET-CT2** `A0+32`: the Centurion statue and the freed Centurion (2) | 24 | 3 | statue rooms | D | **Must** (CENTURION, R2.5). Conflicts with the piranha and seahorse: the statue rooms are dry |
| Champion pinch set: the tide-call pose, STUMBLE, the three slot-reel icons | 24 | 5 | 17 | D | Must (round 1: 12) |
| The ZONE card's digits | 0 | | | the HUD widget's LABEL/DIGITS with vanilla digits | Must |
| The hot spring with steam, the sunken throne (BG) | 40 | | 1A-1C | D | Should |
| Nasubi Mage (float ×2, cast) and the eggplant; Grim Reap-bot (patrol ×2, look, alarm) and Reaplets (2), SET-CT3 `D0+48` | 72 | 10 | 0E-18, 11-14 | D | Should. SET-CT3 conflicts with the pelicans and the waterfall enemy |
| Eggplant-Rock (a set-piece sheet, §2.4) | 12 | 4 | curse | D | Could |

Changes from round 1 (venues_b §3.8): the plaque digits are BG tiles; the ZONE card uses the HUD widget; the Centurions
leave the Should set for a Must one; the wrap tower's screens become the tidal shaft (R3.1), whose rooms reuse `$AA`
water.

### 4.9 Venue totals (`budget_r2.py`)

| Venue | Must: new BG / sprite tiles / frames | Must sessions | Should (BG / sprite / frames) | Could | Heaviest sprite screen |
|---|---|---|---|---|---|
| SUMMIT CLIMBER | 74 / 104 / 24 | 2.4 | 16 / 12 / 4 | 12 BG | ship + icicles; the boss (§3.5) |
| SKY ACE | 152 / 112 / 22 | 2.8 | 222 / 40 / 10 | | 01, the sortie (80 / 96) |
| LOST JUNGLE | 288 / 148 / 28 | 4.5 | 48 / 24 / 6 | 32 BG | jungle (80 / 96) |
| PERSIAN PALACE | 90 / 112 / 22 | 2.6 | 6 / 28 / 8 | | 0B (SET-FL1 alone) |
| EDO NINJA ROW | 92 / 124 / 21 | 2.6 | 32 / 8 / 2 | 8 sprite | 11-13, the Daruma (64 / 96) |
| HIGH NOON FRONTIER | 280 / 248 / 41 | 5.4 | 48 / 12 / 3 | 8 sprite | 10-11, the train |
| HERO'S QUEST | 40 / 90 / 19 | 1.6 | 8 / 18 / 5 | | encounters |
| ATLANTIS RUINS | 70 / 64 / 11 | 1.5 | 40 / 72 / 10 | 12 sprite | statue rooms |
| **Total** | **1,086 / 1,002 / 188** | **23.5** | 420 / 214 / 48 (8.7 sessions) | 44 / 28 (0.8) | |

The venues also own 72 Won't sprite tiles (Yamato's cut cast). Cheap reuse is already counted at zero or as R: Shadow
Rock, Metal Metslime, CONGA, Gamadayu, the vanilla desert parallax, the ship, the tide, the spike ceiling and every
vanilla enemy the venues keep. CX recoloured 71 % of its reused sprites (cx/graphics.md §6); GP does the same.

### 4.10 Art and audio under the CASUAL levers (R2.9)

art_audio owns no stage, so it fills in no lever list of its own. Each stage owner fills in R2.9's five standard levers
(the venue docs and fortress do). What art and audio **guarantee**, so that no lever ever needs new art or a new track:

| Lever (R2.9) | The art and audio guarantee |
|---|---|
| Reflex windows × 2 (and the INPUT LAG offset, R3.5) | every reflex prompt's tell is visual and audible at the window's **start** (the flag drop, the DRAW bell, the hat glint, the boss tells), so a longer window changes only logic |
| Mash counts −40 % (hold to struggle) | no art per press; a struggle meter is the HUD widget's METER (tech §7.13) |
| Set-piece timers +50 % | **every set-piece cue loops with no timed ending** (G25, G15's FINAL LAP entry and their vanilla fallbacks), and every clock or meter is a widget whose maximum is data |
| +1 checkpoint per section | a CASUAL checkpoint gets the same build check as any other: its screen's palette program is self-contained (tech §6.3 check 4) |
| Skill-gated secrets relaxed one step | CASUAL poke lists use only blocks already in the stage's slot (a ledge, a narrower gap): **no CASUAL-only art** |

---

## 5. Non-venue stages: art budget

`fortress.md` owns these stages' staging, layouts and boss techniques (round 2); this is their art, re-run against it
(R5.3, consistency-8). Ids and slots are tech's (§2.2). The rows are `budget_r2.py`'s.

### 5.1 Opening-lite (`$10`, TS_STADIUM) · Must, M5

| Item | Tiles | Frames | Method | Tier |
|---|---|---|---|---|
| Kept: Mr. X 1's night skyline and moon (set `$9D`) behind the plaza | | | [engine-ok] | |
| **TS_STADIUM base**: the players' tunnel, turnstiles, bleachers on vanilla girder and pipe tiles, the pitch and running track (programmatic stripes), the scoreboard (a 6×3-block panel whose digits and words are metatiles written by `map_set`), the press box (Cossack and Kalinka as BG face icons in the window), floodlight towers, Eddie's stall | 130 (40 re-sourced, 30 programmatic, 60 drawn) | | R + C + D | Must |
| Crowd tiles, 2 frames (a CHR swap every 16 f; both frames keep the same mean brightness, §3.2) | 20 | | C | Must |
| **Grand Pi-kun's body: ONE size, 80 px tall**, one pose in NT1 (the Mr. X 2 pod technique, `RL_FLOOR`; fortress §1.6) | 60 | | D | Must (R3.6) |
| Sprites: Pi-kun's valve, puffs, confetti and the pump hose; the high striker's puck and bell; the lane judge (16×24, 2) with card digits; training targets; beach balls; the float deck (48×16); a white glove | 64 | 16 | D | Must |
| **SET-PARADE**: the eight champions' vanilla idle frames, about 12 tiles each, packed into one 96-tile enemy-area set; reused at the podium (§3.5) | 96 | 8 | R | Must |
| The NPC Break Man (masked palette for S06), Bass β | (§5.2) | | | Must |
| Pi-kun's S and L sizes (F-SIZES; with M, about 150 tiles in all) | 120 | | D | Should (R3.6) |
| The GP Rush lobby screen (`$10` screen `$1D` on TS_STADIUM, consistency-31) | 24 | | D | Could |

### 5.2 HALFTIME RIOT (`$11`, TS_STADIUM: NIGHT / BLACKOUT / FIRE palettes) · Must, M6

| Item | Tiles | Frames | Method | Tier |
|---|---|---|---|---|
| New BG: service tunnels (pipes, cable trays, emergency lights), rubble, the scoreboard scaffold and the jumbotron (a 6×4-block panel written by `map_set`), the roof gantry, two fuse boxes and the master breaker, the emblem door | 80 (40 re-sourced pipes, rubble and girders; 40 drawn) | | R + D | Must |
| **VENDING MAN and CHEER MAN**, the rejects (16×24, ≤ 8 frames each), composites of vanilla RM6 enemies (R4.3, R5.1) | 48 | 12 | X | Must |
| The ACCEPTED stamp, the can, the BASS BLASTER (2 pre-drawn sizes) | 22 | 4 | D | Must |
| **Bass β boss set**: Rock's frames recoloured, with overlay parts (helmet fins, the β, crash-test markers), ≤ 16 frames re-pointed (R4.2, R5.1) | 50 + 20 overlay | 16 | R + D | Must |
| **His 4 pre-drawn copies** in his own 96-tile set (R3.6): B.ATTACK (3), F.BLAST (9), KNIGHT.C (2), SILVER.T (5), plus his spread shot | 22 | 4 | R | Must |
| **The NPC Break Man**: Rock's frames recoloured, about 10 frames with overlay parts (visor, scarf, shield) (R4.2; tech §7.9's family `$F7` NPC). Used in the Opening, the Riot, H5, W3 and the ending | 30 + 10 overlay | 10 | R + D | Must |
| UMBRELLA MAN (a parachute, not a shield, R3.1) | 20 | 5 | X | Should |

Bass β's set is 92 of 96 tiles. Duel 1 draws his copies from it, and W2's duel 2 reuses it. The NPC Break Man's set is
40 tiles at `A0+48`.

### 5.3 The Hall of Fame: H1, H3, H5 (`$16`, `$18`, `$1A`) · Must, M7; H2, H4 Should

**The MUSEUM third** (≈ 96 tiles: marble trim, velvet ropes and posts, plaque frames, glass cases, the wing doors with
years) is **one CHR set** (§2.1), swapped into `$0A00-$0FFF` by a screen exit and shared by every wing (fortress §0.1).
Method: 16 programmatic (frames, years), 80 drawn. Must.

**The H-wing look rule** (Must, cheap): each wing re-creates its game's *signature hazard* in RM6's tile style, then
sells the era with **palette**: H1 in MM1's flat blue-grey, H3 in MM3's teal, H5 in MM5's purple (H2 MM2's night sky and
H4 MM4's dusk snow when they ship). **No tiles are ripped from RM1-5 ROMs** (BRIEF §7.4); they are redrawn or rebuilt
from RM6's own pages.

| Stage | Item | Tiles | Frames | Method | Tier |
|---|---|---|---|---|---|
| **The trophy theft** (S25, the 8th win; fortress §4.0) | The UFO-catcher claw (3 frames) lowered from Mr. Y's pod (the H5 row's recolour, the Y painted over its W). H4's Cossack Catcher reuses the claw | 20 sprite | 3 | D | Must |
| **H1** (bank `$66` slot 1, Wily 2's base) | The pink MM1 third: Elec beam emitters, fire vents, score balls, the appearing-block cells (`alt_flip`) | 36 | | D | Must |
| | **Yellow Devil MK-VI**: a 3×4 grid of 16×16 pieces (48×64) + the eye socket, BG in NT1 (Wily 2's walker room, `RL_FLOOR`; F-PIECES moves pieces) | 60 | | D | Must |
| | YD sprites: the eye (open, closed, hit), a flying piece (3 shapes), the splat (2) | 24 | 8 | D | Must |
| | **Big Eye MK-VI** (≤ 8 frames; vanilla eye-cannon parts) | 40 | 6 | X | Must |
| | Guts Man's lifts, the box-art figure | 24 | | D | Should |
| **H3** (bank `$67` slot 0, Mr. X 3's base; the Metonger Z tank's tiles are freed for Gamma) | Needle-press heads (vanilla pistons), the Gemini laser (R3.1), the Break Man statue (BG), the practice fist and the punching bag with its bell (R2.11) | 48 (16 + 8 + 24) | | R + C + D | Must |
| | **Gamma MK-VI, head and shoulders only** (R2.11): static BG in NT0 (the Mechazaurus technique) | 82 | | D | Must |
| | Gamma's rocket fists, 24×24 sprites (2 × 2 frames); they become platforms | 18 | 4 | D | Must |
| | **KAMEGORO MAKER MK-VI** (R3.6): the vanilla dome dispenser re-skinned: the shell press, turtles (the hard-hat walkers recoloured with a shell), eggs | 24 | 4 | X | Must |
| | Doc Robot MK-VI copying AIR MAN (Air Man's set) and Air Man's arena (R3.6) | 60 + 48 BG | 12 | D | Should |
| **H5** (bank `$67` slot 1, Mr. X 4's base) | A starfield, crystal emitters, the Super Arrow launcher, the throne room and its pedestal; room 19 loads vanilla's own Mr. X 1 set `$9D` | 60 (8 + 52) | | C + D | Must |
| | The MEGAMAN V letter plates (from the font), the Super Arrow (16×8, 2) | 18 | 3 | C | Must |
| | **Dark Man's disguise**: a 40-tile enemy-area set made from the NPC Break Man with **the scarf orange instead of yellow**, the one visual tell (feasibility-14, consistency-8) | 40 | 6 | R | Must |
| | **Dark Man MK-VI**, the true form (≤ 16 frames, composited first) | 64 | 12 | D | Must |
| | The unmasking: Mr. Y's pod (the vanilla Mr. X pod recoloured, with a Y emblem), the **GP CUP** (16×24; also in W3, the podium and the sixth wing). The Mr. X face and Wily are vanilla; the castle picture's green → NES → SUPER ramp is palette data | 10 | 2 | R | Must |
| | Wave Man's geysers (BG) | 12 | | D | Should |
| | The gravity-arrow panels | 8 | | D | Could |
| **H2** (Should) | The MM2 wing: force beams, the password board, Heat Man's blocks, the dragon-chase sky; **the Mecha Dragon at one size**; Picopico-kun's pieces (F-PIECES); fireballs and platforms | 96 + 120 + 24 BG, 12 sprite | 4 | D | Should |
| **H4** (Should) | The MM4 wing: the flash-bulb photo puzzle (R3.1; its flashes go through the lighting service, ≤ 3 per second), chapel bells, Dust Man's conveyors (R3.1); **the Cossack Catcher at one size**; the claw (3), prize capsules (3), the Cossack Balloon and Flip-Top Jr. (4) | 96 + 120 BG, 56 sprite | 12 | D | Should |

### 5.4 Super Wily Castle: W2, W3 and the escape (`$1C`, `$1D`) · Must, M8; W1 Could

**"SUPER colour" in v1.0** (R1.3) is palettes, raster bands and the music, never ExGrafix (§2.7). It costs palette data,
not tiles.

| Stage | Item | Tiles | Frames | Method | Tier |
|---|---|---|---|---|---|
| **W2** (bank `$68` slot 0, Wily 3's base) | **The bracket board** on the hub's back wall: the champions' and Bass's 16×16 face icons as BG copies, the bracket lines (lit by palette), vanilla's pause-menu weapon icons copied for the finishers | 68 | | R | Must |
| | The Championship Ring and its ropes | 24 | | D | Must |
| | The SUPER palettes for the moat and hub; the refights in each champion's own arena (no new art) | 0 | | data | Must |
| **W3** (bank `$68` slot 1, Wily 4's base) | **WILY MACHINE 6.5** = vanilla Wily Machine 6 art (`$BE`, 202 tiles at `$0360`) **retinted**, plus a `6.5` decal (R3.6) | 6 | | D | Must |
| | The checker floor texture (NT0 rows 24-29) for `RL_FLOOR8`'s 8 bands | 16 | | C | Must |
| | The Capsule's SUPER badge; the Trophy Dispenser re-skin with the GP CUP bolted on (mini-Metalls are vanilla) | 16 | 3 | X | Must |
| | The escape's crumbling-ladder variant blocks (R3.1); the trophy room's shelves (hidden room 0D) | 32 (8 + 24) | | R + D | Must |
| | The Capsule's afterimage decoys, the 16-BIT BLAST glow band, the escape's SUPER → NES → greens palettes | 0 | | palette and raster data | Must |
| | **THE APPROACH**: the drive-toward-camera sizes. If they return, use fortress's sizes (S 64, M 112, L 160 px) with the **L pose ≤ 150 tiles**; the castle background is blanked during the near phase and no glyph window opens there (feasibility-16) | 200 | | D | Should (R3.6) |
| | Flip-Top Jr.'s escape cameo (shared with H4) | 0 | | R | Should |
| | A 16-bit Wily Capsule redraw | 60 | 8 | D | Could |
| **W1** (Could) | TS_LAB (the Game Boy tier is palette over the NES tier's tiles); **METALL 16** at one size in three eras (the Metonger Z technique); Enker (≤ 8 frames); the per-metatile ExGrafix table for TS_LAB (§2.7) | 96 + 150 BG, 40 sprite | 8 | D + X | Could |

### 5.5 The ending (R4.1's order) · Must, M8

| Scene (story's) | Art | Tiles | Method | Tier |
|---|---|---|---|---|
| 2. The castle pixelates | a skull-shaped cloud drawn once, then 2 programmatic downsamples (SUPER palettes → chunky 8-bit blocks → four greens → one green pixel), with 8-f palette steps | 70 | C | Must |
| 3. S40, the catch | the NPC Break Man's stand and walk frames, Rock, vanilla Wily (kneeling) | 0 | R | Must. The carry art is Should (story's) |
| 4. The arrest | two Committee guards (recoloured vanilla robots with an armband); vanilla's Wily-behind-bars art | 4 | R | Must |
| 5. The podium and Bass's vow | podium steps on TS_STADIUM by day; Rock with the GP CUP; **the champions in pairs** (SET-PARADE; §3.5); Bass β's beam (a palette cycle) | 16 | D | Must. The all-eight BG row (112 tiles) is Should |
| 6. The CAPCOM TIMES | the vanilla driver and masthead; the headline `ROCKMAN WINS GP!!` redrawn in the masthead's style (story's words) | 40 | D | Must. The doped headline (with the bundle) is Could |
| 7. The credits | the vanilla staff roll and the DWNB cards; the champions in their own rooms (fortress §6.2) | 0 | [engine-ok] | Must |
| 8. The rating and Break Man's debrief | meta's screen over the judges' desk (meta §6.1) with the meter and title plates (§9.8) | (§9) | | Must |
| 9. LIGHTS OUT (S42) | the stadium at night (the Riot's NIGHT palette); the six floodlight towers switch off as palette steps; Rock, Light, Roll, Rush and Beat in the stands (§3.5) | 0 | | Must |
| 10. The sixth wing | H5's room 19, the GP CUP under the WING 6 plaque | 0 | | Must |
| 11. TO BE CONTINUED | vanilla `$88`, in silence | 0 | | Must |
| The victory lap (Could, one lap) | the credits written into the stadium (scoreboard, banners, the infield grass, crowd card stunts), the venue backdrop strips, the caged-Wily float, the PHOTO FINISH still | 200 + 16 sprite | D + X | Could |

### 5.6 The Exhibitions E1-E3 (`$12-$14`) · Could (R3.7); E4 Won't

Each one, when it returns, is **one lobby plus one rule-boss arena** on TS_ARCADE (bank `$6A` slot 1), built on `map_set`
and T6. §8 has the guests. The arena grids are geometric (programmatic, 120 BG tiles for the lobby and the three arenas).

### 5.7 Non-venue totals (`budget_r2.py`, Must)

| Stage | New BG | New sprite | Frames | Sessions |
|---|---|---|---|---|
| Opening-lite | 210 | 160 | 24 | 4.1 |
| HALFTIME RIOT | 80 | 202 | 46 | 3.8 |
| MUSEUM third, the trophy theft's claw | 96 | 20 | 3 | 1.4 |
| H1 | 96 | 64 | 14 | 2.3 |
| H3 | 130 | 42 | 8 | 2.1 |
| H5 + the unmasking | 60 | 132 | 23 | 2.4 |
| W2 | 92 | 0 | 0 | 0.55 |
| W3 + the escape | 54 | 16 | 3 | 0.7 |
| The ending | 126 (pixelation 70, podium 16, headline 40) | 4 | 2 | 1.2 |
| **Total** | **944** | **640** | **123** | **18.5** |

Should: 972 BG, 128 sprite tiles, 30 frames (14.4 sessions). Could: 638 BG, 266 sprite, 54 frames (11.9 sessions).

---

## 6. BG bosses: one size each (R3.6, R5.1)

All big bosses are nametable art plus a few sprite parts, the technique RM6 already has. In `rm6/SUMMARY.md` §2's words:
"the boss is drawn in a scrolled nametable, an IRQ split shows an unscrolled floor strip from NT0, and invisible hit-box
objects follow the scroll". Both CX and 4MI rely on it. **fortress owns each boss's technique** (consistency-8); this
table adopts its precedents and gives the art budget. **One size per BG boss**: no poses stream in play in v1.0, so the
art loads at room entry with the screen off.

| Boss | Technique (fortress) | Size | BG tiles | Sprite parts (tiles, frames) | Hit box | Tier |
|---|---|---|---|---|---|---|
| **Grand Pi-kun** (Opening) | the Mr. X 2 pod technique: BG in NT1, positioned by the scroll above `RL_FLOOR` (vanilla chain 7) | 80 px tall, **one size** | 60 | valve, puffs, confetti, hose (in §5.1's 64) | the valve, when open | Must |
| **Yellow Devil MK-VI** (H1) | Wily 2's walker room (`RL_FLOOR`) + F-PIECES: a piece flies as a sprite, lands as a block | 48×64 (3×4 pieces) | 60 | eye (8, 3), flying piece (12, 3), splat (4, 2) | the eye | Must |
| **Gamma MK-VI** (H3) | the Wily 1 Mechazaurus technique: static BG in NT0, no split; **head and fists only** (R2.11) | head and shoulders over x 144-255 | 82 | rocket fists 24×24 (18, 4) | chin cannon (phase 1), cockpit (phase 2) | Must |
| **WILY MACHINE 6.5** (W3) | vanilla Wily Machine 6 art (`$BE`) **retinted**, BG in NT1 over **`RL_FLOOR8`** (8 bands, the Mode-7 joke); one hit box (the cockpit) | vanilla | 6 (decal) + 16 (checker) | vanilla parts | cockpit | Must (R3.6) |
| **Wily Capsule SUPER** (W3) | vanilla `$F2` (sprite), new palette; afterimage decoys by palette | vanilla | 0 | a 4-tile badge | vanilla | Must. A 16-bit redraw (60 tiles, 8 frames) is Could |
| Mecha Dragon MK-VI (H2) | fortress §4.2 (the X Crusher technique, in the `$8B` budget), one size | ≈ 96×80 | 120 | fireball, platforms (12, 4) | head | Should |
| Picopico-kun (H2) | F-PIECES, as the Yellow Devil | | 24 | | | Should |
| Cossack Catcher MK-VI (H4) | fortress §4.4, one size | gantry + cabin | 120 | the claw (the trophy theft's, Must, §5.3), capsules (12, 3) | claw | Should |
| AYACO (SKY ACE) as BG art | the sky band | 96×48 | 110 | the v1.0 sprite build (§4.2) | engines | Should |
| METALL 16 (W1) | the Metonger Z technique, three eras of one size | | 150 | | | Could |
| Dark Man MK-VI (H5) | a sprite boss on the Robot Master framework (§5.3) | 24×32 | 0 | 64 + the 40-tile disguise | body | Must |

**The CHR rule for a BG boss** (one rule for all): the arena's base set keeps ≤ 100 tiles for the room, the floor, the
HUD digits and the glyph strip (28 ids, tech §11.4); the boss takes the rest. `bgboss.py` checks that body + room + HUD +
strip fit in 256 BG ids (§10.7).

**Boss panels**: the vanilla typed panel (`$3C:$81B1`, extended by tech §11.2) shows a sprite boss's own pose. For the BG
bosses it types beside **the boss's 16×16 face icon** (§9.4) in v1.0. Match-card portraits are Should (R5.1).

**Totals (Must)**: 202 BG tiles for Pi-kun, the Yellow Devil and Gamma, 22 for WILY MACHINE 6.5, plus 42 sprite tiles of
parts (Pi-kun's parts are in §5.1's sprites). Round 1's 600 Must BG-boss tiles (with a 340-tile three-size MODE-7 Machine and a 200-tile Gamma) are gone.

---

## 7. Sprite list: new characters and frame counts

### 7.1 Player sheets (the player area, `$00-$70`, plus each sheet's own slot set)

| Sheet | Built from | New tiles | Frames | When loaded | Method | Tier |
|---|---|---|---|---|---|---|
| **Super Rock** (the H3 reward, form 3) | a composite of the Power sheet (body, fist arm) and the Jet sheet (backpack), redrawn where they meet; its slot set holds the tap fist and the rocket fist (≤ 15, systems §1.4) | 70 | 12 drawn (the rest re-point Power's layouts) | a form swap (2 KB, §2.6) | X | Must (with H3; tech's `$9B` audit first, R1.12) |
| **SKY ACE sortie sheet** | the Jet sheet: flight banks, 4 loop frames, the RENTAL bib | 24 | 6 | the catapult's cut | X | Must |
| **EDO NINJA ROW pogo sheet** | the normal sheet + 2 pogo frames | 8 | 2 | the rack's take animation | X | Must |
| Break Man (the playable partner) | Rock's sheet recoloured with the NPC overlay parts baked in (visor, scarf, shield); stand, run, jump, shoot, slide, ladder, hurt, teleport, whistle, shield-jump, Break Shot charge | 113 | 20 | behind his beam-in | R | Should (R0.3 item 2) |
| Swing poses, Eggplant-Rock | §2.4 | | | | | Should / Could |
| Bass β (Bass Mode) | | 113 | 30 | | | Won't (v1) |

### 7.2 Bosses and mid-bosses (sprite)

| Boss | Where | Tiles | Frames (cap 16) | Notes | Method | Tier |
|---|---|---|---|---|---|---|
| 8 champions, rebuilt sets | venues | 0 new in phase 1; pinch sets 144 in all | 32 | §2.5, per venue in §4 | D | Must |
| **Bass β** | the Riot, W2 | 92 of 96 | 16 + 4 shot frames | Rock's frames recoloured + fins, the β and crash-test markers (no Treble); his 4 copies pre-drawn | R + D | Must |
| **Dark Man MK-VI** | H5 | 64 + the 40-tile disguise | 12 + 6 | the orange scarf is the tell | D, R | Must |
| **Big Eye MK-VI** | H1 | 40 | 6 | vanilla eye-cannon parts | X | Must |
| **Kamegoro Maker**, **Trophy Dispenser** | H3, W3 | 24, 16 | 4, 3 | re-skins of the vanilla dome dispenser routine | X | Must |
| Grand Pi-kun, the Yellow Devil, Gamma, WILY MACHINE 6.5 | | BG | | §6 | | Must |
| Daruma, Shadow Rock, CONGA, Gamadayu, Metal Metslime, Six-Shot Sam, Sidewinder, the simple AYACO | venues | §4 | | | | Must |
| The 8 secret-arena fights | venues | 0 | | the champion in his boss room with a new palette (R0.2) | R | Must |
| Doc Robot MK-VI (Air Man) | H3 | 60 | 12 | via the fight loader (R3.6) | D | Should |
| Picopico-kun, Mecha Dragon, Cossack Catcher, Flip-Top Jr. | H2, H4 | §5.3 | | | D | Should |
| UMBRELLA MAN | the Riot | 20 | 5 | | X | Should |
| METALL 16, Enker | W1 | §5.4 | | | D, X | Could |
| Block Man, Paddle Man, Invader Man | E1-E3 | §8 | | | D | Could |

### 7.3 Cast and NPC sprites

| Who | Size | Tiles | Frames | Notes | Method | Tier |
|---|---|---|---|---|---|---|
| **The NPC Break Man** | 16×24 | 40 | 10 | §5.2: the Opening (masked), the Riot, H5, W3, the ending | R + D | Must |
| **Eddie** | 16×24 | 12 | 3 (idle, hop, open lid) | **New art: Eddie is not in vanilla RM6** (fortress §1.2 lists him as vanilla; a request, §15). The Opening's stall, Tomahawk's window, the pit stop (as BG) | D | Must |
| **Roll** | 16×24 | 14 | 3 (idle, wave, refill) | composited from Rock's sheet (hair, dress, palette). LIGHTS OUT, the pit crew | X | Must |
| **Dr. Light** | 16×32 | 12 | 2 | LIGHTS OUT | D | Must |
| **Mr. Y** | as Mr. X | 6 | 3 | **vanilla Mr. X's sprite with a fake moustache and a "Y" pin**: the disguise changed one letter | R | Must |
| Dr. Wily, Mr. X, Beat, Rush | | 0 | | vanilla RM6 | [engine-ok] | Must |
| Cossack and Kalinka, full bodies | 16×32, 16×24 | 20 | 4 | v1.0 shows them as face icons (§9.4) | D | Should |
| The judges' cardboard Mr. Y + BACK SOON / RESERVED signs | 16×32 | 8 | 1 | meta's sponsor's chair | D | Should |

### 7.4 Totals (`budget_r2.py`)

| | Must tiles | Must frames | All tiers (M+S+C) tiles | frames |
|---|---|---|---|---|
| Venue sprites (§4) | 1,002 | 188 | 1,244 | 242 |
| Non-venue sprites (§5-§7.2) | 640 | 123 | 1,034 | 207 |
| Player sheets, weapons (§7.1, §2.4) | 114 | 23 | 254 | 53 |
| Cast (§7.3) | 44 | 11 | 72 | 16 |
| UI sprites (§9) | 168 | 9 | 266 | 14 |
| **All sprites** | **1,968** | **354** | **2,870** | **532** |

---

## 8. Guests and exhibitions · Could (R3.7); E4 Won't

BRIEF §6: "A guest or homage must be a mechanic, not just a sprite", with parody names and no trademark logos. R3.3 adds
that **plaques describe, never name** third-party games, and no third-party character names appear on screen. The art's
job is to make the rule readable at a glance. When the Exhibitions return, each is **one lobby plus one rule-boss arena**
(R3.7) on TS_ARCADE, with arena tiles that are geometric (programmatic). Each gets its own hidden-room trick, or none
(R3.8).

| Match | Guest (parody name) | The art carries the rule | Guest sprite | Arena BG | Tier |
|---|---|---|---|---|---|
| **E1** | **Block Man** (a falling-block puzzle born in Moscow, 1984) | the 7 piece shapes as **BG metatiles** in 3 colours, a 10-wide well, a line-clear palette pulse (≤ 3 per second); Block Man is built from 4 blocks and re-arranges into the next piece's shape | 50 tiles, ≤ 16 frames | programmatic | Could |
| **E2** | **Paddle Man** (block breaker) | the brick shell around him is BG (a brick breaks by `map_set`), the ball is an 8×8 sprite with a 3-frame trail, the capsules are 16×8 | 40 tiles, ≤ 16 frames | programmatic | Could |
| **E3** | **Invader Man** (a fixed shooter of 1978) | a formation of 3 invader-*robot* kinds (16×8, 2 frames each: **original designs**), destructible bunkers as BG (chipped per 8×8 tile), a saucer for the bonus | 60 tiles, ≤ 16 frames | programmatic | Could |
| **E4** | Maze Man | (round 1's design is in `art_audio_round1.md`; if it ever returns, its ghosts use **2 palettes plus shape differences**, since a screen has only 2 enemy palettes, feasibility-20) | | | **Won't (v1)** |
| Venue guests | the simple AYACO, the King and Sage, Metslime, Killer Chest, Six-Shot Sam, the robot cat, the seal-bot and bird-bot, Shadow Rock, the Jaja-nin | counted in §4 | | | Must |
| Legacy guests | the MK-VIs (§6) | counted in §5-§6 | | | Must / Should |

---

## 9. UI art

meta owns what each menu screen shows and does; story owns every word on it; this is the art. Rows are `budget_r2.py`'s
`ui` area: **Must 537 BG + 168 sprite tiles, 9 frames, plus the 240 glyphs: 7.5 sessions**.

### 9.1 Title [new-art] M · Must (meta §2.1)

- **Logo**: vanilla's ROCKMAN 6 logo (142 tiles) is kept, with a **"GP" badge as sprites** on top: two 16×24 letters in
  red and gold with a 2-frame glint (16 sprite tiles, D). The title's sprite table has 251 tiles free.
- **Subtitle**: 史上最大の戦い!! → **史上最大のグランプリ!!**. 史上最大の and !! are vanilla logo art and stay. 戦い (≈ 8
  tiles) is replaced by グランプリ drawn in the same brush style (≈ 20 tiles, D). The extra tiles come from the
  pattern-table split (§2.8): the menu text moves to the sprite table, which frees its 16 tiles. The logo's kanji are art,
  so the text engine stays kana-only (consistency decision 5).
- **Menu**: GAME START / SPECIAL EVENTS / CONFIG and the © lines, in meta's order and story's words, drawn from a caps
  font in the sprite table under the split at line 112 (16 tiles re-sourced from vanilla's font). The split is tech's
  `RL_SPLIT_PT` (M5); **until M5 the slice's title uses a plain text menu** (meta §2.1).
- **Moon**: kept (90 tiles).
- **The health notice** (R3.5, meta §2.1) is a text page and costs no art.
- **Music**: G01 GP FANFARE into G00's title cut (§12.3); vanilla `$19` until they exist.

### 9.2 File select, bracket, boss panels [new-art] M · Must (meta §2.2, §3)

| Screen | New art | Tiles | Method |
|---|---|---|---|
| **File select** ("ENTRANT REGISTRATION") | three card frames (vanilla's blue frame tiles), labels, the medal strip; the 8 venue icons are the champions' face icons (§9.4), lit by palette; Kalinka's face icon at the right with her clipboard | 24 BG (+ shared icons) | R |
| **Bracket** | the 8 vanilla 32×32 portraits **kept**; new: bracket lines (straight, corner, T; gold when lit and grey when not, by palette), rivets, the centre frame's states (a trophy silhouette, the lit trophy, the fortress logos) | 56 BG (24 programmatic + 32 drawn) | C + D |
| **Bracket centre: Bass β** | a 32×32 Bass β in a cracked frame, **composited from vanilla's centre Rockman portrait** (fins, palette, cracks; R5.1). Rockman's face on the trophy is vanilla | 20 BG | X |
| **Bracket sprites** | the medal ribbon (1 shape, 4 palettes), the POSTPONED stamp (32×16), ★, the participation ribbon; plate letters B/E/A/T and the cursor are vanilla | 18 sprite | C |
| Exhibition badges (4 rings that blink by palette) | | 16 sprite | Could, with the Exhibitions |
| **Boss panels** (vanilla `$3C:$81B1`, extended by tech §11.2) | a sprite boss shows its own pose, as vanilla; **a BG boss's panel shows its 16×16 face icon** (§9.4). The bold set gains `- ? ! ' β` and the panel frame gains a VENUE strip (story's ask) | 10 BG | D |
| Match-card portraits for the BG bosses | | 64 BG | **Should** (R5.1) |

### 9.3 Judges' desk, scorecard, rating screen [new-art] M · Must (meta §4.0, §6)

- **The desk** fills the top third: **Cossack (head judge, centre) and Kalinka (left) as 16×16 face icons with name
  labels** (R5.1; desk portraits are Should). The desk front, chairs, name plates and the GP banner are 60 BG tiles
  (D), drawn under the pattern-table split so the rows below use the second page.
- **The sponsor's chair** (Should, meta): a cardboard Mr. Y cut-out holding up a "1", then the BACK SOON (from S26) and
  RESERVED (from S33) signs, in story's words. 8 sprite tiles.
- **Scorecard rows**: TIME / DAMAGE / VARIETY / SECRETS / STYLE in vanilla's caps font, with vanilla digits and a slide-in
  tick (an SFX).
- **The medal stamp**: one 32×32 shape in 4 palettes (bronze, silver, gold, platinum), the C / N / H preset badges, and
  the **secret icons** (exit, room, item, plate, envelope), 5 × 16×16, lit or dim by palette and shared with the file
  cards and the pause menu. Together 40 sprite tiles (D). The `93` badge and the TURBO `*` are Could (1993 RULES and the
  bundle).
- **The rating screen** (meta §6.1): in v1.0 it draws over the judges' desk (meta's choice; fortress's "stadium at dusk"
  is withdrawn here in meta's favour), with the rating meter and the title plates (GRAND CHAMPION … PARTICIPANT): 40 BG
  tiles (D). The participation ribbon is in §9.2's sprites. The PHOTO FINISH background comes with the lap (Could).

### 9.4 Face icons instead of portraits [new-art] S · Must (R5.1)

**v1.0 has no portraits.** Every speaker shows a **16×16 face icon** (4 tiles) and a **name label**.

- **In a pop-up the icon is 4 BG tiles** in columns 0-1 of the window, **inside the glyph strip**: ≤ 24 glyphs + 4 icon
  tiles = 28 ids (tech §11.3-§11.4). It needs no sprite tiles, so it works in boss rooms whose enemy area is full. That
  answers the first-weakness line (consistency-14, consistency decision 29).
- A screen with 24-27 free ids shows the name label without the icon; with fewer than 24 the line waits (tech §11.4).
- On menu screens the same CHR loads as a sprite set where a sprite is easier (the file cards).

The set (consistency-40: story's POP speakers, plus the faces the screens need):

| Icons | Used by | Tiles | Method |
|---|---|---|---|
| Mr. Y (the Mr. X face + moustache), Wily, Rock, Bass β, Break Man (the visor), Roll | heckles, the ending, the unmasking's "WE KNOW.", the Riot, W2, the debrief, radio lines | 24 | X (crops and composites of vanilla faces) |
| Cossack, Kalinka, Eddie | every commentator line, the desk, the press box, the pit stop | 12 | D |
| **Light: a radio frame** (static, no face; story's choice) | Light's radio lines | 4 | C |
| The 8 champions | the file cards, the W2 board, the float lines | 32 | R (crops of their boss sprites' heads) |
| Grand Pi-kun, the Yellow Devil, Gamma, WILY MACHINE 6.5 | the BG bosses' panels | 16 | C (downsampled from the BG art) |
| **Total** | 22 icons | **88** | |

**Should (v1.1+)**:

- 32×32 portraits in the CX style (grey scale plus one accent colour, cx/graphics.md §8), loaded only while a scene window
  is up: Rock, Light, Roll, Cossack, Kalinka, Eddie, Break Man, Bass β, Mr. Y and Wily, with 2-tile mouth swaps (180 BG);
- the 4 BG bosses' match-card portraits (64);
- Mr. X's portrait (Could, 16).

Round 1's Beat portrait and Break Man's "NO" variant are dropped: Beat never speaks, and the TURBO refusal ships with the
bundle. A full portrait never appears during play: 8 KB CHR-RAM cannot hold one beside a venue.

### 9.5 Pit stop and chip icons [new-art] M · Must (meta §3.8, systems §9.2)

- **The pit stop**: Eddie's counter and shelves of E-tanks and bolts (vanilla item tiles redrawn as BG), 60 BG tiles
  (20 re-sourced, 40 drawn). Eddie behind the counter is BG (his 3-frame sprite is for in-stage use). The garage door and
  Mr. Y's booth are **Could** (the bundle, R2.5).
- **Chip icons: the 14 v1.0 chips** (systems §9.2), 16×16 each (56 sprite tiles, D), read at a glance:

  | Chip | Icon | Chip | Icon |
  |---|---|---|---|
  | ENERGY BALANCER | a balance scale | YASHICHI | **the Yashichi pinwheel** (Capcom's own icon) |
  | SHOCK ABSORBER | a spring | KAISHIN | a "!" star |
  | SPIKE GUARD | a spike under a shield | SHERIFF STAR | a sheriff's star |
  | CHARGE KIT | a lightning bolt | AUTO RECOVER | a leaf |
  | EXCHANGER | two arrows | SNOW CHAINS | a chain |
  | ENERGY SAVER | a drop | FIREPROOF | a flame with a slash |
  | | | CENTURION | a Centurion helmet |
  | | | DARUMA | a daruma |

- **The envelope icon** is Must (systems); the W-tank icon is Should.
- **Could**: the bundle's chips (IRON HELMET, THERMOS, BIRD SEED, and Y-TURBO as a suspicious "Y") and the 8 PART icons,
  shipping with the bundle (R2.5).
- **Won't**: AFTERIMAGE, GLIDER and JET TUNER are cut chips.

### 9.6 Text: the window and the 1-bpp glyph set [new-art] S · Must (R1.4; tech §11.4; story §10.2)

- **The window**: 7 tiles (corners, edges, blank), white on black (C). It is also the plaque frame and Knight's command
  window.
- **The glyph set**: about 240 1-bpp glyphs (≈ 2 KB) in a text bank:
  - Latin capitals, digits, `. , ! ? ' " : ; - / & % ( )` and `★ ♥ ♪ β × ▶ ・ …`;
  - hiragana and katakana, with voiced and semi-voiced forms **precomposed** (one cell each, unlike vanilla's separate
    `゛`);
  - small kana and `ー 「 」 『 』 、 。 ~`.

  About 180 are converted from vanilla's caps and kana fonts (R). About 60 are new: precomposed kana and symbols,
  generated by composing vanilla's `゛゜` onto the base kana, then checked by eye (C).
- **EN is ALL CAPS: there is no lowercase set** (R1.4; round 1's 30-tile mixed-case set is dropped, consistency-3).
  **JP is kana only** (no kanji).
- **No glyph lives in CHR.** The runner renders each page's distinct glyphs into strip tiles when the window opens (tech
  §11.4). The free-id map (§10.5) gives the strip its ids. Pop-ups wait when a screen lacks them: deferral is accepted
  except for P1 lines, which show on READY (consistency decision 36).
- **Vanilla-font surfaces** (YOU GET, the boss panel, the newspaper, the staff roll) keep vanilla's fonts and quirks
  (story §10.1), plus §9.2's 10 bold-set tiles.

### 9.7 HUD, pause menu, labels [new-art] S · Must

- **GP-COMMON** (§2.4): W, K, !, the swap flash, CENTURION, 1 spare (6 tiles).
- **HUD labels**: 4-tile words, generated from the font (C): `ACE`, `ZONE`, `KEYS`, `BOUNTY`, `BALLS`, `TIME!` and
  `+30 INJURY TIME` (28 sprite tiles). tech's HUD widget module draws them (≤ 4 widgets, ≤ 12 sprites, ≤ 6 on a line;
  tech §7.13). Counters use vanilla digits.
- **The pause menu** (108 free BG tiles in the vanilla pause menu, `rm6/text.md` §7): weapon icons for M.BEAM and SUPER,
  and the 6-slot chip strip (16 BG tiles). The Break Man call row and his icon are Should (with the partner).

### 9.8 Maps, plaques, ending, post-game

| Item | Tiles | Method | Tier |
|---|---|---|---|
| **The Hall of Fame map**: a museum floor plan with 5 wing doors marked with years, the 1993 door UNDER CONSTRUCTION, H2 and H4 drawn **CLOSED FOR RENOVATION** in v1.0. **The Super Wily Castle map**: vanilla's fortress-map pages, a skull castle with a "16-BIT" antenna, W1 drawn closed (meta §3.9, fortress §4.0) | 120 (40 re-sourced, 20 programmatic, 60 drawn) | R + C + D | Must |
| Plaques: full-screen text pages in the window frame (no art); wing emblems (helmet silhouettes by era) | 40 | D | the emblems are Should |
| The rating screen's meter and title plates (§9.3) | 40 | D | Must |
| The ending's pictures | §5.5 | | Must |
| Achievement plates | 40 | C | Could |
| Museum booth meters | 20 | C | Won't (the Museum is Won't) |
| The attract crawl's three new pictures (story S02) | 90 | D | Could (R0.3 item 12) |
| The weapon-get card for M.BEAM | 0 | vanilla YOU GET screen and font | Must. **SUPER has no YOU GET card**: FORMS.SUPER is set at the H3 dock (consistency-28) |

---

## 10. The pipeline (tech builds the tools; this is what they take in and check)

tech schedules and builds the minimal pipeline before any new art (R1.13; tech §6.7: `chr.py`, `sprites.py`,
`palettes.py`, `artcheck.py` at M2, `bgboss.py` at M7). This section specifies their art-side inputs and checks.

### 10.1 Layout in the repo

```
assets/chr/<group>/<set>.png + <set>.json      # one CHR set per sheet (BG third, sprite set, pinch set, icons)
assets/sprites/<object>.json (+ <object>.png)   # metasprites: frames, layouts, animations
assets/bgboss/<boss>/pose.png + boss.json       # BG-boss art (one pose in v1.0), nametable block, hit boxes
assets/palettes/<stage>.json                    # start program + per-exit / per-screen updates, flash requests
assets/text/glyphs.png                          # the 1-bpp glyph set (tech's compiler packs it)
assets/music/<track>.mml, assets/sfx/<id>.yaml  # music and SFX sources (§12.7)
build/revise/art_audio/budget_r2.py             # the art ledger; artcheck compares the built counts against it
```

### 10.2 PNG ↔ CHR (`chr.py`)

- Input: an indexed PNG with ≤ 4 colours per 8×8 tile, or any PNG plus the palette JSON that maps its colours to 0-3.
  Output: raw 2-bpp planar CHR (RM6 stores CHR uncompressed).
- `chr2png` + `png2chr` must **round-trip every vanilla CHR set byte for byte**: the first test, as `levels.py` did for
  levels.
- Sprite sheets may dedupe flipped tiles (sprites can flip); BG sheets may not (the NES cannot flip BG tiles).
- Reserved but undrawn slots are filled with a visible marker tile (4MI's "R-box", r4mi/graphics.md §2), never left
  blank, so a tile editor shows the allocation.
- **Provenance** column in every set JSON: `vanilla` (with its source address), `recolour`, `copy-of`, `composite`,
  `generated`, `drawn`. **It is the R / X / C / D method** of the ledger: artcheck sums it per milestone, so the reuse
  share is measured, not estimated. The credits and the novelty census read it too.

### 10.3 The CHR set manifest and the packer

Each `<set>.json` holds `{"id": "local:E3" | "global:7C", "ppu": "spr:A0" | "bg:0A0", "count": 48, "sheet": "...png",
"palette": "...", "stage": "plant", "method": "X"}`. The packer:

1. places sets into tech's CHR banks `$54-$61` (8 KB = 512 tiles each; a set may cross into the next bank, as vanilla's
   do);
2. writes the v2 set table (§2.1) and the per-stage local tables;
3. leaves the 1,126 vanilla gap tiles (§1.3) as a **reserve**: GP does not need them, and leaving Capcom's banks
   byte-identical keeps the "never overwrite Capcom art" check trivial.

### 10.4 Metasprites (`sprites.py`; tech §7.5)

```json
{ "object": "seal", "chr_set": "local:E0", "base_tile": "A0", "palette": 2, "method": "X",
  "frames": { "walk0": [[-8, -16, "02", "pal2"], [0, -16, "03", "pal2"], [-8, -8, "12", "pal2"], [0, -8, "13", "pal2"]],
              "walk1": "...", "push": "...", "stun": "..." },
  "anims":  { "walk": {"half": 0, "seq": [["walk0", 8], ["walk1", 8]]}, "stun": {"half": 0, "seq": [["stun", 90]]} } }
```

The compiler emits Capcom's format exactly (`rm6/engine.md` §1.5, verified 118/118). A frame is `[n-1][layout id]` + n ×
`[tile][attr]`. Layouts are `[dy][dx]`, **deduplicated by geometry** (frames that share a pose shape share a layout, as
Capcom did). Animations are a half flag plus `[frame][duration]` pairs. The pointer tables go into a **GP sprite bank
pair** (`$4E-$53`; v1.0 needs 2 pairs, the full design 3; tech §1.2).

- **Import** (`sprites.py import`, round 1's `sprslice.py`): it cuts an Aseprite strip on an 8×8 grid aligned to the
  object's origin, dedupes tiles with flips, and writes the tiles into the set and the frames into the JSON.
- **Overlay composites** (Bass β, the NPC Break Man, Roll): an overlay JSON adds parts (fins, visor, scarf) at per-frame
  offsets to an existing vanilla frame list, so a composite of Rock's 16 frames is data, not 16 redraws.
- Validation:
  - ≤ 16 hardware sprites per frame, ≤ 4 per 8-px row inside one frame;
  - every tile inside its set's range;
  - palette 1 or the object's declared enemy palette (§3.2);
  - **≤ 8 frames per enemy and ≤ 16 per boss** (R5.1);
  - a preview GIF per animation for review.

### 10.5 `artcheck.py`: the build's art gate [new-code] M · Must (tech §6.7 builds it)

It runs on every build, over the level JSON and the asset manifests:

1. **Enemy-area overlap**: per screen (and the sets still resident from the 8-entry "recently loaded" list), no two
   sprite sets overlap (tech §7.6). Vanilla has 4 such screens (§1.4); GP may have none.
2. **Enemy palette conflict**: per screen, at most one program each for sprite palettes 2 and 3.
3. **BG free-id map**: per screen and its scroll neighbours, the BG ids referenced after the screen's CHR state. It proves
   every third safe and feeds tech's free-id table for the glyph strip (28 ids for a pop-up, tech §6.3).
4. **Flicker simulation**: for each wave director (the sortie, the gallery, the train) and each boss pattern, step the
   object boxes frame by frame and count sprites per scanline; fail above §3.4's budget.
5. **Streaming budget**: every stream (form swap, slot set, set-piece sheet, pinch set, glyph strip) fits the window the
   design gives it at tech's rates (§2.6).
6. **Capcom art untouched**: every vanilla CHR byte that a vanilla CHR set reads equals `rm6j.nes`. The blank gaps of
   §1.3 stay byte-identical too, unless the full design ever draws on that reserve (§13.1); they hold no Capcom art.
7. **Novelty census**: on the golden-movie states, the share of new BG and sprite tiles per screen, and **ghost frames**
   (4MI's `ghost.py`: vanilla tiles dithered, new art in colour) for the art-acceptance gate (§11.5).
8. **The slot set** (R2.3): any set loaded at `$71-$7F` is ≤ 15 tiles; no non-weapon object draws from `$71-$7F`; a
   set-piece sheet is exactly 128 tiles, with its own buster tiles in `$71-$7F`.
9. **Frame caps** (R5.1): 8 per enemy, 16 per boss.
10. **Occupied slots** (R1.8): the worst case per screen is ≤ 9 (with tech's level-build check 6), counted as tech §15.1
    does.
11. **Flashes** (R3.5): each stage's palette JSON declares its `pal_flash` requests with their periods; any large-area
    flash faster than 3 per second fails. The two frames of an animated BG set (the crowd, the tar) must keep the same
    mean brightness.
12. **HUD widgets**: ≤ 4 per stage, ≤ 12 sprites, ≤ 6 on a line (tech §7.13).
13. **The ledger**: per stage and tier, the built tile and frame counts against `budget_r2.py`'s rows; an overrun of
    more than 10 % is a warning that the milestone gate reviews.

### 10.6 OAM census (`artcheck.py census`)

It plays every golden movie and records which sprite tiles are ever drawn. It confirms GP-COMMON's 6 free slots and the
rarely drawn player tiles before anything uses them (§1.1).

### 10.7 BG-boss art (`bgboss.py`, M7; tech §6.7)

- Each boss is authored as **one pose** (R5.1) in a PNG on a 16×16 attribute grid, with ≤ 4 BG palettes and one palette
  per 16×16 block (checked).
- The tool cuts unique 8×8 tiles (no flips) and emits the CHR set, the nametable block, the attribute bytes, the palette
  program and the hit boxes. It also emits F-PIECES' piece list for the Yellow Devil (§6).
- `boss.json` holds the hit boxes relative to the boss origin (the invisible hit-box objects follow the scroll, as in
  vanilla), the sprite parts (eyes, fists) with their metasprite JSON, and the raster entries (the floor split line,
  `RL_FLOOR8`'s band table for W3).
- A preview renders the boss over its arena with the HUD and checks that **body + room + HUD + the 28-id glyph strip
  fit in 256 BG ids**.
- When F-SIZES returns (Should), the same tool emits pose deltas, so a size change streams only what differs.

### 10.8 Palettes (`palettes.py`)

A palette JSON per stage holds the start program, every update by exit, script or thread, and **the flash requests**
(§10.5 check 11). It compiles to vanilla's partial programs (start index, colours, bit 6 = write `$0F` first, bit 7 =
last; `rm6/levels.md` §7). The revisit palettes (bank `$28`) and the SUPER palettes of W2/W3 use the same format.
Checkpoint screens must be self-contained (tech §6.3 check 4).

---

## 11. Who draws what: the no-artist baseline (R5.1)

### 11.1 The baseline

**There is no pixel artist** (R5.1, scope-7; the user's answer is still open, §18). **Claude's drafts are final**, and
a human pass is optional polish that replaces PNGs without changing any budget. Round 1 assigned 1,368 BG tiles, 1,594
sprite tiles and 419 frames to a human (≈ 660 h for Must); that plan is withdrawn. The budgets, tiers and sizes of this
doc are written for the Claude-only plan.

### 11.2 The rules (R5.1)

1. **Reuse first.** Every new enemy starts as a recolour or a composite of vanilla RM6 sprites, and every BG third starts
   from vanilla pages. Both are counted honestly as R or X in the ledger and in each set's provenance (§10.2).
2. **One size per BG boss**: Grand Pi-kun, the Yellow Devil, Gamma (head and fists), WILY MACHINE 6.5 on vanilla art.
   F-SIZES and its extra sizes are Should (R3.6).
3. **16×16 face icons + name labels** instead of portraits and match-card portraits (§9.4). Portraits are Should.
4. **Break Man and Bass β are composited from Rock's sheet**: Rock's frames recoloured plus overlay parts (visor, scarf,
   shield; fins, the β, crash-test markers), built by `sprites.py`'s overlay composites (§10.4). Dark Man's disguise
   copies the NPC Break Man with an orange scarf.
5. **Frame caps**: at most 8 frames per enemy and 16 per boss (artcheck check 9).
6. **Placeholder first** (process rule): every asset exists from day one as a Claude-generated greybox with the final
   size, tile count, palette slots, frame count and timing. Code and levels never wait for art.
7. **An art-acceptance gate** with screenshots for the user at every milestone (§11.5).

### 11.3 The methods

| Code | Method | What it covers | Why |
|---|---|---|---|
| **R** | Reuse: copy, recolour, crop, repack | SET-PARADE; Bass β's and the NPC Break Man's recoloured frames; Dark Man's disguise; Shadow Rock; Metal Metslime; Mr. Y; the champions' face icons; W2's board copies; re-sourced parts of thirds (decks, bricks, caves, water, mesas, torches, moon); the glyph conversion; the Committee guards | pure data work on Capcom's own pixels; the house style comes for free |
| **X** | Composite: vanilla parts plus new pixels per frame | the seal-bot, Met fighters, the King and Sage, Metslimes, outlaws and townsfolk, Sam and the Sheriff, the scorpion and cat, the guard-bot, Jaja-nin and ashigaru, the rejects, Big Eye, the Kamegoro Maker, the Trophy Dispenser, Roll, the Super Rock sheet, the two set-piece sheets, the cactus walkers | starts from Capcom's silhouettes and outlines; the new pixels are the joke |
| **C** | Programmatic (a generator script) | the 2600 canopy, W-SEA, rails and wheels, the crowd tiles, the pitch stripes, bracket lines, signs and words from the font, HUD labels, the checker floor, the pixelation downsamples, the BG-boss face icons, the new glyphs | exact and repeatable; the script is the source |
| **D** | A Claude draft, final | the venue thirds' new parts (carrier deck, saloon, town, palace, Edo street, caverns), the stadium, the MUSEUM third, the BG bosses' bodies (Pi-kun, the Yellow Devil, Gamma), Dark Man, Sidewinder, the Daruma, the champions' pinch sets, Eddie, Light, the UI screens (desk, pit stop, maps, title kana, GP badge), chip icons | Claude can lay out tiles that read at 16×16 and keep palettes legal; R5.1 accepts the result as final |

### 11.4 Workload (`budget_r2.py`)

Session model, Claude only, per focused session (the ledger's units):

- **D**: 80 BG tiles, or 12 animated sprite frames (their tiles included);
- **X**: 18 animated frames, their tiles included (1.5× a draft's rate: the outlines and shading are Capcom's), or 150
  tiles for a composite with no new frames;
- **R**: 300 tiles plus 24 frames re-pointed;
- **C**: 200 tiles (writing and tuning the generator);
- **+5 %** for the fixes the art gates ask for (the gate sessions themselves are in the ledger's user-gate overhead).

The model is **calibrated at M4** from the Blizzard slice's real counts (R0.1). The scope critic's own formula
(`tight.py`, round 1) on these counts gives about 53.5; this model is a little lower because it prices composites of
Capcom's frames below fresh drafts, and it adds the gate fixes.

| Tier | R tiles | X tiles | C tiles | D tiles | Frames | Sessions |
|---|---|---|---|---|---|---|
| **Must** | 954 (+ 180 glyphs) | 658 | 495 (+ 60 glyphs) | 2,428 | 354 | **51.6** |
| Should | 113 | 126 | 128 | 1,835 | 114 | 29.7 |
| Could | 32 | 56 | 198 | 926 | 64 | 14.5 |
| **M + S + C** | 1,099 | 840 | 821 | 5,189 | 532 | 95.8 |
| Won't (not built) | 0 | 143 | 20 | 136 | 63 | 4.6 |

By area (Must): the venues 23.5 sessions, the non-venue stages 18.5, the UI 7.5, the player sheets 1.4, the cast 0.8.
**The biggest single Must items**: HIGH NOON FRONTIER's set (5.4 sessions: four thirds, four sprite sets), LOST JUNGLE
(4.5), the Opening (4.1), the Riot's cast (3.8), and Bass β with the NPC Break Man (≈ 2 together, cheap because they are
overlays on Rock's frames). Round 1's biggest items, the 3-size MODE-7 Machine (340 BG tiles) and the 200-tile Gamma,
are gone (R3.6, R2.11).

### 11.5 The art-acceptance gate (R5.1) [new-code] S · Must

At **every milestone** (and at the ⛳ gates M4, M6 and M8 with the user playing):

1. The golden-movie runner (tech §14.4) takes **screenshots of every new screen, set piece and boss**. The mailbox's
   "judges' desk" command (meta §9.6) adds every debrief.
2. artcheck's novelty census adds the **ghost frames** (vanilla dithered, new art in colour) and the ledger's built
   counts per stage against `budget_r2.py`.
3. The results go into **one gallery page for the user** (a published artifact or a local HTML file).
4. The user marks each picture **FINE**, **FIX** (a named problem) or **REDRAW**.
5. FIX and REDRAW items go into the next milestone's art sessions (the +5 %); REDRAW is rare by design, since every asset
   was a placeholder with the final size first.

The gate also answers R5.1's open question in practice: if the user wants a human pass, the gallery shows where it
would pay most.

### 11.6 If a pixel artist joins later (optional polish)

A human pass changes PNGs, not budgets: sizes, tile counts, palettes and frame counts stay, so artcheck and the ledger
still hold. The order in which a human pass pays most:

1. Bass β and Dark Man (the rivals, now overlays);
2. the BG bosses (Gamma, the Yellow Devil, Grand Pi-kun);
3. the stadium and the MUSEUM third;
4. the champions' pinch sets;
5. the Should portraits.

---

## 12. Music and sound

**art_audio owns one track list** (R5.2, consistency-13): every stage doc names its cues by the G-ids below, and nothing
plays that is not here. The rows are `music_r2.py`'s.

### 12.1 Policy

1. **Vanilla themes stay.** Each venue keeps its RM6 stage theme as its main theme, and the champion fights keep `$0C`.
   RM6's eight themes are the champions' identity; the homage is carried by **set-piece cues**, all Should or Could.
2. **Every new track has a vanilla fallback id** (R5.2), so every stage is playable and shippable before its music
   exists. In v1.0 only the 7 Must tracks are new; everything else plays its fallback.
3. **Originals, not quotations.** New tracks are original compositions *in the style* of the homage. The exceptions:
   - **Public-domain melodies** may be arranged: *Korobeiniki* (E1, Could) and the folk song ***Kalinka*** (I.
     Larionov, 1860), which becomes Kalinka the commentator's 3-second sting (G06, Should). Cossack's daughter was named
     after it; now the game admits it.
   - **Capcom's own music** may be arranged, re-sequenced from scratch for RM6's driver: the Hall of Fame tributes
     G08-G12 (each an arrangement of its game's fortress theme, consistency decision 24), Break Man's whistle G27
     (he is Rockman 3's Break Man), and G37's closing phrase. No sound data is imported from other ROMs (BRIEF §7.4).
   - Every third-party style (the arcade shooter, the console RPG, the jungle and the ice-climbing games, the palace
     platformer, the Edo-period action games, the undersea and the arcade classics) is **evoked, never quoted**: scale,
     rhythm, instrumentation, form. **No third-party title appears on screen** (R3.3); the sound test, if it ever ships,
     uses the G-names below.
4. **The MMC5 voices are a layer, never a requirement** (Could). Every 6-channel track must stand alone on the 4 base
   channels (MMC5 AUDIO OFF; an NES-001 without the expansion-audio mod; emulators without it).
5. **Claude writes every track** (R5.1's no-artist baseline extends to music: there is no composer). A human pass is
   optional polish; the tracks that would gain most are G04, G37 and the tributes.

### 12.2 Driver work (tech builds it, §12 there; specified here)

| Id | Change | Why | Size | Tier |
|---|---|---|---|---|
| D1 | **A bank byte per track**; the reader `$34:$803A` maps the track's own bank (CX `$18:97B7`, 4MI `$1E:$8E51`) | new music outside `$34-$36` | S | Must |
| D2 | The track table grows from 102 to **240 ids** (`$00-$EF`), moved to bank `$75` with D1's table | ~100 new ids | S | Must |
| D3 | The instrument table moved (its pointer is at `$34:$8A41`) and grown past 71 entries | new timbres; until then new songs use the 71 vanilla instruments | S | Should |
| D4 | The driver's own bank switch (`$34:$804E-$8060`) ported to MMC5 | the porting checklist | S | Must |
| D5 | **MMC5 pulses**: a second driver instance with its own RAM block (WORK `$6F00`) and register base `$5000`; a COMPANION table starts a 2-channel stream with its track (tech §12.5) | the "16-bit" layer | M | Could |
| D6 | **The hardware multiplier** (`$5205/$5206`) replaces the driver's 8×8 multiply loop `$8006`, its hottest loop (4MI did the same). It belongs to the sound driver only | the driver is 18 % of the frame (`rm6/engine.md` §8) | S | **Must** (tech §12.2; round 1 had it Must only with D5) |
| D7 | **The charge sound on MMC5 pulse 1** (4MI's trick): holding a charge no longer steals a music channel | music never drops notes while charging | S | Could (needs the MMC5 pulses' audio path) |
| D8 | MMC5 AUDIO ON/OFF: OFF mutes `$5000-$5007` and returns the charge sound to its SFX; **default ON** (every track is complete on the 4 base channels, consistency decision 36) | BRIEF §5.7 | S | Could (with D5/D7) |
| D9 | **The channel mute mask** (`MUTE`, one bit per music channel; a muted stream keeps advancing; SFX are not masked; tech §12.6) | **LIGHTS OUT** (§12.9); W1's tiers (Could) | S | **Must** (R5.2, scope-3) |
| D10 | A tempo-override request | E3's formation (Could); Blizzard's bonus countdown (Should) | S | Should |
| D11 | Several ids may enter one song at different offsets (a header pointing into the same channel data) | title/stage/duel cuts for free | S | Must (data only) |
| D12 | DPCM drums | | M | **Won't (v1)**: DPCM fetches from `$C000-$FFFF`, which the C-window switches; if a sample ever ships, it lives in `$7F` (R1.14, consistency decision 36) |
| D13 | A raw-PCM announcer clip | | S | **Won't (v1)** (the conservative reading of the same decision) |

**Id plan**: vanilla `$00-$65` unchanged; the empty stub `$1A` and the unused SFX `$3D/$3E/$4D/$51` are recycled first;
new music `$66-$9F`, new SFX `$A0-$EF`.

### 12.3 Track list: every scene

"v1.0 plays" is what ships; "Upgrade" names the new track and its tier.

| Scene | v1.0 plays | Upgrade (tier) |
|---|---|---|
| License, the health notice | vanilla `$0E`; silence | |
| The attract crawl (Could) | vanilla `$0D` | |
| **Title** | **G01 GP FANFARE → G00 GRAND PRIX MARCH (title cut)** (vanilla `$19` until they exist) | |
| File select | vanilla `$15` | G05 PIT STOP (Should) |
| **Opening-lite** | **G00 (stage cut, D11 entry)** | |
| Grand Pi-kun | vanilla `$0C` | |
| Bracket | vanilla `$0F` (the stage-select theme *is* the bracket's, consistency decision 36) | |
| Boss panel | vanilla `$10` | |
| Venue stages | vanilla `$00-$07` | the venue cues (§12.4): Should and Could |
| Champion fights, the secret arenas | vanilla `$0C` | |
| HERO'S QUEST's ENCOUNTER | vanilla `$0C` (venues_a asked art to pick the id) | G23 ENCOUNTER (Should) |
| Boss defeated / YOU GET | vanilla `$13` / `$16` | |
| **The judges' desk** | **G02 THE JUDGES + G03 MEDAL STAMP** (4 ids, D11) | |
| Pit stop | vanilla `$15` | G05 PIT STOP (Should) |
| A commentator pop-up | the pop-up chime (SFX) | G06 KALINKA! (Should) |
| **HALFTIME RIOT** | **G04 BETA, stage entry** | G38 RIOT (Should: a G04 remix with the rejects' crowd chant; fallback G04, then `$0B`) |
| **Bass duels 1 and 2, the W2 final** | **G04 BETA, duel entry** | |
| **The NPC Break Man's beats** (the Riot's help and reveal, H3's music box at the statue, S40 over the white, the Opening's tip after a death to Pi-kun) | **G27 WHISTLE** (2 s) | |
| The Hall of Fame map | vanilla `$11` | G07 HALL OF FAME (Should) |
| H1, H3, H5 | vanilla `$09` | G08, G10, G12 tributes (Should) |
| H2, H4 (Should) | vanilla `$09` | G09, G11 (Should) |
| The MK-VI fights, Big Eye, the Kamegoro Maker | vanilla `$0C` | G13 LEGACY BOSS (Should) |
| The unmasking | vanilla's Mr. X reveal cue, kept | G33 MR. Y (Could) |
| The castle map | vanilla `$12` | |
| W1 (Could) | vanilla `$0B` | G14 UPGRADE LAB (Could, the POCKET / NES tiers through D9), G14x MMC5 voices (Could) |
| W2 | vanilla `$0B`; the refights `$0C`; the final G04 | G34 16-BIT WILY STAGE (Could, MMC5) |
| W3: the Trophy Dispenser, WILY MACHINE 6.5, the Capsule | vanilla `$18` | G15 FINAL CHAMPIONSHIP (Should); G15x, G35 (Could, MMC5) |
| **The escape** | vanilla `$18` | **FINAL LAP = G15's escape entry (D11)** (Should, fallback `$18`) |
| The ending: pixelation, the catch, the arrest | vanilla `$08` (and the scene cues `$1B-$22`) | |
| The podium and Bass's vow | vanilla `$17` | G16 CHAMPION (Should) |
| The CAPCOM TIMES, the credits | vanilla (their own cues) | |
| The rating and Break Man's debrief | G01's sting, then G02 | |
| **LIGHTS OUT** (S42) | **G37 LAST MATCH** on the 2A03, with D9 | G37x MMC5 stems (Could) |
| The sixth wing, TO BE CONTINUED | **silence** (pulse 1 stays the last sound, R4.1) | |
| The victory lap (Could) | vanilla `$0A` | G17 VICTORY LAP (Could) |
| Game over, continue | vanilla `$14`, `$15` | |
| Mr. Y's booth (Could, the bundle) | vanilla `$09` | G33 MR. Y (Could) |
| The Exhibitions (Could) | vanilla `$0C` | G18-G20 (Could); G21 is Won't with E4 |
| Bass Mode | | G36 (Won't) |

Fortress's names map to these ids (consistency-13): GP STADIUM = G00's stage cut; RIOT = G04's stage entry in v1.0 and
G38 when it ships; FINAL LAP = G15's escape entry. Round 1's "HALL OF FAME theme in 5 arrangements" is withdrawn in
favour of G08-G12 (fortress §0.12 agrees).

### 12.4 The venue cues (homages evoked; all Should or Could)

| Venue | Main theme | Set-piece cue (tier) | Style in driver terms |
|---|---|---|---|
| SKY ACE | `$00` | **G22 SORTIE** (Should); POW / LOOP / ACE stingers in G28 (Should). v1.0: the ACE fanfare and the DRAW bell are vanilla SFX | Capcom's own 1940s arcade-shooter march: driving 16ths on the triangle, pulse 2 an "engine drone" with a slow detune wobble (cmd `0C`), a 50 % duty heroic lead in a minor key |
| HERO'S QUEST | `$07` | **G23 ENCOUNTER** (Should; v1.0 swaps to `$0C`); inn and level-up stingers (Could) | a short baroque-flavoured battle loop: a running 16th bass on the triangle, a fanfare lead, no borrowed phrases |
| HIGH NOON FRONTIER | `$06` | **G24 4:50 TRAIN** (Should), the duel stinger in G28 (Should), G32 HONKY-TONK (Could) | a galloping 2/4 shuffle, a "harmonica" lead on 12.5 % duty with slides (cmd `0D`), a whistle slide, chugging noise |
| LOST JUNGLE | `$04` | G29 LOST CAVERNS (Could) | a 1970s-console flavour: square leads on a deliberately "out of tune" scale (per-note detune), sparse, no triangle |
| SUMMIT CLIMBER | `$01` | **G25 BONUS SUMMIT** (Should; a loop, so CASUAL's +50 % meter needs no new music, §4.10) | a 40-s bonus-round romp: staccato bells (12.5 % duty, short gate), oom-pah triangle; D10 speeds it up in the last 10 s |
| PERSIAN PALACE | `$03` | G31 PALACE (Could) | harmonic minor, slow 6/8, triangle drone, sliding pulse ornaments: the mood of the palace-platformer genre, no regional pastiche (R3.4) |
| ATLANTIS RUINS | `$05` | G30 UNDERWATER (Could) | slow minor arpeggios in triplets (cmd `00`), the second pulse as an echo |
| EDO NINJA ROW | `$02` | **G26 KABUKI** (Should, with the revolving stage; v1.0's 1D plays `$0C`) | yo / in pentatonic, a plucked 25 % pulse with a short gate (shamisen), noise clappers that accelerate, a pitch-swept triangle taiko |
| E1 Block Man | | G18 KOROBEINIKI REMIX (Could) | the PD folk song at 160 bpm, our own arrangement |
| E2 Paddle Man | | G19 BRICK FUNK (Could) | a syncopated bass and a hi-hat noise groove |
| E3 Invader Man | | G20 FORMATION (Could) | a 4-note bass ostinato (original notes) whose tempo follows the formation (D10) |

### 12.5 The new tracks and their bytes (`music_r2.py`)

Sizes are estimated from vanilla (`songsizes.py`): a stage theme 617-1,238 B (mean 1,010), a fortress stage 788-871, a
boss 633, the Wily Machine 575, jingles 116-260, ending scenes 349-546. MMC5 companions add about 50 %.

| # | Track | Bytes | Tier | Fallback |
|---|---|---|---|---|
| G00 | GRAND PRIX MARCH (title and stage cuts) | 1,150 | **Must** | `$19` / `$0D` |
| G01 | GP FANFARE | 180 | **Must** | `$16` |
| G02 | THE JUDGES | 420 | **Must** | `$15` |
| G03 | MEDAL STAMP (4 ids) | 190 | **Must** | `$13` |
| G04 | BETA (stage and duel entries) | 1,050 | **Must** | `$0B` |
| G27 | WHISTLE (2 s) | 110 | **Must** (R5.2; round 1: Should) | silence |
| G37 | **LAST MATCH** (4 stems, §12.9) | 600 | **Must** (R5.2, consistency-13) | `$08` with no channel drop |
| G05-G07 | PIT STOP 520, KALINKA! 90, HALL OF FAME 520 | 1,130 | Should | `$15`, the chime, `$11` |
| G08-G12 | the five tributes, 900 each (G09 and G11 ship with H2 and H4) | 4,500 | Should | `$09` |
| G13 | LEGACY BOSS | 650 | Should | `$0C` |
| G15 | FINAL CHAMPIONSHIP, with the FINAL LAP entry | 1,000 | Should | `$18` |
| G16 | CHAMPION (the podium) | 700 | Should | `$17` |
| G38 | RIOT | 900 | Should | G04, then `$0B` |
| G22-G26 | SORTIE 1,000, ENCOUNTER 600, TRAIN 900, BONUS 400, KABUKI 800 | 3,700 | Should | the venue's theme or `$0C` |
| G28 | 8 stingers (duel bell, POW, LOOP, ACE 100 %, secret found, plate, inn, level-up) | 600 | Should | vanilla SFX |
| G14 / G14x | UPGRADE LAB 1,100 / its MMC5 voices 550 | 1,650 | Could (with W1; R5.2 lists the POCKET arrangements as Should, but they have no user until W1, which is Could) | `$0B` |
| G15x, G37x | MMC5 voices for G15 and G37 | 800 | Could | the 2A03 track |
| G17 | VICTORY LAP (one lap) | 1,100 | Could | `$0A` |
| G18-G20 | the Exhibition themes (750, 700, 500) | 1,950 | Could | `$0C` |
| G29-G33 | LOST CAVERNS 600, UNDERWATER 700, PALACE 700, HONKY-TONK 500, MR. Y 350 | 2,850 | Could | the venue's theme, `$09` |
| G34, G35 | 16-BIT WILY STAGE 1,300, 16-BIT WILY MACHINE 900 (MMC5) | 2,200 | Could | `$0B`, `$18` |
| G21, G36 | CHASE (E4), BASS MODE | 1,500 | **Won't (v1)** | |
| | **Total** | **Must 3,700 (7); Should 13,180 (18); Could 10,550 (15)** | | |

### 12.6 SFX

New SFX are 8-40 B each (vanilla's mean is 29 B). SFX priorities follow the vanilla rule (a new SFX plays only if its
priority ≥ the current one, `rm6/engine.md` §5.2): UI and crowd SFX get low priority, so they never cut a weapon sound.

- **Must, new (21, 392 B)**, packed into the `$36` tail (449 B, reserved for SFX by R1.14), with 57 B to spare:
  - the menus and judging: the weapon-cycle tick, the results row tick, the total roll, the medal-stamp thunk (also
    `ACCEPTED!`), shop buy, shop deny, the chip click, the pop-up chime;
  - combat: the form-swap whoosh, the WEAK! crunch, the EXCELLENT MOVE chime (KAISHIN);
  - the crowd: a cheer (a noise swell) and an "ooh" on a death;
  - the stages: the head bonk and the ice-cell break (Blizzard), the **mouse squeak** (Flame's Must hidden room,
    venues_b), the **referee's whistle** (the escape clock), the high striker's DING and the HIGH FIVE slap (the
    Opening), the pogo boing (Yamato);
  - **the speaker blips**: 4 pitch variants of vanilla's typing blip (`$06A6`'s mechanism, story's per-speaker blips).
- **Must, vanilla ids reused (15, 0 B)**: gate rumble, plate click, door unlock, chest open, the gunshot, the DRAW bell,
  the ACE fanfare, thunder, knock, the press shake, the rocket-fist launch and return, the jet hop, the M.BEAM build,
  the dink (`$27`), the heal tick (`$31`). Each id is picked at M2 from `songdec.py`'s list.
- **Should (35, ≈ 0.9 KB)**, each with a vanilla fallback in v1.0: catapult, POW change, loop whoosh, gust, lamp, menu
  blip, spell, train whistle, ricochet, bounty stamp, croc snap, log roll, tar bubble, vine creak, cat, seal push, condor
  cry, door fade, siren, slot reel, chirp, scroll spin, wooden clappers, daruma chime, chomper "shing", the bell scale
  and the claw's ding-ding (H4), crane motor, dragon roar, appearing-block pip, engine rev, the M.BEAM hum, new
  rocket-fist and jet-hop sounds, Break Man's call.
- **Could**: the parry "ting" (the parry is Could, R2.4), crowd gasp, piano plinks, line clear, ball bounce, brick
  break, saucer whine.
- **Won't**: the "pikoon" critical (criticals are Won't); the hanabi fuse and burst (R3.1).

### 12.7 Composition pipeline: MML → driver bytecode (tech §12.3)

tech builds `mml.py` with its dialect (1:1 onto commands `$00-$18`) and gates it on **a byte-exact round trip of all 36
vanilla tracks**. art_audio writes in it:

- Music: `assets/music/<id>.mml`, one file per G-id, with D11 entry labels for the cuts (title / stage / duel /
  escape).
- SFX: vanilla's format (a priority byte + a register stream), written as YAML register frames.
- **Checks** (`sndtest`, with tech's harness): every new track plays alone and **under each fallback swap**. Its driver
  cycles per frame must not exceed the busiest vanilla track: the driver is already 18 % of the frame (D6 helps).
  Every track is complete on the 4 base channels.
- **Every set-piece cue is a loop with no timed ending** (§4.10), so CASUAL's +50 % timers never need a new track.
- `fms2mml.py` (a FamiStudio import, for a human composer) is Could (tech).
- The packer places each track wholly inside one music bank, fills D1's bank table, and prints the free bytes per bank.

### 12.8 Byte budget against the banks (tech §1.2, §12.4)

| | Bytes | Where |
|---|---|---|
| Vanilla music + SFX (kept) | 20,728 | `$34-$36` (unchanged) |
| **Must SFX** (21 new) | **392** | the `$36` tail (449 B; 57 spare) |
| **Must music** (7 tracks) + the track table v2 (240 × 3 B) | **3,700 + 720** | bank `$75` |
| Should music + SFX | 13,180 + 864 | the rest of `$75`, `$76`, the start of `$77` |
| Could music + SFX | 10,550 + 184 | `$77-$78` |
| **Total new, all tiers** | **≈ 29.6 KB** | **4 of tech's 5 banks `$75-$79`**; v1.0 fills about 4.4 KB of `$75` |

For scale: vanilla RM6 has 18.8 KB of music; CX added 38 songs in 3 banks; 4MI 47 songs in 36 banks of gaps.

### 12.9 LIGHTS OUT: G37 LAST MATCH [new-music] S · Must (R4.1, R5.2; story S42, fortress §6.1 scene 9)

**What it is.** The GP's own march, G00, the first thing the tournament played, slowed to half tempo and re-voiced as
**four stems, one per 2A03 channel**: the melody on pulse 1, the harmony on pulse 2, the bass on the triangle, the
brushes on the noise. Its last phrase quotes vanilla RM6's ending theme `$08` (Capcom's own music, §12.1), so the
farewell is to this very game.

**How it plays** (fortress stages it; story owns the scene and its words):

1. The six floodlight towers go dark one by one. **Each takes a music channel with it** through D9: the MMC5 voices first
   (G37x, Could, only if they ship and are on), then noise, triangle, pulse 2. No DPCM cue (consistency decision 25).
2. **Pulse 1 plays the melody alone**, and the last tower goes dark on its last note.
3. Muted streams keep advancing (tech §12.6), so a channel never drifts out of time.
4. **Sync**: G37 carries a marker at the end of each stem's last phrase (the `F n` flags command `04`, or a frame-count
   table if the flag is unsuitable; tech decides at M2). The scene script reads it to switch the next tower off and set
   its `MUTE` bit, so the picture follows the music, never the reverse.
5. **The last sound is pulse 1 alone** (R4.1). D9 does not mask SFX, so the scene plays **no SFX after the first tower
   goes dark**, the sixth wing that follows is silent, and TO BE CONTINUED types without blips (fortress §6.1).

**Fallback** (never shipped, but keeps the ending playable while G37 is written): vanilla `$08` with no channel drop.

**Reading R1.3's "music channel drop"** for W2, W3 and the escape: in v1.0 the console's channels are **kept** for LIGHTS
OUT, so its gag is not spent early. The escape drops only the MMC5 voices, at 09 and 0A, if they ship (Could; fortress
§5.4; tech §12.5 reads R1.3 the same way). This is the conservative reading; §18 asks the director to confirm it.

---

## 13. Totals (the ledgers: `budget_r2.py`, `music_r2.py`)

### 13.1 Art

| Tier | BG tiles | Sprite tiles | CHR tiles | 1-bpp glyphs | Frames | Sessions | CHR |
|---|---|---|---|---|---|---|---|
| **Must (v1.0)** | 2,567 | 1,968 | **4,535** | 240 | **354** | **51.6** | 70.9 KB |
| Should | 1,684 | 518 | 2,202 | | 114 | 29.7 | 34.4 KB |
| Could | 828 | 384 | 1,212 | | 64 | 14.5 | 18.9 KB |
| **All tiers built (M+S+C)** | 5,079 | 2,870 | 7,949 | 240 | 532 | 95.8 | 124.2 KB |
| Won't (not built) | 20 | 279 | 299 | | 63 | 4.6 | |

| By area (Must) | BG | Sprite | Frames | Sessions |
|---|---|---|---|---|
| The 8 venues (§4) | 1,086 | 1,002 | 188 | 23.5 |
| The non-venue stages and their bosses (§5-§7) | 944 | 640 | 123 | 18.5 |
| Player sheets and weapon tiles (§7.1, §2.4) | 0 | 114 | 23 | 1.4 |
| Cast (§7.3) | 0 | 44 | 11 | 0.8 |
| UI (§9) | 537 | 168 | 9 | 7.5 (with the 240 glyphs) |

**Round 1 → round 2 (Must)**: 4,851 → 4,535 CHR tiles; 421 → 354 frames; ≈ 660 human hours → 51.6 Claude sessions.
The cuts (Pi-kun's sizes, the 3-size machine, the full Gamma, portraits, Exhibitions, H2/H4/W1, the second set pieces)
outweigh the additions (the mid-bosses, the rejects, the MUSEUM third, SET-PARADE, the face icons, the venues' promoted
chips and tells).

**ROM, against tech's ledger** (tech §1.2):

| Ledger row | v1.0 | All tiers | Note for tech |
|---|---|---|---|
| CHR source `$54-$61` (14 banks, 112 KB) | **≈ 9 banks** (70.9 KB) | ≈ 15.5 banks (124.2 KB) | the full design overflows by ≈ 780 tiles; **the vanilla gap reserve** (§1.3: 1,126 blank tiles outside Capcom's sets; filling blanks overwrites no art, BRIEF §7.4) absorbs it. So **no CHR bank can leave this row** for text; text's possible 10th bank should come from the music row (below) |
| Sprite bank pairs `$4E-$53` (3 pairs) | 1 pair is enough for 354 frames; use 2 (venue objects; bosses, player, cast, UI) | 2 pairs (532 frames, ≤ 512 per pair) | the 3rd pair is spare |
| Tileset slots `$62-$6E` (13 banks) | 14 slots in 7 banks | 26 slots in 13 | as tech §5.3 |
| Music `$75-$79` (5 banks) | ≈ 0.55 bank (4.4 KB) | ≈ 3.6 banks (29.6 KB) | **`$79` stays spare in the full design**: the natural donor if text needs a 10th bank |
| `$36` tail (449 B, SFX only) | 392 B | 392 B | 57 B spare |
| Text banks (glyphs) | ≈ 2 KB of 1-bpp glyphs in T1 | | the glyph set is art; the format is tech's |

### 13.2 Audio

| Tier | Tracks | Music bytes | New SFX | SFX bytes | Sessions |
|---|---|---|---|---|---|
| **Must** | **7** (G00-G04, G27, G37) | **3,700** | **21** (+ 15 vanilla ids) | **392** | **9** |
| Should | 18 | 13,180 | 35 | 864 | 26.4 |
| Could | 15 | 10,550 | 7 | 184 | 19.1 |
| Won't | 2 (G21, G36) | 1,500 | | | |
| Driver work (tech's sessions) | D1, D2, D4, D6, D9, D11 Must; D3, D10 Should; D5, D7, D8 Could; D12, D13 Won't | | | | |

### 13.3 art_audio's sessions in the ledger

| | Must (v1.0) | Should | Could |
|---|---|---|---|
| Art | 51.6 | 29.7 | 14.5 |
| Music + SFX | 9 | 26.4 | 19.1 |
| **Total** | **60.6** | **56.1** | **33.6** |

`tools/plan/tight.py` carries art 51.6 and music 9 (its tight Must total stays at about 450).
`tools/plan/tally.py` carries all four tiers of both. Re-estimated at M4 from the Blizzard slice's real counts (R0.1).

---

## 14. Build list

| Item | Tags | Size | Tier |
|---|---|---|---|
| CHR set table v2 + stage-local ids (§2.1; tech builds) | [new-code] | S | Must (M2) |
| The tileset-slot table's content (§2.2; tech owns the table) | data | S | Must (14 slots); Should (H2/H4 and the venues' second slots); Could (TS_LAB, TS_ARCADE) |
| Section switch to slot B (§2.2) | [new-code] | S | Should |
| GP-COMMON (W, K, !, swap flash, CENTURION, spare) (§2.4) | [new-art] | S | Must (M2) |
| The slot sets: the Ice Block's 4 tiles, M.BEAM's set, the Super sheet's slot tiles (§2.4) | [new-art] | S | Must |
| Alt and synergy tiles (§2.4) | [new-art] | S | Should (R2.4) |
| Set-piece player sheets: the sortie, the pogo (§2.4) | [new-art] | S | Must; the swing poses Should; Eggplant-Rock Could |
| Rebuilt champion sets + 8 pinch sets (§2.5) | [new-art] [new-code] | M | Must |
| ExGrafix in W1's locked rooms and the METALL 16 arena (§2.7) | [new-code] [new-art] | M | Could (R1.3) |
| Pattern-table split for menus (§2.8; tech's `RL_SPLIT_PT`) | [new-code] | S | Must (M5) |
| Venue art, 8 venues: thirds, sets, pinch sets (§4) | [new-art] | L | Must (as tiered per row) |
| Opening-lite and HALFTIME RIOT art on TS_STADIUM (§5.1-§5.2) | [new-art] | L | Must |
| The MUSEUM third, H1/H3/H5 art, the trophy theft's claw (§5.3) | [new-art] | M | Must |
| W2/W3/escape art, SUPER palettes (§5.4) | [new-art] | M | Must |
| The ending's pictures and the podium (§5.5) | [new-art] | S | Must |
| BG bosses at one size: Pi-kun, the Yellow Devil, Gamma (head and fists), WILY MACHINE 6.5's retint (§6) | [new-art] | M | Must |
| Pi-kun's S/L sizes, THE APPROACH's sizes, Mecha Dragon, Cossack Catcher, AYACO BG (§6) | [new-art] | L | Should |
| METALL 16, the 16-bit Capsule (§6) | [new-art] | M | Could |
| Super Rock sheet (§7.1) | [new-art] | M | Must (with H3) |
| Bass β (composite, 4 pre-drawn copies), the NPC Break Man, Dark Man + disguise, Big Eye, the re-skins (§7.2) | [new-art] | M | Must |
| Break Man's playable sheet (§7.1) | [new-art] | M | Should (with the partner) |
| Cast: Eddie, Roll, Light, Mr. Y (§7.3) | [new-art] | S | Must; Cossack/Kalinka bodies Should |
| Exhibition guests and arenas (§8) | [new-art] | M | Could (E4 Won't) |
| Title: GP badge, subtitle, split menu (§9.1) | [new-art] | M | Must |
| File cards, bracket, Bass β's centre frame, boss-panel glyphs (§9.2) | [new-art] | M | Must; match-card portraits Should |
| Judges' desk, medal stamp, secret icons, rating screen (§9.3) | [new-art] | M | Must; the sponsor's chair Should |
| **22 face icons** (§9.4) | [new-art] | S | Must |
| Portraits (10 + Mr. X) (§9.4) | [new-art] | M | Should (Mr. X Could) |
| Pit stop, 14 chip icons, envelope icon (§9.5) | [new-art] | M | Must; W-tank Should; bundle icons Could |
| Text window frame + the 1-bpp glyph set, ALL CAPS (§9.6) | [new-art] | S | Must (M2) |
| HUD labels, pause icons (§9.7) | [new-art] | S | Must |
| Maps, rating plates (§9.8) | [new-art] | M | Must; wing emblems Should; achievements Could; the attract crawl's pictures Could |
| artcheck's art checks 1-13 and the gallery for the art gate (§10.5, §11.5) | [new-code] tools | M | Must (tech builds; art supplies the data) |
| `sprites.py` overlay composites (§10.4) | [new-code] tools | S | Must (tech) |
| Driver D1, D2, D4, D6, D9, D11 (§12.2) | [new-code] | S | Must (tech, M2) |
| Driver D3, D10 | [new-code] | S | Should |
| Driver D5, D7, D8 (the MMC5 voices) | [new-code] | M | Could |
| Driver D12 (DPCM), D13 (PCM voice) | [new-code] | M | Won't (v1) |
| Music G00-G04, G27, G37 + 21 Must SFX (§12) | [new-music] | M | Must |
| Music G05-G13, G15, G16, G22-G26, G28, G38 + 35 SFX | [new-music] | L | Should |
| Music G14, G14x, G15x, G17-G20, G29-G35, G37x + 7 SFX | [new-music] | M | Could |
| G21, G36 | [new-music] | M | Won't (v1) |

---

## 15. Cross-doc dependencies (single sources of truth)

| Doc (what it owns) | What this doc takes from it, and asks of it |
|---|---|
| `tech.md` (ids, memory, raster, CHR, tilesets, the bank ledger) | **Takes**: the stage ids (R1.2); the tileset-slot table (§5.3), which §2.2 regenerates; the CHR set table v2 (§7.6); the stream rates (§15.3); the glyph strip (§11.4: ≤ 24 glyphs + 4 icon tiles); `RL_FLOOR`, `RL_FLOOR8`, `RL_PALBAND`, `RL_SPLIT_PT` (§8.3); the HUD widget limits (§7.13); the lag cap and its count (§15.1); ExRAM in mode 0 (§3.3); the driver extension (§12). **Asks**: (1) **confirm the CHR row**: v1.0 ≈ 9 of 14 banks, the full design ≈ 15.5 with the vanilla gap reserve, so text's possible 10th bank comes from music's spare `$79`, not from CHR (§13.1; tech open question 6 asked for this re-run); (2) 2 sprite pairs suffice (the 3rd is spare); 14 / 26 tileset slots confirmed; (3) `sprites.py` overlay composites (§10.4); (4) artcheck's new checks 8-13 (§10.5) and the gallery for the art gate (§11.5); (5) G37's sync marker: command `04`'s flag or a frame table (§12.9); (6) the SFX player reads through the same reader as music, or the 21 Must SFX must stay in the `$36` tail (they do: 392 of 449 B) |
| `systems.md` (combat, economy, chips) | **Takes**: the per-form `$71-$7F` map and the weapon sets' sizes (§1.4); `gp_player_sheet` (§1.4); the 16-f swap (§1.3); the 14 chips (§9.2); WEAK! (§5) via tech's family `$FD`. **Gives**: GP-COMMON's 6 tiles (W, K, !, the swap flash, CENTURION, a spare); no CRIT! tiles; `?!` with SC3 (Could); the Ice Block's 4 tiles; M.BEAM's set ≤ 15; the Super sheet (Must with H3, its slot tiles ≤ 15); the 14 chip icons and the envelope icon (W-tank Should, PART icons with the bundle); the Must SFX it asked (the cycle tick, the WEAK! crunch, the KAISHIN chime; the parry ting is Could); **G27 WHISTLE is Must** (R5.2) |
| `meta.md` (save bytes, bracket, events, debrief) | **Takes**: every screen's contents and order. **Gives**: the title plan (the GP badge, the subtitle, the split menu at M5, a plain menu before); the file cards with face icons; the bracket with vanilla portraits and Bass β composited in the cracked frame; the desk with Cossack's and Kalinka's face icons and name labels (desk portraits Should); the sponsor's chair (Should); **the rating screen over the desk** in v1.0 (meta §6.1); the participation ribbon; the maps with H2, H4 and W1 drawn closed; the lobby screen on TS_STADIUM (Could, no slot); G01 for the title and rating (vanilla `$19` until then); MMC5 AUDIO defaults ON when D8 ships (Could) |
| `venues_a.md` (Wind, Knight, Tomahawk, Plant staging) | **Adopted**: every v1.0 delta of its §1.1/§2.1/§3.1/§4.1: the seagull is Must; the windsock is BG; the loop poses go into the sortie's set-piece sheet; Wind's pinch set is 24; W-SEA drops the destroyer (Should); SET-WS5 is Should; Knight's inn bed, Princess, Innkeeper and heart are Should and the sconce is Won't; **T-MESA** replaces T-BOOTHILL (Must); T-RODEO is Should; the cactus walker is Must; the flag judge joins SET-TM3 and "HEY!" joins SET-TM2; Plant's 12-tile vine set is dropped; the tar bubbles are BG; the eel is Should. **Music**: no new venue track in v1.0; the encounter plays `$0C`; the DRAW bell and the ACE fanfare are vanilla SFX |
| `venues_b.md` (Blizzard, Flame, Centaur, Yamato staging) | **Adopted**: the change lists of §1.8, §2.6, §3.8 and §4.7 (hanging icicles as BG, the condor on ladder poses, the snowman and snowball Should, the mouse and the marshal Must, 2 chandeliers, no minarets or crescent, the plaque digits as BG, the Centurions Must, the Daruma and the pogo rack Must, the pogo poses in a set-piece sheet, Yamato's cut cast Won't). **The mouse squeak is a Must SFX** (16 B). Cue tiers as asked: G25, G26 Should; G30, G31 Could. **The Blizzard fight's flicker check** is §3.5's row, with an AI fallback that venues_b decides |
| `fortress.md` (non-venue staging, boss techniques) | **Adopted**: every asset and technique of its §9.6 and §1-§6 (§5-§6 here), the orange scarf, one size per BG boss, the vanilla Wily Machine 6 retint. **Asks**: (1) **Eddie is new art**, not a vanilla sprite (its §1.2 lists him under vanilla sprites); (2) **the podium cannot show eight champion sprites at once**: 12 occupied slots against the cap of 9, and 8 palettes against 2 (§3.5). Art recommends the champions applauding **in pairs** (0 new tiles); the all-eight BG row is Should; (3) the rating screen draws over meta's desk (its §6.1 scene 8 says the stadium at dusk; meta owns the screen); (4) G37's sync is driven by the music (§12.9); (5) the SFX it asked: the DING, HIGH FIVE and the referee's whistle are new Must SFX, the knocks and the press shake are vanilla ids, the bell scale and the claw's ding-ding are Should with H4; (6) the trophy theft's claw is Must art here and H4's Catcher reuses it; (7) if THE APPROACH returns, its L pose is ≤ 150 tiles with the background blanked and no glyph window (feasibility-16) |
| `story.md` (every word, the ending) | **Gives**: face icons for its 7 POP speakers (Light as a radio frame) plus Rock, Bass β, Eddie and the champions; portraits are Should (Mr. X Could); the boss panel's bold `- ? ! ' β` and the VENUE strip; the plaque frame is the window frame (no art; the wing emblems are Should); the trophy theft's claw on Mr. Y's pod; **one** CAPCOM TIMES headline in v1.0 (the doped one is Could); 4 speaker blips; **G37 LAST MATCH** with one stem per channel; **no mixed-case EN set** (its §10.3); no DPCM cue. The attract crawl's three pictures are Could (R0.3 item 12). **Asks**: the S42 cue table follows §12.9's order (MMC5 first if on, then noise, triangle, pulse 2, pulse 1); S42's "already silenced when the castle fell" applies only to the MMC5 voices |

---

## 16. Lessons applied

- **CX 1 (one premise)**: the GP shows up in the art and audio itself: the stadium march, the judges' desk, the medal
  stamp, the bracket lines, the crowd SFX, Kalinka's own folk song (Should), and LIGHTS OUT ending on the march that
  opened the GP.
- **CX 2 (a guest is a mechanic)**: §8's guests make the rule readable at a glance; the venue sets carry their homage's
  rules (the lamp board, the gallery windows, the tar pits).
- **CX 3 / "big things in the background"**: every boss bigger than 32×32 is nametable art (§6), at one size.
- **CX 5 (watch the per-line budget)**: §3.4's flicker budget, §3.5's recount and §10.5's simulator; repeated hazards
  are BG.
- **CX 6 (jokes can be graphical)**: Mr. Y is Mr. X with a moustache; Dark Man is Break Man with the wrong scarf; the
  2600 canopy; the castle picture's green ramp; the pixelating castle.
- **CX 7 (mind the junk)**: artcheck rejects overlapping sets, oversize slot sets and unreferenced loads.
- **CX's quick-hack honesty** (scope-7, R5.1): 71 % of CX's reused sprites are recolours; GP counts its own reuse
  honestly (R and X) and builds Bass β and Break Man from Rock's frames.
- **4MI 2 (spend new pixels on set pieces and bosses)**: stages keep their vanilla sets; thirds carry the homage.
- **4MI 3 / 4 (art is portable; never overwrite)**: vanilla CHR banks stay byte-identical (§10.5 check 6); the gaps
  are a reserve that the full design may need (§13.1).
- **4MI 5 (BG boss + sprite parts)** and **4MI 6 (status labels)**: §6, §9.7.
- **4MI 7 (per-message canvas)**: the glyph strip with the face icon inside it (§9.4, §9.6).
- **4MI 8 (palette tricks double the content)**: §3.2's list; the SUPER colour of W2/W3 is palettes and bands.
- **4MI engine (MMC5)**: the hardware multiplier in the driver (D6, Must); the charge sound on MMC5 pulse 1 (D7, Could).
- **RM6 lesson 2 (the block table is the binding budget)**: §2.2's block counts per slot.
- **RM6 lesson 5 (per-screen sprite CHR conflicts)**: measured (§1.4) and enforced (§10.5); every venue set placed.
- **RM6 lesson 8 (keep quirks)**: C.FLRSH stays on the YOU GET card; TO BE CONTINUED keeps its place, now in silence;
  the vanilla staff roll carries the credits.

---

## 17. Risks

1. **No pixel artist, now the baseline** (R5.1). Claude's drafts ship as final.
   - The weak spots are the D-heavy items with personality: Dark Man, Gamma's head, the Yellow Devil, Grand Pi-kun, the
     stadium.
   - *Mitigation*: reuse and composites first (36 % of Must tiles); the gate with ghost frames at every milestone
     (§11.5); the fallback list in "v1.0 scope"; a human pass later replaces PNGs without touching budgets (§11.6).
2. **Art over R5.1's target**: 4,535 tiles against about 3,900 (sessions 51.6 against about 50), and the session model
   is a guess until M4.
   - *Mitigation*: the 9 art-side fallbacks (≈ 4 sessions) keep every mechanic; the M4 calibration re-sizes the model
     from the Blizzard slice.
3. **8 KB of CHR-RAM is the real limit.** Pop-ups need free BG ids that dense venue screens lack (Plant has 0), so lines
   wait.
   - *Mitigation*: boss rooms always have room (§1.4); P1 lines show on READY; the free-id map flags the gaps at build
     time (tech §6.3 check 9).
4. **2-KB streams** (form swaps, set-piece sheets, Super Rock) take 11-22 frames at tech's rates.
   - *Mitigation*: systems' fixed 16-f swap behind the flash; set-piece sheets stream only at locked moments.
5. **Champion pinch sets** need each boss set rebuilt; Wind, Yamato and Knight have 0 free tiles, so some vanilla frames
   must go.
6. **Sprite-set conflicts** are tight in SUMMIT CLIMBER, PERSIAN PALACE and HIGH NOON FRONTIER (§4): a late layout change
   can break a screen. artcheck runs from the first venue build (M4).
7. **Multi-character scenes** hit two limits at once: 2 enemy palettes and 9 slots (§3.5).
   - The podium is the case found so far.
   - *Mitigation*: pairs, staggering, BG rows; artcheck's slot and palette checks run on cutscenes too.
8. **The CHR ledger is full in the full design** (≈ 15.5 of 14 banks).
   - *Mitigation*: the vanilla gap reserve; the Should and Could rows are re-totalled at every ⛳ gate (R0.1).
9. **Composites can read as palette swaps of Rock.**
   - *Mitigation*: every composite adds silhouette parts on every frame (fins, visor and scarf, the crash-test
     markers), and the gate checks them at M6.
10. **Driver cost**: the sound driver is already 18 % of the frame.
    - *Mitigation*: D6 is Must; no new track may exceed the busiest vanilla track's cycles (`sndtest`); D5 never ships
      without D6.
11. **Quotation risk**: the RM1-5 tributes (Should), the whistle and G37's coda arrange Capcom's own music, which is fan-hack
    tradition (CX and 4MI did the same with RM2/RM4). Every third-party homage stays evoked; the two folk songs are
    public domain.
12. **MMC5 audio reach** (Could): an NES-001 without the expansion-audio mod and some flash carts play no MMC5 sound. The
    4-channel rule keeps every track complete.

---

## 18. Open questions

1. **(User, R5.1, RULINGS §7 Q2)** Will a pixel artist join (now, later or never)? This plan assumes never. The gallery
   of §11.5 shows where a human pass would pay most.
2. **(Director)** R1.3's "the music channel drop" in W2, W3 and the escape: confirm the conservative reading (§12.9). The
   console's channels are kept for LIGHTS OUT; only the MMC5 voices drop at the escape, and only if they ship. fortress
   and tech read it the same way.
3. **(Director)** R5.2 lists "the POCKET arrangements" as Should, but their only user is W1, which is Could. This doc
   tiers G14 Could with W1; confirm.
4. **(fortress)** The podium in pairs (recommended), or the all-eight BG row promoted from Should?
5. **(tech)** The CHR row (§13.1): confirm 9 banks for v1.0, the gap reserve for the full design, and music's `$79` (not
   CHR) as text's spare.
6. **(tech)** G37's sync: the `04` flags command, or a frame-count table?
7. **(User)** The art gate's gallery: a published page (private by default) or a local HTML file per milestone?
8. **(tech, Could)** Which emulator and hardware matrix decides "MMC5 audio works", for D8's default? (It defaults ON,
   since every track is complete without it; consistency decision 36.)

**Resolved since round 1** (consistency decision 36 and the rulings):

- 32 KB CHR-RAM: no (tech D6, R1.3).
- `$C000` stays switchable (the C-window), so DPCM is Won't (v1).
- Deferred pop-ups are accepted except P1 lines.
- The Hall of Fame plays arrangements of each RM1-5 fortress theme (Should, consistency decision 24).
- `$0F` stays the bracket theme.
- The venue docs accepted the enemy-area placements.
- EN is ALL CAPS.

---

## Changes in round 2

Finding ids are those of [`review_feasibility_design.md`](review_feasibility_design.md) and
[`review_consistency_scope.md`](review_consistency_scope.md); R-numbers are [`RULINGS.md`](RULINGS.md)'s.

| # | Change | Rulings and findings |
|---|---|---|
| 1 | Added **"v1.0 scope"**: what ships, the tier table (art 51.6 + music 9 = 60.6 Must sessions), the milestones, the Must-only dependency table, the not-in-v1.0 table, and 9 art-side fallbacks | R0.1-R0.4; scope-1, scope-2, scope-3 |
| 2 | **§11 rewritten for the no-artist baseline**: R / X / C / D methods, Claude's drafts final, the reuse-first rules, one size per BG boss, face icons, Break Man and Bass β from Rock's sheet, frame caps 8 / 16, placeholder first, the art-acceptance gate with a gallery; round 1's 890 human hours withdrawn | R5.1; scope-7 |
| 3 | **Every budget re-run** in a new ledger (`budget_r2.py`) against the revised venue, fortress, systems, meta and tech docs. Must went from 4,851 tiles and 421 frames to **4,535 tiles and 354 frames**. Added: Grand Pi-kun as a one-size BG boss, Big Eye, the Kamegoro Maker, the Trophy Dispenser, the rejects, the ACCEPTED stamp and BASS BLASTER, the MUSEUM third, SET-PARADE, the trophy theft's claw, 22 face icons, the HUD labels, the boss-panel glyphs. Tiered: METALL 16 and Enker Could, Doc Robot and Flip-Top Jr. Should, TS_ARCADE Could, Picopico-kun Should. fortress's technique per boss adopted; one scarf tell (orange) | R5.3; consistency-8, scope-1 |
| 4 | **The tileset-slot table regenerated from tech §5.3** (2 slots per bank, an independent alternate set per slot; 14 slots in v1.0, 26 in all). Round 1's 10-bank, 3-slot plan, its no-sharing rule and its use of `$2B:$92`/`$2D:$92` are withdrawn; the lobby is Opening screen `$1D` | R1.10; scope-11, consistency-9, feasibility-17, consistency-31 |
| 5 | **One track list** (§12.3-§12.5): Must = G00-G04, **G27 WHISTLE** (was Should), **G37 LAST MATCH** (new, 2A03 stems) and D9 (was Should); **G38 RIOT** (new, Should); FINAL LAP = G15's escape entry (Should); G16 for the podium; G14 Could with W1; G17 Could; G18-G20 Could; G21 and G36 Won't. Fortress's names mapped to G-ids | R5.2; scope-23, consistency-13, consistency decisions 24, 25 |
| 6 | **§12.9 LIGHTS OUT**: G37's stems, the drop order (MMC5 first if on, then noise, triangle, pulse 2; pulse 1 last), no DPCM, the music-driven sync, no SFX after the first tower, silence after | R4.1, R5.2; design-1, consistency-13 |
| 7 | **ExGrafix narrowed** to W1's locked rooms and the METALL 16 arena (Could); no extra 4 KB page; W2/W3/escape SUPER colour = palettes, bands and music; the castle picture's bloom Could | R1.3; feasibility-1, consistency-1 |
| 8 | **The slot set has one owner per form** (systems' map); artcheck rejects sets over 15 tiles; **set-piece player sheets** for the sortie and the pogo; vines, the balloon and the condor use ladder poses; round 1's 24-tile loop poses, 12-tile vine set and condor tiles removed | R2.3; feasibility-8, consistency-43 |
| 9 | §1.5 corrected (the menu loads sets `$02`/`$03` in bank `$00`, 119 of 128 positions differ); §2.6 uses tech's stream rates (192 / 96 / 32 B): a form swap is 11-22 frames under systems' fixed 16-f swap | R2.3; feasibility-7, consistency-5 |
| 10 | **The text model**: a 1-bpp glyph cache, **EN ALL CAPS** (the mixed-case set is dropped), JP kana; pop-up strip ≤ 24 glyphs + 4 icon tiles | R1.4; feasibility-11, consistency-3, consistency decision 4 |
| 11 | **Face icons are BG tiles inside the glyph strip**, so the first-weakness line works in full boss rooms; the icon set follows story's speakers (Light as a radio frame); Beat's portrait and Break Man's "NO" are dropped; portraits and match-card portraits are Should | R5.1; consistency-14, consistency-40, consistency decision 29 |
| 12 | **One size per BG boss**: Pi-kun 80 px; WILY MACHINE 6.5 = vanilla `$BE` retinted + a decal + the checker for `RL_FLOOR8`; Gamma head and fists (≈ 100 tiles); round 1's 340-tile, 3-size MODE-7 Machine becomes THE APPROACH (Should) with the L pose ≤ 150 tiles | R3.6, R2.11; scope-14, feasibility-16 |
| 13 | **Break Man**: the NPC composite is Must (≈ 10 frames from Rock's sheet); the playable sheet is Should; Dark Man's disguise is a 40-tile set from the NPC with the orange scarf | R4.2; scope-15, feasibility-14, consistency-8 |
| 14 | **Bass β** is composited from Rock's sheet, with his 4 copied weapons pre-drawn in his own set | R3.6, R5.1; scope-13 |
| 15 | **Names and trademarks**: venue headings use R3.3's names; no third-party names on screen; plaques describe; style notes evoke genres | R3.3; design-10 |
| 16 | **Cultural fixes (Must)**: T-MESA without graves replaces T-BOOTHILL; the cactus re-skin is Must and the totem is gone; PERSIAN PALACE has domes and a full moon, no minarets or crescent; the vizier is Wily in costume (Should); Tomahawk Man's pinch frames show a showman's bow | R3.4; design-11, design-12 |
| 17 | **Flashes**: ≤ 3 large flashes per second, REDUCED fades through tech's `pal_flash`, a flash audit of art-owned effects, artcheck check 11; round 1's "every 6 frames" rule withdrawn | R3.5; design-13 |
| 18 | **Lag and flicker recount** (§3.5) with every occupied slot: the podium found over the cap (12 slots, 8 palettes), so art recommends pairs; LIGHTS OUT and the ending's groups are staggered; artcheck check 10 | R1.8; feasibility-4, venues_b's flicker request |
| 19 | §4.10: the art and audio guarantees behind every stage's CASUAL levers (cues loop, tells at the window's start, no CASUAL-only art) | R2.9; design-7 |
| 20 | Repetition and trim cuts reflected: Yamato's sekisho, passes, kites and hanabi are Won't; Knight's sconce Won't; Centaur's tidal shaft; the escape's crumbling ladders; H4's conveyors and photo puzzle (Should); the hanabi SFX cut | R3.1, R3.2; design-5, design-25 |
| 21 | **Exhibitions Could** as single arenas with programmatic grids; E4 Won't (its 2-palette note kept); the victory lap one lap (Could) | R3.7, R3.8; scope-9, design-20, feasibility-20 |
| 22 | **Chips**: 14 v1.0 icons (was 21); the bundle's icons and PART icons Could; no CRIT! tiles; the Ice Block's 4 tiles; alt and synergy tiles Should | R2.4, R2.5; design-6, consistency-24 |
| 23 | The pipeline is tech's (M2, `bgboss.py` at M7); this doc specifies inputs and checks; provenance = the ledger's method; overlay composites; artcheck checks 8-13 | R1.13; scope-6 |
| 24 | Driver: **D6 Must** (tech), **D9 Must**, D12 DPCM and D13 PCM Won't (v1); the `$36` tail holds only SFX (21 Must SFX, 392 of 449 B) | R1.14, R5.2; feasibility-21, consistency decision 36 |
| 25 | **Bank ledger answers for tech**: CHR ≈ 9 of 14 banks in v1.0, ≈ 15.5 in the full design with the gap reserve; 2 sprite pairs; music ≈ 3.6 of 5 banks, so `$79` is spare | R1.5; feasibility-13, consistency-4 |
| 26 | The ending's art follows R4.1's order (pixelation, the catch, the arrest, the podium, one headline, the vanilla staff roll, LIGHTS OUT, silence); the roof and door Break Man art is gone; `$94` is not reprinted | R4.1; design-1, consistency-6 |
| 27 | HALFTIME RIOT's name and its crowd of rejects; SUPER has no YOU GET card; the WEAK! pop is tech's family `$FD` with art's 3-tile build | R4.3; consistency-24, consistency-28 |
| 28 | Cross-doc flags raised (§15): Eddie is new art (fortress), the rating screen draws over meta's desk, the trophy theft's claw is Must art (story), 4 speaker blips | consistency-8, consistency-40 |
| 29 | The ledger fed: `tools/plan/tight.py` (art 51.6, was a formula giving ≈ 50; music 9, was ≈ 10) and `tools/plan/tally.py` (all four tiers of art and music) | R0.1; scope-1 |
| 30 | Open questions resolved by consistency decision 36 (32 KB CHR-RAM, DPCM, deferral, the bracket theme, the enemy-area placements, MMC5 default ON); new questions for the director, tech, fortress and the user (§18) | consistency decision 36 |
| 31 | Small rulings with art: the mirror's glow palette is Shadow Rock's merge tell (FL-PALACE); plaques say BLUES and use the window frame (story's words); SUPER's sheet waits for tech's `$9B` audit | R3.9, R1.12; design-17, design-23, feasibility-14 |
