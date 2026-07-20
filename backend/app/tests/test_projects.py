from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from app.models.project import ProjectCreate
from app.models.user import UserOut
from app.routers.projects import create_project


def test_create_project_accepts_user_model() -> None:
    payload = ProjectCreate(topic="AI research", slide_count=8, presentation_style="modern", uploaded_files=[])

    with patch("app.routers.projects.get_db", return_value=None), patch("app.routers.projects.ProjectRepository") as repo_cls, patch("app.routers.projects.run_research_pipeline") as run_pipeline:
        repo = repo_cls.return_value
        repo.create.return_value = SimpleNamespace(id="project-123")

        result = create_project(payload)

        assert result.id == "project-123"
        repo.create.assert_called_once_with(payload)
        run_pipeline.assert_called_once_with("project-123", "AI research", 8, "modern", [])
