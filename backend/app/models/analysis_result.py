from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    job_title: Mapped[str] = mapped_column(
        String(255),
        default="Unknown Position",
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        default="Unknown Company",
    )

    match_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    matched_skills: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    missing_skills: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    generated_bullets: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    cover_letter: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )