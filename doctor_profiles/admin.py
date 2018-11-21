from django.contrib import admin

# Register your models here.
from doctor_profiles.models import Specialization, InsuranceProvider, MedicalDegree, MedicalAssociation, DoctorProfile, \
    DoctorDegree, MedicalInstitution, MedicalInstitutionType, MedicalInstitutionLocation, \
    MedicalInstitutionLocationVote, MedicalInstitutionPhone, MedicalInstitutionPhoneVote


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'parent')


admin.site.register(Specialization, SpecializationAdmin)


class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(InsuranceProvider, InsuranceProviderAdmin)


class MedicalDegreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')


admin.site.register(MedicalDegree, MedicalDegreeAdmin)


class MedicalAssociationAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')


admin.site.register(MedicalAssociation, MedicalAssociationAdmin)


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_degrees')

    def get_degrees(self, obj):
        return obj.get_degrees()


admin.site.register(DoctorProfile, DoctorProfileAdmin)


class DoctorDegreeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'degree', 'school', 'year_attained', 'license_number')


admin.site.register(DoctorDegree, DoctorDegreeAdmin)

admin.site.register(MedicalInstitution)
admin.site.register(MedicalInstitutionType)
admin.site.register(MedicalInstitutionLocation)
admin.site.register(MedicalInstitutionLocationVote)
admin.site.register(MedicalInstitutionPhone)
admin.site.register(MedicalInstitutionPhoneVote)
