"""DEPRECATED — use app.repositories.apikey_repository.APIKeyRepository instead."""
from app.repositories.apikey_repository import APIKeyRepository

_repo = APIKeyRepository()

init_db = _repo._ensure_schema
create_key = lambda name=None: _repo.create(name)["key"]
list_keys = lambda: [(r["key"], r.get("name")) for r in _repo.list_all()]
delete_key = _repo.delete
verify_key = _repo.verify
