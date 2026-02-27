"""
Global exception handler — catches all AstraBlockError subclasses and
unhandled exceptions, returning a consistent JSON error envelope.
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AstraBlockError
from app.core.logging import get_logger
from app.models.schemas import ErrorResponse

logger = get_logger("middleware.errors")


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AstraBlockError)
    async def astra_error_handler(request: Request, exc: AstraBlockError):
        rid = getattr(request.state, "request_id", None)
        logger.warning(
            exc.message,
            extra={"extra_data": {"error_code": exc.error_code, "request_id": rid}},
        )
        body = ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            request_id=rid,
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        rid = getattr(request.state, "request_id", None)
        body = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
            request_id=rid,
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        rid = getattr(request.state, "request_id", None)
        logger.exception("Unhandled exception", extra={"extra_data": {"request_id": rid}})
        body = ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            request_id=rid,
        )
        return JSONResponse(status_code=500, content=body.model_dump())
