from rest_framework import serializers

from src.apps.backend.models import Post
from src.apps.backend.serializers.user import UserResponseSerializer


class PostResponseSerializer(serializers.ModelSerializer):
    author = UserResponseSerializer(read_only=True)

    class Meta:
        model = Post
        fields = read_only_fields = (
            'id', 'author', 'text', 'posted_on', 'likes_count'
        )
