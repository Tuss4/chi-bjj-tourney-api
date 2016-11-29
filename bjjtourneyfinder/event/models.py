from django.db import models
from django.conf import settings
from django.utils import timezone


TOURNAMENT = 'T'
SEMINAR = 'S'

EVENT_TYPES = (
    (TOURNAMENT, 'Tournament'),
    (SEMINAR, 'Seminar')
)


class Event(models.Model):

    name = models.CharField(max_length=100, unique=True)
    website = models.URLField()
    early_registration_date = models.DateField(null=True)
    registration_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    early_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event')
    event_type = models.CharField(max_length=1, choices=EVENT_TYPES, default=TOURNAMENT)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    @property
    def get_permalink(self):
        return "/#/event/{}".format(self.id)
