import arrow
from django.db import models


class DoctorDegreeQuerySet(models.QuerySet):
    pass


class DoctorDegreeManager(models.Manager):
    def validate(self, *args, **kwargs):
        current_year = arrow.utcnow().year
        min_year = current_year - 70

        if kwargs['year_attained'] < min_year or kwargs['year_attained'] > current_year:
            raise ValueError('Dubious year attained')

        return True
