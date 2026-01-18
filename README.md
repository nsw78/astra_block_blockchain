# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Português Brasileiro](README.pt-br.md) | [Español](README.es.md)

AstraBlock is a minimal LLM toolkit for blockchain and cryptocurrency analysis, built as an educational scaffold. It provides tools for smart contract risk assessment and Retrieval-Augmented Generation (RAG) searches on indexed documents.

> **⚠️ Disclaimer:** This is an educational project. Do not use results for financial decisions without professional validation.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Contract Analyzer**: Simple heuristic-based risk assessment for Ethereum smart contracts
- **Embedding Indexer**: RAG implementation using Sentence Transformers and FAISS for semantic search
- **REST API**: FastAPI-based backend with authentication and health checks
- **Modern Frontend**: React/TypeScript SPA with contract analysis and RAG search interfaces
- **Docker Support**: Microservices architecture with Docker Compose for easy deployment
- **CI/CD**: GitHub Actions workflow for automated testing

## Architecture

The project follows a microservices architecture:

- **Backend (Python/FastAPI)**: Handles API requests, contract analysis, and RAG operations
- **Frontend (React/TypeScript)**: User interface for interacting with the analysis tools
- **Database/Index**: FAISS vector index for embeddings (in-memory for demo)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (React/TS)    │◄──►│   (FastAPI)     │
│   Port 3002     │    │   Port 8081     │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 Docker Compose
```

## Prerequisites

- Python 3.10 or higher
- Node.js 18+ (for frontend development)
- Docker and Docker Compose
- API keys for Etherscan, INFURA, and OpenAI (optional for full functionality)

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/astrablock.git
   cd astrablock
   ```

2. Set up Python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Set up frontend (optional):
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   ```

### Docker Deployment

```bash
docker-compose up --build
```

This starts the backend on port 8081 and frontend on port 3002.

## Usage

### Running the Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Access the API documentation at `http://localhost:8080/docs`

### Running the Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

### Example Usage

Analyze a contract:
```bash
python examples/demo.py --address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/analyze_contract?address=<addr>` | Contract risk analysis | No |
| GET | `/rag_query?q=<query>` | RAG search | No |
| POST | `/index_docs` | Add documents to index | Yes |
| GET | `/docs` | List indexed documents | Yes |
| POST | `/admin/keys` | Create user API key | Admin |
| GET | `/health` | Health check | No |

Authentication: Use `x-api-key` header with your API key.

## Development

### Running Tests

```bash
pytest
```

### Building Frontend for Production

```bash
cd frontend
npm run build
```

### Code Quality

- Use `black` for Python formatting
- Use `flake8` for linting
- Frontend uses ESLint and Prettier

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
