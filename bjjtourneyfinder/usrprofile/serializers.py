from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Profile
        read_only_fields = ('id', 'user')
