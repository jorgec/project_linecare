from django.db import models
from django.contrib.postgres.fields import JSONField


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
