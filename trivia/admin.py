from django.contrib import admin
from .models import Trivia, TriviaCategory, UserTriviaLog

admin.site.register(Trivia)
admin.site.register(TriviaCategory)
admin.site.register(UserTriviaLog)
