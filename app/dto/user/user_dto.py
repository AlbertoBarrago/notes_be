"""
    This module defines the UserDTO class,
    which is used to transfer data between the application and the database.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """
    Represents a Data Transfer Object (DTO) for user information.

    The UserDTO is used to transfer user data between different parts of the
    application.
    It contains user-related information such as user ID, username,
    email, role, picture URL, and timestamps for creation and last update.
    The
    UserDTO can be populated from a user model using its static method.

    Attributes:
        user_id: Unique identifier for the user.
        username: Name chosen by the user to represent themselves.
        email: Email address associated with the user account.
        role: Role assigned to the user, indicating their level of access.
        picture_url: Optional URL to the user's profile picture.
        created_at: Timestamp indicating when the user account was created.
        updated_at: Timestamp indicating the last time the user information was
            updated.

    Methods:
        from_model(user): Static method that creates a dictionary from a user
            model object, suitable for easy data serialization and transfer.

    Parameters for from_model:
        user: The user object from which to extract data.
        Must include attributes
            matching those of the UserDTO.

    Returns from from_model:
        A dictionary representation of the user data, with all fields transformed
        to a suitable format for transfer or storage.
        This includes converting
        datetime objects to ISO formatted strings.
    """
    user_id: int
    username: str
    email: str
    role: str
    picture_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(user) -> dict:
        """
        Converts a user model instance into a dictionary representation. This method
        extracts user information such as user ID, username, email, role, picture URL,
        and timestamps of creation and last update, returning them in a dictionary
        format suitable for JSON serialization or data transfer.

        Args:
            user: An object representing a user model instance from which data is to be
            extracted.

        Returns:
            A dictionary containing user information including user_id, username, email,
            role, picture_url, created_at, and updated_at fields. The picture_url is
            returned as None if not available.
        """
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "picture_url": user.picture_url or None,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }
