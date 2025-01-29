"""
Notes model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Note(Base):
    """
    Note Class
    """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_public = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)
    image_url = Column(String(255), nullable=True)

    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.title}>"
