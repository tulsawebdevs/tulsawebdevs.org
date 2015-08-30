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
        self.model = mommy.make(Speaker, name='Set Name')

    # def test_attr(self):
    #     pass

    def test_mro(self):
        self.assertIsInstance(self.model, TimeStampedModel)

    def test_get_name_with_user(self):
        self.model.user = mommy.make(settings.AUTH_USER_MODEL, first_name='Full', last_name='Name')
        self.assertEqual(self.model.get_name(), 'Set Name')

    def test_get_name_without_name(self):
        self.model.user = mommy.make(settings.AUTH_USER_MODEL, first_name='Full', last_name='Name')
        self.model.name = None
        self.assertEqual(self.model.get_name(), 'Full Name')

    def test_str(self):
        mock_full_name = fudge.Fake('Speaker.get_name()').is_callable().returns('Got Name')
        with fudge.patched_context(Speaker, 'get_name', mock_full_name):
            self.assertEqual(str(self.model), 'Got Name')

    def test_post_save_name_creation(self):
        speaker = mommy.prepare(Speaker)
        mock_update_speaker_name = fudge.Fake(
            'Speaker.update_speaker_name_on_creation').expects_call().with_args(
                Speaker, speaker, True)
        with fudge.patched_context(
                Speaker, 'update_speaker_name_on_creation', mock_update_speaker_name):
            speaker.save()

    def test_update_speaker_name_on_creation_has_user(self):
        speaker = mommy.prepare(Speaker, name='wut', user__first_name='Set', user__last_name='Name')
        speaker.user.save()
        Speaker.update_speaker_name_on_creation(Speaker, speaker, True)
        # Name is set from user on creation
        self.assertEqual(speaker.name, 'Set Name')

    def test_update_speaker_name_on_creation_has_user_not_created(self):
        speaker = mommy.prepare(Speaker, name='wut', user__first_name='Set', user__last_name='Name')
        speaker.user.save()
        Speaker.update_speaker_name_on_creation(Speaker, speaker, False)
        # Name is set from user on creation
        self.assertEqual(speaker.name, 'wut')

    def test_update_speaker_name_on_creation_no_user(self):
        speaker = mommy.prepare(Speaker, name='wut', user=None)
        Speaker.update_speaker_name_on_creation(Speaker, speaker, True)
        # Name is set from user on creation
        self.assertEqual(speaker.name, 'wut')


class TestTalkModel(TestCase):

    def setUp(self):
        self.model = mommy.make(Talk, title='This talk is going to rock')

    def test_str(self):
        self.assertEqual(str(self.model), 'This talk is going to rock')
