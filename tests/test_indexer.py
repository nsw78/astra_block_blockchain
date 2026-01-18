from embeddings.indexer import build_index_from_texts


def test_indexer_basic():
    docs = ["alpha beta", "gamma delta", "owner can drain liquidity"]
    idx = build_index_from_texts(docs)
    res = idx.search('owner drain', k=3)
    assert isinstance(res, list)
    assert len(res) >= 1
