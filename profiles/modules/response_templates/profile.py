from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from albums.serializers import AlbumSerializer, PhotoSerializer, SinglePhotoSerializer
from profiles.modules.response_templates.phone import phone_dict_template, private_phone_dict_template
from profiles.serializers import GenderSerializer


def public_profile_template(user, as_json=False):
    profile = user.base_profile()
    if not profile:
        return False

    try:
        phones = profile.get_public_phones()
    except AttributeError:
        phones = None
    _phones = ''
    try:
        profile_photo = profile.get_profile_photo()
    except AttributeError:
        profile_photo = None
    _profile_photo = ''
    try:
        cover_photo = profile.get_cover_photo()
    except AttributeError:
        cover_photo = None
    _cover_photo = ''

    if phones:
        _phones = phone_dict_template(phones)
    if profile_photo:
        _profile_photo = PhotoSerializer(profile_photo).data
    if cover_photo:
        _cover_photo = PhotoSerializer(cover_photo).data

    data = {
        'username': user.username,
        'user_type': user.user_type,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'gender': GenderSerializer(profile.gender).data,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'phones': _phones
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
    if not profile:
        return False

    try:
        phones = profile.get_all_phones()
    except AttributeError:
        phones = None
    _phones = {}
    try:
        profile_photo = profile.get_profile_photo()
    except AttributeError:
        profile_photo = None
    _profile_photo = {'photo': None}
    try:
        cover_photo = profile.get_cover_photo()
    except AttributeError:
        cover_photo = None
    _cover_photo = {'photo': None}

    if phones:
        _phones = private_phone_dict_template(phones)
    if profile_photo:
        _profile_photo = SinglePhotoSerializer({'photo': profile_photo}).data
    if cover_photo:
        _cover_photo = SinglePhotoSerializer({'photo': cover_photo}).data

    data = {
        'id': user.id,
        'username': user.username,
        'user_type': user.user_type,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'gender': GenderSerializer(profile.gender).data,
        'date_of_birth': profile.date_of_birth,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'phones': _phones
    }

    if as_json:
        return json.dumps(data)
    return data
