from rest_framework import serializers

from drug_information.models.drug_models import DrugRoute


class DrugRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugRoute
        fields = '__all__'
