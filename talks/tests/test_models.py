# -*- coding: utf-8 -*-
"""Tests for events models."""
from django.conf import settings
from django.test import TestCase
from django_extensions.db.models import TimeStampedModel
from model_mommy import mommy
import fudge

from talks.models import Speaker, Talk


class TestSpeakerModel(TestCase):

    def setUp(self):
        self.model = mommy.make(Speaker, name="Set Name")

    # def test_attr(self):
    #     pass

    def test_mro(self):
        self.assertIsInstance(self.model, TimeStampedModel)

    def test_get_name_with_user(self):
        self.model.user = mommy.make(settings.AUTH_USER_MODEL, first_name='Full', last_name='Name')
        self.assertEqual(self.model.get_name(), 'Full Name')

    def test_get_name_without_user(self):
        self.assertIsNone(self.model.user)
        self.assertEqual(self.model.get_name(), 'Set Name')

    def test_str(self):
        mock_full_name = fudge.Fake('Speaker.get_name()').is_callable().returns('Full Name Property')
        with fudge.patched_context(Speaker, 'get_name', mock_full_name):
            self.assertEqual(str(self.model), 'Full Name Property')


class TestTalkModel(TestCase):

    def setUp(self):
        self.model = mommy.make(Talk, title="This talk is going to rock")

    def test_str(self):
        self.assertEqual(str(self.model), "This talk is going to rock")
