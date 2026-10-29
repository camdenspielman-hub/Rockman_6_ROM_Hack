# Rockman 6 GP: player-facing systems

Author: design-systems. Status: **v1, complete for its scope** (§0 lists the scope). It follows `BRIEF.md` §5 and
§8. Facts come from `docs/research/*`; numbers I measured for this doc are tagged **[seen, ds]**. The scripts are
in `build/design/design-systems/`. Every number is either grounded in vanilla, argued in the text, or marked
**(tune)**.

Tags (BRIEF §8):

- **[engine-ok]**: vanilla does it, or it is a data change;
- **[new-code]**, **[new-art]**, **[new-music]**;
- sizes **S/M/L**; tiers **Must/Should/Could**.

Every item has an id (`SYS-…`), so other docs can cite it.

---

## 0. Scope and the decisions in one page

This doc owns what the player touches in every stage:

- controls; forms and physics;
- the weapons, Magnet Beam and the Break Man moveset;
- the damage and i-frame tables; weakness feedback;
- the scorecard; bolts, the shop and chips; slots and plates;
- the tag partner rules; pickups and economy; difficulty; criticals.

It does not own stage layouts, boss patterns, story text, UI art or the memory map. It states what it needs from each
(§15).

**The decisions:**

1. **SELECT is a modifier** (§1).
   - Hold SELECT + Up/Down cycles weapons; hold SELECT + Left/Right cycles forms.
   - A SELECT tap toggles the last weapon.
   - Controller 2's A/B act as pseudo L/R.
2. **The quick form swap has no cutscene** (§1.3). It streams the form's sprite CHR in 8-16 frames behind a
   12-frame "swap flash" and grants no invincibility. The vanilla Rush-docking cutscene plays once per form per save,
   the first time.
3. **Forms fire weapons** (§3).
   - Every weapon fires in every form.
   - Each of the 8 boss weapons has **one** synergy: Power with Y.SPEAR, F.BLAST, KNIGHT.C and C.FLASH; Jet with
     W.STORM, B.ATTACK, PLANT.B and SILVER.T.
   - In Power form the "buster" is the punch; in Jet form it is the uncharged buster.
4. **Combat = two tables, 4MI-style (credit: Puresabe)** (§4).
   - Damage per boss × source, 1-4.
   - I-frames per boss × source. Measured vanilla: **60 frames after every hit, whatever the weapon** [seen, ds].
   - GP keeps 60 for the buster family and drops the rest: weakness 4 dmg / 16 f, "good" 3 / 20 f, neutral 2 / 30 f,
     resisted 1 / 45 f.
   - The vanilla weakness cycle is kept. A second "good" permutation and a "resist" permutation make every weapon
     equally useful across the eight champions.
5. **The shot class is the scoring key** (§6.4).
   - GP gives every player shot family its own class nibble: 1 buster, 2 punch, 5-C the eight weapons, D Magnet Beam,
     E Break Man, 4 player-caused hazards.
   - A copy of the hit latch `$056C` (which the victim clears) is kept per slot in WRAM. The death sites read it.
   - VARIETY is a popcount over those classes.
6. **The economy has no grind** (§7-§8).
   - Bolts come only from scorecards (best score per stage, paid once), sponsor envelopes in hidden rooms and a
     handful of fixed prizes.
   - Prices are sized against a measured income model.
7. **Fifteen chips** (§9): 7 bought, 1 found (the Energy Balancer, now a chip), 2 earned by behaviour, 4 crafted and
   1 moral trade-off.
   - **Crafting is RM6-native.** Vanilla's per-class one-shot tables (F.BLAST melts the snow robot) are extended. A
     venue's featured enemy killed by its *thematic* weapon drops a PART, and Eddie builds chips from pairs of PARTs.
   - **The moral trade-off is doping.** Mr. Y buys a PART and gives you the TURBO chip. Break Man then refuses to
     partner you, and your records carry an asterisk.
8. **Beat** (§10).
   - Each plate adds a chip slot (2 + 4 = 6).
   - B-E-A-T complete: Beat becomes the pit rescue.
   - Vanilla's BEAT weapon slot (slot 9) becomes MAGNET BEAM.
9. **Break Man** is a once-per-life, 20-HP spare body (§11).
   - Buster only, with a Break Shot, an airborne shield and double knockback.
   - At 0 HP he retreats; no life is lost.
10. **Pickups** (§12).
    - Vanilla values were measured: small/large life +2/+10, weapon +2/+10, drops on 31/256 of kills.
    - Base rule: an unusable weapon pickup becomes half-value HP (CX).
    - The Balancer chip routes it to the lowest weapon (the vanilla behaviour, measured).
11. **Difficulty** = CASUAL / NORMAL / HARD / 1993 presets over one-byte knobs (§13). HARD = poke lists + AI branches
    (4MI).
12. **Criticals** are a *Could*, off in records modes (§14): LFSR dice, 1/128 base, +2 damage on bosses.

### 0.1 Item index

| Id | Item | Tags | Size | Tier |
|---|---|---|---|---|
| SYS-CTL-1 | SELECT modifier: weapon and form cycle | new-code | S | Must |
| SYS-CTL-2 | Last-weapon toggle (SELECT tap) | new-code | S | Must |
| SYS-CTL-3 | Controller-2 pseudo L/R | new-code | S | Should |
| SYS-CTL-4 | Quick form swap with CHR streaming | new-code, new-art (2 tiles) | M | Must |
| SYS-FRM-1 | Forms fire weapons (fire dispatch by weapon × form) | new-code | M | Must |
| SYS-FRM-2 | Adaptors by win count (Power 2nd, Jet 4th) | new-code (patch `$38:$931D`, `$3B:$BA3F`) | S | Must |
| SYS-FRM-3 | Power parry | new-code, new-art (1 spark) | M | Should |
| SYS-FRM-4 | Power ice grip | new-code | S | Could |
| SYS-FRM-5 | Super Adaptor: rocket fist with homing return, jet hop | new-code, new-art | L | Must (with H3) |
| SYS-FRM-6 | Jet low-fuel pip | new-code, new-art (1 tile) | S | Should |
| SYS-WPN-1..8 | Eight boss weapons: tap, alt, synergy | new-code (+ new-art per alt) | L total | Must (tap, alt, synergy); Could (own-weapon reactions) |
| SYS-WPN-9 | MAGNET BEAM (slot 9) | new-code, new-art | M | Must (H1 is Must) |
| SYS-WPN-10 | Buster charge rules (vanilla thresholds) | engine-ok | S | Must |
| SYS-CMB-1 | Boss damage + i-frame tables, one lookup | new-code | M | Must |
| SYS-CMB-2 | Normal-enemy rules (low nibble, thematic tables, re-hit timer) | engine-ok + new-code | S | Must |
| SYS-CMB-3 | Frozen tick (time stop, freeze, stagger keep taking damage) | new-code | M | Must |
| SYS-WK-1 | WEAK! pop, stagger, SFX, announcer event | new-code, new-art (5 tiles) | S | Must |
| SYS-SC-1 | Scorecard counters and formulas | new-code | M | Must |
| SYS-SC-2 | Results screen (judges) | new-code, new-art | M | Must (owner: meta.md) |
| SYS-SC-3 | Secret tokens on replays | new-code | S | Must |
| SYS-ECO-1 | Bolts, Eddie's Pit Stop stock and prices | new-code | M | Must |
| SYS-CHP-1 | Chip framework (bits, slots, help pages) | new-code | M | Must |
| SYS-CHP-2 | The 15 chips | new-code | M | 9 Must / 6 Should |
| SYS-CHP-3 | PARTs and the garage (crafting) | new-code, new-art (8 icons) | M | Should |
| SYS-CHP-4 | Mr. Y's booth (TURBO) | new-code, text | S | Should |
| SYS-BT-1 | Plates → slots; Beat pit rescue | new-code | M | Must (slots), Should (rescue) |
| SYS-TAG-1 | Break Man tag partner | new-code, new-art (sprite set), new-music (whistle) | L | Should (BRIEF §9) |
| SYS-PU-1 | Pickup routing (HP conversion, Balancer, Exchanger) | new-code | S | Must |
| SYS-PU-2 | Drops table and presets | engine-ok (data) + new-code (preset switch) | S | Must |
| SYS-PU-3 | Pit-crew refill on respawn | new-code | S | Must |
| SYS-PU-4 | W-tank; E-tank heal ×2 | new-code | S | Should |
| SYS-DIF-1 | Presets and overrides | new-code | M | Must |
| SYS-DIF-2 | HARD: poke lists + AI flag | new-code | M | Must (framework); content per venue |
| SYS-DIF-3 | 1993 rules switch | new-code | M | Should |
| SYS-CRT-1 | Criticals | new-code, new-sfx | S | Could |

---

## 1. Controls

Vanilla facts: joypad 1 held/new = `$40`/`$42`, joypad 2 = `$41`/`$43`; A=$80 B=$40 SELECT=$20 START=$10 UP=$08
DOWN=$04 LEFT=$02 RIGHT=$01. The read routine is `$3E:$C711`. The only SELECT test in the ROM is the dead sound player
(`$28:$813C`), and holding SELECT for 240 frames in 8 game states changes nothing (`rm6/ram.md`). **SELECT is free.**

### 1.1 SYS-CTL-1: the SELECT modifier [new-code] S, Must

One filter runs right after the joypad read. It is active only in stage play: not paused, not in a transition,
no cutscene, not playing Break Man. It changes `$40/$42` before the player AI sees them.

```
if SELECT held:
    on UP edge    -> weapon_prev()        on DOWN edge  -> weapon_next()
    on LEFT edge  -> form_prev()          on RIGHT edge -> form_next()
    any D-pad edge sets SEL_USED
    UP and DOWN are removed from $40/$42 while SELECT is held (no ladder grab, no slide)
    a LEFT/RIGHT edge sets that direction's bit in SWAPMASK
SWAPMASK bits are removed from $40/$42 until that direction is released
```

Why the mask works this way:

- Walking right with RIGHT held, then pressing SELECT + LEFT, swaps the form while Rock keeps walking right. LEFT is
  masked; RIGHT is untouched.
- Swapping in mid-air keeps the player's air control, which a full D-pad mask (CX's rule) would not. RM6 air control
  is direct, so a full mask would kill the jump.

Cycle orders (skip what is not owned):

- **Weapons**: BUSTER, Y.SPEAR, W.STORM, B.ATTACK, F.BLAST, PLANT.B, KNIGHT.C, SILVER.T, C.FLASH, M.BEAM, wrapping.
  This is the vanilla menu order, `$0688-$0691`, with slot 9 renamed (§3.10). A slot is owned when its energy byte is
  not `$80`.
- **Forms**: NORMAL, POWER, JET, SUPER, wrapping.

Feedback: the weapon bar recolours at once, plus a short new tick SFX. Vanilla's menu blip `$32` is the placeholder.

What a swap keeps (CX lesson: "decide what survives a swap"):

- Shots already in flight finish, and they keep their own class for scoring.
- Lingering objects (barrier, held flail, Magnet Beam platforms, an active Time Stop) stay until their own timer ends.
  So a swap never deletes the platform under you, which was CX's trap.
- Swapping away from the buster clears the charge (`$9E` = 0).

Config: **SELECT SWAP = FULL / WEAPONS ONLY / OFF** (OFF for players who want vanilla feel).

### 1.2 SYS-CTL-2: last-weapon toggle [new-code] S, Must

- A SELECT press released within **15 frames (tune)** with no D-pad edge swaps the current weapon and `LASTW`.
- `LASTW` is written by every weapon change: the cycle, the pause menu, the toggle itself.
- If `LASTW` is no longer owned (W2's bracket rush, where weapons can be withheld), the toggle goes to the buster.
- Holding SELECT longer than 15 frames with no D-pad does nothing. It is safe to "rest" on SELECT.

### 1.3 SYS-CTL-4: quick form swap with CHR streaming [new-code] M, Must; [new-art] 2 tiles

Vanilla: only the pause-menu transform `$38:$965F` loads a form's sprite CHR (bank `$01`, sets `$04-$07`, 2,048 bytes
read for Power). Poking `$9B` alone shows garbled sprites (`rm6/engine.md` §3.2). Closing the menu with a form also
resets the weapon to the buster (`$38:$93F7`). GP drops that reset.

The swap:

| Frame | What happens |
|---|---|
| 0 | `$9B` = new form. Physics switch at once. The charge is cleared. Rock's sprite is hidden (`$03B7` bit 0), and a **swap-flash** object (type from the free id list, 2 resident tiles, Rush red/white) is drawn over him |
| 1..n | A streamer copies the form's *difference tiles* into the player's sprite CHR, **128 bytes (8 tiles) per frame (tune)**, through the NMI transfer queue. n = tiles / 8 |
| n+1 | Rock is shown with the new tiles. The flash fades over 4 frames |

Budget and timing:

- **Target n ≤ 8**: at most 64 changed tiles (1 KB) per form, so the swap reads as a 12-frame flash (0.2 s).
- Vanilla's 2,048-byte read is the worst case: 16 frames at 128 B. art_audio.md and tech.md must confirm how many
  tiles really differ (§15).
- 128 B/frame is a guess at what fits beside the scroll column paints. tech.md owns the real VBlank budget.

Rules:

- **No i-frames during the swap.** Otherwise swap spam would be invincibility.
- **20-frame cooldown (tune)** between form swaps, so a stream always finishes. A press during a stream is queued
  (one deep).
