import operator
import requests
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models as models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver


class MedicalInstitutionLocation(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    address = models.TextField(max_length=255)

    # Relationship Fields
    country = models.ForeignKey('locations.Country', related_name="medical_institutions_in_country",
                                on_delete=models.CASCADE, default=169)
    region = models.ForeignKey('locations.Region', related_name="medical_institutions_in_region",
                               on_delete=models.CASCADE)
    province = models.ForeignKey('locations.Province', related_name="medical_institutions_in_province",
                                 on_delete=models.CASCADE)
    city = models.ForeignKey('locations.City', related_name="medical_institutions_in_city", on_delete=models.CASCADE)

    zip_code = models.PositiveSmallIntegerField(null=True, blank=True, default=None)

    suggested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="medical_institution_location_suggestions"
    )
    medical_institution = models.ForeignKey(
        'doctor_profiles.MedicalInstitution',
        on_delete=models.CASCADE, related_name="medical_institution_locations"
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.zip_code}, {self.province}, {self.region}, {self.country}"

    def get_address_with_votes(self):
        return {
            "address": self,
            "votes": self.total_votes()
        }

    def save(self, *args, **kwargs):
        return super(MedicalInstitutionLocation, self).save(*args, **kwargs)

    def vote_up(self, user):
        try:
            return MedicalInstitutionLocationVote.objects.create(
                type='Up',
                voter=user,
                medical_institution_location=self
            )
        except IntegrityError as e:
            raise IntegrityError

    def vote_down(self, user):
        try:
            return MedicalInstitutionLocationVote.objects.create(
                type='Down',
                voter=user,
                medical_institution_location=self
            )
        except IntegrityError as e:
            raise IntegrityError

    def get_ups(self):
        return self.medical_institution_location_votes.filter(type='Up').count()

    def get_downs(self):
        return self.medical_institution_location_votes.filter(type='Down').count()

    def total_votes(self):
        return self.get_ups() - self.get_downs()

    def user_has_voted(self, user):
        return self.medical_institution_location_votes.filter(voter=user).count() > 0


class MedicalInstitutionLocationVote(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    type = models.CharField(max_length=4, choices=(('Up', 'Up'), ('Down', 'Down')))
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship Fields
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="user_votes_medical_institution_location"
    )
    medical_institution_location = models.ForeignKey(
        'doctor_profiles.MedicalInstitutionLocation',
        on_delete=models.CASCADE, related_name="medical_institution_location_votes"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('voter', 'medical_institution_location', 'type')

    def __str__(self):
        return f'{type}'


class MedicalInstitutionCoordinate(models.Model):
    # Fields
    lat = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    lon = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    medical_institution = models.ForeignKey(
        'doctor_profiles.MedicalInstitution',
        on_delete=models.CASCADE, related_name="medical_institution_coordinates"
    )
    suggested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="medical_institution_coordinate_suggestions",
        null=True, blank=True, default=None
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('lat', 'lon', 'medical_institution')

    def __str__(self):
        return f'{self.lat}, {self.lon}'

    def vote_up(self, user):
        try:
            return MedicalInstitutionCoordinateVote.objects.create(
                type='Up',
                voter=user,
                coordinate=self
            )
        except IntegrityError as e:
            raise IntegrityError

    def vote_down(self, user):
        try:
            return MedicalInstitutionCoordinateVote.objects.create(
                type='Down',
                voter=user,
                coordinate=self
            )
        except IntegrityError as e:
            raise IntegrityError

    def get_ups(self):
        return self.medical_institution_coordinate_votes.filter(type='Up').count()

    def get_downs(self):
        return self.medical_institution_coordinate_votes.filter(type='Down').count()

    def total_votes(self):
        return self.get_ups() - self.get_downs()

    def user_has_voted(self, user):
        return self.medical_institution_coordinate_votes.filter(voter=user).count() > 0


class MedicalInstitutionCoordinateVote(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    type = models.CharField(max_length=4, choices=(('Up', 'Up'), ('Down', 'Down')))
    metadata = JSONField(default=dict, blank=True, null=True)

    # Relationship Fields
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="user_votes_medical_institution_coordinate"
    )
    coordinate = models.ForeignKey(
        'doctor_profiles.MedicalInstitutionCoordinate',
        on_delete=models.CASCADE, related_name="medical_institution_coordinate_votes"
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('voter', 'coordinate', 'type')

    def __str__(self):
        return f'{type}'


@receiver(post_save, sender=MedicalInstitutionLocation)
def autocreate_coordinates(sender, instance=None, created=False, **kwargs):
    if created:
        address = f'{instance.address} {instance.city.name}'
        payload = {
            'format': 'json',
            'addressdetails': 1,
            'limit': 1,
            'q': address
        }

        result = requests.get('https://nominatim.openstreetmap.org/search', params=payload)
        if result.status_code == 200:
            response = result.json()
            if len(response) > 0:
                lat = response[0]['lat']
                lon = response[0]['lon']
                MedicalInstitutionCoordinate.objects.create(
                    lat=lat,
                    lon=lon,
                    suggested_by=instance.suggested_by,
                    medical_institution=instance.medical_institution
                )
