from rest_framework import serializers
from .models import Event, EventLocation, EVENT_TYPES


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


class EventLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventLocation
        fields = ('id', 'event', 'address', 'city',
                  'state_province', 'country', 'zipcode')


class CreateEventSerializer(serializers.Serializer):

    name = serializers.CharField()
    website = serializers.URLField()
    early_registration_date = serializers.DateField(required=False)
    registration_date = serializers.DateField()
    price = serializers.IntegerField()
    early_price = serializers.IntegerField(required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    event_type = serializers.ChoiceField(choices=EVENT_TYPES)
    address = serializers.CharField()
    city = serializers.CharField()
    state_province = serializers.CharField()
    country = serializers.CharField()
    zipcode = serializers.CharField()

    def create(self, validated_data):
        event_dict = {
            "name": validated_data.get('name'),
            "website": validated_data.get('website'),
            "early_registration_date": validated_data.get('early_registration_date'),
            "registration_date": validated_data.get('registration_date'),
            "price": validated_data.get('price'),
            "early_price": validated_data.get("early_price"),
            "start_date": validated_data.get('start_date'),
            "end_date": validated_data.get('end_date'),
            "event_type": validated_data.get('event_type')
        }
        event = Event.objects.create(**event_dict)
        address_dict = {
            'event': event,
            'address': validated_data.get('address'),
            'city': validated_data.get('city'),
            'state_province': validated_data.get('state_province'),
            'country': validated_data.get('country'),
            'zipcode': validated_data.get('zipcode')
        }
        addr = EventLocation.objects.create(**address_dict)
        return event


class ModeratorEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('approved', )
        read_only_fields = ('id', 'created', 'updated', 'author')
