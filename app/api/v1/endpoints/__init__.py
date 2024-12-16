"""
This module contains the endpoints for the API.
"""

from .auth import router as auth_router
from .healthcheck import router as healthcheck_router
from .home import router as home_router
from .notes import router as notes_router
from .oauth import router as oauth_router
from .users import router as users_router

__all__ = (
	"healthcheck_router",
	"auth_router",
	"notes_router",
	"users_router",
	"home_router",
	"oauth_router"
)
