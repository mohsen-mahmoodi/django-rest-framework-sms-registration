import logging

from django.core.signing import BadSignature
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions
from django.contrib.auth import password_validation
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as TokenObtainSerializer

from phonenumber_field.serializerfields import PhoneNumberField

from project.apps.membership import utils
from project.apps.membership.models import User

logger = logging.getLogger('achare.api')


class UserRegistrationSerializer(serializers.Serializer):
    default_error_messages = {
        'already_registered': _('The user is already registered'),
        'cannot_create_user': _('Unable to create account.')
    }

    mobile = PhoneNumberField()
    signature = serializers.SerializerMethodField()

    def get_signature(self, obj):
        return utils.sign_uid(obj.id)

    def validate_mobile(self, value):
        try:
            user = User.objects.get(mobile=value)
            self.user = user
            if user and user.is_registered:
                self.fail('already_registered')
        except User.DoesNotExist:
            self.user = None
        return value

    def create(self, validated_data):
        if self.user:
            return self.user
        try:
            with transaction.atomic():
                user = User.objects.create(mobile=validated_data['mobile'], pin=utils.generate_pin(), number_of_tries=0,
                                           is_active=False)
        except IntegrityError:
            self.fail('cannot_create_user')
        return user


class VerificationCodeSerializer(serializers.Serializer):
    default_error_messages = {
        'invalid_code': _('The provided code is not valid'),
        'invalid_pin': _('Please register to get a valid code by SMS'),
        'invalid_signature': _('The provided signature is no longer valid'),
        'already_registered': _('The user is already registered')
    }

    code = serializers.CharField(write_only=True)
    signature = serializers.CharField(max_length=100)

    def validate_signature(self, value):
        try:
            uid = utils.decode_uid_signature(value, max_age=settings.REGISTRATION_SEND_SMS_INTERVAL)
            self.user = User.objects.get(pk=uid)
            return value
        except (BadSignature, User.DoesNotExist):
            self.fail('invalid_signature')

    def validate(self, data):
        data = super(VerificationCodeSerializer, self).validate(data)
        if self.user.pin == User.INVALID_PIN:
            # The user is validated already or verification requested before calling registration
            self.fail('invalid_pin')
        if self.user.pin == User.INVALID_PIN or data['code'] != self.user.pin:
            self.fail('invalid_code')
        if self.user.is_registered:
            # prevent user from logging in using registration process
            self.fail('already_registered')
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PasswordSerializer(serializers.Serializer):
    default_error_messages = {
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_password(self, value):
        try:
            password_validation.validate_password(password=value, user=self.instance)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        data = super(PasswordSerializer, self).validate(data)
        if data['password'] != data['password_confirm']:
            self.fail('password_mismatch')
        return data


class TokenObtainPairSerializer(TokenObtainSerializer):
    username_field = 'mobile'
