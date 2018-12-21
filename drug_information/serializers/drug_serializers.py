from rest_framework import serializers

from drug_information.models import Drug, GenericName


class GenericNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericName
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    generic_name = GenericNameSerializer()

    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'base_name',
            'slug',
            'is_generic',
            'product_type',
            'generic_name',
            'drug_ingredients',
            'drug_routes',
            'drug_pharmclass',
            'drug_dosageforms'
        )


class DrugCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = (
            'name',
            'base_name',
            'generic_name',
            'is_generic',
            'product_type'
        )