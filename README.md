# Resume Tailor Agent

An AI-powered resume tailoring tool built with Streamlit and Claude. Paste a job description and your current resume — the agent analyzes the JD, finds gaps, rewrites your bullets using the STAR-K formula, generates a professional summary, and scores your ATS compatibility. Output is a ready-to-submit tailored resume.

---

## What It Does

1. **Parses the JD** — extracts required skills, preferred skills, ATS keywords, seniority, and hidden signals (team size, tech maturity, culture cues, red flags)
2. **Analyzes gaps** — compares your resume against the JD, produces a match matrix, identifies critical gaps and transferable skills
3. **Rewrites bullets** — applies the STAR-K formula (Action + What + Scale + Result + Keyword) to every bullet; every rewrite includes a number, no duplicate opening verbs, seniority-appropriate verb choices
4. **Generates a summary** — produces 3 summary variants, recommends the highest-scoring one, enforces a 60-word cap
5. **Scores ATS compatibility** — before/after scorecard using the formula: `(0.5 × keyword%) + (0.2 × skills%) + (0.15 × summary) + (0.15 × format)`

---

## Project Structure

```
resume-tailor-agen/
├── app.py                          # Streamlit UI + Claude API call
├── requirements.txt                # Python dependencies
├── agents/
│   └── resume_tailor_agent.md      # Orchestrator prompt (5-step workflow)
└── skills/
    ├── jd_parser.md                # Skill 1 — JD parsing
    ├── gap_analyzer.md             # Skill 2 — Gap analysis
    ├── bullet_rewriter.md          # Skill 3 — Bullet rewriting (STAR-K)
    ├── summary_generator.md        # Skill 4 — Summary generation
    └── ats_scorer.md               # Skill 5 — ATS scoring
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/akv803101/Resume-Agent-demo.git
cd Resume-Agent-demo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

The app reads `ANTHROPIC_API_KEY` automatically from your environment.

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

You can get your API key from [console.anthropic.com](https://console.anthropic.com).

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How to Use

1. **Paste the Job Description** — copy the full JD from LinkedIn or any job board into the left text box
2. **Paste your Resume** — paste your current resume as plain text into the right text box
3. **Click "Tailor My Resume"** — the agent runs all 5 steps and produces a full report
4. **Review the output:**
   - Section 1: Tailored resume (copy-paste ready)
   - Section 2: Gap analysis with match matrix and strategies
   - Section 3: ATS scorecard (before vs. after)
   - Section 4: Next steps checklist

---

## How It Works — Architecture

The system prompt is built by concatenating the orchestrator (`resume_tailor_agent.md`) with all 5 skill prompts at runtime. This means Claude receives the full workflow definition and all skill instructions in a single API call — no multi-turn chaining needed.

```
load_prompts()
  └── agents/resume_tailor_agent.md   (orchestrator)
      + skills/jd_parser.md
      + skills/gap_analyzer.md
      + skills/bullet_rewriter.md
      + skills/summary_generator.md
      + skills/ats_scorer.md
          │
          ▼
  claude-sonnet-4-6  (max_tokens=6000)
          │
          ▼
  Full tailored resume report
```

Prompts are cached with `@st.cache_data` so files are read from disk only once per session.

---

## Skills Reference

| Skill | What It Does |
|---|---|
| `jd_parser` | Extracts role, seniority, required/preferred skills, ATS keywords, hidden signals |
| `gap_analyzer` | Match matrix, critical gaps, transferable skills, keyword overlap % |
| `bullet_rewriter` | STAR-K rewrites with quantification, verb-variety enforcement, fabrication flagging |
| `summary_generator` | 3 summary variants, word-count enforcement, keyword integration |
| `ats_scorer` | Weighted before/after score: keyword 50%, skills 20%, summary 15%, format 15% |

---

## Guardrails

- **No fabrication** — the agent flags any bullet that claims a skill not present in the original resume with ⚠️ FABRICATED
- **Keyword fidelity** — exact JD phrasing is preserved; no synonym-swapping
- **ATS safety** — if keyword overlap is below 30%, the agent warns: *"This role may be a significant stretch."*
- **Bullet quality** — every bullet must have a number; no duplicate opening verbs within a role; no verb used more than twice across all roles

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥1.56 | Web UI |
| `anthropic` | ≥0.96 | Claude API client |
| `reportlab` | ≥4.4 | PDF generation |

---

## Model

Uses `claude-sonnet-4-6` with `max_tokens=6000` to ensure the full ~2,500-word report is never truncated.

---

## License

MIT
