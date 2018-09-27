import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer
from rest_framework.utils import json

from accounts.constants import USER_TYPES_TO_TEST
from profiles.constants import SMART, GLOBE
from profiles.modules.api import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestProfileApi:
    def test_get_public_mobtels_by_pk(self):
        # create dummy account
        user = mixer.blend('accounts.Account')
        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'is_public': True,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'is_public': False,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'pk': user.pk})
        response = retrieve.ApiPublicProfileGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this by profile"
        assert 'date_of_birth' not in response.data['mobtels'], "Date of birth must not be visible"
        assert '+639101234567' in response.data['mobtels'], "Public mobtel should be listed"
        assert '+639101234569' not in response.data['mobtels'], "Private mobtel should not be listed"
        assert '+639101234560' not in response.data['mobtels'], "Inactive mobtel should not be listed"

        request = factory.get('/')
        response = retrieve.ApiPublicProfileGetByPK.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'pk': 234634})
        response = retrieve.ApiPublicProfileGetByPK.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

    def test_get_public_mobtels_by_username(self):
        # create dummy account
        user = mixer.blend('accounts.Account')

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'is_public': True,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'is_public': False,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiPublicProfileGetByUsername.as_view()(request)
        assert response.status_code == 200, "Able to call this profile"
        assert 'date_of_birth' not in response.data, "Date of birth must not be visible"
        assert '+639101234567' in response.data['mobtels'], "Public mobtel should be listed"
        assert '+639101234569' not in response.data['mobtels'], "Private mobtel should not be listed"
        assert '+639101234560' not in response.data['mobtels'], "Inactive mobtel should not be listed"

        request = factory.get('/')
        response = retrieve.ApiPublicProfileGetByUsername.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'username': 'qwerty'})
        response = retrieve.ApiPublicProfileGetByUsername.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

    def test_public_mobtels_by_user_type(self):
        #create dummy user
        user = mixer.blend('accounts.Account', user_type=USER_TYPES_TO_TEST[0][0])
        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'is_public': True,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234568',
            'carrier': SMART,
            'is_public': False,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'user_type': user.user_type})
        response = retrieve.ApiPublicProfileGetByUserType.as_view()(request)
        assert response.status_code == 200, "Able to access profiles"

        request = factory.get('/')
        response = retrieve.ApiPublicProfileGetByUserType.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request 400"

        request = factory.get('/', {'user_type': 12345})
        response = retrieve.ApiPublicProfileGetByUserType.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

    def test_private_mobtels_by_pk(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'is_public': True,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234568',
            'carrier': SMART,
            'is_public': False,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this profile"
        assert 'date_of_birth' in response.data, "Date of birth must be visible"
        assert '+639101234567' in response.data['mobtels'], "Public mobtel should be listed"
        assert '+639101234568' in response.data['mobtels'], "Private mobtel should be listed"
        assert '+639101234569' in response.data['mobtels'], "Inactive mobtel should be listed"
        assert len(response.data['mobtels']) == 3, "Expected number of mobtels 3. got {}".format(len(response.data['mobtels']))

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True
        })

        user.base_profile().edit_mobtel('+639101234569', **{
            'number': '+63 910 1234563',
            'is_public': True,
            'carrier': GLOBE
        })
        request = factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByPK.as_view()(request)
        assert '+639101234569' not in response.data['mobtels'], "Old number should be gone"
        assert '+639101234563' in response.data['mobtels'], "Public mobtel should be listed"
        assert len(response.data['mobtels']) == 4, "Expected number of mobtels 4. got {}".format(len(response.data['mobtels']))

        user.base_profile().delete_mobtel('+639101234563')
        request = factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByPK.as_view()(request)
        assert '+639101234563' not in response.data['mobtels'], "Deleted mobtel should not be listed"

        request = factory.get('/', {'pk': user.pk})
        response = retrieve.ApiPrivateProfileGetByPK.as_view()(request)
        assert  response.status_code == 401, "Must fail for unauthenticated user"

        request = factory.get('/', {'pk': 45621})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByPK.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"

    def test_private_mobtels_by_username(self):
        # create dummy user
        user = mixer.blend('accounts.Account')
        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'is_public': True,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234568',
            'carrier': SMART,
            'is_public': False,
            'is_primary': True
        })

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'username': user.username})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByUsername.as_view()(request)
        assert response.status_code == 200, "Able to call this profile"
        assert 'date_of_birth' in response.data, "Date of birth must be visible"
        assert '+639101234567' in response.data['mobtels'], "Public mobtel should be listed"
        assert '+639101234568' in response.data['mobtels'], "Private mobtel should be listed"
        assert '+639101234569' in response.data['mobtels'], "Inactive mobtel should be listed"
        assert len(response.data['mobtels']) == 3, "Expected number of mobtels 3. got {}".format(len(response.data['mobtels']))

        user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True
        })

        user.base_profile().edit_mobtel('+639101234569', **{
            'number': '+63 910 1234563',
            'is_public': True,
            'carrier': GLOBE
        })
        request = factory.get('/', {'username': user.username})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByUsername.as_view()(request)
        assert '+639101234569' not in response.data['mobtels'], "Old number should be gone"
        assert '+639101234563' in response.data['mobtels'], "Public mobtel should be listed"
        assert len(response.data['mobtels']) == 4, "Expected number of motels 4. got {}".format(len(response.data['mobtels']))

        user.base_profile().delete_mobtel('+639101234563')
        request = factory.get('/', {'username': user.username})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByUsername.as_view()(request)
        assert '+639101234563' not in response.data['mobtels'], "Deleted mobtel should not be listed"

        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiPrivateProfileGetByUsername.as_view()(request)
        assert response.status_code == 401, "Must fail for unauthenticated user"

        request = factory.get('/', {'username': 45621})
        force_authenticate(request, user=user)
        response = retrieve.ApiPrivateProfileGetByUsername.as_view()(request)
        assert response.status_code == 404, "Must fail on bad request"