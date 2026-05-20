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

### v0.2

- Added resume PDF upload API
- Saved uploaded PDF files to `data/uploads`
- Extracted text from PDF using `pypdf`
- Added `/api/resumes/upload` endpoint

### v0.3

- Added job description analysis API
- Extracted required and preferred skills from job descriptions
- Added simple keyword extraction
- Added `/api/jobs/analyze` endpoint

### v0.4

- Added match score calculation API
- Compared resume skills with job description skills
- Returned matched skills and missing skills
- Added recommendation message based on score
- Added `/api/match/analyze` endpoint


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

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check server status |
| POST | `/api/resumes/upload` | Upload resume PDF and extract text |
| POST | `/api/jobs/analyze` | Analyze job description text |
| POST | `/api/match/analyze` | Calculate resume-job match score |