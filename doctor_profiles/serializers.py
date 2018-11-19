from rest_framework import serializers

from accounts.serializers import AccountSerializerPublic
from doctor_profiles import models


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'metadata',
            'abbreviation',
        )

class SpecializationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'slug',
            'name',
            'abbreviation',
        )


class SpecializationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'name',
            'abbreviation'
        )


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceProvider
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'metadata',
        )


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializerPublic()

    class Meta:
        model = models.DoctorProfile
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'user'
        )


class DoctorProfilePublicSerializer(serializers.ModelSerializer):
    user = AccountSerializerPublic()

    class Meta:
        model = models.DoctorProfile
        fields = (
            'user',
        )


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


class MedicalAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalAssociation
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'abbreviation',
            'metadata',
        )


class DoctorSpecializationSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    specialization = SpecializationSerializer()
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'id',
            'created',
            'last_updated',
            'year_attained',
            'place_of_residency',
            'doctor',
            'specialization'
        )

class DoctorSpecializationPublicSerializer(serializers.ModelSerializer):
    doctor = DoctorProfilePublicSerializer()
    specialization = SpecializationPublicSerializer()
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'id',
            'year_attained',
            'place_of_residency',
            'doctor',
            'specialization'
        )

class DoctorSpecializationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'year_attained',
            'place_of_residency',
            'specialization'
        )
        extra_kwargs = {
            "place_of_residency": {
                "error_messages": {
                    "blank": "Place of Residency is required",
                }
            },
            "year_attained": {
                "error_messages": {
                    "blank": "Year Attained is required",
                    "invalid": "Year Attained must be a year",
                }
            },
        }


class DoctorSpecializationEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'year_attained',
            'place_of_residency',
        )


class DoctorInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorInsurance
        fields = (
            'id',
            'created',
            'last_updated',
            'expiry',
            'identifier',
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


class DoctorDegreeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'school',
            'year_attained',
            'license_number',
        )


class DoctorAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAssociation
        fields = (
            'id',
            'created',
            'last_updated',
            'level',
            'year_attained',
        )
