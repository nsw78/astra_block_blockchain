"""
Admin endpoints — API key management.
"""
from fastapi import APIRouter, Depends, Path

from app.core.security import verify_admin_key
from app.models.schemas import (
    APIKeyInfo,
    CreateKeyRequest,
    CreateKeyResponse,
    DeleteKeyResponse,
    ListKeysResponse,
)
from app.services.apikey_service import APIKeyService

router = APIRouter(prefix="/admin", tags=["admin"])

_service = APIKeyService()


@router.post(
    "/keys",
    response_model=CreateKeyResponse,
    status_code=201,
    summary="Create a new API key",
)
async def create_key(
    req: CreateKeyRequest,
    _admin: str = Depends(verify_admin_key),
):
    result = _service.create_key(req.name)
    return CreateKeyResponse(key=result["key"], name=result["name"])


@router.get(
    "/keys",
    response_model=ListKeysResponse,
    summary="List all API keys",
)
async def list_keys(_admin: str = Depends(verify_admin_key)):
    rows = _service.list_keys()
    keys = [
        APIKeyInfo(key=r["key"], name=r.get("name"), created_at=r.get("created_at"))
        for r in rows
    ]
    return ListKeysResponse(keys=keys)


@router.delete(
    "/keys/{key}",
    response_model=DeleteKeyResponse,
    summary="Revoke an API key",
)
async def delete_key(
    key: str = Path(..., min_length=1),
    _admin: str = Depends(verify_admin_key),
):
    ok = _service.delete_key(key)
    return DeleteKeyResponse(deleted=ok)
