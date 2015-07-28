from rest_framework import viewsets, filters
from rest_framework_gis.pagination import GeoJsonPagination

from api.serializers import LocationSerializer
from events.models import Location


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    pagination_class = GeoJsonPagination
    serializer_class = LocationSerializer
