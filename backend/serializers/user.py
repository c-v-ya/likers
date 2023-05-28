from rest_framework import serializers

from backend.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = read_only_fields = (
            "username",
            "first_name",
            "last_name",
        )
