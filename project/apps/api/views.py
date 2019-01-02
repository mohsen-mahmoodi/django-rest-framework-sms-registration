import datetime
import logging

from django.conf import settings
from six import text_type

from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler, APIView

from rest_framework_simplejwt.views import TokenObtainPairView as TokenObtainView
from rest_framework_simplejwt.tokens import RefreshToken

from project.apps.api import serializers, exceptions, throttling
from project.apps.membership import utils
from project.apps.membership.models import User

logger = logging.getLogger('achare.api')


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and isinstance(exc, APIException):
        if isinstance(response.data, list):
            response.data = {
                'detail': response.data
            }
        response.data['status_code'] = response.status_code
        response.data['error_code'] = exc.default_code

    return response


class RegistrationView(APIView):
    throttle_classes = [throttling.RegistererMobileRateThrottle]

    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # this rarely happens in API or by a malicious user, but
            # worth considering if the App provides such a call.
            raise exceptions.UserLoggedIn()

        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate new pin if the old one is expired
        if user.last_generated < timezone.now() - datetime.timedelta(
                minutes=settings.REGISTRATION_PIN_EXPIRATION_MINUTES):
            user.pin = utils.generate_pin()
            user.last_generated = timezone.now()
            user.save(update_fields=['pin', 'last_generated'])

        self.send_verification_sms(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_verification_sms(self, user):
        print('SMS send to user with code: %s' % user.pin)


class VerificationView(APIView):
    permission_classes = (
        permissions.AllowAny,
    )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': text_type(refresh),
            'access': text_type(refresh.access_token)
        }

    def post(self, request, *args, **kwargs):
        serializer = serializers.VerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if not user.is_verified:
            user.is_verified = True
            # activate the user only in first verification, after that the user can't activate herself
            user.is_active = True
            user.pin = User.INVALID_PIN
            user.save(update_fields=['is_verified', 'is_active', 'pin'])

        return Response(self.get_token(user), status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        serializer = serializers.ProfileSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['password'])
        request.user.is_registered = True
        request.user.save(update_fields=['password', 'is_registered'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenObtainPairView(TokenObtainView):
    serializer_class = serializers.TokenObtainPairSerializer


class ServiceView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({'Services': 'successful'}, status=status.HTTP_200_OK)
