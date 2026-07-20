import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "AI Research Presentation Generator")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    mongodb_uri: str | None = os.getenv("MONGODB_URI")
    jwt_secret: str = os.getenv("JWT_SECRET")
    redis_url: str = os.getenv("REDIS_URL")
    qdrant_url: str = os.getenv("QDRANT_URL")
    qdrant_api_key: str | None = None
    arxiv_api_key: str | None = os.getenv("ARXIV_API_KEY")
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/uploads")
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
