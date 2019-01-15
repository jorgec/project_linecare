from rest_framework import serializers

from accounts.serializers import AccountSerializerPublic, AccountWithProfileSerializerPrivate
from doctor_profiles import models


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializerPublic()
    doctor_name = serializers.SerializerMethodField('repr_doctor_name')

    def repr_doctor_name(self, obj):
        return str(obj)
    class Meta:
        model = models.DoctorProfile
        fields = (
            'id',
            'created',
            'last_updated',
            'metadata',
            'user',
            'doctor_name'
        )


class DoctorProfilePublicSerializer(serializers.ModelSerializer):
    user = AccountSerializerPublic()
    doctor_name = serializers.SerializerMethodField('repr_doctor_name')

    def repr_doctor_name(self, obj):
        return str(obj)
    class Meta:
        model = models.DoctorProfile
        fields = (
            'id',
            'user',
            'doctor_name'
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
