from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from ..constants import UNIQUE_CONSTRAINT_VIOLATED
from ..db import Database
from ..models.user import UserDb

__all__ = ("UserRepository", )


class UserRepository:
    def __init__(self, *, db: Database):
        self.db = db

    async def save_user(self, user: UserDb):
        session = await self.db.get_session()

        async with session.begin():
            session.add(user)

            try:
                await session.commit()
                return user.activation_link

            except IntegrityError as error:
                if error.orig.sqlstate == UNIQUE_CONSTRAINT_VIOLATED:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="user is already registered"
                    )

                else:
                    # error will be logged
                    raise
