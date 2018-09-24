import pytest
from django.db import IntegrityError, transaction
from mixer.backend.django import mixer

from accounts.constants import DOCTOR
from accounts.models import Account
from profiles.constants import SMART
from profiles.models import BaseProfile, ProfileMobtel

pytestmark = pytest.mark.django_db


class TestProfile:

    def test_user_and_profile_creation(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profile = BaseProfile.objects.create(user=user)
        assert profile.pk is not None, profile.pk

    def test_gender(self):
        obj = mixer.blend('profiles.Gender')
        assert obj.name == str(obj), "__str__ mismatch"

    def test_baseprofile(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.last_name = 'Tester'
        user.first_name = 'Juan'
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR

        profile = BaseProfile.objects.get(user=user)
        assert str(user.username) == str(profile.user), "username {} must match with user profile {}".format(user.username, profile.user)

        profile = user.base_profile()
        assert profile.user.get_full_name() == str(profile), "full name: {}".format(profile.user.get_full_name())

    def test_duplicate_profile(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.last_name = 'Tester'
        user.first_name = 'Juan'
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profiles = BaseProfile.objects.filter(user=user)
        profile_count = len(profiles)
        assert profile_count == 1, "Should only have 1 profile, got {}".format(profile_count)


    def test_mobtels(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.last_name = 'Tester'
        user.first_name = 'Juan'
        user.user_type = DOCTOR
        user.save()

        n1 = ProfileMobtel.objects.create(**{
            'number': '+63 910 1234567',
            'carrier': SMART,
            'profile': user.base_profile(),
            'is_primary': False
        })
        primary_number = user.base_profile().get_primary_number()
        assert primary_number is None, "Expected 'None', got {}".format(primary_number)
        n1.is_primary = True
        n1.save()
        primary_number = user.base_profile().get_primary_number()
        assert str(primary_number) == '+639101234567', "Expected +639101234567, got {}".format(primary_number)
        assert user.base_profile().get_primary_public_number() is None, "Expected empty queryset, got {}".format(user.base_profile().get_primary_public_number())
        n1.is_private = False
        n1.save()
        assert str(user.base_profile().get_primary_public_number()) == '+639101234567', "Expected +639101234567, got {}".format(
            user.base_profile().get_primary_public_number())

        with pytest.raises(IntegrityError) as excinfo:
            with transaction.atomic():
                n2 = ProfileMobtel.objects.create(**{
                    'number': '+63 910 1234567',
                    'carrier': SMART,
                    'profile': user.base_profile(),
                    'is_primary': False
                })
                assert 'UNIQUE constraint failed' in str(excinfo.value)

        n2 = ProfileMobtel.objects.create(**{
            'number': '+63 910 1234568',
            'carrier': SMART,
            'profile': user.base_profile(),
            'is_primary': False
        })

        assert user.base_profile().get_all_numbers().count() == 2, "Expected 2, got {}".format(user.base_profile().get_all_numbers().count())

        n3 = ProfileMobtel.objects.create(**{
            'number': '+63 910 1234569',
            'carrier': SMART,
            'profile': user.base_profile(),
            'is_primary': False,
            'is_private': False
        })

        assert user.base_profile().get_public_numbers().count() == 2, "Expected 2, got {}".format(user.base_profile().get_public_numbers().count())