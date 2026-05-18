"""
phoneme_data.py — Complete GA English phoneme inventory
========================================================
16 vowels (11 monophthongs + 5 diphthongs) and 24 consonants.
Each entry contains articulation description, Mandarin-speaker
difficulty notes, common substitution error, minimal pairs,
and two shadowing practice sentences.

difficulty: 1 (easy) → 5 (very hard) for Mandarin speakers
"""

# ── Vowels ────────────────────────────────────────────────────────────────────

VOWELS = [
    # ── Close vowels ──────────────────────────────────────────────────────────
    {
        "symbol": "iː",
        "ipa": "/iː/",
        "label": "feet",
        "row": "close", "col": "front",
        "type": "monophthong",
        "difficulty": 2,
        "artic_en": (
            "Tongue is high and pushed toward the front of the mouth. "
            "Lips are spread wide, as if smiling. "
            "Hold the sound longer than you think — the length is part of the vowel."
        ),
        "artic_zh": "舌位高且靠前，嘴唇向两侧展开，类似微笑的嘴型。这个音要比你以为的持续更长——时长本身就是这个元音的组成部分。",
        "hard_en": (
            "Similar to Chinese 衣 (yī), but more tense and noticeably longer. "
            "Mandarin speakers often shorten it to sound like /ɪ/, making 'feet' sound like 'fit'."
        ),
        "hard_zh": "与汉语「衣」(yī)相似，但更紧张、明显更长。普通话母语者常将其缩短，使「feet」听起来像「fit」。",
        "substitution": "/ɪ/",
        "sub_note_en": "Shortened and laxed — the vowel becomes too brief.",
        "sub_note_zh": "缩短且松弛——元音变得过于简短。",
        "pairs": [("feet", "fit"), ("sheep", "ship"), ("beat", "bit"), ("leave", "live")],
        "practice": [
            "She needs to keep the green team clean.",
            "We agreed to meet by the sea each week.",
        ],
    },
    {
        "symbol": "ɪ",
        "ipa": "/ɪ/",
        "label": "fit",
        "row": "close", "col": "front",
        "type": "monophthong",
        "difficulty": 3,
        "artic_en": (
            "Tongue is slightly lower and more central than for /iː/. "
            "Lips are relaxed, not spread. "
            "The sound is short and lax — do not lengthen it."
        ),
        "artic_zh": "舌位比/iː/略低、略靠中央，嘴唇放松，不要向两侧展开。这个音短而松弛——不要拉长它。",
        "hard_en": (
            "Mandarin has no lax/tense vowel distinction. "
            "Speakers tend to produce /iː/ instead, making 'ship' sound like 'sheep'."
        ),
        "hard_zh": "普通话没有松/紧元音之分。母语者倾向于发成/iː/，使「ship」听起来像「sheep」。",
        "substitution": "/iː/",
        "sub_note_en": "Over-tensed and lengthened — the vowel becomes too prominent.",
        "sub_note_zh": "过于紧张且拉长——元音变得过于突出。",
        "pairs": [("fit", "feet"), ("ship", "sheep"), ("bit", "beat"), ("sit", "seat")],
        "practice": [
            "This film is filled with interesting images.",
            "He quickly picked a big ticket for the trip.",
        ],
    },
    {
        "symbol": "e",
        "ipa": "/e/",
        "label": "bed",
        "row": "mid", "col": "front",
        "type": "monophthong",
        "difficulty": 2,
        "artic_en": (
            "Tongue is mid-front, lower than for /ɪ/. "
            "Mouth is open about a finger's width. "
            "Lips are slightly spread, not rounded."
        ),
        "artic_zh": "舌位中前，比/ɪ/稍低，嘴巴张开约一指宽，嘴唇略微展开，不要圆唇。",
        "hard_en": (
            "Similar to the Chinese 诶, but shorter and more consistently mid. "
            "Common errors include raising it to /ɪ/ or lowering to /æ/."
        ),
        "hard_zh": "与汉语「诶」相似，但更短且位置更稳定。常见错误是将其抬高至/ɪ/或降低至/æ/。",
        "substitution": "/æ/ or /ɪ/",
        "sub_note_en": "Either too open (like 'cat') or too close (like 'fit').",
        "sub_note_zh": "要么开口太大（像「cat」），要么开口太小（像「fit」）。",
        "pairs": [("bed", "bad"), ("set", "sat"), ("men", "man"), ("net", "nat")],
        "practice": [
            "Let's get ready to head to bed at ten.",
            "Ten well-dressed men left the shed together.",
        ],
    },
    {
        "symbol": "æ",
        "ipa": "/æ/",
        "label": "cat",
        "row": "open-mid", "col": "front",
        "type": "monophthong",
        "difficulty": 4,
        "artic_en": (
            "Tongue is low and pushed to the front. "
            "Drop your jaw wide — this needs more opening than most English vowels. "
            "Lips spread wide, almost in a grin."
        ),
        "artic_zh": "舌位低且靠前，下颌需大幅下落——比大多数英语元音开口更大。嘴唇向两侧大幅展开，几乎像咧嘴笑。",
        "hard_en": (
            "This vowel does not exist in Mandarin. "
            "Speakers typically substitute /e/ (not enough jaw drop), "
            "making 'bad' sound like 'bed'."
        ),
        "hard_zh": "这个元音在普通话中不存在。母语者通常用/e/代替（下颌下落不足），使「bad」听起来像「bed」。",
        "substitution": "/e/",
        "sub_note_en": "Jaw doesn't drop far enough — the vowel sits too high.",
        "sub_note_zh": "下颌下落不足——元音位置太高。",
        "pairs": [("cat", "cut"), ("bad", "bed"), ("man", "men"), ("hat", "hot")],
        "practice": [
            "That bad man grabbed a black backpack and ran.",
            "Can you plan a camping trip to Japan in January?",
        ],
    },
    # ── Back vowels ───────────────────────────────────────────────────────────
    {
        "symbol": "ɑː",
        "ipa": "/ɑː/",
        "label": "father",
        "row": "open", "col": "back",
        "type": "monophthong",
        "difficulty": 2,
        "artic_en": (
            "Tongue is low and pushed to the back. "
            "Mouth is wide open — say 'ah' when a doctor checks your throat. "
            "Lips are unrounded and relaxed."
        ),
        "artic_zh": "舌位低且靠后，嘴巴大张——就像医生检查喉咙时发「啊」的感觉。嘴唇不圆，自然放松。",
        "hard_en": (
            "Similar to Chinese 啊 (ā). "
            "The main error is producing /æ/ instead — not pushing the tongue back far enough."
        ),
        "hard_zh": "与汉语「啊」(ā)相似。主要错误是发成/æ/——舌头没有足够地向后退。",
        "substitution": "/æ/",
        "sub_note_en": "Tongue stays front instead of moving to the back.",
        "sub_note_zh": "舌头留在前方而没有移向后部。",
        "pairs": [("father", "feather"), ("calm", "come"), ("spa", "spear"), ("car", "care")],
        "practice": [
            "Her father started a large farm by the dark harbour.",
            "The calm, hard bark on the palm tree looked like art.",
        ],
    },
    {
        "symbol": "ɔː",
        "ipa": "/ɔː/",
        "label": "law",
        "row": "mid", "col": "back",
        "type": "monophthong",
        "difficulty": 3,
        "artic_en": (
            "Tongue is mid-back. "
            "Lips are rounded and pushed slightly forward. "
            "Mouth is fairly open — more than for /oʊ/."
        ),
        "artic_zh": "舌位中后，嘴唇圆且略向前突，嘴巴开口比/oʊ/更大。",
        "hard_en": (
            "Easily confused with /oʊ/ (closing too much) or /ɑː/ (opening too much). "
            "Chinese speakers sometimes replace it with a single Chinese o."
        ),
        "hard_zh": "容易与/oʊ/（闭合过多）或/ɑː/（开口过大）混淆。普通话母语者有时会用汉语的「哦」代替。",
        "substitution": "/oʊ/",
        "sub_note_en": "Mouth closes too much, adding a glide that shouldn't be there.",
        "sub_note_zh": "嘴巴闭合过多，产生了不该有的滑音。",
        "pairs": [("law", "low"), ("caught", "coat"), ("thought", "throat"), ("tall", "toll")],
        "practice": [
            "The audience applauded the astronaut's long walk.",
            "She thought the awful storm would cause a water shortage.",
        ],
    },
    {
        "symbol": "ʊ",
        "ipa": "/ʊ/",
        "label": "foot",
        "row": "close", "col": "back",
        "type": "monophthong",
        "difficulty": 3,
        "artic_en": (
            "Tongue is high-back but relaxed — not as far back or as high as /uː/. "
            "Lips are lightly rounded. "
            "Keep the sound short and unstressed."
        ),
        "artic_zh": "舌位高后但放松——不如/uː/那么靠后或那么高。嘴唇轻微圆润，保持这个音短且不重读。",
        "hard_en": (
            "Mandarin /u/ is closer to English /uː/. "
            "Speakers typically over-tense this vowel, making 'foot' sound like 'food'."
        ),
        "hard_zh": "普通话的/u/更接近英语的/uː/。母语者通常将这个元音过度紧张，使「foot」听起来像「food」。",
        "substitution": "/uː/",
        "sub_note_en": "Over-tensed and too long — the vowel is too pronounced.",
        "sub_note_zh": "过度紧张且太长——元音太突出了。",
        "pairs": [("foot", "food"), ("put", "pool"), ("book", "boot"), ("could", "cooed")],
        "practice": [
            "The cook stood by the wooden hook and looked.",
            "Would you put this good book on the full shelf?",
        ],
    },
    {
        "symbol": "uː",
        "ipa": "/uː/",
        "label": "food",
        "row": "close", "col": "back",
        "type": "monophthong",
        "difficulty": 2,
        "artic_en": (
            "Tongue is high and far back. "
            "Lips are strongly rounded and pushed forward. "
            "Hold the sound — it is a long vowel."
        ),
        "artic_zh": "舌位高且靠后，嘴唇有力圆拢并向前突出。持续发这个音——它是一个长元音。",
        "hard_en": (
            "Similar to Chinese 乌 (wū), but with stronger lip rounding and sustained longer. "
            "Most speakers handle this well, but may under-round the lips."
        ),
        "hard_zh": "与汉语「乌」(wū)相似，但嘴唇圆拢更有力且持续更长。大多数母语者掌握较好，但可能圆唇不足。",
        "substitution": "/ʊ/",
        "sub_note_en": "Lips not rounded enough — the sound is too lax.",
        "sub_note_zh": "嘴唇圆拢不足——音听起来太松弛了。",
        "pairs": [("food", "foot"), ("pool", "pull"), ("boot", "book"), ("moon", "mun")],
        "practice": [
            "Move the cool blue tool to the school room.",
            "Who knew the new moon would move through so soon?",
        ],
    },
    # ── Central vowels ────────────────────────────────────────────────────────
    {
        "symbol": "ʌ",
        "ipa": "/ʌ/",
        "label": "cup",
        "row": "open-mid", "col": "central",
        "type": "monophthong",
        "difficulty": 4,
        "artic_en": (
            "Tongue is mid-central, slightly lower than neutral. "
            "Mouth opens about a finger's width. "
            "Lips are unrounded and relaxed. "
            "It is a short, unstressed-sounding vowel even in stressed syllables."
        ),
        "artic_zh": "舌位中央偏低，嘴巴张开约一指宽，嘴唇不圆且放松。即使在重读音节中，这个音也听起来短促而不重读。",
        "hard_en": (
            "This sound does not clearly exist in Mandarin. "
            "Speakers often substitute /ɑː/ (too open and back) or /æ/ (too far front), "
            "so 'cup' ends up sounding like 'cap' or 'cop'."
        ),
        "hard_zh": "这个音在普通话中没有明确对应。母语者常用/ɑː/（过于开放和靠后）或/æ/（过于靠前）代替，导致「cup」听起来像「cap」或「cop」。",
        "substitution": "/ɑː/ or /æ/",
        "sub_note_en": "Either too far back (cop) or too far front (cap).",
        "sub_note_zh": "要么太靠后（cop），要么太靠前（cap）。",
        "pairs": [("cup", "cap"), ("cut", "cat"), ("love", "laugh"), ("come", "calm")],
        "practice": [
            "Some of us must adjust to sudden struggles.",
            "The young couple discovered enough trust to recover.",
        ],
    },
    {
        "symbol": "ɜː",
        "ipa": "/ɜː/",
        "label": "bird",
        "row": "mid", "col": "central",
        "type": "monophthong",
        "difficulty": 5,
        "artic_en": (
            "Tongue is mid-central. "
            "In General American, the tongue also curls back slightly (r-coloring). "
            "Lips are neutral, slightly rounded. "
            "This is a long, sustained sound — do not rush it."
        ),
        "artic_zh": "舌位中央，在美式英语中舌头还要稍微向后卷（r音色）。嘴唇自然放松，稍微圆拢。这是一个长音，不要急于结束。",
        "hard_en": (
            "No equivalent sound exists in Mandarin. "
            "The r-coloring is very different from Chinese retroflex sounds. "
            "Speakers often substitute /e/ or a Chinese 额 sound, "
            "making 'bird' sound like 'bed'."
        ),
        "hard_zh": "普通话中没有对应的音。r音色与汉语卷舌音完全不同。母语者常用/e/或汉语「额」来代替，使「bird」听起来像「bed」。",
        "substitution": "/e/ or Chinese è",
        "sub_note_en": "Tongue doesn't curl back — the r-coloring is missing entirely.",
        "sub_note_zh": "舌头没有向后卷——完全缺失了r音色。",
        "pairs": [("bird", "bad"), ("work", "walk"), ("heard", "had"), ("stir", "stay")],
        "practice": [
            "The nurse worked early every Thursday morning.",
            "Her first concern was turning words into clear verbs.",
        ],
    },
    {
        "symbol": "ə",
        "ipa": "/ə/",
        "label": "about",
        "row": "mid", "col": "central",
        "type": "monophthong",
        "difficulty": 4,
        "artic_en": (
            "Tongue is completely neutral — mid-central, no tension. "
            "Mouth is slightly open. "
            "This is the most common vowel in English, but it only appears in unstressed syllables. "
            "It is the sound of a syllable that is barely there."
        ),
        "artic_zh": "舌位完全中立——中央位，无紧张感。嘴巴微微张开。这是英语中最常见的元音，但只出现在非重读音节中。它是一个「几乎不存在」的音节的声音。",
        "hard_en": (
            "Mandarin is syllable-timed: every syllable gets roughly equal prominence. "
            "There is no equivalent to English schwa reduction. "
            "Speakers tend to give full vowel quality to unstressed syllables, "
            "making speech sound robotic and over-pronounced."
        ),
        "hard_zh": "普通话是音节计时语言，每个音节大致获得相同的突出程度。英语中的弱化元音在普通话中没有对应。母语者倾向于给非重读音节完整的元音质量，使语音听起来机械且过度咬字。",
        "substitution": "Full vowel (e.g., /æ/ for unstressed 'a')",
        "sub_note_en": "Every syllable is given full weight — schwa reduction never happens.",
        "sub_note_zh": "每个音节都被赋予完整的重量——弱化元音从未发生。",
        "pairs": [("a·BOUT", "—"), ("ba·NA·na", "—"), ("the (weak form)", "—")],
        "practice": [
            "A hundred people were waiting at the station.",
            "The teacher opened a window and entered the kitchen.",
        ],
    },
    # ── Diphthongs ────────────────────────────────────────────────────────────
    {
        "symbol": "eɪ",
        "ipa": "/eɪ/",
        "label": "day",
        "row": "diphthong", "col": "front",
        "type": "diphthong",
        "difficulty": 2,
        "artic_en": (
            "Start at the /e/ position (mid-front), "
            "then glide the tongue upward toward /ɪ/ (close-front). "
            "The first part is longer; the glide is brief."
        ),
        "artic_zh": "从/e/的位置（中前）开始，然后舌头向上滑向/ɪ/（高前）。前半部分更长，滑音简短。",
        "hard_en": (
            "Similar to Chinese 诶, but the glide movement is more pronounced in English. "
            "Speakers sometimes produce a single /e/ without the upward glide."
        ),
        "hard_zh": "与汉语「诶」相似，但英语中的滑动更明显。母语者有时只发一个/e/，没有向上的滑动。",
        "substitution": "Single /e/ (no glide)",
        "sub_note_en": "The vowel stays flat — the glide toward /ɪ/ never happens.",
        "sub_note_zh": "元音保持平稳——向/ɪ/的滑动从未发生。",
        "pairs": [("day", "die"), ("say", "sigh"), ("main", "mine"), ("late", "light")],
        "practice": [
            "They paid eight to stay at the great café.",
            "Take a break and wait — the plane may be late today.",
        ],
    },
    {
        "symbol": "aɪ",
        "ipa": "/aɪ/",
        "label": "time",
        "row": "diphthong", "col": "front",
        "type": "diphthong",
        "difficulty": 2,
        "artic_en": (
            "Start at an open /a/ position (low, unrounded), "
            "then glide up toward /ɪ/ (close-front). "
            "This is a wide-ranging diphthong — the movement is large."
        ),
        "artic_zh": "从开放的/a/位置（低，不圆唇）开始，然后向上滑向/ɪ/（高前）。这是一个跨度大的双元音——移动幅度很大。",
        "hard_en": (
            "Similar to Chinese 爱 (ài). "
            "Generally well-produced, but some speakers shorten the glide path, "
            "starting too high."
        ),
        "hard_zh": "与汉语「爱」(ài)相似。通常发音较好，但有些母语者会缩短滑动路径，起始位置过高。",
        "substitution": "Starting too high (closer to /eɪ/)",
        "sub_note_en": "The starting point is too high — the vowel doesn't open enough.",
        "sub_note_zh": "起始点太高——元音开口不足。",
        "pairs": [("time", "team"), ("night", "neat"), ("find", "fiend"), ("my", "me")],
        "practice": [
            "I tried to find a bright light on Friday night.",
            "The right idea arrived right on time — surprisingly.",
        ],
    },
    {
        "symbol": "ɔɪ",
        "ipa": "/ɔɪ/",
        "label": "boy",
        "row": "diphthong", "col": "back",
        "type": "diphthong",
        "difficulty": 3,
        "artic_en": (
            "Start at /ɔː/ (mid-back, rounded), "
            "then glide toward /ɪ/ (close-front). "
            "The starting position is rounded; the glide moves forward and up."
        ),
        "artic_zh": "从/ɔː/（中后，圆唇）位置开始，然后向/ɪ/（高前）滑动。起始位置圆唇，滑音向前且向上移动。",
        "hard_en": (
            "This diphthong is rare in Mandarin. "
            "Speakers sometimes replace it with /aɪ/ (wrong starting position) "
            "or a simple /ɔː/."
        ),
        "hard_zh": "这个双元音在普通话中很少见。母语者有时将其替换为/aɪ/（起始位置错误）或简单的/ɔː/。",
        "substitution": "/aɪ/ or /ɔː/",
        "sub_note_en": "Either wrong starting vowel or glide omitted entirely.",
        "sub_note_zh": "要么起始元音错误，要么完全省略滑音。",
        "pairs": [("boy", "bay"), ("voice", "vase"), ("coin", "cane"), ("oil", "ale")],
        "practice": [
            "The boy enjoyed the noise from the royal toy.",
            "She avoided the choice between boiling oil and foil.",
        ],
    },
    {
        "symbol": "aʊ",
        "ipa": "/aʊ/",
        "label": "now",
        "row": "diphthong", "col": "back",
        "type": "diphthong",
        "difficulty": 2,
        "artic_en": (
            "Start at an open /a/ (low, unrounded), "
            "then glide back and up toward /ʊ/ (close-back, rounded). "
            "Lips round as the glide progresses."
        ),
        "artic_zh": "从开放的/a/（低，不圆唇）开始，然后向后上方滑向/ʊ/（高后，圆唇）。随着滑音进行，嘴唇逐渐圆拢。",
        "hard_en": (
            "Similar to Chinese 凹 or the ao in 好 (hǎo). "
            "Usually well-produced. "
            "The error is starting too far back, closer to /oʊ/."
        ),
        "hard_zh": "与汉语「凹」或「好」中的ao相似。通常发音较好。错误是起始位置过于靠后，偏向/oʊ/。",
        "substitution": "Starting too back (closer to /oʊ/)",
        "sub_note_en": "The first vowel is too rounded and back — it starts too closed.",
        "sub_note_zh": "第一个元音太圆且靠后——起始位置过于封闭。",
        "pairs": [("now", "no"), ("house", "hose"), ("cow", "go"), ("out", "oat")],
        "practice": [
            "How loud is the sound of the crowd downtown?",
            "The brown cow was found around the south ground.",
        ],
    },
    {
        "symbol": "oʊ",
        "ipa": "/oʊ/",
        "label": "go",
        "row": "diphthong", "col": "back",
        "type": "diphthong",
        "difficulty": 3,
        "artic_en": (
            "Start at a mid-back /o/ with rounded lips, "
            "then glide up toward /ʊ/. "
            "Both parts involve rounded lips — maintain rounding throughout."
        ),
        "artic_zh": "从中后/o/（圆唇）位置开始，然后向上滑向/ʊ/。两部分都需要圆唇——全程保持圆唇。",
        "hard_en": (
            "Mandarin /o/ is typically a single steady vowel without the upward glide. "
            "Speakers produce a flat /o:/, missing the movement toward /ʊ/."
        ),
        "hard_zh": "普通话的/o/通常是一个稳定的单元音，没有向上的滑动。母语者会发出平坦的/o:/，错过向/ʊ/的滑动。",
        "substitution": "Single /oː/ (no glide toward /ʊ/)",
        "sub_note_en": "The vowel stays flat — the closing movement never happens.",
        "sub_note_zh": "元音保持平稳——闭合移动从未发生。",
        "pairs": [("go", "got"), ("home", "hum"), ("know", "now"), ("road", "rod")],
        "practice": [
            "Don't go home alone — phone before you go.",
            "Joe drove slowly down the old stone road alone.",
        ],
    },
]


