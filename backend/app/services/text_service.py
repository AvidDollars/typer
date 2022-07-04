from ..models.text import TextDb
from ..repositories.crud_operations import CrudOperations

__all__ = ("TextService", )


class TextService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text(self, text: TextDb):
        await self.repository.create_resource(text)
