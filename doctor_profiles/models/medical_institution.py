from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django_extensions.db import fields as extension_fields


class MedicalInstitution(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    is_approved = models.BooleanField(default=True)
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship Fields
    type = models.ForeignKey(
        'doctor_profiles.MedicalInstitutionType',
        on_delete=models.CASCADE, related_name="type_institutions"
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="medical_institutions_added"
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'

    def get_addresses(self):
        return self.medical_institution_locations.all()

    def get_approved_addresses(self):
        return self.medical_institution_locations.filter(is_approved=True)

    def get_phones(self):
        return self.medical_institution_phones.all()

    def get_approved_phones(self):
        return self.medical_institution_phones.filter(is_approved=True)

    def phones(self):
        approved = self.get_approved_phones()

        if approved.count() > 0:
            phone_numbers = list(approved)
        else:
            phone_numbers = list(self.get_phones())

        # selection sort
        for i in range(len(phone_numbers) - 1, 0, -1):
            pos_max = 0
            for location in range(1, i + 1):
                if phone_numbers[location].total_votes() > phone_numbers[pos_max].total_votes():
                    pos_max = location
            temp = phone_numbers[i]
            phone_numbers[i] = phone_numbers[pos_max]
            phone_numbers[pos_max] = temp

        return phone_numbers
    
    def addresses(self):
        approved = self.get_approved_addresses()

        if approved.count() > 0:
            address_list = list(approved)
        else:
            address_list = list(self.get_addresses())

        # selection sort
        for i in range(len(address_list) - 1, 0, -1):
            pos_max = 0
            for location in range(1, i + 1):
                if address_list[location].total_votes() > address_list[pos_max].total_votes():
                    pos_max = location
            temp = address_list[i]
            address_list[i] = address_list[pos_max]
            address_list[pos_max] = temp


class MedicalInstitutionType(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'
