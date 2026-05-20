import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    genai_provider: str = os.getenv("GENAI_PROVIDER", "fallback").lower()

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./resume_matcher.db",
    )


settings = Settings()