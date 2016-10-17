from rest_framework import serializers
from collections import OrderedDict
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email')
        read_only_fields = ('id', 'email')


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate_email(self, value):
        value = value.lower()
        return value

    def validate(self, data):
        user = authenticate(username=data.get('email'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        data['token'] = user.auth_token.key
        data['user'] = UserSerializer(user).data
        return data


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
