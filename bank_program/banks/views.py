from rest_framework import mixins, serializers, viewsets

from banks import models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["id", "name", "countries"]


class BankViewSet(viewsets.ModelViewSet):
    queryset = models.Bank.objects.all()
    serializer_class = BankSerializer


