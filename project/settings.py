"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
from datetime import timedelta

from configurations import Configuration, values


class Common(Configuration):
    # this will be the django-projects root directory where the manage.py file exists.
    BASE_DIR = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # this will be directory under which all the project's assets will be stored
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

    CONTENTS_DIR = os.path.join(BASE_DIR, 'contents')

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_extensions',
        'rest_framework',
        'phonenumber_field',

        'project.apps.membership.apps.MembershipConfig',
        'project.apps.api.apps.ApiConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'project.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'project.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )

    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                               'project.apps.membership.backends.MobileBackend']

    APPEND_SLASH = False

    # Internationalization
    # https://docs.djangoproject.com/en/2.1/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    MEDIA_URL = values.Value('/media/')

    STATIC_URL = values.Value('/statics/')

    MEDIA_ROOT = os.path.join(CONTENTS_DIR, 'media')

    STATIC_ROOT = os.path.join(CONTENTS_DIR, 'statics')

    STATICFILES_DIRS = (
        os.path.join(ASSETS_DIR, 'static'),
    )

    LOCALE_PATHS = (
        os.path.join(ASSETS_DIR, 'locale'),
    )

    FIXTURE_DIRS = (
        os.path.join(ASSETS_DIR, 'fixtures'),
    )

    AUTH_USER_MODEL = 'membership.User'

    LOGGING_LEVEL = values.Value('DEBUG', environ_prefix='ACHARE')

    LOGGING = values.DictValue({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO'
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'achare': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    })

    REST_FRAMEWORK = {
        'DEFAULT_VERSION': 'v1',
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
        'EXCEPTION_HANDLER': 'project.apps.api.views.api_exception_handler',
        # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],
        'DEFAULT_PERMISSION_CLASSES': ['project.apps.api.permissions.IsRegistered', ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ]
    }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': True,

        # 'ALGORITHM': 'HS256',
        # 'SIGNING_KEY': SECRET_KEY,
        # 'VERIFYING_KEY': None,

        'AUTH_HEADER_TYPES': ('Bearer',),
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',

        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',

        # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
        # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    }

    # membership and registration settings
    REGISTRATION_PIN_EXPIRATION_MINUTES = values.IntegerValue(5, environ_prefix='ACHARE')

    VALID_MOBILE_COUNTRY_CODES = values.ListValue(['98'], environ_prefix='ACHARE')

    REGISTRATION_SEND_SMS_INTERVAL = values.IntegerValue(120, environ_prefix='ACHARE')

    REGISTER_ATTEMPTS_LIMIT = values.IntegerValue(3, environ_prefix='ACHARE')

    VERIFY_ATTEMPTS_LIMIT = values.IntegerValue(10, environ_prefix='ACHARE')

    REGISTRATION_BAN_MINUTES = values.IntegerValue(30, environ_prefix='ACHARE')


class Development(Common):
    """
    The in-development settings and the default configuration.
    """

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar'
    ]


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )


class Production(Staging):
    """
    The in-production settings.
    """
    DEBUG = False
