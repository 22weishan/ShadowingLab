"""
session.py  —  the full 5-phase session flow

Phase 1  select   — material picker
Phase 2  prepare  — parallel listening + vocab
Phase 3  shadow   — sentence / passage shadowing + recording
Phase 4  compare  — side-by-side playback + notice input
Phase 5  capture  — structured reflection + session summary
"""

import streamlit as st
import streamlit.components.v1 as components
import base64, json, os
from datetime import datetime

from modules.state     import start_new_session, advance_phase
from modules.materials import get_all_materials, get_segments, TAGS
from modules.phonology  import inline_concept_card
from modules.ai         import get_session_suggestion, is_ai_available, get_timestamps_for_material
from modules.userdata   import save_user_data


# ══════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def session_page():
    phase = st.session_state.get("session_phase", "select")
    if   phase == "select":  _phase_select()
    elif phase == "prepare": _phase_prepare()
    elif phase == "shadow":  _phase_shadow()
    elif phase == "compare": _phase_compare()
    elif phase == "capture": _phase_capture()


# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════

def _load_audio_b64(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def _phase_header(phase_num: int, title_en: str, title_zh: str,
                  color: str, bg: str, desc: str):
    st.markdown(f"""
    <div class="phase-banner" style="background:{bg};border:1px solid {color}30;">
        <div style="font-size:1.6rem;flex-shrink:0;">{"①②③④⑤"[phase_num-1]}</div>
        <div>
            <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.06em;color:{color};margin-bottom:2px;">
                Phase {phase_num} of 5
            </div>
            <div style="font-size:1.05rem;font-weight:700;color:{color};">
                {title_en} / {title_zh}
            </div>
            <div style="font-size:.83rem;color:{color};opacity:.85;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _tag_chip(tag_key: str, size: str = "normal") -> str:
    t = TAGS.get(tag_key, {})
    fs = ".72rem" if size == "small" else ".78rem"
    return (
        f'<span class="tag-chip" '
        f'style="background:{t.get("bg","#F3F4F6")};color:{t.get("color","#374151")};'
        f'border:1px solid {t.get("border","#D1D5DB")};font-size:{fs};">'
        f'{t.get("label","?")} / {t.get("zh","")}</span>'
    )


def _progress_bar(pct: int, color: str = "#2563EB") -> str:
    return (
        f'<div class="prog-bar-wrap">'
        f'<div class="prog-bar-fill" style="width:{pct}%;background:{color};"></div>'
        f'</div>'
    )


def _annotated_sentence_html(seg: dict, active: bool = False,
                              show_annotations: bool = True) -> str:
    """
    Render a sentence with inline phonological annotation labels above
    flagged words.  Returns an HTML string.
    """
    words  = seg["text"].split()
    anns   = {a["word"].rstrip(".,!?;"): a for a in seg.get("annotations", [])}
    rows_top, rows_word = [], []

    for w in words:
        clean = w.rstrip(".,!?;")
        ann   = anns.get(clean)
        if ann and show_annotations:
            tag = TAGS.get(ann["type"], {})
            top = (f'<span class="{tag.get("css","ann-stress")}" '
                   f'style="white-space:nowrap;">{ann["label"]}</span>')
        else:
            top = '<span style="visibility:hidden;font-size:.7rem;">·</span>'
        rows_top.append(f'<td style="text-align:center;padding:0 3px;">{top}</td>')
        rows_word.append(
            f'<td style="text-align:center;padding:0 3px;font-size:.95rem;'
            f'{"font-weight:600;" if active else ""}">{w}</td>'
        )

    bg  = "#DBEAFE" if active else "transparent"
    bl  = "4px solid #2563EB" if active else "none"
    return (
        f'<div style="background:{bg};border-left:{bl};border-radius:6px;'
        f'padding:8px 10px;margin:6px 0;overflow-x:auto;">'
        f'<table style="border-collapse:collapse;">'
        f'<tr>{"".join(rows_top)}</tr>'
        f'<tr>{"".join(rows_word)}</tr>'
        f'</table></div>'
    )


_GET_NONBT_MIC_JS = """
// Prefer built-in / non-Bluetooth microphone to keep Bluetooth headphones
// in A2DP (high-quality) mode during simultaneous playback + recording.
async function getNonBtStream() {
  // Probe to unlock device labels (immediately released)
  try {
    const probe = await navigator.mediaDevices.getUserMedia({audio:true,video:false});
    probe.getTracks().forEach(t=>t.stop());
  } catch(_) {}

  const devices = await navigator.mediaDevices.enumerateDevices();
  const mics = devices.filter(d =>
    d.kind==='audioinput' &&
    d.deviceId!=='default' &&
    d.deviceId!=='communications'
  );

  const btKw   = ['bluetooth','airpods','beats','wireless','headset','headphone',
                  'bose','sony','jabra','sennheiser','plantronics','poly','anker'];
  const biKw   = ['built-in','macbook','internal','内置','laptop','built in'];

  // 1. Explicitly built-in
  let pick = mics.find(m => biKw.some(k => m.label.toLowerCase().includes(k)));
  // 2. Any non-Bluetooth
  if (!pick) pick = mics.find(m => !btKw.some(k => m.label.toLowerCase().includes(k)));
  // 3. Fallback: whatever is available
  if (!pick && mics.length) pick = mics[0];

  const constraints = {audio:{
    deviceId: pick ? {ideal: pick.deviceId} : undefined,
    echoCancellation:false, noiseSuppression:false,
    autoGainControl:false, channelCount:1
  }, video:false};
  return navigator.mediaDevices.getUserMedia(constraints);
}
"""


def _js_recorder_component(rec_key: str, label_en: str, label_zh: str) -> dict | None:
    """
    Custom JS recorder. Prefers built-in / non-Bluetooth microphone so that
    Bluetooth headphones stay in A2DP (high-quality) mode during recording.
    Returns {type:'rec', value:<base64>} on new recording, else None.
    """
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:transparent;}}
#wrap{{padding:6px 0;}}
.lbl{{font-size:.78rem;color:#6B7280;margin-bottom:8px;}}
#btn{{background:#2563EB;color:#fff;border:none;border-radius:8px;
      padding:8px 18px;font-size:.85rem;font-weight:700;cursor:pointer;}}
#btn:hover{{background:#1D4ED8;}}
#btn.rec{{background:#DC2626;animation:pulse 1s infinite;}}
#btn:disabled{{opacity:.4;cursor:not-allowed;animation:none;}}
@keyframes pulse{{0%,100%{{opacity:1;}}50%{{opacity:.7;}}}}
#status{{font-size:.78rem;margin-top:6px;color:#6B7280;min-height:18px;}}
#err{{font-size:.78rem;margin-top:4px;color:#DC2626;min-height:14px;}}
#micinfo{{font-size:.72rem;color:#9CA3AF;margin-top:2px;min-height:14px;}}
audio{{margin-top:8px;width:100%;max-width:340px;display:none;}}
</style></head><body>
<!-- key:{rec_key} -->
<div id="wrap">
  <div class="lbl">🎙️ {label_en} / {label_zh}</div>
  <button id="btn" onclick="toggle()">▶ Start Recording</button>
  <div id="status">Click to start recording.</div>
  <div id="err"></div>
  <div id="micinfo"></div>
  <audio id="preview" controls></audio>
</div>
<script>
(function(){{
function post(type,extra){{
  window.parent.postMessage(Object.assign({{isStreamlitMessage:true,type:type}},extra),"*");
}}
function SL_setFrameHeight(h){{post("streamlit:setFrameHeight",{{height:h}});}}
function SL_setValue(val){{post("streamlit:setComponentValue",{{value:val,dataType:"json"}});}}
post("streamlit:componentReady",{{apiVersion:1}});

{_GET_NONBT_MIC_JS}

let recorder=null,chunks=[],stream=null,recording=false;
const btn=document.getElementById("btn");
const status=document.getElementById("status");
const err=document.getElementById("err");
const micinfo=document.getElementById("micinfo");
const preview=document.getElementById("preview");

function toggle(){{ if(!recording) startRec(); else stopRec(); }}
window.toggle=toggle;

async function startRec(){{
  err.textContent=""; micinfo.textContent="";
  try{{
    stream=await getNonBtStream();
    const track=stream.getAudioTracks()[0];
    if(track) micinfo.textContent="🎤 "+track.label;
  }}catch(e){{
    if(e.name==="NotAllowedError"||e.name==="PermissionDeniedError")
      err.textContent="❌ Microphone access denied.";
    else if(e.name==="NotFoundError")
      err.textContent="❌ No microphone found.";
    else
      err.textContent="❌ Could not access microphone: "+e.message;
    return;
  }}
  chunks=[];
  let mimeType="audio/webm;codecs=opus";
  if(!MediaRecorder.isTypeSupported(mimeType)) mimeType="audio/webm";
  if(!MediaRecorder.isTypeSupported(mimeType)) mimeType="";
  recorder=new MediaRecorder(stream,mimeType?{{mimeType,audioBitsPerSecond:128000}}:{{}});
  recorder.ondataavailable=e=>{{ if(e.data.size>0) chunks.push(e.data); }};
  recorder.onstop=()=>{{
    const blob=new Blob(chunks,{{type:mimeType||"audio/webm"}});
    preview.src=URL.createObjectURL(blob);
    preview.style.display="block";
    SL_setFrameHeight(document.body.scrollHeight);
    status.textContent="⏳ Saving…";
    const reader=new FileReader();
    reader.onloadend=()=>{{
      SL_setValue({{type:"rec",value:reader.result.split(",")[1]}});
      status.textContent="✅ Saved — page updating…";
      btn.disabled=false;
      btn.textContent="▶ Start Recording";
      btn.classList.remove("rec");
    }};
    reader.readAsDataURL(blob);
    stream.getTracks().forEach(t=>t.stop()); stream=null;
  }};
  recorder.start();
  recording=true;
  btn.textContent="⏹ Stop Recording";
  btn.classList.add("rec");
  status.textContent="🔴 Recording…";
}}

function stopRec(){{
  if(recorder&&recorder.state!=="inactive") recorder.stop();
  recording=false;
  btn.textContent="▶ Start Recording";
  btn.classList.remove("rec");
  btn.disabled=true;
  status.textContent="Processing…";
}}

SL_setFrameHeight(document.body.scrollHeight||145);
}})();</script></body></html>"""
    result = components.html(html, height=155, scrolling=False)
    if isinstance(result, dict) and result.get("type") == "rec":
        return result
    return None


_RECORDER_COMPONENT_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "components", "sentence_recorder"
))
_sentence_recorder_func = components.declare_component(
    "sentence_recorder",
    path=_RECORDER_COMPONENT_PATH,
)


