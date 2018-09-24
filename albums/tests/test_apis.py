import json

import pytest
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class TestAlbumApi:
    def test_generic_albums(self):
        user = mixer.blend('accounts.Account')

        assert user.base_profile().get_profile_album().slug == '{}-profile-photos'.format(
            user.username), "Expected '{}-profile-photos', got {}".format(
            user.username, user.base_profile().get_profile_album().slug)
        assert user.base_profile().get_cover_album().slug == '{}-cover-photos'.format(
            user.username), "Expected '{}-cover-photos', got {}".format(
            user.username, user.base_profile().get_cover_album().slug)

        assert user.base_profile().get_albums().count() == 2, "Expected 2, got {}".format(
            user.base_profile().get_albums().count())

        assert user.base_profile().get_private_albums().count() == 0, "Expected 0, got {}".format(
            user.base_profile().get_albums().count())

        assert user.base_profile().get_all_albums().count() == 2, "Expected 2, got {}".format(
            user.base_profile().get_all_albums().count())

        assert user.base_profile().get_profile_photo() is None, "Expected none"
        assert user.base_profile().get_cover_photo() is None, "Expected none"