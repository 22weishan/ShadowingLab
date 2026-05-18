"""
about.py — About Shadowing: Science & Method
=============================================
Five-tab science communication page covering:
  1. Definition — what shadowing is
  2. Origin — where it came from
  3. Why it works — theoretical mechanisms
  4. Research evidence — key studies and data
  5. How ShadowingLab guides practice — interactive 5-phase timeline
"""

import streamlit as st


# ── Shared helpers ────────────────────────────────────────────────────────────

def _section_header(en, zh, icon=""):
    st.markdown(
        f'<div style="margin-bottom:20px;">'
        f'<div style="font-size:1.25rem;font-weight:700;color:#1A3A5C;margin-bottom:4px;">'
        f'{icon + " " if icon else ""}{en}</div>'
        f'<div style="font-size:.85rem;color:#9CA3AF;">{zh}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _card(body, border_color="#2563EB", bg="#F9FAFB"):
    st.markdown(
        f'<div style="border:1px solid #E5E7EB;border-left:4px solid {border_color};'
        f'border-radius:10px;padding:18px 22px;background:{bg};margin-bottom:14px;">'
        f'{body}</div>',
        unsafe_allow_html=True,
    )


def _cite(n):
    """Return a superscript citation badge."""
    return (
        f'<sup style="font-size:.65rem;color:#2563EB;font-weight:700;'
        f'background:#DBEAFE;border-radius:3px;padding:1px 4px;margin-left:2px;">{n}</sup>'
    )


def _ref_block(refs):
    """Render a compact reference list at the bottom of a tab."""
    items = "".join(
        f'<div style="margin-bottom:6px;">'
        f'<span style="font-size:.72rem;font-weight:700;color:#2563EB;'
        f'background:#DBEAFE;border-radius:3px;padding:1px 5px;margin-right:6px;">{r["n"]}</span>'
        f'<span style="font-size:.78rem;color:#6B7280;">{r["text"]}</span>'
        f'</div>'
        for r in refs
    )
    st.markdown(
        f'<div style="background:#F8FAFC;border:1px solid #E5E7EB;border-radius:10px;'
        f'padding:14px 18px;margin-top:24px;">'
        f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:.06em;color:#9CA3AF;margin-bottom:10px;">References / 参考文献</div>'
        f'{items}</div>',
        unsafe_allow_html=True,
    )


def _pill(text, color="#2563EB", bg="#DBEAFE"):
    return (
        f'<span style="display:inline-block;background:{bg};color:{color};'
        f'font-size:.72rem;font-weight:700;border-radius:99px;'
        f'padding:3px 10px;margin:2px 3px 2px 0;">{text}</span>'
    )


# ── Tab 1: Definition ─────────────────────────────────────────────────────────

def _tab_definition():
    _section_header("What Is Shadowing?", "什么是跟读法？", "📌")

    c1 = _cite(1)
    c2 = _cite(2)

    _card(
        f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:.06em;color:#9CA3AF;margin-bottom:8px;">Formal definition / 正式定义</div>'
        f'<div style="font-size:1rem;font-weight:600;color:#1A3A5C;line-height:1.7;margin-bottom:10px;">'
        f'"The act of vocalizing the speech one is listening to as simultaneously as possible."{c1}'
        f'</div>'
        f'<div style="font-size:.88rem;color:#6B7280;line-height:1.7;">'
        f'即：在听到目标语言的同时，尽可能实时地将所听内容复述出来。{c1}'
        f'</div>',
        border_color="#2563EB",
        bg="#F0F6FF",
    )

    st.markdown(
        '<div style="font-size:.85rem;font-weight:600;color:#1A3A5C;margin:18px 0 10px;">Three defining features / 三个核心特征</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    features = [
        ("⚡", "Simultaneous", "同步性",
         "You speak while you listen — no pause in between. This is what sets shadowing apart from delayed repetition.",
         "边听边说，中间没有停顿间隔，这是跟读法与延迟重复练习的根本区别。"),
        ("🎯", "Imitation-based", "模仿导向",
         "The goal is to match the model as closely as possible — sound, rhythm, intonation, and speed.",
         "目标是尽可能贴近范本的音色、节奏、语调和语速。"),
        ("🧠", "Meaning-engaged", "意义参与",
         "Effective shadowing is not mindless parroting. You track meaning while imitating form.",
         "有效的跟读不是机械鹦鹉学舌，而是在模仿形式的同时追踪意义。"),
    ]
    for col, (icon, en, zh, desc_en, desc_zh) in zip(cols, features):
        with col:
            st.markdown(
                f'<div style="border:1px solid #E5E7EB;border-radius:10px;'
                f'padding:16px 14px;background:#FAFAFA;height:100%;">'
                f'<div style="font-size:1.4rem;margin-bottom:8px;">{icon}</div>'
                f'<div style="font-size:.9rem;font-weight:700;color:#1A3A5C;margin-bottom:2px;">{en}</div>'
                f'<div style="font-size:.78rem;color:#9CA3AF;margin-bottom:8px;">{zh}</div>'
                f'<div style="font-size:.82rem;color:#374151;line-height:1.6;margin-bottom:4px;">{desc_en}</div>'
                f'<div style="font-size:.78rem;color:#9CA3AF;line-height:1.55;">{desc_zh}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="font-size:.85rem;font-weight:600;color:#1A3A5C;margin:22px 0 10px;">How shadowing differs from other methods / 与其他方法的区别</div>',
        unsafe_allow_html=True,
    )
    table_html = (
        '<div style="overflow-x:auto;">'
        '<table style="width:100%;border-collapse:collapse;font-size:.82rem;">'
        '<thead><tr style="background:#F3F4F6;">'
        '<th style="padding:8px 12px;text-align:left;color:#374151;border-bottom:1px solid #E5E7EB;">Method / 方法</th>'
        '<th style="padding:8px 12px;text-align:left;color:#374151;border-bottom:1px solid #E5E7EB;">Timing / 时机</th>'
        '<th style="padding:8px 12px;text-align:left;color:#374151;border-bottom:1px solid #E5E7EB;">Focus / 重点</th>'
        '</tr></thead><tbody>'
        '<tr style="background:#EFF6FF;">'
        '<td style="padding:8px 12px;font-weight:600;color:#1D4ED8;border-bottom:1px solid #E5E7EB;">Shadowing 跟读</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Simultaneous 同步</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Form + Meaning 形式与意义</td>'
        '</tr>'
        '<tr><td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Delayed repetition 延迟重复</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">After a pause 停顿后</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Accuracy 准确性</td>'
        '</tr>'
        '<tr style="background:#F9FAFB;"><td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Listen-and-repeat 听后重复</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">After full sentence 句子结束后</td>'
        '<td style="padding:8px 12px;color:#374151;border-bottom:1px solid #E5E7EB;">Memory recall 记忆提取</td>'
        '</tr>'
        '<tr><td style="padding:8px 12px;color:#374151;">Dictation 听写</td>'
        '<td style="padding:8px 12px;color:#374151;">After hearing 听完后</td>'
        '<td style="padding:8px 12px;color:#374151;">Orthographic form 书写形式</td>'
        '</tr>'
        '</tbody></table></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown(
        f'<div style="background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:8px;'
        f'padding:12px 16px;margin-top:20px;font-size:.84rem;color:#92400E;">'
        f'<strong>Note / 说明：</strong> Research identifies 16 distinct shadowing variations,{c2} '
        f'ranging from silent mouthing to full-voice simultaneous shadowing with or without text support. '
        f'ShadowingLab uses a structured 5-phase cycle derived from best-practice guidelines.<br>'
        f'<span style="color:#B45309;">研究者已归纳出16种跟读变体，从无声口型到全声同步跟读。ShadowingLab采用基于最佳实践的五阶段结构化循环。</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    _ref_block([
        {"n": 1, "text": "Hamada, Y. & Suzuki, A. (2024). Situating Shadowing in the Framework of Deliberate Practice. Language Teaching Research."},
        {"n": 2, "text": "Hamada, Y. & Suzuki, A. (2024). 16 Shadowing Technique Variations. RELC Journal."},
    ])


