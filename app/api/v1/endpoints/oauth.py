"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.mysql import get_db
from app.repositories.auth.login.repository import LoginManager
from app.repositories.auth.oauth.google.repository import get_user_info, add_user_to_db
from app.schemas.authorization.request import TokenResponse, OauthRequest
from app.schemas.common.responses import CommonResponses

router = APIRouter()


@router.post("/oauth/login",
             response_model=TokenResponse,
             responses={**CommonResponses.BAD_REQUEST, **CommonResponses.UNAUTHORIZED})
def login_google(request: OauthRequest,
                 db: Session = Depends(get_db)):
    """
    Login from Google
    :param request:
    :param db:
    :return: Token
    """

    return LoginManager(db).perform_action_auth(
        "login",
        get_user_info(db, request),
        oauth=True)


@router.post("/oauth/register",
             response_model=TokenResponse,
             responses={**CommonResponses.BAD_REQUEST,
                        **CommonResponses.UNAUTHORIZED,
                        **CommonResponses.MAIL_NOT_SENT})
async def register_from_google(request: OauthRequest,
                         background_tasks: BackgroundTasks,
                         db: Session = Depends(get_db)):
    """
    Register from Google
    :param request:
    :param background_tasks:
    :param db:
    :return: Token
    """
    return await add_user_to_db(db, request, background_tasks)
