# Rockman 6 GP: design brief (binding decisions for all design docs)

This brief fixes the decisions that every design doc in `docs/design/` must follow, so that parallel work stays
coherent. It supersedes `docs/PLAN.md` wherever they disagree, and the research supersedes both on facts.

Read first:

- `docs/research/rm6/SUMMARY.md`: vanilla RM6. **§4 audits the old PLAN and lists its contradictions.**
- `docs/research/cx/SUMMARY.md`: Rockman CX.
- `docs/research/r4mi/SUMMARY.md`: Rockman 4 Minus Infinity.
- The topic docs those summaries link to (detail, addresses, images).
- Full stage maps of vanilla RM6, rendered from ROM: `docs/research/rm6/img/maps/*.png`.

---

## 1. Identity

**Rockman 6 GP: Shijō Saidai no Saikai!!** (史上最大の再会, "The Greatest Reunion in History"; codename `r6gp`)

**One premise, followed through every layer** (CX lesson 1): *the World Robot Tournament is real this time*.

- Every stage is a **match**.
- Every clear is **judged**.
- The stage select is a **bracket**.
- Deaths, secrets and weaknesses get **live commentary**.
- Money is **prize money**.
- There is a **rival entrant**.
- The finale is the **championship**.

The second layer is **game history**:

- The venues are tributes to eras and genres of games.
- The fortress is a **museum of Rockman 1-5**.
- The final castle is the villain's "**16-bit upgrade**" (Project SUPER), the farewell of the last NES Rockman.

Running gag: the sponsor **"Mr. Y"** is obviously Dr. Wily. Everyone says so, constantly.

## 2. Cast (fixed)

