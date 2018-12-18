from django.db import models
from django_extensions.db.fields.json import JSONField
from django_extensions.db import fields as extension_fields

from doctor_profiles.models.managers.patient_checkup_manager import PatientCheckupRecordManager, \
    PatientCheckupRecordAccessManager, PatientSymptomManager


class PatientCheckupRecord(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    # Relationship Fields
    appointment = models.OneToOneField('doctor_profiles.PatientAppointment', related_name="appointment_checkup",
                                       on_delete=models.CASCADE)

    objects = PatientCheckupRecordManager()

    class Meta:
        ordering = ('appointment__patient',)

    def __str__(self):
        return f'{self.appointment.patient}'

    def get_symptoms(self):
        return self.checkup_symptoms.filter(is_deleted=False)

    def get_dismissed_symptoms(self):
        return self.checkup_symptoms.filter(is_deleted=True)

    def doctor_has_access(self, doctor):
        allowed = self.checkup_access.filter(is_approved=True, doctor=doctor)
        if allowed.count() > 0:
            return True
        return False


class PatientCheckupRecordAccess(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    is_approved = models.BooleanField(default=True)
    checkup = models.ForeignKey(PatientCheckupRecord, on_delete=models.CASCADE, related_name='checkup_access')
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='patient_records',
                               on_delete=models.CASCADE)

    objects = PatientCheckupRecordAccessManager()

    class Meta:
        ordering = ('-checkup__appointment__schedule_day',)
        unique_together = ('checkup', 'doctor')

    def __str__(self):
        return f'{self.checkup.appointment}'


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

    is_deleted = models.BooleanField(default=False)

    # Relationship Fields
    symptom = models.ForeignKey(Symptom, related_name="patient_symptoms", on_delete=models.CASCADE, null=True)
    checkup = models.ForeignKey(PatientCheckupRecord, related_name="checkup_symptoms",
                                on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                 related_name='symptoms_added')
    removed_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                   related_name='symptoms_deleted')

    objects = PatientSymptomManager()

    class Meta:
        ordering = ('symptom__name',)
        unique_together = ('symptom', 'checkup')

    def __str__(self):
        return f'{self.symptom}: {self.checkup.appointment.patient}'
