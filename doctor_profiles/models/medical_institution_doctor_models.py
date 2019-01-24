from django.db import models
from django.contrib.postgres.fields import JSONField

from doctor_profiles.constants import APPOINTMENT_TYPES


class MedicalInstitutionDoctor(models.Model):
    """
    Many to many relation between doctors and medical institutions
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    is_approved = models.BooleanField(default=True)
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship fields
    doctor = models.ForeignKey("doctor_profiles.DoctorProfile",
                               on_delete=models.CASCADE,
                               related_name="medical_institutions_joined")
    medical_institution = models.ForeignKey("doctor_profiles.MedicalInstitution",
                                            on_delete=models.CASCADE,
                                            related_name="member_doctors")

    class Meta:
        ordering = ('-created',)
        unique_together = ('doctor', 'medical_institution')

    def __str__(self):
        return f'{self.medical_institution}: {self.doctor}'

    def get_schedule_options(self):
        try:
            return {
                'fees': self.metadata['fees'],
                'durations': self.metadata['durations']
            }
        except KeyError:
            types = APPOINTMENT_TYPES
            self.metadata['durations'] = {}
            self.metadata['fees'] = {}
            for t in types:
                self.metadata['durations'][f'{t[0]}_duration'] = 15
                self.metadata['durations'][f'{t[0]}_gap'] = 1
                self.metadata['fees'][t[0]] = 0
            self.save()
            return {
                'fees': self.metadata['fees'],
                'durations': self.metadata['durations']
            }
