from fastapi import APIRouter

from backend.app.schemas.generate import (
    GenerateApplicationRequest,
    GenerateApplicationResponse,
)
from backend.app.services.genai_service import generate_application_text

router = APIRouter()

@router.post("/application", response_model=GenerateApplicationResponse)
def generate_application(request: GenerateApplicationRequest):
    result = generate_application_text(
        resume_text=request.resume_text,
        job_description=request.job_description,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills,
    )

    return GenerateApplicationResponse(**result)