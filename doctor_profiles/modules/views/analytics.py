from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from datesdim.models import DateDim


class DoctorProfileAnalyticsPatientByCheckupAggregateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        date = DateDim.objects.today()
        context = {
            'page_title': 'Patient Checkups Overview',
            'location': 'doctor_profile_analytics',
            'sublocation': 'patient_checkup_overview',
            'doctor': doctor,
            'medical_institutions': doctor.get_medical_institutions(),
            'date': date
        }

        return render(request, 'neo/doctor_profiles/analytics/patient_by_checkup_aggregate.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
