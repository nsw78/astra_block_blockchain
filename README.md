# AstraBlock — Mini LLM toolkit for Blockchain & Crypto (example)

[Português Brasileiro](README.pt-br.md) | [Español](README.es.md)

This repository is a Python scaffold that demonstrates a minimal environment for building LLM tools focused on cryptocurrencies and smart contracts:

- Contract analyzer (simple heuristics)
- Embedding indexer (RAG) with `sentence-transformers` + `faiss`
- Minimal API using FastAPI to expose analysis and RAG searches

Risks and notes:
- This project is an educational starting point. Do not use the results for financial decisions without human validation.

Requirements
- Python 3.10+
- It is recommended to create a virtual environment

Quick Installation
```bash
cd /home/nelsons_walcow/Documentos/Projects/AstraBlock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill .env with your keys (Etherscan/INFURA/OPENAI)
```

Running the API
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Docker (for quick production)
```bash
docker-compose up --build
```

This will start both the backend API on port 8081 and the frontend on port 3002.

## Frontend

A modern React/TypeScript frontend is available in the `frontend/` directory. It is a complete single-page application featuring:

- Contract Analysis page: Input contract address and view risk analysis results
- RAG Search page: Perform semantic searches on indexed documents
- Responsive UI with Tailwind CSS
- API integration via Axios
- Client-side routing with React Router

To run the frontend locally (development):
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The frontend will be available at `http://localhost:5173` and connects to the API at `http://localhost:8080`.

In production (via Docker), it's served on port 3002 as a microservice, containerized with Nginx for static asset serving and SPA routing.

Admin keys & API keys
- Set `ADMIN_API_KEY` env var for admin operations (creating user keys).
- Create user API keys via `POST /admin/keys` with header `x-api-key: <ADMIN_API_KEY>`.
- Use user keys in header `x-api-key` to call protected endpoints (`/documents`, `/index_docs`, etc.).

CI
- A simple GitHub Actions workflow is included in `.github/workflows/ci.yml` which runs tests.

Endpoints
- `GET /analyze_contract?address=<0x...>` — returns risk heuristics for the contract
- `GET /rag_query?q=text` — performs search on the index (OpenAI embeddings/faiss or fallback TF-IDF)
- `POST /index_docs` — *authenticated* (header `x-api-key`) accepts JSON `{ "docs": ["a","b"], "ids": ["id1", "id2"] }` and adds to the index
- `GET /docs` — *authenticated* lists indexed documents
- `GET /health` — healthcheck

Exemplos rápidos
```bash
python examples/demo.py --address 0x...  # demonstra análise de contrato
```

Próximos passos sugeridos
- Adicionar testes automatizados
- Melhorar heurísticas com exemplos de ataques
- Construir pipeline de coleta on-chain para alimentar RAG
- Subir index FAISS em storage (S3) e orquestrar com Airflow
- Considerar uso de uma conta de embeddings (OpenAI / HuggingFace) dedicada para produção

Quer que eu: 
- rode um `pip install` e verifique dependências aqui?
- implemente autenticação na API?
- adicione coleta do Twitter e integração com OpenAI para sumarização?
# astra_block_blockchain
