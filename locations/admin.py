from django import forms
from django.contrib import admin

from .models import Region, Province, City, ProvinceCoordinate, CityCoordinate, \
    RegionCoordinate, Country, Barangay, BarangayCoordinate


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso3']
    search_fields = ['name']
    readonly_fields = ['iso', 'iso3', 'numcode', 'phonecode']


admin.site.register(Country, CountryAdmin)


class RegionAdminForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class RegionAdmin(admin.ModelAdmin):
    form = RegionAdminForm
    list_display = ['name', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']
    search_fields = ['name']


admin.site.register(Region, RegionAdmin)


class ProvinceAdminForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'


class ProvinceAdmin(admin.ModelAdmin):
    form = ProvinceAdminForm
    list_display = ['name', 'region', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']
    list_filter = ['region', ]
    search_fields = ['name']


admin.site.register(Province, ProvinceAdmin)


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = ['name', 'slug', 'province']
    readonly_fields = ['created', 'last_updated']
    list_filter = ['province', ]
    search_fields = ['name']


admin.site.register(City, CityAdmin)


class RegionCoordinateAdmin(admin.ModelAdmin):
    list_display = ['region', 'lat', 'lon', 'is_approved']
    readonly_fields = ['created', 'last_updated']


admin.site.register(RegionCoordinate, RegionCoordinateAdmin)


class ProvinceCoordinateAdminForm(forms.ModelForm):
    class Meta:
        model = ProvinceCoordinate
        fields = '__all__'


class ProvinceCoordinateAdmin(admin.ModelAdmin):
    form = ProvinceCoordinateAdminForm
    list_display = ['province', 'created', 'last_updated', 'lat', 'lon', 'is_approved']
    readonly_fields = ['created', 'last_updated']
    list_filter = ['province']
    search_fields = ['province__name']


admin.site.register(ProvinceCoordinate, ProvinceCoordinateAdmin)


class CityCoordinateAdminForm(forms.ModelForm):
    class Meta:
        model = CityCoordinate
        fields = '__all__'


class CityCoordinateAdmin(admin.ModelAdmin):
    form = CityCoordinateAdminForm
    list_display = ['city', 'created', 'last_updated', 'lat', 'lon', 'is_approved']
    readonly_fields = ['created', 'last_updated']
    list_filter = ['city']
    search_fields = ['city__name']


admin.site.register(CityCoordinate, CityCoordinateAdmin)


class BarangayAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    def city(self):
        return


class BarangayCoordinateAdmin(admin.ModelAdmin):
    list_display = ['barangay', 'lat', 'lon']
    list_filter = ['barangay']
    search_fields = ['barangay']


admin.site.register(Barangay, BarangayAdmin)
admin.site.register(BarangayCoordinate, BarangayCoordinateAdmin)
