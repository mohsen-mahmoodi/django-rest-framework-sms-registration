from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MembershipConfig(AppConfig):
    name = 'project.apps.membership'
    verbose_name = _('membership')
