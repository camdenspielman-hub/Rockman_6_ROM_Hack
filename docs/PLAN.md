# ROCKMAN 6 GP — Design & Build Plan

> **ロックマン6 GP 史上最大のグランプリ!!** / *Mega Man 6 GP: The Greatest Grand Prix in History*
> Codename **`r6gp`**. The title is a working title; alternatives are listed in §9.

This document has everything needed to start building without further research. Sections §1–§4 are the **game
design**. Sections §5–§7 are the **technical architecture**, starting from facts already measured in the ROM.
Section §8 is the **milestone plan**, broken into session-sized tasks. `docs/STATUS.md` is the running hand-off log:
update it at the end of every work session.

---

## 1. Vision

The two reference hacks share a skeleton (see `docs/DECONSTRUCTION.md` §3): a premise with a twist, an arsenal-centred
combat economy, verbs from the series' future, earned secrets and a meta-score, deep configuration, a doubled cartridge,
a fortress built as set pieces, and humor throughout. R6GP uses that skeleton but builds every bone from **what makes
Rockman 6 unique**:

| What RM6 uniquely has | How R6GP amplifies it |
|---|---|
| A **World Robot Tournament** premise | A real tournament structure: each stage is a *match*, scored by judges, with prize money, a bracket, and a rival entrant |
| Its subtitle, *"The Greatest Battle in **History**"* | Every venue is a tribute to an era or genre of **game history**, and the fortress is a museum of **Rockman history** (1–5) |
| Bosses **designed by fans** in a worldwide contest | Keep the fan-made eight as the "returning champions", fully reworked like 4MI reworked RM4's bosses |
| **Rush Power / Rush Jet** fusion adaptors | Adaptors become a full second axis of play: rebalanced, quick-swappable, with weapon synergies, and a late **Super Adaptor** (the MM7 successor) |
| **Branching stages** with second exits, and **Beat** plates | Every venue gets a secret exit (in the spirit of Super Mario World) that opens bonus **Exhibition** stages. Beat plates expand your chip slots |
| The **last** NES Rockman (1993) | The story is the farewell to 8-bit: the villain's scheme is a "16-bit upgrade", and the final castle literally gains colors, audio channels and Mode 7-style tricks |

