from rest_framework.serializers import Field


class StraightJSONField(Field):

    def to_representation(self, obj):
        return obj
