from django.db import models, IntegrityError


class DoctorProfileQuerySet(models.QuerySet):
    pass


class DoctorProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        user = kwargs['user']

        if user.receptionist_profile():
            raise IntegrityError("A receptionist can't have a doctor profile")
        try:
            doctor = self.get(user=kwargs['user'])
            return doctor
        except self.model.DoesNotExist:
            metadata = {
                "doctor_progress": {},
                "options": {},
                "tutorial": {
                    "basic": False,
                    "medical_institution": False,
                    "queue": False,
                    "calendar": False
                }
            }

            kwargs['metadata'] = metadata

            return super(DoctorProfileManager, self).create(*args, **kwargs)


