# -*- coding: utf-8 -*-
"""
Django settings for tulsawebdevs.org project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

For the configurations module and it's values, see
https://github.com/jezdez/django-configurations
"""

import sys
from os.path import dirname, abspath, join

from configurations import Configuration, values


class Common(Configuration):

    # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

    BASE_DIR = dirname(dirname(abspath(__file__)))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'vhmc9lo887c)w%dum0oln(!wof(m#+f5$j8p#%&v=(3946n2ht'

    # SECURITY WARNING: don't run with debug turned on in production!
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # Whether or not to expect webpack in debug mode
    WEBPACK_DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = []

    # APP CONFIGURATION
    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.gis',
    )

    # Third-party apps, patches, fixes
    THIRD_PARTY_APPS = (
        'mptt',
        'recurrence',
        'django_extensions',
        'rest_framework',
        'rest_framework_gis',
        'webpack_loader',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'twd',
        'api',
        'events',
        'talks',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

    ROOT_URLCONF = 'twd.urls'

    WSGI_APPLICATION = 'twd.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases
    # https://github.com/kennethreitz/dj-database-url

    DATABASES = values.DatabaseURLValue('postgis://localhost/twd')

    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'America/Chicago'

    USE_TZ = True

    USE_I18N = False

    USE_L10N = False

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/

    STATIC_ROOT = join(BASE_DIR, 'static')
    STATIC_URL = values.Value('/static/')
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    MEDIA_ROOT = join(BASE_DIR, 'media/')
    MEDIA_URL = values.Value("/media/")

    # Rest framework settings

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        ),
        # 'DEFAULT_PAGINATION_CLASS': 'api.pagination.DateRangePagination',
    }

    # Templates

    # List of processors used by RequestContext to populate the context.
    # Each one should be a callable that takes the request object as its
    # only parameter and returns a dictionary to add to the context.
    DEFAULT_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        # "django.contrib.messages.context_processors.messages",
        "django.template.context_processors.debug",
        # "django.template.context_processors.i18n",
        "django.template.context_processors.static",
        "django.template.context_processors.media",
        "django.template.context_processors.request",
        # "django.template.context_processors.tz",
        "twd.context_processors.webpack_debug",
    )

    # https://niwinz.github.io/django-jinja/#_user_guide_for_django_1_8
    TEMPLATES = [
        {
            "BACKEND": "django_jinja.backend.Jinja2",
            "NAME": "jinja2",
            "APP_DIRS": True,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "OPTIONS": {
                "match_extension": ".jinja",
                "match_regex": r"^(?!admin|debug_toolbar/).*",
                "newstyle_gettext": True,
                "extensions": [
                    # "jinja2.ext.do",
                    # "jinja2.ext.loopcontrols",
                    # "jinja2.ext.with_",
                    "jinja2.ext.i18n",
                    # "jinja2.ext.autoescape",
                    # "django_jinja.builtins.extensions.CsrfExtension",
                    # "django_jinja.builtins.extensions.CacheExtension",
                    # "django_jinja.builtins.extensions.TimezoneExtension",
                    # "django_jinja.builtins.extensions.UrlsExtension",
                    # "django_jinja.builtins.extensions.StaticFilesExtension",
                    "django_jinja.builtins.extensions.DjangoFiltersExtension",
                    "django_jinja.builtins.extensions.DjangoExtraFiltersExtension",
                    "webpack_loader.contrib.jinja2ext.WebpackExtension",
                ],
                "context_processors": DEFAULT_CONTEXT_PROCESSORS,
                "autoescape": True,
                "auto_reload": DEBUG,
                "translation_engine": "django.utils.translation",
            }
        },
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": DEFAULT_CONTEXT_PROCESSORS
            },
        },
    ]

    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     }
    # }

    # Webpack
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': abspath(BASE_DIR + '/twd/assets/webpack.stats.json')
        }
    }

    # Place bcrypt first in the list, so it will be the default password hashing
    # mechanism
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.BCryptPasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.CryptPasswordHasher',
    )

    # Mail settings
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = values.Value('localhost')
    EMAIL_PORT = values.IntegerValue(1025)
    EMAIL_HOST_USER = values.Value('')
    EMAIL_HOST_PASSWORD = values.Value('')
    # End mail settings

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'py.warnings': {
                'handlers': ['console'],
            },
        }
    }

    # Detect that we're running tests
    TESTING = sys.argv[1:2] == ['test']

    # Sessions
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_URL = values.Value('redis://localhost/4')

    # Django nose
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    # memory db for testing
    if TESTING:
        DATABASES = values.DatabaseURLValue('postgis://localhost/twd-test')
