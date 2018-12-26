import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search_indexes.documents import DoctorDocument


class DoctorDocumentSerializer(DocumentSerializer):
    """Serializer for the Doctor document."""

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = DoctorDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'name',
            'specializations',
            'degrees',
            'associations',
            'diplomates',
            'fellowships',
            'insurance_providers',
            'medical_institutions',
            'addresses',
        )
