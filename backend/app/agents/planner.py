from __future__ import annotations
import json
import google.generativeai as genai
from app.core.config import get_settings

settings = get_settings()


class PlannerAgent:
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def create_outline(self, topic: str, slide_count: int, presentation_style: str) -> dict[str, object]:
        try:
            if not settings.gemini_api_key or settings.gemini_api_key.startswith("AQ."):
                raise ValueError("Missing or invalid GEMINI_API_KEY")

            prompt = f"""You are a professional presentation architect.
Generate a structured slide-by-slide outline for a presentation on the topic: "{topic}".
The presentation style is "{presentation_style}".
You must generate exactly {slide_count} slides.

Each slide in the outline must contain:
1. "title": A unique, specific, and engaging title for that slide. Do NOT use generic titles like "Slide 1" or "Introduction". Every slide title must be tailored to the topic {topic}.
2. "description": A brief summary of what the slide will cover.
3. "focus": A specific key question or detail that the slide's content should focus on.

Return the result strictly as a JSON object matching this structure:
{{
  "title": "{topic} — {presentation_style.title()} Presentation",
  "slides": [
    {{
      "title": "Topic-Specific Slide Title 1",
      "description": "Slide Description 1",
      "focus": "Focus Area 1"
    }},
    ...
  ],
  "theme": "{presentation_style}"
}}

You must return exactly {slide_count} slides in the JSON list. Generate ONLY the JSON. Do not write any preamble, introduction, explanation, or markdown formatting. Just start with {{ and end with }}.
"""
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            if response and response.text:
                outline_data = json.loads(response.text.strip())
                if isinstance(outline_data, dict) and "slides" in outline_data:
                    slides = outline_data["slides"]
                    if len(slides) == slide_count:
                        return outline_data
                    elif len(slides) > 0:
                        if len(slides) > slide_count:
                            outline_data["slides"] = slides[:slide_count]
                        else:
                            while len(outline_data["slides"]) < slide_count:
                                idx = len(outline_data["slides"])
                                outline_data["slides"].append({
                                    "title": f"{topic} - Detail {idx + 1}",
                                    "description": f"Further analysis of {topic}.",
                                    "focus": f"Key aspect {idx + 1} of {topic}"
                                })
                        return outline_data

            raise Exception("Invalid or incomplete response from Gemini")

        except Exception as e:
            print(f"Error generating dynamic outline with Gemini: {e}. Falling back to default outline.")
            
            slides = []
            for i in range(slide_count):
                slides.append({
                    "title": f"{topic} - Section {i + 1}",
                    "description": f"Detailed review of key aspect {i + 1} of {topic}.",
                    "focus": f"Key point {i + 1}"
                })
            
            return {
                "title": f"{topic} — {presentation_style.title()} Presentation",
                "slides": slides,
                "theme": presentation_style,
            }
