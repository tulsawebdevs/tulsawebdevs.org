# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from django_extensions.db.fields import AutoSlugField


class Speaker(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=60, blank=True, null=True, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_('User'), blank=True, null=True)
    slug = AutoSlugField(_('Name Slug'), populate_from='name')

    def __str__(self):
        return "{name}".format(name=self.name or self.user)


class Talk(TimeStampedModel, TitleSlugDescriptionModel):
    speaker = models.ForeignKey(Speaker, blank=True, null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "{title}".format(title=self.title)
