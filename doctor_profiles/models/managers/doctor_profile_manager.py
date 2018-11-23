from django.db import models


class DoctorProfileQuerySet(models.QuerySet):
    pass


class DoctorProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            doctor = self.get(user=kwargs['user'])
            return doctor
        except self.model.DoesNotExist:
            return super(DoctorProfileManager, self).create(*args, **kwargs)


