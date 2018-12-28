from rest_framework import serializers

from drug_information.models import Drug, GenericName
from drug_information.models.drug_models import ActiveIngredient, DrugRoute, PharmaceuticalClass, DosageForm


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


class ActiveIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveIngredient
        fields = '__all__'


class DrugRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugRoute
        fields = '__all__'


class PharmaceuticalClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmaceuticalClass
        fields = '__all__'


class DosageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageForm
        fields = '__all__'


class DrugDetailSerializer(serializers.ModelSerializer):
    generic_name = GenericNameSerializer()
    generic_name_list = serializers.SerializerMethodField('repr_generic_name_list')
    active_ingredients = serializers.SerializerMethodField('repr_active_ingredients')
    routes = serializers.SerializerMethodField('repr_routes')
    pharm_class = serializers.SerializerMethodField('repr_pharm_class')
    dosage_forms = serializers.SerializerMethodField('repr_dosage_forms')
    active_ingredients_rel = serializers.SerializerMethodField('repr_active_ingredients_rel')
    routes_rel = serializers.SerializerMethodField('repr_routes_rel')
    pharm_class_rel = serializers.SerializerMethodField('repr_pharm_class_rel')
    dosage_forms_rel = serializers.SerializerMethodField('repr_dosage_forms_rel')

    def repr_generic_name_list(self, obj):
        return obj.get_generic_names()

    def repr_active_ingredients(self, obj):
        return obj.get_active_ingredients()

    def repr_routes(self, obj):
        return obj.get_routes()

    def repr_pharm_class(self, obj):
        return obj.get_pharm_class()

    def repr_dosage_forms(self, obj):
        return obj.get_dosage_forms()

    def repr_active_ingredients_rel(self, obj):
        return ActiveIngredientSerializer(obj.get_active_ingredients_rel(), many=True).data

    def repr_routes_rel(self, obj):
        return DrugRouteSerializer(obj.get_routes_rel(), many=True).data

    def repr_pharm_class_rel(self, obj):
        return PharmaceuticalClassSerializer(obj.get_pharm_class_rel(), many=True).data

    def repr_dosage_forms_rel(self, obj):
        return DosageFormSerializer(obj.get_dosage_forms_rel(), many=True).data

    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'base_name',
            'slug',
            'is_generic',
            'product_type',
            "generic_name_list",
            "active_ingredients",
            "routes",
            "pharm_class",
            "dosage_forms",
            "generic_name",
            "active_ingredients_rel",
            "routes_rel",
            "pharm_class_rel",
            "dosage_forms_rel",
        )
