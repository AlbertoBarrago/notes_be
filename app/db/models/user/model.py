"""
Users Model
"""
import uuid
from datetime import datetime

import bcrypt
from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from app.db.models.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    User Class
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    picture_url = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    role = Column(String(50), nullable=False, default="GUEST")

    notes = relationship("Note", back_populates="user")
    audit = relationship("Audit", back_populates="user")

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify password
        :param plain_password:
        :return: bool
        """
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password.encode())

    def set_password(self, plain_password: str):
        """
        Set password
        :param plain_password:
        :return: str
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode(), salt)
        self.hashed_password = hashed_password.decode()
        return self.hashed_password
