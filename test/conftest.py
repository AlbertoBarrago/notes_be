"""
Shared fixtures for endpoint integration tests.

Strategy
--------
app/db/mysql.py runs ``with engine.connect()`` at *module import time*, which
would fail without a running MySQL instance.  We intercept ``create_engine``
with a MagicMock before the first import of ``app.main`` so that the
module-level connection check becomes a no-op.

The RateLimitMiddleware is also patched to bypass its MySQL-backed session and
just forward every request unchanged.

A real SQLite in-memory database is created for the actual test logic.
"""
# pylint: disable=redefined-outer-name  # standard pytest fixture injection pattern
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

# ---------------------------------------------------------------------------
# 1. Patch create_engine *before* any app module is imported so that the
#    module-level `with engine.connect()` in app/db/mysql.py becomes a no-op.
# ---------------------------------------------------------------------------
_mock_engine = MagicMock()
with patch("sqlalchemy.create_engine", return_value=_mock_engine):
    from app.main import app          # noqa: E402
    from app.db.mysql import get_db, get_current_user  # noqa: E402

# ---------------------------------------------------------------------------
# 2. Replace the rate-limit middleware dispatch with a transparent passthrough.
#    The middleware's __init__ already captured the mock SessionLocal; patching
#    the class method means all existing instances use the new dispatch too.
# ---------------------------------------------------------------------------
from app.core.middleware.rate_limit import RateLimitMiddleware  # noqa: E402  # pylint: disable=wrong-import-position


async def _noop_dispatch(self, request, call_next):  # pylint: disable=unused-argument
    return await call_next(request)


RateLimitMiddleware.dispatch = _noop_dispatch

# ---------------------------------------------------------------------------
# 3. Real test database — SQLite in-memory, same schema as production.
# ---------------------------------------------------------------------------
from app.db.models import Base          # noqa: E402  # pylint: disable=wrong-import-position
from app.db.models.user.model import User  # noqa: E402  # pylint: disable=wrong-import-position

_TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=_TEST_ENGINE
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create all tables once per test session and seed a single test user.
    Yields the test user's UUID so other session-scoped fixtures can use it.
    """
    Base.metadata.create_all(_TEST_ENGINE)

    session = _TestingSessionLocal()
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="placeholder",
        role="GUEST",
    )
    user.set_password("testpassword")
    session.add(user)
    session.commit()
    user_id = user.id
    session.close()

    yield user_id

    Base.metadata.drop_all(_TEST_ENGINE)


@pytest.fixture
def db_session(setup_test_db):  # pylint: disable=unused-argument
    """Opens a fresh SQLite session for each test and closes it afterwards."""
    session = _TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user(db_session, setup_test_db):
    """Returns the seeded test user loaded from the current db_session."""
    user_id = setup_test_db
    return db_session.query(User).filter(User.id == user_id).first()


@pytest.fixture
def client(db_session, test_user):
    """
    Yields a TestClient whose ``get_db`` and ``get_current_user`` dependencies
    are overridden to use the test SQLite session and the seeded test user.
    """
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.clear()


@pytest.fixture
def client_real_auth(db_session):
    """
    Like ``client`` but does NOT override ``get_current_user``, so the real
    JWT decode and blacklist check in ``get_current_user`` run.
    Use for tests that need to verify token revocation.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.pop(get_db, None)
