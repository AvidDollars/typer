from ..models.user import UserDb, UserIn
from . import hashing_service

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
