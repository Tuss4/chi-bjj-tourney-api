from django.db import models


class Event(models.Model):

    name = models.CharField(max_length=100, unique=True)
    website = models.URLField()
    early_registration = models.DateField(null=True)
    reg_registration = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
