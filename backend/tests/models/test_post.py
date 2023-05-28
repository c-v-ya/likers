import datetime

import pytest
from django.db import IntegrityError

from backend.models import Post


@pytest.mark.django_db
def test_post_required_author():
    with pytest.raises(IntegrityError):
        Post.objects.create(text="Test post")


@pytest.mark.django_db
def test_post_has_posted_date(user):
    post = Post.objects.create(author=user, text="Test post")
    assert isinstance(post.posted_on, datetime.datetime)
