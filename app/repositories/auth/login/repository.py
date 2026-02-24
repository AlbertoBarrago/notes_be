"""
Session actions
"""
from datetime import datetime
from typing import Optional

import jwt
from sqlalchemy.orm import Session

from app.core.exceptions.auth import AuthErrorHandler
from app.core.security import generate_user_token_and_return_user
from app.core.settings import settings
from app.db.models.auth.model import RevokedToken
from app.repositories.auth.common.services import CommonService
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger

class LoginManager:
    """
    Session manager
    """
    def __init__(self, db: Session):
        self.db = db

    def login(self, request, oauth: bool = False) -> dict:
        """
        Login user
        :param request:
        :param oauth:
        :return: TokenResponse object
        """
        user = CommonService(self.db).get_user(request.username)

        if not user:
            AuthErrorHandler.raise_user_not_found()

        if not oauth and not user.verify_password(request.password):
            AuthErrorHandler.raise_invalid_credentials()

        CommonService(self.db).log_action(
            user_id=user.id,
            action="Login",
            description="User logged in successfully"
        )

        return generate_user_token_and_return_user(user)

    def swagger_login(self, username: str, password: str) -> dict:
        """
        Login user from swagger
        :param username:
        :param password:
        :return: TokenResponse object
        """
        user = CommonService(self.db).get_user(username)

        if not user or not user.verify_password(password):
            AuthErrorHandler.raise_invalid_credentials()

        CommonService(self.db).log_action(
            user_id=user.id,
            action="Login",
            description="Logged from swagger"
        )

        return generate_user_token_and_return_user(user)

    def logout(self, token: str) -> dict:
        """
        Revoke a JWT by storing its jti in the blacklist.
        Also purges any already-expired rows to keep the table lean.
        :param token: raw Bearer token string
        :return: confirmation message
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            jti = payload.get("jti")
            exp = payload.get("exp")

            if jti:
                expires_at = datetime.fromtimestamp(exp)
                self.db.add(RevokedToken(jti=jti, expires_at=expires_at))
                # Clean up tokens that have already expired naturally
                self.db.query(RevokedToken).filter(
                    RevokedToken.expires_at < datetime.now()
                ).delete()
                self.db.commit()

            return {"message": "Logged out successfully"}
        except jwt.PyJWTError:
            return AuthErrorHandler.raise_invalid_token()

    def perform_action_auth(self, action: str, request=None, **kwargs) -> Optional[dict]:
        """
        Perform action authorization
        :param action:
        :param request:
        :param kwargs:
        :return: TokenResponse object
        """
        match action:
            case "login":
                return self.login(request, oauth=kwargs.get('oauth', False))
            case "swagger_login":
                return self.swagger_login(kwargs.get('username'), kwargs.get('password'))
            case "logout":
                return self.logout(kwargs.get('token'))
