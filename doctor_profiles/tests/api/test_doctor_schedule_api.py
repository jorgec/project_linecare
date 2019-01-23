import json

import pytest
import random
from faker import Faker
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import Account
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution, MedicalInstitutionDoctor
from doctor_profiles.modules.api.medical_institution_doctors_api import ApiMedicalInstitutionDoctorCreate
from doctor_profiles.modules.api.medical_institutions_api import ApiPrivateMedicalInstitutionCreate
from locations.models import Region, Province, City, Country

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()
fake = Faker()


class TestDoctorScheduleApi:

    def test_full_create(self):
        # fixtures
        email = fake.email()
        password = fake.password()
        user = Account.objects.create_user(email=email, password=password)
        assert user is not None, "User was not created"

        doctor = user.create_doctor_profile()
        assert doctor is not None, "Doctor Profile was not created"

        mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert mi_type is not None, "Type was not created"

        country = Country.objects.create(name=fake.name())
        assert country is not None, "Country was not created"

        region = Region.objects.create(
            name=fake.name(),
            country=country
        )
        assert region is not None, "Region was not created"

        province = Province.objects.create(
            name=fake.name(),
            region=region,
            country=country
        )
        assert province is not None, "Province was not created"

        city = City.objects.create(
            name=fake.name(),
            province=province
        )
        assert city is not None, "City was not created"
        # /fixtures

        name = fake.name()
        zip_code = random.randint(1000, 9999)
        address = fake.address()

        form_data = {
            'name': name,
            'region': region.id,
            'province': province.id,
            'city': city.id,
            'zip_code': zip_code,
            'address': address,
            'type': mi_type.id
        }

        request = factory.post('/', form_data)
        force_authenticate(request, user=user)

        response = ApiPrivateMedicalInstitutionCreate.as_view()(request)
        assert response.status_code == 200, f"Medical Institution creation failed: {response.data} {form_data}"

        medical_institution_id = response.data['id']
        medical_institution = MedicalInstitution.objects.get(id=medical_institution_id)
        request = factory.post('/', {
            'doctor': doctor.id,
            'medical_institution': medical_institution.id
        })
        force_authenticate(request, user=user)
        response = ApiMedicalInstitutionDoctorCreate.as_view()(request)
        assert response.status_code == 201, f"Connection between {doctor} and {medical_institution} was not created: {response.data}"

