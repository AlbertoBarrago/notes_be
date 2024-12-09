"""
 Google OAuth Actions
"""
import secrets

import requests

from app.core import generate_user_token
from app.core.exceptions.auth import AuthErrorHandler
from app.core.exceptions.generic import GlobalErrorHandler
from app.db.models import User
from app.repositories.audit.repository import log_audit_event
from app.repositories.auth.common.services import CommonService
from app.repositories.logger.repository import LoggerService
from app.schemas.auth.request import TokenRequest

logger = LoggerService().logger


def get_info_from_google(token):
    """
    Fetches user information from Google using an OAuth2 token.

    This function sends a request to the Google API to retrieve the user's
    information based on the provided OAuth2 token.
    It returns a dictionary containing the user's email, name, and profile picture URL.
    If an error occurs during the API request, it logs the error and triggers an
    authorization error handler.

    Parameters:
        token (str): OAuth2 token used for authorization to access Google user
        information.

    Returns:
        dict: A dictionary with keys 'email', 'name', and 'picurl' corresponding
        to the user's email, full name, and profile picture URL respectively.

    Raises:
        AuthErrorHandler: If a RequestException occurs during the API call,
        indicating unauthorized access or other request failures.
    """
    try:
        userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(userinfo_url, headers=headers, timeout=5)
        response.raise_for_status()

        user_info = response.json()
        logger.debug("Google API Response: %s", {user_info})

        return {
            "email": user_info.get('email'),
            "name": user_info.get('name'),
            "picurl": user_info.get('picture')
        }
    except requests.RequestException as e:
        logger.error("Google API Error: %s", {str(e)})
        AuthErrorHandler.raise_unauthorized()
        return None


def get_user_info(db, request):
    """
    Get User Info
    :param db:
    :param request:
    :return:
    """
    user_from_google = get_info_from_google(request.credential)

    if 'error' in user_from_google:
        AuthErrorHandler.raise_invalid_token()

    user = db.query(User).filter(User.email == user_from_google['email']).first()

    if not user:
        AuthErrorHandler.raise_user_not_found()

    if not user.picture_url:
        user.picture_url = user_from_google['picurl']
        db.commit()
        db.refresh(user)

    request = TokenRequest(username=user_from_google['name'])

    log_audit_event(db, user_id=user.user_id, action="login", description="Login from Google")
    logger.info("User %s login from Google", user.user_id)

    return request


async def add_user_to_db(db, request, background_tasks):
    """
    Add User to DB and send email
    :param db:
    :param request:
    :param background_tasks:
    :return:
    """
    result = None
    user_from_google = get_info_from_google(request.credential)

    existing_user = db.query(User).filter(User.email == user_from_google['email']).first()

    if existing_user:
        AuthErrorHandler.raise_existing_user_error()

    if not existing_user:
        temp_password = secrets.token_urlsafe(32)
        user = User(
            email=user_from_google['email'],
            username=user_from_google['name'],
            picture_url=user_from_google['picurl'],
        )
        user.set_password(temp_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        user_fetched = db.query(User).filter(User.email == user_from_google['email']).first()
        log_audit_event(db,
                        user_id=user_fetched.user_id,
                        action="Google Registered",
                        description="Registered user By Google")
        logger.info("User %s registered", user_fetched.user_id)

        token = generate_user_token(user_fetched)

        try:
            await CommonService().send_email(background_tasks=background_tasks,
                                     token=token,
                                     user=user)
        except (ConnectionError, TimeoutError):
            GlobalErrorHandler.raise_mail_not_sent()
            return None

        result = {
            "access_token": token,
            "token_type": "bearer",
            "user": user_fetched
        }
    return result
