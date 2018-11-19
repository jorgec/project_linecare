from django.urls import path

from .modules.views import home as home_views
from .modules.views import settings as setting_views

from .modules.views import snippets

from .modules.api import medical_degree_api
from .modules.api import specializations_api

#############################################################################
# Views
#############################################################################
urlpatterns = [
    path('home',
         home_views.DoctorProfileHomeView.as_view(),
         name='doctor_profile_home'),

    #############################################################################
    # Settings
    #############################################################################
    path('settings',
         setting_views.DoctorProfileSettingsHomeView.as_view(),
         name='doctor_profile_settings_home'),
    path('settings/medical_degree',
         setting_views.DoctorProfileMedicalDegreeSettingsView.as_view(),
         name='doctor_profile_settings_medical_degree'),
    path('settings/specialization',
         setting_views.DoctorProfileSpecializationSettingsView.as_view(),
         name='doctor_profile_settings_specialization'),
]

#############################################################################
# Snippets
#############################################################################
urlpatterns += [
    path('snippets/profile_progress',
         snippets.DoctorProfileProgressSnippet.as_view(),
         name='doctor_snippets_profile_progress'),
    path('snippets/profile_progress_detail',
         snippets.DoctorProfileProgressDetailSnippet.as_view(),
         name='doctor_snippets_profile_progress'),
]


#############################################################################
# API
#############################################################################
version = 'api/v1'

urlpatterns += [
    #############################################################################
    # Medical Degrees
    #############################################################################
    path(f'{version}/public/medical_degrees',
         medical_degree_api.ApiPublicMedicalDegreeList.as_view(),
         name='api_public_medical_degree_list'),

    path(f'{version}/public/medical_degree',
         medical_degree_api.ApiPublicMedicalDegreeDetail.as_view(),
         name='api_public_medical_degree_detail'),

    path(f'{version}/private/medical_degree/create',
         medical_degree_api.ApiPrivateMedicalDegreeCreate.as_view(),
         name='api_private_medical_degree_create'),

    #############################################################################
    # Doctor Degrees
    #############################################################################
    path(f'{version}/public/doctor_degrees',
         medical_degree_api.ApiPublicDoctorDegreeList.as_view(),
         name='api_public_doctor_degree_list'),
    path(f'{version}/private/doctor_degree/detail',
         medical_degree_api.ApiPrivateDoctorDegreeDetail.as_view(),
         name='api_private_doctor_degree_detail'),
    path(f'{version}/private/doctor_degree/create',
         medical_degree_api.ApiPrivateDoctorDegreeCreate.as_view(),
         name='api_private_doctor_degree_create'),
    path(f'{version}/private/doctor_degree/update',
         medical_degree_api.ApiPrivateDoctorDegreeUpdate.as_view(),
         name='api_private_doctor_degree_update'),
    path(f'{version}/private/doctor_degree/delete',
         medical_degree_api.ApiPrivateDoctorDegreeDelete.as_view(),
         name='api_private_doctor_degree_delete'),

    #############################################################################
    # Specialization
    #############################################################################
    path(f'{version}/public/specializations',
         specializations_api.ApiPublicSpecializationList.as_view(),
         name='api_public_specialization_list'),

    path(f'{version}/public/specialization',
         specializations_api.ApiPublicSpecializationDetail.as_view(),
         name='api_public_specialization_detail'),

    path(f'{version}/private/specialization/create',
         specializations_api.ApiPrivateSpecializationCreate.as_view(),
         name='api_private_specialization_create'),

    #############################################################################
    # Doctor Specializations
    #############################################################################
    path(f'{version}/public/doctor_specializations',
         specializations_api.ApiPublicDoctorSpecializationList.as_view(),
         name='api_public_doctor_specialization_list'),
    path(f'{version}/private/doctor_specialization/detail',
         specializations_api.ApiPrivateDoctorSpecializationDetail.as_view(),
         name='api_private_doctor_specialization_detail'),
    path(f'{version}/private/doctor_specialization/create',
         specializations_api.ApiPrivateDoctorSpecializationCreate.as_view(),
         name='api_private_doctor_specialization_create'),
    path(f'{version}/private/doctor_specialization/update',
         specializations_api.ApiPrivateDoctorSpecializationUpdate.as_view(),
         name='api_private_doctor_specialization_update'),
    path(f'{version}/private/doctor_specialization/delete',
         specializations_api.ApiPrivateDoctorSpecializationDelete.as_view(),
         name='api_private_doctor_specialization_delete'),
]
