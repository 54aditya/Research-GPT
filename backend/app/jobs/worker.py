from __future__ import annotations
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.mongodb import get_db
from app.models.project import ProjectStatus
from app.repositories.project_repository import ProjectRepository
from app.agents.planner import PlannerAgent
from app.agents.search import SearchAgent
from app.agents.pdf import PDFAgent
from app.agents.embeddings import EmbeddingAgent
from app.agents.retriever import RetrievalAgent
from app.agents.slide import SlideAgent
from app.agents.citation import CitationAgent
from app.agents.diagram import DiagramAgent
from app.agents.presentation import PresentationAgent
from app.agents.gemini import GeminiContentAgent

settings = get_settings()
logger = get_logger(__name__)


def run_pipeline(project_id: str, topic: str, slide_count: int, presentation_style: str, uploaded_files: list[str]) -> dict[str, Any]:
    db = get_db()
    repo = ProjectRepository(db)
    repo.update_status(project_id, ProjectStatus.RUNNING, ["Starting research pipeline"])

    planner = PlannerAgent()
    search = SearchAgent()
    pdf_agent = PDFAgent()
    embedding_agent = EmbeddingAgent()
    retrieval_agent = RetrievalAgent()
    slide_agent = SlideAgent()
    citation_agent = CitationAgent()
    diagram_agent = DiagramAgent()
    presentation_agent = PresentationAgent()
    gemini_agent = GeminiContentAgent()
    try:
        outline = planner.create_outline(topic, slide_count, presentation_style)
        logger.info(f"Outline created with {len(outline.get('slides', []))} slides: {[s.get('title') for s in outline.get('slides', [])]}")
        repo.update_status(project_id, ProjectStatus.RUNNING, [f"Outline created: {outline['title']}"])
    except Exception as e:
        logger.error(f"Failed to create outline: {e}")
        repo.update_status(project_id, ProjectStatus.RUNNING, ["Using default outline"])
        outline = {
            "title": topic,
            "slides": [
                {"title": f"Introduction to {topic}"},
                {"title": "Key Concepts"},
                {"title": "Current State"},
                {"title": "Future Outlook"},
                {"title": "Conclusion"}
            ]
        }

    papers = []
    texts = []

    try:
        papers = search.search(topic, 5)
        logger.info(f"Found {len(papers)} research papers")
        repo.update_status(project_id, ProjectStatus.RUNNING, [f"Found {len(papers)} papers"])

        pdf_paths = []
        for paper in papers:
            try:
                path = pdf_agent.download_pdf(paper.get("url", ""), topic)
                if path:
                    pdf_paths.append(path)
                    logger.info(f"Downloaded PDF: {path}")
            except Exception as e:
                logger.warning(f"Failed to download PDF from {paper.get('url', 'unknown')}: {e}")
                continue

        for path in pdf_paths:
            try:
                text = pdf_agent.extract_text(path)
                if text:
                    texts.append(text)
                    logger.info(f"Extracted {len(text)} characters from {path}")
            except Exception as e:
                logger.warning(f"Failed to extract text from {path}: {e}")
                continue
        logger.info(f"Total texts extracted: {len(texts)} documents")
    except Exception as e:
        logger.error(f"Failed to search/download papers: {e}")
        repo.update_status(project_id, ProjectStatus.RUNNING, ["Using default research data"])

    has_real_content = len(texts) > 0
    chunks = []
    try:
        if texts:
            chunks = embedding_agent.chunk_documents(texts)
            embedding_agent.store_chunks(chunks, topic)
            # Mark each chunk as real extracted content
            for chunk in chunks:
                chunk["is_real_content"] = True
            repo.update_status(project_id, ProjectStatus.RUNNING, [f"Created {len(chunks)} document chunks"])
        else:
            # No PDFs extracted — use empty placeholders; SlideAgent will use context templates
            chunks = [{"text": "", "is_real_content": False} for _ in range(slide_count)]
        
        # Request enough docs for all slides
        docs = retrieval_agent.retrieve(topic, chunks, top_k=slide_count)
        logger.info(f"Retrieved {len(docs)} documents for {slide_count} slides")
    except Exception as e:
        logger.error(f"Failed to process documents: {e}")
        # Let SlideAgent context templates handle content — pass empty docs
        docs = [{"text": "", "is_real_content": False} for _ in range(slide_count)]

    slides = []
    try:
        outline_slides = outline.get("slides", []) if isinstance(outline, dict) else []
        
        # Ensure we have enough docs for all requested slides
        while len(docs) < slide_count:
            docs.append({"text": "", "is_real_content": False})
        
        for index in range(slide_count):
            doc = docs[index] if index < len(docs) else {"text": "", "is_real_content": False}
            
            # Use outline slide info if available
            outline_item = outline_slides[index] if index < len(outline_slides) else {}
            slide_title = outline_item.get("title", f"Key Research Point {index + 1}")
            slide_description = outline_item.get("description", "")
            slide_focus = outline_item.get("focus", "")
            
            # Generate high-quality content using Gemini with PresentationGPT system prompt
            try:
                gemini_content = gemini_agent.generate_slide_content(
                    slide_title=slide_title,
                    topic=topic,
                    description=slide_description,
                    focus=slide_focus,
                    slide_index=index,
                    total_slides=slide_count
                )
                slide = {
                    "title": slide_title,
                    "content": gemini_content,
                    "notes": "Generated by PresentationGPT Gemini Agent"
                }
                logger.info(f"Generated slide {index + 1}/{slide_count} with Gemini: {slide_title}")
            except Exception as e:
                logger.warning(f"Gemini generation failed for slide {index + 1}, using fallback: {e}")
                # Fallback to standard slide generation
                enhanced_doc = dict(doc)
                # Pass topic and outline context so SlideAgent can generate meaningful content
                enhanced_doc["topic"] = topic
                enhanced_doc["slide_title"] = slide_title
                enhanced_doc["slide_description"] = slide_description
                enhanced_doc["slide_focus"] = slide_focus
                # If the doc contains placeholder/junk text (not real research), clear it so
                # SlideAgent falls through to the context_mapping templates
                if not doc.get("is_real_content", False):
                    enhanced_doc["text"] = ""
                
                slide = slide_agent.generate_slide(slide_title, enhanced_doc, presentation_style)
            
            slide["citations"] = citation_agent.add_citations(slide.get("content", ""), papers)
            if diagram_agent.should_generate_diagram(slide.get("content", "")):
                try:
                    slide["diagram"] = diagram_agent.create_diagram(slide_title)
                except Exception as e:
                    logger.warning(f"Failed to create diagram: {e}")
            slides.append(slide)
            logger.info(f"Generated slide {index + 1}/{slide_count}: {slide_title} with {len(slide.get('content', ''))} chars of content")
    except Exception as e:
        logger.error(f"Failed to generate slides: {e}")
        outline_slides_fb = outline.get("slides", []) if isinstance(outline, dict) else []
        slides = []
        for i in range(slide_count):
            fb_title = outline_slides_fb[i].get("title", f"Key Research Point {i + 1}") if i < len(outline_slides_fb) else f"Key Research Point {i + 1}"
            fb_doc = {"text": "", "is_real_content": False, "topic": topic, "slide_title": fb_title}
            slide = slide_agent.generate_slide(fb_title, fb_doc, presentation_style)
            slide["citations"] = []
            slides.append(slide)

    try:
        ppt_path = presentation_agent.create_presentation(topic, slides, presentation_style)
        logger.info(f"Presentation created successfully: {ppt_path}")
        logger.info(f"PPT contains {len(slides)} slides with content lengths: {[len(s.get('content', '')) for s in slides]}")
        repo.update_status(project_id, ProjectStatus.COMPLETED, ["Presentation generated successfully"])
        repo.update_ppt_path(project_id, ppt_path)
        return {"project_id": project_id, "ppt_path": ppt_path}
    except Exception as e:
        logger.error(f"Failed to create presentation: {e}")
        repo.update_status(project_id, ProjectStatus.FAILED, [f"Failed to generate presentation: {str(e)}"])
        return {"project_id": project_id, "ppt_path": None, "error": str(e)}
