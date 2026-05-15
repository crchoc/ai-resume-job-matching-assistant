from fastapi import APIRouter, HTTPException, UploadFile

from backend.app.services.pdf_service import (
    extract_text_from_pdf,
    save_upload_file,
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile):
    try:
        saved_path = await save_upload_file(file)
        extracted_text = extract_text_from_pdf(saved_path)

        return {
            "filename": file.filename,
            "saved_path": str(saved_path),
            "text_length": len(extracted_text),
            "text_preview": extracted_text[:1000],
            "text": extracted_text,
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {error}",
        )