def _sentence_recorder_component(seg_key: str, seg_num: int) -> dict | None:
    """
    Sentence-level recorder using a declared Streamlit component.
    Uses getNonBtStream() so Bluetooth headphones stay in A2DP mode.
    Returns {type:'rec', value:<base64>} on new recording, else None.
    """
    result = _sentence_recorder_func(seg_num=seg_num, key=seg_key)
    if isinstance(result, dict) and result.get("type") == "rec":
        return result
    return None


def _sync_shadow_component(audio_b64: str, ts_start: float, ts_end: float,
                            seg_num: int, total_segs: int, take_num: int = 0) -> dict | None:
    """
    Simultaneous playback + recording. Plays the audio segment while recording
    from microphone at the same time — true shadowing mode.
    take_num is embedded in HTML so the iframe resets after each stored take.
    Returns {type:'rec', value:<base64>} on completion, else None.
    """
    duration = ts_end - ts_start
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<!-- take:{take_num} seg:{seg_num} -->
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:transparent;}}
#wrap{{background:#F5F3FF;border:1.5px solid #7C3AED;border-radius:12px;padding:12px 16px;}}
.lbl{{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
      color:#7C3AED;margin-bottom:10px;}}
#btn{{background:#7C3AED;color:#fff;border:none;border-radius:8px;padding:10px 0;
      font-size:.88rem;font-weight:700;cursor:pointer;width:100%;}}
#btn:hover{{background:#6D28D9;}}
#btn.running{{background:#DC2626;cursor:default;animation:pulse 1s infinite;}}
#btn:disabled{{opacity:.4;cursor:not-allowed;animation:none;}}
@keyframes pulse{{0%,100%{{opacity:1;}}50%{{opacity:.7;}}}}
#prog{{height:5px;background:#DDD6FE;border-radius:3px;margin-top:8px;display:none;overflow:hidden;}}
#progfill{{height:100%;width:0%;background:#7C3AED;border-radius:3px;transition:width .1s linear;}}
#status{{font-size:.8rem;margin-top:6px;color:#6B7280;text-align:center;min-height:18px;}}
#err{{font-size:.78rem;margin-top:4px;color:#DC2626;text-align:center;min-height:14px;}}
audio{{margin-top:8px;width:100%;display:none;}}
</style></head><body>
<div id="wrap">
  <div class="lbl">🎤 Sync Shadow · Sentence {seg_num}/{total_segs} · Take {take_num+1}</div>
  <button id="btn" onclick="startShadow()">▶ Play &amp; Shadow Simultaneously</button>
  <div id="prog"><div id="progfill"></div></div>
  <div id="status">Click to hear the sentence and record your shadow at the same time.</div>
  <div id="err"></div>
  <audio id="preview" controls></audio>
