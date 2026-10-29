# Rockman 6 GP: narrative bible and script plan (story.md)

Owner: design-story. Status: **v1, complete for its scope** (§0-§12, Appendix A).
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
| **Sports broadcast, played straight** | Cossack and Kalinka call the action like a real tournament: stats, records, replays, "the judges are not pleased". The comedy comes from treating a robot brawl as a sporting event | CX's straight-faced villain inversion (cx SUMMARY §5) | C: "A clean match from Rockman. The judges will remember that slide." |
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
8. **ENGRISH never touches story text, hints or help pages** (`meta.md` §12). It is a menu joke only (§9), with one
   deliberate exception: Break Man's perfect-score line, 4MI's own (S47).

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

Each scene: where it plays, then the lines. JP is a draft for a native-speaker pass (Risks, item 2). Line lengths obey
§10.2 (28 cells per line; a POP page is ≤ 2 lines, a SCN page ≤ 4).

### 4.0 The arcs at a glance

**Break Man's beats** (the 4MI Proto Man pattern, then the CX Quick Man pattern; BRIEF §2, §5.6). Three variants run
through the late game: **partner** (FORMS.TAG, the normal path), **walked** (RATEFLAGS.DOPED: he left after the
booth), and **no tag** (if SYS-TAG-1 is cut, Risks item 7).

| # | Scene | What he does | Helps how | Variants |
|---|---|---|---|---|
| BM-1 | S06 roll call | Registers as entrant 10, no sponsor, no data; "Break Man." | — | — |
| BM-2 | S08 Opening boss | "Hold B. Let go when you glow." | teaches the charge shot | — |
| BM-3 | S18 Semifinal | Holds back the rioting crowd: "Go. I've got the crowd." | clears the set piece | — |
| BM-4 | S20 Rule 9 | Steps forward as tag partner; explains the call | the tag mechanic unlocks | no tag: a far whistle only |
| BM-5 | S21 the booth | Is "watching"; walks if you dope; pause portrait `N0` | the moral cost, shown not told | — |
| BM-6 | S30 H5 | His in-tune whistle unmasks Dark Man, as in Rockman 5 | ends the disguise phase | partner: speaks; walked: offscreen, silent |
| BM-7 | S40 the fall | Catches Rock, takes Wily too: "This time." | Rockman 3's ending, answered | walked: watches from a ridge; no tag: as walked |
| BM-8 | S47 debrief | The 4MI-style hint, then "...Hmph." | the post-game hint | doped and BASS variants |

**Bass β's beats**: S06 (entrant β, "I'm the FINAL version!"), S14 (the Riot), S19 (duel 1: "the beta build has...
bugs!"), S37 (duel 2, patched against your favourite weapon: "Then I'll use the others."), S44 (still at large,
"next time").

**Mr. Y / Wily**: the ladder in §1.3; S21 (booth), S25 (theft), S26 (map), §6.5 (heckles), S32-S33 (unmasking and
Project SUPER), S34-S39 (the castle), S41 ("Mr. Z").

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
| 2 | **new**: a jail cell with a cardboard Wily cut-out in it and a sign, BACK IN 5 MINUTES | Wily went to jail. The CAPCOM TIMES warned that he might build a jailbreak robot in his cell. / This year the jail reports that he is still there. | ワイリーは ろうやへ。 「ろうやで だつごくよう ロボットを つくって いるかも しれない」と カプコンタイムスは かいた。 / ことし けいむしょは 「ワイリーは まだ いる」と はっぴょう している。 |
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

---

## 5. Boss intro cards (vanilla's boss panel, extended)

### 5.1 Format [engine-ok] + [new-code] S · Must

Vanilla's panel (`rm6/text.md` §4.4): after the frame (script `$13`) and CHR set `$8F` load, `$3C:$81B1` types one
**record** per boss: 9 fields, each ended by a byte with bit 7 set, chosen by `$51` through the pointer tables at
`$3C:$8606/$860E`. Field addresses and delays are tables (`$85EE-$8615`), so the layout can be re-flowed without code.

GP keeps the record format and its English text **in both languages** (vanilla's panel is English even in the JP
game; kept as a quirk, rm6 lesson 8), and changes three things:

