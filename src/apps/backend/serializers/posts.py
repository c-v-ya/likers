from rest_framework import serializers

from src.apps.backend.models import Post


class PostResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = read_only_fields = (
            'id', 'author', 'text', 'posted_on', 'likes_count'
        )
