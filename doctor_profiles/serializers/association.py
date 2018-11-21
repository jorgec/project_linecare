from rest_framework import serializers

from doctor_profiles import models
from doctor_profiles.serializers import DoctorProfileSerializer, DoctorProfilePublicSerializer


class MedicalAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalAssociation
        fields = (
            'id',
            'slug',
            'name',
            'created',
            'last_updated',
            'abbreviation',
            'metadata',
        )


class MedicalAssociationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalAssociation
        fields = (
            'id',
            'slug',
            'name',
            'abbreviation',
        )


class MedicalAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalAssociation
        fields = (
            'name',
            'abbreviation'
        )


class DoctorAssociationSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    association = MedicalAssociationSerializer()

    class Meta:
        model = models.DoctorAssociation
        fields = (
            'id',
            'created',
            'last_updated',
            'level',
            'year_attained',
            'doctor',
            'association'
        )


class DoctorAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAssociation
        fields = (
            'level',
            'year_attained',
            'association'
        )


class DoctorAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAssociation
        fields = (
            'level',
            'year_attained',
        )


class DoctorAssociationPublicSerializer(serializers.ModelSerializer):
    doctor = DoctorProfilePublicSerializer()
    association = MedicalAssociationPublicSerializer()

    class Meta:
        model = models.DoctorAssociation
        fields = (
            'id',
            'created',
            'last_updated',
            'level',
            'year_attained',
            'doctor',
            'association'
        )
