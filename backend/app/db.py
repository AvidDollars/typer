from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


class Database:

    def __init__(self, db_url: str, environment: str):
        self._engine = create_async_engine(
            db_url,
            echo=True if environment == "development" else False,
            future=True
        )

    async def initialize(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self):
        async_session = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        async with async_session() as session:
            return session
