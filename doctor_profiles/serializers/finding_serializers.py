from rest_framework import serializers

from doctor_profiles.models import Finding, PatientFinding, PatientCheckupRecord
from doctor_profiles.serializers import PatientQueuePrivateSerializer
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'


class FindingCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Finding
        fields = (
            'id',
            'name',
            'description'
        )


class PatientFindingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFinding
        fields = (
            'finding',
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


class PatientFindingSerializer(serializers.ModelSerializer):
    finding = FindingSerializer()
    checkup = PatientCheckupRecordSerializer()
    added_by = DoctorProfilePrivateSerializer()
    removed_by = DoctorProfilePrivateSerializer()
    class Meta:
        model = PatientFinding
        fields = (
            'id',
            'finding',
            'checkup',
            'is_deleted',
            'added_by',
            'removed_by'
        )
