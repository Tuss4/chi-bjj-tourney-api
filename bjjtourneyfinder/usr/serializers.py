from rest_framework import serializers
from .models import User
from collections import OrderedDict


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')
        read_only_fields = ('id', 'email')


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate_email(self, value):
        value = value.lower()
        return value

    def to_representation(self, instance):
        obj = OrderedDict()
        user = User.objects.get(email=instance.get('email').lower())
        obj['user'] = UserSerializer(instance=user).data
        obj['token'] = user.auth_token.key
        return obj


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    
