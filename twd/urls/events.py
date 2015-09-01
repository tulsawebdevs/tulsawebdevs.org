from django.conf.urls import url

from twd import views


urlpatterns = (
    # Event views
    url(r'^$', views.EventsListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$',
        views.EventDetailView.as_view(),
        name='detail'),

    # occurrence views
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.OccurrenceDetailView.as_view(),
        name='occurrence_detail'),
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/update/$',
        views.OccurrenceUpdateView.as_view(),
        name='occurrence_update'),
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/delete/$',
        views.OccurrenceDeleteView.as_view(),
        name='occurrence_delete'),
    url(r'upcoming$', views.UpcomingOccurrencesView.as_view(), name='upcoming'),
)
