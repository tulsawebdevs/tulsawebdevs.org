# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from events.models import Location, Event, Occurrence
from api.fields import StraightJSONField


class GeoLocationSerializer(GeoFeatureModelSerializer):

    resource_uri = serializers.HyperlinkedIdentityField(
        view_name='api:location-detail', read_only=True)

    meta = StraightJSONField(read_only=True)

    class Meta:
        model = Location
        geo_field = 'location'
        id_field = False
        fields = ('id', 'name', 'resource_uri', 'address', 'location', 'meta',)
        read_only_fields = ('location',)


class EventSerializer(serializers.ModelSerializer):

    resource_uri = serializers.HyperlinkedIdentityField(
        view_name='api:event-detail', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'resource_uri', 'title', 'description', 'category', 'recurrences',)


class GeoOccurrenceSerializer(GeoFeatureModelSerializer):

    resource_uri = serializers.HyperlinkedIdentityField(
        view_name='api:occurrence-detail', read_only=True)

    # a field which contains a geometry value and can be used as geo_field
    location = GeometrySerializerMethodField()

    class Meta:
        model = Occurrence
        geo_field = 'location'
        id_field = False
        fields = ('id', 'resource_uri', 'title', 'description', 'start', 'end', 'location',)

    def get_location(self, obj):
        try:
            # Get the location from relation
            return obj.location.location
        except AttributeError:
            return None
