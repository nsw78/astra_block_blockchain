"""
Pydantic v2 request / response schemas.
Every API boundary uses explicit models — no raw dicts escape to the client.
"""
from datetime import datetime
from typing import Any, List, Optional, Tuple

from pydantic import BaseModel, Field, field_validator


# ────────────────────────────── Base Envelope ──────────────────────────────


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "ok"
    data: Any = None


class ErrorResponse(BaseModel):
    """Standard error envelope returned by the global error handler."""
    success: bool = False
    error_code: str
    message: str
    details: Any = None
    request_id: Optional[str] = None


class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int


class PaginatedResponse(BaseModel):
    success: bool = True
    data: Any = None
    pagination: PaginationMeta


# ──────────────────────────── Contract Analysis ────────────────────────────


class ContractAnalyzeRequest(BaseModel):
    address: str = Field(..., min_length=42, max_length=42, examples=["0xdAC17F958D2ee523a2206206994597C13D831ec7"])

    @field_validator("address")
    @classmethod
    def must_be_hex(cls, v: str) -> str:
        if not v.startswith("0x"):
            raise ValueError("address must start with 0x")
        return v


class Finding(BaseModel):
    pattern: str
    snippet: str


class ContractRiskAnalysis(BaseModel):
    score: int = Field(0, ge=0, le=100)
    findings: List[Finding] = []
    error: Optional[str] = None


class ContractAnalyzeResponse(BaseModel):
    address: str
    source_available: bool
    analysis: ContractRiskAnalysis


# ──────────────────────────── RAG / Documents ──────────────────────────────


class RAGQueryRequest(BaseModel):
    q: str = Field(..., min_length=1, max_length=2000, description="Search query")
    k: int = Field(5, ge=1, le=100, description="Max results to return")


class RAGResult(BaseModel):
    doc_id: str
    score: float


class RAGQueryResponse(BaseModel):
    query: str
    results: List[RAGResult]


class IndexDocsRequest(BaseModel):
    docs: List[str] = Field(..., min_length=1, max_length=1000)
    ids: Optional[List[str]] = None

    @field_validator("ids")
    @classmethod
    def ids_must_match_docs(cls, v, info):
        docs = info.data.get("docs")
        if v is not None and docs is not None and len(v) != len(docs):
            raise ValueError("ids length must match docs length")
        return v


class IndexDocsResponse(BaseModel):
    indexed: int
    total_docs: int


class ListDocsResponse(BaseModel):
    docs: List[str]


# ──────────────────────────── Admin / API Keys ─────────────────────────────


class CreateKeyRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=128)


class APIKeyInfo(BaseModel):
    key: str
    name: Optional[str]
    created_at: Optional[datetime] = None


class CreateKeyResponse(BaseModel):
    key: str
    name: Optional[str]


class ListKeysResponse(BaseModel):
    keys: List[APIKeyInfo]


class DeleteKeyResponse(BaseModel):
    deleted: bool


# ──────────────────────────── Health ───────────────────────────────────────


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    environment: str


class ReadinessCheck(BaseModel):
    name: str
    status: str  # "ok" | "degraded" | "down"
    latency_ms: Optional[float] = None


class ReadinessResponse(BaseModel):
    status: str  # "ok" | "degraded" | "down"
    checks: List[ReadinessCheck]


# ──────────────────────────── Root ─────────────────────────────────────────


class RootResponse(BaseModel):
    service: str
    version: str
    status: str
    docs: str
