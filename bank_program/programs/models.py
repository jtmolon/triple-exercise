import uuid
from django.db import models


class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(null=False)
    currency = models.TextField(null=False, max_length=3)
    return_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=False)

