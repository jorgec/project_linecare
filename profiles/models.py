import phonenumbers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields
from phonenumber_field.modelfields import PhoneNumberField

from accounts.constants import DOCTOR, USER
from albums.constants import PROFILE_PHOTO_ALBUM, COVER_PHOTO_ALBUM
from albums.models import Album
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

    objects = BaseProfileManager()

    class Meta:
        ordering = ('user', '-created')

    def __str__(self):
        return self.user.get_full_name()

    def get_public_numbers(self):
        return self.profile_mobtels.filter(is_public=True, is_active=True)

    def get_all_numbers(self):
        return self.profile_mobtels.all()

    def get_primary_public_number(self):
        return self.profile_mobtels.filter(is_primary=True, is_active=True, is_public=True).first()

    def get_primary_number(self):
        return self.profile_mobtels.filter(is_primary=True, is_active=True).first()

    # Media
    def get_albums(self):
        return self.profile_albums.filter(is_public=True)

    def get_private_albums(self):
        return self.profile_albums.filter(is_public=False)

    def get_all_albums(self):
        return self.profile_albums.all()

    def get_profile_album(self):
        try:
            album = self.profile_albums.get(album_type=PROFILE_PHOTO_ALBUM)
            return album
        except:
            return None

    def get_cover_album(self):
        try:
            album = self.profile_albums.get(album_type=COVER_PHOTO_ALBUM)
            return album
        except:
            return None

    def get_profile_photo(self):
        album = self.get_profile_album()
        if album:
            return album.get_primary_photo()
        return None

    def get_cover_photo(self):
        album = self.get_cover_album()
        if album:
            return album.get_primary_photo()
        return None


class ProfileMobtel(models.Model):
    # Fields
    number = PhoneNumberField(unique=True)
    carrier = models.PositiveSmallIntegerField(choices=MOBTEL_CARRIERS)
    is_public = models.BooleanField(default=False)
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


@receiver(post_save, sender=BaseProfile)
def create_generic_albums(sender, instance=None, created=False, **kwargs):
    if created:
        Album.objects.create(**{
            'name': '{} Profile Photos'.format(instance.user.username),
            'description': 'Profile photos',
            'profile': instance,
            'album_type': PROFILE_PHOTO_ALBUM
        })

        Album.objects.create(**{
            'name': '{} Cover Photos'.format(instance.user.username),
            'description': 'Cover photos',
            'profile': instance,
            'album_type': COVER_PHOTO_ALBUM
        })
