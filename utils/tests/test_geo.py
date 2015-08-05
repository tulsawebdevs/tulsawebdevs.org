# -*- coding: utf-8 -*-
from django.test import TestCase
import fudge

from geopy.exc import GeopyError
from utils.geo import geocode


class TestGeocode(TestCase):

    @fudge.patch('utils.geo.geolocator', 'utils.geo.logger')
    def test_geocode_error(self, geolocator, logger):

        (geolocator.is_a_stub()
            .expects('geocode').with_args('an address').raises(GeopyError))
        logger.is_a_stub().expects('exception')

        result = geocode('an address')

        self.assertEqual(result, None)

    @fudge.patch('utils.geo.geolocator', 'utils.geo.logger')
    def test_geocode_success(self, geolocator, logger):

        (geolocator.is_a_stub()
            .expects('geocode').with_args('an address').returns('geolocator.geocode result'))
        logger.is_a_stub().provides('exception')

        result = geocode('an address')

        self.assertEqual(result, 'geolocator.geocode result')
