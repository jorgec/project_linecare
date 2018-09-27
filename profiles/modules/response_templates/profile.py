from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from albums.serializers import AlbumSerializer, PhotoSerializer
from profiles.modules.response_templates.mobtel import mobtel_dict_template, private_mobtel_dict_template


def public_profile_template(user, as_json=False):
    profile = user.base_profile()
    albums = profile.get_albums()
    _albums = ''
    mobtels = profile.get_public_mobtels()
    _mobtels = ''
    profile_photo = profile.get_profile_photo()
    _profile_photo = ''
    cover_photo = profile.get_cover_photo()
    _cover_photo = ''

    if albums:
        _albums = AlbumSerializer(albums, many=True).data
    if mobtels:
        _mobtels = mobtel_dict_template(mobtels)
    if profile_photo:
        _profile_photo = PhotoSerializer(profile_photo).data
    if cover_photo:
        _cover_photo = PhotoSerializer(cover_photo).data

    data = {
        'username': user.username,
        'user_type': user.user_type,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'gender': profile.gender,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'albums': _albums,
        'mobtels': _mobtels
    }

    if as_json:
        return json.dumps(data)
    return data


def update_template(**kwargs):
    as_json = kwargs['as_json']
    status = kwargs['status']
    request = kwargs['request']
    result = kwargs['result']

    if status == HTTP_200_OK:
        message = 'Save successful'
        data = result
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


def private_profile_template(user, as_json=False):
    profile = user.base_profile()
    albums = profile.get_albums()
    _albums = ''
    private_albums = profile.get_private_albums()
    _private_albums = ''
    mobtels =profile.get_all_mobtels()
    _mobtels = ''
    profile_photo = profile.get_profile_photo()
    _profile_photo = ''
    cover_photo = profile.get_cover_photo()
    _cover_photo = ''

    if albums:
        _albums = AlbumSerializer(albums, many=True).data
    if private_albums:
        _private_albums = AlbumSerializer(private_albums, many=True).data
    if mobtels:
        _mobtels = private_mobtel_dict_template(mobtels)
    if profile_photo:
        _profile_photo = PhotoSerializer(profile_photo).data
    if cover_photo:
        _cover_photo = PhotoSerializer(cover_photo).data

    data = {
        'username': user.username,
        'user_type': user.user_type,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'gender': profile.gender,
        'date_of_birth': profile.date_of_birth,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'albums': _albums,
        'private_albums': _private_albums,
        'mobtels': _mobtels
    }

    if as_json:
        return json.dump(data)
    return data