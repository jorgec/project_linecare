from django.urls import path

from .modules.views import home as home_views
from .modules.views import doctor_schedule as doctor_schedule_views

from .modules.api import receptionist_profile_api
from .modules.api import receptionist_connections_api

urlpatterns = [
    path('home', home_views.ReceptionistProfileHomeView.as_view(),
         name='receptionist_profile_home'),

    path('schedule/<medical_institution>/<doctor_id>', doctor_schedule_views.ReceptionistProfileDoctorScheduleList.as_view(),
         name='receptionist_profile_doctor_schedules'),
    path('queue/<medical_institution>/<doctor_id>', doctor_schedule_views.ReceptionistProfileDoctorScheduleDetail.as_view(),
         name='receptionist_profile_doctor_queue'),
]


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

    # connections
    path(f'{version}/private/connection/list',
         receptionist_connections_api.ApiPrivateReceptionistProfileConnectionList.as_view(),
         name='api_private_receptionist_connection_list'),
]