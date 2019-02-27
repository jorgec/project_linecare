import os
from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models as models, IntegrityError
from django.db.models import Q, F
from django_extensions.db import fields as extension_fields
from taggit.managers import TaggableManager

from doctor_profiles.models.managers.questionnaire_managers import QuestionnaireManager, DoctorQuestionnaireManager, \
    QuestionnaireSectionManager, QuestionManager, SectionQuestionManager, ChoiceGroupManager, QuestionChoiceGroupManager
from doctor_profiles.constants import ANSWER_DATA_TYPES, ANSWER_SELECTION_TYPES, ANSWER_TYPES, \
    QUESTIONNAIRE_RESTRICTION_CHOICES, QUESTION_FLOW, FORK_OPERATORS, QUESTIONNAIRE_HOOKS


def question_photo_upload_path(instance, filename):
    return f'uploads/question_photos/{instance.pk}/{filename}'


def choice_photo_upload_path(instance, filename):
    return f'uploads/choice_photos/{instance.pk}/{filename}'


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
    # is_required = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, null=True, blank=True, default='')
    instructions = models.CharField(max_length=1024, null=True, blank=True, default='')
    restriction = models.CharField(max_length=60, choices=QUESTIONNAIRE_RESTRICTION_CHOICES, default='private')

    # Relationship Fields
    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_questionnaires',
                                   on_delete=models.SET_NULL, null=True, blank=True, default=None)

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
        return QuestionnaireSection.objects.filter(questionnaire=self, is_approved=True)

    def get_questions(self):
        sections = self.get_sections()
        questions = []
        for section in sections:
            questions = questions + section.get_questions()

        return questions

    def section(self, index: int = 0):
        index = int(index)
        try:
            return self.get_sections()[index]
        except KeyError:
            return None

    def get_doctors(self):
        return self.doctor_questionnaires.filter(is_approved=True)


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

    # Fields
    is_required = models.BooleanField(default=False)
    hook_location = models.CharField(max_length=30, choices=QUESTIONNAIRE_HOOKS, default='pre_appointment')

    # Relationship Fields
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='doctor_questionnaires',
                               on_delete=models.CASCADE)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution', related_name='mi_questionnaires',
                                            null=True, blank=True, default=None, on_delete=models.SET_NULL)
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
    parent = models.ForeignKey("self", null=True, blank=True, default=None, related_name="subsections",
                               on_delete=models.SET_NULL)

    objects = QuestionnaireSectionManager()

    class Meta:
        ordering = ('questionnaire__name', 'order', 'name')
        # unique_together = ('questionnaire', 'order')

    def __str__(self):
        return f"[{self.order}] {self.name} - {self.questionnaire}"

    def get_questions(self):
        rel = self.section_questions.filter(is_approved=True)
        questions = [r.question for r in rel]
        return questions

    def get_questions_rel(self):
        return self.section_questions.filter(is_approved=True)

    def question(self, index: int):
        questions = self.get_questions()
        try:
            return questions[index]
        except IndexError:
            return False

    def create_question(self, *args, **kwargs):
        """
        kwargs:
        - Question **kwargs
        - order: int

        Returns:
        bool, object/None, message
        """
        Question = apps.get_model('doctor_profiles.Question')
        SectionQuestion = apps.get_model('doctor_profiles.SectionQuestion')
        question = Question.objects.create(
            name=kwargs.get('name', None),
            text=kwargs.get('text'),
            answer_type=kwargs.get('answer_type', None),
            answer_selection_type=kwargs.get('answer_selection_type', None),
            answer_data_type=kwargs.get('answer_data_Type', None),
            created_by=self.questionnaire.created_by
        )
        try:
            sq = SectionQuestion.objects.create(
                order=kwargs.get('order', 0),
                section=self,
                question=question,
                fork_map=kwargs.get('fork_map', None),
                question_flow=kwargs.get('question_flow', 'linear'),
            )
            return True, sq, f"Question added to {self}"
        except SectionQuestion.DoesNotExist:
            return False, question, f"Question created but was not added to {self}"

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
    img = models.ImageField(upload_to=question_photo_upload_path, max_length=1024, null=True, blank=True, default=None)
    answer_type = models.CharField(max_length=60, choices=ANSWER_TYPES, default='free_text')
    answer_selection_type = models.CharField(max_length=60, choices=ANSWER_SELECTION_TYPES, default='single_answer')
    answer_data_type = models.CharField(max_length=60, choices=ANSWER_DATA_TYPES, default='text')
    restriction = models.CharField(max_length=60, choices=QUESTIONNAIRE_RESTRICTION_CHOICES, default='private')

    # Relationship Fields
    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_questions',
                                   on_delete=models.SET_NULL, null=True, blank=True, default=None)

    objects = QuestionManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('name', 'text', '-created')

    def excerpt(self, n):
        words = self.text.split(' ')
        return " ".join(words[:n])

    def __str__(self):
        return f'[{self.name}] {self.excerpt(10)}...'

    def create_choice_group(self, **kwargs):
        ChoiceGroup = apps.get_model('doctor_profiles.ChoiceGroup')
        QuestionChoiceGroup = apps.get_model('doctor_profiles.QuestionChoiceGroup')
        choice_group = ChoiceGroup.objects.create(**kwargs)
        return self.add_choice_group(choice_group=choice_group).choice_group

    def add_choice_group(self, choice_group):
        QuestionChoiceGroup = apps.get_model('doctor_profiles.QuestionChoiceGroup')

        try:
            return QuestionChoiceGroup.objects.create(
                question=self,
                choice_group=choice_group
            )
        except IntegrityError:
            return False

    def get_choice_group(self):
        QuestionChoiceGroup = apps.get_model('doctor_profiles.QuestionChoiceGroup')
        try:
            question_choice_group = QuestionChoiceGroup.objects.get(question=self)
            return question_choice_group.choice_group
        except QuestionChoiceGroup.DoesNotExist:
            return False

    def get_choices(self):
        choice_group = self.get_choice_group()
        if choice_group:
            return choice_group.get_choices()
        return False

    def get_choice(self, index: int = 0):
        choice_group = self.get_choice_group()
        if choice_group:
            return choice_group.get_choice(index).choice
        return False


