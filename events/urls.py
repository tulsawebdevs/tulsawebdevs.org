from django.conf.urls import url

from events.views import UpcomingEventsView


urlpatterns = (
    url(r'upcoming$', UpcomingEventsView.as_view(), name='upcoming'),
)
