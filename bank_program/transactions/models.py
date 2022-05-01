import uuid

from django.db import models

from programs.models import Program


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.TextField()
    currency = models.TextField(max_length=3)
    program = models.TextField()
    bank = models.TextField()
    is_eligible = models.BooleanField(default=True)

