from django.db import models
from django.urls import reverse
from django_extensions.db import fields as extension_fields

class MedicalSubject(models.Model):
    # Fields
    name = models.CharField(max_length=32)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    create = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    # Fields
    name = models.CharField(max_length=64)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

class Insurance(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)


class DoctorProfile(models.Model):
    # Fields
    license_number = models.CharField(max_length=12, blank=True)
    year_started = models.IntegerField(null=True)

    # Relationship Fields
    profile = models.ForeignKey('profiles.BaseProfile', on_delete=models.CASCADE, related_name='profile_doctor')
    medical_subject = models.ForeignKey(MedicalSubject, related_name='medical_subject_doctor', on_delete=models.SET_NULL, blank=True, null=True )
    insurance = models.ForeignKey(Insurance, on_delete=models.SET_NULL, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created',)
        unique_together = ('license_number', 'profile')

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('doctors_doctorprofile_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('doctors_doctorprofile_update', args=(self.pk,))

    def get_doctor_specialties(self):
        return self.doctor_specialty.all()

class DoctorSpecialty(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)

    # Relationship Fields
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='doctor_specialty')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
