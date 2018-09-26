from django.urls import path
from .modules.api import retrieve, update

urlpatterns = [
    # Retrieve
    path('api/public/profile/by_pk',
         retrieve.ApiPublicProfileGetByPK.as_view(),
         name='api_public_profile_by_pk'),
    path('api/public/profile/by_username',
         retrieve.ApiPublicProfileGetByUsername.as_view(),
         name='api_public_profile_by_username'),

    # Update
    path('api/private/profile/update',
         update.ApiPrivateProfileUpdate.as_view(),
         name='api_private_profile_update'),

]
