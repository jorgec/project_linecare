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