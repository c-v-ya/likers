from django.db import models
from django.utils.translation import ugettext_lazy as _

from src.apps.backend.models import User


class Post(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name=_('Post'),
        related_name='posts',
        on_delete=models.deletion.CASCADE,
    )

    text = models.TextField(
        verbose_name=_('Text'),
        max_length=1000,
    )

    posted_on = models.DateTimeField(
        verbose_name=_('Posted on'),
        auto_now=True,
    )

    liked_by = models.ManyToManyField(
        to=User,
        verbose_name=_('Liked by'),
        related_name='liked_posts',
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f'{self.id} {self.posted_on.isoformat()}'

    @property
    def likes_count(self):
        return self.liked_by.count()
