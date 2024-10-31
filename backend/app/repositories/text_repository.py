from .crud_operations import CrudOperations
from db import Database


__all__ = ("TextRepository", )


class TextRepository(CrudOperations):
    def __init__(self, *, db: Database):
        super().__init__(db=db)
