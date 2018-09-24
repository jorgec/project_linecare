import pytest
from mixer.backend.django import mixer

from accounts.constants import DOCTOR
from accounts.models import Account
from profiles.models import BaseProfile, ProfileMobtel

pytestmark = pytest.mark.django_db


class TestProfile:

    def test_user_and_profile_creation(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profile = BaseProfile(user=user)
        profile.save()
        assert profile.pk is not None, profile.pk

    def test_gender(self):
        obj = mixer.blend('profiles.Gender')
        assert obj.name == str(obj), "__str__ mismatch"

    # Not final
    def test_baseprofile(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.last_name = 'Tester'
        user.first_name = 'Juan'
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profile = BaseProfile(user=user)
        profile.save()
        assert profile.user.get_full_name() == str(profile)

    def test_duplicate_profile(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.last_name = 'Tester'
        user.first_name = 'Juan'
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profile = BaseProfile.objects.create(user=user)
        profile.save()
        profiles = BaseProfile.objects.filter(user=user)
        profile_count = len(profiles)
        assert profile_count == 1, "Should only have 1 profile, got {}".format(profile_count)