# ── Tab 2: Origin ─────────────────────────────────────────────────────────────

def _tab_origin():
    _section_header("Where Did Shadowing Come From?", "跟读法从何而来？", "🕰️")

    timeline = [
        {
            "period": "1980s",
            "color": "#6B7280",
            "bg": "#F9FAFB",
            "title_en": "Roots in interpreter training",
            "title_zh": "起源于口译员培训",
            "body_en": (
                "Shadowing first appeared as a drill for simultaneous interpreters. "
                "Trainees were required to repeat incoming speech with minimal delay — "
                "a technique used to build the split-attention capacity needed for live interpreting."
            ),
            "body_zh": "跟读最早作为同声传译员的训练练习出现。学员须以极短延迟重复所听内容，以培养同声传译所需的注意力分配能力。",
            "cite": _cite(1),
        },
        {
            "period": "1992",
            "color": "#2563EB",
            "bg": "#EFF6FF",
            "title_en": "Shadowing enters EFL research",
            "title_zh": "进入英语教学研究领域",
            "body_en": (
                "Japanese linguist Katsuhiko Tamai conducted one of the first controlled studies "
                "comparing shadowing against dictation for listening development. "
                "Shadowing outperformed dictation — sparking a wave of academic interest in Japan."
            ),
            "body_zh": "日本语言学家玉井健进行了首批对照研究，比较跟读与听写对听力发展的效果。跟读优于听写——在日本引发了一波学术研究热潮。",
            "cite": _cite(2),
        },
        {
            "period": "2001",
            "color": "#0F6E56",
            "bg": "#E8F5F3",
            "title_en": "Conversational shadowing popularised",
            "title_zh": "会话跟读走向大众",
            "body_en": (
                "Tim Murphey's landmark paper \"Exploring Conversational Shadowing\" "
                "in Language Teaching Research brought shadowing into mainstream communicative language teaching. "
                "Murphey framed it as \"deep listening\" — training the brain, not just the mouth."
            ),
            "body_zh": "Tim Murphey在《语言教学研究》发表了「探索会话跟读」一文，将跟读法带入主流交际语言教学。他将其定性为「深度听力」——训练大脑，不仅仅是嘴。",
            "cite": _cite(3),
        },
        {
            "period": "2000s–2010s",
            "color": "#7C3AED",
            "bg": "#F5F3FF",
            "title_en": "Arguelles and the polyglot community",
            "title_zh": "多语学习者社群的推广",
            "body_en": (
                "Linguist and polyglot Alexander Arguelles (fluent in 50+ languages) "
                "documented his \"outdoor shadowing\" method — walking while shadowing at full voice — "
                "spreading the technique to millions of self-directed language learners worldwide."
            ),
            "body_zh": "语言学家兼多语学习者Alexander Arguelles（精通50多种语言）记录了他的「户外跟读法」——边走边大声跟读——将该技术推广至全球数百万自主学习者。",
            "cite": _cite(4),
        },
        {
            "period": "2016–2017",
            "color": "#B54F1A",
            "bg": "#FBF0EB",
            "title_en": "Empirical evidence solidifies",
            "title_zh": "实证证据趋于成熟",
            "body_en": (
                "Hamada (2016) ran a 6-week study with 43 EFL learners, confirming phoneme perception gains. "
                "Foote & McDonough (2017) extended findings to mobile learning contexts, "
                "showing significant improvements in pronunciation, prosody, and fluency."
            ),
            "body_zh": "Hamada（2016）对43名EFL学习者进行为期6周的研究，证实了音素感知的提升。Foote & McDonough（2017）将研究延伸至移动学习场景，发现在发音、韵律和流利度上均有显著改善。",
            "cite": _cite(5),
        },
        {
            "period": "2024–2025",
            "color": "#065F46",
            "bg": "#ECFDF5",
            "title_en": "Systematic reviews confirm effectiveness",
            "title_zh": "系统综述确认有效性",
            "body_en": (
                "A 2025 systematic review of 44 studies by Whitworth & Rose provided the broadest "
                "evidence base to date, confirming shadowing's effectiveness across diverse learner "
                "populations and contexts. A 2024 framework by Hamada & Suzuki formalized 16 technique variations "
                "and situated shadowing within deliberate practice theory."
            ),
            "body_zh": "Whitworth & Rose（2025）对44项研究进行系统综述，提供了迄今最广泛的证据基础，确认跟读法在不同学习者群体和场景中的有效性。Hamada & Suzuki（2024）整理了16种变体，并将跟读法纳入刻意练习理论框架。",
            "cite": _cite(6),
        },
    ]

    for item in timeline:
        st.markdown(
            f'<div style="display:flex;gap:14px;margin-bottom:14px;align-items:flex-start;">'
            f'<div style="min-width:80px;text-align:center;padding-top:14px;">'
            f'<div style="background:{item["color"]};color:white;border-radius:6px;'
            f'font-size:.72rem;font-weight:700;padding:4px 8px;white-space:nowrap;">{item["period"]}</div>'
            f'</div>'
            f'<div style="flex:1;border:1px solid #E5E7EB;border-left:4px solid {item["color"]};'
            f'border-radius:10px;padding:14px 18px;background:{item["bg"]};">'
            f'<div style="font-size:.9rem;font-weight:700;color:#1A3A5C;margin-bottom:2px;">'
            f'{item["title_en"]}{item["cite"]}</div>'
            f'<div style="font-size:.78rem;color:#9CA3AF;margin-bottom:8px;">{item["title_zh"]}</div>'
            f'<div style="font-size:.84rem;color:#374151;line-height:1.65;margin-bottom:5px;">{item["body_en"]}</div>'
            f'<div style="font-size:.8rem;color:#9CA3AF;line-height:1.55;">{item["body_zh"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    _ref_block([
        {"n": 1, "text": "Lambert, S. (1992). Shadowing. The Jerome Quarterly, 7(3), 5–9."},
        {"n": 2, "text": "Tamai, K. (1992). The effect of shadowing on the improvement of English listening ability. STEP Bulletin, 4, 108–118."},
        {"n": 3, "text": "Murphey, T. (2001). Exploring conversational shadowing. Language Teaching Research, 5(2), 128–155."},
        {"n": 4, "text": "Arguelles, A. Outdoor shadowing technique. Polyglot community documentation."},
        {"n": 5, "text": "Hamada, Y. (2016). Shadowing: Who benefits and how? Uncovering a booming practice. ELT Journal, 70(1), 77–87."},
        {"n": 6, "text": "Whitworth, K. & Rose, H. (2025). A systematic review of research on the use of shadowing for L2 pronunciation. Language Teaching."},
    ])


# ── Tab 3: Why it works ───────────────────────────────────────────────────────

