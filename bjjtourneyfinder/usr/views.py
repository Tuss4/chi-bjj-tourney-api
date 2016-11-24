from rest_framework import viewsets, status, views
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import (
    LoginSerializer, RegisterSerializer, ForgotPasswordSerializer, PasswordResetSerializer)
from django.contrib.auth import get_user_model, authenticate, login
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from usrtoken.models import ConfirmationToken, PasswordToken
from notification.email import TourneyEmail


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
    emailer = TourneyEmail()

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        try:
            user = get_user_model().objects.create_user(**valid_data)
            ctoken = ConfirmationToken.objects.create(user=user)
            self.emailer.send_confirmation_email(user, ctoken)
            resp = {'id': user.pk, 'token': user.auth_token.key}
            return Response(resp, status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ConfirmationView(views.APIView):

    permission_classes = (AllowAny, )

    def get(self, request, token=None):
        ctoken = get_object_or_404(ConfirmationToken, token=token)
        if not ctoken.is_expired:
            ctoken.user.is_active = True
            ctoken.user.save()
            ctoken.delete()
            resp = {'confirmed': True}
            return Response(resp, status=status.HTTP_200_OK)
        ctoken.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(views.APIView):

    permission_classes = (AllowAny, )
    serializer_class = ForgotPasswordSerializer
    emailer = TourneyEmail()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.get(email=serializer.validated_data.get('email'))
        ptoken = PasswordToken.objects.create(user=user)
        self.emailer.send_password_reset(user, ptoken)
        return Response(status=status.HTTP_200_OK)


class PasswordResetView(views.APIView):

    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer

    def post(self, request, token=None):
        ptoken = get_object_or_404(PasswordToken, token=token)
        serializer = self.serializer_class(data=request.data)
        if not ptoken.is_expired:
            serializer.is_valid(raise_exception=True)
            newp = serializer.validated_data.get('new_password')
            ptoken.user.set_password(newp)
            ptoken.user.save()
            ptoken.delete()
            return Response(status=status.HTTP_200_OK)
        ptoken.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
