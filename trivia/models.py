import uuid

from abstract_models import TimeStampedModel
from django.conf import settings
from django.db import models


class TriviaCategory(TimeStampedModel):

    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )
    name = models.CharField(
        max_length=100, verbose_name="Trivia Category Name", null=False, blank=False
    )
    description = models.TextField(
        verbose_name="Trivia category description", null=False, blank=False
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Trivia Category"
        verbose_name_plural = "Trivia Categories"


class Trivia(TimeStampedModel):

    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public Identifier",
    )
    category = models.ForeignKey(to=TriviaCategory, on_delete=models.CASCADE)
    question = models.TextField(
        verbose_name="Trivia Questions", null=False, blank=False
    )
    option_1 = models.CharField(max_length=200, null=False, blank=False)
    option_2 = models.CharField(max_length=200, null=False, blank=False)
    option_3 = models.CharField(max_length=200, null=False, blank=False)
    correct_option = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["created_date"]
        verbose_name = "Trivia Question"
        verbose_name_plural = "Trivia Questions"


class UserTriviaLog(TimeStampedModel):
    session_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    total_correct_answers = models.IntegerField(null=False, blank=False)
    total_wrong_answers = models.IntegerField(null=False, blank=False)
    total_time_spent_in_seconds = models.IntegerField(null=False, blank=False)
    trivia_category = models.ForeignKey(to=TriviaCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "User Trivia Logs"
        ordering = ["created_date"]
