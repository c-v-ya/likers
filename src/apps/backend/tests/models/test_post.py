import datetime

from django.db import IntegrityError
from django.test import TestCase

from src.apps.backend.models import User, Post


class TestPost(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create()

    def test_required_author(self):
        with self.assertRaises(IntegrityError):
            Post.objects.create(text='Test post')

    def test_has_posted_date(self):
        post = Post.objects.create(author=self.author, text='Test post')
        self.assertTrue(isinstance(post.posted_on, datetime.datetime))
