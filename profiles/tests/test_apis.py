# TODO
# Retrieve
# - get base profile of user via pk, username, email (public/private) DONE
# - get phone numbers of user via pk, username, email
# - get profiles of all users of type X
# - get profiles of all users of gender X
# - get profile photo
# Create
# - profile of user (constraint: 1 profile only)
# - phone numbers
# Update
# - update profile of user (given pk or email)
# - update phone of user (given pk or email)
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer

from accounts.constants import USER_TYPES_TO_TEST
from accounts.models import Account
from profiles.models import BaseProfile, ProfileMobtel, Gender
from profiles.modules.apis import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestApiView:
    def test_get_profile_by_pk_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        profile = BaseProfile.objects.create(user=user)

        request = factory.get('/', {'pk': profile.user})
        response = retrieve.ApiPublicGetProfileByPK.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

        request = factory.get('/', {'pk': profile.pk})
        response = retrieve.ApiPublicGetProfileByPK.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_pk_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        BaseProfile.objects.create(user=user)

        request = factory.get('/', {'pk': user.pk})
        response = retrieve.ApiPrivateGetProfileByPK.as_view()(request)
        assert response.status_code == 401, "Must not be accessed if not authenticated"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByPK.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByPK.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_username_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        profile = BaseProfile.objects.create(user=user)

        request = factory.get('/')
        response = retrieve.ApiPublicGetProfileByUsername.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'username': profile.user.username})
        response = retrieve.ApiPublicGetProfileByUsername.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_username_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        BaseProfile.objects.create(user=user)

        request = factory.get('/', {'username': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByUsername.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiPrivateGetProfileByUsername.as_view()(request)
        assert response.status_code == 401, "Must not be accessed if not authenticated"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByUsername.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'username': user.username})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByUsername.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_email_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        profile = BaseProfile.objects.create(user=user)

        request = factory.get('/')
        response = retrieve.ApiPublicGetProfileByEmail.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'email': profile.user.email})
        response = retrieve.ApiPublicGetProfileByEmail.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_email_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        BaseProfile.objects.create(user=user)

        request = factory.get('/', {'email': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByEmail.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

        request = factory.get('/', {'email': user.email})
        response = retrieve.ApiPrivateGetProfileByEmail.as_view()(request)
        assert response.status_code == 401, "Must not be accessed if not authenticated"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByEmail.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'email': user.email})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByEmail.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_user_type_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        users = []
        for type in USER_TYPES_TO_TEST:
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    user_type=type[0]
                )
                BaseProfile.objects.create(user=user)

                users.append(user)

        for type in USER_TYPES_TO_TEST:
            request = factory.get('/', {'user_type': type[0]})
            response = retrieve.ApiPublicGetProfileByUserType.as_view()(request)
            assert response.status_code == 200, response.data
            assert len(response.data) == 5, "Expecting {}, got {}".format(len(response.data), len(users))

    def test_get_profile_by_user_type_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        users = []
        for type in USER_TYPES_TO_TEST:
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    user_type=type[0]
                )
                BaseProfile.objects.create(user=user)

                users.append(user)

        for type in USER_TYPES_TO_TEST:
            request = factory.get('/', {'user_type': type[0]})
            force_authenticate(request, user=user)
            response = retrieve.ApiPrivateGetProfileByUserType.as_view()(request)
            assert response.status_code == 200, response.data
            assert len(response.data) == 5, "Expecting {}, got {}".format(len(response.data), len(users))

    def test_get_profile_by_gender_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        gender = mixer.blend('profiles.Gender')
        profile = BaseProfile.objects.create(user=user, gender=gender)

        request = factory.get('/')
        response = retrieve.ApiPublicGetProfileByGender.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'gender': profile.gender})
        response = retrieve.ApiPublicGetProfileByGender.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_by_gender_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        gender = mixer.blend('profiles.Gender')
        profile = BaseProfile.objects.create(user=user, gender=gender)

        request = factory.get('/', {'gender': profile.gender})
        response = retrieve.ApiPrivateGetProfileByGender.as_view()(request)
        assert response.status_code == 401, "Must not be accessed if not authenticated"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByGender.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'gender': user})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateGetProfileByGender.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    def test_get_profile_album(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        # username-profile-photos
        # username-cover-photos

        profile_album = '{}-profile-photos'.format(user.username)
        cover_album = '{}-cover-photos'.format(user.username)

        # check if album was created

        request = factory.get('/', {'album': profile_album})
        response = retrieve.ApiPrivateGetAlbum.as_view()(request)
        assert response.status_code == 200, "Must be accessible"

    # def test_get_profile_photo(self):

    # def test_get_cover_photo(self):
