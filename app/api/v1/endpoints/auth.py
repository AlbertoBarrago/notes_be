"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.repositories.auth.login.repository import LoginManager
from app.repositories.auth.reset.repository import PasswordManager
from app.repositories.user.repository import UserManager
from app.schemas.auth.request import TokenRequest, TokenResponse, ResetRequest, ResetUserEmail
from app.schemas.common.responses import CommonResponses
from app.schemas.user.request import ResetPswRequest

router = APIRouter()


@router.post("/auth/login",
             response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
def login(
        request: TokenRequest,
        db: Session = Depends(get_db)
):
    """
    Handles the login process by validating user credentials and generating an
    authentication token if successful.

    Arguments:
    request: TokenRequest
        The data required to authenticate, such as username and password.
    db: Session
        The database session, injected by the FastAPI dependency injection system.

    Returns:
    TokenResponse
        An object containing the authentication token and associated metadata.

    Raises:
    401 Unauthorized
        If the authentication credentials are invalid.
    500 Internal Server Error
        If there is an issue processing the request on the server side.
    """
    return LoginManager(db).perform_action_auth("login", request)


@router.post("/auth/swagger",
             response_model=TokenResponse,
             responses=CommonResponses.UNAUTHORIZED,
             include_in_schema=False)
def swagger_login(
        grant_type: str = Form(description="OAuth grant type"),
        username: str = Form(description="User's username or email"),
        password: str = Form(description="User's password"),
        db: Session = Depends(get_db)
):
    """
    Authenticates a user using OAuth and provides a token upon successful
    authentication.
    The function handles login requests for the Swagger UI,
    validates credentials, and generates a token if the credentials
    are correct.
    This is used for accessing secure endpoints during
    Swagger documentation access.

    Parameters:
        grant_type: OAuth grant type used for the authentication request.
        username: User's username or email for authentication.
        password: User's password for authentication.
        db: Database session dependency injected for database access.

    Returns:
        An instance of TokenResponse upon successful authentication,
        containing the token information.

    Raises:
        UNAUTHORIZED: If the authentication fails due to invalid
        credentials.
    """

    return LoginManager(db).perform_action_auth(
        "swagger_login",
        grant_type=grant_type,
        username=username,
        password=password)


@router.post("/auth/refresh-token", response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
async def refresh_token(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
    Handles the endpoint for refreshing a user authentication token.
    This function depends on the current user's authentication details and the database session,
    interacting with user management logic to generate a new token for the authenticated
    user.
    The method returns a response model for the token upon success.

    Parameters:
        current_user: User object injected by dependency.
        Represents the currently
                      authenticated user.
        db: Session object injected by dependency.
        Represents the database session.

    Returns:
        A TokenResponse object containing details of the newly generated token.

    Raises:
        HTTPException: If an unauthorized access or internal server error occurs.
    """
    return UserManager(db).perform_action_user(
        "generate_user_token_and_return_user",
        current_user)


@router.post("/auth/reset",
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
async def reset_password(
        psw_req: ResetPswRequest,
        db: Session = Depends(get_db)
):
    """
    Asynchronously resets the password for a user. This function is an endpoint for the
    password reset operation and uses a POST request. It primarily handles the business
    logic around the password reset feature by using the UserManager class.

    Parameters:
    psw_req: ResetPswRequest
        An instance containing the token and new password required for resetting the
        password.
    db: Session
        The database session dependency injected to perform operations on the
        database.

    Returns:
    coroutine
        The result of the password reset action performed by the UserManager.
    """
    return await UserManager(db).perform_action_user(
        "reset_password",
        token=psw_req.token,
        new_password=psw_req.new_password
    )


@router.post("/auth/send-reset-email",
             response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
def send_reset_email(
        request: ResetRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
    Sends a password reset email to a user. This function handles the
    process of generating and sending a password reset email to the user
    who has requested it. It leverages the PasswordManager for handling
    the reset logic.

    Parameters
    ----------
    request : ResetRequest
        The request containing the username and token for password reset.
    background_tasks : BackgroundTasks
        A utility for executing tasks in the background.
    db : Session
        The database session dependency provided by FastAPI.

    Returns
    -------
    TokenResponse
        The response model indicating the result of the password reset
        email send operation.

    Raises
    ------
    HTTPException
        If any internal server error or unauthorized access is encountered.

    """
    return PasswordManager(db).send_password_reset_email(
        username=request.username,
        token=request.token,
        background_tasks=background_tasks,
    )


@router.post("/auth/password-reset")
async def request_password_reset(
        request: ResetUserEmail,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
       Initiate a password reset process for a user

       Args:
           request (ResetUserEmail): Email request object containing user's email
           background_tasks (BackgroundTasks): FastAPI background tasks handler
           db (Session): Database session dependency

       Returns:
           dict: Response containing status of password reset initiation
       """
    return PasswordManager(db).initiate_password_reset(request.email, background_tasks)
