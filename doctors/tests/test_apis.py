import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer

from doctors.models import DoctorProfile
from doctors.modules.apis import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()

class TestDoctorApi:
    def test_get_doctor_by_pk(self):
        # create dummy account
        user = mixer.blend('accounts.Account')
        profile = user.base_profile()
        doctor = profile.get_doctor_profile()
        doctor.license_number = 'DR85213'
        doctor.year_started = 2010
        doctor.save()

        request =  factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateDoctorProfileGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this profile. got {} doctor_license_number: {}".format(response.status_code, doctor.license_number)
        # assert len(response.data) == 1, 'Expected 1. got {}'.format(len(response.data))