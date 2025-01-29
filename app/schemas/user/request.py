"""
User Schema
"""
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    User Base Model
    """
    role: str = "GUEST"
    username: str
    email: str


class UserOut(BaseModel):
    """
    User Out Model
    """
    id: str
    username: str
    email: str
    picture_url: Optional[str] = None


class UserRequestAdd(BaseModel):
    """
    User Update Model
    """
    password: str


class PasswordReset(BaseModel):
    """
    Password Reset Model
    """
    username: str
    current_password: str
    new_password: str


class ResetPswRequest(BaseModel):
    """
    Google Email Request Model
    """
    token: str
    new_password: str


class UserResponse(BaseModel):
    """
    User Response Model
    """
    user: UserOut
    message: str


class UserDelete(BaseModel):
    """
    User Delete Model
    """
    message: str
