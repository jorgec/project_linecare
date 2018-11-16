import pytest
from mixer.backend.django import mixer
from django.contrib.auth import authenticate

pytestmark = pytest.mark.django_db


class TestAccount:
    def test_init(self):
        obj = mixer.blend('accounts.Account')
        assert obj.pk is not None, "Should save an instance"

    def test_str(self):
        obj = mixer.blend('accounts.Account')
        assert obj.username == str(obj), "__str__ mismatch"

    def test_blank_username(self):
        obj = mixer.blend('accounts.Account', username='')
        assert obj is not True, "Username can't be blank"

    def test_blank_email(self):
        obj = mixer.blend('accounts.Account', email='')
        assert obj is not True, "Email can't be blank"

    def test_password(self):
        obj = mixer.blend('accounts.Account', email='juantester@asdg.com')
        obj.set_password("asdf1234")
        obj.save()

        result = authenticate(email='juantester@asdg.com', password='asdf1234')

        assert result is not None, "Can't authenticate!"

    def test_perm(self):
        obj = mixer.blend('accounts.Account')
        assert obj.has_perm(perm=None) is True, "Permission error"

    def test_module_perm(self):
        obj = mixer.blend('accounts.Account')
        assert obj.has_module_perms(app_label=None) is True, "Permission error"

    def test_is_staff(self):
        obj = mixer.blend('accounts.Account')
        assert obj.is_staff == obj.is_admin, "Admin/staff mismatch"


