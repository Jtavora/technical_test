from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = Field(default="local")
    APP_NAME: str = Field(default="Email Classification API")

    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./emails.db",
        description="URL de conexão do banco de dados",
    )

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")

    class Config:
        # Load the .env colocated with the app package regardless of cwd.
        env_file = Path(__file__).resolve().parents[1] / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
