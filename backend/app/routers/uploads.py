from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/pdf")
def upload_pdf(file: UploadFile = File(...)) -> dict[str, str]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    upload_dir = Path(settings.upload_dir) / "pdfs"
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / file.filename
    with destination.open("wb") as handle:
        handle.write(file.file.read())
    return {"path": str(destination)}
