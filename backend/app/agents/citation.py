from __future__ import annotations


class CitationAgent:
    def add_citations(self, content: str, papers: list[dict[str, str]]) -> list[str]:
        citations = []
        for paper in papers[:3]:
            citations.append(paper.get("title", "Unknown source"))
        return citations
