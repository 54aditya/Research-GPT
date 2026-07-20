from datetime import datetime
from typing import Any
from bson import ObjectId
from app.models.project import ProjectCreate, ProjectDetail, ProjectOut, ProjectStatus, Slide


class ProjectRepository:
    def __init__(self, db: Any):
        self.collection = db.projects
        self.slides_collection = db.slides
        self.references_collection = db.references

    def create(self, payload: ProjectCreate) -> ProjectOut:
        doc = {
            "topic": payload.topic,
            "slide_count": payload.slide_count,
            "presentation_style": payload.presentation_style,
            "status": ProjectStatus.PENDING.value,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "ppt_path": None,
            "logs": [],
            "references": [],
        }
        result = self.collection.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        return ProjectOut(**doc)

    def get_many(self) -> list[ProjectOut]:
        docs = list(self.collection.find().sort("created_at", -1))
        return [ProjectOut(**{**doc, "id": str(doc["_id"])}) for doc in docs]

    def get_by_id(self, project_id: str) -> ProjectDetail | None:
        doc = self.collection.find_one({"_id": ObjectId(project_id)})
        if not doc:
            return None
        slides = list(self.slides_collection.find({"project_id": project_id}))
        references = list(self.references_collection.find({"project_id": project_id}))
        return ProjectDetail(
            **{
                **doc,
                "id": str(doc["_id"]),
                "slides": [Slide(**slide) for slide in slides],
                "references": [ref.get("citation", "") for ref in references],
                "logs": doc.get("logs", []),
            }
        )

    def update_status(self, project_id: str, status: ProjectStatus, logs: list[str] | None = None) -> None:
        update = {"status": status.value, "updated_at": datetime.utcnow()}
        if logs is not None:
            update["logs"] = logs
        self.collection.update_one({"_id": ObjectId(project_id)}, {"$set": update})

    def update_ppt_path(self, project_id: str, ppt_path: str) -> None:
        self.collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"ppt_path": ppt_path, "updated_at": datetime.utcnow()}})

    def delete(self, project_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(project_id)})
        return result.deleted_count > 0
