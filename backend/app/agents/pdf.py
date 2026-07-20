from __future__ import annotations
import os
import re
from pathlib import Path
import requests
import fitz
from app.core.config import get_settings

settings = get_settings()


class PDFAgent:
    def download_pdf(self, url: str, topic: str) -> str:
        if not url:
            return ""
        dest_dir = Path(settings.upload_dir) / "pdfs"
        dest_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{re.sub(r'[^a-zA-Z0-9]+', '_', topic).strip('_')}_{len(list(dest_dir.glob('*.pdf')))}.pdf"
        path = dest_dir / filename
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        path.write_bytes(response.content)
        return str(path)

    def extract_text(self, path: str) -> str:
        if not path:
            return ""
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
