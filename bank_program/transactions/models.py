import uuid

from django.db import models

from banks import models as bank_models
from general import models as general_models
from programs import models as program_models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(general_models.Country, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(general_models.Currency, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(program_models.Program, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(bank_models.Bank, on_delete=models.SET_NULL, null=True)
    is_eligible = models.BooleanField(default=True)

