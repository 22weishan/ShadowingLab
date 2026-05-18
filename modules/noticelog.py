"""
noticelog.py  —  Notice Log page
All captured notices across sessions, filterable and searchable.
Includes AI-style pattern summary when ≥10 notices exist.
"""

import streamlit as st
from modules.materials import TAGS
from modules.ai import get_pattern_summary, is_ai_available
from modules.community import open_share_draft


def _notice_tags(n: dict) -> list:
    """Return tag keys for a notice, handling both old single-tag and new multi-tag formats."""
    if "tags" in n:
        return n["tags"]
    t = n.get("tag")
    return [t] if t else []


def noticelog_page():
    st.title("📋 Notice Log / 发现记录")
    st.markdown(
        '<p class="muted" style="margin-top:-8px;margin-bottom:20px;">'
        'Every gap you noticed between your production and the original, across all sessions. '
        'This is not a record of errors — it is a map of what you are actively working on.'
        '</p>', unsafe_allow_html=True
    )

    log = st.session_state.notice_log

    if not log:
        st.markdown("""
        <div style="text-align:center;padding:48px 24px;color:#9CA3AF;">
            <div style="font-size:2rem;margin-bottom:10px;">📋</div>
            <div style="font-size:1rem;font-weight:600;margin-bottom:6px;">
                No notices yet
            </div>
            <div style="font-size:.85rem;">
                Complete a session and use the Compare phase to start building your log.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start a session", type="primary"):
            st.session_state.page = "session"
            st.rerun()
        return

    # ── stats row ────────────────────────────────────────────────
    tag_counts: dict = {}
    for n in log:
        for t in _notice_tags(n):
            tag_counts[t] = tag_counts.get(t, 0) + 1

    top_tag = max(tag_counts, key=tag_counts.get) if tag_counts else None
    sessions = len({n.get("session_id","") for n in log})

    m1, m2, m3, m4 = st.columns(4)
    for col, num, lbl in [
        (m1, len(log),     "Total notices"),
        (m2, len(tag_counts), "Phenomenon types"),
        (m3, sessions,      "Sessions reviewed"),
        (m4, TAGS[top_tag]["label"] if top_tag else "—", "Most common"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;
                        padding:12px 10px;text-align:center;margin-bottom:16px;">
                <div style="font-size:1.4rem;font-weight:700;color:#1A3A5C;">{num}</div>
                <div style="font-size:.78rem;color:#6B7280;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── AI pattern summary (≥10 notices) ─────────────────────────
    if len(log) >= 10:
        # Try real GPT first
        ai_summary = get_pattern_summary(log)
        if ai_summary:
            st.markdown(
                '<div style="background:#F0FDF4;border:1.5px solid #6EE7B7;border-radius:12px;'
                'padding:16px 18px;margin-bottom:16px;">'
                '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:.05em;color:#065F46;margin-bottom:8px;">'
                f'🔍 AI Pattern Summary / AI规律总结 &nbsp;'
                f'<span style="font-weight:400;font-size:.75rem;">based on your {len(log)} notices</span>'
                '</div>'
                f'<div style="font-size:.88rem;color:#064E3B;line-height:1.65;white-space:pre-wrap;">'
                f'{ai_summary}</div></div>',
                unsafe_allow_html=True
            )
        else:
            _pattern_summary(log, tag_counts, top_tag)

    # ── filters ──────────────────────────────────────────────────
    st.markdown("---")
    fc1, fc2, fc3 = st.columns([2, 1.5, 1.5])
    with fc1:
        search = st.text_input("🔍 Search notices",
                               placeholder="keyword in your notice text…",
                               label_visibility="collapsed", key="nl_search")
    with fc2:
        type_opts = ["All types"] + [
            f'{v["label"]} / {v["zh"]}' for v in TAGS.values()
        ]
        type_filter = st.selectbox("Filter by type", type_opts,
                                   label_visibility="collapsed", key="nl_type")
    with fc3:
        sort_opt = st.selectbox("Sort", ["Newest first", "Oldest first", "By type"],
                                label_visibility="collapsed", key="nl_sort")

    # apply filters
    filtered = log[:]
    if type_filter != "All types":
        for k, v in TAGS.items():
            if v["label"] in type_filter:
                filtered = [n for n in filtered if k in _notice_tags(n)]
                break
    if search:
        filtered = [n for n in filtered
                    if search.lower() in n.get("text","").lower()]
    if "Oldest" in sort_opt:
        pass
    elif "type" in sort_opt.lower():
        filtered = sorted(filtered, key=lambda x: (_notice_tags(x) or [""])[0])
    else:
        filtered = list(reversed(filtered))

    st.markdown(
        f'<div class="muted" style="margin-bottom:10px;">'
        f'Showing {len(filtered)} of {len(log)} notices</div>',
        unsafe_allow_html=True
    )

    # ── notice cards ─────────────────────────────────────────────
    for i, notice in enumerate(filtered):
        _notice_card(notice, i)
        if st.button(
            "💬 Share to Community",
            key=f"share_community_{i}",
            help="Share this notice to the community forum",
        ):
            open_share_draft(notice)

    # ── clear ────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("⚠️ Clear Notice Log / 清空记录"):
        st.warning("This permanently deletes all notices. / 此操作将永久删除所有记录。")
        if st.button("🗑️ Clear all notices", key="nl_clear_all"):
            st.session_state.notice_log = []
            st.rerun()


def _notice_card(notice: dict, idx: int):
    tag_keys = _notice_tags(notice)
    first    = TAGS.get(tag_keys[0], {}) if tag_keys else {}
    left_border = first.get("color", "#E5E7EB")

    badges = "".join(
        f'<span style="background:{TAGS.get(k,{}).get("bg","#F3F4F6")};'
        f'color:{TAGS.get(k,{}).get("color","#6B7280")};'
        f'border:1px solid {TAGS.get(k,{}).get("border","#D1D5DB")};'
        f'border-radius:99px;padding:2px 10px;font-size:.74rem;font-weight:700;margin-right:4px;">'
        f'{TAGS.get(k,{}).get("label","?")} / {TAGS.get(k,{}).get("zh","")}</span>'
        for k in tag_keys if k in TAGS
    )

    st.markdown(
        f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;'
        f'border-left:4px solid {left_border};padding:14px 16px;margin-bottom:8px;">'
        f'<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px;">'
        f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{badges if badges else ""}</div>'
        f'<span style="font-size:.74rem;color:#9CA3AF;white-space:nowrap;margin-left:8px;">'
        f'{notice.get("material_title","")} · {notice.get("created_at","")}</span>'
        f'</div>'
        f'<div style="font-size:.9rem;font-weight:600;color:#1F2937;line-height:1.5;">'
        f'{notice.get("text","—")}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def _pattern_summary(log, tag_counts, top_tag):
    t = TAGS.get(top_tag, {})

    suggestions = {
        "stress":  (
            "You have recorded multiple Stress Pattern notices. This often reflects the "
            "syllable-timing tendency of Mandarin — treating all syllables as equally important. "
            "Before your next session, try marking the stressed syllable in every content word "
            "in the passage before you start listening."
        ),
        "link": (
            "Linking appears frequently in your notices. This is one of the most common "
            "challenges for Mandarin-speaking learners because Mandarin syllables have clear "
            "boundaries. Try drawing linking arcs in the text before you listen — "
            "predicting where linking will happen trains your ear to expect it."
        ),
        "weak": (
            "Weak forms appear often in your log. Focus one full session on a single function "
            "word — 'of', 'are', or 'a' — and listen for how reduced it sounds throughout "
            "the entire passage. This targeted listening builds a new phonological template."
        ),
        "intonation": (
            "You have noticed intonation differences in multiple sessions. Try humming the "
            "melody of each sentence before shadowing it, without any words. "
            "This isolates the pitch contour and makes it easier to imitate."
        ),
        "rhythm": (
            "Rhythm is your most noticed phenomenon. Tap the table on every stressed syllable "
            "as you shadow — do not tap on unstressed syllables. This makes stress-timing "
            "physical and reveals when you are giving too much time to unstressed syllables."
        ),
    }
    sugg = suggestions.get(
        top_tag,
        f"Review the {t.get('label','?')} concept card in the Phonology Guide."
    )

    pct = int(tag_counts.get(top_tag, 0) / len(log) * 100) if log else 0

    st.markdown(f"""
    <div style="background:#F0FDF4;border:1.5px solid #6EE7B7;border-radius:12px;
                padding:16px 18px;margin-bottom:16px;">
        <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:.05em;color:#065F46;margin-bottom:8px;">
            🔍 Pattern Summary / 规律总结
            <span style="font-weight:400;text-transform:none;font-size:.75rem;
                         color:#059669;margin-left:6px;">
                based on your {len(log)} notices
            </span>
        </div>
        <div style="font-size:.88rem;color:#064E3B;line-height:1.6;margin-bottom:8px;">
            Your most common notice type is
            <strong>{t.get('label','?')} / {t.get('zh','')}</strong>
            ({tag_counts.get(top_tag,0)} of {len(log)} notices, {pct}%).
            {sugg}
        </div>
        <div style="font-size:.78rem;color:#059669;">
            📚 See the <strong>{t.get('label','?')}</strong> card in the Phonology Guide
            for the full explanation and practice tips.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📖 Open Phonology Guide →", key="nl_open_phon"):
        st.session_state.phon_open_card = top_tag
        st.session_state.page = "phonology"
        st.rerun()
