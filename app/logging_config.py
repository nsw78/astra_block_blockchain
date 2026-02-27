"""DEPRECATED — use app.core.logging instead. Kept for backward compat."""
from app.core.logging import configure_logging as _configure  # noqa: F401


def configure_logging():
    _configure(level="INFO", fmt="text")
