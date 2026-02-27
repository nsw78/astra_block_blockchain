"""
AstraBlock API — Enterprise-grade application factory.

Architecture:
  app/core/         → config, security, exceptions, logging
  app/api/v1/       → versioned HTTP endpoints
  app/services/     → business logic
  app/repositories/ → data access
  app/middleware/    → cross-cutting concerns
  app/models/       → Pydantic schemas
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.api.v1.router import api_router
from app.middleware.error_handler import register_error_handlers
from app.middleware.rate_limiter import RateLimitMiddleware, SlidingWindowRateLimiter
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.models.schemas import RootResponse
from app.services.indexer_service import build_default_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    settings = get_settings()
    configure_logging(level=settings.LOG_LEVEL, fmt=settings.LOG_FORMAT)
    logger = get_logger("main")

    # -- startup --
    logger.info(
        "Starting AstraBlock",
        extra={"extra_data": {"version": settings.APP_VERSION, "env": settings.ENVIRONMENT}},
    )

    # rate limiter
    app.state.rate_limiter = SlidingWindowRateLimiter(
        calls=settings.RATE_LIMIT_CALLS,
        period=settings.RATE_LIMIT_PERIOD,
    )

    # vector index
    app.state.indexer = build_default_index()

    logger.info("AstraBlock startup complete")
    yield
    # -- shutdown --
    logger.info("AstraBlock shutting down")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Blockchain smart-contract risk analysis & RAG search API. "
            "Enterprise-grade with versioned endpoints, structured logging, "
            "rate limiting, and API-key authentication."
        ),
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # ── middleware (order matters: outermost runs first) ──
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # ── error handlers ──
    register_error_handlers(app)

    # ── versioned routes ──
    app.include_router(api_router)

    # ── favicon ──
    _static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

    @app.get("/favicon.ico", include_in_schema=False)
    @app.get("/favicon.svg", include_in_schema=False)
    async def favicon():
        return FileResponse(
            str(_static_dir / "favicon.svg"),
            media_type="image/svg+xml",
        )

    # ── root ──
    @app.get("/", response_model=RootResponse, tags=["root"])
    async def root():
        return RootResponse(
            service=settings.APP_NAME,
            version=settings.APP_VERSION,
            status="ok",
            docs="/docs",
        )

    return app


# The ASGI entrypoint used by uvicorn / gunicorn
app = create_app()
