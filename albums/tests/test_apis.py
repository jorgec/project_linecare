import json

import pytest
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from albums.models import Album, Photo
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

        Album.objects.create(
            name='Sample Album',
            description='This is a sentence',
            is_public=False,
            album_type=76930,
            profile=user.base_profile()
        )

        request = factory.get('/', {'user': user.pk})
        response = retrieve.ApiPublicAlbumsGetByUser.as_view()(request)
        assert response.status_code == 200, "Able to access. got {}".format(response.status_code)
        assert user.base_profile().get_albums().count() == 2, "Expected 2. got {}".format(user.base_profile.get_albums().count())

        request = factory.get('/', {'username': 'qwerty'})
        response = retrieve.ApiPublicAlbumsGetByUser.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)


    def test_public_album_get_by_pk(self):
        # create dummy user
        user = mixer.blend('accounts.Account')

        album = Album.objects.create(
            name='Sample Album',
            description='This is a sentence',
            is_public=True,
            album_type=76930,
            profile = user.base_profile()
        )

        Photo.objects.create(photo='Desktop', caption='Test image 1', is_primary=True, album=album)
        Photo.objects.create(photo='Downloads', caption='Test image 2', is_primary=False, album=album)

        request = factory.get('/', {'album': album.pk})
        response = retrieve.ApiPublicAlbumGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to access. got {} {}".format(response.status_code, album.pk)
        assert user.base_profile().get_albums().count() == 3, "Expected 3. got {}".format(user.base_profile().get_albums().count())
        assert len(response.data['photos']) == 2, "Expected 2. got {}".format(len(response.data['photos']))
        assert '/media/Downloads' in response.data['photos'], "Photo must be visible. got {}".format(response.data['photos'])
        assert '/media/Test' not in response.data['photos'], "Photo must be visible. got {}".format(response.data['photos'])

        request = factory.get('/', {'album': 10674})
        response = retrieve.ApiPublicAlbumGetByPK.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)


    def test_private_album_get_albums(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        u1 = mixer.blend('accounts.Account')
        Album.objects.create(
            name='Sample Album',
            description='This is a sentence',
            is_public=True,
            album_type=76930,
            profile=user.base_profile()
        )

        Album.objects.create(
            name='U1 Album',
            description='This is a sentence',
            is_public=True,
            album_type=76930,
            profile=u1.base_profile()
        )

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 200, "Able to access. got {}".format(response.status_code)
        assert len(response.data) == 3, "Expected 3. got {}".format(len(response.data))

        request = factory.get('/')
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 401, "Must fail for unauthorized user. got {}".format(response.status_code)

        request = factory.get('/', {'username': 'qwerty'})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateAlbumGetAlbums.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request. got {}".format(response.status_code)