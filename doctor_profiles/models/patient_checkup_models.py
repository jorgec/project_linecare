from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_extensions.db.fields.json import JSONField
from django_extensions.db import fields as extension_fields

from doctor_profiles.models.managers.patient_checkup_manager import PatientCheckupRecordManager, \
    PatientCheckupRecordAccessManager, PatientSymptomManager, PatientFindingManager, PatientDiagnosisManager, \
    CheckupNoteManager, PatientLabTestRequestManager, LabTestManager


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

    def get_findings(self):
        return self.checkup_findings.filter(is_deleted=False)

    def get_dismissed_findings(self):
        return self.checkup_findings.filter(is_deleted=True)

    def get_diagnoses(self):
        return self.checkup_diagnoses.filter(is_deleted=False)

    def get_dismissed_diagnoses(self):
        return self.checkup_diagnoses.filter(is_deleted=True)

    def get_requested_tests(self):
        return self.checkup_tests.filter(is_approved=True)

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
        ordering = ('-checkup__appointment__schedule_day__date_obj',)
        unique_together = ('checkup', 'doctor')

    def __str__(self):
        return f'{self.checkup.appointment}'


class LabTest(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    name = models.CharField(max_length=120, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    aliases = ArrayField(models.CharField(max_length=1024), blank=True, null=True, default=list)

    description = models.TextField(max_length=4096, blank=True, null=True)
    purpose = models.TextField(max_length=2048, blank=True, null=True)
    indication = models.TextField(max_length=2048, blank=True, null=True)
    sample = models.TextField(max_length=2048, blank=True, null=True)
    preparation = models.TextField(max_length=2048, blank=True, null=True)
    usage = models.TextField(max_length=4096, blank=True, null=True)
    interpretation = models.TextField(max_length=4096, blank=True, null=True)
    notes = models.TextField(max_length=4096, blank=True, null=True)

    objects = LabTestManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class PatientLabTestRequest(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='tested_patients')
    checkup = models.ForeignKey('doctor_profiles.PatientCheckupRecord', on_delete=models.CASCADE,
                                related_name='checkup_tests')
    requested_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                 related_name='labtests_requested')

    objects = PatientLabTestRequestManager()

    class Meta:
        ordering = ('checkup',)
        unique_together = ('lab_test', 'checkup')

    def __str__(self):
        return f'{self.lab_test}: {self.checkup}'


class Symptom(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    name = models.CharField(max_length=120, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    synonym = models.ForeignKey("self", null=True, blank=True, related_name="synonymous_symptoms",
                                on_delete=models.SET_NULL)

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


class Finding(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    name = models.CharField(max_length=120, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    synonym = models.ForeignKey("self", null=True, blank=True, related_name="synonymous_findings",
                                on_delete=models.SET_NULL)

    description = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class PatientFinding(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    # Relationship Fields
    finding = models.ForeignKey(Finding, related_name="patient_findings", on_delete=models.CASCADE, null=True)
    checkup = models.ForeignKey(PatientCheckupRecord, related_name="checkup_findings",
                                on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                 related_name='findings_added')
    removed_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                   related_name='findings_deleted')

    objects = PatientFindingManager()

    class Meta:
        ordering = ('finding__name',)
        unique_together = ('finding', 'checkup')

    def __str__(self):
        return f'{self.finding}'


class Diagnosis(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    name = models.CharField(max_length=120, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    synonym = models.ForeignKey("self", null=True, blank=True, related_name="synonymous_diagnoses",
                                on_delete=models.SET_NULL)

    description = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "diagnoses"

    def __str__(self):
        return self.name


class PatientDiagnosis(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    # Relationship Fields
    diagnosis = models.ForeignKey(Diagnosis, related_name="patient_diagnoses", on_delete=models.CASCADE, null=True)
    checkup = models.ForeignKey(PatientCheckupRecord, related_name="checkup_diagnoses",
                                on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                 related_name='diagnoses_added')
    removed_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                   related_name='diagnoses_deleted')

    objects = PatientDiagnosisManager()

    class Meta:
        ordering = ('diagnosis__name',)
        unique_together = ('diagnosis', 'checkup')

    def __str__(self):
        return f'{self.diagnosis}'


class CheckupNote(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    note = models.TextField(max_length=1024)

    # Relationship Fields
    checkup = models.ForeignKey(PatientCheckupRecord, related_name="checkup_notes",
                                on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True,
                                 related_name='notes_added')

    objects = CheckupNoteManager()

    class Meta:
        ordering = ('checkup',)

    def __str__(self):
        return f'{self.checkup}: {self.note[:30]}'


class Prescription(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)