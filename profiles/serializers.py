from rest_framework import serializers

from albums.serializers import AlbumSerializer, PhotoSerializer
from profiles.models import BaseProfile, ProfilePhone, Gender


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (
            'name',
            'slug'
        )


class PublicPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhone
        fields = (
            'number',
            'carrier'
        )


class PublicProfileSerializer(serializers.Serializer):
    phones = PublicPhoneSerializer(many=True, read_only=True)
    albums = AlbumSerializer(many=True, read_only=True)
    profile_photo = PhotoSerializer(read_only=True)
    cover_photo = PhotoSerializer(read_only=True)
    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    gender = GenderSerializer(read_only=True)
    user_type = serializers.IntegerField()


class PrivatePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhone
        fields = (
            'number',
            'carrier',
            'is_public',
            'is_primary',
            'is_active'
        )


# class PrivateProfileSerializer(serializers.ModelSerializer):
#     phones = PrivatePhoneSerializer(many=True, read_only=True)
#     albums = AlbumSerializer(many=True, read_only=True)
#     profile_photo = PhotoSerializer(read_only=True)
#     cover_photo = PhotoSerializer(read_only=True)
#     username = serializers.CharField(max_length=32)
#     first_name = serializers.CharField(max_length=32)
#     last_name = serializers.CharField(max_length=32)
#     gender = GenderSerializer(read_only=True)
#     user_type = serializers.IntegerField()

class PrivateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'first_name',
            'last_name',
            'gender',
            'date_of_birth'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'first_name',
            'last_name',
            'gender',
            'date_of_birth'
        )

        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.save()
            return instance


class PublicBaseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = (
            'first_name',
            'last_name',
        )
