"""
Healthcheck endpoint
"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.mysql import get_db

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
async def healthcheck(db: Session = Depends(get_db)):
    """
    Returns the operational status of the service and its database connection.
    Responds with 200 when healthy, 503 when the database is unreachable.
    """
    try:
        db.execute(text("SELECT 1"))
        return JSONResponse(content={"status": "healthy", "database": "connected"})
    except Exception:  # pylint: disable=broad-except
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "unreachable"},
        )
