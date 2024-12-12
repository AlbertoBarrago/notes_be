"""
 Cache Repository
"""
from functools import lru_cache
from typing import Any

from app.core import settings
from app.repositories.audit.repository import log_audit_event
from app.repositories.auth.common.services import CommonService
from app.repositories.logger.repository import LoggerService
from app.repositories.note.repository import NoteManager

logger = LoggerService().logger


class CacheRepository:
    """
    Manages cache repositories and integrates caching with database-backed storage solutions.

    The CacheRepository class serves as a bridge between the application's caching layer and
    the database layer. It provides methods for accessing public and paginated notes with caching
    enabled, to enhance performance by reducing the need for repeated database queries. The class
    uses the least recently used (LRU) caching strategy to manage cache size and maintains an
    audit trail of actions performed by users interacting with the cached data.
    """
    def __init__(self, db):
        self.db = db

    def _log_action(self, user_id, action, description):
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_public_notes(self, current_user, page: int, page_size: int,
                         search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """
        Retrieves public notes from cache or database storage.

        This function leverages caching to retrieve public notes efficiently. It accepts
        parameters for pagination and searching, and returns a list of public notes.
        It also logs the action of fetching data from the cache.

        Args:
            current_user (Any): The current logged-in user requiring access to public notes.
            page (int): The page number in the paginated list of notes.
            page_size (int): The number of notes per page in the results.
            search_query (str): The query string used to filter the notes by keywords.
            sort_by (str): The field by which the notes are sorted.
            sort_order (str, optional): Indicates the sorting direction, either 'asc'
                                        or 'desc'. Defaults to 'desc'.

        Returns:
            Any: A list of notes retrieved based on the specified parameters.
        """
        CommonService(self.db).log_action(
            user_id=current_user.user_id,
            action='Fetch from cache',
            description='Get Public Notes from Cache'
        )
        return NoteManager(self.db).get_explore_notes(
            current_user, page, page_size, search_query, sort_by, sort_order
        )

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_note_paginated(self, current_user, page: int, page_size: int,
                           search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """
        A method to retrieve paginated notes, utilizing caching for enhanced
        performance to prevent repetitive database queries. It accepts
        various parameters to customize pagination, filtering, and sorting.
        Logs the action of fetching notes using a common service.

        Parameters:
            current_user
                The currently authenticated user, whose information is utilized
                for note fetching and authorization.
            page: int
                Page number for pagination.
            page_size: int
                Number of notes to display per page.
            search_query: str
                The search query string to filter the notes.
            sort_by: str
                Column or field name on which sorting is to be applied.
            sort_order: str
                Sort order for the notes. Possible values are 'asc' for ascending
                and 'desc' for descending. Defaults to 'desc'.

        Returns:
            Any
                The paginated list of notes along with relevant metadata.
        """
        CommonService(self.db).log_action(
            user_id=current_user.user_id,
            action='Fetch from cache',
            description='Get Notes from Cache'
        )
        return NoteManager(self.db).get_note_paginated(
            current_user, page, page_size, search_query, sort_by, sort_order
        )
