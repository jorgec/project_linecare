from rest_framework import serializers

from doctor_profiles import models


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'metadata',
            'abbreviation',
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
    class Meta:
        model = models.DoctorProfile
        fields = (
            'pk',
            'created',
            'last_updated',
            'metadata',
        )


class MedicalDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalDegree
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'abbreviation',
            'metadata',
            'is_approved',
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
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'pk',
            'created',
            'last_updated',
            'year_attained',
            'place_of_residency',
        )


class DoctorInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorInsurance
        fields = (
            'pk',
            'created',
            'last_updated',
            'expiry',
            'identifier',
        )


class DoctorDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'pk',
            'created',
            'last_updated',
            'year_attained',
            'school',
            'metadata',
            'license_number',
        )

class DoctorDegreeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'school',
            'year_attended',
            'license_number',
            'degree'
        )


class DoctorDegreeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDegree
        fields = (
            'school',
            'year_attended',
            'license_number',
        )


class DoctorAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAssociation
        fields = (
            'pk',
            'created',
            'last_updated',
            'level',
            'year_attained',
        )
