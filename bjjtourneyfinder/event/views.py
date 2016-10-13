from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .serializers import EventSerializer, ModeratorEventSerializer
from .models import Event
from .permissions import ModeratorPermission


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(approved=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ModerateEventViewSet(viewsets.ModelViewSet):

    serializer_class = ModeratorEventSerializer
    queryset = Event.objects.all()
    permission_classes = [ModeratorPermission, ]
