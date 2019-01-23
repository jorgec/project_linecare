from rest_framework import serializers

from doctor_profiles.models import MedicalInstitutionDoctor


class MedicalInstitutionDoctorPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionDoctor
        fields = '__all__'


class MedicalInstitutionDoctorCreatePrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitutionDoctor
        fields = (
            'doctor',
            'medical_institution'
        )
