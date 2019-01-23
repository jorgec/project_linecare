import pytest
from faker import Faker

from mixer.backend.django import mixer
import random
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from accounts.modules.api.create import ApiPatientSubAccountCreate
from biometrics.models import BLOOD_TYPE_CHOICES
from profiles.models import Gender

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


from accounts.models import Account


class TestCreateApi:
    user = None

    def test_init(self):
        fake = Faker()
        email = fake.email()
        password = fake.password()

        self.user = Account.objects.create_user(email=email, password=password)
        assert self.user is not None, "Should save an instance"
        assert self.user.base_profile() is not None, "Should have a base_profile()"

    def test_api_subaccount_create(self):
        fake = Faker()

        email = fake.email()
        password = fake.password()

        parent = Account.objects.create_user(email=email, password=password)

        gender = mixer.blend(Gender)
        first_name, last_name = fake.name().split(" ")

        blood_type = 'A+'

        request = factory.post('/', {
            'height': random.randint(100, 300),
            'weight': random.randint(100, 300),
            'blood_type': random.choice(blood_type),
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': fake.date(),
            'gender_id': gender.id,
            'user': parent.id
        })

        response = ApiPatientSubAccountCreate.as_view()(request)
        assert response.status_code == 401, f"Was able to access despite being not logged in: {response.status_code}"

        force_authenticate(request, user=parent)
        response = ApiPatientSubAccountCreate.as_view()(request)

        assert response.status_code == 200, f"Sub user was not created, {response.data}"

        request = factory.post('/', {
            'height': f'{random.randint(2, 9)}\' {random.randint(0, 12)}"',
            'weight': f'{random.randint(100, 300)} lb',
            'blood_type': random.choice(blood_type),
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': fake.date(),
            'gender_id': gender.id,
            'user': parent
        })

        force_authenticate(request, user=parent)
        response = ApiPatientSubAccountCreate.as_view()(request)

        assert response.status_code == 200, f"Sub user was not created, {response.data}"

        request = factory.post('/', {
            'height': 'sadg',
            'weight': f'{random.randint(100, 300)} lb',
            'blood_type': random.choice(blood_type),
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': fake.date(),
            'gender_id': gender.id,
            'user': parent
        })

        force_authenticate(request, user=parent)
        response = ApiPatientSubAccountCreate.as_view()(request)

        assert response.status_code == 400, f"Sub user was not created, {response.data}"

        request = factory.post('/', {
            'height': f'{random.randint(2, 9)}\' {random.randint(0, 12)}"',
            'weight': 'asdasdg',
            'blood_type': random.choice(blood_type),
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': fake.date(),
            'gender_id': gender.id,
            'user': parent
        })

        force_authenticate(request, user=parent)
        response = ApiPatientSubAccountCreate.as_view()(request)

        assert response.status_code == 400, f"Sub user was not created, {response.data}"