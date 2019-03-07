from django.db import models, IntegrityError
from django.apps import apps


class PatientCheckupRecordManager(models.Manager):
    def create(self, *args, **kwargs):
        record = super(PatientCheckupRecordManager, self).create(*args, **kwargs)
        PatientCheckupRecordAccess = apps.get_model('doctor_profiles.PatientCheckupRecordAccess')
        try:
            PatientCheckupRecordAccess.objects.create(
                checkup=record,
                doctor=record.appointment.doctor
            )
        except IntegrityError:
            pass
        return record


class PatientCheckupRecordAccessManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientCheckupRecordAccessManager, self).create(*args, **kwargs)


class PatientSymptomManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientSymptomManager, self).create(*args, **kwargs)


class PatientFindingManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientFindingManager, self).create(*args, **kwargs)


class PatientDiagnosisManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientDiagnosisManager, self).create(*args, **kwargs)


class CheckupNoteManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(CheckupNoteManager, self).create(*args, **kwargs)


class LabTestManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(LabTestManager, self).create(*args, **kwargs)


class PatientLabTestRequestManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientLabTestRequestManager, self).create(*args, **kwargs)


class PatientPrescriptionManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientPrescriptionManager, self).create(*args, **kwargs)
