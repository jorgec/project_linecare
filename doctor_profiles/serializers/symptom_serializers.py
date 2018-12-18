from rest_framework import serializers

from doctor_profiles.models import Symptom, PatientSymptom, PatientCheckupRecord
from doctor_profiles.serializers import PatientQueuePrivateSerializer
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


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


class PatientSymptomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSymptom
        fields = (
            'symptom',
            'checkup'
        )


class PatientCheckupRecordSerializer(serializers.ModelSerializer):
    appointment = PatientQueuePrivateSerializer()

    class Meta:
        model = PatientCheckupRecord
        fields = (
            'id',
            'appointment'
        )


class PatientSymptomSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer()
    checkup = PatientCheckupRecordSerializer()
    added_by = DoctorProfilePrivateSerializer()
    removed_by = DoctorProfilePrivateSerializer()
    class Meta:
        model = PatientSymptom
        fields = (
            'id',
            'symptom',
            'checkup',
            'is_deleted',
            'added_by',
            'removed_by'
        )
