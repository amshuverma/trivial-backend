from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .models import UserToken


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_tokens(sender, instance, created, **kwargs):
    if created:
        UserToken.objects.create(user=instance)
