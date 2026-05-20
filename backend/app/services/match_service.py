from backend.app.services.skill_service import extract_skills


def calculate_match_score(
    resume_text: str,
    job_description: str,
) -> dict:
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    if not job_skills:
        return {
            "match_score": 0.0,
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": "No recognizable technical skills were found in the job description.",
        }

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    match_score = round(
        len(matched_skills) / len(job_skills) * 100,
        2,
    )

    recommendation = build_recommendation(
        match_score=match_score,
        missing_skills=sorted(missing_skills),
    )

    return {
        "match_score": match_score,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "recommendation": recommendation,
    }


def build_recommendation(
    match_score: float,
    missing_skills: list[str],
) -> str:
    if match_score >= 75:
        return (
            "Strong match. Focus on showing project impact, measurable results, "
            "and responsibilities related to the matched skills."
        )

    if match_score >= 50:
        return (
            "Moderate match. Improve your resume by emphasizing relevant projects "
            "and filling key missing skills."
        )

    if missing_skills:
        top_missing = ", ".join(missing_skills[:3])

        return (
            "Weak match. Consider improving your resume or learning the most important "
            f"missing skills first: {top_missing}."
        )

    return (
        "Weak match. The job description may require skills that are not clearly listed "
        "in the resume."
    )