from __future__ import annotations


class RetrievalAgent:
    def retrieve(self, query: str, chunks: list[dict[str, str]], top_k: int = 5) -> list[dict[str, str]]:
        return chunks[:top_k]
