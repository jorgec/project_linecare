from django.urls import path
from .modules.api import create, retrieve, update

urlpatterns = [
    # api

    # create
    path('api/private/create',
         create.ApiPrivateAlbumCreate.as_view(),
         name='api_private_album_create'),
    # path('api/private/upload',
    #      create.ApiPrivateAlbumPostUploadPhoto.as_view(),
    #      name='api_private_album_post_upload_photo'),
    path('api/private/upload',
         create.ApiPrivatePhotoViewSet.as_view({'post': 'create'}),
         name='api_private_album_post_upload_photo'),

    # albums retrieve, public
    path('api/public/get_by_user',
         retrieve.ApiPublicAlbumsGetByUser.as_view(),
         name='api_public_albums_by_profile'),
    path('api/public/get_album',
         retrieve.ApiPublicAlbumGetByPK.as_view(),
         name='api_public_album_get_by_pk'),
    path('api/public/album/photos/all',
         retrieve.ApiPublicGetPhotos.as_view(),
         name='api_public_album_photos_all'),

    # albums retrieve, private
    path('api/private/albums/all',
         retrieve.ApiPrivateAlbumGetAlbums.as_view(),
         name='api_private_albums_all'),
    path('api/private/profile_photos/all',
         retrieve.ApiPrivateGetProfilePhotos.as_view(),
         name='api_private_profile_photos_all'),

    # albums update, private
    path('api/private/album/toggle_privacy',
         update.ApiPrivateAlbumTogglePrivacy.as_view(),
         name='api_private_album_toggle_privacy'),
    path('api/private/album/update',
         update.ApiPrivateAlbumUpdate.as_view(),
         name='api_private_album_update'),

    # photos update, private
    path('api/private/photo/set_primary',
         update.ApiPrivateSetPrimaryPhoto.as_view(),
         name='api_private_photo_set_primary'),
    path('api/private/photo/toggle_privacy',
         update.ApiPrivatePhotoTogglePrivacy.as_view(),
         name='api_private_photo_toggle_privacy'),
    path('api/private/photo/update',
         update.ApiPrivatePhotoUpdate.as_view(),
         name='api_private_photo_update'),
    path('api/private/photo/unset_primary',
         update.ApiPrivateUnsetPrimaryPhoto.as_view(),
         name='api_private_photo_unset_primary'),

    # photos retrieve, private
    path('api/private/photo/primary/detail',
         retrieve.ApiPrivateGetProfilePhoto.as_view(),
         name='api_private_profile_photo_detail'),
]