- Not allowed: on a ladder (`$94` = 4), in knockback, while sliding, while playing Break Man.
  - In Jet flight a swap out of Jet is allowed: Rock falls with his current Y speed.
  - A swap into Jet in mid-air may fly at once if `$9C` ≥ 0.
- The fuel `$9C` and its regen keep running in every form. Vanilla's HUD routine `$3E:$CF90` already refills it
  whenever Rock is not flying.
- **First use of each form per save** plays the vanilla Rush-docking sequence ($38:$965F) once, as a "transformation
  debut". After that only the quick path runs. Cost: 1 save bit per form.
- The pause-menu form selection uses the quick path too. Under the 1993 preset it always plays the vanilla cutscene
  (§13.3).

### 1.4 SYS-CTL-3: controller-2 pseudo L/R [new-code] S, Should

The 4MI precedent: controller 2's A/B cycle weapons.

| P2 input | Action |
|---|---|
| A | next weapon |
| B | previous weapon |
| A+B (both held on the same frame) | buster |
| LEFT / RIGHT | previous / next form |
| UP | last-weapon toggle |

- A Famicom pad II has A/B and the D-pad but no SELECT/START, so everything above is reachable on real hardware.
- Emulator users can bind P2 A/B to shoulder buttons.
- Config **2P SHIFT = ON (default) / OFF**.
- Vanilla's reads of `$41/$43` must be checked by tech.md (§15), in case the Famicom mic or expansion-port logic reads
  them.

### 1.5 Other control rules

- **Alternate fire = UP+B** (B pressed while UP is held), except where a weapon says "hold".
  - On a ladder only the tap fires, because UP means "climb" there.
  - RM6 has no up-aim, so UP+B steals nothing.
- **Pause menu: SELECT calls Break Man** (§11), as in CX.
- **The bracket screen** (stage select) uses SELECT to open Eddie's Pit Stop (meta.md owns the screen).

---

## 2. Forms and physics

### 2.1 Vanilla numbers (the ground truth)

| | Normal | Jet (`$9B` = 1) | Power (`$9B` = 2) | Source |
|---|---|---|---|---|
| Walk | 1.297 px/f (`$01.4C`) | same | same | engine.md §3.2 |
| Jump | stored vy `$FA.CC` (-5.20 px/f), gravity +0.25 px/f², peak 51 px, 42 f airtime | same start, then flight while A is held | same as normal | ram.md, critic |
| Slide | DOWN+A, 2.5 px/f, 40 px in 16 f | none | none | engine.md |
| Charge `$9E` | +1/f; half at `$24` (36 f), full at `$5A` (90 f, `$06AB`) | none (always shot `$09`) | +2/f, full in 45 f | `$38:$8651`, table `$38:$854A` = `09 0A 0B 09 / 09 09 09 09 / 0C 0E 0F 09` |
| Fuel `$9C` | regenerates | 19 units; −1 per 4 f of flight (76 f full tank); +1 per 2 f when not flying, even in mid-air | regenerates | engine.md |
| Flight [seen, ds] | | holding A from the floor: Y 175 → 42 (133 px) in ~70 f, holds height, then falls at −1. Fuel back to 19 about 40 f after landing. **Pulsing A (4/2, 6/2, 8/4, 3/3 frames) never sustains altitude**, so vanilla has no infinite-hover exploit | | `jet.py`, `jet2.py` |
| Punch [seen] | | | fist appears 6 f after B at +21 px, flies 4 px/f to +81 px, holds ~10 f, gone at 32 f; hits 16-80 px | engine.md `punch.py` |
| Hurt [seen, ds] | 30 f knockback state at 0.5 px/f (14 px), then 60 f of blinking i-frames (2 on / 2 off): **90 f of safety per hit**. Power form identical | | | `dbg2.py` |

Floor types (`$064B` / latch `$A7`):

| Type | Floor | Effect |
|---|---|---|
| 5 / `$15` | ice | momentum `$A1.$A0`, ±`$00.06` per frame; 24-36 px of slide after letting go |
| 9 | oil | jump `$FB.CC` (−4.20 px/f, peak ≈ 35 px), walk 0.5 px/f |
| 8 | water | gravity `$00.18` |
| A / C | updraft / fan | |
| E | blocks Jet thrust | |
| 6 | ship deck | |

### 2.2 What GP changes, per form

**NORMAL** [engine-ok]: unchanged. It stays the reference feel and the only form with a slide and a charge buster.

**POWER** (after the 2nd win, SYS-FRM-2):

- Walk, jump and charge as vanilla. The punch keeps its reach and timing.
- **Punch damage moves to its own class** (§4.1): tap `$22`, half `$23`, full `$24`.
  - The punch-only rule (`$3F:$EA99`: Metalls) and the shield rule (`$38:$90A2`) test `$24` instead of `$14`.
  - The cracked-block rule (collision `$B`) accepts `$24`.
  - Normal-enemy damage keeps vanilla's 2 / 3 / 4.
- **SYS-FRM-3 Parry** [new-code] M, Should. Vanilla precedent: the full punch rebounds projectiles in Wily 1 as player
  objects `$DA/$E4`, attack `$1A` (engine.md §1.2). GP generalises it:
  - In the class-4 handler `$38:$9028` (enemy bullets), a punch fist of any level that touches a bullet not listed in
    a NOPARRY type table replaces it with a reflected object.
  - The reflected object reverses the bullet's velocity, flies at 1.5× speed, has attack `$23` (class 2: PUNCH for
    scoring) and its own boss column, PARRY.
  - Feedback: a "ting" SFX and a 1-sprite spark. Rock gets **12 i-frames without blinking (tune)**, so the rest of a
    volley can't punish the parry.
  - NOPARRY holds beams, big boss bodies and anything a venue marks.
  - The first parry per stage is a STYLE act and an announcer event.
- **SYS-FRM-4 Ice grip** [new-code] S, Could. On type 5/$15 floors Power's momentum decays at 2× (`$00.0C`/f), so it
  slides 12-18 px instead of 24-36. That is the "heavy form" identity for the Blizzard venue.
- With a weapon equipped, B fires the weapon. The punch is the Power form's "buster" (slot 0).

**JET** (after the 4th win):

- Keep the 19-unit stamina bar exactly. It is not exploitable (measured above), so the BRIEF's *overheat stall* adds
  nothing and is **dropped**.
- Jet still cannot charge (the buster always fires `$09`).
- With a weapon equipped, B fires the weapon in flight. That is how 4 synergies happen.
- **SYS-FRM-6 Low-fuel pip** [new-code] S, Should. When the weapon bar shows a weapon (not fuel), fuel is invisible.
  A single sprite pip under Rock blinks when `$9C` < 5 (20 frames of flight left). It costs 1 tile and 1 sprite.
  - With the buster equipped, the weapon bar shows fuel as in vanilla (`$3E:$CF90`).
- Floor type E keeps blocking thrust. It is the venue designers' anti-Jet tool, and they should use it to protect
  intended routes.
- Air-dash (the PLAN idea) is **cut to Could**. It needs double-tap detection and fights with the SELECT filter.

**SUPER** (H3 reward, SYS-FRM-5) [new-code] L, Must with H3; [new-art] fist sprite + Super Rock set:

The design rule from PLAN: weaker than each specialist, no gauge.

| | Super | Compared with |
|---|---|---|
| Walk / jump | Normal's (1.297, `$FA.CC`) | |
| Slide | no | Normal |
| **Jet hop** | the second A press in the air (once per airtime): vy := `$FC.40` (−3.75 px/f), ≈ +28 px. Max height ≈ 51 + 28 = **79 px (tune)** | Jet: 133 px |
| Tap B (slot 0) | short punch, like Power's tap (2 to mooks) | |
| **Rocket fist** (hold B, +2/f, full at 45 f like Power) | the fist flies straight ahead at 5 px/f up to 112 px or until it hits. Then it **homes back** at 6 px/f, re-aiming at Rock each frame with ±2 px/f of lateral correction. It hits on both legs, breaks cracked blocks (`$B`) on the outward leg, and allows one fist at a time | Power full punch: 4 to mooks, reach 81 px, parries |
| Fist damage | mooks 3 out / 2 back; bosses: the FIST column (§4) | |
| Weapons | all, no synergies (the 8 synergies are Power or Jet only, BRIEF §5.1) | |

The homing return lets the fist hit an enemy *behind* Rock on the way back. That is the trick the H3 Gamma fight and
late fortress rooms can teach.

### 2.3 SYS-FRM-2: acquisition by win count [new-code] S, Must

Per BRIEF §4:

- `$38:$931D` (menu) and `$3B:$BA3F` (stage start) derive the forms from a **WINS** counter instead of the Plant and
  Flame bits: Power when WINS ≥ 2, Jet when WINS ≥ 4.
- Super = a save bit set by the H3 clear.
- WINS = the number of venue champion flags set.

The announcer celebrates each new form at the next stage start.

### 2.4 Normal-route rule (shared with the venue docs)

**A normal exit never needs a form, an alt fire, a synergy or Break Man.** Secret exits, hidden rooms and PART kills
may.

- This keeps PLAN §2.2's rule.
- It keeps the 1993 preset (§13.3) finishable.
- It keeps the sequence free: forms arrive by count, so any venue can be first.

---

## 3. The weapon roster

### 3.0 Rules shared by every weapon

- **Inputs.** Tap = B. Alt = UP+B, or "hold B" where stated. A synergy is what the tap or hold becomes in the named
  form; in the other forms the weapon behaves as in Normal.
- **Dispatch** (SYS-FRM-1) [new-code] M, Must.
  - Vanilla's fire jump table `$38:$8556/$8560` (by `$0699`) becomes a weapon × {tap, alt} table plus a synergy
    override by form.
  - The "may shoot in this state" table `$E130[form*8 + $94]` is opened for forms 1-3.
  - The vanilla fire routines (`$8582`, `$85D9`, `$857E`, `$857A`) and the slot rules (one-at-a-time in slot 3; the
    spread weapons need slots 1-4 empty) are kept for the taps.
- **Energy** is spent through vanilla `$38:$9E8E` on the first frame (bar = 28 units). A weapon at 0 can't fire. The
  ENERGY SAVER chip halves costs (§9).
- **Normal-enemy damage** = the low nibble of the shot's attack byte (vanilla `$3F:$E9D7`). The tables below give that
  nibble.
- **Boss damage** comes from §4. A synergy shot uses its weapon's cell. Alt fires use their weapon's cell unless
  stated.
- **Class nibble = scoring category** (§6.4). Alts and synergies keep their weapon's class, so they count for that
  weapon in VARIETY.
- **Help pages** (4MI lesson: ship one per weapon from day one) are the quoted lines. EN is given; the JP text pass is
  owned by story.md.

### 3.1 R.BUSTER (slot 0, class 1) [engine-ok] S, Must

| Level | Hold | Shot (vanilla type) | Attack byte | Mook dmg | Boss column |
|---|---|---|---|---|---|
| tap | - | `$09` | `$11` | 1 | BUSTER |
| half | ≥ 36 f (`$24`) | `$0A` | **`$12`** (vanilla `$11`) | **2** (vanilla 1) | BUSTER |
| full | ≥ 90 f (`$5A`) | `$0B` | `$13` | 3, flies on through what it kills (vanilla) | CHARGE |
| Jet form | no charge | `$09` | `$11` | 1 | BUSTER |

- Up to 3 tap shots on screen, as in vanilla.
- The half charge gains 1 damage against normal enemies only. Vanilla's half shot was a useless 1; now a partial
  charge is worth holding in mook rooms. Against bosses it stays in the BUSTER column.
- CHARGE KIT (§9) moves the thresholds to 24 / 60 frames.
- A held charge survives the pause menu (vanilla, measured by the critic).

> R.BUSTER - "Hold B to charge. A full charge pierces whatever it destroys. The judges call it 'reliable'. They do not
> mean it as a compliment."

### 3.2 Y.SPEAR (Yamato, slot 1, class 5)

Vanilla: shot `$81`, attack `$52`, one at a time, cost 1, mook 2. It is Knight Man's weakness.

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Spearhead straight ahead (vanilla speed). **New: it pierces the first enemy it does not kill** (one pass-through, then it stops on the next) | 1 | 2 |
| Alt: **Wall Spear** | UP+B | A thrown spear that sticks in the first wall it reaches and becomes a 16×8 **one-way platform** (class 9, the vanilla solid-platform contact `$38:$8F96`) for 240 f (tune). Max 2. If it hits an enemy first, it deals 2 and makes no platform | 3 | 2 |
| Synergy: **Pogo** (Power) | hold DOWN in the air | Rock rides the spear point-down (the DuckTales pogo; Capcom, 1989). **On an enemy**: 3 damage and a bounce (vy `$FB.00`, or `$FA.CC` with A held). **On spikes**: a safe bounce that costs 1 energy per bounce; at 0 energy spikes kill as usual. On a boss: the Y.SPEAR cell. On the floor: a normal landing | 1 per spike bounce | 3 |

Tags: tap [engine-ok] + pierce [new-code] S; Wall Spear [new-code] S, [new-art] 2 tiles; Pogo [new-code] M, [new-art]
pose (2 frames). All Must.

> Y.SPEAR - "UP+B: a spear that stays in the wall. POWER: hold DOWN in the air. Spikes are only a problem for people
> without spears."

### 3.3 W.STORM (Wind, slot 2, class 6)

