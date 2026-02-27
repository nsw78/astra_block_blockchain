"""
V1 API router — aggregates all endpoint modules under /api/v1.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import admin, contracts, documents, health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(contracts.router)
api_router.include_router(documents.router)
api_router.include_router(admin.router)
