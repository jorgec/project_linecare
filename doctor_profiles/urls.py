from django.urls import path


from .modules.views import home as home_views
from .modules.views import settings as setting_views
from .modules.views import medical_institutions as institution_views

from .modules.views import snippets

from .modules.api import medical_degrees_api
from .modules.api import specializations_api
from .modules.api import medical_associations_api
from .modules.api import insurance_providers_api

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
    path('settings/association',
         setting_views.DoctorProfileAssociationSettingsView.as_view(),
         name='doctor_profile_settings_association'),
    path('settings/insurance',
         setting_views.DoctorProfileInsuranceSettingsView.as_view(),
         name='doctor_profile_settings_insurance'),
    path('settings/medical_institution',
         institution_views.DoctorProfileMedicalInstitutionSettingsHomeView.as_view(),
         name='doctor_profile_settings_medical_institution'),
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
    path(f'{version}/public/medical_degree/list',
         medical_degrees_api.ApiPublicMedicalDegreeList.as_view(),
         name='api_public_medical_degree_list'),

    path(f'{version}/public/medical_degree/detail',
         medical_degrees_api.ApiPublicMedicalDegreeDetail.as_view(),
         name='api_public_medical_degree_detail'),

    path(f'{version}/private/medical_degree/create',
         medical_degrees_api.ApiPrivateMedicalDegreeCreate.as_view(),
         name='api_private_medical_degree_create'),

    #############################################################################
    # Doctor Degrees
    #############################################################################
    path(f'{version}/public/doctor_degree/list',
         medical_degrees_api.ApiPublicDoctorDegreeList.as_view(),
         name='api_public_doctor_degree_list'),
    path(f'{version}/private/doctor_degree/detail',
         medical_degrees_api.ApiPrivateDoctorDegreeDetail.as_view(),
         name='api_private_doctor_degree_detail'),
    path(f'{version}/private/doctor_degree/create',
         medical_degrees_api.ApiPrivateDoctorDegreeCreate.as_view(),
         name='api_private_doctor_degree_create'),
    path(f'{version}/private/doctor_degree/update',
         medical_degrees_api.ApiPrivateDoctorDegreeUpdate.as_view(),
         name='api_private_doctor_degree_update'),
    path(f'{version}/private/doctor_degree/delete',
         medical_degrees_api.ApiPrivateDoctorDegreeDelete.as_view(),
         name='api_private_doctor_degree_delete'),

    #############################################################################
    # Specialization
    #############################################################################
    path(f'{version}/public/specialization/list',
         specializations_api.ApiPublicSpecializationList.as_view(),
         name='api_public_specialization_list'),

    path(f'{version}/public/specialization/detail',
         specializations_api.ApiPublicSpecializationDetail.as_view(),
         name='api_public_specialization_detail'),

    path(f'{version}/private/specialization/create',
         specializations_api.ApiPrivateSpecializationCreate.as_view(),
         name='api_private_specialization_create'),

    #############################################################################
    # Doctor Specializations
    #############################################################################
    path(f'{version}/public/doctor_specialization/list',
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
    
    #############################################################################
    # Medical Associations
    #############################################################################
    path(f'{version}/public/medical_association/list',
         medical_associations_api.ApiPublicMedicalAssociationList.as_view(),
         name='api_public_medical_association_list'),

    path(f'{version}/public/medical_association/detail',
         medical_associations_api.ApiPublicMedicalAssociationDetail.as_view(),
         name='api_public_medical_association_detail'),

    path(f'{version}/private/medical_association/create',
         medical_associations_api.ApiPrivateMedicalAssociationCreate.as_view(),
         name='api_private_medical_association_create'),

    #############################################################################
    # Doctor Associations
    #############################################################################
    path(f'{version}/public/doctor_association/list',
         medical_associations_api.ApiPublicDoctorAssociationList.as_view(),
         name='api_public_doctor_association_list'),
    path(f'{version}/private/doctor_association/detail',
         medical_associations_api.ApiPrivateDoctorAssociationDetail.as_view(),
         name='api_private_doctor_association_detail'),
    path(f'{version}/private/doctor_association/create',
         medical_associations_api.ApiPrivateDoctorAssociationCreate.as_view(),
         name='api_private_doctor_association_create'),
    path(f'{version}/private/doctor_association/update',
         medical_associations_api.ApiPrivateDoctorAssociationUpdate.as_view(),
         name='api_private_doctor_association_update'),
    path(f'{version}/private/doctor_association/delete',
         medical_associations_api.ApiPrivateDoctorAssociationDelete.as_view(),
         name='api_private_doctor_association_delete'),
    
    #############################################################################
    # Insurance Providers
    #############################################################################
    path(f'{version}/public/insurance_provider/list',
         insurance_providers_api.ApiPublicInsuranceProviderList.as_view(),
         name='api_public_insurance_provider_list'),

    path(f'{version}/public/insurance_provider/detail',
         insurance_providers_api.ApiPublicInsuranceProviderDetail.as_view(),
         name='api_public_insurance_provider_detail'),

    path(f'{version}/private/insurance_provider/create',
         insurance_providers_api.ApiPrivateInsuranceProviderCreate.as_view(),
         name='api_private_insurance_provider_create'),

    #############################################################################
    # Doctor Insurance
    #############################################################################
    path(f'{version}/public/doctor_insurance/list',
         insurance_providers_api.ApiPublicDoctorInsuranceList.as_view(),
         name='api_public_doctor_insurance_list'),
    path(f'{version}/private/doctor_insurance/detail',
         insurance_providers_api.ApiPrivateDoctorInsuranceDetail.as_view(),
         name='api_private_doctor_insurance_detail'),
    path(f'{version}/private/doctor_insurance/create',
         insurance_providers_api.ApiPrivateDoctorInsuranceCreate.as_view(),
         name='api_private_doctor_insurance_create'),
    path(f'{version}/private/doctor_insurance/update',
         insurance_providers_api.ApiPrivateDoctorInsuranceUpdate.as_view(),
         name='api_private_doctor_insurance_update'),
    path(f'{version}/private/doctor_insurance/delete',
         insurance_providers_api.ApiPrivateDoctorInsuranceDelete.as_view(),
         name='api_private_doctor_insurance_delete'),
]
