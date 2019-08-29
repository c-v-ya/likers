from django.db import IntegrityError
from django.test import TestCase

from src.apps.backend.models import User


class TestUser(TestCase):
    def test_unique_email(self):
        email = 'test@test.test'
        User.objects.create(email=email)
        with self.assertRaises(IntegrityError):
            User.objects.create(email=email)
