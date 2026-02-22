# Sahayak — AI Workflow Automation Platform

> Built for Smart India Hackathon 2025 | Led a team of 4 | Python • FastAPI • LangChain • PostgreSQL • Docker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](Dockerfile)

---

## What is Sahayak?

Sahayak is an AI-powered workflow automation platform that turns manual, repetitive business processes into intelligent, automated pipelines using natural language understanding.

Instead of configuring rigid rule-based automations, users describe what they want in plain language. Sahayak classifies the intent, routes to the right workflow, executes it, and returns a result — all with built-in fallback handling when AI confidence is low.

**15+ workflow types automated. 70% reduction in task completion time. 99.2% uptime under 24-hour stress testing.**

---

## Demo

> https://www.youtube.com/watch?v=PgYZooBt1YM&t=10s
---

## Key Metrics

| Metric | Result |
|--------|--------|
| Concurrent requests handled | 500+ |
| Uptime (24-hour stress test) | 99.2% |
| Task completion time reduction | 70% (10+ min → ~3 min avg) |
| Workflow types automated | 15+ |
| AI classification accuracy | 95%+ |
| API call reduction (prompt caching) | 60% |

---

## Architecture

```
User Request
     │
     ▼
FastAPI (Async)
     │
     ▼
Request Queue (async queue-based processing)
     │
     ▼
LangChain Orchestration Layer
  ├── HuggingFace Model (intent classification)
  ├── Confidence Scoring
  └── Fallback Handler (if confidence < threshold)
     │
     ▼
Workflow Router
  ├── Workflow Executor (15+ types)
  └── PostgreSQL (state, logs, results)
     │
     ▼
Response to User
```

### Why Async Queue-Based Architecture?

4 weeks before the deadline, synchronous LLM calls were timing out 15–20% of requests under load. I made the decision to redesign the entire request pipeline to async queue-based processing — rewriting 40% of the backend in 2 weeks.

**Result:** Timeouts dropped to <0.1%. Uptime hit 99.2% under stress testing.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI (async) |
| AI Orchestration | LangChain, HuggingFace |
| Database | PostgreSQL |
| Containerization | Docker |
| Version Control | Git / GitHub |
| Testing | Automated integration tests |

---

## Features

- **Natural Language Workflow Triggering** — describe a task, Sahayak routes it
- **AI Classification with Confidence Scoring** — unreliable outputs are caught before execution
- **Fallback Mechanisms** — graceful degradation when AI confidence is below threshold
- **Prompt Caching** — reduces LLM API calls by 60%
- **Async Processing** — handles LLM latency without blocking requests
- **Real-time Status Tracking** — monitor workflow execution state
- **Comprehensive Logging** — full observability into execution and failures

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- PostgreSQL
- HuggingFace API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Sarthak816/sahayak.git
cd sahayak

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database config
```

### Run with Docker

```bash
docker-compose up --build
```

### Run Locally

```bash
# Start PostgreSQL
# Apply database migrations
python migrate.py

# Start the server
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

---

## API Overview

```
POST /workflow/trigger     — Submit a workflow request
GET  /workflow/{id}/status — Check execution status
GET  /workflows            — List available workflow types
GET  /health               — Health check
```

---

## Project Background

Built during **Smart India Hackathon 2025** as Team Leader of a 4-person engineering team.

**Role:** System architecture, backend development, LangChain integration, team coordination, and presentation to national-level judges.

**Critical Decision Made:** Midway through development, I identified that synchronous LLM calls would make the system unreliable at scale. Despite the deadline pressure, I led a full async architecture redesign — splitting the backend rewrite across two parallel workstreams while keeping the rest of the team unblocked.

---

## What I Learned

- AI features require reliable infrastructure, not just smart models
- Design explicitly for AI's unreliability: confidence scores, overrides, fallbacks
- Async architecture is non-negotiable when LLM latency is in the critical path
- Leadership under pressure means making hard calls fast and explaining why clearly

