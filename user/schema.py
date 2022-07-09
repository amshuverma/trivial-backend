from ninja import Schema


class TokenSchema(Schema):
    access: str
    refresh: str


class UserRegistrationSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    country: str
