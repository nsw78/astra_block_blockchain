"""Tests for the indexer service."""
from app.services.indexer_service import IndexerService


def test_indexer_basic():
    svc = IndexerService(index_path="./data/test_index")
    docs = ["alpha beta", "gamma delta", "owner can drain liquidity"]
    svc.add_texts(docs, ["d0", "d1", "d2"])
    results = svc.search("owner drain", k=3)
    assert isinstance(results, list)
    assert len(results) >= 1


def test_indexer_add_and_count():
    svc = IndexerService(index_path="./data/test_index2")
    svc.add_texts(["hello world", "foo bar"], ["a", "b"])
    assert svc.doc_count == 2
