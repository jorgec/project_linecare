from rest_framework import serializers
from doctors.models import MedicalSubject, Specialty, DoctorProfile, Insurance


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

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        mode = Insurance
        fields = {
            'name',
            'slug'
        }

class PrivateDoctorSerializer(serializers.Serializer):
    license_number = serializers.CharField(max_length=12)
    year_started = serializers.IntegerField()
    medical_subject = MedicalSubjectSerializer(read_only=True)
    specialty = SpecialtySerializer(many=True, read_only=True)
    insurance = InsuranceSerializer(read_only=True)