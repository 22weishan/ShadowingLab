"""
research.py — Research Mode for ShadowingLab
=============================================
Experimental session studying shadowing's effect on F0 contours.

Flow:
  1. Recording Check — audio quality verification
  2. Participant Info — name only
  3. Pre-test — read L1 / S1 / Q1 (order not disclosed), auto-recorded
  4. Shadowing — listen once → shadow × 3 per sentence (all attempts recorded)
  5. Post-test — 6 sentences interleaved (trained + transfer), auto-recorded
  6. Export — ZIP with named WAVs + metadata CSV
"""

import streamlit as st
import base64, io, csv, zipfile
from datetime import datetime


# ── Sentence materials ────────────────────────────────────────────────────────

# Pre-test + Shadow: presented in L → S → Q order (not disclosed)
SHADOW_SENTENCES = [
    {"id": "L1", "type": "list",      "text": "I'll need your name, year, and University I.D."},
    {"id": "S1", "type": "statement", "text": "The videos are over there."},
    {"id": "Q1", "type": "question",  "text": "Is this the Carter Language Lab?"},
]

# Post-test: interleaved trained + transfer (order mixed, distinction not disclosed)
POSTTEST_SENTENCES = [
    {"id": "L1", "type": "list",      "text": "I'll need your name, year, and University I.D.",  "trained": True},
    {"id": "Q2", "type": "question",  "text": "Has it been moved?",                               "trained": False},
    {"id": "S1", "type": "statement", "text": "The videos are over there.",                       "trained": True},
    {"id": "L2", "type": "list",      "text": "The market sells ceramics, jewelry, and decorative items.", "trained": False},
    {"id": "Q1", "type": "question",  "text": "Is this the Carter Language Lab?",                "trained": True},
    {"id": "S2", "type": "statement", "text": "I'll wait to hear from you.",                     "trained": False},
]

TYPE_LABELS = {
    "question":  ("一般疑问句 ↑",  "Yes/No question — rising intonation at the end"),
    "statement": ("陈述句 ↓",      "Statement — falling intonation at the end"),
    "list":      ("列举句 ↑↑↓",    "List — rise on each item, fall on the final item"),
}

import os
from pathlib import Path
AUDIO_DIR = Path(__file__).parent.parent / "audio" / "experiment"

SHADOW_ATTEMPTS = 3   # simultaneous shadowing attempts per sentence


# ── State ─────────────────────────────────────────────────────────────────────

def _rs():
    if "research" not in st.session_state:
        st.session_state["research"] = {}
    return st.session_state["research"]

def _init_research():
    rs = _rs()
    rs.setdefault("phase",              "check")  # check|info|pretest|shadow|posttest|done
    rs.setdefault("participant_name",   "")
    rs.setdefault("started_at",         None)
    rs.setdefault("check_rec",          None)     # base64 of test recording
    rs.setdefault("pretest_recs",       {})       # {id: base64}
    rs.setdefault("shadow_recs",        {})       # {id_attempt: base64}
    rs.setdefault("shadow_sent_idx",    0)
    rs.setdefault("shadow_stage",       "listen") # listen|shadow
    rs.setdefault("shadow_attempt",     1)        # 1-3
    rs.setdefault("posttest_recs",      {})       # {id: base64}
    rs.setdefault("posttest_sent_idx",  0)
    rs.setdefault("pretest_sent_idx",   0)


# ── UI helpers ────────────────────────────────────────────────────────────────

def _banner(title_en, title_zh, desc, color, bg):
    st.markdown(
        f'<div style="background:{bg};border-left:5px solid {color};border-radius:10px;'
        f'padding:14px 18px;margin-bottom:20px;">'
        f'<div style="font-size:1.1rem;font-weight:700;color:{color};">{title_en} / {title_zh}</div>'
        f'<div style="font-size:.85rem;color:{color};opacity:.85;margin-top:4px;">{desc}</div>'
        f'</div>', unsafe_allow_html=True
    )

