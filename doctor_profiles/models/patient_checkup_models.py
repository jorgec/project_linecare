from django.db import models
from django_extensions.db.fields.json import JSONField
from django_extensions.db import fields as extension_fields


class Symptom(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    name = models.CharField(max_length=120, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    synonym = models.ForeignKey("self", null=True, blank=True, related_name="synonymous", on_delete=models.SET_NULL)

    description = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class PatientSymptom(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Relationship Fields
    symptom = models.ForeignKey(Symptom, related_name="patient_symptoms", on_delete=models.CASCADE)
    appointment = models.ForeignKey('doctor_profiles.PatientAppointment', related_name="appointment_symptoms",
                                    on_delete=models.CASCADE)

    class Meta:
        ordering = ('symptom__name',)
        unique_together = ('symptom', 'appointment')

    def __str__(self):
        return f'{self.symptom}: {self.appointment.patient}'
