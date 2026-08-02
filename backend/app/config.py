import os
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default="Capital OS")
    app_env: str = Field(default="development")
    app_debug: bool = Field(default=True)
    api_prefix: str = Field(default="/api")
    database_url: str = Field(
        default="sqlite:///./capital_os.db"
    )
    secret_key: str = Field(default="change-me")
    ai_provider: str = Field(default="openai")

    class Config:
        extra = "ignore"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Capital OS"),
        app_env=os.getenv("APP_ENV", "development"),
        app_debug=os.getenv("APP_DEBUG", "true").lower() == "true",
        api_prefix=os.getenv("API_PREFIX", "/api"),
        database_url=os.getenv(
            "DATABASE_URL",
            "sqlite:///./capital_os.db",
        ),
        secret_key=os.getenv("SECRET_KEY", "change-me"),
        ai_provider=os.getenv("AI_PROVIDER", "openai"),
    )
