from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


class GenericToken(models.Model):

    token = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    expires = models.DateTimeField(
        default=timezone.now() + timedelta(days=settings.EXPIRY))

    @property
    def is_expired(self):
        return self.expires <= timezone.now()

    class Meta:
        abstract = True


class ConfirmationToken(GenericToken):

    pass


class PasswordToken(GenericToken):

    pass
