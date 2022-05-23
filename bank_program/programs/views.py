from rest_framework import serializers, viewsets

from programs import models


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Program
        fields = ("id", "name", "currency", "return_percentage",)


class ProgramEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramEligibility
        fields = ("id", "program", "bank", "country")


class ProgramViewSet(viewsets.ModelViewSet,):
    queryset = models.Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramEligibilityViewSet(viewsets.ModelViewSet,):
    queryset = models.ProgramEligibility.objects.all()
    serializer_class = ProgramEligibilitySerializer
