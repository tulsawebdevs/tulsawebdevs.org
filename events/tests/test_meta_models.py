# -*- coding: utf-8 -*-
"""Tests for events models."""
from django.contrib.gis.geos import Point
from django.test import TestCase
from model_mommy import mommy
import fudge

from events.models.meta import Location


class LocationModelTest(TestCase):
    """The Location model supports storing machine and human readable locations."""

    def setUp(self):
        self.location = mommy.prepare(
            Location, name='Location Name', address='an address')

    def test_str(self):
        self.assertEqual(str(self.location), 'Location Name')

    @fudge.patch('events.models.meta.md5')
    @fudge.patch('events.models.meta.geocode')
    def test_save_with_matched_location_hash(self, md5, geocode):
        self.location.location = Point([123, 123])
        self.location.location_hash = 'this'

        (md5.expects_call().with_args(b'Location Name@an address').returns_fake()
            .expects('hexdigest').returns('this'))

        self.location.save()

        # meta remains unchanged
        self.assertEqual(self.location.meta, None)
        # Location is unchanged
        self.assertEqual(self.location.location, Point([123, 123]))
        # hash is unchanged
        self.assertEqual(self.location.location_hash, 'this')

    @fudge.patch('events.models.meta.md5')
    @fudge.patch('events.models.meta.geocode')
    def test_save_with_missed_location_hash_and_address_present(self, md5, geocode):
        self.location.location = Point([123, 123])
        self.location.location_hash = 'not this'

        (md5.expects_call().with_args(b'Location Name@an address').returns_fake()
            .expects('hexdigest').returns('this'))
        mock_location_geocode = fudge.Fake('location_geocode').has_attr(
            raw={'raw': 'data', 'lat': '123.4', 'lon': '-12.3'})
        geocode.expects_call().with_args('an address').returns(mock_location_geocode)

        self.location.save()

        # meta set from gecode raw
        self.assertEqual(
            self.location.meta, {'raw': 'data', 'lat': '123.4', 'lon': '-12.3'})
        # Location is set
        self.assertEqual(self.location.location, Point([-12.3, 123.4]))
        # hash is updated
        self.assertEqual(self.location.location_hash, 'this')

    @fudge.patch('events.models.meta.md5')
    @fudge.patch('events.models.meta.geocode')
    def test_save_with_missed_location_hash_and_address_present_geocode_fail(self, md5, geocode):
        self.location.location = Point([123, 123])
        self.location.location_hash = 'not this'

        (md5.expects_call().with_args(b'Location Name@an address').returns_fake()
            .expects('hexdigest').returns('this'))
        geocode.expects_call().with_args('an address').returns(None)

        self.location.save()

        # meta had error state
        self.assertEqual(
            self.location.meta, {'geocoded': False})
        # Location is unset
        self.assertEqual(self.location.location, None)
        # hash is not updated
        self.assertEqual(self.location.location_hash, 'not this')

    @fudge.patch('events.models.meta.md5')
    @fudge.patch('events.models.meta.geocode')
    def test_save_with_missed_location_hash_no_address(self, md5, geocode):
        self.location.location = Point([123, 123])
        self.location.location_hash = 'not this'
        self.location.address = None

        (md5.expects_call().with_args(b'Location Name@None').returns_fake()
            .expects('hexdigest').returns('this'))

        self.location.save()

        # meta remains unchanged
        self.assertEqual(self.location.meta, None)
        # Location is unchanged
        self.assertEqual(self.location.location, Point([123, 123]))
        # hash is unchanged
        self.assertEqual(self.location.location_hash, 'not this')
        # Address is unchanged
        self.assertEqual(self.location.address, None)
