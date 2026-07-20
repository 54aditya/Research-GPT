from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Slide(BaseModel):
    title: str
    content: str
    notes: str | None = None
    diagram: str | None = None
    citations: list[str] = Field(default_factory=list)


class ProjectCreate(BaseModel):
    topic: str
    slide_count: int = Field(ge=3, le=20)
    presentation_style: str = "professional"
    uploaded_files: list[str] = Field(default_factory=list)


class ProjectOut(BaseModel):
    id: str
    topic: str
    slide_count: int
    presentation_style: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    ppt_path: str | None = None


class ProjectDetail(ProjectOut):
    slides: list[Slide] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    logs: list[str] = Field(default_factory=list)
