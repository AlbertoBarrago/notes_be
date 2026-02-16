"""
Backoffice Manager
"""
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions.user import UserErrorHandler
from app.db.models import Note, User, Audit
from app.dto.audit.audit_dto import AuditDTO
from app.dto.note.note_dto import NoteDTO
from app.dto.user.user_dto import UserDTO
from app.repositories.auth.common.services import CommonService
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger


class BackofficeManager:
    """
    Backoffice manager class — admin-only operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def _check_admin(self, current_user: User) -> None:
        """Verify current user has ADMIN role."""
        if current_user.role != "ADMIN":
            UserErrorHandler.raise_unauthorized_user_action()

    def get_all_users(self,
                      current_user: User,
                      page: int = 1,
                      page_size: int = 10) -> Optional[dict]:
        """Get paginated list of all users (admin only)."""
        try:
            self._check_admin(current_user)
            skip = (page - 1) * page_size
            total = self.db.query(User).count()
            users = self.db.query(User).offset(skip).limit(page_size).all()

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Backoffice: Get Users",
                description="Admin fetched paginated user list"
            )

            return {
                "items": [UserDTO.from_model(u) for u in users],
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
                "has_next": page < ((total + page_size - 1) // page_size),
                "has_prev": page > 1,
            }
        except SQLAlchemyError as e:
            logger.error("Database error in backoffice get_all_users: %s", e)
            UserErrorHandler.raise_server_error(str(e))
        return None

    def get_all_notes(self,
                      current_user: User,
                      page: int = 1,
                      page_size: int = 10) -> Optional[dict]:
        """Get paginated list of all notes (admin only)."""
        try:
            self._check_admin(current_user)
            skip = (page - 1) * page_size
            query = self.db.query(Note).options(joinedload(Note.user))
            total = query.count()
            notes = query.offset(skip).limit(page_size).all()

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Backoffice: Get Notes",
                description="Admin fetched paginated note list"
            )

            return NoteDTO.paginated_response(
                notes, page, page_size, "", total, "created_at", "desc"
            )
        except SQLAlchemyError as e:
            logger.error("Database error in backoffice get_all_notes: %s", e)
            UserErrorHandler.raise_server_error(str(e))
        return None

    def get_audit_logs(self,
                       current_user: User,
                       page: int = 1,
                       page_size: int = 10) -> Optional[dict]:
        """Get paginated list of audit logs (admin only)."""
        try:
            self._check_admin(current_user)
            skip = (page - 1) * page_size
            query = self.db.query(Audit).options(joinedload(Audit.user))
            total = query.count()
            audits = (query.order_by(Audit.timestamp.desc())
                      .offset(skip).limit(page_size).all())

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Backoffice: Get Audit",
                description="Admin fetched paginated audit log"
            )

            return AuditDTO.paginated_response(audits, page, page_size, total)
        except SQLAlchemyError as e:
            logger.error("Database error in backoffice get_audit_logs: %s", e)
            UserErrorHandler.raise_server_error(str(e))
        return None
