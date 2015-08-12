import arrow
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel


class EventModelMixin(TimeStampedModel, TitleSlugDescriptionModel):
    """
    Abstract base class to prevent code duplication.

    `title` `description`, and `slug` fields inherited from djang-extensions TitleSlugDescriptionModel.

    :start: The start date of the event.
    :end: The end date of the event.
    :title: The title of the event.
    :slug: The url slug of the event.
    :description: The description of the event.
    """
    start = models.DateTimeField(
        verbose_name=_('Start time'),
    )

    end = models.DateTimeField(
        verbose_name=_('End time'),
    )

    def __str__(self):
        return "{title} ({start})".format(title=self.title, start=arrow.get(self.start).format('MMM D, YYYY'))

    def clean(self):
        super().clean()

        if (self.end and self.start) and self.end < self.start:
            # REVIEW: would be nice if this was a part of the field validators
            raise ValidationError("Start time must be earlier than end time.")

    class Meta:
        abstract = True
        ordering = ('start', )
