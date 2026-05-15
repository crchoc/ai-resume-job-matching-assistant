from pydantic import BaseModel


class JobAnalyzeRequest(BaseModel):
    job_description: str


class JobAnalyzeResponse(BaseModel):
    job_title: str
    company_name: str
    required_skills: list[str]
    preferred_skills: list[str]
    keywords: list[str]