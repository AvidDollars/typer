from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .crud_operations import CrudOperations
from ..constants import UNIQUE_CONSTRAINT_VIOLATED
from ..db import Database
from ..models.user import UserDb
from ..utils import timedelta_is_less_than

__all__ = ("UserRepository", )


class UserRepository(CrudOperations):
    def __init__(self, *, db: Database, registration_token_expiration: int):
        super().__init__(db=db)
        self.registration_token_expiration = registration_token_expiration

    async def register_user(self, user: UserDb) -> str:
        try:
            await self.create_resource(user)
            return user.activation_link

        except IntegrityError as error:
            if error.orig.sqlstate == UNIQUE_CONSTRAINT_VIOLATED:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="user is already registered"
                )

            else:
                raise  # unexpected error... will be logged

    async def activate_user(self, activation_token: str) -> dict[str, str]:
        session = await self.db.get_session()

        async with session.begin():
            stmt = select(UserDb).filter(UserDb.activation_link == activation_token)

            user = (await session.execute(stmt)).scalars().first()

            # activation token is not present in a database
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="activation token does not exist"
                )

            # activation token is present in a database, but account is already activated
            if user.is_activated:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="account is already activated"
                )

            # user clicked on valid link and is not yet activated -> activation process
            if not user.is_activated:

                token_is_not_expired = timedelta_is_less_than(
                    user.created_at,
                    hours=self.registration_token_expiration
                )

                # user is not activated and activation link is not expired
                if token_is_not_expired:
                    user.is_activated = True
                    await session.commit()
                    return {"message": "account was activated"}

                # user is not activated, but activation link is expired
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="activation link is expired"
                    )
