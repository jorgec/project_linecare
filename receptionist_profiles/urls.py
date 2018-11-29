from django.urls import path

from .modules.api import receptionist_profile_api


urlpatterns = []


#############################################################################
# API
#############################################################################
version = 'api/v1'

urlpatterns += [
    path(f'{version}/private/connection/create',
         receptionist_profile_api.ApiPrivateReceptionistConnectionCreate.as_view(),
         name='api_private_receptionist_connection_create'),
    path(f'{version}/private/connection/delete',
         receptionist_profile_api.ApiPrivateReceptionistConnectionDelete.as_view(),
         name='api_private_receptionist_connection_delete'),
    path(f'{version}/private/profile/create_by_doctor',
         receptionist_profile_api.ApiPrivateReceptionistProfileCreateByDoctor.as_view(),
         name='api_private_receptionist_profile_create_by_doctor'),
]