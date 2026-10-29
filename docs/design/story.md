# Rockman 6 GP: narrative bible and script plan (story.md)

Owner: design-story. Status: **v1** (written in parts; the container can restart, so the file is extended in place).
Scratch: `build/design/design-story/`.

Scope: everything the player **reads or hears said**:

- the tone guide (§1) and the cast (§2);
- every scene in play order with an EN draft and JP notes (§3-§4);
- the boss intro cards, in vanilla's boss-panel format (§5);
- the commentator system and its line tables, Mr. Y's fortress heckles included (§6);
- the judges' debrief hints (§7), the chip help pages (§8), ENGRISH (§9);
- the text-engine rules and how bilingual output works (§10);
- a fact sheet for every game-history claim the text makes (Appendix A).

Out of scope, owned elsewhere: stage layouts and boss patterns (`venues_a.md`, `venues_b.md`, `fortress.md`); weapon and
chip *effects*, the scorecard maths (`systems.md`); save bits, the bracket, the debrief *engine*, the rating
(`meta.md`); the MMC5 port, CHR streaming and the window raster split (`tech.md`); portraits, fonts as art, music
(`art_audio.md`). Where this doc needs something from them it says so in §12 (dependencies).

Binding inputs: `BRIEF.md` (overrides `PLAN.md`), the three research SUMMARY files, `rm6/text.md` for the text
engines and fonts. The venue docs' draft lines are adopted here by their stable ids (`BLZ-07`, `FLM-14`, …); this
doc is where they become final, in both languages.

Tags (BRIEF §8): **[engine-ok]** vanilla as-is or data only; **[new-code]**; **[new-art]**; **[new-music]**; size
**S / M / L**; tier **Must / Should / Could**. Text itself is data; a scene's tags describe what the scene needs
beyond its strings.

**How to read the scripts.** EN drafts are written in sentence case for readability; the build upper-cases all EN
(§10.3: ALL CAPS is the house style). `*word*` = the window's highlight colour. `/` = a forced line break. `▶YES NO`
= a choice. JP is kana only (no kanji, as vanilla), with spaces between phrases (vanilla's wakachigaki,
`rm6/text.md` §5.1). Speakers: **R** Rockman, **L** Dr. Light, **Ro** Roll, **C** Dr. Cossack, **K** Kalinka,
**E** Eddie, **BM** Break Man, **B** Bass β, **Y** Mr. Y, **W** Dr. Wily (after the unmasking).

---

## 0. The story in one page

**Logline.** One year after "Mr. X" was unmasked as Dr. Wily, the World Robot Championship comes back as the **Grand
Prix**: a real tournament with venues, judges, prize money and live commentary. Its new sponsor, **Mr. Y**, is
obviously Wily. Everyone says so, from the first screen to the last. He is.

**The two layers** (BRIEF §1): a sports tournament played straight (matches, scorecards, a bracket, a rival, a
championship), and a love letter to game history (venues that are eras of games, a fortress that is a museum of
Rockman 1-5, and a villain whose master plan is to force the whole world to upgrade to 16 bits, told in the last
NES Rockman).

