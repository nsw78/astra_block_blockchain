# AstraBlock — Mini toolkit LLM para Blockchain & Cripto (exemplo)

[English](README.md) | [Español](README.es.md)

Este repositório é um scaffold em Python que demonstra um ambiente mínimo para construir ferramentas LLM focadas em criptomoedas e smart contracts:

- Analisador de contratos (heurísticas simples)
- Indexador de embeddings (RAG) com `sentence-transformers` + `faiss`
- API mínima usando FastAPI para expor análise e buscas RAG

Riscos e notas:
- Este projeto é um ponto de partida educacional. Não use os resultados para decisões financeiras sem validação humana.

Requisitos
- Python 3.10+
- Recomenda-se criar um ambiente virtual

Instalação rápida
```bash
cd /home/nelsons_walcow/Documentos/Projects/AstraBlock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Preencha .env com suas chaves (Etherscan/INFURA/OPENAI)
```

Rodando a API
```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Docker (para produção rápida)
```bash
docker-compose up --build
```

Isso iniciará tanto a API backend na porta 8081 quanto o frontend na porta 3002.

## Frontend

Um frontend moderno em React/TypeScript está disponível no diretório `frontend/`. É uma aplicação completa de página única com recursos como:

- Página de Análise de Contratos: Insira o endereço do contrato e visualize os resultados de análise de risco
- Página de Busca RAG: Realize buscas semânticas em documentos indexados
- Interface responsiva com Tailwind CSS
- Integração de API via Axios
- Roteamento do lado cliente com React Router

Para executar o frontend localmente (desenvolvimento):
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

O frontend estará disponível em `http://localhost:5173` e se conecta à API em `http://localhost:8080`.

Em produção (via Docker), é servido na porta 3002 como um microserviço, containerizado com Nginx para servir ativos estáticos e roteamento SPA.

Admin keys & API keys
- Defina a variável de ambiente `ADMIN_API_KEY` para operações de admin (criar chaves de usuário).
- Crie chaves de API de usuário via `POST /admin/keys` com header `x-api-key: <ADMIN_API_KEY>`.
- Use chaves de usuário no header `x-api-key` para chamar endpoints protegidos (`/documents`, `/index_docs`, etc.).

CI
- Um workflow simples do GitHub Actions está incluído em `.github/workflows/ci.yml` que executa testes.

Endpoints
- `GET /analyze_contract?address=<0x...>` — retorna heurísticas de risco para o contrato
- `GET /rag_query?q=texto` — realiza busca sobre o índice (OpenAI embeddings/faiss ou fallback TF-IDF)
- `POST /index_docs` — *autenticado* (header `x-api-key`) aceita JSON `{ "docs": ["a","b"], "ids": ["id1", "id2"] }` e adiciona ao índice
- `GET /docs` — *autenticado* lista documentos indexados