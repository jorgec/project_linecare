import pytest
import random
from faker import Faker
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution, DoctorSchedule
from doctor_profiles.modules.api.doctor_schedule_api import ApiDoctorScheduleCreate, ApiDoctorScheduleDelete, \
    ApiDoctorScheduleAppointmentCreate, ApiPrivateDoctorScheduleQueueList, ApiPrivateDoctorScheduleCalendar
from doctor_profiles.modules.api.medical_institution_doctors_api import ApiMedicalInstitutionDoctorCreate
from doctor_profiles.modules.api.medical_institutions_api import ApiPrivateMedicalInstitutionCreate
from locations.models import Region, Province, City, Country
from receptionist_profiles.modules.api.receptionist_profile_api import ApiPrivateReceptionistConnectionCreate

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()
client = APIClient()
fake = Faker()


class TestDoctorScheduleApi:

    def test_full_create(self):
        # fixtures
        DateDim.objects.preload_year(year=2019)
        TimeDim.objects.preload_times()

        email = fake.email()
        password = fake.password()
        user = Account.objects.create_user(email=email, password=password)
        assert user is not None, "User was not created"

        doctor = user.create_doctor_profile()
        assert doctor is not None, "Doctor Profile was not created"

        email = fake.email()
        password = fake.password()
        user4 = Account.objects.create_user(email=email, password=password)
        assert user4 is not None, "User 4 was not created"

        doctor2 = user4.create_doctor_profile()
        assert doctor2 is not None, "Doctor Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        user2 = Account.objects.create_user(email=email, password=password)
        assert user2 is not None, "User 2 was not created"

        receptionist = user2.create_receptionist_profile()
        assert receptionist is not None, "Receptionist Profile 1 was not created"

        email = fake.email()
        password = fake.password()
        user3 = Account.objects.create_user(email=email, password=password)
        assert user3 is not None, "User 3 was not created"

        receptionist2 = user3.create_receptionist_profile()
        assert receptionist2 is not None, "Receptionist Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        user5 = Account.objects.create_user(email=email, password=password)
        assert user5 is not None, "User 5 was not created"

        email = fake.email()
        password = fake.password()
        user6 = Account.objects.create_user(email=email, password=password)
        assert user6 is not None, "User 6 was not created"

        mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert mi_type is not None, "Type was not created"

        country = Country.objects.create(name=fake.name())
        assert country is not None, "Country was not created"

        region = Region.objects.create(
            name=fake.name(),
            country=country
        )
        assert region is not None, "Region was not created"

        province = Province.objects.create(
            name=fake.name(),
            region=region,
            country=country
        )
        assert province is not None, "Province was not created"

        city = City.objects.create(
            name=fake.name(),
            province=province
        )
        assert city is not None, "City was not created"
        # /fixtures

        """ create institution 1 """
        m1_name = fake.name()
        m1_zip_code = random.randint(1000, 9999)
        m1_address = fake.address()

        form_data = {
            'name': m1_name,
            'region': region.id,
            'province': province.id,
            'city': city.id,
            'zip_code': m1_zip_code,
            'address': m1_address,
            'type': mi_type.id
        }

        request = factory.post('/', form_data)
        force_authenticate(request, user=user)

        response = ApiPrivateMedicalInstitutionCreate.as_view()(request)
        medical_institution_id = response.data['id']
        medical_institution = MedicalInstitution.objects.get(id=medical_institution_id)
        assert response.status_code == 200, f"Medical Institution creation failed: {response.data} {form_data}"

        """ create institution 2 """
        m2_name = fake.name()
        m2_zip_code = random.randint(1000, 9999)
        m2_address = fake.address()

        form_data = {
            'name': m2_name,
            'region': region.id,
            'province': province.id,
            'city': city.id,
            'zip_code': m2_zip_code,
            'address': m2_address,
            'type': mi_type.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiPrivateMedicalInstitutionCreate.as_view()(request)
        medical_institution_2_id = response.data['id']
        medical_institution_2 = MedicalInstitution.objects.get(id=medical_institution_2_id)
        assert response.status_code == 200, f"Medical Institution 2 creation failed: {response.data} {form_data}"

        """ make connection with doctor 1 """
        form_data = {
            'doctor': doctor.id,
            'medical_institution': medical_institution.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiMedicalInstitutionDoctorCreate.as_view()(request)
        assert response.status_code == 201, f"Connection between {doctor} and {medical_institution} was not created: {response.status_code}: {response.data} with data: {form_data}"

        """ make connection with doctor 2 """
        form_data = {
            'doctor': doctor2.id,
            'medical_institution': medical_institution_2.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user4)
        response = ApiMedicalInstitutionDoctorCreate.as_view()(request)
        assert response.status_code == 201, f"Connection between {doctor2} and {medical_institution_2} was not created: {response.status_code}: {response.data} with data: {form_data}"

        """ make connection with receptionist """
        form_data = {
            'receptionist_id': receptionist.id,
            'medical_institution_id': medical_institution.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user2)
        response = ApiPrivateReceptionistConnectionCreate.as_view()(request)
        assert response.status_code == 201 or response.status_code == 200, f"Connection between {receptionist} and {medical_institution} was not created: {response.status_code}: {response.data} with data: {form_data}"

        """ connect doctor and receptionist in medical institution """
        form_data = {
            'receptionist_id': receptionist.id,
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiPrivateReceptionistConnectionCreate.as_view()(request)
        assert response.status_code == 201, f"Connection between {receptionist} and {doctor} in {medical_institution} was not created: {response.status_code}: {response.data} with data: {form_data}"

        """ create schedule for doctor on medical institution """
        """ schedule 1"""
        form_data = {
            'start_time': '8:00am',
            'end_time': '11:00am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 201, f"Schedule not created for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 1 """

        """ schedule 1b"""
        form_data = {
            'start_time': '8:00am',
            'end_time': '11:00am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Wednesday;Friday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        schedule_to_delete_2 = DoctorSchedule.objects.get(id=response.data['id'])
        assert response.status_code == 201, f"Schedule not created for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 1b """

        """ schedule 1c"""
        form_data = {
            'start_time': '8:00am',
            'end_time': '11:00am',
            'start_date': '2019-11-01',
            'end_date': '2019-11-20',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        schedule_to_delete = DoctorSchedule.objects.get(id=response.data['id'])
        assert response.status_code == 201, f"Schedule not created for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 1c """

        """ schedule 1d"""
        form_data = {
            'start_time': '8:00am',
            'end_time': '11:00am',
            'start_date': '2019-11-01',
            'end_date': '2019-11-20',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': 43543
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        """ /schedule 1d """

        """ schedule 2 -- conflict """
        form_data = {
            'start_time': '8:00am',
            'end_time': '11:00am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 409, f"Conflict expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 2 """

        """ schedule 3 -- conflict """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:00am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 409, f"Conflict expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 3 """

        """ schedule 4 -- conflict """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 409, f"Conflict expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 4 """

        """ schedule 5 -- conflict """
        form_data = {
            'start_time': '9:00am',
            'end_time': '10:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 409, f"Conflict expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 5 """

        """ schedule 6 -- conflict """
        form_data = {
            'start_time': '9:00am',
            'end_time': '1:30pm',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday;Tuesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 409, f"Conflict expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 6 """

        """ schedule 7 -- empty days """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': '',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 400, f"Bad Request expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 7 """

        """ schedule 8 -- authorized receptionist """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Thursday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user2)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 201, f"Receptionist allowed expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8 """

        """ schedule 8b -- different user """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Saturday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user3)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 403, f"Unauthorized expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8b """

        """ schedule 8c -- different user """
        form_data = {
            'start_time': '7:00am',
            'end_time': '11:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Sunday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user4)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 401, f"Unauthorized expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8c """

        """ schedule 8d -- different medical institution """
        form_data = {
            'start_time': '7:00pm',
            'end_time': '11:30pm',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday',
            'medical_institution_id': medical_institution_2.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user3)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 404, f"404 expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8d """

        """ schedule 8e -- not a receptionist """
        form_data = {
            'start_time': '1:00am',
            'end_time': '5:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday',
            'medical_institution_id': medical_institution_2.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user5)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 403, f"403 expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8e """

        """ schedule 8f -- not a doctor """
        form_data = {
            'start_time': '1:00am',
            'end_time': '5:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Monday',
            'medical_institution_id': medical_institution_2.id,
            'doctor_id': user5.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user5)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 403, f"403 expected for {user5} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8f """

        """ schedule 8g -- invalid time """
        form_data = {
            'start_time': '7:00am',
            'end_time': '5:30am',
            'start_date': '2019-12-01',
            'end_date': '2019-12-31',
            'days': 'Wednesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 400, f"400 expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8g """

        """ schedule 8g -- invalid date """
        form_data = {
            'start_time': '1:00am',
            'end_time': '5:30am',
            'start_date': '2019-04-04',
            'end_date': '2019-03-03',
            'days': 'Wednesday',
            'medical_institution_id': medical_institution.id,
            'doctor_id': doctor.id
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleCreate.as_view()(request)
        assert response.status_code == 400, f"400 expected for {doctor} at {medical_institution}: {response.status_code}, {response.data}"

        """ /schedule 8g """

        """ schedule delete - invalid user type """
        form_data = {
            'id': schedule_to_delete.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user5)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"403 expected: {response.status_code}, {response.data}"

        """ schedule delete - invalid doctor """
        form_data = {
            'id': schedule_to_delete.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user4)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"403 expected: {response.status_code}, {response.data}"

        """ schedule delete - invalid receptionist """
        form_data = {
            'id': schedule_to_delete.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=receptionist2.user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 403, f"403 expected: {response.status_code}, {response.data}"

        """ schedule delete - by doctor """
        form_data = {
            'id': schedule_to_delete.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 200, f"200 expected: {response.status_code}, {response.data}"

        """ schedule delete - by receptionist """
        form_data = {
            'id': schedule_to_delete_2.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=receptionist.user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 200, f"200 expected: {response.status_code}, {response.data}"

        """ schedule delete - 404 """
        form_data = {
            'id': schedule_to_delete.id,
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleDelete.as_view()(request)
        assert response.status_code == 404, f"404 expected: {response.status_code}, {response.data}"

        """ create appointment: in the past """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-01-07',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 400 or response.status_code == 404, f"Expected 400, got {response.status_code}: {response.data}"

        """ create appointment: wrong doctor """
        form_data = {
            'doctor_id': doctor2.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        """ create appointment: wrong receptionist """
        form_data = {
            'doctor_id': receptionist2.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user3)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        """ create appointment: wrong user type """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user6)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        """ create appointment: no patient """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"

        """ create appointment: no day """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        """ create appointment: no schedule day """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-03-28',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        """ create appointment: wrong appointment type """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'sdafghsd'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"

    def test_appointments(self):
        # fixtures
        DateDim.objects.preload_year(year=2019)
        TimeDim.objects.preload_times()

        email = fake.email()
        password = fake.password()
        user = Account.objects.create_user(email=email, password=password)
        assert user is not None, "User was not created"

        doctor = user.create_doctor_profile()
        assert doctor is not None, "Doctor Profile was not created"

        email = fake.email()
        password = fake.password()
        user2 = Account.objects.create_user(email=email, password=password)
        assert user2 is not None, "User 4 was not created"

        doctor2 = user2.create_doctor_profile()
        assert doctor2 is not None, "Doctor Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        user3 = Account.objects.create_user(email=email, password=password)
        assert user3 is not None, "User 2 was not created"

        receptionist = user3.create_receptionist_profile()
        assert receptionist is not None, "Receptionist Profile 1 was not created"

        email = fake.email()
        password = fake.password()
        user4 = Account.objects.create_user(email=email, password=password)
        assert user4 is not None, "User 3 was not created"

        receptionist2 = user4.create_receptionist_profile()
        assert receptionist2 is not None, "Receptionist Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        user5 = Account.objects.create_user(email=email, password=password)
        assert user5 is not None, "User 5 was not created"

        email = fake.email()
        password = fake.password()
        user6 = Account.objects.create_user(email=email, password=password)
        assert user6 is not None, "User 6 was not created"

        mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert mi_type is not None, "Type was not created"

        country = Country.objects.create(name=fake.name())
        assert country is not None, "Country was not created"

        region = Region.objects.create(
            name=fake.name(),
            country=country
        )
        assert region is not None, "Region was not created"

        province = Province.objects.create(
            name=fake.name(),
            region=region,
            country=country
        )
        assert province is not None, "Province was not created"

        city = City.objects.create(
            name=fake.name(),
            province=province
        )
        assert city is not None, "City was not created"

        medical_institution = MedicalInstitution.objects.create(
            name=fake.name(),
            type=mi_type,
            added_by=user
        )

        medical_institution_2 = MedicalInstitution.objects.create(
            name=fake.name(),
            type=mi_type,
            added_by=user
        )

        conn1 = doctor.connect_medical_institution(medical_institution=medical_institution)
        assert conn1, f'Connection failed {conn1}'

        recep_doc = doctor.connect_receptionist(medical_institution=medical_institution, receptionist=receptionist)
        assert recep_doc, f'Receptionist connection failed {recep_doc}'

        schedule_result_1, schedule_message_1, schedule_1 = doctor.create_schedule(
            medical_institution=medical_institution,
            start_time='8:00am',
            end_time='11:00am',
            start_date='2019-12-01',
            end_date='2019-12-31',
            days='Monday;Tuesday;Wednesday;Thursday;Friday;Saturday;Sunday'
        )

        assert schedule_result_1, f"Schedule creation failed: {schedule_message_1}, {schedule_1}"

        """ create appointment: first available """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user5.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 201, f"Expected 201 for 2019-12-02, got {response.status_code}: {response.data}: {schedule_1} : {schedule_1.schedule_on_days.all()}"

        """ create appointment: first available - receptionist """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user3)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"

        """ create appointment: first available - bad receptionist """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user4)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        """ create appointment: first available - other doctor """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user2)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.data}"

        """ create appointment: first available - normal user """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'first_available',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup'
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user5)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        """ create appointment: user selection, bad time """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'user_select',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup',
            'appointment_time_start': '7:00am',
            'appointment_time_end': '8:00am',
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        """ create appointment: user selection, bad time """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'user_select',
            'appointment_day': '2019-12-02',
            'appointment_type': 'checkup',
            'appointment_time_start': '7asdgs',
            'appointment_time_end': '8:00am',
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"

        """ create appointment: user selection, bad date """
        form_data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id,
            'profile_id': user6.id,
            'schedule_choice': 'user_select',
            'appointment_day': '2019-12-45',
            'appointment_type': 'checkup',
            'appointment_time_start': '8:00',
            'appointment_time_end': '10:00am',
        }
        request = factory.post('/', form_data)
        force_authenticate(request, user=user)
        response = ApiDoctorScheduleAppointmentCreate.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"

        """ queue schedule """
        data = {
            'doctor_id': doctor.id,
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution_2.id
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'medical_institution_id': 13248
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user6)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"

        data = {
            'doctor_id': 23321,
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'medical_institution_id': medical_institution.id
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user2)
        response = ApiPrivateDoctorScheduleQueueList.as_view()(request)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

        """ calendar """
        data = {
            'doctor_id': doctor.id,
            'year': 2019,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = {
            'year': 2019,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = {
            'doctor_id': 2346,
            'year': 2019,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'year': 2019,
        }
        request = factory.get('/', data)
        force_authenticate(request, user=user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'year': 2019,
            'month': 12,
            'consumer': 'receptionist'
        }
        request = factory.get('/', data)
        force_authenticate(request, user=receptionist.user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'year': 2019,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=doctor2.user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

        data = {
            'doctor_id': doctor.id,
            'year': 2019,
            'month': 12
        }
        request = factory.get('/', data)
        force_authenticate(request, user=receptionist2.user)
        response = ApiPrivateDoctorScheduleCalendar.as_view()(request)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
