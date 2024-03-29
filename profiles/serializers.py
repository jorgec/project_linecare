from django.urls import reverse
from rest_framework import serializers

from albums.models import Photo
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
            'id',
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


class BaseProfilePrivateSerializerFull(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField('repr_profile_photo')
    profile_photo_css = serializers.SerializerMethodField('repr_profile_photo_css')
    gender = GenderSerializer()
    full_name = serializers.SerializerMethodField('repr_full_name')
    patient_detail_url = serializers.SerializerMethodField('repr_patient_url')

    def repr_profile_photo(self, obj):
        if type(obj.get_profile_photo()) == Photo:
            return obj.get_profile_photo().photo.url
        else:
            return obj.get_profile_photo()

    def repr_profile_photo_css(self, obj):
        if type(obj.get_profile_photo()) == Photo:
            photo = obj.get_profile_photo().photo.url
        else:
            photo = obj.get_profile_photo()

        return f"background-image: url({photo})"

    def repr_patient_url(self, obj):
        url = reverse('doctor_profile_patient_detail', kwargs={
            'patient_id': obj.id
        })
        return url

    def repr_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = BaseProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'profile_photo',
            'profile_photo_css',
            'full_name',
            'patient_detail_url'
        )
