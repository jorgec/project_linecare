import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer
from rest_framework.utils import json

from accounts.constants import USER_TYPES_TO_TEST
from profiles.constants import SMART, GLOBE
from profiles.modules.api import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()

