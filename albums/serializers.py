from . import models

from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = (
            'slug',
            'name',
            'description',
            'is_public',
            'album_type'
        )


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = (
            'pk',
            'photo',
            'caption',
            'is_primary',
            'is_public',
        )
