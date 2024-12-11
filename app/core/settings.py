"""
    Settings file
"""
import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Settings class
    """
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    SECRET_KEY: str = "8d0f39701a43810766d0c9fa25acd6f0097dff05c2d0322d8983969c88c81bd8"
    ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_SECRET_KEY: str = os.getenv("GOOGLE_SECRET_KEY")
    RATE_LIMIT: int = 1000
    RATE_LIMIT_WINDOW: int = 60
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS",
                                  "http://localhost:5173")
    TOKEN_EXPIRES_MINUTES: str = os.getenv("EXPIRES_MINUTES", str(15))
    TOKEN_REFRESH_MINUTES: str = os.getenv("REFRESH_MINUTES", str(60))
    TOKEN_REFRESH_EXPIRES_MINUTES: str = os.getenv("REFRESH_EXPIRES_MINUTES", str(1440))
    TOKEN_REFRESH_EXPIRES_SECONDS: str = (
            TOKEN_REFRESH_MINUTES * 60
    )
    CACHE_CONFIG = {
        "MAXSIZE": 128,
        "TTL": 300  # 5 minutes in seconds
    }

settings = Settings()
