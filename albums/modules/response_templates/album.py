from rest_framework.utils import json

from albums.serializers import PhotoSerializer


def album_with_photos_template(album, photos, as_json=False):
    obj = {
        'pk': album.pk,
        'slug': album.slug,
        'name': album.name,
        'description': album.description,
        'is_public': album.is_public,
        'album_type': album.album_type,
        'photos': list(PhotoSerializer(photos, many=True).data)
    }

    if as_json:
        return json.dumps(obj)
    return obj
