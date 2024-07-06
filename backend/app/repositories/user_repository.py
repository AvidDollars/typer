from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .crud_operations import CrudOperations
from constants import UNIQUE_CONSTRAINT_VIOLATED
from custom_exceptions import \
    UserAlreadyRegisteredException, \
    ActivationTokenNotFoundException, \
    AccountAlreadyActivatedException, \
    ActivationLinkExpiredException
from db import Database
from models import UserDb
from utils import timedelta_is_less_than, auto_repr

__all__ = ("UserRepository", )


@auto_repr(hide="registration_token_expiration")
class UserRepository(CrudOperations):

    def __init__(self, *, db: Database, registration_token_expiration: int):
        super().__init__(db=db)
        self.registration_token_expiration = registration_token_expiration

    async def register_user(self, user: UserDb) -> str:
        try:
            await self.create_resource(user)
            return user.activation_link

        except IntegrityError as error:

            # Sqlite3 doesn't know "sqlstate" attribute
            if "UNIQUE" in error._message() or error.orig.sqlstate == UNIQUE_CONSTRAINT_VIOLATED:
                raise UserAlreadyRegisteredException

            else:
                raise  # unexpected error... will be logged

    async def activate_user(self, activation_token: str) -> dict[str, str]:
        session = await self.db.get_session()

        async with session.begin():
            stmt = select(UserDb).filter(UserDb.activation_link == activation_token)

            user = (await session.execute(stmt)).scalars().first()

            # activation token is not present in a database
            if not user:
                raise ActivationTokenNotFoundException

            # activation token is present in a database, but account is already activated
            if user.is_activated:
                raise AccountAlreadyActivatedException

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
                    raise ActivationLinkExpiredException