def _sent_card(sent, idx, total, color="#1A4B8C", show_type=True):
    type_zh, type_hint = TYPE_LABELS.get(sent["type"], ("",""))
    type_row = f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#9CA3AF;margin-bottom:6px;">Sentence {idx+1} of {total} &nbsp;·&nbsp; {sent["id"]}{(" &nbsp;·&nbsp; "+type_zh) if show_type else ""}</div>' if show_type else f'<div style="font-size:.72rem;color:#9CA3AF;margin-bottom:6px;">Sentence {idx+1} of {total}</div>'
    st.markdown(
        f'<div style="border:1px solid #E5E7EB;border-left:4px solid {color};'
        f'border-radius:10px;padding:16px 20px;background:#F9FAFB;margin-bottom:12px;">'
        f'{type_row}'
        f'<div style="font-size:1.15rem;font-weight:600;color:#1A1A2E;margin-bottom:8px;">{sent["text"]}</div>'
        + (f'<div style="font-size:.82rem;color:#6B7280;font-style:italic;">{type_hint}</div>' if show_type else '')
        + '</div>', unsafe_allow_html=True
    )

def _play_audio(sentence_id):
    path = AUDIO_DIR / f"{sentence_id}.mp3"
    if path.exists():
        data = path.read_bytes()
        b64 = base64.b64encode(data).decode()
        # Use components.html with unique key per sentence to prevent browser audio caching
        import streamlit.components.v1 as components
        components.html(
            f'''<audio id="audio_{sentence_id}" controls
                style="width:100%;margin-bottom:8px;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>''',
            height=60
        )
    else:
        st.warning(f"Audio not found: audio/experiment/{sentence_id}.mp3")

def _recorder(key, label="● Record / 录音"):
    try:
        from audio_recorder_streamlit import audio_recorder
        audio_bytes = audio_recorder(
            text=label, recording_color="#E53E3E",
            neutral_color="#374151", icon_size="2x", key=key
        )
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode()
    except ImportError:
        st.error("Run: pip install audio-recorder-streamlit")
    return None

def _pid(rs):
    """Sanitised participant ID for filenames."""
    return rs.get("participant_name","participant").replace(" ","_")

def _progress_bar(phase_order, current):
    labels = ["Check","Info","Pre-test","Shadowing","Post-test","Done"]
    keys   = ["check","info","pretest","shadow","posttest","done"]
    try: idx = keys.index(current)
    except: idx = 0
    html = '<div style="display:flex;gap:5px;margin-bottom:22px;">'
    for i, lbl in enumerate(labels):
        if i < idx:   bg,col = "#1A4B8C","white"
        elif i == idx: bg,col = "#3B82F6","white"
        else:          bg,col = "#F3F4F6","#9CA3AF"
        html += f'<div style="flex:1;text-align:center;padding:6px 2px;background:{bg};border-radius:6px;font-size:.75rem;font-weight:600;color:{col};">{lbl}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ── Phase 1: Recording Check ──────────────────────────────────────────────────

def _phase_check():
    rs = _rs()
    _banner("Recording Check", "录音质量检查",
            "Before we begin, please verify your audio setup. / 开始前，请先确认你的录音设备正常工作。",
            "#374151", "#F9FAFB")

    st.markdown("""
    <div style="background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:8px;
    padding:14px 18px;margin-bottom:16px;font-size:.88rem;color:#92400E;">
    <strong>Setup instructions / 设置说明</strong><br>
    • Use a quiet room / 请在安静的房间内进行<br>
    • Position microphone ~1 fist away from your mouth / 麦克风距嘴约一拳距离<br>
    • Headset microphone preferred / 建议使用耳机麦克风<br>
    • Speak at a normal conversational volume / 用正常对话音量说话
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Test sentence / 测试句子:**")
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:600;color:#1A1A2E;'
        'padding:12px 16px;background:#F3F4F6;border-radius:8px;margin-bottom:12px;">'
        'The weather is nice today.'
        '</div>', unsafe_allow_html=True
    )
    st.markdown('<div style="font-size:.82rem;color:#6B7280;margin-bottom:8px;">🎙 Record the sentence above, then play it back to verify the quality. / 录制上面的句子，然后回放确认录音质量。</div>', unsafe_allow_html=True)

    rec = _recorder("check_rec", "● Record test / 录制测试")
    if rec:
        rs["check_rec"] = rec

    if rs.get("check_rec"):
        st.markdown("**Playback / 回放:**")
        st.audio(base64.b64decode(rs["check_rec"]), format="audio/wav")

        st.markdown(
            '<div style="font-size:.85rem;color:#374151;margin:12px 0;">Can you hear yourself clearly? Is the audio free of distortion? / 你能清晰地听到自己的声音吗？录音是否没有杂音？</div>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Re-record / 重录", key="check_rerecord"):
                rs["check_rec"] = None
                st.rerun()
        with col2:
            if st.button("✅ Audio is good — Continue / 录音正常，继续", type="primary", key="check_ok"):
                rs["phase"] = "info"
                st.rerun()
    else:
        st.info("Record the test sentence above to continue. / 请先录制测试句子再继续。")


# ── Phase 2: Participant Info ─────────────────────────────────────────────────

def _phase_info():
    rs = _rs()
    _banner("Participant Information", "参与者信息",
            "Please enter your name to begin the experiment. / 请输入您的姓名开始实验。",
            "#1A4B8C", "#EEF3FA")

    name = st.text_input("Name / 姓名", value=rs.get("participant_name",""), placeholder="Your full name")

    st.markdown("""
    <div style="background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:8px;
    padding:12px 16px;font-size:.88rem;color:#92400E;margin:16px 0;">
    <strong>What to expect / 实验说明：</strong><br>
    This session has three parts: a pre-test reading, a shadowing practice, and a post-test reading.
    Please complete it in one sitting without interruption.<br>
    本次实验包含三个部分：前测朗读、跟读练习和后测朗读。请一次性完成，中间不要中断。
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶ Start Experiment / 开始实验", type="primary",
                  key="info_start", disabled=not name.strip()):
        rs["participant_name"] = name.strip()
        rs["started_at"]       = datetime.now().isoformat()
        rs["phase"]            = "pretest"
        rs["pretest_sent_idx"] = 0
        st.rerun()


