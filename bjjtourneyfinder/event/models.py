from django.db import models


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
    author = models.ForeignKey('usr.Profile', related_name='event')

    def __str__(self):
        return self.name