| Who | Role |
|---|---|
| Rockman | Player. Normal / Power / Jet forms, later the Super Adaptor |
| **Break Man** (= Blues; MM3's alias) | The masked **10th entrant**. He helps at key beats (the 4MI Proto Man pattern), then becomes a **tag partner** (the CX Quick Man pattern; see §5.6) |
| **Bass β** (Forte β) | Mr. Y's entrant and the rival. Duel 1 in the Semifinal, duel 2 in Super Wily Castle. A playable Bass Mode is a *Could* |
| Dr. Cossack and Kalinka | **Commentators** (announcer pop-ups) |
| Eddie | Runs the pit-stop **shop** |
| Beat | Plate collectible; rescue helper; chip slots |
| Dr. Light | Entrant's sponsor. Vanilla RM6 has **no Light lines**, so all of his are new |
| Roll | Pit crew; optional cameo |
| The 8 champions | Blizzard, Centaur, Flame, Knight, Plant, Tomahawk, Wind, Yamato: good-natured rivals rebuilt by their fan designers (the vanilla credit cards DWNB-41..48 name them) |

## 3. Structure (target; tiers in §9)

**Opening Ceremony** → **8 Heritage Venues** (any order) → **Semifinal Riot** (after the 4th win) → **Hall of Fame** H1-H5
(MM1-MM5 tribute wings) → **Super Wily Castle** W1-W3 → championship ending → **playable victory lap credits**
(CX's playable staff roll).

The **4 Exhibition Matches** E1-E4 are optional bonus stages, unlocked by pairs of venue secret exits.

That makes 22 stages against vanilla's 16 stage ids. See §7.2 for how the id space grows.

## 4. Corrections the designs must respect (from `rm6/SUMMARY.md` §4)

| Old PLAN said | Reality, and the decision |
|---|---|
| "Menu fixes" | Already vanilla. Drop them |
| "Upward-scroll jump boost" | Vanilla can't enter a screen from below without a ladder. A *new exit condition* is needed: a Could, design it only if a venue needs it |
| Jet "heat gauge replaces energy drain" | The Jet already has a regenerating 19-unit stamina bar (`$9C`). Keep it; tune it. The "heat" idea becomes an *overheat stall* only if it adds play |
| Adaptors by win count | Vanilla gives them by boss (Plant → Jet, Flame → Power), derived from progress bits (`$38:$931D`, `$3B:$BA3F`). **Decision: by win count** (Power after the 2nd win, Jet after the 4th; 4MI precedent), stored as a real save flag |
| Forms with weapons | **Vanilla forms cannot fire weapons.** Form × weapon synergies are all new code; budget them as such |
| Damage "at least 2" | Superseded by the combat model in §5.1 |
| Every venue has a secret exit | Only 4 vanilla stages branch (plates B/E/A/T), with no flag bits for stages 0-3. **Decision: all 8 venues get a secret exit**, with new flags in save RAM. The branches are level data (screens `$18-$1F`) |
| Homage set pieces on vanilla tilesets | Blocks and tiles are nearly exhausted (Plant: 0 free tile ids). **Decision: every venue gets its own new tileset slot** (vanilla CHR kept and extended). Set pieces are sprite objects or BG-boss art |
| ASCII level format | Up to 256 block ids, so **2 hex digits per block** |
| Autoscroll | Doesn't exist in vanilla. It is a new engine feature (T1) |
| 22 stage ids | Breaks the 45 `$51` readers. See §7.2 |

## 5. Systems decisions

### 5.1 Combat model: "the judges like variety"

- **Two tables, as in 4MI (credit it):**
  - **damage per boss × weapon**: 1-4, with special cases in visible code, not table fall-through (CX lesson 7);
  - **post-hit invincibility per boss × weapon**. A weakness gives short i-frames and a unique reaction; most weapons are mid; the buster is long (≈ 60 frames, gentler than 4MI's 127).
- The flash length must be readable on screen.
- **Normal enemies:** keep vanilla's low-nibble fixed damage, plus per-class thematic one-shots (vanilla already has these: F.BLAST kills snow robots).
- **The RM6 signature: forms can fire weapons.** Each of the 8 weapons gets:
  - a tap behaviour;
  - one alternate (UP+B or hold);
  - **one form synergy** (Power or Jet).

  That makes 8 synergies, not 24.
- **Weakness feedback:** a "WEAK!" pop, a boss stagger, and a commentator line on the first weakness hit.

### 5.2 Movement and controls

- **SELECT is free** (verified). Hold SELECT plus:
  - Up/Down: weapon cycle;
  - Left/Right: form cycle.
- Tapping SELECT toggles to the last weapon. Optional: controller-2 pseudo L/R.
- A quick form swap must stream the form's sprite CHR without the vanilla transform cutscene. Budget a short flash.
- **Super Adaptor** (H3): rocket fist with homing return, plus a short jet hop. No gauge.

### 5.3 Economy: scorecard → bolts → Eddie → chips

- **Scorecard per stage**, out of 100: TIME 20, DAMAGE 20, VARIETY 25, SECRETS 20, STYLE 15. Medals at 40 / 60 / 80 / 95. Bolts = score + medal bonus. Replays pay only the improvement.
- **Chips** are passive equipment, stored as bits, each with a help page (4MI: some pages cryptic on purpose).
  - Slots: 2, +1 per Beat plate, max 6.
  - Some chips are **earned by behaviour**, not bought (4MI lesson 3). Include at least one moral trade-off recipe.

### 5.4 Secrets and hints

- **Per venue:**
  - one secret exit;
  - one one-screen hidden room;
  - one behaviour-gated item or chip;
  - plates in 4 venues (the vanilla 4, or re-homed).
- **The judges' debrief = 4MI's predicate table.** After each stage, the first missed secret in that venue gets a one-line hint. Write real hints; never ship WIP text.
- **Telegraph required tools** (CX lesson 6): every gate needs a visible tell.

### 5.5 Voice on failure (CX lesson 3)

- The commentators react to **deaths** with a rotating table per venue, plus generic lines.
- In the fortress, Mr. Y heckles between lives.
- Lines are short (≤ 2 lines in the pop-up window) and **toggleable**.

### 5.6 The tag partner (Break Man)

- He joins after a story beat (designers choose the point; mid-game).
- From then on, **pause menu → call** once per life, as a separate body with its own HP (CX Quick Man).
- **Moveset:**
  - shield blocks shots while jumping;
  - Break charge shot;
  - double knockback;
  - no forms;
  - uses the buster only, or a limited weapon set (designer's choice, justified).
- Levels: every tag-only shortcut is optional.

### 5.7 Difficulty and configuration (4MI lesson: accessibility = difficulty)

Presets: CASUAL / NORMAL / HARD / 1993 (vanilla rules). HARD = per-section byte-poke lists plus AI branches (the 4MI
model).

Overrides:

- damage multiplier;
- lives;
- E-tank floor;
- drops;
- criticals on/off (if criticals ship);
- announcer on/off;
- reduced flashes;
- MMC5 audio on/off;
- language: **JAPANESE / ENGLISH / ENGRISH**, the last a joke tribute to 4MI that swaps in deliberately broken-English strings for a handful of menus.

## 6. Content rules

- **A guest or homage must be a mechanic**, not just a sprite (CX lesson 2). Use parody names; never trademark logos.
- **Make each stage's theme into mechanics** (4MI lesson 7): curses, heat, compactor, quick-draw, RPG encounter, and so on.
- **Reuse engine set pieces with one twist each** (CX lesson 5).
  - Vanilla tech to reuse: rocking-ship split, igniting oil, slippery ice, falling ceiling, tide, parallax, updraft/fans, Wily 3's data-driven rush, BG bosses.
  - BG-boss re-skin fits for H1-H5 are in `rm6/SUMMARY.md` §4 (Section 3, CONFIRMED).
- **Keep vanilla quirks deliberately** (rm6 lesson 8): igniting oil, slippery ice, Wily 2's twin plugs, the Jet sky bypass, C.FLRSH, TO BE CONTINUED.
- **Lag budget:** about 10 live objects per screen (vanilla profile). Set pieces must respect it.

## 7. Technical decisions

### 7.1 Platform

MMC5, 1 MB PRG (expansion by insertion; fixed banks moved to `$7E/$7F`), 8 KB CHR-RAM, and battery PRG-RAM.

- **Size the PRG-RAM:** at least 8 KB save; consider 16-32 KB of work RAM for WRAM-resident stage sections (the 4MI model).
- Use the **corrected porting checklist** in `rm6/SUMMARY.md` §3, including the two `LDA #$3E / JSR $CB91` sites, the sound reader's own bank switch, and the 19 IRQ-chain sites.
- The vanilla IRQ chains move into a **generic double-buffered raster list** (4MI lesson 11). Keep the three logic-in-IRQ handlers working.

### 7.2 Stage id space

Grow to 32 ids. Replace the 45 `$51` readers' assumptions (5 `AND #$08`, 3 `CPY #$08`, 14 `CMP #n`, the 8-entry tables) with a **stage-attribute table**: class, plate slot, music, collision group, layout bank, tileset, and so on.

- Relocate the packed stage, object-list and collision-group tables to new banks.
- Evaluate **WRAM-resident layout sections** (the 4MI model). They make map-editing bosses, link-table hidden rooms and HARD poke lists cheap.

### 7.3 Dev tooling from day one

- A level select and RAM editor, built in (the 4MI EXTRA CONFIG pattern). It doubles as the regression entry point.
- Warps and a hook registry.
- Golden-movie tests (shadow6 tracer).
- `levels.py` round trip.

### 7.4 Assets

- **Never overwrite Capcom art in place** (4MI). Add tiles in new banks and slots.
- **No byte-for-byte imports from other Rockman ROMs in v1**, because the patch would carry their data. A later multi-ROM patcher may source optional imports from the user's own ROMs (*Could*).

### 7.5 Text and sound

- **Text:** the vanilla engine is 168 PPU scripts with no control codes, so dialogue needs a **new** text engine: window, typewriter, portraits, choices, JP/EN.
- **Sound:** the vanilla driver is kept (commands decoded); add new songs and SFX; MMC5 pulses for "16-bit" colour.

## 8. Deliverable conventions for design docs

- **Files:** write to `docs/design/<topic>.md`. Never name a file with "summary" or "report"; the harness blocks those. If a write is refused, return the full text instead.
- **Be concrete enough to implement:**
  - screen-by-screen outlines for stages, referencing the vanilla map screens;
  - pattern lists with frame timings for bosses;
  - numbers for systems;
  - addresses and table names for engine work.
- **Mark each item:**
  - **[engine-ok]**: vanilla supports it as-is or with data only;
  - **[new-code]**;
  - **[new-art]**;
  - **[new-music]**;
  - a size estimate: S / M / L;
  - a tier: Must / Should / Could.
- **End with:**
  - "Lessons applied" (which CX/4MI/RM6 lessons the doc uses);
  - "Risks";
  - "Open questions".
- **Humour:** be funny where the brief says to be. The bar is CX's and 4MI's "how crazy it gets" lists: every venue and boss should have at least one moment worth a screenshot.

## 9. Scope tiers (initial; designers may argue changes in "Risks")

| Tier | Contents |
|---|---|
| **Must** | Systems §5.1-5.3; 8 venues with secret exits; Opening; Semifinal; H1, H3, H5; W2 + W3; ending; saves and config; JP + EN; dev tooling |
| **Should** | H2, H4; W1 Upgrade Lab; Exhibitions E1-E4; the tag partner; Time Attack; GP Rush; victory-lap credits |
| **Could** | Bass Mode; MMC5 audio arrangements; Exhibition Rules; Museum; ENGRISH; "Mr. X Returns" |
| **Won't (v1)** | Slopes; cross-ROM asset imports |
