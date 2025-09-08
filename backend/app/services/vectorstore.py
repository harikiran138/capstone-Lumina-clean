import faiss
import numpy as np
from typing import List, Dict, Any

class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.index = None
            cls._instance.payloads: Dict[int, Dict[str, Any]] = {}
            cls._instance.dimension = 384  # For all-MiniLM-L6-v2
        return cls._instance

    def _ensure_index(self):
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)

    def upsert(self, points: List[Dict[str, Any]]):
        self._ensure_index()
        vectors = []
        ids = []
        for point in points:
            vectors.append(point["vector"])
            ids.append(point["id"])
            self.payloads[point["id"]] = point["payload"]
        
        vectors_np = np.array(vectors).astype("float32")
        self.index.add(vectors_np)

    def search(self, vector: List[float], limit: int = 5):
        self._ensure_index()
        query_np = np.array([vector]).astype("float32")
        distances, indices = self.index.search(query_np, limit)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  # FAISS returns -1 if no result
                payload = self.payloads.get(idx, {})
                results.append(type('Result', (), {'payload': payload, 'score': float(dist)})())
        return results
