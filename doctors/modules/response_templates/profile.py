from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

def private_doctor_profile_template(user, as_json=False):
    profile = user.base_profile()
    doctor = profile.get_doctor_profile()

    data = {
        'license_number': doctor.license_number,
        'medical_subject': doctor.medical_subject,
        'insurance': doctor.insurance
    }