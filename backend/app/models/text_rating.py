from uuid import uuid4

from pydantic import UUID4
from sqlmodel import SQLModel, Field, UniqueConstraint


class TextRatingIn(SQLModel):
    rating: int = Field(ge=1, le=10)
    rated_by: UUID4 = Field(foreign_key="users.id", nullable=False)
    rated_text: UUID4 = Field(foreign_key="texts.id", nullable=False)


class TextRatingDb(TextRatingIn, table=True):

    __tablename__ = "text_ratings"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4)

    __table_args__ = UniqueConstraint("rated_by", "rated_text", name="uix_1"),


class TextRatingOut(TextRatingDb):
    ...
