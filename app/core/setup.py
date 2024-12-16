"""
Set up the app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.core.middleware.rate_limit import RateLimitMiddleware
from app.db.mysql import SessionLocal


def create_app() -> FastAPI:
    """
    Create the FastAPI app
    :return: FastAPI app
    """
    app = FastAPI(
        title="Notes BE",
        contact={
            "name": "Alberto Barrago",
            "email": "albertobarrago@gmail.com",
        },
        description="An API for creating and managing notes",
        version="1.1.0",
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    origins = settings.CORS_ORIGINS.split(",")

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.add_middleware(
        RateLimitMiddleware,  # type: ignore
        db_session=SessionLocal
    )

    return app
