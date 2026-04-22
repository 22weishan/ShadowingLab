"""
ai.py  —  OpenAI integration layer (Whisper + GPT)

All AI calls are isolated here.  The rest of the codebase uses mock
data by default; set OPENAI_API_KEY in Streamlit secrets or environment
to activate real API calls.

Usage
-----
from modules.ai import annotate_material, get_session_suggestion

# annotate a material (run once, result cached in session_state)
segs = annotate_material(material)

# get a suggestion after capture phase
suggestion = get_session_suggestion(tag_counts, total_notices)
"""

import os
import json
import streamlit as st

# ── try to import openai; degrade gracefully if not installed ──────
try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


def _get_client():
    """Return an OpenAI client, or None if key/library unavailable."""
    if not _OPENAI_AVAILABLE:
        return None
    key = (
        st.secrets.get("OPENAI_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )
    if not key:
        return None
    return OpenAI(api_key=key)


def is_ai_available() -> bool:
    return _get_client() is not None


# ══════════════════════════════════════════════════════════════════
# WHISPER — transcribe audio + get word timestamps
# ══════════════════════════════════════════════════════════════════

def transcribe_audio(audio_path: str) -> dict | None:
    """
    Call Whisper on a local audio file.
    Returns verbose_json dict with word-level timestamps, or None on failure.
    """
    client = _get_client()
    if not client:
        return None
    try:
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )
        return result.model_dump()
    except Exception as e:
        st.warning(f"Whisper transcription failed: {e}")
        return None


def align_whisper_to_segments(whisper_result: dict, segments: list) -> list:
    """
    Align Whisper word-level timestamps to sentence segments.
    Uses sequential matching — never goes backwards in the word list.
    Falls back to proportional estimation for any segment that fails to match.
    """
    words = whisper_result.get("words", [])
    if not words or not segments:
        return segments

    import re

    def clean(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    word_texts = [clean(w.get("word", "")) for w in words]
    total_dur  = words[-1]["end"] if words else 1.0
    search_from = 0
    updated = []

    for seg in segments:
        seg_words = [clean(w) for w in seg["text"].split() if clean(w)]
        if not seg_words:
            updated.append(seg)
            continue

        first_w = seg_words[0]
        last_w  = seg_words[-1]
        n_words = len(seg_words)

        # ── find start of segment ────────────────────────────────
        start_idx = None
        # try exact match first
        for i in range(search_from, len(word_texts)):
            if word_texts[i] == first_w:
                start_idx = i
                break
        # fallback: partial match (first 4 chars)
        if start_idx is None and len(first_w) >= 3:
            prefix = first_w[:4]
            for i in range(search_from, len(word_texts)):
                if word_texts[i].startswith(prefix):
                    start_idx = i
                    break
        # fallback: use search_from position
        if start_idx is None:
            start_idx = search_from

        # ── find end of segment ──────────────────────────────────
        # search up to n_words*2 ahead to handle insertions/deletions
        search_end = min(start_idx + n_words * 2 + 5, len(words) - 1)
        end_idx = min(start_idx + n_words - 1, len(words) - 1)

        # try exact match for last word
        for i in range(start_idx, search_end + 1):
            if word_texts[i] == last_w:
                end_idx = i  # keep updating — take the furthest match in range

        # ── build timestamp ──────────────────────────────────────
        ts = {
            "start": round(max(0.0, words[start_idx]["start"] - 0.05), 2),
            "end":   round(min(total_dur, words[end_idx]["end"] + 0.1), 2),
        }
        # sanity check — end must be after start
        if ts["end"] <= ts["start"]:
            ts["end"] = ts["start"] + 2.0

        updated.append({**seg, "ts": ts, "_whisper_aligned": True})
        search_from = end_idx + 1

    return updated


def get_timestamps_for_material(material: dict) -> list:
    """
    Main entry point for timestamp retrieval.

    1. Check session_state cache — return immediately if already computed.
    2. Try Whisper API — if available, transcribe and align.
    3. Fall back to word-count estimation if Whisper unavailable.

    Returns a list of {start, end} dicts, one per segment.
    """
    from modules.materials import get_segments

    cache_key = "whisper_ts_" + material["id"] + "_" + str(len(get_segments(material)))
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    segs = get_segments(material)

    # Try Whisper
    client = _get_client()
    if client:
        whisper = transcribe_audio(material["audio_path"])
        if whisper:
            aligned = align_whisper_to_segments(whisper, segs)
            ts_list = [s["ts"] for s in aligned]
            st.session_state[cache_key] = ts_list
            return ts_list

    # Fallback: word-count proportion
    ts_list = _estimate_timestamps(segs, material.get("duration_sec", 60))
    st.session_state[cache_key] = ts_list
    return ts_list


def _estimate_timestamps(segments: list, total_sec: float) -> list:
    """Word-count-based timestamp estimation (fallback only)."""
    pad   = 0.5
    avail = max(total_sec - pad, 1.0)
    wcs   = [max(1, len(s["text"].split())) for s in segments]
    total = sum(wcs)
    out, cursor = [], pad
    for wc in wcs:
        dur = wc / total * avail
        out.append({"start": round(cursor, 2), "end": round(cursor + dur, 2)})
        cursor += dur
    # Always return one entry per segment
    assert len(out) == len(segments)
    return out


# ══════════════════════════════════════════════════════════════════
# GPT — phonological annotation + listening cues
# ══════════════════════════════════════════════════════════════════

_ANNOTATION_SYSTEM = """You are a phonology expert specialising in English as a foreign language
for Mandarin-Chinese speaking learners. You will be given a sentence from an English listening
passage. Your task is to:

1. Identify up to 4 words or word-pairs with notable phonological features that are
   commonly difficult for Mandarin speakers. Focus on:
   - Word stress (especially multi-syllable nouns/verbs where stress is non-obvious)
   - Linking (consonant-final word followed by vowel-initial word)
   - Weak forms (articles, prepositions, auxiliaries that reduce to schwa)
   - Intonation (sentence-final rise or fall, or a notable contour)

2. Write a short listening cue in both English and Chinese (Simplified) that tells the
   student exactly what to listen for in this sentence. Keep each cue to 1-2 sentences.

Return ONLY valid JSON in this exact format, no other text:
{
  "annotations": [
    {"word": "<word or word-pair>", "type": "<stress|link|weak|intonation>",
     "label": "<short label like 'stress: PRO-' or 'linking' or 'weak /e/'>"}
  ],
  "cue_en": "<English listening cue>",
  "cue_zh": "<Chinese listening cue>"
}"""


def annotate_segment(sentence: str) -> dict | None:
    """
    Call GPT to annotate phonological features of a single sentence.
    Returns dict with annotations, cue_en, cue_zh, or None on failure.
    """
    client = _get_client()
    if not client:
        return None
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _ANNOTATION_SYSTEM},
                {"role": "user",   "content": f'Sentence: "{sentence}"'},
            ],
            temperature=0.3,
            max_tokens=400,
        )
        raw = resp.choices[0].message.content.strip()
        # strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as e:
        st.warning(f"GPT annotation failed for sentence: {e}")
        return None


