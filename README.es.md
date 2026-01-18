# AstraBlock — Mini kit de herramientas LLM para Blockchain & Cripto (ejemplo)

[English](README.md) | [Português Brasileiro](README.pt-br.md)

Este repositorio es un scaffold en Python que demuestra un entorno mínimo para construir herramientas LLM enfocadas en criptomonedas y contratos inteligentes:

- Analizador de contratos (heurísticas simples)
- Indexador de embeddings (RAG) con `sentence-transformers` + `faiss`
- API mínima usando FastAPI para exponer análisis y búsquedas RAG

Riesgos y notas:
- Este proyecto es un punto de partida educativo. No use los resultados para decisiones financieras sin validación humana.

Requisitos
- Python 3.10+
- Se recomienda crear un entorno virtual

Instalación rápida
```bash
cd /home/nelsons_walcow/Documentos/Projects/AstraBlock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Llene .env con sus claves (Etherscan/INFURA/OPENAI)
```

Ejecutando la API
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Docker (para producción rápida)
```bash
docker-compose up --build
```

Esto iniciará tanto la API backend en el puerto 8081 como el frontend en el puerto 3002.

## Frontend

Un frontend moderno en React/TypeScript está disponible en el directorio `frontend/`. Es una aplicación completa de página única con características como:

- Página de Análisis de Contratos: Ingrese la dirección del contrato y vea los resultados de análisis de riesgo
- Página de Búsqueda RAG: Realice búsquedas semánticas en documentos indexados
- Interfaz responsiva con Tailwind CSS
- Integración de API via Axios
- Enrutamiento del lado cliente con React Router

Para ejecutar el frontend localmente (desarrollo):
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

El frontend estará disponible en `http://localhost:5173` y se conecta a la API en `http://localhost:8080`.

En producción (via Docker), se sirve en el puerto 3002 como un microservicio, containerizado con Nginx para servir activos estáticos y enrutamiento SPA.

Claves admin & API keys
- Establezca la variable de entorno `ADMIN_API_KEY` para operaciones de admin (crear claves de usuario).
- Cree claves de API de usuario via `POST /admin/keys` con header `x-api-key: <ADMIN_API_KEY>`.
- Use claves de usuario en header `x-api-key` para llamar endpoints protegidos (`/documents`, `/index_docs`, etc.).

CI
- Un flujo de trabajo simple de GitHub Actions está incluido en `.github/workflows/ci.yml` que ejecuta pruebas.

Endpoints
- `GET /analyze_contract?address=<0x...>` — retorna heurísticas de riesgo para el contrato
- `GET /rag_query?q=texto` — realiza búsqueda sobre el índice (OpenAI embeddings/faiss o fallback TF-IDF)
- `POST /index_docs` — *autenticado* (header `x-api-key`) acepta JSON `{ "docs": ["a","b"], "ids": ["id1", "id2"] }` y añade al índice
- `GET /docs` — *autenticado* lista documentos indexados