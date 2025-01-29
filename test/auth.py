"""
This module contains the test class for the User model.
"""
from datetime import datetime

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.models.user.model import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestUser:
    def setup_class(self):
        """
        Set up the test by creating the user in an in-memory SQLite database.
        Hashes the password before saving the user.
        """

    def __init__(self):
        self.session = None
        self.new_user = None

        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }

        Base.metadata.create_all(engine)

        self.session = SessionLocal()

        hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        self.new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.session.add(self.new_user)
        self.session.commit()

    def teardown_class(self):
        """
        Clean up after the test by rolling back the session and closing it.
        """
        self.session.rollback()
        self.session.close()

    def test_register_user(self):
        """
        Test that the user was correctly registered and the password is hashed.
        Verifies that the user exists in the database and that the password matches.
        """
        created_user = (self.session.query(User)
                        .filter(User.username == "testuser").first())

        assert created_user is not None
        assert created_user.username == "testuser"
        assert created_user.email == "test@example.com"

        assert bcrypt.checkpw("password123".encode('utf-8'), created_user.hashed_password.encode('utf-8'))
