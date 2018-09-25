from rest_framework import serializers

from albums.serializers import AlbumSerializer, PhotoSerializer
from profiles.models import BaseProfile, ProfileMobtel, Gender


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (
            'name',
            'slug'
        )


class PublicMobtelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMobtel
        fields = (
            'number',
            'carrier'
        )


class PublicProfileSerializer(serializers.Serializer):
    mobtels = PublicMobtelSerializer(many=True, read_only=True)
    albums = AlbumSerializer(many=True, read_only=True)
    profile_photo = PhotoSerializer(read_only=True)
    cover_photo = PhotoSerializer(read_only=True)
    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    gender = GenderSerializer(read_only=True)
    user_type = serializers.IntegerField()


class PrivateMobtelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMobtel
        fields = (
            'number',
            'carrier',
            'is_primary',
            'is_active',
            'is_private'
        )


class PrivateProfileSerializer(serializers.ModelSerializer):
    mobtels = PrivateMobtelSerializer(many=True, read_only=True)
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = BaseProfile
        fields = (
            'gender',
            'date_of_birth',
            'mobtels',
            'albums'
        )
