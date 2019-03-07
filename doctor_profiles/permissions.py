from typing import List

from itypes import Object

from accounts.models import Account
from doctor_profiles.models import DoctorProfile
from receptionist_profiles.models import ReceptionistProfile


def is_doctor_or_receptionist(user: Account):
    """
    Check whether logged in user is a doctor or a receptionist

    Parameters:
    accounts.Account model

    Returns:
    bool, profile instance
    """
    user_type = None
    try:
        doctor = DoctorProfile.objects.get(user=user)
        user_type = doctor
    except DoctorProfile.DoesNotExist:
        try:
            receptionist = ReceptionistProfile.objects.get(user=user)
            user_type = receptionist
        except ReceptionistProfile.DoesNotExist:
            return False, user_type
    return True, user_type


def user_is_authorized(user: Account, doctor: DoctorProfile, allowed_types: List[str]) -> bool:
    """

    :param user:
    :param doctor:
    :param allowed_types:
    :return: bool
    """
    is_authorized = False

    if user.doctor_profile():
        if 'doctor' in allowed_types:
            is_authorized = user.doctor_profile() == doctor
    if user.receptionist_profile():
        if 'receptionist' in allowed_types:
            is_authorized = user.receptionist_profile() == doctor.get_receptionists()

    return is_authorized
