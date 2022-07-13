from ninja.errors import ValidationError

from .models import UserToken


def save_or_update_refresh_token(refresh_token, user) -> bool:
    if not refresh_token or not user:
        return False
    try:
        user_token = UserToken.objects.get(user=user)
    except UserToken.DoesNotExist:
        return False
    user_token.token = refresh_token
    user_token.save()
    return True
