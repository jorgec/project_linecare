import phonenumbers
from django.db import models
from django_extensions.db import fields as extension_fields
from phonenumber_field.modelfields import PhoneNumberField

from accounts.constants import DOCTOR, USER
from profiles.constants import MOBTEL_CARRIERS


class Gender(models.Model):
    name = models.CharField(max_length=32)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseProfileQuerySet(models.QuerySet):
    def doctors(self):
        return self.user.filter(user_type=DOCTOR)

    def users(self):
        return self.user.filter(user_type=USER)


class BaseProfileManager(models.Manager):
    def get_queryset(self):
        return BaseProfileQuerySet(self.model, using=self._db)

    def doctors(self):
        return self.get_queryset().doctors()

    def users(self):
        return self.get_queryset().users

    def create(self, *args, **kwargs):
        try:
            user = BaseProfile.objects.get(user=kwargs['user'])
            return user
        except BaseProfile.DoesNotExist:
            return super(BaseProfileManager, self).create(*args, **kwargs)


class BaseProfile(models.Model):
    # Fields
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('accounts.Account', related_name='account_profiles', on_delete=models.CASCADE)
    # album = models.ForeignKey('albums.Album', related_name='profile_albums', on_delete=models.CASCADE)

    objects = BaseProfileManager()

    class Meta:
        ordering = ('user', '-created')

    def __str__(self):
        return self.user.get_full_name()

    def get_public_numbers(self):
        return self.profile_mobtels.filter(is_private=False, is_active=True)

    def get_all_numbers(self):
        return self.profile_mobtels.all()

    def get_primary_public_number(self):
        return self.profile_mobtels.filter(is_primary=True, is_active=True, is_private=False).first()

    def get_primary_number(self):
        return self.profile_mobtels.filter(is_primary=True, is_active=True).first()


class ProfileMobtel(models.Model):
    # Fields
    number = PhoneNumberField(unique=True)
    carrier = models.PositiveSmallIntegerField(choices=MOBTEL_CARRIERS)
    is_private = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    profile = models.ForeignKey(BaseProfile, related_name='profile_mobtels', on_delete=models.CASCADE)

    class Meta:
        ordering = ('profile', '-created')

    def __str__(self):
        return '{}'.format(
            self.number
        )

    def is_valid(self):
        return phonenumbers.is_valid_number(self)
