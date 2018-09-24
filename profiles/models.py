from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db import fields as extension_fields

from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models

from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers

SMART = 0
GLOBE = 1
SUN = 2
TNT = 3
TM = 4

MOBTEL_CARRIERS = (
    (SMART, "Smart"),
    (GLOBE, "Globe"),
    (SUN, "Sun Cellular"),
    (TNT, "Talk N Text"),
    (TM, "Touch Mobile"),
)


class Gender(models.Model):
    name = models.CharField(max_length=32)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseProfile(models.Model):
    # Fields
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('accounts.Account', related_name='account_profiles', on_delete=models.CASCADE)

    class Meta:
        ordering = ('user', '-created')

    def __str__(self):
        return self.user.get_full_name()


class ProfileMobtel(models.Model):
    # Fields
    number = PhoneNumberField()
    carrier = models.PositiveSmallIntegerField(choices=MOBTEL_CARRIERS)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    profile = models.ForeignKey(BaseProfile, related_name='profile_mobtels', on_delete=models.CASCADE)

    class Meta:
        ordering = ('profile', '-created')

    def __str__(self):
        return '{}: {}'.format(
            self.profile,
            self.number
        )

    def is_valid(self):
        return phonenumbers.is_valid_number(self)