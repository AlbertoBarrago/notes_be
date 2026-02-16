"""
BackOffice Endpoint — Admin-only routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.models.user.model import User
from app.db.mysql import get_db, get_current_user
from app.repositories.backoffice.repository import BackofficeManager
from app.schemas.common.responses import CommonResponses

router = APIRouter()


@router.get("/users",
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def get_all_users(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated list of all users (admin only).
    """
    return BackofficeManager(db).get_all_users(
        current_user, page=page, page_size=page_size
    )


@router.get("/notes",
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def get_all_notes(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated list of all notes (admin only).
    """
    return BackofficeManager(db).get_all_notes(
        current_user, page=page, page_size=page_size
    )


@router.get("/audit",
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def get_audit_logs(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated list of audit logs (admin only).
    """
    return BackofficeManager(db).get_audit_logs(
        current_user, page=page, page_size=page_size
    )
