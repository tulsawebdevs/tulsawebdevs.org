# -*- coding: utf-8 -*-
"""Tests for events models."""
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from model_mommy import mommy

from events.models.mixins import EventModelMixin


class TestEventModelMixin(TestCase):
    def setUp(self):
        self.model = mommy.prepare(EventModelMixin, title='Event Title', start=datetime(2015, 8, 1))

    def test_attr(self):
        self.assertEqual(str(self.model), 'Event Title (Aug 1, 2015)')

    def test_Meta(self):
        self.assertEqual(EventModelMixin._meta.abstract, True)
        self.assertEqual(EventModelMixin._meta.ordering, ('start',))

    def test_mro(self):
        self.assertIsInstance(self.model, TimeStampedModel)
        self.assertIsInstance(self.model, TitleSlugDescriptionModel)

    def test_clean_end_date_sooner_than_start(self):

        self.model.start = datetime(2015, 1, 10)
        self.model.end = datetime(2015, 1, 1)

        with self.assertRaises(ValidationError) as cm:
            self.model.clean()

        self.assertEqual(cm.exception.message, "Start time must be earlier than end time.")

    def test_clean_end_date_later_than_start(self):
        self.model.start = datetime(2015, 1, 10)
        self.model.end = datetime(2015, 1, 13)

        self.model.clean()
