from pydantic import UUID4
from sqlmodel import SQLModel, Field, UniqueConstraint

from ..utils import uuid4_bugfix


class TextRatingIn(SQLModel):
    rating: int = Field(ge=1, le=10, nullable=True)
    rated_text: UUID4 = Field(foreign_key="texts.id", nullable=False)


class TextRatingUpdate(SQLModel):
    rating: int | None = Field(ge=1, le=10, nullable=True)
    id: UUID4


class TextRatingDb(TextRatingIn, table=True):

    __tablename__ = "text_ratings"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4_bugfix)
    rated_by: UUID4 = Field(foreign_key="users.id", nullable=False)

    __table_args__ = UniqueConstraint("rated_by", "rated_text", name="uix_1"),


class TextRatingOut(TextRatingDb):
    ...
