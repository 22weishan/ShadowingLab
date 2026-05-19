import os
import streamlit as st
import streamlit.components.v1 as components

_DOTS_COMPONENT_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "components", "onboarding_dots"
))
_dots_component = components.declare_component("onboarding_dots", path=_DOTS_COMPONENT_PATH)

def landing_page():
    if not st.session_state.get("seen_onboarding"):
        _onboarding()
    else:
        _landing()

def _onboarding():
    step = st.session_state.get("onboarding_step", 0)

    # Phase diagram HTML for card 4 — built as a plain string (no f-string needed)
    _phase_diagram = (
        '<div style="white-space:normal;text-align:center;">'
        '<div style="display:flex;justify-content:center;align-items:flex-start;'
        'gap:6px;margin-bottom:14px;flex-wrap:wrap;">'
        '<div style="text-align:center;min-width:54px;">'
        '<div style="font-size:1.5rem;">🎯</div>'
        '<div style="font-size:.72rem;font-weight:700;color:#2563EB;margin-top:4px;">Select</div>'
        '</div>'
        '<div style="color:#D1D5DB;font-size:1.1rem;padding-top:12px;">›</div>'
        '<div style="text-align:center;min-width:54px;">'
        '<div style="font-size:1.5rem;">📖</div>'
        '<div style="font-size:.72rem;font-weight:700;color:#2563EB;margin-top:4px;">Prepare</div>'
        '</div>'
        '<div style="color:#D1D5DB;font-size:1.1rem;padding-top:12px;">›</div>'
        '<div style="text-align:center;min-width:54px;">'
        '<div style="font-size:1.5rem;">🎙️</div>'
        '<div style="font-size:.72rem;font-weight:700;color:#2563EB;margin-top:4px;">Shadow</div>'
        '</div>'
        '<div style="color:#D1D5DB;font-size:1.1rem;padding-top:12px;">›</div>'
        '<div style="text-align:center;min-width:54px;">'
        '<div style="font-size:1.5rem;">🔍</div>'
        '<div style="font-size:.72rem;font-weight:700;color:#2563EB;margin-top:4px;">Compare</div>'
        '</div>'
        '<div style="color:#D1D5DB;font-size:1.1rem;padding-top:12px;">›</div>'
        '<div style="text-align:center;min-width:54px;">'
        '<div style="font-size:1.5rem;">📋</div>'
        '<div style="font-size:.72rem;font-weight:700;color:#2563EB;margin-top:4px;">Capture</div>'
        '</div>'
        '</div>'
        '<div style="font-size:.85rem;color:#374151;margin-top:6px;">Each session takes 20–30 minutes.</div>'
        '<div style="font-size:.8rem;color:#9CA3AF;margin-top:3px;">建议每次20–30分钟。</div>'
        '</div>'
    )

    cards = [
        {"icon": "🎧", "en": "ShadowingLab", "zh": "",
         "detail_en": "More than a practice tool — every design decision is grounded in teaching experience, empirical research, and learning science.",
         "detail_zh": "不只是练习工具——每一个设计决策背后，都有教学经验、实证研究和学习科学的支撑。",
         "btn": "Tell me more / 继续"},
        {"icon": "🗣️", "en": "The real problem", "zh": "",
         "detail_en": "You can catch the words, but not the speed.\nYou want to speak, but think in Chinese first.\nThis isn't about effort — it's about how you've been trained.\n\nYears of multiple-choice listening have never taught you how to actually listen.",
         "detail_zh": "听得懂单词，却跟不上语速。\n开口想说，脑子里还是中文在转。\n这不是努力不够——是训练方式出了问题。\n\n多年的选择题听力练习，从来没有教会你怎么听。",
         "btn": "Tell me more / 继续"},
        {"icon": "🔁", "en": "Shadowing is the fix", "zh": "",
         "detail_en": "Shadowing means repeating what you hear in real time. It trains your brain to decode fast native speech.",
         "detail_zh": "跟读就是实时重复你听到的内容。它训练大脑解码快速的母语语音。",
         "btn": "How does it work? / 怎么用？"},
        {"icon": "🧰", "en": "What's inside", "zh": "工具里有什么",
         "detail_en": (
             '<div style="display:flex;flex-direction:column;gap:12px;">'

             '<div style="display:flex;gap:12px;align-items:flex-start;">'
             '<span style="font-size:1.3rem;flex-shrink:0;">📚</span>'
             '<div><div style="font-weight:700;color:#1A3A5C;font-size:.9rem;">'
             'Authentic materials / 真实练习材料</div>'
             '<div style="color:#6B7280;font-size:.82rem;">'
             'TOEFL conversations at beginner to advanced level, with full phonological annotation.<br>'
             '<span style="color:#9CA3AF;">涵盖初级到进阶的托福对话音频，附带完整语音标注。</span>'
             '</div></div></div>'

             '<div style="display:flex;gap:12px;align-items:flex-start;">'
             '<span style="font-size:1.3rem;flex-shrink:0;">📖</span>'
             '<div><div style="font-weight:700;color:#1A3A5C;font-size:.9rem;">'
             'Phonology Guide / 语音知识库</div>'
             '<div style="color:#6B7280;font-size:.82rem;">'
             'Understand why fast native speech sounds the way it does — and stop mishearing the same patterns.<br>'
             '<span style="color:#9CA3AF;">彻底搞懂母语者快速语音背后的规律，不再反复听漏同一个地方。</span>'
             '</div></div></div>'

             '<div style="display:flex;gap:12px;align-items:flex-start;">'
             '<span style="font-size:1.3rem;flex-shrink:0;">📋</span>'
             '<div><div style="font-weight:700;color:#1A3A5C;font-size:.9rem;">'
             'Notice Log / 发现记录</div>'
             '<div style="color:#6B7280;font-size:.82rem;">'
             'Capture what you observe after each session. Over time, patterns in your log reveal exactly what to work on.<br>'
             '<span style="color:#9CA3AF;">每次练习后记录你注意到的差距，积累越多，越能看清自己真正需要突破的点。</span>'
             '</div></div></div>'

             '<div style="display:flex;gap:12px;align-items:flex-start;">'
             '<span style="font-size:1.3rem;flex-shrink:0;">📈</span>'
             '<div><div style="font-weight:700;color:#1A3A5C;font-size:.9rem;">'
             'Progress / 学习进度</div>'
             '<div style="color:#6B7280;font-size:.82rem;">'
             'Track your sessions and see which phonological phenomena you notice most across your practice.<br>'
             '<span style="color:#9CA3AF;">记录每次练习，看清哪类语音现象在你的记录中出现最频繁。</span>'
             '</div></div></div>'

             '<div style="display:flex;gap:12px;align-items:flex-start;">'
             '<span style="font-size:1.3rem;flex-shrink:0;">💬</span>'
             '<div><div style="font-weight:700;color:#1A3A5C;font-size:.9rem;">'
             'Community / 社区</div>'
             '<div style="color:#6B7280;font-size:.82rem;">'
             'Share your notices with other learners and see what others are discovering in their practice.<br>'
             '<span style="color:#9CA3AF;">把你的发现分享给其他学习者，也看看别人在练习中注意到了什么。</span>'
             '</div></div></div>'

             '</div>'
         ),
         "detail_zh": "",
         "btn": "Let's start / 开始练习"},
    ]
    card = cards[step]

    st.markdown(f"""
    <div style="max-width:560px;margin:80px auto 0;padding:0 16px;text-align:center;">
        <div style="font-size:3rem;margin-bottom:16px;">{card['icon']}</div>
        <div style="font-size:1.35rem;font-weight:700;color:#1A3A5C;line-height:1.4;margin-bottom:10px;">{card['en']}</div>
        <div style="font-size:1rem;color:#6B7280;margin-bottom:20px;">{card['zh']}</div>
        <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:12px;padding:20px 24px;margin-bottom:16px;text-align:left;{'white-space:pre-line;' if step < 3 else ''}">
            <div style="font-size:.9rem;color:#374151;line-height:1.7;">{card['detail_en']}</div>
            <div style="font-size:.84rem;color:#9CA3AF;margin-top:8px;line-height:1.65;">{card['detail_zh']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clickable dots via declare_component — stable key means value persists across reruns
    dot_result = _dots_component(current_step=step, total=len(cards), key="ob_dots")
    if isinstance(dot_result, dict) and "step" in dot_result:
        new_step = int(dot_result["step"])
        if new_step != step:
            st.session_state.onboarding_step = new_step
            st.rerun()

    col_skip, col_next = st.columns([1, 1])
    with col_skip:
        if st.button("Skip intro / 跳过介绍", use_container_width=True, key="ob_skip"):
            st.session_state.seen_onboarding = True
            st.session_state.page = "session"
            st.rerun()
    with col_next:
        if st.button(card["btn"], use_container_width=True, type="primary", key=f"ob_next_{step}"):
            if step < len(cards) - 1:
                st.session_state.onboarding_step = step + 1
                st.rerun()
            else:
                st.session_state.seen_onboarding = True
                st.session_state.page = "session"
                st.rerun()

def _landing():
    history = st.session_state.get("session_history", [])
    st.markdown("""
    <div style="max-width:680px;margin:48px auto 40px;text-align:center;padding:0 16px;">
        <div style="font-size:2.4rem;font-weight:800;color:#1A3A5C;line-height:1.2;margin-bottom:12px;">🎧 ShadowingLab</div>
        <div style="font-size:1.1rem;color:#374151;line-height:1.6;margin-bottom:6px;">Train your ear, not just your test score.</div>
        <div style="font-size:.95rem;color:#9CA3AF;line-height:1.6;">用跟读法训练你的耳朵，而不只是应付考试。</div>
    </div>
    """, unsafe_allow_html=True)
    if history:
        last = history[-1]
        total_notices = sum(h.get("notices",0) for h in history)
        st.markdown(f"""
        <div style="max-width:560px;margin:0 auto 32px;background:#F0FDF4;border:1px solid #6EE7B7;border-radius:14px;padding:18px 24px;">
            <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#065F46;margin-bottom:10px;">Welcome back / 欢迎回来</div>
            <div style="display:flex;gap:24px;flex-wrap:wrap;">
                <div><div style="font-size:1.5rem;font-weight:700;color:#065F46;">{len(history)}</div><div style="font-size:.78rem;color:#059669;">sessions</div></div>
                <div><div style="font-size:1.5rem;font-weight:700;color:#065F46;">{total_notices}</div><div style="font-size:.78rem;color:#059669;">notices logged / 发现记录</div></div>
                <div><div style="font-size:.9rem;font-weight:600;color:#065F46;margin-top:4px;">Last: {last['material_title']}</div><div style="font-size:.78rem;color:#059669;">{last['date']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    col_l, col_btn, col_r = st.columns([1,1.2,1])
    with col_btn:
        label = "Continue practising / 继续练习 →" if history else "Start your first session / 开始第一次练习 →"
        if st.button(label, type="primary", use_container_width=True, key="landing_start"):
            st.session_state.page = "session"
            st.session_state.session_phase = "select"
            st.rerun()
    st.markdown("<div style='margin-bottom:40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style="text-align:center;margin:32px 0 20px;"><div style="font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#9CA3AF;">How it works / 怎么运作</div></div>""", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    features = [
        ("🪜","Structured shadowing","结构化跟读","A research-backed 5-phase process guides you from first listen to recorded shadowing.","基于研究的五阶段流程，从初次聆听到录音跟读，全程有引导。"),
        ("📋","Notice Log","发现记录","Record what you notice — gaps between your voice and the original. Not errors, discoveries.","记录你注意到的差距——不是错误，是发现。"),
        ("📖","Phonology Guide","语音知识库","Seven concept cards explain stress, linking, weak forms — for Mandarin speakers specifically.","七张概念卡片解释重音、连读、弱读——专门针对普通话母语者的难点。"),
    ]
    for col,(icon,ten,tzh,den,dzh) in zip([c1,c2,c3],features):
        with col:
            st.markdown(f"""<div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:12px;padding:20px 18px;">
                <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
                <div style="font-size:.95rem;font-weight:700;color:#1A3A5C;margin-bottom:2px;">{ten}</div>
                <div style="font-size:.82rem;color:#9CA3AF;margin-bottom:10px;">{tzh}</div>
                <div style="font-size:.84rem;color:#374151;line-height:1.6;margin-bottom:6px;">{den}</div>
                <div style="font-size:.8rem;color:#9CA3AF;line-height:1.55;">{dzh}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style="max-width:600px;margin:24px auto;text-align:center;"><div style="font-size:.8rem;color:#9CA3AF;line-height:1.7;">Grounded in Schmidt's Noticing Hypothesis (1990), Cognitive Load Theory (Sweller, 2011), and shadowing research (Hamada, 2016).<br><span style="color:#D1D5DB;">基于Schmidt注意假说、认知负荷理论和跟读法研究。</span></div></div>""", unsafe_allow_html=True)
