from datetime import datetime

from pydantic import validator, UUID4
from sqlalchemy import Column, TEXT
from sqlmodel import SQLModel, Field

from utils import uuid4_bugfix


class TextBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None


class TextIn(TextBase):
    content: str = Field(sa_column=Column(TEXT), nullable=False)

    # WORKAROUND FOR GETTING LENGTH OF A TEXT: Pydantic V1 has no functionality for computed fields
    @validator("content", always=True)
    def char_count(cls, value: str):
        cls.content_length = len(value)
        return value


class TextDetail(TextBase):
    created_at: datetime
    id: UUID4


class TextDb(TextIn, table=True):

    __tablename__ = "texts"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4_bugfix)
    created_at: datetime = Field(default_factory=datetime.now)
    added_by: UUID4 = Field(foreign_key="users.id", nullable=False)
    is_public: bool = False
    characters_count: int = Field(nullable=False, default=1) # without "default" value validator will not be executed

    # WORKAROUND FOR GETTING LENGTH OF A TEXT: Pydantic V1 has no functionality for computed fields
    @validator("characters_count", always=True)
    def text_length(cls, _value):
        return vars(cls).get("content_length") or 0


class TextOut(TextDb):
    ...


__all__ = [item for item in dir() if str(item).startswith("Text")]
