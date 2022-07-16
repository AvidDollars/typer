from datetime import datetime

from pydantic import UUID4
from sqlalchemy import Column, TEXT
from sqlmodel import SQLModel, Field

from ..utils import uuid4_bugfix


class TextBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None


class TextIn(TextBase):
    content: str = Field(sa_column=Column(TEXT), nullable=False)


class TextDetail(TextBase):
    created_at: datetime
    id: UUID4


class TextDb(TextIn, table=True):

    __tablename__ = "texts"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4_bugfix)
    created_at: datetime = Field(default_factory=datetime.now)
    added_by: UUID4 = Field(foreign_key="users.id", nullable=False)
    is_public: bool = False


class TextOut(TextDb):
    ...
