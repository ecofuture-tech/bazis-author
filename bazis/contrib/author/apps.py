from django.utils.translation import gettext_lazy as _

from bazis.core.utils.apps import BaseConfig


class AuthingConfig(BaseConfig):
    name = 'bazis.contrib.author'
    verbose_name = _('Author')
