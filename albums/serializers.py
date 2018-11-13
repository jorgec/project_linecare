from . import models

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = (
            'pk',
            'slug',
            'name',
            'description',
            'is_public',
            'album_type'
        )


class AlbumUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=500, allow_blank=True, required=False)

    class Meta:
        model = models.Album
        fields = (
            'name',
            'description',
            'is_public'
        )

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.is_public = validated_data.get('is_public', instance.is_public)
            instance.save()
            return instance


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = (
            'pk',
            'photo',
            'caption',
            'is_primary',
            'is_public',
            'album'
        )


class PhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = (
            'caption',
        )

        def update(self, instance, validated_data):
            instance.caption = validated_data.get('caption', instance.caption)
            instance.save()
            return instance


class PhotoUploadSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()

    class Meta:
        model = models.Photo
        fields = (
            'photo',
            'caption',
        )

        def create(self, validated_data):
            photo = validated_data.pop('photo')

            return models.Photo.objects.create(photo=photo)


class AlbumWithPhotosSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = (
            'pk',
            'slug',
            'name',
            'description',
            'is_public',
            'album_type',
            'photos'
        )
