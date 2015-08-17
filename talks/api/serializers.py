# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Speaker, Talk


class SpeakerSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'slug', 'talks',)

    def get_name(self, obj):
        return obj.get_name()


class TalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talk
        fields = ('id', 'title', 'description', 'speaker', 'accepted',)
