from django.views.generic import ListView
from django.utils.timezone import now, timedelta
from events.models import Event


class UpcomingEventsView(ListView):
    context_object_name = 'occurrences'
    template_name = 'events/upcoming_events.jinja'

    def get_queryset(self):
        qs_kwargs = {
            'start': now(),
            'end': now() + timedelta(40)
        }
        return Event.objects.get_occurrences(**qs_kwargs)
