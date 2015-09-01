from django.views.generic import TemplateView

from events import views as base_views


class UpcomingOccurrencesView(base_views.UpcomingOccurrencesViewBase):
    template_name = 'events/upcoming_events.jinja'


class EventsListView(base_views.EventsListViewBase):
    template_name = 'events/events_list.jinja'


class HomePageView(TemplateView):
    template_name = 'twd/home.jinja'


# Event/Occurrence Views
class EventDetailView(base_views.EventDetailViewBase):
    template_name = 'events/event_detail.jinja'


class OccurrenceDetailView(base_views.OccurrenceDetailViewBase):
    template_name = 'events/occurrence_detail.jinja'


class OccurrenceUpdateView(base_views.OccurrenceUpdateViewBase):
    template_name = 'events/occurrence_update.jinja'


class OccurrenceDeleteView(base_views.OccurrenceDeleteViewBase):
    template_name = 'events/occurrence_delete.jinja'
