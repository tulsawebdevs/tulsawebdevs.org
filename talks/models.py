# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from django_extensions.db.fields import AutoSlugField


class Speaker(TimeStampedModel):
    """
    Hold data related to those dedicated few who decide to give talks.

    :name: Name of the speaker
    :user: Optional user to relate the speaker to
    :slug: Slug used in urls when looking up a speaker
    """

    name = models.CharField(
        _('Name'),
        max_length=60,
        blank=False, null=True, unique=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        blank=True, null=True, unique=True)

    slug = AutoSlugField(_('Slug'), populate_from='name')

    def get_name(self):
        """Get the set name of the speaker or the associated user's full name."""
        return self.name or (self.user and self.user.get_full_name())

    def __str__(self):
        return self.get_name()

    @staticmethod
    def update_speaker_name_on_creation(sender, instance, created, **kwargs):
        "Signal callback to hangle updating the speaker name only when created"
        if created and instance.user:
            instance.name = instance.user.get_full_name()
            instance.save()

post_save.connect(Speaker.update_speaker_name_on_creation, sender=Speaker, dispatch_uid="set_speaker_name")


class Talk(TimeStampedModel, TitleSlugDescriptionModel):
    """
    Store information about a talk that may ot may not be given.

    `title` `description`, and `slug` fields inherited from djang-extensions
    TitleSlugDescriptionModel.

    :speaker: designated speaker if not yet assigned.
    :accepted: Whether or not this talk has been accepted.
    """

    speaker = models.ForeignKey(
        Speaker, related_name='talks',
        blank=True, null=True,)

    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "{title}".format(title=self.title)
