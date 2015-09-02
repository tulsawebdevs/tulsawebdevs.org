from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.utils.timezone import datetime, now, timedelta

from events.models import Event, Occurrence


class UpcomingOccurrencesViewBase(ListView):
    context_object_name = 'occurrences'

    def get_queryset(self):
        qs_kwargs = {
            'start': now(),
            'end': now() + timedelta(40)
        }
        return Event.objects.get_occurrences(**qs_kwargs)


class EventsListViewBase(ListView):
    context_object_name = 'events'
    model = Event


class EventMixin(object):
    model = Event
    context_object_name = 'event'


class EventDetailViewBase(EventMixin, DetailView):
    """View to return information of an event."""


class EventCreateViewBase(EventMixin, CreateView):
    pass


class EventUpdateViewBase(EventMixin, UpdateView):
    pass


class EventDeleteViewBase(EventMixin, DeleteView):
    pass


class OccurrenceViewMixin(object):
    """Mixin to avoid repeating code for the Occurrence view classes."""
    # form_class = OccurrenceForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.event = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404
        year = int(kwargs.get('year'))
        month = int(kwargs.get('month'))
        day = int(kwargs.get('day'))
        try:
            date = datetime(year, month, day)
        except (TypeError, ValueError):
            raise Http404('not a valid occurrence date')
        # this should retrieve the one single occurrence, that has a
        # matching start date
        try:
            occ = Occurrence.objects.get(
                start__year=year, start__month=month, start__day=day)
        except Occurrence.DoesNotExist:
            # TODO: Change start date to equal that being searched for so we
            # find it quicker with less generator iteration
            occ_gen = self.event.get_occurrences(date)
            occ = next(occ_gen)
            while occ.start.date() < date.date():
                occ = next(occ_gen)
        if occ.start.date() == date.date():
            self.occurrence = occ
        else:
            raise Http404('no found occurrence for this date')
        self.object = occ
        return super(OccurrenceViewMixin, self).dispatch(
            request, *args, **kwargs)

    def get_object(self):
        return self.object

    def get_form_kwargs(self):
        kwargs = super(OccurrenceViewMixin, self).get_form_kwargs()
        kwargs.update({'initial': model_to_dict(self.object)})
        return kwargs


class OccurrenceDeleteViewBase(OccurrenceViewMixin, DeleteView):
    """View to delete an occurrence of an event."""
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        decision = self.request.POST.get('decision')
        self.object.delete_period(decision)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, object):
        ctx = super(OccurrenceDeleteViewBase, self).get_context_data()
        ctx.update({
            # 'decisions': OCCURRENCE_DECISIONS,
            'object': self.object
        })
        return ctx

    def get_success_url(self):
        return reverse('events:current_month')


class OccurrenceDetailViewBase(OccurrenceViewMixin, DetailView):
    """View to show information of an occurrence of an event."""
    pass


class OccurrenceUpdateViewBase(OccurrenceViewMixin, UpdateView):
    """View to edit an occurrence of an event."""
    pass
