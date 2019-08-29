from django.db import transaction
from django.db.models import Q
from rest_framework import serializers

from src.apps.backend.models import User
from src.apps.backend.services import EmailHunter
from src.apps.backend.services.clearbit import ClearBit


class SignUpRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    custom_error_messages = {
        'user_exists_error': 'This user already exists',
        'invalid_email': 'This email is not deliverable',
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data: dict):
        password = validated_data.pop('password')

        # Checking for deliverability of an email via EmailHunter
        email = validated_data.get('email')
        self.check_email(email)

        if User.objects.filter(
                Q(email=email) |
                Q(username=validated_data.get('username'))
        ).exists():
            raise serializers.ValidationError(
                self.custom_error_messages.get('user_exists_error'),
                code='invalid'
            )

        with transaction.atomic():
            user = super().create(validated_data)
            user.set_password(password)
            user.save()

        # Enrich user via ClearBit if there was no first or last name
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not any([first_name, last_name]):
            ClearBit.enrich_user(user)

        return user

    def check_email(self, email):
        if not EmailHunter.email_valid(email):
            raise serializers.ValidationError(
                self.custom_error_messages.get('invalid_email'),
                code='invalid'
            )
