# Vanilla Rockman 6 (J): research summary for Rockman 6 GP (rm6-critic)
Tags: [seen] emulator, [code] disassembly/ROM, [text] in-game text, [doc] outside source, [guess].
(critic) = measured or corrected by the critic. Scratch: build/research/rm6/rm6-critic/.

## 1. Vanilla structure

### 1.1 Flow
Title, then the stage select (3x3 grid at $3F:$F232; the centre opens once all 8 are beaten), then a Robot Master stage, its boss, YOU GET, and the password / stage select. After the 8: Mr. X Fortress 1-4 ($51 = 8-11), the Mr. X reveal and the Wily Fortress picture, then Wily Fortress 1-4 (12-15), then the ending (TO BE CONTINUED; START resets). That is 16 stage ids. Passwords hold only 8 bosses + 4 plates + the Energy Balancer (13 bits, 8192 states, each with 2 encodings, always 5 orbs). Fortress progress is never saved, and a game over in a fortress offers CONTINUE only.

### 1.2 Robot Masters ($51: stage; weakness x4; award; plate / alt exit; gate; music; screens)
- 0 Blizzard; F.BLAST; B.ATTACK; none; items only; $01; 25.
- 1 Wind; C.FLASH; W.STORM; none; item only; $00; 22.
- 2 Plant; B.ATTACK (F.BLAST 2); PLANT.B + Rush Jet; none; items; $04; 24.
- 3 Flame; W.STORM; F.BLAST + Rush Power; none; item; $03; 24.
- 4 Yamato; SILVER.T; Y.SPEAR; E plate, room 1D via the 0B up ladder; Rush Jet (plus a lower bypass 02 to 0C-0F behind a charged punch, with a dark-room mid-boss and an E-tank); $02; 30.
- 5 Tomahawk; PLANT.B; SILVER.T; B plate, room 1F via the right ladder of 12 (no adaptor); Energy Balancer room 1C (charged punch); sky bypass 18-1B (Rush Jet, critic); $06; 32.
- 6 Knight; Y.SPEAR; KNIGHT.C; A plate, room 1A via the Power pillar in 15; charged punch; $07; 27.
- 7 Centaur; KNIGHT.C; C.FLASH (data spells C.FLRSH); T plate, room 17 across the 112-px gap in 15; Rush Jet; $05; 27.

Weakness cycle: Flame > Blizzard > Plant > Tomahawk > Yamato > Knight > Centaur > Wind > Flame. Everything else does 1. PLANT.B and C.FLASH do 0 to all but their target. Buster 1, charged buster 3, Power punch 2 even when charged (special case $31:$9AD6).
Boss HP is 27; a boss dies below 0. The intro object $93 spawns the room controller $94, then becomes the boss type from $31:$9D43 = 90 99 B2 9C 98 9F 95 9B. Knight Man's attack byte $34 is class 3, a shield: shots from the front are reflected and only the full punch always hits.
There are no stage rematches: walking into a beaten boss's room beams Rockman out. The plate is set at the kill when $57 = $3F:$F518[stage]. The YOU GET text id is $60 + $51 + $06A5.

### 1.3 Adaptors, Beat, Energy Balancer (all derived from progress bits)
- Jet = $0695 b0 (Plant Man beaten). Power = $0694 b0 (Flame Man beaten). Both are derived in two places: menu $38:$931D and stage start $3B:$BA3F.
- Beat = bit 2 in all four of $0692-$0695 (gives $0691 = $1B at stage start). Balancer = $0696.
- Forms: $9B = 0 normal / 1 Jet / 2 Power.
  - A form changes only through the pause menu. Its transform sequence $38:$965F loads the form's sprite CHR (bank $01, sets $04-$07).
  - Closing the menu with a form selected resets the weapon to the buster: forms have no special weapons.
  - Jet: buster only, no charge, no slide. Fuel $9C is a 19-unit stamina bar: -1 per 4 frames of flight, +1 per 2 frames otherwise, even in mid-air.
  - Power: punch only (reach 21-81 px), charges at 2 per frame (full in 45 frames), no slide. No adaptor uses weapon energy.
- Energy Balancer (critic, seen): with the buster equipped, a weapon-energy pickup goes to the lowest weapon. Without the Balancer that pickup is wasted, and with a weapon equipped the pickup refills that weapon.

### 1.4 Weapons (slot $0699: weapon, class/shot byte, energy per use of 28, damage to a normal enemy)
- 0 R.BUSTER: 1/$11 (full charge $13), free, 1 (charged 3).
- 1 Y.SPEAR: 5/$52, 1, 2.
- 2 W.STORM: 6/$62, 1, 2.
- 3 B.ATTACK: 7/$72 (4 flakes), 3, 2 per flake.
- 4 F.BLAST: 8/$84, 1, 4.
- 5 PLANT.B: 9/$94, 4, 4.
- 6 KNIGHT.C: A/$A3, 1, 3.
- 7 SILVER.T: B/$B3, 1, 3.
- 8 C.FLASH: C/$C4 (latched into every class 1/3/F object), 4, 4 screen-wide.
- 9 BEAT: D/$DF, costs the victim's HP+1, kills any class-1 enemy, never hurts bosses (BEAT mode also fires a buster shot).
- Power punch: $12/$13/$14 = 2/3/4.

