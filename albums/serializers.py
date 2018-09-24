from . import models

from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'description',
            'is_public',
            'album_type'
        )


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = (
            'pk',
            'created',
            'last_updated',
            'photo',
            'caption',
            'is_primary',
            'is_public',
        )
