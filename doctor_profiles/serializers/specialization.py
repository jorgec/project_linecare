from rest_framework import serializers

from doctor_profiles import models
from doctor_profiles.serializers import DoctorProfileSerializer, DoctorProfilePublicSerializer


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
            'practitioner_title',
            'practitioner_title_plural'
        )


class SpecializationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'id',
            'slug',
            'name',
            'abbreviation',
            'practitioner_title',
            'practitioner_title_plural'
        )


class SpecializationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            'name',
            'abbreviation',
            'practitioner_title',
            'practitioner_title_plural'
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


class DoctorSpecializationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorSpecialization
        fields = (
            'year_attained',
            'place_of_residency',
        )
