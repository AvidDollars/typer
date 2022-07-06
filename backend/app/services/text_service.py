from ..models.text import TextDb
from ..repositories.crud_operations import CrudOperations
from ..utils import Pagination
from fastapi import HTTPException
from ..constants import USER_TEXTS_MAX_COUNT
from ..models.enums import UserRole

__all__ = ("TextService", )


class TextService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text(self, *, text: TextDb, user_id: str, role: UserRole):
        user_texts_count = await self.repository.get_count(TextDb, filter_=TextDb.added_by == user_id)

        if user_texts_count >= USER_TEXTS_MAX_COUNT and role < UserRole.master_admin:
            raise HTTPException(status_code=403, detail=f"user can store {USER_TEXTS_MAX_COUNT} texts at most")
        else:
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
