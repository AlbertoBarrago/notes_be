"""
    This module contains the functions for sending emails to users.
"""
from fastapi import BackgroundTasks
from pydantic.v1 import EmailStr

from app.core.exceptions.generic import GlobalErrorHandler
from app.db.models import User
from app.email.email_service import EmailService, EmailSchema
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger


class CommonService:
    """
    This class contains the functions for sending emails to users.
    """

    def __init__(self, db=None):
        self.email_service = EmailService()
        self.db = db

    async def send_email(self, background_tasks: BackgroundTasks, token: str, user) -> None:
        """
        Send password setup email in a background task

        Args:
            background_tasks: FastAPI background tasks handler
            token: Verification token
            user: User object with username and email

        Raises:
            GlobalErrorHandler: If email sending fails
        """
        try:
            email_schema = EmailSchema(
                username=user.username,
                email=[EmailStr(user.email)],
            )

            background_tasks.add_task(
                self.email_service.send_password_setup_email,
                email_schema,
                token
            )

            logger.info("Password setup email queued for user %s:", {user.username})

        except (ConnectionError, TimeoutError) as e:
            logger.error("Email sending failed for user %s:", e)
            raise GlobalErrorHandler.raise_mail_not_sent()
        except Exception as e:
            logger.error("Unexpected error sending email %s:", e)
            raise GlobalErrorHandler.raise_mail_not_sent()

    def get_user(self, username):
        """
        Get user from database
        :param username:
        :return: User object
        """
        return (self.db.query(User)
                .filter((User.username == username) |
                        (User.email == username))
                .first())

    def log_action(self, user_id, action, description):
        """
        Log action
        :param user_id:
        :param action:
        :param description:
        """
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)
