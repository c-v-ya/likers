from django.contrib import admin
from django.contrib.auth import get_user_model

from backend.models import Post

User = get_user_model()

admin.site.register(User)
admin.site.register(Post)
