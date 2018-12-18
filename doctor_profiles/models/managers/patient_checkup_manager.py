from django.db import models


class PatientCheckupRecordManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(PatientCheckupRecordManager, self).create(*args, **kwargs)


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
