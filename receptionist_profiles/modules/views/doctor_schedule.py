from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from datesdim.models import DateDim
from doctor_profiles.models import DoctorProfile, MedicalInstitution
from receptionist_profiles.models import ReceptionistProfile
from receptionist_profiles.models.receptionist_profile_model import ReceptionistConnection


class ReceptionistProfileDoctorScheduleList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ReceptionistProfile, user=request.user)
        doctor = get_object_or_404(DoctorProfile, id=kwargs['doctor_id'])
        medical_institution = get_object_or_404(MedicalInstitution, slug=kwargs['medical_institution'])
        rel = get_object_or_404(ReceptionistConnection, receptionist=profile, doctor=doctor,
                                medical_institution=medical_institution)
        context = {
            'page_title': f'Managing schedule for {doctor} in {rel.medical_institution}',
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


class ReceptionistProfileDoctorScheduleDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ReceptionistProfile, user=request.user)
        doctor = get_object_or_404(DoctorProfile, id=kwargs['doctor_id'])
        medical_institution = get_object_or_404(MedicalInstitution, slug=kwargs['medical_institution'])
        rel = get_object_or_404(ReceptionistConnection, receptionist=profile, doctor=doctor,
                                medical_institution=medical_institution)

        date = request.GET.get('date', DateDim.objects.today())

        context = {
            'page_title': f'Queue for {doctor} in {rel.medical_institution}',
            'location': 'receptionist_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'profile': profile,
            'doctor': doctor,
            'rel': rel,
            'medical_institution': medical_institution,
            'date': date
        }

        return render(request, 'neo/receptionist_profiles/schedule/queue.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()
