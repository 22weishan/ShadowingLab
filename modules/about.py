"""
about.py — About Shadowing: Science & Method
=============================================
Five-tab science communication page covering:
  1. Definition — what shadowing is
  2. Origin — where it came from
  3. Why it works — theoretical mechanisms
  4. Research evidence — key studies and data
  5. How to do it right — best practices
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


# ── Tab 5: How to do it right ─────────────────────────────────────────────────

def _tab_howto():
    _section_header("How to Shadow Correctly", "怎么做才对？", "✅")

    c1 = _cite(1)

    # Stage 1: Voice level
    st.markdown(
        '<div style="font-size:.85rem;font-weight:700;color:#1A3A5C;margin-bottom:10px;">'
        '1 · Voice level progression / 发声阶段递进</div>',
        unsafe_allow_html=True,
    )
    voice_stages = [
        ("Silent mouthing", "无声口型", "#6B7280", "#F9FAFB",
         "Mouth the words without sound. Use this when the material is very new or fast. Builds physical familiarity with articulation patterns.",
         "无声地做嘴型。用于材料非常陌生或语速过快时。培养发音动作的肌肉记忆。"),
        ("Whisper shadowing", "低声跟读", "#2563EB", "#EFF6FF",
         "Shadow at low volume. A bridge between silent and full-voice. Tracks timing and rhythm without performance pressure.",
         "低声跟读。是从无声到全声的过渡桥梁。在没有演讲压力的情况下追踪时间和节奏。"),
        ("Full-voice shadowing", "全声跟读", "#0F6E56", "#E8F5F3",
         "Shadow at natural conversational volume, standing upright. This is the target mode — engage your full respiratory system and match the speaker's energy.",
         "以自然对话音量站立跟读。这是目标模式——调动完整的呼吸系统，配合说话者的语气和节奏。"),
    ]
    for i, (en, zh, color, bg, desc_en, desc_zh) in enumerate(voice_stages):
        arrow = " → " if i < len(voice_stages) - 1 else ""
        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-left:4px solid {color};'
            f'border-radius:10px;padding:14px 18px;background:{bg};margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
            f'<div style="background:{color};color:white;font-size:.72rem;font-weight:700;'
            f'border-radius:4px;padding:2px 7px;">Step {i+1}</div>'
            f'<div style="font-size:.9rem;font-weight:700;color:#1A3A5C;">{en}{c1}</div>'
            f'<div style="font-size:.8rem;color:#9CA3AF;">{zh}</div>'
            f'</div>'
            f'<div style="font-size:.84rem;color:#374151;line-height:1.65;margin-bottom:4px;">{desc_en}</div>'
            f'<div style="font-size:.8rem;color:#9CA3AF;line-height:1.55;">{desc_zh}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Stage 2: Text support
    st.markdown(
        '<div style="font-size:.85rem;font-weight:700;color:#1A3A5C;margin:20px 0 10px;">'
        '2 · Text support strategy / 文本辅助策略</div>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div style="border:1px solid #E5E7EB;border-left:4px solid #F59E0B;'
            'border-radius:10px;padding:14px 16px;background:#FFFBEB;">'
            '<div style="font-size:.88rem;font-weight:700;color:#92400E;margin-bottom:6px;">📄 With transcript</div>'
            '<div style="font-size:.78rem;color:#92400E;margin-bottom:8px;">有文本</div>'
            '<div style="font-size:.82rem;color:#374151;line-height:1.65;">'
            'Use for new or difficult material. Frees cognitive load from vocabulary decoding, '
            'letting you focus on pronunciation and prosody.</div>'
            '<div style="font-size:.78rem;color:#9CA3AF;margin-top:6px;line-height:1.55;">'
            '用于新材料或难度较高的内容。减少词汇解码的认知负担，让你专注于发音和韵律。</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div style="border:1px solid #E5E7EB;border-left:4px solid #2563EB;'
            'border-radius:10px;padding:14px 16px;background:#EFF6FF;">'
            '<div style="font-size:.88rem;font-weight:700;color:#1D4ED8;margin-bottom:6px;">🎧 Audio only</div>'
            '<div style="font-size:.78rem;color:#1D4ED8;margin-bottom:8px;">纯音频</div>'
            '<div style="font-size:.82rem;color:#374151;line-height:1.65;">'
            'The harder and more powerful mode. Forces genuine auditory processing — '
            'you must hear the rhythm before you can shadow it.</div>'
            '<div style="font-size:.78rem;color:#9CA3AF;margin-top:6px;line-height:1.55;">'
            '更难也更有效的模式。逼迫真正的听觉处理——你必须先听出节奏，才能跟读。</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div style="font-size:.8rem;color:#6B7280;margin-top:8px;line-height:1.6;">'
        '💡 Recommended path: start with transcript, remove it as confidence builds on that material.<br>'
        '<span style="color:#D1D5DB;">建议路径：从有文本开始，随着熟悉度提升逐步去掉文本。</span></div>',
        unsafe_allow_html=True,
    )

    # Stage 3: Session guidelines
    st.markdown(
        '<div style="font-size:.85rem;font-weight:700;color:#1A3A5C;margin:20px 0 10px;">'
        '3 · Session guidelines / 练习建议</div>',
        unsafe_allow_html=True,
    )
    guidelines = [
        ("⏱️", "Duration", "时长", "10–20 minutes per session", "每次10–20分钟"),
        ("📅", "Frequency", "频率", "Daily practice beats longer, infrequent sessions", "每日练习优于低频长时练习"),
        ("📈", "Horizon", "周期", "Expect noticeable gains after 4–6 weeks of consistent practice", "坚持4–6周可见明显进步"),
        ("🚶", "Posture", "姿态", "Stand or walk — full respiratory engagement produces better prosody", "站立或行走——充分调动呼吸产生更好的韵律效果"),
        ("🔁", "Repetition", "重复", "3 passes per sentence: listen → whisper → full voice", "每句三遍：先听 → 低声 → 全声"),
    ]
    for icon, en, zh, val_en, val_zh in guidelines:
        st.markdown(
            f'<div style="display:flex;align-items:flex-start;gap:12px;'
            f'border-bottom:1px solid #F3F4F6;padding:10px 4px;">'
            f'<div style="font-size:1.1rem;width:24px;flex-shrink:0;">{icon}</div>'
            f'<div style="flex:1;">'
            f'<span style="font-size:.85rem;font-weight:600;color:#1A3A5C;">{en}</span>'
            f'<span style="font-size:.78rem;color:#9CA3AF;margin-left:6px;">{zh}</span>'
            f'<div style="font-size:.82rem;color:#374151;margin-top:2px;">{val_en}</div>'
            f'<div style="font-size:.78rem;color:#9CA3AF;">{val_zh}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # Common mistakes
    st.markdown(
        '<div style="font-size:.85rem;font-weight:700;color:#1A3A5C;margin:20px 0 10px;">'
        '4 · Common mistakes to avoid / 常见错误</div>',
        unsafe_allow_html=True,
    )
    mistakes = [
        ("Muttering too quietly", "声音太小", "Sub-audible shadowing gets you no prosody training. At least one pass per session must be at full voice.", "太小声的跟读无法训练韵律。每次练习至少要有一遍全声跟读。"),
        ("Skipping the listen phase", "跳过听的阶段", "Jumping straight to shadowing before hearing the model properly means you're imitating your own guess, not the target.", "没有认真听原声就直接跟读，意味着你在模仿自己的猜测，而不是目标音。"),
        ("Using too-difficult material", "材料难度过高", "If you can't understand 70–80% of the content, cognitive load overwhelms the practice. Work at i+1, not i+5.", "如果你听不懂70–80%的内容，认知负荷会压垮练习效果。应在i+1难度练习，而非i+5。"),
        ("Practising without noticing", "练习时不注意", "Mindless shadowing builds bad habits. Pause, identify what you missed, then redo. Noticing is the mechanism — don't bypass it.", "无意识地跟读只会巩固坏习惯。暂停、找出哪里没做好、重新做。注意到差异才是机制所在，不要绕过它。"),
    ]
    for en, zh, desc_en, desc_zh in mistakes:
        st.markdown(
            f'<div style="border:1px solid #FEE2E2;border-left:4px solid #EF4444;'
            f'border-radius:8px;padding:12px 16px;background:#FFF8F8;margin-bottom:8px;">'
            f'<div style="font-size:.85rem;font-weight:700;color:#991B1B;margin-bottom:2px;">'
            f'✗ {en} · <span style="color:#DC2626;">{zh}</span></div>'
            f'<div style="font-size:.82rem;color:#374151;line-height:1.65;margin-bottom:3px;">{desc_en}</div>'
            f'<div style="font-size:.78rem;color:#9CA3AF;line-height:1.55;">{desc_zh}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _ref_block([
        {"n": 1, "text": "Hamada, Y. & Suzuki, A. (2024). Situating Shadowing in the Framework of Deliberate Practice. Language Teaching Research."},
    ])


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
        "✅ How to do it / 怎么做",
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
