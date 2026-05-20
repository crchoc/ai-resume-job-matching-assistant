from pydantic import BaseModel


class GenerateApplicationRequest(BaseModel):
    resume_text: str
    job_description: str
    matched_skills: list[str]
    missing_skills: list[str]


class GenerateApplicationResponse(BaseModel):
    tailored_bullets: list[str]
    cover_letter: str