import pytest
from django.test import TransactionTestCase
from faker import Faker

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution

pytestmark = pytest.mark.django_db
fake = Faker()


class TestDoctorQuestionnaire(TransactionTestCase):
    doctor = None
    doctor2 = None
    receptionist = None
    receptionist2 = None
    patient = None
    patient2 = None
    mi = None
    questionnaire1 = None
    questionnaire2 = None
    questionnaire3 = None

    def test_init(self):
        email = fake.email()
        password = fake.password()
        user = Account.objects.create_user(email=email, password=password)
        assert user is not None, "User was not created"

        self.doctor = user.create_doctor_profile()
        assert self.doctor is not None, "Doctor Profile was not created"

        email = fake.email()
        password = fake.password()
        user2 = Account.objects.create_user(email=email, password=password)
        assert user2 is not None, "User 2 was not created"

        self.doctor2 = user2.create_doctor_profile()
        assert self.doctor2 is not None, "Doctor Profile 2 was not created"

        mi_type = MedicalInstitutionType.objects.create(name='Hospital')
        assert mi_type is not None, "Type was not created"

        self.mi = MedicalInstitution.objects.create(
            name=fake.name(),
            type=mi_type,
            added_by=user
        )
        assert self.mi, f"{fake.name()} not created: {self.mi}"

        d1_mi1 = self.doctor.connect_medical_institution(
            medical_institution=self.mi
        )
        assert d1_mi1, f"Connection between {self.doctor} and {self.mi} not created"

        email = fake.email()
        password = fake.password()
        self.patient = Account.objects.create_user(email=email, password=password)
        assert self.patient is not None, "User 3/Patient 1 was not created"

        email = fake.email()
        password = fake.password()
        self.patient2 = Account.objects.create_user(email=email, password=password)
        assert self.patient2 is not None, "User 4/Patient 2 was not created"

        email = fake.email()
        password = fake.password()
        user5 = Account.objects.create_user(email=email, password=password)
        assert user5 is not None, "User 5 was not created"

        self.receptionist = user5.create_receptionist_profile()

        email = fake.email()
        password = fake.password()
        user6 = Account.objects.create_user(email=email, password=password)
        assert user6 is not None, "User 6 was not created"

        self.receptionist2 = user6.create_receptionist_profile()

        d1_r1 = self.doctor.connect_receptionist(
            medical_institution=self.mi,
            receptionist=self.receptionist
        )
        assert d1_r1, f"Connection between {self.doctor} and {self.receptionist} at {self.mi} not created"

    def test_create_questionnaire_for_mi(self):
        self.test_init()
        result, self.questionnaire1, message = self.doctor.create_questionnaire(
            medical_institution=self.mi,
            restriction='internal',
            is_required=True,
            name='Sample Questionnaire',
            description='This is a tribute to the greatest questionnaire in the world'
        )

        assert result, "Questionnaire was not created"
        assert len(self.questionnaire1.get_sections()) > 0, \
            "Sections were not automatically generated"

        result, self.questionnaire2, message = self.doctor.create_questionnaire(
            medical_institution=self.mi,
        )
        assert self.questionnaire2.name == f'{self.doctor} Patient Questionnaire ({self.mi}', \
            f"Expecting '{self.doctor} Patient Questionnaire ({self.mi}', got '{self.questionnaire2.name}'"
        assert self.questionnaire2.is_required is False, \
            f"Expecting False, got '{self.questionnaire2.is_required}'"
        assert self.questionnaire2.restriction == 'private', \
            f"Expecting 'private', got '{self.questionnaire2.restriction}'"

        invalid_add_result, invalid_add_message = self.doctor2.add_questionnaire(
            questionnaire=self.questionnaire1,
            medical_institution=self.mi
        )

        assert invalid_add_result is False, \
            f"Questionnaire was added by a doctor not in the same institution: {invalid_add_message}"

    def test_create_public_questionnaire(self):
        self.test_init()
        result, self.questionnaire1, message = self.doctor.create_questionnaire(
            restriction='public'
        )

        valid_add_result, valid_add_message = self.doctor2.add_questionnaire(
            questionnaire=self.questionnaire1
        )

        assert valid_add_result, f"{self.doctor2} unable to add {self.questionnaire1}: {valid_add_message}"

        doctor_questionnaires = self.doctor2.get_questionnaires()
        assert len(doctor_questionnaires) > 0, \
            f"{self.doctor2} should have 1 questionnaire, got {len(doctor_questionnaires)}"

    def test_add_sections(self):
        self.test_init()
        result, self.questionnaire1, message = self.doctor.create_questionnaire()

        self.questionnaire1.add_section()
        assert len(self.questionnaire1.get_sections()) == 1, \
            f"Expected 1, got {len(self.questionnaire1.get_sections())}"

        self.questionnaire1.add_section(
            order=0,
            name='General History'
        )
        assert len(self.questionnaire1.get_sections()) == 2, \
            f"Expected 2, got {len(self.questionnaire1.get_sections())}"
        assert self.questionnaire1.get_section()[0].name == 'General History', \
            f"Expected 'General History', got {self.questionnaire1.get_section()[0].name}"
