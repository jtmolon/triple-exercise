import uuid

from django.db import models

from general import models as general_models


class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(null=False)
    currency = models.ForeignKey(general_models.Currency, on_delete=models.CASCADE)
    return_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=False)


class ProgramEligibility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="eligible_for")
    bank = models.TextField()
    country = models.ForeignKey(general_models.Country, on_delete=models.CASCADE)
