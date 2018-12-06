from rest_framework import serializers

from doctor_profiles import models
from .doctor_profile_serializers import DoctorProfileSerializer, DoctorProfilePublicSerializer


class MedicalDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalDegree
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'abbreviation',
            'metadata',
            'is_approved',
        )


class MedicalDegreePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalDegree
        fields = (
            'id',
            'slug',
            'name',
            'abbreviation',
        )


class MedicalDegreeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalDegree
        fields = (
            'name',
            'abbreviation',
        )


class DoctorDegreeSerializer(serializers.ModelSerializer):
    degree = MedicalDegreeSerializer()
    doctor = DoctorProfileSerializer()

    class Meta:
        model = models.DoctorDegree
        fields = (
            'id',
            'created',
            'last_updated',
            'year_attained',
            'school',
            'metadata',
            'license_number',
            'doctor',
            'degree',
        )


class DoctorDegreePublicSerializer(serializers.ModelSerializer):
    degree = MedicalDegreePublicSerializer()
    doctor = DoctorProfilePublicSerializer()

    class Meta:
        model = models.DoctorDegree
        fields = (
            'id',
            'year_attained',
            'school',
            'license_number',
            'doctor',
            'degree',
        )


class DoctorDegreeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'school',
            'year_attained',
            'license_number',
            'degree'
        )
        extra_kwargs = {
            "degree": {
                "error_messages": {
                    "blank": "Medical Degree is required",
                    "null": "Medical Degree is required",
                    "invalid": "Medical Degree is required",
                }
            },
            "school": {
                "error_messages": {
                    "blank": "School is required",
                }
            },
            "year_attained": {
                "error_messages": {
                    "blank": "Year Attained is required",
                    "invalid": "Year Attained must be a year",
                }
            },
            "license_number": {
                "error_messages": {
                    "blank": "License Number is required"
                }
            }
        }


class DoctorDegreeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'school',
            'year_attained',
            'license_number',
        )
