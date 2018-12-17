from rest_framework import serializers

from doctor_profiles.models import Symptom, PatientSymptom
from doctor_profiles.serializers import PatientQueuePrivateSerializer


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class SymptomCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Symptom
        fields = (
            'id',
            'name',
            'description'
        )


class PatientSymptomSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer()
    appointment = PatientQueuePrivateSerializer()

    class Meta:
        model = PatientSymptom
        fields = (
            'id',
            'symptom',
            'appointment'
        )


class PatientSymptomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSymptom
        fields = (
            'id',
            'symptom',
            'appointment'
        )
