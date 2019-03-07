import pytest
from django.db import transaction
from django.test import TransactionTestCase
from faker import Faker
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution
from doctor_profiles.modules.api.patient_appointment_api import ApiPatientAppointmentList, \
    ApiPatientAppointmentUpdateStatus

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()
client = APIClient()
fake = Faker()


class TestPatientAppointmentApi(TransactionTestCase):
    user = None
    user2 = None
    user3 = None
    user4 = None
    user5 = None
    user6 = None
    doctor = None
    doctor2 = None
    receptionist = None
    receptionist2 = None
    mi = None
    mi2 = None
    mi_type = None
    s1r, s1m, s1s = None, None, None
    a1res, a1, a1status = None, None, None

    def test_init(self):
        DateDim.objects.preload_year(year=2019)
        TimeDim.objects.preload_times()

        email = fake.email()
        password = fake.password()
        self.user = Account.objects.create_user(email=email, password=password)
        assert self.user is not None, "User was not created"

        self.doctor = self.user.create_doctor_profile()
        assert self.doctor is not None, "Doctor Profile was not created"

        email = fake.email()
        password = fake.password()
        self.user4 = Account.objects.create_user(email=email, password=password)
        assert self.user4 is not None, "User 4 was not created"

        self.doctor2 = self.user4.create_doctor_profile()
        assert self.doctor2 is not None, "Doctor Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        self.user2 = Account.objects.create_user(email=email, password=password)
        assert self.user2 is not None, "User 2 was not created"

        self.receptionist = self.user2.create_receptionist_profile()
        assert self.receptionist is not None, "Receptionist Profile 1 was not created"

        email = fake.email()
        password = fake.password()
        self.user3 = Account.objects.create_user(email=email, password=password)
        assert self.user3 is not None, "User 3 was not created"

        self.receptionist2 = self.user3.create_receptionist_profile()
        assert self.receptionist2 is not None, "Receptionist Profile 2 was not created"

        email = fake.email()
        password = fake.password()
        self.user5 = Account.objects.create_user(email=email, password=password)
        assert self.user5 is not None, "User 5 was not created"

        email = fake.email()
        password = fake.password()
        self.user6 = Account.objects.create_user(email=email, password=password)
        assert self.user6 is not None, "User 6 was not created"

        self.mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert self.mi_type is not None, "Type was not created"

        m1_name = fake.name()

        self.mi = MedicalInstitution.objects.create(
            name=m1_name,
            type=self.mi_type,
            added_by=self.user
        )
        assert self.mi, f"{m1_name} not created: {self.mi}"

        self.mi2 = MedicalInstitution.objects.create(
            name=fake.name(),
            type=self.mi_type,
            added_by=self.user6
        )
        assert self.mi, f"{self.mi2.name} not created: {self.mi2}"

        d1_mi1 = self.doctor.connect_medical_institution(
            medical_institution=self.mi
        )
        assert d1_mi1, f"Connection between {self.doctor} and {self.mi} not created"

        d1_r1 = self.doctor.connect_receptionist(
            medical_institution=self.mi,
            receptionist=self.receptionist
        )
        assert d1_r1, f"Connection between {self.doctor} and {self.receptionist} at {self.mi} not created"

        self.s1r, self.s1m, self.s1s = self.doctor.create_schedule(
            medical_institution=self.mi,
            start_time='8:00',
            end_time='11:00',
            start_date='2019-12-01',
            end_date='2019-12-31',
            days='Monday^Tuesday'
        )
        assert self.s1r, f"Schedule not created for {self.doctor} at {self.mi}"

        self.a1res, self.a1, self.a1status = self.user5.base_profile().create_appointment(
            doctor_id=self.doctor.id,
            medical_institution_id=self.mi.id,
            day='2019-12-02',
            time_start='9:00',
            time_end='9:30',
            appointment_type='checkup'
        )

        assert self.a1, f"{self.a1status}: {self.user5} appointment with {self.doctor} at {self.mi} on 2019-12-02 not created: {self.a1}"
        # /fixtures

        # should pass: same doctor
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)
        assert len(response.data) == 1, f"Expected len(1), got {len(response.data)}: {response.data}"
        assert response.status_code == 200, f"Response: {response.data}^ Expected 200, got {response.status_code}"

        # should pass: same doctor
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 200, f"Response: {response.data}^ Expected 200, got {response.status_code}"
        assert len(response.data) == 1, f"Expected len(1), got {len(response.data)}: {response.data}"

        # should pass: valid receptionist for doctor
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 200, f"Response: {response.data}^ Expected 200, got {response.status_code}"
        assert len(response.data) == 1, f"Expected len(1), got {len(response.data)}: {response.data}"

        # should fail: invalid receptionist for doctor
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.receptionist2.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 403, f"Response: {response.data}^ Expected 403, got {response.status_code}"

        # should fail: different doctor
        request = factory.get('/', {
            'doctor_id': self.doctor2.id,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 401, f"Response: {response.data}^ Expected 401, got {response.status_code}"

        # should fail: not a doctor
        request = factory.get('/', {
            'doctor_id': 3245,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 404, f"Response: {response.data}^ Expected 404, got {response.status_code}"

        # should fail: wrong mi
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
            'medical_institution': 235325,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 404, f"Response: {response.data}^ Expected 404, got {response.status_code}"

        # should fail: wrong mi
        request = factory.get('/', {
            'doctor_id': self.doctor.id,
            'medical_institution': self.mi2.id,
            'day_start': '2019-12-01',
            'day_end': '2019-12-31',
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentList.as_view()(request)

        assert response.status_code == 404, f"Response: {response.data}^ Expected 404, got {response.status_code}"

        # should pass: doctor -> pending
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'pending'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> queueing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'queueing'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> in_progress
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'in_progress'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> finishing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'finishing'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> done
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'done'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> cancelled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_doctor'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: doctor -> rescheduled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_doctor'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        #######################################################################
        # patient
        #######################################################################
        # should pass: patient -> pending
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'pending'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: patient -> queueing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'queueing'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should fail: patient -> in_progress
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'in_progress'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: patient -> finishing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'finishing'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: patient -> done
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'done'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: patient -> cancelled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_doctor'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: patient -> rescheduled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_doctor'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should succeed: patient -> cancelled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_patient'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should succeed: patient -> rescheduled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_patient'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should fail: doctor -> cancelled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_patient'
        })
        force_authenticate(request, user=self.doctor.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: receptionist -> rescheduled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_patient'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: receptionist -> cancelled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_patient'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: receptionist -> rescheduled_by_patient
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_patient'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: invalid appointment
        request = factory.get('/', {
            'appointment_id': 42121,
            'queue_status': 'pending'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.data}"

        # should fail: invalid status
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'pendingasdg'
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should fail: no status
        request = factory.get('/', {
            'appointment_id': self.a1.id,
        })
        force_authenticate(request, user=self.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.data}"

        #######################################################################
        # receptionist
        #######################################################################
        # should pass: receptionist -> pending
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'pending'
        })
        force_authenticate(request, user=self.user5)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should pass: receptionist -> queueing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'queueing'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should succeed: receptionist -> in_progress
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'in_progress'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should succeed: receptionist -> finishing
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'finishing'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should fail: receptionist -> done
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'done'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.data}"

        # should succeed: receptionist -> cancelled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'cancelled_by_doctor'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"

        # should succeed: receptionist -> rescheduled_by_doctor
        request = factory.get('/', {
            'appointment_id': self.a1.id,
            'queue_status': 'rescheduled_by_doctor'
        })
        force_authenticate(request, user=self.receptionist.user)
        response = ApiPatientAppointmentUpdateStatus.as_view()(request)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
