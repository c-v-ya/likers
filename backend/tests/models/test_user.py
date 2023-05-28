import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_user_unique_email(user):
    with pytest.raises(IntegrityError):
        User.objects.create(email=user.email)
