from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from events.models import Location


class LocationSerializer(GeoFeatureModelSerializer):

    resource_uri = serializers.HyperlinkedIdentityField(
        view_name='api:location-detail', read_only=True)

    class Meta:
        model = Location
        geo_field = 'location'
        id_field = False
        fields = ('id', 'name', 'resource_uri', 'address', 'location')