# ── Consonants ────────────────────────────────────────────────────────────────

CONSONANTS = [
    # ── Stops ─────────────────────────────────────────────────────────────────
    {
        "symbol": "p",
        "ipa": "/p/",
        "label": "pin",
        "manner": "stop", "place": "bilabial", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "Press both lips together tightly, build up air pressure, "
            "then release with a small puff of air (aspiration). "
            "The aspiration — the brief burst of air — is most noticeable at the start of a stressed syllable."
        ),
        "artic_zh": "双唇紧闭，积累气压，然后带着一小股气流（送气）爆发释放。送气——短暂的气流——在重读音节开头最为明显。",
        "hard_en": (
            "Chinese pīnyīn p is aspirated, so initial /p/ is fine. "
            "The difficulty is in unstressed positions — English /p/ in 'stop' or 'happen' "
            "should not be aspirated, but speakers often add aspiration everywhere."
        ),
        "hard_zh": "汉语拼音p是送气音，所以词首/p/通常没问题。难点在非重读位置——「stop」或「happen」中的/p/不应送气，但母语者常处处送气。",
        "substitution": "/b/ (in unstressed positions)",
        "sub_note_en": "Sometimes devoiced inconsistently, or aspiration is misplaced.",
        "sub_note_zh": "有时清浊音不一致，或送气位置错误。",
        "pairs": [("pin", "bin"), ("cap", "cab"), ("pat", "bat"), ("rip", "rib")],
        "practice": [
            "Please put the apple pie on top of the plate.",
            "The price of paper products keeps popping up.",
        ],
    },
    {
        "symbol": "b",
        "ipa": "/b/",
        "label": "bin",
        "manner": "stop", "place": "bilabial", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "Press both lips together. "
            "Start your voice (vocal cord vibration) before releasing — "
            "that voicing is what distinguishes /b/ from /p/. "
            "No puff of air on release."
        ),
        "artic_zh": "双唇紧闭，在释放气流前就开始发声（声带振动）——正是这个浊音使/b/区别于/p/。释放时不带气流。",
        "hard_en": (
            "Chinese b (bā) is unvoiced and unaspirated — very different from English /b/. "
            "English /b/ requires vocal cord vibration. "
            "Speakers may produce a sound between /p/ and /b/, especially at the end of words."
        ),
        "hard_zh": "汉语拼音b（巴）是清音且不送气——与英语/b/很不同。英语/b/需要声带振动。母语者可能发出介于/p/和/b/之间的音，尤其是在词尾。",
        "substitution": "/p/ (devoiced)",
        "sub_note_en": "Vocal cords don't vibrate — the voiced quality is lost.",
        "sub_note_zh": "声带不振动——浊音特质丢失了。",
        "pairs": [("bin", "pin"), ("cab", "cap"), ("bet", "pet"), ("big", "pig")],
        "practice": [
            "Bob grabbed a big blue bag before boarding the bus.",
            "The baby's brown bear belongs on the big bed.",
        ],
    },
    {
        "symbol": "t",
        "ipa": "/t/",
        "label": "top",
        "manner": "stop", "place": "alveolar", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "Touch the tip of your tongue to the ridge just behind your upper front teeth "
            "(the alveolar ridge). "
            "Build up air, then release with aspiration at the start of stressed syllables. "
            "In fast speech, /t/ between vowels (like 'butter') often sounds like a quick /d/ tap."
        ),
        "artic_zh": "舌尖触碰上前牙后方的齿槽嵴，积累气流，然后在重读音节开头带送气释放。在快速语流中，两个元音之间的/t/（如「butter」）常听起来像一个快速的/d/闪音。",
        "hard_en": (
            "Chinese t is aspirated and alveolar, so initial /t/ presents few problems. "
            "The main difficulty is the flap rule in American English — "
            "'butter', 'water', 'better' all have a /d/-like tap that surprises learners."
        ),
        "hard_zh": "汉语拼音t是送气齿槽音，所以词首/t/通常没问题。主要难点是美式英语的闪音规则——「butter」「water」「better」都有一个类似/d/的闪音，常令学习者感到惊讶。",
        "substitution": "/d/ (word-finally, under-aspirated)",
        "sub_note_en": "Final /t/ is often devoiced correctly but unreleased — that is actually fine in English.",
        "sub_note_zh": "词尾/t/通常被正确清化，但不释放——这在英语中实际上是正确的。",
        "pairs": [("top", "dop"), ("cat", "cad"), ("ten", "den"), ("train", "drain")],
        "practice": [
            "Take the last train to the top of the tall hill tonight.",
            "Try not to talk too fast and keep the text tight.",
        ],
    },
    {
        "symbol": "d",
        "ipa": "/d/",
        "label": "dog",
        "manner": "stop", "place": "alveolar", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "Touch the tongue tip to the alveolar ridge — same position as /t/. "
            "Start vocal cord vibration before the release. "
            "No aspiration. Word-final /d/ is often unreleased."
        ),
        "artic_zh": "舌尖触碰齿槽嵴——与/t/相同的位置。在气流释放前开始声带振动。不送气。词尾/d/通常不释放。",
        "hard_en": (
            "Chinese d (dā) is voiceless and unaspirated — not the same as English /d/. "
            "English /d/ must be voiced. "
            "In word-final position, speakers often devoice it to sound like /t/."
        ),
        "hard_zh": "汉语拼音d（打）是清音不送气——与英语/d/不同。英语/d/必须是浊音。在词尾位置，母语者常将其清化，听起来像/t/。",
        "substitution": "/t/ (devoiced word-finally)",
        "sub_note_en": "Final /d/ becomes /t/ — 'bad' sounds like 'bat'.",
        "sub_note_zh": "词尾/d/变成/t/——「bad」听起来像「bat」。",
        "pairs": [("dog", "dock"), ("bad", "bat"), ("deed", "deet"), ("rid", "rit")],
        "practice": [
            "David decided to drive to the downtown district.",
            "Did he find the old red bed in the dark shed?",
        ],
    },
    {
        "symbol": "k",
        "ipa": "/k/",
        "label": "cat",
        "manner": "stop", "place": "velar", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "The back of the tongue rises to touch the soft palate (velum). "
            "Build up air behind this contact, then release with aspiration "
            "at the start of a stressed syllable."
        ),
        "artic_zh": "舌根抬起触碰软腭（软腭）。在触碰点后方积累气流，然后在重读音节开头带送气释放。",
        "hard_en": (
            "Chinese k is also aspirated and velar — very similar. "
            "Difficulty mainly arises in consonant clusters like 'sky', 'skill' "
            "where English /k/ is unaspirated."
        ),
        "hard_zh": "汉语拼音k也是送气软腭音——非常相似。难点主要出现在辅音丛中，如「sky」「skill」中的英语/k/是不送气的。",
        "substitution": "/g/ (in consonant clusters)",
        "sub_note_en": "Correct in isolation; cluster reduction is the more common error.",
        "sub_note_zh": "单独发音时正确；辅音丛简化是更常见的错误。",
        "pairs": [("cat", "gat"), ("lock", "log"), ("coat", "goat"), ("back", "bag")],
        "practice": [
            "Keep the black clock in the back of the kitchen.",
            "The cool silk jacket came back surprisingly quickly.",
        ],
    },
    {
        "symbol": "g",
        "ipa": "/g/",
        "label": "go",
        "manner": "stop", "place": "velar", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "Same position as /k/: back of tongue on the soft palate. "
            "Start vocal cord vibration before the release. "
            "No aspiration."
        ),
        "artic_zh": "与/k/相同的位置：舌根在软腭上。在气流释放前开始声带振动，不送气。",
        "hard_en": (
            "Chinese g (gā) is voiceless and unaspirated — English /g/ requires voicing. "
            "Speakers often devoice it, especially word-finally, so 'bag' sounds like 'back'."
        ),
        "hard_zh": "汉语拼音g（嘎）是清音不送气——英语/g/需要声带振动。母语者常将其清化，尤其在词尾，使「bag」听起来像「back」。",
        "substitution": "/k/ (devoiced)",
        "sub_note_en": "Voicing disappears — the sound becomes /k/.",
        "sub_note_zh": "浊音消失——声音变成了/k/。",
        "pairs": [("go", "co"), ("bag", "back"), ("big", "bick"), ("give", "cliff")],
        "practice": [
            "The green frog grabbed a big grey-gold bug.",
            "Greg's dog got good at guiding guests to the garden.",
        ],
    },
    # ── Fricatives ────────────────────────────────────────────────────────────
    {
        "symbol": "f",
        "ipa": "/f/",
        "label": "fan",
        "manner": "fricative", "place": "labiodental", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "Place your upper front teeth lightly on your lower lip. "
            "Force air through the gap — you should feel a stream of air on your hand. "
            "No voicing."
        ),
        "artic_zh": "将上前牙轻轻放在下唇上，强制气流通过间隙——你应该能感到气流吹到手上。不发声。",
        "hard_en": (
            "Chinese has /f/ in a similar position, so this is generally well-produced. "
            "Occasional confusion with /h/ (substituting throat friction for lip-teeth friction)."
        ),
        "hard_zh": "汉语有类似位置的/f/，所以通常发音较好。偶尔会与/h/混淆（用喉部摩擦代替唇齿摩擦）。",
        "substitution": "/h/ or /p/",
        "sub_note_en": "Teeth not placed on lower lip — friction is in the wrong place.",
        "sub_note_zh": "上牙没有放在下唇上——摩擦发生在错误的位置。",
        "pairs": [("fan", "van"), ("off", "of"), ("fine", "vine"), ("safe", "save")],
        "practice": [
            "The fan fell off the shelf after five minutes.",
            "She prefers fresh fruit for her afternoon coffee.",
        ],
    },
    {
        "symbol": "v",
        "ipa": "/v/",
        "label": "van",
        "manner": "fricative", "place": "labiodental", "voiced": True,
        "difficulty": 5,
        "artic_en": (
            "Exactly like /f/ — upper teeth on lower lip — but add voicing. "
            "Your vocal cords should vibrate while the air passes through. "
            "You can feel the vibration by touching your throat."
        ),
        "artic_zh": "与/f/完全相同——上牙放在下唇——但加上声带振动。气流通过时声带应振动。触摸喉部可感受到振动。",
        "hard_en": (
            "This sound does not exist in Mandarin. "
            "Speakers commonly substitute /f/ (removing the voicing), "
            "/w/ (replacing teeth-on-lip with rounded lips), "
            "or even /b/."
        ),
        "hard_zh": "这个音在普通话中不存在。母语者通常用/f/代替（去除声带振动），或用/w/代替（将牙-唇接触改为圆唇），甚至用/b/代替。",
        "substitution": "/f/ (most common), /w/ or /b/",
        "sub_note_en": "Vocal cords don't vibrate — 'very' sounds like 'ferry'.",
        "sub_note_zh": "声带不振动——「very」听起来像「ferry」。",
        "pairs": [("van", "fan"), ("vine", "fine"), ("vat", "fat"), ("veil", "fail")],
        "practice": [
            "Victor's vivid novel received five very positive reviews.",
            "The village evolved over several adventurous, eventful years.",
        ],
    },
    {
        "symbol": "θ",
        "ipa": "/θ/",
        "label": "think",
        "manner": "fricative", "place": "dental", "voiced": False,
        "difficulty": 5,
        "artic_en": (
            "Place the tip of your tongue between your upper and lower front teeth, "
            "or just behind the upper teeth. "
            "Force air through — you should feel air flowing over your tongue tip. "
            "No voicing."
        ),
        "artic_zh": "将舌尖放在上下前牙之间，或紧靠上齿后方。强制气流通过——你应该感到气流从舌尖流过。不发声。",
        "hard_en": (
            "Dental fricatives do not exist in Mandarin. "
            "Speakers almost universally substitute /s/ (tongue pulled back from teeth), "
            "/t/ (full stop instead of fricative), "
            "or /f/ (wrong place of articulation)."
        ),
        "hard_zh": "齿摩擦音在普通话中不存在。母语者几乎普遍用/s/（舌头从牙齿处缩回）、/t/（完全爆破代替摩擦）或/f/（发音部位错误）代替。",
        "substitution": "/s/ (most common), /t/ or /f/",
        "sub_note_en": "Tongue is not between or touching the teeth — the friction is wrong.",
        "sub_note_zh": "舌头没有在牙齿之间或触碰牙齿——摩擦位置错误。",
        "pairs": [("think", "sink"), ("three", "free"), ("math", "mass"), ("thin", "sin")],
        "practice": [
            "Thank the author for the thorough thought on the theme.",
            "Three months of therapy helped him think through everything.",
        ],
    },
    {
        "symbol": "ð",
        "ipa": "/ð/",
        "label": "this",
        "manner": "fricative", "place": "dental", "voiced": True,
        "difficulty": 5,
        "artic_en": (
            "Same position as /θ/ — tongue tip at the upper teeth — "
            "but add vocal cord vibration. "
            "This is the voiced version: 'this', 'that', 'the', 'them', 'there'."
        ),
        "artic_zh": "与/θ/相同的位置——舌尖在上齿处——但加上声带振动。这是浊音版本：「this」「that」「the」「them」「there」。",
        "hard_en": (
            "Same articulation challenge as /θ/ — no Mandarin equivalent. "
            "The most common substitution is /d/ (correct place but wrong manner) "
            "or /z/ (correct voicing, wrong place)."
        ),
        "hard_zh": "与/θ/有相同的发音挑战——普通话中没有对应音。最常见的替代是/d/（发音部位正确但方式错误）或/z/（浊音正确，部位错误）。",
        "substitution": "/d/ (most common), /z/ or /v/",
        "sub_note_en": "Tongue isn't at the teeth — a stop or wrong fricative replaces it.",
        "sub_note_zh": "舌头没有在牙齿处——爆破音或错误的摩擦音代替了它。",
        "pairs": [("this", "dis"), ("breathe", "breed"), ("then", "den"), ("they", "day")],
        "practice": [
            "This is the other method they decided to use.",
            "Their father would rather bathe together in the evening.",
        ],
    },
    {
        "symbol": "s",
        "ipa": "/s/",
        "label": "see",
        "manner": "fricative", "place": "alveolar", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "Tongue tip near (but not touching) the alveolar ridge. "
            "Force air through a narrow groove in the tongue — "
            "you hear a sharp hissing sound. "
            "Lips are slightly spread. No voicing."
        ),
        "artic_zh": "舌尖靠近（但不触碰）齿槽嵴，强制气流通过舌面上的窄沟——你会听到尖锐的嘶嘶声。嘴唇略微展开，不发声。",
        "hard_en": (
            "Chinese has a similar /s/. "
            "The main error is substituting /ʃ/ before high front vowels like /iː/ "
            "(saying 'she' instead of 'see')."
        ),
        "hard_zh": "汉语有类似的/s/。主要错误是在高前元音如/iː/前用/ʃ/代替（把「see」说成「she」）。",
        "substitution": "/ʃ/ before /iː/ or /j/",
        "sub_note_en": "Tongue moves too far back when followed by a front vowel.",
        "sub_note_zh": "在前元音前舌头移动过于靠后。",
        "pairs": [("see", "she"), ("sip", "ship"), ("class", "clash"), ("so", "show")],
        "practice": [
            "She said the store sells six sorts of special seeds.",
            "Some students still struggle to speak distinctly in class.",
        ],
    },
    {
        "symbol": "z",
        "ipa": "/z/",
        "label": "zoo",
        "manner": "fricative", "place": "alveolar", "voiced": True,
        "difficulty": 4,
        "artic_en": (
            "Same tongue position as /s/ — near the alveolar ridge. "
            "Add vocal cord vibration to create the buzzing /z/ sound. "
            "Common in grammar: plurals (-s), third person (-s), past tense (-ed) after voiced consonants."
        ),
        "artic_zh": "与/s/相同的舌头位置——靠近齿槽嵴。加上声带振动产生嗡嗡声的/z/。常见于语法：复数（-s）、第三人称（-s）、浊辅音后的过去式（-ed）。",
        "hard_en": (
            "Mandarin z is a completely different sound — an affricate (dz). "
            "English /z/ is a pure fricative. "
            "Speakers often devoice it to /s/ or substitute the Mandarin z sound."
        ),
        "hard_zh": "普通话的z是完全不同的音——一个破擦音（dz）。英语/z/是纯摩擦音。母语者常将其清化为/s/或用普通话的z音代替。",
        "substitution": "/s/ (devoiced) or Mandarin z-affricate",
        "sub_note_en": "Vocal cords don't vibrate — 'zoo' sounds like 'sue'.",
        "sub_note_zh": "声带不振动——「zoo」听起来像「sue」。",
        "pairs": [("zoo", "sue"), ("buzz", "bus"), ("his", "hiss"), ("rise", "rice")],
        "practice": [
            "The bees buzzed as they zigzagged across the rose bushes.",
            "These days those prizes are easier to visualize clearly.",
        ],
    },
    {
        "symbol": "ʃ",
        "ipa": "/ʃ/",
        "label": "she",
        "manner": "fricative", "place": "postalveolar", "voiced": False,
        "difficulty": 3,
        "artic_en": (
            "Tongue is raised toward the area just behind the alveolar ridge "
            "(post-alveolar). "
            "Lips are slightly rounded and pushed forward. "
            "Air flows over the tongue producing a 'shh' sound."
        ),
        "artic_zh": "舌头抬起靠近齿槽嵴后方区域（后齿槽），嘴唇略圆且向前突出。气流流过舌面产生「嘘」的声音。",
        "hard_en": (
            "Chinese sh is retroflex (tongue tip curls further back toward the palate). "
            "English /ʃ/ is more forward. "
            "Using Chinese sh for English /ʃ/ produces a slightly harsher sound."
        ),
        "hard_zh": "汉语的sh是卷舌音（舌尖向后卷向硬腭）。英语/ʃ/更靠前。用汉语sh来发英语/ʃ/会产生稍微刺耳的音色。",
        "substitution": "Chinese retrolex sh (too far back)",
        "sub_note_en": "Tongue curls too far back — the sound is slightly retroflex.",
        "sub_note_zh": "舌头卷得太靠后——声音略带卷舌色彩。",
        "pairs": [("she", "see"), ("ship", "sip"), ("rush", "rust"), ("fish", "fist")],
        "practice": [
            "She should wash the fresh fish on the shelf.",
            "The fashion show showcased sharp shoulder shapes.",
        ],
    },
    {
        "symbol": "ʒ",
        "ipa": "/ʒ/",
        "label": "measure",
        "manner": "fricative", "place": "postalveolar", "voiced": True,
        "difficulty": 4,
        "artic_en": (
            "Same tongue and lip position as /ʃ/, but add voicing. "
            "This is a rare sound in English — mostly in borrowed words and certain suffixes: "
            "measure, vision, genre, beige."
        ),
        "artic_zh": "与/ʃ/相同的舌头和嘴唇位置，但加上声带振动。这是英语中的稀有音——主要出现在借词和某些后缀中：measure、vision、genre、beige。",
        "hard_en": (
            "This sound does not exist in Mandarin and is rare in English. "
            "Speakers typically substitute /ʃ/ (removing voicing) or /dʒ/."
        ),
        "hard_zh": "这个音在普通话中不存在，在英语中也很少见。母语者通常用/ʃ/（去除浊音）或/dʒ/代替。",
        "substitution": "/ʃ/ or /dʒ/",
        "sub_note_en": "The voiced quality disappears or an extra stop is added.",
        "sub_note_zh": "浊音特质消失，或额外添加了爆破音。",
        "pairs": [("measure", "mesher"), ("leisure", "lesion"), ("vision", "fission")],
        "practice": [
            "The usual measure of pleasure was casual television.",
            "His vision of the azure treasure impressed the regime.",
        ],
    },
    {
        "symbol": "h",
        "ipa": "/h/",
        "label": "hat",
        "manner": "fricative", "place": "glottal", "voiced": False,
        "difficulty": 2,
        "artic_en": (
            "Open the glottis (vocal cords apart) and let air flow freely. "
            "Tongue and lips are already in the position of the following vowel. "
            "There is no friction from tongue or lips — just airflow from the throat."
        ),
        "artic_zh": "张开声门（声带分开）让气流自由通过。舌头和嘴唇已准备好发下一个元音的位置。不是舌头或嘴唇产生的摩擦——只是来自喉部的气流。",
        "hard_en": (
            "Chinese h has more friction (velar fricative) than English /h/. "
            "English /h/ is much lighter — almost just a breath. "
            "Using Chinese h makes the sound too harsh."
        ),
        "hard_zh": "汉语h的摩擦比英语/h/更强（软腭摩擦音）。英语/h/轻得多——几乎只是一口气。使用汉语h会使声音过于刺耳。",
        "substitution": "Chinese velar fricative (too much friction)",
        "sub_note_en": "Too much back-of-throat friction — sounds like clearing the throat.",
        "sub_note_zh": "喉部摩擦过多——听起来像在清嗓子。",
        "pairs": [("hat", "at"), ("his", "is"), ("hope", "ope"), ("heat", "eat")],
        "practice": [
            "He had hoped to handle the heat with a bit of humour.",
            "Hold on — the whole house needs a heavy renovation.",
        ],
    },
    # ── Affricates ────────────────────────────────────────────────────────────
    {
        "symbol": "tʃ",
        "ipa": "/tʃ/",
        "label": "chair",
        "manner": "affricate", "place": "postalveolar", "voiced": False,
        "difficulty": 3,
        "artic_en": (
            "Start with a /t/ stop (tongue on alveolar ridge), "
            "then release slowly into a /ʃ/ fricative. "
            "It is a single combined sound, not two separate sounds."
        ),
        "artic_zh": "从/t/爆破音开始（舌头在齿槽嵴上），然后缓慢释放进入/ʃ/摩擦音。这是一个组合音，不是两个独立的音。",
        "hard_en": (
            "Chinese ch is retroflex (tongue curls back), while English /tʃ/ is post-alveolar (more forward). "
            "Using Chinese ch for /tʃ/ produces a noticeably different tone."
        ),
        "hard_zh": "汉语ch是卷舌音（舌尖向后卷），而英语/tʃ/是后齿槽音（更靠前）。用汉语ch发英语/tʃ/会产生明显不同的音色。",
        "substitution": "Chinese retroflex ch (too far back)",
        "sub_note_en": "The release point is too far back — sounds retroflex.",
        "sub_note_zh": "释放点过于靠后——听起来带卷舌色彩。",
        "pairs": [("chair", "share"), ("cheap", "sheep"), ("watch", "wash"), ("chin", "shin")],
        "practice": [
            "The children chose chocolate chip sandwiches for lunch.",
            "Each teacher checked whether children reached the right answers.",
        ],
    },
    {
        "symbol": "dʒ",
        "ipa": "/dʒ/",
        "label": "jump",
        "manner": "affricate", "place": "postalveolar", "voiced": True,
        "difficulty": 4,
        "artic_en": (
            "Start with a /d/ stop, then release into a /ʒ/ fricative. "
            "This is the voiced counterpart of /tʃ/. "
            "Vocal cords vibrate throughout."
        ),
        "artic_zh": "从/d/爆破音开始，然后释放进入/ʒ/摩擦音。这是/tʃ/的浊音对应音。声带全程振动。",
        "hard_en": (
            "No voiced affricate exists in Mandarin in the same position. "
            "Speakers commonly devoice it to /tʃ/, so 'jump' sounds like 'chump'."
        ),
        "hard_zh": "普通话中在相同位置没有浊破擦音。母语者常将其清化为/tʃ/，使「jump」听起来像「chump」。",
        "substitution": "/tʃ/ (devoiced)",
        "sub_note_en": "Voicing is lost — 'judge' sounds like 'church'.",
        "sub_note_zh": "浊音丢失——「judge」听起来像「church」。",
        "pairs": [("jump", "chump"), ("jail", "chain"), ("edge", "etch"), ("badge", "batch")],
        "practice": [
            "Judge Jackson enjoyed jogging through the jungle each day.",
            "The geography project challenged every junior college student.",
        ],
    },
    # ── Nasals ────────────────────────────────────────────────────────────────
    {
        "symbol": "m",
        "ipa": "/m/",
        "label": "man",
        "manner": "nasal", "place": "bilabial", "voiced": True,
        "difficulty": 1,
        "artic_en": (
            "Press both lips together. "
            "Let the air and sound pass through your nose, not your mouth. "
            "Vocal cords vibrate."
        ),
        "artic_zh": "双唇紧闭，让气流和声音通过鼻腔而非口腔。声带振动。",
        "hard_en": "Identical to Chinese m — no difficulty for most learners.",
        "hard_zh": "与汉语m完全相同——对大多数学习者没有难度。",
        "substitution": "None (well-produced by most speakers)",
        "sub_note_en": "Occasionally omitted at word endings in fast speech.",
        "sub_note_zh": "偶尔在快速语流中词尾被省略。",
        "pairs": [("man", "ban"), ("some", "sun"), ("came", "cane"), ("home", "hone")],
        "practice": [
            "My mother makes amazing mushroom and meat meals.",
            "Come meet my family sometime — maybe tomorrow morning.",
        ],
    },
    {
        "symbol": "n",
        "ipa": "/n/",
        "label": "no",
        "manner": "nasal", "place": "alveolar", "voiced": True,
        "difficulty": 1,
        "artic_en": (
            "Touch the tongue tip to the alveolar ridge. "
            "Air and sound pass through the nose. "
            "Vocal cords vibrate."
        ),
        "artic_zh": "舌尖触碰齿槽嵴，气流和声音通过鼻腔。声带振动。",
        "hard_en": (
            "Similar to Chinese n. "
            "The main issue is distinguishing word-final /n/ from /ŋ/ "
            "(many speakers merge them)."
        ),
        "hard_zh": "与汉语n相似。主要问题是区分词尾/n/和/ŋ/（许多母语者将两者合并）。",
        "substitution": "/ŋ/ word-finally (merger)",
        "sub_note_en": "Final /n/ is produced too far back — tongue touches velum instead of alveolar ridge.",
        "sub_note_zh": "词尾/n/发音过于靠后——舌头触碰软腭而非齿槽嵴。",
        "pairs": [("sun", "sung"), ("thin", "thing"), ("win", "wing"), ("ban", "bang")],
        "practice": [
            "No one knew the name of the man near the corner.",
            "Nine new nurses needed training throughout November.",
        ],
    },
    {
        "symbol": "ŋ",
        "ipa": "/ŋ/",
        "label": "sing",
        "manner": "nasal", "place": "velar", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "The back of the tongue rises to touch the soft palate — same contact as /k/ and /g/. "
            "Air and sound pass through the nose. "
            "This sound never appears at the start of a syllable in English."
        ),
        "artic_zh": "舌根抬起触碰软腭——与/k/和/g/相同的接触位置。气流和声音通过鼻腔。这个音在英语中从不出现在音节开头。",
        "hard_en": (
            "Many Mandarin speakers merge /n/ and /ŋ/ in syllable-final position. "
            "A further error is adding a /g/ after /ŋ/ — 'singing' becomes 'sing-ging'."
        ),
        "hard_zh": "许多普通话母语者在音节末尾合并/n/和/ŋ/。另一个错误是在/ŋ/后加/g/——「singing」变成「sing-ging」。",
        "substitution": "/n/ (wrong place) or /ŋg/ (extra stop added)",
        "sub_note_en": "Either wrong place of articulation, or an unwanted /g/ follows.",
        "sub_note_zh": "要么发音部位错误，要么后面跟了不该有的/g/。",
        "pairs": [("sing", "sin"), ("ring", "rim"), ("long", "lon"), ("thing", "thin")],
        "practice": [
            "Singing and dancing bring something amazing to everything.",
            "The king of the ring kept winning longer and longer.",
        ],
    },
    # ── Approximants ──────────────────────────────────────────────────────────
    {
        "symbol": "l",
        "ipa": "/l/",
        "label": "let",
        "manner": "approximant", "place": "alveolar", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "Touch the tongue tip to the alveolar ridge. "
            "Air flows around the sides of the tongue (not over the top). "
            "In syllable-final position ('feel', 'milk'), English uses a 'dark l' "
            "where the back of the tongue also rises — it sounds more like a vowel."
        ),
        "artic_zh": "舌尖触碰齿槽嵴，气流从舌头两侧流过（而非从上方）。在音节末尾（「feel」「milk」），英语使用「暗l」——舌根也抬起，听起来更像元音。",
        "hard_en": (
            "Chinese l is similar to English 'light l' (syllable-initial). "
            "The difficulty is 'dark l' in syllable-final position — "
            "many speakers produce a clear /l/ everywhere, or even substitute a vowel."
        ),
        "hard_zh": "汉语l与英语「亮l」（音节首位）相似。难点是音节末尾的「暗l」——许多母语者处处发清晰的/l/，甚至用元音代替。",
        "substitution": "Clear /l/ everywhere (missing 'dark l' in final position)",
        "sub_note_en": "Final 'dark l' sounds too clear and front — missing the back-tongue raising.",
        "sub_note_zh": "末尾「暗l」听起来过于清晰且靠前——缺少舌根抬起。",
        "pairs": [("let", "red"), ("light", "right"), ("feel", "fear"), ("milk", "mirk")],
        "practice": [
            "Let the little girl help fill the tall blue bottle.",
            "Old Bill always called people by their full legal name.",
        ],
    },
    {
        "symbol": "r",
        "ipa": "/r/",
        "label": "red",
        "manner": "approximant", "place": "postalveolar", "voiced": True,
        "difficulty": 5,
        "artic_en": (
            "In General American, the tongue tip curls back (retroflex) or bunches up in the middle "
            "— without touching any part of the palate. "
            "Lips are slightly rounded. "
            "There is no contact, no friction — just the tongue shaping the airstream."
        ),
        "artic_zh": "在美式英语中，舌尖向后卷（卷舌）或在中间隆起——不触碰腭部任何部位。嘴唇略微圆拢。没有接触，没有摩擦——只是舌头塑造气流的形状。",
        "hard_en": (
            "Chinese r (rè) is a retroflex fricative — the tongue curls back and touches the palate. "
            "English /r/ requires no tongue contact at all. "
            "Using Chinese r produces a buzzing, fricative quality that sounds noticeably foreign."
        ),
        "hard_zh": "汉语r（热）是卷舌摩擦音——舌尖向后卷并触碰硬腭。英语/r/完全不需要舌头接触。使用汉语r会产生嗡嗡的摩擦音质，听起来明显是外国口音。",
        "substitution": "Chinese retroflex r (tongue contacts palate)",
        "sub_note_en": "Tongue tip touches the palate — introduces friction that shouldn't be there.",
        "sub_note_zh": "舌尖触碰硬腭——产生了不该有的摩擦。",
        "pairs": [("red", "led"), ("right", "light"), ("rain", "lane"), ("try", "tie")],
        "practice": [
            "The right word rarely arrives ready-made — read broadly.",
            "Three runners raced around the river road at dawn.",
        ],
    },
    {
        "symbol": "w",
        "ipa": "/w/",
        "label": "we",
        "manner": "approximant", "place": "bilabial-velar", "voiced": True,
        "difficulty": 3,
        "artic_en": (
            "Start with lips tightly rounded and pushed forward (like for /uː/), "
            "and tongue high and back. "
            "Then quickly glide the lips open toward the following vowel. "
            "No teeth contact — this is not /v/."
        ),
        "artic_zh": "从双唇紧圆且向前突出（类似/uː/）开始，舌头高且靠后。然后快速将嘴唇张开滑向下一个元音。不涉及牙齿接触——这不是/v/。",
        "hard_en": (
            "The main error is substituting /v/ — placing upper teeth on lower lip "
            "instead of rounding the lips. "
            "This makes 'wine' sound like 'vine'. "
            "Chinese w is often less rounded than English /w/."
        ),
        "hard_zh": "主要错误是用/v/代替——将上牙放在下唇上而不是圆拢嘴唇。这使「wine」听起来像「vine」。汉语的w通常不如英语/w/圆润。",
        "substitution": "/v/ (teeth on lower lip instead of rounded lips)",
        "sub_note_en": "Teeth contact lower lip — 'west' sounds like 'vest'.",
        "sub_note_zh": "牙齿接触下唇——「west」听起来像「vest」。",
        "pairs": [("wine", "vine"), ("west", "vest"), ("wet", "vet"), ("wail", "veil")],
        "practice": [
            "We always watch the weather when we walk at weekends.",
            "Would you want to work in the warm southwestern woods?",
        ],
    },
    {
        "symbol": "j",
        "ipa": "/j/",
        "label": "yes",
        "manner": "approximant", "place": "palatal", "voiced": True,
        "difficulty": 2,
        "artic_en": (
            "Tongue is in the high-front /iː/ position. "
            "Quickly glide it away toward the following vowel. "
            "It is a brief, smooth movement — not a stop, not a fricative."
        ),
        "artic_zh": "舌头处于高前/iː/位置，然后快速滑向下一个元音。这是一个短暂、流畅的动作——不是爆破音，也不是摩擦音。",
        "hard_en": (
            "Similar to Chinese y (yā). "
            "The main error is adding affrication — 'yes' becomes 'dges' (/dʒes/). "
            "This happens when the tongue releases too slowly."
        ),
        "hard_zh": "与汉语y（呀）相似。主要错误是添加破擦音——「yes」变成「dges」(/dʒes/)。当舌头释放过慢时会发生这种情况。",
        "substitution": "/dʒ/ (affrication added)",
        "sub_note_en": "Tongue releases too slowly — a /d/ onset is added before the glide.",
        "sub_note_zh": "舌头释放过慢——在滑音前加了/d/起音。",
        "pairs": [("yes", "guess"), ("year", "ear"), ("you", "do"), ("yell", "dell")],
        "practice": [
            "You should use your yellow umbrella in the yard.",
            "Did you say you were young when you first visited New York?",
        ],
    },
]


# ── Lookup helpers ────────────────────────────────────────────────────────────

def get_vowel(symbol: str) -> dict | None:
    return next((v for v in VOWELS if v["symbol"] == symbol), None)

def get_consonant(symbol: str) -> dict | None:
    return next((c for c in CONSONANTS if c["symbol"] == symbol), None)

def get_sound(symbol: str) -> dict | None:
    return get_vowel(symbol) or get_consonant(symbol)
