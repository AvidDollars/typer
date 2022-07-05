from ..models.text import TextDb
from ..repositories.crud_operations import CrudOperations
from ..utils import Pagination

__all__ = ("TextService", )


class TextService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text(self, text: TextDb):
        await self.repository.create_resource(text)

    async def get_user_texts(self, *, user_id, pagination: Pagination = None):
        return await self.repository.read_resource(
            TextDb,
            method="all",
            filter_=TextDb.added_by == user_id,
            pagination=pagination if pagination is not None and isinstance(pagination, Pagination) else None
        )

    async def get_public_texts(self, *, pagination: Pagination = None):
        return await self.repository.read_resource(
            TextDb,
            method="all",
            filter_=TextDb.is_public == True,
            pagination=pagination if pagination is not None and isinstance(pagination, Pagination) else None
        )
