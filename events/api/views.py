from django.utils.timezone import now, timedelta
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination

from .serializers import GeoLocationSerializer, EventSerializer, GeoOccurrenceSerializer
from events.models import Location, Event, Occurrence


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    pagination_class = GeoJsonPagination
    serializer_class = GeoLocationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all()
    pagination_class = GeoJsonPagination
    serializer_class = GeoOccurrenceSerializer


class UpcomingView(generics.GenericAPIView):
    serializer_class = GeoOccurrenceSerializer

    # authentication_classes
    permission_classes = ()

    def get(self, *args, **kwargs):
        qs_kwargs = {
            'start': now(),
            'end': now() + timedelta(40)
        }
        occurrences = Event.objects.get_occurrences(**qs_kwargs)
        serializer = self.get_serializer(occurrences, many=True)
        return Response(serializer.data)
