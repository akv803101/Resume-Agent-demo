import streamlit as st
import anthropic
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,   # → creates the PDF file, manages pages
    Paragraph,           # → renders styled text (bold, italic, color)
    Spacer,              # → Spacer(1, N) = N points of vertical whitespace
    Table,               # → Table([[col1_content, col2_content]]) = side-by-side layout
    TableStyle,
    HRFlowable,          # → draws a horizontal line
    KeepInFrame,         # → scales content down to fit rather than crashing
)
from reportlab.lib.styles import ParagraphStyle   # → font, size, color, spacing
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER

st.set_page_config(
    page_title="Resume Tailor Agent",
    page_icon="📄",
    layout="wide"
)

# ── 1. LOAD ALL PROMPTS ───────────────────────────────────────────────────────
@st.cache_data
def load_prompts():
    """
    Concatenate orchestrator + all 5 skills into one system prompt.
    @st.cache_data: reads files once, caches result — not re-read on every click.
    """
    import os
    base = os.path.dirname(__file__)
    system = open(os.path.join(base, "agents/resume_tailor_agent.md")).read()
    for skill in ["jd_parser", "gap_analyzer", "bullet_rewriter",
                  "summary_generator", "ats_scorer"]:
        system += "\n\n---\n\n"
        system += open(os.path.join(base, f"skills/{skill}.md")).read()
    return system

# ── 2. UI — INPUT BOXES ──────────────────────────────────────────────────────
st.markdown("## 📄 Resume Tailor Agent")
st.markdown("Paste a LinkedIn JD + your resume → two ATS-optimised PDFs")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📋 Job Description", height=320,
                      placeholder="Paste the full JD from LinkedIn...")
with col2:
    resume = st.text_area("📄 Current Resume", height=320,
                          placeholder="Paste your resume text here...")

_, run_col, _ = st.columns([3, 2, 3])
with run_col:
    run = st.button("🚀 Tailor My Resume", type="primary",
                    use_container_width=True)

if run:
    if not jd.strip() or not resume.strip():
        st.error("⚠️ Both fields are required.")
    else:
        with st.spinner("Analyzing JD → Finding gaps → Rewriting bullets → Scoring ATS…"):
            try:
                system = load_prompts()
                client = anthropic.Anthropic()
                # ANTHROPIC_API_KEY read automatically from environment
                msg = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=6000,      # full report is ~2,500 words — never truncate
                    system=system,
                    messages=[{
                        "role": "user",
                        "content": (
                            f"## Job Description\n{jd}\n\n"
                            f"## My Current Resume\n{resume}"
                        )
                    }]
                )
                result = msg.content[0].text
                st.session_state["result"] = result
                # Clear cached PDFs when new result comes in
                st.session_state.pop("resume_pdf", None)
                st.session_state.pop("report_pdf", None)
            except Exception as e:
                st.error(f"❌ Error: {e}")
