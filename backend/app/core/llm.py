from typing import List, Dict
import textwrap

class LocalLLMStub:
    """
    A lightweight, deterministic extractive summarizer:
    - Concatenates top chunks (respecting token-ish budget).
    - Produces a structured answer + bullet sources.
    Replace later with a local LLM (Ollama / llama.cpp).
    """

    def __init__(self):
        pass

    @staticmethod
    def _trim_context(chunks: List[Dict], max_chars: int) -> List[Dict]:
        total = 0
        kept = []
        for c in chunks:
            t = c["text"]
            if total + len(t) + 1 <= max_chars:
                kept.append(c)
                total += len(t)
            else:
                # take partial end if useful
                remain = max_chars - total
                if remain > 200:
                    kept.append({**c, "text": t[:remain]})
                    total = max_chars
                break
        return kept

    def answer(self, question: str, retrieved: List[Dict], max_context_tokens: int = 1200) -> str:
        # Very rough char budget assuming ~4 chars/token
        char_budget = max_context_tokens * 4
        context = self._trim_context(retrieved, char_budget)

        bullets = []
        for r in context:
            line = r["text"].strip().replace("\n", " ")
            if len(line) > 240:
                line = line[:240] + "…"
            bullets.append(f"- {line}")

        if not bullets:
            return "I couldn't find relevant context in the knowledge base yet. Try ingesting documents first."

        synthesis = textwrap.dedent(f"""
        Answer (context-based):
        - Your question: "{question}"

        Key points from retrieved context:
        {chr(10).join(bullets[:8])}

        Synthesis:
        """).strip()

        # Primitive "synthesis": concatenate top 2–3 statements into a coherent paragraph
        top = [r["text"].strip().replace("\n", " ") for r in context[:3]]
        para = " ".join(top)
        if len(para) > 700:
            para = para[:700] + "…"

        return synthesis + "\n" + para
