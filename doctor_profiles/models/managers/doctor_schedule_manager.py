from django.db import models as models


class DoctorScheduleManager(models.Manager):
    def create(self, *args, **kwargs):
        pass