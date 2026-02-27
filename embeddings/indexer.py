"""DEPRECATED — use app.services.indexer_service instead."""
from app.services.indexer_service import IndexerService as Indexer  # noqa: F401
from app.services.indexer_service import build_default_index


def build_index_from_texts(texts):
    svc = Indexer()
    ids = [f"doc_{i}" for i in range(len(texts))]
    svc.add_texts(texts, ids)
    return svc
