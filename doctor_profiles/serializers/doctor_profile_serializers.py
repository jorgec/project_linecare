from rest_framework import serializers

from accounts.serializers import AccountSerializerPublic, AccountWithProfileSerializerPrivate
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


class DoctorProfilePrivateSerializer(serializers.ModelSerializer):
    user = AccountWithProfileSerializerPrivate()
    doctor_name = serializers.SerializerMethodField('repr_doctor_name')

    def repr_doctor_name(self, obj):
        return str(obj)

    class Meta:
        model = models.DoctorProfile
        fields = ('id',
                  'user',
                  'doctor_name'
                  )
