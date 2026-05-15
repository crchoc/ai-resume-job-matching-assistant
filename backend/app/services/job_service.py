import re

from backend.app.services.skill_service import extract_keywords, extract_skills


def guess_job_title(job_description: str) -> str:
    lines = [
        line.strip()
        for line in job_description.splitlines()
        if line.strip()
    ]

    if lines and len(lines[0]) <= 80:
        return lines[0]

    title_patterns = [
        r"backend developer",
        r"frontend developer",
        r"fullstack developer",
        r"software engineer",
        r"python developer",
        r"ai engineer",
        r"machine learning engineer",
        r"data analyst",
        r"data scientist",
        r"백엔드 개발자",
        r"프론트엔드 개발자",
        r"풀스택 개발자",
        r"소프트웨어 엔지니어",
        r"AI 엔지니어",
        r"머신러닝 엔지니어",
        r"데이터 분석가",
    ]

    lowered = job_description.lower()

    for pattern in title_patterns:
        match = re.search(pattern, lowered, re.IGNORECASE)
        if match:
            return match.group(0).title()

    return "Unknown Position"


def guess_company_name(job_description: str) -> str:
    patterns = [
        r"company[:\s]+([A-Za-z0-9가-힣 ._-]{2,50})",
        r"회사명[:\s]+([A-Za-z0-9가-힣 ._-]{2,50})",
        r"회사[:\s]+([A-Za-z0-9가-힣 ._-]{2,50})",
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Unknown Company"


def split_required_and_preferred_skills(
    job_description: str,
    skills: list[str],
) -> tuple[list[str], list[str]]:
    lowered = job_description.lower()

    preferred_markers = [
        "preferred",
        "nice to have",
        "plus",
        "우대",
        "우대사항",
        "선호",
    ]

    has_preferred_section = any(
        marker in lowered
        for marker in preferred_markers
    )

    if not has_preferred_section:
        return skills, []

    required_skills = []
    preferred_skills = []

    for skill in skills:
        skill_position = lowered.find(skill.lower())

        nearby_text = lowered[max(0, skill_position - 120): skill_position + 120]

        if any(marker in nearby_text for marker in preferred_markers):
            preferred_skills.append(skill)
        else:
            required_skills.append(skill)

    return required_skills, preferred_skills


def analyze_job_description(job_description: str) -> dict:
    skills = extract_skills(job_description)
    keywords = extract_keywords(job_description)

    required_skills, preferred_skills = split_required_and_preferred_skills(
        job_description=job_description,
        skills=skills,
    )

    return {
        "job_title": guess_job_title(job_description),
        "company_name": guess_company_name(job_description),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "keywords": keywords,
    }