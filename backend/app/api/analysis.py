from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.analysis_result import AnalysisResult
from backend.app.schemas.analysis import FullAnalysisResponse
from backend.app.services.genai_service import generate_application_text
from backend.app.services.job_service import analyze_job_description
from backend.app.services.match_service import calculate_match_score
from backend.app.services.pdf_service import extract_text_from_pdf, save_upload_file


router = APIRouter()


@router.post("/run", response_model=FullAnalysisResponse)
async def run_full_analysis(
    file: UploadFile,
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # 1. Save uploaded resume PDF
        saved_path = await save_upload_file(file)

        # 2. Extract resume text from PDF
        resume_text = extract_text_from_pdf(saved_path)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF. The file may be scanned or image-based.",
            )

        # 3. Analyze job description
        job_result = analyze_job_description(job_description)

        # 4. Calculate match score
        match_result = calculate_match_score(
            resume_text=resume_text,
            job_description=job_description,
        )

        # 5. Generate tailored bullets and cover letter
        generated_result = generate_application_text(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
        )

        # 6. Save final result to database
        db_result = AnalysisResult(
            resume_filename=file.filename or "uploaded_resume.pdf",
            job_title=job_result["job_title"],
            company_name=job_result["company_name"],
            match_score=match_result["match_score"],
            matched_skills=", ".join(match_result["matched_skills"]),
            missing_skills=", ".join(match_result["missing_skills"]),
            generated_bullets="\n".join(generated_result["tailored_bullets"]),
            cover_letter=generated_result["cover_letter"],
        )

        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        # 7. Return complete result
        return FullAnalysisResponse(
            result_id=db_result.id,
            resume_filename=db_result.resume_filename,
            job_title=db_result.job_title,
            company_name=db_result.company_name,
            match_score=db_result.match_score,
            resume_skills=match_result["resume_skills"],
            job_skills=match_result["job_skills"],
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            recommendation=match_result["recommendation"],
            tailored_bullets=generated_result["tailored_bullets"],
            cover_letter=generated_result["cover_letter"],
            created_at=db_result.created_at,
        )

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Full analysis failed: {error}",
        )