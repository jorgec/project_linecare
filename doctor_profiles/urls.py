from django.urls import path

from .modules.views import home as home_views
from .modules.views import settings as setting_views

from .modules.api import medical_degree_api

urlpatterns = [
    path('home',
         home_views.DoctorProfileHomeView.as_view(),
         name='doctor_profile_home'),

    path('settings/medical_degree',
         setting_views.DoctorProfileMedicalDegreeSettingsView.as_view(),
         name='doctor_profile_settings_medical_degree'),
]

version = 'api/v1'

urlpatterns += [
    #############################################################################
    # Medical Degrees
    #############################################################################
    path(f'{version}/public/medical_degrees',
         medical_degree_api.ApiPublicMedicalDegreeList.as_view(),
         name='api_public_get_medical_degrees'),

    path(f'{version}/public/medical_degree',
         medical_degree_api.ApiPublicMedicalDegreeDetail.as_view(),
         name='api_public_get_medical_degree'),

    path(f'{version}/private/medical_degree/create',
         medical_degree_api.ApiPrivateMedicalDegreeCreate.as_view(),
         name='api_private_create_medical_degree'),

    #############################################################################
    # Doctor Degrees
    #############################################################################
    path(f'{version}/public/doctor_degrees',
         medical_degree_api.ApiPublicDoctorDegreeList.as_view(),
         name='api_public_doctor_degrees'),
    path(f'{version}/private/doctor_degree/detail',
         medical_degree_api.ApiPrivateDoctorDegreeDetail.as_view(),
         name='api_private_doctor_degree_detail'),
    path(f'{version}/private/doctor_degree/add',
         medical_degree_api.ApiPrivateDoctorDegreeCreate.as_view(),
         name='api_private_doctor_degree_add'),
    path(f'{version}/private/doctor_degree/edit',
         medical_degree_api.ApiPrivateDoctorDegreeEdit.as_view(),
         name='api_private_doctor_degree_edit'),
    path(f'{version}/private/doctor_degree/delete',
         medical_degree_api.ApiPrivateDoctorDegreeDelete.as_view(),
         name='api_private_doctor_degree_delete'),
]
