from django.urls import path, include
from rest_framework import routers

from doctor_profiles.modules.api import doctor_notifications_api
from .modules.views import home as home_views
from .modules.views import settings as setting_views
from .modules.views import medical_institutions as institution_views
from .modules.views import schedule as schedule_views
from .modules.views import patient as patient_views
from .modules.views import analytics as analytics_views

from .modules.views import snippets

from .modules.api import medical_degrees_api
from .modules.api import specializations_api
from .modules.api import medical_associations_api
from .modules.api import insurance_providers_api
from .modules.api import medical_institutions_api
from .modules.api import medical_institution_doctors_api
from .modules.api import doctor_profile_api
from .modules.api import doctor_schedule_api
from .modules.api import patient_connection_api
from .modules.api import patient_appointment_api
from .modules.api import symptoms_api
from .modules.api import findings_api
from .modules.api import diagnosis_api
from .modules.api import checkup_api
from .modules.api import labtest_api
from .modules.api import prescriptions_api
from .modules.api import questionnaire_api

from .modules.analytics_api import patient_analytics_api

#############################################################################
# Views
#############################################################################
urlpatterns = [
    path('home',
         home_views.DoctorProfileHomeView.as_view(),
         name='doctor_profile_home'),
    path('create',
         home_views.DoctorProfileCreate.as_view(),
         name='doctor_profile_create'),

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

    #############################################################################
    # Medical Institutions
    #############################################################################
    path('settings/medical_institution/connect',
         institution_views.DoctorProfileMedicalInstitutionConnect.as_view(),
         name='doctor_profile_settings_medical_institution_connect'),
    path('settings/medical_institution/create_connection',
         institution_views.DoctorProfileMedicalInstitutionDoctorCreateConnection.as_view(),
         name='doctor_profile_settings_medical_institution_create_connection'),
    path('medical_institution/<slug>',
         institution_views.DoctorProfileMedicalInstitutionManageConnectionView.as_view(),
         name='doctor_profile_medical_institution_home'),

    #############################################################################
    # Schedule
    #############################################################################
    path('schedule/<medical_institution>/history',
         schedule_views.DoctorProfileScheduleHistory.as_view(),
         name='doctor_profile_medical_institution_history_list'),
    path('schedule/<medical_institution>',
         schedule_views.DoctorProfileMedicalInstitutionScheduleList.as_view(),
         name='doctor_profile_medical_institution_schedule_list'),
    path('queue/<medical_institution>',
         schedule_views.DoctorProfileScheduleDetail.as_view(),
         name='doctor_profile_schedule_detail'),
    path('queue',
         schedule_views.DoctorProfileScheduleDetail.as_view(),
         name='doctor_profile_schedule_detail_urlstring'),
    path('calendar',
         schedule_views.DoctorProfileScheduleCalendarMonth.as_view(),
         name='doctor_profile_calendar'),

    #############################################################################
    # Patients/Appointment
    #############################################################################
    path('appointments',
         schedule_views.DoctorProfileScheduleList.as_view(),
         name='doctor_profile_appointments_list'),
    path('patients',
         patient_views.DoctorProfilePatientList.as_view(),
         name='doctor_profile_patient_list'),
    path('patients/appointment/detail',
         patient_views.DoctorProfilePatientAppointmentDetail.as_view(),
         name='doctor_profile_patient_appointment_detail'),
    path('patients/appointment/history/detail',
         patient_views.DoctorProfilePatientAppointmentHistoryDetail.as_view(),
         name='doctor_profile_patient_appointment_history_detail'),
    path('patients/<patient_id>/detail',
         patient_views.DoctorProfilePatientDetail.as_view(),
         name='doctor_profile_patient_detail'),
    path('patients/detail',
         patient_views.DoctorProfilePatientQSDetail.as_view(),
         name='doctor_profile_patient_qs_detail'),

    #############################################################################
    # Analytics
    #############################################################################
    path('analytics/checkups',
         analytics_views.DoctorProfileAnalyticsPatientByCheckupAggregateView.as_view(),
         name='doctor_profile_analytics_checkups_aggregate'),
    path('analytics/symptoms',
         analytics_views.DoctorProfileAnalyticsPatientBySymptomAggregateView.as_view(),
         name='doctor_profile_analytics_symptoms_aggregate'),
    path('analytics/findings',
         analytics_views.DoctorProfileAnalyticsPatientByFindingAggregateView.as_view(),
         name='doctor_profile_analytics_findings_aggregate'),
    path('analytics/diagnoses',
         analytics_views.DoctorProfileAnalyticsPatientByDiagnosisAggregateView.as_view(),
         name='doctor_profile_analytics_diagnoses_aggregate'),
    path('analytics/prescriptions',
         analytics_views.DoctorProfileAnalyticsPatientByPrescriptionAggregateView.as_view(),
         name='doctor_profile_analytics_prescriptions_aggregate'),
    path('analytics/labtests',
         analytics_views.DoctorProfileAnalyticsPatientByLabtestAggregateView.as_view(),
         name='doctor_profile_analytics_labtests_aggregate'),
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
    # Doctor Profile
    #############################################################################
    path(f'{version}/private/profile/dismiss_progress_display',
         doctor_profile_api.ApiDismissProfileProgressDisplay.as_view(),
         name='api_doctor_profile_dismiss_profile_progress_display'),
    path(f'{version}/public/profile/detail',
         doctor_profile_api.ApiPublicDoctorProfileDetail.as_view(),
         name='api_public_doctor_profile_detail'),

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
    # Doctor Degrees api_public_doctor_medical_degree_list
    #############################################################################
    path(f'{version}/public/doctor_degree/list',
         medical_degrees_api.ApiPublicDoctorDegreeList.as_view(),
         name='api_public_doctor_medical_degree_list'),
    path(f'{version}/private/doctor_degree/detail',
         medical_degrees_api.ApiPrivateDoctorDegreeDetail.as_view(),
         name='api_private_doctor_medical_degree_detail'),
    path(f'{version}/private/doctor_degree/create',
         medical_degrees_api.ApiPrivateDoctorDegreeCreate.as_view(),
         name='api_private_doctor_medical_degree_create'),
    path(f'{version}/private/doctor_degree/update',
         medical_degrees_api.ApiPrivateDoctorDegreeUpdate.as_view(),
         name='api_private_doctor_medical_degree_update'),
    path(f'{version}/private/doctor_degree/delete',
         medical_degrees_api.ApiPrivateDoctorDegreeDelete.as_view(),
         name='api_private_doctor_medical_degree_delete'),

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

    #############################################################################
    # Medical Institutions
    #############################################################################
    path(f'{version}/public/medical_institutions/connected/list',
         doctor_profile_api.ApiPublicDoctorProfileMedicalInstitutions.as_view(),
         name='api_public_doctor_medical_institutions_list'),
    path(f'{version}/public/medical_institution/type/list',
         medical_institutions_api.ApiPublicMedicalInstitutionTypeList.as_view(),
         name='api_public_medical_institution_type_list'),

    path(f'{version}/public/medical_institution/list',
         medical_institutions_api.ApiPublicMedicalInstitutionList.as_view(),
         name='api_public_medical_institution_list'),
    path(f'{version}/public/medical_institution/detail',
         medical_institutions_api.ApiPublicMedicalInstitutionDetail.as_view(),
         name='api_public_medical_institution_detail'),
    path(f'{version}/private/medical_institution/create',
         medical_institutions_api.ApiPrivateMedicalInstitutionCreate.as_view(),
         name='api_private_medical_institution_create'),

    # connection meta
    path(f'{version}/private/medical_institution_doctor/list',
         medical_institution_doctors_api.ApiMedicalInstitutionDoctorList.as_view(),
         name='api_private_medical_institution_doctor_list'),
    path(f'{version}/private/medical_institution_doctor/connection/create',
         medical_institution_doctors_api.ApiMedicalInstitutionDoctorCreate.as_view(),
         name='api_private_medical_institution_doctor_connection_create'),
    path(f'{version}/public/medical_institution_doctor/meta/list',
         medical_institution_doctors_api.ApiMedicalInstitutionDoctorMetaList.as_view(),
         name='api_public_medical_institution_doctor_meta_list'),
    path(f'{version}/private/medical_institution_doctor/meta/update',
         medical_institution_doctors_api.ApiMedicalInstitutionDoctorMetaUpdate.as_view(),
         name='api_private_medical_institution_doctor_meta_update'),

    # location
    path(f'{version}/public/medical_institution/location/list',
         medical_institutions_api.ApiPublicMedicalInstitutionAddressList.as_view(),
         name='api_public_medical_institution_location_list'),
    path(f'{version}/public/medical_institution/location/top/detail',
         medical_institutions_api.ApiPublicMedicalInstitutionTopAddressDetail.as_view(),
         name='api_public_medical_institution_top_location_detail'),
    path(f'{version}/public/medical_institution/location/detail',
         medical_institutions_api.ApiPublicMedicalInstitutionAddressDetail.as_view(),
         name='api_public_medical_institution_location_detail'),
    path(f'{version}/private/medical_institution/location/create',
         medical_institutions_api.ApiPrivateMedicalInstitutionLocationCreate.as_view(),
         name='api_private_medical_institution_location_create'),
    path(f'{version}/private/medical_institution/location/vote_up',
         medical_institutions_api.ApiPrivateMedicalInstitutionLocationVoteUp.as_view(),
         name='api_private_medical_institution_location_vote_up'),
    path(f'{version}/private/medical_institution/location/vote_down',
         medical_institutions_api.ApiPrivateMedicalInstitutionLocationVoteDown.as_view(),
         name='api_private_medical_institution_location_vote_down'),

    # coordinate
    path(f'{version}/public/medical_institution/coordinate/list',
         medical_institutions_api.ApiPublicMedicalInstitutionCoordinateList.as_view(),
         name='api_public_medical_institution_coordinate_list'),
    path(f'{version}/public/medical_institution/coordinate/top/detail',
         medical_institutions_api.ApiPublicMedicalInstitutionTopCoordinateDetail.as_view(),
         name='api_public_medical_institution_top_coordinate_detail'),
    path(f'{version}/public/medical_institution/coordinate/detail',
         medical_institutions_api.ApiPublicMedicalInstitutionCoordinateDetail.as_view(),
         name='api_public_medical_institution_coordinate_detail'),
    path(f'{version}/private/medical_institution/coordinate/create',
         medical_institutions_api.ApiPrivateMedicalInstitutionCoordinateCreate.as_view(),
         name='api_private_medical_institution_coordinate_create'),
    path(f'{version}/private/medical_institution/coordinate/vote_up',
         medical_institutions_api.ApiPrivateMedicalInstitutionCoordinateVoteUp.as_view(),
         name='api_private_medical_institution_coordinate_vote_up'),
    path(f'{version}/private/medical_institution/coordinate/vote_down',
         medical_institutions_api.ApiPrivateMedicalInstitutionCoordinateVoteDown.as_view(),
         name='api_private_medical_institution_coordinate_vote_down'),

    # receptionists
    path(f'{version}/private/medical_institution/receptionist/list',
         medical_institutions_api.ApiPrivateMedicalInstitutionReceptionistList.as_view(),
         name='api_private_medical_institution_receptionist_list'),
    path(f'{version}/private/medical_institution/receptionist/not_connected/list',
         medical_institutions_api.ApiPrivateMedicalInstitutionNotConnectedReceptionistList.as_view(),
         name='api_private_medical_institution_receptionist_not_connected_list'),
    path(f'{version}/private/medical_institution/receptionist/connected/list',
         medical_institutions_api.ApiPrivateMedicalInstitutionConnectedReceptionistList.as_view(),
         name='api_private_medical_institution_receptionist_connected_list'),

    # schedule
    path(f'{version}/private/doctor/schedule/create',
         doctor_schedule_api.ApiDoctorScheduleCreate.as_view(),
         name='api_private_doctor_schedule_create'),
    path(f'{version}/public/doctor/schedule/list',
         doctor_schedule_api.ApiDoctorScheduleList.as_view(),
         name='api_public_doctor_schedule_list'),
    path(f'{version}/public/doctor/schedule/days',
         doctor_schedule_api.ApiDoctorScheduleDayList.as_view(),
         name='api_public_doctor_schedule_days_list'),
    path(f'{version}/private/doctor/schedule/delete',
         doctor_schedule_api.ApiDoctorScheduleDelete.as_view(),
         name='api_private_doctor_schedule_delete'),
    path(f'{version}/private/doctor/schedule_day/presence/toggle',
         doctor_schedule_api.ApiPrivateDoctorScheduleDayPresenceToggle.as_view(),
         name='api_private_doctor_schedule_day_presence_toggle'),
    path(f'{version}/private/doctor/schedule_day/presence/status',
         doctor_schedule_api.ApiPrivateDoctorScheduleDayPresenceStatus.as_view(),
         name='api_private_doctor_schedule_day_presence_status'),
    path(f'{version}/private/doctor/schedule_day/delete',
         doctor_schedule_api.ApiDoctorScheduleDayDelete.as_view(),
         name='api_private_doctor_schedule_day_delete'),

    # patient connections
    path(f'{version}/private/patients/search',
         patient_connection_api.ApiPrivatePatientConnectionSearchList.as_view(),
         name='api_private_patient_connection_search'),

    # appointments
    path(f'{version}/private/appointment/create',
         doctor_schedule_api.ApiDoctorScheduleAppointmentCreate.as_view(),
         name='api_private_appointment_create'),
    path(f'{version}/private/queue/list',
         doctor_schedule_api.ApiPrivateDoctorScheduleQueueList.as_view(),
         name='api_private_queue_list'),
    path(f'{version}/private/patient/appointments/history',
         patient_appointment_api.ApiPatientAppointmentHistory.as_view(),
         name='api_private_patient_appointments_history'),

    path(f'{version}/public/queue/list',
         doctor_schedule_api.ApiPublicDummyScheduleQueueList.as_view(),
         name='api_public_queue_list'),

    path(f'{version}/private/appointment/status/update',
         patient_appointment_api.ApiPatientAppointmentUpdateStatus.as_view(),
         name='api_private_patient_appointment_status_update'),
    path(f'{version}/private/appointment/list',
         patient_appointment_api.ApiPatientAppointmentList.as_view(),
         name='api_private_patient_appointment_list'),
    path(f'{version}/private/appointments/today/count',
         patient_appointment_api.ApiPatientAppointmentCount.as_view(),
         name='api_private_patient_appointment_count'),

    # calendar
    path(f'{version}/private/calendar/month',
         doctor_schedule_api.ApiPrivateDoctorScheduleCalendar.as_view(),
         name='api_private_calendar_month'),

    # symptoms
    path(f'{version}/private/symptom/create',
         symptoms_api.ApiPrivateSymptomCreate.as_view(),
         name='api_private_symptom_create'),
    path(f'{version}/private/appointment/symptom/create',
         symptoms_api.ApiPrivatePatientSymptomCreate.as_view(),
         name='api_private_appointment_symptom_create'),
    path(f'{version}/public/symptoms/list',
         symptoms_api.ApiPublicSymptomList.as_view(),
         name='api_public_symptoms_list'),
    path(f'{version}/private/appointment/symptom/list',
         symptoms_api.ApiPrivatePatientSymptomList.as_view(),
         name='api_private_appointment_symptom_list'),
    path(f'{version}/private/appointment/symptom/dismissed_list',
         symptoms_api.ApiPrivatePatientDismissedSymptomList.as_view(),
         name='api_private_appointment_symptom_dismissed_list'),
    path(f'{version}/private/appointment/symptom/delete',
         symptoms_api.ApiPrivatePatientSymptomRemove.as_view(),
         name='api_private_appointment_symptom_delete'),
    path(f'{version}/private/appointment/symptom/undismiss',
         symptoms_api.ApiPrivatePatientSymptomUndismiss.as_view(),
         name='api_private_appointment_symptom_undismiss'),

    # findings
    path(f'{version}/private/finding/create',
         findings_api.ApiPrivateFindingCreate.as_view(),
         name='api_private_finding_create'),
    path(f'{version}/private/appointment/finding/create',
         findings_api.ApiPrivatePatientFindingCreate.as_view(),
         name='api_private_appointment_finding_create'),
    path(f'{version}/public/findings/list',
         findings_api.ApiPublicFindingList.as_view(),
         name='api_public_findings_list'),
    path(f'{version}/private/appointment/finding/list',
         findings_api.ApiPrivatePatientFindingList.as_view(),
         name='api_private_appointment_finding_list'),
    path(f'{version}/private/appointment/finding/dismissed_list',
         findings_api.ApiPrivatePatientDismissedFindingList.as_view(),
         name='api_private_appointment_finding_dismissed_list'),
    path(f'{version}/private/appointment/finding/delete',
         findings_api.ApiPrivatePatientFindingRemove.as_view(),
         name='api_private_appointment_finding_delete'),
    path(f'{version}/private/appointment/finding/undismiss',
         findings_api.ApiPrivatePatientFindingUndismiss.as_view(),
         name='api_private_appointment_finding_undismiss'),

    # diagnoses
    path(f'{version}/private/diagnosis/create',
         diagnosis_api.ApiPrivateDiagnosisCreate.as_view(),
         name='api_private_diagnosis_create'),
    path(f'{version}/private/appointment/diagnosis/create',
         diagnosis_api.ApiPrivatePatientDiagnosisCreate.as_view(),
         name='api_private_appointment_diagnosis_create'),
    path(f'{version}/public/diagnoses/list',
         diagnosis_api.ApiPublicDiagnosisList.as_view(),
         name='api_public_diagnoses_list'),
    path(f'{version}/private/appointment/diagnosis/list',
         diagnosis_api.ApiPrivatePatientDiagnosisList.as_view(),
         name='api_private_appointment_diagnosis_list'),
    path(f'{version}/private/appointment/diagnosis/dismissed_list',
         diagnosis_api.ApiPrivatePatientDismissedDiagnosisList.as_view(),
         name='api_private_appointment_diagnosis_dismissed_list'),
    path(f'{version}/private/appointment/diagnosis/delete',
         diagnosis_api.ApiPrivatePatientDiagnosisRemove.as_view(),
         name='api_private_appointment_diagnosis_delete'),
    path(f'{version}/private/appointment/diagnosis/undismiss',
         diagnosis_api.ApiPrivatePatientDiagnosisUndismiss.as_view(),
         name='api_private_appointment_diagnosis_undismiss'),

    # notes
    path(f'{version}/private/appointment/note/list',
         checkup_api.ApiCheckupNoteList.as_view(),
         name='api_private_appointment_note_list'),
    path(f'{version}/private/appointment/note/create',
         checkup_api.ApiCheckupNoteCreate.as_view(),
         name='api_private_appointment_note_create'),

    # labtests
    path(f'{version}/public/labtest/list',
         labtest_api.ApiPublicLabtestList.as_view(),
         name='api_public_labtest_list'),
    path(f'{version}/private/appointment/labtest/create',
         labtest_api.ApiPrivatePatientLabTestCreate.as_view(),
         name='api_private_patient_labtest_create'),
    path(f'{version}/private/appointment/labtest/list',
         labtest_api.ApiPrivatePatientLabTestList.as_view(),
         name='api_private_patient_labtest_list'),
    path(f'{version}/private/appointment/labtest/dismissed_list',
         labtest_api.ApiPrivatePatientDismissedLabTestList.as_view(),
         name='api_private_patient_labtest_dismissed_list'),
    path(f'{version}/private/appointment/labtest/delete',
         labtest_api.ApiPrivatePatientLabTestRemove.as_view(),
         name='api_private_appointment_labtest_delete'),
    path(f'{version}/private/appointment/labtest/undismiss',
         labtest_api.ApiPrivatePatientLabTestUndismiss.as_view(),
         name='api_private_appointment_labtest_undismiss'),

    # prescriptions
    path(f'{version}/private/appointment/prescription/create',
         prescriptions_api.ApiPrivatePrescriptionCreate.as_view(),
         name='api_private_patient_prescription_create'),
    path(f'{version}/private/appointment/prescription/list',
         prescriptions_api.ApiPrivatePatientPrescriptionList.as_view(),
         name='api_private_patient_prescription_list'),
    path(f'{version}/private/appointment/prescription/dismissed_list',
         prescriptions_api.ApiPrivatePatientDismissedPrescriptionList.as_view(),
         name='api_private_patient_prescription_dismissed_list'),
    path(f'{version}/private/prescription/detail',
         prescriptions_api.ApiPrivatePatientPrescriptionDetail.as_view(),
         name='api_private_prescription_detail'),
    path(f'{version}/private/appointment/prescription/delete',
         prescriptions_api.ApiPrivatePatientPrescriptionRemove.as_view(),
         name='api_private_appointment_prescription_delete'),
    path(f'{version}/private/appointment/prescription/undismiss',
         prescriptions_api.ApiPrivatePatientPrescriptionUndismiss.as_view(),
         name='api_private_appointment_prescription_undismiss'),

    #############################################################################
    # Notifications
    #############################################################################
    path(f'{version}/private/notifications/appointments/list',
         doctor_notifications_api.ApiPrivateDoctorAppointmentNotificationsList.as_view(),
         name='api_private_notifications_appointments_list'),
    path(f'{version}/private/notifications/appointments/clear',
         doctor_notifications_api.ApiPrivateDoctorAppointmentNotificationsDelete.as_view(),
         name='api_private_notifications_appointments_clear'),

    #############################################################################
    # Analytics
    #############################################################################

    # patient analytics
    path(f'{version}/analytics/agg/patient/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_checkup_aggregate_counts'),
    path(f'{version}/analytics/agg/symptoms/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupSymptomsAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_symptoms_aggregate_counts'),
    path(f'{version}/analytics/agg/findings/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupFindingsAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_findings_aggregate_counts'),
    path(f'{version}/analytics/agg/diagnoses/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupDiagnosesAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_diagnoses_aggregate_counts'),
    path(f'{version}/analytics/agg/prescriptions/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupPrescriptionsAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_prescriptions_aggregate_counts'),
    path(f'{version}/analytics/agg/labtests/by_checkup/counts',
         patient_analytics_api.ApiAnalyticsPatientByCheckupLabtestsAggregateCounts.as_view(),
         name='api_private_doctor_patient_analytics_by_labtests_aggregate_counts'),
]

