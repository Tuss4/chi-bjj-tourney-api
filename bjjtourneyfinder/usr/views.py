from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model, authenticate, login


class LoginViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    queryset = get_user_model().objects.all()

    @list_route(methods=['POST'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        user = authenticate(
            username=valid_data.get('email'),
            password=valid_data.get('password'))
        if user is not None:
            login(request, user)
            return Response(serializer.data)
        errors = {"errors": "Invalid credentials."}
        return Response(errors, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewSet(viewsets.GenericViewSet):

    @list_route(methods=['POST'])
    def register(self, request):
        pass
