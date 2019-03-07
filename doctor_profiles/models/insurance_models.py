from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields


class InsuranceProvider(models.Model):
    """
    List of Insurance Providers
    """

    # Fields
    name = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class DoctorInsurance(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`InsuranceProvider`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    identifier = models.CharField(max_length=120, blank=True, null=True, default=None)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    doctor = models.ForeignKey(
        'doctor_profiles.DoctorProfile',
        on_delete=models.CASCADE, related_name="doctor_insurance"
    )
    insurance = models.ForeignKey(
        'doctor_profiles.InsuranceProvider',
        on_delete=models.CASCADE, related_name="insurance_doctors"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('doctor', 'insurance')

    def __str__(self):
        return f"{self.insurance} ({self.doctor})"

    def save(self, *args, **kwargs):
        return super(DoctorInsurance, self).save(*args, **kwargs)


@receiver(post_save, sender=DoctorInsurance)
def doctor_insurance_on_save(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['insurance'] = DoctorInsurance.objects.filter(doctor=instance.doctor,
                                                               insurance__is_approved=True).count()
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()


@receiver(post_delete, sender=DoctorInsurance)
def doctor_insurance_on_delete(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['insurance'] = DoctorInsurance.objects.filter(doctor=instance.doctor,
                                                               insurance__is_approved=True).count()
        if progress['insurance'] == 0:
            progress['insurance'] = None
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()
