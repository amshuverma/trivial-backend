from django.contrib import admin
from .models import CustomUser, UserToken

admin.site.register(CustomUser)
admin.site.register(UserToken)
