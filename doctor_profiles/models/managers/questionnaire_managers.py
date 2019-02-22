from django.db import models
from django.apps import apps
from django.db.models import F
from django.db import IntegrityError

class QuestionnaireManager(models.Manager):
    def create(self, *args, **kwargs):
        QuestionnaireSection = apps.get_model('doctor_profiles.QuestionnaireSection')

        if not kwargs.get('name', None):
            kwargs['name'] = f"Patient Questionnaire"
        questionnaire = super(QuestionnaireManager, self).create(*args, **kwargs)
        # if kwargs.get('auto_add_section', True):
        #    QuestionnaireSection.objects.create(
        #        questionnaire=questionnaire
        #    )
        return questionnaire

    def create_raw(self, tree: dict):
        questionnaire = self.create(
            name=tree.get('name', None),
            is_required=tree.get('is_required', False),
            description=tree.get('description', None),
            instructions=tree.get('instructions', None),
            restriction=tree.get('restriction', 'private'),
            # auto_add_section=False
        )

        if "sections" in tree:
            __sections = tree.get('sections')
            if __sections:
                for section in tree.get('sections'):
                    __section = questionnaire.add_section(
                        name=section.get('name'),
                        order=section.get('order', None),
                        description=section.get('description', None),
                        instructions=section.get('instructions', None)
                    )
                    if "questions" in section:
                        __questions = section.get('questions')
                        if __questions:
                            for question in __questions:
                                qres, __question, qmsg = __section.create_question(
                                    order=question.get('order', 0),
                                    name=question.get('name', None),
                                    text=question.get('text'),
                                    answer_type=question.get('answer_type', None),
                                    answer_selection_type=question.get('answer_selection_type', None),
                                    answer_data_type=question.get('answer_data_type', None)
                                )
                                if "choices" in question:
                                    choice_group = __question.create_choice_group()
                                    __choices = question.get('choices')
                                    if __choices:
                                        for choice in __choices:
                                            __choice = choice_group.create_choice(
                                                name=choice.get('name', None),
                                                text=choice.get('text'),
                                                value=choice.get('value'),
                                                order=choice.get('order', 0)
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

        if not kwargs.get('name', None):
            kwargs['name'] = f"{created_by.user.doctor_profile()} Patient Questionnaire"

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
        try:
            return super(DoctorQuestionnaireManager, self).create(*args, **kwargs)
        except IntegrityError:
            return self.get(
                doctor=kwargs.get('doctor'),
                medical_institution=kwargs.get('medical_institution'),
                questionnaire=kwargs.get('questionnaire')
            )


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
        __kwargs = {}
        for k, v in kwargs.items():
            if v is not None:
                __kwargs[k] = v

        return super(QuestionManager, self).create(*args, **__kwargs)


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

        return section_question.question


class ChoiceGroupItemManager(models.Manager):
    def create(self, *args, **kwargs):
        choice_group_item = super(ChoiceGroupItemManager, self).create(*args, **kwargs)
        return choice_group_item


class ChoiceGroupManager(models.Manager):
    def create(self, *args, **kwargs):
        Choice = apps.get_model('doctor_profiles.Choice')
        ChoiceGroupItem = apps.get_model('doctor_profiles.ChoiceGroupItem')

        choice_group_kwargs = {
            "name": kwargs.get("name", "Unnamed Choice Group")
        }

        choice_group = super(ChoiceGroupManager, self).create(*args, **choice_group_kwargs)

        if 'choices' in kwargs:
            __choices = []
            for choice in kwargs.get('choices'):
                __choice = Choice.objects.create(
                    name=choice.get('name'),
                    text=choice.get('text'),
                    value=choice.get('value')
                )
                choice_group.add_choice(__choice, order=choice.get('order', 0))
        return choice_group


class QuestionChoiceGroupManager(models.Manager):
    def create(self, *args, **kwargs):
        question = kwargs.get('question', None)
        if self.filter(question=question).count() > 0:
            return False

        return super(QuestionChoiceGroupManager, self).create(*args, **kwargs)
