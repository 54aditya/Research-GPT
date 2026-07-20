from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logging import get_logger
from app.routers import projects, uploads

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://research-gpt-ashy.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(uploads.router, prefix="/upload", tags=["uploads"])




@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
