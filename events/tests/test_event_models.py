# -*- coding: utf-8 -*-
"""Tests for events models."""
from datetime import datetime

from django.test import TestCase
from model_mommy import mommy
import fudge

from events.models import Occurrence


class TestEventModel(TestCase):

    def setUp(self):
        # main start date
        self.main_start = datetime(2015, 1, 1, 12, 00)
        self.main_end = datetime(2015, 1, 1, 16, 00)

        self.event = mommy.make(
            'events.Event', start=self.main_start, end=self.main_end, recurrences='RRULE:FREQ=MONTHLY;BYDAY=3MO')

    def test_get_occurrences_none_persisted(self):
        until = datetime(2015, 3, 2, 16, 00)
        occurrences = self.event.get_occurrences(self.main_start, until)
        self.assertQuerysetEqual(occurrences, [])

    def test_get_occurrences_in_range(self):
        first_occ = Occurrence.from_event(self.event, datetime(2015, 1, 3, 16, 00))
        first_occ.save()
        second_occ = Occurrence.from_event(self.event, datetime(2015, 2, 6, 16, 00))
        second_occ.save()
        # Shouldn't show up in the results
        outofrange_occ = Occurrence.from_event(self.event, datetime(2025, 2, 6, 16, 00))
        outofrange_occ.save()

        until = datetime(2015, 3, 2, 16, 00)
        occurrences = self.event.get_occurrences(self.main_start, until)

        import ipdb; ipdb.set_trace()
        self.assertQuerysetEqual([oc for oc in occurrences], map(repr, [first_occ, second_occ]))

    def test_get_occurrences_in_range_with_non_persisted(self):
        pass


class TestOccurenceModel(TestCase):

    def setUp(self):
        self.main_start = datetime(2015, 1, 1, 12, 00)
        self.main_end = datetime(2015, 1, 1, 16, 00)

        self.event = mommy.make(
            'events.Event', start=self.main_start, end=self.main_end, recurrences='RRULE:FREQ=MONTHLY;BYDAY=3MO')

    def test_from_event_no_occurrence_start(self):
        with self.assertRaises(TypeError):
            Occurrence.from_event(self.event)

    def test_from_event_wrong_occurrence_start(self):
        with self.assertRaises(AssertionError):
            Occurrence.from_event(self.event, 'string date')

    @fudge.patch(
        'events.models.Occurrence.update_template_title',
        'events.models.Occurrence.update_template_description')
    def test_from_event_no_occurrence_end_created(self, mock_title, mock_description):
        # provised mocked template functions as we expect them not to be called
        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occ = Occurrence.from_event(self.event, occurrence_start)
        self.assertEqual(occ.start, occurrence_start)
        self.assertEqual(occ.original_start, occurrence_start)
        orig_end = datetime(2015, 2, 1, 16, 00)
        self.assertEqual(occ.end, orig_end)
        self.assertEqual(occ.original_end, orig_end)
        self.assertEqual(occ.event, self.event)

    @fudge.patch(
        'events.models.Occurrence.update_template_title',
        'events.models.Occurrence.update_template_description')
    def test_from_event_occurrence_created(self, mock_title, mock_description):
        # An alternative end time is provided
        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)
        self.assertEqual(occ.start, occurrence_start)
        self.assertEqual(occ.original_start, occurrence_start)
        orig_end = datetime(2015, 2, 1, 18, 00)
        self.assertEqual(occ.end, orig_end)
        self.assertEqual(occ.original_end, orig_end)
        self.assertEqual(occ.event, self.event)

    @fudge.patch(
        'events.models.Occurrence.update_template_title',
        'events.models.Occurrence.update_template_description')
    def test_from_event_occurrence_use_templates_enabled(self, mock_title, mock_description):
        # Check to make sure they are called
        mock_title.expects_call()
        mock_description.expects_call()

        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, use_templates=True)
        self.assertEqual(occ.start, occurrence_start)
        self.assertEqual(occ.original_start, occurrence_start)
        orig_end = datetime(2015, 2, 1, 16, 00)
        self.assertEqual(occ.end, orig_end)
        self.assertEqual(occ.event, self.event)