| Act | Where (meta index) | What happens | Scenes |
|---|---|---|---|
| **0. Opening** | attract crawl; Opening Ceremony (0) | The GP is announced. Roll call of the 8 champions, the masked entrant 10 (Break Man) and the late "entrant β" (Bass β). Cossack reads the rules. The mascot goes rogue; Break Man teaches the charge shot | S01-S08 |
| **I. Round one** | bracket; any 4 venues (1-8) | Matches, scorecards, prize money. Roll fits Rush's POWER adaptor after the 2nd win and the JET after the 4th. Bass β crashes the bracket and postpones every other match | S09-S16 |
| **II. Semifinal** | Semifinal Riot (9) | Rockman vs Bass β, in a stadium full of Mr. Y's hired "fans". Break Man holds the crowd. Rule 9 makes tag teams legal; Break Man becomes Rock's partner. Mr. Y opens a shady booth | S17-S21 |
| **III. Round two** | the other 4 venues; Exhibitions (10-13) | The countdown to the final. Secret exits light exhibition badges; four arcade legends play by their own rules | S22-S24 |
| **IV. Hall of Fame** | H1-H5 (14-18) | At the trophy ceremony Mr. Y steals the GP Cup with a crane claw (Cossack's, from 1991). The final moves to the Hall of Fame, a museum of Rockman 1-5 whose exhibits Mr. Y has "upgraded" to MK-VI. Museum plaques open each wing. The Super Adaptor waits under glass in H3. A fake Break Man guards H5. Then the unmasking: "WE KNOW." | S25-S33 |
| **V. Project SUPER** | Super Wily Castle W1-W3 (19-21) | Wily's plan: upgrade every robot on Earth to 16 bits, by force. The castle upgrades itself as you climb (Game Boy greens, NES, "16-bit"). Bass β's second duel. Wily Machine 6.5 over a Mode 7-style floor, the capsule, the escape; Break Man carries Rock out of the rubble (Rockman 3's ending) | S34-S41 |
| **VI. Ending** | ending; victory lap (23); rating | The stadium's lights go out one sound channel at a time. The CAPCOM TIMES. The playable victory-lap credits. The championship rating, Break Man's debrief, and vanilla's last line: TO BE CONTINUED | S42-S48 |
| **Post-game** | bracket; Mr. X Returns (22, Could) | "Welcome back, champion." The real Mr. X wants his name back | S49-S51 |

**STORY_BEAT** (FILE `$013`, `meta.md` §1.6; this doc owns the values). It is a monotonic act counter used to pick
dialogue variants; the bracket logic itself reads STAGE_CLEAR (`meta.md` §3.5), never this byte.

| Value | Name | Set when | What it changes in text |
|---|---|---|---|
| `$00` | NEW | file created | — |
| `$01` | OPENED | Opening Ceremony cleared | bracket lines start |
| `$02` | SEMI_DONE | Semifinal cleared | Break Man lines in venues (if joined); booth lines |
| `$03` | CUP_STOLEN | trophy theft played (EVENTS b4) | Hall of Fame map lines; Mr. Y heckles active |
| `$04`-`$08` | H1 … H5 | each wing cleared | plaque gallery; heckle variants |
| `$09` | UNMASKED | unmasking played (EVENTS b6) | the speaker "Mr. Y" becomes "Dr. Wily" in every table; the judges' desk chair is empty |
| `$0A`-`$0B` | W1, W2 | castle stages cleared | W3 heckles |
| `$0C` | CHAMPION | W3 cleared (ending seen) | post-game lines; the file card ★ |
| `$0D`-`$FF` | reserved | | |

---

## 1. Tone guide

### 1.1 The four voices

The game speaks in four registers. Every line belongs to one of them; a scene may mix them, a single line should not.

| Voice | What it sounds like | Model | Example |
|---|---|---|---|
| **Sports broadcast, played straight** | Cossack and Kalinka call the action like a real tournament: stats, records, replays, "the judges are not pleased". The comedy comes from treating a robot massacre as a sporting event | CX's straight-faced villain inversion (cx SUMMARY §5) | C: "A clean match from Rockman. The judges will remember that slide." |
| **CX-level silliness** | Absurd escalation, fourth-wall winks, jokes that are mechanics (a YES that kills you, a seal union, a mascot full of the sponsor's helium) | CX's 24 moments; 4MI's ENGRISH | K: "Don't hurt the seals! They're union workers!" |
| **Sincere game-history affection** | Plaques, credits, a thank-you to fan designers, true trivia told with care. Never sarcastic about the games it quotes | 4MI's tributes (its imports, its credits) | Plaque: "Beat a master, take his weapon: the rule every Rockman since has followed." |
| **The farewell to 8-bit** | Quiet, warm, a little sad. Used rarely: the castle's palette tiers, Wily's speech, the ending's lights going out channel by channel, the last plaque | the last NES Rockman (1993) | L: "Every machine I build will be outdone by the next one. That isn't sad, Rock. That's the job." |

### 1.2 Rules

1. **A joke should be a mechanic or sit on one** (CX lesson 2). The best lines in this doc comment on something the
   player just did: a death, a secret, a weakness, a parry.
2. **Nobody is cruel.** The champions are good-natured rivals rebuilt by their fan designers (BRIEF §2): they
   trash-talk and they lose gracefully. Kalinka is a child: her jokes are never mean. Deaths are teased, never mocked.
3. **Content notes.** Tomahawk Man and Flame Man draw on real cultures in vanilla; GP's jokes target the *game genres*
   their venues quote (westerns, Prince of Persia), never their designs or cultures (`venues_a.md` §3.13). Cossack
   is a scientist and a father, not a Russian caricature: one "in my country" joke per venue at most. The doping
   trade-off (Y-TURBO) is about **cheating**, never drugs: it is a chip.
4. **Every fact is true.** A line that states game history must match Appendix A, which lists each claim with its
   source and confidence. A riddle may be oblique; it may not be wrong. When unsure, the line is rewritten to avoid
   the claim (several venue drafts were changed for this: §7.1).
5. **Parody names, never logos** (BRIEF §6). Text may *name* a real game when it credits or explains (plaques,
   tier-A riddles); on-screen titles of venues and guests use parody or generic names (§5.1 proposes PERSIAN PALACE
   for the on-screen name of Flame's venue).
6. **Short.** A pop-up page is ≤ 2 lines; a scene page ≤ 4. If a line needs a third, it is two pages or it is cut.
7. **Toggleable.** Every commentator line obeys CONFIG ANNOUNCER (ON / DEATHS ONLY / OFF, `meta.md` §11.1). Story
   scenes and the debrief are not commentary and always play (START skips a scene page).
8. **ENGRISH never touches story text, hints or help pages** (`meta.md` §12). It is a menu joke only (§9).

### 1.3 The running gag: Mr. Y is Wily

The gag works because it **escalates without the villain ever conceding**, until the unmasking, where he concedes
too eagerly and nobody cares. Its ladder, in play order:

| Step | Where | The gag |
|---|---|---|
| 1 | Attract crawl | "...the generous, the mysterious, the definitely-not-Wily... MR. Y!" Rock: "Doctor, that's Wily." |
| 2 | Opening rules | Light: "...It's Wily." Rock: "It's definitely Wily." (PLAN's line, kept.) Cossack: "His papers say 'Mr. Y'." |
| 3 | Judges' desk (every clear) | A cardboard Mr. Y always holds up a "1" on the sponsor's chair (`meta.md` §4.0) |
| 4 | Every venue | One cheap sign or prop: the MR. Y MARU icebreaker, the vizier on the balcony, the "Y-MAN SHALL COME" mural, the 1,000,000-ryo wanted poster, "WANTED: ROCKMAN, SPONSOR: MR. Y", and so on (venue docs) |
| 5 | The booth | A fake moustache worn **over his real moustache** (art: `art_audio.md` §3.2 "Mr. Y as Mr. X with a moustache") |
| 6 | Trophy theft | His saucer has a "Y" painted over a "W" |
| 7 | Hall of Fame heckles | In JP he speaks in an absurdly polite わたくし … でございます, and slips into Wily's わし … じゃ! when excited. In EN he slips on names: "Welcome to my castle— *a* castle." |
| 8 | Unmasking | "Surprise! It's me, Dr. Wi—" "WE KNOW." (PLAN, kept) |
| 9 | Ending | The CAPCOM TIMES: "MR. Z REGISTERS FOR NEXT YEAR'S GRAND PRIX" (the alphabet joke runs out of letters) |
| 10 | Post-game, Could | The real Mr. X, furious that Wily borrowed his name twice |

**Mirror gag: Break Man.** Mr. Y's disguise is transparent and he insists on it; everyone calls him Wily anyway.
Break Man's disguise is just as transparent (a visor and a scarf), and **everyone politely plays along**, because he
is honest. Rock says "Blues?" exactly twice in the game; Break Man answers "Break Man." both times. Light never says
the name until the very last scene, and only once.

### 1.4 The farewell to 8-bit

The game is set in the last NES Rockman, and Project SUPER is an upgrade the world did not ask for. The farewell
surfaces five times, each in the quiet voice:

1. **Wily's speech** after the unmasking: he is not wrong that the 8-bit era is ending; he is wrong to force it (S33).
2. **The Upgrade Lab** (W1): Kalinka notices the colours; Cossack notices the music getting more channels (S35).
3. **Wily Machine 6.5**: a machine halfway between 6 and 7, literally (S38). The number is the joke and the point.
4. **The ending**: the stadium shuts down one sound channel at a time, and Light says the line in §1.1 (S42).
5. **The last plaque**: the Hall of Fame gets a sixth wing, ROCKMAN 6 (1993), with this game's own true history
   (S43). The museum of the past ends on the game you are playing.

### 1.5 Voice per surface

| Surface | Speaker | Register |
|---|---|---|
| In-stage pop-ups | Cossack, Kalinka (Mr. Y / Wily in the fortress, Roll for adaptor tips) | broadcast + silliness |
| Story scenes | everyone | all four |
| Boss intro cards | the panel (English stats in both languages, as vanilla) + one line from the boss | broadcast |
| Judges' debrief | Kalinka | tier A: a riddle that rewards knowing the homage; tier B: a plain instruction |
| Chip help pages | the shop's catalogue voice (Eddie's) | dry, occasionally cryptic |
| Plaques | the museum | sincere; one joke per plaque at most, always last |
| Break Man's debrief | Break Man | terse, fond, never says "good job" outright |

---

## 2. The cast

Each sheet gives the role, the arc, the voice in EN and JP, signature lines and the rules for writing them.

### 2.1 Rockman (ロックマン / ロック)

- **Role:** the player; Dr. Light's wildcard entrant (he did not compete in the 1st Championship; he stopped it).
- **Arc:** competes in good faith in a tournament everyone knows is rigged; proves it can be won cleanly.
- **Voice EN:** earnest, polite, brief; deadpan when stating the obvious ("That's Wily."). Never quips during play.
- **Voice JP:** ぼく; です/ます to Light (はかせ), plain to friends. Vanilla's battle cry is kept: 「ゆくぞ!! ラッシュ!」.
- **Rules:** he speaks only in scenes, never in pop-ups. He says "Blues?" twice in the game (S06, S40). He never calls
  Mr. Y anything but "Wily".

### 2.2 Break Man (ブレイクマン) = Blues

- **Role:** the masked **entrant 10** (BRIEF §2). Rockman 3's alias, kept. Helps at key beats (the 4MI Proto Man
  pattern), then becomes the **tag partner** after the Semifinal (the CX Quick Man pattern; `systems.md` §11).
- **Arc:** registers alone, with no sponsor and no data; is never actually scheduled a match ("SEED: TBD"); watches
  Rock from the edges; joins him when the rules break; leaves him if Rock takes Mr. Y's money; carries him out of the
  castle at the end either way, because he is family.
- **Voice EN:** two to six words. "Hmph." "Hold B." "Your turn." Never explains himself. His whistle comes first.
- **Voice JP:** おれ; 「・・・ふん。」; plain, clipped endings (だ, しろ). Calls Rock 「ロック」, never 「ロックマン」.
- **Signature:** "...Break Man." (whenever someone says "Blues"); "Tch. Your turn." (retreat, `systems.md` §11).
- **Rules:** never jokes, but is the target of gentle ones (Cossack: "He brought his own theme music."). Never
  speaks in the judges' voice; the end-of-game debrief is his only long text (`meta.md` §6.2, restyled in S47).

### 2.3 Bass β (フォルテβ, "Bass beta")

- **Role:** Mr. Y's entrant and the rival (BRIEF §2). Built from Rockman's own tournament data, gathered by the
  judges' cameras that Mr. Y sponsored. The **β** is a version number: he is the beta build of the robot Wily will
  finish in 1995 (Rockman 7's Bass), and he hates hearing it.
- **Registration:** the bracket has ten numbered slots (8 champions, Rockman 9, Break Man 10), so Mr. Y registers him
  as **entrant β**. The committee is still arguing whether a Greek letter counts as a number.
- **Arc:** sneers at the "original"; crashes the bracket (Riot); loses duel 1 and blames bugs; loses duel 2 and
  promises the next one "won't be 8-bit" (PLAN's MM7 nod); escapes.
- **Voice EN:** loud, contemptuous, insecure about the β. "I'm the FINAL version!" Calls Rockman "original".
- **Voice JP:** オレ; rough endings (だ, ぜ, しろ); calls Rock 「オリジナル」 in katakana. Insists 「オレは
  さいしゅうばん だ!」.
- **Rules:** never wins a scene; always gets the last word anyway.

### 2.4 Mr. Y (Mr.Y) = Dr. Wily (Dr.ワイリー)

- **Role:** the sponsor; obviously Wily (§1.3). Before the unmasking every text table names him "MR. Y"; from
  STORY_BEAT `$09` on, the same slots read "DR. WILY".
- **The disguise:** Wily's own lab coat, sunglasses, a "Y" badge, and a fake moustache worn over his real one.
  Strictly less effort than last year's Mr. X.
- **The plan (Project SUPER):** the scorecard cameras record every match; the GP Cup is the data core that holds them;
  with the data he builds Bass β and the "SUPER" upgrade, a forced 16-bit conversion of every robot on Earth, all
  running Wily's own system. The trophy is the plan.
- **Voice EN (as Mr. Y):** a game-show host's smarm. "Pleasure doing business!" Slips: "Welcome to my castle— *a*
  castle." **(as Wily):** the classic ranting genius; begs on his knees when beaten (the dogeza, kept).
- **Voice JP (as Mr. Y):** わたくし, ございます, ございましょう; slips into わし and じゃ when excited, and Kalinka
  catches it: 「いま 'わし' って いった!」. **(as Wily):** わし, じゃ, ぞ; 「ワーッハッハッハ!」.
- **Rules:** he never admits it before S33. He heckles between lives in the fortress (§6.5, the CX Light 6 table).

### 2.5 Dr. Light (Dr.ライト)

- **Role:** Rockman's sponsor and creator. **Vanilla RM6 gives Light no lines at all** (`rm6/text.md` §5.7), so every
  line here is new.
- **Voice EN:** warm, wry, tired of Albert's nonsense; the only adult who never raises his voice. Delivers the
  farewell line (§1.1).
- **Voice JP:** わし; じゃ, のう; calls Rock 「ロック」, Wily 「ワイリー」 (and 「アルバート」 once, in S33).
- **Rules:** Light jokes only about Wily. He says "Blues" once, in the last scene.

### 2.6 Roll (ロール)

- **Role:** pit crew (BRIEF §2): adaptor hand-offs on the bracket (S12, S13), the Super Adaptor (S29), the lobby in GP
  Rush (`meta.md` §9.2.2). **Cameo:** Princess Roll in Knight's venue (`venues_a.md` §2.6: approved; "BUT THOU
  MUST!" is hers).
- **Voice EN:** brisk, practical, proud of Rush's fittings; teaches controls in-world. **JP:** わたし; よ, ね;
  「ロック!」.

### 2.7 Dr. Cossack (Dr.コサック) and Kalinka (カリンカ): the commentators

- **Role:** Cossack is head judge and play-by-play; Kalinka is colour commentary and the debrief speaker
  (`meta.md` §4.1). They sit at the judges' desk next to the empty sponsor's chair.
- **Cossack, voice EN:** a scientist doing sports: precise, dry, fond of statistics and of "lad". Guilt about 1991
  surfaces in H4 (his Cossack Catcher is an exhibit). **JP:** わたし; だ, だな; calls Rock 「ロックマン」.
- **Kalinka, voice EN:** quick, excited, knows game trivia nobody asked for ("Is that... Tango? From the Game
  Boy?"), calls her father "Papa". She "hears things": she is the one who knows where secrets are. **JP:** わたし;
  だよ, だね, じゃない!; calls him 「パパ」.
- **Rules:** never both talk on one page; an exchange is two pages. Cossack states, Kalinka reacts, or the reverse;
  the punchline goes to whoever did not set it up.

### 2.8 Eddie (エディ)

- **Role:** runs **Eddie's Pit Stop** (the shop, chips, the garage; `meta.md` §3.8). Speaks in shopkeeper bleeps.
- **Voice EN:** "WELCOME! *PIPIPI*" Short sales lines that rotate (§4, S10). **JP:** 「ピピッ! いらっしゃいませ!」.
- **Rule:** Eddie is never the butt of a moral joke here (4MI's "Eddie you can eat" is answered by Mr. Y's booth
  instead, `systems.md` §9.4).

### 2.9 Beat (ビート) and Rush (ラッシュ)

- **Beat:** collected as plates B-E-A-T; each plate is a chip slot (`systems.md` §10). Speaks only 「ピィ!」 / "PEEP!".
  Cossack built Beat in Rockman 5 (Appendix A, A-5.4), so every plate pickup gets a proud Cossack line (§6.3).
- **Rush:** "WOOF!" / 「ワン!」. Wears a **RENTAL** bib on the Committee's loaner jet in Wind's sortie (`venues_a.md` §1:
  approved).

### 2.10 The eight champions

Rebuilt by their original fan designers (the vanilla credit cards name them, `rm6/text.md` §5.6). Seeds 1-8 of the
bracket. Each has one personality hook, which drives their card line (§5), their trash talk at the bar fill, their
defeat line and their victory-lap cameo.

| Champion (DWNB card) | Designer (vanilla card) | Personality | EN voice | JP voice |
|---|---|---|---|---|
| **Blizzard Man** (41) | HIROFUMI OGAWA | A sunny optimist on a glacier who runs on SOLAR ENERGY and keeps trying to tan | "Fresh powder, Rockman!" | おれ, だぜ |
| **Centaur Man** (42) | KAZUKI KIDOGUCHI | A gentleman with a secret even from himself: ABILITY UNKNOWN (it turns out to be gambling). Sensitive about his DRY BATTERY | "Exciting, is it not?" | わたし, ですな |
| **Flame Man** (43) | NORITSUGU KUROKAWA | A theatrical showman and duelist; bows before every fight | "En garde!" | わがはい, だ |
| **Knight Man** (44) | DANIEL VALLIE | A chivalric ham who narrates his own attacks (the battle log) | "Hark! Have at thee!" | われ, であるぞ; calls Rock なんじ |
| **Plant Man** (45) | NOBUHIRO HOSHINO | A gentle gardener-explorer; apologises to the flowers | "Please mind the petunias." | わたし, ですよ |
| **Tomahawk Man** (46) | YOSHINOBU SUDA | The dignified champion of the frontier; laconic, fair, the Sheriff's friend | "Out west, we shake hands before the draw." | おれ, だ |
| **Wind Man** (47) | MICHAEL LEADER | A would-be ace pilot with a short attention span | "Tally-ho! Try to keep up!" | おれさま, だぜ |
| **Yamato Man** (48) | RAI ICHIKAWA | An honourable samurai, immovable and proud of it (DEFENCE 185, MOBILE 31) | "This one shall not move." | せっしゃ, でござる |

### 2.11 Exhibition guests (E1-E4)

Arcade legends who play by their own games' rules (BRIEF §6: a guest is a mechanic). Owner of the stages:
`fortress.md`. Their PLAN names are kept; their personalities are this doc's.

| Guest | Homage (year) | Personality | Line |
|---|---|---|---|
| **Block Man** (E1) | *Tetris* (1984) | Silent, orderly, mildly annoyed by gaps. Communicates only by clearing lines | "...(a single line clears)." K: "I think that was hello." |
| **Paddle Man** (E2) | *Breakout* (1976), *Arkanoid* (1986) | A bored goalkeeper; has been returning the same ball for decades | "Same ball. Every day. Same ball." |
| **Invader Man** (E3) | *Space Invaders* (1978) | Marches everywhere in step; speaks in descending tones | "WE. ARE. COMING. DOWN." |
| **Maze Man** (E4) | *Pac-Man* (1980) | Polite, always hungry; calls the four Met-ghosts his "roommates" | "Excuse me. Is that pellet yours?" |

**Name clash note.** "Block Man" is also a Rockman 11 Robot Master (2018). The joke is kept on purpose: K: "Block Man?
Isn't that name taken?" C: "Not until 2018." (Open question 4.)

### 2.12 The legacy bosses (Hall of Fame MK-VI exhibits)

Museum pieces Mr. Y "upgraded". They do not speak (they are machines), but their **exhibit cards** (§5.4) and plaques
(§4, S27) speak for them. Dark Man MK-VI speaks only in disguise, in Break Man's voice, badly.

| Exhibit | From | Its joke |
|---|---|---|
| **Yellow Devil MK-VI** (H1) | Rockman (1987) | It reassembles across the room block by block; the plaque hints at the SELECT trick (`systems.md` SC7) |
| **Mecha Dragon MK-VI** (H2) | Rockman 2 (1988) | It chases you across the sky again; Kalinka has the music in her head |
| **Gamma MK-VI** (H3) | Rockman 3 (1990) | Built by Light and Wily together "for peace"; "the head respects only a fist" (`systems.md` SC5) |
| **Cossack Catcher MK-VI** (H4) | Rockman 4 (1991) | Cossack's own machine, on loan to the museum. He commentates against it, guiltily |
| **Dark Man MK-VI** (H5) | Rockman 5 (1992) | Disguised as Break Man; the real one's whistle gives him away, as in 1992 |

### 2.13 Others

- **Grand Pi-kun** (グランピーくん): the GP mascot, an inflatable robot, grumpy because nobody watches the mascot (the
  name is a pun on グランプリ and "grumpy"). Filled with Mr. Y-brand helium, it goes rogue in the Opening. Squeaks only.
- **The Committee**: offstage. Represented by the rulebook, which Cossack reads aloud and occasionally disagrees with.
- **Mr. X, the real one** (Could, `meta.md` §9.8): a real, separate person, furious that Wily borrowed his name in
  1993 and then the next letter this year. Speaks like an offended aristocrat.
- **Venue NPCs** (King, Sage, Innkeeper, Sheriff, the conductor, the vizier, Tango the cat, the seals' union …):
  their lines are in the venue docs; §4 S15 lists them with their JP notes.

---

## 3. The scene list, in play order

"Engine" names the surface (§10.1): **SCN** = a full-screen scene in the new text engine (4-line window or full page,
portraits); **POP** = the in-stage pop-up (2 lines, face icon); **NPC** = a T2 window opened by an object
(`venues_a.md` §0.4); **PNL** = vanilla's boss panel typer `$3C:$81B1`; **PPU** = a vanilla PPU script. "Seen" is the
save bit that makes a scene play once (`meta.md` §1.6 EVENTS / EVENTS2), or `—` if it plays every time.

| Id | Scene | Trigger | Engine | Seen / beat | Tags | Tier |
|---|---|---|---|---|---|---|
| S01 | License line | boot | PPU | — | [engine-ok] S | Must |
| S02 | Attract crawl (6 panels) | title idle / boot | SCN | — | [new-code] S (crawl driver = vanilla bytecode `$3D:$BD00` with new scripts), [new-art] S (3 new pictures) | Should |
| S03 | The players' tunnel | Opening, stage start | SCN | — | text | Must |
| S04 | Roll at the pit; Eddie's closed stall | Opening, NPCs | NPC | — | text | Must |
| S05 | Roll call: the 8 champions | Opening, parade screens | POP | — | text, [new-art] (podium sprites: `art_audio.md`) | Should |
| S06 | Entrants 10 and β | Opening, after the parade | SCN | — | text | Must |
| S07 | The tournament rules | Opening, the big screen | SCN | — | text | Must |
| S08 | Grand Pi-kun; Break Man's tip; the bracket reveal | Opening boss | POP + SCN | STORY_BEAT → `$01` | text | Must |
| S09 | Bracket lines (first visit, centre states, POSTPONED, badges) | bracket | POP (bracket window) | — | text | Must |
| S10 | Eddie's Pit Stop lines | pit stop | NPC | — | text | Must |
| S11 | Per match: card, bar-fill line, defeat line, YOU GET | every champion match | PNL + POP + PPU | — | text | Must |
| S12 | POWER hand-off | bracket, 2nd win | SCN (bracket) | EVENTS b0 | text | Must |
| S13 | JET hand-off | bracket, 4th win | SCN (bracket) | EVENTS b1 | text | Must |
| S14 | The Riot intro | bracket, after S13 | SCN (bracket) | EVENTS b2 | text (+ meta's animation, Should) | Must (lines) |
| S15 | Venue NPC lines (index) | venues | NPC | — | text | per venue |
| S16 | Game over, RETIRE, unplug lines | game over; load with IN_MATCH | POP / SCN | — | text | Must |
| S17 | Semifinal night | Semifinal start | POP | — | text | Must |
| S18 | Break Man holds the crowd | Semifinal, mid-stage set piece | POP | — | text; set piece `fortress.md` | Should |
| S19 | Bass β, duel 1 | Semifinal boss | SCN + POP | RATEFLAGS b2 on no damage | text | Must |
| S20 | Rule 9: Break Man joins | bracket, after the Semifinal | SCN (bracket) | EVENTS b3, b5 | text | Should (with SYS-TAG-1) |
| S21 | Mr. Y's booth; Break Man walks | pit stop row; bracket | SCN | EVENTS2 b5 | text | Should (with SYS-CHP-4) |
| S22 | Exhibition badges light | bracket | SCN (bracket) | EVENTS2 b0-3 | text | Should |
| S23 | Exhibition matches: guests and plaques | E1-E4 | PNL + POP + SCN | — | text | Should |
| S24 | The countdown | bracket centre | POP (bracket window) | — | text | Must |
| S25 | Trophy ceremony and theft | START on the lit trophy | SCN | EVENTS b4; STORY_BEAT → `$03` | text, [new-art] M (claw, saucer), [new-music] S (ceremony fanfare: `art_audio.md`) | Must |
| S26 | The Hall of Fame map | fortress map, first visit | SCN | — | text | Must |
| S27 | Museum plaques H1-H5, two thanks plaques | wing entry; hidden rooms | SCN (plaque page) | Museum PLAQUE GALLERY bits | text, [new-art] S (plaque frame) | Must (H1, H3, H5), Should (H2, H4) |
| S28 | Exhibit lines; Mr. X's business card | wing bosses; card pickup | POP + SCN | RATEFLAGS b1 | text | Must / Should |
| S29 | The Super Adaptor | after H3 | SCN (map) | EVENTS2 b4 | text | Must |
| S30 | H5: the fake Break Man | H5 boss room | SCN | — | text | Must |
| S31 | Mr. Y's heckles between lives | every respawn in H1-W3 | POP | — | text (§6.5) | Must |
| S32 | The cup on the pedestal | after H5 | SCN | — | text | Must |
| S33 | The unmasking; Project SUPER | after S32 | SCN | EVENTS b6; STORY_BEAT → `$09` | text | Must |
| S34 | Super Wily Castle map | castle map, first visit | SCN | — | text | Must |
| S35 | W1: the Upgrade Lab | W1 palette tiers; W1 boss | POP | — | text | Should |
| S36 | W2: the Bracket of Doom | W2 hub; refights | POP | — | text | Must |
| S37 | Bass β, duel 2 | W2 boss | SCN + POP | — | text | Must |
| S38 | Wily Machine 6.5 | W3 boss | SCN + POP | — | text | Must |
| S39 | The Wily Capsule; the dogeza | W3 second fight | SCN | — | text | Must |
| S40 | The castle falls; Break Man carries Rock out | W3 escape end | SCN | — | text, [new-art] S (Break Man carrying Rock) | Must (Should for the carry art) |
| S41 | Wily to jail: "Mr. Z" | after S40 | SCN | STORY_BEAT → `$0C` | text | Must |
| S42 | Lights out, one channel at a time | ending | SCN | — | text, [new-music] S (an ending arrangement with per-channel stems) | Must |
| S43 | The sixth wing | ending | SCN (plaque page) | — | text | Must |
| S44 | The CAPCOM TIMES | ending | vanilla newspaper driver `$3B:$A886` | — | text, [new-art] S (3 headline variants) | Must |
| S45 | The victory lap (playable credits) | after S44 | stage + POP + credit text | — | text; the level is `fortress.md`'s | Should |
| S46 | The championship rating | after S45 | `meta.md` §6 | — | text | Must |
| S47 | Break Man's debrief | after S46 | SCN | — | text | Must |
| S48 | TO BE CONTINUED | after S47 | PPU `$88` (vanilla, kept) | — | [engine-ok] | Must |
| S49 | Post-game bracket intro | bracket, first visit after the ending | SCN (bracket) | EVENTS b7 | text | Should |
| S50 | Mr. X Returns | U1.5 | SCN | — | text | Could |
| S51 | Bass Mode line swaps | BASS files | all | — | text | Could |

---

## 4. Scripts

Each scene: where it plays, then the lines. JP is a draft for a native-speaker pass (§13 risk 2). Line lengths obey
§10.2 (28 cells per line; a POP page is ≤ 2 lines, a SCN page ≤ 4).

### Act 0: the Opening

#### S01 License line [engine-ok] S Must

Vanilla script `$1F` (the copyright lines) plus one line, in English in both languages, as vanilla's own boot screen
is: `ROCKMAN 6 GP - A FAN PATCH. NOT MADE BY CAPCOM.` Main font (A=`$0B`) has every glyph but `-`; use the RLE
`ー` tile or add `-` (§10.1).

#### S02 Attract crawl [new-code] S, [new-art] S · Should

Replaces vanilla scripts `$50-$5E` (`rm6/text.md` §5.1). It keeps vanilla's first card, `IN THE YEAR 20XX AD・・・`,
untouched (English in both languages, as vanilla), and vanilla's bytecode driver (`$3D:$BD00`, op `D` = typewriter at
2 f/char). Any button skips the whole crawl, as vanilla.

| Panel | Picture | EN | JP |
|---|---|---|---|
| 0 | black | IN THE YEAR 20XX AD... (vanilla, kept) | (same, English) |
| 1 | vanilla tournament picture (`$57-$5A`) | Last year the 1st World Robot Championship was hijacked by its own sponsor, the mysterious Mr. X. / Rockman stopped him. Mr. X was Dr. Wily all along. | きょねんの だい1かい せかいロボット せんしゅけんは スポンサーの Mr.X に のっとられた。 / ロックマンが それを くいとめた。 Mr.X の しょうたいは Dr.ワイリー だった。 |
| 2 | **new**: a jail cell with a cardboard Wily cut-out in it | Wily went to jail. The CAPCOM TIMES warned that he might build a jailbreak robot in his cell. / This year the jail reports that he is still there. | ワイリーは ろうやへ。 「ろうやで だつごくよう ロボットを つくって いるかも しれない」と カプコンタイムスは かいた。 / ことし けいむしょは 「ワイリーは まだ いる」と はっぴょう している。 |
| 3 | **new**: the GP stadium at night, searchlights | Now the Committee wants its honour back. / Presenting the WORLD ROBOT GRAND PRIX: eight venues, eight champions, real judges, real prize money! | いいんかいは めいよばんかいを ちかった。 / せかいロボット グランプリ かいさい! 8つの かいじょう、 8にんの チャンピオン、 ほんものの しんさいんと しょうきん! |
| 4 | vanilla robot pictures (`$53-$56`) | The champions are back, rebuilt by the fans who designed them. | チャンピオンたちが かえってきた。 かれらを うみだした ファンの てで パワーアップ して! |
| 5 | **new**: Mr. Y in the sponsor's box (Mr. X sprite + "Y" badge + second moustache) | And this year's sponsor... / the generous, the mysterious, the definitely-not-Wily... MR. Y! | そして ことしの スポンサーは・・・ / ナゾの だいふごう。 ぜったいに ワイリーでは ない・・・ Mr.Y! |
| 6 | vanilla Rock and Rush (`$48`) | R: "Doctor... that's Wily." / L: "Of course it is. Enter anyway, Rock. If he's paying for it, someone honest had better win it." / R: "Let's go, Rush!" | R「はかせ・・・ あれ ワイリー ですよね。」 / L「もちろん そうじゃ。 だが でるのじゃ ロック。 あいつが かねを だすなら しょうじきものが かたねば。」 / R「ゆくぞ!! ラッシュ!」 (vanilla's own line, `$4A`) |

Panel 2 sets up two payoffs: the jail guards in S44 and Wily's line in S41. Panel 6 ends on vanilla's battle cry.

#### S03 The players' tunnel · Must

Opening Ceremony, its first screen (`fortress.md` §1 owns the layout). SCN window over the stage, 3 pages.

| Who | EN | JP |
|---|---|---|
| L | Rock, this year it's a real tournament. Judges, points, prize money. Win cleanly. | ロック、 ことしは ほんものの たいかいじゃ。 しんさいん、 てんすう、 しょうきん。 せいせいどうどうと かつのじゃぞ。 |
| R | And Mr. Y? | Mr.Y の ことは? |
| L | Win cleanly, *and* keep an eye on Mr. Y. | せいせいどうどうと かって、 *Mr.Y からは めを はなすな*。 |

#### S04 Roll at the pit; Eddie's closed stall · Must

NPCs on the concourse (T2 windows, UP to talk). Roll teaches that adaptors come later; Eddie's stall teaches that the
shop exists.

| Who | EN | JP |
|---|---|---|
| Ro | Pit crew reporting! That's me. Rush is getting his adaptors fitted, so your first two matches are solo. | ピットクルー さんじょう! わたしの ことよ。 ラッシュは アダプターの ちょうせいちゅう。 さいしょの 2しあいは ひとりで がんばって! |
| Ro | After a match, see Eddie. Prize money buys chips! | しあいの あとは エディの おみせへ。 しょうきんで チップが かえるわ! |
| sign | EDDIE'S PIT STOP. OPENS AFTER YOUR FIRST MATCH. | エディの ピットストップ。 さいしょの しあいの あと オープン。 |
| E (behind the shutter) | *PIPIPI* ...closed! | ピピッ・・・ じゅんびちゅう! |

#### S05 Roll call: the eight champions [new-art] (podiums) · Should

The Opening's parade screens pass eight podiums. As Rockman reaches each one, a POP: Kalinka introduces, the champion
answers (2 pages, auto-advance). The location is vanilla's panel LOCATION, translated in JP.

| Champion | K (EN) | Champion (EN) | JP (K / champion) |
|---|---|---|---|
| Blizzard | From FROZEN ISLAND: Blizzard Man! | Hey, Rockman! Bring sunscreen to my match. I'm serious. | こおりの しまから ブリザードマン! / よう ロックマン! おれの しあいには ひやけどめを もってこいよ。 マジだぜ。 |
| Wind | From the MECHANICAL TOWER: Wind Man! | Ace pilot Wind Man, reporting! Try to keep up. Nobody does! | きかいの とうから ウインドマン! / エースパイロット ウインドマンさま さんじょう! ついてこれるかな? だれも こられないぜ! |
| Plant | From the FORGOTTEN AREA: Plant Man! | Welcome! Please mind the flowers in my jungle. | わすれられた ちいきから プラントマン! / ようこそ! ジャングルの おはなを ふまないで くださいね。 |
| Flame | From the OIL FIELD: Flame Man! | Welcome to my palace, friend. The floor is... mostly safe. | ゆでんから フレイムマン! / わがはいの きゅうでんへ ようこそ。 ゆかは・・・ だいたい あんぜんだ。 |
| Yamato | From the IMPREGNABLE FORTRESS: Yamato Man! | This one shall wait for you. This one shall not move. This one never moves. | なんこうふらくの とりでから ヤマトマン! / せっしゃ まって おるで ござる。 うごかぬ。 せっしゃは けっして うごかぬ。 |
| Tomahawk | From the RESTRICTED AREA: Tomahawk Man! | Good luck, Rockman. Out west, we shake hands before the draw. | たちいりきんし くいきから トマホークマン! / がんばれよ ロックマン。 けっとうの まえに あくしゅ する。 それが おれたちの やりかただ。 |
| Knight | From the CAPITAL OF SCIENCE: Knight Man! | Hark! A challenger approaches! ...That is thee. Hark! | かがくの みやこから ナイトマン! / きけ! ちょうせんしゃが ちかづいて おるぞ! ・・・なんじの ことだ。 きけ! |
| Centaur | From the ANCIENT CITY: Centaur Man! | My specialty? Ability unknown. Even to me. Exciting, is it not? | こだいとしから ケンタウロスマン! / わたしの とくぎ ですか? ふめい です。 わたしにも わかりません。 たのしみ ですな? |

#### S06 Entrants 10 and β · Must

SCN on the parade's last screen. Break Man's whistle (`systems.md` §11's jingle) plays before his first page.

| Who | EN | JP |
|---|---|---|
| K | Entrant ten... BREAK MAN! Sponsor: none. Data: none. | エントリー ナンバー10・・・ ブレイクマン! スポンサー なし。 データ なし。 |
| C | He brought his own theme music. | テーマソングは もちこみ らしい。 |
| R | ...Blues? | ・・・ブルース? |
| BM | Break Man. | ブレイクマンだ。 |
| K | And a late entry! Registered one minute before the deadline... entrant β! | そして かけこみ エントリー! しめきり 1ぷんまえに とうろく された・・・ エントリー ナンバーβ! |
| B (lands; screen shakes) | So you're the "original". I'm the upgrade. | おまえが 'オリジナル' か。 オレは アップグレードばん だ。 |
| K | β? That's not a number! | β って かずじゃ ないよ! |
| C | It is a letter. Mr. Y says his robot is "in beta". | もじ だな。 Mr.Y いわく 「まだ ベータばん」 だそうだ。 |
| B | I'm the FINAL version! (dashes off) | オレは さいしゅうばん だ!! |

#### S07 The tournament rules · Must

The stadium's big screen; SCN with Cossack's and Kalinka's portraits. Every number must match `systems.md` §6 and
`meta.md` §3; the rules are the tutorial for the meta layer. 11 pages; START skips the rest.

| # | Who | EN | JP |
|---|---|---|---|
| 1 | C | Rule 1. Eight venues, eight champions, any order. Beat a champion and take the champion's weapon. | ルール1。 8つの かいじょうに 8にんの チャンピオン。 じゅんばんは じゆう。 かてば その ぶきが てに はいる。 |
| 2 | K | Same as always! | いつもどおり だね! |
| 3 | C | Rule 2. Every match is judged out of 100. TIME 20, DAMAGE 20, VARIETY 25, SECRETS 20, STYLE 15. | ルール2。 しあいは 100てんまんてんで しんさ する。 タイム20 ダメージ20 バラエティ25 シークレット20 スタイル15。 |
| 4 | K | Variety is worth the most. The judges *like variety*! | いちばん おおきいのは バラエティ! しんさいんは *いろんな ぶきが すき* なんだよ! |
| 5 | C | Rule 3. Medals at 40, 60, 80 and 95. Prize money is paid in bolts. A rematch pays only what you improve. | ルール3。 40 60 80 95てんで メダル。 しょうきんは ボルトで しはらう。 さいせんは のびた ぶん だけ。 |
| 6 | C | Rule 4. Spend bolts at Eddie's Pit Stop. Press SELECT on the bracket. | ルール4。 ボルトは エディの ピットストップで。 トーナメントひょうで セレクト だ。 |
| 7 | C | Rule 5. Partner robots may join after an entrant's 2nd win, and again after the 4th. After the 4th: the Semifinal. | ルール5。 パートナーロボは 2しょうめと 4しょうめの あとに さんか できる。 4しょうめの あとは じゅんけっしょう。 |
| 8 | C | Rule 6. Every venue *hides* a secret exit. Two that share a badge open an exhibition match. ...Why does a rulebook say "hides"? | ルール6。 かくかいじょうには ひみつの でぐちが *かくされて いる*。 おなじ バッジの 2つで エキシビション。 ・・・なぜ ルールブックに 「かくされて」 と? |
| 9 | K | I know why! | わたしは しってるよ! |
| 10 | C | Rule 7. This Grand Prix is proudly sponsored by... Mr. Y. (the screen cuts to Mr. Y, waving) | ルール7。 この グランプリの スポンサーは・・・ Mr.Y さま です。 |
| 11 | L / R | L: "...It's Wily." R: "It's definitely Wily." | L「・・・ワイリーじゃ。」 R「ぜったい ワイリー です。」 |
| 12 | C / K | C: "We have checked. His papers say Mr. Y." K: "His papers are in crayon." | C「しらべたとも。 しょるいには Mr.Y と ある。」 K「クレヨンで かいてあるよ。」 |
| 13 | C | Rule 9. If a sponsor interferes in a match, the other entrant may name a tag partner. | ルール9。 スポンサーが しあいに かいにゅう したら あいては タッグパートナーを ひとり よべる。 |
| 14 | K / C | K: "What happened to Rule 8?" C: "Rule 8 is: do not ask about Rule 8." | K「ルール8は?」 C「ルール8。 ルール8に ついて きいては ならない。」 |

Rule 9 is the setup for S20; Rule 8 pays off in S18.

#### S08 Grand Pi-kun; Break Man's tip; the bracket reveal · Must

The Opening's boss room (`systems.md` §4.5: HP 14, the charge tutorial). The window is a SCN before the bar fills,
then a POP for Break Man (he is not on screen; only his whistle).

| Who | EN | JP |
|---|---|---|
| K | And now, give it up for our mascot... GRAND PI-KUN! | それでは みなさん ごいっしょに! マスコットの グランピーくん~! |
| (Pi-kun squeaks and sags) | | |
| C | ...Who filled the mascot with *Mr. Y brand helium*? | ・・・マスコットに *Mr.Y じるしの ヘリウム* を いれたのは だれだ? |
| (Pi-kun inflates to fill the room; the shutters close) | | |
| BM (POP, whistle first) | Hold B. Let go when you glow. | Bを おしつづけろ。 ひかったら はなせ。 |
| K (on the kill) | The mascot is down! The Grand Prix is OPEN! | マスコット ダウン! グランプリ かいまく~! |
| C | Someone please return the mascot to the gift shop. | だれか マスコットを ばいてんへ もどして おいてくれ。 |
| K (bracket, first frame) | Here's the bracket! Pick any venue. The judges are watching! | これが トーナメントひょう! すきな かいじょうを えらんでね。 しんさいんが みてるよ! |

Death in this fight (POP, once): K: "Charge it up, Rockman! Somebody said so!" / 「チャージだよ ロックマン! だれかが そう いってた!」

### Act I: round one

#### S09 Bracket lines · Must

Kalinka in the bracket's message window (`meta.md` §3.3-3.4 owns the states; this doc owns the words). The bracket
font cannot print `!`, `?`, `'` or `:` (A=`$2B`, §10.1), so these lines use the new engine's window, and the node
labels stay in the stage-select font.

| Where | EN | JP |
|---|---|---|
| first visit | SELECT opens Eddie's Pit Stop. B shows the exhibition badges, once one lights up. | セレクトで エディの ピットストップ。 バッジが ひかったら Bで エキシビション。 |
| centre, < 4 wins | The final? Win some matches first! | けっしょう? まずは しあいに かってから! |
| a POSTPONED frame | Rain delay! ...It's not raining. It's Bass. | あめで えんき! ・・・ふってないけど。 フォルテの せい。 |
| a HALF badge | One more secret exit: %NAME%'s venue! | あと ひとつ! %NAME%の かいじょうの ひみつの でぐち! |
| a cleared frame (rematch) | A rematch! The judges love a comeback. | さいせん! しんさいんは カムバックが だいすき。 |
| SECRET exit star on a frame | That star means you found the back way. | その ほしは うらみちを みつけた しるし。 |

#### S10 Eddie's Pit Stop · Must

Eddie's rotating lines (one per visit, by a counter). Bleeps are text, not SFX.

| Event | EN | JP |
|---|---|---|
| open (rotates) | WELCOME! *PIPIPI* / Bolts in, chips out! / No refunds. I don't have arms. / Every chip is an excellent choice. That one too. / Slots? Beat plates make slots. I just sell. | ピピッ! いらっしゃいませ! / ボルトを いれると チップが でます! / へんぴんは できません。 うでが ないので。 / どの チップも おめが たかい。 それも。 / スロットは ビートの プレートで ふえます。 わたしは うる だけ。 |
| bought | Thank you! *PIPIPI* | まいど! ピピッ! |
| too poor | Not enough bolts! Go win something! | ボルトが たりません! かってきて! |
| garage, build | Two PARTs, one chip. Eddie's math! | パーツ ふたつで チップ ひとつ。 エディけいさん! |
| leave | Come back soon! I'll be here. I'm a shop. | また きてね! ずっと ここに います。 おみせ なので。 |
| 1993 file (shop closed) | Shop's closed. It's 1993! *pipi...* | おみせは おやすみ。 1993ねん なので! ピピ・・・ |

#### S11 Per match: card, bar fill, defeat, YOU GET · Must

1. **The match card** (PNL): §5.2's record for the champion, typed by vanilla's `$3C:$81B1`, plus the VENUE field.
2. **The bar fill** (POP, the champion speaks): one line per champion, below. A secret-room fight uses the second
   line; a rematch uses K's generic "A rematch!" line instead.
3. **The defeat line** (POP, after the explosion, before YOU GET).
4. **YOU GET** (PPU, vanilla `$60 + $51 + $06A5` scripts): the weapon, plus `AND BEAT x-PARTS` where the plate came
   with the kill. **Adaptors are never announced on YOU GET** (Roll does it on the bracket, S12/S13), which avoids a
   three-line card and removes the vanilla `AND RUSH JET ADAPTOR` coupling to Plant Man (`venues_a.md` §4.7.4 asked;
   this is the answer). `C.FLRSH` stays misspelled on the card in every language (`systems.md` §3.9; CEN-20 jokes
   about it).

| Champion | Bar fill (EN / JP) | Secret-room bar fill (EN / JP) | Defeat (EN / JP) |
|---|---|---|---|
| Blizzard | Fresh powder and solar panels! Let's go! / しんせつと ソーラーパネル! いくぜ! | Up here the sun never sets! ...It's behind a cloud, but still! / ここなら たいようが しずまない! ・・・くもに かくれてるけどな! | Brr... I'll go thaw out. Good match, Rockman! / さむっ・・・ ちょっと とけて くるぜ。 いい しあい だったな! |
| Wind | Tally-ho! Wind Man, cleared for combat! / タリホー! ウインドマン せんとう かいし! | A fight on a flying wing! Now THIS is flying! / とんでる つばさの うえで しょうぶ! これぞ フライトだ! | Mayday... Good flying. Next time I'm the ace. / メーデー・・・ いい フライト だったぜ。 つぎは おれが エースだ。 |
| Plant | Please don't trample anything. Including me. / なにも ふまないで くださいね。 わたしも ふくめて。 | You found the Lost City! Then you've earned a real fight. / ロストシティを みつけましたね! では ほんきで いきます。 | Oh... you were gentle with the flowers. Thank you. / ああ・・・ おはなを だいじに して くれましたね。 ありがとう。 |
| Flame | En garde! / アン・ギャルド! | You came through the mirror? Then meet MY shadow. / かがみを ぬけて きたか? ならば わがはいの かげと たたかえ。 | Touché! A splendid duel. The palace salutes you! / まいった! みごとな けっとう だ。 きゅうでんが きみを たたえる! |
| Yamato | This one shall not move. Come to me. / せっしゃは うごかぬ。 かかって まいれ。 | The stage turns, but this one does not. / ぶたいは まわれど せっしゃは まわらぬ。 | This one... moved. A little. Well fought. / せっしゃ・・・ うごいて しもうた。 すこしだけ。 みごとで ござる。 |
| Tomahawk | (after HIGH NOON) Fair draw. Now let's see your aim. / フェアな ドローだ。 つぎは うでまえを みせて もらおう。 | That poster? Mr. Y put it up. I'm not collecting. / あの てはいしょ? Mr.Y が はったんだ。 おれは しらん。 | You're quick, Rockman. The fastest I've faced. Shake? / はやいな ロックマン。 いままでで いちばんだ。 あくしゅ しよう。 |
| Knight | (the battle log speaks: "KNIGHT MAN DRAWS NEAR!") / 「ナイトマンが あらわれた!」 | If thou wilt join me, I shall give thee half the bracket. (the venue's YES/NO, `venues_a.md` §2.8.4) / もし わしの みかたに なれば トーナメントの はんぶんを なんじに やろう。 | Thou hast bested me. A fine bout! Huzzah! / なんじの かちだ。 みごとな しょうぶで あった! ばんざい! |
| Centaur | Shall we find out my ability together? / わたしの のうりょく、 いっしょに たしかめましょうか? | Down here, I am a sea-centaur. That's a new one even for me. / ここでは わたしは うみの ケンタウロス。 わたしも はじめて です。 | So it was luck all along. How exciting! I lost. / けっきょく うん だったの ですな。 たのしかった! まけましたが。 |

The Knightlord's offer quotes Dragon Quest's Dragonlord, who offers the hero half the world (JP: せかいの はんぶん).
The JP line keeps the archaic わし / なんじ register of the original; EN keeps `venues_a.md`'s wording.

#### S12 POWER hand-off (EVENTS b0) · Must

On the bracket after the 2nd venue win: Roll's portrait with Rush. Then the vanilla Rush-docking cutscene plays the
first time the form is used (`systems.md` §1.3, FORM_DEBUT).

| Who | EN | JP |
|---|---|---|
| Ro | Rock! Rush's POWER adaptor passed inspection! | ロック! ラッシュの パワーアダプター けんさ ごうかく! |
| Rush | WOOF! | ワン! |
| Ro | Hold SELECT and press LEFT or RIGHT to dock. The punch breaks cracked blocks, and you can still fire your weapons! | セレクトを おしながら ひだりか みぎで ドッキング。 パンチで ひびわれた ブロックも こわせるし ぶきも うてるわ! |
| Ro | And the judges count the punch as its own weapon. Variety points! | しんさいんは パンチも ぶきの ひとつに かぞえるの。 バラエティ ポイントよ! |

#### S13 JET hand-off (EVENTS b1) · Must

On the bracket after the 4th win, immediately followed by S14 (`meta.md` §3.5: JET, then Riot).

| Who | EN | JP |
|---|---|---|
| Ro | JET adaptor fitted! Nineteen units of fuel, and it refills whenever you're not flying. | ジェットアダプター そうちゃく! ねんりょうは 19。 とんで いない ときは かってに たまるわ。 |
| Ro | Same controls: SELECT, then LEFT or RIGHT. | そうさは おなじ。 セレクトと ひだり みぎよ。 |
| Rush | WOOF WOOF! | ワンワン! |
| Ro | ...Rock? Why is the bracket shaking? | ・・・あれ? トーナメントひょうが ゆれてる? |

#### S14 The Riot intro (EVENTS b2) · Must (lines), Should (animation)

`meta.md` §3.5 owns the choreography (music cut, shake, Bass lands on the FINAL frame, shoots it, dashes across the
unbeaten portraits stamping POSTPONED). Pages play over it in this order.

| Who | EN | JP |
|---|---|---|
| K | An unregistered entrant is attacking the bracket! | みとうろくの せんしゅが トーナメントひょうを こうげきして います! |
| C | ...Registered, actually. Entrant β. Sponsor: Mr. Y. | ・・・とうろくずみ だ。 エントリーナンバーβ。 スポンサーは Mr.Y。 |
| K | Of course it is. | やっぱりね。 |
| B (on the cracked frame) | Four wins? Cute. Every other match is POSTPONED. You fight me next, original. | 4しょう? かわいい もんだ。 ほかの しあいは ぜんぶ えんき。 つぎの あいては オレだ、 オリジナル。 |
| C | The Committee has... approved this. By fax. From Mr. Y's office. | いいんかいは・・・ これを しょうにん した。 ファックスで。 Mr.Y の じむしょから。 |

#### S15 Venue NPC lines (index)

The venue docs own these lines and their triggers; this doc adopts them for the text pass with these JP rules:

| Venue | NPCs (owner) | JP register and the real quote it rests on |
|---|---|---|
| Knight | King, Sage, Innkeeper, Princess Roll, the Knightlord, the battle log (`venues_a.md` §2.6-2.8) | Dragon Quest's archaic register (わし / なんじ / じゃ). The King's death line uses **DQ1's own words**: 「おお ロックよ! しんでしまうとは なにごとだ!」 (EN keeps Dragon Warrior's "DEATH SHOULD NOT HAVE TAKEN THEE"). Princess Roll's NO loop uses DQ1's JP refusal line 「そんな ひどい・・・」 where EN has "BUT THOU MUST!". The battle log uses DQ's 「ナイトマンが あらわれた!」 / 「かいしんの いちげき!」 (EN "AN EXCELLENT MOVE!", Dragon Warrior's wording) |
| Tomahawk | the Sheriff, the conductor, the posters, the saloon sign (`venues_a.md` §3) | Plain western 「〜だぜ」 for outlaws, polite for the Sheriff. The sign is Oscar Wilde's (he reported it from a Leadville saloon): 「ピアニストを うたないで ください。 かれは けんめいに ひいています。」 |
| Wind | the carrier deck crew, the LOOP / POW icons (`venues_a.md` §1) | Military radio: 「りょうかい!」, 「メーデー!」 |
| Plant | the treasure pops, Tango the cat (`venues_a.md` §4) | Tango only says 「ニャー」. Kalinka's "Is that... Tango? From the Game Boy?" is accurate: Tango first appeared in Rockman World 5 (Game Boy, 1994) |
| Blizzard | the seals' union, Shirokuma (`venues_b.md` §1) | Seals: 「キュー」. The union sign: 「アザラシ ろうどうくみあい」 |
| Flame | the vizier (silent), the mouse (`venues_b.md` §2) | The mouse: 「チュー」 |
| Centaur | the tablet, the zone plaques (`venues_b.md` §3) | Plaques are numerals only (ZONE 12 = 「ゾーン12」) |
| Yamato | the sekisho guard, the runner ninja, the kabuki audience (`venues_b.md` §4) | Guard: 「とおりたくば てがた 3まいを みせよ。」 Audience: 「やまとや!」 (a real kabuki *ōmukō* shout pattern: the actor's house name + や) |

#### S16 Game over, RETIRE and unplug · Must

**Game over** (Kalinka, rotating; the window under vanilla's `GAME OVER`, `meta.md` §3.7):

| # | EN | JP |
|---|---|---|
| 1 | He'll be back. They always come back. | きっと もどってくる。 みんな もどって くるんだよ。 |
| 2 | The crowd is chanting your name. Well, the ones who stayed. | かんきゃくが なまえを よんでるよ。 のこってる ひとたちが。 |
| 3 | Every champion has lost a match. Most of them to you, later. | チャンピオンだって まけたこと あるよ。 あとで あなたに まけるの。 |
| 4 | Papa says a game over is just a very long pit stop. | パパが いってた。 ゲームオーバーは ながーい ピットストップ だって。 |
| 5 | Retry? Retry. Retry! | リトライ? リトライ。 リトライ! |
| 6 | Insert coin! ...Kidding. Press START. | コインを いれてね! ・・・うそ。 スタートで いいよ。 |

In H1-H5 the line is Mr. Y's: "Game over! Mr. Y thanks you for your participation!" / 「ゲームオーバー! Mr.Y より
ごさんか ありがとう ございました!」. In W1-W3, Wily's: "HA! Come back when you're 16-bit!" / 「ワハハ!
16ビットに なってから でなおして こい!」.

**RETIRE** (pause menu): no line; the bracket simply returns. On the first RETIRE of a file, K: "Tactical retreat!
The judges allow it." / 「さくせんてき てったい! しんさいんも みとめてるよ。」

**Unplug** (a file loads with IN_MATCH set, `meta.md` §1.7), rotating:

| # | EN | JP |
|---|---|---|
| 1 | K: We lost the feed during %NAME%'s match! ...Did someone trip over the stadium cable? | K: %NAME%の しあいちゅうに ちゅうけいが きれちゃった! ・・・だれか ケーブルに つまずいた? |
| 2 | C: A power cut in the middle of a match. The judges have recorded it as... weather. | C: しあいちゅうの ていでん。 しんさいんは 「てんこう」 と きろく した。 |
| 3 | K: The stadium went dark. Papa thinks it was a squirrel. | K: スタジアムが まっくら。 パパは リスの しわざ だって。 |

### Act II: the Semifinal

#### S17 Semifinal night · Must

POP sequence on the Semifinal's first screen (`fortress.md` §2 owns the stage).

| Who | EN | JP |
|---|---|---|
| K | Semifinal night! Rockman versus... entrant β! | じゅんけっしょうの よる! ロックマン たい・・・ エントリーナンバーβ! |
| C | The stands are full. Of Sniper Joes. In Bass scarves. | かんきゃくせきは まんいん。 フォルテの マフラーを まいた スナイパージョーで。 |
| K | Mr. Y bought every ticket! | Mr.Y が チケットを ぜんぶ かったんだって! |
| C | And gave them to his robots. Kick-off! | そして ロボットに くばった。 キックオフ! |

#### S18 Break Man holds the crowd · Should

At the Semifinal's set piece where the stands empty onto the pitch (`fortress.md` places it), Break Man's whistle,
then he drops in between Rockman and the horde, shield up, and stays behind.

| Who | EN | JP |
|---|---|---|
| BM | Go. I've got the crowd. | いけ。 きゃくせきは おれが おさえる。 |
| R | Break Man! | ブレイクマン! |
| K | Is entrant 10 allowed to do that? | 10ばんって あんなこと して いいの? |
| C | There is no rule against it. I checked. There is Rule 8. | きんし する ルールは ない。 しらべた。 ルール8 なら あるが。 |

#### S19 Bass β, duel 1 · Must

| Who | When | EN | JP |
|---|---|---|---|
| B | before the bar fills | Your data's in me, original. Every slide. Every charge. I know what you'll do. | おまえの データは オレの なかに ある。 スライディングも チャージも ぜんぶ だ。 うごきは おみとおし だ。 |
| R | | Then you know I won't quit. | なら ぼくが あきらめない ことも わかるよね。 |
| B | | ...Shut up and fight! | ・・・うるさい! かかってこい! |
| C (POP) | SC6 fires ("He's adapting!", `systems.md` §4.6) | He's adapting! Change weapons, Rockman! | てきおう している! ぶきを かえろ ロックマン! |
| B | defeated | This doesn't count! The beta build has... bugs! (teleports out) | こんなの ノーカン だ! ベータばんには バグが・・・! |
| K | | He blamed the bugs! | バグの せいに した! |
| C | | In fairness, that is what betas are for. | まあ ベータばんとは そういう ものだ。 |
| K | no damage taken (RATEFLAGS b2) | Not a scratch! Bass is going to be SO mad. | むきず! フォルテ ぜったい おこってるよ! |

#### S20 Rule 9: Break Man joins (EVENTS b3 → b5) · Should

On the bracket, right after the Semifinal: the POSTPONED stamps peel off (b3), then the join (b5). If the tag partner
is cut (`systems.md` Risk 11), pages 3-6 are dropped and b5 is never set.

| # | Who | EN | JP |
|---|---|---|---|
| 1 | K | The Committee has ruled! Mr. Y's "fans" invaded a match, so Rule 9 applies! | いいんかいの はんけつ です! Mr.Y の 「ファン」 が しあいに らんにゅう したので ルール9 てきよう! |
| 2 | C | Rockman may name a tag partner. And the other four matches are back on. | ロックマンは タッグパートナーを ひとり よべる。 のこり 4しあいも さいかい だ。 |
| 3 | (whistle; Break Man walks in from the bracket's edge) | | |
| 4 | BM | ...He'll take me. | ・・・おれが いく。 |
| 5 | BM | Pause. Press SELECT. Once per life. Don't waste me. | ポーズして セレクト。 いのち ひとつに 1かい。 むだに するな。 |
| 6 | C | That is the most he has ever said. | かれが こんなに しゃべったのは はじめてだ。 |

#### S21 Mr. Y's booth; Break Man walks · Should

`systems.md` §9.4 owns the offer and its cost; this is the script. The booth is a PIT STOP row (`meta.md` §3.8).

| Step | Who | EN | JP |
|---|---|---|---|
| offer | Y | Psst. Champ. Feeling sluggish in round two? Try Y-TURBO! One PART in, one chip out. *Results guaranteed.* ▶NO YES | もしもし チャンピオン。 2かいせんで おつかれ ですか? Y-ターボ いかがで ございましょう! パーツ ひとつで チップ ひとつ。 *こうか ほしょう いたします*。 |
| NO | Y | Think it over! Mr. Y will be right here. Mr. Y is always right here. | ごけんとうを! わたくし Mr.Y は いつでも ここに おります。 |
| YES (1st) | Y | Splendid! Just one teeny formality... Break Man is watching, you know. Still yes? ▶NO YES | すばらしい! ひとつだけ かくにんを・・・ ブレイクマンが みて おりますよ? それでも はい? |
| NO (2nd) | Y | Your loss! Probably literally! | ざんねん! きっと まけますぞ! (the slip: ぞ is Wily's ending) |
| YES (2nd) | Y | Pleasure doing business! Mr. Y guarantees results! (PART taken, Y-TURBO given) | まいど ありがとう ございます! Mr.Y は けっかを ほしょう いたします! |
| later visits (rotate) | Y | Y-TURBO! Now with 20% more Y! / Everyone's doing it! Well. Someone. Once. / My lawyers say it is legal in at least one country. / Your rival uses it! ...He IS it, actually. | Y-ターボ! いまなら Y が 20% ぞうりょう! / みなさま つかって おりますよ! ・・・ひとりは。 いちどは。 / べんごしに よれば すくなくとも ひとつの くにでは ごうほう で ございます。 / ライバルも つかって おります! ・・・というか かれ そのもの で ございます。 |

**BREAK MAN WALKS** (EVENTS2 b5, next bracket visit after the purchase, `meta.md` §6.3): Break Man stands at the
bracket's edge.

| Who | EN | JP |
|---|---|---|
| BM | You took Y's money. Fight your own matches. | Mr.Y の かねを うけとったな。 じぶんの しあいは じぶんで たたかえ。 |
| (the whistle fades; he walks off the edge of the screen) | | |
| K | ...Papa? Where's he going? | ・・・パパ? どこ いくの? |
| C | Home, I think. | かえるの だろう。 |

From then on the pause menu shows his portrait greyed, labelled **N0**: the pause font has no O, so it is spelled
with a zero, exactly like vanilla's `N0R` and `P0W` (`rm6/text.md` §5.3). A quirk turned into a small, sad joke.

The commentators notice the chip once (`systems.md` §9.4 item 4): the first stage started with Y-TURBO equipped, C:
"Is that... a sponsor patch?" K: "Papa, don't look." / C「あれは・・・ スポンサーの ワッペンか?」 K「パパ、 みちゃ
だめ。」

### Act III: round two

#### S22 Exhibition badges light (EVENTS2 b0-3) · Should

Cossack announces each guest when its badge lights (`meta.md` §3.1 pairs). The years are the original games' (Appendix A).

| Badge | Who | EN | JP |
|---|---|---|---|
| E1 | C | Exhibition match unlocked! From 1984, the robot who fills every gap... BLOCK MAN! | エキシビション かいほう! 1984ねんから すきまを うめる おとこ・・・ ブロックマン! |
| E1 | K / C | K: "Block Man? Isn't that name taken?" C: "Not until 2018." | K「ブロックマン? その なまえ つかわれて なかった?」 C「2018ねん までは まだだ。」 |
| E2 | C | From 1976 and 1986, the wall's best friend... PADDLE MAN! | 1976ねんと 1986ねんから かべの しんゆう・・・ パドルマン! |
| E2 | K | He's been returning the same ball for decades! | もう なんじゅうねんも おなじ ボールを うちかえしてるんだって! |
| E3 | C | From 1978, coming down one step at a time... INVADER MAN! | 1978ねんから 1だんずつ おりてくる・・・ インベーダーマン! |
| E3 | K / C | K: "Papa, what's the Nagoya attack?" C: "Something your grandfather was very proud of." | K「パパ、 なごやうち って なに?」 C「おじいちゃんの じまんの わざ だよ。」 |
| E4 | C | From 1980, the hungriest entrant in history... MAZE MAN! | 1980ねんから しじょう いちばん はらぺこの せんしゅ・・・ メイズマン! |
| E4 | K | Four Met-ghosts and a whole lot of pellets! | メットの おばけが 4ひきと えさが いっぱい! |

#### S23 Exhibition matches · Should

Each guest gets a card (§5.3), a bar-fill line, a defeat line and a **plaque** for the Museum's PLAQUE GALLERY
(`meta.md` §9.5), shown on the results screen of the first clear.

| Guest | Bar fill (EN / JP) | Defeat (EN / JP) |
|---|---|---|
| Block Man | (no words: one line clears.) K: "I think that was hello." / K「いまの あいさつ かな?」 | (the last block drops into place) C: "A perfect fit. He seems at peace." / C「ぴったり おさまった。 まんぞく そうだ。」 |
| Paddle Man | Same ball. Every day. Same ball. / おなじ ボール。 まいにち。 おなじ ボール。 | ...A different ball. Finally. / ・・・ちがう ボール だ。 やっと。 |
| Invader Man | WE. ARE. COMING. DOWN. / ワレワレハ。 オリテ。 イク。 | WE. HAVE. COME. DOWN. / ワレワレハ。 オリテ。 キタ。 |
| Maze Man | Excuse me. Is that pellet yours? / すみません。 その えさ あなたのですか? | Waka... waka... / パク・・・ パク・・・ |

Invader Man's JP is katakana robot-speech, the register 4MI gives its fake Roll (`r4mi/text.md` §0).

**Exhibition plaques** (EN / JP):

| Guest | Plaque |
|---|---|
| Block Man | After a falling-block puzzle created in Moscow in 1984 by Alexey Pajitnov. In 1989 it came packed with the Game Boy in America. / 1984ねん モスクワで アレクセイ・パジトノフが うみだした おちものパズルに ささぐ。 1989ねん アメリカでは ゲームボーイに どうこん された。 |
| Paddle Man | After Atari's *Breakout* (1976) and Taito's *Arkanoid* (1986), where the paddle was a spaceship called the Vaus. / アタリの ブロックくずし (1976) と タイトーの アルカノイド (1986) に ささぐ。 アルカノイドの パドルは バウスという うちゅうせん だった。 |
| Invader Man | After Taito's *Space Invaders* (1978), by Tomohiro Nishikado. The invaders sped up as you shot them, because the hardware had fewer of them to draw. / タイトーの スペースインベーダー (1978 にしかど とものり) に ささぐ。 インベーダーは へるほど はやく なった。 えがく かずが へって きかいが らくに なったから。 |
| Maze Man | After Namco's *Pac-Man* (1980), by Toru Iwatani. Each of the four ghosts chases in its own way. The 256th maze breaks in half. / ナムコの パックマン (1980 いわたに とおる) に ささぐ。 4ひきの おばけは それぞれ ちがう おいかたを する。 256めんめは はんぶん こわれて いる。 |

#### S24 The countdown · Must

Kalinka on the centre node once the Semifinal is won (`meta.md` §3.4):

| Wins left | EN | JP |
|---|---|---|
| 4 | Four venues to go! Then the final! | あと 4かいじょう! そしたら けっしょう! |
| 3 | Three to go! The trophy's getting polished. | あと 3つ! トロフィーを みがいてる ところ。 |
| 2 | Two more! Papa's practising his speech. | あと 2つ! パパが スピーチの れんしゅう ちゅう。 |
| 1 | One more match! I can see the trophy from here! | あと 1しあい! ここから トロフィーが みえるよ! |
| 0 | All eight! Come to the centre for the ceremony! | 8しょう! ひょうしょうしきは まんなかで! |

### Act IV: the Hall of Fame

#### S25 Trophy ceremony and theft (EVENTS b4) · Must

START on the lit trophy (`meta.md` §3.4). The stadium at night, the podium, the GP Cup. The claw is the Cossack
Catcher's (it foreshadows H4); the saucer is Wily's with a "Y" painted over the "W".

| Who | EN | JP |
|---|---|---|
| C | Ladies, gentlemen and robots! After eight matches, the winner of the Grand Prix rounds... ROCKMAN! | みなさん! 8しあいを かちぬいた グランプリ よせんの しょうしゃは・・・ ロックマン! |
| K | The GP Cup! Papa, it's so shiny! | GPカップだ! パパ、 ぴかぴか! |
| C | Until the final, the cup goes on display. Rockman, hold it up for the cameras... | けっしょうまで カップは てんじ される。 ロックマン、 カメラに むけて かかげて くれ・・・ |
| (a crane claw drops from a saucer and takes the cup) | | |
| C | That is MY claw! | わたしの アームだ! |
| Y (from the saucer) | Correction, Doctor! It is MY claw. I bought it in the museum gift shop! | ていせい いたします はかせ! わたくしの アーム で ございます。 はくぶつかんの おみやげやで かいました! |
| K | That saucer has a Y painted over a W. | あの ユーフォー、 W の うえに Y って ぬってある。 |
| Y | The final will be held at MY venue: the HALL OF FAME! Come and get it, Rockman! Wahaha— I mean, ho ho ho! | けっしょうは わたくしの かいじょう ホール・オブ・フェイムにて! とりに いらっしゃい ロックマン! ワーッハッハ・・・ いえ、 ホッホッホ! |
| L / R | L: "...Rock. It's Wily." R: "It's definitely Wily." | L「・・・ロック。 ワイリーじゃ。」 R「ぜったい ワイリー です。」 |

#### S26 The Hall of Fame map · Must

First visit to the fortress map (`fortress.md` §4 owns it): Mr. Y on the museum's video wall.

| Who | EN | JP |
|---|---|---|
| Y | Welcome to the HALL OF FAME, the museum of Rockman's greatest battles! Every exhibit has been... *upgraded*. By me. A stranger. | ホール・オブ・フェイムへ ようこそ! ロックマンの かずかずの たたかいの はくぶつかん で ございます! てんじひんは すべて・・・ *アップグレード* ずみ。 とおりすがりの わたくしが。 |
| K | He keeps saying "stranger". | 「とおりすがり」 って いいはってる。 |
| C | Five wings, five games. The cup is at the end. | ウイングは 5つ。 ゲームも 5つ。 カップは そのさき だ。 |

The judges' desk changes from here on: the cardboard Mr. Y is gone from the sponsor's chair (he is busy), replaced by a
sign, `BACK SOON`. After S33 the sign reads `RESERVED` (`meta.md` §4.0).

#### S27 Museum plaques · Must (H1, H3, H5), Should (H2, H4)

A plaque opens each wing (SCN, plaque page: a brass frame, up to 9 lines × 28). The text is **true** (Appendix A
lists every claim). One joke per plaque, always last. The two thanks plaques sit in the hidden rooms that PLAN put
them in (H2: Air Man's fans; H4: the Cossack snow citadel); `fortress.md` places them.

**H1: ROCKMAN (1987)**

> EN: ROCKMAN. Famicom, 17 December 1987; MEGA MAN in America the same month. / Dr. Wily reprogrammed six of Dr.
> Light's industrial robots: Cut, Guts, Ice, Bomb, Fire and Elec Man. Light's lab assistant, Rock, volunteered to
> stop them. / It began the rule every Rockman since has followed: beat a master, take his weapon. / It is the only
> numbered Rockman with a points score. / The Yellow Devil flew across his room in pieces and rebuilt himself on the
> other side. The Elec Beam was the cure. / Some tricks are a SELECT few.
>
> JP: ロックマン。 1987ねん 12がつ 17にち ファミコンで はつばい。 アメリカでは おなじ つきに MEGA MAN として。 /
> ワイリーは ライトはかせの 6たいの さぎょうロボットを のっとった。 カットマン、 ガッツマン、 アイスマン、
> ボンバーマン、 ファイヤーマン、 エレキマン。 じょしゅの ロックは じぶんから たたかうと もうしでた。 / ボスを
> たおして ぶきを てに いれる。 いまに つづく ルールは ここから はじまった。 / スコアが ある ゆいいつの ナンバリング
> さくひん でもある。 / イエローデビルは バラバラに なって へやを とびこえ むこうで がったい した。 きりふだは
> サンダービーム。 / とっておきの ワザは セレクトボタンに かくれて いる。

The last line is the SC7 hint (`systems.md` §4.6): in Rockman, SELECT paused the game, and pausing let a beam hit the
Yellow Devil's eye again (Appendix A, A-1.6). JP says "Elec Beam" by its JP name, サンダービーム; Bomb Man is
ボンバーマン in Japan.

**H1 exhibit label: MAGNET BEAM** (the wing's reward, `systems.md` §3.10)

> EN: MAGNET BEAM (1987). Hidden in Elec Man's stage, behind blocks only the Super Arm could lift. On loan to
> entrants. Three beams at a time: the museum only had three in stock.
>
> JP: マグネットビーム (1987)。 エレキマンステージの スーパーアームで しか どかせない ブロックの おくに あった。
> せんしゅに かしだし ちゅう。 どうじに 3ぼんまで。 はくぶつかんの ざいこが 3ぼん だけ なので。

**H2: ROCKMAN 2: DR. WILY NO NAZO (1988)**

> EN: ROCKMAN 2: DR. WILY NO NAZO, "The Mystery of Dr. Wily". Famicom, 24 December 1988. / Its development began
> Capcom's tradition of robot-design contests for fans. / It set the standard of eight Robot Masters: Metal, Air,
> Bubble, Quick, Crash, Flash, Heat and Wood Man. / It also brought the E-tank and passwords. / In Japan it had one
> difficulty. The American release added an easier mode, NORMAL, and called the original DIFFICULT. / The Mecha
> Dragon chased Rock across the sky of the first Wily stage. You can probably hum it.
>
> JP: ロックマン2 Dr.ワイリーの なぞ。 1988ねん 12がつ 24にち はつばい。 / ファンから ボスの デザインを ぼしゅう
> する でんとうは この さくひんから はじまった。 / ボスは 8たいが きほんに なった。 メタルマン、 エアーマン、
> バブルマン、 クイックマン、 クラッシュマン、 フラッシュマン、 ヒートマン、 ウッドマン。 / Eかんと パスワードも
> ここから。 / にほんばんの なんいどは ひとつ。 アメリカばんには やさしい NORMAL が くわわり もとの むずかしさは
> DIFFICULT と よばれた。 / ワイリーステージ1では メカドラゴンが そらを おいかけて きた。 あの きょく くちずさめる
> でしょう?

**H2 thanks plaque** (the hidden room with Air Man's fans):

> EN: WITH THANKS TO ROCKMAN CX, by HIMAJIN JICHIKU, which played this game from the other side, made Dr. Light the
> villain, and taught us that a death can be a line of dialogue. / Also: Air Man is still hard to see.
>
> JP: ロックマンCX (HIMAJIN JICHIKU さく) に かんしゃを こめて。 この ゲームを うらがわから あそび、 ライトはかせを
> わるものに し、 しぬ ことも セリフに なると おしえて くれた。 / あと エアーマンは あいかわらず みえにくい。

(CX's Air Man is an invisible stipple, `cx/SUMMARY.md` §2 item 3. The author's name is kept in Latin letters in JP
until its kana/kanji spelling is confirmed: Open question 6.)

**H3: ROCKMAN 3: DR. WILY NO SAIGO!? (1990)**

> EN: ROCKMAN 3: DR. WILY NO SAIGO!?, "The End of Dr. Wily!?". Famicom, 28 September 1990. Note the question mark.
> / It introduced the slide, Rush, and a masked rival with a whistle who called himself BREAK MAN. / Dr. Light and Dr.
> Wily built Gamma together, to keep the peace. Dr. Wily had other plans. / Gamma's last form fell to a spinning
> kick: the Top Spin. This one respects only a fist. / Doc Robot fought with the eight bosses of Rockman 2. /
> Holding RIGHT on the second controller let Rock jump out of pits: a debugging leftover the European release removed.
>
> JP: ロックマン3 Dr.ワイリーの さいご!? 1990ねん 9がつ 28にち はつばい。 「さいご」 の あとの 「!?」 に ちゅうもく。 /
> スライディング、 ラッシュ、 そして くちぶえを ふく なぞの ライバル 「ブレイクマン」 が はじめて とうじょう。 /
> ライトはかせと ワイリーは へいわの ために ガンマを いっしょに つくった。 ワイリーには べつの もくろみが あった。 /
> ガンマの さいごの すがたを たおしたのは トップスピン。 この ガンマは こぶし しか みとめない。 / ドクロボットは
> ロックマン2の 8ボスの ちからで たたかった。 / 2コンの みぎを おしていると あなから とびだせた。 デバッグの
> なごりで ヨーロッパばんでは けされた。

**H3 exhibit label: SUPER ADAPTOR** (the wing's reward, `systems.md` SYS-FRM-5)

> EN: SUPER ADAPTOR. Dr. Light's next design: Rock and Rush as one, with a rocket fist. Not due until 1995. On early
> loan. Please return it by then.
>
> JP: スーパーアダプター。 ライトはかせの つぎの せっけい。 ロックと ラッシュが ひとつに なり ロケットパンチを
> うつ。 かんせいは 1995ねんの よてい。 とくべつに さきがし ちゅう。 それまでに かえして ください。

**H4: ROCKMAN 4: ARATANARU YABŌ!! (1991)**

> EN: ROCKMAN 4: ARATANARU YABO!!, "A New Ambition!!". Famicom, 6 December 1991. / It introduced the charge shot,
> Eddie, Dr. Cossack and Kalinka. / Dr. Cossack built eight robots and a citadel in the snow because Dr. Wily was
> holding Kalinka hostage. Break Man brought her home. / New tools: the Wire and the Balloon. / The Cossack Catcher
> was a crane game that flew. Dr. Cossack would like everyone to know that he has apologised.
>
> JP: ロックマン4 あらたなる やぼう!! 1991ねん 12がつ 6にち はつばい。 / チャージショット、 エディ、 Dr.コサック、
> カリンカが はじめて とうじょう。 / コサックはかせが 8たいの ロボットと ゆきの ようさいを つくったのは ワイリーに
> カリンカを ひとじちに とられて いたから。 カリンカを つれかえったのは ブレイクマン だった。 / あたらしい どうぐ:
> ワイヤーと バルーン。 / コサックキャッチャーは そらとぶ クレーンゲーム。 コサックはかせは もう あやまった
> そうです。

(EN drops the macron, `YABO`, because the fonts have no Ō; the doc's heading keeps it.)

**H4 thanks plaque** (the hidden room in the snow citadel):

> EN: WITH THANKS TO ROCKMAN 4 MINUS INFINITY, by PURESABE (2008-2016), which rebuilt this game from the ground up,
> hid a friend inside a wall, and taught us to read a weakness in the flashing.
>
> JP: ロックマン4 ミナスインフィニティ (PURESABE さく 2008-2016) に かんしゃを こめて。 この ゲームを いちから
> つくりなおし、 かべの なかに なかまを かくし、 てんめつの ながさで じゃくてんを よむ ことを おしえて くれた。

**H5: ROCKMAN 5: BLUES NO WANA!? (1992)**

> EN: ROCKMAN 5: BLUES NO WANA!?, "Blues' Trap!?". Famicom, 1992. / A robot that looked like Blues attacked the
> city and kidnapped Dr. Light. It was Dark Man, built by Dr. Wily. When the real Blues appeared, the disguise came
> off. / While Light was missing, Dr. Cossack built Rock a bird: Beat. You found him by collecting eight plates that
> spelled R-O-C-K-M-A-N-5 in Japan and M-E-G-A-M-A-N-V in America. / Gravity Man turned the whole screen upside
> down.
>
> JP: ロックマン5 ブルースの わな!? 1992ねん はつばい。 / ブルースに そっくりの ロボットが まちを おそい ライト
> はかせを さらった。 しょうたいは ワイリーが つくった ダークマン。 ほんものの ブルースが あらわれ へんそうは
> はがれた。 / ライトはかせの いない あいだに コサックはかせが ロックに とりの ロボット ビートを つくった。
> 8まいの プレートは にほんでは R-O-C-K-M-A-N-5、 アメリカでは M-E-G-A-M-A-N-V。 / グラビティーマンは がめんを
> まるごと さかさまに した。

#### S28 Exhibit lines; Mr. X's business card · Must / Should

Each wing boss gets a bar-fill exchange and a defeat line (POP). Mr. Y's own heckles between lives are §6.5.

| Exhibit | Bar fill (EN / JP) | Defeat (EN / JP) |
|---|---|---|
| Yellow Devil MK-VI | K: "He comes apart and flies across the room!" C: "Watch the eye. Only the eye." / K「バラバラに なって とんでくるよ!」 C「めを ねらえ。 めだけを。」 | C: "It will not be reassembling this time." Y: "That was a museum piece!" / C「こんどは がったい できまい。」 Y「てんじひん なのに!」 |
| Mecha Dragon MK-VI | K: "I can hear the music in my head!" C: "Don't look down, lad. There is no down." / K「あたまの なかで あの きょくが ながれてる!」 C「したを みるな。 したは ない。」 | K: "It's falling! Just like 1988!" / K「おちていく! 1988ねんと おなじ!」 |
| Gamma MK-VI | L (radio): "We built Gamma for peace, Wily and I. Don't hold back, Rock." / L「ガンマは へいわの ために ワイリーと わしで つくったのじゃ。 えんりょ するな ロック。」 Phase 2, C: "The head! Only a fist will do!" / C「あたまだ! こぶし しか きかない!」 | K: "Gamma's down! Again!" / K「ガンマ ダウン! また!」 |
| Cossack Catcher MK-VI | C: "That is... my machine. On loan. I signed the form." K: "Papa! Commentate!" C: "Rockman avoids the claw. Good. GOOD. I am so sorry." / C「あれは・・・ わたしの マシンだ。 かしだし ちゅう。 しょるいに サインした。」 K「パパ! じっきょう して!」 C「ロックマン アームを かわした。 よし。 よし! ほんとうに すまない。」 | C: "I feel much better now. Thank you, Rockman." / C「すっきり した。 ありがとう ロックマン。」 |
| Dark Man MK-VI | see S30 | K: "Fake! Fake fake fake!" / K「にせもの! にせものー!」 |

**Mr. X's business card** (one pickup in H1-H5, RATEFLAGS b1; `meta.md` §6.1 T14; `fortress.md` places it):

| Who | EN | JP |
|---|---|---|
| (card) | A business card: "MR. X. INTERNATIONAL ROBOT FINANCIER." The address is real. So is the phone number. | めいし だ。 「Mr.X こくさい ロボット とうしか」。 じゅうしょも でんわばんごうも ほんもの らしい。 |
| K | Papa... is there a REAL Mr. X? | パパ・・・ ほんものの Mr.X って いるの? |
| C | ...Let us not think about it. | ・・・かんがえないで おこう。 |

#### S29 The Super Adaptor (EVENTS2 b4) · Must

On the Hall of Fame map after H3. Roll's portrait with Rush.

| Who | EN | JP |
|---|---|---|
| Ro | Rock! The museum's "future exhibit" fits Rush perfectly! SUPER ADAPTOR fitted! | ロック! はくぶつかんの 「みらいの てんじひん」、 ラッシュに ぴったり! スーパーアダプター そうちゃく! |
| Rush | WOOF! | ワン! |
| Ro | A rocket fist that comes back, a little jet hop, and no fuel gauge. Not as strong as POWER, not as quick as JET, but it does both. | もどってくる ロケットパンチと ちいさな ジェットジャンプ。 ねんりょうは いらないわ。 パワーほど つよくないし ジェットほど はやくないけど りょうほう できるの。 |
| Ro | The Doctor says to bring it back by 1995. | はかせが 1995ねんまでに かえしなさい って。 |

#### S30 H5: the fake Break Man · Must

H5's boss room (`fortress.md`). An off-key whistle. "Break Man" stands on a throne. Two variants by the partner state.

| Variant | Who | EN | JP |
|---|---|---|---|
| both | DM (disguised) | It's me. Break Man. Your... brother? Hand over the Super Adaptor. | おれだ。 ブレイクマン だ。 おまえの・・・ あに? スーパーアダプターを よこせ。 |
| both | K / C | K: "His whistle is flat." C: "And his scarf is on the wrong side." | K「くちぶえ ちょっと おんち だよ。」 C「マフラーも はんたいがわ だな。」 |
| partner (FORMS.TAG) | (the real whistle, in tune, from the doorway) BM | ...Break Man. | ・・・ブレイクマン だ。 |
| partner | (the disguise falls off: Dark Man's palette) K / C | K: "Two Break Men!" C: "One and a half." | K「ブレイクマンが ふたり!」 C「ひとりと はんぶん だな。」 |
| partner | BM | He's yours, Rock. (leaves) | こいつは おまえの ぶんだ、 ロック。 |
| walked (DOPED) | (the real whistle, offscreen; the disguise falls; nobody is seen) K / C | K: "...That whistle." C: "He still came." | K「・・・あの くちぶえ。」 C「それでも きて くれたのか。」 |

This is Rockman 5's own reveal (Appendix A, A-5.2): the real Blues shows up and the fake is unmasked.

#### S31 Mr. Y's heckles between lives

The CX Light 6 pattern: one line per respawn in H1-W3. The table is §6.5.

#### S32 The cup on the pedestal · Must

After H5, the Hall's central gallery (`fortress.md`): the GP Cup sits on a pedestal with cables running out of it.

| Who | EN | JP |
|---|---|---|
| K | The cup! It's plugged into something! | カップだ! なにかに つながってる! |
| C | Into everything, by the look of it. | みたところ なにもかもに だな。 |
| Y (descends in a capsule) | Congratulations, Rockman! You have reached the Hall of Fame's final exhibit... ME! | おめでとう ございます ロックマン! ホール・オブ・フェイム さいごの てんじひんは・・・ わたくし で ございます! |

#### S33 The unmasking; Project SUPER (EVENTS b6) · Must

SCN, the central gallery. Everyone who has ever said "It's Wily" says it once more, together. Light is on the radio;
Roll is on the radio from the pit.

| # | Who | EN | JP |
|---|---|---|---|
| 1 | Y | You have done well to come this far. It is time you learned the truth. Mr. Y is... Mr. Y is actually... | よくぞ ここまで たどりついた。 しんじつを おしえて しんぜよう。 Mr.Y の しょうたいは・・・ じつは・・・ |
| 2 | (he tears off the badge, the sunglasses and the fake moustache; the real moustache stays) | | |
| 3 | W | ...SURPRISE! It's me, Dr. Wi— | ・・・ジャーン! わしじゃ! Dr.ワイ・・・ |
| 4 | R, L, Ro, C, K (one page, all five faces) | WE KNOW. | しってる。 |
| 5 | W | ...HOW?! | ・・・なぜじゃ!? |
| 6 | K | You signed the entry form "Dr. W", then crossed it out. In crayon. | とうろくようしに 「Dr.W」 って かいて けしてあったもん。 クレヨンで。 |
| 7 | C | Your fake moustache was on the outside of your real moustache. | つけひげが ほんものの ひげの そとがわに ついていた。 |
| 8 | R | You laugh like Wily. | わらいかたが ワイリー でした。 |
| 9 | L (radio) | I'd know you anywhere, Albert. | アルバート、 おまえの ことは どこに いても わかるわい。 |
| 10 | W | BAH! It doesn't matter! Do you know what that cup is? | ええい! どうでも よいわ! あの カップが なにか わかるか? |
| 11 | W | Every match of this Grand Prix was recorded by MY judges' cameras. Every slide, every charge, every weakness. It's all in the cup! | この グランプリの しあいは すべて わしの しんさカメラが きろく した! スライディングも チャージも じゃくてんも ぜんぶ カップの なかじゃ! |
| 12 | W | With it I built Bass β. And with it I will finish PROJECT SUPER! | それで フォルテβを つくった。 そして プロジェクト・スーパーを かんせい させる! |
| 13 | W | Look at you! Three colours a sprite. Eight sprites a line. Five sound channels. The world has moved on, Rockman! The future has MORE! | みろ ロックマン! スプライト ひとつに 3しょく。 よこに 8まい。 おとは 5チャンネル。 せかいは もう さきへ すすんで おる! みらいには もっと あるのじゃ! |
| 14 | W | I will upgrade every robot on Earth to 16 bits! More colours! More channels! MODE 7! And every one of them will run on WILY OS! | ちきゅうの ロボットを すべて 16ビットに アップグレード してやる! いろも おとも もっと! モード7も! そして ぜんぶ ワイリーOSで うごくのじゃ! |
| 15 | L (radio) | You can't force an upgrade on the world, Albert. People move on when they're ready. | アップグレードを せかいに おしつける ことは できんぞ アルバート。 ひとは じゅんびが できた ときに すすむ ものじゃ。 |
| 16 | W | Watch me! SUPER WILY CASTLE... RISE! | みておれ! スーパー ワイリー キャッスル・・・ しゅつげん!! |
| 17 | (the screen shakes; through the museum's glass roof a castle rises, all in four shades of green) K / C | K: "Papa... why is it green?" C: "It is starting from the bottom." | K「パパ・・・ なんで みどりいろ なの?」 C「いちばん したから はじめる らしい。」 |

Page 13 is accurate NES trivia (a sprite has 3 colours plus transparency; 8 sprites per scanline; 2 pulse, triangle,
noise and DPCM channels: Appendix A, A-6.4). Wily is half right, which is the point of §1.4.

### Act V: Project SUPER

#### S34 Super Wily Castle map · Must

| Who | EN | JP |
|---|---|---|
| W | Welcome to SUPER WILY CASTLE! The higher you climb, the better it looks. Literally! | スーパー ワイリー キャッスルへ ようこそ! のぼれば のぼるほど きれいに なるぞ。 もじどおり! |
| K | He's right. That's the worst part. | ほんとう なのが くやしい。 |

#### S35 W1: the Upgrade Lab · Should

POPs at the palette tiers (`fortress.md` §5; `art_audio.md` §2.7 ExGrafix; the MMC5 pulses join the music at the
third tier).

| Tier | Who | EN | JP |
|---|---|---|---|
| 1 (four greens) | K / C | K: "Everything's green! It's like a Game Boy!" C: "Four shades. Very economical." | K「ぜんぶ みどり! ゲームボーイ みたい!」 C「4しょく だけ。 けいざいてき だな。」 |
| 2 (NES colours) | K / C | K: "Colours! Our colours!" C: "Home sweet home." | K「いろが ついた! いつもの いろ!」 C「わがやに かえった ようだ。」 |
| 3 ("16-bit") | C / K / W | C: "The music has... more channels." K: "Papa, the blocks have *gradients*." W: "BEHOLD! SIXTEEN BITS!" | C「おんがくの チャンネルが・・・ ふえている。」 K「パパ、 ブロックに *グラデーション* が ある!」 W「みよ! 16ビット じゃあ!」 |
| W1 boss (proposal: THE UPGRADER, §5.4) grabs Rockman | boss / K | "INSTALLING... 3%... PLEASE DO NOT TURN OFF YOUR ROBOT." K: "Don't turn him off!" | 「インストールちゅう・・・ 3%・・・ ロボットの でんげんを きらないで ください。」 K「きっちゃ だめー!」 |
| boss down | K | The upgrade's rolling back! | アップグレードが もとに もどっていく! |

#### S36 W2: the Bracket of Doom · Must

A teleporter hall laid out as a bracket (`fortress.md`). The refights are **data copies** built from the cup, not the
real champions, who watch from the stands (they stay good-natured, BRIEF §2). On entering:

| Who | EN | JP |
|---|---|---|
| W | The BRACKET OF DOOM! Your old opponents, rebuilt from your own match data! | ドゥームの トーナメントへ ようこそ! おまえの データから つくった むかしの あいて じゃ! |
| K | Those aren't the real champions! They're copies! | ほんものの チャンピオンじゃ ない! コピーだよ! |
| C | The real ones are in the stands. Booing. | ほんものは かんきゃくせきに いる。 ブーイング ちゅうだ。 |

On each refight's bar fill, the **real** champion shouts from the stands (POP):

| Champion | EN | JP |
|---|---|---|
| Blizzard | Hey! That copy's got MY skis! Get him! | おい! あの コピー おれの スキー はいてるぞ! やっちまえ! |
| Wind | My copy can't even fly straight! Shoot him down! | おれの コピー まっすぐ とべて ないぜ! うちおとせ! |
| Plant | Oh no, he's trampling everything. Please hurry. | ああ なにもかも ふみつけて。 いそいで ください。 |
| Flame | An impostor! Duel him for my honour! | にせものめ! わがはいの めいよの ために たたかって くれ! |
| Yamato | That one moves too much. It is not me. | あやつは うごきすぎる。 せっしゃ では ない。 |
| Tomahawk | That ain't me, partner. I never drew that slow. | ありゃ おれじゃ ない。 おれは あんなに おそく ぬかない。 |
| Knight | A false knight! Smite him, I beseech thee! | にせの きしめ! なんじ たのむ、 うちたおせ! |
| Centaur | Does the copy know my ability? I'd love to know. | コピーは わたしの のうりょくを しって いるのかな? わたしも しりたい。 |

#### S37 Bass β, duel 2 · Must

At the bracket's top. `systems.md` SC6: his armour starts adapted to the weapon the player used most in duel 1, so the
script tells the player what to do about it.

| Who | When | EN | JP |
|---|---|---|---|
| B | before | Round two, original. I've been patched. Every weapon you used on me, I'm ready for. | 2ラウンドめだ オリジナル。 パッチは あてた。 まえに つかった ぶきは ぜんぶ たいさく ずみだ。 |
| R | | Then I'll use the others. | なら ほかの ぶきを つかうよ。 |
| B | | ...Huh? | ・・・は? |
| B | defeated | Tch... Next time, it won't be 8-bit. (teleports out) | ちっ・・・ つぎは 8ビットじゃ ねえぞ。 |
| K / C | | K: "Next time?" C: "He sounded very sure." | K「つぎ?」 C「ずいぶん じしん ありげ だったな。」 |

Bass's last line is PLAN's nod to Rockman 7 (1995), where Bass debuts in 16 bits (Appendix A, A-7.1).

#### S38 Wily Machine 6.5 · Must

| Who | When | EN | JP |
|---|---|---|---|
| W | before | Behold my masterpiece: WILY MACHINE 6.5! Halfway to the future! | みよ わしの けっさく! ワイリーマシーン 6.5ごう! みらいへの はんぶん じゃ! |
| K / C | | K: "Six point five?" C: "He couldn't wait for seven." | K「6.5?」 C「7まで まてなかった らしい。」 |
| W | pinch (the Mode 7-style floor starts) | MODE 7! The floor ROTATES! ...It's supposed to rotate. | モード7! ゆかが かいてん するのじゃ! ・・・する はず なのじゃ。 |
| K / C | | K: "It's just scrolling in strips." C: "It's a very good effort." | K「よこじまで スクロール してる だけ だよ。」 C「よく がんばって いる。」 |
| W | destroyed | Not yet! NOT YET! | まだじゃ! まだ おわらんぞ! |

Kalinka is right: the "Mode 7" floor is a per-band scroll trick (PLAN §3.5, `fortress.md`), the honest NES answer to a
Super Famicom feature. The joke is the effect's own credit line.

#### S39 The Wily Capsule; the dogeza · Must

| Who | When | EN | JP |
|---|---|---|---|
| W | before | The capsule has THREE NEW COLOURS! | カプセルには あたらしい いろが 3つも あるのじゃ! |
| W | defeated, on his knees (vanilla's ending animation, kept) | F-forgive me! It was Mr. Y's idea! Mr. Y made me do it! | ゆ、 ゆるして くれ~! Mr.Y の さしがね なのじゃ! Mr.Y に やらされたのじゃ! |
| R | | You ARE Mr. Y. | あなたが Mr.Y です。 |
| W | | ...Mr. Y is very persuasive. | ・・・Mr.Y は くちが うまいのじゃ。 |

#### S40 The castle falls; Break Man carries Rock out · Must (lines), Should (carry art)

The castle collapses (the escape is `fortress.md`'s). At its end the floor gives way under Rockman, who is holding
Wily by the collar. The homage: in Rockman 3's ending, Break Man pulls Rock from Gamma's wreckage (Appendix A, A-3.5).

| Variant | Who | EN | JP |
|---|---|---|---|
| partner | (whistle; a hand catches Rock's) BM | ...Tch. I'll take him too. This time. | ・・・ちっ。 そいつも つれていく。 こんどは な。 |
| partner | R | Blues? | ブルース? |
| partner | BM | Break Man. (sets Rock and Wily down on the grass; the whistle fades) | ブレイクマン だ。 |
| walked (DOPED) | (Rock escapes on Rush; far away on a ridge Break Man watches, then turns away. No line.) K (radio) / C | K: "Was that...?" C: "Yes." | K「いまのは・・・?」 C「ああ。」 |

This is Rock's second and last "Blues?" (§1.3). "This time" answers Rockman 3, where Break Man said he was too late
to save Wily and left him in the rubble (Appendix A, A-3.5).

#### S41 Wily to jail: "Mr. Z" · Must

The Committee's security robots lead Wily away (vanilla's arrest, re-staged).

| Who | EN | JP |
|---|---|---|
| W | This isn't over! Next year there will be a MR. Z! | これで おわりと おもうな! らいねんは Mr.Z じゃ! |
| K | Papa, there are no more letters after Z. | パパ、 Z の つぎは もう もじが ないよ。 |
| C | He will find one. | あいつなら みつける だろう。 |

### Act VI: the ending

#### S42 Lights out, one channel at a time · Must, [new-music] S

The empty GP stadium at night. Light and Rock sit in the stands; Roll, Rush and (if B-E-A-T is complete) Beat beside
them. The scoreboard shows the finished bracket. The music is an arrangement of the ending theme with **one stem per
channel**, and the stems drop out one by one on the marked pages (`art_audio.md` builds it; the vanilla driver can stop
a channel by sending it a rest).

| # | Cue | Who | EN | JP |
|---|---|---|---|---|
| 1 | all channels | L | Wily wasn't wrong, you know. The 16-bit machines are coming. Bigger, faster, more colours. | ワイリーの いうことも まちがっては おらん。 16ビットの マシンは もうすぐ くる。 おおきく はやく いろも ゆたかに。 |
| 2 | | R | Will I have to upgrade too, Doctor? | ぼくも アップグレード しなくちゃ いけないん ですか? |
| 3 | DPCM stops | L | Someday. When you're ready. Not by force. Not tonight. | いつかは な。 おまえの じゅんびが できたら。 むりやり では なく。 こんや でも なく。 |
| 4 | noise stops | L | Every machine I build will be outdone by the next one. That isn't sad, Rock. That's the job. | わしが つくる マシンは みな つぎの マシンに こえられる。 それは かなしい ことでは ない。 それが しごと なのじゃ ロック。 |
| 5 | triangle stops | Ro | Rock, Doctor, they're closing the stadium. | ロック、 はかせ、 スタジアム しまっちゃうわよ。 |
| 6 | pulse 2 stops; the scoreboard goes dark | R | Let's go home. | かえろう。 |
| 7 | pulse 1 plays four notes alone, then stops | (silence, 60 f) | | |

If MMC5 AUDIO is on, its two extra pulses were already silenced when the castle fell (they are Wily's 16-bit
channels): the ending starts on the console's own five.

#### S43 The sixth wing · Must

The Hall of Fame, the next morning. A new wing has opened; the GP Cup stands under its plaque. The museum of the past
ends on the game being played.

> EN: WING 6 · ROCKMAN 6: SHIJO SAIDAI NO TATAKAI!!, "The Greatest Battle in History!!". Famicom, 5 November 1993.
> The last Rockman on the Famicom. / Its eight Robot Masters were designed by fans. Knight Man and Wind Man came
> from readers in North America. / In North America it was published by Nintendo, in March 1994. / Six weeks after
> its release, on 17 December 1993, Rockman X came out on the Super Famicom: six years to the day after the first
> Rockman. / Exhibit: the GP Cup. Donated by the winner.
>
> JP: ウイング6 ・ ロックマン6 しじょう さいだいの たたかい!! 1993ねん 11がつ 5にち はつばい。 ファミコンで
> さいごの ロックマン。 / 8たいの ボスは すべて ファンの デザイン。 ナイトマンと ウインドマンは きたアメリカの
> ファンの さくひん。 / きたアメリカでは 1994ねん 3がつ にんてんどうが はつばい した。 / はつばいの 6しゅうかんご、
> 1993ねん 12がつ 17にち スーパーファミコンで ロックマンXが はつばい。 さいしょの ロックマンから ちょうど 6ねんご
> の おなじ ひ だった。 / てんじひん: GPカップ。 ゆうしょうしゃより きぞう。

#### S44 The CAPCOM TIMES · Must, [new-art] S

Vanilla's newspaper driver (`$3B:$A886`): masthead `CAPCOM TIMES ●▲.●▲.20XX` kept, a new picture headline per variant
(art), and the typed body. The last two pages are **vanilla's own `$95`/`$96` text, kept word for word in JP** (the
sincere last line of the 1993 game); EN translates it.

| Page | Normal | Variant |
|---|---|---|
| headline (art) | ROCKMAN WINS GP!! | DOPED: CHAMPION'S CHIP UNDER REVIEW · BASS file (Could): BASS WINS GP. WILY DENIES SPONSORING HIM |
| 1 | Rockman wins the Grand Prix! Sponsor "Mr. Y" revealed as Dr. Wily (everyone: "We know"). / ロックマン グランプリ ゆうしょう! スポンサー 「Mr.Y」 の しょうたいは Dr.ワイリー (みんな 「しってた」)。 | DOPED: The judges are reviewing a chip stamped with a "Y". The result stands, with an asterisk. / しんさいんは 「Y」 の きざまれた チップを ちょうさ ちゅう。 けっかは ほしじるし つきで せいりつ。 |
| 2 | Dr. Wily is back in jail. Guards have been told to check daily that he is not a cardboard cut-out. / ワイリーは ふたたび ろうやへ。 かんしゅには まいにち 「だんボールの にんぎょう では ないか」 かくにん する よう しじが でた。 | |
| 3 | The mystery robot "Bass" is still at large. He was last heard saying "next time". / なぞの ロボット 「フォルテ」 は いまも ゆくえふめい。 さいごに 「つぎは」 と いっていた という。 | |
| 4 | The Committee announces next year's sponsor: a "Mr. Z". Dr. Cossack has asked for a longer alphabet. / いいんかいは らいねんの スポンサーを はっぴょう。 「Mr.Z」 だという。 コサックはかせは もっと ながい アルファベットを ようきゅう している。 | |
| 5 (vanilla `$95`, kept) | But with a heart that loves peace, and the strength never to lose to evil... / しかし へいわを あいする こころと / あくに まけない ちからを もった | |
| 6 (vanilla `$96`, kept) | ...as long as the strongest robot, Rockman, is here, this peace will surely last!! / さいきょうのロボット ロックマンが / いるかぎり このへいわは つづくだろう!! | |

Vanilla's own page `$94` ("he may be building a jailbreak robot inside his cell") is not reprinted: S02 quoted it,
and page 2 answers it.

#### S45 The victory lap (playable credits) · Should

CX's playable staff roll (`cx/SUMMARY.md` §2 item 24), meta 23; `fortress.md` builds the level. Rockman runs a lap of
the GP stadium through miniature venues; names are written into the scenery. The text, in order:

1. **THE CHAMPIONS.** At each venue, the champion stands in the stands, says one line (POP), and his vanilla card is
   shown **verbatim**, including vanilla's alphabetical order and its spellings (`DWNB-41 BLIZZARD-MAN / DESIGNER
   HIROFUMI OGAWA` … `DWNB-48 YAMATOMAN / DESIGNER RAI ICHIKAWA`, `rm6/text.md` §5.6). These eight people are the
   reason the game exists; their cards are the sincere centre of the credits.

   | Champion | EN | JP |
   |---|---|---|
   | Blizzard | Good match, champ! The sun came out for you! | いい しあい だったぜ! おまえの ために たいようが でたな! |
   | Centaur | I found my ability! It's cheering! | わたしの のうりょくが わかりました! おうえん です! |
   | Flame | A bow for the champion! | チャンピオンに けいれい! |
   | Knight | Huzzah! All hail the champion! | ばんざい! チャンピオンに えいこう あれ! |
   | Plant | I planted something for you. It will bloom next year. | あなたの ために たねを まきました。 らいねん さきます。 |
   | Tomahawk | Fastest gun in the Grand Prix. Shake, partner. | グランプリ いちの はやうち。 あくしゅ だ。 |
   | Wind | Okay. You're the ace. This time. | わかったよ。 エースは おまえだ。 こんかいは な。 |
   | Yamato | This one... moves. For you. A little. (he takes one step) | せっしゃ・・・ うごく。 そなたの ために。 すこしだけ。 |

2. **ALL ENTRANTS.** Every enemy, in the classic Capcom roll-call style, under the heading `ALL ENTRANTS` (4MI's
   FABRICATED ENEMIES, `r4mi/text.md` §0), each followed by its result, always `ELIMINATED`. The names come from the
   venue and fortress docs (TOPPY, NITPICKY, SHIROKUMA, PROPELLER MET, KITE MET, AYACO, METSLIME, METAL METSLIME,
   KILLER CHEST, SIDEWINDER, CONGA, JAJA-NIN, GRIM REAP-BOT, NASUBI MAGE, CENTURION-BOT, SKELETON-BOT, …). The text
   build collects them from each doc's object list, so none is forgotten. The last two entries: `GRAND PI-KUN
   ...DEFLATED` and `BASS β ...ESCAPED`.
3. **ROCKMAN 6 GP STAFF.** Role headers in vanilla's cyan role font (A=`$80`); names in romaji capitals in both
   languages, as vanilla. The release build refuses an empty role (no placeholder ships: 4MI's WIP lesson). The
   TRANSLATION credit reads `(RESERVED)` in ENGRISH only (4MI's credit, `meta.md` §12).
4. **THE 1993 STAFF.** Vanilla's roll (`$81-$86`), unchanged: the contest entrants, `-PLANNER- TURKEYー613` … `AND
   CAPCOM ALL STAFF`, then vanilla's `PRESENTED BY CAPCOM` page (`$87`) under a `ROCKMAN 6 (1993)` header, so it
   credits the original game and not the patch.
5. **SPECIAL THANKS.** ROCKMAN CX (HIMAJIN JICHIKU); ROCKMAN 4 MINUS INFINITY (PURESABE); "AND EVERY FAN WHO EVER
   MAILED A ROBOT TO CAPCOM." / 「そして カプコンに ロボットを おくった すべての ファンへ。」
6. **The finish line**: everyone waits at the tape (the champions, Roll, Light, Eddie, Beat, Cossack, Kalinka). K: "And
   the winner is..." / 「そして ゆうしょうは・・・」 → S46.

#### S46 The championship rating · Must

`meta.md` §6 owns the rows, tests and arithmetic. Rank titles (JP in katakana, the panel keeps EN in both):

| EN | JP |
|---|---|
| GRAND CHAMPION | グランドチャンピオン |
| CHAMPION | チャンピオン |
| FINALIST | ファイナリスト |
| SEMIFINALIST | セミファイナリスト |
| QUARTERFINALIST | クォーターファイナリスト |
| PARTICIPANT (with the ribbon) | さんかしゃ |

#### S47 Break Man's debrief · Must

`meta.md` §6.2's table, restyled into Break Man's voice (§2.2): one greeting, then the entry for the first failed test,
then "...Hmph." and S48. One hint per test is kept, as meta requires.

| Entry | EN | JP |
|---|---|---|
| greeting | ...You won. Not bad, Rock. | ・・・かったか。 わるくない、 ロック。 |
| T0 Beat | That bird's still in pieces. B. E. A. T. Spell it. | あの とりは まだ バラバラ だ。 B、 E、 A、 T。 ぜんぶ あつめろ。 |
| T1 never called | You barely called me. Pause, SELECT. I'd have come. | ほとんど よばなかったな。 ポーズして セレクト。 よべば いった。 |
| T1 doped | You took Y's chip. I don't tag with cheats. | Mr.Y の チップを つかったな。 ずるを する やつとは くまない。 |
| T2 exits | The judges counted %N% secret exits. There are 8. One per venue. | ひみつの でぐちは %N%こ。 ぜんぶで 8こ。 かいじょうに 1こずつ だ。 |
| T3 exhibitions | Four badges on that bracket. Two secret exits light each one. | ひょうに バッジが 4つ。 ひみつの でぐち 2つで 1つ ひかる。 |
| T4 rooms | Every venue hides one room, one screen big. Listen to the judges. | どの かいじょうにも かくしべやが ひとつ。 しんさいんの ヒントを きけ。 |
| T5 chips | Some prizes aren't won by winning. They're won by acting strange. | かって もらえない しょうひんも ある。 かわった ことを して もらうんだ。 |
| T6 gear | Eddie's shelf isn't empty. Neither is his garage. | エディの たなは まだ から じゃない。 ガレージも な。 |
| T8 gold | Gold in every venue. You know what to do. | ぜんぶの かいじょうで ゴールド。 わかるな。 |
| T9 platinum | Ninety-five is a perfect run. Get three. | 95てんは かんぺきな しあい だ。 3つ とれ。 |
| T10 game overs | %N% game overs. A champion doesn't pay the entry fee twice. | ゲームオーバー %N%かい。 チャンピオンは さんかひを 2どは はらわない。 |
| T11 time | %H%:%MM% on the clock. A first title takes under three hours. | %H%じかん %MM%ふん。 はじめての ゆうしょうなら 3じかん いない だ。 |
| T12 unplugs | The stadium lost power %N% times in your matches. Funny. It never does. | おまえの しあいの とき だけ スタジアムが %N%かい ていでん した。 ふしぎ だな。 |
| T13 rival | Bass tells everyone he hit you in the Semifinal. Make him a liar. | フォルテは じゅんけっしょうで おまえに あてたと いいふらしてる。 うそに してやれ。 |
| T14 card | Someone dropped a card in the Hall of Fame. "Mr. X." A real one? | ホール・オブ・フェイムに めいしが おちてる。 「Mr.X」。 ほんもの か? |
| T15 top seed | You went down in a champion's ring. Top seeds don't. | チャンピオンの リングで たおれたな。 トップシードは たおれない。 |
| perfect | Nothing to add. You're the champion. Go home, Rock. Wily won't stay put. | いう ことは ない。 チャンピオンは おまえだ。 かえれ ロック。 ワイリーは じっと して いない。 |
| perfect, ENGRISH | I HAVE NO ADVICE. / YOU ARE REAL CHAMPION! (`meta.md` §12's 4MI tribute: the one ENGRISH line in story text, on purpose) | (JP unchanged) |
| BASS file, T1 | Even Wily's own robot gets an asterisk. (`meta.md` §9.7) | ワイリーの ロボットにも ほしじるしが つく。 |
| close | ...Hmph. | ・・・ふん。 |

The perfect line points at Rockman 7, which opens with Wily breaking out of jail (Appendix A, A-7.2).

#### S48 TO BE CONTINUED [engine-ok] · Must

Vanilla script `$88`, typed at 4 f/tile, in English in both languages, kept on purpose (rm6 lesson 8). On the first
clear, `(SPECIAL EVENTS ARE NOW OPEN)` follows (`meta.md` §6.2) / 「(スペシャルイベントが ひらいた)」.

### Post-game

#### S49 Post-game bracket intro (EVENTS b7) · Should

| Who | EN | JP |
|---|---|---|
| K | Welcome back, champion! Every match is open for rematches. Medals don't polish themselves! | おかえり チャンピオン! ぜんぶの しあいで さいせん できるよ。 メダルは かってに ひからないからね! |
| C | Also, the museum has a new wing. Someone donated a cup. | それと はくぶつかんに あたらしい ウイングが できた。 だれかが カップを きぞう したそうだ。 |

#### S50 Mr. X Returns · Could

`meta.md` §9.8: the real Mr. X, a separate person, replays the 1993 Mr. X Fortress 1 exactly as it was. One SCN
before the stage, one after the chair fight.

| When | Who | EN | JP |
|---|---|---|---|
| before | X | So. You are the robot who keeps defeating people named after me. | ほう。 わたしの なまえを かたる ものを たおして まわって いる ロボットとは きみか。 |
| | R | Named after you? | あなたの なまえ? |
| | X | I am MR. X. The REAL one. International robot financier. First Wily borrowed my name. Then he took the NEXT LETTER. Do you know how that looks on a business card? | わたしが Mr.X だ。 ほんものの。 こくさい ロボット とうしか。 まず ワイリーが わたしの なまえを かたり、 つぎは *つぎの もじ* まで もっていった。 めいしに どう みえるか わかるかね? |
| | K | Papa, the card was real! | パパ、 めいし ほんもの だった! |
| | C | ...I said let us not think about it. | ・・・かんがえないで おこうと いったのに。 |
| | X | I have bought the 1993 fortress, exactly as it was. Come and see how a REAL Mr. X does it! | 1993ねんの ようさいを そのまま かいとった。 ほんものの Mr.X の やりかたを みせて あげよう! |
| after | X | Fine. FINE. Keep the alphabet. | わかった。 わかったとも。 アルファベットは くれてやる。 |

#### S51 Bass Mode line swaps · Could

On a BASS file (`meta.md` §9.7), these beats swap. Everything else plays as written with "Bass" in Rockman's place
where a line names the player.

| Beat | Swap |
|---|---|
| S02 panel 6 | B: "Original this, original that. Watch me win the whole thing." / 「オリジナル オリジナル うるさい。 ぜんぶ かって みせる。」 |
| S06 | Entrant β is the player; Rockman is announced as entrant 9 and says "Bass, this isn't a game." B: "It's literally a game." / R「フォルテ、 これは あそびじゃ ない。」 B「どう みても ゲーム だろ。」 |
| S14 | The Riot is Rockman crashing *Bass's* bracket (`meta.md` §9.7): R: "Bass! Stop this!" B: "Make me." / R「フォルテ! やめるんだ!」 B「とめて みろ。」 |
| S20 | No partner. K: "Bass works alone." C: "He says." / K「フォルテは ひとりで たたかう。」 C「と いっている。」 |
| S33 | W: "Bass, my boy! Help me!" B: "Pay me first." / W「フォルテよ! たすけて くれ!」 B「さきに かね だ。」 |
| S42 | Bass alone on the stadium roof. B: "Sixteen bits, huh." (the channels drop out the same way) / B「16ビット か。」 |

