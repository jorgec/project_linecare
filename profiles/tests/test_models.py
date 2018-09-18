import pytest
from mixer.backend.django import mixer

from accounts.models import Account, DOCTOR

pytestmark = pytest.mark.django_db


class TestProfile:

    def test_user_and_profile_creation(self):
        user = Account.objects.create_user(email='test@test.com')
        assert user.user_type is None
        user.user_type = DOCTOR
        user.save()
        assert user.user_type == DOCTOR
        profile = mixer.blend('profiles.BaseProfile', user=user)
        assert profile.pk is not None