from rest_framework import serializers

from profiles.models import BaseProfile, ProfileMobtel


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'gender',
        )


class PrivateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'gender',
            'date_of_birth',
        )


class PrivateMobtelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMobtel
        fields = (
            'number',
            'carrier',
            'is_primary'
        )
