from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class DoctorProfileMedicalInstitutionSettingsHomeView(LoginRequiredMixin, View):


    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Medical Institutions',
            'location': 'doctor_profile_settings',
            'sublocation': 'institution',
        }

        return render(request, 'neo/doctor_profiles/medical_institutions/home.html', context)
