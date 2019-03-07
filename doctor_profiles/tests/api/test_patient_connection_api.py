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

