from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from doctor_profiles.forms import MedicalInstitutionLocationForm
from doctor_profiles.models import MedicalInstitution
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor


class DoctorProfileMedicalInstitutionSettingsHomeView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Medical Institutions',
            'location': 'doctor_profile_settings',
            'sublocation': 'home',
            'medical_institutions': request.user.doctor_profile().get_medical_institutions()
        }

        return render(request, 'neo/doctor_profiles/medical_institutions/settings.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileMedicalInstitutionConnect(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))

        if request.user.doctor_profile():
            return HttpResponseRedirect(
                f"{reverse('doctor_profile_settings_medical_institution_create_connection')}?id={medical_institution.id}"
            )
        else:
            # redirect somewhere else
            pass


class DoctorProfileMedicalInstitutionDoctorCreateConnection(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))

        try:
            MedicalInstitutionDoctor.objects.create(
                doctor=request.user.doctor_profile(),
                medical_institution=medical_institution
            )
        except IntegrityError:
            pass

        return HttpResponseRedirect(
            reverse('doctor_profile_medical_institution_home', kwargs={'slug': medical_institution.slug}))

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileMedicalInstitutionManageConnectionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        rel = get_object_or_404(MedicalInstitutionDoctor, doctor=request.user.doctor_profile(),
                                medical_institution__slug=kwargs['slug'])

        context = {
            'page_title': f'Manage your connection to {rel.medical_institution}',
            'location': 'doctor_profile_medical_institution',
            'sublocation': 'connection',
            'rel': rel,
            'submit_location_form': MedicalInstitutionLocationForm
        }

        return render(request, 'neo/doctor_profiles/medical_institutions/manage_connection.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
