from django.conf import settings
from django.contrib.gis.db import models

from bazis.contrib.users.models_abstract import UserMixin


class AuthorMixin(UserMixin):
    """
    Mixin that enables working with author fields in a model
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='author_%(class)s',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    author_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='author_updated_%(class)s',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if author := self.CTX_USER_REQUEST.get():
            if not self.author:
                self.author = author
            self.author_updated = author
        super().save(*args, **kwargs)
