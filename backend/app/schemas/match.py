from pydantic import BaseModel


class MatchAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class MatchAnalyzeResponse(BaseModel):
    match_score: float
    resume_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str