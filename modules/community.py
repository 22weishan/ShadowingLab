"""
community.py  —  Community Forum page
Firebase Firestore-backed discussion board focused on phonological noticing.
"""

import streamlit as st
from datetime import datetime

# ── Firebase init (singleton) ────────────────────────────────────────

def _get_db():
    """Return Firestore client, or None if Firebase not configured."""
    if "firebase_db" in st.session_state:
        return st.session_state.firebase_db

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            fb = st.secrets.get("firebase", {})
            if not fb:
                st.session_state.firebase_db = None
                return None
            cred = credentials.Certificate(dict(fb))
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        st.session_state.firebase_db = db
        return db
    except Exception as e:
        st.session_state.firebase_db = None
        return None


def _is_firebase_available() -> bool:
    return _get_db() is not None


# ── Nickname system ──────────────────────────────────────────────────

CATEGORIES = ["Stress", "Linking", "Intonation", "Weak Forms", "Other"]
CATEGORY_COLORS = {
    "Stress":     ("#0C447C", "#DBEAFE"),
    "Linking":    ("#065F46", "#D1FAE5"),
    "Intonation": ("#7C2D12", "#FEF3C7"),
    "Weak Forms": ("#4C1D95", "#EDE9FE"),
    "Other":      ("#374151", "#F3F4F6"),
}


