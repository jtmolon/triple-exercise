import uuid

from django.db import models

from general import models as general_models


class Bank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    countries = models.ManyToManyField(general_models.Country, related_name="banks")
