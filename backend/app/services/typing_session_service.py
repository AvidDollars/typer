from pydantic import UUID4
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from constants import INVALID_FOREIGN_KEY
from custom_exceptions import CantSaveTypingSessionException
from models import TypingSessionDb
from repositories import CrudOperations

__all__ = ("TypingSessionService", )


class TypingSessionService:
    def __init__(self, repository: CrudOperations, logger):
        self.repository = repository
        self.logger = logger

    async def insert_typing_session(self, typing_session: TypingSessionDb):
        try:
            await self.repository.create_resource(typing_session)

        except IntegrityError as error:
            self.logger.warning(f"exception: {error}\n", exc_info=True)

            if error.orig.sqlstate == INVALID_FOREIGN_KEY:
                raise CantSaveTypingSessionException
            else:
                raise  # unexpected error... will be logged

    async def get_user_typing_sessions(self, *, user_id: UUID4, text_id: UUID4):
        user_sessions_filter = TypingSessionDb.user_id == user_id
        particular_text_sessions_filter = TypingSessionDb.text_id == text_id

        if text_id is None:
            filter_ = user_sessions_filter
        else:
            filter_ = and_(user_sessions_filter, particular_text_sessions_filter)

        return await self.repository.read_resource(
            TypingSessionDb, filter_=filter_, method="all"
        )
