from rest_framework import serializers

from backend.models import Post


class PostResponseSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = read_only_fields = (
            "id",
            "author",
            "text",
            "posted_on",
            "likes_count",
        )


class PostRequestSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000)
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("text", "author_id")

    def save(self, **kwargs):
        user = self.context["request"].user
        super(PostRequestSerializer, self).save(author_id=user.id, **kwargs)
