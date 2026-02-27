"""
In-memory sliding-window rate limiter middleware.
Production: swap for Redis-backed (e.g. via fastapi-limiter).
"""
import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.config import get_settings
from app.core.exceptions import RateLimitError
from app.core.logging import get_logger

logger = get_logger("middleware.ratelimit")


class SlidingWindowRateLimiter:
    """Fixed-window limiter keyed by API key or client IP."""

    def __init__(self, calls: int = 120, period: int = 60):
        self.calls = calls
        self.period = period
        self._store: Dict[str, Tuple[float, int]] = {}

    def check(self, key: str) -> Tuple[bool, int]:
        """Returns (allowed, remaining)."""
        now = time.time()
        entry = self._store.get(key)
        if not entry or now - entry[0] > self.period:
            self._store[key] = (now, 1)
            return True, self.calls - 1
        start, count = entry
        if count < self.calls:
            self._store[key] = (start, count + 1)
            return True, self.calls - count - 1
        return False, 0


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # skip health probes
        if request.url.path in ("/api/v1/health", "/api/v1/readiness"):
            return await call_next(request)

        limiter: SlidingWindowRateLimiter = request.app.state.rate_limiter
        identity = request.headers.get("x-api-key") or (request.client.host if request.client else "unknown")
        allowed, remaining = limiter.check(identity)

        if not allowed:
            raise RateLimitError()

        response = await call_next(request)
        settings = get_settings()
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_CALLS)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
