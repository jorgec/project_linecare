from django.db import models


class ReceptionistProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            receptionist = self.get(user=kwargs['user'])
            return receptionist
        except self.model.DoesNotExist:
            return super(ReceptionistProfileManager, self).create(*args, **kwargs)
