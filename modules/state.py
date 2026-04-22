import streamlit as st
import uuid

def init_state():
    defaults = {
        # navigation
        "page":                 "session",
        "session_phase":        "select",   # select | prepare | shadow | compare | capture

        # active session
        "active_material":      None,       # dict from MATERIALS
        "current_session_id":   None,       # uuid str, set at session start
        "current_segment":      0,
        "shadow_mode":          "sentence", # sentence | passage
        "visited_segments":     set(),
        "recordings_by_segment": {},        # {seg_idx: base64_str}
        "full_recording":       None,       # base64_str
        "compare_recording":    None,       # the recording chosen for Phase 4

        # notice log (persists across sessions)
        "notice_log":           [],         # list[dict]

        # vocabulary bank
        "vocabulary":           [],         # list[str]

        # session history (for Progress page)
        "session_history":      [],         # list[dict]

        # phonology guide state
        "phon_open_card":       None,       # tag key of open card, or None
        "phon_inline_card":     None,       # tag key of inline popup in shadow phase
        "saved_sentences":      set(),      # bookmarked difficult sentences
        "shadow_playback_mode": "shadow",   # shadow | flow
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def start_new_session(material: dict):
    """Call when a student picks a material and begins Phase 2."""
    st.session_state.active_material       = material
    st.session_state.current_session_id    = str(uuid.uuid4())[:8]
    st.session_state.session_phase         = "prepare"
    st.session_state.current_segment       = 0
    st.session_state.shadow_mode           = "sentence"
    st.session_state.visited_segments      = set()
    st.session_state.recordings_by_segment = {}
    st.session_state.full_recording        = None
    st.session_state.compare_recording     = None
    st.session_state.phon_inline_card      = None
    st.session_state.saved_sentences       = set()
    st.session_state.shadow_playback_mode  = "shadow"


def advance_phase(to: str):
    st.session_state.session_phase = to


def go_page(page: str):
    st.session_state.page = page