def _tab_why():
    _section_header("Why Does Shadowing Work?", "为什么跟读法有效？", "🧬")

    st.markdown(
        '<div style="font-size:.88rem;color:#374151;line-height:1.7;margin-bottom:20px;">'
        'Four converging theories explain why simultaneous shadowing produces such consistent gains '
        'in pronunciation, prosody, and listening comprehension.<br>'
        '<span style="color:#9CA3AF;">四种理论共同解释为何同步跟读能在发音、韵律和听力理解上产生如此稳定的进步。</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    mechanisms = [
        {
            "n": "01",
            "color": "#2563EB",
            "bg": "#EFF6FF",
            "icon": "🔊",
            "en": "Phonological Loop",
            "zh": "语音回路",
            "body_en": (
                "Baddeley's working memory model includes a phonological loop — "
                "a short-term buffer that holds and rehearses speech sounds. "
                "Shadowing forces this loop to operate at full capacity: "
                "you must hold an incoming chunk just long enough to reproduce it. "
                "Repeated practice expands loop capacity, making it easier to track "
                "fast native speech in real time."
            ),
            "body_zh": "Baddeley工作记忆模型中的语音回路是一个保存并演练语音的短时缓冲区。跟读迫使语音回路满负荷运转：你必须保留刚听到的语块，足以将其复现。反复练习扩大了回路容量，使实时追踪母语快速语流变得更容易。",
            "cite": _cite(1),
        },
        {
            "n": "02",
            "color": "#0F6E56",
            "bg": "#E8F5F3",
            "icon": "🗣️",
            "en": "Motor Theory of Speech",
            "zh": "言语运动理论",
            "body_en": (
                "Perceiving and producing speech share overlapping neural pathways. "
                "The dorsal auditory stream connects the temporal cortex to Broca's area — "
                "linking what you hear to the motor commands that produce it. "
                "Shadowing repeatedly activates this perception-production loop, "
                "strengthening the articulatory programs for foreign sounds "
                "and intonation patterns."
            ),
            "body_zh": "感知语言和产出语言共享重叠的神经通路。背侧听觉流将颞叶皮层与布洛卡区相连，把你听到的声音与产生声音的运动指令联系起来。跟读反复激活这一感知-产出回路，强化外语音素和语调模式的发音程序。",
            "cite": _cite(2),
        },
        {
            "n": "03",
            "color": "#7C3AED",
            "bg": "#F5F3FF",
            "icon": "🔍",
            "en": "Noticing Hypothesis",
            "zh": "注意假说",
            "body_en": (
                "Schmidt (1990) argued that learners cannot acquire a linguistic feature "
                "unless they consciously notice it. Shadowing operationalises this: "
                "simultaneous vocalization forces deliberate attention to every incoming "
                "phoneme, stress beat, and intonation contour. "
                "You cannot shadow something you haven't noticed."
            ),
            "body_zh": "Schmidt（1990）提出，除非学习者有意识地注意到某个语言特征，否则无法习得它。跟读将这一理论付诸实践：同步发声迫使你对每一个音素、重音节拍和语调轮廓保持刻意的注意。你无法跟读你没有注意到的内容。",
            "cite": _cite(3),
        },
        {
            "n": "04",
            "color": "#B54F1A",
            "bg": "#FBF0EB",
            "icon": "⚙️",
            "en": "Automatization through Deliberate Practice",
            "zh": "通过刻意练习实现自动化",
            "body_en": (
                "Fluent speech requires automatic processing — the brain cannot consciously "
                "compute every phoneme in real time. Shadowing fits Ericsson's deliberate "
                "practice framework: it is focused, repetitive, and provides immediate "
                "implicit feedback (your voice vs. the model). "
                "Repeated sessions convert conscious phonological knowledge into "
                "procedural fluency — the kind that works when you're busy meaning what you say."
            ),
            "body_zh": "流利的语言需要自动化处理——大脑无法实时有意识地计算每个音素。跟读符合Ericsson的刻意练习框架：专注、重复，并提供即时隐性反馈（你的声音 vs 范本）。反复练习将有意识的语音知识转化为程序性流利——那种在你专注于表达意义时仍能运转的能力。",
            "cite": _cite(4),
        },
    ]

    for m in mechanisms:
        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-left:4px solid {m["color"]};'
            f'border-radius:10px;padding:18px 22px;background:{m["bg"]};margin-bottom:14px;">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">'
            f'<div style="font-size:.7rem;font-weight:800;color:{m["color"]};'
            f'background:white;border:1px solid {m["color"]};border-radius:4px;padding:2px 7px;">'
            f'{m["n"]}</div>'
            f'<div style="font-size:1rem;font-weight:700;color:#1A3A5C;">'
            f'{m["icon"]} {m["en"]}{m["cite"]}</div>'
            f'<div style="font-size:.82rem;color:#9CA3AF;">{m["zh"]}</div>'
            f'</div>'
            f'<div style="font-size:.86rem;color:#374151;line-height:1.7;margin-bottom:6px;">{m["body_en"]}</div>'
            f'<div style="font-size:.8rem;color:#9CA3AF;line-height:1.6;">{m["body_zh"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="background:#F0FDF4;border:1px solid #6EE7B7;border-radius:10px;'
        f'padding:16px 20px;margin-top:4px;">'
        f'<div style="font-size:.85rem;font-weight:700;color:#065F46;margin-bottom:6px;">'
        f'The combined effect / 四力合一</div>'
        f'<div style="font-size:.84rem;color:#374151;line-height:1.7;">'
        f'No single mechanism explains shadowing\'s effectiveness alone. It is the simultaneous '
        f'activation of all four — memory, motor, attention, and automatization — that makes '
        f'it uniquely powerful for both pronunciation and listening development.</div>'
        f'<div style="font-size:.8rem;color:#6B7280;line-height:1.6;margin-top:6px;">'
        f'没有任何单一机制能单独解释跟读的有效性。正是四种机制同时激活——记忆、运动、注意力与自动化——使其在发音和听力发展上具有独特的强大效果。</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    _ref_block([
        {"n": 1, "text": "Baddeley, A. (2000). The episodic buffer: A new component of working memory. Trends in Cognitive Sciences, 4(11), 417–423."},
        {"n": 2, "text": "Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. Nature Reviews Neuroscience, 8, 393–402."},
        {"n": 3, "text": "Schmidt, R. (1990). The role of consciousness in second language learning. Applied Linguistics, 11(2), 129–158."},
        {"n": 4, "text": "Hamada, Y. & Suzuki, A. (2024). Situating Shadowing in the Framework of Deliberate Practice. Language Teaching Research."},
    ])


# ── Tab 4: Research evidence ──────────────────────────────────────────────────

