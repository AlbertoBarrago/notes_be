"""
Dependency Utils
"""
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.settings import settings
from app.db.models.user.model import User
from app.repositories.logger.repository import LoggerService

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://"
    f"{settings.MYSQL_USER}:"
    f"{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}"
    f"/{settings.MYSQL_DATABASE}"
)

logger = LoggerService().logger
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as connection:
        logger.info("\033[92m🚀 Connected with success! to %s\033[0m", SQLALCHEMY_DATABASE_URL)
except OperationalError as e:
    raise HTTPException(status_code=500, detail="Errore di connessione al database") \
        from e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/swagger")


def get_db():
    """
    Get database session
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    """
    Get Current User in Session
    :param token:
    :param db:
    :return: User
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        user = db.query(User).filter(User.user_id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401,
                                detail="Invalid authentication credentials")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Token has expired") from None
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,
                            detail="Invalid token") from None
