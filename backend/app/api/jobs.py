from fastapi import APIRouter

from backend.app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse
from backend.app.services.job_service import analyze_job_description

router = APIRouter()


@router.post("/analyze", response_model=JobAnalyzeResponse)
def analyze_job(request: JobAnalyzeRequest):
    result = analyze_job_description(request.job_description)

    return JobAnalyzeResponse(**result)