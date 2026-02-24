"""
 Auth Models: RateLimit and RevokedToken
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime

from app.db.models.base import Base


class RateLimit(Base):
    """
    Rate Limit Model
    """
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), index=True)  # IP or user_id
    requests = Column(Integer, default=0)
    timestamp = Column(DateTime)


class RevokedToken(Base):
    """
    Stores invalidated JWT IDs so logout is enforced before natural expiry.
    Rows whose expires_at is in the past are safe to clean up.
    """
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(36), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=False, default=datetime.now)
