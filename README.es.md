# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063.svg)](https://docs.pydantic.dev/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178c6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Production--Ready-2496ed.svg)](https://www.docker.com/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088ff.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [Portugues Brasileiro](README.pt-br.md)

**AstraBlock** es una plataforma enterprise-grade de analisis blockchain que ofrece evaluacion de riesgo de contratos inteligentes y busqueda semantica de documentos con RAG. Construida con arquitectura limpia en capas, seguridad lista para produccion, observabilidad estructurada y orquestacion Docker completa.

> **Advertencia:** Este es un proyecto educativo. No use los resultados para decisiones financieras sin validacion profesional.

---

## Indice

- [Funcionalidades](#funcionalidades)
- [Arquitectura](#arquitectura)
- [Stack Tecnologico](#stack-tecnologico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Prerrequisitos](#prerrequisitos)
- [Inicio Rapido](#inicio-rapido)
- [Configuracion](#configuracion)
- [Referencia de la API](#referencia-de-la-api)
- [Seguridad](#seguridad)
- [Observabilidad](#observabilidad)
- [Desarrollo](#desarrollo)
- [Pruebas](#pruebas)
- [Pipeline CI/CD](#pipeline-cicd)
- [Contribucion](#contribucion)
- [Licencia](#licencia)

---

## Funcionalidades

### Capacidades Principales

- **Analisis de Riesgo de Contratos Inteligentes** — Deteccion heuristica de patrones en contratos Ethereum via codigo fuente de Etherscan (patrones de ownership, funciones mint/burn, manipulacion de tasas, hooks de transferencia)
- **Busqueda Semantica RAG** — Retrieval-Augmented Generation con indexacion vectorial FAISS y embeddings multi-backend (OpenAI, Sentence Transformers, fallback TF-IDF)
- **Gestion de Claves de API** — Ciclo CRUD completo para claves de usuario con endpoints exclusivos de admin

### Infraestructura Enterprise-Grade

- **Arquitectura Limpia en Capas** — Core, API, Services, Repositories, Middleware, Models
- **API REST Versionada** — Todos los endpoints bajo `/api/v1` con documentacion OpenAPI/Swagger
- **Schemas Pydantic v2** — Validacion rigurosa de request/response con envoltorios tipados
- **Patron App Factory** — `create_app()` con gestor de contexto async lifespan
- **Inyeccion de Dependencias** — FastAPI `Depends()` para auth, config y resolucion de servicios

### Seguridad

- **Autenticacion por Clave de API** — Comparacion en tiempo constante via `secrets.compare_digest()`
- **Separacion Admin/Usuario** — Auth de dos niveles con dependencias FastAPI dedicadas
- **Headers de Seguridad OWASP** — HSTS, X-Frame-Options, nosniff, proteccion XSS, Permissions-Policy, Referrer-Policy
- **Rate Limiting** — Limitador de ventana deslizante con headers `X-RateLimit-Limit` / `X-RateLimit-Remaining`
- **Docker Non-Root** — Usuario `astra` dedicado con privilegios minimos
- **Configuracion CORS** — Control de origen basado en whitelist

### Observabilidad

- **Logging JSON Estructurado** — Compatible con 12-factor, JSON en linea unica por entrada de log
- **Rastreo de Request ID** — IDs de correlacion UUID via header `X-Request-ID` (propagado o generado)
- **Health Probes** — Liveness (`/health`) y readiness (`/readiness`) con verificacion de dependencias y metricas de latencia
- **Manejo Global de Errores** — Envoltorio `ErrorResponse` consistente con codigos de error, request IDs y respuestas 500 seguras

### DevOps

- **Build Docker Multi-Stage** — Imagen optimizada con patron builder, Python 3.12-slim
- **Orquestacion Docker Compose** — Backend + frontend con dependencias controladas por health, limites de recursos, volumenes nombrados
- **Proxy Reverso Nginx** — Frontend enruta `/api/` al backend, fallback SPA, compresion gzip, cache de assets estaticos
- **CI GitHub Actions** — Lint (ruff) + Type Check (mypy) + Test (pytest) + Docker Build con smoke test

---

## Arquitectura

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

### Arquitectura en Capas

| Capa | Ruta | Responsabilidad |
|------|------|-----------------|
| **Core** | `app/core/` | Config, seguridad, excepciones, logging |
| **API** | `app/api/v1/` | Endpoints HTTP versionados (routers) |
| **Services** | `app/services/` | Logica de negocio (analisis de contratos, indexacion, gestion de claves) |
| **Repositories** | `app/repositories/` | Acceso a datos (SQLite con modo WAL) |
| **Middleware** | `app/middleware/` | Preocupaciones transversales (rate limit, tracing, headers, errores) |
| **Models** | `app/models/` | Schemas Pydantic v2 de request/response |

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|-----------|
| **Framework API** | FastAPI 0.115+ con async lifespan |
| **Validacion** | Pydantic v2 + pydantic-settings |
| **Servidor** | Uvicorn (ASGI) |
| **Indice Vectorial** | FAISS (IndexFlatL2) con persistencia en disco |
| **Embeddings** | OpenAI `text-embedding-3-small` / Sentence Transformers `all-MiniLM-L6-v2` / fallback TF-IDF |
| **Base de Datos** | SQLite con modo WAL |
| **Frontend** | React 18 + TypeScript + Tailwind CSS + Vite |
| **Cliente HTTP** | Axios (frontend) / httpx (backend) |
| **Proxy Reverso** | Nginx (Docker) |
| **Containerizacion** | Docker multi-stage + Docker Compose |
| **CI/CD** | GitHub Actions (pipeline de 4 etapas) |
| **Linting** | Ruff (Python) + ESLint (TypeScript) |
| **Type Checking** | mypy (Python) + TypeScript strict |
| **Pruebas** | pytest + pytest-asyncio |

---

## Estructura del Proyecto

```
astra_block_blockchain/
├── app/
│   ├── main.py                      # App factory, lifespan, middleware stack
│   ├── core/
│   │   ├── config.py                # Pydantic Settings (validacion de env)
│   │   ├── security.py              # Dependencias de auth (verify_api_key, verify_admin_key)
│   │   ├── exceptions.py            # Jerarquia de excepciones (401/403/404/422/429/502)
│   │   └── logging.py              # Formatters JSON/Text, logging estructurado
│   ├── api/v1/
│   │   ├── router.py                # Agregador de rutas
│   │   └── endpoints/
│   │       ├── health.py            # /health, /readiness
│   │       ├── contracts.py         # /contracts/analyze
│   │       ├── documents.py         # /documents/search, /documents/
│   │       └── admin.py             # /admin/keys CRUD
│   ├── services/
│   │   ├── contract_service.py      # Fetch Etherscan + analisis heuristico
│   │   ├── indexer_service.py       # Indexacion vectorial multi-backend
│   │   └── apikey_service.py        # Logica de gestion de claves
│   ├── repositories/
│   │   └── apikey_repository.py     # Repositorio SQLite (WAL, thread-safe)
│   ├── middleware/
│   │   ├── rate_limiter.py          # Rate limiter de ventana deslizante
│   │   ├── request_id.py            # IDs de correlacion UUID
│   │   ├── security_headers.py      # Headers OWASP
│   │   └── error_handler.py         # Envoltorio global de errores
│   ├── models/
│   │   └── schemas.py               # Todos schemas Pydantic v2
│   └── static/
│       └── favicon.svg              # Favicon AstraBlock
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # Router + Layout
│   │   ├── api/astrablock.ts        # Cliente API tipado (Axios)
│   │   ├── pages/
│   │   │   ├── Home.tsx             # Dashboard con stats y acciones rapidas
│   │   │   ├── ContractAnalysis.tsx # UI de analisis de riesgo de contratos
│   │   │   ├── RagSearch.tsx        # UI de busqueda semantica
│   │   │   └── MarketOptions.tsx    # Analisis de opciones (demo)
│   │   └── components/
│   │       └── Layout.tsx           # Layout con navegacion lateral
│   ├── public/favicon.svg
│   ├── nginx.conf                   # Proxy reverso + SPA + gzip
│   └── Dockerfile                   # Build multi-stage del frontend
├── tests/
│   ├── conftest.py                  # Fixtures de sesion (TestClient, admin headers)
│   ├── test_health.py               # Health, readiness, headers, request IDs
│   ├── test_contracts.py            # Validacion de analisis de contratos
│   ├── test_documents.py            # Busqueda RAG e indexacion
│   ├── test_admin.py                # CRUD de claves + flujos de auth
│   ├── test_analyzer.py             # Tests de servicio de analisis
│   └── test_indexer.py              # Tests unitarios del IndexerService
├── docker-compose.yml               # Orquestacion (API + Frontend)
├── Dockerfile                       # Build multi-stage Python
├── pyproject.toml                   # Config de Ruff, mypy, pytest
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Template de variables de entorno
├── .github/workflows/ci.yml         # Pipeline CI
└── CLAUDE.md                        # Contexto del proyecto para Claude Code
```

---

## Prerrequisitos

- **Python 3.11+** (3.12 recomendado)
- **Node.js 18+** (para desarrollo del frontend)
- **Docker** y **Docker Compose**
- Claves de API (opcional, para funcionalidad completa):
  - **Etherscan** — Busqueda de codigo fuente de contratos
  - **Infura/RPC** — Acceso a nodo blockchain
  - **OpenAI** — Embeddings en la nube (`text-embedding-3-small`)

---

## Inicio Rapido

### Docker (Recomendado)

```bash
# Clonar
git clone https://github.com/yourusername/astrablock.git
cd astrablock

# Configurar
cp .env.example .env
# Edita .env con tus claves de API (opcional)

# Build y ejecucion
docker compose up --build -d

# Verificar
curl http://localhost:8083/api/v1/health
# {"status":"ok","version":"1.0.0","environment":"development"}
```

| Servicio | URL |
|----------|-----|
| **API** | http://localhost:8083 |
| **Swagger Docs** | http://localhost:8083/docs |
| **ReDoc** | http://localhost:8083/redoc |
| **Frontend** | http://localhost:3003 |

### Desarrollo Local

```bash
# Backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

# Frontend (terminal separada)
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Configuracion

Toda la configuracion se gestiona via variables de entorno con validacion al inicio (fail-fast). Consulta [.env.example](.env.example) para el template completo.

| Variable | Defecto | Descripcion |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `production` / `staging` / `development` |
| `ADMIN_API_KEY` | — | Clave admin para endpoints `/admin/*` |
| `OPENAI_API_KEY` | — | Embeddings OpenAI (opcional, fallback a local) |
| `ETHERSCAN_API_KEY` | — | API de codigo fuente de Etherscan |
| `RPC_URL` | `https://mainnet.infura.io/v3/...` | Endpoint RPC Ethereum |
| `RATE_LIMIT_CALLS` | `120` | Max peticiones por ventana |
| `RATE_LIMIT_PERIOD` | `60` | Tamano de ventana en segundos |
| `CORS_ORIGINS` | `["*"]` | Origenes CORS permitidos (array JSON) |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `LOG_FORMAT` | `json` | `json` (estructurado) o `text` (legible) |
| `FAISS_INDEX_PATH` | `./data/faiss.index` | Ruta de persistencia del indice vectorial |
| `APIKEY_DB_PATH` | `./data/apikeys.db` | Ruta de base de datos SQLite |
| `API_PORT` | `8083` | Puerto Docker host para API |
| `FRONTEND_PORT` | `3003` | Puerto Docker host para frontend |

### Prioridad del Backend de Embeddings

El indexador selecciona automaticamente el mejor backend disponible:

1. **OpenAI** (`text-embedding-3-small`) — si `OPENAI_API_KEY` esta configurada
2. **Sentence Transformers** (`all-MiniLM-L6-v2`) — local, sin necesidad de clave
3. **TF-IDF** — fallback final, sin dependencias mas alla de sklearn

---

## Referencia de la API

Todos los endpoints estan prefijados con `/api/v1`. Documentacion interactiva disponible en `/docs` (solo desarrollo).

### Endpoints Publicos

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Probe de liveness |
| `GET` | `/api/v1/readiness` | Probe de readiness (verifica indexer + base de datos) |
| `GET` | `/api/v1/contracts/analyze?address=0x...` | Analisis de riesgo de contrato inteligente |
| `GET` | `/api/v1/documents/search?q=query&k=5` | Busqueda semantica RAG |

### Endpoints Autenticados (Clave de API)

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| `POST` | `/api/v1/documents/` | Indexar nuevos documentos |
| `GET` | `/api/v1/documents/` | Listar documentos indexados |

### Endpoints Admin (Clave Admin)

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| `POST` | `/api/v1/admin/keys` | Crear clave de API de usuario |
| `GET` | `/api/v1/admin/keys` | Listar todas las claves |
| `DELETE` | `/api/v1/admin/keys/{key}` | Revocar una clave |

### Autenticacion

```bash
# Endpoint de usuario (header X-API-Key)
curl -H "X-API-Key: tu-clave-usuario" http://localhost:8083/api/v1/documents/

# Endpoint admin
curl -H "X-API-Key: tu-clave-admin" http://localhost:8083/api/v1/admin/keys

# Crear clave de usuario (admin)
curl -X POST -H "X-API-Key: tu-clave-admin" \
     -H "Content-Type: application/json" \
     -d '{"name": "mi-app"}' \
     http://localhost:8083/api/v1/admin/keys
```

### Ejemplo: Analizar un Contrato

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

### Envoltorio de Error

Todos los errores siguen un formato consistente:

```json
{
  "success": false,
  "error_code": "AUTHENTICATION_ERROR",
  "message": "Missing or invalid API key",
  "details": null,
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

| Codigo de Error | HTTP Status | Descripcion |
|-----------------|-------------|-------------|
| `AUTHENTICATION_ERROR` | 401 | Clave de API ausente o invalida |
| `AUTHORIZATION_ERROR` | 403 | Permisos insuficientes (admin requerido) |
| `NOT_FOUND` | 404 | Recurso no encontrado |
| `VALIDATION_ERROR` | 422 | Fallo en validacion de la peticion |
| `RATE_LIMIT_EXCEEDED` | 429 | Demasiadas peticiones |
| `EXTERNAL_SERVICE_ERROR` | 502 | Fallo en servicio externo (Etherscan, OpenAI) |
| `INTERNAL_ERROR` | 500 | Error interno del servidor |

---

## Seguridad

### Modelo de Autenticacion

```
Request → Header X-API-Key
  │
  ├─ Endpoints admin → verify_admin_key() → secrets.compare_digest(key, ADMIN_API_KEY)
  │
  └─ Endpoints usuario → verify_api_key() → compara clave admin O verifica repositorio SQLite
```

### Headers de Seguridad (todas las respuestas)

| Header | Valor |
|--------|-------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Cache-Control` | `no-store` |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=()` |

### Rate Limiting

- Algoritmo de ventana deslizante con clave por API key o IP del cliente
- Configurable via `RATE_LIMIT_CALLS` y `RATE_LIMIT_PERIOD`
- Headers de respuesta: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Probes de health/readiness excluidos del rate limiting

### Hardening para Produccion

- Swagger/ReDoc/OpenAPI deshabilitados en produccion (`ENVIRONMENT=production`)
- Usuario Docker non-root (`astra`) sin shell
- Limites de recursos via Docker Compose (1GB RAM, 1 CPU)
- Volumenes nombrados para persistencia de datos entre reinicios

---

## Observabilidad

### Logging Estructurado

Cada entrada de log es una unica linea JSON (compatible 12-factor):

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

### Rastreo de Peticiones

- Cada peticion recibe un UUID `X-Request-ID` (generado o propagado del cliente)
- Request ID se adjunta a todas las entradas de log via `ContextVar`
- Retornado en headers de respuesta para correlacion end-to-end

### Health Probes

```bash
# Liveness (el proceso esta vivo?)
GET /api/v1/health → {"status":"ok","version":"1.0.0","environment":"development"}

# Readiness (las dependencias estan saludables?)
GET /api/v1/readiness → {
  "status": "ok",
  "checks": [
    {"name": "indexer", "status": "ok", "latency_ms": null},
    {"name": "database", "status": "ok", "latency_ms": 2.39}
  ]
}
```

---

## Desarrollo

### Calidad de Codigo

```bash
# Lint (Python)
ruff check .
ruff format --check .

# Type check
mypy app/

# Ejecutar todas las verificaciones
ruff check . && ruff format --check . && mypy app/ && pytest
```

### Configuracion de Herramientas

Todas las herramientas configuradas en [pyproject.toml](pyproject.toml):

- **Ruff**: Line length 120, reglas E/F/W/I/N/UP/B/SIM
- **mypy**: Python 3.12, `warn_return_any`, `ignore_missing_imports`
- **pytest**: Directorio de pruebas `tests/`, modo async auto

---

## Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Con salida detallada
pytest -v

# Archivo de prueba especifico
pytest tests/test_health.py
```

### Suite de Pruebas

| Archivo | Cobertura |
|---------|-----------|
| `test_health.py` | Health, readiness, headers de seguridad, propagacion de request ID |
| `test_contracts.py` | Validacion de direccion, pipeline de analisis, capa de servicio |
| `test_documents.py` | Busqueda RAG, indexacion de documentos, enforcement de auth |
| `test_admin.py` | Ciclo CRUD de claves, auth admin, flujo de clave de usuario |
| `test_analyzer.py` | Servicio de contratos con deteccion de patrones |
| `test_indexer.py` | IndexerService add/search/count |

---

## Pipeline CI/CD

El [workflow de GitHub Actions](.github/workflows/ci.yml) ejecuta un pipeline de 4 etapas:

```
Lint (ruff) ──► Type Check (mypy) ──► Test (pytest) ──► Docker Build + Smoke Test
```

| Etapa | Herramienta | Descripcion |
|-------|-----------|-------------|
| **Lint** | ruff | Verificacion de formato + linting (PEP 8, imports, naming, modernizacion) |
| **Type Check** | mypy | Analisis estatico de tipos |
| **Test** | pytest | Suite completa de pruebas de integracion |
| **Docker** | docker build | Build multi-stage + smoke test de health check |

---

## Contribucion

1. Haz un fork del repositorio
2. Crea una rama de feature: `git checkout -b feature/funcionalidad-increible`
3. Sigue los patrones de codigo existentes (arquitectura en capas, schemas Pydantic, servicios tipados)
4. Agrega pruebas para nuevos endpoints/servicios
5. Asegura que todas las verificaciones pasen: `ruff check . && mypy app/ && pytest`
6. Confirma tus cambios: `git commit -m 'feat: agrega funcionalidad increible'`
7. Push a la rama: `git push origin feature/funcionalidad-increible`
8. Abre un Pull Request

---

## Licencia

Este proyecto esta licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para mas detalles.
