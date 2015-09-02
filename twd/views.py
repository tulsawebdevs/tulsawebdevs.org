import arrow
from django.utils.timezone import datetime, now
from django.views.generic import TemplateView

from events import views as base_views

from events.models import Event


class UpcomingOccurrencesView(base_views.UpcomingOccurrencesViewBase):
    template_name = 'events/upcoming_events.jinja'


class EventsListView(base_views.EventsListViewBase):
    template_name = 'events/events_list.jinja'


class HomePageView(TemplateView):
    template_name = 'twd/home.jinja'

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'get_upcoming_events': self.get_upcoming_events
        })
        return context

    def get_upcoming_events(self):
        """Grab all occurrences from a week ago to a month in the future"""
        start_from = arrow.utcnow().replace(weeks=-1).naive
        until = arrow.utcnow().replace(months=1).naive
        return Event.objects.get_occurrences(start_from, until)


# Event/Occurrence Views
class EventDetailView(base_views.EventDetailViewBase):
    template_name = 'events/event_detail.jinja'


class OccurrenceDetailView(base_views.OccurrenceDetailViewBase):
    template_name = 'events/occurrence_detail.jinja'


class OccurrenceUpdateView(base_views.OccurrenceUpdateViewBase):
    template_name = 'events/occurrence_update.jinja'


class OccurrenceDeleteView(base_views.OccurrenceDeleteViewBase):
    template_name = 'events/occurrence_delete.jinja'
