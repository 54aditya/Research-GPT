from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response
from app.db.mongodb import get_db
from app.models.project import ProjectCreate, ProjectDetail, ProjectOut, ProjectStatus
from app.repositories.project_repository import ProjectRepository
from app.services.pipeline import run_research_pipeline
from app.core.config import get_settings

settings = get_settings()

router = APIRouter()


@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate) -> ProjectOut:
    db = get_db()
    repo = ProjectRepository(db)
    project = repo.create(payload)
    run_research_pipeline(str(project.id), payload.topic, payload.slide_count, payload.presentation_style, payload.uploaded_files)
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects() -> list[ProjectOut]:
    db = get_db()
    repo = ProjectRepository(db)
    return repo.get_many()


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: str) -> ProjectDetail:
    db = get_db()
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: str) -> dict[str, str]:
    db = get_db()
    repo = ProjectRepository(db)
    deleted = repo.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"message": "Project deleted"}


@router.get("/{project_id}/status")
def get_status(project_id: str) -> dict[str, str]:
    db = get_db()
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"status": project.status.value}


@router.get("/{project_id}/download")
def download_project(project_id: str) -> FileResponse:
    db = get_db()
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not project.ppt_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presentation not yet generated")
    
    file_path = Path(project.ppt_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presentation file not found")
    
    safe_filename = f"{project.topic.replace(' ', '_')}.pptx"
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=safe_filename,
        headers={
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


