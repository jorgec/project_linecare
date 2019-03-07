import uuid

from django.conf import settings
from django.db import models as models
from django.urls import reverse
from django_extensions.db import fields as extension_fields

from albums.constants import GENERIC_ALBUM_CHOICES, GENERIC_ALBUM, PROFILE_PHOTO_ALBUM, COVER_PHOTO_ALBUM


def photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return 'uploads/profile_photos/{}'.format(
        filename
    )


class Album(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    album_type = models.PositiveIntegerField(choices=GENERIC_ALBUM_CHOICES, default=GENERIC_ALBUM)

    # Relationship Fields
    profile = models.ForeignKey('profiles.BaseProfile', on_delete=models.CASCADE, related_name='profile_albums')

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'profile')

    def __str__(self):
        return self.name

    # auth
    def verify_ownership(self, user):
        return user == self.profile.user

    # utils
    def toggle_privacy(self):
        if self.is_public:
            self.is_public = False
        else:
            self.is_public = True
        self.save()
        return self

    def get_primary_photo(self, return_null=False):
        try:
            return self.album_photos.get(is_primary=True)
        except Photo.DoesNotExist:
            if return_null:
                return None
            else:
                return self.get_null_photo()

    def get_public_photos(self):
        return self.album_photos.filter(is_public=True)

    def get_null_photo(self):
        if self.album_type == PROFILE_PHOTO_ALBUM:
            return f"{settings.STATIC_URL}neo/images/profile-dummy.png"
        elif self.album_type == COVER_PHOTO_ALBUM:
            return f"{settings.STATIC_URL}neo/images/bg-01-01.jpg"
        else:
            return f"{settings.STATIC_URL}neo/images/colors-png/darkgray-1.png"


class Photo(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    photo = models.ImageField(upload_to=photo_upload_path, max_length=512)
    caption = models.TextField(max_length=500, default='')
    is_primary = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    # Relationship Fields
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_photos', null=True, blank=True)

    class Meta:
        ordering = ('-is_primary', '-created',)

    def __str__(self):
        return self.photo.url

    def get_photo(self):
        return f"{settings.MEDIA_URL}{self.photo}"

    def set_primary_photo(self):
        photos_in_album = Photo.objects.filter(album=self.album)
        photos_in_album.update(is_primary=False)
        self.is_primary = True
        self.is_public = True
        self.save()
        return self

    def unset_primary_photo(self):
        self.is_primary = False
        self.save(update_fields=['is_primary'])
        return self

    def toggle_privacy(self):
        if self.is_primary:
            return False
        if self.is_public:
            self.is_public = False
        else:
            self.is_public = True
        self.save()
        return self
