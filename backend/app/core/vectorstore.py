import os
import json
import faiss
import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from threading import Lock

class VectorStore:
    """
    A minimal FAISS + sidecar metadata JSON store.
    - Embeddings stored in FAISS index (IndexFlatIP cosine-like with normalized vectors).
    - Metadata stored as a list[{id, text, source, chunk_id, extra}], indexed by row id.
    """

    _instance = None
    _lock = Lock()

    def __init__(self):
        os.makedirs(settings.VECTOR_DIR, exist_ok=True)
        os.makedirs(settings.DOCS_DIR, exist_ok=True)
        self.model_name = settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self._dim = self.model.get_sentence_embedding_dimension()

    @classmethod
    def get(cls) -> "VectorStore":
        with cls._lock:
            if cls._instance is None:
                cls._instance = VectorStore()
        return cls._instance

    def _new_index(self):
        # Cosine similarity via L2-normalized vectors + Inner Product index
        return faiss.IndexFlatIP(self._dim)

    def load_or_initialize(self):
        meta_exists = os.path.exists(settings.VECTOR_META_PATH)
        index_exists = os.path.exists(settings.VECTOR_INDEX_PATH)

        if index_exists and meta_exists:
            self.index = faiss.read_index(settings.VECTOR_INDEX_PATH)
            with open(settings.VECTOR_META_PATH, "r", encoding="utf-8") as f:
                payload = json.load(f)
            self.metadata = payload.get("metadata", [])
            # Safety check for dimension mismatch
            if self.index.d != self._dim:
                # Rebuild index using saved vectors if present (not stored here)
                # For simplicity, re-embed all metadata text to rebuild
                self.rebuild_index()
        else:
            self.index = self._new_index()
            self.metadata = []

    def persist(self):
        if self.index is None:
            return
        faiss.write_index(self.index, settings.VECTOR_INDEX_PATH)
        with open(settings.VECTOR_META_PATH, "w", encoding="utf-8") as f:
            json.dump({"model": self.model_name, "metadata": self.metadata}, f, ensure_ascii=False)

    def _embed(self, texts: List[str]) -> np.ndarray:
        embs = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
        if embs.ndim == 1:
            embs = embs.reshape(1, -1)
        return embs.astype("float32")

    def add_texts(self, texts: List[str], metadatas: List[Dict]):
        assert len(texts) == len(metadatas)
        if self.index is None:
            self.load_or_initialize()

        embs = self._embed(texts)
        self.index.add(embs)
        # FAISS rows are aligned with metadata order; append sequentially
        self.metadata.extend(metadatas)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index is None or self.index.ntotal == 0:
            return []
        q = self._embed([query])  # (1, dim)
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            meta = self.metadata[idx] if idx < len(self.metadata) else {}
            results.append({
                "score": float(score),
                "index": int(idx),
                "text": meta.get("text", ""),
                "source": meta.get("source", ""),
                "chunk_id": meta.get("chunk_id", ""),
                "extra": meta.get("extra", {}),
            })
        return results

    def rebuild_index(self):
        # Rebuild from metadata text
        self.index = self._new_index()
        texts = [m.get("text", "") for m in self.metadata]
        if texts:
            embs = self._embed(texts)
            self.index.add(embs)
