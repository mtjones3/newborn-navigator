import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

_default_db = f"sqlite:///{BASE_DIR / 'newborn_navigator.db'}"


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL", _default_db)
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH: str = os.getenv(
        "ADMIN_PASSWORD_HASH",
        # default hash for "admin123"
        "$2b$12$kO8UzrldxQOOazIWrZo5deAB6VjR13A./5PDKb0RN3Mc26.mNoirq",
    )
    DATABASE_URL: str = _get_database_url()
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "hello@newborn-navigator.com")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours


settings = Settings()
