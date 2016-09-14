from django.db import models
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    display_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.display_name
