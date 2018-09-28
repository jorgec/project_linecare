import json

import pytest
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from albums.models import Album
from albums.modules.api import retrieve

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

    def test_public_album_get_by_user(self):
        user = mixer.blend('accounts.Account')

        request = factory.get('/', {'user': user.pk})
        response = retrieve.ApiPublicAlbumsGetByUser.as_view()(request)
        assert response.status_code == 200, "Able to access. got {}".format(response.status_code)

        request = factory.get('/', {'username': 'qwerty'})
        response = retrieve.ApiPublicAlbumsGetByUser.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)


    def test_public_album_get_by_pk(self):
        # create dummy user
        user = mixer.blend('accounts.Account')

        Album.objects.create(
            name='Sample Album',
            is_public=False,
            album_type=76930
        )

        # add photo function

        album = user.base_profile().get_albums().first()

        request = factory.get('/', {'pk': album.pk})
        response = retrieve.ApiPublicAlbumGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to access. got {}".format(response.status_code)
        assert len(user.base_profile().get_albums()) == 2, "Expected 2. got {}".format(len(user.base_profile().get_albums))
        assert len(user.base_profile().get_all_albums()) == 3, "Expected 3. got {}".format(len(user.base_profile().get_albums))
        assert 'Sample Album' not in response.data, "Album must not be visible"
        assert 'Photo name here' in response.data['photos'], "Must be visible"

        request = factory.get('/', {'pk': 10674})
        response = retrieve.ApiPublicAlbumGetByPK.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)


    def test_private_album_get_albums(self):
        # create dummy user
        user = mixer.blend('accounts.Account')

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 200, "Able to access. got {}".format(response.status_code)
        assert user.base_profile().get_profile_album().slug == '{}-profile-photos'.format(
            user.username), "Expected {}-profile-photos. got {}".format(
            user.username, user.base_profile().get_profile_album().slug)

        assert user.base_profile().get_cover_album().slug == '{}-cover-photos'.format(
            user.username), "Expected {}-cover-photos. got {}".format(
            user.username, user.base_profile().get_cover_album())

        request = factory.get('/')
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 401, "Must fail for unauthorized user. got {}".format(response.status_code)

        request = factory.get('/', {'username': 'qwerty'})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)