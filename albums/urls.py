from django.urls import path
from .modules.api import create, retrieve

urlpatterns = [
    # api

    # create
    path('api/private/upload',
         create.ApiPrivateAlbumPostUploadPhoto.as_view(),
         name='api_private_album_post_upload_photo'),

    # retrieve
    path('api/public/get_by_user',
         retrieve.ApiPublicAlbumsGetByUser.as_view(),
         name='api_public_albums_by_profile'),
    path('api/public/get_album',
         retrieve.ApiPublicAlbumGetByPK.as_view(),
         name='api_public_album_get_by_pk'),
]
