import re
from datetime import datetime

from pydantic import validator
from sqlmodel import SQLModel, Field

from .enums import UserRole
from ..constants import EMAIL_VALIDATOR_REGEX
from ..utils.helpers import generate_registration_token
from ..utils.validators import at_least_one_uppercase_and_one_digit_password


class UserBase(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": True})
    email: str = Field(sa_column_kwargs={"unique": True})

    @validator("name")
    def must_be_valid_name(cls, name):
        if not re.fullmatch(r"\w{3,}", name):
            raise ValueError(
                "Please enter a name that is at least 3 characters long and uses only a-z, A-Z, 0-9 or _ characters."
            )

        return name

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

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    role: UserRole = Field(default=UserRole.user, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    email_subscription: bool = True
    is_activated: bool = False
    activation_link: str = Field(default_factory=generate_registration_token)


class UserOut(UserBase):
    role: UserRole
    created_at: datetime
    email_subscription: bool
    is_activated: bool
