import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django.db.models import Model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_extensions.db import fields as extension_fields

from datesdim.models import DateDim
from doctor_profiles.managers import DoctorDegreeManager


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


class DoctorProfile(models.Model):
    """
    The core Doctor profile
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
    user = models.OneToOneField('accounts.Account', related_name='doctorprofile', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        degrees = ", ".join([a.degree.abbreviation for a in self.get_degrees()])
        fellowships = ", ".join([a.get_abbreviation() for a in self.get_fellowships()])
        diplomates = ", ".join([a.get_abbreviation() for a in self.get_diplomates()])

        title = f"Dr. {self.user.base_profile().get_name()} {degrees} {fellowships} {diplomates}"

        return title

    def get_degrees(self):
        return self.doctor_degrees.filter(degree__is_approved=True)

    def get_insurance_providers(self):
        return self.doctor_insurance.filter(is_approved=True)

    def get_specializations(self):
        return self.doctor_specializations.filter(specialization__parent__isnull=True, specialization__is_approved=True)

    def get_associations(self):
        return self.doctor_associations.filter(association__is_approved=True)

    def get_fellowships(self):
        return self.doctor_associations.filter(level='Fellow', association__is_approved=True)

    def get_diplomates(self):
        return self.doctor_associations.filter(level='Diplomate', association__is_approved=True)

    def settings_progress(self):
        progress = self.user.user_settings.get('doctor_progress', None)
        retval = {
            'progress': 0.0,
            'progress_pct': '0%',
            'progress_int': 0,
            'items': {}
        }
        if progress:
            max = len(progress)
            total = 0
            for key, value in progress.items():
                if value is not None:
                    total = total + 1
            retval['progress'] = total / max
            retval['progress_pct'] = f'{round((total/max)*100)}%'
            retval['progress_int'] = round((total / max) * 100)
            retval['items'] = progress
        return retval


class DoctorSpecialization(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`Specialization`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    year_attained = models.PositiveSmallIntegerField(blank=True, null=True)
    place_of_residency = models.CharField(max_length=120)

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
        current_year = arrow.utcnow().year
        min_year = current_year - 70

        if self.year_attained < min_year or self.year_attained > current_year:
            raise ValueError('Dubious year attained')

        return super(DoctorSpecialization, self).save(*args, **kwargs)


class DoctorInsurance(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`InsuranceProvider`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    identifier = models.CharField(max_length=120)

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
        today = DateDim.objects.today()

        return super(DoctorInsurance, self).save(*args, **kwargs)


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
