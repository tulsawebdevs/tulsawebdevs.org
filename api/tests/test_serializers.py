from django.test import TestCase
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.serializers import LocationSerializer
from events.models import Location


class TestLocationSerializer(TestCase):

    def test_mro(self):
        self.assertIsInstance(LocationSerializer(), GeoFeatureModelSerializer)

    def test_meta_class(self):
        meta = LocationSerializer.Meta

        self.assertEqual(meta.model, Location)
        self.assertEqual(meta.geo_field, 'location')
        self.assertEqual(meta.id_field, False)
        self.assertEqual(meta.fields, ('id', 'name', 'resource_uri', 'address', 'location', 'meta'))
        self.assertEqual(meta.read_only_fields, ('location',))
