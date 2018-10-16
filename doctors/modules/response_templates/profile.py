from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

def private_doctor_profile_template(user, as_json=False):
    doctor = user.base_profile().get_doctor_profile()
    specialties = doctor.get_doctor_specialties()

    data = {
        'license_number': doctor.license_number,
        'year_started': doctor.year_started,
        'medical_subject': doctor.medical_subject,
        'specialties': specialties,
        'insurance': doctor.insurance
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

def public_doctor_profile_template(user, as_json=False):
    doctor = user.base_profile().get_doctor_profile()
    specialties = doctor.get_doctor_specialties()

    data = {
        'year_started': doctor.year_started,
        'medical_subject': doctor.medical_subject,
        'specialties': specialties,
        'insurance': doctor.insurance
    }

    if as_json:
        return json.dumps(data)
    return data