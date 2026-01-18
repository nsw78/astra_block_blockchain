# AstraBlock

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [Português Brasileiro](README.pt-br.md)

AstraBlock es un kit de herramientas LLM mínimo para análisis de blockchain y criptomonedas, construido como un scaffold educativo. Proporciona herramientas para evaluación de riesgo de contratos inteligentes y búsquedas de Generación Aumentada por Recuperación (RAG) en documentos indexados.

> **⚠️ Advertencia:** Este es un proyecto educativo. No use los resultados para decisiones financieras sin validación profesional.

## Índice

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Prerrequisitos](#prerrequisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Desarrollo](#desarrollo)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Características

- **Analizador de Contratos**: Evaluación de riesgo basada en heurísticas simples para contratos inteligentes Ethereum
- **Indexador de Embeddings**: Implementación de RAG usando Sentence Transformers y FAISS para búsqueda semántica
- **API REST**: Backend basado en FastAPI con autenticación y verificaciones de salud
- **Frontend Moderno**: SPA React/TypeScript con interfaces de análisis de contratos y búsqueda RAG
- **Soporte Docker**: Arquitectura de microservicios con Docker Compose para despliegue fácil
- **CI/CD**: Workflow de GitHub Actions para pruebas automatizadas

## Arquitectura

El proyecto sigue una arquitectura de microservicios:

- **Backend (Python/FastAPI)**: Maneja solicitudes de API, análisis de contratos y operaciones RAG
- **Frontend (React/TypeScript)**: Interfaz de usuario para interactuar con las herramientas de análisis
- **Base de Datos/Índice**: Índice vectorial FAISS para embeddings (en memoria para demostración)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (React/TS)    │◄──►│   (FastAPI)     │
│   Puerto 3002   │    │   Puerto 8081   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 Docker Compose
```

## Prerrequisitos

- Python 3.10 o superior
- Node.js 18+ (para desarrollo del frontend)
- Docker y Docker Compose
- Claves de API para Etherscan, INFURA y OpenAI (opcional para funcionalidad completa)

## Instalación

### Desarrollo Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/yourusername/astrablock.git
   cd astrablock
   ```

2. Configura el entorno Python:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configura variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus claves de API
   ```

4. Configura el frontend (opcional):
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   ```

### Despliegue con Docker

```bash
docker-compose up --build
```

Esto inicia el backend en el puerto 8081 y el frontend en el puerto 3002.

## Uso

### Ejecutando el Backend

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080
```

Accede a la documentación de la API en `http://localhost:8080/docs`

### Ejecutando el Frontend

```bash
cd frontend
npm run dev
```

Abre `http://localhost:5173` en el navegador.

### Ejemplo de Uso

Analizar un contrato:
```bash
python examples/demo.py --address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

## Endpoints de la API

| Método | Endpoint | Descripción | Autenticación Requerida |
|--------|----------|-------------|--------------------------|
| GET | `/analyze_contract?address=<addr>` | Análisis de riesgo de contrato | No |
| GET | `/rag_query?q=<query>` | Búsqueda RAG | No |
| POST | `/index_docs` | Agregar documentos al índice | Sí |
| GET | `/docs` | Listar documentos indexados | Sí |
| POST | `/admin/keys` | Crear clave de API de usuario | Admin |
| GET | `/health` | Verificación de salud | No |

Autenticación: Usa el encabezado `x-api-key` con tu clave de API.

## Desarrollo

### Ejecutando Pruebas

```bash
pytest
```

### Construyendo Frontend para Producción

```bash
cd frontend
npm run build
```

### Calidad del Código

- Usa `black` para formateo Python
- Usa `flake8` para linting
- Frontend usa ESLint y Prettier

## Contribución

1. Haz un fork del repositorio
2. Crea una rama de característica: `git checkout -b feature/caracteristica-increible`
3. Confirma tus cambios: `git commit -m 'Agrega característica increíble'`
4. Haz push a la rama: `git push origin feature/caracteristica-increible`
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para detalles.