# AstraBlock — Project Guide

## What is this?
Enterprise-grade FastAPI backend for blockchain smart-contract risk analysis and RAG (Retrieval-Augmented Generation) document search. React frontend with Vite + TailwindCSS.

## Architecture
```
app/
  main.py              # App factory (create_app) with lifespan
  core/                # Config, security, exceptions, structured logging
  api/v1/              # Versioned HTTP endpoints (health, contracts, documents, admin)
  services/            # Business logic (contract_service, indexer_service, apikey_service)
  repositories/        # Data access (apikey_repository — SQLite)
  middleware/           # Rate limiter, request ID, error handler, security headers
  models/              # Pydantic v2 request/response schemas
```

## Key Commands
- **Run dev server**: `uvicorn app.main:app --reload --port 8080`
- **Run tests**: `pytest`
- **Lint**: `ruff check .`
- **Type check**: `mypy app/ --ignore-missing-imports`
- **Docker**: `docker compose up --build`

## API Versioning
All endpoints are under `/api/v1/`. Swagger docs at `/docs` (disabled in production).

## Environment
Configured via `.env` file — see `.env.example`. Key vars:
- `ENVIRONMENT` (production/staging/development)
- `ADMIN_API_KEY` — required for `/api/v1/admin/*` endpoints
- `ETHERSCAN_API_KEY` — for contract source fetching
- `OPENAI_API_KEY` — for embedding generation (optional, falls back to sentence-transformers or TF-IDF)

## Conventions
- Pydantic v2 for all schemas
- FastAPI dependency injection for auth
- JSON structured logging in production
- All errors return `{ success, error_code, message, details, request_id }`
