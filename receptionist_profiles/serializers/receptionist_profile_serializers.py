from rest_framework import serializers

from receptionist_profiles.models import ReceptionistProfile


class ReceptionistProfileSerializer(serializers.ModelSerializer):
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


