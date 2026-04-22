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

inject_global_css()
init_state()

if "seen_onboarding" not in st.session_state:
    st.session_state.seen_onboarding = False
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ── sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 24px;">
        <div style="font-size:1.4rem;font-weight:700;color:var(--color-primary);">
            🎧 ShadowingLab
        </div>
        <div style="font-size:.78rem;color:var(--color-muted);margin-top:2px;">
            Structured shadowing for EFL learners
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home":             "landing",
        "▶  Start Session":    "session",
        "📖  Phonology Guide":  "phonology",
        "📋  Notice Log":       "noticelog",
        "📈  Progress":         "progress",
    }

    for label, key in pages.items():
        active = st.session_state.page == key
        if st.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.page = key
            if key == "session":
                st.session_state.session_phase = "select"
            st.rerun()

    # Research Mode separator + button
    st.markdown("---")
    active_research = st.session_state.page == "research"
    if st.button(
        "🔬  Research Mode",
        key="nav_research",
        use_container_width=True,
        type="primary" if active_research else "secondary",
    ):
        st.session_state.page = "research"
        st.rerun()

    st.markdown("---")

    # live session status
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
        st.markdown(f"""
        <div style="font-size:.75rem;color:var(--color-muted);margin-bottom:4px;">
            Current session
        </div>
        <div style="font-size:.85rem;font-weight:600;color:var(--color-text);margin-bottom:2px;">
            {mat['title']}
        </div>
        <div style="font-size:.75rem;color:var(--color-accent);">
            {phase_labels.get(phase, '')}
        </div>
        """, unsafe_allow_html=True)

        notices_today = len([
            n for n in st.session_state.notice_log
            if n.get("session_id") == st.session_state.get("current_session_id")
        ])
        if notices_today:
            st.markdown(
                f'<div style="font-size:.75rem;color:var(--color-muted);margin-top:4px;">'
                f'{notices_today} notice{"s" if notices_today != 1 else ""} this session</div>',
                unsafe_allow_html=True,
            )

# ── route ─────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "landing":   landing_page()
elif page == "session":   session_page()
elif page == "phonology": phonology_page()
elif page == "noticelog": noticelog_page()
elif page == "progress":  progress_page()
elif page == "research":  research_page()
