"""
RAG / document indexing endpoints.
"""
from fastapi import APIRouter, Depends, Query, Request

from app.core.security import verify_api_key
from app.models.schemas import (
    IndexDocsRequest,
    IndexDocsResponse,
    ListDocsResponse,
    RAGQueryResponse,
    RAGResult,
)

router = APIRouter(prefix="/documents", tags=["documents"])


def _get_indexer(request: Request):
    return request.app.state.indexer


@router.get(
    "/search",
    response_model=RAGQueryResponse,
    summary="Semantic search over indexed documents",
)
async def rag_query(
    request: Request,
    q: str = Query(..., min_length=1, max_length=2000, description="Search query"),
    k: int = Query(5, ge=1, le=100, description="Number of results"),
):
    indexer = _get_indexer(request)
    raw = indexer.search(q, k=k)
    results = [RAGResult(doc_id=doc_id, score=score) for doc_id, score in raw]
    return RAGQueryResponse(query=q, results=results)


@router.post(
    "/",
    response_model=IndexDocsResponse,
    summary="Index new documents",
    status_code=201,
)
async def index_docs(
    req: IndexDocsRequest,
    request: Request,
    _key: str = Depends(verify_api_key),
):
    indexer = _get_indexer(request)
    count = indexer.add_texts(req.docs, req.ids)
    return IndexDocsResponse(indexed=count, total_docs=indexer.doc_count)


@router.get(
    "/",
    response_model=ListDocsResponse,
    summary="List all indexed document IDs",
)
async def list_docs(
    request: Request,
    _key: str = Depends(verify_api_key),
):
    indexer = _get_indexer(request)
    return ListDocsResponse(docs=indexer.ids)
