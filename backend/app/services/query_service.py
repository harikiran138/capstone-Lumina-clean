from typing import List, Tuple
from app.core.vectorstore import VectorStore
from app.core.llm import LocalLLMStub

class QueryService:
    def __init__(self):
        self.vs = VectorStore.get()
        self.llm = LocalLLMStub()

    def answer_query(self, query: str, top_k: int = 5, max_context_tokens: int = 1200) -> Tuple[str, List[dict]]:
        retrieved = self.vs.search(query, top_k=top_k)
        answer = self.llm.answer(query, retrieved, max_context_tokens=max_context_tokens)

        # Minimal, clean sources payload
        sources = []
        for r in retrieved:
            sources.append({
                "source": r.get("source", ""),
                "chunk_id": r.get("chunk_id", ""),
                "score": round(r.get("score", 0.0), 4),
                "preview": (r.get("text", "")[:200] + "…") if r.get("text") else ""
            })
        return answer, sources
