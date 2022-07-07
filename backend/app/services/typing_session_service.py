from ..repositories import CrudOperations
from ..models.typing_session import TypingSessionDb
from sqlalchemy.exc import IntegrityError
from ..constants import INVALID_FOREIGN_KEY
from fastapi import HTTPException, status


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
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="unable to save - text or user does not exist"
                )
            else:
                raise  # unexpected error... will be logged