def _tab_evidence():
    _section_header("Research Evidence", "研究证据", "📊")

    st.markdown(
        '<div style="font-size:.88rem;color:#374151;line-height:1.7;margin-bottom:20px;">'
        'A growing body of controlled studies supports shadowing\'s effectiveness. '
        'Below are the most cited findings relevant to EFL pronunciation and listening.<br>'
        '<span style="color:#9CA3AF;">越来越多的对照研究支持跟读法的有效性。以下是与EFL发音和听力最相关的研究发现。</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Key metrics row
    metrics = [
        ("44", "studies reviewed", "项研究综述", "#2563EB", "#EFF6FF"),
        ("38.6%", "avg fluency gain", "平均流利度提升", "#0F6E56", "#E8F5F3"),
        ("6 weeks", "to see results", "即可见效", "#7C3AED", "#F5F3FF"),
    ]
    cols = st.columns(3)
    for col, (val, label_en, label_zh, color, bg) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div style="text-align:center;border:1px solid #E5E7EB;border-radius:10px;'
                f'padding:18px 12px;background:{bg};">'
                f'<div style="font-size:2rem;font-weight:800;color:{color};">{val}</div>'
                f'<div style="font-size:.8rem;font-weight:600;color:#374151;margin-top:4px;">{label_en}</div>'
                f'<div style="font-size:.75rem;color:#9CA3AF;">{label_zh}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    studies = [
        {
            "year": "2016",
            "color": "#2563EB",
            "bg": "#F0F6FF",
            "authors": "Hamada, Y.",
            "title_en": "Shadowing for EFL listening: phoneme perception gains",
            "title_zh": "跟读对EFL听力的影响：音素感知提升",
            "design": "43 Japanese EFL learners · 6 weeks · 10–15 min/day",
            "design_zh": "43名日本EFL学习者 · 6周 · 每天10–15分钟",
            "findings": [
                "Significant gains in phoneme perception for both proficiency groups",
                "Lower-proficiency learners showed the largest listening comprehension gains",
                "Established 15–20 min daily practice as optimal session length",
            ],
            "findings_zh": [
                "两个水平组的音素感知均有显著提升",
                "低水平学习者在听力理解上取得了最大进步",
                "确立每天15–20分钟为最佳练习时长",
            ],
            "cite": _cite(1),
        },
        {
            "year": "2017",
            "color": "#0F6E56",
            "bg": "#E8F5F3",
            "authors": "Foote, J. & McDonough, K.",
            "title_en": "Mobile shadowing for pronunciation and fluency",
            "title_zh": "移动端跟读对发音和流利度的影响",
            "design": "ESL learners · 8 weeks · ≥4 sessions/week, ≥10 min/session",
            "design_zh": "ESL学习者 · 8周 · 每周≥4次，每次≥10分钟",
            "findings": [
                "Significant improvements in pronunciation accuracy",
                "Gains in prosodic fluency (rhythm, intonation, stress)",
                "Results replicated in a mobile/app-based learning context",
            ],
            "findings_zh": [
                "发音准确性显著提升",
                "韵律流利度（节奏、语调、重音）有所改善",
                "在移动/应用学习场景中结果得到复现",
            ],
            "cite": _cite(2),
        },
        {
            "year": "2024",
            "color": "#7C3AED",
            "bg": "#F5F3FF",
            "authors": "Hamada, Y. & Suzuki, A.",
            "title_en": "Deliberate practice framework for 16 shadowing techniques",
            "title_zh": "16种跟读变体的刻意练习理论框架",
            "design": "Theoretical framework + empirical validation",
            "design_zh": "理论框架 + 实证验证",
            "findings": [
                "Identified 16 distinct shadowing variations organized into 2 categories",
                "Situated shadowing within Ericsson's deliberate practice theory",
                "Provided evidence-based guidance for technique selection and sequencing",
            ],
            "findings_zh": [
                "归纳出16种跟读变体，分为2大类",
                "将跟读法纳入Ericsson刻意练习理论",
                "为技术选择和顺序排列提供了基于证据的指导",
            ],
            "cite": _cite(3),
        },
        {
            "year": "2025",
            "color": "#065F46",
            "bg": "#ECFDF5",
            "authors": "Whitworth, K. & Rose, H.",
            "title_en": "Systematic review of 44 shadowing studies",
            "title_zh": "44项跟读研究的系统综述",
            "design": "Systematic review · 44 controlled studies · cross-population",
            "design_zh": "系统综述 · 44项对照研究 · 跨群体",
            "findings": [
                "Shadowing effective for pronunciation across diverse learner populations",
                "Fluency gains (38.6%) exceed pronunciation gains (31.0%) on average",
                "Evidence base now mature enough to inform curriculum design",
            ],
            "findings_zh": [
                "跟读法在不同学习者群体中对发音均有效",
                "流利度提升（38.6%）平均超过发音提升（31.0%）",
                "证据基础已足够成熟，可指导课程设计",
            ],
            "cite": _cite(4),
        },
    ]

    for s in studies:
        findings_en = "".join(
            f'<li style="margin-bottom:4px;">{f}</li>' for f in s["findings"]
        )
        findings_zh = "".join(
            f'<li style="margin-bottom:3px;color:#9CA3AF;">{f}</li>' for f in s["findings_zh"]
        )
        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-left:4px solid {s["color"]};'
            f'border-radius:10px;padding:16px 20px;background:{s["bg"]};margin-bottom:14px;">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
            f'<span style="background:{s["color"]};color:white;font-size:.72rem;font-weight:700;'
            f'border-radius:4px;padding:2px 8px;">{s["year"]}</span>'
            f'<span style="font-size:.82rem;font-weight:600;color:#6B7280;">{s["authors"]}</span>'
            f'{s["cite"]}'
            f'</div>'
            f'<div style="font-size:.92rem;font-weight:700;color:#1A3A5C;margin-bottom:2px;">{s["title_en"]}</div>'
            f'<div style="font-size:.78rem;color:#9CA3AF;margin-bottom:10px;">{s["title_zh"]}</div>'
            f'<div style="font-size:.76rem;color:#6B7280;margin-bottom:8px;">'
            f'Study design: {s["design"]}<br><span style="color:#D1D5DB;">{s["design_zh"]}</span></div>'
            f'<ul style="font-size:.84rem;color:#374151;line-height:1.65;'
            f'margin:0;padding-left:18px;">{findings_en}</ul>'
            f'<ul style="font-size:.78rem;line-height:1.55;margin-top:4px;'
            f'padding-left:18px;">{findings_zh}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:8px;'
        'padding:12px 16px;font-size:.84rem;color:#92400E;margin-top:4px;">'
        '<strong>What the evidence does NOT yet show / 证据尚未解答的问题</strong><br>'
        'Most studies rely on controlled speaking tasks, not spontaneous production. '
        'The transfer from shadowing practice to natural conversation is plausible but needs more research.'
        '<br><span style="color:#B45309;">'
        '大多数研究依赖控制性口语任务，而非自发性产出。跟读练习向自然会话的迁移具有理论合理性，但仍需更多研究。'
        '</span></div>',
        unsafe_allow_html=True,
    )

    _ref_block([
        {"n": 1, "text": "Hamada, Y. (2016). Shadowing: Who benefits and how? ELT Journal, 70(1), 77–87."},
        {"n": 2, "text": "Foote, J. & McDonough, K. (2017). Using shadowing with mobile technology to improve L2 pronunciation. Journal of Second Language Pronunciation, 3(1)."},
        {"n": 3, "text": "Hamada, Y. & Suzuki, A. (2024). Shadowing in the framework of deliberate practice. Language Teaching Research."},
        {"n": 4, "text": "Whitworth, K. & Rose, H. (2025). A systematic review of research on the use of shadowing for L2 pronunciation. Language Teaching."},
    ])


# ── Tab 5: ShadowingLab 5-phase interactive guide ────────────────────────────

# ── Phase data ────────────────────────────────────────────────────────────────

