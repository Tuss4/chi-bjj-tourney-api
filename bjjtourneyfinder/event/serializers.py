from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    permalink = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'website', 'early_registration_date', 'registration_date',
                  'created', 'updated', 'price', 'early_price', 'author', 'event_type',
                  'start_date', 'end_date', 'permalink')
        read_only_fields = ('id', 'created', 'updated', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        return Event.objects.create(author=user, **validated_data)

    def get_permalink(self, obj):
        return obj.get_permalink


class ModeratorEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        read_only_fields = ('id', 'created', 'updated', 'author')
