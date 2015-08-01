from django.test import TestCase
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.serializers import LocationSerializer


class TestLocationSerializer(TestCase):

    def test_mro(self):
        self.assertIsInstance(LocationSerializer(), GeoFeatureModelSerializer)

    def test_meta_class(self):
        pass
