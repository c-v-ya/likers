from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name="Email", blank=False, unique=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.id, self.email}"


class Post(models.Model):
    author = models.ForeignKey(
        to=User, verbose_name="Post", related_name="posts", on_delete=models.deletion.CASCADE
    )
    text = models.TextField(verbose_name="Text", max_length=1000)
    posted_on = models.DateTimeField(verbose_name="Posted on", auto_now=True)
    liked_by = models.ManyToManyField(to=User, verbose_name="Liked by", related_name="liked_posts")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.id} {self.posted_on.isoformat()}"

    @property
    def likes_count(self):
        return self.liked_by.count()
