from ninja import Schema
from ninja.errors import ValidationError
from pydantic import root_validator, validator

from .utils import validate_email, validate_password


def set_title_case(value: str) -> str:
    return value.title()


class UserRegistrationSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    country: str

    @validator("email", pre=True, always=True)
    def validate_email(cls, value):
        if not validate_email(value):
            raise ValidationError("Invalid email.")
        return value.lower()

    @validator("password", pre=True, always=True)
    def validate_password(cls, value):
        password_is_valid = validate_password(value)
        if not password_is_valid:
            raise ValidationError("Invalid password.")
        return value

    _ensure_first_name_is_title_case = validator("first_name", allow_reuse=True)(
        set_title_case
    )
    _ensure_last_name_is_title_case = validator("last_name", allow_reuse=True)(
        set_title_case
    )
    _ensure_country_is_title_case = validator("country", allow_reuse=True)(
        set_title_case
    )

    class Config(Schema.Config):
        max_anystr_length = 30
        max_anystr_length = 30


class UserLoginSchema(Schema):
    email: str
    password: str


class CurrentUserSchema(Schema):
    email: str
    refresh: str


class UserOutSchema(Schema):
    email: str
    first_name: str
    last_name: str
    country: str
