from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from datesdim.models import DateDim
from doctor_profiles.constants import APPOINTMENT_TYPES


class DoctorProfileAnalyticsPatientByCheckupAggregateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        date = DateDim.objects.today()

        appointment_keys = [at[1] for at in APPOINTMENT_TYPES]

        context = {
            'page_title': 'Patient Checkups Overview',
            'location': 'doctor_profile_analytics',
            'sublocation': 'patient_checkup_overview',
            'doctor': doctor,
            'medical_institutions': doctor.get_medical_institutions(),
            'date': date,
            'appointment_keys': appointment_keys,
            'appointment_types': APPOINTMENT_TYPES
        }

        return render(request, 'neo/doctor_profiles/analytics/patient_by_checkup_aggregate.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileAnalyticsPatientBySymptomAggregateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        date = DateDim.objects.today()

        appointment_keys = [at[1] for at in APPOINTMENT_TYPES]

        context = {
            'page_title': 'Patient Symptoms Overview',
            'location': 'doctor_profile_analytics',
            'sublocation': 'patient_symptoms_overview',
            'doctor': doctor,
            'medical_institutions': doctor.get_medical_institutions(),
            'date': date,
            'appointment_keys': appointment_keys,
            'appointment_types': APPOINTMENT_TYPES
        }

        return render(request, 'neo/doctor_profiles/analytics/symptoms_by_checkup_aggregate.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()

