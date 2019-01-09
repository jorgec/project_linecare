from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.utils import json

from biometrics.forms import BiometricForm
from datesdim.models import DateDim
from doctor_profiles.constants import APPOINTMENT_TYPES
from doctor_profiles.models import DoctorProfile, MedicalInstitution, MedicalInstitutionDoctor
from profiles.models import Gender
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

        date = request.GET.get('date', None)
        if not date:
            date = DateDim.objects.today()
        else:
            date = DateDim.objects.parse_get(date)
            if not date:
                date = DateDim.objects.today()

        biometrics_form = BiometricForm

        doctor_rel = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor, medical_institution=medical_institution)

        context = {
            'page_title': f'Queue for {doctor} in {rel.medical_institution}',
            'location': 'receptionist_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'profile': profile,
            'doctor': doctor,
            'rel': rel,
            'medical_institution': medical_institution,
            'date': date,
            'appointment_types': APPOINTMENT_TYPES,
            'doctor_sched_options': json.dumps(doctor_rel.metadata.get('durations', {})),
            'doctor_fee_options': json.dumps(doctor_rel.metadata.get('fees', {})),
            'today': DateDim.objects.today(),
            'tomorrow': date.tomorrow(),
            'yesterday': date.yesterday(),
            'schedules': doctor.get_schedule_on_day(day=date, medical_institution=medical_institution),
            'genders': Gender.objects.all(),
            'biometrics_form': biometrics_form
        }

        return render(request, 'neo/receptionist_profiles/schedule/queue.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()


class ReceptionistProfileDoctorScheduleCalendarMonth(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ReceptionistProfile, user=request.user)
        doctor = get_object_or_404(DoctorProfile, id=kwargs['doctor_id'])

        context = {
            'page_title': f'Calendar for {doctor}',
            'location': 'receptionist_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'profile': profile,
            'doctor': doctor,
        }

        return render(request, 'neo/receptionist_profiles/schedule/calendar.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()
