from datetime import datetime

from sqlalchemy import Column, TEXT
from sqlmodel import SQLModel, Field


class TextBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None
    content: str = Field(sa_column=Column(TEXT), nullable=False)
    is_public: bool
    added_by: int = Field(foreign_key="users.id", nullable=False)


class TextIn(TextBase):
    ...


class TextDb(TextBase, table=True):

    __tablename__ = "texts"
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)