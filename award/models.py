import uuid
from tabnanny import verbose

from abstract_models import TimeStampedModel
from django.conf import settings
from django.db import models


class Award(TimeStampedModel):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public Identifier",
    )
    name = models.CharField(
        max_length=200, verbose_name="Award Name", null=False, blank=False
    )
    description = models.TextField(
        verbose_name="Award Description", null=False, blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Awards"
        ordering = ["-name"]


class AwardUser(TimeStampedModel):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public Identifier",
    )
    received_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False
    )
    award = models.ForeignKey(
        to=Award, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return f"Received {self.award} by {self.received_by.first_name}"

    class Meta:
        verbose_name_plural = "Awards - Users"
