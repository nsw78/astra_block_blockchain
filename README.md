# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063.svg)](https://docs.pydantic.dev/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178c6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Production--Ready-2496ed.svg)](https://www.docker.com/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088ff.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Portugues Brasileiro](README.pt-br.md) | [Espanol](README.es.md)

**AstraBlock** is an enterprise-grade blockchain analysis platform providing smart contract risk assessment and RAG-powered semantic document search. Built with a layered clean architecture, production-ready security, structured observability, and full Docker orchestration.

> **Disclaimer:** This is an educational project. Do not use results for financial decisions without professional validation.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Security](#security)
- [Observability](#observability)
- [Development](#development)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Core Capabilities

- **Smart Contract Risk Analysis** — Heuristic pattern detection on Ethereum contracts via Etherscan source code (ownership patterns, mint/burn functions, fee manipulation, transfer hooks)
- **RAG Semantic Search** — Retrieval-Augmented Generation with FAISS vector indexing and multi-backend embeddings (OpenAI, Sentence Transformers, TF-IDF fallback)
- **API Key Management** — Full CRUD lifecycle for user API keys with admin-only endpoints

### Enterprise-Grade Infrastructure

- **Layered Clean Architecture** — Core, API, Services, Repositories, Middleware, Models
- **Versioned REST API** — All endpoints under `/api/v1` with OpenAPI/Swagger documentation
- **Pydantic v2 Schemas** — Strict request/response validation with typed envelopes
- **App Factory Pattern** — `create_app()` with async lifespan context manager
- **Dependency Injection** — FastAPI `Depends()` for auth, config, and service resolution

### Security

- **API Key Authentication** — Constant-time comparison via `secrets.compare_digest()`
- **Admin/User Key Separation** — Two-tier auth with dedicated FastAPI dependencies
- **OWASP Security Headers** — HSTS, X-Frame-Options, nosniff, XSS protection, Permissions-Policy, Referrer-Policy
- **Rate Limiting** — Sliding-window limiter with `X-RateLimit-Limit` / `X-RateLimit-Remaining` headers
- **Non-Root Docker** — Dedicated `astra` user with minimal privileges
- **CORS Configuration** — Whitelist-based origin control

### Observability

- **Structured JSON Logging** — 12-factor compliant, single-line JSON per log entry
- **Request ID Tracing** — UUID correlation IDs via `X-Request-ID` header (propagated or generated)
- **Health Probes** — Liveness (`/health`) and readiness (`/readiness`) with dependency checks and latency metrics
- **Global Error Handling** — Consistent `ErrorResponse` envelope with error codes, request IDs, and safe 500 responses

### DevOps

- **Multi-Stage Docker Build** — Optimized image with builder pattern, Python 3.12-slim
- **Docker Compose Orchestration** — Backend + frontend with health-gated dependencies, resource limits, named volumes
- **Nginx Reverse Proxy** — Frontend routes `/api/` to backend, SPA fallback, gzip compression, static asset caching
- **GitHub Actions CI** — Lint (ruff) + Type Check (mypy) + Test (pytest) + Docker Build with smoke test

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │            Docker Compose               │
                        │                                         │
┌───────────┐     ┌─────┴──────────┐     ┌──────────────────┐    │
│  Browser   │────►│   Nginx        │────►│  FastAPI (ASGI)  │    │
│            │     │   :3003→:80    │     │  :8083→:8080     │    │
└───────────┘     │                │     │                  │    │
                  │  /api/* proxy  │     │  /api/v1/*       │    │
                  │  SPA fallback  │     │  Swagger /docs   │    │
                  └────────────────┘     └────────┬─────────┘    │
                                                  │              │
                                    ┌─────────────┴──────────┐   │
                                    │    Middleware Stack     │   │
                                    │  ┌───────────────────┐ │   │
                                    │  │ Security Headers  │ │   │
                                    │  │ Rate Limiter      │ │   │
                                    │  │ Request ID        │ │   │
                                    │  │ CORS              │ │   │
                                    │  │ Error Handler     │ │   │
                                    │  └───────────────────┘ │   │
                                    └─────────────┬──────────┘   │
                                                  │              │
                              ┌────────────────┬──┴───┬────────┐ │
                              ▼                ▼      ▼        ▼ │
                        ┌──────────┐  ┌─────────┐ ┌──────┐ ┌───┐│
                        │ Contract │  │ Indexer  │ │ Key  │ │...││
                        │ Service  │  │ Service  │ │ Svc  │ │   ││
                        └────┬─────┘  └────┬────┘ └──┬───┘ └───┘│
                             │             │         │           │
                        ┌────┴─────┐  ┌────┴────┐ ┌──┴───────┐  │
                        │Etherscan │  │  FAISS   │ │ SQLite   │  │
                        │   API    │  │  Index   │ │ (apikeys)│  │
                        └──────────┘  └─────────┘ └──────────┘  │
                                                                 │
                        Volume: astra-data (faiss.index, apikeys.db)
                        └─────────────────────────────────────────┘
```

### Layered Architecture

| Layer | Path | Responsibility |
|-------|------|----------------|
| **Core** | `app/core/` | Config, security, exceptions, logging |
| **API** | `app/api/v1/` | Versioned HTTP endpoints (routers) |
| **Services** | `app/services/` | Business logic (contract analysis, indexing, key management) |
| **Repositories** | `app/repositories/` | Data access (SQLite with WAL mode) |
| **Middleware** | `app/middleware/` | Cross-cutting concerns (rate limit, tracing, headers, errors) |
| **Models** | `app/models/` | Pydantic v2 request/response schemas |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI 0.115+ with async lifespan |
| **Validation** | Pydantic v2 + pydantic-settings |
| **Server** | Uvicorn (ASGI) |
| **Vector Index** | FAISS (IndexFlatL2) with disk persistence |
| **Embeddings** | OpenAI `text-embedding-3-small` / Sentence Transformers `all-MiniLM-L6-v2` / TF-IDF fallback |
| **Database** | SQLite with WAL mode |
| **Frontend** | React 18 + TypeScript + Tailwind CSS + Vite |
| **HTTP Client** | Axios (frontend) / httpx (backend) |
| **Reverse Proxy** | Nginx (Docker) |
| **Containerization** | Docker multi-stage + Docker Compose |
| **CI/CD** | GitHub Actions (4-stage pipeline) |
| **Linting** | Ruff (Python) + ESLint (TypeScript) |
| **Type Checking** | mypy (Python) + TypeScript strict |
| **Testing** | pytest + pytest-asyncio |

---

## Project Structure

```
astra_block_blockchain/
├── app/
│   ├── main.py                      # App factory, lifespan, middleware stack
│   ├── core/
│   │   ├── config.py                # Pydantic Settings (env validation)
│   │   ├── security.py              # Auth dependencies (verify_api_key, verify_admin_key)
│   │   ├── exceptions.py            # Exception hierarchy (401/403/404/422/429/502)
│   │   └── logging.py              # JSON/Text formatters, structured logging
│   ├── api/v1/
│   │   ├── router.py                # Route aggregator
│   │   └── endpoints/
│   │       ├── health.py            # /health, /readiness
│   │       ├── contracts.py         # /contracts/analyze
│   │       ├── documents.py         # /documents/search, /documents/
│   │       └── admin.py             # /admin/keys CRUD
│   ├── services/
│   │   ├── contract_service.py      # Etherscan fetch + heuristic analysis
│   │   ├── indexer_service.py       # Multi-backend vector indexing
│   │   └── apikey_service.py        # Key management logic
│   ├── repositories/
│   │   └── apikey_repository.py     # SQLite repository (WAL, thread-safe)
│   ├── middleware/
│   │   ├── rate_limiter.py          # Sliding-window rate limiter
│   │   ├── request_id.py            # UUID correlation IDs
│   │   ├── security_headers.py      # OWASP headers
│   │   └── error_handler.py         # Global error envelope
│   ├── models/
│   │   └── schemas.py               # All Pydantic v2 schemas
│   └── static/
│       └── favicon.svg              # AstraBlock favicon
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # Router + Layout
│   │   ├── api/astrablock.ts        # Typed API client (Axios)
│   │   ├── pages/
│   │   │   ├── Home.tsx             # Dashboard with stats and quick actions
│   │   │   ├── ContractAnalysis.tsx # Contract risk analysis UI
│   │   │   ├── RagSearch.tsx        # Semantic search UI
│   │   │   └── MarketOptions.tsx    # Options analysis (demo)
│   │   └── components/
│   │       └── Layout.tsx           # Sidebar navigation layout
│   ├── public/favicon.svg
│   ├── nginx.conf                   # Reverse proxy + SPA + gzip
│   └── Dockerfile                   # Multi-stage frontend build
├── tests/
│   ├── conftest.py                  # Session fixtures (TestClient, admin headers)
│   ├── test_health.py               # Health, readiness, headers, request IDs
│   ├── test_contracts.py            # Contract analysis validation
│   ├── test_documents.py            # RAG search and indexing
│   ├── test_admin.py                # Key CRUD + auth flows
│   ├── test_analyzer.py             # Service-level analysis tests
│   └── test_indexer.py              # IndexerService unit tests
├── docker-compose.yml               # Orchestration (API + Frontend)
├── Dockerfile                       # Multi-stage Python build
├── pyproject.toml                   # Ruff, mypy, pytest config
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .github/workflows/ci.yml         # CI pipeline
└── CLAUDE.md                        # Claude Code project context
```

---

## Prerequisites

- **Python 3.11+** (3.12 recommended)
- **Node.js 18+** (for frontend development)
- **Docker** and **Docker Compose**
- API keys (optional, for full functionality):
  - **Etherscan** — Contract source code fetching
  - **Infura/RPC** — Blockchain node access
  - **OpenAI** — Cloud embeddings (`text-embedding-3-small`)

---

## Quick Start

### Docker (Recommended)

```bash
# Clone
git clone https://github.com/yourusername/astrablock.git
cd astrablock

# Configure
cp .env.example .env
# Edit .env with your API keys (optional)

# Build and run
docker compose up --build -d

# Verify
curl http://localhost:8083/api/v1/health
# {"status":"ok","version":"1.0.0","environment":"development"}
```

| Service | URL |
|---------|-----|
| **API** | http://localhost:8083 |
| **Swagger Docs** | http://localhost:8083/docs |
| **ReDoc** | http://localhost:8083/redoc |
| **Frontend** | http://localhost:3003 |

### Local Development

```bash
# Backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Configuration

All configuration is managed via environment variables with validation at startup (fail-fast). See [.env.example](.env.example) for the full template.

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `production` / `staging` / `development` |
| `ADMIN_API_KEY` | — | Admin key for `/admin/*` endpoints |
| `OPENAI_API_KEY` | — | OpenAI embeddings (optional, falls back to local) |
| `ETHERSCAN_API_KEY` | — | Etherscan source code API |
| `RPC_URL` | `https://mainnet.infura.io/v3/...` | Ethereum RPC endpoint |
| `RATE_LIMIT_CALLS` | `120` | Max requests per window |
| `RATE_LIMIT_PERIOD` | `60` | Window size in seconds |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins (JSON array) |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `LOG_FORMAT` | `json` | `json` (structured) or `text` (human-readable) |
| `FAISS_INDEX_PATH` | `./data/faiss.index` | Vector index persistence path |
| `APIKEY_DB_PATH` | `./data/apikeys.db` | SQLite database path |
| `API_PORT` | `8083` | Docker host port for API |
| `FRONTEND_PORT` | `3003` | Docker host port for frontend |

### Embedding Backend Priority

The indexer automatically selects the best available embedding backend:

1. **OpenAI** (`text-embedding-3-small`) — if `OPENAI_API_KEY` is set
2. **Sentence Transformers** (`all-MiniLM-L6-v2`) — local, no API key needed
3. **TF-IDF** — final fallback, no dependencies beyond sklearn

---

## API Reference

All endpoints are prefixed with `/api/v1`. Interactive documentation available at `/docs` (development only).

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Liveness probe |
| `GET` | `/api/v1/readiness` | Readiness probe (checks indexer + database) |
| `GET` | `/api/v1/contracts/analyze?address=0x...` | Smart contract risk analysis |
| `GET` | `/api/v1/documents/search?q=query&k=5` | RAG semantic search |

### Authenticated Endpoints (API Key)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/documents/` | Index new documents |
| `GET` | `/api/v1/documents/` | List indexed documents |

### Admin Endpoints (Admin Key)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/admin/keys` | Create user API key |
| `GET` | `/api/v1/admin/keys` | List all API keys |
| `DELETE` | `/api/v1/admin/keys/{key}` | Revoke an API key |

### Authentication

```bash
# User endpoint (X-API-Key header)
curl -H "X-API-Key: your-user-key" http://localhost:8083/api/v1/documents/

# Admin endpoint
curl -H "X-API-Key: your-admin-key" http://localhost:8083/api/v1/admin/keys

# Create a user key (admin)
curl -X POST -H "X-API-Key: your-admin-key" \
     -H "Content-Type: application/json" \
     -d '{"name": "my-app"}' \
     http://localhost:8083/api/v1/admin/keys
```

### Example: Analyze a Contract

```bash
curl "http://localhost:8083/api/v1/contracts/analyze?address=0xdAC17F958D2ee523a2206206994597C13D831ec7"
```

```json
{
  "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "source_available": true,
  "analysis": {
    "score": 40,
    "findings": [
      { "pattern": "owner", "snippet": "address public owner;" },
      { "pattern": "transferOwnership", "snippet": "function transferOwnership(address newOwner)..." },
      { "pattern": "mint", "snippet": "function issue(uint amount)..." },
      { "pattern": "burn", "snippet": "function redeem(uint amount)..." }
    ],
    "error": null
  }
}
```

### Error Envelope

All errors follow a consistent format:

```json
{
  "success": false,
  "error_code": "AUTHENTICATION_ERROR",
  "message": "Missing or invalid API key",
  "details": null,
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `AUTHENTICATION_ERROR` | 401 | Missing or invalid API key |
| `AUTHORIZATION_ERROR` | 403 | Insufficient permissions (admin required) |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `EXTERNAL_SERVICE_ERROR` | 502 | Third-party service failure (Etherscan, OpenAI) |
| `INTERNAL_ERROR` | 500 | Unhandled server error |

---

## Security

### Authentication Model

```
Request → X-API-Key header
  │
  ├─ Admin endpoints → verify_admin_key() → secrets.compare_digest(key, ADMIN_API_KEY)
  │
  └─ User endpoints  → verify_api_key()   → compare admin key OR check SQLite repository
```

### Security Headers (all responses)

| Header | Value |
|--------|-------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Cache-Control` | `no-store` |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=()` |

### Rate Limiting

- Sliding-window algorithm keyed by API key or client IP
- Configurable via `RATE_LIMIT_CALLS` and `RATE_LIMIT_PERIOD`
- Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Health/readiness probes are excluded from rate limiting

### Production Hardening

- Swagger/ReDoc/OpenAPI disabled in production (`ENVIRONMENT=production`)
- Non-root Docker user (`astra`) with no shell
- Resource limits enforced via Docker Compose (1GB RAM, 1 CPU)
- Named volumes for data persistence across container restarts

---

## Observability

### Structured Logging

Every log entry is a single JSON line (12-factor compliant):

```json
{
  "timestamp": "2026-02-27T21:12:54.123456Z",
  "level": "INFO",
  "logger": "astra.service.contract",
  "message": "Contract analysis complete",
  "request_id": "a1b2c3d4-...",
  "extra_data": { "address": "0xdAC1...", "score": 40 }
}
```

### Request Tracing

- Every request gets a UUID `X-Request-ID` (generated or propagated from client)
- Request ID is attached to all log entries via `ContextVar`
- Returned in response headers for end-to-end correlation

### Health Probes

```bash
# Liveness (is the process alive?)
GET /api/v1/health → {"status":"ok","version":"1.0.0","environment":"development"}

# Readiness (are dependencies healthy?)
GET /api/v1/readiness → {
  "status": "ok",
  "checks": [
    {"name": "indexer", "status": "ok", "latency_ms": null},
    {"name": "database", "status": "ok", "latency_ms": 2.39}
  ]
}
```

---

## Development

### Code Quality

```bash
# Lint (Python)
ruff check .
ruff format --check .

# Type check
mypy app/

# Run all checks
ruff check . && ruff format --check . && mypy app/ && pytest
```

### Tooling Configuration

All tools are configured in [pyproject.toml](pyproject.toml):

- **Ruff**: Line length 120, rules E/F/W/I/N/UP/B/SIM
- **mypy**: Python 3.12, `warn_return_any`, `ignore_missing_imports`
- **pytest**: Test directory `tests/`, async mode auto

---

## Testing

```bash
# Run all tests
pytest

# With verbose output
pytest -v

# Specific test file
pytest tests/test_health.py
```

### Test Suite

| File | Coverage |
|------|----------|
| `test_health.py` | Health, readiness, security headers, request ID propagation |
| `test_contracts.py` | Address validation, analysis pipeline, service layer |
| `test_documents.py` | RAG search, document indexing, auth enforcement |
| `test_admin.py` | Key CRUD lifecycle, admin auth, user key flow |
| `test_analyzer.py` | Contract service with pattern detection |
| `test_indexer.py` | IndexerService add/search/count |

---

## CI/CD Pipeline

The [GitHub Actions workflow](.github/workflows/ci.yml) runs a 4-stage pipeline:

```
Lint (ruff) ──► Type Check (mypy) ──► Test (pytest) ──► Docker Build + Smoke Test
```

| Stage | Tool | Description |
|-------|------|-------------|
| **Lint** | ruff | Format check + linting (PEP 8, imports, naming, modernization) |
| **Type Check** | mypy | Static type analysis |
| **Test** | pytest | Full integration test suite |
| **Docker** | docker build | Multi-stage build + health check smoke test |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Follow existing code patterns (layered architecture, Pydantic schemas, typed services)
4. Add tests for new endpoints/services
5. Ensure all checks pass: `ruff check . && mypy app/ && pytest`
6. Commit your changes: `git commit -m 'feat: add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
