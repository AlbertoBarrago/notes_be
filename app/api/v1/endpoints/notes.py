"""
Note Endpoint
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.models.user.model import User
from app.db.mysql import get_db, get_current_user
from app.repositories.note.cache.repository import CacheRepository
from app.repositories.note.repository import NoteManager
from app.schemas.base import PaginatedResponse
from app.schemas.common.responses import CommonResponses
from app.schemas.notes.list.request import NoteQueryParams
from app.schemas.notes.request import (NoteOut, NoteCreate,
                                       NoteDelete, NoteUpdate)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

router = APIRouter()


@router.get("/list/public",
            response_model=PaginatedResponse[NoteOut],
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def get_public_notes(
        params: Annotated[NoteQueryParams, Depends()],
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get pagination notes
    :param params: NoteQueryParams (page, page_size, sort_order, query)
    :param current_user:
    :param db:
    :return:
    """
    return NoteManager(db).perform_note_action("get_explore_notes",
                                               current_user=current_user,
                                               page=params.page,
                                               sort_order=params.sort_order,
                                               query=params.query,
                                               page_size=params.page_size)


@router.get("/list/private",
            response_model=PaginatedResponse[NoteOut],
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def get_paginated_and_filtered_notes(
        params: Annotated[NoteQueryParams, Depends()],
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get pagination notes
    :param params: NoteQueryParams (page, page_size, sort_order, query)
    :param current_user:
    :param db:
    :return:
    """
    cache_repo = CacheRepository(db)
    return cache_repo.get_note_paginated(current_user=current_user,
                                         page=params.page,
                                         search_query=params.query,
                                         page_size=params.page_size,
                                         sort_by=params.sort_by,
                                         sort_order=params.sort_order,
                                         )


@router.get("/{note_id}",
            response_model=NoteOut,
            responses={
                401: {
                    "description": "Not authenticated",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Not authenticated",
                                "status_code": 401
                            }
                        }
                    }
                },
                500: {
                    "description": "Note not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Note not found",
                                "status_code": 500
                            }
                        }
                    }
                },
            })
def get_note(note_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Get Note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('get_note_by_id',
                                               note_id=note_id,
                                               current_user=current_user)


@router.post("/",
             response_model=NoteOut,
             responses={**CommonResponses.UNAUTHORIZED,
                        **CommonResponses.INTERNAL_SERVER_ERROR})
def add_note(note: NoteCreate,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Create a new note
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('add_note',
                                               note,
                                               current_user=current_user)


@router.put("/{note_id}",
            response_model=NoteOut,
            responses={**CommonResponses.UNAUTHORIZED,
                       **CommonResponses.INTERNAL_SERVER_ERROR})
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Update a note
    :param note_id:
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('update_note',
                                               note,
                                               note_id=note_id,
                                               current_user=current_user)


@router.delete("/{note_id}",
               response_model=NoteDelete,
               responses={**CommonResponses.UNAUTHORIZED,
                          **CommonResponses.INTERNAL_SERVER_ERROR})
def delete_note(note_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Delete a note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteDelete
    """

    return NoteManager(db).perform_note_action("delete_note",
                                               note_id=note_id,
                                               current_user=current_user)
