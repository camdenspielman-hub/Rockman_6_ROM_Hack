# Rockman CX / Mega Man CX: the complete text

Agent: cx-text. Status: **v0, work in progress** (dialogue complete; scene context, menus, ending and screenshots being
added). Sources: `roms/cx_en.nes`, `roms/cx_jp.nes` (v1.1). Scripts: `build/research/cx/cx-text/` (predecessor run)
and `build/research/cx/cx-text2/` (this run). Tags: **[seen]** emulator, **[code]** ROM data/disassembly, **[text]**
in-game text, **[doc]** readme, **[guess]**.

## 1. Where the text lives and how it is drawn

Diffing the JP and EN builds gives about 110 differing runs. Most of them are glyph graphics; the real text is in
six places [code]:

| What | Where (ROM offset, no header) | EN encoding | JP encoding |
|---|---|---|---|
| Story crawl (intro) | pre-rendered tile strips, banks $13/$27 | proportional font baked into tiles | kana/kanji baked into tiles |
| Dialogue boxes (26 scripts + 3 branches) | bank $26, `0x4c700-0x4d9c7` EN / `-0x4d780` JP; pointer table lo `$85B0`, hi `$85D0` (CPU $8000) | **ASCII**, drawn by a variable-width-font (VWF) renderer; font 1bpp at `0x53000` (bank $29 $B000, widths in the first 128 bytes); bytes >= $80 = same letter in the **highlight colour** | tile codes; the script itself loads 16-glyph CHR pages (`CHR` op) from banks $01/$03/$09/$10/$12/$17/$28/$29/$2A; 327 distinct glyphs |
| Opening cutscene box (Guts Man) | bank $1E (`0x3ccdf` JP glyph strings) | small fixed font | kana tile string, glyphs at `0x4f500` |
| Pause menu names | bank $1F `0x3e380` (16-byte rows: 3 icon tiles + name) | `A=$01`, space `$1F`, `.`=$1B | identical table, only MEGA/ROCK differ |
| Boss roll call (ending) | bank $12 `0x24500` (offsets) / `0x24510` (lengths) / `0x24520` (strings) | `A=$31`, space `$20`, `.`=$4F, digits `$50+` | same |
| Staff roll | bank $12, tables at `0x24a62` (offset lo), `0x24ac0` (hi), `0x24b20`/`0x24b80` (PPU address), `0x24be0` (length), strings at `0x24c40` | `A=$31`, `a=$61`, space `$30`/`$20`/`$60` | same, ROCKMAN for MEGAMAN |

### 1.1 The dialogue engine (bank $26) [code]

Each dialogue box is a game object (type $26) whose `$0460,X` holds the script number x 2. The interpreter reads the
script byte by byte; bytes below $20 are opcodes:

| Op | Args | Meaning |
|---|---|---|
| `00` | | END |
| `01` | | new line |
| `02` | | wait (page continues on the next line after a beat) |
| `03 f` | face | show portrait *f* (16x16 tiles from bank $39/$3B) |
| `04 hi bank dst` | 3 | copy a CHR page into PPU $dst00 (JP uses this to swap glyph pages mid-script) |
| `05` | | short pause |
| `06` | | clear box (new page) |
| `07` | EN 0 / JP 5 | print a decimal number (the spike-death counter) |
| `08 n` | 1 | text speed |
| `09 lo hi bank` | 3 | far call: scripted action (Yes/No menu at `$24:AEF9`, teleport attempt, which-hero test at `$24:B5BF`, screen shake...) |
| `0A n` | 1 | input lock flags |
| `0B` | | close box |
| `0C n` | 1 | skip *n* bytes if the last call returned carry (used for **Fake Rockman vs Quick Man** variants and Yes/No branches) |
| `0D n` | 1 | (EN only) VWF base column |

The EN build rewrote the renderer: the JP routine at $80C4 stores tile codes into a line buffer; the EN routine at $8490
shifts 1bpp glyphs into a 16-byte buffer pixel by pixel (`LSR`/`ROR $03C8,X`) and advances by a per-character width.
That is a proper VWF on an NES, added just for the translation [code].

