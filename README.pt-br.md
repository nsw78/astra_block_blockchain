# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063.svg)](https://docs.pydantic.dev/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178c6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Production--Ready-2496ed.svg)](https://www.docker.com/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088ff.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [Espanol](README.es.md)

**AstraBlock** e uma plataforma enterprise-grade de analise blockchain que oferece avaliacao de risco de contratos inteligentes e busca semantica de documentos com RAG. Construido com arquitetura limpa em camadas, seguranca pronta para producao, observabilidade estruturada e orquestracao Docker completa.

> **Aviso:** Este e um projeto educacional. Nao use os resultados para decisoes financeiras sem validacao profissional.

---

## Indice

- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Stack Tecnologica](#stack-tecnologica)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pre-requisitos](#pre-requisitos)
- [Inicio Rapido](#inicio-rapido)
- [Configuracao](#configuracao)
- [Referencia da API](#referencia-da-api)
- [Seguranca](#seguranca)
- [Observabilidade](#observabilidade)
- [Desenvolvimento](#desenvolvimento)
- [Testes](#testes)
- [Pipeline CI/CD](#pipeline-cicd)
- [Contribuicao](#contribuicao)
- [Licenca](#licenca)

---

## Funcionalidades

### Capacidades Principais

- **Analise de Risco de Contratos Inteligentes** — Deteccao heuristica de padroes em contratos Ethereum via codigo-fonte do Etherscan (padroes de ownership, funcoes mint/burn, manipulacao de taxas, hooks de transferencia)
- **Busca Semantica RAG** — Retrieval-Augmented Generation com indexacao vetorial FAISS e embeddings multi-backend (OpenAI, Sentence Transformers, fallback TF-IDF)
- **Gerenciamento de Chaves de API** — Ciclo CRUD completo para chaves de usuario com endpoints exclusivos de admin

### Infraestrutura Enterprise-Grade

- **Arquitetura Limpa em Camadas** — Core, API, Services, Repositories, Middleware, Models
- **API REST Versionada** — Todos endpoints sob `/api/v1` com documentacao OpenAPI/Swagger
- **Schemas Pydantic v2** — Validacao rigorosa de request/response com envelopes tipados
- **Padrao App Factory** — `create_app()` com gerenciador de contexto async lifespan
- **Injecao de Dependencias** — FastAPI `Depends()` para auth, config e resolucao de servicos

### Seguranca

- **Autenticacao por Chave de API** — Comparacao em tempo constante via `secrets.compare_digest()`
- **Separacao Admin/Usuario** — Auth de dois niveis com dependencias FastAPI dedicadas
- **Headers de Seguranca OWASP** — HSTS, X-Frame-Options, nosniff, protecao XSS, Permissions-Policy, Referrer-Policy
- **Rate Limiting** — Limitador de janela deslizante com headers `X-RateLimit-Limit` / `X-RateLimit-Remaining`
- **Docker Non-Root** — Usuario `astra` dedicado com privilegios minimos
- **Configuracao CORS** — Controle de origem baseado em whitelist

### Observabilidade

- **Logging JSON Estruturado** — Compativel com 12-factor, JSON em linha unica por entrada de log
- **Rastreamento de Request ID** — IDs de correlacao UUID via header `X-Request-ID` (propagado ou gerado)
- **Health Probes** — Liveness (`/health`) e readiness (`/readiness`) com verificacao de dependencias e metricas de latencia
- **Tratamento Global de Erros** — Envelope `ErrorResponse` consistente com codigos de erro, request IDs e respostas 500 seguras

### DevOps

- **Build Docker Multi-Stage** — Imagem otimizada com padrao builder, Python 3.12-slim
- **Orquestracao Docker Compose** — Backend + frontend com dependencias controladas por health, limites de recursos, volumes nomeados
- **Proxy Reverso Nginx** — Frontend roteia `/api/` para o backend, fallback SPA, compressao gzip, cache de assets estaticos
- **CI GitHub Actions** — Lint (ruff) + Type Check (mypy) + Test (pytest) + Docker Build com smoke test

---

## Arquitetura

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

### Arquitetura em Camadas

| Camada | Caminho | Responsabilidade |
|--------|---------|------------------|
| **Core** | `app/core/` | Config, seguranca, excecoes, logging |
| **API** | `app/api/v1/` | Endpoints HTTP versionados (routers) |
| **Services** | `app/services/` | Logica de negocio (analise de contratos, indexacao, gerenciamento de chaves) |
| **Repositories** | `app/repositories/` | Acesso a dados (SQLite com modo WAL) |
| **Middleware** | `app/middleware/` | Preocupacoes transversais (rate limit, tracing, headers, erros) |
| **Models** | `app/models/` | Schemas Pydantic v2 de request/response |

---

## Stack Tecnologica

| Componente | Tecnologia |
|------------|-----------|
| **Framework API** | FastAPI 0.115+ com async lifespan |
| **Validacao** | Pydantic v2 + pydantic-settings |
| **Servidor** | Uvicorn (ASGI) |
| **Indice Vetorial** | FAISS (IndexFlatL2) com persistencia em disco |
| **Embeddings** | OpenAI `text-embedding-3-small` / Sentence Transformers `all-MiniLM-L6-v2` / fallback TF-IDF |
| **Banco de Dados** | SQLite com modo WAL |
| **Frontend** | React 18 + TypeScript + Tailwind CSS + Vite |
| **Cliente HTTP** | Axios (frontend) / httpx (backend) |
| **Proxy Reverso** | Nginx (Docker) |
| **Containerizacao** | Docker multi-stage + Docker Compose |
| **CI/CD** | GitHub Actions (pipeline de 4 estagios) |
| **Linting** | Ruff (Python) + ESLint (TypeScript) |
| **Type Checking** | mypy (Python) + TypeScript strict |
| **Testes** | pytest + pytest-asyncio |

---

## Estrutura do Projeto

```
astra_block_blockchain/
├── app/
│   ├── main.py                      # App factory, lifespan, middleware stack
│   ├── core/
│   │   ├── config.py                # Pydantic Settings (validacao de env)
│   │   ├── security.py              # Dependencias de auth (verify_api_key, verify_admin_key)
│   │   ├── exceptions.py            # Hierarquia de excecoes (401/403/404/422/429/502)
│   │   └── logging.py              # Formatters JSON/Text, logging estruturado
│   ├── api/v1/
│   │   ├── router.py                # Agregador de rotas
│   │   └── endpoints/
│   │       ├── health.py            # /health, /readiness
│   │       ├── contracts.py         # /contracts/analyze
│   │       ├── documents.py         # /documents/search, /documents/
│   │       └── admin.py             # /admin/keys CRUD
│   ├── services/
│   │   ├── contract_service.py      # Fetch Etherscan + analise heuristica
│   │   ├── indexer_service.py       # Indexacao vetorial multi-backend
│   │   └── apikey_service.py        # Logica de gerenciamento de chaves
│   ├── repositories/
│   │   └── apikey_repository.py     # Repositorio SQLite (WAL, thread-safe)
│   ├── middleware/
│   │   ├── rate_limiter.py          # Rate limiter de janela deslizante
│   │   ├── request_id.py            # IDs de correlacao UUID
│   │   ├── security_headers.py      # Headers OWASP
│   │   └── error_handler.py         # Envelope global de erros
│   ├── models/
│   │   └── schemas.py               # Todos schemas Pydantic v2
│   └── static/
│       └── favicon.svg              # Favicon AstraBlock
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # Router + Layout
│   │   ├── api/astrablock.ts        # Cliente API tipado (Axios)
│   │   ├── pages/
│   │   │   ├── Home.tsx             # Dashboard com stats e acoes rapidas
│   │   │   ├── ContractAnalysis.tsx # UI de analise de risco de contratos
│   │   │   ├── RagSearch.tsx        # UI de busca semantica
│   │   │   └── MarketOptions.tsx    # Analise de opcoes (demo)
│   │   └── components/
│   │       └── Layout.tsx           # Layout com navegacao lateral
│   ├── public/favicon.svg
│   ├── nginx.conf                   # Proxy reverso + SPA + gzip
│   └── Dockerfile                   # Build multi-stage do frontend
├── tests/
│   ├── conftest.py                  # Fixtures de sessao (TestClient, admin headers)
│   ├── test_health.py               # Health, readiness, headers, request IDs
│   ├── test_contracts.py            # Validacao de analise de contratos
│   ├── test_documents.py            # Busca RAG e indexacao
│   ├── test_admin.py                # CRUD de chaves + fluxos de auth
│   ├── test_analyzer.py             # Testes de servico de analise
│   └── test_indexer.py              # Testes unitarios do IndexerService
├── docker-compose.yml               # Orquestracao (API + Frontend)
├── Dockerfile                       # Build multi-stage Python
├── pyproject.toml                   # Config do Ruff, mypy, pytest
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Template de variaveis de ambiente
├── .github/workflows/ci.yml         # Pipeline CI
└── CLAUDE.md                        # Contexto do projeto para Claude Code
```

---

## Pre-requisitos

- **Python 3.11+** (3.12 recomendado)
- **Node.js 18+** (para desenvolvimento do frontend)
- **Docker** e **Docker Compose**
- Chaves de API (opcional, para funcionalidade completa):
  - **Etherscan** — Busca de codigo-fonte de contratos
  - **Infura/RPC** — Acesso a no blockchain
  - **OpenAI** — Embeddings na nuvem (`text-embedding-3-small`)

---

## Inicio Rapido

### Docker (Recomendado)

```bash
# Clonar
git clone https://github.com/yourusername/astrablock.git
cd astrablock

# Configurar
cp .env.example .env
# Edite .env com suas chaves de API (opcional)

# Build e execucao
docker compose up --build -d

# Verificar
curl http://localhost:8083/api/v1/health
# {"status":"ok","version":"1.0.0","environment":"development"}
```

| Servico | URL |
|---------|-----|
| **API** | http://localhost:8083 |
| **Swagger Docs** | http://localhost:8083/docs |
| **ReDoc** | http://localhost:8083/redoc |
| **Frontend** | http://localhost:3003 |

### Desenvolvimento Local

```bash
# Backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

# Frontend (terminal separado)
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Configuracao

Toda configuracao e gerenciada via variaveis de ambiente com validacao no startup (fail-fast). Veja [.env.example](.env.example) para o template completo.

| Variavel | Padrao | Descricao |
|----------|--------|-----------|
| `ENVIRONMENT` | `development` | `production` / `staging` / `development` |
| `ADMIN_API_KEY` | — | Chave admin para endpoints `/admin/*` |
| `OPENAI_API_KEY` | — | Embeddings OpenAI (opcional, fallback para local) |
| `ETHERSCAN_API_KEY` | — | API de codigo-fonte do Etherscan |
| `RPC_URL` | `https://mainnet.infura.io/v3/...` | Endpoint RPC Ethereum |
| `RATE_LIMIT_CALLS` | `120` | Max requisicoes por janela |
| `RATE_LIMIT_PERIOD` | `60` | Tamanho da janela em segundos |
| `CORS_ORIGINS` | `["*"]` | Origens CORS permitidas (array JSON) |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `LOG_FORMAT` | `json` | `json` (estruturado) ou `text` (legivel) |
| `FAISS_INDEX_PATH` | `./data/faiss.index` | Caminho de persistencia do indice vetorial |
| `APIKEY_DB_PATH` | `./data/apikeys.db` | Caminho do banco SQLite |
| `API_PORT` | `8083` | Porta Docker host para API |
| `FRONTEND_PORT` | `3003` | Porta Docker host para frontend |

### Prioridade do Backend de Embeddings

O indexador seleciona automaticamente o melhor backend disponivel:

1. **OpenAI** (`text-embedding-3-small`) — se `OPENAI_API_KEY` estiver definida
2. **Sentence Transformers** (`all-MiniLM-L6-v2`) — local, sem necessidade de chave
3. **TF-IDF** — fallback final, sem dependencias alem do sklearn

---

## Referencia da API

Todos endpoints sao prefixados com `/api/v1`. Documentacao interativa disponivel em `/docs` (apenas desenvolvimento).

### Endpoints Publicos

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/v1/health` | Probe de liveness |
| `GET` | `/api/v1/readiness` | Probe de readiness (verifica indexer + banco) |
| `GET` | `/api/v1/contracts/analyze?address=0x...` | Analise de risco de contrato inteligente |
| `GET` | `/api/v1/documents/search?q=query&k=5` | Busca semantica RAG |

### Endpoints Autenticados (Chave de API)

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `POST` | `/api/v1/documents/` | Indexar novos documentos |
| `GET` | `/api/v1/documents/` | Listar documentos indexados |

### Endpoints Admin (Chave Admin)

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `POST` | `/api/v1/admin/keys` | Criar chave de API de usuario |
| `GET` | `/api/v1/admin/keys` | Listar todas as chaves |
| `DELETE` | `/api/v1/admin/keys/{key}` | Revogar uma chave |

### Autenticacao

```bash
# Endpoint de usuario (header X-API-Key)
curl -H "X-API-Key: sua-chave-usuario" http://localhost:8083/api/v1/documents/

# Endpoint admin
curl -H "X-API-Key: sua-chave-admin" http://localhost:8083/api/v1/admin/keys

# Criar chave de usuario (admin)
curl -X POST -H "X-API-Key: sua-chave-admin" \
     -H "Content-Type: application/json" \
     -d '{"name": "meu-app"}' \
     http://localhost:8083/api/v1/admin/keys
```

### Exemplo: Analisar um Contrato

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

### Envelope de Erro

Todos erros seguem formato consistente:

```json
{
  "success": false,
  "error_code": "AUTHENTICATION_ERROR",
  "message": "Missing or invalid API key",
  "details": null,
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

| Codigo de Erro | HTTP Status | Descricao |
|----------------|-------------|-----------|
| `AUTHENTICATION_ERROR` | 401 | Chave de API ausente ou invalida |
| `AUTHORIZATION_ERROR` | 403 | Permissoes insuficientes (admin necessario) |
| `NOT_FOUND` | 404 | Recurso nao encontrado |
| `VALIDATION_ERROR` | 422 | Falha na validacao da requisicao |
| `RATE_LIMIT_EXCEEDED` | 429 | Muitas requisicoes |
| `EXTERNAL_SERVICE_ERROR` | 502 | Falha em servico externo (Etherscan, OpenAI) |
| `INTERNAL_ERROR` | 500 | Erro interno do servidor |

---

## Seguranca

### Modelo de Autenticacao

```
Request → Header X-API-Key
  │
  ├─ Endpoints admin → verify_admin_key() → secrets.compare_digest(key, ADMIN_API_KEY)
  │
  └─ Endpoints usuario → verify_api_key() → compara chave admin OU verifica repositorio SQLite
```

### Headers de Seguranca (todas respostas)

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

- Algoritmo de janela deslizante com chave por API key ou IP do cliente
- Configuravel via `RATE_LIMIT_CALLS` e `RATE_LIMIT_PERIOD`
- Headers de resposta: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Probes de health/readiness sao excluidos do rate limiting

### Hardening para Producao

- Swagger/ReDoc/OpenAPI desabilitados em producao (`ENVIRONMENT=production`)
- Usuario Docker non-root (`astra`) sem shell
- Limites de recursos via Docker Compose (1GB RAM, 1 CPU)
- Volumes nomeados para persistencia de dados entre restarts

---

## Observabilidade

### Logging Estruturado

Cada entrada de log e uma unica linha JSON (compativel 12-factor):

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

### Rastreamento de Requisicoes

- Cada requisicao recebe um UUID `X-Request-ID` (gerado ou propagado do cliente)
- Request ID e anexado a todas entradas de log via `ContextVar`
- Retornado nos headers de resposta para correlacao end-to-end

### Health Probes

```bash
# Liveness (o processo esta vivo?)
GET /api/v1/health → {"status":"ok","version":"1.0.0","environment":"development"}

# Readiness (as dependencias estao saudaveis?)
GET /api/v1/readiness → {
  "status": "ok",
  "checks": [
    {"name": "indexer", "status": "ok", "latency_ms": null},
    {"name": "database", "status": "ok", "latency_ms": 2.39}
  ]
}
```

---

## Desenvolvimento

### Qualidade de Codigo

```bash
# Lint (Python)
ruff check .
ruff format --check .

# Type check
mypy app/

# Executar todas verificacoes
ruff check . && ruff format --check . && mypy app/ && pytest
```

### Configuracao de Ferramentas

Todas ferramentas configuradas no [pyproject.toml](pyproject.toml):

- **Ruff**: Line length 120, regras E/F/W/I/N/UP/B/SIM
- **mypy**: Python 3.12, `warn_return_any`, `ignore_missing_imports`
- **pytest**: Diretorio de testes `tests/`, modo async auto

---

## Testes

```bash
# Executar todos os testes
pytest

# Com saida detalhada
pytest -v

# Arquivo de teste especifico
pytest tests/test_health.py
```

### Suite de Testes

| Arquivo | Cobertura |
|---------|-----------|
| `test_health.py` | Health, readiness, headers de seguranca, propagacao de request ID |
| `test_contracts.py` | Validacao de endereco, pipeline de analise, camada de servico |
| `test_documents.py` | Busca RAG, indexacao de documentos, enforcement de auth |
| `test_admin.py` | Ciclo CRUD de chaves, auth admin, fluxo de chave de usuario |
| `test_analyzer.py` | Servico de contratos com deteccao de padroes |
| `test_indexer.py` | IndexerService add/search/count |

---

## Pipeline CI/CD

O [workflow do GitHub Actions](.github/workflows/ci.yml) executa um pipeline de 4 estagios:

```
Lint (ruff) ──► Type Check (mypy) ──► Test (pytest) ──► Docker Build + Smoke Test
```

| Estagio | Ferramenta | Descricao |
|---------|-----------|-----------|
| **Lint** | ruff | Verificacao de formato + linting (PEP 8, imports, naming, modernizacao) |
| **Type Check** | mypy | Analise estatica de tipos |
| **Test** | pytest | Suite completa de testes de integracao |
| **Docker** | docker build | Build multi-stage + smoke test de health check |

---

## Contribuicao

1. Faca um fork do repositorio
2. Crie uma branch de feature: `git checkout -b feature/funcionalidade-incrivel`
3. Siga os padroes de codigo existentes (arquitetura em camadas, schemas Pydantic, servicos tipados)
4. Adicione testes para novos endpoints/servicos
5. Garanta que todas verificacoes passem: `ruff check . && mypy app/ && pytest`
6. Faca commit das mudancas: `git commit -m 'feat: adiciona funcionalidade incrivel'`
7. Push para a branch: `git push origin feature/funcionalidade-incrivel`
8. Abra um Pull Request

---

## Licenca

Este projeto esta licenciado sob a Licenca MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