#############################################################################
# Questionnaire
#############################################################################
questionnaire_admin_router = routers.DefaultRouter()
questionnaire_admin_router.register(r'q', questionnaire_api.QuestionnaireViewSet)
questionnaire_admin_router.register(r'dq', questionnaire_api.DoctorQuestionnaireViewSet)
questionnaire_admin_router.register(r'qs', questionnaire_api.QuestionnaireSectionViewSet)
questionnaire_admin_router.register(r'qq', questionnaire_api.QuestionViewSet)
questionnaire_admin_router.register(r'sq', questionnaire_api.SectionQuestionViewSet)
questionnaire_admin_router.register(r'c', questionnaire_api.ChoiceViewSet)
questionnaire_admin_router.register(r'cg', questionnaire_api.ChoiceGroupViewSet)
questionnaire_admin_router.register(r'cgi', questionnaire_api.ChoiceGroupItemViewSet)
questionnaire_admin_router.register(r'qcg', questionnaire_api.QuestionChoiceGroupViewSet)

READ_ONLY = {
    'get': 'list'
}

DETAIL = {
    'get': 'retrieve'
}

CREATE = {
    'get': 'list',
    'post': 'create',
}

UPDATE = {
    'get': 'retrieve',
    'put': 'update',
    # 'patch': 'update_partial'
}

