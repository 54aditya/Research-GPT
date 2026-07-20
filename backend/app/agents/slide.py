from __future__ import annotations

class SlideAgent:
    def generate_slide(self, title: str, doc: dict[str, str], presentation_style: str) -> dict[str, str]:
        content = doc.get("text", "") or ""
        topic = doc.get("topic", "this topic")
        is_real_content = doc.get("is_real_content", bool(content and len(content.strip()) > 100))

        if is_real_content and content and len(content.strip()) > 50:
            sentences = [s.strip() for s in content.split('. ') if s.strip()]
            meaningful = [s for s in sentences if len(s) > 20 and len(s) < 400]

            if meaningful:
                num_sentences = min(8, len(meaningful))
                slide_content = '. '.join(meaningful[:num_sentences])
                if not slide_content.endswith('.'):
                    slide_content += '.'
                if len(slide_content) < 500 and len(meaningful) > num_sentences:
                    additional = '. '.join(meaningful[num_sentences:min(num_sentences + 4, len(meaningful))])
                    slide_content += ' ' + additional
                    if not slide_content.endswith('.'):
                        slide_content += '.'
                return {
                    "title": title,
                    "content": slide_content[:1200],
                    "notes": "Generated from research papers",
                }

        return {
            "title": title,
            "content": f"Analysis and research findings regarding {title} in the context of {topic}.",
            "notes": f"Generated using {presentation_style} style",
        }
