"""
progress.py — Progress dashboard

Layout:
  Row 1 — Overview stats (3 metric cards)
  Row 2 — Gap Map (notice type bar chart, min 1 session)
  Row 3 — Mastered vs Still Noticing (Adaptive Fading, min 3 sessions)
  Row 4 — Session History (expandable)
  Row 5 — Vocabulary Bank
"""

import streamlit as st
from modules.materials import TAGS

_MASTERY_THRESHOLD = 5   # sessions without a notice type → mastered


def progress_page():
    st.title("📈 Progress / 学习进度")
    st.markdown(
        '<p class="muted" style="margin-top:-8px;margin-bottom:20px;">'
        "Your learning history across all sessions."
        "</p>", unsafe_allow_html=True
    )

    history = st.session_state.session_history
    log     = st.session_state.notice_log
    vocab   = st.session_state.vocabulary

    if not history:
        st.markdown("""
        <div style="text-align:center;padding:48px 24px;color:#9CA3AF;">
            <div style="font-size:2rem;margin-bottom:10px;">📈</div>
            <div style="font-size:1rem;font-weight:600;margin-bottom:6px;">
                No sessions completed yet
            </div>
            <div style="font-size:.85rem;">
                Complete your first session to see your progress here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start a session", type="primary"):
            st.session_state.page = "session"
            st.rerun()
        return

    # ── ROW 1: Overview metric cards ─────────────────────────────
    total_notices = sum(h["notices"] for h in history)

    # most noticed type across all sessions
    tag_counts: dict = {}
    for n in log:
        t = n.get("tag")
        if t:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    most_noticed_key = max(tag_counts, key=tag_counts.get) if tag_counts else None
    most_noticed_lbl = (
        TAGS[most_noticed_key]["label"] if most_noticed_key and most_noticed_key in TAGS
        else "—"
    )

    c1, c2, c3 = st.columns(3)
    for col, num, lbl, sublbl in [
        (c1, len(history),   "Sessions",       "completed"),
        (c2, total_notices,  "Total notices",  "logged"),
        (c3, most_noticed_lbl, "Most noticed", "phonology type"),
    ]:
        with col:
            is_text = isinstance(num, str)
            st.markdown(
                f'<div style="background:#F9FAFB;border:1px solid #E5E7EB;'
                f'border-radius:12px;padding:16px 12px;text-align:center;">'
                f'<div style="font-size:{"1.1rem" if is_text else "1.8rem"};font-weight:700;'
                f'color:#1A3A5C;margin-bottom:2px;">{num}</div>'
                f'<div style="font-size:.75rem;font-weight:600;color:#374151;">{lbl}</div>'
                f'<div style="font-size:.7rem;color:#9CA3AF;">{sublbl}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    # ── ROW 2: Gap Map ────────────────────────────────────────────
    st.markdown(
        '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.06em;color:#9CA3AF;margin-bottom:10px;">'
        "Gap Map / 差距地图</div>",
        unsafe_allow_html=True
    )

    if tag_counts:
        total_tagged = sum(tag_counts.values())
        sorted_tags  = sorted(tag_counts.items(), key=lambda x: -x[1])
        for tag_key, count in sorted_tags:
            t   = TAGS.get(tag_key, {})
            pct = int(count / total_tagged * 100) if total_tagged else 0
            bar_color = t.get("color", "#2563EB")
            bg_color  = t.get("bg",    "#F3F4F6")
            label     = t.get("label", tag_key)
            zh        = t.get("zh",    "")
            st.markdown(
                f'<div style="margin-bottom:10px;">'
                f'<div style="display:flex;justify-content:space-between;'
                f'align-items:center;margin-bottom:4px;">'
                f'<span style="display:flex;align-items:center;gap:6px;">'
                f'<span style="background:{bg_color};color:{bar_color};'
                f'border-radius:99px;padding:2px 10px;font-size:.75rem;font-weight:700;">'
                f'{label}</span>'
                f'<span style="font-size:.78rem;color:#9CA3AF;">{zh}</span>'
                f'</span>'
                f'<span style="font-size:.78rem;color:#6B7280;font-weight:600;">'
                f'{count} notice{"s" if count!=1 else ""} &nbsp;·&nbsp; {pct}%</span>'
                f'</div>'
                f'<div style="background:#F3F4F6;border-radius:99px;height:8px;overflow:hidden;">'
                f'<div style="width:{pct}%;height:100%;background:{bar_color};'
                f'border-radius:99px;transition:width .3s;"></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div style="color:#9CA3AF;font-size:.85rem;padding:12px 0;">'
            "No notices logged yet — complete a session and use the Notice Log.</div>",
            unsafe_allow_html=True
        )

    # ── ROW 3: Adaptive Fading (Mastered vs Still Noticing) ───────
    n_sessions = len(history)
    if n_sessions >= 3 and tag_counts:
        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:.06em;color:#9CA3AF;margin-bottom:10px;">'
            "Phonology Status / 语音现象掌握情况</div>",
            unsafe_allow_html=True
        )

        # figure out which tags appeared in last N sessions
        recent_sessions = history[-_MASTERY_THRESHOLD:]
        recent_tags: set = set()
        for h in recent_sessions:
            for t in h.get("tag_distribution", {}).keys():
                recent_tags.add(t)

        all_seen_tags = set(tag_counts.keys())
        mastered    = [t for t in all_seen_tags if t not in recent_tags]
        still_noticing = [t for t in all_seen_tags if t in recent_tags]

        col_m, col_s = st.columns(2)
        with col_m:
            st.markdown(
                '<div style="background:#F0FDF4;border:1px solid #86EFAC;'
                'border-radius:12px;padding:14px 16px;">'
                '<div style="font-size:.72rem;font-weight:700;color:#166534;'
                'text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px;">'
                "✅ Mastered / 已掌握</div>",
                unsafe_allow_html=True
            )
            if mastered:
                for tk in mastered:
                    t = TAGS.get(tk, {})
                    st.markdown(
                        f'<div style="font-size:.82rem;color:#166534;margin-bottom:4px;">'
                        f'• {t.get("label", tk)}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div style="font-size:.78rem;color:#6B7280;">None yet — '
                    f'keep practising! Mastery = absent for {_MASTERY_THRESHOLD} sessions.</div>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_s:
            st.markdown(
                '<div style="background:#FFFBEB;border:1px solid #FDE68A;'
                'border-radius:12px;padding:14px 16px;">'
                '<div style="font-size:.72rem;font-weight:700;color:#92400E;'
                'text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px;">'
                "⚠️ Still noticing / 仍需注意</div>",
                unsafe_allow_html=True
            )
            if still_noticing:
                for tk in still_noticing:
                    t = TAGS.get(tk, {})
                    st.markdown(
                        f'<div style="font-size:.82rem;color:#92400E;margin-bottom:4px;">'
                        f'• {t.get("label", tk)}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div style="font-size:.78rem;color:#6B7280;">—</div>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

    elif n_sessions < 3:
        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;'
            f'padding:12px 16px;font-size:.82rem;color:#9CA3AF;">'
            f'Complete {3 - n_sessions} more session{"s" if 3-n_sessions!=1 else ""} '
            f'to unlock Phonology Status.</div>',
            unsafe_allow_html=True
        )

    # ── ROW 4: Session History ────────────────────────────────────
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.06em;color:#9CA3AF;margin-bottom:10px;">'
        "Session History / 学习记录</div>",
        unsafe_allow_html=True
    )

    for h in reversed(history):
        tag_dist  = h.get("tag_distribution", {})
        tag_chips = "".join(
            f'<span style="background:{TAGS[k]["bg"]};color:{TAGS[k]["color"]};'
            f'border-radius:99px;padding:1px 8px;font-size:.72rem;font-weight:700;'
            f'margin-right:3px;">{TAGS[k]["label"]} ×{v}</span>'
            for k, v in tag_dist.items() if k in TAGS
        )
        ref     = h.get("reflection", {})
        has_ref = any(ref.get(k) for k in ["notice", "reason", "focus"])

        with st.expander(
            f"📅 {h['date']}  ·  {h['material_title']}  ·  {h['notices']} notice{'s' if h['notices']!=1 else ''}"
        ):
            sc1, sc2, sc3 = st.columns(3)
            for col, num, lbl in [
                (sc1, h["notices"],             "Notices"),
                (sc2, h.get("sentences",  0),   "Sentences"),
                (sc3, h.get("recordings", 0),   "Recordings"),
            ]:
                with col:
                    st.markdown(
                        f'<div style="text-align:center;padding:8px 0;">'
                        f'<div style="font-size:1.2rem;font-weight:700;color:#1A3A5C;">{num}</div>'
                        f'<div style="font-size:.75rem;color:#6B7280;">{lbl}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            if tag_chips:
                st.markdown(f"**Notices by type:** {tag_chips}", unsafe_allow_html=True)

            if has_ref:
                st.markdown("**Reflection**")
                ref_cols = st.columns(3)
                for col, key, icon, label in [
                    (ref_cols[0], "notice", "①", "What I noticed"),
                    (ref_cols[1], "reason", "②", "Why it happened"),
                    (ref_cols[2], "focus",  "③", "Next focus"),
                ]:
                    with col:
                        val = ref.get(key, "")
                        if val:
                            st.markdown(
                                f'<div style="background:#F9FAFB;border-radius:8px;'
                                f'padding:10px 12px;font-size:.83rem;">'
                                f'<div style="font-weight:600;color:#374151;margin-bottom:4px;">'
                                f'{icon} {label}</div>'
                                f'<div style="color:#6B7280;">{val}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

    # ── ROW 5: Vocabulary Bank ────────────────────────────────────
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.06em;color:#9CA3AF;margin-bottom:10px;">'
        "Vocabulary Bank / 生词库</div>",
        unsafe_allow_html=True
    )

    if vocab:
        chips = "".join(
            f'<span style="background:#DBEAFE;color:#1D4ED8;border:1px solid #93C5FD;'
            f'border-radius:99px;padding:4px 12px;font-size:.85rem;font-weight:600;'
            f'margin:3px 4px 3px 0;display:inline-block;">{w}</span>'
            for w in vocab
        )
        st.markdown(chips, unsafe_allow_html=True)
        if st.button("Clear vocabulary", key="prog_clear_vocab"):
            st.session_state.vocabulary = []
            st.rerun()
    else:
        st.markdown(
            '<div style="color:#9CA3AF;font-size:.85rem;">No vocabulary words saved yet.</div>',
            unsafe_allow_html=True
        )
