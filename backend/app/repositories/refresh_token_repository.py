from .crud_operations import CrudOperations, RowsAffected
from db import Database
from models import RefreshTokenDb

__all__ = ("RefreshTokenRepository", )


class RefreshTokenRepository(CrudOperations):

    def __init__(self, *, db: Database):
        super().__init__(db=db)

    async def store_refresh_token(self, *, refresh_token: RefreshTokenDb) -> RowsAffected:
        """ To be used for login action. Simply appends new refresh token to an existing list of refresh tokens. """
        return await self.create_resource(resource=refresh_token)

    async def delete_refresh_token(self, *, refresh_token_hash) -> RowsAffected:
        """ To be used for logout action. """
        return await self.delete_resource(RefreshTokenDb, filter_=RefreshTokenDb.refresh_token_hash == refresh_token_hash)
