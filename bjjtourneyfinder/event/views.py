from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .serializers import (
    EventSerializer, ModeratorEventSerializer, CreateEventSerializer)
from .models import Event
from .permissions import EventPermission, ModeratorPermission
from datetime import date


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [EventPermission, ]

    def get_queryset(self):
        return Event.objects.filter(end_date__gte=date.today())

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(approved=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        srlzr = CreateEventSerializer(
            data=request.data, context={'request': request})
        srlzr.is_valid(raise_exception=True)
        srlzr.save()
        return Response(srlzr.data, status=status.HTTP_201_CREATED)


class ModerateEventViewSet(viewsets.ModelViewSet):

    serializer_class = ModeratorEventSerializer
    queryset = Event.objects.filter(approved=False)
    permission_classes = [ModeratorPermission, ]
