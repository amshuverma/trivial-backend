from config.settings import (
    JWT_ACCESS_EXPIRY_IN_DAYS,
    JWT_HASHING_ALGORITHM,
    JWT_SECRET_KEY_REFRESH,
)
import jwt
from ninja.errors import ValidationError
from validate_email import validate_email
from password_validator import PasswordValidator
from datetime import datetime, timedelta

from django.conf import settings


def create_access_token(email):
    JWT_SECRET_KEY = getattr(settings, "JWT_SECRET_KEY", None)
    JWT_HASHING_ALGORITHM = getattr(settings, "JWT_HASHING_ALGORITHM", None)
    jwt_expiry_date = datetime.utcnow() + timedelta(
        days=settings.JWT_ACCESS_EXPIRY_IN_DAYS
    )
    payload = {"sub": email, "exp": jwt_expiry_date}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_HASHING_ALGORITHM)
    return token


def create_refresh_token(email):
    JWT_SECRET_KEY_REFRESH = getattr(settings, "JWT_SECRET_KEY_REFRESH", None)
    JWT_HASHING_ALGORITHM = getattr(settings, "JWT_HASHING_ALGORITHM", None)
    jwt_expiry_date = datetime.utcnow() + timedelta(
        days=settings.JWT_REFRESH_EXPIRY_IN_DAYS
    )
    payload = {"sub": email, "exp": jwt_expiry_date}
    token = jwt.encode(payload, JWT_SECRET_KEY_REFRESH, algorithm=JWT_HASHING_ALGORITHM)
    return token


password_schema = PasswordValidator()

password_schema.min(8).max(100).has().digits().has().no().spaces()


def validate_credentials(email, password):
    email_is_valid = validate_email(email)
    password_is_valid = password_schema.validate(password)
    if email_is_valid and password_is_valid:
        return True
    return False