DELETE = {
    'get': 'retrieve',
    'delete': 'destroy'
}

# admin
urlpatterns += [
    path(f'{version}/admin/questionnaires/', include(questionnaire_admin_router.urls)),

]

# public
urlpatterns += [
    # Questionnaire
    path(f'{version}/public/questionnaires/',
         questionnaire_api.ApiQuestionnairePublicViewSet.as_view(READ_ONLY),
         name='api_public_questionnaires'
         ),
    path(f'{version}/public/questionnaires/<pk>/detail',
         questionnaire_api.ApiQuestionnairePublicViewSet.as_view(DETAIL),
         name='api_public_questionnaires_detail'
         ),

    # Doctor Questionnaire
    path(f'{version}/public/doctor_questionnaires/<doctor_id>/list',
         questionnaire_api.ApiDoctorQuestionnairePublicViewSet.as_view(READ_ONLY),
         name='api_public_doctor_questionnaires'
         ),
    path(f'{version}/public/doctor_questionnaires/<doctor_id>/<pk>/detail',
         questionnaire_api.ApiDoctorQuestionnairePublicViewSet.as_view(DETAIL),
         name='api_public_doctor_questionnaires_detail'
         ),

    # Questionnaire Section
    path(f'{version}/public/questionnaires/<questionnaire_id>/sections/list',
         questionnaire_api.ApiQuestionnaireSectionPublicViewSet.as_view(READ_ONLY),
         name='api_public_questionnaire_sections'),
    path(f'{version}/public/questionnaires/<questionnaire_id>/sections/<index>/detail',
         questionnaire_api.ApiQuestionnaireSectionPublicViewSet.as_view(READ_ONLY),
         name='api_public_questionnaire_sections_detail'),

    # Question
    path(f'{version}/public/questions/list',
         questionnaire_api.ApiQuestionPublicViewSet.as_view(READ_ONLY),
         name='api_public_questions'),
    path(f'{version}/public/questions/<pk>/detail',
         questionnaire_api.ApiQuestionPublicViewSet.as_view(READ_ONLY),
         name='api_public_questions_detail'),

    # Section Question
    path(f'{version}/public/section_questions/list',
         questionnaire_api.ApiSectionQuestionPublicViewSet.as_view(READ_ONLY),
         name='api_public_section_questions'),
    path(f'{version}/public/section_questions/<pk>/detail',
         questionnaire_api.ApiSectionQuestionPublicViewSet.as_view(READ_ONLY),
         name='api_public_section_questions_detail'),
]

