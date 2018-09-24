from rest_framework import serializers

from profiles.models import BaseProfile, ProfileMobtel


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'gender',
        )


class PrivateMobtelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMobtel
        fields = (
            'number',
            'carrier',
            'is_primary'
        )


class PrivateProfileSerializer(serializers.ModelSerializer):
    mobtels = PrivateMobtelSerializer(many=True, read_only=True)

    class Meta:
        model = BaseProfile
        fields = (
            'gender',
            'date_of_birth',
            'mobtels'
        )
