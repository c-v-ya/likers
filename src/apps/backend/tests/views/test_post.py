from django.test import TestCase
from django.urls import reverse

from src.apps.backend.models import User, Post


class TestPostView(TestCase):

    def test_no_access_for_anonymous_user(self):
        user = User.objects.create(username='test')
        Post.objects.create(author=user, text='test')
        response = self.client.get(
            reverse('backend:post_list', args=[user.username])
        )
        self.assertEqual(401, response.status_code)
