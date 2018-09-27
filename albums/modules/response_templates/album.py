from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from albums.serializers import PhotoSerializer, AlbumSerializer


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


def save_template(**kwargs):
    as_json = kwargs['as_json']
    status = kwargs['status']
    request = kwargs['request']
    result = kwargs['result']

    if status == HTTP_200_OK:
        message = 'Save successful'
        data = AlbumSerializer(result).data
    else:
        message = result
        data = request.data

    response = {
        'status': status,
        'message': message,
        'data': data
    }

    if as_json:
        return json.dumps(response)
    return response