Vanilla: `$82`, attack `$62`, cost 1, mook 2. It is Flame Man's weakness. Wind Man takes only one hit from it per
vanilla quirk (stages_b.md).

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Vanilla tornado | 1 | 2 |
| Alt: **Updraft** | UP+B | A 16×64 updraft column in front of Rock for 150 f. Inside it Rock's gravity becomes −0.5 px/f² until vy reaches −2.0 px/f, so he rises to the column top. It is a Normal-form climbing tool, the same idea as the vanilla updraft floor types A/C. Enemies inside take 1 per 8 f | 3 | 1 / 8 f |
| Synergy: **Tailwind** (Jet) | B in flight | The tornado peels off behind Rock. For 90 f the fuel does not drain and the flight X speed is ×1.5 | 4 | (2 to what the tornado hits) |

Tags: Updraft [new-code] S, [new-art] 4 tiles; Tailwind [new-code] S. Must.

> W.STORM - "UP+B: a column of wind you can ride. In flight it pushes you instead. Wind Man says it was his idea."

### 3.4 B.ATTACK (Blizzard, slot 3, class 7)

Vanilla: `$83` spawns 4 × `$8E` in a spread, attack `$72`, cost 3, 2 per flake. It needs player slots 1-4 empty. It
kills the fire robots `$2A/$2C` outright (thematic table). It is Plant Man's weakness.

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | 4-flake spread (vanilla) | **2** (vanilla 3) | 2 per flake |
| Alt: **Cold Snap** | UP+B | One slow snowflake (2 px/f). The first normal enemy it touches is **frozen for 150 f**: its AI stops (the frozen tick, SYS-CMB-3), it turns ice-blue, and its class becomes 9 (solid platform), so **Rock can stand on it** and touching it is harmless. It still takes damage. A boss takes 1 and is not frozen. Fire enemies die (vanilla table). Types in NOFREEZE (BG bosses, big parts) just take 1 | 2 | 1, plus the freeze |
| Synergy: **Snow Bomb** (Jet) | B in flight | The 4 flakes fall straight down in a 32-px spread at 3 px/f | 2 | 2 per flake |

The cost cut from 3 to 2 is because the flakes no longer stack on bosses: i-frames eat the extra flakes. The weapon is
judged by its crowd value.

Tags: Cold Snap [new-code] M (freeze + class swap), [new-art] ice palette only. Snow Bomb [new-code] S. Must.

> B.ATTACK - "UP+B: one careful snowflake. Whatever it touches holds still and holds you up. Please wipe your feet."

### 3.5 F.BLAST (Flame, slot 4, class 8)