_PHASES = [
    {
        "num": 1, "icon": "🎯", "en": "Select", "zh": "选材料",
        "color": "#2563EB", "bg": "#EFF6FF", "border": "#BFDBFE",
        "tagline_en": "Pick material that stretches you without overwhelming you.",
        "tagline_zh": "选一个能拉伸但不压垮你的材料。",
        "action_title_en": "What you do",
        "action_title_zh": "你做什么",
        "action_en": (
            "Browse the material library and choose an audio clip. "
            "Filter by topic, difficulty, or length. "
            "ShadowingLab shows duration and content tags to help you match your level."
        ),
        "action_zh": "浏览材料库，选择一段音频。可以按话题、难度或时长筛选。ShadowingLab 展示时长和内容标签，帮助你找到适合当前水平的材料。",
        "principle_en": (
            "Krashen's i+1 hypothesis: input slightly above your current level drives acquisition. "
            "If you understand 70–80% on first listen, the material is well-calibrated. "
            "Too easy means no cognitive engagement; too hard means the phonological loop is overwhelmed before shadowing begins."
        ),
        "principle_zh": "Krashen i+1 假说：略高于当前水平的输入驱动习得。初次聆听能听懂七八成说明材料难度合适。太简单则缺乏认知参与，太难则在跟读开始前语音回路已被压垮。",
        "tips_en": [
            "Shorter is better — 30–60 seconds of dense native speech is plenty for one session.",
            "Repeat the same material across sessions — fluency builds through repetition, not novelty.",
            "Familiar topics let you focus on how things are said, not just what.",
        ],
        "tips_zh": [
            "短一点更好——30–60秒真实语速材料，一次练习已经足够。",
            "同一篇材料多次练习没问题——流利度靠重复积累，不必不断换新材料。",
            "熟悉的话题能让你专注于「怎么说」而不只是「说了什么」。",
        ],
        "mockup": (
            '<div style="border:1px solid #BFDBFE;border-radius:8px;padding:12px;background:white;font-size:.75rem;">'
            '<div style="color:#6B7280;margin-bottom:8px;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Material Library</div>'
            '<div style="display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap;">'
            '<span style="background:#DBEAFE;color:#1D4ED8;border-radius:4px;padding:2px 7px;font-size:.68rem;">Interview</span>'
            '<span style="background:#D1FAE5;color:#065F46;border-radius:4px;padding:2px 7px;font-size:.68rem;">News</span>'
            '<span style="background:#EDE9FE;color:#5B21B6;border-radius:4px;padding:2px 7px;font-size:.68rem;">Conversation</span>'
            '</div>'
            '<div style="border:1px solid #E5E7EB;border-radius:6px;padding:8px 10px;margin-bottom:6px;background:#F9FAFB;">'
            '<div style="font-weight:600;color:#1A3A5C;margin-bottom:3px;">How language shapes thought</div>'
            '<div style="display:flex;gap:6px;align-items:center;">'
            '<span style="background:#DBEAFE;color:#1D4ED8;border-radius:3px;padding:1px 6px;font-size:.66rem;">Interview</span>'
            '<span style="color:#9CA3AF;font-size:.68rem;">45 sec · Intermediate</span>'
            '</div></div>'
            '<div style="border:2px solid #2563EB;border-radius:6px;padding:8px 10px;background:#EFF6FF;">'
            '<div style="font-weight:600;color:#1D4ED8;margin-bottom:3px;">The silent takeover of the office</div>'
            '<div style="display:flex;gap:6px;align-items:center;">'
            '<span style="background:#EDE9FE;color:#5B21B6;border-radius:3px;padding:1px 6px;font-size:.66rem;">Conversation</span>'
            '<span style="color:#9CA3AF;font-size:.68rem;">38 sec · Upper-intermediate</span>'
            '</div></div>'
            '</div>'
        ),
    },
    {
        "num": 2, "icon": "📖", "en": "Prepare", "zh": "预习",
        "color": "#0F6E56", "bg": "#E8F5F3", "border": "#6EE7B7",
        "tagline_en": "Read for meaning. Study the phonological map. Prime your articulators.",
        "tagline_zh": "先读懂意思，研究语音标注，给发音器官热身。",
        "action_title_en": "What you do",
        "action_title_zh": "你做什么",
        "action_en": (
            "Read the transcript while listening to the audio once through. "
            "Study the inline phonological annotations — stress marks (●), "
            "linking arcs (⌢), weak-form labels, and intonation arrows. "
            "Look up any unknown words before you start shadowing."
        ),
        "action_zh": "边听音频边阅读文本，先完整听一遍。研究行内语音标注——重音（●）、连读弧线（⌢）、弱读标签和语调箭头。在开始跟读前查好所有不认识的词。",
        "principle_en": (
            "Cognitive Load Theory (Sweller): shadowing demands full attention on sound. "
            "Resolving vocabulary and grammar in Prepare offloads that burden, "
            "so your working memory is free to focus entirely on phonological imitation during Phase 3."
        ),
        "principle_zh": "认知负荷理论（Sweller）：跟读需要全部注意力集中在声音上。在预习阶段解决词汇和语法，释放工作记忆，让第三阶段能完全专注于语音模仿。",
        "tips_en": [
            "Punctuation = rhythm cues. Commas signal brief pauses; full stops signal falling intonation.",
            "Mouth the words quietly before the first listen — it primes your articulators.",
            "Focus on the annotation labels, not just the words. They tell you where native speakers compress speech.",
        ],
        "tips_zh": [
            "标点是节奏信号。逗号意味着短暂停顿，句号意味着降调。",
            "第一遍听之前先轻声试读——给发音器官提前热身。",
            "关注标注标签，不只是文字本身。它们标出了母语者压缩语流的地方。",
        ],
        "mockup": (
            '<div style="border:1px solid #6EE7B7;border-radius:8px;padding:12px;background:white;font-size:.75rem;">'
            '<div style="color:#0F6E56;margin-bottom:8px;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Annotated Transcript</div>'
            '<div style="background:#F0FDF4;border-radius:6px;padding:10px;margin-bottom:8px;line-height:1.9;">'
            '<span style="color:#374151;">The </span>'
            '<span style="background:#FFFBEB;color:#92400E;font-size:.68rem;font-weight:700;border-radius:3px;padding:1px 4px;margin-right:2px;">●</span>'
            '<span style="font-weight:600;color:#1A3A5C;">si·lent </span>'
            '<span style="color:#374151;">ta</span>'
            '<span style="background:#DBEAFE;color:#1D4ED8;font-size:.68rem;font-weight:700;border-radius:3px;padding:1px 4px;margin:0 2px;">⌢</span>'
            '<span style="font-weight:600;color:#1A3A5C;">ke·over</span>'
            '<span style="color:#374151;"> of the </span>'
            '<span style="background:#EDE9FE;color:#5B21B6;font-size:.68rem;font-weight:700;border-radius:3px;padding:1px 4px;margin-right:2px;">wk</span>'
            '<span style="color:#6B7280;">office</span>'
            '<span style="color:#9CA3AF;margin-left:4px;">↘</span>'
            '</div>'
            '<div style="display:flex;align-items:center;gap:6px;background:#E8F5F3;border-radius:5px;padding:6px 8px;">'
            '<div style="width:20px;height:20px;border-radius:50%;background:#0F6E56;display:flex;align-items:center;justify-content:center;color:white;font-size:.7rem;flex-shrink:0;">▶</div>'
            '<div style="flex:1;height:4px;background:#A7F3D0;border-radius:2px;position:relative;">'
            '<div style="width:40%;height:100%;background:#0F6E56;border-radius:2px;"></div>'
            '</div>'
            '<span style="color:#6B7280;font-size:.68rem;">0:18 / 0:38</span>'
            '</div>'
            '</div>'
        ),
    },
    {
        "num": 3, "icon": "🎙️", "en": "Shadow", "zh": "跟读",
        "color": "#7C3AED", "bg": "#F5F3FF", "border": "#DDD6FE",
        "tagline_en": "Speak simultaneously. Chase the speaker's voice.",
        "tagline_zh": "同步发声，追着说话者的声音走。",
        "action_title_en": "What you do",
        "action_title_zh": "你做什么",
        "action_en": (
            "Play the audio and shadow simultaneously — your voice runs in parallel with the speaker's. "
            "ShadowingLab auto-records each attempt. "
            "Work sentence by sentence: listen once, then shadow 2–3 times at progressively fuller voice. "
            "Stay less than half a second behind. If you miss a word, skip it and keep going."
        ),
        "action_zh": "播放音频并同步跟读——你的声音与说话者并行。ShadowingLab 自动录制每次尝试。逐句进行：先听一遍，再以逐渐增大的音量跟读2–3遍。保持落后说话者不超过半秒。漏了词就跳过，保持节奏。",
        "principle_en": (
            "This is where the four mechanisms converge: the phonological loop is forced to capacity, "
            "the motor-perception pathway activates, Schmidt's noticing is operationalised, "
            "and each repetition accumulates toward automatization. "
            "The simultaneous constraint — not allowed to pause — is what makes shadowing different from all other imitation drills."
        ),
        "principle_zh": "四种机制在此汇合：语音回路被迫满负荷运转，运动-感知通路激活，Schmidt的注意机制付诸实践，每次重复都在向自动化积累。同步约束——不允许暂停——正是跟读法区别于所有其他模仿练习的关键。",
        "tips_en": [
            "Shadow the music, not just the words — mimic rises and falls in pitch, speed changes, pauses.",
            "It's okay to sound strange. Discomfort means you're pushing past your current habits.",
            "Repeat difficult sentences 2–3 times back to back before moving on.",
        ],
        "tips_zh": [
            "跟读「音乐」，不只是文字——模仿语调起伏、速度变化和停顿。",
            "听起来奇怪是正常的。不适感说明你在突破现有习惯。",
            "难的句子连续重复2–3遍再继续。",
        ],
        "mockup": (
            '<div style="border:1px solid #DDD6FE;border-radius:8px;padding:12px;background:white;font-size:.75rem;">'
            '<div style="color:#7C3AED;margin-bottom:8px;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Shadow · Sentence 2 of 6</div>'
            '<div style="background:#DBEAFE;border-left:4px solid #2563EB;border-radius:5px;padding:8px 10px;margin-bottom:8px;">'
            '<span style="font-weight:600;color:#1A3A5C;font-size:.82rem;">The silent takeover of the office</span>'
            '</div>'
            '<div style="display:flex;gap:6px;margin-bottom:8px;">'
            '<div style="flex:1;background:#F3F4F6;border-radius:5px;padding:6px 8px;display:flex;align-items:center;gap:5px;">'
            '<div style="width:16px;height:16px;border-radius:50%;background:#7C3AED;display:flex;align-items:center;justify-content:center;color:white;font-size:.6rem;">▶</div>'
            '<div style="font-size:.68rem;color:#6B7280;">Original</div>'
            '<div style="flex:1;height:3px;background:#E5E7EB;border-radius:2px;">'
            '<div style="width:60%;height:100%;background:#7C3AED;border-radius:2px;"></div>'
            '</div>'
            '</div>'
            '</div>'
            '<div style="display:flex;align-items:center;justify-content:center;gap:8px;background:#FDF4FF;border:1px solid #DDD6FE;border-radius:6px;padding:8px;">'
            '<div style="width:28px;height:28px;border-radius:50%;background:#EF4444;display:flex;align-items:center;justify-content:center;color:white;font-size:.8rem;">●</div>'
            '<div style="font-size:.72rem;color:#7C3AED;font-weight:600;">Recording attempt 2/3…</div>'
            '</div>'
            '</div>'
        ),
    },
    {
        "num": 4, "icon": "🔍", "en": "Compare", "zh": "对比",
        "color": "#B54F1A", "bg": "#FBF0EB", "border": "#FCD9BD",
        "tagline_en": "Listen back. Find the gap between your voice and the model.",
        "tagline_zh": "回听，找出你的声音和范本之间的差距。",
        "action_title_en": "What you do",
        "action_title_zh": "你做什么",
        "action_en": (
            "Play your recording and the original side by side. "
            "Listen for rhythm first — did your stress land on the same syllables? Did your pauses match? "
            "Find one specific moment that surprised you and log it as a Notice."
        ),
        "action_zh": "将你的录音和原声并排播放对比。先听节奏——重音落在相同音节上了吗？停顿一致吗？找到一个让你意外的具体时刻，将它记录为一条发现。",
        "principle_en": (
            "This phase operationalises Schmidt's Noticing Hypothesis: "
            "learners cannot acquire a feature they haven't consciously noticed. "
            "The comparison creates a gap — your ear hears the difference between what you produced "
            "and what you intended. That gap is the acquisition trigger."
        ),
        "principle_zh": "这个阶段实践了Schmidt的注意假说：学习者无法习得他们没有有意识注意到的特征。对比制造了一个差距——你的耳朵听到了你产出的和你意图产出的之间的区别。这个差距就是习得的触发器。",
        "tips_en": [
            "Listen for rhythm first, sounds second — stress and pause differences are usually bigger than vowel differences.",
            "Your accent is not the problem. You're training your ear, not auditioning.",
            "Use the timestamp scrubber — replay just the 2-second moment that surprised you.",
        ],
        "tips_zh": [
            "先听节奏，再听音——重音和停顿的差距通常比元音差距更大。",
            "你的口音不是问题。这是在训练耳朵，不是在试镜。",
            "用时间轴定位——只回听那个让你意外的2秒时刻。",
        ],
        "mockup": (
            '<div style="border:1px solid #FCD9BD;border-radius:8px;padding:12px;background:white;font-size:.75rem;">'
            '<div style="color:#B54F1A;margin-bottom:8px;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Compare</div>'
            '<div style="display:flex;flex-direction:column;gap:5px;margin-bottom:8px;">'
            '<div style="background:#F9FAFB;border-radius:5px;padding:6px 8px;display:flex;align-items:center;gap:6px;">'
            '<span style="font-size:.68rem;color:#6B7280;min-width:52px;">Original</span>'
            '<div style="flex:1;height:18px;background:#FEF3C7;border-radius:3px;overflow:hidden;position:relative;">'
            '<div style="position:absolute;top:2px;left:0;right:0;display:flex;align-items:center;padding:0 4px;gap:1px;">'
            + ''.join([f'<div style="width:3px;background:#F59E0B;border-radius:1px;height:{h}px;"></div>' for h in [6,10,14,8,12,16,10,6,14,12,8,16,10,6,12,14,8,10,6,12]]) +
            '</div></div>'
            '</div>'
            '<div style="background:#F5F3FF;border-radius:5px;padding:6px 8px;display:flex;align-items:center;gap:6px;">'
            '<span style="font-size:.68rem;color:#7C3AED;min-width:52px;font-weight:600;">Your shadow</span>'
            '<div style="flex:1;height:18px;background:#EDE9FE;border-radius:3px;overflow:hidden;position:relative;">'
            '<div style="position:absolute;top:2px;left:0;right:0;display:flex;align-items:center;padding:0 4px;gap:1px;">'
            + ''.join([f'<div style="width:3px;background:#7C3AED;border-radius:1px;height:{h}px;"></div>' for h in [4,8,10,6,14,12,8,4,10,14,6,12,8,4,10,12,6,8,4,10]]) +
            '</div></div>'
            '</div>'
            '</div>'
            '<div style="background:#FFFBEB;border:1px solid #FEF3C7;border-radius:5px;padding:6px 8px;">'
            '<div style="font-size:.68rem;color:#92400E;margin-bottom:3px;font-weight:600;">📋 Log a notice</div>'
            '<div style="background:white;border:1px solid #E5E7EB;border-radius:4px;padding:4px 6px;color:#9CA3AF;font-size:.68rem;">I noticed that "takeover" — my stress was on the wrong syllable…</div>'
            '</div>'
            '</div>'
        ),
    },
    {
        "num": 5, "icon": "📋", "en": "Capture", "zh": "记录",
        "color": "#065F46", "bg": "#ECFDF5", "border": "#6EE7B7",
        "tagline_en": "Name what you noticed. Tag it. Build your pattern library.",
        "tagline_zh": "命名你的发现，打上标签，积累你的规律库。",
        "action_title_en": "What you do",
        "action_title_zh": "你做什么",
        "action_en": (
            "Write down what you noticed — the specific phonological feature, the word, the moment. "
            "Tag it (stress / linking / weak form / intonation / rhythm). "
            "The Notice Log accumulates across sessions, letting you track which patterns keep appearing."
        ),
        "action_zh": "写下你注意到的——具体的语音特征、词语、时刻。给它打上标签（重音/连读/弱读/语调/节奏）。发现记录在多次练习中积累，让你追踪哪些规律反复出现。",
        "principle_en": (
            "Encoding specificity (Tulving): memory for a feature is strongest when retrieval conditions "
            "match encoding conditions. Naming and tagging the notice at the moment of discovery "
            "creates a retrievable memory trace. "
            "Over sessions, patterns emerge — and patterns are what you actually practice next."
        ),
        "principle_zh": "编码特异性原则（Tulving）：当提取条件与编码条件匹配时，对特征的记忆最为牢固。在发现时命名并标记，创建可检索的记忆痕迹。随着练习积累，规律浮现——而规律正是你下次实际要练习的东西。",
        "tips_en": [
            "A notice is an observation, not a mistake — write what you noticed, not what you 'should' have done.",
            "Be specific: name the word, the feature, the moment. Vague notices don't help later.",
            "One session, one pattern — if the same thing recurs three times, write it once, clearly.",
        ],
        "tips_zh": [
            "发现是观察，不是错误——写下你注意到的，而不是你「应该」做到的。",
            "要具体：写清楚是哪个词、哪个现象、哪个时刻。模糊的记录日后没有参考价值。",
            "一次练习，找一个规律——同一个问题出现三次，清晰地写一条就够了。",
        ],
        "mockup": (
            '<div style="border:1px solid #6EE7B7;border-radius:8px;padding:12px;background:white;font-size:.75rem;">'
            '<div style="color:#065F46;margin-bottom:8px;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Notice Log · This session</div>'
            '<div style="display:flex;flex-direction:column;gap:5px;margin-bottom:8px;">'
            '<div style="border:1px solid #E5E7EB;border-radius:5px;padding:6px 8px;background:#F9FAFB;">'
            '<div style="display:flex;align-items:center;gap:5px;margin-bottom:2px;">'
            '<span style="background:#FFFBEB;color:#92400E;font-size:.64rem;font-weight:700;border-radius:3px;padding:1px 5px;">stress</span>'
            '<span style="font-size:.7rem;color:#374151;">"ta·<strong>ke</strong>·over" — stress on wrong syllable</span>'
            '</div></div>'
            '<div style="border:1px solid #E5E7EB;border-radius:5px;padding:6px 8px;background:#F9FAFB;">'
            '<div style="display:flex;align-items:center;gap:5px;margin-bottom:2px;">'
            '<span style="background:#DBEAFE;color:#1D4ED8;font-size:.64rem;font-weight:700;border-radius:3px;padding:1px 5px;">linking</span>'
            '<span style="font-size:.7rem;color:#374151;">"of_the" — I paused between these</span>'
            '</div></div>'
            '</div>'
            '<div style="display:flex;justify-content:space-between;background:#ECFDF5;border-radius:5px;padding:6px 8px;">'
            '<span style="font-size:.68rem;color:#065F46;font-weight:600;">Session complete ✓</span>'
            '<span style="font-size:.68rem;color:#6B7280;">2 notices · 3 sentences shadowed</span>'
            '</div>'
            '</div>'
        ),
    },
]


