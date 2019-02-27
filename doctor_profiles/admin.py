from django.contrib import admin

# Register your models here.
from doctor_profiles.models import Specialization, InsuranceProvider, MedicalDegree, MedicalAssociation, DoctorProfile, \
    DoctorDegree, MedicalInstitution, MedicalInstitutionType, MedicalInstitutionLocation, \
    MedicalInstitutionLocationVote, MedicalInstitutionPhone, MedicalInstitutionPhoneVote, LabTest, QuestionChoiceGroup, \
    Questionnaire, DoctorQuestionnaire, QuestionnaireSection, Question, SectionQuestion, Choice, ChoiceGroup, \
    ChoiceGroupItem


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
        return obj.get_degrees_rel()


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


class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases')
    search_fields = ('name', 'aliases')


admin.site.register(LabTest, LabTestAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'name', 'slug', 'description', 'instructions',
                    'restriction']


admin.site.register(Questionnaire, QuestionnaireAdmin)


class DoctorQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'is_creator', 'is_required', 'hook_location']


admin.site.register(DoctorQuestionnaire, DoctorQuestionnaireAdmin)


class QuestionnaireSectionAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'order', 'name', 'description',
                    'instructions']


admin.site.register(QuestionnaireSection, QuestionnaireSectionAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'answer_type', 'answer_selection_type', 'answer_data_type']


admin.site.register(Question, QuestionAdmin)


class SectionQuestionAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'order']


admin.site.register(SectionQuestion, SectionQuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'name', 'text', 'img', 'value']


admin.site.register(Choice, ChoiceAdmin)


class ChoiceGroupAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'name']


admin.site.register(ChoiceGroup, ChoiceGroupAdmin)


class ChoiceGroupItemAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved', 'order']


admin.site.register(ChoiceGroupItem, ChoiceGroupItemAdmin)


class QuestionChoiceGroupAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_updated', 'metadata', 'is_approved']


admin.site.register(QuestionChoiceGroup, QuestionChoiceGroupAdmin)
