from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from src.apps.backend.models import User


class TestAuthView(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'test',
            'email': 'test@test.test',
            'password': 'test',
        }

    @patch('src.apps.backend.services.clearbit')
    def test_sign_up_creates_user(self, clearbit_mock):
        # Mock Clearbit service so we don't hit API every time we run test
        clearbit_mock.Clearbit.enrich_user.return_value = None
        response = self.client.post(
            reverse('backend:sign_up'),
            data=self.data, content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            User.objects.filter(username=self.data.get('username')).exists()
        )

    def test_sign_up_requires_username(self):
        data = self.data.copy()
        del data['username']
        response = self.client.post(
            reverse('backend:sign_up'),
            data=data, content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertFalse(User.objects.filter(email=data.get('email')).exists())

    def test_sign_up_requires_email(self):
        data = self.data.copy()
        del data['email']
        response = self.client.post(
            reverse('backend:sign_up'),
            data=data, content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertFalse(
            User.objects.filter(username=data.get('username')).exists()
        )

    def test_sign_up_requires_password(self):
        data = self.data.copy()
        del data['password']
        response = self.client.post(
            reverse('backend:sign_up'),
            data=data, content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertFalse(User.objects.filter(email=data.get('email')).exists())

    def test_sign_up_handles_existing_username(self):
        data = self.data.copy()
        User.objects.create(username=data.get('username'))
        response = self.client.post(
            reverse('backend:sign_up'),
            data=data, content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            1, User.objects.filter(username=data.get('username')).count()
        )

    def test_sign_up_handles_existing_email(self):
        data = self.data.copy()
        User.objects.create(email=data.get('email'))
        response = self.client.post(
            reverse('backend:sign_up'),
            data=data, content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            1, User.objects.filter(email=data.get('email')).count()
        )
