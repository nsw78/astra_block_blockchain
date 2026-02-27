"""
Vector indexer service — wraps the embedding/search engine.
"""
import os
from typing import List, Optional, Tuple

import numpy as np

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("service.indexer")

# Optional heavy-weight imports — graceful degradation
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_AVAILABLE = True
except Exception:
    SENTENCE_AVAILABLE = False

try:
    import openai as _openai_mod
    _settings = get_settings()
    if _settings.OPENAI_API_KEY:
        _openai_mod.api_key = _settings.OPENAI_API_KEY
        OPENAI_AVAILABLE = True
    else:
        OPENAI_AVAILABLE = False
except Exception:
    OPENAI_AVAILABLE = False


class IndexerService:
    """Flexible vector indexer: OpenAI > sentence-transformers+FAISS > TF-IDF."""

    def __init__(self, index_path: Optional[str] = None) -> None:
        settings = get_settings()
        self.index_path = index_path or settings.FAISS_INDEX_PATH
        self.ids: List[str] = []
        self.dim: Optional[int] = None
        self.faiss_index = None
        self.vectors: Optional[np.ndarray] = None
        self.use_openai = OPENAI_AVAILABLE
        self.use_sentence = SENTENCE_AVAILABLE and not self.use_openai
        self._vectorizer = None  # lazy TF-IDF

        if self.use_sentence:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Using sentence-transformers backend")
        elif self.use_openai:
            logger.info("Using OpenAI embeddings backend")
        else:
            logger.info("Using TF-IDF fallback backend")

        self._try_load_persisted()

    # ── embedding backends ──

    def _embed_openai(self, texts: List[str]) -> np.ndarray:
        import openai
        embeds = []
        for chunk in texts:
            resp = openai.Embedding.create(model="text-embedding-3-small", input=chunk)
            embeds.append(resp["data"][0]["embedding"])
        return np.array(embeds, dtype=np.float32)

    def _embed_sentence(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True).astype(np.float32)

    # ── persistence ──

    def _try_load_persisted(self) -> None:
        if FAISS_AVAILABLE and os.path.exists(self.index_path):
            try:
                self.faiss_index = faiss.read_index(self.index_path)
                ids_path = self.index_path + ".ids.npy"
                if os.path.exists(ids_path):
                    self.ids = list(np.load(ids_path, allow_pickle=True).tolist())
                    self.dim = int(self.faiss_index.d)
                logger.info("Loaded persisted FAISS index", extra={"extra_data": {"docs": len(self.ids)}})
            except Exception:
                self.faiss_index = None

    def _persist(self) -> None:
        d = os.path.dirname(self.index_path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        if FAISS_AVAILABLE and self.faiss_index is not None:
            try:
                faiss.write_index(self.faiss_index, self.index_path)
                np.save(self.index_path + ".ids.npy", np.array(self.ids, dtype=object))
                return
            except Exception:
                pass
        if self.vectors is not None:
            np.save(self.index_path + ".vectors.npy", self.vectors)
            np.save(self.index_path + ".ids.npy", np.array(self.ids, dtype=object))

    def _ensure_faiss(self, dim: int) -> None:
        if not FAISS_AVAILABLE:
            return
        if self.faiss_index is None:
            self.faiss_index = faiss.IndexFlatL2(dim)
            self.dim = dim

    # ── public ──

    def add_texts(self, texts: List[str], ids: Optional[List[str]] = None) -> int:
        if ids is None:
            ids = [str(i) for i in range(len(self.ids), len(self.ids) + len(texts))]

        if self.use_openai:
            embs = self._embed_openai(texts)
        elif self.use_sentence:
            embs = self._embed_sentence(texts)
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            if self.vectors is None:
                self._vectorizer = TfidfVectorizer()
                X = self._vectorizer.fit_transform(texts).toarray().astype(np.float32)
                self.vectors = X
            else:
                X = self._vectorizer.transform(texts).toarray().astype(np.float32)
                self.vectors = np.vstack([self.vectors, X])
            self.ids.extend(ids)
            self._persist()
            return len(texts)

        if FAISS_AVAILABLE:
            self._ensure_faiss(embs.shape[1])
            self.faiss_index.add(embs)
        else:
            self.vectors = embs if self.vectors is None else np.vstack([self.vectors, embs])

        self.ids.extend(ids)
        self._persist()
        logger.info("Indexed documents", extra={"extra_data": {"count": len(texts)}})
        return len(texts)

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        if self.use_openai:
            q_emb = self._embed_openai([query])
        elif self.use_sentence:
            q_emb = self._embed_sentence([query])
        else:
            if self.vectors is None or self._vectorizer is None:
                return []
            q_vec = self._vectorizer.transform([query]).toarray().astype(np.float32)
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(q_vec, self.vectors)[0]
            top_idx = np.argsort(-sims)[:k]
            return [(self.ids[int(i)], float(sims[int(i)])) for i in top_idx]

        if FAISS_AVAILABLE and self.faiss_index is not None:
            D, I = self.faiss_index.search(q_emb, k)
            results = []
            for score, idx in zip(D[0], I[0]):
                if 0 <= idx < len(self.ids):
                    results.append((self.ids[idx], float(score)))
            return results

        if self.vectors is None:
            return []
        from sklearn.metrics.pairwise import cosine_similarity
        sims = cosine_similarity(q_emb, self.vectors)[0]
        top_idx = np.argsort(-sims)[:k]
        return [(self.ids[int(i)], float(sims[int(i)])) for i in top_idx]

    @property
    def doc_count(self) -> int:
        return len(self.ids)


def build_default_index() -> IndexerService:
    """Build the starter index with sample documents."""
    svc = IndexerService()
    sample_texts = [
        "Uniswap V2 pair contract example",
        "ERC20 token with mint function and owner control",
        "Typical rugpull pattern: owner can drain liquidity",
    ]
    if svc.doc_count == 0:
        svc.add_texts(sample_texts, [f"doc_{i}" for i in range(len(sample_texts))])
        logger.info("Default sample index built")
    return svc
