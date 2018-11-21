import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields


class Specialization(models.Model):
    """
    Denotes entry into a specialized field of medicine (i.e. Pediatrics, Internal Medicine, etc.)
    Subspecializations must have a `parent` specialization model:`doctor_profiles`.`Specialization`
    """

    # Fields
    name = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    abbreviation = models.CharField(max_length=30, unique=True)
    practitioner_title = models.CharField(max_length=100, null=True, blank=True)
    practitioner_title_plural = models.CharField(max_length=105, null=True, blank=True)


    practitioner_title = models.CharField(max_length=60, blank=True, null=True)
    practitioner_title_plural = models.CharField(max_length=64, blank=True, null=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    parent = models.ForeignKey(
        'doctor_profiles.Specialization',
        on_delete=models.CASCADE, related_name="subspecs",
        null=True, blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class DoctorSpecialization(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`Specialization`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    year_attained = models.PositiveSmallIntegerField(blank=True, null=True)
    place_of_residency = models.CharField(max_length=120, blank=True, null=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    doctor = models.ForeignKey(
        'doctor_profiles.DoctorProfile',
        on_delete=models.CASCADE, related_name="doctor_specializations"
    )
    specialization = models.ForeignKey(
        'doctor_profiles.Specialization',
        on_delete=models.CASCADE, related_name="specialization_doctors"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('doctor', 'specialization')

    def __str__(self):
        return f"{self.doctor}, {self.specialization.abbreviation}"

    def save(self, *args, **kwargs):
        if self.year_attained:
            current_year = arrow.utcnow().year
            min_year = current_year - 70

            if self.year_attained < min_year or self.year_attained > current_year:
                raise ValueError('Dubious year attained')

        return super(DoctorSpecialization, self).save(*args, **kwargs)



"""
Signals
"""


@receiver(post_save, sender=DoctorSpecialization)
def doctor_specialization_on_save(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['specialization'] = DoctorSpecialization.objects.filter(doctor=instance.doctor,
                                                                         specialization__is_approved=True).count()
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()


@receiver(post_delete, sender=DoctorSpecialization)
def doctor_specialization_on_delete(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['specialization'] = DoctorSpecialization.objects.filter(doctor=instance.doctor,
                                                                         specialization__is_approved=True).count()
        if progress['specialization'] == 0:
            progress['specialization'] = None
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()

