"""Note testing the Note model."""
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.models.notes.model import Note
from app.db.models.user.model import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestNote:
    """
    A test class for verifying the functionality of the Note model.
    """

    def __init__(self):
        """Initialize attributes to avoid Pylint warnings"""
        self.session = None
        self.test_user = None
        self.valid_note = None

    def setup_class(self):
        """Setup the test database and create test data"""
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

        # Create a test user
        self.test_user = User(
            username="test_user",
            email="test_user@example.com",
            hashed_password="hashed_password",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.session.add(self.test_user)
        self.session.commit()

        # Create a test note
        self.valid_note = Note(
            title="Test Note",
            content="This is a test note.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=self.test_user.id
        )

        self.session.add(self.valid_note)
        self.session.commit()

    def teardown_class(self):
        """Teardown class by rolling back and closing the session"""
        self.session.rollback()
        self.session.close()

    def test_note_creation(self):
        """Test if a note is correctly created in the database"""
        note = self.session.query(Note).filter_by(title="Test Note").first()

        assert note is not None
        assert note.title == "Test Note"
        assert note.content == "This is a test note."

    def test_note_update(self):
        """Test updating a note's content"""
        note = self.session.query(Note).filter_by(title="Test Note").first()

        note.content = "Updated content"
        self.session.commit()

        updated_note = self.session.query(Note).filter_by(title="Test Note").first()
        assert updated_note.content == "Updated content"

    def test_note_deletion(self):
        """Test deleting a note"""
        note = self.session.query(Note).filter_by(title="Test Note").first()
        self.session.delete(note)
        self.session.commit()

        deleted_note = self.session.query(Note).filter_by(title="Test Note").first()
        assert deleted_note is None
