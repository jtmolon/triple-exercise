import uuid

from django.db import models


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(unique=True, null=False)
    name = models.TextField(null=False)


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(unique=True, null=False)
    name = models.TextField(null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="countries")