def _phase_node_html(p, is_active, is_first_visit_hint):
    """Render a single timeline node (visual only — interaction via st.button)."""
    if is_active:
        dot_bg = p["color"]
        dot_border = p["color"]
        dot_color = "white"
        label_color = p["color"]
        label_weight = "700"
        shadow = f"box-shadow:0 0 0 3px {p['border']};"
    else:
        dot_bg = "white"
        dot_border = "#D1D5DB"
        dot_color = "#9CA3AF"
        label_color = "#9CA3AF"
        label_weight = "500"
        shadow = ""
    hint = ""
    if is_first_visit_hint and not is_active:
        hint = f'<div style="font-size:.6rem;color:#D1D5DB;margin-top:2px;">click to explore</div>'
    return (
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:60px;">'
        f'<div style="width:36px;height:36px;border-radius:50%;background:{dot_bg};'
        f'border:2px solid {dot_border};{shadow}'
        f'display:flex;align-items:center;justify-content:center;font-size:1rem;">'
        f'{p["icon"]}</div>'
        f'<div style="font-size:.72rem;font-weight:{label_weight};color:{label_color};text-align:center;">{p["en"]}</div>'
        f'<div style="font-size:.65rem;color:#D1D5DB;text-align:center;">{p["zh"]}</div>'
        f'{hint}'
        f'</div>'
    )


