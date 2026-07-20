from __future__ import annotations
import google.generativeai as genai
from app.core.config import get_settings

settings = get_settings()


class GeminiContentAgent:
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.system_prompt = """You are PresentationGPT, an expert AI Presentation Architect.

You can create high-quality presentations on ANY topic in the world.

For every user request, you should:

- Understand the topic.
- Use the latest and most relevant information.
- Gather information from reliable sources.
- Organize the presentation with a clear beginning, middle, and conclusion.
- Create engaging slide titles.
- Write concise bullet points.
- give the content to per slide not more than 250 words.
- Suggest images, icons, graphs, flowcharts, or diagrams for each slide.
- Include real-world examples, statistics, and comparisons whenever appropriate.
- Adjust the technical depth based on the topic.
- Generate presentations suitable for students, professionals, researchers, executives, or educators.
- Return clean structured content that can be directly converted into a PowerPoint presentation.

Always prioritize factual accuracy, readability, and professional presentation design.

Your objective is to generate presentation-ready content that requires minimal editing before export to a PowerPoint (.pptx) file."""

    def generate_slide_content(self, slide_title: str, topic: str, description: str, focus: str, slide_index: int = 0, total_slides: int = 8) -> str:
        """Generate high-quality slide content using Gemini with PresentationGPT system prompt."""
        try:
            if not settings.gemini_api_key or settings.gemini_api_key.startswith("AQ."):
                raise ValueError("Missing or invalid GEMINI_API_KEY")

            prompt = f"""Generate unique and distinct content for THIS SPECIFIC SLIDE TYPE, NOT generic content.

Slide Title: {slide_title}
Topic: {topic}

This is slide {slide_index + 1} of {total_slides}.

Requirements:
1. Write clear, concise bullet points or 1-2 short paragraphs (not more than 150 words total). Avoid long walls of text.
2. Include concrete examples, statistics, or data points for THIS slide type if applicable.
3. Use professional language suitable for a presentation.
4. Structure clearly with natural flow.
5. Provide UNIQUE perspective for this slide, NOT generic information.
6. Focus on: {focus if focus else description if description else 'Key aspects'}

Generate ONLY the slide content. Do not include slide title or metadata."""

            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            raise e

    def enhance_content(self, content: str, topic: str) -> str:
        """Enhance existing content to be more engaging and comprehensive."""
        try:
            if not settings.gemini_api_key or settings.gemini_api_key.startswith("AQ."):
                raise ValueError("Missing or invalid GEMINI_API_KEY")

            prompt = f"""System: {self.system_prompt}

Enhance and expand the following presentation slide content to be more engaging, detailed, and professional:

Topic: {topic}
Current Content:
{content}

Requirements:
1. Keep length concise (150-200 words total)
2. Add specific examples, statistics, or case studies where relevant
3. Improve clarity and flow
4. Maintain professional tone
5. Include practical insights and actionable information
6. Suggest relevant visual elements (diagrams, charts, graphs)

Return ONLY the enhanced content in polished paragraph form."""

            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return content
                
        except Exception:
            return content
