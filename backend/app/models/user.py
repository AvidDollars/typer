import re
from datetime import datetime

from pydantic import validator, BaseModel, UUID4
from sqlmodel import SQLModel, Field

from .enums import UserRole
from utils import \
    at_least_one_uppercase_and_one_digit_password, \
    email_validator, \
    generate_registration_token, \
    uuid4_bugfix


class UserBase(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": False})
    email: str = Field(sa_column_kwargs={"unique": True})

    @validator("name")
    def must_be_valid_name(cls, name):
        if not re.fullmatch(r"\w{3,}", name):
            raise ValueError(
                "Please enter a name that is at least 3 characters long and uses only a-z, A-Z, 0-9 or _ characters."
            )

        return name

    _validate_email = validator("email", allow_reuse=True)(email_validator)


class UserLogin(BaseModel):
    name: str | None
    email: str | None
    password: str

    _validate_email = validator("email", allow_reuse=True)(email_validator)


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

    id: UUID4 | None = Field(primary_key=True, nullable=False, index=True, default_factory=uuid4_bugfix)
    role: UserRole | None = Field(default=UserRole.user, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    email_subscription: bool = True
    is_activated: bool = False
    activation_link: str = Field(default_factory=generate_registration_token)


class UserOut(UserBase):
    role: UserRole
    created_at: datetime
    email_subscription: bool
    is_activated: bool


__all__ = [item for item in dir() if str(item).startswith("User")]
