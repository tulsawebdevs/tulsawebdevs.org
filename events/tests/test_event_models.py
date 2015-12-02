# -*- coding: utf-8 -*-
"""Tests for events models."""
from datetime import datetime

from django.test import TestCase
from model_mommy import mommy
import fudge

from events.models import Occurrence
import events.models.events as events_models


class TestEventModel(TestCase):

    def setUp(self):
        # main start date
        self.main_start = datetime(2015, 1, 1, 18, 00)
        self.main_end = datetime(2015, 1, 1, 20, 00)

        # Create an event with a recurrence of monthly on the 3rd monday.
        self.event = mommy.make(
            'events.Event', start=self.main_start, end=self.main_end, recurrences='RRULE:FREQ=MONTHLY;BYDAY=3MO')

        self.first_occ = Occurrence.from_event(self.event, datetime(2015, 1, 18, 16, 00))
        self.first_occ.save()
        self.second_occ = Occurrence.from_event(self.event, datetime(2015, 2, 18, 16, 00))
        self.second_occ.save()

    # def test_get_occurrences_none_persisted(self):
    #     until = datetime(2015, 3, 2, 16, 00)
    #     occurrences = self.event.get_occurrences(self.main_start, until)
    #     self.assertQuerysetEqual(occurrences, [])
    #
    # def test_get_occurrences_in_range(self):
    #     first_occ = Occurrence.from_event(self.event, datetime(2015, 1, 3, 16, 00))
    #     first_occ.save()
    #     second_occ = Occurrence.from_event(self.event, datetime(2015, 2, 6, 16, 00))
    #     second_occ.save()
    #     # Shouldn't show up in the results
    #     outofrange_occ = Occurrence.from_event(self.event, datetime(2025, 2, 6, 16, 00))
    #     outofrange_occ.save()
    #
    #     until = datetime(2015, 3, 2, 16, 00)
    #     occurrences = self.event.get_occurrences(self.main_start, until)
    #
    #     self.assertQuerysetEqual([oc for oc in occurrences], map(repr, [first_occ, second_occ]))
    #
    # @fudge.patch(
    #     'events.models.events.Event.occurrences',
    #     'events.models.events.Event._get_occurrence_generator',
    #     'events.models.events.OccurrenceReplacer')
    # def test_get_occurrences_none_returned(
    #         self,
    #         mock_occurrences,
    #         mock_get_occurrence_generator,
    #         mock_OccurrenceReplater):
    #
    #     occ_start = datetime(2015, 1, 1)
    #     occ_end = datetime(2015, 3, 1)
    #
    #     # Getting persisted occurrences
    #     mock_persisted_occ = fudge.Fake('persisted_occurrences')
    #     mock_occurrences.is_a_stub()
    #     (mock_occurrences.expects('filter').with_args(start__gte=occ_start, end__lte=occ_end)
    #         .returns(mock_persisted_occ))
    #
    #     # OccurrenceReplacer init and methods
    #     mock_occurrence_replacer_instance = fudge.Fake('occurrence_replacer').is_a_stub()
    #     mock_occurrence_replacer_instance.expects('get_additional_occurrences').with_args(occ_start, occ_end)
    #     (mock_OccurrenceReplater.expects_call().with_args(mock_persisted_occ)
    #         .returns(mock_occurrence_replacer_instance))
    #
    #     # _get_occurrence_generator is called and returns
    #     from unittest.mock import MagicMock
    #     mock_occurrence_generator = MagicMock()
    #     mock_occurrence_generator.iter.return_value.__iter__.return_value = iter([self.first_occ, self.second_occ])
    #     (mock_get_occurrence_generator.expects_call().with_args(occ_start, occ_end)
    #         .returns(mock_occurrence_generator))
    #
    #     occurrences = self.event.get_occurrences(occ_start, occ_end)
    #
    #     self.assertQuerysetEqual([oc for oc in occurrences], map(repr, [self.first_occ, self.second_occ]))

    # def test_get_occurrences_in_range_with_non_persisted(self):
    #     pass


class TestOccurenceModel(TestCase):

    def setUp(self):
        self.main_start = datetime(2015, 1, 1, 12, 00)
        self.main_end = datetime(2015, 1, 1, 16, 00)

        self.event = mommy.make(
            'events.Event',
            start=self.main_start, end=self.main_end,
            title_template='jinja title template',
            description_template='jinja description template',
            recurrences='RRULE:FREQ=MONTHLY;BYDAY=3MO')

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
        self.assertEqual(occ.location, self.event.location)

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
        self.assertEqual(occ.location, self.event.location)

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
        self.assertEqual(occ.location, self.event.location)

    def test_get_template_context(self):
        # Create occurrence
        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)

        context = occ.get_template_context()

        self.assertEqual(context, {
            'occurrence': occ,
            'event': self.event
        })

    @fudge.patch('events.models.Occurrence.get_template_context')
    def test_set_template(self, mock_get_template_context):
        # Create occurrence
        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)

        # getting context returns mock context string
        mock_get_template_context.is_callable().returns('context')

        # Jinja template engine is selected and is passed the template string, render is called on the template
        mock_jinja_engine = fudge.Fake()
        mock_template = mock_jinja_engine.expects('from_string').with_args('jinja template').returns_fake()
        mock_template.expects('render').with_args('context').returns('rendered context')

        mock_engines = {
            'jinja2': mock_jinja_engine
        }

        patched_engines = fudge.patch_object(events_models, 'engines', mock_engines)

        # call set_template
        occ.set_template('a_field', 'jinja template')

        self.assertEqual(occ.a_field, 'rendered context')

        patched_engines.restore()

        pass

    @fudge.patch('events.models.Occurrence.get_template_context')
    def test_set_template_no_template_string(self, mock_get_template_context):
        # Create occurrence
        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)

        # getting context returns mock context string
        mock_get_template_context.is_callable().returns('context')

        # Expact the default template to be set on the occurrence
        occ.default_a_field_template = 'default jinja template'

        # Jinja template engine is selected and is passed the template string, render is called on the template
        mock_jinja_engine = fudge.Fake()
        mock_template = mock_jinja_engine.expects('from_string').with_args('default jinja template').returns_fake()
        mock_template.expects('render').with_args('context').returns('rendered context')

        mock_engines = {
            'jinja2': mock_jinja_engine
        }

        patched_engines = fudge.patch_object(events_models, 'engines', mock_engines)

        # call set_template
        occ.set_template('a_field')

        self.assertEqual(occ.a_field, 'rendered context')

        patched_engines.restore()

    @fudge.patch('events.models.Occurrence.set_template')
    def test_update_template_title(self, mock_set_template):
        mock_set_template.is_callable().with_args('title', 'jinja title template')

        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)

        occ.update_template_title()

    @fudge.patch('events.models.Occurrence.set_template')
    def test_update_template_description(self, mock_set_template):
        mock_set_template.is_callable().with_args('description', 'jinja description template')

        occurrence_start = datetime(2015, 2, 1, 12, 00)
        occurrence_end = datetime(2015, 2, 1, 18, 00)
        occ = Occurrence.from_event(self.event, occurrence_start, occurrence_end)

        occ.update_template_description()
