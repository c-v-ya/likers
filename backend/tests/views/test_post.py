import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from backend.models import Post
from backend.views.post import PostView


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def view(factory):
    return PostView.as_view({"get": "list", "post": "create"})


@pytest.fixture
def post(user):
    return Post.objects.create(author=user, text="Test post", posted_on=timezone.now())


@pytest.mark.django_db
def test_post_view_list(view, factory, post, user):
    request = factory.get("/posts/")
    force_authenticate(request, user=user)

    response = view(request)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_view_create(view, factory, user):
    request = factory.post("/posts/", data={"text": "Test post"}, format="json")
    force_authenticate(request, user=user)

    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_post_view_like(view, factory, post, user):
    post.liked_by.add(user)

    request = factory.get(reverse("backend:post-like", args=[post.id]))
    force_authenticate(request, user=user)

    response = view(request, pk=post.id)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_view_unlike(view, factory, post, user):
    post.liked_by.add(user)

    request = factory.get(reverse("backend:post-unlike", args=[post.id]))
    force_authenticate(request, user=user)

    response = view(request, pk=post.id)
    assert response.status_code == status.HTTP_200_OK
