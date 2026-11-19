# Project Overview: Revision Hub

Revision Hub is a statically generated study portal built with a dark **"Black Glass"** aesthetic, unifying syllabus-aligned question banks, midterm guides, interactive quizzes, textbook-style comprehensive reports, cheat sheets, and an AI study assistant across six Semester 3 CSE subjects.

---

## Supported Subjects & Color Identity

Each subject maps to a `--subject-color` CSS token across cards, ambient glows, progress bars, and controls:

1. **DBMS** (Database Management Systems) – Blue `#3b82f6` (`dbms/`)
2. **Java** (Object Oriented Programming using Java) – Orange `#f97316` (`java/`)
3. **OS** (Operating Systems) – Emerald `#10b981` (`os/`)
4. **DAA** (Design and Analysis of Algorithms) – Purple `#8b5cf6` (`daa/`)
5. **ML** (Introduction to Machine Learning) – Rose `#f43f5e` (`ml/`)
6. **Maths** (Discrete Mathematics) – Amber `#f59e0b` (`maths/`)

---

## Directory Structure

```text
revision-hub/
├── index.html                    # Landing dashboard & subject mastery tracker
├── profile.html                  # User profile, saved state & Supabase account page
├── reset-password.html           # Password reset page
├── import-data.html              # LocalStorage study progress import/export tool
├── vercel.json                   # Clean URLs + permanent /subjects/(.*) -> /$1 redirect
├── package.json                  # Node test runner (jsdom + Mocha/Node assertions)
├── requirements.txt              # Python prerequisites (Jinja2, BeautifulSoup4, etc.)
├── schema*.sql                   # Supabase Postgres schema & RLS migrations
├── api/
│   ├── package.json              # ESM module config for Vercel Functions
│   ├── chat.js                   # Vercel Serverless Groq proxy (Deep Mode)
│   └── config.js                 # Public runtime Supabase URL + publishable key endpoint
├── data/<subject>/               # Source of truth JSONs (<subject>_questions.json, _quiz.json)
├── templates/                    # Jinja2 templates (question-bank-template.html, quiz-template.html)
├── shared/                       # Shared CSS (design-system.css) & client JS (app-utils.js, assistant-core.mjs, etc.)
├── scripts/                      # Build, quiz generation, OBE picker, report builder & Node test scripts
├── global/assistant-index.json   # Aggregated cross-subject RAG search index
└── <subject>/                    # Generated HTML & assistant-index.json + hand-crafted cheat-sheet.html
```

---

## Build Pipeline & Automated Tests

All `question-bank.html`, `midterm-important.html`, `interactive-quiz.html`, and `assistant-index.json` files are statically generated. Do **not** edit them directly.

```powershell
# 1. Install dependencies
pip install -r requirements.txt
npm install

# 2. Rebuild all subject pages & global assistant RAG index
python scripts\build_site.py

# 3. Run automated JS tests (Assistant router/lookup + DBMS report theme toggle)
npm test

# 4. Preview locally
python -m http.server 8000
```

### Content Pipelines
- **OBE Predictive Filter (`scripts/predictive_picker.py`)**: Scores questions (`score >= 9.0`) against Bloom's Taxonomy levels (`K1/L1–K4/L4`) to flag Midterm high-yield items.
- **Comprehensive Reports (`scripts/build_comprehensive_reports.py`)**: Converts `data/<subject>/<subject>_questions.json` into textbook-style `comprehensive-report.html` pages.
- **AI Quiz & Syllabus Weaving (`scripts/generate_quizzes.py`, `scripts/weave_missing_info.py`)**: Generates MCQ/Code/Short-answer pools and weaves missing syllabus points into cheat sheets.

---

## AI Assistant, Auth & Deployment

### 1. Ask AI Assistant (3-Tier Fallback)
- **Deep Mode (Cloud Default)**: Calls `/api/chat` (`api/chat.js`), a Vercel Serverless function proxying Groq (`https://api.groq.com/openai/v1/chat/completions`) with exponential backoff on `503`.
- **Smart Mode (WebGPU)**: Runs Meta Llama 3.2 locally in WebGPU-capable desktop browsers via `@mlc-ai/web-llm`.
- **Lite Mode (Offline Fallback)**: Runs a client-side BM25 / fuzzy search engine (`shared/assistant-core.mjs`) over `<subject>/assistant-index.json` and `global/assistant-index.json` when WebGPU and cloud AI are unavailable.

### 2. Supabase Authentication & Profile Sync
- Client pages (`profile.html`, `reset-password.html`) fetch public Supabase settings from `/api/config` (`api/config.js`), backed by `schema.sql`, `schema_phase1_5.sql`, and `schema_phase2.sql`.
- **Required Env Vars (Vercel)**:
  - `GROQ_API_KEY` *(Secret)* — Groq API key
  - `GROQ_MODEL` *(Config)* — Active Groq model ID (note: `api/chat.js` currently falls back to `'qwen/qwen3.8-27b'` if unset; verify against Groq's active model catalog)
  - `ALLOWED_ORIGINS` *(Config)* — Comma-separated allowed origins (e.g., `https://larping-study.vercel.app`)
  - `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY` *(Config)* — Used by `api/config.js` *(note: check that Supabase project `pubdqdkdbdfhegcgfwlv` is unpaused/active before testing login/sync)*

### 3. Deployment
Hosted on **Vercel** (`https://larping-study.vercel.app`). `vercel.json` enables `cleanUrls` and permanently redirects legacy `/subjects/*` URLs to `/<subject>/*`. Deploy via Git integration or Vercel CLI (`vercel --prod`) rather than manual folder uploads.

---

## UI & Print Engineering Notes
- **Black Glass CSS**: Uses `#030303` canvas + blurred `.glow-bg` radial gradients + `backdrop-filter: blur(16px)`. Never apply `contain: paint` or `will-change: opacity/transform` on parents of blurred glass elements (breaks blur in Chromium).
- **View Transitions & Performance**: Uses `<meta name="view-transition" content="same-origin">`, pure CSS skeleton loaders, row-batched `IntersectionObserver` cards, and `requestIdleCallback` deferred setup.
- **Client-Side Print/PDF**: "Save as PDF" expands all `details.q-card` accordions and renders a high-contrast `@media print` stylesheet.