</div>
<script>(function(){{
function post(type,extra){{window.parent.postMessage(Object.assign({{isStreamlitMessage:true,type:type}},extra),"*");}}
function SL_setFrameHeight(h){{post("streamlit:setFrameHeight",{{height:h}});}}
function SL_setValue(val){{post("streamlit:setComponentValue",{{value:val,dataType:"json"}});}}
post("streamlit:componentReady",{{apiVersion:1}});
const B64="{audio_b64}";
const TS_START={ts_start};
const DURATION={duration:.3f};
let running=false;
const btn=document.getElementById("btn");
const status=document.getElementById("status");
const err=document.getElementById("err");
const prog=document.getElementById("prog");
const progfill=document.getElementById("progfill");
const preview=document.getElementById("preview");

async function startShadow(){{
  if(running) return;
  err.textContent="";
  status.textContent="Requesting microphone…";
  btn.disabled=true;
  let stream;
  try{{
    stream=await navigator.mediaDevices.getUserMedia({{
      audio:{{
        echoCancellation:false,
        noiseSuppression:false,
        autoGainControl:false,
        channelCount:1
      }},
      video:false
    }});
  }}catch(e){{
    btn.disabled=false;
    if(e.name==="NotAllowedError"||e.name==="PermissionDeniedError")
      err.textContent="❌ Microphone denied. Allow it in browser settings and try again.";
    else if(e.name==="NotFoundError")
      err.textContent="❌ No microphone found.";
    else
      err.textContent="❌ Mic error: "+e.message;
    status.textContent="";
    return;
  }}
  status.textContent="Loading audio…";
  try{{
    const bin=atob(B64);
    const buf=new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) buf[i]=bin.charCodeAt(i);
    const AudioCtx=window.AudioContext||window.webkitAudioContext;
    const actx=new AudioCtx();
    const decoded=await new Promise((res,rej)=>actx.decodeAudioData(buf.buffer,res,rej));

    let mimeType="audio/webm;codecs=opus";
    if(!MediaRecorder.isTypeSupported(mimeType)) mimeType="audio/webm";
    if(!MediaRecorder.isTypeSupported(mimeType)) mimeType="";
    const recOpts=mimeType?{{mimeType,audioBitsPerSecond:128000}}:{{}};
    const recorder=new MediaRecorder(stream,recOpts);
    const chunks=[];
    recorder.ondataavailable=e=>{{ if(e.data.size>0) chunks.push(e.data); }};
    recorder.onstop=()=>{{
      const blob=new Blob(chunks,{{type:mimeType||"audio/webm"}});
      preview.src=URL.createObjectURL(blob);
      preview.style.display="block";
      const reader=new FileReader();
      reader.onloadend=()=>{{
        SL_setValue({{type:"rec",value:reader.result.split(",")[1]}});
        status.textContent="✅ Done! Listen to your shadow below.";
        btn.disabled=false;
        btn.textContent="▶ Shadow Again";
        btn.classList.remove("running");
        prog.style.display="none";
        running=false;
      }};
      reader.readAsDataURL(blob);
      stream.getTracks().forEach(t=>t.stop());
    }};

    const source=actx.createBufferSource();
    source.buffer=decoded;
    source.connect(actx.destination);

    recorder.start();
    source.start(0, TS_START, DURATION);
    running=true;
    btn.classList.add("running");
    btn.textContent="🔴 Shadowing…";
    status.textContent="🔴 Audio playing · microphone recording simultaneously…";
    prog.style.display="block";

    const t0=actx.currentTime;
    const iv=setInterval(()=>{{
      const pct=Math.min(100,(actx.currentTime-t0)/DURATION*100);
      progfill.style.width=pct+"%";
      if(pct>=100) clearInterval(iv);
    }},80);

    source.onended=()=>{{
      clearInterval(iv);
      progfill.style.width="100%";
      recorder.stop();
      btn.disabled=true;
      status.textContent="Processing…";
    }};
  }}catch(e){{
    err.textContent="❌ Audio error: "+e.message;
    status.textContent="";
    btn.disabled=false;
    if(stream) stream.getTracks().forEach(t=>t.stop());
    running=false;
  }}
}}
window.startShadow=startShadow;
SL_setFrameHeight(document.body.scrollHeight||185);
}})();</script></body></html>"""
    result = components.html(html, height=195, scrolling=False)
    if isinstance(result, dict) and result.get("type") == "rec":
        return result
    return None


# ══════════════════════════════════════════════════════════════════
# COACH AVATAR — per-phase tips popover
# ══════════════════════════════════════════════════════════════════

_COACH_TIPS = {
    "select": [
        {"icon": "🎯",
         "en": "**Match your level, not your ego.** If you can understand 70–80% on first listen, it's a good fit. Too easy = no growth; too hard = frustration.",
         "zh": "选接近但略超出舒适区的材料。能听懂七八成就合适——太简单没收获，太难只会沮丧。"},
        {"icon": "⏱️",
         "en": "**Shorter is better to start.** 30–60 seconds of dense native speech is plenty for one session.",
         "zh": "篇幅短一点反而更好。30–60秒的真实语速材料，一次练习已经足够。"},
        {"icon": "💡",
         "en": "**Topic familiarity helps.** Familiar topics let you focus on *how* things are said, not just *what*.",
         "zh": "熟悉的话题更有利。当你不需要分心理解内容，才能专注于「怎么说」。"},
        {"icon": "🔁",
         "en": "**Repeat materials.** Coming back to the same passage in a later session is not cheating — it's how fluency builds.",
         "zh": "重复练同一篇没问题。流利度正是在反复中积累的。"},
    ],
    "prepare": [
        {"icon": "📖",
         "en": "**Read for meaning first.** Skim the text silently. If there are words you don't know, look them up now — not during shadowing.",
         "zh": "先默读理解意思。碰到不认识的词，现在查，不要留到跟读时分心。"},
        {"icon": "🔤",
         "en": "**Study the annotations.** The stress marks (●), linking labels (⌢), weak-form labels, and intonation arrows (↘↗) tell you exactly where native speakers compress and connect speech.",
         "zh": "注意语音标注。重音（●）、连读（⌢）、弱读和语调箭头（↘↗）标出了母语者压缩和连接语流的规律。",
         "link_phonology": True},
        {"icon": "🗣️",
         "en": "**Mouth the words quietly.** Before the first listen, read the text aloud softly to yourself — it primes your articulators.",
         "zh": "轻声试读一遍。在听之前先小声念一遍，帮助嘴巴提前热身。"},
        {"icon": "🎵",
         "en": "**Punctuation = rhythm cues.** Commas signal brief pauses; full stops signal falling intonation. These are your shadowing anchors.",
         "zh": "标点是节奏信号。逗号意味着短暂停顿，句号意味着降调——这些都是跟读时的锚点。"},
    ],
    "shadow": [
        {"icon": "⚡",
         "en": "**Stay close, don't stop.** Aim to be less than half a second behind the speaker. If you miss a word, skip it and keep going — momentum matters more than completeness.",
         "zh": "紧跟，别停。目标是落后说话者不超过半秒。漏了一个词就跳过——保持节奏比字字不漏更重要。"},
        {"icon": "🎵",
         "en": "**Shadow the music, not just the words.** Mimic the rises and falls in pitch, the speed changes, the pauses. The melody carries as much meaning as the words.",
         "zh": "跟读「音乐」，不只是文字。模仿语调起伏、速度变化和停顿——旋律和词语同样重要。"},
        {"icon": "😌",
         "en": "**It's okay to sound strange.** Your voice will feel unfamiliar when you push toward native-speaker rhythm. That discomfort means you're working outside your current habits.",
         "zh": "听起来奇怪是正常的。当你开始接近母语者节奏时，自己声音会觉得陌生——这种不适感说明你在突破习惯。"},
        {"icon": "🔂",
         "en": "**Repeat difficult sentences.** If a sentence felt wrong, replay it 2–3 times back to back before moving on.",
         "zh": "难的句子多来几遍。一个句子觉得没跟好，就连续重复2–3次再继续。"},
    ],
    "compare": [
        {"icon": "🥁",
         "en": "**Listen for rhythm first, sounds second.** Did your stress land on the same syllables? Did your pauses match? Rhythm differences are usually bigger than vowel differences.",
         "zh": "先听节奏，再听音。重音落在相同的音节上了吗？停顿一致吗？节奏上的差距往往比元音差距更大。"},
        {"icon": "🔍",
         "en": "**Find one moment to be curious about.** You don't need to fix everything — find the single most interesting gap between your voice and the original.",
         "zh": "只找一个值得好奇的地方。不必面面俱到——找出你和原声之间最有趣的那个差距就够了。"},
        {"icon": "🙂",
         "en": "**Your accent is not the problem.** You're training your ear to perceive fast speech — the voice you use to do that is yours.",
         "zh": "你的口音不是问题。目标不是听起来像说话者，而是训练耳朵感知快速语流。"},
        {"icon": "⏯️",
         "en": "**Use the timestamps.** If a specific moment surprised you, replay just that segment. Precision beats re-listening to the whole thing.",
         "zh": "用时间轴定位。精准回听比整段重来效率更高。"},
    ],
    "capture": [
        {"icon": "👁️",
         "en": "**A notice is an observation, not a mistake.** Write down what you *noticed*, not what you think you *should* have done.",
         "zh": "发现是观察，不是错误。记录你注意到的，而不是你认为应该做到的。"},
        {"icon": "📌",
         "en": "**Be specific.** Name the word, the feature, the moment. The more precise your notice, the more useful it is next session.",
         "zh": "要具体。写清楚是哪个词、哪个语音现象、哪个时刻——越精准的记录，下次练习越有参考价值。"},
        {"icon": "🏷️",
         "en": "**Tag it.** Using consistent tags (stress / linking / weak form / intonation) lets you see patterns across sessions over time.",
         "zh": "打好标签。用固定的分类来标记，方便日后发现跨课次的规律。"},
        {"icon": "🎯",
         "en": "**One session, one pattern.** If you notice the same thing three times in one session, write it once, clearly.",
         "zh": "一次练习，找一个规律。同一个问题出现了三次，清晰地写一条就够了。"},
    ],
}


def _coach_avatar(phase_key: str):
    """💬 coach tip button, right-aligned, opens a popover with phase tips."""
    tips = _COACH_TIPS.get(phase_key, [])
    if not tips:
        return
    _, btn_col = st.columns([14, 1])
    with btn_col:
        with st.popover("💬", use_container_width=True):
            st.markdown(
                '<div style="font-size:.82rem;font-weight:700;color:#374151;margin-bottom:12px;">'
                '💬 Coach tips / 练习提示</div>',
                unsafe_allow_html=True
            )
            for i, tip in enumerate(tips):
                st.markdown(f'{tip["icon"]} {tip["en"]}')
                st.caption(tip["zh"])
                if tip.get("link_phonology"):
                    if st.button(
                        "📖 Learn annotation symbols in Phonology Guide →",
                        key=f"tip_phon_{phase_key}_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.page = "phonology"
                        st.rerun()
                if i < len(tips) - 1:
                    st.markdown("---")


# ══════════════════════════════════════════════════════════════════
# PHASE 1 — SELECT
# ══════════════════════════════════════════════════════════════════

def _phase_select():
    st.title("🎧 ShadowingLab")
    st.markdown(
        '<p class="muted" style="margin-top:-8px;margin-bottom:24px;">'
        'A structured shadowing tool for Chinese EFL learners. '
        'Each session takes 20–30 minutes and follows a research-backed five-phase process.'
        '</p>', unsafe_allow_html=True
    )

    # previous sessions callout
    history = st.session_state.session_history
    if history:
        last = history[-1]
        st.markdown(f"""
        <div class="sl-card sl-card-teal" style="margin-bottom:20px;">
            <div class="label-xs" style="margin-bottom:6px;">Last session</div>
            <div style="font-weight:600;color:var(--color-primary);">{last['material_title']}</div>
            <div class="muted">{last['date']} &nbsp;·&nbsp;
            {last['notices']} notice{"s" if last['notices']!=1 else ""} recorded</div>
        </div>
        """, unsafe_allow_html=True)

    _coach_avatar("select")
    st.markdown("### Choose a material / 选择练习材料")

    for mat in get_all_materials():
        prev         = [h for h in history if h["material_id"] == mat["id"]]
        prev_notices = sum(h["notices"] for h in prev)
        diff_colors  = {
            "beginner":     ("#065F46", "#ECFDF5"),
            "intermediate": ("#92400E", "#FFFBEB"),
            "advanced":     ("#9F1239", "#FFF1F2"),
        }
        dc, db = diff_colors.get(mat["difficulty"], ("#374151", "#F3F4F6"))
        mins   = mat["duration_sec"] // 60
        n_segs = len(get_segments(mat))
        kw     = ", ".join(mat["keywords"])
        diff   = mat["difficulty"].title()
        title  = mat["title"]

        with st.container():
            st.markdown(
                f'<div style="border:1px solid #E5E7EB;border-radius:12px;'
                f'padding:14px 16px;margin-bottom:6px;">' +
                f'<div style="font-size:1.05rem;font-weight:700;color:#1A3A5C;margin-bottom:8px;">{title}</div>' +
                f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">' +
                f'<span style="background:{db};color:{dc};border-radius:99px;padding:2px 10px;font-size:.75rem;font-weight:700;">{diff}</span>' +
                f'<span style="font-size:.82rem;color:#6B7280;">⏱ ~{mins} min</span>' +
                f'<span style="font-size:.82rem;color:#6B7280;">{n_segs} sentences</span>' +
                (f'<span style="font-size:.78rem;color:#6B7280;">{len(prev)} prev session{"s" if len(prev)!=1 else ""}</span>' if prev else '') +
                (f'<span style="font-size:.78rem;color:#0F6E56;">{prev_notices} notices</span>' if prev_notices else '') +
                f'</div>' +
                f'<div style="font-size:.78rem;color:#9CA3AF;">Keywords: {kw}</div>' +
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button("Start session →", key="start_" + mat["id"], type="primary"):
                start_new_session(mat)
                st.rerun()

    st.markdown("---")
    st.markdown(
        '<div class="caption-note">'
        '📁 <strong>Upload your own material</strong> — coming in a future version. '
        'When enabled, Whisper will automatically annotate stress, linking, and weak forms '
        'in any MP3 you upload.'
        '</div>', unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════
# PHASE 2 — PREPARE
# ══════════════════════════════════════════════════════════════════

def _phase_prepare():
    mat  = st.session_state.active_material
    segs = get_segments(mat)

    _phase_header(2, "Prepare", "准备",
                  "#0EA5E9", "#E0F2FE",
                  "Listen once while reading. Mark any words you don't know.")
    _coach_avatar("prepare")

    col_left, col_right = st.columns([1, 1.4])

    with col_left:
        st.markdown("**🔊 Listen & Read / 听读**")
        st.markdown(
            '<div class="caption-note">'
            'Play the audio and follow the text on the right. '
            "Don't shadow yet — just listen and read together.<br>"
            '播放音频，跟随右侧文本阅读。此阶段不要跟读——只是同时听和读。'
            '</div>', unsafe_allow_html=True
        )

        audio_b64 = _load_audio_b64(mat["audio_path"])
        if audio_b64:
            st.audio(base64.b64decode(audio_b64), format="audio/mp3")
        else:
            st.info("Audio file not found at: " + mat["audio_path"])
            st.caption("Place your MP3 at the path above and reload.")

        st.markdown("---")
        st.markdown("**📚 Vocabulary / 生词本**")
        st.caption("Tap any word in the text you don't know, or add it here.")
        nw = st.text_input("Add a word", placeholder="e.g. prodigy",
                           label_visibility="collapsed", key="prep_vocab_in")
        if st.button("➕ Add", key="prep_vocab_add"):
            if nw and nw not in st.session_state.vocabulary:
                st.session_state.vocabulary.append(nw)
                st.success(f"Added '{nw}'")
            elif nw:
                st.info("Already in your vocabulary list.")

        if st.session_state.vocabulary:
            chips = "".join(
                f'<span class="tag-chip" style="background:#DBEAFE;color:#1D4ED8;'
                f'border:1px solid #93C5FD;">{w}</span>'
                for w in st.session_state.vocabulary
            )
            st.markdown(chips, unsafe_allow_html=True)

    with col_right:
        st.markdown("**📄 Full Text / 完整文本**")
        st.markdown(
            '<div style="display:flex;gap:14px;flex-wrap:wrap;font-size:.72rem;'
            'color:#6B7280;margin-bottom:10px;line-height:1.8;">'
            '<span><span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            'background:#0C447C;vertical-align:middle;margin-right:3px;"></span>stress 重音</span>'
            '<span style="color:#854F0B;">★ nuclear 核心重音</span>'
            '<span style="color:#993C1D;">↘ fall 降调</span>'
            '<span style="color:#0F6E56;">↗ rise 升调</span>'
            '<span style="background:#DBEAFE;color:#185FA5;border-radius:3px;'
            'padding:1px 4px;">⌢ link 连读</span>'
            '<span style="background:#F1EFE8;color:#5F5E5A;border-radius:3px;'
            'padding:1px 4px;font-style:italic;">wk weak 弱读</span>'
            '<span style="color:#9CA3AF;font-size:.68rem;">'
            '↑ suprasegmental 超音段 &nbsp;|&nbsp; ↓ segmental 音段</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div style="font-size:.75rem;color:#6B7280;background:#FFF7ED;'
            'border-left:3px solid #F59E0B;border-radius:4px;'
            'padding:6px 10px;margin-bottom:10px;">'
            '💡 Study these marks now — Phase 3 shows plain text by default so you focus on listening.<br>'
            '现在熟悉这些标注，第三阶段默认隐藏注释，让你专注于听觉。'
            '</div>',
            unsafe_allow_html=True
        )
        for seg in segs:
            ann_html = _render_word_annotations(seg)
            st.markdown(ann_html, unsafe_allow_html=True)

    st.markdown("---")
    col_nav1, col_nav2, _ = st.columns([1, 1, 3])
    with col_nav1:
        if st.button("← Back to materials", key="prep_back"):
            st.session_state.session_phase = "select"
            st.rerun()
    with col_nav2:
        if st.button("Ready — Start Shadowing →", type="primary", key="prep_next"):
            advance_phase("shadow")
            st.rerun()



# ══════════════════════════════════════════════════════════════════
# PHASE 3 — SHADOW  (v3: text-on-top, audio-bar-bottom layout)
# ══════════════════════════════════════════════════════════════════


def _audio_player_component(audio_b64, timestamps, key):
    import json as _j
    ts_json = _j.dumps(timestamps)
    n = len(timestamps)
    shadow_btn = (
        "<button class='mb on' id='mshadow' "
        "onclick='setMode(\"shadow\")'>🎤 Shadow mode"
        "<br><span style='font-weight:400;font-size:.73rem;'>"
        "Auto-pause · 逐句暂停</span></button>"
    )
    flow_btn = (
        "<button class='mb' id='mflow' "
        "onclick='setMode(\"flow\")'>🎵 Flow mode"
        "<br><span style='font-weight:400;font-size:.73rem;'>"
        "Continuous · 连续播放</span></button>"
    )
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:transparent;}}
#wrap{{background:#F0F4FF;border:2px solid #2563EB;border-radius:14px;padding:16px 18px;}}
.lbl{{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#2563EB;margin-bottom:10px;}}
audio{{display:none;}}
#waveWrap{{position:relative;height:56px;background:#fff;border-radius:8px;
           border:0.5px solid #BFDBFE;overflow:hidden;margin-bottom:6px;cursor:pointer;}}
#waveCanvas{{position:absolute;top:0;left:0;width:100%;height:100%;}}
#waveLoading{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
              font-size:.72rem;color:#93C5FD;}}
.seg-labels{{display:flex;margin-bottom:8px;}}
.sl{{font-size:10px;font-weight:500;text-align:center;padding:2px 0;
     border-right:1px solid #BFDBFE;color:#9CA3AF;cursor:pointer;flex-shrink:0;}}
.sl:last-child{{border-right:none;}}
.sl.active{{color:#2563EB;font-weight:700;background:#DBEAFE;border-radius:4px;}}
.si{{font-size:.78rem;color:#3B82F6;margin-bottom:8px;min-height:16px;}}
.nr{{display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;}}
.nb{{background:#fff;border:1.5px solid #BFDBFE;border-radius:8px;padding:6px 14px;
     font-size:.85rem;font-weight:700;cursor:pointer;color:#2563EB;}}
.nb:hover{{background:#DBEAFE;}}.nb:disabled{{opacity:.35;cursor:not-allowed;}}
.sb{{background:#EFF6FF;border:1px solid #BFDBFE;border-radius:6px;padding:4px 10px;
     font-size:.78rem;font-weight:700;cursor:pointer;color:#3B82F6;}}
.sb.on{{background:#2563EB;color:#fff;border-color:#2563EB;}}
.mr{{display:flex;gap:8px;margin-top:6px;}}
.mb{{flex:1;padding:7px 8px;border-radius:10px;border:1.5px solid #E5E7EB;font-size:.8rem;
     font-weight:700;cursor:pointer;text-align:center;background:#fff;color:#6B7280;}}
.mb.on{{border-color:#2563EB;color:#2563EB;background:#EFF6FF;}}
</style></head><body>
<div id="wrap">
<div class="lbl">🔊 Original Audio / 原音</div>
<audio id="aud" preload="auto"><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>
<div id="waveWrap" onclick="waveClick(event)">
  <canvas id="waveCanvas"></canvas>
  <div id="waveLoading">Loading waveform…</div>
</div>
<div class="seg-labels" id="segLabels"></div>
<div class="si" id="si">Sentence — / {n}</div>
<div class="nr">
<button class="nb" id="bp" onclick="prevSeg()">⏮ Prev</button>
<button class="nb" id="bpl" onclick="togglePlay()">▶ Play</button>
<button class="nb" onclick="replaySeg()">↺ Replay</button>
<button class="nb" id="bn" onclick="nextSeg()">⏭ Next</button>
<span style="flex:1"></span>
<button class="sb" onclick="setSpd(0.75)">0.75x</button>
<button class="sb on" onclick="setSpd(1.0)">1.0x</button>
<button class="sb" onclick="setSpd(1.25)">1.25x</button>
</div>
<div class="mr">{shadow_btn}{flow_btn}</div>
</div>
<script>(function(){{
function post(type,extra){{window.parent.postMessage(Object.assign({{isStreamlitMessage:true,type:type}},extra),"*");}}
function SL_setFrameHeight(h){{post("streamlit:setFrameHeight",{{height:h}});}}
function SL_setValue(val){{post("streamlit:setComponentValue",{{value:val,dataType:"json"}});}}
post("streamlit:componentReady",{{apiVersion:1}});
const SK="{key}";
const ts={ts_json};
const aud=document.getElementById("aud");
const canvas=document.getElementById("waveCanvas");
const ctx=canvas.getContext("2d");
let waveData=null;
let curSeg=-1,lastSeg=-1,p4s=false;
const saved=JSON.parse(sessionStorage.getItem(SK)||"{{}}");
let playMode=saved.mode||"shadow";
let savedTime=saved.time||0;
let savedSpd=saved.spd||1.0;
document.getElementById("mshadow").classList.toggle("on",playMode==="shadow");
document.getElementById("mflow").classList.toggle("on",playMode==="flow");

// ── Build segment label bar ──────────────────────────────────────
function buildLabels(){{
  const el=document.getElementById("segLabels");
  el.innerHTML="";
  const dur=aud.duration||1;
  ts.forEach(function(t,i){{
    const d=document.createElement("div");
    d.className="sl"+(i===curSeg?" active":"");
    d.textContent="S"+(i+1);
    d.style.width=((t.end-t.start)/dur*100)+"%";
    d.onclick=(function(s){{return function(e){{e.stopPropagation();jumpTo(s);}};}})(i);
    el.appendChild(d);
  }});
}}

// ── Decode audio and extract waveform via Web Audio API ──────────
function decodeWaveform(){{
  try{{
    const b64="{audio_b64}";
    const bin=atob(b64);
    const buf=new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++)buf[i]=bin.charCodeAt(i);
    const AudioCtx=window.AudioContext||window.webkitAudioContext;
    if(!AudioCtx){{ drawFallbackWave(); return; }}
    const actx=new AudioCtx();
    actx.decodeAudioData(buf.buffer,function(decoded){{
      const raw=decoded.getChannelData(0);
      const samples=512;
      const blockSize=Math.floor(raw.length/samples);
      waveData=new Float32Array(samples);
      for(let i=0;i<samples;i++){{
        let max=0;
        for(let j=0;j<blockSize;j++){{
          const v=Math.abs(raw[i*blockSize+j]);
          if(v>max)max=v;
        }}
        waveData[i]=max;
      }}
      document.getElementById("waveLoading").style.display="none";
      drawWave(0,1);
    }},function(){{ drawFallbackWave(); }});
  }}catch(e){{ drawFallbackWave(); }}
}}

function drawFallbackWave(){{
  // Pseudo-random but stable waveform as fallback
  const samples=512;
  waveData=new Float32Array(samples);
  for(let i=0;i<samples;i++){{
    waveData[i]=Math.max(0.05,Math.abs(Math.sin(i*0.35)*Math.sin(i*0.12+1.1)*0.8+0.1));
  }}
  document.getElementById("waveLoading").style.display="none";
  drawWave(0,1);
}}

function drawWave(playPct,dur){{
  if(!waveData)return;
  const W=canvas.offsetWidth,H=canvas.offsetHeight;
  if(W===0||H===0)return;
  canvas.width=W;canvas.height=H;
  ctx.clearRect(0,0,W,H);

  const barW=2,gap=1,step=barW+gap;
  const cols=Math.floor(W/step);

  // draw bars
  for(let i=0;i<cols;i++){{
    const pct=i/cols;
    const si=Math.floor(pct*waveData.length);
    const amp=waveData[si]||0.05;
    const h=Math.max(3,amp*H*0.9);
    const y=(H-h)/2;
    const x=i*step;

    // which segment is this bar in?
    const t=pct*(aud.duration||1);
    let segIdx=-1;
    for(let s=0;s<ts.length;s++)if(t>=ts[s].start&&t<ts[s].end){{segIdx=s;break;}}

    if(pct<=playPct){{
      // played: solid blue
      ctx.fillStyle=segIdx===curSeg?"#2563EB":"#60A5FA";
    }}else{{
      // unplayed: light
      ctx.fillStyle=segIdx===curSeg?"#93C5FD":"#DBEAFE";
    }}
    ctx.beginPath();
    ctx.roundRect(x,y,barW,h,1);
    ctx.fill();
  }}

  // segment divider lines
  if(aud.duration){{
    ts.forEach(function(t,i){{
      if(i===0)return;
      const x=t.start/aud.duration*W;
      ctx.strokeStyle="rgba(37,99,235,0.4)";
      ctx.lineWidth=1.5;
      ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.moveTo(x,3);ctx.lineTo(x,H-3);ctx.stroke();
      ctx.setLineDash([]);
    }});
  }}

  // playhead
  const px=playPct*W;
  ctx.strokeStyle="#1D4ED8";
  ctx.lineWidth=2;
  ctx.setLineDash([]);
  ctx.beginPath();ctx.moveTo(px,0);ctx.lineTo(px,H);ctx.stroke();
}}

// ── Audio events ─────────────────────────────────────────────────
aud.addEventListener("loadedmetadata",function(){{
  aud.playbackRate=savedSpd;
  buildLabels();
  decodeWaveform();
  if(savedTime>0&&savedTime<aud.duration-0.5){{
    aud.currentTime=savedTime;
    const seg=getseg(savedTime);
    document.getElementById("si").textContent="Sentence "+(seg+1)+" / {n}";
    curSeg=seg;lastSeg=seg;
    buildLabels();
    document.getElementById("bp").disabled=(seg===0);
    document.getElementById("bn").disabled=(seg===ts.length-1);
  }}
  document.querySelectorAll(".sb").forEach(b=>{{
    if(parseFloat(b.textContent)===savedSpd)b.classList.add("on");
    else b.classList.remove("on");
  }});
}});

function saveState(){{sessionStorage.setItem(SK,JSON.stringify({{time:aud.currentTime,mode:playMode,spd:aud.playbackRate}}));}}
function getseg(t){{for(let i=0;i<ts.length;i++)if(t>=ts[i].start&&t<ts[i].end)return i;if(t>=ts[ts.length-1].end)return ts.length-1;return 0;}}
function setSpd(s){{aud.playbackRate=s;document.querySelectorAll(".sb").forEach(b=>b.classList.remove("on"));document.querySelectorAll(".sb").forEach(b=>{{if(b.textContent.trim()===s+"x")b.classList.add("on");}});saveState();}}
window.setSpd=setSpd;
function setMode(m){{playMode=m;document.getElementById("mshadow").classList.toggle("on",m==="shadow");document.getElementById("mflow").classList.toggle("on",m==="flow");saveState();SL_setValue({{type:"mode",value:m}});}}
window.setMode=setMode;
function togglePlay(){{if(aud.paused){{aud.play().then(()=>{{document.getElementById("bpl").textContent="⏸ Pause";}}).catch(()=>{{}});}}else{{aud.pause();document.getElementById("bpl").textContent="▶ Play";}}}}
window.togglePlay=togglePlay;
function jumpTo(i){{if(i<0||i>=ts.length)return;aud.currentTime=ts[i].start+0.05;p4s=false;saveState();if(aud.paused)aud.play().then(()=>{{document.getElementById("bpl").textContent="⏸ Pause";}}).catch(()=>{{}});}}
function prevSeg(){{jumpTo(curSeg>0?curSeg-1:0);}}
function nextSeg(){{jumpTo(curSeg<ts.length-1?curSeg+1:ts.length-1);}}
function replaySeg(){{jumpTo(curSeg>=0?curSeg:0);}}
window.prevSeg=prevSeg;window.nextSeg=nextSeg;window.replaySeg=replaySeg;
function waveClick(e){{
  const r=document.getElementById("waveWrap").getBoundingClientRect();
  aud.currentTime=((e.clientX-r.left)/r.width)*(aud.duration||1);
  saveState();
}}
window.waveClick=waveClick;

// ── Main loop ────────────────────────────────────────────────────
setInterval(function(){{
  if(!aud.duration)return;
  const t=aud.currentTime,dur=aud.duration;
  const playPct=t/dur;
  drawWave(playPct,dur);
  const seg=getseg(t);
  if(seg!==lastSeg){{
    lastSeg=seg;curSeg=seg;
    document.getElementById("si").textContent="Sentence "+(seg+1)+" / {n}";
    document.getElementById("bp").disabled=(seg===0);
    document.getElementById("bn").disabled=(seg===ts.length-1);
    buildLabels();
    SL_setValue({{type:"seg",value:seg}});
    saveState();
  }}
  if(playMode==="shadow"&&!aud.paused&&!p4s&&seg>=0){{
    if(ts[seg].end-t<0.12){{aud.pause();p4s=true;document.getElementById("bpl").textContent="▶ Play";saveState();}}
  }}
  if(p4s&&aud.paused)p4s=false;
  if(!aud.paused)document.getElementById("bpl").textContent="⏸ Pause";
  else document.getElementById("bpl").textContent="▶ Play";
}},100);
aud.addEventListener("ended",function(){{
  drawWave(1,aud.duration);
  document.getElementById("bpl").textContent="▶ Play";
  saveState();
}});
SL_setFrameHeight(document.body.scrollHeight||310);
}})();</script></body></html>"""
    result = components.html(html, height=320, scrolling=False)
    if isinstance(result, dict) and result.get("type") in ("seg", "mode"):
        return result
    return None

