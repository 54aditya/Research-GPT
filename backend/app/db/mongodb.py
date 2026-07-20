from pymongo import MongoClient
from app.core.config import get_settings

settings = get_settings()

client = MongoClient(settings.mongodb_uri) if settings.mongodb_uri else None

def get_db():
    if client is None:
        raise RuntimeError("MONGODB_URI is not configured")
    return client.get_database("ai_agent")
