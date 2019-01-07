from rest_framework import serializers

from doctor_profiles.models import PatientSymptom
from doctor_profiles.serializers.symptom_serializers import PatientSymptomSerializer


class SymptomAggregateSerializer(serializers.Serializer):
    symptom = serializers.IntegerField()
    scount = serializers.IntegerField()
    symptom_name = serializers.SerializerMethodField('repr_symptom_obj')

    def repr_symptom_obj(self, obj):
        return ''


