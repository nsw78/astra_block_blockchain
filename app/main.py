from fastapi import FastAPI, HTTPException, Header, Depends
from starlette.middleware import Middleware
from app.logging_config import configure_logging
from app.middleware import rate_limit_middleware, SimpleRateLimiter
from auth import keys as keystore
import logging
from pydantic import BaseModel
from analyzer.contract_analyzer import analyze_contract
from embeddings.indexer import build_index_from_texts, Indexer
import os

app = FastAPI(title="AstraBlock API")
configure_logging()
logger = logging.getLogger('astra')

# In-memory example index (in production, persist to disk/S3)
SAMPLE_TEXTS = [
    "Uniswap V2 pair contract example",
    "ERC20 token with mint function and owner control",
    "Typical rugpull pattern: owner can drain liquidity",
]
index: Indexer = build_index_from_texts(SAMPLE_TEXTS)


ADMIN_API_KEY = os.getenv('ADMIN_API_KEY')

# initialize key DB
keystore.init_db()

# attach rate limiter to app state in startup event


@app.on_event('startup')
async def _startup():
    # attach a simple in-memory rate limiter (60 req/min)
    app.state.rate_limiter = SimpleRateLimiter(calls=120, period_seconds=60)
    logger.info('AstraBlock startup complete')


def verify_api_key(x_api_key: str = Header(None)):
    # Admin key bypass
    if ADMIN_API_KEY and x_api_key == ADMIN_API_KEY:
        return True
    # Otherwise check stored user keys
    if not x_api_key or not keystore.verify_key(x_api_key):
        raise HTTPException(status_code=401, detail='invalid api key')
    return True


def verify_admin_key(x_api_key: str = Header(None)):
    if not ADMIN_API_KEY or x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail='admin api key required')
    return True

class AnalyzeResponse(BaseModel):
    address: str
    source_available: bool
    analysis: dict


@app.get('/analyze_contract', response_model=AnalyzeResponse)
async def api_analyze_contract(address: str):
    if not address.startswith('0x'):
        raise HTTPException(status_code=400, detail='address must start with 0x')
    res = analyze_contract(address)
    return res


@app.get('/rag_query')
async def api_rag_query(q: str):
    res = index.search(q, k=5)
    return {'query': q, 'results': res}


@app.get('/health')
async def health():
    return {'status': 'ok'}


class IndexDocsRequest(BaseModel):
    docs: list[str]
    ids: list[str] | None = None


@app.post('/documents')
async def api_index_docs(req: IndexDocsRequest, _: bool = Depends(verify_api_key)):
    ids = req.ids
    index.add_texts(req.docs, ids)
    return {'indexed': len(req.docs), 'total_docs': len(index.ids)}


@app.get('/documents')
async def api_docs(_: bool = Depends(verify_api_key)):
    return {'docs': index.ids}


class CreateKeyRequest(BaseModel):
    name: str | None = None


@app.post('/admin/keys')
async def admin_create_key(req: CreateKeyRequest, _: bool = Depends(verify_admin_key)):
    key = keystore.create_key(req.name)
    return {'key': key}


@app.get('/admin/keys')
async def admin_list_keys(_: bool = Depends(verify_admin_key)):
    keys = keystore.list_keys()
    return {'keys': [{'key': k, 'name': n} for k, n in keys]}


@app.delete('/admin/keys/{key}')
async def admin_delete_key(key: str, _: bool = Depends(verify_admin_key)):
    ok = keystore.delete_key(key)
    return {'deleted': ok}


@app.get('/')
async def root():
    """Root endpoint with basic status and available endpoints."""
    return {
        'service': 'AstraBlock',
        'status': 'ok',
        'endpoints': {
            'analyze_contract': '/analyze_contract?address=<0x...>',
            'rag_query': '/rag_query?q=<text>'
        }
    }
