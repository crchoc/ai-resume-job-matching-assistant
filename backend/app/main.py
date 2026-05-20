from fastapi import FastAPI

from backend.app.api import analysis, generate, jobs, match, resumes, results
from backend.app.db.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Resume & Job Matching Assistant",
    description="A portfolio project for resume and job description matching.",
    version="0.6.5",
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

app.include_router(
    match.router,
    prefix="/api/match",
    tags=["match"],
)

app.include_router(
    generate.router,
    prefix="/api/generate",
    tags=["generate"],
)

app.include_router(
    results.router,
    prefix="/api/results",
    tags=["results"],
)

app.include_router(
    analysis.router,
    prefix="/api/analysis",
    tags=["analysis"],
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
        "version": "0.6.5"
    }