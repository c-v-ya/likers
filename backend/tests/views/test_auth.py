import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from backend.views.auth import SignUpView


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def view(factory):
    return SignUpView.as_view()


@pytest.mark.django_db
def test_signup_view_post_authenticated(view, factory, user):
    request = factory.post(reverse("backend:sign_up"))
    force_authenticate(request, user=user)

    response = view(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_signup_view_post_invalid_data(view, factory):
    request = factory.post(reverse("backend:sign_up"), data={"username": "testuser"}, format="json")
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_view_post_valid_data(view, factory, mocker):
    mocker.patch("backend.serializers.auth.EmailHunter.email_valid", return_value=True)
    mock_enrich = mocker.patch("backend.serializers.auth.enrich.delay")
    request = factory.post(
        reverse("backend:sign_up"),
        data={"username": "testuser", "password": "testpassword", "email": "test@email.com"},
        format="json",
    )
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    mock_enrich.assert_called_once()
