"""
Health & readiness probes.
"""
import time

from fastapi import APIRouter, Request

from app.core.config import get_settings
from app.models.schemas import HealthResponse, ReadinessCheck, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health():
    """Liveness probe — always returns 200 if the process is alive."""
    s = get_settings()
    return HealthResponse(status="ok", version=s.APP_VERSION, environment=s.ENVIRONMENT)


@router.get("/readiness", response_model=ReadinessResponse)
async def readiness(request: Request):
    """Readiness probe — checks downstream dependencies."""
    checks = []

    # check indexer is loaded
    indexer = getattr(request.app.state, "indexer", None)
    if indexer and indexer.doc_count >= 0:
        checks.append(ReadinessCheck(name="indexer", status="ok"))
    else:
        checks.append(ReadinessCheck(name="indexer", status="down"))

    # check DB connectivity
    try:
        from app.repositories.apikey_repository import APIKeyRepository
        t0 = time.perf_counter()
        APIKeyRepository().list_all()
        latency = round((time.perf_counter() - t0) * 1000, 2)
        checks.append(ReadinessCheck(name="database", status="ok", latency_ms=latency))
    except Exception:
        checks.append(ReadinessCheck(name="database", status="down"))

    overall = "ok" if all(c.status == "ok" for c in checks) else "degraded"
    return ReadinessResponse(status=overall, checks=checks)
