import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from doctor_profiles.managers import DoctorDegreeManager


class MedicalDegree(models.Model):
    """
    List of medical degrees
    """
    # Fields
    name = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    abbreviation = models.CharField(max_length=30, unique=True)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class DoctorDegree(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`MedicalDegree`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    year_attained = models.PositiveSmallIntegerField()
    school = models.CharField(max_length=120)
    metadata = JSONField(default=dict, null=True, blank=True)
    license_number = models.CharField(max_length=60)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    objects = DoctorDegreeManager()

    # Relationship Fields
    doctor = models.ForeignKey(
        'doctor_profiles.DoctorProfile',
        on_delete=models.CASCADE, related_name="doctor_degrees",
    )
    degree = models.ForeignKey(
        'doctor_profiles.MedicalDegree',
        on_delete=models.CASCADE, related_name="degree_doctors"
    )

    class Meta:
        ordering = ('degree',)
        unique_together = ('doctor', 'degree')

    def __str__(self):
        return f"{self.doctor}, {self.degree.abbreviation}"

    def save(self, *args, **kwargs):
        current_year = arrow.utcnow().year
        min_year = current_year - 70

        if self.year_attained < min_year or self.year_attained > current_year:
            raise ValueError('Dubious year attained')

        return super(DoctorDegree, self).save(*args, **kwargs)


"""
Signals
"""


@receiver(post_save, sender=DoctorDegree)
def doctor_degree_on_save(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['medical_degree'] = DoctorDegree.objects.filter(doctor=instance.doctor,
                                                                 degree__is_approved=True).count()
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()


@receiver(post_delete, sender=DoctorDegree)
def doctor_degree_on_delete(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['medical_degree'] = DoctorDegree.objects.filter(doctor=instance.doctor,
                                                                 degree__is_approved=True).count()
        if progress['medical_degree'] == 0:
            progress['medical_degree'] = None
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()
