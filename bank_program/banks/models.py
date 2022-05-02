import uuid

from django.db import models
# from django.contrib.postgres.fields import ArrayField

from general import models as general_models


class Bank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    # countries = ArrayField(models.TextField(), default=list, blank=True)
    countries = models.ManyToManyField(general_models.Country, related_name="banks")