Portraits used by `03 f` [code, rendered `build/research/cx/cx-text/faces_en.png`]: 00 Rock, 01 Dr. Light, 02 Roll,
03 Ultraman (black silhouette), 04/08 Guts Man, 05 the player's **Fake Rockman** (Rock's face, other palette),
06/07 Quick Man, 09 a masked robot, 0A/0B a two-part robot, 0C Dr. Light (stern), 0D Dr. Light (furious),
0E Dr. Light (beaten).

## 2. The script, in order

### 2.1 Story crawl (attract mode) [seen]

| EN (verbatim, including the typo) | JP | JP gist |
|---|---|---|
| In the year of 20XX, Dr. Light is appriciated by defeating the evil | 20XX年 ー Dr.ライトはナゾの科学者 Dr.ワイリーの野望を阻止したことを認められ | 20XX: Dr. Light is recognised for stopping the plans of the mysterious scientist Dr. Wily, |
| desire of Dr. Wily. His robots are world-famous. | 彼の造るロボットは世界的に信頼されるようになっていた。 | and the robots he builds came to be trusted all over the world. |
| While Dr. Wily thinks he can win if he creates many robots of only one kind. | 一方、Dr.ワイリーは1 VS 複数に持ちこめば、Dr.ライトを倒せると考えていた。 | Meanwhile Wily thought: if he can make it **1 VS many**, he can beat Light. |
| Thus, a new fake Mega Man has been sent out to the world... | こうして、新たにロボットが大量生産され、世に送りだされたのだった……。 | And so new robots were **mass-produced** and sent out into the world... |

The JP crawl is the readme joke ("We lose because we fight 8 vs 1!") stated straight: the whole series is reframed as
Wily losing on numbers. "ナゾの科学者 Dr.ワイリー" quotes the phrasing of the original Rockman 2 manual/opening.

### 2.2 Opening stage: Guts Man captures you [seen]

Cutscene box at the top of the screen, gray Fake Rockman on the left, Guts Man on the right
(`build/research/cx/cx-scout/guts.png`, `build/research/cx/cx-text/guts_jp.png`):

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Fake Rockman | Hey, Guts Man, what are you doing? | きみは ワイリーはかせが気に入っているガッツマンじゃないか。 | Aren't you Guts Man, the one Dr. Wily is so fond of? |
| (Guts Man throws a boulder; you are buried in rubble) | | | |
| Guts Man | You're far too unaware, gray man. I'm a member of Dr. Light Numbers. | 油断したようだな ワシはDr.ライトナンバーズの一員だ。 | You let your guard down. I'm one of the Dr. Light Numbers. |
| Guts Man | Now you're captured. | 悪いが お前をつかまえる。 | Sorry, but I'm taking you in. |

Joke: in Rockman 1 Wily stole Guts Man because he wanted him for construction, and his RM2 Guts Dozer is a Guts Man
tribute. The JP line plays on that ("the Guts Man Wily likes"). "Gray man" is the mass-produced Fake Rockman's palette.

### 2.3 Dr. Light's fortress dialogue (26 scripts)

Script numbers are the index in the pointer table. EN and JP were written separately: JP is the original, EN is a loose
(sometimes meme-ified) rewrite, so the JP gist column matters. **Bold** = highlight colour in EN.

