from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import Column
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field


class TypingSessionBase(SQLModel):
    duration_in_seconds: int = Field(nullable=False)
    text_id: UUID4 = Field(foreign_key="texts.id", nullable=False)
    user_id: UUID4 = Field(foreign_key="users.id", nullable=False)
    stats: dict = Field(sa_column=Column(JSON), nullable=False)


class TypingSessionDb(TypingSessionBase, table=True):

    __tablename__ = "typing_sessions"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4)
    created_at: datetime = Field(nullable=False, default_factory=datetime.now)


class TypingSessionOut(TypingSessionDb):
    ...
