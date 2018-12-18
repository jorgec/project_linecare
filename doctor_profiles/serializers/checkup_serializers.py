from rest_framework import serializers

from doctor_profiles.models import CheckupNote
from doctor_profiles.serializers.doctor_profile_serializers import DoctorProfilePrivateSerializer


class CheckupNoteSerializer(serializers.ModelSerializer):
    added_by = DoctorProfilePrivateSerializer()
    class Meta:
        model = CheckupNote
        fields = (
            'id',
            'note',
            'checkup',
            'added_by',
            'created'
        )


class CheckupNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckupNote
        fields = (
            'note',
            'checkup',
            'added_by'
        )