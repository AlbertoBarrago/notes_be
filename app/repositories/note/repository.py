"""
Note Action DB
"""
from datetime import datetime
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.elements import or_

from app.core.exceptions.auth import AuthErrorHandler
from app.core.exceptions.note import NoteErrorHandler
from app.db.models import Note, User
from app.dto.note.note_dto import NoteDTO
from app.repositories.auth.common.services import CommonService
from app.repositories.logger.repository import LoggerService
from app.schemas.notes.request import NoteCreate, NoteUpdate

logger = LoggerService().logger


class NoteManager:
    """
    Note manager class
    """

    def __init__(self, db: Session):
        self.db = db

    def handling_paginated_request(self,
                                   current_user: User,
                                   page: int,
                                   page_size: int,
                                   query,
                                   search_query: str,
                                   skip: int,
                                   sort_by: str,
                                   sort_order: str) -> Optional[dict]:
        """
        Handling pagination request
        """
        try:
            if search_query := search_query.strip():
                search = f"%{search_query}%"
                query = query.filter(
                    or_(
                        Note.title.ilike(search),
                        Note.content.ilike(search),
                        Note.tags.contains(search),
                        User.username.ilike(search),
                        User.email.ilike(search)
                    )
                )
            sort_column = getattr(Note, sort_by)
            query = query.order_by(sort_column.desc()
                                   if sort_order == "desc"
                                   else sort_column.asc())

            total = query.count()
            notes = query.offset(skip).limit(page_size).all()

            log_description = (f"User get pagination notes with search: "
                               f"{search_query}") if search_query \
                else "User get pagination notes"

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Get notes",
                description=log_description
            )

            return NoteDTO.paginated_response(
                notes,
                page,
                page_size,
                search_query,
                total,
                sort_by,
                sort_order
            )
        except SQLAlchemyError as e:
            logger.error("Database error while logging action: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except ValueError as e:
            logger.error("Invalid value error while logging action: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except IOError as e:
            logger.error("I/O error while logging action: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        return None

    def get_explore_notes(self,
                          current_user: User,
                          page: int = 1,
                          page_size: int = 10,
                          search_query: str = "",
                          sort_by: str = "created_at",
                          sort_order: str = "desc"
                          ) -> Optional[dict]:
        """
         Get public notes for logged user
        """
        try:
            skip = (page - 1) * page_size
            query = (self.db.query(Note).join(User,
                                              Note.user_id == User.id,
                                              isouter=True)
                     .filter(Note.is_public.is_(True)))

            return self.handling_paginated_request(current_user,
                                                   page,
                                                   page_size,
                                                   query,
                                                   search_query,
                                                   skip, sort_by,
                                                   sort_order)
        except SQLAlchemyError as e:
            logger.error("Database error while get public note paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except ValueError as e:
            logger.error("Invalid value error while public get note paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except IOError as e:
            logger.error("I/O error while get note public paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        return None

    def get_note_paginated(self, current_user: User,
                           page: int = 1,
                           page_size: int = 10,
                           search_query: str = "",
                           sort_by: str = "created_at",
                           sort_order: str = "desc"
                           ) -> Optional[dict]:
        """
         Get pagination notes for specific user
        """
        try:
            skip = (page - 1) * page_size
            query = (self.db.query(Note)
                     .join(User)
                     .options(joinedload(Note.user))
                     .filter(Note.user_id == current_user.id))

            return self.handling_paginated_request(current_user,
                                                   page,
                                                   page_size,
                                                   query,
                                                   search_query,
                                                   skip,
                                                   sort_by,
                                                   sort_order)
        except SQLAlchemyError as e:
            logger.error("Database error while get note paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except ValueError as e:
            logger.error("Invalid value error while get note paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except IOError as e:
            logger.error("I/O error while get note paginated: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        return None

    def get_note(self, note_id: int, current_user: User) -> Optional[dict]:
        """Get note by ID"""
        try:
            note_obj = (self.db.query(Note)
                        .filter(Note.id == note_id).first())
            if not note_obj:
                NoteErrorHandler.raise_note_not_found()
            if not note_obj.is_public and note_obj.user_id != current_user.id:
                AuthErrorHandler.raise_unauthorized()
            return NoteDTO.from_model(note_obj)
        except SQLAlchemyError as e:
            logger.error("Database error while get note: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except ValueError as e:
            logger.error("Invalid value error while get note: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        except IOError as e:
            logger.error("I/O error while get note: %s", e)
            NoteErrorHandler.raise_pagination_error(e)
        return None

    def search_notes(self, current_user: User, query: str) -> Optional[list[dict]]:
        """Search notes by query"""
        try:
            base_query = self.db.query(Note).join(User).filter(Note.user_id == current_user.id)

            if query:
                search = f"%{query}%"
                base_query = base_query.filter(
                    or_(
                        Note.title.ilike(search),
                        Note.content.ilike(search),
                        User.username.ilike(search)
                    )
                )

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Search Notes",
                description="User searched notes successfully"
            )

            notes = base_query.all()
            return [NoteDTO.from_model(note) for note in notes]
        except SQLAlchemyError as e:
            logger.error("Database error while searching notes action: %s", e)
            NoteErrorHandler.raise_note_not_found()
        except ValueError as e:
            logger.error("Invalid value error while searching notes action: %s", e)
            NoteErrorHandler.raise_note_not_found()
        except IOError as e:
            logger.error("I/O error while searching notes action: %s", e)
            NoteErrorHandler.raise_note_not_found()
        return None

    def add_note(self, note: NoteCreate, current_user: User) -> Optional[dict]:
        """Add new note"""
        try:
            new_note = Note(
                title=note.title,
                content=note.content,
                is_public=note.is_public,
                tags=note.tags,
                image_url=note.image_url,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.id
            )

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Create Note",
                description="User create note successfully"
            )
            self.db.add(new_note)
            self.db.commit()
            self.db.refresh(new_note)

            return NoteDTO.from_model(new_note)
        except SQLAlchemyError as e:
            logger.error("Database error while adding notes: %s", e)
        except ValueError as e:
            logger.error("Invalid value error while adding notes: %s", e)
        except IOError as e:
            logger.error("I/O error while adding notes: %s", e)
            NoteErrorHandler.raise_note_creation_error(str(e))
        return None

    def update_note(self, note_id: int, note: NoteUpdate, current_user: User) -> Optional[dict]:
        """Update existing note"""
        try:
            note_obj = (self.db.query(Note)
                        .filter(Note.id == note_id).first())
            if not note_obj:
                NoteErrorHandler.raise_note_not_found()
            if note_obj.user_id != current_user.id:
                AuthErrorHandler.raise_unauthorized()

            update_fields = {
                'title': note.title,
                'content': note.content,
                'is_public': note.is_public,
                'image_url': note.image_url,
                'tags': note.tags
            }

            for field, value in update_fields.items():
                if value is not None:
                    setattr(note_obj, field, value)

            note_obj.updated_at = datetime.now()

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Update Note",
                description="User update note successfully"
            )

            self.db.commit()
            self.db.refresh(note_obj)
            return NoteDTO.from_model(note_obj)
        except SQLAlchemyError as e:
            logger.error("Database error while adding notes: %s", e)
            NoteErrorHandler.raise_note_update_error(e)
        except ValueError as e:
            logger.error("Invalid value error while adding notes: %s", e)
            NoteErrorHandler.raise_note_update_error(e)
        except IOError as e:
            logger.error("I/O error while adding notes: %s", e)
            NoteErrorHandler.raise_note_update_error(e)
        return None

    def delete_note(self, note_id: int, current_user: User) -> Optional[dict]:
        """Delete note"""
        try:
            note_obj = (self.db.query(Note)
                        .filter(Note.id == note_id).first())
            if not note_obj:
                NoteErrorHandler.raise_note_not_found()
            if note_obj.user_id != current_user.id:
                AuthErrorHandler.raise_unauthorized()

            CommonService(self.db).log_action(
                user_id=current_user.id,
                action="Delete Note",
                description="User delete note successfully"
            )
            self.db.delete(note_obj)
            self.db.commit()
            return {"result": f"Note {note_id} has been deleted",
                    "id_note": note_id}
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error deleting note: %s", e)
            NoteErrorHandler.raise_delete_note_error(e)
        except ValueError as e:
            logger.error("Invalid value error while deleting note: %s", e)
            NoteErrorHandler.raise_delete_note_error(e)
        except IOError as e:
            logger.error("I/O error while deleting note: %s", e)
            NoteErrorHandler.raise_delete_note_error(e)
        return None

    def perform_note_action(self, action: str,
                            note=None,
                            note_id=None,
                            current_user=None,
                            **kwargs):
        """
        Perform database actions for note
        :param action: Action to perform
        :param note: Note object
        :param note_id: ID of note
        :param current_user: Current authenticated user
        :param kwargs: Additional arguments
        :return: Note or response object
        """
        try:
            actions = {
                "search_notes": lambda: self.search_notes(current_user, kwargs.get("query")),
                "get_note_paginated": lambda: self.get_note_paginated(
                    current_user,
                    kwargs.get("page", 1),
                    kwargs.get("page_size", 10),
                    kwargs.get("query", ""),
                    kwargs.get("sort_by", "created_at"),
                    kwargs.get("sort_order", "desc"),
                ),
                "get_explore_notes": lambda: self.get_explore_notes(
                    current_user,
                    kwargs.get("page", 1),
                    kwargs.get("page_size", 10),
                    kwargs.get("query", ""),
                    kwargs.get("sort_by", "created_at"),
                    kwargs.get("sort_order", "desc"),
                ),
                "add_note": lambda: self.add_note(note, current_user),
                "get_note_by_id": lambda: self.get_note(note_id, current_user),
                "update_note": lambda: self.update_note(note_id, note, current_user),
                "delete_note": lambda: self.delete_note(note_id, current_user)
            }
            return actions[action]()
        except SQLAlchemyError as e:
            logger.error("Database error while select action: %s", e)
            NoteErrorHandler.raise_general_error(e)
        except ValueError as e:
            logger.error("Invalid value error while select action: %s", e)
            NoteErrorHandler.raise_general_error(e)
        except IOError as e:
            logger.error("I/O error while select action: %s", e)
            NoteErrorHandler.raise_general_error(e)
        return None
