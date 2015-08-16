# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.template import engines
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from recurrence.fields import RecurrenceField

from .mixins import EventModelMixin
from ..managers import EventModelManager
from ..utils import OccurrenceReplacer


# TODO: occurrence name pattern generator from *_templates (eg. January Meeting)
class Event(EventModelMixin):
    """
    Hold the information about an event in the calendar.

    inherits from EventModelMixin which defines basic event metadata

    :category: FK to the ``EventCategory`` this event belongs to.
    # :rule: FK to the definition of the recurrence of an event.
    # :end_recurring_period: The possible end of the recurring definition.
    # :title: The title of the event.
    """

    category = models.ForeignKey(
        'EventCategory',
        verbose_name=_('Category'),
        related_name='events',
        null=True, blank=True,
    )

    title_template = models.TextField(
        null=True, blank=True,
        help_text="jinja2 template used to render occurrence titles"
    )

    description_template = models.TextField(
        null=True, blank=True,
        help_text="jinja2 template used to render occurrence descriptions"
    )

    recurrences = RecurrenceField()

    # TODO: Enable at some point
    # end_recurring_period = models.DateTimeField(
    #     verbose_name=_('End of recurring'),
    #     blank=True, null=True,
    # )

    objects = EventModelManager()

    def _get_date_generator(self, start, end):
        """Return a generator to create the start dates for occurrences."""
        date = self.recurrences.after(start)
        while end and date <= end or not(end):
            yield date
            date = self.recurrences.after(date)

    def _get_occurrence_generator(self, start, end):
        """Compute all occurrences for this event from start to end."""
        # get length of the event
        length = self.end - self.start

        # if the end of the recurring period is before the end arg passed
        # the end of the recurring period should be the new end
        # TODO: Enable at some point
        # if self.end_recurring_period and end and (
        #         self.end_recurring_period < end):
        #     end = self.end_recurring_period
        # making start date generator
        occurrence_start_generator = self._get_date_generator(start - length, end)

        # chosing the first item from the generator to initiate
        occurrence_start = next(occurrence_start_generator)
        while not end or (end and occurrence_start <= end):
            occurrence_end = occurrence_start + length
            yield Occurrence.from_event(self, occurrence_start, occurrence_end, use_templates=True)
            occurrence_start = next(occurrence_start_generator)

    def get_occurrences(self, start, end=None):
        """Return a generator that outputs occurrences in the given range"""
        # get persisted occurrences from the database in that range
        persisted_occurrences = self.occurrences.filter(start__gte=start, end__lte=end)
        occurrence_replacer = OccurrenceReplacer(persisted_occurrences)
        occurrence_generator = self._get_occurrence_generator(start, end)
        additional_occurrences = occurrence_replacer.get_additional_occurrences(start, end)

        occurrence = next(occurrence_generator)
        while not end or (occurrence.start < end or any(additional_occurrences)):
            if occurrence_replacer.has_occurrence(occurrence):
                persisted_occ = occurrence_replacer.get_occurrence(occurrence)
                if end and persisted_occ.start < end and persisted_occ >= start:
                    estimated_occurrence = persisted_occ
            else:
                estimated_occurrence = occurrence

            if any(additional_occurrences) and estimated_occurrence.start == additional_occurrences[0].start:
                final_occurrence = additional_occurrences.pop(0)
            else:
                final_occurrence = estimated_occurrence

            if not final_occurrence.cancelled:
                yield final_occurrence
            occurrence = next(occurrence_generator)


class EventCategory(MPTTModel):
    """
    The category of an event.

    :name: The name of the category.
    :slug: The slug of the category.
    :parent: Allows you to create hierarchies of event categories.

    """
    name = models.CharField(
        _('Name'),
        max_length=255
    )

    slug = AutoSlugField(_('Slug'), populate_from='name')

    parent = TreeForeignKey(
        'self',
        verbose_name=_('Parent'),
        null=True, blank=True,
        related_name='children',
        db_index=True
    )

    order = models.PositiveSmallIntegerField(blank=False, default=0)

    objects = TreeManager()

    class Meta:
        ordering = ('lft',)

    class MPTTMeta:
        order_insertion_by = ('order',)

    def __str__(self):
        return self.name


class Occurrence(EventModelMixin):
    """
    Needed if one occurrence of an event has slightly different settings than all other.

    :event: FK to the ``Event`` this ``Occurrence`` belongs to.
    :original_start: The original start of the related ``Event``.
    :original_end: The original end of the related ``Event``.
    :cancelled: True or false of the occurrence's cancellation status.
    :title: The title of the event.

    """
    event = models.ForeignKey(
        'Event',
        verbose_name=_('Event'),
        related_name='occurrences'
    )

    original_start = models.DateTimeField(
        _('Original start')
    )

    original_end = models.DateTimeField(
        _('Original end')
    )

    cancelled = models.BooleanField(
        _('Cancelled'),
        default=False,
    )

    @classmethod
    def from_event(cls, event, occurrence_start, occurrence_end=None, use_templates=False):
        """Return a new occurrence with a relation to the parent event"""
        assert isinstance(occurrence_start, datetime)

        if not occurrence_end:
            occurrence_end = occurrence_start + (event.end - event.start)

        occurrence = cls(
            event=event, start=occurrence_start, end=occurrence_end,
            original_start=occurrence_start, original_end=occurrence_end,
            location=event.location)

        if use_templates:
            occurrence.update_template_title()
            occurrence.update_template_description()

        return occurrence

    @property
    def category(self):
        return self.event.category


    def get_template_context(self):
        return {
            'occ': self,
            'event': self.event
        }

    def set_template(self, field, template_string=None):
        assert isinstance(field, str)
        if not template_string:
            template_string = getattr(self, 'default_{}_template'.format(field))
        engine = engines['jinja2']
        template = engine.from_string(template_string)
        rendered = template.render(self.get_template_context())
        setattr(self, field, rendered)

    default_title_template = "{{ occ.start|date('M') }} - {{event.title}}"

    def update_template_title(self):
        self.set_template('title', self.event.title_template)

    default_description_template = "{{ event.description }}"

    def update_template_description(self):
        self.set_template('description', self.event.description_template)