def _render_word_annotations(seg: dict, show_annotations: bool = True) -> str:
    """
    Render a sentence as a word-by-word annotation table using the new
    rich annotation system: stress dots, weak labels, linking arrows,
    intonation arrows, nuclear star, pause marks.
    Returns an HTML string.
    """
    if not show_annotations:
        return f'<span style="font-size:.9rem;line-height:1.8;">{seg["text"]}</span>'

    words   = seg.get("words", [])
    pauses  = set(seg.get("pauses", []))
    final   = seg.get("intonation", "fall")

    if not words:
        return f'<span style="font-size:.9rem;">{seg["text"]}</span>'

    cells = []
    for i, wd in enumerate(words):
        anns      = wd.get("anns", [])
        ann_types = {a["type"] for a in anns}
        is_last   = (i == len(words) - 1)

        # ── above-word (suprasegmental): stress, nuclear, intonation ─
        above_parts = []
        if "nuclear" in ann_types:
            above_parts.append('<span style="font-size:11px;color:#854F0B;line-height:1;">&#9733;</span>')
        elif "stress" in ann_types:
            above_parts.append('<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#0C447C;"></span>')
        else:
            if not ("weak" in ann_types or "link" in ann_types):
                above_parts.append('<span style="display:inline-block;width:4px;height:4px;border-radius:50%;background:#B5D4F4;"></span>')
        # intonation is suprasegmental → above
        arrows = {"fall": "&#8600;", "rise": "&#8599;", "fall_rise": "&#8599;&#8600;"}
        colors = {"fall": "#993C1D", "rise": "#0F6E56", "fall_rise": "#534AB7"}
        if is_last:
            arr = arrows.get(final, "&#8600;")
            col = colors.get(final, "#993C1D")
            above_parts.append(f'<span style="font-size:12px;color:{col};line-height:1;">{arr}</span>')
        elif "fall" in ann_types:
            above_parts.append('<span style="font-size:12px;color:#993C1D;line-height:1;">&#8600;</span>')
        elif "rise" in ann_types:
            above_parts.append('<span style="font-size:12px;color:#0F6E56;line-height:1;">&#8599;</span>')
        elif "fall_rise" in ann_types:
            above_parts.append('<span style="font-size:11px;color:#534AB7;line-height:1;">&#8599;&#8600;</span>')
        above = "".join(above_parts)

        # ── word styling ──────────────────────────────────────────
        if "stress" in ann_types or "nuclear" in ann_types:
            word_style = 'font-weight:600;color:#0C447C;font-size:.9rem;'
        elif "weak" in ann_types:
            word_style = 'color:#888780;font-size:.82rem;'
        else:
            word_style = 'font-size:.88rem;color:#374151;'

        # ── below-word (segmental): linking, weak forms only ──────
        below = ""
        if "link" in ann_types:
            lbl = next((a.get("label", "⌢") for a in anns if a["type"] == "link"), "⌢")
            below = f'<span style="font-size:9px;background:#DBEAFE;color:#185FA5;border-radius:3px;padding:1px 3px;">{lbl}</span>'
        elif "weak" in ann_types:
            lbl = next((a.get("label", "wk") for a in anns if a["type"] == "weak"), "wk")
            below = f'<span style="font-size:9px;background:#F1EFE8;color:#5F5E5A;border-radius:3px;padding:1px 3px;font-style:italic;">{lbl}</span>'

        cell = (
            f'<td style="text-align:center;padding:0 3px;vertical-align:middle;">'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:1px;">'
            f'<div style="height:16px;display:flex;align-items:flex-end;justify-content:center;">{above}</div>'
            f'<div style="{word_style}white-space:nowrap;">{wd["w"]}</div>'
            f'<div style="height:16px;display:flex;align-items:flex-start;justify-content:center;">{below}</div>'
            f'</div></td>'
        )
        cells.append(cell)

        # pause mark after this word
        if i in pauses:
            cells.append(
                '<td style="padding:0 2px;vertical-align:middle;">'
                '<div style="display:flex;flex-direction:column;align-items:center;gap:1px;">'
                '<div style="height:16px;"></div>'
                '<div style="font-size:13px;color:#A32D2D;font-weight:700;line-height:1;">&vert;</div>'
                '<div style="height:16px;"></div>'
                '</div></td>'
            )

    return (
        '<div style="overflow-x:auto;">'
        '<table style="border-collapse:collapse;white-space:nowrap;">'
        '<tr>' + ''.join(cells) + '</tr>'
        '</table></div>'
    )


