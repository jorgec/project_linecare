from django.urls import path
from .modules.api import retrieve as api_retrieve
from .modules.api import update as api_update

from .modules.views import settings as settings_view
from .modules.views import home as home_view
from .modules.views import albums as albums_view

urlpatterns = [
    # Retrieve
    # multiple
    path('api/public/profiles/by_user_type',
         api_retrieve.ApiPublicProfileGetByUserType.as_view(),
         name='api_public_profiles_by_user_type'),
    path('api/private/profiles/by_name',
         api_retrieve.ApiPrivateProfilesGetByName.as_view(),
         name='api_private_profiles_by_name'),

    # single
    path('api/public/profile/by_pk',
         api_retrieve.ApiPublicProfileGetByPK.as_view(),
         name='api_public_profile_by_pk'),
    path('api/public/profile/by_username',
         api_retrieve.ApiPublicProfileGetByUsername.as_view(),
         name='api_public_profile_by_username'),
    path('api/public/profile/by_pk',
         api_retrieve.ApiPrivateProfileGetByPK.as_view(),
         name='api_private_profile_by_pk'),

    # Update
    path('api/private/profile/update',
         api_update.ApiPrivateProfileUpdate.as_view(),
         name='api_private_profile_update'),

     # albums
     path('api/public/profile_photos/album',
          api_retrieve.ApiPublicProfileGetProfilePhotoAlbum.as_view(),
          name='api_public_profile_photo_album'),
     path('api/public/cover_photos/album',
          api_retrieve.ApiPublicProfileGetCoverPhotoAlbum.as_view(),
          name='api_public_cover_photo_album'),
]

# views

urlpatterns += [
    # home
    path('home', home_view.BaseProfileHomeView.as_view(), name='base_profile_home_view'),

    # settings
    path('settings/basic', settings_view.ProfileSettingsBasicInfoView.as_view(), name='profile_settings_basic_info_view'),
    path('settings/email', settings_view.ProfileSettingsEmailView.as_view(), name='profile_settings_email_view'),
    path('settings/password', settings_view.ProfileSettingsPasswordView.as_view(), name='profile_settings_password_view'),
    path('settings/biometrics/create', settings_view.BiometricsCreateView.as_view(), name='profile_settings_biometrics_create'),
    path('settings/biometrics/update', settings_view.BiometricsUpdateView.as_view(), name='profile_settings_biometrics_update'),

    path('albums/list', albums_view.BaseProfileAlbumList.as_view(), name='profile_album_list'),
    path('albums/<slug>/detail', albums_view.BaseProfileAlbumDetail.as_view(), name='profile_album_detail'),
]