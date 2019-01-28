from django.urls import path

from doctor_profiles.modules.api import medical_institutions_api
from .modules.views import home as home_views
from .modules.views import doctor_schedule as doctor_schedule_views
from .modules.views import receptionist_connections as receptionist_connection_views

from .modules.api import receptionist_profile_api
from .modules.api import receptionist_connections_api

urlpatterns = [
    path('home', home_views.ReceptionistProfileHomeView.as_view(),
         name='receptionist_profile_home'),
    path('create', home_views.ReceptionistProfileCreate.as_view(),
         name='receptionist_profile_create'),

    path('schedule/<medical_institution>/<doctor_id>',
         doctor_schedule_views.ReceptionistProfileDoctorScheduleList.as_view(),
         name='receptionist_profile_doctor_schedules'),
    path('calendar/<doctor_id>',
         doctor_schedule_views.ReceptionistProfileDoctorScheduleCalendarMonth.as_view(),
         name='receptionist_profile_doctor_calendar_month'),
    path('queue/<medical_institution>/<doctor_id>',
         doctor_schedule_views.ReceptionistProfileDoctorScheduleDetail.as_view(),
         name='receptionist_profile_doctor_queue'),
    path('schedule/<medical_institution>/<doctor>/history',
         doctor_schedule_views.DoctorProfileScheduleHistory.as_view(),
         name='receptionist_profile_medical_institution_doctor_history_list'),

    # connections
    path('settings/medical_institution',
         receptionist_connection_views.ReceptionistProfileMedicalInstitutionSettingsHomeView.as_view(),
         name='receptionist_profile_settings_medical_institution'),
    path('settings/medical_institution/connect',
         receptionist_connection_views.ReceptionistMedicalInstitutionConnect.as_view(),
         name='receptionist_profile_settings_medical_institution_connect'),
    path('settings/medical_institution/create_connection',
         receptionist_connection_views.ReceptionistProfileMedicalInstitutionCreateConnection.as_view(),
         name='receptionist_profile_settings_medical_institution_create_connection'),
    path('medical_institution/<slug>',
         receptionist_connection_views.ReceptionistProfileMedicalInstitutionManageConnectionView.as_view(),
         name='receptionist_profile_medical_institution_home'),
    path('medical_institution/<slug>/remove',
         receptionist_connection_views.ReceptionistProfileRemoveConnectionView.as_view(),
         name='receptionist_profile_medical_intitution_remove'),
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

    path(f'{version}/private/medical_institution/create',
         medical_institutions_api.ApiPrivateMedicalInstitutionCreate.as_view(),
         name='api_private_medical_institution_create_by_receptionist'),
]
