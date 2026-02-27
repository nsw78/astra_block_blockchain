"""
API-key management service layer.
"""
from typing import List, Optional

from app.core.logging import get_logger
from app.repositories.apikey_repository import APIKeyRepository

logger = get_logger("service.apikeys")


class APIKeyService:
    def __init__(self, repo: Optional[APIKeyRepository] = None) -> None:
        self._repo = repo or APIKeyRepository()

    def create_key(self, name: Optional[str] = None) -> dict:
        return self._repo.create(name)

    def list_keys(self) -> List[dict]:
        return self._repo.list_all()

    def delete_key(self, key: str) -> bool:
        return self._repo.delete(key)

    def verify_key(self, key: str) -> bool:
        return self._repo.verify(key)
