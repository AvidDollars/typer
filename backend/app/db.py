from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from utils.auto_repr_util import auto_repr
import json

@auto_repr
class Database:
    def __init__(self, config):
        self.environment = config["environment"]
        db_url = config["test_db_url"] if self.environment == "testing" else config["db_url"]

        self._engine = create_async_engine(
            db_url,
            echo=True if self.environment == "development" else False,
            future=True,
            # for avoiding escaping non-ASCII characters in typing stats ("typing_sessions" table, "stats" column):
            json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False) 
        )

    async def initialize(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_all(self):
        if self.environment != "testing":
            raise Exception("attempted dropping tables in non-testing environment")

        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def get_session(self):
        async_session = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        async with async_session() as session:
            return session
