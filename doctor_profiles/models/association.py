from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields


class MedicalAssociation(models.Model):
    """
    Medical Associations that confer specializations
    """
    # Fields
    name = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
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


class DoctorAssociation(models.Model):
    """
    Associative table for the m:n relationship between :model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`MedicalAssociation`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    level = models.CharField(max_length=30, choices=(('Diplomate', 'Diplomate'), ('Fellow', 'Fellow')))
    year_attained = models.PositiveSmallIntegerField()

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    doctor = models.ForeignKey(
        'doctor_profiles.DoctorProfile',
        on_delete=models.CASCADE, related_name="doctor_associations"
    )
    association = models.ForeignKey(
        'doctor_profiles.MedicalAssociation',
        on_delete=models.CASCADE, related_name="association_doctors"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('doctor', 'association', 'level')

    def __str__(self):
        return self.get_abbreviation()

    def get_abbreviation(self):
        return f"{self.level[0]}{self.association.abbreviation}"


"""
Signals
"""


@receiver(post_save, sender=DoctorAssociation)
def doctor_association_on_save(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['association'] = DoctorAssociation.objects.filter(doctor=instance.doctor,
                                                                   association__is_approved=True).count()
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()


@receiver(post_delete, sender=DoctorAssociation)
def doctor_association_on_delete(sender, instance, created=False, **kwargs):
    progress = instance.doctor.user.user_settings.get('doctor_progress', None)
    if progress:
        progress['association'] = DoctorAssociation.objects.filter(doctor=instance.doctor,
                                                                   association__is_approved=True).count()
        if progress['association'] == 0:
            progress['association'] = None
        instance.doctor.user.user_settings['doctor_progress'] = progress
        instance.doctor.user.save()
