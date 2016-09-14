from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CreateEventSerializer, EventSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        return EventSerializer

    def get_queryset(self):
        return Event.objects.filter(approved=True)
