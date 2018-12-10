from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from doctor_profiles.models import DoctorProfile
from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.models.receptionist_profile_model import ReceptionistConnection


class ReceptionistProfileDoctorScheduleList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ReceptionistProfile, user=request.user)
        doctor = get_object_or_404(DoctorProfile, id=kwargs['doctor_id'])
        rel = get_object_or_404(ReceptionistConnection, receptionist=profile, doctor=doctor)
        context = {
            'page_title': f'Managing schedule for {doctor}',
            'location': 'receptionist_profile_manage_schedule',
            'sublocation': 'list',
            'user': request.user,
            'profile': profile,
            'doctor': doctor,
            'rel': rel
        }

        return render(request, 'neo/receptionist_profiles/schedule/home.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()
