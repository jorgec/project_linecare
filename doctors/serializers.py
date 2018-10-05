from rest_framework import serializers
from doctors.models import MedicalSubject, Specialty, DoctorProfile


class MedicalSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSubject
        fields = (
            'name',
            'slug'
        )

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        mode = Specialty
        fields = (
            'name',
            'slug'
        )

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        mode = DoctorProfile
        fields = (
            'license_number',
            'year_started',
            'insurance'
        )