def _render_phase_timeline(selected_num, first_visit):
    """Render the visual timeline rail + connector lines."""
    nodes_html = ""
    for i, p in enumerate(_PHASES):
        is_active = p["num"] == selected_num
        nodes_html += _phase_node_html(p, is_active, first_visit)
        if i < len(_PHASES) - 1:
            line_color = "#E5E7EB"
            nodes_html += (
                f'<div style="flex:1;height:2px;background:{line_color};'
                f'margin-top:17px;min-width:8px;max-width:40px;"></div>'
            )
    st.markdown(
        f'<div style="display:flex;align-items:flex-start;justify-content:center;'
        f'gap:0;padding:8px 0 4px;overflow-x:auto;">'
        f'{nodes_html}</div>',
        unsafe_allow_html=True,
    )


def _render_phase_buttons(selected_num):
    """5 invisible-ish buttons that control the selected phase."""
    cols = st.columns(5)
    for i, p in enumerate(_PHASES):
        with cols[i]:
            is_active = p["num"] == selected_num
            btn_type = "primary" if is_active else "secondary"
            if st.button(
                p["en"],
                key=f"about_phase_{p['num']}",
                use_container_width=True,
                type=btn_type,
            ):
                st.session_state["about_phase_sel"] = p["num"]
                st.session_state["about_first_visit"] = False
                st.rerun()


