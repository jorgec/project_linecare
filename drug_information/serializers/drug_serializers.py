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


class DrugDetailSerializer(serializers.ModelSerializer):
    generic_name_list = serializers.SerializerMethodField('repr_generic_name_list')
    active_ingredients = serializers.SerializerMethodField('repr_active_ingredients')
    routes = serializers.SerializerMethodField('repr_routes')
    pharm_class = serializers.SerializerMethodField('repr_pharm_class')
    dosage_forms = serializers.SerializerMethodField('repr_dosage_forms')

    def repr_generic_name_list(self, obj):
        generic_names = []

        meta = obj.meta.get('generic_names', None)
        if meta:
            for gn in meta:
                generic_names.append(gn)

        return ", ".join(generic_names)

    def repr_active_ingredients(self, obj):
        return ", ".join([x.active_ingredient.name for x in obj.drug_ingredients.all()])

    def repr_routes(self, obj):
        return ", ".join([x.route.name for x in obj.drug_routes.all()])

    def repr_pharm_class(self, obj):
        return ", ".join([x.pharm_class.name for x in obj.drug_pharmclass.all()])

    def repr_dosage_forms(self, obj):
        return ", ".join([x.dosage_form.name for x in obj.drug_dosageforms.all()])

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
            "dosage_forms"
        )
