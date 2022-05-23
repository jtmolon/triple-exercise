from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


from banks import models as bank_models
from programs import models as program_models
from transactions.models import Transaction


@receiver(pre_save, sender=Transaction)
def pre_save_transaction(sender, instance, **kwargs):
    instance.is_eligible = (
        instance.country.currency.id == instance.currency.id and
        instance.bank.countries.contains(instance.country) and
        program_models.ProgramEligibility.objects.filter(
            country=instance.country,
            bank=instance.bank.name,
            program__currency=instance.currency,
            program=instance.program,
        ).exists()
    )


@receiver(post_save, sender=bank_models.Bank)
def post_save_bank(sender, instance, created, **kwargs):
    # new banks have no transactions
    if created:
        return
    for transaction in Transaction.objects.filter(bank=instance).all():
        transaction.is_eligible = (
            transaction.is_eligible and
            instance.countries.contains(transaction.country)
        )
        transaction.save()
