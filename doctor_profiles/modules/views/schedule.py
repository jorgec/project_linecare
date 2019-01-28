from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from rest_framework.utils import json

from biometrics.forms import BiometricForm
from datesdim.models import DateDim
from doctor_profiles.constants import APPOINTMENT_TYPES
from doctor_profiles.models import MedicalInstitution, PatientAppointment, DoctorScheduleDay, DoctorProfile
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
            return HttpResponseRedirect(reverse(
                'doctor_profile_schedule_detail',
                kwargs={
                    'medical_institution': medical_institution.slug
                }
            ))
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
            'doctor_sched_options': json.dumps(rel.metadata.get('durations', {})),
            'doctor_fee_options': json.dumps(rel.metadata.get('fees', {})),
            'today': DateDim.objects.today(),
            'tomorrow': date.tomorrow(),
            'yesterday': date.yesterday(),
            'schedules': doctor.get_schedule_on_day(day=date, medical_institution=medical_institution),
            'genders': Gender.objects.all(),
            'biometrics_form': biometrics_form,
        }

        return render(request, 'neo/doctor_profiles/schedule/queue.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileScheduleHistory(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()

        if 'medical_institution' in kwargs:
            medical_institution = get_object_or_404(MedicalInstitution, slug=kwargs['medical_institution'])
        else:
            medical_institution = get_object_or_404(MedicalInstitution,
                                                    slug=request.GET.get('medical_institution', None))

        if not doctor:
            try:
                doctor = DoctorProfile.objects.get(id=request.GET.get('doctor_id', None))
            except DoctorProfile.DoesNotExist:
                return HttpResponseRedirect(reverse('/403'))
            # check if receptionist
            receptionist = request.user.receptionist_profile()
            if not receptionist:
                return HttpResponseRedirect(reverse('/403'))

            conn = doctor.verify_receptionist(receptionist=receptionist, medical_institution=medical_institution)
            if not conn:
                return HttpResponseRedirect(reverse('/403'))

        rel = get_object_or_404(MedicalInstitutionDoctor, doctor=doctor, medical_institution=medical_institution)

        date = request.GET.get('date', None)
        if not date:
            date = DateDim.objects.today()
        else:
            date = DateDim.objects.parse_get(date)
            if not date:
                date = DateDim.objects.today()

        appointments = PatientAppointment.objects.filter(
                doctor=doctor,
                medical_institution=medical_institution,
                schedule_day=date
            ).order_by('time_start__minutes_since')

        context = {
            'page_title': f'Appointment History in {rel.medical_institution} on {date}',
            'location': 'doctor_profile_manage_schedule',
            'sublocation': 'detail',
            'user': request.user,
            'profile': doctor,
            'doctor': doctor,
            'rel': rel,
            'medical_institution': medical_institution,
            'date': date,
            'appointments': appointments,
            'today': DateDim.objects.today(),
            'tomorrow': date.tomorrow(),
            'yesterday': date.yesterday(),
        }

        return render(request, 'neo/doctor_profiles/schedule/queue_history.html', context)

    def test_func(self):
        return self.request.user.doctor_profile() or self.request.user.receptionist_profile()

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


class DoctorProfileScheduleList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.doctor_profile():
            doctor = request.user.doctor_profile()

            context = {
                'page_title': f'Appointment history for {doctor}',
                'location': 'doctor_profile_manage_schedule',
                'sublocation': 'detail',
                'user': request.user,
                'doctor': doctor,
            }

            return render(request, 'neo/doctor_profiles/schedule/list.html', context)
        elif request.user.receptionist_profile():
            doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))
            receptionist = request.user.receptionist_profile()

            if not receptionist:
                raise PermissionDenied(self.get_permission_denied_message())

            if not doctor.verify_receptionist(receptionist=receptionist):
                raise PermissionDenied(self.get_permission_denied_message())

            context = {
                'page_title': f'Appointment history for {doctor}',
                'location': 'doctor_profile_manage_schedule',
                'sublocation': 'detail',
                'user': request.user,
                'receptionist': receptionist,
                'doctor': doctor,
            }

            return render(request, 'neo/receptionist_profiles/schedule/list.html', context)

    def test_func(self):
        return self.request.user.doctor_profile() or self.request.user.receptionist_profile()