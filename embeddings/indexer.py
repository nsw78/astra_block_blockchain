import os
from typing import List, Tuple, Optional
import numpy as np
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FAISS_INDEX_PATH = os.getenv('FAISS_INDEX_PATH', './data/faiss.index')

# Optional imports
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
    import openai
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        OPENAI_AVAILABLE = True
    else:
        OPENAI_AVAILABLE = False
except Exception:
    OPENAI_AVAILABLE = False


class Indexer:
    """Flexible indexer: prefers OpenAI embeddings (if API key provided),
    falls back to sentence-transformers+faiss if available, else TF-IDF.
    Persists index to disk when possible.
    """

    def __init__(self, index_path: Optional[str] = None):
        self.index_path = index_path or FAISS_INDEX_PATH
        self.ids: List[str] = []
        self.dim: Optional[int] = None
        self.faiss_index = None
        self.vectors: Optional[np.ndarray] = None
        self.use_openai = OPENAI_AVAILABLE
        self.use_sentence = SENTENCE_AVAILABLE and not self.use_openai
        if self.use_sentence:
            self.model = SentenceTransformer(MODEL_NAME)
        # attempt to load persisted index
        if FAISS_AVAILABLE and os.path.exists(self.index_path):
            try:
                self.faiss_index = faiss.read_index(self.index_path)
                ids_path = self.index_path + '.ids.npy'
                if os.path.exists(ids_path):
                    self.ids = list(np.load(ids_path).tolist())
                    self.dim = int(self.faiss_index.d)
            except Exception:
                # ignore load errors
                self.faiss_index = None

    def _embed_openai(self, texts: List[str]) -> np.ndarray:
        if not OPENAI_AVAILABLE:
            raise RuntimeError('OpenAI not configured')
        # use batching if needed
        embeds = []
        for chunk in texts:
            resp = openai.Embedding.create(model='text-embedding-3-small', input=chunk)
            embeds.append(resp['data'][0]['embedding'])
        return np.array(embeds, dtype=np.float32)

    def _embed_sentence(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)

    def _ensure_faiss(self, dim: int):
        if not FAISS_AVAILABLE:
            return
        if self.faiss_index is None:
            self.faiss_index = faiss.IndexFlatL2(dim)
            self.dim = dim

    def add_texts(self, texts: List[str], ids: Optional[List[str]] = None):
        if ids is None:
            ids = [str(i) for i in range(len(self.ids), len(self.ids) + len(texts))]
        # choose embedding backend
        if self.use_openai:
            embs = self._embed_openai(texts)
        elif self.use_sentence:
            embs = self._embed_sentence(texts)
            embs = embs.astype(np.float32)
        else:
            # TF-IDF fallback
            from sklearn.feature_extraction.text import TfidfVectorizer
            if self.vectors is None:
                self.vectorizer = TfidfVectorizer()
                X = self.vectorizer.fit_transform(texts).toarray().astype(np.float32)
                self.vectors = X
            else:
                X = self.vectorizer.transform(texts).toarray().astype(np.float32)
                self.vectors = np.vstack([self.vectors, X])
            self.ids.extend(ids)
            self._persist()
            return

        # use faiss if available
        if FAISS_AVAILABLE:
            self._ensure_faiss(embs.shape[1])
            if self.faiss_index is None:
                raise RuntimeError('faiss unavailable')
            self.faiss_index.add(embs)
            self.ids.extend(ids)
            self._persist()
        else:
            # keep in-memory numpy array
            if self.vectors is None:
                self.vectors = embs
            else:
                self.vectors = np.vstack([self.vectors, embs])
            self.ids.extend(ids)
            self._persist()

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        # embed query
        if self.use_openai:
            q_emb = self._embed_openai([query])
        elif self.use_sentence:
            q_emb = self._embed_sentence([query]).astype(np.float32)
        else:
            if self.vectors is None:
                return []
            q_vec = self.vectorizer.transform([query]).toarray().astype(np.float32)
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(q_vec, self.vectors)[0]
            top_idx = np.argsort(-sims)[:k]
            return [(self.ids[int(i)], float(sims[int(i)])) for i in top_idx]

        if FAISS_AVAILABLE and self.faiss_index is not None:
            D, I = self.faiss_index.search(q_emb, k)
            results = []
            for score, idx in zip(D[0], I[0]):
                if idx < len(self.ids):
                    results.append((self.ids[idx], float(score)))
            return results
        else:
            if self.vectors is None:
                return []
            # cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(q_emb, self.vectors)[0]
            top_idx = np.argsort(-sims)[:k]
            return [(self.ids[int(i)], float(sims[int(i)])) for i in top_idx]

    def _persist(self):
        # ensure data dir
        d = os.path.dirname(self.index_path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        if FAISS_AVAILABLE and self.faiss_index is not None:
            try:
                faiss.write_index(self.faiss_index, self.index_path)
                np.save(self.index_path + '.ids.npy', np.array(self.ids, dtype=object))
                return
            except Exception:
                pass
        # fallback persist
        if self.vectors is not None:
            np.save(self.index_path + '.vectors.npy', self.vectors)
            np.save(self.index_path + '.ids.npy', np.array(self.ids, dtype=object))


def build_index_from_texts(texts: List[str]) -> Indexer:
    idx = Indexer()
    ids = [f'doc_{i}' for i in range(len(texts))]
    idx.add_texts(texts, ids)
    return idx
