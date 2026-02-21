"""
  Custom Rate Limit Middleware
  Provides the rate limiting functionality for API endpoints.

  - Implemented as a Starlette BaseHTTPMiddleware
  - Every request hits the middleware before reaching the router
  - Identifier is either user:<username> (from JWT) or ip:<address> for
  anonymous
  - Counts are stored in a rate_limits table in MySQL with a time window
  - Returns HTTP 429 when exceeded, and adds X-RateLimit-Limit,
  X-RateLimit-Remaining, X-RateLimit-Reset headers to every response

"""
from datetime import datetime, timedelta

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from app.core.security import decode_access_token
from app.core.settings import settings
from app.db.models.auth.model import RateLimit


def _get_identifier(request: Request, ip: str) -> str:
    """Extract identifier from request"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            username = decode_access_token(auth_header.split(' ')[1])
            return f"user:{username}"
        except HTTPException:
            return f"ip:{ip}"
    return f"ip:{ip}"


def _get_or_create_rate_limit(identifier: str,
                              now: datetime,
                              window_start: datetime,
                              db) -> RateLimit:
    """Get or create the rate limit record"""
    rate_limit = db.query(RateLimit).filter(
        RateLimit.identifier == identifier,
        RateLimit.timestamp > window_start
    ).first()

    if not rate_limit:
        rate_limit = RateLimit(
            identifier=identifier,
            requests=1,
            timestamp=now
        )
        db.add(rate_limit)
    else:
        rate_limit.requests += 1
        rate_limit.timestamp = now

    return rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
        Rate Limit Middleware
    """

    def __init__(self, app: ASGIApp, db_session):
        super().__init__(app)
        self.rate_limit = int(settings.RATE_LIMIT)
        self.window = int(settings.RATE_LIMIT_WINDOW)
        self.db_session = db_session

    async def dispatch(self, request: Request, call_next):
        db = self.db_session()
        try:
            ip = request.client.host
            identifier = _get_identifier(request, ip)

            now = datetime.now()
            window_start = now - timedelta(minutes=self.window)

            rate_limit = _get_or_create_rate_limit(identifier, now, window_start, db)

            if rate_limit.requests > self.rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )

            db.commit()
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(
                self.rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(
                self.rate_limit - rate_limit.requests)
            response.headers["X-RateLimit-Reset"] = str(
                int(window_start.timestamp()))
            return response
        finally:
            db.close()
