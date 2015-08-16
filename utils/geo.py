# -*- coding: utf-8 -*-
import logging

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
geolocator = Nominatim()


logger = logging.getLogger(__name__)


def geocode(address):
    try:
        return geolocator.geocode(address)
    except GeopyError as e:
        logger.exception(e)
        return None
