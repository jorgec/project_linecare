from django.contrib import admin

# Register your models here.
from doctors.models import DoctorProfile, DoctorSpecialty, MedicalSubject, Specialty

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'year_started')
    list_filter = ('license_number', 'year_started')
    search_fields = ('license_number',)

admin.site.register(DoctorProfile, DoctorProfileAdmin)

class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(Specialty, SpecialtyAdmin)


class DoctorSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'specialty')
    list_filter = ('doctor', 'specialty')
    search_fields = ('doctor',)

admin.site.register(DoctorSpecialty, DoctorSpecialtyAdmin)

class MedicalSubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(MedicalSubject, MedicalSubjectAdmin)