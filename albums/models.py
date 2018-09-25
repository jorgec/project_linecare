import uuid

from django.db import models as models
from django.urls import reverse
from django_extensions.db import fields as extension_fields

from albums.constants import GENERIC_ALBUM_CHOICES, GENERIC_ALBUM


def photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return 'uploads/{}/{}/{}'.format(
        instance.profile.user.pk,
        instance.album.slug,
        filename
    )


class Album(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(max_length=500)
    is_public = models.BooleanField(default=True)
    album_type = models.PositiveIntegerField(choices=GENERIC_ALBUM_CHOICES, default=GENERIC_ALBUM)

    # Relationship Fields
    profile = models.ForeignKey('profiles.BaseProfile', on_delete=models.CASCADE, related_name='profile_albums')

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'profile')

    def __str__(self):
        return self.name

    def get_primary_photo(self):
        try:
            return self.album_photos.get(is_primary=True)
        except Photo.DoesNotExist:
            return None


class Photo(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    photo = models.ImageField(upload_to=photo_upload_path)
    caption = models.TextField(max_length=500)
    is_primary = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    # Relationship Fields
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_photos')

    class Meta:
        ordering = ('-is_primary', '-created',)

    def __str__(self):
        return self.photo.url

    def set_primary_photo(self):
        photos_in_album = Photo.objects.filter(album=self.album)
        photos_in_album.update(is_primary=False)
        self.is_primary = True
        self, is_public = True
        self.save()
