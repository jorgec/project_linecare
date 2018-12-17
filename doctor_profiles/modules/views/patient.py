from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import View

from doctor_profiles.models import PatientAppointment


class DoctorProfilePatientAppointmentDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment', None))

        context = {
            'page_title': f'Appointment for {appointment.patient} on {appointment.schedule_day.nice_name} at {appointment.medical_institution}',
            'location': 'doctor_profile_patients',
            'sublocation': 'detail',
            'doctor': doctor,
            'patient': appointment.patient,
            'appointment': appointment
        }

        return render(request, 'neo/doctor_profiles/patient/home.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
