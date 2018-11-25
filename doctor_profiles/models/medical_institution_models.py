import operator
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models as models
from django_extensions.db import fields as extension_fields

from doctor_profiles.models.managers.medical_institution_manager import MedicalInstitutionManager


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

    objects = MedicalInstitutionManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.type.name})'

    def get_addresses(self):
        return self.medical_institution_locations.all()

    def get_approved_addresses(self):
        return self.medical_institution_locations.filter(is_approved=True)

    def get_phones(self):
        return self.medical_institution_phones.all()

    def get_approved_phones(self):
        return self.medical_institution_phones.filter(is_approved=True)

    def phones(self, with_votes=True):
        approved = self.get_approved_phones()

        if approved.count() > 0:
            phone_list = approved
        else:
            phone_list = self.get_phones()

        if phone_list.count() > 0:
            phone_votes = {a: a.total_votes() for a in phone_list}
            sorted_phones = sorted(phone_votes.items(), key=operator.itemgetter(1), reverse=True)

            if with_votes:
                return [{"phone": a[0], "votes": a[1]} for a in sorted_phones]
            else:
                return [phone[0] for phone in sorted_phones]

        return None

    def addresses(self, with_votes=True):
        approved = self.get_approved_addresses()

        if approved.count() > 0:
            address_list = approved
        else:
            address_list = self.get_addresses()

        if address_list.count() > 0:
            address_votes = {a: a.total_votes() for a in address_list}
            sorted_addresses = sorted(address_votes.items(), key=operator.itemgetter(1), reverse=True)

            if with_votes:
                return [{"address": a[0], "votes": a[1]} for a in sorted_addresses]
            else:
                return [address[0] for address in sorted_addresses]

        return None

    def address(self):
        addresses = self.addresses()
        if addresses:
            if len(addresses) > 0:
                return addresses[0]
        return None

    def get_coordinates(self):
        return self.medical_institution_coordinates.all()

    def get_approved_coordinates(self):
        return self.medical_institution_coordinates.filter(is_approved=True)

    def all_coordinates(self, with_votes=True):
        approved = self.get_approved_coordinates()

        if approved.count() > 0:
            coordinate_list = approved
        else:
            coordinate_list = self.get_coordinates()

        if coordinate_list.count() > 0:
            coordinate_votes = {a: a.total_votes() for a in coordinate_list}
            sorted_coordinates = sorted(coordinate_votes.items(), key=operator.itemgetter(1), reverse=True)

            if with_votes:
                return [{"coordinates": a[0], "votes": a[1]} for a in sorted_coordinates]
            else:
                return [coordinate[0] for coordinate in sorted_coordinates]

        return None

    def coordinates(self):
        coords = self.all_coordinates()
        print(coords)
        if coords:
            if len(coords) > 0:
                print(coords[0])
                return coords[0]
        return None


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
