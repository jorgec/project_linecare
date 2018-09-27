from django.contrib import admin

# Register your models here.
from albums.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'album_type', 'is_public')
    list_filter = ('profile', 'album_type', 'is_public')
    search_fields = ('name', 'profile')


admin.site.register(Album, AlbumAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'album', 'caption')
    list_filter = ('album', 'is_public', 'is_primary')
    search_fields = ('album', 'caption')


admin.site.register(Photo, PhotoAdmin)
