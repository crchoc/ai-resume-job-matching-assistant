from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from pypdf import PdfReader


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_file(file: UploadFile) -> Path:
    if not file.filename:
        raise ValueError("Filename is missing.")

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    content = await file.read()
    file_path.write_bytes(content)

    return file_path


def extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    return "\n".join(pages_text).strip()