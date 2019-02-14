"""
Schedules and Appointments

Scenario: Doctor can create schedule
Test Cases
#       Description                                                     Test Data
1       Assert response 201 when valid schedule is entered
2       Check if schedule is stored in DB
3       Assert 400
"""
import pytest
from django.db import transaction
from django.test import TransactionTestCase
from factory import LazyAttribute, SubFactory, LazyFunction
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import DoctorProfile, MedicalInstitution, MedicalInstitutionType, PatientAppointment, \
    DoctorSchedule
from doctor_profiles.modules.api.doctor_schedule_api import ApiDoctorScheduleCreate, ApiDoctorScheduleDayList, \
    ApiDoctorScheduleList, ApiDoctorScheduleDelete, ApiDoctorScheduleAppointmentCreate
from profiles.models import BaseProfile
from receptionist_profiles.models import ReceptionistProfile

pytestmark = pytest.mark.django_db
apifactory = APIRequestFactory()
apiclient = APIClient()
fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = Account


class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = DoctorProfile

    user = SubFactory(UserFactory)


class ReceptionistFactory(DjangoModelFactory):
    class Meta:
        model = ReceptionistProfile

    user = SubFactory(UserFactory)


class MedicalInstitutionTypeFactory(DjangoModelFactory):
    class Meta:
        model = MedicalInstitutionType


class MedicalInstitutionFactory(DjangoModelFactory):
    class Meta:
        model = MedicalInstitution

    type = SubFactory(MedicalInstitutionTypeFactory)
    added_by = SubFactory(UserFactory)


MWF = "Monday^Wednesday^Friday"
TTHS = "Tuesday^Thursday^Saturday"
WKND = "Saturday^Sunday"


class TestCreateScheduleAndAppointment(TransactionTestCase):
    def test_doctor_create_schedule_and_set_appointment(self):
        user = UserFactory(email=fake.email())
        user2 = UserFactory(email=fake.email())
        user3 = UserFactory(email=fake.email())
        user4 = UserFactory(email=fake.email())
        doctor = user.create_doctor_profile()
        doctor2 = user2.create_doctor_profile()
        receptionist = user3.create_receptionist_profile()
        receptionist2 = user4.create_receptionist_profile()
        mi = MedicalInstitutionFactory(name=fake.name())
        doctor.connect_medical_institution(medical_institution=mi)
        receptionist.create_connection(doctor=doctor, medical_institution=mi)
        receptionist.create_connection(doctor=doctor2, medical_institution=mi)
        receptionist2.create_connection(doctor=doctor2, medical_institution=mi)

        patient = UserFactory(email=fake.email())
        patient2 = UserFactory(email=fake.email())
        patient3 = UserFactory(email=fake.email())
        patient4 = UserFactory(email=fake.email())

        TimeDim.objects.preload_times()
        DateDim.objects.preload_year(year=2018)
        DateDim.objects.preload_year(year=2019)

        d1 = DateDim.objects.parse_get('2019-12-01')
        d2 = DateDim.objects.parse_get('2019-12-31')
        form_data = {
            "start_time": "7:00am",
            "end_time": "5:00pm",
            "start_date": str(d1),
            "end_date": str(d2),
            "doctor_id": doctor.id,
            "medical_institution_id": mi.id,
            "days": MWF
        }

        request = apifactory.post('/', form_data)
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        schedule1 = DoctorSchedule.objects.get(id=response.data.get('id'))
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"
        assert schedule1 is not None, f"Schedule was not stored in DB: {response.data}"

        request = apifactory.get('/', {'id': schedule1.id})
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleDayList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        request = apifactory.get('/', {'id': doctor.id, 'medical_institution': mi.id})
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        request = apifactory.get('/', {'id': doctor.id, 'filter_days': WKND})
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
        assert response.data == [], f"Expected [], got {response.data}"

        form_data = {
            "start_time": "7:00am",
            "end_time": "5:00pm",
            "start_date": '2018-10-10',
            "end_date": '2018-10-20',
            "doctor_id": doctor.id,
            "medical_institution_id": mi.id,
            "days": MWF
        }

        request = apifactory.post('/', form_data)
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        schedule = DoctorSchedule.objects.get(id=response.data.get('id'))
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"
        assert schedule is not None, f"Schedule was not stored in DB: {response.data}"

        request = apifactory.get('/', {'id': doctor.id, 'include_past': 'yes'})
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
        assert len(response.data) == 2, f"Expected 2, got {len(response.data)}: {response.data}"

        """ appointments """
        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': '2019-11-25',
            'appointment_type': 'checkup',
            'schedule_day_id': schedule.get_schedule_days().first().id
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, patient)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}: {appointment_data}: {schedule.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, patient)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id,
            'force_schedule': 'true',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, patient)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id,
            'force_schedule': 'true',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, doctor2.user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id,
            'force_schedule': 'true',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, receptionist2.user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id,
            'force_schedule': 'true',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        appointment_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': mi.id,
            'profile_id': patient.id,
            'appointment_day': str(schedule1.get_schedule_days().first().day),
            'appointment_type': 'checkup',
            'schedule_day_id': schedule1.get_schedule_days().first().id,
            'force_schedule': 'true',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = apifactory.post('/', appointment_data)
        force_authenticate(request, receptionist.user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}: {appointment_data}: {schedule1.get_schedule_days()}"

        """ delete schedule """

        request = apifactory.post('/', {'id': schedule.id})
        force_authenticate(request, doctor2.user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {doctor2} should not be able to delete schedule of {doctor}"

        request = apifactory.post('/', {'id': schedule.id})
        force_authenticate(request, receptionist2.user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {receptionist2} should not be able to delete schedule of {doctor}"

        request = apifactory.post('/', {'id': schedule.id})
        force_authenticate(request, patient)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {patient} should not be able to delete schedule of {doctor}"

        request = apifactory.post('/', {'id': schedule.id})
        force_authenticate(request, doctor.user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
