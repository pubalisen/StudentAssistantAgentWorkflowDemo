# UCSC Student Services — Lisa 🎓

**ADK 2.0 Multi-Agent Demo** for UC Santa Cruz student services, built with Google's Agent Development Kit. Lisa is an AI assistant that helps UCSC students with enrollment, advising, tuition, housing, and more — grounded in real 2025-2026 university data.

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│              Root Orchestrator — "Lisa" (LlmAgent)                     │
│              Model: gemini-2.5-flash                                   │
│              Tool: lookup_ucsc_knowledge (FunctionTool)                │
├──────────┬──────────────┬─────────────┬───────────────────────────────┤
│          │              │             │                               │
│ Sequential│   Parallel   │    Loop    │   Web Search Agent            │
│ Enrollment│   Semester   │    Advisor │   (GoogleSearchTool)          │
│ Pipeline │   Dashboard  │    Session  │                               │
│          │              │             │   Live web grounding          │
│ Prereq   │ Courses      │  Student Q │   for fresh queries           │
│  Check   │ Financial Aid│    ↓       │                               │
│   ↓      │ Housing      │  Advisor   │                               │
│ Schedule │ Events       │  Response  │                               │
│  Builder │              │    ↓ loop  │                               │
│   ↓      │              │  Resolved? │                               │
│ Confirm  │              │            │                               │
└──────────┴──────────────┴────────────┴───────────────────────────────┘
```

### ADK 2.0 Patterns Demonstrated

| Pattern | Agent | Purpose |
|---------|-------|---------|
| **SequentialAgent** | `enrollment_pipeline` | Prereq Check → Schedule Build → Enrollment Confirm |
| **ParallelAgent** | `semester_dashboard` | Courses + Financial Aid + Housing + Events (concurrent) |
| **LoopAgent** | `advisor_session` | Multi-turn advising until resolved (max 5 iterations) |
| **LlmAgent** | `web_search_agent` | Google Search grounding for live queries |
| **FunctionTool** | `knowledge_tool` | RAG over 8 real UCSC documents |

### Grounding Strategy

**Local RAG** — 8 real UCSC documents (~34K tokens) served via `lookup_ucsc_knowledge` tool:

| Document | Content |
|----------|---------|
| `cs-bs-requirements.md` | CS B.S. prerequisites, courses, 4-year plan |
| `biology-biochem-requirements.md` | Bio, MCD Bio, BMB requirements + CS switch comparison |
| `tuition-and-fees.md` | Tuition, COA, financial aid, payment deadlines |
| `academic-calendar.md` | Quarter dates, enrollment passes, deadlines |
| `professors-and-advising.md` | 10 CSE faculty profiles, office hours |
| `ucsc-faq.md` | 20+ student Q&As |
| `housing-and-dining.md` | 10 colleges, room rates, meal plans |
| `campus-map-and-buildings.md` | Building directory, parking, transit |

**Google Search** — Isolated `web_search_agent` for live queries (news, events, cross-UC comparisons).

> **Note:** Vertex AI requires search tools and function tools to be on separate agents. Lisa uses `FunctionTool` on root, `GoogleSearchTool` on `web_search_agent`.

## Quick Start

### Prerequisites
- Python 3.10+
- GCP project with Vertex AI API enabled
- Service account with AI Platform permissions

### Local Development

```bash
# Clone and install
cd agents/ucsc-student-services
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example app/.env
# Edit app/.env with your GCP project and credentials

# Run locally
adk web --port 8001
# Open http://localhost:8001
```

### Deploy to Cloud Run

```bash
# Authenticate
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push
gcloud builds submit --tag gcr.io/mygenerativeai/ucsc-student-services

# Deploy
gcloud run deploy ucsc-student-services \
  --image gcr.io/mygenerativeai/ucsc-student-services \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=mygenerativeai,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE"
```

### Deploy to Vertex AI Agent Engine

```bash
python deploy.py --project mygenerativeai
python deploy.py --dry-run  # Validate first
python deploy.py --list     # List deployed agents
```

## Sample Queries

| Query | Workflow Triggered |
|-------|--------------------|
| "What are the prerequisites for CSE 130?" | `lookup_ucsc_knowledge` → cs_requirements |
| "I want to enroll in CSE 101 for Fall" | `enrollment_pipeline` (Sequential) |
| "Give me everything for Winter 2026" | `semester_dashboard` (Parallel) |
| "Should I switch from Biology to CS?" | `advisor_session` (Loop) |
| "How much is tuition for a CA resident?" | `lookup_ucsc_knowledge` → tuition |
| "Who teaches CSE 140?" | `lookup_ucsc_knowledge` → professors |
| "Is there a career fair this fall?" | `web_search_agent` (Google Search) |

## Project Structure

```
ucsc-student-services/
├── app/
│   ├── __init__.py
│   ├── agent.py                  # Root orchestrator + all workflow agents
│   ├── .env                      # Local environment config
│   └── corpus/                   # RAG source documents (8 files, 791 lines)
│       ├── cs-bs-requirements.md
│       ├── biology-biochem-requirements.md
│       ├── tuition-and-fees.md
│       ├── academic-calendar.md
│       ├── professors-and-advising.md
│       ├── ucsc-faq.md
│       ├── housing-and-dining.md
│       └── campus-map-and-buildings.md
├── deploy.py                     # Vertex AI Agent Engine deployment
├── Dockerfile                    # Cloud Run container
├── pyproject.toml
├── requirements.txt
└── README.md
```

## GCP Configuration

| Setting | Value |
|---------|-------|
| Project | `mygenerativeai` |
| Region | `us-central1` |
| Model | `gemini-2.5-flash` |
| Service Account | `web-hemli@mygenerativeai.iam.gserviceaccount.com` |
| APIs | `aiplatform`, `discoveryengine`, `generativelanguage` |

## Related

- [Enterprise Content Ops](../enterprise-content-ops/) — The CPE multi-agent system this project was modeled after
- [ADK Documentation](https://adk.dev) — Google Agent Development Kit
