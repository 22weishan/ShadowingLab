import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
    /* ── Design tokens ─────────────────────────────── */
    :root {
        --color-primary:  #1A3A5C;
        --color-accent:   #2563EB;
        --color-accent-light: #DBEAFE;
        --color-teal:     #0F6E56;
        --color-teal-light: #E1F5EE;
        --color-amber:    #92400E;
        --color-amber-light: #FFFBEB;
        --color-rose:     #9F1239;
        --color-rose-light: #FFF1F2;
        --color-text:     #1F2937;
        --color-muted:    #6B7280;
        --color-border:   #E5E7EB;
        --color-surface:  #F9FAFB;
        --color-white:    #FFFFFF;
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;
    }

    /* ── Sidebar ────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #F8FAFC !important;
        border-right: 1px solid var(--color-border);
    }
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: var(--radius-md) !important;
        font-size: .88rem !important;
        padding: 8px 14px !important;
        margin-bottom: 2px;
    }

    /* ── Global typography ──────────────────────────── */
    h1 { font-size: 1.6rem !important; font-weight: 700 !important;
         color: var(--color-primary) !important; }
    h2 { font-size: 1.2rem !important; font-weight: 600 !important;
         color: var(--color-primary) !important; }
    h3 { font-size: 1rem !important; font-weight: 600 !important;
         color: var(--color-text) !important; }

    /* ── Cards ──────────────────────────────────────── */
    .sl-card {
        background: var(--color-white);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: 20px 22px;
        margin-bottom: 12px;
    }
    .sl-card-accent {
        border-left: 4px solid var(--color-accent);
    }
    .sl-card-teal {
        border-left: 4px solid var(--color-teal);
    }
    .sl-card-amber {
        border-left: 4px solid #F59E0B;
    }
    .sl-surface {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 14px 16px;
    }

    /* ── Phase banner ───────────────────────────────── */
    .phase-banner {
        display: flex;
        align-items: center;
        gap: 14px;
        border-radius: var(--radius-lg);
        padding: 14px 20px;
        margin-bottom: 20px;
    }

    /* ── Sentence display ───────────────────────────── */
    .sent-active {
        background: #DBEAFE;
        border-left: 4px solid var(--color-accent);
        border-radius: var(--radius-sm);
        padding: 10px 14px;
        margin: 5px 0;
        font-size: .95rem;
        font-weight: 600;
        color: var(--color-primary);
        line-height: 1.6;
    }
    .sent-done {
        background: #F0FDF4;
        border-left: 3px solid #10B981;
        border-radius: var(--radius-sm);
        padding: 8px 12px;
        margin: 4px 0;
        font-size: .88rem;
        color: var(--color-text);
        line-height: 1.6;
    }
    .sent-inactive {
        border-left: 3px solid var(--color-border);
        border-radius: var(--radius-sm);
        padding: 8px 12px;
        margin: 4px 0;
        font-size: .88rem;
        color: var(--color-muted);
        line-height: 1.6;
    }

    /* ── Notice tag chips ───────────────────────────── */
    .tag-chip {
        display: inline-block;
        border-radius: 99px;
        padding: 3px 11px;
        font-size: .75rem;
        font-weight: 600;
        margin: 2px 3px 2px 0;
        cursor: default;
    }

    /* ── Phonology annotation inline labels ─────────── */
    .ann-stress  { background:#FFFBEB; color:#92400E;
                   font-size:.7rem; font-weight:600;
                   border-radius:4px; padding:1px 5px; }
    .ann-link    { background:#DBEAFE; color:#1D4ED8;
                   font-size:.7rem; font-weight:600;
                   border-radius:4px; padding:1px 5px; }
    .ann-weak    { background:#EDE9FE; color:#5B21B6;
                   font-size:.7rem; font-weight:600;
                   border-radius:4px; padding:1px 5px; }
    .ann-rhythm  { background:#FCE7F3; color:#9D174D;
                   font-size:.7rem; font-weight:600;
                   border-radius:4px; padding:1px 5px; }
    .ann-intonation { background:#ECFDF5; color:#065F46;
                   font-size:.7rem; font-weight:600;
                   border-radius:4px; padding:1px 5px; }

    /* ── Progress bar ───────────────────────────────── */
    .prog-bar-wrap {
        background: var(--color-border);
        border-radius: 99px;
        height: 6px;
        overflow: hidden;
        margin: 4px 0;
    }
    .prog-bar-fill {
        height: 100%;
        border-radius: 99px;
        background: var(--color-accent);
        transition: width .3s ease;
    }

    /* ── Misc helpers ───────────────────────────────── */
    .label-xs {
        font-size: .72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .05em;
        color: var(--color-muted);
        margin-bottom: 4px;
    }
    .muted { color: var(--color-muted); font-size: .85rem; }
    .caption-note {
        background: var(--color-surface);
        border-radius: var(--radius-md);
        padding: 10px 14px;
        font-size: .82rem;
        color: var(--color-muted);
        margin: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)
