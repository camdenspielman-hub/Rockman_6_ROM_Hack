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

- **Role:** pit crew (BRIEF §2): adaptor hand-offs on the bracket (S11, S13), the Super Adaptor (S29), the lobby in GP
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

EOF