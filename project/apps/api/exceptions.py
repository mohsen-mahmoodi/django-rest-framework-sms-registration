from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class UserLoggedIn(APIException):
    status_code = 400
    default_detail = _('The request contains a logged in user.')
    default_code = 'user_logged_in'