class SectionQuestion(models.Model):
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    order = models.PositiveSmallIntegerField(default=0)
    fork_map = JSONField(default=dict, null=True, blank=True)
    question_flow = models.CharField(max_length=30, choices=QUESTION_FLOW, default='linear')

    # Related Fields
    question = models.ForeignKey(Question, related_name='question_sections', on_delete=models.CASCADE)
    section = models.ForeignKey(QuestionnaireSection, related_name='section_questions', on_delete=models.CASCADE)

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
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    name = models.CharField(max_length=120, null=True, blank=True, default='Unnamed Choice')
    text = models.CharField(max_length=512, default="")
    img = models.ImageField(upload_to=choice_photo_upload_path, max_length=1024, null=True, blank=True, default=None)
    value = models.CharField(max_length=255)

    # Relationship Fields
    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_choices',
                                   on_delete=models.SET_NULL, null=True, blank=True, default=None)

    tags = TaggableManager()

    class Meta:
        ordering = ('name', '-created')

    def excerpt(self, n):
        words = self.text.split(' ')
        return " ".join(words[:n])

    def __str__(self):
        if self.text:
            return self.excerpt(10)
        return self.name


class ChoiceGroup(models.Model):
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    name = models.CharField(max_length=120, null=True, blank=True, default='Unnamed Choice Group')
    restriction = models.CharField(max_length=60, choices=QUESTIONNAIRE_RESTRICTION_CHOICES, default='private')

    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_choicegroups',
                                   on_delete=models.SET_NULL, null=True, blank=True, default=None)

    objects = ChoiceGroupManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('name', '-created')

    def __str__(self):
        return self.name

    def create_choice(self, **kwargs):
        Choice = apps.get_model('doctor_profiles.Choice')
        choice = Choice.objects.create(
            name=kwargs.get('name', None),
            text=kwargs.get('text'),
            value=kwargs.get('value')
        )
        return self.add_choice(choice=choice, order=kwargs.get('order', 0)).choice

    def add_choice(self, choice, order=0):
        ChoiceGroupItem = apps.get_model('doctor_profiles.ChoiceGroupItem')
        return ChoiceGroupItem.objects.create(
            choice_group=self,
            choice=choice,
            order=order
        )

    def get_choices_rel(self):
        return self.choices.all()

    def get_choices(self):
        rel = self.get_choices_rel().order_by('order')
        return rel

    def get_choice(self, index=0):
        choices = self.get_choices()
        try:
            return choices[index]
        except IndexError:
            return False


class ChoiceGroupItem(models.Model):
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Fields
    order = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    # Relationship Fields
    choice = models.ForeignKey(Choice, related_name='choice_groups', on_delete=models.CASCADE)
    choice_group = models.ForeignKey(ChoiceGroup, related_name='choices', on_delete=models.CASCADE)

    class Meta:
        ordering = ('choice_group', 'order', '-created')
        # unique_together = ('choice_group', 'order')

    def __str__(self):
        return f"[{self.order}] {self.choice_group} choice: {self.choice}"


class QuestionChoiceGroup(models.Model):
    # Basic Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Admin Fields
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    question = models.ForeignKey(Question, related_name='question_choice_group', on_delete=models.CASCADE)
    choice_group = models.ForeignKey(ChoiceGroup, related_name='choice_group_questions', on_delete=models.CASCADE)

    objects = QuestionChoiceGroupManager()

    class Meta:
        ordering = ('question', '-created')
        unique_together = ('question', 'choice_group')

    def __str__(self):
        return f'{self.question} choice group: {self.choice_group}'
