import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer

from accounts.constants import USER_TYPES_TO_TEST
from accounts.models import Account
from profiles.models import BaseProfile, ProfileMobtel, Gender
from profiles.modules.apis import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestProfileApi:
    def test_get_profile_by_pk_public(self):
        pass

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
