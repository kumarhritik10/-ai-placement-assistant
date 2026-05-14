"""
app.py  -  AI Placement Writing Assistant
Streamlit Cloud compatible. No heavy ML dependencies.
"""

import re
import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))



st.set_page_config(
    page_title="AI Placement Assistant",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: #0d1220 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

.hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2040 50%, #1a1040 100%);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 18px;
    padding: 36px 40px;
    margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(245,158,11,0.10), transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.1rem; font-weight: 700; margin: 0 0 8px 0;
    background: linear-gradient(90deg, #f59e0b, #fbbf24, #e2e8f0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: #94a3b8; font-size: 0.98rem; margin: 0; }

.metric-row { display: flex; gap: 14px; margin: 18px 0; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 120px;
    background: #111827;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 16px 18px; text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: rgba(245,158,11,0.3); }
.metric-val {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.metric-label { color: #64748b; font-size: 0.75rem; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

.section-head {
    color: #f1f5f9; font-size: 0.85rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px;
    margin: 22px 0 10px 0;
    border-left: 3px solid #f59e0b; padding-left: 10px;
}

.diff-box {
    background: #0f172a; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;
    line-height: 2; color: #e2e8f0; min-height: 70px;
}
.w-ok      { color: #cbd5e1; }
.w-changed { background: rgba(245,158,11,0.18); color: #fbbf24;
             border-radius: 4px; padding: 1px 5px; }
.w-filler  { background: rgba(239,68,68,0.18); color: #f87171;
             border-radius: 4px; padding: 1px 5px;
             text-decoration: underline dotted; }

.ats-track { background: #1e293b; border-radius: 999px; height: 10px; overflow: hidden; margin-top: 6px; }
.ats-fill  { height: 100%; border-radius: 999px;
             background: linear-gradient(90deg, #f59e0b, #22c55e);
             transition: width 0.6s ease; }

.kw-matched { display:inline-block; background: rgba(34,197,94,0.12);
              border: 1px solid rgba(34,197,94,0.3); color: #4ade80;
              border-radius: 6px; padding: 2px 10px; margin: 3px; font-size: 0.8rem; }
.kw-missing { display:inline-block; background: rgba(245,158,11,0.10);
              border: 1px solid rgba(245,158,11,0.3); color: #fbbf24;
              border-radius: 6px; padding: 2px 10px; margin: 3px; font-size: 0.8rem; }

.suggestion-card {
    background: #111827; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 14px 18px; margin: 7px 0;
}
.weak-word   { color: #f87171; font-weight: 600; }
.strong-alts { color: #4ade80; }

.verb-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.verb-pill {
    background: rgba(245,158,11,0.10); border: 1px solid rgba(245,158,11,0.3);
    color: #fbbf24; border-radius: 999px;
    padding: 4px 14px; font-size: 0.8rem;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0f172a; border-radius: 12px; padding: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: #64748b; font-weight: 500; padding: 8px 22px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a5f, #1a1040) !important;
    color: #fbbf24 !important;
    border-bottom: 2px solid #f59e0b !important;
}
.stTextArea textarea {
    background: #0f172a !important; color: #e2e8f0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; font-size: 0.95rem !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: #080d1a !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 28px !important; transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(245,158,11,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Cached loaders ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Building spell-check corpus...")
def load_spell_engine():
    import auto_correct as ac
    return ac

@st.cache_data(show_spinner=False)
def load_vocab():
    from placement_vocab import WEAK_TO_STRONG, ATS_KEYWORDS, FILLER_WORDS, POWER_VERBS
    return WEAK_TO_STRONG, ATS_KEYWORDS, FILLER_WORDS, POWER_VERBS

# ── Helpers ───────────────────────────────────────────────────────────────────
def second_pass_correct(text: str, ac) -> str:
    """Run a second Norvig pass on already-corrected text for cleaner output."""
    corrected, _ = ac.correct_with_diff(text)
    return corrected

def ats_score(text: str, keywords: list) -> tuple:
    """Returns (score 0-100, matched list, missing list)."""
    tl = text.lower()
    matched = [kw for kw in keywords if kw.lower() in tl]
    missing = [kw for kw in keywords if kw.lower() not in tl]
    score   = round(len(matched) / max(len(keywords), 1) * 100)
    return score, matched, missing

def detect_fillers(text: str, filler_list: list) -> list:
    found = []
    for f in filler_list:
        for m in re.finditer(r'\b' + re.escape(f) + r'\b', text, re.IGNORECASE):
            found.append((m.start(), m.end(), m.group()))
    return sorted(found, key=lambda x: x[0])

def highlight_fillers_html(text: str, fillers: list) -> str:
    if not fillers:
        return f'<span class="w-ok">{text}</span>'
    out, prev = "", 0
    for s, e, w in fillers:
        out += f'<span class="w-ok">{text[prev:s]}</span>'
        out += f'<span class="w-filler" title="Filler word">{w}</span>'
        prev = e
    return out + f'<span class="w-ok">{text[prev:]}</span>'

def render_diff_html(changes) -> str:
    parts = []
    for c in changes:
        if c.changed:
            parts.append(f'<span class="w-changed" title="Was: {c.original}">{c.corrected}</span>')
        else:
            parts.append(f'<span class="w-ok">{c.original}</span>')
    return " ".join(parts)

def professionalism_score(text: str, filler_list: list) -> int:
    words = text.split()
    if not words:
        return 100
    filler_hits = sum(1 for f in filler_list
                      if re.search(r'\b' + re.escape(f) + r'\b', text, re.IGNORECASE))
    penalty = min(70, filler_hits * 10)
    return max(0, 100 - penalty)

def composite_score(spell: int, ats: int, prof: int) -> int:
    return round(spell * 0.35 + ats * 0.35 + prof * 0.30)

def weak_word_suggestions(text: str, weak_map: dict) -> list:
    tl = text.lower()
    return [(w, alts) for w, alts in weak_map.items()
            if re.search(r'\b' + re.escape(w) + r'\b', tl)]

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("corrections", 0), ("fillers_caught", 0)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Placement AI")
    st.caption("AI Placement Writing Assistant")
    st.divider()

    target_role = st.selectbox(
        "Target Role",
        ["Software Engineer (SDE)", "Data Analyst", "ML / AI Engineer",
         "Full Stack Developer", "DevOps / Cloud", "Business Analyst"],
    )
    st.divider()
    st.markdown("### Session Stats")
    c1, c2 = st.columns(2)
    c1.metric("Corrections", st.session_state.corrections)
    c2.metric("Fillers", st.session_state.fillers_caught)
    st.divider()
    st.caption("Norvig Probabilistic NLP")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title">AI Placement Assistant</p>
  <p class="hero-sub">AI-powered writing assistant for college placements — spell correction, ATS scoring, interview polish, and vocabulary upgrade</p>
</div>
""", unsafe_allow_html=True)

# ── Load resources ────────────────────────────────────────────────────────────
ac = load_spell_engine()
WEAK_TO_STRONG, ATS_KEYWORDS, FILLER_WORDS, POWER_VERBS = load_vocab()

tab1, tab2, tab3 = st.tabs([
    "Resume Corrector",
    "Interview Polish",
    "Vocabulary Upgrade",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Resume Corrector
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-head">Paste your resume section or cover letter</p>', unsafe_allow_html=True)

    resume_input = st.text_area(
        label="Resume input",
        label_visibility="collapsed",
        placeholder="e.g.  I have devloped a machine lerning model using pytoch and deployd it on AWS with 95% acuracy...",
        height=170, key="resume_text",
    )
    word_count = len(resume_input.split()) if resume_input.strip() else 0
    st.caption(f"{word_count} words")

    run_resume = st.button("Analyse and Correct", key="btn_resume")

    if run_resume:
        if not resume_input.strip():
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Running spell correction and ATS analysis..."):
                corrected_text, changes = ac.correct_with_diff(resume_input)
                spell            = ac.get_spelling_score(resume_input)
                n_errors         = sum(1 for c in changes if c.changed)
                st.session_state.corrections += n_errors

                # TextBlob second-pass correction
                final_text = second_pass_correct(corrected_text, ac)

                role_kws              = ATS_KEYWORDS.get(target_role, [])
                ats, matched, missing = ats_score(final_text, role_kws)
                prof                  = professionalism_score(final_text, FILLER_WORDS)
                overall               = composite_score(spell, ats, prof)

            # Metric strip
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-card"><div class="metric-val">{overall}</div><div class="metric-label">Resume Score</div></div>
              <div class="metric-card"><div class="metric-val">{spell}</div><div class="metric-label">Spell Score</div></div>
              <div class="metric-card"><div class="metric-val">{ats}%</div><div class="metric-label">ATS Match</div></div>
              <div class="metric-card"><div class="metric-val">{n_errors}</div><div class="metric-label">Errors Fixed</div></div>
            </div>
            """, unsafe_allow_html=True)

            # ATS bar
            st.markdown(f"""
            <div style="margin:4px 0 4px 0">
              <div style="display:flex;justify-content:space-between;color:#94a3b8;font-size:0.82rem;margin-bottom:6px">
                <span>ATS Keyword Score — {target_role}</span><span>{ats}%</span>
              </div>
              <div class="ats-track"><div class="ats-fill" style="width:{ats}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

            # Keyword breakdown
            kw_col1, kw_col2 = st.columns(2)
            with kw_col1:
                st.markdown("**Matched keywords**")
                if matched:
                    st.markdown("".join(f'<span class="kw-matched">{k}</span>' for k in matched), unsafe_allow_html=True)
                else:
                    st.caption("None matched yet")
            with kw_col2:
                st.markdown("**Suggested additions**")
                if missing:
                    st.markdown("".join(f'<span class="kw-missing">{k}</span>' for k in missing[:6]), unsafe_allow_html=True)
                else:
                    st.caption("All keywords covered!")

            # Side-by-side diff
            st.markdown('<p class="section-head">Before vs After</p>', unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.markdown("**Original**")
                st.markdown(f'<div class="diff-box">{resume_input}</div>', unsafe_allow_html=True)
            with right:
                st.markdown("**Corrected** (hover word to see original)")
                diff_html = render_diff_html(changes)
                st.markdown(f'<div class="diff-box">{diff_html}</div>', unsafe_allow_html=True)

            # Final output with built-in copy
            st.markdown('<p class="section-head">Final Corrected Text</p>', unsafe_allow_html=True)
            st.code(final_text, language="text")
            st.download_button(
                "Download corrected text",
                data=final_text,
                file_name="corrected_resume.txt",
                mime="text/plain",
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Interview Polish
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-head">Paste your interview answer</p>', unsafe_allow_html=True)

    interview_input = st.text_area(
        label="Interview input",
        label_visibility="collapsed",
        placeholder='e.g. "Basically I just used python for the project and like, I think I was responsible for the backend stuff..."',
        height=150, key="interview_text",
    )
    run_interview = st.button("Polish My Answer", key="btn_interview")

    if run_interview:
        if not interview_input.strip():
            st.warning("Please enter your answer.")
        else:
            with st.spinner("Analysing tone and fillers..."):
                fillers_found = detect_fillers(interview_input, FILLER_WORDS)
                prof_score    = professionalism_score(interview_input, FILLER_WORDS)
                spell_fixed, _= ac.correct_with_diff(interview_input)
                polished      = second_pass_correct(spell_fixed, ac)
                st.session_state.fillers_caught += len(fillers_found)

            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-card"><div class="metric-val">{prof_score}</div><div class="metric-label">Professionalism</div></div>
              <div class="metric-card"><div class="metric-val">{len(fillers_found)}</div><div class="metric-label">Fillers Found</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<p class="section-head">Filler Word Analysis</p>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="diff-box">{highlight_fillers_html(interview_input, fillers_found)}</div>',
                unsafe_allow_html=True,
            )
            st.caption("Red underlined words are fillers — remove or rephrase for a confident tone")

            if fillers_found:
                unique = sorted({f[2].lower() for f in fillers_found})
                st.markdown("**Detected:** " + "  |  ".join([f"`{w}`" for w in unique]))

            st.markdown('<p class="section-head">Polished Answer</p>', unsafe_allow_html=True)
            st.code(polished, language="text")

            with st.expander("Interview Answer Tips"):
                for tip in [
                    "Use the STAR method: Situation, Task, Action, Result",
                    "Keep behavioural answers under 2 minutes",
                    "Quantify your impact — instead of 'improved performance', say 'reduced latency by 40%'",
                    "Start every answer with a strong action verb",
                    "End with the outcome or what you learned",
                ]:
                    st.markdown(f"- {tip}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Vocabulary Upgrade
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-head">Paste your resume bullets or bio</p>', unsafe_allow_html=True)

    vocab_input = st.text_area(
        label="Vocab input",
        label_visibility="collapsed",
        placeholder='e.g. "I made a web app using React and used REST APIs. I helped fix bugs and worked on the database."',
        height=140, key="vocab_text",
    )
    run_vocab = st.button("Upgrade Vocabulary", key="btn_vocab")

    if run_vocab:
        if not vocab_input.strip():
            st.warning("Please enter some text first.")
        else:
            suggestions = weak_word_suggestions(vocab_input, WEAK_TO_STRONG)
            if not suggestions:
                st.success("No weak resume words detected. Vocabulary looks strong.")
            else:
                st.markdown(f'<p class="section-head">{len(suggestions)} Weak Word(s) Found</p>', unsafe_allow_html=True)
                for weak, alts in suggestions:
                    st.markdown(f"""
                    <div class="suggestion-card">
                      <span class="weak-word">"{weak}"</span>
                      <span style="color:#475569;margin:0 8px">→</span>
                      <span class="strong-alts">{" · ".join(alts)}</span>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown('<p class="section-head">Power Verb Bank</p>', unsafe_allow_html=True)
    st.caption("Copy and use these in your resume bullet points")
    verb_pills = "".join(f'<span class="verb-pill">{v}</span>' for v in POWER_VERBS)
    st.markdown(f'<div class="verb-grid">{verb_pills}</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander(f"ATS Keywords for {target_role}"):
        role_kws = ATS_KEYWORDS.get(target_role, [])
        st.markdown("  ·  ".join([f"`{kw}`" for kw in role_kws]))
        st.caption("Include these naturally in your resume to pass ATS filters.")
