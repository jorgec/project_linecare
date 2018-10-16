import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer

from doctors.models import DoctorProfile
from accounts.constants import DOCTOR
from doctors.modules.apis import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()

class TestDoctorApi:
    def test_get_private_doctor_by_pk(self):
        # create dummy account
        user = mixer.blend('accounts.Account', user_type=DOCTOR)
        doctor = user.base_profile().get_doctor_profile()
        doctor.license_number = 'DR85213'
        doctor.year_started = 2010
        doctor.save()

        request =  factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this profile. got {} doctor_license_number: {}".format(response.status_code, doctor.license_number)
        assert response.data['year_started'] == 2010, "Expected 2010. got {}".format(
            response.data['year_started']
        )
        assert 'license_number' in response.data, "Doctor's license should be visible"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 400, 'Must fail on bad request. got {}'.format(response.status_code)

        request = factory.get('/', {'pk': 234634})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 404, 'Must fail on bad request. got {}'.format(response.status_code)

    def test_get_public_doctor_by_pk(self):
        #create dummy user
        user = mixer.blend('accounts.Account', user_type=DOCTOR)
        doctor = user.base_profile().get_doctor_profile()
        doctor.license_number = 'DR85223'
        doctor.year_started = 2015
        doctor.save()

        request = factory.get('/', {'pk': user.pk})
        response = retrieve.ApiPublicDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this profile. got {} doctor_license_number: {}".format(
            response.status_code, doctor.license_number)
        assert response.data['year_started'] == 2015, 'Expected 2010. got {}'.format(
            response.data['year_started']
        )
        assert 'license_number' not in response.data, "Doctor's license should not be visible"
        assert 'medical_subject' in response.data, 'Medical subject should be visible'

        request = factory.get('/')
        response = retrieve.ApiPublicDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 400, 'Must fail on bad request. got {}'.format(response.status_code)

        request = factory.get('/', {'pk': 234634})
        response = retrieve.ApiPublicDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 404, 'Must fail on bad request. got {}'.format(response.status_code)

    def test_get_public_doctor_by_medical_subject(self):
        # create dummy user
        user = mixer.blend('accounts.Account', user_type=DOCTOR)
        m = mixer.blend('doctors.MedicalSubject')
        doctor = user.base_profile().get_doctor_profile()
        doctor.medical_subject = m
        doctor.save()

        request = factory.get('/', {'medical_subject': m.pk})
        response = retrieve.ApiPublicDoctorProfileGetByMedicalSubject.as_view()(request)
        assert response.status_code == 200, "Able to cal this profile. got {}".format(
            response.status_code
        )
        assert len(response.data) == 1, 'Expected 1. got {}'.format(len(response.data))
        assert 'license_number' not in response.data, 'License number must not be visible'

        request = factory.get('/')
        response = retrieve.ApiPublicDoctorProfileGetByMedicalSubject.as_view()(request)
        assert response.status_code == 400, 'Must fail on bad request. got {}'.format(response.status_code)

    def test_get_private_doctor_by_medical_subject(self):
        # create dummy user
        user = mixer.blend('accounts.Account', user_type=DOCTOR)
        m = mixer.blend('doctors.MedicalSubject')
        doctor = user.base_profile().get_doctor_profile()
        doctor.medical_subject = m
        doctor.save()

        request = factory.get('/', {'medical_subject': m.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByMedicalSubject.as_view()(request)
        assert response.status_code == 200, "Able to cal this profile. got {}".format(
            response.status_code
        )
        assert len(response.data) == 1, 'Expected 1. got {}'.format(len(response.data))
        assert 'license_number' not in response.data, 'License number must not be visible'

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByMedicalSubject.as_view()(request)
        assert response.status_code == 400, 'Must fail on bad request. got {}'.format(response.status_code)

        request = factory.get('/', {'medical_subject': m.pk})
        response = retrieve.ApiPrivateDoctorProfileGetByMedicalSubject.as_view()(request)
        assert response.status_code == 401, 'Must fail on bad request. got {}'.format(response.status_code)
