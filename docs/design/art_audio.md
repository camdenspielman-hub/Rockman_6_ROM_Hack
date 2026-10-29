# Rockman 6 GP: art and audio production plan (art_audio.md)

Owner: design-art-audio. Status: **v1, complete** (all sections written; numbers re-tallied by script).
Scratch and scripts: `build/design/design-art-audio/` (all run from the repo root with `python3 -I`).

This doc plans every pixel and every note that GP adds to vanilla Rockman 6: where the new art lives in CHR, what each
venue and stage costs in tiles and frames, which art is drawn by a human and which Claude can generate, the style rules,
the pipeline, and the whole music and SFX plan with a byte budget. It follows `docs/design/BRIEF.md` (binding); facts come
from `docs/research/{rm6,cx,r4mi}/`. Where it needs something from a parallel doc, it says so in §15.

Tags per BRIEF §8: **[engine-ok]** vanilla as-is or data only; **[new-code]**; **[new-art]**; **[new-music]**; size
**S / M / L**; tier **Must / Should / Could**. Tile counts are 8x8 tiles (16 bytes each). "Frames" are metasprite frames
(one pose of one character). Vanilla screens are written **vNN**, GP screens **NN**.

---

## 0. The plan in one page

| Question | Answer |
|---|---|
| Where does new art live? | In **14-16 new CHR source banks** (never over Capcom art, BRIEF §7.4). The **1,126 blank tiles** in the gaps of vanilla CHR banks `$00-$0A`, `$10-$1F` (measured, §1.3) stay as a reserve, and banks `$0B-$0F` are left to `tech.md` for code |
| How does it reach the screen? | Through vanilla's **CHR set** mechanism (`$37:$8000`, 4 bytes per set), extended to a **v2 set table** that can address banks above `$3F` and gives each stage **28 local set ids** (§2.1) |
| What limits a venue? | **256 BG tile ids live at once** and a **96-tile sprite "enemy area"** (`$1A00-$1FFF`) per screen. Not ROM space. The rules of §2 ration both |
| How much new art? | **6,793 tiles** (4,508 BG + 2,285 sprite) and **573 metasprite frames** in total; **Must = 4,851 tiles, 421 frames** (§13). For scale: 4MI added 5,266 new tiles, CX's screens are 70 % new |
| Who draws it? | A human pixel artist for characters, BG bosses, portraits and the logo (**1,368 BG tiles + 419 frames**, ≈ 890 hours with the cleanup of Claude's drafts); Claude drafts or generates the rest (**3,140 BG tiles + 151 frames**) (§11) |
| Music? | Vanilla's 36 tracks stay. **37 new compositions (51 track ids)**: 5 Must (3.0 KB), 24 Should, 8 Could (+2 MMC5 layers), **27.5 KB** in all; about **70 new SFX (≈ 1.9 KB)**; MMC5 "16-bit" arrangements for Super Wily Castle (Could, per BRIEF §9). Vanilla has **449 bytes** of free sound space, so new music goes into **5 new 8 KB banks** with a per-track bank byte (§12) |
| The one technical bet | **8 KB CHR-RAM is the real budget.** Every in-stage pop-up, boss pinch form and form swap is planned around it (§2). §18 asks whether `tech.md` can measure a 32 KB CHR-RAM option |

---

## 1. Facts this plan stands on (measured)

All measured from `roms/rm6j.nes` and the shared savestates; scripts in `build/design/design-art-audio/`.

### 1.1 CHR-RAM layout during play [code][seen]

RM6 has **8 KB of CHR-RAM** and writes the MMC3 CHR registers once (identity map). PPUCTRL is `$88` in stages: **BG
uses pattern table `$0000` (256 tiles), sprites use `$1000` (256 tiles), 8x8 sprites** (`rm6/levels.md` §6, confirmed in
every state sampled).

| Sprite tiles | Contents | Loaded by |
|---|---|---|
| `$00-$70` (113) | Rockman's sheet (normal form: set `$00`, bank `$00`) | stage start; form sheets `$04-$07` (bank `$01`) on a transform |
| `$71-$7F` (15) | **the equipped weapon's shot tiles** (sets `$29`, `$56-$5D`, `$79`) | weapon change |
| `$80-$9F` (32) | **common**: items, explosion, `READY` (`$99-$9D`), HUD pieces (set `$01`) | stage start |
| `$A0-$FF` (96) | **the enemy area**: per-screen enemy sets (16-96 tiles each), or one boss set | camera entering a screen (`$3A:$826F`, AI header byte AI-4) |

`resident.py` drew 73 states for 120 frames each: 111 of the player tiles and 21 of the 32 common tiles were drawn.
`$80`, `$86`, `$87`, `$8A`, `$8B`, `$8D` were never drawn (candidates for GP's resident sprites, §2.4); `$99-$9D` are the
`READY` letters, drawn only at (re)spawn.

**Sprite palettes** (`pals.py`, 6 states): palette 0 = Rockman (`0F 2C 11`, recoloured per weapon), palette 1 =
`0F 20 37` (black / white / skin: Rockman's face, items, common sprites), palettes 2-3 = **the two enemy palettes of the
screen**, written by the enemies' palette programs (`$C9EF`, which start at buffer index `$18`/`$19`). Colour 1 of
every sprite palette is black (`$0F`): the outline.

### 1.2 The CHR set table [code] (`chrsets.py`, output `chrsets.txt`)

- 256 entries of 4 bytes at `$37:$8000`: count, PPU address / 16, source offset / 16, flags (bit 7 = PPU `+$1000`,
  bits 1-6 = **8 KB source bank, so only banks `$00-$3F` are addressable**, bit 0 = source `+$1000`).
- **223 ids are used** (126 sprite sets, 97 BG sets). **33 ids look unused** (all `$00` or all `$FF`): `$7C-$7F`,
  `$DF-$FB`. Ids `$FC-$FF` are the debug sound player's font.
- BG stage sets are 256-tile bases (`$82`-`$C9`) plus "thirds" of 32-128 tiles swapped in by exits; tiny 4-8-tile sets
  animate torches, water and oil (`$9F-$A1`, `$AB-$B0`, `$D8-$DB`).
- **Boss sprite sets fill the enemy area**: Blizzard `$36` 93 tiles, Wind `$3F` 96, Plant `$45` 85, Flame `$43` 73,
  Yamato `$3E` 96, Tomahawk `$44` 94, Knight `$39` 96, Centaur `$46` 73 (`bossets.py`). Only Flame and Centaur leave
  23 tiles; Wind has 8 duplicate (flipped) tiles, the others 0-1. **New champion frames therefore cannot just be
  added** (§2.5).

### 1.3 Free tiles in vanilla CHR banks [code] (`chrfree.py`)

A tile is free if no CHR set reads it and it is blank.

| Banks | Free tiles | Notes |
|---|---|---|
| `$00`, `$03-$07`, `$09`, `$0A` (sprite art) | 830 | gaps between Capcom's sets, in runs of 16-96 (bank `$00` has one run of 96) |
| `$02`, `$08` | 62 | |
| `$17`, `$19`, `$1E`, `$1F` (BG art) | 234 | `$1E` has a run of 78, `$1F` a run of 128 |
| `$10-$16`, `$18`, `$1A-$1D` | 0 | full |
| **Total outside `$0B-$0F`** | **1,126** | 4MI's "fill the gaps" (r4mi/graphics.md §4) |
| `$0B-$0F` | 2,548 | the 40 KB that `rm6/SUMMARY.md` §3 lists as free ROM; this plan leaves it to `tech.md` |

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
are gone by then. GP's build must check this automatically (§10.5).

**BG tiles**: a venue uses 229-256 of its 256 ids over all its CHR states (`rm6/SUMMARY.md` §2), but **one screen
references far fewer**: a boss room 52-195 (Blizzard's 89, Mr. X 2's 52, Wily 1's 195), the stage select 190, the title
252 (`scenes.py`). The venue docs found runs of 50-170 unused ids per screen group (`venues_a.md` §0.7).

**Title screen**: 252 BG tiles in use: 142 logo, 90 moon, 16 menu text (`title.py`). 251 sprite tiles are free.

### 1.5 The form sheets [code] (`formdiff.py`)

The four form sheets (sets `$04-$07`, bank `$01`, 128 tiles each) share **only 10 tile positions** with the normal
sheet, and **109-114 of their tiles exist nowhere in it**. So `systems.md` SYS-CTL-4's target of "≤ 64 difference
tiles per form" cannot be met by streaming differences: **a form swap streams the whole 2 KB sheet**. At 128 B per
frame that is 16 frames; at 256 B per frame (an unrolled VBlank copy, 4MI's 1.8x) it is 8 frames. §2.6 makes the
budget.

### 1.6 Flicker baseline [seen] (`flicker.py`, 240 frames per state, Rockman running and firing)

| State | Max sprites on a line | Frames with > 8 on a line | Max OAM entries |
|---|---|---|---|
| Blizzard start, Plant cp1, Knight cp1 | 6-8 | 0 % | 18-41 |
| Flame, Knight, Centaur boss | 8 | 0 % | 38-46 |
| Blizzard boss | 9 | 56 % | 44 |
| Mr. X 1 / Mr. X 3 / Wily 2 boss | 9-10 | 5-6 % | 36-60 |
| Wily 1 boss (Mechazaurus) | 11 | 21 % | 64 |
| Wily 3 Plant Man refight | 13 | 71 % | 54 |

Vanilla RM6 is **clean in stages and flickers in a few boss rooms**. OAM order is reversed on odd frames
(`$07D9`, `rm6/engine.md` §1.5), so overflow becomes 30 Hz flicker. CX's median state drops sprites in 22 % of samples
(cx/graphics.md §9). GP's budget (§3.4) sits between the two.

### 1.7 Sound [code] (`songsizes.py`, driver facts from `rm6/engine.md` §5)

| Measure | Value |
|---|---|
| Track ids | 102 (`$34:$8A40`); `$00-$22` + `$39` music (36), `$23-$65` SFX (66) |
| Music data | **18,788 B**; stage themes `$00-$07` 617-1,238 B (mean 1,010); Mr. X / Wily stage 788 / 871; boss `$0C` 633; Wily Machine `$18` 575; jingles 116-260; ending scenes 349-546 |
| SFX data | 1,940 B, mean 29 B per effect |
| Free | **449 B** (bank `$36` tail). `$1A` is an empty stub; SFX `$3D/$3E/$4D/$51` look unused |
| Channels | pulse 1, pulse 2, triangle, noise. **No DPCM**. SFX steal music channels |
| Instruments | table at `$8B0F` (pointer at `$34:$8A41`), 8 bytes each; 71 fit before the first song (`$8D47`) |
| Command set | `$00-$18` decoded (notes ≥ `$20`: 3-bit length index + 5-bit pitch); MML-like |
| Lag | the driver runs in NMI (or the IRQ), so **music keeps tempo during lag** |

---

## 2. Asset architecture: how 512 live tiles carry a 22-stage game

### 2.1 CHR set table v2 [new-code] S · Must (built by `tech.md`)

Vanilla's 6-bit source bank cannot reach GP's new banks (`$40-$7D`). The v2 table:

- **Global ids `$00-$DE`**: vanilla's sets, unchanged, plus GP globals in the free ids `$7C-$7F` and `$DF` (5 ids: the
  GP common sprite set, the text-window font, the form-swap flash, two spares).
- **Stage-local ids `$E0-$FB`** (28 per stage): resolved through a per-stage 28-entry table that the stage-attribute
  table (BRIEF §7.2) points to. Each venue therefore has 28 ids for its new thirds, sprite sets, pinch sets and
  animation frames without growing the global table. A byte in an AI header (AI-4) or a screen exit that names `$E0+`
  means "this stage's set n".
- **Entry format v2**: 5 bytes (count, PPU / 16, source offset / 16, **source bank (8 bits)**, flags: bit 7 PPU
  `+$1000`, bit 0 source `+$1000`). The loader `$C95C` reads v2 entries for local ids and for any global id whose v1
  entry has the escape pattern; vanilla's 4-byte entries keep working.

Why not a 16-bit id: AI headers, exit bytes and checkpoint saves (`$0685`) all hold one byte. Local ids keep every
one of those formats.

### 2.2 Tileset slot plan (the 2 empty slots plus new banks) [new-code] S · Must

A **tileset slot** is 9 pages (5 metatile + 4 block pages, 2,304 B); a tileset bank holds 3 slots (`$80`, `$89`,
`$92`) plus **one alternate metatile set** (`$9B-$9F`, 1,280 B) that its 3 slots share (`rm6/levels.md` §4). The
alternate set is what breakables, toggling floors (`venues_a.md` VA-TIMED), pressure plates and Power blocks use, so
**two alternate-heavy stages must not share a bank**.

| Bank (symbolic; `tech.md` numbers it) | Slot `$80` | Slot `$89` | Slot `$92` | Alternate set used by |
|---|---|---|---|---|
| **TS-BLZ** | Blizzard (copy of `$2E:$80`, + ~70 tiles' worth of blocks) | Blizzard secret route + summit (`venues_b.md` 17-1A) | E3 Invader arena | Blizzard (ice cells) |
| **TS-WND** | Wind (copy of `$2C:$80`) | Wind hangar / wing (1C-1D) | E1 Block arena | Wind; E1 gives alternates only to metatile ids `$E0-$FF` |
| **TS-PLT** | Plant (rebuilt from `$2E:$92`) | Plant underground + caverns (18-1F) | E2 Paddle arena | Plant (tar pits, croc heads); E2 bricks use T6 per-position bits, not the alternate set |
| **TS-FLM** | Flame (copy of `$2F:$80`) | Flame palace roof + throne | Semifinal Riot | Flame (plates, oil ignite) |
| **TS-YMT** | Yamato (copy of `$2E:$89`) | Yamato secret road + kabuki stage | E4 Maze arena | Yamato (trapdoors) |
| **TS-TMH** | Tomahawk (copy of `$2C:$89`) | Tomahawk town + saloon + train | Opening Ceremony | Tomahawk (Power blocks) |
| **TS-KNT** | Knight (copy of `$2D:$80`) | Knight basement + DQ rooms | H5 (MM5 wing) | Knight (stairs, walls); H5 none |
| **TS-CTR** | Centaur (copy of `$2D:$89`) | Centaur towers + sunken throne | W2 Bracket of Doom hub | Centaur (zone doors) |
| **TS-HOF1** | H1 (MM1 wing) | H3 (MM3 wing) | W1 Upgrade Lab | H1 (yoku blocks) |
| **TS-HOF2** | H2 (MM2 wing) | H4 (MM4 wing) | W3 castle core | H2 (Heat blocks) |
| vanilla `$2B:$92` (empty) | Victory-lap credits | | | none needed (shares `$2B`'s set with vanilla Mr. X 4 / Wily 4) |
| vanilla `$2D:$92` (empty) | Players' Tunnel lobby (GP Rush) | | | none needed |

That is **10 new 8 KB banks (80 KB) for 30 slots** plus the 2 empty vanilla slots. All vanilla tileset tables stay
untouched (the 1993 preset and the dev tool can still load vanilla stages).

**Section switch** [new-code] S · Should: an exit may change the stage's metatile/block pages (`$63`/`$67`) to the
bank's second slot, in the same way an exit changes the CHR set. This doubles the block budget for the full venues
(Plant and Tomahawk use 255 and 221 block ids, `rm6/SUMMARY.md` §2). Rule: switch only on type 1-6 exits (a scroll
lock or vertical transition), never at a free-scroll seam. Without it, slot `$89` is unused and the venues keep
vanilla's 256-block limit.

### 2.3 BG tiles: thirds, not additions

Every venue doc already follows the rule this section fixes for all stages:

1. A stage's **base set** is vanilla's 256-tile set, kept.
2. New art arrives as **thirds** (`$0000-$03FF`, `$0400-$07FF`, `$0A00-$0FFF` and similar 32-128-tile ranges) that
   an exit's CHR byte swaps in over art the next screens do not show, exactly as vanilla's `$91`/`$95`/`$98` do.
3. The build tool proves each swap safe: for every screen and its scroll neighbours, the BG ids referenced must all
   be present after the swap (§10.5, the **free-id map**).
4. Animated BG tiles (wheels, rain, water, torches) are 4-8-tile local sets cycled by a thread, vanilla's torch
   technique (`$39:$888A`).

Non-venue stages (Opening, Semifinal, H, W, Exhibitions) get **new 256-tile bases** built mostly from vanilla tiles
re-sourced (4MI's "every tile set is just a list of pages", r4mi/graphics.md §8).

### 2.4 Sprites: the enemy area, the common row and the resident GP tiles

- **Enemy area** (`$A0-$FF`): each enemy type's AI header names its set (AI-4); sets are placed at fixed PPU
  addresses. **Rule**: a new enemy set is 16, 32 or 48 tiles, aligned to 16, and the build tool rejects a screen
  whose sets overlap (§10.5). Venue docs place their new enemies; §4 lists each venue's per-screen numbers.
- **Common row** (`$80-$9F`): GP replaces set `$01` with a copy (**GP-COMMON**, global id `$7C`) that keeps every
  vanilla tile and fills the 6 never-drawn slots, after a full-game OAM census confirms them (§10.6):
  - `WEAK!`: **W**, **K**, **!** only. **E** and **A** are already in `READY` (`$99-$9D`). 3 tiles.
  - `CRIT!` and `?!` (`systems.md` §5, §14): **C**, **I**, **T**, **?**. R comes from READY. 4 tiles, Could with criticals.
  - If the census finds fewer than 6 free slots, the low-fuel pip and the swap flash move to the weapon slot below.
- **Weapon slot** (`$71-$7F`, 15 tiles): each weapon's shot set. GP adds the alt-fire tiles of `systems.md` §3 here,
  per weapon (2-4 tiles each, 27 in all), and the **set-piece player poses** that only occur with one weapon:
  - the pogo pose (2 frames, Y.SPEAR's synergy) in the Y.SPEAR set;
  - the vine-hang and carry poses (Plant, Blizzard condor; the buster is the only weapon allowed while hanging, a
    venue rule) in a venue-local "buster + poses" set;
  - the Rock-on-Rush loop poses (Wind sortie, buster only) in the sortie's set.
- **Player area** (`$00-$70`): the vanilla sheet, untouched. Super Rock and Break Man are whole replacement sheets
  (§7.1).

### 2.5 Bosses: pinch sets, streamed during an invincible beat [new-code] S · Must

A champion's boss set fills the enemy area (§1.2). New frames (Plant's bloom, Blizzard's skis-off, Yamato's flying
kabuto, the weak reactions of `systems.md` §5) go into a **pinch set** of 16-24 tiles that **replaces the frames the
champion no longer needs in that phase**, streamed during an invincible animation that already exists in the design
(Plant's 30-f bloom, Knight's "ENRAGED" log line, Tomahawk's high-noon draw). At 128 B per frame a 24-tile pinch set
streams in 3 frames. **Each champion's GP boss set is rebuilt** (copy of the vanilla set, dropped frames removed,
projectiles first) so that phase 1 fits in 96 tiles and phase 2 = phase 1 − dropped + pinch set.

### 2.6 The VBlank streaming budget (for `tech.md`)

| Stream | Bytes | Frames at 128 B/f | Frames at 256 B/f | When |
|---|---|---|---|---|
| Form swap (whole sheet, §1.5) | 2,048 | 16 | 8 | SELECT form swap; the swap flash covers it |
| Super Rock / Break Man sheet | 2,048 | 16 | 8 | adaptor change / tag call (beam-in hides it) |
| Champion pinch set | 256-384 | 2-3 | 1-2 | the invincible pinch beat |
| BG boss pose (CX streaming, §6) | up to 2,560 | 20 | 10 | between poses; double-buffered halves |
| Pop-up glyphs (§9.6) | ≤ 384 (24 tiles) | 3 | 2 | before the window opens |
| Face icon | 64 | 1 | 1 | with the pop-up |

**Recommendation to `tech.md`**: an unrolled 256 B/frame copy path for CHR streams (4MI's Rock5easily VBlank transfer,
r4mi/engine.md §8), and one stream at a time, queued.

### 2.7 MMC5 extended attributes (ExGrafix) [new-code] M · Could, spike first

PLAN's W1 wanted per-tile palettes. MMC5 ExRAM mode 1 lets each 8x8 BG tile pick its own palette (and a 4 KB CHR
page). With 8 KB of CHR-RAM the page bits only reach the two pattern tables, but the **per-tile palette works**: the
same 4 BG palettes, chosen per 8x8 tile instead of per 16x16 block, which is what makes art look "16-bit". Cost: the painter (`$D1FF`/`$D322`) must also write ExRAM; emulator support
for MMC5 + CHR-RAM must be checked on FCEUmm and Mesen first. **Use it only in W1's "16-bit" tier**, where the effect is
the point. If the spike fails, W1's 16-bit tier is a palette upgrade plus the MMC5 music (§12.5), which already sells
the joke.

### 2.8 Pattern-table split (BG from `$1000` below a line) [new-code] S · Should

A mid-frame PPUCTRL write (bit 4) makes the BG rows below a scanline read **the sprite pattern table**. On menu screens
the sprite table is 80-100 % free (`rm6/text.md` §7), so:

- the **title** keeps the vanilla logo and moon (232 tiles) in `$0000` and draws its menu (GAME START / SPECIAL EVENTS
  / CONFIG / ©) from a font in `$1000`, below line 112 (§9.1); the moon's rows below the split are duplicated into
  `$1000` too (≈ 60 tiles; the title's sprite table has 251 free);
- the **bracket**, **judges' desk** and **pit stop** get a second 256-tile page for their lower panels;
- one entry in the generic raster list (BRIEF §7.1); never used in stages, where the sprite table is busy.

---

## 3. Style guide

### 3.1 The house style

- **RM6's Capcom house style, always**: thick black outlines (sprite colour 1 is `$0F`), 3-colour sprites with one light
  highlight, 16x16 metatiles, chunky readable silhouettes. A new enemy should be impossible to tell from Capcom's at a
  glance (4MI's standard, r4mi/graphics.md §8).
- **Homage by rules and silhouette, never by logo** (BRIEF §6): the venues *quote the look* of their games at Rockman's
  scale (CX's SMB stage, cx/graphics.md §7). Parody names only; no trademark logos, no title-screen lettering of other
  games.
- **One exception per venue may break the house style on purpose**, as a joke the art carries (CX lesson 6): Plant's
  2600 canopy (fat pixels, 2 colours), the Game Boy tier of W1 (4 greens), the 8-bit-on-8-bit Exhibition arenas.

### 3.2 Palettes

| Rule | Detail |
|---|---|
| Sprite palette 0 | Rockman, recoloured per weapon (vanilla). Super Rock, Break Man, Bass β each get their own palette 0 when played |
| Sprite palette 1 | `0F 20 37` (black / white / skin) is **shared**: Rockman's face, items, GP-COMMON, every face icon. Never change it per stage |
| Sprite palettes 2-3 | **The screen's two enemy palettes.** Every new enemy is drawn to use **one** of them plus palette 1. Two enemy types on a screen may not need two different palette-2 programs: the build checks this exactly like CHR overlap (§10.5) |
| Boss | A boss owns palettes 2 and 3 (vanilla). A weak flash is 2 frames of white (`systems.md` §5) |
| BG | 4 palettes, colour 0 shared (`$0F` in nearly every vanilla stage). Venue identity comes from palette first: re-use vanilla tiles under a new palette before drawing new ones (4MI's dusk city) |
| Palette tricks to use | dusk/night variants of vanilla sets (Tomahawk's sunset program already cycles), the Game Boy tier (`$0F $0A $1A $2A` greens), C.FLASH's "lights a dark room" fade, a Shadow Rock as Rockman in a dark palette (Flame), Dark Man disguised as Break Man (palette swap), Mr. Y as Mr. X with a moustache (§7.3) |
| Accessibility | REDUCED FLASHES (BRIEF §5.7) replaces every full-screen white flash with a 2-step darken; a flash never exceeds 3 frames on, and never repeats faster than every 6 frames |

### 3.3 Sizes

| Kind | Size | Hardware sprites | Example |
|---|---|---|---|
| Small enemy | 16x16 | 4 | Metslime, Toppy, scorpion |
| Standard enemy | 16x24 to 24x24 | 6-9 | guard-bot, outlaw |
| Large enemy | 32x32 max | ≤ 16 | Sidewinder on his horse, condor |
| Robot Master scale (champions, Bass β, guests, Dark Man) | 24x24 to 32x32 | 9-14 | as vanilla |
| Anything bigger | **BG art** + sprite parts | parts ≤ 12 | AYACO (Should), all H bosses but Dark Man, the MODE-7 Machine |
| Portrait (menus, cutscenes) | 32x32 BG | 16 tiles | commentators, judges |
| Face icon (in-stage pop-up) | 16x16 sprite | 4 tiles | Cossack, Kalinka, Mr. Y |
| Chip / PART icon | 16x16 sprite | 4 tiles | 21 chips, 8 PARTs |

**Widths matter more than heights**: the limit is 8 sprites per scanline. A 32-px-wide enemy uses 4 of them.

### 3.4 Flicker budget

| Context | Max sprites on any line | Frames with a line over 8 | How |
|---|---|---|---|
| Venue stages | **≤ 8 on 95 % of frames** | ≤ 5 % | at most two 32-px-wide objects side by side; repeated hazards are BG tiles, not sprites (CX lesson 5); bullets 8 px wide |
| Set pieces (sortie, train, gallery) | ≤ 10 | ≤ 15 % | wave directors space enemies vertically by data; the build's flicker simulator (§10.5) runs each wave |
| Boss fights | ≤ 10 | ≤ 25 % | vanilla peaks at 9-11; HUD bars cost 2 per line |
| Menus and cutscenes | ≤ 8 | 0 % | |

The **~10 live objects** lag budget (BRIEF §6) is separate and usually binds first.

### 3.5 Text and UI look

- Menus keep vanilla's blue frame tiles and caps font; GP adds only the letters each screen lacks (4MI's title rule).
- Dialogue window: black, white 1-px frame (the DQ window `venues_a.md` §2.1 asks for is the same frame), 2 lines in
  play, 4 in scenes. EN uses mixed case from a GP font set in the kana slots (`rm6/text.md` §7, option 1).
- Status labels as 4-tile condensed words (4MI's curse labels): `ACE 100%`, `DRAW!`, `FOUL!`, `LEVEL UP`, `WEAK!`.
- Numbers on the scorecard and bolts use vanilla's digit tiles.


---

## 4. Per-venue art budget

The venue docs (`venues_a.md` §1.1/2.1/3.1/4.1, `venues_b.md` §1.6/2.6/3.7/4.10) own *what* each venue shows; this
section turns their lists into a budget the build can enforce: **kept vanilla CHR**, **new BG thirds** (tiles, ids,
screens), **sprite sets with their enemy-area placement** (so no two sets that share a screen overlap), frames, the
champion's pinch set, and the conflicts to respect. Tile counts for the venue-A sprites are this doc's estimates from
their lists; venue-B counts are theirs.

**Enemy-area notation**: `A0+32` = a set of 32 tiles at sprite tiles `$A0-$BF`. Vanilla enemy sets keep their vanilla
addresses (looked up with `enemysets.py`, quoted as tile ranges). A venue's new sets are stage-local ids `$E0+` (§2.1).
"Conflicts with" = the vanilla sets whose tiles overlap: **those enemies may not share a screen** with the new set.

Common to all eight [new-art] [new-code] S · Must: a **tileset slot** (§2.2), a **rebuilt champion boss set** plus a
**pinch set** (§2.5), and the venue's **PART icon** (GP UI set, §9.7).

**What stays: vanilla blocks, metatiles and tiles** (`rm6/SUMMARY.md` §2). Each venue's slot starts as a byte copy of
its vanilla tables, so every vanilla block and metatile stays available. New blocks go into **reclaimed ids**: the
ids the GP layout no longer uses (`levels.py` lists the ids a layout references; the rebuild drops the rest), and,
with the section switch (§2.2), into the second slot's fresh 256.

| Venue | Vanilla blocks used / 256 | Metatiles used / 256 | BG tile ids free (all CHR states) | Plan |
|---|---|---|---|---|
| Blizzard | 255 | 245 | 3 | reclaim from the cut screens; summit and secret route in slot `$89` |
| Wind | 232 | 194 | 8 | 24 free blocks + reclaimed; hangar in slot `$89` |
| Plant | 255 | 197 | 0 | rebuild from the GP layout (the second gorilla room and half the lodge go); underground and caverns in slot `$89` |
| Flame | 254 | 178 | 27 | reclaim; palace in slot `$89` |
| Yamato | 255 | 221 | 4 | reclaim; kabuki and secret road in slot `$89` |
| Tomahawk | 221 | 212 | 1 | 35 free blocks; town, saloon and train in slot `$89` |
| Knight | 255 | 155 | 6 | reclaim (only 155 metatiles used: room for 100 new ones); DQ rooms in slot `$89` |
| Centaur | 250 | 176 | 11 | reclaim; towers and sunken throne in slot `$89` |

### 4.1 Blizzard Man: SUMMIT CLIMBER (stage 0)

Vanilla sets on the climb: snow robot `$4D` (`C0-EF`), count bombs `$19/$21` (`A0-BD`), drone `$24` (`F0-FE`), walker
`$1E` (`C0-DA`); ship riders `$1F/$20` (`C0-DF`); jester head `$10` (`A0-FF`, all 96).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$82` (ice, ledges, girders, skyline), `$85` (ship), `$84` (cave) | | all | [engine-ok] |
| **BZ-CLIMB** third: Ice Climber floor cells (intact / cracked / gone), rock floor, grassy ends, clouds, signs | ~40 | | climb, at `$0A00` (the climb hides the far skyline) | [new-art] M Must |
| **BZ-SUMMIT** third: summit peak and flag, lodge (logs, window, sun deck), ski fence and moguls, MR. Y MARU banner, the giant eggplant statue | ~30 | | 0F-1A | [new-art] S Must |
| **SET-BZ1** `A0+32`: Toppy (walk 2, push, stun, bow, sad), ice cube, icicle (hang, shake, fall) | 32 | 10 | climb, ship | [new-art] M Must. Conflicts with count bombs, jester. Fits beside the snow robot, drone and ship riders |
| **SET-BZ2** `A0+32`: Nitpicky (fly 2, dive), 4 vegetables, rolling snowball (2) | 32 | 9 | climb, ski run | [new-art] M Must. Never with SET-BZ1 (same slot) |
| **SET-BZ3** `C0+48`: condor 32x24 (2), floe/cloud 48x8, snowman, Toppy foreman (2) | 48 | 6 | summit, 11, 17 | [new-art] M Must. Conflicts with snow robot, walker, riders: none of them on the summit |
| Champion pinch set: skis-off, slush puddle, "skis slip" weak reaction | 16 | 4 | boss 16 | [new-art] S Must |
| Shirokuma 32x32 (`C0+32`) | 12 | 3 | HARD only | [new-art] S Could |
| PART icon SNOW | 4 | | | §9.7 |

The ship screens use SET-BZ1 (icicles) at `A0-BF` beside the riders at `C0-DF`: no conflict. Palette: Toppy and
Nitpicky share the climb's enemy palette 2 (white / light blue) with the snow robot; vegetables use palette 1.

### 4.2 Wind Man: SKY ACE 1943 (stage 1)

Vanilla sets: panda drums `$27/$28` (`D0-EF`), crawler `$29` (`C0-DF`), bomber `$1B` (`E0-EF`), tops `$36`
(`F0-FC`), stomper `$2D` and beetle `$75` (`D0-D8`), shield-car `$34` (`B0-BF`), big robot `$59` (`C0-F6`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$83` sky, clouds, coral girders, pillars, tower, fans; `$8C`, `$8D`, `$8E` | | 03-15 | [engine-ok] |
| **W-CARRIER** third (ids `$54-$B3`) | 96 | | 00, 02 | [new-art] M Must |
| **W-SEA** band (ids `$76-$B5`): 512-px sea loop, islands, destroyer silhouette | 64 | | 01 | [new-art] S Must (programmatic) |
| **W-HANGAR** third | 96 | | 18-1D | [new-art] M Should |
| AYACO as BG art in the sky band | 110 | | 01, its phase only | [new-art] L Should |
| **SET-WS1** `A0+32`: propeller Met fighter (bank L / level / bank R; green and red by palette), gold leader (2), bullets | 32 | 7 | 01 | [new-art] M Must |
| **SET-WS2** `C0+16`: POW / 3-WAY / AUTO / YASHICHI icons, LOOP "R", lamp | 16 | 6 | 01, 02 | [new-art] S Must |
| **SET-WS3** `D0+48`: AYACO sprite build 48x24, 4 engine parts (2 frames each), damage | 32 (+16 spare) | 8 | 01 | [new-art] M Must |
| **SET-WS4** `A0+16`: Kite Met (2), seagull (2) | 16 | 4 | 09-0A | [new-art] S Should. Fits beside the shield-car (`B0-BF`) |
| **SET-WS5** `C0+16`: windsock (3), deck crew Met (flags, wrench), bomb cart (2) | 16 | 8 | 00, 02, 06-08, 19-1A | [new-art] S Must. Conflicts with the crawler and big robot (03-05, 0E-10 only) |
| Weapon-slot poses: Rock on Rush, the loop (4 frames) | 24 | 4 | 01 | [new-art] S Must |
| Champion pinch set: SKY ACE goggles and scarf, gust pose | 16 | 4 | 15, 1D | [new-art] S Must |

The sortie (01) carries SET-WS1 + WS2 + WS3 = 96 tiles, so **no vanilla Wind enemy appears on 01** and explosions use
the common row. **Flicker hot spot**: the wave director must keep ≤ 3 fighters in any 8-px band (§3.4).

### 4.3 Plant Man: JUNGLE PITFALL (stage 2)

Vanilla sets kept: gorilla tank `$50` (`B0-FF`, 80 tiles) and its parts, eye cannon, springs `$57/$5A` (`F0-FF`),
`$60` (`C0-DF`), `$61` (`A0-BF`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$90` base; `$91`/`$92` dark-room swap; `$BB`/`$93` flower swamp; palettes `$32-$35` | | 03-08, 0F-17 | [engine-ok] |
| **P-PITFALL** third (`$0A00-$0FFF`): a 2600-style canopy (~40 tiles, fat pixels, 2 greens: the homage is why it can be smaller than vanilla's 96-tile foliage) + vine knots, tar surface (+ "closed" tiles), croc water, ladder-hole rim, parrot ledge, rope ladder | 96 | | 00-02, 09-0E, 1F | [new-art] M Must (canopy programmatic) |
| **P-UNDER** third: brick tunnel, breakable-look wall, ladders, scorpion nests | 96 | | 18-1A | [new-art] M Must |
| **P-CAVERN** third: cave walls, underground river, waterfall, Lost City gate and garden | 96 | | 1B-1E | [new-art] M Must |
| P-RAIN (8 tiles x 4 frames, torch technique) | 32 | | 0B-0E | [new-art] S Could |
| **SET-PL1** `A0+48`: vine (11 angle tiles; one object of 5 segments), croc head 32x16 (closed, opening, open), log (2), tar bubbles (2) | 48 | 18 | jungle | [new-art] M Must. Conflicts with `$61`, `$60` |
| **SET-PL2** `D0+32`: 4 treasures, parrot (2) | 32 | 6 | jungle | [new-art] S Must. Conflicts with `$60` (keep it in the swamp) |
| **SET-PL3** `A0+48`: scorpion (3), robot cat (3), bat (2), eel (2), balloon (2) | 48 | 12 | 18-1E | [new-art] M Must |
| Weapon-slot poses: vine hang (2), swing (2), in a "buster + vine" set | 12 | 4 | jungle | [new-art] S Must |
| Champion pinch set: the bloom form (the 30-f invincible bloom covers the stream), vine lash | 24 | 5 | 17, 1E | [new-art] S Must |
| CONGA's logs | 4 | | 08 | a 4-tile copy of the log inside CONGA's set (its 80-tile set leaves `A0-AF`) |

Plant has **0 free BG tile ids** (`rm6/SUMMARY.md` §2): every new BG tile enters through a third, as `venues_a.md` §4.1's
CHR-state table plans. Vanilla's worst lag (09-0D, 21 %) becomes vine screens with ≤ 6 objects.

### 4.4 Flame Man: PRINCE OF PERSIA PALACE (stage 3)

Vanilla sets: Metall `$18` (`C0-EA`), Fire Telly `$2C` (`EC-FF`) and its drop `$30` (`A0-AF`), dome turret `$2B`
(`C0-E7`), wheel cannons `$C0/$C9` (`D0-EF`), juggler `$2A` (`E0-FF`), mine `$73` (`D0-D8`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$86` oil field, `$87` fire vault; oil palette cycle and ignite alternates (`$E6-$E9`) | | oil screens | [engine-ok] |
| **FL-DUNGEON** third: stone, torches, columns, arches, carpets, pressure plates (raised / pressed via the alternate set), loose-tile socket, chomper slots | ~50 | | 04-0E | [new-art] M Must |
| **FL-PALACE** third: mirror 32x48, hourglass mural, mousehole, throne room, domes, minarets, moon, balcony | ~40 | | 0F-1A | [new-art] M Must |
| **SET-FL1** `B0+48`: guard-bot (stand, advance, raise, slash, block), skeleton (walk 2, collapse, bones) | 48 | 9 | dungeon | [new-art] M Must (skeleton Should). Fits beside the Fire Telly and its drop (the vanilla igniter); conflicts with Metall, dome, wheel cannon |
| **SET-FL2** `E0+16`: loose tile (2), chomper (2), spike trap (3) | 16 | 7 | dungeon | [new-art] S Must. Conflicts with the Telly and juggler: trap rooms have no Telly |
| **SET-FL3** `A0+48`: portcullis 16x48, chandelier 16x24 (2), mouse-bot (2), fire marshal, vizier | 48 | 8 | palace, 1C | [new-art] M Must |
| Shadow Rock | 0 | | 0D-0E, 1A | **reuse**: Rockman's frames in a dark palette (4MI's Snatchman trick) |
| Champion pinch set: the flaming scimitar, "head flame gutters" weak reaction | 12 | 3 | 16 | [new-art] S Must |

Peak screen 0B (3 guards, 3 chandeliers) needs SET-FL1 + SET-FL3, which overlap at `B0-CF`: **0B uses the chandelier
copy inside SET-FL1's last 16 tiles** (guards then lose the skeleton frames, which 0B does not use). This is the kind
of fix the build's conflict check (§10.5) must force early.

### 4.5 Yamato Man: EDO NINJA ROW (stage 4)

Vanilla sets: lantern robot `$C2` (`C0-DF`), samurai `$A2` (`A0-FF`, all 96), shuriken robot `$69` (`D0-FF`), eye
cannon `$54` (`A0-AF`), springs `$5F` (`B0-BF`); GAMARN & GAMADAYU `$61` (`A0-EF`, 80).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$97` (Fuji vista, castle walls, shoji), `$98` interiors, `$99` dark bypass, plate-route sunset `$9A-$9C` | | | [engine-ok] |
| **YM-EDO** third: shopfronts with noren, kawara roofs, notice board and WANTED poster, tatami, 3 hanging scrolls (2-frame flutter), sekisho gate | ~60 | | 00-0B, 1B | [new-art] M Must |
| **YM-CASTLE** third: gold nightingale boards, caltrop floor, gold crest, kabuki curtain, audience, flats, treasure vault, shachihoko | ~40 | | 0C-1E | [new-art] M Must |
| **SET-YM1** `A0+32`: Jaja-nin (hop, throw, stunned), runner + pass (3), shuriken | 32 | 8 | town | [new-art] M Must. Fits beside the lantern robot and the shuriken robot |
| **SET-YM2** `A0+48`: ashigaru (3), kite (2) and kite ninja (2), bells (2), sekisho guard (2) | 48 | 11 | town edge, roofs | [new-art] M Must (kites Should) |
| **SET-YM3** `A0+64` + `E0+32`: the Daruma (5 coloured blocks, head with 0/1/2 eyes, angry head, fortune slip), pogo rack, kuroko (2), hanabi (3) | 96 | 13 | 11, 1B-1D | [new-art] M Should |
| Weapon-slot poses: pogo (2), in the Y.SPEAR set | 8 | 2 | 12-13 | [new-art] S Must |
| Champion pinch set: flying kabuto, topknot frames | 16 | 4 | 16 | [new-art] S Must |

The samurai `$A2` takes all 96 tiles: it keeps its vanilla screens and gets nothing new beside it. The Gamadayu room
keeps `$61` alone; its firework (hanabi) is a 4-tile copy inside a rebuilt `$61` (`F0-FF` is free in it).

### 4.6 Tomahawk Man: GUN.SMOKE FRONTIER (stage 5)

Vanilla sets: cowboy gunner `$6C` (`A0-CF`), totem `$12` (`A0-BF`), dome dispenser `$4F` (`C0-EA`), `$67` (`A0-CF`),
lift `$A0` (`D9-DE`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$94` desert + parallax mesas, `$96` cave, `$95` sunset sky and sun disc, `$D7` boss corridor | | | [engine-ok] |
| **T-TOWN** third (ids `$BD-$FF`): false fronts, gallery windows and doors (open / closed via the alternate set), boardwalk, water tower, outhouse, WANTED board, store signs | 64 | | 0A-0C | [new-art] M Must |
| **T-SALOON** third (`$A0-$FF`): bar, bottles, mirror, piano, swinging doors, skylight | 96 | | 0D | [new-art] M Must |
| **T-TRAIN** set (fresh ids): car roofs, couplings, platform, rails and ties (512-px band), wheels (4-frame CHR animation) | 80 | | 0E-11 | [new-art] M Must |
| **T-BOOTHILL** third (`$BE-$FF`): high-noon mesa, grave markers | 48 | | 17 | [new-art] S Should |
| **SET-TM1** `A0+64`: outlaw (pop up, aim, shoot, hit), townsfolk (lady with parasol 2, pianist 2, Eddie at a window 2), tumbleweed (2) | 64 | 12 | gallery 0B-0C | [new-art] M Must |
| **SET-TM2** `E0+32`: "DRAW!" / "FOUL!" (4-tile words), bounty stamp, hat glint, bullet hole | 32 | 6 | 0B-0D, 17 | [new-art] S Must |
| **SET-TM3** `A0+64`: Six-Shot Sam (stand, draw, shoot, fall), Sheriff (2), conductor (2) | 64 | 8 | 0D-0F, 12 | [new-art] M Must |
| **SET-TM4** `A0+64`: Sidewinder on his robot horse 32x32 (4-frame gallop + shoot), tunnel mouth 32x48, dust devil (2) | 64 | 8 | 10-11 | [new-art] M Must |
| Champion pinch set: SHOWDOWN (hat over the eyes), the draw | 16 | 4 | 17 | [new-art] S Must |

The cowboy gunners `$6C` (the featured family, `A0-CF`) conflict with SET-TM1/3/4: they stay in the desert and mine
(01-09) and on the train only as a local copy inside SET-TM4. Vanilla's conflict screens 04 and 15 (the `$61` preload,
§1.4) disappear in the GP layout; the build re-checks. The train is the flicker hot spot (Sidewinder 32 px wide + 2
outlaws).

### 4.7 Knight Man: DRAGON QUESTLIKE (stage 6)

Vanilla sets: lance knight `$6E` (`A0-BF`), `$3D` (`F0-FF`), `$65` (`A0-BF`), spearman `$70` (`A0-B9`), `$C6`
(`A0-BF`), `$3A` (`D0-D8`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$9E` castle (green stone, halls, chains, machine hall), torch animation `$9F-$A1`, revisit palettes (bank `$28`) | | all | [engine-ok] |
| **K-DQ** third (ids `$B5-$E4`): two thrones 32x32, stone tablet, inn bed, cracked floor and trapdoor, hidden-stairs metatiles | 48 | | 01, 0A-0D, 15 | [new-art] S Must |
| Window frame (white on black) | 0 | | | comes with the text engine's font set (§9.6) |
| **SET-KN1** `C0+48`: King (2), Sage (2), Innkeeper (2), Princess Roll in a gown (2), chest closed/open (2), MAGIC KEY, Roll's Love heart | 48 | 12 | 00-0B | [new-art] M Must (Princess, Innkeeper Should) |
| **SET-KN2** `C0+48`: Metslime (bounce 3), Metal Metslime (palette swap + 2-tile shine), Killer Chest (3), ceiling winch (2), sconce flame (3) | 48 | 13 | 03-06, 0C-14, 18 | [new-art] M Must |
| Champion pinch set: ENRAGED (red eyes, mace raised), "drops his guard" weak reaction | 12 | 3 | 17, 1A | [new-art] S Must |

Every vanilla Knight enemy lives in `A0-BF`, `D0-D8` or `F0-FF`, so `C0+48` is free of conflicts except with `$3A`
(`D0-D8`), which stays out of encounter rooms. Encounters (0C, 13) put SET-KN2's slimes beside the vanilla lance
knights with no change. Metal Metslime costs 2 tiles: Metslime under a grey palette.

### 4.8 Centaur Man: ATLANTIS RUINS (stage 7)

Vanilla sets: pelicans `$A9` (`FA-FF`) and `$AB` (`D0-F9`), piranha `$C1` and seahorse `$C4` (`A0-AF`), waterfall
enemy `$A5` (`D0-FF`), dome turret `$2B` (`C0-E7`).

| Item | Tiles | Frames | Where | Tags |
|---|---|---|---|---|
| Kept | `$AA` (ruins, water, waterfalls, orange castle), water animation (`$DC-$DF`, `$E8-$EF`) | | all | [engine-ok] |
| **CT-ZONE** third: zone doors (honest / lying / fake), plaques, the sky temple, hot spring with steam, the sunken throne | ~80 | | 06-1C | [new-art] M Must |
| **SET-CT1** `B0+32`: zone digits 0-9 (shared with the ZONE card), cloud platform, eggplant | 32 | 4 | 06-18 | [new-art] S Must. Fits beside the piranha, seahorse and pelicans; conflicts with the dome turret `$2B` |
| **SET-CT2** `A0+48`: Centurion statue and freed Centurion (2), Nasubi Mage (float 2, cast) | 48 | 5 | 0E-18 | [new-art] M Should. Conflicts with piranha / seahorse |
| **SET-CT3** `D0+48`: Grim Reap-bot (patrol 2, look, alarm), Reaplets (2) | 48 | 6 | 11-14 | [new-art] M Should. Conflicts with pelicans, waterfall enemy |
| Eggplant-Rock (player sheet patch: walk, jump) | 12 | 4 | curse | [new-art] S Could |
| Champion pinch set: tide-call pose, weak reaction | 12 | 3 | 17 | [new-art] S Must |

The Reaplet alarm (screen 12, 8 objects) is the venue's peak.

### 4.9 Venue totals (from the ledger, `budget.py`)

| Venue | New BG tiles | New sprite tiles | Frames | Heaviest sprite screen |
|---|---|---|---|---|
| Blizzard | 70 | 126 (+12 Could) | 41 | ship + icicles |
| Wind | 160 (+206 Should) | 142 | 40 | 01, the sortie (96 / 96) |
| Plant | 288 (+32 Could) | 124 | 41 | jungle (80 / 96) |
| Flame | 90 | 112 | 35 | 0B |
| Yamato | 100 | 128 | 38 | 1B-1D, the Daruma (96 / 96) |
| Tomahawk | 240 (+48 Should) | 146 | 42 | 10-11, the train |
| Knight | 48 | 74 (+18 Should) | 29 | encounters |
| Centaur | 80 | 102 (+12 Could) | 33 | 12, the alarm |
| **Total** | **1,076 Must; 1,362 with Should and Could** | **954 Must; 996 with Should and Could** | **299** | |

Cheap reuse already counted at zero: Shadow Rock, Metal Metslime, CONGA, Gamadayu, the vanilla desert parallax, the
ship, the tide, the spike ceiling and every vanilla enemy the venues keep (71 % of CX's reused sprites are recoloured,
cx/graphics.md §6: do the same).

---

## 5. Non-venue stages: art budget

`fortress.md` owns these stages' layouts; this is their art. Each gets a new 256-tile base built mostly from re-sourced
vanilla pages (4MI: "every tile set is just a list of pages"), plus the new tiles counted here.

| Stage | Look (one line) | Vanilla art reused | New BG | New sprites (frames) | Tier |
|---|---|---|---|---|---|
| **Opening Ceremony** | The GP stadium on opening day: stands with a crowd band (2-frame CHR animation, the torch technique), a giant scoreboard, a running track, the Players' Tunnel, flags of the 8 champions | the title's moon as the night sky (palette), vanilla girder and pipe tiles for the stand structure | 150 | Grand Pi-kun 70 (14); confetti, flags, camera drone, ref-bot 30 (10, Should) | Must |
| **Semifinal Riot** | The bracket stage wrecked by Bass: cracked jumbotron, torn banners, broken bracket boards, sparking cables | Mr. X 4 machinery (`$C3`), the Opening's stadium pages | 96 | Bass β boss set 90 (22) | Must |
| **E1-E4 Exhibitions** | Single-arena guest matches (§8) | vanilla HUD, stars | 92 | 190 (52) | Should |
| **H1** ROCKMAN | MM1 tribute: Guts lift rails, Elec beams, appearing (yoku) blocks drawn in RM6 style | Wily 1 / Mr. X tiles re-paletted to MM1's blue-grey | 96 | YD parts 14 (6) | Must |
| **H2** ROCKMAN 2 | Heat Man vanishing blocks, the dragon-chase sky | vanilla sky and cloud pages from Wind (`$8D`) | 96 | dragon parts 12 (4) | Should |
| **H3** ROCKMAN 3 | Gemini mirror rooms (BG mirrored by data, sprites mirrored by palette), needle presses | Wily 3 machine pages | 96 | Gamma parts 34 (6) | Must |
| **H4** ROCKMAN 4 | Cossack's snow citadel | Blizzard's ice and skyline pages under a dusk palette | 96 | claw and prizes 36 (6) | Should |
| **H5** ROCKMAN 5 | the "Proto" castle with gravity flips (the room flips by nametable rewrite, not by tile art) | Knight's castle pages, re-paletted | 96 | Dark Man 60 (12) | Must |
| **W1** Upgrade Lab | Game Boy tier = palette (`$0F $0A $1A $2A` greens) over the NES tier's tiles; NES tier; 16-bit tier = richer palette, ExGrafix if the spike works (§2.7) | Wily 2/3 lab pages | 96 | none | Should |
| **W2** Bracket of Doom | Teleporter hall laid out as a bracket (vanilla Wily 3 hub data) | Wily 3 hub pages (`$A2`, `$A8`, `$A9`) | 64 | (Bass β set reused) | Must |
| **W3** MODE-7 Machine | Castle core and the pseudo-3D floor band | Wily 4 pages (`$BA`, `$BC`) | 96 | machine parts 30 (8); 16-bit Capsule 60 (8, Could) | Must |
| **Victory lap credits** | A silhouette stadium-and-castle walk, names written into the scenery (CX's playable staff roll) | the Opening's pages in a silhouette palette | 80 | none (the cast walks in using existing sprites) | Should |
| **Players' Tunnel** (GP Rush lobby) | One screen from the Opening set | Opening pages | 24 | none | Should |

The **H-wing look rule** [new-art] (Must, cheap): each wing re-creates its game's *signature hazard* in RM6's tile
style, then sells the era with **palette**: H1 in MM1's flat blue-grey, H2 in MM2's night sky, H3 in MM3's teal, H4 in
MM4's dusk snow, H5 in MM5's purple. **No tiles are ripped from RM1-5 ROMs** (BRIEF §7.4); they are redrawn from scratch
or rebuilt from RM6's own pages.

---

## 6. BG bosses (Hall of Fame and finale)

All big bosses are nametable art plus a few sprite parts, the technique RM6 already has (`rm6/SUMMARY.md` §2: "the boss
is drawn in a scrolled nametable, an IRQ split shows an unscrolled floor strip from NT0, and invisible hit-box objects
follow the scroll") and that both CX and 4MI rely on. Each row names the vanilla precedent it copies (the re-skin fits
of `rm6/SUMMARY.md` §4, Section 3).

| Boss | Precedent (vanilla code it reuses) | Size | BG tiles | Sprite parts (tiles, frames) | Movement | Hit box | Tags |
|---|---|---|---|---|---|---|---|
| **Yellow Devil MK-VI** (H1) | X Crusher (Mr. X 4: NT0, multi-split chain `$16`) for the flying body; Wily Machine floor split (chain `$19`) | 64x80 (8x10 cells) | 60 | eye 16x16 (open, closed, hit: 8, 3); flying block 16x16 (4, 1); splat (2, 2) | **Flies across** as one body (scroll), then **disassembles** block by block: each departing block clears 2x2 nametable cells and spawns a block sprite that flies to the other side, where cells are written back | eye only (an invisible object pinned to the scroll) | [new-art] M Must |
| **Mecha Dragon MK-VI** (H2) | Wily Machine (NT1 + floor split, chain `$19`) | 96x80 (12x10) | 150 (head open / closed mouths by a 12-tile stream) | fireball 16x16 (8, 2); 3 platforms 16x8 (4, 1) | Bobs and advances while the floor of sprite platforms scrolls under you (the MM2 chase, T1-lite) | head | [new-art] L Should |
| **Gamma MK-VI** (H3) | Mechazaurus (Wily 1: static BG + head hit box `$E1`) | 128x160 (16x20), scrolls vertically into view | 200 | fists 24x24 (18, 2 each); phase-2 head 32x32 (16, 2) | Phase 1 static, fists punch (sprites); phase 2 the head detaches (sprite) and needs a Power / Super uppercut, as MM3's Gamma needed Top Spin | head, chin | [new-art] L Must |
| **Cossack Catcher MK-VI** (H4) | Metonger Z (Mr. X 3: BG tank + sprite pilot, chain `$1A`) | gantry 256x48 BG across the top; claw 32x24 sprite | 120 | claw (24, 3: open, closing, holding); prize capsules (12, 3 kinds) | The crane slides on its gantry (BG scroll in the top band only), the claw drops to grab: grabbing Rockman = carry to the prize chute (damage); grabbing a capsule = it drops a "prize" (a Met, a bomb or an E-can) | claw | [new-art] M Should |
| **Dark Man MK-VI** (H5) | Robot Master framework (`$93` intro, then the boss type) | 24x32 sprite | 0 | disguise: 40 tiles **copied from Break Man's sheet** with the scarf one shade off (the tell); true form 60 tiles, streamed at the unmasking (12 frames total) | sprite boss | body | [new-art] M Must |
| **MODE-7 Machine** (W3) | Wily Machine 6 (NT1 + floor split chain `$19`) + **CX's giant Dr. Light CHR streaming** (cx/graphics.md §5) | far 48x32, mid 96x64, near 192x96 | 340 over 3 sizes (24 / 96 / 220) | cannons (8, 2), Wily in the cockpit (8, 2), shots and sparks (14, 4) | **It drives toward the camera** along a pseudo-3D road: the road is 8-line bands with per-band X scroll (PLAN's T-raster), and each size step streams the next pose while a smoke burst covers the swap (≤ 20 frames at 128 B) | cockpit, cannons | [new-art] L Must |
| **Wily Capsule** (W3 phase 2) | vanilla `$F2` (sprite) | | 0 | vanilla tiles, new palette (Must); a 16-bit redraw 60 tiles, 8 frames (Could) | vanilla | vanilla | [engine-ok] / [new-art] M Could |
| **AYACO** (Wind sortie, `venues_a.md`) | gorilla tank multi-part (T8) | 96x48 | 110 (Should) | sprite build (Must, §4.2) | crosses the sky band | engines | [new-art] L Should |

**CHR plan for a BG boss** (one rule for all): the arena's base set keeps ≤ 100 tiles for the room, floor, HUD digits
and the text glyph window; the boss gets the other **≥ 150 BG ids**. The MODE-7 Machine double-buffers its far and mid
sizes in two halves of that range and shows the near size alone (its swap is the only one covered by a full smoke
burst). Every BG boss gets a 32x32 **match-card portrait** (§9.2), since the vanilla boss-intro panel shows a
sprite pose that a BG boss does not have.

**Totals**: 870 BG tiles (Must 600: Yellow Devil 60, Gamma 200, MODE-7 Machine 340; Should 270: Mecha Dragon 150,
Cossack Catcher 120; AYACO's 110 are counted in §4.2), 126 sprite tiles of parts, plus Dark Man's 60.

---

## 7. Sprite list: new characters and frame counts

### 7.1 Player sheets (the player area, `$00-$70`, 113 tiles each)

| Sheet | Built from | New tiles | Frames | When loaded | Tags |
|---|---|---|---|---|---|
| **Super Rock** (H3 reward) | a composite of the Power sheet (body, fist arm) and the Jet sheet (backpack), redrawn where they meet | 70 | 30 (the vanilla Power set of poses + jet-hop + fist throw / catch) + the **rocket fist** 16x16 (3 frames, in the weapon slot) | form change, 16-frame stream (§2.6) | [new-art] M Must |
| **Break Man** (tag partner) | new; Blues' silhouette with the MM3 visor and scarf, the "Break Man" mask | 113 | 28: stand, run 3, jump, shoot (stand / run / jump), slide, ladder 2, hurt, teleport 3, whistle, shield-jump, Break Shot charge glow (2), knockback | the tag call (the beam-in covers the stream) | [new-art] L Should |
| **Bass β** (playable, Bass Mode) | new player sheet; Bass's boss set (§7.2) gives the base poses | 113 | 30: + dash, 8-way aim (Bass's buster) | file flag | [new-art] L Could |
| Set-piece poses in the weapon slot | pogo 2 (Yamato), vine hang / swing 4 (Plant), Rock-on-Rush loop 4 (Wind), condor carry 2 (Blizzard), swap flash 2 tiles | 20 | 12 | per venue | [new-art] S Must |

### 7.2 Bosses (sprite)

| Boss | Where | Tiles (enemy area ≤ 96) | Frames | Notes | Tags |
|---|---|---|---|---|---|
| 8 champions, rebuilt sets | venues | 0 new in phase 1; pinch sets 124 in all | 30 | §2.5, per venue in §4 | [new-art] M Must |
| **Bass β** | Semifinal, W2 | 90 | 22: stand, run 3, jump, shoot (stand / air / up / diagonal), dash 2, hurt, intro pose, teleport 3, taunt, defeat, buster shots (3) | Bass's RM7 look, before Treble; the "β" on his chest plate | [new-art] L Must |
| **Grand Pi-kun** | Opening | 70 | 14: waddle 2, bounce, spin, wave, flag throw, head-off (the costume head pops off at pinch to show a **Met inside**: reuse Metall tiles), dizzy, defeat | the GP mascot, a round costume robot with "GP" on its belly | [new-art] M Must |
| **Dark Man MK-VI** | H5 | 60 + 40 copied | 12 | §6 | [new-art] M Must |
| **Block / Paddle / Invader / Maze Man** | E1-E4 | 40-60 each | 10-16 each | §8 | [new-art] M Should |
| **Daruma** | Yamato 11 | in SET-YM3 | | `venues_b.md` §4.5.3 | [new-art] M Should |
| **The Knightlord / Hideout / Lost City / Wing Walker / Cloud Summit / Throne Room / Sunken Throne / Kabuki stage** | venue secret rooms | 0: the champion, re-staged | | venue docs; the secret arenas are BG (counted in §4) | [engine-ok] |

### 7.3 Cast and NPC sprites

| Who | Size | Tiles | Frames | Notes | Tags |
|---|---|---|---|---|---|
| **Eddie** | 16x24 | 12 | 3 (idle, hop, open lid) | Not in vanilla RM6: new. Pit stop, Tomahawk's window, the lobby | [new-art] S Must |
| **Roll** | 16x24 | 14 | 3 (idle, wave, refill) | Not in vanilla RM6: new. Pit crew, the lobby, Princess Roll (Knight) is a gown variant | [new-art] S Must |
| **Dr. Light** | 16x32 | 12 | 2 | Not in vanilla RM6 art | [new-art] S Must |
| **Dr. Cossack, Kalinka** | 16x32, 16x24 | 20 | 4 | cutscene bodies; the commentary booth | [new-art] S Must |
| **Mr. Y** | as Mr. X | 6 | 3 | **Vanilla Mr. X's sprite with a fake moustache and a "Y" pin**: the joke is that the disguise only changed one letter | [new-art] S Must (reuse) |
| **Dr. Wily** (unmasked) | | 0 | | vanilla RM6 Wily (ending, Mr. X reveal) | [engine-ok] |
| **Beat** | | 0 | | vanilla RM6 Beat (the BEAT weapon / plates) | [engine-ok] |
| **The judges' cut-out of Mr. Y** | 16x32 | 6 | 1 | holds up a "1"; the RESERVED sign after the unmasking | [new-art] S Should |

### 7.4 Totals

| | Tiles | Frames |
|---|---|---|
| Venue enemies, NPCs, set pieces (§4) | 996 | 299 |
| Player sheets and poses | 316 | 96 |
| Bosses (non-venue), guests, Opening extras | 626 | 148 |
| Cast | 70 | 16 |
| UI sprites (§9) | 250 | 14 |
| Weapon alt-fire tiles (`systems.md` §3) | 27 | |
| **All sprites** | **2,285 tiles** (from `budget.py`) | **573** |

---

## 8. Guest and exhibition art

BRIEF §6: "A guest or homage must be a mechanic, not just a sprite", parody names, no trademark logos. The art's job is
to make the rule readable at a glance; arena tiles are geometric, so Claude generates them (§11).

| Match | Guest (parody name) | The art carries the rule | Guest sprite | Arena BG | Tags |
|---|---|---|---|---|---|
| **E1** | **Block Man** (falling-block puzzle) | 7 tetromino shapes as **BG metatiles** in 3 colours (the arena's 3 BG palettes), a 10-wide well, a line-clear flash (palette); the stack is drawn by nametable writes, so it costs no sprites. Block Man himself is built from 4 blocks and re-arranges into the next piece's shape between attacks | 50 tiles, 12 frames (4 piece shapes + walk + throw) | 24 (programmatic) | [new-art] M Should |
| **E2** | **Paddle Man** (block breaker) | the brick shell around him is BG (bricks break by metatile write), the ball is a 8x8 sprite with a 3-frame trail, the power capsules are 16x8 sprites | 40 tiles, 10 frames | 20 (programmatic) | [new-art] M Should |
| **E3** | **Invader Man** (fixed shooter) | a formation of 3 invader-*robot* kinds (16x8, 2 frames each: **original designs**, not Taito's), destructible bunkers as BG (chipped per 8x8 tile), a saucer for the bonus, a ground line | 60 tiles, 16 frames | 24 (programmatic) | [new-art] M Should |
| **E4** | **Maze Man** (maze chase) | the maze is BG (walls, pellets, power pellets that blink by palette); the 4 "Met-ghosts" are **vanilla Metall tiles** in four ghost palettes, with a frightened palette and an eyes-only frame (2 tiles); Maze Man is a round robot with a mouth (4 directions x 2 frames, flips used) | 40 tiles, 14 frames | 24 (programmatic) | [new-art] M Should |
| Venue guests | AYACO (1942's big bomber), the DQ cast (Metslime, Killer Chest, the King), Six-Shot Sam, the robot cat, Toppy and Nitpicky, Shadow Rock, the Jaja-nin, the Reap-bot | counted in §4 | | | |
| Legacy guests | the MK-VIs (§6) | counted in §6 | | | |

---

## 9. UI art

### 9.1 Title [new-art] M · Must

- **Logo**: keep vanilla's ROCKMAN 6 logo (142 tiles) and add a **"GP" badge as sprites** (two 16x24 letters in red
  and gold, a 2-frame glint; 16 sprite tiles; the title's sprite table is 251 tiles free).
- **Subtitle**: 史上最大の戦い!! → **史上最大のグランプリ!!**. 史上最大の and !! are vanilla logo art and stay; 戦い (≈ 8
  tiles) is replaced by グランプリ drawn in the same brush style (≈ 20 tiles). The extra 12 tiles come from the pattern-table
  split (§2.8): the menu text moves to the sprite table, freeing the 16 text tiles.
- **Menu**: GAME START / SPECIAL EVENTS / CONFIG / ©CAPCOM 1993 / ROCKMAN 6 GP FAN PATCH, from a 40-glyph caps font in
  the sprite table, under the split at line 112.
- **Moon**: kept (90 tiles), as `meta.md` §2.1 asks.

### 9.2 File select, bracket, match card [new-art] M · Must

| Screen | New art | Tiles |
|---|---|---|
| **File select** ("ENTRANT REGISTRATION") | three card frames (vanilla blue frame tiles), 8 venue icons 16x16 (the champions' faces at icon scale), medal colours by palette, the Bass icon, Kalinka with her clipboard (32x48 sprite, 2 frames) | 40 BG + 24 sprite |
| **Bracket** | the 8 vanilla 32x32 portraits **kept**; new: bracket lines (straight, corner, T, gold when lit by palette, grey when not), rivets, the centre frame states (trophy silhouette, lit trophy, **Bass β portrait in a cracked frame**, the fortress logos, Rockman's face on the trophy) | 60 BG |
| **Bracket sprites** | 4 badge rings + 4 guest icons (blink by palette), medal ribbon (1 shape, 4 palettes), POSTPONED stamp (32x16), ★, plate letters B/E/A/T (vanilla), cursor | 30 sprite |
| **Match card** | vanilla's typed boss-intro panel (`$3C:$81B1`), extended. New: portraits for the entrants without a sprite pose (5 BG bosses, AYACO) and for the new sprite entrants' intro poses | 160 BG (10 x 16) |

### 9.3 Judges' desk and scorecard [new-art] M · Must

- The **desk** fills the top third: Cossack (head judge, centre), Kalinka (left), the **sponsor's chair** at the right
  with the cardboard Mr. Y cut-out holding a "1" (one sprite; after the unmasking an empty chair with a RESERVED sign).
  70 BG tiles (desk front, chairs, name plates, the GP banner), drawn under the pattern-table split so the rows
  below use the second page.
- **Scorecard rows**: TIME / DAMAGE / VARIETY / SECRETS / STYLE in the caps font, vanilla digits, a slide-in tick.
- **Medal stamp**: one 32x32 stamp shape in 4 palettes (bronze, silver, gold, platinum) plus the C / N / H / 93 preset
  badge and the TURBO `*`. 24 sprite tiles.
- **Secret icons** (exit, room, item, plate, envelope): 5 x 16x16, lit or dim by palette. 20 sprite tiles (shared with
  the file cards and the pause menu).

### 9.4 Portraits [new-art] L · Must

32x32 BG portraits (16 tiles each) in the CX style (cx/graphics.md §8: grey-scale plus one accent colour), loaded only
while a scene window is up. **12 faces**: Cossack, Kalinka, Dr. Light, Roll, Eddie, Break Man (and his "NO" variant
for the TURBO refusal), Bass β, Mr. Y, Rockman, Dr. Wily, Beat. 192 tiles. Each face has 2 mouth frames by a 2-tile
swap (+24 tiles), so a talking face costs no extra layout.

**In-stage pop-ups** use a **16x16 face icon** instead (4 sprite tiles each: Cossack, Kalinka, Mr. Y, Break Man, Roll,
Eddie = 24 tiles), streamed into the enemy area's free tiles; the text glyphs go into free BG ids (§9.6). A full portrait never appears
during play: the 8 KB CHR-RAM cannot hold one beside a venue.

### 9.5 Pit stop, chips, PARTs [new-art] M · Must

- **Pit stop**: Eddie's counter, shelves of E-tanks and bolts, the garage door, the Mr. Y booth (Should, 16 sprite
  tiles); 70 BG tiles. Eddie behind the counter is BG (his 3-frame body is for in-stage use).
- **Chip icons**: **21 icons, 16x16 each** (84 sprite tiles), one per `systems.md` §9.2 chip, read at a glance:
  balance scale (BALANCER), spring (SHOCK ABSORBER), spike with a shield (SPIKE GUARD), lightning bolt (CHARGE KIT),
  fuel can (JET TUNER), two arrows (EXCHANGER), ghost Rock (AFTERIMAGE), drop (ENERGY SAVER), helmet (IRON HELMET),
  thermos, seed, glider wing, **the Yashichi pinwheel** (Capcom's own icon), "!" star (KAISHIN), sheriff star, leaf
  (AUTO RECOVER), chains, flame with a slash (FIREPROOF), Centurion helmet, daruma, and a suspicious "Y" (Y-TURBO).
- **PART icons**: 8 x 16x16 (32 tiles, Should) + token, envelope and W-tank icons (12 tiles).

### 9.6 Text window, fonts, pop-up glyphs [new-art] S · Must

- **Window**: 6 tiles (corners, edges) + blank, white on black.
- **EN font set**: lowercase a-z + `" - ;` in the kana slots of the main font (`rm6/text.md` §7, option 1): 30 tiles.
  JP stays kana-only (vanilla has no kanji in text). ENGRISH uses the EN set.
- **Glyph allocator (in-stage pop-ups)** [new-code] S Must: a 2-line pop-up uses only its **distinct** glyphs (typically
  18-24 for EN, 20-26 for kana). The build computes, for every screen and its scroll neighbours, the BG ids no visible
  tile uses (the **free-id map**, §10.5) and stores up to 32 of them; the pop-up uploads its glyphs there (≤ 3 frames
  of streaming). Where fewer than 24 ids are free, the line is **deferred** to the next screen that has room, or shown
  in its short form. Boss rooms have room: they reference 52-195 BG tiles (§1.4). This is 4MI's per-message canvas
  (r4mi/graphics.md §7), generalised.

### 9.7 HUD, pause menu, labels [new-art] S · Must

- WEAK! / CRIT! / ?! in GP-COMMON (§2.4): 3 + 4 tiles.
- Fuel pip (1), swap flash (2).
- Status words as 4-tile labels: `ACE 100%`, `LEVEL UP`, `BOUNTY`, `TIME STOP` (24 tiles, per venue sets).
- Pause menu: weapon icons for M.BEAM and SUPER, the chip-slot strip (6 slots), the Break Man call line and his
  portrait slot (30 BG tiles; the menu's own CHR, `rm6/text.md` §7: 108 free BG tiles in the vanilla pause menu).

### 9.8 Maps, plaques, ending, post-game

| Item | Tiles | Tier |
|---|---|---|
| Hall of Fame map (a museum floor plan with 5 wing doors) and Super Wily Castle map (vanilla fortress-map pages, new skull-castle-with-a-"16-BIT"-antenna) | 150 BG | Must |
| Plaques: frame + 5 wing emblems (helmet silhouettes by era) | 40 BG | Should |
| Trophy ceremony, championship rating screen (a podium, the trophy 48x64, the rating meter) | 120 BG | Must |
| Achievement plates, museum booth meters, the dancing Rockman and Roll (reuse their sprites) | 40 BG | Could |
| Weapon-get cards for M.BEAM and the Super Adaptor | 0 | vanilla YOU GET screen and font |

---

## 10. The pipeline

### 10.1 Layout in the repo [new-code] M · Must (tools)

```
assets/chr/<group>/<set>.png + <set>.json      # one CHR set per sheet (BG third, sprite set, pinch set, font)
assets/sprites/<object>.json (+ <object>.png)   # metasprites: frames, layouts, animations
assets/bgboss/<boss>/pose_*.png + boss.json     # BG-boss poses, nametable blocks, hit boxes, streams
assets/palettes/<stage>.json                    # start program + per-exit / per-screen updates
assets/music/<track>.mml, assets/sfx/<id>.mml   # music and SFX sources (§12.7)
tools/build/{chr.py, sprites.py, bgboss.py, palettes.py, artcheck.py, mml.py, fms2mml.py, sndtest.py}
```

### 10.2 PNG ↔ CHR (`tools/build/chr.py`)

- Input: an indexed PNG with ≤ 4 colours per 8x8 tile, or any PNG plus the palette JSON that maps its colours to 0-3.
  Output: raw 2bpp planar CHR (RM6 stores CHR uncompressed, `rm6/SUMMARY.md` §6).
- `chr2png` + `png2chr` must **round-trip every vanilla CHR set byte for byte** (the first test, as `levels.py` did for
  levels).
- Sprite sheets may dedupe flipped tiles (sprites can flip); BG sheets may not (the NES cannot flip BG tiles).
- Reserved but undrawn slots are filled with a visible marker tile (4MI's "R-box", r4mi/graphics.md §2), never left
  blank, so a tile editor shows the allocation.
- **Provenance** column in every set JSON: `vanilla` (with its source address), `new`, `recolour`, `copy-of`. The
  credits and the novelty census read it.

### 10.3 The CHR set manifest and the packer

Each `<set>.json`: `{"id": "local:E3" | "global:7C", "ppu": "spr:A0" | "bg:0A0", "count": 48, "sheet": "...png",
"palette": "...", "stage": "plant"}`. The packer:

1. places sets into the new CHR banks (8 KB = 512 tiles each, a set may cross into the next bank as vanilla's do);
2. writes the v2 set table (§2.1) and the per-stage local tables;
3. leaves the 1,126 vanilla gap tiles (§1.3) as a **reserve**: GP does not need them, and leaving Capcom's banks
   byte-identical keeps the "never overwrite Capcom art" check trivial.

### 10.4 Metasprite JSON (`tools/build/sprites.py`)

```json
{ "object": "toppy", "chr_set": "local:E0", "base_tile": "A0", "palette": 2,
  "frames": { "walk0": [[-8, -16, "02", "pal2"], [0, -16, "03", "pal2"], [-8, -8, "12", "pal2"], [0, -8, "13", "pal2"]],
              "walk1": "...", "push": "...", "stun": "..." },
  "anims":  { "walk": {"half": 0, "seq": [["walk0", 8], ["walk1", 8]]}, "stun": {"half": 0, "seq": [["stun", 90]]} } }
```

The compiler emits Capcom's format exactly (`rm6/engine.md` §1.5, verified 118/118): per frame `[n-1][layout id]` + n x
`[tile][attr]`; layouts `[dy][dx]` **deduplicated by geometry** (frames that share a pose shape share a layout, as Capcom
did); animations = half flag + `[frame][duration]` pairs; pointer tables at `$8000-$87FF` of a **GP sprite bank pair**
(each table holds 256 entries per half, 512 frames per pair). The 573 new frames need **3 new sprite bank pairs**
(venue objects; bosses and players; UI), allocated by `tech.md` through the X-GPOBJ sub-id → sprite-bank table.

`sprslice.py` imports a PNG frame strip (Aseprite export): it cuts each frame on an 8x8 grid aligned to the object's
origin, dedupes tiles (with flips), and writes the tiles into the set and the frames into the JSON. Validation:

- ≤ 16 hardware sprites per frame; ≤ 4 per 8-px row inside one frame;
- every tile inside its set's range; palette 1 or the object's declared enemy palette (§3.2);
- a preview GIF per animation (`sprites.py preview`) for review.

### 10.5 `artcheck.py`: the build's art gate [new-code] M · Must

Runs on every build, over the level JSON (`levels.py` export) and the asset manifests:

1. **Enemy-area overlap**: per screen (and the sets still resident from the 8-entry "recently loaded" list), no two
   sprite sets overlap. Vanilla has 4 such screens (§1.4); GP may have none.
2. **Enemy palette conflict**: per screen, at most one program each for sprite palettes 2 and 3.
3. **BG free-id map**: per screen and scroll neighbours, the BG ids referenced after the screen's CHR state. Proves
   every third safe, and stores up to 32 free ids per screen for the pop-up glyph allocator (§9.6).
4. **Flicker simulation**: for each wave director (Wind sortie, Tomahawk gallery and train) and each boss pattern,
   step the object boxes frame by frame and count sprites per scanline; fail above the §3.4 budget.
5. **Streaming budget**: every stream (form swap, pinch, BG-boss pose, glyphs) fits the window the design gives it.
6. **Capcom art untouched**: every vanilla CHR byte in the built ROM equals `rm6j.nes`.
7. **Novelty census**: on the golden-movie states, the share of new BG and sprite tiles per screen, and **ghost frames**
   (4MI's `ghost.py`: vanilla tiles dithered, new art in colour) for the review gallery.

### 10.6 OAM census (`artcheck.py census`)

Plays every golden movie and records which sprite tiles are ever drawn. It confirms the 6 free common-row slots and the
rarely drawn player tiles (`$37`, `$38`, `$3B`, `$3C` were never drawn in 73 states, §1.1) before GP-COMMON uses them.

### 10.7 BG-boss nametable art (`tools/build/bgboss.py`)

- Author each **pose** as a PNG on a 16x16 attribute grid, ≤ 4 BG palettes, one palette per 16x16 block (checked).
- The tool cuts unique 8x8 tiles (no flips), **shares tiles across poses**, and emits: one CHR set per pose (the delta
  over the previous pose, so a pose change streams only what differs), the nametable block (rows x cols of tile ids),
  the attribute bytes, the palette program, and the stream list with byte counts per transition.
- `boss.json` holds the hit boxes relative to the boss origin (the invisible hit-box objects follow the scroll, as in
  vanilla), the sprite parts (eyes, fists, claw) with their metasprite JSON, and the raster entries (floor split line).
- A preview renders every pose over its arena with the HUD, and checks that pose + room + HUD + glyph window fit in
  256 BG ids.

### 10.8 Palettes (`tools/build/palettes.py`)

Palette JSON per stage: the start program and every update by exit, script or thread, compiled to vanilla's partial
programs (start index, colours, bit 6 = write `$0F` first, bit 7 = last; `rm6/levels.md` §7). The revisit palettes
(bank `$28`) get the same format.

---

## 11. Who draws what, and the workload

### 11.1 The split

| Who | What | Why |
|---|---|---|
| **Claude, programmatic** (C) | Geometric and rule-driven art: the 4 Exhibition arenas (tetrominoes, bricks, bunkers, maze walls), bracket lines and frames, scorecard rows, digits reuse, the W-SEA band, the **2600 canopy** (fat-pixel by design), rain frames, starfields, dithers, the **MODE-7 floor stripes** (computed perspective), the Game Boy and dusk palette tiers, the text-window frame | Exact, repeatable, cheap to iterate; the generator script is the source |
| **Claude, mechanical reuse** (R) | Recolours and copies: Shadow Rock, Metal Metslime, Mr. Y, Dark Man's disguise, the Met-ghosts, Princess Roll's palette, all palette tricks of §3.2, rebuilding vanilla sets into GP sets | Pure data work on vanilla tiles |
| **Claude drafts, a human cleans** (D) | Venue BG thirds (carrier deck, saloon, town, palace, Edo street, caverns), stadium, H-wing tiles, UI screens (desk, pit stop, maps), chip and PART icons, small enemies and NPC set-piece props, Super Rock (a composite of two vanilla sheets), the EN lowercase font | Claude can lay out tiles that read correctly at 16x16 and keep palettes legal; a pixel artist fixes clusters, anti-aliasing and charm |
| **Human pixel artist** (H) | Characters with animation (Bass β, Break Man, Grand Pi-kun, the guests, NPCs with personality, champion pinch forms), **all BG bosses** (Yellow Devil, Mecha Dragon, Gamma, Cossack Catcher, MODE-7 Machine in 3 sizes), the 12 portraits and match-card portraits, the logo kana グランプリ, the GP badge | Characters and big set pieces are where a hack is judged (4MI's lesson: "the memorable art is the T-rex, the whale, the sky") |

**Placeholder first** (process rule, Must): every asset exists from day one as a Claude-generated **greybox** with the
final size, tile count, palette slots, frame count and timing. Code and levels never wait for art; the human replaces
PNGs, and `artcheck.py` keeps the budget honest.

### 11.2 Workload (from `budget.py`)

| | BG tiles | Sprite tiles | Frames |
|---|---|---|---|
| Human (H) | 1,368 | 1,594 | 419 |
| Claude draft + human cleanup (D) | 2,630 | 649 | 147 |
| Claude programmatic (C) | 510 | 36 | 4 |
| Reuse (R) | 0 | 6 | 3 |

Rough human hours (assumptions: a finished BG tile from scratch 5 min; an animated sprite frame 1.5 h including its
tiles; cleaning a Claude draft 1.5 min per BG tile and 30 min per frame):

| Tier | Hours | |
|---|---|---|
| Must | ≈ 660 | about 16 weeks at 40 h, or a year of evenings |
| Should | ≈ 160 | |
| Could | ≈ 70 | |
| **All** | **≈ 890** | |

The biggest single items: the MODE-7 Machine's three sizes (340 BG tiles ≈ 28 h), Gamma (200 ≈ 17 h), Bass β and Break
Man (50 frames ≈ 75 h), the 12 portraits (≈ 20 h), the venue enemy casts (≈ 300 frames ≈ 330 h with cleanup).

**If no pixel artist joins**, Claude can still ship Must at a lower bar: the D items become final, the H characters
are drafted by composing vanilla parts (Bass β from Rockman's skeleton, Break Man from Rockman's sheet with a scarf and
visor, as CX built Quick Man partly from RM2 boss art), and the BG bosses are drawn as blockier shapes (Yellow Devil is
blocks anyway). §17 lists this as the top art risk.

---

## 12. Music and sound

### 12.1 Policy

1. **Vanilla themes stay.** Each venue keeps its RM6 stage theme as its main theme (`venues_b.md` §5.4 agrees), and
   the champion fights keep `$0C`. RM6's eight themes are the champions' identity; the homage is carried by **set-piece
   cues** in the genre of the homage.
2. **Every new track has a vanilla fallback id** (PLAN §6.5), so a stage is playable before its music exists.
3. **Originals, not quotations.** New tracks are original compositions *in the style* of the homage. Exceptions:
   - **Public-domain melodies** may be arranged: *Korobeiniki* (E1's falling-block arena) and the folk song
     ***Kalinka*** (I. Larionov, 1860): Kalinka the commentator gets it as her 3-second sting. Cossack's daughter was
     named after it; now the game admits it.
   - **Capcom's own Rockman 1-5** music may be arranged: the Hall of Fame wings (the museum *is* of those games) and
     Break Man's whistle (he is MM3's Break Man), re-sequenced from scratch for RM6's driver. No sound data is imported
     from other ROMs (BRIEF §7.4).
   - Everything else (1943, Dragon Quest, Pitfall, Ice Climber, Prince of Persia, Jajamaru, Atlantis, Tetris's other
     tunes, Space Invaders, Pac-Man, Breakout) is **evoked, never quoted**: scale, rhythm, instrumentation, form.
4. **The MMC5 voices are a layer, never a requirement.** Every 6-channel track must stand alone on the 4 base channels
   (MMC5 AUDIO OFF in CONFIG; an NES-001 without the expansion-audio mod; emulators without it).

### 12.2 Driver work [new-code] (built by `tech.md`; specified here)

| Id | Change | Why | Size | Tier |
|---|---|---|---|---|
| D1 | **Per-track bank byte** table; the single reader `$34:$803A` maps the track's bank (CX `$18:97B7`, 4MI `$1E:$8E51`) | new music outside `$34-$36` | S | Must |
| D2 | Track table grows from 102 to 240 ids, moved to a new bank with D1's table | ~100 new ids | S | Must |
| D3 | Instrument table moved (its pointer is at `$34:$8A41`) and grown past 71 entries | new timbres | S | Should |
| D4 | The driver's own bank switch (`$34:$804E-$8060`) ported to MMC5 | porting checklist | S | Must (`tech.md`) |
| D5 | **MMC5 pulses**: a second instance of the channel interpreter with its own RAM block (in WRAM) and register base `$5000`; header byte 0 = `$01` marks a 6-channel track with 2 extra channel pointers | "16-bit" layer | M | Could (BRIEF §9) |
| D6 | **The hardware multiplier** (`$5205/$5206`) replaces the driver's 8x8 multiply loop `$8006`, its hottest loop (4MI did the same) | the driver is 18 % of the frame (`rm6/engine.md` §8); D5 must be cycle-neutral | S | Must with D5, Should otherwise |
| D7 | **Charge sound on MMC5 pulse 1** (4MI's trick): holding a charge no longer steals a music channel | music never drops notes while charging | S | Should |
| D8 | MMC5 AUDIO ON/OFF: OFF mutes `$5000-$5007` writes and returns the charge sound to its SFX | BRIEF §5.7 | S | Must if D5 or D7 ship |
| D9 | **Channel mute mask** set by the game (`$D8`-style request) | W1's tiers; the sound test's meters | S | Should |
| D10 | **Tempo override** request (writes `$C9/$CA`) | E3's formation tempo, Blizzard's bonus countdown | S | Should |
| D11 | Several ids may enter one song at different offsets (a header pointing into the same channel data) | stage/duel variants for free | S | Must (data only) |
| D12 | DPCM drums (kick, snare, crash, clap ≈ 2.5 KB; needs a switchable `$C000-$DFFF` window) | "16-bit" punch | M | Could |
| D13 | A raw-PCM announcer clip ("READY... GO!", ≈ 0.5 s at 8 kHz ≈ 4 KB) during a frozen frame (CX's Ultraman cry, 21.7 KB) | the GP's voice | S | Could |

Id plan: vanilla `$00-$65` unchanged; the empty stub `$1A` and the unused SFX `$3D/$3E/$4D/$51` are recycled first;
new music `$66-$9F`, new SFX `$A0-$EF`.

### 12.3 Track list: every stage and scene

"Ships with" is what the scene plays at Must; "Upgrade" names the new track (G-numbers, §12.5) and its tier.

| Scene | Ships with (Must) | Upgrade | Style |
|---|---|---|---|
| License, attract crawl | vanilla `$0E`, `$0D` | | |
| **Title** | **G01 GP FANFARE → G00 GRAND PRIX MARCH (title cut)** | | a stadium march: 25 % duty brass lead, snare rolls on noise, triangle tuba |
| File select | vanilla `$15` | G05 PIT STOP (Should) | |
| **Opening Ceremony** | **G00 (stage cut, D11 entry)** | | march with a crowd-chant B section |
| Grand Pi-kun | vanilla `$0C` | | |
| Bracket | vanilla `$0F` (the stage-select theme *is* the bracket) | | |
| Match card | vanilla `$10` | | |
| Venue stages | vanilla `$00-$07` | set-piece cues (§12.4) | |
| Champion fights, secret arenas | vanilla `$0C` | | |
| Boss defeated / YOU GET | vanilla `$13` / `$16` | | |
| **Judges' desk** | **G02 THE JUDGES + G03 MEDAL STAMP (4 ids, D11)** | | a game-show "thinking" loop; the stamp is one stinger transposed per medal |
| Pit stop | vanilla `$15` | G05 PIT STOP (Should) | Eddie's shop: bouncy bass, a cash-register riff |
| Commentator pop-up | SFX chime | G06 KALINKA! sting (Should) | the PD folk tune, 3 s, on Kalinka's first pop-up per stage |
| **Semifinal Riot, Bass duels** | **G04 BETA** (stage and duel entries, D11) | | the rival theme: Bass's arrogance in a minor key, the tune Break Man's whistle answers in W2 |
| Exhibitions E1-E4 | vanilla `$0C` | G18-G21 (Should) | §12.4 |
| Hall of Fame map | vanilla `$11` | G07 HALL OF FAME (Should) | a quiet museum audio-guide loop |
| H1-H5 stages | vanilla `$09` | G08-G12 TRIBUTES (Should) | each an arrangement of its game's fortress theme |
| MK-VI fights | vanilla `$0C` | G13 LEGACY BOSS (Should) | |
| Castle map | vanilla `$12` | | |
| W1 Upgrade Lab | vanilla `$0B` | G14 UPGRADE LAB (Should, D9 tiers); its MMC5 voices G14x (Could) | starts as a 2-pulse "Game Boy" mix, the triangle and noise join at the NES tier, the MMC5 voices at the 16-bit tier |
| W2 Bracket of Doom | vanilla `$0B`; G04 for Bass | G34 16-BIT WILY STAGE (Could) | |
| W3 MODE-7 Machine, Capsule, escape | vanilla `$18` | G15 FINAL CHAMPIONSHIP (Should), G15x MMC5 voices (Could), G35 (Could) | |
| Trophy ceremony | vanilla `$17` | G16 CHAMPION (Should) | |
| Victory-lap credits | vanilla `$0A` | G17 VICTORY LAP (Should) | a 3-minute medley of the GP themes |
| Ending scenes, newspaper, TO BE CONTINUED | vanilla `$08`, `$1B-$22` | | kept (BRIEF §6: TO BE CONTINUED stays) |
| Rating screen | G01 + G02 | | |
| Game over, continue | vanilla `$14`, `$15` | | |
| Break Man's call | SFX | G27 WHISTLE (Should) | Blues' whistle tradition, 2 s |
| Mr. Y's booth, heckles | vanilla `$09` | G33 MR. Y (Could) | a sleazy tango |
| Players' Tunnel lobby | G00 (lobby entry) | | |
| Bass Mode | G04 | G36 (Could) | |

### 12.4 Style per venue (genre homages, evoked)

| Venue | Main theme | Set-piece cue (tier) | Style in driver terms |
|---|---|---|---|
| Wind / 1942-43 | `$00` | **G22 SORTIE** (Should), POW / LOOP / ACE 100 % stingers (Should) | an arcade-shooter march: driving 16ths on the triangle, pulse 2 an "engine drone" with a slow detune wobble (cmd `0C`), a 50 % duty heroic lead in a minor key |
| Knight / Dragon Quest | `$07` | **G23 ENCOUNTER** (Should), inn and level-up stingers (Could) | a short baroque-flavoured battle loop: a running 16th bass on the triangle, a fanfare lead, no borrowed phrases |
| Tomahawk / Gun.Smoke, Wild Gunman | `$06` | **G24 4:50 TRAIN** (Should), duel stinger (Should), G32 honky-tonk (Could) | a galloping 2/4 shuffle, a "harmonica" lead on 12.5 % duty with slides (cmd `0D`), a whistle slide, chugging noise |
| Plant / Pitfall | `$04` | G29 LOST CAVERNS (Could) | a TIA-flavoured tune: square leads on a deliberately "out of tune" scale (per-note detune), sparse, no triangle |
| Blizzard / Ice Climber | `$01` | **G25 BONUS SUMMIT** (Should) | a 40-s bonus-round romp: staccato bells (12.5 % duty, short gate), oom-pah triangle; D10 speeds it up in the last 10 s |
| Flame / Prince of Persia | `$03` | G31 PALACE (Could) | harmonic minor (Hijaz), slow 6/8, triangle drone, sliding pulse ornaments |
| Centaur / Atlantis, Kid Icarus | `$05` | G30 UNDERWATER (Could) | slow minor arpeggios in triplets (cmd `00`), the second pulse as an echo |
| Yamato / Jajamaru, Goemon, DuckTales | `$02` | **G26 KABUKI** (Should) | yo / in pentatonic, a plucked 25 % pulse with a short gate (shamisen), noise clappers (hyoshigi) that accelerate, a pitch-swept triangle taiko |
| E1 Block Man | | **G18 KOROBEINIKI REMIX** (Should) | the PD folk song at 160 bpm, our own arrangement; the commentators clap along |
| E2 Paddle Man | | **G19 BRICK FUNK** (Should) | a syncopated bass and a hi-hat noise groove |
| E3 Invader Man | | **G20 FORMATION** (Should) | a 4-note bass ostinato (original notes) whose tempo follows the formation (D10): the mechanic as music |
| E4 Maze Man | | **G21 CHASE** (Should) | a chase loop and a power-pellet entry (D11) with a siren lead |

### 12.5 The new tracks and their bytes

Sizes are estimated from vanilla (`songsizes.py`): stage theme 617-1,238 B (mean 1,010), fortress stage 788-871, boss
633, Wily Machine 575, jingles 116-260, ending scenes 349-546. MMC5 voices add ~50 % to a track.

| # | Track | Bytes | Tier | Fallback |
|---|---|---|---|---|
| G00 | GRAND PRIX MARCH (title, Opening, lobby entries) | 1,150 | Must | `$19` / `$0D` |
| G01 | GP FANFARE | 180 | Must | `$16` |
| G02 | THE JUDGES | 420 | Must | `$15` |
| G03 | MEDAL STAMP (4 ids) | 190 | Must | `$13` |
| G04 | BETA (stage + duel ids) | 1,050 | Must | `$0B` |
| G05-G07 | PIT STOP 520, KALINKA! 90, HALL OF FAME 520 | 1,130 | Should | `$15`, none, `$11` |
| G08-G12 | H1-H5 TRIBUTES, 900 each | 4,500 | Should | `$09` |
| G13 | LEGACY BOSS | 650 | Should | `$0C` |
| G14 / G14x | UPGRADE LAB 1,100 / MMC5 voices 550 | 1,650 | Should / Could | `$0B` |
| G15 / G15x | FINAL CHAMPIONSHIP 1,000 / MMC5 voices 500 | 1,500 | Should / Could | `$18` |
| G16, G17 | CHAMPION 700, VICTORY LAP 1,500 | 2,200 | Should | `$17`, `$0A` |
| G18-G21 | Exhibition themes (750, 700, 500, 700) | 2,650 | Should | `$0C` |
| G22-G26 | SORTIE 1,000, ENCOUNTER 600, TRAIN 900, BONUS 400, KABUKI 800 | 3,700 | Should | the venue's theme |
| G27, G28 | WHISTLE 110; 8 stingers (duel bell, inn, level-up, POW, LOOP, ACE 100 %, secret found, plate) 600 | 710 | Should | SFX |
| G29-G33 | LOST CAVERNS 600, UNDERWATER 700, PALACE 700, HONKY-TONK 500, MR. Y 350 | 2,850 | Could | the venue's theme |
| G34-G36 | 16-BIT WILY STAGE 1,300, 16-BIT WILY MACHINE 900, BASS MODE 800 | 3,000 | Could | `$0B`, `$18`, G04 |
| | **Total: 37 compositions + 2 MMC5 layers, 51 track ids** | **27,530** | Must 2,990; Should 17,640; Could 6,900 | |

### 12.6 SFX

New SFX are 10-60 B each (vanilla mean 29 B). **Must** (≈ 20, ≈ 440 B: they fit the 449-B tail of bank `$36`, though
their ids still need D2): weapon-cycle tick, form-swap whoosh, parry "ting", WEAK crunch, results tick, total roll, medal thunk,
shop buy and deny, chip click, pop-up chime, crowd cheer (a noise swell), crowd "ooh" on a death, bonk, gate rumble,
plate click, door unlock, chest open, ice-cell break, pogo boing, gunshot.

**Should** (≈ 45, ≈ 1.35 KB): catapult, POW change, loop whoosh, gust, lamp, DQ menu blip, spell, train whistle, DRAW
bell, ricochet, bounty stamp, thunder, croc snap, log roll, tar bubble, vine creak, cat, Toppy push, condor cry,
chomper "shing", mouse squeak, door fade, siren, slot reel, chirp, scroll spin, wooden clappers, hanabi fuse and
burst, daruma chime, line clear, ball bounce, brick break, saucer whine, maze munch, ghost eaten, yoku "pip", dragon
roar, crane motor, engine rev, M.BEAM hum, rocket-fist launch / return, jet hop.

**Could**: the "pikoon" critical (`systems.md` §14), piano plinks, crowd gasp.

Reuse vanilla wherever it fits (explosions, dink `$27`, item pickups, the heal tick `$31`). SFX priorities follow the
vanilla rule (a new SFX plays only if its priority ≥ the current one, `rm6/engine.md` §5.2): UI and crowd SFX get low
priority so they never cut a weapon sound.

### 12.7 Composition pipeline: MML → driver bytecode

**`tools/build/mml.py`** [new-code] M · Must. A small MML compiler whose output is exactly the decoded command set
(`rm6/engine.md` §5.3), plus a **decompiler**. **Test 1: decompile all 36 vanilla tracks to MML and recompile them
byte-identically** (the `levels.py` standard).

| MML | Bytecode | Notes |
|---|---|---|
| `c d e f g a b`, `+` / `-`, `r` | note byte: length index (bits 7-5) + pitch (bits 4-0); 0 = rest | pitch = semitone above the octave base |
| lengths `1 2 4 8 16 32 64` | length index 7..1 → 192, 96, 48, 24, 12, 6, 3 ticks | whole note = 192 ticks |
| `.` | `02` dot (x1.5, one note) | |
| `{ ... }` | `00` triplet on / off | lengths 128, 64, 32, ..., 2 |
| `&` | `01` tie (legato into the next note) | |
| `o n`, `>` / `<` | `09` octave, `03` octave+ toggle | |
| `t hhll` | `05` tempo (16-bit tick increment per frame) | |
| `q n` | `06` gate (note-on fraction / 256) | |
| `v n`, `@ n`, `@d n` | `07` volume, `08` instrument (8-byte envelope), `18` duty | |
| `k n`, `K n`, `D n`, `s n` | `0B` transpose, `0A` global transpose, `0C` detune, `0D` slide | |
| `[ ... ]n`, `|` | `0E-11` loop 1-4 (nested), `12-15` break on the last pass | |
| `L` | `16` jump (the loop point at the channel's end) | |
| `!` | `17` end | |
| `F n` | `04` flags | |
| channels `A B C D` (+ `E F` for MMC5, D5) | header: type byte, then big-endian channel pointers | `D` = noise: pitches index the noise periods |

- **`fms2mml.py`** [new-code] M · Should: a human composer writes in **FamiStudio** (it supports the MMC5
  expansion), exports text, and the converter maps notes, volumes (to instrument envelopes), duty and slides; it
  **rejects** effects the driver lacks rather than approximating them silently.
- **`sndtest.py`** [new-code] S · Must: builds a ROM that plays one track id, records the APU through the emulator
  harness to WAV, and reports **driver cycles per frame** (rule: no new track may exceed the busiest vanilla track,
  because the driver is already 18 % of the frame).
- The packer places each track wholly inside one music bank and fills D1's bank table; it prints the free bytes per
  bank.
- Who writes: Claude can write MML for jingles, SFX, the march and the stylistic cues (the forms are well defined);
  the Hall of Fame arrangements and the big themes (G04 BETA, G15, G17) want a human composer or a human pass.

### 12.8 Byte budget against the free sound space

| | Bytes | Where |
|---|---|---|
| Vanilla music + SFX (kept) | 20,728 | `$34-$36` (unchanged) |
| Free in vanilla sound banks | 449 | `$36` tail: the Must SFX |
| New music, Must | 2,990 | music bank M0 |
| New music, Should | 17,640 | M0-M2 |
| New music, Could | 6,900 | M3 |
| New SFX, Should and Could | ≈ 1,450 | M0 |
| DPCM drums (Could, D12) | ≈ 2,500 | a bank mapped at `$C000` |
| PCM announcer (Could, D13) | ≈ 4,000 | any bank (CPU-played) |
| **Total new** | **≈ 35.9 KB** | **5 new 8 KB banks (40 KB)**, or **3 banks (24 KB) for Must + Should** |

For scale: vanilla RM6 has 18.8 KB of music; CX added 38 songs in 3 banks; 4MI 47 songs in 36 banks of gaps.

---

## 13. Totals

### 13.1 Art (ledger: `build/design/design-art-audio/budget.py`)

| | BG tiles | Sprite tiles | All tiles | Frames |
|---|---|---|---|---|
| **Must** | 3,228 | 1,623 | **4,851** | **421** |
| Should | 1,208 | 465 | 1,673 | 107 |
| Could | 72 | 197 | 269 | 45 |
| **All** | **4,508** | **2,285** | **6,793** | **573** |

| By area | BG | Sprite | Frames |
|---|---|---|---|
| 8 venues | 1,362 | 996 | 299 |
| Opening, Semifinal, Exhibitions | 338 | 380 | 98 |
| Hall of Fame H1-H5 (incl. BG bosses) | 1,010 | 156 | 34 |
| Super Wily Castle W1-W3 (incl. MODE-7 Machine) | 596 | 90 | 16 |
| Credits, lobby | 104 | 0 | 0 |
| Player sheets, cast, weapons | 0 | 413 | 112 |
| UI (title, menus, bracket, desk, shop, portraits, icons, maps, ending) | 1,098 | 250 | 14 |

**ROM**: 6,793 tiles x 16 B = **106 KB of new CHR**, which packs into **14-16 new 8 KB CHR banks** (Must alone: 76 KB,
10-11 banks). Plus 10 tileset banks (80 KB, §2.2) and 3 sprite bank pairs (48 KB, §10.4). Vanilla's 1,126 gap tiles
stay as a reserve.

For scale: 4MI added **5,266** new tiles; CX's screens are **70 %** new (4,128 distinct new tiles seen). GP's Must is
in 4MI's range because, like 4MI, it keeps every vanilla stage set and spends new pixels on set pieces, bosses and UI
(r4mi lesson 2).

**Human workload**: ≈ 890 hours in all, ≈ 660 for Must (§11.2).

### 13.2 Audio

| | Count | Bytes |
|---|---|---|
| New compositions | 37 (+ 2 MMC5 layers), **51 track ids** | 27,530 |
| of which Must | 5 (G00-G04) | 2,990 |
| New SFX | ≈ 70 (≈ 20 Must) | ≈ 1,900 |
| Samples (Could) | 4 drums + 1 voice | ≈ 6,500 |
| **All new sound data** | | **≈ 35.9 KB in 5 banks** (Must + Should: 3 banks) |
| Driver work | D1-D13 (§12.2) | Must: D1, D2, D4, D6 (with D5), D8 (with D5/D7), D11 |

---

## 14. Build list

| Item | Tags | Size | Tier |
|---|---|---|---|
| CHR set table v2 + stage-local ids (§2.1) | [new-code] | S | Must |
| 10 tileset banks + 2 empty vanilla slots (§2.2) | [new-code] data | S | Must |
| Section switch to slot `$89` (§2.2) | [new-code] | S | Should |
| GP-COMMON sprite set (WEAK!, pips, flash) (§2.4) | [new-art] [new-code] | S | Must |
| Weapon-slot alt-fire tiles and set-piece poses (§2.4) | [new-art] | S | Must |
| Rebuilt champion sets + pinch sets + streaming (§2.5) | [new-art] [new-code] | M | Must |
| Unrolled 256 B/frame CHR stream (§2.6) | [new-code] | S | Should |
| ExGrafix spike for W1 (§2.7) | [new-code] | M | Could |
| Pattern-table split for menus (§2.8) | [new-code] | S | Should |
| Venue art, 8 venues (§4) | [new-art] | L | Must (Should/Could rows as marked) |
| Non-venue stage art (§5) | [new-art] | L | per stage tier |
| BG bosses: YD, Gamma, MODE-7 Machine (§6) | [new-art] [new-code] | L | Must |
| BG bosses: Mecha Dragon, Cossack Catcher, AYACO BG (§6) | [new-art] [new-code] | L | Should |
| Super Rock sheet (§7.1) | [new-art] | M | Must |
| Break Man sheet (§7.1) | [new-art] | L | Should |
| Bass β boss set; Grand Pi-kun; Dark Man (§7.2) | [new-art] | L | Must |
| Bass β player sheet (§7.1) | [new-art] | L | Could |
| Cast sprites (§7.3) | [new-art] | M | Must |
| Exhibition guests and arenas (§8) | [new-art] | M | Should |
| Title (GP badge, subtitle, menu) (§9.1) | [new-art] | M | Must |
| File select, bracket, match card (§9.2) | [new-art] | M | Must |
| Judges' desk, scorecard, medal stamp (§9.3) | [new-art] | M | Must |
| 12 portraits + 6 face icons (§9.4) | [new-art] | L | Must |
| Pit stop, 21 chip icons (§9.5) | [new-art] | M | Must; PART icons Should |
| Text window, EN font, glyph allocator (§9.6) | [new-art] [new-code] | S | Must |
| Maps, ending, rating (§9.8) | [new-art] | M | Must; plaques Should; museum Could |
| Pipeline: chr.py, sprites.py, sprslice.py, bgboss.py, palettes.py (§10) | [new-code] tools | M | Must |
| artcheck.py (overlap, palettes, free-id map, flicker, streams, Capcom-untouched, census) (§10.5) | [new-code] tools | M | Must |
| Driver D1, D2, D4, D11 (§12.2) | [new-code] | S | Must |
| Driver D3, D6, D7, D9, D10 | [new-code] | S | Should |
| Driver D5 (MMC5 pulses), D8 | [new-code] | M | Could (Must D8 if D5/D7 ship) |
| Driver D12 (DPCM), D13 (voice) | [new-code] | M | Could |
| mml.py + vanilla round trip, sndtest.py (§12.7) | [new-code] tools | M | Must |
| fms2mml.py (§12.7) | [new-code] tools | M | Should |
| Music G00-G04 + Must SFX | [new-music] | M | Must |
| Music G05-G28 + Should SFX | [new-music] | L | Should |
| Music G29-G36, G14x, G15x | [new-music] | M | Could |

---

## 15. Cross-doc dependencies

| Doc | What it must agree with |
|---|---|
| `tech.md` | The **CHR set table v2** and stage-local ids (§2.1); **10 tileset banks** + the 2 empty slots and the section switch (§2.2); **14-16 CHR banks**, **3 sprite bank pairs**, **5 music banks** (numbers to assign); the X-GPOBJ sub-id → sprite-bank table (§10.4); the **VBlank stream path** at 128-256 B/frame, one stream at a time (§2.6); a raster-list entry for the pattern-table split (§2.8) and for the MODE-7 road (§6); whether `$C000-$DFFF` stays switchable (DPCM, D12); WRAM for D5's second channel block; the driver work D1-D11 (§12.2); the ExGrafix spike (§2.7); the 32 KB CHR-RAM question (§18) |
| `systems.md` | **Form swap**: 109-114 of 128 tiles differ per form, so the swap streams the full 2 KB sheet (16 frames at 128 B, 8 at 256 B), not ≤ 64 tiles (§1.5); WEAK!/CRIT!/?! cost 3 + 4 tiles thanks to READY (§2.4); 21 chip icons and 8 PART icons (§9.5); the alt-fire tiles live in each weapon's 15-tile slot (§2.4); Break Man's sheet is Should (§7.1); the SFX list (§12.6); Break Man's whistle G27 |
| `venues_a.md`, `venues_b.md` | The enemy-area maps and conflicts of §4 (e.g. Tomahawk's cowboys stay out of the town; Flame's chandeliers on 0B live in SET-FL1; Wind 01 has no vanilla enemy; Yamato's samurai screens get nothing new); the per-venue tile and frame counts (§4.9); the set-piece cues and their tiers (§12.4: one Should cue per venue, the rest Could); the vanilla stage themes kept; **while hanging on a vine (Plant) or carried by the condor (Blizzard) only the buster fires**, because those poses share the buster's 15-tile weapon slot (§2.4) |
| `fortress.md` | The art of §5 and the BG-boss techniques of §6 (YD on the X Crusher / Wily Machine code, Gamma on Mechazaurus, Cossack Catcher on Metonger Z, Dark Man on the RM framework with Break Man's tiles, the MODE-7 Machine on Wily Machine 6 + CX streaming); the H-wing palette eras; the music of §12.3 for H, W, the ending and the victory lap |
| `meta.md` | Title (vanilla logo + GP badge + new subtitle, menu under the split), file cards, bracket art, the judges' desk with the Mr. Y cut-out, the pit stop, the lobby from the Opening set, the museum sound test (D9's channel meters), the **GP fanfare** (G01) for the title and rating screens, MMC5 AUDIO in CONFIG |
| `story.md` | 12 portraits and 6 face icons (§9.4); in-stage pop-ups have **no full portrait** and may be **deferred** when a screen has fewer than 24 free BG ids (§9.6); Kalinka's folk-song sting (G06); Mr. Y is Mr. X's sprite with a moustache (§7.3) |

---

## 16. Lessons applied

- **CX 1 (one premise)**: the GP shows up in the art and audio itself: the stadium march, the judges' desk, the medal
  stamp, the bracket lines, the crowd SFX, Kalinka's own folk song.
- **CX 2 (a guest is a mechanic)**: §8's guests are drawn so that the rule reads at a glance (tetromino BG, brick
  shells, bunkers, Met-ghosts); E3's tempo follows the formation (D10).
- **CX 3 / CX lesson "big things in the background"**: every boss bigger than 32x32 is nametable art (§6); the MODE-7
  Machine uses CX's giant-Light CHR streaming.
- **CX 5 (watch the per-line budget)**: §3.4's flicker budget and §10.5's simulator; repeated hazards are BG.
- **CX 6 (jokes can be graphical)**: Mr. Y is Mr. X with a moustache; Grand Pi-kun's head comes off to reveal a Met; the
  2600 canopy; the Game Boy tier; Dark Man's disguise is Break Man with the wrong scarf shade.
- **CX 7 (mind the junk)**: `artcheck.py` rejects overlapping sets and unreferenced CHR loads.
- **4MI 2 (spend new pixels on set pieces and bosses)**: stages keep their vanilla sets; the budget goes to thirds,
  bosses, UI.
- **4MI 3 / 4 (art is portable; never overwrite)**: vanilla CHR banks stay byte-identical (§10.5 check 6); gaps are a
  reserve; reuse is by recolour and copy, not import (BRIEF §7.4).
- **4MI 5 (BG boss + sprite parts)** and **4MI 6 (status labels)**: §6, §9.7.
- **4MI 7 (per-message canvas)**: the glyph allocator (§9.6).
- **4MI 8 (palette tricks double the content)**: §3.2's list, the H-wing eras, Metal Metslime, Shadow Rock.
- **4MI engine (MMC5)**: the hardware multiplier in the driver (D6) and the charge sound on MMC5 pulse 1 (D7).
- **RM6 lesson 2 (the block table is the binding budget)**: §2.2's slot plan and section switch.
- **RM6 lesson 5 (per-screen sprite CHR conflicts)**: measured (§1.4) and enforced (§10.5); every venue set placed.
- **RM6 lesson 8 (keep quirks)**: C.FLRSH stays on the YOU GET card; TO BE CONTINUED keeps its music; the hidden debug
  sound player gets a museum door (`meta.md`).

---

## 17. Risks

1. **No pixel artist.** The Must art is ≈ 660 human hours. Without a human, Claude's drafts ship as final: the venues
   survive (they are mostly re-arranged vanilla art plus geometric thirds), but Bass β, the BG bosses and the portraits
   would look amateur. Mitigation: placeholder-first (§11.1), composite drafts from vanilla parts, and cutting the
   Should bosses (Mecha Dragon, Cossack Catcher) before the Must ones.
2. **8 KB of CHR-RAM is the real limit.** In-stage pop-ups need free BG ids that a full venue screen may not have; the
   glyph allocator defers lines, which can make commentary feel late. Mitigation: venue designers leave a 24-id window
   on key screens (the boss rooms always have one); the free-id map shows the gaps at build time.
3. **Form-swap streaming is 2 KB, not ≤ 1 KB** (§1.5). At 128 B/frame the swap takes 16 frames (0.27 s), heavier than
   `systems.md` hoped. Mitigation: the 256 B/frame unrolled copy (8 frames), or the 32 KB CHR-RAM question (§18).
4. **Champion pinch sets** need each boss set rebuilt; Wind, Yamato and Knight have 0 free tiles. Some vanilla frames
   must go (the pinch beat must exist in each pattern for the stream).
5. **Sprite-set conflicts** in the venues are tight on Blizzard, Flame and Tomahawk (§4): a late layout change can break
   a screen. `artcheck.py` must run from the first venue build.
6. **MMC5 audio reach**: an NES-001 without the expansion-audio mod and some flash carts play no MMC5 sound. The 4-channel
   rule (§12.1) keeps every track complete; the MMC5 voices stay Could, as BRIEF §9 says.
7. **Driver cost**: the sound driver is already 18 % of the frame. Two more channels without the hardware multiplier
   (D6) would add lag. D5 never ships without D6.
8. **Quotation risk**: arranging RM1-5 themes for the Hall of Fame is consistent with fan-hack tradition (CX and 4MI
   did the same with RM2/RM4) but is still Capcom's music; every non-Capcom homage stays original, and the two quoted
   folk songs are public domain.
9. **ExGrafix with CHR-RAM** may not be emulated everywhere; it is a Could behind a spike (§2.7).
10. **Scale creep**: 6,793 tiles is more than 4MI's 5,266. The Must line (4,851) is the plan; Should and Could art is
    cut first, in the order: Could; Should bosses; W-HANGAR; T-BOOTHILL; AYACO BG.

---

## 18. Open questions

1. **32 KB CHR-RAM?** BRIEF §7.1 fixes 8 KB. With 32 KB and MMC5 CHR banking, form swaps, pinch sets and BG-boss poses
   become bank switches (0 frames), and in-stage portraits become possible. Can `tech.md` measure whether FCEUmm,
   Mesen and the target flash carts support MMC5 + CHR-RAM banking (NES 2.0 CHR-RAM size field) before the decision is
   final?
2. Does `tech.md` keep `$C000-$DFFF` switchable under MMC5 (needed for DPCM drums, D12), or is it fixed with the moved
   fixed banks (`$7E/$7F`)?
3. Will the project recruit a pixel artist and a composer, and for which tier? This doc's Must art assumes ≈ 660 human
   hours.
4. Do `story.md` and the venue docs accept **deferred** pop-ups when a screen lacks free BG ids, or must certain lines
   (the first weakness hit) always show? (Boss rooms always have room, so the weakness line is safe.)
5. Should the Hall of Fame wings use arrangements of RM1-5 themes (the plan) or originals "in the style of" each game
   (safer, more work)?
6. Is the vanilla stage-select theme `$0F` acceptable as the bracket theme for the whole game, or does `meta.md` want a
   new bracket theme (it would replace G05 in the Should list)?
7. Do the venue designers agree to the enemy-area placements of §4 (in particular: Tomahawk's cowboys out of the town,
   Flame's dungeon without Metalls, Blizzard's count bombs off the Toppy screens)?
8. Which emulator and hardware matrix decides "MMC5 audio works" for the MMC5 AUDIO option's default (ON on Famicom-style
   targets, OFF otherwise)?
