from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models as models, IntegrityError
from django.db.models import Q
from django_extensions.db import fields as extension_fields
from taggit.managers import TaggableManager

from doctor_profiles.models.managers.questionnaire_managers import QuestionnaireManager, DoctorQuestionnaireManager
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
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', unique=True)
    is_required = models.BooleanField(default=False)
    description = models.CharField(max_length=512, null=True, blank=True, default=None)
    restriction = models.CharField(max_length=60, choices=QUESTIONNAIRE_RESTRICTION_CHOICES, default='private')

    # Relationship Fields
    created_by = models.ForeignKey('profiles.BaseProfile', related_name='created_questionnaires', on_delete=models.CASCADE)

    tags = TaggableManager()

    objects = QuestionnaireManager()

    class Meta:
        ordering = ('name', '-created')

    def __str__(self):
        return f"{self.name}"


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

    objects = DoctorQuestionnaireManager

    class Meta:
        ordering = ('questionnaire__name', '-created')
        unique_together = ('doctor', 'medical_institution', 'questionnaire')

    def __str__(self):
        mi = ""
        if self.medical_institution:
            mi = f" at {self.medical_institution}"
        return f'{self.questionnaire.name} for {self.doctor}{mi}'
