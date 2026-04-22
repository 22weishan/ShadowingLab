# ShadowingLab

A structured shadowing tool for Chinese EFL high school learners.

## Project structure

```
shadowinglab/
├── app.py                  ← entry point
├── requirements.txt
├── audio/
│   └── music_prodigy.mp3   ← place your audio file here
└── modules/
    ├── __init__.py
    ├── state.py            ← session state management
    ├── styles.py           ← global CSS
    ├── materials.py        ← material data + mock annotations
    ├── session.py          ← 5-phase session flow
    ├── phonology.py        ← Phonology Guide + inline cards
    ├── noticelog.py        ← Notice Log page
    └── progress.py         ← Progress dashboard
```

## Setup

```bash
pip install -r requirements.txt
```

Place your audio file at `audio/music_prodigy.mp3`.

## Run

```bash
streamlit run app.py
```

The app must be served over HTTPS (or localhost) for the
in-browser microphone recording to work.

Streamlit Cloud satisfies this automatically.
For local development, localhost also works.

## AI integration (future)

The mock annotations in `modules/materials.py` are ready to be
replaced with real Whisper + GPT output. The data structure for
each segment is:

```python
{
    "idx":    int,
    "text":   str,
    "ts":     {"start": float, "end": float},   # Whisper timestamps
    "annotations": [                             # GPT phonology tags
        {"word": str, "type": str, "label": str, "zh": str}
    ],
    "cue_en": str,   # GPT listening cue (English)
    "cue_zh": str,   # GPT listening cue (Chinese)
}
```

To connect Whisper:
1. Call `openai.audio.transcriptions.create(model="whisper-1", ...
   response_format="verbose_json")` on the audio file.
2. Map word-level timestamps to segments.
3. Pass the transcript to GPT with the annotation prompt.
4. Store the result in the material dict (can be cached to disk).

Add `openai` to requirements.txt when ready.
