import jwt
from ninja import Router
from ninja.security import HttpBearer
from ninja.errors import ValidationError, HttpError

from django.db import transaction
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.hashers import check_password

from .schema import UserRegistrationSchema, UserLoginSchema, CurrentUserSchema
from .observer import save_or_update_refresh_token
from .models import CustomUser, UserToken
from .utils import (
    create_access_token,
    create_refresh_token,
    token_blacklisted,
)

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        is_blacklisted = cache.get(f"ac_{token}")
        print(is_blacklisted)
        if is_blacklisted is not None:
            raise ValidationError("Token not authorized.")
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
                raise ValidationError("Invalid token.")
        except jwt.PyJWTError as e:
            raise ValidationError("Pyjwt error")
        return email


router = Router()


@router.post("/register")
def register_user(request, payload: UserRegistrationSchema):
    email = payload.email
    email_exists = CustomUser.objects.filter(email=email).exists()
    if email_exists:
        raise ValidationError("An account with that email already exists.")
    with transaction.atomic():
        user = CustomUser(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            country=payload.country,
        )
        user.set_password(payload.password)
        user.save()
        access_token, refresh_token = create_access_token(
            user.email
        ), create_refresh_token(user.email)
        user_token = user.usertoken
        user_token.token = refresh_token
        user_token.save(update_fields=["token"])
    return 200, {"access": access_token, "refresh_token": refresh_token}


@router.post("/login")
def login_user(request, payload: UserLoginSchema):
    email = payload.email
    password = payload.password
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        raise ValidationError({"message": "Incorrect email"})
    print(cache.get(f"rf_{user.usertoken.token}"))
    password_match = check_password(password, user.password)
    if not password_match:
        raise ValidationError("Incorrect password")
    try:
        refresh_token = UserToken.objects.get(user=user).token
    except UserToken.DoesNotExist:
        refresh_token = create_refresh_token(user.email)
        is_token_saved = save_or_update_refresh_token(refresh_token, user)
        if not is_token_saved:
            raise ValidationError("User does not exist.")
    if refresh_token.strip() == "" or refresh_token is None:
        refresh_token = create_refresh_token(user.email)
        is_token_saved = save_or_update_refresh_token(refresh_token, user)
        if not is_token_saved:
            raise ValidationError("User does not exist.")
    access_token = create_access_token(user.email)
    return 200, {"access": access_token, "refresh_token": refresh_token}


@router.post("/token")
def refresh_token(request, payload: str):
    token = payload
    if token is not None:
        if not token_blacklisted(token):
            try:
                jwt_payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY_REFRESH,
                    algorithms=[
                        settings.JWT_HASHING_ALGORITHM,
                    ],
                )
            except jwt.PyJWTError as e:
                raise ValidationError("Invalid token. Decode failed.")
            user_email = jwt_payload.get("sub", None)
            if user_email is None:
                raise ValidationError({"message": "Invalid Token"})
            access_token = create_access_token(user_email)
            return 200, {"access": access_token}
        raise HttpError(401, "Invalid token")
    raise HttpError(401, "Invalid token")


@router.get("/current-user", auth=AuthBearer())
def get_current_user(request):
    try:
        user = CustomUser.objects.prefetch_related("usertoken").get(email=request.auth)
        refresh_token = user.usertoken.token
    except CustomUser.DoesNotExist:
        raise ValidationError("Authentication failed, User does not exist.")
    return 200, {"email": user.email, "refresh": refresh_token}


@router.get("/logout", auth=AuthBearer())
def logout(request):
    try:
        user = CustomUser.objects.get(email=request.auth)
    except CustomUser.DoesNotExist:
        raise ValidationError("Logout failed, User does not exist.")
    token = user.usertoken
    cache.set(f"rf_{token.token}", token.token)
    token.token = ""
    token.save()
    return 200, {"message": "Token invalidated. Logout successful"}