1. **Record selection by fight id**, not `$51`: a 2-byte pointer per fight id (`meta.md` §9.2.1's fight table), so
   the champions, the guests, the legacy exhibits and the castle bosses all get cards, and ENTRANT FILES in the
   Museum (`meta.md` §9.5) reuses the same records. [new-code] S.
2. **A tenth field, VENUE** (≤ 20 characters, 2 f/tile), placed in a strip the art adds to the panel frame
   (`art_audio.md`). [new-code] S (the field counter `$0624`, which counts 8 down to 0, starts at 9), [new-art] S.
3. **Five glyphs added to the panel's bold set** at `$26-$2A`: `-` `?` `!` `'` `β` (the panel CHR has 87 free
   tiles, `rm6/text.md` §7). [new-art] S.

| Field | Width | Vanilla address | Rule |
|---|---|---|---|
| HEIGHT / WEIGHT / ATTACK / DEFENCE / MOBILE | 3 each | `$206A` `$2079` `$20AA` `$20B9` `$20EA` | digits, right-aligned with spaces |
| ENERGY | ≤ 13 | `$20F1` | |
| LOCATION | ≤ 20 | `$2126` | |
| SPECIALTY | ≤ 19 | `$22E6` | |
| NAME | ≤ 12 | `$22AA` (8 f/tile, sound `$27`) | vanilla style: no space in a Robot Master name (`BLIZZARDMAN`) |
| VENUE (new) | ≤ 20 | art places it | |

Glyphs allowed on the panel: `0-9 A-Z . space` (vanilla) plus the five above. The text compiler checks widths and
glyphs (§10.3).

After the panel, the stage loads, and when the boss bar fills the **bar-fill line** (POP) plays: S11 for champions,
S19/S37 for Bass β, S23 for guests, S28 for exhibits, S35-S39 for the castle.

**On-screen venue names.** The venue docs' working titles go on the card, with one change: Flame's "PRINCE OF
PERSIA PALACE" is 23 characters (over the 20 limit) and uses a third-party trademark as an on-screen title, which
BRIEF §6 rules out ("parody names"). This doc proposes **PERSIAN PALACE** for every on-screen use (card, bracket,
records). The design name can stay in the docs. (Open question 2; `venues_b.md` owns the venue.)

### 5.2 The eight champions: vanilla's records, kept verbatim

The 1993 numbers are canon and they carry three of the venue jokes (SOLAR ENERGY on a glacier, MOBILE 31, ABILITY
UNKNOWN). Only VENUE is new.

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE |
|---|---|---|---|---|---|---|---|---|---|
| BLIZZARDMAN | 163 | 167 | 88 | 42 | 113 | SOLAR ENERGY | FROZEN ISLAND | MASTER OF SNOW | SUMMIT CLIMBER |
| WINDMAN | 169 | 173 | 66 | 129 | 51 | WIND ENERGY | MECHANICAL TOWER | MASTER OF WIND | SKY ACE 1943 |
| PLANTMAN | 143 | 111 | 42 | 103 | 98 | SOLAR ENERGY | FORGOTTEN AREA | FLOWER FANCIER | JUNGLE PITFALL |
| FLAMEMAN | 155 | 98 | 84 | 93 | 88 | THERMAL POWER | OIL FIELD | MASTER OF FLAME | PERSIAN PALACE |
| YAMATOMAN | 161 | 149 | 199 | 185 | 31 | SOLAR POWER | IMPREGNABLE FORTRESS | MASTER OF SPEAR | EDO NINJA ROW |
| TOMAHAWKMAN | 177 | 87 | 157 | 71 | 149 | SOLAR POWER | RESTRICTED AREA | MASTER OF TOMAHAWK | GUN.SMOKE FRONTIER |
| KNIGHTMAN | 158 | 146 | 121 | 204 | 60 | SOLAR POWER | CAPITAL OF SCIENCE | MASTER OF MACE BALL | DRAGON QUESTLIKE |
| CENTAURMAN | 155 | 172 | 35 | 47 | 205 | DRY BATTERY | ANCIENT CITY | ABILITY UNKNOWN | ATLANTIS RUINS |

Secret-room fights use the same record with VENUE replaced by the secret arena's name (≤ 20): `WING WALKER`, `THE
KNIGHTLORD`, `THE HIDEOUT`, `THE LOST CITY`, `CLOUD SUMMIT`, `THE THRONE ROOM`, `THE SUNKEN THRONE`, `THE KABUKI
STAGE`. Refights in W2 replace NAME with the copy's (`BLIZZARD.EXE` is 12: the joke is that the copies are files) and
VENUE with `BRACKET OF DOOM`.

### 5.3 New entrants

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE | The joke |
|---|---|---|---|---|---|---|---|---|---|---|
| GRAND PI-KUN | 250 | 8 | 10 | 5 | 120 | HOT AIR | GP STADIUM | BEING ADORABLE | OPENING CEREMONY | an inflatable mascot weighs 8 kg |
| BASS β (Semifinal) | 133 | 105 | 199 | 99 | 199 | SPONSOR MONEY | MR.Y LABORATORY | BEATING ROCKMAN | SEMIFINAL RIOT | one centimetre taller than Rockman's commonly given 132 cm (Appendix A, A-6.5); K: "He measured with his hair." The SPECIALTY is never true |
| BASS β (W2) | 133 | 105 | 255 | 199 | 255 | SPONSOR MONEY | SUPER WILY CASTLE | FINAL VERSION | BRACKET OF DOOM | the β stays on the NAME; he typed FINAL VERSION himself |
| BLOCK MAN | 4 | 4 | 1 | 4 | 1 | GRAVITY | THE WELL | LINE CLEAR | EXHIBITION 1 | four blocks by four; the playfield of a falling-block game is often called the well |
| PADDLE MAN | 8 | 32 | 1 | 999 | 255 | BOUNCING | THE BRICK WALL | RETURNING BALLS | EXHIBITION 2 | |
| INVADER MAN | 16 | 16 | 10 | 1 | 8 | 100 YEN COINS | TABLE CABINET | MARCHING DOWN | EXHIBITION 3 | the cocktail-table cabinets of 1978 cafés |
| MAZE MAN | 16 | 16 | 4 | 1 | 88 | POWER PELLETS | LEVEL 256 | EATING | EXHIBITION 4 | |

### 5.4 Hall of Fame exhibits and the castle

The exhibit cards are museum labels: LOCATION carries the year of the original fight.

| NAME | HEIGHT | WEIGHT | ATTACK | DEFENCE | MOBILE | ENERGY | LOCATION | SPECIALTY | VENUE |
|---|---|---|---|---|---|---|---|---|---|
| YELLOW DEVIL | 480 | 999 | 140 | 120 | 160 | CENTRAL EYE | WILY CASTLE 1987 | REASSEMBLY | HALL OF FAME 1 |
| MECHA DRAGON | 600 | 999 | 180 | 150 | 140 | DRAGON FIRE | WILY CASTLE 1988 | CHASING | HALL OF FAME 2 |
| GAMMA | 999 | 999 | 200 | 200 | 10 | PEACEKEEPING | WILY CASTLE 1990 | KEEPING THE PEACE | HALL OF FAME 3 |
| C.CATCHER | 300 | 450 | 90 | 130 | 180 | PRIZE TOKENS | COSSACK CITADEL 1991 | GRABBING PRIZES | HALL OF FAME 4 |
| BREAK MAN? | 170 | 120 | 150 | 140 | 100 | DISGUISE KIT | BLUES CASTLE 1992 | IMPERSONATION | HALL OF FAME 5 |
| THE UPGRADER | 256 | 512 | 16 | 16 | 8 | 16 BIT CORE | SUPER WILY CASTLE | FORCED UPDATES | UPGRADE LAB |
| WILY MACHINE | 999 | 999 | 250 | 250 | 65 | THE GP CUP | SUPER WILY CASTLE | VERSION 6.5 | PROJECT SUPER |
| WILY CAPSULE | 200 | 300 | 160 | 80 | 220 | PURE GENIUS | SUPER WILY CASTLE | ESCAPING | PROJECT SUPER |
| MR.X (Could) | 175 | 70 | 50 | 50 | 50 | OLD MONEY | MR.X FORTRESS 1993 | BEING MR.X | MR.X RETURNS |

Notes:

- **Dark Man's card** says `BREAK MAN?`, with the question mark. K: "Why is there a question mark?" C: "Museums are
  honest." / K「なんで はてなが ついてるの?」 C「はくぶつかんは しょうじき なのだ。」 It reads `DARKMAN` in ENTRANT FILES.
- **THE UPGRADER** is this doc's **proposal** for the W1 boss, which `fortress.md` owns and has not yet named: a
  machine that tries to install 16 bits into Rockman ("INSTALLING... 3%", S35). Its numbers are powers of two.
- **WILY MACHINE**'s MOBILE 65 is "6.5". Its ENERGY is the stolen cup (S33: the cup is the data core).
- **Mid-bosses** (AYACO, CONGA, the Daruma, the Metal Metslime, Sidewinder, Shadow Rock, …) get records for ENTRANT
  FILES only (Should); their venue owners fill in the fields with the same width rules. They show no card in play,
  as vanilla shows none for mid-bosses.

---

## 6. The commentator system

### 6.1 How it works [new-code] M · Must

BRIEF §5.5: the commentators react to deaths with a rotating table per venue plus generic lines; in the fortress, Mr.
Y heckles between lives; lines are ≤ 2 lines and toggleable. This is the engine that delivers them.

**Events.** Gameplay code raises an event id (one byte) with one argument byte. The ids, their owners and their tables:

| Event | Raised by | Argument | Table | Priority |
|---|---|---|---|---|
| `EV_DEATH` | the player-death path (exit code `$F0` = 2 or 3, `rm6/SUMMARY.md` §3; `tech.md` names the hook site) | cause: 0 enemy, 1 pit, 2 spike, 3 boss room | §6.3 venue table, then §6.4 | P1 |
| `EV_RESPAWN_HECKLE` | respawn in a fortress stage (meta 14-21) | — | §6.5 | P1 |
| `EV_WEAK_FIRST` | `systems.md` §5, once per fight | fight id | §6.2 / §6.3 | P2 |
| `EV_RESIST`, `EV_IMMUNE` | `systems.md` §5 | fight id | §6.2 | P3 |
| `EV_OWN_WEAPON` | SC4, once per fight | fight id | §6.3 | P2 |
| `EV_PINCH` | boss enters pinch | fight id | §6.3 | P3 |
| `EV_NODMG_BOSS` | boss killed, BOSS NO-HIT set (`systems.md` §6.5) | — | §6.2 | P2 |
| `EV_SECRET` | exit / room / item / plate / envelope collected | kind 0-4 | §6.2, venue line first if any | P2 |
| `EV_PARRY` | parry (first, and the 5th, per stage visit) | count | §6.2 | P3 |
| `EV_SYNERGY_FIRST` | first use of a synergy, once per save | synergy 0-7 | §6.2 | P3 |
| `EV_TIMESTOP_FIRST` | first C.FLASH Time Stop, once per save | — | §6.2 | P3 |
| `EV_CRIT` | a critical or EXCELLENT MOVE (first per stage visit) | — | §6.2 | P4 |
| `EV_CLOSE_CALL` | HP ≤ 3 and alive 300 f later (once per stage visit) | — | §6.2 | P4 |
| `EV_FORM_FIRST` | first use of POWER / JET / SUPER, once per save | form | §6.2 | P3 |
| `EV_TAG` | Break Man called / retreats | 0 call, 1 retreat | §6.2 | P3 |
| `EV_TANK` | E-tank or W-tank used (first per stage visit) | — | §6.2 | P4 |
| `EV_HOOK` | a venue object (a stable id, `BLZ-07`, `WND-03`, …) | hook id | §6.3 | P3 |

**Priorities and the queue.**

- **P0** is story (SCN), outside this system: it always plays and pauses the game.
- **P1** (death, heckle) plays on the respawn's READY, held 2 s or until any button.
- **P2-P4** play in the POP window during play, auto-advancing after `60 + 2 × characters` frames (90 minimum, 240
  maximum). No button dismisses a POP (the buttons are gameplay); START pauses it with the game.
- The queue holds 2 entries. A higher priority goes ahead; a P3/P4 entry older than 120 f is dropped (stale news is
  not news).
- **Cooldown:** after a P3/P4 line, no other P3/P4 line for 600 f. P1/P2 ignore it.
- **Never:** during a quick-draw (`venues_a.md` VA-DRAW), the panel, a T2 NPC window, a boss's own bar-fill line, the
  Semifinal's reaction-time beats if any, Time Attack (all lines off), and GP Rush (P1 only).
- **ANNOUNCER** (`meta.md` §11.1): ON = all; DEATHS ONLY = P1 (+ P0); OFF = P0 only.

**Rotation.** A venue's death table plays **in order**, one per KO in that stage visit; after its last line, the
generic table (§6.4) takes over at a save-wide rotating pointer, so the generic lines spread across the game.
Cause-specific generic lines (pit, spike, boss room) are preferred over plain generic ones when the cause matches.
"First" events use a 32-bit once-per-visit field in WRAM; once-per-save flags use 8 bits of FILE `$04A` (`meta.md`
§1.6 reserved for story.md: b0-7 = the first-use flags of POWER, JET, SUPER, Time Stop, the first plate, the first
envelope, Y-TURBO noticed, Break Man's first call).

**Data.** A line record is 6 bytes: speaker (face icon id), flags (variant selectors: pre/post unmask, BASS, DOPED,
TAG), EN pointer, JP pointer. Per-stage tables are byte lists of line ids. About 300 lines × 2 languages × ~45 bytes
≈ 27 KB in a text bank; ~2 KB of tables. [new-code] M (event bus, queue, window), text S per venue.

**Speakers and icons** (16×16 sprite face icons, `art_audio.md` §3.3): Cossack, Kalinka, Mr. Y, Wily, Roll, Break Man
(the visor), Light (radio static frame). Each speaker has a typing blip (§10.2).

### 6.2 Generic event lines

**First weakness hit on a non-venue boss** (`EV_WEAK_FIRST`; the weakness per `systems.md` §4.5):

| Boss | EN | JP |
|---|---|---|
| Grand Pi-kun (no WEAK cell: plays on the first charged hit) | K: Charged shots pop balloons! | K: チャージショットで ふうせんが われる! |
| Bass β (no WEAK cell: plays on the first hit after SC6 adapts, from a new column) | C: That one stung him! | C: いまのは きいたぞ! |
| Yellow Devil MK-VI (C.FLASH) | K: The eye flinched! | K: めが ひるんだ! |
| Mecha Dragon MK-VI (KNIGHT.C) | C: Right on the snout! | C: はなさきに めいちゅう! |
| Gamma MK-VI (W.STORM, phase 1) | K: It's wobbling! | K: ぐらついてる! |
| Cossack Catcher MK-VI (Y.SPEAR) | C: The claw's joint! ...I designed that joint. Badly. | C: アームの かんせつだ! ・・・わたしの せっけいだ。 よくない せっけいだ。 |
| Dark Man MK-VI (F.BLAST) | K: His disguise is melting! | K: へんそうが とけてる! |
| Wily Machine 6.5 (SILVER.T) | C: Silver Tomahawk on the Wily Machine! Just like 1993! | C: ワイリーマシンに シルバートマホーク! 1993ねんと おなじだ! |
| Wily Capsule (KNIGHT.C) | K: Bonk! C: That's the spot. | K: ゴツン! C: そこだ。 |
| Exhibition guests (the arena rule hits) | K: That's how you play it! | K: そう やって あそぶんだよ! |

Silver Tomahawk was the Wily Machine 6's weakness in vanilla (`systems.md` §4.5 note), so the line is true for 1993.

**Resisted and immune** (`EV_RESIST`, rotating; `EV_IMMUNE`):

| Event | EN | JP |
|---|---|---|
| resist 1 | C: That's barely scratching him! | C: ほとんど きいて いない! |
| resist 2 | K: Try something else! The judges like variety! | K: べつの ぶきを! しんさいんは バラエティが すき! |
| resist 3 | C: Watch the flashing. He shrugs that off. | C: てんめつを みろ。 へいき そうだ。 |
| immune | K: Not a scratch! | K: きず ひとつ ない! |

Resist 3 teaches the i-frame read (4MI's "read the weakness from the flashing", BRIEF §5.1).

**Style, forms, partner, tanks:**

| Event | EN | JP |
|---|---|---|
| no-damage boss (rotating) | K: Not a scratch on him! A perfect match! / C: The judges are standing. Two of them. The third is cardboard. (until S33; after: "The judges are standing. All of them.") / C: Flawless. Write that down, Kalinka. | K: むきず! パーフェクト! / C: しんさいんが たちあがった。 ふたり。 のこりは だんボール。 (S33 いこう 「ぜんいん たちあがった。」) / C: かんぺき だ。 メモして くれ カリンカ。 |
| parry, first | K: PARRY! He punched a bullet! C: Style points! | K: パリィ! たまを なぐりかえした! C: スタイル ポイント! |
| parry, 5th | C: Five parries. Somebody's been practising. | C: パリィ 5かい。 だれかさん れんしゅう したな。 |
| Time Stop, first | C: TIME, STOP! K: Papa, that's Flash Man's line! | C: ときよ とまれ! K: パパ、 それ フラッシュマンの セリフ! |
| synergy: Pogo | K: A pogo! Just like the duck with the cane! | K: ホッピング! ステッキの アヒルさん みたい! |
| synergy: Tailwind | C: Tailwind! Rush has never flown that fast. | C: おいかぜ! ラッシュが こんなに はやく とぶのは はじめてだ。 |
| synergy: Snow Bomb | K: Snow bombs! Look out below! | K: ゆきの ばくだん! したに ちゅうい! |
| synergy: Burning Knuckle | K: BURNING KNUCKLE! That sounds like a fighting game. C: It is one now. | K: バーニングナックル! かくとうゲーム みたい。 C: いまは そうだ。 |
| synergy: Petal Storm | K: A petal storm! It's beautiful! C: And bulletproof. | K: はなふぶき! きれい! C: そして ぼうだん。 |
| synergy: Morning Star | C: A giant flail! Knight Man is taking notes. | C: きょだいな フレイル! ナイトマンが メモ してる。 |
| synergy: Dive Throw | K: Dive-bombing tomahawks! | K: きゅうこうか トマホーク! |
| synergy: Time Fist | K: ORA ORA ORA! C: Kalinka, where did you learn that? | K: オラオラオラ! C: カリンカ、 どこで おぼえた? |
| critical / EXCELLENT MOVE | C: Critical hit! / (KAISHIN) K: AN EXCELLENT MOVE! | C: クリティカル! / K: かいしんの いちげき! |
| close call | K: Hanging on by one bolt! / C: Low on energy. High on spirit. | K: ボルト いっぽんで ふみとどまってる! / C: エネルギーは ひくい。 きあいは たかい。 |
| POWER, first | K: Rush POWER! Look at those fists! | K: ラッシュ パワー! すごい こぶし! |
| JET, first | K: He's flying! C: Nineteen units of fuel. Spend them wisely. | K: とんでる! C: ねんりょう 19。 だいじに つかえ。 |
| SUPER, first | C: Super Rockman! ...Is that legal? K: It's on loan. | C: スーパーロックマン! ・・・ルール いはん では? K: かりもの だから。 |
| Break Man called, first | K: Break Man is in! Tag team! | K: ブレイクマン とうじょう! タッグだ! |
| Break Man called, later | C: Entrant 10 enters the match. | C: 10ばん さんせん。 |
| Break Man retreats | BM: Tch. Your turn. | BM: ちっ。 おまえの ばんだ。 |
| tank used | C: A tank! There go the NO TANKS points. | C: タンクを つかった! ノータンク ポイントは なしだ。 |

The Pogo line names DuckTales by its hero (the duck with the cane); DuckTales is Capcom's own (1989), as `systems.md`
§3.2 credits. Time Fist's "ORA ORA" is the time-stop punch rush of *JoJo's Bizarre Adventure* Part 3; Flash Man's Time
Stopper is Rockman 2's (Appendix A).

**Secrets** (`EV_SECRET`; a venue's own line plays instead where its doc has one):

| Kind | EN | JP |
|---|---|---|
| secret exit | K: A secret exit! The judges love this! / C: Off the map. Literally. | K: ひみつの でぐち! しんさいん だいこうぶつ! / C: ちずに ない みち だ。 |
| hidden room | K: A hidden room! I KNEW it was there! | K: かくしべや! ぜったい あると おもってた! |
| behaviour item | C: A prize for *how* you played. The judges noticed. | C: *あそびかた* への しょうひん だ。 しんさいんは みていた。 |
| plate, first ever | C: Beat's parts! I built that bird, you know. | C: ビートの パーツ! あの とりは わたしが つくったんだぞ。 |
| plate, later | K: Another piece of Beat! | K: ビートの パーツ また ひとつ! |
| envelope | K: A sponsor envelope! Thirty bolts! C: From Mr. Y. Count it twice. | K: スポンサーの ふうとう! 30ボルト! C: Mr.Y から だ。 2かい かぞえろ。 |

Cossack really did build Beat, in Rockman 5 (Appendix A, A-5.4).

### 6.3 Venue tables: hooks and deaths

The venue docs own the triggers; the ids are theirs where they gave ids (venues_b: `BLZ-`, `FLM-`, `CEN-`, `YAM-`),
and this doc assigns `WND-`, `KNT-`, `TMH-`, `PLT-` to venues_a's tables in their order. Changes from the drafts are
marked †. Each venue has **6 death lines** (BRIEF §5.5), played in order, then the generic table.

#### Wind: SKY ACE 1943 (`venues_a.md` §1.9)

| Id | Trigger | EN | JP |
|---|---|---|---|
| WND-01 | launch | C: Rockman is cleared for takeoff! | C: ロックマン はっしん よし! |
| WND-02 | first POW shot | K: It changes when you shoot it! | K: うつと かわるよ! |
| WND-03 | a red squadron wiped | K: Red squadron down! | K: あかい へんたい げきつい! |
| WND-04 | AYACO appears | C: That's not a plane. That's a bigger plane. | C: あれは ひこうき では ない。 もっと おおきな ひこうき だ。 |
| WND-05 | AYACO shot down | K: AYACO is going down! | K: アヤコ ついらく! |
| WND-06 | tally 100 % | C: One hundred percent! In my day we called that an ace. | C: げきついりつ 100%! むかしは それを エースと よんだ。 |
| WND-07 | first gust | K: Watch the windsock, Rockman! | K: ふきながしを みて! |
| WND-08 | elevator unlocks | C: The elevator's moving. Where is he going? | C: エレベーターが うごいた。 どこへ いく? |
| WND-09 | W.STORM on Wind Man (SC4) | K: He LIKES that! | K: よろこんでる! |
| WND-10 | first C.FLASH hit (weak) | C: His engines stalled! No wind, no Wind Man! | C: エンジン ていし! かぜが なければ ウインドマンも ない! |
| WND-11 † | pinch (SKY ACE) | K: A loop! He's showing off! | K: ループ! かっこつけてる! |

Deaths: 1 K: Mayday, mayday! / メーデー、 メーデー! · 2 C: He forgot the loop button. / ループを わすれたな。 · 3 K: Gone
with the wind. / かぜと ともに さりぬ・・・ · 4 C: The windsock tried to warn him. / ふきながしは ちゃんと おしえて いた。 ·
5 K: That cloud was NOT a floor. / あの くもは ゆか じゃ ないよ! · 6 C: Even 1942 gave you three loops! / 1942でさえ
ループは 3かい あったぞ!

#### Knight: DRAGON QUESTLIKE (`venues_a.md` §2.10)

| Id | Trigger | EN | JP |
|---|---|---|---|
| KNT-01 | first encounter | K: A random encounter! In a Rockman game? C: It is not random. I checked. | K: ランダム エンカウント! ロックマンで!? C: ランダムでは ない。 しらべた。 |
| KNT-02 | RUN blocked | C: You cannot run from a tournament, Rockman. | C: たいかいからは にげられんぞ。 |
| KNT-03 | ceiling defeated | K: He beat the ceiling. Can you DO that? | K: てんじょうに かっちゃった。 そんなこと できるの? |
| KNT-04 | Metal Metslime escapes | C: They always get away. Always. | C: あいつらは かならず にげる。 かならず だ。 |
| KNT-05 | search finds the stairs | K: Stairs! Behind the throne! Just like the old days! | K: かいだん! ぎょくざの うしろに! むかしと おなじ! |
| KNT-06 | charged punch opens them | K: That is NOT how you find secret stairs! | K: かくしかいだんは そうやって さがす ものじゃ ない! |
| KNT-07 | shield broke | C: Shield down! Now we have a fight! | C: たてが こわれた! これで しょうぶに なる! |
| KNT-08 | first Y.SPEAR hit (weak) | K: Right through the shield! | K: たてを つらぬいた! |
| KNT-09 | the Knightlord's YES | C: Did he just take the deal?! K: Papa, he pressed YES. | C: とりひきに のったのか!? K: パパ、 はいを えらんだよ。 |
| KNT-10 † | KNIGHT.C clash (SC4) | C: Mace meets mace! | C: てつきゅう たい てつきゅう! |

Deaths: 1 King: DEATH SHOULD NOT HAVE TAKEN THEE, ROCK. I WILL GIVE THEE ANOTHER CHANCE. / おお ロックよ! しんでしまうとは
なにごとだ! (DQ1's own words, S15) · 2 C: Rockman was defeated. The judges are not pleased. / ロックマンは ちからつきた。
しんさいんは ごきげん ななめ。 · 3 K: He should have stayed at the inn. / やどやに とまれば よかったのに。 · 4 C: The ceiling
won that round. / この ラウンドは てんじょうの かち。 · 5 K: Thou art... out of HP. / HPが・・・ つきた。 · 6 K: That
chest had teeth! / あの たからばこ はが あった!

#### Tomahawk: GUN.SMOKE FRONTIER (`venues_a.md` §3.10)

| Id | Trigger | EN | JP |
|---|---|---|---|
| TMH-01 | reading the posters | C: Three bounties. Kalinka, my reading glasses. | C: しょうきんくびが 3にん。 カリンカ、 めがねを。 |
| TMH-02 | first civilian hit | K: Not the PIANIST! | K: ピアニストは だめ! |
| TMH-03 | quick-draw won | K: %T% seconds! (the timer, e.g. 0.19) | K: %T%びょう! |
| TMH-04 | FOUL | C: He jumped the gun! | C: フライングだ! |
| TMH-05 | tunnel hit | C: Mind your head, Rockman! | C: あたまに きを つけろ! |
| TMH-06 | Sidewinder escapes | K: He got away! | K: にげられた! |
| TMH-07 | the Sheriff opens the gate | C: Deputy Rockman! I always knew. | C: ほあんかん ロックマン! わかって いたとも。 |
| TMH-08 | the Balancer room (vanilla's) | C: The old pipe room! Still here after all these years. | C: むかしの パイプべや! まだ あったのか。 |
| TMH-09 | sky bypass taken | K: He's taking the high road! | K: そらの みちを いく つもりだ! |
| TMH-10 | first PLANT.B hit (weak) | K: Bless you! | K: おだいじに! |
| TMH-11 | Break Man's whistle during READY | C: Not the whistle! | C: くちぶえは だめだ! |
| TMH-12 † | SILVER.T caught (SC4) | K: He caught it! | K: キャッチした! |

Deaths: 1 C: Too slow on the draw. / ぬくのが おそかった。 · 2 K: The 4:50 doesn't stop for anyone. / 4じ50ぷんの きしゃは
だれも まって くれない。 · 3 C: That was a bad trade, partner. / わるい とりひき だったな。 · 4 K: The pianist is fine, by
the way. / ちなみに ピアニストは ぶじ です。 · 5 C: Boot Hill has room for one more. / ブートヒルには まだ あきが ある。 ·
6 K: Always check the outhouse first. / まず トイレを しらべる こと。

TMH-08 is for vanilla players: the Energy Balancer's pipe room is vanilla's own (`rm6/SUMMARY.md` §1.3).

#### Plant: JUNGLE PITFALL (`venues_a.md` §4.10)

| Id | Trigger | EN | JP |
|---|---|---|---|
| PLT-01 | stage start | K: Twenty minutes on the clock! C: ...It does nothing. That was the old rules. | K: のこり 20ぷん! C: ・・・なにも おきない。 むかしの ルールだ。 |
| PLT-02 | first vine | C: Hold on tight, Rockman! | C: しっかり つかまれ! |
| PLT-03 | croc death (a pair) | C: See you later, alligator! K: In a while, crocodile. | C: じゃあね ワニさん! K: またね ワニさん。 (the rhyme is EN-only; JP keeps the call and answer) |
| PLT-04 | first log hit | K: TIMBER! | K: たおれるぞー! |
| PLT-05 | treasure | K: Treasure! That's %N% of four! | K: おたから! これで %N%こめ! |
| PLT-06 | rhinestone | C: That's paste, Rockman. Harry never let a log touch him. | C: それは イミテーション だ。 ハリーは まるたに いちども ぶつからなかった。 |
| PLT-07 | first lightning | K: Eek! | K: きゃっ! |
| PLT-08 | the cat | K: Is that... Tango? From the Game Boy? | K: あれって・・・ タンゴ? ゲームボーイの? |
| PLT-09 | brick wall broken | C: Nine screens in three! The underground is faster! | C: 3がめんで 9がめんぶん! ちかの ほうが はやい! |
| PLT-10 | first B.ATTACK hit (weak) | K: He's wilting! | K: しおれてる! |
| PLT-11 | bloom (pinch) | C: Full bloom! Careful, Rockman! | C: まんかいだ! きを つけろ! |
| PLT-12 † | PLANT.B clash (SC4) | K: Both barriers popped! | K: バリアが どっちも はじけた! |

Deaths: 1 C: See you later, alligator! / ワニに たべられちゃった・・・ · 2 K: Stuck in the tar! / タールに はまった! · 3 C: He
let go too early. / てを はなすのが はやすぎた。 · 4 K: The jungle always wins the first round. / さいしょの ラウンドは
いつも ジャングルの かち。 · 5 C: Watch the eyes on those crocs! / ワニの めを よく みろ! · 6 K: That wasn't a floor,
Rockman. / あれは ゆか じゃ なかったよ。

PLT-01: *Pitfall!* gave Harry 20 minutes (Appendix A). PLT-08: Tango debuted in Rockman World 5 (Game Boy, 1994).

#### Blizzard: SUMMIT CLIMBER (`venues_b.md` §1.11)

| Id | EN | JP |
|---|---|---|
| BLZ-01 | K: Frozen Island! Blizzard Man runs on SOLAR ENERGY. C: ...On a glacier? | K: こおりの しま! ブリザードマンは ソーラーエネルギーで うごくの。 C: ・・・ひょうがの うえで? |
| BLZ-02 | C: Ice is slippery, Rockman. Science! | C: こおりは すべる。 かがく だ! |
| BLZ-03 | K: The ship is shaking the icicles loose! | K: ふねの ゆれで つららが おちてくる! |
| BLZ-04 | K: Sponsored by Mr. Y. C: It's Wily. K: It's definitely Wily. | K: スポンサーは Mr.Y。 C: ワイリーだ。 K: ぜったい ワイリー。 |
| BLZ-05 | C: Use your head! Literally! | C: あたまを つかえ! もじどおり! |
| BLZ-06 | K: Hey! It filled the hole back in! | K: ちょっと! あなを うめちゃった! |
| BLZ-07 | K: Don't hurt the seals! They're union workers! | K: アザラシを いじめないで! くみあいいん なんだから! |
| BLZ-08 | C: Is that... a polar bear in sunglasses? K: He looks cool. | C: あれは・・・ サングラスの シロクマか? K: かっこいい。 |
| BLZ-09 | K: He's skiing! Does he even have skis? | K: すべってる! スキー もってたっけ? |
| BLZ-10 | K: The condor! Jump for its feet! | K: コンドルだ! あしに とびついて! |
| BLZ-11 | C: Next stop: the clouds! Hold on, lad! | C: つぎは くもの うえだ! はなすなよ! |
| BLZ-12 | K: He's melting! C: That's what you get for skiing on solar power. | K: とけてる! C: ソーラーで スキーなんか するからだ。 |
| BLZ-13 | C: He built a snowman. Mid-match. The judges love it. | C: しあいちゅうに ゆきだるまを つくった。 しんさいんは だいよろこびだ。 |
| BLZ-14 | K: Is he... yodelling? C: AVALANCHE! | K: あれって・・・ ヨーデル? C: なだれだ! |
| BLZ-15 | K: You broke a seal! C: The union will hear about this. | K: アザラシを こわしちゃった! C: くみあいに ほうこく されるぞ。 |

Deaths: 1 K: Brr! Rockman's taking a cold nap. C: Up, lad! It's only minus forty! / ブルッ! ロックマン おひるね ちゅう。
おきろ! たったの マイナス40ど だ! · 2 C: In my country we call this weather "spring". / わたしの くにでは これを 「はる」
と いう。 · 3 K: The seals are clapping. I think that's bad. / アザラシが はくしゅ してる。 よくない かんじ。 · 4 C: The
mountain always wins the first round. / やまは いつも さいしょの ラウンドを とる。 · 5 K: Note to self: helmets are for
bonking, not landing. / メモ: ヘルメットは ずつき よう。 ちゃくち ようじゃ ない。 · 6 † C: Popo and Nana made it look so
easy. / ポポと ナナは かんたん そうに やっていた ものだ。

(The one "in my country" joke of this venue is death line 2, §1.2 rule 3. Popo and Nana are the Ice Climbers.)

#### Flame: PERSIAN PALACE (`venues_b.md` §2.11)

| Id | EN | JP |
|---|---|---|
| FLM-01 † | K: The Palace on the Oil Field! C: Built on an oil field. What could go wrong? | K: ゆでんの きゅうでん! C: ゆでんの うえに たてた。 なにが おきても ふしぎ では ない。 |
| FLM-02 | K: Shoot it before it drops! / C: The oil's lit. And it stays lit. Remember that. | K: おとす まえに うって! / C: あぶらに ひが ついた。 ずっと もえる。 おぼえて おけ。 |
| FLM-03 | K: A pressure plate! Just like the old computer games! | K: スイッチの ゆか! むかしの パソコンゲーム みたい! |
| FLM-04 | C: That's the "loose" in "loose floor". | C: だから 「くずれる ゆか」 と いうのだ。 |
| FLM-05 | K: Slide! Tiptoe! Do something! | K: スライディング! ぬきあし! なんとか して! |
| FLM-06 | C: His guard's up. Hit him while he swings. | C: かまえて いる。 ふりかぶった ところを ねらえ。 |
| FLM-07 | K: You set the gallery on fire! C: Effective. Expensive. | K: ギャラリーが もえてる! C: こうかてき。 そして たかくつく。 |
| FLM-08 | K: Who's on the balcony? C: A vizier with Wily's moustache. K: It's Mr. Y. C: It's *Wily*. | K: バルコニーに だれか いる? C: ワイリーの ひげの だいじん だ。 K: Mr.Y だよ。 C: *ワイリー* だ。 |
| FLM-09 | K: There's another Rockman! C: He copies everything you do. *Everything.* | K: ロックマンが もうひとり! C: すべて まねを する。 *すべて* だ。 |
| FLM-10 | K: They... merged? C: Sometimes the best fight is no fight at all. | K: ・・・ひとつに なった? C: たたかわない ことが いちばんの しょうぶ という ことも ある。 |
| FLM-11 | C: You beat yourself. Philosophically troubling. | C: じぶんに かった。 てつがくてきに なやましい。 |
| FLM-12 | K: A mouse! It's pressing the plate! Good mouse! | K: ネズミ! スイッチを ふんでる! いいこ! |
| FLM-13 | C: The fire marshal approves. A rare event in this palace. / K: He's tutting at you. | C: しょうぼうかんも にっこり。 この きゅうでんでは めずらしい。 / K: しょうぼうかんが したうち してる。 |
| FLM-14 | K: His flame went out! C: He's looking for a match. | K: ひが きえた! C: マッチを さがして いる。 |
| FLM-15 | C: You *fed* him? | C: *えさを* やったのか? |
| FLM-16 | K: The whole floor's on fire! | K: ゆかが ぜんぶ もえてる! |

FLM-01 drops the draft's "Oil Sultanate" (§1.2 rule 3: the joke is the oil field, not a culture). FLM-03: *Prince of
Persia* began on the Apple II (1989).

Deaths: 1 K: Sliced! C: The palace has a strict no-running policy. / きられた! きゅうでんは はしり きんし だ。 · 2 C: Oil and
fire. Who could have predicted this? / あぶらと ひ。 だれが よそう できた ことか。 · 3 K: The floor fell! C: Read the
brochure, lad: *loose* floors. / ゆかが おちた! パンフレットを よめ。 *くずれる* ゆか だ。 · 4 C: The hourglass doesn't
stop for retries. / すなどけいは リトライでも とまらない。 · 5 K: The vizier is laughing. C: Wily always laughs. / だいじんが
わらってる。 ワイリーは いつも わらう。 · 6 † K: The old game gave you sixty minutes. This one gives you lives. /
むかしの ゲームは 60ぷん。 この ゲームは ざんき。

#### Centaur: ATLANTIS RUINS (`venues_b.md` §3.11)

| Id | EN | JP |
|---|---|---|
| CEN-01 | K: Centaur Man! Specialty: ABILITY UNKNOWN. C: Even the judges don't know. | K: ケンタウロスマン! とくぎ: ふめい。 C: しんさいんにも わからない。 |
| CEN-02 † | K: ZONE 1? How many zones are there? C: In Atlantis? Over a hundred. | K: ゾーン1? ぜんぶで いくつ? C: アトランティス なら 100いじょう だ。 |
| CEN-03 | C: Doors in Atlantis go where they like, Rockman. | C: アトランティスの とびらは すきな ところへ つながる。 |
| CEN-04 | K: "A cracked door lies." Helpful! | K: 「ひびの はいった とびらは うそを つく」。 たすかる! |
| CEN-05 | K: Back to ZONE %N%?! That's so mean! | K: ゾーン%N%に もどされた!? ひどい! |
| CEN-06 | K: It's a *painting*! | K: *え* だった! |
| CEN-07 | K: I can't see a thing! C: Then look for what shines. | K: なにも みえない! C: ひかる ものを さがせ。 |
| CEN-08 | K: The statue said thank you! | K: せきぞうが ありがとう って! |
| CEN-09 | K: He's... an eggplant. C: A very determined eggplant. | K: ナスに・・・ なっちゃった。 C: とても けつい の かたい ナス だ。 |
| CEN-10 | C: A hot spring! Even robots need a soak. | C: おんせんだ! ロボットだって つかりたい。 |
| CEN-11 | K: He saw you! RUN! | K: みつかった! にげて! |
| CEN-12 | C: High tide! You'll jump like a fish. | C: まんちょうだ! さかなの ように とべるぞ。 |
| CEN-13 | K: ZONE 100? That's the whole game! | K: ゾーン100!? ぜんクリア じゃん! |
| CEN-14 | K: Is that Medusa? C: A jester with snakes. Budget cuts. | K: あれ メデューサ? C: ヘビを つけた ピエロ だ。 よさん さくげん。 |
| CEN-15 | C: Wings! Well, a dog. Close enough. | C: つばさだ! まあ いぬ だが。 にたような ものだ。 |
| CEN-16 † | K: Beat's T-parts! | K: ビートの Tパーツ! |
| CEN-17 | K: His legs buckled! | K: あしが くずれた! |
| CEN-18 | C: He's posing for the photo! Say cheese! | C: ポーズを とってる! はい チーズ! |
| CEN-19 | K: So *that's* his ability! C: It's... gambling? | K: *それが* のうりょく!? C: ・・・ギャンブル? |
| CEN-20 | K: C... F-L-R-S-H? C: The engraver was paid by the letter. | K: C・・・ F・L・R・S・H? C: ちょうこくしは もじ たんかで はらわれて いた。 |

CEN-02 † says "over a hundred": *Atlantis no Nazo* has 101 zones counting its secret final zone (Appendix A). CEN-16
† leaves the "I built that bird" line to the first plate of the save (§6.2).

Deaths: 1 K: Wrong door! C: In Atlantis, every door is the wrong door. / とびら まちがえた! アトランティスでは どの とびらも
まちがい だ。 · 2 C: Centaur Man runs on a DRY battery. Rockman, evidently, does not. / ケンタウロスマンは かんでんち。
ロックマンは ちがう らしい。 · 3 K: Time and tide wait for no robot. / さいげつ ロボットを またず。 · 4 C: Only ninety-nine
zones to go. / のこり たったの 99ゾーン。 · 5 K: A vegetable has fallen. (after an eggplant death) / やさいが たおれた。 ·
6 † K: Even Pit fell down a lot. / ピットも よく おちてたよ。

#### Yamato: EDO NINJA ROW (`venues_b.md` §4.12)

| Id | EN | JP |
|---|---|---|
| YAM-01 | K: Yamato Man! DEFENCE 185! C: And MOBILE 31. He isn't going anywhere. | K: ヤマトマン! DEFENCE 185! C: そして MOBILE 31。 どこにも いかない。 |
| YAM-02 | K: "Mr. Y. Wanted. A million ryo." C: Cheap. Wily's worth at least two. | K: 「Mr.Y 100まんりょう」 C: やすい。 ワイリーなら 200まんは する。 |
| YAM-03 | C: Knock them from below! Ninja manners. | C: したから つきあげろ! にんじゃの さほう だ。 |
| YAM-04 | K: That ninja stole a travel pass! | K: あの にんじゃ てがたを ぬすんだ! |
| YAM-05 | K: PASS %N% of 3! The sekisho wants three. / (3 of 3) The back road's open! | K: てがた %N%まいめ! せきしょには 3まい いるよ。 / うらみち かいほう! |
| YAM-06 | K: Shh! The floor sings when you walk! C: Slide, lad. Quietly. | K: しーっ! あるくと ゆかが なく! C: スライディングで しずかに。 |
| YAM-07 | C: Edo architecture: beautiful and lethal. | C: えどの けんちく。 うつくしく そして きけん。 |
| YAM-08 | K: The wall turned around! | K: かべが まわった! |
| YAM-09 | K: It's just a scroll. | K: ただの かけじく だね。 |
| YAM-10 | K: Daruma otoshi! Knock out the blocks, and never hit the head! | K: だるまおとし! ブロックを ぬいて。 あたまは たたいちゃ だめ! |
| YAM-11 | C: You hit the head. The daruma is NOT amused. | C: あたまを たたいたな。 だるまは ごりっぷく だ。 |
| YAM-12 | K: It painted in its other eye! Wish granted! | K: もう かたほうの めを いれた! ねがいが かなった! |
| YAM-13 | K: A pogo stick... with a spear on it? C: In my day we called that a Sakugarne. | K: ホッピング・・・ やりつき? C: むかしは それを サクガーンと よんだ ものだ。 |
| YAM-14 | C: Three passes. The back road is yours. | C: てがた 3まい。 うらみちは きみの ものだ。 |
| YAM-15 | K: Who turned off the lights?! / (first firework) K: Tamaya~! | K: でんき けしたの だれ!? / K: たまや~! |
| YAM-16 | K: He chopped the spear in half! | K: やりを まっぷたつ! |
| YAM-17 | C: A samurai never drops his spear. He throws yours back. | C: さむらいは やりを おとさない。 きみの やりを なげかえす。 |
| YAM-18 | K: His helmet flew off! C: His MOBILE just went from 31 to 99! | K: かぶとが とんだ! C: MOBILE が 31から 99に! |
| YAM-19 | (audience) YAMATO-YA! | (かんきゃく) やまとや! |
| YAM-20 | K: Beat's E-parts! On a golden fish! | K: ビートの Eパーツ! しゃちほこの うえに! |

YAM-13: the Sakugarne is Quint's pogo from Rockman World 2 (Game Boy, 1991). Panel labels (DEFENCE, MOBILE) stay in
Latin letters in JP, as on the card.

Deaths: 1 K: Shuriken! Duck! C: He did not duck. / しゅりけん! ふせて! ふせなかった。 · 2 C: The floors sang at your
funeral, Rockman. / ゆかが とむらいの うたを うたって いる。 · 3 K: The ceiling came down! C: Beautiful *and* lethal. /
てんじょうが おちてきた! うつくしく *そして* きけん。 · 4 C: DEFENCE 185, MOBILE 31, and still faster than you. / DEFENCE
185、 MOBILE 31。 それでも きみより はやい。 · 5 K: Fall seven times, stand up eight! / ななころび やおき! · 6 † K: Ninja rule
one: don't be seen. Rule two: don't be hit. / にんじゃの おきて その1: みつかるな。 その2: あたるな。

### 6.4 Death lines outside the venues, and the generic table

**Opening** (3, then generic): 1 K: Don't worry! Nobody's judging the Opening. C: ...We are, actually. / しんぱい ないよ!
かいかいしきは しんさ しないから。 C: ・・・じつは してる。 · 2 K: Practice makes perfect! / れんしゅう あるのみ! · 3 C:
The mascot thanks you for your participation. / マスコットより ごさんか ありがとう。

**Semifinal** (6): 1 K: The Bass fan club is cheering. Boo! / フォルテの ファンクラブが もりあがってる。 ブー! · 2 C: The Joes
are doing the wave. / ジョーたちが ウェーブを している。 · 3 K: That doesn't count! Right, Papa? C: It counts. /
ノーカン だよね パパ? C: カウント する。 · 4 C: Bass's file on you is getting very thick. / フォルテの きみの ファイルが
ぶあつく なって いく。 · 5 K: Mr. Y is selling replays of that. / Mr.Y が いまの リプレイを うってる。 · 6 C: Up, lad. It's the
Semifinal. / おきろ。 じゅんけっしょう だぞ。

**Exhibitions** (2 per guest): Block Man: K: Wait, you still have lives! / C: Too many gaps. — まって、 まだ ざんきが
ある! / すきまが おおすぎる。 · Paddle Man: K: He returned YOU. / C: Same ball, different robot. — ロックマンを うちかえした!
/ おなじ ボール、 ちがう ロボット。 · Invader Man: K: They reached the bottom! / C: Your grandfather would be
disappointed. — したまで きちゃった! / おじいちゃんが がっかり するぞ。 · Maze Man: K: Caught by a Met-ghost! / C: Should have
eaten a pellet. — メットおばけに つかまった! / えさを たべて おけば よかった。

**Generic**, by cause (preferred when the cause matches):

| Cause | EN | JP |
|---|---|---|
| pit | K: Mind the gap! | K: すきまに ちゅうい! |
| pit | C: That pit had no bottom. Most don't. | C: そこなしの あなだ。 たいてい そうだ。 |
| pit (Beat not complete) | K: Where's Beat when you need him? | K: こんな とき ビートが いれば! |
| pit | C: Gravity: still undefeated. | C: じゅうりょく いまだ むはい。 |
| spike | K: Spikes! The classic! | K: トゲ! おやくそく! |
| spike | C: One touch. Always one touch. | C: さわれば おわり。 いつも だ。 |
| spike (SPIKE GUARD not owned) | K: There's a chip for that, you know. | K: それよけの チップも あるよ。 |
| spike | C: Spikes. Undefeated since 1987. | C: トゲは 1987ねんから むはい。 |
| boss room | K: So close! Look at his health bar! | K: おしい! たいりょく ゲージを みて! |
| boss room | C: Try his weakness. The flashing tells you. | C: じゃくてんを ためせ。 てんめつが おしえて くれる。 |
| boss room | C: The champion is breathing hard too. | C: チャンピオンも いきが あがって いるぞ。 |

**Generic**, any cause (rotating, 12):

| # | EN | JP |
|---|---|---|
| 1 | K: Ooh! That's going to cost DAMAGE points. | K: いたっ! ダメージてんが へっちゃう。 |
| 2 | C: Down goes Rockman! The crowd gasps. | C: ロックマン ダウン! かんきゃくが いきを のむ。 |
| 3 | K: Shake it off! You've got this! | K: きにしない! いけるよ! |
| 4 | C: The judges have noted it. In large letters. | C: しんさいんが メモ した。 おおきな じで。 |
| 5 | K: Replay! ...No. Let's not show the replay. | K: リプレイ! ・・・は やめとこう。 |
| 6 | C: Every champion falls. The good ones get up. | C: チャンピオンも たおれる。 いい チャンピオンは たちあがる。 |
| 7 | K: Tiun tiun tiun... | K: ティウン ティウン ティウン・・・ |
| 8 | C: A setback. Statistically, a temporary one. | C: つまずいた。 とうけいてきには いちじてき。 |
| 9 | K: Papa, is that allowed? C: Falling over? Sadly, yes. | K: パパ、 あれ いいの? C: たおれる ことか? ざんねんながら いい。 |
| 10 | C: Rockman returns to the start line. With dignity. | C: ロックマン スタートラインへ。 ほこりたかく。 |
| 11 | K: Mr. Y just bought a T-shirt that says "I saw that". (until S33; after: "Wily just bought...") | K: Mr.Y が 「みたぞ」 って Tシャツ かってる。 |
| 12 | C: In my day we had three lives and no continues. | C: むかしは ざんき 3で コンティニュー なし だった。 |

Line 7 is the death sound's own name: Japanese players call it "tiun tiun" (ティウンティウン), and 4MI heads its death
counter TIWNS (`r4mi/text.md` §0).

### 6.5 Mr. Y's heckles between lives (the CX Light 6 table)

CX's Dr. Light speaks once per respawn in the final fortress, from a 12-line table that includes a Yes/No where YES
kills you (`cx/SUMMARY.md` §2 item 20). GP gives the table to Mr. Y, for every respawn in **H1-H5** (meta 14-18),
then to Wily for **W1-W3** (meta 19-21). It replaces the venue death line in those stages (`EV_RESPAWN_HECKLE`, P1).

The index is the fortress KO count of the file (the sum of STAGEREC KOs for meta 14-21), so the lines keep advancing
across stages and sessions; after the last line, the table loops from line 6 (the early lines are introductions).
Choices use the T2 menu; the respawn waits for the answer.

**H1-H5: Mr. Y** (polite わたくし … ございます; the slips are marked ‡)

| # | EN | JP |
|---|---|---|
| 1 | Ho ho ho! Welcome to my— to *a* museum! | ホッホッホ! わたくしの・・・ いえ *ある* はくぶつかんへ ようこそ! |
| 2 | Did you know? Exhibits are not to be touched. Or to touch you. | ごぞんじ ですか? てんじひんに さわっては なりません。 さわられても なりません。 |
| 3 | In 1987 you couldn't even slide. You've come so far. Downwards. | 1987ねんには スライディングも できなかった あなた。 ずいぶん おちぶれ・・・ いえ すすまれ ましたね。 したに。 |
| 4 | Let's make a deal. You stop dying, I stop laughing. Deal? ▶YES NO — YES: ...I lied! Wahaha— ho ho ho! ‡ / NO: Suit yourself! Ho ho ho! | とりひき しましょう。 あなたは しなない。 わたくしは わらわない。 いかが? ▶はい いいえ — はい: ・・・うそで ございます! ワハハ・・・ いえ ホッホッホ! ‡ / いいえ: おすきに どうぞ! ホッホッホ! |
| 5 | Mr. Y's respawn insurance! Only 1 bolt! ▶YES NO — YES (−1 bolt): Thank you! Your policy does not cover dying. / NO: Uninsured! How brave! | Mr.Y の ふっかつ ほけん! たったの 1ボルト! ▶はい いいえ — はい: まいど! なお しぼうは ほしょうの たいしょうがい で ございます。 / いいえ: むほけん! ゆうかん ですこと! |
| 6 | That Wily fellow everyone talks about? Never met him. Handsome, I hear. | みなさまが うわさの ワイリーという かた? ぞんじあげません。 ハンサム だそうで ございますね。 |
| 7 | Every time you fall, my cameras record it. For science. And the highlight reel. | あなたが たおれる たびに カメラが きろく いたします。 かがくの ため。 そして ハイライトの ため。 |
| 8 | Bass never dies this much. Bass is perfect. In beta, but perfect. | フォルテは こんなに しにません。 フォルテは かんぺき。 ベータばん ですが かんぺき。 |
| 9 | (booth offered, not taken) Have you considered Y-TURBO? Have you considered it NOW? / (DOPED) How is your Y-TURBO? Read the warranty yet? | Y-ターボは いかが? *いまなら* いかが? / Y-ターボの ぐあいは いかが? ほしょうしょは もう およみに なりました? |
| 10 | Light's robot, falling over in a museum. I would put THAT in a wing. | ライトの ロボットが はくぶつかんで ころんで いる。 それこそ てんじ したい もので ございます。 |
| 11 | ‡ In my day— in *Mr. Y's* day— robots stayed down! | ‡ わしの わかい ころは・・・ いえ *わたくしの* わかい ころは、 ロボットは おきあがらなかった ものじゃ! |
| 12 | Have you heard of sixteen bits? You will. | 16ビットを ごぞんじ? いずれ ごぞんじに なりますよ。 |
| 13 | Kalinka, dear, would you tell Rockman he is doing badly? K: He's doing GREAT! | カリンカさま、 ロックマンに へた だと おつたえ ください。 K: すっごく じょうず だよ! |
| 14 | The gift shop sells your helmet now. Half price. | おみやげやで あなたの ヘルメットを うって おります。 はんがく で。 |
| 15 | ‡ Wahahaha— AHEM. Ho. Ho. Ho. | ‡ ワーッハッハッハ・・・ ゴホン。 ホッ。 ホッ。 ホッ。 |
| 16 | Again? I am running out of things to say. ...No, I'm not. Ho ho ho! | また? いうことが なくなって まいりました。 ・・・うそ です。 ホッホッホ! |

Line 5 is the CX "Yes that hurts", at the size of one bolt [new-code] S Could (a bolt deduction from a choice).
Line 7 foreshadows S33 (the cameras are the plan). In JP, Kalinka notices the first ‡ slip in her next POP: 「いま
'わし' って いった!」.

**W1-W3: Dr. Wily** (after the unmasking; わし … じゃ)

| # | EN | JP |
|---|---|---|
| 1 | WAHAHAHA! No more disguises! No more "ho ho ho"! | ワーッハッハッハ! もう へんそうも 「ホッホッホ」も いらんわ! |
| 2 | Fall all you like! Every fall is more data for Project SUPER! | いくらでも おちるが よい! おちる たびに プロジェクト・スーパーの データが ふえるのじゃ! |
| 3 | Light! Are you watching? Your boy is lying down! | ライト! みておるか? おまえの ロボットが ねころんで おるぞ! |
| 4 | (DOPED) Did you think my own chip would work against ME? / (else) In sixteen bits, that pit would have had a bottom. Probably. | わしの チップが わしに きくと おもったか? / 16ビットなら あの あなにも そこが あった かも しれんぞ。 |
| 5 | Bass! Write this down! "Rockman: falls over." | フォルテ! メモ しておけ! 「ロックマン: ころぶ」! |
| 6 | I've been beaten five times, and look at me now! ...Six. Six times. K: Ten, with the Game Boy ones. | わしは 5かいも まけた。 だが みよ この とおり! ・・・6かい。 6かい だった。 K: ゲームボーイの ぶんも いれたら 10かい だよ。 |
| 7 | Shall I lower the difficulty? NO! WAHAHA! | なんいどを さげて やろうか? いやじゃ! ワハハ! |
| 8 | (W1, third tier) Every channel of this music is MINE! Listen to it laugh at you! | この おんがくの チャンネルは ぜんぶ わしの ものじゃ! おまえを わらって おるわ! |
| 9 | Mr. Y says hello. ...I'm Mr. Y. I say hello. | Mr.Y が よろしく と。 ・・・わしが Mr.Y じゃ。 よろしく。 |
| 10 | Give up, and you'll be the first robot I upgrade! Free! ▶YES NO — YES: ...Really? I hadn't planned for that. Er. Carry on! / NO: Fool! | あきらめれば いちばんに アップグレード してやるぞ! むりょうで! ▶はい いいえ — はい: ・・・ほんとうに? そこまで かんがえて なかった。 ええい つづけろ! / いいえ: ばかめ! |
| 11 | (partner) Your brother isn't coming, you know. (a whistle, offscreen) ...Is that a whistle? / (walked) Your brother isn't coming. You saw to that. | おまえの あにきは こんぞ。 (くちぶえ) ・・・いまのは くちぶえか? / あにきは こんぞ。 おまえの せいでな。 |
| 12 | WAHAHAHA... *cough* ...HAHA. | ワーッハッハッハ・・・ ゴホゴホ・・・ ハッハ。 |

Line 6 is true to the series: by the end of 1993 Wily had lost in Rockman 1 through 6 on the Famicom and in Rockman
World 1 through 4 on the Game Boy (Appendix A, A-6.6). Line 4's DOPED variant is a **proposal for `systems.md`**: Y-TURBO does nothing in Super Wily
Castle (Wily left a back door in his own chip). Its help page hints at it (§8, "SEE WARRANTY").

### 6.6 Difficulty and mode variants

| Setting | What changes in the text |
|---|---|
| CASUAL | Death lines unchanged (they never mock). The first death of a file adds K: "Papa, CASUAL means they're having fun, right?" C: "That is the whole point." / パパ、 カジュアルって たのしむ ことだよね? C: それが いちばん だいじ だ。 |
| HARD | The first READY of a HARD file: K: "HARD mode! Papa, should I cover my eyes?" C: "Watch. This is how legends start." / ハード モード! パパ、 めを ふさいだ ほうが いい? C: みて いなさい。 でんせつは こうして はじまる。 Game-over line 7 is added: K: "On HARD, that counts as warming up." / ハードなら いまのは じゅんびうんどう。 |
| 1993 | No shop, no bolts, no chips (`systems.md` §13.3): Eddie's closed line (S10), no booth (so no S21, no walked variant), no envelope or chip lines. The commentators stay: they are flavour, not rules |
| ANNOUNCER = DEATHS ONLY / OFF | §6.1 |
| Time Attack | No POP lines at all; scenes are skipped |
| GP Rush | P1 only; the lobby scoreboard and ELIMINATED / CHAMPION screens are `meta.md`'s (their words: §9 for ENGRISH) |
| BASS file (Could) | S51; "Rockman" in generic lines becomes "Bass" through the `%PLAYER%` variable (width 7) |

---

## 7. The judges' debrief: one hint per venue secret

`meta.md` §4 owns the engine (4MI's predicate table, per stage: the first missed secret, by weight, picks the line;
tier A riddle on the first two misses, tier B instruction from the third). This section is the final text of every
entry, EN and JP, spoken by **Kalinka** (`meta.md` §4.1; confirmed here: she is the one who "hears things"). Rules:

- **Tier B is the venue owner's own line, word for word** (`meta.md` §4.3). Changes here are only to fit 4 lines of 28.
- **Tier A rewards knowing the homage game, and every fact in it is true** (Appendix A). Four of `meta.md`'s v0 riddles
  made claims that were wrong or unverifiable; they are rewritten and marked †.
- Each entry is ≤ 4 lines × 28 cells (§10.2). EN is upper-cased at build; JP is kana.
- A riddle may be oblique. It may not point at the wrong place.

### 7.1 Venue hints

**Blizzard: SUMMIT CLIMBER** (*Ice Climber*)

| Id | Secret | Tier A | Tier B (`venues_b.md` §1.12) |
|---|---|---|---|
| BL0 | exit: the condor | EN: The condor never waits for slow climbers. Race the bonus clock to the top. / JP: コンドルは おそい クライマーを まって くれない。 ボーナスの とけいと きょうそう して うえまで。 | EN: The summit condor only carries climbers who reach it with time on the clock. Jump for its feet. / JP: ちょうじょうの コンドルは じかんが のこって いる クライマーだけを はこぶ。 あしに とびつけ。 |
| BL1 | room: the no-wrap floor | EN: The seals know every floor of that mountain. One of them never comes back. / JP: アザラシは やまの ゆかを ぜんぶ しっている。 もどって こない ゆかが ひとつ ある。 | EN: On the mountain, one floor doesn't wrap around. Watch where the seals walk. / JP: やまの ゆかで ひとつだけ はしが つながって いない。 アザラシの いく さきを みて。 |
| BL2 | item: SNOW CHAINS | EN: The seals are union workers. The union remembers who was nice to them. / JP: アザラシは くみあいいん。 くみあいは やさしく された ことを わすれない。 | EN: The seals are only doing their job. A climber who never breaks one earns a set of chains. / JP: アザラシは しごとを してる だけ。 ひとつも こわさなかった クライマーには チェーンが もらえる。 |

**Wind: SKY ACE 1943** (*1942*, *1943*)

| Id | Secret | Tier A | Tier B (`venues_a.md` §1.5-1.6) |
|---|---|---|---|
| WI0 † | exit: the ace's elevator | EN: In 1943, wiping out a red squadron left a POW. An ace leaves none of them flying. / JP: 1943では あかい へんたいを ぜんめつ させると POWが でた。 エースは 1きも にがさない。 | EN: Four red squadrons, four lamps. The elevator only takes aces. / JP: あかい へんたいが 4つ、 ランプも 4つ。 エレベーターは エースしか のせない。 |
| WI1 | room: WEATHER BALLOON | EN: Seagulls never stand on nothing. Ask one where it's standing. / JP: カモメは なにも ない ところには とまらない。 どこに とまって いるか みて。 | EN: A seagull was standing on a cloud. Clouds aren't floors... are they? / JP: カモメが くもの うえに たって いた。 くもは ゆか じゃ ない・・・ よね? |
| WI2 | item: YASHICHI | EN: Capcom's oldest secret is a pinwheel. It hides in something you shoot. / JP: カプコンで いちばん ふるい ひみつは かざぐるま。 うつ ものの なかに かくれて いる。 | EN: Shoot the POW. Then keep shooting it. / JP: POWを うって。 そして うちつづけて。 |

WI0 †: `meta.md` v0 said the red planes "came in fives", which this doc could not confirm for *1943*; the rewrite states
only the POW rule. WI2: the Yashichi has appeared in Capcom games since *Vulgus* (1984), Capcom's first arcade game; in
*1943*, shooting a POW cycles its item, and the pinwheel is one of them (Appendix A).

**Plant: JUNGLE PITFALL** (*Pitfall!*, *Pitfall II*)

| Id | Secret | Tier A | Tier B (`venues_a.md` §4.4-4.8) |
|---|---|---|---|
| PL0 † | exit: follow the cat | EN: In Pitfall II, Harry had to find Quickclaw. This cat is trying to find you. / JP: ピットフォールIIで ハリーは クイッククローを さがした。 この ねこは きみを さがして いる。 | EN: The cat knew a way down. Next time, follow it. / JP: ねこは したへの みちを しっていた。 こんどは ついて いって。 |
| PL1 | room: TREETOP HUT | EN: The storm shows more than rain. Watch the trees when the sky lights up. / JP: あらしが みせるのは あめ だけ じゃない。 そらが ひかったら きを みて。 | EN: When the lightning struck, a ladder appeared in the trees. / JP: いなずまが ひかった とき、 きの うえに はしごが みえた。 |
| PL2 | item: AUTO RECOVER | EN: Harry's perfect score never let a log touch him. Not one. / JP: ハリーの パーフェクトは まるたに いちども ぶつからない こと。 1かいも。 | EN: Four treasures, zero logs. The diamond is shy. / JP: たからは 4つ、 まるたは 0。 ダイヤは はずかしがりや。 |

PL0 †: the v0 riddle called Quickclaw Harry's cat; sources disagree on what Quickclaw is (a cat or a mountain lion), so
the riddle names him instead.

**Flame: PERSIAN PALACE** (*Prince of Persia*)

| Id | Secret | Tier A | Tier B (`venues_b.md` §2.12) |
|---|---|---|---|
| FL0 | exit: the shadow | EN: The prince never beat his shadow. He did something smarter with it. / JP: おうじは かげに かたなかった。 もっと かしこい ことを した。 | EN: Your shadow only fights if you fight. Hold your fire and walk into it. / JP: かげは きみが たたかう ときだけ たたかう。 うつのを やめて かげに あるいて いけ。 |
| FL1 | room: the mouse | EN: In 1989 a mouse saved the prince. Mice still live in that palace. / JP: 1989ねん ネズミが おうじを すくった。 その きゅうでんには いまも ネズミが すんで いる。 | EN: Something small lives behind a gate in the fire vault. Stand still and listen. / JP: ほのおの ちかしつの もんの おくに ちいさな なにかが いる。 じっと して みみを すませて。 |
| FL2 | item: FIREPROOF | EN: The fire marshal hates bonfires. He counts every pool you light. / JP: しょうぼうかんは たきびが きらい。 きみが つけた ひを ぜんぶ かぞえて いる。 | EN: The palace fire marshal rewards entrants who leave the oil unlit. Shoot the fire-droppers first. / JP: しょうぼうかんは あぶらに ひを つけなかった せんしゅを ほめる。 ひを おとす てきを さきに うて。 |

**Yamato: EDO NINJA ROW** (*Ninja Jajamaru-kun*, *Ganbare Goemon!*, *DuckTales*)

| Id | Secret | Tier A | Tier B (`venues_b.md` §4.13) |
|---|---|---|---|
| YA0 | exit: the sekisho back road | EN: No traveller passes the sekisho without papers. Goemon knew that. / JP: てがた なしでは せきしょは とおれない。 ゴエモンも そうだった。 | EN: The sekisho opens its back road for travellers with three passes. One runs, one hides behind a scroll, one sits under a daruma. / JP: せきしょの うらみちは てがた 3まいで ひらく。 1まいは にげる、 1まいは かけじくの うら、 1まいは だるまの した。 |
| YA1 † | room: the gold crest | EN: Scrooge's cane found treasure where others saw only floor. / JP: スクルージの ステッキは ただの ゆかに たからを みつけた。 | EN: Edo's gold is under the floor. Bounce your pogo on the crest in the caltrop hall. / JP: えどの こばんは ゆかの した。 まきびしの ひろまの もんしょうで ホッピング して。 |
| YA2 | item: DARUMA | EN: Daruma otoshi: knock out the blocks, not the head. Keep his face on. / JP: だるまおとし。 たたくのは ブロック。 あたまは だめ。 かおを おとさないで。 | EN: Daruma otoshi: knock out every block, never touch the head, and the daruma will paint its other eye. / JP: だるまおとし。 ブロックを ぜんぶ ぬいて あたまに さわらなければ、 だるまが もう かたほうの めを いれる。 |
| YA3 | plate E (JET) | EN: Beat's E-part is on the castle roof, where only flying ninjas go. / JP: ビートの Eパーツは おしろの やね。 とべる にんじゃ しか いけない。 | EN: Beat's E-plate shines on the castle roof. The ladder over the courtyard ledge needs a Jet. / JP: ビートの Eプレートは おしろの やねで ひかって いる。 なかにわの はしごには ジェットが いる。 |

YA1 †: the v0 riddle said DuckTales floors "open if you bounce on them", which is not a DuckTales rule; the rewrite
keeps only what is true (the cane-pogo finds hidden treasure). YA0: in *Ganbare Goemon! Karakuri Dōchū* (1986) a stage
is cleared by collecting three travel passes (通行手形) to get through the checkpoint.

**Tomahawk: GUN.SMOKE FRONTIER** (*Gun.Smoke*, *Wild Gunman*)

| Id | Secret | Tier A | Tier B (`venues_a.md` §3.7) |
|---|---|---|---|
| TO0 | exit: the back way (+ plate B) | EN: Three faces on the wanted posters. The Sheriff knows who collects. / JP: てはいしょに 3つの かお。 だれが しょうきんを うけとるか シェリフは しっている。 | EN: The Sheriff only opens the back way for a deputy with three bounties. / JP: シェリフは しょうきんくびを 3にん とらえた ほあんかんにだけ うらみちを ひらく。 |
| TO1 | room: THE OUTHOUSE | EN: "Occupied," says the sign. It has said so all day. Knock louder. / JP: 「しようちゅう」 と ふだに ある。 あさから ずっと。 もっと つよく ノックして。 | EN: Something in town was rattling. In Gun.Smoke you shoot what looks odd. / JP: まちで なにかが ガタガタ いって いた。 ガンスモークでは あやしい ものは うつ。 |
| TO2 | item: SHERIFF STAR | EN: Please do not shoot the pianist. Or anyone else who isn't wanted. / JP: ピアニストを うたないで ください。 てはい されて いない ひとも ぜんいん。 | EN: The Sheriff saw you shoot at townsfolk. Read the sign by the piano. / JP: シェリフは きみが まちの ひとを うつのを みた。 ピアノの そばの はりがみを よんで。 |

**Knight: DRAGON QUESTLIKE** (*Dragon Quest*)

| Id | Secret | Tier A | Tier B (`venues_a.md` §2.5-2.7) |
|---|---|---|---|
| KN0 | exit: the stairs behind the empty throne (+ plate A) | EN: In 1986 the real lord waited below his own empty throne. Old habits... / JP: 1986ねん ほんとうの まおうは からっぽの ぎょくざの したで まって いた。 むかしの くせは・・・ | EN: The Knightlord's throne is empty. Why? Search where no one sits. / JP: ナイトロードの ぎょくざは からっぽ。 なぜ? だれも すわって いない ところを しらべよ。 |
| KN1 | room: LIGHT'S TABLET | EN: Erdrick left a tablet for his heir. Someone else left one here. / JP: ロトは しそんに せきばんを のこした。 ここにも だれかが のこして いる。 | EN: Something glittered on the floor of the hall. Thou didst not search. / JP: ひろまの ゆかで なにかが ひかって いた。 なんじは しらべなかった。 |
| KN2 † | item: KAISHIN | EN: Metal ones are worth a fortune in EXP. They know it. They won't wait around. / JP: メタルは けいけんちの かたまり。 じぶんでも しっている。 まっては くれない。 | EN: Metal ones flee fast. Hit them often, not hard. / JP: メタルは すぐ にげる。 つよく より なんども たたけ。 |

KN2 †: the v0 riddle said a metal one is "worth 1000 EXP", which is not true of Dragon Quest's first Metal Slime; the
rewrite keeps the joke and drops the number. (The in-venue line "ROCK GAINED 1000 EXP." stays: it is a gag about
this game, not a claim about Dragon Quest.) KN1: JP uses Erdrick's Japanese name, ロト (Loto).

**Centaur: ATLANTIS RUINS** (*Atlantis no Nazo*, *Kid Icarus*)

| Id | Secret | Tier A | Tier B (`venues_b.md` §3.12) |
|---|---|---|---|
| CE0 † | exit: ZONE 100 | EN: Atlantis had more than a hundred zones, and the last ones were the hardest to reach. Here the last one is mostly underwater. / JP: アトランティスには 100いじょうの ゾーンが あり、 さいごの ゾーンほど たどりつくのが むずかしい。 ここでは さいごの ゾーンは ほとんど みずの なか。 | EN: Atlantis keeps its deepest door underwater. In ZONE 15, wait for the lowest tide. / JP: アトランティスで いちばん ふかい とびらは みずの なか。 ゾーン15で しおが いちばん ひく ときを まて。 |
| CE1 | room: ZONE 0 | EN: ZONE 0 is on no map. It only shows up when the lights go out. / JP: ゾーン0は どの ちずにも ない。 あかりが きえた ときだけ あらわれる。 | EN: In the black zone, one door only shines with the lights off. Climb to it. / JP: くらやみの ゾーンで ひとつの とびらは あかりを けした ときだけ ひかる。 そこまで のぼれ。 |
| CE2 | item: CENTURION | EN: In Kid Icarus, freed stone soldiers flew into the boss fight. Three here would like to stop being statues. / JP: パルテナの かがみでは いしから とけた へいしが ボスせんに かけつけた。 ここにも せきぞうを やめたい へいしが 3にん。 | EN: Three soldiers in the ruins are not statues. A charged shot wakes them. / JP: いせきの へいし 3にんは せきぞう では ない。 チャージショットで めを さます。 |
| CE3 | plate T (JET) | EN: Pegasus crossed that gap with wings. You have a dog with a jetpack. / JP: ペガサスは つばさで その すきまを こえた。 きみには ジェットの いぬが いる。 | EN: Beat's T-plate rests in a temple beyond the Pegasus gap. You'll need wings, or a Jet. / JP: ビートの Tプレートは ペガサスの すきまの むこうの しんでんに ある。 つばさか ジェットが いる。 |

CE0 †: *Atlantis no Nazo* has 101 zones counting its secret final zone, so "a hundred" became "more than a hundred". CE2
names *Kid Icarus* by its Japanese title in JP (パルテナの鏡, *Palthena no Kagami*).

### 7.2 Generic debrief lines (JP)

`meta.md` §4.5's EN lines are kept; the JP:

| Id | JP |
|---|---|
| R1 POWER | ここは パンチりょくが たりない。 2しょうめの あとに また きてね! |
| R2 JET | ここには とぶ せんしゅ むけの みちが ある。 4しょうめの あとに また きてね。 |
| R3 SUPER | ホール・オブ・フェイムに あたらしい アダプターが かくれてる。 ここで なにかが それを まってる。 |
| R4 TAG | ふたりなら いける ばしょが ある。 もうすぐ タッグパートナーが できるよ。 かめんの ひとが。 |
| R5 weapon | しんさいんの みたてでは べつの チャンピオンの ぶきが かぎ。 %WEAPON% かも? |
| G TIME | しんさいんには おそすぎ! ここの パーは %PAR%。 きみは %TIME%。 |
| G DAMAGE | しんさいんは ダメージを ぜんぶ かぞえてる。 へらせば しょうきん アップ。 |
| G VARIETY | しんさいんは バラエティが だいすき! いろんな ぶきと フォームで たおすと いちばん もうかる。 |
| G SECRETS | ここには まだ ひみつが ある。 ひとつ みつけたら つぎを おしえて あげる。 |
| G STYLE | チャンピオンには じゃくてんで とどめを。 Eかんは ポケットに しまって おいて。 |
| perfect 1 | パーフェクト! パパが ないてる。 スタジアムの ライトの せい だって。 |
| perfect 2 | もう さがす ものは ない! しんさいんも ヒントが きれちゃった。 |
| perfect 3 | Mr.Y の しんさいんまで 10てんを あげた! すぐ ひっこめた けど みんな みたよ。 (after S33: 「ワイリーの」) |
| perfect 4 | この かいじょうは 100% クリア。 もう やめて いいよ。 ・・・やめない? じゃあ また みてる。 |

`meta.md`'s STYLE line ("keep the E-tank in your pocket") is right for NO TANKS (2 points, `systems.md` §6.5); the
weakness-finish clause matches WEAK FINISH (4 points).

---

## 8. Chip help pages

`systems.md` §9.2 owns the 21 chips and their effects and drafted the EN help pages; this section rewraps them to
the window (**3 lines × 28 cells**, `systems.md` §9.1: the drafts ran to 37 cells) and adds the JP. The catalogue voice
is Eddie's shop. **◊ = cryptic on purpose** (4MI's help pages, whose readme warned that some hide functions, `r4mi/text.md`
§2). Each ◊ page's meaning is given for the designers; it never ships.

| # | Chip | EN (3 × 28) | JP | ◊ and what it hides |
|---|---|---|---|---|
| 1 | ENERGY BALANCER | Spare energy finds the / emptiest tank. The 1993 / original. Accept no copies. | あまった エネルギーは / いちばん へった ぶきへ。 / 1993ねんの げんてんモデル。 | — (it is vanilla's Balancer, `rm6/SUMMARY.md` §1.3) |
| 2 | SHOCK ABSORBER | No more flinching. You / still blink. You just blink / standing up. | もう のけぞらない。 / てんめつは する。 / たったまま てんめつ する。 | — |
| 3 | SPIKE GUARD | One spike, one more chance, / once per life. The second / spike is still a spike. | トゲに ふれても 1いのちに / 1かいは たえる。 / 2ほんめの トゲは トゲ。 | — |
| 4 | CHARGE KIT | Charges faster. The judges / call it "efficient". This / time they mean it nicely. | チャージが はやくなる。 / しんさいんいわく 「こうりつ / てき」。 こんどは ほめことば。 | — |
| 5 | JET TUNER | Bigger tank, same Rush. / Do not tell him about the / extra weight. | タンクは おおきく / ラッシュは そのまま。 / おもくなった ことは ないしょ。 | — |
| 6 | EXCHANGER | Life you can't use becomes / energy you can. Two for / one. Eddie's math. | つかえない ライフを / つかえる エネルギーに。 / 2たい1。 エディけいさん。 | — |
| 7 | AFTERIMAGE | After a hit you stay a blur / a little longer. Enemies / hate that. | ダメージの あと すこし / ながく ぶれて いられる。 / てきは それが きらい。 | — |
| 8 | ENERGY SAVER | Every weapon sips instead / of gulping. Takes two / slots. Worth it? Discuss. | どの ぶきも ちびちび のむ。 / スロットを 2つ つかう。 / その かちは? ぎろん しよう。 | — |
| 9 | IRON HELMET ◊ | Hammered from a sword and a / shield. Some blows forget / themselves. Late, always. | かたなと たてから きたえた。 / ときどき いちげきが じぶんを / わすれる。 よわれば かならず。 | Halves a hit on 1 frame in 8, and always at HP ≤ 4 ("late" = low HP) |
| 10 | THERMOS | Keeps tanks hot and weapons / cold. Or the other way / round. Drink up. | タンクは あつく ぶきは / つめたく。 はんたい かも。 / ぐいっと どうぞ。 | — |
| 11 | BIRD SEED ◊ | Beat says thank you. Beat / says it with less / pecking. | ビートが ありがとう って。 / つつくのは すくなめに / して くれる そうです。 | The pit rescue costs 2 HP instead of 4 ("less pecking") and works from HP ≥ 3 |
| 12 | GLIDER ◊ | Wind and feathers. When / the tank is dry, keep / holding on. | かぜと はね。 / タンクが からに なっても / にぎった ままで。 | Hold A with an empty Jet tank to glide |
| 13 | YASHICHI ◊ | It spins when you need it / most. Once. Then it rests / until the next match. | いちばん ひつような ときに / まわる。 1どだけ。 つぎの / しあいまで やすむ。 | Once per stage, at HP ≤ 4, a full refill |
| 14 | KAISHIN | AN EXCELLENT MOVE! Now and / then a hit lands harder / than it should. | かいしんの いちげき! / ときどき いちげきが / おもったより きく。 | — |
| 15 | SHERIFF STAR | Deputies get paid better. / That is the whole point of / being a deputy. | ほあんかんは きゅうりょうが / いい。 ほあんかんに なる / りゆうは それだけ。 | — |
| 16 | AUTO RECOVER ◊ | Stand still and listen. / Something is growing back. / The jungle is patient. | じっと して みみを すませて。 / なにかが はえて くる。 / ジャングルは きが ながい。 | 60 f without input, then +1 HP every 30 f |
| 17 | SNOW CHAINS | Ice holds still under your / boots. Icicles bounce off. / The seals taught you this. | こおりでも すべらない。 / つららも はねかえす。 / アザラシたちに おそわった。 | — |
| 18 | FIREPROOF | Fire hurts. Fire no longer / ends the match. The fire / marshal approves. | ひは いたい。 でも ひで / しあいは おわらない。 / しょうぼうかんも にっこり。 | — |
| 19 | CENTURION | A friend from the ruins / waits at every title fight. / Three arrows' worth. | いせきの ともだちが / ボスせんで まって いる。 / やは 3ぼんまで。 | — |
| 20 | DARUMA ◊ | Fall seven times, stand up / eight. Well. Once. But do / count your falls. | ななころび やおき。 / まあ 1かい だけ。 でも / ころんだ かずは かぞえて。 | Proposed **secret function** (`systems.md`): after the 7th KO in one stage visit, DARUMA triggers twice per life for the rest of that visit. The proverb made literal |
| 21 | Y-TURBO ◊ | Mr. Y guarantees results. / Mr. Y guarantees a lot of / things. See warranty. | Mr.Y は けっかを ほしょう / いたします。 いろいろ ほしょう / いたします。 ほしょうしょ さんしょう。 | Proposed **secret function** (`systems.md`): Y-TURBO is inert in Super Wily Castle (Wily's back door); its CHIPS row there reads `WARRANTY VOID` (§6.5 W line 4) |

The two proposals are 4MI's "help pages that hide secret functions", one generous and one a moral. Both are listed as
dependencies (§12); if `systems.md` declines them, pages 20 and 21 lose their last line's hint and get
"Takes two slots." / 「スロットを 2つ つかう。」 and "Results not guaranteed." / 「けっかは ほしょう いたしかねます。」.

---

## 9. ENGRISH

`meta.md` §12 owns the mechanism (a sparse override table, EN fallback, the letter O for zero in numbers) and a first
table; this section is the final list. **Rules:** menus only (never story, hints or help pages; the one exception is
Break Man's perfect line, §4 S47, a deliberate 4MI tribute); affectionate, never mocking; the classics quoted
correctly; every string legal in its surface's font (§10.1: the pause font has no D, O, Q or Z, and ENGRISH there
must spell around them too).

| Surface | ENGLISH | ENGRISH | Note |
|---|---|---|---|
| Title | GAME START | GAME STARTING | |
| Title | CONFIG | CONFIGULATION | |
| Title | SPECIAL EVENTS | SPECIAL EVENT IS HAPPEN | |
| CONFIG, language row | ENGRISH | ENGRISH (ENGLISH IS COME!!) | 4MI's "ENGLISH COMING SOON", answered |
| File select | NEW ENTRANT | NEW CHALLENGER IS HERE | |
| File select | ERASE / COPY | ERASE IT!! / COPY IT | |
| File select | BROKEN DATA | DATA IS BROKEN. SORRY | |
| Saving icon | SAVING | NOW SAVING... | the "NOW LOADING" family |
| Difficulty | CASUAL / HARD / 1993 | CASUALLY / VERY HARD / 1993 (OLD DAYS) | |
| Bracket | PUSH START | PUSH START BUTTON | |
| Bracket | SEMIFINAL / POSTPONED | SEMI-FAINAL / POSTPONE | stage-select font: letters, `.` and `-` only |
| Bracket | 4 TO GO | 4 MORE TO GOING | |
| Bracket, B layer | EXHIBITIONS | EXHIBITON MATCH | |
| YOU GET | YOU GET | YOU GOT A | |
| Pause, weapons | C.FLASH | C.FLRSH | vanilla's own misspelling (`rm6/SUMMARY.md` §1.2) |
| Pause | CALL / RETIRE | CALL HIM / GIVE UP | pause-font legal |
| Scorecard | MEDAL / PLATINUM / BOLTS | METAL / PLATINAM / BORTS | |
| Scorecard | NO IMPROVEMENT / NEW RECORD!! | NOT IMPROVE. SAD / NEW RECORDS!! | |
| Shop | WELCOME! | ALL YOUR BOLTS ARE BELONG TO EDDIE | *Zero Wing* (Mega Drive, 1991 in Europe) |
| Pit stop | SAVE & QUIT | SAVE AND GOODBYE | |
| Game over | GAME OVER / CONTINUE | GAME IS OVER / CONTINUE? YOU CAN | |
| GP Rush | ELIMINATED / CHAMPION | YOU ARE ELIMINATE / A WINNER IS YOU | *Pro Wrestling* (Famicom 1986, NES 1987) |
| Records | KNOCKOUTS / TOTAL | TIWNS / TOTALLY | 4MI's heading |
| Rating, header | CHAMPIONSHIP RATING | CONGLATURATION !!! | *Ghostbusters* (NES, 1988), its ending screen |
| Rating | GRAND CHAMPION / PARTICIPANT | GRAND CHAMPIOM / THANK YOU FOR PARTICIPATE | |
| Credits | TRANSLATION: (name) | TRANSLATION: (RESERVED) | 4MI's credit |

The quoted classics are accurate to their originals' spelling: "ALL YOUR BASE ARE BELONG TO US" (*Zero Wing*), "A
WINNER IS YOU" (*Pro Wrestling*), "CONGLATURATION !!!" (*Ghostbusters*). Digits: ENGRISH prints numbers with O for zero
(`meta.md` §12: `1OO`), the mirror of vanilla's pause font, which writes O with a zero.

---

## 10. Text engines, fonts and bilingual output

### 10.1 Every text surface, its engine and its font (from `rm6/text.md`)

Vanilla's fonts differ per screen: the same byte is a different letter on different screens (`rm6/text.md` §1, §6).
GP keeps the vanilla surfaces with their fonts (and their quirks), and puts every sentence it adds in **one new
engine** (§10.2). The rule that keeps this simple, taken from vanilla itself:

> **Labels stay English in both languages; sentences are translated.** Vanilla's JP game shows GAME START, PASS WORD,
> STAGE SELECT, CONTINUE, the pause labels, the boss panel and YOU GET in English (`rm6/text.md` §5). GP does the
> same for every menu label, and translates only sentences: dialogue, commentary, hints, help pages, plaques,
> descriptions.

| Surface | Engine | Font (vanilla "A=") | Glyphs available | Limits and rules | Language |
|---|---|---|---|---|---|
| Boot / license | PPU script `$1F` | main `$0B` | `0-9 A-Z . ー ゜ ? ! 「 」 ' : ,` `・ © 。`, 46 hiragana, 16 katakana | no `-`: S01 uses `ー` or adds one tile | EN in both |
| Title, CONFIG, file select | `meta.md` / `art_audio.md` (menu font in `$1000`, `art_audio.md` §2.8) | GP menu font | caps, digits, `. - : ! ? ' / ( )` | labels only | labels EN in both; the difficulty descriptions are sentences (§10.2) |
| Bracket node labels | PPU (stage-select font) | stage select `$2B` | **`0-9 A-Z . -` and blank only: no `! ? ' :`** | `meta.md`'s `B: EXHIBITIONS` needs a `:` tile or becomes `B EXHIBITIONS` | EN in both |
| Bracket message window (Kalinka) | new engine | glyph cache | full (§10.2) | 2 lines × 28 | translated |
| Boss panel | `$3C:$81B1` | panel bold set | `0-9 A-Z .` + GP's `- ? ! ' β` (§5.1) | field widths §5.1 | **English in both** (vanilla quirk) |
| YOU GET | PPU `$60+` | YOU GET bold set | `0-9 A-Z .`, `-` = `$B8`; R and A look alike | `C.FLRSH` kept on the card (`systems.md` §3.9) | EN in both |
| Pause menu, weapon page | PPU `$0A`, `$38-$40` | pause `$20` | **no D, O, Q or Z** (their slots hold icons); `.` but no `-` | write O as **0** (`N0R`, `P0W`, `W.ST0RM`); new strings must avoid D, Q, Z: `M.BEAM`, `CALL`, `RETIRE`, `SUPER`, `CHIPS` are legal; Break Man's refusal is `N0`; Y-TURBO here is `Y.TURB0` | labels EN in both |
| Pause CHIPS page and help pages | new engine | glyph cache | full | 3 lines × 28 per help page (§8) | translated |
| Password grid (hidden gag) | vanilla `$14`, `$16` | main | vanilla | — | EN in both |
| Game over / continue | PPU `$18/$19/$1A` + `RETIRE` | main `$0B` | as boot | Kalinka's line goes in the new window | labels EN |
| Crawl, scenes, NPC windows, pop-ups, debrief, plaques | **new engine** | glyph cache | full | §10.2 | translated |
| CAPCOM TIMES | vanilla driver `$3B:$A886` | main `$0B` + picture headline | the body: main font, plus the glyph cache for katakana it lacks | 2 lines per page, typed with blip `$27` | translated; vanilla `$95/$96` kept verbatim in JP |
| Ending robot cards | PPU `$71-$80` | stage select `$2B` | as bracket | kept verbatim (`DWNB-41 BLIZZARD-MAN`…) | EN in both |
| Staff roll | PPU `$81-$87` | roles `$80` (cyan) + main | caps | names in romaji capitals | EN in both |
| TO BE CONTINUED | PPU `$88` | main | — | kept | EN in both |
| Debug sound player (Museum VAULT) | bank `$28` | ASCII `$FC-$FF` | — | untouched | EN |

**Main-font katakana.** Vanilla's main font has only 16 katakana (イ ク シ ス ト フ ホ マ ラ リ ル ロ ワ ン and small ッ ュ;
voiced forms use a separate ゛ tile; `rm6/text.md` §6): enough for ロックマン, ロボット, ラッシュ and
Dr.ワイリー, not for フォルテ, ブレイクマン or コサック. So **no GP JP sentence is drawn in a vanilla font**; they all go
through the new engine, whose font is complete.

### 10.2 The new text engine (BRIEF §7.5) [new-code] M · Must

`tech.md` builds it; this is what the text needs from it.

**Glyph cache, not a resident font.** In stages, the BG pattern table is full (Plant uses all 256 tile ids,
`rm6/SUMMARY.md` §2), so a resident font is impossible there. Instead the font lives in PRG as 1-bpp 8×8 glyphs, and
each window **uploads only the distinct glyphs of the page it is about to show** into a reserved strip of CHR, then
writes the nametable with strip indices. This is how `art_audio.md` §2.6 already budgets the pop-up ("pop-up glyphs ≤
384 B, 24 tiles, before the window opens").

| Window | Lines × cells | Glyph strip | Notes |
|---|---|---|---|
| POP (in-stage) | 2 × 28 | **24 tiles** (`art_audio.md` §2.6) | + a 16×16 face icon (sprites, 4 tiles). The compiler splits a page over 24 distinct glyphs |
| SCN (story window over a scene) | 4 × 28 | up to 96 | portraits 32×32 BG (16 tiles each) |
| Plaque / crawl page | up to 9 × 28 | up to 128 | full-screen scenes have 65-131 free BG tiles (`rm6/text.md` §7); check each with `chrfree3.py` |
| Debrief (`meta.md` §4.1) | 4 × 28 | up to 96 | the judges' desk is a menu screen with room |
| Help page (§8) | 3 × 28 | up to 64 | pause / pit stop |

**Measured against this doc's own lines** (`build/design/design-story/glyph_budget.py`): the commentator pages have a
median of **12 distinct glyphs (EN) and 13 (JP)**; 10 EN and 21 JP pages exceed 24, almost all of them the multi-page
choice lines of §6.5, which the compiler splits anyway. So the 24-tile strip holds; JP needs splitting on about 1 page
in 12.

**Glyph set** (≈ 240 glyphs, ≈ 2 KB per weight at 8 B each):

- Latin capitals, digits, `. , ! ? ' " : ; - / & % ( ) ★ ♥ ♪ β × ▶ ・ …` (EN is upper-cased: no lowercase set, §10.3);
- hiragana and katakana, **with voiced and semi-voiced forms as precomposed glyphs** (ば, パ, ヴ: one tile each, unlike
  vanilla's separate ゛ tile), small kana (ぁぃぅぇぉっゃゅょ / ァィゥェォッャュョ), `ー 「 」 『 』 、 。 ~`;
- no kanji (vanilla's JP text has none; the only kanji in RM6 are the logo's, `rm6/text.md` §1).

**Typewriter.** Speed from CONFIG TEXT SPEED (2 / 1 / 0 / 4 frames per character, `meta.md` §11.1). A per-speaker blip
(vanilla's own mechanism, `$06A6` per tile, `rm6/text.md` §4.2): Cossack low, Kalinka high, Mr. Y a cash-register
"ching", Wily a cackle, Roll a soft beep, Light none (radio static at page start), Break Man none (his whistle at page
start). Spaces are free (vanilla charges them; GP does not).

**Highlight colour.** `*word*` draws in the window's second colour (CX does this, `cx/SUMMARY.md` §4).

**Choices.** `▶YES NO` and up to 4 items (T2, `venues_a.md` §0.4). In JP, `▶はい いいえ`.

### 10.3 Writing rules (enforced by the text compiler)

1. **EN is ALL CAPS** in every window. Reasons: it is the house style of every NES Rockman script; vanilla's fonts and
   `meta.md`'s debrief are capitals; a caps-only glyph cache needs a third fewer distinct glyphs per page than mixed
   case. `art_audio.md` §3.5 planned a mixed-case EN set in the kana slots; this doc asks it to drop that set (a saving
   of about 26 tiles of art). Dependency §12.
2. **JP is kana only**, with spaces between phrases (vanilla's style: 「8つの ちいきから えらびぬかれた」). Katakana for
   loanwords and robot names; Latin for `Mr.Y`, `Dr.`, `GP`, `DEFENCE`/`MOBILE` (as on the card), `B` (the button);
   Arabic digits; 「」 for quotes; `・・・` for ellipses (vanilla's).
3. **Widths:** 28 cells per line; POP ≤ 2 lines, SCN ≤ 4. A JP line is counted in cells, one per kana.
4. **Per-surface glyph check:** every string is checked against its surface's font (§10.1). On the pause surface the
   compiler rejects D, Q, Z and converts O to 0 if the string is flagged `ZERO_O`; on the bracket it rejects `! ? ' :`.
5. **No WIP text ships.** The release build fails on any string containing `WIP`, `TODO`, `TBD`, `XXX` or an empty
   credit field (4MI shipped "WIP WIP WIP / UNDER CONSTRUCTION", `r4mi/text.md` §0).
6. **Variables** reserve their width: `%N%` 2, `%T%` 4, `%PAR%` / `%TIME%` 7, `%H%` 1, `%MM%` 2, `%NAME%` 12,
   `%WEAPON%` 8, `%PLAYER%` 7.
7. **Variant selectors** per line: pre/post unmask (STORY_BEAT ≥ `$09`), BASS, DOPED, TAG, and the cause byte for
   deaths.

### 10.4 How bilingual output works

- **One setting:** SYS `$008` LANGUAGE = 0 JAPANESE, 1 ENGLISH, 2 ENGRISH (`meta.md` §8).
- **One id per string, one table per language.** Source: `text/*.tsv`, one row per string: `id, surface, speaker,
  EN, JP, ENGRISH (optional), max_lines, notes`. The compiler (`tools/text/`, `tech.md`) emits `TXT_EN`, `TXT_JP` and
  a sparse `TXT_ENGRISH` (sorted ids, falling back to EN, `meta.md` §12), plus a coverage report: every id has EN and
  JP, every page fits, every glyph exists on its surface.
- **The new engine** reads LANGUAGE once per page and picks the table.
- **Vanilla PPU scripts** go through one hook at `$3C:$8631` (`rm6/text.md` §8 lesson 2) that picks an EN pointer
  table. GP replaces almost all of vanilla's JP-only scripts (the intro `$49-$5E`, the Mr. X speech `$6C-$6E`, the
  newspaper `$92-$94`), so the hook is needed only for the few vanilla JP scripts GP keeps: the newspaper's last
  pages `$95/$96` (EN versions added) and, for MR. X RETURNS, the Mr. X speech (Could).
- **The boss panel, YOU GET, the staff roll and TO BE CONTINUED do not branch**: they are English in both, as vanilla.
- **Language switch at run time** (CONFIG): takes effect at the next page; no reload.
- **Size:** about 1,100 strings (300 commentator lines, ~350 scene pages, 120 hint and help pages, ~300 labels and
  NPC lines) × 2 languages ≈ 70-90 KB with a simple dictionary compression of common words, in 2-3 text banks.

### 10.5 What the vanilla text constraints mean for the script

| Constraint (`rm6/text.md`) | Consequence in this doc |
|---|---|
| The pause font has no D, O, Q, Z | Pause labels chosen to avoid D/Q/Z; O written as 0; Break Man's refusal `N0` is a joke on purpose (S21) |
| The stage-select font has no punctuation | Kalinka's bracket lines live in the new window; node labels are bare words |
| The panel is English in JP; only 12 letters for a name | Cards in English (§5); W2 copies named `BLIZZARD.EXE` (12) |
| The YOU GET font draws R like A | `C.FLRSH` kept: it reads "C.FLASH" on screen and is a joke in CEN-20 |
| No kanji anywhere but the logo | JP is kana-only, spaced (§10.3); GP's subtitle 史上最大のグランプリ!! is logo art like vanilla's |
| Main font has 16 katakana | All GP JP goes through the glyph cache |
| Typing speed and blip are per-call variables | Per-speaker blips (§10.2) |
| Text timing is fixed waits after typing | Scenes advance on a button; pop-ups on a length-based timer (§6.1) |

---

## 11. How crazy it gets: the story's screenshot moments

The venue docs list their own; these are the story's.

1. The attract crawl's jail cell holds a cardboard Wily. Its sign says BACK IN 5 MINUTES.
2. Roll call: a masked entrant with no sponsor and no data, who "brought his own theme music"; Rock says "Blues?"
   and gets "Break Man."
3. Bass β is registered as **entrant β**, because Mr. Y ran out of numbers; the committee is still arguing.
4. Rule 8 of the tournament is "do not ask about Rule 8"; Rule 9 makes tag teams legal, and it happens.
5. The GP mascot, filled with Mr. Y-brand helium, inflates to fill the room. Break Man's voice: "Hold B. Let go when
   you glow."
6. The judges' desk always has a cardboard Mr. Y on the sponsor's chair, holding up a 1.
7. Bass dashes across the bracket stamping POSTPONED on every match; the Committee approves it by fax.
8. The Semifinal crowd is entirely Sniper Joes in Bass scarves.
9. A shady booth sells a chip "legal in at least one country"; take it, and Break Man walks off the edge of the
   bracket, and his pause portrait reads **N0**, spelled with a zero like vanilla's N0R.
10. The trophy is stolen with Cossack's own claw, which Mr. Y "bought in the museum gift shop", from a saucer with a Y
    painted over a W.
11. A museum of Rockman 1-5 whose plaques are true, and whose exhibits fight back.
12. Cossack commentates against his own 1991 machine and apologises live on air.
13. A fake Break Man with a flat whistle and his scarf on the wrong side; the real whistle, in tune, from the doorway.
14. Five faces, one page: "WE KNOW."
15. Wily's 16-bit speech, which is half right: three colours a sprite, eight a line, five channels.
16. A castle that rises in Game Boy green and upgrades its palette as you climb; the boss tries to install itself into
    Rockman: "PLEASE DO NOT TURN OFF YOUR ROBOT."
17. The refights are data copies named `BLIZZARD.EXE`; the real champions boo them from the stands.
18. WILY MACHINE 6.5 ("He couldn't wait for seven"), whose "Mode 7" floor Kalinka exposes as scrolling strips.
19. Wily blames Mr. Y. "You ARE Mr. Y." "Mr. Y is very persuasive."
20. Break Man catches Rock in the falling castle and takes Wily too: "This time." (Rockman 3 left him behind.)
21. The ending turns the music off one sound channel at a time while Light explains why that isn't sad.
22. The Hall of Fame opens a sixth wing for the game you are playing, and its plaque is true.
23. The CAPCOM TIMES announces next year's sponsor, Mr. Z, and ends on vanilla's own last sentence.
24. The credits list every enemy as an **entrant**, each one ELIMINATED, and keep the 1993 fan designers' cards exactly
    as Capcom printed them.

---

## 12. Cross-doc dependencies

| Doc | This doc needs | This doc gives |
|---|---|---|
| `meta.md` | STORY_BEAT at FILE `$013` (§0 defines the values); FILE `$04A` b0-7 for the once-per-save commentator flags (§6.1); the bracket message window; EVENTS bits b0-b7 and EVENTS2 b0-5 as listed in §3; the results screen's sponsor-chair sign `BACK SOON` from S26 and `RESERVED` from S33 (an amendment to §4.0's "after the unmasking") | every line `meta.md` §15 asked for: the attract crawl, the Riot lines, Roll's adaptor lines, the trophy theft, Break Man's join beat and debrief voice, the post-game intro, ENTRANT FILES data, Mr. X Returns, Bass Mode swaps; final tier A/B hint text with JP; the confirmation that Kalinka speaks the debrief; ENGRISH's final list |
| `systems.md` | **Proposals:** (1) DARUMA's hidden function (7 KOs → twice per life, §8); (2) Y-TURBO inert in W1-W3 with a `WARRANTY VOID` label (§8, §6.5); (3) the 1-bolt "respawn insurance" choice (§6.5 line 5, Could). The synergy names as used in §6.2. The weakness columns in §6.2 follow its §4.5 placeholders | the JP help pages; the EN pages rewrapped to 28 cells; every announcer line it asked for (EV_WEAK_FIRST, resist, immune, parry, synergies, Time Stop, crits, close calls, Break Man call/retreat, forms, tanks); Break Man's refusal line; the doping headline |
| `venues_a.md` | — | final EN/JP of its hooks and death tables (`WND-`, `KNT-`, `TMH-`, `PLT-`, §6.3); answers: the rental Jet and the RENTAL bib are approved; Princess Roll is approved; Tango as the cat is approved and accurate; "WANTED: ROCKMAN" is approved; YOU GET never shows adaptors (S11); the KN2 riddle changed (§7.1) |
| `venues_b.md` | Agreement to show Flame's venue as **PERSIAN PALACE** on screen (§5.1); FLM-01 without "Oil Sultanate" | final EN/JP of `BLZ-`, `FLM-`, `CEN-`, `YAM-` and a 6th death line each; the Yamato and Centaur tier B lines adopted from §3.12/§4.13 |
| `fortress.md` | Placement of: the Opening's tunnel, pit, parade podiums and big screen (S03-S07); the Semifinal's crowd set piece (S18); the H2 and H4 thanks-plaque rooms; Mr. X's card; the central gallery (S32); the castle's palette tiers (S35); the W2 refight hub and stands (S36); the escape's end (S40); the victory lap (S45). A name for the W1 boss (this doc proposes THE UPGRADER, §5.4) | every line in those scenes; the exhibit cards; the plaques; the heckle tables |
| `art_audio.md` | Portraits: Rock, Light, Roll, Cossack, Kalinka, Eddie, Break Man, Bass β, Mr. Y, Wily, Mr. X (Could); face icons for the POP speakers; the crawl's three new pictures; the plaque frame; the claw and saucer; three CAPCOM TIMES headlines; the ending arrangement **with one stem per channel** (S42); the speaker blips; **drop the mixed-case EN font set** (§10.3) | the glyph list (§10.2); the per-window CHR budgets |
| `tech.md` | The glyph-cache window (24-tile strip in stages); the text compiler with the checks of §10.3; the language hook at `$3C:$8631`; the boss panel's record pointer by fight id and its 10th field; the commentator event bus, queue and cooldown (§6.1); ~80 KB of text banks | the string inventory and sizes (§10.4) |

## Lessons applied

| Source | Lesson | Where |
|---|---|---|
| CX 1 | One premise in every layer: the menus speak tournament (entrant β, POSTPONED, Rule 9, ALL ENTRANTS … ELIMINATED) | §3-§4, §11 |
| CX 2 | Jokes sit on mechanics: the helium mascot is the charge tutorial; the "Mode 7" joke is the effect's own credit; the booth's cost is a lost partner | S08, S38, S21 |
| CX 3 | The villain's voice on failure: a per-respawn heckle table with a Yes/No that (barely) hurts | §6.5 |
| CX 5 | Reuse the engine's set pieces with one twist: vanilla's boss panel becomes the match card; vanilla's newspaper ends the game again, with its own last sentence | §5, S44 |
| CX 6 | Telegraph the tool: the requirement hints, the resist line that says "watch the flashing", the help pages | §6.2, §7, §8 |
| CX (text) | Light's lines, a whole new voice for a character vanilla left silent; the dogeza kept | §2.5, S39 |
| 4MI 4 | Friends are mechanics and story beats: Break Man's join, his refusal, his debrief | S20, S21, S47 |
| 4MI 5 | The debrief as hints, with **no WIP text** (a build check) | §7, §10.3 |
| 4MI (help) | Cryptic help pages that hide functions, two of them proposed for real | §8 |
| 4MI (voice) | ENGRISH, TIWNS, `(RESERVED)`, the fake Roll's robot katakana (for Invader Man) | §9, S23 |
| RM6 8 | Vanilla quirks kept on purpose: C.FLRSH, N0R/P0W (and the new N0), the English panel in JP, SOLAR ENERGY, ABILITY UNKNOWN, MOBILE 31, TO BE CONTINUED, the newspaper's last lines, the DWNB cards | §5, §10, S44-S48 |
| RM6 text lessons 1-10 | PPU-script hook for the few kept JP scripts; per-screen fonts respected; free CHR checked per scene; JP kana-only | §10 |

## Risks

1. **Text volume.** About 1,100 strings in two languages is a lot of text for a fan project, and every one needs a
   native-speaker JP pass. *Mitigation:* the Must set is smaller (the scenes marked Must, the death tables, the
   hints): about 600 strings. Should/Could scenes (crawl, roll call, exhibitions, victory lap, Bass Mode) can ship
   EN+JP later without code changes, since the tables are data.
2. **JP quality.** These JP drafts were written by a non-native pass. Register is the main risk (Mr. Y's わたくし, the
   DQ archaic forms, Yamato's ござる, Invader Man's katakana). *Mitigation:* a native review before M10; the DQ lines
   quote the real games' known lines (S15) so they can be checked against them.
3. **The 24-tile pop-up strip.** JP pages exceed it about 1 time in 12 (§10.2). *Mitigation:* the compiler splits; if
   `tech.md` finds 32 tiles, the splits disappear.
4. **Pop-up noise.** CX's lesson is to speak on failure, not constantly. 300 lines can feel chatty. *Mitigation:* the
   600-f cooldown for P3/P4, DEATHS ONLY mode, and a playtest metric: no more than one P3/P4 line per 20 s on average.
5. **Facts.** A wrong fact in a plaque is worse than no plaque. *Mitigation:* Appendix A lists each claim with its
   confidence; three claims are marked "medium" and are worded so that they stay true if the detail is off (RM5's day
   of release is not printed; Rockman's height is "commonly given"; Quickclaw is named, not classified).
6. **Trademarks in text.** Plaques and riddles name real games (*Dragon Quest*, *Pac-Man*, *Tetris* …) to credit them.
   That is homage text, not branding, and no logo appears; but on-screen titles use parody or generic names (§1.2
   rule 5, PERSIAN PALACE). If the project wants zero third-party names, the riddles can drop the names and keep the
   rules (each riddle was written to work either way).
7. **Dependence on Should systems.** Break Man's whole arc rests on SYS-TAG-1 (Should). Without it: S18 stays (he
   helps once), S20 becomes "Rule 9 applies; nobody steps forward... then a whistle, far away", S21's cost moves to the
   asterisk and the headline, S30 and S40 keep their *walked* variants, and S47 stays. The story survives the cut.

## Open questions

1. **Entrant numbering.** This doc fixes the champions as entrants 1-8, Rockman 9, Break Man 10 (BRIEF §2), and Bass
   β as "entrant β". PLAN called Bass "a ninth entrant". Is β acceptable as the bracket's in-joke?
2. **PERSIAN PALACE** as Flame's on-screen venue name (§5.1): does `venues_b.md` agree?
3. **EN in capitals** (§10.3) against `art_audio.md` §3.5's mixed-case set: which does the project want?
4. **Block Man's name** clashes with Rockman 11's Robot Master (2018). The joke is written in (S22); rename the guest
   instead (TETRA MAN) if the project prefers no clash.
5. **Light's "Albert"** (S33, S42 context): the full name Albert W. Wily is from English-language material; the JP
   line uses アルバート. Keep, or have Light say ワイリー in JP?
6. The CX author's name in kana/kanji for the JP thanks plaque (kept in Latin letters until confirmed).
7. Should Mr. Y's 1-bolt insurance (§6.5 line 5) really take a bolt (CX's "Yes that hurts"), or only pretend to?
8. Should the victory lap's ALL ENTRANTS roll be generated from the object lists at build time (proposed) or written
   by hand?

---

## Appendix A. Fact sheet (every game-history claim in the text)

Confidence: **high** = confirmed from a cited source in this session or from the project's own research docs;
**medium** = widely reported, worded so a small error would not make the line false. Sources checked in this session
are listed by name; the project's own docs by path.

| Id | Claim | Used in | Confidence and source |
|---|---|---|---|
| A-1.1 | Rockman (Famicom) was released on 17 December 1987; Mega Man in America the same month | H1 plaque | high: gamer.ne.jp (30th anniversary on 17 Dec 2017), Famitsu |
| A-1.2 | Wily reprogrammed six of Light's robots: Cut, Guts, Ice, Bomb, Fire, Elec; Rock was Light's lab assistant and volunteered | H1 | high (series canon; the JP names カットマン … ボンバーマン … エレキマン) |
| A-1.3 | Rockman 1 is the only numbered Rockman with a points score | H1 | high |
| A-1.4 | The Yellow Devil splits into pieces, flies across, reassembles; weak to the Elec Beam (JP Thunder Beam) | H1, §5.4 | high |
| A-1.5 | The Magnet Beam is in Elec Man's stage, behind blocks the Super Arm must lift | H1 label | high |
| A-1.6 | In Rockman 1, SELECT pauses, and pausing/unpausing lets a weapon (the Thunder Beam) hit the Yellow Devil again | H1 last line, `systems.md` SC7 | high: the Mega Man Glitches wiki; Steam community threads |
| A-2.1 | Rockman 2: Dr. Wily no Nazo, released 24 December 1988 | H2 | high: rank-king.jp comparison table |
| A-2.2 | Capcom's fan robot-design contests began with Rockman 2 (1988) | H2 | high: The Mega Man Network, gamereactor (contest histories) |
| A-2.3 | Eight Robot Masters (Metal, Air, Bubble, Quick, Crash, Flash, Heat, Wood); E-tanks and passwords debut | H2 | high |
| A-2.4 | The JP release has one difficulty; the US added NORMAL and called the original DIFFICULT | H2 | high |
| A-2.5 | The Mecha Dragon chases Rock in Wily stage 1 | H2, S28 | high |
| A-2.6 | Flash Man's Time Stopper | §6.2 Time Stop line | high |
| A-3.1 | Rockman 3: Dr. Wily no Saigo!?, released 28 September 1990 | H3 | high: Nintendo's VC page, Famitsu |
| A-3.2 | Rockman 3 introduced the slide, Rush and Break Man (Blues) with his whistle | H3 | high: Famitsu ("ブルースやラッシュが初登場…スライディングも追加") |
| A-3.3 | Light and Wily built Gamma together as a peacekeeping robot; its last form falls to the Top Spin | H3, S28 | high (canon); "falls to" = its weakness |
| A-3.4 | Doc Robot uses the eight Rockman 2 bosses' abilities | H3 | high |
| A-3.5 | At Rockman 3's end Break Man pulls Rock from the rubble and says he is too late for Wily | S40 | high: Mega Man wiki (MM3 story) |
| A-3.6 | Holding RIGHT on controller 2 gives a super jump that escapes pits; removed from the European release | H3 | high: TCRF, StrategyWiki, TASVideos |
| A-4.1 | Rockman 4: Aratanaru Yabō!!, released 6 December 1991 | H4 | high: Nintendo's VC page |
| A-4.2 | Rockman 4 introduced the charge shot, Eddie, Dr. Cossack and Kalinka; the Wire and Balloon | H4 | high |
| A-4.3 | Wily held Kalinka hostage to force Cossack; Break Man (Proto Man) brought her back | H4 | high |
| A-4.4 | The Cossack Catcher is a crane-game machine | H4, §2.12 | high (its name is the UFO-catcher pun) |
| A-4.5 | Rockman 4 Minus Infinity is by Puresabe, 2008-2016; Rush is sealed in a wall; its hint says to read weaknesses from the flashing | H4 thanks | high: `r4mi/SUMMARY.md` |
| A-4.6 | Rockman CX is by Himajin Jichiku (ver 1.1, 2017); its Air Man is an invisible stipple; Light is the villain | H2 thanks | high: `cx/SUMMARY.md`, `cx/text.md` |
| A-5.1 | Rockman 5: Blues no Wana!?, 1992 | H5 | high (year); the day is not printed (medium: 4 December) |
| A-5.2 | A Blues look-alike kidnapped Light; it was Dark Man (built by Wily); the real Blues appeared and unmasked him | H5, S30 | high: Wikipedia (MM5), Mega Man wiki |
| A-5.3 | The Beat plates spell R-O-C-K-M-A-N-5 in Japan and M-E-G-A-M-A-N-V abroad | H5 | high: TCRF (MM5 regional differences), Mega Man wiki |
| A-5.4 | Dr. Cossack built Beat in Rockman 5 | H5, §6.2, CEN/plate lines | high: Wikipedia (MM5) |
| A-5.5 | Gravity Man flips gravity (the screen) | H5 | high |
| A-6.1 | Rockman 6 was released on 5 November 1993, the last Rockman on the Famicom | S43 | high: inside-games (the Famicom's last Rockman), gamer.ne.jp |
| A-6.2 | All eight RM6 Robot Masters came from fan designs; Knight Man and Wind Man from a Nintendo Power contest in North America | S43 | high: Wikipedia (MM6), The Mega Man Network; vanilla's DWNB cards name the designers. The card's `DANIEL VALLIE` is commonly reported as Daniel Vallée, a Canadian fan; the card is kept verbatim (no accented letters in the font) |
| A-6.3 | Nintendo published Mega Man 6 in North America, March 1994 | S43 | high: Mega Man wiki |
| A-6.4 | NES: a sprite has 3 colours plus transparency; 8 sprites per scanline; 5 sound channels (2 pulse, triangle, noise, DPCM); MMC5 adds 2 pulses | S33, S42 | high (hardware) |
| A-6.5 | Rockman's commonly given height is 132 cm (and 105 kg) | §5.3 Bass β card | medium: licensed-product articles (toy-people, sakidori); the card's joke is worded "commonly given" |
| A-6.6 | By the end of 1993 Wily had lost in Rockman 1-6 and in Rockman World 1-4 (Game Boy; RW4 is 1993) | §6.5 W line 6 | high: StrategyWiki (RW4 1993) |
| A-6.7 | Rockman X was released on 17 December 1993, six years to the day after Rockman 1 and six weeks after Rockman 6 | S43 | high: Famitsu (30th anniversary article), wikiwiki.jp |
| A-7.1 | Bass (Forte) debuts in Rockman 7 (Super Famicom, 1995), which also introduces the Super Adaptor | S37, H3 label, §2.3 | high |
| A-7.2 | Rockman 7 opens with Wily breaking out of jail | S47 perfect line | high |
| A-7.3 | Tango debuts in Rockman World 5 (Game Boy, 22 July 1994) | PLT-08, S15 | high: ne.jp database, Famitsu |
| A-7.4 | The Sakugarne is Quint's pogo in Rockman World 2 (Game Boy, 1991) | YAM-13 | high |
| A-7.5 | "Block Man" is a Rockman 11 Robot Master (2018) | S22 | high |
| A-8.1 | Dragon Quest (1986): the hidden stairs behind the Dragonlord's empty throne; Erdrick's (ロト) tablet; the King's 「しんでしまうとは なにごとだ!」; the Princess's 「そんな ひどい」 / "But thou must!"; 「かいしんの いちげき」 / "Excellent move!"; "half the world" | KN0, KN1, S15, KNT death 1 | high: Da Vinci News and Game Watch (the DQ1 king's line); the rest series canon |
| A-8.2 | *1943*: shooting a POW cycles its item, the Yashichi among them; the Yashichi appeared first in *Vulgus* (1984), Capcom's first arcade game; *1942* gives three loops | WI0, WI2, WND death 6 | high: Sega Retro, Giant Bomb (Yashichi, Vulgus); loops: high |
| A-8.3 | *Pitfall!* has a 20-minute clock; logs cost points; *Pitfall II*: Harry seeks Rhonda, Quickclaw and the Raj diamond (Quickclaw's species varies by source) | PLT-01, PL0, PL2 | high: Wikipedia, Spectrum manual (Pitfall II) |
| A-8.4 | *Prince of Persia* (1989, Apple II): the mouse opens a gate; the hero merges with his shadow; 60 minutes | FL0, FL1, FLM-03, FLM death 6 | high |
| A-8.5 | *Ganbare Goemon! Karakuri Dōchū* (1986): three travel passes to pass the checkpoint | YA0 | high |
| A-8.6 | *Atlantis no Nazo* (1986): 101 zones counting the secret final zone | CEN-02, CE0 | high: Wikipedia |
| A-8.7 | *Kid Icarus* (JP *Palthena no Kagami*): Centurions freed from stone help at the boss; the Eggplant Wizard; Medusa | CE2, CEN-09, CEN-14 | high |
| A-8.8 | *Ice Climber*: Popo and Nana; Topi (a seal in the Famicom version); the bonus stage's condor | BLZ death 6, BL0-2 | high |
| A-8.9 | *Gun.Smoke* (1985): wanted posters, shooting objects reveals items; *Wild Gunman* (1984 Famicom); Oscar Wilde's "Please do not shoot the pianist" from Leadville | TO0-2, S15 | high |
| A-8.10 | *Tetris*: Moscow 1984, Alexey Pajitnov; packed with the Game Boy in America in 1989 | E1 plaque | high |
| A-8.11 | *Breakout* (Atari 1976); *Arkanoid* (Taito 1986), whose paddle is the Vaus | E2 plaque | high |
| A-8.12 | *Space Invaders* (Taito 1978, Tomohiro Nishikado): the invaders speed up because fewer are drawn; the "Nagoya attack" | E3 plaque, S22 | high |
| A-8.13 | *Pac-Man* (Namco 1980, Toru Iwatani): four ghosts with different chase rules; the 256th maze splits | E4 plaque | high |
| A-8.14 | ENGRISH classics: *Zero Wing* ("ALL YOUR BASE ARE BELONG TO US", European Mega Drive 1991), *Pro Wrestling* ("A WINNER IS YOU"), *Ghostbusters* NES ("CONGLATURATION !!!") | §9 | high |
| A-8.15 | Fireworks call "Tamaya!"; daruma: one eye painted at the wish, the other when it comes true; 七転び八起き; the nightingale floor; kabuki *ōmukō* shouts of the actor's house name | YAM lines, S15 | high (cultural) |
| A-8.16 | *DuckTales* (Capcom 1989): Scrooge's cane pogo finds hidden treasure | YA1, §6.2 Pogo | high |
| A-8.17 | *JoJo's Bizarre Adventure* Part 3: a time-stop punch rush, "ORA ORA" | §6.2 Time Fist | high |
| A-8.18 | Rockman's death sound is called "tiun tiun" by Japanese players; 4MI's TIWNS | §6.4 line 7 | high: `r4mi/text.md` §0 |
