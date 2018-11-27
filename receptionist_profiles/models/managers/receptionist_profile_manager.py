from django.db import models
from django.apps import apps


class ReceptionistConnectionManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            connection = self.get(
                receptionist=kwargs['receptionist'],
                doctor=kwargs['doctor'],
                medical_institution=kwargs['medical_institution']
            )
            return connection
        except self.model.DoesNotExist:
            return super(ReceptionistConnectionManager, self).create(*args, **kwargs)


class ReceptionistProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            receptionist = self.get(user=kwargs['user'])
            return receptionist
        except self.model.DoesNotExist:
            return super(ReceptionistProfileManager, self).create(*args, **kwargs)

    def create_by_doctor(self, *args, **kwargs):
        """
        Required kwargs:
        - doctor
        - medical_institution
        """
        if not 'doctor' or not 'medical_institution' in kwargs:
            return self.create(*args, **kwargs)

        # receptionist = super(ReceptionistProfileManager, self).create(*args, **kwargs)
        receptionist = self.create(
            user=kwargs['user']
        )
        ReceptionistConnection = apps.get_model('receptionist_profiles.ReceptionistConnection')

        connection = ReceptionistConnection.objects.create(
            receptionist=receptionist,
            doctor=kwargs['doctor'],
            medical_institution=kwargs['medical_institution']
        )

        return receptionist

