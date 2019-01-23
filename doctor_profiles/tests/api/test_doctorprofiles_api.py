import pytest
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from mixer.backend.django import mixer
from rest_framework.utils import json

from accounts.models import Account
from doctor_profiles.modules.api.doctor_profile_api import ApiPrivateDoctorProfileCreate

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()
client = APIClient()

from doctor_profiles.modules.api import medical_degrees_api as md


class TestDoctorProfileApi:
    user = None
    profile = None
    token = None

    def test_init(self):
        self.user = mixer.blend('accounts.Account')
        assert self.user is not None, "No user created"

        self.token = Token.objects.get(user_id=self.user.pk)
        assert self.token is not None, f"No token created for {self.user}"

        self.profile = self.user.create_doctor_profile()
        assert self.profile is not None, f"No doctor profile created for {self.user}"

    """ Medical Degrees """

    def test_medical_degree_create(self):
        self.test_init()

        request = factory.post('/', json.dumps({
            'name': 'Medical Doctor',
            'abbreviation': 'MD'
        }), content_type='application/json')
        force_authenticate(request, user=self.user)

        response = md.ApiPrivateMedicalDegreeCreate.as_view()(request)

        assert response.status_code == 201, f"Response: {response.data}; Code: {response.status_code}"


    def test_create_doctor_profile(self):
        fake = Faker()
        email = fake.email()
        password = fake.password()
        user = Account.objects.create_user(email=email, password=password)

        request = factory.get('/')
        force_authenticate(request, user=user)

        response = ApiPrivateDoctorProfileCreate.as_view()(request)
        assert response.status_code == 405, f"Expected 405, got {response.status_code}"

        request = factory.post('/')
        force_authenticate(request, user=user)

        response = ApiPrivateDoctorProfileCreate.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        user.create_doctor_profile()

        request = factory.post('/')
        force_authenticate(request, user=user)

        response = ApiPrivateDoctorProfileCreate.as_view()(request)
        assert str(user.doctor_profile()) == response.data['doctor_name'], f"Expected {user.doctor_profile()}, got {response.data.doctor_name}"
