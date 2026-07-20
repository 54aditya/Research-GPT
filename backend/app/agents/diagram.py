from __future__ import annotations


class DiagramAgent:
    def should_generate_diagram(self, content: str) -> bool:
        return "architecture" in content.lower() or "workflow" in content.lower()

    def create_diagram(self, title: str) -> str:
        return f"graph TD\nA[{title}] --> B[Key Insight]"