def _mic_prewarm_component():
    """
    Silently request mic access as soon as Phase 3 loads.
    Keeps the stream alive so Bluetooth devices stay in HFP mode,
    eliminating the 1-2 s reconnection delay when the user hits Record.
    """
    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;font-family:system-ui,sans-serif;background:transparent;}
#s{font-size:.74rem;padding:3px 10px;border-radius:4px;display:inline-block;
   background:#F0FDF4;border:1px solid #BBF7D0;color:#065F46;}
</style></head><body>
<span id="s">⏳ Connecting microphone…</span>
<script>
(async function(){
  var el=document.getElementById("s");
  try{
    var stream=await navigator.mediaDevices.getUserMedia({audio:true,video:false});
    var track=stream.getAudioTracks()[0];
    el.textContent="🎤 Ready · "+(track?track.label:"Microphone");
    window._prewarmStream=stream; // keep alive → no re-connection delay on Record
  }catch(e){
    el.style.background="#FEF2F2";el.style.borderColor="#FECACA";el.style.color="#991B1B";
    el.textContent=(e.name==="NotAllowedError")
      ?"⚠️ Mic blocked — allow microphone in browser settings / 请在浏览器设置中允许麦克风"
      :"⚠️ Mic unavailable: "+e.message;
  }
})();
</script></body></html>"""
    import streamlit.components.v1 as _c
    _c.html(html, height=30, scrolling=False)


def _phase3_guide():
    """Compact always-visible instruction card for Phase 3."""
    st.markdown(
        '<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;'
        'padding:10px 16px;margin:6px 0 10px;font-size:.82rem;color:#374151;line-height:1.9;">'

        '<strong>🎧 Headphones recommended / 建议戴耳机</strong>'
        '<span style="color:#6B7280;"> — '
        'Bluetooth adds 1–2 s delay; wait for <em>Mic Ready</em> above before recording. '
        '蓝牙有1–2秒延迟，等麦克风显示Ready后再点录音。'
        '</span><br>'

        '<strong>🔤 Shadow mode</strong>'
        '<span style="color:#6B7280;">: audio auto-pauses after each sentence → '
        'shadow <em>as the audio plays</em>, not after it stops. '
        '音频每句结束后自动暂停，跟读时与音频同步，不是等音频停了才说。</span><br>'

        '<strong>🎵 Flow mode</strong>'
        '<span style="color:#6B7280;">: continuous playback — good for listening flow, '
        'not recommended for recording. 连续播放，适合纯听练习，不建议用于录音。</span><br>'

        '<strong>Step 1</strong>'
        '<span style="color:#6B7280;"> sentence-by-sentence practice → </span>'
        '<strong>Step 2</strong>'
        '<span style="color:#6B7280;"> full passage with text hidden.</span>'

        '</div>',
        unsafe_allow_html=True,
    )


def _phase_shadow():
    mat  = st.session_state.active_material
    segs = get_segments(mat)
    n    = len(segs)
    cur  = st.session_state.current_segment

    if "saved_sentences" not in st.session_state:
        st.session_state.saved_sentences = set()
    if "shadow_step" not in st.session_state:
        st.session_state.shadow_step = 1

    _phase_header(3, "Shadow", "跟读",
                  "#7C3AED", "#F5F3FF",
                  "Shadow each sentence · 逐句跟读，再整段挑战")
    _coach_avatar("shadow")
    _mic_prewarm_component()
    _phase3_guide()

    step = st.session_state.shadow_step
    _sc1, _sc2 = st.columns(2)
    with _sc1:
        if st.button("🔤 Step 1 · Sentence by sentence / 逐句",
                     type="primary" if step == 1 else "secondary",
                     use_container_width=True, key="shadow_step1_btn"):
            st.session_state.shadow_step = 1; st.rerun()
    with _sc2:
        if st.button("📄 Step 2 · Full passage / 整段",
                     type="primary" if step == 2 else "secondary",
                     use_container_width=True, key="shadow_step2_btn"):
            st.session_state.shadow_step = 2; st.rerun()
    st.markdown("")

    if step == 1:

        # ── timestamps ──────────────────────────────────────────────
        audio_b64 = _load_audio_b64(mat["audio_path"])
        cache_key = "whisper_ts_" + mat["id"]
        if cache_key not in st.session_state and is_ai_available():
            with st.spinner("Analysing audio with Whisper… / 正在分析音频时间戳…"):
                timestamps = get_timestamps_for_material(mat)
        else:
            timestamps = get_timestamps_for_material(mat)

        # annotation toggle
        show_ann = st.session_state.get("shadow_show_ann", False)
        if st.button(
            "🏷 Hide annotations / 隐藏注释" if show_ann else "🏷 Show annotations / 显示注释",
            key="shadow_ann_toggle",
        ):
            st.session_state.shadow_show_ann = not show_ann; st.rerun()

        # ── TEXT PANEL ───────────────────────────────────────────────
        rows_html = []
        for i, seg_i in enumerate(segs):
            is_cur   = (i == cur)
            is_done  = (i in st.session_state.visited_segments)
            is_saved = (i in st.session_state.saved_sentences)
            ann_html = _render_word_annotations(seg_i, show_annotations=show_ann)
            star_c   = "#F59E0B" if is_saved else "#CBD5E1"
            star_ch  = "&#9733;" if is_saved else "&#9734;"
            star_span = (
                f'<span id="star{i}" onclick="toggleStar({i})" ' +
                f'style="cursor:pointer;font-size:14px;color:{star_c};' +
                'margin-right:5px;user-select:none;">' +
                f'{star_ch}</span>'
            )

            if is_cur:
                rows_html.append(
                    f'<div id="s{i}" style="scroll-margin-top:4px;background:#F9FAFB;' +
                    'border-left:2px solid #D1D5DB;border-radius:0 8px 8px 0;' +
                    'padding:8px 12px;margin-bottom:5px;">' +
                    f'<div style="display:flex;align-items:center;margin-bottom:4px;">' +
                    star_span +
                    f'<span style="font-size:10px;color:#9CA3AF;">{i+1}</span>' +
                    '</div>' + ann_html + '</div>'
                )
            elif is_done:
                rows_html.append(
                    f'<div id="s{i}" style="scroll-margin-top:4px;background:#F0FDF4;' +
                    'border-left:2px solid #10B981;border-radius:0 8px 8px 0;' +
                    'padding:8px 12px;margin-bottom:5px;">' +
                    f'<div style="display:flex;align-items:center;margin-bottom:3px;">' +
                    star_span +
                    f'<span style="font-size:10px;font-weight:600;color:#10B981;">&#10003; {i+1}</span>' +
                    '</div>' + ann_html + '</div>'
                )
            else:
                rows_html.append(
                    f'<div id="s{i}" style="scroll-margin-top:4px;' +
                    'border-left:2px solid #E5E7EB;border-radius:0 8px 8px 0;' +
                    'padding:8px 12px;margin-bottom:5px;">' +
                    f'<div style="display:flex;align-items:center;margin-bottom:3px;">' +
                    star_span +
                    f'<span style="font-size:10px;color:#9CA3AF;">{i+1}</span>' +
                    '</div>' + ann_html + '</div>'
                )

        saved_json = str(list(st.session_state.saved_sentences))
        inner   = "".join(rows_html)
        panel_h = 100
        panel_html = (
            "<!DOCTYPE html><html><head><style>"
            "html,body{margin:0;padding:0;overflow:hidden;font-family:system-ui,sans-serif;}"
            f"#p{{height:{panel_h}px;overflow-y:scroll;padding:6px 8px 4px;box-sizing:border-box;}}"
            "table{border-collapse:collapse;}td{padding:0;vertical-align:middle;}"
            "</style></head><body>"
            f"<div id='p'>{inner}</div>"
            "<script>"
            "function _post(t,x){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:t},x),'*');}"
            "_post('streamlit:componentReady',{apiVersion:1});"
            f"var saved=new Set({saved_json});"
            "function toggleStar(i){"
            "  var el=document.getElementById('star'+i);"
            "  if(saved.has(i)){saved.delete(i);el.style.color='#CBD5E1';el.innerHTML='&#9734';}"
            "  else{saved.add(i);el.style.color='#F59E0B';el.innerHTML='&#9733';}"
            "  _post('streamlit:setComponentValue',{value:{type:'bk',value:i},dataType:'json'});"
            "}"
            "setTimeout(function(){"
            f"  var e=document.getElementById('s{cur}'),p=document.getElementById('p');"
            "  if(e&&p)p.scrollTop=Math.max(0,e.offsetTop-20);"
            "},80);"
            "</script>"
            "</body></html>"
        )
        panel_result = components.html(panel_html, height=panel_h + 4, scrolling=False)
        if isinstance(panel_result, dict) and panel_result.get("type") == "bk":
            idx = int(panel_result["value"])
            if idx in st.session_state.saved_sentences:
                st.session_state.saved_sentences.discard(idx)
            else:
                st.session_state.saved_sentences.add(idx)
            st.rerun()

                # ── ROW 2: audio player ──────────────────────────────────────
        if audio_b64:
            player_result = _audio_player_component(
                audio_b64, timestamps, key="player_" + mat["id"]
            )
            if player_result:
                if player_result["type"] == "seg":
                    new_seg = int(player_result["value"])
                    if new_seg != cur:
                        st.session_state.current_segment = new_seg
                        st.session_state.visited_segments.add(new_seg)
                        cur = new_seg
                        st.rerun()
                elif player_result["type"] == "mode":
                    st.session_state.shadow_playback_mode = player_result["value"]
        else:
            st.warning("Audio not found: " + mat["audio_path"])

        # ── ROW 3: recording ─────────────────────────────────────────
        seg_key   = "seg" + str(cur) + "_" + mat["id"]
        saved_b64 = st.session_state.recordings_by_segment.get(cur)

        st.markdown("**🎙️ Your Recording / 你的录音**")

        if saved_b64:
            st.markdown(
                f"Sentence {cur+1} " +
                '<span style="background:#DCFCE7;color:#166534;border:1px solid #86EFAC;'
                'border-radius:99px;padding:2px 8px;font-size:.72rem;font-weight:700;">'
                "&#10003; recorded</span>",
                unsafe_allow_html=True
            )
            st.audio(base64.b64decode(saved_b64), format="audio/webm")
            if st.button("Re-record / 重录", key="rrec_" + str(cur)):
                del st.session_state.recordings_by_segment[cur]
                st.rerun()
        else:
            result = _sentence_recorder_component(seg_key, cur + 1)
            if result:
                b64 = result["value"]
                st.session_state.recordings_by_segment[cur] = b64
                st.session_state.visited_segments.add(cur)
                st.rerun()

        done_segs = sorted(st.session_state.recordings_by_segment)
        if done_segs:
            st.markdown(
                '<div style="font-size:.75rem;color:#9CA3AF;margin-top:4px;">' +
                "Done: " + " ".join(f"#{i+1}" for i in done_segs) + "</div>",
                unsafe_allow_html=True
            )

        
    # ── FULL PASSAGE STEP ─────────────────────────────────────────
    elif step == 2:
        show_text = st.session_state.get("shadow_show_text", False)
        _tc1, _tc2 = st.columns([1, 4])
        with _tc1:
            if st.button("👁 Hide text / 隐藏" if show_text else "👁 Show text / 显示文本",
                         key="shadow_toggle_text"):
                st.session_state.shadow_show_text = not show_text; st.rerun()
        st.markdown(
            '<div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;'
            'padding:10px 14px;margin-bottom:12px;font-size:.83rem;color:#6B7280;">'
            "Shadow the entire passage continuously. "
            "Text is hidden by default — focus on listening.<br>"
            "整段连续跟读。文本默认隐藏，专注于聆听。"
            "</div>", unsafe_allow_html=True
        )
        if show_text:
            for s in segs:
                st.markdown(
                    '<div style="border-left:3px solid #E5E7EB;padding:8px 14px;'
                    'margin-bottom:6px;font-size:.88rem;color:#6B7280;">'
                    + s["text"] + "</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="background:#F3F4F6;border-radius:8px;padding:28px;'
                'text-align:center;color:#9CA3AF;font-size:.9rem;margin-bottom:12px;">'
                '🎧 Text hidden · Focus on the audio<br>'
                '<span style="font-size:.78rem;">点击上方"Show text"可随时查看</span></div>',
                unsafe_allow_html=True
            )
        st.markdown("---")
        st.markdown("**🔊 Original / 原音**")
        audio_b64 = _load_audio_b64(mat["audio_path"])
        if audio_b64:
            st.audio(base64.b64decode(audio_b64), format="audio/mp3")
        st.markdown("**🎙️ Your Recording / 你的录音**")
        full_b64 = st.session_state.full_recording
        if full_b64:
            st.markdown(
                'Full passage <span style="background:#DCFCE7;color:#166534;'
                'border:1px solid #86EFAC;border-radius:99px;padding:2px 10px;'
                'font-size:.75rem;font-weight:700;">&#10003; recorded</span>',
                unsafe_allow_html=True
            )
            st.audio(base64.b64decode(full_b64), format="audio/webm")
            if st.button("Re-record / 重录", key="rrec_full"):
                st.session_state.full_recording = None
                st.rerun()
        else:
            full_takes_done = 1 if st.session_state.full_recording else 0
            result = _sentence_recorder_func(
                seg_num=0,
                key=f"full_{mat['id']}_take{full_takes_done}",
            )
            if isinstance(result, dict) and result.get("type") == "rec":
                st.session_state.full_recording = result["value"]
                st.rerun()

    col_b, col_f, _ = st.columns([1, 1.5, 2])
    with col_b:
        if st.button("Back to Prepare", key="shd_back"):
            advance_phase("prepare")
            st.rerun()
    with col_f:
        has_rec = bool(st.session_state.recordings_by_segment or st.session_state.full_recording)
        label = "Continue to Compare" if has_rec else "Continue to Compare (no recording yet)"
        if st.button(label + " →", type="primary", key="shd_next_phase"):
            if st.session_state.full_recording:
                st.session_state.compare_recording = {
                    "b64": st.session_state.full_recording, "type": "full"
                }
            elif st.session_state.recordings_by_segment:
                first_key = sorted(st.session_state.recordings_by_segment)[0]
                st.session_state.compare_recording = {
                    "b64": st.session_state.recordings_by_segment[first_key],
                    "type": "sentence", "seg_idx": first_key,
                }
            advance_phase("compare")
            st.rerun()


# ══════════════════════════════════════════════════════════════════
# PHASE 4 — COMPARE
# ══════════════════════════════════════════════════════════════════

def _phase_compare():
    mat  = st.session_state.active_material
    segs = get_segments(mat)

    _phase_header(4, "Compare", "对比",
                  "#DC2626", "#FFF1F2",
                  "Listen to both recordings. Use the cues to focus your attention.")
    _coach_avatar("compare")

    # ── pick which recording to compare ──────────────────────────
    rec_options = {}
    if st.session_state.full_recording:
        rec_options["Full passage recording"] = {
            "b64": st.session_state.full_recording, "type": "full"
        }
    for idx, b64 in sorted(st.session_state.recordings_by_segment.items()):
        rec_options[f"Sentence {idx+1}: {segs[idx]['text'][:50]}…"] = {
            "b64": b64, "type": "sentence", "seg_idx": idx
        }

    if not rec_options:
        st.info("No recordings found. Go back to Phase 3 to record your shadowing.")
        if st.button("← Back to Shadow"):
            advance_phase("shadow"); st.rerun()
        return

    chosen_label = st.selectbox(
        "Select recording to compare / 选择要对比的录音",
        list(rec_options.keys()),
        label_visibility="visible", key="cmp_sel"
    )
    chosen_rec = rec_options[chosen_label]

    st.markdown("---")

    # ── side by side players ──────────────────────────────────────
    col_orig, col_rec = st.columns(2)
    with col_orig:
        st.markdown("""
        <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:10px;
                    padding:14px 16px;margin-bottom:8px;">
            <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.05em;color:#2563EB;margin-bottom:4px;">
                🎵 Original / 原音
            </div>
            <div style="font-size:.85rem;font-weight:600;color:#1E3A5F;">Native Speaker</div>
        </div>
        """, unsafe_allow_html=True)
        audio_b64 = _load_audio_b64(mat["audio_path"])
        if audio_b64:
            st.audio(base64.b64decode(audio_b64), format="audio/mp3")
        else:
            st.warning("Original audio not found.")

    with col_rec:
        st.markdown("""
        <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;
                    padding:14px 16px;margin-bottom:8px;">
            <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.05em;color:#059669;margin-bottom:4px;">
                🎙️ Your Recording / 你的录音
            </div>
            <div style="font-size:.85rem;font-weight:600;color:#064E3B;">Your Shadowing</div>
        </div>
        """, unsafe_allow_html=True)
        st.audio(base64.b64decode(chosen_rec["b64"]), format="audio/webm")

    # ── listening checklist ───────────────────────────────────────
    st.markdown("---")
    st.markdown("**🧭 What to listen for / 对比时关注**")
    cc1, cc2, cc3 = st.columns(3)
    for col, icon, title, detail, detail_zh in [
        (cc1, "💥", "Stress", "Which syllables are stressed differently?", "哪些音节重音不同？"),
        (cc2, "〰️", "Intonation", "Does your pitch rise/fall match?", "升降调是否一致？"),
        (cc3, "🔗", "Linking", "Are word boundaries blended correctly?", "词语边界连读是否正确？"),
    ]:
        with col:
            st.markdown(f"""
            <div class="sl-surface" style="font-size:.82rem;">
                <strong>{icon} {title}</strong><br>
                {detail}<br>
                <span class="muted">{detail_zh}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── per-sentence notice input ─────────────────────────────────
    st.markdown("**📝 Notice Input / 记录你注意到的**")
    st.markdown(
        '<div class="caption-note">'
        'For each sentence below, write what you noticed after listening to both recordings. '
        'Be specific — describe the exact difference you heard.<br>'
        '对于下面的每个句子，听完两段录音后记录你注意到的差异。尽量具体描述你听到的不同之处。'
        '</div>', unsafe_allow_html=True
    )

    # Always show notice inputs for every sentence that has a recording.
    # (If no sentences were recorded, fall back to the full segs list.)
    recorded_indices = sorted(st.session_state.recordings_by_segment.keys())
    if recorded_indices:
        target_segs = [segs[i] for i in recorded_indices]
    else:
        target_segs = segs

    pending_notices = []

    for seg in target_segs:
        st.markdown(f"""
        <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;
                    padding:14px 16px;margin:10px 0;">
            <div class="label-xs" style="margin-bottom:6px;">Sentence {seg['idx']+1}</div>
            <div style="font-size:.92rem;font-weight:600;color:var(--color-primary);
                        margin-bottom:8px;">{seg['text']}</div>
            <div style="background:#FFFBEB;border-left:3px solid #F59E0B;border-radius:4px;
                        padding:8px 12px;font-size:.82rem;color:#92400E;margin-bottom:10px;">
                👂 <strong>Listen for:</strong> {seg['cue_en']}<br>
                <span style="color:#78350F;">{seg['cue_zh']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        notice_text = st.text_area(
            "What did you notice?",
            placeholder='e.g. "I stressed the second syllable in prodigy — original stresses the first"',
            key=f"cmp_notice_{seg['idx']}",
            height=80,
            label_visibility="collapsed",
        )

        # tag selector
        tag_options = ["— no tag —"] + [
            f'{v["label"]} / {v["zh"]}' for v in TAGS.values()
        ]
        tag_sel = st.selectbox(
            "Tag (optional)",
            tag_options,
            key=f"cmp_tag_{seg['idx']}",
            label_visibility="collapsed",
        )
        tag_key = None
        if tag_sel != "— no tag —":
            for k, v in TAGS.items():
                if v["label"] in tag_sel:
                    tag_key = k
                    break

        if notice_text.strip():
            pending_notices.append({
                "text":           notice_text.strip(),
                "tag":            tag_key,
                "sentence":       seg["text"],
                "sentence_idx":   seg["idx"],
                "material_id":    mat["id"],
                "material_title": mat["title"],
                "session_id":     st.session_state.current_session_id,
                "created_at":     datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    # store pending in session state so Capture phase can save them
    st.session_state["_pending_notices"] = pending_notices

    if pending_notices:
        st.success(
            f"{len(pending_notices)} notice{'s' if len(pending_notices)>1 else ''} ready to save."
        )

    st.markdown("---")
    col_b2, col_f2, _ = st.columns([1, 1.5, 2])
    with col_b2:
        if st.button("← Back to Shadow", key="cmp_back"):
            advance_phase("shadow"); st.rerun()
    with col_f2:
        if st.button("Continue to Capture →", type="primary", key="cmp_next"):
            advance_phase("capture"); st.rerun()


# ══════════════════════════════════════════════════════════════════
# PHASE 5 — CAPTURE
# ══════════════════════════════════════════════════════════════════

def _get_gpt_followup(top_tag: str, count: int, session_notices: list) -> str:
    """
    Generate a scaffolded follow-up question based on the student's top notice type.
    Falls back to a static question if AI unavailable.
    """
    from modules.ai import _get_client
    from modules.materials import TAGS

    tag_label = TAGS.get(top_tag, {}).get("label", top_tag)
    notice_texts = [n.get("text", "") for n in session_notices if n.get("tag") == top_tag]
    examples = "; ".join(notice_texts[:2]) if notice_texts else "no specific examples"

    static_fallbacks = {
        "stress":     "You noticed stress issues several times. Can you think of a rule "
                      "about which syllable gets stressed in English multi-syllable words? "
                      "How is that different from how stress works in Mandarin?",
        "link":       "You noticed linking several times. What physical action happens at "
                      "the boundary between two words when linking occurs? "
                      "Why do you think native speakers link sounds this way?",
        "weak":       "You noticed weak forms several times. Why do you think English reduces "
                      "function words to schwa /ə/? What would it sound like if every word "
                      "were given full stress?",
        "intonation": "You noticed intonation patterns. Can you describe what you heard — "
                      "was it a rise, a fall, or something else? "
                      "When do you think English speakers use a rising tone vs a falling tone?",
        "rhythm":     "You noticed rhythm issues. English is stress-timed — content words "
                      "carry the beat. How does that feel different from Mandarin, "
                      "which is syllable-timed?",
    }

    client = _get_client()
    if not client:
        return static_fallbacks.get(top_tag,
            f"You noticed {count} {tag_label} issue(s) today. "
            f"What do you think is the underlying cause? "
            f"How might you practise this specifically before next session?")

    try:
        prompt = (
            f"A Chinese EFL high school student just finished a shadowing session. "
            f"They logged {count} '{tag_label}' notice(s). "
            f"Example notices: {examples}. "
            f"Write ONE short follow-up question (2-3 sentences max) in English that: "
            f"(1) connects their observation to their Mandarin phonological background, "
            f"(2) encourages them to form a hypothesis rather than just describe what happened, "
            f"(3) is specific to '{tag_label}'. "
            f"Do not use jargon. Write in a friendly, curious tone."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return static_fallbacks.get(top_tag,
            f"You noticed {count} {tag_label} issue(s) today. "
            f"What do you think is the underlying cause?")


def _phase_capture():
    mat  = st.session_state.active_material

    _phase_header(5, "Capture", "记录与反思",
                  "#059669", "#ECFDF5",
                  "Reflect on this session, then finish.")
    _coach_avatar("capture")

    # ── commit pending notices ────────────────────────────────────
    pending = st.session_state.pop("_pending_notices", [])
    if pending:
        st.session_state.notice_log.extend(pending)
        st.success(
            f"✅ {len(pending)} notice{'s' if len(pending)>1 else ''} saved to your Notice Log."
        )

    # ── current session data ──────────────────────────────────────
    session_notices = [
        n for n in st.session_state.notice_log
        if n.get("session_id") == st.session_state.current_session_id
    ]
    tag_counts: dict = {}
    for n in session_notices:
        t = n.get("tag")
        if t:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    # ── guided reflection ─────────────────────────────────────────
    st.markdown("### 💭 Reflection / 反思")

    # Show this session's notices as context
    if session_notices:
        st.markdown(
            '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:.06em;color:#9CA3AF;margin-bottom:8px;">'
            "This session's notices / 本次发现</div>",
            unsafe_allow_html=True
        )
        for n in session_notices:
            tag_key = n.get("tag", "")
            t = TAGS.get(tag_key, {})
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:6px;'
                f'padding:8px 12px;background:#F9FAFB;border-radius:8px;'
                f'border-left:3px solid {t.get("color","#E5E7EB")};">'
                f'<span style="background:{t.get("bg","#F3F4F6")};color:{t.get("color","#374151")};'
                f'border-radius:99px;padding:2px 8px;font-size:.72rem;font-weight:700;'
                f'white-space:nowrap;">{t.get("label","?")}</span>'
                f'<span style="font-size:.82rem;color:#374151;">{n.get("text","")}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="color:#9CA3AF;font-size:.85rem;margin-bottom:12px;">'
            "No notices logged this session.</div>",
            unsafe_allow_html=True
        )

    # Q1: Why — with Mandarin interference angle
    st.markdown(
        '<div style="background:#FFFBEB;border-left:4px solid #F59E0B;'
        'border-radius:8px;padding:12px 16px;margin-bottom:6px;">'
        '<div style="font-weight:600;color:#B45309;font-size:.95rem;margin-bottom:2px;">'
        '① Why did this happen? / 为什么会出现这个问题？'
        '</div>'
        '<div style="font-size:.8rem;color:#B45309;opacity:.85;">'
        "Think about the connection to your Mandarin pronunciation habits — "
        "rhythm, syllable structure, or sounds that don't exist in Chinese.<br>"
        '思考与普通话发音习惯的关联——节奏、音节结构，或中文里没有的音素。'
        '</div></div>',
        unsafe_allow_html=True
    )
    resp_reason = st.text_area(
        "Why", height=90, key="cap_reason",
        placeholder="My theory is: when I encounter /r/ + vowel linking, I insert a pause "
                    "because in Mandarin each syllable is more clearly bounded…",
        label_visibility="collapsed"
    )

    # Q2: Progress comparison (only if previous session exists)
    resp_compare = ""
    history = st.session_state.session_history
    if len(history) >= 1:
        last_h = history[-1]
        last_tag_dist = last_h.get("tag_distribution", {})
        last_summary = ", ".join(
            f"{TAGS[k]['label']} ×{v}" for k, v in last_tag_dist.items() if k in TAGS
        ) or "none recorded"
        st.markdown(
            '<div style="background:#EFF6FF;border-left:4px solid #3B82F6;'
            'border-radius:8px;padding:12px 16px;margin-bottom:6px;">'
            '<div style="font-weight:600;color:#1D4ED8;font-size:.95rem;margin-bottom:2px;">'
            '② How does this compare to last time? / 和上次相比有什么变化？'
            '</div>'
            f'<div style="font-size:.78rem;color:#3B82F6;margin-bottom:6px;">'
            f'Last session: {last_summary}</div>'
            '<div style="font-size:.8rem;color:#1D4ED8;opacity:.85;">'
            "Are the same issues showing up, or are you noticing new things?<br>"
            '同样的问题还在出现吗？还是你开始注意到新的现象？'
            '</div></div>',
            unsafe_allow_html=True
        )
        resp_compare = st.text_area(
            "Compare", height=80, key="cap_compare",
            placeholder="Last time I noticed more stress issues. This time linking came up more — "
                        "I think I'm starting to hear stress more naturally…",
            label_visibility="collapsed"
        )

    # Q3: Next focus
    st.markdown(
        '<div style="background:#ECFDF5;border-left:4px solid #10B981;'
        'border-radius:8px;padding:12px 16px;margin-bottom:6px;">'
        '<div style="font-weight:600;color:#065F46;font-size:.95rem;margin-bottom:2px;">'
        '③ What will you focus on next time? / 下次想重点关注什么？'
        '</div>'
        '<div style="font-size:.8rem;color:#065F46;opacity:.85;">'
        "Set one concrete goal — the more specific the better.<br>"
        '设定一个具体目标——越具体越好。'
        '</div></div>',
        unsafe_allow_html=True
    )
    resp_focus = st.text_area(
        "Focus", height=80, key="cap_focus",
        placeholder="Next time I will: listen specifically for weak forms of 'are', 'was', 'were' "
                    "and try to match the schwa reduction…",
        label_visibility="collapsed"
    )

    # Q4: GPT scaffolded follow-up (button, on demand)
    resp_gpt = ""
    if tag_counts and is_ai_available():
        top_tag  = max(tag_counts, key=tag_counts.get)
        gpt_key  = "gpt_followup_" + st.session_state.current_session_id
        gpt_resp_key = "gpt_resp_" + st.session_state.current_session_id

        if gpt_key not in st.session_state:
            if st.button("🤖 Get AI follow-up question / 获取AI追问", key="cap_gpt_btn"):
                with st.spinner("Generating follow-up question…"):
                    followup = _get_gpt_followup(top_tag, tag_counts[top_tag], session_notices)
                st.session_state[gpt_key] = followup
                st.rerun()
        else:
            st.markdown(
                '<div style="background:#F5F3FF;border-left:4px solid #7C3AED;'
                'border-radius:8px;padding:12px 16px;margin-bottom:6px;">'
                '<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:.05em;color:#5B21B6;margin-bottom:6px;">'
                '🤖 AI follow-up / AI追问'
                '</div>'
                f'<div style="font-size:.88rem;color:#3730A3;">'
                f'{st.session_state[gpt_key]}</div>'
                '</div>',
                unsafe_allow_html=True
            )
            resp_gpt = st.text_area(
                "AI follow-up response", height=80, key=gpt_resp_key,
                placeholder="My answer…",
                label_visibility="collapsed"
            )

    st.markdown("---")

    # ── session summary ───────────────────────────────────────────
    sents_visited = len(st.session_state.visited_segments)
    new_vocab     = len(st.session_state.vocabulary)
    recs_made     = len(st.session_state.recordings_by_segment) + (
                        1 if st.session_state.full_recording else 0)

    st.markdown("### 📊 Session Summary / 会话总结")
    m1, m2, m3, m4 = st.columns(4)
    for col, num, lbl, sublbl in [
        (m1, len(session_notices), "Notices",    "recorded"),
        (m2, sents_visited,        "Sentences",  "visited"),
        (m3, recs_made,            "Recordings", "made"),
        (m4, new_vocab,            "Vocab",      "words saved"),
    ]:
        with col:
            st.markdown(
                f'<div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;'
                f'padding:14px 10px;text-align:center;">'
                f'<div style="font-size:1.6rem;font-weight:700;color:#1A3A5C;">{num}</div>'
                f'<div style="font-size:.82rem;font-weight:600;color:#374151;">{lbl}</div>'
                f'<div style="font-size:.75rem;color:#9CA3AF;">{sublbl}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    col_finish, col_feedback = st.columns([2, 1])
    with col_feedback:
        st.markdown(
            '<a href="https://docs.google.com/forms/d/e/1FAIpQLSc6Yl9b5NDR3Zvaaf_k3z1fiYWCgmfj9OspAhFu7tEOt8mo4g/viewform" target="_blank" ' +
            'style="display:block;text-align:center;background:#F9FAFB;' +
            'border:1px solid #E5E7EB;border-radius:8px;padding:10px 12px;' +
            'font-size:.85rem;color:#374151;text-decoration:none;margin-top:2px;">' +
            '💬 Share Feedback / 反馈</a>',
            unsafe_allow_html=True
        )
    with col_finish:
        pass
    if st.button("✅ Finish Session / 结束会话", type="primary", key="cap_finish"):
        tag_dist: dict = {}
        for n in session_notices:
            t = n.get("tag")
            if t:
                tag_dist[t] = tag_dist.get(t, 0) + 1

        st.session_state.session_history.append({
            "session_id":     st.session_state.current_session_id,
            "material_id":    mat["id"],
            "material_title": mat["title"],
            "date":           datetime.now().strftime("%Y-%m-%d %H:%M"),
            "notices":        len(session_notices),
            "sentences":      sents_visited,
            "recordings":     recs_made,
            "reflection": {
                "reason":  resp_reason,
                "compare": resp_compare,
                "focus":   resp_focus,
            },
            "tag_distribution": tag_dist,
        })

        st.session_state.session_phase   = "select"
        st.session_state.active_material = None
        st.session_state.current_session_id = None

        # Auto-save to Firestore
        uid = st.session_state.get("user_uid")
        if uid:
            save_user_data(uid)

        st.rerun()
