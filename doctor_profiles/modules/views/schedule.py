from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.utils import json

from biometrics.forms import BiometricForm
from datesdim.models import DateDim
from doctor_profiles.constants import APPOINTMENT_TYPES
from doctor_profiles.models import MedicalInstitution
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from profiles.models import Gender


class DoctorProfileMedicalInstitutionScheduleList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        medical_institution = get_object_or_404(MedicalInstitution, slug=kwargs['medical_institution'])
        rel = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor, medical_institution=medical_institution)
        context = {
            'page_title': f'Managing schedule {medical_institution}',
            'location': 'doctor_profile_manage_schedule',
            'sublocation': 'list',
            'user': request.user,
            'profile': doctor,
            'doctor': doctor,
            'rel': rel
        }

        return render(request, 'neo/doctor_profiles/schedule/home.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileScheduleDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        if 'medical_institution' in kwargs:
            medical_institution = get_object_or_404(MedicalInstitution, slug=kwargs['medical_institution'])
        else:
            medical_institution = get_object_or_404(MedicalInstitution, slug=request.GET.get('medical_institution', None))
        rel = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor, medical_institution=medical_institution)

        date = request.GET.get('date', None)
        if not date:
            date = DateDim.objects.today()
        else:
            date = DateDim.objects.parse_get(date)
            if not date:
                date = DateDim.objects.today()

        biometrics_form = BiometricForm

        context = {
            'page_title': f'Queue in {rel.medical_institution} on {date}',
            'location': 'doctor_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'profile': doctor,
            'doctor': doctor,
            'rel': rel,
            'medical_institution': medical_institution,
            'date': date,
            'appointment_types': APPOINTMENT_TYPES,
            'doctor_sched_options': json.dumps(doctor.get_options('schedule_options')),
            'today': DateDim.objects.today(),
            'tomorrow': date.tomorrow(),
            'yesterday': date.yesterday(),
            'schedules': doctor.get_schedule_on_day(day=date, medical_institution=medical_institution),
            'genders': Gender.objects.all(),
            'biometrics_form': biometrics_form
        }

        return render(request, 'neo/doctor_profiles/schedule/queue.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileScheduleCalendarMonth(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()

        context = {
            'page_title': f'Calendar for {doctor}',
            'location': 'doctor_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'doctor': doctor,
        }

        return render(request, 'neo/doctor_profiles/schedule/calendar.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
