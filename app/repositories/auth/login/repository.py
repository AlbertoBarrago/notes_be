"""
Session actions
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions.auth import AuthErrorHandler
from app.core.security import generate_user_token_and_return_user
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
