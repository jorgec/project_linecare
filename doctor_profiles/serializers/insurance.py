from rest_framework import serializers

from doctor_profiles import models
from doctor_profiles.serializers import DoctorProfileSerializer, DoctorProfilePublicSerializer


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceProvider
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'metadata',
            'is_approved'
        )


class InsuranceProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceProvider
        fields = (
            'name',
        )


class InsuranceProviderPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceProvider
        fields = (
            'id',
            'slug',
            'name',
        )


class DoctorInsuranceSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    insurance = InsuranceProviderSerializer()

    class Meta:
        model = models.DoctorInsurance
        fields = (
            'id',
            'created',
            'last_updated',
            'identifier',
            'is_approved',
            'doctor',
            'insurance'
        )


class DoctorInsurancePublicSerializer(serializers.ModelSerializer):
    doctor = DoctorProfilePublicSerializer()
    insurance = InsuranceProviderPublicSerializer()

    class Meta:
        model = models.DoctorInsurance
        fields = (
            'id',
            'identifier',
            'doctor',
            'insurance'
        )


class DoctorInsuranceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorInsurance
        fields = (
            'identifier',
            'insurance'
        )


class DoctorInsuranceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorInsurance
        fields = (
            'identifier',
        )
