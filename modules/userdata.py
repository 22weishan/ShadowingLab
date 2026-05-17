"""
userdata.py  —  Persistent user data via browser localStorage UUID + Firestore

Flow:
  1. uid_component() renders a 0-height JS iframe that reads/creates a UUID
     in the browser's localStorage and sends it back via setComponentValue.
  2. On the first rerun where a UID arrives, load_user_data() pulls the user's
     notice_log, session_history, vocabulary and nickname from Firestore into
     session_state.
  3. save_user_data() writes the current session_state back to Firestore.
     Called automatically on session finish and via the sidebar Save button.
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime


# ── localStorage UUID component ──────────────────────────────────────

_UID_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<script>(function(){
  function post(type,extra){
    window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},extra),"*");
  }
  post("streamlit:componentReady",{apiVersion:1});
  var uid = localStorage.getItem('shadowinglab_uid');
  if (!uid) {
    uid = 'sl_' + Math.random().toString(36).substr(2,9)
               + Date.now().toString(36);
    localStorage.setItem('shadowinglab_uid', uid);
  }
  post("streamlit:setComponentValue",{value:{uid:uid},dataType:"json"});
  post("streamlit:setFrameHeight",{height:0});
})();</script>
</body></html>"""


def uid_component() -> str | None:
    """
    Render an invisible JS component that reads (or creates) a UUID from
    localStorage. Returns the UID string on the rerun after it fires,
    None on the very first render.
    """
    result = components.html(_UID_HTML, height=0, scrolling=False)
    if isinstance(result, dict) and "uid" in result:
        return result["uid"]
    return None


# ── Firestore helpers ────────────────────────────────────────────────

def _get_db():
    from modules.community import _get_db as _community_db
    return _community_db()


def _firebase_ok() -> bool:
    return _get_db() is not None


# ── Load ─────────────────────────────────────────────────────────────

def load_user_data(uid: str) -> bool:
    """
    Pull user data from Firestore into session_state.
    Safe to call when the document doesn't exist yet (first-time user).
    Returns True on success (including "no doc yet"), False on error.
    """
    db = _get_db()
    if not db:
        return False
    try:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            data = doc.to_dict()
            # Only restore if the Firestore list is non-empty, so a fresh
            # session on a new device doesn't wipe an existing session_state.
            if data.get("notice_log"):
                st.session_state.notice_log = data["notice_log"]
            if data.get("session_history"):
                st.session_state.session_history = data["session_history"]
            if data.get("vocabulary"):
                st.session_state.vocabulary = data["vocabulary"]
            if data.get("nickname"):
                st.session_state.community_nickname = data["nickname"]
        return True
    except Exception as e:
        st.warning(f"Could not load saved data: {e}")
        return False


# ── Save ─────────────────────────────────────────────────────────────

def save_user_data(uid: str) -> bool:
    """
    Write notice_log, session_history, vocabulary and nickname to Firestore.
    Uses set(merge=True) so other fields (e.g. created_at) are preserved.
    Returns True on success.
    """
    db = _get_db()
    if not db:
        return False
    try:
        from google.cloud.firestore_v1 import SERVER_TIMESTAMP
        data = {
            "notice_log":      st.session_state.get("notice_log", []),
            "session_history": st.session_state.get("session_history", []),
            "vocabulary":      st.session_state.get("vocabulary", []),
            "nickname":        st.session_state.get("community_nickname", ""),
            "last_active":     SERVER_TIMESTAMP,
        }
        ref = db.collection("users").document(uid)
        # Set created_at only on first write
        snap = ref.get()
        if not snap.exists:
            data["created_at"] = SERVER_TIMESTAMP
        ref.set(data, merge=True)
        st.session_state["last_saved_at"] = datetime.now().strftime("%H:%M")
        return True
    except Exception as e:
        st.warning(f"Could not save data: {e}")
        return False


# ── Convenience: try to save, show status ────────────────────────────

def trigger_save():
    """Save if Firebase is available and we have a UID. Used by sidebar button."""
    uid = st.session_state.get("user_uid")
    if not uid:
        st.warning("Device ID not yet available — try again in a moment.")
        return
    if not _firebase_ok():
        st.warning("Firebase not configured — data is not being saved.")
        return
    if save_user_data(uid):
        st.success("Saved! / 已保存")
    # failure message is shown inside save_user_data


# ── Initialise user on every app boot ────────────────────────────────

def init_user():
    """
    Call once per page render (in app.py, before sidebar and routing).

    1. Renders the invisible localStorage component.
    2. On the rerun when a UID arrives, stores it and loads Firestore data.
    3. Subsequent reruns skip the load (data_loaded flag).
    """
    uid = uid_component()

    if uid and not st.session_state.get("user_uid"):
        # First time we received a UID this session
        st.session_state["user_uid"] = uid
        if _firebase_ok() and not st.session_state.get("data_loaded"):
            load_user_data(uid)
            st.session_state["data_loaded"] = True
            st.rerun()

    elif uid and not st.session_state.get("data_loaded"):
        # UID was set but load hasn't happened yet (e.g. Firebase just configured)
        if _firebase_ok():
            load_user_data(uid)
            st.session_state["data_loaded"] = True
