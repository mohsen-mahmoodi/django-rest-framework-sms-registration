from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'project.apps.api'
    verbose_name = _('api')
