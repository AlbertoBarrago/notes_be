"""
 Main: Entry point for execution
"""
from pathlib import Path

from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import (
    healthcheck_router,
    auth_router,
    backoffice_router,
    notes_router,
    users_router,
    home_router,
    oauth_router
)
from app.core.setup import create_app

BASE_DIR = Path(__file__).resolve().parent.parent
app = create_app()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(healthcheck_router, tags=["Healthcheck"])
app.include_router(home_router, tags=["home"])
app.include_router(
    auth_router, prefix="/api/v1", tags=["Authorization"])
app.include_router(
    oauth_router, prefix="/api/v1", tags=["OAuth"])
app.include_router(
    users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(
    notes_router, prefix="/api/v1/notes", tags=["Notes"])
app.include_router(
    backoffice_router, prefix="/api/v1/backoffice", tags=["BackOffice"])
