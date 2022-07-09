import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager
from abstract_models import TimeStampedModel


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email address", unique=True)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    country = models.CharField(blank=False, max_length=25)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserToken(TimeStampedModel):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.TextField(max_length=200)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"Token for {self.user}"
