from fastapi import FastAPI

from backend.app.api import jobs, resumes

app = FastAPI(
    title="AI Resume & Job Matching Assistant",
    description="A portfolio project for resume and job description matching.",
    version="0.3.0",
)

app.include_router(
    resumes.router,
    prefix="/api/resumes",
    tags=["resumes"],
)

app.include_router(
    jobs.router,
    prefix="/api/jobs",
    tags=["jobs"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume & Job Matching Assistant"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "0.3.0"
    }