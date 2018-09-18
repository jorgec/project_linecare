import pytest
from mixer.backend.django import mixer

from accounts.models import Account, DOCTOR
from profiles.models import BaseProfile

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