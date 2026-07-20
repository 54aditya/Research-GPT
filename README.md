# AI Research Presentation Generator

A full-stack AI application that accepts a research topic, slide count, presentation style, and optional PDFs, then runs a multi-agent workflow to search papers, download PDFs, chunk and embed content, retrieve relevant context, generate slide content, and create a PowerPoint presentation.

## Quick start

1. Add environment variables in a `.env` file or shell.
2. Install backend dependencies:
   - `pip install -r backend/requirements.txt`
3. Install frontend dependencies:
   - `cd frontend && npm install`
4. Start the backend:
   - `uvicorn app.main:app --reload`
5. Start the frontend:
   - `cd frontend && npm run dev`
6. Or use Docker Compose:
   - `docker compose -f docker/docker-compose.yml up`

## Required environment variables

- GEMINI_API_KEY
- MONGODB_URI
- JWT_SECRET
- REDIS_URL
- QDRANT_URL
- QDRANT_API_KEY
- ARXIV_API_KEY
