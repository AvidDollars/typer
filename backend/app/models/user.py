from datetime import datetime

from sqlmodel import SQLModel, Field

from .enums import UserRole


class UserBase(SQLModel):
    name: str | None

    # TODO: regex email validation
    email: str | None


class UserIn(UserBase):
    password: str


class UserDb(UserIn, table=True):

    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    role: UserRole
    created_at: datetime
    email_subscription: bool = True
    is_activated: bool = False


class UserOut(UserBase):
    role: UserRole
    created_at: datetime
    email_subscription: bool = True
    is_activated: bool = False
