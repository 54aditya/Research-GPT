from __future__ import annotations
import os
import tempfile
from typing import Any
from redis import Redis
from rq import Queue
from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

queue = Queue(connection=Redis.from_url(settings.redis_url))


def run_research_pipeline(*args: Any, **kwargs: Any):
    return queue.enqueue("app.jobs.worker.run_pipeline", *args, **kwargs)


class ResearchPipelineService:
    def __init__(self) -> None:
        self.queue = queue
