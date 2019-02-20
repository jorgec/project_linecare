from django.db import models
from django.apps import apps
from django.db.models import F
from django.db import IntegrityError

class QuestionnaireManager(models.Manager):
    def create(self, *args, **kwargs):
        QuestionnaireSection = apps.get_model('doctor_profiles.QuestionnaireSection')
        questionnaire = super(QuestionnaireManager, self).create(*args, **kwargs)
        QuestionnaireSection.objects.create(
            questionnaire=questionnaire
        )
        return questionnaire

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
            if kwargs.get('restriction', 'private') == 'internal' and not mi:
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


class QuestionnaireSectionManager(models.Manager):
    
    def create(self, *args, **kwargs):
        __order = kwargs.get('order', None)
        section = None
        if __order:
            try:
                section = super(QuestionnaireSectionManager, self).create(*args, **kwargs)
            except IntegrityError:
                affected_sections = self.filter(
                    questionnaire=kwargs.get('questionnaire'),
                    order__gte=__order
                ).update(
                    order=F('order') + 1
                )
                section = super(QuestionnaireSectionManager, self).create(*args, **kwargs)
        else:
            order = self.filter(
                questionnaire=kwargs.get('questionnaire')
            ).count()
            kwargs['order'] = order
            section = super(QuestionnaireSectionManager, self).create(*args, **kwargs)

        return section


class QuestionManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(QuestionManager, self).create(*args, **kwargs)


class SectionQuestionManager(models.Manager):
    def create(self, *args, **kwargs):
        __order = kwargs.get('order', None)
        section_question = None
        if __order:
            try:
                section_question = super(SectionQuestionManager, self).create(*args, **kwargs)
            except IntegrityError:
                affected = self.filter(
                    section=kwargs.get('section'),
                    order__gte=__order
                ).update(
                    order=F('order') + 1
                )
                section_question = super(SectionQuestionManager, self).create(*args, **kwargs)
        else:
            order = self.filter(
                section=kwargs.get('section')
            ).count()
            kwargs['order'] = order
            section_question = super(SectionQuestionManager, self).create(*args, **kwargs)

        return section_question
