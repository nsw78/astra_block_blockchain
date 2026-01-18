# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [Español](README.es.md)

AstraBlock é um kit de ferramentas LLM mínimo para análise de blockchain e criptomoedas, construído como um scaffold educacional. Ele fornece ferramentas para avaliação de risco de contratos inteligentes e buscas de Geração Aumentada por Recuperação (RAG) em documentos indexados.

> **⚠️ Aviso:** Este é um projeto educacional. Não use os resultados para decisões financeiras sem validação profissional.

## Índice

- [Recursos](#recursos)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints da API](#endpoints-da-api)
- [Desenvolvimento](#desenvolvimento)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Recursos

- **Analisador de Contratos**: Avaliação de risco baseada em heurísticas simples para contratos inteligentes Ethereum
- **Indexador de Embeddings**: Implementação de RAG usando Sentence Transformers e FAISS para busca semântica
- **API REST**: Backend baseado em FastAPI com autenticação e verificações de saúde
- **Frontend Moderno**: SPA React/TypeScript com interfaces de análise de contratos e busca RAG
- **Suporte ao Docker**: Arquitetura de microsserviços com Docker Compose para implantação fácil
- **CI/CD**: Workflow do GitHub Actions para testes automatizados

## Arquitetura

O projeto segue uma arquitetura de microsserviços:

- **Backend (Python/FastAPI)**: Lida com solicitações de API, análise de contratos e operações RAG
- **Frontend (React/TypeScript)**: Interface do usuário para interagir com as ferramentas de análise
- **Banco de Dados/Índice**: Índice vetorial FAISS para embeddings (em memória para demonstração)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (React/TS)    │◄──►│   (FastAPI)     │
│   Porta 3002    │    │   Porta 8081    │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 Docker Compose
```

## Pré-requisitos

- Python 3.10 ou superior
- Node.js 18+ (para desenvolvimento do frontend)
- Docker e Docker Compose
- Chaves de API para Etherscan, INFURA e OpenAI (opcional para funcionalidade completa)

## Instalação

### Desenvolvimento Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/astrablock.git
   cd astrablock
   ```

2. Configure o ambiente Python:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite .env com suas chaves de API
   ```

4. Configure o frontend (opcional):
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   ```

### Implantação com Docker

```bash
docker-compose up --build
```

Isso inicia o backend na porta 8081 e o frontend na porta 3002.

## Uso

### Executando o Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Acesse a documentação da API em `http://localhost:8080/docs`

### Executando o Frontend

```bash
cd frontend
npm run dev
```

Abra `http://localhost:5173` no navegador.

### Exemplo de Uso

Analisar um contrato:
```bash
python examples/demo.py --address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

## Endpoints da API

| Método | Endpoint | Descrição | Autenticação Necessária |
|--------|----------|-----------|-------------------------|
| GET | `/analyze_contract?address=<addr>` | Análise de risco de contrato | Não |
| GET | `/rag_query?q=<query>` | Busca RAG | Não |
| POST | `/index_docs` | Adicionar documentos ao índice | Sim |
| GET | `/docs` | Listar documentos indexados | Sim |
| POST | `/admin/keys` | Criar chave de API de usuário | Admin |
| GET | `/health` | Verificação de saúde | Não |

Autenticação: Use o cabeçalho `x-api-key` com sua chave de API.

## Desenvolvimento

### Executando Testes

```bash
pytest
```

### Construindo Frontend para Produção

```bash
cd frontend
npm run build
```

### Qualidade do Código

- Use `black` para formatação Python
- Use `flake8` para linting
- Frontend usa ESLint e Prettier

## Contribuição

1. Faça um fork do repositório
2. Crie uma branch de recurso: `git checkout -b feature/recurso-incrivel`
3. Faça commit das suas mudanças: `git commit -m 'Adiciona recurso incrível'`
4. Faça push para a branch: `git push origin feature/recurso-incrivel`
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.