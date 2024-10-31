from pydantic import UUID4
from sqlalchemy import and_, or_

from constants import USER_TEXTS_MAX_COUNT
from custom_exceptions import UserTextCountLimitException, TextNotFoundException
from models import UserRole, TextDb
from repositories.crud_operations import CrudOperations
from utils import Pagination

__all__ = ("TextService", )


class TextService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text(self, *, text: TextDb, user_id: str, role: UserRole):
        user_texts_count = await self.repository.get_count(TextDb, filter_=TextDb.added_by == user_id)

        if user_texts_count >= USER_TEXTS_MAX_COUNT and role < UserRole.master_admin:
            raise UserTextCountLimitException(USER_TEXTS_MAX_COUNT)
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

    async def get_text(self, *, text_id, user_id):
        id_match_filter = TextDb.id == text_id
        is_public_filter = and_(TextDb.is_public == True, id_match_filter)

        if user_id is None:  # user is not logged -> only public texts are available
            filter_ = and_(id_match_filter, is_public_filter)

        else:  # user is logged -> only public and added by user texts can be accessed
            added_by_user_filter = and_(id_match_filter, TextDb.added_by == user_id)
            filter_ = or_(added_by_user_filter, is_public_filter)

        text = await self.repository.read_resource(
            TextDb,
            method="first",
            filter_=filter_
        )

        if not text:
            raise TextNotFoundException
        else:
            return text

    async def delete_text(self, *, text_id: UUID4, user_id: UUID4, user_role):
        if user_role >= UserRole.master_admin:  # only master admin can delete any resource
            filter_ = TextDb.id == text_id
        else:
            filter_ = and_(TextDb.id == text_id, TextDb.added_by == user_id)

        rows_deleted = await self.repository.delete_resource(TextDb, filter_=filter_)

        if not rows_deleted:
            raise TextNotFoundException
