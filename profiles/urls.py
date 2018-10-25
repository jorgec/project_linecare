from django.urls import path
from .modules.api import retrieve as api_retrieve
from .modules.api import update as api_update

from .modules.views import settings as view_settings

urlpatterns = [
    # Retrieve
    # multiple
    path('api/public/profiles/by_user_type',
         api_retrieve.ApiPublicProfileGetByUserType.as_view(),
         name='api_public_profiles_by_user_type'),

    # single
    path('api/public/profile/by_pk',
         api_retrieve.ApiPublicProfileGetByPK.as_view(),
         name='api_public_profile_by_pk'),
    path('api/public/profile/by_username',
         api_retrieve.ApiPublicProfileGetByUsername.as_view(),
         name='api_public_profile_by_username'),

    # Update
    path('api/private/profile/update',
         api_update.ApiPrivateProfileUpdate.as_view(),
         name='api_private_profile_update'),

]

# views

urlpatterns += [
    path('settings/basic', view_settings.ProfileSettingsBasicInfoView.as_view(), name='profile_settings_basic_info_view'),
]