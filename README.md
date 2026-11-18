# BENV — AI-Native Built Environment Design Platform

> An AI-native professional platform for designing, analyzing, and optimizing the physical world.

---

## What Is This?

BENV is a production-oriented AI design platform for architects, engineers, and developers.
It allows users to design buildings and infrastructure using natural language, AI-assisted generation,
2D/3D editing, BIM, and eventually site intelligence and historical construction knowledge.

The platform is NOT an image generator. It is a structured design system where AI understands,
generates, and edits real building models.

---

## Current Status

Phase 1 — Project Foundation (IN PROGRESS)

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full development roadmap.

---

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker + Docker Compose
- PostgreSQL 16 (via Docker)

### Setup

```bash
# Clone and enter directory
cd benv

# Backend
cd apps/api
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Frontend
cd apps/web
npm install
npm run dev

# Full stack (recommended)
docker compose up
```

### Run Tests

```bash
# Backend
cd apps/api
pytest -v

# Frontend
cd apps/web
npm test
```

---

## Documentation

| Document | Description |
|---|---|
| [PROJECT_VISION.md](docs/PROJECT_VISION.md) | Product vision, philosophy, and long-term goals |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical system architecture |
| [ROADMAP.md](docs/ROADMAP.md) | Development roadmap, 20 phases |
| [DECISIONS.md](docs/DECISIONS.md) | Architectural Decision Records (ADRs) |
| [DEVELOPMENT_RULES.md](docs/DEVELOPMENT_RULES.md) | Engineering standards and rules |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Three.js, Zustand |
| Backend | Python 3.11, FastAPI, Pydantic v2 |
| Database | PostgreSQL 16 + PostGIS + pgvector |
| AI | Abstracted provider layer (Google Gemini default) |
| BIM | IfcOpenShell, IFC 4 |
| Geometry | Shapely, custom constraint engine |
| Infrastructure | Docker, GitHub Actions |
| Monitoring | Prometheus, Grafana (Phase 19) |

---

## Core Design Principles

1. **Single Source of Truth** — One master building model drives 2D, 3D, BIM, schedules.
2. **AI Proposes, Solvers Validate** — Never fabricate engineering results.
3. **Structured Over Generative** — Design model is structured data, not images.
4. **Provider-Agnostic AI** — No lock-in to any single LLM provider.
5. **Incremental Construction** — Build each phase correctly before moving to the next.

---

## License

Proprietary — All rights reserved. See LICENSE for details.

## Status

Early development. Not production-ready.
