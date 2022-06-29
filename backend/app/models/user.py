import re
from datetime import datetime

from pydantic import validator
from sqlmodel import SQLModel, Field

from .enums import UserRole
from ..constants import EMAIL_VALIDATOR_REGEX
from ..utils.validators import at_least_one_uppercase_and_one_digit_password


class UserBase(SQLModel):
    name: str | None
    email: str

    @validator("email")
    def must_be_valid_email(cls, email):
        if re.search(EMAIL_VALIDATOR_REGEX, email):
            return email
        raise ValueError("invalid email")


class UserIn(UserBase):
    password: str

    @validator("password")
    def must_be_strong_password(cls, password):
        validation_result = at_least_one_uppercase_and_one_digit_password(password)

        if validation_result["valid"]:
            return password
        raise ValueError(validation_result["message"])


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
