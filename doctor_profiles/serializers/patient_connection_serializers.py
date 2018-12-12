from rest_framework import serializers

from doctor_profiles.models import PatientConnection
from doctor_profiles.serializers import DoctorProfileSerializer
from profiles.serializers import ProfileSerializer


class PatientConnectionSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    patient = ProfileSerializer()
    class Meta:
        model = PatientConnection
        fields = (
            'id',
            'created',
            'doctor',
            'patient'
        )
