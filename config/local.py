# -*- coding: utf-8 -*-
"""
Local Configurations

- Runs in Debug mode
"""

import os

from configurations import values
from django.utils.crypto import get_random_string
from .common import Common


class Local(Common):

    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG

    INTERNAL_IPS = ('*', '127.0.0.1',)

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", get_random_string(50, (
            "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")))

    INSTALLED_APPS = Common.INSTALLED_APPS

    INSTALLED_APPS += ('debug_toolbar',)

    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
