import phonenumbers
from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

from albums.constants import PROFILE_PHOTO_ALBUM, COVER_PHOTO_ALBUM
from albums.models import Album
from profiles.constants import PHONE_NAME_CHOICES, PHONE_CARRIERS
from profiles.managers import BaseProfileManager


class Gender(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseProfile(models.Model):
    # Fields
    first_name = models.CharField(max_length=32, blank=True, null=True, default='')
    middle_name = models.CharField(max_length=32, blank=True, null=True, default='')
    last_name = models.CharField(max_length=32, blank=True, null=True, default='')

    date_of_birth = models.DateField(default=None, blank=True, null=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('accounts.Account', related_name='account_profiles', on_delete=models.CASCADE)

    is_fresh = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)

    metadata = JSONField(default=dict, null=True, blank=True)

    objects = BaseProfileManager()

    class Meta:
        ordering = ('user', '-created')

    def __str__(self):
        return self.get_full_name()

    def as_html(self):
        html = f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Full Name</span><span class='kv-value'>{self.get_full_name()}</p>" \
            f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Sex</span><span class='kv-value'>{self.gender}</p>" \
            f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Date of Birth</span><span class='kv-value'>{self.date_of_birth}</p>"
        return html

    def get_casual_name(self):
        if self.first_name != '':
            return self.first_name
        return 'friend'

    def get_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{} {}'.format(
                self.first_name, self.last_name
            )
        else:
            if self.user.username is not None:
                return self.user.username
            return self.user.email

    def get_full_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{}, {}'.format(
                self.last_name, self.first_name
            )
        else:
            if self.user.username is not None:
                return self.user.username
            return self.user.email

    # phones
    def get_public_phones(self):
        return self.profile_phones.filter(is_public=True, is_active=True)

    def get_all_phones(self):
        return self.profile_phones.all()

    def get_primary_public_phone(self):
        return self.profile_phones.filter(is_primary=True, is_active=True, is_public=True).first()

    def get_primary_phone(self):
        return self.profile_phones.filter(is_primary=True, is_active=True).first()

    def add_phone(self, **kwargs):
        kwargs['profile'] = self
        return ProfilePhone.objects.create(**kwargs)

    def edit_phone(self, phone, **kwargs):
        """
        :param phone: Mobile number
        :type phone: String
        """
        try:
            profile_phone = ProfilePhone.objects.filter(profile=self, number=phone)
            profile_phone.update(**kwargs)
            return profile_phone
        except ProfilePhone.DoesNotExist:
            return False

    def delete_phone(self, phone=None):
        if not phone:
            return False

        try:
            profile_phone = ProfilePhone.objects.get(profile=self, number=phone)
            profile_phone.delete()
            return True
        except ProfilePhone.DoesNotExist:
            return False

    def set_as_primary_phone(self, phone=None):
        if not phone:
            return False

        try:
            profile_phone = ProfilePhone.objects.get(profile=self, number=phone)
            ProfilePhone.objects.filter(profile=self).update(is_primary=False)
            profile_phone.is_primary = True
            profile_phone.save()
            return True
        except ProfilePhone.DoesNotExist:
            return False

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

    def get_profile_photo(self, return_null=False):
        album = self.get_profile_album()
        if album:
            return album.get_primary_photo(return_null)
        return None

    def get_profile_photo_url(self):
        photo = self.get_profile_photo(return_null=True)
        if photo:
            return photo.photo.url
        return f"{settings.STATIC_URL}neo/images/profile-dummy.png"

    def get_cover_photo(self):
        album = self.get_cover_album()
        if album:
            return album.get_primary_photo()
        return None

    # Biometrics
    def get_biometrics(self):
        try:
            return self.profile_biometrics
        except ObjectDoesNotExist:
            return None

    """ appointments """

    def appointment_notifications(self):
        try:
            return self.metadata['notifiers']
        except KeyError:
            self.metadata['notifiers'] = []
            return []

    def update_appointment_notifications(self, data):
        notifs = self.appointment_notifications()
        notifs.append(data)
        notifs.reverse()
        self.metadata['notifiers'] = notifs
        self.save(update_fields=['metadata'])
        return self.appointment_notifications()

    def clear_appointment_notifications(self):
        self.metadata['notifiers'] = []
        self.save(update_fields=['metadata'])
        return []

    def create_appointment(
            self,
            *,
            doctor_id,
            medical_institution_id,
            day,
            time_start,
            time_end,
            schedule_choice='first_available',
            appointment_type='checkup',
            force_schedule=False

    ):
        PatientAppointment = apps.get_model('doctor_profiles.PatientAppointment')

        result, appointment, status_code = PatientAppointment.objects.create(
            patient_id=self.id,
            doctor_id=doctor_id,
            medical_institution_id=medical_institution_id,
            appointment_day=day,
            preferred_time_start=time_start,
            preferred_time_end=time_end,
            schedule_choice=schedule_choice,
            force_schedule=force_schedule,
            appointment_type=appointment_type
        )

        return result, appointment, status_code


""" /appointments """


class ProfilePhone(models.Model):
    # Fields
    name = models.CharField(max_length=20, choices=PHONE_NAME_CHOICES, default='Mobile', blank=True, null=True)
    carrier = models.PositiveSmallIntegerField(choices=PHONE_CARRIERS, blank=True, null=True)
    number = PhoneNumberField(unique=True)
    is_public = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    profile = models.ForeignKey(BaseProfile, related_name='profile_phones', on_delete=models.CASCADE)

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
            'name': 'Profile Photos',
            'description': 'Profile photos',
            'profile': instance,
            'album_type': PROFILE_PHOTO_ALBUM
        })

        Album.objects.create(**{
            'name': 'Cover Photos',
            'description': 'Cover photos',
            'profile': instance,
            'album_type': COVER_PHOTO_ALBUM
        })
