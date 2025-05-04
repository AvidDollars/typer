from datetime import datetime

from pydantic import UUID4
from sqlmodel import SQLModel, Field
from utils import uuid4_bugfix


class RefreshTokenBase(SQLModel):
    refresh_token_hash: str = Field(nullable=False)
    user_id: UUID4 = Field(foreign_key="users.id", nullable=False)
    expires_in: datetime = Field(nullable=False)


class RefreshTokenDb(RefreshTokenBase, table=True):
    """ refresh token from "POST /refresh" endopoint """

    __tablename__ = "refresh_tokens"

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4_bugfix)
    created_at: datetime = Field(default_factory=datetime.now)


__all__ = [item for item in dir() if str(item).startswith("RefreshToken")]
