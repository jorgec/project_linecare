from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from accounts.constants import USERNAME_REGEX, USER_TYPE_CHOICES
from accounts.managers import AccountManager
from profiles.models import BaseProfile


class Account(AbstractBaseUser):
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username can only contain alphanumeric characters and the following characters: . -',
                code='Invalid Username'
            )
        ],
        unique=False,

    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=None, null=True, blank=True)
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # NonRelational data
    user_settings = JSONField(default=list)

    # Relationship Fields
    parent = models.ForeignKey("self", null=True, blank=True, related_name="account_children", on_delete=models.CASCADE)

    children = []
    parents = []

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['username']

    def base_profile(self):
        return self.account_profiles.all().first()


    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def settings_set_primary_profile(self):
        settings = self.user_settings


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Account)
def create_base_profile(sender, instance=None, created=False, **kwargs):
    if created:
        BaseProfile.objects.create(user=instance)

