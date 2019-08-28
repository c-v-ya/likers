from django.contrib import admin

from src.apps.backend import models

admin.site.register(models.User)
admin.site.register(models.Post)
