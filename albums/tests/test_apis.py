import json

import pytest
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from albums.models import Album, Photo
from albums.modules.api import retrieve

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()
