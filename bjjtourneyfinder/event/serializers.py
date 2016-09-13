from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        read_only_fields = ('id', 'created', 'updated', 'approved', 'author')

    def create(self, validated_data):
        # TODO: might need to just make this a regular serializer.
        return Event.objects.create(**validated_data)
