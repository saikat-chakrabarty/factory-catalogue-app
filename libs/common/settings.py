from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str
    GIT_COMMIT_SHA: str = "unknown"
    LOG_LEVEL: str = "DEBUG"

    class Config:
        env_file = ".env_development"
        case_sensitive = False

settings = Settings()
