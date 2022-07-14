from .auth_service import JwtToken
from .hashing_service import AbstractHashingService
from ..custom_exceptions import InvalidCredentialsException, AccountNotActivatedException
from ..models.user import UserDb, UserIn, UserLogin
from ..utils import auto_repr

__all__ = ("UserService", )


@auto_repr(hide="jwt_token")
class UserService:
    def __init__(
            self, *,
            hashing_service: AbstractHashingService,
            jwt_token: JwtToken,
            repository
    ):
        self.hashing_service = hashing_service
        self.jwt_token = jwt_token
        self.repository = repository

    async def register_user(self, user: UserIn):
        hashed_password = self.hashing_service.hash(user.password)
        user.password = hashed_password
        user_db = UserDb.from_orm(user)

        activation_link = await self.repository.register_user(user_db)
        return activation_link

    async def activate_user(self, activation_token: str):
        result = await self.repository.activate_user(activation_token)
        return result

    async def login_user(self, user: UserLogin):
        if (user_db := await self._get_user_from_db(user)) is None:
            raise InvalidCredentialsException

        if self._login_approved(user, user_db, exception_if_password_mismatch=InvalidCredentialsException):

            return self.jwt_token.encode({
                "role": user_db.role,
                "id": str(user_db.id)  # TODO: custom JSONEncoder?
            })

    # ↓↓↓ HELPER METHODS ↓↓↓
    async def _get_user_from_db(self, user: UserLogin):
        if user.name is not None:
            field = UserDb.name == user.name
        else:
            field = UserDb.email == user.email

        user_db = await self.repository.read_resource(UserDb, filter_=field, method="one_or_none")
        return user_db

    def _login_approved(self, user_in, user_db, *, exception_if_password_mismatch) -> bool:

        # TODO: what if account is not activated and activation token is expired?
        if not user_db.is_activated:
            raise AccountNotActivatedException

        password_match = self.hashing_service.verify(user_in.password, user_db.password)

        if not password_match:
            raise exception_if_password_mismatch
        else:
            return True
