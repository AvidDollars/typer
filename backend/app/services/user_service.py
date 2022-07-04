from .hashing_service import AbstractHashingService
from .auth_service import JwtToken
from ..models.user import UserDb, UserIn, UserLogin
from fastapi import HTTPException, status

__all__ = ("UserService", )


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
        # TODO: created custom errors (will inherit from HttpException)
        invalid_credentials_err = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid credentials"
        )

        if (user_db := await self._get_user_from_db(user)) is None:
            raise invalid_credentials_err

        if self._login_approved(user, user_db, message_if_password_mismatch=invalid_credentials_err):
            return self.jwt_token.encode({
                "role": user_db.role,
                "id": user_db.id
            })

    # ↓↓↓ HELPER METHODS ↓↓↓
    async def _get_user_from_db(self, user: UserLogin):
        if user.name is not None:
            field = UserDb.name == user.name
        else:
            field = UserDb.email == user.email

        user_db = await self.repository.read_resource(UserDb, filter_=field, method="one_or_none")
        return user_db

    def _login_approved(self, user_in, user_db, *, message_if_password_mismatch: HTTPException) -> bool:
        # TODO: what if account is not activated and activation token is expired?
        if not user_db.is_activated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="account is not activated"
            )

        password_match = self.hashing_service.verify(user_in.password, user_db.password)

        if not password_match:
            raise message_if_password_mismatch
        else:
            return True
