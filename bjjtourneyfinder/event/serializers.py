from rest_framework import serializers
from .models import Event


class CreateEventSerializer(serializers.Serializer):

    website = serializers.URLField()
    early_registration_date = serializers.DateField(required=False)
    registration_date = serializers.DateField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    early_price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)


    def create(self, validated_data):
        user = self.request.user.profile
        return Event.objects.create(author=user, **validated_data)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        read_only_fields = ('id', 'created', 'updated', 'approved', 'author')
