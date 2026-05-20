from datetime import datetime

from pydantic import BaseModel


class SaveResultRequest(BaseModel):
    resume_filename: str
    job_title: str = "Unknown Position"
    company_name: str = "Unknown Company"
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    generated_bullets: list[str] = []
    cover_letter: str = ""


class SavedResultResponse(BaseModel):
    id: int
    resume_filename: str
    job_title: str
    company_name: str
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    generated_bullets: list[str]
    cover_letter: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }