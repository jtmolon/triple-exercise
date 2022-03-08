from rest_framework import mixins, serializers, viewsets

from banks import models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["id", "name", "countries"]


class BankViewSet(viewsets.ModelViewSet):
    queryset = models.Bank.objects.all()
    serializer_class = BankSerializer


class TransactionSerializer(serializers.Serializer):
    is_eligible = serializers.BooleanField(default=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        pass

