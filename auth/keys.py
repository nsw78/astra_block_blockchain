import os
import sqlite3
import secrets
from typing import List, Tuple

DB_PATH = os.getenv('APIKEY_DB_PATH', './data/apikeys.db')


def _conn():
    d = os.path.dirname(DB_PATH)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS apikeys (
            key TEXT PRIMARY KEY,
            name TEXT,
            created_at INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def create_key(name: str = None) -> str:
    init_db()
    key = secrets.token_urlsafe(32)
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO apikeys (key, name, created_at) VALUES (?, ?, strftime('%s','now'))", (key, name))
    conn.commit()
    conn.close()
    return key


def list_keys() -> List[Tuple[str, str]]:
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT key, name, created_at FROM apikeys ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [(r['key'], r['name']) for r in rows]


def delete_key(key: str) -> bool:
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM apikeys WHERE key = ?", (key,))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def verify_key(key: str) -> bool:
    if not key:
        return False
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM apikeys WHERE key = ? LIMIT 1", (key,))
    ok = cur.fetchone() is not None
    conn.close()
    return ok
