# -*- coding: utf-8 -*-
"""
Dev Docker Configurations

- Runs in Debug mode
"""

import os

from configurations import values
from .local import Local


class Docker(Local):

    INTERNAL_IPS = ('*', '127.0.0.1',)

    GEOS_LIBRARY_PATH = values.Value('', environ_prefix=False)
    GDAL_LIBRARY_PATH = values.Value('', environ_prefix=False)
    PROJ4_LIBRARY_PATH = values.Value('', environ_prefix=False)

    DATABASES = values.DatabaseURLValue('postgis://postgres:postgres@db:5432/twd')
