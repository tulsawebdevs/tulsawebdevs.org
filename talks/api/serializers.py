# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Speaker, Talk


class SpeakerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'slug', 'talks',)


class TalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talk
        fields = ('id', 'title', 'description', 'speaker', 'accepted',)
