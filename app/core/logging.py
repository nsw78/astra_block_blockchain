"""
Structured JSON logging with correlation/request IDs.
"""
import logging
import json
import sys
from datetime import datetime, timezone
from typing import Optional


class JSONFormatter(logging.Formatter):
    """Outputs each log record as a single JSON line — 12-factor friendly."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        # attach request_id if present
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        # attach extra fields
        if hasattr(record, "extra_data"):
            log_entry["data"] = record.extra_data
        # attach exception info
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = {
                "type": type(record.exc_info[1]).__name__,
                "message": str(record.exc_info[1]),
            }
        return json.dumps(log_entry, default=str)


class TextFormatter(logging.Formatter):
    FMT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"

    def __init__(self):
        super().__init__(fmt=self.FMT)


def configure_logging(level: str = "INFO", fmt: str = "json") -> None:
    """Configure root logger. Call once at startup."""
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # clear existing handlers
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    if fmt == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(TextFormatter())
    root.addHandler(handler)

    # silence noisy libraries
    for name in ("uvicorn.access", "uvicorn.error", "asyncio", "httpcore", "httpx"):
        logging.getLogger(name).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"astra.{name}")
