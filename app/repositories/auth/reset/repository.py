"""
 Password manager
"""
from datetime import timedelta

from fastapi import BackgroundTasks
from pydantic.v1 import EmailStr

from app.core import create_access_token
from app.core.exceptions.auth import AuthErrorHandler
from app.core.exceptions.generic import GlobalErrorHandler
from app.db.models import User
from app.email.email_service import EmailService, EmailSchema
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger


class PasswordManager:
    """
    Session manager
    """

    def __init__(self, db):
        self.db = db

    def _get_user(self, username):
        """
        Get user from database
        :param username:
        :return: User object
        """
        return (self.db.query(User)
                .filter((User.username == username) |
                        (User.email == username))
                .first())

    def _log_action(self, user_id, action, description):
        """
        Log action
        :param user_id:
        :param action:
        :param description:
        """
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    def send_password_reset_email(self, token, username, background_tasks):
        """
        Send password reset email
        :param token:
        :param username:
        :param background_tasks:
        :return:
        """
        user = self._get_user(username)
        if not user:
            AuthErrorHandler.raise_user_not_found()

        log_audit_event(self.db,
                        user_id=user.user_id,
                        action="Password Reset",
                        description="Password reset requested")

        try:
            email_service = EmailService()
            email_schema = EmailSchema(
                username=user.username,
                email=[EmailStr(user.email)],
            )
            background_tasks.add_task(
                email_service.send_password_setup_email,
                email_schema,
                token
            )

            result = {
                "access_token": token,
                "token_type": "bearer",
                "username": user.username,
                "user": user
            }

            return result

        except (ConnectionError, TimeoutError):
            GlobalErrorHandler.raise_mail_reset_not_sent()
            return None

    def initiate_password_reset(self, email: str, background_tasks: BackgroundTasks):
        """
        Initiates a password reset process by generating a reset token and
        sending an email to the user if they exist.

        Parameters:
            email: str
                The email address of the user requesting a password reset.
            background_tasks: BackgroundTasks
                The background task manager to handle sending the email asynchronously.

        Returns:
            dict: A message indicating whether the reset link has been sent,
            without revealing if the email exists in the system.

        Raises:
            ConnectionError: If there is an issue connecting to the email service.
            TimeoutError: If the connection to the email service times out.
        """
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return {"message": "If the email exists, a password reset link has been sent"}

        reset_token = create_access_token(
            data={"sub": user.user_id, "purpose": "password_reset"},
            expires_delta=timedelta(minutes=15)
        )

        try:
            email_service = EmailService()
            email_schema = EmailSchema(
                username=user.username,
                email=[EmailStr(user.email)]
            )

            background_tasks.add_task(
                email_service.send_password_setup_email,
                email_schema,
                reset_token
            )

            self._log_action(user.user_id,
                             action="Password Reset",
                             description="Password reset initiated")
            return {"message": "Password reset instructions have been sent to your email"}

        except (ConnectionError, TimeoutError):
            GlobalErrorHandler.raise_mail_reset_not_sent()
        return None
