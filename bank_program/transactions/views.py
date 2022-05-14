from rest_framework import serializers, viewsets

from transactions import models


class TransactionSerializer(serializers.ModelSerializer):

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


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
