"""
phonology.py  —  Phonology Guide: 7 interactive concept cards
"""

import streamlit as st
from modules.materials import TAGS

CARDS = {
    "stress": {
        "tag": "stress",
        "title_en": "Stress Pattern",
        "title_zh": "重音模式",
        "icon": "💥",
        "what_en": (
            "In English, some syllables are pronounced louder, longer, and at a higher pitch "
            "than others. This is called word stress. In multi-syllable words, stress almost "
            "always falls on one specific syllable and that placement is fixed."
        ),
        "what_zh": (
            "英语中，某些音节的发音比其他音节更响、更长、音调更高，这就是词重音。"
            "在多音节词中，重音几乎总是固定地落在某一个特定音节上。"
        ),
        "why_hard_en": (
            "Mandarin is syllable-timed: each syllable gets roughly equal duration and prominence. "
            "This makes English word stress perceptually difficult — you may hear all syllables "
            "as equally important and produce them that way. Words can sound wrong even if every "
            "individual sound is correct."
        ),
        "why_hard_zh": (
            "普通话是音节计时语言：每个音节的时长和重要性大致相等。"
            "这使得英语词重音在感知上很难——你可能把所有音节都听成同等重要的，并这样发音。"
            "结果是，即使每个单独的发音都正确，整个词听起来重音位置也会不对。"
        ),
        "examples": [
            {"word": "PRO-di-gy",   "wrong": "pro-DI-gy",   "note": "Nouns often stress first syllable"},
            {"word": "per-FORM",    "wrong": "PER-form",    "note": "Verbs often stress second syllable"},
            {"word": "EX-cel-lent", "wrong": "ex-CEL-lent", "note": "Adjectives often stress first"},
        ],
        "tip_en": (
            "Before shadowing, mark the stressed syllable in every content word with a dot above it. "
            "Listen carefully to confirm. This priming step reduces cognitive load during shadowing."
        ),
        "tip_zh": (
            "跟读前，在每个实词的重读音节上方点一个点，然后仔细听原音确认。"
            "这个预备步骤能在跟读时降低认知负荷。"
        ),
        "theory": "Cognitive Load Theory — pre-marking reduces extraneous load during shadowing.",
    },
    "link": {
        "tag": "link",
        "title_en": "Linking",
        "title_zh": "连读",
        "icon": "🔗",
        "what_en": (
            "Linking happens when a word ending in a consonant sound is followed by a word "
            "beginning with a vowel sound. The two words blend into one smooth phrase — "
            "the consonant is borrowed by the next word."
        ),
        "what_zh": (
            "当一个以辅音结尾的词后面跟着一个以元音开头的词时，就会发生连读。"
            "两个词融合成一个流畅的短语——辅音被下一个词借用。"
        ),
        "why_hard_en": (
            "Mandarin has clear syllable boundaries — each character is pronounced as a "
            "distinct unit. English linking violates this: took up sounds like too-kup, "
            "not took plus up. When you expect a word boundary, the sound seems to disappear, "
            "making fast English speech feel incomprehensible."
        ),
        "why_hard_zh": (
            "普通话的音节边界非常清晰——每个汉字作为独立单元发音。"
            "英语连读违反了这一直觉：took up 听起来像 too-kup，而不是 took 加 up。"
            "当你期待词语边界时，声音好像消失了，使快速英语听起来难以理解。"
        ),
        "examples": [
            {"word": "took-up",       "wrong": "took | up",     "note": "/k/ blends into /ʌ/"},
            {"word": "areas-such",    "wrong": "areas | such",  "note": "/z/ blends into /s/"},
            {"word": "experts-even",  "wrong": "experts | even","note": "/s/ blends into /iː/"},
        ],
        "tip_en": (
            "In the practice text, draw a small arc between consonant-vowel word boundaries "
            "before you start listening. Predict where linking will happen, then confirm. "
            "Over time this becomes automatic."
        ),
        "tip_zh": (
            "在练习文本中，开始听之前在辅音-元音词语边界之间画一个小弧线。"
            "预测连读发生的地方，然后确认。随着时间推移，这会变得自动化。"
        ),
        "theory": "Noticing Hypothesis — predicting linking forces conscious attention to connected speech.",
    },
    "weak": {
        "tag": "weak",
        "title_en": "Weak Form",
        "title_zh": "弱读",
        "icon": "👻",
        "what_en": (
            "Many common English words — articles, prepositions, pronouns, auxiliaries — have "
            "two pronunciations: a strong form used when emphasised, and a weak form used in "
            "normal unstressed speech. In natural speech, weak forms are used almost all the "
            "time. The vowel reduces to a schwa /e/ or disappears entirely."
        ),
        "what_zh": (
            "许多常见英语词——冠词、介词、代词、助动词——有两种发音：强调时用的强式，"
            "以及正常非重读语流中用的弱式。在自然语流中，弱式几乎一直被使用。"
            "元音会弱化为中央元音或完全消失。"
        ),
        "why_hard_en": (
            "In Mandarin, every character has a fixed, full pronunciation. The idea that a "
            "common word like are or of is almost inaudible in natural speech is "
            "counter-intuitive. Learners often look for a word they know and cannot find it "
            "because it has been reduced to a single schwa sound."
        ),
        "why_hard_zh": (
            "在普通话中，每个汉字都有固定的完整发音。"
            "常见词如 are 或 of 在自然语流中几乎听不见，这违反直觉。"
            "学习者经常寻找他们认识的词，却找不到，因为它已经被弱化为单个中央元音。"
        ),
        "examples": [
            {"word": "are → schwa",  "wrong": "full /ɑː/",  "note": "In: they are experts"},
            {"word": "of → /ev/",    "wrong": "full /ɒv/",  "note": "In: piece of music"},
            {"word": "a → schwa",    "wrong": "full /eɪ/",  "note": "In: a music prodigy"},
            {"word": "to → /te/",    "wrong": "full /tuː/", "note": "In: tried to play"},
        ],
        "tip_en": (
            "Choose one function word (try of or are) and focus your entire listening "
            "attention on it for one full playthrough. Notice how reduced it sounds. "
            "Then do the same for a. This targeted listening builds a new phonological template."
        ),
        "tip_zh": (
            "选择一个功能词（试试 of 或 are），在一次完整播放中将全部注意力集中在它上面。"
            "注意它听起来有多弱化。然后对 a 做同样的事。"
            "这种有针对性的听力训练能建立新的语音模板。"
        ),
        "theory": "Schmidt (1990) — noticing the gap between expected and actual pronunciation is the entry point for acquisition.",
    },
    "intonation": {
        "tag": "intonation",
        "title_en": "Intonation",
        "title_zh": "语调",
        "icon": "〰️",
        "what_en": (
            "Intonation is the rise and fall of pitch across a sentence. English uses "
            "a falling tone at the end of statements and commands, and a rising tone for "
            "yes/no questions. Intonation also carries subtle meaning beyond sentence type."
        ),
        "what_zh": (
            "语调是句子中音调的升降变化。英语在陈述句和命令句末尾使用降调，"
            "在一般疑问句中使用升调。语调还承载超越句子类型的微妙含义。"
        ),
        "why_hard_en": (
            "Mandarin uses tones lexically — tone is part of the word meaning, not a "
            "sentence-level signal. Mandarin speakers often carry syllable-level tonal "
            "patterns into English, creating a flat or monotone delivery. "
            "The sentence-level intonation arc of English feels unnatural."
        ),
        "why_hard_zh": (
            "普通话的声调是词汇性的——声调是词义的一部分，而非句子层面的信号。"
            "普通话母语者经常将音节级别的声调模式带入英语，造成平调或单调的表达。"
            "英语句子层面的语调弧线感觉不自然。"
        ),
        "examples": [
            {"word": "She is a prodigy. (falling)", "wrong": "flat tone throughout",
             "note": "Declarative: falling on final stressed word"},
            {"word": "Is she a prodigy? (rising)",  "wrong": "falling at end",
             "note": "Yes/no question: rising tone"},
        ],
        "tip_en": (
            "Hum the melody of a sentence without any words before you shadow it. "
            "Focus only on the pitch shape. When you then shadow with words, "
            "your body already knows the melodic template."
        ),
        "tip_zh": (
            "在跟读一个句子之前，不带任何词语地哼出它的旋律。只专注于音调形状。"
            "当你带着词语跟读时，你的身体已经知道了旋律模板。"
        ),
        "theory": "Prosodic bootstrapping — pitch contour provides structural information that aids comprehension.",
    },
    "rhythm": {
        "tag": "rhythm",
        "title_en": "Rhythm",
        "title_zh": "节奏",
        "icon": "🥁",
        "what_en": (
            "English is a stress-timed language: the beats fall on stressed syllables, "
            "and the time between beats stays roughly equal regardless of how many "
            "unstressed syllables are squeezed in between. Unstressed syllables are "
            "compressed to maintain the rhythm."
        ),
        "what_zh": (
            "英语是重音计时语言：节拍落在重读音节上，节拍之间的时间大致相等——"
            "无论中间塞入多少非重读音节。非重读音节被压缩以保持节奏。"
        ),
        "why_hard_en": (
            "Mandarin is syllable-timed: every syllable takes roughly the same amount of time. "
            "This is the most fundamental rhythmic difference between the two languages. "
            "When Mandarin speakers use syllable-timing in English, it sounds robotic and "
            "is harder to understand because the rhythm listeners use to predict word "
            "boundaries is missing."
        ),
        "why_hard_zh": (
            "普通话是音节计时语言：每个音节占用大致相同的时间。"
            "这是两种语言节奏模式之间最根本的差异。"
            "当普通话母语者用音节计时说英语时，听起来很机械，也更难理解，"
            "因为听者用来预测词语边界的节奏消失了。"
        ),
        "examples": [
            {"word": "CATS can CATCH MICE",       "wrong": "cats CAN catch mice",
             "note": "4 words, 2 beats: CATS and CATCH"},
            {"word": "she TOOK up PIAno lesSons", "wrong": "equal stress each syllable",
             "note": "Content words carry the beat"},
        ],
        "tip_en": (
            "Tap the table on every stressed syllable as you shadow. Do not tap on unstressed "
            "syllables. The tapping makes the stress-timing pattern physical and reveals "
            "immediately when you give too much time to an unstressed syllable."
        ),
        "tip_zh": (
            "跟读时在每个重读音节上拍桌子，非重读音节不拍。"
            "拍击动作使重音计时模式变得具体，并能立即揭示你何时给了非重读音节太多时间。"
        ),
        "theory": "Motor theory of speech perception — physical rhythm production reinforces phonological memory.",
    },
    "omission": {
        "tag": "omission",
        "title_en": "Omission",
        "title_zh": "漏读",
        "icon": "🕳️",
        "what_en": (
            "In connected speech, English speakers frequently omit certain sounds. "
            "The most common are: final /t/ and /d/ before consonants (elision), "
            "and sounds in consonant clusters that become difficult to pronounce at speed."
        ),
        "what_zh": (
            "在连续语流中，英语母语者经常省略某些音素。最常见的是："
            "在辅音前省略词尾 /t/ 和 /d/（失爆），以及高速度下辅音丛中的音素简化。"
        ),
        "why_hard_en": (
            "Mandarin syllable structure is simple with very limited final consonants. "
            "Chinese speakers tend to add vowels after final consonants rather than "
            "omit them. Noticing that a sound has been omitted requires "
            "you to first know that it should be there."
        ),
        "why_hard_zh": (
            "普通话的音节结构简单，末尾辅音很少。"
            "中文母语者倾向于在词尾辅音后添加元音，而不是省略它——这是相反的问题。"
            "注意到某个音素被省略，首先需要你知道它本应该在那里。"
        ),
        "examples": [
            {"word": "bes(t) friend",   "wrong": "best friend with full /t/",
             "note": "/t/ elided before /f/"},
            {"word": "han(d)s",         "wrong": "hands with full /d/",
             "note": "/d/ often reduced in clusters"},
        ],
        "tip_en": (
            "Listen for what is NOT there, not just what is. In the text, circle every "
            "final /t/ or /d/ before a consonant. Before listening, predict: will this be "
            "pronounced or elided? Then confirm."
        ),
        "tip_zh": (
            "不仅要听有什么，还要听没有什么。在文本中，圈出所有在辅音前出现的词尾 /t/ 或 /d/。"
            "听之前预测：这个音会被发出还是会失爆？然后确认。"
        ),
        "theory": "Noticing Hypothesis — predicting absence requires conscious phonological knowledge.",
    },
    "insertion": {
        "tag": "insertion",
        "title_en": "Insertion",
        "title_zh": "多读",
        "icon": "➕",
        "what_en": (
            "Insertion (epenthesis) is when a sound is added that is not in the original word. "
            "For EFL learners from Mandarin backgrounds, the most common form is adding a "
            "vowel after a final consonant — because Mandarin syllables typically end in a "
            "vowel or a limited set of nasals."
        ),
        "what_zh": (
            "多读（增音）是指添加原词中没有的音素。"
            "对于普通话背景的EFL学习者，最常见的形式是在词尾辅音后添加元音——"
            "因为普通话音节通常以元音或有限的鼻音结尾。"
        ),
        "why_hard_en": (
            "Your phonological system expects syllables to end in vowels. When you encounter "
            "an English word ending in a consonant cluster like skills or strengths, "
            "your brain automatically adds a vowel to create a familiar syllable shape. "
            "This is involuntary and requires conscious, repeated attention to correct."
        ),
        "why_hard_zh": (
            "你的语音系统期待音节以元音结尾。当你遇到以辅音丛结尾的英语词时，"
            "你的大脑会自动添加元音来创造熟悉的音节形状。"
            "这是无意识的，需要有意识地、反复地注意才能纠正。"
        ),
        "examples": [
            {"word": "skills",    "wrong": "skills-uh",   "note": "No vowel after final /z/"},
            {"word": "practice",  "wrong": "practice-uh", "note": "No vowel after final /s/"},
            {"word": "art",       "wrong": "art-uh",      "note": "No vowel after final /t/"},
        ],
        "tip_en": (
            "Record yourself saying the last word of a sentence and listen back at half speed. "
            "Do you add a vowel at the end? If so, practise stopping your voice completely "
            "on the final consonant — no vowel, just closure."
        ),
        "tip_zh": (
            "录下你说一个句子最后一个词的声音，以半速回放。你在末尾添加了元音吗？"
            "如果是，练习在词尾辅音上完全停止发声——没有元音，只有闭合。"
        ),
        "theory": "Phonological transfer — L1 syllable templates are applied to L2 output.",
    },
}


