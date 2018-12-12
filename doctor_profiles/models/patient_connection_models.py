from django.db import models
from django.contrib.postgres.fields import JSONField


class PatientConnection(models.Model):
    """
    Patients of doctor
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
    doctor = models.ForeignKey('doctor_profiles.DoctorProfile', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='doctor_patients')
    patient = models.ForeignKey('profiles.BaseProfile', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='patient_doctors')


    class Meta:
        ordering = ('patient', 'doctor')
        unique_together = ('patient', 'doctor')


    def __str__(self):
        return f'{self.patient} - {self.doctor}'


