from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle
from django.conf import settings


class BaseRegisterationRateThrottle(SimpleRateThrottle):
    """
         Limit calling the registration API with a specific mobile/ip according to following constraints:

         1. interval between each call: settings.REGISTRATION_SEND_SMS_INTERVAL seconds e.g. 1 call per 2 minu
         2. only settings.REGISTER_ATTEMPTS_LIMIT attempts can be done in every
            settings.REGISTRATION_SEND_SMS_INTERVAL * settings.REGISTER_ATTEMPTS_LIMIT seconds e.g. 3 calls in  6 min
         3. calling the api more than the second  REGISTER_ATTEMPTS_LIMIT in the REGISTER_ATTEMPTS_LIMIT  *
          REGISTER_ATTEMPTS_LIMIT seconds, banes the user for settings.REGISTRATION_BAN_MINUTES minutes

     """

    def __init__(self):
        self.num_requests = settings.REGISTER_ATTEMPTS_LIMIT
        self.interval = settings.REGISTRATION_SEND_SMS_INTERVAL
        self.banning_duration = settings.REGISTRATION_BAN_MINUTES * 60
        self.duration = self.num_requests * self.interval

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True
        self.history = self.cache.get(self.key, {
            'banned': False,
            'banned_time': None,
            'requests': []})
        self.now = self.timer()

        requests = self.history['requests']
        banned = self.history['banned']
        banned_time = self.history['banned_time']

        if banned and banned_time > self.now - self.banning_duration:
            return self.throttle_failure()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while requests and requests[-1] <= self.now - self.duration:
            requests.pop()

        self.history['requests'] = requests

        # the maximum number of requests reached, ban the user
        if len(requests) >= self.num_requests:
            self.history['banned'] = True
            self.history['banned_time'] = self.now
            return self.throttle_failure(True)

        # the interval is not passed yet, throttle the request
        if len(requests) > 0 and requests[0] > self.now - self.interval:
            return self.throttle_failure()

        return self.throttle_success()

    def throttle_failure(self, update_cache=False):
        """
        Called when a request to the API has failed due to throttling.
        """
        if update_cache:
            self.cache.set(self.key, self.history, self.banning_duration)

        return False

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history['requests'] = [self.now] + self.history['requests']
        self.history['banned'] = False
        self.cache.set(self.key, self.history, self.duration)
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            if self.history['banned']:
                remaining_duration = self.banning_duration - (self.now - self.history['banned_time'])
            elif self.history['requests']:
                remaining_duration = self.interval - (self.now - self.history['requests'][0])
        else:
            remaining_duration = self.interval

        return remaining_duration


class RegistererMobileRateThrottle(BaseRegisterationRateThrottle):
    """
        Limit calling the registration API with a specific mobile number.
    """
    scope = 'registration.mobile'

    def get_cache_key(self, request, view):
        identity = request.data.get('mobile', None)

        if identity is None:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': identity
        }


class RegistererIPRateThrottle(BaseRegisterationRateThrottle):
    """
        Limit calling the registration API with a specific IP.
    """
    scope = 'registration.ip'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class VerificationRateThrottle(AnonRateThrottle):
    """
        Limit calling the verification API with a specific signature.
    """
    scope = 'verification'
    rate = '#/#'

    def parse_rate(self, rate):
        return settings.VERIFY_ATTEMPTS_LIMIT, settings.REGISTRATION_SEND_SMS_INTERVAL

    def get_cache_key(self, request, view):
        identity = request.data.get('signature', None)

        if identity is None:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': identity
        }
