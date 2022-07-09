from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings

from .models import UserToken


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def save_tokens(sender, instance, **kwargs):
    print("hi")
    token = UserToken.objects.create(user=instance)
    token.save()
