import json

from backend.app.core.config import settings


def generate_application_text(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    provider = settings.genai_provider

    if provider == "groq":
        return generate_with_groq(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

    if provider == "openai":
        return generate_with_openai(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

    return fallback_generation(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )


def generate_with_groq(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    if not settings.groq_api_key:
        return fallback_with_note(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            note="GROQ_API_KEY is missing. Fallback generation was used.",
        )

    try:
        from groq import Groq

        client = Groq(api_key=settings.groq_api_key)

        prompt = build_prompt(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate honest, job-specific resume bullet points "
                        "and cover letter drafts. Return valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.4,
        )

        raw_text = response.choices[0].message.content or ""

        return parse_llm_json_or_fallback(
            raw_text=raw_text,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            provider_name="Groq",
        )

    except Exception as error:
        return fallback_with_note(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            note=f"Groq API call failed. Fallback generation was used. Reason: {error}",
        )


def generate_with_openai(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    if not settings.openai_api_key:
        return fallback_with_note(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            note="OPENAI_API_KEY is missing. Fallback generation was used.",
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)

        prompt = build_prompt(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0.4,
        )

        raw_text = response.output_text

        return parse_llm_json_or_fallback(
            raw_text=raw_text,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            provider_name="OpenAI",
        )

    except Exception as error:
        return fallback_with_note(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            note=f"OpenAI API call failed. Fallback generation was used. Reason: {error}",
        )


def build_prompt(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> str:
    return f"""
You are helping a junior backend / AI application developer tailor a job application.

Use only the information provided in the resume text.
Do not invent companies, degrees, certifications, employment history, or achievements.
If the resume only shows project experience, describe it honestly as project experience.

Resume text:
{resume_text[:4000]}

Job description:
{job_description[:4000]}

Matched skills:
{matched_skills}

Missing skills:
{missing_skills}

Return valid JSON only.

Required JSON format:
{{
  "tailored_bullets": [
    "bullet point 1",
    "bullet point 2",
    "bullet point 3",
    "bullet point 4",
    "bullet point 5"
  ],
  "cover_letter": "short cover letter draft"
}}

Rules:
- Write in English.
- Keep the tone professional and honest.
- Make the bullet points suitable for a resume.
- Focus on backend, API, database, data processing, AI application, and portfolio project experience when relevant.
- Do not claim that the applicant already has missing skills.
- The cover letter should be 2 to 4 short paragraphs.
"""


def parse_llm_json_or_fallback(
    raw_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
    provider_name: str,
) -> dict:
    try:
        parsed = json.loads(raw_text)

        tailored_bullets = parsed.get("tailored_bullets", [])
        cover_letter = parsed.get("cover_letter", "")

        if not isinstance(tailored_bullets, list):
            tailored_bullets = []

        if not isinstance(cover_letter, str):
            cover_letter = ""

        if tailored_bullets and cover_letter:
            return {
                "tailored_bullets": tailored_bullets,
                "cover_letter": cover_letter,
            }

        return fallback_with_note(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            note=f"{provider_name} returned JSON, but required fields were missing. Fallback generation was used.",
        )

    except json.JSONDecodeError:
        fallback = fallback_generation(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

        fallback["cover_letter"] = (
            fallback["cover_letter"]
            + f"\n\n[Note: {provider_name} returned non-JSON text, so fallback generation was used.]"
            + f"\n\nRaw model output:\n{raw_text[:1000]}"
        )

        return fallback


def fallback_with_note(
    matched_skills: list[str],
    missing_skills: list[str],
    note: str,
) -> dict:
    fallback = fallback_generation(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )

    fallback["cover_letter"] = (
        fallback["cover_letter"]
        + f"\n\n[Note: {note}]"
    )

    return fallback


def fallback_generation(
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    matched_text = (
        ", ".join(matched_skills[:5])
        if matched_skills
        else "relevant technical skills"
    )

    missing_text = (
        ", ".join(missing_skills[:3])
        if missing_skills
        else "the company's technical environment"
    )

    bullets = [
        f"Built backend-focused projects using {matched_text}, with emphasis on clean API design and practical implementation.",
        "Developed structured data processing workflows to extract, analyze, and present information from user-provided inputs.",
        "Implemented portfolio projects with attention to version control, documentation, and reproducible setup instructions.",
        "Applied problem-solving skills to connect user requirements with working software features.",
        f"Continuously improving knowledge in {missing_text} to better align with industry requirements.",
    ]

    cover_letter = (
        "Dear Hiring Manager,\n\n"
        "I am interested in this position because it matches my goal of building practical backend and AI-assisted applications. "
        f"My experience includes projects involving {matched_text}, and I am comfortable learning new technologies needed for the role.\n\n"
        "I would welcome the opportunity to contribute as a junior developer while continuing to grow through real production tasks.\n\n"
        "Sincerely,"
    )

    return {
        "tailored_bullets": bullets,
        "cover_letter": cover_letter,
    }