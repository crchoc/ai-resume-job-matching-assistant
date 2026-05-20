from fastapi import APIRouter

from backend.app.schemas.match import (
    MatchAnalyzeRequest,
    MatchAnalyzeResponse,
)
from backend.app.services.match_service import calculate_match_score

router = APIRouter()


@router.post("/analyze", response_model=MatchAnalyzeResponse)
def analyze_match(request: MatchAnalyzeRequest):
    result = calculate_match_score(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    return MatchAnalyzeResponse(**result)