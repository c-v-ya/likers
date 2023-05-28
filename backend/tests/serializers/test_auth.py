import pytest
from django.db import transaction
from rest_framework import serializers

from backend.serializers.auth import SignUpRequestSerializer


@pytest.fixture
def serializer():
    return SignUpRequestSerializer()


@pytest.fixture
def validated_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def user_filter_mock(mocker):
    return mocker.patch("backend.serializers.auth.User.objects.filter")


@pytest.fixture
def email_hunter_mock(mocker):
    return mocker.patch("backend.serializers.auth.EmailHunter")


@pytest.mark.django_db
def test_create_user(serializer, validated_data, email_hunter_mock):
    password = validated_data["password"]
    email = validated_data["email"]

    with transaction.atomic():
        user = serializer.create(validated_data)

    email_hunter_mock.email_valid.assert_called_once_with(email)

    assert user.username == validated_data["username"]
    assert user.email == email
    assert user.check_password(password)


def test_create_user_with_invalid_email(serializer, validated_data, email_hunter_mock):
    email_hunter_mock.email_valid.return_value = False

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.create(validated_data)

    assert exc_info.value.args[0] == serializer.custom_error_messages["invalid_email"]


def test_create_user_with_existing_user(
    serializer, validated_data, user_filter_mock, email_hunter_mock
):
    email_hunter_mock.email_valid.return_value = True
    user_filter_mock.exists.return_value = True

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.create(validated_data)

    assert exc_info.value.args[0] == serializer.custom_error_messages["user_exists_error"]
