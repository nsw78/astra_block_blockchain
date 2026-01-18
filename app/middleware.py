import time
from typing import Dict
from fastapi import Request, HTTPException


class SimpleRateLimiter:
    """In-memory fixed-window rate limiter. Not distributed — fine for MVP/testing.

    Limits by api_key if present, otherwise by client IP.
    """

    def __init__(self, calls: int = 60, period_seconds: int = 60):
        self.calls = calls
        self.period = period_seconds
        # mapping key -> (window_start, count)
        self.store: Dict[str, tuple[float, int]] = {}

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        entry = self.store.get(key)
        if not entry:
            self.store[key] = (now, 1)
            return True
        start, count = entry
        if now - start > self.period:
            # reset
            self.store[key] = (now, 1)
            return True
        if count < self.calls:
            self.store[key] = (start, count + 1)
            return True
        return False


async def rate_limit_middleware(request: Request, call_next):
    limiter: SimpleRateLimiter = request.app.state.rate_limiter
    api_key = request.headers.get('x-api-key') or request.client.host
    if not limiter.is_allowed(api_key):
        raise HTTPException(status_code=429, detail='rate limit exceeded')
    response = await call_next(request)
    return response
