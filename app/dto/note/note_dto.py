"""
 Note Data Transfer Object (DTO)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class NoteDTO:
    """
    Represents a Data Transfer Object (DTO) for a note.

    This class provides a structured representation of a note
    suitable for transferring data between processes or services.
    It encapsulates all necessary attributes of a note, including
    identification, user association, content, metadata, and associated tags.
    It also provides utilities to transform a note model into a dictionary
    representation for serialization purposes and to construct paginated
    responses of note data.

    Attributes:
        id (int): Unique identifier of the note.
        user_id (int): Identifier of the user who owns the note.
        title (str): Title of the note.
        content (str): Main content of the note.
        created_at (datetime): The date and time when the note was created.
        updated_at (datetime): The date and time when the note was last updated.
        is_public (bool): Indicates whether the note is publicly accessible.
        tags (List[str]): List of tags associated with the note.
        image_url (Optional[str]): URL of an image associated with the note.

    """
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    is_public: bool
    tags: List[str]
    image_url: Optional[str]

    @staticmethod
    def from_model(note) -> dict:
        """
            Convert a note model instance into a dictionary representation.

            This static method takes a Note object, extracts its fields, and returns
            a dictionary containing key attributes.
            It includes information such as
            the note's ID, title, content, timestamps, privacy status, tags, and
            user-related data.

            Args:
                note: An instance of a note model with attributes such as `id`,
                      `title`, `content`, `created_at`, `updated_at`, `is_public`,
                      `tags`, `image_url`, and `user`.

            Returns:
                A dictionary containing keys `id`, `title`, `content`, `created_at`,
                `updated_at`, `is_public`, `tags`, `image_url`, and `user`.
                The `user`
                key maps to another dictionary with user's `username`, `email`, `role`,
                and `picture_url`.
        """
        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "is_public": note.is_public,
            "tags": note.tags if note.tags else [],
            "image_url": note.image_url,
            "user": {
                "username": note.user.username,
                "email": note.user.email,
                "role": note.user.role,
                "picture_url": note.user.picture_url
            }
        }

    @staticmethod
    def paginated_response(notes,
                           page: int,
                           page_size: int,
                           search_query: str,
                           total: int,
                           sort_by: str,
                           sort_order: str) -> dict:
        """
        Constructs a paginated response dictionary from the provided notes and pagination
        parameters. It includes metadata such as the current page, page size, total number
        of entries, and sorting information, along with a list of note DTOs for the current
        page.

        parameters:
            notes: A list of note instances to be included in the paginated response.
            page: The current page number.
            page_size: The number of items per page.
            search_query: A string representing the search query applied to the notes.
            total: The total number of notes available.
            sort_by: A string indicating the attribute by which results are sorted.
            sort_order: A string indicating the order of sorting, such as 'asc' or 'desc'.

        returns:
            A dictionary containing the paginated response, which includes the list of
            items, pagination metadata like current page, page size, total number of
            pages, and boolean indicators for the presence of next and previous pages.
        """
        return {
            "items": [NoteDTO.from_model(note) for note in notes],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page < ((total + page_size - 1) // page_size),
            "has_prev": page > 1,
            "search_query": search_query,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
