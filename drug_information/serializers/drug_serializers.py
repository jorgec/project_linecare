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
            'marketing_status',
            'route',
            'pharm_class',
            'dosage_form',
            'generic_name'
        )


class DrugCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = (

        )