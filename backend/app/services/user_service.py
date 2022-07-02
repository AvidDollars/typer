from . import hashing_service
from ..models.user import UserDb, UserIn

__all__ = ("UserService", )


class UserService:
    def __init__(
            self, *,
            hashing_service: hashing_service.AbstractHashingService,
            repository
    ):
        self.hashing_service = hashing_service
        self.repository = repository

    async def save_user(self, user: UserIn):
        hashed_password = self.hashing_service.hash(user.password)
        user.password = hashed_password
        userDb = UserDb.from_orm(user)

        activation_link = await self.repository.save_user(userDb)
        return activation_link

    async def activate_user(self, activation_token: str):
        result = await self.repository.activate_user(activation_token)
        return result