The **"one number that re-centres the game"** (4MI's lesson) is the **Tournament Scorecard**. Each stage is judged on
time, damage taken, **weapon variety**, secrets and style. The judges pay out **bolts**, and bolts buy **chips**
(passives) at Eddie's shop. Using your whole arsenal is literally how you earn money. Unlike 4MI's "bad buster", it is a
carrot, not a stick: buster-only runs stay possible, they just earn less.

### Story

> 20XX. A year after the 1st World Robot Tournament ended with "Mr. X" unmasked as Dr. Wily, the Tournament Committee
> wants to restore the event's honor. It announces the **Grand Prix**: eight venues around the world, each built as a
> tribute to a legendary era of games. The returning champions defend them, rebuilt by their original fan designers.
> Dr. Light enters Rockman. The color commentators are **Dr. Cossack and Kalinka**. **Eddie** runs the pit-stop shop.
>
> At the last minute a ninth entrant registers, sponsored by **"Mr. Y"** (*Light: "…It's Wily." Rock: "It's definitely
> Wily."*). Mr. Y's entrant is **Bass β** (Forte β), a prototype built from Rockman's own tournament data. Mr. Y's real
> pitch is **"Project SUPER"**: upgrade every robot on Earth to 16-bit, by force. After the eight venues, the champions'
> trophies are stolen and taken to the **Hall of Fame**, a museum of Rockman's past battles. Beyond it rises **Super
> Wily Castle**, where the screen itself starts upgrading.
>
> Ending: Project SUPER collapses. Bass escapes, vowing *"next time, it won't be 8-bit"* (a nod to MM7). Rock and Light
> watch the stadium lights go out, one channel at a time. Credits roll as the **Grand Prix results bracket** listing
> every entrant (every enemy, in the classic Capcom style), followed by your stats.

The tone is CX-level silliness in the cutscenes and announcer lines, and 4MI-level sincerity in the design.

---

## 2. Core systems (player-facing spec)

The numbers are **starting tuning targets**; balance happens in M10. "Vanilla" means unmodified Rockman 6.

### 2.1 Controls & quality of life

| Feature | Spec | Precedent |
|---|---|---|
| Weapon quick-swap | **Select held** + Up/Down cycles weapons in menu order. While Select is held the D-pad does not move Rock. | CX |
| Adaptor quick-swap | Select held + Left/Right cycles Normal → Power → Jet (→ Super) | new |
| Last-weapon toggle | Tapping Select alone (press and release with no D-pad) swaps to the previous weapon | new |
| Pseudo L/R | Optional: controller 2's A/B cycle weapons, both at once returns to the buster (config) | 4MI |
| Menu fixes | Opening the menu without changing weapon keeps your charge/weapon state, and you don't fall off ladders | 4MI (*Forever*) |
| Heal speed | E-tank refills 2× faster, and heal SFX loses its triangle-silencing | 4MI (*4 Endless*) |
| Efficient pickups | Weapon energy pickups heal HP when the buster (or a full weapon) is equipped | CX |
| Upward scroll | Jump boost when entering a screen from below | CX |
| Feedback | Colored death explosion, a weapon-get tint, and a "WEAK!" pop when you hit a boss's weakness | 4MI (*Cross*) |
| Saves | **3 battery-backed slots**, autosaving on stage clear, death and shop purchases. Passwords are removed. | CX (3 slots) |
| Lag | Profile, then optimise object loops and VBlank transfers, and use the MMC5 multiplier for any multiply | 4MI |

### 2.2 Adaptor overhaul

Vanilla RM6 already has Power and Jet. R6GP makes them **quick-swappable** and gives each a clear identity:

- **Normal Rock**: slide, charge shot, full weapon access.
- **Power Rock**:
  - The charged punch breaks cracked blocks (vanilla).
  - **New: the punch *parries*.** A punch that connects with a small projectile reflects it, and you get brief
    invincibility on a well-timed parry (an SF3 parry nod).
  - **New: charged punch lunge.** You move forward about 2 tiles while it's active.
  - No slide (vanilla).
- **Jet Rock**:
  - Hover/flight (vanilla).
  - **New: a heat gauge replaces energy drain.** It drains in flight, recharges on the ground, and overheats into a
    ~1 s stall.
  - **New: air-dash.** Double-tap a direction.
  - No charge (vanilla).
- **Super Rock** (found in Hall of Fame wing 3 as the "prototype of Dr. Light's next design", an MM7 Super Adaptor nod):
  a rocket fist (homing return) plus a short jet hop. It is weaker than each specialist form, but has no gauge.
- **Acquisition:**
  - Power after your **2nd** venue win, Jet after the **4th** (counted, not boss-specific). This guarantees sequence
    freedom (4MI's adaptors-after-3-and-6 rule).
  - Venue *secret exits* may need an adaptor, but *normal* exits never do.

### 2.3 Weapons

Each of the eight boss weapons gets:

- **Tap**: a reworked primary.
- **Up+B**: an alternate fire, as in 4MI.
- **One adaptor synergy**: a unique behaviour while in Power or Jet form.

The full list is in the venue table (§3.2).

**Weapon design rules:**

1. Every weapon must be *the best tool somewhere* (a traversal use, a crowd use, or a boss).
2. Weapons deal **fixed damage to normal enemies** (as in 4MI), so the "tough enemy" tier means "bring the right tool".
3. Bosses use per-weapon damage tables as in vanilla, but **every non-buster weapon does at least 2** (4MI: "any special
   weapon fights decently").
4. Weaknesses trigger a stagger animation and the "WEAK!" pop.

Two extra weapons, outside the eight:

- **Magnet Beam** (Hall of Fame wing 1). It builds temporary platforms as you hold B, like MM1's Magnet Beam, and is also
  a tribute to CX's *Instant Floor*.
- **Bass Buster** (Bass Mode only).

### 2.4 The Tournament Scorecard (the core loop)

After every stage clear, a **judges' scorecard** slides in, with a split-screen IRQ panel and three judge portraits:

| Category | Max | Rule (initial) |
|---|---|---|
| TIME | 20 | full points at or under par, minus 1 per 10 s over |
| DAMAGE | 20 | minus 2 per hit taken, and −10 per death |
| VARIETY | 25 | 5 per *distinct* weapon/adaptor that scores a kill (buster counts once) |
| SECRETS | 20 | hidden room 5, secret exit 10, Beat plate 5 |
| STYLE | 15 | boss beaten with its weakness 5, parries 1 each (up to 5), no E-tank 5 |

Medals: **Bronze ≥ 40, Silver ≥ 60, Gold ≥ 80, Platinum ≥ 95**. Bolts paid = score + medal bonus (0 / 20 / 40 / 70 /
100). Replaying a cleared venue pays only the **improvement** over your best score, which prevents grinding. The best
medal per stage is saved, and the medal total is **Hall of Fame Points**, which unlock post-game content (§4.4).

**Announcer pop-ups** (Cossack/Kalinka, 1–2 lines on a small IRQ window at the bottom of the screen) react to events:
first parry, a weakness hit, a no-damage boss, a secret found. They are toggleable in config.

### 2.5 Shop & chips

**Eddie's Pit Stop** is reachable from stage select.

- **Consumables:**
  - E-tank 40 (hold up to 4)
  - W-tank 50 (hold up to 2)
  - 1UP 30
  - "Beat Call" 30 (one rescue from a pit; held up to 3)
- **Chips:** passive equipment, each bought or found once. **Chip slots** start at 2. Each **Beat plate** adds one
  (B-E-A-T gives 4, so the max is 6). Equip chips at the shop or on the pause screen. Each chip has a help page, and
  some help pages are **deliberately cryptic and hide secret functions**, as in 4MI.

| Chip | Effect | Source |
|---|---|---|
| Shock Absorber | No knockback | shop 120 |
| Spike Guard | Survive one spike touch per life | shop 150 (free in CASUAL) |
| Pit Guard | Auto Beat Call once per life | shop 150 (free in CASUAL) |
| Energy Balancer | Weapon pickups refill your lowest weapon | vanilla secret path, kept |
| Half Energy | Weapons cost half | shop 250 |
| Charge Kit | Charge time −40% | shop 120 |
| Bolt Magnet | Pickups drift toward you | shop 80 |
| Auto Recover | Slow HP regen while standing still | found (Plant venue underground) |
| Critical Chip | 1/16 chance of 2× damage with a "pikoon!" sound, and a higher rate at low HP | found (tribute to 4MI) |
| Judge's Favor | +25% bolts | shop 200 |
| Line Clear / Multiball / Barrier / Power Pellet | Exhibition rewards (§3.3) | Exhibitions |

Shop stock unlocks in tiers after 0, 3 and 6 venue wins, so the economy can't be front-loaded.

### 2.6 Secrets

Each of the **8 venues** has:

- one **normal exit** (boss → weapon)
- one **secret exit** (an alternate route → a secret boss door, or a hidden "back way")
- one **hidden room** (exactly one screen, holding consumables or bolts; a 4MI convention)

Four of the venues also hold a **Beat plate**.

Secret exits are tied to **homage trivia** (see the venue table). Players who know the referenced game will smile, and
the help text and the announcers drop hints. Two secret exits unlock one Exhibition stage.

### 2.7 Configuration (title screen → CONFIG)

| Option | Values |
|---|---|
| Language | JAPANESE / ENGLISH |
| Difficulty preset | **CASUAL** (damage ×0.5, extra checkpoints, Spike and Pit Guard granted free) / **NORMAL** / **HARD** (damage ×1.5, HARD layouts and patterns where authored, shop prices ×1.5) / **1993** (vanilla-faithful rules: no chips, no shop, no scorecard bonuses, classic lives) |
| Individual overrides (shows "EDIT") | Damage ×0.5 / ×1 / ×1.5 / ×2; Start lives 2–9; E-tank floor 0–4; Item drops LESS / NORMAL / MORE; Criticals ON / OFF |
| Controls | Select-modifier ON / OFF; Pseudo L/R (2P) ON / OFF |
| Display | Announcer ON / OFF; Screen flashes NORMAL / REDUCED (accessibility: tones down full-screen flashes like Centaur Flash) |
| Audio | MMC5 extra channels ON / OFF (for consoles without expansion audio) |

### 2.8 Second playable: **Bass β**

Unlocked after the first clear (with a "New Game+ as Bass" option), and also used in the post-game modes. This is the
MM&B Bass toolkit:

- dash (Down+A or double-tap)
- double jump
- 7-way rapid **Bass Buster** (can't move while firing on the ground)
- no charge, no slide, no adaptors

He uses the same eight weapons. **Level rule:** every adaptor gate must have a Bass solution (double jump, dash, or
"cracked blocks break to Bass Buster in Bass Mode"). The test harness verifies each one with a scripted route. Bass needs
his own player sprite set, so he is a *Could* item (§8.3).

---

## 3. Content

### 3.1 Stage list (22 stages)

| # | Stage | Replaces vanilla slot | Boss |
|---|---|---|---|
| 0 | **Opening Ceremony** (stadium intro and tutorial) | new | "Grand Pi-kun", the GP mascot gone rogue (mid-boss scale) |
| 1–8 | **Heritage Venues** (§3.2) | the 8 Robot Master stages, rebuilt | the 8 champions, reworked |
| E1–E4 | **Exhibition Matches** (§3.3) | new, short (~6 screens) | guest "arcade legend" robots |
| M | **Semifinal Riot** (after the 4th win) | new | Bass β (first duel) |
| H1–H5 | **Hall of Fame** (§3.4) | the Mr. X fortress slots, plus one new slot | legacy bosses MK-VI |
| W1–W3 | **Super Wily Castle** (§3.5) | the Wily fortress slots | boss rush, Bass β, MODE-7 Machine, Wily Capsule |

For scale: CX has about 15 stages and 4MI about 16 plus modes. Vanilla's own fortress stage count is catalogued in M0.

### 3.2 The eight Heritage Venues

The design constraints are to **reuse each vanilla stage's tileset and palette** (the art-budget saver) and to add one
homage set piece per venue. "Tech" names new engine work, which is reused across venues where marked.

**Wind Man — "SKY ACE 1943"**

- **Homage:** Capcom's *1942/1943* (1984/1987)
- **Set piece and gimmicks:**
  - Opens with a **horizontal shmup segment**: Jet is forced and the heat gauge is off. Shooting a red formation drops
    **POW** for a timed 3-way buster.
  - A big-bomber mid-boss ("AYACO", a nod to 1943's battleship).
  - Then an on-foot airship deck with wind gusts that change direction.
- **Boss rework:** Wind Man changes the arena wind each phase. At low HP he performs a 1943-style evasive loop.
- **Weapon (tap / Up+B / synergy):**
  - **Wind Storm** (tap): a ground-hugging tornado.
  - Up+B: a vertical **updraft** column that lifts Rock (traversal).
  - **Jet synergy, "Tailwind":** 2× jet speed and no heat for 3 s.
- **Secret exit:** destroy all five planes of the second red formation, and a cloud door opens.
- **Tech:** forced autoscroll + spawn waves (T1)

**Knight Man — "DRAGON QUESTLIKE"**

- **Homage:** *Dragon Quest* (1986), *Zelda II* (1987)
- **Set piece and gimmicks:**
  - Keys and locked doors.
  - Treasure chests, some of them **Mimic Mets**.
  - An **INN** room: 20 bolts for a full heal.
  - A sage NPC with text boxes.
  - A corridor where **"ENCOUNTER!"** locks the screen and an RPG command window appears (FIGHT / RUN; RUN →
    *"BUT YOU COULDN'T ESCAPE!"*).
- **Boss rework:** the fight opens with *"A KNIGHT MAN APPEARS! COMMAND?"*. He has a frontal **shield guard** that a
  Power punch breaks, and flail patterns.
- **Weapon (tap / Up+B / synergy):**
  - **Knight Crush** (tap): a returning flail.
  - Up+B: an orbiting flail guard.
  - **Power synergy, "Morning Star":** a giant flail that breaks blocks and reflects projectiles.
- **Secret exit:** press Down on the **throne** (DQ1's hidden stairs under the king's throne).
- **Tech:** text window and command menu (T2), key/door object (T3)

**Tomahawk Man — "GUN.SMOKE FRONTIER"**

- **Homage:** Capcom's *Gun.Smoke* (1985/1988), *Wild Gunman* (1984)
- **Set piece and gimmicks:**
  - **Wanted posters** at the start list 3 optional bounty mini-bosses.
  - Saloon **quick-draw duels**: when "DRAW!" flashes, fire within 20 frames.
  - A **train-top autoscroll** with parallax ground and ducking under tunnels.
- **Boss rework:** a quick-draw opening, where firing first gives a free hit. Dust devils join his feather and tomahawk
  patterns.
- **Weapon (tap / Up+B / synergy):**
  - **Silver Tomahawk** (tap): an arcing tomahawk.
  - Up+B: a boomerang that returns.
  - **Jet synergy:** dive-bombing diagonal throws.
- **Secret exit:** claim all 3 bounties, and the Sheriff opens "the back way".
- **Tech:** T1, split-scroll parallax (T4), quick-draw prompt (T2)

**Plant Man — "JUNGLE PITFALL"**

- **Homage:** *Pitfall!* (1982), *Super Pitfall* (1986)
- **Set piece and gimmicks:**
  - **Swinging vines**: A to release with momentum.
  - Crocodile-head platforms that open and close.
  - Rolling logs.
  - A parallel **underground route**.
  - Rain with lightning palette flashes.
- **Boss rework:** his vines sprout temporary platforms from the floor, and he "blooms" at low HP.
- **Weapon (tap / Up+B / synergy):**
  - **Plant Barrier** (tap): an orbit shield.
  - Up+B: launches the petals as a forward spread.
  - **Jet synergy, "Petal Storm":** a wider, faster orbit.
- **Secret exit:** a cracked floor that a Power punch breaks leads to the underground "gold bar" room and the back door.
- **Tech:** pendulum physics object (T5), timed-platform object (T3)

**Blizzard Man — "SUMMIT CLIMBER"**

- **Homage:** *Ice Climber* (1985)
- **Set piece and gimmicks:**
  - A **vertical ascent** with breakable ice ceilings (shoot them, or Power-punch upward).
  - Seal-like Topi-bots push ice blocks into holes.
  - A **condor bonus** at the summit.
  - Then a downhill ski autoscroll.
- **Boss rework:** he skis across the arena in passes and makes snowballs from the floor snow.
- **Weapon (tap / Up+B / synergy):**
  - **Blizzard Attack** (tap): a 4-flake spread.
  - Up+B: a temporary **ice-block platform**.
  - **Jet synergy:** flakes drop as bombs.
- **Secret exit:** grab the condor before the timer ends, and it carries you to the secret door.
- **Tech:** destructible ceiling tiles (T6), T1

**Flame Man — "PRINCE OF PERSIA PALACE"**

- **Homage:** *Prince of Persia* (1989/FC 1992)
- **Set piece and gimmicks:**
  - Pressure plates and timed gates.
  - Loose floor tiles that fall.
  - Chomper blades.
  - Oil pools that ignite (vanilla).
  - A **mirror room** where your **Shadow Rock** appears (a palette-swapped copy mirroring your inputs).
- **Boss rework:** the oil floor ignites in patterns, and the fire pillars sweep.
- **Weapon (tap / Up+B / synergy):**
  - **Flame Blast** (tap): a fireball that leaves a pillar.
  - Up+B: an upward fire column.
  - **Power synergy, "Burning Knuckle":** a flaming lunge punch.
- **Secret exit:** *don't fight* your shadow. Walk into it with the buster unequipped (PoP's merge), and the hidden
  route opens.
- **Tech:** pressure-plate/gate pair (T3), input-mirroring object (T7)

**Centaur Man — "ATLANTIS RUINS"**

- **Homage:** Sunsoft's *Atlantis no Nazo* (1986), *Kid Icarus* (1986)
- **Set piece and gimmicks:**
  - Many small numbered **ZONES** linked by doors, including **warp and fake doors**.
  - Walls that hide doors and crack under a Power punch.
  - Rising and falling water.
- **Boss rework:** the arena water level cycles, and he gallops in charges.
- **Weapon (tap / Up+B / synergy):**
  - **Centaur Flash** (tap): a screen flash.
  - Up+B: a **time-stop** for 2 s (an MM2 Flash Man nod).
  - **Power synergy:** 3× punch damage during a time-stop.
- **Secret exit:** the "ZONE 1 → ZONE 9" warp door gag (Atlantis's famous warps).
- **Tech:** zone/warp door table (T3), water level (vanilla?)

**Yamato Man — "EDO NINJA ROW"**

- **Homage:** *Ninja Jajamaru-kun* (1985), *Ganbare Goemon!* (1986), Capcom's *DuckTales* (1989)
- **Set piece and gimmicks:**
  - Rooftop runs with ninja enemies.
  - **Sliding-door secret passages**.
  - Falling-ceiling traps.
  - A **Daruma Otoshi** mini-boss: knock out its stacked segments.
- **Boss rework:** spear volleys, plus ashigaru helpers. His helmet flies off at half HP.
- **Weapon (tap / Up+B / synergy):**
  - **Yamato Spear** (tap): a 3-spear volley.
  - Up+B: a spear that **sticks in walls as a platform**.
  - **Power synergy, the DuckTales pogo:** hold Down in the air to bounce on enemies and spikes.
- **Secret exit:** press Up at a specific hanging scroll painting.
- **Tech:** stacked-segment boss (T8), wall-stick projectile (T3)

**Shared tech list** (built once, reused everywhere):

| ID | Tech |
|---|---|
| T1 | Forced autoscroll + spawn-wave scripting |
| T2 | Text window / prompt overlay (an IRQ split at the bottom of the screen) |
| T3 | Generic "switch → target" object pair: keys, doors, plates, warps, timed platforms |
| T4 | Split-scroll parallax bands |
| T5 | Pendulum physics |
| T6 | Destructible tiles written back to the nametable and collision map |
| T7 | Input recorder/mirror object |
| T8 | Multi-segment boss framework |

### 3.3 Exhibition Matches (unlocked by pairs of secret exits)

These are arcade-history guests. Each is short, built from simple tiles (cheap art), and has a parody name, never a
trademark logo.

| # | Unlock | Guest | Homage | Arena rule | Reward chip |
|---|---|---|---|---|---|
| E1 | Wind + Knight secrets | **Block Man** | *Tetris* (1984) | Tetromino blocks rain into the arena; complete a line (shoot the gap-filler) to damage him, and you're crushed if the stack reaches the top | **Line Clear** (once per stage: a screen-clear bomb) |
| E2 | Tomahawk + Plant | **Paddle Man** | *Breakout/Arkanoid* | He guards the top of the screen; Power-punch the ball back to break his brick shell | **Multiball** (buster shots split on wall bounce) |
| E3 | Blizzard + Flame | **Invader Man** | *Space Invaders* (1978) | A descending formation, destructible bunkers and a UFO bonus; Jet is limited to the bottom row | **Barrier** (absorbs one hit per screen) |
| E4 | Centaur + Yamato | **Maze Man** | *Pac-Man* (1980) | A maze arena with four Met-ghosts; eat power pellets to turn them | **Power Pellet** (an E-tank that also grants 3 s of invincibility) |

### 3.4 Hall of Fame (the museum fortress: the history of the Rockman series)

Each wing opens with a **museum plaque** (JP/EN trivia text) and remixes the signature hazards of one game:

| Wing | Tribute | Hazards remixed | Boss |
|---|---|---|---|
| H1 | ROCKMAN (1987) | Appearing **yoku blocks**, Guts lift rails, Elec beams | **Yellow Devil MK-VI** (a BG-tile boss that flies across; weak eye). The reward is **Magnet Beam**. |
| H2 | ROCKMAN 2 (1988) | Heat Man's vanishing blocks; the dragon-chase autoscroll | **Mecha Dragon MK-VI**. A secret room has Air Man's fans and a plaque thanking *Rockman CX* |
| H3 | ROCKMAN 3 (1990) | Gemini mirror rooms, needle presses | **Gamma MK-VI**. The final phase needs a Power or Super uppercut, as Gamma needed Top Spin. The reward is the **Super Adaptor**. |
| H4 | ROCKMAN 4 (1991) | The Cossack snow citadel, with Kalinka cameo dialogue | **Cossack Catcher MK-VI** (a UFO-catcher claw). A secret plaque thanks *Rockman 4 Minus ∞* |
| H5 | ROCKMAN 5 (1992) | The "Proto Man" castle with gravity flips | **Dark Man MK-VI**, disguised as Blues |

After H5, Mr. Y is unmasked (*"Surprise! It's me, Dr. Wi—" "WE KNOW."*).

### 3.5 Super Wily Castle ("Project SUPER")

| Stage | Concept | Tech showpiece |
|---|---|---|
| W1 "Upgrade Lab" | The stage *upgrades as you go*. It starts in a 4-shade **Game Boy palette** (a Rockman World nod), turns to full NES color, then to "16-bit" with **per-tile palettes (MMC5 ExGrafix)** and the **MMC5 extra pulse channels** joining the music | Palette tiers, ExGrafix attributes, expansion audio |
| W2 "Bracket of Doom" | A boss-rush teleporter hall laid out as a **tournament bracket**, ending with **Bass β (final duel)** | Bracket UI and IRQ panel |
| W3 "MODE-7 Machine" | The final machine sits above a pseudo-3D floor (per-band horizontal scroll and scale illusion, like racing-game roads), then the **Wily Capsule**, then a timed escape | Chained MMC5 scanline IRQs, every 2–4 lines with 8-line bands as the fallback |

### 3.6 Bosses to build or rework: 19

| Group | Bosses |
|---|---|
| 8 champions (rework) | Blizzard, Centaur, Flame, Knight, Plant, Tomahawk, Wind, Yamato |
| 3 new set-piece bosses | Grand Pi-kun, AYACO bomber, Daruma Otoshi |
| 4 exhibition guests | Block, Paddle, Invader, Maze |
| 5 legacy MK-VIs | Yellow Devil, Mecha Dragon, Gamma, Cossack Catcher, Dark Man |
| Finale | Bass β (×2), MODE-7 Machine, Wily Capsule |

Vanilla fortress bosses (Mechazaurus, Power Piston, etc.) can be re-skinned as legacy bosses where their AI fits. M0
catalogues which ones do.

---

## 4. Modes & meta

1. **Main game** in 3 save slots.
2. **New Game+ / Bass Mode** after the first clear.
3. **Time Attack**: per stage, with best times and splits saved.
4. **Grand Prix Rush**: a bracket boss rush with random seeding, saving your best time per bracket size (4 / 8 / 16).
5. **Exhibition Rules**: modifier toggles for any cleared stage, such as BUSTER ONLY, 1 HP (4MI's "Owata-shiki"), NO
   ADAPTORS, TURBO ENEMIES (1.25×) and FAMICOM RULES (no checkpoints).
6. **Records & Medals**: play time, deaths, bolts earned, and medals per stage. There are 10 achievements, for example
   "All Platinum", "Bass Mode clear", "1993 rules clear" and "Parry 100 shots".
7. **Museum**: sound test, plaque gallery, and credits for the people and hacks thanked.

**Unlock pacing:**

| Unlock | Requirement |
|---|---|
| Time Attack | Clear the game |
| Exhibition Rules | 40 Hall of Fame Points |
| Grand Prix Rush 16 | All 4 Exhibitions cleared |
| Final secret | All Gold or better: **"Mr. X Returns"**, a final extra match against the *original* Mr. X, who turns out to be a real, separate person after all |

---

## 5. What we already know about the Rockman 6 ROM (measured)

| Fact | Value |
|---|---|
| Base | Rockman 6 (J). MD5 `d9a4eed8b3c13a6bd74b2e9d20385afb`, CRC32 without header `2D664D99`. NES 2.0 header, mapper 4 (MMC3 TGROM), 512 KB PRG, 8 KB CHR-RAM |
| Vectors | NMI `$C000`, RESET `$FF70`, IRQ `$C14C` |
| Fixed banks | 8 KB bank `$3E` at `$C000`, `$3F` at `$E000` (MMC3 PRG mode 0) |
| Bank-switch helpers | `$CBC0`: Y → `$8000`=Y, `$A000`=Y+1 (a 16 KB pair). `$CBDA`: A → `$A000`. `$CBAF`: `$17` → `$8000`. Shadows: `$4A` (`$8000` bank), `$4B` (`$A000` bank), `$4C` (last `$8000` select value) |
| Sound | The driver lives in banks `$34/$35` (file `0x68010–0x6C00F`). It is called at `$C8C1`, which maps them in: `$8003` = play the sound ID in A, `$8000` = per-frame update, then the caller banks are restored from `$4A/$4B`. Queue: ring buffer at `$B0–$BF`, write index `$D9`, read index `$DB` |
| NMI shadows | OAM DMA from `$0200`. PPUCTRL `$FC`/`$F8`, PPUMASK `$FD`, scroll X `$F7` and Y `$F9` (+ offsets `$069D`/`$069C`, copies `$06A7`/`$06A8`), mirroring `$FB` → `$A000`, IRQ latch `$0672` (+ `$0677`→`$0676`), IRQ on/off selector `$F4` (`STA $E000,Y`), frame counter `$F3`, NMI-busy/lag flag `$F2`, PPU-update request flags `$46`/`$47`/`$60` (→ routines `$C79C` / `$C69E` / `$C6D7` / `$C7DE`) |
| Reset | Writes MMC3 CHR registers R0–R5 from the table at `$FF50`, then `JMP $C51E` (main init) |
| IRQ | MMC3 scanline IRQ in use (about 18 latch-write sites), so vanilla already has raster splits |
| Free space | **Banks `$0B–$0F` (40 KB, file `0x16010–0x2000F`) are unused**: Capcom's alternating 32×`FF` / 32×`00` fill. About 101 KB of fill-like runs exist in total. The fixed bank `$3F` has about 1.1 KB of the same fill at **`$FAC0–$FF20`** (confirm with a CDL before use), which will hold trampolines |
| Text | Two letter tables: **A = `$0B`** (menus etc., around file `0x78537`) and **A = `$2B`** (around `0x78EB1`, `0x7AAC7`), both in banks `$3C–$3D`. The kana tables are still to be mapped |
| WRAM | Vanilla does not meaningfully use `$6000–$7FFF` (only scattered matches, consistent with data noise) |
| Headless boot | Title screen verified in cynes and FCEUmm |

---

## 6. Technical architecture

### 6.1 Target cartridge: MMC5, 1 MB PRG, 8 KB CHR-RAM, 8 KB battery PRG-RAM

This is **exactly the format of 4MI's recommended build**, which this environment's FCEUmm core already runs. Why
MMC5, measured against the content budget:

- **The budget doesn't fit 512 KB.** New code (~50 KB) + new stages (~110 KB) + bosses (~50 KB) + music (~25 KB) +
  bilingual text (~20 KB) ≈ 255 KB against ~101 KB free. MMC3 stops at 512 KB, and 4MI's 1 MB MMC3 build is out of spec.
- **MMC5 solves RAM pressure.** It adds 1 KB of ExRAM, and battery PRG-RAM becomes working RAM for the new systems.
- **MMC5 helps lag.** It has a hardware multiplier.
- **MMC5 enables the finale.** Vertical split and ExGrafix serve the HUD panels and the "16-bit" look, and the two
  extra pulse channels give the "upgrade" theme its sound.
- **The trade-off:** NES (non-Famicom) consoles need a mod for expansion audio. The music must stand on the 5 core
  channels, with the MMC5 pulses as optional color, and config can turn them off. Flash carts: EverDrive N8 Pro supports
  MMC5. Emulators: Mesen, FCEUX, Nestopia and FCEUmm.
- **Contingency:** if the migration in M1 hits a wall, fall back to MMC3 512 KB and cut scope to *Must* items (§8.3).

**Expansion by insertion, like both reference hacks:**

| File region | Contents |
|---|---|
| `0x00010–0x7C00F` | original 8 KB banks `$00–$3D`, **in place** |
| `0x7C010–0xFC00F` | 512 KB of new space (banks `$3E–$7D` in the new numbering) |
| `0xFC010–0x10000F` | original `$3E` and `$3F` move to `$7E` and `$7F` (the fixed banks stay at the top) |

- Every `LDY #bank / JSR $CBC0` in original code stays valid, because the bank numbers below `$3E` don't change.
- The only references to the old fixed-bank numbers are the hardware fixed mapping itself.

**MMC5 configuration** (written in the RESET path at `$FFC5`, replacing the MMC3 CHR setup):

| Register | Value | Meaning |
|---|---|---|
| `$5100` | 3 | PRG mode 3: four 8 KB slots, which mirrors MMC3 mode 0 |
| `$5114` / `$5115` | bank \| `$80` | the `$8000` / `$A000` switchable slots (bit 7 = ROM) |
| `$5116` | `$FE` | bank `$7E` at `$C000` |
| `$5117` | `$FF` | bank `$7F` at `$E000` (also its power-on state) |
| `$5113` | 0 | PRG-RAM page at `$6000` |
| `$5102` / `$5103` | 2 / 1 | unlock PRG-RAM writes |
| `$5101` | 0 | 8 KB CHR mode, since CHR-RAM ignores CHR banking in practice |
| `$5104` | 2 | ExRAM as plain RAM (switched to mode 1 only in W1) |
| `$5105` | `$44` / `$50` | vertical / horizontal mirroring |
| `$5015` | `$03` | enable the extra pulses |

The **4MI MMC5 build is a working reference** for MMC5 + CHR-RAM on a Capcom engine. Study the register sequence in a
debugger (as hardware facts), then write our own code. Never copy its bytes (its readme forbids reusing ROM material).

**Code to port** (every MMC3 register access; the M1 task list):

1. Bank switching:
   - `$CBAF`, `$CBC0`, `$CBDA`, `$C8C1–$C903` (sound map/unmap)
   - the `$FFCC–$FFD8` init loop
   - every other `STA $8000` / `$8001` site (about 17 / 14 candidates; confirm with the CDL)
   - Rewrite them as direct `$5114` / `$5115` writes that keep the `$4A/$4B/$4C` shadows, because other code reads
     them.
2. Mirroring: about 7 `STA $A000` sites (the NMI writes `$FB` → `$A000` at `$C01F`) become `$5105` with a lookup table.
3. IRQ: the `$C000/$C001/$E000/$E001` sites (NMI `$C06C–$C077` + handler `$C14C`).
   - MMC3 counts N lines *from the last reload*; MMC5 compares the *absolute* scanline (`$5203`) and is enabled and
     acknowledged with `$5204`.
   - Port: keep a running absolute-line accumulator in the handler, and convert each latch value to
     `target = previous + latch + 1`.
4. **Regression gate:** the vanilla golden movie (§6.6) must produce identical frame hashes before and after migration,
   except frames with known lag differences.

### 6.2 Memory map (new)

| Range | Use |
|---|---|
| `$0000–$07FF` | vanilla RAM. Free slots are mapped in M0 (RAM-diff method §6.6); assume none are free |
| `$5C00–$5FFF` | ExRAM (1 KB): IRQ effect tables (per-line scroll for W3), text window buffer |
| `$6000–$60FF` | **System block**: signature `"R6GP"` + version, config, records, medals, unlock flags, achievements, 16-bit checksum |
| `$6100–$63FF` | **Save slots 1–3** (256 B each): progress flags, weapons/adaptors, energy, bolts, tanks, chips owned/equipped, Beat plates, secrets bitfields, best scores and times per stage, play time, checksum |
| `$6400–$6FFF` | Working state for new systems: scorecard counters, announcer queue, shop, chip effects, adaptor gauges, Bass Mode state |
| `$7000–$7FFF` | Spare / decompression buffer / debug log ring (development builds) |

**Saves:** write slot data with the checksum last. On boot, an invalid system block causes a full initialise. A slot
with an invalid checksum shows "BROKEN DATA" and can be cleared, as in 4MI's handling.

### 6.3 Code organisation and calling convention

- **Far calls.** A `FARCALL` routine lives in the fixed bank's free fill (`$FAC0+`). It saves `$4A/$4B`, maps the
  target bank pair, JSRs, then restores. New code lives in banks `$40–$7D`. Original code is patched only with
  **3-byte `JSR` hooks** into fixed-bank stubs.
- **Hook registry.** Every patched original address is declared in `src/hooks.oph`, with its original bytes and its
  replacement. The build **fails if two hooks overlap** or if the original bytes don't match the base ROM. This keeps
  the patch honest and makes it rebaseable.
- **Free-space allocator.** The build tool tracks free ranges (seeded from `tools/analysis/banks.py`, then confirmed
  with the CDL). Patches declare `.segment`-like regions, and the allocator assigns them and reports usage per bank.

### 6.4 Toolchain (all verified installable in this environment, from PyPI)

| Need | Tool | Status |
|---|---|---|
| Assembler | **Ophis 2.3** (`ophis-asm`), a Python 6502 assembler. Invoke it as `python3 -c "import Ophis.Main as M; M.run_ophis([...])"` (`-m Ophis.Main` does not work) | ✅ assembled a test snippet correctly, including zero-page optimisation |
| Disassembly | py65 (`tools/analysis/dis.py`). M0 adds a bank-aware recursive disassembler that emits Ophis-syntax listings | ✅ |
| Accurate emulator (headless) | **stable-retro → FCEUmm core**. Load `_retro*.so` directly (no gymnasium needed), as `retroshot.py` does | ✅ boots RM6, both 4MI builds (MMC5!) and CX |
| Fast emulator (headless) | cynes (MMC3 only; fails on the battery-RAM hacks) | ✅ for vanilla smoke tests |
| Images | Pillow + numpy | ✅ |
| Patch format | **BPS** (SourceCopy keeps original data out of the patch, and it checksums source and target). A ~150-line Python encoder lives in `tools/build/bps.py` | to write in M0 |
| Not available | GitHub release downloads (proxy 403), apt `cc65` | use pip only |
| On the user's desktop | **Mesen 2** (debugger, CDL, trace logger, event viewer, Lua) for RE sessions and feel tests; optionally an EverDrive N8 Pro for hardware tests | user-side |

`tools/setup_env.sh` installs everything into `.pylib/` (gitignored). The cloud container is ephemeral, so **re-upload
the Rockman 6 ROM at the start of each session** and place it at `roms/rm6j.nes`. The build verifies its MD5. **Never
commit ROMs** (see `.gitignore`).

### 6.5 Asset pipelines

- **Graphics.** Indexed PNG (4 colors, any palette) ↔ NES 2bpp CHR (`tools/build/chr.py`). Sprite metasprites are
  defined as JSON (tile, attributes, offset), exportable to Capcom's sprite-mapping format once it is reverse-engineered
  (M0). Vanilla CHR-RAM uploads come from PRG banks; M0 confirms whether they are raw or compressed. Art sources:
  1. reuse vanilla tiles
  2. programmatic pixel art for simple tiles (blocks, UI, fonts, exhibition arenas)
  3. hand-drawn sprites from the user or a collaborator, imported as PNG
- **Levels.**
  - First, an **extractor** for RM6's stage format: screens → 32×32 blocks → 16×16 tiles → 8×8, plus room/scroll
    tables and enemy lists sorted by screen.
  - Then a **round-trip test**: extract → rebuild must give identical bytes.
  - Authoring format: **ASCII-art maps** in `assets/levels/<stage>.txt`, with one character per 32×32 block, a legend per
    tileset, and enemy and object lines. This is diffable, and directly writable and reviewable by Claude.
  - A **renderer** outputs full-stage PNG maps for review (`build/maps/*.png`).
- **Text.** YAML source per language → encoded with `.tbl` tables (`A=$0B` and `A=$2B` known; kana is mapped in M0).
  The text engine supports a window, typewriter effect, wait, portrait ID and choice prompts (T2).
- **Music.**
  - M0 decodes the Capcom driver's bytecode (`$34/$35`) by dumping one known song and diffing.
  - Then `tools/build/mml.py`, a small MML → Capcom-bytecode compiler.
  - New stages temporarily reuse vanilla tracks until their songs exist.
  - M8 extends the driver to drive MMC5 pulses (`$5000–$5007`).

### 6.6 Testing (the guard-rail that 4MI lacked)

`tests/run.py` drives FCEUmm headless. Each **scenario** is a YAML file: ROM, optional savestate, an input list of
`frame:buttons` pairs, checkpoints (screenshot frame, RAM assertions, frame-hash) and a timeout.

- **Golden movies.** Vanilla: title → stage select → enter each of the 8 stages → walk/jump a fixed input for 600 frames
  → hash the frames. These gate M1. Later: one route per stage (normal exit), recorded by the user in Mesen
  (`.mmo`) or written as input scripts. The Mesen → `frame:buttons` conversion lives in `tools/build/movie.py`.
- **RAM discovery.** `tools/analysis/ramdiff.py` (M0) runs two input variants (e.g. jump vs. no-jump) and diffs RAM per
  frame to find variables automatically: player X/Y, HP, weapon energy, stage ID, lives.
- **Route checks.** Each adaptor gate has a scripted Bass solution, and the bot asserts it reaches a target position.
- **Visual review.** Screenshots go into `build/shots/` and are sent to the user at milestone gates.
- **Static checks.** Hook-overlap check, free-space overflow check, and a checksum for every bank.

---

## 7. Repository layout (target)

```
README.md                 project intro + quick start
docs/DECONSTRUCTION.md    teardown of CX and 4MI
docs/PLAN.md              this document
docs/STATUS.md            hand-off log (update every session)
docs/re/ram.md            RAM map (M0)
docs/re/rom.md            ROM/bank map, tables, formats (M0)
tools/setup_env.sh        pip toolchain into .pylib/
tools/analysis/           measurement scripts (exist now)
tools/build/              build.py, bps.py, chr.py, levels.py, text.py, mml.py, movie.py
src/                      Ophis sources: hooks.oph, fixed/, banks/<NN>_*.oph, systems/, stages/, bosses/
assets/                   gfx/*.png, levels/*.txt, text/{ja,en}.yaml, music/*.mml, tables/*.tbl
tests/                    scenarios/*.yaml, golden/, run.py
roms/  build/  .pylib/    gitignored
```

---

## 8. Milestones

Each milestone ends with a **playable build, passing tests, and an updated `docs/STATUS.md`**. Tasks are sized so that
one task ≈ one focused session (**S** < 1 session, **M** ≈ 1–2, **L** ≈ 3+). Do them in order. Items marked ⛳ are
gates where the user plays the build and gives feedback.

### M0 — Workbench & reverse engineering

1. **M0.1 (S)** Scaffold the repo layout (§7) and `tools/build/build.py`.
   - Steps: verify the base MD5 → copy → apply hooks (none yet) → write the header → emit `build/r6gp.nes` and
     `build/r6gp.bps`.
   - Test: the no-op build is byte-identical to the base.
2. **M0.2 (S)** `tests/run.py` plus the first scenario (boot → title screenshot → Start → stage-select screenshot).
3. **M0.3 (M)** RAM map v0 via `ramdiff.py`: player X/Y/velocity/state, HP, weapon energies, current weapon, adaptor
   state, lives, E-tanks, Beat plates, stage ID, checkpoint, boss HP, object table layout (slot count and fields).
   Write the results to `docs/re/ram.md`.
4. **M0.4 (M)** Bank-aware recursive disassembler (py65 tables). Annotated listings of banks `$3E/$3F` and the
   stage-select, pause-menu and password code. Confirm the free fill at `$FAC0–$FF20` and in banks `$0B–$0F` (a CDL from a
   Mesen playthrough is ideal: **ask the user to record one**).
5. **M0.5 (M)** Stage tables: per-stage pointers to layout, tileset/CHR upload list, palettes, music ID, enemy list,
   boss ID. Catalogue the vanilla fortress stages and bosses.
6. **M0.6 (L)** Level extractor, renderer and **round-trip rebuild** for one stage (Wind Man), then all stages. Output:
   full-map PNGs of vanilla RM6 (a great review artifact).
7. **M0.7 (M)** Object/AI tables: enemy ID → AI pointer, HP, damage, weapon damage tables (and where boss weakness tables
   live).
8. **M0.8 (M)** Sound driver: song table, command bytes, one song decoded to readable form.
9. **M0.9 (S)** Text: kana tables and the dialogue/ending text routine.
10. **Exit:** `docs/re/*.md` are filled, and the build and test pipeline is green on the vanilla ROM.

### M1 — Big Cartridge

1. **M1.1 (M)** Insertion expansion to 1 MB + MMC5 header + RESET MMC5 setup.
2. **M1.2 (M)** Port every bank switch and mirroring site.
3. **M1.3 (M)** Port the IRQ system (accumulator conversion), and test every vanilla stage with splits.
4. **M1.4 (S)** `FARCALL`, the hook registry and the free-space allocator in the build.
5. **M1.5 (S)** PRG-RAM system block + save-slot scaffolding (signature, checksum, init).
6. **Exit:** the golden movies match vanilla. ⛳ The user spot-checks in Mesen.

### M2 — Feel

1. **M2.1 (M)** Select-modifier quick-swap for weapons and adaptors, last-weapon toggle, pseudo L/R.
2. **M2.2 (S)** QoL pack: menu fixes, faster E-tank, efficient pickups, upward-scroll boost, colored death/get tints.
3. **M2.3 (M)** New title screen (logo via CHR-RAM), file select (3 slots), CONFIG menu, removal of the password screen.
4. **M2.4 (S)** Difficulty plumbing: a damage multiplier hook, lives/E-tank floor, item-drop table switch.
5. **Exit:** vanilla content plays with the new controls and saves. ⛳

### M3 — Systems

1. **M3.1 (M)** Scorecard counters + results screen + medals + bolts + announcer queue (T2 text window, minimal).
2. **M3.2 (M)** Shop and chip framework (stock tiers, slots, help pages); implement 6 chips.
3. **M3.3 (L)** Adaptor overhaul (parry, lunge, heat gauge, air-dash, quick-swap integration, acquisition by win count).
4. **M3.4 (M)** Weapon framework: tap / Up+B / per-form synergy dispatch table, fixed mook damage, minimum boss damage,
   "WEAK!" pop.
5. **Exit:** the full loop works on vanilla stages. ⛳

### M4 — Vertical slice ⛳⛳ (the big design gate)

1. **M4.1 (L)** Opening Ceremony stage + Grand Pi-kun.
2. **M4.2 (L)** Wind Man venue (T1, the shmup segment, the AYACO bomber, Wind Man rework, Wind Storm).
3. **M4.3 (L)** Knight Man venue (T2 full, T3, the ENCOUNTER gag, Knight Man rework, Knight Crush).
4. **M4.4 (S)** Story intro text (JP and EN) and the stage-select bracket dressing.
5. **Exit:** ~20–30 minutes of finished content. **Decide here** whether the scope, difficulty and humor are right
   before mass production.

### M5 — The other six venues

One **L** task per venue (Tomahawk, Plant, Blizzard, Flame, Centaur, Yamato), plus Semifinal Riot / Bass β duel 1
(**L**). Each includes the tech items it needs from T1–T8, its hidden room, secret exit and Beat plate (where present).
⛳ after the 8th venue.

### M6 — Exhibitions

E1–E4, one **M** task each (small stages with big gimmicks), plus the reward chips.

### M7 — Hall of Fame

H1–H5, one **L** task each (Magnet Beam in H1, the Super Adaptor in H3), plus the unmasking cutscene. ⛳

### M8 — Project SUPER

1. W1 Upgrade Lab: palette tiers, ExGrafix and expansion audio (**L**).
2. W2 bracket rush + Bass β final (**L**).
3. W3 MODE-7 Machine + Capsule + escape (**L**).
4. Ending and credits bracket (**M**).

### M9 — Post-game

Time Attack (**M**), Grand Prix Rush (**M**), Exhibition Rules (**S**), Records/Medals/Achievements (**M**), Museum
(**S**), Bass Mode (**L**, *Could*), and the "Mr. X Returns" final match (**M**).

### M10 — Polish & release

1. Full JP/EN text pass.
2. Balance pass: scorecard pars, shop prices, damage tables, difficulty presets.
3. Emulator matrix: Mesen, FCEUX, Nestopia, FCEUmm, plus hardware if available.
4. Release package: the BPS patch, a readme (JP/EN) with credits and thanks to the CX and 4MI authors and the RM6 fan
   designers, and patch instructions (Floating IPS / Rom Patcher JS both apply BPS).

### 8.3 Scope tiers (MoSCoW)

| Tier | Scope |
|---|---|
| **Must** | M0–M5; Hall of Fame H1, H3, H5; W2 + W3 (+ ending); 3 slots; config; scorecard/shop/chips; adaptor overhaul; JP + EN |
| **Should** | All 5 Hall of Fame wings; Exhibitions E1–E4; W1 Upgrade Lab; Time Attack; Grand Prix Rush |
| **Could** | Bass Mode; MMC5 expansion-audio arrangements; Exhibition Rules; Museum; "Mr. X Returns" |
| **Won't (v1)** | Slopes; new player sprite sets beyond Bass; netplay-style features |

If the MMC5 migration fails (the M1 contingency), stay on MMC3 512 KB and ship only the **Must** tier.

### 8.4 Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| IRQ port breaks vanilla raster effects | M | Golden movies per IRQ-using stage; port the accumulator first; MMC3 fallback |
| No free RAM in 2 KB | H | Move new-system state to PRG-RAM `$6400+`, and ExRAM |
| Lag in busy scenes (vanilla RM6 already slows down) | M | Mesen profiler, VBlank transfer optimisation, MMC5 multiplier, object caps per screen |
| Level format harder than expected | M | Round-trip test before any authoring (M0.6); ASCII format abstracts it |
| Art bottleneck | H | Reuse tilesets; programmatic art for simple assets; user or collaborator for hero sprites; Bass is *Could* |
| Sound driver format opaque | M | Decode early (M0.8); reuse vanilla tracks as placeholders; music last |
| Emulator dependence (4MI's regret) | M | Test FCEUmm headless every build, Mesen at every ⛳, and hardware before release |
| Session/credit budget | H | Session-sized tasks; `docs/STATUS.md` hand-off; every session ends green and committed |
| Copyright | — | Never commit ROMs; ship BPS only; parody names, no trademark logos; credit everything |

---

## 9. Open decisions for the user

Each has a recommended default, so work can proceed without waiting.

1. **Title:** *ROCKMAN 6 GP* (default). Alternatives: *Rockman 6: Shijō Saidai no Kaizō!!* ("The Greatest **Hack** in
   History", a pun on the subtitle), or *Rockman 6 ENCORE* (the farewell-to-8-bit framing).
2. **Rival:** Bass β (default, an MM7 nod), or an original rival ("MODE-7" as a character rather than a machine).
3. **Real-hardware priority:** if a stock NES without the audio mod matters most, MMC5 audio stays optional (the default
   already assumes this).
4. **Art help:** will the user draw or commission sprites (Bass, guests, legacy bosses), or should Claude produce
   programmatic or edited art first and iterate from screenshots? Default: Claude first, the user approves.
5. **Difficulty target:** NORMAL tuned to "4MI-hard with CX-generous tools" (default), or gentler.

---

## 10. How the next session starts (copy this checklist)

1. Upload `Rockman 6 - Shijou Saidai no Tatakai!! (Japan).nes` and say **"begin M0"**.
2. Claude runs `tools/setup_env.sh`, places the ROM at `roms/rm6j.nes`, and verifies MD5
   `d9a4eed8b3c13a6bd74b2e9d20385afb`.
3. Claude reads `docs/STATUS.md` → picks the next unchecked task → works → runs the tests → commits → updates
   `docs/STATUS.md`.
4. For RE help (optional but very valuable): play vanilla RM6 in **Mesen 2** with the **CDL logger** on (Debug → Code/
   Data Logger), touching every stage once, then upload the `.cdl` file. It turns weeks of static guesswork into
   certainty about what is code, data or free.
