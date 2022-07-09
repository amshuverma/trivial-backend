import jwt
from ninja import Router
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError, ValidationError

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from .schema import UserRegistrationSchema, UserLoginSchema
from .models import CustomUser
from .utils import create_access_token, create_refresh_token, validate_credentials


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            JWT_SECRET_KEY = getattr(settings, "JWT_SECRET_KEY", None)
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[
                    "HS256",
                ],
            )
            email = payload.get("sub")
            if email is None:
                raise ValidationError({"message": "Token verification failed."})
            try:
                user = get_object_or_404(CustomUser, email=email)
            except CustomUser.DoesNotExist:
                raise AuthenticationError(
                    {"message": "Authentication failed. User does not exist."}
                )
        except jwt.PyJWTError as e:
            raise ValidationError({"message": "Token verification failed."})
        return user


router = Router()


@router.post("/register")
def register_user(request, payload: UserRegistrationSchema):
    try:
        email = payload.dict()["email"]
        password = payload.dict()["password"]
        first_name = payload.dict()["first_name"]
        last_name = payload.dict()["last_name"]
        country = payload.dict()["country"]
    except ValueError:
        raise ValidationError("One or more fields have been left blank.")
    credentials_is_valid = validate_credentials(email, password)
    if not credentials_is_valid:
        raise ValidationError("Email or password not valid.")
    email_exists = CustomUser.objects.filter(email=email).exists()
    if email_exists:
        raise ValidationError("An account with that email already exists.")
    user = CustomUser(
        email=email, first_name=first_name, last_name=last_name, country=country
    )
    user.set_password(password)
    user.save()
    access_token, refresh_token = create_access_token(user.email), create_refresh_token(
        user.email
    )
    return 201, {"access": access_token, "refresh_token": refresh_token}


@router.post("/login")
def login_user(request, payload: UserLoginSchema):
    email = payload.email
    password = payload.password
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        raise ValidationError({"message": "Incorrect email"})
    password_match = check_password(password, user.password)
    if not password_match:
        raise ValidationError({"message": "Incorrect password"})
    access_token, refresh_token = create_access_token(user.email), create_refresh_token(
        user.email
    )
    return 200, {"access": access_token, "refresh_token": refresh_token}


@router.post("/token")
def refresh_token(request, payload):
    token = payload
    if token is not None:
        try:
            jwt_payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY_REFRESH,
                algorithms=[
                    settings.JWT_HASHING_ALGORITHM,
                ],
            )
        except jwt.PyJWTError as e:
            raise ValidationError({"message": "Invalid token. Decode failed."})
        user_email = jwt_payload.get("sub", None)
        if user_email is None:
            raise ValidationError({"message": "Invalid Token"})
        access_token = create_access_token(user_email)
        return 200, {"access": access_token}
    return 401, {"message": "Invalid token."}
