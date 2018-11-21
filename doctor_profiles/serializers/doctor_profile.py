from rest_framework import serializers

from accounts.serializers import AccountSerializerPublic
from doctor_profiles import models


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
            'id',
            'user',
        )
