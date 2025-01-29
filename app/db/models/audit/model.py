"""
AuditLog Model
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Audit(Base):
    """
    AuditLog Class
    """
    __tablename__ = "audit"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    action = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", back_populates="audit")
