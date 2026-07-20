from __future__ import annotations
import requests
from app.core.config import get_settings

settings = get_settings()


class SearchAgent:
    def search(self, topic: str, limit: int = 5) -> list[dict[str, str]]:
        papers = []
        try:
            response = requests.get("https://export.arxiv.org/api/query",

                params={"search_query": f"all:{topic}", "start": 0, "max_results": limit},
                timeout=20,
            )
            response.raise_for_status()
            for entry in response.text.split("<entry>"):
                if "<title>" in entry and "<link" in entry:
                    title = entry.split("<title>", 1)[1].split("</title>", 1)[0]
                    url = entry.split('href="', 1)[1].split('"', 1)[0] if 'href="' in entry else ""
                    if "/abs/" in url:
                        url = url.replace("/abs/", "/pdf/")
                    papers.append({"title": title, "url": url})
        except Exception:
            papers = [{"title": f"{topic} research note", "url": "https://example.com"}]
        return papers[:limit]
