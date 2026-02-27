"""
Repository pattern for API key persistence.
Encapsulates all SQLite access — the rest of the app never touches the DB directly.
"""
import os
import sqlite3
import secrets
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("repository.apikeys")


class APIKeyRepository:
    """Thread-safe SQLite repository for API keys."""

    def __init__(self, db_path: Optional[str] = None):
        self._db_path = db_path or get_settings().APIKEY_DB_PATH
        self._ensure_schema()

    # ── internal ──

    def _conn(self) -> sqlite3.Connection:
        d = os.path.dirname(self._db_path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _ensure_schema(self) -> None:
        conn = self._conn()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS apikeys (
                    key        TEXT PRIMARY KEY,
                    name       TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()
        logger.info("API key schema ensured")

    # ── public ──

    def create(self, name: Optional[str] = None) -> dict:
        key = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc).isoformat()
        conn = self._conn()
        try:
            conn.execute(
                "INSERT INTO apikeys (key, name, created_at) VALUES (?, ?, ?)",
                (key, name, now),
            )
            conn.commit()
        finally:
            conn.close()
        logger.info("API key created", extra={"extra_data": {"name": name}})
        return {"key": key, "name": name, "created_at": now}

    def list_all(self) -> List[dict]:
        conn = self._conn()
        try:
            rows = conn.execute(
                "SELECT key, name, created_at FROM apikeys ORDER BY created_at DESC"
            ).fetchall()
        finally:
            conn.close()
        return [dict(r) for r in rows]

    def delete(self, key: str) -> bool:
        conn = self._conn()
        try:
            cur = conn.execute("DELETE FROM apikeys WHERE key = ?", (key,))
            conn.commit()
            deleted = cur.rowcount > 0
        finally:
            conn.close()
        if deleted:
            logger.info("API key deleted", extra={"extra_data": {"key_prefix": key[:8]}})
        return deleted

    def verify(self, key: str) -> bool:
        if not key:
            return False
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT 1 FROM apikeys WHERE key = ? LIMIT 1", (key,)
            ).fetchone()
        finally:
            conn.close()
        return row is not None
