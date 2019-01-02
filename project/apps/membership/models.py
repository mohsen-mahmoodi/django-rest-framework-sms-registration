from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import AbstractUser, Group as AuthGroup, UserManager as DjangoUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.signing import TimestampSigner
from django.conf import settings

from phonenumber_field import modelfields


class Group(AuthGroup):
    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')


class User(AbstractUser):
    INVALID_PIN = '##########'

    mobile = modelfields.PhoneNumberField(unique=True, verbose_name=_('mobile number'))
    is_verified = models.BooleanField(default=False, editable=False, verbose_name=_('verified'))
    is_registered = models.BooleanField(default=False, editable=False, verbose_name=_('registered'))
    pin = models.CharField(max_length=10, editable=False, verbose_name=_('PIN'))
    last_generated = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_('last pin generated date'))

    REQUIRED_FIELDS = ['email', 'mobile']

    signer = TimestampSigner(sep=':', salt='membership.apps.User')

    def clean(self):
        if self.mobile and not str(getattr(self.mobile, 'country_code', '')) in settings.VALID_MOBILE_COUNTRY_CODES:
            raise ValidationError({'mobile': _('Country code is not valid.')})

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = 'user_0' + str(self.mobile.national_number)

        # prevent staff members access_token hijacking through registration API
        if self.is_staff or self.is_superuser:
            self.is_verified = True
            self.is_registered = True
        super(User, self).save(*args, **kwargs)

