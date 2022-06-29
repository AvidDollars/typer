from ..db import Database


__all__ = ("UserService", )


class UserService:
    def __init__(self, db: Database):
        self.db = db
