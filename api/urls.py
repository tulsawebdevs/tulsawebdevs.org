from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from events.api.views import LocationViewSet, EventViewSet, OccurrenceViewSet, UpcomingView
from talks.api.views import SpeakerViewSet, TalkViewSet


router = DefaultRouter()


router.register(r'locations', LocationViewSet, base_name='location')
router.register(r'events', EventViewSet, base_name='event')
router.register(r'occurrences', OccurrenceViewSet, base_name='occurrence')
router.register(r'speakers', SpeakerViewSet, base_name='speaker')
router.register(r'talks', TalkViewSet, base_name='talk')


urlpatterns = router.urls


urlpatterns += (
    url(r'^upcoming/$', UpcomingView.as_view(), name='upcoming'),
)