def annotate_material(material: dict) -> list:
    """
    Annotate all segments of a material using GPT.
    Results are cached in st.session_state to avoid repeated API calls.
    Returns the updated segments list.
    """
    cache_key = f"ai_annotations_{material['id']}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    segments = material["segments"][:]
    updated  = []

    progress = st.progress(0, text="Annotating with GPT…")
    for i, seg in enumerate(segments):
        result = annotate_segment(seg["text"])
        if result:
            # convert GPT annotation format to internal format
            anns = []
            for a in result.get("annotations", []):
                anns.append({
                    "word":  a.get("word", ""),
                    "type":  a.get("type", "stress"),
                    "label": a.get("label", ""),
                    "zh":    "",  # GPT doesn't return zh label per-annotation
                })
            new_seg = {
                **seg,
                "annotations": anns,
                "cue_en":      result.get("cue_en", seg.get("cue_en", "")),
                "cue_zh":      result.get("cue_zh", seg.get("cue_zh", "")),
                "_ai_annotated": True,
            }
        else:
            new_seg = seg  # fall back to mock data
        updated.append(new_seg)
        progress.progress((i + 1) / len(segments),
                          text=f"Annotating sentence {i+1}/{len(segments)}…")

    progress.empty()
    st.session_state[cache_key] = updated
    return updated


# ══════════════════════════════════════════════════════════════════
# GPT — session suggestion
# ══════════════════════════════════════════════════════════════════

_SUGGESTION_SYSTEM = """You are a supportive English pronunciation coach for Chinese high school
students. Based on a student's notice log from one practice session, give ONE specific,
actionable suggestion for their next session. Write 2-3 sentences in English, then the
same in Chinese. Be concrete — not "practise more" but "before shadowing, circle every
consonant-vowel word boundary and predict where linking will occur."

Format: one paragraph in English, then one paragraph in Chinese. No headings."""


def get_session_suggestion(tag_counts: dict, total_notices: int) -> str | None:
    """
    Call GPT to generate a personalised suggestion based on this session's notice types.
    Returns a string (English + Chinese), or None if AI unavailable.
    """
    client = _get_client()
    if not client or not tag_counts:
        return None

    tag_summary = ", ".join(
        f"{k} ({v} notice{'s' if v != 1 else ''})"
        for k, v in sorted(tag_counts.items(), key=lambda x: -x[1])
    )
    prompt = (
        f"The student completed one shadowing session and recorded {total_notices} notices. "
        f"Notice type breakdown: {tag_summary}. "
        f"Give one specific suggestion for their next session."
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SUGGESTION_SYSTEM},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.5,
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return None


# ══════════════════════════════════════════════════════════════════
# GPT — notice log pattern summary
# ══════════════════════════════════════════════════════════════════

_PATTERN_SYSTEM = """You are a supportive English pronunciation coach for Chinese high school
students. Analyse the student's notice log and identify recurring patterns. Write a short
paragraph (3-4 sentences) in English identifying the main pattern and giving one concrete
study suggestion. Then write the same in Chinese.

Format: English paragraph, blank line, Chinese paragraph. No headings, no bullet points."""


def get_pattern_summary(notice_log: list) -> str | None:
    """
    Call GPT to summarise patterns across all notices.
    Returns a string, or None if AI unavailable or fewer than 5 notices.
    """
    client = _get_client()
    if not client or len(notice_log) < 5:
        return None

    # send a compact summary of notices to avoid token overuse
    lines = []
    for n in notice_log[-20:]:  # last 20 notices max
        tag  = n.get("tag", "untagged")
        text = n.get("text", "")[:80]
        lines.append(f"[{tag}] {text}")
    notices_text = "\n".join(lines)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _PATTERN_SYSTEM},
                {"role": "user",
                 "content": f"Student notice log (most recent first):\n{notices_text}"},
            ],
            temperature=0.4,
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return None
