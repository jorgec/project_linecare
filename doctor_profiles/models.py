from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Specialization(models.Model):
    """
    Denotes entry into a specialized field of medicine (i.e. Pediatrics, Internal Medicine, etc.)
    Subspecializations must have a `parent` specialization model:`doctor_profiles`.`Specialization`
    """

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)
    abbreviation = models.CharField(max_length=30)

    # Relationship Fields
    parent = models.ForeignKey(
        'doctor_profiles.Specialization',
        on_delete=models.CASCADE, related_name="subspecs"
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name}"


class InsuranceProvider(models.Model):
    """
    List of Insurance Providers
    """

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

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

    # Relationship Fields
    base_profile = models.OneToOneField('profiles.BaseProfile', related_name='doctor_profile', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        degrees = ", ".join([a.abbreviation for a in self.get_degrees()])
        fellowships = ", ".join([a.abbreviation for a in self.get_fellowships()])
        diplomates = ", ".join([a.abbreviation for a in self.get_diplomates()])

        title = f"Dr. {self.base_profile.get_name()} {degrees} {fellowships} {diplomates}"

        return title

    def get_degrees(self):
        return self.doctor_degrees.all()

    def get_fellowships(self):
        return self.doctor_associations.filter(level='Fellow')

    def get_diplomates(self):
        return self.doctor_associations.filter(level='Diplomate')


class MedicalDegree(models.Model):
    """
    List of medical degrees
    """
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    abbreviation = models.CharField(max_length=30)
    metadata = JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name}"


class MedicalAssociation(models.Model):
    """
    Medical Associations that confer specializations
    """
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    abbreviation = models.CharField(max_length=30)
    metadata = JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

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
    place_of_residency = models.CharField(max_length=120)

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

    def __str__(self):
        return f"{self.doctor}, {self.specialization.abbreviation}"


class DoctorInsurance(models.Model):
    """
    Associative table for the m:n relationship between model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`InsuranceProvider`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    expiry = models.ForeignKey('datesdim.DateDim', on_delete=models.CASCADE, related_name='insurance_expirations')
    identifier = models.CharField(max_length=120)

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

    def __str__(self):
        return f"{self.insurance} ({self.doctor})"


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

    # Relationship Fields
    doctor = models.ForeignKey(
        'doctor_profiles.DoctorProfile',
        on_delete=models.CASCADE, related_name="doctor_degrees"
    )
    degree = models.ForeignKey(
        'doctor_profiles.MedicalDegree',
        on_delete=models.CASCADE, related_name="degree_doctors"
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.doctor}, {self.degree.abbreviation}"


class DoctorAssociation(models.Model):
    """
    Associative table for the m:n relationship between :model:`doctor_profiles`.`DoctorProfile` and model:`doctor_profiles`.`MedicalAssociation`
    """
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    level = models.CharField(max_length=30, choices=(('Diplomate', 'Diplomate'), ('Fellow', 'Fellow')))
    year_attained = models.PositiveSmallIntegerField()

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

    def __str__(self):
        return f"{self.doctor}, {self.association.abbreviation}"
