from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from phonenumber_field.modelfields import PhoneNumberField


class MedicalInstitutionPhone(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    phone_number = PhoneNumberField()
    is_approved = models.BooleanField(default=False)
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship Fields
    medical_institution = models.ForeignKey(
        'doctor_profiles.MedicalInstitution',
        on_delete=models.CASCADE, related_name="medical_institution_phones"
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.phone_number}"

    def get_ups(self):
        return self.medical_institution_phone_votes.filter(type='Up').count()

    def get_downs(self):
        return self.medical_institution_phone_votes.filter(type='Down').count()

    def total_votes(self):
        return self.get_ups() - self.get_downs()

    def user_has_voted(self, user):
        return self.medical_institution_phone_votes.filter(voter=user).count() > 0


class MedicalInstitutionPhoneVote(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    type = models.CharField(max_length=4, choices=(('Up', 'Up'), ('Down', 'Down')))
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship Fields
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="user_votes_medical_institution_phone"
    )
    medical_institution_phone = models.ForeignKey(
        'doctor_profiles.MedicalInstitutionPhone',
        on_delete=models.CASCADE, related_name="medical_institution_phone_votes"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('voter', 'medical_institution_phone')

    def __str__(self):
        return u'%s' % self.pk
