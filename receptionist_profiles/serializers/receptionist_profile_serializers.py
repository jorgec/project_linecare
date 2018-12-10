from rest_framework import serializers

from accounts.serializers import AccountSerializerPublic
from doctor_profiles.serializers import MedicalInstitutionTypePublicSerializer
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer
from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.models.receptionist_profile_model import ReceptionistConnection


class ReceptionistProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializerPublic()

    class Meta:
        model = ReceptionistProfile
        fields = (
            'id',
            'user'
        )


class ReceptionistProfileCreateByDoctorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=120)


class ReceptionistConnectionPrivateNestedSerializer(serializers.ModelSerializer):
    doctor = DoctorProfilePrivateSerializer()
    medical_institution = MedicalInstitutionTypePublicSerializer(allow_null=True)
    receptionist = ReceptionistProfileSerializer(allow_null=True)

    class Meta:
        model = ReceptionistConnection
        fields = (
            'receptionist',
            'doctor',
            'medical_institution'
        )


class ReceptionistConnectionPrivateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionistConnection
        fields = (
            'receptionist',
            'doctor',
            'medical_institution'
        )
