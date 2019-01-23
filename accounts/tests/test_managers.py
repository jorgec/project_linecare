import pytest
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from mixer.backend.django import mixer
from django.contrib.auth import authenticate
from faker import Faker

from accounts.constants import SUPERADMIN
from accounts.models import Account

pytestmark = pytest.mark.django_db

class TestAccountManager:
    user = None
    def test_init(self):
        fake = Faker()
        email = fake.email()
        password = fake.password()

        self.user = Account.objects.create_user(email=email, password=password)
        assert self.user is not None, "Should save an instance"
        assert self.user.base_profile() is not None, "Should have a base_profile()"

    def test_superuser(self):
        su = Account.objects.create_superuser(email='su@test.local', password='cdrw2006$$', username='sutest')
        assert su is not None, "User was not created"
        assert su.user_type == SUPERADMIN, f"{su} is not a superadmin but of type {su.user_type}"
        assert su.is_admin, f"{su} is not is_admin()"

    def test_sub_user(self):
        fake = Faker()

        email = fake.email()
        password = fake.password()

        parent = Account.objects.create_user(email=email, password=password)

        first_name, last_name = fake.name().split(" ")
        subuser = Account.objects.create_sub_user(first_name=first_name, last_name=last_name, parent=parent, date_of_birth='1980-01-07')
        base_username = slugify('{} {} {}'.format(first_name, last_name, parent.email))
        username = '{}-{}'.format(base_username[:32], get_random_string(length=8))
        email = '{}@dummy.linecare.com'.format(username)
        
        assert subuser.username[:-8] == username[:-8], f"Unexpected username; got {subuser.username} instead of {username}"
        assert subuser.base_profile().first_name == first_name, f"Unexpected first name; got {subuser.base_profile().first_name} instead of {first_name}"
        assert subuser.base_profile().last_name == last_name, f"Unexpected last name; got {subuser.base_profile().last_name} instead of {last_name}"