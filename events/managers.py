# -*- coding: utf-8 -*-
from datetime import timedelta

from django.db import models
from django.db.models import Q


class EventModelManager(models.Manager):
    """Custom manager for the ``Event`` model class."""

    def get_occurrences(self, start, end, category=None):
        """Return a list of events and occurrences for the given period."""
        # we always want the time of start and end to be at 00:00
        start = start.replace(minute=0, hour=0)
        end = end.replace(minute=0, hour=0)
        # if we recieve the date of one day as start and end, we need to set
        # end one day forward
        if start == end:
            end = start + timedelta(days=1)
        # retrieving relevant events
        # TODO currently for events with a rule, I can't properly find out when
        # the last occurrence of the event ends, or find a way to filter that,
        # so I'm still fetching **all** events before this period, that have a
        # end_recurring_period.
        # For events without a rule, I fetch only the relevant ones.

        qs = self.get_queryset().filter(start__lt=end)

        if category:
            qs = qs.filter(Q(category=category) | Q(category__parent=category))
        else:
            qs = qs.filter(start__lt=end)
        # get all occurrences for those events that don't already have a
        # persistent match and that lie in this period.
        all_occurrences = []
        for event in qs:
            all_occurrences.extend(event.get_occurrences(start, end))

        # sort and return
        return sorted(all_occurrences, key=lambda x: x.start)
