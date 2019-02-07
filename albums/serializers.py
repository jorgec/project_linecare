from . import models

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, HybridImageField


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = (
            'id',
            'pk',
            'slug',
            'name',
            'description',
            'is_public',
            'album_type'
        )


class AlbumCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = models.Album
        fields = (
            'id',
            'name',
            'is_public'
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
            'id',
            'pk',
            'photo',
            'caption',
            'is_primary',
            'is_public',
            'album'
        )


class SinglePhotoSerializer(serializers.Serializer):
    photo = serializers.CharField(allow_blank=True, allow_null=True, max_length=1024)


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
    photo = HybridImageField()

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
