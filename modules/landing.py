import streamlit as st

def landing_page():
    if not st.session_state.get("seen_onboarding"):
        _onboarding()
    else:
        _landing()

def _onboarding():
    step = st.session_state.get("onboarding_step", 0)
    cards = [
        {"icon":"🎧","en":"Most Chinese students can pass listening tests — but still cannot understand real spoken English.","zh":"很多中国学生能通过听力考试，却还是听不懂真实的英语。","detail_en":"Tests train you to answer questions, not to actually hear English. The gap is in your ears, not your knowledge.","detail_zh":"考试训练你回答问题，而不是真正听懂英语。问题出在你的耳朵上，不是你的知识。","btn":"Tell me more / 继续"},
        {"icon":"🔁","en":"Shadowing is the fix — and ShadowingLab makes it structured.","zh":"跟读法是解决方案——ShadowingLab 让它变得有结构。","detail_en":"Shadowing means repeating what you hear in real time. It trains your brain to decode fast native speech.","detail_zh":"跟读就是实时重复你听到的内容。它训练大脑解码快速的母语语音。","btn":"How does it work? / 怎么用？"},
        {"icon":"🗺️","en":"Each session takes 20–30 minutes and follows five steps.","zh":"每次练习20–30分钟，分五个步骤。","detail_en":"① Prepare  →  ② Shadow  →  ③ Record  →  ④ Compare  →  ⑤ Capture\n\nYou will hear what you sound like next to a native speaker.","detail_zh":"① 准备  →  ② 跟读  →  ③ 录音  →  ④ 对比  →  ⑤ 记录\n\n你会听到自己和母语者的差距。","btn":"Let us start / 开始练习"},
    ]
    card = cards[step]
    dots_html = "".join(f'<span style="width:8px;height:8px;border-radius:50%;display:inline-block;margin:0 4px;background:{"#2563EB" if i==step else "#D1D5DB"};"></span>' for i in range(len(cards)))
    st.markdown(f"""
    <div style="max-width:560px;margin:80px auto 0;padding:0 16px;text-align:center;">
        <div style="font-size:3rem;margin-bottom:16px;">{card['icon']}</div>
        <div style="font-size:1.35rem;font-weight:700;color:#1A3A5C;line-height:1.4;margin-bottom:10px;">{card['en']}</div>
        <div style="font-size:1rem;color:#6B7280;margin-bottom:20px;">{card['zh']}</div>
        <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:12px;padding:20px 24px;margin-bottom:28px;text-align:left;white-space:pre-line;">
            <div style="font-size:.9rem;color:#374151;line-height:1.7;">{card['detail_en']}</div>
            <div style="font-size:.84rem;color:#9CA3AF;margin-top:8px;line-height:1.65;">{card['detail_zh']}</div>
        </div>
        <div style="margin-bottom:20px;">{dots_html}</div>
    </div>
    """, unsafe_allow_html=True)
    col_skip, col_next = st.columns([1,1])
    with col_skip:
        if st.button("Skip intro / 跳过介绍", use_container_width=True, key="ob_skip"):
            st.session_state.seen_onboarding = True
            st.session_state.page = "session"
            st.rerun()
    with col_next:
        if st.button(card["btn"], use_container_width=True, type="primary", key=f"ob_next_{step}"):
            if step < len(cards)-1:
                st.session_state.onboarding_step = step+1
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
