import re

from backend.app.utils.skill_keywords import SKILL_KEYWORDS


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> list[str]:
    normalized = normalize_text(text)
    found_skills = []

    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, normalized):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_keywords(text: str, limit: int = 20) -> list[str]:
    normalized = normalize_text(text)

    words = re.findall(r"[a-zA-Z][a-zA-Z+#.\-/]{2,}", normalized)

    stopwords = {
        "and",
        "the",
        "for",
        "with",
        "you",
        "our",
        "are",
        "will",
        "this",
        "that",
        "from",
        "your",
        "have",
        "has",
        "work",
        "team",
        "role",
        "experience",
        "skills",
        "using",
        "based",
        "looking",
        "required",
        "preferred",
    }

    counts = {}

    for word in words:
        if word not in stopwords:
            counts[word] = counts.get(word, 0) + 1

    sorted_words = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [word for word, count in sorted_words[:limit]]