from datetime import datetime

from pydantic import BaseModel


class FullAnalysisResponse(BaseModel):
    result_id: int
    resume_filename: str

    job_title: str
    company_name: str

    match_score: float
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str

    tailored_bullets: list[str]
    cover_letter: str

    created_at: datetime