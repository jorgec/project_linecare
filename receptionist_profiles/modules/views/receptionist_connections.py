from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from doctor_profiles.forms import MedicalInstitutionLocationForm
from doctor_profiles.models import MedicalInstitution
from receptionist_profiles.models.receptionist_profile_model import ReceptionistConnection


class ReceptionistProfileMedicalInstitutionSettingsHomeView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Medical Institutions',
            'location': 'receptionist_profile_settings',
            'sublocation': 'home',
            'medical_institutions': request.user.receptionist_profile().get_medical_institutions_rel()
        }

        return render(request, 'neo/receptionist_profiles/medical_institutions/settings.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()


class ReceptionistMedicalInstitutionConnect(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))

        if request.user.receptionist_profile():
            return HttpResponseRedirect(
                f"{reverse('receptionist_profile_settings_medical_institution_create_connection')}?id={medical_institution.id}"
            )
        else:
            # redirect somewhere else
            pass


class ReceptionistProfileMedicalInstitutionCreateConnection(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        medical_institution = get_object_or_404(MedicalInstitution, id=request.GET.get('id', None))

        try:
            ReceptionistConnection.objects.create(
                receptionist=request.user.receptionist_profile(),
                medical_institution=medical_institution,
                doctor=None
            )
        except IntegrityError:
            pass

        return HttpResponseRedirect(
            reverse('receptionist_profile_medical_institution_home', kwargs={'slug': medical_institution.slug}))

    def test_func(self):
        return self.request.user.receptionist_profile()


class ReceptionistProfileMedicalInstitutionManageConnectionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        rel = get_object_or_404(ReceptionistConnection, receptionist=request.user.receptionist_profile(),
                                medical_institution__slug=kwargs['slug'], doctor=None)

        context = {
            'page_title': f'Manage your connection to {rel.medical_institution}',
            'location': 'doctor_profile_medical_institution',
            'sublocation': 'connection',
            'rel': rel,
            'submit_location_form': MedicalInstitutionLocationForm
        }

        return render(request, 'neo/receptionist_profiles/medical_institutions/manage_connection.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()


class ReceptionistProfileRemoveConnectionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        receptionsit = request.user.receptionist_profile()
        medical_institution = MedicalInstitution.objects.get(slug=kwargs['slug'])

        connections = ReceptionistConnection.objects.filter(receptionist=receptionsit, medical_institution=medical_institution)
        connections.delete()

        return HttpResponseRedirect(reverse(
            'receptionist_profile_settings_medical_institution'
        ))

    def test_func(self):
        return self.request.user.receptionist_profile()