from rest_framework import serializers

from doctor_profiles.models import Diagnosis, PatientDiagnosis, PatientCheckupRecord
from doctor_profiles.serializers import PatientQueuePrivateSerializer
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


class Diagnoseserializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class DiagnosisCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Diagnosis
        fields = (
            'id',
            'name',
            'description'
        )


class PatientDiagnosisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnosis
        fields = (
            'diagnosis',
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


class PatientDiagnoseserializer(serializers.ModelSerializer):
    diagnosis = Diagnoseserializer()
    checkup = PatientCheckupRecordSerializer()
    added_by = DoctorProfilePrivateSerializer()
    removed_by = DoctorProfilePrivateSerializer()
    class Meta:
        model = PatientDiagnosis
        fields = (
            'id',
            'diagnosis',
            'checkup',
            'is_deleted',
            'added_by',
            'removed_by'
        )
