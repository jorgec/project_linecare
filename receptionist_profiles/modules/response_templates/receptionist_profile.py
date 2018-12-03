from django.core.exceptions import ObjectDoesNotExist
from rest_framework.utils import json

from albums.serializers import SinglePhotoSerializer
from profiles.modules.response_templates.phone import private_phone_dict_template
from profiles.serializers import GenderSerializer
from receptionist_profiles.serializers import ReceptionistConnectionPrivateNestedSerializer, \
    ReceptionistProfileSerializer


def private_receptionist_profile_template(*, user, nested=False, as_json=False, doctor_id=None):
    try:
        receptionist_profile = user.receptionistprofile
    except ObjectDoesNotExist:
        return False

    if nested:
        if doctor_id:
            connections_serializer = ReceptionistConnectionPrivateNestedSerializer(receptionist_profile.get_medical_institution_connections(doctor_id=doctor_id), many=True).data
        else:
            connections_serializer = ReceptionistConnectionPrivateNestedSerializer(receptionist_profile.get_medical_institution_connections(), many=True).data
    else:
        connections_serializer = {}

    receptionist_serializer = ReceptionistProfileSerializer(receptionist_profile)

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
        'phones': _phones,
        'connections': connections_serializer,
        'receptionist': receptionist_serializer.data
    }

    if as_json:
        return json.dumps(data)
    return data