Vanilla: `$84`, attack `$84`, cost 1, mook 4. It breaks collision `$D` and kills the snow robot `$4D` outright. It is
Blizzard Man's weakness.

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Vanilla fireball → floor pillar. **It ignites oil** through vanilla `$3E:$DDFC` (open question: whether vanilla already does this for the player's flame). Enemies killed by oil the player lit score as HAZARD (class 4) | 1 | 4 |
| Alt: **Flare** | UP+B | A 16×80 fire column straight up from Rock for 20 f; 2 per 8 f to enemies. It melts F.BLAST blocks (`$D`) above, and lights "fuse" objects that venues may place | 2 | 2 / 8 f |
| Synergy: **Burning Knuckle** (Power) | hold B (45 f, like the punch), release | A flaming full punch: attack `$84` (class 8, so the F.BLAST boss cell). It breaks both `$B` and `$D` blocks and ignites oil it touches. A tap in Power form still throws a normal fireball | 2 | 4 |

Tags: Flare [new-code] S, [new-art] 3 tiles; Burning Knuckle [new-code] S, [new-art] palette + 2 tiles. Must.

> F.BLAST - "UP+B sets the ceiling on fire. POWER: hold B. Fire insurance not included in the entry fee."

### 3.6 PLANT.B (Plant, slot 5, class 9)

Vanilla: `$85` spawns 4 orbiting leaves `$8D`, attack `$94`, cost 4, mook 4. One hit removes all four; it deletes enemy
bullets (class 4, `$38:$9028`). It does **0 to every boss but Tomahawk** (4).

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Orbiting barrier as in vanilla, but it **survives 2 contacts** (enemy or bullet) instead of 1. It lasts until broken or 600 f (tune) | **3** (vanilla 4) | 4 per contact |
| Alt: **Petal Shot** | UP+B while a barrier is up | The 4 leaves fly off in a forward fan (±15°, ±35°) | 0 (spends the barrier) | 2 each |
| Synergy: **Petal Storm** (Jet) | B in Jet form | Radius ×1.6 (tune). For 180 f bullets are deleted without breaking it; it breaks after 3 enemy contacts. It is built for bullet-curtain set pieces such as a shmup venue | 4 | 4 per contact |

Against bosses the barrier now does its PLANT.B cell (neutral 2/30) instead of vanilla's 0. That is the BRIEF's "every
weapon useful".

Tags: [new-code] S each. Must.

> PLANT.B - "Two hits now, by popular demand. UP+B throws the petals. In flight, it blooms."

### 3.7 KNIGHT.C (Knight, slot 6, class A)

Vanilla: `$86`, attack `$A3`, cost 1, mook 3, two on screen. It is Centaur Man's weakness.

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | The mace flies out and returns (vanilla) | 1 | 3 |
| Alt: **Hold** | keep B held after the throw | The mace stops at its farthest point and hangs there while B is held, then returns. It hits what touches it (3 per 8 f) and **catches pickups, PARTs and envelopes**, which ride back to Rock (the 4MI Ring precedent) | 1 per 30 f held (min 1) | 3 / 8 f |
| Synergy: **Morning Star** (Power) | B in Power form | A giant 32×32 flail. It **breaks cracked blocks (`$B`) with no charge**, reflects enemy bullets on its outward path (the parry handler; it keeps class A) and passes Knight Man's shield | 2 | 4 |

Tags: Hold [new-code] S; Morning Star [new-code] M, [new-art] 4 tiles. Must.

> KNIGHT.C - "Hold B and it waits for you, like a good mace. POWER: bigger. Much bigger."

### 3.8 SILVER.T (Tomahawk, slot 7, class B)

Vanilla: `$87`, attack `$B3`, cost 1, mook 3, two on screen. It is Yamato Man's weakness, and the Wily Machine's and
Capsule's (4).

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Thrown in an upward arc (vanilla) | 1 | 3 |
| Alt: **Feather Fan** | UP+B | Three feathers (Tomahawk Man's own attack) fanned at 30°/45°/60° up-forward | 1 | 2 each |
| Synergy: **Dive Throw** (Jet) | B in flight | Thrown 45° down-forward at 1.5× speed | 1 | 3 |

Tags: [new-code] S, [new-art] feather 2 tiles. Must.

> SILVER.T - "UP+B: three feathers, no waiting. From the air it goes down, which is where the enemies are."

### 3.9 C.FLASH (Centaur, slot 8, class C; vanilla spelling C.FLRSH kept on the YOU GET card, BRIEF §6)

Vanilla: `$88` latches `$C4` into every class 1/3/F object, flashes, then waits 16 f. Cost 4, mook 4 screen-wide. It
does 0 to every boss but Wind Man (4).

| | Input | Behaviour | Cost | Mook dmg |
|---|---|---|---|---|
| Tap | B | Screen flash (vanilla). Bosses take their C.FLASH cell. With **REDUCED FLASHES** on, a 2-step palette darken replaces the white | 4 | 4 to all on screen |
| Alt: **Time Stop** (Flash Man nod, RM2) | UP+B | For 90 f every enemy object (slots 8-`$15`) and enemy bullet freezes; the frozen tick still applies damage. **Bosses freeze for at most 45 f**, then ignore Time Stop for 120 f. **Centaur Man is immune** (visible special case). Darker palette; the music keeps playing | 7 | - |
| Synergy: **Time Fist** (Power) | B in Power form | A 60-f Time Stop in which **B is always the punch and every punch is a full punch** (`$24`: 4 to mooks, breaks `$B`) | 6 | 4 per punch |

Tags: Time Stop [new-code] M (needs SYS-CMB-3); Time Fist [new-code] S. Must. The announcer's "TIME, STOP!" is a
story.md line.

> C.FLASH - "UP+B stops the clock. Not his, though. POWER: punch the moment."

### 3.10 MAGNET BEAM (H1 reward, slot 9, class D) [new-code] M, Must; [new-art] beam tiles

Slot 9 was vanilla's BEAT weapon. Beat becomes the pit rescue (§10), so the slot, its energy byte `$0691` and its
class D are free. This is an MM1 tribute and a nod to CX's Instant Floor.

| | Input | Behaviour | Cost |
|---|---|---|---|
| Build | hold B | A beam grows forward from Rock's hand at 4 px/f. On release, or at 64 px, it freezes into an 8-px-tall solid platform (class 9) for 240 f, blinks for 30 f and vanishes. **Max 3 beams** (CX's Instant Floor limit) | 1 per 16 px (1-4) |
| Alt: **Magnet** | hold UP+B | While held, pickups, PARTs and envelopes within 80 px drift toward Rock at 2 px/f | 1 per 60 f |
| Damage | | none: beams pass through enemies (class D has no damage cell; M.BEAM is not a VARIETY category) | |

There is no synergy (BRIEF: the 8 synergies are for the 8 boss weapons). **Emergent and allowed**: Jet + M.BEAM. Land
on a beam in mid-air and the fuel regenerates. Energy limits it to about 7 beams per bar. Venues that must stop it use
floor type E (no thrust) or ceilings.

> M.BEAM - "Hold B to build. Let go to stop. Three at a time, because the museum only had three in stock."

### 3.11 Break Man's moveset (the tag partner, §11) [new-code] L, Should

His design brief: no forms, a different body, buster only.

| | Break Man | Rock (for comparison) |
|---|---|---|
| HP | **20** (own bar), full on every call | 27 |
| Walk | 1.50 px/f (`$01.80`) | 1.297 |
| Jump | vy `$FA.4C` (−5.70 px/f) → peak ≈ 64 px | 51 px |
| Slide | yes (Rock's slide code) | yes |
| Tap shot | `$E1` (class E), 1 to mooks, 3 on screen | buster `$11` |
| **Break Shot** | hold B 60 f → a big shot, `$E4`: 4 to mooks, flies on through what it kills, **breaks cracked blocks (`$B`)** | full charge 90 f, 3 |
| **Shield** | while airborne and not shooting, enemy bullets (class 4) that touch the front half of his box are deleted (the PLANT.B bullet-delete path); bodies still hurt | - |
| **Double knockback** | knockback 28 px over 30 f (Rock: 14 px). Same 60 f of blink afterwards | 14 px |
| Weapons, forms, chips | none. Body chips (Spike Guard, Shock Absorber, Iron Helmet, Last Stand) apply to Rock only. Economy chips (Balancer, Exchanger, Judge's Favor) still work | |

Why buster only:

- A weaponless body is what makes the call a *change of pace* rather than a better Rock.
- Weapon energy stays Rock's resource.
- It saves a second fire dispatch.
- Break Man earns his keep through the Break Shot, which has its own short boss i-frames (§4), the higher jump and
  the shield.

---

## 4. The combat model: "the judges like variety"

### 4.1 What vanilla does (measured)

- **Robot Masters** [seen, ds `iframes.py`]: after *every* hit, by any weapon, the boss blinks for **60 frames**
  (`$31:$9A01 LDA #$3C / STA $0640`).
  - Blizzard: buster, F.BLAST (weak) and Y.SPEAR all landed exactly 60 f apart under 4- and 6-frame refire. So did
    Knight + Y.SPEAR and Flame + W.STORM.
  - The blink is 2 frames hidden / 2 frames shown.
  - Damage cells (`$31:$9A45`): weakness 4, most weapons 1, PLANT.B and C.FLASH 0, buster 1, charge 3. The full
    punch is special-cased to 2 (`$9AD6`).
  - Best-case vanilla kills (28 HP): weakness 7 × 60 = **420 f (7 s)**; buster 28 × 60 = **1,680 f (28 s)**; any
    other weapon also 1,680 f.
- **Fortress bosses** [seen, ds `iframes2.py`: Mr. X 2, Mr. X 4, Wily 2]: **32 frames** after every hit (`$05DF`),
  damage from `$3F:$EFE4`. The full punch does 4 there (the class-1 low-nibble rule).
- **Normal enemies** [seen, ds]: **no i-frames**. A buster fired every 4 frames into a HP-15 enemy hit every 4 frames.
  The shot vanishes unless it kills (`$38:$9067`).
- **Rock** [seen, ds]: 30 f of knockback (14 px), then 60 f of blinking. Contact damage = the enemy's low nibble.

So vanilla's weakness is pure damage (4 vs 1), and every boss hit costs the same 60 frames. The result is a buster that
is as good as any non-weak weapon, and weapons that are pointless against bosses.

### 4.2 The GP model

Two tables, **damage** and **i-frames**, per boss row × source column. The 4MI model, credited in-game in the Museum
and in the readme. Damage stays 1-4. The weakness lives mostly in the i-frames.

| Grade | Damage / i-frames | Meaning | Reaction |
|---|---|---|---|
| **W**eak | **4 / 16** | the vanilla weakness, kept | WEAK! pop, stagger, announcer (§5) |
| **G**ood | 3 / 20 | a second, thematic answer | short blink |
| **N**eutral | 2 / 30 | "any special weapon fights decently" (4MI) | |
| **R**esisted | 1 / 45 | worse than a charged buster | after 3 in a row the announcer hints |
| **O**wn weapon | 1 / 60 | only in refights | Could: own reaction (§4.6) |
| **BUSTER** | 1 / 60 | vanilla feel, unchanged | the long blink *is* the information |
| **CHARGE** | 3 / 60 | vanilla | |
| **PUNCH** tap/half | 2 / 40 | Power's free option | |
| **PUNCH★** full | 3 / 30 | vanilla 2 → 3: Power is the "no-energy" boss form, but it is close range | |
| **FIST** (Super) | 3 / 40 | weaker than PUNCH★ by design | |
| **PARRY** | 2 / 20 | rewards the skill | |
| **BREAK** / **BREAK★** | 1 / 40, 3 / 40 | the partner's buster is better than Rock's, as it should be | |
| **M.BEAM**, **HAZARD** | 0 | utilities. Bosses ignore player-lit oil, so no cheese | |

**Why 16 frames for a weakness and not 4MI's 1-8.** A refire rate of about 12-16 f is typical for RM6's
one-at-a-time weapons. A 16-f window means a well-placed weakness weapon lands every shot that connects, so the
weakness feels like 4MI's ("the boss melts"), but the boss can't be drained by a held hitbox. Bright Man's 1-frame
overload in 4MI is a deliberate special case, not the norm. Best-case weakness kill: 7 × 16 = 112 f. In practice the
boss pattern decides, about 3-5 s.

**Why the buster stays at 60.** It is exactly vanilla. A buster-only player loses nothing compared with RM6. Every
weapon got better, so the carrot is in the weapons, not a stick on the buster. The BRIEF's "≈ 60, gentler than 4MI's
127" is met.

**Best-case frames to kill 28 HP** (every hit lands when the i-frames end; refire assumed 12 f where not stated):

| Source | Frames | Seconds | vs vanilla |
|---|---|---|---|
| Weak (4/16) | 112 | 1.9 | 420 |
| Good (3/20) | 200 | 3.3 | 1,680 |
| Neutral (2/30) | 420 | 7.0 | 1,680 |
| PUNCH★ (3/30, 45-f charge) | 450 | 7.5 | 1,260 (vanilla 2 / 60, charge 45) |
| PUNCH tap (2/40, 32-f fist) | 560 | 9.3 | 840 |
| FIST (3/40, 45-f charge + flight) | ≈ 600 | 10 | - |
| CHARGE (3/60, 90-f charge) | 900 | 15 | 900 |
| Resisted (1/45) | 1,260 | 21 | 1,680 |
| BUSTER tap (1/60) | 1,680 | 28 | 1,680 |

Energy is the real limit on the good options:

- Neutral needs 14 hits: half a bar of a cost-1 weapon, more than a bar of B.ATTACK, and *impossible* with C.FLASH
  (cost 4).
- The weakness needs 7 hits: a quarter bar.

So mixing weapons is both the fastest and the cheapest way to fight. That is the premise.

### 4.3 Table 1: damage, the 8 champions (rows = source, columns = boss)

Assignments:

- **W** = vanilla weakness cycle (Flame > Blizzard > Plant > Tomahawk > Yamato > Knight > Centaur > Wind > Flame, read
  "F.BLAST beats Blizzard"…).
- **G** and **R** are two more permutations. Each weapon is W for one champion, G for one, R for one, own for one and N
  for four. No weapon is worse overall than another.

| Source | Blizzard | Wind | Plant | Flame | Yamato | Tomahawk | Knight | Centaur |
|---|---|---|---|---|---|---|---|---|
| BUSTER (tap, half, Jet) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| CHARGE | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| PUNCH (tap, half) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| PUNCH★ (full) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| FIST (Super) | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| PARRY | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| Y.SPEAR | 2 | 3 G | 2 | 2 | 1 own | 2 | **4 W** | 1 R |
| W.STORM | 1 R | 1 own | 2 | **4 W** | 2 | 3 G | 2 | 2 |
| B.ATTACK | 1 own | 2 | **4 W** | 3 G | 2 | 1 R | 2 | 2 |
| F.BLAST | **4 W** | 2 | 3 G | 1 own | 2 | 2 | 1 R | 2 |
| PLANT.B | 2 | 1 R | 1 own | 2 | 3 G | **4 W** | 2 | 2 |
| KNIGHT.C | 3 G | 2 | 2 | 2 | 1 R | 2 | 1 own | **4 W** |
| SILVER.T | 2 | 2 | 2 | 1 R | **4 W** | 1 own | 2 | 3 G |
| C.FLASH | 2 | **4 W** | 1 R | 2 | 2 | 2 | 3 G | 1 own |
| M.BEAM, HAZARD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BREAK | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| BREAK★ | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |

Thematic reading of G and R (all tunable):

| Boss | Good (G) | Resisted (R) |
|---|---|---|
| Blizzard | KNIGHT.C: a mace smashes ice | W.STORM: a blizzard enjoys wind |
| Wind | Y.SPEAR: jams the fan | PLANT.B: leaves get blown away |
| Plant | F.BLAST: the vanilla second weakness, 2 in `$9A45`, promoted | C.FLASH: photosynthesis |
| Flame | B.ATTACK: ice puts out fire, as the vanilla thematic table already says for the fire robots | SILVER.T: a wooden haft burns |
| Yamato | PLANT.B: vines tangle armour joints | KNIGHT.C: armour vs armour |
| Tomahawk | W.STORM: a dust devil on a cowboy | B.ATTACK: desert heat |
| Knight | C.FLASH: a flash goes around a shield, as vanilla C.FLASH latches class-3 shields | F.BLAST: plate armour is heat-proof |
| Centaur | SILVER.T: a hunter's axe | Y.SPEAR: hooves kick spears away |

### 4.4 Table 2: i-frames (frames), the 8 champions

| Source | Blizzard | Wind | Plant | Flame | Yamato | Tomahawk | Knight | Centaur |
|---|---|---|---|---|---|---|---|---|
| BUSTER (tap, half, Jet) | 60 | 60 | 60 | 60 | 60 | 60 | 60 | 60 |
| CHARGE | 60 | 60 | 60 | 60 | 60 | 60 | 60 | 60 |
| PUNCH | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| PUNCH★ | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| FIST | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| PARRY | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Y.SPEAR | 30 | 20 | 30 | 30 | 60 | 30 | **16** | 45 |
| W.STORM | 45 | 60 | 30 | **16** | 30 | 20 | 30 | 30 |
| B.ATTACK | 60 | 30 | **16** | 20 | 30 | 45 | 30 | 30 |
| F.BLAST | **16** | 30 | 20 | 60 | 30 | 30 | 45 | 30 |
| PLANT.B | 30 | 45 | 60 | 30 | 20 | **16** | 30 | 30 |
| KNIGHT.C | 20 | 30 | 30 | 30 | 45 | 30 | 60 | **16** |
| SILVER.T | 30 | 30 | 30 | 45 | **16** | 60 | 30 | 20 |
| C.FLASH | 30 | **16** | 45 | 30 | 30 | 30 | 20 | 60 |
| M.BEAM, HAZARD | - | - | - | - | - | - | - | - |
| BREAK | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| BREAK★ | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |

The flash is the boss blink, kept at vanilla's 2-hidden/2-shown rhythm for the whole i-frame time:

- a 16-f flicker reads as a "stutter" (4 blinks);
- 60 f reads as the familiar long blink (15 blinks).

That is BRIEF §5.1's "readable on screen" without new art. REDUCED FLASHES does not change the blink (it is
information); it only removes the white WEAK flash (§5).

### 4.5 Placeholder rows: fortress, legacy, rival, exhibition, mid-bosses

These bosses belong to fortress.md, venues_*.md and story.md. The values below are **defaults those docs may
override**. Cells are "damage / i-frames".

There are two families:

- **Machines** (BG-drawn or vehicle bosses) keep vanilla's fortress base of **32 f** for the buster. The full punch
  does **4** to them, vanilla's "Power is the fortress weapon" rule (fortress.md §11), kept on purpose.
- **Robots** (Bass, Dark Man) use the champion scale.

| Source | Grand Pi-kun (Opening) | Bass β (Semifinal, W2) | H1 Yellow Devil MK-VI | H2 Mecha Dragon MK-VI | H3 Gamma MK-VI phase 1 / phase 2 (head) | H4 Cossack Catcher MK-VI | H5 Dark Man MK-VI | W3 machine | W3 Wily Capsule | E1-E4 guests (rule bosses) | Mid-boss default |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BUSTER | 1/30 | 1/40 | 1/32 | 1/32 | 1/32 / 0 | 1/32 | 1/60 | 1/32 | 1/32 | 1/32 | 1/20 |
| CHARGE | 3/30 | 3/40 | 3/32 | 3/32 | 3/32 / 0 | 3/32 | 3/60 | 3/32 | 3/32 | 1/32 | 3/20 |
| PUNCH | - | 2/30 | 2/32 | 2/32 | 2/32 / 2/30 | 2/32 | 2/40 | 2/32 | 2/32 | 1/32 | 2/16 |
| PUNCH★ | - | 3/30 | **4/24** | **4/24** | 4/24 / **4/12** | **4/24** | 3/30 | **4/24** | **4/24** | 1/32 | 4/16 |
| FIST | - | 3/30 | 3/32 | 3/32 | 3/32 / 3/20 | 3/32 | 3/40 | 3/32 | 3/32 | 1/32 | 3/16 |
| PARRY | - | 2/20 | 2/20 | 2/20 | 2/20 / 0 | 2/20 | 2/20 | 2/20 | 2/20 | 1/32 | 2/16 |
| Y.SPEAR | - | 2/24 | 3/16 G | 2/24 | 2/24 / 0 | **4/12 W** | 2/30 | 1/32 R | 2/24 | 1/32 | 2/16 |
| W.STORM | - | 2/24 | 2/24 | 2/24 | **4/12 W** / 0 | 3/16 G | 2/30 | 2/24 | 2/24 | 1/32 | 2/16 |
| B.ATTACK | - | 2/24 | 2/24 | 2/24 | 3/16 G / 0 | 2/24 | 2/30 | 2/24 | 2/24 | 1/32 | 2/16 |
| F.BLAST | - | 2/24 | 2/24 | 1/32 R | 2/24 / 0 | 2/24 | **4/16 W** | 2/24 | 2/24 | 1/32 | 2/16 |
| PLANT.B | - | 2/24 | 1/32 R | 2/24 | 2/24 / 0 | 2/24 | 3/20 G | 2/24 | 2/24 | 1/32 | 2/16 |
| KNIGHT.C | - | 2/24 | 2/24 | **4/12 W** | 2/24 / 3/20 (Morning Star only) | 1/32 R | 2/30 | 3/16 G | **4/12 W** | 1/32 | 2/16 |
| SILVER.T | - | 2/24 | 2/24 | 3/16 G | 2/24 / 0 | 2/24 | 1/45 R | **4/12 W** | 3/16 G | 1/32 | 2/16 |
| C.FLASH | - | 2/24 | **4/12 W** | 2/24 | 1/32 R / 0 | 2/24 | 2/30 | 2/24 | 1/32 R | 1/32 | 2/16 |
| BREAK / BREAK★ | - | 1/40, 3/40 | 1/32, 3/24 | 1/32, 3/24 | 1/32, 3/24 / 0 | 1/32, 3/24 | 1/40, 3/40 | 1/32, 3/24 | 1/32, 3/24 | 1/32 | 1/20, 3/16 |
| **Rule** | HP 14 (tune). A charge tutorial: the buster is all you own | **Adaptive armour (SC6)** | **The SELECT trick (SC7)** | | **Phase 2: punches only (SC5)** | | | Vanilla homage: SILVER.T was the Wily Machine 6's weakness, KNIGHT.C its second | Vanilla homage: the Capsule ignored C.FLASH | The arena mechanic does the real damage (4/12). Weapons only chip | Venue mid-bosses unless their doc says otherwise |

Notes:

- The legacy weaknesses echo their home games where the GP arsenal allows: Yellow Devil fell to a beam (C.FLASH);
  Mecha Dragon to a thrown, returning weapon (KNIGHT.C) [guess on the MM2 fact; fortress.md checks]; Gamma's head to a
  body blow (punches, the Top Spin nod).
- The W2 bracket rush refights the champions with Table 1/2, own-weapon cells included.

### 4.6 Special cases, in visible code (CX lesson 7: never by table fall-through)

| Id | Case | Rule | Tags | Tier |
|---|---|---|---|---|
| SC1 | Knight Man's shield (class 3, `$38:$90A2`) | Frontal shots reflect, except PUNCH★, Morning Star, Time Fist, PARRY reflections, BREAK★ and C.FLASH (latched directly, as in vanilla). A PUNCH★, Morning Star or BREAK★ hit on the shield **breaks his guard for 180 f** (tune); venues owns the animation | new-code S | Must |
| SC2 | Centaur Man vs Time Stop | Immune to Time Stop and Time Fist's stop; announcer "He galloped right through it!" | new-code S | Should |
| SC3 | Plant Man vs C.FLASH | "Photosynthesis": the first C.FLASH of each fight **heals him 2** (the bar rises, with a "?!" pop). After that, R 1/45 | new-code S | Could |
| SC4 | Own weapons (refights only) | Each champion's own weapon: 1/60 plus a reaction. Blizzard reflects the flakes; Wind is spun faster (vanilla's "one hit only" W.STORM quirk, now on purpose); Plant grows; Flame absorbs (+2); Yamato parries; Tomahawk catches the axe and throws it back; Knight catches the mace; Centaur ignores the flash | new-code M | Could |
| SC5 | Gamma MK-VI phase 2 | Only PUNCH★, Time Fist punches (4/12) and Morning Star (3/20) hurt the head. Everything else dinks (`$27`). A telegraphed Top Spin nod: the plaque says "THE HEAD RESPECTS ONLY A FIST" | new-code S | Must (H3 is Must) |
| SC6 | Bass β adaptive armour | The 3rd consecutive damaging hit from the same column makes that column 1/45 until a *different* column hits him. Announcer: "He's adapting!". In W2 the armour starts adapted to the column the player used most in the Semifinal duel (1 saved byte). The rival literally punishes a one-weapon player: the premise in one rule | new-code S | Must |
| SC7 | Yellow Devil MK-VI "SELECT trick" | A nod to RM1's famous pause bug: a weapon swap within 2 frames of a WEAK hit clears the eye's i-frames, once per eye opening. Hinted in the H1 plaque only ("SOME TRICKS ARE A SELECT FEW") | new-code S | Could |

### 4.7 SYS-CMB-2: normal enemies [engine-ok] + [new-code] S, Must

- **Damage = the low nibble of the shot's attack byte** (vanilla `$E9D7`), as listed per weapon in §3. Fixed damage
  per weapon is already vanilla.
- **Mook HP stays vanilla** (AI header byte AI-2; 0-5 for most).
- **No i-frames on hit**, as in vanilla [seen, ds], **except lingering hitboxes**: Updraft, Flare, the held mace,
  Petal Storm, the Pogo and Morning Star. A given enemy takes a lingering hitbox at most once per **8 f**, through a
  per-slot WRAM re-hit timer. Without it a lingering box would deal damage every frame.
- **Thematic one-shots.** Vanilla has 3 per-class tables (`$3F:$EB46/$EB56/$EB66`): B.ATTACK kills Knight's blue-hall
  enemies and the fire robots; F.BLAST kills the snow robot and walkers. GP keeps them and adds one table per venue
  "featured enemy" family (8 in all). Each names one weapon that kills outright. That weapon must come from *another*
  venue. Those kills drop PARTs (§9.3). The table index of the new classes: 2 = punch, 4 = hazard, D = M.BEAM
  (0 damage), E = Break Man.
- **Punch-only enemies** (`$3F:$EA99`: Metalls `$15/$18`, `$24`, `$A3`) accept any **full-power blow**: PUNCH★
  (`$24`), Morning Star, Time Fist, Burning Knuckle and BREAK★. Vanilla accepted only `$14`.

### 4.8 SYS-CMB-1, SYS-CMB-3: how it is built [new-code] M, Must

- **One lookup, `GP_BOSSHIT(row, col)`.**
  - It replaces `$31:$997D`'s class lookup (`$9A45 + 16*(stage&7) + class`), the full-punch special case `$9AD6` and
    the constant at `$31:$9A01` (`LDA #$3C / STA $0640`).
  - On the fortress side it replaces `$3F:$EF64`'s `$EFE4` lookup and its 32-f store into `$05DF`.
  - `row` comes from the boss's entry in the stage-attribute table (BRIEF §7.2; tech.md). `col` comes from LATCHSRC
    (§6.4).
- **Cell format:** 1 byte.
  - bits 0-2 = damage (0-7);
  - bits 3-6 = i-frame class (0: immune/dink, 1: 8, 2: 12, 3: 16, 4: 20, 5: 24, 6: 30, 7: 32, 8: 40, 9: 45, 10: 60,
    11: 90 f);
  - bit 7 = WEAK.
  - Size: 18 columns × about 26 rows ≈ 470 bytes.
- **The chart is generated from the source data** (CX lesson 7) by a build script (`tools/build/dmgchart.py`, tech.md)
  that prints the tables of this section. This doc's tables are the seed data.
- **The frozen tick (SYS-CMB-3).** Time Stop, Cold Snap and the WEAK stagger stop an object's AI.
  - Damage is applied victim-side, inside the AI (vanilla), so a frozen object would never process its hit latch.
  - The object loop (`$3F:$E438`) therefore calls, for each frozen slot, only that type's damage routine. The routine
    comes from a new 256-entry type → damage-routine table, seeded from engine.md's `dmgmap.json`: `$E9D7`, `$EA20`,
    `$EA6E`, `$EA99`, `$EAB7`, `$31:$997D`, `$EF64` or none.
  - The object is still drawn.

---

## 5. Weakness feedback (SYS-WK-1) [new-code] S, [new-art] 5 tiles, Must

BRIEF §5.1: a "WEAK!" pop, a stagger and a commentator line on the first weakness hit. Each fires on a cell with the
WEAK bit (§4.8):

1. **The WEAK! pop.**
   - A new object type (one of the 32 free ids, e.g. `$7B`) with 5 sprite tiles, W-E-A-K-!.
   - It spawns at the shot's position, rises 1 px/f for 24 f, and cycles yellow/white every 4 f.
   - At most one per boss per 30 f.
   - The same object shows "CRIT!" for criticals (§14, +3 tiles) and "?!" for SC3.
2. **The stagger.**
   - The boss's AI is frozen for **10 f** (the frozen tick keeps damage working), and its sprite shakes ±1 px every
     2 f. That is a hit-stop.
   - Only if **≥ 90 f** have passed since its last stagger. Otherwise 16-f i-frames plus 10-f staggers would stunlock.
   - **Unique reaction**: if the boss's AI table defines a "weak" entry, the stagger calls it instead of the generic
     shake. Examples: Blizzard's skis slip, Flame's head flame gutters, Knight drops his guard. The venue docs and
     art own those frames.
3. **The sound.** A new "crunch" SFX. Free ids exist: the SFX `$3D/$3E/$4D/$51` look unused (engine.md §5).
4. **The flash.** The boss palette goes white for 2 frames. Off under REDUCED FLASHES; the shake stays.
5. **The announcer.**
   - Event `EV_WEAK_FIRST`, once per fight → a commentator pop-up (story.md writes 1-2 lines per champion).
   - `EV_RESIST`: the 3rd resisted hit in a row → a hint line ("That's barely scratching him!").
   - `EV_IMMUNE`: the first dink. Vanilla's dink `$27` already plays.
6. **Memory** (Could). A save bit per boss row records "weakness found". The pause menu's weapon page then shows a
   ★ next to that weapon during that boss's fight. It is a scouting report you earned.

The i-frame blink length (16 vs 30 vs 60 f) is itself the second, quieter feedback (4MI's "read the weakness from the
flashing time").

---

## 6. The scorecard (SYS-SC-1) [new-code] M, Must

Every cleared stage is judged out of 100 (BRIEF §5.3): TIME 20, DAMAGE 20, VARIETY 25, SECRETS 20, STYLE 15. The
results screen (judges, slide-in rows, comments) belongs to meta.md; the formulas are here.

### 6.1 Counters (per run; reset at stage start, kept through deaths in the same run)

| Counter | Meaning |
|---|---|
| `T` | In-stage frames, counted while `$F0` = 0. Excludes pause, the boss bar fill (`$0642` = `$FF`) and the post-kill sequence. **Includes** death and respawn time (dying costs time) |
| `L` | HP lost by Rock or Break Man: damage after the multiplier, capped at the HP they had |
| `K` | Lives lost (pits, spikes, HP) |
| `CATS` | 16-bit set of scoring classes that killed a normal enemy **or** damaged a boss (§6.4) |
| `OWNED` | Classes the player can use at stage start (BUSTER always; PUNCH once Power is owned; each weapon owned; BREAK once he has joined) |
| `SECR` | Secret predicates met this run |
| `STY` | Style flags (§6.5) |
| `TANKS` | E-/W-tanks used this run |

A CONTINUE after a game over starts a new run. That run's lost progress is the game-over penalty; there is no E-tank
halving (CX) in GP.

### 6.2 Formulas

```
TIME     = 20                                    if T <= P
         = max(0, 20 - ceil(20 * (T - P) / P))   otherwise          (0 at twice the par)
DAMAGE   = max(0, 20 - ceil(L / 3) - 4 * K)                         (a full bar lost, no death = 11)
VARIETY  = floor(25 * min(|CATS|, Pv) / Pv),  Pv = min(5, |OWNED|)  (the par grows with the arsenal)
SECRETS  = floor(20 * sum(w found) / sum(w all))                    (a stage with no secrets scores 20)
STYLE    = 4*WEAK_FINISH + 4*BOSS_NO_HIT + 2*NO_TANKS + min(5, style acts)
```

Why each formula:

- **TIME** is relative to par, so short and long stages weigh the same.
- **DAMAGE** counts HP, not hits. A big boss hit costs more than chip damage. Deaths cost an extra flat 4, so a death
  with a full bar lost scores about 3-7.
- **VARIETY** has a par that grows: Pv = 1 in the first venue (buster only), 2-5 later, and 5 from the 4th weapon on.
  So nobody is punished for an early stage, and **a buster-only run still clears, it just earns less** (PLAN §1's
  carrot).
- **SECRETS** weights (default): secret exit 3, hidden room 2, behaviour-gated item 2, Beat plate 1, venue extras 1.
  The predicate list is the same one the judges' debrief walks (BRIEF §5.4, meta.md).

Calibration [guess, checked by playtest at M4]:

| Run | TIME | DAMAGE | VARIETY | SECRETS | STYLE | Total | Medal |
|---|---|---|---|---|---|---|---|
| Decent first clear: 30 % over par, 27 HP lost, Pv met, 2 of 7 secret weight, weak finish + 2 acts | 14 | 11 | 25 | 5 | 6 | **61** | Silver |
| Platinum | 20 | ≥ 18 (≤ 6 HP lost) | 25 | 20 | ≥ 12 | ≥ 95 | Platinum |

### 6.3 Pars

- The par `P` is a per-stage field in the stage-attribute table (BRIEF §7.2).
- **Rule for setting it**: P = 1.25 × the golden-movie reference route (normal exit, no deaths, a competent player),
  rounded up to 10 s. The golden movies exist from M0 (BRIEF §7.3), so pars are measured, not guessed.
- Placeholder pars until the routes exist **(tune)**: Opening 120 s, each venue 180 s, Semifinal 150 s, each
  Hall-of-Fame wing 200 s, W1 200 s, W2 300 s, W3 240 s, each Exhibition 90 s.
- VARIETY's par is Pv (above). DAMAGE has no par. The SECRETS par is "all".

### 6.4 Attribution: the shot class in the hit latch

Vanilla: a player shot touching an enemy copies its attack byte (`CCCC DDDD`, class/power) into the victim's hit latch
`$056C`. The victim's damage routine reads it and **clears it** (engine.md §2.1). The class nibble already separates
the eight weapons (5-C), but class 1 is shared by the buster, the charge, the Jet buster and all three punch levels.
Worse, `$13` is both the full buster and the half punch. GP therefore:

1. **Re-classes the player's shots**, so that *class = scoring category*.

   | Class | Category | Attack bytes |
   |---|---|---|
   | 1 | BUSTER | `$11` tap, `$12` half, `$13` full, Jet `$11` |
   | 2 | PUNCH | `$22`/`$23`/`$24` Power; `$22` Super tap; `$23` Super fist and parry reflections |
   | 4 | HAZARD | `$4x`: enemies killed by oil the player ignited, or crushed under a frozen enemy |
   | 5-C | the 8 weapons | unchanged class nibble. Alts and synergies keep their weapon's class |
   | D | M.BEAM | `$D0`; no damage, so never scores |
   | E | BREAK MAN | `$E1` tap, `$E4` Break Shot |

   Classes 2, 3, 4 and E are unused as *shot* classes in vanilla. Bosses' table entries for classes 0-4 and D-F are
   `$FF`, never reached. Enemy classes (the handler dispatch in `$38:$8FBF`) are a separate namespace, so nothing
   collides. Vanilla routines that test `$14` (`$EA99`, `$90A2`, `$31:$9AD6`) are rewritten to test `$24`.
2. **Keeps a copy of the latch.** At every latch store, GP also writes:
   - `LASTHIT[victim]`, the attack byte, which the damage routine does not clear;
   - `LATCHSRC[victim]`, the source column for §4 (bits 0-4), plus a synergy flag (bit 7) and an alt flag (bit 6).

   The latch stores are the handlers in `$38:$8FDF`: `$9021` (pass-through boxes), `$9067` (normal), `$90A2`
   (shield), `$9028` (bullets, for parries), plus C.FLASH's direct writes in `$38:$9E52`. Both arrays are 23 bytes of
   WRAM, one per object slot.
3. **Reads it where deaths converge.**
   - Normal enemies die by turning into the explosion type `$17` (`$30:$81C7`) or `$25`.
   - Robot Masters die through `$3F:$ED42`; fortress bosses through `$EF64`'s death path.
   - At those inits: `CATS |= 1 << (LASTHIT[slot] >> 4)`, the kill count, the multi-kill timer and the synergy-kill
     flag.
   - Custom deaths (the gorilla tank, the Mr. X 1 riders `$3B:$827A`, new GP enemies) must call the same hook.
     tech.md audits them with shadow6 coverage.
4. **Boss hits count too.** `GP_BOSSHIT` ORs the class into `CATS` on every damaging hit. Mixing weapons in the
   boss fight is exactly what the judges like, and it lets a pacifist (DOVE BADGE, §9) still score some VARIETY.

`CATS` is a set, so farming a respawning enemy with one weapon earns nothing extra. Vanilla's kill bitfield `$0650+`
already stops list enemies from respawning.

### 6.5 STYLE

| Item | Points | Rule |
|---|---|---|
| WEAK FINISH | 4 | The killing hit on the stage's scoring boss (a stage-attribute field) is a WEAK cell, **or** a synergy shot (a "form finish") |
| BOSS NO-HIT | 4 | No HP lost from the boss bar filling until the kill (Break Man included) |
| NO TANKS | 2 | No E-tank or W-tank used in the run |
| Style acts | 1 each, max 5 | PARRY (≥ 1 parry) · SYNERGY KILL · MULTI-KILL (2 kills by the same class within 8 f) · FROZEN STEP (stood on a frozen enemy) · CLOSE CALL (boss killed with Rock at HP ≤ 4) · TAG TEAM (Break Man scored a kill or a boss hit) · CRITICAL (if criticals ship) · VENUE ACT (one per venue, named by its doc: e.g. "won the quick-draw") |

### 6.6 Medals and pay

- **Medals:** Bronze ≥ 40, Silver ≥ 60, Gold ≥ 80, Platinum ≥ 95 (BRIEF).
- **Bonus bolts:** 0 / 10 / 20 / 40 / 60 for none / B / S / G / P **(tune)**.
- `PAY(run) = score + bonus(medal)`, at most 160 per stage.
- **Replays pay only the improvement:** `max(0, PAY(new) − PAY(best))`. So the total ever paid per stage = the best
  PAY. A stage cannot be farmed.
- Saved per stage: best score (7 bits), the medal's preset badge (2 bits: C/N/H/93) and the best PAY.
- Medal points for meta.md: B 1, S 2, G 3, P 4.

### 6.7 SYS-SC-3: secret tokens on replays [new-code] S, Must

A collected plate, chip capsule, PART or envelope does not respawn. Without a fix, a replay could never re-earn
SECRETS. On replays such objects spawn as a **token**:

- a small rotating judge's-pin sprite;
- touching it sets the secret predicate and gives nothing else.

Secret exits and hidden rooms are re-earned simply by taking them.

---

## 7. Bolts and the income model (SYS-ECO-1) [new-code] M, Must

Money is prize money (BRIEF §1). **Bolts never drop from enemies.** That and the improvement-only rule make the
economy grind-proof.

| Source | Bolts | Notes |
|---|---|---|
| Scorecard, first clear | score + medal bonus (≤ 160) | 22 stages |
| Scorecard, replay | the improvement only | |
| Sponsor envelope | 30, once per save | one in each venue's hidden room (8); fortress.md may add some (each one counts as a secret) |
| Exhibition first clear | 100 (tune) | owner: the Exhibitions doc |
| 1UP picked up at 9 lives | 10 ("fan tip") | no dead pickups |
| E-tank picked up while holding 4 | 20 | |

The counter caps at 999.

Income model (the prices in §8 are sized against it):

| Player | After 4 venues | After 8 venues | Full game (22 stages + 4 Exhibitions) |
|---|---|---|---|
| Typical (≈ 62 + Silver per stage, half the envelopes) | ≈ 390 | ≈ 780 | ≈ 2,200 |
| Completionist (Platinum everywhere) | ≈ 700 | ≈ 1,400 | ≈ 4,160 |

The 7 shop chips cost 1,090 in all. A typical player can afford 2-3 chips plus tanks by mid-game and the whole
catalogue around the Hall of Fame. Slots (2-6), not money, are the real limit late on.

---

## 8. Eddie's Pit Stop: stock and prices

Reached from the bracket screen (meta.md owns the UI). Stock unlocks by WINS, so money can't be front-loaded (PLAN
§2.5).

| Item | Price | Max held | Unlock |
|---|---|---|---|
| E-TANK | 40 | 4 | start |
| 1UP | 30 | lives 9 | start |
| SHOCK ABSORBER (chip) | 120 | - | start |
| SPIKE GUARD (chip) | 150 | - | start |
| CHARGE KIT (chip) | 120 | - | start |
| W-TANK (new: refills every weapon) | 50 | 2 | 3 wins |
| EXCHANGER (chip) | 100 | - | 3 wins |
| JUDGE'S FAVOR (chip) | 200 | - | 3 wins |
| JET TUNER (chip) | 150 | - | 4 wins (Jet owned; shown as "???" before) |
| ENERGY SAVER (chip, 2 slots) | 250 | - | 6 wins |
| GARAGE tab (crafting, §9.3) | free | - | the first PART owned |

- Prices do not change with difficulty. Difficulty lives in combat, not in the till. The 1993 preset closes the shop.
- **Why these prices:**
  - E-tank 40 ≈ half a Bronze clear.
  - The T0 chips (120-150) ≈ two decent clears each, bought around the 3rd-4th venue.
  - JUDGE'S FAVOR (200) is an investment that pays back after about 1,000 bolts of later earnings (≈ 12 stages). A
    real choice.
  - ENERGY SAVER (250, 2 slots) is the luxury.

---

## 9. Chips (SYS-CHP-1/2) [new-code] M, Must (framework)

### 9.1 The framework

- Chips are passive, one bit each: 15 chips in a 16-bit `CHIPS_OWNED`, and 16 bits of `CHIPS_EQ`.
- Equip and unequip them at the Pit Stop, or on the pause menu's CHIPS page, at any time. 4MI items are always on;
  GP lets you choose because the slots are limited.
- Each chip costs 1 slot. ENERGY SAVER and LAST STAND cost 2.
- Each chip has a **help page** (≤ 3 lines × 28 characters, EN below; the JP text pass belongs to story.md). As in
  4MI, **some pages are cryptic on purpose**, marked ◊.
- Body effects (knockback, spikes, damage reduction, Last Stand) apply to Rock only, never to Break Man.

### 9.2 The fifteen chips

| # | Chip | Exact effect | Source | Slots | Tier |
|---|---|---|---|---|---|
| 1 | **ENERGY BALANCER** | A weapon-energy pickup the equipped weapon can't take (buster, punch or Jet buster equipped, the weapon full, or Break Man in) goes to the **owned, non-full weapon with the least energy** (ties: menu order). If all are full, it falls through to the base rule (§12.2). This is the vanilla behaviour as measured by the critic (buster equipped → lowest weapon; big +10, small +2), extended to the "weapon full" case | **Found**: the Tomahawk venue, re-homing vanilla room 1C behind a cracked block (venues doc places it). Vanilla object `$8A` | 1 | Must |
| 2 | **SHOCK ABSORBER** | No knockback: the 30-f hurt state is skipped and Rock keeps control. The 60 f of blink are unchanged, so total safety per hit drops from 90 f to 60 f (the trade-off) | Shop 120 | 1 | Must |
| 3 | **SPIKE GUARD** | Once per life, touching spikes at HP ≥ 2 sets HP to 1 instead of killing; 120 i-frames (4MI SHOCK GUARD, which was unlimited) | Shop 150; free and slotless in CASUAL | 1 | Must |
| 4 | **CHARGE KIT** | Buster charge thresholds 36/90 → 24/60 f. Power, Super and Burning Knuckle 45 → 30 f. Break Man unaffected | Shop 120 | 1 | Must |
| 5 | **JET TUNER** | Fuel 19 → 27 units (108 f of flight). Regen rate unchanged (+1 per 2 f) | Shop 150 | 1 | Should |
| 6 | **EXCHANGER** | A life pickup at full HP becomes weapon energy 2:1 (small 1, large 5), routed by §12.2 (4MI's EXCHANGER, credited) | Shop 100 | 1 | Should |
| 7 | **JUDGE'S FAVOR** | +20 % on every scorecard payout, replay improvements included (rounded down) | Shop 200 | 1 | Should |
| 8 | **ENERGY SAVER** | Weapon costs halved, rounded with a per-weapon carry bit: a cost-1 weapon charges every other shot; 3 → 2, 1, 2… | Shop 250 | **2** | Must |
| 9 | **IRON HELMET** | A hit of 2+ is halved (rounded up) on 1 frame in 8 (LFSR), and always at HP ≤ 4 (4MI's METALL'S HELMET, credited) | **Behaviour**: destroy 20 Metalls with full-power blows (§4.7) over the save. The 20th drops the helmet, "the Metall Union surrenders" | 1 | Should |
| 10 | **DOVE BADGE** | Normal enemies' contact damage −1 (minimum 1). Bosses are unaffected | **Behaviour**: clear any venue without destroying a normal enemy (bosses and mid-bosses excepted; HAZARD kills count as kills; frozen enemies don't). The judges' "sportsmanship" prize. That run's VARIETY can come only from boss hits: the trade-off is in the score | 1 | Should |
| 11 | **THERMO CORE** | Ice and oil floors behave as normal floor for Rock (no momentum, normal walk and jump). Burning oil still burns | **Craft**: SNOW + EMBER | 1 | Should |
| 12 | **SEED POD** | After 60 f with no input, +1 HP every 30 f up to max. Off while a boss bar is shown | **Craft**: GUST + SEED | 1 | Should |
| 13 | **LAST STAND** | Once per life, a hit that would kill at HP ≥ 2 leaves 1 HP. Pits and spikes excluded (4MI's SKULL AMULET, but once per life) | **Craft**: KATANA + CREST | **2** | Should |
| 14 | **LUCKY DICE** | Critical chance ×4 (§14). ◊ With criticals OFF: each scorecard payout has a 1-in-8 "LUCKY!" that doubles the medal bonus | **Craft**: FEATHER + SHELL | 1 | Should (Could if criticals are cut) |
| 15 | **Y-TURBO** | +1 damage on every hit against bosses (cap 4) and charges fill 2× faster. **The cost:** see §9.4 | **Moral**: Mr. Y's booth, for any one PART | 1 | Should |

Help pages (EN; ◊ = cryptic on purpose):

```
ENERGY BALANCER  Spare energy finds the emptiest tank.
                 The original. Accept no imitations.
SHOCK ABSORBER   No more flinching. You still blink,
                 you just blink standing up.
SPIKE GUARD      One spike, one second chance, per life.
                 The second spike is still a spike.
CHARGE KIT       Charges faster. The judges call it
                 "efficient". They mean it this time.
JET TUNER        Bigger tank, same Rush. Do not tell
                 him about the extra weight.
EXCHANGER        Life you can't use becomes energy you
                 can. Two for one. Eddie's math.
JUDGE'S FAVOR    The judges have been... persuaded.
                 +20% prize money. Nobody saw anything.
ENERGY SAVER     Every weapon sips instead of gulps.
                 Takes two slots. Worth it? Discuss.
IRON HELMET  ◊   Twenty of them signed it.
                 They seemed relieved.
DOVE BADGE   ◊   For a match won without a single
                 casualty. Some opponents noticed.
THERMO CORE      Ice holds still. Oil lets go. Your
                 floors finally behave.
SEED POD     ◊   Stand still and listen. Something is
                 growing back.
LAST STAND       Once per life, a fatal blow is only
                 almost fatal. Pits did not sign this.
LUCKY DICE   ◊   Roll it. If nothing happens,
                 roll it after the match.
Y-TURBO      ◊   Mr. Y guarantees results.
                 Mr. Y guarantees a lot of things.
```

### 9.3 SYS-CHP-3: PARTs and the garage (crafting, RM6-native) [new-code] M, [new-art] 8 icons, Should

**The RM6 root.** Vanilla already has per-class one-shot tables (`$3F:$EB46/$EB56/$EB66`):

- F.BLAST melts the snow robot `$4D`;
- B.ATTACK snuffs the fire robots `$2A/$2C`;
- B.ATTACK freezes Knight's blue-hall walkers `$2D/$75`.

These "thematic kills" are RM6's own crafting hint. GP turns them into recipes:

- **Each venue has one featured enemy family**, and it dies outright to **that venue's champion's weakness weapon**.
  - Blizzard's snow robot to F.BLAST: exactly vanilla.
  - Flame's featured enemy to W.STORM; Plant's to B.ATTACK; and so on around the cycle.
- The minions share the boss's weakness. That is an **in-stage tell** for the boss (CX lesson 6), and a reason to
  **come back later**: the weakness weapon always comes from another venue.
- **The first thematic kill of that family per save drops its PART**, a gear capsule stamped with the venue's
  letter. Later thematic kills drop a normal item. Vanilla's other one-shots (fire robots ← B.ATTACK, the blue hall)
  stay as plain one-shots.

| PART | Venue | Featured enemy (default; the venue doc may replace it) | Thematic weapon (= the champion's weakness) |
|---|---|---|---|
| SNOW | Blizzard | snow robot `$4D` (vanilla rule) | F.BLAST |
| GUST | Wind | the venue's fan or kite enemy | C.FLASH |
| SEED | Plant | the venue's flower or pod enemy | B.ATTACK |
| EMBER | Flame | Fire Telly `$2C` | W.STORM |
| KATANA | Yamato | samurai `$A2` | SILVER.T |
| FEATHER | Tomahawk | the venue's totem or vulture | PLANT.B |
| CREST | Knight | lance knight `$6E` | Y.SPEAR |
| SHELL | Centaur | seahorse `$C4` | KNIGHT.C |

**The garage** (a Pit Stop tab, free to use) builds chips from pairs:

| Recipe | Chip | Why the pair |
|---|---|---|
| SNOW + EMBER | THERMO CORE | ice and fire |
| GUST + SEED | SEED POD | wind carries seeds |
| KATANA + CREST | LAST STAND | the two warriors' honour |
| FEATHER + SHELL | LUCKY DICE | a gambler's feather and a lucky shell |

Owning one PART of a pair shows the recipe as "SNOW + ???". That is the in-menu hint (4MI: "once you find one by
accident it hints at the others").

### 9.4 SYS-CHP-4: Mr. Y's booth and Y-TURBO (the moral trade-off) [new-code] S, Should

The 4MI precedent: inhale Eddie, get the ENERGY SPLITTER, lose a friend. GP's version is **doping in a sports
tournament**.

- After the Semifinal (story.md fixes the beat), a shady booth appears at the edge of the bracket screen: "MR. Y
  PERFORMANCE PARTNERS". Mr. Y, unconvincingly disguised, offers the Y-TURBO chip for **any one PART**.
- He asks twice. The second time: "Break Man is watching, you know."
- The cost is permanent for that save:
  1. **The PART is gone.** PARTs are unique per save, so that pair's honest chip can never be crafted.
  2. **Break Man refuses to partner you.** His portrait in the pause menu reads "NO". His line: "You took Y's money.
     Fight your own matches."
  3. **Every medal earned while TURBO is equipped carries an asterisk** in the records (1 bit per stage).
  4. **The commentators notice.** Line: "Is that... a sponsor patch?".
  5. **The ending's CAPCOM TIMES headline changes** (story.md writes it, e.g. "CHAMPION'S CHIP UNDER INVESTIGATION").
- The judges' debrief never hints at the booth, like 4MI's Energy Splitter, which had no hint entry either.

---

## 10. Slots and Beat plates (SYS-BT-1) [new-code] M; slots Must, rescue Should

- **Slots** = 2 + one per Beat plate, max 6 (BRIEF §5.3). The vanilla plate count is exactly 4 (rm6 SUMMARY §4).
- **Plates** are in 4 venues: the vanilla four (B Tomahawk, E Yamato, A Knight, T Centaur) or re-homed by the venue
  docs.
  - GP places each plate as an object (simpler than vanilla's "boss killed in the second room" rule, `$3F:$F518`).
  - They are saved as 4 bits. On replays they become tokens (§6.7).
- **B-E-A-T complete → Beat joins as the pit rescue** (vanilla's BEAT weapon slot becomes MAGNET BEAM, §3.10). This
  is 4MI's "friends are mechanics", made friendlier:
  - **Trigger**: Rock falls into a pit with HP ≥ 5.
  - **Effect**: Beat swoops in and drops Rock on the **last safe ground**: the last position where Rock stood ≥ 8 f on
    a solid, non-hazard floor, recorded in WRAM.
  - **Cost**: **4 HP**, then 60 i-frames. No life is lost. No limit while HP ≥ 5.
  - CASUAL lends Beat from the start ("Beat on loan"). 1993: off.
- The 4MI precedent was 3 HP at HP ≥ 4. GP's 4/5 matches RM6's harsher contact damage (bosses hit for 4-5) **(tune)**.

---

## 11. The tag partner: Break Man (SYS-TAG-1) [new-code] L, Should

The moveset is in §3.11. These are the rules (BRIEF §5.6; CX's Quick Man pattern, credited):

| Rule | Value |
|---|---|
| Joins | at a story beat (story.md; mid-game, e.g. after the Semifinal). Save bit `BREAK_JOINED` |
| Call | pause menu → **SELECT** while his portrait shows ("Break Man: SELECT"). Rock beams out; Break Man beams in at the same spot with **20 HP** and his whistle jingle (2 s, [new-music] S) |
| Frequency | **once per life**: the flag resets at respawn and at stage start |
| Swap back | **START** (he has no pause menu). Rock beams back in with **the HP he left with**. Break Man's remaining HP is discarded |
| Break Man at 0 HP, or in a pit, or on spikes | he **retreats** ("Tch. Your turn."): no life is lost and Rock returns with his HP |
| Not allowed | while a boss bar fills; in the Opening; where a stage-attribute flag says NO TAG (set pieces whose physics assume Rock); while TURBO is owned (§9.4) |
| Pickups | life heals him; weapon energy routes as if the buster were equipped (§12.2); no tanks (no menu) |
| Scoring | his HP loss counts in `L`; his kills and boss hits are class E for VARIETY; the TAG TEAM style act |
| Tag gates | shutters stamped with **his yellow-scarf emblem** open only to Break Man. Every tag gate leads to optional content (BRIEF). The emblem is the tell (CX lesson 6) |

Why he retreats instead of costing a life: the call is meant to be used. A spare body that can cost a life gets saved
for emergencies, and then never used (CX's Quick Man is rarely seen in play). 20 HP plus double knockback keeps him
from being a better Rock.

---

## 12. Pickups and economy rules

### 12.1 Vanilla, measured [seen, ds `items.py`]

| Type | Pickup | Effect |
|---|---|---|
| `$38` | small life | +2 HP |
| `$39` | large life | +10 HP |
| `$49` | small weapon energy | +2 |
| `$4A` | large weapon energy | +10 |
| `$37` | 1UP | +1 life |
| `$1D` | E-tank | +1 |

**Drops** [code, ds]: when a normal enemy dies, its explosion (type `$17`, `$30:$81E8`) picks with `$3E:$CC54` (a
cumulative-weights pick against RNG `$DF`).

- First table `$30:$8212` = `1F E0`: **31/256 = 12.1 %** of kills drop something.
- After an LFSR step (`$3E:$C88D`), a second table `$30:$8214` = `18 5F 20 58 10` picks from `$30:$8219` =
  `39 38 4A 49 37`:

| Item | Share of drops | Share of kills |
|---|---|---|
| small life | 37.1 % | |
| small weapon | 34.4 % | |
| large weapon | 12.5 % | |
| large life | 9.4 % | |
| 1UP | 6.3 % | ≈ 0.76 % |

**Deaths** [seen, ds `jet.py`]: HP refills; **weapon energy does not** (Y.SPEAR 5 and W.STORM 0 stayed after a
respawn).

**Energy Balancer** (critic): with the buster equipped, a weapon pickup goes to the lowest weapon. Without the Balancer
it is wasted. With a weapon equipped it refills that weapon.

### 12.2 SYS-PU-1: GP routing [new-code] S, Must

A **weapon-energy** pickup:

1. If a weapon is equipped and not full, it goes to that weapon (vanilla).
2. Otherwise, with the BALANCER chip, it goes to the lowest non-full owned weapon.
3. Otherwise it becomes **HP at half value** (small +1, large +5; CX's rule, credited). If HP is full, it is wasted.

A **life** pickup:

1. It goes to HP.
2. At full HP with the EXCHANGER chip, it becomes weapon energy at 2:1, routed as above.
3. Otherwise it is wasted.

Why rule 3: vanilla wastes the pickup, which the critic saw. Turning it into HP removes dead pickups. The Balancer then
becomes a *choice* (energy instead of HP) rather than the only way not to waste a capsule. That is fair now that it
costs a slot.

### 12.3 Other rules

| Rule | Value | Tags | Tier |
|---|---|---|---|
| **Drops** (SYS-PU-2) | One byte selects the first weight (data only): NONE 0 / LESS 16 (6.3 %) / **NORMAL 40 (15.6 %)** / MORE 256 (every kill). The vanilla item mix is kept. NORMAL sits slightly above vanilla's 12.1 % because GP's weapons are used more (alts cost 2-7) | engine-ok + new-code S | Must |
| **Pit-crew refill** (SYS-PU-3) | On respawn after a death: NORMAL gives every owned weapon +max(4, ⌊missing/2⌋) (4MI's ENERGY CHARGER, credited); CASUAL refills them fully; HARD and 1993 give nothing (vanilla) | new-code S | Must |
| **Game over** | CONTINUE restarts the stage (vanilla) with the preset's lives, full weapons and the E-tank floor. No tank penalty: the lost run is the penalty | new-code S | Must |
| **E-tank** (SYS-PU-4) | heals +1 HP per **2** f (vanilla 4 f, `$38:$9537`): a full bar in 54 f instead of 108. Hold max 4 (shop cap) | new-code S | Should |
| **W-tank** (SYS-PU-4) | new pause-menu item beside the E-tank: refills every weapon. Hold max 2. Shop (3 wins) and rare hidden placements | new-code S, new-art 1 icon | Should |
| **Overflow** | a 1UP at 9 lives → +10 bolts; an E-tank at 4 held → +20 bolts | new-code S | Should |
| **Envelopes** | sponsor envelopes (+30 bolts) in hidden rooms (§7) | new-code S, new-art 1 | Must |

---

## 13. Difficulty and configuration (SYS-DIF-1/2/3)

### 13.1 Settings

Each setting is one byte in the system block (tech.md places it). Each is read at one place, the 4MI lesson:
"accessibility knobs belong in the combat code".

| Setting | Values | Read by |
|---|---|---|
| DAMAGE | ×0.5 / ×1 / ×1.5 / ×2 (round up, as in 4MI) | player hurt `$38:$8F72` |
| LIVES | 1-9 (start and continue) | new game / continue |
| E-TANK FLOOR | 0-4 | new game / continue |
| DROPS | NONE / LESS / NORMAL / MORE | `$30:$8212` weight |
| REFILL | NONE / HALF / FULL | respawn |
| GUARDS | OFF / ON (Spike Guard + Beat on loan, slotless) | stage start |
| HARD | OFF / ON | poke lists + AI `BIT` tests |
| RULES | GP / 1993 | everywhere (§13.3) |
| CRITICALS | OFF / ON (if shipped) | §14 |
| ANNOUNCER | OFF / ON | the pop-up queue |
| FLASHES | NORMAL / REDUCED | C.FLASH, WEAK flash, Time Stop tint, explosions |
| MMC5 AUDIO | ON / OFF | sound driver (art_audio.md) |
| SELECT SWAP | FULL / WEAPONS / OFF | §1.1 |
| 2P SHIFT | ON / OFF | §1.4 |
| LANGUAGE | JAPANESE / ENGLISH / ENGRISH | text engine (story.md) |

Any hand edit after choosing a preset shows the preset as **EDIT** (4MI).

### 13.2 Presets

| | CASUAL | NORMAL | HARD | 1993 |
|---|---|---|---|---|
| DAMAGE | ×0.5 | ×1 | ×1.5 | ×1 |
| LIVES | 5 | 3 | 3 | 3 |
| E-TANK FLOOR | 2 | 0 | 0 | 0 |
| DROPS | MORE | NORMAL | LESS | vanilla 12.1 % |
| REFILL | FULL | HALF | NONE | NONE |
| GUARDS | ON | OFF | OFF | OFF |
| HARD | OFF | OFF | **ON** | OFF |
| CRITICALS | OFF | ON | ON | OFF |
| RULES | GP | GP | GP | **1993** |
| Bolts | yes | yes | yes | none (the card is shown "for the record") |

- **Scores use the same formulas in every preset.** The record shows a C/N/H/93 badge per medal. Accessibility is not
  punished, and records stay honest.
- **HARD (SYS-DIF-2)** [new-code] M, Must as a framework (content per venue). It is the 4MI model:
  - **AI branches**: the bosses' and enemies' code tests `BIT CFG_HARD / BMI`. 4MI has 121 such tests. Each venue
    and fortress doc lists its own.
  - **Poke lists**: a list per stage section, applied when the section loads, to WRAM-resident layout or object data
    (if tech.md adopts that model; otherwise to the relocated object lists). Proposed entry: 3 bytes,
    `[kind << 5 | screen] [offset] [value]`. Kinds: 0 layout block, 1 object type, 2 object X, 3 object Y,
    4 collision group, 7 end.
  - Target: 4-12 pokes per venue, "one meaner screen per section".
  - The combat tables do not change in HARD; the ×1.5 damage and the patterns do the work.

### 13.3 1993 rules (SYS-DIF-3) [new-code] M, Should

The BRIEF's "vanilla rules", as a purist preset:

- **Forms**: change only through the pause menu, with the full vanilla transform. The weapon resets to the buster
  (`$38:$93F7`). Forms cannot fire weapons.
- **Combat**: vanilla damage and i-frames. A "1993" row set is generated from `$31:$9A45` and `$3F:$EFE4`: 60 f / 32 f
  everywhere, the punch 2 on Robot Masters. Vanilla's Knight shield is kept.
- **Off**: alt fires, synergies, the parry, chips, the shop, bolts, Beat rescue, criticals, the refill.
- **The Energy Balancer** is the vanilla passive item, found where GP places the chip.
- **Kept**: saves, the SELECT weapon cycle (it is a control, not a rule; it can be turned off), M.BEAM and the Super
  Adaptor (selected through the menu).
- **It is finishable** because of the normal-route rule (§2.4). 1993 players simply miss the secrets that need GP
  tools.

---

## 14. Optional criticals (SYS-CRT-1) [new-code] S, [new-sfx] 1, Could

The 4MI tribute ("pikoon"), with 4MI's own lesson applied: the dice must not be the frame counter.

- **The roll**, on each damaging hit that would not already kill:
  - it uses the vanilla LFSR (`$3E:$C88D` on `$DF/$E0`);
  - chance 1/128 normally; ×4 at HP ≤ 4 (1/32); ×4 with LUCKY DICE; 1/8 with both.
- **The effect**:
  - on normal enemies, damage ×8 (cap 31: in practice a kill);
  - on bosses, **+2 damage** (cap 6). 4MI's ×3 would break the 1-4 band.
  - The i-frames are unchanged. M.BEAM and HAZARD never crit.
- **Feedback**: a "pikoon" SFX, a star spark, and the pop object reading "CRIT!".
- **Scoring**: the CRITICAL style act.
- **Where it applies**: forced OFF in Time Attack, GP Rush and 1993. Default per preset (§13.2).
- The cost of cutting it: LUCKY DICE falls back to its cryptic bolt effect (§9.2).

---

## 15. What this doc needs from the others

### 15.1 Data and RAM (for tech.md, which owns the map)

Following rm6 lesson 3, GP state lives in PRG-RAM (WRAM). Only hot, per-frame bytes go in vanilla's free RAM
(`$06AF-$06FF`, 81 B).

| Where | Bytes | Contents |
|---|---|---|
| Free RAM (hot) | about 10 | SELECT hold timer, SEL_USED, SWAPMASK, LASTW, the form-swap cooldown, the CHR stream position, the Time Stop timer, the stagger timer, the multi-kill timer |
| WRAM, per object slot (23 each) | 4 × 23 = 92 | LASTHIT, LATCHSRC, REHIT (8-f lingering timer), FREEZE (frozen timer) |
| WRAM, run block | about 24 | T (3), L (2), K, CATS (2), OWNED (2), SECR, STY, TANKS, the kill count, flags |
| Save slot | about 140 | BOLTS (2), CHIPS_OWNED (2), CHIPS_EQ (2), PARTS, PARTS_USED, PLATES, W-tanks, E-tanks, the Metall count, WEAKFOUND (4), FORMS_DEBUT, flags (BREAK_JOINED, TURBO, DOVE…), BASS_ADAPT; per stage × 32: best score + preset badge (1), best PAY (1), secrets found (1), asterisk (bit) |
| System block | about 16 | the §13.1 settings |
| ROM tables | ≈ 1.2 KB | the boss cell table (≈ 470 B), the type → damage-routine table (256), NOPARRY / NOFREEZE (64 bytes as bitmaps), the 8 thematic tables (8 × 16), the chip and recipe data, help text |

**Hook sites** this doc assumes (tech.md confirms them and lists them in the hook registry):

| Area | Addresses |
|---|---|
| Input | joypad read `$3E:$C711` |
| Firing | fire dispatch `$38:$856A` (tables `$8556/$8560`); may-shoot table `$3F:$E130`; shot by form × level `$38:$854A`; charge `$38:$8651` |
| Menu and forms | menu reset to buster `$38:$93F7`; form CHR load inside `$38:$965F`; adaptor derivation `$38:$931D`, `$3B:$BA3F` |
| Shot vs enemy | the latch handlers `$38:$9021/$9028/$9067/$90A2`; C.FLASH `$38:$9E52`; energy `$38:$9E8E` |
| Damage | Robot Masters `$31:$997D` (with `$9A01`, `$9AD6`); fortress `$3F:$EF64`; normal `$3F:$E9D7/$EA20/$EA99/$EAB7` |
| Deaths | `$30:$81C7` (type `$17`), the type `$25` init, `$3F:$ED42` |
| Drops | `$30:$81E8` (weights `$8212`) |
| Player | hurt `$38:$8F72` (`$A2`); E-tank `$38:$9537` |
| Objects | object loop `$3F:$E438` (the frozen tick) |
| Jet HUD | `$3E:$CF90` |

### 15.2 Cross-doc dependencies (each doc must agree with these)

- **venues_a.md / venues_b.md**:
  - **Normal routes:** never need a form, an alt, a synergy or Break Man (§2.4). Use floor type E where Jet must not
    skip.
  - **Featured enemy:** each venue names its featured enemy (the PART drop), which dies to the champion's weakness
    weapon (§9.3).
  - **Scoring data:** each venue gives its VENUE ACT style act, its secret list and weights (exit 3, hidden room 2,
    behaviour item 2, plate 1), and its TIME par (§6.3).
  - **Hidden rooms:** one sponsor envelope each.
  - **Placements:** 4 venues hold plates; Tomahawk (or another venue) holds the ENERGY BALANCER.
  - **Bosses:** each champion's WEAK reaction pose (§5), its G/R thematics (§4.3) and any NOPARRY or NOFREEZE
    entries.
  - **Telegraphs:** tag gates use the scarf emblem and lead to optional content.
  - **HARD:** poke lists and AI branches.
  - **Weapon uses** they build on: Pogo over spikes, the Wall Spear, the Updraft, Cold Snap platforms, the held mace,
    Burning Knuckle and Morning Star on cracked blocks.
- **fortress.md**:
  - the placeholder rows in §4.5 (they may override them) and the special cases SC5 (Gamma), SC6 (Bass) and SC7 (the
    Yellow Devil SELECT trick);
  - the MAGNET BEAM reward in H1 and the SUPER ADAPTOR in H3;
  - secret lists and pars for its stages;
  - the W2 bracket rush uses Tables 1/2, own-weapon cells included.
- **story.md**:
  - the beat where Break Man joins; the Mr. Y booth beat and TURBO's consequences (Break Man's refusal line, the
    asterisk, the CAPCOM TIMES variant);
  - the announcer lines for `EV_WEAK_FIRST`, `EV_RESIST`, `EV_IMMUNE`, the first parry, the first synergy, Time Stop
    ("TIME, STOP!"), crits, close calls, Break Man's call/retreat, new forms, medals;
  - the JP versions of every help page.
- **meta.md**:
  - the results screen (judges, slide-in rows), the medal points (§6.6) and what they unlock;
  - the Pit Stop and garage UI;
  - records with preset badges and asterisks;
  - Time Attack and GP Rush force criticals OFF and use STABLE-like drops (NONE);
  - the debrief predicate list is the same as SECRETS';
  - the Exhibition rewards: proposed as fixed prizes (100 bolts + a special), not chips, to keep the chip count at 15.
- **tech.md**:
  - the VBlank budget for CHR streaming (128 B/frame assumed);
  - whether vanilla reads joypad 2;
  - the frozen tick in the object loop;
  - the LFSR, the WRAM map and the stage-attribute fields (boss row, scoring boss, par, secret list, NO TAG);
  - the poke-list format;
  - the death-hook audit of custom death paths.
- **art_audio.md**:
  - **Tile budgets:** the form difference tiles (target ≤ 64 per form); the swap flash (2 tiles); WEAK!/CRIT!/?!
    (≈ 8 tiles); PART icons (8); the token, envelope and W-tank icons; the alt-fire tiles listed in §3; the Super
    Rock and Break Man sprite sets.
  - **SFX:** the cycle tick, swap, parry "ting", weak crunch, "pikoon".
  - **Music:** Break Man's whistle jingle.

---

## Lessons applied

| Source | Lesson | Where |
|---|---|---|
| 4MI 1 | **Put the weakness in the i-frames**, keep damage 1-4, make the buster a deliberate (but vanilla-gentle) handicap | §4.2-§4.4 |
| 4MI 2 | Separate the mook and boss rules: no i-frames on mooks, only a lingering-hitbox timer | §4.7 |
| 4MI 3 | One crafting system plus one moral trade-off: PARTs/garage; Mr. Y's TURBO in the place of eating Eddie | §9.3-§9.4 |
| 4MI 4 | Friends are mechanics: Beat = pit rescue, Break Man = spare body, Mr. Y's booth costs a friend | §10, §11, §9.4 |
| 4MI 5 | Behaviour-gated items, plus a predicate list that drives both the score and the debrief | §9.2 (#9, #10), §6.2 SECRETS |
| 4MI 6 | Old weapons, new jobs: the full punch remains the fortress weapon (vanilla's 4), Knight's shield yields to it | §4.5, SC1 |
| 4MI (systems) | Accessibility knobs read at one place; frame-counter RNG avoided for crits; help pages from day one | §13, §14, §3 |
| CX 4 | A partner as a second body, once per life, with separate HP | §11 |
| CX 6 | Telegraph tools: the scarf emblem on tag gates; minions die to the boss's weakness (an in-stage tell) | §11, §9.3 |
| CX 7 | Damage in tables, the chart generated from them, special cases in visible code | §4.6, §4.8 |
| CX (systems) | A swap must clean up on purpose (GP keeps platforms); unusable weapon energy becomes HP | §1.1, §12.2 |
| RM6 7 | Adaptors are derived bits, patched at `$38:$931D` / `$3B:$BA3F`; forms couldn't fire weapons, so synergies are budgeted as new code | §2.3, §3.0 |
| RM6 8 | Keep quirks on purpose: C.FLRSH, igniting oil, Knight's shield, Wind Man's one-hit W.STORM (now an own-weapon reaction), the Jet sky bypass (Jet physics unchanged) | §3.9, §3.5, SC1, SC4, §2.2 |
| RM6 3 | GP state in WRAM; free RAM only for hot bytes | §15.1 |
| RM6 (vanilla data) | Thematic one-shot tables become the crafting system; vanilla's 60-f/32-f i-frames, drop weights and pickup values are the measured baseline | §4.1, §9.3, §12.1 |

## Risks

1. **The CHR stream may look bad or cost too much VBlank.** If the form difference is closer to vanilla's 2,048 bytes,
   the swap is 16 frames.
   - *Mitigation:* measure the tile difference early (M2), pack the form tiles, allow 256 B/frame on non-scrolling
     frames. As a fallback, the flash grows to 20 f. It still beats a 2-second cutscene.
2. **Code volume.** Forms × weapons × alts × synergies is about 24 new behaviours, plus the frozen tick, the parry and
   the attribution hooks. It is the largest systems item.
   - *Mitigation:* M3.4 builds the dispatch table first. The alts and synergies are added weapon by weapon, and each
     venue's vertical slice needs only its own weapon.
3. **Lag.** Lingering hitboxes, frozen enemies (still drawn) and Time Stop add collision checks to the ~10-object
   budget (BRIEF §6). *Mitigation:* the profiler (`shadow6`) on the M4 slice; cap lingering objects at one per
   weapon.
4. **Balance.**
   - A 16-f weakness may be too fast with multi-hit weapons; the stagger may still lock some patterns.
   - *Mitigation:* everything is one table byte; playtest at the M4 gate, with 20 f as the fallback.
5. **Attribution holes.** Enemies with custom death code (gorilla tank, Mr. X 1 riders, new GP enemies) may skip the
   death hook, and VARIETY would silently under-count. *Mitigation:* a shadow6 coverage check that every death path
   reaches the hook; a dev-menu "last kill class" readout.
6. **The frozen tick** needs a correct type → damage-routine table for all 256 types. A wrong entry makes an enemy
   immortal or fragile while frozen. *Mitigation:* seed it from `dmgmap.json` and test every placed type with Time
   Stop in the golden movies.
7. **IRQ-logic bosses vs Time Stop.** Knight's ceiling and Centaur's tide run in the IRQ, and the Wily Machine floor
   too. They keep moving during a stop unless their IRQ logic also checks the timer. *Mitigation:* the stop also
   pauses those three handlers' logic (a flag test), or the stage-attribute table marks them NO-STOP.
8. **The moral trade-off may feel unfair** (permanent loss). *Mitigation:* the double confirmation, the booth's
   obvious sleaze, Break Man "watching". And it is optional: TURBO is never needed.
9. **The 1993 preset doubles the test matrix.** *Mitigation:* Should tier. Its combat table is generated from vanilla
   data, so there is no hand balancing.
10. **The economy might be too rich.** A typical full game earns ≈ 2,300 bolts against 1,090 of chips. *Mitigation:*
    slots are the binding limit; prices are one table; the M10 balance pass.
11. **Scope.** Break Man needs a full sprite set (art L). He is a Should, and the scoring, call UI and tag gates
    degrade cleanly without him (the TAG TEAM act and class E simply never fire).

## Open questions

1. Does vanilla's player F.BLAST already ignite oil? The critic saw Fire Telly drops and "a thrown flame" ignite it via
   `$3E:$DDFC`, but not which flames call it.
2. How many sprite tiles really differ between Normal, Power and Jet in bank `$01`? This sets the swap-flash length.
3. What VBlank budget is left beside the column paints on a scrolling frame (tech.md)?
4. Does any vanilla code read joypad 2 (`$41/$43`)? If so, the pseudo L/R needs a guard.
5. What are the vanilla Plant Barrier's duration and radius? They set the Petal Storm numbers (not measured here).
6. Should VARIETY count boss hits (the current proposal) or kills only? Boss hits make Pv easy to reach in the boss
   fight. That is the intent, but it should be playtested.
7. Should TURBO stay permanent, or can the player "return it to Mr. Y" at a cost (for example, all bolts)?
8. Is Break Man's no-cost retreat too generous? The alternative is that a retreat empties his call for the rest of the
   *stage*, not just the life.
9. Are Exhibition rewards chips (PLAN) or fixed prizes (this doc's proposal, which keeps chips at 15)? The Exhibitions
   doc decides.
10. The Mr. X 1 riders' charged buster was measured at 1 but the code predicts 3 (rm6 SUMMARY §8). If fortress.md
    reuses the riders, their row must be checked.
11. Do criticals ship? If not, LUCKY DICE keeps only its cryptic bolt effect.
12. The weakness-found ★ in the pause menu (§5 item 6) is a Could. Is it too much hand-holding next to the minions'
    tell (§9.3)?
