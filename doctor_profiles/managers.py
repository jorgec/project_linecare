import arrow
from django.db import models


class DoctorProfileQuerySet(models.QuerySet):
    pass


class DoctorProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            doctor = self.get(base_profile=kwargs['base_profile'])
            return doctor
        except self.model.DoesNotExist:
            return super(DoctorProfileManager, self).create(*args, **kwargs)


class DoctorDegreeQuerySet(models.QuerySet):
    pass


class DoctorDegreeManager(models.Manager):
    def validate(self, *args, **kwargs):
        current_year = arrow.utcnow().year
        min_year = current_year - 70

        if kwargs['year_attained'] < min_year or kwargs['year_attained'] > current_year:
            raise ValueError('Dubious year attained')

        return True
