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