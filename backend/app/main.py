from fastapi import FastAPI

app = FastAPI(
    title="AI Resume & Job Matching Assistant",
    description="A portfolio project for resume and job description matching.",
    version="0.1.0",
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
        "version": "0.1.0"
    }