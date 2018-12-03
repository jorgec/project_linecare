from django.core.exceptions import ObjectDoesNotExist
from rest_framework.utils import json

from albums.serializers import SinglePhotoSerializer
from doctor_profiles.serializers import MedicalDegreePublicSerializer, InsuranceProviderPublicSerializer, \
    SpecializationPublicSerializer, MedicalAssociationPublicSerializer, \
    MedicalInstitutionPublicSerializer
from profiles.serializers import GenderSerializer


def public_doctor_profile_template(*, user, as_json=False):
    try:
        doctor_profile = user.doctor_profile()
    except ObjectDoesNotExist:
        return False

    profile = user.base_profile()
    if not profile:
        return False

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

    if profile_photo:
        _profile_photo = SinglePhotoSerializer({'photo': profile_photo}).data
    if cover_photo:
        _cover_photo = SinglePhotoSerializer({'photo': cover_photo}).data

    medical_degrees = MedicalDegreePublicSerializer(doctor_profile.get_degrees()).data
    insurance_providers = InsuranceProviderPublicSerializer(doctor_profile.get_insurance_providers()).data
    specializations = SpecializationPublicSerializer(doctor_profile.get_specializations()).data
    subspecializations = {}
    associations = MedicalAssociationPublicSerializer(doctor_profile.get_associations()).data
    fellowships = MedicalAssociationPublicSerializer(doctor_profile.get_fellowships()).data
    diplomates = MedicalAssociationPublicSerializer(doctor_profile.get_diplomates()).data
    medical_institutions = MedicalInstitutionPublicSerializer(doctor_profile.get_medical_institutions()).data

    data = {
        'id': user.id,
        'doctor_id': doctor_profile.id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'gender': GenderSerializer(profile.gender).data,
        'date_of_birth': profile.date_of_birth,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'medical_degrees': medical_degrees,
        'insurance_providers': insurance_providers,
        'specializations': specializations,
        'subspecializations': subspecializations,
        'associations': associations,
        'fellowships': fellowships,
        'diplomates': diplomates,
        'medical_institutions': medical_institutions,
    }

    if as_json:
        return json.dumps(data)
    return data
