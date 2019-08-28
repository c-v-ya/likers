from django.db import transaction
from rest_framework import serializers

from src.apps.backend.models import User


class SignUpRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    custom_error_messages = {
        'user_exists_error': 'This user already exists'
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        if User.objects.filter(
            **{key: val for key, val in validated_data.items()}
        ).exists():
            raise serializers.ValidationError(
                self.custom_error_messages.get('user_exists_error'),
                code='invalid'
            )

        with transaction.atomic():
            user = super().create(validated_data)
            user.set_password(password)
            user.save()

        return user
