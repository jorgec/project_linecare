import pytest
from django.test import TransactionTestCase
from faker import Faker

from accounts.models import Account
from datesdim.models import DateDim, TimeDim
from doctor_profiles.models import MedicalInstitutionType, MedicalInstitution
from doctor_profiles.models import Questionnaire, QuestionnaireSection, Question, ChoiceGroup, Choice

from doctor_profiles.constants import ANSWER_DATA_TYPES, ANSWER_SELECTION_TYPES, ANSWER_TYPES

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
    questionnaire4 = None

    def test_01_init(self):
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

    def test_02_create_questionnaire_for_mi(self):
        self.test_01_init()
        result, self.questionnaire1, message = self.doctor.create_questionnaire(
            medical_institution=self.mi,
            restriction='internal',
            is_required=True,
            name='Sample Questionnaire',
            description='This is a tribute to the greatest questionnaire in the world'
        )

        assert result, "Questionnaire was not created"
        assert len(self.questionnaire1.get_sections()) == 0, \
            "Sections were still automatically generated"

        result, self.questionnaire2, message = self.doctor.create_questionnaire(
            medical_institution=self.mi
        )
        assert self.questionnaire2.name == f'{self.doctor} Patient Questionnaire', \
            f"Expecting '{self.doctor} Patient Questionnaire', got '{self.questionnaire2.name}'"
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

    def test_03_create_public_questionnaire(self):
        self.test_01_init()
        result, self.questionnaire1, message = self.doctor2.create_questionnaire(
            restriction='public'
        )

        assert result, f"Questionnaire not created"
        assert self.questionnaire1.restriction == 'public', f"Expected 'public', got {self.questionnaire1.restriction}"

        valid_add_result, valid_add_message = self.doctor.add_questionnaire(
            questionnaire=self.questionnaire1,
            medical_institution=self.mi
        )

        assert valid_add_result, f"Unable to add {self.questionnaire1}: {valid_add_message}: {self.doctor.get_medical_institutions()}"

        doctor_questionnaires = self.doctor.get_questionnaires()
        assert len(doctor_questionnaires) > 0, \
            f"{self.doctor} should have > 0 questionnaires, got {len(doctor_questionnaires)}"

    def test_04_add_sections(self):
        self.test_01_init()
        result, self.questionnaire1, message = self.doctor.create_questionnaire()

        section1 = self.questionnaire1.add_section(
            name='test section'
        )
        assert len(self.questionnaire1.get_sections()) == 1, \
            f"Expected 1, got {len(self.questionnaire1.get_sections())}"

        section2 = self.questionnaire1.add_section(
            order=0,
            name='General History'
        )
        assert len(self.questionnaire1.get_sections()) == 2, \
            f"Expected 3, got {len(self.questionnaire1.get_sections())}"
        assert self.questionnaire1.section(1).name == 'General History', \
            f"Expected 'General History', got {self.questionnaire1.section(2).name}"

        question1 = Question.objects.create(
            name='question 1',
            text='question text'
        )
        q2r, question2, q2m = self.questionnaire1.section(0).create_question(
            name='question 2',
            text='this is question 2',
            order=0
        )

        q3r, question3, q3m = self.questionnaire1.section(0).create_question(
            name='question 3',
            text='this is question 3'
        )

        q4r, question4, q4m = self.questionnaire1.section(0).create_question(
            name='question4',
            text='question text',
            answer_type='multiple_choice',
            answer_selection_type='single_answer',
            answer_data_type='numeric'
        )

        assert q2r, f"Q2 was not created: {q2m}"
        assert q3r, f"Q3 was not created: {q3m}"
        assert q4r, f"Q4 was not created: {q4m}"

        choice_group_1 = ChoiceGroup.objects.create(
            name='choice group 1',
            choices=[
                {
                    "name": "choice 1",
                    "text": "choice 1 text",
                    "value": 5,
                    "order": 0,
                },
                {
                    "name": "choice 2",
                    "text": "choice 2 text",
                    "value": 4,
                    "order": 4
                },
                {
                    "name": "choice 3",
                    "text": "choice 3 text",
                    "value": 3
                },
                {
                    "name": "choice 4",
                    "text": "choice 4 text",
                    "value": 2
                },
                {
                    "name": "choice 5",
                    "text": "choice 5 text",
                    "value": 1
                },
            ]
        )

        question4.add_choice_group(choice_group_1)
        qchoices = question4.get_choices()
        assert qchoices, f"Choices were not added to {question4}"
        assert len(qchoices) == 5, f"Expected 5, got {len(qchoices)}: {qchoices}"
        assert question4.get_choice(0).name == 'choice 1', f"Expected choice 1, got {question4.get_choice(0).name} instead"
        assert question4.get_choice(4).name == 'choice 2', f"Expected choice 2, got {question4.get_choice(4).name} instead: {qchoices}"
        assert len(question4.get_choices()) == 5, f"Expected 5, got {len(question4.get_choices())} instead"

    def test_05_shortcuts(self):
        self.test_01_init()
        self.questionnaire4 = Questionnaire.objects.create_raw(
            {
                "name": "Questionnaire 4",
                "restriction": "public",
                "is_required": True,
                "description": "This is also a tribute to the greatest questionnaire in the world",
                "sections": [
                    {
                        "name": "Questionnaire 4 Section 1",
                        "order": 0,
                        "questions": [
                            {
                                "name": "q1",
                                "text": "q1 text",
                                "answer_type": "free_text",
                                "answer_selection_type": "single_answer",
                                "answer_data_type": "text",
                                "order": 0,
                                "choices": [
                                    {
                                        "text": "q1 c1",
                                        "value": 1
                                    },
                                    {
                                        "text": "q1 c2",
                                        "value": 2
                                    },
                                ]
                            },
                            {
                                "name": "q2",
                                "text": "q2 text",
                            }
                        ]
                    },
                    {
                        "name": "Questionnaire 4 Section 2",
                        "questions": None
                    }
                ]
            }
        )

        assert self.questionnaire4, "Questionnaire was not created"
        assert len(self.questionnaire4.get_sections()) == 2, f"Expected 2, got {len(self.questionnaire4.get_sections())}"
        assert self.questionnaire4.section(0).name == "Questionnaire 4 Section 1", f"Expected 'Questionnaire 4 Section 1', got {self.questionnaire4.section(2).name} instead"
        assert len(self.questionnaire4.section(0).get_questions()) == 2, f"Expected 2, got {len(self.questionnaire4.section(0).get_questions())} instead"
