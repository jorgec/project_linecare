import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer
from rest_framework.utils import json

from accounts.constants import USER_TYPES_TO_TEST
from accounts.models import Account
from profiles.constants import SMART
from profiles.models import BaseProfile, ProfileMobtel, Gender
from profiles.modules.apis import retrieve

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestProfileApi:
    def __test_get_public_profile_by_pk(self):
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

        n1 = user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'pk': user.base_profile().pk})
        response = retrieve.ApiPublicGetProfileByPK.as_view()(request)
        assert response.status_code == 200, "Able to call this by profile"
        assert 'date_of_birth' not in json.loads(response.data), "Date of birth must not be visible"
        assert '+639101234567' in json.loads(response.data['mobtels']), "Public mobtel should be listed"
        assert '+639101234569' not in json.loads(response.data['mobtels']), "Private mobtel should not be listed"
        assert '+639101234560' not in json.loads(response.data['mobtels']), "Inactive mobtel should not be listed"

        user.base_profile().edit_mobtel(**{
            'pk': n1.pk,
            'is_active': True
        })
        assert '+639101234560' in json.loads(response.data['mobtels']), "Public mobtel should be listed"

        user.base_profile().delete_mobtel(**{'pk': n1.pk})
        assert '+639101234560' in json.loads(response.data['mobtels']), "Deleted mobtel should not be listed"

        request = factory.get('/')
        response = retrieve.ApiPublicGetProfileByPK.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

        request = factory.get('/', {'pk': 234634})
        response = retrieve.ApiPublicGetProfileByPK.as_view()(request)
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

        n1 = user.base_profile().add_mobtel(**{
            'number': '+63 910 1234560',
            'carrier': SMART,
            'is_public': True,
            'is_primary': False,
            'is_active': False
        })

        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiPublicGetProfileByUsername.as_view()(request)
        data = json.loads(response.data)
        assert response.status_code == 200, "Able to call this profile"
        assert 'date_of_birth' not in data, "Date of birth must not be visible"
        assert '+639101234567' in data['mobtels'], "Public mobtel should be listed"
        assert '+639101234569' not in data['mobtels'], "Private mobtel should not be listed"
        assert '+639101234560' not in data['mobtels'], "Inactive mobtel should not be listed"

        user.base_profile().edit_mobtel('+639101234567',
                                        **{
                                            'number': '+63 987 9876543'
                                        })
        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiPublicGetProfileByUsername.as_view()(request)
        data = json.loads(response.data)
        assert '+639101234560' not in data['mobtels'], "Old number should be gone"
        assert '+639879876543' in data['mobtels'], "Public mobtel should be listed"

