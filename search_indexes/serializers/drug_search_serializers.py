import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search_indexes.documents import DrugDocument


class DrugDocumentSerializer(DocumentSerializer):
    """Serializer for the Drug document."""

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = DrugDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'name',
            'base_name',
            'generic_names',
            'active_ingredients',
            'routes',
            'pharm_class',
            'dosage_forms',
        )
