import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    GIT_COMMIT_SHA: str = "unknown"
    LOG_LEVEL: str = "DEBUG"

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env_development")
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
