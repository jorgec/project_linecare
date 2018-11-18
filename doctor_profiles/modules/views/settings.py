from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View

from doctor_profiles.forms import MedicalDegreeForm, DoctorDegreeEditForm


class DoctorProfileMedicalDegreeSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Career Settings',
            'location': 'doctor_profile_career',
            'sublocation': 'degree',
            'medical_degree_form': MedicalDegreeForm,
            'doctor_degree_edit_form': DoctorDegreeEditForm

        }

        return render(request, 'neo/doctor_profiles/settings/career.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
