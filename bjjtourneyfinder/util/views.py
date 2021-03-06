from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class PingView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return Response(dict(ping="pong"), status=status.HTTP_200_OK)