def _nickname_setup():
    """Render nickname prompt if user has no nickname yet. Returns True if ready."""
    if st.session_state.get("community_nickname"):
        return True

    st.markdown("""
    <div style="max-width:480px;margin:40px auto;padding:0 16px;">
        <div style="font-size:1.2rem;font-weight:700;color:#1A3A5C;margin-bottom:6px;">
            Choose a nickname to join the community
        </div>
        <div style="font-size:.88rem;color:#6B7280;margin-bottom:20px;line-height:1.6;">
            Your nickname appears with your posts. No account needed.
            Feel free to write in English or Chinese — both are welcome.<br>
            <span style="color:#9CA3AF;">昵称显示在你的帖子旁边，无需注册。</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        nick = st.text_input(
            "Your nickname / 你的昵称",
            placeholder="e.g. 音韵探索者 / phonics_fan",
            max_chars=30,
            key="nick_input",
        )
        if st.button("Join Community / 加入社区", type="primary",
                     use_container_width=True, key="nick_join"):
            if nick.strip():
                st.session_state.community_nickname = nick.strip()
                st.rerun()
            else:
                st.error("Please enter a nickname. / 请输入昵称。")
    return False


# ── Firebase helpers ─────────────────────────────────────────────────

def _post_to_community(category: str, material: str, content: str,
                       open_question: str = "") -> bool:
    db = _get_db()
    if not db:
        return False
    try:
        from google.cloud.firestore import SERVER_TIMESTAMP
        db.collection("posts").add({
            "category":      category,
            "material":      material,
            "content":       content,
            "open_question": open_question,
            "username":      st.session_state.get("community_nickname", "Anonymous"),
            "timestamp":     SERVER_TIMESTAMP,
            "reply_count":   0,
        })
        return True
    except Exception as e:
        st.error(f"Failed to post: {e}")
        return False


def _add_reply(post_id: str, content: str) -> bool:
    db = _get_db()
    if not db:
        return False
    try:
        from google.cloud.firestore import SERVER_TIMESTAMP
        post_ref = db.collection("posts").document(post_id)
        post_ref.collection("replies").add({
            "content":   content,
            "username":  st.session_state.get("community_nickname", "Anonymous"),
            "timestamp": SERVER_TIMESTAMP,
        })
        post_ref.update({"reply_count": _firestore_increment(1)})
        return True
    except Exception as e:
        st.error(f"Failed to add reply: {e}")
        return False


def _firestore_increment(n):
    from google.cloud.firestore_v1.transforms import Increment
    return Increment(n)


def _get_posts(category_filter: str = "All") -> list:
    db = _get_db()
    if not db:
        return []
    try:
        ref = db.collection("posts").order_by(
            "timestamp", direction="DESCENDING"
        ).limit(50)
        docs = ref.stream()
        posts = []
        for d in docs:
            data = d.to_dict()
            data["id"] = d.id
            if category_filter == "All" or data.get("category") == category_filter:
                posts.append(data)
        return posts
    except Exception as e:
        return []


def _get_replies(post_id: str) -> list:
    db = _get_db()
    if not db:
        return []
    try:
        docs = (
            db.collection("posts").document(post_id)
            .collection("replies")
            .order_by("timestamp")
            .stream()
        )
        return [d.to_dict() for d in docs]
    except Exception:
        return []


def _fmt_ts(ts) -> str:
    if ts is None:
        return ""
    try:
        dt = ts.astimezone() if hasattr(ts, "astimezone") else ts
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ts)[:16]


# ── Share draft (called from noticelog) ─────────────────────────────

def open_share_draft(notice: dict):
    """Set session state to open a share draft for a given notice."""
    from modules.materials import TAGS
    tag_key = notice.get("tag", "")
    cat_map = {
        "stress":     "Stress",
        "link":       "Linking",
        "intonation": "Intonation",
        "weak":       "Weak Forms",
        "rhythm":     "Stress",
        "omission":   "Other",
        "insertion":  "Other",
    }
    st.session_state["share_draft"] = {
        "category":  cat_map.get(tag_key, "Other"),
        "material":  notice.get("material_title", ""),
        "content":   notice.get("text", ""),
    }
    st.session_state.page = "community"
    st.rerun()


# ── Community page ───────────────────────────────────────────────────

def community_page():
    st.title("💬 Community / 社区")
    st.markdown(
        '<p class="muted" style="margin-top:-8px;margin-bottom:16px;">'
        "A space for phonological noticing — share what you heard, read what others noticed. "
        "Feel free to write in English or Chinese — both are welcome.<br>"
        '<span style="font-size:.82rem;">分享你的发现，阅读他人的观察。'
        "中英文都欢迎。</span></p>",
        unsafe_allow_html=True,
    )

    if not _is_firebase_available():
        st.warning(
            "Community requires Firebase to be configured. "
            "Add your Firebase credentials to Streamlit Secrets under `[firebase]`."
        )
        return

    if not _nickname_setup():
        return

    # Show pending share draft if redirected from Notice Log
    draft = st.session_state.pop("share_draft", None)
    if draft:
        _render_share_form(draft)
        st.markdown("---")

    tab_browse, tab_post = st.tabs(["📜 Browse posts / 浏览帖子", "✏️ New post / 发帖"])

    with tab_browse:
        _render_browse()

    with tab_post:
        _render_new_post()


def _category_chip(category: str, small: bool = False) -> str:
    color, bg = CATEGORY_COLORS.get(category, ("#374151", "#F3F4F6"))
    fs = ".72rem" if small else ".78rem"
    return (
        f'<span style="background:{bg};color:{color};border-radius:99px;'
        f'padding:2px 10px;font-size:{fs};font-weight:700;">{category}</span>'
    )


def _render_share_form(draft: dict):
    """Render the pre-filled share form when redirected from Notice Log."""
    st.markdown(
        '<div style="background:#F0FDF4;border:1.5px solid #6EE7B7;border-radius:12px;'
        'padding:16px 18px;margin-bottom:8px;">'
        '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.05em;color:#065F46;margin-bottom:10px;">✨ Share to Community</div>',
        unsafe_allow_html=True,
    )

    category = st.selectbox(
        "Category / 类别",
        CATEGORIES,
        index=CATEGORIES.index(draft["category"]) if draft["category"] in CATEGORIES else 0,
        key="share_draft_cat",
    )
    material = st.text_input(
        "From material / 来自哪个素材",
        value=draft["material"],
        key="share_draft_mat",
    )
    content = st.text_area(
        "Your observation / 你的观察",
        value=draft["content"],
        height=100,
        key="share_draft_content",
    )
    open_q = st.text_input(
        "Open question (optional) / 想问社区的问题（可选）",
        placeholder="e.g. Do you notice this too? How do you practise it?",
        key="share_draft_q",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_post, col_cancel = st.columns(2)
    with col_post:
        if st.button("Post / 发帖", type="primary", use_container_width=True,
                     key="share_draft_submit"):
            if content.strip():
                if _post_to_community(category, material, content.strip(), open_q.strip()):
                    st.success("Posted! / 发帖成功！")
                    st.rerun()
            else:
                st.error("Observation text is required.")
    with col_cancel:
        if st.button("Cancel / 取消", use_container_width=True, key="share_draft_cancel"):
            st.rerun()


def _render_browse():
    cat_options = ["All"] + CATEGORIES
    cat_filter = st.radio(
        "Filter by category / 按类别筛选",
        cat_options,
        horizontal=True,
        key="community_filter",
        label_visibility="collapsed",
    )

    posts = _get_posts(cat_filter)

    if not posts:
        st.markdown(
            '<div style="text-align:center;padding:40px 24px;color:#9CA3AF;">'
            '<div style="font-size:1.5rem;margin-bottom:8px;">💬</div>'
            '<div style="font-size:.9rem;">No posts yet. Be the first to share a noticing!</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        return

    for post in posts:
        _render_post_card(post)


def _render_post_card(post: dict):
    pid       = post["id"]
    category  = post.get("category", "Other")
    material  = post.get("material", "")
    content   = post.get("content", "")
    username  = post.get("username", "Anonymous")
    ts        = _fmt_ts(post.get("timestamp"))
    reply_cnt = post.get("reply_count", 0)
    open_q    = post.get("open_question", "")

    chip = _category_chip(category, small=True)

    st.markdown(
        f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;'
        f'padding:14px 16px;margin-bottom:8px;">'
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;">'
        f'{chip}'
        f'<span style="font-size:.74rem;color:#9CA3AF;">{material}</span>'
        f'<span style="margin-left:auto;font-size:.74rem;color:#9CA3AF;">'
        f'{username} · {ts}</span>'
        f'</div>'
        f'<div style="font-size:.88rem;color:#1F2937;margin-bottom:6px;line-height:1.55;">'
        f'{content}</div>',
        unsafe_allow_html=True,
    )

    if open_q:
        st.markdown(
            f'<div style="background:#FFFBEB;border-left:3px solid #F59E0B;border-radius:4px;'
            f'padding:6px 10px;font-size:.8rem;color:#92400E;margin-bottom:8px;">'
            f'❓ {open_q}</div>',
            unsafe_allow_html=True,
        )

    reply_label = f"💬 {reply_cnt} repl{'ies' if reply_cnt != 1 else 'y'}"
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander(reply_label, expanded=False):
        replies = _get_replies(pid)
        if replies:
            for r in replies:
                st.markdown(
                    f'<div style="background:#F9FAFB;border-radius:8px;padding:8px 12px;'
                    f'margin-bottom:6px;font-size:.83rem;">'
                    f'<span style="font-weight:600;color:#374151;">'
                    f'{r.get("username","Anonymous")}</span>'
                    f'<span style="color:#9CA3AF;font-size:.74rem;margin-left:8px;">'
                    f'{_fmt_ts(r.get("timestamp"))}</span>'
                    f'<div style="color:#4B5563;margin-top:4px;">{r.get("content","")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="color:#9CA3AF;font-size:.82rem;">No replies yet.</div>',
                unsafe_allow_html=True,
            )

        reply_text = st.text_area(
            "Reply / 回复",
            placeholder="Share your thoughts… / 分享你的想法…",
            height=70,
            key=f"reply_{pid}",
            label_visibility="collapsed",
        )
        if st.button("Post reply / 发送回复", key=f"reply_btn_{pid}"):
            if reply_text.strip():
                if _add_reply(pid, reply_text.strip()):
                    st.success("Reply posted! / 回复成功！")
                    st.rerun()
            else:
                st.error("Reply cannot be empty.")


def _render_new_post():
    st.markdown(
        '<div style="font-size:.82rem;color:#6B7280;margin-bottom:16px;line-height:1.6;">'
        "Share a phonological feature you noticed — any language is welcome. "
        "The more specific, the more useful for others.<br>"
        '<span style="color:#9CA3AF;">分享你注意到的语音现象——越具体越好。</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    category = st.selectbox("Category / 类别", CATEGORIES, key="new_post_cat")
    material = st.text_input(
        "From which material? / 来自哪个素材？",
        placeholder="e.g. At the Language Lab",
        key="new_post_mat",
    )
    content = st.text_area(
        "Your observation / 你的观察",
        placeholder=(
            'e.g. "In \'took up\', the /k/ completely disappears — '
            'it sounds like \'too-kup\'. I didn\'t expect the boundary to vanish like that."'
        ),
        height=120,
        key="new_post_content",
    )
    open_q = st.text_input(
        "Open question for the community (optional) / 想问社区的问题（可选）",
        placeholder="e.g. Do you use a different technique to notice weak forms?",
        key="new_post_q",
    )

    st.markdown(
        '<div style="font-size:.78rem;color:#9CA3AF;margin:4px 0 12px;">Feel free to write in English or Chinese — both are welcome. / 中英文都欢迎。</div>',
        unsafe_allow_html=True,
    )

    if st.button("Post / 发帖", type="primary", key="new_post_submit"):
        if not content.strip():
            st.error("Please write your observation before posting.")
        elif not material.strip():
            st.error("Please indicate which material this is from.")
        else:
            if _post_to_community(category, material.strip(), content.strip(), open_q.strip()):
                st.success("Posted successfully! / 发帖成功！Switch to Browse to see it.")
                st.session_state["new_post_content"] = ""
                st.session_state["new_post_mat"] = ""
                st.session_state["new_post_q"] = ""
                st.rerun()
