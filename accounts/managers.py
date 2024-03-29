from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from accounts.constants import SUPERADMIN, USER_SUBACCOUNT


class AccountQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class AccountManager(BaseUserManager):
    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def create_user(self, email, username=None, password=None, user_type=None, parent=None):
        email_validator = EmailValidator()
        try:
            email_validator(email)
            if not username:
                username = slugify(email)
            user = self.model(
                username=username,
                email=self.normalize_email(email),
                user_type=user_type,
                parent=parent
            )

            user.set_password(password)
            user.save(using=self._db)
            return user
        except ValidationError:
            return False

    def create_superuser(self, email, password, username=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.user_type = SUPERADMIN
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_sub_user(self, first_name, last_name, parent, user_type=USER_SUBACCOUNT, date_of_birth=None, gender_id=None):
        username = slugify('{} {} {}'.format(first_name, last_name, parent.email))
        username = '{}-{}'.format(username[:32], get_random_string(length=8))
        email = '{}@dummy.linecare.com'.format(username)

        sub_user = self.create_user(
            username=username,
            email=email,
            parent=parent,
            user_type=user_type
        )
        profile = sub_user.base_profile()
        profile.first_name = first_name
        profile.last_name = last_name
        profile.date_of_birth = date_of_birth
        profile.gender_id = gender_id
        profile.save()
        return sub_user
