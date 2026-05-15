# AI Resume & Job Matching Assistant

A portfolio project that analyzes a resume PDF and a job description to calculate skill match, identify missing skills, and generate tailored application text.

## Tech Stack

- FastAPI
- Python
- Uvicorn

## Version

### v0.1

- Created basic project structure
- Added FastAPI app
- Added `/` endpoint
- Added `/health` endpoint

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Open:
```bash
http://127.0.0.1:8000/docs
```
