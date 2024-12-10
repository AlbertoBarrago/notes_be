"""
Global error handler
"""
from fastapi import HTTPException
from starlette import status


class GlobalErrorHandler:
    """
    Handle global error
    """

    @classmethod
    def raise_mail_not_sent(cls: Exception):
        """
        Raise mail not sent error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send welcome email, but user was registered successfully",
            headers={"X-Error-Type": "email_failure"}
        )

    @classmethod
    def raise_mail_reset_not_sent(cls: Exception):
        """
        Raise mail reset not sent error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email for reset password",
            headers={"X-Error-Type": "email_failure"}
        )

    @classmethod
    def raise_internal_server_error(cls, message: str):
        """
        Class method that raises an internal server error using a standardized approach.
        This method signals that an irreversible server-side error has occurred and is unable
        to process the current request. It is primarily used for error handling and
        to ensure uniformity in error responses.

            @raise:
               Raises an appropriate internal server error exception.
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error - {message}",
            headers={"X-Error-Type": "internal_server_error"}
        )
