from rest_framework import serializers, viewsets

from programs.models import ProgramEligibility
from transactions import models


class TransactionSerializer(serializers.ModelSerializer):
    is_eligible = serializers.SerializerMethodField()

    class Meta:
        model = models.Transaction
        fields = (
            "id",
            "country",
            "currency",
            "bank",
            "program",
            "is_eligible",
        )
        read_only_fields = (
            "is_eligible",
        )

    def get_is_eligible(self, obj):
        return (
            obj.country.currency.id == obj.currency.id and
            obj.bank.countries.contains(obj.country) and
            ProgramEligibility.objects.filter(
                country=obj.country,
                bank=obj.bank.name,
                program__currency=obj.currency,
                program=obj.program,
            ).exists()
        )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
