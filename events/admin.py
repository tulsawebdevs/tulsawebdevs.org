"""Admin views for the models of the ``events`` app."""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from events.models import (
    Location,
    Event,
    EventCategory,
    Occurrence,
)


class LocationAdmin(OSMGeoAdmin):
    fields = ('name', 'address', 'location', 'meta')
    list_display = ('name', 'address', 'location',)
    default_zoom = 8


class EventAdmin(admin.ModelAdmin):
    """Custom admin for the ``Event`` model."""
    model = Event
    fields = (
        'title', 'start', 'end', 'description', 'category',
        'recurrences', )
    list_display = (
        'title', 'start', 'end', 'category', )
    search_fields = ('title', 'description', )
    date_hierarchy = 'start'
    list_filter = ('category', )


class EventCategoryAdmin(admin.ModelAdmin):
    """Custom admin to display a small colored square."""
    model = EventCategory
    list_display = ('name',)
    # list_editable = ('color',)


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Occurrence)
