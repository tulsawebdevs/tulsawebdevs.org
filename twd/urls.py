from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from .views import HomePageView


urlpatterns = [
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
