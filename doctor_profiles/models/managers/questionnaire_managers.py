from django.db import models
from django.apps import apps

class QuestionnaireManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(QuestionnaireManager, self).create(*args, **kwargs)

    def create_by_user(self, *args, **kwargs):
        """
        Returns:
        result: bool, object: Questionnaire or None, message: str
        """
        creator = kwargs.get('created_by', None)
        BaseProfile = apps.get_model('profiles.BaseProfile')
        MedicalInstitution = apps.get_model('doctor_profiles.MedicalInstitution')
        DoctorQuestionnaire = apps.get_model('doctor_profiles.DoctorQuestionnaire')
        try:
            if creator:
                created_by = BaseProfile.objects.get(id=creator.id)
            else:
                return False, None, "Required: created_by"
        except BaseProfile.DoesNotExist:
            return False, None, "Required: user does not exist"

        questionnaire = self.create(
            is_approved=kwargs.get('is_approved', True),
            name=kwargs.get('name'),
            is_required=kwargs.get('is_required', False),
            description=kwargs.get('description', None),
            created_by=created_by,
            restriction=kwargs.get('restriction', 'private')
        )

        if created_by.user.doctor_profile() or created_by.user.receptionist_profile():
            if created_by.user.doctor_profile():
                doctor = created_by.user.doctor_profile()
            else:
                doctor = None

            mi = kwargs.get('medical_institution', None)
            medical_institution = None
            if restriction == 'internal' and not mi:
                questionnaire.restriction = 'private'
                questionnaire.save()
                return False, questionnaire, "Questionnaire restriction set to 'internal' but no Medical Institution was provided; reverting to 'private'"
            if mi:
                try:
                    medical_institution = MedicalInstitution.objects.get(id=mi.id)
                except MedicalInstitution.DoesNotExist:
                    return False, questionnaire, "Medical Institution does not exist"
            DoctorQuestionnaire.objects.create(
                doctor=doctor,
                medical_institution=medical_institution,
                questionnaire=questionnaire,
                is_creator=True
            )

        return True, questionnaire, f"{questionnaire.name} created!"




class DoctorQuestionnaireManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(DoctorQuestionnaireManager, self).create(*args, **kwargs)