# ── Phase 3: Pre-test ─────────────────────────────────────────────────────────

def _phase_pretest():
    rs = _rs()
    _banner("Pre-test", "前测",
            "Read each sentence aloud naturally. Do not listen to any audio first. "
            "Just read as you normally would. / "
            "请自然朗读以下句子，无需听录音，按自己的感觉念即可。",
            "#2E5FA3", "#EEF3FA")

    idx   = rs.get("pretest_sent_idx", 0)
    sents = SHADOW_SENTENCES   # same order: L → S → Q

    if idx >= len(sents):
        st.success("✅ Pre-test complete! / 前测完成！")
        if st.button("Continue to Shadowing / 继续跟读练习 →", type="primary", key="pretest_done"):
            rs["phase"]          = "shadow"
            rs["shadow_sent_idx"] = 0
            rs["shadow_stage"]   = "listen"
            rs["shadow_attempt"] = 1
            st.rerun()
        return

    sent = sents[idx]
    # Show type label to participant (it's pre-test so fine to show intonation type)
    _sent_card(sent, idx, len(sents), "#2E5FA3", show_type=False)

    st.markdown('<div style="font-size:.82rem;color:#6B7280;margin-bottom:8px;">🎙 Click to record, click again to stop. Recording will be saved automatically. / 点击录音，再次点击停止，录音自动保存。</div>', unsafe_allow_html=True)

    rec_key = f"pretest_{sent['id']}_{idx}"
    recorded = _recorder(rec_key)
    existing = rs["pretest_recs"].get(sent["id"])
    if recorded:
        rs["pretest_recs"][sent["id"]] = recorded
        existing = recorded

    if existing:
        st.markdown("**Your recording / 你的录音:**")
        st.audio(base64.b64decode(existing), format="audio/wav")
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button("Re-record / 重录", key=f"pre_redo_{idx}"):
                rs["pretest_recs"].pop(sent["id"], None)
                st.rerun()
        with col2:
            label = "Next →" if idx < len(sents)-1 else "Finish pre-test →"
            if st.button(label, type="primary", key=f"pre_next_{idx}"):
                rs["pretest_sent_idx"] = idx + 1
                st.rerun()
    else:
        st.info("Record your reading above to continue. / 请先录音再继续。")

    # Progress dots
    dots = "".join(f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{"#2E5FA3" if i<=idx else "#E5E7EB"};margin:0 3px;"></span>' for i in range(len(sents)))
    st.markdown(f'<div style="margin-top:16px;">{dots}</div>', unsafe_allow_html=True)


# ── Phase 4: Shadowing ────────────────────────────────────────────────────────

INTONATION_GUIDE = """
**Intonation Guidelines / 语调指引**

| Type | Pattern | Example |
|------|---------|---------|
| Yes/No question (Q ↑) | Rising ↗ at the end | *Is this the lab?* ↗ |
| Statement (S ↓) | Falling ↘ at the end | *The videos are there.* ↘ |
| List (L ↑↑↓) | Rise ↗ on each item, fall ↘ on the last | *name ↗, year ↗, I.D. ↘* |

**While shadowing / 跟读时请注意：**
1. Listen carefully to the speaker's exact pronunciation / 仔细聆听说话人的发音
2. Imitate the speaker's intonation as closely as possible / 尽量模仿说话人的语调
3. Focus on the rise and fall of pitch / 关注音调的升降变化
"""

def _phase_shadow():
    rs = _rs()
    idx     = rs.get("shadow_sent_idx", 0)
    stage   = rs.get("shadow_stage", "listen")  # "listen" or "shadow"
    attempt = rs.get("shadow_attempt", 1)
    sents   = SHADOW_SENTENCES

    if idx >= len(sents):
        st.success("✅ Shadowing complete! / 跟读练习完成！")
        if st.button("Continue to Post-test / 继续后测 →", type="primary", key="shadow_done"):
            rs["phase"]             = "posttest"
            rs["posttest_sent_idx"] = 0
            st.rerun()
        return

    sent = sents[idx]

    if stage == "listen":
        _banner("Shadowing — Listen", "跟读 — 听录音",
                "Listen carefully to the native speaker. Do not speak yet. / 仔细听母语者录音，暂时不要跟读。",
                "#1A7A6E", "#E8F5F3")

        # Show intonation guide before first sentence
        if idx == 0:
            with st.expander("📋 Intonation Guidelines / 语调指引 (read before starting)", expanded=True):
                st.markdown(INTONATION_GUIDE)

        st.markdown(f'<div style="font-size:.78rem;color:#9CA3AF;margin-bottom:10px;">Sentence {idx+1} of {len(sents)} &nbsp;·&nbsp; {sent["id"]}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-left:4px solid #1A7A6E;'
            f'border-radius:10px;padding:16px 20px;background:#F9FAFB;margin-bottom:12px;">'
            f'<div style="font-size:1.15rem;font-weight:600;color:#1A1A2E;">{sent["text"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

        st.markdown("**🎵 Listen carefully / 仔细聆听：**")
        _play_audio(sent["id"])

        if st.button("Ready to shadow / 准备好跟读了 →", type="primary", key=f"listen_done_{idx}"):
            rs["shadow_stage"]   = "shadow"
            rs["shadow_attempt"] = 1
            st.rerun()

    else:  # stage == "shadow"
        _banner(f"Shadowing — Attempt {attempt}/{SHADOW_ATTEMPTS}", f"跟读 — 第{attempt}次",
                "Shadow the audio out loud simultaneously. Your voice is being recorded. / "
                "大声同声跟读，本次录音将自动保存。",
                "#6B3FA0", "#F5F3FF")

        st.markdown(f'<div style="font-size:.78rem;color:#9CA3AF;margin-bottom:10px;">Sentence {idx+1} of {len(sents)} &nbsp;·&nbsp; {sent["id"]} &nbsp;·&nbsp; Attempt {attempt} of {SHADOW_ATTEMPTS}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-left:4px solid #6B3FA0;'
            f'border-radius:10px;padding:16px 20px;background:#F9FAFB;margin-bottom:12px;">'
            f'<div style="font-size:1.15rem;font-weight:600;color:#1A1A2E;">{sent["text"]}</div>'
            f'</div>', unsafe_allow_html=True
        )

        st.markdown("**🎵 Play audio and shadow simultaneously / 播放并同声跟读：**")
        _play_audio(sent["id"])

        st.markdown(
            '<div style="background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:8px;'
            'padding:10px 14px;font-size:.85rem;color:#5B21B6;margin-bottom:10px;">'
            f'🎙 Attempt {attempt} of {SHADOW_ATTEMPTS} — shadow out loud while the audio plays / '
            f'第{attempt}次，跟着录音大声跟读</div>',
            unsafe_allow_html=True
        )

        rec_key = f"shadow_{sent['id']}_attempt{attempt}"
        recorded = _recorder(rec_key, label=f"● Shadow Attempt {attempt} / 第{attempt}次跟读")
        existing = rs["shadow_recs"].get(rec_key)
        if recorded:
            rs["shadow_recs"][rec_key] = recorded
            existing = recorded

        if existing:
            st.markdown("**Playback / 回放:**")
            st.audio(base64.b64decode(existing), format="audio/wav")

            col1, col2 = st.columns([1,2])
            with col1:
                if st.button("Re-record / 重录", key=f"sh_redo_{idx}_{attempt}"):
                    rs["shadow_recs"].pop(rec_key, None)
                    st.rerun()
            with col2:
                if attempt < SHADOW_ATTEMPTS:
                    if st.button(f"Next attempt ({attempt+1}/{SHADOW_ATTEMPTS}) →", type="primary", key=f"sh_next_{idx}_{attempt}"):
                        rs["shadow_attempt"] = attempt + 1
                        st.rerun()
                else:
                    # All 3 attempts done
                    is_last = (idx == len(sents) - 1)
                    label = "Finish shadowing →" if is_last else f"Next sentence ({idx+2}/{len(sents)}) →"
                    if st.button(label, type="primary", key=f"sh_nextsent_{idx}"):
                        rs["shadow_sent_idx"] = idx + 1
                        rs["shadow_stage"]    = "listen"
                        rs["shadow_attempt"]  = 1
                        st.rerun()
        else:
            st.info("Record your shadowing above to continue. / 请先录音再继续。")

        # Attempt progress dots
        dots = "".join(f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{"#6B3FA0" if i<attempt else "#E5E7EB"};margin:0 3px;"></span>' for i in range(SHADOW_ATTEMPTS))
        st.markdown(f'<div style="margin-top:12px;">{dots}</div>', unsafe_allow_html=True)


# ── Phase 5: Post-test ────────────────────────────────────────────────────────

def _phase_posttest():
    rs = _rs()
    _banner("Post-test", "后测",
            "Read each sentence aloud. No audio will play. / "
            "请朗读以下句子，不会播放录音，仅根据文字朗读。",
            "#B54F1A", "#FBF0EB")

    idx   = rs.get("posttest_sent_idx", 0)
    sents = POSTTEST_SENTENCES

    if idx >= len(sents):
        st.success("✅ Post-test complete! / 后测完成！")
        if st.button("View results & export / 查看结果并导出 →", type="primary", key="posttest_done"):
            rs["phase"] = "done"
            st.rerun()
        return

    sent = sents[idx]
    _sent_card(sent, idx, len(sents), "#B54F1A", show_type=False)

    st.markdown('<div style="font-size:.82rem;color:#6B7280;margin-bottom:8px;">🎙 Click to record, click again to stop. / 点击录音，再次点击停止。</div>', unsafe_allow_html=True)

    rec_key = f"posttest_{sent['id']}_{idx}"
    recorded = _recorder(rec_key)
    existing = rs["posttest_recs"].get(f"{sent['id']}_{idx}")
    if recorded:
        rs["posttest_recs"][f"{sent['id']}_{idx}"] = recorded
        existing = recorded

    if existing:
        st.markdown("**Your recording / 你的录音:**")
        st.audio(base64.b64decode(existing), format="audio/wav")
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button("Re-record / 重录", key=f"post_redo_{idx}"):
                rs["posttest_recs"].pop(f"{sent['id']}_{idx}", None)
                st.rerun()
        with col2:
            label = "Next →" if idx < len(sents)-1 else "Finish post-test →"
            if st.button(label, type="primary", key=f"post_next_{idx}"):
                rs["posttest_sent_idx"] = idx + 1
                st.rerun()
    else:
        st.info("Record your reading above to continue. / 请先录音再继续。")

    dots = "".join(f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{"#B54F1A" if i<=idx else "#E5E7EB"};margin:0 3px;"></span>' for i in range(len(sents)))
    st.markdown(f'<div style="margin-top:16px;">{dots}</div>', unsafe_allow_html=True)


# ── Phase 6: Done + Export ────────────────────────────────────────────────────

def _phase_done():
    rs  = _rs()
    pid = _pid(rs)

    st.markdown("### ✅ Experiment Complete / 实验完成")
    st.markdown(
        f'<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:10px;'
        f'padding:16px 20px;margin-bottom:20px;font-size:.9rem;color:#065F46;">'
        f'Thank you, <strong>{rs.get("participant_name","")}</strong>! '
        f'Please download the data file below and send it to the researcher.<br>'
        f'感谢您的参与！请下载下方数据包并发送给研究者。</div>',
        unsafe_allow_html=True
    )

    n_pre    = len(rs.get("pretest_recs",  {}))
    n_shadow = len(rs.get("shadow_recs",   {}))
    n_post   = len(rs.get("posttest_recs", {}))
    c1,c2,c3 = st.columns(3)
    for col,n,lbl in [(c1,n_pre,"Pre-test"),(c2,n_shadow,"Shadow"),(c3,n_post,"Post-test")]:
        with col:
            st.markdown(f'<div style="text-align:center;padding:12px;background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;"><div style="font-size:1.6rem;font-weight:700;color:#1A4B8C;">{n}</div><div style="font-size:.8rem;color:#6B7280;">{lbl} recordings</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📦 Download Data / 下载数据")

    zip_buf  = _build_zip(rs, pid)
    ts       = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ShadowingLab_{pid}_{ts}.zip"

    st.download_button(
        label="⬇ Download ZIP (WAVs + metadata.csv) / 下载数据包",
        data=zip_buf, file_name=filename, mime="application/zip", type="primary"
    )
    st.markdown('<div style="font-size:.82rem;color:#9CA3AF;margin-top:8px;">ZIP contains all WAV files organised by phase, plus a metadata CSV. / 数据包含按阶段整理的WAV录音文件和元数据CSV。</div>', unsafe_allow_html=True)

    if st.button("Start new session / 开始新实验", key="research_restart"):
        st.session_state["research"] = {}
        _init_research()
        st.rerun()


def _build_zip(rs, pid) -> bytes:
    participant = rs.get("participant_name", "unknown")
    started_at  = rs.get("started_at", "")
    buf = io.BytesIO()

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        rows = []

        # Pre-test
        for sent_id, b64 in rs.get("pretest_recs", {}).items():
            fname = f"pretest/{pid}_pretest_{sent_id}.wav"
            zf.writestr(fname, base64.b64decode(b64))
            sent = next((s for s in SHADOW_SENTENCES if s["id"]==sent_id), {})
            rows.append({"participant":participant,"started_at":started_at,
                         "phase":"pretest","sentence_id":sent_id,
                         "sentence_type":sent.get("type",""),"text":sent.get("text",""),
                         "attempt":1,"file":fname})

        # Shadow — all attempts
        for key, b64 in rs.get("shadow_recs", {}).items():
            # key: shadow_{id}_attempt{n}
            parts   = key.split("_")
            sent_id = parts[1] if len(parts)>2 else key
            attempt = parts[-1].replace("attempt","") if "attempt" in key else "1"
            fname   = f"shadow/{pid}_shadow_{sent_id}_attempt{attempt}.wav"
            zf.writestr(fname, base64.b64decode(b64))
            sent = next((s for s in SHADOW_SENTENCES if s["id"]==sent_id), {})
            rows.append({"participant":participant,"started_at":started_at,
                         "phase":"shadow","sentence_id":sent_id,
                         "sentence_type":sent.get("type",""),"text":sent.get("text",""),
                         "attempt":attempt,"file":fname})

        # Post-test
        for key, b64 in rs.get("posttest_recs", {}).items():
            # key: {id}_{position_idx}
            parts   = key.rsplit("_",1)
            sent_id = parts[0]
            pos_idx = int(parts[1]) if len(parts)>1 else 0
            sent    = POSTTEST_SENTENCES[pos_idx] if pos_idx < len(POSTTEST_SENTENCES) else {}
            trained = sent.get("trained", True)
            fname   = f"posttest/{pid}_posttest_{sent_id}.wav"
            zf.writestr(fname, base64.b64decode(b64))
            rows.append({"participant":participant,"started_at":started_at,
                         "phase":"posttest","sentence_id":sent_id,
                         "sentence_type":sent.get("type",""),"text":sent.get("text",""),
                         "trained_item":trained,"attempt":1,"file":fname})

        # CSV
        if rows:
            sbuf = io.StringIO()
            fields = list(rows[0].keys())
            w = csv.DictWriter(sbuf, fieldnames=fields)
            w.writeheader()
            for row in rows:
                w.writerow({f: row.get(f,"") for f in fields})
            zf.writestr("metadata.csv", sbuf.getvalue())

    buf.seek(0)
    return buf.read()


# ── Entry point ───────────────────────────────────────────────────────────────

def research_page():
    _init_research()
    rs = _rs()

    st.title("🔬 Research Mode / 研究模式")
    st.markdown('<p style="color:#6B7280;margin-top:-8px;margin-bottom:20px;">Experimental session: shadowing and F0 contour production · 实验模式：跟读对F0轮廓的影响研究</p>', unsafe_allow_html=True)

    _progress_bar(None, rs.get("phase","check"))

    phase = rs.get("phase","check")
    if   phase == "check":    _phase_check()
    elif phase == "info":     _phase_info()
    elif phase == "pretest":  _phase_pretest()
    elif phase == "shadow":   _phase_shadow()
    elif phase == "posttest": _phase_posttest()
    elif phase == "done":     _phase_done()