# private
urlpatterns += [
    # Questionnaire
    path(f'{version}/private/questionnaires/',
         questionnaire_api.ApiQuestionnairePrivateViewSet.as_view(CREATE),
         name='api_private_questionnaires'
         ),
    path(f'{version}/private/questionnaires/<pk>/detail',
         questionnaire_api.ApiQuestionnairePrivateViewSet.as_view(DETAIL),
         name='api_private_questionnaires_detail'
         ),
    path(f'{version}/private/questionnaires/<pk>/update',
         questionnaire_api.ApiQuestionnairePrivateViewSet.as_view(UPDATE),
         name='api_private_questionnaires_update'
         ),
    path(f'{version}/private/questionnaires/<pk>/delete',
         questionnaire_api.ApiQuestionnairePrivateViewSet.as_view(DELETE),
         name='api_private_questionnaires_detail'
         ),

    # Doctor Questionnaire
    path(f'{version}/private/doctor_questionnaires/<doctor_id>/list',
         questionnaire_api.ApiDoctorQuestionnairePrivateViewSet.as_view(CREATE),
         name='api_private_doctor_questionnaires'
         ),
    path(f'{version}/private/doctor_questionnaires/<doctor_id>/<pk>/detail',
         questionnaire_api.ApiDoctorQuestionnairePrivateViewSet.as_view(DETAIL),
         name='api_private_doctor_questionnaires_detail'
         ),
    path(f'{version}/private/doctor_questionnaires/<doctor_id>/<pk>/update',
         questionnaire_api.ApiDoctorQuestionnairePrivateViewSet.as_view(UPDATE),
         name='api_private_doctor_questionnaires_update'
         ),
    path(f'{version}/private/doctor_questionnaires/<doctor_id>/<pk>/delete',
         questionnaire_api.ApiDoctorQuestionnairePrivateViewSet.as_view(DELETE),
         name='api_private_doctor_questionnaires_detail'
         ),

    # Questionnaire Section
    path(f'{version}/private/questionnaires/<questionnaire_id>/sections/list',
         questionnaire_api.ApiQuestionnaireSectionPrivateViewSet.as_view(CREATE),
         name='api_private_questionnaire_sections'),
    path(f'{version}/private/questionnaires/<questionnaire_id>/sections/<index>/detail',
         questionnaire_api.ApiQuestionnaireSectionPrivateViewSet.as_view(DETAIL),
         name='api_private_questionnaire_section_detail'),
    path(f'{version}/private/questionnaires/<questionnaire_id>/sections/<index>/update',
         questionnaire_api.ApiQuestionnaireSectionPrivateViewSet.as_view(UPDATE),
         name='api_private_questionnaire_section_update'),
    path(f'{version}/private/questionnaires/<questionnaire_id>/sections/<index>/delete',
         questionnaire_api.ApiQuestionnaireSectionPrivateViewSet.as_view(DELETE),
         name='api_private_questionnaire_section_delete'),

    # Question
    path(f'{version}/private/questions/list',
         questionnaire_api.ApiQuestionPrivateViewSet.as_view(CREATE),
         name='api_private_questions'),
    path(f'{version}/private/questions/<pk>/detail',
         questionnaire_api.ApiQuestionPrivateViewSet.as_view(DETAIL),
         name='api_private_questions_detail'),
    path(f'{version}/private/questions/<pk>/update',
         questionnaire_api.ApiQuestionPrivateViewSet.as_view(UPDATE),
         name='api_private_questions_update'),
    path(f'{version}/private/questions/<pk>/delete',
         questionnaire_api.ApiQuestionPrivateViewSet.as_view(DELETE),
         name='api_private_questions_delete'),
    path(f'{version}/private/questions/search',
         questionnaire_api.ApiQuestionSearchPrivateView.as_view(),
         name='api_private_questions_search'),

    # Section Questions
    path(f'{version}/private/section_questions/list',
         questionnaire_api.ApiSectionQuestionPrivateViewSet.as_view(CREATE),
         name='api_private_section_questions'),
    path(f'{version}/private/section_questions/<pk>/detail',
         questionnaire_api.ApiSectionQuestionPrivateViewSet.as_view(DETAIL),
         name='api_private_section_questions_detail'),
    path(f'{version}/private/section_questions/<pk>/update',
         questionnaire_api.ApiSectionQuestionPrivateViewSet.as_view(UPDATE),
         name='api_private_section_questions_update'),
    path(f'{version}/private/section_questions/<pk>/delete',
         questionnaire_api.ApiSectionQuestionPrivateViewSet.as_view(DELETE),
         name='api_private_section_questions_delete'),
]