def phonology_page():
    st.title("📖 Phonology Guide / 语音指南")
    st.markdown(
        '<p class="muted" style="margin-top:-8px;margin-bottom:24px;">' +
        'Seven phonological phenomena explained for Mandarin-speaking EFL learners. ' +
        'Tap a card to expand it.' +
        '</p>', unsafe_allow_html=True
    )

    filter_tab = st.radio(
        "Show",
        ["All", "Stress & Rhythm", "Connected Speech", "Intonation"],
        horizontal=True,
        label_visibility="collapsed",
        key="phon_filter",
    )
    filter_map = {
        "All":              list(CARDS.keys()),
        "Stress & Rhythm":  ["stress", "rhythm"],
        "Connected Speech": ["link", "weak", "omission", "insertion"],
        "Intonation":       ["intonation"],
    }
    visible = filter_map.get(filter_tab, list(CARDS.keys()))
    for tag_key in visible:
        _render_full_card(CARDS[tag_key])


def _render_full_card(card: dict):
    tag   = TAGS.get(card["tag"], {})
    color = tag.get("color", "#374151")
    bg    = tag.get("bg",    "#F9FAFB")

    with st.expander(
        f'{card["icon"]}  {card["title_en"]} / {card["title_zh"]}',
        expanded=(st.session_state.get("phon_open_card") == card["tag"]),
    ):
        col_what, col_hard = st.columns(2)
        with col_what:
            st.markdown(f"""
            <div style="background:{bg};border-left:4px solid {color};border-radius:8px;
                        padding:12px 16px;margin-bottom:10px;">
                <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:.05em;color:{color};margin-bottom:6px;">
                    What is it? / 是什么？
                </div>
                <div style="font-size:.88rem;color:#374151;line-height:1.6;">{card['what_en']}</div>
                <div style="font-size:.82rem;color:#6B7280;line-height:1.55;margin-top:6px;">
                    {card['what_zh']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_hard:
            st.markdown(f"""
            <div style="background:#FFF7ED;border-left:4px solid #F59E0B;border-radius:8px;
                        padding:12px 16px;margin-bottom:10px;">
                <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:.05em;color:#92400E;margin-bottom:6px;">
                    Why hard for Mandarin speakers / 为什么对汉语母语者来说很难
                </div>
                <div style="font-size:.88rem;color:#374151;line-height:1.6;">{card['why_hard_en']}</div>
                <div style="font-size:.82rem;color:#6B7280;line-height:1.55;margin-top:6px;">
                    {card['why_hard_zh']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Examples / 示例**")
        ex_cols = st.columns(min(len(card["examples"]), 3))
        for i, ex in enumerate(card["examples"]):
            with ex_cols[i % len(ex_cols)]:
                st.markdown(f"""
                <div class="sl-surface" style="font-size:.83rem;margin-bottom:6px;">
                    <div style="font-weight:700;color:{color};margin-bottom:3px;">✓ {ex['word']}</div>
                    <div style="color:#DC2626;margin-bottom:3px;">✗ {ex['wrong']}</div>
                    <div class="muted">{ex['note']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#ECFDF5;border-left:4px solid #10B981;border-radius:8px;
                    padding:12px 16px;margin:10px 0;">
            <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.05em;color:#065F46;margin-bottom:6px;">
                💡 Practice tip / 练习建议
            </div>
            <div style="font-size:.88rem;color:#374151;line-height:1.6;">{card['tip_en']}</div>
            <div style="font-size:.82rem;color:#6B7280;line-height:1.55;margin-top:6px;">
                {card['tip_zh']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            f'<div class="muted" style="font-size:.75rem;margin-top:4px;">' +
            f'📚 Theory: {card["theory"]}</div>',
            unsafe_allow_html=True
        )


def inline_concept_card(tag_key: str, context_sentence: str = ""):
    card = CARDS.get(tag_key)
    if not card:
        return
    tag   = TAGS.get(tag_key, {})
    color = tag.get("color", "#374151")
    bg    = tag.get("bg",    "#F9FAFB")

    st.markdown(f"""
    <div style="background:{bg};border:1.5px solid {color}50;border-radius:12px;
                padding:16px 18px;margin:10px 0;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span style="font-size:1.2rem;">{card["icon"]}</span>
            <div>
                <div style="font-weight:700;color:{color};font-size:.95rem;">
                    {card["title_en"]} / {card["title_zh"]}
                </div>
                <div style="font-size:.75rem;color:{color};opacity:.7;">Phonology concept card</div>
            </div>
        </div>
        <div style="font-size:.86rem;color:#374151;line-height:1.6;margin-bottom:6px;">
            {card["what_en"]}
        </div>
        <div style="font-size:.8rem;color:#6B7280;line-height:1.55;margin-bottom:10px;">
            {card["what_zh"]}
        </div>
        <div style="background:#FFF7ED;border-radius:6px;padding:8px 12px;
                    font-size:.82rem;color:#92400E;margin-bottom:8px;">
            <strong>Why hard for Mandarin speakers:</strong><br>{card["why_hard_en"]}
        </div>
        <div style="background:#ECFDF5;border-radius:6px;padding:8px 12px;
                    font-size:.82rem;color:#065F46;">
            <strong>Tip:</strong> {card["tip_en"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_close, col_full = st.columns([1, 1])
    with col_close:
        if st.button("Close", key=f"inline_close_{tag_key}", use_container_width=True):
            st.session_state.phon_inline_card = None
            st.rerun()
    with col_full:
        if st.button("Full card", key=f"inline_full_{tag_key}", use_container_width=True):
            st.session_state.phon_open_card = tag_key
            st.session_state.page = "phonology"
            st.rerun()
