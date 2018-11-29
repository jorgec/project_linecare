from django.core.exceptions import ObjectDoesNotExist
from rest_framework.utils import json

from albums.serializers import SinglePhotoSerializer
from profiles.modules.response_templates.phone import private_phone_dict_template
from receptionist_profiles.serializers import ReceptionistConnectionPrivateNestedSerializer, \
    ReceptionistProfileSerializer


def private_receptionist_profile_template(*, user, nested=False, as_json=False):
    try:
        receptionist_profile = user.receptionistprofile
    except ObjectDoesNotExist:
        return False

    if nested:
        connections_serializer = ReceptionistConnectionPrivateNestedSerializer(
            receptionist_profile.receptionist_connections.all(), many=True).data
    else:
        connections_serializer = {}

    receptionist_serializer = ReceptionistProfileSerializer(receptionist_profile)

    profile = user.base_profile()
    phones = profile.get_all_phones()
    _phones = {}
    profile_photo = profile.get_profile_photo()
    _profile_photo = {'photo': None}
    cover_photo = profile.get_cover_photo()
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
        'gender': profile.gender,
        'date_of_birth': profile.date_of_birth,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'phones': _phones,
        'connections': connections_serializer,
        'receptionist': receptionist_serializer.data
    }

    if as_json:
        return json.dumps(data)
    return data
