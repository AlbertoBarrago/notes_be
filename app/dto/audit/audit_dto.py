"""
Audit Data Transfer Object (DTO)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuditDTO:
    """
    Represents a Data Transfer Object for an audit log entry.
    """
    id: int
    user_id: str
    action: str
    description: Optional[str]
    timestamp: datetime

    @staticmethod
    def from_model(audit) -> dict:
        """
        Convert an audit model instance into a dictionary representation.
        """
        return {
            "id": audit.id,
            "user_id": audit.user_id,
            "action": audit.action,
            "description": audit.description,
            "timestamp": audit.timestamp.isoformat(),
            "user": {
                "username": audit.user.username,
                "email": audit.user.email,
                "role": audit.user.role,
            }
        }

    @staticmethod
    def paginated_response(audits,
                           page: int,
                           page_size: int,
                           total: int) -> dict:
        """
        Constructs a paginated response for audit logs.
        """
        return {
            "items": [AuditDTO.from_model(audit) for audit in audits],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page < ((total + page_size - 1) // page_size),
            "has_prev": page > 1,
        }
