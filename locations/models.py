from django.conf import settings
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Country(models.Model):
    iso = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=80)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True, null=True)
    nicename = models.CharField(max_length=120, blank=True, null=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    numcode = models.PositiveSmallIntegerField(blank=True, null=True)
    phonecode = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        db_table = 'countries'

    def __str__(self):
        return u'%s' % self.nicename


class Region(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)
    extra_1 = models.CharField(max_length=50, blank=True, null=True)

    # Relationship Fields
    country = models.ForeignKey(Country, blank=True, null=True, related_name='region_country', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        db_table = 'regions'

    def __str__(self):
        return u'%s' % self.name


class Province(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)

    # Relationship Fields
    region = models.ForeignKey(Region, null=True, blank=True, related_name='province_region', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, blank=True, related_name='province_country',
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        db_table = 'provinces'

    def __str__(self):
        return u'%s' % self.name

    def get_coords(self):
        try:
            coords = self.provincecoords.get(is_approved=True)
            return {'lat': coords.lat, 'lon': coords.lon}
        except self.provincecoords.DoesNotExist:
            return False


class City(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)

    # Relationship Fields
    province = models.ForeignKey(Province, related_name="city_province", on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'cities'
        db_table = 'cities'

    def __str__(self):
        return u'%s' % self.name

    def get_coords(self):
        try:
            coords = self.citycoords.get(is_approved=True)
            return {'lat': coords.lat, 'lon': coords.lon}
        except self.citycoords.DoesNotExist:
            return False


class Barangay(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)

    # Relationship Fields
    city = models.ForeignKey(City, related_name='brgy_city', on_delete=models.CASCADE)

    def __str__(self):
        return "Brgy. {}, {}".format(self.name, self.city)


class RegionCoordinate(models.Model):
    # Fields
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    lon = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    is_approved = models.BooleanField(default=False)

    # Relationship Fields
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('region__name',)
        db_table = 'region_coordinates'

    def __str__(self):
        return u'%s' % self.region.name


class ProvinceCoordinate(models.Model):
    # Fields
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    lon = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    is_approved = models.BooleanField(default=False)
    d = models.TextField(blank=True, null=True)

    # Relationship Fields
    province = models.ForeignKey(Province, related_name='provincecoords', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('province',)
        db_table = 'province_coordinates'

    def __str__(self):
        return u'%s' % self.province.name


class CityCoordinate(models.Model):
    # Fields
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    lon = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    is_approved = models.BooleanField(default=False)

    # Relationship Fields
    city = models.ForeignKey(City, related_name='citycoords', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('city',)
        db_table = 'city_coordinates'

    def __str__(self):
        return u'%s' % self.city.name


class BarangayCoordinate(models.Model):
    # Fields
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False)
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    lon = models.DecimalField(max_digits=15, decimal_places=12, blank=True)
    is_approved = models.BooleanField(default=False)

    # Relationship Fields
    barangay = models.ForeignKey(Barangay, related_name='brgycoords', on_delete=models.CASCADE)

    class Meta:
        ordering = ('barangay',)
        db_table = 'brgy_coordinates'

    def __str__(self):
        return '{}'.format(self.barangay)

    def coords(self):
        return {'lat': self.lat, 'lon': self.lon}
