"""
Authentication & authorization utilities.
Provides FastAPI dependency functions for API-key verification.
"""
import secrets
from typing import Optional

from fastapi import Header

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.repositories.apikey_repository import APIKeyRepository


_repo = APIKeyRepository()


def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> str:
    """Dependency: validates user or admin API key. Returns the key."""
    settings = get_settings()
    if not x_api_key:
        raise AuthenticationError("Missing API key in X-API-Key header")
    # admin bypass
    if settings.ADMIN_API_KEY and secrets.compare_digest(x_api_key, settings.ADMIN_API_KEY):
        return x_api_key
    if not _repo.verify(x_api_key):
        raise AuthenticationError("Invalid API key")
    return x_api_key


def verify_admin_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> str:
    """Dependency: requires the admin API key."""
    settings = get_settings()
    if not settings.ADMIN_API_KEY:
        raise AuthorizationError("Admin API key is not configured on the server")
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.ADMIN_API_KEY):
        raise AuthorizationError("Admin API key required")
    return x_api_key
