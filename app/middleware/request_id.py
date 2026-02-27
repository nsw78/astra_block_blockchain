"""
Request-ID middleware — attaches a unique correlation ID to every request.
Propagates it in logs and response headers.
"""
import uuid
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

REQUEST_ID_CTX: ContextVar[str] = ContextVar("request_id", default="")

HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        rid = request.headers.get(HEADER) or str(uuid.uuid4())
        REQUEST_ID_CTX.set(rid)
        request.state.request_id = rid

        response = await call_next(request)
        response.headers[HEADER] = rid
        return response
