> **Superseded in depth by the full investigation (October 2026).** This file was the first, readme-level
> teardown. The definitive results, from playing, decoding and disassembling the hacks, are in
> [`docs/research/cx/SUMMARY.md`](research/cx/SUMMARY.md),
> [`docs/research/r4mi/SUMMARY.md`](research/r4mi/SUMMARY.md) and, for the base game,
> [`docs/research/rm6/SUMMARY.md`](research/rm6/SUMMARY.md), plus about 16,000 lines of topic docs beside them.
> Where this file disagrees with them (for example on what the buster's invincibility applies to in 4MI), they win.

# Deconstruction: Rockman CX and Rockman 4 Minus Infinity

This is a teardown of the two reference hacks, covering both their technical construction and their design, and what each
one teaches the Rockman 6 project. Every claim is tagged with where it comes from:

- **[measured]**: verified in this repo by patching the hacks and analysing the bytes (scripts in `tools/analysis/`).
- **[readme]**: stated in the authors' own documentation (Japanese and English readmes, docs, history).
- **[inferred]**: my reading of the evidence, which should be confirmed in an emulator/debugger before relying on it.

---

## 0. The inputs

| File | Size | Header | Notes |
|---|---|---|---|
| Rockman 2 - Dr. Wily no Nazo (J) | 256 KB PRG, CHR-RAM | iNES, mapper 1 (MMC1) | MD5 `055fb8dc626fb1fbadc0a193010a3e3f` |
| Rockman 4 - Aratanaru Yabou!! (J) | 512 KB PRG, CHR-RAM | NES 2.0, mapper 4 (MMC3/TGROM) | MD5 `75e1d0a0b90c1099be6a650d5cd6e205` |
| Rockman 6 - Shijou Saidai no Tatakai!! (J) | 512 KB PRG, CHR-RAM 8 KB | NES 2.0, mapper 4 (MMC3/TGROM) | MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`, CRC32 (no header) `2D664D99` |
| Rockman CX v1.1 | two IPS + `Rockman CX Patcher.exe` | | by 暇人自治区 (Himajin Jichiku), 2017 |
| Rockman 4 Minus Infinity v1.01 | PBTPS scripts + two IPS-format `.bin` + `R4MIPatch.exe` | | by Puresabe (Neo Borokuzu Koubou), 2016 |

**Boot status in this environment [measured]**

- Minus Infinity: `pbtps.py` (a Python re-implementation of its patch engine) reproduces both builds, and **both boot to
  the title screen** in FCEUmm: the "Neo Borokuzu Koubou" splash, then "ROCKMAN 4 Minus ∞ … VER 1.01 … MODIFIED BY
  PURESABE 2008–2016".
- Rockman CX: applying the IPS directly gives garbage interrupt vectors (NMI `$0000`, RESET `$00EC`). This is why the
  readme says *"DO NOT APPLY IPS DIRECTLY"*. Comparing against a pre-patched JP ROM solved the native patcher's
  preprocessing:
  - It keeps RM2's first 224 KB in place, **inserts 256 KB of zeros**, then appends RM2's last 32 KB (the 16 KB banks 14–15,
    including the MMC1 fixed bank), and only then applies the IPS.
  - `tools/analysis/cxpatch.py` does this and is **byte-identical** to the official output (MD5
    `a2542f53663706837f3a5c99bb071217`).
  - The EN build boots to "MEGA MAN CX … 2017 VER 1.1 … HIMAJIN JICHIKU" with NEW GAME / LOAD GAME, and LOAD GAME opens
    **three save slots** (DATA 1–3).

---

## 1. Rockman CX (Rockman 2 → MMC3)

### 1.1 Design

**Premise: an inverted series.** *"Dr. Wily: 'We lose because we fight 8 vs 1!'"* [readme]. Wily builds a production line
of mass-produced fake Rockmen, and **you play one of them**, attacking **Dr. Light**. Light's side fields eight robots:
four existing Light robots active around the world, three newly built ones, and Rock himself. The fortress is Dr. Light's,
with stages 1–6 and then the ending [readme/history]. The whole hack is a joke on the series formula, played completely
straight in its level design.

**Roster as a tour of game history.** The credits table [measured, decoded text at `0x24500` in the EN build] pairs each
boss with the company it parodies:

| Boss | Credited to | Reference |
|---|---|---|
| MEGAMAN | CAPCOM | the hero as a boss |
| YOSHINO MAN | HIMAJIN JICHIKU | the author's own robot |
| CHEAT MAN | (none) | cheat/hacking culture |
| AIR MAN | (none) | RM2's most infamous boss (the "Air Man ga Taosenai" meme) |
| FIRE MARIO | NINTENDO | *Super Mario Bros.* |
| KAMEN RIDER | ISHINOMORI PROD. | tokusatsu, and its many Famicom games |
| BOMBERMAN | HUDSON SOFT | *Bomberman* |
| WHISPY WOODS | HAL LABORATORY | *Kirby* |

The lesson: each guest is *reinterpreted as a Rockman boss*, with its stage built around the guest's home-game mechanics.
That is what makes the crossovers feel designed rather than pasted in.

**Verbs imported from later games** [readme]:

- **Dash** (X-series): down-diagonal + A, with a dust effect. It lets you pass low gaps, but the hitbox does not shrink.
- **Playable Quick Man**: no dash, but he can **wall-kick**, plus a faster wall-kick with Down held. That gives two
  traversal vocabularies across the same levels.
- **Heart tanks**: +4 max HP, four of them hidden across the eight stages.
- **Quick weapon change** with Select + Up/Down, following the menu order.

**RM2's Items 1–3, reimagined as tools** [readme]. All three are available from the start, and "Dr. Light" upgrades
(*or worsens*) them as the count of cleared stages rises:

- *Instant Floor*: spawns a platform under you (up to 3 on screen, timed).
- *Subtank*: refills HP and weapon energy, one unit per tick.
- *Ubercharge*: 1 s of invincibility per use, stackable to about 4 s. This is a *Team Fortress 2* reference.

**Economy and quality of life:** weapon-energy pickups heal HP while the buster or Ubercharge is equipped, so no pickup is
wasted [readme]. A battery save was added in beta4 [history]. Explosions were redrawn in the MM3+ style, a jump boost was
added for upward screen transitions, and an experimental "pseudo-inertia" was removed after beta1 [history].

**Difficulty philosophy:** *"If you try to clear it with only the buster, a terrible **bad time** awaits"* (an Undertale
joke). Use the items and E-tanks [readme]. Difficulty is high, but the toolset is generous.

**Production:** 5+ years. beta1 came out 2014-02, the Light stages were built in 2016-01, v1.0 in 2016-08 (with four
bug-fix re-releases in a week), and v1.1 in 2017-03 with an official English build [history].

### 1.2 Technical [measured unless tagged]

- **Mapper conversion, MMC1 → MMC3:** 256 KB → 512 KB, with battery PRG-RAM (header flags6 `0x42`).
  - Gains: 8 KB bank granularity, a scanline IRQ, and WRAM.
  - The code now writes all four MMC3 IRQ registers and `$A001` (WRAM enable). Vanilla RM2 has no IRQ hardware at all,
    so CX added raster capability from scratch.
- **Patch size:** the JP IPS is 21,139 records and 359,762 bytes; the EN IPS is 20,967 records and 356,598 bytes.
- **Layout strategy:**
  - **Expansion by insertion.** RM2's 8 KB banks `$00–$1B` stay where they were. Banks `$1C–$1F` (the last 32 KB,
    including the fixed bank) move to `$3C–$3F`, which keeps the reset/NMI code at the top of the address space.
    `$1C–$3B` start zeroed and are filled by the IPS.
  - In the kept banks, 7–72% of the bytes are untouched by the IPS, so code and data were edited where they were. The
    middle 256 KB is new content.
  - About 72 KB of runs that look free remain [banks.py]. CX doubled the cartridge but did not fill it.
  - Same idea as 4MI's `SimpleExp`: grow the ROM *below* the fixed bank, so almost no original pointers move.
- **Two languages = two full IPS files**, produced by one patcher. The patcher also accepts MM2 (U) (CRC32
  `0x0FCFC04D`) [readme], so it presumably converts a US ROM to the RM2 (J) base first [inferred]. The J base needs only
  the insertion step [measured].
- **Saves:** three battery-backed save slots (DATA 1–3) [measured: boot screens].
- **Text encoding:** main table `A = $01`, credits table `A = $31` [rel.py].
- **Patcher:** native MSVC C++ (PDB path `…\CXPatcher\Release\Rockman CX Patcher beta3.pdb`). It scans the folder
  for `*.nes` and writes `Rockman CX.nes` and `Mega Man CX.nes`.

### 1.3 What CX teaches

1. **A premise that inverts the formula** buys enormous goodwill and humor. Everything, down to the fortress owner,
   follows from one joke.
2. **Guests should play like their home games.** A crossover boss needs a mechanic, not just a sprite.
3. **Import verbs from the series' future** (dash, wall-kick, heart tanks, quick-swap). Players recognise them instantly.
4. **A second playable character** with a different traversal verb doubles replay value. Every gate then needs two
   solutions.
5. **Bigger-than-vanilla tools with high difficulty** works: the game is hard, but you are never under-equipped.

---

## 2. Rockman 4 Minus Infinity (Rockman 4 → 1 MB, MMC3 or MMC5)

### 2.1 Design

**Name and voice.** 4MI means "degrading Rockman 4 to a grade of −∞". The author jokes that it should mathematically be
"Negative Infinity" but it's too late to change [readme]. The tone is self-deprecating, generous, and full of
gamer-to-gamer winks.

**Systemic rebalance: the buster is deliberately bad** [doc/weapon.txt]:

- *Rock Buster MI* gives enemies long invincibility. Bosses get more than 2 seconds, so the buster is the worst damage
  source.
- The charged **Rail Buster** pierces and has a big hitbox, but deals only 2× damage, and **you can't fire again until it
  leaves the screen**.
- *"The trick to playing well is how little you use this weapon (especially charged)."*
- Every special weapon's behaviour is rewritten, and some gain **D-pad + B alternate fires**.
- Weapons do **fixed damage** to normal enemies (Drill 4, Skull 3, Ring/Pharaoh/Bright 2, Dive 1) [hint.txt].
- *"Against bosses, any non-buster weapon fights well, even off-weakness."*
- **Boss weaknesses are read from i-frames**, not from the health bar: *"watch the invincibility time after you hit"*
  [hint.txt].
- Result: the whole arsenal stays in play, which is the core Mega Man fantasy that vanilla undercuts.

**Rush Search from the start**: Rush always digs up an item (large HP, large WE, 1UP, or E-tank, 100% of the time). Dying
refills Rush Search, so the author openly describes "sacrificing Rockmen" to farm E-tanks, and endorses it: *"features so
convenient they feel like cheating, use them freely… this hack is rough, just push forward."* [hint/readme].
The Rush adaptors arrive after the 3rd and 6th clears, and are attacks, not mobility.

**Critical hits** ("pikoon!"): random, 8× vs. normal enemies and 3× vs. bosses. The rate is **4× higher near death**, a
comeback mechanic. The "STABLE" difficulty disables it for time attack [hint/config].

**Equipment (passives):** three from the start, and **six hidden** ones that are earned by doing *specific things under
specific conditions*. They are not lying around: *"don't hunt for them; after you find one by accident, it hints at the
others."* Effects are documented in a **help screen** (B on the weapon menu, Left/Right to page). The help text
deliberately mixes in useless descriptions that hide real secret functions [weapon.txt/hint.txt].

**Hidden rooms:** every Robot Master stage has one, always exactly one screen, holding 1UPs and E-tanks [hint.txt].

**Hero Score** (out of 100) [readme_e/hint]:

| Category | Points | Contents |
|---|---|---|
| MISSION | 60 | |
| FRIENDS | 5 × 3 | save-flag names include EDDY, BEAT, KARINKA |
| EQUIPMENT | 2 × 6 | |
| PLAY STYLE | 10 | no revisits 2, no Game Over 4, play time 4 |
| BONUS | 5 | "XXXXman" 1 (Toadman, per the flags), Escape 2, "XXXXXXman" 2 (Shadowman) |

The score is shown on a **RESULT** screen [measured strings: `RESULT MISSION FRIENDS EQUIPMENT PLAY STYLE BONUS`].

**Accessibility as a first-class feature** (CONFIGURATION) [config.txt]:

- Language: JP / EN.
- Difficulty preset: NORMAL / EASY / HARD / STABLE. MAIN difficulty changes *maps, enemy and boss patterns, and traps*.
- Damage multiplier ×0.5–×1.5, rounded up.
- Criticals on or off.
- Item drops: NONE / NORMAL (= RM4) / MORE (= MM2's normal rate).
- **FAIL-SAFE**: start with two items that protect you from pits and spikes.
- Energy Generator: refills weapons on death and as the fortress progresses.
- Max HP (default 28), starting lives (default 4 instead of 2), and an E-tank minimum.

**Post-game is a second game** [hint.txt]:

1. **Time Attack**, per stage, with lap times on scroll.
2. A mode unlocked by beating the game *with three friends*.
3. A harder version of 2, with a loophole.
4. A **custom gauntlet editor**: choose bosses 0–5, intervals, randomisation (none / full / all-but-last / per-block),
   equipment, tanks, refill on clear, E-refill at pause, crits, and an i-frame cap. It has presets and one save slot.
5. A sane bonus mode.
6. CONFIGURATION.
7. **EXTRA CONFIGURATION**: a save-state editor plus cheats (infinite lives, refill-at-pause, *carry "super-special
   weapons" into stages where they don't belong, "easily glitches, enjoy the glitches"*). The strings are in the ROM
   [measured]: `STAGE / CHECK POINT / CLEAR FLAG / WEAPONS / LIVES / E.TANK / EQUIPMENT / CHEAT REFILL / PROGRESS /
   VALUE / SAVE DATA … BROKEN`.
8. **RECORD**: total play time and stats.

There is also a final mode the author says *they can't clear*, and **3 achievements** (100 Hero Points, HARD with no
Game Over, beating the final mode).

**Fortress as set pieces** [limited.txt]:

- Forced Balloon segments until Rush arrives in Cossack 1.
- An auto-equipped weapon in Pharaoh's stage.
- A wall cannon that only a charge shot can hit.
- An event final battle where *someone's meddling disables your buster* and the first attempt is a scripted "impossible
  fight".
- Weapon pickups placed in Wily 1 *"give them to the enemies"*.

**Community craft:** a long special-thanks list credits *ideas* borrowed from other hacks [readme]:

- Knockback Y-speed from *2 Core*, and the i-frame policy from *NC*/*DEM*.
- A faster E-tank, and triangle silence removed from the heal sound effect (*4 Endless*).
- Opening the menu without changing weapon keeps your weapon, and doesn't drop you off ladders (*Forever*).
- A coloured death explosion and a weapon-get tint (*Cross*).
- Slopes (Rock5easily's RM3 slope patch, *Odyssey*), pseudo-parallax (*Forever*, *Odyssey*), and water currents
  ("many RM2 hacks").

The Mega Man hacking scene has a shared vocabulary, and 4MI is fluent in it.

### 2.2 Technical [measured unless tagged]

**Two builds from one patch pipeline**, both 1 MB PRG with CHR-RAM and battery:

| Build | flags6 | Status |
|---|---|---|
| MMC3 | `0x43` | **Out of spec**: MMC3 addresses only 512 KB, as Kuja Killer pointed out to the author [readme]. Laggy. |
| MMC5 | `0x53` | **Recommended** by the author: lag reduction, and the charge sound gets its own audio channel so it can't cut out the music [readme_e]. |

**The patch engine (PBTPS).** It is a tiny scripting language, re-implemented in `tools/analysis/pbtps.py`:

1. `PreProcess.pbtps` moves original data *inside the base ROM*. Semantics: `copy DST LEN SRC`, which was confirmed by
   the build booting.
   - Copies a walking/throwing sprite-pattern table.
   - Relocates the bottom rows of Bright Man's background so a **status gauge** fits.
   - `revbit` mirrors Skull Man's bone tiles.
   - **Swaps two 5-byte instruction sequences**, so the splash sound plays even when no splash object can spawn.
   - Performs a **3-way rotation of three stage data blocks** (`0x161C` bytes each) through a scratch area.
   - Copies Bright's background tiles into the space that frees up.
2. `SimpleExp.pbtps` expands the ROM: `insert` 512 KB of `00` at `0x80010`, copy the fixed bank `0x7C010 → 0xFC010`,
   and set header PRG = `0x40`.
3. `ips_o` applies the big IPS: 34,621 records / 595,968 bytes for MMC3, and 34,654 / 596,297 for MMC5.
4. Input and output hashes are verified (`hash_pre` / `hash_res`), using a custom 24-bit hash, not CRC32.

Why this design: an IPS can't express *moves*. Relocating Capcom's own bytes with script ops keeps the patch smaller and
avoids shipping original data. The readme also warns *never to make an IPS from the patched ROM* [readme].
**BPS does the same job natively** (SourceCopy), which is why this project will use BPS.

**Layout:**

- The original 64 banks are kept in place. Many are 90–100% byte-identical (assets reused), and some are 15–50%
  (heavily rewritten code and level data).
- The upper 64 banks (`$40–$7F`) are all new.
- Only about 38 KB of free-looking space remains in 1 MB. **They filled the cartridge.**

**MMC5 features in use** (absolute-addressed write sites found by `regs.py`; this method also picks up some false
positives from data bytes):

| Register | Use |
|---|---|
| `$5000` | extra pulse channel (the separate charge SFX) |
| `$5100` | PRG mode |
| `$5105` | nametable mapping (about 26 sites; dynamic nametable tricks) |
| `$5114` / `$5115` | PRG banks |
| `$5200` | **vertical split mode** (status bars, effects) |
| `$5203` / `$5204` | scanline IRQ and acknowledge |
| `$5205` / `$5206` | **hardware multiplier** (part of the lag reduction) |

The MMC5 build still contains MMC3-style writes [inferred: an abstraction layer or dead paths].

**Raster effects called out in the credits:**

- Water shimmer (Cossack 3).
- Pseudo-double-scroll parallax (Cossack 3 mid-boss and Cossack 4).
- Tall vertical structures where terrain checks depend on the screen's Y position.
- A Bright Man stage status bar.

**Optimisation:** Rock5easily's VBlank-transfer routine (from the RM4 scroll speed-up patch) and Matrixz's optimisations
from *Mega Man Forever* [readme].

**Other details:**

- **Saves:** one autosaving file, written on death or clear. START+A on NEW GAME wipes it [readme].
- **Extra input:** controller 2's A/B act as pseudo L/R to cycle weapons, and both together returns to the buster
  [weapon.txt].
- **Emulator matrix** [readme]: works on Nestopia and FCEUX (old PPU). VirtuaNES runs only the MMC3 build. NNNesterJ and
  G-NES are partial: some visual effects are lost and Bright Man's stage is unplayable. Heavy emulator dependence was the
  cost of mid-frame tricks.
- **Development:** 2008–2016, eight years [measured: title screen].

### 2.3 What 4MI teaches

1. **Change one number and the whole game re-centres.** Giving the buster enemy i-frames turns every special weapon into a
   main weapon. Find RM6's equivalent lever.
2. **Accessibility and difficulty are the same feature.** Fine-grained configuration lets the hack be brutal *and*
   finishable.
3. **Secrets that are earned by behaviour**, not by searching, create stories ("how did you get that?").
4. **Meta-score and post-game modes** multiply the hack's lifespan.
5. **Pick an accurate target early.** 4MI's biggest regret is its emulator dependency. Target Mesen and hardware from day
   one, and run automated regression tests.
6. **Credit your borrowings.** It is good citizenship and good publicity.

---

## 3. Side by side

| | Rockman CX | Rockman 4 Minus Infinity |
|---|---|---|
| Base / mapper | RM2, MMC1 → MMC3 | RM4, MMC3 → MMC3 (OOS) or MMC5 |
| Size | 256 → 512 KB, ~72 KB left | 512 KB → 1 MB, ~38 KB left |
| Core hook | Inverted premise plus crossover roster | Systemic rebalance plus deep meta-game |
| New verbs | Dash, wall-kick (Quick Man), quick-swap | Alt-fires, Rush Search, crits, pseudo L/R |
| Progression | Heart tanks, upgrading items | Hidden equipment, Hero Score, adaptors after clears 3 and 6 |
| Content | 8 new bosses, opening stage, 6 Light stages | 8 reworked stages and bosses, 8 fortress stages, many special modes |
| Accessibility | Generous tools | Full configuration, difficulty presets, fail-safes |
| Persistence | Battery save, 3 slots | 1 autosave slot, records, achievements |
| Language | JP plus EN build | JP/EN switch in config |
| Patching | Zero-insertion expansion, then IPS (× 2 languages) | Script ops (moves), then expansion, then IPS, then hash check |
| Timeline | ~5 years | ~8 years |

**The common skeleton** of a "reinvented" Mega Man hack:

1. A premise with a twist.
2. A combat economy rebalanced to make the arsenal matter.
3. Verbs borrowed from the series' future.
4. Secrets and meta-progression.
5. Configuration that respects every kind of player.
6. A doubled cartridge.
7. A fortress staged as set pieces.
8. Humor and references throughout.

`docs/PLAN.md` applies this skeleton to Rockman 6.
