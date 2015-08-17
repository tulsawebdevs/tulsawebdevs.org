# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..api.serializers import GeoLocationSerializer
from events.models import Location


class TestGeoLocationSerializer(TestCase):
    def setUp(self):
        self.serializer = GeoLocationSerializer()

    def test_mro(self):
        self.assertIsInstance(self.serializer, GeoFeatureModelSerializer)

    def test_meta_class(self):
        meta = GeoLocationSerializer.Meta

        self.assertEqual(meta.model, Location)
        self.assertEqual(meta.geo_field, 'location')
        self.assertEqual(meta.id_field, False)
        self.assertEqual(meta.fields, ('id', 'name', 'resource_uri', 'address', 'location', 'meta'))
        self.assertEqual(meta.read_only_fields, ('location',))
