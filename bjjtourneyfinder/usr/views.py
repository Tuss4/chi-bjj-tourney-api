from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import get_user_model, authenticate, login
from django.db import IntegrityError


class LoginViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    queryset = get_user_model().objects.all()

    @list_route(methods=['POST'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        try:
            user = get_user_model().objects.create_user(**valid_data)
            # TODO: send activation email.
            resp = {'id': user.pk, 'token': user.auth_token.key}
            return Response(resp, status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
