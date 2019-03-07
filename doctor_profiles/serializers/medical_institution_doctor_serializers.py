from rest_framework import serializers

from doctor_profiles.models import MedicalInstitutionDoctor
from doctor_profiles.serializers import MedicalInstitutionSerializer


class MedicalInstitutionDoctorPrivateSerializer(serializers.ModelSerializer):
    medical_institution = MedicalInstitutionSerializer()

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
