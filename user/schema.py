from ninja import Schema


class UserRegistrationSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    country: str


class UserLoginSchema(Schema):
    email: str
    password: str


class CurrentUserSchema(Schema):
    email: str
    refresh: str
