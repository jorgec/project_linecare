from django.contrib.postgres.fields import JSONField
from django.db import models as models

from receptionist_profiles.models.managers.receptionist_profile_manager import ReceptionistConnectionManager, \
    ReceptionistProfileManager


class ReceptionistProfile(models.Model):
    """
    The core Receptionist profile
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    user = models.OneToOneField('accounts.Account', related_name='receptionistprofile', on_delete=models.CASCADE,
                                null=True)

    objects = ReceptionistProfileManager()

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.user}'


class ReceptionistConnection(models.Model):
    """
    Connection between doctor, receptionist, and medical institution
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    receptionist = models.ForeignKey(ReceptionistProfile, related_name="receptionist_connections",
                                     on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', related_name='doctor_connections',
                               on_delete=models.CASCADE)
    medical_institution = models.ForeignKey('doctor_profiles.MedicalInstitution',
                                            related_name='institution_connections', on_delete=models.CASCADE)

    objects = ReceptionistConnectionManager()

    class Meta:
        ordering = ('medical_institution', 'doctor', 'receptionist')
        unique_together = ('medical_institution', 'doctor', 'receptionist')
