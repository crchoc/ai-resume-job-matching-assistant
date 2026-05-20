from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.analysis_result import AnalysisResult
from backend.app.schemas.results import SaveResultRequest, SavedResultResponse


router = APIRouter()


@router.post("/save", response_model=SavedResultResponse)
def save_result(
    request: SaveResultRequest,
    db: Session = Depends(get_db),
):
    result = AnalysisResult(
        resume_filename=request.resume_filename,
        job_title=request.job_title,
        company_name=request.company_name,
        match_score=request.match_score,
        matched_skills=", ".join(request.matched_skills),
        missing_skills=", ".join(request.missing_skills),
        generated_bullets="\n".join(request.generated_bullets),
        cover_letter=request.cover_letter,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return convert_to_response(result)


@router.get("", response_model=list[SavedResultResponse])
def list_results(
    db: Session = Depends(get_db),
):
    results = (
        db.query(AnalysisResult)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )

    return [
        convert_to_response(result)
        for result in results
    ]


def convert_to_response(
    result: AnalysisResult,
) -> SavedResultResponse:
    return SavedResultResponse(
        id=result.id,
        resume_filename=result.resume_filename,
        job_title=result.job_title,
        company_name=result.company_name,
        match_score=result.match_score,
        matched_skills=split_text_list(result.matched_skills),
        missing_skills=split_text_list(result.missing_skills),
        generated_bullets=split_lines(result.generated_bullets),
        cover_letter=result.cover_letter,
        created_at=result.created_at,
    )


def split_text_list(value: str) -> list[str]:
    if not value:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def split_lines(value: str) -> list[str]:
    if not value:
        return []

    return [
        line.strip()
        for line in value.splitlines()
        if line.strip()
    ]