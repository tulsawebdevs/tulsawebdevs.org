from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from events.models import Location


class LocationAdmin(OSMGeoAdmin):
    fields = ('name', 'address', 'location', 'meta')
    list_display = ('name', 'address', 'location',)
    default_zoom = 8


admin.site.register(Location, LocationAdmin)
