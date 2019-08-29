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


class PostRequestSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000)
    author_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('text', 'author_id')