def _render_phase_detail(p):
    """Render the detail panel for the selected phase."""
    st.markdown(
        f'<div style="border:1px solid {p["border"]};border-left:4px solid {p["color"]};'
        f'border-radius:12px;padding:20px 24px;background:{p["bg"]};margin-top:4px;">'
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
        f'<div style="font-size:1.5rem;">{p["icon"]}</div>'
        f'<div>'
        f'<div style="font-size:1rem;font-weight:700;color:{p["color"]};">Phase {p["num"]} · {p["en"]} / {p["zh"]}</div>'
        f'<div style="font-size:.82rem;color:#6B7280;margin-top:2px;">{p["tagline_en"]}</div>'
        f'<div style="font-size:.78rem;color:#9CA3AF;">{p["tagline_zh"]}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # What you do
        st.markdown(
            f'<div style="font-size:.8rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.05em;color:{p["color"]};margin:16px 0 6px;">'
            f'{p["action_title_en"]} / {p["action_title_zh"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:.86rem;color:#374151;line-height:1.7;margin-bottom:4px;">{p["action_en"]}</div>'
            f'<div style="font-size:.8rem;color:#9CA3AF;line-height:1.6;">{p["action_zh"]}</div>',
            unsafe_allow_html=True,
        )

        # Cognitive principle
        st.markdown(
            f'<div style="font-size:.8rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.05em;color:{p["color"]};margin:14px 0 6px;">'
            f'Why this step works / 认知原理</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="background:white;border:1px solid {p["border"]};border-radius:8px;'
            f'padding:12px 14px;">'
            f'<div style="font-size:.84rem;color:#374151;line-height:1.7;margin-bottom:4px;">{p["principle_en"]}</div>'
            f'<div style="font-size:.78rem;color:#9CA3AF;line-height:1.6;">{p["principle_zh"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Tips
        st.markdown(
            f'<div style="font-size:.8rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.05em;color:{p["color"]};margin:14px 0 6px;">'
            f'Tips from the coach / 练习建议</div>',
            unsafe_allow_html=True,
        )
        tips_html = "".join(
            f'<div style="display:flex;gap:8px;margin-bottom:6px;">'
            f'<span style="color:{p["color"]};flex-shrink:0;">›</span>'
            f'<div>'
            f'<div style="font-size:.82rem;color:#374151;line-height:1.6;">{en}</div>'
            f'<div style="font-size:.76rem;color:#9CA3AF;line-height:1.5;">{zh}</div>'
            f'</div></div>'
            for en, zh in zip(p["tips_en"], p["tips_zh"])
        )
        st.markdown(tips_html, unsafe_allow_html=True)

    with col_right:
        st.markdown(
            f'<div style="font-size:.8rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.05em;color:{p["color"]};margin:16px 0 8px;">'
            f'Interface preview / 界面示意</div>',
            unsafe_allow_html=True,
        )
        st.markdown(p["mockup"], unsafe_allow_html=True)

        # Nav hints
        prev_num = p["num"] - 1
        next_num = p["num"] + 1
        nav_html = '<div style="display:flex;gap:6px;margin-top:10px;">'
        if prev_num >= 1:
            prev = _PHASES[prev_num - 1]
            nav_html += (
                f'<div style="flex:1;background:white;border:1px solid #E5E7EB;border-radius:6px;'
                f'padding:6px 8px;text-align:center;">'
                f'<div style="font-size:.65rem;color:#9CA3AF;">← prev</div>'
                f'<div style="font-size:.72rem;font-weight:600;color:#6B7280;">{prev["icon"]} {prev["en"]}</div>'
                f'</div>'
            )
        if next_num <= 5:
            nxt = _PHASES[next_num - 1]
            nav_html += (
                f'<div style="flex:1;background:white;border:1px solid #E5E7EB;border-radius:6px;'
                f'padding:6px 8px;text-align:center;">'
                f'<div style="font-size:.65rem;color:#9CA3AF;">next →</div>'
                f'<div style="font-size:.72rem;font-weight:600;color:#6B7280;">{nxt["icon"]} {nxt["en"]}</div>'
                f'</div>'
            )
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)


def _render_overview():
    """Full overview: all 5 phases in a compact grid."""
    st.markdown(
        '<div style="font-size:.82rem;color:#6B7280;margin-bottom:16px;line-height:1.6;">'
        'One session = five phases, in sequence. Each phase has a distinct cognitive purpose. '
        'The cycle takes 20–30 minutes.<br>'
        '<span style="color:#D1D5DB;">一次练习 = 五个阶段，按顺序进行。每个阶段有独立的认知目的。完整流程约20–30分钟。</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    for p in _PHASES:
        st.markdown(
            f'<div style="display:flex;gap:14px;align-items:flex-start;'
            f'border:1px solid {p["border"]};border-left:4px solid {p["color"]};'
            f'border-radius:10px;padding:14px 18px;background:{p["bg"]};margin-bottom:10px;">'
            f'<div style="font-size:1.6rem;flex-shrink:0;padding-top:2px;">{p["icon"]}</div>'
            f'<div style="flex:1;">'
            f'<div style="font-size:.88rem;font-weight:700;color:{p["color"]};margin-bottom:2px;">'
            f'Phase {p["num"]} · {p["en"]} / {p["zh"]}</div>'
            f'<div style="font-size:.82rem;color:#374151;line-height:1.6;margin-bottom:3px;">{p["action_en"]}</div>'
            f'<div style="font-size:.76rem;color:#9CA3AF;line-height:1.5;">{p["action_zh"]}</div>'
            f'</div>'
            f'<div style="font-size:1.4rem;flex-shrink:0;color:#D1D5DB;padding-top:8px;">'
            f'{"›" if p["num"] < 5 else "✓"}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _tab_howto():
    _section_header("How ShadowingLab Guides Your Practice", "ShadowingLab 怎么辅助练习？", "🗺️")

    # ── Init session state ────────────────────────────────────────────────
    if "about_phase_sel" not in st.session_state:
        st.session_state["about_phase_sel"] = 1
    if "about_first_visit" not in st.session_state:
        st.session_state["about_first_visit"] = True
    if "about_view_mode" not in st.session_state:
        st.session_state["about_view_mode"] = "detail"

    sel = st.session_state["about_phase_sel"]
    first_visit = st.session_state["about_first_visit"]
    view_mode = st.session_state["about_view_mode"]

    # ── View mode toggle (top-right) ──────────────────────────────────────
    col_title, col_toggle = st.columns([3, 1])
    with col_toggle:
        if view_mode == "detail":
            if st.button("☰ Full overview / 完整流程", use_container_width=True, key="about_toggle_overview"):
                st.session_state["about_view_mode"] = "overview"
                st.rerun()
        else:
            if st.button("← Phase detail / 分阶段", use_container_width=True, key="about_toggle_detail"):
                st.session_state["about_view_mode"] = "detail"
                st.rerun()

    if view_mode == "overview":
        _render_overview()
        return

    # ── Detail mode: timeline + detail panel ─────────────────────────────
    if first_visit:
        st.markdown(
            '<div style="background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:8px;'
            'padding:8px 14px;font-size:.82rem;color:#92400E;margin-bottom:8px;">'
            'Click any phase below to explore it · 点击下方任意阶段了解详情</div>',
            unsafe_allow_html=True,
        )

    _render_phase_timeline(sel, first_visit)
    _render_phase_buttons(sel)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    current_phase = _PHASES[sel - 1]
    _render_phase_detail(current_phase)


# ── Entry point ───────────────────────────────────────────────────────────────

def about_page():
    st.title("📚 About Shadowing")
    st.markdown(
        '<p style="color:#6B7280;margin-top:-8px;margin-bottom:24px;">'
        'The science and method behind ShadowingLab · 跟读法的原理与方法</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 Definition / 定义",
        "🕰️ Origin / 起源",
        "🧬 Why it works / 为什么有效",
        "📊 Evidence / 研究证据",
        "🗺️ ShadowingLab / 怎么练",
    ])

    with tab1:
        _tab_definition()
    with tab2:
        _tab_origin()
    with tab3:
        _tab_why()
    with tab4:
        _tab_evidence()
    with tab5:
        _tab_howto()
