from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from events.api.views import LocationViewSet, EventViewSet, OccurrenceViewSet, UpcomingView


router = DefaultRouter()


router.register(r'locations', LocationViewSet, base_name='location')
router.register(r'events', EventViewSet, base_name='event')
router.register(r'occurrences', OccurrenceViewSet, base_name='occurrence')


urlpatterns = router.urls


urlpatterns += (
    url(r'^upcoming/$', UpcomingView.as_view(), name='upcoming'),
)
