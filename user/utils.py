from config.settings import (
    JWT_ACCESS_EXPIRY_IN_DAYS,
    JWT_HASHING_ALGORITHM,
    JWT_SECRET_KEY_REFRESH,
)
import jwt
from ninja.errors import ValidationError

from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.core.validators import validate_email as _validate_email
from django.core.exceptions import ValidationError

from password_validator import PasswordValidator


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


def token_blacklisted(token):
    is_blacklisted = cache.get(f"rf_{token}")
    if is_blacklisted is not None:
        return True
    return False


def validate_email(email):
    try:
        validated_email = _validate_email(email)
    except ValidationError as e:
        return False
    return True


passwordValidationSchema = PasswordValidator()

passwordValidationSchema.min(8).max(
    100
).has().uppercase().has().lowercase().has().digits().has().no().spaces()


def validate_password(password):
    return passwordValidationSchema.validate(password)
