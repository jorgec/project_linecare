import pytest
from django.test import TransactionTestCase
from faker import Faker

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution

pytestmark = pytest.mark.django_db
fake = Faker()


class TestDoctorSchedules(TransactionTestCase):
    def test_init(self):
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
        assert user2 is not None, "User 2 was not created"

        receptionist = user2.create_receptionist_profile()
        assert receptionist is not None, "Receptionist Profile 1 was not created"

        email = fake.email()
        password = fake.password()
        user3 = Account.objects.create_user(email=email, password=password)
        assert user3 is not None, "User 3 was not created"

        mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert mi_type is not None, "Type was not created"

        mi = MedicalInstitution.objects.create(
            name=fake.name(),
            type=mi_type,
            added_by=user
        )
        assert mi, f"{fake.name()} not created: {mi}"

        d1_mi1 = doctor.connect_medical_institution(
            medical_institution=mi
        )
        assert d1_mi1, f"Connection between {doctor} and {mi} not created"

        d1_r1 = doctor.connect_receptionist(
            medical_institution=mi,
            receptionist=receptionist
        )
        assert d1_r1, f"Connection between {doctor} and {receptionist} at {mi} not created"

        s1r, s1m, s1s = doctor.create_schedule(
            medical_institution=mi,
            start_time='8:00',
            end_time='11:00',
            start_date='2019-12-01',
            end_date='2019-12-31',
            days='Monday;Tuesday'
        )
        assert s1r, f"Schedule not created for {doctor} at {mi}"

        s1r, s1m, s1s = doctor.create_schedule(
            medical_institution=mi,
            start_time='12:00pm',
            end_time='17:00',
            start_date='2019-12-01',
            end_date='2019-12-31',
            days='Monday;Tuesday'
        )
        assert s1r, f"Schedule not created for {doctor} at {mi}"

        a1res, a1, a1status = user3.base_profile().create_appointment(
            doctor_id=doctor.id,
            medical_institution_id=mi.id,
            day='2019-12-02',
            time_start='9:00',
            time_end='9:30',
            appointment_type='checkup'
        )
        assert a1, f"{a1status}: {user3} appointment with {doctor} at {mi} on 2019-12-02 not created: {a1}"

        schedules = doctor.get_active_schedules()
        assert schedules.count() == 2, f"Expected 2, got {schedules.count()}"
        assert s1s in schedules, f"{s1s} not in {schedules}"
