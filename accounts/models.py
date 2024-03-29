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

from django.apps import apps


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
    user_settings = JSONField(default=dict)

    # unused
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)

    # Relationship Fields
    parent = models.ForeignKey("self", null=True, blank=True, related_name="account_children", on_delete=models.CASCADE)

    children = []
    parents = []

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['username']

    def __str__(self):  # __unicode__ on Python 2
        return self.username

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

    """
    Profile Functions
    """

    def base_profile(self):
        BaseProfile = apps.get_model('profiles.BaseProfile')
        try:
            return BaseProfile.objects.get(
                user=self,
                is_primary=True
            )
        except BaseProfile.DoesNotExist:
            profile = BaseProfile.objects.create(
                user=self,
                is_primary=True
            )
            return profile

    def settings_set_primary_profile(self):
        # TODO
        settings = self.user_settings

    def doctor_profile(self):
        DoctorProfile = apps.get_model('doctor_profiles.DoctorProfile')
        try:
            return DoctorProfile.objects.get(
                user=self,
                is_approved=True
            )
        except DoctorProfile.DoesNotExist:
            return False

    def create_doctor_profile(self):
        DoctorProfile = apps.get_model('doctor_profiles.DoctorProfile')
        profile = DoctorProfile.objects.create(
            user=self
        )
        return profile

    def receptionist_profile(self):
        ReceptionistProfile = apps.get_model('receptionist_profiles.ReceptionistProfile')
        try:
            return ReceptionistProfile.objects.get(
                user=self,
                is_approved=True
            )
        except ReceptionistProfile.DoesNotExist:
            return False

    def create_receptionist_profile(self):
        ReceptionistProfile = apps.get_model('receptionist_profiles.ReceptionistProfile')
        profile = ReceptionistProfile.objects.create(
            user=self
        )
        return profile




@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Account)
def create_base_profile(sender, instance=None, created=False, **kwargs):
    if created:
        BaseProfile.objects.create(user=instance)
