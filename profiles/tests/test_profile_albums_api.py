import tempfile

import pytest
from django.conf import settings
from faker import Faker
from django.db import IntegrityError, transaction
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APITestCase, APIClient

from accounts.models import Account
from albums.modules.api.create import ApiPrivateAlbumCreate
from profiles.models import BaseProfile

pytestmark = pytest.mark.django_db
fake = Faker()
factory = APIRequestFactory()


class TestProfileAlbumsApi:
    profile1 = None
    profile2 = None
    profile3 = None

    def setUp(self):
        email = fake.email()
        password = 'asdf1234'
        user = Account.objects.create_user(email=email, password=password)
        self.profile1 = user.base_profile()
        assert self.profile1 is not None, "Profile 1 not created"

        email = fake.email()
        password = 'asdf1234'
        user = Account.objects.create_user(email=email, password=password)
        self.profile2 = user.base_profile()
        assert self.profile2 is not None, "Profile 2 not created"

        email = fake.email()
        password = 'asdf1234'
        user = Account.objects.create_user(email=email, password=password)
        self.profile3 = user.base_profile()
        assert self.profile3 is not None, "Profile 3 not created"

    def test_album_create_unauthorized(self):
        self.setUp()

        form_data = {
            'name': fake.name(),
            'is_public': True
        }

        request = factory.post('/', form_data)
        response = ApiPrivateAlbumCreate.as_view()(request)
        assert response.status_code == 401, f"Album was created from {form_data}: {response.data}; expecting 401 fot {response.status_code}"

    def test_album_create(self):
        self.setUp()
        album_name = fake.name()
        form_data = {
            'name': album_name,
            'is_public': True
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=self.profile1.user)
        response = ApiPrivateAlbumCreate.as_view()(request)
        assert response.status_code == 200, f"Album was not created from {form_data}: {response.data}"
        assert response.data.get('name') == album_name, f"Expecting {album_name}, got {response.data.get('name')}"
        assert response.data.get('is_public') is True, f"Expecting True, got {response.data.get('is_public')}"


class TestProfileUploadPhotoTestCase(APITestCase):
    profile1 = None

    def setUp(self):
        email = fake.email()
        password = 'asdf1234'
        user = Account.objects.create_user(email=email, password=password)
        self.profile1 = user.base_profile()
        assert self.profile1 is not None, "Profile 1 not created"

        settings.MEDIA_ROOT = tempfile.mkdtemp()