**s00 - Light's lab is attacked** (Light stage 1 start, room $19 [seen: dialogue logger])

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Roll | W...Wily UFO is here! / It's heading towards us! | ワ、ワイリーはかせのUFOが来ました！ / まっすぐこちらへ向かってきます！！ | W-Wily's UFO is here! Heading straight for us! |
| Dr. Light | Soldiers near him, / assume combat mode! | 付近の者はただちに戦闘準備をしたまえ！！ / 戦闘力のない者は避難せよ！！ | Everyone nearby, prepare for battle! Non-combatants, evacuate! |
| Rock | Beware, they will come / over and over again... | 倒しても倒しても彼らはやってきます… / 注意してください…… | No matter how many we beat, they keep coming... be careful. |
| Dr. Light | Ultra Man, SMASH him. | ロックはまだ休んでおれ。 / …ウルトラマン、彼らをティウンさせなさい。 | Rock, you keep resting. ...Ultraman, **make them "tiun"**. |
| Ultraman | Dwah!! | デュワ！！ | (Ultraman's battle cry) |

"ティウン" (*tiun*) is the fan onomatopoeia for the Rockman death sound, used as a verb ("make them die"). The JP also
explains why Rock is not the hero: he is resting, so Light deploys Ultraman. The "they keep coming" line is the
mass-production premise: you are one of many identical units, and your lives are the horde.

**s01 - the spike counter**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | By the way, my spiky things seem / good at killing instantly. | ところで、あのウニみたいなやつ、いい具合に / 即死させることができるみたいじゃな？ | By the way, those sea-urchin things seem to kill instantly rather nicely, don't they? |
| Guts Man | They've got *N* kills. | *N*ティウンしたらしいぞい。 | Apparently *N* "tiuns" so far. |
| Dr. Light | Hmm... / Bring more spikes.  I guess we can / stop him. | ふーむ…………… / たーくさん置いておきなさい。彼らが通りそう / なところに、ぎっしりと詰めるのじゃ。 | Hmm... Put out lo-ots of them. Pack them tight wherever they're likely to pass. |

*N* is printed live by op `07`: **the game counts how many times you have died on spikes** and the villain comments on
it. Meta humour, and a justification for the spike density of the next stages.

**s02 - Light's "new friend"**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | Look who I found wandering around! / My friend here has a small problem with you. / It seems that you let him die and he's not too happy about that! | …わたしのロボットたちがお世話になっている / ようじゃのう。 / さて、君にどうしてもわたしの新しい仲間を / 紹介したいのじゃ。 | ...It seems my robots have been "well looked after" by you. Now, there's a new companion of mine I simply must introduce. |
| Fake Rockman | !? | ！？ | |
| Dr. Light | Now I think it is time that he / repays the favor! | まあ、楽しんでくれたまえ。 | Well, do enjoy yourself. |

The new friend is **Quick Man** (RM2's DWN-012), rebuilt by Light. EN adds "you let him die": Wily abandoned him after
RM2.

**s03 - Quick Man wakes up**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Fake Rockman (EN) / Quick Man (JP) | Quick Man... Do you remember me...? | どうやら、悪い夢を見ていたようだ……… | (QM) Looks like I was having a bad dream... |
| Quick Man (EN) / Fake Rockman (JP) | Yea... I guess so... / Sorry to cause you so much trouble. | クイックマン！ / お前には、ずいぶん迷惑をかけたみたいだな。 | (FR) Quick Man! (QM) Seems I caused you a lot of trouble. |
| Fake Rockman | Go back to our lab first! | まずは研究所に戻ろう！話は後だ！ | Back to the lab first! We'll talk later! |
| Fake Rockman | (Can't I teleport...!?) | テレポートができない……！？ | I can't teleport...!? |

Between the last two lines the script runs four far calls that play the teleport-out animation and fail (the fortress
blocks teleporting) [code: `09 5F B8 24`, `09 77/96/A9 B8 24`].

**s04 - Quick Man joins**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Quick Man | Let's split out. / Call me in the menu if you need help. | 二手に分かれて勢力を分散させるぞ！！ / 必要な時はサブメニューから呼び出してくれ！ | Let's split up and divide their forces! Call me from the sub-menu when you need me! |

This is the in-story unlock of the second playable character (Quick Man, swapped in from the pause menu) [doc/text].

**s05 - "We're now SERIOUS"**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Guts Man | There's a short circuit zap!! / Our base's gonna ruin!! | ろ、ローデンを起こしているでガス！ / もうダメでガス！ | Th-there's a current leak, -degasu! We're done for, -degasu! |
| Dr. Light | Don't worry, Guts. / ...We're now **SERIOUS**. | わざと漏電させているのじゃ。 / ……こちとら / マ / ジじゃからのう。 | I'm leaking current **on purpose**. ...Because we're dead "ma... ji" (serious) here. |

"でガス" (*-degasu*) is Guts Man's verbal tic, a pun on *-desu* + "Guts". Light deliberately electrifies his own base;
the JP stretches "マジ" (slang for "serious") over two box-closes for comic timing, which the EN reproduces with the
highlight colour.

**s06 - Guts Tank** (two variants chosen by `0C SKIP` after the which-hero call `$24:B5BF`)

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Guts Man (variant A) | Whoa!! / You should be in our clocktower...! | あ！ / こいつはさっき時計塔に / 閉じ込めたはずの…！ | Ah! This one should be locked up in the clock tower...! |
| Guts Man (variant B) | I've lost you once... / Not again... | ……あの時つかまえ損ねたニセロックマンが、 / ここまでたてつくとは……… | ...The fake Rockman I failed to catch back then, defying us this far... |
| Guts Man | I'm going to STOP you with... / The Fierce Dr.Light's Guts Tank!! | こうなったら、博士特製のガッツタンクで / 全力でひねり潰してやるでガス！！ | Then I'll crush you with all my might in the Doctor's special **Guts Tank**, -degasu!! |

Guts Tank is the Wily Castle 3 boss of Rockman 2, here rebuilt as a Light weapon. The "clock tower" refers to where
you were locked up after the opening capture.

**s23 - Guts Tank defeated**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Guts Man | Where... did that... power come from...!? / Arrrggghhh!!! | お…お前のどこに……そんな力が………… / ぐわあああああああ！！ | W-where in you... did such power... GWAAAAAH!! |

"お前のどこにそんな力が" is the stock anime "where did you get that strength" line (a *Dragon Ball*/*Hokuto no Ken*
style defeat cliché).

**s07 - the masked robot** (variant per hero)

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| masked robot (vs Quick Man) | You're, um...the robot master who inherits me? / You look weird... | お前が、その…………わたしを受けついだ / ロボットか。ヘンなツノなんかつけて………。 | So you're... the robot who **inherited** me. Wearing some weird horn... |
| Quick Man | Shut up, you are. | お前こそ、ヘンな仮面をつけているじゃないか。 | Says you, with that weird mask on. |
| masked robot | You are. | ………ふん。それならどっちがヘンか、 / ハッキリさせようではないか。 | ...Hmph. Then let's settle which of us is weird. |
| masked robot (vs Fake Rockman) | You finally got here. / This is the fourth / "Dr.Light's Sanctuary location. / It's ours now. / Take it from us, if you dare... | よく、きた。 / しかし、ここは「わたしの場所」だ。 / うばい取ってみよ。 / …………できるものなら。 | Welcome. But this is "my place". Try and take it... if you can. |

The EN "Shut up, you are." / "You are." is a schoolyard "no, you" exchange. ("fourth" = the fourth fortress stage.)

**s09 - the two-part robot**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| part A | I might be weak... | ひとりでダメなら…… | If one of us is no good... |
| part B | **But we are strong!** | 2人がかりでどうだ！！ | ...how about two at once!! |

**s08 - Light sends his "pet"**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | Welcome!  I see you destroyed my lab by yourself. / Very impressive! / I could destroy you, but I would not rob my pet of that pleasure. / He knows how to deal with wastes. / Should you live, I will be waiting for you.  Don't disappoint me! | フフフ…キミはすばらしいよ。 / この短時間でここまでわたしの研究所を / 荒らして回るとは…………実にすばらしい。 / さてと、すぐにでもわたしとお手合わせ / 願いたいのだが、あいにく…こいつがそれを / 許してくれなくてねえ。なにしろ、 / いつもは研究所のゴミ出し担当なのでね…… / しばらくしても、こいつが戻ってこないよう / なら、キミと試合をすることにしよう。では、 / 楽しみにしているぞ。 / ハハハハハ……… | Fufufu... you're wonderful. To wreck my lab this far in so little time... truly wonderful. I'd love a match with you right away, but unfortunately... this fellow won't allow it. After all, he's normally the lab's **garbage-disposal duty**... If he doesn't come back after a while, I'll have that match with you. Looking forward to it. Hahahaha... |

Light is written as a classic Wily-style villain, complete with the boss-taunt monologue.

**s10 - Light, round 1: the Three Laws** (runs right after s08; JP reuses s08's glyph pages)

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | Excellent job! / But, the time of **your destruction** has arrived! / And you cannot hurt me... | ……………………。 / では、約束どおりキミを殺すことにしよう。 / そして、キミはわたしを傷つけることは / できない…… / さて、どうするかね？ | ...... Then, as promised, I shall kill you. And you **cannot harm me**... So, what will you do? |
| Dr. Light (stern) | How will you survive? | (same page) | |
| Dr. Light | Welp, you defy The Three Laws of Robotics? | ……キミはロボット三原則すら守れないような / ロボットなのかね？ | ...Are you a robot that can't even obey the **Three Laws of Robotics**? |
| Dr. Light (stern) | Dangerous robots like you... | そんな危険なモノはね………… | Something that dangerous... |
| Dr. Light (furious) | AREN'T NEEDED IN THIS PEACEFUL WORLD!! / I   D E S T R O Y   Y O U ! ! | この平和な世界には必要ないのじゃ！！ / わしがこの手で八つ裂きにしてやるわ！！ | ...is NOT NEEDED in this peaceful world!! I'll tear you limb from limb with my own hands!! |

The Asimov joke: a robot may not harm a human, so Light "wins" by definition; when you fight back, you are the
dangerous one. Light's switch from わたし (polite) to わし (old-man) marks his snap into rage.

**s11 - "a law of nature"**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | You listening?  Okay. / Grass grows, | ……非常にカンタンな、自然の摂理じゃ。 / 草木が生え | ...It's a very simple law of nature. Grass grows, |
| Dr. Light (stern) | birds fly, sun shines, / and... | 、鳥が飛び、日が差して……… | birds fly, the sun shines... |
| Dr. Light | I crash you. | そして、わたしはお前をブチのめす。 | ...and I beat you to a pulp. |

This is the Scout's line from *Team Fortress 2*'s **"Meet the Scout"** ("Grass grows, birds fly, sun shines, and
brother, I hurt people."), in both languages. TF2 is the hack's house reference (ÜBERCHARGE, DEAD RINGER).

**s12 - "if you could just... that'd be great"** (Yes/No choice, `09 F9 AE 24`)

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light | So, if you could just do me a favor and off yourself, that'd be great. / Yes  No | ところで、せっかくだから自分から死んで / みようという気はないかな？ / いや、そうしてくれるとわたしが楽なのじゃ。 / たのむよ。 | By the way, since you're here, how about dying by your own hand? It'd make things easy for me. Please. |
| Dr. Light (Yes) | Thanks, pumpkin. | そう。それでいいのじゃよ。 | Yes. That's a good boy. |
| Dr. Light (No) | No...? / Since when have you thought you can say no? | そうか………それなら、 / わしが手にかけるしかないか………。 | I see... then I'll just have to do it myself... |

EN turns Light into **Bill Lumbergh from *Office Space*** ("Yeah, if you could just... that'd be great"). The Yes branch
presumably kills the player (to verify).

**s13 - "on days like these"**

| Speaker | EN | JP | JP gist |
|---|---|---|---|
| Dr. Light (stern) | it's a beautiful day outside. / birds are singing, flowers are blooming... / on days like these, scraps like you... | ………外はとてもよい天気じゃぞ。 / 鳥は歌って、花も咲いて、 / そして、キミみたいなポンコツは………… | ...It's lovely weather outside. Birds are singing, flowers are blooming, and junk like you... |
| Dr. Light | Should be burning in hell. | ……………………こうじゃ。 | ...... gets **this**. |

Verbatim **Sans** from *Undertale*'s genocide-route fight ("it's a beautiful day outside. birds are singing, flowers are
blooming... on days like these, kids like you... Should be burning in hell."), lower case included. It ties to the
readme's "a terrible bad time awaits" [doc]. The JP ends on a bare "...this." followed by the attack.

**s14 / s15 / s16 / s17 - Light's capsules and gifts**

| Script | Speaker | EN | JP | JP gist |
|---|---|---|---|---|
| s15 | Dr. Light | So you want to get more power from me, eh? / If not, too bad - I'm giving you anyway. | またわしの技を受けたいっていうんですかい？ / ま、いやだといっても受けさせますがねえ。 | So you want to take my technique again, huh? Well, even if you say no, I'm making you take it. |
| s14 | Dr. Light | No problem. | うむ。問題なし。 | Mm. No problem. |
| s16 | Dr. Light | So you've come... I hope not to want to fight anymore... | はあ…………… / やはりまた、来てしまったか………。 / できればわたしは、もう戦いたくないのだが… / これも運命なのかのう………。 | Sigh... so you came again after all. If I could, I'd rather not fight anymore... is this fate too? |
| s16 | Dr. Light | Well, step into this capsule. / and receive a mid-air acceleration system to boost your mobility. / Good Luck! | さて、カプセルに入るのじゃ。 / そうすれば、お前は空中でダッシュすることが / できるようになるはずじゃ。 / つらいことも多かろうが、がんばるのじゃぞ。 | Now, step into the capsule. Then you should be able to **dash in mid-air**. It will be hard, but do your best. |
| s16 | Dr. Light | Step into capsule? / Yes  No | カプセルに、入りますか？ | Enter the capsule? |
| s16 (No) | Dr. Light | Okay, I'll go back to **my job**. | ………………こんなところじゃろう。 / では、仕事に戻らねばな。 | ...That'll do. Well, back to work. |
| s17 | Dr. Light | I teach you something good. / You must defeat my Dragon Punch to stand a chance! | お前にいいことを教えてやろう。 / 昇龍拳を破らぬ限り、お前に勝ち目はない！！ | Let me tell you something good. Unless you break my **Shoryuken**, you have no chance!! |

The *Mega Man X* capsule gag turned inside out: Light's hologram capsules in X give X his armour; here Light, the enemy,
sighs "is this fate?" and gives the *Fake Rockman* an **air dash**. s17 cites the hidden *X* **Hadouken/Shoryuken**
capsules (Light in a Ryu gi), but as a boss threat. Placement of s14/s15 [to verify].

**s18-s22, s24, s25 - Light, the final fights**

| Script | Speaker | EN | JP | JP gist |
|---|---|---|---|---|
| s18 | Dr. Light | Great, another dead Mega Man-shaped robot... / ......Wait a minute, it's not dead! / YES!  I must make it die! | またロックの形をしたガラクタか……… / ワイリーも忙しくしているようじゃのう。 / ………うん？おぬし生きておるな！？ / こりゃわしが本当にガラクタにしなければな。 | Another piece of Rock-shaped junk... Wily's keeping busy, I see. ...Hm? You're alive!? Then I really must turn you into junk. |
| s19 | Dr. Light | You have destroyed so much. / What is it exactly, that you have created? / Can you even name one thing? / ......I thought not. / I guess you are useless. / So, let's finish your whole life. | キミは本当に多くのものを壊してきたが… / ところで、キミが作り出したものは何だ？ / 1つでもあるのか？…………ないだろう。 / そんなものはムダでしかない。 / すぐにでもわしが処分してやろう。 | You've destroyed so much... but what have you created? Even one thing? ...No. Something like that is pure waste. I'll dispose of you right now. |
| s19 | Dr. Light | I have laid the foundation for robotics, | ちなみにわたしにはあるぞ。わたしはロボット / 工学の基礎を確立させた。 | I, for the record, have: I founded robot engineering. |
| s19 | Dr. Light (stern) | and not as we have narrowly defined ourselves, / but as something greater than we could ever imagine. | それも、ロボットの可能性を限定する方向に / ではなく、想像を超えて大いなるものへと成長 / できるように……………だ。 | And not so as to limit what robots can be, but so they can grow into something greater than imagination... |
| s19 | Dr. Light | My robots will become something we can only now begin to glimpse. | わたしのロボット三原則に則ったロボットはね、 / 現時点では予想すらできないような大いなる / 存在に、なれるのだよ。 | Robots that follow my **Three Laws** can become great beings we can't even predict today. |
| s20 | Dr. Light | You think I'm professional of creating robots, but also expert of destroying. / Let's show you how I do. | わたしはロボットを作る人だと思われている / ようだが、実はロボットを壊す方法についても / よく知っているのじゃよ。それを今から / キミに教えてやろう。 | People think I'm the man who builds robots, but I know a great deal about breaking them too. Let me show you. |
| s24 | Dr. Light | Heh heh heh... / You respawn repeatedly / while I heal myself permanently. / How amazing story! | ふふふふふ……… / お前は無限に復活してわたしを追い詰める。 / そして、わたしもまた、無限に回復してお前を / 追い詰める。最高のシナリオだと思わんかね？ | You revive endlessly and corner me. And I recover endlessly and corner you. Isn't that the best scenario? |
| s21 | Dr. Light (stern/beaten) | *Cough* *cough* ...I am defeated... / I have no choice...... *cough* / but to throw myself... on your... / MERCY! | ゲホッ…ゴホッ…あわれむが、よい……ゴホッ / わしはもう、ダメじゃ……………… / 土下座して……お許しこいます…………！ | *cough* *cough* ...pity me... *cough* I'm finished... I prostrate myself... and beg forgiveness...! |
| s21 | hero (Fake Rockman or Quick Man, `0C` picks the face) | That's right, Dr.Light! / Your justice is finally... | ……………………分かった！ / もうわれわれの計画のジャマをしないのならば | ......All right! If you'll stop getting in the way of our plans... |
| s21 | Dr. Light | Phew, it was worth a shot. | ………ふう、あぶないところじゃった。 | ...Phew, that was a close one. |
| s21 | hero | We will capture you! | 逃がさないぞ！Dr.ライト！ | You won't get away, Dr. Light! |
| s21 | Dr. Light | Remember, you are still in my lab. | ……………… / ここはわたしの研究所だ。忘れないように。 | ...This is my lab. Don't forget that. |
| s22 | Dr. Light (stern) | Escaping does not only mean that I keep a distance from you. | わたしがキミから遠ざかることだけを / 「逃げる」というのではないのだよ。 | "Running away" doesn't only mean getting further from you. |
| s25 | Dr. Light (beaten) | Awww, it cannot be... | こ、こんなはずでは…………… | Th-this can't be... |
| s25 | hero | The war is now over. | もう、おしまいだ。Dr.ライト。 | It's over, Dr. Light. |
| s25 | Dr. Light (stern) | Ha!  I have the last plan... / It is... | なにをバカなことを……… / よおし、こうなったら…………… | What nonsense... Right, in that case... |
| s25 | Dr. Light (furious) | to become much bigger! | こうなったら、大きくなってやる！！！！ | In that case, I'll get **BIG**!!!! |

Series in-jokes: s21 is the **Wily dogeza** (every classic ending has Wily kneeling and begging), done by Light, who then
escapes exactly as Wily always does. s19 paraphrases Light's message to the future from *Mega Man X* (X's capsule
letter about unlimited potential and the risks of the Three Laws). s24 is a jab at the player's infinite continues.
s25 "get bigger" sets up the giant final form.

## 3. Menus and fixed UI text

Pause menu (bank $1F `0x3e380`) [code]: `MEGAMAN` (JP `ROCKMAN`) header, `MEGA BUSTER` (JP `ROCK BUSTER`),
`CHEAT SABER`, `RIDER KICK`, `DEAD RINGER`, `POWER BOMB`, `RINGO SHIELD`, `1.FLOOR`, `FIRE BALL`, `2.SUBTANK`,
`PRINT CUTTER`, `3.ÜBERCHARGE` (tile $1C is the Ü) [to confirm on screen].

(Title, NEW GAME / LOAD GAME, DATA 1-3, stage select, weapon get, game over: being added.)

## 4. Ending: boss roll call and staff roll [code]

Boss roll call (`0x24500`), EN / JP:

| EN | JP | Credit |
|---|---|---|
| DLN.001 MEGAMAN | DRN.001 ROCKMAN | CAPCOM |
| DLN.009 YOSHINOMAN | DRN.009 YOSHINOMAN | HIMAJIN JICHIKU |
| DLN.010 CHEATMAN | DRN.010 CHEATMAN | HIMAJIN JICHIKU |
| DLN.011 AIRMAN | DRN.011 AIRMAN | HIMAJIN JICHIKU |
| DLN.012 FIREMARIO | DRN.012 FIREMARIO | NINTENDO |
| DLN.013 KAMEN RIDER | DRN.013 仮面 RIDER (3 kanji tiles $4C-$4E) | ISHINOMORI PROD. |
| DLN.014 BOMBERMAN | DRN.014 BOMBERMAN | HUDSON SOFT |
| DLN.015 WHISPYWOODS | DRN.015 WHISPYWOODS | HAL LABORATORY |

The numbering is canon-aware: Light's robots in Rockman 1 are DLN-001 (Rock) through DLN-008 (Elec Man), so CX's new
Light robots continue at 009. JP writes **DRN** because Light's Japanese name is "Dr. Right". Air Man, a Wily robot in
RM2, is re-registered as a Light Number "by Himajin Jichiku".

Staff roll (`0x24c40`, 88 strings): first the **original Rockman 2 staff** kept from the vanilla ending ("original
megaman2 staff": CHARACTER DESIGNER YASUKICHI, INAFKING, TOM PON, NAGINEKO, 2M03CM MAN, A.K; sound programmer OGERETSU
KUN, MANAMI IETEL, YUUKICHAN&S PAPA; PROGRAMMER H.M.D.; PLANNER A.K; then the long vanilla special-thanks list ending in
FISH MAN), then **"megaman cx staff"**: SPECIAL THANKS PROUDMAN, PROETE, ROCK5EASILY, BAD DUMMY; SPECIAL THANKS ENSIS,
**PURESABE** (author of *Rockman 4 Minus Infinity*), NARFNRA, COLASAUR; SPECIAL THANKS ALL BETA TEST PLAYERS. AND YOU..;
HACKED BY (logo tiles); original megaman2 presented by capcom. JP differs only in "rockman2"/"rockman cx".

## 5. Jokes and references (summary, being extended)

| Line | Reference |
|---|---|
| 1 VS 複数 / mass production | the readme's "we lose because we fight 8 vs 1" |
| ティウン as a verb (s00, s01) | fan onomatopoeia for the Rockman death jingle |
| spike kill counter (s01) | meta: the game counts your spike deaths |
| でガス (s05, s06) | Guts Man's verbal tic |
| Guts Tank (s06) | RM2 Wily stage 3 boss, now Light's |
| Three Laws (s10, s19) | Asimov; *Mega Man X* backstory |
| "that'd be great" (s12) | *Office Space* (Lumbergh) |
| "it's a beautiful day outside" (s13) | *Undertale* (Sans) |
| capsule + air dash (s16) | *Mega Man X* Light capsules |
| Dragon Punch / 昇龍拳 (s17) | *Street Fighter* via *Mega Man X* |
| dogeza (s21) | every classic Wily surrender |
| DEAD RINGER, ÜBERCHARGE | *Team Fortress 2* (Spy watch, Medic) |

## 6. Hidden and unused text

- Three branch texts live in gaps between scripts and are only reached through `0C SKIP`: s07 (vs Fake Rockman), s12
  (No), s16 (No) [code]. All three are reachable, so they are variants, not unused text.

## Lessons for Rockman 6 GP

(being written)
