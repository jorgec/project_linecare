from django.db import models
from django_extensions.db.fields.json import JSONField
from django_extensions.db import fields as extension_fields


class Symptom(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    name = models.CharField(max_length=120)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)


class PatientSymptom(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)