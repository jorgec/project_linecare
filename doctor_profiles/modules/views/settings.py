from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View

from doctor_profiles.forms import MedicalDegreeForm, DoctorDegreeEditForm, SpecializationForm


class DoctorProfileSettingsHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Doctor Settings',
            'location': 'doctor_profile_settings',
            'sublocation': 'home',
        }

        return render(request, 'neo/doctor_profiles/settings/home.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileMedicalDegreeSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Medical Degree',
            'location': 'doctor_profile_settings',
            'sublocation': 'degree',
            'medical_degree_form': MedicalDegreeForm,

        }

        return render(request, 'neo/doctor_profiles/settings/medical_degree.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileSpecializationSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Specialization',
            'location': 'doctor_profile_settings',
            'sublocation': 'specialization',
            'specialization_form': SpecializationForm,

        }

        return render(request, 'neo/doctor_profiles/settings/specialization.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileAssociationSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Association',
            'location': 'doctor_profile_settings',
            'sublocation': 'association',

        }

        return render(request, 'neo/doctor_profiles/settings/association.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileInsuranceSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Insurance',
            'location': 'doctor_profile_settings',
            'sublocation': 'insurance',

        }

        return render(request, 'neo/doctor_profiles/settings/insurance.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


