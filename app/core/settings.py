"""
    Settings file
"""
from typing import ClassVar

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_DATABASE: str = ""
    SECRET_KEY: str = "8d0f39701a43810766d0c9fa25acd6f0097dff05c2d0322d8983969c88c81bd8"
    ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_SECRET_KEY: str = ""
    RATE_LIMIT: int = 1000
    RATE_LIMIT_WINDOW: int = 60
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = ""
    FRONTEND_URL: str = ""
    CORS_ORIGINS: str = "http://localhost:5173"
    TOKEN_EXPIRES_MINUTES: str = "15"
    TOKEN_REFRESH_MINUTES: str = "60"
    TOKEN_REFRESH_EXPIRES_MINUTES: str = "1440"
    TOKEN_REFRESH_EXPIRES_SECONDS: str = ""

    CACHE_CONFIG: ClassVar[dict] = {"MAXSIZE": 128, "TTL": 300}

    @model_validator(mode='after')
    def compute_token_seconds(self) -> 'Settings':
        """Compute TOKEN_REFRESH_EXPIRES_SECONDS from TOKEN_REFRESH_MINUTES."""
        self.TOKEN_REFRESH_EXPIRES_SECONDS = str(int(self.TOKEN_REFRESH_MINUTES) * 60)
        return self


settings = Settings()