The victim's routine decides damage from the hit latch $056C:
- normal enemies take the low nibble ($3F:$E9D7);
- per-class tables $3F:$EB46/$EB56/$EB66 give thematic one-shot kills (F.BLAST kills the snow robot $4D, B.ATTACK kills the fire robots $2A/$2C);
- Metalls and others take only the full punch ($EA99).

### 1.5 Fortresses ($51: stage, screens, boss [doc names], how drawn, weakness, side routes)
- 8 Mr. X 1, 22: Rounder II, two rail riders hit only from behind; sprites on a BG lattice; F.BLAST/PLANT.B 4; charged-punch glass door at 06 leads to 12-15 (4 1-ups).
- 9 Mr. X 2, 18: Power Piston; BG in NT1 with vertical scroll + split; SILVER.T 3; falling bell row.
- 10 Mr. X 3, 18: Metonger Z; BG tank + sprite pilot (chain $1A); B.ATTACK 3; Power-block item pockets.
- 11 Mr. X 4, 25: X Crusher; BG in NT0, multi-split (chain $16); F.BLAST 4; open branch 09 > 16-18 > 0F.
- 12 Wily 1, 24: Mechazaurus, a static BG dinosaur; no usable weakness (the table's Y.SPEAR 4 is unreachable); charged-punch pocket 09 > 14-17.
- 13 Wily 2, 19: Tank CSII walker; BG in NT1 (chain 7); W.STORM 4; F.BLAST plug 04 > 10-12 > 0A (one blast opens both plugs).
- 14 Wily 3, 17: boss rush of the 8 Robot Masters with their real AI, any order. Tables $39:$8EC8/$8ED2/$8EDC, room $09+id, palette $9A+id. This is the only place for rematches.
- 15 Wily 4, 7: Wily Machine 6 (2 phases, BG in NT1, floor split chain $19), then the sprite Wily Capsule: three 27-HP bars in one room; SILVER.T 4.
Fortress damage comes from $3F:$EFE4[class*8 + stage-8]. The charged punch does 4 to every fortress boss and C.FLASH 0. Fortress bosses award nothing. There is no plate or Balancer in any fortress.

### 1.6 Secrets and gates
- Collision $B breaks only to the fully charged Power punch (shot $14).
- Collision $D breaks to F.BLAST.
- Geometry gates need Rush Jet.
- Breakables are one bit per metatile id in $0340 (256 bits). They survive deaths and are cleared at stage start; blocks that share an id open together.
- Item pockets behind Power blocks exist in most stages and fortresses. Blizzard 09's E-tank is behind F.BLAST ice.
- Flame's oil ignites (critic).
- Hidden debug SOUND PLAYER in bank $28: unreachable, and the only SELECT handler in the ROM.

### 1.7 Story and text
About 30 lines, all kana; the only kanji are the logo art 史上最大の戦い!!.
- The 1st World Robot Championship 'for the sake of peace'. Mr. X, its sponsor, steals the 8 robots and claims to be the shadow ruler behind Wily.
- After the Mr. X fortress, the disguise comes off in animation only.
- The CAPCOM TIMES reports Wily jailed. The staff roll replays each boss's real AI in its own room, with a card naming its fan designer (DWNB-41..48). The game ends on TO BE CONTINUED.
- No text exists for Light, Roll, Blues or the Balancer. The boss-panel stats are English even in JP.

## 2. Asset inventory per stage (critic, build/research/rm6/rm6-critic/inventory.py / .json)
Columns: layout bank:page | tileset bank:page | screens | blocks used/256 | metatiles/256 | BG tile ids used/free (over all CHR configs) | BG CHR sets | music.
- Blizzard 32:A0 | 2E:80 | 25 | 255 | 245 | 253/3 | 82+84+85 | 01
- Wind 32:A8 | 2C:80 | 22 | 232 | 194 | 248/8 | 83+8C+8D+8E | 00
- Plant 32:B0 | 2E:92 | 24 | 255 | 197 | 256/0 | 90+91+92+93+BB | 04
- Flame 32:B8 | 2F:80 | 24 | 254 | 178 | 229/27 | 86+87 | 03
- Yamato 33:A0 | 2E:89 | 30 | 255 | 221 | 252/4 | 97+98+99 | 02
- Tomahawk 33:A8 | 2C:89 | 32 | 221 | 212 | 255/1 | 94+95+96 | 06
- Knight 33:B0 | 2D:80 | 27 | 255 | 155 | 250/6 | 9E | 07
- Centaur 33:B8 | 2D:89 | 27 | 250 | 176 | 245/11 | AA | 05
- Mr. X 1 26:A0 | 2C:92 | 22 | 249 | 198 | 249/7 | 9D+B9+D7 | 09
- Mr. X 2 26:A8 | 2F:89 | 18 | 234 | 170 | 168/88 | A4+B3+B8 | 09
- Mr. X 3 26:B0 | 2F:92 | 18 | 256 | 169 | 255/1 | B1 | 09
- Mr. X 4 26:B8 | 2B:80 | 25 | 159 | 165 | 253/3 | C3+C4+D2 | 09
- Wily 1 27:A0 | 2A:80 | 24 | 255 | 223 | 254/2 | 89+8B | 0B
- Wily 2 27:A8 | 2A:89 | 19 | 232 | 120 | 221/35 | A2+A3+B2 | 0B
- Wily 3 27:B0 | 2A:92 | 17 | 251 | 151 | 165/91 | A2+A8+A9 | 0B
- Wily 4 27:B8 | 2B:89 | 7 | 177 | 130 | 247/9 | BA+BC+BD+BE | 0B

Per stage (art | placed enemy types | effects):
- Blizzard: ice blocks, snow ledges, girder scaffolds, mountain skyline, ship hull/deck/sea (set $85) | $4D snow robot, $19/$21 count bombs, $24 drone, $13 drill, $1E walker, $12 wall cannon, $10 jester head, $1F/$20 ship riders | rocking-ship split (chain 1, stage-0 collision offset), slippery ice.
- Wind: sky, clouds, coral girders, gold pillars, green tower, fans/updrafts ($A/$C) | $27 panda, $29, $1B bomber, $36, $2D stomper, $34 shield-car, $75 beetle, $59 horned robot | no split.
- Plant: jungle canopy, bamboo floors, curtain-wood interior, flower section | gorilla tank $50-$53 (twice), $60, $61, $54, $24/$26, $59, $5A, springs $57/$5F | floor split in the gorilla rooms (chain 7). No free tile ids; heavy lag.
- Flame: oil field, pipes, DANGER drums, refinery, red fire cave (set $87) | $18 Metall, $2C/$30 Fire Telly, $2B, $C0/$C9, $73 mine, $2A juggler | oil palette cycle, igniting oil.
- Yamato: Fuji vista (screen 00 only), castle walls, shoji, dark bypass | $C2 lantern robot, $A2 samurai, $69, rider tank $D0-$D8, $54, $13, $A7, $75 | no split.
- Tomahawk: desert mesas, cacti, cave, pink sunset with sun disc, pipe/mesh interior | $6C cowboy, $12 totem, $4F dispenser, $6E, $67, $13, $59, $A0 lift | parallax (chain C), heat shimmer (chain E).
- Knight: green stone castle, purple/red halls, chandeliers, machine hall, torch CHR animation | $6E lance knight, $3D, $65, $67, $70, $C6, $75, $3A | descending spike ceiling (chain $11, logic inside the IRQ, stage 6 only). Revisit palettes give a second colour scheme.
- Centaur: Greek ruins, water, waterfalls, orange castle | $A9/$AB pelicans, $C1 piranha, $C9, $C4 seahorse, $2B, $A5, $10 | tide (chain $14, logic inside the IRQ, stage 7 only). One item in the whole stage.
- Fortresses: see 1.5. Mr. X 2 and Wily 3 have 88/91 free BG tile ids. Wily 2 and Wily 3 share base set $A2.
Shared enemies: $10 (Blizzard, Centaur, Wily 1), $C9 (Flame, Centaur, Mr. X 1/4, Wily 3), $2B, $70, $59, $4F. Any type can be placed anywhere if its sprite CHR set (AI header byte AI-4, queued per screen) does not clash on that screen.
Big-boss art packs: Wily Machine set $BE (202 tiles), dinosaur $8B (162), walker about 94, tank and X Crusher inside their stage sets. BG-boss technique: the boss is drawn in a scrolled nametable, an IRQ split shows an unscrolled floor strip from NT0, and invisible hit-box objects follow the scroll.
Music: 102 tracks. $00-$22 and $39 are music, $23-$65 SFX, $F0-$F7 commands. Stage themes $00-$07, Mr. X $09, Wily $0B, fortress boss $0C, Wily Machine $18, boss defeated $13, weapon get $16, stage select $0F, boss intro $10, fortress maps $11/$12, title $19, opening $0D/$0E, ending $08/$0A/$17/$1B-$22, GAME OVER $14 (critic), password/continue $15 (critic). $1A is an empty stub.

## 3. Verified technical facts for the build

### ROM and mapper
- MD5 of the whole file d9a4eed8b3c13a6bd74b2e9d20385afb; PRG CRC32 2D664D99.
- NES 2.0 header: mapper 4, 512 KB PRG, 8 KB CHR-RAM, battery bit clear.
- MMC3 PRG mode 0, banks $3E/$3F fixed.
- Helpers: $CBC0 (Y > $8000, Y+1 > $A000), $CBDA (A > $A000). $CB91 maps A at $8000 after pushing the caller's banks under the return address; $CBAF is its tail. $CBE9 restores. Shadows $4A/$4B/$4C.
- Far call $CB28 + inline byte: the 4-slot table $CB5F = 3C 3A 38 36, all used.
- CHR: RESET writes the identity map 00 02 04 05 06 07 from $FF50 and nothing changes it later.

### RAM
- Stage $51; camera $56/$57 (screen; changes on vertical transitions too, critic).
- Object table 23 slots x 29 arrays at $03A0. HP $03E5; type $03A0; AI pointer $0413/$042A, bank $0441; sprite bank $0458; X $046F/$0486/$049D; Y $04B4/$04CB/$04E2; attack byte $0583; hit-box id $059A; hit latch $056C.
- Inventory $0688-$0691; progress $0692-$0695; Balancer $0696; weapon $0699; E-tanks $06A1; lives $A9; form $9B; fuel $9C; i-frames $A2; charge $9E; floor type $064B/$A7; ice momentum $A1.$A0.
- Exit code $F0 (1 clear / 2 respawn / 3 game over). Checkpoint $0684-$0686.
- Warp: write $51 and $0684-$0686, then set $F0 = 2.

### Free RAM
- Free: $06AF-$06FF (81 B), $07FA-$07FF (6), $0698, $064C. Never written across the scout's 118,526-frame run plus the critic's 114,196 late-game frames.
- $01A0-$01E4 is a stack safety margin only.
- There is no free zero page.
- WRAM is never enabled (no $A001 write).

### Free ROM
- Banks $0B-$0F: 40 KB of fill with 3-35 stray bits. Never executed or read in 139,200 traced frames, and no table points there.
- $3F:$FAC0-$FF1F: 1,120 B, never touched. $FF24-$FF3F are zero; $FF20-$FF23 = 02 00 10 08, unreferenced.
- Text banks: $3C:$9D16-$9FE1, $3D:$BA8D-$BCFF, $3D:$BF42-$BFFF (about 1.5 KB).
- Empty tileset slots: $2B:$9200 and $2D:$9200 (2 x 2,304 B).
- Object-list space: $3A:$95D4-$9FFF (2,604 B).
- Sound: $36 tail, 449 B.
- Sprite-bank fill: 1.2 / 2.3 / 4.3 KB in the pairs $20/$22/$24.
- Fill-like runs total 101.0 KB, of which 61 KB lie outside $0B-$0F, scattered.

### Level format: done
- Table $3E:$DF25 (9 x 16); layout of 8 rows x 256 one-byte 32x32 block ids (32 screens per stage, vertical sections are just screen indices); block = 4 metatiles; metatile = 4 tiles + attribute (palette bits 0-1, collision bits 4-7; bits 2-3 free).
- Alternate metatile set at $9B-$9F, switched by $0340.
- Collision is remapped per stage group ($DB03/$DB13).
- Object lists in $3A as 4 parallel arrays; type $80 = screen script (bank $39: init, mode, per-frame, exits 1-6). The boss-room script $0A lives in $3F:$F947.
- Palettes are cumulative partial programs; bank $28 holds the revisit palettes.
- levels.py: byte-exact round trip (re-run by the critic), JSON export, build_rom tested in game, maps of all 16 stages.

### Objects
- Type tables $3A:$82C9/$83C9/$84C9/$85C9.
- 6-byte AI header (anim, palette, CHR set, hit box, HP, attack) read by $EBD5.
- About 30-32 free type ids: 42 7B-7E BA-BF CE CF D2 D7 DB-DF F4-FF.
- Coroutine AIs (JSR $E46C yields).

### Metasprites (critic, verified 118/118)
- Per sprite bank: $8000/$8200 (+$8100/$8300) frame pointers, $8400/$8500 layouts, $8600/$8700 animations.
- Frame = [n-1][layout] + n x [tile, attr]; layout = n x [dy, dx].
- Flip emitters at $E320/$E357/$E395/$E3D4.

### Text
- One interpreter ($3C:$8631) and one table of 168 PPU scripts (pointers $3C:$8787/$882F). No in-string control codes.
- Typewriter via $069F/$06AC/$06A6.
- 11 per-screen .tbl tables, kana mapped. An all-caps English line was shown on screen by the unmodified engine.

### Sound
- Requests go to $DC, then into the ring $B0-$BF; serviced at $C8C1 ($8003 play, $8000 update).
- Big-endian table at $34:$8A40.
- Data spans $34-$36: the reader $34:$803A switches bank $36 itself.
- Command set $00-$18 decoded.

### IRQ
- 27 handler chains at $3E:$C116, started by $0672/$0677/$F4.
- Handlers 0 and 6 are effectively free.
- Three handlers run game logic inside the IRQ, and several call the sound update.

### Lag
- About 10 live objects fill a frame.
- Cost: OAM builder 23%, sound 18%, bank switching 13%, collision about 20%; enemy AI under 1%.
- The music keeps tempo during lag.

### MMC5 port checklist (critic; engine.md section 9)
- $8000/$8001: $CB91-$CC09 helpers, $C8C1-$C901 sound service, $C7AF/$C7B4 NMI PPU-transfer bank, $34:$804E-$8060 sound reader, RESET $FFCE/$FFD4.
- $A000: $C021, $38:$9295, $38:$95BA, $FFC9.
- IRQ: NMI $C06F-$C077 and $C0CD-$C0D5, $C151/$C154, chain handlers $C188-$C4EE, $C51A, $FF96.
- Renumber the two LDA #$3E / JSR $CB91 sites ($E204, $E430).

### Stage ids
45 executed reads of $51:
- 5 AND/ORA #$08 fortress tests ($38:$916B, $3C:$805F, $3F:$F0FB, $3F:$F9A0, $3B:$BB74);
- CPY #$08 at $EF6B, $F4EB, $F96A;
- 14 CMP #n stage specials;
- 8-entry tables at $F200-$F218, $3C:$8606, $F518, $F6B3/$F6BB/$F6C3.
A stage id of 16 or more breaks the fortress tests.

### Tools and states
- tools/analysis/rm6: cheats.py (warp, godmode, password codec, autoplayer), levels.py, rm6_ppuscript.py, shadow6.py (frame re-execution, code coverage, profiler), rm6_stagemap.py, rm6_level.py.
- States: 52+ in build/research/rm6/states/, plus the agents' scratch states. The critic added none.

## 4. PLAN.md claims: CONFIRMED / CONTRADICTED / UNKNOWN

### Section 2: CONFIRMED
- 2.1 SELECT is free: the only test in the ROM is $28:$813C (critic rescan plus the scout's 8-state test).
- 2.1 Saves replace passwords at no loss: passwords are full (13 bits) and vanilla never uses PRG-RAM.
- 2.1 Lag is real: about 10 objects fill a frame; profiled.
- 2.2 Power's charged punch breaks cracked blocks (only the full charge), and Power has no slide.
- 2.2 Jet flies and cannot charge.
- 2.2 Normal Rock has slide, charge and full weapon access, and forms have no weapons.
- 2.2 'Normal exits never need an adaptor' holds for all 8 Robot Master stages. In the fortresses every gate is on an optional branch, but the main routes were not walked in normal form.
- 2.3 Fixed per-weapon damage to normal enemies is already the vanilla rule (low nibble), and per-boss damage tables exist.
- 2.5 There are exactly 4 Beat plates (B Tomahawk, E Yamato, A Knight, T Centaur), so a maximum of 6 chip slots works.
- 2.5 The Energy Balancer's vanilla path (Tomahawk 1C, charged punch) and its effect (refills the lowest weapon) match, with the buster-only nuance.
- 2.6 Branches are pure data (exit targets into screens $18-$1F plus $F518), and the cracked-floor mechanism exists.
- 2.7 A language switch needs one hook in $3C:$8631. C.FLASH really flashes the screen.

### Section 2: CONTRADICTED
- 2.1 'Menu fixes' are already vanilla behaviour: the ladder state and a held charge survive the menu (critic, seen).
- 2.1 'Upward scroll jump boost': vanilla cannot enter a screen from below without a ladder (up exits need $94 = 4 and Y < $0B), so a new exit condition is needed, not just a boost.
- 2.2 'Heat gauge replaces energy drain': the Jet never drains energy; it already has a regenerating stamina bar.
- 2.2 Acquisition after the 2nd/4th win is a change from vanilla's boss-specific rule (Flame gives Power, Plant gives Jet); patch $38:$931D and $3B:$BA3F.
- 2.3 'Every non-buster weapon does at least 2' is a big change: vanilla gives mostly 1 and many 0s, and Wily 1 has no usable weakness.
- 2.6 'Every venue has a secret exit': only 4 vanilla stages branch, with no flag bits for stages 0-3.

### Section 2: UNKNOWN
- 2.1 Heal speed: the E-tank rate is known (+1 HP per 4 frames, 108 frames for a full refill), but whether the heal SFX $31 silences the triangle is not.
- 2.2 Parry: a precedent exists (full-punch projectile rebound $DA/$E4, attack $1A, in Wily 1 and one more fight); general behaviour untested.
- 2.4 Scorecard kill attribution: feasible, since the victim routines read the shot class; untested.
- 2.8 Bass: no data yet. The sprite format is now known.

### Section 3: CONFIRMED
- 3.1 Vanilla has 8 fortress stages and 16 stage ids; the Mr. X and Wily slots exist, with one Wily slot spare under PLAN's mapping.
- 3.2 A layout can be rewritten on a vanilla tileset (data only, round trip proven).
- 3.2 Knight Man has a vanilla frontal shield.
- 3.2 Centaur's rising and falling water is vanilla (chain $14, stage-7 collision offset).
- 3.2 Flame's oil ignites in vanilla (critic).
- 3.2 Parallax bands (T4) exist (Tomahawk, chain C).
- 3.2 Updraft and fan tiles exist.
- 3.2 A falling ceiling exists (Knight chain $11, stage 6 only).
- 3.2 Warp precedents exist ($39:$89F5, the Wily 3 hub).
- 3.2 Multi-part bosses exist (gorilla tank, Mr. X 1 riders, Wily Machine).
- 3.5 The bracket rush can reuse Wily 3's data-driven rush.
- 3.5 The machine-over-floor setup has a precedent in the Wily Machine (BG boss + chain $19).
- 3.6 Fortress bosses catalogued: Rounder II, Power Piston, Metonger Z, X Crusher, Mechazaurus, Tank CSII, Wily Machine 6, Wily Capsule [doc names].
- 3.4 Re-skin fits [guess]: a flying BG Yellow Devil can follow X Crusher (floating NT0, multi-split) or the Wily Machine (hopping NT1 + floor split); Gamma follows Mechazaurus (static BG + head hit box); Cossack Catcher follows Metonger Z (sprite pod + BG body) or Power Piston (vertical-scroll BG); Dark Man follows the Robot Master sprite framework ($93 intro, then the boss type).

### Section 3: CONTRADICTED / caveats
- 3.2 Homage BG set pieces on vanilla tilesets: blocks and tile ids are nearly exhausted (Plant 0 free tile ids). Use a new tileset slot or free banks, or build set pieces as sprite objects.
- 3.2 Destructible ice ceilings (T6) are genuinely new: vanilla breakables are per metatile id and only open to the full punch or F.BLAST.
- 3.2 Autoscroll (T1: Tomahawk train, Wind shmup): no vanilla autoscroll was found.
- 3.1 22 stages exceed 16 ids: the AND #$08 tests break, and all four layout banks are full.

### Section 3: UNKNOWN
- Which fortress AIs actually fit which MK-VI bosses (untested).
- Wind Man's full pattern against a moving player.

### Section 5: CONFIRMED (critic re-measured)
MD5/CRC/header; vectors; fixed banks; the helpers $CBC0/$CBDA/$CBAF (with $CB91/$CBE9 as context); shadows $4A-$4C; the $C8C1 sound service and ring $B0-$BF/$D9/$DB; RESET writing CHR R0-R5 from $FF50 and then JMP $C51E; IRQ in use (18 $C000 pattern hits, 13 executed); free banks $0B-$0F; $FAC0-$FF20; about 101 KB of fill-like runs (103,407 B); text tables A=$0B / A=$2B in $3C/$3D; WRAM unused.

### Section 5: CORRECTED / EXTENDED
- Sound data spans $34-$36, and the driver switches banks itself.
- Requests go through $DC.
- Kana are now mapped, and the font differs per screen.
- The NMI's mirroring write is at $C021 (the LDA $FB is at $C01F).

### Section 5: UNKNOWN
The exact roles of $46 and $60 (partly known: $47 is the VRAM buffer index, $60 = $68 is the column paint request).

### Section 6: CONFIRMED
- Bank numbers below $3E keep working.
- CHR banking is unused, so the MMC5 8 KB CHR mode is safe.
- There is room for a FARCALL in $FAC0+.
- CHR and all level data are raw (uncompressed).
- The level extractor, round trip and renderer exist.
- The music bytecode is decoded.
- The IRQ chains need translation, including the handlers that run game logic.

### Section 6: CONTRADICTED
- 6.1 'Only references to fixed-bank numbers are the hardware mapping': two LDA #$3E / JSR $CB91 sites exist, and the port list is incomplete (see section 3).
- 6.2 'Assume no RAM is free': 89 bytes are free.
- 6.5 'One ASCII character per 32x32 block': stages use up to 256 block ids, so use 2 hex digits per block.

### Section 6: UNKNOWN to KNOWN
6.5 Capcom's sprite-mapping format is now decoded (engine.md 1.5).

### Section 6: UNKNOWN
Golden movies and ramdiff.py are not built yet; shadow6 can replace a CDL.

## 5. Verification log (critic)
- Header/MD5/CRC: confirmed.
- Vectors, helpers, RESET: confirmed by disassembly.
- Free ROM: bytes confirmed, plus the engine trace.
- Free RAM: confirmed, plus the late-game canary run.
- Stage table: confirmed.
- Level round trip: re-run, identical.
- PPU scripts: selftest 168/168.
- Type tables and AI header HP: confirmed.
- Weakness tables: confirmed, including Plant F.BLAST 2 and Wily 1 Y.SPEAR 4.
- Plate and adaptor code: confirmed.
- SELECT: exactly one test.
- Sound table: confirmed; $14/$15 identified.
- MMC3 sites: listed.

## 6. Corrections made in place
- ram.md: $57 on vertical moves; $0583/$059A/$056C; jump $FA.CC; $9E/$9D/$A0/$A1; $A7 floor type; free-RAM late confirmation; pause, ladder, charge and E-tank facts.
- cheats.md: the $57 note.
- stages_a.md: 27 IRQ chain entries, not 24; the boss room is script $0A (no 'mode $FF'); ice is slippery; oil ignites (+ img/critic_flame_oil_ignites.png).
- stages_b.md: what the Energy Balancer does; the sky bypass is a Rush Jet route (+ img/critic_tomahawk_skybypass.png).
- levels.md: player-side meanings of the collision types.
- engine.md: the jump constant; music $14/$15; 1.5 metasprite format; 9. porting checklist.

## 7. Lessons for Rockman 6 GP
1. Keep vanilla stage ids below 16, or rewrite the AND #$08 / CPY #$08 / stage&7 / stage-8 assumptions before adding stages. Relocate the packed stage, object-list and collision-group tables.
2. The 32x32 block table is the binding art budget. Give each venue its own tileset slot (2 are empty, and free banks hold more), keep the vanilla CHR, and build homage set pieces as sprite objects where possible.
3. Use the 89 free bytes only for hot vanilla-side hooks; GP state belongs in MMC5 PRG-RAM.
4. Use the porting checklist: the sound driver and the OAM/object loops touch MMC3 or fixed-bank numbers outside the documented helpers.
5. New enemies take a free type id, a 6-byte AI header and frames/layouts in a sprite bank pair. The sprite format is known; mind per-screen sprite-CHR conflicts and the ~10-object lag budget.
6. Breakables are per metatile id, which is useful for 'open both plugs' puzzles and igniting oil, but wrong for per-tile destruction (T6 needs per-position flags).
7. Adaptor ownership and plates are derived bits. Change acquisition in $38:$931D and $3B:$BA3F, and remember that vanilla forms cannot fire weapons.
8. Keep vanilla quirks deliberately: igniting oil, slippery ice, the Wily 2 twin plugs, the Jet-only sky bypass, C.FLRSH, TO BE CONTINUED.

## 8. Open questions
- The Mr. X 1 riders' charged buster: measured 1, code $3B:$827A predicts 3.
- How the weapons reach Wily 1's controller.
- Fortress main routes in normal form.
- Collision 7 outside group 2 and the other remapped $1x values.
- Triangle silencing by the heal SFX.
- SFX $3D/$3E/$4D/$51: no literal request site.
- The CAPCOM TIMES headline reading.
- Wind Man's W.STORM single hit.
=====================================================================

## Critic's verification highlights

- docs/research/rm6/SUMMARY.md was NOT created: the harness refused it ('Subagents should return findings as text, not write report files'), so the whole synthesis is in this report's coverage field instead. Corrections and additions were made in place in ram.md, cheats.md, stages_a.md, stages_b.md, levels.md and engine.md, each marked '(corrected by critic)' or '(added by critic)'.
- The load-bearing claims re-checked by the critic all hold: header, MD5 and PRG CRC; vectors $C000/$FF70/$C14C; PRG mode 0 with banks $3E/$3F fixed; the helpers $CB91/$CBAF/$CBC0/$CBDA/$CBE9; the 9x16 stage table at $3E:$DF25; the level round trip (re-run: exit 0, identical); the 168 PPU scripts (selftest 168/168); the AI-header HP bytes; the weakness tables $31:$9A45 and $3F:$EFE4; the plate and adaptor logic ($F4EB, $F518 = FF FF FF FF 1D 1F 1A 17, $38:$931D); the sound table ($34:$8A40 = 102 tracks) and SELECT (exactly one test in the ROM, $28:$813C).
- Free RAM now holds for the whole game: in 114,196 more frames (Mr. X reveal, boss rush and refight kills, Wily Machine and Capsule kills, the full ending, a fortress game over, the attract demo), two canaries never saw $06AF-$06FF, $07FA-$07FF, $0698, $064C or $01A0-$01E4 written. The 7 never-written zero-page bytes are live: poking them made the Capsule's death overflow the stack.
- PLAN 6.1 is contradicted: two code sites, LDA #$3E / JSR $CB91 at $3F:$E204 (OAM builder) and $3F:$E430 (object loop), map bank $3E into the $8000 window as a placeholder, so they need renumbering in the 1 MB MMC5 layout. The port list also misses the sound driver's own bank switch ($34:$804E-$8060, which maps bank $36), the NMI's PPU-transfer switch at $3E:$C7AF, the helper $CBE9, a second NMI IRQ path at $C0CD-$C0D5, and 19 IRQ-chain sites. There are only 4 real $A000 mirroring writes, not about 7.
- Stage-id expansion risk for the 22-stage plan: 45 executed instructions read $51, including five AND #$08 'is this a fortress' tests, three CPY #$08, 14 per-stage CMP #n specials and several 8-entry tables. A stage id of 16 or more has bit 3 clear, so those tests would treat it as a Robot Master stage. All four layout banks are full, and the stage, object-list and collision-group tables are packed back to back.
- Capcom's metasprite format, the last untouched M0 item, is decoded and verified (118 of 118 predicted sprites found in live OAM). Per sprite bank there are frame tables at $8000-$83FF, layout tables at $8400/$8500 and animation tables at $8600/$8700. A frame is [n-1][layout id] then n pairs of [tile, attr]; a layout is n pairs of [dy, dx]; an animation is a half-table flag then [frame, duration] pairs. Now in engine.md 1.5.
- PLAN 3.2's 'oil pools that ignite (vanilla)' is confirmed: a Fire Telly drop or a thrown flame that lands on oil (collision 2) calls $3E:$DDFC, which flips that oil metatile id to its burning alternate (collision $F, deadly). Every oil tile with that id ignites, and it stays lit through deaths. Seen on Flame screens 04 and 0B.
- The one unsolved vanilla secret is solved: Tomahawk's sky bypass (18-1B: E-tank, big WE, big HP) is a Rush Jet route. Fly up from screen 0A's floor under the hanging ladder while holding UP; it takes 55-90 frames and 7 of the 19 fuel units. stages_b's '86 px limit' came from a test that stopped flying too early.
- Energy Balancer, seen in play: with the buster equipped, a weapon-energy pickup goes to the weapon with the lowest energy. Without the Balancer that pickup is wasted, and with a weapon equipped it refills that weapon. This matches PLAN 2.5's chip text.
- RAM map corrections: $57 and $046F switch to the new screen on the first frame of a vertical transition, and $0697 follows when the scroll ends (ram.md wrongly said vertical sections do not change $57). $0583 is the attack byte, $059A the hit-box id, and $056C the hit latch. The jump stores $FA.CC, not $FB.4C. $9E is the charge counter, $A1.$A0 the ice momentum, and $A7 the floor-type latch, not an animation id.
- Floor types are now decoded from the player code: 5 (and the remapped $15) is slippery ice with momentum, and Rockman slides 24-36 px after letting go on Blizzard ice. 9 is oil (lower jump $FB.CC, walking at 0.5 px per frame). 8 is water (gravity $00.18). $A/$C are updraft and fan, $E blocks Jet thrust, and 6 is the rideable Blizzard ship deck.
- Music id $14 is the GAME OVER jingle; engine.md had said the game over was silent. Id $15 is the password/continue screen music. Both were seen queued on a death with 0 lives and read in code at $3C:$801D-$8043 and $3F:$F2C6.
- PLAN 2.1's 'menu fixes' are already vanilla RM6 behaviour: closing the menu on a ladder keeps Rockman on it, and a held full charge survives the menu and fires on release. The E-tank heals +1 HP every 4 frames, so a full refill takes 108 frames ($38:$9537).
- PLAN 2.2's premise is wrong: the Jet does not drain energy. Fuel $9C is already a regenerating 19-unit stamina bar (-1 per 4 frames of flight, +1 per 2 frames otherwise, even in mid-air), and no adaptor uses weapon energy. Adaptor forms cannot use special weapons in vanilla, so every 'adaptor synergy' in PLAN needs new code.
- Only 4 Robot Master stages have alternate exits (Yamato E via Jet, Tomahawk B via the choice of ladder, Knight A via a charged punch, Centaur T via Jet). Blizzard, Wind, Plant and Flame have none, and $F518 and the flag tables have no plate bit for stages 0-3. PLAN 2.6's 'every venue has a secret exit' therefore needs new flags in save RAM; the branches themselves are pure data.
- Asset budget, computed uniformly by the critic: Robot Master stages use 221-255 of 256 32x32 blocks and 229-256 of 256 BG tile ids (Plant 0 free, Flame 27 free). Venues can keep a tileset and rewrite the layout freely, but new BG set pieces need replaced blocks and tiles or a new tileset slot (2 are empty: $2B:$92 and $2D:$92). PLAN 6.5's 'one ASCII character per 32x32 block' cannot cover 250+ block ids per stage.
- Vanilla has 8 fortress stages (Mr. X 1-4 = ids 8-11, Wily 1-4 = 12-15), 16 stage ids in all. The data-driven Wily 3 boss rush (tables $39:$8EC8/$8ED2/$8EDC) is the only place Robot Masters can be refought. The fully charged Power punch does 4 to every fortress boss and 2 to Robot Masters.

## Open questions

- Mr. X 1 riders: fortress.md measured 1 per charged-buster hit, but their damage code ($3B:$827A) subtracts the low nibble ($13 gives 3) for every class except C/D. The measurement probably let the large charged shot touch the front shell; a 16-px-behind glued test would settle it.
- Wily 1 (Mechazaurus): its table entry says Y.SPEAR does 4 but is unreachable, and how the buster and the other weapons reach the controller $E0 at all is unresolved.
- Fortress main routes were never walked in normal form, so 'normal exits never need an adaptor' is confirmed only for the 8 Robot Master stages.
- The meaning of collision 7 outside group 2 and of the remapped values $10-$1F other than $15 (fast ice), $1B, $1D and $1F.
- Whether the heal SFX $31 silences the triangle channel (PLAN 2.1 heal tweak).
- SFX $3D/$3E/$4D/$51 have no literal request site; they may be requested through tables, or be unused.
- The SUMMARY.md file itself: the harness blocks subagents from writing summary/report .md files. If the project wants it on disk, the orchestrator or user can save the coverage text verbatim as docs/research/rm6/SUMMARY.md.

_Written by the rm6-critic agent; saved verbatim from its report by the orchestrator, because subagents may not write report files._
