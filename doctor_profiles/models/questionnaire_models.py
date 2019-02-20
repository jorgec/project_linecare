from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models as models, IntegrityError
from django.db.models import Q, F
from django_extensions.db import fields as extension_fields
from taggit.managers import TaggableManager

from doctor_profiles.models.managers.questionnaire_managers import QuestionnaireManager, DoctorQuestionnaireManager, QuestionnaireSectionManager, QuestionManager, SectionQuestionManager
from doctor_profiles.constants import ANSWER_DATA_TYPES, ANSWER_SELECTION_TYPES, ANSWER_TYPES, QUESTIONNAIRE_RESTRICTION_CHOICES

class Questionnaire(models.Model):
    """
    The questionnaire model is a wrapper that binds sections, questions, and question choices
    """

    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Main Fields
    name = models.CharField(max_length=255, blank=True, null=True, default='Unnamed Questionnaire')
    slug = extension_fields.AutoSlugField(populate_from='name', unique=True)
    is_required = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, null=True, blank=True, default='')
    instructions = models.CharField(max_length=1024, null=True, blank=True, default='')
    restriction = models.CharField(max_length=60, choices=QUESTIONNAIRE_RESTRICTION_CHOICES, default='private')

    # Relationship Fields
    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_questionnaires', on_delete=models.CASCADE)

    tags = TaggableManager()

    objects = QuestionnaireManager()

    class Meta:
        ordering = ('name', '-created')

    def __str__(self):
        return f"{self.name}"

    """ model methods """
    def add_section(self, **kwargs):
        """
        kwargs:
        - name: str
        - order: int
        - description: str
        - instructions: str
        """

        QuestionnaireSection = apps.get_model('doctor_profiles.QuestionnaireSection')
        kwargs['questionnaire'] = self
        return QuestionnaireSection.objects.create(**kwargs)

    def get_sections(self):
        QuestionnaireSection = apps.get_model('doctor_profiles.QuestionnaireSection')
        return QuestionnaireSection.objects.filter(questionnaire=self)

    def section(self, index: int):
        try:
            return self.get_sections()[index]
        except KeyError:
            return False


class DoctorQuestionnaire(models.Model):
    """
    Many-to-many relationship between doctors and questionnaires for a medical institution
    """

    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)
    is_creator = models.BooleanField(default=False)

    # Relationship Fields
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='doctor_questionnaires', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution', related_name='mi_questionnaires', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    questionnaire = models.ForeignKey(Questionnaire, related_name='questionnaire_relations', on_delete=models.CASCADE)

    objects = DoctorQuestionnaireManager()

    class Meta:
        ordering = ('questionnaire__name', '-created')
        unique_together = ('doctor', 'medical_institution', 'questionnaire')

    def __str__(self):
        mi = ""
        if self.medical_institution:
            mi = f" at {self.medical_institution}"
        return f'{self.questionnaire.name} for {self.doctor}{mi}'


class QuestionnaireSection(models.Model):
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    order = models.PositiveSmallIntegerField(default=999)
    name = models.CharField(max_length=255, null=True, blank=True, default='Unnamed Section')
    description = models.CharField(max_length=1024, null=True, blank=True, default='')
    instructions = models.CharField(max_length=1024, null=True, blank=True, default='')

    # Relationship Fields
    questionnaire = models.ForeignKey(Questionnaire, related_name='questionnaire_sections', on_delete=models.CASCADE)

    objects = QuestionnaireSectionManager()

    class Meta:
        ordering = ('questionnaire__name', 'order', 'name')
        unique_together = ('questionnaire', 'order')

    def __str__(self):
        return f"[{self.order}] {self.name} - {self.questionnaire}"

    """ overrides """
    def save(self, *args, **kwargs):
        try:
            obj = super(QuestionnaireSection, self).save(*args, **kwargs)
            return obj
        except IntegrityError:
            affected_sections = self.__class__.objects.filter(
                questionnaire=self.questionnaire,
                order__gte=kwargs.get('order', 0)
            ).update(
                order=F('order') + 1
            )
            obj = super(QuestionnaireSection, self).save(*args, **kwargs)
        return obj
    """ /overrides """


class Question(models.Model):

    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    name = models.CharField(max_length=255, null=True, blank=True, default='Unnamed Question')
    slug = extension_fields.AutoSlugField(populate_from='name', unique=True)
    text = models.CharField(max_length=512)
    answer_type = models.CharField(max_length=60, choices=ANSWER_TYPES, default='free_text')
    answer_selection_type = models.CharField(max_length=60, choices=ANSWER_SELECTION_TYPES, default='single_answer')
    answer_data_type = models.CharField(max_length=60, choices=ANSWER_DATA_TYPES, default='text')

    objects = QuestionManager()
    tags = TaggableManager()


    class Meta:
        ordering = ('name', 'text', '-created')

    def excerpt(self, n):
        words = self.text.split(' ')
        return words[:n]

    def __str__(self):
        return f'[{self.name}] {self.excerpt(10)}...'


class SectionQuestion(models.Model):

    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    # Related Fields
    question = models.ForeignKey(Question, related_name='section_questions', on_delete=models.CASCADE)
    section = models.ForeignKey(QuestionnaireSection, related_name='question_sections', on_delete=models.CASCADE)

    objects = SectionQuestionManager()

    class Meta:
        ordering = ('order', '-created')
        unique_together = ('question', 'section')

    def __str__(self):
        return f'[{self.order}] {self.section}: {self.question}'

    """ overrides """
    def save(self, *args, **kwargs):
        try:
            obj = super(SectionQuestion, self).save(*args, **kwargs)
            return obj
        except IntegrityError:
            affected = self.__class__.objects.filter(
                section=self.section,
                order__gte=kwargs.get('order', 0)
            ).update(
                order=F('order') + 1
            )
            obj = super(SectionQuestion, self).save(*args, **kwargs)
        return obj
    """ /overrides """


class Choice(models.Model):
    pass


class ChoiceGroup(models.Model):
    pass
