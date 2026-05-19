import streamlit as st
st.set_page_config(
    page_title="ShadowingLab",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

from modules.state    import init_state
from modules.session  import session_page
from modules.phonology import phonology_page
from modules.noticelog import noticelog_page
from modules.progress  import progress_page
from modules.landing  import landing_page
from modules.styles   import inject_global_css
from modules.research import research_page
from modules.community import community_page
from modules.about import about_page
from modules.userdata  import init_user, trigger_save

inject_global_css()
init_state()

if "seen_onboarding" not in st.session_state:
    st.session_state.seen_onboarding = False
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Initialise user identity + load Firestore data (invisible, runs every render)
init_user()

# ── sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:14px 0 20px;">'
        '<div style="font-size:1.3rem;font-weight:700;color:var(--color-primary);">'
        '🎧 ShadowingLab</div>'
        '<div style="font-size:.75rem;color:var(--color-muted);margin-top:2px;">'
        'Structured shadowing for EFL learners</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Practice group ────────────────────────────────────────────
    for label, key in [
        ("🏠  Home",          "landing"),
        ("▶  Start Session",  "session"),
        ("📋  Notice Log",    "noticelog"),
        ("📈  Progress",      "progress"),
    ]:
        active = st.session_state.page == key
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            if key == "session":
                st.session_state.session_phase = "select"
            st.rerun()

    # ── Reference group ───────────────────────────────────────────
    st.markdown(
        '<div style="font-size:.68rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.07em;color:#9CA3AF;margin:14px 4px 6px;">Reference</div>',
        unsafe_allow_html=True
    )
    for label, key in [
        ("📖  Phonology Guide", "phonology"),
        ("💬  Community",       "community"),
    ]:
        active = st.session_state.page == key
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    # ── Save progress ─────────────────────────────────────────────
    st.markdown("---")
    last_saved = st.session_state.get("last_saved_at")
    uid        = st.session_state.get("user_uid")
    if uid:
        save_label = "💾 Save progress" + (f" · {last_saved}" if last_saved else "")
        if st.button(save_label, use_container_width=True, key="sidebar_save"):
            trigger_save()

    # ── Live session status ───────────────────────────────────────
    if st.session_state.get("active_material"):
        mat = st.session_state.active_material
        phase_labels = {
            "select":  "—",
            "prepare": "Phase 2  Prepare",
            "shadow":  "Phase 3  Shadow",
            "compare": "Phase 4  Compare",
            "capture": "Phase 5  Capture",
        }
        phase = st.session_state.get("session_phase", "select")
        notices_today = len([
            n for n in st.session_state.notice_log
            if n.get("session_id") == st.session_state.get("current_session_id")
        ])
        st.markdown(
            f'<div style="background:#F0F4FF;border:1px solid #BFDBFE;border-radius:8px;'
            f'padding:8px 12px;margin-top:8px;">'
            f'<div style="font-size:.68rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.06em;color:#3B82F6;margin-bottom:3px;">In session</div>'
            f'<div style="font-size:.82rem;font-weight:600;color:#1E3A5F;'
            f'margin-bottom:1px;">{mat["title"]}</div>'
            f'<div style="font-size:.74rem;color:#6B7280;">'
            f'{phase_labels.get(phase, "")}'
            + (f' · {notices_today} notice{"s" if notices_today!=1 else ""}' if notices_today else "")
            + f'</div></div>',
            unsafe_allow_html=True
        )

    # ── Footer: Feedback + About + Research (de-emphasised) ──────
    st.markdown(
        '<a href="https://docs.google.com/forms/d/e/1FAIpQLSc6Yl9b5NDR3Zvaaf_k3z1fiYWCgmfj9OspAhFu7tEOt8mo4g/viewform"'
        ' target="_blank"'
        ' style="display:block;text-align:center;font-size:.78rem;color:#6B7280;'
        'text-decoration:none;padding:6px 0;">💬 Share Feedback / 反馈</a>',
        unsafe_allow_html=True
    )
    page_cur = st.session_state.page
    fc1, fc2 = st.columns(2)
    with fc1:
        if st.button("📚 About", key="nav_about", use_container_width=True,
                     type="primary" if page_cur == "about" else "secondary"):
            st.session_state.page = "about"
            st.rerun()
    with fc2:
        if st.button("🔬 Research", key="nav_research", use_container_width=True,
                     type="primary" if page_cur == "research" else "secondary"):
            st.session_state.page = "research"
            st.rerun()

# ── route ─────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "landing":   landing_page()
elif page == "session":   session_page()
elif page == "phonology": phonology_page()
elif page == "noticelog": noticelog_page()
elif page == "progress":  progress_page()
elif page == "research":  research_page()
elif page == "community": community_page()
elif page == "about":     about_page()
